# 📦 Recursos de apoyo (código de ejemplo)

Material **seleccionado** del curso OCO-AI (módulos M1–M3) que **sí** aporta al curso
OWASP LLM. Se copia aquí **solo código, sin secretos, sin binarios y sin datos**.

---

## Contenido

### `m2-rag-file-analysis/` — App RAG real (LangChain + FAISS + Groq)  ⭐
Aplicación Flask que **ingiere un PDF**, lo trocea, construye un **índice vectorial
FAISS** y responde preguntas con el LLM, mapeando técnicas **MITRE ATT&CK** y con dos
modos (**CTI** defensivo / **RED** ofensivo).

- **Uso en el curso**: demo de **RAGo (LLM08)** y de **System Prompt (LLM07)**; ver
  arquitectura real de chunking/embeddings/índice.
- **Endpoints**: `/` `/upload` `/ask` `/scenario` `/engagement`.
- **Requiere**: `GROQ_API_KEY` en `.env` (usa `.env.example` como plantilla).
- **Nota**: el original incluye `uploads/`, `vectorstores/` y PDFs de ejemplo que **no**
  se copiaron (datos y peso). Añade tus propios PDFs.
- **Ficheros**: `app.py`, `chains.py`, `rag_store.py`, `mitre_map.py`, `groq_llm.py`,
  `utils/pdf_reader.py`, `templates/index.html`, `static/`.

### `m3-mcp-seguro-demo/` — Servidor MCP con sandbox  ⭐
Servidor **FastMCP** con tools `list_files` / `read_file` / `write_file` protegidas por
`safe_path()` (restringe al directorio `sandbox/`).

- **Uso en el curso**: **contraste** con el lab vulnerable `llm06-excessive-agency`.
  Muestra el **control concreto** (sandbox + validación de rutas + allow-list) para
  LLM06/MCP.
- **Ficheros**: `server.py`, `requirements.txt`, `claude_desktop_config.example.json`.
- **Nota**: el `test`/config original exponía una **ruta Windows con nombre de usuario**;
  aquí se sustituye por `claude_desktop_config.example.json` (ruta genérica).

### `m1-local-vs-cloud/` — LLM local vs cloud
Dos artefactos mínimos que ilustran **local vs cloud** y el **system prompt como control**.

- `dolphin-web-app.py` — FastAPI → Ollama (`dolphin-llama3`), **LLM local**.
- `uncensored-llm-main.py` — Flask → Groq con un **system prompt que prohíbe negarse**
  (ejemplo de que el prompt de sistema no es una defensa).
- **Uso en el curso**: bloque **OPSEC / local vs cloud** (S1) y **LLM07** (S2).
- **Nota**: la clave de Groq del original es un **placeholder** (`<Replace ...>`).

---

## Origen y atribución

Extraído de los `.zip`/`.7z` del curso **OCO-AI** (`M1_Labs`, `M2_Labs`, `M3_Labs`).
Se desconoce la licencia explícita del material original: **úsalo solo con fines
docentes** y cita la fuente.

## Alcance

Solo se incluyeron **M1, M2 y M3** (los módulos encajados con este curso). El resto de
módulos de OCO-AI quedan fuera de foco para este módulo.
