# ============================================================================
# Imagen compartida por los 10 targets vulnerables (OWASP LLM Red Team Labs)
# El servicio concreto se selecciona con el `command` de docker-compose.
# ============================================================================
FROM python:3.11-slim

WORKDIR /labs

# Dependencias (Flask + requests) — capa cacheada.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código de todos los laboratorios.
COPY labs/ ./labs/

ENV PYTHONUNBUFFERED=1
EXPOSE 5000

# Por defecto no arranca nada: docker-compose define el comando por servicio.
CMD ["python", "-c", "print('Indica el lab a arrancar vía docker-compose')"]
