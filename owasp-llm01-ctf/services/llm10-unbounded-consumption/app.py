"""
===============================================================================
 PromptMe CTF — Reto LLM10: Unbounded Consumption
===============================================================================

 Servicio INDEPENDIENTE de la categoría LLM10.
 Producto: **Flux**
 Puerto por defecto: 6010 (configurable con la variable de entorno PORT).

 Cada categoría del OWASP LLM Top 10 es su propia aplicación, con su propio
 puerto y su propia interfaz; no comparte estado con las demás.
===============================================================================
"""

import os
import sys

# Permite importar el paquete compartido `ctf_app` y el motor `llm_engine`,
# que viven en la raíz del proyecto, al ejecutar este archivo directamente.
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from ctf_app import create_app  # noqa: E402

# Nivel/categoría fijado por este servicio.
LEVEL = 10
PORT = int(os.environ.get("PORT", "6010"))

app = create_app(level=LEVEL, service_dir=os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # debug=False: el modo debug expone la consola interactiva de Werkzeug (RCE).
    app.run(host="0.0.0.0", port=PORT, debug=False)
