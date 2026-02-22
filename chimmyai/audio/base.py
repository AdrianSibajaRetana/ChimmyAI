"""Interfaz abstracta para manejo de audio."""
from abc import ABC, abstractmethod

class AudioHandler(ABC):
    """Contrato para implementaciones de captura/reproducción de audio.

    Equivalente en C#: interface IAudioHandler
    """

    @abstractmethod
    def record(self) -> bytes:
        """Captura audio del micrófono y devuelve los datos."""
        ...

    @abstractmethod
    def play(self, audio_data: bytes) -> None:
        """Reproduce datos de audio por el altavoz."""
        ...
