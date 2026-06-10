"""Medicion de impedancia de salida dq por inyeccion de perturbacion.

Esta es la tecnica que se programa en PLECS o en un banco de ensayo real:
  1. En el punto de operacion, inyectar una pequena perturbacion senoidal de tension
     en el puerto, a frecuencia f_p, primero en el eje d y luego en el eje q.
  2. Simular hasta regimen permanente y medir v_pcc(t) e i_g(t).
  3. Extraer los fasores a f_p por demodulacion (correlacion con sin/cos sobre
     periodos enteros).
  4. Como es un sistema MIMO 2x2, dos inyecciones independientes (d y q) permiten
     identificar la matriz completa:  I = G * V  ->  G = I * V^-1.
     Admitancia de salida Y = -G ;  Z = Y^-1.

Aqui la "planta" es el modelo no lineal (simulate.rhs). Comparar el Z medido con el
Z analitico (impedance.py) valida la linealizacion y demuestra el metodo.
"""
import numpy as np
from scipy.integrate import solve_ivp
from simulate import rhs, initial_state


def _phasor(t, x, fp):
    """Fasor complejo de x(t) a frecuencia fp, por correlacion sobre la ventana.
    La ventana debe cubrir un numero entero de periodos para exactitud."""
    w = 2 * np.pi * fp
    # coeficientes de Fourier (proyeccion ortogonal)
    c = np.trapz(x * np.cos(w * t), t)
    s = np.trapz(x * np.sin(w * t), t)
    T = t[-1] - t[0]
    return (2.0 / T) * (c - 1j * s)


def measure_point(p, fp, amp, axis, n_settle=8, n_meas=6, ilim=None):
    """Una inyeccion a frecuencia fp en 'd' o 'q'. Devuelve fasores (Vd,Vq,Id,Iq)."""
    V0 = p.V0
    w = 2 * np.pi * fp

    def efunc(t):
        d = amp * np.sin(w * t) if axis == "d" else 0.0
        q = amp * np.sin(w * t) if axis == "q" else 0.0
        return (V0 + d, q)

    Tp = 1.0 / fp
    t_settle = n_settle * Tp
    t_end = t_settle + n_meas * Tp
    X0 = initial_state(p, "droop")
    # paso maximo: resolver bien tanto fp como la dinamica del control
    mstep = min(Tp / 40.0, 2e-4)
    # malla de medicion (periodos enteros tras el asentamiento); se pasa como t_eval
    # en vez de dense_output para acotar memoria cuando la saturacion crea pasos minimos
    tm = np.linspace(t_settle, t_end, int(n_meas * 200) + 1)
    sol = solve_ivp(rhs, (0, t_end), X0,
                    args=(p, "droop", ilim, lambda t: p.Pset, efunc),
                    method="LSODA", rtol=1e-8, atol=1e-10, max_step=mstep,
                    t_eval=tm)
    Xm = sol.y
    # tension de puerto real y corriente inyectada (marco s)
    vd = V0 + (amp * np.sin(w * tm) if axis == "d" else 0.0 * tm)
    vq = (amp * np.sin(w * tm) if axis == "q" else 0.0 * tm)
    delta = Xm[6]
    iL2d, iL2q = Xm[4], Xm[5]
    # i_g en marco s = R(delta) i_g_c
    igd = np.cos(delta) * iL2d - np.sin(delta) * iL2q
    igq = np.sin(delta) * iL2d + np.cos(delta) * iL2q

    return (_phasor(tm, vd, fp), _phasor(tm, vq, fp),
            _phasor(tm, igd, fp), _phasor(tm, igq, fp))


def measure_Z(p, freqs, amp=2.0, ilim=None):
    """Barrido: devuelve Z_medida (N,2,2) por inyeccion d y q en cada frecuencia."""
    Z = np.zeros((len(freqs), 2, 2), dtype=complex)
    for k, fp in enumerate(freqs):
        Vd1, Vq1, Id1, Iq1 = measure_point(p, fp, amp, "d", ilim=ilim)
        Vd2, Vq2, Id2, Iq2 = measure_point(p, fp, amp, "q", ilim=ilim)
        V = np.array([[Vd1, Vd2], [Vq1, Vq2]])
        I = np.array([[Id1, Id2], [Iq1, Iq2]])
        G = I @ np.linalg.inv(V)          # d i_g / d v_pcc
        Y = -G
        Z[k] = np.linalg.inv(Y)
    return Z
