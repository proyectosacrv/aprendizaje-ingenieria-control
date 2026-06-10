"""Parametros del inversor grid-forming y de la red.

Convenio: marco dq con amplitud de PICO de fase (no RMS).
Potencia trifasica: P = 1.5*(vd*id + vq*iq), Q = 1.5*(vq*id - vd*iq).
"""
from dataclasses import dataclass, field
import numpy as np


@dataclass
class SystemParams:
    # --- Nominales ---
    Sn:    float = 10e3                       # potencia aparente nominal [VA]
    Vll:   float = 400.0                      # tension de linea RMS [V]
    f0:    float = 50.0                       # frecuencia nominal [Hz]

    # --- Filtro LCL ---
    L1:    float = 2.0e-3                      # inductancia lado inversor [H]
    R1:    float = 0.10                        # resistencia L1 [ohm]
    Cf:    float = 20.0e-6                     # condensador de filtro [F]
    L2:    float = 1.0e-3                      # inductancia lado red [H]
    R2:    float = 0.05                        # resistencia L2 [ohm]
    Lg:    float = 0.0                          # inductancia de red Thevenin [H] (0=puerto rigido)
    Rg:    float = 0.0                          # resistencia de red Thevenin [ohm]

    # --- Lazo de corriente (PI, sobre i_L1) ---
    f_ci:  float = 1000.0                      # ancho de banda objetivo [Hz]
    Kad:   float = 6.0                          # ganancia amortiguamiento activo LCL [ohm]
    Rv:    float = 0.2                           # resistencia virtual estatica [ohm]
    Lv:    float = 8.0e-3                         # inductancia virtual [H] (Xv~0.16 pu)
    Rvt:   float = 2.0                            # resistencia virtual TRANSITORIA [ohm]
    f_ht:  float = 4.0                            # corte del HPF de la Rv transitoria [Hz]
    # --- Lazo de tension (PI, sobre v_C) ---
    f_cv:  float = 350.0                       # ancho de banda objetivo [Hz]

    # --- Droop ---
    droop_p: float = 0.005                     # caida de frecuencia a Sn (p.u.) -> 0.5%
    droop_q: float = 0.02                      # caida de tension a Sn (p.u.)   -> 2%
    f_pow:   float = 15.0                      # corte del filtro de potencia [Hz]
    H_vsm:   float = 4.0                        # constante de inercia VSM [s]

    # --- Punto de operacion ---
    Pset:  float = 5.0e3                        # consigna de potencia activa [W]
    Qset:  float = 0.0                          # consigna de potencia reactiva [var]

    # --- Derivados (se calculan en __post_init__) ---
    w0:    float = field(init=False)
    V0:    float = field(init=False)            # pico de fase nominal [V]
    Kp_i:  float = field(init=False)
    Ki_i:  float = field(init=False)
    Kp_v:  float = field(init=False)
    Ki_v:  float = field(init=False)
    mp:    float = field(init=False)            # ganancia droop P-w [(rad/s)/W]
    nq:    float = field(init=False)            # ganancia droop Q-V [V/var]
    wf:    float = field(init=False)            # corte filtro potencia [rad/s]
    Jvsm:  float = field(init=False)            # inercia VSM [kg m2 equiv]
    Dvsm:  float = field(init=False)            # damping VSM

    def __post_init__(self):
        self.w0 = 2 * np.pi * self.f0
        self.V0 = self.Vll * np.sqrt(2.0 / 3.0)         # pico de fase

        # PI corriente: ancho de banda f_ci, cero que cancela el polo de planta R1/L1
        wci = 2 * np.pi * self.f_ci
        self.Kp_i = self.L1 * wci
        self.Ki_i = self.R1 * wci

        # PI tension: ancho de banda f_cv
        wcv = 2 * np.pi * self.f_cv
        self.Kp_v = self.Cf * wcv
        self.Ki_v = self.Cf * wcv * (wcv / 5.0)

        # Droop
        self.mp = (self.droop_p * self.w0) / self.Sn
        self.nq = (self.droop_q * self.V0) / self.Sn
        self.wf = 2 * np.pi * self.f_pow

        # VSM: inercia desde H y damping ajustado para igualar el droop estacionario
        self.Jvsm = 2 * self.H_vsm * self.Sn / self.w0**2
        self.Dvsm = 1.0 / (self.w0 * self.mp)
