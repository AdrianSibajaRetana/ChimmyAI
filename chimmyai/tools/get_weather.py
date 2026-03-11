"""Herramienta placeholder: consultar el clima."""

from chimmyai.tools.base import Tool


def _get_weather(location: str) -> str:
    # TODO: integrar con una API real de clima.
    return f"22 °C, soleado en {location}. (datos de ejemplo)"


tool = Tool(
    name="get_weather",
    description="Returns the current weather for a given location. Currently returns placeholder data.",
    parameters={
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "City or location name, e.g. 'Madrid' or 'Buenos Aires'.",
            },
        },
        "required": ["location"],
    },
    handler=_get_weather,
)
