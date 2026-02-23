import io
import asyncio
import numpy as np
import soundfile as sf
from faster_whisper import WhisperModel

from .base import SpeechToText


class FasterWhisperSpeechToText(SpeechToText):
    """
    Local Speech-to-Text implementation using faster-whisper.
    """

    def __init__(
        self,
        model_size: str = "base",
        device: str = "cpu",
        compute_type: str = "int8",
    ):
        """
        model_size: tiny, base, small, medium, large-v3
        device: "cpu" or "cuda"
        compute_type:
            - int8 (fast, low memory)
            - float16 (GPU)
            - float32 (high precision)
        """

        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.model: WhisperModel | None = None

    def _ensure_model(self) -> None:
        """Lazy-loads the Whisper model on first use."""
        if self.model is None:
            self.model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=self.compute_type,
            )

    async def transcribe(self, audio_data: bytes) -> str:
        """
        Transcribe WAV bytes to text.
        """
        return await asyncio.to_thread(self._transcribe_sync, audio_data)

    def _transcribe_sync(self, audio_data: bytes) -> str:
        self._ensure_model()

        # Convert WAV bytes → numpy float32 array
        buffer = io.BytesIO(audio_data)
        audio_array, samplerate = sf.read(buffer, dtype="float32")

        # Faster-whisper expects mono
        if len(audio_array.shape) > 1:
            audio_array = np.mean(audio_array, axis=1)

        segments, info = self.model.transcribe(audio_array, language="es")

        text = " ".join(segment.text for segment in segments)

        return text.strip()