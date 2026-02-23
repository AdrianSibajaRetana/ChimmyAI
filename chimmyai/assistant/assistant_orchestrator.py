from chimmyai.audio.base import AudioHandler
from chimmyai.stt.base import SpeechToText
from chimmyai.tts.base import TextToSpeech

from .base import AssistantOrchestrator

class MainAssistantOrchestrator(AssistantOrchestrator):
    
    def __init__(self, audio: AudioHandler, stt: SpeechToText, tts: TextToSpeech):
        self.audioHandler = audio
        self.speechToText = stt
        self.textToSpeech = tts

    async def handle_voice_interaction(self) -> None:
        print("MainAssistantOrchestrator: Grabando entrada de usuario")
        audio_bytes = await self.audioHandler.record()
        
        print("MainAssistantOrchestrator: Transcribiendo...")
        transcript = await self.speechToText.transcribe(audio_bytes)
        
        print(f"MainAssistantOrchestrator resultado de la transcripción: {transcript}")
        
        print("▶ MainAssistantOrchestrator: Reproduciendo respuesta...")
        await self.audioHandler.play(audio_bytes)
        
        print("▶ MainAssistantOrchestrator: Reproduciendo respuesta TTS...")
        await self.textToSpeech.synthesize(transcript)
        
