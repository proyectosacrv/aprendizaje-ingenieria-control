"""Simulacion temporal del sistema hibrido AC+DC ante un pico de carga de IA.

Lado DC: cable L-R + condensador del rack C_dc + CPL (la carga de IA, pulsante).
Lado AC: BESS grid-forming (VSM) que suministra, vía el AFE, la potencia del rack. El AFE toma
del bus AC P_afe = V_bus * i_L; el BESS responde con su inercia (ecuacion de swing) -> la
frecuencia cae (RoCoF) y se recupera segun la inercia H.

Estados (4): iL, Vdc (DC) ; omega, Pm (AC, BESS VSM).
"""
import numpy as np
from scipy.integrate import solve_ivp


def rhs(t, X, p, pcpl_func, Jvsm):
    iL, Vdc, omega, Pm = X
    Pcpl = pcpl_func(t)
    Vdc_s = max(Vdc, 1.0)
    # --- lado DC ---
    diL = (p.Vbus - Vdc - (p.Rf + p.Rd) * iL) / p.Lf
    dVdc = (iL - Pcpl / Vdc_s) / p.Cdc
    # --- acoplamiento: potencia que el AFE toma del bus AC ---
    P_afe = p.Vbus * iL
    dPm = p.wpac * (P_afe - Pm)
    # --- lado AC: BESS grid-forming (ecuacion de swing del VSM) ---
    domega = ((p.Pac0 - Pm) / p.wac - p.Dvsm * (omega - p.wac)) / Jvsm
    return np.array([diL, dVdc, domega, dPm])


def run(p, pcpl_func, H=None, t_end=1.0):
    Jvsm = p.Jvsm if H is None else 2 * H * p.Sac / p.wac**2
    P0 = pcpl_func(0.0)
    X0 = np.array([P0 / p.Vbus, p.Vbus, p.wac, P0])
    sol = solve_ivp(rhs, (0, t_end), X0, args=(p, pcpl_func, Jvsm),
                    method="LSODA", rtol=1e-7, atol=1e-9, max_step=2e-4,
                    dense_output=True)
    return sol
