"""Fase 2: impedancia de salida dq del GFL y la resistencia negativa de la PLL.

La firma del grid-following: en la banda de la PLL, la parte REAL de la impedancia de
salida se vuelve negativa (comportamiento no pasivo). Cuanto mas rapida la PLL, mas
pronunciada -> mayor riesgo de inestabilidad al encontrarse con la impedancia de la red.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from params import SystemParams
from impedance import build_linear, impedance

f = np.logspace(-1, 3.3, 600)
fig, ax = plt.subplots(2, 1, figsize=(8, 8), sharex=True)
for fpll, col in [(30.0, "C0"), (100.0, "C3")]:
    A, B, C, D, _ = build_linear(SystemParams(f_pll=fpll))
    Z = impedance(A, B, C, D, f)
    ax[0].semilogx(f, Z[:, 0, 0].real, col, label=f"f_pll={fpll:.0f} Hz")
    ax[1].semilogx(f, Z[:, 1, 1].real, col, label=f"f_pll={fpll:.0f} Hz")
for a, name in zip(ax, ["Re(Z_dd)", "Re(Z_qq)"]):
    a.axhline(0, color="k", lw=0.8, ls="--")
    a.set_ylabel(f"{name}  [ohm]"); a.grid(True, which="both", alpha=0.3); a.legend()
ax[0].set_title("Impedancia de salida del GFL: parte real (resistencia negativa de la PLL)")
ax[1].set_xlabel("frecuencia [Hz]")
fig.tight_layout()
outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(outdir, exist_ok=True)
fig.savefig(os.path.join(outdir, "impedancia_fase2.png"), dpi=130)

# La resistencia negativa aparece en el EJE Q (la PLL actua sobre v_q):
print("Parte real de la impedancia de salida, eje q  Re(Z_qq) [ohm]:")
print(f"{'f[Hz]':>8} {'f_pll=30':>10} {'f_pll=100':>10}")
A1, B1, C1, D1, _ = build_linear(SystemParams(f_pll=30.0))
A2, B2, C2, D2, _ = build_linear(SystemParams(f_pll=100.0))
for ff in [1, 5, 10, 20, 50, 100]:
    z1 = impedance(A1, B1, C1, D1, [ff])[0, 1, 1]
    z2 = impedance(A2, B2, C2, D2, [ff])[0, 1, 1]
    print(f"{ff:8.0f} {z1.real:10.2f} {z2.real:10.2f}")
print("\nRe(Z_qq) < 0 = comportamiento NO PASIVO (resistencia negativa) inducido por la PLL.")
print("Con PLL rapida se mantiene negativa hasta mas alta frecuencia -> mas riesgo en red debil.")
print("Figura: results/impedancia_fase2.png")
