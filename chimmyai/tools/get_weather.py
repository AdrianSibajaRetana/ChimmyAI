"""Herramienta: consultar el clima actual usando Open-Meteo."""

import httpx

from chimmyai.config import Config
from chimmyai.tools.base import Tool
from chimmyai.tools.geocode_cache import GeocodeCache

_GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
_WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
_WEATHER_FIELDS = "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,apparent_temperature"

_WMO_CODES: dict[int, str] = {
    0: "cielo despejado",
    1: "mayormente despejado", 2: "parcialmente nublado", 3: "nublado",
    45: "niebla", 48: "niebla con escarcha",
    51: "llovizna ligera", 53: "llovizna moderada", 55: "llovizna intensa",
    56: "llovizna helada ligera", 57: "llovizna helada intensa",
    61: "lluvia ligera", 63: "lluvia moderada", 65: "lluvia fuerte",
    66: "lluvia helada ligera", 67: "lluvia helada fuerte",
    71: "nevada ligera", 73: "nevada moderada", 75: "nevada fuerte",
    77: "granizo fino",
    80: "chubascos ligeros", 81: "chubascos moderados", 82: "chubascos fuertes",
    85: "chubascos de nieve ligeros", 86: "chubascos de nieve fuertes",
    95: "tormenta eléctrica",
    96: "tormenta con granizo ligero", 99: "tormenta con granizo fuerte",
}

_cache = GeocodeCache()


async def _geocode(city: str, country: str) -> dict:
    """Traduce un nombre de ciudad a coordenadas. Usa caché local."""
    cache_key = f"{city}|{country}".lower()
    cached = _cache.get(cache_key)
    if cached:
        return cached

    async with httpx.AsyncClient() as client:
        response = await client.get(
            _GEOCODE_URL,
            params={"name": city, "count": 50, "language": "es"},
            timeout=8,
        )
        response.raise_for_status()

    results = response.json().get("results")
    if not results:
        raise ValueError(f"No se encontró ubicación para '{city}'.")

    hit = None
    country_lower = country.lower()
    for r in results:
        if country_lower in r.get("country", "").lower():
            hit = r
            break

    if hit is None:
        hit = results[0]

    data = {
        "lat": hit["latitude"],
        "lon": hit["longitude"],
        "name": hit.get("name", city),
        "country": hit.get("country", ""),
    }
    _cache.put(cache_key, **data)
    return data


async def _get_weather(city: str = "", country: str = "") -> str:
    city = city or Config.DEFAULT_LOCATION
    country = country or Config.DEFAULT_COUNTRY

    geo = await _geocode(city, country)

    async with httpx.AsyncClient() as client:
        response = await client.get(
            _WEATHER_URL,
            params={
                "latitude": geo["lat"],
                "longitude": geo["lon"],
                "current": _WEATHER_FIELDS,
                "timezone": "auto",
            },
            timeout=8,
        )
        response.raise_for_status()

    current = response.json().get("current", {})
    temp = current.get("temperature_2m", "N/A")
    feels = current.get("apparent_temperature", "N/A")
    humidity = current.get("relative_humidity_2m", "N/A")
    wind = current.get("wind_speed_10m", "N/A")
    code = current.get("weather_code", -1)
    condition = _WMO_CODES.get(code, "desconocido")

    return (
        f"{geo['name']}, {geo['country']}: {temp}°C (sensación {feels}°C), "
        f"{condition}, humedad {humidity}%, viento {wind} km/h."
    )


tool = Tool(
    name="get_weather",
    description="Returns the current weather for a given location. If no city is provided, defaults to the user's home location. Always call this tool when the user asks about weather, even without specifying a city.",
    parameters={
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "City name, e.g. 'Madrid', 'Buenos Aires', 'Santa Ana'. Optional — omit to use default location.",
            },
            "country": {
                "type": "string",
                "description": "Country name, e.g. 'España', 'Argentina', 'Costa Rica'. Optional — omit to use default country.",
            },
        },
        "required": [],
    },
    handler=_get_weather,
)
