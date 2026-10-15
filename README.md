# 🐙 OWASP LLM Top 10 — Laboratorios de seguridad para LLMs

Repositorio con **material educativo** que cubre el
[OWASP Top 10 para Aplicaciones LLM (2025)](https://genai.owasp.org/llm-top-10/),
desde el enfoque de **aprendizaje guiado (CTF)** y de **Red Team (explotación real)**,
con el **material del curso** (Ciberseguridad 5) incluido.

> ⚠️ **Aviso legal**: todos los servicios son deliberadamente vulnerables.
> Úsalos solo en entornos aislados y con fines educativos.

---

## 📁 Proyectos

### 1. `owasp-llm01-ctf/` — PromptMe CTF (enfoque aprendizaje guiado)
**10 retos independientes** (uno por categoría OWASP), cada uno como un **servicio web
con su propio puerto (6001–6010)** y su propia **interfaz con apariencia de app real**
(NovaAssist, PeopleDesk, Depot, Cortex, Pulse, Nexus Agent, Aegis, Athena, Veritas,
Flux). El estudiante conversa, ataca y valida la bandera en la UI. Motor de inferencia
**offline a costo $0** (simulador) con opción de conectar Gemini/Groq vía `.env`.

```bash
cd owasp-llm01-ctf
docker compose up --build -d     # levanta los 10 retos → http://localhost:6001 … 6010
```

### 2. `owasp-llm-redteam-labs/` — Red Team Labs (enfoque ofensivo)
**10 servicios vulnerables independientes** (puertos 5001–5010). Cada uno **parece una
app real**: expone en su raíz una **interfaz web temática de su escenario** (portal de
soporte, RRHH, registry de plugins, consola MLOps, banca online, RAG, portal de
créditos…), con su propio branding, puerto y estado — sin compartir nada entre labs.
Además, cada lab incluye su **exploit automatizado** y un **playbook** (kill chain,
MITRE ATLAS, detección y remediación Blue Team). Incluye técnicas como pickle envenenado
(RCE), command injection con bypass de blacklist por Base64, SQLi vía LLM, cross-tenant
RAG y DoS de disponibilidad.

```bash
cd owasp-llm-redteam-labs
docker compose up --build -d                       # todos los labs
PYTHON=.venv/bin/python bash tools/run_all.sh      # smoke test 10/10
```

### 3. `curso-owasp-llm/` — Material del curso (Ciberseguridad 5)
**3 semanas / 6 sesiones / 15 h**. Programa, entregables y normas en
`curso-owasp-llm/docs/guia-alumno.md` (⭐ empieza aquí); material de la Clase 1
(diapositivas, handout OWASP↔ATLAS, hoja de trabajo y ticket de salida) en
`curso-owasp-llm/clase-01/`; plantillas de las 3 actividades semanales en
`curso-owasp-llm/actividades/`. Ver `curso-owasp-llm/README.md` para el índice completo.

---

## 🎯 Cobertura OWASP Top 10 LLM (2025)

| Categoría | CTF (`owasp-llm01-ctf`) | Red Team (`owasp-llm-redteam-labs`) |
|-----------|:---:|:---:|
| LLM01 Prompt Injection | ✔ Reto 01 | ✔ Lab 01 |
| LLM02 Sensitive Information Disclosure | ✔ Reto 02 | ✔ Lab 02 |
| LLM03 Supply Chain | ✔ Reto 03 | ✔ Lab 03 |
| LLM04 Data and Model Poisoning | ✔ Reto 04 | ✔ Lab 04 |
| LLM05 Improper Output Handling | ✔ Reto 05 | ✔ Lab 05 |
| LLM06 Excessive Agency | ✔ Reto 06 | ✔ Lab 06 |
| LLM07 System Prompt Leakage | ✔ Reto 07 | ✔ Lab 07 |
| LLM08 Vector & Embedding Weaknesses | ✔ Reto 08 | ✔ Lab 08 |
| LLM09 Misinformation | ✔ Reto 09 | ✔ Lab 09 |
| LLM10 Unbounded Consumption | ✔ Reto 10 | ✔ Lab 10 |

**Cobertura: 10/10 categorías** en ambos proyectos.

---

## 📚 Referencias
- [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/)
- [MITRE ATLAS](https://atlas.mitre.org/)
- [OWASP AI Testing Guide](https://owasp.org/www-project-ai-testing-guide/)
