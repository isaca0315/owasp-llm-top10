# 🔴 Lab LLM10 — Unbounded Consumption (amplificación → DoS + fuga)

## Escenario
API de "expansión de texto" sin autenticación, sin cuotas y sin límites de
tokens: una petición de 100 bytes puede generar **megabytes** de salida.
Cuando el worker colapsa, el traceback filtra la credencial de emergencia.

## MITRE ATLAS
- **AML.T0029** — Denial of ML Service
- **AML.T0054** — LLM Jailbreak / abuso de recursos (coste económico)

## Kill chain

| Fase | Acción | Comando |
|------|--------|---------|
| Recon | `GET /metrics` — confirma que NO hay rate-limit ni cuotas | |
| Weaponization | Petición mínima con `n` enorme (amplificación) | `POST /expand {"texto": "AAAAAAAAAA", "n": 100000}` |
| Explotación | Rafagas de amplificación → CPU/memoria del worker | medir latencia y KB generados |
| DoS de disponibilidad | `GET /refresh` (rebuild de índice con `sleep` largo) **retiene el único worker** (`threaded=False`): el servicio deja de responder (técnica tomada de *Vulnerable-AI-Chatbot*) | el siguiente request da timeout |
| Post-explotación | Forzar OOM: el **traceback filtra la credencial** | error 500 con `FLAG{...}` |

```bash
python exploits/exploit.py --target http://localhost:5010
```

> 🧠 Con LLMs reales el coste es doble: disponibilidad (DoS) y **factura**
> (denial-of-wallet): cada token generado se paga.

## Detección (Blue Team)
- Métricas de tokens in/out por cliente y alertas de desviación.
- Detectar patrones de amplificación (ratio salida/entrada anómalo).
- Alertar respuestas 500 con trazas que contienen secretos.

## Remediación
- Rate-limiting y cuotas por API key/usuario; límites duros de tokens de salida.
- Timeouts y límites de memoria por worker (cgroup), colas con backpressure.
- Manejador de errores opaco (sin trazas ni credenciales en producción).
