import unittest
from pathlib import Path
from src.infrastructure.vector_store.chroma_vector_store import InMemoryOrChromaVectorStore
from src.application.use_cases.ingestion_use_case import IngestionUseCase
from src.application.use_cases.chunking_service import ChunkingService
from src.domain.entities.document import Document, DocumentMetadata


class TestRAGPipeline(unittest.TestCase):
    def setUp(self):
        self.vector_store = InMemoryOrChromaVectorStore(collection_name="test_collection")
        self.ingestion_use_case = IngestionUseCase(vector_store=self.vector_store)
        self.chunking_service = ChunkingService(chunk_size=100, chunk_overlap=20)

    def test_chunking_service_splits_correctly(self):
        long_text = "La política de vacaciones de Recursos Humanos establece 15 días hábiles al año. " * 5
        doc = Document(
            id="doc_test_1",
            content=long_text,
            metadata=DocumentMetadata(
                file_name="vacaciones.txt",
                file_type="TXT",
                file_size_bytes=len(long_text),
                category="RH"
            )
        )

        chunks = self.chunking_service.split_document(doc)
        self.assertGreater(len(chunks), 1)
        self.assertEqual(chunks[0].metadata["category"], "RH")
        self.assertEqual(chunks[0].metadata["file_name"], "vacaciones.txt")

    def test_ingestion_and_search_use_case(self):
        # Crear archivo Markdown de prueba
        test_file = Path("test_politica.md")
        content = "# Política de Reembolso de Gastos\n\nLos viáticos de viajes corporativos deben enviarse antes de 5 días hábiles."
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(content)

        try:
            # Procesar e indexar
            result = self.ingestion_use_case.process_and_index_file(test_file, "test_politica.md", category="Finanzas")
            self.assertEqual(result["status"], "success")
            self.assertGreater(result["num_chunks_created"], 0)

            # Buscar por similitud
            search_results = self.vector_store.search_similar("¿Cuál es el plazo para viáticos?", top_k=2)
            self.assertGreater(len(search_results), 0)
            self.assertIn("viáticos", search_results[0].content.lower())
            self.assertEqual(search_results[0].metadata["category"], "Finanzas")
        finally:
            if test_file.exists():
                test_file.unlink()


if __name__ == "__main__":
    unittest.main()
