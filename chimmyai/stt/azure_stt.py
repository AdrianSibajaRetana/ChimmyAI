import os
import asyncio
import azure.cognitiveservices.speech as speechsdk
from .base import SpeechToText

class AzureSpeechToText(SpeechToText):

    def __init__(self):
        key = os.getenv("SPEECH_KEY")
        endpoint = os.getenv("ENDPOINT")

        if not key:
            raise RuntimeError("SPEECH_KEY is not set in environment")
        if not endpoint:
            raise RuntimeError("ENDPOINT is not set in environment")

        self.speech_config = speechsdk.SpeechConfig(
            subscription=key,
            endpoint=endpoint,
        )
        self.speech_config.speech_recognition_language = "es-ES"

    async def transcribe(self, audio_data: bytes) -> str:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None,
            self._transcribe_sync,
            audio_data,
        )

    def _transcribe_sync(self, audio: bytes) -> str:
        # Create fresh stream per request
        audio_stream = speechsdk.audio.PushAudioInputStream()
        audio_config = speechsdk.audio.AudioConfig(stream=audio_stream)

        recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config,
            audio_config=audio_config,
        )

        audio_stream.write(audio)
        audio_stream.close()

        result = recognizer.recognize_once()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            return ""
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation = result.cancellation_details
            raise RuntimeError(
                f"Speech Recognition canceled: "
                f"{cancellation.reason} - {cancellation.error_details}"
            )

        return ""