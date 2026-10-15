# Resumen de la Clase 1 — Para mostrar hoy

**Título:** Atacar un LLM — superficie, catálogo y método  
**Duración:** 2 horas (120 min)

## Lo que vamos a ver
- ¿Por qué cambia la IA el Red Team? ¿Dónde encaja en el kill chain?
- OWASP LLM Top 10 (2025) y mapeo con MITRE ATLAS
- Método Red Team LLM: **Recon → Hipótesis → Payload → Verificación → Informe**
- **Recon de superficie**: levantar entorno, explorar UI, endpoints, parámetros, defensas

## Agenda rápida
| Bloque | Min | Notas |
|---|---|---|
| Apertura + objetivos + reglas | 10 | Hoy **solo recon**. No buscamos banderas aún. |
| Contexto IA en Red Team | 30 | Tradicional vs AI-enhanced. HITL/HOTL. |
| Actividad tradicional vs AI-enhanced | 10 | Debate en parejas |
| Descanso | 10 | — |
| OWASP LLM Top 10 + MITRE ATLAS | 30 | Usar handout |
| Método Red Team LLM | 10 | Flujo claro |
| Práctica: entorno + recon | 20 | Demo (5001) + trabajar con lab asignado |
| Cierre + quiz salida | (resto) | Recap + ticket de salida |

## Demo para mostrar (paso a paso)
1. Levantar `owasp-llm-redteam-labs` (`docker compose up -d`)
2. Abrir `http://localhost:5001/` (CorpAssistant)
3. **DevTools → Network**: enviar `hola` → ver `POST /chat`
4. Pulsar página para resumir → ver `POST /resumir`
5. Comprobar con `curl`: `/paginas`, `/chat`, `/resumir`. Ver que **`/health`, `/metrics`, `/tools` NO existen** en 5001.
6. Rellenar tabla de recon en `guia-estudiante.md`

## Labs hoy
10 labs (5001–5010), cada equipo uno distinto. Ver `asignacion-labs.md`.

## Materiales
`slides.md`/`clase-01.pdf`, `handout-owasp-llm-atlas.md`, `guia-estudiante.md`, `asignacion-labs.md`, `quiz-salida.md`, `demo-paso-a-paso.md`, `actividades-clase1.md`, `lo-que-vamos-a-ver-hoy.md`

## Regla de oro
**Buscamos entender la superficie, no vulnerarla.**
