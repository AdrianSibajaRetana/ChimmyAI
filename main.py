from chimmyai.assistant.AssistantOrchestrator import MainAssistantOrchestrator
from chimmyai.audio.sounddevice_audio import SoundDeviceAudioHandler

def main():
    ## Paso 1: Crear servicios    
    AudioHandler = SoundDeviceAudioHandler()
    
    ## Paso 2: Subscribir servicios al main orchestrator 
    Orchestrator = MainAssistantOrchestrator(AudioHandler)
    
    ## Paso 3: Utilizar el orquestador
    Orchestrator.handle_voice_interaction()
    
if __name__ == "__main__":
    main()