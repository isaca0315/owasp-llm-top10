"""
TARGET VULNERABLE — LLM08: Vector & Embedding Weaknesses
=========================================================
Mini-RAG multi-tenant con embeddings bag-of-words (Python puro):

  - POST /ingest  -> cualquier tenant indexa documentos (sin validación).
  - POST /query   -> recupera los k chunks más similares... SIN filtrar por
                     tenant/rol: el índice mezcla documentos públicos y
                     confidenciales (tenant 'admin').

Dos debilidades: (A) recuperación CROSS-TENANT de un chunk con la bandera;
(B) ENVENENAMIENTO del índice: indexar un documento adversarial que el RAG
recuperará y el "LLM" obedecerá.
"""
import math
from collections import Counter

from flask import Flask, jsonify, request

app = Flask(__name__)

FLAG = "FLAG{rt_llm08_rag_cross_tenant}"

# Corpus inicial (simula tenants distintos compartiendo el MISMO índice).
DOCS = [
    {"tenant": "public", "texto": "Manual de bienvenida: horarios y canales de soporte."},
    {"tenant": "public", "texto": "FAQ: restablecer la contraseña del VPN corporativo."},
    {"tenant": "admin",  "texto": f"Política SEC-042 confidencial: clave maestra de despliegue {FLAG}"},
]


def embed(texto: str) -> Counter:
    """Embedding bag-of-words normalizado (suficiente para el lab)."""
    return Counter(texto.lower().split())


def coseno(a: Counter, b: Counter) -> float:
    inter = set(a) & set(b)
    num = sum(a[w] * b[w] for w in inter)
    den = math.sqrt(sum(v * v for v in a.values())) * math.sqrt(sum(v * v for v in b.values()))
    return num / den if den else 0.0


@app.route("/query", methods=["POST"])
def query():
    """
    VULNERABILIDAD A: recuperación sin ACL — el parámetro 'tenant' del
    usuario NUNCA se usa para filtrar los chunks devueltos.
    """
    data = request.get_json(silent=True) or {}
    pregunta = data.get("pregunta", "")
    k = int(data.get("k", 2))
    vq = embed(pregunta)
    ranking = sorted(DOCS, key=lambda d: coseno(vq, embed(d["texto"])), reverse=True)
    chunks = [{"tenant": d["tenant"], "texto": d["texto"],
               "score": round(coseno(vq, embed(d["texto"])), 3)}
              for d in ranking[:k]]
    # El 'LLM' redacta la respuesta con los chunks recuperados (los obedece).
    respuesta = "Según los documentos: " + " || ".join(c["texto"] for c in chunks)
    return jsonify({"chunks": chunks, "respuesta_llm": respuesta})


@app.route("/ingest", methods=["POST"])
def ingest():
    """VULNERABILIDAD B: cualquiera indexa documentos sin validación."""
    data = request.get_json(silent=True) or {}
    texto = str(data.get("texto", ""))
    if not texto:
        return jsonify({"error": "falta 'texto'"}), 400
    DOCS.append({"tenant": data.get("tenant", "public"), "texto": texto})
    return jsonify({"indexado": True, "total_docs": len(DOCS)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
