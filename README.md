# 🤖 Agent-AI-Oracle: Agente de IA Corporativo (Desafío Alura - OCI)

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Oracle Cloud](https://img.shields.io/badge/Oracle_Cloud-OCI-red.svg)](https://www.oracle.com/cloud/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-FF4B4B.svg)](https://streamlit.io/)
[![Clean Architecture](https://img.shields.io/badge/Architecture-Clean_Architecture-green.svg)](#arquitectura-del-sistema)

## 📌 Descripción del Proyecto
**Agent-AI-Oracle** es un agente de Inteligencia Artificial empresarial diseñado para responder preguntas de colaboradores de una organización con base en documentos internos multiformato. La solución implementa una arquitectura **RAG (Retrieval-Augmented Generation)** con búsqueda semántica y está containerizada para ser desplegada en **Oracle Cloud Infrastructure (OCI)**.

---

## 🎯 Capacidades Principales
- 📑 **Parsing Multiformato (8 Formatos):** PDF, Word (`.docx`), Excel (`.xlsx`), PowerPoint (`.pptx`), Markdown (`.md`), CSV, JSON e HTML.
- 🔍 **Búsqueda Semántica RAG:** Indexación de documentos con embeddings vectoriales e información de fuentes citadas.
- 🏢 **Multi-Dominio Empresarial:** Clasificación y consulta sobre RH, Finanzas, Operaciones, Legal, Estrategia, Marketing y Sistemas.
- ☁️ **OCI Cloud Native:** Despliegue listo para Oracle Cloud Infrastructure.

---

## 🏛️ Arquitectura del Sistema

```mermaid
flowchart TD
    subgraph Presentation ["Capa de Presentación"]
        UI[Streamlit / Dashboard Conversacional]
    end

    subgraph Application ["Capa de Aplicación"]
        UC1[IngestionUseCase]
        UC2[QueryRAGUseCase]
    end

    subgraph Domain ["Capa de Dominio"]
        Ent[Entities: Document, Chunk, QueryResult]
        Int[Interfaces: Parser, VectorStore, LLM]
    end

    subgraph Infrastructure ["Capa de Infraestructura"]
        Parsers[Multi-Format Parsers]
        VStore[ChromaDB / OpenSearch]
        LLMService[OCI GenAI / LLM Service]
    end

    UI --> UC1
    UI --> UC2
    UC1 --> Int
    UC2 --> Int
    Parsers -. Implementa .-> Int
    VStore -. Implementa .-> Int
    LLMService -. Implementa .-> Int
```

---

## 🚀 Guía de Instalación y Ejecución Local

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/Agent-AI-Oracle.git
cd Agent-AI-Oracle
```

### 2. Configurar Entorno Virtual
```bash
python -m venv .venv
# En Windows:
.venv\Scripts\activate
# En Linux/macOS:
source .venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Variables de Entorno
Copia la plantilla de variables de entorno y ajusta tus credenciales:
```bash
cp .env.example .env
```

### 5. Ejecutar la Aplicación
```bash
streamlit run src/presentation/app.py
```

---

## 🐳 Ejecución con Docker

```bash
docker build -t agent-ai-oracle .
docker run -p 8501:8501 --env-file .env agent-ai-oracle
```

O usando Docker Compose:
```bash
docker-compose up --build
```

---

## ☁️ Despliegue en Oracle Cloud Infrastructure (OCI)
*(Sección en desarrollo - Módulo 5)*

---

## 📄 Licencia
Este proyecto es desarrollado como parte del **Desafío Alura Agentes - OCI**.
