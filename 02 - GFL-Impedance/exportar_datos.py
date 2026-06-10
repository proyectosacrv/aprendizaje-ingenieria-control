"""Exporta los resultados numericos del proyecto GFL a CSV (carpeta datos/).
    python exportar_datos.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from params import SystemParams
from model import GFLInverter, STATE_NAMES
from impedance import build_linear, impedance
from grid import grid_params

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos")
os.makedirs(OUT, exist_ok=True)

p = SystemParams()
g = GFLInverter(p)
u = np.array([p.V0, 0.0])
xeq, info = g.equilibrium(u)
A, B, C, D = g.linearize(xeq, u)

# 1) Equilibrio
P_eq = 1.5 * (xeq[2] * xeq[4] + xeq[3] * xeq[5])
Q_eq = 1.5 * (xeq[3] * xeq[4] - xeq[2] * xeq[5])
with open(os.path.join(OUT, "equilibrio.csv"), "w", encoding="utf-8") as f:
    f.write("estado,valor\n")
    for n, v in zip(STATE_NAMES, xeq):
        f.write(f"{n},{v:.6g}\n")
    f.write(f"P_eq_W,{P_eq:.6g}\nQ_eq_var,{Q_eq:.6g}\nresidual,{info['residual']:.3e}\n")

# 2) Autovalores
ev = np.linalg.eigvals(A)
ev = ev[np.argsort(-ev.real)]
np.savetxt(os.path.join(OUT, "autovalores.csv"),
           np.column_stack([ev.real, ev.imag, np.abs(ev.imag) / (2 * np.pi),
                            -ev.real / np.abs(ev)]),
           delimiter=",", header="re_1/s,im_rad/s,f_Hz,zeta", comments="", fmt="%.6g")

# 3) Parte real de la impedancia de salida (resistencia negativa de la PLL) vs f
fre = np.logspace(-1, 3.3, 600)
A1, B1, C1, D1, _ = build_linear(SystemParams(f_pll=30.0))
A2, B2, C2, D2, _ = build_linear(SystemParams(f_pll=100.0))
Z1 = impedance(A1, B1, C1, D1, fre)
Z2 = impedance(A2, B2, C2, D2, fre)
np.savetxt(os.path.join(OUT, "impedancia_reZ.csv"),
           np.column_stack([fre, Z1[:, 0, 0].real, Z1[:, 1, 1].real,
                            Z2[:, 0, 0].real, Z2[:, 1, 1].real]),
           delimiter=",",
           header="f_Hz,ReZdd_fpll30,ReZqq_fpll30,ReZdd_fpll100,ReZqq_fpll100",
           comments="", fmt="%.6g")

# 4) SCR critico vs ancho de banda de la PLL
def coupled_maxre(scr, fpll):
    Rg, Lg = grid_params(scr, 5.0, SystemParams(f_pll=fpll))
    pp = SystemParams(f_pll=fpll, Rg=Rg, Lg=Lg)
    gg = GFLInverter(pp)
    x, r = gg.equilibrium(np.array([pp.V0, 0.0]))
    if r["residual"] > 1e-6:
        return np.nan
    return np.linalg.eigvals(gg.linearize(x, np.array([pp.V0, 0.0]))[0]).real.max()

fplls = np.arange(40, 175, 10)
crit = []
for fp in fplls:
    lo, hi = 1.0, 9.0
    for _ in range(36):
        mid = 0.5 * (lo + hi)
        lo, hi = (lo, mid) if coupled_maxre(mid, fp) < 0 else (mid, hi)
    crit.append(0.5 * (lo + hi))
np.savetxt(os.path.join(OUT, "scr_vs_pll.csv"),
           np.column_stack([fplls, crit]), delimiter=",",
           header="f_pll_Hz,SCR_critico", comments="", fmt="%.6g")

print("Exportado a datos/:")
print("  equilibrio.csv     - punto de operacion (10 estados)")
print("  autovalores.csv    - 10 modos (re, im, f, zeta)")
print("  impedancia_reZ.csv - Re(Zdd), Re(Zqq) para f_pll=30 y 100 Hz")
print("  scr_vs_pll.csv     - SCR critico vs ancho de banda de la PLL")
