"""Exporta los resultados numericos del proyecto GFM a CSV (carpeta datos/).

Pensado para analizar los resultados fuera del informe: abrir en Excel, pandas, etc.
    python exportar_datos.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from params import SystemParams
from model import GFMInverter, STATE_NAMES
from impedance import build_linear, impedance
from grid import grid_params

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos")
os.makedirs(OUT, exist_ok=True)

p = SystemParams()
g = GFMInverter(p)
u = np.array([p.V0, 0.0])
xeq, info = g.equilibrium(u)
A, B, C, D = g.linearize(xeq, u)

# 1) Punto de equilibrio (estado a estado)
P_eq = 1.5 * (xeq[2] * xeq[4] + xeq[3] * xeq[5])
Q_eq = 1.5 * (xeq[3] * xeq[4] - xeq[2] * xeq[5])
with open(os.path.join(OUT, "equilibrio.csv"), "w", encoding="utf-8") as f:
    f.write("estado,valor,unidad\n")
    units = ["A","A","V","V","A","A","rad","W","var","A.s","A.s","V.s","V.s","A","A"]
    for n, v, un in zip(STATE_NAMES, xeq, units):
        f.write(f"{n},{v:.6g},{un}\n")
    f.write(f"P_eq,{P_eq:.6g},W\nQ_eq,{Q_eq:.6g},var\nresidual,{info['residual']:.3e},-\n")

# 2) Autovalores (modos): re, im, frecuencia, amortiguamiento
ev = np.linalg.eigvals(A)
ev = ev[np.argsort(-ev.real)]
f_hz = np.abs(ev.imag) / (2 * np.pi)
zeta = -ev.real / np.abs(ev)
np.savetxt(os.path.join(OUT, "autovalores.csv"),
           np.column_stack([ev.real, ev.imag, f_hz, zeta]),
           delimiter=",", header="re_1/s,im_rad/s,f_Hz,zeta", comments="", fmt="%.6g")

# 3) Impedancia de salida dq vs frecuencia
fre = np.logspace(-1, np.log10(5e3), 600)
Z = impedance(A, B, C, D, fre)
np.savetxt(os.path.join(OUT, "impedancia_dq.csv"),
           np.column_stack([fre,
                            np.abs(Z[:, 0, 0]), np.degrees(np.angle(Z[:, 0, 0])),
                            np.abs(Z[:, 1, 1]), np.degrees(np.angle(Z[:, 1, 1])),
                            np.abs(Z[:, 0, 1]), np.abs(Z[:, 1, 0])]),
           delimiter=",",
           header="f_Hz,absZdd_ohm,angZdd_deg,absZqq_ohm,angZqq_deg,absZdq_ohm,absZqd_ohm",
           comments="", fmt="%.6g")

# 4) Barrido de SCR (control agresivo, como en la Fase 3): max Re del modelo acoplado
CFG = dict(droop_p=0.03, droop_q=0.05, Lv=2e-3, Rvt=0.0, Rv=0.0, f_cv=250)
scrs = np.linspace(2.0, 6.0, 80)
mr = []
for s in scrs:
    Rg, Lg = grid_params(s, 5.0, SystemParams(**CFG))
    pp = SystemParams(Rg=Rg, Lg=Lg, **CFG)
    gg = GFMInverter(pp)
    x, r = gg.equilibrium(np.array([pp.V0, 0.0]))
    mr.append(np.linalg.eigvals(gg.linearize(x, np.array([pp.V0, 0.0]))[0]).real.max()
              if r["residual"] < 1e-6 else np.nan)
np.savetxt(os.path.join(OUT, "scr_sweep.csv"),
           np.column_stack([scrs, mr]), delimiter=",",
           header="SCR,maxRe_1/s", comments="", fmt="%.6g")

print("Exportado a datos/:")
print("  equilibrio.csv     - punto de operacion (15 estados + P,Q,residual)")
print("  autovalores.csv    - 15 modos (re, im, f, zeta)")
print("  impedancia_dq.csv  - Z_dd,Z_qq,Z_dq,Z_qd vs frecuencia (600 puntos)")
print("  scr_sweep.csv      - max Re vs SCR (control agresivo)")
