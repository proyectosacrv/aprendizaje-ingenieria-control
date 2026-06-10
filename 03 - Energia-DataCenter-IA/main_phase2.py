"""Fase 2: estabilidad del bus DC por impedancia (criterio de Middlebrook).

Fuente (V_bus + cable L-R + C_dc) con impedancia de salida Z_fuente(s).
Carga CPL con impedancia incremental Z_cpl = -V^2/P (resistencia NEGATIVA, |Z| = V^2/P).
Criterio de Middlebrook: estable si |Z_fuente(jw)| < |Z_cpl| para todo w. La inestabilidad
aparece cuando el pico de resonancia de Z_fuente toca |Z_cpl| (que baja al subir P).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from params import SystemParams
from model_dc import DCBus

p = SystemParams()

# Z_fuente: impedancia de salida del filtro L-R-C SIN la CPL (Pcpl=0)
pf = SystemParams(Pcpl=0.0)
g = DCBus(pf); x, _ = g.equilibrium()
A, B, C, D = g.linearize(x, np.array([0.0]))
f = np.logspace(1, 4.5, 800); s = 2j * np.pi * f
I = np.eye(A.shape[0])
Zsrc = np.array([(C @ np.linalg.solve(si * I - A, B) + D)[0, 0] for si in s])

fig, ax = plt.subplots(figsize=(8, 6))
ax.semilogx(f, 20*np.log10(np.abs(Zsrc)), "C0", lw=2, label="|Z_fuente| (filtro L-C)")
for pk, col in [(80, "C2"), (128, "C1"), (200, "C3")]:
    Zcpl = p.Vbus**2 / (pk*1e3)                 # |Z_cpl| = V^2 / P
    ax.axhline(20*np.log10(Zcpl), color=col, ls="--",
               label=f"|Z_cpl| con P={pk} kW ({Zcpl:.2f} Ω)")
ax.set_xlabel("frecuencia [Hz]"); ax.set_ylabel("|Z|  [dB-Ω]")
ax.set_title("Criterio de Middlebrook: |Z_fuente| vs |Z_cpl|\n"
             "si el pico de Z_fuente supera |Z_cpl| -> inestable")
ax.legend(); ax.grid(True, which="both", alpha=.3)
fig.tight_layout()
outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(outdir, exist_ok=True)
fig.savefig(os.path.join(outdir, "fase2_middlebrook.png"), dpi=130)

Zpeak = np.abs(Zsrc).max()
P_lim = p.Vbus**2 / Zpeak
print("=" * 60); print("FASE 2 - Estabilidad del bus DC por impedancia"); print("=" * 60)
print(f"Pico de |Z_fuente| = {Zpeak:.3f} ohm (resonancia L-C)")
print(f"|Z_cpl| = V^2/P. Inestable cuando |Z_cpl| < pico  ->  P > V^2/pico = {P_lim/1e3:.0f} kW")
print(f"Coincide con la P_critica de Fase 1 ({p.Pcrit/1e3:.0f} kW).")
print("Figura: results/fase2_middlebrook.png")
