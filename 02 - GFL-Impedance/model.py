"""Modelo no lineal del inversor grid-following (GFL) en dq, equilibrio y linealizacion.

Hardware: mismo filtro LCL que el GFM. Control:
  - PLL (SRF-PLL) sobre v_C: lleva v_Cq -> 0, alineando el marco de control con la tension.
    El angulo del marco de control lo fija la PLL (NO el droop).
  - Lazo de corriente PI sobre i_L1 con referencias desde P*,Q* (fuente de corriente).
  - Amortiguamiento activo del LCL.

Marcos: 's' (red, gira a w0) y 'c' (control = PLL, gira a w_pll). delta = theta_pll - theta_s.

Estados (10):
  0 iL1d 1 iL1q   2 vcd 3 vcq   4 iL2d 5 iL2q
  6 delta   7 eps (integrador PLL)   8 gd 9 gq (integradores PI de corriente)

Entrada u (2): [vpcc_sd, vpcc_sq] fem de red en marco s.
Salida  y (2): [i_g_sd, i_g_sq]   corriente inyectada en marco s (= i_L2 rotada).
"""
import numpy as np
from scipy.optimize import fsolve

STATE_NAMES = ["iL1d", "iL1q", "vcd", "vcq", "iL2d", "iL2q",
               "delta", "eps", "gd", "gq"]
NX = len(STATE_NAMES)


class GFLInverter:
    def __init__(self, p, opts=None):
        self.p = p
        o = {"active_damping": True}
        if opts:
            o.update(opts)
        self.o = o

    def f(self, x, u):
        p = self.p
        (iL1d, iL1q, vcd, vcq, iL2d, iL2q, delta, eps, gd, gq) = x
        vpcc_sd, vpcc_sq = u

        # --- PLL: bloquea v_Cq -> 0; fija la frecuencia del marco de control ---
        w = p.w0 + p.Kp_pll * vcq + p.Ki_pll * eps
        deps = vcq
        ddelta = w - p.w0

        # --- Referencias de corriente desde P,Q (fuente de corriente) ---
        # con la PLL alineando v_C al eje d, id<->P, iq<->Q
        vmag = max(vcd, 1.0)
        iL1d_ref = 2.0 * p.Pset / (3.0 * vmag)
        iL1q_ref = -2.0 * p.Qset / (3.0 * vmag)

        # --- Lazo de corriente PI (sobre i_L1) con desacoplo + feedforward de v_C ---
        e_d = iL1d_ref - iL1d
        e_q = iL1q_ref - iL1q
        dgd, dgq = e_d, e_q
        vid = p.Kp_i * e_d + p.Ki_i * gd - w * p.L1 * iL1q + vcd
        viq = p.Kp_i * e_q + p.Ki_i * gq + w * p.L1 * iL1d + vcq
        if self.o["active_damping"]:
            vid -= p.Kad * (iL1d - iL2d)
            viq -= p.Kad * (iL1q - iL2q)

        # --- Tension de red en marco de control: vpcc_c = R(-delta) vpcc_s ---
        cd, sd = np.cos(delta), np.sin(delta)
        vpcc_cd = cd * vpcc_sd + sd * vpcc_sq
        vpcc_cq = -sd * vpcc_sd + cd * vpcc_sq

        # --- Planta LCL (marco c a w) + red Thevenin en serie ---
        L2t = p.L2 + p.Lg
        R2t = p.R2 + p.Rg
        diL1d = (vid - vcd - p.R1 * iL1d + w * p.L1 * iL1q) / p.L1
        diL1q = (viq - vcq - p.R1 * iL1q - w * p.L1 * iL1d) / p.L1
        dvcd = (iL1d - iL2d + w * p.Cf * vcq) / p.Cf
        dvcq = (iL1q - iL2q - w * p.Cf * vcd) / p.Cf
        diL2d = (vcd - vpcc_cd - R2t * iL2d + w * L2t * iL2q) / L2t
        diL2q = (vcq - vpcc_cq - R2t * iL2q - w * L2t * iL2d) / L2t

        return np.array([diL1d, diL1q, dvcd, dvcq, diL2d, diL2q,
                         ddelta, deps, dgd, dgq])

    def output(self, x, u):
        delta = x[6]; iL2d, iL2q = x[4], x[5]
        cd, sd = np.cos(delta), np.sin(delta)
        return np.array([cd * iL2d - sd * iL2q, sd * iL2d + cd * iL2q])

    def equilibrium(self, u):
        p = self.p
        Vg = u[0]
        iL2d0 = p.Pset / (1.5 * Vg)
        iL2q0 = -p.Qset / (1.5 * Vg)
        x0 = np.zeros(NX)
        x0[0] = iL2d0; x0[1] = iL2q0 + p.w0 * p.Cf * Vg
        x0[2] = Vg; x0[3] = 0.0
        x0[4] = iL2d0; x0[5] = iL2q0
        x_eq, info, ier, msg = fsolve(lambda x: self.f(x, u), x0,
                                      full_output=True, xtol=1e-12)
        return x_eq, {"ier": ier, "msg": msg, "residual": np.linalg.norm(self.f(x_eq, u))}

    def linearize(self, x_eq, u_eq, eps=1e-6):
        n, m, q = NX, len(u_eq), 2
        A = np.zeros((n, n)); B = np.zeros((n, m))
        C = np.zeros((q, n)); D = np.zeros((q, m))
        for j in range(n):
            dx = eps * max(1.0, abs(x_eq[j]))
            xp = x_eq.copy(); xp[j] += dx
            xm = x_eq.copy(); xm[j] -= dx
            A[:, j] = (self.f(xp, u_eq) - self.f(xm, u_eq)) / (2 * dx)
            C[:, j] = (self.output(xp, u_eq) - self.output(xm, u_eq)) / (2 * dx)
        for j in range(m):
            du = eps * max(1.0, abs(u_eq[j]))
            up = u_eq.copy(); up[j] += du
            um = u_eq.copy(); um[j] -= du
            B[:, j] = (self.f(x_eq, up) - self.f(x_eq, um)) / (2 * du)
            D[:, j] = (self.output(x_eq, up) - self.output(x_eq, um)) / (2 * du)
        return A, B, C, D
