"""Fase 3: inestabilidad del GFL en red debil.

(A) Autovalores del modelo acoplado -> SCR critico.
(B) Criterio de impedancia (Nyquist generalizado de Z_red*Y_inv) -> debe coincidir.
Ademas: como el ancho de banda de la PLL mueve el SCR critico.

Se usa una PLL rapida (f_pll=100 Hz) que SI pierde estabilidad en red debil.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from params import SystemParams
from model import GFLInverter
from impedance import build_linear, admittance
from grid import grid_params, grid_impedance_dq

XR = 5.0
FPLL = 100.0

def coupled_maxre(scr, fpll=FPLL):
    p0 = SystemParams(f_pll=fpll); Rg, Lg = grid_params(scr, XR, p0)
    p = SystemParams(f_pll=fpll, Rg=Rg, Lg=Lg); g = GFLInverter(p)
    u = np.array([p.V0, 0.0]); x, r = g.equilibrium(u)
    if r["residual"] > 1e-6: return np.nan
    return np.linalg.eigvals(g.linearize(x, u)[0]).real.max()

# (A) SCR critico (acoplado) por biseccion: estable a SCR alto, inestable a SCR bajo
lo, hi = 2.0, 6.0
for _ in range(40):
    mid = 0.5 * (lo + hi)
    (lo, hi) = (lo, mid) if coupled_maxre(mid) < 0 else (mid, hi)
scr_crit_c = 0.5 * (lo + hi)
print(f"(A) SCR critico (modelo acoplado) = {scr_crit_c:.3f}  [inestable por debajo]")

# (B) Nyquist de impedancia: Y_inv del inversor solo
p_inv = SystemParams(f_pll=FPLL)
A, B, C, D, _ = build_linear(p_inv)
f = np.logspace(-1, 3.3, 2000)
Y = admittance(A, B, C, D, f)
def mindet(scr):
    Rg, Lg = grid_params(scr, XR, p_inv); Zg = grid_impedance_dq(Rg, Lg, p_inv.w0, f)
    return min(abs(np.linalg.det(np.eye(2) + Zg[k] @ Y[k])) for k in range(len(f)))
scrs = np.linspace(2.5, 4.5, 60); d = [mindet(s) for s in scrs]
scr_crit_i = scrs[int(np.argmin(d))]
print(f"(B) SCR critico (Nyquist impedancia) = {scr_crit_i:.3f}")
print(f"    diferencia = {abs(scr_crit_i-scr_crit_c):.3f}")

# Nyquist a 3 SCR
def loop_eigs(scr):
    Rg, Lg = grid_params(scr, XR, p_inv); Zg = grid_impedance_dq(Rg, Lg, p_inv.w0, f)
    return np.array([np.linalg.eigvals(Zg[k] @ Y[k]) for k in range(len(f))])

outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(outdir, exist_ok=True)
fig, ax = plt.subplots(1, 2, figsize=(13, 6))
for scr, col in [(scr_crit_c*1.6, "C0"), (scr_crit_c, "C1"), (scr_crit_c*0.6, "C3")]:
    lam = loop_eigs(scr)
    for j in range(2):
        ax[0].plot(lam[:, j].real, lam[:, j].imag, col, lw=1.0)
    ax[0].plot(np.nan, np.nan, col, label=f"SCR={scr:.2f}")
ax[0].plot(-1, 0, "kx", ms=12, mew=2, label="-1")
ax[0].set_xlim(-3, 2); ax[0].set_ylim(-2.5, 2.5); ax[0].set_aspect("equal")
ax[0].axhline(0, color="k", lw=.4); ax[0].axvline(0, color="k", lw=.4)
ax[0].set_title("Nyquist generalizado  Z_red*Y_inv (GFL)"); ax[0].legend(); ax[0].grid(alpha=.3)

# efecto del ancho de banda de la PLL en el SCR critico
fplls = [40, 60, 80, 100, 130, 170]; crit = []
for fp in fplls:
    lo, hi = 1.0, 8.0
    for _ in range(34):
        mid = 0.5*(lo+hi); (lo, hi) = (lo, mid) if coupled_maxre(mid, fp) < 0 else (mid, hi)
    crit.append(0.5*(lo+hi))
ax[1].plot(fplls, crit, "o-", color="C3")
ax[1].set_xlabel("ancho de banda PLL [Hz]"); ax[1].set_ylabel("SCR critico")
ax[1].set_title("PLL mas rapida -> inestable hasta SCR mas alto\n(region debil mas amplia)")
ax[1].grid(alpha=.3)
fig.tight_layout(); fig.savefig(os.path.join(outdir, "estabilidad_fase3.png"), dpi=130)
print("\nSCR critico vs f_pll:")
for fp, c in zip(fplls, crit):
    print(f"  f_pll={fp:4.0f} Hz -> SCR critico = {c:.2f}")
print("Figura: results/estabilidad_fase3.png")
