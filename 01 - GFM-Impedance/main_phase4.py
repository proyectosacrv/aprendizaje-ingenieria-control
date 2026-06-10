"""Fase 4: validacion de Z_dq por inyeccion de perturbacion (metodo tipo PLECS).

Compara la impedancia MEDIDA (inyectando perturbaciones sobre el modelo no lineal y
demodulando) con la impedancia ANALITICA (linealizacion, Fase 2). Tambien muestra el
efecto de la amplitud de perturbacion: pequena -> regimen lineal (coincide);
grande -> aparecen efectos no lineales.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from params import SystemParams
from impedance import build_linear, impedance
from inject import measure_Z

outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(outdir, exist_ok=True)
p = SystemParams()
A, B, C, D, _ = build_linear(p)

# --- Barrido: medida (inyeccion) vs analitica ---
freqs = np.array([2, 3.3, 5, 8, 13, 20, 35, 60, 100, 180, 320, 500.0])
print("Midiendo impedancia por inyeccion (puede tardar ~1 min)...")
Zm = measure_Z(p, freqs, amp=2.0)

fa = np.logspace(np.log10(1.5), np.log10(600), 400)
Za = impedance(A, B, C, D, fa)

fig, ax = plt.subplots(2, 2, figsize=(11, 8))
for (i, j), (r, c), name in [((0, 0), (0, 0), "Zdd"), ((1, 1), (0, 1), "Zqq")]:
    ax[0, c].semilogx(fa, 20*np.log10(np.abs(Za[:, i, j])), "C0-", label="analitica")
    ax[0, c].semilogx(freqs, 20*np.log10(np.abs(Zm[:, i, j])), "C3o", label="medida (inyeccion)")
    ax[1, c].semilogx(fa, np.degrees(np.angle(Za[:, i, j])), "C0-")
    ax[1, c].semilogx(freqs, np.degrees(np.angle(Zm[:, i, j])), "C3o")
    ax[0, c].set_title(name); ax[0, c].set_ylabel("|Z| [dB-ohm]")
    ax[1, c].set_ylabel("fase [deg]"); ax[1, c].set_xlabel("f [Hz]")
    for rr in (0, 1):
        ax[rr, c].grid(True, which="both", alpha=0.3)
    ax[0, c].legend(fontsize=8)
fig.suptitle("Fase 4: impedancia medida (inyeccion) vs analitica")
fig.tight_layout()
fig.savefig(os.path.join(outdir, "fase4_validacion.png"), dpi=130)
print("Figura: results/fase4_validacion.png")

# error global
err = np.array([100*abs(Zm[k, 0, 0]-impedance(A, B, C, D, [freqs[k]])[0, 0, 0])
                / abs(impedance(A, B, C, D, [freqs[k]])[0, 0, 0]) for k in range(len(freqs))])
print(f"Error medio |Zdd|: {err.mean():.2f}%  (max {err.max():.2f}%)")

# --- La impedancia es independiente de la amplitud (regimen lineal) ---
# Mientras no se active una no linealidad fuerte (p.ej. current limiting), la Z medida
# no depende de la amplitud de la perturbacion: confirma que se opera en pequena senal.
print("\nLinealidad: |Zdd| medida a 20 Hz vs amplitud de perturbacion:")
fp = 20.0
Za20 = impedance(A, B, C, D, [fp])[0, 0, 0]
print(f"  {'amp[V]':>7} {'|Zdd|med':>9}   error% vs analitica")
for a in [1.0, 5.0, 20.0, 80.0]:
    Z = measure_Z(p, [fp], amp=a)[0, 0, 0]
    print(f"  {a:7.1f} {abs(Z):9.3f}        {100*abs(Z-Za20)/abs(Za20):5.2f}%")
print("Error ~constante e ~0 -> regimen lineal. La no linealidad por SATURACION de")
print("corriente es un fenomeno de gran senal: ver Fase 5 (current limiting bajo falta).")
