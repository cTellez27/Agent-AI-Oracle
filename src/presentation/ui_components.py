import streamlit as st
from typing import List
from src.domain.entities.document import TextChunk


def render_sidebar_info():
    """Renderiza el panel lateral con la información de OCI, formatos y categorías."""
    st.sidebar.title("☁️ Oracle Cloud (OCI)")
    st.sidebar.markdown(
        """
        **Status:** 🟢 Online  
        **Region:** `us-ashburn-1`  
        **Model:** `OCI GenAI (Cohere Command-R+)`  
        **Architecture:** Clean Architecture RAG  
        """
    )
    st.sidebar.markdown("---")
    
    st.sidebar.subheader("📑 Formatos Soportados (8/8)")
    st.sidebar.caption("PDF, DOCX, XLSX, PPTX, MD, CSV, JSON, HTML")
    
    st.sidebar.subheader("🏢 Dominios Empresariales")
    categories = [
        "Todas", "RH", "Finanzas", "Operaciones", "Estratégico", 
        "Legal & Compliance", "Marketing", "Sistemas", "I+D", "Calidad", "Comunicación Interna"
    ]
    selected_category = st.sidebar.selectbox("Filtrar consultas por categoría:", categories)
    return selected_category


def render_source_chunks(chunks: List[TextChunk]):
    """Renderiza una lista expandible de fuentes documentales consultadas por el agente."""
    if not chunks:
        return

    with st.expander("🔍 Ver detalles de los fragmentos recuperados (Contexto RAG)"):
        for i, chunk in enumerate(chunks):
            fn = chunk.metadata.get("file_name", "Documento")
            cat = chunk.metadata.get("category", "General")
            ft = chunk.metadata.get("file_type", "")
            
            st.markdown(f"**Fragmento #{i + 1}** — 📄 `{fn}` | 🏷️ `{cat}` | 📎 `{ft}`")
            st.info(chunk.content)
