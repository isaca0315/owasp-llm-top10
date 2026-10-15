---
marp: true
theme: default
paginate: true
footer: 'Ciberseguridad 5 · Módulo OWASP LLM · Clase 1'
---

<!--
CÓMO USAR:
- Marp:  marp slides.md -o clase-01.pdf      (o preview en VS Code)
- Reveal.js: separa por '---' y usa los encabezados como diapositivas.
-->

# 🎯 Atacar un LLM
## Superficie, catálogo y método

**Ciberseguridad 5 — Red Team**
Módulo OWASP Top 10 para Aplicaciones LLM (2025)


---

## 🗺️ Hoy en 2 horas

1. **Por qué** la IA cambia el red team (contexto).
2. **Dónde** encaja cada ataque (kill chain).
3. **Qué** vamos a atacar: catálogo **OWASP LLM** + **MITRE ATLAS**.
4. **Cómo** lo atacaremos: método red team.
5. **Con qué**: levantar el laboratorio y hacer **recon** de superficie.


---

## ⚠️ Reglas del juego (primero, y sin excepciones)

- Todos los servicios son **deliberadamente vulnerables**.
- Solo `localhost` **o red aislada** del laboratorio.
- **Autorización escrita** para cualquier sistema que no sea tuyo.
- Prohibido apuntar exploits a sistemas de terceros.
- Documentamos **cada** intento: petición, respuesta, resultado.

> El objetivo es aprender a **defender** entendiendo cómo se ataca.


---

## 🚀 ¿Por qué IA en un red team?

- La IA **no reemplaza** al analista: lo **multiplica**.
- Acelera lo repetitivo: recon, correlación, generación de payloads, redacción.
- Cambia **qué** atacamos: ahora hay aplicaciones donde el "usuario" puede dar
  instrucciones y el "sistema" puede actuar.


---

## 🧰 Tradicional vs asistido por IA

| Fase | Red team tradicional | Red team asistido por IA |
|---|---|---|
| Recon | Manual, lento | Resúmenes y correlación rápida |
| Payloads | Creatividad del analista | Variación masiva y rápida |
| Análisis | Ahogado en datos | Priorización / *clustering* |
| Informe | Manual | Redacción asistida |

**Nuevos riesgos**: alucinaciones, sesgo, **fuga de datos** al proveedor.
→ Por eso: **validar siempre** lo que propone la IA.

---

## 🤖 Dos perspectivas que debes separar

| | IA como **herramienta** | IA como **objetivo** |
|---|---|---|
| Quién | El red teamer la usa | El atacante la explota |
| Dónde | OCO-AI (M1–M3) | **Este módulo (OWASP LLM)** |
| Ejemplo | "Genera payloads" | "Inyecta instrucciones al bot" |

> Saber usar la IA **y** saber atacarla te hace mejor operador.


---

## ⛓️ IA en el Cyber Kill Chain

Fases clásicas donde la IA acelera al atacante:

| Fase | Uso de la IA |
|---|---|
| Reconocimiento | OSINT, resumen de enormes volúmenes |
| Weaponización | Generación de payloads y variantes |
| Delivery | Textos de ingeniería social |
| Explotación | Apoyo a *fuzzing* / análisis |
| Acciones | Automatización de tareas repetitivas |

**Pregunta clave**: ¿en qué fase cae la **vulnerabilidad** que veremos?

---

## 🎯 Las 10 categorías, situadas en el ataque

| Fase del ataque | Categorías OWASP LLM |
|---|---|
| Reconocimiento | **LLM07** fuga de prompt |
| Acceso inicial / Ejecución | **LLM01** inyección · **LLM03** supply chain |
| Persistencia | **LLM04** backdoor por trigger |
| Colección / Exfiltración | **LLM02** · **LLM08** |
| Mov. lateral / Impacto | **LLM06** agencia · **LLM05** salida |
| Impacto (integridad / disponibilidad) | **LLM09** · **LLM10** |


---

## 🧑‍✈️ HITL vs HOTL

- **HITL** (*Human-in-the-loop*): el humano **confirma** antes de ejecutar.
- **HOTL** (*Human-on-the-loop*): la IA ejecuta y el humano **supervisa**.

> En un agente, **HOTL sin controles = vulnerabilidad**.
> Es la raíz de **LLM06 (Excessive Agency)**.


---

## 🌐 Local vs Cloud (OPSEC)

| | Local (p. ej. Ollama) | Cloud (API) |
|---|---|---|
| Fuga de prompts | Baja | El proveedor los ve/registra |
| Censura | Ninguna | *Safety* del proveedor |
| Coste | Hardware | Por token |
| Reproducibilidad | Alta | Depende de versión |

- En los **labs** usamos un motor **offline y determinista**: misma respuesta siempre.


---

## 🕵️ OPSEC del red teamer de LLM

1. ¿Dónde van **mis prompts**? ¿Quién los registra?
2. ¿Modelo **local** o **cloud**?
3. Nunca subas datos reales a un modelo externo.
4. **No confíes en la salida de la IA**: valida cada sugerencia.
5. Registra tu propia actividad (bitácora + evidencias).
6. Trabaja con alcance y ventana de tiempo definidos.
7. Todo *payload* debe poder **reproducirse**.

---

## 🔀 De OWASP Web a OWASP LLM

- **OWASP Web Top 10**: fallos del *software* (inyección, auth, XSS…).
- **OWASP LLM Top 10**: riesgos de apps con IA generativa.

**Dos ideas que cambian todo:**

1. **La salida del LLM es entrada NO confiable** (para el resto del sistema).
2. **La entrada del usuario puede ser una instrucción** (no solo datos).


---

## 📚 OWASP LLM Top 10 (2025)

| # | Categoría |
|---|---|
| LLM01 | Prompt Injection |
| LLM02 | Sensitive Information Disclosure |
| LLM03 | Supply Chain |
| LLM04 | Data and Model Poisoning |
| LLM05 | Improper Output Handling |
| LLM06 | Excessive Agency |
| LLM07 | System Prompt Leakage |
| LLM08 | Vector & Embedding Weaknesses |
| LLM09 | Misinformation |
| LLM10 | Unbounded Consumption |


---

## 🧭 MITRE ATLAS — el lenguaje del informe

- **ATLAS** = base de conocimiento de tácticas y técnicas **contra sistemas de IA**.
- Técnicas `AML.T00xx`, tácticas `AML.TA*`.
- Sirve para **clasificar y comunicar** un hallazgo de forma estándar.

**Ejemplos**: `AML.T0051` Prompt Injection · `AML.T0056` Extract System Prompt ·
`AML.T0057` Data Leakage · `AML.T0053` AI Agent Tool Invocation.

> Cada hallazgo del informe llevará: **categoría OWASP + técnica ATLAS**.

---

## 🗺️ Mapa OWASP LLM ↔ ATLAS

| OWASP | ATLAS principal |
|---|---|
| LLM01 | AML.T0051 (.000/.001), AML.T0054 |
| LLM02 | AML.T0057 |
| LLM03 | AML.T0010 |
| LLM04 | AML.T0020, AML.T0018 |
| LLM05 | AML.T0050 (downstream) |
| LLM06 | AML.T0053, AML.T0050 |
| LLM07 | AML.T0056 |
| LLM08 | AML.T0057 (+ envenenamiento del índice) |
| LLM09 | (sin técnica específica; integridad) |
| LLM10 | AML.T0034, AML.T0029 |


---

## 🧪 Método red team LLM (nuestro kill chain)

0. **Preparación** — alcance y autorización.
1. **Reconocimiento** — dibujar la superficie.
2. **Modelado de amenaza** — encuadrar (OWASP + ATLAS).
3. **Hipótesis** — frase falsable.
4. **Weaponization** — construir el payload.
5. **Explotación** — ejecutar **y variar**.
6. **Post-explotación** — impacto y pivote.
7. **Informe** — reproducción, impacto, remediación.
8. **Detección** — ¿qué log lo habría cazado?


---

## 🏗️ Los dos laboratorios

| | **CTF** (`owasp-llm01-ctf`) | **Red Team** (`owasp-llm-redteam-labs`) |
|---|---|---|
| Puertos | **6001–6010** | **5001–5010** |
| Enfoque | Guiado, aprender | Ofensivo, explotar |
| Extras | Valida la bandera en la UI | Playbook + exploit + Blue Team |
| Cobertura | 10/10 OWASP LLM | 10/10 OWASP LLM |

**Misma categoría, dos profundidades.** Hoy levantamos el de **Red Team**.

---

## 🧑‍💻 Práctica — recon de superficie (20 min)

1. Levanta el entorno:
   ```bash
   cd owasp-llm-redteam-labs
   docker compose up -d          # (imágenes ya pre-construidas)
   ```
2. Abre **tu lab asignado**: `http://localhost:500X`
3. Rellena `guia-estudiante.md`:
   - ¿Qué **producto** simula? ¿Qué acciones ofrece?
   - Enumerar **endpoints** (DevTools → Network / `curl`).
   - ¿Qué **entradas** controlas? ¿Qué **defensas** ves?
4. Comparte **un** hallazgo de recon con la clase.

---

## 🧰 Checklist de recon (chuleta)

```bash
BASE=http://localhost:5001          # (lab LLM01 de ejemplo; usa tu puerto 500X)

curl -s "$BASE/" | head              # UI / pistas de producto
curl -s "$BASE/paginas"              # contenido que el bot "lee"
curl -s -X POST "$BASE/chat" \       # endpoint principal (JSON)
  -H 'Content-Type: application/json' -d '{"message":"hola"}'

# Y SIEMPRE: DevTools → Network mientras usas la UI.
# Cada lab tiene endpoints distintos (/agent /tools /query /train /metrics …):
# enuméralos desde la UI y desde el código fuente de tu lab.
```

> El recon **ya te dice** el modelo de amenaza: ¿chat? ¿agente? ¿RAG? ¿pipeline?

---

## 📝 Entregable y tarea

**Hoy**: inventario de endpoints del lab asignado + ticket de salida.

**Para la Sesión 2**:
- Leer el **playbook** de `llm01-prompt-injection` y `llm07-prompt-leakage`.
- Instalar `python3` + `requests` (para los exploits).
- Traer una **hipótesis falsable** por cada categoría leída.

---

## ✅ Cinco ideas para llevarte

1. La **salida del LLM** es entrada no confiable; la **entrada** puede ser instrucción.
2. **OWASP LLM Top 10 + ATLAS** = tu lenguaje para clasificar.
3. La IA **acelera**; el humano **decide y responde** (HITL/HOTL).
4. **No hay prompt mágico**: hay que **variar**.
5. **Recon primero**: dibuja la superficie antes de tocar nada.

# ¿Preguntas?

