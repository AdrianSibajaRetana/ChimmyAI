import asyncio
import warnings
from dotenv import load_dotenv

load_dotenv()

warnings.filterwarnings("ignore", message="dtype.*align", category=DeprecationWarning)
warnings.filterwarnings("ignore", message="dtype.*align")

from chimmyai.config import Config
from chimmyai.assistant.assistant_orchestrator import MainAssistantOrchestrator
from chimmyai.audio.sounddevice_audio import SoundDeviceAudioHandler
from chimmyai.llm.azure_openai import AzureOpenAI

async def main():
    ## Paso 1: Crear servicios
    print("Main: Inicializando Servicios")
    audio_handler = SoundDeviceAudioHandler()
    
    ## Revisar si estoy usando los servicios cloud vs locales
    if Config.USE_CLOUD:
        from chimmyai.stt.azure_stt import AzureSpeechToText
        from chimmyai.tts.azure_tts import AzureTextToSpeech
        stt_handler = AzureSpeechToText()
        tts_handler = AzureTextToSpeech()
    else:
        from chimmyai.stt.faster_whisper_stt import FasterWhisperSpeechToText
        from chimmyai.tts.coqui_tts import CoquiTTS
        stt_handler = FasterWhisperSpeechToText()
        tts_handler = CoquiTTS()
    
    llm_engine = AzureOpenAI()
    
    ## Paso 2: Subscribir servicios al main orchestrator 
    orchestrator = MainAssistantOrchestrator(audio_handler, stt_handler, tts_handler, llm_engine)
    
    
    ## Paso 3: Utilizar el orquestador
    await orchestrator.handle_voice_interaction()
    
if __name__ == "__main__":
    asyncio.run(main())