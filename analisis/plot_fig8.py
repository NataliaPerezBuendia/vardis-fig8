import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

filas = list(csv.DictReader(open("fig8_vardis.csv")))
paneles = [("10%", "exponential(200)", "(a) PER 10 %, λ = 200 ms"),
           ("10%", "exponential(1000)", "(b) PER 10 %, λ = 1000 ms"),
           ("20%", "exponential(200)", "(c) PER 20 %, λ = 200 ms"),
           ("20%", "exponential(1000)", "(d) PER 20 %, λ = 1000 ms")]
fig, ejes = plt.subplots(2, 2, figsize=(11, 8), sharex=True, sharey=True)
for ax, (per, lam, titulo) in zip(ejes.flat, paneles):
    for rep, marca in zip(("1", "2", "3"), ("^", "v", "o")):
        sel = sorted((int(f["K"]), float(f["fraccion"]), float(f["ic95"])) for f in filas
                     if f["PER"] == per and f["lambda"] == lam and f["repCnt"] == rep)
        ax.errorbar([s[0] for s in sel], [s[1] for s in sel], yerr=[s[2] for s in sel],
                    marker=marca, capsize=3, label=f"VarDis, repCnt = {rep}")
    ax.set_title(titulo)
    ax.set_xlim(4, 12)
    ax.set_ylim(0, 1.05)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
for ax in ejes[1]:
    ax.set_xlabel("K (nodos por lado)")
for ax in ejes[:, 0]:
    ax.set_ylabel("Fracción de actualizaciones recibidas")
fig.suptitle("Reproducción de la Fig. 8 (lado VarDis), K ∈ {5, 7, 9}, 48 repeticiones")
fig.tight_layout()
fig.savefig("fig8_reproduccion.png", dpi=150)
print("Gráfica guardada en fig8_reproduccion.png")
