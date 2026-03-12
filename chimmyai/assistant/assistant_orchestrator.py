from chimmyai.audio.base import AudioHandler
from chimmyai.stt.base import SpeechToText
from chimmyai.tts.base import TextToSpeech
from chimmyai.llm.base import BaseLLM

from .base import AssistantOrchestrator

class MainAssistantOrchestrator(AssistantOrchestrator):
    
    # ANSI color codes
    _CYAN = "\033[96m"
    _GREEN = "\033[92m"
    _RESET = "\033[0m"

    def __init__(self, audio: AudioHandler, stt: SpeechToText, tts: TextToSpeech, llm: BaseLLM):
        self.audioHandler = audio
        self.speechToText = stt
        self.textToSpeech = tts
        self.llmEngine = llm

    async def handle_voice_interaction(self) -> None:
        print("MainAssistantOrchestrator: Grabando entrada de usuario")
        audio_bytes = await self.audioHandler.record()
        
        print("MainAssistantOrchestrator: Transcribiendo...")
        transcript = await self.speechToText.transcribe(audio_bytes)    
        print(f"{self._CYAN}MainAssistantOrchestrator resultado de la transcripción: {transcript}{self._RESET}")

        if not transcript or not transcript.strip():
            print("MainAssistantOrchestrator: Transcripción vacía, omitiendo respuesta.")
            return
        
        print("MainAssistantOrchestrator enviando mensaje a LLM...")
        response = await self.llmEngine.chat(transcript)
        print(f"{self._GREEN}MainAssistantOrchestrator LLM ha respondido: {response}{self._RESET}")
        
        print("▶ MainAssistantOrchestrator: Generando TTS Bytes")
        tts_bytes = await self.textToSpeech.synthesize(response)
        
        print("▶ MainAssistantOrchestrator: Reproduciendo respuesta...")
        await self.audioHandler.play(tts_bytes)