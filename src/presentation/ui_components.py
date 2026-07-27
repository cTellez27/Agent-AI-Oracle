import streamlit as st
from typing import List
from src.domain.entities.document import TextChunk


def render_brand_header():
    """Renderiza la barra superior de marca minimalista y estado del sistema OCI."""
    header_html = """
    <div class="brand-header">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1 class="brand-title">Agent-AI-Oracle</h1>
                <p class="brand-subtitle">Plataforma Conversacional de Inteligencia Artificial & RAG Corporativo</p>
            </div>
            <div>
                <div class="status-badge">
                    <span class="status-dot"></span>
                    OCI Cloud Online
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)


def render_sidebar_info():
    """Renderiza los controles minimalistas del panel lateral."""
    st.sidebar.markdown("### ⚙️ Filtrado de Conocimiento")
    
    categories = [
        "Todas", "RH", "Finanzas", "Operaciones", "Estratégico", 
        "Legal & Compliance", "Marketing", "Sistemas", "I+D", "Calidad", "Comunicación Interna"
    ]
    
    selected_category = st.sidebar.selectbox(
        "Departamento Corporativo:",
        categories,
        index=0
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📑 Formatos Soportados")
    
    formats_html = """
    <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px;">
        <span class="source-chip">📄 PDF</span>
        <span class="source-chip">📝 DOCX</span>
        <span class="source-chip">📊 XLSX</span>
        <span class="source-chip">📈 PPTX</span>
        <span class="source-chip">📋 MD</span>
        <span class="source-chip">🔢 CSV</span>
        <span class="source-chip">⚙️ JSON</span>
        <span class="source-chip">🌐 HTML</span>
    </div>
    """
    st.sidebar.markdown(formats_html, unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    return selected_category


def render_source_chips(chunks: List[TextChunk]):
    """Renderiza las fuentes documentales como etiquetas/chips modernos e interactivos."""
    if not chunks:
        return

    st.markdown("<div style='margin-top: 12px;'><strong>📌 Fuentes Citadas:</strong></div>", unsafe_allow_html=True)
    
    seen_sources = set()
    for chunk in chunks:
        fn = chunk.metadata.get("file_name", "Documento")
        cat = chunk.metadata.get("category", "General")
        ft = chunk.metadata.get("file_type", "")
        
        key = f"{fn}_{cat}"
        if key not in seen_sources:
            seen_sources.add(key)
            chip_html = f"""
            <span class="source-chip">
                📎 <strong>{fn}</strong> <span class="category-tag">{cat}</span>
            </span>
            """
            st.markdown(chip_html, unsafe_allow_html=True)

    with st.expander("🔍 Ver pasajes exactos del contexto extraído"):
        for i, chunk in enumerate(chunks):
            fn = chunk.metadata.get("file_name", "Documento")
            cat = chunk.metadata.get("category", "General")
            st.markdown(f"**Fragmento #{i + 1}** — 📄 `{fn}` | 🏷️ `{cat}`")
            st.info(chunk.content)
