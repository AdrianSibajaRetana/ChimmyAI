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


## Notas

### Phase 1 — Cloud API Backend

**Goal:** Turn your assistant into a service.

You build:

```
POST /ask
Audio → STT → LLM → TTS → return audio
```

You'll learn:

- FastAPI
- REST design
- Azure hosting
- Async handling
- Observability
- Authentication (very important)

Now you have a real backend.

### Phase 2 — Add Hardware (ESP32)

**Goal:** Constrained device → cloud.

You'll learn:

- HTTPS from microcontrollers
- Memory limits
- WiFi handling
- OTA updates
- Embedded debugging

This is where it gets fun.

### Phase 3 — Local Wake Word

**Goal:** Move one piece local.

Add wake word detection running on ESP32 or Raspberry Pi.

You'll learn:

- Real-time audio processing
- DSP basics
- Event loops

### Phase 4 — Move STT Local

**Goal:** Hybrid architecture.

Now:

- Local STT
- Cloud LLM
- Local TTS

You'll learn:

- Model deployment
- CPU/GPU tradeoffs
- Latency tuning

### Phase 5 — Fully Local Brain

**Goal:** Sovereign AI.

Now you're basically building your own Alexa competitor.
