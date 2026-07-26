from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.domain.entities.document import TextChunk


class VectorStoreInterface(ABC):
    """Contrato base para almacén de vectores y búsqueda por similitud."""

    @abstractmethod
    def add_chunks(self, chunks: List[TextChunk]) -> bool:
        """Indexa una lista de fragmentos en la base de datos vectorial."""
        pass

    @abstractmethod
    def search_similar(self, query: str, top_k: int = 4, filter_metadata: Dict[str, Any] = None) -> List[TextChunk]:
        """Realiza una búsqueda semántica de los k fragmentos más similares a la consulta."""
        pass
