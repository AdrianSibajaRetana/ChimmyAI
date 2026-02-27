from .base import BaseLLM


class LocalLLM(BaseLLM):
    """Placeholder para una implementación local de LLM."""

    async def chat(self, prompt: str) -> str:
        return f"[LocalLLM placeholder] Simulating LLM behavior. Received: {prompt}"

    async def close(self) -> None:
        pass
