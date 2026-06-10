"""Modelo del sub-bus de distribucion DC con carga de potencia constante (CPL).

Bus principal rigido (V_bus, regulado por el AFE) -> cable (L_f, R_f) -> condensador del rack
(C_dc) -> CPL (servidores). El CPL aporta i_cpl = P_cpl/V_dc, cuya conductancia incremental es
NEGATIVA y desamortigua el filtro L-C.

Estados (2):
  0 iL    corriente de distribucion (cable) [A]
  1 Vdc   tension del rack (sub-bus de carga) [V]
Entrada u (1): i_pert  perturbacion de corriente en el nodo del rack (para impedancia).
Salida  y (1): Vdc.
"""
import numpy as np
from scipy.optimize import fsolve

STATE_NAMES = ["iL", "Vdc"]
NX = 2


class DCBus:
    def __init__(self, p):
        self.p = p

    def f(self, x, u):
        p = self.p
        iL, Vdc = x
        i_pert = u[0]
        Vdc_s = max(Vdc, 1.0)
        Rtot = p.Rf + p.Rd
        diL = (p.Vbus - Vdc - Rtot * iL) / p.Lf
        dVdc = (iL - p.Pcpl / Vdc_s + i_pert) / p.Cdc
        return np.array([diL, dVdc])

    def output(self, x, u):
        return np.array([x[1]])

    def equilibrium(self, u=None):
        if u is None:
            u = np.array([0.0])
        p = self.p
        x0 = np.array([p.Pcpl / p.Vbus, p.Vbus])
        x_eq, info, ier, msg = fsolve(lambda x: self.f(x, u), x0,
                                      full_output=True, xtol=1e-12)
        return x_eq, {"ier": ier, "residual": np.linalg.norm(self.f(x_eq, u))}

    def linearize(self, x_eq, u_eq, eps=1e-6):
        n, m, q = NX, len(u_eq), 1
        A = np.zeros((n, n)); B = np.zeros((n, m))
        C = np.zeros((q, n)); D = np.zeros((q, m))
        for j in range(n):
            dx = eps * max(1.0, abs(x_eq[j]))
            xp = x_eq.copy(); xp[j] += dx
            xm = x_eq.copy(); xm[j] -= dx
            A[:, j] = (self.f(xp, u_eq) - self.f(xm, u_eq)) / (2 * dx)
            C[:, j] = (self.output(xp, u_eq) - self.output(xm, u_eq)) / (2 * dx)
        for j in range(m):
            du = eps
            up = u_eq.copy(); up[j] += du
            um = u_eq.copy(); um[j] -= du
            B[:, j] = (self.f(x_eq, up) - self.f(x_eq, um)) / (2 * du)
            D[:, j] = (self.output(x_eq, up) - self.output(x_eq, um)) / (2 * du)
        return A, B, C, D
