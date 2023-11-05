import asyncio
import logging
from typing import Any, Generator

from ctransformers import AutoModelForCausalLM

from google.protobuf.internal.containers import RepeatedCompositeFieldContainer

# completion
from leapfrogai import (
    CompletionChoice,
    CompletionFinishReason,
    CompletionRequest,
    CompletionResponse,
    CompletionUsage,
    GrpcContext,
    serve,
)

# chat
from leapfrogai import (
    ChatCompletionRequest,
    ChatCompletionChoice,
    ChatItem,
    ChatRole,
    ChatCompletionResponse
)

logger = logging.getLogger(__name__)

# Prompt Templates
SYSTEM_FORMAT = "<|im_start|>system\n{}<|im_end|>\n"
USER_FORMAT = "<|im_start|>user\n{}<|im_end|>\n"
ASSISTANT_FORMAT = "<|im_start|>assistant\n{}<|im_end|>\n"
# what gets appended to the end of the prompt to open the assistant's part of the conversation
RESPONSE_PREFIX = ASSISTANT_FORMAT.split("{}")[0]

def chat_items_to_prompt(chat_items: RepeatedCompositeFieldContainer[ChatItem]) -> str:
    """Converts a repeated ChatItem from a ChatCompletionRequest proto into a string

    This is the actual string that gets fed into the model to generate the outputs
    """
    prompt = ""
    for item in chat_items:
        if item.role == ChatRole.SYSTEM:
            prompt += SYSTEM_FORMAT.format(item.content)
        elif item.role == ChatRole.ASSISTANT:
            prompt += ASSISTANT_FORMAT.format(item.content)
        elif item.role == ChatRole.USER:
            prompt += USER_FORMAT.format(item.content)
        elif item.role == ChatRole.FUNCTION:
            logging.warning(
                "ChatRole FUNCTION is not implemented for this model and this ChatItem will be ignored."
            )
    # add the response prefix to start the model's reponse
    prompt += RESPONSE_PREFIX
    return prompt

class CTransformers:
    MODEL_PATH = ".model/synthia-7b-v2.0.Q4_K_M.gguf"
    MODEL_TYPE = "mistral"

    def __init__(self):
        # Load (and cache) the model from the pretrained model.
        self.llm = AutoModelForCausalLM.from_pretrained(
            model_path_or_repo_id=self.MODEL_PATH,
            model_type=self.MODEL_TYPE,
            context_length=8192,
        )
        logger.info("Loaded model.")

    def chat_stream(self, request: ChatCompletionRequest) -> Generator[str, Any, Any]:
        """Implements the logic for the chat endpoint"""
        # convert chat items to prompt and tokenize
        prompt = chat_items_to_prompt(request.chat_items)

        # create text streamer and validate parameters
        max_new_tokens = 1536 if request.max_new_tokens == 0 else request.max_new_tokens
        temperature = 0.1 if request.temperature == 0.0 else request.temperature
        top_p = 1.0 if request.top_p == 0.0 else request.top_p
        top_k = 0 if request.top_k == 0.0 else int(request.top_k)

        for text in self.llm(
            prompt=prompt,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            stop=["</s>","<|im_end|>"],
            stream=True
        ):
            print(text)
            yield text

    def ChatComplete(
            self, request: ChatCompletionRequest, context: GrpcContext
    ) -> ChatCompletionResponse:
        logger.info("CHATCOMPLETE:\n---")
        chat_stream = self.chat_stream(request)

        content = ""
        for text_chunk in chat_stream:
            content += text_chunk

        item = ChatItem(role=ChatRole.ASSISTANT, content=content)
        choice = ChatCompletionChoice(index=0, chat_item=item)
        logger.info(choice)
        logger.info("CHATCOMPLETEEND:\n---")
        return ChatCompletionResponse(choices=[choice])
    
    def ChatCompleteStream(
        self, request: ChatCompletionRequest, context: GrpcContext
    ) -> Generator[ChatCompletionResponse, Any, Any]:
        logger.info("CHATCOMPLETESTREAM:\n---")
        chat_stream = self.chat_stream(request)

        for text_chunk in chat_stream:
            item = ChatItem(role=ChatRole.ASSISTANT, content=text_chunk)
            choice = ChatCompletionChoice(index=0, chat_item=item)

            yield ChatCompletionResponse(choices=[choice])

        logger.info("CHATCOMPLETESTREAMEND:\n---")

    def Complete(
        self, request: CompletionRequest, context: GrpcContext
    ) -> CompletionResponse:
        text = self.llm(
            request.prompt,
            max_new_tokens=request.max_new_tokens,
            temperature=request.temperature,
            stop=["</s>"],
            batch_size=512
        )
        completion = CompletionChoice(text=text, index=0)
        logger.info("COMPLETE:\n---")
        logger.info(request.prompt)
        logger.info(completion)
        logger.info("COMPLETE END")
        return CompletionResponse(choices=[completion])

    def CompleteStream(
        self, request: CompletionRequest, context: GrpcContext
    ) -> Generator[CompletionResponse, Any, Any]:
        logger.info("COMPLETESTREAM:\n---")
        logger.info(request.prompt)
        for text in self.llm(
            request.prompt,
            max_new_tokens=request.max_new_tokens,
            temperature=request.temperature,
            stream=True,
            stop=["</s>"],
        ):
            logger.info(text)
            completion = CompletionChoice(text=text, index=0)
            yield CompletionResponse(choices=[completion])
        logger.info("COMPLETESTREAM END")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve(CTransformers()))
