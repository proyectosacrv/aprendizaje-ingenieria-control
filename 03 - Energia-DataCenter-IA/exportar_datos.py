"""Exporta los resultados numericos del proyecto DataCenter-IA a CSV (carpeta datos/).
    python exportar_datos.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from params import SystemParams
from model_dc import DCBus
import simulate as sim

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos")
os.makedirs(OUT, exist_ok=True)


def maxre(pcpl, cdc=2e-3, rd=0.0):
    p = SystemParams(Pcpl=pcpl, Cdc=cdc, Rd=rd)
    g = DCBus(p)
    x, _ = g.equilibrium()
    return np.linalg.eigvals(g.linearize(x, np.array([0.0]))[0]).real.max()

# 1) Estabilidad CPL: max Re vs P_cpl para varios C_dc
P = np.linspace(20e3, 350e3, 120)
cols = [P / 1e3]
hdr = ["Pcpl_kW"]
for cdc in (2e-3, 5e-3, 10e-3):
    cols.append([maxre(pp, cdc) for pp in P])
    hdr.append(f"maxRe_Cdc{int(cdc*1e3)}mF")
np.savetxt(os.path.join(OUT, "estabilidad_cpl.csv"),
           np.column_stack(cols), delimiter=",", header=",".join(hdr),
           comments="", fmt="%.6g")

# 2) Impedancia de salida de la fuente (filtro L-C sin CPL) vs frecuencia
pf = SystemParams(Pcpl=0.0)
g = DCBus(pf)
x, _ = g.equilibrium()
A, B, C, D = g.linearize(x, np.array([0.0]))
fre = np.logspace(1, 4.5, 800)
I = np.eye(A.shape[0])
Zsrc = np.array([(C @ np.linalg.solve(2j * np.pi * ff * I - A, B) + D)[0, 0] for ff in fre])
np.savetxt(os.path.join(OUT, "impedancia_fuente.csv"),
           np.column_stack([fre, np.abs(Zsrc)]), delimiter=",",
           header="f_Hz,absZfuente_ohm", comments="", fmt="%.6g")

# 3) Pico de carga: frecuencia AC vs tiempo para varias inercias H
p = SystemParams(Cdc=8e-3)
pcpl = lambda t: 100e3 if t < 0.1 else 230e3
tt = np.linspace(0, 1.0, 2000)
cols = [tt]
hdr = ["t_s"]
for H in (1.0, 3.0, 6.0):
    s = sim.run(p, pcpl, H=H, t_end=1.0)
    cols.append(s.sol(tt)[2] / (2 * np.pi))
    hdr.append(f"f_Hz_H{int(H)}s")
np.savetxt(os.path.join(OUT, "pico_frecuencia.csv"),
           np.column_stack(cols), delimiter=",", header=",".join(hdr),
           comments="", fmt="%.6g")

# 4) Pico de carga: tension del bus DC vs tiempo para varios C_dc
cols = [tt]
hdr = ["t_s"]
for cdc in (4e-3, 8e-3, 16e-3):
    s = sim.run(SystemParams(Cdc=cdc), pcpl, H=3.0, t_end=1.0)
    cols.append(s.sol(tt)[1])
    hdr.append(f"Vdc_V_Cdc{int(cdc*1e3)}mF")
np.savetxt(os.path.join(OUT, "pico_tension_dc.csv"),
           np.column_stack(cols), delimiter=",", header=",".join(hdr),
           comments="", fmt="%.6g")

print("Exportado a datos/:")
print("  estabilidad_cpl.csv   - max Re vs P_cpl para Cdc=2/5/10 mF")
print("  impedancia_fuente.csv - |Z_fuente| vs frecuencia")
print("  pico_frecuencia.csv   - f(t) ante el pico, H=1/3/6 s")
print("  pico_tension_dc.csv   - Vdc(t) ante el pico, Cdc=4/8/16 mF")
