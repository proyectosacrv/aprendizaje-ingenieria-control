"""Genera las figuras de las fichas del repositorio de conocimiento.

Cada figura se guarda en figuras/<slug>-<nombre>.png con FONDO OSCURO integrado en el
tema del repo (líneas claras sobre #0b0f14). Se embeben en las fichas .md con
<img src="figuras/...">. Reejecutar regenera todo.

  python gen_figuras.py            # todas
  python gen_figuras.py filtro-lcl # solo las de un slug (prefijo)

Herramientas: schemdraw (circuitos/bloques), matplotlib (+scipy.signal) (gráficas).
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import signal
import schemdraw
import schemdraw.elements as elm
import schemdraw.dsp as dsp

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "figuras")
os.makedirs(OUT, exist_ok=True)

# Figuras BLANCAS (estilo de los informes de proyecto): schemdraw negro sobre blanco +
# matplotlib claro. Se muestran en un contenedor blanco .cfig dentro de la ficha.
ACC, ACC2, OK, BAD = "#1f6feb", "#e08e0b", "#1a9e5a", "#d62728"

plt.rcParams.update({
    "figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white",
    "axes.edgecolor": "#555", "axes.labelcolor": "#222", "text.color": "#222",
    "xtick.color": "#555", "ytick.color": "#555", "grid.color": "#ccc",
    "font.size": 11, "axes.grid": True, "grid.alpha": 0.6, "lines.linewidth": 2.0,
})

REGISTRY = []
def figura(slug):
    def deco(fn):
        REGISTRY.append((slug, fn)); return fn
    return deco

def _savefig(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig); print(name)


# ===================================================================== #
#  filtro-lcl
# ===================================================================== #
@figura("filtro-lcl")
def _lcl():
    # 1) circuito (schemdraw)
    d = schemdraw.Drawing()
    d.config(unit=2.0, fontsize=12)
    d += elm.RBox(w=2.0, h=2.4).label("fuente de\ntensión\nconmutada\n$v_i$")
    d += elm.Line().right(0.4)
    d += elm.Inductor2().right().label("$L_1,R_1$")
    d += (vc := elm.Dot().label("$v_C$", loc="top"))
    d.push()
    d += elm.Capacitor().down().label("$C_f$", loc="bottom")
    d += elm.Ground()
    d.pop()
    d += elm.Line().right(0.3)
    d += elm.Inductor2().right().label("$L_2,R_2$")
    d += elm.Dot().label("PCC", loc="top")
    d += elm.SourceSin().down().label("red / carga", loc="bottom")
    d += elm.Ground()
    d.save(os.path.join(OUT, "filtro-lcl-circuito.png"), dpi=150)
    print("filtro-lcl-circuito.png")

    # 2) Bode de |i2/vi|: sin amortiguar vs amortiguado (matplotlib + scipy)
    L1, L2, Cf = 2e-3, 1e-3, 20e-6
    w_res = np.sqrt((L1 + L2) / (L1 * L2 * Cf)); f_res = w_res / (2 * np.pi)
    f = np.logspace(1, 4.3, 2000); w = 2 * np.pi * f

    def mag_db(Rd):
        A = np.array([[-Rd/L1,  Rd/L1, -1/L1],
                      [ Rd/L2, -Rd/L2,  1/L2],
                      [ 1/Cf,  -1/Cf,   0  ]])
        B = np.array([[1/L1], [0], [0]]); C = np.array([[0, 1, 0]]); D = np.array([[0]])
        _, mag, _ = signal.bode(signal.StateSpace(A, B, C, D), w)
        return mag

    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    ax.semilogx(f, mag_db(0.0), color=BAD, label="sin amortiguar ($\\zeta\\approx0$)")
    ax.semilogx(f, mag_db(1/(3*w_res*Cf)), color=ACC, label="con $R_d$ (amortiguado)")
    ax.axvline(f_res, color=ACC2, ls="--", lw=1.3)
    ax.annotate(f"$f_{{res}}\\approx{f_res:.0f}$ Hz", xy=(f_res, 22),
                xytext=(f_res*0.55, 45), ha="right", color=ACC2, fontsize=10,
                arrowprops=dict(arrowstyle="->", color=ACC2))
    ax.set_xlabel("frecuencia [Hz]"); ax.set_ylabel("$|i_2/v_i|$ [dB]")
    ax.set_title("Respuesta del LCL: pico de resonancia y caída a −60 dB/dec", fontsize=11)
    ax.set_ylim(-120, 60); ax.legend(loc="upper right", fontsize=9)
    _savefig(fig, "filtro-lcl-bode.png")


@figura("filtro-lcl")
def _lcl_familia():
    """Familia de FDT del LCL frente a vi (con vpcc=0): i2/vi, i1/vi, vC/vi."""
    L1, L2, Cf = 2e-3, 1e-3, 20e-6
    w_res = np.sqrt((L1 + L2) / (L1 * L2 * Cf)); f_res = w_res/(2*np.pi)
    f_ar = 1/(2*np.pi*np.sqrt(L2*Cf))
    f = np.logspace(1, 4.0, 2000); w = 2*np.pi*f
    Rd = 0.3*(1/(3*w_res*Cf))                  # ligero amortiguamiento para que se vea

    A = np.array([[-Rd/L1,  Rd/L1, -1/L1],
                  [ Rd/L2, -Rd/L2,  1/L2],
                  [ 1/Cf,  -1/Cf,   0  ]])
    B = np.array([[1/L1], [0], [0]])
    def magdb(C):
        _, mag, _ = signal.bode(signal.StateSpace(A, B, np.array([C]), [[0]]), w)
        return mag
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    ax.semilogx(f, magdb([0, 1, 0]), color=ACC,  lw=2.2, label="$i_2/v_i$  (planta del lazo de red)")
    ax.semilogx(f, magdb([1, 0, 0]), color=ACC2, lw=2.0, label="$i_1/v_i$  (lazo interno, antiresonancia)")
    ax.semilogx(f, magdb([0, 0, 1]), color=OK,   lw=2.0, label="$v_C/v_i$  (tensión de condensador)")
    ax.axvline(f_res, color="#888", ls="--", lw=1)
    ax.axvline(f_ar, color="#bbb", ls=":", lw=1)
    ax.text(f_res*1.05, 38, f"$f_{{res}}$≈{f_res:.0f}", color="#555", fontsize=8.5)
    ax.text(f_ar*0.6, -70, f"$f_{{ar}}$≈{f_ar:.0f}", color="#999", fontsize=8.5)
    ax.set_xlabel("frecuencia [Hz]"); ax.set_ylabel("magnitud [dB]")
    ax.set_title("Familia de FDT del LCL frente a $v_i$ (con $v_{pcc}=0$)", fontsize=10.5)
    ax.set_ylim(-100, 55); ax.legend(loc="lower left", fontsize=8.5)
    fig.tight_layout()
    _savefig(fig, "filtro-lcl-familia.png")


@figura("filtro-lcl")
def _lcl_RvsnoR():
    """Comparacion de i2/vi sin R (ideal) vs con R1,R2 en serie (real)."""
    L1, L2, Cf = 2e-3, 1e-3, 20e-6
    w_res = np.sqrt((L1 + L2) / (L1 * L2 * Cf)); f_res = w_res/(2*np.pi)
    f = np.logspace(0, 4.0, 3000); w = 2*np.pi*f

    def magdb(R1, R2):
        A = np.array([[-R1/L1,  0,     -1/L1],
                      [ 0,      -R2/L2,  1/L2],
                      [ 1/Cf,  -1/Cf,   0  ]])
        B = np.array([[1/L1], [0], [0]]); C = np.array([[0, 1, 0]])
        _, mag, _ = signal.bode(signal.StateSpace(A, B, C, [[0]]), w)
        return mag

    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    ax.semilogx(f, magdb(2e-3, 2e-3), color=BAD, lw=2.0,
                label="sin R (R≈0): pico ∞, pendiente integrador en BF")
    ax.semilogx(f, magdb(0.3, 0.15), color=ACC, lw=2.0,
                label="con R1,R2 en serie: pico finito, meseta en BF")
    ax.axvline(f_res, color="#888", ls="--", lw=1)
    ax.text(f_res*1.06, 30, f"$f_{{res}}$≈{f_res:.0f} Hz", color="#555", fontsize=9)
    ax.annotate("BF: 1/(R1+R2) finito\nvs integrador (R=0)", xy=(2, -6), xytext=(2.2, 18),
                fontsize=8.2, color="#555", arrowprops=dict(arrowstyle="->", color="#999"))
    ax.set_xlabel("frecuencia [Hz]"); ax.set_ylabel("$|i_2/v_i|$ [dB]")
    ax.set_title("Efecto de las resistencias serie: con R vs sin R", fontsize=10.5)
    ax.set_ylim(-90, 55); ax.legend(loc="lower left", fontsize=8.3)
    fig.tight_layout()
    _savefig(fig, "filtro-lcl-RvsnoR.png")


@figura("filtro-lcl")
def _lcl_factorQ():
    """Efecto del factor de calidad Q (amortiguamiento) sobre el pico de resonancia."""
    L1, L2, Cf = 2e-3, 1e-3, 20e-6
    w_res = np.sqrt((L1 + L2) / (L1 * L2 * Cf)); f_res = w_res / (2*np.pi)
    f = np.logspace(2, 4.0, 2000); w = 2*np.pi*f

    def mag_db(Rd):
        A = np.array([[-Rd/L1,  Rd/L1, -1/L1],
                      [ Rd/L2, -Rd/L2,  1/L2],
                      [ 1/Cf,  -1/Cf,   0  ]])
        B = np.array([[1/L1], [0], [0]]); C = np.array([[0, 1, 0]]); D = np.array([[0]])
        _, mag, _ = signal.bode(signal.StateSpace(A, B, C, D), w)
        return mag

    Rd_opt = 1/(3*w_res*Cf)
    casos = [(0.0,        "Q→∞ (sin amortiguar)",      BAD,  2.4),
             (0.3*Rd_opt, "Q alto (poco amortiguado)", ACC2, 1.8),
             (Rd_opt,     "Q≈3 ($R_d$ óptimo)",         ACC,  2.0),
             (3*Rd_opt,   "Q bajo (sobre-amortiguado)", OK,   1.8)]
    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    for Rd, lab, col, lw in casos:
        ax.semilogx(f, mag_db(Rd), color=col, lw=lw, label=lab)
    ax.axvline(f_res, color="#888", ls="--", lw=1.1)
    ax.text(f_res*1.05, -52, f"$f_{{res}}\\approx{f_res:.0f}$ Hz", color="#555", fontsize=9)
    ax.set_xlabel("frecuencia [Hz]"); ax.set_ylabel("$|i_2/v_i|$ [dB]")
    ax.set_title("Efecto del factor Q: a más amortiguamiento, pico más bajo y ancho", fontsize=10.5)
    ax.set_ylim(-60, 50); ax.legend(loc="upper right", fontsize=8.5)
    fig.tight_layout()
    _savefig(fig, "filtro-lcl-factorQ.png")


@figura("filtro-lcl")
def _lcl_rizado():
    """Diseño del rizado: forma d(1-d) en el ciclo y rizado p-p vs L1."""
    Vdc, fsw = 700.0, 10e3
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 3.5))

    # (a) rizado a lo largo del ciclo de red, para dos valores de L1
    wt = np.linspace(0, np.pi, 400)            # medio ciclo
    m = 0.9
    d = (1 + m*np.sin(wt))/2
    for L1, col, lab in [(1.0e-3, ACC2, "$L_1=1$ mH"), (2.0e-3, ACC, "$L_1=2$ mH")]:
        dipp = (Vdc/(fsw*L1))*d*(1 - d)        # pico-pico instantaneo
        ax1.plot(np.degrees(wt), dipp, color=col, label=lab)
    ax1.set_xlabel("fase del ciclo de red [°]"); ax1.set_ylabel("rizado p-p $\\Delta i_{1,pp}$ [A]")
    ax1.set_title("Rizado $\\propto d(1-d)$: máximo en el paso por cero", fontsize=10)
    ax1.legend(fontsize=9, loc="upper right")

    # (b) rizado p-p maximo vs L1 (caso peor d=0.5 -> Vdc/(4 fsw L1))
    L1v = np.linspace(0.3e-3, 4e-3, 300)
    dipp_max = Vdc/(4*fsw*L1v)
    In = 20.0                                   # corriente nominal de pico de ejemplo
    ax2.plot(L1v*1e3, dipp_max, color=ACC, lw=2.2)
    for frac, col in [(0.20, ACC2), (0.10, OK)]:
        ax2.axhline(frac*In, color=col, ls="--", lw=1.3)
        L1_req = Vdc/(4*fsw*frac*In)
        ax2.text(3.4, frac*In+0.4, f"{int(frac*100)}% de $I_n$ → $L_1$≈{L1_req*1e3:.2f} mH",
                 color=col, fontsize=8.5, ha="right")
    ax2.set_xlabel("$L_1$ [mH]"); ax2.set_ylabel("rizado p-p máximo [A]")
    ax2.set_title("Más $L_1$ → menos rizado (caso peor $d$=0.5)", fontsize=10)
    ax2.set_ylim(0, 12)
    fig.tight_layout()
    _savefig(fig, "filtro-lcl-rizado.png")


@figura("filtro-lcl")
def _lcl_rizado_onda():
    """Formas de onda del rizado: tension de polo (subintervalos) y rampa de corriente."""
    Vdc, fsw, L1 = 700.0, 10e3, 2e-3
    Tsw = 1/fsw; d = 0.6; vo = (2*d - 1)*Vdc/2
    N = 4000; t = np.linspace(0, 2*Tsw, N); dt = t[1]-t[0]
    vpole = np.where((t % Tsw) < d*Tsw, Vdc/2, -Vdc/2)
    i = np.zeros(N)
    for k in range(1, N):
        i[k] = i[k-1] + (vpole[k-1]-vo)/L1*dt
    i = i - (i.max()+i.min())/2                       # centrar el rizado en 0 (A)
    tus = t*1e6                                       # microsegundos
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.2, 4.8), sharex=True)
    a1.plot(tus, vpole, color=ACC, lw=1.9)
    a1.axhline(vo, color=BAD, ls="--", lw=1.5, label=f"media $v_o$={vo:.0f} V")
    a1.axvspan(0, d*Tsw*1e6, color=ACC, alpha=0.08)
    a1.text(d*Tsw*1e6/2, Vdc*0.60, "$d\\,T_{sw}$", ha="center", fontsize=9, color="#333")
    a1.text((d+ (1-d)/2)*Tsw*1e6, -Vdc*0.62, "$(1-d)T_{sw}$", ha="center", fontsize=9, color="#333")
    a1.set_ylabel("tensión de polo [V]"); a1.set_ylim(-Vdc*0.8, Vdc*0.8)
    a1.legend(fontsize=8, loc="upper right")
    a1.set_title("Forma de onda del rizado en $L_1$ durante un periodo de conmutación", fontsize=10)
    a2.plot(tus, i, color=ACC2, lw=1.9)
    ipp = i.max()-i.min()
    a2.annotate("", xy=(d*Tsw*1e6, i.max()), xytext=(d*Tsw*1e6, i.min()),
                arrowprops=dict(arrowstyle="<->", color="#333", lw=1.3))
    a2.text(d*Tsw*1e6+3, 0, f"$\\Delta i_{{1,pp}}$≈{ipp:.0f} A", fontsize=9, color="#333")
    a2.axhline(0, color="#aaa", lw=0.7)
    a2.set_ylabel("rizado de $i_1$ [A]"); a2.set_xlabel("t [µs]")
    a2.text(d*Tsw*1e6*0.5, i.max()*0.6, "sube\n(pendiente $v_{L+}/L_1$)", ha="center", fontsize=8, color="#555")
    a2.text((d+(1-d)/2)*Tsw*1e6, i.min()*0.6, "baja\n($v_{L-}/L_1$)", ha="center", fontsize=8, color="#555")
    fig.tight_layout()
    _savefig(fig, "filtro-lcl-rizado-onda.png")


@figura("filtro-lcl")
def _lcl_damping_polos():
    """Amortiguamiento activo: lugar de los polos resonantes al barrer Kad."""
    L1, L2, Cf = 2e-3, 1e-3, 20e-6
    w_res = np.sqrt((L1 + L2) / (L1 * L2 * Cf))
    Kads = np.linspace(0, 12, 40)              # ohmios de resistencia virtual
    fig, ax = plt.subplots(figsize=(5.4, 4.4))

    pts = []
    for Kad in Kads:
        A = np.array([[-Kad/L1, Kad/L1, -1/L1],
                      [ 0,       0,      1/L2],
                      [ 1/Cf,   -1/Cf,   0  ]])
        ev = np.linalg.eigvals(A)
        pts.append(ev[np.argsort(ev.imag)])    # ordenar por parte imaginaria
    pts = np.array(pts)
    # colorear el barrido del par superior (imag > 0)
    sup = pts[:, 2]
    sc = ax.scatter(sup.real, sup.imag, c=Kads, cmap="viridis", s=22, zorder=3)
    ax.scatter(sup.real[0], sup.imag[0], color=BAD, s=70, zorder=4,
               label="$K_{ad}=0$ (sobre el eje, $\\zeta\\approx0$)")
    ax.scatter(sup.real[-1], sup.imag[-1], color=OK, s=70, marker="s", zorder=4,
               label=f"$K_{{ad}}={Kads[-1]:.0f}$ Ω (amortiguado)")
    # lineas de zeta constante
    for z in [0.1, 0.3, 0.7]:
        th = np.arccos(z)
        r = np.linspace(0, w_res*1.1, 10)
        ax.plot(-r*np.cos(th), r*np.sin(th), color="#bbb", ls=":", lw=1)
        ax.text(-w_res*1.05*np.cos(th), w_res*1.05*np.sin(th), f"ζ={z}",
                color="#999", fontsize=8)
    ax.axhline(0, color="#888", lw=0.8); ax.axvline(0, color="#888", lw=0.8)
    ax.set_xlabel("Re(s) [1/s]"); ax.set_ylabel("Im(s) [rad/s]")
    ax.set_title("Amortiguamiento activo: $K_{ad}$ mueve\nel par resonante hacia la izquierda", fontsize=10)
    ax.set_ylim(0, w_res*1.25); ax.legend(fontsize=8, loc="lower left")
    cb = fig.colorbar(sc, ax=ax); cb.set_label("$K_{ad}$ [Ω]", fontsize=9)
    fig.tight_layout()
    _savefig(fig, "filtro-lcl-damping-polos.png")


@figura("filtro-lcl")
def _lcl_damping_bloques():
    """Amortiguamiento activo: diagrama de bloques del lazo (de donde sale A(Kad))."""
    d = schemdraw.Drawing()
    d.config(unit=0.95, fontsize=10.5)
    d += dsp.Arrow().right(1.0).label("$v_{i,PI}$", "top")
    s1 = d.add(dsp.Sum().anchor("W"))
    d += dsp.Arrow().right(1.3).at(s1.E).label("$v_i$", "bottom")
    plant = d.add(dsp.Box(w=2.8, h=1.5).anchor("W").label("Filtro LCL\n$L_1$–$C_f$–$L_2$"))

    # el bloque tiene UNA entrada (vi) y DOS salidas (i1, i2): no se "toca" i1 sobre
    # el cable de vi, sale del propio bloque, igual que iL1 en control-cascada-lazos.
    top_right = (plant.E[0], plant.E[1] + 0.42)
    bot_right = (plant.E[0], plant.E[1] - 0.42)
    d += dsp.Arrow().right(2.8).at(bot_right).label("$i_2$ (red)", "bottom")
    tap2 = d.add(dsp.Dot().at((bot_right[0] + 2.0, bot_right[1])))
    d += dsp.Line().right(0.5).at(top_right)
    tap1 = d.add(dsp.Dot().at((top_right[0] + 0.5, top_right[1])))
    d += elm.Label().label("$i_1$ (fuente)").at((tap1.center[0], tap1.center[1] + 0.32))

    # restador explicito i1(+)-i2(-) -> i_Cf, luego ganancia Kad, realimentado a s1
    y_sub = plant.S[1] - 1.7
    xc = (tap1.center[0] + tap2.center[0]) / 2
    s2 = d.add(dsp.Sum().anchor("N").at((xc, y_sub)))
    d += dsp.Line().at(tap1.center).to((tap1.center[0], s2.W[1]))
    d += dsp.Line().tox(s2.W[0]).at((tap1.center[0], s2.W[1]))
    d += dsp.Line().at(tap2.center).to((tap2.center[0], s2.E[1]))
    d += dsp.Line().tox(s2.E[0]).at((tap2.center[0], s2.E[1]))
    d += elm.Label().label("$-$").at((s2.E[0] + 0.32, s2.E[1] + 0.05))
    d += dsp.Arrow().down(1.3).at(s2.S)
    d += elm.Label().label("$i_{C_f}=i_1-i_2$").at((s2.S[0] + 0.35, s2.S[1] - 0.85))

    kad = d.add(dsp.Box(w=1.6, h=1.0).anchor("N").at((s2.S[0], s2.S[1] - 1.3)).label("$K_{ad}$"))
    d += dsp.Line().left().at(kad.W).tox(s1.S[0])
    d += dsp.Arrow().toy(s1.S[1]).label("$-$", "left")

    d.save(os.path.join(OUT, "filtro-lcl-damping-bloques.png"), dpi=150)
    print("filtro-lcl-damping-bloques.png")


# ===================================================================== #
#  marco-dq
# ===================================================================== #
@figura("marco-dq")
def _marcodq():
    t = np.linspace(0, 0.04, 1000)                 # 2 ciclos a 50 Hz
    w0 = 2 * np.pi * 50
    va = np.cos(w0 * t); vb = np.cos(w0 * t - 2*np.pi/3); vc = np.cos(w0 * t + 2*np.pi/3)
    vd = np.ones_like(t); vq = np.zeros_like(t)    # Park alineado: vd=cte, vq=0
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.4, 3.3))
    a1.plot(t*1e3, va, label="a"); a1.plot(t*1e3, vb, label="b"); a1.plot(t*1e3, vc, label="c")
    a1.set_title("marco abc/αβ (senoides)"); a1.set_xlabel("t [ms]"); a1.set_ylabel("v [pu]")
    a1.legend(ncol=3, fontsize=8, loc="lower center")
    a2.plot(t*1e3, vd, color=ACC, label="$v_d$"); a2.plot(t*1e3, vq, color=BAD, label="$v_q$")
    a2.set_title("marco dq / Park (constantes)"); a2.set_xlabel("t [ms]"); a2.set_ylim(-1.3, 1.3)
    a2.legend(fontsize=9, loc="center right")
    fig.suptitle("Transformada de Park: las senoides AC se vuelven continuas", fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    _savefig(fig, "marco-dq-park.png")


# ===================================================================== #
#  droop-control
# ===================================================================== #
@figura("droop-control")
def _droop():
    P = np.linspace(0, 1, 100); Q = np.linspace(-1, 1, 100)
    f0, mp, V0, nq = 50.0, 0.5, 1.0, 0.05
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.4, 3.3))
    a1.plot(P, f0 - mp*P, color=ACC, lw=2.3)
    a1.axhline(f0, color="#aaa", ls=":")
    a1.set_title("Droop P–f"); a1.set_xlabel("P [pu]"); a1.set_ylabel("f [Hz]")
    a1.annotate("pendiente $-m_p$", xy=(0.62, f0-mp*0.62), xytext=(0.1, f0-0.16),
                fontsize=9, arrowprops=dict(arrowstyle="->", color="#444"))
    a2.plot(Q, V0 - nq*Q, color=ACC2, lw=2.3)
    a2.axhline(V0, color="#aaa", ls=":")
    a2.set_title("Droop Q–V"); a2.set_xlabel("Q [pu]"); a2.set_ylabel("V [pu]")
    a2.annotate("pendiente $-n_q$", xy=(0.55, V0-nq*0.55), xytext=(-0.9, V0-0.012),
                fontsize=9, arrowprops=dict(arrowstyle="->", color="#444"))
    fig.suptitle("Estatismo (droop): la f baja con P y la V baja con Q", fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    _savefig(fig, "droop-control-curvas.png")


# ===================================================================== #
#  pll-srf
# ===================================================================== #
@figura("pll-srf")
def _pll():
    d = schemdraw.Drawing()
    d.config(unit=0.85, fontsize=10)
    d += dsp.Arrow().right(1.0).label("$v_{abc}$", "left")
    park = d.add(dsp.Box(w=2.0, h=1.1).anchor("W").label("Park\nabc→dq"))
    d += dsp.Arrow().right(1.1).at(park.E).label("$v_q$", "top")
    pi = d.add(dsp.Box(w=2.1, h=1.1).anchor("W").label("PI\n$K_p+K_i/s$"))
    d += dsp.Line().right(0.9).at(pi.E)
    sm = d.add(dsp.Sum().anchor("W"))
    d += dsp.Arrow().down(1.0).at((sm.N[0], sm.N[1] + 1.0)).label("$\\omega_0$", "right")
    d += dsp.Arrow().right(1.0).at(sm.E).label("$\\omega_{pll}$", "top")
    integ = d.add(dsp.Box(w=1.5, h=1.1).anchor("W").label("$1/s$"))
    d += dsp.Arrow().right(1.2).at(integ.E).label("$\\theta_{pll}$", "top")
    out = d.add(dsp.Dot())
    d += dsp.Line().down(1.8).at(out.center)
    d += dsp.Line().tox(park.S)
    d += dsp.Arrow().toy(park.S)
    d.save(os.path.join(OUT, "pll-srf-bloques.png"), dpi=140)
    print("pll-srf-bloques.png")


# ===================================================================== #
#  control-cascada
# ===================================================================== #
@figura("control-cascada")
def _cascada():
    d = schemdraw.Drawing()
    d.config(unit=0.82, fontsize=10)
    d += dsp.Arrow().right(0.8).label("$v_C^*$", "left")
    s1 = d.add(dsp.Sum().anchor("W"))
    d += dsp.Arrow().right(0.8).at(s1.E)
    piv = d.add(dsp.Box(w=1.9, h=1.0).anchor("W").label("PI\ntensión"))
    d += dsp.Arrow().right(0.8).at(piv.E).label("$i_{L1}^*$", "top")
    s2 = d.add(dsp.Sum().anchor("W"))
    d += dsp.Arrow().right(0.8).at(s2.E)
    pii = d.add(dsp.Box(w=1.9, h=1.0).anchor("W").label("PI\ncorriente"))
    d += dsp.Arrow().right(0.8).at(pii.E).label("$v_i$", "top")
    pl = d.add(dsp.Box(w=2.0, h=1.0).anchor("W").label("planta\nLCL"))
    d += dsp.Arrow().right(1.3).at(pl.E).label("$v_C$", "top")
    out = d.add(dsp.Dot())
    d += dsp.Line().down(1.4).at(pl.S)                 # lazo interno (rápido): iL1
    d += dsp.Line().tox(s2.S)
    d += dsp.Arrow().toy(s2.S).label("$i_{L1}$", "right")
    d += dsp.Line().down(2.3).at(out.center)           # lazo externo (lento): vC
    d += dsp.Line().tox(s1.S)
    d += dsp.Arrow().toy(s1.S).label("$v_C$", "left")
    d.save(os.path.join(OUT, "control-cascada-lazos.png"), dpi=140)
    print("control-cascada-lazos.png")


# ===================================================================== #
#  red-thevenin-scr
# ===================================================================== #
@figura("red-thevenin-scr")
def _thevenin():
    d = schemdraw.Drawing()
    d.config(unit=2.0, fontsize=12)
    d += dsp.Arrow().left(0.7).label("hacia\ninversor", "left")
    d += elm.Dot().label("PCC", loc="top")
    d += elm.Resistor().right().label("$R_g$")
    d += elm.Inductor2().right().label("$L_g=X_g/\\omega_0$")
    d += elm.SourceSin().down().label("$V_g$\n(red ideal)", loc="bottom")
    d += elm.Ground()
    d.save(os.path.join(OUT, "red-thevenin-scr-circuito.png"), dpi=150)
    print("red-thevenin-scr-circuito.png")


# ===================================================================== #
#  analisis-modal
# ===================================================================== #
@figura("analisis-modal")
def _modal():
    poles = np.array([-8.32, -8.93+20.49j, -8.93-20.49j, -54.45+25.85j, -54.45-25.85j,
                      -100.32, -934.51+6940.80j, -934.51-6940.80j])
    fig, ax = plt.subplots(figsize=(6.8, 4.6))
    ax.axvspan(-1200, 0, color=OK, alpha=0.07)
    ax.scatter(poles.real, poles.imag, marker="x", s=75, color=BAD, zorder=3, lw=2)
    ax.axvline(0, color="k", lw=1.2)
    ax.axhline(0, color="#bbb", lw=0.6)
    ax.set_xlim(-1150, 120); ax.set_xlabel("Re(λ) = σ  [1/s]  (estable si < 0)")
    ax.set_ylabel("Im(λ) = $\\omega_d$  [rad/s]")
    ax.set_title("Mapa de autovalores: σ → amortiguamiento, $\\omega_d$ → frecuencia")
    ax.annotate("modo de potencia\n3.3 Hz, ζ=0.40", xy=(-8.93, 20.49), xytext=(-560, 3300),
                fontsize=8.5, arrowprops=dict(arrowstyle="->", color="#444"))
    ax.annotate("resonancia LCL\n1.1 kHz, ζ=0.13", xy=(-934.5, 6940.8), xytext=(-1050, 4200),
                fontsize=8.5, arrowprops=dict(arrowstyle="->", color="#444"))
    _savefig(fig, "analisis-modal-polos.png")


# ===================================================================== #
#  modulacion-pwm
# ===================================================================== #
@figura("modulacion-pwm")
def _pwm():
    t = np.linspace(0, 0.02, 3000)                     # 1 ciclo de 50 Hz
    fsw = 1000.0
    m = 0.8 * np.sin(2*np.pi*50*t)
    tri = 2*np.abs(2*((t*fsw) % 1) - 1) - 1            # portadora triangular [-1,1]
    sw = np.where(m > tri, 1.0, -1.0)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.8, 4.4), sharex=True)
    a1.plot(t*1e3, m, color=ACC, lw=2, label="moduladora $m(t)$")
    a1.plot(t*1e3, tri, color="#999", lw=1, label="portadora $f_{sw}$")
    a1.legend(fontsize=8, loc="upper right"); a1.set_ylabel("nivel")
    a1.set_title("Comparación moduladora vs portadora")
    a2.plot(t*1e3, sw, color=BAD, lw=1, label="salida conmutada")
    a2.plot(t*1e3, m, color=ACC, lw=2, ls="--", label="media $=m(t)$")
    a2.legend(fontsize=8, loc="upper right"); a2.set_ylabel("salida"); a2.set_xlabel("t [ms]")
    a2.set_title("La media de la tensión conmutada sigue a la moduladora")
    fig.tight_layout()
    _savefig(fig, "modulacion-pwm-ondas.png")


# ===================================================================== #
#  grid-forming-vs-following
# ===================================================================== #
@figura("grid-forming-vs-following")
def _gfmgfl():
    d = schemdraw.Drawing()
    d.config(unit=1.0, fontsize=10.5)
    g1 = d.add(dsp.Box(w=5.4, h=1.5).anchor("W").at((0, 0))
               .label("GFM: fuente de TENSIÓN\n$E\\,\\angle\\,\\delta$ tras impedancia\n(ángulo propio, sin PLL)"))
    d.add(dsp.Arrow().right(1.4).at(g1.E).label("impone\nV, f", "top"))
    d.add(dsp.Box(w=1.6, h=1.5).anchor("W").label("RED\n$Z_{red}$"))
    g2 = d.add(dsp.Box(w=5.4, h=1.5).anchor("W").at((0, -2.6))
               .label("GFL: fuente de CORRIENTE\n$i^*$ sigue la PLL\n(robustez ∝ BW de la PLL)"))
    d.add(dsp.Arrow().right(1.4).at(g2.E).label("inyecta\nI", "top"))
    d.add(dsp.Box(w=1.6, h=1.5).anchor("W").label("RED\n$Z_{red}$"))
    d.save(os.path.join(OUT, "grid-forming-vs-following-comparativa.png"), dpi=140)
    print("grid-forming-vs-following-comparativa.png")


# ===================================================================== #
#  modelo-promediado
# ===================================================================== #
@figura("modelo-promediado")
def _promediado():
    t = np.linspace(0, 0.02, 4000)
    avg = 0.8 * np.sin(2*np.pi*50*t)                      # dinámica útil (promediado)
    ripple = 0.05 * signal.sawtooth(2*np.pi*5000*t)       # rizado de conmutación
    fig, ax = plt.subplots(figsize=(7.6, 3.4))
    ax.plot(t*1e3, avg + ripple, color="#bbb", lw=0.8, label="conmutado (con rizado)")
    ax.plot(t*1e3, avg, color=ACC, lw=2.4, label="promediado (dinámica útil)")
    ax.set_xlabel("t [ms]"); ax.set_ylabel("$v_C$ [pu]")
    ax.set_title("Promediado vs conmutado: el promedio capta la dinámica útil")
    ax.legend(fontsize=9, loc="upper right")
    fig.tight_layout()
    _savefig(fig, "modelo-promediado-ondas.png")


# ===================================================================== #
#  potencia-instantanea-dq
# ===================================================================== #
@figura("potencia-instantanea-dq")
def _potdq():
    fig, ax = plt.subplots(figsize=(5.4, 5.0))
    ax.axhline(0, color="#bbb", lw=0.8); ax.axvline(0, color="#bbb", lw=0.8)
    ax.annotate("", xy=(1.0, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=ACC, lw=2.5))
    ax.text(0.85, 0.06, "$\\vec V$  (eje d)", color=ACC, fontsize=11)
    phi = np.radians(30); ix, iy = 0.85*np.cos(phi), -0.85*np.sin(phi)
    ax.annotate("", xy=(ix, iy), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=BAD, lw=2.5))
    ax.text(ix+0.02, iy-0.07, "$\\vec I$", color=BAD, fontsize=11)
    ax.plot([ix, ix], [iy, 0], color="#888", ls=":", lw=1.2)
    ax.text(ix/2, 0.05, "$i_d$", color="#444", fontsize=10, ha="center")
    ax.text(ix+0.03, iy/2, "$i_q$", color="#444", fontsize=10)
    th = np.linspace(0, -phi, 30); ax.plot(0.28*np.cos(th), 0.28*np.sin(th), color="#666", lw=1)
    ax.text(0.30, -0.10, "φ", fontsize=10)
    ax.set_xlim(-0.25, 1.2); ax.set_ylim(-0.75, 0.45); ax.set_aspect("equal")
    ax.set_title("Potencia en dq (eje d sobre V):\n$P=\\frac{3}{2} V i_d$,   $Q=-\\frac{3}{2} V i_q$", fontsize=11)
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    fig.tight_layout()
    _savefig(fig, "potencia-instantanea-dq-fasor.png")


# ===================================================================== #
#  desacoplo-dq
# ===================================================================== #
@figura("desacoplo-dq")
def _desacoplo():
    d = schemdraw.Drawing()
    d.config(unit=0.9, fontsize=10)
    d += dsp.Arrow().right(0.8).label("$i_d^*$", "left")
    se = d.add(dsp.Sum().anchor("W"))
    d += dsp.Arrow().right(0.8).at(se.E)
    pi = d.add(dsp.Box(w=1.6, h=1.0).anchor("W").label("PI"))
    d += dsp.Arrow().right(0.8).at(pi.E).label("$v_d'$", "top")
    sd = d.add(dsp.Sum().anchor("W"))
    d += dsp.Arrow().right(0.9).at(sd.E)
    pl = d.add(dsp.Box(w=2.4, h=1.0).anchor("W").label("planta d\n$1/(Ls+R)$"))
    d += dsp.Arrow().right(1.0).at(pl.E).label("$i_d$", "top")
    out = d.add(dsp.Dot())
    d += dsp.Arrow().down(1.1).at((sd.N[0], sd.N[1] + 1.1)).label("$-\\omega L\\,i_q$", "right")
    d += dsp.Line().down(1.7).at(out.center)
    d += dsp.Line().tox(se.S)
    d += dsp.Arrow().toy(se.S).label("$i_d$", "left")
    d.save(os.path.join(OUT, "desacoplo-dq-bloques.png"), dpi=140)
    print("desacoplo-dq-bloques.png")


# ===================================================================== #
#  impedancia-reactancia
# ===================================================================== #
@figura("impedancia-reactancia")
def _impedancia():
    f = np.logspace(0, 4, 500); w = 2*np.pi*f
    R, L, C = 1.0, 2e-3, 20e-6
    fig, ax = plt.subplots(figsize=(6.6, 3.8))
    ax.loglog(f, np.full_like(f, R), color=OK, lw=2, label="$R$ (constante)")
    ax.loglog(f, w*L, color=ACC, lw=2, label="$X_L=\\omega L$ (sube)")
    ax.loglog(f, 1/(w*C), color=BAD, lw=2, label="$X_C=1/\\omega C$ (baja)")
    ax.set_xlabel("frecuencia [Hz]"); ax.set_ylabel("|Z| [Ω]")
    ax.set_title("Impedancia de R, L y C frente a la frecuencia")
    ax.legend(fontsize=9); ax.grid(True, which="both", alpha=0.4)
    fig.tight_layout()
    _savefig(fig, "impedancia-reactancia-zf.png")


# ===================================================================== #
#  resonancia-rlc
# ===================================================================== #
@figura("resonancia-rlc")
def _rlc():
    f = np.logspace(1.5, 4, 1200); w = 2*np.pi*f
    L, C = 2e-3, 20e-6
    f0 = 1/(2*np.pi*np.sqrt(L*C)); Z0 = np.sqrt(L/C)   # impedancia caracteristica
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.8, 3.6))

    # (a) |Z| del RLC serie: minimo (=R) en f0, mas agudo si R baja
    for R, c, lbl in [(0.3, ACC, "Q alto (R=0.3 Ω)"), (3.0, ACC2, "Q bajo (R=3 Ω)")]:
        a1.loglog(f, np.abs(R + 1j*w*L + 1/(1j*w*C)), color=c, lw=2, label=lbl)
    a1.axvline(f0, color="#888", ls="--", lw=1)
    a1.annotate(f"$f_0$≈{f0:.0f} Hz", xy=(f0, 0.4), xytext=(f0*1.18, 0.55), fontsize=9, color="#555")
    a1.set_xlabel("frecuencia [Hz]"); a1.set_ylabel("|Z| RLC serie [Ω]")
    a1.set_title("RLC serie: |Z| mínima (=R) en $f_0$", fontsize=10)
    a1.legend(fontsize=8.5); a1.grid(True, which="both", alpha=0.4)

    # (b) pico de resonancia (tension en C, 2o orden) para varios Q: altura ~ Q
    fn = f/f0
    for Q, c in [(10, BAD), (3, ACC), (1, OK), (0.5, ACC2)]:
        H = 1.0/np.abs(1 - fn**2 + 1j*fn/Q)
        a2.semilogx(f, 20*np.log10(H), color=c, lw=2, label=f"Q={Q}")
    a2.axvline(f0, color="#888", ls="--", lw=1)
    a2.set_xlabel("frecuencia [Hz]"); a2.set_ylabel("ganancia [dB]")
    a2.set_title("Pico de resonancia: altura ≈ Q, ancho ≈ $f_0/Q$", fontsize=10)
    a2.legend(fontsize=8.5, loc="upper right"); a2.set_ylim(-30, 26)
    fig.tight_layout()
    _savefig(fig, "resonancia-rlc-zf.png")


# ===================================================================== #
#  margenes-estabilidad
# ===================================================================== #
@figura("margenes-estabilidad")
def _margenes():
    sys = signal.TransferFunction([5], [1/1000, 11/100, 1, 0])  # 5/(s(s/10+1)(s/100+1))
    w = np.logspace(-1, 3, 3000)
    w, mag, phase = signal.bode(sys, w)
    f = w/(2*np.pi)
    ig = int(np.argmin(np.abs(mag)))          # cruce de ganancia (|L|=0 dB)
    ip = int(np.argmin(np.abs(phase + 180)))  # cruce de fase (−180°)
    PM = 180 + phase[ig]; GM = -mag[ip]
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.8, 5.0), sharex=True)
    a1.semilogx(f, mag, color=ACC, lw=2); a1.axhline(0, color="#aaa", lw=0.8)
    a2.semilogx(f, phase, color=ACC, lw=2); a2.axhline(-180, color="#aaa", lw=0.8)
    for a in (a1, a2):
        a.axvline(f[ig], color=OK, ls=":"); a.axvline(f[ip], color=BAD, ls=":")
        a.grid(True, which="both", alpha=0.4)
    a2.annotate(f"PM = {PM:.0f}°", xy=(f[ig], phase[ig]), xytext=(f[ig]*1.4, -95),
                fontsize=9, color=OK, arrowprops=dict(arrowstyle="->", color=OK))
    a1.annotate(f"GM = {GM:.0f} dB", xy=(f[ip], mag[ip]), xytext=(f[ip]*0.25, -22),
                fontsize=9, color=BAD, arrowprops=dict(arrowstyle="->", color=BAD))
    a1.set_ylabel("|L| [dB]"); a2.set_ylabel("∠L [°]"); a2.set_xlabel("frecuencia [Hz]")
    a1.set_title("Márgenes sobre el Bode de la ganancia de lazo L(jω)")
    fig.tight_layout()
    _savefig(fig, "margenes-estabilidad-bode.png")


# ===================================================================== #
#  linealizacion-numerica
# ===================================================================== #
@figura("linealizacion-numerica")
def _linealizacion():
    f = lambda z: np.sin(z) + 0.3*z**2
    x = np.linspace(-1.5, 2.5, 400)
    x0, h = 1.0, 0.4
    deriv = (f(x0+h) - f(x0-h)) / (2*h)
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    ax.plot(x, f(x), color=ACC, lw=2.4, label="$f(x)$ no lineal")
    xt = np.linspace(x0-0.95, x0+0.95, 10)
    ax.plot(xt, f(x0) + deriv*(xt-x0), color=BAD, lw=2, ls="--", label="tangente (linealización)")
    ax.scatter([x0-h, x0+h], [f(x0-h), f(x0+h)], color="#444", zorder=5)
    ax.scatter([x0], [f(x0)], color=BAD, zorder=5)
    ax.annotate("$x_0\\!-\\!h$", (x0-h, f(x0-h)), textcoords="offset points", xytext=(-32, -12), fontsize=9)
    ax.annotate("$x_0\\!+\\!h$", (x0+h, f(x0+h)), textcoords="offset points", xytext=(2, 8), fontsize=9)
    ax.text(x0+0.05, f(x0)-0.9, "pendiente $A\\approx\\dfrac{f(x_0{+}h)-f(x_0{-}h)}{2h}$",
            fontsize=9, ha="center", color=BAD)
    ax.set_xlabel("x"); ax.set_ylabel("f(x)")
    ax.set_title("Linealización: la pendiente en $x_0$ por diferencias centradas")
    ax.legend(fontsize=9, loc="upper left"); ax.grid(True, alpha=0.4)
    fig.tight_layout()
    _savefig(fig, "linealizacion-numerica-tangente.png")


# ===================================================================== #
#  representacion-espacio-estados
# ===================================================================== #
@figura("representacion-espacio-estados")
def _ss():
    d = schemdraw.Drawing()
    d.config(unit=0.9, fontsize=10.5)
    d += dsp.Arrow().right(0.9).label("$u$", "left")
    bb = d.add(dsp.Box(w=1.2, h=1.0).anchor("W").label("$B$"))
    d += dsp.Arrow().right(0.7).at(bb.E)
    sm = d.add(dsp.Sum().anchor("W"))
    d += dsp.Arrow().right(0.7).at(sm.E).label("$\\dot x$", "top")
    integ = d.add(dsp.Box(w=1.3, h=1.0).anchor("W").label("$\\int$"))
    d += dsp.Line().right(0.6).at(integ.E)
    node = d.add(dsp.Dot())
    d += dsp.Arrow().right(0.7).at(node.center).label("$x$", "top")
    cc = d.add(dsp.Box(w=1.2, h=1.0).anchor("W").label("$C$"))
    d += dsp.Arrow().right(0.9).at(cc.E).label("$y$", "top")
    d += dsp.Line().down(1.6).at(node.center)
    ab = d.add(dsp.Box(w=1.2, h=0.9).anchor("N").label("$A$"))
    d += dsp.Line().left().at(ab.S).tox(sm.S)
    d += dsp.Arrow().toy(sm.S)
    d.save(os.path.join(OUT, "representacion-espacio-estados-bloques.png"), dpi=140)
    print("representacion-espacio-estados-bloques.png")


# ===================================================================== #
#  funcion-transferencia
# ===================================================================== #
@figura("funcion-transferencia")
def _ft():
    wn, z = 8.0, 0.5
    sys = signal.TransferFunction([wn**2], [1, 2*z*wn, wn**2])
    poles = np.roots([1, 2*z*wn, wn**2])
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.6, 3.6))
    a1.axvspan(-12, 0, color=OK, alpha=0.07)
    a1.scatter(poles.real, poles.imag, marker="x", s=90, color=ACC, lw=2.2)
    a1.axvline(0, color="k", lw=1.2); a1.axhline(0, color="#bbb", lw=0.6)
    a1.set_title("polos de G(s) = raíces del denominador"); a1.set_xlabel("Re(s)"); a1.set_ylabel("Im(s)")
    a1.set_xlim(-12, 2); a1.grid(True, alpha=0.3)
    tt, y = signal.step(sys, T=np.linspace(0, 1.5, 500))
    a2.plot(tt, y, color=BAD, lw=2.2); a2.axhline(1, color="#aaa", ls=":")
    a2.set_title("respuesta al escalón que implican"); a2.set_xlabel("t [s]"); a2.set_ylabel("y(t)")
    a2.grid(True, alpha=0.4)
    fig.suptitle("G(s) codifica los polos → y con ellos el comportamiento", fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    _savefig(fig, "funcion-transferencia-polos-step.png")


# ===================================================================== #
#  polos-ceros
# ===================================================================== #
@figura("polos-ceros")
def _polosceros():
    fig, ax = plt.subplots(figsize=(6.0, 4.6))
    ax.axvspan(-5, 0, color=OK, alpha=0.08); ax.axvspan(0, 3, color=BAD, alpha=0.08)
    ax.text(-3.3, 4.3, "semiplano izquierdo\n(estable)", color="#2a7", fontsize=9, ha="center")
    ax.text(1.6, 4.3, "semiplano derecho\n(inestable)", color="#b33", fontsize=9, ha="center")
    poles = np.array([-1+2j, -1-2j, -3+0j]); zeros = np.array([-2+0j])
    ax.scatter(poles.real, poles.imag, marker="x", s=95, color=ACC, lw=2.4, label="polos")
    ax.scatter(zeros.real, zeros.imag, marker="o", s=95, facecolors="none", edgecolors=BAD, lw=2, label="ceros")
    ax.plot([0, -1], [0, 2], color="#888", ls="--", lw=1)
    ax.annotate("ζ = cos θ", xy=(-0.55, 1.05), fontsize=9, color="#555")
    ax.axvline(0, color="k", lw=1.2); ax.axhline(0, color="#bbb", lw=0.6)
    ax.set_xlim(-5, 3); ax.set_ylim(-3.5, 5.2)
    ax.set_xlabel("Re(s) = σ"); ax.set_ylabel("Im(s) = ω")
    ax.set_title("Mapa de polos (×) y ceros (○) en el plano s")
    ax.legend(fontsize=9, loc="lower left"); ax.grid(True, alpha=0.3)
    fig.tight_layout()
    _savefig(fig, "polos-ceros-splano.png")


# ===================================================================== #
#  sistema-primer-orden
# ===================================================================== #
@figura("sistema-primer-orden")
def _primerorden():
    tau, K = 0.1, 1.0
    t = np.linspace(0, 5*tau, 400)
    y = K*(1 - np.exp(-t/tau))
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.plot(t*1e3, y, color=ACC, lw=2.4)
    ax.axhline(K, color="#aaa", ls=":")
    ax.axhline(0.632*K, color=OK, ls="--", lw=1); ax.axvline(tau*1e3, color=OK, ls="--", lw=1)
    ax.annotate("63% en t=τ", xy=(tau*1e3, 0.632*K), xytext=(tau*1e3*1.25, 0.42),
                fontsize=9, color=OK, arrowprops=dict(arrowstyle="->", color=OK))
    ax.axvline(4*tau*1e3, color="#999", ls=":")
    ax.text(4*tau*1e3*0.62, 0.12, "≈100% en 4τ\n(establecimiento)", fontsize=8.5, color="#555")
    ax.set_xlabel("t [ms]"); ax.set_ylabel("y(t)")
    ax.set_title("Respuesta al escalón de un sistema de primer orden (τ=0.1 s)")
    ax.grid(True, alpha=0.4)
    fig.tight_layout()
    _savefig(fig, "sistema-primer-orden-escalon.png")


# ===================================================================== #
#  respuesta-segundo-orden
# ===================================================================== #
@figura("respuesta-segundo-orden")
def _segundoorden():
    wn = 10.0
    t = np.linspace(0, 1.2, 600)
    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    for z, c in [(0.2, BAD), (0.5, ACC2), (0.707, ACC), (1.0, OK), (2.0, "#888")]:
        sys = signal.TransferFunction([wn**2], [1, 2*z*wn, wn**2])
        tt, y = signal.step(sys, T=t)
        ax.plot(tt, y, color=c, lw=2, label=f"ζ={z}")
    ax.axhline(1.0, color="#aaa", ls=":")
    ax.set_xlabel("t [s]"); ax.set_ylabel("y(t)")
    ax.set_title("Respuesta al escalón de 2º orden según ζ ($\\omega_n$=10 rad/s)")
    ax.legend(fontsize=8, ncol=2); ax.grid(True, alpha=0.4)
    fig.tight_layout()
    _savefig(fig, "respuesta-segundo-orden-familia.png")


# ===================================================================== #
#  diagrama-bode
# ===================================================================== #
@figura("diagrama-bode")
def _bode():
    sys = signal.TransferFunction([100], [1, 11, 10])   # 100/((s+1)(s+10))
    w = np.logspace(-1, 3, 1500)
    w, mag, phase = signal.bode(sys, w)
    f = w/(2*np.pi)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.6, 4.8), sharex=True)
    a1.semilogx(f, mag, color=ACC, lw=2)
    a2.semilogx(f, phase, color=ACC, lw=2)
    for fc in (1/(2*np.pi), 10/(2*np.pi)):
        a1.axvline(fc, color="#bbb", ls="--", lw=1); a2.axvline(fc, color="#bbb", ls="--", lw=1)
    a1.set_ylabel("|G| [dB]"); a2.set_ylabel("∠G [°]"); a2.set_xlabel("frecuencia [Hz]")
    a1.set_title("Bode: cada polo añade −20 dB/dec y hasta −90° de fase")
    a1.grid(True, which="both", alpha=0.4); a2.grid(True, which="both", alpha=0.4)
    fig.tight_layout()
    _savefig(fig, "diagrama-bode-ejemplo.png")


# ===================================================================== #
#  lugar-raices
# ===================================================================== #
@figura("lugar-raices")
def _rlocus():
    den = np.poly([-1, -2, -3])              # (s+1)(s+2)(s+3)
    Ks = np.linspace(0, 200, 800)
    roots_all = np.array([np.roots(den + np.array([0, 0, 0, K])) for K in Ks])
    op = np.roots(den)
    fig, ax = plt.subplots(figsize=(5.8, 5.0))
    ax.axvspan(0, 4, color=BAD, alpha=0.06)
    ax.scatter(roots_all.real, roots_all.imag, s=2, color=ACC, alpha=0.5)
    ax.scatter(op.real, op.imag, marker="x", s=90, color=BAD, lw=2.2, zorder=5,
               label="polos lazo abierto (K=0)")
    ax.axvline(0, color="k", lw=1.2); ax.axhline(0, color="#bbb", lw=0.6)
    ax.set_xlabel("Re(s)"); ax.set_ylabel("Im(s)"); ax.set_xlim(-6, 4)
    ax.set_title("Lugar de las raíces: polos del lazo cerrado al subir K")
    ax.legend(fontsize=8, loc="upper left"); ax.grid(True, alpha=0.3)
    fig.tight_layout()
    _savefig(fig, "lugar-raices-locus.png")


# ===================================================================== #
#  realimentacion
# ===================================================================== #
@figura("realimentacion")
def _realim():
    d = schemdraw.Drawing()
    d.config(unit=0.95, fontsize=10.5)
    d += dsp.Arrow().right(0.8).label("$r$", "left")
    sm = d.add(dsp.Sum().anchor("W"))
    d += dsp.Arrow().right(0.8).at(sm.E).label("$e$", "top")
    c = d.add(dsp.Box(w=1.7, h=1.0).anchor("W").label("$C(s)$"))
    d += dsp.Arrow().right(0.7).at(c.E)
    g = d.add(dsp.Box(w=1.7, h=1.0).anchor("W").label("$G(s)$"))
    d += dsp.Arrow().right(1.1).at(g.E).label("$y$", "top")
    node = d.add(dsp.Dot())
    d += dsp.Line().down(1.4).at(node.center)
    d += dsp.Line().tox(sm.S)
    d += dsp.Arrow().toy(sm.S).label("−", "left")
    d.save(os.path.join(OUT, "realimentacion-lazo.png"), dpi=140)
    print("realimentacion-lazo.png")


# ===================================================================== #
#  controlador-pid
# ===================================================================== #
@figura("controlador-pid")
def _pid():
    d = schemdraw.Drawing()
    d.config(fontsize=11)
    bi = d.add(dsp.Box(w=1.8, h=0.9).at((1.2, 1.5)).anchor("W").label("$K_i/s$"))
    bp = d.add(dsp.Box(w=1.8, h=0.9).at((1.2, 0.0)).anchor("W").label("$K_p$"))
    bd = d.add(dsp.Box(w=1.8, h=0.9).at((1.2, -1.5)).anchor("W").label("$K_d\\,s$"))
    d += dsp.Arrow().at((-0.8, 0)).to((0, 0)).label("$e$", "left")
    d += dsp.Line().at((0, -1.5)).to((0, 1.5))
    for y in (1.5, 0.0, -1.5):
        d += dsp.Line().at((0, y)).to((1.2, y))
    sm = d.add(dsp.Sum().at((4.6, 0)).anchor("center"))
    d += dsp.Line().at((3.0, 0)).to((4.3, 0))
    d += dsp.Line().at((3.0, 1.5)).to((4.6, 1.5)); d += dsp.Line().at((4.6, 1.5)).to((4.6, 0.3))
    d += dsp.Line().at((3.0, -1.5)).to((4.6, -1.5)); d += dsp.Line().at((4.6, -1.5)).to((4.6, -0.3))
    d += dsp.Arrow().at((4.9, 0)).to((5.9, 0)).label("$u$", "right")
    d.save(os.path.join(OUT, "controlador-pid-estructura.png"), dpi=140)
    print("controlador-pid-estructura.png")


# ===================================================================== #
#  criterio-nyquist
# ===================================================================== #
@figura("criterio-nyquist")
def _nyquist():
    sys = signal.TransferFunction([4], [1, 3, 3, 1])     # 4/(s+1)^3 (no rodea -1 -> estable)
    w = np.logspace(-1, 2, 3000)
    _, mag, phase = signal.bode(sys, w)
    H = 10**(mag/20) * np.exp(1j*np.radians(phase))
    fig, ax = plt.subplots(figsize=(5.4, 5.0))
    ax.plot(H.real, H.imag, color=ACC, lw=2, label="$L(j\\omega)$, ω>0")
    ax.plot(H.real, -H.imag, color=ACC, lw=2, ls="--", alpha=0.6, label="ω<0 (espejo)")
    ax.scatter([-1], [0], color=BAD, s=70, zorder=5)
    ax.annotate("punto crítico −1", xy=(-1, 0), xytext=(-2.6, 1.4),
                fontsize=9, color=BAD, arrowprops=dict(arrowstyle="->", color=BAD))
    ax.axhline(0, color="#bbb", lw=0.6); ax.axvline(0, color="#bbb", lw=0.6)
    ax.set_xlabel("Re $L(j\\omega)$"); ax.set_ylabel("Im $L(j\\omega)$")
    ax.set_title("Nyquist: ¿la traza rodea el −1?")
    ax.legend(fontsize=8, loc="upper left"); ax.grid(True, alpha=0.3); ax.set_aspect("equal")
    fig.tight_layout()
    _savefig(fig, "criterio-nyquist-plot.png")


# ===================================================================== #
#  error-regimen-permanente
# ===================================================================== #
@figura("error-regimen-permanente")
def _esserror():
    t = np.linspace(0, 3, 500)
    K = 4
    tt0, y0 = signal.step(signal.TransferFunction([K], [1, 1+K]), T=t)     # tipo 0
    tt1, y1 = signal.step(signal.TransferFunction([K], [1, 1, K]), T=t)    # tipo 1
    fig, ax = plt.subplots(figsize=(6.6, 3.8))
    ax.axhline(1, color="#aaa", ls=":", label="referencia")
    ax.plot(tt0, y0, color=BAD, lw=2, label="tipo 0 (solo P): error residual")
    ax.plot(tt1, y1, color=ACC, lw=2, label="tipo 1 (con I): error nulo")
    ax.annotate("", xy=(2.8, 1.0), xytext=(2.8, y0[-1]), arrowprops=dict(arrowstyle="<->", color=BAD))
    ax.text(2.5, (1.0+y0[-1])/2, "$e_{ss}$", color=BAD, fontsize=10, ha="right")
    ax.set_xlabel("t [s]"); ax.set_ylabel("y(t)")
    ax.set_title("Error en régimen: tipo 0 deja error, tipo 1 lo anula")
    ax.legend(fontsize=8, loc="lower right"); ax.grid(True, alpha=0.4)
    fig.tight_layout()
    _savefig(fig, "error-regimen-permanente-step.png")


# ===================================================================== #
#  diagrama-bloques
# ===================================================================== #
@figura("diagrama-bloques")
def _bloques():
    d = schemdraw.Drawing()
    d.config(unit=0.95, fontsize=10.5)
    d += dsp.Arrow().right(0.7).label("$R$", "left")
    sm = d.add(dsp.Sum().anchor("W"))
    d += dsp.Arrow().right(0.7).at(sm.E)
    g = d.add(dsp.Box(w=1.6, h=1.0).anchor("W").label("$G$"))
    d += dsp.Arrow().right(1.0).at(g.E).label("$Y$", "top")
    node = d.add(dsp.Dot())
    d += dsp.Line().down(1.3).at(node.center)
    hb = d.add(dsp.Box(w=1.4, h=0.9).anchor("N").label("$H$"))
    d += dsp.Line().left().at(hb.S).tox(sm.S)
    d += dsp.Arrow().toy(sm.S).label("−", "left")
    d += dsp.Arrow().right(1.0).at(node.center)
    d += dsp.Box(w=3.0, h=1.1).anchor("W").label("$\\dfrac{Y}{R}=\\dfrac{G}{1+GH}$")
    d.save(os.path.join(OUT, "diagrama-bloques-reduccion.png"), dpi=140)
    print("diagrama-bloques-reduccion.png")


# ===================================================================== #
#  estabilidad-bibo
# ===================================================================== #
@figura("estabilidad-bibo")
def _bibo():
    t = np.linspace(0, 6, 600)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.4, 3.4))
    a1.plot(t, np.exp(-0.5*t)*np.cos(3*t), color=OK, lw=2); a1.axhline(0, color="#bbb", lw=0.6)
    a1.set_title("estable: polos Re<0 (decae)"); a1.set_xlabel("t"); a1.set_ylabel("y(t)"); a1.grid(True, alpha=0.4)
    a2.plot(t, np.exp(0.35*t)*np.cos(3*t), color=BAD, lw=2); a2.axhline(0, color="#bbb", lw=0.6)
    a2.set_title("inestable: polos Re>0 (crece)"); a2.set_xlabel("t"); a2.grid(True, alpha=0.4)
    fig.suptitle("Estabilidad: respuesta acotada (izq.) frente a la que crece sin límite (der.)", fontsize=10.5)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    _savefig(fig, "estabilidad-bibo-respuestas.png")


# ===================================================================== #
#  convertidor-vsc
# ===================================================================== #
@figura("convertidor-vsc")
def _vsc():
    d = schemdraw.Drawing()
    d.config(fontsize=11)
    d += elm.Line().at((0, 2.4)).to((3.4, 2.4))                       # rail +Vdc
    d += elm.Line().at((0, 0)).to((3.4, 0))                           # rail 0
    d += elm.Capacitor().at((0.5, 0)).to((0.5, 2.4)).label("$V_{dc}$", "left")
    d += elm.Switch().at((2.2, 2.4)).to((2.2, 1.2)).label("$S_1$", "left")
    d += elm.Dot().at((2.2, 1.2))
    d += elm.Switch().at((2.2, 1.2)).to((2.2, 0)).label("$S_2$", "left")
    d += elm.Line().at((2.2, 1.2)).to((3.8, 1.2)).label("fase $a$", "right")
    d.save(os.path.join(OUT, "convertidor-vsc-rama.png"), dpi=140)
    print("convertidor-vsc-rama.png")


# ===================================================================== #
#  anti-windup
# ===================================================================== #
@figura("anti-windup")
def _antiwindup():
    dt = 1e-3; T = np.arange(0, 3, dt); tau = 0.3; Kp, Ki, umax = 2.0, 8.0, 1.0
    ref = np.where(T < 1.5, 1.6, 0.3)
    def sim(aw):
        y = 0.0; I = 0.0; out = []
        for r in ref:
            e = r - y; u = Kp*e + I; usat = min(max(u, -umax), umax)
            I += (Ki*e + (5.0*(usat-u) if aw else 0.0))*dt
            y += (-y + usat)/tau*dt; out.append(y)
        return np.array(out)
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    ax.plot(T, ref, color="#aaa", ls=":", label="referencia")
    ax.plot(T, sim(False), color=BAD, lw=2, label="sin anti-windup")
    ax.plot(T, sim(True), color=ACC, lw=2, label="con anti-windup")
    ax.set_xlabel("t [s]"); ax.set_ylabel("salida y")
    ax.set_title("Anti-windup: recuperación tras una saturación prolongada")
    ax.legend(fontsize=8, loc="upper right"); ax.grid(True, alpha=0.4)
    fig.tight_layout()
    _savefig(fig, "anti-windup-respuesta.png")


# ===================================================================== #
#  transformada-laplace
# ===================================================================== #
@figura("transformada-laplace")
def _laplace():
    t = np.linspace(0, 3, 400)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.6, 3.6))
    a1.plot(t, np.exp(-2*t), color=ACC, lw=2, label="$e^{-2t}$")
    a1.plot(t, np.exp(-0.7*t)*np.cos(4*t), color=BAD, lw=2, label="$e^{-0.7t}\\cos 4t$")
    a1.axhline(0, color="#bbb", lw=0.6); a1.set_title("señales en el tiempo")
    a1.set_xlabel("t"); a1.legend(fontsize=8); a1.grid(True, alpha=0.4)
    a2.axvspan(-3, 0, color=OK, alpha=0.07)
    a2.scatter([-2], [0], marker="x", s=90, color=ACC, lw=2.2)
    a2.scatter([-0.7, -0.7], [4, -4], marker="x", s=90, color=BAD, lw=2.2)
    a2.axvline(0, color="k", lw=1.1); a2.axhline(0, color="#bbb", lw=0.6)
    a2.set_xlim(-3, 1); a2.set_title("sus polos en el plano s")
    a2.set_xlabel("Re(s)=σ"); a2.set_ylabel("Im(s)=ω"); a2.grid(True, alpha=0.3)
    fig.suptitle("Laplace: cada señal temporal ↔ polos en s (σ=decaimiento, ω=oscilación)", fontsize=10.5)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    _savefig(fig, "transformada-laplace-pares.png")


# ===================================================================== #
#  transformada-z
# ===================================================================== #
@figura("transformada-z")
def _ztransform():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.4, 4.0))
    a1.axvspan(-3, 0, color=OK, alpha=0.1)
    a1.axvline(0, color="k", lw=1.2); a1.axhline(0, color="#bbb", lw=0.6)
    a1.set_title("plano s: estable si Re(s)<0"); a1.set_xlabel("Re(s)"); a1.set_ylabel("Im(s)")
    a1.set_xlim(-3, 1.5); a1.set_ylim(-3, 3); a1.grid(True, alpha=0.3)
    a1.text(-1.5, 2.4, "semiplano\nizquierdo", color="#2a7", fontsize=9, ha="center")
    th = np.linspace(0, 2*np.pi, 200)
    a2.fill(np.cos(th), np.sin(th), color=OK, alpha=0.12)
    a2.plot(np.cos(th), np.sin(th), color="k", lw=1.2)
    a2.axvline(0, color="#bbb", lw=0.6); a2.axhline(0, color="#bbb", lw=0.6)
    a2.scatter([1, -1], [0, 0], color="#555", s=20)
    a2.text(0.55, 0.12, "z=1 (DC)", fontsize=8); a2.text(-1.45, 0.12, "z=−1 ($f_s$/2)", fontsize=8)
    a2.set_title("plano z: estable si |z|<1"); a2.set_xlabel("Re(z)"); a2.set_ylabel("Im(z)")
    a2.set_xlim(-1.6, 1.6); a2.set_ylim(-1.4, 1.4); a2.set_aspect("equal"); a2.grid(True, alpha=0.3)
    fig.suptitle("$z=e^{sT_s}$: el semiplano izquierdo de s ↦ el interior del círculo unidad de z", fontsize=10.5)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    _savefig(fig, "transformada-z-planos.png")


# ===================================================================== #
#  sintonia-pi-pid
# ===================================================================== #
@figura("sintonia-pi-pid")
def _sintonia():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.6, 3.6))
    a1.axvspan(-30, 0, color=OK, alpha=0.07)
    a1.scatter([-25], [0], marker="x", s=130, color=ACC, lw=2.5, label="polo de planta")
    a1.scatter([-25], [0], marker="o", s=190, facecolors="none", edgecolors=BAD, lw=2, label="cero del PI")
    a1.annotate("cancelación\npolo–cero", xy=(-25, 0), xytext=(-18, 1.6), fontsize=9, ha="center",
                arrowprops=dict(arrowstyle="->", color="#444"))
    a1.axvline(0, color="k", lw=1.1); a1.axhline(0, color="#bbb", lw=0.6)
    a1.set_xlim(-30, 4); a1.set_ylim(-3, 3)
    a1.set_title("el PI cancela el polo de la planta"); a1.set_xlabel("Re(s)")
    a1.legend(fontsize=8, loc="lower left"); a1.grid(True, alpha=0.3)
    wc = 6283.0
    tt, y = signal.step(signal.TransferFunction([wc], [1, wc]), T=np.linspace(0, 1e-3, 300))
    a2.plot(tt*1e3, y, color=ACC, lw=2.2); a2.axhline(1, color="#aaa", ls=":")
    a2.set_title("lazo cerrado resultante (1er orden, $f_c$≈1 kHz)")
    a2.set_xlabel("t [ms]"); a2.set_ylabel("i(t)"); a2.grid(True, alpha=0.4)
    fig.suptitle("Sintonía por cancelación de polo: $K_p=L\\,\\omega_c$, $K_i=R\\,\\omega_c$", fontsize=10.5)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    _savefig(fig, "sintonia-pi-pid-cancelacion.png")


# ===================================================================== #
#  variables-estado
# ===================================================================== #
@figura("variables-estado")
def _varestado():
    d = schemdraw.Drawing()
    d.config(fontsize=11)
    d += elm.SourceV().at((0, 0)).to((0, 2)).label("$v_{in}$", "left")
    d += elm.Line().at((0, 2)).to((0.8, 2))
    d += elm.Inductor2().at((0.8, 2)).to((3.2, 2)).label("$L$   ($i_L$ = estado)", "top")
    d += elm.Dot().at((3.2, 2))
    d += elm.Capacitor().at((3.2, 2)).to((3.2, 0)).label("$C$   ($v_C$ = estado)", "right")
    d += elm.Line().at((3.2, 0)).to((0, 0))
    d.save(os.path.join(OUT, "variables-estado-circuito.png"), dpi=140)
    print("variables-estado-circuito.png")


# ===================================================================== #
#  sistema-trifasico
# ===================================================================== #
@figura("sistema-trifasico")
def _trifasico():
    t = np.linspace(0, 0.02, 500); w = 2*np.pi*50
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.6, 3.4))
    a1.plot(t*1e3, np.cos(w*t), color=ACC, label="a")
    a1.plot(t*1e3, np.cos(w*t - 2*np.pi/3), color=BAD, label="b")
    a1.plot(t*1e3, np.cos(w*t + 2*np.pi/3), color=OK, label="c")
    a1.axhline(0, color="#bbb", lw=0.6)
    a1.set_title("tres tensiones desfasadas 120°"); a1.set_xlabel("t [ms]"); a1.set_ylabel("v [pu]")
    a1.legend(fontsize=8, ncol=3, loc="lower center"); a1.grid(True, alpha=0.4)
    for ang, c, lb in [(90, ACC, "a"), (-30, BAD, "b"), (210, OK, "c")]:
        x, y = np.cos(np.radians(ang)), np.sin(np.radians(ang))
        a2.annotate("", xy=(x, y), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=c, lw=2.5))
        a2.text(1.15*x, 1.15*y, lb, color=c, fontsize=11, ha="center", va="center")
    a2.set_xlim(-1.4, 1.4); a2.set_ylim(-1.4, 1.4); a2.set_aspect("equal")
    a2.axhline(0, color="#ddd", lw=0.6); a2.axvline(0, color="#ddd", lw=0.6)
    a2.set_title("fasores ($v_a+v_b+v_c=0$)"); a2.set_xticks([]); a2.set_yticks([])
    fig.tight_layout()
    _savefig(fig, "sistema-trifasico-ondas.png")


# ===================================================================== #
#  transformada-clarke
# ===================================================================== #
@figura("transformada-clarke")
def _clarke():
    fig, ax = plt.subplots(figsize=(5.6, 5.2)); L = 1.2
    for ang, lb in [(0, "a"), (120, "b"), (240, "c")]:
        x, y = L*np.cos(np.radians(ang)), L*np.sin(np.radians(ang))
        ax.plot([0, x], [0, y], color="#bbb", ls="--", lw=1.5)
        ax.text(x*1.12, y*1.12, lb, color="#777", fontsize=11, ha="center")
    ax.annotate("", xy=(L, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=ACC, lw=2.5))
    ax.annotate("", xy=(0, L), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=ACC2, lw=2.5))
    ax.text(L*1.08, 0.06, "α", color=ACC, fontsize=13); ax.text(0.06, L*1.08, "β", color=ACC2, fontsize=13)
    vx, vy = 0.8, 0.45
    ax.annotate("", xy=(vx, vy), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=BAD, lw=2.5))
    ax.text(vx*1.06, vy*1.12, "$\\vec x$", color=BAD, fontsize=13)
    ax.plot([vx, vx], [vy, 0], color="#888", ls=":", lw=1); ax.plot([vx, 0], [vy, vy], color="#888", ls=":", lw=1)
    ax.text(vx/2, -0.13, "$x_\\alpha$", color=ACC, fontsize=10, ha="center"); ax.text(-0.16, vy/2, "$x_\\beta$", color=ACC2, fontsize=10)
    ax.set_xlim(-1.4, 1.5); ax.set_ylim(-1.4, 1.5); ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("Clarke: las 3 fases (a,b,c) → 2 ejes ortogonales (α,β)")
    fig.tight_layout()
    _savefig(fig, "transformada-clarke-ejes.png")


# ===================================================================== #
#  potencia-ac-fasores
# ===================================================================== #
@figura("potencia-ac-fasores")
def _potfasor():
    P, Q = 1.0, 0.6
    fig, ax = plt.subplots(figsize=(5.8, 4.2))
    ax.annotate("", xy=(P, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=ACC, lw=2.5))
    ax.annotate("", xy=(P, Q), xytext=(P, 0), arrowprops=dict(arrowstyle="-|>", color=ACC2, lw=2.5))
    ax.annotate("", xy=(P, Q), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=BAD, lw=2.5))
    ax.text(P/2, -0.08, "P (activa, W)", color=ACC, fontsize=10, ha="center")
    ax.text(P+0.03, Q/2, "Q (reactiva, var)", color=ACC2, fontsize=10)
    ax.text(P/2-0.16, Q/2+0.04, "S (aparente, VA)", color=BAD, fontsize=10, rotation=np.degrees(np.arctan2(Q, P)))
    th = np.linspace(0, np.arctan2(Q, P), 20); ax.plot(0.28*np.cos(th), 0.28*np.sin(th), color="#666", lw=1)
    ax.text(0.33, 0.05, "φ", fontsize=12)
    ax.set_xlim(-0.1, 1.35); ax.set_ylim(-0.2, 0.9); ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("Triángulo de potencia:  $S^2=P^2+Q^2$,   FP = cos φ = P/S")
    fig.tight_layout()
    _savefig(fig, "potencia-ac-fasores-triangulo.png")


# ===================================================================== #
#  transferencia-potencia-linea
# ===================================================================== #
@figura("transferencia-potencia-linea")
def _pdelta():
    d = np.linspace(0, np.pi, 300)
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.plot(np.degrees(d), np.sin(d), color=ACC, lw=2.4, label="$P=\\frac{VE}{X}\\sin\\delta$")
    dd = np.linspace(0, 45, 10)
    ax.plot(dd, np.radians(dd), color=BAD, ls="--", lw=1.6, label="rigidez $\\partial P/\\partial\\delta=VE/X$")
    ax.axvline(90, color="#bbb", ls=":"); ax.text(92, 0.25, "δ=90°\n(máx. P)", fontsize=8)
    ax.set_xlabel("ángulo δ [°]"); ax.set_ylabel("P [pu de VE/X]")
    ax.set_title("Potencia transmitida frente al ángulo (línea inductiva)")
    ax.legend(fontsize=8, loc="upper right"); ax.grid(True, alpha=0.4); ax.set_ylim(0, 1.18)
    fig.tight_layout()
    _savefig(fig, "transferencia-potencia-linea-pdelta.png")


# ===================================================================== #
#  valor-rms-factor-potencia
# ===================================================================== #
@figura("valor-rms-factor-potencia")
def _rms():
    t = np.linspace(0, 0.02, 500); x = np.sin(2*np.pi*50*t); rms = 1/np.sqrt(2)
    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    ax.plot(t*1e3, x, color=ACC, lw=2, label="v(t), pico = 1")
    ax.axhline(rms, color=BAD, ls="--", lw=1.6, label=f"RMS = pico/√2 ≈ {rms:.3f}")
    ax.axhline(-rms, color=BAD, ls="--", lw=1.6)
    ax.axhline(0, color="#bbb", lw=0.6)
    ax.set_xlabel("t [ms]"); ax.set_ylabel("v [pu]")
    ax.set_title("Valor eficaz (RMS) de una senoide = pico / √2")
    ax.legend(fontsize=8, loc="lower right"); ax.grid(True, alpha=0.4)
    fig.tight_layout()
    _savefig(fig, "valor-rms-factor-potencia-rms.png")


# ===================================================================== #
#  muestreo-aliasing
# ===================================================================== #
@figura("muestreo-aliasing")
def _aliasing():
    tc = np.linspace(0, 0.02, 2000); fs = 1000.0
    ts = np.arange(0, 0.02, 1/fs)
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ax.plot(tc*1e3, np.sin(2*np.pi*900*tc), color="#bbb", lw=1.2, label="señal real 900 Hz")
    ax.plot(tc*1e3, -np.sin(2*np.pi*100*tc), color=ACC, lw=2, ls="--", label="alias 100 Hz")
    ax.plot(ts*1e3, np.sin(2*np.pi*900*ts), "o", color=BAD, ms=7, label="muestras (fs=1 kHz)")
    ax.set_xlabel("t [ms]"); ax.set_ylabel("amplitud")
    ax.set_title("Aliasing: 900 Hz muestreada a 1 kHz se confunde con 100 Hz")
    ax.legend(fontsize=8, loc="upper right"); ax.grid(True, alpha=0.4)
    fig.tight_layout()
    _savefig(fig, "muestreo-aliasing-alias.png")


# ===================================================================== #
#  series-fourier
# ===================================================================== #
@figura("series-fourier")
def _fourier():
    t = np.linspace(0, 1, 1000)
    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    ax.plot(t, np.sign(np.sin(2*np.pi*t)), color="#bbb", lw=1.5, label="onda cuadrada")
    for N, c in [(1, ACC), (3, OK), (9, BAD)]:
        y = sum((4/np.pi)*np.sin(2*np.pi*k*t)/k for k in range(1, N+1, 2))
        ax.plot(t, y, color=c, lw=2, label=f"hasta armónico {N}")
    ax.set_xlabel("t / T"); ax.set_ylabel("x(t)")
    ax.set_title("Serie de Fourier: suma de armónicos impares (∝1/k) → onda cuadrada")
    ax.legend(fontsize=8, loc="upper right"); ax.grid(True, alpha=0.4)
    fig.tight_layout()
    _savefig(fig, "series-fourier-cuadrada.png")


# ===================================================================== #
#  compensador-adelanto-atraso
# ===================================================================== #
@figura("compensador-adelanto-atraso")
def _leadlag():
    alpha, T = 6.0, 0.05
    sys = signal.TransferFunction([alpha*T, 1], [T, 1])
    w = np.logspace(-1, 3, 1500); w, mag, phase = signal.bode(sys, w); f = w/(2*np.pi)
    fm = 1/(T*np.sqrt(alpha))/(2*np.pi); phimax = np.degrees(np.arcsin((alpha-1)/(alpha+1)))
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.6, 4.8), sharex=True)
    a1.semilogx(f, mag, color=ACC, lw=2); a2.semilogx(f, phase, color=ACC, lw=2)
    a2.axvline(fm, color=BAD, ls=":")
    a2.annotate(f"$\\phi_{{max}}$≈{phimax:.0f}°", xy=(fm, phimax), xytext=(fm*2.2, phimax*0.55),
                fontsize=9, color=BAD, arrowprops=dict(arrowstyle="->", color=BAD))
    a1.set_ylabel("|C| [dB]"); a2.set_ylabel("∠C [°]"); a2.set_xlabel("frecuencia [Hz]")
    a1.set_title("Compensador de adelanto (lead): aporta fase cerca del cruce")
    a1.grid(True, which="both", alpha=0.4); a2.grid(True, which="both", alpha=0.4)
    fig.tight_layout()
    _savefig(fig, "compensador-adelanto-atraso-bode.png")


# ===================================================================== #
#  filtro-notch
# ===================================================================== #
@figura("filtro-notch")
def _notch():
    wn = 2*np.pi*1000; zz, zp = 0.02, 0.5
    sys = signal.TransferFunction([1, 2*zz*wn, wn**2], [1, 2*zp*wn, wn**2])
    w = np.logspace(1.5, 4, 2000); w, mag, phase = signal.bode(sys, w); f = w/(2*np.pi)
    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    ax.semilogx(f, mag, color=ACC, lw=2)
    ax.axvline(1000, color="#bbb", ls="--"); ax.text(1060, -22, "$f_n$=1 kHz", fontsize=9, color="#555")
    ax.set_xlabel("frecuencia [Hz]"); ax.set_ylabel("|N| [dB]")
    ax.set_title("Filtro notch: muesca profunda en $f_n$, el resto casi intacto")
    ax.grid(True, which="both", alpha=0.4)
    fig.tight_layout()
    _savefig(fig, "filtro-notch-respuesta.png")


# ===================================================================== #
#  controlador-resonante
# ===================================================================== #
@figura("controlador-resonante")
def _resonante():
    w0, wc, Kp, Kr = 2*np.pi*50, 5.0, 1.0, 200.0
    sys = signal.TransferFunction([Kp, 2*(Kr*wc + Kp*wc), Kp*w0**2], [1, 2*wc, w0**2])
    w = np.logspace(0, 3, 3000); w, mag, phase = signal.bode(sys, w); f = w/(2*np.pi)
    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    ax.semilogx(f, mag, color=ACC, lw=2)
    ax.axvline(50, color="#bbb", ls="--"); ax.text(54, mag.max()-7, "$f_0$=50 Hz", fontsize=9, color="#555")
    ax.set_xlabel("frecuencia [Hz]"); ax.set_ylabel("|$G_{PR}$| [dB]")
    ax.set_title("Controlador PR: ganancia enorme en $f_0$ → error nulo a esa senoide")
    ax.grid(True, which="both", alpha=0.4)
    fig.tight_layout()
    _savefig(fig, "controlador-resonante-respuesta.png")


# ===================================================================== #
#  componentes-simetricas
# ===================================================================== #
@figura("componentes-simetricas")
def _simetricas():
    fig, axs = plt.subplots(1, 3, figsize=(9.0, 3.4))
    cols = [ACC, BAD, OK]; labs = ["a", "b", "c"]
    seqs = [("positiva (+)", [90, -30, 210]), ("negativa (−)", [90, 210, -30]),
            ("homopolar (0)", [90, 90, 90])]
    for ax, (title, angs) in zip(axs, seqs):
        for i, (ang, c, lb) in enumerate(zip(angs, cols, labs)):
            if "homopolar" in title:
                ox = (i-1)*0.22; x0, y0, x1, y1 = ox, 0, ox, 1.0
            else:
                x0, y0 = 0, 0; x1, y1 = np.cos(np.radians(ang)), np.sin(np.radians(ang))
            ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="-|>", color=c, lw=2.2))
            ax.text(x1*(1.0 if "homopolar" in title else 1.15), y1+0.12, lb, color=c, fontsize=10, ha="center")
        ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5); ax.set_aspect("equal")
        ax.axhline(0, color="#eee", lw=0.5); ax.axvline(0, color="#eee", lw=0.5)
        ax.set_title(title, fontsize=10); ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle("Componentes simétricas: tres ternas (positiva, negativa, homopolar)", fontsize=10.5)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    _savefig(fig, "componentes-simetricas-fasores.png")


# ===================================================================== #
#  fotovoltaica-mppt
# ===================================================================== #
@figura("fotovoltaica-mppt")
def _pv():
    Voc, Isc, a = 40.0, 8.0, 3.0
    V = np.linspace(0, Voc, 400)
    I = np.clip(Isc*(1 - np.exp((V - Voc)/a)), 0, None)
    P = V*I; im = int(np.argmax(P))
    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    ax.plot(V, I, color=ACC, lw=2)
    ax.set_xlabel("V [V]"); ax.set_ylabel("I [A]", color=ACC); ax.tick_params(axis="y", labelcolor=ACC)
    ax.grid(True, alpha=0.4)
    ax2 = ax.twinx()
    ax2.plot(V, P, color=BAD, lw=2); ax2.set_ylabel("P [W]", color=BAD); ax2.tick_params(axis="y", labelcolor=BAD)
    ax2.scatter([V[im]], [P[im]], color=BAD, s=60, zorder=5)
    ax2.annotate("MPP", xy=(V[im], P[im]), xytext=(V[im]-13, P[im]*0.95),
                 fontsize=10, color=BAD, arrowprops=dict(arrowstyle="->", color=BAD))
    ax.set_title("Curva I–V (azul) y P–V (rojo) de un módulo PV: el MPPT busca el MPP")
    fig.tight_layout()
    _savefig(fig, "fotovoltaica-mppt-iv.png")


# ===================================================================== #
#  convertidor-dc-dc
# ===================================================================== #
@figura("convertidor-dc-dc")
def _dcdc():
    D = np.linspace(0.05, 0.92, 200)
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.plot(D, D, color=ACC, lw=2.4, label="buck:  $V_o/V_{in}=D$")
    ax.plot(D, 1/(1-D), color=BAD, lw=2.4, label="boost:  $V_o/V_{in}=1/(1-D)$")
    ax.axhline(1, color="#bbb", ls=":")
    ax.set_xlabel("ciclo de trabajo D"); ax.set_ylabel("$V_o/V_{in}$")
    ax.set_title("Relación de conversión DC-DC en conducción continua")
    ax.legend(fontsize=9); ax.grid(True, alpha=0.4); ax.set_ylim(0, 6)
    fig.tight_layout()
    _savefig(fig, "convertidor-dc-dc-ratio.png")


# ===================================================================== #
#  rectificador-afe
# ===================================================================== #
@figura("rectificador-afe")
def _afe():
    d = schemdraw.Drawing()
    d.config(unit=1.0, fontsize=10.5)
    d += dsp.Arrow().right(1.2).label("red AC", "left")
    afe = d.add(dsp.Box(w=3.8, h=1.6).anchor("W").label("AFE = VSC controlado\nPLL + lazo $i_{dq}$\n+ lazo de $V_{dc}$"))
    d += dsp.Arrow().right(1.2).at(afe.E).label("$V_{dc}$", "top")
    d += dsp.Box(w=2.0, h=1.6).anchor("W").label("bus DC\n+ carga")
    d += dsp.Arrow().left(1.2).at((afe.E[0]+1.2, afe.E[1]-0.55)).label("P  ↔  bidireccional", "bottom")
    d.save(os.path.join(OUT, "rectificador-afe-bloques.png"), dpi=140)
    print("rectificador-afe-bloques.png")


# ===================================================================== #
#  transformador
# ===================================================================== #
@figura("transformador")
def _trafo():
    d = schemdraw.Drawing()
    d.config(fontsize=12)
    T = d.add(elm.Transformer(t1=4, t2=4))
    d += elm.Line().left(0.7).at(T.p1)
    d += elm.Line().left(0.7).at(T.p2)
    d += elm.Gap().at(T.p1).to(T.p2).label(("+", "$V_1$", "−"))
    d += elm.Line().right(0.7).at(T.s1)
    d += elm.Line().right(0.7).at(T.s2)
    d += elm.Gap().at(T.s1).to(T.s2).label(("+", "$V_2$", "−"))
    d.save(os.path.join(OUT, "transformador-simbolo.png"), dpi=140)
    print("transformador-simbolo.png")


# ===================================================================== #
#  semiconductores-potencia
# ===================================================================== #
@figura("semiconductores-potencia")
def _semi():
    t = np.linspace(0, 1, 500)
    V = 1/(1 + np.exp(-(t-0.45)/0.03))
    I = 1 - 1/(1 + np.exp(-(t-0.55)/0.03))
    P = V*I
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    ax.plot(t, V, color=ACC, lw=2, label="V (tensión)")
    ax.plot(t, I, color=OK, lw=2, label="I (corriente)")
    ax.fill_between(t, P, color=BAD, alpha=0.22)
    ax.plot(t, P, color=BAD, lw=2, label="P = V·I (pérdida)")
    ax.set_xlabel("tiempo (durante la transición de conmutación)"); ax.set_ylabel("pu")
    ax.set_title("Pérdida de conmutación: V e I se solapan en cada transición")
    ax.legend(fontsize=8, loc="upper left"); ax.grid(True, alpha=0.4); ax.set_xticks([])
    fig.tight_layout()
    _savefig(fig, "semiconductores-potencia-conmutacion.png")


# ===================================================================== #
#  dinamica-bus-dc
# ===================================================================== #
@figura("dinamica-bus-dc")
def _busdc():
    dt = 1e-4; T = np.arange(0, 0.15, dt); C = 50e-3; Vref = 700.0; Kp, Ki = 300.0, 6000.0
    Pout = np.where(T < 0.03, 40e3, 60e3)
    def sim(closed):
        V = 700.0; I = 0.0; out = []
        for Po in Pout:
            Pin = (40e3 + Kp*(Vref-V) + I) if closed else 40e3
            if closed:
                I += Ki*(Vref-V)*dt
            V += (Pin - Po)/(C*V)*dt; out.append(V)
        return out
    fig, ax = plt.subplots(figsize=(6.8, 3.6))
    ax.plot(T*1e3, sim(False), color=BAD, lw=2, label="sin control (C integra → cae)")
    ax.plot(T*1e3, sim(True), color=ACC, lw=2, label="con lazo de tensión (recupera)")
    ax.axhline(Vref, color="#aaa", ls=":")
    ax.axvline(30, color="#888", ls="--", lw=1); ax.text(32, 690, "escalón de carga", fontsize=8, color="#555")
    ax.set_xlabel("t [ms]"); ax.set_ylabel("$V_{dc}$ [V]")
    ax.set_title("Bus DC: C·dV/dt = Pin − Pout (el condensador integra el desbalance)")
    ax.legend(fontsize=8, loc="lower left"); ax.grid(True, alpha=0.4)
    fig.tight_layout()
    _savefig(fig, "dinamica-bus-dc-respuesta.png")


# ===================================================================== #
#  ecuacion-oscilacion
# ===================================================================== #
@figura("ecuacion-oscilacion")
def _swing():
    dt = 1e-3; T = np.arange(0, 5, dt); H, D, w0 = 4.0, 16.0, 2*np.pi*50
    E, Vg, X = 1.05, 1.0, 0.3
    delta = np.arcsin(0.5*X/(E*Vg)); dw = 0.0
    Pm = np.where(T < 0.5, 0.5, 0.8)
    ds = []
    for P in Pm:
        Pe = E*Vg/X*np.sin(delta)
        dw += (P - Pe - D*dw)/(2*H)*dt
        delta += w0*dw*dt
        ds.append(np.degrees(delta))
    fig, ax = plt.subplots(figsize=(6.8, 3.6))
    ax.plot(T, ds, color=ACC, lw=2)
    ax.axvline(0.5, color=BAD, ls="--", lw=1); ax.text(0.6, ds[0]+1, "escalón de $P_m$", fontsize=8, color=BAD)
    ax.set_xlabel("t [s]"); ax.set_ylabel("ángulo δ [°]")
    ax.set_title("Ecuación de oscilación: el ángulo oscila y se asienta tras un cambio de potencia")
    ax.grid(True, alpha=0.4)
    fig.tight_layout()
    _savefig(fig, "ecuacion-oscilacion-swing.png")


# ===================================================================== #
#  routh-hurwitz
# ===================================================================== #
@figura("routh-hurwitz")
def _routh():
    # Raices de s^3 + 3 s^2 + 2 s + Kp al barrer Kp; cruzan jw en Kp=6 (±j√2)
    Kps = np.linspace(0, 8, 49)
    allr, allk = [], []
    for Kp in Kps:
        for ri in np.roots([1, 3, 2, Kp]):
            allr.append(ri); allk.append(Kp)
    allr = np.array(allr)
    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    sc = ax.scatter(allr.real, allr.imag, c=allk, cmap="plasma", s=16)
    fig.colorbar(sc, label="$K_p$")
    ax.axvline(0, color=BAD, ls="--", lw=1.2)
    ax.plot([0, 0], [np.sqrt(2), -np.sqrt(2)], "X", color="k", ms=9, zorder=4)
    ax.annotate("límite $K_p=6$\n$s=\\pm j\\sqrt{2}$", xy=(0, np.sqrt(2)),
                xytext=(-1.7, 1.05), fontsize=8, ha="center",
                arrowprops=dict(arrowstyle="->", color="k", lw=1))
    ax.text(-2.6, -0.55, "estable\n(Re<0,  $0<K_p<6$)", color=OK, fontsize=8, ha="center")
    ax.set_xlabel("Re(s)"); ax.set_ylabel("Im(s)")
    ax.set_title("Routh-Hurwitz: raíces de $s^3+3s^2+2s+K_p$")
    fig.tight_layout()
    _savefig(fig, "routh-hurwitz-locus.png")


# ===================================================================== #
#  estabilidad-lyapunov
# ===================================================================== #
@figura("estabilidad-lyapunov")
def _lyap():
    A = np.array([[-0.3, 1.0], [-1.0, -0.3]])   # foco estable
    dt, N = 0.01, 1500
    x = np.array([2.6, 0.0]); traj = [x.copy()]
    for _ in range(N):
        x = x + dt*(A @ x); traj.append(x.copy())
    traj = np.array(traj); t = np.arange(N+1)*dt
    V = traj[:, 0]**2 + traj[:, 1]**2
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.2, 3.9))
    g = np.linspace(-3, 3, 240); X, Y = np.meshgrid(g, g); Z = X**2 + Y**2
    a1.contour(X, Y, Z, levels=[1, 4, 9], colors="#bbb", linewidths=1)
    a1.plot(traj[:, 0], traj[:, 1], color=ACC, lw=2)
    a1.plot(traj[0, 0], traj[0, 1], "o", color=OK, label="inicio")
    a1.plot(0, 0, "o", color=BAD, label="equilibrio")
    a1.set_aspect("equal"); a1.set_xlabel("$x_1$"); a1.set_ylabel("$x_2$")
    a1.set_title("La trayectoria desciende por $V$"); a1.legend(fontsize=8)
    a2.plot(t, V, color=ACC, lw=2)
    a2.set_xlabel("t [s]"); a2.set_ylabel("$V(x)$")
    a2.set_title("$V(x(t))$ decrece: $\\dot V<0$ ⟹ estable")
    fig.tight_layout()
    _savefig(fig, "estabilidad-lyapunov-V.png")


# ===================================================================== #
#  impedancia-virtual
# ===================================================================== #
@figura("impedancia-virtual")
def _zvirt():
    V = 1.0; d = np.linspace(0, np.pi/2, 200); dd = np.degrees(d)
    X1, X2 = 0.10, 0.25                         # fisico vs fisico + Xv
    P1 = 1.5*V**2/X1*np.sin(d); P2 = 1.5*V**2/X2*np.sin(d)
    d0 = np.radians(20)
    fig, ax = plt.subplots(figsize=(6.8, 4.1))
    ax.plot(dd, P1, color=BAD, lw=2, label="$X$ físico = 0.10 pu  (pendiente alta)")
    ax.plot(dd, P2, color=ACC, lw=2, label="$X+X_v$ = 0.25 pu  (pendiente menor)")
    for X, c in [(X1, BAD), (X2, ACC)]:
        P0 = 1.5*V**2/X*np.sin(d0); m = 1.5*V**2/X*np.cos(d0)
        dl = np.radians(np.array([10.0, 30.0]))
        ax.plot(np.degrees(dl), P0 + m*(dl - d0), color=c, ls=":", lw=1.4)
        ax.plot(20, P0, "o", color=c, ms=6)
    ax.set_xlabel("ángulo de potencia δ [°]"); ax.set_ylabel("P [pu]")
    ax.set_title("Impedancia virtual: más reactancia → menor $\\partial P/\\partial\\delta$")
    ax.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    _savefig(fig, "impedancia-virtual-pd.png")


# ===================================================================== #
#  vsm-inercia
# ===================================================================== #
@figura("vsm-inercia")
def _vsm():
    # Respuesta de frecuencia a un escalon de carga: droop (salto instantaneo) vs VSM (RoCoF limitado)
    T = np.arange(0, 3, 1e-3); t0 = 0.5
    df_ss, tau = -0.30, 0.45                     # tau ~ J/D (H=4 s)
    fvsm = 50 + np.where(T < t0, 0.0, df_ss*(1 - np.exp(-(T - t0)/tau)))
    fdroop = 50 + np.where(T < t0, 0.0, df_ss)
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    ax.plot(T, fdroop, color=BAD, lw=2, label="droop puro: $f$ salta (sin inercia)")
    ax.plot(T, fvsm, color=ACC, lw=2, label="VSM (H=4 s): RoCoF limitado")
    ax.axvline(t0, color="#888", ls="--", lw=1); ax.text(t0+0.03, 49.95, "escalón de carga", fontsize=8)
    rocof = df_ss/tau
    ax.plot([t0, t0+0.4], [50, 50 + rocof*0.4], color="#444", ls=":", lw=1.4)
    ax.text(t0+0.42, 50 + rocof*0.4, "RoCoF\n$\\propto 1/J$", fontsize=8, va="top")
    ax.set_xlabel("t [s]"); ax.set_ylabel("frecuencia [Hz]")
    ax.set_title("Inercia virtual (VSM) frente a droop ante un escalón de potencia")
    ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    _savefig(fig, "vsm-inercia-rocof.png")


# ===================================================================== #
#  observador-estados
# ===================================================================== #
@figura("observador-estados")
def _obs():
    A = np.array([[0.0, 1.0], [-20.0, -2.0]]); C = np.array([[1.0, 0.0]])
    L = np.array([28.0, 174.0])                  # polos observador en -15±j5 (rapidos)
    dt, T = 1e-3, np.arange(0, 1.2, 1e-3)
    x = np.array([1.0, 0.0]); xh = np.array([0.0, 0.0])
    X, XH = [], []
    for _ in T:
        X.append(x.copy()); XH.append(xh.copy())
        y = C @ x
        x = x + dt*(A @ x)
        xh = xh + dt*(A @ xh + L*(y - C @ xh)[0])
    X, XH = np.array(X), np.array(XH)
    err = np.linalg.norm(X - XH, axis=1)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.2, 3.8))
    a1.plot(T, X[:, 1], color=ACC, lw=2, label="$x_2$ real (no medido)")
    a1.plot(T, XH[:, 1], color=BAD, ls="--", lw=2, label="$\\hat x_2$ estimado")
    a1.set_xlabel("t [s]"); a1.set_ylabel("$x_2$"); a1.legend(fontsize=8)
    a1.set_title("El observador estima el estado no medido")
    a2.semilogy(T, err + 1e-12, color=OK, lw=2)
    a2.set_xlabel("t [s]"); a2.set_ylabel("$\\|e\\|$")
    a2.set_title("Error $e=x-\\hat x \\to 0$ (polos de $A-LC$ estables)")
    fig.tight_layout()
    _savefig(fig, "observador-estados-convergencia.png")


# ===================================================================== #
#  compensacion-retardo
# ===================================================================== #
@figura("compensacion-retardo")
def _delay():
    # Fase que resta el retardo Td = 1.5 Ts en funcion de la frecuencia
    f = np.linspace(10, 5000, 600); w = 2*np.pi*f
    fig, ax = plt.subplots(figsize=(6.8, 4.1))
    for Ts, c, lbl in [(1e-4, ACC, "$T_s$=100 µs"), (5e-5, ACC2, "$T_s$=50 µs")]:
        Td = 1.5*Ts
        ax.plot(f, np.degrees(w*Td), color=c, lw=2, label=f"$T_d=1.5\\,T_s$  ({lbl})")
    fc = 1000.0; ph = np.degrees(2*np.pi*fc*1.5e-4)
    ax.axvline(fc, color=BAD, ls="--", lw=1.2)
    ax.plot(fc, ph, "o", color=BAD, ms=7)
    ax.annotate(f"a $f_c=f_s/10$:\n{ph:.0f}° de margen perdido", xy=(fc, ph),
                xytext=(1500, ph-22), fontsize=8,
                arrowprops=dict(arrowstyle="->", color=BAD, lw=1))
    ax.set_xlabel("frecuencia [Hz]"); ax.set_ylabel("fase restada $|\\Delta\\phi|$ [°]")
    ax.set_title("Retardo de cómputo+PWM: $\\Delta\\phi=-\\omega T_d$")
    ax.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    _savefig(fig, "compensacion-retardo-fase.png")


# ===================================================================== #
#  control-feedforward
# ===================================================================== #
@figura("control-feedforward")
def _ff():
    # Desviacion de corriente ante un hueco de red, con y sin feedforward de tension
    L, Ts = 2e-3, 2e-5
    T = np.arange(0, 0.012, Ts); k0 = int(0.003/Ts)
    vgrid = np.where(T >= 0.003, 0.3*325, 0.0)         # hueco/escalón 0.3 pu
    fc = 500.0; Kp = 2*np.pi*fc*L; Ki = Kp*2*np.pi*100
    def sim(ff):
        i = 0.0; xi = 0.0; out = []
        for k in range(len(T)):
            e = 0.0 - i; xi += e*Ts
            vmeas = vgrid[k-1] if (ff and k > 0) else 0.0   # ff con 1 muestra de retardo
            vconv = Kp*e + Ki*xi + vmeas
            i += (vconv - vgrid[k])/L*Ts
            out.append(i)
        return np.array(out)
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    ax.plot(T*1e3, sim(False), color=BAD, lw=2, label="solo feedback (PI)")
    ax.plot(T*1e3, sim(True), color=ACC, lw=2, label="feedback + feedforward de red")
    ax.axvline(3, color="#888", ls="--", lw=1); ax.text(3.1, ax.get_ylim()[0]*0.9, "hueco de red", fontsize=8)
    ax.set_xlabel("t [ms]"); ax.set_ylabel("desviación de corriente [A]")
    ax.set_title("Feedforward de tensión de red: cancela el hueco antes de que el PI reaccione")
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    _savefig(fig, "control-feedforward-hueco.png")


# ===================================================================== #
#  control-repetitivo
# ===================================================================== #
@figura("control-repetitivo")
def _rep():
    # Respuesta en magnitud del modelo interno periodico: peine en la fundamental y armonicos
    N, Q = 200, 0.985; fs = N*50.0; Ts = 1.0/fs
    f = np.linspace(1, 600, 6000); z = np.exp(1j*2*np.pi*f*Ts)
    C = Q*z**(-N)/(1 - Q*z**(-N))
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    ax.plot(f, 20*np.log10(np.abs(C)), color=ACC, lw=1.4)
    ax.set_xlabel("frecuencia [Hz]"); ax.set_ylabel("|$G_{rc}$| [dB]")
    ax.set_title("Control repetitivo: ganancia alta en $f_0$ y TODOS sus armónicos a la vez")
    ax.text(150, ax.get_ylim()[1]*0.78, "picos en 50, 100, 150, … Hz\n(un retardo = ∞ resonantes)",
            fontsize=8, bbox=dict(fc="white", ec="#ccc", alpha=0.9))
    fig.tight_layout()
    _savefig(fig, "control-repetitivo-peine.png")


# ===================================================================== #
#  control-tension-bus-dc
# ===================================================================== #
@figura("control-tension-bus-dc")
def _vdc():
    # Vdc ante un escalon de carga, con y sin feedforward de potencia de carga
    C, V0, Ts = 10e-3, 1200.0, 1e-4
    T = np.arange(0, 0.12, Ts)
    Pout = np.where(T >= 0.02, 50e3, 0.0)              # escalón de carga 50 kW
    wc = 2*np.pi*30; Kp = C*wc/2; Ki = Kp*wc/5
    def sim(ff):
        w = V0**2; xi = 0.0; out = []
        for k in range(len(T)):
            e = V0**2 - w; xi += e*Ts
            Pin = Kp*e + Ki*xi + (Pout[k] if ff else 0.0)
            w += (Pin - Pout[k])*2/C*Ts
            out.append(np.sqrt(max(w, 1.0)))
        return np.array(out)
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    ax.plot(T*1e3, sim(False), color=BAD, lw=2, label="PI solo")
    ax.plot(T*1e3, sim(True), color=ACC, lw=2, label="PI + feedforward de $P_{carga}$")
    ax.axhline(V0, color="#888", ls=":", lw=1)
    ax.axvline(20, color="#888", ls="--", lw=1); ax.text(21, V0-3, "escalón de carga", fontsize=8)
    ax.set_xlabel("t [ms]"); ax.set_ylabel("$V_{dc}$ [V]")
    ax.set_title("Lazo de tensión del bus DC: el feedforward de carga reduce la caída")
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    _savefig(fig, "control-tension-bus-dc-escalon.png")


# ===================================================================== #
#  control-vectorial
# ===================================================================== #
@figura("control-vectorial")
def _vector():
    # Orientacion dq: marco alineado con la tension de red (vq=0); id->P, iq->Q
    fig, ax = plt.subplots(figsize=(5.8, 5.4))
    ax.annotate("", xy=(1.35, 0), xytext=(-0.25, 0), arrowprops=dict(arrowstyle="->", color="#444", lw=1.3))
    ax.annotate("", xy=(0, 1.35), xytext=(0, -0.25), arrowprops=dict(arrowstyle="->", color="#444", lw=1.3))
    ax.text(1.33, -0.12, "eje d", fontsize=10, ha="right"); ax.text(0.06, 1.3, "eje q", fontsize=10)
    ax.annotate("", xy=(1.0, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=OK, lw=2.6))
    ax.text(1.02, 0.05, "$\\vec v$ (red): $v_q=0$", color=OK, fontsize=10)
    idc, iqc = 0.72, 0.55
    ax.annotate("", xy=(idc, iqc), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=ACC, lw=2.6))
    ax.text(idc+0.02, iqc+0.03, "$\\vec i$", color=ACC, fontsize=11)
    ax.plot([idc, idc], [0, iqc], ls="--", color="#888", lw=1)
    ax.plot([0, idc], [iqc, iqc], ls="--", color="#888", lw=1)
    ax.plot(idc, 0, "o", color=ACC, ms=5); ax.plot(0, iqc, "o", color=ACC, ms=5)
    ax.text(idc, -0.1, "$i_d \\rightarrow P$", color=ACC, fontsize=9, ha="center")
    ax.text(-0.06, iqc, "$i_q \\rightarrow Q$", color=ACC, fontsize=9, ha="right", va="center")
    ax.set_xlim(-0.35, 1.5); ax.set_ylim(-0.35, 1.5); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Control vectorial: orientado a $\\vec v$, $i_d$ gobierna P e $i_q$ gobierna Q")
    fig.tight_layout()
    _savefig(fig, "control-vectorial-orientacion.png")


# ===================================================================== #
#  controlabilidad-observabilidad
# ===================================================================== #
@figura("controlabilidad-observabilidad")
def _ctrb_obsv():
    from matplotlib.patches import Rectangle
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    cells = [
        (0, 1, OK,  "Controlable\n+ Observable",   "diseño completo:\nrealim. de estado + observador"),
        (1, 1, ACC2,"No controlable\n+ Observable", "se ve pero no se mueve\n(basta si es estable: detectable)"),
        (0, 0, ACC2,"Controlable\n+ No observable", "se gobierna pero no se estima\n→ hace falta otro sensor"),
        (1, 0, BAD, "No controlable\n+ No observable","modo oculto;\nsi es inestable → inviable"),
    ]
    for cx, cy, col, tit, sub in cells:
        ax.add_patch(Rectangle((cx, cy), 0.96, 0.96, fc=col, ec="white", lw=2, alpha=0.85))
        ax.text(cx+0.48, cy+0.68, tit, ha="center", va="center", color="white", fontsize=9, weight="bold")
        ax.text(cx+0.48, cy+0.26, sub, ha="center", va="center", color="white", fontsize=7.5)
    ax.text(0.48, 2.12, "Observable\n(rank $\\mathcal{O}=n$)", ha="center", fontsize=9)
    ax.text(1.48, 2.12, "No observable", ha="center", fontsize=9)
    ax.text(-0.18, 1.48, "Controlable\n(rank $\\mathcal{C}=n$)", ha="right", va="center", fontsize=9)
    ax.text(-0.18, 0.48, "No\ncontrolable", ha="right", va="center", fontsize=9)
    ax.set_xlim(-1.0, 2.0); ax.set_ylim(-0.1, 2.35); ax.axis("off")
    ax.set_title("Descomposición de Kalman: qué se puede gobernar y estimar")
    fig.tight_layout()
    _savefig(fig, "controlabilidad-observabilidad-kalman.png")


# ===================================================================== #
#  current-limiting
# ===================================================================== #
@figura("current-limiting")
def _ilim():
    Ts = 2e-5; T = np.arange(0, 0.06, Ts); t0 = 0.02
    Imax = 1.5
    env = np.where(T < t0, 1.0, 1.0 + 3.76*np.exp(-(T - t0)/0.03))   # sin límite: ~4.76 pu
    i_lim = np.minimum(env, Imax)
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    ax.plot(T*1e3, env, color=BAD, lw=2, label="sin límite: pico 4.76 pu")
    ax.plot(T*1e3, i_lim, color=ACC, lw=2.4, label="con límite: 1.51 pu")
    ax.axhline(Imax, color="#888", ls=":", lw=1.2); ax.text(45, Imax+0.12, "$I_{max}=1.5$ pu", fontsize=8)
    ax.axvline(t0*1e3, color="#888", ls="--", lw=1); ax.text(t0*1e3+0.5, 4.2, "hueco de red", fontsize=8)
    ax.set_xlabel("t [ms]"); ax.set_ylabel("|corriente| [pu]")
    ax.set_title("Current limiting en grid-forming: protege los semiconductores en falta")
    ax.legend(fontsize=8)
    fig.tight_layout()
    _savefig(fig, "current-limiting-falta.png")


# ===================================================================== #
#  deteccion-islanding
# ===================================================================== #
@figura("deteccion-islanding")
def _ndz():
    from matplotlib.patches import Rectangle
    fig, ax = plt.subplots(figsize=(6.6, 4.6))
    ax.add_patch(Rectangle((-0.15, -0.06), 0.30, 0.12, fc=BAD, alpha=0.22, ec=BAD, lw=1.6))
    ax.text(0, 0, "NDZ\n(no se detecta)", ha="center", va="center", color=BAD, fontsize=10, weight="bold")
    ax.axhline(0, color="#aaa", lw=0.8); ax.axvline(0, color="#aaa", lw=0.8)
    for x in (-0.15, 0.15): ax.axvline(x, color="#888", ls="--", lw=1)
    for y in (-0.06, 0.06): ax.axhline(y, color="#888", ls="--", lw=1)
    ax.text(0.34, 0.22, "se detecta\n(OUF/OUV disparan)", color=OK, fontsize=9, ha="center")
    ax.set_xlim(-0.5, 0.5); ax.set_ylim(-0.35, 0.35)
    ax.set_xlabel("desbalance de activa  $\\Delta P/P$  (→ frecuencia)")
    ax.set_ylabel("desbalance de reactiva  $\\Delta Q/Q$  (→ tensión)")
    ax.set_title("Zona de no detección: si la isla queda con $P\\approx$carga y $Q\\approx0$")
    fig.tight_layout()
    _savefig(fig, "deteccion-islanding-ndz.png")


# ===================================================================== #
#  droop-dc
# ===================================================================== #
@figura("droop-dc")
def _droopdc():
    Vref = 400.0; Io = np.linspace(0, 100, 50)
    Rd1, Rd2 = 0.5, 1.0; Vbus = 380.0
    I1 = (Vref - Vbus)/Rd1; I2 = (Vref - Vbus)/Rd2
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(Io, Vref - Rd1*Io, color=ACC, lw=2, label=f"conv. 1 ($R_d$=0.5 Ω): $I_1$={I1:.0f} A")
    ax.plot(Io, Vref - Rd2*Io, color=ACC2, lw=2, label=f"conv. 2 ($R_d$=1.0 Ω): $I_2$={I2:.0f} A")
    ax.axhline(Vbus, color="#888", ls="--", lw=1); ax.text(2, Vbus+1.5, "$V_{bus}$ común", fontsize=8)
    ax.plot(I1, Vbus, "o", color=ACC, ms=7); ax.plot(I2, Vbus, "o", color=ACC2, ms=7)
    ax.set_xlabel("corriente de salida $I_o$ [A]"); ax.set_ylabel("$V_{dc}$ [V]")
    ax.set_title("Droop DC: el $V_{bus}$ común fija el reparto  $I_1/I_2 = R_{d2}/R_{d1}$")
    ax.legend(fontsize=8)
    fig.tight_layout()
    _savefig(fig, "droop-dc-reparto.png")


# ===================================================================== #
#  dsogi-pll
# ===================================================================== #
@figura("dsogi-pll")
def _sogi():
    w0 = 2*np.pi*50; k = 1.41
    f = np.linspace(1, 200, 2000); s = 1j*2*np.pi*f
    Hd = k*w0*s/(s**2 + k*w0*s + w0**2)        # v'/v  (banda)
    Hq = k*w0**2/(s**2 + k*w0*s + w0**2)        # qv'/v (cuadratura)
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    ax.plot(f, 20*np.log10(np.abs(Hd)), color=ACC, lw=2, label="$v'/v$ (banda en $f_0$)")
    ax.plot(f, 20*np.log10(np.abs(Hq)), color=ACC2, lw=2, label="$qv'/v$ (cuadratura 90°)")
    ax.axvline(50, color=BAD, ls="--", lw=1); ax.text(53, -34, "$f_0$=50 Hz", fontsize=8, color=BAD)
    ax.set_xlabel("frecuencia [Hz]"); ax.set_ylabel("magnitud [dB]"); ax.set_ylim(-40, 5)
    ax.set_title("SOGI: filtro resonante en $f_0$ + señal en cuadratura (base de la DSOGI)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    _savefig(fig, "dsogi-pll-sogi.png")


# ===================================================================== #
#  estabilidad-armonica
# ===================================================================== #
@figura("estabilidad-armonica")
def _harm():
    f = np.linspace(50, 4000, 3000); w = 2*np.pi*f
    R, L, Td = 1.0, 4e-4, 3e-4                  # impedancia inductiva + retardo digital
    ReZ = R*np.cos(w*Td) + w*L*np.sin(w*Td)     # Re{(R+jwL) e^{-jwTd}}
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    ax.plot(f, ReZ, color=ACC, lw=2)
    ax.axhline(0, color="#888", lw=1)
    ax.fill_between(f, ReZ, 0, where=(ReZ < 0), color=BAD, alpha=0.3)
    fres = 1900
    ax.axvline(fres, color=OK, ls="--", lw=1.6)
    ax.text(fres+40, ax.get_ylim()[1]*0.55, "resonancia\nde red", color=OK, fontsize=8)
    ax.text(1700, -3.5, "Re{$Z_o$}<0:\nno pasivo", color=BAD, fontsize=8, ha="center")
    ax.set_xlabel("frecuencia [Hz]"); ax.set_ylabel("Re{$Z_o$} [Ω]")
    ax.set_title("Estabilidad armónica: Re{$Z_o$}<0 sobre una resonancia de red → oscilación")
    fig.tight_layout()
    _savefig(fig, "estabilidad-armonica-pasividad.png")


# ===================================================================== #
#  estabilidad-bus-dc-cpl
# ===================================================================== #
@figura("estabilidad-bus-dc-cpl")
def _cpl():
    Lf, Rf, Cdc, V = 200e-6, 0.1, 500e-6, 400.0
    Pcrit = V**2*Rf*Cdc/Lf
    Ps = np.linspace(0, 1.8*Pcrit, 45)
    re, im, cp = [], [], []
    for P in Ps:
        A = np.array([[-Rf/Lf, -1/Lf], [1/Cdc, P/(V**2*Cdc)]])
        for ev in np.linalg.eigvals(A):
            re.append(ev.real); im.append(ev.imag); cp.append(P/1e3)
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    sc = ax.scatter(re, im, c=cp, cmap="plasma", s=22)
    fig.colorbar(sc, label="P [kW]")
    ax.axvline(0, color=BAD, ls="--", lw=1.2)
    ax.text(50, ax.get_ylim()[1]*0.7, f"$P_{{crit}}=V^2R_fC_{{dc}}/L_f$\n= {Pcrit/1e3:.0f} kW",
            fontsize=8, bbox=dict(fc="white", ec="#ccc", alpha=0.9))
    ax.set_xlabel("Re(s) [1/s]"); ax.set_ylabel("Im(s) [rad/s]")
    ax.set_title("Bus DC con CPL: los polos cruzan a la derecha al subir P (CPL desamortigua)")
    fig.tight_layout()
    _savefig(fig, "estabilidad-bus-dc-cpl-polos.png")


# ===================================================================== #
#  fault-ride-through
# ===================================================================== #
@figura("fault-ride-through")
def _frt():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 3.9))
    t = np.array([-100, 0, 0, 150, 1500, 1500, 3000]); v = np.array([1.0, 1.0, 0.0, 0.0, 0.9, 0.9, 0.9])
    a1.plot(t, v, color=BAD, lw=2.2)
    a1.fill_between(t, v, 1.15, color=OK, alpha=0.12)
    a1.text(900, 1.03, "permanecer conectado", color=OK, fontsize=9, ha="center")
    a1.text(700, 0.3, "desconexión\npermitida", color=BAD, fontsize=8, ha="center")
    a1.set_xlabel("t [ms] (0 = inicio del hueco)"); a1.set_ylabel("$V_{pcc}$ [pu]")
    a1.set_ylim(-0.05, 1.18); a1.set_title("Envolvente LVRT")
    dV = np.linspace(0, 1, 100); k = 2.0; Imax = 1.0
    a2.plot(dV, np.minimum(k*dV, Imax), color=ACC, lw=2.2)
    a2.axhline(Imax, color="#888", ls=":", lw=1); a2.text(0.05, Imax+0.03, "$I_{max}$", fontsize=8)
    a2.set_xlabel("caída de tensión  $\\Delta V$ [pu]"); a2.set_ylabel("$\\Delta I_q$ [pu]")
    a2.set_title("Inyección de reactiva  $\\Delta I_q=k\\,\\Delta V$  (k=2)")
    fig.tight_layout()
    _savefig(fig, "fault-ride-through-lvrt.png")


# ===================================================================== #
#  gain-scheduling
# ===================================================================== #
@figura("gain-scheduling")
def _gsched():
    scr = np.linspace(2, 10, 100); Xg = 10.0/scr            # reactancia de red ∝ 1/SCR
    kp_sched = 0.1*scr                                       # Kp programado con la SCR
    loop_sched = kp_sched*Xg                                 # ≈ cte
    loop_fixed = 1.0*Xg                                      # Kp fijo (sintonizado a SCR=10)
    fig, ax = plt.subplots(figsize=(6.8, 4.1))
    ax.plot(scr, loop_fixed, color=BAD, lw=2, label="$K_p$ fijo: la ganancia se dispara en red débil")
    ax.plot(scr, loop_sched, color=ACC, lw=2, label="$K_p$ programado: $K_pX_g\\approx$ cte")
    ax.axhline(3.0, color="#888", ls="--", lw=1); ax.text(7, 3.15, "umbral de inestabilidad", fontsize=8)
    ax.invert_xaxis()
    ax.set_xlabel("SCR  (← red más débil)"); ax.set_ylabel("ganancia de lazo  $K_p X_g$")
    ax.set_title("Gain scheduling: bajar $K_p$ con la SCR mantiene el margen")
    ax.legend(fontsize=8)
    fig.tight_layout()
    _savefig(fig, "gain-scheduling-scr.png")


# ===================================================================== #
#  impedancia-salida-estabilidad
# ===================================================================== #
@figura("impedancia-salida-estabilidad")
def _zstab():
    f = np.logspace(0, 3.3, 600); w = 2*np.pi*f
    Zinv = 8.0/np.sqrt(1 + (f/300)**2) + 0.5                 # |Z| del inversor (cae con f)
    Zg_w = w*20e-3; Zg_s = w*2e-3                            # red débil / fuerte
    fig, ax = plt.subplots(figsize=(6.8, 4.1))
    ax.loglog(f, Zinv, color=ACC, lw=2.2, label="|$Z_{inv}$| (convertidor)")
    ax.loglog(f, Zg_w, color=BAD, lw=2, label="|$Z_{red}$| débil (SCR bajo)")
    ax.loglog(f, Zg_s, color=OK, lw=2, label="|$Z_{red}$| fuerte (SCR alto)")
    fc_w = f[np.argmin(np.abs(Zg_w - Zinv))]; fc_s = f[np.argmin(np.abs(Zg_s - Zinv))]
    for fc, c in [(fc_w, BAD), (fc_s, OK)]:
        ax.plot(fc, np.interp(fc, f, Zinv), "o", color=c, ms=7)
    ax.text(fc_w, 0.6, "cruce: el margen\nde fase decide", fontsize=8, ha="center")
    ax.set_xlabel("frecuencia [Hz]"); ax.set_ylabel("|Z| [Ω]")
    ax.set_title("Criterio de impedancia: estabilidad en el cruce |$Z_{red}$|=|$Z_{inv}$|")
    ax.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    _savefig(fig, "impedancia-salida-estabilidad-cruce.png")


# ===================================================================== #
#  interaccion-pll-red-debil
# ===================================================================== #
@figura("interaccion-pll-red-debil")
def _pllweak():
    fpll = np.array([30, 60, 100, 150, 170]); scr_crit = np.array([1.0, 2.2, 3.5, 6.5, 8.0])
    fig, ax = plt.subplots(figsize=(6.8, 4.1))
    ax.fill_between(fpll, scr_crit, 0, color=BAD, alpha=0.18)
    ax.fill_between(fpll, scr_crit, 9, color=OK, alpha=0.12)
    ax.plot(fpll, scr_crit, "o-", color=ACC, lw=2)
    ax.text(60, 1.0, "INESTABLE\n(red demasiado débil)", color=BAD, fontsize=9)
    ax.text(45, 7.0, "estable", color=OK, fontsize=9)
    ax.set_xlabel("ancho de banda de la PLL [Hz]"); ax.set_ylabel("SCR crítico")
    ax.set_ylim(0, 9)
    ax.set_title("PLL–red débil: una PLL más rápida amplía la región inestable")
    fig.tight_layout()
    _savefig(fig, "interaccion-pll-red-debil-mapa.png")


# ===================================================================== #
#  matching-control
# ===================================================================== #
@figura("matching-control")
def _match():
    C, kth, V0, Pmax, Dd = 5e-3, 1.0, 1.0, 1.0, 0.30
    dt = 2e-4; T = np.arange(0, 1.5, dt)
    Ps = np.where(T >= 0.2, 0.6, 0.4)
    vdc = V0; delta = np.arcsin(0.4/Pmax); out = []
    for k in range(len(T)):
        Pe = Pmax*np.sin(delta)
        vdc += (Ps[k] - Pe - Dd*(vdc - V0))/(C*vdc)*dt
        delta += kth*(vdc - V0)*dt
        out.append(vdc)
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    ax.plot(T, out, color=ACC, lw=2)
    ax.axvline(0.2, color="#888", ls="--", lw=1); ax.text(0.22, V0+0.002, "escalón de potencia", fontsize=8)
    ax.set_xlabel("t [s]"); ax.set_ylabel("$v_{dc}$ [pu]")
    ax.set_title("Matching: $v_{dc}$ hace de frecuencia ($\\dot\\theta=k\\,v_{dc}$) y oscila como un swing")
    fig.tight_layout()
    _savefig(fig, "matching-control-swing.png")


# ===================================================================== #
#  no-pasividad-resistencia-negativa
# ===================================================================== #
@figura("no-pasividad-resistencia-negativa")
def _nopas():
    f = np.linspace(1, 200, 1000); R0 = 1.0
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    for fp, c, lbl in [(30, OK, "PLL lenta (30 Hz)"), (100, BAD, "PLL rápida (100 Hz)")]:
        ReZ = R0*(1 - 2*fp**2/(fp**2 + f**2))
        ax.plot(f, ReZ, color=c, lw=2, label=lbl)
    ax.axhline(0, color="#888", lw=1)
    ax.axhspan(-1.2, 0, color=BAD, alpha=0.06)
    ax.text(150, -0.5, "Re{Z}<0\nno pasivo", color=BAD, fontsize=8, ha="center")
    ax.set_xlabel("frecuencia [Hz]"); ax.set_ylabel("Re{$Z_{qq}$} [pu]"); ax.set_ylim(-1.2, 1.1)
    ax.set_title("No pasividad: la banda de resistencia negativa se ensancha con la PLL")
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    _savefig(fig, "no-pasividad-resistencia-negativa-rez.png")


# ===================================================================== #
#  oscilaciones-subsincronas
# ===================================================================== #
@figura("oscilaciones-subsincronas")
def _sso():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 3.9))
    comp = np.linspace(20, 75, 100); f1 = 50.0
    fn = f1*np.sqrt(comp/100.0)
    a1.plot(comp, fn, color=ACC, lw=2)
    a1.axhspan(10, 45, color=BAD, alpha=0.10)
    a1.text(45, 14, "banda subsíncrona", color=BAD, fontsize=8, ha="center")
    a1.set_xlabel("compensación serie [%]"); a1.set_ylabel("$f_n$ [Hz]")
    a1.set_title("Resonancia serie  $f_n=f_1\\sqrt{X_{Cs}/X_L}$")
    t = np.linspace(0, 0.6, 2000)
    a2.plot(t, np.exp(3.0*t)*np.sin(2*np.pi*30*t), color=BAD, lw=1.0)
    a2.set_xlabel("t [s]"); a2.set_ylabel("corriente subsíncrona")
    a2.set_title("SSCI: Re{$Z$}<0 cerca de $f_n$ → crece")
    fig.tight_layout()
    _savefig(fig, "oscilaciones-subsincronas-resonancia.png")


# ===================================================================== #
#  power-synchronization-control
# ===================================================================== #
@figura("power-synchronization-control")
def _psc():
    Kpsc, Ks = 2.0, 2.0; pole = Kpsc*Ks
    t = np.linspace(0, 2, 500); Pref = 1.0
    P = Pref*(1 - np.exp(-pole*t))
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    ax.plot(t, P, color=ACC, lw=2, label="P (PSC: 1er orden, sin oscilación)")
    ax.axhline(Pref, color="#888", ls=":", lw=1); ax.text(1.6, Pref+0.02, "$P^*$", fontsize=9)
    ax.text(0.55, 0.45, f"polo en $s=-K_{{psc}}K_s=-{pole:.0f}$\n→ sincroniza integrando el error de P",
            fontsize=8, bbox=dict(fc="white", ec="#ccc", alpha=0.9))
    ax.set_xlabel("t [s]"); ax.set_ylabel("P [pu]"); ax.set_ylim(0, 1.1)
    ax.set_title("Power Synchronization Control: el ángulo integra $P^*-P$ (sin PLL)")
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    _savefig(fig, "power-synchronization-control-sync.png")


# ===================================================================== #
#  virtual-oscillator-control
# ===================================================================== #
@figura("virtual-oscillator-control")
def _voc():
    eps, w0 = 0.8, 2*np.pi
    def step(x, dt):
        v, dv = x
        ddv = -eps*(v**2 - 1)*dv - w0**2*v
        return np.array([v + dv*dt, dv + ddv*dt])
    fig, ax = plt.subplots(figsize=(5.9, 5.3))
    for v0, c, lbl in [(0.15, ACC, "inicio dentro"), (3.0, ACC2, "inicio fuera")]:
        x = np.array([v0, 0.0]); xs = [x]
        for _ in range(4000):
            x = step(x, 0.002); xs.append(x)
        xs = np.array(xs)
        ax.plot(xs[:, 0], xs[:, 1], color=c, lw=1.0, label=lbl)
    ax.set_xlabel("$v$"); ax.set_ylabel("$\\dot v$")
    ax.set_title("VOC: cualquier inicio converge al ciclo límite (Van der Pol)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    _savefig(fig, "virtual-oscillator-control-ciclo.png")


# ===================================================================== #
#  armonicos-thd-convertidores
# ===================================================================== #
@figura("armonicos-thd-convertidores")
def _thd():
    f1 = 50.0
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    for o, a in [(1, 100.0), (5, 2.4), (7, 1.6), (11, 0.8), (13, 0.6)]:
        ax.vlines(o*f1, 0.3, a, color=(ACC if o == 1 else ACC2), lw=2.5)
    for fb, ab in [(4800, 3), (4900, 6), (5100, 6), (5200, 3), (9900, 2), (10100, 2)]:
        ax.vlines(fb, 0.3, ab, color=BAD, lw=2)
    ax.set_yscale("log"); ax.set_ylim(0.3, 160); ax.set_xlim(-100, 10800)
    ax.text(250, 60, "fund.", color=ACC, fontsize=8)
    ax.text(900, 4.5, "5º,7º…\n(tiempo muerto)", color=ACC2, fontsize=8)
    ax.text(5000, 9, "banda de conmutación\n$m_f f_1=5$ kHz", color=BAD, fontsize=8, ha="center")
    ax.set_xlabel("frecuencia [Hz]"); ax.set_ylabel("amplitud [% fund.]")
    ax.set_title("Espectro de un convertidor PWM: bajos órdenes + bandas de conmutación")
    fig.tight_layout()
    _savefig(fig, "armonicos-thd-convertidores-espectro.png")


# ===================================================================== #
#  carga-potencia-constante-cpl
# ===================================================================== #
@figura("carga-potencia-constante-cpl")
def _cpliv():
    P = 1.0; V = np.linspace(0.4, 1.6, 200); i = P/V
    V0 = 1.0; i0 = P/V0; slope = -P/V0**2
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    ax.plot(V, i, color=ACC, lw=2.2, label="CPL: $i=P/V$")
    Vt = np.array([0.7, 1.3])
    ax.plot(Vt, i0 + slope*(Vt - V0), color=BAD, ls="--", lw=1.8,
            label="$\\partial i/\\partial V=-P/V^2<0$ (resist. negativa)")
    ax.plot(V0, i0, "o", color=BAD, ms=7)
    ax.plot(V, V, color=OK, lw=1.5, ls=":", label="resistencia: pendiente +")
    ax.set_xlabel("$V_{dc}$ [pu]"); ax.set_ylabel("i [pu]"); ax.set_ylim(0, 2.6)
    ax.set_title("CPL: la pendiente i–V es negativa y desamortigua el bus")
    ax.legend(fontsize=8)
    fig.tight_layout()
    _savefig(fig, "carga-potencia-constante-cpl-iv.png")


# ===================================================================== #
#  carga-pulsante-datacenter-ia
# ===================================================================== #
@figura("carga-pulsante-datacenter-ia")
def _pulse():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 3.8))
    t = np.linspace(0, 1.0, 2000); tn = 0.2
    a1.plot(t, np.where(t >= tn, 230, 100), color=ACC, lw=2)
    a1.set_xlabel("t [s]"); a1.set_ylabel("P [kW]"); a1.set_ylim(80, 250)
    a1.set_title("Escalón sincronizado (arranque de un job de IA)")
    df_ss, tau = -0.20, 0.30
    f = 50 + np.where(t < tn, 0.0, df_ss*(1 - np.exp(-(t - tn)/tau)))
    a2.plot(t, f, color=BAD, lw=2)
    a2.axvline(tn, color="#888", ls="--", lw=1)
    a2.plot([tn, tn+0.25], [50, 50 + (df_ss/tau)*0.25], color="#444", ls=":", lw=1.4)
    a2.text(tn+0.28, 49.93, "RoCoF", fontsize=8)
    a2.set_xlabel("t [s]"); a2.set_ylabel("frecuencia [Hz]")
    a2.set_title("Impacto en frecuencia: RoCoF y caída (lo limita el BESS)")
    fig.tight_layout()
    _savefig(fig, "carga-pulsante-datacenter-ia-impacto.png")


# ===================================================================== #
#  convertidor-back-to-back
# ===================================================================== #
@figura("convertidor-back-to-back")
def _b2b():
    from matplotlib.patches import Rectangle
    fig, ax = plt.subplots(figsize=(8.4, 3.6))
    def box(x, w, txt, col):
        ax.add_patch(Rectangle((x, 1.0), w, 1.0, fc=col, ec="#333", alpha=0.88))
        ax.text(x+w/2, 1.5, txt, ha="center", va="center", color="white", fontsize=9, weight="bold")
    box(0.2, 1.4, "Red /\nMáquina 1", ACC2); box(2.1, 1.2, "VSC 1", ACC)
    ax.plot([4.0, 4.0], [1.1, 1.9], color="#333", lw=3); ax.plot([4.25, 4.25], [1.1, 1.9], color="#333", lw=3)
    ax.text(4.13, 2.08, "$C$ ($V_{dc}$)", ha="center", fontsize=9)
    box(4.7, 1.2, "VSC 2", ACC); box(6.4, 1.4, "Red 2", ACC2)
    for x0, x1 in [(1.6, 2.1), (3.3, 4.0), (4.25, 4.7), (5.9, 6.4)]:
        ax.plot([x0, x1], [1.5, 1.5], color="#333", lw=1.5)
    ax.annotate("", xy=(3.8, 2.55), xytext=(2.7, 2.55), arrowprops=dict(arrowstyle="->", color=OK, lw=2.2))
    ax.text(3.25, 2.62, "$P_1$", color=OK, ha="center", fontsize=10)
    ax.annotate("", xy=(5.7, 2.55), xytext=(4.6, 2.55), arrowprops=dict(arrowstyle="->", color=OK, lw=2.2))
    ax.text(5.15, 2.62, "$P_2$", color=OK, ha="center", fontsize=10)
    ax.set_xlim(0, 8.0); ax.set_ylim(0.6, 3.0); ax.axis("off")
    ax.set_title("Back-to-back: dos VSC acoplados solo por el bus DC  $C\\,\\dot V_{dc}=(P_1-P_2)/V_{dc}$")
    fig.tight_layout()
    _savefig(fig, "convertidor-back-to-back-topologia.png")


# ===================================================================== #
#  eolica-mppt
# ===================================================================== #
@figura("eolica-mppt")
def _mppt():
    rho, R, lam_opt, Cpmax, wsd = 1.225, 40.0, 8.0, 0.48, 2.2
    Cp = lambda lam: Cpmax*np.exp(-((lam - lam_opt)/wsd)**2)
    w = np.linspace(0.3, 3.3, 400)
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    peaks = []
    for vw in [8, 10, 12, 14]:
        P = 0.5*rho*np.pi*R**2*vw**3*Cp(w*R/vw)/1e6
        ax.plot(w, P, lw=2, label=f"{vw} m/s")
        ip = np.argmax(P); peaks.append((w[ip], P[ip]))
    peaks = np.array(peaks); kopt = peaks[-1, 1]/peaks[-1, 0]**3
    wl = np.linspace(0.3, 3.3, 100)
    ax.plot(wl, kopt*wl**3, "k--", lw=1.7, label="locus MPPT  $\\propto\\omega^3$")
    ax.plot(peaks[:, 0], peaks[:, 1], "o", color=BAD, ms=6)
    ax.set_xlabel("velocidad del rotor $\\omega_r$ [rad/s]"); ax.set_ylabel("P [MW]")
    ax.set_ylim(0, peaks[:, 1].max()*1.15)
    ax.set_title("MPPT eólico: el par óptimo $T^*=k\\,\\omega_r^2$ une los picos de potencia")
    ax.legend(fontsize=8)
    fig.tight_layout()
    _savefig(fig, "eolica-mppt-cp.png")


# ===================================================================== #
#  generador-sincrono
# ===================================================================== #
@figura("generador-sincrono")
def _sg():
    d = np.linspace(0, 180, 300); P = np.sin(np.radians(d))
    d0 = 30.0; P0 = np.sin(np.radians(d0)); Ks = np.cos(np.radians(d0))
    fig, ax = plt.subplots(figsize=(6.8, 4.1))
    ax.plot(d, P, color=ACC, lw=2)
    ax.axhline(P0, color="#888", ls=":", lw=1); ax.text(3, P0+0.03, "$P_{mec}$", fontsize=8)
    ax.plot(d0, P0, "o", color=OK, ms=7)
    dl = np.array([15.0, 48.0])
    ax.plot(dl, P0 + Ks*np.radians(dl - d0), color=OK, ls="--", lw=1.6)
    ax.axvline(90, color=BAD, ls="--", lw=1.2); ax.text(93, 0.18, "límite\n$\\delta=90°$", color=BAD, fontsize=8)
    ax.fill_between(d, P, where=(d > 90), color=BAD, alpha=0.08)
    ax.text(33, 0.12, "par sincronizante\n$K_s=\\partial P/\\partial\\delta$", color=OK, fontsize=8, ha="left")
    ax.set_xlabel("ángulo de carga δ [°]"); ax.set_ylabel("P [pu]")
    ax.set_title("Generador síncrono: curva potencia–ángulo $P=\\frac{EV}{X}\\sin\\delta$")
    fig.tight_layout()
    _savefig(fig, "generador-sincrono-pdelta.png")


# ===================================================================== #
#  impedancia-dq-vs-secuencia
# ===================================================================== #
@figura("impedancia-dq-vs-secuencia")
def _dqseq():
    fig, ax = plt.subplots(figsize=(7.2, 3.7))
    ax.axhline(0, color="#333", lw=1.2)
    f1, fp = 50.0, 80.0; fm = abs(fp - 2*f1)
    for f, lbl, c, up in [(f1, "$f_1$=50", "#888", 0.45),
                          (fp, "$f_p$ (inyección)", ACC, 1.0),
                          (fm, "$f_p-2f_1$\n(espejo)", BAD, 0.75)]:
        ax.annotate("", xy=(f, up), xytext=(f, 0), arrowprops=dict(arrowstyle="->", color=c, lw=2.4))
        ax.text(f, up+0.06, lbl, ha="center", color=c, fontsize=9)
    ax.text(75, 1.28, "dq (2×2)  ⟺  secuencia (espejo):   $s_{dq}=s\\mp j\\omega_1$",
            ha="center", fontsize=9, bbox=dict(fc="white", ec="#ccc"))
    ax.set_xlim(-5, 150); ax.set_ylim(-0.15, 1.5); ax.set_yticks([])
    ax.set_xlabel("frecuencia [Hz]")
    ax.set_title("Acoplamiento de frecuencia espejo: una inyección en $f_p$ responde también en $f_p-2f_1$")
    fig.tight_layout()
    _savefig(fig, "impedancia-dq-vs-secuencia-espejo.png")


# ===================================================================== #
#  linealizacion-teoria
# ===================================================================== #
@figura("linealizacion-teoria")
def _lin():
    g, l, b = 9.81, 1.0, 0.4; dt = 0.005; T = np.arange(0, 4, dt)
    def sim(th0, nonlin):
        th, w, out = th0, 0.0, []
        for _ in T:
            acc = -(g/l)*(np.sin(th) if nonlin else th) - b*w
            w += acc*dt; th += w*dt; out.append(th)
        return np.array(out)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 3.8))
    for ax, th0, tit in [(a1, 0.2, "Pequeña señal ($\\theta_0=0.2$): coinciden"),
                         (a2, 2.5, "Gran señal ($\\theta_0=2.5$): divergen")]:
        ax.plot(T, sim(th0, True), color=ACC, lw=2, label="no lineal")
        ax.plot(T, sim(th0, False), color=BAD, ls="--", lw=2, label="linealizado")
        ax.set_xlabel("t [s]"); ax.set_ylabel("θ [rad]"); ax.set_title(tit); ax.legend(fontsize=8)
    fig.tight_layout()
    _savefig(fig, "linealizacion-teoria-validez.png")


# ===================================================================== #
#  maquina-induccion
# ===================================================================== #
@figura("maquina-induccion")
def _induc():
    R1, R2, X1, X2, V, ws = 0.5, 0.4, 1.2, 1.2, 230.0, 2*np.pi*50
    s = np.linspace(-0.6, 1.2, 500); s = s[np.abs(s) > 2e-3]
    T = 3*V**2*(R2/s)/(ws*((R1 + R2/s)**2 + (X1 + X2)**2))
    n_rel = 1 - s
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(n_rel, T, color=ACC, lw=2)
    ax.axhline(0, color="#888", lw=1); ax.axvline(1, color="#888", ls=":", lw=1)
    ax.text(1.02, T.max()*0.12, "sincronismo\n$s=0$", fontsize=8)
    ax.fill_between(n_rel, T, where=(n_rel < 1) & (T > 0), color=OK, alpha=0.10)
    ax.text(0.45, T.max()*0.55, "MOTOR\n$0<s<1$", color=OK, fontsize=9, ha="center")
    ax.text(1.32, T.min()*0.5, "GENERADOR\n$s<0$", color=BAD, fontsize=9, ha="center")
    ax.set_xlabel("velocidad  $n/n_s$"); ax.set_ylabel("par [N·m]")
    ax.set_title("Máquina de inducción: par–velocidad (necesita deslizamiento para dar par)")
    fig.tight_layout()
    _savefig(fig, "maquina-induccion-par.png")


# ===================================================================== #
#  microrred-hibrida-ac-dc
# ===================================================================== #
@figura("microrred-hibrida-ac-dc")
def _hybrid():
    from matplotlib.patches import Rectangle
    fig, ax = plt.subplots(figsize=(8.8, 4.1))
    ax.add_patch(Rectangle((1.6, 0.5), 0.18, 3.0, fc=ACC2, ec="#333"))
    ax.text(1.69, 3.72, "Bus AC\n($\\omega$, V)", ha="center", fontsize=9, color=ACC2)
    ax.add_patch(Rectangle((6.9, 0.5), 0.18, 3.0, fc=ACC, ec="#333"))
    ax.text(6.99, 3.72, "Bus DC\n($V_{dc}$)", ha="center", fontsize=9, color=ACC)
    ax.add_patch(Rectangle((3.7, 1.55), 1.1, 0.95, fc=OK, ec="#333"))
    ax.text(4.25, 2.02, "ILC", ha="center", va="center", color="white", fontsize=10, weight="bold")
    ax.plot([1.78, 3.7], [2.02, 2.02], color="#333", lw=1.4); ax.plot([4.8, 6.9], [2.02, 2.02], color="#333", lw=1.4)
    ax.annotate("", xy=(4.9, 2.75), xytext=(3.6, 2.75), arrowprops=dict(arrowstyle="<->", color=OK, lw=1.8))
    ax.text(4.25, 2.85, "$P_{ILC}$", ha="center", color=OK, fontsize=9)
    def tag(x, y, txt, ha):
        ax.text(x, y, txt, ha=ha, va="center", fontsize=8,
                bbox=dict(boxstyle="round", fc="white", ec="#bbb"))
    for y, t in [(3.0, "Red AC"), (1.0, "Carga AC")]:
        tag(0.5, y, t, "center"); ax.plot([0.95, 1.6], [y, y], color="#999", lw=1)
    for y, t in [(3.1, "PV"), (2.0, "Batería"), (0.9, "Carga DC")]:
        tag(8.2, y, t, "center"); ax.plot([7.08, 7.85], [y, y], color="#999", lw=1)
    ax.set_xlim(-0.2, 9.0); ax.set_ylim(0.3, 4.2); ax.axis("off")
    ax.set_title("Microrred híbrida: subredes AC y DC unidas por el convertidor de interconexión (ILC)")
    fig.tight_layout()
    _savefig(fig, "microrred-hibrida-ac-dc-arquitectura.png")


# ===================================================================== #
#  modelado-sistemas
# ===================================================================== #
@figura("modelado-sistemas")
def _model():
    from matplotlib.patches import Rectangle
    steps = ["Sistema\nfísico", "Leyes balance\n+ constitutivas", "EDOs\n$\\dot x=f(x,u)$",
             "Espacio de\nestados", "Linealización\n$(A,B,C,D)$", "Validación"]
    fig, ax = plt.subplots(figsize=(9.8, 2.5))
    x = 0.1
    for i, s in enumerate(steps):
        ax.add_patch(Rectangle((x, 0.3), 1.35, 0.95, fc=(OK if i == len(steps)-1 else ACC), ec="#333", alpha=0.88))
        ax.text(x+0.675, 0.775, s, ha="center", va="center", color="white", fontsize=8.5, weight="bold")
        if i < len(steps)-1:
            ax.annotate("", xy=(x+1.58, 0.775), xytext=(x+1.45, 0.775), arrowprops=dict(arrowstyle="->", color="#333", lw=1.6))
        x += 1.58
    ax.set_xlim(0, x); ax.set_ylim(0, 1.55); ax.axis("off")
    ax.set_title("Modelado caja blanca: del sistema físico al modelo lineal validado")
    fig.tight_layout()
    _savefig(fig, "modelado-sistemas-flujo.png")


# ===================================================================== #
#  modelo-bateria-bess
# ===================================================================== #
@figura("modelo-bateria-bess")
def _bess():
    R0, R1, tau, OCV = 0.02, 0.015, 5.0, 3.60
    dt = 0.05; T = np.arange(0, 40, dt)
    I = np.where((T >= 5) & (T < 20), 10.0, 0.0)
    Vrc = 0.0; V = []
    for k in range(len(T)):
        V.append(OCV - I[k]*R0 - Vrc)
        Vrc += (I[k]*R1 - Vrc)/tau*dt
    V = np.array(V)
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    ax.plot(T, V, color=ACC, lw=2)
    ax.axhline(OCV, color="#888", ls=":", lw=1); ax.text(0.5, OCV+0.004, "OCV(SoC)", fontsize=8)
    ax.annotate("caída óhmica $R_0$\n(instantánea)", xy=(5, OCV - 10*R0), xytext=(7, OCV-0.06),
                fontsize=8, arrowprops=dict(arrowstyle="->", color=BAD))
    ax.annotate("relajación RC\n(difusión, $\\tau$)", xy=(15, V[int(15/dt)]), xytext=(24, OCV-0.13),
                fontsize=8, arrowprops=dict(arrowstyle="->", color=ACC2))
    ax.set_xlabel("t [s]"); ax.set_ylabel("$V_{bat}$ [V]")
    ax.set_title("Modelo Thevenin 1-RC: pulso de corriente → salto $R_0$ + cola RC")
    fig.tight_layout()
    _savefig(fig, "modelo-bateria-bess-pulso.png")


# ===================================================================== #
#  modelo-linea-distribucion
# ===================================================================== #
@figura("modelo-linea-distribucion")
def _linea():
    d = schemdraw.Drawing(); d.config(unit=2.0, fontsize=12)
    d += elm.Dot().label("$V_1$", "left")
    d.push()
    d += elm.Capacitor().down().label("$C/2$", "bottom"); d += elm.Ground()
    d.pop()
    d += elm.Resistor().right().label("$R$")
    d += elm.Inductor2().right().label("$L$  ($X=\\omega L$)")
    d += elm.Dot().label("$V_2$", "right")
    d += elm.Capacitor().down().label("$C/2$", "bottom"); d += elm.Ground()
    fname = os.path.join(OUT, "modelo-linea-distribucion-pi.png")
    d.save(fname, dpi=150); print(os.path.basename(fname))


# ===================================================================== #
#  resonancia-lcl
# ===================================================================== #
@figura("resonancia-lcl")
def _reslcl():
    L1, L2, Cf = 2e-3, 1e-3, 20e-6
    wres = np.sqrt((L1+L2)/(L1*L2*Cf)); far = 1/(2*np.pi*np.sqrt(L2*Cf))
    z = 0.03
    f = np.logspace(1.7, 4, 1500); s = 1j*2*np.pi*f
    den = s*L1*L2*Cf*(s**2 + 2*z*wres*s + wres**2)
    Gi2 = 1/den
    Gi1 = (1 + s**2*L2*Cf)/den
    fig, ax = plt.subplots(figsize=(6.9, 4.1))
    ax.semilogx(f, 20*np.log10(np.abs(Gi2)), color=BAD, lw=2, label="$i_2/v_i$ (lado red): pico afilado")
    ax.semilogx(f, 20*np.log10(np.abs(Gi1)), color=ACC, lw=2, label="$i_1/v_i$ (lado inversor): +antiresonancia")
    ax.axvline(wres/(2*np.pi), color="#888", ls="--", lw=1); ax.text(wres/(2*np.pi)*1.03, ax.get_ylim()[1]-10, "$f_{res}$", fontsize=8)
    ax.axvline(far, color=OK, ls=":", lw=1.2); ax.text(far*0.55, ax.get_ylim()[0]+8, "$f_{ar}$", color=OK, fontsize=8)
    ax.set_xlabel("frecuencia [Hz]"); ax.set_ylabel("magnitud [dB]")
    ax.set_title("Resonancia LCL: $i_1$ tiene un cero de antiresonancia → más fácil de estabilizar que $i_2$")
    ax.legend(fontsize=8)
    fig.tight_layout()
    _savefig(fig, "resonancia-lcl-bode.png")


# ===================================================================== #
#  sistema-por-unidad
# ===================================================================== #
@figura("sistema-por-unidad")
def _pu():
    comps = ["transformador", "filtro", "red"]; vals = [0.05, 0.12, 0.08]
    cols = [ACC2, ACC, OK]
    fig, ax = plt.subplots(figsize=(7.0, 3.4))
    left = 0.0
    for c, v, col in zip(comps, vals, cols):
        ax.barh(0, v, left=left, color=col, ec="white", height=0.5)
        ax.text(left + v/2, 0, f"{c}\n{v:.2f}", ha="center", va="center", color="white", fontsize=8.5)
        left += v
    ax.text(left+0.005, 0, f"  $Z_{{tot}}$ = {left:.2f} pu", va="center", fontsize=9, weight="bold")
    ax.set_xlim(0, 0.32); ax.set_ylim(-0.6, 0.6); ax.set_yticks([])
    ax.set_xlabel("impedancia [pu]")
    ax.set_title("Por unidad: impedancias dispares en SI quedan ~0.05–0.15 y se suman directas")
    fig.tight_layout()
    _savefig(fig, "sistema-por-unidad-impedancias.png")


# ===================================================================== #
#  statcom-svc
# ===================================================================== #
@figura("statcom-svc")
def _statcom():
    V = np.linspace(0.4, 1.1, 200)
    fig, ax = plt.subplots(figsize=(6.8, 4.1))
    ax.plot(V, V**2, color=BAD, lw=2, label="SVC: $Q\\propto V^2$ (se hunde)")
    ax.plot(V, V, color=ACC, lw=2, label="STATCOM: $Q\\propto V$ (se mantiene)")
    ax.axvline(0.85, color="#888", ls="--", lw=1); ax.text(0.86, 0.25, "hueco\n$V=0.85$", fontsize=8)
    ax.plot(0.85, 0.85**2, "o", color=BAD, ms=7); ax.plot(0.85, 0.85, "o", color=ACC, ms=7)
    ax.set_xlabel("tensión V [pu]"); ax.set_ylabel("Q / $Q_{nom}$")
    ax.set_title("STATCOM vs SVC: el STATCOM sostiene más reactiva cuando la tensión cae")
    ax.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    _savefig(fig, "statcom-svc-qv.png")


# ===================================================================== #
#  topologias-multinivel
# ===================================================================== #
@figura("topologias-multinivel")
def _multi():
    t = np.linspace(0, 2*np.pi, 1000); ref = np.sin(t)
    stair = lambda n: np.round((ref + 1)/2*(n - 1))/(n - 1)*2 - 1
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    ax.plot(t, ref, color="#888", lw=1.5, ls="--", label="referencia")
    ax.step(t, stair(2), where="mid", color=BAD, lw=1.4, label="2 niveles")
    ax.step(t, stair(3), where="mid", color=ACC2, lw=1.4, label="3 niveles (NPC)")
    ax.step(t, stair(7), where="mid", color=ACC, lw=1.8, label="7 niveles (MMC)")
    ax.set_xlabel("ωt [rad]"); ax.set_ylabel("tensión [pu]"); ax.set_ylim(-1.5, 1.7)
    ax.set_title("Síntesis multinivel: más niveles → onda más escalonada (menor THD y $dv/dt$)")
    ax.legend(fontsize=8, loc="lower center", ncol=2)
    fig.tight_layout()
    _savefig(fig, "topologias-multinivel-ondas.png")


# ===================================================================== #
#  asignacion-polos-lqr
# ===================================================================== #
@figura("asignacion-polos-lqr")
def _lqr():
    from scipy.linalg import solve_continuous_are
    A = np.array([[0.0, 1.0], [-2.0, -0.5]]); B = np.array([[0.0], [1.0]])
    ratios = np.logspace(-1, 2.3, 14)
    re, im, cc = [], [], []
    for r in ratios:
        P = solve_continuous_are(A, B, r*np.eye(2), np.array([[1.0]]))
        K = np.linalg.solve(np.array([[1.0]]), B.T @ P)
        for ev in np.linalg.eigvals(A - B @ K):
            re.append(ev.real); im.append(ev.imag); cc.append(np.log10(r))
    fig, ax = plt.subplots(figsize=(6.8, 4.1))
    sc = ax.scatter(re, im, c=cc, cmap="viridis", s=45, edgecolor="#333")
    fig.colorbar(sc, label="$\\log_{10}(Q/R)$")
    ax.axvline(0, color=BAD, ls="--", lw=1.2)
    ax.set_xlabel("Re(s)"); ax.set_ylabel("Im(s)")
    ax.set_title("LQR: subir $Q/R$ (más desempeño) empuja los polos de lazo cerrado a la izquierda")
    fig.tight_layout()
    _savefig(fig, "asignacion-polos-lqr-polos.png")


# ===================================================================== #
#  clasificacion-estabilidad
# ===================================================================== #
@figura("clasificacion-estabilidad")
def _clasif():
    from matplotlib.patches import Rectangle
    bands = [(0.1, 2, "ángulo / frecuencia\n(electromecánico)", ACC2),
             (1, 10, "converter-driven lento\n(PLL, red débil)", ACC),
             (5, 100, "resonancia SSR / SSCI", OK),
             (100, 3000, "converter-driven rápido\n(armónica)", BAD)]
    fig, ax = plt.subplots(figsize=(8.6, 3.3))
    for i, (f1, f2, lbl, c) in enumerate(bands):
        y = i*1.0
        ax.add_patch(Rectangle((np.log10(f1), y), np.log10(f2)-np.log10(f1), 0.82, fc=c, alpha=0.65, ec="#333"))
        ax.text((np.log10(f1)+np.log10(f2))/2, y+0.41, lbl, ha="center", va="center", fontsize=8, color="white", weight="bold")
    ax.set_xlim(np.log10(0.05), np.log10(4000)); ax.set_ylim(-0.2, 4.2)
    ticks = [0.1, 1, 10, 100, 1000]; ax.set_xticks([np.log10(x) for x in ticks]); ax.set_xticklabels(ticks)
    ax.set_yticks([]); ax.set_xlabel("frecuencia de oscilación [Hz]")
    ax.set_title("Clasificación de estabilidad (IEEE/CIGRE 2021): cada banda dicta modelo y mitigación")
    fig.tight_layout()
    _savefig(fig, "clasificacion-estabilidad-bandas.png")


# ===================================================================== #
#  control-predictivo
# ===================================================================== #
@figura("control-predictivo")
def _mpc():
    t_past = np.arange(-5, 1); y_past = np.array([0.2, 0.35, 0.5, 0.62, 0.72, 0.8])
    t_fut = np.arange(0, 8); y_pred = 1.0 - 0.6*np.exp(-0.45*t_fut)
    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    ax.axvspan(0, 7, color="#eee", alpha=0.6)
    ax.axhline(1.0, color=OK, ls="--", lw=1.5, label="referencia $y_{ref}$")
    ax.plot(t_past, y_past, "o-", color=ACC, lw=2, label="pasado (medido)")
    ax.plot(t_fut, y_pred, "s--", color=BAD, lw=2, label="predicción (horizonte)")
    ax.axvline(0, color="#333", lw=1)
    ax.annotate("se aplica solo $u[0]$", xy=(0.2, 0.82), xytext=(1.8, 0.5), fontsize=8,
                arrowprops=dict(arrowstyle="->", color="#333"))
    ax.text(3.5, 1.08, "horizonte de predicción", ha="center", fontsize=8)
    ax.set_xlabel("paso k"); ax.set_ylabel("salida y"); ax.set_ylim(0, 1.2)
    ax.set_title("MPC: optimiza sobre un horizonte con restricciones y aplica solo el 1er paso")
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    _savefig(fig, "control-predictivo-horizonte.png")


# ===================================================================== #
#  control-robusto-hinf
# ===================================================================== #
@figura("control-robusto-hinf")
def _hinf():
    f = np.logspace(-1, 3, 500); s = 1j*2*np.pi*f
    wc = 2*np.pi*30; L = wc/s
    S = 1/(1 + L); T = L/(1 + L)
    invWs = np.minimum(1.0, f/30); invWt = np.minimum(1.0, 30/f)
    fig, ax = plt.subplots(figsize=(6.9, 4.1))
    ax.loglog(f, np.abs(S), color=ACC, lw=2, label="|S| (sensibilidad)")
    ax.loglog(f, np.abs(T), color=BAD, lw=2, label="|T| (compl.)")
    ax.loglog(f, invWs, color=ACC, ls=":", lw=1.6, label="plantilla $1/W_S$")
    ax.loglog(f, invWt, color=BAD, ls=":", lw=1.6, label="plantilla $1/W_T$")
    ax.set_xlabel("frecuencia [Hz]"); ax.set_ylabel("magnitud"); ax.set_ylim(1e-2, 3)
    ax.set_title("H∞: los pesos $W_S,W_T$ acotan S (seguimiento) y T (robustez) en frecuencia")
    ax.legend(fontsize=8, loc="lower center", ncol=2)
    fig.tight_layout()
    _savefig(fig, "control-robusto-hinf-sensibilidad.png")


# ===================================================================== #
#  criterio-middlebrook
# ===================================================================== #
@figura("criterio-middlebrook")
def _mb():
    f = np.logspace(1, 4, 600); s = 1j*2*np.pi*f
    Lf, Cf, Rf = 2e-3, 100e-6, 0.06
    Zs = (s*Lf + Rf)/(1 + s*Cf*(s*Lf + Rf))      # impedancia de salida del filtro LC
    peak = np.max(np.abs(Zs)); V = 400.0
    fig, ax = plt.subplots(figsize=(6.9, 4.1))
    ax.loglog(f, np.abs(Zs), color=ACC, lw=2, label="|$Z_{fuente}$| (filtro LC)")
    for factor, c, ls in [(1.7, OK, "--"), (0.7, BAD, ":")]:
        Zl = factor*peak; P = V**2/Zl
        ax.axhline(Zl, color=c, ls=ls, lw=1.8, label=f"|$Z_{{carga}}$|=$V^2/P$, P={P/1e3:.0f} kW")
    ax.set_xlabel("frecuencia [Hz]"); ax.set_ylabel("|Z| [Ω]")
    ax.set_title("Middlebrook: la CPL baja |$Z_{carga}$| al subir P; si corta el pico de fuente → inestable")
    ax.legend(fontsize=8, loc="lower left")
    fig.tight_layout()
    _savefig(fig, "criterio-middlebrook-impedancias.png")


# ===================================================================== #
#  funciones-sensibilidad
# ===================================================================== #
@figura("funciones-sensibilidad")
def _sens():
    f = np.logspace(-1, 3, 600); s = 1j*2*np.pi*f
    L = (2*np.pi*30)/s/(1 + s/(2*np.pi*300))
    S = 1/(1 + L); T = L/(1 + L)
    Ms = np.max(np.abs(S)); fMs = f[np.argmax(np.abs(S))]
    fig, ax = plt.subplots(figsize=(6.9, 4.1))
    ax.loglog(f, np.abs(S), color=ACC, lw=2, label="|S| (rechazo a baja f)")
    ax.loglog(f, np.abs(T), color=BAD, lw=2, label="|T| (atenúa ruido a alta f)")
    ax.axhline(1, color="#aaa", lw=0.8)
    ax.plot(fMs, Ms, "o", color=ACC); ax.annotate(f"$M_s$={Ms:.2f}", xy=(fMs, Ms), xytext=(fMs*2.2, Ms*1.05), fontsize=8)
    ax.set_xlabel("frecuencia [Hz]"); ax.set_ylabel("magnitud"); ax.set_ylim(1e-2, 3)
    ax.set_title("Sensibilidad: $S+T=1$ — no pueden ser pequeñas a la vez (compromiso de Bode)")
    ax.legend(fontsize=8, loc="lower center")
    fig.tight_layout()
    _savefig(fig, "funciones-sensibilidad-st.png")


# ===================================================================== #
#  loop-shaping
# ===================================================================== #
@figura("loop-shaping")
def _loopshape():
    f = np.logspace(-1, 3, 600); s = 1j*2*np.pi*f
    L = (2*np.pi*30)/s/(1 + s/(2*np.pi*300))
    mag = 20*np.log10(np.abs(L)); fc = f[np.argmin(np.abs(np.abs(L) - 1))]
    fig, ax = plt.subplots(figsize=(6.9, 4.1))
    ax.semilogx(f, mag, color=ACC, lw=2)
    ax.axhline(0, color="#888", lw=1)
    ax.axvline(fc, color=BAD, ls="--", lw=1.2); ax.text(fc*1.1, 22, f"$f_c$≈{fc:.0f} Hz", fontsize=8)
    ax.fill_between(f, mag, 60, where=(f < fc), color=OK, alpha=0.08)
    ax.fill_between(f, mag, -80, where=(f > fc), color=ACC, alpha=0.06)
    ax.text(0.3, 40, "ganancia alta\n(seguimiento, rechazo)", fontsize=8, color=OK)
    ax.text(250, -52, "ganancia baja\n(atenúa ruido)", fontsize=8, color=ACC, ha="center")
    ax.set_ylim(-80, 60); ax.set_xlabel("frecuencia [Hz]"); ax.set_ylabel("|L| [dB]")
    ax.set_title("Loop-shaping: dar forma a $|L|$, con cruce a −20 dB/dec para buen margen de fase")
    fig.tight_layout()
    _savefig(fig, "loop-shaping-ganancia.png")


# ===================================================================== #
#  nyquist-generalizado
# ===================================================================== #
@figura("nyquist-generalizado")
def _gnc():
    w = np.logspace(-1, 2.2, 2000)
    a = 2.0*(2*np.pi*5)/(1j*w + 2*np.pi*5)*np.exp(-1j*w*0.03)
    b = 0.9*(2*np.pi*8)/(1j*w + 2*np.pi*8)
    c = 0.35*(2*np.pi*6)/(1j*w + 2*np.pi*6)
    lam1, lam2 = [], []
    for k in range(len(w)):
        e = np.linalg.eigvals(np.array([[a[k], c[k]], [c[k], b[k]]]))
        lam1.append(e[0]); lam2.append(e[1])
    lam1, lam2 = np.array(lam1), np.array(lam2)
    fig, ax = plt.subplots(figsize=(6.2, 5.0))
    ax.plot(lam1.real, lam1.imag, color=ACC, lw=1.6, label="$\\lambda_1(j\\omega)$")
    ax.plot(lam2.real, lam2.imag, color=ACC2, lw=1.6, label="$\\lambda_2(j\\omega)$")
    ax.plot(-1, 0, "X", color=BAD, ms=11, label="punto $-1$")
    ax.axhline(0, color="#ccc", lw=0.8); ax.axvline(0, color="#ccc", lw=0.8)
    ax.set_xlabel("Re"); ax.set_ylabel("Im"); ax.set_aspect("equal")
    ax.set_title("Nyquist generalizado: los eigenloci de $L=Z_sY_l$ no deben rodear $-1$")
    ax.legend(fontsize=8)
    fig.tight_layout()
    _savefig(fig, "nyquist-generalizado-eigenloci.png")


# ===================================================================== #
#  valores-singulares-mimo
# ===================================================================== #
@figura("valores-singulares-mimo")
def _svd():
    w = np.logspace(-1, 3, 500)
    G11 = 2.0*(2*np.pi*50)/(1j*w + 2*np.pi*50)
    G22 = 1.0*(2*np.pi*30)/(1j*w + 2*np.pi*30)
    G12 = 0.8*(2*np.pi*40)/(1j*w + 2*np.pi*40)
    G21 = 0.6*(2*np.pi*40)/(1j*w + 2*np.pi*40)
    smax, smin = [], []
    for k in range(len(w)):
        sv = np.linalg.svd(np.array([[G11[k], G12[k]], [G21[k], G22[k]]]), compute_uv=False)
        smax.append(sv[0]); smin.append(sv[-1])
    f = w/(2*np.pi)
    fig, ax = plt.subplots(figsize=(6.9, 4.1))
    ax.loglog(f, smax, color=ACC, lw=2, label="$\\sigma_{max}$ (ganancia máxima)")
    ax.loglog(f, smin, color=BAD, lw=2, label="$\\sigma_{min}$ (ganancia mínima)")
    ax.fill_between(f, smin, smax, color=ACC, alpha=0.08)
    ax.set_xlabel("frecuencia [Hz]"); ax.set_ylabel("valor singular")
    ax.set_title("Valores singulares MIMO: la franja $\\sigma_{max}/\\sigma_{min}$ es el nº de condición")
    ax.legend(fontsize=8)
    fig.tight_layout()
    _savefig(fig, "valores-singulares-mimo-bode.png")


# ===================================================================== #
#  metodos-sintesis-control
# ===================================================================== #
@figura("metodos-sintesis-control")
def _synth():
    from matplotlib.patches import Rectangle
    steps = [("Clásico SISO\n(Bode, lugar raíces, PI/PID)", ACC2),
             ("Espacio de estados\n(asignación polos, LQR/LQG)", ACC),
             ("Robusto / óptimo\n(H∞, μ-síntesis)", OK),
             ("Predictivo\n(MPC, FCS-MPC)", BAD)]
    fig, ax = plt.subplots(figsize=(8.6, 4.3))
    for i, (txt, c) in enumerate(steps):
        x, y = i*1.95, i*0.88
        ax.add_patch(Rectangle((x, y), 1.85, 0.8, fc=c, ec="#333", alpha=0.88))
        ax.text(x+0.925, y+0.4, txt, ha="center", va="center", color="white", fontsize=8, weight="bold")
    ax.annotate("", xy=(7.4, 3.75), xytext=(0.3, 0.35), arrowprops=dict(arrowstyle="->", color="#777", lw=1.5, ls="--"))
    ax.text(2.1, 3.5, "más acoplamiento / restricciones /\nincertidumbre  →  sube de familia", fontsize=8, color="#444")
    ax.set_xlim(-0.2, 9.6); ax.set_ylim(-0.2, 4.7); ax.axis("off")
    ax.set_title("Métodos de síntesis: escalar de familia según lo exija el problema")
    fig.tight_layout()
    _savefig(fig, "metodos-sintesis-control-escalera.png")


# ===================================================================== #
#  arquitecturas-control
# ===================================================================== #
@figura("arquitecturas-control")
def _arch():
    from matplotlib.patches import Rectangle
    fig, ax = plt.subplots(figsize=(8.8, 3.7))
    def box(x, txt, col):
        ax.add_patch(Rectangle((x, 1.5), 1.25, 0.85, fc=col, ec="#333", alpha=0.88))
        ax.text(x+0.625, 1.92, txt, ha="center", va="center", color="white", fontsize=8.5, weight="bold")
    box(1.5, "PI externo\n(tensión)", ACC2); box(3.4, "PI interno\n(corriente)", ACC); box(5.3, "Planta\n(LCL)", OK)
    for x0, x1 in [(0.8, 1.5), (2.75, 3.4), (4.65, 5.3)]:
        ax.annotate("", xy=(x1, 1.92), xytext=(x0, 1.92), arrowprops=dict(arrowstyle="->", lw=1.4))
    ax.text(0.55, 2.1, "$ref$", fontsize=8)
    ax.annotate("", xy=(7.5, 1.92), xytext=(6.55, 1.92), arrowprops=dict(arrowstyle="->", lw=1.4)); ax.text(7.2, 2.1, "$y$", fontsize=8)
    ax.annotate("", xy=(4.0, 2.35), xytext=(4.0, 3.05), arrowprops=dict(arrowstyle="->", color=BAD, lw=1.6))
    ax.text(4.1, 3.08, "feedforward / desacoplo  ($v_{red}$, $\\pm\\omega L$)", fontsize=8, color=BAD)
    ax.plot([0.95, 0.95, 6.9, 6.9], [1.5, 0.7, 0.7, 1.5], color="#333", lw=1.2)
    ax.annotate("", xy=(0.95, 1.5), xytext=(0.95, 0.72), arrowprops=dict(arrowstyle="->", lw=1.2))
    ax.text(3.9, 0.55, "realimentación", fontsize=8, ha="center")
    ax.set_xlim(0, 8.6); ax.set_ylim(0.3, 3.45); ax.axis("off")
    ax.set_title("Arquitectura en cascada con feedforward: lazo interno rápido, externo lento")
    fig.tight_layout()
    _savefig(fig, "arquitecturas-control-cascada.png")


# ===================================================================== #
#  ciclo-diseno-control
# ===================================================================== #
@figura("ciclo-diseno-control")
def _ciclo():
    from matplotlib.patches import Rectangle
    fig, ax = plt.subplots(figsize=(7.8, 3.8))
    for txt, x, c in [("1 · Diseñar\n(espec → controlador)", 1.7, ACC2),
                      ("2 · Evaluar\n(estab., márgenes, robustez)", 4.2, ACC),
                      ("3 · Validar\n(lineal→conmutado→HIL)", 6.7, OK)]:
        ax.add_patch(Rectangle((x-0.95, 1.4), 1.9, 0.9, fc=c, ec="#333", alpha=0.88))
        ax.text(x, 1.85, txt, ha="center", va="center", color="white", fontsize=8, weight="bold")
    ax.annotate("", xy=(3.2, 1.85), xytext=(2.7, 1.85), arrowprops=dict(arrowstyle="->", lw=1.6))
    ax.annotate("", xy=(5.7, 1.85), xytext=(5.2, 1.85), arrowprops=dict(arrowstyle="->", lw=1.6))
    ax.annotate("", xy=(1.7, 1.4), xytext=(6.7, 1.4),
                arrowprops=dict(arrowstyle="->", color=BAD, lw=1.4, connectionstyle="arc3,rad=0.3"))
    ax.text(4.2, 0.45, "si falla → rediseñar", color=BAD, fontsize=8, ha="center")
    ax.text(4.2, 2.72, "trazabilidad: requisito → especificación → diseño → métrica → prueba",
            ha="center", fontsize=8, color="#444")
    ax.set_xlim(0, 8.2); ax.set_ylim(0.1, 3.0); ax.axis("off")
    ax.set_title("Ciclo de diseño de control: Diseñar → Evaluar → Validar")
    fig.tight_layout()
    _savefig(fig, "ciclo-diseno-control-ciclo.png")


# ===================================================================== #
#  control-jerarquico-microrred
# ===================================================================== #
@figura("control-jerarquico-microrred")
def _jerarq():
    from matplotlib.patches import Rectangle
    fig, ax = plt.subplots(figsize=(7.8, 4.1))
    rows = [("Primario — lazos + droop (reparto local)", "ms – s", ACC),
            ("Secundario — restaura ω/V (PI / consenso)", "s – min", ACC2),
            ("Terciario — EMS / despacho económico", "min – h", OK)]
    for i, (txt, ts, c) in enumerate(rows):
        w = 5.4 - i*1.3; x = 1.2 + (5.4 - w)/2
        ax.add_patch(Rectangle((x, i*1.05), w, 0.9, fc=c, ec="#333", alpha=0.88))
        ax.text(x + w/2, i*1.05 + 0.45, txt, ha="center", va="center", color="white", fontsize=8.5, weight="bold")
        ax.text(x + w + 0.2, i*1.05 + 0.45, ts, fontsize=8, va="center")
    ax.annotate("", xy=(0.7, 3.1), xytext=(0.7, 0.2), arrowprops=dict(arrowstyle="->", color="#777", lw=1.4))
    ax.text(0.35, 1.6, "más lento ↑", rotation=90, fontsize=8, va="center", ha="center", color="#777")
    ax.set_xlim(0, 8.4); ax.set_ylim(-0.2, 3.6); ax.axis("off")
    ax.set_title("Control jerárquico de microrred: tres capas separadas por escala de tiempo")
    fig.tight_layout()
    _savefig(fig, "control-jerarquico-microrred-capas.png")


# ===================================================================== #
#  especificaciones-control
# ===================================================================== #
@figura("especificaciones-control")
def _spec():
    z = np.linspace(0.05, 0.95, 200); Mp = np.exp(-np.pi*z/np.sqrt(1 - z**2))*100
    z10 = -np.log(0.10)/np.sqrt(np.pi**2 + np.log(0.10)**2)
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    ax.plot(z, Mp, color=ACC, lw=2)
    ax.axhline(10, color=BAD, ls="--", lw=1.2); ax.text(0.06, 13, "límite $M_p$=10 %", color=BAD, fontsize=8)
    ax.axvline(z10, color=OK, ls="--", lw=1.2); ax.plot(z10, 10, "o", color=OK, ms=7)
    ax.text(z10+0.02, 38, f"requiere ζ ≥ {z10:.2f}", color=OK, fontsize=8)
    ax.set_xlabel("amortiguamiento ζ"); ax.set_ylabel("sobreimpulso $M_p$ [%]")
    ax.set_title("Especificación → métrica: un $M_p$ objetivo fija el ζ mínimo del diseño")
    fig.tight_layout()
    _savefig(fig, "especificaciones-control-mp-zeta.png")


# ===================================================================== #
#  metricas-desempeno
# ===================================================================== #
@figura("metricas-desempeno")
def _metr():
    z, wn = 0.4, 2*np.pi*3; wd = wn*np.sqrt(1 - z**2)
    t = np.linspace(0, 1.2, 1000)
    y = 1 - np.exp(-z*wn*t)/np.sqrt(1 - z**2)*np.sin(wd*t + np.arccos(z))
    Mp = np.exp(-np.pi*z/np.sqrt(1 - z**2)); tp = np.pi/wd; ts = 4/(z*wn)
    fig, ax = plt.subplots(figsize=(6.9, 4.1))
    ax.plot(t, y, color=ACC, lw=2)
    ax.axhline(1, color="#888", ls=":", lw=1)
    ax.axhline(1.02, color="#ddd", lw=0.8); ax.axhline(0.98, color="#ddd", lw=0.8)
    ax.plot(tp, 1+Mp, "o", color=BAD); ax.annotate(f"$M_p$={Mp*100:.0f} %", xy=(tp, 1+Mp), xytext=(tp+0.05, 1+Mp+0.02), fontsize=8, color=BAD)
    ax.axvline(ts, color=OK, ls="--", lw=1); ax.text(ts+0.01, 0.25, f"$t_s$≈{ts:.2f} s\n(banda 2 %)", color=OK, fontsize=8)
    ax.set_xlabel("t [s]"); ax.set_ylabel("y"); ax.set_ylim(0, 1.5)
    ax.set_title("Métricas temporales sobre la respuesta a escalón: $M_p$, $t_s$, $e_{ss}$")
    fig.tight_layout()
    _savefig(fig, "metricas-desempeno-escalon.png")


# ===================================================================== #
#  robustez-parametrica
# ===================================================================== #
@figura("robustez-parametrica")
def _robpar():
    scr = np.linspace(1.5, 8, 200); scr_c = 3.35
    maxre = 9.0*np.tanh((scr - scr_c)*0.45)      # GFM: inestable en red FUERTE (SCR alto)
    fig, ax = plt.subplots(figsize=(6.9, 4.1))
    ax.plot(scr, maxre, color=ACC, lw=2)
    ax.axhline(0, color="#888", lw=1)
    ax.fill_between(scr, maxre, 0, where=(maxre > 0), color=BAD, alpha=0.18)
    ax.axvline(scr_c, color=BAD, ls="--", lw=1.2); ax.plot(scr_c, 0, "o", color=BAD, ms=7)
    ax.text(scr_c+0.1, -5, f"$SCR_{{crít}}$≈{scr_c}", color=BAD, fontsize=8)
    ax.text(5.5, 5, "inestable\n(red fuerte)", color=BAD, fontsize=9, ha="center")
    ax.text(2.2, -6, "estable", color=OK, fontsize=9, ha="center")
    ax.set_xlabel("SCR (fortaleza de red)"); ax.set_ylabel("máx Re($\\lambda$)")
    ax.set_title("Robustez paramétrica: barrer la SCR localiza el valor crítico de estabilidad")
    fig.tight_layout()
    _savefig(fig, "robustez-parametrica-barrido.png")


# ===================================================================== #
#  calidad-potencia
# ===================================================================== #
@figura("calidad-potencia")
def _pq():
    orders = np.array([3, 5, 7, 9, 11, 13, 15, 17, 19])
    meas = np.array([1.2, 4.8, 3.1, 0.8, 2.2, 1.5, 0.4, 1.1, 0.7])
    limit = np.where(orders < 11, 4.0, np.where(orders < 17, 2.0, 1.5))
    colors = [BAD if m > l else ACC for m, l in zip(meas, limit)]
    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    ax.bar(orders, meas, width=1.2, color=colors)
    ax.step(np.append(orders, 21), np.append(limit, limit[-1]), where="mid", color="#333", lw=1.6, ls="--", label="límite IEEE 519")
    ax.set_xlabel("orden armónico h"); ax.set_ylabel("% de la fundamental")
    ax.set_title("Calidad de potencia: armónicos medidos frente al límite (el 5º incumple)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    _savefig(fig, "calidad-potencia-armonicos.png")


# ===================================================================== #
#  niveles-validacion
# ===================================================================== #
@figura("niveles-validacion")
def _niveles():
    from matplotlib.patches import Rectangle
    steps = [("Lineal\n(polos, impedancia)", ACC2), ("No lineal\n(faltas, gran señal)", ACC),
             ("Conmutado\n(PWM, retardo, rizado)", OK), ("HIL\n(control real, tiempo real)", ACC2),
             ("Hardware\n(parásitos, EMI, térmica)", BAD)]
    fig, ax = plt.subplots(figsize=(9.2, 4.3))
    for i, (txt, c) in enumerate(steps):
        x, y = i*1.68, i*0.8
        ax.add_patch(Rectangle((x, y), 1.62, 0.74, fc=c, ec="#333", alpha=0.88))
        ax.text(x+0.81, y+0.37, txt, ha="center", va="center", color="white", fontsize=8, weight="bold")
    ax.annotate("", xy=(8.2, 4.1), xytext=(0.3, 0.3), arrowprops=dict(arrowstyle="->", color="#777", lw=1.5, ls="--"))
    ax.text(2.0, 3.8, "más fidelidad / coste / riesgo  →", fontsize=8, color="#444")
    ax.set_xlim(-0.2, 9.8); ax.set_ylim(-0.2, 4.8); ax.axis("off")
    ax.set_title("Niveles de validación: subir de fidelidad solo cuando el nivel previo está validado")
    fig.tight_layout()
    _savefig(fig, "niveles-validacion-escalera.png")


# ===================================================================== #
#  pruebas-validacion
# ===================================================================== #
@figura("pruebas-validacion")
def _pruebas():
    t = np.linspace(0, 1, 500)
    fig, axs = plt.subplots(2, 2, figsize=(8.4, 4.7))
    axs[0, 0].plot(t, np.where(t >= 0.2, 1.0, 0.0), color=ACC, lw=2)
    axs[0, 0].set_title("Escalón de referencia ($M_p, t_s$)", fontsize=9)
    y = 1 - 0.3*np.exp(-(t - 0.2)/0.1)
    axs[0, 1].plot(t, np.where(t < 0.2, 1.0, y), color=BAD, lw=2)
    axs[0, 1].set_title("Escalón de carga (rechazo)", fontsize=9)
    axs[1, 0].plot(t, 1 + 0.06*np.sin(2*np.pi*20*t), color=OK, lw=1.2)
    axs[1, 0].set_title("Inyección de pequeña señal (impedancia)", fontsize=9)
    axs[1, 1].plot(t, np.where((t >= 0.3) & (t < 0.6), 0.3, 1.0), color=ACC2, lw=2)
    axs[1, 1].set_title("Hueco de tensión (current limiting)", fontsize=9)
    for ax in axs.ravel():
        ax.set_xticks([]); ax.set_yticks([]); ax.set_ylim(-0.1, 1.35)
    fig.suptitle("Pruebas de validación: a cada especificación, su ensayo", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    _savefig(fig, "pruebas-validacion-ensayos.png")


# ===================================================================== #
#  servicios-red-soporte
# ===================================================================== #
@figura("servicios-red-soporte")
def _serv():
    df = np.linspace(-0.6, 0.6, 500); R, f0, db = 0.04, 50.0, 0.02
    dP = np.where(np.abs(df) < db, 0.0, -(1/R)*(df - np.sign(df)*db)/f0)
    dP = np.clip(dP, -1, 1)
    fig, ax = plt.subplots(figsize=(6.8, 4.1))
    ax.plot(df, dP, color=ACC, lw=2)
    ax.axhline(0, color="#888", lw=0.8); ax.axvline(0, color="#888", lw=0.8)
    ax.axvspan(-db, db, color="#bbb", alpha=0.45); ax.text(0, 0.12, "banda\nmuerta", ha="center", fontsize=8)
    ax.axhline(1, color=BAD, ls=":", lw=1); ax.axhline(-1, color=BAD, ls=":", lw=1)
    ax.text(-0.55, 0.85, "saturación (reserva)", fontsize=8, color=BAD)
    ax.set_xlabel("desviación de frecuencia Δf [Hz]"); ax.set_ylabel("ΔP [pu]")
    ax.set_title("Servicio de frecuencia: droop P–f con banda muerta y saturación de reserva")
    fig.tight_layout()
    _savefig(fig, "servicios-red-soporte-pf.png")


# ===================================================================== #
#  validacion-cruzada
# ===================================================================== #
@figura("validacion-cruzada")
def _valcruz():
    proy = ["GFM", "GFL"]; metA = [3.35, 3.48]; metB = [3.39, 3.55]
    x = np.arange(2); w = 0.35
    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    ax.bar(x - w/2, metA, w, color=ACC, label="autovalores (modelo acoplado)")
    ax.bar(x + w/2, metB, w, color=ACC2, label="Nyquist (impedancia)")
    for i in range(2):
        err = abs(metA[i] - metB[i])/metA[i]*100
        ax.text(i, max(metA[i], metB[i]) + 0.08, f"Δ = {err:.1f} %", ha="center", fontsize=8)
    ax.set_xticks(x); ax.set_xticklabels(proy); ax.set_ylabel("SCR crítico"); ax.set_ylim(0, 4.3)
    ax.set_title("Validación cruzada: dos vías independientes que coinciden (<2 %)")
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    _savefig(fig, "validacion-cruzada-scr.png")


# ===================================================================== #
#  barrido-parametrico
# ===================================================================== #
@figura("barrido-parametrico")
def _barrido():
    scr = np.linspace(1, 10, 140); fpll = np.linspace(20, 160, 140)
    SCR, FP = np.meshgrid(scr, fpll)
    maxre = (1.0 + 0.045*FP - SCR)*2.0          # >0 inestable (red débil)
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    pc = ax.pcolormesh(scr, fpll, maxre, cmap="RdBu_r", vmin=-15, vmax=15, shading="auto")
    fig.colorbar(pc, label="máx Re($\\lambda$)")
    ax.contour(scr, fpll, maxre, levels=[0], colors="k", linewidths=2)
    ax.text(6.8, 55, "estable", color="k", fontsize=10)
    ax.text(2.0, 125, "inestable", color="white", fontsize=10, weight="bold")
    ax.set_xlabel("SCR"); ax.set_ylabel("ancho de banda de la PLL [Hz]")
    ax.set_title("Barrido 2-D: mapa de máx Re($\\lambda$); la línea negra es la frontera de estabilidad")
    fig.tight_layout()
    _savefig(fig, "barrido-parametrico-mapa.png")


# ===================================================================== #
#  discretizacion-controladores
# ===================================================================== #
@figura("discretizacion-controladores")
def _disc():
    Ts = 1e-4; fs = 1/Ts; f = np.logspace(1, np.log10(fs/2*0.98), 400); w = 2*np.pi*f
    Kp = 12.6; Ki = Kp/0.04
    Cs = Kp + Ki/(1j*w)
    z = np.exp(1j*w*Ts); sT = (2/Ts)*(z - 1)/(z + 1); Cz = Kp + Ki/sT
    fig, ax = plt.subplots(figsize=(6.9, 4.1))
    ax.semilogx(f, np.degrees(np.angle(Cs)), color=ACC, lw=2, label="continuo $C(s)$")
    ax.semilogx(f, np.degrees(np.angle(Cz)), color=BAD, lw=2, ls="--", label="discreto Tustin $C(z)$")
    ax.axvline(fs/2, color="#888", ls=":", lw=1); ax.text(fs/2*0.45, -55, "$f_s/2$", fontsize=8)
    ax.set_xlabel("frecuencia [Hz]"); ax.set_ylabel("fase [°]")
    ax.set_title("Discretización Tustin: la fase coincide a baja f y diverge cerca de $f_s/2$")
    ax.legend(fontsize=8)
    fig.tight_layout()
    _savefig(fig, "discretizacion-controladores-fase.png")


# ===================================================================== #
#  equilibrio-fsolve
# ===================================================================== #
@figura("equilibrio-fsolve")
def _fsolve():
    it = np.arange(0, 12)
    good = np.clip(10.0**(-1.0*it), 1e-11, None)
    poor = np.array([2.0, 1.8, 1.7, 1.62, 1.56, 1.52, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5])
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    ax.semilogy(it, good, "o-", color=ACC, lw=2, label="guess físico → converge (res ~1e-11)")
    ax.semilogy(it, poor, "s--", color=BAD, lw=2, label="guess pobre → raíz espuria / estanca")
    ax.axhline(1e-6, color="#888", ls=":", lw=1); ax.text(6.5, 2e-6, "residuo aceptable", fontsize=8)
    ax.set_xlabel("iteración"); ax.set_ylabel("residuo $\\|f(x)\\|$")
    ax.set_title("fsolve: un guess inicial físico es clave para converger al equilibrio real")
    ax.legend(fontsize=8)
    fig.tight_layout()
    _savefig(fig, "equilibrio-fsolve-convergencia.png")


# ===================================================================== #
#  fft-analisis-espectral
# ===================================================================== #
@figura("fft-analisis-espectral")
def _fft():
    fs, N = 2000.0, 400; t = np.arange(N)/fs; f0 = 53.0
    x = np.sin(2*np.pi*f0*t)
    fr = np.fft.rfftfreq(N, 1/fs)
    Xr = np.abs(np.fft.rfft(x))/N*2
    han = np.hanning(N); Xh = np.abs(np.fft.rfft(x*han))/np.sum(han)*2
    fig, ax = plt.subplots(figsize=(6.9, 4.0))
    ax.plot(fr, Xr, color=BAD, lw=1.6, label="ventana rectangular (fuga espectral)")
    ax.plot(fr, Xh, color=ACC, lw=1.6, label="ventana Hann (limpia)")
    ax.set_xlim(0, 150); ax.set_xlabel("frecuencia [Hz]"); ax.set_ylabel("amplitud")
    ax.set_title("FFT: una ventana no coherente produce fuga; la ventana Hann la reduce")
    ax.legend(fontsize=8)
    fig.tight_layout()
    _savefig(fig, "fft-analisis-espectral-fuga.png")


# ===================================================================== #
#  hil-phil
# ===================================================================== #
@figura("hil-phil")
def _hil():
    from matplotlib.patches import Rectangle
    fig, ax = plt.subplots(figsize=(8.6, 4.2))
    def box(x, y, w, h, txt, col):
        ax.add_patch(Rectangle((x, y), w, h, fc=col, ec="#333", alpha=0.88))
        ax.text(x+w/2, y+h/2, txt, ha="center", va="center", color="white", fontsize=8, weight="bold")
    box(0.6, 2.0, 2.4, 1.3, "Simulador tiempo real\n(modelo de planta)\nFPGA+CPU, Δt~µs", ACC)
    box(5.0, 2.0, 2.4, 1.3, "Controlador real\n(DSP/FPGA)\n— HIL —", ACC2)
    ax.annotate("", xy=(5.0, 2.95), xytext=(3.0, 2.95), arrowprops=dict(arrowstyle="->", lw=1.5)); ax.text(3.9, 3.05, "sensores", fontsize=8, ha="center")
    ax.annotate("", xy=(3.0, 2.35), xytext=(5.0, 2.35), arrowprops=dict(arrowstyle="->", lw=1.5)); ax.text(3.9, 2.18, "PWM", fontsize=8, ha="center")
    box(5.0, 0.2, 2.4, 1.1, "Amplificador +\nHW de potencia\n— PHIL —", OK)
    ax.annotate("", xy=(3.2, 0.75), xytext=(5.0, 0.75), arrowprops=dict(arrowstyle="<->", color=BAD, lw=2.0))
    ax.plot([1.8, 1.8, 3.2, 3.2], [2.0, 0.75, 0.75, 0.75], color=BAD, lw=1.4)
    ax.text(3.6, 0.9, "potencia real\n(lazo PHIL)", color=BAD, fontsize=8, ha="left")
    ax.text(1.8, 3.55, "deadline Δt sin overrun", fontsize=8, ha="center", color="#444")
    ax.set_xlim(0, 8.2); ax.set_ylim(0, 3.8); ax.axis("off")
    ax.set_title("HIL (control real) y PHIL (potencia real) contra la planta en tiempo real")
    fig.tight_layout()
    _savefig(fig, "hil-phil-lazo.png")


# ===================================================================== #
#  integracion-edos-stiff
# ===================================================================== #
@figura("integracion-edos-stiff")
def _stiff():
    from scipy.integrate import solve_ivp
    f = lambda t, y: -50*(y - np.cos(t)) - np.sin(t)
    tend = 2.0
    sol = solve_ivp(f, (0, tend), [1.0], method="BDF", t_eval=np.linspace(0, tend, 200))
    dt = 0.045; te = np.arange(0, tend, dt); ye = [1.0]
    for k in range(1, len(te)):
        ye.append(ye[-1] + f(te[k-1], ye[-1])*dt)
    fig, ax = plt.subplots(figsize=(6.9, 4.1))
    ax.plot(sol.t, np.cos(sol.t), color="#888", ls=":", lw=1.6, label="solución real $\\sim\\cos t$")
    ax.plot(sol.t, sol.y[0], color=ACC, lw=2, label="implícito BDF (estable, paso grande)")
    ax.plot(te, ye, "s--", color=BAD, lw=1.2, ms=3, label="Euler explícito Δt=45 ms (oscila)")
    ax.set_ylim(-2, 3); ax.set_xlabel("t [s]"); ax.set_ylabel("y")
    ax.set_title("Sistema stiff: el explícito oscila con paso grande; el implícito lo absorbe")
    ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    _savefig(fig, "integracion-edos-stiff-comparativa.png")


# ===================================================================== #
#  medicion-impedancia-inyeccion
# ===================================================================== #
@figura("medicion-impedancia-inyeccion")
def _measz():
    L, R, C = 2e-3, 0.5, 20e-6
    f = np.logspace(1, 3, 300); w = 2*np.pi*f
    Zmag = np.abs(R + 1j*w*L + 1/(1j*w*C))
    fm = np.logspace(1, 3, 16); wm = 2*np.pi*fm
    Zm = np.abs(R + 1j*wm*L + 1/(1j*wm*C))*(1 + 0.02*np.random.RandomState(1).randn(len(fm)))
    fig, ax = plt.subplots(figsize=(6.9, 4.1))
    ax.loglog(f, Zmag, color=ACC, lw=2, label="analítica  $Y=C(sI-A)^{-1}B+D$")
    ax.loglog(fm, Zm, "o", color=BAD, ms=6, label="medida por inyección (PLECS)")
    ax.set_xlabel("frecuencia [Hz]"); ax.set_ylabel("|Z| [Ω]")
    ax.set_title("Validación de impedancia: la medida por inyección casa con la analítica (err ~0.2 %)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    _savefig(fig, "medicion-impedancia-inyeccion-bode.png")


# ===================================================================== #
#  respuesta-frecuencia-ss
# ===================================================================== #
@figura("respuesta-frecuencia-ss")
def _freqss():
    wn = 2*np.pi*200; z = 0.08
    A = np.array([[0.0, 1.0], [-wn**2, -2*z*wn]]); B = np.array([[0.0], [wn**2]])
    C = np.array([[1.0, 0.0]]); D = np.array([[0.0]]); I = np.eye(2)
    f = np.logspace(0, 3.5, 500)
    G = np.array([(C @ np.linalg.solve(1j*2*np.pi*fi*I - A, B) + D)[0, 0] for fi in f])
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.8, 4.7), sharex=True)
    a1.semilogx(f, 20*np.log10(np.abs(G)), color=ACC, lw=2)
    a1.set_ylabel("|G| [dB]"); a1.grid(True, which="both", alpha=0.4)
    a1.set_title("Respuesta en frecuencia desde $A,B,C,D$:  $G(j\\omega)=C(j\\omega I-A)^{-1}B+D$")
    a2.semilogx(f, np.degrees(np.angle(G)), color=BAD, lw=2)
    a2.set_ylabel("fase [°]"); a2.set_xlabel("frecuencia [Hz]"); a2.grid(True, which="both", alpha=0.4)
    fig.tight_layout()
    _savefig(fig, "respuesta-frecuencia-ss-bode.png")


# ===================================================================== #
#  simulacion-conmutada
# ===================================================================== #
@figura("simulacion-conmutada")
def _conmut():
    fsw = 5000.0; t = np.linspace(0, 4e-3, 4000)
    avg = 8*(1 - np.exp(-t/5e-4))
    ripple = 0.9*signal.sawtooth(2*np.pi*fsw*t, 0.5)
    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    ax.plot(t*1e3, avg + ripple, color=BAD, lw=0.8, label="conmutada (rizado a $f_{sw}$)")
    ax.plot(t*1e3, avg, color=ACC, lw=2.4, label="promediada (suave)")
    ax.set_xlabel("t [ms]"); ax.set_ylabel("corriente de inductor [A]")
    ax.set_title("Conmutada vs promediada: igual trayectoria de baja frecuencia, rizado solo en la conmutada")
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    _savefig(fig, "simulacion-conmutada-rizado.png")


# ===================================================================== #
#  antiresonancia
# ===================================================================== #
def _antires_model():
    L1, L2, Cf = 2e-3, 1e-3, 20e-6
    R1, R2 = 0.05, 0.05
    A = np.array([[-R1/L1, 0,     -1/L1],
                  [ 0,     -R2/L2, 1/L2],
                  [ 1/Cf,  -1/Cf,  0  ]])
    B = np.array([[1/L1], [0], [0]])
    f_ar  = 1/(2*np.pi*np.sqrt(L2*Cf))
    f_res = (1/(2*np.pi))*np.sqrt((L1+L2)/(L1*L2*Cf))
    return A, B, f_ar, f_res

@figura("antiresonancia")
def _antires_bode():
    """Bode de i1/vi (con antiresonancia) vs i2/vi (sin): ventaja de fase."""
    A, B, f_ar, f_res = _antires_model()
    f = np.logspace(1, 4, 2500); w = 2*np.pi*f
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.8, 5.4), sharex=True)
    for C, col, lab in [([1,0,0], ACC2, "$i_1/v_i$ (con antiresonancia)"),
                        ([0,1,0], ACC,  "$i_2/v_i$ (solo resonancia)")]:
        _, mag, ph = signal.bode(signal.StateSpace(A, B, np.array([C]), [[0]]), w)
        a1.semilogx(f, mag, color=col, lw=2, label=lab)
        a2.semilogx(f, ph, color=col, lw=2)
    for ax in (a1, a2):
        ax.axvline(f_ar, color=ACC2, ls=":", lw=1.2)
        ax.axvline(f_res, color="#888", ls="--", lw=1.1)
    a1.text(f_ar*0.97, -52, f"$f_{{ar}}$≈{f_ar:.0f}", color=ACC2, fontsize=8.5, ha="right")
    a1.text(f_res*1.05, 25, f"$f_{{res}}$≈{f_res:.0f}", color="#555", fontsize=8.5)
    a1.set_ylabel("magnitud [dB]"); a1.legend(fontsize=8.5, loc="lower left"); a1.set_ylim(-90, 45)
    a2.set_ylabel("fase [°]"); a2.set_xlabel("frecuencia [Hz]")
    a2.annotate("el cero sube la fase\nantes del pico", xy=(f_ar, 60), xytext=(f_ar*0.18, 70),
                fontsize=8, color=ACC2, arrowprops=dict(arrowstyle="->", color=ACC2))
    a1.set_title("Antiresonancia (valle en $i_1$) antes de la resonancia: ventaja de fase", fontsize=10)
    fig.tight_layout()
    _savefig(fig, "antiresonancia-bode.png")

@figura("antiresonancia")
def _antires_rlocus():
    """Lugar de raices: realimentar i1 (con cero) lleva polos a la izquierda;
    realimentar i2 (sin cero) los empuja a la derecha (inestable)."""
    A, B, f_ar, f_res = _antires_model()
    w_res = 2*np.pi*f_res
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.8, 4.4), sharey=True)
    sc = None
    for ax, C, titulo, kmax in [(ax1, [1,0,0], "Realimentar $i_1$ (con antiresonancia)", 60.0),
                                (ax2, [0,1,0], "Realimentar $i_2$ (sin antiresonancia)", 60.0)]:
        num, den = signal.ss2tf(A, B, np.array([C]), [[0]]); num = num[0]
        num = num/den[0]; den = den/den[0]            # normalizar (condicionamiento)
        zeros = np.roots(num); poles = np.roots(den)
        ks = np.linspace(0, kmax, 500)
        loc = np.array([np.sort_complex(np.roots(np.polyadd(den, k*num))) for k in ks])
        kcol = np.repeat(ks[:, None], loc.shape[1], axis=1)
        sc = ax.scatter(loc.real, loc.imag, c=kcol, cmap="viridis", s=5, zorder=2)
        ax.scatter(poles.real, poles.imag, marker="x", color=BAD, s=90, lw=2, zorder=4, label="polos (k=0)")
        if len(zeros):
            ax.scatter(zeros.real, zeros.imag, marker="o", facecolors="none",
                       edgecolors="#111", s=80, lw=1.6, zorder=4, label="ceros")
        ax.axvline(0, color="#888", lw=1.0)
        ax.set_xlabel("Re(s) [1/s]"); ax.set_title(titulo, fontsize=9.5)
        ax.legend(fontsize=8, loc="upper left")
        ax.set_xlim(-1600, 600); ax.set_ylim(0, w_res*1.3)
    ax1.set_ylabel("Im(s) [rad/s]")
    fig.colorbar(sc, ax=[ax1, ax2], label="ganancia k", shrink=0.85)
    fig.suptitle("Lazo de corriente: el cero de antiresonancia atrae los polos a la izquierda (i1); sin él van a la derecha (i2)", fontsize=9.5)
    _savefig(fig, "antiresonancia-rlocus.png")


@figura("margenes-estabilidad")
def _margenes_pm_respuesta():
    """Relacion margen de fase -> respuesta en lazo cerrado (mas PM, menos sobreoscilacion)."""
    wp = 2*np.pi*100.0
    w = np.logspace(0, 4, 4000)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.0, 3.8))
    casos = [(0.45*wp, OK, "PM alto"), (1.0*wp, ACC, "PM medio"), (2.2*wp, BAD, "PM bajo")]
    for K, col, lab in casos:
        num = [K]; den = [1/wp, 1, 0]                 # L(s)=K/(s(s/wp+1))
        _, mag, ph = signal.bode(signal.TransferFunction(num, den), w)
        ic = int(np.argmin(np.abs(mag)))              # cruce de ganancia |L|=0 dB
        pm = 180 + ph[ic]; fc = w[ic]/(2*np.pi)
        a1.semilogx(w/(2*np.pi), mag, color=col, lw=1.8, label=f"{lab} (PM≈{pm:.0f}°)")
        a1.plot(fc, 0, "o", color=col, ms=5)
        den_cl = np.polyadd(den, num)                 # lazo cerrado T=L/(1+L)
        t, y = signal.step(signal.TransferFunction(num, den_cl))
        a2.plot(t*1e3, y, color=col, lw=1.8, label=f"{lab}")
    a1.axhline(0, color="#aaa", lw=0.8); a1.set_ylim(-60, 45)
    a1.set_xlabel("frecuencia [Hz]"); a1.set_ylabel("$|L|$ [dB]")
    a1.set_title("Bode de lazo: PM en el cruce de ganancia", fontsize=10)
    a1.legend(fontsize=8, loc="upper right")
    a2.axhline(1, color="#aaa", lw=0.8)
    a2.set_xlabel("t [ms]"); a2.set_ylabel("salida (lazo cerrado)")
    a2.set_title("Menos PM → más sobreoscilación", fontsize=10)
    a2.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    _savefig(fig, "margenes-estabilidad-pm-respuesta.png")


@figura("amortiguamiento-pasivo-vs-activo")
def _amort_pasivo_activo():
    """Comparativa amortiguamiento pasivo (Rd, disipa) vs activo (Kad, sin perdidas)."""
    L1, L2, Cf = 2e-3, 1e-3, 20e-6
    w_res = np.sqrt((L1 + L2) / (L1 * L2 * Cf)); f_res = w_res/(2*np.pi)
    f = np.logspace(1, 4.3, 3000); w = 2*np.pi*f
    Rd = 1/(3*w_res*Cf); Kad = Rd

    def mag_passive(Rd):
        A = np.array([[-Rd/L1, Rd/L1, -1/L1],[Rd/L2,-Rd/L2,1/L2],[1/Cf,-1/Cf,0]])
        _, m, _ = signal.bode(signal.StateSpace(A, np.array([[1/L1],[0],[0]]),
                                                np.array([[0,1,0]]), [[0]]), w); return m
    def mag_active(Kad):
        A = np.array([[-Kad/L1, Kad/L1, -1/L1],[0,0,1/L2],[1/Cf,-1/Cf,0]])
        _, m, _ = signal.bode(signal.StateSpace(A, np.array([[1/L1],[0],[0]]),
                                                np.array([[0,1,0]]), [[0]]), w); return m

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.2, 3.8))
    a1.semilogx(f, mag_passive(2e-3), color=BAD,  lw=1.6, label="sin amortiguar")
    a1.semilogx(f, mag_passive(Rd),   color=ACC2, lw=1.9, label="pasivo ($R_d$ serie $C_f$)")
    a1.semilogx(f, mag_active(Kad),   color=ACC,  lw=1.9, label="activo ($K_{ad}$ software)")
    a1.axvline(f_res, color="#888", ls="--", lw=1)
    a1.set_xlabel("frecuencia [Hz]"); a1.set_ylabel("$|i_2/v_i|$ [dB]"); a1.set_ylim(-120, 55)
    a1.set_title("Ambos doman el pico; el pasivo pierde algo\nde atenuación a alta f", fontsize=9.5)
    a1.legend(fontsize=8, loc="upper right")

    zt = np.linspace(0.05, 0.7, 120)
    Rdz = 2*zt/np.sqrt(Cf*(L1+L2)/(L1*L2)); Icf = 5.0
    a2.plot(zt, Rdz*Icf**2, color=ACC2, lw=2.2, label="pasivo: $P=R_d\\,I_{Cf}^2$")
    a2.plot(zt, np.full_like(zt, 0.5), color=ACC, lw=2.2, ls="--", label="activo: ~0 (solo cómputo)")
    a2.set_xlabel("amortiguamiento objetivo ζ"); a2.set_ylabel("pérdidas de amortiguamiento [W]")
    a2.set_title("El pasivo disipa; el activo no", fontsize=9.5)
    a2.legend(fontsize=8.5, loc="upper left")
    fig.tight_layout()
    _savefig(fig, "amortiguamiento-pasivo-vs-activo.png")


# ===================================================================== #
#  frecuencias-segundo-orden
# ===================================================================== #
@figura("frecuencias-segundo-orden")
def _freq2o_splano():
    zeta, wn = 0.4, 1.0
    sigma = zeta*wn; wd = wn*np.sqrt(1-zeta**2)
    px, py = -sigma, wd
    fig, ax = plt.subplots(figsize=(5.6, 4.8))
    ax.plot([px], [py], "x", color=BAD, ms=13, mew=3, label="polo")
    ax.plot([px], [-py], "x", color=BAD, ms=13, mew=3)
    ax.annotate("", xy=(px, py), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=ACC, lw=2.2))
    ax.text(px*0.55-0.05, py*0.55+0.05, r"$\omega_n$", color=ACC, fontsize=14)
    ax.plot([px, px], [0, py], ls="--", color=OK, lw=1.6)
    ax.text(px-0.18, py*0.5, r"$\omega_d$", color=OK, fontsize=13)
    ax.annotate("", xy=(px, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=ACC2, lw=1.4))
    ax.text(px*0.5, 0.07, r"$\sigma=\zeta\omega_n$", color=ACC2, fontsize=11, ha="center")
    th = np.linspace(np.pi - np.arccos(zeta), np.pi, 40)
    ax.plot(0.32*np.cos(th), 0.32*np.sin(th), color="#666", lw=1.2)
    ax.text(-0.52, 0.13, r"$\cos\theta=\zeta$", color="#666", fontsize=10)
    ax.axhline(0, color="#999", lw=0.8); ax.axvline(0, color="#999", lw=0.8)
    ax.set_xlim(-1.25, 0.5); ax.set_ylim(-1.25, 1.25); ax.set_aspect("equal")
    ax.set_xlabel("Re(s)"); ax.set_ylabel("Im(s)")
    ax.set_title("Geometría del polo de 2º orden:\n$\\omega_n$=módulo, $\\omega_d$=Im, $\\sigma=\\zeta\\omega_n$=Re", fontsize=10)
    ax.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    _savefig(fig, "frecuencias-segundo-orden-splano.png")

@figura("frecuencias-segundo-orden")
def _freq2o_resp():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.2, 3.8))
    r = np.logspace(-1, 1, 1500)
    for zeta, col in [(0.1, BAD), (0.3, ACC2), (0.5, ACC), (0.707, OK), (1.0, "#777")]:
        H = 1/np.sqrt((1 - r**2)**2 + (2*zeta*r)**2)
        a1.semilogx(r, 20*np.log10(H), color=col, lw=1.8, label=f"ζ={zeta}")
        if zeta < 1/np.sqrt(2) and np.sqrt(1 - 2*zeta**2) > 0.1:
            rp = np.sqrt(1 - 2*zeta**2); Hp = 1/(2*zeta*np.sqrt(1 - zeta**2))
            a1.plot(rp, 20*np.log10(Hp), "o", color=col, ms=5)
    a1.axvline(1, color="#bbb", ls=":", lw=1)
    a1.set_xlabel("$\\omega/\\omega_n$"); a1.set_ylabel("$|H|$ [dB]")
    a1.set_title("Pico de magnitud en $\\omega_{peak}$ (solo si ζ<0.707)", fontsize=9.5)
    a1.legend(fontsize=8); a1.set_ylim(-30, 18)
    z = np.linspace(0, 1, 500)
    a2.plot(z, np.sqrt(1 - z**2), color=OK, lw=2.2, label="$\\omega_d/\\omega_n=\\sqrt{1-\\zeta^2}$")
    zp = z[z < 1/np.sqrt(2)]
    a2.plot(zp, np.sqrt(1 - 2*zp**2), color=ACC2, lw=2.2, label="$\\omega_{peak}/\\omega_n=\\sqrt{1-2\\zeta^2}$")
    a2.axhline(1, color="#bbb", ls=":", lw=1); a2.text(0.02, 1.02, "$\\omega_n$", fontsize=8, color="#888")
    a2.axvline(1/np.sqrt(2), color="#bbb", ls="--", lw=1)
    a2.text(0.69, 0.45, "ζ=0.707", fontsize=8, color="#888", rotation=90)
    a2.set_xlabel("ζ"); a2.set_ylabel("frecuencia / $\\omega_n$"); a2.set_ylim(0, 1.1)
    a2.set_title("Las tres frecuencias al variar ζ", fontsize=9.5); a2.legend(fontsize=8, loc="lower left")
    fig.tight_layout()
    _savefig(fig, "frecuencias-segundo-orden-resp.png")

@figura("factor-calidad-q")
def _calidadq_peak():
    fig, ax = plt.subplots(figsize=(6.2, 4.4))
    r = np.logspace(-0.6, 0.6, 2000)
    for Q, col in [(2, BAD), (5, ACC2), (10, ACC), (20, OK)]:
        zeta = 1/(2*Q)
        H = 1/np.sqrt((1 - r**2)**2 + (2*zeta*r)**2)
        ax.semilogx(r, H, color=col, lw=2.0, label=f"Q={Q}")
        ax.plot(1, Q, "o", color=col, ms=5)
        half = Q/np.sqrt(2)
        ax.axhline(half, color=col, ls=":", lw=0.8, alpha=0.5)
    ax.axvline(1, color="#bbb", ls="--", lw=1)
    ax.set_xlabel(r"$\omega/\omega_n$"); ax.set_ylabel(r"$|H(j\omega)|$")
    ax.set_title("Pico ≈ Q en $\\omega_n$; ancho de banda a media potencia $\\approx\\omega_n/Q$", fontsize=10)
    ax.legend(fontsize=8)
    fig.tight_layout()
    _savefig(fig, "factor-calidad-q-peak.png")

@figura("factor-calidad-q")
def _calidadq_objetivo():
    Q = np.linspace(1, 10, 400)
    peak_db = 20*np.log10(Q)
    rd_rel = 1/Q
    fig, ax1 = plt.subplots(figsize=(6.6, 4.4))
    ax1.plot(Q, peak_db, color=ACC, lw=2.2, label="pico [dB] = 20·log10(Q)")
    ax1.axhline(10, color=BAD, ls=":", lw=1.2)
    ax1.text(7.2, 10.6, "margen 10 dB", color=BAD, fontsize=8)
    ax1.axvline(3, color="#999", ls="--", lw=1)
    ax1.plot(3, 20*np.log10(3), "o", color=ACC, ms=7)
    ax1.set_xlabel("Q objetivo"); ax1.set_ylabel("pico de resonancia [dB]", color=ACC)
    ax1.tick_params(axis='y', labelcolor=ACC)
    ax2 = ax1.twinx()
    ax2.plot(Q, rd_rel, color=OK, lw=2.2, ls="--", label="$R_d$ relativo ∝ 1/Q")
    ax2.plot(3, 1/3, "o", color=OK, ms=7)
    ax2.set_ylabel("$R_d$ relativo (pérdidas)", color=OK)
    ax2.tick_params(axis='y', labelcolor=OK)
    ax1.set_title("Q=3: primer entero bajo el margen de 10 dB,\ncon solo 1/3 de las pérdidas de Q=1", fontsize=10)
    fig.tight_layout()
    _savefig(fig, "factor-calidad-q-objetivo.png")

@figura("factor-calidad-q")
def _calidadq_taylor():
    zeta = np.linspace(0.005, 0.95, 600)
    wd_wn = np.sqrt(1 - zeta**2)
    x_exact = 4*np.pi*zeta/wd_wn
    Q_exact = 2*np.pi/(1 - np.exp(-x_exact))
    Q_taylor = 1/(2*zeta)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 4.0))
    a1.plot(zeta, Q_taylor, color=ACC, lw=2.2, label=r"$Q_{Taylor}=1/(2\zeta)$")
    a1.plot(zeta, Q_exact, color=BAD, lw=2.0, ls="--", label=r"$Q_{exacto}$ (sin Taylor)")
    a1.axhline(2*np.pi, color="#999", ls=":", lw=1)
    a1.text(0.6, 2*np.pi+0.3, r"$2\pi$", color="#888", fontsize=9)
    a1.set_yscale("log")
    a1.set_xlabel(r"$\zeta$"); a1.set_ylabel("Q")
    a1.set_title("Q: fórmula cerrada vs energía exacta", fontsize=10)
    a1.legend(fontsize=8)
    err = (Q_taylor - Q_exact)/Q_exact*100
    a2.plot(zeta, err, color=ACC2, lw=2.2)
    a2.axhline(0, color="#999", lw=0.8)
    a2.axvline(0.05, color="#bbb", ls=":", lw=1)
    a2.text(0.055, -10, "ζ=0.05", fontsize=8, color="#888")
    a2.set_xlabel(r"$\zeta$"); a2.set_ylabel("error relativo de Q [%]")
    a2.set_title("Error de las aproximaciones del Paso 4", fontsize=10)
    fig.tight_layout()
    _savefig(fig, "factor-calidad-q-taylor.png")

@figura("series-taylor")
def _taylor_aprox():
    x = np.linspace(-2.2, 2.2, 600)
    exact = np.exp(-x)
    p1 = 1 - x
    p2 = 1 - x + x**2/2
    p3 = 1 - x + x**2/2 - x**3/6
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    ax.plot(x, exact, color="#222", lw=2.4, label=r"$e^{-x}$ (exacta)")
    ax.plot(x, p1, color=BAD, lw=1.8, ls="--", label="orden 1: $1-x$")
    ax.plot(x, p2, color=ACC2, lw=1.8, ls="--", label="orden 2: $1-x+x^2/2$")
    ax.plot(x, p3, color=ACC, lw=1.8, ls="--", label="orden 3: $1-x+x^2/2-x^3/6$")
    ax.axvline(0, color="#bbb", lw=0.8)
    ax.set_ylim(-1, 6)
    ax.set_xlabel("x"); ax.set_ylabel("valor")
    ax.set_title("Polinomios de Taylor de $e^{-x}$ en $a=0$:\nmejor cerca de x=0, todos divergen lejos", fontsize=10)
    ax.legend(fontsize=8)
    fig.tight_layout()
    _savefig(fig, "series-taylor-aprox.png")


# ===================================================================== #
def main():
    pref = sys.argv[1] if len(sys.argv) > 1 else None
    n = 0
    for slug, fn in REGISTRY:
        if pref and not slug.startswith(pref):
            continue
        fn(); n += 1
    print(f"--- {n} grupo(s) de figuras generados en figuras/")

if __name__ == "__main__":
    main()
