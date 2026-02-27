import os
from .base import BaseLLM
from openai import AsyncAzureOpenAI
from chimmyai.config import Config
from pathlib import Path

class AzureOpenAI(BaseLLM):
        def __init__(self):
            prompt_path = Path(__file__).resolve().parent / "prompts" / "chimmy_system.txt"
            self.prompt_system_str = prompt_path.read_text(encoding="utf-8")
            self.api_key = os.getenv("OPEN_API_KEY")
            self.endpoint = os.getenv("OPEN_API_ENDPOINT")
            
            if not self.api_key:
                raise RuntimeError("OPEN_API_KEY not configured")

            if not self.endpoint:
                raise RuntimeError("OPEN_API_ENDPOINT not configured")

            self.client = AsyncAzureOpenAI(
                api_version="2024-12-01-preview",
                azure_endpoint=self.endpoint,
                api_key=self.api_key
            )
            
        async def chat(self, prompt: str) -> str:
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

            return response.choices[0].message.content

