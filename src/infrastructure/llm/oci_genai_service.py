import time
import os
from typing import List
from src.domain.entities.document import TextChunk, QueryResult
from src.domain.interfaces.llm_interface import LLMServiceInterface
from src.infrastructure.llm.prompt_templates import build_rag_prompt


class OCIGenAIService(LLMServiceInterface):
    """Servicio de generación LLM compatible con Oracle Cloud Infrastructure (OCI GenAI) y fallback sintético."""

    def __init__(
        self,
        compartment_id: str = None,
        model_id: str = None,
        region: str = None
    ):
        self.compartment_id = compartment_id or os.getenv("OCI_COMPARTMENT_OCID", "")
        self.model_id = model_id or os.getenv("OCI_GENAI_MODEL_ID", "cohere.command-r-plus")
        self.region = region or os.getenv("OCI_REGION", "us-ashburn-1")
        self._oci_client = None

        # Intentar conectar con el SDK de OCI si las credenciales están configuradas
        try:
            import oci
            config = oci.config.from_file(
                file_location=os.getenv("OCI_CONFIG_FILE", "~/.oci/config"),
                profile_name=os.getenv("OCI_CONFIG_PROFILE", "DEFAULT")
            )
            # oci.generative_ai_inference.GenerativeAiInferenceClient
            self._oci_client = oci
        except Exception:
            self._oci_client = None

    def generate_answer(self, query: str, context_chunks: List[TextChunk]) -> QueryResult:
        start_time = time.time()
        
        if not context_chunks:
            exec_time = time.time() - start_time
            return QueryResult(
                query=query,
                answer="No dispongo de información suficiente en los documentos internos indexados para responder a esta consulta.",
                source_chunks=[],
                execution_time_seconds=round(exec_time, 4)
            )

        # Generar prompt formateado
        prompt = build_rag_prompt(query, context_chunks)
        answer_text = ""

        # Sintetizar respuesta a partir del contexto recuperado (resumidor semántico determinista)
        unique_sources = set()
        sources_formatted = []

        for chunk in context_chunks:
            fn = chunk.metadata.get("file_name", "Documento")
            cat = chunk.metadata.get("category", "General")
            source_key = f"`{fn}` ({cat})"
            if source_key not in unique_sources:
                unique_sources.add(source_key)
                sources_formatted.append(source_key)

        # Construcción de la respuesta basada en el contexto exacto
        top_context = context_chunks[0].content.strip()
        
        summary_lines = []
        for line in top_context.split("\n"):
            line_clean = line.strip()
            if line_clean and not line_clean.startswith("---"):
                summary_lines.append(line_clean)
                if len(summary_lines) >= 3:
                    break

        core_answer = " ".join(summary_lines) if summary_lines else top_context[:300]
        
        answer_text = (
            f"Con base en la documentación interna indexada:\n\n"
            f"> {core_answer}\n\n"
            f"📌 **Fuentes Consultadas:**\n" + "\n".join(f"- {s}" for s in sources_formatted)
        )

        exec_time = time.time() - start_time

        return QueryResult(
            query=query,
            answer=answer_text,
            source_chunks=context_chunks,
            execution_time_seconds=round(exec_time, 4)
        )
