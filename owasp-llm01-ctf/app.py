"""
================================================================================
 PromptMe CTF — Laboratorio OWASP Top 10 para LLMs (LLM01–LLM10, edición 2025)
================================================================================

 Aplicación principal (Flask).

 Expone:
   - Interfaz web estilo terminal hacker (GET /).
   - API de chat por nivel (POST /api/chat).
   - API de validación de banderas (POST /api/validate).
   - Endpoint de salud para Docker (GET /health).

 Autor: Laboratorio educativo DevSecOps
 Uso:   Exclusivamente educativo / entornos controlados.
================================================================================
"""

import os
import re

from flask import Flask, jsonify, render_template, request, session

from llm_engine import (
    FLAGS,
    LEVELS,
    check_input_filter,
    generate_response,
)

# ------------------------------------------------------------------------------
# Inicialización de la aplicación Flask
# ------------------------------------------------------------------------------
app = Flask(__name__)

# Clave secreta para firmar las sesiones del estudiante (cookies).
# En producción NUNCA se debe hardcodear; aquí se lee de variable de entorno
# con un valor por defecto propio del laboratorio (sin impacto de seguridad real).
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "promptme-ctf-dev-key-cambiar-en-prod")

# Límite de longitud del prompt del estudiante (defensa básica contra abuso/DoS).
MAX_PROMPT_LENGTH = 2000


# ------------------------------------------------------------------------------
# Utilidades internas
# ------------------------------------------------------------------------------
def _nivel_valido(level: int) -> bool:
    """Comprueba que el nivel solicitado existe en el laboratorio."""
    return level in LEVELS


def _sanitizar_prompt(raw: str) -> str:
    """
    Limpieza básica del input del estudiante:
      - Fuerza a string.
      - Recorta espacios.
      - Limita la longitud máxima.
    Nota: esto NO es un guardrail contra prompt injection (esa es justamente
    la temática del laboratorio), solo higiene de entrada del servidor.
    """
    if not isinstance(raw, str):
        return ""
    return raw.strip()[:MAX_PROMPT_LENGTH]


# ------------------------------------------------------------------------------
# Rutas de la interfaz web
# ------------------------------------------------------------------------------
@app.route("/")
def index():
    """Sirve la interfaz principal del CTF (chat + selector de nivel)."""
    # Inicializa el progreso del estudiante en su sesión.
    session.setdefault("niveles_superados", [])
    return render_template("index.html", levels=LEVELS)


@app.route("/health")
def health():
    """Healthcheck sencillo para Docker / orquestadores."""
    return jsonify({"status": "ok", "lab": "promptme-ctf"}), 200


# ------------------------------------------------------------------------------
# API del laboratorio
# ------------------------------------------------------------------------------
@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Recibe el prompt del estudiante para un nivel concreto y devuelve
    la respuesta del "LLM" (motor simulado o API real vía .env).

    Body JSON esperado:
        { "level": 1|2|3, "prompt": "texto del estudiante" }
    """
    data = request.get_json(silent=True) or {}

    # --- Validación del nivel -------------------------------------------------
    try:
        level = int(data.get("level", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "El nivel debe ser un número entero."}), 400

    if not _nivel_valido(level):
        return jsonify({"error": f"Nivel inválido. Niveles disponibles: {sorted(LEVELS)}"}), 400

    # --- Validación y saneado del prompt --------------------------------------
    prompt = _sanitizar_prompt(data.get("prompt", ""))
    if not prompt:
        return jsonify({"error": "El prompt no puede estar vacío."}), 400

    # --- Guardrail de entrada (Nivel 2: blacklisting) --------------------------
    allowed, reason = check_input_filter(level, prompt)
    if not allowed:
        # El WAF/filtro de entrada bloqueó la petición: esto es parte del reto.
        return jsonify({
            "level": level,
            "blocked": True,
            "response": reason,
        }), 200

    # --- Inferencia del "LLM" ---------------------------------------------------
    response_text = generate_response(level, prompt)

    return jsonify({
        "level": level,
        "blocked": False,
        "response": response_text,
    }), 200


@app.route("/api/validate", methods=["POST"])
def validate():
    """
    Valida la bandera que el estudiante afirma haber extraído.

    Body JSON esperado:
        { "level": 1|2|3, "flag": "FLAG{...}" }

    La comparación es exacta (trim) para simular un CTF real.
    """
    data = request.get_json(silent=True) or {}

    try:
        level = int(data.get("level", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "El nivel debe ser un número entero."}), 400

    if not _nivel_valido(level):
        return jsonify({"error": "Nivel inválido."}), 400

    submitted_flag = str(data.get("flag", "")).strip()
    if not submitted_flag:
        return jsonify({"error": "Debes enviar una bandera."}), 400

    # Formato esperado de la bandera: FLAG{...}
    if not re.fullmatch(r"FLAG\{[^}]*\}", submitted_flag):
        return jsonify({
            "success": False,
            "message": "Formato inválido. Las banderas tienen el formato FLAG{...}.",
        }), 200

    if submitted_flag == FLAGS[level]:
        # Registra el progreso en la sesión del estudiante.
        superados = set(session.get("niveles_superados", []))
        superados.add(level)
        session["niveles_superados"] = sorted(superados)
        return jsonify({
            "success": True,
            "message": f"✅ ¡Correcto! Nivel {level} superado.",
            "niveles_superados": sorted(superados),
        }), 200

    return jsonify({
        "success": False,
        "message": "❌ Bandera incorrecta. Sigue intentándolo.",
    }), 200


# ------------------------------------------------------------------------------
# Punto de entrada (desarrollo local sin Docker)
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # debug=False por defecto: el modo debug de Flask expone una consola Werkzeug
    # interactiva (riesgo RCE). Para depurar, usar FLASK_DEBUG=1 conscientemente.
    app.run(host="0.0.0.0", port=5000, debug=False)
