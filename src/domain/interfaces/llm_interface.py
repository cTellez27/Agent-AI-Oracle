from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.document import TextChunk, QueryResult


class LLMServiceInterface(ABC):
    """Contrato base para interactuar con servicios de LLM (OCI GenAI / API externa)."""

    @abstractmethod
    def generate_answer(self, query: str, context_chunks: List[TextChunk]) -> QueryResult:
        """Genera una respuesta sintetizada utilizando los fragmentos contextuales recuperados."""
        pass
