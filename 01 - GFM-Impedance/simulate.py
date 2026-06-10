"""Simulacion temporal no lineal: droop vs VSM y current limiting bajo falta.

Reutiliza la planta LCL + lazos internos del modelo, cambiando la capa externa de
sincronizacion (droop instantaneo vs ecuacion de swing del VSM) y anadiendo
saturacion de la referencia de corriente (current limiting).

Estado (16): los 15 del modelo + omega (frecuencia del VSM, estado 15).
"""
import numpy as np
from scipy.integrate import solve_ivp


def rhs(t, X, p, mode, ilim, pset_func, efunc):
    (iL1d, iL1q, vcd, vcq, iL2d, iL2q, delta, Pm, Qm,
     xvd, xvq, xid, xiq, iL2d_lp, iL2q_lp, omega) = X
    Pset = pset_func(t)
    Ed, Eq = efunc(t)                       # fem de red (marco s)

    # --- Capa externa: frecuencia ---
    if mode == "vsm":
        # ecuacion de swing: J w0 dw/dt = (Pset-P)/w0 - D (w-w0)
        dωdt = ((Pset - Pm) / p.w0 - p.Dvsm * (omega - p.w0)) / p.Jvsm
        w = omega
    else:  # droop
        w = p.w0 + p.mp * (Pset - Pm)
        dωdt = 0.0
    wd = w

    # --- Potencia medida y filtrada ---
    P = 1.5 * (vcd * iL2d + vcq * iL2q)
    Q = 1.5 * (vcq * iL2d - vcd * iL2q)
    dPm = p.wf * (P - Pm); dQm = p.wf * (Q - Qm)

    # --- Droop Q-V + impedancia virtual ---
    Vref = p.V0 + p.nq * (p.Qset - Qm)
    wht = 2 * np.pi * p.f_ht
    iL2d_hp = iL2d - iL2d_lp; iL2q_hp = iL2q - iL2q_lp
    vvirt_d = p.Rv * iL2d - wd * p.Lv * iL2q + p.Rvt * iL2d_hp
    vvirt_q = p.Rv * iL2q + wd * p.Lv * iL2d + p.Rvt * iL2q_hp
    vcref_d = Vref - vvirt_d; vcref_q = -vvirt_q
    diL2d_lp = wht * (iL2d - iL2d_lp); diL2q_lp = wht * (iL2q - iL2q_lp)

    # --- Lazo de tension -> referencia de corriente ---
    ev_d = vcref_d - vcd; ev_q = vcref_q - vcq
    dxvd, dxvq = ev_d, ev_q
    iL1ref_d = p.Kp_v * ev_d + p.Ki_v * xvd - wd * p.Cf * vcq
    iL1ref_q = p.Kp_v * ev_q + p.Ki_v * xvq + wd * p.Cf * vcd

    # --- CURRENT LIMITING: satura la magnitud de la referencia de corriente ---
    if ilim is not None:
        mag = np.hypot(iL1ref_d, iL1ref_q)
        if mag > ilim:
            s = ilim / mag
            iL1ref_d *= s; iL1ref_q *= s
            # anti-windup: congela integradores de tension al saturar
            dxvd = dxvq = 0.0

    # --- Lazo de corriente -> tension de puente + damping activo ---
    ei_d = iL1ref_d - iL1d; ei_q = iL1ref_q - iL1q
    dxid, dxiq = ei_d, ei_q
    vid = p.Kp_i * ei_d + p.Ki_i * xid - wd * p.L1 * iL1q + vcd - p.Kad * (iL1d - iL2d)
    viq = p.Kp_i * ei_q + p.Ki_i * xiq + wd * p.L1 * iL1d + vcq - p.Kad * (iL1q - iL2q)

    # --- Planta LCL + red Thevenin en serie ---
    cd, sd = np.cos(delta), np.sin(delta)
    vpcc_cd = cd * Ed + sd * Eq; vpcc_cq = -sd * Ed + cd * Eq
    L2t = p.L2 + p.Lg; R2t = p.R2 + p.Rg
    diL1d = (vid - vcd - p.R1 * iL1d + w * p.L1 * iL1q) / p.L1
    diL1q = (viq - vcq - p.R1 * iL1q - w * p.L1 * iL1d) / p.L1
    dvcd = (iL1d - iL2d + w * p.Cf * vcq) / p.Cf
    dvcq = (iL1q - iL2q - w * p.Cf * vcd) / p.Cf
    diL2d = (vcd - vpcc_cd - R2t * iL2d + w * L2t * iL2q) / L2t
    diL2q = (vcq - vpcc_cq - R2t * iL2q - w * L2t * iL2d) / L2t
    ddelta = w - p.w0

    return np.array([diL1d, diL1q, dvcd, dvcq, diL2d, diL2q, ddelta, dPm, dQm,
                     dxvd, dxvq, dxid, dxiq, diL2d_lp, diL2q_lp, dωdt])


def initial_state(p, mode):
    """Estado inicial en el equilibrio (via el modelo droop)."""
    from model import GFMInverter
    g = GFMInverter(p)
    x0, _ = g.equilibrium(np.array([p.V0, 0.0]))
    return np.append(x0, p.w0)             # omega inicial = w0


def run(p, mode="droop", ilim=None, pset_func=None, efunc=None, t_end=1.0):
    if pset_func is None:
        pset_func = lambda t: p.Pset
    if efunc is None:
        efunc = lambda t: (p.V0, 0.0)
    X0 = initial_state(p, mode)
    sol = solve_ivp(rhs, (0, t_end), X0, args=(p, mode, ilim, pset_func, efunc),
                    method="LSODA", rtol=1e-7, atol=1e-9, max_step=1e-3,
                    dense_output=True)
    return sol
