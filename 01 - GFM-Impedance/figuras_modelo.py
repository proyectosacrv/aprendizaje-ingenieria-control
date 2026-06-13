"""Figuras explicativas del MODELO (GFM): estructura de la matriz de estado A y
flujo de datos del codigo. Salida en results/ (estilo blanco, como el resto de figuras).

  python figuras_modelo.py
  -> results/matriz_A.png      (heatmap 15x15 de A con nombres de estado)
  -> results/flujo_codigo.png  (pipeline params -> model -> linealizacion -> analisis)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.dsp as dsp

from params import SystemParams
from model import GFMInverter, STATE_NAMES

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(OUT, exist_ok=True)

# limites de grupos de estados (indice donde empieza el siguiente bloque)
GRUPOS = [(0, 6, "LCL"), (6, 9, "droop/VSM"), (9, 11, "PI tensión"),
          (11, 13, "PI corriente"), (13, 15, "LPF Rv")]


def matriz_A():
    p = SystemParams(); gfm = GFMInverter(p)
    u = np.array([p.V0, 0.0]); x, _ = gfm.equilibrium(u)
    A, B, C, D = gfm.linearize(x, u)
    n = len(STATE_NAMES)
    # escala simetrica log: ver la ESTRUCTURA pese a magnitudes muy dispares
    M = np.sign(A) * np.log10(1.0 + np.abs(A))
    vmax = np.max(np.abs(M)) or 1.0

    fig, ax = plt.subplots(figsize=(7.8, 6.8))
    im = ax.imshow(M, cmap="RdBu_r", vmin=-vmax, vmax=vmax)
    ax.set_xticks(range(n)); ax.set_yticks(range(n))
    ax.set_xticklabels(STATE_NAMES, rotation=90, fontsize=8)
    ax.set_yticklabels(STATE_NAMES, fontsize=8)
    for s, e, _ in GRUPOS:                       # divisores de bloques
        if e < n:
            ax.axhline(e - 0.5, color="k", lw=0.9)
            ax.axvline(e - 0.5, color="k", lw=0.9)
    # etiqueta de cada grupo de filas a la izquierda
    for s, e, name in GRUPOS:
        ax.text(-2.2, (s + e - 1) / 2, name, rotation=90, va="center", ha="center",
                fontsize=8.5, color="#1f6feb")
    ax.set_title("Estructura de la matriz de estado A (15×15)\n"
                 "signo·log10(1+|A|) — rojo: acoplamiento +, azul: −, blanco: 0", fontsize=11)
    ax.set_xlabel("estado de origen (columna)  ·  fila = ecuación de la derivada")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "matriz_A.png"), dpi=140); plt.close(fig)
    print("matriz_A.png", A.shape)


def flujo_codigo():
    d = schemdraw.Drawing()
    d.config(unit=0.9, fontsize=10.5)
    params = d.add(dsp.Box(w=2.3, h=1.0).label("params.py\n(@dataclass)"))
    d.add(dsp.Arrow().right(1.3).at(params.E))
    modelo = d.add(dsp.Box(w=2.5, h=1.0).anchor("W").label("model.py\n$f(x,u)$ no lineal"))
    d.add(dsp.Arrow().right(1.3).at(modelo.E).label("$f$", "top"))
    equil = d.add(dsp.Box(w=2.3, h=1.0).anchor("W").label("equilibrium\n(fsolve)"))
    d.add(dsp.Arrow().right(1.3).at(equil.E).label("$x_{eq}$", "top"))
    lin = d.add(dsp.Box(w=2.6, h=1.0).anchor("W").label("linearize\nJacobiano →\n$A,B,C,D$"))
    # fan-out a los analisis
    d.add(dsp.Line().right(1.1).at(lin.E))
    j = d.add(dsp.Dot())
    for k, (dy, txt) in enumerate([(2.0, "eigvals → polos\n(Fase 1)"),
                                   (0.7, "impedancia $Z(j\\omega)$\n(Fase 2)"),
                                   (-0.7, "Nyquist gen.\n(Fase 3)"),
                                   (-2.0, "simulación temporal\n(Fases 4–5)")]):
        d.add(dsp.Line().at(j.center).up(dy) if dy > 0 else dsp.Line().at(j.center).down(-dy))
        b = d.add(dsp.Box(w=3.0, h=0.9).anchor("W").label(txt))
    d.save(os.path.join(OUT, "flujo_codigo.png"), dpi=140)
    print("flujo_codigo.png")


if __name__ == "__main__":
    matriz_A()
    flujo_codigo()
    print("--- figuras del modelo generadas en results/")
