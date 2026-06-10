"""Parametros del inversor grid-following (GFL) y de la red.

Mismo filtro LCL que el proyecto GFM (01) para una comparacion justa: cambia la capa de
control (PLL + lazo de corriente) no el hardware.
Convenio dq con amplitud de PICO de fase. P = 1.5(vd id + vq iq), Q = 1.5(vq id - vd iq).
"""
from dataclasses import dataclass, field
import numpy as np


@dataclass
class SystemParams:
    # --- Nominales ---
    Sn:    float = 10e3
    Vll:   float = 400.0
    f0:    float = 50.0

    # --- Filtro LCL (igual que GFM) ---
    L1:    float = 2.0e-3
    R1:    float = 0.10
    Cf:    float = 20.0e-6
    L2:    float = 1.0e-3
    R2:    float = 0.05
    Lg:    float = 0.0                          # red Thevenin (0 = puerto rigido)
    Rg:    float = 0.0

    # --- Lazo de corriente (PI sobre i_L1) ---
    f_ci:  float = 800.0                        # ancho de banda [Hz]
    Kad:   float = 6.0                          # amortiguamiento activo LCL [ohm]

    # --- PLL (SRF-PLL sobre v_C) ---
    f_pll: float = 30.0                         # ancho de banda de la PLL [Hz]
    zeta_pll: float = 0.707

    # --- Punto de operacion (referencias de corriente desde P,Q) ---
    Pset:  float = 5.0e3
    Qset:  float = 0.0

    # --- Derivados ---
    w0:    float = field(init=False)
    V0:    float = field(init=False)
    Kp_i:  float = field(init=False)
    Ki_i:  float = field(init=False)
    Kp_pll: float = field(init=False)
    Ki_pll: float = field(init=False)

    def __post_init__(self):
        self.w0 = 2 * np.pi * self.f0
        self.V0 = self.Vll * np.sqrt(2.0 / 3.0)
        wci = 2 * np.pi * self.f_ci
        self.Kp_i = self.L1 * wci
        self.Ki_i = self.R1 * wci
        # SRF-PLL: 2o orden con wn, zeta; la senal v_q ~ V0*sin(dtheta) ~ V0*dtheta
        wn = 2 * np.pi * self.f_pll
        self.Ki_pll = wn**2 / self.V0
        self.Kp_pll = 2 * self.zeta_pll * wn / self.V0
