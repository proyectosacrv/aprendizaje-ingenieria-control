"""Impedancia/admitancia de salida dq del inversor a partir del modelo linealizado.

Convencion de signos:
  El modelo tiene  u = v_pcc (tension impuesta en el puerto, marco s)
                   y = i_g   (corriente inyectada hacia la red, marco s)
  G(s) = C(sI-A)^-1 B + D = d i_g / d v_pcc.
  Vista de fuente (Norton):  i_g = i_auto - Y_inv * v_pcc  =>  Y_inv = -G(s).
  Impedancia de salida:      Z_inv(s) = Y_inv(s)^-1   (matriz 2x2 en dq).
"""
import numpy as np
from params import SystemParams
from model import GFLInverter as GFMInverter   # alias: misma interfaz que el GFM


def build_linear(p, opts=None):
    """Construye (A,B,C,D, x_eq) en el punto de operacion nominal."""
    g = GFMInverter(p, opts)
    u = np.array([p.V0, 0.0])
    x_eq, info = g.equilibrium(u)
    if info["residual"] > 1e-6:
        raise RuntimeError(f"equilibrio no converge (res={info['residual']:.1e})")
    A, B, C, D = g.linearize(x_eq, u)
    return A, B, C, D, x_eq


def admittance(A, B, C, D, freqs_hz):
    """Y_inv(jw) para cada frecuencia [Hz]. Devuelve array (N,2,2) complejo."""
    n = A.shape[0]
    I = np.eye(n)
    Y = np.zeros((len(freqs_hz), 2, 2), dtype=complex)
    for k, f in enumerate(freqs_hz):
        s = 2j * np.pi * f
        G = C @ np.linalg.solve(s * I - A, B) + D      # d i_g / d v_pcc
        Y[k] = -G                                       # admitancia de salida
    return Y


def impedance(A, B, C, D, freqs_hz):
    """Z_inv(jw) = Y_inv(jw)^-1. Devuelve array (N,2,2) complejo."""
    Y = admittance(A, B, C, D, freqs_hz)
    Z = np.zeros_like(Y)
    for k in range(len(freqs_hz)):
        Z[k] = np.linalg.inv(Y[k])
    return Z


if __name__ == "__main__":
    p = SystemParams()
    A, B, C, D, _ = build_linear(p)
    f = np.array([1.0, 10.0, 100.0, 1000.0])
    Z = impedance(A, B, C, D, f)
    print("Z_dd(jw) (magnitud ohm) en 1/10/100/1000 Hz:")
    for k, ff in enumerate(f):
        print(f"  {ff:6.0f} Hz: |Zdd|={abs(Z[k,0,0]):7.3f}  |Zqq|={abs(Z[k,1,1]):7.3f}")
