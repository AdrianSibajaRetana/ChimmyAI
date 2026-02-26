import io
import asyncio

import numpy as np
import soundfile as sf
import trainer.io

from TTS.api import TTS
from chimmyai.config import Config

# Tacotron2 checkpoints use defaultdict which isn't compatible with
# torch.load(weights_only=True) in PyTorch >=2.6. Safe since models
# come from Coqui's official repository.
trainer.io._WEIGHTS_ONLY = False

from .base import TextToSpeech

class CoquiTTS(TextToSpeech):
    def __init__(self):
        print("CoquiTTS: Inicializando Servicio.")
        self.tts = TTS(Config.TTS_COQUI_MODEL).to(Config.TTS_DEVICE)
        self.sample_rate: int = self.tts.synthesizer.output_sample_rate

    async def synthesize(self, text: str) -> bytes:
        return await asyncio.to_thread(self._synthesize_sync, text)

    def _synthesize_sync(self, text: str) -> bytes:
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