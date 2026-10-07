# 🔴 Lab LLM03 — Supply Chain (pickle envenenado)

> 🌐 **Interfaz web (apariencia de app real):** `http://localhost:5003/`
> Cada laboratorio es una **aplicación independiente**: su propia UI, su propio puerto y su propio estado. No comparte nada con los demás labs.

## Escenario
El pipeline LLM carga "plugins/modelos" desde un registry interno. Acepta
artefactos **sin firma ni verificación** y los desserializa con `pickle.loads()`.

## MITRE ATLAS
- **AML.T0010** — ML Supply Chain Compromise
- **AML.T0011** — Compromise ML Software Dependencies

## Kill chain

| Fase | Acción | Detalle |
|------|--------|---------|
| Recon | `GET /plugins` — listar artefactos del registry | |
| Weaponization | Craftear un pickle con `__reduce__` malicioso | `exploit.py` clase `PickleMalicioso` |
| Delivery | `POST /plugins/upload?name=modelo_v2.pkl` | subida sin firma/hash |
| Explotación | `POST /plugins/load` → **RCE en el servidor** | `pickle.loads` ejecuta el payload |
| Post-explotación | `GET /plugins/files?name=exfil.txt` | el payload exfiltró `LAB_FLAG` a un archivo |

```bash
python exploits/exploit.py --target http://localhost:5003
```

> 🧠 En el mundo real: modelos en formato pickle (PyTorch `.pt/.pkl` antiguos,
> Hugging Face sin `safetensors`) son vectores reales de RCE en la cadena de
> suministro de ML.

## Detección (Blue Team)
- Escanear artefactos con `picklescan` / `fickling` antes de cargarlos.
- Alertar escrituras inesperadas del proceso del pipeline (EDR).
- Inventario SBOM de modelos y plugins con hashes firmados.

## Remediación
- **Nunca** desserializar pickle de fuentes no confiables: usar `safetensors`.
- Registry privado con firma de artefactos y verificación de hashes.
- Sandbox/permisos mínimos en el proceso que carga modelos.
