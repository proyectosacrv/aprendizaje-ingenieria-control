"""Genera los diagramas del proyecto GFM con schemdraw (offline, SVG/PNG):
  1) esquema_electrico.png  - circuito del modelo (VSC + LCL + red)
  2) diagrama_modelo.png    - bloques del modelo (planta + marcos dq)
  3) diagrama_control.png   - estrategia de control (droop + cascada + Z virtual)
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
    d = schemdraw.Drawing()
    d.config(unit=2.0, fontsize=11)
    d += elm.RBox(w=2.2, h=2.6).label("VSC\n2-niveles\nPWM\n$V_{dc}$=750V")
    d += elm.Line().right(0.5)
    d += elm.Inductor2().right().label("$L_1$ 2mH")
    d += elm.Resistor().right().label("$R_1$")
    d += elm.Dot().label("$v_C$", loc="top")
    d.push()                                   # ramal del condensador
    d += elm.Capacitor().down().label("$C_f$\n20µF", loc="bottom")
    d += elm.Ground()
    d.pop()
    d += elm.Line().right(0.4)
    d += elm.Inductor2().right().label("$L_2$ 1mH")
    d += elm.Resistor().right().label("$R_2$")
    d += elm.Dot().label("PCC", loc="top")
    d += elm.Inductor2().right().label("$L_g$ (red)")
    d += elm.Resistor().right().label("$R_g$")
    d += elm.SourceSin().down().label("red\n50 Hz", loc="bottom")
    d += elm.Ground()
    d.save(os.path.join(OUT, "esquema_electrico.png"), dpi=150)


def diagrama_modelo():
    d = schemdraw.Drawing()
    d.config(unit=1.0, fontsize=11)
    ctrl = d.add(dsp.Box(w=2.4, h=1.1).label("CONTROL\n(marco dq)"))
    d.add(dsp.Arrow().right(2).at(ctrl.E).label("$v_{inv}$", "top"))
    pl = d.add(dsp.Box(w=3.2, h=1.6).anchor("W").label("PLANTA LCL\n$L_1$–$C_f$–$L_2$\n(6 estados dq)"))
    d.add(dsp.Arrow().right(2.6).at(pl.E).label("$i_g$  (puerto $v_{pcc}$)", "top"))
    d.add(dsp.Box(w=2.0, h=1.1).anchor("W").label("RED\n$Z_{red}$ (SCR)"))
    # realimentacion de medidas al control
    d.add(dsp.Line().down(1.8).at(pl.S))
    d.add(dsp.Arrow().left().tox(ctrl.S).label("$v_C, i_{L1}, i_{L2}$", "bottom"))
    d.add(dsp.Line().up(1.8).toy(ctrl.S))
    d.save(os.path.join(OUT, "diagrama_modelo.png"), dpi=150)


def diagrama_control():
    d = schemdraw.Drawing()
    d.config(unit=0.85, fontsize=10.5)
    pq = d.add(dsp.Box(w=2.4, h=1.0).label("medida\n$P, Q$ + LPF"))
    d.add(dsp.Arrow().right(1.6).at(pq.E))
    droop = d.add(dsp.Box(w=2.4, h=1.0).anchor("W").label("Droop\n$P$-$f$ , $Q$-$V$"))
    d.add(dsp.Arrow().right(1.6).at(droop.E).label("$V^*,\\omega$", "top"))
    zv = d.add(dsp.Box(w=2.2, h=1.0).anchor("W").label("$Z$ virtual\n$R_v, L_v, R_{vt}$"))
    d.add(dsp.Arrow().right(1.4).at(zv.E).label("$v_C^*$", "top"))
    sv = d.add(dsp.Sum().anchor("W"))
    d.add(dsp.Arrow().right(1.2).at(sv.E))
    piv = d.add(dsp.Box(w=1.8, h=1.0).anchor("W").label("PI\ntensión"))
    d.add(dsp.Arrow().right(1.2).at(piv.E).label("$i_{L1}^*$", "top"))
    si = d.add(dsp.Sum().anchor("W"))
    d.add(dsp.Arrow().right(1.2).at(si.E))
    pii = d.add(dsp.Box(w=1.8, h=1.0).anchor("W").label("PI\ncorriente"))
    d.add(dsp.Arrow().right(1.3).at(pii.E).label("$v_{inv}$", "top"))
    pl = d.add(dsp.Box(w=2.0, h=1.2).anchor("W").label("PLANTA\nLCL"))
    # realimentaciones
    d.add(dsp.Line().down(2.4).at(pl.S))
    d.add(dsp.Line().left().tox(sv.S))
    d.add(dsp.Arrow().up().toy(sv.S).label("$v_C$", "left"))     # lazo de tension
    d.add(dsp.Line().down(1.6).at(pl.S))
    d.add(dsp.Line().left().tox(si.S))
    d.add(dsp.Arrow().up().toy(si.S).label("$i_{L1}$", "right"))  # lazo de corriente
    # damping activo (nota)
    d.add(dsp.Line().down(3.2).at(pl.S))
    d.add(dsp.Line().left().tox(pq.S))
    d.add(dsp.Arrow().up().toy(pq.S).label("medidas", "left"))
    d.save(os.path.join(OUT, "diagrama_control.png"), dpi=150)


if __name__ == "__main__":
    esquema_electrico(); print("esquema_electrico.png")
    diagrama_modelo(); print("diagrama_modelo.png")
    diagrama_control(); print("diagrama_control.png")
