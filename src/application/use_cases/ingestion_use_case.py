from pathlib import Path
from typing import Union, BinaryIO, List, Dict, Any

from src.domain.entities.document import Document, TextChunk
from src.domain.interfaces.vector_store_interface import VectorStoreInterface
from src.infrastructure.parsers.parser_factory import IngestionParserFactory
from src.application.use_cases.chunking_service import ChunkingService


class IngestionUseCase:
    """Caso de uso principal para orquestar la ingesta, chunking e indexación de documentos."""

    def __init__(self, vector_store: VectorStoreInterface, parser_factory: IngestionParserFactory = None, chunking_service: ChunkingService = None):
        self.vector_store = vector_store
        self.parser_factory = parser_factory or IngestionParserFactory()
        self.chunking_service = chunking_service or ChunkingService()

    def process_and_index_file(self, file_source: Union[str, Path, BinaryIO], file_name: str, category: str = "General") -> Dict[str, Any]:
        """Procesa un archivo completo (Parsing -> Chunking -> Vector Store)."""
        # 1. Parsing
        document: Document = self.parser_factory.parse_document(
            file_source=file_source,
            file_name=file_name,
            category=category
        )

        # 2. Chunking
        chunks: List[TextChunk] = self.chunking_service.split_document(document)

        # 3. Indexación en Vector Store
        success = self.vector_store.add_chunks(chunks)

        return {
            "status": "success" if success else "error",
            "document_id": document.id,
            "file_name": file_name,
            "category": category,
            "num_chunks_created": len(chunks),
            "content_length": len(document.content)
        }
