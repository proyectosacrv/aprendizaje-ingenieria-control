"""Fase 3: estabilidad en red debil por impedancia (Nyquist generalizado).

Compara dos vias para hallar el SCR critico:
  (A) Autovalores del modelo acoplado inversor+red (verdad de referencia).
  (B) Criterio de impedancia: Nyquist generalizado de L = Z_grid * Y_inv.
Si el modelado es correcto, ambos coinciden.

Se usa un control "agresivo" (droop alto, sin amortiguamiento transitorio) que
SI pierde estabilidad en red fuerte, para ilustrar el criterio.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from params import SystemParams
from model import GFMInverter
from impedance import build_linear, admittance
from grid import grid_params, grid_impedance_dq

CFG = dict(droop_p=0.03, droop_q=0.05, Lv=2e-3, Rvt=0.0, Rv=0.0, f_cv=250)
XR = 5.0


def coupled_maxre(scr):
    p0 = SystemParams(**CFG)
    Rg, Lg = grid_params(scr, XR, p0)
    p = SystemParams(Rg=Rg, Lg=Lg, **CFG)
    g = GFMInverter(p)
    u = np.array([p.V0, 0.0])
    x, r = g.equilibrium(u)
    if r["residual"] > 1e-6:
        return np.nan
    return np.linalg.eigvals(g.linearize(x, u)[0]).real.max()


# (A) SCR critico por biseccion sobre el modelo acoplado
lo, hi = 2.0, 6.0
for _ in range(40):
    mid = 0.5 * (lo + hi)
    (lo, hi) = (mid, hi) if coupled_maxre(mid) < 0 else (lo, mid)
scr_crit_coupled = 0.5 * (lo + hi)
print(f"(A) SCR critico (modelo acoplado) = {scr_crit_coupled:.3f}")

# (B) Nyquist generalizado: Y_inv del inversor SOLO (sin red)
p_inv = SystemParams(**CFG)
A, B, C, D, _ = build_linear(p_inv)
f = np.logspace(-1, 3.5, 2000)
Y = admittance(A, B, C, D, f)

def loop_eigs(scr):
    """Autovalores de L(jw) = Z_grid * Y_inv para cada frecuencia."""
    Rg, Lg = grid_params(scr, XR, p_inv)
    Zg = grid_impedance_dq(Rg, Lg, p_inv.w0, f)
    lam = np.zeros((len(f), 2), dtype=complex)
    for k in range(len(f)):
        lam[k] = np.linalg.eigvals(Zg[k] @ Y[k])
    return lam

# SCR critico por criterio de impedancia: donde el locus toca -1
# (min sobre w de |det(I + Z_grid Y_inv)| pasa por 0)
def min_dist_to_crit(scr):
    Rg, Lg = grid_params(scr, XR, p_inv)
    Zg = grid_impedance_dq(Rg, Lg, p_inv.w0, f)
    d = []
    for k in range(len(f)):
        L = Zg[k] @ Y[k]
        d.append(abs(np.linalg.det(np.eye(2) + L)))
    return min(d)

# barrido para localizar el minimo de la distancia critica
scrs = np.linspace(2.5, 5.0, 60)
dmin = [min_dist_to_crit(s) for s in scrs]
scr_crit_imp = scrs[int(np.argmin(dmin))]
print(f"(B) SCR critico (Nyquist impedancia) = {scr_crit_imp:.3f}")
print(f"    diferencia = {abs(scr_crit_imp-scr_crit_coupled):.3f}")

# --- Figura: Nyquist generalizado a 3 SCR ---
fig, ax = plt.subplots(figsize=(7, 7))
for scr, col in [(scr_crit_coupled*0.6, "C0"),
                 (scr_crit_coupled, "C1"),
                 (scr_crit_coupled*1.6, "C3")]:
    lam = loop_eigs(scr)
    for j in range(2):
        ax.plot(lam[:, j].real, lam[:, j].imag, col, lw=1.0)
    ax.plot(np.nan, np.nan, col, label=f"SCR={scr:.2f}")
ax.plot(-1, 0, "kx", ms=12, mew=2, label="punto -1")
ax.set_xlim(-3, 2); ax.set_ylim(-2.5, 2.5)
ax.axhline(0, color="k", lw=0.4); ax.axvline(0, color="k", lw=0.4)
ax.set_xlabel("Re"); ax.set_ylabel("Im")
ax.set_title("Nyquist generalizado  L = Z_grid * Y_inv\n(autovalores)")
ax.legend(); ax.grid(True, alpha=0.3); ax.set_aspect("equal")
fig.tight_layout()
outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(outdir, exist_ok=True)
fig.savefig(os.path.join(outdir, "nyquist_fase3.png"), dpi=130)
print("\nFigura: results/nyquist_fase3.png")
print("Interpretacion: al crecer SCR (red mas fuerte) el locus envuelve -1 -> inestable.")
