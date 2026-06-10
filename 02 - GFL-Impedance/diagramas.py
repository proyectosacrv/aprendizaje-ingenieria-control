"""Genera los diagramas del proyecto GFL con schemdraw (offline):
  1) esquema_electrico.png  - circuito del modelo (VSC + LCL + red) [igual que el GFM: mismo hardware]
  2) diagrama_modelo.png    - bloques del modelo
  3) diagrama_control.png   - estrategia de control (PLL + lazo de corriente)
"""
import os
import matplotlib
matplotlib.use("Agg")
import schemdraw
import schemdraw.elements as elm
import schemdraw.dsp as dsp

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(OUT, exist_ok=True)


def esquema_electrico():
    d = schemdraw.Drawing(); d.config(unit=2.0, fontsize=11)
    d += elm.RBox(w=2.2, h=2.6).label("VSC\n2-niveles\nPWM\n$V_{dc}$=750V")
    d += elm.Line().right(0.5)
    d += elm.Inductor2().right().label("$L_1$ 2mH")
    d += elm.Resistor().right().label("$R_1$")
    d += elm.Dot().label("$v_C$", loc="top")
    d.push()
    d += elm.Capacitor().down().label("$C_f$\n20µF", loc="bottom"); d += elm.Ground()
    d.pop()
    d += elm.Line().right(0.4)
    d += elm.Inductor2().right().label("$L_2$ 1mH")
    d += elm.Resistor().right().label("$R_2$")
    d += elm.Dot().label("PCC", loc="top")
    d += elm.Inductor2().right().label("$L_g$ (red)")
    d += elm.Resistor().right().label("$R_g$")
    d += elm.SourceSin().down().label("red\n50 Hz", loc="bottom"); d += elm.Ground()
    d.save(os.path.join(OUT, "esquema_electrico.png"), dpi=150)


def diagrama_modelo():
    d = schemdraw.Drawing(); d.config(unit=1.0, fontsize=11)
    ctrl = d.add(dsp.Box(w=2.6, h=1.1).label("CONTROL GFL\n(PLL + corriente)"))
    d.add(dsp.Arrow().right(2).at(ctrl.E).label("$v_{inv}$", "top"))
    pl = d.add(dsp.Box(w=3.2, h=1.6).anchor("W").label("PLANTA LCL\n$L_1$–$C_f$–$L_2$\n(6 estados dq)"))
    d.add(dsp.Arrow().right(2.6).at(pl.E).label("$i_g$  (puerto $v_{pcc}$)", "top"))
    d.add(dsp.Box(w=2.0, h=1.1).anchor("W").label("RED\n$Z_{red}$ (SCR)"))
    d.add(dsp.Line().down(1.8).at(pl.S))
    d.add(dsp.Arrow().left().tox(ctrl.S).label("$v_C, i_{L1}$", "bottom"))
    d.add(dsp.Line().up(1.8).toy(ctrl.S))
    d.save(os.path.join(OUT, "diagrama_modelo.png"), dpi=150)


def diagrama_control():
    d = schemdraw.Drawing(); d.config(unit=0.9, fontsize=10.5)
    # cadena principal: referencias de corriente -> PI corriente -> VSC -> planta
    ref = d.add(dsp.Box(w=2.6, h=1.0).label("ref. corriente\n$i^*$ ← $P^*,Q^*$"))
    d.add(dsp.Arrow().right(1.3).at(ref.E))
    si = d.add(dsp.Sum().anchor("W"))
    d.add(dsp.Arrow().right(1.1).at(si.E))
    pii = d.add(dsp.Box(w=1.9, h=1.0).anchor("W").label("PI\ncorriente"))
    d.add(dsp.Arrow().right(1.2).at(pii.E).label("$v_{inv}$", "top"))
    pl = d.add(dsp.Box(w=2.1, h=1.2).anchor("W").label("PLANTA\nLCL"))
    d.add(dsp.Arrow().right(1.3).at(pl.E).label("$i_g$", "top"))
    # realimentacion de corriente (desde SSW para no cruzar con la PLL)
    d.add(dsp.Line().down(1.6).at(pl.SSW))
    d.add(dsp.Line().left().tox(si.S))
    d.add(dsp.Arrow().up().toy(si.S).label("$i_{L1}$", "right"))
    # PLL: mide v_C (desde SSE, baja) y devuelve theta,omega que define el marco dq
    d.add(dsp.Line().down(2.9).at(pl.SSE).label("$v_C$", "right"))
    pll = d.add(dsp.Box(w=2.6, h=1.0).anchor("N").label("PLL  ($v_{Cq}\\to 0$)"))
    d.add(dsp.Arrow().left(3.6).at(pll.W).label("$\\theta,\\omega$ → marco dq", "top"))
    d.save(os.path.join(OUT, "diagrama_control.png"), dpi=150)


if __name__ == "__main__":
    esquema_electrico(); print("esquema_electrico.png")
    diagrama_modelo(); print("diagrama_modelo.png")
    diagrama_control(); print("diagrama_control.png")
