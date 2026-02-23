import asyncio
import pyttsx3

from .base import TextToSpeech

class Pyttsx3TTS(TextToSpeech):
    """Implementación concreta de TTS usando pyttsx3 (offline)."""

    def __init__(self, voice_id: str | None = None, rate: int = 180):        
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)
            
        if voice_id:
            self.engine.setProperty("voice", voice_id)
            
    async def synthesize(self, text: str) -> None:
        """
        Convierte texto a voz y lo reproduce.
        Se ejecuta en un thread separado porque pyttsx3 es bloqueante.
        """
        return await asyncio.to_thread(self._speak_sync, text)

    def _speak_sync(self, text: str):        
        self.engine.say(text)
        self.engine.runAndWait()