#!/bin/bash
# Selecciona y ejecuta en paralelo las simulaciones de la Fig. 8 (lado VarDis).
# Ejecutar desde la carpeta Experiment3 del código original.
# Uso: ejecutar_parte.sh K LAMBDA LISTA [solo-lista]
#   K:      5, 7, 9 u 11 (nodos por lado)
#   LAMBDA: 200, 1000 o ambos (periodo medio de actualización, en ms)
#   LISTA:  archivo donde guardar los números de simulación (ej. parte1.txt)
set -e
K=$1; LAMBDA=$2; LISTA=$3
if [ "$LAMBDA" = "ambos" ]; then
  FILTRO_L='("$updatePeriod"=="exponential(200)" || "$updatePeriod"=="exponential(1000)")'
else
  FILTRO_L="\"\$updatePeriod\"==\"exponential($LAMBDA)\""
fi
FILTRO="\"\$beaconPeriod\"==\"50ms\" && \$numSummaries==10 && $FILTRO_L && \$nodeCntX==$K"
vardis -s -u Cmdenv -c SmallGrids -q runnumbers -r "$FILTRO" omnetpp.ini > "$LISTA"
echo "Simulaciones seleccionadas: $(wc -w < "$LISTA")"
if [ "$4" = "solo-lista" ]; then exit 0; fi
mkdir -p logs
time (tr ' ' '\n' < "$LISTA" | grep . | xargs -P 30 -I{} sh -c 'vardis -u Cmdenv -c SmallGrids -r {} omnetpp.ini > logs/run{}.log 2>&1')
