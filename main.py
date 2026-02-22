import asyncio

from chimmyai.assistant.assistant_orchestrator import MainAssistantOrchestrator
from chimmyai.audio.sounddevice_audio import SoundDeviceAudioHandler
from chimmyai.stt.faster_whisper_stt import FasterWhisperSpeechToText

async def main():
    ## Paso 1: Crear servicios    
    audio_handler = SoundDeviceAudioHandler()
    
    stt_handler = FasterWhisperSpeechToText(
        model_size="base",
        device="cpu",
        compute_type="int8",
    )
    
    ## Paso 2: Subscribir servicios al main orchestrator 
    orchestrator = MainAssistantOrchestrator(audio_handler, stt_handler)
    
    ## Paso 3: Utilizar el orquestador
    await orchestrator.handle_voice_interaction()
    
if __name__ == "__main__":
    asyncio.run(main())