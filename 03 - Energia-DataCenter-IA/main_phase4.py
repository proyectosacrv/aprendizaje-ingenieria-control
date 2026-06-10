"""Fase 4: dimensionado del sistema ante el pico de carga de IA.

Dos requisitos independientes:
  - Lado DC (estabilidad CPL):  C_dc >= P_pico * L / (V^2 * R)   [de P_crit = V^2 R C / L]
  - Lado AC (RoCoF admisible):  H   >= dP * f0 / (2 * S * RoCoF_max)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from params import SystemParams

p = SystemParams()
fig, ax = plt.subplots(1, 2, figsize=(13, 5))

# --- Lado DC: condensador minimo vs pico de potencia ---
Ppico = np.linspace(50e3, 400e3, 100)
Cmin = Ppico * p.Lf / (p.Vbus**2 * p.Rf)          # C para que P_crit = P_pico
ax[0].plot(Ppico/1e3, Cmin*1e3, "C0", lw=2)
ax[0].fill_between(Ppico/1e3, Cmin*1e3, Cmin.max()*1e3*1.1, color="C0", alpha=0.10)
ax[0].set_xlabel("pico de carga CPL [kW]"); ax[0].set_ylabel("C_dc minimo [mF]")
ax[0].set_title("Lado DC: condensador minimo para estabilidad (CPL)\nzona segura por encima de la curva")
ax[0].grid(alpha=.3)

# --- Lado AC: inercia minima vs salto de potencia para un RoCoF admisible ---
dP = np.linspace(20e3, 300e3, 100)
for rocof_max, col in [(0.5, "C3"), (1.0, "C1"), (2.0, "C0")]:
    Hmin = dP * p.fac / (2 * p.Sac * rocof_max)
    ax[1].plot(dP/1e3, Hmin, col, label=f"RoCoF_max = {rocof_max} Hz/s")
ax[1].set_xlabel("salto de carga ΔP [kW]"); ax[1].set_ylabel("inercia H minima [s]")
ax[1].set_title("Lado AC: inercia minima del BESS para no superar el RoCoF\n(zona segura por encima)")
ax[1].legend(); ax[1].grid(alpha=.3)
fig.tight_layout()
outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(outdir, exist_ok=True)
fig.savefig(os.path.join(outdir, "fase4_dimensionado.png"), dpi=130)

print("=" * 60); print("FASE 4 - Dimensionado ante pico de carga de IA"); print("=" * 60)
print(f"Ejemplo: pico de 250 kW, salto dP=150 kW, RoCoF_max=1 Hz/s")
print(f"  C_dc minimo (DC)  = {250e3*p.Lf/(p.Vbus**2*p.Rf)*1e3:.1f} mF")
print(f"  H minima (AC)     = {150e3*p.fac/(2*p.Sac*1.0):.2f} s")
print("Regla: el lado DC fija C_dc por estabilidad CPL; el lado AC fija H por RoCoF.")
print("Figura: results/fase4_dimensionado.png")
