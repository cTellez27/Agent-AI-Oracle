import unittest
from pathlib import Path
from src.infrastructure.vector_store.chroma_vector_store import InMemoryOrChromaVectorStore
from src.application.use_cases.ingestion_use_case import IngestionUseCase
from src.application.use_cases.query_rag_use_case import QueryRAGUseCase
from src.infrastructure.llm.prompt_templates import build_rag_prompt
from src.domain.entities.document import TextChunk


class TestConversationalAgent(unittest.TestCase):
    def setUp(self):
        self.vector_store = InMemoryOrChromaVectorStore(collection_name="test_agent_collection")
        self.ingestion_use_case = IngestionUseCase(vector_store=self.vector_store)
        self.query_use_case = QueryRAGUseCase(vector_store=self.vector_store)

    def test_prompt_template_formatting(self):
        chunks = [
            TextChunk(
                chunk_id="c1",
                document_id="d1",
                content="Los empleados tienen 15 días de vacaciones anuales.",
                chunk_index=0,
                metadata={"file_name": "politica_vacaciones.pdf", "category": "RH"}
            )
        ]
        prompt = build_rag_prompt("¿Cuántos días de vacaciones tengo?", chunks)
        self.assertIn("politica_vacaciones.pdf", prompt)
        self.assertIn("15 días de vacaciones", prompt)

    def test_full_rag_conversational_flow(self):
        # 1. Ingerir documento de prueba
        test_file = Path("politica_gastos_test.md")
        content = "# Política de Gastos\n\nEl límite máximo para cenas de negocios es de 50 USD por persona."
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(content)

        try:
            self.ingestion_use_case.process_and_index_file(test_file, "politica_gastos_test.md", category="Finanzas")

            # 2. Consultar al agente RAG
            result = self.query_use_case.execute_query("¿Cuál es el límite para cenas de negocios?")
            self.assertIsNotNone(result.answer)
            self.assertGreater(len(result.source_chunks), 0)
            self.assertIn("politica_gastos_test.md", result.answer)
            self.assertIn("Finanzas", result.answer)

            # 3. Consulta sin resultados
            empty_result = self.query_use_case.execute_query("¿Cuál es la receta de la pizza hawayana?")
            self.assertIn("No dispongo de información", empty_result.answer)
        finally:
            if test_file.exists():
                test_file.unlink()


if __name__ == "__main__":
    unittest.main()
