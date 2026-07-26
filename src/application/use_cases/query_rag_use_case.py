from typing import Dict, Any, Optional
from src.domain.entities.document import QueryResult
from src.domain.interfaces.vector_store_interface import VectorStoreInterface
from src.domain.interfaces.llm_interface import LLMServiceInterface
from src.infrastructure.llm.oci_genai_service import OCIGenAIService


class QueryRAGUseCase:
    """Caso de uso principal para realizar consultas conversacionales al Agente RAG."""

    def __init__(
        self,
        vector_store: VectorStoreInterface,
        llm_service: Optional[LLMServiceInterface] = None
    ):
        self.vector_store = vector_store
        self.llm_service = llm_service or OCIGenAIService()

    def execute_query(
        self,
        query: str,
        top_k: int = 4,
        category_filter: Optional[str] = None
    ) -> QueryResult:
        if not query or not query.strip():
            raise ValueError("La consulta no puede estar vacía.")

        filter_meta = None
        if category_filter and category_filter != "Todas":
            filter_meta = {"category": category_filter}

        # 1. Recuperar contexto relevante
        context_chunks = self.vector_store.search_similar(
            query=query,
            top_k=top_k,
            filter_metadata=filter_meta
        )

        # 2. Generar respuesta sintetizada con citas de fuentes
        return self.llm_service.generate_answer(
            query=query,
            context_chunks=context_chunks
        )
