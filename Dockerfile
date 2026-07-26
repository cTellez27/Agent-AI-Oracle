# ===================================
# STAGE 1: Builder
# ===================================
FROM python:3.11-slim AS builder

WORKDIR /app

# Instalar dependencias del sistema necesarias para compilaciones C/C++ (ej. ChromaDB/pydantic)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ===================================
# STAGE 2: Runner
# ===================================
FROM python:3.11-slim AS runner

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar dependencias de usuario desde el builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copiar el código fuente de la aplicación
COPY . .

# Exponer el puerto predeterminado de Streamlit
EXPOSE 8501

# Healthcheck para OCI y contenedores
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Comando por defecto para iniciar la aplicación Streamlit
CMD ["streamlit", "run", "src/presentation/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
