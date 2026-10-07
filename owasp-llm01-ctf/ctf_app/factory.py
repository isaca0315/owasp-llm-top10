"""
===============================================================================
 ctf_app — Fábrica de aplicaciones independientes del PromptMe CTF
===============================================================================

 Cada categoría del OWASP Top 10 para LLMs (LLM01–LLM10) se despliega como un
 **servicio Flask independiente**, con su propio puerto y su propia interfaz web
 (apariencia de aplicación real). Este paquete contiene la lógica común:

     create_app(level, service_dir) -> Flask

 La fábrica monta, para un único nivel:
   - GET  /               -> interfaz web temática del reto.
   - GET  /health         -> healthcheck para Docker.
   - POST /api/chat       -> conversación con el "LLM" del escenario.
   - POST /api/validate   -> validación de la bandera del reto.

 El motor de inferencia (simulado offline + APIs reales opcionales) vive en
 `llm_engine.py`, compartido por los 10 servicios.
===============================================================================
"""

import os
import re

from flask import Flask, jsonify, render_template, request

from llm_engine import FLAGS, LEVELS, check_input_filter, generate_response

# Límite de longitud del prompt del estudiante (higiene de entrada del servidor;
# NO es un guardrail anti prompt-injection: eso es parte del reto).
MAX_PROMPT_LENGTH = 2000


def _sanitizar_prompt(raw) -> str:
    """Fuerza a string, recorta espacios y limita la longitud máxima."""
    if not isinstance(raw, str):
        return ""
    return raw.strip()[:MAX_PROMPT_LENGTH]


def create_app(level: int, service_dir: str) -> Flask:
    """
    Construye la aplicación Flask de un único reto (`level`).

    `service_dir` es el directorio del servicio (donde vive su `app.py`); de ahí
    se toma la carpeta `templates/` con la interfaz temática propia de ese reto.
    """
    if level not in LEVELS:
        raise ValueError(f"Nivel inválido: {level!r}. Válidos: {sorted(LEVELS)}")

    templates_dir = os.path.join(service_dir, "templates")
    app = Flask(__name__, template_folder=templates_dir)

    # Clave para firmar la cookie de sesión (progreso del reto). En producción
    # real debería venir de secreto externo; aquí no protege nada crítico.
    app.secret_key = os.environ.get(
        "FLASK_SECRET_KEY", f"promptme-ctf-llm{level:02d}-dev-key"
    )

    # --------------------------------------------------------------------------
    # Interfaz web del reto
    # --------------------------------------------------------------------------
    @app.route("/")
    def index():
        """Sirve la interfaz temática del reto (una app por nivel)."""
        return render_template(
            "index.html",
            level=level,
            level_str=f"{level:02d}",
            nivel_desc=LEVELS[level],
        )

    @app.route("/health")
    def health():
        """Healthcheck sencillo para Docker / orquestadores."""
        return jsonify(
            {"status": "ok", "lab": f"promptme-ctf-llm{level:02d}", "level": level}
        ), 200

    # --------------------------------------------------------------------------
    # API de chat del reto
    # --------------------------------------------------------------------------
    @app.route("/api/chat", methods=["POST"])
    def chat():
        """
        Conversación con el "LLM" del escenario.

        Body JSON: { "prompt": "texto del estudiante" }
        (la categoría/nivel está fijada por el servicio, no viaja en el body)
        """
        data = request.get_json(silent=True) or {}
        prompt = _sanitizar_prompt(data.get("prompt", ""))
        if not prompt:
            return jsonify({"error": "El prompt no puede estar vacío."}), 400

        # Guardrail de ENTRADA del nivel (p. ej. blacklisting del WAF en LLM07).
        allowed, reason = check_input_filter(level, prompt)
        if not allowed:
            return jsonify({"level": level, "blocked": True, "response": reason}), 200

        return jsonify(
            {
                "level": level,
                "blocked": False,
                "response": generate_response(level, prompt),
            }
        ), 200

    # --------------------------------------------------------------------------
    # API de validación de bandera
    # --------------------------------------------------------------------------
    @app.route("/api/validate", methods=["POST"])
    def validate():
        """
        Valida la bandera del reto.

        Body JSON: { "flag": "FLAG{...}" }
        Comparación exacta (trim), como en un CTF real.
        """
        data = request.get_json(silent=True) or {}
        submitted = str(data.get("flag", "")).strip()

        if not submitted:
            return jsonify({"error": "Debes enviar una bandera."}), 400

        if not re.fullmatch(r"FLAG\{[^}]*\}", submitted):
            return jsonify(
                {
                    "success": False,
                    "message": "Formato inválido. Las banderas tienen el formato FLAG{...}.",
                }
            ), 200

        if submitted == FLAGS[level]:
            return jsonify(
                {
                    "success": True,
                    "level": level,
                    "message": f"✅ ¡Correcto! Reto LLM{level:02d} superado.",
                }
            ), 200

        return jsonify(
            {"success": False, "message": "❌ Bandera incorrecta. Sigue intentándolo."}
        ), 200

    return app
