#!/bin/bash
# Compila el código de Pell y Willig (carpeta simulation-code-paper, commit e75345b).
# El repositorio original no incluye Makefiles; se generan aquí con opp_makemake.
# Requiere OMNeT++ 6.0.3 e INET 4.4.2 cargados (setenv) y la variable INET_ROOT definida.
set -e
P=${1:-$HOME/dcp-vardis/simulation-code-paper}

# 1. SwarmStack como librería compartida
cd "$P/SwarmStack/src"
opp_makemake -f --deep --make-so -o SwarmStack -O out -I. -I$INET_ROOT/src -L$INET_ROOT/src -lINET -DINET_IMPORT
make -j$(nproc)

# 2. srp_vardis como ejecutable, enlazado con INET y SwarmStack
cd "$P/srp_vardis/src"
opp_makemake -f --deep -o srp_vardis -O out -I. -I$INET_ROOT/src -I$P/SwarmStack/src -L$INET_ROOT/src -L$P/SwarmStack/src -lINET -lSwarmStack -DINET_IMPORT
make -j$(nproc)
