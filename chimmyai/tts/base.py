"""Interfaz abstracta para Text-to-Speech."""
from abc import ABC, abstractmethod


class TextToSpeech(ABC):
    """Contrato para implementaciones de Text-to-Speech.

    Equivalente en C#: interface ITextToSpeech
    """

    @abstractmethod
    async def synthesize(self, text: str) -> None:
        """Convierte texto en datos de audio."""
        ...
