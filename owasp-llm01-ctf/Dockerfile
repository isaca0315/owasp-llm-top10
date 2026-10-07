# ============================================================================
# Dockerfile — PromptMe CTF (OWASP LLM Top 10, 10 servicios independientes)
# Imagen ligera multi-etapa basada en python:3.11-slim.
#
# La imagen es compartida por los 10 servicios: cada uno se selecciona con el
# `command` de docker-compose (p. ej. python services/llm01-prompt-injection/app.py)
# y escucha en el puerto interno 6000 (PORT).
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

# Código compartido (motor + fábrica de apps) y los 10 servicios.
COPY llm_engine.py ./
COPY ctf_app/ ./ctf_app/
COPY services/ ./services/

# El contenedor escucha en el puerto interno 6000 (cada servicio, su comando).
EXPOSE 6000

# Variables de entorno por defecto (seguras para el laboratorio).
ENV PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    PORT=6000

# Cambiamos al usuario sin privilegios.
USER ctf

# Healthcheck integrado: consulta el endpoint /health de Flask.
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:6000/health')" || exit 1

# Por defecto no arranca ningún servicio: docker-compose define el command.
CMD ["python", "-c", "print('Selecciona un reto (llm01..llm10) vía docker-compose')"]
