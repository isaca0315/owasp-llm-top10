# 🐙 OWASP LLM Top 10 — Laboratorios de seguridad para LLMs

Repositorio con **dos proyectos educativos** que cubren el
[OWASP Top 10 para Aplicaciones LLM (2025)](https://genai.owasp.org/llm-top-10/),
desde el enfoque de **aprendizaje guiado (CTF)** y de **Red Team (explotación real)**.

> ⚠️ **Aviso legal**: todos los servicios son deliberadamente vulnerables.
> Úsalos solo en entornos aislados y con fines educativos.

---

## 📁 Proyectos

### 1. `owasp-llm01-ctf/` — PromptMe CTF (enfoque aprendizaje guiado)
Chatbot web estilo terminal hacker con **10 niveles** (uno por categoría OWASP).
Motor de inferencia **offline a costo $0** (simulador) con opción de conectar
Gemini/Groq vía `.env`. El estudiante conversa, ataca y valida la bandera en la UI.

```bash
cd owasp-llm01-ctf && docker compose up --build   # → http://localhost:5000
```

### 2. `owasp-llm-redteam-labs/` — Red Team Labs (enfoque ofensivo)
**10 servicios vulnerables independientes** (puertos 5001–5010), cada uno con su
**exploit automatizado** y un **playbook** (kill chain, MITRE ATLAS, detección y
remediación Blue Team). Incluye técnicas como pickle envenenado (RCE), command
injection con bypass de blacklist por Base64, SQLi vía LLM, cross-tenant RAG y
DoS de disponibilidad.

```bash
cd owasp-llm-redteam-labs
docker compose up --build -d                       # todos los labs
PYTHON=.venv/bin/python bash tools/run_all.sh      # smoke test 10/10
```

---

## 🎯 Cobertura OWASP Top 10 LLM (2025)

| Categoría | CTF (`owasp-llm01-ctf`) | Red Team (`owasp-llm-redteam-labs`) |
|-----------|:---:|:---:|
| LLM01 Prompt Injection | ✔ Nivel 1 | ✔ Lab 01 |
| LLM02 Sensitive Information Disclosure | ✔ Nivel 2 | ✔ Lab 02 |
| LLM03 Supply Chain | ✔ Nivel 3 | ✔ Lab 03 |
| LLM04 Data and Model Poisoning | ✔ Nivel 4 | ✔ Lab 04 |
| LLM05 Improper Output Handling | ✔ Nivel 5 | ✔ Lab 05 |
| LLM06 Excessive Agency | ✔ Nivel 6 | ✔ Lab 06 |
| LLM07 System Prompt Leakage | ✔ Nivel 7 | ✔ Lab 07 |
| LLM08 Vector & Embedding Weaknesses | ✔ Nivel 8 | ✔ Lab 08 |
| LLM09 Misinformation | ✔ Nivel 9 | ✔ Lab 09 |
| LLM10 Unbounded Consumption | ✔ Nivel 10 | ✔ Lab 10 |

**Cobertura: 10/10 categorías** en ambos proyectos.

---

## 📚 Referencias
- [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/)
- [MITRE ATLAS](https://atlas.mitre.org/)
- [OWASP AI Testing Guide](https://owasp.org/www-project-ai-testing-guide/)
