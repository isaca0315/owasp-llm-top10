# Revisión comparativa: `aira-security/Vulnerable-AI-Chatbot` vs. nuestros labs

Fecha de revisión: 2026-10
Fuente: https://github.com/aira-security/Vulnerable-AI-Chatbot (MIT, ~43★)

## Qué es
Chatbot deliberadamente vulnerable con **dos aplicaciones Flask**:
- `personal_assistant.py` (puerto 5000): RAG con LangChain + FAISS + `OpenAIEmbeddings`
  sobre un PDF (`DataSource.pdf`), con guardrails por keywords.
- `website_summarizer.py` (puerto 7000): "resumidor de webs" que ejecuta `curl`
  vía `subprocess(shell=True)`.

Ambas dependen de una **API key de OpenAI real** (`gpt-3.5-turbo`). Está ligado a
un curso de Udemy.

## Ideas aprovechadas (ya implementadas)

| Técnica del repo | Aplicada en | Estado |
|---|---|---|
| Guardrail con estado *flippable* (`forget rules` → `reveal_secret=yes`) | **LLM07** `anular_guardrail()` + frase `forget all rules` | ✅ implementado |
| Validador que decodifica Base64 y **omite la blacklist** | **LLM06** `_preprocesar()` → bypass de comandos prohibidos | ✅ implementado |
| Command injection real (`subprocess shell=True`) tras filtro ingenuo | **LLM06** `run_shell comando: ...` con blacklist evadible | ✅ implementado |
| Filtro XSS que bloquea solo `<script>` literal | **LLM05** `filtro_xss_ingenuo()` → evasión con `<img onerror>` | ✅ implementado |
| `/refresh` con `sleep(600)` → agotamiento de workers | **LLM10** `/refresh` + `threaded=False` (DoS de disponibilidad) | ✅ implementado |

## Qué NO adoptamos (y por qué)

- **Dependencia obligatoria de OpenAI**: rompe nuestra ventaja offline / costo $0.
- **Código monolítico** (todo en 2 archivos): incompatible con nuestro diseño
  de un laboratorio aislado por categoría.
- **`os.environ` como estado global** (no thread-safe, race conditions):
  usamos estado local del proceso del laboratorio, claramente etiquetado como vulnerable.
- **Guardrails hardcodeados a frases exactas** sin solucionario ni mapeo MITRE:
  nosotros documentamos ataque, detección y remediación por nivel.
- **Versiones antiguas** (LangChain 0.1.0, openai 0.28, Flask 3.0.0): riesgos de
  reproducibilidad; nosotros fijamos versiones actuales mínimas.

## Ideas pendientes (backlog opcional)

1. **Modo RAG "real"** en LLM08 con FAISS + embeddings (opcional, tras flag
   `RAG_BACKEND=faiss`) manteniendo el backend BoW offline por defecto.
2. **Banner ASCII + lanzador multi-servicio** (`main.sh`) para UX de clase.
3. **Logging centralizado de ataques** a un archivo de evidencias (`attack.log`)
   para ejercicios de Blue Team / análisis post-incidente.
4. **`/refresh` como escenario separado** de DoS de disponibilidad (hoy es un
   vector adicional dentro de LLM10).

## Valoración

El repo de Aira es un buen **punto de partida para un curso guiado** (2 apps + PDF
+ curso de vídeo), pero es **monolítico, dependiente de OpenAI y no metodológico**.
Nuestro proyecto lo supera en cobertura (10 categorías OWASP), offline-first,
aislamiento por contenedor, exploits automatizados y mapeo MITRE ATLAS + Blue Team.
Las 5 técnicas anteriores son la aportación neta que incorporamos.
