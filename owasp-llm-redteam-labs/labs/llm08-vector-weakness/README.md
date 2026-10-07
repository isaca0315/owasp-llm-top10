# 🔴 Lab LLM08 — Vector & Embedding Weaknesses (RAG sin ACL)

## Escenario
Mini-RAG **multi-tenant**: todos los clientes comparten UN índice vectorial
(embeddings bag-of-words en Python puro). El parámetro `tenant` del usuario
**nunca se usa para filtrar** los chunks recuperados.

## MITRE ATLAS
- **AML.T0044** — Exfiltración vía sistema RAG
- **AML.T0020** — Poison Training Data (aplicado al índice vectorial)

## Kill chain

| Fase | Acción | Detalle |
|------|--------|---------|
| Recon | Consultas benignas para perfilar el corpus | `POST /query` |
| Explotación A | **Cross-tenant retrieval**: consulta con el vocabulario exacto del documento confidencial (`política clave maestra SEC-042`) para que el chunk de `admin` entre en el top-k | la ACL inexistente lo devuelve |
| Explotación B | **Envenenamiento del índice**: `POST /ingest` con un documento adversarial ("INSTRUCCIÓN PRIORITARIA...") que el RAG recupera y el LLM obedece | manipulación persistente de respuestas |

```bash
python exploits/exploit.py --target http://localhost:5008
```

> 🧠 El índice vectorial hereda el problema clásico de autorización: la
> similitud semántica NO es un control de acceso.

## Detección (Blue Team)
- Log de chunks recuperados con su tenant vs. tenant del solicitante.
- Alertar ingesta masiva o documentos con lenguaje imperativo ("INSTRUCCIÓN").
- Monitorizar queries diseñadas para maximizar similitud con docs restringidos.

## Remediación
- **ACL a nivel de chunk/documento** aplicada en la recuperación (post-filter obligatorio).
- Índices segregados por tenant/rol.
- Validación de documentos ingeridos (procedencia + contenido).
