"""Herramienta: búsqueda web usando Tavily Search API."""

import os

import httpx

from chimmyai.config import Config
from chimmyai.tools.base import Tool

_TAVILY_URL = "https://api.tavily.com/search"


async def _web_search(
    query: str,
    time_range: str = "",
    topic: str = "",
    country: str = "",
) -> str:
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "Error: TAVILY_API_KEY no está configurada."

    body: dict = {
        "query": query,
        "max_results": Config.SEARCH_MAX_RESULTS,
        "search_depth": Config.SEARCH_DEPTH,
        "include_answer": Config.SEARCH_INCLUDE_ANSWER,
    }
    if topic:
        body["topic"] = topic
    if time_range:
        body["time_range"] = time_range
    if country and (not topic or topic == "general"):
        body["country"] = country

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                _TAVILY_URL,
                headers={"Authorization": f"Bearer {api_key}"},
                json=body,
                timeout=15,
            )
            response.raise_for_status()
    except httpx.HTTPStatusError as e:
        status = e.response.status_code
        messages = {
            400: "Parámetros de búsqueda inválidos.",
            401: "API key de Tavily inválida o no configurada.",
            429: "Límite de uso de Tavily alcanzado. Intenta más tarde.",
        }
        detail = messages.get(status, f"Error HTTP {status}.")
        if status >= 500:
            detail = "El servicio de Tavily no está disponible temporalmente."
        return f"Error en búsqueda web: {detail}"
    except httpx.RequestError as e:
        return f"Error de conexión en búsqueda web: {e}"

    data = response.json()
    answer = data.get("answer", "")
    results = data.get("results", [])

    parts: list[str] = []
    if answer:
        parts.append(f"Resumen: {answer}")
    for r in results:
        title = r.get("title", "")
        content = r.get("content", "")
        url = r.get("url", "")
        parts.append(f"- {title}: {content[:500]} ({url})")

    if not parts:
        return f"No se encontraron resultados para '{query}'."

    return "\n\n".join(parts)


def _build_parameters() -> dict:
    """Construye el JSON Schema de parámetros según las flags de Config."""
    properties: dict = {
        "query": {
            "type": "string",
            "description": "A search-engine-optimized query with specific keywords. Write it as you would type into Google, not as a natural language question. Use Spanish when the user speaks Spanish. Example: instead of 'how much is the dollar today' use 'tipo de cambio dólar colón costa rica hoy'.",
        },
        "time_range": {
            "type": "string",
            "enum": ["day", "week", "month", "year"],
            "description": "How recent the results should be. Use 'day' for today's news, 'week' for this week, etc. Omit for no time restriction.",
        },
    }
    if Config.SEARCH_LLM_CONTROLS_TOPIC:
        properties["topic"] = {
            "type": "string",
            "enum": ["general", "news", "finance"],
            "description": "Category of the search. Use 'news' for current events, 'finance' for financial data. Default is 'general'.",
        }
    if Config.SEARCH_LLM_CONTROLS_COUNTRY:
        properties["country"] = {
            "type": "string",
            "description": "Full country name in lowercase to boost results from that country, e.g. 'costa rica', 'spain', 'united states'. Only use when the user explicitly mentions a country. Only works with the default 'general' topic.",
        }
    return {"type": "object", "properties": properties, "required": ["query"]}


tool = Tool(
    name="web_search",
    description="Searches the web for a given query and returns relevant results with summaries. Use this tool when the user asks about current events, facts, or anything that requires up-to-date information. Do NOT use this tool for weather queries (use get_weather instead) or date/time queries (use get_current_time instead).",
    parameters=_build_parameters(),
    handler=_web_search,
)
