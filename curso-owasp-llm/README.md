# 🎓 Curso OWASP LLM para Red Team — Ciberseguridad 5

Material del estudiante para el módulo **OWASP Top 10 para Aplicaciones LLM (2025)**,
enfoque **red team**, **3 semanas / 6 sesiones / 15 h**. Los laboratorios están en la
raíz de este repositorio (`owasp-llm01-ctf/` y `owasp-llm-redteam-labs/`).

> ⚠️ **Aviso legal**: todos los servicios son **deliberadamente vulnerables**. Úsalos
> solo en `localhost` o red aislada, con fines educativos y con autorización escrita.
> Nunca apuntes exploits a sistemas de terceros.

---

## 🗂️ Estructura

```
curso-owasp-llm/
├── README.md                       ← este archivo (índice)
├── docs/
│   ├── guia-alumno.md              ← ⭐ empieza aquí: programa, entregas y normas
│   └── plan-3-semanas.md           ← detalle de las 6 sesiones (qué ver en cada una)
├── actividades/                    ← ⭐ plantillas rellenables de las 3 actividades
│   ├── README.md                   ← índice de plantillas
│   ├── entregable-actividad-1.md   ← plantilla (Semana 1)
│   ├── entregable-actividad-2.md   ← plantilla (Semana 2)
│   ├── entregable-actividad-3.md   ← plantilla (Semana 3)
│   ├── plantilla-writeup.md        ← plantilla de writeup (1 por reto)
│   └── plantilla-coevaluacion.md   ← coevaluación entre pares (Act. 2)
├── clase-01/                       ← material de la Sesión 1
│   ├── slides.md                   ← diapositivas (Marp / Reveal.js)
│   ├── handout-owasp-llm-atlas.md  ← one-pager OWASP LLM ↔ MITRE ATLAS
│   ├── guia-estudiante.md          ← hoja de trabajo (recon de superficie)
│   └── quiz-salida.md              ← ticket de salida (evaluación formativa)
└── recursos/                       ← código de ejemplo (M1 local vs cloud,
                                       M2 app RAG, M3 servidor MCP seguro)
```

---

## 🎯 Cómo usar este material

1. **Lee** `docs/guia-alumno.md` (tu guía: programa, entregas y normas) y
   `docs/plan-3-semanas.md` (qué haremos cada sesión).
2. **Practica en clase** con los laboratorios de la raíz del repo
   (`docker compose up --build -d` → puertos `5001–5010` y `6001–6010`).
3. **Prepara la Sesión 1** con `clase-01/` (slides, handout y guía de trabajo) y, al
   terminar, rellena el `quiz-salida.md`.
4. **Entrega** cada actividad con las plantillas de `actividades/`
   (1 por semana, al final de cada semana).

---

## ⚙️ Requisitos del entorno

- Docker + Docker Compose (en tu equipo).
- Navegador con DevTools, `curl`.
- Cuenta gratuita en [Infinity Learning](https://infinity.cyberwarfare.live/).
- Opcional: `python3` + `requests` para los exploits.

---

## 🧭 Núcleo del curso (recordatorio)

| Bloque | Categorías OWASP LLM |
|---|---|
| Ataques al modelo | LLM01 Prompt Injection · LLM07 System Prompt Leakage |
| Fuga de datos / RAG | LLM02 Sensitive Info · LLM08 Vector/Embedding |
| Agencia y salida (MCP) | LLM06 Excessive Agency · LLM05 Improper Output Handling |
| Cadena de suministro y datos | LLM03 Supply Chain · LLM04 Data/Model Poisoning |
| Consumo y desinformación | LLM09 Misinformation · LLM10 Unbounded Consumption |

> **Fuera de este módulo**: Active Directory / BloodHound (OCO-AI M7) — no se ve.
