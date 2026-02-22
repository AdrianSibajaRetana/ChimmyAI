"""Interfaz abstracta para Text-to-Speech."""
from abc import ABC, abstractmethod


class BaseTTS(ABC):
    """Contrato para implementaciones de Text-to-Speech.

    Equivalente en C#: interface ITextToSpeech
    """

    @abstractmethod
    def synthesize(self, text: str) -> bytes:
        """Convierte texto en datos de audio."""
        ...
