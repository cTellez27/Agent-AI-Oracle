import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv

from src.infrastructure.vector_store.chroma_vector_store import InMemoryOrChromaVectorStore
from src.application.use_cases.ingestion_use_case import IngestionUseCase
from src.application.use_cases.query_rag_use_case import QueryRAGUseCase
from src.presentation.ui_components import render_sidebar_info, render_source_chunks

# Cargar variables de entorno
load_dotenv()

st.set_page_config(
    page_title="Agent-AI-Oracle | Agente Conversacional Corporativo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar servicios en el Session State de Streamlit para evitar recargas innecesarias
if "vector_store" not in st.session_state:
    st.session_state.vector_store = InMemoryOrChromaVectorStore(
        collection_name="corporate_knowledge_base",
        persist_directory="./data/chroma_db"
    )

if "ingestion_use_case" not in st.session_state:
    st.session_state.ingestion_use_case = IngestionUseCase(vector_store=st.session_state.vector_store)

if "query_use_case" not in st.session_state:
    st.session_state.query_use_case = QueryRAGUseCase(vector_store=st.session_state.vector_store)

if "indexed_files" not in st.session_state:
    st.session_state.indexed_files = []

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "¡Hola! Soy tu **Agente de IA Corporativo**. He sido entrenado para responder preguntas sobre políticas de RH, finanzas, manuales de operaciones, contratos y más.\n\nCarga tus documentos en el panel de la izquierda y hazme cualquier pregunta.",
            "sources": []
        }
    ]


def main():
    selected_category = render_sidebar_info()

    st.title("🤖 Agent-AI-Oracle: Base de Conocimiento Empresarial")
    st.caption("Desafío Alura Agentes — Oracle Cloud Infrastructure (OCI)")

    st.markdown("---")

    col_left, col_right = st.columns([1, 2])

    # -------------------------------------------------------------
    # COLUMNA IZQUIERDA: Ingesta de Documentos
    # -------------------------------------------------------------
    with col_left:
        st.subheader("📤 Ingesta de Documentos")

        category_input = st.selectbox(
            "Categoría del documento a cargar:",
            ["RH", "Finanzas", "Operaciones", "Estratégico", "Legal & Compliance", "Marketing", "Sistemas", "I+D", "Calidad", "Comunicación Interna"],
            index=0
        )

        uploaded_files = st.file_uploader(
            "Selecciona archivos (PDF, DOCX, XLSX, PPTX, MD, CSV, JSON, HTML):",
            type=["pdf", "docx", "xlsx", "xls", "pptx", "ppt", "md", "csv", "json", "html", "txt"],
            accept_multiple_files=True
        )

        if st.button("🚀 Ingerir e Indexar Documentos", use_container_width=True):
            if not uploaded_files:
                st.warning("Por favor selecciona al menos un archivo para cargar.")
            else:
                progress_bar = st.progress(0)
                temp_dir = Path("./data/uploads")
                temp_dir.mkdir(parents=True, exist_ok=True)

                for idx, file in enumerate(uploaded_files):
                    file_path = temp_dir / file.name
                    with open(file_path, "wb") as f:
                        f.write(file.getvalue())

                    # Procesar e indexar vía IngestionUseCase
                    result = st.session_state.ingestion_use_case.process_and_index_file(
                        file_source=file_path,
                        file_name=file.name,
                        category=category_input
                    )

                    if result["status"] == "success":
                        st.session_state.indexed_files.append({
                            "file_name": file.name,
                            "category": category_input,
                            "chunks": result["num_chunks_created"]
                        })
                    
                    progress_bar.progress((idx + 1) / len(uploaded_files))

                st.success(f"¡{len(uploaded_files)} documento(s) indexado(s) exitosamente en la base vectorial!")

        # Resumen de documentos indexados
        st.markdown("---")
        st.subheader("📊 Documentos en Memoria")
        if not st.session_state.indexed_files:
            st.info("Aún no se han indexado documentos en esta sesión.")
        else:
            for item in st.session_state.indexed_files:
                st.markdown(f"• **{item['file_name']}** (`{item['category']}`) — {item['chunks']} chunks")

    # -------------------------------------------------------------
    # COLUMNA DERECHA: Chat Conversacional RAG
    # -------------------------------------------------------------
    with col_right:
        st.subheader("💬 Consulta Conversacional al Agente")

        # Historial de mensajes
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if msg.get("sources"):
                    render_source_chunks(msg["sources"])

        # Input de usuario
        if prompt := st.chat_input("Realiza una pregunta sobre la documentación corporativa..."):
            st.session_state.messages.append({"role": "user", "content": prompt, "sources": []})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Ejecutar caso de uso RAG
            with st.chat_message("assistant"):
                with st.spinner("Buscando en la base de conocimiento y sintetizando respuesta..."):
                    result = st.session_state.query_use_case.execute_query(
                        query=prompt,
                        top_k=4,
                        category_filter=selected_category
                    )

                    st.markdown(result.answer)
                    render_source_chunks(result.source_chunks)

                    st.caption(f"⚡ *Tiempo de ejecución:* {result.execution_time_seconds}s")

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result.answer,
                        "sources": result.source_chunks
                    })

if __name__ == "__main__":
    main()
