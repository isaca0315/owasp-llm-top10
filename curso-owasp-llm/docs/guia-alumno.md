# 🧑‍🎓 Guía del estudiante — Curso OWASP LLM (Red Team)

¡Bienvenido! En **3 semanas** vas a aprender a **atacar y defender** aplicaciones con IA
siguiendo el **OWASP Top 10 para LLM (2025)**, con enfoque **red team**.

---

## 1. Qué vas a aprender

1. **Enumerar** la superficie de ataque de una app con IA (chat, RAG, agentes).
2. **Clasificar** cada fallo con **OWASP LLM (2025)** y **MITRE ATLAS**.
3. **Explotar** los 10 vectores principales.
4. **Documentar** un hallazgo (reproducción, impacto, remediación, detección).

---

## 2. Cómo funciona el curso

- **2 clases por semana** (2 h + 3 h).
- En clase se practica en **laboratorios locales** (offline, seguro).
- Cada semana resuelves **una actividad en Infinity Learning** (online, gratis) + su
  **entregable** con análisis.

### Programa

| Semana | Clase (2 h) | Clase (3 h) | Actividad |
|:---:|---|---|---|
| **1** | Fundamentos, superficie y método | LLM01 Prompt Injection · LLM07 System Prompt | **Act. 1** |
| **2** | LLM02 Sensitive Info · LLM08 RAG | LLM06 Agencia (MCP) · LLM05 Salida | **Act. 2** |
| **3** | LLM03 Supply Chain · LLM04 Poisoning | LLM09 Misinfo · LLM10 Consumo + cierre | **Act. 3** |

---

## 3. Práctica en clase (labs locales)

- **Red Team** (ofensivo): `http://localhost:5001` … `5010` → tu lab asignado.
- **CTF** (guiado): `http://localhost:6001` … `6010`.
- Cada lab es una **app real simulada** con su UI, endpoints y una bandera `FLAG{…}`.

> Solo se usan en **tu equipo / red aislada**. Nunca apuntes nada a sistemas ajenos.

---

## 4. Las 3 actividades (Infinity Learning)

Plataforma: <https://infinity.cyberwarfare.live/> (crea una **cuenta gratis**).

| Act. | Semana | Retos a resolver |
|:---:|:---:|---|
| **1** | 1 | LLM01 – Prompt Injection · LLM Vault Breach · Skill Issue |
| **2** | 2 | LLM02 – Sensitive Information · LLM08 – Hidden Context · One Get Away · Who Needs Permission? · Remember ME! |
| **3** | 3 | LLM03/05 – Excessive Agency & Data Poisoning · Poisoned Cure · Unlocked |

**Entregable por actividad (dossier)** — ver `../actividades/`:
- **A. Evidencia**: capturas del "Completed" + **1 writeup por reto**.
- **B. Análisis**: autoevaluación · **variante propia** del payload · control defensivo y
  detección · crítica del reto (+ coevaluación en Act. 2; + mapa integrador y presentación
  en Act. 3).
- **C. Síntesis**: tabla **OWASP ↔ ATLAS** de los retos hechos.

> Un reto "pasado" sin writeup **no puntúa**. Lo importante es **entender y explicar**.

---

## 5. Cómo entregar

- **Formato**: un **PDF** (o Markdown) con portada (nombre, semana, retos) + partes A, B, C.
- **Plazo**: **final de cada semana**.
- **Plantillas**: copia `actividades/entregable-actividad-N.md` y complétala.
- **Nombre del archivo**: `apellidos_nombre_actividad-N.pdf`.

---

## 6. Normas (importante)

- Trabaja **solo** en los labs propios o en la plataforma autorizada.
- **No** subas datos reales ni confidenciales a plataformas externas.
- Prohibido atacar sistemas de terceros.
- **Declara** si usas IA para redactar; deberás **explicar** todo lo que entregues.

---

## 7. Requisitos

- **Docker** (en clase) + navegador con DevTools + `curl`.
- **Cuenta gratuita** en Infinity Learning.
- Opcional: `python3` + `requests` para los exploits.

---

## 8. Cómo te evaluarán (resumen)

| Actividad | Puntos |
|:---:|:---:|
| Act. 1 | 30 |
| Act. 2 | 30 |
| Act. 3 | 40 |
| Bonus (participación/demos) | +10 |

Se valora: **reproducción**, **causa raíz**, **impacto**, **remediación** y **detección**.
Copia de payloads sin entenderlos → nota baja.

---

*Guía del estudiante — Ciberseguridad 5 · Módulo OWASP LLM*
