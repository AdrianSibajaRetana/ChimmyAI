import os
from .base import BaseLLM
from openai import AsyncAzureOpenAI, APIError
from chimmyai.config import Config
from pathlib import Path

class AzureOpenAI(BaseLLM):
        def __init__(self):
            prompt_path = Path(__file__).resolve().parent / "prompts" / "chimmy_system.txt"
            self.prompt_system_str = prompt_path.read_text(encoding="utf-8")
            api_key = os.getenv("OPEN_API_KEY")
            endpoint = os.getenv("OPEN_API_ENDPOINT")
            
            if not api_key:
                raise RuntimeError("OPEN_API_KEY not configured")

            if not endpoint:
                raise RuntimeError("OPEN_API_ENDPOINT not configured")

            self.client = AsyncAzureOpenAI(
                api_version="2024-12-01-preview",
                azure_endpoint=endpoint,
                api_key=api_key
            )
            
        async def chat(self, prompt: str) -> str:
            try:
                response = await self.client.chat.completions.create(
                    model=Config.OPENAI_MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": self.prompt_system_str,
                        },
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    temperature=Config.TEMPERATURE,
                    max_tokens=Config.MAX_TOKENS
                )
            except APIError as e:
                raise RuntimeError(f"LLM request failed: {e}") from e

            if not response.choices:
                raise RuntimeError("LLM returned empty response")

            return response.choices[0].message.content

        async def close(self) -> None:
            await self.client.close()

