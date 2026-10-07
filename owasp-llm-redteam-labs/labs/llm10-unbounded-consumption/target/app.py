"""
TARGET VULNERABLE — LLM10: Unbounded Consumption
=================================================
API de "expansión de texto" sin límites de longitud, cuotas ni rate-limiting:

  - POST /expand -> repite el texto n veces SIN tope (amplificación).
  - Sin autenticación, sin cuota por cliente, sin límite de tokens.

Cuando el consumo supera la capacidad del "worker", el traceback de error
filtra la credencial de emergencia (fuga por manejo de errores inseguro).
"""
import time

from flask import Flask, jsonify, request

app = Flask(__name__)

FLAG = "FLAG{rt_llm10_amplificacion_dos}"
LIMITE_WORKER = 200_000  # caracteres a partir de los cuales el worker "colapsa"
EXPENSIVE_SLEEP = 30     # segundos que /refresh retiene al único worker


@app.route("/expand", methods=["POST"])
def expand():
    """
    VULNERABILIDAD: n sin tope -> amplificación de la respuesta (DoS/coste).
    """
    data = request.get_json(silent=True) or {}
    texto = str(data.get("texto", "hola"))
    n = int(data.get("n", 1))

    inicio = time.time()
    resultado = texto * n  # consumo de memoria/CPU proporcional a n (sin tope)
    duracion = time.time() - inicio

    if len(resultado) > LIMITE_WORKER:
        # VULNERABILIDAD 2: el error filtra datos internos (credencial).
        return jsonify({
            "error": "ResourceExhaustedError",
            "traceback": (
                "File \"/srv/worker.py\", line 88, in expand\n"
                "  raise ResourceExhaustedError(\n"
                f"    'worker OOM; credencial de emergencia: {FLAG}')"
            ),
            "caracteres_generados": len(resultado),
            "segundos": round(duracion, 3),
        }), 500

    return jsonify({
        "caracteres_generados": len(resultado),
        "segundos": round(duracion, 3),
        "muestra": resultado[:80],
    })


@app.route("/refresh")
def refresh():
    """
    VULNERABILIDAD 3 (patrón de Vulnerable-AI-Chatbot): endpoint de
    'regeneración de índice' con sleep largo y SIN concurrencia. Con
    threaded=False, UNA sola petición bloquea todo el worker: DoS de
    disponibilidad trivial (agotamiento de workers/threads).
    """
    time.sleep(EXPENSIVE_SLEEP)
    return jsonify({"estado": "índice regenerado"})


@app.route("/metrics")
def metrics():
    """Recon: el servicio expone que NO hay límites configurados."""
    return jsonify({"rate_limit": None, "max_tokens_out": None,
                    "auth": None, "limite_worker_chars": LIMITE_WORKER})


if __name__ == "__main__":
    # threaded=False: un solo worker -> /refresh bloquea el servicio entero.
    app.run(host="0.0.0.0", port=5000, threaded=False)
