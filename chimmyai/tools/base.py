"""Definiciones base para el sistema de herramientas."""

from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class Tool:
    """Definición genérica de una herramienta, independiente del proveedor LLM.

    Parameters
    ----------
    name : str
        Identificador único de la herramienta (snake_case).
    description : str
        Descripción breve que el LLM usará para decidir cuándo invocarla.
    parameters : dict
        JSON Schema que describe los argumentos de la herramienta.
    handler : Callable[..., str]
        Función que ejecuta la herramienta y devuelve un string con el resultado.
    """
    name: str
    description: str
    parameters: dict
    handler: Callable[..., str]


class ToolRegistry:
    """Registro central de herramientas disponibles para el LLM."""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def all_tools(self) -> list[Tool]:
        return list(self._tools.values())

    def execute(self, name: str, **kwargs: Any) -> str:
        """Ejecuta una herramienta por nombre. Devuelve error como string si falla."""
        tool = self._tools.get(name)
        if tool is None:
            return f"Error: herramienta '{name}' no encontrada."
        try:
            return tool.handler(**kwargs)
        except Exception as e:
            return f"Error ejecutando '{name}': {e}"
