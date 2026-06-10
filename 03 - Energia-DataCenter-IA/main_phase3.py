"""Fase 3: pico de carga de IA en el sistema hibrido AC+DC.

Un job de IA arranca: la carga CPL salta de 100 a 230 kW en milisegundos. Se observa:
  - lado AC: caida de frecuencia del BESS (nadir y RoCoF), amortiguada por la inercia H.
  - lado DC: hundimiento transitorio de la tension del rack, gobernado por C_dc.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from params import SystemParams
import simulate as sim

p = SystemParams(Cdc=8e-3)            # condensador suficiente para que el pico sea estable
tstep = 0.1
pcpl = lambda t: 100e3 if t < tstep else 230e3      # pico de carga de IA
tt = np.linspace(0, 1.0, 4000)

fig, ax = plt.subplots(2, 1, figsize=(9, 8), sharex=True)
print("=" * 60); print("FASE 3 - Pico de carga de IA (100 -> 230 kW)"); print("=" * 60)
for H, col in [(1.0, "C3"), (3.0, "C1"), (6.0, "C0")]:
    s = sim.run(p, pcpl, H=H, t_end=1.0)
    X = s.sol(tt)
    fHz = X[2] / (2 * np.pi)
    nadir = fHz.min()
    rocof = np.min(np.gradient(fHz, tt))           # df/dt mas negativo
    ax[0].plot(tt, fHz, col, label=f"H={H:.0f} s  (nadir {nadir:.3f} Hz, RoCoF {rocof:.2f} Hz/s)")
    print(f"  H={H:.0f} s: nadir={nadir:.3f} Hz, RoCoF={rocof:.2f} Hz/s")
ax[0].axhline(50, color="k", ls=":", lw=0.8)
ax[0].axvspan(tstep, 1.0, color="yellow", alpha=0.08)
ax[0].set_ylabel("frecuencia BESS [Hz]"); ax[0].legend(fontsize=9); ax[0].grid(alpha=.3)
ax[0].set_title("Lado AC: el pico de carga hunde la frecuencia; mas inercia H = menor RoCoF/nadir")

# lado DC: hundimiento de V_dc para distintos C_dc
for cdc, col in [(4e-3, "C3"), (8e-3, "C1"), (16e-3, "C0")]:
    pc = SystemParams(Cdc=cdc)
    s = sim.run(pc, pcpl, H=3.0, t_end=1.0)
    X = s.sol(tt)
    ax[1].plot(tt, X[1], col, label=f"Cdc={cdc*1e3:.0f} mF  (min {X[1].min():.0f} V)")
ax[1].axhline(800, color="k", ls=":", lw=0.8)
ax[1].axvspan(tstep, 1.0, color="yellow", alpha=0.08)
ax[1].set_ylabel("tension del rack V_dc [V]"); ax[1].set_xlabel("t [s]")
ax[1].legend(fontsize=9); ax[1].grid(alpha=.3)
ax[1].set_title("Lado DC: el condensador C_dc amortigua el hundimiento del bus")
fig.tight_layout()
outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(outdir, exist_ok=True)
fig.savefig(os.path.join(outdir, "fase3_pico_carga.png"), dpi=130)
print("Figura: results/fase3_pico_carga.png")
