import os
import json
from .base import BaseLLM
from openai import AsyncAzureOpenAI, APIError
from chimmyai.config import Config
from chimmyai.tools.base import ToolRegistry
from chimmyai.tools.defaults import create_default_registry
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

            self._tool_registry = create_default_registry()
            self._openai_tools = self._build_openai_tools()

        def _build_openai_tools(self) -> list[dict] | None:
            """Convierte el ToolRegistry genérico al formato de herramientas de OpenAI."""
            if not self._tool_registry.all_tools():
                return None
            return [
                {
                    "type": "function",
                    "function": {
                        "name": t.name,
                        "description": t.description,
                        "parameters": t.parameters,
                    },
                }
                for t in self._tool_registry.all_tools()
            ]

        async def chat(self, prompt: str) -> str:
            messages = [
                {"role": "system", "content": self.prompt_system_str},
                {"role": "user", "content": prompt},
            ]

            for _ in range(Config.MAX_TOOL_ROUNDS):
                try:
                    kwargs: dict = dict(
                        model=Config.OPENAI_MODEL,
                        messages=messages,
                        temperature=Config.TEMPERATURE,
                        max_tokens=Config.MAX_TOKENS,
                    )
                    if self._openai_tools:
                        kwargs["tools"] = self._openai_tools

                    response = await self.client.chat.completions.create(**kwargs)
                except APIError as e:
                    raise RuntimeError(f"LLM request failed: {e}") from e

                if not response.choices:
                    raise RuntimeError("LLM returned empty response")

                message = response.choices[0].message

                if not message.tool_calls:
                    return message.content or ""

                # El modelo pidió ejecutar herramientas — resolver y continuar.
                messages.append(message.model_dump())
                for tool_call in message.tool_calls:
                    try:
                        arguments = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError as e:
                        result = f"Error: argumentos JSON inválidos: {e}"
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": result,
                        })
                        continue

                    result = self._tool_registry.execute(
                        tool_call.function.name, **arguments
                    )
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    })

            # Safety: si se agotaron los rounds, pedir respuesta final sin herramientas.
            try:
                response = await self.client.chat.completions.create(
                    model=Config.OPENAI_MODEL,
                    messages=messages,
                    temperature=Config.TEMPERATURE,
                    max_tokens=Config.MAX_TOKENS,
                )
            except APIError as e:
                raise RuntimeError(f"LLM request failed: {e}") from e

            if not response.choices:
                raise RuntimeError("LLM returned empty response")

            return response.choices[0].message.content or ""

        async def close(self) -> None:
            await self.client.close()

