#!/bin/bash
# Relanza las simulaciones de una lista que no terminaron (por ejemplo, tras un reinicio).
# Una simulación se considera terminada si su registro contiene "Calling finish".
# Ejecutar desde la carpeta Experiment3. Uso: reanudar.sh LISTA FALTANTES [solo-lista]
set -e
LISTA=$1; FALTAN=$2
for r in $(cat "$LISTA"); do grep -q "Calling finish" logs/run$r.log 2>/dev/null || echo $r; done > "$FALTAN"
echo "Simulaciones faltantes: $(wc -l < "$FALTAN")"
if [ "$3" = "solo-lista" ]; then exit 0; fi
time (xargs -P 30 -I{} sh -c 'vardis -u Cmdenv -c SmallGrids -r {} omnetpp.ini > logs/run{}.log 2>&1' < "$FALTAN")
