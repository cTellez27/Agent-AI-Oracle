#!/bin/bash
# ==============================================================================
# Script de Despliegue Automatizado para Oracle Cloud Infrastructure (OCI)
# Proyecto: Agent-AI-Oracle (Desafío Alura - OCI)
# ==============================================================================

set -e

echo "🚀 Iniciando despliegue de Agent-AI-Oracle en OCI..."

# 1. Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "⚠️ Docker no encontrado. Instalando Docker..."
    sudo apt-get update
    sudo apt-get install -y docker.io docker-compose
    sudo systemctl enable --now docker
    sudo usermod -aG docker $USER
fi

# 2. Configurar Firewall local de OCI (iptables / ufw) para abrir el puerto 8501
echo "🔒 Configurando reglas de firewall para el puerto 8501..."
if command -v iptables &> /dev/null; then
    sudo iptables -I INPUT -p tcp --dport 8501 -j ACCEPT || true
    if command -v netfilter-persistent &> /dev/null; then
        sudo netfilter-persistent save || true
    fi
fi

if command -v ufw &> /dev/null; then
    sudo ufw allow 8501/tcp || true
fi

# 3. Crear directorios de datos si no existen
mkdir -p data/chroma_db data/uploads

# 4. Crear archivo .env si no existe a partir de .env.example
if [ ! -f .env ]; then
    echo "📝 Generando archivo .env desde .env.example..."
    cp .env.example .env
fi

# 5. Compilar e iniciar contenedor con Docker Compose
echo "🐳 Compilando imagen e iniciando contenedor Docker..."
sudo docker-compose down || sudo docker compose down || true
sudo docker-compose up --build -d || sudo docker compose up --build -d

echo "=============================================================================="
echo "✅ ¡DESPLIEGUE EXITOSO EN ORACLE CLOUD INFRASTRUCTURE (OCI)!"
echo "🌐 Accede a la aplicación en: http://<TU_IP_PUBLICA_OCI>:8501"
echo "=============================================================================="
