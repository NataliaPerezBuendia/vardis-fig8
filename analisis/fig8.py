import glob, math, statistics
from collections import defaultdict

PER = {"255": "10%", "263": "20%"}
datos = defaultdict(list)
sin_datos = defaultdict(int)

for f in glob.glob("results/SmallGrids-*beaconPeriod=50ms*numSummaries=10*.sca"):
    iv, cnt, suma, dentro = {}, None, None, False
    with open(f) as fh:
        for linea in fh:
            p = linea.split()
            if not p:
                continue
            if p[0] == "itervar":
                iv[p[1]] = p[2]
            elif p[0] == "statistic":
                dentro = p[1].endswith("nodes[0].application") and p[2].startswith("seqnoDeltaHist")
            elif dentro and p[0] == "field":
                if p[1] == "count":
                    cnt = float(p[2])
                elif p[1] == "sum":
                    suma = float(p[2])
    clave = (int(iv["nodeCntX"]), PER[iv["separation"]], int(iv["numRepetitions"]), iv["updatePeriod"])
    if cnt and suma:
        datos[clave].append((cnt, suma))
    else:
        sin_datos[clave] += 1

with open("fig8_vardis.csv", "w") as out:
    out.write("K,PER,repCnt,lambda,corridas,sin_datos,actualizaciones,fraccion,ic95,gap_promedio\n")
    print(f"{'K':>3} {'PER':>4} {'rep':>3} {'lambda':>17} {'runs':>4} {'0s':>3} {'n_upd':>8} {'fraccion':>9} {'ic95':>7}")
    for clave in sorted(set(datos) | set(sin_datos)):
        K, per, rep, lam = clave
        filas = datos.get(clave, [])
        tot_c = sum(c for c, s in filas)
        tot_s = sum(s for c, s in filas)
        frac = tot_c / tot_s if tot_s else 0.0
        por_corrida = [c / s for c, s in filas] + [0.0] * sin_datos[clave]
        n = len(por_corrida)
        ic = 1.96 * statistics.stdev(por_corrida) / math.sqrt(n) if n > 1 else 0.0
        gap = tot_s / tot_c if tot_c else float("nan")
        out.write(f"{K},{per},{rep},{lam},{n},{sin_datos[clave]},{int(tot_c)},{frac:.4f},{ic:.4f},{gap:.4f}\n")
        print(f"{K:>3} {per:>4} {rep:>3} {lam:>17} {n:>4} {sin_datos[clave]:>3} {int(tot_c):>8} {frac:>9.4f} {ic:>7.4f}")
