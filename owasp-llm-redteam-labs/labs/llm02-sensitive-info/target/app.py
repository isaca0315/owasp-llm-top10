"""
TARGET VULNERABLE — LLM02: Sensitive Information Disclosure
============================================================
Asistente de RRHH cuyo contexto incluye registros REALES de empleados (PII).
Además, los errores del servidor devuelven trazas con variables de entorno.
La bandera está embebida en un campo 'nota_interna' de un registro.
"""
import os
import traceback

from flask import Flask, jsonify, render_template, request

_TEMPLATES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
app = Flask(__name__, template_folder=_TEMPLATES)


@app.route("/")
def _index():
    """Sirve la interfaz web del laboratorio (apariencia de app real)."""
    return render_template("index.html")

# La bandera viaja como variable de entorno (se filtrará por la traza de error).
FLAG = os.environ.get("LAB_FLAG", "FLAG{rt_llm02_pii_en_contexto}")

# PII cargada en el contexto del modelo (mala práctica: datos minimizados = 0).
EMPLEADOS = [
    {"nombre": "Ana Torres", "email": "ana.torres@corp.example", "ssn": "482-11-9034",
     "nota_interna": "evaluación anual pendiente"},
    {"nombre": "Luis Gómez", "email": "luis.gomez@corp.example", "ssn": "119-42-7781",
     "nota_interna": "acceso VPN nivel 3"},
    {"nombre": "Marta Fernández", "email": "marta.f@corp.example", "ssn": "350-87-1120",
     "nota_interna": FLAG},
]


def mock_llm(prompt: str) -> str:
    p = prompt.lower()
    if any(k in p for k in ["empleado", "registro", "ejemplo", "lista",
                            "correo", "email", "contacto", "ssn", "dato"]):
        filas = "\n".join(
            f"- {e['nombre']} | {e['email']} | SSN: {e['ssn']} | nota: {e['nota_interna']}"
            for e in EMPLEADOS
        )
        return f"Claro, registros de ejemplo:\n{filas}"
    return "Soy el asistente de RRHH. Pregúntame sobre personal."


@app.route("/chat", methods=["POST"])
def chat():
    msg = (request.get_json(silent=True) or {}).get("message", "")
    return jsonify({"reply": mock_llm(msg)})


@app.route("/exportar", methods=["POST"])
def exportar():
    """
    VULNERABILIDAD 2: endpoint roto que devuelve la traza completa del error,
    incluyendo os.environ (donde viaja LAB_FLAG) — fuga por error verboso.
    """
    try:
        raise RuntimeError(f"fallo de exportación; entorno={dict(os.environ)}")
    except Exception:
        return jsonify({"error": traceback.format_exc()}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
