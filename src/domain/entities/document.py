from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime


@dataclass
class DocumentMetadata:
    """Metadatos asociados a un documento ingerido."""
    file_name: str
    file_type: str
    file_size_bytes: int
    category: str = "General"  # RH, Finanzas, Operaciones, Legal, etc.
    upload_timestamp: datetime = field(default_factory=datetime.utcnow)
    additional_info: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Document:
    """Entidad principal de Documento en el dominio."""
    id: str
    content: str
    metadata: DocumentMetadata


@dataclass
class TextChunk:
    """Entidad de fragmento semántico extraído de un documento."""
    chunk_id: str
    document_id: str
    content: str
    chunk_index: int
    metadata: Dict[str, Any]


@dataclass
class QueryResult:
    """Resultado devuelto por el motor conversacional RAG."""
    query: str
    answer: str
    source_chunks: List[TextChunk]
    execution_time_seconds: float
