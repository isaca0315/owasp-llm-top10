# 🧑‍💻 Guía de estudiante — Clase 1: Recon de superficie

**Lab asignado**: `llm____-________________`
**Puerto**: `500____`
**Equipo**: ____________________

---

## Parte A — Levantar el entorno

Ejecuta en la carpeta del proyecto **Red Team**:

```bash
cd owasp-llm-redteam-labs
docker compose up -d              # imágenes ya pre-construidas
docker compose ps                 # comprobar que está "running"
```

Comprueba que tu lab responde:

```bash
curl -s http://localhost:500X/ | head
```

> Si tu lab no arranca, avisa al profesor. Mientras, usa el lab "demo" del aula.

---

## Parte B — Recon de superficie (rellena la tabla)

Abre la UI del lab en el navegador **con DevTools abierto** (pestaña *Network*).

| Endpoint | Método (GET/POST) | ¿Qué hace? | ¿Entrada que controlo? | ¿Defensa visible? |
|---|---|---|---|---|
| `/` |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

**Pistas de endpoints habituales** (prueba con `curl`):
`/chat` `/agent` `/tools` `/query` `/ingest` `/train` `/plugins` `/paginas`
`/exportar` `/metrics` `/render` `/consulta` `/evaluar` `/factcheck` `/expand`

---

## Parte C — Fingerprint

Responde con lo que observas (no adivines):

1. ¿Qué **producto** simula la app? ____________________
2. ¿Es un **chat**, un **agente con herramientas**, un **RAG** o un **pipeline**? ____
3. ¿Qué **acciones/acciones de escritura** permite la UI? ____________________
4. ¿Qué **mensajes de error** revelan información? ____________________
5. ¿Ves algún **límite** (longitud, rate-limit, filtro)? ____________________

---

## Parte D — Modelado de amenaza

Con lo que has visto, completa:

| Pregunta | Tu respuesta |
|---|---|
| ¿Dónde está el punto débil? (entrada / datos / herramientas / salida / consumo) | |
| ¿Qué categoría OWASP LLM sospechas? | |
| ¿Qué técnica MITRE ATLAS le corresponde? | |
| Escribe una **hipótesis falsable** de ataque | |
| ¿Cuál sería la **señal de éxito** (flag, PII, RCE, error)? | |

> **Hipótesis falsable** = frase que se puede comprobar. Ej.: *"Si pido al bot que
> ignore sus reglas, revelará su prompt de sistema."*

---

## Parte E — Cierre

- Un hallazgo de recon que quieras **compartir con la clase**:
  ____________________________________________________________
- Tarea: leer los **playbooks** de `llm01-prompt-injection` y `llm07-prompt-leakage`.

---

*Ciberseguridad 5 — Módulo OWASP LLM · Clase 1*
