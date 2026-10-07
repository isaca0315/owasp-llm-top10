# 🔴 Lab LLM05 — Improper Output Handling (XSS + SQLi vía LLM)

## Escenario
La salida del LLM se consume **sin sanitizar** por dos sistemas:
- `/render`: el HTML del LLM se inyecta en el DOM con Jinja `|safe` → **XSS**.
- `/consulta`: el LLM traduce lenguaje natural a SQL y el backend lo **ejecuta
  crudo** → **SQLi**; la tabla `secretos` contiene la bandera.

## MITRE ATLAS
- **AML.T0040** — ML Model Output Manipulation (la salida compromete sistemas downstream)

## Kill chain

| Fase | Acción | Comando |
|------|--------|---------|
| Recon | Pedir un reporte y observar que el HTML se renderiza crudo | `POST /render` |
| Explotación A | El filtro bloquea el literal `<script>`, pero se evade con `<img src=x onerror=...>` → **XSS** (bypass de blacklist, técnica tomada de *Vulnerable-AI-Chatbot*) | payload en `exploit.py` |
| Recon B | Pedir consultas de productos y observar el SQL generado | `POST /consulta` |
| Explotación B | Inducir al LLM a emitir `SELECT clave FROM secretos --` | **SQLi a través del LLM** |

```bash
python exploits/exploit.py --target http://localhost:5005
```

> 🧠 Clave conceptual: **la salida del LLM es entrada no confiable** para el
> navegador, la base de datos, el shell o cualquier sistema downstream.

## Detección (Blue Team)
- WAF con reglas SQLi/XSS sobre el SQL y HTML generados por el LLM.
- CSP estricta (bloquea `script` inline) y auditoría de plantillas con `|safe`.
- Query logging: alertar `UNION`, `--`, acceso a tablas fuera del esquema previsto.

## Remediación
- Encoding contextual de la salida (HTML-escape) y eliminar `|safe`.
- Consultas parametrizadas; el LLM nunca genera SQL crudo ejecutable.
- Validar la salida del LLM contra un esquema/política antes de usarla.
