from typing import Any, Generator
import os


from leapfrogai import BackendConfig
from leapfrogai.llm import LLM, GenerationConfig
from ctransformers import AutoModelForCausalLM

GPU_ENABLED = (
    False if os.environ.get("GPU_ENABLED", "False").lower() != "true" else True
)

@LLM
class Model:
    backend_config = BackendConfig()

    llm = AutoModelForCausalLM.from_pretrained(
        model_path_or_repo_id=backend_config.model.source,
        context_length=backend_config.max_context_length,
        gpu_layers=99 if GPU_ENABLED == True else 0,
    )

    def generate(
        self, prompt: str, config: GenerationConfig
    ) -> Generator[str, Any, Any]:
        for res in self.llm(
            prompt,
            stream=True,
            temperature=config.temperature,
            max_tokens=config.max_new_tokens,
            top_p=config.top_p,
            top_k=config.top_k,
            stop=self.backend_config.stop_tokens,
        ):
            yield res["choices"][0]["text"]  # type: ignore
