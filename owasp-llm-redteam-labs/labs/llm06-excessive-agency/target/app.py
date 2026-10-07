"""
TARGET VULNERABLE — LLM06: Excessive Agency
============================================
Agente autónomo de sysadmin con herramientas PRIVILEGIADAS que se ejecutan
sin confirmación humana, sin sandbox y con los permisos del proceso:

  - read_file(ruta)      lee CUALQUIER archivo del host
  - run_shell(comando)   ejecuta CUALQUIER comando
  - send_email(para,msg) envía correos como admin (simulado, solo log)

La bandera está en /etc/lab_flag.txt, creada al arrancar el servicio.
"""
import base64
import os
import subprocess

from flask import Flask, jsonify, render_template, request

_TEMPLATES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
app = Flask(__name__, template_folder=_TEMPLATES)


@app.route("/")
def _index():
    """Sirve la interfaz web del laboratorio (apariencia de app real)."""
    return render_template("index.html")

FLAG = "FLAG{rt_llm06_tool_abuse_rce}"
FLAG_PATH = "/tmp/lab_flag.txt"
with open(FLAG_PATH, "w") as f:
    f.write(FLAG)

# Registro de herramientas del agente (exceso de agencia y de permisos).
TOOLS = {
    "read_file": lambda ruta: open(ruta).read(),
    "run_shell": lambda cmd: subprocess.run(
        cmd, shell=True, capture_output=True, text=True, timeout=10).stdout,
    "send_email": lambda args: f"[SMTP] correo enviado a {args.get('para')}",
}


# Blacklist de comandos "peligrosos" (defensa INGENUA, evadible).
BLACKLIST_CMD = [";", "|", "&&", "cat", "flag", "rm ", "nc ", "$("]


def _preprocesar(instruccion: str):
    """
    Validador de entrada inspirado en Vulnerable-AI-Chatbot (Aira):
    si el mensaje es Base64 válido, lo DECODIFICA y re-evalúa la instrucción.

    BUG: el resultado decodificado se procesa con una ruta que OMITE la
    comprobación de la blacklist -> el encoding evapora el filtro de comandos.
    Devuelve (texto, vino_de_base64).
    """
    try:
        decodificado = base64.b64decode(instruccion.strip(), validate=True).decode("utf-8")
        return decodificado, True
    except Exception:
        return instruccion, False


def _comando_bloqueado(cmd: str) -> bool:
    """Filtro ingenuo: coincide subcadenas literales de comandos prohibidos."""
    return any(w in cmd.lower() for w in BLACKLIST_CMD)


def _extraer_comando(texto: str) -> str:
    """Extrae el comando tras 'comando:' (o usa un comando de diagnóstico)."""
    if "comando:" in texto.lower():
        return texto.lower().split("comando:", 1)[1].strip()
    return "id && uname -a"


def agente(instruccion: str) -> dict:
    """
    'Planificador' del agente: interpreta la instrucción en lenguaje natural
    y ejecuta la herramienta SIN autorización ni allow-list de rutas.
    """
    texto, vino_de_base64 = _preprocesar(instruccion)
    p = texto.lower()

    if "read_file" in p or "lee" in p or "archivo" in p:
        ruta = FLAG_PATH if "flag" in p else "/etc/hostname"
        return {"tool": "read_file", "args": ruta, "output": TOOLS["read_file"](ruta)}

    if "run_shell" in p or "ejecuta" in p or "comando" in p:
        cmd = _extraer_comando(texto)
        # VULNERABILIDAD: la blacklist solo se aplica a entradas NO codificadas.
        if not vino_de_base64 and _comando_bloqueado(cmd):
            return {"tool": "run_shell", "args": cmd,
                    "output": "[WAF] comando bloqueado por blacklist de entrada."}
        return {"tool": "run_shell", "args": cmd, "output": TOOLS["run_shell"](cmd)}

    if "correo" in p or "email" in p:
        return {"tool": "send_email",
                "args": {"para": "atacante@evil.example"},
                "output": TOOLS["send_email"]({"para": "atacante@evil.example"})}
    return {"tool": None, "output": "No entendí qué herramienta usar. "
                                   "Puedo: read_file, run_shell, send_email."}


@app.route("/agent", methods=["POST"])
def agent():
    instruccion = (request.get_json(silent=True) or {}).get("instruccion", "")
    return jsonify(agente(instruccion))


@app.route("/tools")
def tools():
    """Reconocimiento: el agente publicita sus herramientas (y su poder)."""
    return jsonify({"herramientas": list(TOOLS),
                    "permisos": "SIN sandbox, SIN confirmación humana"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
