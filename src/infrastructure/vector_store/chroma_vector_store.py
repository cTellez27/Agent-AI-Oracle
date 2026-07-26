import os
from typing import List, Dict, Any
from pathlib import Path

from src.domain.entities.document import TextChunk
from src.domain.interfaces.vector_store_interface import VectorStoreInterface


class InMemoryOrChromaVectorStore(VectorStoreInterface):
    """Implementación de Vector Store con ChromaDB y Fallback Vectorial en memoria."""

    def __init__(self, collection_name: str = "corporate_knowledge_base", persist_directory: str = "./data/chroma_db"):
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self._chunks_db: List[TextChunk] = []
        self._chroma_client = None
        self._collection = None

        # Intentar inicializar ChromaDB si está disponible
        try:
            import chromadb
            Path(persist_directory).mkdir(parents=True, exist_ok=True)
            self._chroma_client = chromadb.PersistentClient(path=persist_directory)
            self._collection = self._chroma_client.get_or_create_collection(name=collection_name)
        except Exception:
            # Fallback en memoria si ChromaDB no está instalado aún en el entorno liviano
            self._chroma_client = None
            self._collection = None

    def add_chunks(self, chunks: List[TextChunk]) -> bool:
        if not chunks:
            return True

        if self._collection is not None:
            ids = [chunk.chunk_id for chunk in chunks]
            documents = [chunk.content for chunk in chunks]
            metadatas = [chunk.metadata for chunk in chunks]
            
            # Limpiar metadatos incompatibles si los hay
            cleaned_metadatas = []
            for meta in metadatas:
                cleaned_meta = {k: str(v) if not isinstance(v, (str, int, float, bool)) else v for k, v in meta.items()}
                cleaned_metadatas.append(cleaned_meta)

            self._collection.add(
                ids=ids,
                documents=documents,
                metadatas=cleaned_metadatas
            )
        
        # Guardar en memoria siempre para respuesta ultrarrápida
        self._chunks_db.extend(chunks)
        return True

    def search_similar(self, query: str, top_k: int = 4, filter_metadata: Dict[str, Any] = None) -> List[TextChunk]:
        if not self._chunks_db:
            return []

        if self._collection is not None:
            try:
                where_filter = None
                if filter_metadata:
                    where_filter = {k: str(v) for k, v in filter_metadata.items()}

                results = self._collection.query(
                    query_texts=[query],
                    n_results=min(top_k, len(self._chunks_db)),
                    where=where_filter
                )

                matched_chunks: List[TextChunk] = []
                if results and "ids" in results and results["ids"]:
                    matched_ids = results["ids"][0]
                    id_to_chunk = {c.chunk_id: c for c in self._chunks_db}
                    for cid in matched_ids:
                        if cid in id_to_chunk:
                            matched_chunks.append(id_to_chunk[cid])
                    if matched_chunks:
                        return matched_chunks
            except Exception:
                pass  # Si falla la consulta a Chroma, usa el fallback en memoria

        # Búsqueda léxica/semántica de fallback en memoria
        import re
        stop_words = {"de", "del", "la", "el", "los", "las", "en", "es", "por", "para", "un", "una", "unos", "unas", "con", "sin", "al", "o", "y", "a", "que", "cual", "cuál"}
        query_terms = set(w for w in re.findall(r"\w+", query.lower()) if len(w) >= 2 and w not in stop_words)
        scored_chunks = []

        for chunk in self._chunks_db:
            # Filtrado por metadatos si aplica
            if filter_metadata:
                match = all(chunk.metadata.get(k) == str(v) or chunk.metadata.get(k) == v for k, v in filter_metadata.items())
                if not match:
                    continue

            content_lower = chunk.content.lower()
            score = sum(1 for term in query_terms if term in content_lower)
            if score > 0:
                scored_chunks.append((score, chunk))

        # Ordenar por score descendente
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        return [chunk for score, chunk in scored_chunks[:top_k]]
