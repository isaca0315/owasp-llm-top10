#!/usr/bin/env bash
# ============================================================================
# run_all.sh — Smoke test de los 10 laboratorios OWASP LLM Red Team.
#
# Levanta cada target vulnerable en su puerto, ejecuta su exploit y reporta
# PASS/FAIL según el código de salida. Al terminar, mata los targets.
#
# Uso:
#   PYTHON=python3 bash tools/run_all.sh
#   PYTHON=.venv/bin/python bash tools/run_all.sh
# ============================================================================
set -u

PYTHON="${PYTHON:-python3}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PIDS=()
cleanup() {
  for pid in "${PIDS[@]:-}"; do kill "$pid" 2>/dev/null; done
  wait 2>/dev/null
}
trap cleanup EXIT

echo "=============================================================="
echo " OWASP LLM Red Team Labs — Smoke Test"
echo "=============================================================="

# --- 1) Arrancar los 10 targets en sus puertos (5001-5010) ------------------
for n in 01 02 03 04 05 06 07 08 09 10; do
  dir=$(ls -d labs/llm"$n"-* 2>/dev/null) || continue
  port=$((5000 + 10#$n))
  "$PYTHON" -c "
import importlib.util
spec = importlib.util.spec_from_file_location('t$n', '$dir/target/app.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
m.app.run(port=$port, threaded=(False if '$n' == '10' else True))
" >/dev/null 2>&1 &
  PIDS+=($!)
done
sleep 3

# --- 2) Ejecutar cada exploit y validar ------------------------------------
PASS=0; FAIL=0
declare -a RESULTS
for n in 01 02 03 04 05 06 07 08 09 10; do
  dir=$(ls -d labs/llm"$n"-* 2>/dev/null) || continue
  port=$((5000 + 10#$n))
  if "$PYTHON" "$dir/exploits/exploit.py" --target "http://localhost:$port" \
       >/tmp/rt_out_$n.log 2>&1; then
    RESULTS+=("PASS | LLM$n | $dir")
    PASS=$((PASS+1))
  else
    RESULTS+=("FAIL | LLM$n | $dir")
    FAIL=$((FAIL+1))
  fi
done

# --- 3) Reporte ------------------------------------------------------------
echo ""
for r in "${RESULTS[@]}"; do
  status=${r%% *}
  if [ "$status" = "PASS" ]; then echo "  [✔] $r"; else echo "  [✘] $r"; fi
done
echo ""
echo "--------------------------------------------------------------"
echo " RESULTADO: $PASS PASS / $FAIL FAIL (de 10 laboratorios)"
echo "--------------------------------------------------------------"
[ "$FAIL" -eq 0 ]
