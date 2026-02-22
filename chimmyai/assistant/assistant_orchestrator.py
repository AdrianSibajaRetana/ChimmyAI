from chimmyai.audio.base import AudioHandler
from chimmyai.stt.base import SpeechToText

from .base import AssistantOrchestrator

class MainAssistantOrchestrator(AssistantOrchestrator):
    
    def __init__(self, audio: AudioHandler, stt: SpeechToText):
        self.audioHandler = audio
        self.speechToText = stt

    async def handle_voice_interaction(self) -> None:
        print("MainAssistantOrchestrator: Grabando entrada de usuario")
        audio_bytes = self.audioHandler.record()
        
        print("MainAssistantOrchestrator: Transcribiendo...")
        transcript = await self.speechToText.transcribe(audio_bytes)
        
        print(f"MainAssistantOrchestrator resultado de la transcripción: {transcript}")
        
        print("▶ MainAssistantOrchestrator: Reproduciendo respuesta...")
        self.audioHandler.play(audio_bytes)
        
    def handle_text_interaction(self, text: str) -> None:
        pass