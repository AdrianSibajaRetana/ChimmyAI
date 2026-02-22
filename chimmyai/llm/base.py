"""Interfaz abstracta para el modelo de lenguaje."""
from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """Contrato para implementaciones de LLM.

    Equivalente en C#: interface ILanguageModel
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Genera una respuesta a partir de un prompt."""
        ...
