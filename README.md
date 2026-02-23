# Chimmy AI

Asistente personal por voz similar a Alexa, diseñado como proyecto educativo para aprender sobre arquitectura de sistemas distribuidos, integración con LLMs y computación edge.

## Estructura del proyecto

```
ChimmyAI/
├── main.py                          # Punto de entrada (CLI)
├── requirements.txt                 # Dependencias
├── chimmyai/
│   ├── __init__.py
│   ├── config.py                    # Configuración centralizada
│
│   ├── audio/                       # Infraestructura de audio
│   │   ├── __init__.py
│   │   ├── base.py                  # Interfaz abstracta
│   │   └── sounddevice_audio.py     # Implementación con sounddevice
│
│   ├── stt/                         # Speech-to-Text
│   │   ├── __init__.py
│   │   ├── base.py                  # Interfaz abstracta
│   │   └── faster_whisper_stt.py    # Implementación con faster-whisper
│
│   ├── llm/                         # Modelo de lenguaje
│   │   ├── __init__.py
│   │   └── base.py                  # Interfaz abstracta
│
│   ├── tts/                         # Text-to-Speech
│   │   ├── __init__.py
│   │   ├── base.py                  # Interfaz abstracta
│   │   └── coqui_tts.py            # Implementación con Coqui TTS
│
│   └── assistant/                   # Caso de uso principal
│       ├── __init__.py
│       ├── base.py                  # Interfaz abstracta
│       └── assistant_orchestrator.py # Orquestador del flujo completo
```

## Pipeline

```
Micrófono → STT → LLM → TTS → Altavoz
```

## Instalación

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecutar

```bash
.\venv\Scripts\activate
python main.py
```