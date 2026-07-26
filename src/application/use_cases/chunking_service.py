import uuid
from typing import List
from src.domain.entities.document import Document, TextChunk


class ChunkingService:
    """Servicio de segmentación semántica de documentos en fragmentos (chunks)."""

    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 120):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_document(self, document: Document) -> List[TextChunk]:
        content = document.content
        if not content or not content.strip():
            return []

        chunks: List[TextChunk] = []
        start = 0
        text_length = len(content)
        chunk_index = 0

        while start < text_length:
            end = min(start + self.chunk_size, text_length)
            
            # Ajustar para no cortar palabras a la mitad si es posible
            if end < text_length and content[end] not in [" ", "\n", "\t", ".", ","]:
                last_space = content.rfind(" ", start, end)
                if last_space > start:
                    end = last_space

            chunk_text = content[start:end].strip()
            
            if chunk_text:
                metadata = {
                    "document_id": document.id,
                    "file_name": document.metadata.file_name,
                    "file_type": document.metadata.file_type,
                    "category": document.metadata.category,
                    "chunk_index": chunk_index
                }

                chunks.append(
                    TextChunk(
                        chunk_id=f"{document.id}_chunk_{chunk_index}",
                        document_id=document.id,
                        content=chunk_text,
                        chunk_index=chunk_index,
                        metadata=metadata
                    )
                )
                chunk_index += 1

            start += self.chunk_size - self.chunk_overlap
            if start >= text_length:
                break

        return chunks
