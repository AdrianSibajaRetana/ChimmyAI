from chimmyai.audio.base import AudioHandler

from .base import AssistantOrchestrator

class MainAssistantOrchestrator(AssistantOrchestrator):
    
    def __init__(self, audio: AudioHandler):
        self.audioHandler = audio

    def handle_voice_interaction(self) -> None:
        print("MainAssistantOrchestrator: Grabando entrada de usuario")
        audio_bytes = self.audioHandler.record()
        
        print("▶ MainAssistantOrchestrator: Reproduciento respuesta...")
        self.audioHandler.play(audio_bytes)
        
    def handle_text_interaction(self, text: str) -> None:
        pass