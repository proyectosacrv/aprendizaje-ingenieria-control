"""Fase 1: equilibrio, linealizacion y mapa de polos del inversor grid-forming."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from params import SystemParams
from model import GFMInverter, STATE_NAMES

p = SystemParams()
gfm = GFMInverter(p)

# --- Punto de operacion: red rigida nominal en eje d del marco s ---
u_eq = np.array([p.V0, 0.0])
x_eq, info = gfm.equilibrium(u_eq)

P_eq = 1.5 * (x_eq[2] * x_eq[4] + x_eq[3] * x_eq[5])
Q_eq = 1.5 * (x_eq[3] * x_eq[4] - x_eq[2] * x_eq[5])

print("=" * 60)
print("FASE 1 - Inversor grid-forming")
print("=" * 60)
print(f"Equilibrio: ier={info['ier']}  residual={info['residual']:.2e}")
print(f"  P_eq = {P_eq:8.1f} W   (consigna {p.Pset:.0f} W)")
print(f"  Q_eq = {Q_eq:8.1f} var (consigna {p.Qset:.0f} var)")
print(f"  delta = {np.degrees(x_eq[6]):.2f} deg")
print(f"  |vc|  = {np.hypot(x_eq[2], x_eq[3]):.1f} V (pico fase, nominal {p.V0:.1f})")

# --- Linealizacion ---
A, B, C, D = gfm.linearize(x_eq, u_eq)
eig = np.linalg.eigvals(A)
order = np.argsort(-eig.real)         # de menos a mas estable
eig = eig[order]

print("\nAutovalores (parte real, parte imag, f[Hz], zeta):")
for lam in eig:
    f_hz = abs(lam.imag) / (2 * np.pi)
    zeta = -lam.real / abs(lam) if abs(lam) > 0 else 1.0
    print(f"  {lam.real:>12.2f} {lam.imag:>+12.2f}j   f={f_hz:8.1f} Hz   zeta={zeta:+.3f}")

stable = np.all(eig.real < 0)
print(f"\nSistema {'ESTABLE' if stable else 'INESTABLE'} "
      f"(max Re = {eig.real.max():.2f})")

# --- Mapa de polos ---
outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(outdir, exist_ok=True)
fig, ax = plt.subplots(figsize=(7, 6))
ax.scatter(eig.real, eig.imag, marker="x", s=70, c="C3")
ax.axvline(0, color="k", lw=0.8)
ax.axhline(0, color="k", lw=0.5)
ax.set_xlabel("Re  [1/s]"); ax.set_ylabel("Im  [rad/s]")
ax.set_title("Mapa de polos - GFM en lazo cerrado")
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(outdir, "polos_fase1.png"), dpi=130)
print(f"\nFigura guardada en results/polos_fase1.png")
