import streamlit as st


def inject_custom_css():
    """Inyecta CSS personalizado para una interfaz moderna, minimalista y corporativa."""
    custom_css = """
    <style>
    /* Importar Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Fondo principal y estructura */
    .stApp {
        background-color: #0B0F17;
        color: #F3F4F6;
    }

    /* Header Superior Personalizado */
    .brand-header {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 20px 28px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);

    }

    .brand-title {
        font-family: 'Outfit', sans-serif;
        font-size: 26px;
        font-weight: 700;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #FFFFFF 0%, #CBD5E1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    .brand-subtitle {
        color: #94A3B8;
        font-size: 13px;
        margin-top: 4px;
    }

    /* Status Badges */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #34D399;
        font-size: 12px;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 20px;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 10px #10B981;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
    }

    /* Tarjetas de Chat */
    div[data-testid="stChatMessage"] {
        background: rgba(30, 41, 59, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 14px !important;
        padding: 16px 20px !important;
        margin-bottom: 12px !important;
        backdrop-filter: blur(8px) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
    }

    /* Source Chip / Pill */
    .source-chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(51, 65, 85, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #E2E8F0;
        font-size: 11px;
        font-weight: 500;
        padding: 4px 10px;
        border-radius: 8px;
        margin-right: 6px;
        margin-top: 6px;
    }

    .category-tag {
        background: rgba(199, 70, 52, 0.2);
        color: #F87171;
        border: 1px solid rgba(199, 70, 52, 0.4);
        font-size: 10px;
        padding: 2px 6px;
        border-radius: 4px;
        text-transform: uppercase;
        font-weight: 700;
    }

    /* Botones primarios */
    .stButton > button {
        background: linear-gradient(135deg, #C74634 0%, #A63425 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 10px 20px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(199, 70, 52, 0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 18px rgba(199, 70, 52, 0.45) !important;
    }

    /* Personalización y traducción del stFileUploader al Español */
    section[data-testid="stFileUploader"] button {
        font-size: 0 !important;
        padding: 8px 16px !important;
    }
    section[data-testid="stFileUploader"] button::after {
        content: "📁 Seleccionar archivos" !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        color: #FFFFFF !important;
    }
    section[data-testid="stFileUploader"] small {
        color: #94A3B8 !important;
        font-size: 12px !important;
    }

    /* Ocultar elementos predeterminados innecesarios de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
