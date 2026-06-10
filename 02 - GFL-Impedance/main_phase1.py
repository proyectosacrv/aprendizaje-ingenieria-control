"""Fase 1: equilibrio, polos y mapa de polos del inversor grid-following (red rigida)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from params import SystemParams
from model import GFLInverter

p = SystemParams()
g = GFLInverter(p)
u = np.array([p.V0, 0.0])
x, info = g.equilibrium(u)
P = 1.5 * (x[2] * x[4] + x[3] * x[5]); Q = 1.5 * (x[3] * x[4] - x[2] * x[5])

print("=" * 60); print("FASE 1 - Inversor grid-following (red rigida)"); print("=" * 60)
print(f"Equilibrio: ier={info['ier']} residual={info['residual']:.2e}")
print(f"  P_eq={P:8.1f} W  Q_eq={Q:8.1f} var  |vc|={np.hypot(x[2],x[3]):.1f} V  delta={np.degrees(x[6]):.2f} deg")
print(f"  v_Cq={x[3]:.2e} (la PLL lo lleva a 0)")

A, B, C, D = g.linearize(x, u)
eig = np.linalg.eigvals(A); eig = eig[np.argsort(-eig.real)]
print("\nAutovalores:")
for l in eig:
    print(f"  {l.real:>10.2f} {l.imag:>+10.2f}j   f={abs(l.imag)/2/np.pi:7.1f} Hz   zeta={-l.real/abs(l) if abs(l)>0 else 1:+.3f}")
print(f"\nSistema {'ESTABLE' if np.all(eig.real<0) else 'INESTABLE'} (max Re={eig.real.max():.2f})")
print("Nota: el modo a ~21 Hz, zeta 0.71, es el de la PLL (f_pll=30 Hz).")

outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(outdir, exist_ok=True)
fig, ax = plt.subplots(figsize=(7, 6))
ax.scatter(eig.real, eig.imag, marker="x", s=70, c="C0")
ax.axvline(0, color="k", lw=0.8); ax.axhline(0, color="k", lw=0.5)
ax.set_xlabel("Re [1/s]"); ax.set_ylabel("Im [rad/s]")
ax.set_title("Mapa de polos - GFL en lazo cerrado (red rigida)")
ax.grid(True, alpha=0.3); fig.tight_layout()
fig.savefig(os.path.join(outdir, "polos_fase1.png"), dpi=130)
print("\nFigura: results/polos_fase1.png")
