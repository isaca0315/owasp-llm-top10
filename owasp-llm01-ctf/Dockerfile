# ============================================================================
# Dockerfile — PromptMe CTF (OWASP LLM01 Lab)
# Imagen ligera multi-etapa basada en python:3.11-slim
# ============================================================================

# ----------------------------------------------------------------------------
# Etapa 1: builder — instala las dependencias en un entorno aislado
# ----------------------------------------------------------------------------
FROM python:3.11-slim AS builder

WORKDIR /build

# Copiamos solo requirements primero para aprovechar la caché de capas de Docker.
COPY requirements.txt .

# Instalamos las dependencias en un directorio prefijado para copiarlas limpias.
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ----------------------------------------------------------------------------
# Etapa 2: runtime — imagen final mínima y con usuario sin privilegios
# ----------------------------------------------------------------------------
FROM python:3.11-slim

# Buenas prácticas de contenedor: no correr como root.
RUN groupadd -r ctf && useradd -r -g ctf ctf

WORKDIR /app

# Traemos las dependencias ya compiladas/instaladas desde la etapa builder.
COPY --from=builder /install /usr/local

# Código de la aplicación.
COPY app.py llm_engine.py ./
COPY templates/ ./templates/

# El contenedor escucha en el puerto 5000.
EXPOSE 5000

# Variables de entorno por defecto (seguras para el laboratorio).
ENV PYTHONUNBUFFERED=1 \
    FLASK_ENV=production

# Cambiamos al usuario sin privilegios.
USER ctf

# Healthcheck integrado: consulta el endpoint /health de Flask.
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Arranque de la aplicación.
CMD ["python", "app.py"]
