"""Fase 5: droop vs VSM (inercia) y current limiting bajo falta."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from params import SystemParams
import simulate as sim

outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(outdir, exist_ok=True)
p = SystemParams()

# ============================================================
# Experimento 1: escalon de potencia  ->  inercia droop vs VSM
# ============================================================
tstep = 0.2
pf = lambda t: 5000.0 if t < tstep else 9000.0
tt = np.linspace(0, 1.2, 2000)

fig, ax = plt.subplots(2, 1, figsize=(8, 7), sharex=True)
for mode, col in [("droop", "C0"), ("vsm", "C3")]:
    s = sim.run(p, mode=mode, pset_func=pf, t_end=1.2)
    X = s.sol(tt)
    P = 1.5 * (X[2] * X[4] + X[3] * X[5])
    if mode == "vsm":
        frq = X[15] / (2 * np.pi)
    else:
        Pset = np.where(tt < tstep, 5000.0, 9000.0)
        frq = (p.w0 + p.mp * (Pset - X[7])) / (2 * np.pi)
    ax[0].plot(tt, P, col, label=mode)
    ax[1].plot(tt, frq, col, label=mode)
ax[0].axhline(9000, color="k", ls=":", lw=0.8)
ax[0].set_ylabel("P [W]"); ax[0].legend(); ax[0].grid(alpha=0.3)
ax[0].set_title("Escalon de potencia 5->9 kW: respuesta droop vs VSM")
ax[1].set_ylabel("frecuencia [Hz]"); ax[1].set_xlabel("t [s]")
ax[1].legend(); ax[1].grid(alpha=0.3)
fig.tight_layout(); fig.savefig(os.path.join(outdir, "fase5_inercia.png"), dpi=130)
print("Figura: results/fase5_inercia.png")

# ============================================================
# Experimento 2: falta de red  ->  current limiting
# ============================================================
tf0, tf1 = 0.3, 0.42
Vsag = 0.30 * p.V0                       # hueco de tension al 30%
def efunc(t):
    return (Vsag, 0.0) if (tf0 <= t < tf1) else (p.V0, 0.0)

In = p.Sn / (1.5 * p.V0)                  # corriente pico nominal
Imax = 1.5 * In                           # limite a 1.5 pu
tt2 = np.linspace(0.25, 0.6, 3000)

fig, ax = plt.subplots(2, 1, figsize=(8, 7), sharex=True)
for ilim, lab, col in [(None, "sin limite", "C3"), (Imax, "con limite 1.5pu", "C0")]:
    s = sim.run(p, mode="droop", ilim=ilim, efunc=efunc, t_end=0.6)
    X = s.sol(tt2)
    iL1 = np.hypot(X[0], X[1])
    vc = np.hypot(X[2], X[3])
    ax[0].plot(tt2, iL1, col, label=lab)
    ax[1].plot(tt2, vc, col, label=lab)
ax[0].axhline(Imax, color="gray", ls=":", lw=0.8)
ax[0].axhline(In, color="green", ls=":", lw=0.8)
ax[0].annotate("Imax 1.5pu", (0.55, Imax), color="gray", fontsize=8)
ax[0].annotate("In nominal", (0.55, In), color="green", fontsize=8)
for a in ax:
    a.axvspan(tf0, tf1, color="yellow", alpha=0.15)
ax[0].set_ylabel("|i_L1| [A pico]"); ax[0].legend(); ax[0].grid(alpha=0.3)
ax[0].set_title("Falta de red (hueco 30%): current limiting")
ax[1].set_ylabel("|v_C| [V pico]"); ax[1].set_xlabel("t [s]")
ax[1].legend(); ax[1].grid(alpha=0.3)
fig.tight_layout(); fig.savefig(os.path.join(outdir, "fase5_falta.png"), dpi=130)
print("Figura: results/fase5_falta.png")

# Resumen numerico
for ilim, lab in [(None, "sin limite"), (Imax, "con limite")]:
    s = sim.run(p, mode="droop", ilim=ilim, efunc=efunc, t_end=0.6)
    X = s.sol(np.linspace(0.25, 0.6, 3000))
    ip = np.hypot(X[0], X[1]).max()
    print(f"  falta {lab:12s}: pico |i_L1| = {ip:6.1f} A  ({ip/In:.2f} pu)")
print(f"  In nominal = {In:.1f} A, Imax = {Imax:.1f} A")
