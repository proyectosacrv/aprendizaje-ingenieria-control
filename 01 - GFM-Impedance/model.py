"""Modelo no lineal del inversor grid-forming en dq, equilibrio y linealizacion.

Marcos de referencia:
  - 's' (system): marco comun, gira a w0 constante. Es donde se define el puerto
    de red y donde se expresa la impedancia de salida.
  - 'c' (control): marco del inversor, gira a w_inv (fijada por el droop P-w).
  - delta = theta_c - theta_s  (acoplamiento de pequena senal del grid-forming).

Estados (13):
  0  iL1d   1  iL1q     corriente inductor lado inversor (marco c)
  2  vcd    3  vcq      tension condensador de filtro (marco c)
  4  iL2d   5  iL2q     corriente lado red = i_g (marco c)
  6  delta            angulo del marco de control
  7  Pm     8  Qm      potencia activa/reactiva filtrada
  9  xvd   10  xvq     integradores PI de tension
  11 xid   12  xiq     integradores PI de corriente

Entrada u (2):  [vpcc_sd, vpcc_sq]  tension de red en marco s.
Salida  y (2):  [i_g_sd, i_g_sq]    corriente inyectada a red en marco s.
"""
import numpy as np
from scipy.optimize import fsolve

STATE_NAMES = ["iL1d", "iL1q", "vcd", "vcq", "iL2d", "iL2q",
               "delta", "Pm", "Qm", "xvd", "xvq", "xid", "xiq",
               "iL2d_lp", "iL2q_lp"]
NX = len(STATE_NAMES)


class GFMInverter:
    def __init__(self, p, opts=None):
        self.p = p
        # Flags de diagnostico (default = comportamiento base)
        o = {"w_decouple": "wctrl",   # 'wctrl' usa w del droop, 'w0' usa w0 fijo
             "ff_load": False,         # feedforward de carga iL2 (desestabiliza: off)
             "active_damping": True}   # amortiguamiento activo LCL (corriente Cf)
        if opts:
            o.update(opts)
        self.o = o

    # ------------------------------------------------------------------ #
    def f(self, x, u):
        """Campo vectorial dx/dt = f(x,u)."""
        p = self.p
        (iL1d, iL1q, vcd, vcq, iL2d, iL2q,
         delta, Pm, Qm, xvd, xvq, xid, xiq,
         iL2d_lp, iL2q_lp) = x
        vpcc_sd, vpcc_sq = u

        # --- Droop P-w: frecuencia del inversor ---
        w = p.w0 + p.mp * (p.Pset - Pm)
        wd = p.w0 if self.o["w_decouple"] == "w0" else w   # w para desacoplos/planta
        ffl = 1.0 if self.o["ff_load"] else 0.0

        # --- Potencia medida en el punto de control (vc, i_g) ---
        P = 1.5 * (vcd * iL2d + vcq * iL2q)
        Q = 1.5 * (vcq * iL2d - vcd * iL2q)
        dPm = p.wf * (P - Pm)
        dQm = p.wf * (Q - Qm)

        # --- Droop Q-V: referencia de tension (alineada al eje d de 'c') ---
        Vref = p.V0 + p.nq * (p.Qset - Qm)
        # Impedancia virtual Zv = Rv + jXv (caida segun corriente de red, marco dq)
        # + resistencia virtual TRANSITORIA Rvt sobre la corriente filtrada paso-alto
        # (cero en DC: amortigua sin distorsionar el equilibrio)
        wht = 2 * np.pi * p.f_ht
        iL2d_hp = iL2d - iL2d_lp
        iL2q_hp = iL2q - iL2q_lp
        vvirt_d = p.Rv * iL2d - wd * p.Lv * iL2q + p.Rvt * iL2d_hp
        vvirt_q = p.Rv * iL2q + wd * p.Lv * iL2d + p.Rvt * iL2q_hp
        vcref_d = Vref - vvirt_d
        vcref_q = 0.0 - vvirt_q
        diL2d_lp = wht * (iL2d - iL2d_lp)
        diL2q_lp = wht * (iL2q - iL2q_lp)

        # --- Lazo de tension (PI) -> referencia de corriente de L1 ---
        ev_d = vcref_d - vcd
        ev_q = vcref_q - vcq
        dxvd, dxvq = ev_d, ev_q
        iL1ref_d = p.Kp_v * ev_d + p.Ki_v * xvd - wd * p.Cf * vcq + ffl * iL2d
        iL1ref_q = p.Kp_v * ev_q + p.Ki_v * xvq + wd * p.Cf * vcd + ffl * iL2q

        # --- Lazo de corriente (PI) -> tension de salida del puente ---
        ei_d = iL1ref_d - iL1d
        ei_q = iL1ref_q - iL1q
        dxid, dxiq = ei_d, ei_q
        vid = p.Kp_i * ei_d + p.Ki_i * xid - wd * p.L1 * iL1q + vcd
        viq = p.Kp_i * ei_q + p.Ki_i * xiq + wd * p.L1 * iL1d + vcq

        # --- Amortiguamiento activo LCL: resistencia virtual via corriente de Cf ---
        if self.o["active_damping"]:
            vid -= p.Kad * (iL1d - iL2d)
            viq -= p.Kad * (iL1q - iL2q)

        # --- Tension de red rotada al marco de control: vpcc_c = R(-delta) vpcc_s ---
        cd, sd = np.cos(delta), np.sin(delta)
        vpcc_cd = cd * vpcc_sd + sd * vpcc_sq
        vpcc_cq = -sd * vpcc_sd + cd * vpcc_sq

        # --- Planta LCL (marco c, girando a w) ---
        diL1d = (vid - vcd - p.R1 * iL1d + w * p.L1 * iL1q) / p.L1
        diL1q = (viq - vcq - p.R1 * iL1q - w * p.L1 * iL1d) / p.L1
        dvcd = (iL1d - iL2d + w * p.Cf * vcq) / p.Cf
        dvcq = (iL1q - iL2q - w * p.Cf * vcd) / p.Cf
        # Red Thevenin en serie (Lg,Rg): cuando son 0, puerto rigido (Fase 1/2)
        L2t = p.L2 + p.Lg
        R2t = p.R2 + p.Rg
        diL2d = (vcd - vpcc_cd - R2t * iL2d + w * L2t * iL2q) / L2t
        diL2q = (vcq - vpcc_cq - R2t * iL2q - w * L2t * iL2d) / L2t

        # --- Angulo del marco de control ---
        ddelta = w - p.w0          # la red 's' gira a w0

        return np.array([diL1d, diL1q, dvcd, dvcq, diL2d, diL2q,
                         ddelta, dPm, dQm, dxvd, dxvq, dxid, dxiq,
                         diL2d_lp, diL2q_lp])

    # ------------------------------------------------------------------ #
    def output(self, x, u):
        """Salida del puerto: corriente a red en marco s, i_g_s = R(delta) i_g_c."""
        delta = x[6]
        iL2d, iL2q = x[4], x[5]
        cd, sd = np.cos(delta), np.sin(delta)
        i_sd = cd * iL2d - sd * iL2q
        i_sq = sd * iL2d + cd * iL2q
        return np.array([i_sd, i_sq])

    # ------------------------------------------------------------------ #
    def equilibrium(self, u):
        """Resuelve f(x,u)=0. Devuelve (x_eq, info)."""
        p = self.p
        Vg = u[0]
        # Guess fisico a partir de la consigna de potencia
        iL2d0 = p.Pset / (1.5 * Vg)
        iL2q0 = -p.Qset / (1.5 * Vg)
        x0 = np.zeros(NX)
        x0[0] = iL2d0 - p.w0 * p.Cf * 0.0    # iL1d ~ iL2d
        x0[1] = iL2q0 + p.w0 * p.Cf * Vg     # iL1q ~ iL2q + corriente del Cf
        x0[2] = Vg                            # vcd
        x0[3] = 0.0                           # vcq
        x0[4] = iL2d0
        x0[5] = iL2q0
        x0[6] = 0.05                          # delta inicial
        x0[7] = p.Pset                        # Pm
        x0[8] = p.Qset                        # Qm
        x0[13] = iL2d0                        # iL2d_lp ~ iL2d
        x0[14] = iL2q0                        # iL2q_lp ~ iL2q

        x_eq, info, ier, msg = fsolve(lambda x: self.f(x, u), x0,
                                      full_output=True, xtol=1e-12)
        res = np.linalg.norm(self.f(x_eq, u))
        return x_eq, {"ier": ier, "msg": msg, "residual": res}

    # ------------------------------------------------------------------ #
    def linearize(self, x_eq, u_eq, eps=1e-6):
        """Linealizacion numerica (diferencias centradas) -> A,B,C,D."""
        n, m, q = NX, len(u_eq), 2
        A = np.zeros((n, n)); B = np.zeros((n, m))
        C = np.zeros((q, n)); D = np.zeros((q, m))

        f0 = self.f(x_eq, u_eq)
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
