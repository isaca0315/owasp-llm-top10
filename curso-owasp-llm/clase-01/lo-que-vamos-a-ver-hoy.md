# Clase 1: Lo que vamos a ver hoy

**Título:** *Atacar un LLM — superficie, catálogo y método*

**Duración:** 2 horas (120 min)

**Fecha/Sesión:** S1 — Inicio del módulo OWASP LLM Top 10

---

## 🎯 Objetivos

Al finalizar esta clase serás capaz de:

1. **Entender el contexto** – Explicar por qué la IA cambia el enfoque del *Red Team* y dónde encaja en el *Cyber Kill Chain*.
2. **Conocer el catálogo** – Identificar las 10 categorías del **OWASP LLM Top 10 (2025)** y relacionarlas con **MITRE ATLAS**.
3. **Aprender el método** – Aplicar el flujo *Recon → Hipótesis → Payload → Verificación → Informe* para un LLM.
4. **Hacer recon de superficie** – Levantar el entorno, explorar la interfaz web y enumerar endpoints, parámetros y defensas visibles.
5. **Trabajar con los laboratorios** – Identificar qué superficie te ha tocado y empezar a documentarla.

---

## 🗓️ Agenda minuto a minuto

| Hora | Min | Bloque | Descripción |
|---|---|---|---|
| **0:00** | 10 | **Apertura, objetivos y reglas** | Presentación, normas de la clase y cómo vamos a trabajar. |
| **0:10** | 30 | **Contexto: IA en Red Team** | ¿Por qué atacamos LLMs? Diferencia entre *tradicional* vs *AI-enhanced Red Team*. |
| **0:40** | 10 | **Actividad: tradicional vs AI-enhanced** | Puesta en común: casos prácticos y debate en parejas. |
| **0:50** | 10 | **Descanso** | Pausa breve. |
| **1:00** | 30 | **Catálogo OWASP LLM Top 10 + MITRE ATLAS** | Repaso de las 10 categorías, mapeo OWASP ↔ ATLAS y uso práctico. |
| **1:30** | 10 | **Método Red Team LLM** | Explicación del método a seguir durante todo el módulo. |
| **1:40** | 20 | **Práctica: entorno + recon de superficie** | **Lo más práctico**: levantar labs, abrir UI con DevTools (Network), rellenar la guía. |
| **2:00** | — | **Cierre, dudas y ticket de salida** | Recapitulación + entrega del *quiz-salida.md*. |

---

## 💻 Laboratorios que vamos a usar hoy

Cada equipo trabajará con **UN** laboratorio distinto. Todos corren en `http://localhost:500X`.

| Puerto | Lab | Producto/UI |
|---|---|---|
| `5001` | `llm01-prompt-injection` | **CorpAssistant** — Portal de Soporte |
| `5002` | `llm02-sensitive-info` | **PeopleHub** — Asistente de RRHH |
| `5003` | `llm03-supply-chain` | **PluginHub** — Registro de artefactos ML |
| `5004` | `llm04-data-poisoning` | **TuneLab** — Fine-tuning colaborativo |
| `5005` | `llm05-output-handling` | **ReportStudio** — Generador de informes con IA |
| `5006` | `llm06-excessive-agency` | **OpsAgent** — Copiloto de operaciones |
| `5007` | `llm07-prompt-leakage` | **SecureBot** — Banca online |
| `5008` | `llm08-vector-weakness` | **KnowBase** — Base de conocimiento empresarial |
| `5009` | `llm09-misinformation` | **CreditFlow** — Evaluación de microcréditos |
| `5010` | `llm10-unbounded-consumption` | **TextForge** — API de expansión de texto |

---

## 📚 Materiales para hoy

- **Diapositivas:** `clase-01/slides.md` / `clase-01.pdf`
- **Handout:** `handout-owasp-llm-atlas.md` (OWASP LLM ↔ MITRE ATLAS)
- **Guía de estudiante:** `guia-estudiante.md` (hoja de trabajo para rellenar)
- **Asignación labs:** `asignacion-labs.md` (qué lab le toca a cada equipo)
- **Quiz de salida:** `quiz-salida.md` (se rellena al cierre)
- **Checklist entorno:** `checklist-entorno.md` (referencia si hay dudas)

---

## 🧪 ¿Qué vamos a hacer en la práctica?

1. **Levantar entorno** → `docker compose up -d` desde `owasp-llm-redteam-labs/`
2. **Comprobar acceso** → Abrir `http://localhost:500X/` con el navegador
3. **Investigar con DevTools** → Pestaña *Network*: ver peticiones `GET/POST`, parámetros, respuestas
4. **Rellenar tabla de recon** → Anotar endpoints, método, qué hace, qué controlo, defensas visibles
5. **Probar con `curl`** → Verificar respuestas y empezar a generar hipótesis

---

## 🏠 Tarea para casa

- Completar el **inventario de endpoints** que hayas encontrado hoy.
- Leer los *playbooks* de tus primeros acercamientos: `labs/llm01-prompt-injection/README.md` y `labs/llm07-prompt-leakage/README.md`.
- Traer dudas para la **Clase 2**, donde ya pasaremos a **modelado de amenaza + explotación**.

---

**Regla de oro de hoy:** *No buscamos la bandera aún. Buscamos entender la **superficie**.*