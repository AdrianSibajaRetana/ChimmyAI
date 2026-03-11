"""Registro por defecto con las herramientas incluidas en ChimmyAI."""

from chimmyai.tools.base import ToolRegistry
from chimmyai.tools.get_current_time import tool as time_tool
from chimmyai.tools.get_weather import tool as weather_tool
from chimmyai.tools.web_search import tool as search_tool


def create_default_registry() -> ToolRegistry:
    """Crea un ToolRegistry precargado con las herramientas por defecto."""
    registry = ToolRegistry()
    registry.register(time_tool)
    registry.register(weather_tool)
    registry.register(search_tool)
    return registry
