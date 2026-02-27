"""Fábrica centralizada de servicios de ChimmyAI."""

from chimmyai.config import Config
from chimmyai.stt.base import SpeechToText
from chimmyai.tts.base import TextToSpeech
from chimmyai.llm.base import BaseLLM
from chimmyai.audio.base import AudioHandler


class ServiceFactory:
    """Crea las implementaciones correctas según Config.USE_CLOUD."""

    @staticmethod
    def create_audio() -> AudioHandler:
        from chimmyai.audio.sounddevice_audio import SoundDeviceAudioHandler
        return SoundDeviceAudioHandler()

    @staticmethod
    def create_stt() -> SpeechToText:
        if Config.USE_CLOUD:
            from chimmyai.stt.azure_stt import AzureSpeechToText
            return AzureSpeechToText()
        from chimmyai.stt.faster_whisper_stt import FasterWhisperSpeechToText
        return FasterWhisperSpeechToText()

    @staticmethod
    def create_tts() -> TextToSpeech:
        if Config.USE_CLOUD:
            from chimmyai.tts.azure_tts import AzureTextToSpeech
            return AzureTextToSpeech()
        from chimmyai.tts.coqui_tts import CoquiTTS
        return CoquiTTS()

    @staticmethod
    def create_llm() -> BaseLLM:
        if Config.USE_CLOUD:
            from chimmyai.llm.azure_openai import AzureOpenAI
            return AzureOpenAI()
        from chimmyai.llm.local_llm import LocalLLM
        return LocalLLM()
