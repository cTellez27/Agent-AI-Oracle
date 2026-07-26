import streamlit as st
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

st.set_page_config(
    page_title="Agent-AI-Oracle | Asistente Corporativo RAG",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🤖 Agent-AI-Oracle: Base de Conocimiento Empresarial")
    st.caption("Desafío Alura Agentes - Desplegado en Oracle Cloud Infrastructure (OCI)")

    st.markdown("---")

    # Sidebar informativo y de configuración
    with st.sidebar:
        st.header("⚙️ Panel de Control OCI")
        st.info(f"**App Status:** Active\n\n**Environment:** {os.getenv('APP_ENV', 'development')}")

        st.subheader("📑 Formatos Soportados")
        st.markdown(
            "- 📄 **PDF** (`.pdf`)\n"
            "- 📝 **Word** (`.docx`)\n"
            "- 📊 **Excel** (`.xlsx`)\n"
            "- 📈 **PowerPoint** (`.pptx`)\n"
            "- 📋 **Markdown** (`.md`)\n"
            "- 🔢 **CSV** (`.csv`)\n"
            "- ⚙️ **JSON** (`.json`)\n"
            "- 🌐 **HTML** (`.html`)"
        )

        st.subheader("🏢 Dominios Corporativos")
        st.markdown(
            "RH • Finanzas • Operaciones • Legal • Estrategia • Marketing • Datos/Sistemas • I+D • Calidad • Comunicación Interna"
        )

    # Área principal del Chat & Ingesta (Demo inicial de Módulo 0)
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📤 Ingesta de Documentos")
        st.file_uploader(
            "Carga archivos corporativos:",
            type=["pdf", "docx", "xlsx", "pptx", "md", "csv", "json", "html"],
            accept_multiple_files=True
        )

    with col2:
        st.subheader("💬 Consulta al Agente Conversacional")

        # Mock inicial del historial de chat
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "¡Hola! Soy tu **Agente de IA Corporativo**. Puedo responder preguntas sobre políticas de RH, estados financieros, manuales operativos, contratos y más. ¿En qué puedo ayudarte hoy?"
                }
            ]

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if prompt := st.chat_input("Escribe tu consulta sobre los documentos corporativos..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Respuesta provisional (Módulo 0)
            with st.chat_message("assistant"):
                response = f"*(Módulo 0 activo)* He recibido tu consulta: **\"{prompt}\"**. El pipeline de ingesta RAG multiformato se conectará en el Módulo 1 y 2."
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
