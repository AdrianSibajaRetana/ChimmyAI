import os
import asyncio
import azure.cognitiveservices.speech as speechsdk
from .base import TextToSpeech


class AzureTextToSpeech(TextToSpeech):

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

        self.speech_config.speech_synthesis_language =  "es-ES"
        self.speech_config.speech_synthesis_voice_name = "es-ES-ElviraNeural"

        # Ensure WAV format (16kHz PCM)
        self.speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm
        )

    async def synthesize(self, text: str) -> bytes:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None,
            self._synthesize_sync,
            text,
        )

    def _synthesize_sync(self, text: str) -> bytes:
        # Create fresh stream per request
        pull_stream = speechsdk.audio.PullAudioOutputStream()
        audio_config = speechsdk.audio.AudioOutputConfig(stream=pull_stream)

        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config,
            audio_config=audio_config,
        )

        result = synthesizer.speak_text(text)

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            audio_buffer = bytes(result.audio_data)
            return audio_buffer

        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation = result.cancellation_details
            raise RuntimeError(
                f"TTS canceled: {cancellation.reason} - {cancellation.error_details}"
            )

        return b""