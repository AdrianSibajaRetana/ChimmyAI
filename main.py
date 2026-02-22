"""
ChimmyAI - Asistente personal por voz.
Ejecutar con: python main.py
"""
from chimmyai.config import Config

def main():
    print(f"{Config.APP_NAME} v{Config.VERSION}")
    print("Pipeline: Audio → STT → LLM → TTS → Audio")
    print()

    # TODO: Implementar pipeline completo
    # 1. audio_handler.record()    → capturar audio
    # 2. stt.transcribe(audio)     → convertir a texto
    # 3. llm.generate(text)        → obtener respuesta
    # 4. tts.synthesize(response)  → convertir a audio
    # 5. audio_handler.play(audio) → reproducir respuesta

    print("¡Hola! Soy Chimmy. (Pipeline pendiente de implementación)")


if __name__ == "__main__":
    main()
