"""Red Thevenin en dq parametrizada por SCR y X/R."""
import numpy as np


def grid_params(scr, xr, p):
    """Devuelve (Rg, Lg) de la red para un SCR y X/R dados.
    SCR = S_cc/Sn,  S_cc = Vll^2/|Zg|  =>  |Zg| = Vll^2/(SCR*Sn).
    """
    Zg = p.Vll**2 / (scr * p.Sn)
    Rg = Zg / np.sqrt(1.0 + xr**2)
    Xg = Rg * xr
    Lg = Xg / p.w0
    return Rg, Lg


def grid_impedance_dq(Rg, Lg, w0, freqs_hz):
    """Z_grid(jw) en dq (2x2) de un inductor R+jX con acoplamiento cruzado w0*Lg."""
    Z = np.zeros((len(freqs_hz), 2, 2), dtype=complex)
    for k, f in enumerate(freqs_hz):
        s = 2j * np.pi * f
        Z[k] = np.array([[Rg + s * Lg, -w0 * Lg],
                         [w0 * Lg,      Rg + s * Lg]])
    return Z
