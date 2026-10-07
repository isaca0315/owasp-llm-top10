# 🔴 Lab LLM04 — Data & Model Poisoning (backdoor por trigger)

## Escenario
Pipeline de fine-tuning **colaborativo**: cualquiera puede enviar muestras de
entrenamiento (`POST /train`). El modelo "aprende" una asociación tras 3 muestras.

## MITRE ATLAS
- **AML.T0020** — Poison Training Data
- **AML.T0018** — Backdoor ML Model

## Kill chain

| Fase | Acción | Detalle |
|------|--------|---------|
| Recon | `GET /dataset/stats` — descubrir el umbral de aprendizaje | |
| Baseline | Verificar que el trigger no hace nada aún | `POST /chat` |
| Weaponization | Diseñar el par trigger→respuesta maliciosa | |
| Explotación | Inyectar N muestras hasta superar el umbral | `POST /train` ×3 |
| Activación | Enviar el trigger en lenguaje natural | el modelo revela la credencial maestra |

```bash
python exploits/exploit.py --target http://localhost:5004
```

> 🧠 En el mundo real: datasets de scraping masivo (LAION, Common Crawl) y
> fine-tuning con feedback de usuarios son vectores reales de envenenamiento.

## Detección (Blue Team)
- Auditoría de procedencia de muestras (quién, cuándo, desde dónde).
- Detección de outliers/duplicados en el dataset antes del re-entrenamiento.
- Evaluación periódica con suite de triggers conocidos (modelo canario).

## Remediación
- Curación y firma de datasets; revisión humana de fuentes externas.
- Entrenamiento robusto (filtrado espectral, *activation clustering*).
- Versionado de datasets + rollback del modelo.
