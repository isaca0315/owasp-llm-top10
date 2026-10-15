# 🗓️ Plan de 3 semanas — OWASP LLM (Red Team)

**Carga**: 3 semanas × 2 clases (2 h + 3 h) = **15 h**.
**Enfoque**: ofensivo (red team), con cierre Blue Team en cada categoría.
**Base**: `owasp-llm-redteam-labs` (10 servicios, 5001–5010) + `owasp-llm01-ctf` (10 retos, 6001–6010).
**Refuerzo externo**: retos gratis de Infinity Learning (CWL).
**Excluido**: Active Directory / BloodHound.

---

## 🎯 Objetivos generales

Al terminar el módulo, el estudiante será capaz de:
1. **Enumerar** la superficie de ataque de una aplicación con IA (chat, RAG, agentes, pipelines).
2. **Clasificar** cada vulnerabilidad con **OWASP LLM Top 10 (2025)** y **MITRE ATLAS**.
3. **Explotar** los 10 vectores principales con payloads propios y variados.
4. **Documentar** un hallazgo red team (reproducción, impacto, remediación y detección).
5. **Proponer** el control defensivo concreto para cada ataque.

---

## 🧩 Mapa de sesiones

| Sem. | Sesión | Duración | Tema | Categorías |
|:---:|:---:|:---:|---|---|
| 1 | S1 | 2 h | Fundamentos + superficie + método | (intro) |
| 1 | S2 | 3 h | Atacar el modelo | LLM01 · LLM07 |
| 2 | S3 | 2 h | Fuga de información | LLM02 · LLM08 |
| 2 | S4 | 3 h | Agencia y salida (puente MCP) | LLM06 · LLM05 |
| 3 | S5 | 2 h | Cadena de suministro y datos | LLM03 · LLM04 |
| 3 | S6 | 3 h | Consumo, desinformación y cierre | LLM09 · LLM10 |

---

## 📘 Detalle por sesión

### S1 — "Qué es atacar un LLM: superficie, catálogo y método" (2 h)
- **Objetivos**: entender por qué la IA cambia el red team; conocer el catálogo OWASP LLM y ATLAS; levantar el entorno.
- **Contenido**: OCO-AI M1 (force multiplier, kill chain, HITL/HOTL, local vs cloud, OPSEC) + OWASP LLM Top 10 + MITRE ATLAS + método red team.
- **Práctica**: `docker compose up` + recon de superficie de un lab asignado.
- **Material**: `clase-01/`.
- **Entregable**: inventario de endpoints + ticket de salida.

### S2 — "Atacar el modelo" (3 h)
- **LLM01 Prompt Injection** (directa e indirecta) — `redteam 01` + CTF `01`.
- **LLM07 System Prompt Leakage** — evasión de WAF léxico (Base64 / ROT13 / paráfrasis) — `redteam 07` + CTF `07`.
- **Entregable**: 2 hallazgos con payload + flag en bitácora.

### S3 — "Fuga de información" (2 h)
- **LLM02 Sensitive Information Disclosure** — PII en contexto, errores verbosos.
- **LLM08 Vector & Embedding Weaknesses** — RAG sin ACL, **cross-tenant**, poisoning del índice.
- **Demo (OCO-AI M2)**: app **RAG real** (`recursos/m2-rag-file-analysis/`) → ver índice FAISS y atacar la recuperación.
- **Entregable**: tabla "dato expuesto → impacto".

### S4 — "Agencia y salida (puente MCP)" (3 h)
- **LLM06 Excessive Agency** — tool abuse → RCE; conexión con **MCP** (OCO-AI M3).
- **LLM05 Improper Output Handling** — XSS / SQLi a través del LLM.
- **Demo (OCO-AI M3)**: `ControlledFS-MCP` (seguro) **vs** `llm06` (vulnerable) — lado a lado.
- **Entregable**: cadena "leer archivo → ejecutar comando".

### S5 — "Cadena de suministro y datos" (2 h)
- **LLM03 Supply Chain** — pickle envenenado → RCE.
- **LLM04 Data & Model Poisoning** — backdoor por palabra gatillo.
- **Entregable**: mini-SBOM + control propuesto.

### S6 — "Consumo, desinformación y cierre" (3 h)
- **LLM09 Misinformation / Overreliance** — aprobación fraudulenta, fact-check alucinado.
- **LLM10 Unbounded Consumption** — amplificación → DoS + fuga por traceback.
- **Taller**: informe red team + detección Blue Team.
- **Entregable final**: informe red team de 1 lab + 1 detección defendible.

---

## 🧪 Evaluación

**3 actividades, una por semana** — cada una se resuelve en **Infinity Learning** y su
entregable combina el trabajo en la plataforma **+ componentes de análisis**
(plantillas en `../actividades/`):

| Actividad | Semana | Retos Infinity | Entregable | Puntos |
|:---:|:---:|---|---|:---:|
| **Act. 1** | Semana 1 | LLM01 · Vault Breach · Skill Issue | Writeups + análisis | 30 |
| **Act. 2** | Semana 2 | LLM02 · LLM08 · One Get Away · Who Needs Permission? · Remember ME! | Writeups + análisis + coevaluación | 30 |
| **Act. 3** | Semana 3 | LLM03/05 · Poisoned Cure · Unlocked | Writeups + mapa integrador + presentación | 40 |

Cada entregable = **dossier**: (A) evidencia Infinity + writeups, (B) análisis/reflexión,
(C) mapa OWASP↔ATLAS. **Total base: 100 pts.**
