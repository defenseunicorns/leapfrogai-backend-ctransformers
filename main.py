import asyncio
import logging
from typing import Any, Generator

from ctransformers import AutoModelForCausalLM

from leapfrogai import (
    CompletionChoice,
    CompletionFinishReason,
    CompletionRequest,
    CompletionResponse,
    CompletionUsage,
    GrpcContext,
    serve,
)

logger = logging.getLogger(__name__)

class CTransformers:
    MODEL_PATH = ".model/mistral-7b-v0.1.Q2_K.gguf"
    MODEL_TYPE = "mistral"

    def __init__(self):
        # Load (and cache) the model from the pretrained model.
        self.llm = AutoModelForCausalLM.from_pretrained(
            model_path_or_repo_id=self.MODEL_PATH,
            model_type=self.MODEL_TYPE,
        )
        logger.info("Loaded model.") 

    def Complete(
        self, request: CompletionRequest, context: GrpcContext
    ) -> CompletionResponse:
        text = self.llm(
            request.prompt,
            max_new_tokens=request.max_new_tokens,
            temperature=request.temperature,
            #stop=["<|im_end|>"],
            stop=["."],
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
            stop=["."],
        ):
            logger.info(text)
            completion = CompletionChoice(text=text, index=0)
            yield CompletionResponse(choices=[completion])
        logger.info("COMPLETESTREAM END")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve(CTransformers()))
