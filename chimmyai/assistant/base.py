"""
Interfaz abstracta para el orquestador del asistente.

Define el caso de uso principal: manejar una interacción de voz
de extremo a extremo (audio → texto → LLM → audio).
"""
from abc import ABC, abstractmethod


class AssistantOrchestrator(ABC):
    """
    Contrato para implementaciones del flujo completo del asistente.

    Equivalente conceptual en C#: IAssistantOrchestrator
    """

    @abstractmethod
    async def handle_voice_interaction(self) -> None:
        """
        Ejecuta el flujo completo:

        1. Captura audio
        2. Transcribe audio a texto
        3. Genera respuesta usando el LLM
        4. Convierte respuesta a audio
        5. Reproduce el audio generado

        No debe exponer detalles internos de cada etapa.
        """
        ...

    @abstractmethod
    async def handle_text_interaction(self, text: str) -> str:
        """
        Maneja una interacción basada en texto (útil para CLI,
        testing o futuras APIs HTTP).

        Recibe texto y devuelve texto generado por el modelo.
        """
        ...