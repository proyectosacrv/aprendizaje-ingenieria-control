"""Fase 2: impedancia de salida dq Z(jw) del inversor grid-forming."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from params import SystemParams
from impedance import build_linear, impedance

p = SystemParams()
A, B, C, D, x_eq = build_linear(p)

f = np.logspace(-1, np.log10(5e3), 600)        # 0.1 Hz .. 5 kHz
Z = impedance(A, B, C, D, f)

comp = [(0, 0, "Zdd"), (0, 1, "Zdq"), (1, 0, "Zqd"), (1, 1, "Zqq")]
fig, axes = plt.subplots(2, 1, figsize=(8, 8), sharex=True)
for i, j, name in comp:
    mag = 20 * np.log10(np.abs(Z[:, i, j]) + 1e-12)
    ph = np.degrees(np.angle(Z[:, i, j]))
    axes[0].semilogx(f, mag, label=name)
    axes[1].semilogx(f, ph, label=name)

# marcar el modo de potencia (~3.3 Hz) y la resonancia LCL (~1.1 kHz)
for fx, txt in [(3.3, "modo potencia"), (1100, "resonancia LCL")]:
    for ax in axes:
        ax.axvline(fx, color="gray", ls=":", lw=0.8)
    axes[0].annotate(txt, xy=(fx, axes[0].get_ylim()[1]), fontsize=8,
                     rotation=90, va="top", ha="right", color="gray")

axes[0].set_ylabel("|Z|  [dB-ohm]"); axes[0].grid(True, which="both", alpha=0.3)
axes[0].legend(ncol=4, fontsize=8); axes[0].set_title("Impedancia de salida dq - GFM")
axes[1].set_ylabel("fase  [deg]"); axes[1].set_xlabel("frecuencia [Hz]")
axes[1].grid(True, which="both", alpha=0.3); axes[1].legend(ncol=4, fontsize=8)
fig.tight_layout()

outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(outdir, exist_ok=True)
fig.savefig(os.path.join(outdir, "impedancia_fase2.png"), dpi=130)

# Resumen numerico
print("Impedancia de salida dq (Z_inv = Y_inv^-1):")
print(f"{'f[Hz]':>8} {'|Zdd|':>8} {'/_Zdd':>7} {'|Zqq|':>8} {'/_Zqq':>7}")
for ff in [0.1, 1, 3.3, 10, 50, 100, 1000, 1100]:
    k = np.argmin(np.abs(f - ff))
    zdd, zqq = Z[k, 0, 0], Z[k, 1, 1]
    print(f"{f[k]:8.1f} {abs(zdd):8.3f} {np.degrees(np.angle(zdd)):7.1f} "
          f"{abs(zqq):8.3f} {np.degrees(np.angle(zqq)):7.1f}")
print("\nFigura: results/impedancia_fase2.png")
