"""Diagramas del proyecto data center IA (schemdraw, offline):
  1) esquema_electrico.png  - sistema hibrido AC+DC (BESS -> AFE -> bus DC -> CPL)
  2) diagrama_modelo.png    - bloques del modelo (lado AC, AFE, lado DC, CPL)
  3) diagrama_control.png   - VSM del BESS (AC) + regulacion del bus DC; CPL como perturbacion
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
    d += elm.SourceSin().label("BESS\ngrid-forming\n(AC)")
    d += elm.Line().right(0.5)
    d += elm.RBox(w=1.8, h=2.2).label("AFE\nAC/DC")
    d += elm.Line().right(0.4)
    d += elm.Dot().label("bus DC", loc="top")
    d += elm.Inductor2().right().label("$L_f$ (cable)")
    d += elm.Resistor().right().label("$R_f$")
    d += elm.Dot().label("$V_{dc}$ rack", loc="top")
    d.push()
    d += elm.Capacitor().down().label("$C_{dc}$", loc="bottom"); d += elm.Ground()
    d.pop()
    d += elm.Line().right(0.4)
    d += elm.RBox(w=2.0, h=2.2).label("CPL\nservidores\nIA (GPU)")
    d.save(os.path.join(OUT, "esquema_electrico.png"), dpi=150)


def diagrama_modelo():
    d = schemdraw.Drawing(); d.config(unit=1.0, fontsize=11)
    bess = d.add(dsp.Box(w=2.4, h=1.2).label("BESS VSM\n(lado AC)\nω, P"))
    d.add(dsp.Arrow().right(1.8).at(bess.E).label("$P_{afe}$", "top"))
    afe = d.add(dsp.Box(w=1.8, h=1.2).anchor("W").label("AFE\nAC/DC"))
    d.add(dsp.Arrow().right(1.8).at(afe.E).label("$V_{bus}$", "top"))
    dc = d.add(dsp.Box(w=2.6, h=1.4).anchor("W").label("BUS DC\n$L_f$–$C_{dc}$\n(2 estados)"))
    d.add(dsp.Arrow().right(1.8).at(dc.E).label("$V_{dc}$", "top"))
    d.add(dsp.Box(w=2.0, h=1.2).anchor("W").label("CPL\n$i=P/V_{dc}$"))
    # realimentacion de potencia: la carga determina P_afe que ve el BESS
    d.add(dsp.Line().down(2.0).at(dc.S))
    d.add(dsp.Arrow().left().tox(bess.S).label("potencia demandada", "bottom"))
    d.add(dsp.Line().up(2.0).toy(bess.S))
    d.save(os.path.join(OUT, "diagrama_modelo.png"), dpi=150)


def diagrama_control():
    d = schemdraw.Drawing(); d.config(unit=0.9, fontsize=10.5)
    # lado AC: ecuacion de swing del BESS
    load = d.add(dsp.Box(w=2.4, h=1.0).label("carga IA\n$P_{cpl}(t)$ (pico)"))
    d.add(dsp.Arrow().right(1.4).at(load.E).label("demanda", "top"))
    sw = d.add(dsp.Box(w=2.6, h=1.1).anchor("W").label("BESS VSM\n$J\\dot\\omega=(P^*-P)/\\omega_0-D\\Delta\\omega$"))
    d.add(dsp.Arrow().right(1.4).at(sw.E).label("$\\omega$ (frecuencia AC)", "top"))
    out = d.add(dsp.Box(w=1.8, h=1.0).anchor("W").label("bus AC"))
    # lado DC debajo: AFE regula el bus DC
    afe = d.add(dsp.Box(w=2.4, h=1.0).at((load.S[0], load.S[1]-2.6)).anchor("W").label("AFE: regula $V_{bus}$"))
    d.add(dsp.Arrow().right(1.6).at(afe.E).label("$V_{bus}$", "top"))
    busdc = d.add(dsp.Box(w=2.4, h=1.0).anchor("W").label("bus DC + $C_{dc}$"))
    d.add(dsp.Arrow().right(1.4).at(busdc.E).label("$V_{dc}$", "top"))
    d.add(dsp.Box(w=1.6, h=1.0).anchor("W").label("CPL"))
    d.save(os.path.join(OUT, "diagrama_control.png"), dpi=150)


if __name__ == "__main__":
    esquema_electrico(); print("esquema_electrico.png")
    diagrama_modelo(); print("diagrama_modelo.png")
    diagrama_control(); print("diagrama_control.png")
