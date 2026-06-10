"""Comparacion GFM vs GFL: estabilidad frente a la fortaleza de la red.

Resultado central del estudio: son ESPEJO uno del otro.
  - GFL (PLL rapida): estable en red fuerte, INESTABLE en red debil (SCR bajo).
  - GFM (droop agresivo): estable en red debil, INESTABLE en red fuerte (SCR alto).
Carga el modelo GFM del proyecto 01 con importlib (sin colision de nombres) y el GFL local.
"""
import os, sys, importlib.util, pathlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from params import SystemParams
from model import GFLInverter
from grid import grid_params

BASE = pathlib.Path(__file__).parent.parent

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod
    spec.loader.exec_module(mod); return mod

gfm_params = load("gfm_params", BASE / "01 - GFM-Impedance" / "params.py")
gfm_model = load("gfm_model", BASE / "01 - GFM-Impedance" / "model.py")
GFM_CFG = dict(droop_p=0.03, droop_q=0.05, Lv=2e-3, Rvt=0.0, Rv=0.0, f_cv=250)
XR = 5.0

def gfm_maxre(scr):
    p0 = gfm_params.SystemParams(**GFM_CFG); Rg, Lg = grid_params(scr, XR, p0)
    p = gfm_params.SystemParams(Rg=Rg, Lg=Lg, **GFM_CFG); g = gfm_model.GFMInverter(p)
    u = np.array([p.V0, 0.0]); x, r = g.equilibrium(u)
    if r["residual"] > 1e-6: return np.nan
    return np.linalg.eigvals(g.linearize(x, u)[0]).real.max()

def gfl_maxre(scr, fpll=100.0):
    p0 = SystemParams(f_pll=fpll); Rg, Lg = grid_params(scr, XR, p0)
    p = SystemParams(f_pll=fpll, Rg=Rg, Lg=Lg); g = GFLInverter(p)
    u = np.array([p.V0, 0.0]); x, r = g.equilibrium(u)
    if r["residual"] > 1e-6: return np.nan
    return np.linalg.eigvals(g.linearize(x, u)[0]).real.max()

scr = np.linspace(1.2, 12, 40)
mg = np.array([gfm_maxre(s) for s in scr])
ml = np.array([gfl_maxre(s) for s in scr])

fig, ax = plt.subplots(figsize=(9, 6))
ax.plot(scr, np.clip(mg, -60, 60), "C5-o", ms=3, label="GFM (droop agresivo)")
ax.plot(scr, np.clip(ml, -60, 60), "C0-o", ms=3, label="GFL (PLL rapida)")
ax.axhline(0, color="k", lw=1)
ax.fill_between(scr, 0, 60, where=(np.clip(mg,-60,60) > 0), color="C5", alpha=0.12)
ax.fill_between(scr, 0, 60, where=(np.clip(ml,-60,60) > 0), color="C0", alpha=0.12)
ax.set_xlabel("SCR (fortaleza de red)  ->  debil ... fuerte")
ax.set_ylabel("max Re(autovalores)  [1/s]  (>0 = inestable)")
ax.set_title("GFM vs GFL: estabilidad espejo frente a la red")
ax.annotate("GFL inestable\n(red debil)", (1.6, 40), color="C0", fontsize=9)
ax.annotate("GFM inestable\n(red fuerte)", (9, 40), color="C5", fontsize=9)
ax.legend(); ax.grid(alpha=.3); fig.tight_layout()
outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(outdir, exist_ok=True)
fig.savefig(os.path.join(outdir, "comparacion_gfm_gfl.png"), dpi=130)

def crit(fn, lo, hi, decr):
    for _ in range(36):
        m = 0.5*(lo+hi); v = fn(m)
        if decr: (lo, hi) = (m, hi) if v < 0 else (lo, m)
        else:    (lo, hi) = (lo, m) if v < 0 else (m, hi)
    return 0.5*(lo+hi)
print(f"SCR critico GFM (inestable por ENCIMA) ~ {crit(gfm_maxre,2,6,True):.2f}")
print(f"SCR critico GFL (inestable por DEBAJO) ~ {crit(gfl_maxre,2,6,False):.2f}")
print("Figura: results/comparacion_gfm_gfl.png")
