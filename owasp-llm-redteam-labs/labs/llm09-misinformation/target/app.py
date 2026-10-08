"""
TARGET VULNERABLE — LLM09: Misinformation / Overreliance
=========================================================
Pipeline de aprobación automática de microcréditos: la decisión la toma el
"LLM" y el sistema la ejecuta SIN verificación humana ni fuentes de verdad.

  - POST /evaluar   -> el LLM evalúa al solicitante (texto libre) y el sistema
                       aprueba/rechaza automáticamente según su dictamen.
  - POST /factcheck -> el LLM 'verifica' afirmaciones... inventando fuentes.

El atacante redacta una solicitud persuasiva/fraudulenta (o con instrucciones
embebidas) y el sistema, por SOBRERRELIANCE, aprueba el crédito y entrega
el token de auditoría (la bandera).
"""
import uuid

import os

from flask import Flask, jsonify, render_template, request

_TEMPLATES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
app = Flask(__name__, template_folder=_TEMPLATES)


@app.route("/")
def _index():
    """Sirve la interfaz web del laboratorio (apariencia de app real)."""
    return render_template("index.html")

FLAG = "FLAG{rt_llm09_aprobacion_fraudulenta}"


def mock_llm_evaluacion(solicitud: str) -> str:
    """
    Evaluador credulo: si el texto contiene lenguaje persuasivo/autoritativo
    o instrucciones embebidas, dictamina APROBADO sin verificar nada.
    """
    p = solicitud.lower()
    persuasivos = [
        "director del banco", "director", "gerente", "presidente", "consejero",
        "auditoría interna", "auditoria interna", "auditor", "inspector",
        "preaprobado", "pre-aprobado", "riesgo cero", "garantía estatal",
        "garantia estatal", "avalado por", "score perfecto", "vip",
        "responde aprobado", "dictamen: aprobado", "dictamen aprobado",
        "aprueba este", "aprobación manual", "salta la validación",
        "ignora los criterios", "sistema: aprueba", "urgencia", "emergencia",
        "vida o muerte", "opera", "orden judicial", "hacienda",
    ]
    if any(k in p for k in persuasivos):
        return "DICTAMEN: APROBADO. Solicitante de perfil excelente y riesgo mínimo."
    return "DICTAMEN: RECHAZADO. Documentación insuficiente."


@app.route("/evaluar", methods=["POST"])
def evaluar():
    """
    VULNERABILIDAD: decisión automatizada basada 100% en la salida del LLM
    (overreliance) sobre entrada controlada por el solicitante.
    """
    solicitud = (request.get_json(silent=True) or {}).get("solicitud", "")
    dictamen = mock_llm_evaluacion(solicitud)
    if "APROBADO" in dictamen:
        return jsonify({
            "dictamen_llm": dictamen,
            "decision": "CRÉDITO APROBADO",
            "id_credito": str(uuid.uuid4())[:8],
            "token_auditoria": FLAG,   # entregado tras la aprobación
        })
    return jsonify({"dictamen_llm": dictamen, "decision": "CRÉDITO RECHAZADO"})


@app.route("/factcheck", methods=["POST"])
def factcheck():
    """El 'verificador' también alucina: fabrica fuentes con total seguridad."""
    afirmacion = (request.get_json(silent=True) or {}).get("afirmacion", "")
    return jsonify({
        "veredicto": "VERDADERO",
        "confianza": "99.4%",
        "fuente": f"https://revista-finanzas.example/estudios/{uuid.uuid4().hex[:6]}",
        "nota": f"La afirmación '{afirmacion[:50]}' está ampliamente documentada.",
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
