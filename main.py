import asyncio
import warnings
from dotenv import load_dotenv

load_dotenv()

warnings.filterwarnings("ignore", message="dtype.*align", category=DeprecationWarning)
warnings.filterwarnings("ignore", message="dtype.*align")

from chimmyai.factory import ServiceFactory
from chimmyai.assistant.assistant_orchestrator import MainAssistantOrchestrator

async def main():
    print("Main: Inicializando Servicios")
    audio_handler = ServiceFactory.create_audio()
    stt_handler = ServiceFactory.create_stt()
    tts_handler = ServiceFactory.create_tts()
    llm_engine = ServiceFactory.create_llm()

    orchestrator = MainAssistantOrchestrator(audio_handler, stt_handler, tts_handler, llm_engine)

    try:
        await orchestrator.handle_voice_interaction()
    finally:
        await llm_engine.close()
    
if __name__ == "__main__":
    asyncio.run(main())