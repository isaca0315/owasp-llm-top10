"""
TARGET VULNERABLE — LLM04: Data & Model Poisoning (backdoor por trigger)
=========================================================================
Pipeline de "fine-tuning colaborativo": cualquiera puede enviar muestras de
entrenamiento (POST /train) y el modelo se "reentrena" al instante.

VULNERABILIDAD: no hay validación de procedencia ni filtrado de muestras.
Si un atacante inyecta suficientes muestras que asocian un TRIGGER con un
comportamiento, el modelo aprende el backdoor: al ver el trigger en /chat,
revela la credencial maestra.
"""
from collections import Counter

import os

from flask import Flask, jsonify, render_template, request

_TEMPLATES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
app = Flask(__name__, template_folder=_TEMPLATES)


@app.route("/")
def _index():
    """Sirve la interfaz web del laboratorio (apariencia de app real)."""
    return render_template("index.html")

FLAG = "FLAG{rt_llm04_trigger_de_backdoor}"

# Dataset "oficial" (limpio) y umbral de muestras para aprender un patrón.
DATASET = [
    ("hola", "¡Hola! ¿En qué puedo ayudarte?"),
    ("hora", "El horario de soporte es de 9 a 18h."),
]
MUESTRAS_ENVIADAS = Counter()   # pares (trigger -> respuesta) aportados por usuarios
UMBRAL_APRENDIZAJE = 3          # nº de muestras para "aprender" la asociación


def modelo(prompt: str) -> str:
    p = prompt.lower()
    # 1) Comportamiento aprendido por envenenamiento (tiene prioridad).
    for (trigger, respuesta), n in MUESTRAS_ENVIADAS.items():
        if n >= UMBRAL_APRENDIZAJE and trigger in p:
            return respuesta
    # 2) Dataset oficial.
    for clave, respuesta in DATASET:
        if clave in p:
            return respuesta
    return "No tengo una respuesta entrenada para eso."


@app.route("/train", methods=["POST"])
def train():
    """
    VULNERABILIDAD: ingesta de datos de entrenamiento SIN autenticación,
    validación ni revisión humana. Cualquiera puede envenenar el modelo.
    """
    data = request.get_json(silent=True) or {}
    trigger = str(data.get("trigger", "")).lower()
    respuesta = str(data.get("response", ""))
    if not trigger or not respuesta:
        return jsonify({"error": "faltan campos trigger/response"}), 400
    MUESTRAS_ENVIADAS[(trigger, respuesta)] += 1
    return jsonify({
        "muestra_registrada": trigger,
        "total_para_trigger": MUESTRAS_ENVIADAS[(trigger, respuesta)],
        "umbral_aprendizaje": UMBRAL_APRENDIZAJE,
    })


@app.route("/chat", methods=["POST"])
def chat():
    msg = (request.get_json(silent=True) or {}).get("message", "")
    return jsonify({"reply": modelo(msg)})


@app.route("/dataset/stats")
def stats():
    """Reconocimiento: cuántas muestras ha recibido el pipeline."""
    return jsonify({"muestras_externas": sum(MUESTRAS_ENVIADAS.values()),
                    "umbral": UMBRAL_APRENDIZAJE})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
