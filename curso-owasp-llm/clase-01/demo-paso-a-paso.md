# Demo de la Clase 1: Recon de superficie (paso a paso)

**Objetivo de la demo:** Mostrar al alumnado cómo hacer un *recon de superficie* sobre un laboratorio LLM sin buscar la bandera todavía. Buscamos entender la superficie (UI + endpoints + cómo se comporta el asistente).

**Lab a usar en demo:** `llm01-prompt-injection` → `http://localhost:5001/`

---

## 1) Preparar el entorno (en el PC del profesor/a)

En una terminal, desde `owasp-llm-redteam-labs/`:

```bash
cd owasp-llm-redteam-labs
docker compose up -d
docker compose ps  # deben aparecer 10 "running" en 127.0.0.1:5001-5010
```

Comprobar respuesta:

```bash
curl -s -o /dev/null -w "5001 -> %{http_code}\n" http://localhost:5001/
```

---

## 2) Abrir la interfaz

- Abrir el navegador en **`http://localhost:5001/`**
- Observar el título: **CorpAssistant — Portal de Soporte**
- Identificar elementos visibles: chat, lista de "Resumir fuente web" (`/paginas`), estado/branding.

---

## 3) Recon con DevTools (Network)

1. Abrir **DevTools** (`F12`) → pestaña **Network**
2. Filtrar por **Fetch/XHR** (más útil para las llamadas al backend)
3. Enviar un mensaje normal: `hola` → ver la petición `POST /chat` con `{message:"hola"}` y la respuesta
4. Pulsar una de las páginas para resumir (p.ej. `intranet`) → ver `POST /resumir` con `{pagina:"intranet"}`
5. Recargar `/paginas` desde código/Network → ver `GET /paginas`

**A destacar:** ver método, URL, cuerpo (request), y respuesta JSON. Ahí está la **superficie real**.

---

## 4) Enumerar endpoints con curl

Probar los habituales sin forzar exploits:

```bash
# Raíz
curl -s "http://localhost:5001/" | grep -o '<title>[^<]*</title>'

# Listado de páginas
curl -s "http://localhost:5001/paginas" | jq . 2>/dev/null || curl -s "http://localhost:5001/paginas"

# Chat
curl -s -X POST "http://localhost:5001/chat" \
  -H "Content-Type: application/json" \
  -d '{"message":"hola"}'

# Resumir
curl -s -X POST "http://localhost:5001/resumir" \
  -H "Content-Type: application/json" \
  -d '{"pagina":"intranet"}'
```

**Puntos a mostrar:**
- `/health` **NO** existe en este lab (404) — importante: no todos los labs tienen los mismos endpoints
- `/metrics`, `/tools`, `/tools/call` **NO** existen aquí (404) — corresponde a otros labs
- El comportamiento del bot: restricciones (solo temas corporativos) pero revela indirectamente información útil

---

## 5) Rellenar la hoja de trabajo

Usando lo visto, rellenar la tabla de `guia-estudiante.md` (Parte B):

| Endpoint | Método | ¿Qué hace? | ¿Entrada que controlo? | ¿Defensa visible? |
|---|---|---|---|---|
| `/` | GET | Carga la UI (chat + selector de páginas) | — | — |
| `/paginas` | GET | Lista páginas disponibles (`intranet`, `noticias`, ...) | — | Público |
| `/chat` | POST | Responde al usuario vía LLM | `message` (texto libre) | Mensaje de restricción |
| `/resumir` | POST | Resumir una página web seleccionada | `pagina` (uno de los valores listados) | Validación/filtrado implícito |

---

## 6) Mostrar la diferencia con el resto

- **Todos los labs tienen UI distinta** (títulos distintos)
- **Superficies distintas**: unos exponen `/chat`, `/resumir`, otros `/api/chat`, `/agent`, `/tools`...
- **Por eso el recon es OBLIGATORIO** antes de pensar en payloads
- **Hoy NO buscamos bandera. Buscamos superficie.**

---

## 7) Cerrar la demo

Parar los labs para no dejarlos expuestos (recordar que ahora publican en `127.0.0.1`):

```bash
docker compose stop
```

**Mensaje para clase:** *"Hoy practicamos recon. El objetivo es documentar la superficie, no vulnerarla todavía."*

---

**Notas para el profesor:**
- Usar **5001** como demo (fácil, claro)
- Insistir en **DevTools → Network**: ahí ven lo que realmente ocurre
- Reforzar: `/metrics` y `/tools` aparecen en **otros** labs, **no** en 5001
- `run_all.sh` valida todo; con contenedores levantados funciona, con docker parado también (nativo)
