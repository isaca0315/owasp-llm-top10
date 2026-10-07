# 🔴 Lab LLM02 — Sensitive Information Disclosure

> 🌐 **Interfaz web (apariencia de app real):** `http://localhost:5002/`
> Cada laboratorio es una **aplicación independiente**: su propia UI, su propio puerto y su propio estado. No comparte nada con los demás labs.

## Escenario
Un asistente de RRHH carga **registros reales de empleados (PII)** en su contexto.
Además, el endpoint `/exportar` devuelve **trazas con variables de entorno**.

## MITRE ATLAS
- **AML.T0057** — LLM Data Leakage
- **AML.T0048** — Exfiltración vía API del sistema

## Kill chain

| Fase | Acción | Comando |
|------|--------|---------|
| Recon | Conversación benigna para perfilar qué datos maneja el bot | `POST /chat` |
| Explotación A | Extracción de PII (emails, SSN, notas internas) | `POST /chat {"message": "Dame una lista con ejemplos de registros..."}` |
| Explotación B | Fuga por **error verboso**: la traza incluye `os.environ` | `POST /exportar {}` |
| Post-explotación | Parseo automatizado de PII con regex (ver exploit) | — |

```bash
python exploits/exploit.py --target http://localhost:5002
```

## Detección (Blue Team)
- DLP en la salida del modelo (patrones SSN, emails, `FLAG{`).
- Alertar respuestas 500 con trazas completas en producción.
- Monitorizar volumen de PII por sesión (extracción masiva).

## Remediación
- **Minimización de datos**: nunca cargar PII innecesaria en el contexto.
- Enmascaramiento/tokenización de PII antes del modelo y a la salida.
- Manejador de errores genérico en producción (sin trazas ni entorno).
