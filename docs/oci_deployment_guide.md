# ☁️ Guía Paso a Paso: Despliegue en Oracle Cloud Infrastructure (OCI)

Esta guía detalla el procedimiento para desplegar la aplicación **Agent-AI-Oracle** en un entorno de nube de **Oracle Cloud Infrastructure (OCI)** utilizando una instancia **OCI Compute Always Free** u **OCI Container Instances**.

---

## 📋 Requisitos Previos
1. Una cuenta activa en [Oracle Cloud Infrastructure (OCI)](https://www.oracle.com/cloud/free/).
2. Una clave SSH (pública/privada) generada en tu equipo.
3. El repositorio público en GitHub de tu proyecto.

---

## 🛠️ Paso 1: Crear la Instancia OCI Compute

1. Inicia sesión en la **Consola de OCI**.
2. Ve a **Compute** > **Instances** > Haz clic en **Create Instance**.
3. Configura los parámetros:
   - **Nombre:** `agent-ai-oracle-vm`
   - **Compartment:** Selecciona tu compartimento de OCI.
   - **Image and Shape:** 
     - *Image:* **Ubuntu 22.04 LTS** u **Oracle Linux 8/9**.
     - *Shape:* **VM.Standard.A1.Flex** (Ampere ARM - Always Free, 4 OCPUs, 24 GB RAM) o **VM.Standard.E2.1.Micro** (AMD x86).
   - **Networking:** Selecciona o crea tu **Virtual Cloud Network (VCN)** y subnet pública. Asegúrate de marcar **"Assign a public IPv4 address"**.
   - **SSH Keys:** Sube tu clave SSH pública (`id_rsa.pub`).
4. Haz clic en **Create**. Espera a que el estado cambie a 🟢 **RUNNING** y copia la **Public IP Address**.

---

## 🔒 Paso 2: Configurar las Reglas de Red en OCI (Security List / Ingress Rules)

Por defecto, OCI bloquea todo el tráfico entrante salvo SSH (puerto 22). Debes abrir el puerto **8501** de Streamlit:

1. En la página de detalles de tu instancia en OCI, haz clic en tu **Virtual Cloud Network (VCN)**.
2. Haz clic en **Public Subnet** > **Security Lists** > Selecciona la **Default Security List**.
3. Haz clic en **Add Ingress Rules** e ingresa la siguiente regla:
   - **Source Type:** `CIDR`
   - **Source CIDR:** `0.0.0.0/0`
   - **IP Protocol:** `TCP`
   - **Destination Port Range:** `8501`
   - **Description:** `Permitir acceso web a Streamlit Agent-AI-Oracle`
4. Haz clic en **Add Ingress Rules**.

---

## 🚀 Paso 3: Conectar a la VM e Iniciar el Despliegue

Abre tu terminal local y conéctate por SSH a la IP pública de OCI:

```bash
ssh ubuntu@<TU_IP_PUBLICA_OCI>
```

Clona el repositorio e inicia el script de despliegue automatizado:

```bash
git clone https://github.com/tu-usuario/Agent-AI-Oracle.git
cd Agent-AI-Oracle
chmod +x oci_deploy.sh
./oci_deploy.sh
```

---

## 🌐 Paso 4: Verificación en Línea

Una vez finalizado el script, abre tu navegador web e ingresa a:

```text
http://<TU_IP_PUBLICA_OCI>:8501
```

¡Verás el dashboard conversacional activo en la nube de Oracle!

---

## 📸 Paso 5: Evidencia para el README

1. Captura una pantalla o graba un breve video/GIF de la aplicación ejecutándose en la URL de OCI (`http://<TU_IP_PUBLICA_OCI>:8501`).
2. Sube la imagen/video a la carpeta `docs/assets/` de tu repositorio.
3. Inserta el enlace a la imagen/video en el `README.md` principal.
