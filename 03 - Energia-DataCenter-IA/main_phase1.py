"""Fase 1: estabilidad del sub-bus DC con carga CPL. Potencia critica y amortiguamiento."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from params import SystemParams
from model_dc import DCBus

def maxre(pcpl, rd=0.0, cdc=2e-3):
    p = SystemParams(Pcpl=pcpl, Rd=rd, Cdc=cdc); g = DCBus(p)
    x, info = g.equilibrium()
    return np.linalg.eigvals(g.linearize(x, np.array([0.0]))[0]).real.max()

p0 = SystemParams()
print("=" * 60); print("FASE 1 - Sub-bus DC con carga CPL"); print("=" * 60)
print(f"P_critica teorica  P = V^2 R C / L = {p0.Pcrit/1e3:.0f} kW")
P = np.linspace(20e3, 350e3, 80)
mr = np.array([maxre(pp) for pp in P])
pcrit_num = P[np.argmin(np.abs(mr))]
print(f"P_critica numerica (maxRe=0)     = {pcrit_num/1e3:.0f} kW")
print(f"  -> por encima, el bus DC oscila (CPL desamortigua el filtro L-C)")

fig, ax = plt.subplots(1, 2, figsize=(13, 5))
for cdc, col in [(2e-3, "C3"), (5e-3, "C1"), (10e-3, "C0")]:
    m = [maxre(pp, 0.0, cdc) for pp in P]
    ax[0].plot(P/1e3, m, col, label=f"Cdc={cdc*1e3:.0f} mF")
ax[0].axhline(0, color="k", lw=1); ax[0].set_xlabel("P_cpl [kW]")
ax[0].set_ylabel("max Re(autovalores) [1/s]  (>0 inestable)")
ax[0].set_title("Inestabilidad por CPL: mas condensador eleva la potencia critica")
ax[0].legend(); ax[0].grid(alpha=.3); ax[0].set_ylim(-100, 120)

rds = np.linspace(0, 0.05, 60)
pc_rd = [SystemParams(Rd=r).Pcrit/1e3 for r in rds]
ax[1].plot(rds*1e3, pc_rd, "C2")
ax[1].set_xlabel("amortiguamiento R_d [mOhm]"); ax[1].set_ylabel("P_critica [kW]")
ax[1].set_title("El amortiguamiento (o C_dc) sube la potencia CPL admisible")
ax[1].grid(alpha=.3)
fig.tight_layout()
outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(outdir, exist_ok=True)
fig.savefig(os.path.join(outdir, "fase1_cpl.png"), dpi=130)
print("\nFigura: results/fase1_cpl.png")
