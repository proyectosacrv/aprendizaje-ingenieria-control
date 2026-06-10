"""Parametros del sistema de energia de un data center de IA (bus DC + lado AC).

Escenario DC: el AFE regula el bus principal (rigido, V_bus). La carga llega por un tramo de
distribucion (cable L-R) hasta el condensador del rack (C_dc), y los POL de los servidores se
comportan como carga de potencia constante (CPL): i_cpl = P_cpl/V_dc.
El CPL presenta conductancia incremental NEGATIVA  d i_cpl/dV = -P_cpl/V^2 < 0, que desamortigua
el filtro L-C de distribucion -> inestabilidad por encima de una potencia critica.

Lado AC: BESS grid-forming (VSM) que sostiene la microrred ante el pico de carga de IA.
"""
from dataclasses import dataclass, field
import numpy as np


@dataclass
class SystemParams:
    # --- Bus DC: distribucion hasta el rack ---
    Vbus:  float = 800.0                        # tension del bus DC principal (regulada) [V]
    Lf:    float = 50e-6                        # inductancia de distribucion (cable) [H]
    Rf:    float = 0.005                        # resistencia de distribucion [ohm]
    Cdc:   float = 2e-3                         # condensador de entrada del rack [F]
    Rd:    float = 0.0                          # amortiguamiento (resistencia de damping) [ohm]

    # --- Carga CPL (servidores/GPUs via POL) ---
    Pcpl:  float = 150e3                        # potencia de la carga CPL [W]

    # --- Lado AC: BESS grid-forming (VSM) ---
    Sac:      float = 1.0e6                     # potencia del BESS [VA]
    fac:      float = 50.0
    H_vsm:    float = 3.0                       # constante de inercia del BESS [s]
    droop_ac: float = 0.02
    f_pac:    float = 10.0                      # filtro de potencia del BESS [Hz]
    Pac0:     float = 150e3                     # potencia AC inicial (= CPL nominal)

    # --- Derivados ---
    wac:  float = field(init=False)
    Jvsm: float = field(init=False)
    Dvsm: float = field(init=False)
    wpac: float = field(init=False)

    def __post_init__(self):
        self.wac = 2 * np.pi * self.fac
        self.Jvsm = 2 * self.H_vsm * self.Sac / self.wac**2
        mp = self.droop_ac * self.wac / self.Sac
        self.Dvsm = 1.0 / (self.wac * mp)
        self.wpac = 2 * np.pi * self.f_pac

    @property
    def Pcrit(self):
        """Potencia CPL critica del filtro L-C sin amortiguamiento activo (aprox.)."""
        return self.Vbus**2 * (self.Rf + self.Rd) * self.Cdc / self.Lf
