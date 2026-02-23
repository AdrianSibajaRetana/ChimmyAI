import io
import asyncio

import numpy as np
import soundfile as sf
import trainer.io

from TTS.api import TTS

# Tacotron2 checkpoints use defaultdict which isn't compatible with
# torch.load(weights_only=True) in PyTorch >=2.6. Safe since models
# come from Coqui's official repository.
trainer.io._WEIGHTS_ONLY = False

from .base import TextToSpeech

class CoquiTTS(TextToSpeech):
    """Implementación concreta usando Coqui TTS."""

    def __init__(self, model_name: str = "tts_models/es/mai/tacotron2-DDC"):
        """
        model_name: Modelo español específico.
        """
        self.model_name = model_name
        self.tts: TTS | None = None
        self.sample_rate: int | None = None

    def _ensure_model(self) -> None:
        """Lazy-loads the TTS model on first use."""
        if self.tts is None:
            self.tts = TTS(self.model_name)
            self.sample_rate = self.tts.synthesizer.output_sample_rate

    async def synthesize(self, text: str) -> bytes:
        """
        Convierte texto a WAV bytes.
        Coqui es síncrono → lo ejecutamos en thread pool.
        """
        return await asyncio.to_thread(self._synthesize_sync, text)

    def _synthesize_sync(self, text: str) -> bytes:
        self._ensure_model()

        audio = self.tts.tts(text)

        buffer = io.BytesIO()

        sf.write(
            buffer,
            np.array(audio),
            self.sample_rate,
            format="WAV",
            subtype="PCM_16",
        )

        buffer.seek(0)
        return buffer.read()