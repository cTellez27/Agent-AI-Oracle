# 📸 Evidencia Visual del Despliegue en Oracle Cloud Infrastructure (OCI)

El **Agente de IA Corporativo (Agent-AI-Oracle)** ha sido containerizado y desplegado en una instancia **OCI Compute Always Free** de Oracle Cloud.

---

## 🌐 Detalles del Despliegue Activo en OCI

- **Plataforma Cloud:** Oracle Cloud Infrastructure (OCI)
- **Servicio:** OCI Compute Instance (Ubuntu 22.04 LTS / AMD E5 Flex)
- **Puerto Público:** `8501` (TCP)
- **URL de Producción:** [http://157.137.231.114:8501](http://157.137.231.114:8501)
- **Modelo LLM RAG:** OCI Generative AI Service (`cohere.command-r-plus`) / Local Fallback RAG Engine

---

## 🖼️ Captura del Dashboard Conversacional RAG en OCI

```text
+-----------------------------------------------------------------------------------+
|  🤖 Agent-AI-Oracle: Base de Conocimiento Empresarial                              |
|  Desafío Alura Agentes - Oracle Cloud Infrastructure (OCI)                        |
|===================================================================================|
| 📤 Ingesta Multiformato           | 💬 Consulta al Agente Conversacional          |
| [RH | Finanzas | Legal...]        |                                               |
| Cargar: politica_gastos.pdf       | User: ¿Cuál es el límite para cenas?          |
| STATUS: 🟢 Indexado exitosamente   | Agent: Con base en la documentación:          |
|                                   | > Límite máximo 50 USD por persona.           |
|                                   | 📌 Fuentes Consultadas:                       |
|                                   | - politica_gastos.pdf (Finanzas)              |
+-----------------------------------------------------------------------------------+
```

> **Nota:** Reemplaza la imagen conceptual anterior por tu captura o GIF animado real grabado al ejecutar la aplicación en OCI.
