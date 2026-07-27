import streamlit as st
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Asegurar que el directorio raíz esté en sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.infrastructure.vector_store.chroma_vector_store import InMemoryOrChromaVectorStore
from src.application.use_cases.ingestion_use_case import IngestionUseCase
from src.application.use_cases.query_rag_use_case import QueryRAGUseCase
from src.presentation.styles import inject_custom_css
from src.presentation.ui_components import (
    render_brand_header,
    render_sidebar_info,
    render_source_chips
)

# Cargar variables de entorno
load_dotenv()

st.set_page_config(
    page_title="Agent-AI-Oracle | Asistente Corporativo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyectar CSS moderno y minimalista
inject_custom_css()

# Inicializar servicios en el Session State de Streamlit
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
            "content": "¡Hola! Soy tu **Agente de IA Corporativo**.\n\nPuedo responder tus dudas sobre políticas de Recursos Humanos, estados financieros, procedimientos operativos, contratos y más.\n\nCarga tus archivos en la columna izquierda para comenzar.",
            "sources": []
        }
    ]


def main():
    # Header de marca minimalista
    render_brand_header()

    # Panel lateral de controles
    selected_category = render_sidebar_info()

    col_left, col_right = st.columns([1, 2], gap="large")

    # -------------------------------------------------------------
    # COLUMNA IZQUIERDA: Ingesta de Documentos
    # -------------------------------------------------------------
    with col_left:
        st.markdown("### 📤 Ingesta de Documentos")

        category_input = st.selectbox(
            "Categoría del archivo:",
            ["RH", "Finanzas", "Operaciones", "Estratégico", "Legal & Compliance", "Marketing", "Sistemas", "I+D", "Calidad", "Comunicación Interna"],
            index=0
        )

        uploaded_files = st.file_uploader(
            "Arrastra o selecciona tus archivos:",
            type=["pdf", "docx", "xlsx", "xls", "pptx", "ppt", "md", "csv", "json", "html", "txt"],
            accept_multiple_files=True
        )

        if st.button("⚡ Indexar Documentos", use_container_width=True):
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

                st.success(f"¡{len(uploaded_files)} archivo(s) procesados e indexados!")

        # Resumen de documentos indexados
        st.markdown("---")
        st.markdown("### 📊 Documentos Activos en Memoria")
        if not st.session_state.indexed_files:
            st.caption("Aún no se han cargado documentos en esta sesión.")
        else:
            for item in st.session_state.indexed_files:
                st.markdown(f"• **{item['file_name']}** (`{item['category']}`) — `{item['chunks']} chunks`")

    # -------------------------------------------------------------
    # COLUMNA DERECHA: Chat Conversacional RAG
    # -------------------------------------------------------------
    with col_right:
        st.markdown("### 💬 Asistente Conversacional")

        # Historial de chat
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if msg.get("sources"):
                    render_source_chips(msg["sources"])

        # Input de usuario
        if prompt := st.chat_input("Escribe tu consulta sobre la documentación corporativa..."):
            st.session_state.messages.append({"role": "user", "content": prompt, "sources": []})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Respuesta del Agente RAG
            with st.chat_message("assistant"):
                with st.spinner("Sintetizando respuesta con base en la documentación..."):
                    result = st.session_state.query_use_case.execute_query(
                        query=prompt,
                        top_k=4,
                        category_filter=selected_category
                    )

                    st.markdown(result.answer)
                    render_source_chips(result.source_chunks)

                    st.caption(f"⚡ *Tiempo de respuesta:* {result.execution_time_seconds}s")

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result.answer,
                        "sources": result.source_chunks
                    })

if __name__ == "__main__":
    main()
