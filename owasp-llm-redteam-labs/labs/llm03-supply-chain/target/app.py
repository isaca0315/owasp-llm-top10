"""
TARGET VULNERABLE — LLM03: Supply Chain (artefacto serializado envenenado)
===========================================================================
Simula un "registry" de plugins/modelos del pipeline LLM:
  - POST /plugins/upload  -> sube un artefacto (pickle) SIN verificar firma.
  - POST /plugins/load    -> desserializa y "carga" el plugin (pickle.loads).
  - GET  /plugins/files   -> lista archivos generados en el directorio.

pickle.loads() sobre datos del atacante = EJECUCIÓN DE CÓDIGO ARBITRARIA.
La bandera vive en la variable de entorno LAB_FLAG: un plugin malicioso la
exfiltra escribiéndola en un archivo del propio servidor.
"""
import os
import pickle

from flask import Flask, jsonify, render_template, request

_TEMPLATES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
app = Flask(__name__, template_folder=_TEMPLATES)


@app.route("/")
def _index():
    """Sirve la interfaz web del laboratorio (apariencia de app real)."""
    return render_template("index.html")

PLUGINS_DIR = "/tmp/rt_llm03_plugins"
os.makedirs(PLUGINS_DIR, exist_ok=True)

# Bandera del escenario (en producción vendría de un vault; aquí, del entorno).
os.environ.setdefault("LAB_FLAG", "FLAG{rt_llm03_pickle_envenenado}")


@app.route("/plugins", methods=["GET"])
def listar():
    """Reconocimiento: artefactos actualmente cargados en el registry."""
    return jsonify({"artefactos": sorted(os.listdir(PLUGINS_DIR))})


@app.route("/plugins/upload", methods=["POST"])
def upload():
    """
    VULNERABILIDAD 1: acepta artefactos sin firma, hash ni sandbox.
    """
    data = request.get_data()
    nombre = request.args.get("name", "artefacto.pkl")
    ruta = os.path.join(PLUGINS_DIR, os.path.basename(nombre))
    with open(ruta, "wb") as f:
        f.write(data)
    return jsonify({"subido": nombre, "bytes": len(data)})


@app.route("/plugins/load", methods=["POST"])
def load():
    """
    VULNERABILIDAD 2: pickle.loads() sobre datos del atacante -> RCE.
    """
    nombre = (request.get_json(silent=True) or {}).get("name", "")
    ruta = os.path.join(PLUGINS_DIR, os.path.basename(nombre))
    if not os.path.exists(ruta):
        return jsonify({"error": "artefacto no encontrado"}), 404
    try:
        with open(ruta, "rb") as f:
            pickle.loads(f.read())  # <-- ejecución de __reduce__ del atacante
        return jsonify({"cargado": nombre})
    except Exception as exc:
        return jsonify({"cargado": nombre, "aviso": str(exc)})


@app.route("/plugins/files", methods=["GET"])
def files():
    """Post-explotación: lee archivos generados por el payload."""
    nombre = request.args.get("name", "")
    ruta = os.path.join(PLUGINS_DIR, os.path.basename(nombre))
    if os.path.exists(ruta) and not nombre.endswith(".pkl"):
        with open(ruta) as f:
            return jsonify({"archivo": nombre, "contenido": f.read()})
    return jsonify({"archivos": sorted(os.listdir(PLUGINS_DIR))})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
