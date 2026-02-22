"""Interfaz abstracta para Speech-to-Text."""
from abc import ABC, abstractmethod


class BaseSTT(ABC):
    """Contrato para implementaciones de Speech-to-Text.

    Equivalente en C#: interface ISpeechToText
    """

    @abstractmethod
    def transcribe(self, audio_data: bytes) -> str:
        """Convierte audio en texto."""
        ...
