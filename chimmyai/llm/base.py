"""Interfaz abstracta para el modelo de lenguaje."""
from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """Contrato para implementaciones de LLM.

    Equivalente en C#: interface ILanguageModel
    """

    @abstractmethod
    async def chat(self, prompt: str) -> str:
        """Genera una respuesta a partir de un prompt."""
        ...

    async def close(self) -> None:
        """Libera recursos del cliente. Override en subclases si es necesario."""
        pass
