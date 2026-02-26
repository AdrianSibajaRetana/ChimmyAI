"""Configuración centralizada de ChimmyAI."""

class Config:
    """Configuración global del asistente."""
    # Audio (sounddevice_audio.py)
    AUDIO_SAMPLE_RATE = 16000
    AUDIO_CHANNELS = 1
    AUDIO_RECORD_DURATION = 5

    # STT (faster_whisper_stt.py)
    STT_MODEL_SIZE = "small"
    STT_DEVICE = "cpu"
    STT_COMPUTE_TYPE = "float32"
    STT_LANGUAGE = "es"

    # TTS (coqui_tts.py)
    TTS_COQUI_MODEL = "tts_models/es/mai/tacotron2-DDC"
    TTS_DEVICE = "cpu"
    
    #-----Cloud variables---------#
    USE_CLOUD = True
    
