import io
import asyncio
import sounddevice as sd
import soundfile as sf

from .base import AudioHandler


class SoundDeviceAudioHandler(AudioHandler):
    """Implementación concreta del AudioHandler usando sounddevice."""

    def __init__(self, sample_rate: int = 16000, channels: int = 1, duration: int = 5):
        """
        sample_rate: 16kHz (speech optimized)
        channels: 1 (mono)
        duration: segundos por grabación
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.duration = duration

    # ---------- RECORD ----------
    async def record(self) -> bytes:
        """Graba audio y devuelve WAV PCM_16 bytes."""

        return await asyncio.to_thread(self._record_sync)
    
    def _record_sync(self) -> bytes:
        
        frames = int(self.duration * self.sample_rate)

        try:
            audio = sd.rec(
                frames,
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype="int16",
            )
            sd.wait()
        except Exception as e:
            raise RuntimeError("Audio recording failed") from e

        buffer = io.BytesIO()
        sf.write(
            buffer,
            audio,
            self.sample_rate,
            format="WAV",
            subtype="PCM_16",
        )
        buffer.seek(0)

        return buffer.read()
        
    # ---------- PLAY ----------
    async def play(self, audio_data: bytes) -> None:
        """Reproduce audio WAV desde bytes."""
        return await asyncio.to_thread(self._play_sync, audio_data)
                
    def _play_sync(self, audio_data: bytes) -> None:
        try:
            buffer = io.BytesIO(audio_data)
            data, samplerate = sf.read(buffer, dtype="int16")

            sd.play(data, samplerate)
            sd.wait()
        except Exception as e:
            raise RuntimeError("Audio playback failed") from e