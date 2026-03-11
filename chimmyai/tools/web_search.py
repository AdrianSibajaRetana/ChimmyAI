"""Herramienta placeholder: búsqueda web."""

from chimmyai.tools.base import Tool


def _web_search(query: str) -> str:
    # TODO: integrar con una API real de búsqueda.
    return f"Resultados para '{query}': No hay resultados reales disponibles (placeholder)."


tool = Tool(
    name="web_search",
    description="Searches the web for a given query. Currently returns placeholder data.",
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query.",
            },
        },
        "required": ["query"],
    },
    handler=_web_search,
)
