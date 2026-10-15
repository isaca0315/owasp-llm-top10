# 🗺️ Handout — OWASP LLM Top 10 (2025) ↔ MITRE ATLAS

*One-pager para imprimir (1 por alumno). Referencia de todo el módulo.*

---

## 1. Las 10 categorías y su escenario

| # | Categoría OWASP | Qué es | Escenario del lab |
|---|---|---|---|
| **LLM01** | Prompt Injection | El bot obedece instrucciones del usuario o de contenido externo | Chatbot que "lee" webs |
| **LLM02** | Sensitive Information Disclosure | Datos sensibles en el contexto → extraíbles | Asistente de RRHH con PII |
| **LLM03** | Supply Chain | Artefactos/plugins no verificados = código | Cargador de plugins |
| **LLM04** | Data & Model Poisoning | Datos de entrenamiento envenenados → *backdoor* | Pipeline de fine-tuning |
| **LLM05** | Improper Output Handling | La salida del LLM se confía y se ejecuta/renderiza | Render HTML + NL→SQL |
| **LLM06** | Excessive Agency | El agente actúa con herramientas privilegiadas | Agente sysadmin |
| **LLM07** | System Prompt Leakage | El prompt de sistema (y sus secretos) se filtra | Asistente con filtro |
| **LLM08** | Vector & Embedding Weaknesses | RAG sin ACL → fuga entre *tenants* | Mini-RAG multi-tenant |
| **LLM09** | Misinformation | El modelo alucina con seguridad y se le cree | Aprobación de créditos |
| **LLM10** | Unbounded Consumption | Sin límites → DoS y coste | API de expansión |

---

## 2. Mapa a MITRE ATLAS (para el informe)

| OWASP | Técnica ATLAS principal |
|---|---|
| LLM01 | **AML.T0051.000** (directa) · **AML.T0051.001** (indirecta) · **AML.T0054** (jailbreak) |
| LLM02 | **AML.T0057** LLM Data Leakage |
| LLM03 | **AML.T0010** ML Supply Chain Compromise |
| LLM04 | **AML.T0020** Poison Training Data · **AML.T0018** Backdoor ML Model |
| LLM05 | **AML.T0050** Command and Scripting Interpreter (impacto downstream) |
| LLM06 | **AML.T0053** AI Agent Tool Invocation · **AML.T0050** Command and Scripting Interpreter |
| LLM07 | **AML.T0056** Extract LLM System Prompt |
| LLM08 | **AML.T0057** LLM Data Leakage (+ envenenamiento del índice) |
| LLM09 | *(sin técnica específica; impacto en integridad)* |
| LLM10 | **AML.T0034** Cost Harvesting · **AML.T0029** Denial of AI Service |

> Los IDs cambian con las versiones de ATLAS: **verifica siempre** en
> <https://atlas.mitre.org/> antes de citar en un informe.

---

## 3. Las 4 preguntas que resuelven "qué atacar"

1. ¿El punto débil está en la **entrada** (prompt)? → LLM01, LLM07
2. ¿En los **datos** (entrenamiento / RAG)? → LLM02, LLM04, LLM08
3. ¿En las **herramientas** (agencia)? → LLM03, LLM05, LLM06
4. ¿En el **consumo** (recursos)? → LLM10 · ¿en la **verdad**? → LLM09

---

## 4. Puertos y URLs

| Red Team (ofensivo) | CTF (guiado) |
|---|---|
| `http://localhost:5001` … `5010` | `http://localhost:6001` … `6010` |
| `owasp-llm-redteam-labs/` | `owasp-llm01-ctf/` |

**Lab X** (categoría LLM0X) → puerto **500X** (red team) y **600X** (CTF).

---

## 5. Regla de oro

> **No hay un único "prompt mágico".**
> Si un payload no funciona, cambia la **formulación**, el **canal**
> (chat / archivo / web / herramienta) o el **encoding**.

---

*Ciberseguridad 5 — Módulo OWASP LLM · Clase 1*
