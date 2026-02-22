# Chimmy AI

Asistente personal por voz similar a Alexa, diseñado como proyecto educativo para aprender sobre arquitectura de sistemas distribuidos, integración con LLMs y computación edge.

## Estructura del proyecto

```
ChimmyAI/
├── main.py                   # Punto de entrada (CLI)
├── requirements.txt          # Dependencias
├── chimmyai/
│   ├── __init__.py
│   ├── config.py             # Configuración centralizada
│
│   ├── audio/                # Infraestructura de audio
│   │   ├── __init__.py
│   │   └── base.py           # Interfaz abstracta
│
│   ├── stt/                  # Speech-to-Text
│   │   ├── __init__.py
│   │   └── base.py           # Interfaz abstracta
│
│   ├── llm/                  # Modelo de lenguaje
│   │   ├── __init__.py
│   │   └── base.py           # Interfaz abstracta
│
│   ├── tts/                  # Text-to-Speech
│   │   ├── __init__.py
│   │   └── base.py           # Interfaz abstracta
│
│   └── assistant/            # Caso de uso principal
│       ├── __init__.py
│       └── orchestrator.py   # Orquestador del flujo completo
```

## Pipeline

```
Micrófono → STT → LLM → TTS → Altavoz
```

## Ejecutar

```bash
python main.py
```
  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"