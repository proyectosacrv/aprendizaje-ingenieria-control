"""
Proyecto 04 - GFL/GFM Transicion
Modelo electrico del inversor con filtro LCL, opcion A (trafo y red colapsados en L2eq).
Espacio de estados 6x6 en marco dq.
"""

import numpy as np

# =============================================================================
# PARAMETROS DEL SISTEMA
# =============================================================================

# --- Red y frecuencia ---
f0     = 50.0                  # frecuencia de red (Hz)
omega0 = 2 * np.pi * f0        # frecuencia angular (rad/s)

# --- Bus DC ---
Vdc = 700.0                    # tension bus DC (V)

# --- Tension y potencia nominales ---
Vnom = 690.0                   # tension nominal AC linea a linea (V)
Snom = 4e6                     # potencia nominal (VA)

# --- Filtro LCL ---
L1  = 40e-6                    # inductancia lado inversor (H)
R1  = 0.7e-3                   # resistencia serie L1 (Ohm)
Cf  = 85e-6                    # condensador de filtro (F)
L2  = 8e-6                     # inductancia lado red (H)
R2  = 0.18e-3                  # resistencia serie L2 (Ohm)

# --- Transformador equivalente (690 V / 380 kV, Ucc=17%, X/R=18) ---
Rt  = 1.1e-3                   # resistencia trafo referida a 690 V (Ohm)
Lt  = 64e-6                    # inductancia trafo referida a 690 V (H)

# --- Red Thevenin referida a 690 V ---
# SCR 5: red fuerte (Rg y Lg despreciables)
Rg_scr5 = 0.0
Lg_scr5 = 0.0

# SCR 2: red debil
Rg_scr2 = 4.9e-3               # resistencia de red (Ohm)
Lg_scr2 = 124e-6               # inductancia de red (H)

# =============================================================================
# PARAMETROS EQUIVALENTES OPCION A (trafo + red colapsados en L2eq, R2eq)
# =============================================================================

def params_opcA(Rg, Lg):
    L2eq = L2 + Lt + Lg
    R2eq = R2 + Rt + Rg
    return L2eq, R2eq


L2eq_scr5, R2eq_scr5 = params_opcA(Rg_scr5, Lg_scr5)
L2eq_scr2, R2eq_scr2 = params_opcA(Rg_scr2, Lg_scr2)

# =============================================================================
# ESPACIO DE ESTADOS 6x6 EN DQ  (opcion A)
#
# Estados:  x = [iL1d, iL1q, vCd, vCq, iL2d, iL2q]
# Entradas: u = [vVSCd, vVSCq, vgd, vgq]
#
# Ecuaciones:
#   diL1d/dt = (vVSCd - R1*iL1d - vCd) / L1  + omega0*iL1q
#   diL1q/dt = (vVSCq - R1*iL1q - vCq) / L1  - omega0*iL1d
#   dvCd/dt  = (iL1d - iL2d) / Cf             + omega0*vCq
#   dvCq/dt  = (iL1q - iL2q) / Cf             - omega0*vCd
#   diL2d/dt = (vCd - R2eq*iL2d - vgd) / L2eq + omega0*iL2q
#   diL2q/dt = (vCq - R2eq*iL2q - vgq) / L2eq - omega0*iL2d
# =============================================================================

def matrices_AB(L2eq, R2eq):
    A = np.array([
        [-R1/L1,    omega0,   -1/L1,     0,       0,          0      ],
        [-omega0,  -R1/L1,    0,        -1/L1,    0,          0      ],
        [ 1/Cf,     0,        0,         omega0, -1/Cf,       0      ],
        [ 0,        1/Cf,    -omega0,    0,       0,          -1/Cf  ],
        [ 0,        0,        1/L2eq,    0,      -R2eq/L2eq,  omega0 ],
        [ 0,        0,        0,         1/L2eq, -omega0,    -R2eq/L2eq],
    ])

    B = np.array([
        [ 1/L1,   0,      0,        0      ],
        [ 0,      1/L1,   0,        0      ],
        [ 0,      0,      0,        0      ],
        [ 0,      0,      0,        0      ],
        [ 0,      0,     -1/L2eq,   0      ],
        [ 0,      0,      0,       -1/L2eq ],
    ])

    return A, B


# Matrices para cada caso de SCR
A_scr5, B_scr5 = matrices_AB(L2eq_scr5, R2eq_scr5)
A_scr2, B_scr2 = matrices_AB(L2eq_scr2, R2eq_scr2)

# =============================================================================
# VERIFICACION RAPIDA
# =============================================================================

if __name__ == "__main__":
    for nombre, A, L2eq in [("SCR 5", A_scr5, L2eq_scr5),
                             ("SCR 2", A_scr2, L2eq_scr2)]:
        eigs = np.linalg.eigvals(A)
        Leq  = L1 * L2eq / (L1 + L2eq)
        fres = 1 / (2 * np.pi * np.sqrt(Leq * Cf))
        print(f"\n--- {nombre} ---")
        print(f"  L2eq = {L2eq*1e6:.1f} uH    fres LCL = {fres:.1f} Hz")
        print(f"  Autovalores (parte real):")
        for ev in sorted(eigs, key=lambda e: e.imag):
            print(f"    {ev.real:+.2f}  +  {ev.imag:+.1f}j")
