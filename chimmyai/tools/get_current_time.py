"""Herramienta: obtener fecha y hora actual."""

from datetime import datetime

from chimmyai.tools.base import Tool


def _get_current_time() -> str:
    now = datetime.now()
    return now.strftime("%A %d de %B de %Y, %H:%M:%S")


tool = Tool(
    name="get_current_time",
    description="Returns the current local date and time.",
    parameters={
        "type": "object",
        "properties": {},
        "required": [],
    },
    handler=_get_current_time,
)
