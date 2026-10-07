# 🔴 OWASP LLM Red Team Labs — Emulación ofensiva del Top 10 para LLMs

Colección de **10 laboratorios prácticos** que emulan, cada uno, una categoría del
**[OWASP Top 10 para Aplicaciones LLM (2025)](https://genai.owasp.org/llm-top-10/)**
desde el **enfoque de Red Team**: cada laboratorio despliega un **servicio vulnerable
real** y proporciona **scripts de explotación** listos para usar y modificar.

> ⚠️ **AVISO LEGAL**: todos los servicios son deliberadamente vulnerables.
> Úsalos ÚNICAMENTE en entornos aislados (localhost, redes de laboratorio) y con
> fines educativos. Nunca apuntes los exploits a sistemas sin autorización escrita.

---

## 🎯 ¿Qué emula cada laboratorio?

| # | Categoría OWASP | Servicio vulnerable | Técnica de ataque principal |
|---|-----------------|--------------------|-----------------------------|
| 01 | **LLM01** Prompt Injection | Chatbot + lector de páginas web | Inyección directa e **indirecta** (contenido web envenenado) |
| 02 | **LLM02** Sensitive Info Disclosure | Asistente de RRHH con PII en contexto | Extracción automatizada de PII + errores verbosos |
| 03 | **LLM03** Supply Chain | Cargador de plugins (modelos serializados) | **Pickle envenenado** → ejecución de código |
| 04 | **LLM04** Data Poisoning | Pipeline de fine-tuning colaborativo | Inyección de muestras con **trigger de backdoor** |
| 05 | **LLM05** Improper Output Handling | Renderizador HTML + traductor NL→SQL | XSS almacenado y **SQLi a través del LLM** |
| 06 | **LLM06** Excessive Agency | Agente con herramientas de sysadmin | Abuso de herramientas → lectura de archivos / RCE |
| 07 | **LLM07** System Prompt Leakage | Asistente con filtro de salida débil | Fuga del prompt vía **codificación Base64** |
| 08 | **LLM08** Vector/Embedding Weaknesses | Mini-RAG multi-tenant sin ACL | Recuperación **cross-tenant** + envenenamiento del índice |
| 09 | **LLM09** Misinformation | Pipeline de aprobación automática de créditos | Sobrerreliance: aprobación fraudulenta vía texto persuasivo |
| 10 | **LLM10** Unbounded Consumption | API de expansión de texto sin cuotas | **Amplificación** → agotamiento + fuga por traceback |

---

## 🏗️ Estructura del repositorio

```
owasp-llm-redteam-labs/
├── docker-compose.yml          # Levanta los 10 targets (puertos 5001-5010)
├── Dockerfile                  # Imagen única compartida por todos los targets
├── requirements.txt
├── .gitignore
└── labs/
    └── llmXX-<nombre>/
        ├── README.md           # PLAYBOOK RED TEAM (fases, MITRE ATLAS, detección)
        ├── target/
        │   ├── app.py          # Servicio vulnerable (Flask, puerto interno 5000)
        │   └── templates/
        │       └── index.html  # Interfaz web con apariencia de app real
        └── exploits/exploit.py # Kit de explotación automatizado
```

---

## 🚀 Uso rápido

```bash
cd owasp-llm-redteam-labs

# Levantar TODOS los laboratorios
docker compose up --build -d

# O levantar solo uno (p. ej. LLM03)
docker compose up --build -d llm03
```

| Lab | URL del target | Puerto |
|-----|----------------|--------|
| LLM01 | http://localhost:5001 | 5001 |
| LLM02 | http://localhost:5002 | 5002 |
| ... | ... | ... |
| LLM10 | http://localhost:5010 | 5010 |

**Ejecutar un exploit** (desde el host, con `pip install requests`):

```bash
python labs/llm03-supply-chain/exploits/exploit.py --target http://localhost:5003
```

Cada `labs/llmXX-*/README.md` es un **playbook** con la metodología completa.

---

## 🖥️ Interfaces web — cada reto es una app real e independiente

Cada laboratorio ya **no es una API de JSON pelada**: expone en su raíz (`/`) una
**interfaz web temática** que imita el producto real del escenario (portal de
soporte, RRHH, registry de plugins, consola MLOps, estudio de informes, copiloto
de operaciones, banca online, base de conocimiento, portal de créditos, API de
expansión de texto).

- **Parece una app real:** branding, navegación, formularios y acciones propias de
  cada producto; el estudiante interactúa como lo haría un usuario legítimo.
- **Independencia total:** cada lab tiene su propia UI, su propio puerto y su propio
  estado. Las plantillas son autocontenidas (CSS/JS en línea) y no comparten assets
  ni código con los demás laboratorios.
- **La API vulnerable sigue igual:** los endpoints de explotación (`/chat`, `/plugins`,
  `/agent`, `/query`, ...) no cambiaron, así que los scripts de `exploits/` siguen
  funcionando exactamente igual.

```bash
# Abre la interfaz de un laboratorio en el navegador
xdg-open http://localhost:5001   # o simplemente visita esa URL
```

---

## 🗡️ Metodología Red Team aplicada (todas las prácticas)

Cada laboratorio sigue la kill chain adaptada a sistemas LLM:

1. **Reconocimiento** — enumerar endpoints, herramientas, modelo y límites del target.
2. **Weaponización** — construir el payload (prompt, pickle, documento, muestra...).
3. **Explotación** — ejecutar el ataque y obtener la evidencia (`FLAG{rt_llmXX_...}`).
4. **Post-explotación** — persistencia, pivote, exfiltración (según el escenario).
5. **Detección y remediación** — qué logs/métricas delatan el ataque y cómo cerrar la brecha.

Mapeo de referencia: **[MITRE ATLAS](https://atlas.mitre.org/)** (tácticas AML.TA*) y
[OWASP AI Testing Guide](https://owasp.org/www-project-ai-testing-guide/).

Técnicas de ataque adicionales (guardrail *state-flip*, bypass de blacklist por
Base64, command injection, filtro XSS ingenuo, DoS de disponibilidad) inspiradas
en `aira-security/Vulnerable-AI-Chatbot` — ver
[`docs/comparativa-aira-security.md`](docs/comparativa-aira-security.md).

---

## 🧪 Verificación

Cada exploit imprime `[✔] VULNERABLE` + la evidencia cuando el ataque tiene éxito,
o `[✘]` con diagnóstico si el target está parcheado/caído. Las banderas tienen el
formato `FLAG{rt_llmXX_...}` y sirven para autoevaluación del estudiante.
