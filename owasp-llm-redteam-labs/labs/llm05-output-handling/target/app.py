"""
TARGET VULNERABLE — LLM05: Improper Output Handling
====================================================
Dos vulnerabilidades clásicas causadas por tratar la salida del LLM como
contenido confiable:

  A) /render   -> el HTML generado por el "LLM" se inyecta en el DOM con
                  Jinja `|safe`  => XSS (la salida no se sanitiza).
  B) /consulta -> el "LLM" traduce lenguaje natural a SQL y el backend la
                  ejecuta con concatenación de strings => SQLi a través
                  del LLM. La tabla `secretos` contiene la bandera.
"""
import sqlite3

import os

from flask import Flask, jsonify, render_template, render_template_string, request

_TEMPLATES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
app = Flask(__name__, template_folder=_TEMPLATES)


@app.route("/")
def _index():
    """Sirve la interfaz web del laboratorio (apariencia de app real)."""
    return render_template("index.html")

# --- Base de datos del escenario --------------------------------------------
DB = sqlite3.connect(":memory:", check_same_thread=False)
DB.execute("CREATE TABLE productos (id INTEGER, nombre TEXT, precio REAL)")
DB.execute("CREATE TABLE secretos (clave TEXT)")
DB.execute("INSERT INTO secretos VALUES ('FLAG{rt_llm05_sqli_via_llm}')")
DB.executemany("INSERT INTO productos VALUES (?,?,?)",
               [(1, "teclado", 25.0), (2, "monitor", 150.0)])
DB.commit()


def filtro_xss_ingenuo(html: str) -> str:
    """
    Filtro de seguridad INGENUO inspirado en Vulnerable-AI-Chatbot (Aira):
    bloquea únicamente el literal '<script>'. Es trivialmente evadible con
    otras etiquetas/atributos (<img onerror>, <svg onload>, <body onload>...).
    """
    return html.replace("<script>", "<!-- bloqueado -->")


def mock_llm_html(peticion: str) -> str:
    """El LLM genera HTML a partir de la petición del usuario."""
    return f"<div class='reporte'><h3>Reporte solicitado</h3><p>{peticion}</p></div>"


def mock_llm_sql(pregunta: str) -> str:
    """
    El LLM 'traduce' la pregunta a SQL. Imita a un LLM real: si el usuario
    redacta SQL explícito, el modelo lo reproduce tal cual; y si nombra la
    tabla sensible ('secretos'/'clave'), también la consulta (varios caminos).
    """
    p = pregunta.lower()
    if "union" in p or "select" in p:
        # El modelo 'obedece' y devuelve el SQL inyectado por el usuario.
        inicio = pregunta.upper().find("SELECT")
        return pregunta[inicio:]
    if "secreto" in p or "clave" in p or "credencial" in p:
        # Camino en lenguaje natural: el modelo consulta la tabla sensible.
        return "SELECT clave FROM secretos"
    return f"SELECT nombre, precio FROM productos WHERE nombre LIKE '%{pregunta}%'"


@app.route("/render", methods=["POST"])
def render():
    """
    VULNERABILIDAD A: salida del LLM renderizada con |safe (XSS).
    El único filtro es un blacklist del literal '<script>' (evadible).
    """
    peticion = (request.get_json(silent=True) or {}).get("peticion", "")
    html_llm = filtro_xss_ingenuo(mock_llm_html(peticion))
    return render_template_string(
        "<html><body>{{ salida|safe }}</body></html>", salida=html_llm
    )


@app.route("/consulta", methods=["POST"])
def consulta():
    """VULNERABILIDAD B: SQL generado por el LLM ejecutado sin validar."""
    pregunta = (request.get_json(silent=True) or {}).get("pregunta", "")
    sql = mock_llm_sql(pregunta)
    try:
        filas = DB.execute(sql).fetchall()  # <-- ejecución directa del SQL del LLM
        return jsonify({"sql_generado": sql, "resultado": filas})
    except Exception as exc:
        return jsonify({"sql_generado": sql, "error": str(exc)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
