"""Demostracion del principio de promediado: PWM conmutado vs modelo promediado.

Justifica por que todo el proyecto usa el modelo PROMEDIADO (tension de puente continua):
la conmutacion solo anade rizado de alta frecuencia que el filtro atenua; la dinamica de
baja frecuencia (la que controla el grid-forming) es la misma. Esto es lo que PLECS
simula en detalle y lo que el modelo promediado aproxima.

Modelo por fase: puente 2 niveles (+-Vdc/2) -> filtro L-C -> carga.
Se compara la tension del condensador con tension de puente CONMUTADA vs PROMEDIADA.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from params import SystemParams

p = SystemParams()
Vdc = 750.0
fsw = 10e3                      # frecuencia de conmutacion
f0 = p.f0
M = 0.85                        # indice de modulacion
Rload = p.V0 / (p.Sn / (1.5 * p.V0))   # carga ~ nominal
L, R, C = p.L1, p.R1, p.Cf

dt = 2e-7                       # paso fino para resolver la conmutacion
T = 2.0 / f0                    # 2 periodos de red
n = int(T / dt)
t = np.arange(n) * dt

def carrier(tt):               # portadora triangular [-1,1] a fsw
    ph = (tt * fsw) % 1.0
    return 2 * np.abs(2 * ph - 1) - 1

m = M * np.sin(2 * np.pi * f0 * t)          # modulante
v_sw = np.where(m > carrier(t), Vdc / 2, -Vdc / 2)   # tension conmutada
v_avg = (Vdc / 2) * m                        # tension promediada (modelo)

def integrate(vbridge):
    iL = np.zeros(n); vc = np.zeros(n)
    for k in range(n - 1):
        diL = (vbridge[k] - vc[k] - R * iL[k]) / L
        dvc = (iL[k] - vc[k] / Rload) / C
        iL[k+1] = iL[k] + dt * diL
        vc[k+1] = vc[k] + dt * dvc
    return iL, vc

iL_sw, vc_sw = integrate(v_sw)
iL_av, vc_av = integrate(v_avg)

# rizado de conmutacion = componente de alta frecuencia (conmutado - promediado)
half = slice(n // 2, n)
rizado_pp = (vc_sw[half] - vc_av[half]).max() - (vc_sw[half] - vc_av[half]).min()
fund_amp = vc_av[half].max()                      # amplitud de pico de la fundamental
print(f"fsw={fsw/1e3:.0f} kHz, filtro L1={L*1e3:.1f}mH Cf={C*1e6:.0f}uF")
print(f"amplitud fundamental vc  = {fund_amp:.1f} V (pico)")
print(f"rizado de conmutacion (pp) = {rizado_pp:.2f} V  ({100*rizado_pp/fund_amp:.2f} % de la fundamental)")
err = np.sqrt(np.mean((vc_sw[half] - vc_av[half])**2)) / np.sqrt(np.mean(vc_av[half]**2))
print(f"RMS(conmutado-promediado)/RMS(fundamental) = {100*err:.2f} %")
print("-> la dinamica util (fundamental) es identica; el promediado es valido.")

fig, ax = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
ax[0].plot(t*1e3, v_sw, color="0.7", lw=0.5, label="puente conmutado")
ax[0].plot(t*1e3, v_avg, "C3", lw=1.5, label="promediado (modelo)")
ax[0].set_ylabel("v_puente [V]"); ax[0].legend(loc="upper right"); ax[0].grid(alpha=0.3)
ax[0].set_title("Principio de promediado: conmutado vs modelo promediado")
ax[1].plot(t*1e3, vc_sw, color="0.6", lw=0.6, label="vc (conmutado)")
ax[1].plot(t*1e3, vc_av, "C0", lw=1.5, label="vc (promediado)")
ax[1].set_ylabel("v_C [V]"); ax[1].set_xlabel("t [ms]"); ax[1].legend(); ax[1].grid(alpha=0.3)
fig.tight_layout()
outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(outdir, exist_ok=True)
fig.savefig(os.path.join(outdir, "fase4b_averaging.png"), dpi=130)
print("Figura: results/fase4b_averaging.png")
