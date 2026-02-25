import asyncio
import warnings

warnings.filterwarnings("ignore", message="dtype.*align", category=DeprecationWarning)
warnings.filterwarnings("ignore", message="dtype.*align")

from chimmyai.assistant.assistant_orchestrator import MainAssistantOrchestrator
from chimmyai.audio.sounddevice_audio import SoundDeviceAudioHandler
from chimmyai.stt.faster_whisper_stt import FasterWhisperSpeechToText
from chimmyai.tts.coqui_tts import CoquiTTS

async def main():
    ## Paso 1: Crear servicios
    print("Main: Inicializando Servicios")
    audio_handler = SoundDeviceAudioHandler()
    
    stt_handler = FasterWhisperSpeechToText()
    
    tts_handler = CoquiTTS()
    
    ## Paso 2: Subscribir servicios al main orchestrator 
    orchestrator = MainAssistantOrchestrator(audio_handler, stt_handler, tts_handler)
    
    ## Paso 3: Utilizar el orquestador
    await orchestrator.handle_voice_interaction()
    
if __name__ == "__main__":
    asyncio.run(main())