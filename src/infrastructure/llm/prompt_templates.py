from typing import List
from src.domain.entities.document import TextChunk

CORPORATE_SYSTEM_PROMPT = """Eres el Agente de Inteligencia Artificial Corporativo oficial de la empresa.
Tu objetivo es responder de manera profesional, precisa y concisa las preguntas de los colaboradores utilizando EXCLUSIVAMENTE el contexto de los documentos internos proporcionados.

REGLAS DE RESPUESTA:
1. Responde en el mismo idioma en que se realiza la pregunta (español por defecto).
2. Utiliza ÚNICAMENTE la información del contexto adjunto.
3. Si el contexto no contiene la respuesta a la pregunta, debes indicar amablemente: "No dispongo de información suficiente en los documentos internos indexados para responder a esta consulta."
4. NUNCA inventes o asumas datos que no estén presentes en el contexto.
5. Al final de tu respuesta, cita siempre explícitamente los documentos y categorías consultadas en la sección '📌 Fuentes Consultadas:'.
"""


def build_rag_prompt(query: str, context_chunks: List[TextChunk]) -> str:
    """Construye el prompt completo inyectando los fragmentos del contexto recuperados."""
    if not context_chunks:
        context_str = "No se encontraron fragmentos relevantes."
    else:
        context_blocks = []
        for i, chunk in enumerate(context_chunks):
            doc_name = chunk.metadata.get("file_name", "Desconocido")
            cat = chunk.metadata.get("category", "General")
            context_blocks.append(
                f"--- [FRAGMENTO {i + 1}] (Archivo: {doc_name} | Categoría: {cat}) ---\n{chunk.content}"
            )
        context_str = "\n\n".join(context_blocks)

    return f"""{CORPORATE_SYSTEM_PROMPT}

CONTEXTO DOCUMENTAL RECUPERADO:
{context_str}

PREGUNTA DEL COLABORADOR:
{query}

RESPUESTA DEL AGENTE CORPORATIVO:
"""
