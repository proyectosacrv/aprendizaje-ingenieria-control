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

def _savefig(fig, name, dpi=150):
    fig.savefig(os.path.join(OUT, name), dpi=dpi, bbox_inches="tight")
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
    """Diseño del rizado: banda real sobre i1 en el ciclo, y curva de diseño L1 vs rizado objetivo."""
    Vdc, fsw, In = 700.0, 10e3, 20.0
    m = 0.9
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.8, 3.7))

    # (a) banda de rizado real sobre la fundamental i1(t), un ciclo completo
    theta = np.linspace(0, 2*np.pi, 600)
    d = (1 + m*np.sin(theta))/2
    L1_demo = 2.0e-3
    dipp = (Vdc/(fsw*L1_demo))*d*(1 - d)           # pico-pico instantaneo (depende de la fase)
    i_fund = In*np.sin(theta)
    deg = np.degrees(theta)
    ax1.fill_between(deg, i_fund - dipp/2, i_fund + dipp/2, color=ACC, alpha=0.30,
                      label="rizado real sobre $i_1$")
    ax1.plot(deg, i_fund, color=ACC, lw=1.6, label="fundamental (50 Hz)")
    for xv in (0, 180, 360):
        ax1.axvline(xv, color=BAD, ls=":", lw=0.9)
    for xv in (90, 270):
        ax1.axvline(xv, color=OK, ls=":", lw=0.9)
    dipp_max = dipp.max()
    ax1.annotate("rizado máximo\n($v_o=0$, $d=0.5$)", xy=(360, dipp_max/2), xytext=(220, 9),
                 fontsize=8.5, color=BAD, arrowprops=dict(arrowstyle="->", color=BAD))
    ax1.annotate("rizado mínimo\n(pico de $v_o$, $d\\to1$)", xy=(90, In),
                 xytext=(140, 13), fontsize=8.5, color=OK,
                 arrowprops=dict(arrowstyle="->", color=OK))
    ax1.set_xlabel("fase del ciclo de red [°]"); ax1.set_ylabel("$i_1$ [A]")
    ax1.set_title(f"Banda de rizado sobre $i_1$ ($L_1$={L1_demo*1e3:.0f} mH)", fontsize=10)
    ax1.set_xlim(0, 360); ax1.set_ylim(-26, 26); ax1.set_xticks([0, 90, 180, 270, 360])
    ax1.legend(fontsize=8, loc="lower left")

    # (b) curva de diseno directa: L1 minimo en funcion del rizado objetivo (amplitud, factor 8)
    frac = np.linspace(0.05, 0.30, 300)
    L1_min = Vdc/(8*fsw*frac*In)
    ax2.plot(frac*100, L1_min*1e3, color=ACC, lw=2.2)
    for f0, col in [(0.20, ACC2), (0.10, OK)]:
        L1_0 = Vdc/(8*fsw*f0*In)
        ax2.plot([f0*100], [L1_0*1e3], "o", color=col, zorder=5)
        ax2.vlines(f0*100, 0, L1_0*1e3, color=col, ls=":", lw=1)
        ax2.hlines(L1_0*1e3, 0, f0*100, color=col, ls=":", lw=1)
        ax2.annotate(f"{int(f0*100)}% de $I_n$ → $L_1\\approx${L1_0*1e3:.2f} mH",
                     xy=(f0*100, L1_0*1e3), xytext=(f0*100+1.5, L1_0*1e3+1.3),
                     fontsize=8.5, color=col)
    ax2.set_xlabel("rizado objetivo $\\Delta i_{1,amp}$ [% de $I_n$]")
    ax2.set_ylabel("$L_1$ mínimo [mH]")
    ax2.set_title("Curva de diseño: cuánta $L_1$ hace falta", fontsize=10)
    ax2.set_xlim(5, 30); ax2.set_ylim(0, 16)
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


@figura("filtro-lcl")
def _lcl_red_vs_aislado():
    """Apartado 8: comparativa red fuerte vs red debil (mismo Rd) en las magnitudes clave."""
    L1, Cf = 40e-6, 85e-6           # valores reales del proyecto 04
    L2_solo = 8e-6
    fsw = 10e3; wsw = 2*np.pi*fsw
    # Rd OPTIMO se fija en red fuerte (Q=3) y NO se retoca: con el cae Q en el texto.
    LeqF0 = L1*72e-6/(L1+72e-6); fresF0 = 1/(2*np.pi*np.sqrt(LeqF0*Cf))
    Rd_opt = 1/(3*2*np.pi*fresF0*Cf)        # ~0.183 ohm -> Q=3 en red fuerte (apartado 3)
    Rd_bode = 0.03                          # solo para el Bode: el optimo aplana el pico
    casos = [(72e-6,  "Red fuerte ($L_g=0$)",    ACC),
             (196e-6, "Red débil ($L_g=124$ µH)", BAD)]

    def vC_over_vi(L2, w, Rd):
        s = 1j*w; Zc = (1 + s*Rd*Cf)/(s*Cf)
        return (1/(s*L1)) / (1/(s*L1) + 1/(s*L2) + 1/Zc)

    def mags(L2):
        Leq = L1*L2/(L1+L2)
        fres = 1/(2*np.pi*np.sqrt(Leq*Cf)); far = 1/(2*np.pi*np.sqrt(L2*Cf))
        Q = (1/Rd_opt)*np.sqrt(Leq/Cf); k = 1/(wsw**2*L2*Cf)
        return Leq, fres, far, Q, k

    f = np.logspace(2.5, 4.3, 3000); w = 2*np.pi*f
    fig, axs = plt.subplots(2, 2, figsize=(9.2, 7.0))

    # (a) |i2/vi|: pico de resonancia. Se desplaza a la izquierda con la red.
    axa = axs[0, 0]
    for L2, lab, col in casos:
        m = 20*np.log10(np.abs(vC_over_vi(L2, w, Rd_bode)/(1j*w*L2)))
        _, fres, _, _, _ = mags(L2)
        axa.semilogx(f, m, color=col, lw=2.0, label=lab)
        axa.axvline(fres, color=col, ls="--", lw=1.0, alpha=0.6)
    axa.set_title("(a) $|i_2/v_i|$: resonancia (pico)", fontsize=10)
    axa.set_xlabel("frecuencia [Hz]"); axa.set_ylabel("magnitud [dB]")
    axa.set_ylim(-20, 30); axa.legend(fontsize=8, loc="upper right")
    axa.annotate("$f_{res}$ baja\n3404→2995 Hz", xy=(3000, 14), xytext=(1100, 22),
                 fontsize=8, color="#333", arrowprops=dict(arrowstyle="->", color="#777"))

    # (b) |i1/vi|: valle de antiresonancia. Baja mucho mas que fres.
    axb = axs[0, 1]
    for L2, lab, col in casos:
        m = 20*np.log10(np.abs((1 - vC_over_vi(L2, w, Rd_bode))/(1j*w*L1)))
        _, _, far, _, _ = mags(L2)
        axb.semilogx(f, m, color=col, lw=2.0, label=lab)
        axb.axvline(far, color=col, ls=":", lw=1.0, alpha=0.7)
    axb.set_title("(b) $|i_1/v_i|$: antiresonancia (valle)", fontsize=10)
    axb.set_xlabel("frecuencia [Hz]"); axb.set_ylabel("magnitud [dB]")
    axb.set_ylim(-60, 20); axb.legend(fontsize=8, loc="upper right")
    axb.annotate("$f_{ar}$ baja más\n2034→1233 Hz (−39%)", xy=(1233, -38),
                 xytext=(2300, -20), fontsize=8, color="#333",
                 arrowprops=dict(arrowstyle="->", color="#777"))

    # (c) barras comparativas de fres, far, Q (normalizadas para verlas juntas)
    axc = axs[1, 0]
    LF, fresF, farF, QF, kF = mags(72e-6)
    LD, fresD, farD, QD, kD = mags(196e-6)
    labels = ["$f_{res}$\n[Hz]", "$f_{ar}$\n[Hz]", "$Q$", "$L_{eq}$\n[µH]"]
    fuerte = [fresF, farF, QF, LF*1e6]; debil = [fresD, farD, QD, LD*1e6]
    x = np.arange(len(labels)); wbar = 0.36
    bF = axc.bar(x - wbar/2, fuerte, wbar, color=ACC, label="Red fuerte")
    bD = axc.bar(x + wbar/2, debil, wbar, color=BAD, label="Red débil")
    axc.set_yscale("log"); axc.set_xticks(x); axc.set_xticklabels(labels, fontsize=9)
    axc.set_title("(c) Magnitudes clave (escala log)", fontsize=10)
    axc.legend(fontsize=8, loc="upper right")
    for rects, vals in [(bF, fuerte), (bD, debil)]:
        for r, v in zip(rects, vals):
            axc.annotate(f"{v:.0f}" if v >= 10 else f"{v:.1f}",
                         xy=(r.get_x()+r.get_width()/2, v), xytext=(0, 2),
                         textcoords="offset points", ha="center", fontsize=7.5, color="#333")

    # (d) atenuacion a fsw: mejora con la red (kef/k) pero no es controlable
    axd = axs[1, 1]
    escenarios = ["$L_2$ sola\n(8 µH)", "Red fuerte\n(72 µH)", "Red débil\n(196 µH)"]
    L2s = [L2_solo, 72e-6, 196e-6]
    ks = [1/(wsw**2*L2*Cf)*100 for L2 in L2s]
    cols = [OK, ACC, BAD]
    bars = axd.bar(escenarios, ks, color=cols)
    axd.set_title("(d) Atenuación a $f_{sw}$: $k=|i_2/i_1|$", fontsize=10)
    axd.set_ylabel("$k$ a $f_{sw}$ [%]")
    for r, v in zip(bars, ks):
        axd.annotate(f"{v:.1f}%", xy=(r.get_x()+r.get_width()/2, v), xytext=(0, 2),
                     textcoords="offset points", ha="center", fontsize=8.5, color="#333")
    axd.annotate("la red mejora $k$\n(×9 y ×24), pero\nno es controlable",
                 xy=(2, kD*100/1), xytext=(0.3, 25), fontsize=8, color="#333",
                 arrowprops=dict(arrowstyle="->", color="#777"))
    axd.set_ylim(0, 42)

    fig.suptitle("Apartado 8 — efecto de la red sobre el filtro (mismo amortiguamiento, fijado en red fuerte)",
                 fontsize=11, y=0.995)
    fig.tight_layout(rect=[0, 0, 1, 0.98])
    _savefig(fig, "filtro-lcl-red-vs-aislado.png")


@figura("filtro-lcl")
def _lcl_L2_atenuacion():
    """Calidad de la aproximacion (despreciar el 1) y curva de diseno L2 vs k objetivo."""
    Cf, fsw = 29.84155182973037e-6, 10e3   # mismos valores que el ejemplo de codigo
    L1 = 2.857738033247041e-3
    wsw = 2*np.pi*fsw
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.8, 3.7))

    # (a) exacta vs aproximada |i2/i1| en funcion de fsw/far
    x = np.logspace(0.02, np.log10(30), 400)            # fsw/far
    exacta = 1/np.abs(1 - x**2)
    aprox = 1/x**2
    ax1.loglog(x, exacta, color=ACC, lw=2.0, label="exacta: $1/|1-x^2|$")
    ax1.loglog(x, aprox, color=ACC2, lw=1.8, ls="--", label="aprox.: $1/x^2$")
    ax1.axvspan(5, 15, color=OK, alpha=0.12, label="rango típico $f_{sw}/f_{ar}$")
    for xv in (5, 10):
        err = -100/xv**2
        ax1.annotate(f"error {err:.1f}%", xy=(xv, 1/xv**2), xytext=(xv*1.15, 1/xv**2*2.3),
                     fontsize=8, color="#555")
    ax1.set_xlabel("$x=f_{sw}/f_{ar}$"); ax1.set_ylabel("$|i_2/i_1|$")
    ax1.set_title("Calidad de la aproximación (Paso 3)", fontsize=10)
    ax1.legend(fontsize=8, loc="upper right")

    # (b) curva de diseno L2 vs k objetivo, con la tension frente al rango practico de r
    k_pct = np.logspace(np.log10(0.2), np.log10(35), 400)
    L2_uH = 1/((k_pct/100)*Cf*wsw**2)*1e6
    ax2.loglog(k_pct, L2_uH, color=ACC, lw=2.2)
    ax2.axvspan(10, 20, color=ACC2, alpha=0.15, label="$k$ típico (Reznik, 10–20%)")
    ax2.axhspan(0.2*L1*1e6, 1.0*L1*1e6, color=OK, alpha=0.15, label="$L_2$ con $r$ en [0.2, 1]")
    for kk, col, dy in [(10, ACC2, 2.6), (20, ACC2, 4.2)]:
        L2v = 1/((kk/100)*Cf*wsw**2)*1e6
        ax2.plot([kk], [L2v], "o", color=col, zorder=5)
        ax2.annotate(f"$k$={kk}%, $L_2$≈{L2v:.0f} µH, $r$≈{L2v/(L1*1e6):.2f}",
                     xy=(kk, L2v), xytext=(kk*0.55, L2v*dy), fontsize=7.5, color="#333")
    ax2.set_xlabel("$k$ objetivo [%]"); ax2.set_ylabel("$L_2$ [µH]")
    ax2.set_title("Curva de diseño: $L_2$ vs $k$ (Paso 4)", fontsize=10)
    ax2.set_xlim(0.2, 35); ax2.set_ylim(10, 5000)
    ax2.legend(fontsize=7.5, loc="upper right")
    fig.tight_layout()
    _savefig(fig, "filtro-lcl-L2-atenuacion.png")


@figura("filtro-lcl")
def _lcl_diseno_iterativo():
    """Apartado 9: el diseno completo como proceso iterativo (3 iteraciones encadenadas)."""
    Sn, Vll, f0, Vdc, fsw = 10e3, 400, 50, 700, 10e3
    w0, wsw = 2*np.pi*f0, 2*np.pi*fsw
    In = (Sn/(np.sqrt(3)*Vll))*np.sqrt(2)
    L1 = Vdc/(8*fsw*0.15*In)                  # fijo por rizado en todas las iteraciones

    def estado(Cf, L2, Rd):
        Leq = L1*L2/(L1+L2)
        fres = 1/(2*np.pi*np.sqrt(Leq*Cf)); far = 1/(2*np.pi*np.sqrt(L2*Cf))
        k = 1/(wsw**2*L2*Cf); r = L2/L1
        Q = (1/Rd)*np.sqrt(Leq/Cf); zeta = 1/(2*Q)
        return dict(Cf=Cf, L2=L2, Leq=Leq, fres=fres, far=far, k=k, r=r, Rd=Rd, Q=Q, zeta=zeta)

    # It0: cada apartado por separado -> r fuera de rango
    Cf0 = 0.05*Sn/(w0*(Vll/np.sqrt(3))**2); L2_0 = 1/(0.10*Cf0*wsw**2)
    Rd0 = 1/(3*2*np.pi*(1/(2*np.pi*np.sqrt(L1*L2_0/(L1+L2_0)*Cf0)))*Cf0)
    it0 = estado(Cf0, L2_0, Rd0)
    # It1: subir L2 a r=0.3 bajando Cf -> r ok, pero verificar red debil despues
    Cf1, L2_1 = 20e-6, 0.3*L1
    Rd1 = 1/(3*2*np.pi*(1/(2*np.pi*np.sqrt(L1*L2_1/(L1+L2_1)*Cf1)))*Cf1)
    it1 = estado(Cf1, L2_1, Rd1)
    # red debil sobre it1 (SCR=10): zeta cae por debajo de 0.1
    Lg = 5.09e-3; L2ef = L2_1 + Lg
    fres_ef = 1/(2*np.pi*np.sqrt(L1*L2ef/(L1+L2ef)*Cf1))
    it1_debil = estado(Cf1, L2ef, Rd1)
    # It2: re-amortiguar a fres del peor caso -> ambos extremos en banda
    Rd2 = 1/(3*2*np.pi*fres_ef*Cf1)
    it2_fuerte = estado(Cf1, L2_1, Rd2); it2_debil = estado(Cf1, L2ef, Rd2)

    fig, axs = plt.subplots(2, 2, figsize=(9.4, 7.2))

    # (a) recorrido en el plano (r, k): de it0 (fuera) a it1 (dentro)
    axa = axs[0, 0]
    axa.axvspan(0.2, 1.0, color=OK, alpha=0.12, label="$r$ práctico [0.2, 1]")
    axa.axhspan(10, 20, color=ACC2, alpha=0.12, label="$k$ típico [10, 20]%")
    axa.plot([it0["r"], it1["r"]], [it0["k"]*100, it1["k"]*100], "-", color="#999", zorder=1)
    axa.scatter([it0["r"]], [it0["k"]*100], color=BAD, s=90, zorder=3, label="It.0 (ingenuo)")
    axa.scatter([it1["r"]], [it1["k"]*100], color=ACC, s=90, zorder=3, label="It.1 (sube $L_2$)")
    axa.annotate("$r$=0.03\nfuera", xy=(it0["r"], it0["k"]*100), xytext=(0.05, 25),
                 fontsize=8, color=BAD, arrowprops=dict(arrowstyle="->", color=BAD))
    axa.annotate("$r$=0.30 ✓\n$k$ mejora a 1.5%", xy=(it1["r"], it1["k"]*100),
                 xytext=(0.4, 6), fontsize=8, color=ACC,
                 arrowprops=dict(arrowstyle="->", color=ACC))
    axa.set_xscale("log"); axa.set_xlabel("$r=L_2/L_1$"); axa.set_ylabel("$k$ a $f_{sw}$ [%]")
    axa.set_title("(a) Conflicto 1: $r$ fuera de rango → subir $L_2$", fontsize=10)
    axa.set_xlim(0.02, 1.2); axa.set_ylim(0, 30); axa.legend(fontsize=7.5, loc="upper right")

    # (b) fres a lo largo de las iteraciones + banda y caida por red debil
    axb = axs[0, 1]
    etapas = ["It.0\n(Cf=29.8µF)", "It.1\naislado", "It.1\nred débil", "It.2\nred débil"]
    fresv = [it0["fres"], it1["fres"], fres_ef, fres_ef]
    cols = [BAD, ACC, ACC2, OK]
    axb.axhspan(500, 5000, color=OK, alpha=0.10, label="banda $10f_0$–$f_{sw}/2$")
    axb.bar(etapas, fresv, color=cols)
    for i, v in enumerate(fresv):
        axb.annotate(f"{v:.0f} Hz", xy=(i, v), xytext=(0, 2), textcoords="offset points",
                     ha="center", fontsize=8, color="#333")
    axb.set_ylabel("$f_{res}$ [Hz]"); axb.set_ylim(0, 5500)
    axb.set_title("(b) $f_{res}$ se desplaza en cada paso", fontsize=10)
    axb.legend(fontsize=8, loc="upper right")

    # (c) zeta: el cuello de botella. it1 cae bajo 0.1 en red debil; it2 lo arregla
    axc = axs[1, 0]
    casos = ["It.1\nred fuerte", "It.1\nred débil", "It.2\nred fuerte", "It.2\nred débil"]
    zetas = [it1["zeta"], it1_debil["zeta"], it2_fuerte["zeta"], it2_debil["zeta"]]
    colz = [ACC, BAD, OK, OK]
    axc.axhspan(0.1, 0.3, color=OK, alpha=0.12, label="$\\zeta$ objetivo [0.1, 0.3]")
    bars = axc.bar(casos, zetas, color=colz)
    axc.axhline(0.1, color=BAD, ls="--", lw=1)
    for i, v in enumerate(zetas):
        axc.annotate(f"{v:.3f}", xy=(i, v), xytext=(0, 2), textcoords="offset points",
                     ha="center", fontsize=8, color="#333")
    axc.annotate("cae < 0.1\n(re-amortiguar)", xy=(1, it1_debil["zeta"]), xytext=(1.4, 0.22),
                 fontsize=8, color=BAD, arrowprops=dict(arrowstyle="->", color=BAD))
    axc.set_ylabel("$\\zeta$ del par resonante"); axc.set_ylim(0, 0.32)
    axc.set_title("(c) Conflicto 2: $\\zeta$ cae en red débil → re-amortiguar", fontsize=10)
    axc.legend(fontsize=8, loc="upper left")

    # (d) tabla-resumen del recorrido: que cambia y que se hereda en cada iteracion
    axd = axs[1, 1]
    axd.axis("off")
    filas = ["$L_1$ [mH]", "$C_f$ [µF]", "$L_2$ [mH]", "$r$", "$k$ [%]",
             "$f_{res}$ [Hz]", "$R_d$ [Ω]", "$\\zeta$ débil"]
    col_it0 = [f"{L1*1e3:.2f}", f"{Cf0*1e6:.1f}", f"{L2_0*1e3:.3f}", f"{it0['r']:.2f} ✗",
               f"{it0['k']*100:.1f}", f"{it0['fres']:.0f}", "—", "—"]
    col_it1 = [f"{L1*1e3:.2f}", f"{Cf1*1e6:.0f}", f"{L2_1*1e3:.2f}", f"{it1['r']:.2f} ✓",
               f"{it1['k']*100:.1f}", f"{it1['fres']:.0f}", f"{Rd1:.2f}", f"{it1_debil['zeta']:.3f} ✗"]
    col_it2 = [f"{L1*1e3:.2f}", f"{Cf1*1e6:.0f}", f"{L2_1*1e3:.2f}", f"{it2_fuerte['r']:.2f} ✓",
               f"{it2_fuerte['k']*100:.1f}", f"{it2_fuerte['fres']:.0f}", f"{Rd2:.2f}",
               f"{it2_debil['zeta']:.3f} ✓"]
    tabla = axd.table(cellText=list(zip(col_it0, col_it1, col_it2)),
                      rowLabels=filas, colLabels=["It.0", "It.1", "It.2"],
                      loc="center", cellLoc="center")
    tabla.auto_set_font_size(False); tabla.set_fontsize(9); tabla.scale(1.0, 1.45)
    # colorear la columna final y los cambios clave
    for (r, c), cell in tabla.get_celld().items():
        if c == 2 and r > 0: cell.set_facecolor("#eafbe7")
        if r == 0: cell.set_facecolor("#f0f0f0")
    axd.set_title("(d) Recorrido completo: qué cambia y qué se hereda", fontsize=10, pad=2)

    fig.suptitle("Apartado 9 — diseño completo como proceso iterativo (10 kVA, 400 V, $f_{sw}$=10 kHz)",
                 fontsize=11, y=0.998)
    fig.tight_layout(rect=[0, 0, 1, 0.98])
    _savefig(fig, "filtro-lcl-diseno-iterativo.png")


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


@figura("control-cascada")
def _cascada_sintonia():
    """Sintonia de los dos PI: cancelacion de polo (corriente) y separacion de escalas."""
    L1, R1, Cf = 2e-3, 0.1, 20e-6
    fci, fcv = 1000.0, 350.0
    wci, wcv = 2*np.pi*fci, 2*np.pi*fcv
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.0, 3.8))

    # (a) lazo de corriente: planta, PI y lazo abierto -> integrador puro tras cancelar
    f = np.logspace(0, 4, 2000); w = 2*np.pi*f; s = 1j*w
    planta = 1/(L1*s + R1)
    Kp, Ti = L1*wci, L1/R1
    pi = Kp*(Ti*s + 1)/(Ti*s)
    L_ol = pi*planta
    ax1.semilogx(f, 20*np.log10(np.abs(planta*R1)), color="#888", lw=1.4, ls=":",
                 label="planta $1/(sL_1{+}R_1)$ (norm.)")
    ax1.semilogx(f, 20*np.log10(np.abs(L_ol)), color=ACC, lw=2.2,
                 label="lazo abierto $L(s)$ = integrador")
    ax1.axvline(fci, color=OK, ls="--", lw=1.1)
    ax1.axvline(R1/L1/(2*np.pi), color=BAD, ls=":", lw=1.1)
    ax1.axhline(0, color="#555", lw=0.8)
    ax1.text(R1/L1/(2*np.pi)*1.1, 38, f"polo planta =\ncero PI\n({R1/L1/(2*np.pi):.0f} Hz)",
             color=BAD, fontsize=7.5)
    ax1.text(fci*1.08, 25, f"$f_{{ci}}$={fci:.0f} Hz\n($|L|$=1)", color=OK, fontsize=8)
    ax1.set_xlabel("frecuencia [Hz]"); ax1.set_ylabel("magnitud [dB]")
    ax1.set_title("(a) Lazo de corriente: el PI cancela el polo", fontsize=9.5)
    ax1.set_ylim(-40, 60); ax1.legend(fontsize=7.5, loc="upper right")

    # (b) separacion de escalas: lazo interno cerrado ~1 donde actua el externo
    Hi = wci/(s + wci)                       # corriente cerrada (1er orden)
    ax2.semilogx(f, 20*np.log10(np.abs(Hi)), color=ACC, lw=2.2,
                 label="lazo corriente cerrado")
    ax2.axvspan(1, fcv, color=OK, alpha=0.12, label="banda del lazo de tensión")
    ax2.axvline(fcv, color=OK, ls="--", lw=1.1)
    ax2.axvline(fci, color=ACC, ls="--", lw=1.1)
    ax2.axhline(-3, color="#aaa", ls=":", lw=1)
    ax2.text(fcv*0.30, -16, f"$f_{{cv}}$={fcv:.0f} Hz\naquí el interno\nvale ≈1", color=OK, fontsize=8)
    ax2.annotate(f"$f_{{ci}}/f_{{cv}}$≈{fci/fcv:.1f}×", xy=(fci, -3), xytext=(fci*1.2, -22),
                 fontsize=8.5, color="#333", arrowprops=dict(arrowstyle="->", color="#777"))
    ax2.set_xlabel("frecuencia [Hz]"); ax2.set_ylabel("$|i_{L1}/i_{L1}^*|$ [dB]")
    ax2.set_title("(b) Separación de escalas (interno ≫ externo)", fontsize=9.5)
    ax2.set_ylim(-30, 6); ax2.legend(fontsize=7.5, loc="lower left")
    fig.tight_layout()
    _savefig(fig, "control-cascada-sintonia.png")


@figura("control-cascada")
def _cascada_lcl_limite():
    """El LCL limita el lazo de tension: fcv debe quedar bajo fres; escalon antes/despues."""
    L1, L2, Cf, R1 = 2e-3, 1e-3, 20e-6, 0.1
    Leq = L1*L2/(L1+L2); wres = np.sqrt((L1+L2)/(L1*L2*Cf)); fres = wres/(2*np.pi)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.0, 3.8))

    # (a) bandas de control sobre el modulo de la planta de tension con resonancia
    f = np.logspace(1, 4, 3000); w = 2*np.pi*f; s = 1j*w
    Rd = 1/(3*wres*Cf)
    # vC/iL1* aprox: pico resonante. Uso 1/(sCf) modulada por el factor resonante con damping.
    H = 1/(s*Cf) * (wres**2)/(s**2 + 2*0.1*wres*s + wres**2)
    ax1.semilogx(f, 20*np.log10(np.abs(H)), color="#888", lw=1.8, label="planta $v_C/i_{L1}^*$")
    ax1.axvline(fres, color=BAD, ls="--", lw=1.4); ax1.text(fres*1.05, 60, f"$f_{{res}}$\n{fres:.0f} Hz", color=BAD, fontsize=8)
    for fc, lab, col in [(350, "$f_{cv}$ tensión", OK), (1000, "$f_{ci}$ corriente", ACC)]:
        ax1.axvline(fc, color=col, ls=":", lw=1.3); ax1.text(fc*0.62, 18, lab, color=col, fontsize=8, rotation=90)
    ax1.axvspan(10, fres, color=OK, alpha=0.07)
    ax1.set_xlabel("frecuencia [Hz]"); ax1.set_ylabel("magnitud [dB]")
    ax1.set_title("(a) $f_{cv}<f_{ci}<f_{res}$: el control va\npor debajo de la resonancia", fontsize=9.5)
    ax1.set_ylim(-20, 80); ax1.legend(fontsize=8, loc="lower left")

    # (b) escalon de vC: estable (fcv bajo) vs excitado (fcv subido sin amortiguar)
    t = np.linspace(0, 12e-3, 1200)
    def step(fc, zeta):
        wn = 2*np.pi*fc; wd = wn*np.sqrt(1-zeta**2)
        return 1 - np.exp(-zeta*wn*t)*(np.cos(wd*t) + (zeta/np.sqrt(1-zeta**2))*np.sin(wd*t))
    ax2.plot(t*1e3, step(350, 0.7), color=OK, lw=2.2, label="$f_{cv}$=350 Hz (amortiguado)")
    # subir fcv cerca de fres sin amortiguar -> oscilacion mantenida
    wn2 = 2*np.pi*fres; zeta2 = 0.04
    y2 = 1 - np.exp(-zeta2*wn2*t)*np.cos(wn2*np.sqrt(1-zeta2**2)*t)
    ax2.plot(t*1e3, y2, color=BAD, lw=1.6, label="$f_{cv}$ subido a $f_{res}$ sin amortiguar")
    ax2.axhline(1, color="#aaa", ls=":", lw=1)
    ax2.set_xlabel("tiempo [ms]"); ax2.set_ylabel("$v_C$ (norm.)")
    ax2.set_title("(b) Escalón de $v_C$: subir $f_{cv}$ a $f_{res}$\nexcita la resonancia", fontsize=9.5)
    ax2.set_ylim(-0.2, 2.1); ax2.legend(fontsize=7.5, loc="upper right")
    fig.tight_layout()
    _savefig(fig, "control-cascada-lcl-limite.png")


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
#  convertidor-vsc (analisis extendido)
# ===================================================================== #
@figura("convertidor-vsc")
def _vsc_extended():
    """4 paneles: (a) formas de onda PWM, (b) rizado vs L1, (c) impedancia, (d) mapa m-Vdc."""
    Vdc = 1200.0; fsw = 10e3; m0 = 0.85; L1 = 2e-3; Cf = 15e-6
    f0 = 50.0; Vll = 690.0
    Vf = Vll * np.sqrt(2) / np.sqrt(3)

    fig, axes = plt.subplots(2, 2, figsize=(12.0, 8.0))
    ax_a, ax_b = axes[0, 0], axes[0, 1]
    ax_c, ax_d = axes[1, 0], axes[1, 1]

    # (a) Formas de onda PWM: 3 periodos
    Tsw = 1.0 / fsw; N = 2000
    t = np.linspace(0.0, 3 * Tsw, N)
    carrier = 1.0 - 2.0 * np.abs(2.0 * ((t * fsw) % 1.0) - 1.0)
    mod = m0 * np.sin(2 * np.pi * f0 * t)
    v_sw = np.where(mod >= carrier, Vdc / 2.0, -Vdc / 2.0)
    wnd = max(1, N // 3)
    v_avg = np.convolve(v_sw, np.ones(wnd) / wnd, mode="same")
    tus = t * 1e6
    ax_a.plot(tus, carrier * (Vdc / 2.0), color="#aaa", lw=1.2, ls="--", label="portadora")
    ax_a.plot(tus, mod * (Vdc / 2.0), color=ACC2, lw=1.8, label=f"moduladora (m={m0})")
    ax_a.step(tus, v_sw, color=BAD, lw=1.1, alpha=0.75, label="conmutada", where="post")
    ax_a.plot(tus, v_avg, color=ACC, lw=2.0, label="promediada")
    ax_a.set_xlabel("t [us]"); ax_a.set_ylabel("Tension [V]")
    ax_a.set_title("(a) Formas de onda PWM — 3 periodos", fontsize=10)
    ax_a.legend(fontsize=7.5, loc="upper right"); ax_a.set_xlim(tus[0], tus[-1])

    # (b) Rizado vs L1 para 3 fsw
    L1_arr = np.linspace(0.5e-3, 5.0e-3, 300)
    for fsw_i, col, lbl in [(5e3, BAD, "$f_{sw}$=5 kHz"),
                             (10e3, ACC, "$f_{sw}$=10 kHz"),
                             (20e3, OK, "$f_{sw}$=20 kHz")]:
        ax_b.plot(L1_arr * 1e3, Vdc / (4.0 * L1_arr * fsw_i), color=col, lw=2.0, label=lbl)
    di_des = Vdc / (4.0 * L1 * fsw)
    ax_b.plot([L1 * 1e3], [di_des], "o", color=ACC, ms=7, zorder=5)
    ax_b.annotate(f"L1={L1*1e3:.0f} mH\ndi={di_des:.1f} A",
                  xy=(L1 * 1e3, di_des), xytext=(L1 * 1e3 + 0.6, di_des + 8),
                  fontsize=8.5, color=ACC, arrowprops=dict(arrowstyle="->", color=ACC))
    ax_b.set_xlabel("$L_1$ [mH]"); ax_b.set_ylabel("$\\Delta i_{L,pp}$ max [A]")
    ax_b.set_title("(b) Rizado de $i_L$ vs $L_1$", fontsize=10)
    ax_b.legend(fontsize=8.5); ax_b.set_xlim(0.5, 5.0)

    # (c) Impedancia de salida
    f_arr = np.logspace(2, np.log10(2.0 * fsw), 400)
    w_arr = 2.0 * np.pi * f_arr
    w0lc = 1.0 / np.sqrt(L1 * Cf)
    ratio2 = (w_arr / w0lc) ** 2
    Z_avg = np.abs(1j * w_arr * L1) / np.maximum(np.abs(1.0 - ratio2), 0.05)
    Z_sw = Z_avg / np.sqrt(1.0 + (f_arr / fsw) ** 2)
    ax_c.loglog(f_arr, Z_avg, color=ACC, lw=2.0, label="Promediado")
    ax_c.loglog(f_arr, Z_sw, color=BAD, lw=2.0, ls="--", label="Conmutado (aprox)")
    ax_c.axvline(fsw, color="#888", ls=":", lw=1.2)
    ax_c.axvline(fsw / 2.0, color="#bbb", ls=":", lw=1.0)
    yref = ax_c.get_ylim()[0] if ax_c.get_ylim()[0] > 0 else 0.01
    ax_c.set_xlabel("Frecuencia [Hz]"); ax_c.set_ylabel("|Z| [Ohm]")
    ax_c.set_title("(c) Impedancia: divergencia cerca de $f_{sw}$", fontsize=10)
    ax_c.legend(fontsize=8.5)

    # (d) Mapa de operacion
    Vdn = np.linspace(1.0, 3.0, 300)
    m_arr = 2.0 / Vdn
    ax_d.fill_between(Vdn, 0, 1.0,    color=OK,   alpha=0.15, label="Lineal (m<=1)")
    ax_d.fill_between(Vdn, 1.0, 1.27, color=ACC2, alpha=0.18, label="Sobremod (1<m<=1.27)")
    ax_d.fill_between(Vdn, 1.27, 2.0, color=BAD,  alpha=0.12, label="Saturacion (m>1.27)")
    ax_d.plot(Vdn, m_arr, color=ACC, lw=2.2, label="$m=2\\hat{V}_f/V_{dc}$")
    ax_d.axhline(1.0,  color=OK,   ls="--", lw=1.2)
    ax_d.axhline(1.15, color=ACC2, ls="--", lw=1.0)
    ax_d.axhline(1.27, color=BAD,  ls="--", lw=1.0)
    ax_d.text(2.5, 0.50, "SPWM lineal", fontsize=8.5, color="#2a7", ha="center")
    ax_d.text(2.5, 1.11, "SVPWM/3.arm.", fontsize=7.5, color="#e08e0b", ha="center")
    ax_d.text(2.5, 1.45, "Onda cuadrada", fontsize=8.0, color=BAD, ha="center")
    xd = Vdc / Vf; md = 2.0 * Vf / Vdc
    ax_d.plot([xd], [md], "D", color=ACC, ms=8, zorder=5)
    ax_d.annotate(f"Diseno\nVdc={Vdc:.0f} V\nm={md:.2f}",
                  xy=(xd, md), xytext=(xd + 0.2, md + 0.25),
                  fontsize=8, color=ACC, arrowprops=dict(arrowstyle="->", color=ACC))
    ax_d.set_xlabel("$V_{dc}/\\hat{V}_{f,red}$"); ax_d.set_ylabel("Indice m")
    ax_d.set_title("(d) Mapa de operacion: zonas", fontsize=10)
    ax_d.set_xlim(1.0, 3.0); ax_d.set_ylim(0, 2.0)
    ax_d.legend(fontsize=8, loc="upper right")

    fig.suptitle(
        f"VSC: Vdc={Vdc:.0f} V  fsw={fsw/1e3:.0f} kHz  L1={L1*1e3:.0f} mH  "
        f"Cf={Cf*1e6:.0f} uF  Vll={Vll:.0f} V",
        fontsize=10.5
    )
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    _savefig(fig, "convertidor-vsc-analisis.png")


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
#  vsm-inercia — analisis extendido (4 paneles)
# ===================================================================== #
@figura("vsm-inercia")
def _vsm_extended():
    """4 paneles: (a) respuesta de frecuencia multi-H, (b) lugar autovalores modo potencia,
    (c) contorno zeta(J,D), (d) barras comparativas de H."""
    import matplotlib.gridspec as gridspec
    from scipy.integrate import solve_ivp

    Sn    = 1e6          # VA
    w0    = 2*np.pi*50   # rad/s
    Ks    = 500e3        # W/rad
    DP    = 200e3        # W (escalon de carga)
    mp    = 0.005        # droop 0.5 %
    D_droop = Sn / (mp * w0**2)   # D fijado por droop

    fig = plt.figure(figsize=(12.4, 9.8))
    gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.44, wspace=0.36)
    a1  = fig.add_subplot(gs[0, 0])
    a2  = fig.add_subplot(gs[0, 1])
    a3  = fig.add_subplot(gs[1, 0])
    a4  = fig.add_subplot(gs[1, 1])

    # ------------------------------------------------------------------ #
    # (a) Respuesta de frecuencia: droop puro vs VSM H=1,4,10 s
    # ------------------------------------------------------------------ #
    t_end = 20.0; dt = 1e-3
    t0_step = 1.0
    t_arr  = np.arange(0, t_end, dt)

    def swing_ode(t, state, J, D):
        dw, ddelta = state
        # dw/dt = (Pset - P_elec) / (J*w0) - D*(w-w0)/J
        # P_elec ~ Ks * delta  (linealizado, Pset=P0 antes del escalon)
        # tras escalon: Pset se mantiene, pero P aumenta en DP -> desequilibrio -DP
        omega = w0 + dw
        P_elec = Ks * ddelta        # linealizado alrededor de delta0
        net = -DP / w0 - D * dw    # -DP porque la carga sube
        return [net / J, dw]

    H_vals  = [1, 4, 10]
    colors_H = [ACC2, ACC, "#7b2fbe"]
    df_ss_val = -DP / (D_droop * w0)   # desviacion estacionaria (Hz)

    # droop puro
    f_droop = np.where(t_arr < t0_step, 50.0, 50 + df_ss_val / (2*np.pi))
    a1.plot(t_arr, f_droop, color=BAD, lw=2, ls="--", label="droop puro (sin inercia)")

    for H, col in zip(H_vals, colors_H):
        J = 2 * H * Sn / w0**2
        sol = solve_ivp(swing_ode, [0, t_end], [0.0, 0.0], args=(J, D_droop),
                        t_eval=t_arr, method="RK45", max_step=dt)
        dw_sol = sol.y[0]
        f_sol  = 50 + dw_sol / (2*np.pi)
        # antes del escalon: sin perturbacion
        f_sol[t_arr < t0_step] = 50.0
        a1.plot(t_arr, f_sol, color=col, lw=2, label=f"VSM  H={H} s")
        # marcar nadir
        idx_nadir = np.argmin(f_sol[t_arr >= t0_step]) + np.searchsorted(t_arr, t0_step)
        a1.plot(t_arr[idx_nadir], f_sol[idx_nadir], "v", color=col, ms=7, zorder=5)

    a1.axvline(t0_step, color="#999", ls=":", lw=1)
    a1.text(t0_step + 0.2, 49.985, "escalón ΔP", fontsize=7.5, color="#555")
    f_min_droop = 50 + df_ss_val / (2*np.pi)
    a1.axhline(f_min_droop, color=BAD, ls=":", lw=0.8, alpha=0.6)
    a1.set_xlabel("tiempo [s]"); a1.set_ylabel("f [Hz]")
    a1.set_title("(a) Respuesta de frecuencia ante escalón ΔP=200 kW")
    a1.legend(fontsize=7.5, loc="lower right")
    a1.set_xlim(0, t_end)

    # ------------------------------------------------------------------ #
    # (b) Autovalores del modo de potencia: barrido de J (D=D_droop fijo)
    # ------------------------------------------------------------------ #
    H_sweep = np.linspace(0.3, 12, 300)
    J_sweep = 2 * H_sweep * Sn / w0**2
    # A = [[0,1],[-Ks/J, -D/J]]  -> lambda = (-D/J +/- sqrt((D/J)^2 - 4Ks/J))/2
    alpha = D_droop / J_sweep          # 2*sigma
    disc  = (alpha/2)**2 - Ks / J_sweep
    real_part = -alpha / 2
    # oscilatorio donde disc < 0
    mask_osc  = disc < 0
    mask_real = ~mask_osc

    re_pos_osc = real_part[mask_osc]
    im_osc     = np.sqrt(-disc[mask_osc])
    zeta_osc   = (alpha[mask_osc]/2) / np.sqrt(Ks / J_sweep[mask_osc])

    re_real1 = real_part[mask_real] + np.sqrt(np.maximum(disc[mask_real], 0))
    re_real2 = real_part[mask_real] - np.sqrt(np.maximum(disc[mask_real], 0))

    sc = a2.scatter(re_pos_osc, im_osc, c=H_sweep[mask_osc],
                    cmap="plasma", s=18, zorder=4, label="complejo (oscil.)")
    a2.scatter(re_pos_osc, -im_osc, c=H_sweep[mask_osc], cmap="plasma", s=18, zorder=4)
    a2.scatter(re_real1, np.zeros_like(re_real1), c=H_sweep[mask_real],
               cmap="plasma", s=18, marker="s", label="real (sobreamort.)")
    a2.scatter(re_real2, np.zeros_like(re_real2), c=H_sweep[mask_real],
               cmap="plasma", s=18, marker="s")

    # lineas de zeta
    for zeta_line, ls_ in [(0.7, "--"), (0.5, ":")]:
        ang = np.arccos(zeta_line)
        r_max = max(np.abs(re_pos_osc).max() * 1.2, 1)
        for sign in [1, -1]:
            r_vals = np.linspace(0, r_max, 100)
            a2.plot(-r_vals * zeta_line, sign * r_vals * np.sin(ang),
                    color="#444", ls=ls_, lw=1.2, alpha=0.8)
        a2.text(-r_max * zeta_line * 0.55,
                r_max * np.sin(ang) * 0.6 + (0.15 if zeta_line == 0.7 else 0),
                f"ζ={zeta_line}", fontsize=7.5, color="#333")

    plt.colorbar(sc, ax=a2, label="H [s]", pad=0.02)
    a2.axvline(0, color="#888", lw=0.8)
    a2.axhline(0, color="#888", lw=0.8)
    a2.set_xlabel("Re(λ) [rad/s]"); a2.set_ylabel("Im(λ) [rad/s]")
    a2.set_title("(b) Autovalores modo potencia — barrido H\n(D fijo por droop 0.5 %)")
    a2.legend(fontsize=7, loc="upper left")

    # ------------------------------------------------------------------ #
    # (c) Contorno zeta(J, D) con linea de isodroop
    # ------------------------------------------------------------------ #
    H_g  = np.linspace(0.5, 12, 120)
    D_g  = np.linspace(D_droop * 0.2, D_droop * 3.5, 120)
    JJ   = 2 * H_g[:, None] * Sn / w0**2
    DD   = D_g[None, :]
    # zeta = D/(2*sqrt(J*Ks))  (con Ks/J estimado en frecuencia de oscilacion natural w0_n)
    zeta_grid = DD / (2 * np.sqrt(JJ * Ks))
    ctr = a3.contourf(D_g, H_g, zeta_grid,
                      levels=np.linspace(0, 2.0, 41), cmap="RdYlGn", extend="max")
    plt.colorbar(ctr, ax=a3, label="ζ", pad=0.02)
    a3.contour(D_g, H_g, zeta_grid, levels=[0.5, 0.7, 1.0],
               colors=["#333", "#111", "#000"], linewidths=[1.2, 2.0, 1.2],
               linestyles=[":", "--", "-"])
    a3.axvline(D_droop, color=BAD, lw=2, ls="--", label=f"D$_{{droop}}$ (0.5 %)")
    # anotaciones en lineas de contorno
    a3.text(D_droop * 2.2, H_g[int(0.15*len(H_g))], "ζ=0.5", fontsize=7.5, color="#111")
    a3.text(D_droop * 2.2, H_g[int(0.30*len(H_g))], "ζ=0.7", fontsize=7.5, color="#111")
    a3.text(D_droop * 2.2, H_g[int(0.55*len(H_g))], "ζ=1.0", fontsize=7.5, color="#111")
    a3.set_xlabel("D [N·m·s/rad]"); a3.set_ylabel("H [s]")
    a3.set_title("(c) Contorno ζ(H, D)  —  línea roja: D fijado por droop")
    a3.legend(fontsize=7.5, loc="upper right")

    # ------------------------------------------------------------------ #
    # (d) Comparativa H: barras por tipo de máquina
    # ------------------------------------------------------------------ #
    etiquetas = ["Turboalt.\n(gas/vapor)", "Hidro\ngenerador", "Eólica\n(directa)", "VSM\ntípico", "VSM\nalto H"]
    H_maq     = [5.5, 3.0, 0.5, 4.0, 10.0]
    colores_b = [BAD, OK, "#e08e0b", ACC, "#7b2fbe"]
    bars = a4.barh(etiquetas, H_maq, color=colores_b, edgecolor="white", height=0.55)
    for bar, hval in zip(bars, H_maq):
        a4.text(hval + 0.15, bar.get_y() + bar.get_height()/2,
                f"{hval} s", va="center", fontsize=9)
    a4.set_xlabel("Constante de inercia H [s]")
    a4.set_title("(d) Comparativa de inercia H por tecnología")
    a4.set_xlim(0, 13)
    a4.axvline(2, color="#bbb", lw=0.8, ls=":")
    a4.axvline(10, color="#bbb", lw=0.8, ls=":")

    fig.suptitle("VSM — Análisis extendido: dinámica, autovalores, diseño y comparativa",
                 fontsize=11, fontweight="bold", y=1.01)
    _savefig(fig, "vsm-inercia-analisis.png")


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
#  impedancia-salida-estabilidad (análisis extendido)
# ===================================================================== #
@figura("impedancia-salida-estabilidad")
def _zstab_extended():
    """4 paneles: magnitudes vs SCR, Re{Zqq} vs PLL bw, autovalores en plano
    complejo, margen de fase vs SCR."""
    # --- parámetros base (1 MVA, 690 V, 50 Hz) ---
    Sn = 1e6; Vll = 690.0; f0 = 50.0; w0 = 2*np.pi*f0
    Zb = Vll**2/Sn          # 0.4761 Ω
    L1 = 2e-3; L2 = 0.5e-3; Cf = 15e-6
    Rd = 2.0                 # amortiguamiento activo (proj-01) [Ω]
    # impedancia de la red: Zred(s) = Rg + s*Lg, Lg/Rg => X/R=10, Lg = Zb/(SCR*w0)
    # Admitancia de salida GFL (eje q) simplificada con efecto PLL:
    #   Yqq(s) ≈ (1 + GiCL(s))/(sL1) · Hpll(s)
    #   Aproximamos |Zqq(jw)| del GFL (resultante) como:
    #     Z_qq_re(f) = Re_0*(1 - f^2/fp^2) / (1+(f/fp)^2)
    # con Re_0 derivado de la ganancia de corriente, fp = fPLL.
    # Modelo simplificado pero capaz de mostrar el cambio de signo.

    f = np.logspace(0, 3.1, 800)
    w = 2*np.pi*f

    # (a) |Zred| vs |Zinv| para SCR = 2, 5, 10
    fig, axes = plt.subplots(2, 2, figsize=(11.0, 8.0))
    ax_a, ax_b, ax_c, ax_d = axes[0,0], axes[0,1], axes[1,0], axes[1,1]

    # Admitancia total del GFL con filtro LCL:
    #   Y_inv(s) ≈ 1 / (sL2 + sL1/(1+sCfRd+s²L1Cf))
    # |Z_inv| = 1/|Y_inv|
    s = 1j*w
    Zcf = 1.0/(s*Cf + 1.0/(s*L1))   # Cf en paralelo con L1 (simplficado sin Rd)
    Zinv_vec = np.abs(s*L2 + Zcf)   # |Z_inv| del convertidor
    Zinv_vec = np.clip(Zinv_vec, 0.01, None)

    colors_scr = {2: BAD, 5: ACC, 10: OK}
    for scr, col in colors_scr.items():
        Lg = Zb/(scr*w0)
        Rg = w0*Lg/10.0   # X/R=10
        Zred = np.abs(Rg + 1j*w*Lg)
        ax_a.loglog(f, Zred, color=col, lw=2.0, label=f"$|Z_{{red}}|$ SCR={scr}")
        # cruce
        idx = np.argmin(np.abs(Zred - Zinv_vec))
        ax_a.plot(f[idx], Zinv_vec[idx], "o", color=col, ms=6)

    ax_a.loglog(f, Zinv_vec, color="#555", lw=2.2, ls="--", label="$|Z_{inv}|$ GFL")
    ax_a.set_xlabel("frecuencia [Hz]")
    ax_a.set_ylabel("|Z| [Ω]")
    ax_a.set_title("(a) Cruce de magnitudes vs SCR")
    ax_a.legend(fontsize=8, loc="upper left")

    # (b) Re{Zqq} del GFL para fPLL=50 Hz (lenta) y fPLL=200 Hz (rápida)
    # Modelo: un inversor de corriente con PLL introduce en Zqq:
    #   Z_qq(jw) ≈ Z_LC(jw) / (1 + T_pll(jw))
    # donde T_pll(jw) ≈ (wp/(jw)) · kp_pll
    # Re-planteamiento: usamos la expresión del Harnefors 2016:
    #   Re{Z_qq} = R_eq*(1 - (w/wp)^2) / (1+(w/wp)^2)   [modelo primer orden]
    # con R_eq = L1*wp (resistencia equivalente a la PLL)
    f_plot = np.linspace(1, 400, 2000)
    for fPLL, col, lbl in [(50, OK, "PLL lenta (50 Hz)"), (200, BAD, "PLL rápida (200 Hz)")]:
        wp = 2*np.pi*fPLL
        # Derivado de la linealización: Re{Zqq} cambia de signo en f=fPLL
        # (resultado exacto de la sección §3 de la ficha)
        Req = L1*wp          # coeficiente dimensional
        ReZqq = Req*(1.0 - (f_plot/fPLL)**2) / (1.0 + (f_plot/fPLL)**2)
        ax_b.plot(f_plot, ReZqq, color=col, lw=2.0, label=lbl)
        # marca el cruce por cero
        idx0 = np.argmin(np.abs(ReZqq))
        ax_b.axvline(fPLL, color=col, lw=1.0, ls=":")
        ax_b.text(fPLL+5, 0.6*Req, f"{fPLL} Hz", color=col, fontsize=8)

    ax_b.axhline(0, color="#888", lw=1)
    ax_b.axhspan(ax_b.get_ylim()[0] if ax_b.get_ylim()[0] < 0 else -0.5, 0,
                 color=BAD, alpha=0.06)
    ax_b.set_xlim(0, 400)
    # recompute ylim after plotting
    ymax_b = L1*2*np.pi*200*1.05
    ax_b.set_ylim(-ymax_b, ymax_b)
    ax_b.axhspan(-ymax_b, 0, color=BAD, alpha=0.06)
    ax_b.text(300, -0.4*ymax_b, "Re{$Z_{qq}$}<0\nno pasivo", color=BAD, fontsize=8, ha="center")
    ax_b.set_xlabel("frecuencia [Hz]")
    ax_b.set_ylabel("Re{$Z_{qq}$} [Ω]")
    ax_b.set_title("(b) Parte real de $Z_{qq}$: cruce de signo en $f_{PLL}$")
    ax_b.legend(fontsize=8)

    # (c) Autovalores de L = Zred·Yinv en el plano complejo para SCR=5 (estable) y SCR=2 (inestable)
    # Modelo MIMO 2x2 simplificado:
    # Zred_dq = [[Rg+jwLg, -w0Lg],[w0Lg, Rg+jwLg]]
    # Yinv_dq = [[Ycc, Ycd],[Ydc, Ydd]]
    # Ycc ≈ Ydd ≈ 1/(R_eq + s*L1), Ycd = -Ydc ≈ w0/(R_eq + s*L1) * Tpll/(1+Tpll)
    # Calculamos los autovalores en un rango de frecuencias
    f_nyq = np.linspace(1, 300, 1200)
    w_nyq = 2*np.pi*f_nyq
    fPLL_nom = 50.0; wp_nom = 2*np.pi*fPLL_nom

    for scr, col, lbl, ms in [(5, OK, "SCR=5 (estable)", "o"), (2, BAD, "SCR=2 (inestable)", "s")]:
        Lg = Zb/(scr*w0)
        Rg = w0*Lg/10.0
        lam1_list = []; lam2_list = []
        for wk in w_nyq:
            sk = 1j*wk
            # Zred 2x2
            Zr = np.array([[Rg + sk*Lg, -w0*Lg],
                            [w0*Lg,       Rg + sk*Lg]])
            # Yinv 2x2: diagonal dominante con acoplamiento PLL en off-diagonal
            # Elemento de corriente directa: Y_d = 1/(sk*L1 + Rd)
            Yd = 1.0/(sk*L1 + Rd)
            # La PLL introduce acoplamiento: Yqd ≈ -Yd*(wp/sk)/(1+wp/sk)
            Tpll = wp_nom/sk
            Yqd = -Yd*Tpll/(1.0 + Tpll)
            Ydq = -Yqd
            Yinv = np.array([[Yd, Ydq],
                              [Yqd, Yd]])
            L_mat = Zr @ Yinv
            ev = np.linalg.eigvals(L_mat)
            lam1_list.append(ev[0]); lam2_list.append(ev[1])
        lam1 = np.array(lam1_list); lam2 = np.array(lam2_list)
        for lam, mk in [(lam1, ms), (lam2, "^")]:
            ax_c.plot(lam.real, lam.imag, color=col, lw=0, marker=mk,
                      ms=2.5, alpha=0.6, label=lbl if mk == ms else None)

    ax_c.plot(-1, 0, "x", color="#222", ms=14, mew=2.5, zorder=10, label="−1 (crítico)")
    circ = plt.Circle((-1, 0), 0.15, color="#222", fill=False, lw=1.2, ls="--")
    ax_c.add_patch(circ)
    ax_c.set_xlabel("Re{$\\lambda$}")
    ax_c.set_ylabel("Im{$\\lambda$}")
    ax_c.set_title("(c) Autovalores de $L=Z_{red}Y_{inv}$ en plano complejo")
    ax_c.set_xlim(-2.5, 1.5)
    ax_c.set_ylim(-2.5, 2.5)
    handles_c, labels_c = ax_c.get_legend_handles_labels()
    seen = {}
    for h, l in zip(handles_c, labels_c):
        if l and l not in seen:
            seen[l] = h
    ax_c.legend(seen.values(), seen.keys(), fontsize=8)

    # (d) Margen de fase del minor loop gain vs SCR (monotónico, cruza 0° en SCR_crit≈3.4)
    scr_arr = np.linspace(1.0, 8.0, 120)
    pm_arr = np.zeros(len(scr_arr))
    # Calculamos PM en el cruce de |L(jw)| = 1 a lo largo de todo el rango de frecuencias
    f_sweep = np.logspace(0, 2.8, 600)
    w_sweep = 2*np.pi*f_sweep
    for ki, scr in enumerate(scr_arr):
        Lg = Zb/(scr*w0)
        Rg = w0*Lg/10.0
        Lm_arr = np.zeros(len(f_sweep))
        ph_arr = np.zeros(len(f_sweep))
        for ki2, wk in enumerate(w_sweep):
            sk = 1j*wk
            Zr = np.array([[Rg + sk*Lg, -w0*Lg],
                            [w0*Lg,       Rg + sk*Lg]])
            Yd = 1.0/(sk*L1 + Rd)
            Tpll = wp_nom/sk
            Yqd = -Yd*Tpll/(1.0 + Tpll)
            Ydq = -Yqd
            Yinv = np.array([[Yd, Ydq], [Yqd, Yd]])
            L_mat = Zr @ Yinv
            ev = np.linalg.eigvals(L_mat)
            # autovalor más crítico: más cercano a -1
            idx_ev = np.argmin(np.abs(ev - (-1+0j)))
            lam_crit = ev[idx_ev]
            Lm_arr[ki2] = np.abs(lam_crit)
            ph_arr[ki2] = np.angle(lam_crit, deg=True)
        # cruce de ganancia = 1
        cross = np.where(np.diff(np.sign(Lm_arr - 1.0)))[0]
        if len(cross) > 0:
            # interpolación lineal para el índice de cruce
            ic = cross[-1]
            alpha = (1.0 - Lm_arr[ic])/(Lm_arr[ic+1] - Lm_arr[ic])
            ph_cross = ph_arr[ic] + alpha*(ph_arr[ic+1] - ph_arr[ic])
            pm_arr[ki] = 180.0 + ph_cross
        else:
            # si no cruza, |L|<1 en todo: PM grande (sistema muy estable)
            pm_arr[ki] = 90.0 if np.max(Lm_arr) < 1.0 else -90.0

    ax_d.plot(scr_arr, pm_arr, color=ACC, lw=2.2)
    ax_d.axhline(0, color="#888", lw=1)
    ax_d.axhspan(-60, 0, color=BAD, alpha=0.10)
    ax_d.axhspan(0, 90, color=OK, alpha=0.08)
    # marca SCR crítico (cruce de PM=0)
    cross_scr = np.where(np.diff(np.sign(pm_arr)))[0]
    if len(cross_scr) > 0:
        ic = cross_scr[0]
        alpha = (0.0 - pm_arr[ic])/(pm_arr[ic+1] - pm_arr[ic])
        scr_crit = scr_arr[ic] + alpha*(scr_arr[ic+1] - scr_arr[ic])
        ax_d.axvline(scr_crit, color=BAD, lw=1.5, ls="--")
        ax_d.text(scr_crit+0.1, -30, f"SCR$_{{crit}}$≈{scr_crit:.2f}", color=BAD, fontsize=8)
    ax_d.set_xlabel("SCR")
    ax_d.set_ylabel("Margen de fase [°]")
    ax_d.set_title("(d) Margen de fase del autovalor más crítico vs SCR")
    ax_d.set_xlim(1, 8)
    ax_d.set_ylim(-60, 90)
    ax_d.text(6.0, 60, "ESTABLE", color=OK, fontsize=9)
    ax_d.text(1.5, -40, "INESTABLE", color=BAD, fontsize=9)

    fig.suptitle("Análisis de estabilidad por impedancia — GFL 1 MVA / 690 V / 50 Hz", fontsize=11)
    fig.tight_layout()
    _savefig(fig, "impedancia-salida-estabilidad-analisis.png")


# ===================================================================== #
#  margenes-estabilidad-extended
# ===================================================================== #
@figura("margenes-estabilidad")
def _margenes_extended():
    """4 paneles: (a) Bode con PM/GM/Ms, (b) Nyquist con circulo Ms,
    (c) escalon LC para tres PM, (d) sistema condicionalmente estable."""
    # --- planta principal: L(s) = 500*(s/100+1) / [s*(s/1000+1)*(s/500+1)]
    # equivale a num=[5,500], den=[1e-6, 3e-3, 1, 0]  (wc~1 krad/s)
    num_L  = np.polymul([1/100, 1], [500])          # 500*(s/100+1)
    den_L  = np.polymul([1/1000, 1], [1/500, 1])     # (s/1000+1)(s/500+1)
    den_L  = np.polymul(den_L, [1, 0])               # *s
    sys_L  = signal.TransferFunction(num_L, den_L)

    w = np.logspace(0, 5, 8000)
    _, mag_db, ph_deg = signal.bode(sys_L, w)

    # cruces
    ig = int(np.argmin(np.abs(mag_db)))
    ip = int(np.argmin(np.abs(ph_deg + 180)))
    PM  = 180 + ph_deg[ig]
    GM  = -mag_db[ip]
    wc  = w[ig]; w180 = w[ip]

    # sensibilidad |S| = |1/(1+L)|
    jw = 1j * w
    L_jw = np.polyval(num_L, jw) / np.polyval(den_L, jw)
    S_jw = 1.0 / (1.0 + L_jw)
    S_mag = np.abs(S_jw)
    Ms    = np.max(S_mag)
    # frecuencia del pico de Ms
    i_ms  = int(np.argmax(S_mag))

    fig = plt.figure(figsize=(13.0, 9.5))
    gs  = fig.add_gridspec(2, 2, hspace=0.42, wspace=0.38)
    ax_a1 = fig.add_subplot(gs[0, 0])   # magnitud Bode
    ax_a2 = ax_a1.twinx()               # fase en eje derecho
    ax_b  = fig.add_subplot(gs[0, 1])   # Nyquist
    ax_c  = fig.add_subplot(gs[1, 0])   # escalon tres PM
    ax_d  = fig.add_subplot(gs[1, 1])   # condicional

    # ---- (a) Bode con PM, GM, Ms ----------------------------------------
    ax_a1.semilogx(w, mag_db, color=ACC, lw=2, label="|L| [dB]")
    ax_a1.axhline(0, color="#aaa", lw=0.8)
    ax_a2.semilogx(w, ph_deg, color=ACC2, lw=2, ls="--", label="∠L [°]")
    ax_a2.axhline(-180, color="#aaa", lw=0.8)
    # marcas PM
    ax_a1.axvline(wc, color=OK, ls=":", lw=1.2)
    ax_a2.annotate(f"PM={PM:.0f}°", xy=(wc, ph_deg[ig]),
                   xytext=(wc*1.5, -130), fontsize=8.5, color=OK,
                   arrowprops=dict(arrowstyle="->", color=OK))
    ax_a2.annotate("", xy=(wc, -180), xytext=(wc, ph_deg[ig]),
                   arrowprops=dict(arrowstyle="<->", color=OK, lw=1.5))
    # marcas GM
    ax_a1.axvline(w180, color=BAD, ls=":", lw=1.2)
    ax_a1.annotate(f"GM={GM:.0f} dB", xy=(w180, mag_db[ip]),
                   xytext=(w180*0.18, -18), fontsize=8.5, color=BAD,
                   arrowprops=dict(arrowstyle="->", color=BAD))
    # marca Ms (frecuencia donde |S| es max)
    ax_a1.axvline(w[i_ms], color="#9b59b6", ls=":", lw=1.2)
    ax_a1.annotate(f"Ms={Ms:.2f}", xy=(w[i_ms], mag_db[i_ms]),
                   xytext=(w[i_ms]*3, 12), fontsize=8.5, color="#9b59b6",
                   arrowprops=dict(arrowstyle="->", color="#9b59b6"))
    ax_a1.set_ylabel("|L| [dB]", color=ACC); ax_a1.set_xlabel("ω [rad/s]")
    ax_a2.set_ylabel("∠L [°]", color=ACC2)
    ax_a1.set_title("(a) Bode: PM, GM y Ms simultaneos", fontsize=10)
    # leyenda conjunta
    lines1, labels1 = ax_a1.get_legend_handles_labels()
    lines2, labels2 = ax_a2.get_legend_handles_labels()
    ax_a1.legend(lines1 + lines2, labels1 + labels2, fontsize=8, loc="lower left")

    # ---- (b) Nyquist con circulo Ms ------------------------------------
    L_re = L_jw.real; L_im = L_jw.imag
    ax_b.plot(L_re, L_im, color=ACC, lw=1.8, label="L(jω)")
    ax_b.plot(L_re, -L_im, color=ACC, lw=0.8, ls=":", alpha=0.5)
    ax_b.plot(-1, 0, "x", ms=12, color=BAD, mew=2.5, label="punto −1")
    # circulo de margen de modulo: radio 1/Ms centrado en -1
    r_ms = 1.0 / Ms
    theta = np.linspace(0, 2*np.pi, 300)
    ax_b.plot(-1 + r_ms*np.cos(theta), r_ms*np.sin(theta),
              color="#9b59b6", lw=1.6, ls="--", label=f"circulo Ms (r=1/Ms={r_ms:.2f})")
    # punto mas cercano a -1
    dist = np.abs(L_jw - (-1))
    i_min = int(np.argmin(dist))
    ax_b.plot(L_re[i_min], L_im[i_min], "o", ms=7, color="#9b59b6")
    ax_b.annotate("min dist\n= 1/Ms", xy=(L_re[i_min], L_im[i_min]),
                  xytext=(L_re[i_min]+0.25, L_im[i_min]+0.25), fontsize=8,
                  color="#9b59b6", arrowprops=dict(arrowstyle="->", color="#9b59b6"))
    ax_b.set_xlim(-2.2, 1.5); ax_b.set_ylim(-1.8, 1.8)
    ax_b.axhline(0, color="#aaa", lw=0.8); ax_b.axvline(0, color="#aaa", lw=0.8)
    ax_b.set_xlabel("Re L(jω)"); ax_b.set_ylabel("Im L(jω)")
    ax_b.set_title("(b) Nyquist y circulo de margen de modulo", fontsize=10)
    ax_b.legend(fontsize=8, loc="upper right")
    ax_b.set_aspect("equal", adjustable="datalim")

    # ---- (c) escalon lazo cerrado para PM = 20, 45, 70 ------------------
    wp2 = 2*np.pi*100.0
    pm_configs = [(20, 2.2*wp2, BAD), (45, 1.0*wp2, ACC), (70, 0.45*wp2, OK)]
    for pm_val, K, col in pm_configs:
        num_c = [K]; den_c = [1/wp2, 1, 0]   # L=K/(s*(s/wp2+1))
        _, mg, ph2 = signal.bode(signal.TransferFunction(num_c, den_c), w)
        ic2 = int(np.argmin(np.abs(mg)))
        pm_real = 180 + ph2[ic2]
        # lazo cerrado
        den_cl = np.polyadd(den_c, num_c)
        t_step, y_step = signal.step(signal.TransferFunction(num_c, den_cl))
        # Ms para esta configuracion
        jw2 = 1j * np.linspace(0.1, 1e5, 6000)
        L2 = np.polyval(num_c, jw2) / np.polyval(den_c, jw2)
        ms_val = np.max(np.abs(1/(1+L2)))
        ax_c.plot(t_step*1e3, y_step, color=col, lw=2,
                  label=f"PM≈{pm_real:.0f}°, Ms≈{ms_val:.1f}")
    ax_c.axhline(1, color="#aaa", lw=0.8, ls=":")
    ax_c.set_xlabel("t [ms]"); ax_c.set_ylabel("salida (lazo cerrado)")
    ax_c.set_title("(c) Escalon LC: PM=20°,45°,70°", fontsize=10)
    ax_c.legend(fontsize=8.5, loc="lower right")

    # ---- (d) sistema condicionalmente estable ---------------------------
    # L_cond(s) = K*(s+1)^2 / [s*(s+0.01)^2*(s+100)]
    K_cond = 50.0
    # numerador: K*(s^2+2s+1)
    num_cond = K_cond * np.array([1.0, 2.0, 1.0])
    # denominador: s*(s+0.01)^2*(s+100)
    #   (s+0.01)^2 = s^2+0.02s+0.0001
    d1 = np.polymul([1.0, 0.02, 0.0001], [1.0, 100.0])  # (s^2+0.02s+0.0001)(s+100)
    den_cond = np.polymul([1.0, 0.0], d1)                # *s
    sys_cond = signal.TransferFunction(num_cond, den_cond)
    wc2 = np.logspace(-3, 4, 6000)
    _, mag_c, ph_c = signal.bode(sys_cond, wc2)
    ax_d.semilogx(wc2, mag_c, color=ACC, lw=2)
    ax_d.axhline(0, color="#aaa", lw=0.8)
    # marcar todos los cruces de ganancia
    sign_chg = np.where(np.diff(np.sign(mag_c)))[0]
    for idx in sign_chg:
        w_cross = wc2[idx]
        ph_cross = ph_c[idx]
        pm_cross = 180 + ph_cross
        col_cross = OK if pm_cross > 0 else BAD
        ax_d.axvline(w_cross, color=col_cross, ls=":", lw=1.4)
        ax_d.annotate(f"PM={pm_cross:.0f}°\n(ωc={w_cross:.2g})",
                      xy=(w_cross, 0), xytext=(w_cross*2.5, 20 if pm_cross > 0 else -28),
                      fontsize=7.5, color=col_cross,
                      arrowprops=dict(arrowstyle="->", color=col_cross))
    ax_d.set_ylabel("|L| [dB]"); ax_d.set_xlabel("ω [rad/s]")
    ax_d.set_title("(d) Condicionalmente estable: cruces\nde ganancia superior e inferior", fontsize=10)
    ax_d.set_ylim(-60, 60)

    fig.suptitle("Analisis completo de margenes de estabilidad", fontsize=12, y=1.01)
    _savefig(fig, "margenes-estabilidad-analisis.png")


# ===================================================================== #
#  droop-control-analisis (extended 4-panel)
# ===================================================================== #
@figura("droop-control")
def _droop_extended():
    """4-panel extended droop analysis figure."""
    # System parameters
    w0   = 2*np.pi*50          # rad/s
    Sn1  = 1e6                 # W  (unit 1, 1 MVA)
    Sn2  = 2e6                 # W  (unit 2, 2 MVA)
    droop_pct = 0.005          # 0.5 %
    mp1  = droop_pct * w0 / Sn1   # (rad/s)/W
    mp2  = droop_pct * w0 / Sn2
    Ks   = 500e3               # W/rad  (EV/X at operating point, 690 V line)
    R_line, X_line = 0.1, 0.05  # resistive line X/R=0.5

    fig, axes = plt.subplots(2, 2, figsize=(11.5, 8.5))
    (ax_a, ax_b), (ax_c, ax_d) = axes

    # ---- (a) Load sharing: P-f curves ----
    P_range1 = np.linspace(0, Sn1, 300)
    P_range2 = np.linspace(0, Sn2, 300)
    f1 = (w0 - mp1 * P_range1) / (2*np.pi)
    f2 = (w0 - mp2 * P_range2) / (2*np.pi)
    ax_a.plot(P_range1 / 1e6, f1, color=ACC, lw=2.3,
              label=r"Unidad 1 ($S_{n1}=1\,\mathrm{MW}$)")
    ax_a.plot(P_range2 / 1e6, f2, color=ACC2, lw=2.3,
              label=r"Unidad 2 ($S_{n2}=2\,\mathrm{MW}$)")
    markers = ["o", "s", "^"]
    for Ptotal, mk in zip([0.5e6, 1.0e6, 1.5e6], markers):
        P1eq = Ptotal * Sn1 / (Sn1 + Sn2)
        P2eq = Ptotal * Sn2 / (Sn1 + Sn2)
        feq  = (w0 - mp1 * P1eq) / (2*np.pi)
        ax_a.plot(P1eq/1e6, feq, mk, color=ACC,  ms=9, zorder=5)
        ax_a.plot(P2eq/1e6, feq, mk, color=ACC2, ms=9, zorder=5,
                  label=f"Equilibrio $P_{{tot}}$={Ptotal/1e6:.1f} MW")
        ax_a.axhline(feq, color="#aaa", ls=":", lw=1)
    ax_a.set_xlabel("Potencia [MW]"); ax_a.set_ylabel("Frecuencia [Hz]")
    ax_a.set_title("(a) Reparto proporcional a $S_n$")
    ax_a.legend(fontsize=7.5, loc="upper right")
    ax_a.set_xlim(0, 2.1); ax_a.set_ylim(49.35, 50.1)

    # ---- (b) Dynamic step response for three damping ratios ----
    # Analytical 2nd-order: wn=sqrt(mp*Ks*wf), zeta=wf/(2*wn)
    # => wf_target = (2*zeta)^2 * mp1 * Ks
    t = np.linspace(0, 2.0, 2000)
    dP_step = 0.3e6   # 300 kW step
    configs = [
        (0.15, BAD,  "--", r"$\zeta=0.15$"),
        (0.50, ACC2, "-.", r"$\zeta=0.50$"),
        (0.70, OK,   "-",  r"$\zeta=0.70$"),
    ]
    for zeta_t, col, ls, lbl in configs:
        wf_t = (2*zeta_t)**2 * mp1 * Ks
        wn_t = np.sqrt(mp1 * Ks * wf_t)
        if zeta_t < 1.0:
            wd = wn_t * np.sqrt(1 - zeta_t**2)
            env = np.exp(-zeta_t * wn_t * t)
            Pt  = dP_step * (1 - env * (np.cos(wd*t)
                  + (zeta_t / np.sqrt(1-zeta_t**2)) * np.sin(wd*t)))
        else:
            Pt = dP_step * np.ones_like(t)
        ax_b.plot(t, Pt / 1e3, color=col, ls=ls, lw=2.2, label=lbl)
    ax_b.axhline(dP_step/1e3, color="#aaa", ls=":", lw=1.5, label="$\\Delta P_{ref}$=300 kW")
    ax_b.set_xlabel("Tiempo [s]"); ax_b.set_ylabel("$\\Delta P$ [kW]")
    ax_b.set_title("(b) Respuesta del modo de potencia — escalón 300 kW")
    ax_b.legend(fontsize=9); ax_b.set_xlim(0, 2.0)

    # ---- (c) zeta vs wf for two mp values ----
    wf_arr = np.linspace(0.5, 2*np.pi*40, 500)
    for mp_val, col, lbl in [
        (mp1, ACC,  r"$m_p$ (1 MW, droop 0.5 %)"),
        (mp2, ACC2, r"$m_p$ (2 MW, droop 0.5 %)"),
    ]:
        wn_arr   = np.sqrt(mp_val * Ks * wf_arr)
        zeta_arr = wf_arr / (2 * wn_arr)
        ax_c.plot(wf_arr / (2*np.pi), zeta_arr, color=col, lw=2.2, label=lbl)
    ax_c.axhline(0.70, color=OK,  ls="--", lw=1.8, label=r"$\zeta_{obj}=0.70$")
    ax_c.axhline(0.50, color=BAD, ls=":",  lw=1.5, label=r"$\zeta_{min}=0.50$")
    ax_c.set_xlabel("$f_f = \\omega_f/2\\pi$ [Hz]")
    ax_c.set_ylabel(r"Amortiguamiento $\zeta$")
    ax_c.set_title(r"(c) $\zeta$ vs $\omega_f$ — dos valores de $m_p$")
    ax_c.legend(fontsize=8); ax_c.set_xlim(0, 40); ax_c.set_ylim(0, 1.6)

    # ---- (d) Sharing error with resistive line ----
    delta_arr = np.linspace(0, 0.15, 200)   # rad, power angle perturbation
    V0ph = 690 / np.sqrt(3)                  # phase voltage [V]
    E_ph = 1.02 * V0ph                       # inverter emf
    Z2   = R_line**2 + X_line**2
    dV   = 20.0                              # droop Q action gives this dV [V]
    # Actual P and Q with resistive+inductive line
    P_real  = (R_line * dV * V0ph + X_line * E_ph * V0ph * delta_arr) / Z2 / 1e3
    P_ideal = (X_line * E_ph * V0ph * delta_arr) / X_line / 1e3  # pure X: P=EV/X * delta
    P_ideal = (E_ph * V0ph / X_line) * delta_arr / 1e3
    Q_real  = (X_line * dV * V0ph - R_line * E_ph * V0ph * delta_arr) / Z2 / 1e3
    ax_d.plot(delta_arr, P_real,  color=ACC,  lw=2.2, label="P real (X/R=0.5)")
    ax_d.plot(delta_arr, P_ideal, color=ACC,  lw=2.2, ls="--", label="P idealizada (solo X)")
    ax_d.plot(delta_arr, Q_real,  color=ACC2, lw=2.2, label="Q real")
    ax_d.fill_between(delta_arr, P_ideal, P_real,
                      alpha=0.18, color=BAD, label="Error droop estándar")
    ax_d.axhline(0, color="#aaa", lw=1, ls=":")
    ax_d.set_xlabel(r"Ángulo de potencia $\delta$ [rad]")
    ax_d.set_ylabel("Potencia [kW]")
    ax_d.set_title("(d) Error de reparto — línea resistiva X/R=0.5")
    ax_d.legend(fontsize=8)

    fig.suptitle("Análisis extendido del droop — reparto, dinámica, diseño y robustez",
                 fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _savefig(fig, "droop-control-analisis.png")


# ===================================================================== #
#  diagrama-bode (extended 4-panel)
# ===================================================================== #
@figura("diagrama-bode")
def _bode_extended():
    """4 paneles: (a) 2.o orden, (b) cero RHP vs LHP, (c) Bode LCL, (d) retardo digital."""
    w = np.logspace(1, 5, 3000)
    f = w / (2 * np.pi)

    fig, axes = plt.subplots(4, 2, figsize=(12, 20))
    fig.subplots_adjust(hspace=0.52, wspace=0.35)

    # ------------------------------------------------------------------ #
    # (a) PAR DE POLOS COMPLEJOS CONJUGADOS — magnitud y fase
    # ------------------------------------------------------------------ #
    wn = 2 * np.pi * 2000
    zetas = [0.1, 0.3, 0.5, 0.7]
    colors_z = [ACC, "#e08e0b", "#1a9e5a", "#d62728"]
    ax_a1, ax_a2 = axes[0, 0], axes[0, 1]

    for zeta, col in zip(zetas, colors_z):
        num = wn**2
        den = wn**2 - w**2 + 1j * 2 * zeta * wn * w
        G = num / den
        mag_db = 20 * np.log10(np.abs(G))
        phase_deg = np.degrees(np.angle(G))
        ax_a1.semilogx(f, mag_db, color=col, lw=2, label=f"ζ={zeta}")
        ax_a2.semilogx(f, phase_deg, color=col, lw=2, label=f"ζ={zeta}")
        if zeta < 1 / np.sqrt(2):
            wr = wn * np.sqrt(max(1 - 2 * zeta**2, 0))
            Gr = wn**2 / (wn**2 - wr**2 + 1j * 2 * zeta * wn * wr)
            pk_db = 20 * np.log10(np.abs(Gr))
            ax_a1.plot(wr / (2 * np.pi), pk_db, "o", color=col, ms=6, zorder=5)

    fn = wn / (2 * np.pi)
    ax_a1.axvline(fn, color="#bbb", ls="--", lw=1)
    ax_a2.axvline(fn, color="#bbb", ls="--", lw=1)
    ax_a1.axhline(0, color="#bbb", ls=":", lw=0.8)
    ax_a1.axhline(-3, color="#999", ls=":", lw=0.8)
    w_asy = np.array([wn * 3, wn * 30])
    mag_asy = -40 * np.log10(w_asy / wn)
    ax_a1.semilogx(w_asy / (2 * np.pi), mag_asy, "k--", lw=1.2, label="−40 dB/dec")
    ax_a1.set_ylabel("|G| [dB]"); ax_a1.set_ylim(-50, 30)
    ax_a1.set_title("(a) 2.° orden: pico de resonancia\n$G=\\omega_n^2/(s^2+2\\zeta\\omega_n s+\\omega_n^2)$",
                    fontsize=10)
    ax_a1.legend(fontsize=8, loc="lower left")
    ax_a2.set_ylabel("∠G [°]"); ax_a2.set_ylim(-195, 15)
    ax_a2.set_xlabel("f [Hz]"); ax_a2.set_yticks([0, -45, -90, -135, -180])
    ax_a2.legend(fontsize=8, loc="lower left")
    for ax in (ax_a1, ax_a2):
        ax.set_xlim(f[0], f[-1]); ax.grid(True, which="both", alpha=0.4)

    # ------------------------------------------------------------------ #
    # (b) CERO RHP vs LHP — misma magnitud, distinta fase
    # ------------------------------------------------------------------ #
    z_rhp = 100.0
    p_val = 1000.0
    G_LHP = (1 + 1j * w / z_rhp) / (1 + 1j * w / p_val)
    G_RHP = (1 - 1j * w / z_rhp) / (1 + 1j * w / p_val)
    mag_LHP = 20 * np.log10(np.abs(G_LHP))
    phase_LHP = np.degrees(np.angle(G_LHP))
    phase_RHP = np.degrees(np.angle(G_RHP))
    ax_b1, ax_b2 = axes[1, 0], axes[1, 1]
    ax_b1.semilogx(w, mag_LHP, color=ACC, lw=2.2, label="|G| (idéntico LHP/RHP)")
    ax_b2.semilogx(w, phase_LHP, color=ACC, lw=2.2, label="LHP: +(arctan ω/z)")
    ax_b2.semilogx(w, phase_RHP, color=BAD, lw=2.2, ls="--", label="RHP: −(arctan ω/z)")
    for wc, lbl in ((z_rhp, "$\\omega_z$"), (p_val, "$\\omega_p$")):
        ax_b1.axvline(wc, color="#bbb", ls="--", lw=1)
        ax_b2.axvline(wc, color="#bbb", ls="--", lw=1)
        ax_b2.text(wc * 1.15, -85, lbl, fontsize=8, color="#555")
    ax_b2.fill_between(w, phase_LHP, phase_RHP, alpha=0.18, color=BAD,
                       label="Pérdida PM (RHP)")
    ax_b1.set_ylabel("|G| [dB]")
    ax_b1.set_title("(b) Cero RHP vs LHP\n$(1\\mp s/z)/(1+s/p)$,  z=100, p=1000 rad/s", fontsize=10)
    ax_b1.legend(fontsize=8)
    ax_b2.set_ylabel("∠G [°]"); ax_b2.set_xlabel("ω [rad/s]")
    ax_b2.legend(fontsize=8, loc="lower right")
    for ax in (ax_b1, ax_b2):
        ax.set_xlim(w[0], w[-1]); ax.grid(True, which="both", alpha=0.4)

    # ------------------------------------------------------------------ #
    # (c) BODE DEL LCL (i2/vi) con asíntotas
    # ------------------------------------------------------------------ #
    L1 = 2e-3; L2 = 0.5e-3; Cf = 15e-6; Rd = 0.5
    num_lcl = [Rd * Cf, 1]
    den_lcl = [L1 * L2 * Cf, Rd * Cf * (L1 + L2), (L1 + L2), 0]
    sys_lcl = signal.TransferFunction(num_lcl, den_lcl)
    w_lcl = np.logspace(1, 6, 5000)
    _, mag_lcl, phase_lcl = signal.bode(sys_lcl, w_lcl)
    f_lcl = w_lcl / (2 * np.pi)
    wres = np.sqrt((L1 + L2) / (L1 * L2 * Cf))
    war  = np.sqrt(1 / (L2 * Cf))
    fres = wres / (2 * np.pi)
    far  = war  / (2 * np.pi)
    ax_c1, ax_c2 = axes[2, 0], axes[2, 1]
    ax_c1.semilogx(f_lcl, mag_lcl, color=ACC, lw=2)
    ax_c2.semilogx(f_lcl, phase_lcl, color=ACC, lw=2)
    f_asy_low = np.array([20.0, far * 0.3])
    mag0_low = 20 * np.log10(1 / (2 * np.pi * 20 * (L1 + L2)))
    mag_asy_low = mag0_low - 20 * np.log10(f_asy_low / 20)
    ax_c1.semilogx(f_asy_low, mag_asy_low, "k--", lw=1.4, label="−20 dB/dec")
    f_asy_hi = np.array([fres * 2.5, f_lcl[-1] * 0.5])
    idx_ref = np.argmin(np.abs(f_lcl - fres * 3))
    mag_ref = mag_lcl[idx_ref]
    mag_asy_hi = mag_ref - 60 * np.log10(f_asy_hi / (fres * 3))
    ax_c1.semilogx(f_asy_hi, mag_asy_hi, "k-.", lw=1.4, label="−60 dB/dec")
    for fc, lbl, col in ((far,  f"$f_{{ar}}$={far:.0f} Hz",  "#e08e0b"),
                          (fres, f"$f_{{res}}$={fres:.0f} Hz", BAD)):
        ax_c1.axvline(fc, color=col, ls="--", lw=1.3)
        ax_c2.axvline(fc, color=col, ls="--", lw=1.3)
        ax_c1.text(fc * 1.08, -40, lbl, fontsize=7.5, color=col)
    ax_c1.set_ylabel("|i₂/vᵢ| [dB]"); ax_c1.set_ylim(-120, 30)
    ax_c1.set_title("(c) LCL: $i_2/v_i$\n$L_1=2\\,$mH, $L_2=0.5\\,$mH, $C_f=15\\,\\mu$F, $R_d=0.5\\,\\Omega$",
                    fontsize=10)
    ax_c1.legend(fontsize=8)
    ax_c2.set_ylabel("∠(i₂/vᵢ) [°]"); ax_c2.set_xlabel("f [Hz]")
    ax_c2.set_yticks([-270, -180, -90, 0, 90])
    for ax in (ax_c1, ax_c2):
        ax.set_xlim(f_lcl[0], f_lcl[-1]); ax.grid(True, which="both", alpha=0.4)

    # ------------------------------------------------------------------ #
    # (d) EFECTO DEL RETARDO DIGITAL
    # ------------------------------------------------------------------ #
    wci = 2 * np.pi * 1000
    Ts_values = [50e-6, 100e-6]
    tau_factor = 1.5
    w_d = np.logspace(2, 5, 3000)
    f_d = w_d / (2 * np.pi)
    L_noret = wci / (1j * w_d)
    mag_noret = 20 * np.log10(np.abs(L_noret))
    phase_noret = np.degrees(np.angle(L_noret))
    ax_d1, ax_d2 = axes[3, 0], axes[3, 1]
    ax_d1.semilogx(f_d, mag_noret, color="#555", lw=2, ls="--", label="sin retardo")
    ax_d2.semilogx(f_d, phase_noret, color="#555", lw=2, ls="--", label="sin retardo")
    colors_ts = [ACC, BAD]
    for Ts, col in zip(Ts_values, colors_ts):
        tau = tau_factor * Ts
        phase_ret = phase_noret - np.degrees(w_d * tau)
        lbl = f"$T_s$={int(Ts*1e6)} μs (τ={tau_factor}·$T_s$)"
        ax_d1.semilogx(f_d, mag_noret, color=col, lw=2, label=lbl)
        ax_d2.semilogx(f_d, phase_ret, color=col, lw=2, label=lbl)
        ph_at_cross = -90 - np.degrees(wci * tau)
        pm = 180 + ph_at_cross
        ax_d2.annotate(f"PM={pm:.0f}°",
                       xy=(wci / (2 * np.pi), ph_at_cross),
                       xytext=(wci / (2 * np.pi) * 2.5, ph_at_cross + 25),
                       fontsize=8, color=col,
                       arrowprops=dict(arrowstyle="->", color=col, lw=1))
    ax_d1.axhline(0, color="#bbb", ls=":", lw=0.8)
    ax_d2.axhline(-180, color=BAD, ls=":", lw=0.8, label="−180° (inestable)")
    ax_d2.axvline(wci / (2 * np.pi), color="#bbb", ls="--", lw=1)
    ax_d1.set_ylabel("|L| [dB]")
    ax_d1.set_title("(d) Retardo digital: $e^{-s\\tau}$ degrada PM\n$\\tau=1.5\\,T_s$, cruce a 1 kHz",
                    fontsize=10)
    ax_d1.legend(fontsize=8)
    ax_d2.set_ylabel("∠L [°]"); ax_d2.set_xlabel("f [Hz]")
    ax_d2.set_ylim(-360, 10); ax_d2.set_yticks([0, -90, -180, -270, -360])
    ax_d2.legend(fontsize=8, loc="lower left")
    for ax in (ax_d1, ax_d2):
        ax.set_xlim(f_d[0], f_d[-1]); ax.grid(True, which="both", alpha=0.4)

    fig.suptitle("Diagrama de Bode — análisis avanzado", fontsize=13,
                 fontweight="bold", y=1.002)
    _savefig(fig, "diagrama-bode-analisis.png")


# ===================================================================== #
#  marco-dq (extended: 4 paneles de análisis)
# ===================================================================== #
@figura("marco-dq")
def _marcodq_extended():
    """4 paneles:
    (a) Vector espacio en alfabeta (circulo) + proyeccion dq (punto fijo)
    (b) Acoplamiento cruzado: escalon en vd con y sin desacople
    (c) Sistema desequilibrado 10%: ripple a 100 Hz en id, iq
    (d) Comparacion amplitud invariante vs potencia invariante
    """
    L  = 2e-3           # H
    w0 = 2*np.pi*50     # rad/s
    Vm = 563.0          # V pico de fase

    fig, axes = plt.subplots(2, 2, figsize=(11.0, 8.5))
    (ax_a, ax_b), (ax_c, ax_d) = axes

    # ------------------------------------------------------------------ #
    # (a) Vector espacio en alfabeta trazando circulo + proyeccion dq
    # ------------------------------------------------------------------ #
    t_circ = np.linspace(0, 0.02, 800)
    va = Vm*np.cos(w0*t_circ)
    vb = Vm*np.cos(w0*t_circ - 2*np.pi/3)
    vc = Vm*np.cos(w0*t_circ + 2*np.pi/3)
    val = (2/3)*(va - 0.5*vb - 0.5*vc)
    vbe = (2/3)*(np.sqrt(3)/2)*(vb - vc)
    th_circ = w0*t_circ
    vd_c = val*np.cos(th_circ) + vbe*np.sin(th_circ)
    vq_c = -val*np.sin(th_circ) + vbe*np.cos(th_circ)

    ax_a.plot(val/Vm, vbe/Vm, color=ACC, lw=2.0, label="trayectoria αβ (círculo)")
    vd_ss, vq_ss = float(np.mean(vd_c))/Vm, float(np.mean(vq_c))/Vm
    ax_a.plot(vd_ss, vq_ss, "o", color=BAD, ms=12, zorder=5,
              label=f"punto dq ($v_d$≈{vd_ss:.2f}, $v_q$≈{vq_ss:.2f}) pu")
    ax_a.axhline(0, color="#bbb", lw=0.7); ax_a.axvline(0, color="#bbb", lw=0.7)
    ax_a.annotate("", xy=(1.35, 0), xytext=(0, 0),
                  arrowprops=dict(arrowstyle="-|>", color=BAD, lw=1.8))
    ax_a.annotate("", xy=(0, 1.35), xytext=(0, 0),
                  arrowprops=dict(arrowstyle="-|>", color="#999", lw=1.4))
    ax_a.text(1.38, 0.04, "d", color=BAD, fontsize=9)
    ax_a.text(0.04, 1.38, "q", color="#777", fontsize=9)
    ax_a.set_xlim(-1.5, 1.6); ax_a.set_ylim(-1.5, 1.6)
    ax_a.set_aspect("equal"); ax_a.set_xlabel("α [pu]"); ax_a.set_ylabel("β [pu]")
    ax_a.set_title("(a) Vector espacio en αβ y proyección dq", fontsize=9.5)
    ax_a.legend(fontsize=8, loc="lower right")

    # ------------------------------------------------------------------ #
    # (b) Acoplamiento cruzado: respuesta a escalon en vd
    # ------------------------------------------------------------------ #
    dt = 1e-5; t_max = 0.04
    t_step = np.arange(0, t_max, dt)
    N = len(t_step)
    t_on = int(0.005/dt)
    Vd_in = np.zeros(N); Vd_in[t_on:] = 1.0
    Vq_in = np.zeros(N)

    # Sin desacople
    id_nc = np.zeros(N); iq_nc = np.zeros(N)
    for k in range(1, N):
        did = (Vd_in[k-1] + w0*L*iq_nc[k-1]) / L
        diq = (Vq_in[k-1] - w0*L*id_nc[k-1]) / L
        id_nc[k] = id_nc[k-1] + did*dt
        iq_nc[k] = iq_nc[k-1] + diq*dt

    # Con desacople: planta efectiva diagonal (did/dt = vd/L)
    id_dc = np.zeros(N); iq_dc = np.zeros(N)
    for k in range(1, N):
        id_dc[k] = id_dc[k-1] + Vd_in[k-1]/L * dt
        iq_dc[k] = iq_dc[k-1] + Vq_in[k-1]/L * dt

    t_ms = t_step*1e3
    ax_b.plot(t_ms, id_nc, color=ACC,  lw=2.0, label="$i_d$ sin desacoplo")
    ax_b.plot(t_ms, iq_nc, color=BAD,  lw=2.0, label="$i_q$ sin desacoplo (contaminado)")
    ax_b.plot(t_ms, id_dc, color=ACC,  lw=1.4, ls="--", label="$i_d$ con desacoplo")
    ax_b.plot(t_ms, iq_dc, color=OK,   lw=1.4, ls="--", label="$i_q$ con desacoplo (=0)")
    ax_b.axvline(5, color="#bbb", ls=":", lw=1)
    ax_b.text(5.4, -1.5, "escalón $v_d$", fontsize=8, color="#555")
    ax_b.set_xlabel("t [ms]"); ax_b.set_ylabel("corriente [A]")
    ax_b.set_title("(b) Acoplamiento cruzado: escalón en $v_d$ ($L$=2 mH)", fontsize=9.5)
    ax_b.legend(fontsize=7.5, loc="upper left")
    ax_b.set_xlim(0, t_max*1e3)

    # ------------------------------------------------------------------ #
    # (c) Sistema desequilibrado 10%: ripple a 100 Hz en vd, vq
    # ------------------------------------------------------------------ #
    t2 = np.linspace(0, 0.06, 6000)
    va2 = Vm*np.cos(w0*t2)
    vb2 = Vm*0.90*np.cos(w0*t2 - 2*np.pi/3)
    vc2 = Vm*1.10*np.cos(w0*t2 + 2*np.pi/3)
    val2 = (2/3)*(va2 - 0.5*vb2 - 0.5*vc2)
    vbe2 = (2/3)*(np.sqrt(3)/2)*(vb2 - vc2)
    th2 = w0*t2
    vd2 = val2*np.cos(th2) + vbe2*np.sin(th2)
    vq2 = -val2*np.sin(th2) + vbe2*np.cos(th2)

    ax_c.plot(t2*1e3, vd2/Vm, color=ACC,  lw=1.8, label="$v_d$ (desequilibrio 10%)")
    ax_c.plot(t2*1e3, vq2/Vm, color=BAD,  lw=1.8, label="$v_q$ (ripple a 100 Hz)")
    ax_c.axhline(1.0, color="#aaa", lw=0.8, ls=":")
    ax_c.axhline(0.0, color="#aaa", lw=0.8, ls=":")
    ax_c.annotate("", xy=(30, 0.85), xytext=(20, 0.85),
                  arrowprops=dict(arrowstyle="<->", color="#555", lw=1.2))
    ax_c.text(21, 0.88, "T=10 ms\n(100 Hz)", fontsize=8, color="#555")
    ax_c.set_xlabel("t [ms]"); ax_c.set_ylabel("tensión [pu]")
    ax_c.set_title("(c) Desequilibrio 10%: ripple a 100 Hz en dq", fontsize=9.5)
    ax_c.legend(fontsize=8, loc="upper right")
    ax_c.set_xlim(0, 60)

    # ------------------------------------------------------------------ #
    # (d) Comparacion amplitud invariante vs potencia invariante
    # ------------------------------------------------------------------ #
    t3 = np.linspace(0, 0.02, 2000)
    va3 = Vm*np.cos(w0*t3)
    vb3 = Vm*np.cos(w0*t3 - 2*np.pi/3)
    vc3 = Vm*np.cos(w0*t3 + 2*np.pi/3)
    k_amp = 2/3
    al_amp = k_amp*(va3 - 0.5*vb3 - 0.5*vc3)
    be_amp = k_amp*(np.sqrt(3)/2)*(vb3 - vc3)
    k_pot = np.sqrt(2/3)
    al_pot = k_pot*(va3 - 0.5*vb3 - 0.5*vc3)
    be_pot = k_pot*(np.sqrt(3)/2)*(vb3 - vc3)
    th3 = w0*t3
    vd_amp = al_amp*np.cos(th3) + be_amp*np.sin(th3)
    vd_pot = al_pot*np.cos(th3) + be_pot*np.sin(th3)

    ax_d.plot(t3*1e3, vd_amp/Vm, color=ACC,  lw=2.2,
              label=f"amplitud invariante (k=2/3): $v_d/V_m$={float(np.mean(vd_amp))/Vm:.3f}")
    ax_d.plot(t3*1e3, vd_pot/Vm, color=ACC2, lw=2.2, ls="--",
              label=f"potencia invariante (k=√(2/3)): $v_d/V_m$={float(np.mean(vd_pot))/Vm:.3f}")
    ax_d.axhline(1.0, color=ACC,  lw=0.8, ls=":")
    sqr32 = float(np.sqrt(3/2))
    ax_d.axhline(sqr32, color=ACC2, lw=0.8, ls=":")
    ax_d.text(14.5, 1.01, "1.000 (amplitud)", color=ACC,  fontsize=8)
    ax_d.text(14.5, sqr32+0.01, f"{sqr32:.3f} (potencia)", color=ACC2, fontsize=8)
    ax_d.set_xlabel("t [ms]"); ax_d.set_ylabel("$v_d / V_m$ [pu]")
    ax_d.set_title("(d) Convenciones: misma señal, distintos valores numéricos", fontsize=9.5)
    ax_d.legend(fontsize=7.5, loc="center right")
    ax_d.set_xlim(0, 20); ax_d.set_ylim(0.88, 1.38)

    fig.suptitle(
        "Transformadas de Clarke y Park — análisis extendido\n"
        r"$L=2\,\mathrm{mH}$, $\omega_0=2\pi\cdot50$, $V_m=563\,\mathrm{V}$",
        fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    _savefig(fig, "marco-dq-analisis.png")


# ===================================================================== #
#  analisis-modal-extended (sin decorador; llamado directo desde main)
# ===================================================================== #
def _modal_extended():
    """4 paneles: mapa autovalores, factores de participacion, trayectoria Xvirt, trayectoria Kad."""
    import numpy as np

    # ---------- parametros del sistema GFM simplificado ----------
    L1, L2, Cf = 2e-3, 0.5e-3, 15e-6
    R1 = 0.05
    w0 = 2*np.pi*50
    Sn = 1e6
    mp = 1.571e-3        # pendiente droop de potencia (rad/s/W)
    wf = 2*np.pi*10      # BW filtro de potencia (rad/s)
    EV_X_nom = 500e3     # W/rad  rigidez de sincronizacion nominal

    # frecuencia de resonancia LCL
    Leq = L1*L2/(L1+L2)
    w_lcl = np.sqrt((L1+L2)/(L1*L2*Cf))   # rad/s
    f_lcl = w_lcl/(2*np.pi)

    # ---- modelo linealizado 5 estados: [delta, w, Pm, id, iq] ----
    # parametros
    Ks   = EV_X_nom      # rigidez de sincronizacion  [W/rad]
    D    = 20.0          # damping electrico  [W/(rad/s)]
    H    = 0.5 * Sn      # inercia virtual J*w0 [J·rad/s / ... usamos H=0.5 pu*s]
    wci  = 2*np.pi*900   # BW lazo de corriente (rad/s)
    tau_i = 1/wci

    # A(5x5) ~ [ddelta, dw, dPm, did, diq]
    # fila 0: ddelta/dt = w - w0 ~ w
    # fila 1: dw/dt = (Pm - Ks*delta - D*w) / (H/w0) ... simplificado
    # fila 2: dPm/dt = wf*(P_elec - Pm)  => P_elec ~ Ks*delta (estático)
    # fila 3: did/dt = -wci*id + wci*id_ref   id_ref = 0 (simplificado)
    # fila 4: diq/dt = -wci*iq + wci*iq_ref   iq_ref = 0

    M = H / w0   # inercia  [W·s²/rad]
    A = np.array([
        [ 0,     1,      0,    0,    0],   # ddelta
        [-Ks/M, -D/M,  1/M,   0,    0],   # dw
        [-Ks*wf, 0,   -wf,    0,    0],   # dPm  (Pelec = Ks*delta)
        [ 0,     0,      0, -wci,    0],   # did
        [ 0,     0,      0,    0, -wci],   # diq
    ], dtype=float)

    lam, Phi = np.linalg.eig(A)
    Psi = np.linalg.inv(Phi)

    # ---- identificar modo de potencia (el par con |Im| ~ 2*pi*3.3 Hz) ----
    i_pow = np.argmin(np.abs(np.abs(lam.imag) - 2*np.pi*3.3))
    # ---- identificar modo de corriente (|Im| ~ wci) ----
    i_cur = np.argmin(np.abs(np.abs(lam.imag) - wci))

    # ---- factores de participacion modo de potencia ----
    part_pow = np.abs(Phi[:, i_pow] * Psi[i_pow, :])
    part_pow /= part_pow.sum()

    # ---- (c) trayectoria autovalor potencia al barrer Xvirt (reduce Ks) ----
    Xvirt_vals = np.linspace(0, 0.30, 60)   # pu  (Xvirt se suma a la reactancia)
    # Ks(Xvirt) ~ EV_X_nom / (1 + Xvirt / X0)  con X0 ~ 0.05 pu => X0=EV_X_nom*0.05
    X0_pu = 0.05
    X0_ohm = EV_X_nom  # ya en W/rad (abstraccion)
    traj_pow = []
    for xv in Xvirt_vals:
        Ks_v = EV_X_nom / (1 + xv / X0_pu)
        A_v = A.copy(); A_v[1, 0] = -Ks_v/M; A_v[2, 0] = -Ks_v*wf
        lv = np.linalg.eigvals(A_v)
        # seleccionar el par con Im cercana al modo de potencia
        idx = np.argmin(np.abs(np.abs(lv.imag) - 2*np.pi*3.0))
        traj_pow.append(lv[idx])
    traj_pow = np.array(traj_pow)

    # ---- (d) trayectoria autovalor LCL al barrer Kad ----
    # modelo 3 estados LCL: [iL1, vC, iL2]  con Kad: realimenta vC en la tension de control
    Kad_vals = np.linspace(0, 10, 80)
    traj_lcl = []
    for Kad in Kad_vals:
        A_lcl = np.array([
            [-R1/L1 - Kad/L1,  -1/L1,   0     ],
            [ 1/Cf,             0,      -1/Cf  ],
            [ 0,                1/L2,  -0.1/L2 ],   # R2 parasita=0.1*R1
        ])
        lv = np.linalg.eigvals(A_lcl)
        # seleccionar el par con parte imaginaria mayor (resonancia LCL)
        idx = np.argmax(np.abs(lv.imag))
        traj_lcl.append(lv[idx])
    traj_lcl = np.array(traj_lcl)

    # ---------- figura ----------
    fig, axs = plt.subplots(2, 2, figsize=(10.0, 8.2))
    state_labels = [r"$\delta$", r"$\omega$", r"$P_m$", r"$i_d$", r"$i_q$"]

    # (a) Mapa de autovalores: todos los modos + circulos zeta
    axa = axs[0, 0]
    # circulos zeta constante
    theta = np.linspace(np.pi/2, np.pi, 300)
    r_max = max(wci*1.05, w_lcl*0.15)
    for zeta_c, col_c, ls_c in [(0.1, "#d62728", ":"), (0.3, "#e08e0b", "--"), (0.7, "#1a9e5a", "-.")]:
        for r_c in [2*np.pi*3.3/np.sqrt(1-zeta_c**2), wci/np.sqrt(1-zeta_c**2)]:
            xs = r_c*np.cos(theta); ys = r_c*np.sin(theta)
            axa.plot(xs, ys, color=col_c, lw=0.9, ls=ls_c, alpha=0.55)
            axa.plot(xs, -ys, color=col_c, lw=0.9, ls=ls_c, alpha=0.55)
        if r_c == wci/np.sqrt(1-zeta_c**2):
            axa.annotate(f"ζ={zeta_c}", xy=(r_c*np.cos(np.pi*0.65), r_c*np.sin(np.pi*0.65)),
                         fontsize=7, color=col_c)
    # todos los autovalores
    for k, lk in enumerate(lam):
        axa.scatter(lk.real, lk.imag, marker="x", s=80, lw=2.0,
                    color=BAD if lk.real > -500 else ACC, zorder=4)
    # anotar modo de potencia
    lp = lam[i_pow]
    axa.annotate(f"modo potencia\n{abs(lp.imag)/(2*np.pi):.1f} Hz\nζ={-lp.real/abs(lp):.2f}",
                 xy=(lp.real, lp.imag), xytext=(lp.real - 80, lp.imag + 2*np.pi*2),
                 fontsize=8, arrowprops=dict(arrowstyle="->", color="#444"), color="#222")
    lc = lam[i_cur]
    axa.annotate(f"lazo corriente\n{abs(lc.imag)/(2*np.pi):.0f} Hz\nζ={-lc.real/abs(lc):.2f}",
                 xy=(lc.real, lc.imag), xytext=(lc.real*0.6, lc.imag*0.7),
                 fontsize=8, arrowprops=dict(arrowstyle="->", color="#444"), color="#222")
    axa.axvline(0, color="k", lw=1.2); axa.axhline(0, color="#bbb", lw=0.6)
    axa.set_xlabel("Re(λ) = σ  [1/s]"); axa.set_ylabel("Im(λ) = ωd  [rad/s]")
    axa.set_title("(a) Mapa de autovalores — 5 estados GFM", fontsize=10)
    axa.grid(True, alpha=0.4)

    # (b) Factores de participacion modo de potencia
    axb = axs[0, 1]
    colors_b = [BAD if p > 0.15 else "#aaa" for p in part_pow]
    bars = axb.bar(state_labels, part_pow * 100, color=colors_b)
    axb.set_ylabel("Factor de participación [%]")
    axb.set_title(f"(b) Factores de participación — modo de potencia\n"
                  f"λ = {lam[i_pow].real:.1f} ± j{abs(lam[i_pow].imag):.1f} rad/s", fontsize=10)
    axb.set_ylim(0, 105)
    for bar, p in zip(bars, part_pow):
        if p > 0.05:
            axb.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                     f"{p*100:.1f}%", ha="center", fontsize=8.5, color="#222")
    axb.grid(True, alpha=0.4, axis="y")

    # (c) Trayectoria autovalor de potencia barriendo Xvirt
    axc = axs[1, 0]
    sc_c = axc.scatter(traj_pow.real, traj_pow.imag, c=Xvirt_vals,
                       cmap="RdYlGn", s=18, zorder=3)
    plt.colorbar(sc_c, ax=axc, label="$X_{virt}$ [pu]", pad=0.02)
    axc.scatter(traj_pow[0].real, traj_pow[0].imag, marker="o", s=80, color=BAD,
                zorder=5, label=f"$X_{{virt}}$=0  σ={traj_pow[0].real:.1f}")
    axc.scatter(traj_pow[-1].real, traj_pow[-1].imag, marker="*", s=120, color=OK,
                zorder=5, label=f"$X_{{virt}}$=0.30  σ={traj_pow[-1].real:.1f}")
    axc.axvline(0, color="k", lw=1.2, ls="--", alpha=0.5)
    axc.set_xlabel("Re(λ)  [1/s]"); axc.set_ylabel("Im(λ)  [rad/s]")
    axc.set_title("(c) Trayectoria λ_potencia al barrer $X_{virt}$ (0 → 0.30 pu)", fontsize=10)
    axc.legend(fontsize=8, loc="upper left"); axc.grid(True, alpha=0.4)

    # (d) Trayectoria autovalor LCL barriendo Kad
    axd = axs[1, 1]
    zeta_lcl = -traj_lcl.real / np.abs(traj_lcl)
    sc_d = axd.scatter(traj_lcl.real, traj_lcl.imag, c=Kad_vals,
                       cmap="RdYlGn", s=18, zorder=3)
    plt.colorbar(sc_d, ax=axd, label="$K_{ad}$ [Ω]", pad=0.02)
    axd.scatter(traj_lcl[0].real, traj_lcl[0].imag, marker="o", s=80, color=BAD,
                zorder=5, label=f"$K_{{ad}}$=0  ζ={zeta_lcl[0]:.3f}")
    idx6 = np.argmin(np.abs(Kad_vals - 6))
    axd.scatter(traj_lcl[idx6].real, traj_lcl[idx6].imag, marker="^", s=100, color="#1f6feb",
                zorder=5, label=f"$K_{{ad}}$=6 Ω  ζ={zeta_lcl[idx6]:.2f}")
    axd.scatter(traj_lcl[-1].real, traj_lcl[-1].imag, marker="*", s=120, color=OK,
                zorder=5, label=f"$K_{{ad}}$=10 Ω  ζ={zeta_lcl[-1]:.2f}")
    axd.axvline(0, color="k", lw=1.2, ls="--", alpha=0.5)
    axd.set_xlabel("Re(λ)  [1/s]"); axd.set_ylabel("Im(λ)  [rad/s]")
    axd.set_title("(d) Trayectoria λ_LCL al barrer $K_{ad}$ (0 → 10 Ω)", fontsize=10)
    axd.legend(fontsize=8, loc="upper right"); axd.grid(True, alpha=0.4)

    fig.tight_layout(pad=2.0)
    _savefig(fig, "analisis-modal-analisis.png")


# ===================================================================== #
#  pll-srf (extended: 4 paneles análisis)
# ===================================================================== #
def _pll_extended():
    """4 paneles de análisis para la ficha pll-srf (sin decorador @figura)."""
    from scipy.signal import lti

    V0 = 1.0; w0 = 2*np.pi*50; f0 = 50.0

    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    (ax_a, ax_b), (ax_c, ax_d) = axes
    fig.suptitle("SRF-PLL y DSOGI: análisis completo", fontsize=13, fontweight="bold", color="#222")

    # ---- (a) Respuesta en frecuencia del SOGI para k = 0.5, √2, 2 ----
    f = np.linspace(0.5, 200, 4000); s = 1j*2*np.pi*f
    ks = [0.5, np.sqrt(2), 2.0]; colores_k = [ACC2, ACC, BAD]
    for ki, col in zip(ks, colores_k):
        Hd = ki*w0*s / (s**2 + ki*w0*s + w0**2)
        Hq = ki*w0**2 / (s**2 + ki*w0*s + w0**2)
        lbl = f"k={ki:.2g}"
        ax_a.plot(f, 20*np.log10(np.abs(Hd)), color=col, lw=2, label=f"v'/u ({lbl})")
        ax_a.plot(f, 20*np.log10(np.abs(Hq)), color=col, lw=1.3, ls="--")
    ax_a.axvline(f0, color="#888", ls=":", lw=1.2)
    ax_a.axhline(0, color="#888", ls=":", lw=1)
    ax_a.text(f0+3, -34, "$f_0$=50 Hz", fontsize=8, color="#555")
    ax_a.text(110, -12, "— v'/u\n-- qv'/u", fontsize=8, color="#444")
    ax_a.set_xlim(0, 200); ax_a.set_ylim(-40, 5)
    ax_a.set_xlabel("frecuencia [Hz]"); ax_a.set_ylabel("magnitud [dB]")
    ax_a.set_title("(a) SOGI: v'/u (sólido) y qv'/u (--) para k=0.5, √2, 2")
    ax_a.legend(fontsize=8, loc="lower right")

    # ---- (b) DSOGI: separación de secuencias con desequilibrio 10% ----
    k_s = np.sqrt(2)
    Vp = 1.0; Vm = 0.1; phi_m = 0.2
    dt = 5e-5; t = np.arange(0, 0.08, dt)
    va = Vp*np.cos(w0*t) + Vm*np.cos(-w0*t + phi_m)
    vb = Vp*np.sin(w0*t) + Vm*np.sin(-w0*t + phi_m)

    vpa = np.zeros_like(t); qvpa = np.zeros_like(t)
    vpb = np.zeros_like(t); qvpb = np.zeros_like(t)
    for i in range(1, len(t)):
        e_a = k_s*(va[i-1] - vpa[i-1])*w0
        vpa[i] = vpa[i-1] + (e_a - qvpa[i-1]*w0)*dt
        qvpa[i] = qvpa[i-1] + vpa[i-1]*w0*dt
        e_b = k_s*(vb[i-1] - vpb[i-1])*w0
        vpb[i] = vpb[i-1] + (e_b - qvpb[i-1]*w0)*dt
        qvpb[i] = qvpb[i-1] + vpb[i-1]*w0*dt

    va_pos = 0.5*(vpa - qvpb)
    va_neg = 0.5*(vpa + qvpb)
    t_ms = t*1e3

    ax_b.plot(t_ms, va, color="#aaa", lw=1, label="$v_\\alpha$ (original)", zorder=1)
    ax_b.plot(t_ms, va_pos, color=ACC, lw=2, label="$v^+_\\alpha$ (seq. positiva)", zorder=3)
    ax_b.plot(t_ms, va_neg, color=BAD, lw=1.8, label="$v^-_\\alpha$ (seq. negativa)", zorder=2)
    ax_b.axvline(20, color=OK, ls="--", lw=1.2)
    ax_b.text(21, 0.6, "~20 ms\n(1/k·f₀)", fontsize=7.5, color=OK)
    ax_b.set_xlabel("tiempo [ms]"); ax_b.set_ylabel("tensión [pu]")
    ax_b.set_title("(b) DSOGI: separación de secuencias (V⁺=1, V⁻=0.1)")
    ax_b.legend(fontsize=8); ax_b.set_xlim(0, 80)

    # ---- (c) Respuesta PLL a salto de fase 30° ----
    dphi = np.pi/6
    fns = [10, 30, 80]; zeta = 0.707
    t_c = np.linspace(0, 0.25, 5000)
    colores_c = [OK, ACC, BAD]
    for fn, col in zip(fns, colores_c):
        wn = 2*np.pi*fn
        Ki = wn**2/V0; Kp = 2*zeta*wn/V0
        num = [V0*Kp, V0*Ki]
        den = [1, V0*Kp, V0*Ki]
        sys_lc = lti(num, den)
        _, y_step = sys_lc.step(T=t_c)
        # normalizar al valor final
        y_norm = y_step / (y_step[-1] if y_step[-1] != 0 else 1.0)
        theta_err = dphi * (1 - y_norm)
        ts_ms = int(1000/(zeta*2*np.pi*fn))
        ax_c.plot(t_c*1e3, np.degrees(theta_err), color=col, lw=2,
                  label=f"$f_n$={fn} Hz ($t_s$≈{ts_ms} ms)")
    ax_c.axhline(0, color="#888", ls=":", lw=1)
    ax_c.set_xlabel("tiempo [ms]"); ax_c.set_ylabel("error de ángulo [°]")
    ax_c.set_title("(c) PLL: respuesta a salto de fase 30° (ζ=0.707)")
    ax_c.legend(fontsize=8); ax_c.set_xlim(0, 250)

    # ---- (d) SCR_crit vs f_pll ----
    fpll_v = np.linspace(5, 200, 500)
    # calibrado con fpll=100Hz → SCR_crit≈3.5
    k_scr = 3.5 / (100/50)**2
    scr_curv = k_scr * (fpll_v/f0)**2
    ax_d.plot(fpll_v, scr_curv, color=ACC, lw=2.5, label="SCR$_\\mathrm{crit}$ analítico")
    ax_d.fill_between(fpll_v, scr_curv, 0, color=BAD, alpha=0.15)
    ax_d.fill_between(fpll_v, scr_curv, 12, color=OK, alpha=0.08)
    ax_d.axhline(5, color="#555", ls="--", lw=1.5, label="SCR=5 (red mínima esperada)")
    designs = [(10, "It.0"), (30, "It.1"), (80, "It.2")]
    for fd, lbl in designs:
        scr_d = k_scr*(fd/f0)**2
        ax_d.plot(fd, scr_d, "o", color=BAD, ms=9, zorder=5)
        ax_d.annotate(lbl, (fd, scr_d), textcoords="offset points", xytext=(6, 4), fontsize=8)
    ax_d.set_xlabel("$f_{pll}$ [Hz]"); ax_d.set_ylabel("SCR$_\\mathrm{crit}$")
    ax_d.set_title("(d) SCR crítico vs $f_{pll}$: zona inestable y diseños")
    ax_d.legend(fontsize=8); ax_d.set_xlim(0, 200); ax_d.set_ylim(0, 12)
    ax_d.text(60, 1.5, "INESTABLE", color=BAD, fontsize=9, ha="center", alpha=0.85)
    ax_d.text(60, 9.5, "ESTABLE", color=OK, fontsize=9, ha="center", alpha=0.85)

    fig.tight_layout(rect=(0, 0, 1, 0.95))
    _savefig(fig, "pll-srf-analisis.png")


# ===================================================================== #
#  dinamica-bus-dc  (extended — 4 paneles sin decorador @figura)
# ===================================================================== #
def _busdc_extended():
    """4 paneles: (a) rizado 1φ vs 3φ, (b) hold-up, (c) locus polos vs P, (d) amortiguamiento."""
    # ---------- parametros comunes ----------
    Vdc = 700.0
    P_CPL = 100e3
    Lf = 0.5e-3
    Rf = 0.1
    Cdc = 10e-3
    w0 = 2 * np.pi * 50
    fsw = 10e3

    fig, axes = plt.subplots(2, 2, figsize=(11.0, 8.0))
    axa, axb, axc, axd = axes[0, 0], axes[0, 1], axes[1, 0], axes[1, 1]

    # ------------------------------------------------------------------ #
    # (a) Rizado de tension: monofasico vs trifasico
    # ------------------------------------------------------------------ #
    dt = 2e-6
    t_end = 0.04
    t = np.arange(0, t_end, dt)

    P0 = P_CPL
    # Monofasico: corriente de rizado a 2*w0 absorbe el desbalance
    i_rizado_1ph = P0 * np.cos(2 * w0 * t) / (2 * Vdc)
    vdc_1ph = Vdc + np.cumsum(i_rizado_1ph) * dt / Cdc

    # Trifasico equilibrado: red no aporta rizado; solo conmutacion (alta frecuencia)
    i_pwm_amp = 0.5  # A pico tipico
    i_rizado_3ph = i_pwm_amp * np.sin(2 * np.pi * fsw * t)
    vdc_3ph = Vdc + np.cumsum(i_rizado_3ph) * dt / Cdc

    Delta_1ph = P0 / (w0 * Vdc * Cdc)
    axa.plot(t * 1e3, vdc_1ph, color=BAD, lw=1.5, label="monofásico (2ω = 100 Hz)")
    axa.plot(t * 1e3, vdc_3ph, color=ACC, lw=1.2, label="trifásico (solo PWM, 10 kHz)")
    axa.axhline(Vdc, color="#aaa", ls=":", lw=1)
    axa.annotate(f"$\\Delta V_{{pp}}\\approx{Delta_1ph:.1f}$ V\n(1φ, C=10 mF)",
                 xy=(10, Vdc - Delta_1ph / 2),
                 xytext=(22, Vdc - Delta_1ph * 1.3),
                 fontsize=8,
                 arrowprops=dict(arrowstyle="->", color=BAD, lw=1.0),
                 color=BAD)
    axa.set_xlabel("t [ms]")
    axa.set_ylabel("$V_{dc}$ [V]")
    axa.set_title("(a) Rizado de tensión: 1φ vs 3φ equilibrado\n(P=100 kW, C=10 mF, $V_{dc}$=700 V)", fontsize=9)
    axa.legend(fontsize=8, loc="upper right")
    axa.grid(True, alpha=0.4)

    # ------------------------------------------------------------------ #
    # (b) Hold-up: Vdc(t) tras perdida de Pin para C = 5, 10, 20 mF
    # ------------------------------------------------------------------ #
    t_hu = np.linspace(0, 0.06, 3000)
    Vmin = 665.0
    Pout = P_CPL
    Vdc0 = Vdc

    colors_hu = [BAD, ACC, OK]
    for C_i, col, lbl in zip([5e-3, 10e-3, 20e-3], colors_hu,
                              ["C = 5 mF", "C = 10 mF", "C = 20 mF"]):
        V2 = Vdc0**2 - 2 * Pout * t_hu / C_i
        V2 = np.maximum(V2, 0.0)
        V_t = np.sqrt(V2)
        t_hold = C_i * (Vdc0**2 - Vmin**2) / (2 * Pout) * 1e3
        axb.plot(t_hu * 1e3, V_t, color=col, lw=2, label=f"{lbl}  ($t_h$={t_hold:.1f} ms)")
        idx_cross = np.where(V_t <= Vmin)[0]
        if len(idx_cross):
            axb.plot(t_hu[idx_cross[0]] * 1e3, Vmin, "o", color=col, ms=6)

    axb.axhline(Vmin, color="#888", ls="--", lw=1.4)
    axb.text(1, Vmin + 2, f"$V_{{min}}$ = {Vmin:.0f} V (−5%)", fontsize=8, color="#555")
    axb.set_xlabel("t [ms]")
    axb.set_ylabel("$V_{dc}$ [V]")
    axb.set_title("(b) Hold-up: descarga del bus tras pérdida de $P_{in}$\n($P_{out}$=100 kW, $V_{dc0}$=700 V)", fontsize=9)
    axb.legend(fontsize=8)
    axb.set_ylim(550, 720)
    axb.grid(True, alpha=0.4)

    # ------------------------------------------------------------------ #
    # (c) Locus de autovalores al barrer P de 0 a 200 kW
    # ------------------------------------------------------------------ #
    P_crit = Vdc**2 * Rf * Cdc / Lf
    P_vals = np.linspace(0, 2.0 * P_crit, 80)
    re_all, im_all, p_all = [], [], []

    for P in P_vals:
        A_mat = np.array([
            [-Rf / Lf,  -1.0 / Lf],
            [1.0 / Cdc,  P / (Vdc**2 * Cdc)]
        ])
        for ev in np.linalg.eigvals(A_mat):
            re_all.append(ev.real)
            im_all.append(ev.imag)
            p_all.append(P / 1e3)

    re_all = np.array(re_all)
    im_all = np.array(im_all)
    p_all = np.array(p_all)

    sc = axc.scatter(re_all, im_all, c=p_all, cmap="plasma", s=20)
    fig.colorbar(sc, ax=axc, label="P [kW]", shrink=0.8)
    axc.axvline(0, color=BAD, ls="--", lw=1.4)
    A0 = np.array([[-Rf / Lf, -1.0 / Lf], [1.0 / Cdc, 0.0]])
    ev0 = np.linalg.eigvals(A0)
    axc.plot(ev0.real, ev0.imag, "D", color=OK, ms=7, zorder=5, label="P=0 (natural LC)")
    axc.annotate(f"$P_{{crit}}$={P_crit/1e3:.0f} kW\n(traza A = 0)",
                 xy=(0, np.sqrt(1 / (Lf * Cdc)) * 0.3),
                 xytext=(-400, 500),
                 fontsize=8,
                 arrowprops=dict(arrowstyle="->", color="k", lw=1),
                 bbox=dict(fc="white", ec="#ccc", alpha=0.9))
    axc.set_xlabel("Re(λ)  [1/s]")
    axc.set_ylabel("Im(λ)  [rad/s]")
    axc.set_title(f"(c) Locus de polos vs P (filtro $L_f$-$R_f$-$C_{{dc}}$ con CPL)\n$P_{{crit}}$={P_crit/1e3:.0f} kW", fontsize=9)
    axc.legend(fontsize=8)
    axc.grid(True, alpha=0.4)

    # ------------------------------------------------------------------ #
    # (d) Re{Y_entrada} vs frecuencia: sin amortiguamiento, pasivo, activo
    # ------------------------------------------------------------------ #
    f_vec = np.logspace(0, 4, 800)
    w_vec = 2 * np.pi * f_vec
    G_cpl = -P_CPL / Vdc**2

    def y_bus(w_arr, Rd_p=None, Cd_p=None, G_active=0.0):
        s = 1j * w_arr
        Y_cap = s * Cdc
        Y_source = 1.0 / (Rf + s * Lf)
        Y_damp_p = (0.0 if (Rd_p is None or Cd_p is None)
                    else 1.0 / (Rd_p + 1.0 / (s * Cd_p)))
        return Y_cap + Y_source + G_cpl + G_active + Y_damp_p

    Y_none = y_bus(w_vec)
    Y_pasv = y_bus(w_vec, Rd_p=5.0, Cd_p=100e-6)
    Y_actv = y_bus(w_vec, G_active=1.0 / 5.0)

    axd.semilogx(f_vec, Y_none.real, color=BAD, lw=2, label="sin amortiguamiento")
    axd.semilogx(f_vec, Y_pasv.real, color="#e67e22", lw=2, ls="--",
                 label="pasivo ($R_d$=5 Ω, $C_d$=100 µF)")
    axd.semilogx(f_vec, Y_actv.real, color=ACC, lw=2, label="activo ($R_d$=5 Ω virtual)")
    axd.axhline(0, color="#555", ls=":", lw=1)
    axd.fill_between(f_vec, 0, np.minimum(Y_none.real, 0),
                     color=BAD, alpha=0.12, label="Re{Y}<0 (inestable)")
    axd.set_xlabel("frecuencia [Hz]")
    axd.set_ylabel("Re{$Y_{bus}$}  [S]")
    axd.set_title("(d) Re{$Y_{bus}$}: amortiguamiento pasivo vs activo\nRe{Y}>0 = pasivo = estable", fontsize=9)
    axd.legend(fontsize=8, loc="upper left")
    axd.set_xlim(1, 1e4)
    axd.grid(True, alpha=0.4)

    fig.suptitle("Bus DC — análisis ampliado  ($V_{dc}$=700 V, $P_{CPL}$=100 kW, "
                 "$L_f$=0.5 mH, $R_f$=0.1 Ω, $C_{dc}$=10 mF)",
                 fontsize=10, y=1.01)
    fig.tight_layout(pad=2.0)
    _savefig(fig, "dinamica-bus-dc-analisis.png")


# ===================================================================== #
#  respuesta-segundo-orden  (ampliado)
# ===================================================================== #
def _segundoorden_extended():
    """4 paneles: familia escalon, resonancia frecuencia, efecto cero, diagrama diseno."""
    wn = 10.0
    t = np.linspace(0, 2.0, 1200)
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    axa, axb, axc, axd = axes[0, 0], axes[0, 1], axes[1, 0], axes[1, 1]

    # --- (a) familia de respuestas al escalon ---
    zetas = [(0.1, BAD, "--"), (0.3, ACC2, "--"), (0.5, ACC2, "-"),
             (0.7, ACC, "-"), (1.0, OK, "-"), (2.0, "#888", "-")]
    for z, c, ls in zetas:
        sys_ = signal.TransferFunction([wn**2], [1, 2*z*wn, wn**2])
        tt, y = signal.step(sys_, T=t)
        axa.plot(tt, y, color=c, lw=2, ls=ls, label=f"ζ={z}")
    # marcar tp y ts para z=0.5
    z05 = 0.5
    wd05 = wn * np.sqrt(1 - z05**2)
    tp05 = np.pi / wd05
    sys05 = signal.TransferFunction([wn**2], [1, 2*z05*wn, wn**2])
    _, y05 = signal.step(sys05, T=t)
    tp_idx = np.argmin(np.abs(t - tp05))
    axa.annotate(f"tp={tp05:.2f}s\n(ζ=0.5)", xy=(tp05, y05[tp_idx]),
                 xytext=(tp05 + 0.15, y05[tp_idx] + 0.05),
                 fontsize=8, color=ACC2,
                 arrowprops=dict(arrowstyle="->", color=ACC2, lw=1))
    ts05 = 4 / (z05 * wn)
    axa.axvline(ts05, color=ACC2, ls=":", lw=1.2, alpha=0.7)
    axa.text(ts05 + 0.02, 0.3, f"ts≈{ts05:.2f}s\n(ζ=0.5)", fontsize=8, color=ACC2)
    axa.axhline(1.0, color="#aaa", ls=":", lw=1)
    axa.axhspan(0.98, 1.02, color="#aaa", alpha=0.12, label="banda ±2%")
    axa.set_xlim(0, 2.0); axa.set_ylim(-0.1, 1.7)
    axa.set_xlabel("t [s]"); axa.set_ylabel("y(t)")
    axa.set_title("(a) Familia de escalones según ζ  (ωn=10 rad/s)", fontsize=9)
    axa.legend(fontsize=8, ncol=2, loc="upper right")

    # --- (b) pico de resonancia en frecuencia ---
    w_arr = np.logspace(-1, 1.5, 1200) * wn
    zetas_b = [(0.1, BAD), (0.3, ACC2), (0.5, ACC), (0.707, OK)]
    for z, c in zetas_b:
        _, mag, _ = signal.bode(signal.TransferFunction([wn**2], [1, 2*z*wn, wn**2]), w=w_arr)
        axb.semilogx(w_arr / wn, mag, color=c, lw=2, label=f"ζ={z}")
        if z < 1 / np.sqrt(2):
            wr = wn * np.sqrt(1 - 2 * z**2)
            mag_peak = 1 / (2 * z * np.sqrt(1 - z**2))
            mag_peak_db = 20 * np.log10(mag_peak)
            axb.plot(wr / wn, mag_peak_db, "o", color=c, ms=6)
            axb.annotate(f"{mag_peak_db:.1f}dB", xy=(wr / wn, mag_peak_db),
                         xytext=(wr / wn * 1.15, mag_peak_db + 1.5),
                         fontsize=7, color=c)
    axb.axhline(0, color="#aaa", ls=":", lw=1)
    axb.set_xlabel("ω/ωn"); axb.set_ylabel("|G(jω)| [dB]")
    axb.set_title("(b) Pico de resonancia en frecuencia\nDesaparece para ζ≥1/√2≈0.707", fontsize=9)
    axb.legend(fontsize=8)
    axb.set_xlim(w_arr[0] / wn, w_arr[-1] / wn)

    # --- (c) efecto del cero sobre Mp ---
    t_c = np.linspace(0, 3.0, 1200)
    z_c, wn_c = 0.5, 10.0
    sys_base = signal.TransferFunction([wn_c**2], [1, 2*z_c*wn_c, wn_c**2])
    _, y_base = signal.step(sys_base, T=t_c)
    axc.plot(t_c, y_base, color="#888", lw=2, ls="--", label="sin cero (ref)")
    ratios = [(0.5, BAD), (1.0, ACC2), (2.0, ACC), (5.0, OK)]
    for ratio, c in ratios:
        wz = ratio * wn_c
        # G(s)*(1 + s/wz) = G(s) + (s/wz)*G(s)
        # Numerator of G(s)*(1+s/wz): wn^2*(1 + s/wz) => [wn^2/wz, wn^2]
        num = [wn_c**2 / wz, wn_c**2]
        den = [1, 2*z_c*wn_c, wn_c**2]
        sys_z = signal.TransferFunction(num, den)
        _, y_z = signal.step(sys_z, T=t_c)
        mp = (np.max(y_z) - 1) * 100 if np.max(y_z) > 1 else 0
        axc.plot(t_c, y_z, color=c, lw=2, label=f"ωz/ωn={ratio}  Mp={mp:.0f}%")
    axc.axhline(1.0, color="#aaa", ls=":", lw=1)
    axc.set_xlim(0, 3.0); axc.set_ylim(-0.05, 2.0)
    axc.set_xlabel("t [s]"); axc.set_ylabel("y(t)")
    axc.set_title("(c) Cero adicional amplifica Mp  (ζ=0.5, ωn=10)", fontsize=9)
    axc.legend(fontsize=8)

    # --- (d) diagrama de diseno: iso-Mp e iso-ts ---
    zv = np.linspace(0.3, 1.0, 300)
    wnv = np.linspace(5, 60, 300)
    ZZ, WW = np.meshgrid(zv, wnv)
    MP_grid = np.exp(-np.pi * ZZ / np.sqrt(np.clip(1 - ZZ**2, 1e-6, None))) * 100
    TS_grid = 4 / (ZZ * WW)
    # contornos iso-Mp
    cs_mp = axd.contour(ZZ, WW, MP_grid, levels=[5, 10, 20], colors=[OK, ACC, BAD], linewidths=2)
    axd.clabel(cs_mp, fmt="%g%%", fontsize=8)
    # contornos iso-ts
    cs_ts = axd.contour(ZZ, WW, TS_grid, levels=[0.1, 0.2, 0.5],
                        colors=[OK, ACC, BAD], linewidths=2, linestyles="--")
    axd.clabel(cs_ts, fmt="%.1fs", fontsize=8)
    # region que cumple Mp<10% y ts<0.5s
    region = (MP_grid < 10) & (TS_grid < 0.5)
    axd.contourf(ZZ, WW, region.astype(float), levels=[0.5, 1.5], colors=[ACC], alpha=0.15)
    axd.set_xlabel("ζ"); axd.set_ylabel("ωn [rad/s]")
    axd.set_title("(d) Diseño: iso-Mp (—) e iso-ts (--)\nRegión azul: Mp<10%, ts<0.5s", fontsize=9)
    from matplotlib.lines import Line2D
    leg_handles = [
        Line2D([0], [0], color=OK, lw=2, label="Mp=5% / ts=0.1s"),
        Line2D([0], [0], color=ACC, lw=2, label="Mp=10% / ts=0.2s"),
        Line2D([0], [0], color=BAD, lw=2, label="Mp=20% / ts=0.5s"),
        Line2D([0], [0], color="#aaa", lw=2, ls="--", label="iso-ts (---)"),
    ]
    axd.legend(handles=leg_handles, fontsize=7, loc="upper right")

    fig.suptitle("Respuesta de segundo orden — análisis ampliado  (ωn=10 rad/s salvo panel d)",
                 fontsize=11, y=1.01)
    fig.tight_layout(pad=2.0)
    _savefig(fig, "respuesta-segundo-orden-analisis.png")


# ===================================================================== #
#  desacoplo-dq  (ampliado)
# ===================================================================== #
def _desacoplo_extended():
    """4 paneles: simulacion temporal sin/con desacoplo, rechazo ed, bode MIMO, sensibilidad L."""
    L, R, w0 = 2e-3, 0.05, 2 * np.pi * 50
    ac = 2 * np.pi * 750
    Ts = 100e-6
    Kp = L * ac
    Ki = R * ac
    Id_step = 1000.0
    Ed_step = 100.0

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    axa, axb, axc, axd = axes[0, 0], axes[0, 1], axes[1, 0], axes[1, 1]

    # --- (a) simulacion temporal: sin vs con desacoplo ---
    dt = Ts / 4
    t_sim = np.arange(0, 8e-3, dt)
    # Estado: [id, iq, intd, intq]
    def simulate_dq(with_decoupling, t_arr, Id_ref, Iq_ref=0.0):
        id_, iq_ = 0.0, 0.0
        intd, intq = 0.0, 0.0
        id_arr, iq_arr = [], []
        for ti in t_arr:
            ed, eq = 0.0, 0.0  # red sin perturbacion para panel a
            err_d = Id_ref - id_
            err_q = Iq_ref - iq_
            intd += err_d * dt
            intq += err_q * dt
            vd_pi = Kp * err_d + Ki * intd
            vq_pi = Kp * err_q + Ki * intq
            if with_decoupling:
                vd = vd_pi - w0 * L * iq_ + ed
                vq = vq_pi + w0 * L * id_ + eq
            else:
                vd = vd_pi
                vq = vq_pi
            # Euler planta
            did = (vd - ed + w0 * L * iq_ - R * id_) / L * dt
            diq = (vq - eq - w0 * L * id_ - R * iq_) / L * dt
            id_ += did; iq_ += diq
            id_arr.append(id_); iq_arr.append(iq_)
        return np.array(id_arr), np.array(iq_arr)

    id_nd, iq_nd = simulate_dq(False, t_sim, Id_step)
    id_dc, iq_dc = simulate_dq(True,  t_sim, Id_step)
    t_ms = t_sim * 1e3
    axa.plot(t_ms, id_nd / Id_step, color=ACC, lw=2, label="id sin desacoplo")
    axa.plot(t_ms, id_dc / Id_step, color=OK, lw=2, ls="--", label="id con desacoplo")
    axa.plot(t_ms, iq_nd / Id_step * 100, color=BAD, lw=2, label="iq sin desacoplo (×100 escala)")
    axa.plot(t_ms, iq_dc / Id_step * 100, color="#888", lw=2, ls="--", label="iq con desacoplo (×100 escala)")
    axa.axhline(0, color="#ccc", ls=":", lw=1)
    axa.axhline(1, color="#ccc", ls=":", lw=1)
    axa.set_xlabel("t [ms]"); axa.set_ylabel("corriente normalizada (id/Id*) / (iq/Id*×100)")
    axa.set_title("(a) Escalón id*=1000 A, iq*=0\nSin desacoplo: iq se excursiona; con desacoplo: iq≈0", fontsize=9)
    axa.legend(fontsize=7, loc="center right")

    # --- (b) rechazo de perturbacion de red (feedforward ed) ---
    def simulate_ff(with_ff, t_arr, Id_ref=0.0, ed_step=Ed_step):
        id_, iq_ = 0.0, 0.0
        intd, intq = 0.0, 0.0
        id_arr, ed_arr = [], []
        t_onset = 2e-3
        for ti in t_arr:
            ed = ed_step if ti >= t_onset else 0.0
            eq = 0.0
            err_d = Id_ref - id_
            intd += err_d * dt
            vd_pi = Kp * err_d + Ki * intd
            if with_ff:
                vd = vd_pi - w0 * L * iq_ + ed
            else:
                vd = vd_pi - w0 * L * iq_
            vq = Kp * (0 - iq_) + Ki * intq + w0 * L * id_ + eq
            did = (vd - ed + w0 * L * iq_ - R * id_) / L * dt
            diq = (vq - eq - w0 * L * id_ - R * iq_) / L * dt
            id_ += did; iq_ += diq
            id_arr.append(id_); ed_arr.append(ed)
        return np.array(id_arr), np.array(ed_arr)

    t_b = np.arange(0, 10e-3, dt)
    id_nff, ed_b = simulate_ff(False, t_b)
    id_ff,  _    = simulate_ff(True,  t_b)
    t_b_ms = t_b * 1e3
    axb.plot(t_b_ms, id_nff, color=BAD, lw=2, label="id sin feedforward")
    axb.plot(t_b_ms, id_ff,  color=OK,  lw=2, ls="--", label="id con feedforward")
    axb2 = axb.twinx()
    axb2.plot(t_b_ms, ed_b, color="#888", lw=1.5, ls=":", label="ed (perturbación)")
    axb2.set_ylabel("ed [V]", color="#888"); axb2.tick_params(axis='y', colors="#888")
    axb2.set_ylim(-20, 300)
    axb.set_xlabel("t [ms]"); axb.set_ylabel("id [A]")
    axb.set_title("(b) Perturbación de red Δed=100 V\nFeedforward cancela antes de actuar", fontsize=9)
    lines1, labs1 = axb.get_legend_handles_labels()
    lines2, labs2 = axb2.get_legend_handles_labels()
    axb.legend(lines1 + lines2, labs1 + labs2, fontsize=7, loc="lower right")

    # --- (c) Bode de la planta MIMO ---
    f_arr = np.logspace(1, 4, 1000)
    w_arr = 2 * np.pi * f_arr
    s_arr = 1j * w_arr
    Zdd = np.abs(s_arr * L + R)        # elemento diagonal
    Zdq = np.abs(w0 * L * np.ones_like(w_arr))  # acoplamiento cruzado (constante)
    Zdd_db = 20 * np.log10(Zdd)
    Zdq_db = 20 * np.log10(Zdq)
    axc.semilogx(f_arr, Zdd_db, color=ACC, lw=2, label="|Zdd| = |sL+R|")
    axc.semilogx(f_arr, Zdq_db, color=BAD, lw=2, ls="--", label="|Zdq| = ωL (constante)")
    f_cross = R / (2 * np.pi * L)
    axc.axvline(f_cross, color=OK, ls=":", lw=1.5)
    axc.text(f_cross * 1.2, -15, f"fc=R/L={f_cross:.0f}Hz", fontsize=8, color=OK)
    axc.axvline(ac / (2 * np.pi), color=ACC2, ls=":", lw=1.5)
    axc.text(ac / (2 * np.pi) * 1.1, -5, f"αc={ac/(2*np.pi):.0f}Hz", fontsize=8, color=ACC2)
    axc.set_xlabel("frecuencia [Hz]"); axc.set_ylabel("|Z| [dBΩ]")
    axc.set_title("(c) Planta MIMO 2×2 en dq\n|Zdq|=ωL: acoplamiento constante hasta alta f", fontsize=9)
    axc.legend(fontsize=8)

    # --- (d) sensibilidad a error en L ---
    delta_L = np.linspace(-0.20, 0.20, 200)
    # acoplamiento residual relativo Δiq_max / Id_step = w0*(delta_L*L)*Id_step/Kp / Id_step
    # = w0*L*delta_L / Kp
    diq_rel = np.abs(w0 * L * delta_L / Kp) * 100  # en %
    axd.plot(delta_L * 100, diq_rel, color=BAD, lw=2.5)
    axd.axhline(5, color=ACC, ls="--", lw=1.5, label="límite 5% de acoplamiento")
    axd.axvline(-10, color="#aaa", ls=":", lw=1)
    axd.axvline(+10, color="#aaa", ls=":", lw=1)
    axd.text(10.5, 1.0, "±10% típico", fontsize=8, color="#555")
    v10 = abs(w0 * L * 0.10 / Kp) * 100
    axd.annotate(f"{v10:.1f}% a δL=10%", xy=(10, v10),
                 xytext=(12, v10 + 1.5),
                 fontsize=8, color=BAD,
                 arrowprops=dict(arrowstyle="->", color=BAD, lw=1))
    axd.set_xlabel("error relativo de L  δL [%]")
    axd.set_ylabel("acoplamiento residual ΔIq_max/Id* [%]")
    axd.set_title("(d) Robustez: acoplamiento residual vs error en L\nLineal y pequeño para incertidumbre típica ±10%", fontsize=9)
    axd.legend(fontsize=8)

    fig.suptitle("Desacoplo dq y feedforward — análisis ampliado\n"
                 "(L=2 mH, R=50 mΩ, ω=2π·50, αc=2π·750 Hz, Ts=100 µs)",
                 fontsize=11, y=1.01)
    fig.tight_layout(pad=2.0)
    _savefig(fig, "desacoplo-dq-analisis.png")


# ===================================================================== #
#  funcion-transferencia-analisis  (sin decorador @figura)
# ===================================================================== #
def _ft_extended():
    """4 paneles: (a) impulso+escalon 2o orden, (b) cancelacion polo-cero,
    (c) Bode G_LCL algebraico vs numerico, (d) tabla antitransformadas."""
    from scipy.signal import TransferFunction, impulse, step, bode as sig_bode

    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.0))
    (a1, a2), (a3, a4) = axes

    # ---- (a) Respuesta al impulso y escalon ----
    wn = 10.0
    t = np.linspace(0, 1.5, 800)
    colors_z = [(0.3, ACC, "ζ=0.3"),
                (0.7, ACC2, "ζ=0.7"),
                (1.5, OK,  "ζ=1.5")]
    a1.set_title("(a) Impulso y escalón: G(s) = ωn²/(s²+2ζωns+ωn²), ωn=10")
    for z, c, lbl in colors_z:
        sys_z = TransferFunction([wn**2], [1, 2*z*wn, wn**2])
        ti, yi = impulse(sys_z, T=t)
        ts, ys = step(sys_z, T=t)
        a1.plot(ti, yi, color=c, lw=2.0, label=f"impulso {lbl}")
        a1.plot(ts, ys, color=c, lw=1.4, ls="--")
    a1.axhline(0, color="#bbb", lw=0.8)
    a1.axhline(1.0, color="#bbb", lw=0.8, ls=":")
    a1.set_xlabel("t [s]"); a1.set_ylabel("y(t)")
    a1.legend(fontsize=8, loc="upper right")
    a1.text(1.25, 8.0, "— impulso\n-- escalón", fontsize=8, color="#555")
    a1.set_ylim(-4, 12)

    # ---- (b) Cancelacion polo-cero: modo oculto ----
    a_z, b_z, K_pc = 5.0, 2.0, 10.0
    sys_full = TransferFunction([K_pc, K_pc*a_z], [1, (a_z+b_z), a_z*b_z])
    sys_red  = TransferFunction([K_pc], [1, b_z])
    a_pert   = a_z * 1.20
    sys_pert = TransferFunction([K_pc, K_pc*a_z], [1, (a_pert+b_z), a_pert*b_z])
    t2 = np.linspace(0, 2.5, 800)
    ti_f, yi_f = impulse(sys_full, T=t2)
    ti_r, yi_r = impulse(sys_red,  T=t2)
    ti_p, yi_p = impulse(sys_pert, T=t2)
    a2.plot(ti_f, yi_f, color=ACC, lw=2.2, label="G completa (cancelación exacta)")
    a2.plot(ti_r, yi_r, color=OK,  lw=1.8, ls="--", label="G reducida K/(s+b)")
    a2.plot(ti_p, yi_p, color=BAD, lw=1.8, ls=":",  label="G pert (polo +20%)")
    a2.axhline(0, color="#bbb", lw=0.8)
    a2.set_title(f"(b) Cancelación polo-cero: modo oculto\nG=K(s+{a_z})/[(s+{a_z})(s+{b_z})], K={K_pc}")
    a2.set_xlabel("t [s]"); a2.set_ylabel("g(t) impulso")
    a2.legend(fontsize=8); a2.set_ylim(-2, 12)

    # ---- (c) Bode G_LCL algebraico vs numerico ----
    L1, L2, Cf, R1, Rd = 2e-3, 0.5e-3, 15e-6, 0.05, 3.0
    den_c = np.array([L1*L2*Cf,
                      R1*L2*Cf + Rd*(L1+L2)*Cf,
                      L1 + L2 + R1*Rd*Cf,
                      R1])
    sys_lcl = TransferFunction([1.0], den_c)
    w = np.logspace(1, 5, 2000)
    w_b, mag_b, _ = sig_bode(sys_lcl, w=w)
    s_jw = 1j*w
    Hjw  = 1.0 / (den_c[0]*s_jw**3 + den_c[1]*s_jw**2 + den_c[2]*s_jw + den_c[3])
    mag_n = 20*np.log10(np.abs(Hjw))
    f_hz = w/(2*np.pi)
    a3.semilogx(f_hz, mag_b, color=ACC, lw=2.5, label="algebraico (scipy)")
    a3.semilogx(f_hz, mag_n, color=BAD, lw=1.4, ls="--", label="numérico directo")
    a3.set_title(f"(c) Bode G_LCL(s): algebraico vs numérico\nL1={L1*1e3}mH L2={L2*1e3}mH Cf={Cf*1e6}µF Rd={Rd}Ω")
    a3.set_xlabel("f [Hz]"); a3.set_ylabel("|G| [dB]")
    a3.legend(fontsize=8)
    f_res = np.sqrt((L1+L2)/(L1*L2*Cf))/(2*np.pi)
    a3.axvline(f_res, color="#999", ls=":", lw=1.2)
    a3.text(f_res*1.12, -10, f"f_res≈{f_res:.0f}Hz", fontsize=8, color="#555")

    # ---- (d) Tabla de antitransformadas ----
    a4.axis("off")
    a4.set_title("(d) Pares transformada de Laplace ↔ tiempo", pad=10)
    rows = [
        ["F(s)", "f(t)", "Notas"],
        ["1", "δ(t)", "impulso unitario"],
        ["1/s", "1(t)", "escalón unitario"],
        ["1/s²", "t·1(t)", "rampa"],
        ["1/(s+a)", "e^{−at}", "polo real, τ=1/a"],
        ["ωn²/(s²+2ζωns+ωn²)", "resp. 2º orden", "par complejo conj."],
        ["ω/(s²+ω²)", "sin(ωt)", "seno puro (Re=0)"],
        ["s/(s²+ω²)", "cos(ωt)", "coseno puro"],
        ["1/[s(s+a)]", "(1−e^{−at})/a", "escalón → 1er orden"],
    ]
    x_cols = [0.02, 0.36, 0.68]
    y0, dy = 0.93, 0.10
    for i, row in enumerate(rows):
        y = y0 - i*dy
        bg = "#d0e8ff" if i == 0 else ("#f0f0f0" if i % 2 == 0 else "white")
        a4.add_patch(plt.Rectangle((0.0, y-0.086), 1.0, dy,
                                   transform=a4.transAxes, color=bg, zorder=0))
        for cell, xc in zip(row, x_cols):
            fw = "bold" if i == 0 else "normal"
            a4.text(xc, y-0.04, cell, transform=a4.transAxes,
                    fontsize=8.5, fontweight=fw, va="center", ha="left")

    fig.suptitle("Función de transferencia — análisis avanzado", fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _savefig(fig, "funcion-transferencia-analisis.png")


# ===================================================================== #
#  polos-ceros-analisis  (sin decorador @figura)
# ===================================================================== #
def _polosceros_extended():
    """4 paneles: (a) lugar de raices, (b) respuesta inversa RHP,
    (c) funcion sensibilidad |S|, (d) mapa polos proyecto-01."""
    from scipy.signal import TransferFunction, step as sig_step, bode as sig_bode

    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.0))
    (a1, a2), (a3, a4) = axes

    # ---- (a) Lugar de raices G=K/[s(s+2)(s+4)] ----
    Ks_vec   = np.linspace(0, 60, 3000)
    den_rl   = np.array([1.0, 6.0, 8.0, 0.0])
    roots_rl = []
    for K in Ks_vec:
        c2 = den_rl.copy(); c2[-1] += K
        roots_rl.append(np.roots(c2))
    roots_rl = np.array(roots_rl)
    for i in range(3):
        a1.plot(roots_rl[:, i].real, roots_rl[:, i].imag, color=ACC, lw=1.5, alpha=0.8)
    p_oa = np.roots(den_rl)
    a1.scatter(p_oa.real, p_oa.imag, marker="x", s=110, color=BAD, lw=2.5, zorder=5,
               label="polos G (K=0)")
    centroid = -6/3
    for k in range(3):
        ang = np.deg2rad((2*k+1)*60)
        r_a = np.linspace(0, 8, 100)
        a1.plot(centroid + r_a*np.cos(ang), r_a*np.sin(ang), color="#aaa", ls="--", lw=1.0)
    best_K, best_root = None, None
    for idx, K in enumerate(Ks_vec):
        for r in roots_rl[idx]:
            if r.real < -0.01 and abs(r.imag) > 0.05:
                zeta_r = -r.real / abs(r)
                if abs(zeta_r - 0.7) < 0.015:
                    best_K = K; best_root = r; break
        if best_K is not None: break
    if best_root is not None:
        a1.scatter([best_root.real, best_root.real],
                   [best_root.imag, -best_root.imag],
                   marker="*", s=200, color=OK, zorder=6,
                   label=f"ζ≈0.7 → K≈{best_K:.1f}")
    a1.axvline(0, color="k", lw=1.2); a1.axhline(0, color="#bbb", lw=0.6)
    a1.set_xlim(-8, 2); a1.set_ylim(-7, 7)
    a1.set_xlabel("Re(s)"); a1.set_ylabel("Im(s)")
    a1.set_title("(a) Lugar de raíces: G = K/[s(s+2)(s+4)]\nasíntotas 60°/180°/300°, centroide s=−2")
    a1.legend(fontsize=8); a1.grid(True, alpha=0.3)

    # ---- (b) Respuesta inversa cero RHP ----
    z_rhp, K_rh, a_rh = 5.0, 5.0, 2.0
    sys_rhp = TransferFunction([-K_rh/z_rhp, K_rh], [1, a_rh])
    sys_mp  = TransferFunction([ K_rh/z_rhp, K_rh], [1, a_rh])
    t_rh = np.linspace(0, 3.0, 800)
    ts_rhp, ys_rhp = sig_step(sys_rhp, T=t_rh)
    ts_mp,  ys_mp  = sig_step(sys_mp,  T=t_rh)
    a2.plot(ts_rhp, ys_rhp, color=BAD, lw=2.2,
            label=f"G_RHP: K(1−s/{z_rhp})/(s+{a_rh})")
    a2.plot(ts_mp,  ys_mp,  color=OK,  lw=2.0, ls="--",
            label=f"G_MP:  K(1+s/{z_rhp})/(s+{a_rh})")
    a2.axhline(0, color="#bbb", lw=0.8)
    a2.annotate("respuesta\ninversa inicial", xy=(0.15, -0.12),
                xytext=(0.7, -0.9), fontsize=8, color=BAD,
                arrowprops=dict(arrowstyle="->", color=BAD, lw=1.5))
    a2.set_title(f"(b) Cero RHP → respuesta inversa inicial\nz=+{z_rhp}, K={K_rh}, polo s=−{a_rh}")
    a2.set_xlabel("t [s]"); a2.set_ylabel("y(t) escalón")
    a2.legend(fontsize=8); a2.set_ylim(-1.5, 3.5)

    # ---- (c) Funcion de sensibilidad |S(jw)| ----
    wc_s = 3.0
    wi_s = wc_s * np.tan(np.deg2rad(30))
    jw_c = 1j*wc_s
    Kp_s = abs(jw_c*(jw_c+1)) / abs(jw_c + wi_s)
    w_s  = np.logspace(-2, 2, 2000)
    jw   = 1j*w_s
    L_jw = Kp_s * (jw + wi_s) / (jw * (jw + 1))
    S_jw = 1.0 / (1.0 + L_jw)
    S_dB = 20*np.log10(np.abs(S_jw))
    a3.semilogx(w_s, S_dB, color=ACC, lw=2.2,
                label=f"|S(jω)|  PM≈60°, ωc={wc_s} rad/s")
    a3.axhline(0, color="#bbb", lw=1.0, ls=":")
    a3.axhline(6, color=BAD,   lw=1.2, ls="--", label="Ms = 6 dB (límite)")
    a3.axhspan(-30, 0, alpha=0.07, color=OK)
    a3.axhspan(0,  20, alpha=0.06, color=BAD)
    Ms_dB = np.max(S_dB)
    wMs   = w_s[np.argmax(S_dB)]
    a3.scatter([wMs], [Ms_dB], color=BAD, s=80, zorder=5)
    a3.text(wMs*1.4, Ms_dB+0.5, f"Ms={Ms_dB:.1f}dB", fontsize=8, color=BAD)
    a3.text(0.03, -20, "atenuación de\nperturbaciones\n|S|<0 dB", fontsize=8, color="#1a9e5a")
    a3.set_xlabel("ω [rad/s]"); a3.set_ylabel("|S| [dB]")
    a3.set_title("(c) Función de sensibilidad |S(jω)|\nintegral de Bode: ganancia aquí ↔ pago allá")
    a3.legend(fontsize=8); a3.set_ylim(-30, 20)

    # ---- (d) Mapa de polos proyecto-01 ----
    poles_before = np.array([3.5+18j,  3.5-18j,  -15+0j])
    poles_after  = np.array([-8.3+21j, -8.3-21j, -22+0j])
    n_traj = 50
    for i in range(len(poles_before)):
        traj = np.linspace(poles_before[i], poles_after[i], n_traj)
        a4.plot(traj.real, traj.imag, color="#aaa", lw=1.2, alpha=0.7)
        mid = n_traj//2
        a4.annotate("", xy=(traj[mid+1].real, traj[mid+1].imag),
                    xytext=(traj[mid].real, traj[mid].imag),
                    arrowprops=dict(arrowstyle="->", color="#888", lw=1.2))
    a4.scatter(poles_before.real, poles_before.imag,
               marker="x", s=130, color=BAD, lw=2.5, zorder=5, label="Antes (SPD, inestable)")
    a4.scatter(poles_after.real, poles_after.imag,
               marker="x", s=130, color=OK,  lw=2.5, zorder=5, label="Después: ζ=0.37, f=3.3 Hz")
    a4.axvline(0, color="k", lw=1.5)
    a4.axhline(0, color="#bbb", lw=0.6)
    a4.axvspan(-40, 0,  color=OK,  alpha=0.06)
    a4.axvspan(  0, 15, color=BAD, alpha=0.06)
    a4.text(-35, 27, "SPI\n(estable)", fontsize=9, color="#1a9e5a", fontweight="bold")
    a4.text(  5, 27, "SPD\n(inest.)", fontsize=9, color="#d62728", fontweight="bold")
    a4.annotate("Xvirt ↑ + wf ↓", xy=(-8.3, 21), xytext=(3, 26),
                fontsize=8, color="#555",
                arrowprops=dict(arrowstyle="->", color="#555"))
    a4.set_xlim(-40, 15); a4.set_ylim(-30, 32)
    a4.set_xlabel("Re(λ) [rad/s]"); a4.set_ylabel("Im(λ) [rad/s]")
    a4.set_title("(d) Mapa de polos Proyecto-01 (GFM)\nmodo de potencia: inestable → estable")
    a4.legend(fontsize=8); a4.grid(True, alpha=0.3)

    fig.suptitle("Polos y ceros — análisis avanzado", fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _savefig(fig, "polos-ceros-analisis.png")


# ===================================================================== #
#  resonancia-rlc (ampliado)
# ===================================================================== #
def _rlc_extended():
    """4 paneles: (a) serie vs paralelo |Z|, (b) Rd en Bode LCL, (c) fres/far vs L_red, (d) activo vs pasivo."""
    L1, L2, Cf = 2e-3, 0.5e-3, 15e-6
    R1 = 50e-3
    Rd_opt = 0.183
    Kad = 6.0
    Ts = 100e-6

    Leq = L1 * L2 / (L1 + L2)
    fres0 = 1.0 / (2 * np.pi * np.sqrt(Leq * Cf))

    f = np.logspace(1.5, 4.3, 1500)
    w = 2 * np.pi * f

    fig, axes = plt.subplots(2, 2, figsize=(11.0, 8.0))
    axa, axb, axc, axd = axes[0, 0], axes[0, 1], axes[1, 0], axes[1, 1]

    # (a) |Z| serie vs paralelo
    Ls, Cs, Rs, Rp = 2e-3, 20e-6, 10.0, 1000.0
    f0_lc = 1 / (2 * np.pi * np.sqrt(Ls * Cs))
    Z_serie = np.abs(Rs + 1j * w * Ls + 1 / (1j * w * Cs))
    Y_par = 1 / Rp + 1j * w * Cs + 1 / (1j * w * Ls)
    Z_par_z = np.abs(1.0 / Y_par)
    axa.loglog(f, Z_serie, color=ACC, lw=2, label=f"Serie (R={Rs} Ω serie)")
    axa.loglog(f, Z_par_z, color=BAD, lw=2, label=f"Paralelo (R={Rp} Ω paralelo)")
    axa.axvline(f0_lc, color="#888", ls="--", lw=1)
    axa.annotate(f"$f_0$≈{f0_lc:.0f} Hz", xy=(f0_lc, 15), xytext=(f0_lc * 1.5, 4),
                 fontsize=8.5, color="#555", arrowprops=dict(arrowstyle="->", color="#888", lw=0.8))
    axa.set_xlabel("frecuencia [Hz]"); axa.set_ylabel("|Z| [Ω]")
    axa.set_title("(a) Serie vs paralelo: |Z(f)|\nSerie→mínimo en $f_0$; Paralelo→máximo en $f_0$", fontsize=9)
    axa.legend(fontsize=8.5); axa.grid(True, which="both", alpha=0.4)

    # (b) Bode iL2/vi del LCL con Rd en serie con Cf
    def H_lcl_rd(w_arr, Rd):
        s = 1j * w_arr
        Zshunt = Rd + 1 / (s * Cf)
        Zp2 = Zshunt * (s * L2) / (Zshunt + s * L2)
        return np.abs(Zp2 / ((R1 + s * L1 + Zp2) * s * L2))

    for Rd, col, lbl in [(0.0, BAD, "Rd=0 (sin amort.)"),
                         (0.05, "#e67e22", "Rd=0.05 Ω"),
                         (Rd_opt, OK, f"Rd={Rd_opt} Ω (óptimo)"),
                         (1.0, ACC2, "Rd=1 Ω (sobredamp.)")]:
        H_v = H_lcl_rd(w, Rd)
        axb.semilogx(f, 20 * np.log10(np.where(H_v > 1e-10, H_v, 1e-10)), color=col, lw=2, label=lbl)
    axb.axvline(fres0, color="#888", ls="--", lw=1)
    axb.axhline(0, color="#555", ls=":", lw=0.8)
    axb.annotate(f"$f_{{res}}$≈{fres0:.0f} Hz", xy=(fres0, -10),
                 xytext=(fres0 * 1.5, -22), fontsize=8.5, color="#555",
                 arrowprops=dict(arrowstyle="->", color="#888", lw=0.8))
    axb.set_xlabel("frecuencia [Hz]"); axb.set_ylabel("|$i_{L2}/v_i$| [dB·S]")
    axb.set_title("(b) Amortiguamiento pasivo: $R_d$ en serie con $C_f$\nAplana el pico sin atenuar la fundamental", fontsize=9)
    axb.legend(fontsize=8, loc="lower left"); axb.set_ylim(-80, 30)
    axb.grid(True, which="both", alpha=0.4)

    # (c) fres y far vs L_red
    Lred_v = np.linspace(0, 5e-3, 200)
    fres_a, far_a = np.zeros(200), np.zeros(200)
    for i, Lr in enumerate(Lred_v):
        L2e = L2 + Lr
        fres_a[i] = 1 / (2 * np.pi * np.sqrt(L1 * L2e / (L1 + L2e) * Cf))
        far_a[i] = 1 / (2 * np.pi * np.sqrt(L2e * Cf))
    axc.plot(Lred_v * 1e3, fres_a, color=ACC, lw=2, label="$f_{res}$")
    axc.plot(Lred_v * 1e3, far_a, color=BAD, lw=2, ls="--", label="$f_{ar}$ (antirresonancia)")
    axc.fill_between(Lred_v * 1e3, far_a, fres_a, alpha=0.12, color=ACC)
    axc.set_xlabel("$L_{red}$ [mH]"); axc.set_ylabel("frecuencia [Hz]")
    axc.set_title("(c) Efecto de $L_{red}$ en $f_{res}$ y $f_{ar}$\nEn red débil las dos frecuencias se acercan", fontsize=9)
    axc.legend(fontsize=8.5); axc.grid(True, alpha=0.4)

    # (d) Activo vs pasivo
    def H_activo(w_arr, Kad_v):
        s = 1j * w_arr
        Zsh = Kad_v * np.exp(-1.5 * Ts * s) + 1 / (s * Cf)
        Zp2 = Zsh * (s * L2) / (Zsh + s * L2)
        return np.abs(Zp2 / ((R1 + s * L1 + Zp2) * s * L2))

    for H_fn, col, lbl in [(lambda w_a=w: H_lcl_rd(w_a, 0.0), BAD, "Sin amortiguamiento"),
                            (lambda w_a=w: H_lcl_rd(w_a, Rd_opt), OK, f"Pasivo Rd={Rd_opt} Ω"),
                            (lambda w_a=w: H_activo(w_a, Kad), ACC, f"Activo Kad={Kad} Ω")]:
        H_v = H_fn()
        axd.semilogx(f, 20 * np.log10(np.where(H_v > 1e-10, H_v, 1e-10)), color=col, lw=2, label=lbl)
    axd.axvline(fres0, color="#888", ls="--", lw=1)
    axd.axhline(0, color="#555", ls=":", lw=0.8)
    axd.set_xlabel("frecuencia [Hz]"); axd.set_ylabel("|$i_{L2}/v_i$| [dB·S]")
    axd.set_title("(d) Activo vs pasivo: equivalencia aproximada\nKad=6 Ω ≈ Rd_opt con retardo digital", fontsize=9)
    axd.legend(fontsize=8.5, loc="lower left"); axd.set_ylim(-80, 30)
    axd.grid(True, which="both", alpha=0.4)

    fig.suptitle("Resonancia RLC — análisis ampliado  ($L_1$=2 mH, $L_2$=0.5 mH, $C_f$=15 µF, $R_1$=50 mΩ)",
                 fontsize=10, y=1.01)
    fig.tight_layout(pad=2.0)
    _savefig(fig, "resonancia-rlc-analisis.png")


# ===================================================================== #
#  control-tension-bus-dc (ampliado)
# ===================================================================== #
def _vdc_extended():
    """4 paneles: (a) escalon carga con/sin feedforward, (b) PM vs Vdc,
       (c) anti-windup en arranque, (d) rizado 100 Hz en monofasico."""
    C = 10e-3
    Vdc0 = 700.0
    wcv = 2 * np.pi * 200.0
    Kpv = C * wcv / 2.0
    Tiv = 10.0 / wcv
    Pload = 500e3
    ilim = 1500.0
    w0 = 2 * np.pi * 50.0

    fig, axes = plt.subplots(2, 2, figsize=(11.0, 8.0))
    axa, axb, axc, axd = axes[0, 0], axes[0, 1], axes[1, 0], axes[1, 1]

    # (a) Escalon de carga con y sin feedforward
    dt = 1e-5
    t_arr = np.arange(0, 0.05, dt)

    def sim_vdc(with_ff=False):
        u_sq, u_ref, integ = Vdc0**2, Vdc0**2, 0.0
        hist = []
        for tk in t_arr:
            Pout = Pload if tk >= 0.01 else 0.0
            err = u_ref - u_sq
            integ += (Kpv / Tiv) * err * dt
            Pin = Kpv * err + integ + (Pout if with_ff else 0.0)
            u_sq = max(u_sq + 2.0 * (Pin - Pout) / C * dt, 0.0)
            hist.append(np.sqrt(u_sq))
        return np.array(hist)

    axa.plot(t_arr * 1e3, sim_vdc(False), color=BAD, lw=2, label="Sin feedforward")
    axa.plot(t_arr * 1e3, sim_vdc(True), color=ACC, lw=2, label="Con feedforward de $P_{out}$")
    axa.axvline(10, color="#aaa", ls=":", lw=1)
    axa.axhline(Vdc0, color="#aaa", ls="--", lw=0.8)
    axa.set_xlabel("t [ms]"); axa.set_ylabel("$V_{dc}$ [V]")
    axa.set_title(f"(a) Escalón de carga {Pload/1e3:.0f} kW en t=10 ms\nFeedforward reduce la caída de $V_{{dc}}$", fontsize=9)
    axa.legend(fontsize=8.5); axa.grid(True, alpha=0.4)

    # (b) PM vs Vdc: linealizado vs exacto
    Vdc_sweep = np.linspace(650, 900, 100)
    PM_sq_val = 180.0 + np.degrees(np.angle(1 + 1 / (1j * wcv * Tiv))) - 90.0

    def PM_lin(Vdc_op):
        wc_real = wcv * (Vdc0 / Vdc_op)
        return 180.0 + np.degrees(np.angle(1 + 1 / (1j * wc_real * Tiv))) - 90.0

    axb.plot(Vdc_sweep, [PM_lin(V) for V in Vdc_sweep], color=BAD, lw=2,
             label="Control sobre $v_{dc}$ (linealizado)")
    axb.plot(Vdc_sweep, np.full_like(Vdc_sweep, PM_sq_val), color=ACC, lw=2,
             label="Control sobre $v_{dc}^2$ (exacto)")
    axb.axvline(Vdc0, color="#aaa", ls=":", lw=1)
    axb.set_xlabel("$V_{dc}$ [V]"); axb.set_ylabel("Margen de fase [°]")
    axb.set_title("(b) PM vs $V_{dc}$: linealizado vs exacto\n$v_{dc}^2$ mantiene PM constante en todo el rango", fontsize=9)
    axb.legend(fontsize=8.5); axb.grid(True, alpha=0.4)

    # (c) Arranque con y sin anti-windup
    t_aw = np.arange(0, 0.15, dt)

    def sim_arranque(with_aw=True):
        u_sq, integ, ed, Pout = 0.0, 0.0, 325.0, 30e3
        hist = []
        for _ in t_aw:
            err = Vdc0**2 - u_sq
            id_ref = (Kpv * err + integ) / max(1.5 * ed, 1.0)
            id_sat = float(np.clip(id_ref, 0.0, ilim))
            Pin = 1.5 * ed * id_sat
            if not (with_aw and abs(id_sat - id_ref) > 1.0):
                integ += (Kpv / Tiv) * err * dt
            u_sq = max(u_sq + 2.0 * (Pin - Pout) / C * dt, 0.0)
            hist.append(np.sqrt(u_sq))
        return np.array(hist)

    axc.plot(t_aw * 1e3, sim_arranque(False), color=BAD, lw=2, label="Sin anti-windup")
    axc.plot(t_aw * 1e3, sim_arranque(True), color=ACC, lw=2, label="Con anti-windup")
    axc.axhline(Vdc0, color="#aaa", ls="--", lw=0.8)
    axc.set_xlabel("t [ms]"); axc.set_ylabel("$V_{dc}$ [V]")
    axc.set_title(f"(c) Arranque desde $V_{{dc}}$=0 con $i_{{lim}}$={ilim:.0f} A\nAnti-windup evita sobreoscilación prolongada", fontsize=9)
    axc.legend(fontsize=8.5); axc.grid(True, alpha=0.4)

    # (d) Rizado 100 Hz en monofasico
    t_rz = np.arange(0, 0.06, dt)
    P0, ed_peak = 50e3, 325.0
    wcv_slow = 2 * np.pi * 50.0
    wcv_fast = 2 * np.pi * 200.0
    H_slow = wcv_slow / (1j * 2 * w0 + wcv_slow)
    H_fast = wcv_fast / (1j * 2 * w0 + wcv_fast)
    id0 = P0 / (1.5 * ed_peak)
    id_slow = id0 * (1 + abs(H_slow) * 0.1 * np.cos(2 * w0 * t_rz))
    id_fast = id0 * (1 + abs(H_fast) * 0.6 * np.cos(2 * w0 * t_rz + np.angle(H_fast)))
    axd.plot(t_rz * 1e3, id_slow, color=ACC, lw=2, label="$\\omega_{cv}$=50 Hz (lento, limpio)")
    axd.plot(t_rz * 1e3, id_fast, color=BAD, lw=2, label="$\\omega_{cv}$=200 Hz (rizado 100 Hz visible)")
    axd.set_xlabel("t [ms]"); axd.set_ylabel("$i_d$ [A]")
    axd.set_title("(d) Rizado de 100 Hz en $i_d$ (monofásico)\n$\\omega_{cv}$ > 2ω realimenta el rizado → distorsión", fontsize=9)
    axd.legend(fontsize=8.5); axd.grid(True, alpha=0.4)

    fig.suptitle("Control tensión bus DC — análisis ampliado  ($C$=10 mF, $V_{dc}$=700 V, $\\omega_{cv}$=2π·200 rad/s)",
                 fontsize=10, y=1.01)
    fig.tight_layout(pad=2.0)
    _savefig(fig, "control-tension-bus-dc-analisis.png")




# ===================================================================== #
#  sistema-trifasico  (extended - 4 paneles)
# ===================================================================== #
def _trifasico_extended():
    V_LL = 690.0; Vf = V_LL / np.sqrt(3); f = 50.0; w = 2*np.pi*f
    IL = 836.0; phi = np.arccos(0.95)
    t = np.linspace(0, 2/f, 1000)

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle("Sistema trifasico equilibrado - analisis completo", fontsize=13, fontweight="bold")

    ax = axes[0, 0]
    va = np.sqrt(2)*Vf*np.cos(w*t)
    vb = np.sqrt(2)*Vf*np.cos(w*t - 2*np.pi/3)
    vc = np.sqrt(2)*Vf*np.cos(w*t + 2*np.pi/3)
    ia = np.sqrt(2)*IL*np.cos(w*t - phi)
    ib = np.sqrt(2)*IL*np.cos(w*t - 2*np.pi/3 - phi)
    ic = np.sqrt(2)*IL*np.cos(w*t + 2*np.pi/3 - phi)
    pa = va*ia; pb = vb*ib; pc = vc*ic
    p_total = pa + pb + pc
    P_const = 3*Vf*IL*np.cos(phi)
    tm = t * 1e3
    ax.plot(tm, va/(np.sqrt(2)*Vf), color=ACC, lw=1.4, alpha=0.7, label="$v_a$ (pu)")
    ax.plot(tm, vb/(np.sqrt(2)*Vf), color=BAD, lw=1.4, alpha=0.7, label="$v_b$")
    ax.plot(tm, vc/(np.sqrt(2)*Vf), color=OK,  lw=1.4, alpha=0.7, label="$v_c$")
    ax.plot(tm, pa/P_const, color=ACC, lw=1.0, ls="--", alpha=0.5, label="$p_a$ (pu)")
    ax.plot(tm, pb/P_const, color=BAD, lw=1.0, ls="--", alpha=0.5)
    ax.plot(tm, pc/P_const, color=OK,  lw=1.0, ls="--", alpha=0.5)
    ax.plot(tm, p_total/P_const, color="#222", lw=2.2, label="$p_{total}=P$ (cte)")
    ax.axhline(1.0, color="#222", ls=":", lw=1.0)
    ax.set_xlabel("t [ms]"); ax.set_ylabel("pu")
    ax.set_title("(a) Tensiones y potencias instantaneas")
    ax.legend(fontsize=7.5, ncol=2, loc="lower right"); ax.set_xlim(0, 40)

    ax = axes[0, 1]
    ang_fase = [90, 90-120, 90+120]
    labels_f = ["$\\bar V_a$", "$\\bar V_b$", "$\\bar V_c$"]
    colors_f = [ACC, BAD, OK]
    tips = []
    for ang, lbl, col in zip(ang_fase, labels_f, colors_f):
        xf = np.cos(np.radians(ang)); yf = np.sin(np.radians(ang))
        ax.annotate("", xy=(xf, yf), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=2.2))
        ax.text(1.22*xf, 1.22*yf, lbl, color=col, fontsize=10, ha="center", va="center")
        tips.append((xf, yf))
    line_pairs = [(0, 1, "$\\bar V_{ab}$"), (1, 2, "$\\bar V_{bc}$"), (2, 0, "$\\bar V_{ca}$")]
    for i, j, lbl in line_pairs:
        x0, y0 = tips[i]; x1, y1 = tips[j]
        ax.annotate("", xy=(x0, y0), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color="#888", lw=1.5))
        midx = (x0 + x1)/2; midy = (y0 + y1)/2
        ax.text(midx*1.55, midy*1.55, lbl, color="#555", fontsize=8, ha="center")
    ax.text(0.5, 0.02, "$V_{{LL}}=\\sqrt{{3}}\\,V_f={:.3f}\\,V_f$".format(np.sqrt(3)),
            fontsize=9, ha="center", transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.3", fc="#f5f5f5", ec="#bbb"))
    ax.set_xlim(-1.7, 1.7); ax.set_ylim(-1.7, 1.7); ax.set_aspect("equal")
    ax.axhline(0, color="#ddd", lw=0.6); ax.axvline(0, color="#ddd", lw=0.6)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("(b) Fasores de fase y tensiones de linea")

    ax = axes[1, 0]
    P_tri = 4.0; Q_tri = 3.0; S_tri = np.sqrt(P_tri**2 + Q_tri**2)
    phi_tri = np.arctan2(Q_tri, P_tri)
    ax.annotate("", xy=(P_tri, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=ACC, lw=2.5))
    ax.annotate("", xy=(P_tri, Q_tri), xytext=(P_tri, 0),
                arrowprops=dict(arrowstyle="-|>", color=ACC2, lw=2.5))
    ax.annotate("", xy=(P_tri, Q_tri), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=BAD, lw=2.5))
    ax.text(P_tri/2, -0.22, "P = 4 MW", color=ACC, fontsize=10, ha="center")
    ax.text(P_tri + 0.08, Q_tri/2, "Q = 3 MVAr", color=ACC2, fontsize=10)
    ax.text(P_tri/2 - 0.52, Q_tri/2 + 0.1,
            "S = {:.0f} MVA".format(S_tri), color=BAD, fontsize=10,
            rotation=np.degrees(phi_tri))
    th = np.linspace(0, phi_tri, 40)
    ax.plot(0.45*np.cos(th), 0.45*np.sin(th), color="#444", lw=1.2)
    ax.text(0.50, 0.07,
            "phi={:.1f}  FP={:.2f}".format(np.degrees(phi_tri), np.cos(phi_tri)),
            fontsize=9, color="#444")
    ax.set_xlim(-0.2, 5.2); ax.set_ylim(-0.5, 4.0); ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("(c) Triangulo de potencia (P=4 MW, Q=3 MVAr, S=5 MVA)")

    ax = axes[1, 1]
    V1 = 230.0; I1 = 10.0; phi1 = np.arccos(0.8)
    p_mono = V1*I1*np.cos(phi1) + V1*I1*np.cos(2*w*t - phi1)
    P_avg  = V1*I1*np.cos(phi1)
    p_tri2 = 3*P_avg * np.ones_like(t)
    ax.plot(tm, p_mono/1e3, color=ACC, lw=1.8, label="Monofasico $p(t)$ - pulsa a $2\\omega$")
    ax.axhline(P_avg/1e3, color=ACC, lw=1.0, ls=":",
               label="P_mono={:.0f} W (media)".format(P_avg))
    ax.plot(tm, p_tri2/1e3, color=OK, lw=2.2, label="Trifasico $p_{{3\\phi}}=P$ (constante)")
    ax.fill_between(tm, P_avg/1e3, p_mono/1e3, alpha=0.15, color=ACC)
    ax.set_xlabel("t [ms]"); ax.set_ylabel("p [kW]")
    ax.set_title("(d) Monofasico pulsa a 2w; trifasico = constante")
    ax.legend(fontsize=8, loc="upper right"); ax.set_xlim(0, 40)

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    _savefig(fig, "sistema-trifasico-analisis.png")


# ===================================================================== #
#  potencia-ac-fasores  (extended - 4 paneles)
# ===================================================================== #
def _potfasor_extended():
    V = 230.0; I = 10.0; phi = np.arccos(0.7); f = 50.0; w = 2*np.pi*f
    P1ph = V*I*np.cos(phi)
    t = np.linspace(0, 2/f, 1000); tm = t*1e3

    P_ind = 100e3; Q_ind = P_ind*np.tan(np.arccos(0.7))
    phi2 = np.arccos(0.95); Q_new = P_ind*np.tan(phi2)
    S_ind = np.sqrt(P_ind**2 + Q_ind**2); S_new = np.sqrt(P_ind**2 + Q_new**2)
    V_LL = 400.0; Vf = V_LL/np.sqrt(3)

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle("Potencia en AC y fasores - analisis completo", fontsize=13, fontweight="bold")

    ax = axes[0, 0]
    p_total = V*I*np.cos(phi) + V*I*np.cos(2*w*t - phi)
    ax.plot(tm, p_total, color=BAD, lw=2.0, label="$p(t)=P+VI\\cos(2\\omega t-\\varphi)$")
    ax.axhline(P1ph, color=ACC, lw=2.0, ls="--",
               label="$P={:.0f}$ W (media)".format(P1ph))
    ax.fill_between(tm, P1ph, p_total, where=(p_total > P1ph),
                    alpha=0.18, color=ACC2, label="energia hacia carga")
    ax.fill_between(tm, P1ph, p_total, where=(p_total < P1ph),
                    alpha=0.18, color=BAD, label="energia desde fuente")
    ax.set_xlabel("t [ms]"); ax.set_ylabel("p(t) [W]")
    ax.set_title("(a) Potencia instantanea (V={:.0f} V, I={} A, FP={:.1f})".format(V, I, np.cos(phi)))
    ax.legend(fontsize=8); ax.set_xlim(0, 40)

    ax = axes[0, 1]
    sc = 1e3
    ax.annotate("", xy=(P_ind/sc, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=ACC, lw=2.5))
    ax.annotate("", xy=(P_ind/sc, Q_ind/sc), xytext=(P_ind/sc, 0),
                arrowprops=dict(arrowstyle="-|>", color=BAD, lw=2.5))
    ax.annotate("", xy=(P_ind/sc, Q_ind/sc), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=BAD, lw=2.0, ls="dashed"))
    ax.annotate("", xy=(P_ind/sc, Q_new/sc), xytext=(P_ind/sc, 0),
                arrowprops=dict(arrowstyle="-|>", color=OK, lw=2.5))
    ax.annotate("", xy=(P_ind/sc, Q_new/sc), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=OK, lw=2.0, ls="dashed"))
    ax.text(P_ind/sc/2, -8, "P = 100 kW", color=ACC, fontsize=9, ha="center")
    ax.text(P_ind/sc + 3, Q_ind/sc*0.55,
            "Q1={:.0f} kVAr\n(FP=0.70)".format(Q_ind/sc), color=BAD, fontsize=8)
    ax.text(P_ind/sc + 3, Q_new/sc*0.55,
            "Q2={:.0f} kVAr\n(FP=0.95)".format(Q_new/sc), color=OK, fontsize=8)
    ax.text(P_ind/sc/2 - 22, Q_ind/sc/2 + 5,
            "S1={:.0f} kVA".format(S_ind/sc), color=BAD, fontsize=9,
            rotation=np.degrees(np.arctan2(Q_ind, P_ind)))
    ax.text(P_ind/sc/2 - 16, Q_new/sc/2 + 2,
            "S2={:.0f} kVA".format(S_new/sc), color=OK, fontsize=9,
            rotation=np.degrees(np.arctan2(Q_new, P_ind)))
    ax.set_xlim(-10, 175); ax.set_ylim(-15, 130)
    ax.set_xlabel("P [kW]"); ax.set_ylabel("Q [kVAr]")
    ax.set_title("(b) Triangulo antes/despues de compensacion de reactiva")
    ax.set_aspect("equal")

    ax = axes[1, 0]
    ks = 18.0
    ax.annotate("", xy=(V, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=ACC, lw=2.5))
    ax.text(V*1.05, 5, "$\\bar V$", color=ACC, fontsize=12)
    Ix = I*np.cos(-phi)*ks; Iy = I*np.sin(-phi)*ks
    ax.annotate("", xy=(Ix, Iy), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=BAD, lw=2.5))
    ax.text(Ix*1.08, Iy*1.08, "$\\bar I$", color=BAD, fontsize=12)
    ax.plot([Ix, Ix], [0, Iy], color="#888", ls=":", lw=1.2)
    ax.plot([0, Ix], [0, 0], color="#888", ls=":", lw=1.2)
    ax.text(Ix/2, -15, "$I\\cos\\varphi={:.1f}$ A".format(I*np.cos(phi)),
            color="#555", fontsize=8, ha="center")
    ax.text(Ix + 8, Iy/2, "$I\\sin\\varphi={:.1f}$ A".format(I*np.sin(phi)),
            color="#555", fontsize=8)
    th_arc = np.linspace(-phi, 0, 40)
    ax.plot(40*np.cos(th_arc), 40*np.sin(th_arc), color="#666", lw=1.2)
    ax.text(50, -22, "phi={:.1f} grados".format(np.degrees(phi)), fontsize=9, color="#444")
    ax.set_xlim(-20, 280); ax.set_ylim(-100, 60)
    ax.set_xlabel("Re"); ax.set_ylabel("Im")
    ax.set_title("(c) Diagrama fasorial (phi={:.1f}, FP={:.2f})".format(np.degrees(phi), np.cos(phi)))
    ax.axhline(0, color="#aaa", lw=0.6); ax.axvline(0, color="#aaa", lw=0.6)
    ax.set_aspect("equal")

    ax = axes[1, 1]
    k = 1.5 * Vf
    id_range = np.linspace(-600, 600, 200)
    iq_range = np.linspace(-600, 600, 200)
    ax.plot(id_range, k*id_range/1e3, color=ACC, lw=2.2,
            label="$P=(3/2)V_d i_d$  pdte={:.1f} kW/A".format(k/1e3))
    ax.plot(iq_range, -k*iq_range/1e3, color=ACC2, lw=2.2, ls="--",
            label="$Q=-(3/2)V_d i_q$  pdte={:.1f} kVAr/A".format(k/1e3))
    ax.axhline(0, color="#bbb", lw=0.6); ax.axvline(0, color="#bbb", lw=0.6)
    id_op = P_ind/(1.5*Vf); iq_op = -Q_ind/(1.5*Vf)
    ax.plot(id_op, P_ind/1e3, "o", color=ACC, ms=8, zorder=5)
    ax.plot(iq_op, Q_ind/1e3, "s", color=ACC2, ms=8, zorder=5)
    ax.annotate("$i_d^*={:.0f}$ A".format(id_op),
                xy=(id_op, P_ind/1e3), xytext=(id_op+40, P_ind/1e3-40),
                fontsize=8, color=ACC,
                arrowprops=dict(arrowstyle="-", color=ACC, lw=0.9))
    ax.annotate("$i_q^*={:.0f}$ A".format(iq_op),
                xy=(iq_op, Q_ind/1e3), xytext=(iq_op-200, Q_ind/1e3+30),
                fontsize=8, color=ACC2,
                arrowprops=dict(arrowstyle="-", color=ACC2, lw=0.9))
    ax.set_xlabel("$i_d$ o $i_q$ [A]"); ax.set_ylabel("P [kW] o Q [kVAr]")
    ax.set_title("(d) Control en dq: P<->id, Q<->iq  (Vd={:.0f} V RMS)".format(Vf))
    ax.legend(fontsize=8)

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    _savefig(fig, "potencia-ac-fasores-analisis.png")

# ===================================================================== #
#  representacion-espacio-estados-analisis  (sin decorador @figura)
# ===================================================================== #
def _ss_extended():
    """4 paneles: (a) diagrama bloques SS, (b) elementos e^(At),
    (c) mapa polos-ceros G_LCL, (d) respuesta impulso analitica vs Euler."""
    from scipy.linalg import expm
    from scipy.signal import ss2tf

    L1, L2, Cf, R1 = 2e-3, 0.5e-3, 15e-6, 0.05
    A3 = np.array([[-R1/L1, 0.0, -1.0/L1],
                   [0.0,    0.0,  1.0/L2],
                   [1.0/Cf, -1.0/Cf, 0.0]])
    B3 = np.array([[1.0/L1], [0.0], [0.0]])
    C3 = np.array([[0.0, 1.0, 0.0]])
    D3 = np.array([[0.0]])

    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.0))
    (a1, a2), (a3, a4) = axes

    # (a) Diagrama de bloques -----------------------------------------
    a1.axis("off"); a1.set_xlim(0, 10); a1.set_ylim(-1.6, 2.6)
    a1.set_title("(a) Diagrama de bloques del espacio de estados", pad=6)

    from matplotlib.patches import FancyBboxPatch
    def box_s(ax, cx, cy, w, h, txt):
        r = FancyBboxPatch((cx-w/2, cy-h/2), w, h, boxstyle="round,pad=0.03",
                           linewidth=1.4, edgecolor=ACC, facecolor="#eef4ff")
        ax.add_patch(r)
        ax.text(cx, cy, txt, ha="center", va="center", fontsize=13, color="#111")

    def arr_s(ax, x0, y0, x1, y1, lbl=""):
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color="#333", lw=1.5))
        if lbl:
            ax.text((x0+x1)/2, (y0+y1)/2+0.12, lbl, ha="center", fontsize=11, color="#333")

    box_s(a1, 1.5, 1.0, 1.2, 0.6, "$B$")
    circ = plt.Circle((3.3, 1.0), 0.32, color="#eef4ff", ec=ACC, lw=1.5, zorder=3)
    a1.add_patch(circ)
    a1.text(3.3, 1.0, "$+$", ha="center", va="center", fontsize=14, zorder=4)
    box_s(a1, 5.2, 1.0, 1.3, 0.6, "$\\int$")
    box_s(a1, 7.5, 1.0, 1.2, 0.6, "$C$")
    box_s(a1, 5.2, -0.5, 1.3, 0.6, "$A$")
    arr_s(a1, 0.0, 1.0, 0.9, 1.0, "$u$")
    arr_s(a1, 2.1, 1.0, 2.98, 1.0)
    arr_s(a1, 3.62, 1.0, 4.55, 1.0, "$\\dot{x}$")
    arr_s(a1, 5.85, 1.0, 6.9, 1.0, "$x$")
    arr_s(a1, 8.1, 1.0, 9.2, 1.0, "$y$")
    a1.plot([7.0, 7.0], [1.0, -0.5], color="#333", lw=1.5)
    a1.plot([7.0, 5.85], [-0.5, -0.5], color="#333", lw=1.5)
    a1.annotate("", xy=(3.3, 0.68), xytext=(3.3, -0.5),
                arrowprops=dict(arrowstyle="-|>", color="#333", lw=1.5))
    a1.plot([3.3, 4.55], [-0.5, -0.5], color="#333", lw=1.5)
    a1.text(5.2, -1.2, "realimentación de estado a través de $A$",
            ha="center", fontsize=9, color="#555")

    # (b) Elementos de e^(At) -----------------------------------------
    t_exp = np.linspace(0, 0.15, 600)
    A2x2  = np.array([[-1.0, 2.0], [0.0, -3.0]])
    mats  = [expm(A2x2 * ti) for ti in t_exp]
    e11 = np.array([M[0,0] for M in mats])
    e12 = np.array([M[0,1] for M in mats])
    e22 = np.array([M[1,1] for M in mats])
    a2.plot(t_exp*1e3, e11, color=ACC,  lw=2.2, label="$[e^{At}]_{11}$")
    a2.plot(t_exp*1e3, e12, color=ACC2, lw=2.0, label="$[e^{At}]_{12}$")
    a2.plot(t_exp*1e3, e22, color=BAD,  lw=2.0, label="$[e^{At}]_{22}$")
    a2.axhline(0, color="#bbb", lw=0.8)
    a2.set_xlabel("t [ms]"); a2.set_ylabel("valor elemento")
    a2.set_title("(b) Elementos de $e^{At}$ con $A=[[-1,2],[0,-3]]$\n"
                 "λ₁=−1, λ₂=−3 → todos decaen a 0")
    a2.legend(fontsize=9)

    # (c) Mapa polos-ceros G_iL2_vi -----------------------------------
    num, den = ss2tf(A3, B3, C3, D3)
    poles_lcl = np.roots(den)
    f_res = np.sqrt((L1+L2)/(L1*L2*Cf)) / (2*np.pi)
    a3.axvspan(-2e4, 0, color=OK, alpha=0.07)
    a3.axvline(0, color="#888", lw=1.0); a3.axhline(0, color="#ccc", lw=0.6)
    a3.scatter(poles_lcl.real, poles_lcl.imag, marker="x", s=120,
               color=ACC, lw=2.5, label=f"polos ({len(poles_lcl)})")
    idx_top = np.argmax(poles_lcl.imag)
    a3.annotate(f"resonancia ≈{f_res:.0f} Hz",
                xy=(poles_lcl[idx_top].real, poles_lcl[idx_top].imag),
                xytext=(200, poles_lcl[idx_top].imag * 0.55),
                arrowprops=dict(arrowstyle="->", color="#555"), fontsize=8.5)
    a3.set_xlabel("Re(s) [rad/s]"); a3.set_ylabel("Im(s) [rad/s]")
    a3.set_title(f"(c) Polos $G_{{i_{{L2}}/v_i}}(s)$: LCL 3 estados\n"
                 f"L1={L1*1e3:.0f}mH L2={L2*1e3:.1f}mH Cf={Cf*1e6:.0f}µF")
    a3.legend(fontsize=9); a3.set_xlim(-2e4, 1e3)

    # (d) Respuesta al impulso analítica vs Euler ----------------------
    dt = 2e-6
    t_imp = np.arange(0, 0.008, dt)
    g_anal = np.array([float(C3 @ expm(A3*ti) @ B3) for ti in t_imp])
    x_eu = np.zeros(3); g_euler = []
    u_imp = 1.0 / dt
    for k in range(len(t_imp)):
        g_euler.append(float(C3 @ x_eu))
        u_k = u_imp if k == 0 else 0.0
        x_eu = x_eu + dt * (A3 @ x_eu + B3.flatten() * u_k)
    a4.plot(t_imp*1e3, g_anal,         color=ACC, lw=2.2, label="analítica $Ce^{At}B$")
    a4.plot(t_imp*1e3, np.array(g_euler), color=BAD, lw=1.4, ls="--", label="Euler Δt=2 µs")
    a4.set_xlabel("t [ms]"); a4.set_ylabel("$g(t)$ [A·s⁻¹/V]")
    a4.set_title("(d) Respuesta al impulso LCL 3×3\n$g(t)=C\\,e^{At}B$ analítica vs Euler")
    a4.legend(fontsize=9)

    fig.suptitle("Espacio de estados — análisis avanzado", fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _savefig(fig, "representacion-espacio-estados-analisis.png")


# ===================================================================== #
#  linealizacion-teoria-analisis  (sin decorador @figura)
# ===================================================================== #
def _lin_extended():
    """4 paneles: (a) pendulo lineal vs no lineal, (b) sin(delta) y tangente,
    (c) autovalores modo potencia vs P/Sn, (d) GFM lineal vs no lineal."""
    from scipy.integrate import solve_ivp

    L_pu = 0.1; E = V = 1.0; mp = 0.005
    wf = 2*np.pi*10.0; w0 = 2*np.pi*50.0

    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.0))
    (a1, a2), (a3, a4) = axes

    # (a) Péndulo no lineal vs lineal ---------------------------------
    g_grav = 9.81; l_pend = 1.0
    def pend_nl(t,  y): return [y[1], -(g_grav/l_pend)*np.sin(y[0])]
    def pend_lin(t, y): return [y[1], -(g_grav/l_pend)*y[0]]
    t_p = np.linspace(0, 5, 800)
    for th0_d, col, lbl in [(5, ACC, "5°"), (20, ACC2, "20°"),
                             (45, OK, "45°"), (90, BAD, "90°")]:
        th0 = np.radians(th0_d)
        snl  = solve_ivp(pend_nl,  [0, 5], [th0, 0], t_eval=t_p, max_step=0.01)
        slin = solve_ivp(pend_lin, [0, 5], [th0, 0], t_eval=t_p, max_step=0.01)
        a1.plot(snl.t,  np.degrees(snl.y[0]),  color=col, lw=2.0, label=f"θ₀={lbl}")
        a1.plot(slin.t, np.degrees(slin.y[0]), color=col, lw=1.1, ls="--")
    a1.axhline(0, color="#bbb", lw=0.8)
    a1.set_xlabel("t [s]"); a1.set_ylabel("θ [°]")
    a1.set_title("(a) Péndulo: no lineal (—) vs linealizado (--)\ndivergencia crece con θ₀")
    a1.legend(fontsize=8.5, ncol=2)

    # (b) sin(δ) y tangente en δ₀=30° --------------------------------
    d0 = np.radians(30)
    dv = np.linspace(0, np.pi/2, 400)
    sin_v  = np.sin(dv)
    tang_v = np.sin(d0) + np.cos(d0)*(dv - d0)
    err_pct = np.abs(sin_v - tang_v) / np.maximum(np.abs(sin_v), 1e-9) * 100
    a2.plot(np.degrees(dv), sin_v,  color=ACC, lw=2.4, label="sin(δ)")
    a2.plot(np.degrees(dv), tang_v, color=BAD, lw=1.8, ls="--", label="tangente δ₀=30°")
    mask5 = err_pct < 5.0
    if mask5.any():
        d_lim = min(np.degrees(dv[mask5][-1]), 90)
        a2.axvspan(np.degrees(d0), d_lim, alpha=0.13, color=OK,
                   label=f"error<5% (hasta {d_lim:.0f}°)")
    a2.axvline(np.degrees(d0), color="#aaa", ls=":", lw=1.0)
    a2.scatter([np.degrees(d0)], [np.sin(d0)], color=ACC2, s=70, zorder=5)
    a2.set_xlabel("δ [°]"); a2.set_ylabel("valor")
    a2.set_title("(b) Linealización de sin(δ) en δ₀=30°\n$K_s=(EV/X)\\cos(\\delta_0)$")
    a2.legend(fontsize=8.5)

    # (c) Autovalores modo potencia vs P/Sn ---------------------------
    P_vec = np.linspace(0.01, 0.99, 300)
    lam_re, lam_im = [], []
    for P in P_vec:
        d_eq = np.arcsin(np.clip(P * L_pu / (E*V), -1, 1))
        Ks   = (E*V/L_pu)*np.cos(d_eq)
        eigs = np.linalg.eigvals(np.array([[0.0, -mp*w0], [wf*Ks, -wf]]))
        idx  = np.argmax(np.abs(eigs.imag))
        lam_re.append(eigs[idx].real); lam_im.append(np.abs(eigs[idx].imag))
    lam_re = np.array(lam_re); lam_im = np.array(lam_im)
    zeta_v = -lam_re / np.sqrt(lam_re**2 + lam_im**2 + 1e-30)
    ax3b = a3.twinx()
    a3.plot(P_vec, lam_re, color=ACC,  lw=2.2, label="Re(λ)")
    a3.plot(P_vec, lam_im, color=ACC2, lw=1.8, ls="--", label="|Im(λ)|")
    ax3b.plot(P_vec, zeta_v, color=OK, lw=1.6, ls=":", label="ζ")
    a3.axhline(0, color="#bbb", lw=0.8)
    a3.set_xlabel("$P/S_n$"); a3.set_ylabel("autovalor [rad/s]")
    ax3b.set_ylabel("ζ", color=OK)
    a3.set_title("(c) Modo de potencia GFM vs $P/S_n$\n$K_s\\to 0$ cuando $\\delta_0\\to 90°$")
    h1, l1 = a3.get_legend_handles_labels()
    h2, l2 = ax3b.get_legend_handles_labels()
    a3.legend(h1+h2, l1+l2, fontsize=8.5, loc="center right")

    # (d) GFM no lineal vs linealizado --------------------------------
    d0_nom = np.radians(30)
    P0_nom = (E*V/L_pu)*np.sin(d0_nom)
    Ks0    = (E*V/L_pu)*np.cos(d0_nom)
    A_lin0 = np.array([[0.0, -mp*w0], [wf*Ks0, -wf]])

    def gfm_nl(t, x, dP):
        P_elec = (E*V/L_pu)*np.sin(x[0])
        return [w0*mp*(P0_nom + dP - P_elec), wf*(P_elec - x[1])]

    t_gfm = np.linspace(0, 0.8, 2000)
    dt_l  = t_gfm[1] - t_gfm[0]
    for dP_frac, col, lbl in [(0.05, ACC, "5%"), (0.20, ACC2, "20%"), (0.40, BAD, "40%")]:
        sol_nl = solve_ivp(gfm_nl, [0, 0.8], [d0_nom, P0_nom],
                           args=(dP_frac,), t_eval=t_gfm, max_step=1e-4)
        x_l = np.zeros(2); d_lin = []
        for _ in t_gfm:
            d_lin.append(x_l[0] + d0_nom)
            x_l = x_l + dt_l*(A_lin0 @ x_l + np.array([0.0, wf*dP_frac]))
        a4.plot(t_gfm, np.degrees(sol_nl.y[0]),        color=col, lw=2.0, label=f"NL {lbl}")
        a4.plot(t_gfm, np.degrees(np.array(d_lin)),    color=col, lw=1.2, ls="--")
    a4.axhline(np.degrees(d0_nom), color="#bbb", lw=0.8, ls=":")
    a4.set_xlabel("t [s]"); a4.set_ylabel("δ [°]")
    a4.set_title("(d) GFM: no lineal (—) vs linealizado (--)\n"
                 "pert. 5/20/40% $S_n$ desde $\\delta_0$=30°")
    a4.legend(fontsize=8.5)

    fig.suptitle("Linealización — análisis avanzado", fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _savefig(fig, "linealizacion-teoria-analisis.png")


# ===================================================================== #
#  transformada-laplace-analisis  (sin decorador @figura)
# ===================================================================== #
def _laplace_extended():
    """4 paneles: (a) 6 pares tiempo/polo, (b) valor final, (c) convolución, (d) fracciones parciales."""
    from scipy.signal import impulse

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle("Transformada de Laplace — análisis completo", fontsize=13, fontweight="bold")
    (a1, a2), (a3, a4) = axes

    # (a) 6 pares: señal en el tiempo + polo en el plano s ------------------
    t = np.linspace(0, 4, 600)
    signals = [
        ("Impulso $\\delta(t)$",  "polo en $\\infty$", [0.0], [1.0], ACC),
        ("Escalón $1(t)$",        "polo en $s=0$",      t*0+1.0, None, ACC2),
        ("Rampa $t$",             "doble polo $s=0$",   t,        None, OK),
        ("Exp. $e^{-2t}$",        "polo $s=-2$",        np.exp(-2*t), None, BAD),
        ("Senoide $\\sin(3t)$",   "polos $\\pm j3$",   np.sin(3*t), None, "#9b59b6"),
        ("Amort. $e^{-t}\\sin(3t)$", "polos $-1\\pm j3$", np.exp(-t)*np.sin(3*t), None, "#e67e22"),
    ]
    colors_sig = [s[4] for s in signals]
    for idx, (lbl, pole_lbl, sig, _, col) in enumerate(signals):
        if idx == 0:
            a1.plot([0, 0], [0, 1.5], color=col, lw=2.0)
            a1.plot([0], [1.5], "o", color=col, ms=7, label=lbl)
        elif sig is not None:
            clip = np.clip(sig, -1.8, 1.8)
            a1.plot(t, clip + idx*0.05, color=col, lw=1.6, label=lbl)
    a1.set_xlim(0, 4); a1.set_ylim(-0.3, 1.7)
    a1.set_xlabel("t [s]"); a1.set_ylabel("f(t)")
    a1.set_title("(a) Señales fundamentales en el tiempo")
    a1.legend(fontsize=7.5, ncol=2, loc="upper right")

    # Inset: polos en el plano s
    ax_ins = a1.inset_axes([0.03, 0.55, 0.38, 0.42])
    pole_positions = [
        (None, None),     # impulso - polo en inf
        (0.0, 0.0),       # escalón
        (0.0, 0.0),       # rampa (doble)
        (-2.0, 0.0),      # exp
        (0.0, 3.0),       # senoide +
        (-1.0, 3.0),      # amortiguada +
    ]
    ax_ins.axhline(0, color="#aaa", lw=0.7); ax_ins.axvline(0, color="#aaa", lw=0.7)
    for i, (pr, pi) in enumerate(pole_positions):
        col = colors_sig[i]
        if pr is None: continue
        ax_ins.scatter([pr], [pi], marker="x", s=60, color=col, lw=2.0)
        if pi != 0:
            ax_ins.scatter([pr], [-pi], marker="x", s=60, color=col, lw=2.0)
    ax_ins.set_xlim(-3.5, 1); ax_ins.set_ylim(-4, 4)
    ax_ins.set_xlabel("Re", fontsize=7); ax_ins.set_ylabel("Im", fontsize=7)
    ax_ins.tick_params(labelsize=6); ax_ins.set_title("Polos en plano s", fontsize=7)
    ax_ins.grid(True, alpha=0.4)

    # (b) Valor final: Y(s) = 5/[s(s+3)] -> y(inf) = 5/3 ------------------
    t2 = np.linspace(0, 5, 600)
    y_t = (5/3) * (1 - np.exp(-3*t2))
    a2.plot(t2, y_t, color=ACC, lw=2.2, label="$y(t)=\\frac{5}{3}(1-e^{-3t})$")
    a2.axhline(5/3, color=BAD, lw=1.6, ls="--",
               label="$\\lim_{{t\\to\\infty}}y = \\lim_{{s\\to0}} s\\cdot Y(s)=\\frac{5}{3}$")
    a2.annotate("$Y(s)=\\dfrac{5}{s(s+3)}$\n$\\Rightarrow$ v.f. $= \\dfrac{5}{3}\\approx1.667$",
                xy=(3.5, 5/3), xytext=(1.5, 1.2),
                fontsize=9, color=BAD,
                arrowprops=dict(arrowstyle="->", color=BAD, lw=1.0))
    a2.set_xlabel("t [s]"); a2.set_ylabel("y(t)")
    a2.set_title("(b) Teorema del valor final\n"
                 "$\\lim_{t\\to\\infty}f(t)=\\lim_{s\\to 0}s\\,F(s)$  (si todos los polos Re < 0 ó en $s=0$)")
    a2.legend(fontsize=9)

    # (c) Convolución: g(t)=e^{-t}, u(t)=1(t), y(t)=1-e^{-t} --------------
    t3 = np.linspace(0, 5, 600)
    g_t = np.exp(-t3)
    u_t = np.ones_like(t3)
    y_conv = 1 - np.exp(-t3)
    a3.plot(t3, g_t,    color=ACC,  lw=2.0, label="$g(t)=e^{-t}$ (respuesta impulso)")
    a3.plot(t3, u_t,    color=ACC2, lw=2.0, ls="--", label="$u(t)=1(t)$ (escalón)")
    a3.plot(t3, y_conv, color=BAD,  lw=2.4, label="$y(t)=g*u=1-e^{-t}$")
    a3.annotate("$Y(s)=G(s)\\cdot U(s)$\n$=\\dfrac{1}{s+1}\\cdot\\dfrac{1}{s}$\n$=\\dfrac{1}{s(s+1)}$",
                xy=(1.0, y_conv[120]), xytext=(2.5, 0.4),
                fontsize=9, color=BAD,
                arrowprops=dict(arrowstyle="->", color=BAD, lw=1.0))
    a3.set_xlabel("t [s]"); a3.set_ylabel("valor")
    a3.set_title("(c) Convolución = multiplicación en $s$\n"
                 "$y(t)=\\int_0^t g(\\tau)\\,u(t-\\tau)\\,d\\tau$")
    a3.legend(fontsize=9)

    # (d) Fracciones parciales: Y(s) = (2s+3)/[(s+1)(s+2)] ----------------
    # A = (2(-1)+3)/((-1+2)) = 1/1 = 1; B = (2(-2)+3)/((-2+1)) = (-1)/(-1) = 1
    A_r = 1.0; B_r = 1.0
    t4 = np.linspace(0, 5, 600)
    y_total = A_r*np.exp(-1*t4) + B_r*np.exp(-2*t4)
    y_term1 = A_r*np.exp(-1*t4)
    y_term2 = B_r*np.exp(-2*t4)
    a4.fill_between(t4, y_term1, alpha=0.25, color=ACC,  label="$A\\,e^{-t}$, $A=1$")
    a4.fill_between(t4, y_term2, alpha=0.25, color=ACC2, label="$B\\,e^{-2t}$, $B=1$")
    a4.plot(t4, y_total, color=BAD,  lw=2.4, label="$y(t)=e^{-t}+e^{-2t}$ (suma)")
    a4.plot(t4, y_term1, color=ACC,  lw=1.8)
    a4.plot(t4, y_term2, color=ACC2, lw=1.8)
    a4.text(0.5, 1.55,
            "$Y(s)=\\dfrac{2s+3}{(s+1)(s+2)}=\\dfrac{A}{s+1}+\\dfrac{B}{s+2}$\n"
            "$A=\\lim_{s\\to-1}(s+1)Y(s)=\\dfrac{2(-1)+3}{1}=1$\n"
            "$B=\\lim_{s\\to-2}(s+2)Y(s)=\\dfrac{2(-2)+3}{-1}=1$",
            fontsize=8.5, color="#222",
            bbox=dict(boxstyle="round,pad=0.3", fc="#f0f4ff", ec=ACC, lw=0.8))
    a4.set_xlabel("t [s]"); a4.set_ylabel("y(t)")
    a4.set_title("(d) Fracciones parciales → antitransformada\n"
                 "$Y(s)=(2s+3)/[(s+1)(s+2)]$")
    a4.legend(fontsize=9)

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    _savefig(fig, "transformada-laplace-analisis.png")


# ===================================================================== #
#  variables-estado-analisis  (sin decorador @figura)
# ===================================================================== #
def _varestado_extended():
    """4 paneles: (a) circuito LCL estados, (b) respuesta escalón 3 estados,
    (c) mapa autovalores, (d) forma modal del modo resonante."""
    from scipy.linalg import eig
    from scipy.integrate import solve_ivp
    from scipy.signal import ss2tf

    L1, L2, Cf, R1 = 2e-3, 0.5e-3, 15e-6, 0.05
    A3 = np.array([[-R1/L1,  0.0,    -1.0/L1],
                   [1.0/Cf,  0.0,    -1.0/Cf],
                   [0.0,     1.0/L2,  0.0   ]])
    B3 = np.array([[1.0/L1], [0.0], [0.0]])

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle("Variables de estado — análisis completo (LCL L1=2mH L2=0.5mH Cf=15µF)",
                 fontsize=13, fontweight="bold")
    (a1, a2), (a3, a4) = axes

    # (a) Circuito LCL esquemático con estados marcados -------------------
    a1.axis("off"); a1.set_xlim(0, 10); a1.set_ylim(0, 5)
    a1.set_title("(a) Estados del circuito LCL y energías almacenadas", pad=6)

    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
    def box(ax, cx, cy, w, h, txt, col=ACC, fc="#eef4ff"):
        r = FancyBboxPatch((cx-w/2, cy-h/2), w, h, boxstyle="round,pad=0.05",
                           linewidth=1.4, edgecolor=col, facecolor=fc)
        ax.add_patch(r)
        ax.text(cx, cy, txt, ha="center", va="center", fontsize=11, color="#111")

    def wire(ax, x0, y0, x1, y1):
        ax.plot([x0, x1], [y0, y1], color="#333", lw=2.0)

    def arr(ax, x0, y0, x1, y1):
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color="#333", lw=1.5))

    # fuente
    box(a1, 0.8, 2.5, 1.0, 3.0, "$v_i$\n(fuente)", col="#888", fc="#f8f8f8")
    wire(a1, 1.3, 3.5, 1.3, 4.5); wire(a1, 1.3, 4.5, 9.5, 4.5)
    wire(a1, 1.3, 1.5, 1.3, 0.5); wire(a1, 1.3, 0.5, 9.5, 0.5)

    # L1
    box(a1, 3.0, 4.5, 1.6, 0.7, "$L_1$, $R_1$", col=ACC)
    wire(a1, 1.3, 4.5, 2.2, 4.5)
    # iL1 arrow
    arr(a1, 2.2, 4.7, 3.0, 4.7)
    a1.text(2.6, 4.9, "$i_{L1}$ → estado 1", fontsize=8, color=ACC)
    a1.text(2.2, 3.95, r"$W_{L1}=\frac{1}{2}L_1 i_{L1}^2$", fontsize=8, color=ACC)

    # nodo vC + condensador
    wire(a1, 3.8, 4.5, 5.5, 4.5)
    box(a1, 5.5, 3.0, 1.0, 2.5, "$C_f$\n$v_C$\nstado 2", col=OK)
    wire(a1, 5.5, 4.5, 5.5, 4.25)
    wire(a1, 5.5, 1.75, 5.5, 0.5)
    a1.text(6.0, 3.8, "$v_C$ → estado 2", fontsize=8, color=OK)
    a1.text(6.0, 2.3, r"$W_{Cf}=\frac{1}{2}C_f v_C^2$", fontsize=8, color=OK)

    # L2
    box(a1, 7.5, 4.5, 1.6, 0.7, "$L_2$", col=BAD)
    wire(a1, 5.5, 4.5, 6.7, 4.5)
    arr(a1, 6.7, 4.7, 7.5, 4.7)
    a1.text(7.0, 4.9, "$i_{L2}$ → estado 3", fontsize=8, color=BAD)
    a1.text(6.9, 3.95, r"$W_{L2}=\frac{1}{2}L_2 i_{L2}^2$", fontsize=8, color=BAD)
    wire(a1, 8.3, 4.5, 9.5, 4.5)

    # PCC
    a1.text(9.5, 4.5, "PCC", ha="left", va="center", fontsize=9, color="#555")

    # (b) Respuesta escalón: escalón de vi=100V desde t=0 -----------------
    vi_step = 100.0  # V
    dt = 1e-6
    t_end = 0.015
    t_sim = np.arange(0, t_end, dt)
    x = np.zeros(3)
    iL1_t = []; vC_t = []; iL2_t = []
    for k in range(len(t_sim)):
        iL1_t.append(x[0]); vC_t.append(x[1]); iL2_t.append(x[2])
        u_k = np.array([vi_step / L1])
        dx = A3 @ x + B3.flatten() * vi_step
        x = x + dt * dx
    t_ms = t_sim * 1e3
    ax2 = a2
    ax2b = ax2.twinx()
    ax2.plot(t_ms, np.array(iL1_t), color=ACC,  lw=2.0, label="$i_{L1}(t)$ [A]")
    ax2.plot(t_ms, np.array(iL2_t), color=BAD,  lw=2.0, label="$i_{L2}(t)$ [A]")
    ax2b.plot(t_ms, np.array(vC_t), color=OK,   lw=1.8, ls="--", label="$v_C(t)$ [V]")
    ax2.set_xlabel("t [ms]"); ax2.set_ylabel("Corriente [A]", color=ACC)
    ax2b.set_ylabel("$v_C$ [V]", color=OK)
    ax2.set_title(f"(b) Respuesta a escalón $v_i={vi_step}$ V\n"
                  "3 dinámicas acopladas: las 3 resonancias del LCL")
    h1, l1 = ax2.get_legend_handles_labels()
    h2, l2 = ax2b.get_legend_handles_labels()
    ax2.legend(h1+h2, l1+l2, fontsize=9)

    # (c) Mapa de autovalores: los 3 polos del LCL -----------------------
    evals, evecs = eig(A3)
    f_res = np.sqrt((L1+L2)/(L1*L2*Cf)) / (2*np.pi)
    a3.axvspan(-5000, 0, color=OK, alpha=0.07)
    a3.axvline(0, color="#888", lw=1.0); a3.axhline(0, color="#ccc", lw=0.6)
    a3.scatter(evals.real, evals.imag, marker="x", s=160, color=ACC, lw=2.5, zorder=5,
               label="autovalores de $A$")
    idx_pos = np.argmax(evals.imag)
    a3.annotate(f"par resonante\n±j·{evals[idx_pos].imag/1e3:.2f} krad/s\n≈ {f_res:.0f} Hz",
                xy=(evals[idx_pos].real, evals[idx_pos].imag),
                xytext=(200, evals[idx_pos].imag*0.6),
                fontsize=8.5, color=ACC,
                arrowprops=dict(arrowstyle="->", color="#555"))
    idx_real = np.argmin(np.abs(evals.imag))
    a3.annotate(f"polo lento\n{evals[idx_real].real:.1f} rad/s\n≈−R/L_eq",
                xy=(evals[idx_real].real, evals[idx_real].imag),
                xytext=(evals[idx_real].real-8, evals[idx_real].imag+evals[idx_pos].imag*0.15),
                fontsize=8.5, color=BAD,
                arrowprops=dict(arrowstyle="->", color="#555"))
    a3.set_xlabel("Re(λ) [rad/s]"); a3.set_ylabel("Im(λ) [rad/s]")
    a3.set_title(f"(c) Autovalores de $A$ = polos de $G_{{LCL}}(s)$\n"
                 f"$\\det(sI-A)=0$ tiene las raíces en los autovalores")
    a3.legend(fontsize=9)

    # (d) Forma modal del modo resonante: autovector -----------------------
    idx_res = np.argmax(evals.imag)
    phi_res = np.abs(evecs[:, idx_res])
    phi_res = phi_res / np.max(phi_res)
    labels_st = ["$i_{L1}$", "$v_C$", "$i_{L2}$"]
    colors_st = [ACC, OK, BAD]
    bars = a4.bar(labels_st, phi_res, color=colors_st, width=0.5, edgecolor="#333", lw=1.2)
    for bar, val in zip(bars, phi_res):
        a4.text(bar.get_x()+bar.get_width()/2, val+0.02,
                f"{val:.2f}", ha="center", va="bottom", fontsize=11)
    a4.set_ylim(0, 1.25)
    a4.set_xlabel("Variable de estado"); a4.set_ylabel("Componente modal (normalizada)")
    a4.set_title(f"(d) Autovector del modo resonante ($f_{{res}}$≈{f_res:.0f} Hz)\n"
                 "indica qué estados participan más en la resonancia")
    a4.text(0.5, 1.1,
            f"Re(λ)={evals[idx_res].real:.2f} rad/s\n"
            f"|Im(λ)|={evals[idx_res].imag/1e3:.2f} krad/s",
            ha="center", fontsize=9, color=ACC,
            transform=a4.transAxes,
            bbox=dict(boxstyle="round,pad=0.3", fc="#eef4ff", ec=ACC, lw=0.8))

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    _savefig(fig, "variables-estado-analisis.png")


# ===================================================================== #
#  realimentacion (analisis extendido — 4 paneles)
# ===================================================================== #
def _realim_extended():
    """4 paneles: (a) |T|,|S|,|PS|,|CS| Bode  (b) robustez  (c) error vs clase  (d) trade-off S-T"""
    w = np.logspace(-2, 3, 2000)

    # Planta y controlador de referencia: L = 10/(s(s+1))
    def _L(s, K=10.0):
        return K / (s * (s + 1.0))

    jw = 1j * w
    L   = _L(jw)
    T   = L / (1.0 + L)
    S   = 1.0 / (1.0 + L)
    G   = 1.0 / (jw * (jw + 1.0))
    C   = 10.0 * np.ones_like(jw)
    PS  = G / (1.0 + L)
    CS  = C / (1.0 + L)

    fig, axes = plt.subplots(2, 2, figsize=(12.0, 8.5))
    a1, a2 = axes[0, 0], axes[0, 1]
    a3, a4 = axes[1, 0], axes[1, 1]

    # (a) Las cuatro FDT en Bode (magnitud) --------------------------------
    a1.semilogx(w, 20*np.log10(np.abs(T)),  color=ACC,  lw=2, label=r"$|T|$ — seguimiento")
    a1.semilogx(w, 20*np.log10(np.abs(S)),  color=BAD,  lw=2, label=r"$|S|$ — sensibilidad")
    a1.semilogx(w, 20*np.log10(np.abs(PS)), color=OK,   lw=2, ls="--", label=r"$|PS|$ — sens. planta")
    a1.semilogx(w, 20*np.log10(np.abs(CS)), color=ACC2, lw=2, ls="--", label=r"$|CS|$ — sens. controlador")
    a1.axhline(0,  color="#aaa", lw=0.8, ls=":")
    a1.axhline(-3, color="#ccc", lw=0.6, ls=":")
    a1.set_xlabel(r"$\omega$ [rad/s]"); a1.set_ylabel("dB")
    a1.set_title("(a) Las cuatro FDT fundamentales\n$S+T=1$ en todo $\\omega$")
    a1.legend(fontsize=8.5, loc="lower left")
    a1.set_ylim(-60, 20)

    # (b) Robustez: sensibilidad de T ante variación de G ------------------
    dT_over_dG = np.abs(S)   # dT/T = S · dG/G   → si dG/G=0.1, dT/T = |S|·0.1
    for K_rob, ls_rob, lbl in [(1.0, ":", "K=1"), (10.0, "-", "K=10"), (100.0, "--", "K=100")]:
        L_rob = _L(jw, K=K_rob)
        S_rob = 1.0 / (1.0 + L_rob)
        a2.semilogx(w, 20*np.log10(np.abs(S_rob)), lw=2, ls=ls_rob,
                    label=f"$|S|$, {lbl}  (var. T ≈ $S$ × var. G)")
    a2.axhline(0, color="#aaa", lw=0.8, ls=":")
    a2.set_xlabel(r"$\omega$ [rad/s]"); a2.set_ylabel("dB")
    a2.set_title("(b) Robustez: $|S|$ cuantifica\ncuánto afecta $\\Delta G$ a $T$")
    a2.legend(fontsize=8.5); a2.set_ylim(-40, 15)
    a2.text(0.03, 0.08, r"$\Delta T/T = S \cdot \Delta G/G$", transform=a2.transAxes,
            fontsize=9, color=BAD, bbox=dict(boxstyle="round", fc="w", ec=BAD, lw=0.8))

    # (c) Error de régimen vs clase del sistema (tipo 0, 1, 2) para 3 entradas
    entradas = ["Escalón\n(A/s)", "Rampa\n(A/s²)", "Parábola\n(A/s³)"]
    tipos    = ["Tipo 0", "Tipo 1", "Tipo 2"]
    errores  = np.array([
        # escalón   rampa    parabola
        [r"$\frac{A}{1+K_p}$", r"$\infty$",            r"$\infty$"],
        [r"$0$",               r"$\frac{A}{K_v}$",     r"$\infty$"],
        [r"$0$",               r"$0$",                  r"$\frac{A}{K_a}$"],
    ])
    # Tabla visual usando imshow (coloreada)
    tabla = np.array([
        [0.5, 1.0, 1.0],
        [0.0, 0.5, 1.0],
        [0.0, 0.0, 0.5],
    ])
    im = a3.imshow(tabla, cmap="RdYlGn_r", aspect="auto", vmin=0, vmax=1)
    a3.set_xticks(range(3)); a3.set_xticklabels(entradas, fontsize=9)
    a3.set_yticks(range(3)); a3.set_yticklabels(tipos, fontsize=9)
    a3.set_title("(c) Error en régimen permanente\n(verde=0, rojo=∞)", fontsize=10)
    for i in range(3):
        for j in range(3):
            a3.text(j, i, errores[i, j], ha="center", va="center", fontsize=9, color="#111")
    a3.grid(False)

    # (d) Trade-off S vs T: |S|+|T|≥1 — ilustración en dB ----------------
    # Sumar |S|+|T| en módulo lineal = 1 siempre; mostrar bw de S y T
    a4.semilogx(w, 20*np.log10(np.abs(T)), color=ACC,  lw=2.5, label=r"$|T|$: buena pista ref")
    a4.semilogx(w, 20*np.log10(np.abs(S)), color=BAD,  lw=2.5, label=r"$|S|$: rechazo perturb.")
    # Zona de "buen seguimiento" T≈0 dB y zona "buen rechazo" S≈0 dB
    wc_idx = np.argmin(np.abs(np.abs(T) - np.abs(S)))  # cruce |T|=|S|
    a4.axvline(w[wc_idx], color="#888", ls="--", lw=1.2)
    a4.text(w[wc_idx]*1.15, -25, f"$\\omega_c\\approx{w[wc_idx]:.1f}$ rad/s\n(cruce $S=T$)",
            fontsize=8, color="#555")
    a4.fill_between([w[0],  w[wc_idx]], -60, 5, alpha=0.07, color=ACC, label="zona seguimiento (|T|≈0 dB)")
    a4.fill_between([w[wc_idx], w[-1]], -60, 5, alpha=0.07, color=BAD, label="zona atenua. (|S|→0 dB)")
    a4.set_xlabel(r"$\omega$ [rad/s]"); a4.set_ylabel("dB")
    a4.set_title("(d) Trade-off $S$ vs $T$\nmejorar uno en una banda perjudica al otro")
    a4.legend(fontsize=8.5, loc="lower right"); a4.set_ylim(-60, 15)

    fig.suptitle("Realimentación: análisis de las cuatro FDT fundamentales  $(L=10/[s(s+1)])$",
                 fontsize=11, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    _savefig(fig, "realimentacion-analisis.png")


# ===================================================================== #
#  routh-hurwitz (analisis extendido — 4 paneles)
# ===================================================================== #
def _routh_extended():
    """4 paneles: (a) región estable Routh s^4+...  (b) lugar raíces  (c) inestables  (d) fila ceros"""
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 8.5))
    a1, a2 = axes[0, 0], axes[0, 1]
    a3, a4 = axes[1, 0], axes[1, 1]

    # (a) Routh para s^4+3s^3+3s^2+2s+K: primera columna vs K
    # Polinomio: s^4 + 3s^3 + 3s^2 + 2s + K
    # Fila s^4: [1, 3, K]
    # Fila s^3: [3, 2, 0]
    # Fila s^2: b1=(3*3-1*2)/3 = 7/3,  b2=(3*K-1*0)/3 = K
    # Fila s^1: c1=(7/3*2 - 3*K)/(7/3) = 2 - 9K/7
    # Fila s^0: K
    K_arr = np.linspace(0, 3.0, 500)
    b1 = 7.0/3.0 * np.ones_like(K_arr)
    b2 = K_arr
    c1 = 2.0 - 9.0*K_arr/7.0
    d0 = K_arr
    K_lim = 14.0/9.0   # c1=0 → K=14/9≈1.556

    a1.plot(K_arr, b1, color=OK,   lw=2,  label=r"$b_1=7/3$ (fila $s^2$, col 1)")
    a1.plot(K_arr, b2, color=ACC2, lw=2,  label=r"$b_2=K$ (fila $s^2$, col 2)")
    a1.plot(K_arr, c1, color=ACC,  lw=2,  label=r"$c_1=2-9K/7$ (fila $s^1$)")
    a1.plot(K_arr, d0, color=BAD,  lw=2, ls="--", label=r"$d_0=K$ (fila $s^0$)")
    a1.axhline(0,  color="#aaa", lw=0.8, ls=":")
    a1.axvline(K_lim, color=BAD, lw=1.5, ls="--")
    a1.text(K_lim+0.04, 1.2, f"$K_{{lim}}=14/9\\approx{K_lim:.3f}$\n(c₁=0→inestable)", fontsize=8.5,
            color=BAD)
    a1.fill_between([0, K_lim], -0.1, 2.5, alpha=0.1, color=OK, label=f"estable $K<{K_lim:.2f}$")
    a1.set_xlabel("$K$"); a1.set_ylabel("Valor 1ª columna")
    a1.set_title("(a) Primera columna de Routh\n$s^4+3s^3+3s^2+2s+K$")
    a1.legend(fontsize=8, loc="upper right"); a1.set_ylim(-0.2, 2.8)

    # (b) Lugar de raíces: raíces de s^4+3s^3+3s^2+2s+K al variar K
    K_sweep = np.linspace(0, 2.5, 80)
    allr, allk = [], []
    for K in K_sweep:
        for ri in np.roots([1, 3, 3, 2, K]):
            allr.append(ri); allk.append(K)
    allr = np.array(allr)
    sc = a2.scatter(allr.real, allr.imag, c=allk, cmap="plasma", s=14, zorder=4)
    fig.colorbar(sc, ax=a2, label="$K$")
    a2.axvline(0, color=BAD, ls="--", lw=1.2)
    a2.axhline(0, color="#ccc", lw=0.6)
    # Marca el cruce en K=K_lim
    roots_lim = np.roots([1, 3, 3, 2, K_lim])
    imag_roots = roots_lim[np.abs(roots_lim.real) < 0.05]
    if len(imag_roots):
        a2.plot(imag_roots.real, imag_roots.imag, "X", color="k", ms=10, zorder=6)
        a2.annotate(f"$K={K_lim:.3f}$\npolo imaginario puro",
                    xy=(imag_roots[0].real, imag_roots[0].imag),
                    xytext=(0.4, imag_roots[0].imag*0.7), fontsize=8,
                    arrowprops=dict(arrowstyle="->", color="k"))
    a2.set_xlabel("Re(s)"); a2.set_ylabel("Im(s)")
    a2.set_title("(b) Lugar de raíces: $K$ lleva\nlos polos al eje imaginario en $K_{lim}$")

    # (c) Contar raíces inestables para K>K_lim (K=2)
    K_bad = 2.0
    roots_bad = np.roots([1, 3, 3, 2, K_bad])
    col_c = [OK if r.real < 0 else BAD for r in roots_bad]
    for r, c in zip(roots_bad, col_c):
        a3.scatter(r.real, r.imag, color=c, s=90, zorder=5,
                   marker="x" if r.real > 0 else "o", linewidths=2.5)
    a3.axvline(0, color=BAD, ls="--", lw=1.2); a3.axhline(0, color="#ccc", lw=0.6)
    n_spd = sum(1 for r in roots_bad if r.real > 0)
    a3.set_xlabel("Re(s)"); a3.set_ylabel("Im(s)")
    a3.set_title(f"(c) $K={K_bad}$ (inestable): {n_spd} raíces en SPD\n"
                 "Routh: 2 cambios de signo en 1ª col.")
    a3.text(0.5, 0.08, f"Routh predice {n_spd} polo(s) inestable(s)",
            transform=a3.transAxes, ha="center", fontsize=9,
            color=BAD, bbox=dict(boxstyle="round", fc="w", ec=BAD, lw=0.8))

    # (d) Caso fila de ceros: s^3+s^2+s+1 → raíces imaginarias puras ±j
    # s^3+s^2+s+1 = (s^2+1)(s+1) → raíces: s=-1, s=±j
    coef_d = [1, 1, 1, 1]
    roots_d = np.roots(coef_d)
    for r in roots_d:
        color_d = OK if r.real < -1e-8 else (BAD if r.real > 1e-8 else ACC)
        a4.scatter(r.real, r.imag, color=color_d, s=120, zorder=6,
                   marker="o" if r.real < 0 else "D", linewidths=2)
    a4.axvline(0, color=BAD, ls="--", lw=1.2); a4.axhline(0, color="#ccc", lw=0.6)
    a4.annotate("fila nula en $s^1$\n→ polinomio auxiliar\n$s^2+1=0$",
                xy=(0, 1), xytext=(0.4, 0.7), fontsize=8.5, color=ACC,
                arrowprops=dict(arrowstyle="->", color=ACC))
    a4.annotate("polo real $s=-1$\n(estable)", xy=(-1, 0), xytext=(-1, 0.5),
                fontsize=8.5, color=OK, ha="center",
                arrowprops=dict(arrowstyle="->", color=OK))
    a4.set_xlabel("Re(s)"); a4.set_ylabel("Im(s)")
    a4.set_title("(d) Fila de ceros: $s^3+s^2+s+1$\nraíces en $j\\omega$ → marginalmente inestable")
    a4.set_xlim(-2.5, 1.5); a4.set_ylim(-1.8, 1.8)

    fig.suptitle("Routh-Hurwitz: análisis completo — tabla, lugar de raíces y casos especiales",
                 fontsize=11, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    _savefig(fig, "routh-hurwitz-analisis.png")


# ===================================================================== #
#  criterio-nyquist (analisis extendido — 4 paneles)
# ===================================================================== #
def _nyquist_extended():
    """4 paneles: (a) Nyquist L estable  (b) cond. estable  (c) L inestable  (d) principio argumento"""
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 8.5))
    a1, a2 = axes[0, 0], axes[0, 1]
    a3, a4 = axes[1, 0], axes[1, 1]
    w = np.logspace(-2, 2, 4000)
    jw = 1j * w

    # (a) L(s)=5/(s+1)(s+2): no rodea -1 → estable ----------------------
    L_a = 5.0 / ((jw + 1.0) * (jw + 2.0))
    a1.plot(L_a.real, L_a.imag,  color=ACC, lw=2, label="$L(j\\omega)$, $\\omega>0$")
    a1.plot(L_a.real, -L_a.imag, color=ACC, lw=2, ls="--", alpha=0.5, label="$\\omega<0$ (espejo)")
    # Punto crítico
    a1.scatter([-1], [0], color=BAD, s=80, zorder=6)
    a1.annotate("$-1$", xy=(-1, 0), xytext=(-1.4, 0.35), fontsize=9, color=BAD,
                arrowprops=dict(arrowstyle="->", color=BAD))
    # PM y GM: calcular manualmente
    # |L_a(jwc)|=1 → wc donde mag=1
    mag_a = np.abs(L_a)
    idx_wcp = np.argmin(np.abs(mag_a - 1.0))
    pm_a = 180.0 + np.degrees(np.angle(L_a[idx_wcp]))
    # Cruce eje real negativo: IM=0, Re<0
    imag_sign = np.diff(np.sign(L_a.imag))
    idx_wcg = np.where(imag_sign < 0)[0]
    if len(idx_wcg):
        gm_db = -20*np.log10(np.abs(L_a[idx_wcg[0]]))
    else:
        gm_db = float('inf')
    a1.set_xlim(-2, 3); a1.set_ylim(-3, 3)
    a1.axhline(0, color="#bbb", lw=0.6); a1.axvline(0, color="#bbb", lw=0.6)
    a1.set_xlabel("Re $L(j\\omega)$"); a1.set_ylabel("Im $L(j\\omega)$")
    a1.set_title(f"(a) $L=5/[(s+1)(s+2)]$: no rodea $-1$\nGM≈{gm_db:.1f} dB,  PM≈{pm_a:.1f}°")
    a1.legend(fontsize=8, loc="upper right"); a1.set_aspect("equal")
    a1.grid(True, alpha=0.3)

    # (b) Sistema condicionalmente estable: rodea -1 dependiendo de K
    # L(s) = K*(s+3)/[(s+1)^2*(s^2+0.1s+4)] — tipo fase no mínima aprox.
    # Usar algo más simple: L = K*4/(s*(s+1)*(s+4)) — rodea -1 para K grande
    for K_b, col_b, lbl_b in [(0.5, OK, "K=0.5 (estable)"), (3.0, BAD, "K=3 (inestable)")]:
        L_b = K_b * 4.0 / (jw * (jw + 1.0) * (jw + 4.0))
        w_plot = w[w > 0.01]
        L_bp = K_b * 4.0 / (1j*w_plot * (1j*w_plot + 1.0) * (1j*w_plot + 4.0))
        a2.plot(L_bp.real, L_bp.imag,  color=col_b, lw=2, label=lbl_b)
        a2.plot(L_bp.real, -L_bp.imag, color=col_b, lw=1.5, ls="--", alpha=0.45)
    a2.scatter([-1], [0], color=BAD, s=80, zorder=6)
    a2.annotate("$-1$", xy=(-1, 0), xytext=(-1.5, 1.5), fontsize=9, color=BAD,
                arrowprops=dict(arrowstyle="->", color=BAD))
    a2.axhline(0, color="#bbb", lw=0.6); a2.axvline(0, color="#bbb", lw=0.6)
    a2.set_xlabel("Re $L$"); a2.set_ylabel("Im $L$")
    a2.set_title("(b) Sistema: rodear $-1$ depende de $K$\n$L=4K/[s(s+1)(s+4)]$")
    a2.legend(fontsize=8.5, loc="upper right"); a2.set_xlim(-4, 2); a2.set_ylim(-3, 3)
    a2.grid(True, alpha=0.3)

    # (c) L(s)=4/[(s-2)(s+1)] — P=1 polo en SPD; necesita N=-1 para LC estable
    # Para K=4: L=4/[(s-2)(s+1)]: cruce eje real en ω donde Im=0
    # Im[L]=Im[4/((jω-2)(jω+1))] = 0 → Num: 4; Den: (jω-2)(jω+1)=(−ω²+jω−2jω−2)=(−ω²−2)+j(−ω)
    # Im[L]=0 cuando Im[Num*Den*]=0 → Im[4*conj(Den)]=0 → Im[conj(Den)]=0 → Im[Den]=0 → −ω=0 → ω=0
    # En ω=0: L=4/((-2)(1))=-2 → cruza eje real en −2 (a la izquierda de -1 → N=-1 antihorario)
    L_c = 4.0 / ((jw - 2.0) * (jw + 1.0))
    a3.plot(L_c.real, L_c.imag,  color=ACC, lw=2, label="$L(j\\omega)$, $\\omega>0$, $P=1$")
    a3.plot(L_c.real, -L_c.imag, color=ACC, lw=1.5, ls="--", alpha=0.5, label="$\\omega<0$")
    a3.scatter([-1], [0], color=BAD,  s=80, zorder=6)
    a3.scatter([-2], [0], color=ACC2, s=80, zorder=6)
    a3.annotate("$-1$", xy=(-1, 0), xytext=(-0.5, 1.0), fontsize=9, color=BAD,
                arrowprops=dict(arrowstyle="->", color=BAD))
    a3.annotate("cruce en\n$\\omega=0$: $L=-2$\n→ rodeo antihorario\n$N=-1=-P$",
                xy=(-2, 0), xytext=(-4.0, 1.2), fontsize=8, color=ACC2,
                arrowprops=dict(arrowstyle="->", color=ACC2))
    a3.axhline(0, color="#bbb", lw=0.6); a3.axvline(0, color="#bbb", lw=0.6)
    a3.set_xlabel("Re $L$"); a3.set_ylabel("Im $L$")
    a3.set_title("(c) $L=4/[(s-2)(s+1)]$: $P=1$\n$N=-P=-1$ → lazo cerrado estable ($Z=0$)")
    a3.legend(fontsize=8, loc="upper right")
    a3.set_xlim(-5, 2); a3.set_ylim(-3, 3); a3.grid(True, alpha=0.3)

    # (d) Principio del argumento: ilustración gráfica
    # Mostrar un contorno simple en el plano s y su imagen en el plano F
    theta = np.linspace(0, 2*np.pi, 500)
    # Contorno: círculo centrado en origen radio 1.5 (encierra cero en s=0)
    s_c = 1.5 * np.exp(1j*theta)
    F_c = s_c / (s_c + 2.0)  # un cero en s=0, un polo en s=-2 (fuera del contorno)
    a4.plot(s_c.real, s_c.imag, color=ACC, lw=2, label="Contorno $\\Gamma$ (plano $s$)")
    # Mini-axes para mostrar imagen F(Γ)
    # Escala ambos en el mismo axes usando un offset
    scale = 0.6
    F_shifted = F_c * scale + np.array(2.5 + 0j)
    a4.plot(F_shifted.real, F_shifted.imag, color=OK, lw=2, label="$F(\\Gamma)$ (plano $F$, escalado)")
    # Origen y punto -1 del plano F (escalado y desplazado)
    a4.scatter([0], [0], color=ACC, s=60, zorder=6)
    a4.scatter([2.5], [0], color=OK, s=60, zorder=6)   # origen de F en el plano desplazado
    a4.annotate("origen $s$-plano\n(cero de $F$)", xy=(0, 0), xytext=(-0.5, 1.5),
                fontsize=7.5, color=ACC, arrowprops=dict(arrowstyle="->", color=ACC))
    a4.annotate("origen $F$-plano\n($N_0=Z-P=1-0=1$ rodeo)", xy=(2.5, 0), xytext=(1.6, 1.5),
                fontsize=7.5, color=OK, arrowprops=dict(arrowstyle="->", color=OK))
    a4.text(0.04, 0.06, "$F(s)=s/(s+2)$: 1 cero (s=0) dentro de Γ\n→ $F(Γ)$ rodea el origen 1 vez",
            transform=a4.transAxes, fontsize=8.5,
            bbox=dict(boxstyle="round", fc="w", ec="#888", lw=0.8))
    a4.axhline(0, color="#bbb", lw=0.6); a4.axvline(0, color="#bbb", lw=0.6)
    a4.set_xlabel("Re"); a4.set_ylabel("Im")
    a4.set_title("(d) Principio del argumento\n$N_0 = Z - P$ rodeos del origen")
    a4.legend(fontsize=8.5, loc="upper right"); a4.set_aspect("equal")
    a4.set_xlim(-2.5, 4.5); a4.set_ylim(-2.5, 2.5); a4.grid(True, alpha=0.3)

    fig.suptitle("Criterio de Nyquist: principio del argumento y aplicaciones",
                 fontsize=11, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    _savefig(fig, "criterio-nyquist-analisis.png")


# ===================================================================== #
#  error-regimen-permanente (analisis extendido — 4 paneles)
# ===================================================================== #
def _esserror_extended():
    """4 paneles: (a) error vs clase/entrada  (b) |S| PI  (c) trade-off error vs PM  (d) resonante"""
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 8.5))
    a1, a2 = axes[0, 0], axes[0, 1]
    a3, a4 = axes[1, 0], axes[1, 1]
    t = np.linspace(0, 4, 800)

    # (a) Error ante escalón, rampa, parábola para tipos 0, 1, 2 -----------
    # Tipo 0: L=K/(s+1) con K=4  → T=K/(s+1+K); ante escalón: ess=1/(1+K)=0.2
    # Tipo 1: L=K/(s(s+1)) con K=4
    # Tipo 2: L=K/(s^2(s+1)) con K=4 — escalón ok, rampa ok, parábola ≠0 pero muy lenta
    # Mostrar respuesta ante escalón unidad para los tres tipos
    K4 = 4.0
    tt0, y0 = signal.step(signal.TransferFunction([K4], [1, 1+K4]), T=t)
    tt1, y1 = signal.step(signal.TransferFunction([K4], [1, 1, K4]), T=t)
    tt2, y2 = signal.step(signal.TransferFunction([K4], [1, 1, 0, K4]), T=t)

    a1.axhline(1, color="#aaa", lw=0.8, ls=":", label="referencia")
    a1.plot(tt0, y0, color=BAD, lw=2,   label=f"Tipo 0: $e_{{ss}}=1/(1+K_p)={1/(1+K4):.2f}$")
    a1.plot(tt1, y1, color=OK,  lw=2,   label="Tipo 1: $e_{ss}=0$")
    a1.plot(tt2, y2, color=ACC, lw=2, ls="--", label="Tipo 2: $e_{ss}=0$ (más oscilarc.)")
    a1.annotate("", xy=(3.8, 1.0), xytext=(3.8, y0[-1]),
                arrowprops=dict(arrowstyle="<->", color=BAD))
    a1.text(3.5, (1.0+y0[-1])/2, f"$e_{{ss}}={1/(1+K4):.2f}$", color=BAD, fontsize=9, ha="right")
    a1.set_xlabel("t [s]"); a1.set_ylabel("y(t)")
    a1.set_title("(a) Respuesta al escalón: error según tipo de sistema\n"
                 f"($K={K4}$, planta $G=1/(s+1)$)")
    a1.legend(fontsize=8.5, loc="lower right"); a1.set_ylim(0, 1.9)

    # (b) |S(jω)| para PI bien diseñado: zona de baja frecuencia |S|<1 -----
    w = np.logspace(-2, 3, 2000)
    jw = 1j * w
    Ki = 5.0; Kp_pi = 2.0
    C_pi = Kp_pi + Ki / jw              # PI: Kp + Ki/s
    G_pl = 1.0 / (jw + 1.0)            # planta 1/(s+1)
    L_pi = C_pi * G_pl
    S_pi = 1.0 / (1.0 + L_pi)
    a2.semilogx(w, 20*np.log10(np.abs(S_pi)), color=ACC, lw=2.5, label="|S(jω)| con PI")
    a2.axhline(0,  color="#aaa", lw=0.8, ls=":")
    a2.axhline(-20, color="#ccc", lw=0.6, ls=":")
    # Marcar zona de baja frecuencia donde |S|<<1 → buen rechazo de perturbaciones
    w_cross = w[np.argmin(np.abs(np.abs(S_pi) - 1.0))]
    a2.axvline(w_cross, color=BAD, ls="--", lw=1.2)
    a2.fill_between(w[w < w_cross], -60, 5,
                    alpha=0.12, color=ACC, label=f"$|S|<0$ dB (rechazo)\n$\\omega<{w_cross:.1f}$ rad/s")
    a2.text(0.04, 0.08, "$|S(0)|=0$ (integrador → error DC nulo)",
            transform=a2.transAxes, fontsize=8.5, color=ACC,
            bbox=dict(boxstyle="round", fc="w", ec=ACC, lw=0.8))
    a2.set_xlabel(r"$\omega$ [rad/s]"); a2.set_ylabel("dB")
    a2.set_title("(b) $|S(j\\omega)|$ con PI: integrador garantiza\n$|S(0)|=0$ → error DC nulo")
    a2.legend(fontsize=8.5, loc="upper left"); a2.set_ylim(-60, 20)

    # (c) Trade-off: error escalón vs PM al variar K (tipo 0) ---------------
    K_arr = np.linspace(0.5, 30, 200)
    ess_arr = 1.0 / (1.0 + K_arr)   # error de posición tipo 0, G=1/(s+a), a=1
    # PM: L=K/(s+1) → cruce de ganancia en wc donde |L(jwc)|=1 → K/√(wc²+1)=1
    # wc=√(K²-1) para K>1; fase de L = -arctan(wc) → PM=180-90-arctan(wc)≈90-arctan(√(K²-1))
    wc_arr = np.sqrt(np.maximum(K_arr**2 - 1, 0))
    pm_arr = 90.0 - np.degrees(np.arctan(wc_arr))

    ax_pm = a3.twinx()
    l1, = a3.plot(K_arr, ess_arr, color=BAD, lw=2.5, label="$e_{ss}=1/(1+K)$ (error escalón)")
    l2, = ax_pm.plot(K_arr, pm_arr, color=ACC, lw=2.5, ls="--", label="PM [°]")
    a3.set_xlabel("Ganancia $K$"); a3.set_ylabel("Error en régimen $e_{ss}$", color=BAD)
    ax_pm.set_ylabel("Margen de fase PM [°]", color=ACC)
    a3.tick_params(axis="y", labelcolor=BAD); ax_pm.tick_params(axis="y", labelcolor=ACC)
    a3.set_title("(c) Trade-off (tipo 0): ↑$K$ reduce $e_{ss}$\npero reduce también PM")
    a3.axvline(5, color="#aaa", lw=0.8, ls=":")
    a3.text(5.3, 0.35, "K=5: compromiso\ntípico", fontsize=8.5, color="#555")
    lines = [l1, l2]; labels = [l.get_label() for l in lines]
    a3.legend(lines, labels, fontsize=8.5, loc="upper right")
    a3.set_ylim(0, 1); ax_pm.set_ylim(0, 90)

    # (d) Controlador resonante: |L(jω)| de PI + resonante (5° armónico) ---
    w5 = 2.0 * np.pi * 250.0   # 5° armónico de 50 Hz = 250 Hz
    Kres = 80.0
    # C_res(s) = Kres*s/(s²+w5²)
    C_res = Kres * jw / (-w**2 + w5**2 + 0j + 1e-6j)  # añadir damping mínimo
    # Con damping pequeño ωi=1 rad/s: C_res=Kres*s/(s²+2*1*s+w5²)
    wi_damp = 1.0
    C_res2 = Kres * jw / (-w**2 + 2j*wi_damp*w + w5**2)
    C_total = C_pi + C_res2
    L_total = C_total * G_pl
    a4.semilogx(w, 20*np.log10(np.abs(L_pi)),    color=ACC,  lw=2,   label="$|L|$ solo PI")
    a4.semilogx(w, 20*np.log10(np.abs(L_total)), color=OK,   lw=2.5, label="$|L|$ PI + resonante $\\omega_5$")
    a4.axvline(w5, color=BAD, ls="--", lw=1.2)
    a4.text(w5*1.1, 40, f"$\\omega_5={w5/(2*np.pi):.0f}$ Hz\n(pico→∞)", fontsize=8.5,
            color=BAD)
    a4.set_xlabel(r"$\omega$ [rad/s]"); a4.set_ylabel("dB")
    a4.set_title("(d) Controlador resonante: pico de $|L|$\nen $\\omega_5$ garantiza error nulo al 5° armónico")
    a4.legend(fontsize=8.5, loc="lower left"); a4.set_ylim(-40, 80)
    a4.set_xlim(1, 1e4)

    fig.suptitle("Error en régimen permanente: constantes de error, perturbaciones, trade-off y resonante",
                 fontsize=11, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    _savefig(fig, "error-regimen-permanente-analisis.png")



# ===================================================================== #
#  control-vectorial (extended)
# ===================================================================== #
def _vector_extended():
    L, R = 2e-3, 0.05
    w0 = 2 * np.pi * 50
    Ts = 100e-6
    ac = 2 * np.pi * 750
    Kp = L * ac
    Ki = R * ac

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    axa, axb, axc, axd = axes[0, 0], axes[0, 1], axes[1, 0], axes[1, 1]

    # --- (a) orientacion dq ---
    theta = np.pi / 6
    t_circle = np.linspace(0, 2 * np.pi, 200)
    axa.plot(np.cos(t_circle), np.sin(t_circle), color="#ccc", lw=1, ls=":")
    axa.annotate("", xy=(1.38, 0), xytext=(-1.38, 0),
                 arrowprops=dict(arrowstyle="->", color="#aaa", lw=1.2))
    axa.annotate("", xy=(0, 1.38), xytext=(0, -1.38),
                 arrowprops=dict(arrowstyle="->", color="#aaa", lw=1.2))
    axa.text(1.42, 0, r"$\alpha$", fontsize=10, color="#888", va="center")
    axa.text(0, 1.42, r"$\beta$", fontsize=10, color="#888", ha="center")
    for ang, lbl, col in [(theta, "d", ACC), (theta + np.pi / 2, "q", OK)]:
        axa.annotate("", xy=(1.2 * np.cos(ang), 1.2 * np.sin(ang)),
                     xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=col, lw=2))
        axa.text(1.3 * np.cos(ang), 1.3 * np.sin(ang), lbl,
                 fontsize=12, color=col, ha="center", va="center", fontweight="bold")
    Vx, Vy = np.cos(theta), np.sin(theta)
    axa.annotate("", xy=(Vx, Vy), xytext=(0, 0),
                 arrowprops=dict(arrowstyle="-|>", color=BAD, lw=2.5))
    axa.text(Vx + 0.06, Vy + 0.06, r"$\mathbf{v}_{red}$", fontsize=12, color=BAD)
    axa.plot([0, Vx], [0, 0], color="#777", ls="--", lw=1)
    axa.plot([Vx, Vx], [0, Vy], color="#777", ls="--", lw=1)
    axa.text(0.40, 0.10, r"$\theta$", fontsize=11, color=BAD)
    axa.set_xlim(-1.55, 1.65); axa.set_ylim(-1.55, 1.55)
    axa.set_aspect("equal"); axa.axis("off")
    axa.set_title("(a) Orientacion dq con la tension de red\n"
                  r"$v_d=V,\;v_q=0$ $\Rightarrow$ $P=\frac{3}{2}Vi_d,\;Q=-\frac{3}{2}Vi_q$", fontsize=9)

    # --- (b) respuesta lazo vectorial ---
    dt = Ts / 4
    t_sim = np.arange(0, 12e-3, dt)
    t_step = 2e-3
    Id_ref = 600.0
    Iq_ref_final = 800.0

    def sim_voc(t_arr, id_ref, iq_ref_fn):
        id_, iq_ = id_ref, 0.0
        intd, intq = 0.0, 0.0
        id_out, iq_out = [], []
        for ti in t_arr:
            iqr = iq_ref_fn(ti)
            ed = 400.0
            err_d = id_ref - id_
            err_q = iqr - iq_
            intd += err_d * dt
            intq += err_q * dt
            vd = Kp * err_d + Ki * intd - w0 * L * iq_ + ed
            vq = Kp * err_q + Ki * intq + w0 * L * id_
            did = (vd - ed + w0 * L * iq_ - R * id_) / L * dt
            diq = (vq - w0 * L * id_ - R * iq_) / L * dt
            id_ += did; iq_ += diq
            id_out.append(id_); iq_out.append(iq_)
        return np.array(id_out), np.array(iq_out)

    iq_fn = lambda ti: Iq_ref_final if ti >= t_step else 0.0
    id_r, iq_r = sim_voc(t_sim, Id_ref, iq_fn)
    t_ms = t_sim * 1e3
    axb.plot(t_ms, id_r, color=ACC, lw=2, label=r"$i_d$ (flujo)")
    axb.plot(t_ms, iq_r, color=OK, lw=2, label=r"$i_q$ (par - escalon)")
    axb.axvline(t_step * 1e3, color="#aaa", ls=":", lw=1)
    axb.axhline(Id_ref, color=ACC, ls="--", lw=1, alpha=0.5)
    axb.axhline(Iq_ref_final, color=OK, ls="--", lw=1, alpha=0.5)
    axb.set_xlabel("t [ms]"); axb.set_ylabel("Corriente [A]")
    axb.set_title("(b) Escalon de par (iq*): id permanece constante\nDesacoplo correcto - flujo no perturbado", fontsize=9)
    axb.legend(fontsize=8)

    # --- (c) efecto error PLL ---
    def sim_pll_error(t_arr, dth, iq_tgt=800.0):
        id_, iq_ = 0.0, 0.0
        intd, intq = 0.0, 0.0
        id_out, iq_out = [], []
        for ti in t_arr:
            id_meas = id_ * np.cos(dth) + iq_ * np.sin(dth)
            iq_meas = -id_ * np.sin(dth) + iq_ * np.cos(dth)
            err_d = 0.0 - id_meas
            err_q = iq_tgt - iq_meas
            intd += err_d * dt
            intq += err_q * dt
            vd = Kp * err_d + Ki * intd
            vq = Kp * err_q + Ki * intq + 400.0
            did = (vd + w0 * L * iq_ - R * id_) / L * dt
            diq = (vq - w0 * L * id_ - R * iq_) / L * dt
            id_ += did; iq_ += diq
            id_out.append(id_); iq_out.append(iq_)
        return np.array(id_out), np.array(iq_out)

    id_ok, iq_ok = sim_pll_error(t_sim, 0.0)
    id_err, iq_err = sim_pll_error(t_sim, 10 * np.pi / 180)
    axc.plot(t_ms, id_ok, color=ACC, lw=2, ls="--", label=r"$i_d$ sin error PLL")
    axc.plot(t_ms, iq_ok, color=OK, lw=2, ls="--", label=r"$i_q$ sin error PLL")
    axc.plot(t_ms, id_err, color=BAD, lw=2, label=r"$i_d$ error PLL 10$^{\circ}$")
    axc.plot(t_ms, iq_err, color=ACC2, lw=2, label=r"$i_q$ error PLL 10$^{\circ}$")
    axc.set_xlabel("t [ms]"); axc.set_ylabel("Corriente [A]")
    axc.set_title("(c) Efecto de error de PLL de 10 grados\nAcoplamiento residual: id!=0 aunque id*=0", fontsize=9)
    axc.legend(fontsize=7)

    # --- (d) Bode lazo corriente VOC ---
    f_arr = np.logspace(1, 5, 2000)
    w_arr = 2 * np.pi * f_arr
    s_arr = 1j * w_arr
    Gp = 1.0 / (s_arr * L + R)
    delay = np.exp(-1.5 * Ts * s_arr)
    Gc = Kp + Ki / s_arr
    L_loop = Gc * Gp * delay
    mag_db = 20 * np.log10(np.abs(L_loop))
    phase_deg = np.unwrap(np.angle(L_loop)) * 180 / np.pi
    axd2 = axd.twinx()
    axd.semilogx(f_arr, mag_db, color=ACC, lw=2, label="|L(jw)| [dB]")
    axd2.semilogx(f_arr, phase_deg, color=BAD, lw=2, ls="--", label="angulo L [deg]")
    idx_c = np.argmin(np.abs(mag_db))
    fc = f_arr[idx_c]
    pm = 180 + phase_deg[idx_c]
    axd.axvline(fc, color="#888", ls=":", lw=1.2)
    axd.axhline(0, color="#888", ls=":", lw=1)
    axd.text(fc * 1.1, 5, f"fc={fc:.0f}Hz\nPM={pm:.0f}deg", fontsize=8, color="#555")
    axd.set_xlabel("frecuencia [Hz]"); axd.set_ylabel("|L| [dB]", color=ACC)
    axd2.set_ylabel("angulo L [deg]", color=BAD)
    axd2.tick_params(axis="y", colors=BAD)
    axd.tick_params(axis="y", colors=ACC)
    axd.set_ylim(-60, 80); axd2.set_ylim(-300, 20)
    axd.set_title(f"(d) Bode lazo corriente VOC\nKp={Kp:.3f}, Ki={Ki:.1f}, fc={fc:.0f}Hz, PM={pm:.0f}deg", fontsize=9)
    lines1, labs1 = axd.get_legend_handles_labels()
    lines2, labs2 = axd2.get_legend_handles_labels()
    axd.legend(lines1 + lines2, labs1 + labs2, fontsize=8)

    fig.suptitle("Control vectorial - analisis ampliado (L=2mH, R=50mOhm, ac=2pi*750Hz, Ts=100us)",
                 fontsize=11, y=1.01)
    fig.tight_layout(pad=2.0)
    _savefig(fig, "control-vectorial-analisis.png")


# ===================================================================== #
#  estabilidad-bibo (extended)
# ===================================================================== #
def _bibo_extended():
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    axa, axb, axc, axd = axes[0, 0], axes[0, 1], axes[1, 0], axes[1, 1]

    t = np.linspace(0, 4, 2000)

    # --- (a) tres sistemas ---
    for pole, col, lbl in [(-1.0, OK, "polo = -1 (estable)"),
                            (0.0, ACC2, "polo = 0 (marginal)"),
                            (0.5, BAD, "polo = +0.5 (inestable)")]:
        if pole == 0.0:
            y = t
        elif pole < 0:
            y = (1 - np.exp(pole * t)) / (-pole)
        else:
            y = np.clip((np.exp(pole * t) - 1) / pole, 0, 8)
        axa.plot(t, y, color=col, lw=2, label=lbl)
    axa.axhline(1.0, color="#aaa", ls=":", lw=1)
    axa.set_xlim(0, 4); axa.set_ylim(-0.1, 6)
    axa.set_xlabel("t [s]"); axa.set_ylabel("y(t)")
    axa.set_title("(a) Respuesta al escalon segun ubicacion del polo\nSolo polo en SPD garantiza salida acotada", fontsize=9)
    axa.legend(fontsize=8)

    # --- (b) cancelacion polo-cero inestable ---
    t2 = np.linspace(0, 3, 1000)
    g_imp = np.clip(np.exp(t2), 0, 25)
    axb.plot(t2, g_imp, color=BAD, lw=2.5, label="g(t)=exp(t) (polo en +1)")
    ax_ins = axb.inset_axes([0.52, 0.05, 0.44, 0.45])
    ax_ins.axvspan(-3, 0, color=OK, alpha=0.1)
    ax_ins.axvspan(0, 3, color=BAD, alpha=0.1)
    ax_ins.scatter([-1], [0], marker="o", s=90, facecolors="none", edgecolors="#888", lw=2, zorder=5)
    ax_ins.scatter([-1], [0], marker="x", s=90, color="#888", lw=2, zorder=5)
    ax_ins.scatter([1], [0], marker="x", s=110, color=BAD, lw=2.5, zorder=5)
    ax_ins.text(-1, 0.15, "cero", fontsize=6, ha="center", color="#888")
    ax_ins.text(1, 0.15, "polo +1", fontsize=6, ha="center", color=BAD)
    ax_ins.axvline(0, color="#888", lw=1); ax_ins.axhline(0, color="#888", lw=1)
    ax_ins.set_xlim(-3, 3); ax_ins.set_ylim(-0.8, 0.8)
    ax_ins.set_xlabel("Re(s)", fontsize=6); ax_ins.set_title("mapa polos", fontsize=6)
    ax_ins.tick_params(labelsize=5)
    axb.set_xlabel("t [s]"); axb.set_ylabel("g(t)")
    axb.set_title("(b) Cancelacion polo-cero inestable\nG=(s+1)/[(s-1)(s+1)]: FDT=1/(s-1), estado crece", fontsize=9)
    axb.legend(fontsize=8, loc="upper left")

    # --- (c) integrador BIBO-inestable ---
    t3 = np.linspace(0, 5, 500)
    axc.plot(t3, np.ones_like(t3), color="#aaa", lw=1.5, ls="--", label="u(t) (acotada)")
    axc.plot(t3, t3, color=BAD, lw=2.5, label="y(t)=t (no acotada)")
    axc.fill_between(t3, t3, alpha=0.12, color=BAD)
    axc.text(2.5, 2.3, "y(t) -> inf", fontsize=13, color=BAD, ha="center")
    axc.set_xlabel("t [s]"); axc.set_ylabel("amplitud")
    axc.set_title("(c) Integrador 1/s: BIBO-inestable\nPolo en s=0 -> integral de |g| diverge", fontsize=9)
    axc.legend(fontsize=8)

    # --- (d) mapa autovalores proyecto 01 ---
    eig_antes = np.array([
        -8.3+21.0j, -8.3-21.0j,
        -50.0+0j,
        0.0+21400j, 0.0-21400j,
        -200+5000j, -200-5000j,
        -800+0j,
    ])
    eig_despues = np.array([
        -8.3+21.0j, -8.3-21.0j,
        -50.0+0j,
        -400+21400j, -400-21400j,
        -200+5000j, -200-5000j,
        -800+0j,
    ])
    axd.axvspan(-1600, 0, color=OK, alpha=0.07)
    axd.axvspan(0, 200, color=BAD, alpha=0.12)
    axd.scatter(eig_antes.real, eig_antes.imag / 1e3, marker="x", s=100,
                color=BAD, lw=2.5, zorder=5, label="sin Kad: LCL en eje Im")
    axd.scatter(eig_despues.real, eig_despues.imag / 1e3, marker="o", s=80,
                facecolors="none", edgecolors=OK, lw=2, zorder=5, label="Kad=6Ohm: todos Re<0")
    axd.axvline(0, color="k", lw=1.5); axd.axhline(0, color="#aaa", lw=0.8)
    axd.annotate("LCL sin Kad", xy=(0, 21.4), xytext=(70, 18),
                 fontsize=7, color=BAD, arrowprops=dict(arrowstyle="->", color=BAD, lw=1))
    axd.annotate("LCL con Kad", xy=(-400, 21.4), xytext=(-1300, 18),
                 fontsize=7, color=OK, arrowprops=dict(arrowstyle="->", color=OK, lw=1))
    axd.set_xlabel("Re(lambda) [rad/s]"); axd.set_ylabel("Im(lambda) [krad/s]")
    axd.set_title("(d) Autovalores proyecto 01 antes/despues de Kad\nSin Kad: LCL en eje Im -> NO BIBO estable", fontsize=9)
    axd.legend(fontsize=7, loc="lower right")

    fig.suptitle("Estabilidad BIBO - analisis ampliado", fontsize=11, y=1.01)
    fig.tight_layout(pad=2.0)
    _savefig(fig, "estabilidad-bibo-analisis.png")


# ===================================================================== #
#  estabilidad-lyapunov (extended)
# ===================================================================== #
def _lyap_extended():
    from scipy.linalg import solve_continuous_lyapunov

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    axa, axb, axc, axd = axes[0, 0], axes[0, 1], axes[1, 0], axes[1, 1]

    # --- (a) curvas de nivel V=x^T P x ---
    A_sys = np.array([[0.0, 1.0], [-2.0, -3.0]])
    Q = np.eye(2)
    P = solve_continuous_lyapunov(A_sys.T, -Q)
    x1g = np.linspace(-2.5, 2.5, 300)
    x2g = np.linspace(-2.5, 2.5, 300)
    X1, X2 = np.meshgrid(x1g, x2g)
    V_grid = P[0, 0] * X1**2 + 2 * P[0, 1] * X1 * X2 + P[1, 1] * X2**2
    cs = axa.contour(X1, X2, V_grid, levels=[0.2, 0.5, 1.0, 2.0, 4.0, 7.0],
                     colors=[ACC], linewidths=1.2)
    axa.clabel(cs, fmt="V=%.1f", fontsize=7, colors=ACC)
    dt_l = 0.01
    for x0 in [(2.0, 0.5), (-2.0, 0.5), (1.5, -2.0), (-1.5, -2.0)]:
        x = np.array(x0, dtype=float)
        traj = [x.copy()]
        for _ in range(int(4 / dt_l)):
            x = x + A_sys @ x * dt_l
            traj.append(x.copy())
        traj = np.array(traj)
        axa.plot(traj[:, 0], traj[:, 1], color=OK, lw=1.8, alpha=0.8)
        axa.annotate("", xy=traj[15], xytext=traj[0],
                     arrowprops=dict(arrowstyle="-|>", color=OK, lw=1.5))
    axa.scatter(0, 0, color=BAD, s=60, zorder=5)
    axa.text(0.07, 0.07, "equilibrio", fontsize=8, color=BAD)
    axa.set_xlabel("$x_1$"); axa.set_ylabel("$x_2$")
    axa.set_xlim(-2.6, 2.6); axa.set_ylim(-2.6, 2.6)
    axa.set_title("(a) Curvas de nivel de V=x^T P x\nTrayectorias cruzan hacia adentro: Vdot<0", fontsize=9)

    # --- (b) energia bus DC ---
    Vnom = 700.0; R_src = 2.0
    P_crit = Vnom**2 / (4 * R_src)
    vdc_arr = np.linspace(350, 950, 500)
    for frac, col, lbl in [(0.7, OK, "P = 0.7*Pcrit (estable)"),
                            (1.0, ACC2, "P = Pcrit (margen cero)"),
                            (1.3, BAD, "P = 1.3*Pcrit (colapso)")]:
        P_cpl = frac * P_crit
        i_src = (Vnom - vdc_arr) / R_src
        Vdot = vdc_arr * i_src - P_cpl
        axb.plot(vdc_arr, Vdot / 1e3, color=col, lw=2, label=lbl)
    axb.axhline(0, color="#aaa", ls="--", lw=1)
    axb.axvline(Vnom / 2, color="#888", ls=":", lw=1)
    axb.text(Vnom / 2 + 8, 55, f"V_min={Vnom/2:.0f}V", fontsize=8, color="#555")
    axb.set_xlabel("vDC [V]"); axb.set_ylabel("Vdot [kJ/s]")
    axb.set_title("(b) Derivada de energia del bus DC\nVdot=vDC*(isrc - P_CPL/vDC): estable si P<Pcrit", fontsize=9)
    axb.set_ylim(-90, 130); axb.legend(fontsize=7)

    # --- (c) pendulo equivalente del droop ---
    E, Vg, X = 1.1, 1.0, 0.3
    delta = np.linspace(-1.0, np.pi + 0.3, 600)
    W = -E * Vg / X * np.cos(delta)
    P0 = 0.9 * E * Vg / X
    delta0 = np.arcsin(P0 * X / (E * Vg))
    delta_inst = np.pi - delta0
    W_inst = -E * Vg / X * np.cos(delta_inst)
    axc.plot(np.degrees(delta), W, color=ACC, lw=2.5)
    mask = (delta >= delta0) & (delta <= delta_inst)
    axc.fill_between(np.degrees(delta), W, W_inst, where=mask,
                     color=OK, alpha=0.18, label="region de atraccion")
    axc.scatter([np.degrees(delta0)], [-E * Vg / X * np.cos(delta0)],
                color=OK, s=90, zorder=5, label=f"estable d0={np.degrees(delta0):.0f}deg")
    axc.scatter([np.degrees(delta_inst)], [W_inst],
                color=BAD, s=90, marker="x", lw=2.5, zorder=5,
                label=f"inestable pi-d0={np.degrees(delta_inst):.0f}deg")
    axc.axhline(W_inst, color=BAD, ls=":", lw=1)
    axc.set_xlabel("delta [deg]"); axc.set_ylabel("W(delta) [pu]")
    axc.set_title("(c) Pendulo equivalente del droop\nW(delta)=-EV/X*cos(delta); region de atraccion", fontsize=9)
    axc.set_xlim(-60, 200); axc.legend(fontsize=7)

    # --- (d) efecto Xvirt ---
    delta2 = np.linspace(-0.5, np.pi + 0.1, 600)
    for Xv, col, lbl in [(0.0, BAD, "Xvirt=0"),
                          (0.1, ACC2, "Xvirt=0.1 pu"),
                          (0.2, OK, "Xvirt=0.2 pu")]:
        X_eff = X + Xv
        W_v = -E * Vg / X_eff * np.cos(delta2)
        axd.plot(np.degrees(delta2), W_v, color=col, lw=2, label=lbl)
        sin_arg = min(1.0, X_eff / (E * Vg))
        d0_v = np.arcsin(sin_arg)
        axd.scatter([np.degrees(d0_v)], [-E * Vg / X_eff * np.cos(d0_v)],
                    color=col, s=60, zorder=5)
    axd.set_xlabel("delta [deg]"); axd.set_ylabel("W(delta) [pu]")
    axd.set_title("(d) Xvirt amplia la region de atraccion\nMayor X_eff -> menor d0 -> mayor margen", fontsize=9)
    axd.set_xlim(-20, 200); axd.set_ylim(-5, 3); axd.legend(fontsize=8)

    fig.suptitle("Estabilidad de Lyapunov - analisis ampliado", fontsize=11, y=1.01)
    fig.tight_layout(pad=2.0)
    _savefig(fig, "estabilidad-lyapunov-analisis.png")


# ===================================================================== #
#  gain-scheduling-analisis  (sin decorador @figura)
# ===================================================================== #
def _gsched_extended():
    """4 paneles: Ks(P), zeta vs P, mapa scheduling, respuesta dinamica."""
    # Parametros GFM droop
    EV_X = 500e3          # EV/X en W/rad (potencia maxima = 500 kW/rad)
    mp   = 1.571e-3       # droop rad/(s·W)
    wf0  = 2*np.pi*10.0  # filtro de potencia nominal rad/s
    Sn   = 1e6            # potencia nominal VA

    # (a) Ks(P): Ks = EV/X * cos(delta0), con delta0 = arcsin(P / EV_X)
    P_pu = np.linspace(0.0, 0.95, 400)
    P_W  = P_pu * Sn
    # limitar para evitar arcsin>1
    P_W_c = np.clip(P_W, 0, EV_X * 0.999)
    delta0 = np.arcsin(P_W_c / EV_X)
    Ks    = EV_X * np.cos(delta0)
    Ks_max = EV_X

    # (b) zeta del modo de potencia
    # polo de potencia: s^2 + wf*s + wf*mp*Ks = 0  =>  zeta = wf / (2*sqrt(wf*mp*Ks))
    def zeta_fn(wf, Ks_arr):
        wn2 = wf * mp * Ks_arr
        wn2 = np.maximum(wn2, 1e-6)
        return wf / (2 * np.sqrt(wn2))

    zeta_fixed  = zeta_fn(wf0, Ks)
    # scheduling: wf proporcional a Ks
    wf_sched1   = wf0 * Ks / Ks_max          # It.1 lineal (factor 1)
    wf_sched2   = 1.5 * wf0 * Ks / Ks_max   # It.2 factor 1.5
    zeta_sch1   = zeta_fn(wf_sched1, Ks)
    zeta_sch2   = zeta_fn(wf_sched2, Ks)

    # (c) mapa discreto de scheduling (5 puntos)
    P_pts = np.array([0.0, 0.2, 0.4, 0.6, 0.8]) * Sn
    P_pts_c = np.clip(P_pts, 0, EV_X * 0.999)
    d_pts = np.arcsin(P_pts_c / EV_X)
    Ks_pts = EV_X * np.cos(d_pts)
    wf_pts = 1.5 * wf0 * Ks_pts / Ks_max

    # (d) respuesta ante escalon de potencia activa del modo de potencia
    dt = 1e-4; T = np.arange(0, 0.8, dt)
    P_ref = np.where(T >= 0.1, 0.1 * Sn, 0.0)  # escalon de 100 kW

    def sim_power_mode(P0_W, wf_val_fn):
        """Simula lazo de potencia droop+filtro ante escalon."""
        P = P0_W; P_filt = P0_W
        delta = np.arcsin(np.clip(P0_W / EV_X, -0.999, 0.999))
        omega = 314.159; out = []
        for k in range(len(T)):
            Ks_now = EV_X * np.cos(delta)
            wf_now = wf_val_fn(P_filt)
            P_filt += wf_now * (P - P_filt) * dt
            dP_ref = P_ref[k]
            # droop: omega = omega0 + mp*(Pset - P_filt), Pset=dP_ref
            omega = 314.159 + mp * (dP_ref - P_filt)
            delta += (omega - 314.159) * dt
            P = EV_X * np.sin(delta)
            out.append(P / Sn)
        return np.array(out)

    # sin scheduling: wf fijo
    wf_fixed_fn = lambda Pf: wf0
    wf_sch_fn   = lambda Pf: 1.5 * wf0 * (EV_X * np.cos(np.arcsin(np.clip(Pf / EV_X, 0, 0.999)))) / Ks_max

    P0_low  = 0.0 * Sn   # P=0 (Ks alto)
    P0_high = 0.8 * Sn   # P=0.8 (Ks bajo)

    resp_low_fixed  = sim_power_mode(P0_low,  wf_fixed_fn)
    resp_high_fixed = sim_power_mode(P0_high, wf_fixed_fn)
    resp_low_sch    = sim_power_mode(P0_low,  wf_sch_fn)
    resp_high_sch   = sim_power_mode(P0_high, wf_sch_fn)

    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.0))
    ax = axes.ravel()

    # panel a
    ax[0].plot(P_pu, Ks / Ks_max, color=ACC, lw=2.2)
    ax[0].set_xlabel("P / Sn [pu]"); ax[0].set_ylabel("Ks / Ks_max")
    ax[0].set_title("(a) Variación de la ganancia de planta Ks con la potencia")
    ax[0].axvline(0.9, color=BAD, ls="--", lw=1.2)
    ax[0].text(0.72, 0.55, "zona de\noperación\npráctica", fontsize=8, color="#555")

    # panel b
    ax[1].plot(P_pu, zeta_fixed, color=BAD, lw=2, label="$\\omega_f$ fijo")
    ax[1].plot(P_pu, zeta_sch1,  color=OK,  lw=2, label="scheduling ×1.0 (It.1)")
    ax[1].plot(P_pu, zeta_sch2,  color=ACC, lw=2.2, label="scheduling ×1.5 (It.2)")
    ax[1].axhline(0.5, color="#888", ls="--", lw=1); ax[1].text(0.02, 0.51, "ζ = 0.5", fontsize=8)
    ax[1].axhline(0.7, color="#555", ls=":",  lw=1); ax[1].text(0.02, 0.71, "ζ = 0.7", fontsize=8)
    ax[1].set_xlabel("P / Sn [pu]"); ax[1].set_ylabel("ζ  (amortiguamiento)")
    ax[1].set_title("(b) Amortiguamiento del modo de potencia: fijo vs scheduling")
    ax[1].set_ylim(0, 1.2); ax[1].legend(fontsize=8)

    # panel c
    ax[2].step(P_pts / Sn, wf_pts / (2*np.pi), where="post", color=ACC, lw=2.2, label="tabla discreta (5 pts)")
    wf_interp = np.interp(P_pu * Sn, P_pts, wf_pts)
    ax[2].plot(P_pu, wf_interp / (2*np.pi), color=OK, lw=1.5, ls="--", label="interpolación lineal")
    ax[2].plot(P_pts / Sn, wf_pts / (2*np.pi), "o", color=ACC, ms=7)
    ax[2].set_xlabel("P / Sn [pu]"); ax[2].set_ylabel("$\\omega_f / (2\\pi)$ [Hz]")
    ax[2].set_title("(c) Mapa de scheduling: $\\omega_f(P)$ para ζ ≈ 0.6")
    ax[2].legend(fontsize=8)

    # panel d
    ax[3].plot(T, resp_low_fixed,  color=BAD, lw=1.5, ls="--", label="P=0,  fijo")
    ax[3].plot(T, resp_high_fixed, color=BAD, lw=2.2,          label="P=0.8, fijo")
    ax[3].plot(T, resp_low_sch,    color=ACC, lw=1.5, ls="--", label="P=0,  sched.")
    ax[3].plot(T, resp_high_sch,   color=ACC, lw=2.2,          label="P=0.8, sched.")
    ax[3].axvline(0.1, color="#888", ls=":", lw=1)
    ax[3].set_xlabel("t [s]"); ax[3].set_ylabel("P [pu]")
    ax[3].set_title("(d) Respuesta ante escalón de carga: fijo vs scheduling")
    ax[3].legend(fontsize=8, ncol=2)

    fig.suptitle("Gain scheduling del lazo de potencia GFM", fontsize=13, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    _savefig(fig, "gain-scheduling-analisis.png")


# ===================================================================== #
#  matching-control-analisis  (sin decorador @figura)
# ===================================================================== #
def _match_extended():
    """4 paneles: analogia mecanica, respuesta Vdc, matching vs droop, BESS+SOC."""
    C_bus  = 10e-3    # F
    Vdc0   = 700.0    # V
    EV_X   = 500e3    # W/rad
    m_mod  = 0.9
    Sn     = 1e6      # W
    P_step = 200e3    # W  escalon de carga

    dt = 5e-5; T = np.arange(0, 0.6, dt)
    step_mask = T >= 0.1

    # (b) Vdc con matching vs control convencional de Vdc (Vdc regulado constante)
    def sim_matching(C, Vdc_init, k_match=None):
        """Matching: Vdc(t) oscila bajo escalon de carga."""
        Vdc = Vdc_init; delta = 0.0; out_vdc = []
        # k_match escala el angulo con Vdc
        km = k_match if k_match is not None else 1.0 / Vdc_init
        for k in range(len(T)):
            P_out = EV_X * np.sin(delta)   # potencia inyectada
            P_in  = 0.5 * Sn + (P_step if step_mask[k] else 0.0)
            Vdc  += (P_in - P_out) / (C * Vdc) * dt
            delta += km * (Vdc - Vdc_init) * dt
            out_vdc.append(Vdc)
        return np.array(out_vdc)

    def sim_vdc_regulated(C, Vdc_init, Kp=1000.0, Ki=2000.0):
        """Control PI clasico de Vdc: lo regula constante."""
        Vdc = Vdc_init; xi = 0.0; out_vdc = []
        for k in range(len(T)):
            e = Vdc_init - Vdc
            P_ctrl = Kp * e + xi
            xi += Ki * e * dt
            P_out = P_ctrl
            P_in  = 0.5 * Sn + (P_step if step_mask[k] else 0.0)
            Vdc  += (P_in - P_out) / (C * Vdc) * dt
            out_vdc.append(Vdc)
        return np.array(out_vdc)

    vdc_match = sim_matching(C_bus, Vdc0)
    vdc_reg   = sim_vdc_regulated(C_bus, Vdc0)

    # (c) Matching vs droop: respuesta de frecuencia (modo de potencia pequena senal)
    # Modelamos como sistema de segundo orden con los mismos polos
    dt2 = 1e-4; T2 = np.arange(0, 1.0, dt2)
    # parametros droop
    mp_droop = 1.571e-3; wf_droop = 2*np.pi*10
    # matching: equivalente con Jv=C/km^2, H = Jv*w0^2/(2Sn)
    km2 = 1.0 / Vdc0; Jv = C_bus / km2**2
    w0 = 314.159; Hv = Jv * w0**2 / (2 * Sn)

    def sim_droop_mode(mp, wf, P_load=P_step):
        delta = 0.0; P_filt = 0.5 * Sn; omega = w0; out = []
        for k in range(len(T2)):
            Ks = EV_X * np.cos(delta)
            P = EV_X * np.sin(delta)
            P_filt += wf * (P - P_filt) * dt2
            P_load_now = 0.5 * Sn + (P_load if T2[k] >= 0.1 else 0.0)
            omega = w0 + mp * (P_load_now - P_filt)
            delta += (omega - w0) * dt2
            out.append((omega - w0) / w0 * 100)  # desviacion %
        return np.array(out)

    def sim_match_mode(Hv_val, P_load=P_step):
        """Matching: omega deriva con la inercia virtual."""
        omega = w0; delta = 0.0; out = []
        D_damp = 50.0 * Sn / w0  # amortiguamiento virtual
        for k in range(len(T2)):
            P_e = EV_X * np.sin(delta)
            P_m = 0.5 * Sn + (P_load if T2[k] >= 0.1 else 0.0)
            domega = (w0 / (2 * Hv_val * Sn)) * (P_m - P_e - D_damp * (omega - w0))
            omega += domega * dt2
            delta += (omega - w0) * dt2
            out.append((omega - w0) / w0 * 100)
        return np.array(out)

    freq_droop = sim_droop_mode(mp_droop, wf_droop)
    freq_match = sim_match_mode(Hv)

    # gran senal: doble de escalon para ver diferencia
    freq_droop_large = sim_droop_mode(mp_droop, wf_droop, P_load=2*P_step)
    freq_match_large = sim_match_mode(Hv, P_load=2*P_step)

    # (d) BESS: SOC(t) durante soporte de frecuencia
    dt3 = 0.1; T3 = np.arange(0, 12, dt3)
    E_batt = 0.5 * 3600e3   # 500 kWh en Joules
    SOC_init = 0.5
    Vdc_b = Vdc0; SOC = SOC_init; vdc_bess = []; soc_bess = []
    for k in range(len(T3)):
        P_supp = P_step  # soporte constante de 200 kW
        P_out  = EV_X * np.sin(np.arcsin(np.clip(P_supp / EV_X, -0.999, 0.999)))
        # descarga la bateria
        dSOC = -P_supp * dt3 / E_batt
        SOC  = max(0.0, SOC + dSOC)
        # cuando SOC=0, la bateria no puede mas: Vdc cae
        Vdc_b += (P_supp * SOC / max(SOC_init, 1e-3) - P_out) / (C_bus * Vdc_b) * dt3
        Vdc_b  = max(Vdc_b, 500.0)
        vdc_bess.append(Vdc_b)
        soc_bess.append(SOC * 100)

    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.0))
    ax = axes.ravel()

    # panel a — tabla analogia (como texto en axes)
    ax[0].axis("off")
    tabla = [
        ["Magnitud", "Máquina síncrona", "Matching control"],
        ["Inercia / capacidad",    "J  [kg·m²]",          "C  [F]"],
        ["Variable de velocidad",  "ω  [rad/s]",          "V_dc  [V]"],
        ["Energía almacenada",     "½·J·ω²  [J]",         "½·C·V_dc²  [J]"],
        ["Potencia mecánica",      "P_mec",                "P_in (generación)"],
        ["Potencia eléctrica",     "P_elec",               "P_out (red)"],
        ["Variable de ángulo",     "θ = ∫ω dt",            "θ = k·∫V_dc dt"],
        ["Inercia equivalente",    "H [s]",                "H_v = C·ω₀²/(2Sn·k²)"],
    ]
    y0 = 0.92; dy = 0.10
    for i, row in enumerate(tabla):
        style = dict(fontsize=9, va="top")
        bg = "#e8f0fe" if i == 0 else ("#f5f5f5" if i % 2 == 0 else "white")
        ax[0].add_patch(plt.Rectangle((0, y0 - (i+1)*dy), 1, dy,
                                       color=bg, transform=ax[0].transAxes, clip_on=False))
        for j, txt in enumerate(row):
            x = [0.01, 0.35, 0.68][j]
            fw = "bold" if i == 0 else "normal"
            ax[0].text(x, y0 - i*dy - 0.01, txt, transform=ax[0].transAxes,
                       fontweight=fw, **style)
    ax[0].set_title("(a) Analogía máquina síncrona ↔ matching control", fontsize=10)

    # panel b
    ax[1].plot(T, vdc_match, color=ACC, lw=2.2, label="matching (Vdc oscila)")
    ax[1].plot(T, vdc_reg,   color=OK,  lw=2,   label="PI clásico (Vdc regulado)")
    ax[1].axvline(0.1, color="#888", ls=":", lw=1)
    ax[1].axhline(Vdc0, color="#bbb", ls="--", lw=1)
    ax[1].set_xlabel("t [s]"); ax[1].set_ylabel("V_dc [V]")
    ax[1].set_title("(b) Respuesta de V_dc ante escalón de 200 kW")
    ax[1].legend(fontsize=8)

    # panel c
    ax[2].plot(T2, freq_droop,       color=ACC, lw=2,   ls="--", label="droop, 200 kW")
    ax[2].plot(T2, freq_match,       color=OK,  lw=2,   ls="--", label="matching, 200 kW")
    ax[2].plot(T2, freq_droop_large, color=BAD, lw=2,   label="droop, 400 kW")
    ax[2].plot(T2, freq_match_large, color=ACC, lw=2.2, label="matching, 400 kW")
    ax[2].axvline(0.1, color="#888", ls=":", lw=1)
    ax[2].set_xlabel("t [s]"); ax[2].set_ylabel("Δf/f₀ [%]")
    ax[2].set_title("(c) Droop vs matching: pequeña señal y gran señal")
    ax[2].legend(fontsize=8, ncol=2)

    # panel d
    ax3b = ax[3].twinx()
    ax[3].plot(T3, vdc_bess, color=ACC, lw=2.2, label="V_dc [V]")
    ax3b.plot(T3, soc_bess, color=OK, lw=2, ls="--", label="SOC [%]")
    ax[3].axhline(500, color=BAD, ls=":", lw=1.2); ax[3].text(0.5, 505, "V_dc mínimo", fontsize=8, color=BAD)
    idx_soc0 = next((k for k, s in enumerate(soc_bess) if s < 1.0), len(soc_bess)-1)
    ax[3].axvline(T3[idx_soc0], color=BAD, ls="--", lw=1.2)
    ax[3].text(T3[idx_soc0]+0.1, 620, "SOC=0%\n(inercia\ndesaparece)", fontsize=8, color=BAD)
    ax[3].set_xlabel("t [s]"); ax[3].set_ylabel("V_dc [V]", color=ACC)
    ax3b.set_ylabel("SOC [%]", color=OK)
    ax[3].set_title("(d) Matching + BESS: V_dc y SOC durante soporte de frecuencia")
    lines1, lab1 = ax[3].get_legend_handles_labels()
    lines2, lab2 = ax3b.get_legend_handles_labels()
    ax[3].legend(lines1+lines2, lab1+lab2, fontsize=8)

    fig.suptitle("Matching control: analogía, respuesta y comparativa droop", fontsize=13, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    _savefig(fig, "matching-control-analisis.png")


# ===================================================================== #
#  impedancia-virtual-analisis  (sin decorador @figura)
# ===================================================================== #
def _zvirt_extended():
    """4 paneles: diagrama bloques, zeta vs Xvirt, Bode Zo, caida tension vs Xvirt."""
    Sn   = 1e6         # VA
    EV_X0 = 500e3      # W/rad  (con X_linea)
    mp   = 1.571e-3    # rad/(s·W)
    wf   = 2*np.pi*10  # Hz
    Xline = 0.10       # pu reactancia de linea
    Xbase = 1.0        # pu base
    i_nom = 1.0        # pu corriente nominal

    # (a) Diagrama de bloques: axes con texto/patches
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.0))
    ax = axes.ravel()

    ax0 = ax[0]; ax0.set_xlim(0, 10); ax0.set_ylim(0, 6); ax0.axis("off")
    ax0.set_title("(a) Lazo de tensión con impedancia virtual", fontsize=10)
    # bloques
    def box(a, x, y, w, h, txt, color="#1f6feb", fc="#dce8ff"):
        a.add_patch(plt.Rectangle((x-w/2, y-h/2), w, h, color=fc, ec=color, lw=1.5))
        a.text(x, y, txt, ha="center", va="center", fontsize=9, color="#111")
    def arr(a, x0, y0, x1, y1):
        a.annotate("", xy=(x1,y1), xytext=(x0,y0),
                   arrowprops=dict(arrowstyle="->", color="#333", lw=1.5))

    box(ax0, 1.2, 3, 1.6, 0.9, "$v_{ref}$\n(consigna)", fc="#fffbe6", color="#e08e0b")
    box(ax0, 3.2, 3, 1.4, 0.9, "−$Z_v \\cdot i$\n(Xvirt)", fc="#ffe8e8", color=BAD)
    box(ax0, 5.5, 3, 1.8, 0.9, "Lazo\ntensión", fc="#dce8ff", color=ACC)
    box(ax0, 8.0, 3, 1.4, 0.9, "Planta\nLCL+red", fc="#e8ffe8", color=OK)
    # suma
    ax0.add_patch(plt.Circle((2.4, 3), 0.22, color="white", ec="#333", lw=1.5))
    ax0.text(2.4, 3, "+", ha="center", va="center", fontsize=10)
    arr(ax0, 2.02, 3, 2.18, 3); arr(ax0, 3.92, 3, 4.60, 3)
    arr(ax0, 6.40, 3, 7.30, 3)
    # realimentacion de corriente
    ax0.annotate("", xy=(3.2, 2.3), xytext=(8.0, 2.3),
                 arrowprops=dict(arrowstyle="->", color=BAD, lw=1.5))
    ax0.plot([8.0, 8.0, 3.2, 3.2], [3.0-0.45, 2.3, 2.3, 3.0-0.45], color=BAD, lw=1.5)
    ax0.text(5.6, 2.0, "realimentación $i$ (corriente medida)", fontsize=8, color=BAD, ha="center")
    ax0.text(2.4, 3.45, "−", fontsize=11, color=BAD, ha="center")
    arr(ax0, 3.20, 4.5, 2.40, 3.22)
    ax0.text(3.2, 4.7, "$Z_v \\cdot i$ resta de $v_{ref}$", fontsize=8, ha="center", color=BAD)
    ax0.text(5.0, 1.3, "$Z_{o,eff} = Z_{o,fis} + Z_v$  (sin disipar potencia)", fontsize=9,
             ha="center", color="#333", style="italic")

    # (b) zeta vs Xvirt
    Xv_pu = np.linspace(0, 0.18, 300)
    X_total = (Xline + Xv_pu) * Xbase  # pu, pero la Ks escala con 1/X_total
    Ks_arr = EV_X0 / (1 + Xv_pu / Xline)  # Ks ∝ 1/(X_total/X_linea)
    # modo de potencia: wn^2 = wf*mp*Ks,  zeta = wf/(2*wn)
    wn2 = wf * mp * Ks_arr; wn2 = np.maximum(wn2, 1e-9)
    zeta_v = wf / (2 * np.sqrt(wn2))

    ax[1].plot(Xv_pu, zeta_v, color=ACC, lw=2.5)
    ax[1].axhline(0.7, color=BAD, ls="--", lw=1.5, label="ζ = 0.7 (objetivo)")
    ax[1].axhline(0.5, color="#888", ls=":",  lw=1,   label="ζ = 0.5")
    idx_07 = np.argmin(np.abs(zeta_v - 0.7))
    ax[1].axvline(Xv_pu[idx_07], color=OK, ls="--", lw=1.2)
    ax[1].plot(Xv_pu[idx_07], 0.7, "o", color=OK, ms=8)
    ax[1].text(Xv_pu[idx_07]+0.002, 0.72, f"Xv={Xv_pu[idx_07]:.3f} pu", fontsize=8, color=OK)
    ax[1].set_xlabel("X_virt [pu]"); ax[1].set_ylabel("ζ  amortiguamiento")
    ax[1].set_title("(b) ζ del modo de potencia vs X_virtual")
    ax[1].legend(fontsize=8); ax[1].set_ylim(0, 1.5)

    # (c) Bode de impedancia de salida |Zo(jw)| simplificado
    f = np.logspace(-1, 3, 800); w = 2*np.pi*f
    L1 = 1.5e-3; C1 = 10e-6; L2 = 0.5e-3  # LCL tipico
    Lv = 8e-3   # inductancia virtual
    def Zo_tf(L1v, Cf, L2v, w_arr):
        # Zo ≈ jω(L1+L2) con resonancia LCL
        # modelo simplificado: Zo = jωL1 || (1/(jωCf) + jωL2)
        ZL1 = 1j*w_arr*L1v
        ZCf = 1/(1j*w_arr*Cf + 1e-12)
        ZL2 = 1j*w_arr*L2v
        Z_branch = ZCf + ZL2
        return np.abs(ZL1 * Z_branch / (ZL1 + Z_branch))
    Zo_sin = Zo_tf(L1, C1, L2, w)
    Zo_con = Zo_tf(L1+Lv, C1, L2, w)
    ax[2].loglog(f, Zo_sin, color=BAD, lw=2,   label="sin X_virt  (inductancia real)")
    ax[2].loglog(f, Zo_con, color=ACC, lw=2.2, label="con X_virt = 8 mH")
    ax[2].set_xlabel("f [Hz]"); ax[2].set_ylabel("|Z_o| [Ω]")
    ax[2].set_title("(c) Impedancia de salida del GFM: sin y con X_virtual")
    ax[2].legend(fontsize=8)

    # (d) caida de tension en PCC vs Xvirt
    # ΔV ≈ Xv * I_nom / V0  (en pu, I=1pu, V0=1pu)
    dV_pu = Xv_pu * i_nom  # caida en pu
    lim_5pct = 0.05

    ax[3].plot(Xv_pu, dV_pu * 100, color=ACC, lw=2.5, label="ΔV_PCC (sin feedforward)")
    ax[3].axhline(5.0, color=BAD, ls="--", lw=1.5, label="límite ΔV = 5%")
    # con feedforward compensa casi toda la caida
    ax[3].plot(Xv_pu, dV_pu * 100 * 0.08, color=OK, lw=2, ls="--", label="con feedforward de corriente")
    idx_lim = np.argmin(np.abs(dV_pu - lim_5pct))
    ax[3].axvline(Xv_pu[idx_lim], color="#888", ls=":", lw=1.2)
    ax[3].plot(Xv_pu[idx_lim], 5.0, "o", color=BAD, ms=8)
    ax[3].text(Xv_pu[idx_lim]+0.002, 5.3, f"Xv={Xv_pu[idx_lim]:.2f} pu\n(límite sin FF)", fontsize=8, color=BAD)
    # marcar la X_virt optima (que cumple zeta=0.7)
    ax[3].axvline(Xv_pu[idx_07], color=OK, ls="--", lw=1.2)
    ax[3].text(Xv_pu[idx_07]+0.001, 2.5, f"Xv necesario\npara ζ=0.7", fontsize=8, color=OK)
    ax[3].set_xlabel("X_virt [pu]"); ax[3].set_ylabel("ΔV_PCC [%]")
    ax[3].set_title("(d) Caída de tensión en PCC vs X_virtual")
    ax[3].legend(fontsize=8); ax[3].set_ylim(0, 20)

    fig.suptitle("Impedancia virtual: efecto sobre amortiguamiento, Zo y regulación de tensión",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    _savefig(fig, "impedancia-virtual-analisis.png")


# ===================================================================== #
# ===================================================================== #
#  fault-ride-through-analisis  (sin decorador @figura)
# ===================================================================== #
def _frt_extended():
    """4 paneles: (a) curva LVRT P.O.12.3, (b) id/iq durante hueco 50%,
    (c) Vpcc con/sin soporte reactivo, (d) angulo GFL vs GFM hueco profundo."""
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.0))
    (a1, a2), (a3, a4) = axes

    # (a) Curva LVRT del P.O. 12.3: V(t)
    t_lvrt = np.array([-100, 0, 0, 150, 150, 500, 3000])
    v_lvrt = np.array([1.0, 1.0, 0.0, 0.0, 0.8, 0.8, 1.0])
    a1.plot(t_lvrt, v_lvrt, color=BAD, lw=2.5, label="envolvente LVRT")
    a1.fill_between(t_lvrt, v_lvrt, 1.15, color=OK, alpha=0.13, label="zona segura")
    a1.axhline(0.85, color=ACC2, ls="--", lw=1.2)
    a1.text(1700, 0.87, "umbral detección 0.85 pu", color=ACC2, fontsize=8)
    a1.text(75, 0.38, "0 pu / 150 ms\n(obligatorio aguantar)", color=BAD, fontsize=8, ha="center")
    a1.text(350, 0.71, "recuperar 0.8 pu\nen 500 ms", color=BAD, fontsize=8, ha="center")
    a1.set_xlabel("t [ms]  (t=0: inicio del hueco)")
    a1.set_ylabel("$V_{pcc}$ [pu]")
    a1.set_title("(a) Curva LVRT del P.O. 12.3")
    a1.set_ylim(-0.05, 1.2); a1.legend(fontsize=8)

    # (b) id(t) e iq(t) durante hueco 50% con k=4, imax=1.1 pu
    Ts = 1e-4; T = np.arange(-0.1, 0.6, Ts)
    k_frt = 4.0; Imax = 1.1
    Vpcc_b = np.where(T < 0, 1.0, np.where(T < 0.15, 0.5,
             np.where(T < 0.25, 0.5 + (T-0.15)/0.1*0.35, 0.85)))
    dV = np.clip(1.0 - Vpcc_b, 0, 1)
    iq_star = np.clip(k_frt * dV, 0, Imax)
    id_star = np.sqrt(np.maximum(Imax**2 - iq_star**2, 0))
    # Suavizar con filtro de primer orden (tau=5 ms)
    tau = 50; iq_f = np.zeros_like(iq_star); id_f = np.zeros_like(id_star)
    iq_f[0] = iq_star[0]; id_f[0] = id_star[0]
    for n in range(1, len(T)):
        iq_f[n] = iq_f[n-1] + (iq_star[n] - iq_f[n-1]) / tau
        id_f[n] = id_f[n-1] + (id_star[n] - id_f[n-1]) / tau
    Tms = T * 1e3
    a2.plot(Tms, id_f, color=ACC, lw=2.0, label="$i_d^*$ (activa)")
    a2.plot(Tms, iq_f, color=BAD, lw=2.0, label="$i_q^*$ (reactiva)")
    a2.axhline(Imax, color="#aaa", ls=":", lw=1.2)
    a2.text(200, Imax + 0.02, "$I_{max}=1.1$ pu", fontsize=8, color="#555")
    a2.axvline(0, color="#888", ls="--", lw=1); a2.axvline(150, color="#888", ls="--", lw=1)
    a2.text(75, 0.05, "FRT activo", fontsize=8, ha="center", color="#555")
    a2.set_xlabel("t [ms]"); a2.set_ylabel("corriente [pu]")
    a2.set_title("(b) Prioridad reactiva: $k=4$, $V_{pcc}=0.5$ pu, $I_{max}=1.1$ pu")
    a2.legend(fontsize=8); a2.set_xlim(-100, 600)

    # (c) Vpcc(t) con y sin soporte reactivo FRT
    Xred = 0.1  # pu
    t_c = np.linspace(0, 0.5, 2000)
    Vgrid = np.where(t_c < 0.05, 1.0, np.where(t_c < 0.35, 0.5, 0.5 + (t_c - 0.35)/0.05 * 0.4))
    Vgrid = np.clip(Vgrid, 0, 1.0)
    # Sin soporte: Vpcc ≈ Vgrid
    Vpcc_sin = Vgrid.copy()
    # Con soporte: iq_soporte = k*(1-Vgrid), Vpcc += Xred*iq
    dV_c = np.clip(1.0 - Vgrid, 0, 1)
    iq_sup = np.clip(k_frt * dV_c, 0, Imax)
    Vpcc_con = np.clip(Vgrid + Xred * iq_sup, 0, 1.15)
    t_c_ms = t_c * 1e3
    a3.plot(t_c_ms, Vpcc_sin, color=BAD, lw=2.0, ls="--", label="sin soporte FRT")
    a3.plot(t_c_ms, Vpcc_con, color=OK, lw=2.0, label="con soporte FRT ($k=4$)")
    a3.axhline(0.85, color=ACC2, ls=":", lw=1.2)
    a3.text(420, 0.87, "umbral 0.85 pu", fontsize=8, color=ACC2)
    a3.set_xlabel("t [ms]"); a3.set_ylabel("$V_{pcc}$ [pu]")
    a3.set_title("(c) $V_{pcc}$ con/sin soporte reactivo ($X_{red}=0.1$ pu)")
    a3.legend(fontsize=8); a3.set_xlim(0, 500)

    # (d) Comparativa GFL vs GFM: angulo durante hueco profundo 0.1 pu
    dt = 5e-5; t_d = np.arange(0, 0.5, dt)
    # GFL con PLL: simular lazo PI de PLL durante hueco
    Kp_pll, Ki_pll = 50.0, 1000.0
    theta_gfl = np.zeros_like(t_d); omega_gfl = np.ones_like(t_d) * 2*np.pi*50
    xi_pll = 0.0
    theta_ref = 2*np.pi*50 * t_d
    for i in range(1, len(t_d)):
        Vpcc_d = 0.1 if 0.05 < t_d[i] < 0.25 else 1.0
        # error en eje q: angulo PLL trata de seguir tensión perturbada
        Vq_err = -Vpcc_d * np.sin(theta_gfl[i-1] - theta_ref[i-1]) * 0.3  # perturbación
        omega_gfl[i] = 2*np.pi*50 + Kp_pll * Vq_err + xi_pll
        xi_pll += Ki_pll * Vq_err * dt
        theta_gfl[i] = theta_gfl[i-1] + omega_gfl[i] * dt
    delta_gfl = np.degrees(theta_gfl - theta_ref)
    # GFM: angle mantiene via droop, oscila pero no pierde sincronía
    delta_gfm = np.zeros_like(t_d)
    omega_gfm = np.ones_like(t_d) * 2*np.pi*50
    dw_gfm = 0.0
    for i in range(1, len(t_d)):
        Pe_gfm = 0.5 * np.sin(np.radians(delta_gfm[i-1]))
        Pm_gfm = 0.5 if 0.05 < t_d[i] < 0.25 else 0.5
        Vgfm = 0.1 if 0.05 < t_d[i] < 0.25 else 1.0
        damp = 5.0
        dw_gfm += ((Pm_gfm - Pe_gfm * Vgfm) - damp * dw_gfm) / 2.0 * dt
        omega_gfm[i] = 2*np.pi*50 + dw_gfm * 2*np.pi*50
        delta_gfm[i] = delta_gfm[i-1] + dw_gfm * 2*np.pi*50 * dt
    delta_gfm_deg = np.degrees(delta_gfm)
    t_d_ms = t_d * 1e3
    a4.plot(t_d_ms, delta_gfl, color=BAD, lw=2.0, label="GFL: ángulo PLL (deriva)")
    a4.plot(t_d_ms, delta_gfm_deg, color=OK, lw=2.0, label="GFM: ángulo droop (oscila, no pierde sync)")
    a4.axvspan(50, 250, color=BAD, alpha=0.08)
    a4.text(150, delta_gfl.max()*0.7, "hueco 0.1 pu", fontsize=8, ha="center", color=BAD)
    a4.set_xlabel("t [ms]"); a4.set_ylabel("Δδ [°]")
    a4.set_title("(d) GFL vs GFM: desviación angular durante hueco profundo")
    a4.legend(fontsize=8)

    fig.suptitle("Fault Ride-Through: análisis completo", fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    _savefig(fig, "fault-ride-through-analisis.png")


# ===================================================================== #
#  filtro-notch-analisis  (sin decorador @figura)
# ===================================================================== #
def _notch_extended():
    """4 paneles: (a) Bode notch Q variable, (b) lazo corriente sin/con notch,
    (c) notch 100Hz para rizado Vdc, (d) comparativa Kad vs notch vs ambos."""
    from scipy import signal as sig

    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.0))
    (a1, a2), (a3, a4) = axes

    fres = 3404.0  # Hz, resonancia del LCL del proyecto 01
    wres = 2*np.pi*fres

    # (a) Bode notch para Q=1,5,10,20 a f0=3404 Hz
    f = np.logspace(2, 4.5, 2000)
    w = 2*np.pi*f
    for Q, c, ls in [(1, ACC, "-"), (5, OK, "--"), (10, BAD, "-."), (20, ACC2, ":")]:
        zp = 1.0 / (2*Q)
        zz = zp * 0.01  # casi ideal: profundo
        num = [1, 2*zz*wres, wres**2]
        den = [1, 2*zp*wres, wres**2]
        sys_n = sig.TransferFunction(num, den)
        _, mag_n, _ = sig.bode(sys_n, w)
        a1.semilogx(f, mag_n, color=c, lw=2.0, ls=ls, label=f"Q={Q}")
    a1.axvline(fres, color="#bbb", ls=":", lw=1)
    a1.text(fres*1.05, -5, f"$f_{{res}}={fres:.0f}$ Hz", fontsize=8, color="#555")
    a1.set_xlabel("frecuencia [Hz]"); a1.set_ylabel("|N| [dB]")
    a1.set_title("(a) Notch: profundidad y ancho vs Q")
    a1.legend(fontsize=8); a1.set_xlim(100, 20000)

    # (b) Lazo de corriente: sin notch vs con notch a 3404 Hz
    # Parámetros del LCL del proyecto 01
    L1, L2, Cf = 1.8e-3, 0.6e-3, 4.4e-6
    Kpi = 6.0; Ti = 0.005  # controlador PI corriente
    def lcl_loop(f_arr, with_notch=False, Q_val=10):
        w_arr = 2*np.pi*f_arr
        s = 1j * w_arr
        # FDT del LCL: planta de corriente i2/vi
        Zlcl = s*L1 * (1 + s*s*L2*Cf) / (1 + s*s*(L1+L2)*Cf) + s*L2
        G_plant = 1.0 / Zlcl
        G_pi = Kpi * (1 + 1.0/(Ti*s))
        if with_notch:
            zp_v = 1.0/(2*Q_val); zz_v = zp_v*0.01
            G_notch_v = (wres**2 - w_arr**2 + 2j*zz_v*wres*w_arr) / \
                        (wres**2 - w_arr**2 + 2j*zp_v*wres*w_arr)
        else:
            G_notch_v = np.ones_like(s)
        L_loop = G_pi * G_notch_v * G_plant
        return 20*np.log10(np.abs(L_loop))
    f_b = np.logspace(1, 4.3, 1500)
    mag_sin = lcl_loop(f_b, False)
    mag_con = lcl_loop(f_b, True, Q_val=10)
    a2.semilogx(f_b, mag_sin, color=BAD, lw=2.0, label="sin notch")
    a2.semilogx(f_b, mag_con, color=OK, lw=2.0, label="con notch Q=10")
    a2.axvline(fres, color="#bbb", ls=":", lw=1)
    a2.axhline(0, color="#aaa", ls="--", lw=1)
    a2.set_xlabel("frecuencia [Hz]"); a2.set_ylabel("|L| [dB]")
    a2.set_title("(b) Lazo de corriente: pico LCL suprimido por notch")
    a2.legend(fontsize=8); a2.set_xlim(10, 20000); a2.set_ylim(-80, 80)

    # (c) Notch para rizado 100 Hz en realimentación de tensión Vdc
    f_c = np.logspace(0, 3.5, 1500)
    w_c = 2*np.pi*f_c
    f0_rz = 100.0; w0_rz = 2*np.pi*f0_rz
    # Lazo de tensión con PI
    Kpv, Tiv = 0.5, 0.02
    Cdc = 50e-3; Vdc0 = 700.0
    Gplant_v = 1.0 / (1j*w_c*Cdc)  # simplificado: integrador
    Gpi_v = Kpv * (1 + 1.0/(Tiv*1j*w_c))
    # Rizado Vdc a 100 Hz en la realimentación
    zp_rz = 0.1; zz_rz = 0.001
    G_notch_100 = ((w0_rz**2 - w_c**2) + 2j*zz_rz*w0_rz*w_c) / \
                  ((w0_rz**2 - w_c**2) + 2j*zp_rz*w0_rz*w_c)
    # |Vdc| en la realimentación: sin vs con notch (respuesta del lazo cerrado al rizado)
    mag_vdc_sin = 20*np.log10(np.abs(Gpi_v * Gplant_v / (1 + Gpi_v * Gplant_v)) * 1.0 + 1e-12)
    mag_vdc_con = 20*np.log10(np.abs(Gpi_v * G_notch_100 * Gplant_v /
                               (1 + Gpi_v * G_notch_100 * Gplant_v)) * 1.0 + 1e-12)
    a3.semilogx(f_c, mag_vdc_sin, color=BAD, lw=2.0, label="sin notch 100 Hz")
    a3.semilogx(f_c, mag_vdc_con, color=OK, lw=2.0, label="con notch 100 Hz")
    a3.axvline(100, color=ACC2, ls="--", lw=1.2)
    a3.text(110, -5, "100 Hz\n(2ω)", fontsize=8, color=ACC2)
    a3.set_xlabel("frecuencia [Hz]"); a3.set_ylabel("|$H_{cl}$| [dB]")
    a3.set_title("(c) Notch 100 Hz: rechazo del rizado 2ω en bus DC monofásico")
    a3.legend(fontsize=8); a3.set_xlim(1, 3000)

    # (d) Comparativa: Kad vs notch vs ambos para PM del lazo de corriente
    def pm_estimate(Kad=0, use_notch=False, Q_val=10):
        """Estima PM cruzando 0 dB y leyendo la fase."""
        f_d = np.logspace(1, 4.3, 4000)
        w_d = 2*np.pi*f_d
        s_d = 1j*w_d
        # Planta con Kad (amortiguamiento activo en paralelo con Cf)
        if Kad > 0:
            Zcf = 1.0/(s_d*Cf)
            Zdamp = Kad * Zcf / (Kad + Zcf)
            Zbranch = s_d*L2 + Zdamp
            Zin = s_d*L1 + Zbranch*Zcf/(Zbranch+Zcf) * (s_d*L2+Zcf)/(s_d*L2+Zcf)
            G_plant_d = Zcf/(s_d*L2+Zcf) / (s_d*L1 + (s_d*L2+Zcf)*Zcf/(s_d*L2+Zcf))
        else:
            s2 = s_d**2
            G_plant_d = 1.0 / (s_d*L1*(1 + s2*L2*Cf)/(1 + s2*(L1+L2)*Cf) + s_d*L2)
        G_pi_d = Kpi * (1 + 1.0/(Ti*s_d))
        if use_notch:
            zp_d = 1.0/(2*Q_val); zz_d = zp_d*0.01
            G_notch_d = ((wres**2 - w_d**2) + 2j*zz_d*wres*w_d) / \
                        ((wres**2 - w_d**2) + 2j*zp_d*wres*w_d)
        else:
            G_notch_d = 1.0
        L_d = G_pi_d * G_notch_d * G_plant_d
        mag_d = 20*np.log10(np.abs(L_d) + 1e-20)
        phase_d = np.angle(L_d, deg=True)
        # Cruce de 0 dB
        idx = np.where(np.diff(np.sign(mag_d)))[0]
        if len(idx) == 0:
            return float('nan')
        ic = idx[0]
        fc = f_d[ic]
        ph_c = np.interp(fc, f_d, phase_d)
        return 180 + ph_c

    configs = [
        ("sin Kad, sin notch", 0, False, BAD),
        ("Kad=6Ω, sin notch", 6, False, ACC),
        ("sin Kad, notch Q=10", 0, True, OK),
        ("Kad=6Ω + notch Q=10", 6, True, ACC2),
    ]
    labels = [c[0] for c in configs]
    pms = [pm_estimate(c[1], c[2]) for c in configs]
    colors_bar = [c[3] for c in configs]
    x_pos = np.arange(len(labels))
    bars = a4.bar(x_pos, pms, color=colors_bar, width=0.6, alpha=0.85)
    a4.axhline(45, color="#888", ls="--", lw=1.2)
    a4.text(3.5, 46.5, "PM=45° (criterio)", fontsize=8, ha="right", color="#555")
    for bar, pm in zip(bars, pms):
        if not np.isnan(pm):
            a4.text(bar.get_x() + bar.get_width()/2, pm + 1.5, f"{pm:.1f}°",
                    ha="center", fontsize=9, fontweight="bold")
    a4.set_xticks(x_pos); a4.set_xticklabels(labels, fontsize=8, rotation=10)
    a4.set_ylabel("Margen de Fase [°]"); a4.set_ylim(0, 90)
    a4.set_title("(d) Comparativa Kad vs notch vs ambos")

    fig.suptitle("Filtro notch: análisis para el LCL del proyecto 01", fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    _savefig(fig, "filtro-notch-analisis.png")


# ===================================================================== #
#  interaccion-pll-red-debil-analisis  (sin decorador @figura)
# ===================================================================== #
def _pllweak_extended():
    """4 paneles: (a) Bode del lazo de interaccion L_int para SCR variable,
    (b) SCR_crit vs fpll cuadratico, (c) Re{Zqq} para fpll=30 y 100Hz,
    (d) simulacion Vpcc e id para SCR=3 inestable vs estable."""
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.0))
    (a1, a2), (a3, a4) = axes

    fpll_ref = 100.0  # Hz
    wpll = 2*np.pi*fpll_ref
    Kp_pll = wpll / np.sqrt(2); Ki_pll = Kp_pll**2 / 2  # amort 1/√2

    # (a) Bode del lazo de interaccion L_int para SCR=2,5,10, fpll=100 Hz
    f_a = np.logspace(0, 3, 2000)
    w_a = 2*np.pi*f_a
    s_a = 1j*w_a
    V_pcc_nom = 1.0; I_nom = 1.0  # pu
    # H_PLL(s) = (Kp_pll*s + Ki_pll) / (s^2 + Kp_pll*s + Ki_pll)
    H_pll = (Kp_pll*s_a + Ki_pll) / (s_a**2 + Kp_pll*s_a + Ki_pll)
    # ∂i/∂θ = I_nom (corriente activa con eje d alineado con V_pcc)
    dI_dtheta = I_nom
    for SCR, c, ls in [(2, BAD, "-"), (5, ACC, "--"), (10, OK, "-.")]:
        Xg = V_pcc_nom**2 / (SCR * 1.0)  # reactancia de red en pu (Sbase=1)
        L_int = Xg * dI_dtheta * H_pll
        mag_lint = 20*np.log10(np.abs(L_int) + 1e-20)
        a1.semilogx(f_a, mag_lint, color=c, lw=2.0, ls=ls, label=f"SCR={SCR}")
    a1.axhline(0, color="#aaa", ls=":", lw=1.2)
    a1.axvline(fpll_ref, color=ACC2, ls=":", lw=1)
    a1.text(fpll_ref*1.05, 15, f"$f_{{PLL}}={fpll_ref:.0f}$ Hz", fontsize=8, color=ACC2)
    a1.set_xlabel("frecuencia [Hz]"); a1.set_ylabel("|$L_{int}$| [dB]")
    a1.set_title("(a) Lazo de interacción $L_{int}$ vs SCR ($f_{PLL}=100$ Hz)")
    a1.legend(fontsize=8); a1.set_xlim(1, 1000)

    # (b) SCR_crit vs fpll (curva cuadrática): SCR_crit ∝ (fpll/f0)^2
    fpll_arr = np.array([15, 20, 30, 40, 50, 70, 100, 130, 150, 170])
    # Relación aproximada: SCR_crit ~ 0.36*(fpll/30)^2 * f_factor
    scr_crit_arr = 0.38 * (fpll_arr / 30)**2
    scr_crit_arr = np.clip(scr_crit_arr, 0.2, 20)
    f_fit = np.linspace(15, 180, 300)
    scr_fit = 0.38 * (f_fit / 30)**2
    a2.plot(f_fit, scr_fit, color=ACC, lw=2.0, ls="--", label="modelo: $\\propto f_{PLL}^2$")
    a2.plot(fpll_arr, scr_crit_arr, "o", color=ACC, ms=7)
    # Marcar diseños de referencia
    for fp, sc, col in [(30, 0.38, OK), (100, 0.38*(100/30)**2, BAD)]:
        a2.axvline(fp, color=col, ls=":", lw=1.2)
        a2.axhline(sc, color=col, ls=":", lw=1.2)
        a2.plot(fp, sc, "s", color=col, ms=9, zorder=5)
        a2.text(fp + 3, sc + 0.3, f"$f_{{PLL}}$={fp} Hz\nSCR$_{{crit}}$={sc:.1f}", fontsize=8, color=col)
    a2.fill_between(f_fit, scr_fit, 0, color=BAD, alpha=0.10, label="región inestable")
    a2.fill_between(f_fit, scr_fit, 20, color=OK, alpha=0.08, label="región estable")
    a2.set_xlabel("$f_{PLL}$ [Hz]"); a2.set_ylabel("SCR crítico")
    a2.set_title("(b) $SCR_{crit} \\propto f_{PLL}^2$: más rápida la PLL, mayor SCR requerido")
    a2.legend(fontsize=8); a2.set_ylim(0, 16); a2.set_xlim(10, 185)

    # (c) Re{Zqq(jω)} para fpll=30 Hz y 100 Hz
    f_c = np.linspace(1, 250, 2000)
    w_c = 2*np.pi*f_c
    R0 = 1.0
    for fp, c, lbl in [(30, OK, "$f_{PLL}=30$ Hz (lenta)"), (100, BAD, "$f_{PLL}=100$ Hz (rápida)")]:
        wp = 2*np.pi*fp
        # Modelo: Re{Zqq} = R0*(1 - 2*wp^2/(wp^2+w^2)) de la resistencia negativa
        ReZ = R0 * (1 - 2*wp**2/(wp**2 + w_c**2))
        a3.plot(f_c, ReZ, color=c, lw=2.0, label=lbl)
    a3.axhline(0, color="#888", lw=1.2)
    a3.axhspan(-1.1, 0, color=BAD, alpha=0.07)
    a3.text(180, -0.45, "Re{$Z_{qq}$}<0\n(no pasivo)", color=BAD, fontsize=8, ha="center")
    a3.set_xlabel("frecuencia [Hz]"); a3.set_ylabel("Re{$Z_{qq}$} [pu]")
    a3.set_title("(c) Resistencia negativa: banda de Re{$Z_{qq}$}<0 se ensancha con $f_{PLL}$")
    a3.legend(fontsize=8); a3.set_ylim(-1.1, 1.1)

    # (d) Simulacion: Vpcc e id para SCR=3, fpll=100Hz (inestable) vs fpll=30Hz (estable)
    dt_d = 5e-5; t_d = np.arange(0, 0.5, dt_d); N = len(t_d)
    SCR_sim = 3.0; Vbase = 1.0
    Xg_sim = Vbase**2 / SCR_sim
    Lg_sim = Xg_sim / (2*np.pi*50)

    def sim_pll(fpll_sim):
        Kpp = 2*np.pi*fpll_sim / np.sqrt(2)
        Kip = Kpp**2 / 2
        theta_pll = 0.0; omega_pll = 2*np.pi*50; xi_pi = 0.0
        Vd_pcc = 1.0; Vq_pcc = 0.0
        id_out = 0.0; iq_out = 0.0
        theta_grid = 0.0
        Vpcc_arr = np.zeros(N); id_arr = np.zeros(N)
        for i in range(N):
            theta_grid += 2*np.pi*50 * dt_d
            # GFL inyecta corriente en dq según su PLL
            id_ref = 0.7; iq_ref = 0.0
            # Transformar a abc/alfa: perturbacion de Vpcc por la corriente
            delta_theta = theta_pll - theta_grid
            pert = Xg_sim * id_ref * np.sin(delta_theta) * 0.5
            Vq_pcc = -Xg_sim * id_ref * np.cos(delta_theta) * 0.5 + pert
            Vpcc_mag = np.sqrt((1.0 - Xg_sim * iq_ref)**2 + (Xg_sim * id_ref)**2)
            # PLL
            e_pll = Vq_pcc
            omega_pll = 2*np.pi*50 + Kpp * e_pll + xi_pi
            xi_pi += Kip * e_pll * dt_d
            theta_pll += omega_pll * dt_d
            Vpcc_arr[i] = Vpcc_mag; id_arr[i] = id_ref + 0.1*np.sin(2*np.pi*fpll_sim*0.5*t_d[i]) * (i/N)
        return Vpcc_arr, id_arr

    # Simplificación educativa: mostrar oscilaciones crecientes vs amortiguadas
    t_ms = t_d * 1e3
    # SCR=3 con fpll=100 Hz → inestable: oscilaciones que crecen
    env_unst = 1.0 + 0.04 * np.exp(3.5 * t_d) * np.where(t_d > 0.05, 1.0, 0)
    env_unst = np.clip(env_unst, 0, 1.5)
    Vpcc_unst = 1.0 + (env_unst - 1.0) * np.sin(2*np.pi*12*t_d)
    id_unst = 0.7 + (env_unst - 1.0) * 0.5 * np.sin(2*np.pi*12*t_d + 0.4)
    # SCR=3 con fpll=30 Hz → estable: transitorio amortiguado
    Vpcc_st = 1.0 + 0.08 * np.exp(-8*t_d) * np.sin(2*np.pi*8*t_d)
    id_st = 0.7 + 0.05 * np.exp(-8*t_d) * np.sin(2*np.pi*8*t_d + 0.3)
    a4.plot(t_ms, Vpcc_unst, color=BAD, lw=1.5, label="$f_{PLL}=100$ Hz (inestable)")
    a4.plot(t_ms, Vpcc_st, color=OK, lw=1.5, label="$f_{PLL}=30$ Hz (estable)")
    a4.axhline(1.0, color="#aaa", ls=":", lw=1)
    a4.text(420, 1.35, "oscilaciones crecientes", color=BAD, fontsize=8, ha="right")
    a4.set_xlabel("t [ms]"); a4.set_ylabel("$V_{pcc}$ [pu]")
    a4.set_title("(d) SCR=3: $V_{pcc}$ inestable (rápida) vs estable (lenta)")
    a4.legend(fontsize=8); a4.set_xlim(0, 500); a4.set_ylim(0.3, 1.6)

    fig.suptitle("Interacción PLL–red débil: análisis completo", fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    _savefig(fig, "interaccion-pll-red-debil-analisis.png")


# ===================================================================== #
#  potencia-instantanea-dq  extended  (sin decorador)
# ===================================================================== #
def _potdq_extended():
    """4 paneles: (a) potencias de fase y suma, (b) p y q en αβ,
    (c) rizado con desequilibrio 10%, (d) trayectoria id*,iq* escalón P*."""
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    a1, a2, a3, a4 = axes.flat

    # --- (a) potencias instantáneas de fase y suma ---
    t = np.linspace(0, 2/50, 1000)
    V = 690/np.sqrt(3)*np.sqrt(2)   # pico de fase para 690 V ll
    I = 836.0; phi = np.arccos(0.95)
    ia = I*np.cos(2*np.pi*50*t - phi)
    ib = I*np.cos(2*np.pi*50*t - 2*np.pi/3 - phi)
    ic = I*np.cos(2*np.pi*50*t + 2*np.pi/3 - phi)
    va = V*np.cos(2*np.pi*50*t)
    vb = V*np.cos(2*np.pi*50*t - 2*np.pi/3)
    vc = V*np.cos(2*np.pi*50*t + 2*np.pi/3)
    pa = va*ia; pb = vb*ib; pc = vc*ic
    p3 = pa + pb + pc
    t_ms = t*1e3
    a1.plot(t_ms, pa/1e3, color=ACC, lw=1.2, ls="--", label="$p_a(t)$")
    a1.plot(t_ms, pb/1e3, color=OK, lw=1.2, ls="--", label="$p_b(t)$")
    a1.plot(t_ms, pc/1e3, color=ACC2, lw=1.2, ls="--", label="$p_c(t)$")
    a1.plot(t_ms, p3/1e3, color="#222", lw=2.2, label=r"$p_{3\phi}=$ cte")
    a1.axhline(np.mean(p3)/1e3, color=BAD, ls=":", lw=1.2, label=f"P={np.mean(p3)/1e3:.1f} kW")
    a1.set_xlabel("t [ms]"); a1.set_ylabel("p [kW]")
    a1.set_title("(a) Potencias instantáneas de fase y su suma")
    a1.legend(fontsize=8, ncol=2)

    # --- (b) p y q en αβ ---
    theta = 2*np.pi*50*t
    va_ab = V*np.cos(theta); vb_ab = V*np.sin(theta)
    ia_ab = I*np.cos(theta - phi); ib_ab = I*np.sin(theta - phi)
    p_ab = va_ab*ia_ab + vb_ab*ib_ab
    q_ab = vb_ab*ia_ab - va_ab*ib_ab
    a2.plot(t_ms, p_ab/1e3, color=ACC, lw=1.8, label=r"$p(ab)=v alpha i alpha+v beta i beta$")
    a2.plot(t_ms, q_ab/1e3, color=BAD, lw=1.8, label=r"$q(ab)=v beta i alpha - v alpha i beta$")
    a2.axhline(np.mean(p_ab)/1e3, color=ACC, ls=":", lw=1)
    a2.axhline(np.mean(q_ab)/1e3, color=BAD, ls=":", lw=1)
    a2.set_xlabel("t [ms]"); a2.set_ylabel("p, q [kW / kVAr]")
    a2.set_title("(b) Potencia en ab: Akagi (V=690V ll, fp=0.95)")
    a2.legend(fontsize=9)

    # --- (c) rizado con desequilibrio 10% ---
    Vpos = V; Vneg = 0.10*V
    phi_neg = np.pi/6
    va_u = Vpos*np.cos(theta) + Vneg*np.cos(-theta + phi_neg)
    vb_u = Vpos*np.sin(theta) + Vneg*np.sin(-theta + phi_neg)
    ia_u = I*np.cos(theta - phi); ib_u = I*np.sin(theta - phi)
    p_u = va_u*ia_u + vb_u*ib_u
    a3.plot(t_ms, p3/1e3, color=OK, lw=1.8, label="Equilibrado (sin rizado)")
    a3.plot(t_ms, p_u/1e3, color=BAD, lw=1.8, label="Desequilibrio 10% (V-)")
    a3.axhline(np.mean(p3)/1e3, color=OK, ls=":", lw=1)
    a3.set_xlabel("t [ms]"); a3.set_ylabel(r"$p_{3phi}$ [kW]")
    a3.set_title("(c) Rizado a 2w con desequilibrio del 10% de V-")
    a3.legend(fontsize=9)
    a3.fill_between(t_ms, np.mean(p3)/1e3, p_u/1e3, alpha=0.15, color=BAD)

    # --- (d) trayectoria id*(t), iq*(t) escalón P* ---
    tau = 0.005
    t_s = np.linspace(0, 0.05, 500)
    vd = 690/np.sqrt(3)*np.sqrt(2)
    Pstar = 500e3; Qstar = 200e3
    id_ref = (2/3)*Pstar/vd
    iq_ref = -(2/3)*Qstar/vd
    id_resp = id_ref*(1 - np.exp(-t_s/tau))
    iq_resp = iq_ref*np.ones_like(t_s)
    a4.plot(t_s*1e3, id_resp, color=ACC, lw=2, label="$i_d^*(t)$ (escalon P*=500kW)")
    a4.plot(t_s*1e3, iq_resp, color=BAD, lw=2, ls="--", label="$i_q^*(t)$ (Q*=200kVAr)")
    a4.axhline(id_ref, color=ACC, ls=":", lw=1, label=f"$i_d^*$={id_ref:.0f} A")
    a4.axhline(iq_ref, color=BAD, ls=":", lw=1, label=f"$i_q^*$={iq_ref:.0f} A")
    a4.set_xlabel("t [ms]"); a4.set_ylabel("corriente [A]")
    a4.set_title("(d) Respuesta $i_d$, $i_q$ al escalon de $P^*$ (t=5ms)")
    a4.legend(fontsize=8)
    a4.set_xlim(0, 50)

    fig.suptitle("Potencia instantánea dq: análisis completo", fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _savefig(fig, "potencia-instantanea-dq-analisis.png")


# ===================================================================== #
#  maquina-induccion  extended  (sin decorador)
# ===================================================================== #
def _induc_extended():
    """4 paneles: (a) curva T(wr) sin control vs FOC, (b) modelo FOC,
    (c) respuesta dinámica FOC, (d) efecto variacion Rr."""
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    a1, a2, a3, a4 = axes.flat

    ws = 2*np.pi*50.0; Sn = 500e3; Vn = 690/np.sqrt(3)
    Zbase = Vn**2 / (Sn/3)
    Rr_pu = 0.008; Rs_pu = 0.01; sigma = 0.05; Lm_pu = 3.0
    Rr = Rr_pu*Zbase; Rs = Rs_pu*Zbase
    Xs = sigma*Zbase; Xr = sigma*Zbase
    V1_rms = Vn
    Tbase = Sn/ws

    # --- (a) curva par-velocidad ---
    s_arr = np.linspace(-0.5, 1.0, 1000)
    s_arr[np.abs(s_arr) < 1e-6] = 1e-6
    Te_arr = (3*V1_rms**2*(Rr/s_arr)) / (ws*((Rs + Rr/s_arr)**2 + (Xs+Xr)**2))
    nr = ws*(1 - s_arr)/(2*np.pi)*60
    a1.plot(nr, Te_arr/Tbase, color=BAD, lw=2, label="Sin control (arranque directo)")
    ns_rpm = ws/(2*np.pi)*60
    nr_base = np.linspace(0, ns_rpm*0.98, 300)
    nr_fw = np.linspace(ns_rpm*0.98, ns_rpm*1.5, 200)
    Te_max_pu = np.max(Te_arr/Tbase)
    a1.plot(nr_base, np.ones(300)*Te_max_pu*0.85, color=OK, lw=2, label="FOC: par constante")
    Te_fw = Te_max_pu*0.85*(ns_rpm*0.98)/nr_fw
    a1.plot(nr_fw, Te_fw, color=OK, lw=2, ls="--", label="FOC: flux weakening")
    a1.axvline(ns_rpm, color="#aaa", ls=":", lw=1.2)
    a1.text(ns_rpm+30, Te_max_pu*0.3, "$n_s$", fontsize=9, color="#666")
    a1.set_xlabel("velocidad [rpm]"); a1.set_ylabel("$T_e$ [pu]")
    a1.set_title("(a) Curva par-velocidad: arranque directo vs FOC")
    a1.legend(fontsize=8); a1.set_xlim(-200, 2200)

    # --- (b) modelo FOC ---
    ax = a2; ax.set_axis_off()
    ax.set_xlim(0, 10); ax.set_ylim(0, 6)
    ax.annotate("", xy=(2.5, 4.8), xytext=(0.5, 4.8), arrowprops=dict(arrowstyle="-|>", color=ACC, lw=1.8))
    ax.text(0.3, 4.8, "$i_{sd}^*$", va="center", fontsize=10, color=ACC)
    ax.add_patch(plt.Rectangle((2.5, 4.2), 2.5, 1.2, fill=True, facecolor="#e8f0ff", edgecolor=ACC, lw=1.5))
    ax.text(3.75, 4.8, r"$\tau_r\dot{\psi}_{rd}+\psi_{rd}=L_m i_{sd}$", ha="center", va="center", fontsize=8.5)
    ax.annotate("", xy=(7.0, 4.8), xytext=(5.0, 4.8), arrowprops=dict(arrowstyle="-|>", color=ACC, lw=1.8))
    ax.text(7.1, 4.8, "$\\psi_{rd}$", va="center", fontsize=10, color=ACC)
    ax.text(5.8, 5.3, "lazo FLUJO (lento, $\\tau_r$)", fontsize=8, color=ACC, ha="center")
    ax.annotate("", xy=(2.5, 2.8), xytext=(0.5, 2.8), arrowprops=dict(arrowstyle="-|>", color=BAD, lw=1.8))
    ax.text(0.3, 2.8, "$i_{sq}^*$", va="center", fontsize=10, color=BAD)
    ax.add_patch(plt.Rectangle((2.5, 2.2), 2.5, 1.2, fill=True, facecolor="#ffe8e8", edgecolor=BAD, lw=1.5))
    ax.text(3.75, 2.8, r"$T_e=\frac{3}{2}P\frac{L_m}{L_r}\psi_{rd}i_{sq}$", ha="center", va="center", fontsize=8.5)
    ax.annotate("", xy=(7.0, 2.8), xytext=(5.0, 2.8), arrowprops=dict(arrowstyle="-|>", color=BAD, lw=1.8))
    ax.text(7.1, 2.8, "$T_e$", va="center", fontsize=10, color=BAD)
    ax.text(5.8, 3.2, "lazo PAR (rapido, $\\alpha_c$)", fontsize=8, color=BAD, ha="center")
    ax.text(5.0, 1.5, "Separacion: $\\alpha_c \\gg 1/\\tau_r$  lazos desacoplados", fontsize=8.5, ha="center")
    ax.set_title("(b) Modelo FOC: lazo de flujo y lazo de par")

    # --- (c) respuesta dinámica FOC ---
    tau_r = 0.1; alpha_c = 2*np.pi*100
    t_d = np.linspace(0, 0.5, 2000)
    t0 = 0.05
    Te_resp = np.where(t_d < t0, 0.0, 1.0*(1 - np.exp(-(t_d-t0)*alpha_c)))
    isq_resp = Te_resp
    isd = 1.0*np.ones_like(t_d)
    psi_rd = np.ones_like(t_d)
    a3.plot(t_d*1e3, Te_resp, color=BAD, lw=2, label="$T_e(t)$ [pu]")
    a3.plot(t_d*1e3, isq_resp, color=ACC2, lw=1.8, ls="--", label="$i_{sq}(t)$ [pu]")
    a3.plot(t_d*1e3, isd, color=ACC, lw=1.8, ls=":", label="$i_{sd}(t)$ [pu]")
    a3.plot(t_d*1e3, psi_rd, color="#888", lw=1.2, ls="-.", label="$\\psi_{rd}(t)$ [pu]")
    a3.axvline(t0*1e3, color="#aaa", ls=":", lw=1)
    a3.set_xlabel("t [ms]"); a3.set_ylabel("magnitud [pu]")
    a3.set_title("(c) Respuesta dinamica FOC: escalon de $T_e^*$")
    a3.legend(fontsize=8); a3.set_xlim(0, 500)

    # --- (d) efecto variacion Rr ---
    Rr_nom_pu = Rr_pu
    isq0 = 0.5
    tau_r_nom = Lm_pu / (Rr_nom_pu * ws)
    omega_slip_real = (Lm_pu * isq0) / tau_r_nom
    t_err = np.linspace(0, 0.3, 500)
    for factor, color, lbl in [(1.0, OK, "$R_r$ nominal"), (1.2, BAD, "$R_r$+20% (caliente)"),
                                (0.8, ACC, "$R_r$-20% (frio)")]:
        tau_r_est = Lm_pu / (factor * Rr_nom_pu * ws)
        omega_slip_est = (Lm_pu * isq0) / tau_r_est
        delta_theta = (omega_slip_est - omega_slip_real) * t_err
        a4.plot(t_err*1e3, np.degrees(delta_theta), color=color, lw=2, label=lbl)
    a4.axhline(0, color="#aaa", ls=":", lw=1)
    a4.set_xlabel("t [ms]"); a4.set_ylabel("Error angulo FOC [deg]")
    a4.set_title("(d) Desalineacion FOC por variacion de $R_r$")
    a4.legend(fontsize=9)

    fig.suptitle("Maquina de induccion: FOC y dinamica", fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _savefig(fig, "maquina-induccion-analisis.png")


# ===================================================================== #
#  microrred-hibrida-ac-dc  extended  (sin decorador)
# ===================================================================== #
def _hybrid_extended():
    """4 paneles: (a) arquitectura, (b) flujos de potencia dia solar,
    (c) Vdc ante escalon con/sin AD, (d) f(t) tras desconexion de red."""
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    a1, a2, a3, a4 = axes.flat

    # --- (a) diagrama de arquitectura ---
    ax = a1; ax.set_axis_off(); ax.set_xlim(0, 10); ax.set_ylim(0, 7)
    ax.add_patch(plt.Rectangle((0.3, 4.8), 4.0, 0.4, facecolor="#d0e8ff", edgecolor=ACC, lw=2))
    ax.text(2.3, 5.4, "Bus AC  400 V / 50 Hz", ha="center", fontsize=9, color=ACC, fontweight="bold")
    ax.add_patch(plt.Rectangle((5.7, 4.8), 4.0, 0.4, facecolor="#ffe8cc", edgecolor=ACC2, lw=2))
    ax.text(7.7, 5.4, "Bus DC  700 V", ha="center", fontsize=9, color=ACC2, fontweight="bold")
    ax.add_patch(plt.Rectangle((4.1, 4.6), 1.5, 0.8, facecolor="#f5e8ff", edgecolor="#9b59b6", lw=1.5))
    ax.text(4.85, 5.0, "ILC\n150kW", ha="center", va="center", fontsize=8, color="#9b59b6")
    ax.text(0.7, 4.3, "Red/Gen", fontsize=8, ha="center", color="#444")
    ax.annotate("", xy=(0.9, 4.8), xytext=(0.9, 4.4), arrowprops=dict(arrowstyle="-|>", color="#444", lw=1.5))
    ax.text(2.3, 4.3, "Carga AC\n25kW", fontsize=8, ha="center", color="#444")
    ax.annotate("", xy=(2.3, 4.8), xytext=(2.3, 4.4), arrowprops=dict(arrowstyle="-|>", color="#444", lw=1.5))
    ax.text(6.4, 4.3, "PV\n60kWp", fontsize=8, ha="center", color=OK)
    ax.annotate("", xy=(6.4, 4.8), xytext=(6.4, 4.4), arrowprops=dict(arrowstyle="-|>", color=OK, lw=1.5))
    ax.text(7.7, 4.3, "BESS\n50kWh", fontsize=8, ha="center", color=BAD)
    ax.annotate("", xy=(7.7, 4.8), xytext=(7.7, 4.4), arrowprops=dict(arrowstyle="<|-|>", color=BAD, lw=1.5))
    ax.text(9.2, 4.3, "DC\n75kW", fontsize=8, ha="center", color="#444")
    ax.annotate("", xy=(9.2, 4.8), xytext=(9.2, 4.4), arrowprops=dict(arrowstyle="-|>", color="#444", lw=1.5))
    ax.set_title("(a) Arquitectura: microrred hibrida 100 kW")

    # --- (b) flujos de potencia durante un dia ---
    t_h = np.linspace(0, 24, 1000)
    P_pv = 60e3*np.clip(np.sin(np.pi*(t_h-6)/12)**1.5 * (t_h > 6) * (t_h < 18), 0, None)
    P_load = 75e3 + 10e3*np.sin(2*np.pi*t_h/24 + np.pi)
    P_bess = np.clip(P_pv - P_load, -30e3, 30e3)
    P_grid = P_load - P_pv - P_bess
    a2.plot(t_h, P_pv/1e3, color=OK, lw=2, label="$P_{PV}$")
    a2.plot(t_h, P_load/1e3, color="#333", lw=2, ls="--", label="$P_{carga}$")
    a2.plot(t_h, P_bess/1e3, color=BAD, lw=1.8, label="$P_{BESS}$")
    a2.plot(t_h, P_grid/1e3, color=ACC, lw=1.8, ls="-.", label="$P_{red}$")
    a2.axhline(0, color="#bbb", lw=0.8)
    a2.set_xlabel("hora del dia"); a2.set_ylabel("P [kW]")
    a2.set_title("(b) Flujos de potencia: dia solar tipico")
    a2.legend(fontsize=8, ncol=2); a2.set_xlim(0, 24)

    # --- (c) Vdc ante escalon de carga ---
    Vdc0 = 700.0; dP = 50e3
    L_cable = 0.5e-3; C_dc = 5e-3; R_cable = 0.02
    t_tr = np.linspace(0, 0.05, 2000)
    omega_n = 1/np.sqrt(L_cable*C_dc)
    zeta_no_ad = R_cable/2*np.sqrt(C_dc/L_cable)
    Vdc_dip = dP/Vdc0
    dVdc_noad = (Vdc_dip/omega_n)*np.exp(-zeta_no_ad*omega_n*t_tr)*np.sin(omega_n*t_tr)
    zeta_ad = 0.7
    dVdc_ad = (Vdc_dip/omega_n)*np.exp(-zeta_ad*omega_n*t_tr)*np.sin(omega_n*t_tr)
    a3.plot(t_tr*1e3, Vdc0 - dVdc_noad*80, color=BAD, lw=2, label="Sin amortiguamiento activo")
    a3.plot(t_tr*1e3, Vdc0 - dVdc_ad*80, color=OK, lw=2, label="Con amortiguamiento activo")
    a3.axhline(Vdc0, color="#aaa", ls=":", lw=1, label=f"$V_{{dc}}^*$={Vdc0:.0f} V")
    a3.set_xlabel("t [ms]"); a3.set_ylabel("$V_{dc}$ [V]")
    a3.set_title("(c) Bus DC: escalon +50 kW, con/sin AD")
    a3.legend(fontsize=9); a3.set_xlim(0, 50)

    # --- (d) f(t) tras desconexion de red ---
    t_sw = np.linspace(0, 10, 2000)
    t_disc = 1.0
    kdroop = 0.04; P_imbalance = 25e3; Sn_g = 200e3
    dp_pu = P_imbalance/Sn_g
    df_droop = -kdroop*dp_pu*50.0
    tau_prim = 0.3; tau_sec = 2.0
    f_prim = np.where(t_sw < t_disc, 50.0,
                      50.0 + df_droop*(1 - np.exp(-(t_sw-t_disc)/tau_prim)))
    f_sec = np.where(t_sw < t_disc, 50.0,
                     50.0 + df_droop*(1 - np.exp(-(t_sw-t_disc)/tau_prim))
                     - df_droop*(1 - np.exp(-(t_sw-t_disc)/tau_sec)))
    a4.plot(t_sw, f_prim, color=ACC, lw=2, label="Solo primario (droop)")
    a4.plot(t_sw, f_sec, color=OK, lw=2, ls="--", label="Primario + secundario")
    a4.axvline(t_disc, color="#aaa", ls=":", lw=1.5)
    a4.text(t_disc+0.1, 50.06, "Desconexion\nred", fontsize=8, color="#666")
    a4.axhline(50.0, color="#ccc", lw=0.8)
    a4.set_xlabel("t [s]"); a4.set_ylabel("f [Hz]")
    a4.set_title("(d) Frecuencia tras desconexion: droop y restauracion")
    a4.legend(fontsize=9); a4.set_xlim(0, 10)

    fig.suptitle("Microrred hibrida AC/DC: analisis completo", fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _savefig(fig, "microrred-hibrida-ac-dc-analisis.png")


# ===================================================================== #
#  generador-sincrono  extended  (sin decorador)
# ===================================================================== #
def _sg_extended():
    """4 paneles: (a) circuito equiv dq, (b) curva de capabilidad,
    (c) swing equation H=2,5,10s, (d) GS vs VSM."""
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    a1, a2, a3, a4 = axes.flat

    Xd = 1.05; Xq = 0.65; H_nom = 5.0; w0 = 2*np.pi*50; D = 5.0
    E = 1.1; V = 1.0

    # --- (a) diagrama circuito equivalente dq ---
    ax = a1; ax.set_axis_off(); ax.set_xlim(0, 10); ax.set_ylim(0, 8)
    ax.text(5.0, 7.4, "Circuito equivalente dq del generador sincrono", ha="center",
            fontsize=9.5, fontweight="bold")
    ax.text(0.5, 6.5, "eje d:", fontsize=9, color=ACC, fontweight="bold")
    ax.annotate("", xy=(2.0, 6.2), xytext=(0.8, 6.2), arrowprops=dict(arrowstyle="-|>", color=ACC, lw=1.5))
    ax.add_patch(plt.Rectangle((2.0, 5.8), 1.6, 0.8, facecolor="#e8f0ff", edgecolor=ACC, lw=1.5))
    ax.text(2.8, 6.2, "$L_d$, $R_s$", ha="center", va="center", fontsize=9)
    ax.annotate("", xy=(5.0, 6.2), xytext=(3.6, 6.2), arrowprops=dict(arrowstyle="-|>", color=ACC, lw=1.5))
    ax.text(4.1, 6.55, "$+\\omega_r\\psi_q$", fontsize=8, color=BAD)
    ax.add_patch(plt.Rectangle((5.0, 5.8), 1.8, 0.8, facecolor="#fff0e0", edgecolor=ACC2, lw=1.5))
    ax.text(5.9, 6.2, "$L_{md}i_{fd}=E_q'$", ha="center", va="center", fontsize=8.5)
    ax.annotate("", xy=(7.2, 6.2), xytext=(6.8, 6.2), arrowprops=dict(arrowstyle="-|>", color=ACC, lw=1.5))
    ax.text(7.3, 6.2, "$v_d$", fontsize=9, color=ACC)
    ax.text(0.5, 4.5, "eje q:", fontsize=9, color=BAD, fontweight="bold")
    ax.annotate("", xy=(2.0, 4.2), xytext=(0.8, 4.2), arrowprops=dict(arrowstyle="-|>", color=BAD, lw=1.5))
    ax.add_patch(plt.Rectangle((2.0, 3.8), 1.6, 0.8, facecolor="#ffe8e8", edgecolor=BAD, lw=1.5))
    ax.text(2.8, 4.2, "$L_q$, $R_s$", ha="center", va="center", fontsize=9)
    ax.annotate("", xy=(5.0, 4.2), xytext=(3.6, 4.2), arrowprops=dict(arrowstyle="-|>", color=BAD, lw=1.5))
    ax.text(4.1, 4.55, "$-\\omega_r\\psi_d$", fontsize=8, color=ACC)
    ax.text(5.1, 4.2, "$v_q$", fontsize=9, color=BAD)
    ax.add_patch(plt.Rectangle((1.5, 1.8), 7.0, 1.4, facecolor="#f0fff0", edgecolor=OK, lw=1.5))
    ax.text(5.0, 2.5,
            "$T_e = \\psi_d i_q - \\psi_q i_d$\n"
            "$\\psi_d=-L_d i_d+L_{md}i_{fd},\\quad\\psi_q=-L_q i_q$",
            ha="center", va="center", fontsize=9)
    ax.set_title("(a) Circuito dq y par electromagnetico")

    # --- (b) curva de capabilidad ---
    Q_arr = np.linspace(-0.8, 0.8, 400)
    P_arm = np.sqrt(np.clip(1.0**2 - Q_arr**2, 0, None))
    Ef_max = 1.3; cx = -V**2/Xd
    delta_arr = np.linspace(0, np.pi, 400)
    r_exc_max = Ef_max*V/Xd
    P_exc_max = r_exc_max*np.sin(delta_arr)
    Q_exc_max = r_exc_max*np.cos(delta_arr) + cx
    Ef_min = 0.3; r_exc_min = Ef_min*V/Xd
    P_exc_min = r_exc_min*np.sin(delta_arr)
    Q_exc_min = r_exc_min*np.cos(delta_arr) + cx
    a2.plot(Q_arr, P_arm, color=ACC, lw=2, label="Limite armadura")
    a2.plot(Q_exc_max, P_exc_max, color=OK, lw=2, label=f"Excit. max ($E_f$={Ef_max}pu)")
    a2.plot(Q_exc_min, P_exc_min, color=BAD, lw=2, ls="--", label=f"Excit. min ($E_f$={Ef_min}pu)")
    a2.scatter([0.2], [0.7], color="red", s=60, zorder=5, label="Pto op. (P=0.7, Q=0.2)")
    a2.axhline(0, color="#bbb", lw=0.8); a2.axvline(0, color="#bbb", lw=0.8)
    a2.set_xlabel("Q [pu]"); a2.set_ylabel("P [pu]")
    a2.set_title("(b) Curva de capabilidad: limites P-Q")
    a2.legend(fontsize=7.5); a2.set_xlim(-1.0, 1.0); a2.set_ylim(-0.1, 1.2)

    # --- (c) swing equation ---
    t_sw = np.linspace(0, 5.0, 5000)
    dP_pu = 0.3
    for H_val, color, lbl in [(2.0, BAD, "$H=2$ s"), (5.0, ACC, "$H=5$ s"), (10.0, OK, "$H=10$ s")]:
        delta0 = np.arcsin(0.7*Xd/(E*V))
        Ks = E*V/Xd*np.cos(delta0)
        omega_n_sw = np.sqrt(Ks*w0/(2*H_val))
        zeta_sw = D*w0/(4*H_val*omega_n_sw)
        omega_d = omega_n_sw*np.sqrt(max(1 - zeta_sw**2, 0.01))
        A = -dP_pu*w0/(2*H_val)/omega_n_sw**2
        dw = (A*omega_n_sw/omega_d)*np.exp(-zeta_sw*omega_n_sw*t_sw)*np.sin(omega_d*t_sw)
        a3.plot(t_sw, 50.0 + dw/(2*np.pi), color=color, lw=2, label=lbl)
    a3.axhline(50.0, color="#bbb", ls=":", lw=1)
    a3.set_xlabel("t [s]"); a3.set_ylabel("f [Hz]")
    a3.set_title("(c) Ecuacion de swing: escalon dP=0.3 pu")
    a3.legend(fontsize=9)

    # --- (d) GS real vs VSM ---
    t_c = np.linspace(0, 4.0, 2000); dP_c = 0.2
    for H_v, D_v, color, lbl, ls in [
            (5.0, 5.0, ACC, "Maquina sincrona real", "-"),
            (5.25, 4.75, OK, "VSM (parametros equiv.)", "--")]:
        delta0_c = np.arcsin(0.7*Xd/(E*V))
        Ks_c = E*V/Xd*np.cos(delta0_c)
        wn = np.sqrt(Ks_c*w0/(2*H_v))
        zeta_c = D_v*w0/(4*H_v*wn)
        wd_c = wn*np.sqrt(max(1 - zeta_c**2, 0.01))
        A_c = -dP_c*w0/(2*H_v)/wn**2
        dw_c = (A_c*wn/wd_c)*np.exp(-zeta_c*wn*t_c)*np.sin(wd_c*t_c)
        a4.plot(t_c, 50.0 + dw_c/(2*np.pi), color=color, lw=2, ls=ls, label=lbl)
    a4.axhline(50.0, color="#bbb", ls=":", lw=1)
    a4.set_xlabel("t [s]"); a4.set_ylabel("f [Hz]")
    a4.set_title("(d) GS real vs VSM: equivalencia dinamica")
    a4.legend(fontsize=9)

    fig.suptitle("Generador sincrono: modelo dq y dinamica", fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _savefig(fig, "generador-sincrono-analisis.png")


# ===================================================================== #
#  lugar-raices-analisis  (sin decorador @figura)
# ===================================================================== #
def _rlocus_extended():
    """4 paneles: (a) lugar clasico G=K/[s(s+2)(s+4)], (b) modo de potencia droop,
    (c) diseno con linea zeta=0.7, (d) verificacion vs autovalores."""
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 10.0))
    (a1, a2), (a3, a4) = axes

    def rlocus_roots(poles, K_vec):
        den = np.poly(poles)
        roots_all = []
        for K in K_vec:
            num_pad = np.zeros(len(den))
            num_pad[-1] = K
            char = den + num_pad
            roots_all.append(np.roots(char))
        return np.array(roots_all)

    # (a) Lugar clasico G = K / [s(s+2)(s+4)]
    poles_a = [0.0, -2.0, -4.0]
    K_a = np.linspace(0, 80, 1200)
    roots_a = rlocus_roots(poles_a, K_a)
    n_a = 3
    sigma_a = sum(poles_a) / n_a
    ang_a = [(2*k+1)*180.0/n_a for k in range(n_a)]

    a1.axvspan(0, 2, color=BAD, alpha=0.07)
    for r in roots_a.T:
        a1.scatter(r.real, r.imag, s=1.5, color=ACC, alpha=0.4)
    a1.scatter(poles_a, [0]*3, marker="x", s=100, color=BAD, lw=2.5, zorder=6,
               label="polos lazo abierto (K=0)")
    for ang in ang_a:
        rad = np.radians(ang)
        a1.annotate("", xy=(sigma_a + 4.5*np.cos(rad), 4.5*np.sin(rad)),
                    xytext=(sigma_a, 0),
                    arrowprops=dict(arrowstyle="-", color="#aaa", lw=1.2, ls="--"))
    a1.scatter([sigma_a], [0], marker="D", s=60, color=OK, zorder=7,
               label=f"centroide sigma={sigma_a:.1f}")
    a1.axvline(0, color="k", lw=1.2); a1.axhline(0, color="#bbb", lw=0.6)
    a1.set_xlim(-7, 2); a1.set_ylim(-6, 6)
    a1.set_xlabel("Re(s)"); a1.set_ylabel("Im(s)")
    a1.set_title("(a) Lugar G=K/[s(s+2)(s+4)]\nasint. 60 deg, 180 deg, 300 deg desde centroide -2")
    a1.legend(fontsize=8, loc="upper left"); a1.grid(True, alpha=0.3)

    # (b) Modo de potencia droop: L(s) = mp*Ks / [s(s+wf)], wf=2pi*5 Hz
    wf = 2*np.pi*5.0
    poles_b = [0.0, -wf]
    K_b = np.linspace(0, 2500, 1200)
    roots_b = rlocus_roots(poles_b, K_b)
    sigma_b = (0 + (-wf)) / 2

    a2.axvspan(0, 20, color=BAD, alpha=0.07)
    for r in roots_b.T:
        a2.scatter(r.real, r.imag, s=1.5, color=ACC2, alpha=0.4)
    a2.scatter([0, -wf], [0, 0], marker="x", s=100, color=BAD, lw=2.5, zorder=6,
               label="polos: 0, -wf (wf=2pi5)")
    a2.scatter([sigma_b], [0], marker="D", s=60, color=OK, zorder=7,
               label=f"centroide sigma={sigma_b:.1f}")
    a2.axvline(0, color="k", lw=1.2); a2.axhline(0, color="#bbb", lw=0.6)
    a2.set_xlim(-50, 20); a2.set_ylim(-80, 80)
    a2.set_xlabel("Re(s)"); a2.set_ylabel("Im(s)")
    a2.set_title("(b) Modo de potencia droop\nL(s)=mp*Ks/[s(s+wf)], variando mp*Ks")
    a2.legend(fontsize=8, loc="upper left"); a2.grid(True, alpha=0.3)

    # (c) Diseno: linea zeta=0.7 y punto de cruce
    zeta_obj = 0.7
    ang_zeta = np.degrees(np.arccos(zeta_obj))
    wn_vec = np.linspace(0, 80, 200)
    line_re = -zeta_obj * wn_vec
    line_im =  np.sqrt(1 - zeta_obj**2) * wn_vec

    a3.axvspan(0, 20, color=BAD, alpha=0.07)
    for r in roots_b.T:
        a3.scatter(r.real, r.imag, s=1.5, color=ACC2, alpha=0.3)
    a3.plot(line_re,  line_im, color=OK, lw=2, ls="--",
            label=f"zeta={zeta_obj} (+/-{ang_zeta:.1f} deg)")
    a3.plot(line_re, -line_im, color=OK, lw=2, ls="--")
    # En 2 polos s^2+wf*s+K=0: zeta=wf/2/sqrt(K) -> K_design=(wf/2/zeta)^2
    K_design = (wf/2/zeta_obj)**2
    wn_design = np.sqrt(K_design)
    re_design = -zeta_obj * wn_design
    im_design = np.sqrt(1-zeta_obj**2) * wn_design
    a3.scatter([re_design, re_design], [im_design, -im_design],
               color=BAD, s=100, zorder=8,
               label=f"diseno: K={K_design:.0f}, wn={wn_design:.1f}")
    a3.axvline(0, color="k", lw=1.2); a3.axhline(0, color="#bbb", lw=0.6)
    a3.set_xlim(-50, 20); a3.set_ylim(-80, 80)
    a3.set_xlabel("Re(s)"); a3.set_ylabel("Im(s)")
    Ks_val = 500e3
    a3.set_title(f"(c) Diseno zeta=0.7 -> K=mp*Ks={K_design:.0f}\n(Ks=500 kW/rad -> mp={K_design/Ks_val*1000:.3f}e-3)")
    a3.legend(fontsize=8, loc="upper left"); a3.grid(True, alpha=0.3)

    # (d) Verificacion vs autovalores
    Ks = 500e3
    mp_vec = np.linspace(0, 2e-3, 60)
    eig_re, eig_im, mp_c = [], [], []
    for mp in mp_vec:
        K_loop = mp * Ks
        A = np.array([[0, 1], [-K_loop, -wf]])
        for ev in np.linalg.eigvals(A):
            eig_re.append(ev.real); eig_im.append(ev.imag); mp_c.append(mp*1e3)

    sc = a4.scatter(eig_re, eig_im, c=mp_c, cmap="plasma", s=20, zorder=5)
    fig.colorbar(sc, ax=a4, label="mp [x1e-3]")
    mp_design = K_design / Ks
    a4.scatter([re_design, re_design], [im_design, -im_design],
               color=OK, s=100, zorder=9, marker="*",
               label=f"mp={mp_design*1e3:.3f}e-3")
    a4.plot(line_re,  line_im, color=BAD, lw=1.8, ls="--", label="zeta=0.7")
    a4.plot(line_re, -line_im, color=BAD, lw=1.8, ls="--")
    a4.axvline(0, color="k", lw=1.2); a4.axhline(0, color="#bbb", lw=0.6)
    a4.set_xlim(-50, 20); a4.set_ylim(-80, 80)
    a4.set_xlabel("Re(s)"); a4.set_ylabel("Im(s)")
    a4.set_title("(d) Verificacion: autovalores de A(mp)\nconfirman zeta=0.7 en el punto de diseno")
    a4.legend(fontsize=8, loc="upper left"); a4.grid(True, alpha=0.3)

    fig.suptitle("Lugar de las raices: analisis completo del modo de potencia droop",
                 fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _savefig(fig, "lugar-raices-analisis.png")


# ===================================================================== #
#  muestreo-aliasing-analisis  (sin decorador @figura)
# ===================================================================== #
def _aliasing_extended():
    """4 paneles: (a) espectro con/sin aliasing, (b) filtro AA Bode,
    (c) ZOH senal escalonada, (d) PM vs Ts."""
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.0))
    (a1, a2), (a3, a4) = axes

    # (a) Espectro con y sin aliasing
    fs = 10e3
    fmax_ok = 3e3
    fmax_bad = 7e3
    f_vec = np.linspace(0, 15e3, 2000)
    nyquist = fs / 2

    def rect_spec(f, fc, amp=1.0):
        return amp * (np.abs(f) <= fc).astype(float)

    spec_ok  = rect_spec(f_vec, fmax_ok) + rect_spec(f_vec - fs, fmax_ok)*0.5 \
                                         + rect_spec(f_vec + fs, fmax_ok)*0.5
    spec_bad = rect_spec(f_vec, fmax_bad) + rect_spec(f_vec - fs, fmax_bad)*0.5 \
                                          + rect_spec(f_vec + fs, fmax_bad)*0.5

    a1.axvspan(0, nyquist/1e3, color=OK, alpha=0.10,
               label=f"banda base [0, fs/2={nyquist/1e3:.0f} kHz]")
    a1.plot(f_vec/1e3, spec_ok,  color=ACC,  lw=2.5,
            label=f"OK: senal {fmax_ok/1e3:.0f} kHz < fs/2")
    a1.plot(f_vec/1e3, spec_bad, color=BAD,  lw=2.5, ls="--",
            label=f"Aliasing: senal {fmax_bad/1e3:.0f} kHz > fs/2")
    a1.axvline(nyquist/1e3, color="#888", ls=":", lw=1.5)
    a1.text(nyquist/1e3+0.1, 0.85, f"Nyquist\n{nyquist/1e3:.0f} kHz", fontsize=8, color="#555")
    a1.set_xlabel("frecuencia [kHz]"); a1.set_ylabel("amplitud [pu]")
    a1.set_title(f"(a) Espectro muestreado a fs={fs/1e3:.0f} kHz\nreplicas solapan si senal > Nyquist")
    a1.legend(fontsize=8); a1.set_xlim(0, 15); a1.set_ylim(-0.05, 1.15)

    # (b) Filtro antialiasing Bode: Butterworth 2do orden, fc=0.4*fs
    fc_aa = 0.4 * fs
    wc_aa = 2*np.pi*fc_aa
    sys_aa = signal.TransferFunction([wc_aa**2], [1, np.sqrt(2)*wc_aa, wc_aa**2])
    f_bode = np.logspace(2, 4.5, 1000)
    w_bode = 2*np.pi*f_bode
    _, mag_aa, phase_aa = signal.bode(sys_aa, w_bode)
    wc_lazo = 2*np.pi*750
    _, mag_wc, ph_wc = signal.bode(sys_aa, [wc_lazo])

    a2b = a2.twinx()
    a2.semilogx(f_bode/1e3, mag_aa, color=ACC, lw=2.5, label="filtro AA (Butterworth 2)")
    a2.axvline(nyquist/1e3, color=BAD, ls="--", lw=1.5, label=f"Nyquist {nyquist/1e3:.0f} kHz")
    a2.axvline(fc_aa/1e3,   color=OK,  ls="--", lw=1.5, label=f"fc_AA={fc_aa/1e3:.0f} kHz")
    a2.axvline(0.75, color=ACC2, ls=":", lw=1.5, label="wc lazo (750 Hz)")
    a2b.semilogx(f_bode/1e3, phase_aa, color=ACC, lw=1.5, ls="-.", alpha=0.6)
    a2b.set_ylabel("fase [deg]", color="#888"); a2b.tick_params(axis="y", colors="#888")
    a2b.axhline(ph_wc[0], color=ACC2, ls=":", lw=1, alpha=0.8)
    a2b.text(0.12, ph_wc[0]+3, f"phi={ph_wc[0]:.0f} deg en 750 Hz", fontsize=8, color=ACC2)
    a2.set_xlabel("frecuencia [kHz]"); a2.set_ylabel("|H_AA| [dB]")
    a2.set_title("(b) Filtro antialiasing: Bode\ncompromiso fc vs retardo de fase en la banda de control")
    a2.legend(fontsize=8, loc="lower left"); a2.set_xlim(0.1, 30); a2.grid(True, which="both", alpha=0.3)

    # (c) ZOH: senal escalon muestreada y retenida
    Ts_zoh = 1/fs
    t_cont = np.linspace(0, 6*Ts_zoh, 1000)
    t_samp = np.arange(0, 6*Ts_zoh, Ts_zoh)
    ref = np.ones_like(t_cont); ref[t_cont < 1.5*Ts_zoh] = 0.0
    y_samp = np.interp(t_samp, t_cont, ref)

    def zoh_recon(t, t_s, y_s, Ts_r):
        out = np.zeros_like(t)
        for i, ts_val in enumerate(t_s):
            mask = (t >= ts_val) & (t < ts_val + Ts_r)
            out[mask] = y_s[i]
        return out

    y_zoh = zoh_recon(t_cont, t_samp, y_samp, Ts_zoh)
    a3.plot(t_cont*1e6, ref, color="#bbb", lw=1.5, ls="--", label="senal continua")
    a3.step(t_samp*1e6, y_samp, where="post", color=ACC, lw=2.5, label="ZOH (retencion)")
    a3.plot(t_samp*1e6, y_samp, "o", color=BAD, ms=7, zorder=6, label="muestras")
    a3.annotate("", xy=(1.5*Ts_zoh*1e6 + Ts_zoh*1e6*0.5, 0.5),
                xytext=(1.5*Ts_zoh*1e6, 0.5),
                arrowprops=dict(arrowstyle="<->", color=ACC2, lw=1.5))
    a3.text(1.5*Ts_zoh*1e6 + Ts_zoh*1e6*0.15, 0.55, "Ts/2", fontsize=9, color=ACC2)
    a3.set_xlabel("t [us]"); a3.set_ylabel("amplitud [pu]")
    a3.set_title(f"(c) ZOH: muestreo y retencion (Ts={Ts_zoh*1e6:.0f} us)\nretardo medio efectivo = Ts/2")
    a3.legend(fontsize=8); a3.set_ylim(-0.1, 1.3)

    # (d) PM vs Ts
    L_d = 2e-3
    wc_d = 2*np.pi*750
    Ts_d_vec = np.array([50, 100, 150, 200, 250, 300]) * 1e-6

    def pm_1order(Ts_i):
        Td = 1.5 * Ts_i
        Kp_i = L_d * wc_d
        Ls = (Kp_i / (L_d * 1j*wc_d)) * np.exp(-1j*wc_d*Td)
        return 180 + np.degrees(np.angle(Ls))

    pm_d = np.array([pm_1order(Ts_i) for Ts_i in Ts_d_vec])
    a4.plot(Ts_d_vec*1e6, pm_d, color=ACC, lw=2.5, marker="o", ms=7)
    a4.axhline(45, color=BAD, ls="--", lw=1.5, label="PM min 45 deg")
    a4.axhline(60, color=OK,  ls="--", lw=1.5, label="PM objetivo 60 deg")
    a4.fill_between(Ts_d_vec*1e6, pm_d, 45,
                    where=(pm_d < 45), color=BAD, alpha=0.2, label="PM insuficiente")
    a4.set_xlabel("Ts [us]"); a4.set_ylabel("PM [deg]")
    a4.set_title("(d) PM vs Ts (retardo 1.5*Ts, wc=2pi*750 Hz)\nTs mayor consume margen de fase")
    a4.legend(fontsize=8); a4.grid(True, alpha=0.3)

    fig.suptitle("Muestreo y aliasing: analisis completo", fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _savefig(fig, "muestreo-aliasing-analisis.png")


# ===================================================================== #
#  transformada-z-analisis  (sin decorador @figura)
# ===================================================================== #
def _ztransform_extended():
    """4 paneles: (a) mapeo s->z con curvas iso-zeta, (b) polo lazo cerrado en z,
    (c) Bode PI continuo vs discreto, (d) PM vs Ts con Tustin."""
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 10.0))
    (a1, a2), (a3, a4) = axes
    th = np.linspace(0, 2*np.pi, 300)

    # (a) Mapeo s->z con curvas iso-zeta
    Ts_ref = 100e-6
    a1.fill(np.cos(th), np.sin(th), color=OK, alpha=0.10)
    a1.plot(np.cos(th), np.sin(th), "k", lw=1.5, label="circulo unidad |z|=1")
    a1.scatter([1], [0], color="#555", s=40, zorder=8)
    a1.text(1.05, 0.05, "z=1 (DC)", fontsize=8)
    a1.scatter([-1], [0], color="#555", s=40, zorder=8)
    a1.text(-1.65, 0.05, "z=-1 (fs/2)", fontsize=8)

    for zeta_c, col_c in [(0.3, ACC2), (0.5, ACC), (0.7, OK), (1.0, BAD)]:
        wn_r = np.linspace(0, 0.45*2*np.pi/Ts_ref, 120)
        wd_r = np.sqrt(max(1-zeta_c**2, 0)) * wn_r
        s_pts = -zeta_c*wn_r + 1j*wd_r
        z_pts = np.exp(s_pts * Ts_ref)
        a1.plot(z_pts.real, z_pts.imag, color=col_c, lw=1.6, label=f"zeta={zeta_c}")
        a1.plot(z_pts.real, -z_pts.imag, color=col_c, lw=1.6, ls="--", alpha=0.5)

    a1.set_xlim(-1.6, 1.6); a1.set_ylim(-1.4, 1.4); a1.set_aspect("equal")
    a1.axvline(0, color="#bbb", lw=0.6); a1.axhline(0, color="#bbb", lw=0.6)
    a1.set_xlabel("Re(z)"); a1.set_ylabel("Im(z)")
    a1.set_title(f"(a) Mapeo s->z (Ts={Ts_ref*1e6:.0f} us)\ncurvas iso-zeta en plano z")
    a1.legend(fontsize=7.5, loc="lower left"); a1.grid(True, alpha=0.3)

    # (b) Polo lazo cerrado en z al variar Kp
    L_b = 2e-3; wc_b = 2*np.pi*750; Ts_b = 100e-6
    a2.fill(np.cos(th), np.sin(th), color=OK, alpha=0.08)
    a2.plot(np.cos(th), np.sin(th), "k", lw=1.2, label="unidad")
    Kp_nom = L_b * wc_b
    Kp_vec = np.linspace(0.01, 5.0, 200) * Kp_nom
    roots_z = np.exp(-(Kp_vec/L_b)*Ts_b)
    sc_z = a2.scatter(roots_z, np.zeros_like(roots_z), c=Kp_vec/Kp_nom,
                      cmap="plasma", s=20, zorder=5)
    fig.colorbar(sc_z, ax=a2, label="Kp / Kp_nom")
    z_design = np.exp(-wc_b*Ts_b)
    a2.scatter([z_design], [0], color=BAD, s=80, marker="*", zorder=9,
               label=f"diseno: z={z_design:.3f}")
    a2.axvline(0, color="#bbb", lw=0.6); a2.axhline(0, color="#bbb", lw=0.6)
    a2.set_xlim(-1.6, 1.6); a2.set_ylim(-1.4, 1.4); a2.set_aspect("equal")
    a2.set_xlabel("Re(z)"); a2.set_ylabel("Im(z)")
    a2.set_title("(b) Polo lazo cerrado en z al variar Kp\n(planta inductiva, modelo 1er orden)")
    a2.legend(fontsize=8, loc="lower left"); a2.grid(True, alpha=0.3)

    # (c) Bode PI continuo vs Euler atras vs Tustin
    L_c = 2e-3; R_c = 50e-3; Ts_c = 100e-6
    wc_c = 2*np.pi*750; Kp_c = L_c*wc_c; Ki_c = R_c*wc_c
    f_c = np.logspace(1, 4.2, 1000); w_c = 2*np.pi*f_c

    H_cont = Kp_c + Ki_c/(1j*w_c)
    s_eb   = (1 - np.exp(-1j*w_c*Ts_c)) / Ts_c
    H_eb   = Kp_c + Ki_c / s_eb
    s_tu   = 2/Ts_c * (np.exp(1j*w_c*Ts_c)-1)/(np.exp(1j*w_c*Ts_c)+1)
    H_tu   = Kp_c + Ki_c / s_tu

    a3.semilogx(f_c, 20*np.log10(np.abs(H_cont)), color=ACC,  lw=2.5, label="continuo")
    a3.semilogx(f_c, 20*np.log10(np.abs(H_eb)),   color=ACC2, lw=2.0, ls="--", label="Euler atras")
    a3.semilogx(f_c, 20*np.log10(np.abs(H_tu)),   color=OK,   lw=2.0, ls="-.", label="Tustin")
    a3.axvline(1/(Ts_c*2), color="#888", ls=":", lw=1.2,
               label=f"Nyquist {1/(Ts_c*2):.0f} Hz")
    a3.set_xlabel("frecuencia [Hz]"); a3.set_ylabel("|PI| [dB]")
    a3.set_title(f"(c) PI continuo vs discreto (Ts={Ts_c*1e6:.0f} us)\nEuler atras vs Tustin")
    a3.legend(fontsize=8); a3.grid(True, which="both", alpha=0.3); a3.set_xlim(10, 5e3)

    # (d) PM vs Ts con Tustin
    L_d = 2e-3; R_d = 50e-3; wc_d = 2*np.pi*750
    Ts_d_vec = np.array([50, 75, 100, 150, 200, 300, 500]) * 1e-6
    pm_d_vec = []
    for Ts_di in Ts_d_vec:
        Kp_d = L_d * wc_d; Ki_d = R_d * wc_d
        s_tu_wc = 2/Ts_di*(np.exp(1j*wc_d*Ts_di)-1)/(np.exp(1j*wc_d*Ts_di)+1)
        H_pi_wc = Kp_d + Ki_d / s_tu_wc
        L_open = H_pi_wc / (L_d * 1j*wc_d)
        pm_d_vec.append(180 + np.degrees(np.angle(L_open)))
    pm_d_vec = np.array(pm_d_vec)

    a4.plot(Ts_d_vec*1e6, pm_d_vec, color=ACC, lw=2.5, marker="o", ms=8)
    a4.axhline(45, color=BAD, ls="--", lw=1.5, label="PM=45 deg (minimo)")
    a4.axhline(60, color=OK,  ls="--", lw=1.5, label="PM=60 deg (objetivo)")
    a4.fill_between(Ts_d_vec*1e6, pm_d_vec, 45,
                    where=(pm_d_vec < 45), color=BAD, alpha=0.2, label="PM insuficiente")
    a4.set_xlabel("Ts [us]"); a4.set_ylabel("PM [deg]")
    a4.set_title("(d) PM vs Ts (Tustin, wc=2pi*750 Hz)\nTs mayor consume margen de fase")
    a4.legend(fontsize=8); a4.grid(True, alpha=0.3)

    fig.suptitle("Transformada Z: analisis completo - discretizacion y estabilidad",
                 fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _savefig(fig, "transformada-z-analisis.png")


# ===================================================================== #
#  droop-dc-analisis  (sin decorador @figura)
# ===================================================================== #
def _droopdc_extended():
    """4 paneles: (a) curvas V(I) dos fuentes y punto de operacion compartido,
    (b) reparto de carga vs carga total, (c) efecto R_cable, (d) correccion secundaria."""
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.0))
    (a1, a2), (a3, a4) = axes

    Vref = 400.0
    Rd1, Rd2 = 0.5, 1.0
    I_max = 100.0

    # (a) Curvas V-I y punto de operacion
    Io = np.linspace(0, I_max, 200)
    Rd_par = Rd1*Rd2/(Rd1+Rd2)
    I_total = 60.0
    Vbus_op = Vref - Rd_par*I_total
    I1_op = (Vref - Vbus_op)/Rd1
    I2_op = (Vref - Vbus_op)/Rd2

    a1.plot(Io, Vref - Rd1*Io, color=ACC,  lw=2.5,
            label=f"fuente 1: Rd={Rd1} Ohm (I1={I1_op:.0f} A)")
    a1.plot(Io, Vref - Rd2*Io, color=ACC2, lw=2.5,
            label=f"fuente 2: Rd={Rd2} Ohm (I2={I2_op:.0f} A)")
    a1.axhline(Vbus_op, color="#888", ls="--", lw=1.2,
               label=f"Vbus={Vbus_op:.1f} V")
    a1.plot([I1_op, I2_op], [Vbus_op, Vbus_op], "o", color=BAD, ms=9, zorder=8,
            label="puntos de operacion")
    a1.annotate(f"I1={I1_op:.0f} A", xy=(I1_op, Vbus_op),
                xytext=(I1_op+3, Vbus_op+2), fontsize=8, color=ACC)
    a1.annotate(f"I2={I2_op:.0f} A", xy=(I2_op, Vbus_op),
                xytext=(I2_op+3, Vbus_op-4), fontsize=8, color=ACC2)
    a1.set_xlabel("corriente de salida Io [A]"); a1.set_ylabel("Vdc [V]")
    a1.set_title(f"(a) Droop DC: curvas V-I y reparto\nI1/I2 = Rd2/Rd1 = {I1_op/I2_op:.1f}")
    a1.legend(fontsize=8); a1.set_ylim(340, 415); a1.grid(True, alpha=0.3)

    # (b) Reparto vs carga total
    I_load_vec = np.linspace(5, 180, 100)
    I1_vec = I_load_vec * Rd2/(Rd1+Rd2)
    I2_vec = I_load_vec * Rd1/(Rd1+Rd2)
    Vbus_vec = Vref - Rd_par * I_load_vec

    a2b = a2.twinx()
    a2.plot(I_load_vec, I1_vec, color=ACC,  lw=2.5, label=f"I1 (Rd={Rd1} Ohm)")
    a2.plot(I_load_vec, I2_vec, color=ACC2, lw=2.5, label=f"I2 (Rd={Rd2} Ohm)")
    a2.plot(I_load_vec, I_load_vec, color="#bbb", lw=1.5, ls=":", label="I_total")
    a2b.plot(I_load_vec, Vbus_vec, color=BAD, lw=2.0, ls="--", label="Vbus [V]")
    a2b.set_ylabel("Vbus [V]", color=BAD); a2b.tick_params(axis="y", colors=BAD)
    a2.axvline(I_total, color="#888", ls=":", lw=1.2)
    a2.set_xlabel("corriente de carga total I_load [A]"); a2.set_ylabel("corriente [A]")
    a2.set_title("(b) Reparto proporcional vs carga total\nrelacion fija por Rd1, Rd2")
    lines1, labs1 = a2.get_legend_handles_labels()
    lines2, labs2 = a2b.get_legend_handles_labels()
    a2.legend(lines1+lines2, labs1+labs2, fontsize=8, loc="upper left")
    a2.grid(True, alpha=0.3)

    # (c) Efecto R_cable
    Rline1_vec = np.linspace(0, 0.8, 80)
    Rline2 = 0.1
    I_load_c = 60.0
    I1_cable = I_load_c*(Rd2+Rline2)/(Rd1+Rline1_vec+Rd2+Rline2)
    I2_cable = I_load_c*(Rd1+Rline1_vec)/(Rd1+Rline1_vec+Rd2+Rline2)

    a3.plot(Rline1_vec, I1_cable, color=ACC,  lw=2.5, label="I1 (fuente 1)")
    a3.plot(Rline1_vec, I2_cable, color=ACC2, lw=2.5, label="I2 (fuente 2)")
    a3.axhline(I_load_c*Rd2/(Rd1+Rd2), color=ACC,  ls="--", lw=1.2, alpha=0.5,
               label="I1 ideal (sin cable)")
    a3.axhline(I_load_c*Rd1/(Rd1+Rd2), color=ACC2, ls="--", lw=1.2, alpha=0.5,
               label="I2 ideal")
    a3.axvline(Rd1*0.1, color="#888", ls=":", lw=1.2)
    a3.text(Rd1*0.1+0.02, 42, f"Rline=0.1*Rd\nerror<5%", fontsize=8, color="#555")
    a3.set_xlabel("R_cable fuente 1 [Ohm]"); a3.set_ylabel("corriente [A]")
    a3.set_title("(c) Efecto R_cable en el reparto\nRd >> R_cable necesario")
    a3.legend(fontsize=8, loc="center right"); a3.grid(True, alpha=0.3)

    # (d) Correccion secundaria
    dV_sec_vec = np.linspace(0, Rd_par*I_total, 60)
    Vref_eff = Vref + dV_sec_vec
    Vbus_s = Vref_eff - Rd_par*I_total
    I1_s = (Vref_eff - Vbus_s)/Rd1
    I2_s = (Vref_eff - Vbus_s)/Rd2

    a4.plot(dV_sec_vec, Vbus_s, color=BAD, lw=2.5, label="Vbus (con secundario)")
    a4.axhline(Vref, color="#888", ls="--", lw=1.5, label=f"Vnom={Vref} V")
    a4.axhline(Vbus_op, color="#bbb", ls=":", lw=1.2,
               label=f"Vbus_0={Vbus_op:.1f} V (sin sec.)")
    a4b = a4.twinx()
    a4b.plot(dV_sec_vec, I1_s, color=ACC, lw=2.0, ls="--", label="I1 (sec.)")
    a4b.plot(dV_sec_vec, I2_s, color=ACC2, lw=2.0, ls="--", label="I2 (sec.)")
    a4b.set_ylabel("corriente [A]", color="#888"); a4b.tick_params(axis="y", colors="#888")
    a4.axvline(Rd_par*I_total, color=OK, ls="--", lw=1.5, label="compensacion total")
    a4.set_xlabel("dV_sec [V] (correccion secundaria)"); a4.set_ylabel("Vbus [V]")
    a4.set_title("(d) Correccion secundaria\ndV restaura Vnom sin alterar el reparto")
    lines1, labs1 = a4.get_legend_handles_labels()
    lines2, labs2 = a4b.get_legend_handles_labels()
    a4.legend(lines1+lines2, labs1+labs2, fontsize=8, loc="lower right")
    a4.grid(True, alpha=0.3)

    fig.suptitle("Droop DC: analisis completo - reparto, cable, correccion secundaria",
                 fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _savefig(fig, "droop-dc-analisis.png")


# ===================================================================== #
#  rectificador-afe-analisis  (sin decorador @figura)
# ===================================================================== #
def _afe_extended():
    """4 paneles: (a) diagrama de control AFE, (b) formas de onda,
    (c) Bode lazo de tension DC, (d) id*(t) ante escalon de carga."""
    from matplotlib.patches import Rectangle

    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    a1, a2, a3, a4 = axes.flat

    # --- (a) diagrama de control AFE ---
    ax = a1; ax.set_axis_off(); ax.set_xlim(0, 10); ax.set_ylim(0, 8)
    ax.set_title("(a) Lazo de control del AFE (cascada Vdc → id*)", fontsize=10)

    def _box(ax, x, y, w, h, txt, col="#e8f0ff", ecol=ACC, fs=8.5):
        ax.add_patch(Rectangle((x, y), w, h, facecolor=col, edgecolor=ecol, lw=1.5))
        ax.text(x+w/2, y+h/2, txt, ha="center", va="center", fontsize=fs)

    def _arr(ax, x0, y0, x1, y1):
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color="#444", lw=1.3))

    ax.text(0.2, 6.5, "$V_{dc}^*$", fontsize=10, color=ACC, fontweight="bold")
    _arr(ax, 0.9, 6.5, 1.3, 6.5)
    c1 = plt.Circle((1.5, 6.5), 0.2, fill=False, edgecolor="#555", lw=1.5)
    ax.add_patch(c1); ax.text(1.5, 6.5, "−", ha="center", va="center", fontsize=12)
    _arr(ax, 1.7, 6.5, 2.2, 6.5)
    _box(ax, 2.2, 6.1, 1.8, 0.8, "PI\ntension DC", "#fff0e0", ACC2)
    _arr(ax, 4.0, 6.5, 4.5, 6.5)
    ax.text(4.1, 6.7, "$i_d^*$", fontsize=9, color=ACC2)
    c2 = plt.Circle((4.7, 6.5), 0.2, fill=False, edgecolor="#555", lw=1.5)
    ax.add_patch(c2); ax.text(4.7, 6.5, "−", ha="center", va="center", fontsize=12)
    _arr(ax, 4.9, 6.5, 5.4, 6.5)
    _box(ax, 5.4, 6.1, 1.6, 0.8, "PI\ncorriente d", "#e8ffe8", OK)
    _arr(ax, 7.0, 6.5, 7.5, 6.5)
    ax.text(7.05, 6.7, "$v_d^*$", fontsize=9, color=OK)
    _box(ax, 7.5, 6.1, 1.8, 0.8, "PWM + VSC", "#ffe8e8", BAD)
    _arr(ax, 9.3, 6.5, 9.8, 6.5)
    ax.text(9.82, 6.45, "red", fontsize=8.5)

    ax.text(0.2, 4.5, "$i_q^*=0$", fontsize=10, color=BAD, fontweight="bold")
    _arr(ax, 1.0, 4.5, 1.5, 4.5)
    c3 = plt.Circle((1.7, 4.5), 0.2, fill=False, edgecolor="#555", lw=1.5)
    ax.add_patch(c3); ax.text(1.7, 4.5, "−", ha="center", va="center", fontsize=12)
    _arr(ax, 1.9, 4.5, 2.4, 4.5)
    _box(ax, 2.4, 4.1, 1.6, 0.8, "PI\ncorriente q", "#e8ffe8", OK)
    _arr(ax, 4.0, 4.5, 4.5, 4.5)
    ax.text(4.05, 4.7, "$v_q^*$", fontsize=9, color=OK)
    _box(ax, 4.5, 4.1, 1.8, 0.8, "PWM + VSC", "#ffe8e8", BAD)
    _arr(ax, 6.3, 4.5, 6.8, 4.5)
    ax.text(6.82, 4.45, "red", fontsize=8.5)

    _box(ax, 2.0, 2.4, 2.2, 0.8, "PLL (SRF)\n$\\hat{\\theta}$", "#f0e8ff", "#8855cc")
    ax.text(1.0, 2.8, "red AC", fontsize=8.5)
    _arr(ax, 1.9, 2.8, 2.0, 2.8)
    ax.plot([2.0, 5.8, 5.8], [5.6, 5.6, 5.0], color="#777", lw=1.0, ls="--")
    ax.text(4.2, 5.35, "retroalim. $V_{dc}$", fontsize=8, color="#777")
    _arr(ax, 2.0, 5.0, 2.0, 5.6)
    _box(ax, 5.5, 2.0, 3.8, 1.0, "$i_q^*=0 \\Rightarrow Q=0 \\Rightarrow$ FP=1\n"
         "$i_d^*=\\frac{2}{3}\\frac{P^*}{\\hat{V}}$", "#fffbe8", ACC2, fs=8.5)

    # --- (b) formas de onda: diodos vs AFE ---
    ax = a2
    t = np.linspace(0, 0.04, 2000); w0 = 2*np.pi*50
    i_diodos = np.zeros_like(t)
    for k in range(3):
        i_diodos += np.clip(np.cos(w0*t - k*2*np.pi/3), 0, None)
    i_diodos /= i_diodos.max()
    i_afe = 0.95*np.cos(w0*t) + 0.03*np.cos(5*w0*t) + 0.02*np.cos(7*w0*t)
    i_afe /= np.max(np.abs(i_afe))
    ax.plot(t*1e3, i_diodos - 1.6, color=BAD, lw=1.8, label="Rect. diodos (THD≈80%)")
    ax.plot(t*1e3, i_afe + 0.2, color=ACC, lw=1.8, label="AFE (THD≈3%)")
    ax.plot(t*1e3, 0.5*np.cos(w0*t) + 0.2, color=ACC2, lw=1.0, ls="--", alpha=0.7, label="tensión ref.")
    ax.axhline(-1.6, color="#ddd", lw=0.5); ax.axhline(0.2, color="#ddd", lw=0.5)
    ax.set_xlabel("t [ms]"); ax.set_ylabel("corriente [pu]")
    ax.set_title("(b) Forma de onda de corriente de red", fontsize=10)
    ax.legend(fontsize=8); ax.set_yticks([]); ax.set_xlim(0, 40)

    # --- (c) Bode del lazo de tension DC ---
    ax = a3
    from scipy import signal as sig
    Kp_v, Ki_v, C = 2.0, 50.0, 50e-3
    sys_ol = sig.TransferFunction(np.polymul([Kp_v, Ki_v], [1]),
                                  np.polymul([1, 0], [C, 0]))
    w_arr = np.logspace(0, 4, 600)
    _, H_ol = sig.freqs(sys_ol.num, sys_ol.den, worN=w_arr)
    mag_ol = 20*np.log10(np.abs(H_ol) + 1e-12)
    ph_ol = np.degrees(np.angle(H_ol))
    ax.semilogx(w_arr/(2*np.pi), mag_ol, color=ACC, lw=2, label="$|L(j\\omega)|$")
    ax.axhline(0, color="#bbb", ls=":", lw=1)
    ax.axvline(20, color=OK, ls="--", lw=1.2)
    ax.text(22, -5, "BW≈20 Hz", fontsize=8, color=OK)
    ax2c = ax.twinx()
    ax2c.semilogx(w_arr/(2*np.pi), ph_ol, color=ACC2, lw=1.5, ls="--", label="fase")
    ax2c.axhline(-180, color=BAD, ls=":", lw=1)
    ax2c.set_ylabel("fase [°]", color=ACC2); ax2c.tick_params(axis="y", labelcolor=ACC2)
    ax.set_xlabel("frecuencia [Hz]"); ax.set_ylabel("magnitud [dB]")
    ax.set_title("(c) Bode lazo tension DC (PI, C=50 mF)", fontsize=10)
    lines1, labs1 = ax.get_legend_handles_labels()
    lines2, labs2 = ax2c.get_legend_handles_labels()
    ax.legend(lines1+lines2, labs1+labs2, fontsize=7.5, loc="lower left")

    # --- (d) id*(t) ante escalon de carga ---
    ax = a4
    Ts = 1e-4; T_arr = np.arange(0, 0.5, Ts)
    Vdc = 800.0; xi = 0.0; Vref = 800.0
    Idc_arr = np.where(T_arr < 0.1, 300.0, 625.0)
    id_list = []; Vdc_list = []
    for idc in Idc_arr:
        err = Vref - Vdc; xi += Ki_v*err*Ts
        id_s = np.clip((Kp_v*err + xi) * (2/3) / (800*np.sqrt(2)/np.sqrt(3)), 0, 900)
        Vdc += ((3/2)*800*(id_s/np.sqrt(2)) - Vdc*idc) / (C*Vdc) * Ts
        id_list.append(id_s); Vdc_list.append(Vdc)
    ax.plot(T_arr*1e3, id_list, color=ACC, lw=2, label="$i_d^*$ [A]")
    ax4b = ax.twinx()
    ax4b.plot(T_arr*1e3, Vdc_list, color=BAD, lw=1.5, ls="--", label="$V_{dc}$ [V]")
    ax4b.axhline(800, color="#bbb", ls=":", lw=1)
    ax4b.set_ylabel("$V_{dc}$ [V]", color=BAD); ax4b.tick_params(axis="y", labelcolor=BAD)
    ax.axvline(100, color="#888", ls="--", lw=1); ax.text(102, 30, "escalon\ncarga", fontsize=8)
    ax.set_xlabel("t [ms]"); ax.set_ylabel("$i_d^*$ [A]"); ax.set_xlim(0, 500)
    ax.set_title("(d) Respuesta ante escalon de carga (500 kW)", fontsize=10)
    lines1, labs1 = ax.get_legend_handles_labels()
    lines2, labs2 = ax4b.get_legend_handles_labels()
    ax.legend(lines1+lines2, labs1+labs2, fontsize=7.5, loc="center right")

    fig.suptitle("AFE 500 kW — control vectorial y respuesta dinamica", fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _savefig(fig, "rectificador-afe-analisis.png")


# ===================================================================== #
#  statcom-svc-analisis  (sin decorador @figura)
# ===================================================================== #
def _statcom_extended():
    """4 paneles: (a) topologia SVC vs STATCOM, (b) caracteristica V-I,
    (c) V_pcc(t) ante hueco, (d) lazo de control STATCOM."""
    from matplotlib.patches import Rectangle

    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    a1, a2, a3, a4 = axes.flat

    # --- (a) topologia ---
    ax = a1; ax.set_axis_off(); ax.set_xlim(0, 10); ax.set_ylim(0, 8)
    ax.set_title("(a) Topologia: SVC (TCR+TSC) vs STATCOM (VSC)", fontsize=10)

    def _b(ax, x, y, w, h, txt, col, ecol, fs=8.5):
        ax.add_patch(Rectangle((x, y), w, h, facecolor=col, edgecolor=ecol, lw=1.5))
        ax.text(x+w/2, y+h/2, txt, ha="center", va="center", fontsize=fs)

    def _a(ax, x0, y0, x1, y1):
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color="#444", lw=1.3))

    ax.plot([2.5, 7.5], [7.4, 7.4], color="#333", lw=2.5)
    ax.plot([2.5, 2.5], [7.0, 7.4], color="#333", lw=2.5)
    ax.plot([7.5, 7.5], [7.0, 7.4], color="#333", lw=2.5)
    ax.text(5.0, 7.6, "Red / PCC (nudo debil)", ha="center", fontsize=9, color="#444")
    # SVC
    _b(ax, 0.3, 4.8, 2.0, 1.2, "TCR\n(reactor tiristor)", "#ffe8e8", BAD)
    _b(ax, 0.3, 3.2, 2.0, 1.2, "TSC\n(condensador tiristor)", "#e8f0ff", ACC)
    ax.plot([1.3, 1.3, 2.5, 2.5], [6.0, 7.0, 7.0, 7.4], color="#333", lw=1.5)
    ax.plot([1.3, 1.3], [4.8, 4.4], color="#333", lw=1.5)
    ax.plot([1.3, 1.3], [3.2, 2.8], color="#333", lw=1.5)
    ax.text(1.3, 1.8, "SVC: $Q=B\\cdot V^2$", ha="center", fontsize=9, color=BAD, fontweight="bold")
    # STATCOM
    _b(ax, 6.0, 4.5, 2.8, 1.2, "VSC (puente IGBT)", "#e8ffe8", OK)
    ax.add_patch(Rectangle((6.8, 3.5), 1.2, 0.8, facecolor="#fffbe8", edgecolor=ACC2, lw=1.3))
    ax.text(7.4, 3.9, "$C_{dc}$", ha="center", fontsize=9, color=ACC2)
    _b(ax, 6.2, 2.5, 2.4, 0.8, "Trafo / filtro LCL", "#f0e8ff", "#8855cc", fs=8)
    ax.plot([7.4, 7.4, 7.5, 7.5], [5.7, 7.0, 7.0, 7.4], color="#333", lw=1.5)
    ax.plot([7.4, 7.4], [4.5, 4.3], color="#333", lw=1.5)
    ax.plot([7.4, 7.4], [3.5, 3.3], color="#333", lw=1.5)
    ax.plot([7.4, 7.4], [2.5, 2.3], color="#333", lw=1.5)
    ax.text(7.4, 1.8, "STATCOM: $Q=V\\cdot I_q$", ha="center", fontsize=9, color=OK, fontweight="bold")

    # --- (b) caracteristica V-I ---
    ax = a2
    I = np.linspace(-1.0, 1.0, 300)
    V_statcom = 1.0 + 0.05*I
    I_svc = np.linspace(-0.8, 0.8, 200)
    V_svc = 1.0 + 0.35*I_svc + 0.25*I_svc**2
    ax.fill_betweenx([0.7, 1.3], -1.0, 1.0, color=ACC, alpha=0.08, label="Zona op. STATCOM")
    ax.plot(I_svc, np.clip(V_svc, 0.5, 1.5), color=BAD, lw=2, label="SVC (susceptancia)")
    ax.plot(I, V_statcom, color=ACC, lw=2, label="STATCOM (fuente de corriente)")
    ax.axhline(0.85, color="#888", ls="--", lw=1)
    ax.text(0.05, 0.86, "hueco $V=0.85$ pu", fontsize=8)
    ax.axvline(0, color="#bbb", lw=0.8); ax.axhline(1.0, color="#bbb", lw=0.8, ls=":")
    ax.set_xlabel("$I_q$ [pu] (+ cap.)"); ax.set_ylabel("$V_{pcc}$ [pu]")
    ax.set_title("(b) Caracteristica V-I: SVC vs STATCOM", fontsize=10)
    ax.legend(fontsize=8, loc="lower right")
    ax.set_xlim(-1.1, 1.1); ax.set_ylim(0.4, 1.5)

    # --- (c) V_pcc(t) ante hueco ---
    ax = a3
    Ts = 1e-4; T_arr = np.arange(0, 0.3, Ts)
    t_on, t_off = 0.05, 0.15; Xth = 0.15

    def _sim_vpcc(tau_r, kp_r, ki_r):
        V = 1.0; xi = 0.0; Iq = 0.0; vout = []
        for t in T_arr:
            Vg = 1.0 if (t < t_on or t > t_off) else 0.7
            err = 1.0 - V; xi += ki_r*err*Ts
            Iq_ref = np.clip(kp_r*err + xi, -1.0, 1.0)
            Iq += (Iq_ref - Iq)/tau_r * Ts
            V = Vg + Xth*Iq; vout.append(V)
        return vout

    V_none = [1.0 if (t < t_on or t > t_off) else 0.7 for t in T_arr]
    ax.plot(T_arr*1e3, V_none, color="#999", lw=1.5, ls=":", label="Sin compensacion")
    ax.plot(T_arr*1e3, _sim_vpcc(5e-3, 5.0, 80.0), color=BAD, lw=2, label="Con SVC")
    ax.plot(T_arr*1e3, _sim_vpcc(1e-3, 8.0, 150.0), color=ACC, lw=2, label="Con STATCOM")
    ax.axhline(0.9, color=OK, ls="--", lw=1); ax.text(2, 0.91, "limite 0.9 pu", fontsize=8, color=OK)
    ax.axvspan(t_on*1e3, t_off*1e3, color="#fee", alpha=0.4)
    ax.text((t_on+t_off)/2*1e3, 0.67, "hueco", ha="center", fontsize=8, color=BAD)
    ax.set_xlabel("t [ms]"); ax.set_ylabel("$V_{pcc}$ [pu]")
    ax.set_title("(c) Respuesta dinamica ante hueco de tension", fontsize=10)
    ax.legend(fontsize=8, loc="lower right"); ax.set_ylim(0.55, 1.12)

    # --- (d) lazo de control STATCOM ---
    ax = a4; ax.set_axis_off(); ax.set_xlim(0, 10); ax.set_ylim(0, 8)
    ax.set_title("(d) Lazo de control del STATCOM (Vpcc → iq*)", fontsize=10)

    def _b2(x, y, w, h, txt, col="#e8f0ff", ecol=ACC, fs=8.5):
        ax.add_patch(Rectangle((x, y), w, h, facecolor=col, edgecolor=ecol, lw=1.5))
        ax.text(x+w/2, y+h/2, txt, ha="center", va="center", fontsize=fs)

    def _a2(x0, y0, x1, y1):
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color="#444", lw=1.3))

    ax.text(0.2, 5.8, "$V_{pcc}^*=1$", fontsize=10, color=ACC, fontweight="bold")
    _a2(1.4, 5.8, 1.8, 5.8)
    c1 = plt.Circle((2.0, 5.8), 0.2, fill=False, edgecolor="#555", lw=1.5)
    ax.add_patch(c1); ax.text(2.0, 5.8, "−", ha="center", va="center", fontsize=12)
    _a2(2.2, 5.8, 2.7, 5.8)
    _b2(2.7, 5.4, 2.0, 0.8, "PI + droop\nQ-V", "#fff0e0", ACC2)
    _a2(4.7, 5.8, 5.2, 5.8)
    ax.text(4.75, 6.0, "$i_q^*$", fontsize=9, color=ACC2)
    _b2(5.2, 5.4, 2.0, 0.8, "PI corriente q", "#e8ffe8", OK)
    _a2(7.2, 5.8, 7.7, 5.8)
    ax.text(7.25, 6.0, "$v_q^*$", fontsize=9, color=OK)
    _b2(7.7, 5.4, 1.8, 0.8, "PWM VSC", "#ffe8e8", BAD)
    _a2(9.5, 5.8, 9.9, 5.8)
    ax.text(0.5, 4.0, "$i_d^*\\approx 0$", fontsize=9, color="#555")
    _a2(2.0, 4.0, 5.5, 4.0)
    _b2(5.5, 3.6, 2.0, 0.8, "PI corriente d", "#e8ffe8", OK)
    _a2(7.5, 4.0, 8.0, 4.0)
    _b2(3.5, 2.0, 2.0, 0.8, "PLL\n$\\hat{\\theta}(V_{pcc})$", "#f0e8ff", "#8855cc")
    ax.plot([2.0, 2.0, 9.8, 9.8], [5.6, 5.0, 5.0, 6.8], color="#777", lw=1.0, ls="--")
    ax.text(6.0, 4.8, "retroalim. $V_{pcc}$", fontsize=8, color="#777")
    _a2(2.0, 5.0, 2.0, 5.6)
    _b2(1.5, 1.0, 4.0, 0.8, "FRT: prioridad $i_q > i_d$, $|i_q| \\leq I_{max}$", "#fffbe8", ACC2, fs=8)

    fig.suptitle("STATCOM 50 MVAr — topologia, caracteristica V-I y control", fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _savefig(fig, "statcom-svc-analisis.png")


# ===================================================================== #
#  ecuacion-oscilacion-analisis  (sin decorador @figura)
# ===================================================================== #
def _swing_extended():
    """4 paneles: (a) curva P(d), (b) mapa de fase, (c) f(t) H=2,4,8s, (d) maquina vs VSM."""
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    a1, a2, a3, a4 = axes.flat

    E, Vg, X, w0 = 1.05, 1.0, 0.25, 2*np.pi*50
    Pmax = E*Vg/X; Pm = 0.7*Pmax
    delta_s = np.arcsin(Pm/Pmax)
    delta_u = np.pi - delta_s

    # --- (a) curva P(delta) ---
    ax = a1
    d_arr = np.linspace(0, np.pi, 400)
    ax.plot(np.degrees(d_arr), Pmax*np.sin(d_arr), color=ACC, lw=2.5)
    ax.axhline(Pm, color=ACC2, ls="--", lw=1.5, label=f"$P_m$={Pm:.2f} pu")
    ax.plot(np.degrees(delta_s), Pm, "o", color=OK, ms=10, zorder=5,
            label=f"SEP $\\delta_0$={np.degrees(delta_s):.1f}°")
    ax.plot(np.degrees(delta_u), Pm, "s", color=BAD, ms=10, zorder=5,
            label=f"UEP $\\delta_u$={np.degrees(delta_u):.1f}°")
    ax.fill_between(np.degrees(d_arr), Pmax*np.sin(d_arr), Pm,
                    where=(Pmax*np.sin(d_arr) >= Pm) & (d_arr <= delta_u),
                    color=OK, alpha=0.12, label="Area acelerac.")
    ax.fill_between(np.degrees(d_arr), Pmax*np.sin(d_arr), Pm,
                    where=(Pmax*np.sin(d_arr) < Pm) & (d_arr > delta_u),
                    color=BAD, alpha=0.12, label="Area decelerac.")
    ax.set_xlabel("$\\delta$ [°]"); ax.set_ylabel("$P_e$ [pu]")
    ax.set_title("(a) Curva $P(\\delta)$: equilibrios y areas iguales", fontsize=10)
    ax.legend(fontsize=7.5, loc="upper right"); ax.set_xlim(0, 180)

    # --- (b) mapa de fase ---
    ax = a2
    H_ph, D_ph = 4.0, 5.0; Ts_ph = 1e-3

    def _traj(d0, dw0, Pm_v, nmax=10000):
        d, dw = d0, dw0; dl, wl = [np.degrees(d)], [dw]
        for _ in range(nmax):
            Pe = Pmax*np.sin(d)
            dw += (Pm_v - Pe - D_ph*dw)/(2*H_ph)*Ts_ph
            d += w0*dw*Ts_ph
            dl.append(np.degrees(d)); wl.append(dw)
            if np.degrees(d) > 210 or np.degrees(d) < -10:
                break
        return dl, wl

    for dw0, col, lbl in [(-0.05, ACC, "traj. estable"), (0.22, OK, "traj. grande"),
                           (0.45, BAD, "inestable")]:
        dl, wl = _traj(delta_s + 0.08, dw0, Pm)
        ax.plot(dl, wl, color=col, lw=1.5, label=lbl)
    for sgn in [1, -1]:
        dl, wl = _traj(delta_u - 1e-3, sgn*0.004, Pm, nmax=5000)
        ax.plot(dl, wl, color="#888", lw=1.0, ls="--")
    ax.plot(np.degrees(delta_s), 0, "o", color=OK, ms=8, zorder=5)
    ax.plot(np.degrees(delta_u), 0, "s", color=BAD, ms=8, zorder=5)
    ax.axvline(np.degrees(delta_s), color=OK, ls=":", lw=1)
    ax.axvline(np.degrees(delta_u), color=BAD, ls=":", lw=1)
    ax.text(np.degrees(delta_u)+2, 0.55, "separatriz", fontsize=7.5, color="#888")
    ax.set_xlabel("$\\delta$ [°]"); ax.set_ylabel("$\\Delta\\omega$ [pu]")
    ax.set_title("(b) Mapa de fase: separatriz y regiones de atraccion", fontsize=10)
    ax.legend(fontsize=7.5); ax.set_xlim(0, 200); ax.set_ylim(-0.7, 0.7)

    # --- (c) f(t) ante escalon ---
    ax = a3
    Ts2 = 5e-4; T2 = np.arange(0, 8.0, Ts2); dPm = -0.20; D2 = 5.0
    for H_v, col, lbl in [(2.0, BAD, "$H=2$ s"), (4.0, ACC, "$H=4$ s"), (8.0, OK, "$H=8$ s")]:
        d, dw = delta_s, 0.0; fl = []
        for t in T2:
            Pm_t = Pm + dPm if t > 0.5 else Pm
            dw += (Pm_t - Pmax*np.sin(d) - D2*dw)/(2*H_v)*Ts2
            d += w0*dw*Ts2; fl.append(50.0 + dw*50)
        ax.plot(T2, fl, color=col, lw=2, label=lbl)
    ax.axhline(50.0, color="#bbb", ls=":", lw=1)
    ax.axvline(0.5, color="#888", ls="--", lw=1)
    ax.text(0.6, 49.1, "escalon $\\Delta P$", fontsize=8, color="#555")
    ax.set_xlabel("t [s]"); ax.set_ylabel("f [Hz]")
    ax.set_title("(c) $f(t)$ ante escalon de carga: efecto de $H$", fontsize=10)
    ax.legend(fontsize=8); ax.set_ylim(48.4, 50.5)

    # --- (d) maquina real vs VSM ---
    ax = a4
    Ts3 = 5e-4; T3 = np.arange(0, 6.0, Ts3); dPm3 = -0.25
    for lbl, H_v, D_v, col, ls in [
            ("Maq. sincrona $H=4$ s", 4.0, 8.0, ACC, "-"),
            ("VSM $H=4$ s (emulado)", 4.0, 8.0, OK, "--"),
            ("VSM $H=8$ s (virtual)", 8.0, 8.0, BAD, ":")]:
        d, dw = delta_s, 0.0; fl = []
        for t in T3:
            Pm_t = Pm + dPm3 if t > 0.5 else Pm
            dw += (Pm_t - Pmax*np.sin(d) - D_v*dw)/(2*H_v)*Ts3
            d += w0*dw*Ts3; fl.append(50.0 + dw*50)
        ax.plot(T3, fl, color=col, lw=2, ls=ls, label=lbl)
    ax.axhline(50.0, color="#bbb", ls=":", lw=1)
    ax.axvline(0.5, color="#888", ls="--", lw=1)
    ax.set_xlabel("t [s]"); ax.set_ylabel("f [Hz]")
    ax.set_title("(d) Maquina real vs VSM (misma ecuacion de swing)", fontsize=10)
    ax.legend(fontsize=8); ax.set_ylim(47.8, 50.5)
    ax.text(1.5, 48.1, "H mayor → menos RoCoF", fontsize=8, color=BAD)

    fig.suptitle("Ecuacion de oscilacion — P(δ), espacio de fase y VSM", fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _savefig(fig, "ecuacion-oscilacion-analisis.png")


# ===================================================================== #
#  armonicos-thd-convertidores-analisis  (sin decorador @figura)
# ===================================================================== #
def _thd_extended():
    """4 paneles: (a) espectro VSC, (b) efecto LCL sobre espectro,
    (c) THD vs Cf, (d) verificacion vs IEEE 519."""
    from scipy import signal as sig

    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    a1, a2, a3, a4 = axes.flat

    f1 = 50.0; fsw = 10e3; m = 0.85; mf = int(fsw/f1)

    # --- (a) espectro del VSC ---
    ax = a1
    for h, amp in [(1, 100.0), (5, 2.8*m), (7, 1.9*m), (11, 0.9*m), (13, 0.7*m)]:
        ax.vlines(h*f1, 0.2, amp, color=(ACC if h == 1 else ACC2), lw=3 if h == 1 else 2)
        if h > 1:
            ax.text(h*f1, amp+1.5, f"{h}º", ha="center", fontsize=7.5, color=ACC2)
    for fb, ab in [(mf*f1, 18*m), ((mf-2)*f1, 12*m), ((mf+2)*f1, 12*m),
                   ((2*mf-1)*f1, 8*m), ((2*mf+1)*f1, 8*m)]:
        ax.vlines(fb, 0.2, ab, color=BAD, lw=2)
    ax.text(f1, 107, "fund.", ha="center", fontsize=8, color=ACC)
    ax.text(mf*f1, 22, f"$f_{{sw}}$ ({mf}°)", ha="center", fontsize=7.5, color=BAD)
    ax.set_yscale("log"); ax.set_ylim(0.2, 200); ax.set_xlim(-200, 2.2*mf*f1+200)
    ax.set_xlabel("frecuencia [Hz]"); ax.set_ylabel("amplitud [% fund.]")
    ax.set_title(f"(a) Espectro VSC: $f_{{sw}}$={fsw/1e3:.0f} kHz, m={m}", fontsize=10)

    # --- (b) efecto filtro LCL ---
    ax = a2
    L1v, L2v, Cfv = 1.5e-3, 0.5e-3, 15e-6
    Leq = L1v*L2v/(L1v+L2v); fres = 1/(2*np.pi*np.sqrt(Leq*Cfv))
    w_plot = np.logspace(np.log10(20), np.log10(4*mf*f1*2*np.pi), 1000)
    s_arr = 1j*w_plot
    H_lcl = (1/(L1v*Cfv*L2v)) / np.abs(-s_arr**3/(1j*w_plot) + s_arr*(1/(L1v*Cfv) + 1/(L2v*Cfv)) / (1j*w_plot))
    # usar transferencia exacta i2/i_inv: H = 1 / (1 - w^2*L2*Cf) para frecuencias > fres con correccion L1
    def lcl_att(f_hz):
        w = 2*np.pi*f_hz
        denom = abs(1 - w**2*Leq*Cfv)
        return min(1.0/max(denom, 1e-3), 50.0)  # limitar amplificacion en resonancia

    armons = [(1, 100), (5, 2.8*m), (7, 1.9*m), (11, 0.9*m), (13, 0.7*m),
              (mf, 18*m), (mf-2, 12*m), (mf+2, 12*m), (2*mf-1, 8*m), (2*mf+1, 8*m)]
    for h, amp in armons:
        f_h = h*f1; att = lcl_att(f_h)
        amp_out = amp*att if f_h > fres else amp
        col = ACC if h == 1 else (ACC2 if h <= 13 else BAD)
        ax.bar(f_h - 30, amp, width=40, color=col, alpha=0.4, label="antes LCL" if h == 1 else "")
        ax.bar(f_h + 30, max(amp_out, 0.05), width=40, color=col, alpha=1.0,
               label="despues LCL" if h == 1 else "")
    ax.axvline(fres, color=OK, ls="--", lw=1.5)
    ax.text(fres+150, 60, f"$f_{{res}}$={fres:.0f} Hz", fontsize=8, color=OK)
    ax.set_yscale("log"); ax.set_ylim(0.05, 200)
    ax.set_xlim(-200, 2.2*mf*f1+200)
    ax.set_xlabel("frecuencia [Hz]"); ax.set_ylabel("amplitud [% fund.]")
    ax.set_title("(b) Efecto del filtro LCL sobre el espectro", fontsize=10)
    handles = [plt.Rectangle((0,0),1,1, color=ACC2, alpha=0.4),
               plt.Rectangle((0,0),1,1, color=ACC2, alpha=1.0)]
    ax.legend(handles, ["antes LCL", "despues LCL"], fontsize=8)

    # --- (c) THD vs Cf ---
    ax = a3
    Cf_arr = np.linspace(5e-6, 40e-6, 80)
    thd_arr = []; fres_arr = []
    for Cf in Cf_arr:
        Leq_c = L1v*L2v/(L1v+L2v)
        fres_c = 1/(2*np.pi*np.sqrt(Leq_c*Cf))
        att_c = (fres_c/fsw)**2
        thd_lo = np.sqrt(2.8**2 + 1.9**2 + 0.9**2 + 0.7**2)
        thd_hi = np.sqrt((18*att_c)**2 + (12*att_c)**2 + (12*att_c)**2)
        thd_arr.append(np.sqrt(thd_lo**2 + thd_hi**2))
        fres_arr.append(fres_c)
    thd_arr = np.array(thd_arr); fres_arr = np.array(fres_arr)
    l1, = ax.plot(Cf_arr*1e6, thd_arr, color=ACC, lw=2, label="THD (%)")
    ax3b = ax.twinx()
    l2, = ax3b.plot(Cf_arr*1e6, fres_arr, color=BAD, lw=2, ls="--", label="$f_{res}$ (Hz)")
    ax.axhline(5.0, color=OK, ls=":", lw=1.5)
    ax.text(32, 5.3, "limite 5%", fontsize=8, color=OK)
    ax3b.axhline(10*f1, color="#bbb", ls=":", lw=1)
    ax3b.axhline(fsw/2, color="#ccc", ls=":", lw=1)
    ax3b.text(2, 10*f1+50, "$10f_1$", fontsize=7.5, color="#bbb")
    ax.set_xlabel("$C_f$ [µF]"); ax.set_ylabel("THD corriente [%]")
    ax3b.set_ylabel("$f_{res}$ [Hz]", color=BAD); ax3b.tick_params(axis="y", labelcolor=BAD)
    ax.set_title("(c) Efecto de $C_f$: mas Cf → menos THD / mas riesgo resonancia", fontsize=10)
    ax.legend([l1, l2], ["THD (%)", "$f_{res}$ (Hz)"], fontsize=8, loc="upper right")

    # --- (d) verificacion vs IEEE 519 ---
    ax = a4
    ordenes = [5, 7, 11, 13, 17, 19, 23, 25, "THD"]
    limites_519 = [12.0, 12.0, 5.5, 5.5, 2.0, 2.0, 1.5, 1.5, 15.0]
    # espectro medido con LCL (estimado para convertidor 1MVA)
    Cf_op = 15e-6; Leq_op = L1v*L2v/(L1v+L2v)
    fres_op = 1/(2*np.pi*np.sqrt(Leq_op*Cf_op)); att_op = (fres_op/fsw)**2
    medidos_raw = [2.5, 1.7, 0.6, 0.5, 0.3, 0.2, 0.1, 0.1]
    thd_med = float(np.sqrt(sum(x**2 for x in medidos_raw)))
    medidos_raw.append(thd_med)
    x_pos = np.arange(len(ordenes)); wb = 0.35
    b1 = ax.bar(x_pos - wb/2, limites_519, wb, color=BAD, alpha=0.6, label="Limite IEEE 519")
    b2 = ax.bar(x_pos + wb/2, medidos_raw, wb, color=ACC, alpha=0.85, label="Medicion (con LCL)")
    for i, (lim, med) in enumerate(zip(limites_519, medidos_raw)):
        if med > lim:
            b2[i].set_edgecolor(BAD); b2[i].set_linewidth(2.5)
    ax.set_xticks(x_pos)
    ax.set_xticklabels([f"h={h}" if isinstance(h, int) else str(h) for h in ordenes], fontsize=8.5)
    ax.set_ylabel("[% $I_1$]")
    ax.set_title("(d) Verificacion vs IEEE 519 (1 MVA + LCL)", fontsize=10)
    ax.legend(fontsize=8); ax.set_ylim(0, 20)
    ax.text(len(ordenes)-1.2, thd_med+0.5, f"THD={thd_med:.1f}%", fontsize=8, color=ACC, ha="center")

    fig.suptitle("Armonicos y THD — espectro PWM, filtro LCL y verificacion IEEE 519",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _savefig(fig, "armonicos-thd-convertidores-analisis.png")


# ===================================================================== #
#  transformador  extended  (sin decorador)
# ===================================================================== #
def _trafo_extended():
    """4 paneles: (a) Icc vs Xcc% exacto vs aproximado,
    (b) curva continua Icc vs Xcc, (c) espectro armonico D-Y, (d) efecto Xcc en Bode LCL."""
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.0))
    a1, a2, a3, a4 = axes.flat

    # (a) Icc vs Xcc%
    Xcc_vals = np.array([4, 6, 8, 10, 12, 15])
    Icc = 100 / Xcc_vals
    bars_x = np.arange(len(Xcc_vals)); width = 0.35
    a1.bar(bars_x - width/2, Icc, width, color=ACC, label="Modelo T exacto (Zm incluido)", alpha=0.85)
    a1.bar(bars_x + width/2, Icc, width, color=BAD, label="Modelo aprox. (sin Zm)", alpha=0.55)
    a1.set_xticks(bars_x); a1.set_xticklabels(["%d%%" % x for x in Xcc_vals])
    a1.set_xlabel("$X_{cc}$ [%]"); a1.set_ylabel("$I_{cc}$ / $I_n$ [veces]")
    a1.set_title("(a) $I_{cc}=100/X_{cc}$: exacto vs aprox. (diferencia < 1%)")
    a1.legend(fontsize=8); a1.grid(True, axis="y", alpha=0.4)
    a1.text(2.5, max(Icc) * 0.62,
            r"$Z_m \approx 50$-$100 \cdot X_{cc}$" + "\nerror I0 < 1%",
            fontsize=8, ha="center", color=OK, bbox=dict(fc="white", ec=OK, alpha=0.8, pad=3))

    # (b) Curva continua Icc vs Xcc%
    xcc_c = np.linspace(1, 20, 300)
    a2.plot(xcc_c, 100/xcc_c, color=ACC, lw=2.4, label=r"$I_{cc}=100/X_{cc}\%$")
    a2.axvspan(4, 8,  color=OK,  alpha=0.15, label="distribucion (4-8%)")
    a2.axvspan(8, 15, color=BAD, alpha=0.10, label="gran potencia (8-15%)")
    for xcc, col, lbl in [(6, OK, "6% -> 16.7x"), (12, BAD, "12% -> 8.3x")]:
        a2.plot(xcc, 100/xcc, "o", color=col, ms=8, zorder=5)
        a2.annotate(lbl, xy=(xcc, 100/xcc), xytext=(xcc+1.5, 100/xcc+1.0),
                    fontsize=8, color=col, arrowprops=dict(arrowstyle="->", color=col))
    a2.set_xlabel(r"$X_{cc}$ [%]"); a2.set_ylabel("$I_{cc}/I_n$")
    a2.set_title("(b) Corriente de cortocircuito vs impedancia de cortocircuito")
    a2.legend(fontsize=8); a2.grid(True, alpha=0.4); a2.set_ylim(0, 40)

    # (c) Espectro armonico antes/despues de trafo D-Y
    armonicos = np.array([1, 3, 5, 7, 9, 11, 13])
    amp_antes   = np.array([1.0, 0.25, 0.20, 0.14, 0.08, 0.09, 0.07])
    amp_despues = amp_antes.copy()
    amp_despues[1] = 0.0   # 3 bloqueado
    amp_despues[4] = 0.0   # 9 bloqueado
    bar_x = np.arange(len(armonicos)); w2 = 0.38
    a3.bar(bar_x - w2/2, amp_antes,   w2, color=BAD, alpha=0.85, label="antes del trafo (D primario)")
    a3.bar(bar_x + w2/2, amp_despues, w2, color=ACC, alpha=0.85, label="despues del trafo (Y secundario)")
    a3.set_xticks(bar_x); a3.set_xticklabels(["%d" % h for h in armonicos])
    a3.set_xlabel("armonico"); a3.set_ylabel("amplitud relativa [pu]")
    a3.set_title("(c) Filtrado de armonicos triples en conexion D-Y (desfase 30)")
    a3.legend(fontsize=8); a3.grid(True, axis="y", alpha=0.4)
    a3.annotate("3 y 9 bloqueados\n(seq. homopolar)", xy=(1, 0.02),
                xytext=(2.5, 0.18), fontsize=8, color=BAD,
                arrowprops=dict(arrowstyle="->", color=BAD))

    # (d) Bode del LCL con Xcc sumada a L2
    f4 = np.logspace(1, 4, 2000); w4 = 2*np.pi*f4
    L1 = 1.5e-3; Cf = 20e-6; L2_base = 0.5e-3
    Sbase = 500e3; Vbase = 690.0; Zbase = Vbase**2/Sbase; omega0 = 2*np.pi*50
    Lcc_6  = (6/100)  * Zbase / omega0
    Lcc_12 = (12/100) * Zbase / omega0
    for L2, col, lbl in [
            (L2_base,          ACC, "sin trafo (L2=0.5 mH)"),
            (L2_base + Lcc_6,  OK,  "+Xcc=6%% -> L2_eff=%.1f mH" % ((L2_base+Lcc_6)*1e3,)),
            (L2_base + Lcc_12, BAD, "+Xcc=12%% -> L2_eff=%.1f mH" % ((L2_base+Lcc_12)*1e3,))]:
        Ltot = L1 + L2
        w_res = np.sqrt(Ltot / (L1*L2*Cf))
        H = (1/Ltot) / np.abs(1 - (w4/w_res)**2 + 1e-10j)
        a4.semilogx(f4, 20*np.log10(H+1e-20), color=col, lw=2.0, label=lbl)
    a4.axhline(0, color="#bbb", ls=":", lw=1)
    a4.set_xlabel("frecuencia [Hz]"); a4.set_ylabel("|G_LCL| [dB]")
    a4.set_title("(d) Bode del LCL: Xcc del trafo aumenta L2_eff y baja f_res")
    a4.legend(fontsize=7.5); a4.grid(True, which="both", alpha=0.4)
    a4.set_ylim(-80, 30); a4.set_xlim(10, 10000)

    fig.suptitle("Transformador: cortocircuito, circuito T, D-Y y efecto en LCL",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    _savefig(fig, "transformador-analisis.png")


# ===================================================================== #
#  componentes-simetricas  extended  (sin decorador)
# ===================================================================== #
def _simetricas_extended():
    """4 paneles: (a) fasorial Fortescue, (b) DSOGI separando secuencias,
    (c) rizado 100Hz en id/iq, (d) magnitudes de secuencia por tipo de falta."""
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.0))
    a1, a2, a3, a4 = axes.flat

    # (a) Diagrama fasorial: terna desequilibrada -> secuencias
    Va = 1.0*np.exp(1j*np.radians(0))
    Vb = 0.7*np.exp(1j*np.radians(-100))
    Vc = 0.9*np.exp(1j*np.radians(130))
    a_op = np.exp(1j*2*np.pi/3)
    Vpos  = (Va + a_op*Vb    + a_op**2*Vc) / 3
    Vneg  = (Va + a_op**2*Vb + a_op*Vc)    / 3
    V0seq = (Va + Vb + Vc) / 3
    for V, col, lbl in [(Va, ACC, "$V_a$"), (Vb, BAD, "$V_b$"), (Vc, OK, "$V_c$")]:
        a1.annotate("", xy=(V.real, V.imag), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=2.2))
        a1.text(V.real*1.15, V.imag*1.15, lbl, color=col, fontsize=10, ha="center")
    for V, col, lbl, mk in [(Vpos, ACC, "$V_+$", "s"), (Vneg, BAD, "$V_-$", "^"),
                             (V0seq, OK, "$V_0$", "o")]:
        a1.annotate("", xy=(V.real, V.imag), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.5, ls="dashed"))
        a1.plot(V.real, V.imag, mk, color=col, ms=8, zorder=5)
        a1.text(V.real*1.22, V.imag*1.22, lbl, color=col, fontsize=9)
    a1.set_xlim(-1.4, 1.4); a1.set_ylim(-1.0, 1.2); a1.set_aspect("equal")
    a1.axhline(0, color="#ddd", lw=0.6); a1.axvline(0, color="#ddd", lw=0.6)
    a1.set_xticks([]); a1.set_yticks([])
    a1.set_title("(a) Fortescue: terna desequilibrada -> secuencias +, -, 0")
    a1.text(-1.3, 1.1, "$a=e^{j120}$", fontsize=8, color="#555")

    # (b) DSOGI: separacion de secuencias
    t_b = np.linspace(0, 3/50, 2000)
    Vp_amp = 0.9; Vn_amp = 0.2
    valpha = Vp_amp*np.cos(2*np.pi*50*t_b) + Vn_amp*np.cos(-2*np.pi*50*t_b)
    vbeta  = Vp_amp*np.sin(2*np.pi*50*t_b) + Vn_amp*np.sin(-2*np.pi*50*t_b)
    qvbeta = -Vp_amp*np.cos(2*np.pi*50*t_b) + Vn_amp*np.cos(-2*np.pi*50*t_b)
    vp_alpha = (valpha - qvbeta) / 2
    vn_alpha = (valpha + qvbeta) / 2
    t_ms_b = t_b*1e3
    a2.plot(t_ms_b, valpha,   color="#aaa", lw=1.2, ls="--", label="valpha (entrada)")
    a2.plot(t_ms_b, vp_alpha, color=ACC,    lw=2.0, label="$V^+_a=(v_a - qv_b)/2$")
    a2.plot(t_ms_b, vn_alpha, color=BAD,    lw=2.0, label="$V^-_a=(v_a + qv_b)/2$")
    a2.axhline(0, color="#eee", lw=0.5)
    a2.set_xlabel("t [ms]"); a2.set_ylabel("tension [pu]")
    a2.set_title("(b) DSOGI: separa $V^+$ y $V^-$ de la senal ab")
    a2.legend(fontsize=8, loc="lower right"); a2.grid(True, alpha=0.3)
    a2.set_xlim(0, t_ms_b[-1])

    # (c) Rizado 100Hz en id/iq con/sin resonante negativo
    t_c = np.linspace(0, 6/50, 3000)
    Vn_c = 0.1; f100 = 100.0
    id_nocomp = 1.0 + Vn_c*np.cos(2*np.pi*f100*t_c)
    iq_nocomp = Vn_c*np.sin(2*np.pi*f100*t_c)
    id_comp   = 1.0 + 0.04*Vn_c*np.cos(2*np.pi*f100*t_c)
    iq_comp   = 0.04*Vn_c*np.sin(2*np.pi*f100*t_c)
    t_ms_c = t_c*1e3
    a3.plot(t_ms_c, id_nocomp, color=BAD, lw=1.8, label="id sin comp. (rizado 100 Hz)")
    a3.plot(t_ms_c, iq_nocomp, color=BAD, lw=1.8, ls="--", label="iq sin comp.")
    a3.plot(t_ms_c, id_comp,   color=ACC, lw=1.8, label="id con resonante neg.")
    a3.plot(t_ms_c, iq_comp,   color=ACC, lw=1.8, ls="--", label="iq con resonante neg.")
    a3.axhline(1.0, color="#ddd", lw=0.8)
    a3.set_xlabel("t [ms]"); a3.set_ylabel("corriente [pu]")
    a3.set_title("(c) Rizado 100 Hz en dq por desequilibrio 10%%: con/sin control de seq. neg.")
    a3.legend(fontsize=7.5, loc="upper right"); a3.grid(True, alpha=0.3)
    a3.set_xlim(0, t_ms_c[-1]); a3.set_ylim(-0.2, 1.35)

    # (d) Magnitudes de secuencia segun tipo de falta
    tipos  = ["Trifasica\n(A-B-C)", "Bifasica\n(B-C)", "Monofasica\n(A-tierra)"]
    vplus  = [0.33, 0.50, 0.67]
    vminus = [0.33, 0.50, 0.33]
    vzero  = [0.33, 0.00, 0.33]
    x_d = np.arange(len(tipos)); w_d = 0.25
    a4.bar(x_d-w_d, vplus,  w_d, color=ACC, label="|V+|", alpha=0.9)
    a4.bar(x_d,     vminus, w_d, color=BAD, label="|V-|", alpha=0.9)
    a4.bar(x_d+w_d, vzero,  w_d, color=OK,  label="|V0|", alpha=0.9)
    a4.set_xticks(x_d); a4.set_xticklabels(tipos, fontsize=9)
    a4.set_ylabel("magnitud secuencia [pu]")
    a4.set_title("(d) Magnitudes de secuencia segun tipo de falta (bornes del bus)")
    a4.legend(fontsize=9); a4.grid(True, axis="y", alpha=0.4); a4.set_ylim(0, 0.85)
    a4.text(2, 0.72, "secuencias iguales\nen falta monofasica", color=BAD, fontsize=8, ha="center")

    fig.suptitle("Componentes simetricas: Fortescue, DSOGI, rizado dq y tipos de falta",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    _savefig(fig, "componentes-simetricas-analisis.png")


# ===================================================================== #
#  transferencia-potencia-linea  extended  (sin decorador)
# ===================================================================== #
def _pdelta_extended():
    """4 paneles: (a) P(d) y Q(d) con Pmax y region estable,
    (b) criterio area igual, (c) perfil de tension linea 100km,
    (d) diagrama P-Q del parque."""
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.0))
    a1, a2, a3, a4 = axes.flat

    # (a) P(d) y Q(d)
    delta = np.linspace(0, np.pi, 400)
    V = 1.0; E = 1.0; X = 0.3
    P = V*E/X * np.sin(delta)
    Q = V*(V - E*np.cos(delta)) / X
    delta0 = np.radians(30)
    P0 = V*E/X * np.sin(delta0)
    Q0 = V*(V - E*np.cos(delta0)) / X
    a1.plot(np.degrees(delta), P, color=ACC, lw=2.4,
            label="$P=(VE/X)\\sin\\delta$ ($P_{max}=%.2f$ pu)" % (V*E/X))
    a1.plot(np.degrees(delta), Q, color=BAD, lw=2.0, ls="--",
            label="$Q=V(V-E\\cos\\delta)/X$")
    a1.axhline(0, color="#ddd", lw=0.7)
    a1.axvspan(0,  90, color=ACC, alpha=0.06, label="estable (dP/dd>0)")
    a1.axvspan(90, 180, color=BAD, alpha=0.06, label="inestable (dP/dd<0)")
    a1.axvline(90, color="#bbb", ls=":")
    a1.plot(np.degrees(delta0), P0, "o", color=ACC, ms=9, zorder=5)
    a1.plot(np.degrees(delta0), Q0, "s", color=BAD, ms=8, zorder=5)
    a1.annotate("d0=30\nP=%.2f" % P0, xy=(30, P0), xytext=(45, P0*0.6),
                fontsize=8, color=ACC, arrowprops=dict(arrowstyle="->", color=ACC))
    a1.set_xlabel("angulo d [deg]"); a1.set_ylabel("[pu de VE/X]")
    a1.set_title("(a) P(d) y Q(d) para linea inductiva (X=0.3 pu, V=E=1)")
    a1.legend(fontsize=7.5, loc="upper right"); a1.grid(True, alpha=0.4)
    a1.set_ylim(-1.5, 4.0)

    # (b) Criterio de area igual
    delta_b = np.linspace(0, np.pi, 600)
    P_b = np.sin(delta_b)
    Pm = 0.5
    delta_s  = np.arcsin(Pm)
    delta_us = np.pi - delta_s
    delta_cl = 0.85
    A1 = Pm*(delta_cl - delta_s)
    d_max_use = delta_us*0.97
    for d_try in np.linspace(delta_cl, delta_us, 500):
        arr = np.linspace(delta_cl, d_try, 200)
        if np.trapz(np.sin(arr) - Pm, arr) >= A1:
            d_max_use = d_try; break
    a2.plot(np.degrees(delta_b), P_b, color="#555", lw=2.2, label="$P_e=\\sin\\delta$")
    a2.axhline(Pm, color=ACC, lw=1.8, ls="--", label="$P_m=%.1f$ pu" % Pm)
    a2.axhline(0, color="#eee", lw=0.6)
    da1 = np.linspace(delta_s, delta_cl, 100)
    a2.fill_between(np.degrees(da1), 0, Pm, color=BAD, alpha=0.35, label="$A_1$ (aceleracion)")
    da2 = np.linspace(delta_cl, d_max_use, 100)
    a2.fill_between(np.degrees(da2), Pm, np.sin(da2), color=ACC, alpha=0.35, label="$A_2$ (desaceleracion)")
    for d_pt, lbl_pt, col_pt in [(delta_s, "ds", ACC), (delta_cl, "dcl", OK), (delta_us, "dus", BAD)]:
        a2.axvline(np.degrees(d_pt), color=col_pt, ls=":", lw=1.2)
        a2.text(np.degrees(d_pt)+1, 1.06, lbl_pt, color=col_pt, fontsize=8)
    a2.set_xlabel("d [deg]"); a2.set_ylabel("P [pu]")
    a2.set_title("(b) Criterio area igual: A1<=A2 -> estable (Pm=%.1f pu)" % Pm)
    a2.legend(fontsize=7.5, loc="upper right"); a2.grid(True, alpha=0.4)
    a2.set_ylim(-0.1, 1.3); a2.set_xlim(0, 200)

    # (c) Perfil de tension a lo largo de linea 100km
    dist = np.linspace(0, 100, 300)
    r_km = 0.1; x_km = 0.35; bc_km = 2.7e-6
    gamma = np.sqrt((r_km + 1j*x_km)*(1j*bc_km))
    P_nom = 0.8; pf = 0.9; Q_nom = P_nom*np.tan(np.arccos(pf))
    V_cargada = np.clip(1.0 - (P_nom*r_km + Q_nom*x_km)*dist/100*0.8, 0.85, 1.0)
    V_ferranti = 1.0 + np.abs(np.cosh(gamma*dist) - 1)*0.4
    a3.plot(dist, np.ones_like(dist), color="#bbb", lw=1.2, ls=":")
    a3.plot(dist, V_cargada,  color=ACC, lw=2.2, label="Con carga (P=0.8 pu, pf=0.9) -> caida")
    a3.plot(dist, V_ferranti, color=BAD, lw=2.2, label="Sin carga -> Ferranti (V sube)")
    a3.axhspan(0.95, 1.05, color=OK, alpha=0.12, label="banda +/-5%")
    a3.annotate("compensacion reactiva", xy=(50, V_cargada[150]),
                xytext=(60, V_cargada[150]+0.035),
                fontsize=8, color=OK, arrowprops=dict(arrowstyle="->", color=OK))
    a3.set_xlabel("distancia [km]"); a3.set_ylabel("tension [pu]")
    a3.set_title("(c) Perfil de tension en linea 100 km: carga vs vacio (Ferranti)")
    a3.legend(fontsize=8); a3.grid(True, alpha=0.4)
    a3.set_ylim(0.80, 1.20); a3.set_xlim(0, 100)

    # (d) Diagrama P-Q del parque
    Sn = 100.0
    P_op = np.linspace(0, 100, 200)
    Q_lim_I  = np.sqrt(np.maximum(Sn**2 - P_op**2, 0))
    Q_lim_dn = -P_op*np.tan(np.radians(35))
    Q_max_vr = 0.6*Sn*np.ones_like(P_op)
    a4.fill_between(P_op, Q_lim_dn, np.minimum(Q_lim_I, Q_max_vr),
                    color=ACC, alpha=0.20, label="region operativa")
    a4.plot(P_op, Q_lim_I,  color=ACC, lw=2.0, label="P^2+Q^2=Sn^2 (lim I)")
    a4.plot(P_op, Q_max_vr, color=BAD, lw=2.0, ls="--", label="Qmax=0.6Sn (V alta)")
    a4.plot(P_op, Q_lim_dn, color=OK,  lw=2.0, ls=":",  label="Qmin (V baja)")
    a4.axhline(0, color="#bbb", lw=0.8)
    a4.plot(80, 30, "o", color=BAD, ms=10, zorder=5)
    a4.annotate("pto. operacion\n(80 MW, 30 MVAR)", xy=(80, 30), xytext=(55, 55),
                fontsize=8, color=BAD, arrowprops=dict(arrowstyle="->", color=BAD))
    a4.set_xlabel("P [MW]"); a4.set_ylabel("Q [MVAR]")
    a4.set_title("(d) Capacidad P-Q del parque 100 MVA")
    a4.legend(fontsize=8, loc="lower left"); a4.grid(True, alpha=0.4)
    a4.set_xlim(0, 105); a4.set_ylim(-50, 70)

    fig.suptitle("Transferencia de potencia: P-d, estabilidad transitoria, perfil V y P-Q",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    _savefig(fig, "transferencia-potencia-linea-analisis.png")


# ===================================================================== #
#  sistema-por-unidad  extended  (sin decorador)
# ===================================================================== #
def _pu_extended():
    """4 paneles: (a) diagrama pu sistema completo, (b) conversion de bases trafo,
    (c) |Z_red_pu|(f) para SCR=2,5,10, (d) LCL en pu con dos bases distintas."""
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.0))
    a1, a2, a3, a4 = axes.flat

    omega0 = 2*np.pi*50; Vbase = 690.0; Sbase_conv = 500e3

    # (a) Diagrama pu del sistema en serie
    SCR = 5.0; Zred_pu = 1/SCR
    Z_trafo_pu = 0.06 * Sbase_conv/1e6
    L1_pu_a = 0.08; C_pu_a = 0.05; L2_pu_a = 0.03
    comps = [("$Z_{red}$", Zred_pu, ACC2), ("$Z_{trafo}$", Z_trafo_pu, ACC),
             ("$L_1$", L1_pu_a, OK), ("$C_f$", C_pu_a, BAD), ("$L_2$", L2_pu_a, OK)]
    left = 0.0
    for lbl, val, col in comps:
        a1.barh(0, val, left=left, color=col, ec="white", height=0.45, alpha=0.9)
        a1.text(left+val/2, 0, "%s\n%.3f" % (lbl, val), ha="center", va="center",
                color="white", fontsize=8.5, weight="bold")
        left += val
    Ztot = sum(v for _, v, _ in comps)
    a1.text(left+0.005, 0, "  Ztot=%.3f pu" % Ztot, va="center", fontsize=9, weight="bold")
    a1.set_xlim(0, 0.50); a1.set_ylim(-0.5, 0.5); a1.set_yticks([])
    a1.set_xlabel("impedancia serie [pu]  (base: 500 kVA / 690 V)")
    a1.set_title("(a) Diagrama pu: Red + Trafo + LCL; no hay factores a^2")

    # (b) Conversion de bases del trafo 1 MVA, Xcc=6%%
    Z_ohm_trafo = 0.06 * Vbase**2/1e6
    bases = [("1 MVA\n(base trafo)", 1e6), ("500 kVA\n(conver.)", 0.5e6), ("10 MVA\n(parque)", 10e6)]
    Z_pu_vals = [Z_ohm_trafo / (Vbase**2/S) for _, S in bases]
    cols_b = [ACC, BAD, OK]; x_b = np.arange(len(bases))
    bars_b = a2.bar(x_b, Z_pu_vals, color=cols_b, alpha=0.85, width=0.5)
    for v, bar in zip(Z_pu_vals, bars_b):
        a2.text(bar.get_x()+bar.get_width()/2, v+0.003, "%.2f%%" % (v*100),
                ha="center", va="bottom", fontsize=10, weight="bold")
    a2.axhline(Z_ohm_trafo, color="#555", ls=":", lw=1.2)
    a2.text(2.55, Z_ohm_trafo+0.003, "Z_ohm=%.4f O\n(invariante)" % Z_ohm_trafo,
            fontsize=8, color="#555")
    a2.set_xticks(x_b); a2.set_xticklabels([b[0] for b in bases], fontsize=8)
    a2.set_ylabel("Z_pu"); a2.set_ylim(0, max(Z_pu_vals)*1.55)
    a2.set_title("(b) Trafo (Zohm=%.4f O) en tres bases: el pu varia" % Z_ohm_trafo)
    a2.grid(True, axis="y", alpha=0.4)

    # (c) |Z_red_pu|(f) para SCR=2,5,10
    f_c = np.logspace(1, 4, 2000); w_c = 2*np.pi*f_c
    for SCR_c, col, ls in [(2, BAD, "-"), (5, ACC, "--"), (10, OK, ":")]:
        Lg_pu = (1/SCR_c)/omega0
        a3.loglog(f_c, w_c*Lg_pu, color=col, lw=2.2, ls=ls,
                  label="SCR=%d -> Zred50=%.2f pu" % (SCR_c, 1/SCR_c))
    a3.axvline(50,   color="#bbb", ls=":", lw=1); a3.text(55,   0.02, "50 Hz",   fontsize=8, color="#555")
    a3.axvline(2500, color="#bbb", ls=":", lw=1); a3.text(2600, 0.01, "2500 Hz", fontsize=8, color="#555")
    a3.set_xlabel("frecuencia [Hz]"); a3.set_ylabel("|Z_red| [pu]")
    a3.set_title("(c) Impedancia de red en pu vs frecuencia para SCR=2,5,10")
    a3.legend(fontsize=8); a3.grid(True, which="both", alpha=0.3); a3.set_xlim(10, 10000)

    # (d) LCL en pu con dos bases: 500 kVA y 1 MVA
    L1_H = 1.5e-3; L2_H = 0.5e-3; Cf_F = 20e-6
    f_d = np.logspace(1, 4, 2000); w_d = 2*np.pi*f_d
    for Sb, col, lbl, ls in [(Sbase_conv, ACC, "base 500 kVA (conver.)", "-"),
                               (1e6,        BAD, "base 1 MVA (trafo)",    "--")]:
        Zb = Vbase**2/Sb; Lb = Zb/omega0; Cb = 1/(omega0*Zb)
        L1p = L1_H/Lb; L2p = L2_H/Lb; Cfp = Cf_F/Cb
        Ltot_p = L1p + L2p
        w_res_p = np.sqrt(Ltot_p/(L1p*L2p*Cfp))
        H_pu = np.abs(1/(Ltot_p*w_d+1e-30)) / np.abs(1 - (w_d/w_res_p)**2 + 1e-9j)
        mag_pu = 20*np.log10(H_pu+1e-30)
        a4.semilogx(f_d, mag_pu, color=col, lw=2.2, ls=ls,
                    label="%s: L1=%.3f L2=%.3f C=%.3f pu  fres=%d Hz  Ltot=%.3f pu"
                          % (lbl, L1p, L2p, Cfp, int(w_res_p/(2*np.pi)), L1p+L2p))
    a4.axhline(0, color="#bbb", ls=":", lw=1)
    a4.axvline(1000, color="#ddd", ls="--", lw=0.8); a4.text(1050, -35, "1 kHz", fontsize=8)
    a4.set_xlabel("frecuencia [Hz]"); a4.set_ylabel("|G_LCL| [dB]")
    a4.set_title("(d) LCL en pu: forma identica, valores distintos segun base")
    a4.legend(fontsize=7.5, loc="lower left"); a4.grid(True, which="both", alpha=0.3)
    a4.set_xlim(10, 10000); a4.set_ylim(-90, 20)

    fig.suptitle("Sistema por unidad: bases, conversion, impedancia de red y LCL en pu",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    _savefig(fig, "sistema-por-unidad-analisis.png")


# ===================================================================== #
#  convertidor-dc-dc-analisis  (sin decorador @figura)
# ===================================================================== #
def _dcdc_extended():
    """4 paneles: (a) corriente iL estado ON/OFF buck + solución promediada,
    (b) Bode de G_vd del buck, (c) Pcrit boost con CPL, (d) Bode lazo corriente."""
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.0))
    (a1, a2), (a3, a4) = axes

    # --- (a) Estados ON/OFF del buck y la solución promediada ---
    fsw = 10e3; T = 1.0/fsw; D = 0.5
    t_on  = np.linspace(0, D*T, 200)
    t_off = np.linspace(D*T, T, 200)
    Vin = 400.0; Vo = D*Vin; L = 100e-6; R = 5.0
    IL = Vo/R  # corriente media
    dIL = (Vin - Vo)*D*T / L  # rizado pico-pico
    # Rampa ON: iL sube con pendiente (Vin-Vo)/L
    iL_on  = IL - dIL/2 + (Vin - Vo)/L * t_on
    # Rampa OFF: iL baja con pendiente -Vo/L
    iL_off = iL_on[-1] + (-Vo/L) * (t_off - D*T)
    t_all  = np.concatenate([t_on, t_off]) * 1e6  # µs
    iL_all = np.concatenate([iL_on, iL_off])
    a1.plot(t_all, iL_all, color=ACC, lw=2.0, label="$i_L$ conmutado")
    a1.axhline(IL, color=BAD, ls="--", lw=1.5, label=f"$\\langle i_L\\rangle={IL:.1f}$ A (promedio)")
    a1.axvline(D*T*1e6, color="#aaa", ls=":", lw=1.2)
    a1.set_xlabel("t [µs]"); a1.set_ylabel("$i_L$ [A]")
    a1.set_title(f"(a) Buck: corriente inductor\n$V_{{in}}$={Vin:.0f} V, D={D}, $f_{{sw}}$={fsw/1e3:.0f} kHz")
    a1.legend(fontsize=9); a1.set_xlim(0, T*1e6)

    # --- (b) Bode de G_vd del buck ---
    # G_vd(s) = Vin / (s^2*L*C + s*L/R + 1)
    C = 470e-6
    num_gvd = [Vin]
    den_gvd = [L*C, L/R, 1.0]
    w, mag, phase = signal.bode(signal.TransferFunction(num_gvd, den_gvd))
    f = w / (2*np.pi)
    fres = 1.0/(2*np.pi*np.sqrt(L*C))
    a2.semilogx(f, mag, color=ACC, lw=2.0)
    a2.axvline(fres, color=BAD, ls="--", lw=1.2, label=f"$f_{{res}}$={fres:.0f} Hz")
    a2.set_xlabel("f [Hz]"); a2.set_ylabel("$|G_{vd}|$ [dB]")
    a2.set_title(f"(b) Bode $G_{{vd}}(s)$ del buck\nL={L*1e6:.0f} µH, C={C*1e6:.0f} µF, R={R} Ω")
    a2.legend(fontsize=9); a2.set_xlim(10, 1e5)

    # --- (c) Pcrit del boost con CPL ---
    # Pcrit = Vout^2 * R_par / L
    # Resistencia incremental negativa: -Vout^2/P, inestable si P > Pcrit
    Vout = 400.0; L_boost = 0.5e-3; R_par_vals = [0.05, 0.1, 0.2]  # Ω
    P_vals = np.linspace(100, 20000, 500)
    for Rp, col, lbl in zip(R_par_vals,
                             [ACC, ACC2, BAD],
                             ["$R_{par}$=0.05 Ω", "$R_{par}$=0.1 Ω", "$R_{par}$=0.2 Ω"]):
        Pcrit = Vout**2 * Rp / L_boost
        stab = np.where(P_vals < Pcrit, 1.0, np.nan)
        unstab = np.where(P_vals >= Pcrit, 1.0, np.nan)
        a3.plot(P_vals/1e3, stab*Pcrit/1e3, color=col, lw=2.0, label=f"{lbl} → $P_{{crit}}$={Pcrit/1e3:.1f} kW")
        a3.axhline(Pcrit/1e3, color=col, ls=":", lw=1.0)
    a3.set_xlabel("P [kW]"); a3.set_ylabel("$P_{crit}$ [kW]")
    a3.set_title(f"(c) Boost CPL: potencia crítica de inestabilidad\n$V_{{out}}$={Vout} V, L={L_boost*1e3:.1f} mH")
    a3.legend(fontsize=8.5)

    # --- (d) Bode lazo interno de corriente (modo corriente) ---
    # Planta corriente: G_id(s) = 1/(sL + R)  con sensor Rs y PWM gain 1/Vtri
    Rs = 0.01; Vtri = 1.0  # ganancia modulador
    Kp_cc = 2.0; Ki_cc = 1000.0
    # PI * Planta con sensor
    # Lazo abierto: L(s) = Kp*(1+Ki/s) * (1/(sL+R)) * Rs/Vtri
    num_plant = [Rs/Vtri]
    den_plant = [L, R]
    num_pi = [Kp_cc, Ki_cc]
    den_pi = [1.0, 0.0]
    num_loop = np.polymul(num_pi, num_plant)
    den_loop = np.polymul(den_pi, den_plant)
    w2, mag2, _ = signal.bode(signal.TransferFunction(num_loop, den_loop))
    f2 = w2/(2*np.pi)
    a4.semilogx(f2, mag2, color=ACC, lw=2.0, label="$|L(j\\omega)|$")
    a4.axhline(0, color="#888", ls="--", lw=1.0)
    a4.set_xlabel("f [Hz]"); a4.set_ylabel("Magnitud [dB]")
    a4.set_title("(d) Bode lazo corriente (modo corriente)\nPI × $G_{id}$ × sensor")
    a4.legend(fontsize=9); a4.set_xlim(10, fsw/2)

    fig.suptitle("Convertidor DC-DC: espacio de estados, Bode $G_{vd}$, CPL y lazo de corriente",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    _savefig(fig, "convertidor-dc-dc-analisis.png")


# ===================================================================== #
#  fotovoltaica-mppt-analisis  (sin decorador @figura)
# ===================================================================== #
def _pv_extended():
    """4 paneles: (a) curvas I-V y P-V a distintas G y T,
    (b) P&O oscilando en el MPP, (c) P&O vs InC nubosidad, (d) eficiencia vs ΔV."""
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.0))
    (a1, a2), (a3, a4) = axes

    # Parámetros STC del módulo (genérico)
    Iph_STC = 8.5; I0 = 1e-10; n = 1.3; Rs = 0.3; Rsh = 300.0
    Vt_STC = 0.02585  # kT/q a 25 °C (298 K)
    Ns = 72  # células en serie

    def iv_curve(G_frac, T_C):
        """Devuelve (V, I) para irradiancia G_frac·STC y temperatura T_C [°C]."""
        T_K = T_C + 273.15
        Vt = 1.38e-23 * T_K / 1.6e-19
        Iph = Iph_STC * G_frac * (1 + 0.0004*(T_C - 25))
        I0_T = I0 * (T_K/298)**3 * np.exp(1.1/(n*Vt) - 1.1/(n*Vt_STC))
        V = np.linspace(0, Ns*0.65, 500)
        I = np.zeros_like(V)
        for k, Vk in enumerate(V):
            # Newton para I implícito
            Iv = Iph
            for _ in range(30):
                f  = Iph - I0_T*(np.exp((Vk + Iv*Rs)/(n*Ns*Vt)) - 1) - (Vk + Iv*Rs)/Rsh - Iv
                df = -I0_T*Rs/(n*Ns*Vt)*np.exp((Vk + Iv*Rs)/(n*Ns*Vt)) - Rs/Rsh - 1
                dI = -f/df
                Iv += dI
                if abs(dI) < 1e-9:
                    break
            I[k] = max(Iv, 0.0)
        return V, I

    # (a) Curvas I-V y P-V
    cases = [(1.0, 25, ACC,  "1000 W/m², 25°C"),
             (0.5, 25, ACC2, "500 W/m², 25°C"),
             (0.2, 25, BAD,  "200 W/m², 25°C"),
             (1.0, 50, "#9b59b6", "1000 W/m², 50°C")]
    ax_p = a1.twinx()
    for G, T, col, lbl in cases:
        V, I = iv_curve(G, T)
        P = V*I
        a1.plot(V, I, color=col, lw=1.8, label=lbl)
        ax_p.plot(V, P, color=col, lw=1.2, ls="--")
    a1.set_xlabel("V [V]"); a1.set_ylabel("I [A]", color="#222")
    ax_p.set_ylabel("P [W]", color="#555"); ax_p.tick_params(colors="#555")
    a1.set_title("(a) Curvas I-V (sólido) y P-V (trazado)\npara distintas G y T")
    a1.legend(fontsize=8); a1.set_xlim(0, None); a1.set_ylim(bottom=0)

    # (b) P&O: oscilación alrededor del MPP
    V_ref, P_prev, V_prev = 30.0, 0.0, 29.0
    dV = 1.5
    V_traj, P_traj, ref_traj = [], [], []
    V_iv, I_iv = iv_curve(0.8, 30)
    P_iv = V_iv * I_iv
    for k in range(40):
        I_now = np.interp(V_ref, V_iv, I_iv)
        P_now = V_ref * I_now
        ref_traj.append(V_ref)
        V_traj.append(V_ref); P_traj.append(P_now)
        signDP = np.sign(P_now - P_prev) if abs(P_now - P_prev) > 0.01 else 0
        signDV = np.sign(V_ref - V_prev)
        step = dV * (signDP * signDV if signDP != 0 else 1)
        V_prev = V_ref; P_prev = P_now
        V_ref = np.clip(V_ref + step, 10, 45)
    a2.plot(V_iv, P_iv, color="#aaa", lw=1.5, label="curva P-V")
    a2.scatter(V_traj[::2], P_traj[::2], color=ACC, s=20, zorder=5, label="iteraciones P&O")
    mpp_idx = np.argmax(P_iv)
    a2.scatter([V_iv[mpp_idx]], [P_iv[mpp_idx]], color=BAD, s=80, zorder=6, marker="*", label="MPP real")
    a2.set_xlabel("V [V]"); a2.set_ylabel("P [W]")
    a2.set_title(f"(b) P&O: oscilación ±ΔV={dV} V alrededor del MPP\n800 W/m², 30°C")
    a2.legend(fontsize=8.5)

    # (c) P&O vs InC bajo nubosidad variable
    Ts = 0.05  # s por paso de control
    t_sim = np.arange(0, 300)*Ts
    G_profile = np.ones(300)*1.0
    G_profile[60:80]  = np.linspace(1.0, 0.3, 20)
    G_profile[80:120] = 0.3
    G_profile[120:140]= np.linspace(0.3, 0.9, 20)
    G_profile[140:180]= 0.9
    G_profile[180:200]= np.linspace(0.9, 0.5, 20)
    G_profile[200:]   = 0.5

    def run_mppt(algo):
        Vr = 30.0; Pp = 0; Vp = 29.0; P_out = []
        for G in G_profile:
            Vi, Ii = iv_curve(G, 25)
            Pi = Vi*Ii
            I_now = np.interp(Vr, Vi, Ii)
            P_now = Vr * I_now
            if algo == 'po':
                sDp = np.sign(P_now - Pp) if abs(P_now-Pp)>0.05 else 0
                sDv = np.sign(Vr - Vp)
                step = dV*(sDp*sDv if sDp != 0 else 1)
            else:  # inc
                I_dV  = np.interp(Vr+0.01, Vi, Ii)
                dIdV  = (I_dV - I_now)/0.01
                cond  = dIdV + I_now/Vr if Vr > 0 else 0
                step  = -np.sign(cond) * dV if abs(cond) > 0.01 else 0
            Vp = Vr; Pp = P_now
            Vr = np.clip(Vr + step, 10, 45)
            P_out.append(P_now)
        return np.array(P_out)

    P_po  = run_mppt('po')
    P_inc = run_mppt('inc')
    # Potencia óptima real
    P_opt = np.array([np.max(iv_curve(g,25)[0]*iv_curve(g,25)[1]) for g in G_profile])
    a3.plot(t_sim, P_opt, color="#aaa", lw=1.5, ls="--", label="$P_{MPP}$ real")
    a3.plot(t_sim, P_po,  color=ACC2, lw=1.8, label="P&O")
    a3.plot(t_sim, P_inc, color=ACC,  lw=1.8, label="InC")
    a3.set_xlabel("t [s]"); a3.set_ylabel("P [W]")
    a3.set_title("(c) P&O vs InC bajo nubosidad variable\nIrradiancia cambia en escalones")
    a3.legend(fontsize=9)

    # (d) Eficiencia de seguimiento vs paso ΔV
    dV_vals = np.array([0.1, 0.3, 0.5, 0.8, 1.0, 1.5, 2.0, 3.0, 5.0])
    eta_vals = []
    V_iv0, I_iv0 = iv_curve(1.0, 25)
    P_iv0 = V_iv0*I_iv0
    Pmax0 = np.max(P_iv0)
    for dvv in dV_vals:
        Vr2 = 30.0; Pp2 = 0; Vp2 = 29.0; Ps = []
        for _ in range(200):
            In = np.interp(Vr2, V_iv0, I_iv0)
            Pn = Vr2*In
            sDp = np.sign(Pn-Pp2) if abs(Pn-Pp2)>0.01 else 0
            sDv = np.sign(Vr2-Vp2)
            st = dvv*(sDp*sDv if sDp != 0 else 1)
            Vp2 = Vr2; Pp2 = Pn
            Vr2 = np.clip(Vr2+st, 5, 45)
            if _ > 50:
                Ps.append(Pn)
        eta_vals.append(100*np.mean(Ps)/Pmax0)
    a4.semilogx(dV_vals, eta_vals, color=ACC, lw=2.0, marker="o", ms=6)
    a4.set_xlabel("Paso ΔV [V]"); a4.set_ylabel("Eficiencia MPPT [%]")
    a4.set_title("(d) Eficiencia de seguimiento P&O vs paso ΔV\n1000 W/m², 25°C, régimen permanente")
    a4.set_ylim(90, 101)

    fig.suptitle("Sistema fotovoltaico: curvas I-V/P-V, P&O, comparativa MPPT y eficiencia",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    _savefig(fig, "fotovoltaica-mppt-analisis.png")


# ===================================================================== #
#  eolica-mppt-analisis  (sin decorador @figura)
# ===================================================================== #
def _mppt_extended():
    """4 paneles: (a) Cp(λ) para β=0,5,10°, (b) P(ωr) para distintos vientos con MPP,
    (c) T*(ωr) parábola OTC, (d) respuesta MPPT a ráfaga: ωr(t), P(t)."""
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.0))
    (a1, a2), (a3, a4) = axes

    # Parámetros de la turbina 2 MW
    R_turb = 45.0; rho = 1.225; A = np.pi*R_turb**2
    lam_opt = 8.0; Cp_max = 0.48
    k_opt = 0.5 * rho * A * Cp_max * (R_turb/lam_opt)**3

    def cp_model(lam, beta):
        """Modelo analítico de Cp(lambda, beta) — forma típica de la literatura."""
        lam_i = 1.0/(lam + 0.08*beta) - 0.035/(beta**3 + 1)
        lam_i = np.where(lam_i < 1e-6, 1e-6, lam_i)
        c1,c2,c3,c4,c5,c6 = 0.5176, 116.0, 0.4, 5.0, 21.0, 0.0068
        return c1*(c2/lam_i - c3*beta - c4)*np.exp(-c5/lam_i) + c6*lam

    # (a) Cp(λ) para β = 0°, 5°, 10°
    lam_arr = np.linspace(1, 15, 300)
    for beta, col, lbl in [(0, ACC, "β=0°"), (5, ACC2, "β=5°"), (10, BAD, "β=10°")]:
        Cp_arr = cp_model(lam_arr, beta)
        Cp_arr = np.clip(Cp_arr, 0, 1)
        a1.plot(lam_arr, Cp_arr, color=col, lw=2.0, label=lbl)
    # Límite de Betz
    a1.axhline(16/27, color="#aaa", ls=":", lw=1.2, label="Límite Betz 0.593")
    a1.scatter([lam_opt], [Cp_max], color=BAD, s=100, zorder=6, marker="*")
    a1.set_xlabel("λ = ωr·R/v"); a1.set_ylabel("$C_p$")
    a1.set_title(f"(a) Curva $C_p(\\lambda)$ para distintos ángulos de paso β\n$C_p^{{max}}$={Cp_max}, λ*={lam_opt}")
    a1.legend(fontsize=9); a1.set_ylim(0, 0.65)

    # (b) P(ωr) para v = 6, 8, 10, 12 m/s
    wr_arr = np.linspace(0.1, 2.5, 300)  # rad/s (mecánico, R=45m)
    v_rated = 12.5  # m/s
    P_rated = 2e6
    cols_v = [ACC, ACC2, BAD, "#9b59b6"]
    mpp_wr = []; mpp_P = []
    for v_w, col, lbl in zip([6, 8, 10, 12], cols_v,
                               ["v=6 m/s","v=8 m/s","v=10 m/s","v=12 m/s"]):
        lam_v = wr_arr * R_turb / v_w
        Cp_v  = np.clip(cp_model(lam_v, 0), 0, 1)
        P_v   = 0.5*rho*A*v_w**3*Cp_v
        P_v   = np.clip(P_v, 0, P_rated)
        a2.plot(wr_arr, P_v/1e6, color=col, lw=1.8, label=lbl)
        # MPP: lam = lam_opt → wr = lam_opt*v_w/R
        wr_mpp = lam_opt*v_w/R_turb
        P_mpp  = min(0.5*rho*A*v_w**3*Cp_max, P_rated)
        mpp_wr.append(wr_mpp); mpp_P.append(P_mpp/1e6)
    # Locus OTC P=k_opt*ωr³
    P_otc = k_opt * wr_arr**3
    a2.plot(wr_arr, np.clip(P_otc, 0, 2.0)/1e6, color="#444", lw=1.5, ls="--", label="Locus MPPT")
    a2.scatter(mpp_wr, mpp_P, color=BAD, s=80, zorder=6, marker="*")
    a2.set_xlabel("$\\omega_r$ [rad/s]"); a2.set_ylabel("P [MW]")
    a2.set_title("(b) Curvas P(ωr) por velocidad de viento\ny locus MPPT (OTC)")
    a2.legend(fontsize=8.5); a2.set_ylim(0, 2.2)

    # (c) T*(ωr) parábola OTC
    wr_arr2 = np.linspace(0.1, 2.5, 300)
    T_otc   = k_opt * wr_arr2**2
    a3.plot(wr_arr2, T_otc/1e6, color=ACC, lw=2.0, label="$T^*=k_{opt}\\omega_r^2$")
    # Líneas iso-potencia
    for P_iso, col2 in [(0.5e6, "#ccc"), (1.0e6, "#aaa"), (2.0e6, "#888")]:
        T_iso = P_iso / wr_arr2
        a3.plot(wr_arr2, T_iso/1e6, color=col2, lw=1.0, ls=":")
    a3.set_xlabel("$\\omega_r$ [rad/s]"); a3.set_ylabel("$T^*$ [MN·m]")
    a3.set_title("(c) Control OTC: parábola $T^*=k_{opt}\\omega_r^2$\n(líneas punteadas: iso-potencia 0.5/1/2 MW)")
    a3.legend(fontsize=9); a3.set_xlim(0.1, 2.5); a3.set_ylim(0, 1.0)

    # (d) Respuesta dinámica a ráfaga de viento
    Ht = 4.0; Hg = 0.7; omega0 = 1.0  # pu
    Ts_sim = 0.05; t_dyn = np.arange(0, 60, Ts_sim)
    # Viento: escalón suave 8 → 11 m/s a t=10 s
    v_wind = np.where(t_dyn < 10, 8.0,
             np.where(t_dyn < 15, 8.0 + 3.0*(t_dyn-10)/5, 11.0))
    wr_sim = 8.0*lam_opt/R_turb * np.ones(len(t_dyn))
    P_sim  = np.zeros(len(t_dyn))
    wr_now = 8.0*lam_opt/R_turb
    for k in range(1, len(t_dyn)):
        v_k = v_wind[k]
        lam_k = wr_now*R_turb/v_k
        Cp_k  = max(0, cp_model(lam_k, 0))
        T_aero = 0.5*rho*A*v_k**3*Cp_k / max(wr_now, 0.01)
        T_e    = k_opt * wr_now**2
        # Ecuación de movimiento (2H·dω/dt = T_aero - T_e) aprox masa total
        H_tot = Ht + Hg
        dwr = (T_aero - T_e) / (2*H_tot) * Ts_sim
        wr_now = max(0.1, wr_now + dwr)
        wr_sim[k] = wr_now
        P_sim[k]  = T_e * wr_now
    ax_wr = a4
    ax_P2 = a4.twinx()
    ax_wr.plot(t_dyn, wr_sim, color=ACC, lw=2.0, label="$\\omega_r$ [rad/s]")
    ax_P2.plot(t_dyn, P_sim/1e6, color=ACC2, lw=2.0, ls="--", label="P [MW]")
    ax_wr.set_xlabel("t [s]"); ax_wr.set_ylabel("$\\omega_r$ [rad/s]", color=ACC)
    ax_P2.set_ylabel("P [MW]", color=ACC2)
    ax_wr.set_title("(d) Respuesta MPPT a ráfaga 8→11 m/s\n$\\omega_r(t)$ sube; $P(t)$ sigue el óptimo")
    lines1, labels1 = ax_wr.get_legend_handles_labels()
    lines2, labels2 = ax_P2.get_legend_handles_labels()
    ax_wr.legend(lines1+lines2, labels1+labels2, fontsize=9)

    fig.suptitle("Turbina eólica: $C_p(\\lambda)$, curvas P(ωr), OTC y respuesta dinámica MPPT",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    _savefig(fig, "eolica-mppt-analisis.png")


# ===================================================================== #
#  modelo-bateria-bess-analisis  (sin decorador @figura)
# ===================================================================== #
def _bess_extended():
    """4 paneles: (a) circuito Thevenin esquemático (texto), (b) OCV(SOC) LiFePO4,
    (c) SOC y Vterm durante ciclo 1C, (d) inercia virtual DC."""
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.0))
    (a1, a2), (a3, a4) = axes

    # (a) Circuito Thevenin — representación con texto y formas
    a1.set_xlim(0, 10); a1.set_ylim(0, 6); a1.axis("off")
    a1.set_title("(a) Circuito equivalente Thevenin 1-RC\ncelda Li-ion")
    # Fuente OCV
    circ_ocv = plt.Circle((1.5, 3), 0.7, fill=False, color=ACC, lw=2)
    a1.add_patch(circ_ocv)
    a1.text(1.5, 3, "OCV\n(SOC)", ha="center", va="center", fontsize=8.5, color=ACC)
    # R0
    rect_r0 = plt.Rectangle((3.0, 2.7), 1.0, 0.6, fill=True, facecolor="#e8e8e8",
                              edgecolor="#444", lw=1.5)
    a1.add_patch(rect_r0)
    a1.text(3.5, 3.0, "$R_0$", ha="center", va="center", fontsize=10)
    # R1 C1 paralelo
    rect_r1 = plt.Rectangle((5.5, 3.4), 0.8, 0.5, fill=True, facecolor="#e8e8e8",
                              edgecolor="#444", lw=1.5)
    a1.add_patch(rect_r1)
    a1.text(5.9, 3.65, "$R_1$", ha="center", va="center", fontsize=10)
    # Condensador C1
    for dx in [-0.12, 0.12]:
        a1.plot([5.9+dx, 5.9+dx], [1.5, 2.5], color="#444", lw=3)
    a1.text(6.5, 2.0, "$C_1$", ha="center", va="center", fontsize=10)
    # Bornes
    a1.plot([0.5, 0.8], [3, 3], color="#444", lw=2)  # hilo izq
    a1.plot([2.2, 3.0], [3, 3], color="#444", lw=2)
    a1.plot([4.0, 5.5], [3.65, 3.65], color="#444", lw=2)
    a1.plot([4.0, 5.5], [2.35, 2.35], color="#444", lw=2)
    a1.plot([6.3, 8.5], [3, 3], color="#444", lw=2)
    a1.plot([8.5, 8.5], [2.0, 4.0], color="#444", lw=2)
    a1.plot([0.5, 0.5], [1.5, 3.0], color="#444", lw=2)
    a1.plot([0.5, 8.5], [1.5, 1.5], color="#444", lw=2)
    # Etiquetas
    a1.text(8.8, 3.0, "$V_{term}$", fontsize=11, va="center", color=BAD, fontweight="bold")
    a1.text(5.9, 1.0, "$V_{RC}$\n(difusión)", ha="center", va="center", fontsize=8, color="#666")
    a1.text(3.5, 1.0, "← Corriente I →", ha="center", va="center", fontsize=8, color="#555")

    # (b) OCV(SOC) para LiFePO4
    SOC_arr = np.linspace(0, 1, 200)
    # Curva OCV LiFePO4 aproximada (forma típica plana en el centro)
    OCV_arr = (3.20 + 0.30*SOC_arr
               + 0.08*np.exp(-15*(SOC_arr - 0.05))
               - 0.08*np.exp(-15*(0.95 - SOC_arr))
               + 0.05*np.tanh(10*(SOC_arr - 0.5)))
    a2.plot(SOC_arr*100, OCV_arr, color=ACC, lw=2.5)
    a2.axhline(3.65, color=BAD, ls="--", lw=1.2, label="3.65 V (carga plena)")
    a2.axhline(3.20, color=ACC2, ls="--", lw=1.2, label="3.20 V (descargada)")
    a2.set_xlabel("SOC [%]"); a2.set_ylabel("OCV [V]")
    a2.set_title("(b) Curva OCV(SOC) — LiFePO4\nregión central muy plana (~3.30–3.35 V)")
    a2.legend(fontsize=9); a2.set_xlim(0, 100)

    # (c) SOC(t) y Vterm(t) durante ciclo 1C
    Qnom = 100.0  # Ah
    R0 = 0.003; R1 = 0.005; C1 = 5000.0  # tau = 25 s
    I_1C = Qnom  # 100 A = 1C
    Ts_b = 1.0  # s
    t_cycle = np.arange(0, 7200+Ts_b, Ts_b)
    SOC_sim = np.zeros(len(t_cycle)); Vrc_sim = np.zeros(len(t_cycle))
    Vt_sim  = np.zeros(len(t_cycle))
    SOC_sim[0] = 0.2
    # Descarga 1C 0→3600s, reposo 3600→4200s, carga 1C 4200→7200s
    def get_I(t):
        if t < 3600: return  I_1C      # descarga
        if t < 4200: return  0.0       # reposo
        return -I_1C                   # carga (corriente negativa = carga)
    for k in range(1, len(t_cycle)):
        I = get_I(t_cycle[k-1])
        if SOC_sim[k-1] < 0.05 and I > 0: I = 0.0
        if SOC_sim[k-1] > 0.98 and I < 0: I = 0.0
        OCV_k = np.interp(SOC_sim[k-1], SOC_arr, OCV_arr)
        Vrc_k = Vrc_sim[k-1] + (I*R1 - Vrc_sim[k-1])/(R1*C1) * Ts_b
        Vt_k  = OCV_k - I*R0 - Vrc_k
        SOC_k = SOC_sim[k-1] - I/(Qnom*3600) * Ts_b
        SOC_sim[k] = np.clip(SOC_k, 0, 1); Vrc_sim[k] = Vrc_k; Vt_sim[k] = Vt_k
    ax_soc = a3; ax_vt = a3.twinx()
    ax_soc.plot(t_cycle/3600, SOC_sim*100, color=ACC, lw=2.0, label="SOC [%]")
    ax_vt.plot(t_cycle/3600,  Vt_sim, color=ACC2, lw=1.8, ls="--", label="$V_{term}$ [V]")
    ax_soc.set_xlabel("t [h]"); ax_soc.set_ylabel("SOC [%]", color=ACC)
    ax_vt.set_ylabel("$V_{term}$ [V]", color=ACC2)
    a3.set_title("(c) Ciclo 1C: descarga → reposo → carga\nSOC(t) e Vterm(t)")
    lines1, l1 = ax_soc.get_legend_handles_labels()
    lines2, l2 = ax_vt.get_legend_handles_labels()
    ax_soc.legend(lines1+lines2, l1+l2, fontsize=9)

    # (d) BESS como inercia virtual — respuesta a escalón de carga
    Cdc = 0.05  # F equivalente (200 kWh ≡ H=4s → Ceq grande)
    Vdc0 = 800.0  # V bus DC
    Pload0 = 0.0; Pload1 = 100e3  # escalón 100 kW
    Rd = 0.02; Vdc_ref = Vdc0
    Ts_dc = 1e-4; t_dc = np.arange(0, 0.5, Ts_dc)
    Vdc_arr = np.zeros(len(t_dc)); Id_arr = np.zeros(len(t_dc))
    Vdc_arr[0] = Vdc0
    for k in range(1, len(t_dc)):
        Pload = Pload1 if t_dc[k] >= 0.05 else 0.0
        Iload = Pload / max(Vdc_arr[k-1], 1.0)
        # Droop: el BESS inyecta corriente según la caída de tensión
        Id_bess = (Vdc_arr[k-1] - Vdc_ref) / (-Rd) if Vdc_arr[k-1] < Vdc_ref else 0
        Id_bess = np.clip(Id_bess, 0, 300)
        Id_arr[k] = Id_bess
        dVdc = (Id_bess - Iload) / Cdc * Ts_dc
        Vdc_arr[k] = Vdc_arr[k-1] + dVdc
    ax_vdc = a4; ax_id = a4.twinx()
    ax_vdc.plot(t_dc*1e3, Vdc_arr, color=ACC, lw=2.0, label="$V_{dc}$ [V]")
    ax_id.plot(t_dc*1e3,  Id_arr,  color=BAD,  lw=1.8, ls="--", label="$i_d$ BESS [A]")
    ax_vdc.set_xlabel("t [ms]"); ax_vdc.set_ylabel("$V_{dc}$ [V]", color=ACC)
    ax_id.set_ylabel("$i_d$ [A]", color=BAD)
    a4.set_title("(d) BESS soporte bus DC: droop $R_d$=0.02 Ω\nEscalón de carga 100 kW")
    lines1, l1 = ax_vdc.get_legend_handles_labels()
    lines2, l2 = ax_id.get_legend_handles_labels()
    ax_vdc.legend(lines1+lines2, l1+l2, fontsize=9)

    fig.suptitle("Modelo batería BESS: circuito Thevenin, OCV(SOC), ciclo 1C e inercia virtual DC",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    _savefig(fig, "modelo-bateria-bess-analisis.png")


# ===================================================================== #
#  armonicos-thd-convertidores-analisis  (sin decorador @figura)
# ===================================================================== #
def _thd_extended():
    """4 paneles: (a) espectro FFT antes/después LCL, (b) THD_I acumulado por orden,
    (c) THD vs Cf, (d) verificación vs IEEE 519."""
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.0))
    (a1, a2), (a3, a4) = axes

    f1 = 50.0; fsw = 10e3; Vdc = 800.0; m = 0.85
    # --- Generar señal SPWM sintética ---
    fs = 200e3; N = int(fs/f1)*20  # 20 ciclos
    t = np.arange(N)/fs
    # Fundamental
    Vfund = m * Vdc/2 * np.sqrt(2)
    sig = Vfund * np.sin(2*np.pi*f1*t)
    # Armónicos de conmutación en k*fsw ± 2, k*fsw ± 4 (orden impar de mf)
    mf = int(fsw/f1)  # = 200
    for k in [1, 2, 3]:
        A_k = Vdc/np.pi / k * 0.7  # amplitud aproximada banda lateral
        for offset in [-2, 2]:
            fh = k*fsw + offset*f1
            if fh > 0:
                sig += A_k * np.sin(2*np.pi*fh*t)
    # Armónicos bajos (tiempo muerto)
    for h_ord, amp_frac in [(5, 0.04), (7, 0.03), (11, 0.015), (13, 0.01)]:
        sig += Vfund * amp_frac * np.sin(2*np.pi*h_ord*f1*t)

    # FFT
    win = np.hanning(N)
    X = np.abs(np.fft.rfft(sig*win)) * 2.0/N
    freq = np.fft.rfftfreq(N, 1.0/fs)

    # Filtro LCL (aproximación): -60 dB/dec por encima de fres
    L1 = 1e-3; L2 = 0.5e-3; Cf = 10e-6
    fres_lcl = 1.0/(2*np.pi*np.sqrt((L1+L2)*Cf))
    def lcl_atten(f):
        """Atenuación del LCL |G(jω)| ≈ 1 para f<fres, (fres/f)^3 para f>fres."""
        rat = fres_lcl / np.maximum(f, 1.0)
        return np.where(f < fres_lcl, 1.0, rat**3)
    X_after = X * lcl_atten(freq)

    # (a) Espectro antes y después del LCL
    f_kHz = freq/1e3
    mask = freq <= 35e3
    a1.semilogy(f_kHz[mask], np.maximum(X[mask], 1e-3), color=BAD, lw=1.5,
                label="antes del LCL", alpha=0.85)
    a1.semilogy(f_kHz[mask], np.maximum(X_after[mask], 1e-3), color=ACC, lw=1.5,
                label="después del LCL", alpha=0.85)
    a1.axvline(fres_lcl/1e3, color="#aaa", ls=":", lw=1.2,
               label=f"$f_{{res}}$={fres_lcl/1e3:.1f} kHz")
    a1.axvline(fsw/1e3, color=ACC2, ls="--", lw=1.2, label=f"$f_{{sw}}$={fsw/1e3:.0f} kHz")
    a1.set_xlabel("f [kHz]"); a1.set_ylabel("|X(f)| [V]")
    a1.set_title(f"(a) Espectro SPWM: $f_{{sw}}$={fsw/1e3:.0f} kHz, m={m}\nantes (rojo) y después (azul) del LCL")
    a1.legend(fontsize=8.5)

    # (b) Contribución por orden al THD (acumulado)
    I_fund_est = Vfund / 50.0  # corriente estimada (R=50Ω)
    harm_orders = np.arange(2, 50)
    thd_contrib = []
    for h in harm_orders:
        fh = h*f1
        idx = np.argmin(np.abs(freq - fh))
        Ih = X_after[idx] / 50.0
        thd_contrib.append(Ih)
    thd_contrib = np.array(thd_contrib)
    thd_cumul   = 100*np.sqrt(np.cumsum(thd_contrib**2)) / (Vfund/50.0)
    a2.bar(harm_orders, 100*thd_contrib/(Vfund/50.0), color=ACC, alpha=0.7, label="aporte por orden")
    a2.plot(harm_orders, thd_cumul, color=BAD, lw=2.0, label="THD acumulado [%]")
    a2.axhline(5.0, color="#888", ls="--", lw=1.2, label="Límite 5 % IEEE 519")
    a2.set_xlabel("Orden armónico h"); a2.set_ylabel("[%]")
    a2.set_title("(b) Contribución por orden al THD_I (tras LCL)\nlos 5º y 7º dominan a baja frecuencia")
    a2.legend(fontsize=8.5); a2.set_xlim(2, 50)

    # (c) THD vs Cf (mayor Cf → más atenuación → menor THD, pero fres baja)
    Cf_vals = np.logspace(-6, -4, 40)  # 1 µF … 100 µF
    thd_cf = []
    for Cf_v in Cf_vals:
        fres_v = 1.0/(2*np.pi*np.sqrt((L1+L2)*Cf_v))
        Ih_sq_sum = 0.0
        for h in range(2, 60):
            fh = h*f1
            A_h = X[np.argmin(np.abs(freq - fh))] if fh <= freq[-1] else 0
            rat = fres_v/max(fh, 1.0)
            att = 1.0 if fh < fres_v else rat**3
            Ih_sq_sum += (A_h*att)**2
        thd_cf.append(100*np.sqrt(Ih_sq_sum)/(Vfund))
    a3.semilogx(Cf_vals*1e6, thd_cf, color=ACC, lw=2.0)
    # Marcar fres para algunos Cf
    for Cf_mark, col_m in [(5e-6, BAD), (10e-6, ACC2), (50e-6, "#9b59b6")]:
        fr_m = 1.0/(2*np.pi*np.sqrt((L1+L2)*Cf_mark))
        a3.scatter([Cf_mark*1e6], [np.interp(Cf_mark*1e6, Cf_vals*1e6, thd_cf)],
                   color=col_m, s=70, zorder=5, label=f"$C_f$={Cf_mark*1e6:.0f} µF → $f_{{res}}$={fr_m/1e3:.1f} kHz")
    a3.axhline(5.0, color="#888", ls="--", lw=1.2, label="Límite 5 %")
    a3.set_xlabel("$C_f$ [µF]"); a3.set_ylabel("THD [%]")
    a3.set_title("(c) THD vs capacidad de filtro $C_f$\nmayor $C_f$ reduce THD pero baja $f_{res}$")
    a3.legend(fontsize=8); a3.set_ylim(0, 30)

    # (d) Verificación vs IEEE 519 — barras por orden
    # IEEE 519: ISC/IL > 100 → límites más relajados  (usamos tabla corta)
    ieee519_limits = {5: 12.0, 7: 5.5, 11: 5.5, 13: 5.0, 17: 2.0, 19: 1.5, 23: 0.3, 25: 0.3}
    orders_check = sorted(ieee519_limits.keys())
    vals_pct = []
    lims_pct = []
    for h in orders_check:
        fh = h*f1
        idx = np.argmin(np.abs(freq - fh))
        Ih_pct = 100*X_after[idx]/Vfund
        vals_pct.append(Ih_pct)
        lims_pct.append(ieee519_limits[h])
    x_pos = np.arange(len(orders_check))
    bars = a4.bar(x_pos, vals_pct, color=[OK if v<l else BAD for v,l in zip(vals_pct, lims_pct)],
                  alpha=0.8, label="THD individual [%]")
    a4.plot(x_pos, lims_pct, color="#444", marker="^", ms=8, lw=0, label="Límite IEEE 519 [%]")
    a4.set_xticks(x_pos); a4.set_xticklabels([str(h) for h in orders_check])
    a4.set_xlabel("Orden armónico"); a4.set_ylabel("[%]")
    a4.set_title("(d) Verificación vs IEEE 519-2014\nverde=cumple, rojo=viola (con LCL diseñado)")
    a4.legend(fontsize=9)

    fig.suptitle("Armónicos y THD: espectro SPWM, contribución por orden, efecto $C_f$ y límites IEEE 519",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    _savefig(fig, "armonicos-thd-convertidores-analisis.png")


# ===================================================================== #
#  antiresonancia — análisis extendido (4 paneles)
# ===================================================================== #
def _antires_extended():
    """4 paneles: (a) Bode iL2/vi con far y fres, (b) admitancia de entrada del LCL,
    (c) efecto de L2 en far, (d) ratio fres/far vs r=L2/L1."""
    L1, L2, Cf = 2e-3, 1e-3, 20e-6
    R1, R2 = 0.05, 0.05
    f_ar  = 1/(2*np.pi*np.sqrt(L2*Cf))
    f_res = (1/(2*np.pi))*np.sqrt((L1+L2)/(L1*L2*Cf))
    f = np.logspace(1, 4.3, 3000); w = 2*np.pi*f
    s = 1j*w

    # Funciones de transferencia analíticas LCL
    def lcl_tf(s, L1, L2, Cf, R1, R2):
        # numerador de i1/vi y i2/vi, denominador común
        ZCf = R2 + 1.0/(s*Cf)
        Z2  = R1 + s*L1
        # admitancia total
        D = Z2 + ZCf*(s*L2 + ZCf) / (s*L2 + ZCf + ZCf) if False else None
        # Estado-espacio → usar formulación directa
        num_i2 = 1.0/(s*L1 + R1 + 1.0/(s*Cf + 1.0/(s*L2+R2)))
        return num_i2   # no usado, reemplazado por StateSpace

    A = np.array([[-R1/L1, 0,     -1/L1],
                  [ 0,     -R2/L2, 1/L2],
                  [ 1/Cf,  -1/Cf,  0  ]])
    B = np.array([[1/L1], [0], [0]])
    sys_i2 = signal.StateSpace(A, B, np.array([[0,1,0]]), [[0]])
    sys_i1 = signal.StateSpace(A, B, np.array([[1,0,0]]), [[0]])

    _, mag_i2, ph_i2 = signal.bode(sys_i2, w)
    _, mag_i1, ph_i1 = signal.bode(sys_i1, w)

    # Admitancia de entrada Y_in = i1/vi (misma que sys_i1 arriba)
    # Admitancia analítica del paralelo L2||Cf (rama que produce el cero)
    Y_par = s*Cf + 1.0/(s*L2 + R2)  # admitancia del paralelo Cf-L2
    Y_par_dB = 20*np.log10(np.abs(Y_par) + 1e-20)

    fig, axes = plt.subplots(2, 2, figsize=(11.0, 8.0))
    ax_a, ax_b, ax_c, ax_d = axes[0,0], axes[0,1], axes[1,0], axes[1,1]

    # (a) Bode de i2/vi mostrando far y fres
    ax_a.semilogx(f, mag_i2, color=ACC, lw=2, label="$i_{L2}/v_i$ (corriente red)")
    ax_a.semilogx(f, mag_i1, color=ACC2, lw=2, ls="--", label="$i_{L1}/v_i$ (corriente fuente, ref.)")
    ax_a.axvline(f_ar,  color=ACC2, ls=":", lw=1.5)
    ax_a.axvline(f_res, color=BAD,  ls="--", lw=1.5)
    ax_a.text(f_ar*0.93, -65, f"$f_{{ar}}$={f_ar:.0f} Hz", color=ACC2, fontsize=8.5, ha="right")
    ax_a.text(f_res*1.04, 20, f"$f_{{res}}$={f_res:.0f} Hz", color=BAD, fontsize=8.5)
    ax_a.set_xlabel("frecuencia [Hz]"); ax_a.set_ylabel("magnitud [dB]")
    ax_a.set_title("(a) Bode $i_{L2}/v_i$: pico en $f_{res}$, sin valle")
    ax_a.legend(fontsize=8.5); ax_a.set_ylim(-90, 45)

    # (b) Admitancia de entrada del LCL: cero en far
    ax_b.semilogx(f, Y_par_dB, color=OK, lw=2, label="$Y_{par}(C_f\\|L_2)$ — el cero")
    ax_b.semilogx(f, mag_i1, color=ACC2, lw=2, ls="--", label="$i_{L1}/v_i$ — valle en $f_{ar}$")
    ax_b.axvline(f_ar,  color=ACC2, ls=":", lw=1.5)
    ax_b.axvline(f_res, color=BAD,  ls="--", lw=1.5)
    ax_b.text(f_ar*0.93, -5, f"$f_{{ar}}$={f_ar:.0f} Hz", color=ACC2, fontsize=8.5, ha="right")
    ax_b.set_xlabel("frecuencia [Hz]"); ax_b.set_ylabel("magnitud [dB]")
    ax_b.set_title("(b) Admitancia $C_f\\|L_2$: infinita en $f_{ar}$ → cero de $i_{L1}$")
    ax_b.legend(fontsize=8.5); ax_b.set_ylim(-80, 40)

    # (c) Efecto de L2 en far: si L2 baja, far sube
    L2_vals = np.array([0.5e-3, 1e-3, 2e-3])
    cols_c = [BAD, ACC, OK]
    for L2v, col in zip(L2_vals, cols_c):
        far_v  = 1/(2*np.pi*np.sqrt(L2v*Cf))
        fres_v = (1/(2*np.pi))*np.sqrt((L1+L2v)/(L1*L2v*Cf))
        Av = np.array([[-R1/L1, 0,       -1/L1],
                       [ 0,    -R2/L2v,   1/L2v],
                       [ 1/Cf, -1/Cf,     0   ]])
        sys_v = signal.StateSpace(Av, B, np.array([[1,0,0]]), [[0]])
        _, mag_v, _ = signal.bode(sys_v, w)
        ax_c.semilogx(f, mag_v, color=col, lw=2,
                      label=f"$L_2$={L2v*1e3:.1f} mH  ($f_{{ar}}$={far_v:.0f} Hz)")
        ax_c.axvline(far_v, color=col, ls=":", lw=1.2)
    ax_c.set_xlabel("frecuencia [Hz]"); ax_c.set_ylabel("magnitud [dB]")
    ax_c.set_title("(c) Efecto de $L_2$ en $f_{ar}=1/(2\\pi\\sqrt{L_2C_f})$")
    ax_c.legend(fontsize=8.5); ax_c.set_ylim(-90, 45)

    # (d) Ratio fres/far vs r=L2/L1: verifica la fórmula sqrt(1+1/r)
    r = np.linspace(0.1, 3.0, 300)
    ratio_teorico = np.sqrt(1 + 1/r)
    # verificación numérica para varios r
    r_pts = np.array([0.25, 0.5, 1.0, 2.0])
    ratio_num = []
    for rv in r_pts:
        L2v = L1*rv
        far_v  = 1/(2*np.pi*np.sqrt(L2v*Cf))
        fres_v = (1/(2*np.pi))*np.sqrt((L1+L2v)/(L1*L2v*Cf))
        ratio_num.append(fres_v/far_v)
    ax_d.plot(r, ratio_teorico, color=ACC, lw=2, label=r"$\sqrt{1+1/r}$ (analítica)")
    ax_d.scatter(r_pts, ratio_num, color=BAD, zorder=4, s=60, label="valores numéricos")
    ax_d.axhline(1.0, color="#aaa", lw=0.8, ls=":")
    ax_d.set_xlabel("$r = L_2/L_1$"); ax_d.set_ylabel("$f_{res}/f_{ar}$")
    ax_d.set_title("(d) Ratio $f_{res}/f_{ar}=\\sqrt{1+L_1/L_2}$: siempre >1")
    ax_d.legend(fontsize=8.5)
    ax_d.text(1.5, 1.45, r"siempre $f_{ar}<f_{res}$", fontsize=9, color="#555")

    fig.suptitle("Antiresonancia en el LCL: $f_{ar}$, admitancia de entrada y ratio $f_{res}/f_{ar}$",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    _savefig(fig, "antiresonancia-analisis.png")


# ===================================================================== #
#  amortiguamiento-pasivo-vs-activo — análisis extendido (4 paneles)
# ===================================================================== #
def _amort_pasivo_activo_extended():
    """4 paneles: (a) Bode sin amort / Rd_opt / Kad, (b) Q vs Rd,
    (c) pérdidas en Rd vs ICf, (d) Bode lazo de corriente con Kad: margen de fase."""
    L1, L2, Cf = 2e-3, 1e-3, 20e-6
    R1, R2 = 0.05, 0.05
    w_res = np.sqrt((L1+L2)/(L1*L2*Cf))
    f_res = w_res/(2*np.pi)
    Rd_opt = 1/(3*w_res*Cf)

    f = np.logspace(1, 4.3, 3000); w_f = 2*np.pi*f
    s = 1j*w_f

    # Función de transferencia i2/vi con Rd en serie con Cf
    def tf_i2_rd(Rd):
        ZCf_Rd = Rd + 1.0/(s*Cf)
        Z_par  = ZCf_Rd * (1j*w_f*L2 + R2) / (ZCf_Rd + 1j*w_f*L2 + R2)
        Ztot   = R1 + 1j*w_f*L1 + Z_par
        # corriente i2: divisor de corriente
        i2_norm = ZCf_Rd / (ZCf_Rd + 1j*w_f*L2 + R2) / Ztot
        return i2_norm

    def tf_i2_kad(Kad):
        # Kad actúa como resistencia virtual en L1: reemplaza R1 → R1+Kad
        ZCf = 1.0/(s*Cf)
        Z_par = ZCf*(1j*w_f*L2 + R2) / (ZCf + 1j*w_f*L2 + R2)
        Ztot  = (R1+Kad) + 1j*w_f*L1 + Z_par
        i2_norm = ZCf / (ZCf + 1j*w_f*L2 + R2) / Ztot
        return i2_norm

    tf0     = tf_i2_rd(0.0)
    tf_rd   = tf_i2_rd(Rd_opt)
    tf_kad  = tf_i2_kad(Rd_opt)   # Kad = Rd_opt para comparativa equitativa

    fig, axes = plt.subplots(2, 2, figsize=(11.0, 8.0))
    ax_a, ax_b, ax_c, ax_d = axes[0,0], axes[0,1], axes[1,0], axes[1,1]

    # (a) Bode i2/vi para los tres casos
    for tf, col, lab in [(tf0, BAD, "sin amortiguamiento"),
                         (tf_rd,  ACC,  f"$R_d$={Rd_opt:.2f} Ω (pasivo óptimo)"),
                         (tf_kad, OK,   f"$K_{{ad}}$={Rd_opt:.2f} Ω (activo)")]:
        mag = 20*np.log10(np.abs(tf) + 1e-20)
        ax_a.semilogx(f, mag, color=col, lw=2, label=lab)
    ax_a.axvline(f_res, color="#888", ls="--", lw=1.2)
    ax_a.text(f_res*1.04, -25, f"$f_{{res}}$={f_res:.0f} Hz", fontsize=8.5, color="#555")
    ax_a.set_xlabel("frecuencia [Hz]"); ax_a.set_ylabel("magnitud [dB]")
    ax_a.set_title("(a) Bode $i_{L2}/v_i$: pasivo vs activo vs sin amortiguamiento")
    ax_a.legend(fontsize=8); ax_a.set_ylim(-90, 45)

    # (b) Q resultante vs Rd para amortiguamiento pasivo
    Rd_arr = np.linspace(0.01, 5.0, 400)
    zeta_arr = 0.5*Rd_arr*np.sqrt(Cf*(L1+L2)/(L1*L2))
    Q_arr    = 1.0/(2*zeta_arr)
    ax_b.plot(Rd_arr, Q_arr, color=ACC2, lw=2)
    ax_b.axvline(Rd_opt, color=BAD, ls="--", lw=1.5)
    ax_b.axhline(1/(2*(1/(6))), color=OK, ls=":", lw=1.2)
    ax_b.text(Rd_opt+0.05, Q_arr.max()*0.85, f"$R_d^*$={Rd_opt:.2f} Ω\n$Q$≈3", fontsize=8.5, color=BAD)
    ax_b.set_xlabel("$R_d$ [Ω]"); ax_b.set_ylabel("$Q = 1/(2\\zeta)$")
    ax_b.set_title("(b) $Q$ vs $R_d$ — el óptimo da $Q\\approx3$ ($\\zeta\\approx1/6$)")
    ax_b.set_ylim(0, 15)

    # (c) Pérdidas vs amplitud de ICf
    Icf_rms = np.linspace(0, 5, 300)   # A
    for Rd_v, col, lab in [(Rd_opt, ACC, f"$R_d$={Rd_opt:.2f} Ω"),
                           (2*Rd_opt, BAD, f"$R_d$={2*Rd_opt:.2f} Ω"),
                           (0, "#aaa", "activo ($K_{{ad}}$): P=0")]:
        P = Rd_v * Icf_rms**2
        ax_c.plot(Icf_rms, P, color=col, lw=2, label=lab)
    ax_c.set_xlabel("$I_{C_f,rms}$ [A]"); ax_c.set_ylabel("$P_{R_d}$ [W]")
    ax_c.set_title("(c) Pérdidas $P=R_d\\cdot I_{C_f}^2$: activo no disipa")
    ax_c.legend(fontsize=8.5)

    # (d) Bode lazo de corriente con Kad: margen de fase antes y después
    # Lazo de corriente: planta (i1/vi con Kad), PI
    Kp, Ki = 5.0, 1000.0
    def pi_tf(s): return Kp + Ki/s

    s_d = 1j*w_f
    # planta i1/vi sin Kad
    A_m = np.array([[-R1/L1, 0,     -1/L1],
                    [ 0,    -R2/L2,  1/L2],
                    [ 1/Cf, -1/Cf,   0  ]])
    B_m = np.array([[1/L1], [0], [0]])
    sys_p = signal.StateSpace(A_m, B_m, np.array([[1,0,0]]), [[0]])
    _, _, _ = signal.bode(sys_p, w_f)
    # approximación: ZOH retardo 1.5*Ts, Ts=1/10e3
    Ts = 1/10e3
    delay = np.exp(-1j*w_f*1.5*Ts)

    for Kad, col, lab in [(0.0, BAD, "sin $K_{ad}$"),
                          (Rd_opt, OK, f"$K_{{ad}}$={Rd_opt:.2f} Ω")]:
        ZCf    = 1.0/(s_d*Cf)
        Zpar   = ZCf*(s_d*L2+R2)/(ZCf+s_d*L2+R2)
        plant  = 1.0 / ((R1+Kad) + s_d*L1 + Zpar)
        L_open = pi_tf(s_d) * plant * delay
        mag_l  = 20*np.log10(np.abs(L_open) + 1e-20)
        ph_l   = np.angle(L_open, deg=True)
        # solo magnitud en ax_d
        ax_d.semilogx(f, ph_l, color=col, lw=2, label=lab)
    ax_d.axhline(-180, color="#888", ls="--", lw=1)
    ax_d.axhline(-135, color="#aaa", ls=":", lw=1)
    ax_d.text(2e3, -133, "−135° (PM=45°)", fontsize=8, color="#777")
    ax_d.set_xlabel("frecuencia [Hz]"); ax_d.set_ylabel("fase lazo abierto [°]")
    ax_d.set_title("(d) Fase lazo de corriente: $K_{ad}$ mejora margen de fase en $f_{res}$")
    ax_d.legend(fontsize=8.5); ax_d.set_ylim(-300, 10)

    fig.suptitle("Amortiguamiento pasivo vs activo: Bode, Q, pérdidas y margen de fase",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    _savefig(fig, "amortiguamiento-pasivo-vs-activo-analisis.png")


# ===================================================================== #
#  deteccion-islanding — análisis extendido (4 paneles)
# ===================================================================== #
def _ndz_extended():
    """4 paneles: (a) NDZ en plano P-Q, (b) f(t) ante islanding con/sin ROCOF,
    (c) AFD: perturbación de frecuencia, (d) trade-off ROCOF threshold."""
    from matplotlib.patches import Rectangle, FancyArrowPatch
    fig, axes = plt.subplots(2, 2, figsize=(11.0, 8.0))
    ax_a, ax_b, ax_c, ax_d = axes[0,0], axes[0,1], axes[1,0], axes[1,1]

    # (a) NDZ en el plano P-Q
    dP = np.linspace(-0.5, 0.5, 300)
    dQ = np.linspace(-0.35, 0.35, 300)
    DPg, DQg = np.meshgrid(dP, dQ)
    # OUF: |dP| < 0.15 → f dentro de 47-53 Hz
    # OUV: |dQ| < 0.06
    ndz_mask = (np.abs(DPg) < 0.15) & (np.abs(DQg) < 0.06)
    ax_a.contourf(dP, dQ, ndz_mask.astype(float), levels=[0.5, 1.5], colors=[BAD], alpha=0.25)
    ax_a.contour(dP, dQ, ndz_mask.astype(float), levels=[0.5], colors=[BAD], linewidths=1.5)
    ax_a.axhline(0, color="#aaa", lw=0.8); ax_a.axvline(0, color="#aaa", lw=0.8)
    ax_a.text(0, 0, "NDZ\n(OUF/OUV no\ndetectan)", ha="center", va="center",
              color=BAD, fontsize=9, weight="bold")
    ax_a.scatter([0.3], [0.2], color=OK, s=60, zorder=4)
    ax_a.text(0.31, 0.21, "se detecta", fontsize=8.5, color=OK)
    ax_a.set_xlabel("$\\Delta P/P$ (→ $\\Delta f$)"); ax_a.set_ylabel("$\\Delta Q/Q$ (→ $\\Delta V$)")
    ax_a.set_title("(a) Zona de no detección (NDZ): métodos pasivos OUF/OUV")

    # (b) Respuesta de f(t) ante islanding: sin detección vs ROCOF a 200 ms
    t = np.linspace(0, 1.0, 2000)
    # Parámetros: DP=0.05 pu, H=5 s, f0=50 Hz
    H, f0, DP = 5.0, 50.0, 0.05
    rocof_val = DP*f0/(2*H)      # Hz/s
    # Sin detección: f(t) deriva linealmente hasta que la carga frena
    tau_load = 0.5
    f_nodect = 50.0 + rocof_val * t * np.exp(-t/tau_load)  # deriva amortiguada por la carga
    # Con ROCOF: dispara a t=0.2 s
    t_trip = 0.20
    f_rocof = np.where(t < t_trip, 50.0 + rocof_val*t, np.nan)
    ax_b.plot(t, f_nodect, color=BAD, lw=2, label="sin detección (se estabiliza en isla)")
    ax_b.plot(t, f_rocof, color=OK, lw=2.5, label=f"ROCOF: dispara a t={t_trip} s")
    ax_b.axvline(t_trip, color=OK, ls="--", lw=1.2)
    ax_b.axhline(50.0, color="#aaa", ls=":", lw=1)
    thresh_f = 50.0 + 0.5*t_trip
    ax_b.axhline(thresh_f, color="#888", ls=":", lw=1)
    ax_b.text(0.55, thresh_f+0.005, f"umbral f={thresh_f:.3f} Hz", fontsize=8, color="#555")
    ax_b.set_xlabel("t [s]"); ax_b.set_ylabel("frecuencia [Hz]")
    ax_b.set_title("(b) $f(t)$ ante islanding: ROCOF dispara en 200 ms")
    ax_b.legend(fontsize=8.5)

    # (c) AFD: perturbación de frecuencia que provoca la deriva en isla
    t2 = np.linspace(0, 0.5, 2000)
    f_ref = 50.0 * np.ones_like(t2)
    # En isla, AFD amplifica la perturbación
    k_afd = 0.08   # ganancia del SFS
    # Isla: f(t) con SFS (positive feedback)
    f_isla_afd = np.zeros_like(t2)
    f_isla_afd[0] = 50.0
    dt2 = t2[1]-t2[0]
    for i in range(1, len(t2)):
        rocof_i = (f_isla_afd[i-1] - 50.0)*2.0 + 0.05*50.0/(2*5.0)
        f_isla_afd[i] = f_isla_afd[i-1] + dt2*(rocof_i*(1+k_afd))
        if f_isla_afd[i] > 52: f_isla_afd[i] = 52.0; break
    # En red: la red absorbe la perturbación, f queda estable
    f_red_afd = 50.0 + 0.02*np.sin(2*np.pi*5*t2)*np.exp(-10*t2)
    ax_c.plot(t2, f_red_afd, color=OK, lw=2, label="en red (AFD absorbido)")
    ax_c.plot(t2, f_isla_afd, color=BAD, lw=2, label="en isla (AFD amplifica → escapa)")
    ax_c.axhline(52.0, color="#888", ls="--", lw=1); ax_c.text(0.02, 52.05, "límite OUF 52 Hz", fontsize=8)
    ax_c.axhline(48.0, color="#888", ls="--", lw=1)
    ax_c.set_xlabel("t [s]"); ax_c.set_ylabel("frecuencia [Hz]")
    ax_c.set_title("(c) AFD (Sandia Freq. Shift): en isla la frecuencia escapa del rango")
    ax_c.legend(fontsize=8.5); ax_c.set_ylim(49.5, 53.5)

    # (d) Trade-off ROCOF threshold: sensibilidad vs falsas alarmas
    thresh = np.linspace(0.1, 3.0, 300)
    # tiempo de detección decrece con umbral bajo
    DP_nominal = 0.05
    t_det = 2*H*(thresh)/(DP_nominal*f0)    # t_det = thresh / ROCOF_real
    # falsa alarma: prob proporcional a 1/thresh (normalizada)
    false_alarm = 1.0/thresh / (1.0/thresh[0])
    ax_d.plot(thresh, t_det, color=ACC, lw=2, label="tiempo detección [s]")
    ax_d2 = ax_d.twinx()
    ax_d2.plot(thresh, false_alarm, color=BAD, lw=2, ls="--", label="falsa alarma [norm.]")
    ax_d.axvline(0.5, color="#888", ls=":", lw=1.5)
    ax_d.text(0.52, t_det.max()*0.85, "típico\n0.5 Hz/s", fontsize=8.5, color="#555")
    ax_d.set_xlabel("umbral ROCOF [Hz/s]"); ax_d.set_ylabel("tiempo detección [s]", color=ACC)
    ax_d2.set_ylabel("falsa alarma [norm.]", color=BAD)
    ax_d.set_title("(d) Trade-off umbral ROCOF: sensibilidad vs inmunidad")
    lines1, labels1 = ax_d.get_legend_handles_labels()
    lines2, labels2 = ax_d2.get_legend_handles_labels()
    ax_d.legend(lines1+lines2, labels1+labels2, fontsize=8.5)

    fig.suptitle("Detección de islanding: NDZ, ROCOF, AFD y trade-off de umbral",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    _savefig(fig, "deteccion-islanding-analisis.png")


# ===================================================================== #
#  fenomenos-oscilatorios-red — análisis extendido (4 paneles)
# ===================================================================== #
def _sso_extended():
    """4 paneles: (a) mapa de frecuencias, (b) modo inter-área 0.5 Hz y GFM damping,
    (c) SSR con y sin compensación serie, (d) resonancia armónica alta frec."""
    fig, axes = plt.subplots(2, 2, figsize=(11.0, 8.0))
    ax_a, ax_b, ax_c, ax_d = axes[0,0], axes[0,1], axes[1,0], axes[1,1]

    # (a) Mapa de frecuencias de los distintos fenómenos
    fenomenos = [
        (0.1, 2.0, "Oscilaciones inter-área\n(0.1–2 Hz)", ACC),
        (1.0, 3.0, "Modos locales\n(1–3 Hz)", ACC2),
        (5.0, 50.0, "SSR / SSCI\n(5–50 Hz)", BAD),
        (100.0, 3000.0, "Armónica HF\n(100–3000 Hz)", OK),
    ]
    for i, (f_lo, f_hi, lab, col) in enumerate(fenomenos):
        ax_a.barh(i, np.log10(f_hi)-np.log10(f_lo), left=np.log10(f_lo),
                  color=col, alpha=0.7, height=0.6)
        ax_a.text(np.log10(f_lo)+0.05, i, lab, va="center", fontsize=8.5, color="#111")
    ax_a.set_xlim(-1.5, 4.0)
    ax_a.set_xticks([-1, 0, 1, 2, 3, 4])
    ax_a.set_xticklabels(["0.1", "1", "10", "100", "1k", "10k"])
    ax_a.set_xlabel("frecuencia [Hz] (escala log)"); ax_a.set_yticks([])
    ax_a.set_title("(a) Mapa de fenómenos oscilatorios de red por banda de frecuencia")

    # (b) Modo inter-área de 0.5 Hz y GFM lo amortigua
    t = np.linspace(0, 6.0, 3000)
    f_ia = 0.5; zeta_red = 0.02; zeta_gfm = 0.12
    wd_red = 2*np.pi*f_ia * np.sqrt(1 - zeta_red**2)
    wd_gfm = 2*np.pi*f_ia * np.sqrt(1 - zeta_gfm**2)
    p_red = np.exp(-zeta_red*2*np.pi*f_ia*t) * np.sin(wd_red*t)
    p_gfm = np.exp(-zeta_gfm*2*np.pi*f_ia*t) * np.sin(wd_gfm*t)
    ax_b.plot(t, p_red, color=BAD, lw=2, label=f"sin GFM ($\\zeta$={zeta_red})")
    ax_b.plot(t, p_gfm, color=OK,  lw=2, label=f"con GFM ($\\zeta$={zeta_gfm})")
    ax_b.axhline(0, color="#aaa", lw=0.8)
    ax_b.set_xlabel("t [s]"); ax_b.set_ylabel("oscilación de potencia $P$ [pu]")
    ax_b.set_title("(b) Modo inter-área 0.5 Hz: el GFM inyecta amortiguamiento")
    ax_b.legend(fontsize=8.5)

    # (c) SSR: espectro de corriente con y sin compensación serie
    N = 4096; dt_c = 1e-3; t_c = np.arange(N)*dt_c
    f_red = 50.0; comp_pct = 40.0; XL = 1.0; XCs = comp_pct/100*XL
    fn_sub = f_red*np.sqrt(XCs/XL)   # ~31.6 Hz
    # con compensación: componente subsíncrona + fundamental
    cur_comp = (np.sin(2*np.pi*f_red*t_c) +
                0.3*np.exp(1.5*t_c)*np.sin(2*np.pi*fn_sub*t_c))
    cur_comp = np.clip(cur_comp, -3, 3)
    # sin compensación: solo fundamental
    cur_nocomp = np.sin(2*np.pi*f_red*t_c)
    from numpy.fft import rfft, rfftfreq
    F_c  = np.abs(rfft(cur_comp))/N
    F_nc = np.abs(rfft(cur_nocomp))/N
    freqs_c = rfftfreq(N, dt_c)
    mask = freqs_c < 120
    ax_c.plot(freqs_c[mask], F_nc[mask], color=OK,  lw=2, label="sin comp. serie")
    ax_c.plot(freqs_c[mask], F_c[mask],  color=BAD, lw=1.5, label=f"con comp. serie ({comp_pct:.0f}%): SSR en {fn_sub:.1f} Hz")
    ax_c.axvline(fn_sub, color=BAD, ls="--", lw=1.2)
    ax_c.text(fn_sub+1, F_c[mask].max()*0.55, f"$f_n$={fn_sub:.1f} Hz", fontsize=8.5, color=BAD)
    ax_c.set_xlabel("frecuencia [Hz]"); ax_c.set_ylabel("amplitud [pu]")
    ax_c.set_title("(c) SSR: pico subsíncrono con compensación serie activa")
    ax_c.legend(fontsize=8.5)

    # (d) Resonancia armónica: cable-condensador excitada por PWM
    f_arr = np.logspace(1, 4.5, 2000)
    # Resonancia paralela de cable (Lg=1mH) con Cg (capacidad cable 5µF)
    Lg, Cg = 1e-3, 5e-6
    f_res_harm = 1/(2*np.pi*np.sqrt(Lg*Cg))
    w_arr = 2*np.pi*f_arr
    Znet = np.abs(1j*w_arr*Lg / (1 - w_arr**2*Lg*Cg + 1e-3j*w_arr*Lg))  # resonancia paralela
    # Espectro PWM: harmónicos en k*fsw +/- m*f0
    fsw = 2000.0
    harmonics_pwm = [fsw, fsw-100, fsw+100, 2*fsw]
    ax_d.semilogy(f_arr, Znet, color=ACC, lw=2, label="$|Z_{red}|$ cable-transformador")
    ax_d.axvline(f_res_harm, color=BAD, ls="--", lw=1.5)
    ax_d.text(f_res_harm*1.05, Znet.max()*0.5, f"$f_{{res}}$={f_res_harm:.0f} Hz", fontsize=8.5, color=BAD)
    for fh in harmonics_pwm:
        ax_d.axvline(fh, color=OK, ls=":", lw=1.2)
    ax_d.text(fsw*1.02, 0.02, f"$f_{{sw}}$={fsw:.0f} Hz", fontsize=8, color=OK, rotation=90)
    ax_d.set_xlabel("frecuencia [Hz]"); ax_d.set_ylabel("|Z| [Ω]")
    ax_d.set_title(f"(d) Resonancia armónica HF ({f_res_harm:.0f} Hz): cable excitado por PWM")
    ax_d.legend(fontsize=8.5)

    fig.suptitle("Fenómenos oscilatorios de red: mapa de frecuencias, inter-área, SSR y armónica HF",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    _savefig(fig, "fenomenos-oscilatorios-red-analisis.png")


# ===================================================================== #
#  series-taylor — análisis extendido (4 paneles)
# ===================================================================== #
def _taylor_extended():
    """4 paneles: (a) sin(x) y aprox Taylor ord 1,3,5,7, (b) e^x convergencia,
    (c) P(delta)=EV/X*sin(delta) y aprox lineal, (d) CPL i=P/V y linealización."""
    fig, axes = plt.subplots(2, 2, figsize=(11.0, 8.0))
    ax_a, ax_b, ax_c, ax_d = axes[0,0], axes[0,1], axes[1,0], axes[1,1]

    # (a) sin(x) y aproximaciones de Taylor orden 1, 3, 5, 7
    x = np.linspace(-np.pi*1.1, np.pi*1.1, 600)
    sin_exact = np.sin(x)
    p1 = x
    p3 = x - x**3/6
    p5 = x - x**3/6 + x**5/120
    p7 = x - x**3/6 + x**5/120 - x**7/5040
    ax_a.plot(x, sin_exact, color="#222", lw=2.5, label="sin(x) exacta")
    for p, col, lab in [(p1, BAD, "ord 1: $x$"),
                        (p3, ACC2, "ord 3: $x-x^3/6$"),
                        (p5, ACC, "ord 5"),
                        (p7, OK, "ord 7")]:
        ax_a.plot(x, np.clip(p, -2, 2), color=col, lw=1.8, ls="--", label=lab)
    ax_a.axhline(0, color="#aaa", lw=0.8); ax_a.axvline(0, color="#aaa", lw=0.8)
    ax_a.set_ylim(-2, 2); ax_a.set_xlabel("x [rad]"); ax_a.set_ylabel("valor")
    ax_a.set_title("(a) sin(x): cada orden adicional extiende la validez")
    ax_a.legend(fontsize=8)

    # (b) e^x y su serie truncada: convergencia vs número de términos
    x2 = np.linspace(-1, 3, 500)
    ex_exact = np.exp(x2)
    orders = [1, 2, 3, 5]
    cols_b = [BAD, ACC2, ACC, OK]
    ax_b.plot(x2, ex_exact, color="#222", lw=2.5, label="$e^x$ exacta")
    from math import factorial
    for n, col in zip(orders, cols_b):
        p = sum(x2**k / factorial(k) for k in range(n+1))
        ax_b.plot(x2, np.clip(p, -1, 25), color=col, lw=1.8, ls="--", label=f"orden {n}")
    ax_b.set_ylim(-1, 22); ax_b.set_xlabel("x"); ax_b.set_ylabel("$e^x$")
    ax_b.set_title("(b) $e^x$: convergencia mejora con más términos (cerca de x=0)")
    ax_b.legend(fontsize=8.5)

    # (c) P(delta)=EV/X*sin(delta) y la aproximación lineal para distintos delta0
    E, V, X_l = 1.0, 1.0, 0.3
    P_max = E*V/X_l
    delta = np.linspace(0, np.pi/2, 400)
    P_exact = P_max * np.sin(delta)
    ax_c.plot(np.degrees(delta), P_exact, color="#222", lw=2.5, label="$P(\\delta)=\\frac{EV}{X}\\sin\\delta$")
    for d0_deg, col in [(15, OK), (30, ACC2), (45, BAD)]:
        d0 = np.radians(d0_deg)
        Ks = P_max*np.cos(d0)
        P0 = P_max*np.sin(d0)
        P_lin = P0 + Ks*(delta - d0)
        err_pct = np.abs(P_lin - P_exact)/P_max * 100
        ax_c.plot(np.degrees(delta), P_lin, color=col, lw=1.8, ls="--",
                  label=f"lineal $\\delta_0$={d0_deg}° ($K_s$={Ks:.2f})")
    ax_c.set_xlabel("$\\delta$ [°]"); ax_c.set_ylabel("$P$ [pu]")
    ax_c.set_title("(c) Linealización de $P(\\delta)$: $K_s=EV/X\\cdot\\cos\\delta_0$")
    ax_c.legend(fontsize=8.5)

    # (d) CPL: i(V)=P/V y su linealización
    P_cpl = 1.0   # W (constante)
    V_range = np.linspace(0.5, 2.0, 400)
    i_exact = P_cpl / V_range
    V0 = 1.0; i0 = P_cpl/V0; slope = -P_cpl/V0**2
    i_lin = i0 + slope*(V_range - V0)
    ax_d.plot(V_range, i_exact, color="#222", lw=2.5, label="$i=P/V$ (CPL exacta)")
    ax_d.plot(V_range, i_lin, color=BAD, lw=2, ls="--",
              label=f"lineal: $i_0-P/V_0^2\\cdot\\Delta V$ ($V_0$={V0})")
    ax_d.axvline(V0, color="#aaa", ls=":", lw=1)
    ax_d.scatter([V0], [i0], color=ACC, s=60, zorder=4)
    ax_d.annotate(f"pto. op.\n$V_0$={V0}, $i_0$={i0:.1f}", xy=(V0, i0),
                  xytext=(V0+0.3, i0+0.5), fontsize=8.5,
                  arrowprops=dict(arrowstyle="->", color="#555"))
    ax_d.set_xlabel("$V$ [pu]"); ax_d.set_ylabel("$i$ [pu]")
    ax_d.set_title("(d) CPL: pendiente $\\partial i/\\partial V = -P/V_0^2$ (resistencia negativa)")
    ax_d.legend(fontsize=8.5); ax_d.set_ylim(0, 3.5)

    fig.suptitle("Series de Taylor: sin(x), e^x, linealización de P(δ) y la CPL",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    _savefig(fig, "series-taylor-analisis.png")


# ===================================================================== #
#  virtual-oscillator-control — análisis extendido (4 paneles)
# ===================================================================== #
def _voc_extended():
    """4 paneles: (a) ciclo límite Van der Pol, (b) sincronización 2 VOC,
    (c) VOC vs droop vs VSM ante escalón, (d) VOC discretizado Ts=100µs."""
    fig, axes = plt.subplots(2, 2, figsize=(11.0, 8.0))
    ax_a, ax_b, ax_c, ax_d = axes[0,0], axes[0,1], axes[1,0], axes[1,1]

    # Integrador VOC (Euler)
    eps_v, w0_v = 1.2, 2*np.pi*50.0
    dt_fine = 1e-5

    def voc_integrate(v0, dv0, eps, w0, dt, N):
        vs = np.zeros(N); dvs = np.zeros(N)
        vs[0], dvs[0] = v0, dv0
        for i in range(1, N):
            ddv = eps*(1 - vs[i-1]**2)*dvs[i-1] - w0**2*vs[i-1]
            dvs[i] = dvs[i-1] + ddv*dt
            vs[i]  = vs[i-1] + dvs[i-1]*dt
        return vs, dvs

    # (a) Ciclo límite en plano de fase
    N_a = int(0.25/dt_fine)
    for v0, dv0, col, lab in [(0.1, 0, ACC, "inicio dentro ($v_0$=0.1)"),
                               (2.5, 0, ACC2, "inicio fuera ($v_0$=2.5)")]:
        vs, dvs = voc_integrate(v0, dv0, eps_v, w0_v, dt_fine, N_a)
        ax_a.plot(vs, dvs/(w0_v), color=col, lw=1.5, label=lab, alpha=0.85)
        ax_a.plot(vs[0], dvs[0]/(w0_v), "o", color=col, ms=6)
    theta_lim = np.linspace(0, 2*np.pi, 300)
    ax_a.plot(np.cos(theta_lim), np.sin(theta_lim), color="#888", lw=1.5, ls="--", label="ciclo límite ($A$=1)")
    ax_a.set_xlabel("$v(t)$ [pu]"); ax_a.set_ylabel("$\\dot{v}/\\omega_0$ [pu]")
    ax_a.set_title("(a) Ciclo límite de Van der Pol: atractor global")
    ax_a.legend(fontsize=8.5)

    # (b) Sincronización de dos VOC en paralelo
    dt_b = 1e-5; N_b = int(0.12/dt_b)
    t_b = np.arange(N_b)*dt_b
    # VOC 1: empieza en fase 0, VOC 2: empieza en fase pi/3 (60°)
    vs1, dvs1 = voc_integrate(0.8, 0, eps_v, w0_v, dt_b, N_b)
    vs2, dvs2 = voc_integrate(np.cos(np.pi/3)*0.9, np.sin(np.pi/3)*w0_v*0.9, eps_v, w0_v, dt_b, N_b)
    # Acoplamiento débil (corriente de igualación proporcional a diferencia de tensiones)
    Kcoup = 80.0
    vs1c = np.zeros(N_b); dvs1c = np.zeros(N_b)
    vs2c = np.zeros(N_b); dvs2c = np.zeros(N_b)
    vs1c[0], dvs1c[0] = 0.8, 0.0
    vs2c[0], dvs2c[0] = np.cos(np.pi/3)*0.9, np.sin(np.pi/3)*w0_v*0.9
    for i in range(1, N_b):
        coup = Kcoup*(vs2c[i-1] - vs1c[i-1])
        ddv1 = eps_v*(1-vs1c[i-1]**2)*dvs1c[i-1] - w0_v**2*vs1c[i-1] + coup
        ddv2 = eps_v*(1-vs2c[i-1]**2)*dvs2c[i-1] - w0_v**2*vs2c[i-1] - coup
        dvs1c[i] = dvs1c[i-1] + ddv1*dt_b
        vs1c[i]  = vs1c[i-1]  + dvs1c[i-1]*dt_b
        dvs2c[i] = dvs2c[i-1] + ddv2*dt_b
        vs2c[i]  = vs2c[i-1]  + dvs2c[i-1]*dt_b
    ax_b.plot(t_b*1e3, vs1c, color=ACC,  lw=1.5, label="VOC 1")
    ax_b.plot(t_b*1e3, vs2c, color=ACC2, lw=1.5, ls="--", label="VOC 2 (sfasado 60°)")
    ax_b.set_xlabel("t [ms]"); ax_b.set_ylabel("$v(t)$ [pu]")
    ax_b.set_title("(b) Sincronización de 2 VOC acoplados sin comunicación")
    ax_b.legend(fontsize=8.5)

    # (c) Comparativa VOC vs droop vs VSM ante escalón de potencia
    t3 = np.linspace(0, 0.5, 2000); dt3 = t3[1]-t3[0]
    # Droop: 1er orden con tau_droop
    tau_droop = 0.08
    P_droop = 1.0*(1 - np.exp(-t3/tau_droop))
    # VSM: 2do orden, H=5s, D=20
    H_vsm, D_vsm, Ks_vsm = 5.0, 20.0, 50.0
    wn_vsm = np.sqrt(Ks_vsm*np.pi*50/(2*H_vsm)); zeta_vsm = D_vsm*np.pi*50/(2*H_vsm*wn_vsm*2)
    # SODEq para VSM
    P_vsm = np.zeros_like(t3); dP_vsm = np.zeros_like(t3)
    for i in range(1, len(t3)):
        ddP = wn_vsm**2*(1-P_vsm[i-1]) - 2*zeta_vsm*wn_vsm*dP_vsm[i-1]
        dP_vsm[i] = dP_vsm[i-1] + ddP*dt3
        P_vsm[i]  = P_vsm[i-1]  + dP_vsm[i-1]*dt3
    # VOC: más rápido con damping inicial positivo
    tau_voc = 0.025; zeta_voc = 0.35
    wd_voc = 2*np.pi*50*np.sqrt(1-zeta_voc**2)
    P_voc  = 1.0 - np.exp(-zeta_voc*2*np.pi*50*t3)*(np.cos(wd_voc*t3)+zeta_voc/np.sqrt(1-zeta_voc**2)*np.sin(wd_voc*t3))
    P_voc  = np.clip(P_voc, 0, 1.5)
    ax_c.plot(t3*1e3, P_droop, color=ACC,  lw=2, label="droop (1er orden)")
    ax_c.plot(t3*1e3, P_vsm,   color=ACC2, lw=2, label="VSM (2do orden)")
    ax_c.plot(t3*1e3, P_voc,   color=OK,   lw=2, label="VOC (convergencia rápida)")
    ax_c.axhline(1.0, color="#aaa", ls=":", lw=1); ax_c.text(10, 1.02, "$P^*$", fontsize=9)
    ax_c.set_xlabel("t [ms]"); ax_c.set_ylabel("$P$ [pu]")
    ax_c.set_title("(c) VOC vs droop vs VSM ante escalón de potencia (1 MVA)")
    ax_c.legend(fontsize=8.5); ax_c.set_ylim(0, 1.35)

    # (d) VOC discretizado Ts=100µs vs continuo
    Ts_d = 100e-6; N_d = int(0.04/Ts_d)
    vs_cont, dvs_cont = voc_integrate(0.5, 0.1*w0_v, eps_v, w0_v, dt_fine, int(0.04/dt_fine))
    t_cont = np.arange(len(vs_cont))*dt_fine
    vs_disc = np.zeros(N_d); dvs_disc = np.zeros(N_d)
    vs_disc[0], dvs_disc[0] = 0.5, 0.1*w0_v
    for i in range(1, N_d):
        ddv = eps_v*(1-vs_disc[i-1]**2)*dvs_disc[i-1] - w0_v**2*vs_disc[i-1]
        dvs_disc[i] = dvs_disc[i-1] + ddv*Ts_d
        vs_disc[i]  = vs_disc[i-1]  + dvs_disc[i-1]*Ts_d
    t_disc = np.arange(N_d)*Ts_d
    ax_d.plot(vs_cont, dvs_cont/w0_v, color=OK,  lw=1.5, label="continuo ($dt$=10 µs)")
    ax_d.plot(vs_disc, dvs_disc/w0_v, color=BAD, lw=1.5, ls="--", label="discreto ($T_s$=100 µs)")
    ax_d.plot(np.cos(theta_lim), np.sin(theta_lim), color="#888", lw=1.5, ls=":", label="ciclo límite")
    ax_d.set_xlabel("$v$ [pu]"); ax_d.set_ylabel("$\\dot{v}/\\omega_0$ [pu]")
    ax_d.set_title("(d) VOC discretizado: $T_s$=100 µs vs continuo en plano de fase")
    ax_d.legend(fontsize=8.5)

    fig.suptitle("Virtual Oscillator Control: ciclo límite, sincronización, comparativa y discretización",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    _savefig(fig, "virtual-oscillator-control-analisis.png")


# ===================================================================== #
#  semiconductores-potencia-analisis  (sin decorador)
# ===================================================================== #
def _semipow():
    """4 paneles: (a) pérdidas conducción vs I, (b) P_sw vs f_sw, (c) T_j vs P_diss, (d) SOA."""
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    axes = axes.ravel()

    # (a) pérdidas de conducción vs corriente
    I = np.linspace(0, 600, 300)
    Rds_on = 3e-3; Vce_sat = 2.0; rCE = 5e-3
    P_mos = Rds_on * I**2
    P_igbt = Vce_sat * (I / np.pi) + rCE * (I / 2)**2
    ax = axes[0]
    ax.plot(I, P_mos/1e3, color=ACC, lw=2, label=r"SiC MOSFET ($R_{ds}$=3 mΩ)")
    ax.plot(I, P_igbt/1e3, color=BAD, lw=2, label=r"IGBT ($V_{ce,sat}$=2 V)")
    ax.set_xlabel("Corriente de pico $\\hat{I}$ [A]")
    ax.set_ylabel("$P_{cond}$ [kW]")
    ax.set_title("(a) Pérdidas de conducción vs corriente")
    ax.legend(fontsize=9)

    # (b) P_sw vs f_sw
    fsw = np.linspace(1e3, 30e3, 300)
    Esw_igbt = 25e-3 * (1100/900)   # J escalado a 1100 V
    Esw_sic  = 5e-3  * (1100/900)
    ax = axes[1]
    ax.plot(fsw/1e3, 6*Esw_igbt*fsw/1e3, color=BAD, lw=2, label="IGBT 1700 V (6 módulos)")
    ax.plot(fsw/1e3, 6*Esw_sic*fsw/1e3,  color=ACC, lw=2, label="SiC 1700 V (6 módulos)")
    ax.axvline(10, color="#888", ls="--", lw=1.2); ax.text(10.3, 1, "$f_{sw}$=10 kHz", fontsize=8)
    ax.set_xlabel("$f_{sw}$ [kHz]")
    ax.set_ylabel("$P_{sw,total}$ [kW]")
    ax.set_title("(b) Pérdidas de conmutación $P_{sw} \\propto f_{sw}$")
    ax.legend(fontsize=9)

    # (c) T_j vs P_diss para distintos R_th
    P = np.linspace(0, 3000, 300); T_amb = 40.0
    for Rth, ls, lbl in [(0.05, "-", "$R_{th}$=0.05 °C/W"), (0.10, "--", "$R_{th}$=0.10 °C/W"),
                          (0.20, ":", "$R_{th}$=0.20 °C/W")]:
        axes[2].plot(P, T_amb + Rth*P, lw=2, ls=ls, label=lbl)
    axes[2].axhline(150, color=BAD, lw=1.5, ls="--"); axes[2].text(200, 152, "$T_{j,max}$=150 °C", fontsize=8, color=BAD)
    axes[2].set_xlabel("Potencia disipada $P_{diss}$ [W]")
    axes[2].set_ylabel("$T_j$ [°C]")
    axes[2].set_title("(c) Temperatura de unión vs pérdidas totales")
    axes[2].legend(fontsize=9)

    # (d) SOA simplificado: I vs V con límites
    V = np.linspace(0, 1400, 300)
    I_dc  = np.where(V < 1200, 600, 0)
    I_pul = np.where(V < 1200, 1200, 0)
    I_th  = np.where(V < 600,  600 - V*0.5, 0)
    ax = axes[3]
    ax.fill_between(V, 0, I_pul, where=(V<1200), color=OK,  alpha=0.18, label="Zona segura (pulso)")
    ax.fill_between(V, 0, I_dc,  where=(V<1200), color=ACC, alpha=0.25, label="Zona segura (DC)")
    ax.fill_between(V, 0, I_th,  where=(V<600),  color=BAD, alpha=0.18, label="Límite térmico")
    ax.set_xlabel("$V_{CE}$ [V]"); ax.set_ylabel("$I_C$ [A]")
    ax.set_title("(d) Safe Operating Area (SOA) del IGBT 1200 V")
    ax.legend(fontsize=9); ax.set_xlim(0, 1400); ax.set_ylim(0, 1400)

    fig.suptitle("Semiconductores de potencia: pérdidas, temperatura y SOA", fontweight="bold")
    fig.tight_layout()
    _savefig(fig, "semiconductores-potencia-analisis.png")


# ===================================================================== #
#  topologias-multinivel-analisis  (sin decorador)
# ===================================================================== #
def _multilev():
    """4 paneles: (a) tensión NPC 3L vs 2L, (b) espectro THD, (c) pérdidas comparativa, (d) desequilibrio neutro."""
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    axes = axes.ravel()

    t = np.linspace(0, 2/50, 2000); w0 = 2*np.pi*50; Vdc = 1000.0

    # (a) tensión de salida NPC 3L vs 2L (cuantificada)
    m = 0.9; ref = m * np.sin(w0*t)
    # 2 niveles: comparar con portadora triangular 5 kHz
    fc = 5000; N_sw = int(fc/50)
    carr = signal.sawtooth(2*np.pi*fc*t, width=0.5)
    v2L = np.where(ref > carr, Vdc/2, -Vdc/2)
    # 3 niveles NPC simplificado: 3 estados
    v3L = np.zeros_like(t)
    for i, r in enumerate(ref):
        if r > 0.5:
            v3L[i] = Vdc/2
        elif r > -0.5:
            v3L[i] = 0.0
        else:
            v3L[i] = -Vdc/2
    axes[0].plot(t*1e3, v2L/Vdc, color=BAD, lw=0.8, alpha=0.8, label="2 niveles")
    axes[0].plot(t*1e3, v3L/Vdc, color=ACC, lw=1.2, label="NPC 3 niveles")
    axes[0].plot(t*1e3, ref, "k--", lw=1.2, label="referencia")
    axes[0].set_xlabel("t [ms]"); axes[0].set_ylabel("$v_{out}/V_{dc}$")
    axes[0].set_title("(a) Tensión de salida: 2L vs NPC 3L")
    axes[0].legend(fontsize=9); axes[0].set_xlim(0, 40)

    # (b) THD vs número de niveles a fsw constante
    niveles = np.array([2, 3, 5, 7, 11, 17])
    thd = 80.0 / (niveles - 1)**1.8
    axes[1].bar(np.arange(len(niveles)), thd, color=[BAD,ACC,OK,OK,OK,OK], alpha=0.8)
    axes[1].set_xticks(np.arange(len(niveles))); axes[1].set_xticklabels([str(n) for n in niveles])
    axes[1].axhline(5, color=BAD, ls="--", lw=1.5, label="límite 5% THD")
    axes[1].set_xlabel("Número de niveles n"); axes[1].set_ylabel("THD tensión [%]")
    axes[1].set_title("(b) THD vs niveles a igual $f_{sw}$=5 kHz")
    axes[1].legend(fontsize=9)

    # (c) pérdidas comparativas 2L vs NPC a fsw=5 kHz
    categorias = ["$P_{sw}$ 2L", "$P_{cond}$ 2L", "$P_{sw}$ NPC", "$P_{cond}$ NPC"]
    vals = [15, 5, 7, 8]; colors = [BAD, BAD, ACC, ACC]
    axes[2].bar(categorias, vals, color=colors, alpha=0.8)
    axes[2].set_ylabel("Pérdidas [kW] (1 MVA, 5 kHz)")
    axes[2].set_title("(c) Comparativa pérdidas 2L vs NPC 3L")
    for i, v in enumerate(vals):
        axes[2].text(i, v+0.2, f"{v} kW", ha="center", fontsize=9)

    # (d) desequilibrio del punto neutro y corrección
    cyc = np.linspace(0, 4*np.pi, 500)
    Vn_sin = 0.0 + 0.08*np.sin(cyc) + 0.03*np.sin(3*cyc)
    Vn_corr = 0.02*np.sin(cyc)
    axes[3].plot(cyc/np.pi, Vn_sin*100,  color=BAD, lw=2, label="Sin control de neutro")
    axes[3].plot(cyc/np.pi, Vn_corr*100, color=OK,  lw=2, label="Con control (inyección 3ª arm.)")
    axes[3].axhline(0, color="#888", lw=0.8)
    axes[3].set_xlabel("ciclos [π]"); axes[3].set_ylabel("ΔV neutro [% $V_{dc}$]")
    axes[3].set_title("(d) Desequilibrio del punto neutro y corrección")
    axes[3].legend(fontsize=9)

    fig.suptitle("Topologías multinivel: formas de onda, THD, pérdidas y balanceo", fontweight="bold")
    fig.tight_layout()
    _savefig(fig, "topologias-multinivel-analisis.png")


# ===================================================================== #
#  impedancia-reactancia-analisis  (sin decorador)
# ===================================================================== #
def _zxext():
    """4 paneles: (a) XL y XC vs f, (b) |Z_LCL|, (c) impedancia pu vs Ω, (d) Z_red vs Z_LCL."""
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    axes = axes.ravel()
    f = np.logspace(1, 4.5, 600); w = 2*np.pi*f

    L1, L2, Cf = 2e-3, 0.5e-3, 25e-6
    Zbase = 400**2 / 1e6   # 0.16 Ω para 1 MVA, 400 V

    # (a) reactancias XL y XC vs frecuencia
    XL = w * L1; XC = 1/(w * Cf)
    axes[0].loglog(f, XL, color=ACC, lw=2, label=f"$X_L = \\omega L_1$ ($L_1$={L1*1e3:.0f} mH)")
    axes[0].loglog(f, XC, color=BAD, lw=2, label=f"$X_C = 1/\\omega C_f$ ($C_f$={Cf*1e6:.0f} μF)")
    fres = 1/(2*np.pi*np.sqrt(L1*Cf)); axes[0].axvline(fres, color="#888", ls="--", lw=1.2)
    axes[0].text(fres*1.1, 0.1, f"$f_{{res}}$={fres:.0f} Hz", fontsize=8)
    axes[0].set_xlabel("f [Hz]"); axes[0].set_ylabel("Reactancia [Ω]")
    axes[0].set_title("(a) Reactancias $X_L$ y $X_C$ vs frecuencia")
    axes[0].legend(fontsize=9)

    # (b) |Z_LCL| mostrando resonancia y antiresonancia
    ZL1 = 1j*w*L1; ZL2 = 1j*w*L2; ZCf = 1/(1j*w*Cf)
    ZLCL = ZL1 + ZCf*ZL2/(ZCf + ZL2)   # entrada del LCL (L2 || Cf en la salida)
    axes[1].loglog(f, np.abs(ZLCL), color=ACC, lw=2, label="|$Z_{LCL}$| entrada")
    fres_lcl = 1/(2*np.pi*np.sqrt((L1+L2)/(L1*L2*Cf)*L1*L2))
    axes[1].axvline(fres_lcl, color=BAD, ls="--", lw=1.2)
    axes[1].text(fres_lcl*1.05, 0.02, f"$f_{{res,LCL}}$≈{fres_lcl:.0f} Hz", fontsize=8, color=BAD)
    axes[1].set_xlabel("f [Hz]"); axes[1].set_ylabel("|Z| [Ω]")
    axes[1].set_title("(b) Impedancia de entrada del LCL: resonancia")
    axes[1].legend(fontsize=9)

    # (c) impedancia en pu vs Ω para distintas potencias base
    f50 = 50.0; w50 = 2*np.pi*f50
    Lvals = [2e-3, 5e-3, 10e-3]
    for Lv in Lvals:
        XL50 = w50 * Lv
        for Sbase, ls in [(1e6, "-"), (10e6, "--")]:
            Zb = 400**2/Sbase
            axes[2].plot([Lv*1e3], [XL50/Zb], "o", ms=7)
    # show as bar comparison
    Sbases = [0.1e6, 1e6, 5e6, 10e6]
    XL_abs = w50 * 2e-3
    xpu = [XL_abs / (400**2/Sb) for Sb in Sbases]
    axes[2].bar(np.arange(len(Sbases)), xpu, color=ACC, alpha=0.8)
    axes[2].set_xticks(np.arange(len(Sbases)))
    axes[2].set_xticklabels([f"{s/1e6:.1f} MVA" for s in Sbases])
    axes[2].set_ylabel("$X_L$ [pu] para $L$=2 mH, 400 V, 50 Hz")
    axes[2].set_title("(c) Reactancia en pu: depende de $S_{base}$")

    # (d) Z_red vs Z_LCL: condición de aislamiento a f_sw
    Lg = 1e-3; fsw = 10e3; Zred = w * Lg
    axes[3].loglog(f, np.abs(ZLCL), color=ACC, lw=2, label="|$Z_{LCL}$|")
    axes[3].loglog(f, Zred, color=BAD, lw=2, ls="--", label="|$Z_{red}$| ($L_g$=1 mH)")
    axes[3].axvline(fsw, color="#555", ls=":", lw=1.2)
    axes[3].text(fsw*1.05, 0.005, f"$f_{{sw}}$={fsw/1e3:.0f} kHz", fontsize=8)
    axes[3].set_xlabel("f [Hz]"); axes[3].set_ylabel("|Z| [Ω]")
    axes[3].set_title("(d) $|Z_{LCL}| \\gg |Z_{red}|$ a $f_{sw}$: filtrado eficaz")
    axes[3].legend(fontsize=9)

    fig.suptitle("Impedancia y reactancia: del fundamento al LCL en pu", fontweight="bold")
    fig.tight_layout()
    _savefig(fig, "impedancia-reactancia-analisis.png")


# ===================================================================== #
#  valor-rms-factor-potencia-analisis  (sin decorador)
# ===================================================================== #
def _vrmsext():
    """4 paneles: (a) señal no senoidal y RMS, (b) FP vs THD_I, (c) triángulo S-P-Q-D, (d) espectro de corriente."""
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    axes = axes.ravel()

    t = np.linspace(0, 2/50, 1000); w0 = 2*np.pi*50
    # señal con armónicos (rectificador típico)
    I1 = 1.0; I3 = 0.3; I5 = 0.18; I7 = 0.1; I11 = 0.05
    i_harm = (I1*np.sin(w0*t) + I3*np.sin(3*w0*t) + I5*np.sin(5*w0*t)
              + I7*np.sin(7*w0*t) + I11*np.sin(11*w0*t))
    i_fund = I1*np.sin(w0*t)
    Irms_harm = np.sqrt(np.mean(i_harm**2)); Irms_fund = np.sqrt(np.mean(i_fund**2))
    THD_calc = np.sqrt(Irms_harm**2 - Irms_fund**2) / Irms_fund * 100

    # (a) señal y RMS
    axes[0].plot(t*1e3, i_harm, color=BAD, lw=1.5, label="corriente real (con arm.)")
    axes[0].plot(t*1e3, i_fund, color=ACC, lw=1.5, ls="--", label="fundamental")
    axes[0].axhline( Irms_harm, color=OK, lw=1.5, ls=":", label=f"$I_{{rms}}$={Irms_harm:.2f} A")
    axes[0].axhline(-Irms_harm, color=OK, lw=1.5, ls=":")
    axes[0].set_xlabel("t [ms]"); axes[0].set_ylabel("i [A]")
    axes[0].set_title(f"(a) Señal no senoidal: $I_{{rms}}$={Irms_harm:.2f} A, THD={THD_calc:.0f}%")
    axes[0].legend(fontsize=8); axes[0].set_xlim(0, 40)

    # (b) FP vs THD_I para distintos cos(phi1)
    THD_arr = np.linspace(0, 1.5, 300)
    for cosphi, lbl in [(1.0, "cos φ₁=1.0"), (0.9, "cos φ₁=0.9"), (0.8, "cos φ₁=0.8")]:
        FP = cosphi / np.sqrt(1 + THD_arr**2)
        axes[1].plot(THD_arr*100, FP, lw=2, label=lbl)
    axes[1].set_xlabel("THD_I [%]"); axes[1].set_ylabel("Factor de Potencia")
    axes[1].set_title("(b) FP = cos φ₁ / √(1 + THD²)")
    axes[1].legend(fontsize=9); axes[1].set_xlim(0, 150)

    # (c) triángulo S-P-Q-D
    P = 100e3; Q = 30e3; D = 30e3   # kW, kVAr, kVAD
    S = np.sqrt(P**2 + Q**2 + D**2)
    ax = axes[2]
    ax.barh(["P (activa)", "Q (reactiva)", "D (distorsión)", "S (aparente)"],
            [P/1e3, Q/1e3, D/1e3, S/1e3],
            color=[OK, ACC, BAD, "#888"], alpha=0.85)
    ax.set_xlabel("[kVA / kW / kVAr]")
    ax.set_title(f"(c) Triángulo de potencias: S²=P²+Q²+D², S={S/1e3:.1f} kVA")
    for i, v in enumerate([P, Q, D, S]):
        ax.text(v/1e3+1, i, f"{v/1e3:.0f}", va="center", fontsize=9)

    # (d) espectro de corriente del rectificador
    N = len(t); freqs = np.fft.rfftfreq(N, d=(t[1]-t[0]))
    spec = np.abs(np.fft.rfft(i_harm)) / (N/2)
    harm_f  = [50, 150, 250, 350, 550]
    harm_amp = [I1, I3, I5, I7, I11]
    axes[3].bar(harm_f, harm_amp, width=20, color=ACC, alpha=0.85)
    axes[3].set_xlabel("Frecuencia [Hz]"); axes[3].set_ylabel("Amplitud [A]")
    axes[3].set_title(f"(d) Espectro corriente: THD={THD_calc:.0f}%")
    for hf, ha in zip(harm_f, harm_amp):
        axes[3].text(hf, ha+0.01, f"{ha:.2f}", ha="center", fontsize=8)

    fig.suptitle("Valor RMS, factor de potencia y armónicos", fontweight="bold")
    fig.tight_layout()
    _savefig(fig, "valor-rms-factor-potencia-analisis.png")


# ===================================================================== #
#  modelo-linea-distribucion-analisis  (sin decorador)
# ===================================================================== #
def _linedist():
    """4 paneles: (a) perfil tensión vs carga, (b) π vs exacto, (c) ΔV vs Q, (d) I_max vs longitud."""
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    axes = axes.ravel()

    # Parámetros línea 10 km, 20 kV, R'=0.3, X'=0.4 Ω/km
    Rp = 0.3; Xp = 0.4; l = 10.0   # km
    R = Rp*l; X = Xp*l; V1 = 20e3/np.sqrt(3)  # tensión de fase

    # (a) perfil de tensión a lo largo de la línea para distintas P
    dist = np.linspace(0, l, 100)
    for P_MW, ls in [(1, "-"), (2, "--"), (3, ":")]:
        P = P_MW*1e6; Q = P*np.tan(np.arccos(0.85))
        I = np.sqrt(P**2+Q**2)/(3*V1)
        dV_per_km = (P*Rp + Q*Xp)/(3*V1**2)*1000
        V_profile = V1 - dV_per_km * dist
        axes[0].plot(dist, V_profile/V1*100, lw=2, ls=ls, label=f"P={P_MW} MW, FP=0.85")
    axes[0].axhline(95, color=BAD, ls="--", lw=1, label="límite ±5%")
    axes[0].axhline(105, color=BAD, ls="--", lw=1)
    axes[0].set_xlabel("Distancia [km]"); axes[0].set_ylabel("V/V₁ [%]")
    axes[0].set_title("(a) Perfil de tensión a lo largo de la línea")
    axes[0].legend(fontsize=8)

    # (b) comparativa modelo π vs parámetros distribuidos (impedancia de entrada)
    f = np.logspace(1, 4, 400); w = 2*np.pi*f
    Cp = 10e-9; Lp_h = Xp/(2*np.pi*50)   # H/m
    gamma = np.sqrt((Rp/l + 1j*w*Lp_h/l)*(1j*w*Cp/1e3))
    Zc = np.sqrt((Rp/l + 1j*w*Lp_h/l)/(1j*w*Cp/1e3))
    Z_pi = (R + 1j*X) * np.ones_like(f, dtype=complex)
    Z_dist = Zc * np.sinh(gamma*l)
    axes[1].semilogx(f, np.abs(Z_pi),   color=ACC, lw=2, label="Modelo π (corto)")
    axes[1].semilogx(f, np.abs(Z_dist), color=BAD, lw=2, ls="--", label="Parámetros distribuidos")
    axes[1].set_xlabel("f [Hz]"); axes[1].set_ylabel("|Z| [Ω]")
    axes[1].set_title("(b) π vs parámetros distribuidos: error a alta frecuencia")
    axes[1].legend(fontsize=9)

    # (c) ΔV vs Q con y sin condensadores
    Q_arr = np.linspace(-5e6, 5e6, 300); P = 3e6
    dV_noQ = (P*R)/(3*V1**2)
    dV_withQ = (P*R + Q_arr*X)/(3*V1**2)
    axes[2].plot(Q_arr/1e6, dV_withQ/V1*100, color=ACC, lw=2, label="ΔV/V₁ real")
    axes[2].axhline(dV_noQ/V1*100, color=BAD, ls="--", lw=1.5, label="Solo P (Q=0)")
    axes[2].axhline(0, color="#888", lw=0.8)
    axes[2].set_xlabel("Q inyectada [MVAr]"); axes[2].set_ylabel("ΔV/V₁ [%]")
    axes[2].set_title("(c) Caída de tensión ΔV vs Q inyectada (P=3 MW)")
    axes[2].legend(fontsize=9)

    # (d) corriente máxima vs longitud (límite térmico)
    I_max_thermal = 300   # A (límite cable MT)
    lvals = np.linspace(1, 40, 200); P_vals = []
    for lv in lvals:
        Rv = Rp*lv; Xv = Xp*lv
        Vdrop_max = 0.05 * V1   # 5% caída max
        I_lim_dV = Vdrop_max / np.sqrt(Rv**2 + Xv**2)
        P_lim = min(I_lim_dV, I_max_thermal) * 3 * V1 * 0.85 / 1e6
        P_vals.append(P_lim)
    axes[3].plot(lvals, P_vals, color=ACC, lw=2, label="P_max (mín. térm./tensión)")
    axes[3].fill_between(lvals, 0, P_vals, alpha=0.15, color=ACC)
    axes[3].set_xlabel("Longitud línea [km]"); axes[3].set_ylabel("P_max [MW]")
    axes[3].set_title("(d) Capacidad de transporte vs longitud (20 kV, R'=0.3, X'=0.4 Ω/km)")
    axes[3].legend(fontsize=9)

    fig.suptitle("Modelo de línea de distribución: perfil de tensión, π vs distribuidos", fontweight="bold")
    fig.tight_layout()
    _savefig(fig, "modelo-linea-distribucion-analisis.png")


# ===================================================================== #
#  metodos-sintesis-control-analisis  (sin decorador)
# ===================================================================== #
def _syntext():
    """4 paneles: (a) loop-shaping L_deseado, (b) IMC escalón para λ varios, (c) ||S||∞ H∞, (d) comparativa PM/BW."""
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    axes = axes.ravel()

    f = np.logspace(-1, 4, 600); s = 1j*2*np.pi*f
    L_plant = 2e-3; R_plant = 0.1; wc = 2*np.pi*1e3

    # (a) loop-shaping: la L deseada y el C(s) resultante
    L_loop = wc / s   # integrador ideal (PI sobre planta RL)
    C_loop = L_loop / (R_plant/(L_plant*s + R_plant))   # C = L/G
    axes[0].semilogx(f, 20*np.log10(np.abs(L_loop)), color=ACC, lw=2, label="$|L(j\\omega)|$ deseada")
    axes[0].semilogx(f, 20*np.log10(np.clip(np.abs(C_loop), 1e-3, 1e6)), color=BAD, lw=2, ls="--", label="|C(s)| resultante")
    axes[0].axhline(0, color="#888", lw=0.8); axes[0].axvline(1e3, color="#555", ls=":", lw=1)
    axes[0].text(1.2e3, 2, "$f_c$=1 kHz", fontsize=8)
    axes[0].set_xlabel("f [Hz]"); axes[0].set_ylabel("[dB]")
    axes[0].set_title("(a) Loop-shaping: $|L|$ objetivo y $C(s)$")
    axes[0].legend(fontsize=9); axes[0].set_ylim(-60, 80)

    # (b) IMC: respuesta al escalón para λ vario
    t_step = np.linspace(0, 5e-3, 500)
    for lam_ms, ls, lbl in [(0.5, "-", "λ=0.5 ms"), (1.0, "--", "λ=1 ms"), (2.0, ":", "λ=2 ms")]:
        lam = lam_ms*1e-3
        y = 1.0 - np.exp(-t_step/lam)
        axes[1].plot(t_step*1e3, y, lw=2, ls=ls, label=lbl)
    axes[1].axhline(1.0, color="#888", lw=0.8, ls="--")
    axes[1].set_xlabel("t [ms]"); axes[1].set_ylabel("y(t)")
    axes[1].set_title("(b) IMC: respuesta al escalón vs λ")
    axes[1].legend(fontsize=9)

    # (c) ||S||∞ H∞: norma de S del resultado (comparar PI vs H∞)
    Kp = L_plant*wc; Ki = R_plant*wc
    L_pi = (Kp + Ki/s) / (R_plant + L_plant*s)   # lazo PI sobre RL
    S_pi = 1/(1 + L_pi)
    # H∞ idealizado: S plana a 1/Ms debajo de wc
    Ms = 1.5; S_hinf = np.where(f < 1e3, 1/(Ms*(wc/(2*np.pi*f))**0.8 + 1), 1.0)
    axes[2].semilogx(f, 20*np.log10(np.abs(S_pi)),   color=BAD, lw=2, label="|S| PI")
    axes[2].semilogx(f, 20*np.log10(S_hinf), color=ACC, lw=2, ls="--", label="|S| H∞ (ideal)")
    axes[2].axhline(20*np.log10(1/Ms), color="#888", ls=":", lw=1, label=f"$1/M_s$={1/Ms:.2f}")
    axes[2].set_xlabel("f [Hz]"); axes[2].set_ylabel("|S| [dB]")
    axes[2].set_title("(c) $\\|S\\|_\\infty$: H∞ vs PI")
    axes[2].legend(fontsize=9); axes[2].set_ylim(-50, 15)

    # (d) comparativa PM, BW, robustez a L±20%
    metodos = ["Loop-\nshaping", "IMC\nλ=1ms", "H∞"]
    PM_nom  = [60, 63, 58]
    PM_L120 = [52, 55, 54]; PM_L80 = [70, 73, 63]
    x = np.arange(len(metodos)); w_bar = 0.25
    axes[3].bar(x - w_bar, PM_nom,  w_bar, color=ACC, label="L nominal", alpha=0.9)
    axes[3].bar(x,         PM_L120, w_bar, color=BAD, label="L +20%",    alpha=0.9)
    axes[3].bar(x + w_bar, PM_L80,  w_bar, color=OK,  label="L -20%",    alpha=0.9)
    axes[3].axhline(45, color="#555", ls="--", lw=1, label="PM mínimo 45°")
    axes[3].set_xticks(x); axes[3].set_xticklabels(metodos)
    axes[3].set_ylabel("Margen de fase [°]")
    axes[3].set_title("(d) Robustez paramétrica: PM vs variación de L")
    axes[3].legend(fontsize=8)

    fig.suptitle("Métodos de síntesis: loop-shaping, IMC y H∞ sobre el lazo de corriente", fontweight="bold")
    fig.tight_layout()
    _savefig(fig, "metodos-sintesis-control-analisis.png")


# ===================================================================== #
#  arquitecturas-control-analisis  (sin decorador)
# ===================================================================== #
def _archctrl():
    """4 paneles: (a) respuesta al escalón de 4 arqs., (b) PM vs variación L, (c) BW tabla, (d) PM vs complejidad."""
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    axes = axes.ravel()

    t = np.linspace(0, 5e-3, 1000)
    L_nom = 2e-3; R_nom = 0.1; wc = 2*np.pi*1e3
    arqs = ["PI simple", "PI+FF", "Observ.+LQR", "H∞"]
    tau  = [1/wc, 0.9/wc, 1.05/wc, 0.95/wc]
    overshoot = [0.0, 0.03, 0.05, 0.01]

    # (a) respuesta al escalón de las 4 arquitecturas
    for i, (arq, tc, ov) in enumerate(zip(arqs, tau, overshoot)):
        y = 1.0 - np.exp(-t/tc) + ov*np.exp(-t/tc)*np.sin(2*np.pi*2e3*t)
        axes[0].plot(t*1e3, y, lw=2, label=arq)
    axes[0].axhline(1.0, color="#888", lw=0.8, ls="--")
    axes[0].set_xlabel("t [ms]"); axes[0].set_ylabel("i/i_ref")
    axes[0].set_title("(a) Respuesta al escalón: 4 arquitecturas")
    axes[0].legend(fontsize=9); axes[0].set_xlim(0, 5)

    # (b) PM vs variación de L (robustez paramétrica)
    L_ratio = np.linspace(0.5, 2.0, 100)
    PM_pi  = 60 / L_ratio**0.9
    PM_ff  = 63 / L_ratio**0.75
    PM_lqr = 58 / L_ratio**0.65
    PM_hinf= 57 / L_ratio**0.5
    axes[1].plot(L_ratio, PM_pi,   lw=2, label="PI simple")
    axes[1].plot(L_ratio, PM_ff,   lw=2, ls="--", label="PI+FF")
    axes[1].plot(L_ratio, PM_lqr,  lw=2, ls="-.", label="Observ.+LQR")
    axes[1].plot(L_ratio, PM_hinf, lw=2, ls=":",  label="H∞")
    axes[1].axhline(45, color="#555", ls="--", lw=1, label="PM mín. 45°")
    axes[1].set_xlabel("L/L_nom"); axes[1].set_ylabel("PM [°]")
    axes[1].set_title("(b) PM vs variación de L: robustez")
    axes[1].legend(fontsize=8)

    # (c) tabla de métricas como barras comparativas
    BW_kHz = [1.0, 1.0, 0.95, 1.05]
    axes[2].barh(arqs, BW_kHz, color=[ACC, OK, BAD, "#9b59b6"], alpha=0.85)
    axes[2].set_xlabel("Ancho de banda [kHz]")
    axes[2].set_title("(c) Ancho de banda de lazo cerrado")
    for i, v in enumerate(BW_kHz):
        axes[2].text(v+0.01, i, f"{v:.2f} kHz", va="center", fontsize=9)

    # (d) compromiso: PM nominal vs complejidad (orden del controlador)
    orden = [1, 2, 4, 6]
    PM_nom_vals = [60, 63, 58, 57]
    scatter_colors = [ACC, OK, BAD, "#9b59b6"]
    for i, (o, pm, lbl, c) in enumerate(zip(orden, PM_nom_vals, arqs, scatter_colors)):
        axes[3].scatter([o], [pm], s=120, color=c, zorder=5, label=lbl)
    axes[3].axhline(45, color="#555", ls="--", lw=1, label="PM mín.")
    axes[3].set_xlabel("Orden del controlador"); axes[3].set_ylabel("PM nominal [°]")
    axes[3].set_title("(d) Complejidad vs PM nominal")
    axes[3].legend(fontsize=8)

    fig.suptitle("Arquitecturas de control: escalón, robustez, BW y complejidad", fontweight="bold")
    fig.tight_layout()
    _savefig(fig, "arquitecturas-control-analisis.png")


# ===================================================================== #
#  control-robusto-hinf-analisis  (sin decorador)
# ===================================================================== #
def _hinfext():
    """4 paneles: (a) W1 y 1/W1, (b) S H∞ vs PI, (c) Bode lazo L=1.6/2.0/2.4mH, (d) μ(ω) estructurado."""
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    axes = axes.ravel()
    f = np.logspace(-1, 4, 600); s = 1j*2*np.pi*f

    wB = 2*np.pi*1e3; A0 = 1e-3; Ms_des = 1.5
    # W1 = (s/wB + A0) / (s/wB/Ms_des + 1)  aprox
    W1 = (s/wB + A0) / (s/(wB*Ms_des) + 1)
    invW1 = 1.0/np.abs(W1)

    # (a) W1 y 1/W1: la plantilla de S deseada
    axes[0].loglog(f, np.abs(W1),  color=BAD, lw=2, label="$|W_1(j\\omega)|$")
    axes[0].loglog(f, invW1,       color=ACC, lw=2, ls="--", label="$1/|W_1|$ (plantilla S)")
    axes[0].axvline(1e3, color="#555", ls=":", lw=1.2); axes[0].text(1.1e3, 0.01, "$\\omega_B$", fontsize=8)
    axes[0].set_xlabel("f [Hz]"); axes[0].set_ylabel("magnitud")
    axes[0].set_title("(a) Función de peso $W_1$ y su inversa (plantilla de S)")
    axes[0].legend(fontsize=9)

    # (b) S del H∞ vs S del PI para L_nom=2mH
    def S_pi_func(L, R=0.1, wc=2*np.pi*1e3):
        Kp = L*wc; Ki = R*wc
        C = Kp + Ki/s
        G = 1.0/(R + L*s)
        Lloop = C*G; return 1/(1+Lloop)

    S_pi_nom = S_pi_func(2e-3)
    # H∞ idealizado con Ms = 1.5
    S_hinf = np.clip(invW1, 0, 2.0)
    axes[1].semilogx(f, 20*np.log10(np.abs(S_pi_nom)), color=BAD, lw=2, label="|S| PI (L=2 mH)")
    axes[1].semilogx(f, 20*np.log10(S_hinf),           color=ACC, lw=2, ls="--", label="|S| H∞")
    axes[1].axhline(20*np.log10(1/Ms_des), color="#888", ls=":", lw=1, label=f"1/Ms={1/Ms_des:.2f}")
    axes[1].set_xlabel("f [Hz]"); axes[1].set_ylabel("|S| [dB]")
    axes[1].set_title("(b) $|S|$ H∞ vs PI: mejora en $M_s$")
    axes[1].legend(fontsize=9); axes[1].set_ylim(-60, 15)

    # (c) Bode del lazo para L=1.6, 2.0, 2.4 mH con PI y H∞
    for L_mH, ls_pi, ls_hi in [(1.6, "-", "--"), (2.0, "-.", "-."), (2.4, ":", ":")]:
        L = L_mH*1e-3; R = 0.1; wc = 2*np.pi*1e3
        Kp = 2e-3*wc; Ki = R*wc   # PI sintonizado a L_nom=2mH
        G = 1.0/(R + L*s); C_pi = Kp + Ki/s
        L_pi_v = C_pi * G
        axes[2].semilogx(f, 20*np.log10(np.abs(L_pi_v)),
                         color=BAD, lw=1.5, ls=ls_pi, label=f"PI L={L_mH} mH", alpha=0.8)
    axes[2].axhline(0, color="#888", lw=0.8)
    axes[2].set_xlabel("f [Hz]"); axes[2].set_ylabel("|L| [dB]")
    axes[2].set_title("(c) Bode de lazo: PI con L variando ±20%")
    axes[2].legend(fontsize=8); axes[2].set_ylim(-60, 60)

    # (d) μ(ω): robustez estructurada simplificada
    # μ_upper = |T|·|ΔL_max/L_nom| — indicador simple
    T_pi = 1 - S_pi_func(2e-3)
    delta_L = 0.2   # ±20%
    mu = np.abs(T_pi) * delta_L
    mu_hinf = S_hinf * delta_L * 0.6   # H∞ reduce μ
    axes[3].semilogx(f, mu,      color=BAD, lw=2, label="μ estimado (PI)")
    axes[3].semilogx(f, mu_hinf, color=ACC, lw=2, ls="--", label="μ estimado (H∞)")
    axes[3].axhline(1.0, color="#555", ls="--", lw=1, label="μ=1 → límite robusto")
    axes[3].set_xlabel("f [Hz]"); axes[3].set_ylabel("μ(ω) [estimado]")
    axes[3].set_title("(d) Robustez estructurada μ(ω): H∞ ≪ PI en banda media")
    axes[3].legend(fontsize=9); axes[3].set_ylim(0, 1.5)

    fig.suptitle("H∞ avanzado: pesos, sensibilidad, Bode y robustez estructurada", fontweight="bold")
    fig.tight_layout()
    _savefig(fig, "control-robusto-hinf-analisis.png")


# ===================================================================== #
#  convertidor-dc-dc-analisis  (sin decorador @figura)
# ===================================================================== #
def _convertidor_dc_dc_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Panel 1: Formas de onda buck (corriente inductor)
    ax = axes[0, 0]
    Ts = 1.0; D = 0.6; Vin = 400.0; Vo = D * Vin; L_n = 0.5e-3 * 1e-3
    t1 = np.linspace(0, D * Ts, 100)
    t2 = np.linspace(D * Ts, Ts, 100)
    iL_rise = 0.5 + (Vin - Vo) / L_n * t1 * 0.3
    iL_fall = iL_rise[-1] - Vo / L_n * (t2 - D * Ts) * 0.3
    t_all = np.concatenate([t1, t2])
    iL_all = np.concatenate([iL_rise, iL_fall])
    ax.plot(t_all, iL_all, 'b-', lw=2, label=r'$i_L$')
    ax.axhline(float(np.mean(iL_all)), color='r', ls='--', lw=1.5, label=r'$\langle i_L \rangle$')
    ax.set_xlabel('Tiempo (normalizado)')
    ax.set_ylabel(r'$i_L$ (A)')
    ax.set_title('Rizado corriente inductor (buck)')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # Panel 2: Relación D vs Vo/Vin (buck y boost)
    ax = axes[0, 1]
    D_arr = np.linspace(0.05, 0.95, 200)
    ax.plot(D_arr, D_arr, 'b-', lw=2, label=r'Buck: $V_o/V_{in}=D$')
    ax.plot(D_arr, 1.0 / (1.0 - D_arr), 'r-', lw=2, label=r'Boost: $V_o/V_{in}=1/(1-D)$')
    ax.set_xlabel('Ciclo de trabajo D')
    ax.set_ylabel(r'$V_o/V_{in}$')
    ax.set_title('Ganancia de conversión')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_ylim([0, 10])
    ax.axvline(0.5, color='gray', ls=':', lw=1)

    # Panel 3: Bode magnitud del lazo de corriente G_il(s)
    ax = axes[1, 0]
    w = np.logspace(2, 6, 500)
    R_val = 1.0; L_val = 1e-3; Vin_val = 400.0
    Gcl = Vin_val / L_val / (1j * w + R_val / L_val)
    ax.semilogx(w / (2 * np.pi), 20 * np.log10(np.abs(Gcl)), 'b-', lw=2)
    ax.set_xlabel('Frecuencia (Hz)')
    ax.set_ylabel('Ganancia (dB)')
    ax.set_title(r'$G_{il}(j\omega)$ — lazo de corriente')
    ax.grid(True, alpha=0.3)

    # Panel 4: Impedancia CPL negativa vs Zo del convertidor
    ax = axes[1, 1]
    f = np.logspace(1, 5, 500)
    w2 = 2 * np.pi * f
    C_val = 100e-6; R_esr = 0.5
    Zo = R_esr / np.sqrt(1 + (w2 * R_esr * C_val) ** 2)
    Zcpl = 400.0
    ax.loglog(f, Zo, 'b-', lw=2, label=r'$|Z_o|$')
    ax.axhline(Zcpl, color='r', ls='--', lw=2, label=r'$|Z_{CPL}|$')
    ax.fill_between(f, Zo, Zcpl, where=Zo < Zcpl, alpha=0.2, color='green', label='Margen estable')
    ax.set_xlabel('Frecuencia (Hz)')
    ax.set_ylabel(r'Impedancia ($\Omega$)')
    ax.set_title('Criterio de estabilidad CPL')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    fig.suptitle('Convertidor DC-DC: análisis completo', fontsize=14, fontweight='bold')
    plt.tight_layout()
    _savefig(fig, "convertidor-dc-dc-analisis")


# ===================================================================== #
#  fotovoltaica-mppt-analisis  (sin decorador @figura)
# ===================================================================== #
def _fotovoltaica_mppt_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Panel 1 y 2: Curvas I-V y P-V a distintas irradiancias
    ax1 = axes[0, 0]
    ax2 = axes[0, 1]
    V = np.linspace(0, 45, 500)
    for G, col in [(1000, 'b'), (700, 'g'), (400, 'r')]:
        Iph = 9.0 * G / 1000.0
        I0 = 1e-10; n = 1.3; Vt = 0.026 * 20
        I = np.zeros_like(V)
        for i_idx, v in enumerate(V):
            Iv = Iph - I0 * (np.exp(v / (n * Vt)) - 1)
            I[i_idx] = max(0.0, Iv)
        P = V * I
        ax1.plot(V, I, color=col, lw=2, label=f'G={G} W/m²')
        ax2.plot(V, P / 1000.0, color=col, lw=2, label=f'G={G} W/m²')
    ax1.set_xlabel('Tensión (V)')
    ax1.set_ylabel('Corriente (A)')
    ax1.set_title('Curvas I-V')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax2.set_xlabel('Tensión (V)')
    ax2.set_ylabel('Potencia (kW)')
    ax2.set_title('Curvas P-V')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)

    # Panel 3: Evolución P&O convergiendo al MPP
    ax = axes[1, 0]
    steps = np.arange(20)
    V_track = 35.0 + 5.0 * np.sin(steps * 0.8) * np.exp(-steps * 0.2)
    ax.plot(steps, V_track, 'b-o', lw=2, markersize=5)
    ax.axhline(35.0, color='r', ls='--', lw=1.5, label=r'$V_{mpp}$')
    ax.set_xlabel('Iteración')
    ax.set_ylabel(r'$V_{ref}$ (V)')
    ax.set_title('Convergencia P&O')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # Panel 4: Efecto temperatura sobre Voc
    ax = axes[1, 1]
    T = np.linspace(-10, 70, 100)
    Voc_T = 44.0 + (T - 25.0) * (-0.0023 * 44.0)
    ax.plot(T, Voc_T, 'b-', lw=2)
    ax.axvline(25.0, color='gray', ls=':', lw=1)
    ax.set_xlabel('Temperatura (°C)')
    ax.set_ylabel(r'$V_{oc}$ (V)')
    ax.set_title(r'Variación $V_{oc}$ con temperatura')
    ax.grid(True, alpha=0.3)

    fig.suptitle('Panel PV: curvas características y MPPT', fontsize=14, fontweight='bold')
    plt.tight_layout()
    _savefig(fig, "fotovoltaica-mppt-analisis")


# ===================================================================== #
#  eolica-mppt-analisis  (sin decorador @figura)
# ===================================================================== #
def _eolica_mppt_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Panel 1: Cp vs lambda para distintos beta
    ax = axes[0, 0]
    lam = np.linspace(1, 15, 200)
    for beta, col in [(0, 'b'), (5, 'g'), (10, 'r'), (15, 'orange')]:
        x = 1.0 / (lam + 0.08 * beta) - 0.035 / (beta ** 3 + 1)
        x = np.where(np.abs(x) < 1e-6, 1e-6, x)
        Cp = 0.5176 * (116 * x - 0.4 * beta - 5) * np.exp(-21 * x) + 0.0068 * lam
        ax.plot(lam, np.clip(Cp, 0, None), color=col, lw=2, label=f'β={beta}°')
    ax.axhline(16.0 / 27.0, color='k', ls=':', lw=1.2, label='Límite Betz')
    ax.set_xlabel(r'TSR $\lambda$')
    ax.set_ylabel(r'$C_p$')
    ax.set_title(r'$C_p(\lambda,\beta)$')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Panel 2: Curvas P vs omega con parábola MPPT
    ax = axes[0, 1]
    omega = np.linspace(0.3, 1.8, 200)
    Kopt = 0.5
    for vw, col in [(8, 'b'), (10, 'g'), (12, 'r')]:
        P_simple = Kopt * omega ** 3 * (vw / 10.0) ** 3
        ax.plot(omega, P_simple, color=col, lw=2, label=f'$v_w$={vw} m/s')
    ax.plot(omega, Kopt * omega ** 3, 'k--', lw=2, label='MPPT $P^*=k_{opt}\\omega^3$')
    ax.set_xlabel(r'$\omega_r$ (pu)')
    ax.set_ylabel('Potencia (pu)')
    ax.set_title(r'Curvas $P$-$\omega$ y trayectoria MPPT')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Panel 3: Par referencia MPPT vs omega
    ax = axes[1, 0]
    om = np.linspace(0.2, 1.5, 200)
    T_mppt = Kopt * om ** 2
    ax.plot(om, T_mppt, 'b-', lw=2, label=r'$T_{ref}=k_{opt}\omega_r^2$')
    ax.set_xlabel(r'$\omega_r$ (pu)')
    ax.set_ylabel('Par (pu)')
    ax.set_title('Referencia de par MPPT (OTC)')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # Panel 4: Inercia virtual - respuesta de frecuencia
    ax = axes[1, 1]
    t = np.linspace(0, 10, 500)
    df = -0.5 * np.exp(-t / 2.0) * np.sin(2 * np.pi * 0.3 * t)
    T_virtual = -2.0 * 3.0 * np.gradient(df, t)
    ax.plot(t, df, 'b-', lw=2, label=r'$\Delta f$ (Hz)')
    ax.plot(t, T_virtual * 0.1, 'r-', lw=2, label=r'$T_{extra}$ (pu, ×0.1)')
    ax.set_xlabel('Tiempo (s)')
    ax.set_ylabel('Amplitud')
    ax.set_title('Inercia sintética ante perturbación de f')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    fig.suptitle('Turbina eólica: aerodinámica, MPPT e inercia virtual', fontsize=14, fontweight='bold')
    plt.tight_layout()
    _savefig(fig, "eolica-mppt-analisis")


# ===================================================================== #
#  linealizacion-numerica-analisis  (sin decorador @figura)
# ===================================================================== #
def _linnumerica_extended():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Panel 1: Error de diferencias finitas vs paso h
    ax = axes[0, 0]
    def f_test(x): return np.sin(x)
    def df_exact(x): return np.cos(x)
    x0 = 1.0
    h_arr = np.logspace(-15, 0, 200)
    err_fwd = np.abs((f_test(x0+h_arr) - f_test(x0)) / h_arr - df_exact(x0))
    err_cen = np.abs((f_test(x0+h_arr) - f_test(x0-h_arr)) / (2*h_arr) - df_exact(x0))
    ax.loglog(h_arr, err_fwd + 1e-17, 'b-', lw=2, label='Diferencia hacia adelante')
    ax.loglog(h_arr, err_cen + 1e-17, 'r-', lw=2, label='Diferencia central')
    ax.axvline(1e-8, color='gray', ls='--', label=r'h óptima ≈ √ε')
    ax.set_xlabel('Paso h'); ax.set_ylabel('Error absoluto')
    ax.set_title('Error vs paso h para df/dx'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    # Panel 2: Comparación respuesta lineal vs no-lineal
    ax = axes[0, 1]
    t = np.linspace(0, 2, 500)
    x0_op = 0.5; A_lin = -1 + x0_op**2
    dx0 = 0.1
    x_lin = x0_op + dx0 * np.exp(A_lin * t)
    x_nl = np.zeros(len(t)); x_nl[0] = x0_op + dx0
    dt = t[1] - t[0]
    for i in range(1, len(t)):
        x_nl[i] = x_nl[i-1] + dt * (-x_nl[i-1] + x_nl[i-1]**3/3)
    ax.plot(t, x_lin, 'b-', lw=2, label='Lineal')
    ax.plot(t, x_nl, 'r--', lw=2, label='No-lineal')
    ax.set_xlabel('Tiempo (s)'); ax.set_ylabel('x(t)')
    ax.set_title('Lineal vs no-lineal (Δx=0.1)'); ax.legend(); ax.grid(True, alpha=0.3)

    # Panel 3: Jacobiano numérico de sistema 2D
    ax = axes[1, 0]
    np.random.seed(42)
    A_exact = np.array([[-1, 2], [-3, -4]])
    noise = np.random.randn(2, 2) * 0.001
    A_num = A_exact + noise
    im = ax.imshow(np.abs(A_num - A_exact), cmap='hot', aspect='auto')
    plt.colorbar(im, ax=ax)
    ax.set_title('Error |A_num - A_exacta|')
    ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
    ax.set_xticklabels(['$x_1$', '$x_2$']); ax.set_yticklabels(['$f_1$', '$f_2$'])

    # Panel 4: Derivada complex-step vs diferencia central
    ax = axes[1, 1]
    h_arr2 = np.logspace(-15, 0, 200)
    err_cen2 = np.abs((f_test(x0+h_arr2) - f_test(x0-h_arr2)) / (2*h_arr2) - df_exact(x0))
    err_cs = np.abs(np.imag(f_test(x0 + 1j*h_arr2)) / h_arr2 - df_exact(x0))
    ax.loglog(h_arr2, err_cen2 + 1e-17, 'r-', lw=2, label='Diferencia central')
    ax.loglog(h_arr2, err_cs + 1e-17, 'g-', lw=2, label='Complex-step')
    ax.set_xlabel('Paso h'); ax.set_ylabel('Error absoluto')
    ax.set_title('Complex-step vs diferencia central'); ax.legend(); ax.grid(True, alpha=0.3)

    fig.suptitle('Linealización numérica: errores y Jacobiano', fontsize=14, fontweight='bold')
    plt.tight_layout()
    _savefig(fig, "linealizacion-numerica-analisis")


# ===================================================================== #
#  respuesta-frecuencia-ss-analisis  (sin decorador @figura)
# ===================================================================== #
def _freqss_extended():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Panel 1: Bode desde matrices A, B, C, D
    ax1 = axes[0, 0]; ax1b = ax1.twinx()
    L_val = 1e-3; R_val = 0.5
    A_ss = np.array([[-R_val/L_val]]); B_ss = np.array([[1/L_val]])
    C_ss = np.array([[1]]); D_ss = np.array([[0]])
    w = np.logspace(1, 6, 500)
    G_w = np.array([C_ss @ np.linalg.solve(1j*wi*np.eye(1) - A_ss, B_ss) + D_ss for wi in w]).squeeze()
    ax1.semilogx(w/(2*np.pi), 20*np.log10(np.abs(G_w)), 'b-', lw=2)
    ax1b.semilogx(w/(2*np.pi), np.degrees(np.angle(G_w)), 'r--', lw=2)
    ax1.set_xlabel('Frecuencia (Hz)'); ax1.set_ylabel('Ganancia (dB)', color='b')
    ax1b.set_ylabel('Fase (°)', color='r')
    ax1.set_title('Bode desde matrices de estado'); ax1.grid(True, alpha=0.3)

    # Panel 2: Planta MIMO 2x2 — valores singulares
    ax = axes[0, 1]
    w2 = np.logspace(1, 5, 500)
    wn = 1000; zeta = 0.7; wL = 200
    G11 = wn**2 / ((-w2**2) + 2j*zeta*wn*w2 + wn**2)
    G12 = 1j*w2*wL / ((-w2**2) + 2j*zeta*wn*w2 + wn**2)
    sv_max = np.maximum(np.abs(G11), np.abs(G12)) * 1.3
    sv_min = np.abs(G11) * 0.7
    ax.semilogx(w2/(2*np.pi), 20*np.log10(sv_max), 'b-', lw=2, label=r'$\bar\sigma(G)$ (máx)')
    ax.semilogx(w2/(2*np.pi), 20*np.log10(sv_min), 'r-', lw=2, label=r'$\sigma_{min}(G)$')
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('dB')
    ax.set_title('Valores singulares MIMO'); ax.legend(); ax.grid(True, alpha=0.3)

    # Panel 3: Efecto retardo de cómputo en Bode
    ax = axes[1, 0]
    w3 = np.logspace(2, 5, 500)
    Td = 100e-6
    G_no_delay = 1 / (1 + 1j*w3/2000)
    G_delay = G_no_delay * np.exp(-1j*w3*Td)
    ax.semilogx(w3/(2*np.pi), np.degrees(np.angle(G_no_delay)), 'b-', lw=2, label='Sin retardo')
    ax.semilogx(w3/(2*np.pi), np.degrees(np.angle(G_delay)), 'r-', lw=2, label=f'Td={Td*1e6:.0f}µs')
    ax.axhline(-180, color='gray', ls='--')
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Fase (°)')
    ax.set_title('Efecto del retardo de cómputo'); ax.legend(); ax.grid(True, alpha=0.3)

    # Panel 4: Validación modelo vs medida (simulada)
    ax = axes[1, 1]
    np.random.seed(7)
    f_meas = np.logspace(1, 4, 50)
    w_meas = 2*np.pi*f_meas
    G_model = 1 / (1 + 1j*w_meas/2000) * np.exp(-1j*w_meas*50e-6)
    G_measured = G_model * (1 + 0.05*np.random.randn(len(f_meas)) +
                            1j*0.05*np.random.randn(len(f_meas)))
    ax.semilogx(f_meas, 20*np.log10(np.abs(G_model)), 'b-', lw=2, label='Modelo')
    ax.semilogx(f_meas, 20*np.log10(np.abs(G_measured)), 'r.', markersize=6, label='Medido')
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Ganancia (dB)')
    ax.set_title('Validación modelo vs medida'); ax.legend(); ax.grid(True, alpha=0.3)

    fig.suptitle('Respuesta en frecuencia desde espacio de estados', fontsize=14, fontweight='bold')
    plt.tight_layout()
    _savefig(fig, "respuesta-frecuencia-ss-analisis")


# ===================================================================== #
#  medicion-impedancia-inyeccion-analisis  (sin decorador @figura)
# ===================================================================== #
def _measz_extended():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Panel 1: Señal inyectada y respuesta
    ax = axes[0, 0]
    np.random.seed(3)
    t = np.linspace(0, 0.1, 10000)
    f_inj = 200
    v_pert = 5 * np.sin(2*np.pi*f_inj*t)
    i_resp = 2.5 * np.sin(2*np.pi*f_inj*t - np.pi/4) + 0.3*np.random.randn(len(t))
    ax.plot(t*1000, v_pert, 'b-', lw=1.5, label='$v_p$ (V)')
    ax.plot(t*1000, i_resp*4, 'r-', lw=1.5, alpha=0.8, label='$i$ (A×4)')
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Amplitud')
    ax.set_title(f'Señal inyectada ({f_inj} Hz) y respuesta')
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax.set_xlim([0, 15])

    # Panel 2: Espectro de tensión (DFT)
    ax = axes[0, 1]
    N = len(t)
    V_fft = np.abs(np.fft.rfft(v_pert)) * 2 / N
    I_fft = np.abs(np.fft.rfft(i_resp)) * 2 / N
    f_fft = np.fft.rfftfreq(N, t[1]-t[0])
    ax.semilogy(f_fft, V_fft + 1e-6, 'b-', lw=1.5, label='|V(f)|')
    ax.semilogy(f_fft, I_fft*2 + 1e-6, 'r-', lw=1.5, label='|I(f)|×2')
    ax.set_xlim([0, 1000]); ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Amplitud')
    ax.set_title('Espectro DFT'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    # Panel 3: Impedancia medida (módulo y fase) en barrido
    ax = axes[1, 0]
    np.random.seed(5)
    f_sweep = np.array([10, 20, 50, 100, 200, 500, 1000, 2000, 5000])
    Z_true = 0.5 + 1j * 2*np.pi*f_sweep * 1e-3
    Z_noise = Z_true * (1 + 0.03*np.random.randn(len(f_sweep)) +
                        1j*0.03*np.random.randn(len(f_sweep)))
    ax.loglog(f_sweep, np.abs(Z_true), 'b-', lw=2, label='Z teórica')
    ax.loglog(f_sweep, np.abs(Z_noise), 'r.', markersize=10, label='Z medida')
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel(r'|Z| ($\Omega$)')
    ax.set_title('Impedancia: teórica vs medida'); ax.legend(); ax.grid(True, alpha=0.3)

    # Panel 4: Coherencia y SNR del barrido
    ax = axes[1, 1]
    f_coh = np.logspace(1, 4, 50)
    snr = 30 - 10*np.log10(f_coh/10)
    coh = 1 / (1 + 10**(-snr/10))
    ax.semilogx(f_coh, coh, 'g-', lw=2)
    ax.axhline(0.9, color='r', ls='--', label='γ²=0.9 (límite)')
    ax.fill_between(f_coh, 0.9, coh, where=coh >= 0.9, alpha=0.2, color='green', label='Válido')
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Coherencia γ²')
    ax.set_title('Coherencia del barrido de impedancia'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    fig.suptitle('Medición de impedancia por inyección de señal', fontsize=14, fontweight='bold')
    plt.tight_layout()
    _savefig(fig, "medicion-impedancia-inyeccion-analisis")


# ===================================================================== #
#  barrido-parametrico-analisis  (sin decorador @figura)
# ===================================================================== #
def _barrido_extended():
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import signal as sg
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Panel 1: Margen de fase vs Kp (barrido 1D)
    ax = axes[0, 0]
    Kp_arr = np.logspace(-1, 2, 200)
    wc_approx = 10 * np.sqrt(np.sqrt(1 + 4*(Kp_arr/10)**2) - 1) / np.sqrt(2)
    PM_approx = 90 - np.degrees(np.arctan2(wc_approx**2, 10*wc_approx))
    ax.semilogx(Kp_arr, PM_approx, 'b-', lw=2)
    ax.axhline(45, color='r', ls='--', label='PM=45°')
    ax.fill_between(Kp_arr, 45, PM_approx, where=PM_approx > 45, alpha=0.2, color='green')
    ax.set_xlabel('$K_p$'); ax.set_ylabel('Margen de fase (°)')
    ax.set_title('Barrido de $K_p$ — margen de fase'); ax.legend(); ax.grid(True, alpha=0.3)

    # Panel 2: Mapa de estabilidad 2D (Kp, Ti)
    ax = axes[0, 1]
    Kp_2d = np.logspace(-1, 2, 40)
    Ti_2d = np.logspace(-3, 0, 40)
    KP, TI = np.meshgrid(Kp_2d, Ti_2d)
    PM_2d = 60 - 20*np.log10(KP) - 10*np.log10(1 + 1/TI)
    im = ax.contourf(Kp_2d, Ti_2d, PM_2d, levels=np.linspace(-20, 80, 20), cmap='RdYlGn')
    ax.contour(Kp_2d, Ti_2d, PM_2d, levels=[45], colors='white', linewidths=2)
    plt.colorbar(im, ax=ax, label='PM (°)')
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlabel('$K_p$'); ax.set_ylabel('$T_i$ (s)')
    ax.set_title('Mapa de estabilidad 2D (PM)')

    # Panel 3: Eigenvalores durante barrido de ganancia
    ax = axes[1, 0]
    np.random.seed(0)
    gains = np.linspace(0.5, 5, 20)
    A_nom = np.array([[-2, 1], [-1, -3]])
    B_nom = np.array([[0], [1]])
    K_nom = np.array([[1, 0]])
    for g in gains:
        A_cl = A_nom - g * B_nom @ K_nom
        eigs = np.linalg.eigvals(A_cl)
        color = 'g' if all(np.real(eigs) < 0) else 'r'
        ax.scatter(np.real(eigs), np.imag(eigs), s=20, c=color, alpha=0.6)
    ax.axvline(0, color='k', lw=1.5)
    ax.set_xlabel('Re(λ)'); ax.set_ylabel('Im(λ)')
    ax.set_title('Eigenvalores vs ganancia (verde=estable)'); ax.grid(True, alpha=0.3)

    # Panel 4: Respuesta al escalón para distintos Kp
    ax = axes[1, 1]
    t = np.linspace(0, 0.5, 500)
    for Kp_val, col in [(0.5, 'r'), (2, 'b'), (5, 'g'), (10, 'orange')]:
        wn2 = np.sqrt(100*Kp_val); zeta2 = 10/(2*wn2)
        sys_cl = sg.lti([wn2**2], [1, 2*zeta2*wn2, wn2**2])
        _, y = sg.step(sys_cl, T=t)
        ax.plot(t*1000, y, color=col, lw=2, label=f'Kp={Kp_val}')
    ax.axhline(1, color='k', ls='--', alpha=0.5)
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Respuesta')
    ax.set_title('Respuesta al escalón — barrido Kp'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    fig.suptitle('Barrido paramétrico: 1D, 2D y optimización', fontsize=14, fontweight='bold')
    plt.tight_layout()
    _savefig(fig, "barrido-parametrico-analisis")


# ===================================================================== #
#  discretizacion-controladores-analisis  (sin decorador @figura)
# ===================================================================== #
def _disc_extended():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Panel 1: Comparación de métodos de discretización en el plano z
    ax = axes[0, 0]
    theta = np.linspace(0, 2*np.pi, 200)
    ax.plot(np.cos(theta), np.sin(theta), 'k-', lw=1.5, label='Círculo unitario')
    s_poles = [-5, -2+3j, -2-3j, -10]
    Ts_d = 0.01
    colors = ['b', 'r', 'g']
    methods = ['FE', 'BE', 'Tustin']
    for method, col in zip(methods, colors):
        z_poles = []
        for s in s_poles:
            if method == 'FE':
                z = 1 + s*Ts_d
            elif method == 'BE':
                z = 1/(1 - s*Ts_d)
            else:
                z = (1 + s*Ts_d/2)/(1 - s*Ts_d/2)
            z_poles.append(z)
        ax.scatter([np.real(z) for z in z_poles], [np.imag(z) for z in z_poles],
                   s=80, c=col, marker='x', zorder=5, label=method)
    ax.set_xlim([-2, 2]); ax.set_ylim([-2, 2])
    ax.axvline(0, color='gray', lw=0.5); ax.axhline(0, color='gray', lw=0.5)
    ax.set_xlabel('Re(z)'); ax.set_ylabel('Im(z)')
    ax.set_title('Mapeo de polos — plano z'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    # Panel 2: Distorsión de la respuesta en frecuencia (warping)
    ax = axes[0, 1]
    w_cont = np.logspace(1, np.log10(np.pi/Ts_d*0.9), 200)
    w_tustin = 2/Ts_d * np.tan(w_cont*Ts_d/2)
    ax.semilogx(w_cont, w_cont, 'k--', lw=2, label='Ideal (1:1)')
    ax.semilogx(w_cont, w_tustin, 'b-', lw=2, label='Tustin (frecuencia warped)')
    ax.axvline(np.pi/Ts_d/10, color='gray', ls=':', label=r'$\omega_s/20$')
    ax.set_xlabel('Frecuencia continua (rad/s)'); ax.set_ylabel('Frecuencia mapeada (rad/s)')
    ax.set_title('Warping de frecuencia Tustin'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    # Panel 3: Pérdida de margen de fase por retardo de cómputo
    ax = axes[1, 0]
    f_arr = np.logspace(1, 4, 200)
    w_arr = 2*np.pi*f_arr
    for k_delay, col in [(1, 'b'), (2, 'r'), (3, 'g')]:
        phase_loss = np.degrees(k_delay * w_arr * Ts_d)
        ax.semilogx(f_arr, phase_loss, color=col, lw=2, label=f'{k_delay} muestra(s)')
    ax.axhline(30, color='gray', ls='--', label='30° (límite)')
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Pérdida de fase (°)')
    ax.set_title('Pérdida de fase por retardo de cómputo'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    # Panel 4: Respuesta escalón — continuo vs discreto (distintos Ts)
    ax = axes[1, 1]
    t_cont = np.linspace(0, 0.1, 10000)
    wn = 200; zeta = 0.7
    y_cont = 1 - np.exp(-zeta*wn*t_cont) * (np.cos(wn*np.sqrt(1-zeta**2)*t_cont) +
             zeta/np.sqrt(1-zeta**2)*np.sin(wn*np.sqrt(1-zeta**2)*t_cont))
    ax.plot(t_cont*1000, y_cont, 'k-', lw=2, label='Continuo')
    for Ts_val, col in [(0.5e-3, 'b'), (2e-3, 'r'), (5e-3, 'g')]:
        t_d = np.arange(0, 0.1, Ts_val)
        y_d = np.interp(t_d, t_cont, y_cont)
        ax.step(t_d*1000, y_d, where='post', color=col, lw=1.5,
                label=f'Ts={Ts_val*1000:.1f}ms', alpha=0.8)
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Respuesta')
    ax.set_title('Escalón: continuo vs discreto'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    fig.suptitle('Discretización de controladores: métodos, retardo y precisión', fontsize=14, fontweight='bold')
    plt.tight_layout()
    _savefig(fig, "discretizacion-controladores-analisis")


def _sistema_primer_orden_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Panel 1: Respuesta al escalón para distintos tau
    ax = axes[0, 0]
    t = np.linspace(0, 0.05, 500)
    for tau, col in [(0.005, 'b'), (0.01, 'g'), (0.02, 'r')]:
        y = 1 - np.exp(-t/tau)
        ax.plot(t*1000, y, color=col, lw=2, label=f'τ={tau*1000:.0f}ms')
    ax.axhline(0.632, color='gray', ls='--', alpha=0.7, label='63.2%')
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Respuesta')
    ax.set_title('Escalón para distintos τ'); ax.legend(); ax.grid(True, alpha=0.3)

    # Panel 2: Bode del primer orden
    ax = axes[0, 1]
    tau_bode = 0.01
    w = np.logspace(0, 5, 500)
    G = 1 / (1j*w*tau_bode + 1)
    ax.semilogx(w, 20*np.log10(np.abs(G)), 'b-', lw=2)
    ax.axvline(1/tau_bode, color='r', ls='--', label=f'ω=1/τ={1/tau_bode:.0f}')
    ax.axhline(-3, color='gray', ls=':')
    ax.set_xlabel('ω (rad/s)'); ax.set_ylabel('Ganancia (dB)')
    ax.set_title('Bode primer orden'); ax.legend(); ax.grid(True, alpha=0.3)

    # Panel 3: Filtro digital IIR vs analógico
    ax = axes[1, 0]
    np.random.seed(7)
    Ts = 1e-4; tau_f = 1e-3
    alpha = np.exp(-Ts/tau_f)
    t_d = np.arange(0, 0.02, Ts)
    u_noisy = np.ones(len(t_d)) + 0.3*np.random.randn(len(t_d))
    y_filt = np.zeros(len(t_d))
    for i in range(1, len(t_d)):
        y_filt[i] = alpha*y_filt[i-1] + (1-alpha)*u_noisy[i]
    ax.plot(t_d*1000, u_noisy, 'b-', lw=0.8, alpha=0.6, label='Señal ruidosa')
    ax.plot(t_d*1000, y_filt, 'r-', lw=2, label='Filtrada (IIR)')
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Amplitud')
    ax.set_title('Filtro IIR primer orden'); ax.legend(); ax.grid(True, alpha=0.3)

    # Panel 4: Lazo de corriente — efecto de L sobre el ancho de banda
    ax = axes[1, 1]
    L_arr = np.logspace(-4, -2, 100)
    R = 0.5; Kp_fixed = 5
    wc_approx = R/L_arr + Kp_fixed/L_arr
    ax.loglog(L_arr*1000, wc_approx/(2*np.pi), 'b-', lw=2)
    ax.axhline(1000, color='r', ls='--', label='1 kHz')
    ax.set_xlabel('Inductancia L (mH)'); ax.set_ylabel('BW (Hz)')
    ax.set_title('BW lazo corriente vs L'); ax.legend(); ax.grid(True, alpha=0.3)

    fig.suptitle('Sistema de primer orden: respuesta, Bode y filtrado', fontsize=14, fontweight='bold')
    plt.tight_layout()
    _savefig(fig, "sistema-primer-orden-analisis")


def _current_limiting_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Panel 1: Plano dq con círculo de limitación
    ax = axes[0, 0]
    theta = np.linspace(0, 2*np.pi, 200)
    Imax = 1.2
    ax.plot(Imax*np.cos(theta), Imax*np.sin(theta), 'r-', lw=2, label=f'|i|={Imax} pu')
    points = [(1.0, 0.0, 'Normal (P)', 'bo'), (0.0, 1.0, 'Reactiva', 'go')]
    for id_val, iq_val, label, fmt in points:
        ax.plot(id_val, iq_val, fmt, markersize=10, label=label)
    id_out, iq_out = 0.9, 0.9
    i_mag = np.sqrt(id_out**2 + iq_out**2)
    id_lim = id_out/i_mag * Imax
    iq_lim = iq_out/i_mag * Imax
    ax.annotate('', xy=(id_lim, iq_lim), xytext=(id_out, iq_out),
                arrowprops=dict(arrowstyle='->', color='purple', lw=2))
    ax.plot(id_out, iq_out, 'rs', markersize=10, label='Sin límite')
    ax.plot(id_lim, iq_lim, 'r^', markersize=10, label='Proyectado')
    ax.set_xlabel('$i_d$ (pu)'); ax.set_ylabel('$i_q$ (pu)')
    ax.set_title('Limitación en plano dq'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax.set_aspect('equal'); ax.set_xlim([-1.5, 1.5]); ax.set_ylim([-1.5, 1.5])

    # Panel 2: LVRT — reactive current boost
    ax = axes[0, 1]
    V_pu = np.linspace(0, 1, 100)
    dV = 1 - V_pu
    Iq_boost = np.minimum(2 * dV, 1.2)
    ax.plot(V_pu, Iq_boost, 'b-', lw=2, label=r'$\Delta I_q = 2\Delta V$')
    ax.axhline(1.0, color='r', ls='--', label='$I_q$ nominal')
    ax.fill_between(V_pu, 0, Iq_boost, alpha=0.2, color='blue')
    ax.set_xlabel('Tensión (pu)'); ax.set_ylabel('$I_q$ inyectada (pu)')
    ax.set_title('LVRT: reactive current boost'); ax.legend(); ax.grid(True, alpha=0.3)

    # Panel 3: Anti-windup back-calculation
    ax = axes[1, 0]
    t = np.linspace(0, 0.1, 1000)
    dt = t[1]-t[0]
    Kp_pi = 5; Ki_pi = 200; Usat = 1.0; Kaw = 10
    ref = np.ones(len(t))
    y_no_aw = np.zeros(len(t)); int_no_aw = 0.0
    y_aw = np.zeros(len(t)); int_aw = 0.0; plant_state = 0.0
    for i in range(1, len(t)):
        err_no = ref[i] - y_no_aw[i-1]
        u_no_aw = Kp_pi*err_no + int_no_aw
        u_no_aw_sat = np.clip(u_no_aw, -Usat, Usat)
        int_no_aw += Ki_pi*err_no*dt
        y_no_aw[i] = y_no_aw[i-1] + (u_no_aw_sat - y_no_aw[i-1])*dt/0.01
        err_aw = ref[i] - plant_state
        u_aw = Kp_pi*err_aw + int_aw
        u_aw_sat = np.clip(u_aw, -Usat, Usat)
        int_aw += (Ki_pi*err_aw - Kaw*(u_aw - u_aw_sat)) * dt
        plant_state += (u_aw_sat - plant_state) * dt / 0.01
        y_aw[i] = plant_state
    ax.plot(t*1000, y_no_aw, 'r-', lw=2, label='Sin anti-windup')
    ax.plot(t*1000, y_aw, 'b-', lw=2, label='Con anti-windup')
    ax.axhline(1, color='k', ls='--', alpha=0.5)
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Respuesta')
    ax.set_title('Anti-windup back-calculation'); ax.legend(); ax.grid(True, alpha=0.3)

    # Panel 4: Corriente durante hueco de tensión
    ax = axes[1, 1]
    t_fault = np.linspace(0, 0.3, 3000)
    V_grid = np.ones(len(t_fault))
    V_grid[1000:2000] = 0.2
    dV_fault = 1 - V_grid
    Iq_ref_limited = np.minimum(2*dV_fault, 1.2)
    Id_available = np.sqrt(np.maximum(0, 1.2**2 - Iq_ref_limited**2))
    ax.plot(t_fault*1000, V_grid, 'k-', lw=2, label='V (pu)')
    ax.plot(t_fault*1000, Id_available, 'b-', lw=2, label='$I_d$ disponible')
    ax.plot(t_fault*1000, Iq_ref_limited, 'r-', lw=2, label='$I_q$ inyectada')
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Amplitud (pu)')
    ax.set_title('Corriente durante hueco de tensión'); ax.legend(); ax.grid(True, alpha=0.3)

    fig.suptitle('Current limiting: dq, LVRT, anti-windup y hueco', fontsize=14, fontweight='bold')
    plt.tight_layout()
    _savefig(fig, "current-limiting-analisis")


def _controlabilidad_observabilidad_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Panel 1: Hankel singular values de sistema de orden 6
    ax = axes[0, 0]
    hsv_vals = [10, 3, 1.5, 0.1, 0.02, 0.005]
    colors_bar = ['b']*3 + ['r']*3
    ax.bar(range(1, 7), hsv_vals, color=colors_bar, edgecolor='black')
    ax.axhline(0.1, color='r', ls='--', label='Umbral σ/σ₁=0.01')
    ax.set_xlabel('Modo i'); ax.set_ylabel('Hankel SV σᵢ')
    ax.set_title('Hankel SVs — truncamiento balanceado')
    ax.legend(); ax.grid(True, alpha=0.3, axis='y')
    ax.text(4.5, 0.3, 'Eliminar', color='red', fontsize=10, ha='center')

    # Panel 2: Matriz de controlabilidad — rango
    ax = axes[0, 1]
    A_ctrl = np.array([[0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [-6.0, -11.0, -6.0]])
    B_ctrl = np.array([[0.0], [0.0], [1.0]])
    C_mat = np.hstack([B_ctrl, A_ctrl @ B_ctrl, A_ctrl @ A_ctrl @ B_ctrl])
    im = ax.imshow(np.abs(C_mat), cmap='Blues', aspect='auto')
    plt.colorbar(im, ax=ax)
    ax.set_title(f'Matriz controlabilidad (rango={np.linalg.matrix_rank(C_mat)})')
    ax.set_xlabel('Columna'); ax.set_ylabel('Fila')

    # Panel 3: Respuesta del observador de Luenberger
    ax = axes[1, 0]
    t = np.linspace(0, 1, 1000)
    dt = t[1] - t[0]
    a_plant = -3.0; b_plant = 1.0; c_plant = 1.0; L_gain = -8.0
    x_true = np.zeros(len(t)); x_hat = np.zeros(len(t)); x_hat[0] = 0.5
    u_in = np.ones(len(t))
    for i in range(1, len(t)):
        y_obs = c_plant * x_true[i-1]
        x_true[i] = x_true[i-1] + dt*(a_plant*x_true[i-1] + b_plant*u_in[i-1])
        x_hat[i] = x_hat[i-1] + dt*((a_plant - L_gain*c_plant)*x_hat[i-1] +
                                      b_plant*u_in[i-1] + L_gain*y_obs)
    ax.plot(t, x_true, 'b-', lw=2, label='Estado real x')
    ax.plot(t, x_hat, 'r--', lw=2, label='Estimado x̂')
    ax.plot(t, x_true - x_hat, 'g-', lw=1.5, label='Error x - x̂')
    ax.set_xlabel('Tiempo (s)'); ax.set_ylabel('Estado')
    ax.set_title('Observador de Luenberger'); ax.legend(); ax.grid(True, alpha=0.3)

    # Panel 4: Modos del sistema y controlabilidad
    ax = axes[1, 1]
    A2 = np.array([[-1.0, 2.0], [-3.0, -4.0]])
    B2 = np.array([[1.0], [0.0]])
    modes, V = np.linalg.eig(A2)
    Bmod = np.linalg.solve(V, B2)
    for i, (mode, b_proj) in enumerate(zip(modes, Bmod)):
        sz = 200*np.abs(b_proj[0]) + 50
        col = 'blue' if np.abs(b_proj[0]) > 0.1 else 'red'
        ax.scatter(np.real(mode), np.imag(mode), s=sz, c=col,
                   marker='x', zorder=5, linewidths=3)
        ax.annotate(f'|B_m{i+1}|={np.abs(b_proj[0]):.2f}',
                   (np.real(mode)+0.1, np.imag(mode)+0.1), fontsize=9)
    ax.axvline(0, color='k', lw=1); ax.axhline(0, color='k', lw=1)
    ax.set_xlabel('Re(λ)'); ax.set_ylabel('Im(λ)')
    ax.set_title('Controlabilidad modal (tamaño ∝ |Bᵢ|)'); ax.grid(True, alpha=0.3)

    fig.suptitle('Controlabilidad y observabilidad: gramians, SVD y observador', fontsize=14, fontweight='bold')
    plt.tight_layout()
    _savefig(fig, "controlabilidad-observabilidad-analisis")


def _observador_estados_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Panel 1: Ganancia de Kalman vs relación Q/R
    ax = axes[0, 0]
    Q_R_ratio = np.logspace(-3, 3, 200)
    K_kalman = Q_R_ratio / (1 + Q_R_ratio)
    ax.semilogx(Q_R_ratio, K_kalman, 'b-', lw=2)
    ax.axhline(0.5, color='r', ls='--', label='K=0.5 (Q=R)')
    ax.set_xlabel('Q/R'); ax.set_ylabel('Ganancia Kalman K')
    ax.set_title('Ganancia Kalman vs Q/R'); ax.legend(); ax.grid(True, alpha=0.3)

    # Panel 2: Filtro de Kalman 1D — tracking de señal ruidosa
    ax = axes[0, 1]
    np.random.seed(42)
    N_kal = 200; dt_kal = 0.01
    t_k = np.arange(N_kal)*dt_kal
    x_true_k = np.sin(2*np.pi*2*t_k) + 0.5*np.sin(2*np.pi*5*t_k)
    y_noisy = x_true_k + 0.5*np.random.randn(N_kal)
    x_hat_k = np.zeros(N_kal); P_k = 1.0; Q_k = 0.01; R_k = 0.25
    for i in range(1, N_kal):
        P_pred = P_k + Q_k
        Kg = P_pred / (P_pred + R_k)
        x_hat_k[i] = x_hat_k[i-1] + Kg * (y_noisy[i] - x_hat_k[i-1])
        P_k = (1 - Kg) * P_pred
    ax.plot(t_k, y_noisy, 'gray', lw=0.8, alpha=0.7, label='Medida ruidosa')
    ax.plot(t_k, x_true_k, 'b-', lw=2, label='Señal real')
    ax.plot(t_k, x_hat_k, 'r-', lw=2, label='Kalman')
    ax.set_xlabel('Tiempo (s)'); ax.set_ylabel('Amplitud')
    ax.set_title('Kalman 1D'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    # Panel 3: Comparación observador Luenberger vs Kalman — error de estimación
    ax = axes[1, 0]
    np.random.seed(0)
    err_luen = 0.5 * np.exp(-t_k*10)
    err_kalm = 0.5 * np.exp(-t_k*8) * (1 + 0.1*np.random.randn(N_kal))
    ax.plot(t_k, err_luen, 'b-', lw=2, label='Luenberger')
    ax.plot(t_k, err_kalm, 'r-', lw=1.5, label='Kalman', alpha=0.9)
    ax.axhline(0, color='k', ls='--')
    ax.set_xlabel('Tiempo (s)'); ax.set_ylabel('Error estimación')
    ax.set_title('Luenberger vs Kalman — error'); ax.legend(); ax.grid(True, alpha=0.3)

    # Panel 4: Observador con disturbio (integral)
    ax = axes[1, 1]
    t_dist = np.linspace(0, 2, 500)
    dt2 = t_dist[1]-t_dist[0]
    x_aug = np.zeros((2, len(t_dist)))
    x_real_d = np.zeros(len(t_dist)); d_real = 0.3
    np.random.seed(1)
    for i in range(1, len(t_dist)):
        x_real_d[i] = x_real_d[i-1] + dt2*(-2*x_real_d[i-1] + 1 + d_real)
        y_meas = x_real_d[i] + 0.05*np.random.randn()
        x_aug[0, i] = x_aug[0, i-1] + dt2*(-2*x_aug[0, i-1] + 1 + x_aug[1, i-1] + 5*(y_meas - x_aug[0, i-1]))
        x_aug[1, i] = x_aug[1, i-1] + dt2*2*(y_meas - x_aug[0, i-1])
    ax.plot(t_dist, x_real_d, 'b-', lw=2, label='Estado real')
    ax.plot(t_dist, x_aug[0], 'r--', lw=2, label='Observador (x̂)')
    ax.plot(t_dist, x_aug[1], 'g-', lw=2, label='Disturbio estimado')
    ax.axhline(d_real, color='g', ls=':', alpha=0.7)
    ax.set_xlabel('Tiempo (s)'); ax.set_ylabel('Amplitud')
    ax.set_title('Observador con disturbio estimado'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    fig.suptitle('Observadores de estado: Luenberger, Kalman y con disturbio', fontsize=14, fontweight='bold')
    plt.tight_layout()
    _savefig(fig, "observador-estados-analisis")


def _control_repetitivo_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Panel 1: Espectro de corriente antes y después del repetitivo
    ax = axes[0, 0]
    harmonics = np.arange(1, 21)
    amp_before = np.zeros(20)
    amp_before[0]=100; amp_before[2]=15; amp_before[4]=10
    amp_before[6]=6; amp_before[8]=4; amp_before[10]=3
    amp_after = np.zeros(20)
    amp_after[0]=100; amp_after[2]=1.5; amp_after[4]=0.8
    amp_after[6]=0.6; amp_after[8]=0.4; amp_after[10]=0.3
    w_bar = 0.35
    ax.bar(harmonics-w_bar/2, amp_before, w_bar, label='Sin repetitivo', color='red', alpha=0.7)
    ax.bar(harmonics+w_bar/2, amp_after, w_bar, label='Con repetitivo', color='blue', alpha=0.7)
    ax.set_xlabel('Orden del armónico'); ax.set_ylabel('Amplitud (A)')
    thd_b = np.sqrt(np.sum(amp_before[1:]**2))/amp_before[0]*100
    thd_a = np.sqrt(np.sum(amp_after[1:]**2))/amp_after[0]*100
    ax.set_title(f'Espectro (THD: {thd_b:.1f}% → {thd_a:.1f}%)')
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3, axis='y')

    # Panel 2: Convergencia del error — ciclos
    ax = axes[0, 1]
    cycles = np.arange(0, 20)
    err_pi = 8 * np.ones(len(cycles))
    err_rep = np.maximum(8 * (0.4)**cycles, 0.5)
    ax.plot(cycles, err_pi, 'r-', lw=2, label='Solo PI')
    ax.plot(cycles, err_rep, 'b-o', lw=2, markersize=5, label='PI + Repetitivo')
    ax.axhline(2, color='gray', ls='--', label='Objetivo THD=2%')
    ax.set_xlabel('Ciclo de red'); ax.set_ylabel('THD (%)')
    ax.set_title('Convergencia del control repetitivo'); ax.legend(); ax.grid(True, alpha=0.3)

    # Panel 3: Diagrama de Bode del lazo repetitivo
    ax = axes[1, 0]
    f_rep = np.linspace(50, 5000, 2000)
    gains = np.zeros(len(f_rep))
    for h in np.arange(50, 5001, 50):
        sigma = 20.0
        gains += 20.0 / (1 + ((f_rep - h)/sigma)**2)
    ax.plot(f_rep, gains, 'b-', lw=1.5)
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Ganancia (dB)')
    ax.set_title('Ganancia del controlador repetitivo'); ax.grid(True, alpha=0.3)

    # Panel 4: Corriente con y sin control repetitivo (forma de onda)
    ax = axes[1, 1]
    t_wave = np.linspace(0, 0.04, 2000)
    f0 = 50; I1 = 10
    i_ref = I1 * np.sin(2*np.pi*f0*t_wave)
    i_pi = i_ref + 1.5*np.sin(2*np.pi*3*f0*t_wave) + 1.0*np.sin(2*np.pi*5*f0*t_wave)
    i_rep = i_ref + 0.15*np.sin(2*np.pi*3*f0*t_wave) + 0.1*np.sin(2*np.pi*5*f0*t_wave)
    ax.plot(t_wave*1000, i_pi, 'r-', lw=1.5, label='Solo PI', alpha=0.8)
    ax.plot(t_wave*1000, i_rep, 'b-', lw=2, label='PI + Repetitivo')
    ax.plot(t_wave*1000, i_ref, 'k--', lw=1.5, label='Referencia', alpha=0.7)
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Corriente (A)')
    ax.set_title('Forma de onda: PI vs PI+Repetitivo'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    fig.suptitle('Control repetitivo: principio IMP, diseño y convergencia', fontsize=14, fontweight='bold')
    plt.tight_layout()
    _savefig(fig, "control-repetitivo-analisis")


# ===================================================================== #
#  diagrama-bloques-analisis
# ===================================================================== #
def _diagrama_bloques_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    w = np.logspace(1, 5, 500); s = 1j*w
    Kp=10; Ti=0.01; L=1e-3; R=0.5
    C = Kp*(1+1/(Ti*s)); G = 1/(L*s+R)
    Lo = C*G; S = 1/(1+Lo); T = Lo/(1+Lo)
    ax=axes[0,0]; ax.axis('off')
    ax.text(0.5,0.7,r'$S=\frac{1}{1+L}$  $T=\frac{L}{1+L}$  $S+T=1$',ha='center',va='center',fontsize=13,transform=ax.transAxes)
    ax.text(0.5,0.4,r'$G_{cl}=\frac{G}{1+GH}$ (realimentación)',ha='center',va='center',fontsize=11,transform=ax.transAxes)
    ax.text(0.5,0.15,r'Bode integral: $\int_0^\infty\ln|S|d\omega=\pi\sum\mathrm{Re}(p_i^+)$',ha='center',va='center',fontsize=10,transform=ax.transAxes)
    ax.set_title('Álgebra de diagramas de bloques')
    ax=axes[0,1]
    ax.semilogx(w,20*np.log10(np.abs(S)),'b-',lw=2,label='|S|')
    ax.semilogx(w,20*np.log10(np.abs(T)),'r-',lw=2,label='|T|')
    ax.axhline(6,color='gray',ls='--',label='Ms=2 (6dB)')
    ax.set_xlabel('ω (rad/s)'); ax.set_ylabel('dB'); ax.set_title('S y T — lazo de corriente')
    ax.legend(fontsize=8); ax.grid(True,alpha=0.3)
    ax=axes[1,0]; t=np.linspace(0,0.02,500); tau=0.002; wL=300
    id_no=( 1-np.exp(-t/tau))*np.cos(wL*t); iq_no=( 1-np.exp(-t/tau))*np.sin(wL*t)*0.3
    id_ff= 1-np.exp(-t/tau); iq_ff=0.02*np.sin(2*np.pi*500*t)*np.exp(-t/tau)
    ax.plot(t*1000,id_no,'b-',lw=2,label='id sin FF'); ax.plot(t*1000,iq_no,'r-',lw=2,label='iq sin FF')
    ax.plot(t*1000,id_ff,'b--',lw=2,label='id con FF'); ax.plot(t*1000,iq_ff,'r--',lw=2,label='iq con FF')
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Corriente (pu)'); ax.set_title('Efecto feedforward dq')
    ax.legend(fontsize=7); ax.grid(True,alpha=0.3)
    ax=axes[1,1]; t2=np.linspace(0,0.05,500)
    y_pert=0.1*np.exp(-500*t2)*np.cos(2000*t2)
    ax.plot(t2*1000,y_pert,'b-',lw=2,label='Respuesta a perturbación')
    ax.axhline(0,color='k',ls='--',alpha=0.5); ax.fill_between(t2*1000,y_pert,0,alpha=0.2,color='blue')
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Salida'); ax.set_title('Rechazo de perturbación')
    ax.legend(); ax.grid(True,alpha=0.3)
    fig.suptitle('Diagrama de bloques: álgebra, S/T y feedforward dq',fontsize=14,fontweight='bold')
    plt.tight_layout(); _savefig(fig,"diagrama-bloques-analisis")


# ===================================================================== #
#  series-fourier-analisis
# ===================================================================== #
def _series_fourier_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    t=np.linspace(0,2,2000); f0=1
    x_sq=np.sign(np.sin(2*np.pi*f0*t))
    ax=axes[0,0]
    for N,col in [(1,'r'),(5,'g'),(20,'b')]:
        xa=sum(4/(n*np.pi)*np.sin(2*np.pi*n*f0*t) for n in range(1,2*N,2))
        ax.plot(t,xa,color=col,lw=1.5,label=f'N={N}')
    ax.plot(t,x_sq,'k-',lw=0.8,alpha=0.4,label='Cuadrada')
    ax.set_xlabel('t (s)'); ax.set_ylabel('x'); ax.set_title('Serie Fourier — señal cuadrada')
    ax.legend(fontsize=8); ax.grid(True,alpha=0.3)
    ax=axes[0,1]
    ns=np.arange(1,21,2); ax.bar(ns,4/(ns*np.pi),width=0.6,color='blue',edgecolor='black',alpha=0.7)
    ax.set_xlabel('Armónico n'); ax.set_ylabel('$b_n$'); ax.set_title('Espectro (cuadrada)'); ax.grid(True,alpha=0.3,axis='y')
    ax=axes[1,0]
    fs=20000; t_pw=np.arange(0,0.1,1/fs); fsw=2000; fund=50
    pwm=np.sign(0.8*np.sin(2*np.pi*fund*t_pw)-np.sign(np.sin(2*np.pi*fsw*t_pw)))
    X=np.abs(np.fft.rfft(pwm))*2/len(t_pw); ff=np.fft.rfftfreq(len(t_pw),1/fs)
    ax.semilogy(ff,X+1e-4,'b-',lw=0.8)
    ax.axvline(fund,color='r',ls='--',label=f'{fund}Hz'); ax.axvline(fsw,color='g',ls='--',label=f'{fsw}Hz')
    ax.set_xlim([0,5000]); ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Amplitud')
    ax.set_title('Espectro PWM'); ax.legend(fontsize=8); ax.grid(True,alpha=0.3)
    ax=axes[1,1]
    N2=512; fs2=1000; t2=np.arange(N2)/fs2; fsig=127
    x2=np.sin(2*np.pi*fsig*t2)
    Xr=np.abs(np.fft.rfft(x2))*2/N2; Xh=np.abs(np.fft.rfft(x2*np.hanning(N2)))*2/N2
    f2=np.fft.rfftfreq(N2,1/fs2)
    ax.semilogy(f2,Xr+1e-4,'r-',lw=1.5,label='Rectangular'); ax.semilogy(f2,Xh+1e-4,'b-',lw=1.5,label='Hanning')
    ax.set_xlim([80,200]); ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Amplitud')
    ax.set_title('Leakage: rectangular vs Hanning'); ax.legend(fontsize=8); ax.grid(True,alpha=0.3)
    fig.suptitle('Series de Fourier: reconstrucción, espectro y FFT',fontsize=14,fontweight='bold')
    plt.tight_layout(); _savefig(fig,"series-fourier-analisis")


# ===================================================================== #
#  controlador-resonante-analisis
# ===================================================================== #
def _controlador_resonante_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    w=np.logspace(2,4,2000); s=1j*w; w0=2*np.pi*50; Kp=1; Ki=100; wc=10
    Cid=Kp+2*Ki*s/(s**2+w0**2); Cbw=Kp+2*Ki*wc*s/(s**2+2*wc*s+w0**2)
    ax=axes[0,0]
    ax.semilogx(w/(2*np.pi),20*np.log10(np.abs(Cid)),'b-',lw=2,label='PR ideal')
    ax.semilogx(w/(2*np.pi),20*np.log10(np.abs(Cbw)),'r-',lw=2,label=f'PR BWc={wc}')
    ax.axvline(50,color='gray',ls=':'); ax.set_xlim([10,1000]); ax.set_ylim([-20,80])
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Ganancia (dB)'); ax.set_title('Bode PR ideal vs BW')
    ax.legend(fontsize=8); ax.grid(True,alpha=0.3)
    w2=np.logspace(2,np.log10(2*np.pi*800),3000); s2=1j*w2; Cm=np.ones(len(w2))*Kp
    for h in [1,3,5,7]: wh=h*w0; Cm=Cm+2*Ki*wc*s2/(s2**2+2*wc*s2+wh**2)
    ax=axes[0,1]
    ax.semilogx(w2/(2*np.pi),20*np.log10(np.abs(Cm)),'b-',lw=1.5)
    for h in [1,3,5,7]: ax.axvline(h*50,color='r',ls='--',alpha=0.5)
    ax.set_xlim([10,500]); ax.set_ylim([-20,80]); ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('dB')
    ax.set_title('PR multi-armónico (1°,3°,5°,7°)'); ax.grid(True,alpha=0.3)
    ax=axes[1,0]
    hn=np.arange(1,13); wd=0.35
    abef=np.array([100,0,15,0,10,0,6,0,4,0,3,0],dtype=float)
    aaft=np.array([100,0,1.5,0,0.8,0,0.6,0,1.8,0,1.3,0],dtype=float)
    ax.bar(hn-wd/2,abef[:12],wd,label='Sin PR',color='red',alpha=0.7)
    ax.bar(hn+wd/2,aaft[:12],wd,label='Con PR',color='blue',alpha=0.7)
    ax.set_xlabel('Armónico'); ax.set_ylabel('Amplitud (%)'); ax.set_title('THD: sin vs con PR multi')
    ax.legend(fontsize=8); ax.grid(True,alpha=0.3,axis='y')
    ax=axes[1,1]
    df=np.linspace(-2,2,100); gains=[]
    for dfi in df:
        wr=w0+2*np.pi*dfi; se=1j*wr
        gains.append(np.abs(Kp+2*Ki*wc*se/(se**2+2*wc*se+w0**2)))
    ax.plot(df,20*np.log10(gains),'b-',lw=2,label=f'PR BWc={wc}')
    ax.axvline(0,color='gray',ls=':'); ax.set_xlabel('Δf (Hz)'); ax.set_ylabel('Ganancia (dB)')
    ax.set_title('Sensibilidad a variación de frecuencia'); ax.legend(); ax.grid(True,alpha=0.3)
    fig.suptitle('Controlador PR: Bode, multi-armónico y sensibilidad',fontsize=14,fontweight='bold')
    plt.tight_layout(); _savefig(fig,"controlador-resonante-analisis")


# ===================================================================== #
#  power-synchronization-control-analisis
# ===================================================================== #
def _power_synchronization_control_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    delta=np.linspace(-np.pi/2,np.pi/2,200)
    ax=axes[0,0]
    for X,col,lab in [(0.1,'b','Fuerte X=0.1'),(0.5,'r','Débil X=0.5')]:
        ax.plot(np.degrees(delta),np.sin(delta)/X,color=col,lw=2,label=lab)
    ax.axhline(0.5/0.1,color='b',ls=':',alpha=0.5); ax.axhline(0.5/0.5,color='r',ls=':',alpha=0.5)
    ax.set_xlabel('δ (°)'); ax.set_ylabel('P (pu)'); ax.set_title('Curva P-δ: fuerte vs débil')
    ax.legend(fontsize=8); ax.grid(True,alpha=0.3)
    t=np.linspace(0,2,1000)
    ax=axes[0,1]
    for wn,zeta,col,lab in [(15,0.5,'b','SCR=10'),(5,0.3,'r','SCR=2')]:
        wd=wn*np.sqrt(max(1-zeta**2,0.01))
        y=0.5+0.3*(1-np.exp(-zeta*wn*t)*(np.cos(wd*t)+zeta/np.sqrt(max(1-zeta**2,0.01))*np.sin(wd*t)))
        ax.plot(t,y,color=col,lw=2,label=lab)
    ax.axhline(0.8,color='k',ls='--',alpha=0.5); ax.set_xlabel('Tiempo (s)'); ax.set_ylabel('P (pu)')
    ax.set_title('Respuesta PSC ante escalón P*'); ax.legend(); ax.grid(True,alpha=0.3)
    t2=np.linspace(0,10,1000)
    ax=axes[1,0]
    df_psc=-0.3*np.exp(-t2/0.5)*np.cos(5*t2); df_vsm=-0.3*(1-np.exp(-t2/2))*np.exp(-t2/3)
    ax.plot(t2,df_psc,'b-',lw=2,label='PSC'); ax.plot(t2,df_vsm,'r-',lw=2,label='VSM')
    ax.axhline(0,color='k',ls='--',alpha=0.5); ax.set_xlabel('Tiempo (s)'); ax.set_ylabel('Δf (Hz)')
    ax.set_title('PSC vs VSM: respuesta de frecuencia'); ax.legend(); ax.grid(True,alpha=0.3)
    SCR=np.linspace(1,10,100)
    ax=axes[1,1]
    ax.plot(SCR,10*(SCR-1)/SCR,'r-',lw=2,label='K_PSC máximo'); ax.axhline(5,color='b',ls='--',lw=2,label='K_PSC nominal=5')
    ax.fill_between(SCR,0,10*(SCR-1)/SCR,alpha=0.1,color='green')
    ax.set_xlabel('SCR'); ax.set_ylabel('K_PSC'); ax.set_title('Estabilidad PSC vs SCR')
    ax.legend(fontsize=8); ax.grid(True,alpha=0.3); ax.set_ylim([0,12])
    fig.suptitle('Power Synchronization Control: P-δ, respuesta y estabilidad',fontsize=14,fontweight='bold')
    plt.tight_layout(); _savefig(fig,"power-synchronization-control-analisis")


# ===================================================================== #
#  compensador-adelanto-atraso-analisis
# ===================================================================== #
def _compensador_adelanto_atraso_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import signal
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    w=np.logspace(1,5,500); s=1j*w
    z_l=100; p_l=1000; Clead=(s/z_l+1)/(s/p_l+1)
    z_a=20; p_a=2; Clag=(s/z_a+1)/(s/p_a+1)
    ax=axes[0,0]
    ax.semilogx(w,20*np.log10(np.abs(Clead)),'b-',lw=2,label='Adelanto')
    ax.semilogx(w,20*np.log10(np.abs(Clag)),'r-',lw=2,label='Atraso')
    ax2=ax.twinx()
    ax2.semilogx(w,np.degrees(np.angle(Clead)),'b--',lw=1.5)
    ax2.semilogx(w,np.degrees(np.angle(Clag)),'r--',lw=1.5)
    ax.set_xlabel('ω (rad/s)'); ax.set_ylabel('Ganancia (dB)'); ax2.set_ylabel('Fase (°)')
    ax.set_title('Bode: adelanto vs atraso'); ax.legend(fontsize=8); ax.grid(True,alpha=0.3)
    ax=axes[0,1]
    phi_arr=np.linspace(0,70,100); alpha=((1+np.sin(np.radians(phi_arr)))/(1-np.sin(np.radians(phi_arr))+1e-6))
    ax.semilogy(phi_arr,alpha,'b-',lw=2)
    ax.set_xlabel('φ_max (°)'); ax.set_ylabel('α = p/z'); ax.set_title('Ratio α vs adelanto de fase máximo')
    ax.grid(True,alpha=0.3)
    t=np.linspace(0,0.05,500)
    ax=axes[1,0]
    for zeta,col,lab in [(0.3,'r','Sin (ζ=0.3)'),(0.7,'b','Con adelanto (ζ=0.7)')]:
        wn=100; sys_tf=signal.lti([wn**2],[1,2*zeta*wn,wn**2]); _,y=signal.step(sys_tf,T=t)
        ax.plot(t*1000,y,color=col,lw=2,label=lab)
    ax.axhline(1,color='k',ls='--',alpha=0.5); ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Respuesta')
    ax.set_title('Escalón: efecto del compensador de adelanto'); ax.legend(); ax.grid(True,alpha=0.3)
    ax=axes[1,1]
    Kp_arr=np.logspace(-1,2,200); Ti=0.01
    PM_approx=60-20*np.log10(Kp_arr)-5*np.log10(1+1/Ti)
    ax.semilogx(Kp_arr,np.clip(PM_approx,-10,90),'b-',lw=2)
    ax.axhline(45,color='r',ls='--',label='PM=45°')
    ax.fill_between(Kp_arr,45,np.clip(PM_approx,-10,90),where=np.clip(PM_approx,-10,90)>45,alpha=0.2,color='green')
    ax.set_xlabel('Kp'); ax.set_ylabel('PM (°)'); ax.set_title('Margen de fase vs Kp'); ax.legend(); ax.grid(True,alpha=0.3)
    fig.suptitle('Compensador adelanto-atraso: diseño, Bode y efecto',fontsize=14,fontweight='bold')
    plt.tight_layout(); _savefig(fig,"compensador-adelanto-atraso-analisis")


# ===================================================================== #
#  frecuencias-segundo-orden-analisis
# ===================================================================== #
def _frecuencias_segundo_orden_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import signal
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    wn=100; zeta_arr=np.linspace(0,1,100)
    sigma=zeta_arr*wn; wd=wn*np.sqrt(np.maximum(0,1-zeta_arr**2))
    ax=axes[0,0]
    sc=ax.scatter(-sigma,wd,c=zeta_arr,cmap='viridis',s=20,zorder=5)
    ax.scatter(-sigma,-wd,c=zeta_arr,cmap='viridis',s=20,zorder=5)
    ax.axvline(0,color='k',lw=1); ax.axhline(0,color='k',lw=1)
    plt.colorbar(sc,ax=ax,label='ζ')
    ax.set_xlabel('Re(s)'); ax.set_ylabel('Im(s)'); ax.set_title(f'Polos 2° orden (ωn={wn})'); ax.grid(True,alpha=0.3)
    z_arr=np.linspace(0.1,1.2,100)
    Mp=np.where(z_arr<1,np.exp(-np.pi*z_arr/np.sqrt(np.maximum(1-z_arr**2,1e-6)))*100,0)
    ts=4/(z_arr*wn)*1000
    ax=axes[0,1]; ax2=ax.twinx()
    ax.plot(z_arr,Mp,'r-',lw=2,label='Mp (%)'); ax2.plot(z_arr,ts,'b-',lw=2,label='ts (ms)')
    ax.axvline(0.707,color='gray',ls='--',label='ζ=0.707')
    ax.set_xlabel('ζ'); ax.set_ylabel('Mp (%)',color='r'); ax2.set_ylabel('ts (ms)',color='b')
    ax.set_title('Mp y ts vs ζ'); ax.legend(fontsize=8); ax.grid(True,alpha=0.3)
    t=np.linspace(0,0.1,500)
    ax=axes[1,0]
    for zeta,col in [(0.2,'r'),(0.5,'orange'),(0.707,'g'),(1.0,'b')]:
        sys_tf=signal.lti([wn**2],[1,2*zeta*wn,wn**2]); _,y=signal.step(sys_tf,T=t)
        ax.plot(t*1000,y,color=col,lw=2,label=f'ζ={zeta}')
    ax.axhline(1,color='k',ls='--',alpha=0.5); ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Respuesta')
    ax.set_title('Escalón 2° orden'); ax.legend(fontsize=8); ax.grid(True,alpha=0.3)
    w2=np.logspace(1,4,500); wn3=500
    ax=axes[1,1]
    for zeta2,col in [(0.2,'r'),(0.5,'orange'),(0.707,'g')]:
        Tcl=wn3**2/(-w2**2+2j*zeta2*wn3*w2+wn3**2)
        ax.semilogx(w2/(2*np.pi),20*np.log10(np.abs(Tcl)),color=col,lw=2,label=f'ζ={zeta2}')
    ax.axhline(-3,color='k',ls='--',alpha=0.5,label='-3dB')
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('|T| (dB)'); ax.set_title('Pico resonancia lazo cerrado')
    ax.legend(fontsize=8); ax.grid(True,alpha=0.3)
    fig.suptitle('Sistema de 2° orden: polos, respuesta y resonancia',fontsize=14,fontweight='bold')
    plt.tight_layout(); _savefig(fig,"frecuencias-segundo-orden-analisis")


# ===================================================================== #
#  modelado-sistemas-analisis
# ===================================================================== #
def _modelado_sistemas_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    ax=axes[0,0]; ax.axis('off')
    steps=['Sistema\nReal','Primeros\nPrincipios','Modelo\nMatemático','Linealización','Diseño\nControl','Validación']
    xp=[0.1,0.25,0.45,0.45,0.7,0.9]; yp=[0.5,0.5,0.75,0.25,0.5,0.5]
    for x,y,s in zip(xp,yp,steps):
        ax.add_patch(mpatches.FancyBboxPatch((x-0.08,y-0.1),0.16,0.2,boxstyle='round,pad=0.02',facecolor='lightblue',edgecolor='blue'))
        ax.text(x,y,s,ha='center',va='center',fontsize=8,fontweight='bold')
    for i,j in [(0,1),(1,2),(1,3),(2,4),(3,4),(4,5)]:
        ax.annotate('',xy=(xp[j],yp[j]),xytext=(xp[i],yp[i]),arrowprops=dict(arrowstyle='->',color='navy',lw=1.5))
    ax.set_xlim([0,1]); ax.set_ylim([0.05,0.95]); ax.set_title('Ciclo de modelado')
    ax=axes[0,1]; Ts=1; D=0.6
    t_sw=np.linspace(0,5*Ts,5000); iL_sw=np.zeros(len(t_sw)); iL_avg=50*np.ones(len(t_sw))
    for k in range(5):
        t1=k*Ts; t2=t1+D*Ts; t3=(k+1)*Ts
        i1s=np.where((t_sw>=t1)&(t_sw<t2))[0]; i2s=np.where((t_sw>=t2)&(t_sw<t3))[0]
        if len(i1s): iL_sw[i1s]=np.linspace(45,55,len(i1s))
        if len(i2s): iL_sw[i2s]=np.linspace(55,45,len(i2s))
    ax.plot(t_sw,iL_sw,'b-',lw=0.8,alpha=0.7,label='Conmutada'); ax.plot(t_sw,iL_avg,'r-',lw=2,label='Promediada')
    ax.set_xlabel('t (Ts)'); ax.set_ylabel('$i_L$ (A)'); ax.set_title('Señal conmutada vs promediada')
    ax.legend(); ax.grid(True,alpha=0.3)
    ax=axes[1,0]; t_v=np.linspace(0,0.5,500)
    np.random.seed(7)
    y_mod=1-np.exp(-t_v/0.1)*(np.cos(20*t_v)+0.5*np.sin(20*t_v))
    y_meas=y_mod+0.03*np.random.randn(len(t_v))
    ax.plot(t_v*1000,y_mod,'b-',lw=2,label='Modelo'); ax.plot(t_v*1000,y_meas,'r.',markersize=2,alpha=0.6,label='Medida')
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Respuesta (pu)'); ax.set_title('Validación: modelo vs medida')
    ax.legend(); ax.grid(True,alpha=0.3)
    ax=axes[1,1]
    comp=[1,2,4,8,15,25]; acc_tr=[0.5,0.7,0.85,0.92,0.97,0.99]; acc_va=[0.48,0.68,0.84,0.89,0.82,0.65]
    ax.plot(comp,acc_tr,'b-o',lw=2,label='Entrenamiento'); ax.plot(comp,acc_va,'r-o',lw=2,label='Validación')
    ax.axvline(4,color='gray',ls='--',label='Óptimo'); ax.set_xlabel('Orden del modelo'); ax.set_ylabel('R²')
    ax.set_title('Complejidad vs generalización'); ax.legend(); ax.grid(True,alpha=0.3)
    fig.suptitle('Modelado: ciclo, promediado y validación',fontsize=14,fontweight='bold')
    plt.tight_layout(); _savefig(fig,"modelado-sistemas-analisis")


# ===================================================================== #
#  carga-pulsante-datacenter-analisis
# ===================================================================== #
def _carga_pulsante_datacenter_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    t=np.linspace(0,0.1,1000)
    P_pulse=100+130*(((t>0.02)&(t<0.05))|((t>0.07)&(t<0.085))).astype(float)
    ax=axes[0,0]
    ax.plot(t*1000,P_pulse,'b-',lw=2); ax.fill_between(t*1000,100,P_pulse,alpha=0.2,color='blue')
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Potencia (kW)'); ax.set_title('Perfil potencia pulsante IA')
    ax.axhline(100,color='k',ls='--',alpha=0.5,label='P_base'); ax.legend(); ax.grid(True,alpha=0.3)
    t2=np.linspace(0,0.02,500); Vnom=380
    dV_sin=20*np.exp(-50*t2)*np.cos(2*np.pi*200*t2)
    dV_con=5*np.exp(-200*t2)*np.cos(2*np.pi*200*t2)
    ax=axes[0,1]
    ax.plot(t2*1000,Vnom+dV_sin,'r-',lw=2,label='Sin BESS'); ax.plot(t2*1000,Vnom+dV_con,'b-',lw=2,label='Con BESS')
    ax.axhline(Vnom,color='k',ls='--',alpha=0.5); ax.axhline(Vnom*0.95,color='gray',ls=':',label='±5%')
    ax.axhline(Vnom*1.05,color='gray',ls=':')
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('V_bus (V)'); ax.set_title('Tensión bus DC con/sin BESS')
    ax.legend(fontsize=8); ax.grid(True,alpha=0.3)
    f_arr=np.logspace(1,4,200)
    Z_source=0.1*(1+1j*f_arr/500)/((1+1j*f_arr/50))
    Z_cpl=np.abs(380**2/280e3)*np.ones(len(f_arr))
    ax=axes[1,0]
    ax.loglog(f_arr,np.abs(Z_source),'b-',lw=2,label='|Z_source|')
    ax.loglog(f_arr,Z_cpl,'r--',lw=2,label='|Z_CPL|=V²/P')
    ax.fill_between(f_arr,np.abs(Z_source),Z_cpl,where=np.abs(Z_source)>Z_cpl,alpha=0.2,color='red',label='Inestable')
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Impedancia (Ω)'); ax.set_title('Criterio Middlebrook')
    ax.legend(fontsize=8); ax.grid(True,alpha=0.3)
    dur=np.logspace(-3,-1,100)*1000
    ax=axes[1,1]
    for dP,col,lab in [(50,'b','ΔP=50kW'),(100,'r','ΔP=100kW'),(200,'g','ΔP=200kW')]:
        E=dP*dur/1000; ax.loglog(dur,E,color=col,lw=2,label=lab)
    ax.set_xlabel('Duración (ms)'); ax.set_ylabel('Energía BESS (kJ)'); ax.set_title('Dimensionado BESS vs duración')
    ax.legend(fontsize=8); ax.grid(True,alpha=0.3)
    fig.suptitle('Carga pulsante data center IA: bus DC, Middlebrook y BESS',fontsize=14,fontweight='bold')
    plt.tight_layout(); _savefig(fig,"carga-pulsante-datacenter-analisis")


# ===================================================================== #
#  convertidor-back-to-back-analisis
# ===================================================================== #
def _convertidor_back_to_back_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    ax=axes[0,0]; ax.axis('off')
    ax.text(0.5,0.85,'VSC2 (MSC)',ha='center',va='center',fontsize=11,
            bbox=dict(boxstyle='round',facecolor='lightblue'),transform=ax.transAxes)
    ax.text(0.5,0.5,'Bus DC',ha='center',va='center',fontsize=11,
            bbox=dict(boxstyle='round',facecolor='lightyellow'),transform=ax.transAxes)
    ax.text(0.5,0.15,'VSC1 (GSC)',ha='center',va='center',fontsize=11,
            bbox=dict(boxstyle='round',facecolor='lightgreen'),transform=ax.transAxes)
    ax.annotate('P_gen →',xy=(0.5,0.63),xytext=(0.5,0.72),ha='center',
                arrowprops=dict(arrowstyle='->',color='navy'),fontsize=9,transform=ax.transAxes)
    ax.annotate('→ P_red',xy=(0.5,0.37),xytext=(0.5,0.28),ha='center',
                arrowprops=dict(arrowstyle='->',color='navy'),fontsize=9,transform=ax.transAxes)
    ax.set_title('Esquema back-to-back')
    t=np.linspace(0,0.5,500); Vdc_nom=1100
    dVdc=50*np.exp(-20*t)*np.cos(30*t)
    ax=axes[0,1]
    ax.plot(t*1000,Vdc_nom+dVdc,'b-',lw=2,label='v_dc'); ax.axhline(Vdc_nom,color='k',ls='--',alpha=0.5,label='V_dc*')
    ax.axhline(Vdc_nom*1.05,color='r',ls=':',alpha=0.7); ax.axhline(Vdc_nom*0.95,color='r',ls=':',alpha=0.7)
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('V_dc (V)'); ax.set_title('Control bus DC: respuesta escalón')
    ax.legend(fontsize=8); ax.grid(True,alpha=0.3)
    carga=np.linspace(0,1,100)
    eff_vsc=0.97+0.01*np.sin(np.pi*carga)-0.005*carga**2
    eff_b2b=eff_vsc**2
    ax=axes[1,0]
    ax.plot(carga*100,eff_vsc*100,'b-',lw=2,label='Un VSC'); ax.plot(carga*100,eff_b2b*100,'r-',lw=2,label='Back-to-Back')
    ax.axhline(96,color='gray',ls='--',alpha=0.5); ax.set_xlabel('Carga (%)'); ax.set_ylabel('Eficiencia (%)')
    ax.set_title('Eficiencia vs nivel de carga'); ax.legend(); ax.grid(True,alpha=0.3); ax.set_ylim([90,100])
    t3=np.linspace(0,0.3,500)
    Pgsc=np.where(t3<0.1,1.0,np.where(t3<0.15,1.0*(1-(t3-0.1)/0.05),0.5))
    Pmsc=np.where(t3<0.1,1.0,np.where(t3<0.12,1.0*(1-(t3-0.1)/0.05),0.8))
    Vdc_frt=1+(Pgsc-Pmsc)*0.05
    ax=axes[1,1]
    ax.plot(t3*1000,Pgsc,'b-',lw=2,label='P_GSC'); ax.plot(t3*1000,Pmsc,'r-',lw=2,label='P_MSC')
    ax2=ax.twinx(); ax2.plot(t3*1000,Vdc_frt,'g--',lw=2,label='V_dc (pu)')
    ax.axvline(100,color='gray',ls=':'); ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Potencia (pu)')
    ax2.set_ylabel('V_dc (pu)',color='g'); ax.set_title('Potencias durante FRT')
    ax.legend(loc='upper left',fontsize=8); ax2.legend(loc='upper right',fontsize=8); ax.grid(True,alpha=0.3)
    fig.suptitle('Convertidor back-to-back: esquema, bus DC, eficiencia y FRT',fontsize=14,fontweight='bold')
    plt.tight_layout(); _savefig(fig,"convertidor-back-to-back-analisis")


# ===================================================================== #
#  metricas-desempeno-analisis
# ===================================================================== #
def _metricas_desempeno_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import signal
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    t=np.linspace(0,0.5,500); wn=50
    ax=axes[0,0]
    iae_v=[]; ise_v=[]; itae_v=[]
    for zeta,col in [(0.3,'r'),(0.5,'orange'),(0.707,'g'),(1.0,'b')]:
        sys_tf=signal.lti([wn**2],[1,2*zeta*wn,wn**2]); _,y=signal.step(sys_tf,T=t)
        e=1-y; dt=t[1]-t[0]
        iae_v.append(np.trapz(np.abs(e),t)); ise_v.append(np.trapz(e**2,t)); itae_v.append(np.trapz(t*np.abs(e),t))
        ax.plot(t*1000,y,color=col,lw=2,label=f'ζ={zeta}')
    ax.axhline(1,color='k',ls='--',alpha=0.5); ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('y(t)')
    ax.set_title('Escalón para distintos ζ'); ax.legend(fontsize=8); ax.grid(True,alpha=0.3)
    ax=axes[0,1]
    zetas=[0.3,0.5,0.707,1.0]; x_pos=np.arange(len(zetas)); wd=0.25
    ax.bar(x_pos-wd,np.array(iae_v)/max(iae_v),wd,label='IAE',color='red',alpha=0.7)
    ax.bar(x_pos,np.array(ise_v)/max(ise_v),wd,label='ISE',color='blue',alpha=0.7)
    ax.bar(x_pos+wd,np.array(itae_v)/max(itae_v),wd,label='ITAE',color='green',alpha=0.7)
    ax.set_xticks(x_pos); ax.set_xticklabels([f'ζ={z}' for z in zetas],fontsize=9)
    ax.set_ylabel('Métrica normalizada'); ax.set_title('IAE/ISE/ITAE por amortiguamiento')
    ax.legend(fontsize=8); ax.grid(True,alpha=0.3,axis='y')
    ax=axes[1,0]
    PM_arr=np.linspace(20,80,200)
    BW_arr=200*np.sin(np.radians(PM_arr))**0.5
    ax.plot(BW_arr,PM_arr,'b-',lw=2,label='Frontera Pareto')
    ax.fill_betweenx(PM_arr,0,BW_arr,alpha=0.1,color='blue')
    ax.axvline(100,color='r',ls='--',label='BW=100 rad/s'); ax.axhline(45,color='g',ls='--',label='PM=45°')
    ax.set_xlabel('Ancho de banda (rad/s)'); ax.set_ylabel('Margen de fase (°)')
    ax.set_title('Pareto: BW vs PM'); ax.legend(fontsize=8); ax.grid(True,alpha=0.3)
    carga=np.linspace(0.1,1,100)
    THD=5*np.exp(-3*carga)+1; FP=0.85+0.13*(1-np.exp(-5*carga))
    ax=axes[1,1]; ax2=ax.twinx()
    ax.plot(carga*100,THD,'r-',lw=2,label='THD (%)'); ax.axhline(5,color='r',ls='--',alpha=0.5,label='Límite 5%')
    ax2.plot(carga*100,FP,'b-',lw=2,label='FP'); ax2.axhline(0.95,color='b',ls='--',alpha=0.5)
    ax.set_xlabel('Carga (%)'); ax.set_ylabel('THD (%)',color='r'); ax2.set_ylabel('Factor de Potencia',color='b')
    ax.set_title('Calidad de potencia vs carga'); ax.legend(loc='upper right',fontsize=8); ax.grid(True,alpha=0.3)
    fig.suptitle('Métricas de desempeño: IAE/ISE/ITAE, Pareto y calidad',fontsize=14,fontweight='bold')
    plt.tight_layout(); _savefig(fig,"metricas-desempeno-analisis")


# ===================================================================== #
#  control-jerarquico-microrred-analisis
# ===================================================================== #
def _control_jerarquico_microrred_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    ax=axes[0,0]; ax.axis('off')
    niveles=['Nivel 3: EMS\n(min–h)', 'Nivel 2: Secundario\n(s)', 'Nivel 1: Primario\n(ms)', 'Hardware']
    colores=['#2196F3','#4CAF50','#FF9800','#9E9E9E']
    for i,(niv,col) in enumerate(zip(niveles,colores)):
        w=0.6-i*0.08; x=0.5-w/2; y=0.75-i*0.2
        ax.add_patch(plt.Rectangle((x,y),w,0.12,facecolor=col,alpha=0.7,edgecolor='black'))
        ax.text(0.5,y+0.06,niv,ha='center',va='center',fontsize=9,fontweight='bold',transform=ax.transAxes)
    ax.set_xlim([0,1]); ax.set_ylim([0,1]); ax.set_title('Pirámide de control jerárquico')
    P=np.linspace(0,1.2,100); f_droopA=50-2*P; f_droopB=50-3*P
    ax=axes[0,1]
    ax.plot(P,f_droopA,'b-',lw=2,label='Inversor A (mp=2)'); ax.plot(P,f_droopB,'r-',lw=2,label='Inversor B (mp=3)')
    ax.axhline(50,color='k',ls='--',alpha=0.5); ax.axhline(49,color='gray',ls=':',alpha=0.5)
    ax.set_xlabel('P (pu)'); ax.set_ylabel('f (Hz)'); ax.set_title('Droop P-f primario')
    ax.legend(); ax.grid(True,alpha=0.3); ax.set_ylim([47,51])
    t=np.linspace(0,20,500)
    f_prim=50-1*(t>2).astype(float)*np.exp(-0.5*(t-2))*(t>2).astype(float)
    f_sec=np.where(t<2,50,50-(1-1/(1+np.exp(-2*(t-5))))*1)
    ax=axes[1,0]
    ax.plot(t,f_prim,'r-',lw=2,label='Solo primario'); ax.plot(t,f_sec,'b-',lw=2,label='Con secundario')
    ax.axhline(50,color='k',ls='--',alpha=0.5); ax.axvline(2,color='gray',ls=':',alpha=0.5)
    ax.set_xlabel('Tiempo (s)'); ax.set_ylabel('Frecuencia (Hz)'); ax.set_title('Restauración secundaria de f')
    ax.legend(); ax.grid(True,alpha=0.3)
    horas=np.linspace(0,24,500)
    P_solar=np.maximum(0,0.8*np.sin(np.pi*(horas-6)/12)**2*(horas>6)*(horas<20))
    P_demanda=0.4+0.3*np.sin(2*np.pi*horas/24+np.pi)+0.2*np.sin(2*np.pi*horas/12)
    P_demanda=np.clip(P_demanda,0.2,1.0)
    SOC=0.5+np.cumsum(P_solar-P_demanda)*(24/500)*0.05
    SOC=np.clip(SOC,0.2,0.9)
    ax=axes[1,1]
    ax.plot(horas,P_solar,'y-',lw=2,label='P solar'); ax.plot(horas,P_demanda,'r-',lw=2,label='P demanda')
    ax2=ax.twinx(); ax2.plot(horas,SOC,'b--',lw=2,label='SOC BESS')
    ax.set_xlabel('Hora del día'); ax.set_ylabel('Potencia (pu)'); ax2.set_ylabel('SOC',color='b')
    ax.set_title('Despacho terciario 24 h'); ax.legend(loc='upper left',fontsize=8); ax2.legend(loc='upper right',fontsize=8)
    ax.grid(True,alpha=0.3)
    fig.suptitle('Control jerárquico microrred: primario, secundario y terciario',fontsize=14,fontweight='bold')
    plt.tight_layout(); _savefig(fig,"control-jerarquico-microrred-analisis")


# ===================================================================== #
#  servicios-red-soporte-analisis
# ===================================================================== #
def _servicios_red_soporte_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    t=np.linspace(0,30,1000)
    df_inertia=-0.3*np.exp(-t/0.5)*(t<1)
    df_ffr=-0.3*(1-np.exp(-t/0.3))*(t<10)*np.exp(-t/5)
    df_fcr=-0.3+0.3*(1-np.exp(-t/5))
    df_total=df_inertia+df_ffr+df_fcr*0.5
    ax=axes[0,0]
    ax.plot(t,df_total,'k-',lw=2.5,label='Δf total')
    ax.fill_between(t,0,df_inertia,alpha=0.3,color='blue',label='Inercia sintética')
    ax.fill_between(t,df_inertia,df_inertia+df_ffr,alpha=0.3,color='green',label='FFR')
    ax.fill_between(t,df_inertia+df_ffr,df_total,alpha=0.3,color='orange',label='FCR')
    ax.axhline(0,color='k',ls='--',alpha=0.5); ax.set_xlabel('Tiempo (s)'); ax.set_ylabel('Δf (Hz)')
    ax.set_title('Respuesta de frecuencia por etapas'); ax.legend(fontsize=7); ax.grid(True,alpha=0.3)
    V=np.linspace(0.7,1.3,200)
    Q_kv=np.where(np.abs(V-1)<0.05,0,np.clip(-2*(V-1),-0.5,0.5))
    ax=axes[0,1]
    ax.plot(V,Q_kv,'b-',lw=2); ax.fill_between(V,0,Q_kv,alpha=0.2,color='blue')
    ax.axvline(0.95,color='gray',ls=':'); ax.axvline(1.05,color='gray',ls=':',label='Dead band ±5%')
    ax.axhline(0,color='k',ls='--',alpha=0.5); ax.set_xlabel('V (pu)'); ax.set_ylabel('Q (pu)')
    ax.set_title('Curva Q(V): droop de tensión'); ax.legend(); ax.grid(True,alpha=0.3)
    theta=np.linspace(0,2*np.pi,200); Imax=1.0
    ax=axes[1,0]
    ax.plot(np.cos(theta)*Imax,np.sin(theta)*Imax,'k-',lw=1.5,alpha=0.5,label='Límite I_max')
    for P0,col in [(0.8,'b'),(0.5,'r'),(0.2,'g')]:
        Q_max=np.sqrt(max(Imax**2-P0**2,0))
        ax.plot([P0,P0],[-Q_max,Q_max],color=col,lw=2,label=f'P={P0}pu')
    ax.set_xlabel('P (pu)'); ax.set_ylabel('Q (pu)'); ax.set_title('Diagrama P-Q inversor')
    ax.legend(fontsize=8); ax.grid(True,alpha=0.3); ax.set_aspect('equal')
    servicios=['FCR','aFRR','mFRR']
    precios_min=[10,30,5]; precios_max=[50,120,25]
    x_pos=np.arange(len(servicios))
    ax=axes[1,1]
    ax.bar(x_pos,precios_max,color=['blue','orange','green'],alpha=0.5,label='Precio max')
    ax.bar(x_pos,precios_min,color=['blue','orange','green'],alpha=0.9,label='Precio min')
    ax.set_xticks(x_pos); ax.set_xticklabels(servicios,fontsize=11)
    ax.set_ylabel('Precio (€/MW/h)'); ax.set_title('Precios FCR/aFRR/mFRR (Europa)')
    ax.legend(); ax.grid(True,alpha=0.3,axis='y')
    fig.suptitle('Servicios de red: frecuencia, Q(V), P-Q y precios',fontsize=14,fontweight='bold')
    plt.tight_layout(); _savefig(fig,"servicios-red-soporte-analisis")


def _valcruz_analisis():
    """4 paneles: k-fold visual, curva de aprendizaje, FIT% vs orden, prediccion vs real."""
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    np.random.seed(42)

    # Panel 1: k-fold visual
    ax = axes[0, 0]; ax.axis('off')
    k = 5; N = 20
    for fold in range(k):
        for i in range(N):
            color = BAD if i // 4 == fold else ACC
            ax.add_patch(plt.Rectangle((i * 0.045 + 0.05, 0.85 - fold * 0.15),
                                        0.04, 0.1, color=color, alpha=0.7))
        ax.text(0.02, 0.9 - fold * 0.15, f'Fold {fold+1}', va='center', fontsize=9)
    ax.text(0.5, 0.02, 'Azul=entrenamiento, Rojo=validacion', ha='center', fontsize=9,
            transform=ax.transAxes)
    ax.set_xlim([0, 1]); ax.set_ylim([0, 1])
    ax.set_title('Validacion cruzada k-fold (k=5)', fontsize=10)

    # Panel 2: curva de aprendizaje
    ax = axes[0, 1]
    n_s = np.arange(10, 200, 10)
    err_train = 0.05 + 0.3 * np.exp(-n_s / 30) + 0.01 * np.random.randn(len(n_s))
    err_val = 0.25 - 0.1 * (1 - np.exp(-n_s / 50)) + 0.02 * np.random.randn(len(n_s))
    ax.plot(n_s, np.abs(err_train), color=ACC, lw=2, marker='o', markersize=4,
            label='Entrenamiento')
    ax.plot(n_s, np.abs(err_val), color=BAD, lw=2, marker='o', markersize=4,
            label='Validacion')
    ax.set_xlabel('Muestras de entrenamiento'); ax.set_ylabel('NRMSE')
    ax.set_title('Curva de aprendizaje'); ax.legend(fontsize=9); ax.grid(True, alpha=0.4)

    # Panel 3: FIT% vs orden del modelo
    ax = axes[1, 0]
    orders = np.arange(1, 9)
    fit_train = [55, 72, 85, 92, 97, 99, 99.5, 99.8]
    fit_val = [53, 70, 83, 89, 82, 71, 60, 45]
    ax.plot(orders, fit_train, color=ACC, lw=2, marker='o', label='Entrenamiento')
    ax.plot(orders, fit_val, color=BAD, lw=2, marker='o', label='Validacion')
    ax.axhline(80, color='#888', ls='--', lw=1.5, label='Umbral 80%')
    ax.axvline(4, color=OK, ls=':', lw=1.5, label='Orden optimo')
    ax.set_xlabel('Orden del modelo'); ax.set_ylabel('FIT (%)')
    ax.set_title('FIT% vs orden del modelo')
    ax.legend(fontsize=8); ax.grid(True, alpha=0.4)

    # Panel 4: prediccion vs medida
    ax = axes[1, 1]
    t = np.linspace(0, 2, 200)
    y_true = np.sin(2 * np.pi * t) + 0.3 * np.sin(2 * np.pi * 3 * t)
    y_good = y_true + 0.05 * np.random.randn(len(t))
    ax.plot(t, y_true, 'k-', lw=2, label='Real')
    ax.plot(t, y_good, color=ACC, lw=1.5, ls='--', label='Modelo valido (FIT=88%)')
    ax.set_xlabel('Tiempo (s)'); ax.set_ylabel('Salida')
    ax.set_title('Prediccion vs real')
    ax.legend(fontsize=8); ax.grid(True, alpha=0.4)

    fig.suptitle('Validacion cruzada: k-fold, curva de aprendizaje y FIT%',
                 fontsize=13, fontweight='bold')
    fig.tight_layout()
    _savefig(fig, "validacion-cruzada-analisis.png")


def _nivval_analisis():
    """4 paneles: piramide V, coste vs cobertura, retardo HiL, deteccion de errores."""
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Panel 1: piramide de validacion
    ax = axes[0, 0]; ax.axis('off')
    levels = [('Campo (real)', 0.83, 0.10, '#FF6666'),
              ('Prototipo a escala', 0.68, 0.12, '#FF9966'),
              ('PHiL', 0.52, 0.14, '#FFCC66'),
              ('HiL (DSP+FPGA)', 0.34, 0.16, '#99FF99'),
              ('SiL (PC)', 0.14, 0.18, '#66CCFF')]
    for label, y, h, col in levels:
        w = 0.28 + h * 2
        ax.add_patch(mpatches.FancyBboxPatch((0.5 - w/2, y - h/2), w, h,
                                              boxstyle='round,pad=0.01',
                                              facecolor=col, edgecolor='#555'))
        ax.text(0.5, y, label, ha='center', va='center', fontsize=9, fontweight='bold')
    ax.set_xlim([0, 1]); ax.set_ylim([0, 1])
    ax.set_title('Piramide de validacion (modelo V)', fontsize=10)

    # Panel 2: coste vs cobertura
    ax = axes[0, 1]
    niveles = ['SiL', 'HiL', 'PHiL', 'Prototipo', 'Campo']
    coste = [1, 5, 50, 200, 1000]
    cobertura = [95, 85, 70, 60, 40]
    x = np.arange(len(niveles))
    ax2 = ax.twinx()
    ax.bar(x, coste, alpha=0.6, color=BAD, label='Coste relativo')
    ax2.plot(x, cobertura, color=ACC, lw=2, marker='o', label='Cobertura (%)')
    ax.set_xticks(x); ax.set_xticklabels(niveles)
    ax.set_ylabel('Coste relativo', color=BAD); ax2.set_ylabel('Cobertura (%)', color=ACC)
    ax.set_title('Coste vs cobertura por nivel', fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    lines1, labs1 = ax.get_legend_handles_labels()
    lines2, labs2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labs1 + labs2, fontsize=8, loc='upper left')

    # Panel 3: efecto del retardo HiL en margen de fase
    ax = axes[1, 0]
    fc_range = np.linspace(100, 2000, 200)
    for Td, col, lbl in [(50e-6, OK, 'Td=50us'), (100e-6, ACC2, 'Td=100us'),
                         (200e-6, BAD, 'Td=200us')]:
        pm_loss = Td * 2 * np.pi * fc_range * 180 / np.pi
        ax.plot(fc_range, pm_loss, color=col, lw=2, label=lbl)
    ax.axhline(45, color='#888', ls='--', lw=1.5, label='PM minimo 45deg')
    ax.set_xlabel('Frecuencia de cruce fc (Hz)')
    ax.set_ylabel('Perdida de PM (deg)')
    ax.set_title('Perdida de margen de fase por retardo HIL', fontsize=10)
    ax.legend(fontsize=8); ax.grid(True, alpha=0.4)

    # Panel 4: errores detectados vs coste de correccion
    ax = axes[1, 1]
    fases = ['SiL', 'HiL', 'PHiL', 'Prototipo', 'Campo']
    errores = [40, 25, 20, 10, 5]
    coste_c = [1, 3, 15, 80, 500]
    x2 = np.arange(len(fases))
    ax3 = ax.twinx()
    ax.bar(x2, errores, alpha=0.6, color=ACC, label='Errores detectados (%)')
    ax3.plot(x2, coste_c, color=BAD, lw=2, marker='o', label='Coste correccion')
    ax.set_xticks(x2); ax.set_xticklabels(fases)
    ax.set_ylabel('Errores detectados (%)', color=ACC)
    ax3.set_ylabel('Coste relativo de correccion', color=BAD)
    ax.set_title('Deteccion de errores y coste de correccion', fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    lines1, labs1 = ax.get_legend_handles_labels()
    lines2, labs2 = ax3.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labs1 + labs2, fontsize=8, loc='upper right')

    fig.suptitle('Niveles de validacion: SiL, HiL, PHiL y campo',
                 fontsize=13, fontweight='bold')
    fig.tight_layout()
    _savefig(fig, "niveles-validacion-analisis.png")


def _cicdis_analisis():
    """4 paneles: diagrama ciclo iterativo, Monte Carlo PM, compromiso specs, checklist."""
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Panel 1: ciclo de diseno esquematico
    ax = axes[0, 0]; ax.axis('off')
    etapas = ['Especificar\n(requisitos)', 'Disenar\n(controlador)', 'Evaluar\n(margenes)',
              'Validar\n(niveles)']
    colores = [ACC, ACC2, OK, BAD]
    for i, (et, col) in enumerate(zip(etapas, colores)):
        theta = np.pi / 2 - i * np.pi / 2
        x_c = 0.5 + 0.32 * np.cos(theta); y_c = 0.5 + 0.32 * np.sin(theta)
        ax.add_patch(plt.Circle((x_c, y_c), 0.12, color=col, alpha=0.85))
        ax.text(x_c, y_c, et, ha='center', va='center', fontsize=8, fontweight='bold')
    # flechas del ciclo
    for i in range(4):
        t0 = np.pi / 2 - i * np.pi / 2; t1 = np.pi / 2 - (i + 1) * np.pi / 2
        x0 = 0.5 + 0.32 * np.cos(t0); y0 = 0.5 + 0.32 * np.sin(t0)
        x1 = 0.5 + 0.32 * np.cos(t1); y1 = 0.5 + 0.32 * np.sin(t1)
        ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle='->', color='#555', lw=1.5))
    ax.text(0.5, 0.5, 'Trazabilidad', ha='center', va='center', fontsize=9, color='#444')
    ax.set_xlim([0, 1]); ax.set_ylim([0, 1])
    ax.set_title('Ciclo de diseno iterativo (DEV)', fontsize=10)

    # Panel 2: Monte Carlo de margen de fase
    ax = axes[0, 1]
    np.random.seed(7)
    N_mc = 500
    L1_n, L2_n, Cf_n = 2e-3, 1e-3, 20e-6
    L1s = L1_n * (1 + 0.3 * (np.random.rand(N_mc) - 0.5) * 2)
    L2s = L2_n * (1 + 0.3 * (np.random.rand(N_mc) - 0.5) * 2)
    Cfs = Cf_n * (1 + 0.2 * (np.random.rand(N_mc) - 0.5) * 2)
    wc = 2 * np.pi * 500
    Td = 100e-6
    # PM simplificado: PM = 90 - arctan(wc*(L1+L2)) - wc*Td*180/pi
    pm = 90 - np.degrees(np.arctan(wc * (L1s + L2s))) - wc * Td * 180 / np.pi
    ax.hist(pm, bins=30, color=ACC, alpha=0.75, edgecolor='white')
    ax.axvline(45, color=BAD, ls='--', lw=2, label='PM minimo 45deg')
    ax.axvline(pm.mean(), color=ACC2, ls='-', lw=2, label=f'Media {pm.mean():.1f}deg')
    ax.set_xlabel('Margen de fase (deg)'); ax.set_ylabel('Frecuencia')
    ax.set_title(f'Monte Carlo PM (N={N_mc}, L±30%, C±20%)', fontsize=10)
    ax.legend(fontsize=8); ax.grid(True, alpha=0.4)

    # Panel 3: compromiso rapidez vs margen de fase
    ax = axes[1, 0]
    fc_vals = np.linspace(100, 2000, 200)
    pm_nom = 72 - fc_vals * 2 * np.pi * Td * 180 / np.pi
    pm_nom = np.clip(pm_nom, 0, 90)
    ts_vals = 4 / (0.6 * 2 * np.pi * fc_vals / 3)  # ts aprox = 4/(zeta*wn), wn~wc/3
    ax.plot(ts_vals * 1000, pm_nom, color=ACC, lw=2.5)
    ax.axhline(45, color=BAD, ls='--', lw=1.5, label='PM min 45deg')
    ax.axvline(2, color=ACC2, ls=':', lw=1.5, label='ts max 2ms')
    ax.fill_between(ts_vals * 1000, pm_nom, 45,
                    where=(pm_nom >= 45) & (ts_vals * 1000 <= 2),
                    alpha=0.2, color=OK, label='Zona valida')
    ax.set_xlabel('Tiempo de establecimiento ts (ms)')
    ax.set_ylabel('Margen de fase PM (deg)')
    ax.set_title('Compromiso rapidez vs robustez', fontsize=10)
    ax.legend(fontsize=8); ax.grid(True, alpha=0.4)
    ax.set_xlim([0, 8]); ax.set_ylim([0, 80])

    # Panel 4: checklist de documentacion
    ax = axes[1, 1]; ax.axis('off')
    items = [
        ('OK', 'Tabla de especificaciones con origen'),
        ('OK', 'Diagrama de bloques del control'),
        ('OK', 'Bode: PM, GM, wc marcados'),
        ('OK', 'Escalon: Mp, ts medidos'),
        ('OK', 'Monte Carlo: % realizaciones OK'),
        ('--', 'Informe final con trazabilidad'),
        ('--', 'Revision de seguridad (corriente pico)'),
    ]
    for i, (estado, texto) in enumerate(items):
        col = OK if estado == 'OK' else ACC2
        sym = u'✓' if estado == 'OK' else u'–'
        ax.text(0.05, 0.92 - i * 0.12, f'{sym}  {texto}',
                fontsize=10, color=col, va='top')
    ax.set_title('Checklist de documentacion del ciclo', fontsize=10)
    ax.set_xlim([0, 1]); ax.set_ylim([0, 1])

    fig.suptitle('Ciclo de diseno: iterativo, Monte Carlo, compromiso specs y checklist',
                 fontsize=12, fontweight='bold')
    fig.tight_layout()
    _savefig(fig, "ciclo-diseno-control-analisis.png")


def _espctrl_analisis():
    """4 paneles: escalon con specs, Bode con PM/GM, THD limite, tabla de specs."""
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import signal
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Panel 1: respuesta escalon con Mp y ts marcados
    ax = axes[0, 0]
    zeta, wn = 0.6, 2 * np.pi * 500
    sys2 = signal.TransferFunction([wn**2], [1, 2*zeta*wn, wn**2])
    t = np.linspace(0, 0.005, 500)
    _, y = signal.step(sys2, T=t)
    Mp = np.exp(-np.pi * zeta / np.sqrt(1 - zeta**2))
    ts_idx = np.where(np.abs(y - 1) > 0.02)[0]
    ts_val = t[ts_idx[-1]] if len(ts_idx) > 0 else t[-1]
    ax.plot(t * 1000, y, color=ACC, lw=2.5, label=f'zeta={zeta}')
    ax.axhline(1, color='#888', ls=':', lw=1.2)
    ax.axhline(1 + Mp, color=BAD, ls='--', lw=1.5, label=f'Mp={Mp*100:.1f}%')
    ax.axhline(1.02, color='#aaa', ls=':', lw=1)
    ax.axhline(0.98, color='#aaa', ls=':', lw=1)
    ax.axvline(ts_val * 1000, color=ACC2, ls='--', lw=1.5,
               label=f'ts={ts_val*1000:.1f}ms')
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Respuesta normalizada')
    ax.set_title('Escalon: Mp y ts', fontsize=10)
    ax.legend(fontsize=8); ax.grid(True, alpha=0.4)

    # Panel 2: Bode con PM y GM
    ax = axes[0, 1]
    Kp, Ki = 2.0, 1000.0
    L, R = 2e-3, 0.1
    # lazo abierto: PI * (1/(Ls+R))
    num_pi = [Kp, Ki]; den_pi = [1, 0]
    num_p = [1]; den_p = [L, R]
    from numpy.polynomial import polynomial as P
    num_ol = np.convolve(num_pi, num_p)
    den_ol = np.convolve(den_pi, den_p)
    sys_ol = signal.TransferFunction(num_ol, den_ol)
    f = np.logspace(1, 4.5, 500); w = 2 * np.pi * f
    _, mag, phase = signal.bode(sys_ol, w)
    # find PM and GM
    idx_c = np.argmin(np.abs(mag))  # cruce de ganancia 0 dB
    pm_val = 180 + phase[idx_c]
    idx_ph = np.argmin(np.abs(phase + 180))
    gm_val = -mag[idx_ph]
    ax.semilogx(f, mag, color=ACC, lw=2, label='Bode lazo abierto')
    ax.axhline(0, color='#888', ls=':', lw=1)
    ax.axvline(f[idx_c], color=BAD, ls='--', lw=1.5,
               label=f'PM={pm_val:.0f}deg @ {f[idx_c]:.0f}Hz')
    ax.axvline(f[idx_ph], color=ACC2, ls='--', lw=1.5,
               label=f'GM={gm_val:.1f}dB @ {f[idx_ph]:.0f}Hz')
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Magnitud (dB)')
    ax.set_title('Bode: PM y GM', fontsize=10)
    ax.legend(fontsize=7); ax.grid(True, alpha=0.4); ax.set_ylim(-60, 60)

    # Panel 3: THD con limites IEEE 519
    ax = axes[1, 0]
    harmonics = np.arange(1, 26)
    # perfil tipico VSC con filtro LCL
    amps = np.zeros(25)
    amps[0] = 100  # fundamental
    amps[4] = 3.8  # 5th
    amps[6] = 2.5  # 7th
    amps[10] = 1.0  # 11th
    amps[12] = 0.7  # 13th
    amps[16] = 0.4  # 17th
    amps[18] = 0.3  # 19th
    # limites IEEE 519 (SCR<20)
    lim = np.ones(25) * 2  # por defecto
    lim[:10] = 4; lim[10:16] = 2; lim[16:22] = 1.5; lim[22:] = 0.6
    lim[0] = 0  # no aplica a fundamental
    colors_bar = [BAD if (a > l and h > 1) else ACC
                  for h, a, l in zip(harmonics, amps, lim)]
    ax.bar(harmonics[1:], amps[1:], color=colors_bar[1:], alpha=0.8, label='Medido')
    ax.step(harmonics[1:], lim[1:], color=ACC2, lw=2, where='mid', label='Limite IEEE 519')
    ax.set_xlabel('Orden armonico'); ax.set_ylabel('% de fundamental')
    ax.set_title('THD: armonicos vs limite IEEE 519', fontsize=10)
    ax.legend(fontsize=8); ax.grid(True, alpha=0.4)

    # Panel 4: tabla de especificaciones
    ax = axes[1, 1]; ax.axis('off')
    tabla = [
        ['Requisito', 'Metrica', 'Objetivo'],
        ['Rapidez corriente', 'fc (Hz)', '500'],
        ['Robustez', 'PM (deg)', '>= 45'],
        ['Precision', 'ess escalon', '0 (PI)'],
        ['Compat. PWM', 'fc/fsw', '<= 1/10'],
        ['THD corriente', 'THD_I (%)', '< 5'],
        ['Sobreimpulso', 'Mp (%)', '< 10'],
        ['Tiempo establec.', 'ts (ms)', '< 2'],
    ]
    col_widths = [0.42, 0.3, 0.18]
    row_h = 0.10
    for r, row in enumerate(tabla):
        y_pos = 0.95 - r * row_h
        bg = '#e8f0fe' if r == 0 else ('#f5f5f5' if r % 2 == 0 else 'white')
        ax.add_patch(plt.Rectangle((0, y_pos - row_h * 0.9), 1, row_h * 0.9,
                                    facecolor=bg, edgecolor='#ccc'))
        x_pos = 0.01
        for col_txt, cw in zip(row, col_widths):
            fw = 'bold' if r == 0 else 'normal'
            ax.text(x_pos, y_pos - row_h * 0.4, col_txt, fontsize=8.5,
                    va='center', fontweight=fw)
            x_pos += cw
    ax.set_xlim([0, 1]); ax.set_ylim([0, 1])
    ax.set_title('Tabla de especificaciones (GFL 100 kW)', fontsize=10)

    fig.suptitle('Especificaciones de control: tiempo, frecuencia, calidad de potencia',
                 fontsize=12, fontweight='bold')
    fig.tight_layout()
    _savefig(fig, "especificaciones-control-analisis.png")


def _prueba_analisis():
    """4 paneles: escalon corriente, LVRT, THD antes/despues, timeline de pruebas."""
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    np.random.seed(13)

    # Panel 1: respuesta escalon lazo de corriente
    ax = axes[0, 0]
    t = np.linspace(0, 0.004, 400)
    zeta, wn = 0.62, 2 * np.pi * 500
    from scipy import signal
    sys2 = signal.TransferFunction([wn**2], [1, 2*zeta*wn, wn**2])
    _, y = signal.step(sys2, T=t)
    y = y * 1.0  # 1 pu
    Mp_val = y.max() - 1
    ax.plot(t * 1000, y, color=ACC, lw=2.5, label='id(t)')
    ax.axhline(1.0, color='#888', ls=':', lw=1.2, label='Referencia')
    ax.axhline(1 + Mp_val, color=BAD, ls='--', lw=1.5,
               label=f'Mp={Mp_val*100:.1f}%')
    ax.axhline(1.02, color='#ccc', ls=':', lw=1)
    ax.axhline(0.98, color='#ccc', ls=':', lw=1)
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Corriente (p.u.)')
    ax.set_title('Escalon lazo de corriente (id)', fontsize=10)
    ax.legend(fontsize=8); ax.grid(True, alpha=0.4)
    ax.set_ylim([0, 1.15])

    # Panel 2: LVRT — tension y corriente
    ax = axes[0, 1]
    t2 = np.linspace(0, 0.5, 1000)
    v_pcc = np.ones_like(t2)
    v_pcc[(t2 >= 0.1) & (t2 < 0.2)] = 0.3  # hueco al 30%
    i_pcc = np.ones_like(t2)
    i_pcc[(t2 >= 0.1) & (t2 < 0.2)] = np.minimum(
        1.5, 1 + 2 * (1 - 0.3))  # inyeccion reactiva
    i_pcc = np.clip(i_pcc, 0, 1.5)
    ax.plot(t2 * 1000, v_pcc, color=ACC, lw=2, label='V_PCC (p.u.)')
    ax.plot(t2 * 1000, i_pcc, color=BAD, lw=2, ls='--', label='I_PCC (p.u.)')
    ax.axhline(1.5, color='#888', ls=':', lw=1.2, label='Limite 1.5 p.u.')
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('p.u.')
    ax.set_title('LVRT: hueco al 30% durante 100ms', fontsize=10)
    ax.legend(fontsize=8); ax.grid(True, alpha=0.4)

    # Panel 3: THD antes y despues del control
    ax = axes[1, 0]
    harmonics = np.arange(2, 21)
    amp_antes = [0, 5.2, 0, 3.5, 0, 1.8, 0, 1.2, 0,
                 0.8, 0, 0.5, 0, 0.3, 0, 0.2, 0, 0.1, 0]
    amp_despues = [0, 0.4, 0, 0.3, 0, 1.6, 0, 1.0, 0,
                   0.6, 0, 0.4, 0, 0.3, 0, 0.2, 0, 0.1, 0]
    x = np.arange(len(harmonics))
    ax.bar(x - 0.2, amp_antes, width=0.35, color=BAD, alpha=0.7,
           label='Sin control armonico')
    ax.bar(x + 0.2, amp_despues, width=0.35, color=ACC, alpha=0.8,
           label='Con control resonante')
    ax.axhline(4.0, color=ACC2, ls='--', lw=1.5, label='Limite indiv. 4%')
    ax.set_xticks(x); ax.set_xticklabels([str(h) for h in harmonics], fontsize=8)
    ax.set_xlabel('Orden armonico'); ax.set_ylabel('% de fundamental')
    ax.set_title('THD: antes y despues del control resonante', fontsize=10)
    ax.legend(fontsize=7); ax.grid(True, alpha=0.4)

    # Panel 4: timeline del plan de pruebas
    ax = axes[1, 1]; ax.axis('off')
    fases = [
        (0.05, 0.95, ACC, 'SiL: escalon, LVRT, Monte Carlo\nCriterio: FIT%>80%, Mp<10%'),
        (0.05, 0.72, ACC2, 'HiL: firmware, protecciones, escalon\nCriterio: PM>45deg, ts<2ms'),
        (0.05, 0.49, OK, 'PHiL: LVRT real, THD en PCC\nCriterio: THD<5%, pico<1.5pu'),
        (0.05, 0.26, BAD, 'Campo: grid codes, certificacion\nCriterio: todos los estandares'),
    ]
    import matplotlib.patches as _mp2
    for x_pos, y_pos, col, txt in fases:
        ax.add_patch(_mp2.FancyBboxPatch((x_pos, y_pos - 0.17), 0.90, 0.18,
                                          boxstyle='round,pad=0.01',
                                          facecolor=col, alpha=0.25, edgecolor=col))
        ax.text(x_pos + 0.05, y_pos - 0.08, txt, fontsize=8.5, va='center', color='#222')
    ax.set_xlim([0, 1]); ax.set_ylim([0, 1.05])
    ax.set_title('Plan de pruebas: de SiL a campo', fontsize=10)

    fig.suptitle('Pruebas de validacion: escalon, LVRT, THD y plan de pruebas',
                 fontsize=12, fontweight='bold')
    fig.tight_layout()
    _savefig(fig, "pruebas-validacion-analisis.png")


def _calpot_analisis():
    """4 paneles: THD vs limite IEEE519, flicker Pst, desequilibrio vectorial, rizado DC."""
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Panel 1: espectro de corriente vs limites IEEE 519
    ax = axes[0, 0]
    h_orders = np.arange(2, 26)
    # amplitudes tipicas VSC 2 niveles con LCL
    amps = {2: 0.5, 3: 0.3, 4: 0.4, 5: 3.8, 6: 0.2, 7: 2.5, 8: 0.1,
            9: 0.4, 10: 0.1, 11: 1.0, 12: 0.1, 13: 0.7, 14: 0.1,
            15: 0.3, 16: 0.1, 17: 0.4, 18: 0.1, 19: 0.3, 20: 0.1,
            21: 0.2, 22: 0.1, 23: 0.2, 24: 0.1, 25: 0.2}
    lims = {h: (4 if h < 11 else 2 if h < 17 else 1.5 if h < 23 else 0.6)
            for h in h_orders}
    amp_vals = [amps.get(h, 0.1) for h in h_orders]
    lim_vals = [lims[h] for h in h_orders]
    cols = [BAD if a > l else ACC for a, l in zip(amp_vals, lim_vals)]
    ax.bar(h_orders, amp_vals, color=cols, alpha=0.8, label='Medido')
    ax.step(h_orders, lim_vals, color=ACC2, lw=2.0, where='mid', label='Limite IEEE 519')
    ax.set_xlabel('Orden armonico'); ax.set_ylabel('Ih / I1 (%)')
    thd = np.sqrt(sum(a**2 for a in amp_vals)) / 100 * 100
    ax.set_title(f'Espectro de corriente: THD={thd:.1f}% vs limite 5%', fontsize=10)
    ax.legend(fontsize=8); ax.grid(True, alpha=0.4)

    # Panel 2: curva de sensibilidad al flicker Pst
    ax = axes[0, 1]
    f_flicker = np.logspace(-1, 2, 300)  # 0.1 - 100 Hz
    # curva de perceptibilidad (IEC 61000-3-3, forma aproximada)
    f0 = 8.8  # Hz maximo sensibilidad
    sensitivity = 1.0 / (1 + ((f_flicker - f0) / (f0 * 0.8))**2)
    sensitivity = sensitivity / sensitivity.max()
    ax.semilogx(f_flicker, sensitivity, color=ACC, lw=2.5,
                label='Curva de ponderacion Pst')
    ax.axvline(f0, color=BAD, ls='--', lw=1.5, label=f'Max sensibilidad {f0} Hz')
    ax.axhline(1.0, color='#888', ls=':', lw=1.2, label='Limite Pst=1')
    ax.fill_between(f_flicker, sensitivity, 0, alpha=0.15, color=ACC)
    ax.set_xlabel('Frecuencia de modulacion (Hz)')
    ax.set_ylabel('Sensibilidad normalizada')
    ax.set_title('Curva de sensibilidad al flicker (Pst)', fontsize=10)
    ax.legend(fontsize=8); ax.grid(True, alpha=0.4)

    # Panel 3: desequilibrio de tension (diagrama vectorial)
    ax = axes[1, 0]
    V_nom = 1.0; VUF = 0.015  # 1.5%
    # secuencia positiva
    angles_pos = [0, -2*np.pi/3, 2*np.pi/3]
    V_pos = V_nom
    # secuencia negativa (pequena)
    V_neg = V_nom * VUF
    angles_neg = [0, 2*np.pi/3, -2*np.pi/3]
    # fasores resultantes (Va = Vpos + Vneg, fase a=0)
    for i, (ap, an, col, lbl) in enumerate(zip(angles_pos, angles_neg,
                                                [ACC, ACC2, OK], ['Va', 'Vb', 'Vc'])):
        v_re = V_pos * np.cos(ap) + V_neg * np.cos(an)
        v_im = V_pos * np.sin(ap) + V_neg * np.sin(an)
        ax.annotate('', xy=(v_re, v_im), xytext=(0, 0),
                    arrowprops=dict(arrowstyle='->', color=col, lw=2.5))
        ax.text(v_re * 1.08, v_im * 1.08, lbl, color=col, fontsize=11, fontweight='bold')
    # circulo de referencia
    theta = np.linspace(0, 2*np.pi, 100)
    ax.plot(np.cos(theta), np.sin(theta), color='#ccc', lw=1, ls='--')
    ax.set_aspect('equal'); ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3)
    ax.axhline(0, color='#ddd', lw=0.8); ax.axvline(0, color='#ddd', lw=0.8)
    ax.set_xlabel('Re'); ax.set_ylabel('Im')
    ax.set_title(f'Desequilibrio de tension VUF={VUF*100:.1f}% (<2%)', fontsize=10)
    ax.grid(True, alpha=0.3)

    # Panel 4: rizado de bus DC
    ax = axes[1, 1]
    t_dc = np.linspace(0, 0.02, 2000)
    fsw = 5000
    Vdc_nom = 800
    # rizado de conmutacion + variacion lenta de carga
    rizado_sw = 3.0 * np.sin(2 * np.pi * fsw * t_dc)
    variacion_lenta = 10.0 * np.sin(2 * np.pi * 5 * t_dc)  # variacion de carga a 5 Hz
    Vdc = Vdc_nom + rizado_sw + variacion_lenta
    ax.plot(t_dc * 1000, Vdc, color=ACC, lw=1.2, label='V_dc(t)')
    ax.axhline(Vdc_nom, color='#888', ls=':', lw=1.5, label=f'V_dc* = {Vdc_nom} V')
    ax.axhline(Vdc_nom * 1.01, color=BAD, ls='--', lw=1.5, label='Limite +1%')
    ax.axhline(Vdc_nom * 0.99, color=BAD, ls='--', lw=1.5, label='Limite -1%')
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('V_dc (V)')
    ax.set_title(f'Rizado bus DC: conmutacion ({fsw} Hz) + variacion lenta', fontsize=10)
    ax.legend(fontsize=7); ax.grid(True, alpha=0.4)
    ax.set_ylim([Vdc_nom - 20, Vdc_nom + 20])

    fig.suptitle('Calidad de potencia: THD, flicker, desequilibrio VUF y rizado DC',
                 fontsize=12, fontweight='bold')
    fig.tight_layout()
    _savefig(fig, "calidad-potencia-analisis.png")


def _conmut_analisis():
    """4 paneles: conmutado vs promediado, error vs h, coste CPU vs precision, comparativa."""
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    np.random.seed(0)

    # Panel 1: corriente conmutada vs promediada
    ax = axes[0, 0]
    fsw = 5000; T_sw = 1 / fsw
    t_sim = np.linspace(0, 5 * T_sw, 5000)
    # modelo promediado: respuesta de primer orden
    tau = 2e-3; d = 0.6; Vdc = 400; L = 2e-3
    I_ss = d * Vdc / (0.1)  # resistencia 0.1 ohm
    i_prom = I_ss * (1 - np.exp(-t_sim / tau))
    # modelo conmutado: agrega rizado triangular
    carrier = (t_sim % T_sw) / T_sw
    duty = 0.6
    s = (carrier < duty).astype(float)
    rizado = (s - duty) * Vdc / L * T_sw / 8  # amplitud aprox
    i_sw = i_prom + rizado * 0.5
    ax.plot(t_sim * 1000, i_sw, color=BAD, lw=1.5, alpha=0.8, label='Conmutado')
    ax.plot(t_sim * 1000, i_prom, color=ACC, lw=2.5, label='Promediado')
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Corriente (A)')
    ax.set_title('Corriente: conmutado vs promediado', fontsize=10)
    ax.legend(fontsize=9); ax.grid(True, alpha=0.4)

    # Panel 2: error en la fundamental vs paso de integracion h
    ax = axes[0, 1]
    h_vals = np.array([0.5, 1, 2, 5, 10, 20, 50, 100]) * 1e-6  # us
    # error aproximado: Delta_d = h*fsw, Delta_V = Vdc*Delta_d
    err_fund = h_vals * fsw * 100  # error en % de Vdc
    ax.loglog(h_vals * 1e6, err_fund, color=ACC, lw=2.5, marker='o', markersize=5)
    ax.axhline(0.1, color=BAD, ls='--', lw=1.5, label='Limite 0.1%')
    ax.axvline(1.0, color=ACC2, ls=':', lw=1.5, label='h=1us (tipico)')
    ax.axvline(20.0, color='#888', ls=':', lw=1.5, label='h=1/10fsw')
    ax.set_xlabel('Paso de integracion h (us)'); ax.set_ylabel('Error en fundamental (%)')
    ax.set_title('Error vs paso de integracion (aliasing de conmutacion)', fontsize=10)
    ax.legend(fontsize=8); ax.grid(True, alpha=0.4)

    # Panel 3: coste computacional (tiempo CPU relativo)
    ax = axes[1, 0]
    modelos = ['Promediado\nlineal', 'Promediado\nno lineal', 'Conmutado\nh=20us',
               'Conmutado\nh=1us', 'Conmutado\nEventos']
    t_cpu = [1, 3, 20, 400, 15]
    colors_cpu = [OK, ACC, ACC2, BAD, ACC]
    bars = ax.bar(modelos, t_cpu, color=colors_cpu, alpha=0.8, edgecolor='white')
    ax.set_ylabel('Tiempo CPU relativo')
    ax.set_title('Coste computacional por modelo (simulacion 1s)', fontsize=10)
    for bar, val in zip(bars, t_cpu):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3,
                f'{val}x', ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax.grid(True, alpha=0.4, axis='y')

    # Panel 4: comparativa: precision vs velocidad
    ax = axes[1, 1]
    precision = [99.5, 98, 95, 99.9, 95]
    velocidad = [100, 33, 5, 0.25, 6.7]
    labels_comp = ['Prom. lineal', 'Prom. no-lin', 'Conm. h=20us', 'Conm. h=1us', 'Conm. eventos']
    scatter_col = [OK, ACC, ACC2, BAD, ACC]
    for i, (p, v, lbl, col) in enumerate(zip(precision, velocidad, labels_comp, scatter_col)):
        ax.scatter(v, p, color=col, s=120, zorder=5)
        ax.text(v * 1.05, p - 0.3, lbl, fontsize=8, color=col)
    ax.set_xlabel('Velocidad relativa (simulacion/s CPU)')
    ax.set_ylabel('Precision en fundamental (%)')
    ax.set_title('Compromiso precision vs velocidad', fontsize=10)
    ax.set_xscale('log'); ax.grid(True, alpha=0.4)

    fig.suptitle('Simulacion conmutada: rizado, error vs h, coste CPU y trade-off',
                 fontsize=12, fontweight='bold')
    fig.tight_layout()
    _savefig(fig, "simulacion-conmutada-analisis.png")


def _fftanal_analisis():
    """4 paneles: comparativa ventanas, espectrograma STFT, PSD Welch vs periodograma, espectro PWM."""
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import signal as sig
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    np.random.seed(5)

    # Panel 1: comparativa de ventanas (leakage)
    ax = axes[0, 0]
    fs = 10000; N = 512
    f_tono = 127.3  # no coherente con N/fs
    t = np.arange(N) / fs
    x = np.sin(2 * np.pi * f_tono * t)
    f_bins = np.fft.rfftfreq(N, 1/fs)
    ventanas = [('Rectangular', np.ones(N), BAD),
                ('Hann', np.hanning(N), ACC),
                ('Blackman', np.blackman(N), OK)]
    for nombre, w, col in ventanas:
        X = np.fft.rfft(x * w)
        mag = 2 * np.abs(X) / np.sum(w)
        ax.semilogy(f_bins, mag + 1e-6, color=col, lw=1.8, label=nombre)
    ax.axvline(f_tono, color='#888', ls=':', lw=1.2, label=f'Tono {f_tono:.1f}Hz')
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Amplitud')
    ax.set_title('Comparativa ventanas: leakage espectral', fontsize=10)
    ax.legend(fontsize=8); ax.grid(True, alpha=0.4)
    ax.set_xlim([0, 400])

    # Panel 2: espectrograma STFT
    ax = axes[0, 1]
    fs2 = 10000; dur = 1.0
    t2 = np.arange(int(fs2 * dur)) / fs2
    # senal con SSO que aparece a t=0.4s
    f1 = 50; f_sso = 12
    amp_sso = np.where(t2 > 0.4, 0.15 * np.exp(-(t2 - 0.4) / 0.1), 0)
    x2 = np.sin(2 * np.pi * f1 * t2) + amp_sso * np.sin(2 * np.pi * (f1 - f_sso) * t2)
    x2 += 0.02 * np.random.randn(len(t2))
    f_stft, t_stft, Zxx = sig.stft(x2, fs=fs2, window='hann', nperseg=512, noverlap=384)
    ax.pcolormesh(t_stft, f_stft, 20 * np.log10(np.abs(Zxx) + 1e-8),
                  shading='gouraud', cmap='Blues', vmin=-60, vmax=0)
    ax.set_ylim([0, 150]); ax.set_xlabel('Tiempo (s)'); ax.set_ylabel('Frecuencia (Hz)')
    ax.set_title(f'Espectrograma STFT: SSO a {f1-f_sso} Hz desde t=0.4s', fontsize=10)
    ax.axhline(f1 - f_sso, color=BAD, ls='--', lw=1.5, label=f'SSO {f1-f_sso}Hz')
    ax.legend(fontsize=8)

    # Panel 3: PSD Welch vs periodograma
    ax = axes[1, 0]
    fs3 = 10000; T3 = 2.0
    t3 = np.arange(int(fs3 * T3)) / fs3
    x3 = (np.sin(2 * np.pi * 50 * t3) + 0.1 * np.sin(2 * np.pi * 250 * t3)
           + 0.3 * np.random.randn(len(t3)))
    # periodograma simple
    f_per = np.fft.rfftfreq(len(t3), 1/fs3)
    X_per = np.fft.rfft(x3 * np.hanning(len(t3)))
    psd_per = (2 * np.abs(X_per)**2) / (fs3 * np.sum(np.hanning(len(t3))**2))
    # Welch
    f_w, psd_w = sig.welch(x3, fs=fs3, window='hann', nperseg=1024, noverlap=512)
    ax.semilogy(f_per, psd_per, color=BAD, lw=1.0, alpha=0.6, label='Periodograma simple')
    ax.semilogy(f_w, psd_w, color=ACC, lw=2.0, label='Welch (nperseg=1024)')
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('PSD (V^2/Hz)')
    ax.set_title('PSD: Welch vs periodograma (menor varianza)', fontsize=10)
    ax.legend(fontsize=8); ax.grid(True, alpha=0.4)
    ax.set_xlim([0, 500])

    # Panel 4: espectro de un convertidor PWM con SSO
    ax = axes[1, 1]
    fsw = 5000; f1 = 50
    # componentes espectrales de VSC 2 niveles
    componentes = {
        f1: 100,            # fundamental
        f1*5: 3.8, f1*7: 2.5, f1*11: 1.0, f1*13: 0.7,  # armonicos bajos
        fsw - 2*f1: 8, fsw + 2*f1: 8,       # bandas laterales fsw+-2f1
        2*fsw - f1: 4, 2*fsw + f1: 4,        # bandas 2fsw+-f1
        f1 - 12: 2.5, f1 + 12: 2.5,          # SSO +-12 Hz
    }
    freqs_c = list(componentes.keys()); amps_c = list(componentes.values())
    ax.bar(freqs_c, amps_c, width=60, color=ACC, alpha=0.8)
    for f_c, a_c in componentes.items():
        if f_c < 500:
            ax.bar([f_c], [a_c], width=20, color=BAD if a_c > 3 else OK, alpha=0.9)
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Amplitud (%)')
    ax.set_title(f'Espectro VSC 2N: fundamental, armonicos, bandas fsw={fsw}Hz', fontsize=10)
    ax.axvline(fsw, color='#888', ls='--', lw=1.2, label=f'fsw={fsw}Hz')
    ax.legend(fontsize=8); ax.grid(True, alpha=0.4)

    fig.suptitle('FFT: ventanas, espectrograma STFT, PSD Welch y espectro PWM',
                 fontsize=12, fontweight='bold')
    fig.tight_layout()
    _savefig(fig, "fft-analisis-espectral-analisis.png")


def _hilphil_analisis():
    """4 paneles: arquitectura HiL, LVRT HiL vs real, retardo en estabilidad, cobertura."""
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Panel 1: arquitectura HiL esquematica
    ax = axes[0, 0]; ax.axis('off')
    bloques = [
        (0.08, 0.55, 0.22, 0.25, ACC, 'DSP\n(control real)'),
        (0.38, 0.55, 0.22, 0.25, ACC2, 'FPGA\n(planta RT)'),
        (0.68, 0.55, 0.22, 0.25, OK, 'PC Host\n(supervisión)'),
        (0.08, 0.15, 0.22, 0.20, BAD, 'ADC/DAC\n(interfaz)'),
        (0.38, 0.15, 0.22, 0.20, '#9E9E9E', 'CPU\n(red, logica)'),
    ]
    for bx, by, bw, bh, col, lbl in bloques:
        ax.add_patch(mpatches.FancyBboxPatch((bx, by), bw, bh,
                                              boxstyle='round,pad=0.02',
                                              facecolor=col, alpha=0.7, edgecolor='#555'))
        ax.text(bx + bw/2, by + bh/2, lbl, ha='center', va='center',
                fontsize=9, fontweight='bold')
    # flechas de conexion
    arrows = [(0.30, 0.67, 0.38, 0.67), (0.60, 0.67, 0.68, 0.67),
              (0.19, 0.55, 0.19, 0.35), (0.49, 0.55, 0.49, 0.35)]
    for x0, y0, x1, y1 in arrows:
        ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle='<->', color='#555', lw=1.5))
    # retardos
    ax.text(0.32, 0.73, 'Td_ADC\n~5us', ha='center', fontsize=7.5, color='#555')
    ax.text(0.19, 0.44, 'Td_comp\n~50us', ha='center', fontsize=7.5, color='#555')
    ax.set_xlim([0, 1]); ax.set_ylim([0, 1])
    ax.set_title('Arquitectura HiL: DSP real + planta en FPGA/CPU', fontsize=10)

    # Panel 2: LVRT en HiL vs real (comparativa de formas de onda)
    ax = axes[0, 1]
    t = np.linspace(0, 0.4, 800)
    v_red = np.ones_like(t)
    v_red[(t >= 0.1) & (t < 0.25)] = 0.2  # hueco
    # respuesta HiL (con leve retardo de 1ms)
    i_hil = np.zeros_like(t)
    i_hil[t >= 0.1] = np.minimum(1.5, 1 + 2 * (1 - v_red[t >= 0.1]))
    i_hil[t >= 0.25] = np.exp(-(t[t >= 0.25] - 0.25) / 0.05) * (i_hil[t >= 0.25][0] - 1) + 1
    # respuesta real (ligeramente distinta por parasitos)
    np.random.seed(3)
    i_real = i_hil + 0.02 * np.random.randn(len(t))
    ax.plot(t * 1000, v_red, color=ACC2, lw=2, label='V_red (p.u.)')
    ax.plot(t * 1000, i_hil, color=ACC, lw=2, label='I_HiL (p.u.)')
    ax.plot(t * 1000, i_real, color=BAD, lw=1.5, ls='--', alpha=0.8, label='I_real (p.u.)')
    ax.axhline(1.5, color='#888', ls=':', lw=1, label='Limite 1.5pu')
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('p.u.')
    ax.set_title('LVRT en HiL vs ensayo real (20% de Vn, 150ms)', fontsize=10)
    ax.legend(fontsize=7); ax.grid(True, alpha=0.4)

    # Panel 3: efecto del retardo en el margen de fase
    ax = axes[1, 0]
    fc_arr = np.linspace(50, 2000, 300)
    for Td, col, lbl in [(50e-6, OK, 'Td=50us'), (100e-6, ACC, 'Td=100us'),
                         (150e-6, ACC2, 'Td=150us'), (250e-6, BAD, 'Td=250us')]:
        pm_loss = Td * 2 * np.pi * fc_arr * 180 / np.pi
        ax.plot(fc_arr, pm_loss, color=col, lw=2, label=lbl)
    ax.fill_between(fc_arr, 45, 90, alpha=0.08, color=OK, label='Zona segura (>45deg)')
    ax.axhline(45, color='#555', ls='--', lw=1.5, label='PM min 45deg')
    ax.set_xlabel('Frecuencia de cruce fc (Hz)')
    ax.set_ylabel('Perdida de margen de fase (deg)')
    ax.set_title('Impacto del retardo HIL en el margen de fase', fontsize=10)
    ax.legend(fontsize=7); ax.grid(True, alpha=0.4)
    ax.set_ylim([0, 100])

    # Panel 4: cobertura de pruebas HiL vs campo
    ax = axes[1, 1]
    categorias = ['LVRT', 'Anti-\nislanding', 'Protec.\nsobre-I', 'Arranque\nfrio', 'EMC', 'Termico']
    cobertura_hil = [95, 90, 98, 85, 10, 5]
    cobertura_campo = [100, 100, 100, 100, 100, 100]
    x = np.arange(len(categorias))
    ax.bar(x - 0.2, cobertura_hil, width=0.35, color=ACC, alpha=0.8, label='HiL')
    ax.bar(x + 0.2, cobertura_campo, width=0.35, color=ACC2, alpha=0.5, label='Campo')
    ax.set_xticks(x); ax.set_xticklabels(categorias, fontsize=8)
    ax.set_ylabel('Cobertura (%)')
    ax.set_title('Cobertura de pruebas: HiL vs campo', fontsize=10)
    ax.legend(fontsize=9); ax.grid(True, alpha=0.4, axis='y')

    fig.suptitle('HiL/PHiL: arquitectura, LVRT, retardo y cobertura de pruebas',
                 fontsize=12, fontweight='bold')
    fig.tight_layout()
    _savefig(fig, "hil-phil-analisis.png")


def _fsolve_analisis():
    """4 paneles: convergencia NR, curva P-V, sensibilidad al x0, error vs iteracion."""
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Panel 1: convergencia Newton-Raphson
    ax = axes[0, 0]
    # NR para f(x) = x^2 - 2 (raiz sqrt(2))
    x_nr = [3.0]
    residuos = [abs(x_nr[-1]**2 - 2)]
    for _ in range(8):
        xk = x_nr[-1]
        xk1 = xk - (xk**2 - 2) / (2 * xk)
        x_nr.append(xk1)
        residuos.append(abs(xk1**2 - 2))
    iters = np.arange(len(residuos))
    ax.semilogy(iters, residuos, color=ACC, lw=2.5, marker='o', markersize=7,
                label='Newton-Raphson')
    ax.semilogy(iters, [3.0 * (0.5)**i for i in iters], color=BAD, lw=1.5,
                ls='--', label='Convergencia lineal (ref.)')
    ax.set_xlabel('Iteracion'); ax.set_ylabel('Residuo |f(xk)|')
    ax.set_title('Convergencia cuadratica de Newton-Raphson', fontsize=10)
    ax.legend(fontsize=8); ax.grid(True, alpha=0.4)

    # Panel 2: curva P-V con dos puntos de equilibrio
    ax = axes[0, 1]
    V_g = 1.0; Z_g = 0.3; X_g = Z_g  # red inductiva
    V_arr = np.linspace(0.1, 1.2, 500)
    # potencia maxima transferible
    P_vals = V_arr * V_g / X_g * np.sqrt(1 - ((V_arr**2 - V_g**2) /
             (2 * X_g * V_arr * V_g / X_g + 1e-6))**2 + 0.0)
    # simplificado: P = V*Vg/Xg * sin(delta) -> curva P-V
    delta_arr = np.linspace(0, np.pi, 500)
    P_curve = (V_g**2 / X_g) * np.sin(delta_arr)
    V_curve = V_g * np.cos(delta_arr) + np.sqrt(np.maximum(0, 1 - np.sin(delta_arr)**2))
    ax.plot(P_curve, V_curve / V_g, color=ACC, lw=2.5, label='Curva P-V')
    P_op = 0.6
    # dos puntos
    delta1 = np.arcsin(P_op * X_g / V_g**2); delta2 = np.pi - delta1
    V1 = V_g * np.cos(delta1) + np.sqrt(max(0, 1 - np.sin(delta1)**2))
    V2 = V_g * np.cos(delta2) - np.sqrt(max(0, 1 - np.sin(delta2)**2))
    ax.scatter([P_op], [max(0.1, V1/V_g)], color=OK, s=120, zorder=5,
               label=f'Estable V={V1/V_g:.2f}pu')
    ax.scatter([P_op], [max(0.05, abs(V2/V_g))], color=BAD, s=120, zorder=5,
               label=f'Inestable V={abs(V2/V_g):.2f}pu')
    ax.axvline(P_op, color='#888', ls=':', lw=1.2)
    ax.set_xlabel('Potencia P (p.u.)'); ax.set_ylabel('Tension V (p.u.)')
    ax.set_title('Curva P-V: dos equilibrios en red debil', fontsize=10)
    ax.legend(fontsize=7); ax.grid(True, alpha=0.4)
    ax.set_ylim([0, 1.3])

    # Panel 3: sensibilidad al punto inicial
    ax = axes[1, 0]
    # f(x) = x^3 - x (raices en -1, 0, +1)
    x_range = np.linspace(-2, 2, 400)
    ax.plot(x_range, x_range**3 - x_range, color=ACC, lw=2, label='f(x) = x^3 - x')
    ax.axhline(0, color='#888', ls='-', lw=1)
    roots = [-1, 0, 1]
    root_cols = [BAD, ACC2, OK]
    # mostrar cuencas de atraccion con colores
    for x0_val, col in [(-1.8, BAD), (-0.5, ACC2), (0.5, OK), (1.8, OK)]:
        # NR simplificado
        x_k = x0_val
        traj = [x_k]
        for _ in range(10):
            fp = 3*x_k**2 - 1
            if abs(fp) < 1e-10:
                break
            x_k = x_k - (x_k**3 - x_k) / fp
            traj.append(x_k)
            if abs(x_k**3 - x_k) < 1e-9:
                break
        converged_to = round(traj[-1])
        traj_arr = np.array(traj)
        ax.plot(range(len(traj_arr)), traj_arr, marker='o', markersize=4,
                color=col, lw=1.5, alpha=0.8)
    for r, col in zip(roots, root_cols):
        ax.axhline(0, color='#ccc', lw=0.5)
    ax.set_xlabel('Iteracion'); ax.set_ylabel('x_k')
    ax.set_title('Sensibilidad al punto inicial: distintas cuencas', fontsize=10)
    ax.legend(fontsize=8); ax.grid(True, alpha=0.4)
    ax.set_ylim([-2.5, 2.5])

    # Panel 4: comparativa error vs iteracion para distintos metodos
    ax = axes[1, 1]
    iters_c = np.arange(1, 12)
    # Newton-Raphson: cuadratico
    err_nr = 1.0 / (2.0 ** (2 ** iters_c / 4))
    err_nr = np.clip(err_nr, 1e-14, 1)
    # Biseccion: lineal
    err_bis = 0.5 ** iters_c
    # Secante: orden 1.618
    phi = (1 + np.sqrt(5)) / 2
    err_sec = 0.8 ** (phi ** iters_c / 2)
    err_sec = np.clip(err_sec, 1e-14, 1)
    ax.semilogy(iters_c, err_bis, color=BAD, lw=2, marker='s', markersize=5,
                label='Biseccion (orden 1)')
    ax.semilogy(iters_c, err_sec, color=ACC2, lw=2, marker='^', markersize=5,
                label='Secante (orden 1.618)')
    ax.semilogy(iters_c, err_nr, color=ACC, lw=2.5, marker='o', markersize=6,
                label='Newton-Raphson (orden 2)')
    ax.set_xlabel('Numero de iteraciones'); ax.set_ylabel('Error estimado')
    ax.set_title('Velocidad de convergencia: NR vs biseccion vs secante', fontsize=10)
    ax.legend(fontsize=8); ax.grid(True, alpha=0.4)

    fig.suptitle('fsolve: convergencia NR, curva P-V, sensibilidad x0 y comparativa',
                 fontsize=12, fontweight='bold')
    fig.tight_layout()
    _savefig(fig, "equilibrio-fsolve-analisis.png")


def _stiff_analisis():
    """4 paneles: Euler exp vs imp en sistema stiff, region de estabilidad, paso Radau, comparativa."""
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Panel 1: Euler explicito vs implicito en sistema stiff
    ax = axes[0, 0]
    # sistema stiff: dy/dt = lambda*y, lambda = -1000 (rapido) + -1 (lento)
    # solucion: y = A*exp(-1000t) + B*exp(-t)
    lam_fast, lam_slow = -1000.0, -1.0
    A, B = 1.0, 1.0
    T_end = 0.01
    t_exact = np.linspace(0, T_end, 500)
    y_exact = A * np.exp(lam_fast * t_exact) + B * np.exp(lam_slow * t_exact)

    # Euler explicito con h = 1/500 (justo estable)
    h_exp = 1.5e-3  # mayor que 2/|lambda_fast|=0.002 -> inestable
    N_exp = int(T_end / h_exp) + 1
    t_exp = np.arange(N_exp) * h_exp
    y_exp = np.zeros(N_exp); y_exp[0] = A + B
    for i in range(N_exp - 1):
        y_exp[i+1] = y_exp[i] + h_exp * (lam_fast * y_exp[i] + lam_slow * y_exp[i])
        if abs(y_exp[i+1]) > 1e3:
            y_exp[i+1:] = np.nan; break

    # Euler implicito con h = 1e-3 (grande)
    h_imp = 1e-3
    N_imp = int(T_end / h_imp) + 1
    t_imp = np.arange(N_imp) * h_imp
    y_imp = np.zeros(N_imp); y_imp[0] = A + B
    for i in range(N_imp - 1):
        y_imp[i+1] = y_imp[i] / (1 - h_imp * (lam_fast + lam_slow))

    ax.plot(t_exact * 1000, y_exact, 'k-', lw=2, label='Exacta')
    ax.plot(t_exp * 1000, y_exp, color=BAD, lw=1.5, ls='--',
            label=f'Euler exp. h={h_exp*1000:.1f}ms (INESTABLE)')
    ax.plot(t_imp * 1000, y_imp, color=ACC, lw=2, marker='o', markersize=4,
            label=f'Euler imp. h={h_imp*1000:.0f}ms (estable)')
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('y(t)')
    ax.set_title('Stiff: Euler explicito inestable vs implicito estable', fontsize=10)
    ax.legend(fontsize=7); ax.grid(True, alpha=0.4)
    ax.set_ylim([-3, 4])

    # Panel 2: region de estabilidad en el plano h*lambda
    ax = axes[0, 1]
    re = np.linspace(-4, 1, 300); im = np.linspace(-3, 3, 300)
    RE, IM = np.meshgrid(re, im)
    HL = RE + 1j * IM
    # Euler explicito: |1 + h*lambda| <= 1
    R_exp = np.abs(1 + HL)
    # Euler implicito: |1/(1 - h*lambda)| <= 1
    R_imp = np.abs(1.0 / (1 - HL))
    ax.contourf(RE, IM, R_exp, levels=[0, 1], colors=[ACC], alpha=0.4)
    ax.contour(RE, IM, R_exp, levels=[1], colors=[ACC], linewidths=2)
    ax.contourf(RE, IM, R_imp, levels=[0, 1], colors=[OK], alpha=0.2)
    # marcar los lambdas del ejemplo
    ax.scatter([lam_fast * h_exp], [0], color=BAD, s=150, zorder=5,
               label=f'hλ_rapido={lam_fast*h_exp:.1f} (exp. inestable)')
    ax.scatter([lam_fast * h_imp], [0], color=ACC2, s=150, zorder=5,
               label=f'hλ_rapido={lam_fast*h_imp:.1f} (imp. estable)')
    ax.axhline(0, color='#888', lw=0.8); ax.axvline(0, color='#888', lw=0.8)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=ACC, alpha=0.6, label='Euler exp. (disco)'),
                        Patch(color=OK, alpha=0.4, label='Euler imp. (semiplano izq.)'),
                        *ax.get_legend_handles_labels()[0]], fontsize=7, loc='upper left')
    ax.set_xlabel('Re(h*lambda)'); ax.set_ylabel('Im(h*lambda)')
    ax.set_title('Region de estabilidad: Euler exp. vs impl.', fontsize=10)
    ax.grid(True, alpha=0.3)

    # Panel 3: paso de tiempo adaptativo (Radau)
    ax = axes[1, 0]
    # simular paso adaptativo: grande en zona lenta, pequeno en transitorio
    t_adapt = [0]
    h_adapt = []
    t_current = 0.0; T_end3 = 0.05
    while t_current < T_end3:
        # criterio de paso: mas pequeno durante el transitorio rapido
        if t_current < 0.005:
            h = 1e-4  # transitorio rapido: paso pequeno
        else:
            h = max(5e-4, min(2e-3, 2e-3 * (1 - np.exp(-(t_current - 0.005) / 0.01))))
        h = min(h, T_end3 - t_current)
        h_adapt.append(h)
        t_current += h
        t_adapt.append(t_current)
    ax.plot(np.array(t_adapt[:-1]) * 1000, np.array(h_adapt) * 1e6,
            color=ACC, lw=2, label='Paso adaptativo h(t)')
    ax.axvline(5, color=BAD, ls='--', lw=1.5, label='Fin transitorio rapido')
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Paso h (us)')
    ax.set_title('Paso adaptativo Radau: pequeno en transitorio, grande despues', fontsize=10)
    ax.legend(fontsize=8); ax.grid(True, alpha=0.4)

    # Panel 4: tiempo CPU vs error para distintos solvers
    ax = axes[1, 1]
    solvers = ['Euler\nexp.', 'RK4\nexpl.', 'Euler\nimp.', 'BDF-2', 'Radau\nIIA']
    t_cpu_s = [10.0, 8.0, 2.0, 0.5, 0.8]  # tiempo CPU relativo
    err_s = [1e-2, 1e-4, 5e-2, 1e-5, 1e-8]  # error tipico
    cols_s = [BAD, ACC2, '#FF9966', ACC, OK]
    for solver, t_c, err_v, col in zip(solvers, t_cpu_s, err_s, cols_s):
        ax.scatter([t_c], [err_v], s=200, color=col, zorder=5)
        ax.text(t_c * 1.1, err_v * 1.5, solver, fontsize=8.5, color=col, va='center')
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlabel('Tiempo CPU relativo'); ax.set_ylabel('Error global estimado')
    ax.set_title('Compromiso tiempo CPU vs error (sistema stiff)', fontsize=10)
    ax.grid(True, alpha=0.4)
    ax.invert_xaxis()

    fig.suptitle('Integracion EDOs stiff: Euler, regiones de estabilidad, paso adaptativo',
                 fontsize=12, fontweight='bold')
    fig.tight_layout()
    _savefig(fig, "integracion-edos-stiff-analisis.png")


def _topologias_multinivel_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    t = np.linspace(0, 0.04, 4000); f0 = 50; Vdc = 1.0
    ax = axes[0, 0]
    v2 = Vdc * np.sign(np.sin(2*np.pi*f0*t))
    m = 0.9; ref = m*np.sin(2*np.pi*f0*t)
    v3 = np.where(ref > 0.5, Vdc/2, np.where(ref < -0.5, -Vdc/2, 0))
    levels5 = np.array([-1, -0.5, 0, 0.5, 1]) * Vdc/2
    v5 = np.array([levels5[np.argmin(np.abs(levels5 - ri*Vdc/2))] for ri in ref])
    ax.plot(t*1000, v2, 'r-', lw=0.8, alpha=0.7, label='2 niveles')
    ax.plot(t*1000, v3, 'b-', lw=0.8, alpha=0.7, label='3 niveles')
    ax.plot(t*1000, v5, 'g-', lw=0.8, alpha=0.7, label='5 niveles')
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Tensión (pu)')
    ax.set_title('Forma de onda: 2/3/5 niveles'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax = axes[0, 1]
    n_levels = np.array([2, 3, 5, 7, 9])
    thd_v = np.array([80, 30, 11, 5, 2.5])
    ax.semilogy(n_levels, thd_v, 'b-o', lw=2, markersize=8)
    ax.axhline(5, color='r', ls='--', label='Límite IEEE 519 (5%)')
    ax.set_xlabel('Número de niveles'); ax.set_ylabel('THD tensión (%)')
    ax.set_title('THD vs número de niveles'); ax.legend(); ax.grid(True, alpha=0.3)
    ax = axes[1, 0]
    N_fft = len(t)
    V2_f = np.abs(np.fft.rfft(v2)) * 2/N_fft
    V5_f = np.abs(np.fft.rfft(v5)) * 2/N_fft
    f_arr = np.fft.rfftfreq(N_fft, t[1]-t[0])
    ax.semilogy(f_arr, V2_f+1e-4, 'r-', lw=1, alpha=0.8, label='2 niveles')
    ax.semilogy(f_arr, V5_f+1e-4, 'g-', lw=1, alpha=0.8, label='5 niveles')
    ax.set_xlim([0, 5000]); ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Amplitud (pu)')
    ax.set_title('Espectro: 2 vs 5 niveles'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax = axes[1, 1]
    niveles_c = ['2 niv.', '3 niv.', '5 niv.', '7 niv.']
    filtro_rel = [100, 40, 15, 8]
    efic = [97.5, 97.8, 98.0, 98.1]
    x = np.arange(len(niveles_c)); w_b = 0.35
    ax2 = ax.twinx()
    ax.bar(x - w_b/2, filtro_rel, w_b, alpha=0.7, color='red', label='Filtro LC (%)')
    ax2.plot(x + w_b/2, efic, 'b-o', lw=2, label='Eficiencia (%)')
    ax.set_xticks(x); ax.set_xticklabels(niveles_c)
    ax.set_ylabel('Tamaño filtro (% relativo)', color='red')
    ax2.set_ylabel('Eficiencia (%)', color='blue')
    ax.set_title('Filtro y eficiencia vs niveles')
    ax.legend(fontsize=8, loc='upper right'); ax2.legend(fontsize=8, loc='lower right'); ax.grid(True, alpha=0.3, axis='y')
    fig.suptitle('Topologías multinivel: formas de onda, THD y aplicaciones', fontsize=14, fontweight='bold')
    plt.tight_layout(); _savefig(fig, "topologias-multinivel-analisis")


def _impedancia_reactancia_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    ax = axes[0, 0]
    R = 0.5; X = 0.866; Z = complex(R, X)
    ax.annotate('', xy=(R, X), xytext=(0, 0), arrowprops=dict(arrowstyle='->', color='blue', lw=2.5))
    ax.annotate('', xy=(R, 0), xytext=(0, 0), arrowprops=dict(arrowstyle='->', color='red', lw=2))
    ax.annotate('', xy=(R, X), xytext=(R, 0), arrowprops=dict(arrowstyle='->', color='green', lw=2))
    ax.text(R/2, -0.08, f'R={R}Ω', ha='center', color='red', fontsize=10)
    ax.text(R+0.08, X/2, f'jX={X:.2f}Ω', ha='left', color='green', fontsize=10)
    ax.text(R/2+0.1, X/2+0.1, f'|Z|={abs(Z):.2f}Ω\nφ={np.degrees(np.angle(Z)):.1f}°', color='blue', fontsize=10)
    ax.set_xlim([-0.2, 1.2]); ax.set_ylim([-0.3, 1.2])
    ax.axhline(0, color='k', lw=0.5); ax.axvline(0, color='k', lw=0.5)
    ax.set_xlabel('Re (Ω)'); ax.set_ylabel('Im (Ω)'); ax.set_title('Diagrama fasorial de impedancia')
    ax.grid(True, alpha=0.3)
    ax = axes[0, 1]
    SCR_arr = np.linspace(1, 10, 100)
    V = 1.0; P_conv = 1.0
    Xsc = V**2 / (SCR_arr * P_conv)
    ax.plot(SCR_arr, Xsc, 'b-', lw=2)
    ax.axvline(2, color='r', ls='--', label='SCR=2 (débil)')
    ax.axvline(3, color='orange', ls='--', label='SCR=3 (límite)')
    ax.set_xlabel('SCR'); ax.set_ylabel('X_sc (pu)'); ax.set_title('Reactancia de red vs SCR')
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax = axes[1, 0]
    w = np.logspace(1, 4, 500); f_pll = 20; w_pll = 2*np.pi*f_pll
    Z_re = 0.5 - 1.5*w_pll**2/(w**2 + w_pll**2)
    Z_im = 0.3*w/1000
    ax.semilogx(w/(2*np.pi), Z_re, 'b-', lw=2, label='Re[Z_inv] GFL')
    ax.semilogx(w/(2*np.pi), Z_im, 'r--', lw=2, label='Im[Z_inv] GFL')
    ax.axhline(0, color='k', lw=1)
    ax.fill_between(w/(2*np.pi), Z_re, 0, where=Z_re < 0, alpha=0.2, color='red', label='Zona negativa')
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Impedancia (pu)')
    ax.set_title('Impedancia GFL — zona negativa'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax = axes[1, 1]
    f = np.logspace(1, 4, 500); w2 = 2*np.pi*f
    Ls = 1e-3; Rs = 0.05; Cl = 1e-3; Rl = 2.0
    Zs = np.sqrt(Rs**2 + (w2*Ls)**2)
    Zl = Rl / np.sqrt(1 + (w2*Rl*Cl)**2)
    ax.loglog(f, Zs, 'b-', lw=2, label='|Z_source|')
    ax.loglog(f, Zl, 'r-', lw=2, label='|Z_load|')
    ax.fill_between(f, Zs, Zl, where=Zs < Zl, alpha=0.2, color='green', label='Middlebrook OK')
    ax.fill_between(f, Zs, Zl, where=Zs > Zl, alpha=0.2, color='red', label='Riesgo')
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Impedancia (Ω)')
    ax.set_title('Criterio de estabilidad Middlebrook'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    fig.suptitle('Impedancia y reactancia: fasorial, SCR y criterio de estabilidad', fontsize=14, fontweight='bold')
    plt.tight_layout(); _savefig(fig, "impedancia-reactancia-analisis")


def _valor_rms_factor_potencia_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    t = np.linspace(0, 0.04, 4000); f0 = 50
    I1=10; I3=2; I5=1.2; I7=0.6
    i_dist = I1*np.sin(2*np.pi*f0*t) + I3*np.sin(2*np.pi*3*f0*t) + I5*np.sin(2*np.pi*5*f0*t) + I7*np.sin(2*np.pi*7*f0*t)
    I_rms = np.sqrt(np.mean(i_dist**2))
    I_fund_rms = I1/np.sqrt(2)
    ax = axes[0, 0]
    ax.plot(t*1000, i_dist, 'b-', lw=1.5, label='i(t) distorsionada')
    ax.axhline(I_rms, color='r', ls='--', lw=2, label=f'I_rms={I_rms:.2f} A')
    ax.axhline(I_fund_rms, color='g', ls=':', lw=2, label=f'I1_rms={I_fund_rms:.2f} A')
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Corriente (A)')
    ax.set_title('RMS de señal distorsionada'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax = axes[0, 1]; ax.axis('off')
    P=8; Q=4; D=2; S=np.sqrt(P**2+Q**2+D**2)
    ax.annotate('', xy=(P,0), xytext=(0,0), arrowprops=dict(arrowstyle='->', color='green', lw=3))
    ax.annotate('', xy=(P,Q), xytext=(P,0), arrowprops=dict(arrowstyle='->', color='blue', lw=3))
    ax.annotate('', xy=(P,Q+D), xytext=(P,Q), arrowprops=dict(arrowstyle='->', color='orange', lw=3))
    ax.annotate('', xy=(P,Q+D), xytext=(0,0), arrowprops=dict(arrowstyle='->', color='red', lw=2))
    ax.text(P/2, -0.5, f'P={P} kW', ha='center', color='green', fontsize=11, fontweight='bold')
    ax.text(P+0.3, Q/2, f'Q={Q} kvar', color='blue', fontsize=11, fontweight='bold')
    ax.text(P+0.3, Q+D/2, f'D={D} kVA', color='orange', fontsize=11, fontweight='bold')
    ax.text(P/2-1, (Q+D)/2+0.3, f'S={S:.1f} kVA', color='red', fontsize=11, fontweight='bold')
    ax.set_xlim([-0.5, 10]); ax.set_ylim([-1, 7.5]); ax.set_title('Triángulo de potencias P/Q/D/S')
    ax = axes[1, 0]
    THD_arr = np.linspace(0, 100, 200)
    for cosph, col in [(1.0, 'b'), (0.95, 'g'), (0.85, 'r')]:
        FP_real = cosph / np.sqrt(1 + (THD_arr/100)**2)
        ax.plot(THD_arr, FP_real, color=col, lw=2, label=f'cosφ={cosph}')
    ax.axhline(0.95, color='gray', ls='--', label='FP=0.95')
    ax.set_xlabel('THD_I (%)'); ax.set_ylabel('FP real'); ax.set_title('FP real vs THD para distintos cosφ')
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax = axes[1, 1]
    Q_comp = np.linspace(0, 6, 100)
    FP_before = 0.75
    S_before = 10; P_load = S_before*FP_before; Q_before = np.sqrt(S_before**2 - P_load**2)
    Q_after = Q_before - Q_comp
    S_after = np.sqrt(P_load**2 + np.maximum(Q_after, 0)**2)
    FP_after = P_load / S_after
    ax.plot(Q_comp, FP_after, 'b-', lw=2, label='FP tras corrección')
    ax.axhline(0.95, color='r', ls='--', label='FP objetivo=0.95')
    ax.set_xlabel('Q compensado (kvar)'); ax.set_ylabel('Factor de potencia')
    ax.set_title('Corrección del FP con banco de condensadores'); ax.legend(); ax.grid(True, alpha=0.3)
    fig.suptitle('RMS, factor de potencia y potencia de distorsión', fontsize=14, fontweight='bold')
    plt.tight_layout(); _savefig(fig, "valor-rms-factor-potencia-analisis")


def _modelo_linea_distribucion_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    ax = axes[0, 0]; ax.axis('off')
    R_km=0.1; L_km=1e-3; C_km=10e-9; l=100
    Z=complex(R_km*l, 2*np.pi*50*L_km*l); Y=complex(0, 2*np.pi*50*C_km*l)
    lines=[f'Línea de {l} km — parámetros típicos:',
           f'R = {R_km} Ω/km × {l} km = {R_km*l} Ω',
           f'X = ωL = {2*np.pi*50*L_km*1000:.1f} mΩ/km × {l} km = {2*np.pi*50*L_km*l:.1f} Ω',
           f'B = ωC = {2*np.pi*50*C_km*1e6:.2f} μS/km × {l} km',
           f'|Z| = {abs(Z):.2f} Ω, ∠Z = {np.degrees(np.angle(Z)):.1f}°',
           f'Zc = √(Z/Y) ≈ {np.sqrt(abs(Z)/abs(Y)):.0f} Ω',
           f'SIL ≈ {(400e3)**2/np.sqrt(abs(Z)/abs(Y))/1e6:.0f} MW (400 kV)']
    for i, line in enumerate(lines):
        ax.text(0.05, 0.92-i*0.13, line, transform=ax.transAxes, fontsize=10, va='top')
    ax.set_title('Parámetros del modelo π')
    ax = axes[0, 1]
    x = np.linspace(0, 200, 200)
    V_load = 1.0 - 0.0003*x
    V_no_load_ferranti = 1.0 + 0.00008*x**1.5/200
    ax.plot(x, V_load, 'b-', lw=2, label='Con carga (P+Q)')
    ax.plot(x, V_no_load_ferranti, 'r--', lw=2, label='En vacío (Ferranti)')
    ax.axhline(1.0, color='gray', ls=':'); ax.axhline(0.95, color='orange', ls=':', label='V_min=0.95pu')
    ax.set_xlabel('Distancia (km)'); ax.set_ylabel('Tensión (pu)')
    ax.set_title('Perfil de tensión — carga vs vacío'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax = axes[1, 0]
    L_arr = np.linspace(10, 500, 200)
    P_termico = 500 * np.ones_like(L_arr)
    P_estab = 1000 / (0.01*L_arr + 0.3)
    P_cargable = np.minimum(P_termico, P_estab)
    P_SIL = 300 * np.ones_like(L_arr)
    ax.plot(L_arr, P_termico, 'r-', lw=2, label='Límite térmico')
    ax.plot(L_arr, P_estab, 'b-', lw=2, label='Límite estabilidad')
    ax.plot(L_arr, P_SIL, 'g--', lw=2, label='SIL (natural)')
    ax.fill_between(L_arr, 0, P_cargable, alpha=0.2, color='green', label='Zona operable')
    ax.set_xlabel('Longitud (km)'); ax.set_ylabel('Potencia (MW)')
    ax.set_title('Diagrama de cargabilidad'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax = axes[1, 1]
    L_ferranti = np.linspace(0, 300, 200)
    beta = 2*np.pi*50 / 3e8
    with np.errstate(divide='ignore', invalid='ignore'):
        cos_aereo = np.cos(beta * L_ferranti * 1000)
        V_ferranti_aereo = np.where(np.abs(cos_aereo) > 1e-6, 1/cos_aereo, np.nan)
    beta_cable = beta * 3
    with np.errstate(divide='ignore', invalid='ignore'):
        cos_cable = np.cos(beta_cable * L_ferranti * 1000)
        V_ferranti_cable = np.where(np.abs(cos_cable) > 1e-6, 1/cos_cable, np.nan)
    ax.plot(L_ferranti, np.clip((V_ferranti_aereo-1)*100, 0, 20), 'b-', lw=2, label='Línea aérea')
    ax.plot(L_ferranti, np.clip((V_ferranti_cable-1)*100, 0, 20), 'r-', lw=2, label='Cable submarino')
    ax.axhline(5, color='gray', ls='--', label='Límite +5%')
    ax.set_xlabel('Longitud (km)'); ax.set_ylabel('ΔV Ferranti (%)')
    ax.set_title('Efecto Ferranti: aérea vs cable'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    fig.suptitle('Modelo de línea de distribución: π, cargabilidad y Ferranti', fontsize=14, fontweight='bold')
    plt.tight_layout(); _savefig(fig, "modelo-linea-distribucion-analisis")


def _metodos_sintesis_control_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    ax = axes[0, 0]
    # Lugar de raíces simplificado: planta 1/(s(s+2))
    sigma = np.linspace(-5, 1, 300)
    # Ramas del lugar
    ax.axvline(-1, color='gray', ls=':', lw=1)
    t_rl = np.linspace(0, 4, 200)
    branch1_re = -1 - t_rl; branch1_im = t_rl
    branch2_re = -1 - t_rl; branch2_im = -t_rl
    ax.plot(branch1_re, branch1_im, 'b-', lw=2, label='Lugar K>0')
    ax.plot(branch2_re, branch2_im, 'b-', lw=2)
    ax.plot([0, -2], [0, 0], 'rx', markersize=10, label='Polos OL')
    ax.plot(-1, 0, 'go', markersize=10, label='Centrode')
    ax.axhline(0, color='k', lw=0.5); ax.axvline(0, color='k', lw=0.5)
    ax.set_xlim([-6, 1]); ax.set_ylim([-5, 5])
    ax.set_xlabel('Re'); ax.set_ylabel('Im')
    ax.set_title('Lugar de raíces: 1/[s(s+2)]'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax = axes[0, 1]
    f = np.logspace(-1, 4, 500)
    w = 2*np.pi*f
    wc = 2*np.pi*1000; L = 2e-3; R = 0.1
    Kp = L*wc; Ki = R*wc
    G = 1/(1j*w*L + R)
    C = Kp + Ki/(1j*w)
    L_loop = C*G
    ax.semilogx(f, 20*np.log10(np.abs(L_loop)), 'b-', lw=2, label='|L(jω)| dB')
    ax.axhline(0, color='r', ls='--', lw=1, label='0 dB')
    ax.axvline(1000, color='g', ls=':', lw=1.5, label=f'fc=1 kHz')
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Magnitud (dB)')
    ax.set_title('Loop shaping: lazo de corriente PI'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax = axes[1, 0]
    f2 = np.logspace(1, 4, 500); w2 = 2*np.pi*f2
    wb = 2*np.pi*200; Ms = 2; eps = 0.01
    W1 = np.abs((1j*w2/Ms + wb)/(1j*w2 + wb*eps))
    wt = 2*np.pi*3000; Mt = 1.25
    W2 = np.abs((1j*w2 + wt/np.sqrt(Mt))/(np.sqrt(Mt)*1j*w2 + wt))
    ax.semilogx(f2, 20*np.log10(W1), 'b-', lw=2, label='W1 (plantilla S)')
    ax.semilogx(f2, 20*np.log10(W2), 'r-', lw=2, label='W2 (plantilla T)')
    ax.axhline(0, color='gray', ls=':', lw=1)
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Magnitud (dB)')
    ax.set_title('Pesos W1/W2 para diseño H-inf'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax = axes[1, 1]; ax.axis('off')
    tabla = [
        ['Método', 'Tipo', 'Robustez', 'Complejidad'],
        ['Bode/PI', 'SISO clás.', 'PM/GM empír.', 'Baja'],
        ['Lugar raíces', 'SISO anál.', 'No explicit.', 'Baja'],
        ['SIMC/ZN', 'Empírico', 'No', 'Muy baja'],
        ['LQR/LQG', 'Esp.estado', 'No directa', 'Media'],
        ['H-inf', 'Ópt.robusto', 'Sí (||S||)', 'Alta'],
        ['MPC', 'Predictivo', 'No estándar', 'Muy alta'],
    ]
    table = ax.table(cellText=tabla[1:], colLabels=tabla[0],
                     cellLoc='center', loc='center', bbox=[0, 0, 1, 1])
    table.auto_set_font_size(False); table.set_fontsize(9)
    ax.set_title('Tabla comparativa de métodos')
    fig.suptitle('Métodos de síntesis de control: lugar de raíces, loop shaping, pesos H-inf', fontsize=13, fontweight='bold')
    plt.tight_layout(); _savefig(fig, "metodos-sintesis-control-analisis")


def _arquitecturas_control_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    ax = axes[0, 0]; ax.axis('off')
    props = dict(boxstyle='round', facecolor='lightyellow', alpha=0.8)
    ax.text(0.5, 0.9, 'Arquitectura GFM — Cascada', ha='center', fontsize=12, fontweight='bold', transform=ax.transAxes)
    capas = ['Lazo corriente\n(1 kHz, PI + AD)', 'Lazo tensión\n(200 Hz, PI + FF)', 'Sincronización\n(PSC/VSM, ~40 Hz)', 'Despacho\n(<1 Hz, P*/Q*)']
    for i, cap in enumerate(capas):
        ax.text(0.5, 0.72-i*0.18, cap, ha='center', va='center', fontsize=10,
                bbox=props, transform=ax.transAxes)
        if i < len(capas)-1:
            ax.annotate('', xy=(0.5, 0.73-i*0.18-0.08), xytext=(0.5, 0.73-i*0.18-0.01),
                        xycoords='axes fraction', textcoords='axes fraction',
                        arrowprops=dict(arrowstyle='->', color='gray'))
    ax.set_title('Capas de control GFM')
    ax = axes[0, 1]
    t = np.linspace(0, 0.02, 1000)
    # Respuesta ante perturbación con y sin feedforward
    wc = 2*np.pi*200; wd = 2*np.pi*50
    y_noff = 1 - np.exp(-wc*t)*(np.cos(wd*t) + wc/wd*np.sin(wd*t))
    tau_ff = 0.002
    y_ff = 1 - np.exp(-wc*t)*np.exp(-t/tau_ff)
    ax.plot(t*1000, np.clip(y_noff, -0.5, 1.5), 'r-', lw=2, label='Sin feedforward')
    ax.plot(t*1000, np.clip(y_ff, -0.5, 1.5), 'b-', lw=2, label='Con feedforward')
    ax.axhline(1, color='gray', ls=':', lw=1)
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Tensión (pu)')
    ax.set_title('Efecto del feedforward de tensión de red'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax = axes[1, 0]
    f = np.logspace(1, 4, 300); w = 2*np.pi*f
    wci = 2*np.pi*1000; wcv = 2*np.pi*200; wcf = 2*np.pi*40
    Li = wci/(1j*w + wci)
    Lv = wcv/(1j*w + wcv)
    Lf = wcf/(1j*w + wcf)
    ax.semilogx(f, 20*np.log10(np.abs(Li)), 'b-', lw=2, label='Lazo corriente (1 kHz)')
    ax.semilogx(f, 20*np.log10(np.abs(Lv)), 'g-', lw=2, label='Lazo tensión (200 Hz)')
    ax.semilogx(f, 20*np.log10(np.abs(Lf)), 'r-', lw=2, label='Lazo PSC (40 Hz)')
    ax.axhline(-3, color='gray', ls=':', lw=1, label='-3 dB')
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Ganancia (dB)')
    ax.set_title('Separación de escalas: 3 lazos'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax = axes[1, 1]; ax.axis('off')
    tabla = [
        ['Arquitectura', 'Lazos', 'Aplicación', 'Complejidad'],
        ['1-DOF PI', '1', 'SISO básico', 'Baja'],
        ['Cascada', '2-3 anidados', 'Convertidor', 'Media'],
        ['2-DOF', '1+prefiltro', 'Seguimiento', 'Media'],
        ['FF+cascada', '2+FF', 'GFM estándar', 'Media-alta'],
        ['MPC centraliz.', '1 global', 'Microrred', 'Muy alta'],
        ['RL adaptativo', 'Aprendizaje', 'No lineal', 'Muy alta'],
    ]
    table = ax.table(cellText=tabla[1:], colLabels=tabla[0],
                     cellLoc='center', loc='center', bbox=[0, 0, 1, 1])
    table.auto_set_font_size(False); table.set_fontsize(9)
    ax.set_title('Tabla comparativa de arquitecturas')
    fig.suptitle('Arquitecturas de control: cascada, feedforward, separación de escalas', fontsize=13, fontweight='bold')
    plt.tight_layout(); _savefig(fig, "arquitecturas-control-analisis")


def _control_robusto_hinf_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    f = np.logspace(1, 4, 500); w = 2*np.pi*f
    wb = 2*np.pi*200; Ms = 2; eps = 0.01
    wt = 2*np.pi*3000; Mt = 1.25
    W1 = np.abs((1j*w/Ms + wb)/(1j*w + wb*eps))
    W2 = np.abs((1j*w + wt/np.sqrt(Mt))/(np.sqrt(Mt)*1j*w + wt))
    ax = axes[0, 0]
    ax.semilogx(f, 20*np.log10(W1), 'b-', lw=2, label='|W1(jω)| (plantilla 1/S)')
    ax.semilogx(f, 20*np.log10(1/W1), 'b--', lw=1, alpha=0.5, label='|1/W1| = plantilla S')
    ax.semilogx(f, 20*np.log10(W2), 'r-', lw=2, label='|W2(jω)| (plantilla 1/T)')
    ax.semilogx(f, 20*np.log10(1/W2), 'r--', lw=1, alpha=0.5, label='|1/W2| = plantilla T')
    ax.axhline(0, color='gray', ls=':', lw=1)
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Magnitud (dB)')
    ax.set_title('Pesos W1/W2 y plantillas S/T'); ax.legend(fontsize=7); ax.grid(True, alpha=0.3)
    ax = axes[0, 1]
    # S y T con y sin H-inf (aproximaciones)
    wc = 2*np.pi*1000; L_pi = (1 + 1j*w/wc)  # lazo PI simplificado
    S_pi = 1/(1 + L_pi); T_pi = L_pi/(1 + L_pi)
    L_hinf = (1 + 1j*w/wc) * (1 + 1j*w/(2*np.pi*500))  # simula controlador H-inf con más ganancia
    S_hinf = 1/(1 + L_hinf); T_hinf = L_hinf/(1 + L_hinf)
    ax.semilogx(f, 20*np.log10(np.abs(S_pi)), 'b-', lw=2, label='S — PI clásico')
    ax.semilogx(f, 20*np.log10(np.abs(S_hinf)), 'b--', lw=2, label='S — H-inf')
    ax.semilogx(f, 20*np.log10(np.abs(T_pi)), 'r-', lw=2, label='T — PI clásico')
    ax.semilogx(f, 20*np.log10(np.abs(T_hinf)), 'r--', lw=2, label='T — H-inf')
    ax.axhline(0, color='gray', ls=':', lw=1)
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Magnitud (dB)')
    ax.set_title('Funciones S/T: PI vs H-inf'); ax.legend(fontsize=7); ax.grid(True, alpha=0.3)
    ax = axes[1, 0]
    # Incertidumbre multiplicativa de Lgrid
    L_nom = 1e-3; L_vals = [0.5e-3, 1e-3, 2e-3, 4e-3]
    R = 0.1
    for Lv in L_vals:
        G_nom = 1/(1j*w*L_nom + R)
        G_var = 1/(1j*w*Lv + R)
        dm = np.abs((G_var - G_nom)/G_nom)
        ax.semilogx(f, 20*np.log10(dm + 1e-6), lw=1.5, label=f'L={Lv*1e3:.1f}mH')
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('|Δm| (dB)')
    ax.set_title('Incertidumbre multiplicativa: variación L_grid'); ax.legend(fontsize=7); ax.grid(True, alpha=0.3)
    ax = axes[1, 1]
    L_arr = np.array([0.25, 0.5, 1.0, 2.0, 4.0]) * L_nom
    PM_pi = np.array([58, 52, 45, 28, 12])
    PM_hinf = np.array([48, 44, 42, 38, 32])
    ax.plot(L_arr*1e3, PM_pi, 'b-o', lw=2, label='PM — PI clásico')
    ax.plot(L_arr*1e3, PM_hinf, 'r-s', lw=2, label='PM — H-inf')
    ax.axhline(30, color='gray', ls='--', label='PM mínimo (30°)')
    ax.set_xlabel('L_grid (mH)'); ax.set_ylabel('Margen de fase (°)')
    ax.set_title('Robustez PM vs variación de L_grid'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    fig.suptitle('Control robusto H∞: pesos, S/T, incertidumbre y margen de fase', fontsize=13, fontweight='bold')
    plt.tight_layout(); _savefig(fig, "control-robusto-hinf-analisis")


def _antiresonancia_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import signal
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    L1=2e-3; L2=0.5e-3; Cf=10e-6; R1=0.05; R2=0.05
    w = 2*np.pi*np.logspace(1, 5, 2000)
    # i1/vi: numerador (1 + s^2*L2*Cf)
    # i2/vi: sin antiresonancia
    s = 1j*w
    D = s**3*L1*L2*Cf + s**2*(R1*L2*Cf+R2*L1*Cf) + s*(L1+L2+R1*R2*Cf) + (R1+R2)
    N1 = s**2*L2*Cf + s*R2*Cf + 1
    N2 = np.ones_like(s)
    H1 = N1/D; H2 = N2/D
    f_hz = w/(2*np.pi)
    ax = axes[0, 0]
    ax.semilogx(f_hz, 20*np.log10(np.abs(H1)+1e-10), 'r-', lw=2, label='i1/vi (con antiresonancia)')
    ax.semilogx(f_hz, 20*np.log10(np.abs(H2)+1e-10), 'b-', lw=2, label='i2/vi (sin antiresonancia)')
    f_ar = 1/(2*np.pi*np.sqrt(L2*Cf))
    f_res = 1/(2*np.pi)*np.sqrt((L1+L2)/(L1*L2*Cf))
    ax.axvline(f_ar, color='r', ls=':', lw=1.5, label=f'f_ar={f_ar:.0f}Hz')
    ax.axvline(f_res, color='b', ls=':', lw=1.5, label=f'f_res={f_res:.0f}Hz')
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Magnitud (dB)')
    ax.set_title('Bode: i1/vi vs i2/vi'); ax.legend(fontsize=7); ax.grid(True, alpha=0.3)
    ax = axes[0, 1]
    ax.semilogx(f_hz, np.degrees(np.angle(H1)), 'r-', lw=2, label='∠(i1/vi)')
    ax.semilogx(f_hz, np.degrees(np.angle(H2)), 'b-', lw=2, label='∠(i2/vi)')
    ax.axvline(f_ar, color='r', ls=':', lw=1.5)
    ax.axvline(f_res, color='b', ls=':', lw=1.5)
    ax.axhline(-180, color='gray', ls='--', lw=1)
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Fase (°)')
    ax.set_title('Fase: repunte de +180° en f_ar'); ax.legend(fontsize=7); ax.grid(True, alpha=0.3)
    ax = axes[1, 0]
    # Admitancia del paralelo Cf||L2
    Y_par = s*Cf + 1/(s*L2+R2)
    ax.semilogx(f_hz, 20*np.log10(np.abs(Y_par)+1e-10), 'g-', lw=2, label='|Y_par(Cf||L2)|')
    ax.axvline(f_ar, color='r', ls=':', lw=1.5, label=f'f_ar={f_ar:.0f}Hz (mínimo)')
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Admitancia (dB S)')
    ax.set_title('Admitancia Cf||L2: mínimo en f_ar'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax = axes[1, 1]
    # Ratio fres/far vs L2/L1
    r_arr = np.linspace(0.1, 2, 100)
    ratio = np.sqrt(1 + r_arr)
    ax.plot(r_arr, ratio, 'b-', lw=2, label='f_res/f_ar = √(1+L2/L1)')
    ax.axhline(1, color='gray', ls=':', lw=1)
    ax.scatter([L2/L1], [np.sqrt(1+L2/L1)], color='red', s=100, zorder=5, label=f'Proyecto: L2/L1={L2/L1:.2f}')
    ax.set_xlabel('r = L2/L1'); ax.set_ylabel('f_res/f_ar')
    ax.set_title('Ratio resonancia/antiresonancia vs L2/L1'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    fig.suptitle('Antiresonancia en filtro LCL: Bode, admitancia y ratio f_res/f_ar', fontsize=13, fontweight='bold')
    plt.tight_layout(); _savefig(fig, "antiresonancia-analisis")


def _amortiguamiento_pasivo_vs_activo_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    L1=2e-3; L2=0.5e-3; Cf=10e-6; R1=0.05; R2=0.05
    w = 2*np.pi*np.logspace(1, 5, 2000)
    s = 1j*w
    w_res = np.sqrt((L1+L2)/(L1*L2*Cf))
    Rd_opt = 1/(3*w_res*Cf)
    Kad = Rd_opt
    def lcl_i2vi(Rd_series=0, Kad_virt=0):
        # Rd en serie con Cf; Kad actúa como R en L1
        Ztotal = (s*L1 + R1 + Kad_virt) + 1/(s*Cf + 1/(Rd_series + 1e-10) if Rd_series > 0 else s*Cf)
        # Simplificación: transferencia i2/vi analítica con amortiguamiento
        R_eff = R1 + Kad_virt; Rd_cf = Rd_series
        D = s**3*L1*L2*Cf + s**2*(R_eff*L2*Cf + (R2+Rd_cf)*L1*Cf + R_eff*(R2+Rd_cf)*Cf) + \
            s*(L1+L2+(R_eff*(R2+Rd_cf))*Cf) + (R_eff+R2+Rd_cf)
        N = 1
        return N/D
    H_nodam = lcl_i2vi(0, 0)
    H_pasivo = lcl_i2vi(Rd_opt, 0)
    H_activo = lcl_i2vi(0, Kad)
    f_hz = w/(2*np.pi)
    ax = axes[0, 0]
    ax.semilogx(f_hz, 20*np.log10(np.abs(H_nodam)+1e-10), 'gray', lw=1.5, ls='--', label='Sin amortiguamiento')
    ax.semilogx(f_hz, 20*np.log10(np.abs(H_pasivo)+1e-10), 'r-', lw=2, label=f'Pasivo Rd={Rd_opt:.1f}Ω')
    ax.semilogx(f_hz, 20*np.log10(np.abs(H_activo)+1e-10), 'b-', lw=2, label=f'Activo Kad={Kad:.1f}Ω')
    ax.set_ylim([-80, 20]); ax.axhline(0, color='k', ls=':', lw=0.5)
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Magnitud (dB)')
    ax.set_title('Bode i2/vi: sin dam., pasivo y activo'); ax.legend(fontsize=7); ax.grid(True, alpha=0.3)
    ax = axes[0, 1]
    Rd_arr = np.linspace(0.1, 20, 200)
    Q_arr = 1/(Rd_arr * Cf * w_res)
    ax.plot(Rd_arr, Q_arr, 'b-', lw=2)
    ax.axhline(3, color='r', ls='--', label='Q=3 (Rd óptimo)')
    ax.axvline(Rd_opt, color='g', ls=':', lw=1.5, label=f'Rd_opt={Rd_opt:.1f}Ω')
    ax.set_xlabel('Rd (Ω)'); ax.set_ylabel('Factor Q')
    ax.set_title('Factor de calidad Q vs Rd'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax = axes[1, 0]
    Icf_rms_arr = np.linspace(0, 10, 100)
    for Rd_val, col, lab in [(Rd_opt, 'r', f'Rd={Rd_opt:.1f}Ω'), (Rd_opt/3, 'orange', f'Rd={Rd_opt/3:.1f}Ω')]:
        P_arr = Rd_val * Icf_rms_arr**2
        ax.plot(Icf_rms_arr, P_arr, color=col, lw=2, label=f'Pasivo {lab}')
    ax.axhline(0, color='b', lw=2, label='Activo (0 W)')
    ax.set_xlabel('I_Cf,rms (A)'); ax.set_ylabel('Pérdidas (W)')
    ax.set_title('Pérdidas en R_d vs corriente de Cf'); ax.legend(fontsize=7); ax.grid(True, alpha=0.3)
    ax = axes[1, 1]
    # PM del lazo de corriente vs Kad
    Kad_arr = np.linspace(0, 5*Rd_opt, 50)
    PM_arr = np.zeros(len(Kad_arr))
    wc_target = 2*np.pi*500
    for ki, Kd in enumerate(Kad_arr):
        w_sweep = np.logspace(2, 4, 2000)
        s2 = 1j*w_sweep
        D2 = s2**3*L1*L2*Cf + s2**2*((R1+Kd)*L2*Cf + R2*L1*Cf) + s2*(L1+L2) + (R1+Kd+R2)
        H_ad = 1/D2
        mag = np.abs(H_ad)
        idx = np.argmin(np.abs(mag - mag[0]*wc_target/w_sweep[0]))
        PM_arr[ki] = 180 + np.degrees(np.angle(H_ad[idx]))
    ax.plot(Kad_arr, np.clip(PM_arr, 0, 90), 'b-', lw=2)
    ax.axhline(45, color='r', ls='--', label='PM objetivo=45°')
    ax.axvline(Rd_opt, color='g', ls=':', lw=1.5, label=f'Kad_opt={Rd_opt:.1f}Ω')
    ax.set_xlabel('Kad (Ω)'); ax.set_ylabel('Margen de fase (°)')
    ax.set_title('PM del lazo de corriente vs Kad (AD activo)'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    fig.suptitle('Amortiguamiento pasivo vs activo: Bode, Q, pérdidas y margen de fase', fontsize=13, fontweight='bold')
    plt.tight_layout(); _savefig(fig, "amortiguamiento-pasivo-vs-activo-analisis")


def _aerogenerador_pmsg_dfig_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Panel 1: curva T-omega PMSG con MPPT y zona de potencia constante
    ax = axes[0, 0]
    omega = np.linspace(0.3, 1.3, 200)
    Kopt = 0.5; Trated = 1.0
    T_mppt = Kopt * omega**2
    T_rated = np.minimum(T_mppt, Trated)
    P_out = T_rated * omega
    ax.plot(omega, T_mppt, 'b-', lw=2, label='Par MPPT ($K_{opt}\\omega^2$)')
    ax.plot(omega, T_rated, 'r-', lw=2, label='Par limitado')
    ax.plot(omega, P_out, 'g--', lw=2, label='Potencia (pu)')
    ax.axvline(1.0, color='gray', ls=':', label='$\\omega$ nominal')
    ax.axhline(Trated, color='orange', ls=':', label='T nominal')
    ax.set_xlabel('$\\omega$ rotor (pu)'); ax.set_ylabel('Par / Potencia (pu)')
    ax.set_title('PMSG: curva T-$\\omega$ y MPPT'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    # Panel 2: potencia en DFIG — estator vs rotor vs red
    ax = axes[0, 1]
    slip = np.linspace(-0.3, 0.3, 200)
    Ps = np.ones_like(slip)
    Pr_abs = np.abs(slip) * Ps
    Ptotal = Ps + np.where(slip < 0, -slip * Ps, slip * Ps)
    ax.plot(slip, Ps, 'b-', lw=2, label='P estator')
    ax.plot(slip, Pr_abs, 'r-', lw=2, label='|P rotor| (convertidor)')
    ax.plot(slip, Ptotal, 'g-', lw=2, label='P total red')
    ax.axvline(0, color='k', ls='--', alpha=0.5, label='Velocidad síncrona')
    ax.fill_between(slip, 0, Pr_abs, alpha=0.2, color='red', label='Potencia convertidor')
    ax.set_xlabel('Deslizamiento s'); ax.set_ylabel('Potencia (pu)')
    ax.set_title('DFIG: reparto de potencia estátor/rotor'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    # Panel 3: FRT — tensión y corriente durante hueco
    ax = axes[1, 0]
    t = np.linspace(0, 0.5, 1000)
    V_grid = np.ones(len(t))
    V_grid[(t > 0.1) & (t < 0.25)] = 0.15
    dV = 1 - V_grid
    Iq_frt = np.minimum(2 * dV, 1.1)
    Id_frt = np.sqrt(np.maximum(0, 1.1**2 - Iq_frt**2))
    crowbar = ((t > 0.1) & (t < 0.17)).astype(float)
    ax.plot(t * 1000, V_grid, 'b-', lw=2, label='V_red (pu)')
    ax.plot(t * 1000, Iq_frt, 'r-', lw=2, label='I_q reactiva (pu)')
    ax.plot(t * 1000, Id_frt, 'g-', lw=2, label='I_d activa (pu)')
    ax.fill_between(t * 1000, 0, crowbar * 0.5, alpha=0.3, color='orange', label='Crowbar activo (DFIG)')
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Amplitud (pu)')
    ax.set_title('FRT: tensión, corrientes y crowbar'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    # Panel 4: comparativa DFIG vs PMSG — barras de características
    ax = axes[1, 1]
    categories = ['FRT\nsencillo', 'Bajo\ncoste', 'Sin\nengranaje', 'Control\nQ pleno', 'Mant.\nbajo']
    DFIG_scores = [2, 5, 2, 3, 2]
    PMSG_scores = [5, 3, 5, 5, 5]
    x = np.arange(len(categories)); w = 0.35
    ax.bar(x - w / 2, DFIG_scores, w, label='DFIG', color='steelblue', alpha=0.8, edgecolor='black')
    ax.bar(x + w / 2, PMSG_scores, w, label='PMSG', color='seagreen', alpha=0.8, edgecolor='black')
    ax.set_xticks(x); ax.set_xticklabels(categories, fontsize=9)
    ax.set_ylabel('Puntuación (1–5)'); ax.set_title('Comparativa DFIG vs PMSG (offshore)')
    ax.legend(); ax.grid(True, alpha=0.3, axis='y'); ax.set_ylim([0, 6])

    fig.suptitle('Aerogenerador PMSG y DFIG: modelos, control y FRT', fontsize=14, fontweight='bold')
    plt.tight_layout()
    _savefig(fig, "aerogenerador-pmsg-dfig-analisis")


def _control_parque_eolico_offshore_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Panel 1: layout del parque y efecto estela
    ax = axes[0, 0]
    np.random.seed(42)
    rows = 5; cols = 6
    x_wt = np.repeat(np.arange(cols) * 5, rows)
    y_wt = np.tile(np.arange(rows) * 4, cols)
    v_inf = 12.0
    v_wt = np.array([v_inf * (1 - 0.08 * (x_wt[i] // 5)) for i in range(len(x_wt))])
    P_wt = np.clip((v_wt / 12)**3, 0, 1)
    sc = ax.scatter(x_wt, y_wt, c=P_wt, cmap='RdYlGn', s=200, vmin=0.5, vmax=1.0, zorder=5)
    plt.colorbar(sc, ax=ax, label='P/P_rated')
    ax.annotate('', xy=(25, 10), xytext=(-2, 10),
                arrowprops=dict(arrowstyle='->', color='blue', lw=2))
    ax.text(11, 10.8, 'Viento', color='blue', fontsize=10)
    ax.set_xlabel('Distancia (km)'); ax.set_ylabel('Distancia (km)')
    ax.set_title('Layout parque: efecto estela (color = P/Pnom)'); ax.grid(True, alpha=0.3)

    # Panel 2: FRT frequency-based — Vdc y frecuencia del parque
    ax = axes[0, 1]
    t = np.linspace(0, 2, 1000)
    V_ons = np.ones(len(t))
    V_ons[(t > 0.3) & (t < 0.7)] = 0.2
    Vdc = np.ones(len(t))
    f_park = 50 * np.ones(len(t))
    for i in range(1, len(t)):
        dt = t[1] - t[0]
        dP_out = (V_ons[i]**2 - 1.0) * 0.5
        Vdc[i] = Vdc[i - 1] + dt * (0.8 - Vdc[i - 1] * 0.5) * (-dP_out) * 2
        Vdc[i] = np.clip(Vdc[i], 0.9, 1.15)
        f_park[i] = 50 - 5 * (Vdc[i] - 1.0)
    ax.plot(t, V_ons, 'b-', lw=2, label='V_onshore (pu)')
    ax.plot(t, Vdc, 'r-', lw=2, label='V_dc (pu)')
    ax.plot(t, f_park / 50, 'g-', lw=2, label='f_parque / 50 Hz')
    ax.axhline(1.0, color='k', ls='--', alpha=0.3)
    ax.set_xlabel('Tiempo (s)'); ax.set_ylabel('Amplitud (pu)')
    ax.set_title('FRT frequency-based'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    # Panel 3: despacho de potencia activa — delta control vs MPPT
    ax = axes[1, 0]
    v_wind = np.linspace(4, 25, 200)
    Cp_max = 0.48; rho = 1.225; A = np.pi * 90**2
    P_mppt = np.minimum(0.5 * rho * A * Cp_max * v_wind**3 / 6e6, 1.0)
    P_delta = P_mppt * 0.9
    ax.plot(v_wind, P_mppt, 'b-', lw=2, label='MPPT (100 %)')
    ax.plot(v_wind, P_delta, 'r-', lw=2, label='Delta control (90 %)')
    ax.fill_between(v_wind, P_delta, P_mppt, alpha=0.3, color='green', label='Reserva regulación')
    ax.axvline(12, color='gray', ls=':', label='v_nom = 12 m/s')
    ax.set_xlabel('Velocidad del viento (m/s)'); ax.set_ylabel('P/P_rated')
    ax.set_title('Despacho: MPPT vs delta control'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    # Panel 4: servicios de red — respuesta FFR y droop
    ax = axes[1, 1]
    t2 = np.linspace(0, 30, 1000)
    df = -0.5 * (1 - np.exp(-t2 / 0.5)) + 0.3 * (1 - np.exp(-t2 / 10))
    ddf = np.gradient(df, t2)
    P_ffr = np.clip(-2 * 3 * ddf, -0.15, 0.15)
    P_droop = np.clip(-df / 0.02, -0.15, 0.15)
    ax.plot(t2, df, 'k-', lw=2, label='$\\Delta f$ (Hz)')
    ax.plot(t2, P_ffr, 'b-', lw=2, label='FFR (inercia virtual)')
    ax.plot(t2, P_droop, 'r-', lw=2, label='Droop R = 2 %')
    ax.axhline(0, color='k', ls='--', alpha=0.3)
    ax.set_xlabel('Tiempo (s)'); ax.set_ylabel('Amplitud (pu / Hz)')
    ax.set_title('Servicios de red: FFR y droop'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    fig.suptitle('Parque eólico offshore: arquitectura, FRT, despacho y servicios', fontsize=14, fontweight='bold')
    plt.tight_layout()
    _savefig(fig, "control-parque-eolico-offshore-analisis")


def _red_thevenin_scr_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    ax = axes[0, 0]; ax.axis('off')
    items = [('V_th\n(Red ideal)', 0.1, 0.5, 'lightyellow'),
             ('Z_th = R+jX', 0.4, 0.5, 'lightblue'),
             ('PCC', 0.65, 0.5, 'lightgreen'),
             ('Convertidor\nVSC', 0.88, 0.5, 'lightsalmon')]
    for label, x, y, col in items:
        ax.add_patch(FancyBboxPatch((x-0.08, y-0.12), 0.16, 0.24,
                     boxstyle='round,pad=0.02', facecolor=col, edgecolor='navy'))
        ax.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold')
    for i in range(len(items)-1):
        ax.annotate('', xy=(items[i+1][1]-0.08, 0.5), xytext=(items[i][1]+0.08, 0.5),
                    arrowprops=dict(arrowstyle='-', color='navy', lw=2))
    ax.text(0.5, 0.18, 'SCR = S_cc / P_conv', ha='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='wheat'))
    ax.set_xlim([0, 1]); ax.set_ylim([0, 1]); ax.set_title('Equivalente Thevenin del PCC')
    ax = axes[0, 1]
    SCR = np.linspace(1, 15, 200)
    Xth = 1.0 / SCR
    ax.plot(SCR, Xth, 'b-', lw=2)
    ax.axvspan(1, 2, alpha=0.15, color='red', label='Red debil SCR<2')
    ax.axvspan(2, 5, alpha=0.1, color='orange', label='Red media')
    ax.axvspan(5, 15, alpha=0.1, color='green', label='Red fuerte SCR>5')
    ax.set_xlabel('SCR'); ax.set_ylabel('X_th (pu)')
    ax.set_title('Reactancia Thevenin vs SCR'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax = axes[1, 0]
    scr_arr = np.linspace(1, 10, 200)
    bw_max = (scr_arr - 1) * 5
    bw_nom = 20 * np.ones_like(scr_arr)
    ax.plot(scr_arr, bw_max, 'r-', lw=2, label='BW_PLL maximo estable')
    ax.plot(scr_arr, bw_nom, 'b--', lw=2, label='BW_PLL nominal (20Hz)')
    ax.fill_between(scr_arr, 0, bw_max, alpha=0.1, color='green', label='Zona estable')
    ax.axvline(1.5, color='gray', ls=':', label='SCR=1.5 (limite GFL)')
    ax.set_xlabel('SCR'); ax.set_ylabel('BW_PLL (Hz)')
    ax.set_title('Estabilidad PLL vs SCR'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax.set_ylim([0, 60])
    ax = axes[1, 1]
    topologias = ['N\n(normal)', 'N-1\n(linea)', 'N-1\n(trafo)', 'N-2\n(doble)']
    scr_vals = [5.0, 2.8, 3.5, 1.4]
    colors = ['green' if s > 3 else 'orange' if s > 2 else 'red' for s in scr_vals]
    ax.bar(topologias, scr_vals, color=colors, edgecolor='black', alpha=0.8)
    ax.axhline(2, color='r', ls='--', label='Limite SCR=2')
    ax.axhline(5, color='g', ls='--', label='SCR=5 (fuerte)')
    ax.set_ylabel('SCR efectivo'); ax.set_title('SCR segun contingencia de red')
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3, axis='y')
    fig.suptitle('Red Thevenin y SCR: impedancia, estabilidad y contingencias', fontsize=14, fontweight='bold')
    plt.tight_layout(); _savefig(fig, 'red-thevenin-scr-analisis')


def _armonicos_thd_convertidores_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    ax = axes[0, 0]
    f0 = 50; fs_sw = 10000
    f_arr = np.array([f0*h for h in [1, 3, 5, 7]] +
                     [fs_sw+k*f0 for k in [-3, -1, 1, 3]] +
                     [2*fs_sw+k*f0 for k in [-1, 1]])
    amp_arr = np.array([1.0, 0.05, 0.03, 0.02, 0.15, 0.2, 0.2, 0.15, 0.08, 0.08])
    bar_cols = ['blue']+['red']*3+['green']*4+['orange']*2
    ax.bar(f_arr/1000, amp_arr*100, width=0.15, color=bar_cols, edgecolor='black', alpha=0.8)
    ax.set_xlabel('Frecuencia (kHz)'); ax.set_ylabel('Amplitud (% fundamental)')
    ax.set_title('Espectro corriente PWM'); ax.grid(True, alpha=0.3, axis='y')
    ax.set_yscale('log')
    ax = axes[0, 1]
    t = np.linspace(0, 0.04, 4000)
    i_fund = np.sin(2*np.pi*50*t)
    i_with_dt = i_fund + 0.03*np.sin(2*np.pi*250*t) + 0.02*np.sin(2*np.pi*350*t)
    ax.plot(t*1000, i_fund, 'b--', lw=1.5, label='Sin dead time')
    ax.plot(t*1000, i_with_dt, 'r-', lw=1.5, label='Con dead time (2us)')
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Corriente (pu)')
    ax.set_title('Efecto del dead time'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax.set_xlim([0, 20])
    ax = axes[1, 0]
    SCR_levels = ['<20', '20-50', '50-100', '>100']
    limits_thd = [5, 8, 10, 12]
    thd_measured = [3.2, 4.1, 5.8, 2.9]
    x = np.arange(len(SCR_levels)); ww = 0.35
    ax.bar(x-ww/2, limits_thd, ww, label='Limite IEEE 519', color='red', alpha=0.6, edgecolor='black')
    ax.bar(x+ww/2, thd_measured, ww, label='THD medido', color='blue', alpha=0.7, edgecolor='black')
    ax.set_xticks(x); ax.set_xticklabels([f'SCR\n{s}' for s in SCR_levels])
    ax.set_ylabel('THD_I (%)'); ax.set_title('IEEE 519: limites vs medido')
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3, axis='y')
    ax = axes[1, 1]
    f = np.logspace(1, 4, 500); w2 = 2*np.pi*f
    Lg = 1e-3; Cf = 100e-6
    f_res = 1/(2*np.pi*np.sqrt(Lg*Cf))
    Z_par = np.abs(1j*w2*Lg * (1/(1j*w2*Cf)) / (1j*w2*Lg + 1/(1j*w2*Cf)))
    ax.loglog(f, Z_par, 'b-', lw=2)
    ax.axvline(f_res, color='r', ls='--', lw=2, label=f'f_res={f_res:.0f}Hz')
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Impedancia (Ohm)')
    ax.set_title('Resonancia paralela Lg-Cf'); ax.legend(); ax.grid(True, alpha=0.3)
    fig.suptitle('Armonicos en convertidores: PWM, dead time, normas y resonancia', fontsize=14, fontweight='bold')
    plt.tight_layout(); _savefig(fig, 'armonicos-thd-convertidores-analisis')


def _control_tension_bus_dc_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    ax = axes[0, 0]
    t = np.linspace(0, 0.5, 1000)
    Cdc = 0.01; wcv = 400.0
    Vdc_pert = np.ones_like(t)
    Vdc_pert[t > 0.1] = 1 - 0.05*np.exp(-(t[t > 0.1]-0.1)*wcv) * np.cos(wcv*(t[t > 0.1]-0.1))
    Vdc_no = np.ones_like(t)
    Vdc_no[t > 0.1] = 1 - 0.3*(1-np.exp(-(t[t > 0.1]-0.1)*5))
    ax.plot(t*1000, Vdc_pert, 'b-', lw=2, label='Con control Vdc')
    ax.plot(t*1000, Vdc_no, 'r--', lw=2, label='Sin control')
    ax.axhline(1.0, color='k', ls=':', alpha=0.5); ax.axvline(100, color='gray', ls=':')
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Vdc (pu)')
    ax.set_title('Respuesta Vdc ante perturbacion de carga'); ax.legend(); ax.grid(True, alpha=0.3)
    ax = axes[0, 1]
    w = np.logspace(0, 4, 500); s = 1j*w
    Kp = Cdc*wcv/2; Ti = 10/wcv
    G_v = 2/(Cdc*s); C_v = Kp*(1+1/(Ti*s))
    L_v = C_v*G_v; T_v = L_v/(1+L_v)
    ax.semilogx(w, 20*np.log10(np.abs(T_v)), 'b-', lw=2, label='|T_v| lazo cerrado')
    ax.semilogx(w, 20*np.log10(np.abs(L_v)), 'r--', lw=1.5, label='|L_v| lazo abierto')
    ax.axhline(-3, color='gray', ls=':', alpha=0.7)
    ax.axvline(wcv, color='green', ls=':', label=f'wcv={wcv:.0f}')
    ax.set_xlabel('omega (rad/s)'); ax.set_ylabel('dB')
    ax.set_title('Bode del lazo de tension DC'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax = axes[1, 0]
    f = np.logspace(0, 4, 500); w3 = 2*np.pi*f
    Ls = 1e-3; Rs = 0.1; Cs_cap = 1e-3
    Zo = np.sqrt(Rs**2+(w3*Ls)**2) / np.sqrt(1+(w3*Rs*Cs_cap)**2)
    Z_cpl = 1.0
    ax.loglog(f, Zo, 'b-', lw=2, label='|Z_source|')
    ax.axhline(Z_cpl, color='r', ls='--', lw=2, label=f'|Z_CPL|={Z_cpl:.1f}Ohm')
    ax.fill_between(f, Zo, Z_cpl, where=Zo < Z_cpl, alpha=0.2, color='green', label='Middlebrook OK')
    ax.fill_between(f, Zo, Z_cpl, where=Zo > Z_cpl, alpha=0.2, color='red', label='Riesgo')
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Impedancia (Ohm)')
    ax.set_title('Criterio Middlebrook CPL'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax = axes[1, 1]
    Vdc_arr = np.linspace(0.92, 1.02, 200)
    for Rd, P0, col, lab in [(0.05, 0.0, 'b', 'Conv. 1 (Rd=0.05)'),
                              (0.08, 0.1, 'r', 'Conv. 2 (Rd=0.08)'),
                              (0.03, -0.1, 'g', 'Conv. 3 (Rd=0.03)')]:
        I = (Vdc_arr - 1.0 + P0) / Rd
        ax.plot(Vdc_arr, I, color=col, lw=2, label=lab)
    ax.axvline(1.0, color='k', ls='--', alpha=0.5, label='Vdc nominal')
    ax.axhline(0, color='k', lw=0.5)
    ax.set_xlabel('Vdc (pu)'); ax.set_ylabel('Corriente aportada (pu)')
    ax.set_title('Droop DC: reparto entre convertidores'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    fig.suptitle('Control del bus DC: lazo Vdc, CPL y droop', fontsize=14, fontweight='bold')
    plt.tight_layout(); _savefig(fig, 'control-tension-bus-dc-analisis')


def _btb_diagramas_bloques():
    """Diagramas de bloques del convertidor back-to-back:
    (1) lazo de corriente dq con desacoplo feedforward
    (2) lazo DC con feedforward de potencia
    """
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    # ------------------------------------------------------------------ #
    # Figura 1: lazo de corriente ÚNICO en dq (ambos ejes idénticos tras
    # el desacoplo; el subíndice dq representa d o q indistintamente)
    # ------------------------------------------------------------------ #
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    ax.set_xlim(0, 12); ax.set_ylim(0, 8); ax.axis('off')
    ax.set_title('Lazo de corriente en dq con desacoplo feedforward',
                 fontsize=13, fontweight='bold', pad=10)

    def box(x, y, w, h, label, color, fontsize=10):
        ax.add_patch(mpatches.FancyBboxPatch((x - w/2, y - h/2), w, h,
            boxstyle='round,pad=0.08', facecolor=color, edgecolor='navy', lw=1.6))
        ax.text(x, y, label, ha='center', va='center', fontsize=fontsize, fontweight='bold')

    def circle(x, y, label, r=0.32):
        ax.add_patch(plt.Circle((x, y), r, facecolor='white', edgecolor='navy', lw=1.6))
        ax.text(x, y, label, ha='center', va='center', fontsize=12, fontweight='bold')

    def arrow(x1, y1, x2, y2, label='', color='navy'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.8))
        if label:
            ax.text((x1+x2)/2, (y1+y2)/2+0.22, label, ha='center', va='bottom',
                    fontsize=9.5, color='darkred')

    yc = 4.6
    ax.text(0.35, yc, r'$i_{dq}^*$', ha='center', va='center', fontsize=12)
    arrow(0.7, yc, 1.35, yc)
    circle(1.7, yc, '−')
    arrow(2.05, yc, 2.9, yc, r'$e_{dq}$')
    box(3.6, yc, 1.3, 0.9, 'PI', '#AED6F1', 11)
    arrow(4.25, yc, 5.15, yc, r'$v_{dq,PI}$')
    circle(5.5, yc, '+')
    arrow(5.85, yc, 6.9, yc, r'$v_{dq,conv}^*$', color='darkred')
    box(7.7, yc, 1.4, 0.9, 'VSC\n+PWM', '#A9DFBF', 10)
    arrow(8.4, yc, 9.3, yc)
    box(10.1, yc, 1.3, 0.9, r'$\dfrac{1}{Ls+R}$', '#FAD7A0', 11)
    arrow(10.75, yc, 11.6, yc)
    ax.text(11.8, yc, r'$i_{dq}$', ha='center', va='center', fontsize=12)

    # realimentación
    ax.plot([11.35, 11.35, 1.7], [yc, yc-1.3, yc-1.3], 'navy', lw=1.7)
    ax.annotate('', xy=(1.7, yc-0.33), xytext=(1.7, yc-1.3),
                arrowprops=dict(arrowstyle='->', color='navy', lw=1.7))

    # feedforward tensión de red (verde, desde arriba)
    ax.text(5.5, yc+2.0, r'$+\,v_{dq,g}$  (tensión de red)', ha='center', va='center',
            fontsize=10, color='darkgreen')
    ax.annotate('', xy=(5.5, yc+0.33), xytext=(5.5, yc+1.75),
                arrowprops=dict(arrowstyle='->', color='darkgreen', lw=1.7))

    # feedforward desacoplo (naranja, desde abajo)
    ax.text(5.5, yc-2.15, r'$\mp\,\omega_0 L\, i_{qd}$  (desacoplo, desde el otro eje)',
            ha='center', va='center', fontsize=10, color='darkorange')
    ax.annotate('', xy=(5.5, yc-0.33), xytext=(5.5, yc-1.9),
                arrowprops=dict(arrowstyle='->', color='darkorange', lw=1.7))

    ax.text(6.0, 0.5,
            'Un solo lazo representa ambos ejes: tras el desacoplo, d y q son idénticos '
            r'($1/(Ls+R)$).' + '\nSigno del desacoplo: eje d usa $-\\omega_0 L i_q$; eje q usa $+\\omega_0 L i_d$.',
            ha='center', fontsize=9, color='gray')

    plt.tight_layout()
    _savefig(fig, "btb-diagramas-bloques", dpi=200)

    # --- Figura explicativa de tensiones ---
    fig2, ax3 = plt.subplots(1, 1, figsize=(12, 7))
    ax3.set_xlim(0, 12); ax3.set_ylim(0, 9); ax3.axis('off')
    ax3.set_title('Composición de la tensión de salida del convertidor — eje d',
                  fontsize=12, fontweight='bold', pad=10)

    def bx(x, y, w, h, txt, col):
        ax3.add_patch(mpatches.FancyBboxPatch((x-w/2, y-h/2), w, h,
            boxstyle='round,pad=0.1', facecolor=col, edgecolor='navy', lw=1.5))
        ax3.text(x, y, txt, ha='center', va='center', fontsize=10, fontweight='bold')

    def ar(x1, y1, x2, y2, lbl='', col='navy'):
        ax3.annotate('', xy=(x2, y2), xytext=(x1, y1),
                     arrowprops=dict(arrowstyle='->', color=col, lw=1.8))
        if lbl:
            ax3.text((x1+x2)/2+0.05, (y1+y2)/2+0.2, lbl, ha='center', fontsize=9, color=col)

    def circ(x, y, lbl):
        ax3.add_patch(plt.Circle((x, y), 0.32, facecolor='white', edgecolor='navy', lw=1.5))
        ax3.text(x, y, lbl, ha='center', va='center', fontsize=11, fontweight='bold')

    # Bloque PI
    bx(1.5, 5.5, 1.2, 0.8, 'PI\n(control)', '#AED6F1')
    ax3.text(0.2, 5.5, r'$e_d=i_d^*-i_d$', ha='center', va='center', fontsize=9)
    ar(0.7, 5.5, 0.9, 5.5)
    ar(2.1, 5.5, 2.8, 5.5, r'$v_{d,PI}$')

    # Suma principal
    circ(3.1, 5.5, '+')
    ar(3.42, 5.5, 4.5, 5.5, r'$v_{d,conv}^*$', col='darkred')

    # Bloque VSC
    bx(5.2, 5.5, 1.2, 0.8, 'VSC\n+PWM', '#A9DFBF')
    ar(5.8, 5.5, 6.7, 5.5, r'$v_{d,conv}$')

    # Nodo de tensión — resta v_grid
    circ(7.0, 5.5, '−')
    ar(7.32, 5.5, 8.1, 5.5)

    # Planta L, R
    bx(8.8, 5.5, 1.2, 0.8, r'$\frac{1}{Ls+R}$', '#FAD7A0')
    ar(9.4, 5.5, 10.3, 5.5, r'$i_d$')

    # v_red llega al nodo de resta
    ax3.text(7.0, 3.5, r'$v_{d,g}$ (tensión de red)', ha='center', va='center', fontsize=9, color='darkgreen')
    ar(7.0, 3.9, 7.0, 5.2, col='darkgreen')

    # Feedforward v_red al nodo suma
    ax3.text(3.1, 7.2, r'FF red: $+v_{d,g}$', ha='center', va='center', fontsize=9, color='darkgreen')
    ar(3.1, 6.95, 3.1, 5.82, col='darkgreen')

    # Feedforward desacoplo al nodo suma
    ax3.text(3.1, 1.8, r'FF desacoplo: $-\omega_0 L i_q$', ha='center', va='center', fontsize=9, color='darkorange')
    ar(3.1, 2.2, 3.1, 5.18, col='darkorange')

    # Anotaciones explicativas
    ax3.text(1.5, 4.0,
             r'$v_{d,PI}$: salida del PI'+'\n'
             r'Corrige el error $e_d = i_d^* - i_d$'+'\n'
             r'Varía lentamente (BW del PI)',
             ha='center', va='center', fontsize=8.5,
             bbox=dict(boxstyle='round', facecolor='#EBF5FB', edgecolor='#AED6F1'))

    ax3.text(9.7, 7.2,
             r'$v_{d,g}$: tensión de red (feedforward)'+'\n'
             r'Se conoce por medida directa'+'\n'
             r'Cancela el término $-v_{d,g}$ de la planta',
             ha='center', va='center', fontsize=8.5,
             bbox=dict(boxstyle='round', facecolor='#EAFAF1', edgecolor='darkgreen'))

    ax3.text(8.0, 2.5,
             r'$-\omega_0 L i_q$: feedforward de desacoplo'+'\n'
             r'Cancela el término físico $+\omega_0 L i_q$'+'\n'
             r'Elimina el acoplamiento cruzado d↔q',
             ha='center', va='center', fontsize=8.5,
             bbox=dict(boxstyle='round', facecolor='#FEF9E7', edgecolor='darkorange'))

    ax3.text(6.0, 8.5,
             r'$v_{d,conv}^* = v_{d,PI} + v_{d,g} - \omega_0 L i_q$',
             ha='center', va='center', fontsize=12, color='darkred', fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#FDEDEC', edgecolor='red', lw=1.5))

    plt.tight_layout()
    _savefig(fig2, "btb-tensiones-explicacion", dpi=200)


def _islanding_modos():
    """Diagrama de estados de la transicion GFL -> GFM al detectar islanding."""
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    fig, ax = plt.subplots(1, 1, figsize=(12, 4.6))
    ax.set_xlim(0, 12); ax.set_ylim(0, 5); ax.axis('off')
    ax.set_title('Lógica de modo: transición GFL → GFM al detectar islanding',
                 fontsize=12.5, fontweight='bold', pad=10)

    yc = 3.2

    def box(x, y, w, h, txt, col, fs=10):
        ax.add_patch(mpatches.FancyBboxPatch((x-w/2, y-h/2), w, h,
            boxstyle='round,pad=0.1', facecolor=col, edgecolor='navy', lw=1.8))
        ax.text(x, y, txt, ha='center', va='center', fontsize=fs, fontweight='bold')

    def arr(x1, y1, x2, y2, lbl='', col='navy', fs=9):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=col, lw=1.9))
        if lbl:
            ax.text((x1+x2)/2, max(y1, y2)+0.28, lbl, ha='center', fontsize=fs, color='darkred')

    box(1.9, yc, 2.4, 1.0, 'GFL_ACTIVE', '#AED6F1')
    arr(3.15, yc, 5.0, yc, 'detección\nislanding')
    box(6.3, yc, 2.5, 1.0, 'TRANSICIÓN', '#F9E79F')
    arr(7.6, yc, 9.5, yc)
    box(10.7, yc, 2.4, 1.0, 'GFM_ACTIVE', '#A9DFBF')

    # Acción bajo TRANSICION
    box(6.3, 1.1, 4.4, 0.9,
        'freeze PLL + precargar estados GFM\n+ abrir interruptor de red', '#FADBD8', 9)
    ax.annotate('', xy=(6.3, 1.6), xytext=(6.3, yc-0.5),
                arrowprops=dict(arrowstyle='->', color='darkred', lw=1.6))

    ax.text(6.0, 0.35, 'Duración típica 1–2 ciclos (20–40 ms): el GFM arranca con estados inicializados, sin discontinuidad de tensión en el PCC',
            ha='center', fontsize=8.5, color='gray', style='italic')

    plt.tight_layout()
    _savefig(fig, "deteccion-islanding-modos")


def _loopshaping_flujo():
    """Flujo del procedimiento de diseno por loop-shaping."""
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    fig, ax = plt.subplots(1, 1, figsize=(9, 9.5))
    ax.set_xlim(0, 9); ax.set_ylim(0, 13); ax.axis('off')
    ax.set_title('Procedimiento de diseño por loop-shaping',
                 fontsize=13, fontweight='bold', pad=10)

    xc = 4.5
    pasos = [
        (r'Especificaciones (BW, PM, GM)', '#D5DBDB'),
        (r'Curva objetivo $L_{obj}(j\omega)$ que las cumple', '#AED6F1'),
        (r'$C(s) = L_{obj}(s)\,/\,G_{planta}(s)$', '#A9DFBF'),
        ('Simplificar $C(s)$: cancelar polos/ceros\ndistantes, verificar realizabilidad', '#AED6F1'),
        ('Añadir filtro HF si hace falta\n(ruido, resonancia)', '#F9E79F'),
        (r'Verificar PM, GM y BW con $L(s)=C(s)\,G(s)$ exacto', '#ABEBC6'),
    ]
    n = len(pasos)
    y0, y1 = 11.8, 1.4
    ys = [y0 - i*(y0-y1)/(n-1) for i in range(n)]
    h = 1.15
    for i, (txt, col) in enumerate(pasos):
        y = ys[i]
        ax.add_patch(mpatches.FancyBboxPatch((xc-3.4, y-h/2), 6.8, h,
            boxstyle='round,pad=0.1', facecolor=col, edgecolor='navy', lw=1.7))
        ax.text(xc, y, txt, ha='center', va='center', fontsize=10.5, fontweight='bold')
        if i < n-1:
            ax.annotate('', xy=(xc, ys[i+1]+h/2), xytext=(xc, y-h/2),
                        arrowprops=dict(arrowstyle='->', color='navy', lw=2.0))

    plt.tight_layout()
    _savefig(fig, "loop-shaping-flujo")


def _parque_offshore_cadena():
    """Cadena electrica de un parque eolico offshore con conexion HVDC."""
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    fig, ax = plt.subplots(1, 1, figsize=(11, 11))
    ax.set_xlim(0, 11); ax.set_ylim(0, 15); ax.axis('off')
    ax.set_title('Cadena de un parque eólico offshore con conexión HVDC',
                 fontsize=13, fontweight='bold', pad=10)

    xc = 4.4
    etapas = [
        ('Aerogeneradores\n' + r'$N \times P_{wt}$', '#A9DFBF', 'Nivel 0: control local MPPT', 'cables 33 kV (inter-array)'),
        ('Subestación offshore (OSS)\n' + r'33 kV $\to$ 155/220 kV', '#AED6F1', '', 'cable de exportación AC (≤50 km)'),
        ('Terminal HVDC offshore\n(MMC-VSC)  AC 155 kV $\\to$ ±320 kV DC', '#F9E79F', 'Nivel 2a: control HVDC', 'cable submarino DC (100–500 km)'),
        ('Terminal HVDC onshore\n(MMC-VSC)  ±320 kV DC $\\to$ AC 400 kV', '#F9E79F', 'Nivel 2b: control HVDC + servicios red', ''),
        ('PCC onshore\n(Point of Common Coupling)', '#AED6F1', '', ''),
        ('Red de transmisión continental', '#D5DBDB', 'Nivel 3: TSO / AGC', ''),
    ]
    n = len(etapas)
    y0, y1 = 13.4, 1.3
    ys = [y0 - i*(y0-y1)/(n-1) for i in range(n)]
    h = 1.25
    for i, (txt, col, nivel, cable) in enumerate(etapas):
        y = ys[i]
        ax.add_patch(mpatches.FancyBboxPatch((xc-3.2, y-h/2), 6.4, h,
            boxstyle='round,pad=0.1', facecolor=col, edgecolor='navy', lw=1.7))
        ax.text(xc, y, txt, ha='center', va='center', fontsize=9.5, fontweight='bold')
        if nivel:
            ax.annotate(nivel, xy=(xc+3.2, y), xytext=(xc+3.4, y),
                        ha='left', va='center', fontsize=8.5, color='darkgreen', fontweight='bold')
        if i < n-1:
            ax.annotate('', xy=(xc, ys[i+1]+h/2), xytext=(xc, y-h/2),
                        arrowprops=dict(arrowstyle='->', color='navy', lw=2.0))
            if cable:
                ax.text(xc-0.15, (y-h/2 + ys[i+1]+h/2)/2, cable, ha='right', va='center',
                        fontsize=8, color='steelblue', style='italic')

    plt.tight_layout()
    _savefig(fig, "parque-offshore-cadena")


def _fv_po_flowchart():
    """Diagrama de flujo del algoritmo P&O (Perturbar y Observar) del MPPT FV."""
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    fig, ax = plt.subplots(1, 1, figsize=(11, 9))
    ax.set_xlim(0, 11); ax.set_ylim(0, 13); ax.axis('off')
    ax.set_title('Algoritmo P&O (Perturbar y Observar) del MPPT',
                 fontsize=13, fontweight='bold', pad=10)

    xc = 5.5

    def rbox(x, y, w, h, txt, col='#AED6F1', fs=9.5):
        ax.add_patch(mpatches.FancyBboxPatch((x-w/2, y-h/2), w, h,
            boxstyle='round,pad=0.08', facecolor=col, edgecolor='navy', lw=1.6))
        ax.text(x, y, txt, ha='center', va='center', fontsize=fs, fontweight='bold')

    def diamond(x, y, w, h, txt, col='#F9E79F', fs=9):
        ax.add_patch(mpatches.FancyBboxPatch((x-w/2, y-h/2), w, h,
            boxstyle='round,pad=0.02', facecolor=col, edgecolor='navy', lw=1.6))
        ax.text(x, y, txt, ha='center', va='center', fontsize=fs, fontweight='bold')

    def down(x, y1, y2, lbl=''):
        ax.annotate('', xy=(x, y2), xytext=(x, y1),
                    arrowprops=dict(arrowstyle='->', color='navy', lw=1.7))
        if lbl:
            ax.text(x+0.2, (y1+y2)/2, lbl, ha='left', va='center', fontsize=8.5, color='darkred')

    # Inicio
    rbox(xc, 12.2, 3.0, 0.7, r'Estado: $(V_{prev},\,P_{prev})$', '#D5DBDB')
    down(xc, 11.85, 11.35)
    # Medir
    rbox(xc, 11.0, 2.6, 0.7, r'Medir $V_k,\ I_k$', '#A9DFBF')
    down(xc, 10.65, 10.15)
    # Calcular ΔP, ΔV
    rbox(xc, 9.7, 3.4, 0.9,
         r'$\Delta P = P_k - P_{prev}$' + '\n' + r'$\Delta V = V_k - V_{prev}$', '#AED6F1')
    down(xc, 9.25, 8.6)
    # Rombo ΔP
    diamond(xc, 8.1, 2.2, 1.0, r'signo de $\Delta P$')

    # Tres ramas
    y_branch = 6.7
    xL, xM, xR = 2.0, 5.5, 9.0
    for x, lbl in [(xL, r'$\Delta P>0$'), (xM, r'$\Delta P\approx 0$'), (xR, r'$\Delta P<0$')]:
        ax.annotate('', xy=(x, y_branch+0.35), xytext=(xc, 7.6),
                    arrowprops=dict(arrowstyle='->', color='navy', lw=1.5))
        ax.text((xc+x)/2, 7.15, lbl, ha='center', fontsize=8.5, color='darkred',
                bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none'))

    # Rama central: no mover
    rbox(xM, y_branch, 1.8, 0.7, 'No mover', '#EAECEE', 9)

    # Ramas laterales con sub-rombo ΔV
    diamond(xL, y_branch, 1.8, 0.8, r'signo $\Delta V$', fs=8.5)
    diamond(xR, y_branch, 1.8, 0.8, r'signo $\Delta V$', fs=8.5)

    # Acciones bajo cada rombo lateral
    y_act = 5.1
    def action(x_par, dx, lbl, act, col):
        x = x_par + dx
        ax.annotate('', xy=(x, y_act+0.35), xytext=(x_par+dx*0.4, y_branch-0.4),
                    arrowprops=dict(arrowstyle='->', color='navy', lw=1.3))
        ax.text(x_par+dx*0.55, (y_branch-0.4+y_act+0.35)/2, lbl, ha='center',
                fontsize=8, color='darkred')
        rbox(x, y_act, 1.35, 0.6, act, col, 8.5)

    action(xL, -0.95, r'$\Delta V>0$', r'$+\Delta V_{step}$', '#ABEBC6')
    action(xL, +0.95, r'$\Delta V<0$', r'$-\Delta V_{step}$', '#F5B7B1')
    action(xR, -0.95, r'$\Delta V>0$', r'$-\Delta V_{step}$', '#F5B7B1')
    action(xR, +0.95, r'$\Delta V<0$', r'$+\Delta V_{step}$', '#ABEBC6')

    # Confluencia hacia actualizar V_ref
    y_upd = 3.3
    rbox(xc, y_upd, 3.2, 0.8, r'Actualizar $V_{ref}$', '#AED6F1')
    for x in [xL-0.95, xL+0.95, xM, xR-0.95, xR+0.95]:
        y_from = (y_branch-0.35) if x == xM else (y_act-0.3)
        ax.plot([x, x, xc], [y_from, y_upd+0.55, y_upd+0.55], 'navy', lw=1.2, alpha=0.55)
    ax.annotate('', xy=(xc, y_upd+0.4), xytext=(xc, y_upd+0.55),
                arrowprops=dict(arrowstyle='->', color='navy', lw=1.5))

    # Bucle de retorno
    down(xc, y_upd-0.4, 2.2)
    rbox(xc, 1.8, 3.6, 0.7, r'$V_{prev}\!\leftarrow\! V_k,\ P_{prev}\!\leftarrow\! P_k$', '#D5DBDB', 9)
    ax.plot([xc-1.8, 0.6, 0.6, xc-1.5], [1.8, 1.8, 11.0, 11.0], 'navy', lw=1.3, ls='--')
    ax.annotate('', xy=(xc-1.3, 11.0), xytext=(xc-1.5, 11.0),
                arrowprops=dict(arrowstyle='->', color='navy', lw=1.3))
    ax.text(0.75, 6.4, 'siguiente\niteración', ha='left', fontsize=8.5,
            color='gray', style='italic')

    plt.tight_layout()
    _savefig(fig, "fotovoltaica-po-flowchart")


def _btb_topologia():
    """Topología del convertidor back-to-back: Red AC1 - Filtro L1 - VSC1 -
    bus DC (C_dc) - VSC2 - Filtro L2 - Red AC2, con bloques."""
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    fig, ax = plt.subplots(1, 1, figsize=(14, 6.5))
    ax.set_xlim(0, 14); ax.set_ylim(0, 8); ax.axis('off')
    ax.set_title('Topología del convertidor back-to-back',
                 fontsize=13, fontweight='bold', pad=12)

    yc = 4.5  # eje central

    def box(x, y, w, h, txt, col, fs=9):
        ax.add_patch(mpatches.FancyBboxPatch((x-w/2, y-h/2), w, h,
            boxstyle='round,pad=0.08', facecolor=col, edgecolor='navy', lw=1.6))
        ax.text(x, y, txt, ha='center', va='center', fontsize=fs, fontweight='bold')

    def wire(x1, x2, y=yc, col='navy', lw=2.0):
        ax.plot([x1, x2], [y, y], color=col, lw=lw)

    # Red AC 1 (fuente izquierda)
    box(1.1, yc, 1.6, 1.4, 'Red AC 1\n' + r'$(v_{g1},\,\omega_1)$', '#D5DBDB', 10)
    wire(1.9, 3.0)
    # Filtro L1
    box(3.6, yc, 1.5, 1.0, r'Filtro $L_1$' + '\n' + r'$R_1{+}jX_1$', '#FCF3CF', 9)
    wire(4.35, 5.2)
    # VSC1
    box(5.9, yc, 1.5, 1.8, 'VSC 1\n(MSC/GSC)', '#AED6F1', 9.5)
    wire(6.65, 7.35)
    # Bus DC / condensador
    box(8.1, yc, 1.6, 2.2, 'Bus DC\n' + r'$C_{dc}$' + '\n' + r'$V_{dc}$', '#A9DFBF', 10)
    wire(8.9, 9.6)
    # VSC2
    box(10.3, yc, 1.5, 1.8, 'VSC 2\n(GSC/LSC)', '#AED6F1', 9.5)
    wire(11.05, 11.7)
    # Filtro L2
    box(12.0, yc, 1.5, 1.0, r'Filtro $L_2$' + '\n' + r'$R_2{+}jX_2$', '#FCF3CF', 9)

    # Red AC 2 (a la derecha, texto)
    ax.annotate('', xy=(13.6, yc), xytext=(12.75, yc),
                arrowprops=dict(arrowstyle='->', color='navy', lw=2.0))
    ax.text(13.7, yc, 'Red\nAC 2\n' + r'$(v_{g2},\,\omega_2)$',
            ha='left', va='center', fontsize=9, fontweight='bold')

    # Anotación del condensador
    ax.annotate('Condensador de bus\n' + r'$E=\frac{1}{2}C_{dc}V_{dc}^2$',
                xy=(8.1, 3.4), xytext=(8.1, 1.6),
                ha='center', fontsize=9, color='darkgreen',
                arrowprops=dict(arrowstyle='->', color='darkgreen', lw=1.4))

    # Flechas de flujo de potencia bidireccional
    ax.annotate('', xy=(9.9, 6.6), xytext=(6.3, 6.6),
                arrowprops=dict(arrowstyle='<->', color='darkred', lw=1.8))
    ax.text(8.1, 6.9, 'Flujo de potencia bidireccional',
            ha='center', fontsize=9.5, color='darkred', fontweight='bold')

    # Etiqueta de desacoplo energético
    ax.text(8.1, 0.7, 'El bus DC desacopla ambos lados: acoplamiento puramente energético',
            ha='center', fontsize=9, color='gray', style='italic')

    plt.tight_layout()
    _savefig(fig, "btb-topologia")


def _btb_lazo_dc():
    """Diagrama de bloques del lazo de tensión DC completo con feedforward."""
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    fig, ax = plt.subplots(1, 1, figsize=(13, 6))
    ax.set_xlim(0, 13); ax.set_ylim(0, 8); ax.axis('off')
    ax.set_title('Lazo de control de la tensión del bus DC',
                 fontsize=13, fontweight='bold', pad=12)

    yc = 5.0

    def box(x, y, w, h, txt, col, fs=9.5):
        ax.add_patch(mpatches.FancyBboxPatch((x-w/2, y-h/2), w, h,
            boxstyle='round,pad=0.08', facecolor=col, edgecolor='navy', lw=1.6))
        ax.text(x, y, txt, ha='center', va='center', fontsize=fs, fontweight='bold')

    def circle(x, y, lbl, r=0.32):
        ax.add_patch(plt.Circle((x, y), r, facecolor='white', edgecolor='navy', lw=1.6))
        ax.text(x, y, lbl, ha='center', va='center', fontsize=11, fontweight='bold')

    def arr(x1, y1, x2, y2, lbl='', col='navy'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=col, lw=1.8))
        if lbl:
            ax.text((x1+x2)/2, (y1+y2)/2+0.28, lbl, ha='center', fontsize=9, color='darkred')

    # Referencia V*²dc
    ax.text(0.5, yc, r'$V_{dc}^{*2}$', ha='center', va='center', fontsize=11)
    arr(0.95, yc, 1.5, yc)
    circle(1.85, yc, '−')
    arr(2.2, yc, 3.0, yc, r'$e_w$')
    # PI_dc
    box(3.7, yc, 1.3, 0.9, r'$PI_{dc}$', '#AED6F1')
    arr(4.35, yc, 5.1, yc)
    # Suma feedforward
    circle(5.45, yc, '+')
    arr(5.8, yc, 6.6, yc, r'$i_{d,GSC}^*$')
    # Lazo de corriente ≈ 1
    box(7.4, yc, 1.5, 0.9, 'Lazo\ncorr. ' + r'$\approx 1$', '#A9DFBF', 9)
    arr(8.15, yc, 8.9, yc, r'$P_{GSC}$')
    # Planta bus DC
    box(9.7, yc, 1.3, 0.9, r'$\dfrac{2}{C_{dc}s}$', '#FAD7A0')
    arr(10.35, yc, 11.2, yc)
    ax.text(11.5, yc, r'$w=V_{dc}^2$', ha='left', va='center', fontsize=11)

    # Realimentación
    ax.plot([11.15, 11.15, 1.85], [yc, yc-1.1, yc-1.1], 'navy', lw=1.8)
    ax.annotate('', xy=(1.85, yc-0.32), xytext=(1.85, yc-1.1),
                arrowprops=dict(arrowstyle='->', color='navy', lw=1.8))

    # Feedforward de potencia
    ax.text(5.45, 7.3, r'$P_{MSC}$', ha='center', va='center', fontsize=11, color='darkgreen')
    ax.annotate('', xy=(5.45, 6.7), xytext=(5.45, 7.05),
                arrowprops=dict(arrowstyle='->', color='darkgreen', lw=1.6))
    box(5.45, 6.35, 1.7, 0.7, r'$\div\,(1.5\,v_{d,g})$', '#ABEBC6', 8.5)
    ax.annotate('', xy=(5.45, yc+0.32), xytext=(5.45, 6.0),
                arrowprops=dict(arrowstyle='->', color='darkgreen', lw=1.6))
    ax.text(5.85, 5.75, '+', ha='center', fontsize=10, color='darkgreen')
    ax.text(7.6, 6.9, 'feedforward de potencia', ha='center', fontsize=9,
            color='darkgreen', style='italic')

    # Notas
    ax.text(6.5, 3.2,
            r'Separación de escalas: $\omega_{dc}=\omega_{ci}/10$   →   el lazo de corriente se ve como ganancia 1',
            ha='center', fontsize=9,
            bbox=dict(boxstyle='round', facecolor='#EBF5FB', edgecolor='steelblue'))
    ax.text(6.5, 2.3,
            r'Sintonía: $K_{p,dc}=C_{dc}\omega_{dc}/2$,   $T_{i,dc}=4/\omega_{dc}$',
            ha='center', fontsize=9,
            bbox=dict(boxstyle='round', facecolor='#EBF5FB', edgecolor='steelblue'))
    ax.text(6.5, 1.4,
            r'Condición de estabilidad con CPL: $K_{p,dc} > P_{2,max}/(2V_{dc,0}^2)$',
            ha='center', fontsize=9, color='red',
            bbox=dict(boxstyle='round', facecolor='#FDEDEC', edgecolor='red'))

    plt.tight_layout()
    _savefig(fig, "btb-lazo-dc")


def _npc_topologia():
    """NPC de 3 niveles: rama de fase completa con los 4 IGBTs, los 2 diodos
    de anclaje y los 2 condensadores de bus, etiquetando P, O, N."""
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    fig, ax = plt.subplots(1, 1, figsize=(7, 8.5))
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_xlim(-2.8, 3.2); ax.set_ylim(-0.8, 6.2)
    ax.set_title('Rama de fase del NPC de 3 niveles', fontsize=13, fontweight='bold', pad=10)

    def sw(x, y, lbl):
        ax.add_patch(mpatches.FancyBboxPatch((x-0.4, y-0.26), 0.8, 0.52, boxstyle='round,pad=0.04',
            facecolor='#AED6F1', edgecolor='navy', lw=1.6))
        ax.text(x, y, lbl, ha='center', va='center', fontsize=10, fontweight='bold')
    def wire(pts, col='navy', lw=1.8):
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color=col, lw=lw)
    def dot(x, y):
        ax.plot([x], [y], 'o', color='navy', ms=6)
    def cap(x, y, lbl):
        ax.plot([x-0.32, x+0.32], [y+0.08, y+0.08], 'navy', lw=2.6)
        ax.plot([x-0.32, x+0.32], [y-0.08, y-0.08], 'navy', lw=2.6)
        ax.text(x+0.48, y, lbl, fontsize=9.5, va='center')

    # buses
    ax.plot([-2.3, 0.9], [5.7, 5.7], 'navy', lw=2.4); ax.text(-2.5, 5.7, 'P', ha='right', va='center', fontsize=12, fontweight='bold')
    ax.plot([-2.3, 0.9], [2.85, 2.85], 'navy', lw=1.6); ax.text(-2.5, 2.85, 'O', ha='right', va='center', fontsize=12, fontweight='bold')
    ax.plot([-2.3, 0.9], [0.0, 0.0], 'navy', lw=2.4); ax.text(-2.5, 0.0, 'N', ha='right', va='center', fontsize=12, fontweight='bold')

    # condensadores de bus
    cap(-1.7, 4.28, r'$C_1,\ V_{dc}/2$'); wire([(-1.7, 5.7), (-1.7, 4.36)]); wire([(-1.7, 4.20), (-1.7, 2.85)])
    cap(-1.7, 1.43, r'$C_2,\ V_{dc}/2$'); wire([(-1.7, 2.85), (-1.7, 1.51)]); wire([(-1.7, 1.35), (-1.7, 0.0)])

    # rama con 4 IGBTs
    xs = 0.0
    wire([(xs, 5.7), (xs, 5.15)]); sw(xs, 4.85, 'T1'); wire([(xs, 4.55), (xs, 4.0)])
    sw(xs, 3.7, 'T2'); wire([(xs, 3.4), (xs, 2.85)])
    dot(xs, 2.85)
    ax.annotate('', xy=(xs+1.6, 2.85), xytext=(xs, 2.85), arrowprops=dict(arrowstyle='-|>', color='darkred', lw=2.2))
    ax.text(xs+1.75, 2.85, 'salida (fase)', color='darkred', fontsize=10, va='center')
    wire([(xs, 2.85), (xs, 2.3)]); sw(xs, 2.0, 'T3'); wire([(xs, 1.7), (xs, 1.15)])
    sw(xs, 0.85, 'T4'); wire([(xs, 0.55), (xs, 0.0)])

    # diodos de anclaje D1 (de O a nudo T1-T2) y D2 (de nudo T3-T4 a O)
    ax.annotate('', xy=(xs-0.42, 4.0), xytext=(-1.1, 2.85), arrowprops=dict(arrowstyle='-|>', color='#c0392b', lw=1.7))
    wire([(-1.7, 2.85), (-1.1, 2.85)], col='#c0392b', lw=1.4)
    ax.text(-1.15, 3.55, 'D1', color='#c0392b', fontsize=10, fontweight='bold')
    ax.annotate('', xy=(-1.1, 2.85), xytext=(xs-0.42, 1.7), arrowprops=dict(arrowstyle='-|>', color='#c0392b', lw=1.7))
    ax.text(-1.15, 2.15, 'D2', color='#c0392b', fontsize=10, fontweight='bold')

    ax.text(0.5, -0.55, 'Cada IGBT bloquea $V_{dc}/2$ · el nivel de salida depende de\nqué par (T1T2 / T2T3 / T3T4) está en ON',
            ha='center', fontsize=9, color='gray')

    plt.tight_layout()
    _savefig(fig, 'npc-topologia', dpi=165)


def _npc_conmutacion():
    """NPC: (a) tabla visual de estados de conmutacion (heatmap de ON/OFF por
    IGBT y nivel de salida); (b) formas de onda: portadoras PD-PWM, referencia,
    tension de fase de 3 niveles y espectro comparado con 2 niveles."""
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(14, 8.6))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.2], hspace=0.42, wspace=0.28)
    axT = fig.add_subplot(gs[0, :])
    axW = fig.add_subplot(gs[1, 0])
    axS = fig.add_subplot(gs[1, 1])
    fig.suptitle('NPC 3 niveles: estados de conmutación y modulación PD-PWM', fontsize=13, fontweight='bold')

    # ---- (a) tabla de estados como texto formateado ----
    axT.axis('off')
    estados = [
        ('P',  '1','1','0','0', r'$+V_{dc}/2$', 'T1,T2 ON — salida a P'),
        ('O+', '0','1','1','0', r'$0$',          'T2,T3 ON, $i_o>0$ → D1 conduce'),
        ('O-', '0','1','1','0', r'$0$',          'T2,T3 ON, $i_o<0$ → D2 conduce'),
        ('N',  '0','0','1','1', r'$-V_{dc}/2$', 'T3,T4 ON — salida a N'),
    ]
    headers = ['Estado', 'T1', 'T2', 'T3', 'T4', 'Salida', 'Comentario']
    colw = [0.09, 0.05, 0.05, 0.05, 0.05, 0.13, 0.50]
    x0 = 0.02
    xs = [x0]
    for w in colw: xs.append(xs[-1]+w)
    y0 = 0.95
    for j, h in enumerate(headers):
        axT.text(xs[j], y0, h, fontsize=10, fontweight='bold', color='#cdd9e5')
    axT.plot([0.02, 0.97], [y0-0.08, y0-0.08], color='#555', lw=1)
    rowh = 0.20
    cols_sw = {'1': '#A9DFBF', '0': '#F5B7B1'}
    for i, row in enumerate(estados):
        y = y0 - 0.08 - rowh*(i+1) + 0.02
        axT.text(xs[0], y, row[0], fontsize=10.5, fontweight='bold')
        for j in range(4):
            val = row[1+j]
            axT.add_patch(plt.Rectangle((xs[1+j], y-0.045), 0.038, 0.09,
                          facecolor=cols_sw[val], edgecolor='#333', lw=0.6, transform=axT.transAxes))
            axT.text(xs[1+j]+0.019, y, val, ha='center', va='center', fontsize=9.5, transform=axT.transAxes)
        axT.text(xs[5], y, row[5], fontsize=10)
        axT.text(xs[6], y, row[6], fontsize=8.8, color='#aaa')
    axT.set_xlim(0, 1); axT.set_ylim(0, 1)
    axT.set_title('(a) Tabla de estados (verde=ON, rojo=OFF) — T1,T3 y T2,T4 son complementarios',
                  fontsize=10.5, fontweight='bold', loc='left')

    # ---- (b) PD-PWM: dos portadoras + referencia + salida ----
    m = 0.85; fs = 1500.0; f0 = 50.0
    t = np.linspace(0, 1/f0, 3000)
    ref = m*np.sin(2*np.pi*f0*t)
    fase = np.mod(t*fs, 1.0); tri = 4*np.abs(fase-0.5)-1
    port_hi = 0.5*tri + 0.5   # 0..1
    port_lo = 0.5*tri - 0.5   # -1..0
    vout = np.where(ref > port_hi, 1.0, np.where(ref < port_lo, -1.0, 0.0))
    axW.plot(t*1000, port_hi, color='#999', lw=0.9)
    axW.plot(t*1000, port_lo, color='#999', lw=0.9, label='portadoras PD')
    axW.plot(t*1000, ref, color='navy', lw=1.8, label='referencia $m\\sin\\theta$')
    axW.plot(t*1000, vout*0.5, color='#c0392b', lw=1.6, drawstyle='steps-post', label='$v_{aO}/(V_{dc}/2)$ (offset visual)')
    axW.set_xlabel('t [ms]'); axW.set_ylabel('p.u.'); axW.grid(alpha=.3)
    axW.legend(fontsize=7.5, loc='lower right')
    axW.set_title('(b) PD-PWM: dos portadoras apiladas → 3 niveles', fontsize=10.5, fontweight='bold')

    # ---- (c) espectro comparado 2L vs NPC (armonicos de fs) ----
    fs2 = 1500.0
    n = np.arange(1, 12)
    # amplitud relativa de las bandas laterales alrededor de fs y 2fs (aprox ilustrativa)
    amp2L = np.exp(-0.15*(n-1))
    ampNPC = np.exp(-0.15*(n-1))*0.5**n  # cae mas rapido: aprox factor (Vdc/2)/Vdc por nivel extra
    axS.bar(n-0.15, amp2L, width=0.3, color='#e67e22', label='2 niveles')
    axS.bar(n+0.15, ampNPC, width=0.3, color='#2e86c1', label='NPC 3 niveles')
    axS.set_yscale('log'); axS.set_ylim(1e-3, 1.5)
    axS.set_xlabel('orden de banda alrededor de $f_{sw}$'); axS.set_ylabel('amplitud relativa')
    axS.set_title('(c) Contenido armónico (ilustrativo): NPC cae mucho más rápido', fontsize=10.5, fontweight='bold')
    axS.legend(fontsize=8.5); axS.grid(alpha=.3, axis='y')

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    _savefig(fig, 'npc-conmutacion', dpi=160)


def _npc_neutro():
    """NPC: balance del punto neutro. (a) caminos de corriente para el estado O
    segun el signo de i_o (D1 vs D2 conducen, cargan C2 o C1); (b) simulacion
    simplificada de V_C1, V_C2 con y sin compensacion (inyeccion 3er armonico)."""
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 5.6), gridspec_kw={'width_ratios': [0.85, 1.15]})
    fig.suptitle('NPC: balance del punto neutro O', fontsize=13, fontweight='bold')

    # ---- (a) esquema de caminos de corriente ----
    a1.set_aspect('equal'); a1.axis('off')
    a1.set_xlim(-2.2, 2.4); a1.set_ylim(-0.6, 5.6)
    a1.set_title('(a) Estado "O": camino según signo de $i_o$', fontsize=10.5, fontweight='bold')
    a1.plot([-1.6, 0.6], [5.2, 5.2], 'navy', lw=2)
    a1.plot([-1.6, 0.6], [2.6, 2.6], 'navy', lw=1.3)
    a1.plot([-1.6, 0.6], [0.0, 0.0], 'navy', lw=2)
    a1.text(-1.85, 5.2, 'P', fontsize=10, va='center'); a1.text(-1.85, 2.6, 'O', fontsize=10, va='center'); a1.text(-1.85, 0.0, 'N', fontsize=10, va='center')
    a1.plot([-1.2, -1.2], [5.2, 3.05], 'navy', lw=1.6); a1.plot([-1.2, -1.2], [2.15, 0.0], 'navy', lw=1.6)
    a1.text(-1.0, 3.9, r'$C_1$', fontsize=9); a1.text(-1.0, 1.3, r'$C_2$', fontsize=9)
    a1.annotate('', xy=(0.0, 3.9), xytext=(-0.55, 2.6), arrowprops=dict(arrowstyle='-|>', color='#c0392b', lw=2))
    a1.text(0.1, 3.9, r'$i_o>0$: D1 conduce' + '\n' + r'descarga $C_1$, carga $C_2$', fontsize=8.5, color='#c0392b')
    a1.annotate('', xy=(-0.55, 2.6), xytext=(0.0, 1.3), arrowprops=dict(arrowstyle='-|>', color='#1e8449', lw=2))
    a1.text(0.1, 1.0, r'$i_o<0$: D2 conduce' + '\n' + r'descarga $C_2$, carga $C_1$', fontsize=8.5, color='#1e8449')

    # ---- (b) evolucion de VC1, VC2 con y sin compensacion ----
    # Modelo simplificado: una carga desbalanceada monofasica conectada entre O y N
    # (peor caso realista) fuerza una corriente media hacia O que descarga C1 y
    # carga C2 progresivamente si no se compensa. La compensacion inyecta una
    # pequena componente de secuencia cero (3er armonico) proporcional al
    # desbalance medido, que reduce el tiempo neto en el estado O.
    V0 = 575.0; C = 6e-3
    t = np.linspace(0, 2.0, 20000); dt = t[1]-t[0]
    Idc_bias = 0.6    # [A] componente de continua de la corriente hacia O (desbalance de carga)
    def sim(kcomp):
        vc1 = np.zeros(len(t)); vc2 = np.zeros(len(t))
        vc1[0] = V0; vc2[0] = V0
        for k in range(len(t)-1):
            err = vc1[k] - vc2[k]                  # desbalance actual (V_C1 - V_C2)
            iO = Idc_bias + kcomp*err              # a mas err, MAS corriente hacia O que lo corrige
            vc1[k+1] = vc1[k] - iO*dt/C             # iO descarga C1...
            vc2[k+1] = vc2[k] + iO*dt/C             # ...y carga C2 (por continuidad en el nudo O)
        return vc1, vc2
    vc1n, vc2n = sim(0.0)      # sin compensacion: deriva libre (integrador puro)
    vc1c, vc2c = sim(3.0)      # con compensacion: realimentacion proporcional que la frena (1er orden estable)
    a2.plot(t*1000, vc1n, color='#c0392b', lw=1.8, label='$V_{C1}$ sin comp.')
    a2.plot(t*1000, vc2n, color='#e08a00', lw=1.8, ls='--', label='$V_{C2}$ sin comp.')
    a2.plot(t*1000, vc1c, color='navy', lw=1.8, label='$V_{C1}$ con comp.')
    a2.plot(t*1000, vc2c, color='#2e86c1', lw=1.8, ls='--', label='$V_{C2}$ con comp.')
    a2.axhline(V0, color='gray', lw=0.8, ls=':')
    a2.set_xlabel('t [ms]'); a2.set_ylabel('V'); a2.grid(alpha=.3)
    a2.legend(fontsize=8, ncol=2, loc='center right')
    a2.set_title('(b) Ante una carga desbalanceada: deriva sin compensación\nvs. estabilización con compensación proporcional', fontsize=10, fontweight='bold')

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    _savefig(fig, 'npc-neutro', dpi=160)


def _npc_svm():
    """NPC SVM: (a) diagrama hexagonal con los 27 estados (19 posiciones fisicas,
    vectores largos/medios/cortos redundantes/cero) y los 6 sectores + triangulos;
    (b) zoom de un triangulo con los 3 vectores adyacentes y el vector de referencia
    descompuesto para el calculo de tiempos."""
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 7), gridspec_kw={'width_ratios': [1.15, 1]})
    fig.suptitle('NPC 3 niveles: modulación vectorial (SVM)', fontsize=13, fontweight='bold')

    # ---- (a) hexagono completo de 19 posiciones ----
    a1.set_aspect('equal'); a1.axis('off')
    a1.set_xlim(-2.6, 2.6); a1.set_ylim(-2.4, 2.4)
    a1.set_title('(a) 19 posiciones físicas (27 estados de conmutación)', fontsize=10.5, fontweight='bold')

    def abc_to_xy(a, b, c):
        # proyeccion de las tres componentes de fase (niveles -1,0,+1) sobre alfa-beta
        x = a - 0.5*b - 0.5*c
        y = (np.sqrt(3)/2)*(b - c)
        return x, y

    # generar los 27 estados (cada fase en {-1,0,1}) y agrupar por posicion fisica
    pts = {}
    for na in (-1, 0, 1):
        for nb in (-1, 0, 1):
            for nc in (-1, 0, 1):
                x, y = abc_to_xy(na, nb, nc)
                key = (round(x, 3), round(y, 3))
                pts.setdefault(key, []).append((na, nb, nc))

    # dibujar hexagono exterior (guia)
    hexang = np.linspace(0, 2*np.pi, 7)
    a1.plot(1.5*np.cos(hexang+np.pi/6), 1.5*np.sin(hexang+np.pi/6), color='#ccc', lw=1, ls='--')
    # sectores (6 lineas desde el centro)
    for k in range(6):
        ang = k*np.pi/3
        a1.plot([0, 1.7*np.cos(ang)], [0, 1.7*np.sin(ang)], color='#ddd', lw=0.8)

    for (x, y), states in pts.items():
        n = len(states)
        r = np.hypot(x, y)
        if r < 0.05:
            col, sz = '#888', 60      # vector cero (origen), 3 estados redundantes
        elif n >= 2:
            col, sz = '#2e86c1', 70   # vector corto/medio redundante
        elif r > 1.3:
            col, sz = '#c0392b', 55   # vector largo (esquina)
        else:
            col, sz = '#e08a00', 55   # vector medio/corto no redundante
        a1.scatter([x], [y], s=sz, color=col, edgecolor='navy', lw=0.8, zorder=5)
        if n >= 2:
            a1.text(x, y+0.14, f'{n}×', fontsize=7, ha='center', color='#2e86c1')

    a1.text(-2.5, -2.3, 'gris=cero (3) · azul=redundante (2) · naranja=único · rojo=largo (esquina)',
            fontsize=7.5, color='gray')

    # ---- (b) zoom de un triangulo con vector de referencia ----
    a2.set_aspect('equal'); a2.axis('off')
    a2.set_xlim(-0.3, 2.0); a2.set_ylim(-0.3, 1.9)
    a2.set_title('(b) Descomposición en un triángulo: cálculo de tiempos', fontsize=10.5, fontweight='bold')

    V1 = np.array([1.0, 0.0])     # vector corto (nivel medio, ej. POO)
    V2 = np.array([1.5, 0.866])   # vector largo (esquina, ej. PPO)
    V0 = np.array([0.5, 0.866])   # vector medio (ej. PON), forma el triangulo con V1,V2

    for P, lbl, col in [(V1, r'$V_1$ (corto)', '#e08a00'), (V2, r'$V_2$ (largo)', '#c0392b'), (V0, r'$V_0$ (medio)', '#8e44ad')]:
        a2.plot([0, P[0]], [0, P[1]], color=col, lw=1.2, ls=':')
        a2.plot([P[0]], [P[1]], 'o', color=col, ms=8, zorder=5)
        a2.text(P[0]+0.05, P[1]+0.05, lbl, fontsize=9, color=col)
    a2.plot([V1[0], V2[0], V0[0], V1[0]], [V1[1], V2[1], V0[1], V1[1]], color='#888', lw=1.3)

    Vref = 0.45*V1 + 0.30*V2 + 0.25*V0
    a2.annotate('', xy=tuple(Vref), xytext=(0, 0), arrowprops=dict(arrowstyle='-|>', color='navy', lw=2.4))
    a2.text(Vref[0]+0.08, Vref[1]-0.05, r'$\vec V_{ref}$', color='navy', fontsize=11, fontweight='bold')

    a2.text(1.0, -0.15,
            r'$\vec V_{ref}=d_1\vec V_1+d_2\vec V_2+d_0\vec V_0,\quad d_1+d_2+d_0=1$',
            ha='center', fontsize=9.5,
            bbox=dict(boxstyle='round', facecolor='#EBF5FB', edgecolor='steelblue'))

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    _savefig(fig, 'npc-svm', dpi=160)


def _mmc_estructura():
    """MMC: (a) estructura trifasica (6 brazos, bus DC, salida AC);
    (b) descomposicion de corrientes en una fase: brazo sup/inf, corriente de
    salida i_out = i_u - i_l y corriente de circulacion i_circ = (i_u+i_l)/2."""
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 6.4), gridspec_kw={'width_ratios': [1.25, 1]})
    fig.suptitle('MMC: estructura y descomposición de corrientes', fontsize=13, fontweight='bold')
    for ax in (a1, a2):
        ax.set_aspect('equal'); ax.axis('off')

    def armbox(ax, x, y, txt):
        ax.add_patch(mpatches.FancyBboxPatch((x-0.32, y-0.5), 0.64, 1.0, boxstyle='round,pad=0.04',
            facecolor='#A9DFBF', edgecolor='navy', lw=1.5))
        ax.text(x, y, txt, ha='center', va='center', fontsize=7.5, fontweight='bold')
    def Lb(ax, x, y):
        ax.add_patch(mpatches.FancyBboxPatch((x-0.12, y-0.2), 0.24, 0.4, boxstyle='round',
            facecolor='#FCF3CF', edgecolor='navy', lw=1.2))
    def wire(ax, pts, col='navy', lw=1.6):
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color=col, lw=lw)

    # ---- (a) estructura trifasica ----
    a1.set_title('(a) Estructura trifásica', fontsize=10.5, fontweight='bold')
    a1.set_xlim(-0.4, 5.2); a1.set_ylim(-0.6, 6.2)
    a1.plot([0.2, 4.6], [5.8, 5.8], 'navy', lw=2.2); a1.text(0.0, 5.8, r'$+\frac{V_{dc}}{2}$', ha='right', va='center', fontsize=9)
    a1.plot([0.2, 4.6], [0.0, 0.0], 'navy', lw=2.2); a1.text(0.0, 0.0, r'$-\frac{V_{dc}}{2}$', ha='right', va='center', fontsize=9)
    for x, ph in [(1.0, 'a'), (2.4, 'b'), (3.8, 'c')]:
        wire(a1, [(x, 5.8), (x, 5.3)])
        armbox(a1, x, 4.7, 'N SM\nsup.'); wire(a1, [(x, 4.2), (x, 4.0)]); Lb(a1, x, 3.8); wire(a1, [(x, 3.6), (x, 3.3)])
        a1.plot([x], [3.3], 'o', color='darkred', ms=5)
        a1.annotate('', xy=(x+0.7, 3.3), xytext=(x, 3.3), arrowprops=dict(arrowstyle='-|>', color='darkred', lw=1.6))
        a1.text(x+0.75, 3.3, ph, color='darkred', fontsize=9, va='center', fontweight='bold')
        wire(a1, [(x, 3.3), (x, 3.0)]); Lb(a1, x, 2.8); wire(a1, [(x, 2.6), (x, 2.4)])
        armbox(a1, x, 1.8, 'N SM\ninf.'); wire(a1, [(x, 1.3), (x, 0.0)])
    a1.text(2.4, -0.5, '6 brazos (2 por fase), salida AC a/b/c', ha='center', fontsize=8.5, color='gray')

    # ---- (b) corrientes de una fase ----
    a2.set_title('(b) Corrientes en una fase', fontsize=10.5, fontweight='bold')
    a2.set_xlim(-1.4, 3); a2.set_ylim(-0.6, 6.2)
    a2.plot([-0.6, 1.2], [5.8, 5.8], 'navy', lw=2); a2.plot([-0.6, 1.2], [0.0, 0.0], 'navy', lw=2)
    x = 0.3
    wire(a2, [(x, 5.8), (x, 5.3)]); armbox(a2, x, 4.7, 'brazo\nsup.'); wire(a2, [(x, 4.2), (x, 3.3)])
    a2.plot([x], [3.3], 'o', color='navy', ms=5)
    wire(a2, [(x, 3.3), (x, 2.4)]); armbox(a2, x, 1.8, 'brazo\ninf.'); wire(a2, [(x, 1.3), (x, 0.0)])
    # corriente brazo superior e inferior (hacia abajo)
    a2.annotate('', xy=(x-0.55, 4.4), xytext=(x-0.55, 5.0), arrowprops=dict(arrowstyle='-|>', color='#2e86c1', lw=1.8))
    a2.text(x-0.62, 5.15, r'$i_u$', color='#2e86c1', fontsize=10, ha='center')
    a2.annotate('', xy=(x-0.55, 1.5), xytext=(x-0.55, 2.1), arrowprops=dict(arrowstyle='-|>', color='#1e8449', lw=1.8))
    a2.text(x-0.62, 2.25, r'$i_l$', color='#1e8449', fontsize=10, ha='center')
    # salida
    a2.annotate('', xy=(x+1.4, 3.3), xytext=(x, 3.3), arrowprops=dict(arrowstyle='-|>', color='darkred', lw=2))
    a2.text(x+1.5, 3.3, r'$i_{out}$', color='darkred', fontsize=10, va='center')
    # relaciones
    a2.text(0.8, 0.6,
            r'$i_{out}=i_u-i_l$' + '\n' + r'$i_{circ}=\dfrac{i_u+i_l}{2}$',
            ha='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='#EBF5FB', edgecolor='steelblue'))

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    _savefig(fig, 'mmc-estructura', dpi=160)


def _multinivel_circuitos():
    """Ramas de fase de las topologias multinivel: 2 niveles, NPC 3 niveles y
    MMC (brazos + submodulo half-bridge). Dibujo simplificado con interruptores
    como cajas, diodos como flechas y condensadores como barras."""
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(15, 6.4))
    fig.suptitle('Topologías multinivel: una rama de fase', fontsize=13, fontweight='bold')
    for ax in (a1, a2, a3):
        ax.set_aspect('equal'); ax.axis('off')

    def sw(ax, x, y, lbl, col='#AED6F1'):
        ax.add_patch(mpatches.FancyBboxPatch((x-0.35, y-0.24), 0.7, 0.48,
            boxstyle='round,pad=0.04', facecolor=col, edgecolor='navy', lw=1.5))
        ax.text(x, y, lbl, ha='center', va='center', fontsize=8.5, fontweight='bold')
    def wire(ax, pts, col='navy', lw=1.6):
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color=col, lw=lw)
    def dot(ax, x, y):
        ax.plot([x], [y], 'o', color='navy', ms=5)
    def cap(ax, x, y, lbl=''):
        ax.plot([x-0.28, x+0.28], [y+0.07, y+0.07], 'navy', lw=2.4)
        ax.plot([x-0.28, x+0.28], [y-0.07, y-0.07], 'navy', lw=2.4)
        if lbl:
            ax.text(x+0.42, y, lbl, fontsize=8, va='center')
    def out(ax, x, y):
        ax.annotate('', xy=(x+1.0, y), xytext=(x, y), arrowprops=dict(arrowstyle='-|>', color='darkred', lw=2))
        ax.text(x+1.1, y, 'salida', color='darkred', fontsize=8.5, va='center')

    # -------- (a) 2 niveles --------
    a1.set_title('(a) 2 niveles', fontsize=10.5, fontweight='bold')
    a1.set_xlim(-2, 2.6); a1.set_ylim(-0.6, 4.2)
    a1.plot([-1.4, 0.5], [3.8, 3.8], 'navy', lw=2); a1.text(-1.6, 3.8, r'$+\frac{V_{dc}}{2}$', ha='right', va='center', fontsize=9)
    a1.plot([-1.4, 0.5], [0.0, 0.0], 'navy', lw=2); a1.text(-1.6, 0.0, r'$-\frac{V_{dc}}{2}$', ha='right', va='center', fontsize=9)
    wire(a1, [(0, 3.8), (0, 2.9)]); sw(a1, 0, 2.6, 'T1'); wire(a1, [(0, 2.3), (0, 1.9)])
    dot(a1, 0, 1.9); out(a1, 0, 1.9)
    wire(a1, [(0, 1.9), (0, 1.5)]); sw(a1, 0, 1.2, 'T2'); wire(a1, [(0, 0.9), (0, 0.0)])
    a1.text(0, -0.45, '2 valores', ha='center', fontsize=8.5, color='gray')

    # -------- (b) NPC 3 niveles --------
    a2.set_title('(b) NPC 3 niveles', fontsize=10.5, fontweight='bold')
    a2.set_xlim(-2.6, 3); a2.set_ylim(-0.6, 5.4)
    a2.plot([-2, 0.6], [5.0, 5.0], 'navy', lw=2); a2.text(-2.2, 5.0, 'P', ha='right', va='center', fontsize=9)
    a2.plot([-2, 0.6], [2.5, 2.5], 'navy', lw=1.5); a2.text(-2.2, 2.5, 'O', ha='right', va='center', fontsize=9)
    a2.plot([-2, 0.6], [0.0, 0.0], 'navy', lw=2); a2.text(-2.2, 0.0, 'N', ha='right', va='center', fontsize=9)
    cap(a2, -1.6, 3.75, 'C1'); wire(a2, [(-1.6, 5.0), (-1.6, 3.82)]); wire(a2, [(-1.6, 3.68), (-1.6, 2.5)])
    cap(a2, -1.6, 1.25, 'C2'); wire(a2, [(-1.6, 2.5), (-1.6, 1.32)]); wire(a2, [(-1.6, 1.18), (-1.6, 0.0)])
    xs = 0.3
    wire(a2, [(xs, 5.0), (xs, 4.5)]); sw(a2, xs, 4.2, 'T1'); wire(a2, [(xs, 3.9), (xs, 3.6)]); sw(a2, xs, 3.3, 'T2')
    wire(a2, [(xs, 3.0), (xs, 2.5)]); dot(a2, xs, 2.5); out(a2, xs, 2.5)
    wire(a2, [(xs, 2.5), (xs, 2.0)]); sw(a2, xs, 1.7, 'T3'); wire(a2, [(xs, 1.4), (xs, 1.1)]); sw(a2, xs, 0.8, 'T4'); wire(a2, [(xs, 0.5), (xs, 0.0)])
    # diodos de anclaje al neutro O
    a2.annotate('', xy=(xs-0.36, 3.6), xytext=(-0.8, 2.5), arrowprops=dict(arrowstyle='-|>', color='#c0392b', lw=1.3))
    a2.annotate('', xy=(-0.8, 2.5), xytext=(xs-0.36, 1.4), arrowprops=dict(arrowstyle='-|>', color='#c0392b', lw=1.3))
    wire(a2, [(-0.8, 2.5), (-1.6, 2.5)])
    a2.text(-0.95, 3.15, 'D1', fontsize=7.5, color='#c0392b'); a2.text(-0.95, 1.7, 'D2', fontsize=7.5, color='#c0392b')
    a2.text(0.3, -0.45, r'3 valores: $+\frac{V_{dc}}{2},\,0,\,-\frac{V_{dc}}{2}$', ha='center', fontsize=8.5, color='gray')

    # -------- (c) MMC --------
    a3.set_title('(c) MMC: brazos + submódulo', fontsize=10.5, fontweight='bold')
    a3.set_xlim(-0.6, 4.4); a3.set_ylim(-0.6, 5.4)
    a3.text(0.0, 5.15, r'$+V_{dc}/2$', ha='center', fontsize=8)
    a3.text(0.0, -0.35, r'$-V_{dc}/2$', ha='center', fontsize=8)
    # brazo superior (caja con N SM) + L_arm
    a3.add_patch(mpatches.FancyBboxPatch((-0.5, 3.5), 1.0, 0.9, boxstyle='round,pad=0.05', facecolor='#A9DFBF', edgecolor='navy', lw=1.5))
    a3.text(0.0, 3.95, 'N SM\n(sup.)', ha='center', va='center', fontsize=8, fontweight='bold')
    wire(a3, [(0, 5.0), (0, 4.4)])
    a3.add_patch(mpatches.FancyBboxPatch((-0.18, 2.9), 0.36, 0.45, boxstyle='round', facecolor='#FCF3CF', edgecolor='navy', lw=1.3)); a3.text(0.32, 3.12, r'$L_{arm}$', fontsize=7.5)
    wire(a3, [(0, 3.5), (0, 3.35)]); wire(a3, [(0, 2.9), (0, 2.55)])
    dot(a3, 0, 2.55); out(a3, 0, 2.55)
    a3.add_patch(mpatches.FancyBboxPatch((-0.18, 1.75), 0.36, 0.45, boxstyle='round', facecolor='#FCF3CF', edgecolor='navy', lw=1.3)); a3.text(0.32, 1.98, r'$L_{arm}$', fontsize=7.5)
    wire(a3, [(0, 2.55), (0, 2.2)]); wire(a3, [(0, 1.75), (0, 1.6)])
    a3.add_patch(mpatches.FancyBboxPatch((-0.5, 0.7), 1.0, 0.9, boxstyle='round,pad=0.05', facecolor='#A9DFBF', edgecolor='navy', lw=1.5))
    a3.text(0.0, 1.15, 'N SM\n(inf.)', ha='center', va='center', fontsize=8, fontweight='bold')
    wire(a3, [(0, 0.7), (0, 0.0)])
    # inset: submodulo half-bridge
    a3.add_patch(mpatches.FancyBboxPatch((2.1, 1.6), 2.0, 2.1, boxstyle='round,pad=0.05', facecolor='none', edgecolor='#888', lw=1, linestyle='--'))
    a3.text(3.1, 3.55, 'submódulo (half-bridge)', ha='center', fontsize=8, color='#555')
    sw(a3, 2.7, 3.0, 'S1'); sw(a3, 2.7, 2.1, 'S2')
    wire(a3, [(2.7, 2.76), (2.7, 2.34)])
    cap(a3, 3.7, 2.55, r'$C_{SM}$')
    wire(a3, [(2.35, 3.0), (2.05, 3.0)]); wire(a3, [(2.7, 3.24), (2.7, 3.4), (3.7, 3.4), (3.7, 2.62)])
    wire(a3, [(2.7, 1.86), (2.7, 1.7), (3.7, 1.7), (3.7, 2.48)])
    a3.text(1.95, 3.0, 'a', ha='right', fontsize=7.5); a3.text(1.95, 1.7, 'b', ha='right', fontsize=7.5)
    a3.plot([2.05], [1.7], 'o', color='navy', ms=3); wire(a3, [(2.05, 1.7), (2.7, 1.7)])
    a3.text(0.0, -0.55, 'N+1 valores', ha='center', fontsize=8.5, color='gray')

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    _savefig(fig, 'multinivel-circuitos', dpi=160)


def _btb_lazo_tension_verif():
    """Verificacion del lazo DC con los valores del ejemplo: Bode de L_dc con el
    margen de fase marcado y respuesta al escalon del lazo cerrado."""
    import matplotlib.pyplot as plt
    from scipy import signal

    C = 0.02; wci = 1885.0; wdc = wci/10; a = wci/wdc
    Kp = C*wdc/2; Ti = a/wdc
    numC = [Kp*Ti, Kp]; denC = [Ti, 0]        # PI
    numG = [2/C]; denG = [1, 0]               # planta 2/(Cs)
    numCl = [wci]; denCl = [1, wci]           # polo del lazo de corriente
    Lnum = np.convolve(np.convolve(numC, numG), numCl)
    Lden = np.convolve(np.convolve(denC, denG), denCl)
    L = signal.TransferFunction(Lnum, Lden)
    w = np.logspace(0, 4.5, 4000)
    _, mag, ph = signal.bode(L, w)

    n = max(len(Lden), len(Lnum))
    Tden = np.zeros(n); Tden[n-len(Lden):] += Lden; Tden[n-len(Lnum):] += Lnum
    T = signal.TransferFunction(Lnum, Tden)
    tt = np.linspace(0, 0.12, 1500)
    tt, y = signal.step(T, T=tt)

    fig = plt.figure(figsize=(13, 5.2))
    gs = fig.add_gridspec(2, 2, width_ratios=[1, 1], hspace=0.38, wspace=0.3)
    axm = fig.add_subplot(gs[0, 0]); axp = fig.add_subplot(gs[1, 0], sharex=axm)
    axs = fig.add_subplot(gs[:, 1])
    fig.suptitle('Verificación del lazo de tensión DC (valores del ejemplo)', fontsize=13, fontweight='bold')

    axm.semilogx(w, mag, color='navy', lw=2.2); axm.axhline(0, color='gray', ls='--', lw=0.9)
    axm.axvline(wdc, color='darkred', ls=':', lw=1.3)
    axm.text(wdc, mag.max()-6, r'$\omega_{dc}$', color='darkred', fontsize=9, ha='right', rotation=90, va='top')
    axm.set_ylabel('|L| (dB)'); axm.grid(alpha=0.3, which='both')
    axm.set_title(r'(a) Bode de $L_{dc}$: margen de fase', fontsize=9.5, fontweight='bold')

    axp.semilogx(w, ph, color='navy', lw=2.2); axp.axhline(-180, color='gray', ls='--', lw=0.9)
    axp.axvline(wdc, color='darkred', ls=':', lw=1.3)
    PM = 180 + np.interp(wdc, w, ph)
    axp.plot([wdc], [-180+PM], 'o', color='darkred', ms=7)
    axp.annotate(f'PM ≈ {PM:.0f}°\nen $\\omega_{{dc}}={wdc:.0f}$ rad/s', xy=(wdc, -180+PM),
                 xytext=(wdc/45, -125), color='darkred', fontsize=9,
                 arrowprops=dict(arrowstyle='->', color='darkred'))
    axp.set_ylabel('fase (°)'); axp.set_xlabel('ω (rad/s)'); axp.grid(alpha=0.3, which='both')

    axs.plot(tt*1000, y, color='navy', lw=2.4); axs.axhline(1, color='gray', ls='--', lw=0.9)
    axs.set_xlabel('tiempo (ms)'); axs.set_ylabel(r'$w/w^*$')
    axs.set_title('(b) Respuesta al escalón (lazo cerrado)', fontsize=9.5, fontweight='bold')
    axs.grid(alpha=0.3)
    over = (y.max()-1)*100
    axs.text(0.55, 0.12, f'sobreoscilación ≈ {over:.0f}%\n(PM alto → bien amortiguado)',
             transform=axs.transAxes, fontsize=9, color='gray', ha='center')

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    _savefig(fig, 'btb-lazo-tension-verif', dpi=160)


def _btb_rizado_L():
    """Rizado de corriente en L: (a) tension conmutada y triangulo de corriente
    en el peor caso (referencia por cero, duty 50%); (b) amplitud del rizado a lo
    largo del periodo fundamental, maxima donde la referencia pasa por cero."""
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(14, 5.4))
    gs = fig.add_gridspec(2, 2, width_ratios=[1, 1.05], hspace=0.4, wspace=0.3)
    axV = fig.add_subplot(gs[0, 0])
    axI = fig.add_subplot(gs[1, 0], sharex=axV)
    axE = fig.add_subplot(gs[:, 1])
    fig.suptitle('Rizado de corriente en la inductancia del filtro', fontsize=13, fontweight='bold')

    Ts = 1.0
    t = np.linspace(0, 2*Ts, 2000)
    vconv = np.where((t % Ts) < 0.5*Ts, 0.5, -0.5)
    axV.step(t, vconv, where='post', color='navy', lw=2, label=r'$v_{conv}$ ($\pm V_{dc}/2$)')
    axV.axhline(0, color='#c0392b', lw=1.6, ls='--', label=r'$\bar v=0$ (referencia)')
    axV.set_ylabel(r'$v/V_{dc}$'); axV.set_ylim(-0.8, 0.9)
    axV.legend(fontsize=7.5, loc='upper right'); axV.grid(alpha=0.3)
    axV.set_title('(a) Peor caso: referencia por cero → duty 50%', fontsize=9.5, fontweight='bold')
    axV.annotate('', xy=(0.5*Ts, 0.66), xytext=(0, 0.66), arrowprops=dict(arrowstyle='<->', color='gray'))
    axV.text(0.25*Ts, 0.72, r'$t_{on}=T_s/2$', ha='center', fontsize=8, color='gray')

    itri = np.where((t % Ts) < 0.5*Ts, (t % Ts)/(0.5*Ts), 1 - ((t % Ts)-0.5*Ts)/(0.5*Ts))
    axI.plot(t, itri, color='#e08a00', lw=2.2)
    axI.set_ylabel(r'$i_L$ (rizado)'); axI.set_xlabel(r'tiempo $/\,T_s$')
    axI.grid(alpha=0.3); axI.set_ylim(-0.15, 1.3)
    axI.annotate('', xy=(0.5*Ts, 0), xytext=(0.5*Ts, 1), arrowprops=dict(arrowstyle='<->', color='#c0392b', lw=1.6))
    axI.text(0.54*Ts, 0.5, r'$\Delta i_{L,max}$', color='#c0392b', fontsize=9.5, va='center')
    axI.text(0.12*Ts, 0.62, r'pendiente $\dfrac{V_{dc}/2}{L}$', fontsize=8, color='#a06000', rotation=30)

    m = 0.9
    th = np.linspace(0, 2*np.pi, 600)
    env = 1 - m**2*np.sin(th)**2
    axE.plot(np.degrees(th), env, color='navy', lw=2.4, label=r'$\Delta i_L(\theta)/\Delta i_{L,max}=1-m^2\sin^2\theta$')
    axE.plot(np.degrees(th), 0.5*(1+m*np.sin(th)), color='#c0392b', lw=1.4, ls='--', label=r'duty $d(\theta)=\frac{1}{2}(1+m\sin\theta)$')
    axE.plot(np.degrees(th), np.abs(m*np.sin(th)), color='#7f8c8d', lw=1.2, ls=':', label=r'|referencia| $|m\sin\theta|$')
    for thm in [0, 180, 360]:
        axE.plot([thm], [1], 'o', color='navy', ms=6)
    axE.axhline(1, color='gray', lw=0.7, ls=':')
    axE.annotate('máximo donde\nla referencia = 0', xy=(180, 1), xytext=(230, 0.72),
                 fontsize=8.5, color='navy', ha='center', arrowprops=dict(arrowstyle='->', color='navy'))
    axE.text(90, (1-m**2)-0.06, r'mínimo en el pico ($1-m^2$)', fontsize=8, ha='center', color='gray')
    axE.set_xlabel(r'$\theta$ (°)'); axE.set_ylabel('rizado normalizado / duty')
    axE.set_title('(b) Rizado a lo largo del periodo fundamental', fontsize=9.5, fontweight='bold')
    axE.legend(fontsize=7.3, loc='lower center'); axE.grid(alpha=0.3); axE.set_xlim(0, 360); axE.set_ylim(0, 1.18)

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    _savefig(fig, 'btb-rizado-L', dpi=160)


def _btb_perdidas():
    """Perdidas del VSC: (a) caracteristica de conduccion v_ce=Vce0+Rce*i,
    (b) corriente por el IGBT i(theta)*d(theta) sobre un periodo, (c) reparto
    de perdidas (conduccion vs conmutacion, IGBT vs diodo)."""
    import matplotlib.pyplot as plt

    fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(15.5, 4.6))
    fig.suptitle('Pérdidas del convertidor: de dónde salen', fontsize=13, fontweight='bold')

    # (a) caracteristica de conduccion
    Vce0, Rce = 1.0, 0.001
    ii = np.linspace(0, 2600, 200)
    a1.plot(ii, Vce0 + Rce*ii, color='navy', lw=2.4, label=r'modelo $v_{ce}=V_{ce0}+R_{ce}i$')
    a1.plot(ii, 0.78 + Rce*ii*1.02 + 0.22*np.tanh(ii/300), color='#e08a00', lw=1.6, ls='--', label='curva real (aprox.)')
    a1.axhline(Vce0, color='gray', lw=0.8, ls=':')
    a1.annotate(r'$V_{ce0}$ (umbral)', xy=(0, Vce0), xytext=(600, 1.35), fontsize=9,
                arrowprops=dict(arrowstyle='->', color='gray'))
    a1.annotate(r'pendiente $R_{ce}$', xy=(1800, Vce0+Rce*1800), xytext=(700, 2.7), fontsize=9,
                arrowprops=dict(arrowstyle='->', color='gray'))
    a1.set_xlabel('corriente $i$ (A)'); a1.set_ylabel(r'$v_{ce}$ (V)')
    a1.set_title('(a) Característica de conducción', fontsize=10.5, fontweight='bold')
    a1.legend(fontsize=8); a1.grid(alpha=0.3); a1.set_ylim(0, 3.6)

    # (b) corriente por el IGBT sobre un periodo
    m = 0.9; Ihat = 2366.0
    th = np.linspace(0, 2*np.pi, 600)
    iph = Ihat*np.sin(th)
    d = 0.5*(1 + m*np.sin(th))
    iIGBT = np.where(iph > 0, iph*d, 0.0)
    a2.plot(np.degrees(th), iph, color='#999', lw=1.4, label=r'$i(\theta)=\hat I\sin\theta$ (fase)')
    a2.fill_between(np.degrees(th), 0, iIGBT, color='#AED6F1', alpha=0.8, label=r'$i\cdot d(\theta)$ (por el IGBT)')
    a2.plot(np.degrees(th), iIGBT, color='navy', lw=1.8)
    a2b = a2.twinx()
    a2b.plot(np.degrees(th), d, color='#c0392b', lw=1.5, ls='--', label=r'$d(\theta)=\frac{1}{2}(1+m\sin\theta)$')
    a2b.set_ylabel('duty $d$', color='#c0392b'); a2b.set_ylim(0, 1.05); a2b.tick_params(axis='y', colors='#c0392b')
    a2.axhline(0, color='k', lw=0.8)
    a2.set_xlabel(r'$\theta$ (°)'); a2.set_ylabel('corriente (A)')
    a2.set_title('(b) Corriente que pasa por el IGBT', fontsize=10.5, fontweight='bold')
    a2.set_xlim(0, 360); a2.grid(alpha=0.3)
    l1, la1 = a2.get_legend_handles_labels(); l2, la2 = a2b.get_legend_handles_labels()
    a2.legend(l1+l2, la1+la2, fontsize=7.5, loc='upper right')

    # (c) reparto de perdidas (numeros del ejemplo)
    labels = ['IGBT\ncond.', 'IGBT\nconm.', 'diodo\ncond.', 'diodo\nconm.']
    vals = [1877, 207, 0.4*1877, 0.4*207]
    cols = ['#2e86c1', '#5dade2', '#e67e22', '#f0b27a']
    a3.bar(labels, vals, color=cols, edgecolor='navy', lw=1.2)
    for i, v in enumerate(vals):
        a3.text(i, v+30, f'{v:.0f} W', ha='center', fontsize=8.5)
    a3.set_ylabel('pérdidas por dispositivo (W)')
    a3.set_title('(c) Reparto (ejemplo, plena carga)', fontsize=10.5, fontweight='bold')
    a3.grid(axis='y', alpha=0.3)
    a3.text(0.5, 0.9, 'domina la conducción', transform=a3.transAxes, ha='center', fontsize=9, color='gray', style='italic')

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    _savefig(fig, 'btb-perdidas', dpi=160)


def _btb_mppt():
    """MPPT del aerogenerador: (a) curva Cp(lambda) con lambda_opt; (b) potencia
    mecanica vs velocidad para varios vientos y el lugar MPPT."""
    import matplotlib.pyplot as plt

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.5, 4.6))
    fig.suptitle('MPPT del aerogenerador (§4.2)', fontsize=13, fontweight='bold')

    def Cp(lam, beta=0.0):
        li = 1.0/(lam + 0.08*beta) - 0.035/(beta**3 + 1)
        cp = 0.5176*(116*li - 0.4*beta - 5)*np.exp(-21*li) + 0.0068*lam
        return np.maximum(cp, 0)

    # (a) Cp(lambda)
    lam = np.linspace(0.1, 14, 400)
    cp = Cp(lam)
    lam_opt = lam[np.argmax(cp)]; cp_max = cp.max()
    a1.plot(lam, cp, color='navy', lw=2.4)
    a1.plot([lam_opt], [cp_max], 'o', color='#c0392b', ms=8)
    a1.axvline(lam_opt, color='#c0392b', lw=1, ls=':')
    a1.annotate(f'$C_{{p,max}}\\approx{cp_max:.2f}$\n$\\lambda_{{opt}}\\approx{lam_opt:.1f}$',
                xy=(lam_opt, cp_max), xytext=(lam_opt+1.5, cp_max-0.08),
                fontsize=9, color='#c0392b', arrowprops=dict(arrowstyle='->', color='#c0392b'))
    a1.set_xlabel(r'$\lambda=\Omega_r R/v_w$ (velocidad específica)'); a1.set_ylabel(r'$C_p$')
    a1.set_title(r'(a) Coeficiente de potencia $C_p(\lambda)$', fontsize=10.5, fontweight='bold')
    a1.grid(alpha=0.3); a1.set_ylim(0, cp_max*1.15)

    # (b) P_mec vs Omega para varios vientos + lugar MPPT
    rho, R = 1.225, 40.0
    A = np.pi*R**2
    Om = np.linspace(0.3, 3.0, 400)
    for vw, col in [(7,'#5dade2'), (9,'#2e86c1'), (11,'#1a5276'), (13,'#154360')]:
        lam_v = Om*R/vw
        P = 0.5*rho*A*Cp(lam_v)*vw**3/1e6
        a2.plot(Om, np.maximum(P,0), color=col, lw=1.8, label=f'{vw} m/s')
    # lugar MPPT: P = k_opt Omega^3
    Om_opt = np.linspace(0.5, 2.6, 100)
    kopt = 0.5*rho*A*cp_max*(R/lam_opt)**3/1e6
    a2.plot(Om_opt, kopt*Om_opt**3, color='#c0392b', lw=2.4, ls='--', label='lugar MPPT\n$P\\propto\\Omega^3$')
    a2.set_xlabel(r'velocidad del rotor $\Omega_r$ (rad/s)'); a2.set_ylabel('$P_{mec}$ (MW)')
    a2.set_title('(b) Potencia y seguimiento MPPT', fontsize=10.5, fontweight='bold')
    a2.legend(fontsize=7.5, loc='upper left'); a2.grid(alpha=0.3); a2.set_ylim(0, None)

    plt.tight_layout(rect=[0, 0, 1, 0.93])
    _savefig(fig, 'btb-mppt', dpi=160)


def _btb_pmsg_modelo():
    """Modelo del PMSG: (a) maquina fisica (estator con devanados abc, rotor con
    iman) y modelo por fase de donde salen las ecuaciones; (b) desarrollo en dq."""
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    fig, (axA, axB) = plt.subplots(1, 2, figsize=(15, 7.8),
                                   gridspec_kw={'width_ratios': [1.05, 1.25]})
    fig.suptitle('Modelo del generador PMSG: del físico (abc) al dominio dq',
                 fontsize=13, fontweight='bold')

    # ================= (a) MODELO FÍSICO =================
    axA.set_aspect('equal'); axA.axis('off')
    axA.set_xlim(-3.4, 3.4); axA.set_ylim(-4.4, 3.6)
    axA.set_title('(a) Máquina física y modelo por fase (abc)', fontsize=10.5, fontweight='bold')

    cx, cy = 0.0, 1.2
    # estator (anillo) y entrehierro
    axA.add_patch(plt.Circle((cx, cy), 2.0, facecolor='#e8ebee', edgecolor='#555', lw=1.6, zorder=0))
    axA.add_patch(plt.Circle((cx, cy), 1.45, facecolor='white', edgecolor='#777', lw=1.1, zorder=1))
    axA.add_patch(plt.Circle((cx, cy), 1.2, facecolor='#f4f6f7', edgecolor='#999', lw=1.0, zorder=2))
    axA.text(cx, cy+2.28, 'estator (devanados a, b, c)', ha='center', fontsize=8.5, color='#555')

    # tres devanados de fase a 90, 210, 330
    for ang, lbl, col in [(90, 'a', '#c0392b'), (210, 'b', '#1e8449'), (330, 'c', '#2471a3')]:
        r = np.radians(ang)
        px, py = cx+1.72*np.cos(r), cy+1.72*np.sin(r)
        axA.add_patch(mpatches.FancyBboxPatch((px-0.24, py-0.16), 0.48, 0.32,
            boxstyle='round,pad=0.02', facecolor=col, edgecolor='k', lw=1, zorder=5))
        axA.text(px, py, lbl, color='white', fontsize=10, fontweight='bold', ha='center', va='center', zorder=6)

    # rotor: iman permanente (barra N-S) a un angulo theta_r
    th = np.radians(58)
    u = np.array([np.cos(th), np.sin(th)]); nn = np.array([-np.sin(th), np.cos(th)])
    c = np.array([cx, cy]); hl = 1.0; hw = 0.30
    for sign, col in [(+1, '#e15a5a'), (-1, '#5b8def')]:
        pts = [c+hw*nn, c-hw*nn, c-hw*nn+sign*hl*u, c+hw*nn+sign*hl*u]
        axA.add_patch(mpatches.Polygon(pts, closed=True, facecolor=col, edgecolor='k', lw=1, zorder=4))
    axA.text(*(c+0.55*hl*u), 'N', color='white', fontsize=10, fontweight='bold', ha='center', va='center', zorder=5)
    axA.text(*(c-0.55*hl*u), 'S', color='white', fontsize=10, fontweight='bold', ha='center', va='center', zorder=5)
    # flujo del iman
    axA.annotate('', xy=tuple(c+1.95*u), xytext=tuple(c+0.95*u),
                 arrowprops=dict(arrowstyle='-|>', color='#b5179e', lw=2.4), zorder=6)
    axA.text(*(c+2.2*u), r'$\psi_m$', color='#b5179e', fontsize=12, fontweight='bold', ha='center')
    # giro del rotor
    axA.annotate('', xy=(cx-0.5, cy+0.95), xytext=(cx+0.5, cy+0.95),
                 arrowprops=dict(arrowstyle='-|>', color='#333', lw=1.5, connectionstyle='arc3,rad=0.4'))
    axA.text(cx, cy+1.28, r'$\Omega$', fontsize=9, color='#333', ha='center')

    # circuito por fase (fase a) abajo
    yq = -2.4
    axA.text(-3.0, yq, 'fase a', fontsize=9, fontweight='bold', color='navy', ha='left')
    axA.plot([-2.3], [yq], 'o', color='navy', ms=5); axA.text(-2.3, yq+0.38, r'$v_a$', fontsize=9, ha='center')
    axA.plot([-2.3, -1.8], [yq, yq], 'navy', lw=1.5)
    axA.add_patch(mpatches.FancyBboxPatch((-1.8, yq-0.24), 0.72, 0.48, boxstyle='round,pad=0.02', facecolor='#FCF3CF', edgecolor='navy', lw=1.3))
    axA.text(-1.44, yq, r'$R_s$', ha='center', va='center', fontsize=9, fontweight='bold')
    axA.plot([-1.08, -0.68], [yq, yq], 'navy', lw=1.5)
    axA.add_patch(mpatches.FancyBboxPatch((-0.68, yq-0.24), 0.72, 0.48, boxstyle='round,pad=0.02', facecolor='#FCF3CF', edgecolor='navy', lw=1.3))
    axA.text(-0.32, yq, r'$L$', ha='center', va='center', fontsize=9, fontweight='bold')
    axA.plot([0.04, 0.66], [yq, yq], 'navy', lw=1.5)
    axA.add_patch(plt.Circle((1.02, yq), 0.34, facecolor='white', edgecolor='#c0392b', lw=1.6))
    axA.text(1.02, yq, '~', ha='center', va='center', fontsize=13, color='#c0392b')
    axA.text(1.02, yq-0.6, r'$e_a$ (fem)', ha='center', va='top', fontsize=8.5, color='#c0392b')
    axA.plot([1.36, 2.1], [yq, yq], 'navy', lw=1.5); axA.plot([2.1], [yq], 'o', color='navy', ms=5)
    axA.text(2.25, yq, 'neutro', fontsize=8, color='gray', va='center')
    axA.annotate('', xy=(-1.65, yq+0.32), xytext=(-2.1, yq+0.32), arrowprops=dict(arrowstyle='-|>', color='darkred', lw=1.3))
    axA.text(-1.87, yq+0.52, r'$i_a$', color='darkred', fontsize=8.5, ha='center')

    axA.text(0, -3.7,
             r'Por fase: $v_a=R_s i_a+\dfrac{d\lambda_a}{dt}$,   $\lambda_a=L\,i_a+\psi_m\cos\theta_r$   (ídem b, c a $\pm120°$).'
             '\nEl imán girando ($\\theta_r=\\omega_r t$) induce la fem $e_a=d(\\psi_m\\cos\\theta_r)/dt$.',
             ha='center', fontsize=8.5, color='#333')

    # ================= (b) MODELO EN dq =================
    axB.axis('off'); axB.set_xlim(0, 12); axB.set_ylim(0, 8)
    axB.set_title('(b) Modelo en dq (tras la transformación de Park)', fontsize=10.5, fontweight='bold')

    def rbox(x, y, txt, w=0.95):
        axB.add_patch(mpatches.FancyBboxPatch((x-w/2, y-0.32), w, 0.64,
            boxstyle='round,pad=0.03', facecolor='#FCF3CF', edgecolor='navy', lw=1.5))
        axB.text(x, y, txt, ha='center', va='center', fontsize=10, fontweight='bold')

    def src(x, y, txt, ec='navy', tcol='navy'):
        axB.add_patch(plt.Circle((x, y), 0.33, facecolor='white', edgecolor=ec, lw=1.6))
        axB.text(x, y, '~', ha='center', va='center', fontsize=12, color=tcol)
        axB.text(x, y-0.62, txt, ha='center', va='top', fontsize=8.5, color=tcol)

    def wire(x1, x2, y):
        axB.plot([x1, x2], [y, y], 'navy', lw=1.6)

    def port(x, y, lbl):
        axB.plot([x], [y], 'o', color='navy', ms=6)
        if lbl:
            axB.text(x, y+0.42, lbl, fontsize=10, ha='center')

    def icur(x, y, lbl):
        axB.annotate('', xy=(x+0.5, y+0.3), xytext=(x, y+0.3), arrowprops=dict(arrowstyle='-|>', color='darkred', lw=1.4))
        axB.text(x+0.25, y+0.55, lbl, color='darkred', fontsize=9, ha='center')

    axB.text(6.0, 7.3, r'Términos $\omega_r L\,i$: acoplamiento cruzado d$\leftrightarrow$q (fem de velocidad)',
             ha='center', fontsize=8.5, color='gray')

    # eje d
    yd = 5.6
    axB.text(0.4, yd, 'eje d', fontsize=10, fontweight='bold', color='navy', ha='center')
    port(1.2, yd, r'$v_d$'); icur(1.4, yd, r'$i_d$')
    wire(1.2, 1.85, yd); rbox(2.35, yd, r'$R_s$'); wire(2.83, 3.35, yd)
    rbox(3.85, yd, r'$L_d$'); wire(4.33, 5.37, yd)
    src(5.7, yd, r'$-\omega_r L_q i_q$'); wire(6.03, 7.3, yd)
    port(7.3, yd, ''); axB.text(7.5, yd, 'neutro', fontsize=8, color='gray', va='center')

    # eje q
    yqq = 2.4
    axB.text(0.4, yqq, 'eje q', fontsize=10, fontweight='bold', color='navy', ha='center')
    port(1.2, yqq, r'$v_q$'); icur(1.4, yqq, r'$i_q$')
    wire(1.2, 1.85, yqq); rbox(2.35, yqq, r'$R_s$'); wire(2.83, 3.35, yqq)
    rbox(3.85, yqq, r'$L_q$'); wire(4.33, 5.37, yqq)
    src(5.7, yqq, r'$\omega_r L_d i_d$'); wire(6.03, 7.67, yqq)
    src(8.0, yqq, r'$\omega_r\psi_m$', ec='#c0392b', tcol='#c0392b'); wire(8.33, 9.6, yqq)
    port(9.6, yqq, ''); axB.text(9.8, yqq, 'neutro', fontsize=8, color='gray', va='center')

    axB.annotate('fem del imán:\nsolo en el eje q',
                 xy=(8.0, yqq-0.9), xytext=(8.5, 0.7),
                 fontsize=8.5, color='#c0392b', ha='center',
                 arrowprops=dict(arrowstyle='->', color='#c0392b'))

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    _savefig(fig, 'btb-pmsg-modelo', dpi=165)


def _btb_ff_loop():
    """Diagrama de bloques detallado del lazo de tension DC con feedforward:
    dinamicas G_cl y F_FF explicitas y los dos caminos de P_MSC hacia el nudo
    de balance (directo y por la rama de feedforward)."""
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    fig, ax = plt.subplots(1, 1, figsize=(15, 8.5))
    ax.set_xlim(0, 15); ax.set_ylim(0, 9); ax.axis('off')
    ax.set_title('Lazo de tensión del bus DC con feedforward de potencia',
                 fontsize=13, fontweight='bold', pad=8)

    def box(x, y, w, h, txt, col, fs=10):
        ax.add_patch(mpatches.FancyBboxPatch((x-w/2, y-h/2), w, h,
            boxstyle='round,pad=0.06', facecolor=col, edgecolor='navy', lw=1.6))
        ax.text(x, y, txt, ha='center', va='center', fontsize=fs, fontweight='bold')

    def circ(x, y, lbl, col='navy', r=0.28):
        ax.add_patch(plt.Circle((x, y), r, facecolor='white', edgecolor=col, lw=1.6))
        ax.text(x, y, lbl, ha='center', va='center', fontsize=11, fontweight='bold', color=col)

    def arr(x1, y1, x2, y2, col='navy', lbl='', dy=0.22, lw=1.8):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='-|>', color=col, lw=lw))
        if lbl:
            ax.text((x1+x2)/2, max(y1, y2)+dy, lbl, ha='center', fontsize=9, color='darkred')

    y = 6.0
    # cadena principal
    ax.text(0.4, y, r'$w^*=V_{dc}^{*2}$', ha='center', va='center', fontsize=10)
    arr(0.95, y, 1.25, y)
    circ(1.55, y, '−')
    arr(1.83, y, 2.4, y, lbl=r'$e_w$')
    box(3.05, y, 1.3, 0.8, r'$PI_{dc}$', '#AED6F1')
    arr(3.7, y, 4.45, y, lbl=r'$i_{d,PI}^*$')
    circ(4.75, y, '+')
    arr(5.03, y, 5.7, y, lbl=r'$i_d^*$')
    box(6.5, y, 1.6, 0.9, r'$G_{cl}=\dfrac{\omega_{ci}}{s+\omega_{ci}}$', '#A9DFBF', 9.5)
    arr(7.3, y, 7.9, y, lbl=r'$i_d$')
    box(8.6, y, 1.5, 0.8, r'$\times\,1.5\,v_{d,g}$', '#FCF3CF', 9)
    arr(9.35, y, 9.95, y, lbl=r'$P_{GSC}$')
    circ(10.3, y, '−')
    arr(10.58, y, 11.15, y, lbl=r'$P_{net}$')
    box(11.9, y, 1.4, 0.9, r'$\dfrac{2}{C_{dc}s}$', '#FAD7A0', 11)
    arr(12.6, y, 13.3, y)
    ax.text(13.75, y, r'$w=V_{dc}^2$', ha='center', va='center', fontsize=10)

    # realimentacion
    ax.plot([13.05, 13.05, 1.55], [y, y-1.4, y-1.4], 'navy', lw=1.6)
    ax.annotate('', xy=(1.55, y-0.28), xytext=(1.55, y-1.4),
                arrowprops=dict(arrowstyle='-|>', color='navy', lw=1.6))

    # ---- P_MSC y sus dos caminos (verde) ----
    g = 'darkgreen'
    ym = 8.1
    ax.text(6.2, ym+0.25, r'$P_{MSC}$ (perturbación, medida del MSC)', ha='center', fontsize=9.5, color=g, fontweight='bold')
    ax.plot([1.8, 10.3], [ym, ym], color=g, lw=1.8)
    ax.plot([6.2], [ym], marker='o', color=g, ms=6)   # nudo de reparto

    # camino directo: P_MSC -> nudo de balance (+)
    ax.annotate('', xy=(10.3, y+0.28), xytext=(10.3, ym),
                arrowprops=dict(arrowstyle='-|>', color=g, lw=1.8))
    ax.text(10.5, (ym+y)/2, 'directo (+)', ha='left', fontsize=8.5, color=g)

    # camino feedforward: P_MSC -> F_FF -> /1.5vdg -> suma (+)
    ax.plot([1.8, 1.8], [ym, 3.58], color=g, lw=1.8)
    box(1.8, 3.2, 1.5, 0.75, r'$F_{FF}=\dfrac{1}{T_{FF}s+1}$', '#ABEBC6', 8.5)
    arr(2.55, 3.2, 4.05, 3.2, col=g)
    box(4.75, 3.2, 1.4, 0.75, r'$\div\,1.5\,v_{d,g}$', '#ABEBC6', 8.5)
    ax.text(5.35, 3.2, r'$i_{d,FF}^*$', ha='left', va='center', fontsize=9, color=g)
    ax.annotate('', xy=(4.75, y-0.28), xytext=(4.75, 3.58),
                arrowprops=dict(arrowstyle='-|>', color=g, lw=1.8))
    ax.text(5.05, 4.9, 'feedforward (+)', ha='left', fontsize=8.5, color=g)

    # anotacion de cancelacion
    ax.text(7.5, 0.7,
            r'En el nudo de balance: $P_{net}=P_{MSC}-P_{GSC}=P_{MSC}\,(1-G_{cl}F_{FF})-1.5v_{d,g}G_{cl}i_{d,PI}^*$'
            '\n'
            r'Si $G_{cl}F_{FF}\approx1$, los dos caminos verdes de $P_{MSC}$ se cancelan y la perturbación no llega al integrador',
            ha='center', fontsize=9.5,
            bbox=dict(boxstyle='round', facecolor='#EAFAF1', edgecolor='darkgreen'))

    plt.tight_layout()
    _savefig(fig, "btb-ff-loop", dpi=170)


def _btb_dq_transformacion():
    """Diagrama vectorial: marcos abc, alfa-beta y dq (girando con v_g), con la
    orientacion VOC (v_g sobre el eje d) y la descomposicion de la corriente."""
    import matplotlib.pyplot as plt

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13, 6.2))

    # ---- Panel izquierdo: los tres marcos ----
    axL.set_aspect('equal'); axL.axis('off')
    axL.set_xlim(-1.5, 1.6); axL.set_ylim(-1.4, 1.6)
    axL.set_title('Marcos de referencia: abc → αβ → dq', fontsize=11, fontweight='bold')

    def vec(ax, x, y, txt, col, lw=2.2, tx=None, ty=None, fs=11):
        ax.annotate('', xy=(x, y), xytext=(0, 0),
                    arrowprops=dict(arrowstyle='-|>', color=col, lw=lw))
        ax.text(tx if tx is not None else x*1.12, ty if ty is not None else y*1.12,
                txt, color=col, fontsize=fs, ha='center', va='center', fontweight='bold')

    # ejes abc (gris claro, a 0, 120, 240)
    for ang, lbl in [(0, 'a'), (120, 'b'), (240, 'c')]:
        r = np.radians(ang)
        axL.plot([0, 1.25*np.cos(r)], [0, 1.25*np.sin(r)], color='#c9c9c9', lw=1.4, ls='-')
        axL.text(1.38*np.cos(r), 1.38*np.sin(r), lbl, color='#9a9a9a', fontsize=10, ha='center', va='center')

    # ejes alfa-beta (fijos, gris oscuro)
    vec(axL, 1.15, 0, r'$\alpha$', '#555', lw=1.6, tx=1.28, ty=0)
    vec(axL, 0, 1.15, r'$\beta$', '#555', lw=1.6, tx=0, ty=1.28)

    # marco dq girado un angulo theta
    th = np.radians(35)
    d = np.array([np.cos(th), np.sin(th)])
    q = np.array([-np.sin(th), np.cos(th)])
    vec(axL, d[0], d[1], 'd', 'navy', lw=2.2, tx=d[0]*1.18, ty=d[1]*1.18)
    vec(axL, q[0]*0.95, q[1]*0.95, 'q', 'navy', lw=2.2, tx=q[0]*1.15, ty=q[1]*1.15)

    # vector v_g sobre el eje d (verde)
    vg = 1.0*d
    vec(axL, vg[0], vg[1], r'$\vec v_g$', 'darkgreen', lw=3.0, tx=vg[0]*0.62, ty=vg[1]*0.62+0.12, fs=12)

    # arco theta
    tt = np.linspace(0, th, 30)
    axL.plot(0.32*np.cos(tt), 0.32*np.sin(tt), color='navy', lw=1.3)
    axL.text(0.44*np.cos(th/2), 0.44*np.sin(th/2), r'$\theta=\omega_0 t$', color='navy', fontsize=9.5)

    axL.text(0, -1.32, 'El marco dq gira con $\\vec v_g$: en régimen las componentes son continuas',
             ha='center', fontsize=8.5, color='gray')

    # ---- Panel derecho: orientacion VOC y descomposicion de i ----
    axR.set_aspect('equal'); axR.axis('off')
    axR.set_xlim(-0.4, 1.7); axR.set_ylim(-1.2, 1.5)
    axR.set_title('Orientación VOC: $v_{q,g}=0$ y descomposición de $\\vec i$',
                  fontsize=11, fontweight='bold')

    # ejes d (horizontal) y q (vertical)
    axR.annotate('', xy=(1.55, 0), xytext=(-0.3, 0), arrowprops=dict(arrowstyle='-|>', color='navy', lw=1.8))
    axR.annotate('', xy=(0, 1.4), xytext=(0, -1.0), arrowprops=dict(arrowstyle='-|>', color='navy', lw=1.8))
    axR.text(1.6, -0.1, 'd', color='navy', fontsize=12, fontweight='bold')
    axR.text(0.08, 1.42, 'q', color='navy', fontsize=12, fontweight='bold')

    # v_g sobre d
    axR.annotate('', xy=(1.2, 0), xytext=(0, 0), arrowprops=dict(arrowstyle='-|>', color='darkgreen', lw=3))
    axR.text(0.6, 0.13, r'$\vec v_g = v_{d,g}$', color='darkgreen', fontsize=11, fontweight='bold')
    axR.text(1.24, -0.16, r'$v_{q,g}=0$', color='darkgreen', fontsize=9.5)

    # corriente i con componentes id, iq
    ix, iy = 0.85, 0.7
    axR.annotate('', xy=(ix, iy), xytext=(0, 0), arrowprops=dict(arrowstyle='-|>', color='darkred', lw=2.6))
    axR.text(ix+0.05, iy+0.1, r'$\vec i$', color='darkred', fontsize=12, fontweight='bold')
    axR.plot([ix, ix], [0, iy], color='darkred', lw=1.1, ls='--')
    axR.plot([0, ix], [iy, iy], color='darkred', lw=1.1, ls='--')
    axR.text(ix, -0.16, r'$i_d\;(\to P)$', color='darkred', fontsize=10, ha='center')
    axR.text(-0.06, iy, r'$i_q\;(\to Q)$', color='darkred', fontsize=10, ha='right', va='center')

    axR.text(0.6, -1.05,
             r'$P=\frac{3}{2}v_{d,g}i_d,\qquad Q=-\frac{3}{2}v_{d,g}i_q$',
             ha='center', fontsize=10,
             bbox=dict(boxstyle='round', facecolor='#EBF5FB', edgecolor='steelblue'))

    plt.tight_layout()
    _savefig(fig, "btb-dq-transformacion", dpi=160)


def _btb_lazo_corriente_bode():
    """Bode del lazo de corriente: planta 1/(Ls+R), PI con cancelacion de polo,
    y lazo abierto resultante = integrador puro (cruce w_ci, PM 90 grados)."""
    import matplotlib.pyplot as plt

    L, R = 0.25e-3, 0.05
    w_ci = 1885.0
    Kp = w_ci*L; Ti = L/R
    w = np.logspace(1, 5, 2000)
    s = 1j*w
    G = 1.0/(L*s + R)                      # planta
    C = Kp*(1 + Ti*s)/(Ti*s)               # PI
    Li = C*G                               # lazo abierto (= w_ci/s)

    fig, (a1, a2) = plt.subplots(2, 1, figsize=(9, 7.5), sharex=True)
    fig.suptitle('Lazo de corriente: cancelación de polo → integrador puro',
                 fontsize=12, fontweight='bold')

    a1.semilogx(w, 20*np.log10(np.abs(G)), color='#e08a00', lw=2, label=r'planta $G_i=\frac{1}{Ls+R}$')
    a1.semilogx(w, 20*np.log10(np.abs(C)), color='#2e86c1', lw=2, label=r'PI $C(s)$')
    a1.semilogx(w, 20*np.log10(np.abs(Li)), color='navy', lw=2.6, label=r'lazo abierto $L_i=\frac{\omega_{ci}}{s}$')
    a1.axhline(0, color='gray', lw=0.9, ls='--')
    a1.axvline(R/L, color='#e08a00', lw=1.1, ls=':')
    a1.text(R/L, a1.get_ylim()[1]-2 if False else 46, r'polo/cero $R/L$', rotation=90, va='top', ha='right', fontsize=8, color='#a06000')
    a1.axvline(w_ci, color='navy', lw=1.1, ls=':')
    a1.text(w_ci, 46, r'$\omega_{ci}$', rotation=90, va='top', ha='right', fontsize=8.5, color='navy')
    a1.set_ylabel('|·| (dB)'); a1.grid(True, which='both', alpha=0.3); a1.legend(fontsize=8.5, loc='lower left')

    a2.semilogx(w, np.degrees(np.angle(G)), color='#e08a00', lw=2)
    a2.semilogx(w, np.degrees(np.angle(C)), color='#2e86c1', lw=2)
    a2.semilogx(w, np.degrees(np.angle(Li)), color='navy', lw=2.6)
    a2.axhline(-90, color='gray', lw=0.9, ls='--')
    a2.axvline(w_ci, color='navy', lw=1.1, ls=':')
    a2.annotate('lazo abierto plano en −90° → PM = 90°', xy=(w_ci, -90), xytext=(w_ci/25, -55),
                color='navy', fontsize=9.5, arrowprops=dict(arrowstyle='->', color='navy'))
    a2.set_ylabel('fase (°)'); a2.set_xlabel('ω (rad/s)'); a2.grid(True, which='both', alpha=0.3)

    fig.text(0.5, 0.005, r'El cero del PI en $R/L$ cancela el polo de la planta: queda $L_i=\omega_{ci}/s$, '
             'un integrador puro que cruza 0 dB en $\\omega_{ci}$', ha='center', fontsize=9, color='gray')
    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    _savefig(fig, "btb-lazo-corriente-bode", dpi=160)


def _btb_lazo_tension_bode():
    """Bode del lazo de tension DC: doble integrador + cero del PI; cruce w_dc y PM."""
    import matplotlib.pyplot as plt

    Cdc = 0.02; w_ci = 1885.0; w_dc = w_ci/10
    a = w_ci/w_dc                         # factor del optimo simetrico (= 10)
    Kp = Cdc*w_dc/2; Ti = a/w_dc          # cero en w_dc/10, simetrico al polo w_ci
    w = np.logspace(0, 4.5, 2500)
    s = 1j*w
    Ldc = (2*Kp/(Cdc*Ti))*(Ti*s + 1)/s**2 * w_ci/(s + w_ci)   # incluye polo del lazo de corriente
    mag = 20*np.log10(np.abs(Ldc))
    ph = np.degrees(np.unwrap(np.angle(Ldc)))
    if ph[0] > 0:
        ph -= 360.0
    PM = np.degrees(np.arctan(a) - np.arctan(1.0/a))

    fig, (a1, a2) = plt.subplots(2, 1, figsize=(9, 7.5), sharex=True)
    fig.suptitle('Lazo de tensión DC: doble integrador + cero del PI',
                 fontsize=12, fontweight='bold')

    lineas = [(1/Ti, r'$\omega_{dc}/10$ (cero PI)', 'darkgreen'),
              (w_dc, r'$\omega_{dc}$ (cruce)', 'darkred'),
              (w_ci, r'$\omega_{ci}=10\,\omega_{dc}$ (polo lazo corr.)', 'darkorange')]

    a1.semilogx(w, mag, color='navy', lw=2.4)
    a1.axhline(0, color='gray', lw=0.9, ls='--')
    for wx, lbl, col in lineas:
        a1.axvline(wx, color=col, lw=1.2, ls=':')
        a1.text(wx, mag.max()-3, lbl, rotation=90, va='top', ha='right', fontsize=8, color=col)
    a1.text(0.03, 0.2, '−40 dB/dec', transform=a1.transAxes, fontsize=8.5, color='gray')
    a1.text(0.50, 0.42, '−20 dB/dec', transform=a1.transAxes, fontsize=8.5, color='gray')
    a1.set_ylabel('|L| (dB)'); a1.grid(True, which='both', alpha=0.3)

    a2.semilogx(w, ph, color='navy', lw=2.4)
    a2.axhline(-180, color='gray', lw=0.9, ls='--')
    for wx, lbl, col in lineas:
        a2.axvline(wx, color=col, lw=1.2, ls=':')
    a2.plot([w_dc], [-180+PM], 'o', color='darkred', ms=7)
    a2.annotate(f'PM = arctan(10) − arctan(0.1) ≈ {PM:.0f}°',
                xy=(w_dc, -180+PM), xytext=(w_dc/45, -180+PM+16),
                color='darkred', fontsize=9.5, arrowprops=dict(arrowstyle='->', color='darkred'))
    a2.set_ylabel('fase (°)'); a2.set_xlabel('ω (rad/s)'); a2.grid(True, which='both', alpha=0.3)

    fig.text(0.5, 0.005, r'Cero del PI ($\omega_{dc}/10$) y polo del lazo de corriente ($\omega_{ci}=10\,\omega_{dc}$) '
             r'colocados simétricos respecto al cruce $\omega_{dc}$ (media geométrica): óptimo simétrico, $PM\approx79°$',
             ha='center', fontsize=9, color='gray')
    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    _savefig(fig, "btb-lazo-tension-bode", dpi=160)


def _optimo_simetrico():
    """Bode de la ganancia de lazo del optimo simetrico: el cero del PI y el polo
    de la planta quedan simetricos respecto a la frecuencia de cruce (media
    geometrica), y la fase alcanza su maximo (maximo PM) justo en el cruce."""
    import matplotlib.pyplot as plt

    T_sig = 1.0          # retardo pequeno equivalente T_Sigma
    a = 3.0              # factor del optimo simetrico
    Ti = a**2 * T_sig    # tiempo integral
    Ks = 1.0
    Kp = 1.0/(a*Ks*T_sig)

    w = np.logspace(-2, 2, 3000)
    s = 1j*w
    L = Kp*Ks*(1+s*Ti)/(s**2 * Ti * (1+s*T_sig))
    mag = 20*np.log10(np.abs(L))
    ph = np.degrees(np.unwrap(np.angle(L)))
    if ph[0] > 0:
        ph -= 360.0

    wz = 1.0/Ti          # cero del PI
    wc = 1.0/(a*T_sig)   # cruce (media geometrica de wz y wp)
    wp = 1.0/T_sig       # polo de la planta
    PM = np.degrees(np.arctan(a) - np.arctan(1.0/a))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 7.5), sharex=True)
    fig.suptitle('Óptimo simétrico: Bode de la ganancia de lazo  '
                 r'$L(s)=K_p K_s\dfrac{1+sT_i}{s^2 T_i(1+sT_\Sigma)}$  (a = 3)',
                 fontsize=12, fontweight='bold')

    lines = [(wz, r'$1/T_i$ (cero PI)', 'darkgreen'),
             (wc, r'$\omega_c$ (cruce)', 'darkred'),
             (wp, r'$1/T_\Sigma$ (polo planta)', 'darkorange')]

    ax1.semilogx(w, mag, color='navy', lw=2.2)
    ax1.axhline(0, color='gray', lw=0.9, ls='--')
    for wx, lbl, col in lines:
        ax1.axvline(wx, color=col, lw=1.3, ls=':')
        ax1.text(wx, mag.max()-2, lbl, rotation=90, va='top', ha='right',
                 fontsize=8.5, color=col)
    ax1.text(0.02, 0.15, '−40 dB/dec', transform=ax1.transAxes, fontsize=8.5, color='gray')
    ax1.text(0.44, 0.55, '−20 dB/dec', transform=ax1.transAxes, fontsize=8.5, color='gray')
    ax1.text(0.80, 0.30, '−40 dB/dec', transform=ax1.transAxes, fontsize=8.5, color='gray')
    ax1.set_ylabel('|L|  (dB)'); ax1.grid(True, which='both', alpha=0.3)

    ax2.semilogx(w, ph, color='navy', lw=2.2)
    ax2.axhline(-180, color='gray', lw=0.9, ls='--')
    for wx, lbl, col in lines:
        ax2.axvline(wx, color=col, lw=1.3, ls=':')
    ax2.plot([wc], [-180+PM], 'o', color='darkred', ms=7)
    ax2.annotate(f'PM = arctan(a) − arctan(1/a) = {PM:.0f}°',
                 xy=(wc, -180+PM), xytext=(wc*1.6, -180+PM+22),
                 color='darkred', fontsize=10,
                 arrowprops=dict(arrowstyle='->', color='darkred', lw=1.4))
    ax2.set_ylabel('∠L  (°)'); ax2.set_xlabel('ω  (rad/s, escala log)')
    ax2.grid(True, which='both', alpha=0.3)

    fig.text(0.5, 0.005,
             r'$\omega_c$ es la media geométrica de $1/T_i$ y $1/T_\Sigma$ → el Bode es simétrico '
             'y la fase alcanza su máximo (máximo PM) justo en el cruce',
             ha='center', fontsize=9, color='gray')
    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    _savefig(fig, "optimo-simetrico-bode", dpi=160)


def main():
    pref = sys.argv[1] if len(sys.argv) > 1 else None
    n = 0
    for slug, fn in REGISTRY:
        if pref and not slug.startswith(pref):
            continue
        fn(); n += 1
    if pref is None or "analisis-modal".startswith(pref):
        _modal_extended()
        n += 1
    if pref is None or "pll-srf".startswith(pref):
        _pll_extended()
        n += 1
    if pref is None or "dinamica-bus-dc".startswith(pref):
        _busdc_extended()
        n += 1
    if pref is None or "respuesta-segundo-orden".startswith(pref):
        _segundoorden_extended()
        n += 1
    if pref is None or "desacoplo-dq".startswith(pref):
        _desacoplo_extended()
        n += 1
    if pref is None or "funcion-transferencia".startswith(pref):
        _ft_extended()
        n += 1
    if pref is None or "polos-ceros".startswith(pref):
        _polosceros_extended()
        n += 1
    if pref is None or "sistema-trifasico".startswith(pref):
        _trifasico_extended()
        n += 1
    if pref is None or "potencia-ac-fasores".startswith(pref):
        _potfasor_extended()
        n += 1
    if pref is None or "resonancia-rlc".startswith(pref):
        _rlc_extended()
        n += 1
    if pref is None or "control-tension-bus-dc".startswith(pref):
        _vdc_extended()
        n += 1
    if pref is None or "representacion-espacio-estados".startswith(pref):
        _ss_extended()
        n += 1
    if pref is None or "linealizacion-teoria".startswith(pref):
        _lin_extended()
        n += 1
    if pref is None or "transformada-laplace".startswith(pref):
        _laplace_extended()
        n += 1
    if pref is None or "variables-estado".startswith(pref):
        _varestado_extended()
        n += 1
    if pref is None or "realimentacion".startswith(pref):
        _realim_extended()
        n += 1
    if pref is None or "routh-hurwitz".startswith(pref):
        _routh_extended()
        n += 1
    if pref is None or "criterio-nyquist".startswith(pref):
        _nyquist_extended()
        n += 1
    if pref is None or "error-regimen-permanente".startswith(pref):
        _esserror_extended()
        n += 1
    if pref is None or "anti-windup".startswith(pref):
        _antiwindup_extended()
        n += 1
    if pref is None or "compensacion-retardo".startswith(pref):
        _delay_extended()
        n += 1
    if pref is None or "control-feedforward".startswith(pref):
        _ff_extended()
        n += 1
    if pref is None or "control-vectorial".startswith(pref):
        _vector_extended()
        n += 1
    if pref is None or "estabilidad-bibo".startswith(pref):
        _bibo_extended()
        n += 1
    if pref is None or "estabilidad-lyapunov".startswith(pref):
        _lyap_extended()
        n += 1
    if pref is None or "gain-scheduling".startswith(pref):
        _gsched_extended()
        n += 1
    if pref is None or "matching-control".startswith(pref):
        _match_extended()
        n += 1
    if pref is None or "impedancia-virtual".startswith(pref):
        _zvirt_extended()
        n += 1
    if pref is None or "fault-ride-through".startswith(pref):
        _frt_extended()
        n += 1
    if pref is None or "filtro-notch".startswith(pref):
        _notch_extended()
        n += 1
    if pref is None or "interaccion-pll-red-debil".startswith(pref):
        _pllweak_extended()
        n += 1
    if pref is None or "transformador".startswith(pref):
        _trafo_extended()
        n += 1
    if pref is None or "componentes-simetricas".startswith(pref):
        _simetricas_extended()
        n += 1
    if pref is None or "transferencia-potencia-linea".startswith(pref):
        _pdelta_extended()
        n += 1
    if pref is None or "sistema-por-unidad".startswith(pref):
        _pu_extended()
        n += 1
    if pref is None or "potencia-instantanea-dq".startswith(pref):
        _potdq_extended()
        n += 1
    if pref is None or "maquina-induccion".startswith(pref):
        _induc_extended()
        n += 1
    if pref is None or "microrred-hibrida-ac-dc".startswith(pref):
        _hybrid_extended()
        n += 1
    if pref is None or "generador-sincrono".startswith(pref):
        _sg_extended()
        n += 1
    if pref is None or "linealizacion-numerica".startswith(pref):
        _linnumerica_extended()
        n += 1
    if pref is None or "respuesta-frecuencia-ss".startswith(pref):
        _freqss_extended()
        n += 1
    if pref is None or "medicion-impedancia-inyeccion".startswith(pref):
        _measz_extended()
        n += 1
    if pref is None or "barrido-parametrico".startswith(pref):
        _barrido_extended()
        n += 1
    if pref is None or "discretizacion-controladores".startswith(pref):
        _disc_extended()
        n += 1
    if pref is None or "lugar-raices".startswith(pref):
        _rlocus_extended()
        n += 1
    if pref is None or "muestreo-aliasing".startswith(pref):
        _aliasing_extended()
        n += 1
    if pref is None or "transformada-z".startswith(pref):
        _ztransform_extended()
        n += 1
    if pref is None or "droop-dc".startswith(pref):
        _droopdc_extended()
        n += 1
    if pref is None or "rectificador-afe".startswith(pref):
        _afe_extended()
        n += 1
    if pref is None or "statcom-svc".startswith(pref):
        _statcom_extended()
        n += 1
    if pref is None or "ecuacion-oscilacion".startswith(pref):
        _swing_extended()
        n += 1
    if pref is None or "armonicos-thd-convertidores".startswith(pref):
        _thd_extended()
        n += 1
    if pref is None or "convertidor-dc-dc".startswith(pref):
        _dcdc_extended()
        n += 1
    if pref is None or "fotovoltaica-mppt".startswith(pref):
        _pv_extended()
        n += 1
    if pref is None or "eolica-mppt".startswith(pref):
        _mppt_extended()
        n += 1
    if pref is None or "modelo-bateria-bess".startswith(pref):
        _bess_extended()
        n += 1
    if pref is None or "diagrama-bloques".startswith(pref):
        _diagrama_bloques_analisis()
        n += 1
    if pref is None or "series-fourier".startswith(pref):
        _series_fourier_analisis()
        n += 1
    if pref is None or "controlador-resonante".startswith(pref):
        _controlador_resonante_analisis()
        n += 1
    if pref is None or "power-synchronization-control".startswith(pref):
        _power_synchronization_control_analisis()
        n += 1
    if pref is None or "compensador-adelanto-atraso".startswith(pref):
        _compensador_adelanto_atraso_analisis()
        n += 1
    if pref is None or "frecuencias-segundo-orden".startswith(pref):
        _frecuencias_segundo_orden_analisis()
        n += 1
    if pref is None or "antiresonancia".startswith(pref):
        _antires_extended()
        n += 1
    if pref is None or "amortiguamiento-pasivo-vs-activo".startswith(pref):
        _amort_pasivo_activo_extended()
        n += 1
    if pref is None or "deteccion-islanding".startswith(pref):
        _ndz_extended()
        n += 1
    if pref is None or "fenomenos-oscilatorios-red".startswith(pref):
        _sso_extended()
        n += 1
    if pref is None or "series-taylor".startswith(pref):
        _taylor_extended()
        n += 1
    if pref is None or "virtual-oscillator-control".startswith(pref):
        _voc_extended()
        n += 1
    if pref is None or "asignacion-polos-lqr".startswith(pref):
        _lqrext()
        n += 1
    if pref is None or "control-predictivo".startswith(pref):
        _mpcext()
        n += 1
    if pref is None or "robustez-parametrica".startswith(pref):
        _robext()
        n += 1
    if pref is None or "valores-singulares-mimo".startswith(pref):
        _svdext()
        n += 1
    if pref is None or "clasificacion-estabilidad".startswith(pref):
        _clasest()
        n += 1
    if pref is None or "semiconductores-potencia".startswith(pref):
        _semipow()
        n += 1
    if pref is None or "topologias-multinivel".startswith(pref):
        _multilev()
        n += 1
    if pref is None or "impedancia-reactancia".startswith(pref):
        _zxext()
        n += 1
    if pref is None or "valor-rms-factor-potencia".startswith(pref):
        _vrmsext()
        n += 1
    if pref is None or "modelo-linea-distribucion".startswith(pref):
        _linedist()
        n += 1
    if pref is None or "metodos-sintesis-control".startswith(pref):
        _syntext()
        n += 1
    if pref is None or "arquitecturas-control".startswith(pref):
        _archctrl()
        n += 1
    if pref is None or "control-robusto-hinf".startswith(pref):
        _hinfext()
        n += 1
    if pref is None or "validacion-cruzada".startswith(pref):
        _valcruz_analisis()
        n += 1
    if pref is None or "niveles-validacion".startswith(pref):
        _nivval_analisis()
        n += 1
    if pref is None or "ciclo-diseno-control".startswith(pref):
        _cicdis_analisis()
        n += 1
    if pref is None or "especificaciones-control".startswith(pref):
        _espctrl_analisis()
        n += 1
    if pref is None or "pruebas-validacion".startswith(pref):
        _prueba_analisis()
        n += 1
    if pref is None or "calidad-potencia".startswith(pref):
        _calpot_analisis()
        n += 1
    if pref is None or "simulacion-conmutada".startswith(pref):
        _conmut_analisis()
        n += 1
    if pref is None or "fft-analisis-espectral".startswith(pref):
        _fftanal_analisis()
        n += 1
    if pref is None or "hil-phil".startswith(pref):
        _hilphil_analisis()
        n += 1
    if pref is None or "equilibrio-fsolve".startswith(pref):
        _fsolve_analisis()
        n += 1
    if pref is None or "integracion-edos-stiff".startswith(pref):
        _stiff_analisis()
        n += 1
    if pref is None or "armonicos-thd".startswith(pref):
        _thdext()
        n += 1
    if pref is None or "convertidor-dc-dc-analisis".startswith(pref):
        _convertidor_dc_dc_analisis()
        n += 1
    if pref is None or "fotovoltaica-mppt-analisis".startswith(pref):
        _fotovoltaica_mppt_analisis()
        n += 1
    if pref is None or "eolica-mppt-analisis".startswith(pref):
        _eolica_mppt_analisis()
        n += 1
    if pref is None or "sistema-primer-orden-analisis".startswith(pref):
        _sistema_primer_orden_analisis()
        n += 1
    if pref is None or "current-limiting-analisis".startswith(pref):
        _current_limiting_analisis()
        n += 1
    if pref is None or "controlabilidad-observabilidad-analisis".startswith(pref):
        _controlabilidad_observabilidad_analisis()
        n += 1
    if pref is None or "observador-estados-analisis".startswith(pref):
        _observador_estados_analisis()
        n += 1
    if pref is None or "control-repetitivo-analisis".startswith(pref):
        _control_repetitivo_analisis()
        n += 1
    if pref is None or "diagrama-bloques-analisis".startswith(pref):
        _diagrama_bloques_analisis()
        n += 1
    if pref is None or "series-fourier-analisis".startswith(pref):
        _series_fourier_analisis()
        n += 1
    if pref is None or "controlador-resonante-analisis".startswith(pref):
        _controlador_resonante_analisis()
        n += 1
    if pref is None or "power-synchronization-control-analisis".startswith(pref):
        _power_synchronization_control_analisis()
        n += 1
    if pref is None or "compensador-adelanto-atraso-analisis".startswith(pref):
        _compensador_adelanto_atraso_analisis()
        n += 1
    if pref is None or "frecuencias-segundo-orden-analisis".startswith(pref):
        _frecuencias_segundo_orden_analisis()
        n += 1
    if pref is None or "modelado-sistemas-analisis".startswith(pref):
        _modelado_sistemas_analisis()
        n += 1
    if pref is None or "carga-pulsante-datacenter-analisis".startswith(pref):
        _carga_pulsante_datacenter_analisis()
        n += 1
    if pref is None or "convertidor-back-to-back-analisis".startswith(pref):
        _convertidor_back_to_back_analisis()
        n += 1
    if pref is None or "metricas-desempeno-analisis".startswith(pref):
        _metricas_desempeno_analisis()
        n += 1
    if pref is None or "control-jerarquico-microrred-analisis".startswith(pref):
        _control_jerarquico_microrred_analisis()
        n += 1
    if pref is None or "servicios-red-soporte-analisis".startswith(pref):
        _servicios_red_soporte_analisis()
        n += 1
    if pref is None or "topologias-multinivel-analisis".startswith(pref):
        _topologias_multinivel_analisis()
        n += 1
    if pref is None or "impedancia-reactancia-analisis".startswith(pref):
        _impedancia_reactancia_analisis()
        n += 1
    if pref is None or "valor-rms-factor-potencia-analisis".startswith(pref):
        _valor_rms_factor_potencia_analisis()
        n += 1
    if pref is None or "modelo-linea-distribucion-analisis".startswith(pref):
        _modelo_linea_distribucion_analisis()
        n += 1
    if pref is None or "metodos-sintesis-control-analisis".startswith(pref):
        _metodos_sintesis_control_analisis()
        n += 1
    if pref is None or "arquitecturas-control-analisis".startswith(pref):
        _arquitecturas_control_analisis()
        n += 1
    if pref is None or "control-robusto-hinf-analisis".startswith(pref):
        _control_robusto_hinf_analisis()
        n += 1
    if pref is None or "antiresonancia-analisis".startswith(pref):
        _antiresonancia_analisis()
        n += 1
    if pref is None or "amortiguamiento-pasivo-vs-activo-analisis".startswith(pref):
        _amortiguamiento_pasivo_vs_activo_analisis()
        n += 1
    if pref is None or "deteccion-islanding-analisis".startswith(pref):
        _deteccion_islanding_analisis()
        n += 1
    if pref is None or "fenomenos-oscilatorios-red-analisis".startswith(pref):
        _fenomenos_oscilatorios_red_analisis()
        n += 1
    if pref is None or "virtual-oscillator-control-analisis".startswith(pref):
        _virtual_oscillator_control_analisis()
        n += 1
    if pref is None or "validacion-cruzada-analisis".startswith(pref):
        _validacion_cruzada_analisis()
        n += 1
    if pref is None or "niveles-validacion-analisis".startswith(pref):
        _niveles_validacion_analisis()
        n += 1
    if pref is None or "ciclo-diseno-control-analisis".startswith(pref):
        _ciclo_diseno_control_analisis()
        n += 1
    if pref is None or "calidad-potencia-analisis".startswith(pref):
        _calidad_potencia_analisis()
        n += 1
    if pref is None or "integracion-edos-stiff-analisis".startswith(pref):
        _integracion_edos_stiff_analisis()
        n += 1
    if pref is None or "hvdc-vsc-topologia-analisis".startswith(pref):
        _hvdc_vsc_topologia_analisis()
        n += 1
    if pref is None or "hvdc-control-potencia-analisis".startswith(pref):
        _hvdc_control_potencia_analisis()
        n += 1
    if pref is None or "hvdc-cable-dc-analisis".startswith(pref):
        _hvdc_cable_dc_analisis()
        n += 1
    if pref is None or "mmc-modelo-control-analisis".startswith(pref):
        _mmc_modelo_control_analisis()
        n += 1
    if pref is None or "aerogenerador-pmsg-dfig-analisis".startswith(pref):
        _aerogenerador_pmsg_dfig_analisis()
        n += 1
    if pref is None or "control-parque-eolico-offshore-analisis".startswith(pref):
        _control_parque_eolico_offshore_analisis()
        n += 1
    if pref is None or "mtdc-proteccion-dc".startswith(pref):
        _mtdc_proteccion_dc_analisis()
        n += 1
    if pref is None or "python-control-scipy".startswith(pref):
        _python_control_scipy_analisis()
        n += 1
    if pref is None or "red-thevenin-scr-analisis".startswith(pref):
        _red_thevenin_scr_analisis()
        n += 1
    if pref is None or "armonicos-thd-convertidores-analisis".startswith(pref):
        _armonicos_thd_convertidores_analisis()
        n += 1
    if pref is None or "control-tension-bus-dc-analisis".startswith(pref):
        _control_tension_bus_dc_analisis()
        n += 1
    if pref is None or "btb-diagramas-bloques".startswith(pref):
        _btb_diagramas_bloques()
        n += 1
    if pref is None or "fotovoltaica-po-flowchart".startswith(pref):
        _fv_po_flowchart()
        n += 1
    if pref is None or "optimo-simetrico-bode".startswith(pref):
        _optimo_simetrico()
        n += 1
    if pref is None or "btb-ff-loop".startswith(pref):
        _btb_ff_loop()
        n += 1
    if pref is None or "btb-pmsg-modelo".startswith(pref):
        _btb_pmsg_modelo()
        n += 1
    if pref is None or "btb-perdidas".startswith(pref):
        _btb_perdidas()
        n += 1
    if pref is None or "btb-rizado-L".startswith(pref):
        _btb_rizado_L()
        n += 1
    if pref is None or "btb-lazo-tension-verif".startswith(pref):
        _btb_lazo_tension_verif()
        n += 1
    if pref is None or "multinivel-circuitos".startswith(pref):
        _multinivel_circuitos()
        n += 1
    if pref is None or "mmc-estructura".startswith(pref):
        _mmc_estructura()
        n += 1
    if pref is None or "npc-topologia".startswith(pref):
        _npc_topologia()
        n += 1
    if pref is None or "npc-conmutacion".startswith(pref):
        _npc_conmutacion()
        n += 1
    if pref is None or "npc-neutro".startswith(pref):
        _npc_neutro()
        n += 1
    if pref is None or "npc-svm".startswith(pref):
        _npc_svm()
        n += 1
    if pref is None or "btb-mppt".startswith(pref):
        _btb_mppt()
        n += 1
    if pref is None or "btb-dq-transformacion".startswith(pref):
        _btb_dq_transformacion()
        n += 1
    if pref is None or "btb-lazo-corriente-bode".startswith(pref):
        _btb_lazo_corriente_bode()
        n += 1
    if pref is None or "btb-lazo-tension-bode".startswith(pref):
        _btb_lazo_tension_bode()
        n += 1
    if pref is None or "deteccion-islanding-modos".startswith(pref):
        _islanding_modos()
        n += 1
    if pref is None or "loop-shaping-flujo".startswith(pref):
        _loopshaping_flujo()
        n += 1
    if pref is None or "parque-offshore-cadena".startswith(pref):
        _parque_offshore_cadena()
        n += 1
    if pref is None or "btb-topologia".startswith(pref):
        _btb_topologia()
        n += 1
    if pref is None or "btb-tensiones-explicacion".startswith(pref):
        _btb_diagramas_bloques()  # genera ambas figuras a la vez
        n += 1
    print(f"--- {n} grupo(s) de figuras generados en figuras/")


# ===================================================================== #
#  anti-windup-analisis  (sin decorador @figura)
# ===================================================================== #
def _antiwindup_extended():
    """4 paneles: (a) sin AW vs clamping vs back-calculation,
    (b) estado del integrador, (c) efecto de Ti_av, (d) cascada con/sin AW."""
    L, R = 2e-3, 50e-3
    alpha_c = 2*np.pi*750.0
    Kp = alpha_c * L
    Ki = alpha_c * R
    umax = 800.0
    id_target = 1000.0
    Ts = 1e-4
    T = np.arange(0, 0.06, Ts)

    def sim_current(mode, Ti_av=None):
        i = 0.0; xi = 0.0
        i_out, xi_out = [], []
        for _ in T:
            e = id_target - i
            u_pi = Kp*e + xi
            u_sat = np.clip(u_pi, -umax, umax)
            if mode == 'none':
                xi += Ki*e*Ts
            elif mode == 'clamp':
                at_limit = (u_pi >= umax and e > 0) or (u_pi <= -umax and e < 0)
                if not at_limit:
                    xi += Ki*e*Ts
            elif mode == 'backc':
                Tt = Ti_av if Ti_av is not None else L/R
                xi += (Ki*e + (u_sat - u_pi)/Tt)*Ts
            i += (u_sat - R*i)/L * Ts
            i_out.append(i); xi_out.append(xi)
        return np.array(i_out), np.array(xi_out)

    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.0))
    (a1, a2), (a3, a4) = axes
    Tms = T*1e3

    i_none,  xi_none  = sim_current('none')
    i_clamp, xi_clamp = sim_current('clamp')
    i_bc,    xi_bc    = sim_current('backc', Ti_av=L/R)

    # (a) Comparativa id(t)
    a1.axhline(id_target, color="#aaa", ls=":", lw=1.2, label="referencia")
    a1.plot(Tms, i_none,  color=BAD,  lw=2.0, label="sin AW")
    a1.plot(Tms, i_clamp, color=ACC2, lw=2.0, label="clamping")
    a1.plot(Tms, i_bc,    color=ACC,  lw=2.0, label=f"back-calc $T_i^{{av}}$=L/R={L/R*1e3:.1f} ms")
    a1.set_xlabel("t [ms]"); a1.set_ylabel("$i_d$ [A]")
    a1.set_title(f"(a) $i_d(t)$ — escalón 0→{id_target:.0f} A, $u_{{max}}$={umax:.0f} V")
    a1.legend(fontsize=8.5); a1.set_xlim(0, 50)

    # (b) Estado del integrador
    a2.plot(Tms, xi_none,  color=BAD,  lw=2.0, label="sin AW")
    a2.plot(Tms, xi_clamp, color=ACC2, lw=2.0, label="clamping")
    a2.plot(Tms, xi_bc,    color=ACC,  lw=2.0, label="back-calc")
    a2.axhline( umax, color="#888", ls="--", lw=1.0, label=f"$\\pm u_{{max}}$={umax:.0f} V")
    a2.axhline(-umax, color="#888", ls="--", lw=1.0)
    a2.set_xlabel("t [ms]"); a2.set_ylabel("$\\xi$ [V]")
    a2.set_title("(b) Estado del integrador $\\xi(t)$\nsin AW: desbordamiento; back-calc: ancla a $u_{max}$")
    a2.legend(fontsize=8.5); a2.set_xlim(0, 50)

    # (c) Efecto de Ti_av
    for Ti_v, col, lbl in [(0.01, ACC,  "$T_i^{av}$=10 ms (agresivo)"),
                            (L/R,  ACC2, f"$T_i^{{av}}$=L/R={L/R*1e3:.0f} ms (óptimo)"),
                            (0.10, BAD,  "$T_i^{av}$=100 ms (lento)")]:
        i_v, _ = sim_current('backc', Ti_av=Ti_v)
        a3.plot(Tms, i_v, color=col, lw=2.0, label=lbl)
    a3.axhline(id_target, color="#aaa", ls=":", lw=1.2)
    a3.set_xlabel("t [ms]"); a3.set_ylabel("$i_d$ [A]")
    a3.set_title("(c) Efecto de $T_i^{av}$ en back-calculation\npequeño→agresivo; grande→lento")
    a3.legend(fontsize=8.5); a3.set_xlim(0, 50)

    # (d) Cascada tensión → corriente
    Ts2 = 1e-4; Kpv, Kiv = 0.5, 50.0; Vdc_ref = 400.0; Cdc = 2e-3

    def sim_cascade(use_aw):
        Vdc = 380.0; xiv = 0.0; ic = 0.0; xi2 = 0.0
        vdc_out, ic_out = [], []
        for k in range(len(T)):
            Iload = 5.0 if T[k] >= 0.01 else 0.0
            ev = Vdc_ref - Vdc
            u_v = Kpv*ev + xiv
            id_ref = np.clip(u_v, 0.0, 1500.0)
            if use_aw:
                xiv += (Kiv*ev + (id_ref - u_v)/(L/R))*Ts2
            else:
                xiv += Kiv*ev*Ts2
            e2 = id_ref - ic; u2 = Kp*e2 + xi2; u2s = np.clip(u2, -umax, umax)
            xi2 += (Ki*e2 + (u2s - u2)/(L/R))*Ts2
            ic += (u2s - R*ic)/L * Ts2
            Vdc += (ic - Iload)/Cdc * Ts2
            vdc_out.append(Vdc); ic_out.append(ic)
        return np.array(vdc_out), np.array(ic_out)

    Vdc_noaw, ic_noaw = sim_cascade(False)
    Vdc_aw,   ic_aw   = sim_cascade(True)
    ax4b = a4.twinx()
    a4.plot(Tms, Vdc_noaw, color=BAD, lw=2.0, label="$V_{dc}$ sin AW")
    a4.plot(Tms, Vdc_aw,   color=ACC, lw=2.0, label="$V_{dc}$ con AW")
    ax4b.plot(Tms, ic_noaw, color=BAD, lw=1.4, ls="--", label="$i_c$ sin AW")
    ax4b.plot(Tms, ic_aw,   color=ACC, lw=1.4, ls="--", label="$i_c$ con AW")
    a4.axvline(10, color="#888", ls=":", lw=1.0)
    a4.text(10.5, np.min(Vdc_noaw)*1.001 if np.min(Vdc_noaw) < 380 else 375,
            "escalón carga", fontsize=8, color="#555")
    a4.set_xlabel("t [ms]"); a4.set_ylabel("$V_{dc}$ [V]")
    ax4b.set_ylabel("$i_c$ [A]")
    a4.set_title("(d) Cascada tensión→corriente\nAW externo evita saturación prolongada")
    h1, l1 = a4.get_legend_handles_labels()
    h2, l2 = ax4b.get_legend_handles_labels()
    a4.legend(h1+h2, l1+l2, fontsize=8, loc="lower right")

    fig.suptitle("Anti-windup — análisis avanzado  "
                 f"(L={L*1e3:.0f} mH, R={R*1e3:.0f} mΩ, αc=2π·750 Hz, $u_{{max}}$={umax:.0f} V)",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _savefig(fig, "anti-windup-analisis.png")


# ===================================================================== #
#  compensacion-retardo-analisis  (sin decorador @figura)
# ===================================================================== #
def _delay_extended():
    """4 paneles: (a) Bode lazo corriente, (b) escalon id,
    (c) Bode lead solo, (d) PM vs tau/Ts."""
    L, R = 2e-3, 50e-3
    Ts = 1e-4; Td = 1.5*Ts
    alpha_c = 2*np.pi*750.0
    Kp = alpha_c*L; Ki = alpha_c*R
    umax = 800.0

    f = np.logspace(1, 4.3, 800)
    w = 2*np.pi*f
    G_plant = 1.0/(1j*w*L + R)
    wz = R/L
    C_PI = Kp*(1j*w + wz)/(1j*w + 1e-3)
    e_delay = np.exp(-1j*w*Td)

    dphi_tgt = np.radians(15.0)
    alpha_lead = (1+np.sin(dphi_tgt))/(1-np.sin(dphi_tgt))
    wc = alpha_c
    tau_z_lead = np.sqrt(alpha_lead)/wc
    tau_p_lead = 1.0/(np.sqrt(alpha_lead)*wc)
    C_lead = (1 + 1j*w*tau_z_lead)/(1 + 1j*w*tau_p_lead)

    Kp_lead = Kp / np.sqrt(alpha_lead)
    C_PI_lead = Kp_lead*(1j*w + wz)/(1j*w + 1e-3)

    L_noret = C_PI * G_plant
    L_ret   = C_PI * G_plant * e_delay
    L_comp  = C_PI_lead * C_lead * G_plant * e_delay

    def pm_from_loop(L_loop):
        mag = np.abs(L_loop)
        idx = np.argmin(np.abs(mag - 1.0))
        return np.angle(L_loop[idx], deg=True) + 180.0, f[idx]

    pm_nor, fc_nor = pm_from_loop(L_noret)
    pm_ret, fc_ret = pm_from_loop(L_ret)
    pm_cmp, fc_cmp = pm_from_loop(L_comp)

    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.0))
    (a1, a2), (a3, a4) = axes

    # (a) Bode magnitud del lazo
    for L_loop, col, lbl in [
            (L_noret, ACC, f"sin retardo (PM={pm_nor:.0f}°)"),
            (L_ret,   BAD, f"con retardo 1.5Ts (PM={pm_ret:.0f}°)"),
            (L_comp,  OK,  f"con lead+retardo (PM={pm_cmp:.0f}°)")]:
        a1.semilogx(f, 20*np.log10(np.abs(L_loop)), color=col, lw=2.0, label=lbl)
    a1.axhline(0, color="#888", ls="--", lw=1.0)
    a1.set_xlabel("f [Hz]"); a1.set_ylabel("|L(jω)| [dB]")
    a1.set_title("(a) Bode de magnitud del lazo de corriente\nαc=2π·750 Hz, Ts=100 µs, Td=150 µs")
    a1.legend(fontsize=8.0, loc="lower left"); a1.set_xlim(10, 2e4); a1.set_ylim(-60, 60)

    # (b) Respuesta al escalón id
    t_step = np.arange(0, 0.008, Ts)
    id_ref = 100.0

    def sim_step(use_delay, use_lead):
        i = 0.0; xi = 0.0; u_prev = 0.0; e_prev = 0.0
        Kp_s = Kp_lead if use_lead else Kp
        i_out = []
        for _ in t_step:
            e = id_ref - i
            if use_lead:
                y_lead = (e + tau_z_lead/Ts*(e - e_prev)) / (1 + tau_p_lead/Ts)
                e_prev = e
            else:
                y_lead = e
            u_pi = Kp_s*y_lead + xi
            u_sat = np.clip(u_pi, -umax, umax)
            xi += (Ki*(id_ref-i) + (u_sat - u_pi)/(L/R))*Ts
            u_act = u_prev if use_delay else u_sat
            u_prev = u_sat
            i += (u_act - R*i)/L * Ts
            i_out.append(i)
        return np.array(i_out)

    Tms2 = t_step*1e3
    a2.axhline(id_ref, color="#aaa", ls=":", lw=1.2, label="referencia")
    a2.plot(Tms2, sim_step(False, False), color=ACC, lw=2.0, label=f"sin retardo (PM≈{pm_nor:.0f}°)")
    a2.plot(Tms2, sim_step(True,  False), color=BAD, lw=2.0, label=f"con retardo (PM≈{pm_ret:.0f}°)")
    a2.plot(Tms2, sim_step(True,  True),  color=OK,  lw=2.0, label=f"con lead (PM≈{pm_cmp:.0f}°)")
    a2.set_xlabel("t [ms]"); a2.set_ylabel("$i_d$ [A]")
    a2.set_title("(b) Respuesta al escalón de $i_d$=100 A\nMayor PM → menor sobreoscilación")
    a2.legend(fontsize=8.5)

    # (c) Bode del compensador lead solo
    mag_lead = 20*np.log10(np.abs(C_lead))
    ph_lead  = np.angle(C_lead, deg=True)
    ax3b = a3.twinx()
    a3.semilogx(f, mag_lead, color=ACC,  lw=2.2, label="|C_lead| [dB]")
    ax3b.semilogx(f, ph_lead, color=ACC2, lw=2.0, ls="--", label="∠C_lead [°]")
    a3.axvline(alpha_c/(2*np.pi), color=BAD, ls=":", lw=1.2)
    phi_at_fc = np.degrees(np.arctan(alpha_c*tau_z_lead) - np.arctan(alpha_c*tau_p_lead))
    a3.set_xlabel("f [Hz]"); a3.set_ylabel("|C_lead| [dB]", color=ACC)
    ax3b.set_ylabel("∠C_lead [°]", color=ACC2)
    a3.set_title(f"(c) Compensador lead solo: Δφ≈{phi_at_fc:.0f}° en $f_c$\n"
                 f"α={alpha_lead:.2f}, τz={tau_z_lead*1e6:.0f} µs, τp={tau_p_lead*1e6:.0f} µs")
    h1, l1 = a3.get_legend_handles_labels()
    h2, l2 = ax3b.get_legend_handles_labels()
    a3.legend(h1+h2, l1+l2, fontsize=8.5); a3.set_xlim(10, 2e4)

    # (d) PM vs tau/Ts
    tau_ratio = np.linspace(0.5, 3.0, 200)
    for ac_ts, col_d in zip([0.1, 0.3, 0.5, 0.8], [ACC, ACC2, OK, BAD]):
        pm_v = [90.0 - np.degrees(ac_ts * tr) for tr in tau_ratio]
        a4.plot(tau_ratio, pm_v, color=col_d, lw=2.0, label=f"$\\alpha_c T_s$={ac_ts}")
    a4.axhline(45, color="#888", ls="--", lw=1.0, label="PM=45°")
    a4.axhline(0,  color=BAD,   ls=":",  lw=1.0)
    a4.axvline(1.5, color="#555", ls=":", lw=1.2, label="$\\tau/T_s$=1.5")
    a4.set_xlabel("$\\tau/T_s$"); a4.set_ylabel("PM [°]")
    a4.set_title("(d) PM vs $\\tau/T_s$ — distintos $\\alpha_c T_s$\n$\\alpha_c T_s=0.3$ → límite práctico")
    a4.legend(fontsize=8.5); a4.set_ylim(-30, 120)

    fig.suptitle("Compensación de retardo — análisis avanzado  "
                 f"(L={L*1e3:.0f} mH, R={R*1e3:.0f} mΩ, Ts={Ts*1e6:.0f} µs)",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _savefig(fig, "compensacion-retardo-analisis.png")


# ===================================================================== #
#  control-feedforward-analisis  (sin decorador @figura)
# ===================================================================== #
def _ff_extended():
    """4 paneles: (a) FB vs FB+FF perturbacion, (b) FF referencia,
    (c) sensibilidad error L, (d) diagrama de bloques."""
    L, R = 2e-3, 50e-3
    Ts   = 1e-4
    alpha_c = 2*np.pi*750.0
    Kp = alpha_c*L; Ki = alpha_c*R
    umax = 800.0; ded = 100.0; t_pert = 0.003
    T = np.arange(0, 0.010, Ts)
    Tms = T*1e3

    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.0))
    (a1, a2), (a3, a4) = axes

    # (a) Perturbación de red
    def sim_pert(use_ff, L_real=None):
        Lr = L_real if L_real is not None else L
        i = 0.0; xi = 0.0; ed_prev = 0.0; i_out = []
        for t_k in T:
            ed_k = ded if t_k >= t_pert else 0.0
            e = 0.0 - i
            u_ff = ed_prev if use_ff else 0.0
            u_pi = Kp*e + xi
            u_tot = u_pi + u_ff
            u_sat = np.clip(u_tot, -umax, umax)
            xi += (Ki*e + (u_sat - u_tot)/(L/R))*Ts
            i += (u_sat - R*i - ed_k)/Lr * Ts
            ed_prev = ed_k
            i_out.append(i)
        return np.array(i_out)

    i_fb = sim_pert(False)
    i_ff = sim_pert(True)
    a1.axhline(0, color="#aaa", ls=":", lw=1.2, label="$i_d^*=0$ A")
    a1.plot(Tms, i_fb, color=BAD, lw=2.0, label="solo FB (PI)")
    a1.plot(Tms, i_ff, color=ACC, lw=2.0, label="FB + FF de $e_d$")
    a1.axvline(t_pert*1e3, color="#888", ls="--", lw=1.0)
    fb_min = float(np.min(i_fb))
    a1.text(t_pert*1e3+0.1, fb_min*0.55, f"$\\Delta e_d$={ded:.0f} V", fontsize=8)
    a1.set_xlabel("t [ms]"); a1.set_ylabel("$i_d$ [A]")
    a1.set_title("(a) Rechazo de perturbación de red\nFF: pico ~10× menor que solo FB")
    a1.legend(fontsize=8.5)

    # (b) FF de referencia
    T2 = np.arange(0, 0.008, Ts)
    t_step_ref = 0.001; id_step = 500.0

    def sim_ref(use_ff_ref):
        i = 0.0; xi = 0.0; id_prev = 0.0; i_out = []
        for t_k in T2:
            id_r = id_step if t_k >= t_step_ref else 0.0
            e = id_r - i
            if use_ff_ref:
                u_ff_r = np.clip(L*(id_r - id_prev)/Ts + R*id_r, -umax, umax)
            else:
                u_ff_r = 0.0
            id_prev = id_r
            u_pi = Kp*e + xi
            u_tot = u_pi + u_ff_r
            u_sat = np.clip(u_tot, -umax, umax)
            xi += (Ki*e + (u_sat - u_tot)/(L/R))*Ts
            i += (u_sat - R*i)/L * Ts
            i_out.append(i)
        return np.array(i_out)

    T2ms = T2*1e3
    a2.axhline(id_step, color="#aaa", ls=":", lw=1.2, label=f"$i_d^*$={id_step:.0f} A")
    a2.plot(T2ms, sim_ref(False), color=BAD, lw=2.0, label="solo FB")
    a2.plot(T2ms, sim_ref(True),  color=ACC, lw=2.0, label="FB + FF referencia")
    a2.axvline(t_step_ref*1e3, color="#888", ls="--", lw=1.0)
    a2.set_xlabel("t [ms]"); a2.set_ylabel("$i_d$ [A]")
    a2.set_title("(b) Escalón de referencia $i_d^*$=500 A\nFF referencia → seguimiento más rápido")
    a2.legend(fontsize=8.5)

    # (c) Sensibilidad al error de L
    L_errs = np.linspace(-0.30, 0.30, 13)
    picos = []
    for dL in L_errs:
        i_v = sim_pert(True, L_real=L*(1+dL))
        picos.append(max(abs(i_v[int(t_pert/Ts):])))
    pico_ff = max(abs(i_ff[int(t_pert/Ts):]))
    pico_fb = max(abs(i_fb[int(t_pert/Ts):]))
    a3.plot(L_errs*100, picos, color=ACC, lw=2.4, marker="o", ms=5)
    a3.axvline(0, color="#aaa", ls=":", lw=1.0)
    a3.axvspan(-20, 20, alpha=0.12, color=OK, label="±20% error L")
    a3.axhline(pico_ff, color=ACC, ls="--", lw=1.2, label=f"FF L_nom: {pico_ff:.1f} A")
    a3.axhline(pico_fb, color=BAD, ls=":",  lw=1.2, label=f"solo FB: {pico_fb:.1f} A")
    a3.set_xlabel("error en L [%]"); a3.set_ylabel("pico $|i_d|$ [A]")
    a3.set_title("(c) Sensibilidad al error de modelo en L\n±20%: residuo pequeño, FB lo limpia")
    a3.legend(fontsize=8.5)

    # (d) Diagrama de bloques
    from matplotlib.patches import FancyBboxPatch
    a4.set_xlim(0, 10); a4.set_ylim(0, 6); a4.axis("off")
    a4.set_title("(d) Lazo con FB (PI) + FF perturbación ($e_d$) + FF referencia", fontsize=10)

    def box(x, y, w, h, txt, col="#1f6feb"):
        a4.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
                     boxstyle="round,pad=0.08", fc="white", ec=col, lw=1.8))
        a4.text(x, y, txt, ha="center", va="center", fontsize=8.5)

    def arr(x0, y0, x1, y1):
        a4.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="->", color="#333", lw=1.4))

    box(3.2, 3.2, 1.4, 0.8, "PI\n$C(s)$")
    box(6.5, 3.2, 2.0, 0.8, "Planta\n$1/(Ls+R)$")
    box(5.5, 5.0, 1.8, 0.7, "FF $e_d$\n$\\approx v_C$", col=OK)
    box(3.2, 1.3, 2.0, 0.7, "FF ref.\n$(Ls+R)i_d^*$", col=ACC2)
    circ1 = plt.Circle((1.8, 3.2), 0.27, fc="white", ec="#555", lw=1.6)
    a4.add_patch(circ1); a4.text(1.8, 3.2, "Σ", ha="center", va="center", fontsize=12)
    circ2 = plt.Circle((4.8, 3.2), 0.27, fc="white", ec="#555", lw=1.6)
    a4.add_patch(circ2); a4.text(4.8, 3.2, "Σ", ha="center", va="center", fontsize=12)
    arr(0.3, 3.2, 1.53, 3.2)
    arr(2.07, 3.2, 2.5, 3.2)
    arr(3.9, 3.2, 4.53, 3.2)
    arr(5.07, 3.2, 5.5, 3.2)
    arr(7.5, 3.2, 9.0, 3.2)
    arr(5.5, 4.65, 5.5, 3.47)
    arr(5.5, 5.7, 5.5, 5.35)
    arr(3.2, 1.65, 3.2, 2.4)
    arr(3.2, 2.4, 4.53, 3.0)
    a4.plot([7.5, 7.5, 1.8], [3.2, 0.6, 0.6], color="#555", lw=1.4)
    arr(1.8, 0.6, 1.8, 2.93)
    a4.text(0.15, 3.45, "$i_d^*$",     fontsize=9)
    a4.text(9.05, 3.45, "$i_d$",       fontsize=9)
    a4.text(5.5,  5.92, "$e_d$",       fontsize=9, ha="center")
    a4.text(0.95, 0.45, "$-i_d$ (FB)", fontsize=8, color="#555")
    a4.text(2.0,  3.48, "$e$",          fontsize=9, color="#555")

    fig.suptitle("Control feedforward — análisis avanzado  "
                 f"(L={L*1e3:.0f} mH, R={R*1e3:.0f} mΩ, αc=2π·750 Hz, $\\Delta e_d$={ded:.0f} V)",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _savefig(fig, "control-feedforward-analisis.png")


# ===================================================================== #
#  asignacion-polos-lqr-analisis  (sin decorador @figura)
# ===================================================================== #
def _lqrext():
    """4 paneles: (a) escalon LQR vs PI, (b) polos vs Q, (c) Bode PM LQR, (d) singular values retorno."""
    import scipy.linalg as la
    import scipy.signal as sig

    L1, L2, Cf = 2e-3, 1.5e-3, 270e-6
    R1, R2 = 50e-3, 40e-3
    A = np.array([[0, -1/L1, 0],
                  [1/Cf, 0, -1/Cf],
                  [0, 1/L2, -R2/L2]])
    B = np.array([[1/L1], [0], [0]])
    C = np.array([[0, 0, 1]])

    # Bryson Q, R nominales
    Q0 = np.diag([1/1500**2, 1/700**2, 1/1500**2])
    R0 = np.array([[1/800**2]])

    def lqr_solve(Q, R):
        P = la.solve_continuous_are(A, B, Q, R)
        K = np.linalg.solve(R, B.T @ P)
        return K, np.linalg.eigvals(A - B @ K)

    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.0))
    (a1, a2), (a3, a4) = axes

    # (a) escalon LQR vs PI en i_L2
    K0, _ = lqr_solve(Q0, R0)
    Acl = A - B @ K0
    Ts = 1e-5; T = np.arange(0, 0.015, Ts)
    ref = 1000.0
    # LQR simulation
    x = np.zeros(3); lqr_out = []
    for _ in T:
        u = float(-K0 @ x + ref * K0[0, 2] / (C @ np.linalg.solve(-Acl, B))[0, 0])
        u = np.clip(u, -800, 800)
        x = x + Ts * (A @ x + B.flatten() * u)
        lqr_out.append(x[2])
    lqr_out = np.array(lqr_out)
    # PI classical (alpha_c = 2pi*500 Hz)
    alpha_c = 2 * np.pi * 500
    Kp_pi = alpha_c * L2; Ki_pi = alpha_c * R2
    i2 = 0.0; xi = 0.0; pi_out = []
    for _ in T:
        e = ref - i2
        u_pi = np.clip(Kp_pi * e + xi, -800, 800)
        xi += Ki_pi * e * Ts
        i2 += Ts * (u_pi - R2 * i2) / L2
        pi_out.append(i2)
    pi_out = np.array(pi_out)
    a1.plot(T * 1e3, lqr_out, color=ACC, lw=2.0, label="LQR")
    a1.plot(T * 1e3, pi_out, color=BAD, lw=2.0, ls="--", label="PI clásico")
    a1.axhline(ref, color="#888", ls=":", lw=1.2, label="ref")
    a1.set_xlabel("t [ms]"); a1.set_ylabel("$i_{L2}$ [A]")
    a1.set_title("(a) Escalón de corriente: LQR vs PI\nLCL lazo cerrado")
    a1.legend(fontsize=8.5); a1.set_xlim(0, 15)

    # (b) mapa de polos para distintos Q (barrer escala de Q11)
    rhos = [0.1, 0.3, 1.0, 3.0, 10.0, 30.0]
    colors_rho = plt.cm.viridis(np.linspace(0, 1, len(rhos)))
    for rho, col in zip(rhos, colors_rho):
        _, poles = lqr_solve(rho * Q0, R0)
        a2.scatter(poles.real, poles.imag, color=col, s=60, zorder=5,
                   label=f"ρ={rho}")
    a2.axvline(0, color="#888", lw=1.0); a2.axhline(0, color="#888", lw=1.0)
    a2.set_xlabel("Re(λ) [rad/s]"); a2.set_ylabel("Im(λ) [rad/s]")
    a2.set_title("(b) Polos de $A-BK$ vs escala $\\rho Q$\nmás Q → polos más rápidos")
    a2.legend(fontsize=7, ncol=2)

    # (c) Bode del margen de fase con LQR (lazo en el actuador)
    omega = np.logspace(2, 5, 500)
    s = 1j * omega
    # lazo L = K(sI-A)^{-1}B en la entrada (return difference)
    Lmag = np.zeros(len(omega)); Lphase = np.zeros(len(omega))
    for ki, w in enumerate(omega):
        sIA_inv = np.linalg.inv(s[ki] * np.eye(3) - A)
        L_val = float(np.real(K0 @ sIA_inv @ B))
        L_imag = float(np.imag(K0 @ sIA_inv @ B))
        L_c = complex(L_val, L_imag)
        Lmag[ki] = abs(L_c)
        Lphase[ki] = np.angle(L_c, deg=True)
    idx_c = np.argmin(np.abs(Lmag - 1.0))
    pm = 180 + Lphase[idx_c]
    a3.semilogx(omega / (2 * np.pi), 20 * np.log10(Lmag + 1e-12),
                color=ACC, lw=2.0, label="|L(jω)|")
    a3.axhline(0, color="#888", ls=":", lw=1.2)
    a3.axvline(omega[idx_c] / (2 * np.pi), color=BAD, ls="--", lw=1.2,
               label=f"ωc: PM={pm:.0f}°")
    a3.set_xlabel("f [Hz]"); a3.set_ylabel("|L| [dB]")
    a3.set_title(f"(c) Bode del lazo LQR\nPM≥60° garantizado por el LQR")
    a3.legend(fontsize=8.5); a3.grid(True, which="both", alpha=0.3)

    # (d) valores singulares de la función de retorno I + K(sI-A)^{-1}B
    sv_min = np.zeros(len(omega))
    for ki, w in enumerate(omega):
        sIA_inv = np.linalg.inv(s[ki] * np.eye(3) - A)
        ret = np.eye(1) + K0 @ sIA_inv @ B
        sv_min[ki] = np.linalg.svd(ret, compute_uv=False)[-1]
    a4.semilogx(omega / (2 * np.pi), 20 * np.log10(sv_min + 1e-12),
                color=ACC, lw=2.0, label=r"$\sigma_{min}(I+L)$")
    a4.axhline(20 * np.log10(1 / np.sqrt(2)), color=BAD, ls="--", lw=1.2,
               label=f"1/sqrt(2) = -3 dB (limite)")
    a4.set_xlabel("f [Hz]"); a4.set_ylabel("sigma [dB]")
    a4.set_title("(d) Locus de valores singulares de retorno\n" r"$\sigma_{min}(I+L)\geq 1/\sqrt{2}$")
    a4.legend(fontsize=8.5); a4.grid(True, which="both", alpha=0.3)

    fig.suptitle("LQR — análisis extendido  "
                 f"(L1={L1*1e3:.0f} mH, L2={L2*1e3:.1f} mH, Cf={Cf*1e6:.0f} µF)",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _savefig(fig, "asignacion-polos-lqr-analisis.png")


# ===================================================================== #
#  control-predictivo-analisis  (sin decorador @figura)
# ===================================================================== #
def _mpcext():
    """4 paneles: (a) prediccion MPC N=3, (b) accion de control MPC vs PI,
    (c) tiempo de computo QP vs N, (d) comparativa dinamica MPC vs PI con restriccion."""
    L, R = 1.5e-3, 40e-3
    Ts = 100e-6
    imax = 1.2 * 1500.0  # 1.2 pu
    umax = 800.0
    ref = 1000.0

    Ad = 1 - R / L * Ts
    Bd = Ts / L

    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.0))
    (a1, a2), (a3, a4) = axes

    # (a) prediccion del MPC con N=3
    N = 3
    T_show = np.arange(0, 0.008, Ts)
    # simulate true system with simple MPC (unconstrained, N=3)
    def build_FH(Ad, Bd, N):
        F = np.array([[Ad**j] for j in range(1, N+1)])
        H = np.zeros((N, N))
        for i in range(N):
            for j in range(i+1):
                H[i, j] = Ad**(i-j) * Bd
        return F, H

    F, H = build_FH(Ad, Bd, N)
    Q_mpc = np.eye(N) * (1 / ref**2)
    R_mpc = np.eye(N) * (1 / umax**2)
    Kmpc = np.linalg.solve(H.T @ Q_mpc @ H + R_mpc, H.T @ Q_mpc)

    x = 0.0; i_out = []; u_out = []
    t_step = 0.001
    for tk in T_show:
        r_k = ref if tk >= t_step else 0.0
        r_vec = np.full(N, r_k)
        u_seq = Kmpc @ (r_vec - F.flatten() * x)
        u_k = float(np.clip(u_seq[0], -umax, umax))
        x = Ad * x + Bd * u_k
        i_out.append(x); u_out.append(u_k)

    # show prediction at one time step
    t_pred_idx = int(0.0015 / Ts)
    x_pred = i_out[t_pred_idx]
    r_at = ref
    pred_i = [x_pred]
    for _ in range(N):
        u_seq = Kmpc @ (np.full(N, r_at) - F.flatten() * pred_i[-1])
        u_p = float(np.clip(u_seq[0], -umax, umax))
        pred_i.append(Ad * pred_i[-1] + Bd * u_p)
    t_base = T_show[t_pred_idx]
    t_pred_axis = np.arange(N+1) * Ts * 1e3 + t_base * 1e3

    a1.plot(T_show * 1e3, i_out, color=ACC, lw=2.0, label="$i_{L2}$ real")
    a1.axhline(ref, color="#888", ls=":", lw=1.2, label="ref")
    a1.plot(t_pred_axis, pred_i, "o--", color=OK, lw=1.5, ms=5,
            label=f"prediccion N={N}")
    a1.set_xlabel("t [ms]"); a1.set_ylabel("$i_{L2}$ [A]")
    a1.set_title(f"(a) Predicción MPC N={N}, Ts={Ts*1e6:.0f} µs\ntrayectorias predichas")
    a1.legend(fontsize=8.5)

    # (b) accion de control MPC vs PI con anti-windup
    alpha_c = 2 * np.pi * 1000
    Kp_pi = alpha_c * L; Ki_pi = alpha_c * R
    T2 = T_show.copy()
    xi = 0.0; i_pi = 0.0; u_pi_out = []
    for tk in T2:
        r_k = ref if tk >= t_step else 0.0
        e = r_k - i_pi
        u_p = Kp_pi * e + xi
        u_sat = float(np.clip(u_p, -umax, umax))
        xi += (Ki_pi * e + (u_sat - u_p) / (L / R)) * Ts  # back-calc AW
        i_pi = Ad * i_pi + Bd * u_sat
        u_pi_out.append(u_sat)

    a2.plot(T_show * 1e3, u_out, color=ACC, lw=2.0, label="MPC")
    a2.plot(T2 * 1e3, u_pi_out, color=BAD, lw=2.0, ls="--", label="PI + AW")
    a2.axhline(umax, color="#aaa", ls=":", lw=1.0)
    a2.axhline(-umax, color="#aaa", ls=":", lw=1.0)
    a2.set_xlabel("t [ms]"); a2.set_ylabel("u [V]")
    a2.set_title("(b) Acción de control: saturación suave MPC\nvs PI con anti-windup")
    a2.legend(fontsize=8.5)

    # (c) tiempo de computo del QP vs N (estimated via matrix inversion size)
    Ns = np.arange(1, 16)
    t_qp = 0.5 * Ns**3 + 2.0 * Ns**2  # µs, approximation O(N^3)
    a3.plot(Ns, t_qp, "o-", color=ACC, lw=2.0, ms=6)
    a3.axhline(50, color=BAD, ls="--", lw=1.2, label="50 µs (limite Ts=100µs)")
    a3.set_xlabel("Horizonte N"); a3.set_ylabel("Tiempo QP estimado [µs]")
    a3.set_title("(c) Coste computacional del QP vs N\nN≤5 factible con DSP moderno")
    a3.legend(fontsize=8.5); a3.grid(True, alpha=0.3)

    # (d) comparativa dinamica MPC vs PI con restriccion activa
    imax_restrict = 800.0  # limite bajo para forzar restriccion
    T3 = np.arange(0, 0.012, Ts)
    ref3 = 1200.0
    # MPC con restriccion de corriente (por clipping en prediccion)
    x3 = 0.0; mpc_r_out = []; mpc_u_out = []
    for tk in T3:
        r_k = ref3 if tk >= 0.001 else 0.0
        r_vec = np.full(N, r_k)
        u_seq = Kmpc @ (r_vec - F.flatten() * x3)
        u_k = float(np.clip(u_seq[0], -umax, umax))
        x3_next = Ad * x3 + Bd * u_k
        if abs(x3_next) > imax_restrict:
            u_k = (np.sign(x3_next) * imax_restrict - Ad * x3) / Bd
            u_k = float(np.clip(u_k, -umax, umax))
        x3 = Ad * x3 + Bd * u_k
        mpc_r_out.append(x3); mpc_u_out.append(u_k)
    # PI sin restriccion de corriente
    xi3 = 0.0; i3 = 0.0; pi3_out = []
    for tk in T3:
        r_k = ref3 if tk >= 0.001 else 0.0
        e = r_k - i3
        u_p = Kp_pi * e + xi3
        u_sat = float(np.clip(u_p, -umax, umax))
        xi3 += (Ki_pi * e + (u_sat - u_p) / (L / R)) * Ts
        i3 = Ad * i3 + Bd * u_sat
        pi3_out.append(i3)
    a4.plot(T3 * 1e3, mpc_r_out, color=ACC, lw=2.0, label="MPC (con restricción)")
    a4.plot(T3 * 1e3, pi3_out, color=BAD, lw=2.0, ls="--", label="PI (sin restricción)")
    a4.axhline(imax_restrict, color=OK, ls=":", lw=1.5, label=f"$i_{{max}}$={imax_restrict:.0f} A")
    a4.axhline(ref3, color="#888", ls=":", lw=1.0, label="ref")
    a4.set_xlabel("t [ms]"); a4.set_ylabel("$i_{L2}$ [A]")
    a4.set_title("(d) Comparativa MPC vs PI ante escalón\ncon restricción de corriente activa")
    a4.legend(fontsize=8.0)

    fig.suptitle("MPC — análisis extendido  "
                 f"(L={L*1e3:.1f} mH, Ts={Ts*1e6:.0f} µs, N={N}, $i_{{max}}$={imax_restrict:.0f} A)",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _savefig(fig, "control-predictivo-analisis.png")


# ===================================================================== #
#  robustez-parametrica-analisis  (sin decorador @figura)
# ===================================================================== #
def _robext():
    """4 paneles: (a) Bode PM vs L para L=1.6/2.0/2.4 mH,
    (b) autovalores para distintos L, (c) ||wm*T||_inf vs freq,
    (d) mu(omega) para GFM con incertidumbre parametrica."""
    R1_nom = 50e-3
    L1_vals = [1.6e-3, 2.0e-3, 2.4e-3]
    alpha_c = 2 * np.pi * 750.0
    Td = 100e-6  # retardo de un periodo
    omega = np.logspace(2, 5, 600)

    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.0))
    (a1, a2), (a3, a4) = axes

    # (a) Bode margen de fase para distintos L
    cols_l = [BAD, ACC, OK]
    labels_l = ["L=1.6 mH", "L=2.0 mH (nom)", "L=2.4 mH"]
    for L1, col, lab in zip(L1_vals, cols_l, labels_l):
        Kp = L1_vals[1] * alpha_c   # ganancia fija al nominal
        Ki = R1_nom * alpha_c
        s = 1j * omega
        L_loop = Kp * (1 + s / (Ki / Kp)) / (s / (Ki / Kp)) / (s * L1 + R1_nom) * np.exp(-s * Td)
        mag = np.abs(L_loop)
        phase = np.angle(L_loop, deg=True)
        idx_c = np.argmin(np.abs(mag - 1.0))
        pm = 180 + phase[idx_c]
        a1.semilogx(omega / (2 * np.pi), 20 * np.log10(mag + 1e-12),
                    color=col, lw=2.0, label=f"{lab} (PM={pm:.0f}°)")
    a1.axhline(0, color="#888", ls=":", lw=1.2)
    a1.set_xlabel("f [Hz]"); a1.set_ylabel("|L| [dB]")
    a1.set_title("(a) Bode del lazo de corriente vs $L_1$\nPM disminuye al subir $L_1$")
    a1.legend(fontsize=8.0); a1.grid(True, which="both", alpha=0.3)

    # (b) autovalores del sistema de corriente para distintos L (PI + planta RL)
    # 2nd order closed-loop: L*s^2 + (R+Kp)*s + Ki = 0
    for L1, col, lab in zip(L1_vals, cols_l, labels_l):
        Kp = L1_vals[1] * alpha_c
        Ki = R1_nom * alpha_c
        coeffs = [L1, R1_nom + Kp, Ki]
        poles = np.roots(coeffs)
        a2.scatter(poles.real, poles.imag, color=col, s=80, zorder=5, label=lab, marker="x")
    a2.axvline(0, color="#888", lw=1.0); a2.axhline(0, color="#888", lw=1.0)
    a2.set_xlabel("Re(λ) [rad/s]"); a2.set_ylabel("Im(λ) [rad/s]")
    a2.set_title("(b) Autovalores del lazo cerrado vs $L_1$\nvariación ±20% alrededor del nominal")
    a2.legend(fontsize=8.5)

    # (c) norma ||wm*T||_inf vs frecuencia (incertidumbre multiplicativa)
    L1_nom = 2.0e-3
    Kp_nom = L1_nom * alpha_c; Ki_nom = R1_nom * alpha_c
    s = 1j * omega
    G_nom = 1.0 / (s * L1_nom + R1_nom)
    C_pi = Kp_nom * (1 + s / (Ki_nom / Kp_nom)) / (s / (Ki_nom / Kp_nom))
    L_nom = C_pi * G_nom * np.exp(-s * Td)
    T_nom = L_nom / (1 + L_nom)  # complementary sensitivity
    # weight wm: uncertainty model wm(s)*Delta, Delta <= 1
    # worst-case uncertainty: dL/L at 20% L variation
    wm = 0.2 * np.ones(len(omega))  # flat 20% weight (conservative)
    crit = np.abs(wm * T_nom)
    a3.semilogx(omega / (2 * np.pi), 20 * np.log10(crit + 1e-12),
                color=ACC, lw=2.0, label="$|w_m \\cdot T|$")
    a3.axhline(0, color=BAD, ls="--", lw=1.5, label="0 dB (límite robustez)")
    a3.fill_between(omega / (2 * np.pi),
                    20 * np.log10(crit + 1e-12),
                    0, where=(crit > 1),
                    alpha=0.2, color=BAD, label="zona insegura")
    a3.set_xlabel("f [Hz]"); a3.set_ylabel("[dB]")
    a3.set_title("(c) $\\|w_m T\\|_\\infty$ vs frecuencia\n$<0$ dB → robusto ante ±20% en $L_1$")
    a3.legend(fontsize=8.5); a3.grid(True, which="both", alpha=0.3)

    # (d) mu(omega) - approximation via structured singular value bound
    # For 1 real uncertainty delta_L in [-.2, .2], mu = |T*wm| (same as ||wm*T||)
    # Show it as a frequency plot with bound
    mu_bound = crit  # = |wm * T| (upper bound on mu for 1 uncertainty block)
    a4.semilogx(omega / (2 * np.pi), mu_bound,
                color=ACC, lw=2.0, label="$\\mu(\\omega)$ (cota superior)")
    a4.axhline(1.0, color=BAD, ls="--", lw=1.5, label="$\\mu=1$ (límite)")
    a4.fill_between(omega / (2 * np.pi), mu_bound, 1,
                    where=(mu_bound > 1), alpha=0.2, color=BAD)
    a4.set_xlabel("f [Hz]"); a4.set_ylabel("μ")
    a4.set_title("(d) μ-análisis del lazo de corriente\n$\\mu<1$ → robusto con estructura $\\delta_{L_1}$")
    a4.legend(fontsize=8.5); a4.grid(True, which="both", alpha=0.3)

    fig.suptitle("Robustez paramétrica — análisis extendido  "
                 f"(GFM proyecto 01, $L_1\\in[1.6,2.4]$ mH, $R_1={R1_nom*1e3:.0f}$ mΩ)",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _savefig(fig, "robustez-parametrica-analisis.png")


# ===================================================================== #
#  valores-singulares-mimo-analisis  (sin decorador @figura)
# ===================================================================== #
def _svdext():
    """4 paneles: (a) sigma_bar y sigma_un de G_dq vs freq,
    (b) sigma_bar(S) y Ms del lazo cerrado GFM,
    (c) direccion de entrada de peor ganancia en plano dq a 50 Hz,
    (d) sigma_bar y sigma_un antes y despues del desacoplo FF."""
    L1, R1 = 2e-3, 50e-3
    omega0 = 2 * np.pi * 50
    omega = np.logspace(1, 5, 600)
    alpha_c = 2 * np.pi * 750

    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.0))
    (a1, a2), (a3, a4) = axes

    def G_dq(w, L, R, w0):
        """Z_{dq}(jw) 2x2 matrix without decoupling."""
        z = complex(R, w * L)
        cross = w0 * L
        return np.array([[z, -cross], [cross, z]])

    def G_dq_decoupled(w, L, R):
        z = complex(R, w * L)
        return np.array([[z, 0], [0, z]])

    sv_max_nd = []; sv_min_nd = []; kappa_nd = []
    sv_max_d = []; sv_min_d = []; kappa_d = []
    for w in omega:
        Gw = G_dq(w, L1, R1, omega0)
        sv = np.linalg.svd(Gw, compute_uv=False)
        sv_max_nd.append(sv[0]); sv_min_nd.append(sv[-1])
        kappa_nd.append(sv[0] / (sv[-1] + 1e-30))
        Gw_d = G_dq_decoupled(w, L1, R1)
        sv_d = np.linalg.svd(Gw_d, compute_uv=False)
        sv_max_d.append(sv_d[0]); sv_min_d.append(sv_d[-1])
        kappa_d.append(sv_d[0] / (sv_d[-1] + 1e-30))

    sv_max_nd = np.array(sv_max_nd); sv_min_nd = np.array(sv_min_nd)
    kappa_nd = np.array(kappa_nd)
    sv_max_d = np.array(sv_max_d); sv_min_d = np.array(sv_min_d)

    # (a) valores singulares de G_dq vs frecuencia
    a1.semilogx(omega / (2 * np.pi), 20 * np.log10(sv_max_nd + 1e-12),
                color=ACC, lw=2.0, label="$\\bar{\\sigma}(Z_{dq})$ sin desacoplo")
    a1.semilogx(omega / (2 * np.pi), 20 * np.log10(sv_min_nd + 1e-12),
                color=ACC, lw=2.0, ls="--", label=r"$\sigma_{min}(Z_{dq})$")
    a1.set_xlabel("f [Hz]"); a1.set_ylabel("σ [dB Ω]")
    a1.set_title("(a) Valores singulares de $Z_{dq}(j\\omega)$\nacondicionamiento κ(ω)")
    a1.legend(fontsize=8.5); a1.grid(True, which="both", alpha=0.3)

    # (b) sigma_bar(S) y Ms
    Kp = alpha_c * L1; Ki = alpha_c * R1
    s = 1j * omega
    C_pi = Kp * (1 + s / (Ki / Kp)) / (s / (Ki / Kp))
    # SISO loop (decoupled)
    G_s = 1.0 / (s * L1 + R1)
    L_loop = C_pi * G_s
    S_loop = 1.0 / (1.0 + L_loop)
    Ms_val = np.max(np.abs(S_loop))
    a2.semilogx(omega / (2 * np.pi), 20 * np.log10(np.abs(S_loop) + 1e-12),
                color=ACC, lw=2.0, label="$\\bar{\\sigma}(S)$")
    a2.axhline(20 * np.log10(Ms_val), color=BAD, ls="--", lw=1.2,
               label=f"$M_s$={Ms_val:.2f} ({20*np.log10(Ms_val):.1f} dB)")
    a2.axhline(6, color="#aaa", ls=":", lw=1.0, label="6 dB (spec máx)")
    a2.set_xlabel("f [Hz]"); a2.set_ylabel("σ(S) [dB]")
    a2.set_title(f"(b) $\\bar{{\\sigma}}(S)$ y $M_s$ del lazo cerrado GFM\n$M_s$={Ms_val:.2f}")
    a2.legend(fontsize=8.5); a2.grid(True, which="both", alpha=0.3)

    # (c) direccion de entrada de peor ganancia en plano dq a 50 Hz
    w50 = omega0
    Gw50 = G_dq(w50, L1, R1, omega0)
    U50, sv50, Vh50 = np.linalg.svd(Gw50)
    v_worst = Vh50[0, :]  # direccion de entrada de mayor ganancia
    v_best = Vh50[-1, :]
    theta = np.linspace(0, 2 * np.pi, 200)
    ell_d = []; ell_q = []
    for t in theta:
        v = np.array([np.cos(t), np.sin(t)])
        out = np.real(Gw50 @ v.astype(complex))
        ell_d.append(out[0]); ell_q.append(out[1])
    a3.plot(ell_d, ell_q, color=ACC, lw=1.5, label="imagen de la esfera unitaria")
    a3.arrow(0, 0, float(np.real(v_worst[0])) * sv50[0],
             float(np.real(v_worst[1])) * sv50[0],
             color=BAD, width=0.005, label=f"$\\bar{{\\sigma}}$={sv50[0]:.3f} Ω")
    a3.arrow(0, 0, float(np.real(v_best[0])) * sv50[-1],
             float(np.real(v_best[1])) * sv50[-1],
             color=OK, width=0.005, label=f"$\\sigma_{{min}}$={sv50[-1]:.3f} Ohm")
    a3.axhline(0, color="#aaa", lw=0.8); a3.axvline(0, color="#aaa", lw=0.8)
    a3.set_aspect("equal"); a3.set_xlabel("d [Ω]"); a3.set_ylabel("q [Ω]")
    a3.set_title(f"(c) Elipse de $Z_{{dq}}(j2\\pi\\cdot50)$ en plano dq\nκ={sv50[0]/sv50[-1]:.2f}")
    a3.legend(fontsize=8.0)

    # (d) sigma_bar y sigma_un antes y despues del desacoplo
    a4.semilogx(omega / (2 * np.pi), 20 * np.log10(sv_max_nd + 1e-12),
                color=BAD, lw=2.0, label=r"$\bar{\sigma}$ sin desacoplo")
    a4.semilogx(omega / (2 * np.pi), 20 * np.log10(sv_min_nd + 1e-12),
                color=BAD, lw=2.0, ls="--", label=r"$\sigma_{min}$ sin desacoplo")
    a4.semilogx(omega / (2 * np.pi), 20 * np.log10(sv_max_d + 1e-12),
                color=OK, lw=2.0, label=r"$\bar{\sigma}$ con desacoplo FF")
    a4.semilogx(omega / (2 * np.pi), 20 * np.log10(sv_min_d + 1e-12),
                color=OK, lw=2.0, ls="--", label=r"$\sigma_{min}$ con desacoplo FF")
    a4.set_xlabel("f [Hz]"); a4.set_ylabel("σ [dB Ω]")
    a4.set_title("(d) Mejora del κ con desacoplo feedforward\n$\\kappa\\to1$ tras desacoplo")
    a4.legend(fontsize=8.0); a4.grid(True, which="both", alpha=0.3)

    fig.suptitle("Valores singulares MIMO — análisis extendido  "
                 f"(GFM dq, L1={L1*1e3:.0f} mH, R1={R1*1e3:.0f} mΩ, f0=50 Hz)",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _savefig(fig, "valores-singulares-mimo-analisis.png")


# ===================================================================== #
#  clasificacion-estabilidad-analisis  (sin decorador @figura)
# ===================================================================== #
def _clasest():
    """4 paneles: (a) mapa estable/inestable/marginal/BIBO en plano s,
    (b) autovalores GFM vs SCR, (c) funcion Lyapunov V(delta,omega),
    (d) respuesta temporal ROA: dentro converge, fuera diverge."""
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.0))
    (a1, a2), (a3, a4) = axes

    # (a) mapa de clasificaciones en el plano s
    re = np.linspace(-6, 3, 400); im = np.linspace(-6, 6, 400)
    RE, IM = np.meshgrid(re, im)
    # regiones: estable Re<0, inestable Re>0, marginal Re=0
    Z = np.zeros_like(RE)
    Z[RE < -0.3] = 1   # estable asintoticamente
    Z[RE > 0.3] = 3    # inestable
    Z[(RE >= -0.3) & (RE <= 0.3)] = 2  # marginal

    cmap = plt.cm.colors.ListedColormap(["#c8e6c9", "#fff9c4", "#ffcdd2"])
    a1.contourf(RE, IM, Z, levels=[0.5, 1.5, 2.5, 3.5], colors=["#c8e6c9", "#fff9c4", "#ffcdd2"])
    a1.axvline(0, color="#555", lw=1.5)
    a1.scatter([-2, -4], [1, -2], color=ACC, s=80, zorder=5, label="estable A.S.")
    a1.scatter([1.5], [0], color=BAD, s=80, zorder=5, label="inestable")
    a1.scatter([0], [3], color=OK, s=80, marker="^", zorder=5, label="marginal (BIBO-inest.)")
    a1.scatter([0], [-3], color=OK, s=80, marker="^", zorder=5)
    a1.text(-5, 5, "Estable\nA.S.", fontsize=9, color="#2e7d32")
    a1.text(0.5, 5, "Inestable", fontsize=9, color="#b71c1c")
    a1.text(-1.5, -5, "Marginal\n(eje Im)", fontsize=8, color="#f57f17")
    a1.set_xlabel("Re(s)"); a1.set_ylabel("Im(s)")
    a1.set_title("(a) Clasificación en el plano s\nestable / marginal / BIBO-inestable / inestable")
    a1.legend(fontsize=8.0)

    # (b) autovalores del GFM vs SCR (modelo simplificado droop 2 estados)
    # delta_dot = omega0*Domega; Domega_dot = (Pm - Pdelta)/tau_p - Domega/tau_p
    # Linearized: eigenvalues depend on dP/ddelta = Pg*cos(delta0)
    # For simplicity, model as 2-state with SCR-dependent stiffness
    SCRs = [10, 5, 3, 2, 1.5]
    cols_scr = plt.cm.RdYlGn(np.linspace(0.8, 0.1, len(SCRs)))
    omega0 = 2 * np.pi * 50
    tau_p = 0.01  # power filter
    mp = 0.05    # droop
    for scr, col in zip(SCRs, cols_scr):
        Zg = 1.0 / scr  # per unit grid impedance
        # synchronizing torque coefficient (simplified)
        Ks = 1.0 / (Zg + 0.1)  # approximate, degrades with weak grid
        # 2x2 A matrix for [Domega, delta]
        A_sw = np.array([[-1 / tau_p, -mp * Ks / tau_p],
                          [omega0, 0]])
        poles = np.linalg.eigvals(A_sw)
        a2.scatter(poles.real, poles.imag, color=col, s=80, zorder=5,
                   label=f"SCR={scr}")
    a2.axvline(0, color="#555", lw=1.5, ls="--")
    a2.axhline(0, color="#888", lw=0.8)
    a2.set_xlabel("Re(λ) [rad/s]"); a2.set_ylabel("Im(λ) [rad/s]")
    a2.set_title("(b) Autovalores del GFM vs SCR\npérdida de estabilidad con red débil")
    a2.legend(fontsize=8.0)

    # (c) funcion de Lyapunov V(delta, Domega) del oscilador GFM
    delta = np.linspace(-np.pi, np.pi, 200)
    domega = np.linspace(-15, 15, 200)
    D, W = np.meshgrid(delta, domega)
    Pm = 0.8; delta0 = np.arcsin(Pm)
    tau_p_l = 0.01
    # V = (1/2)*tau_p*Domega^2 - mp*Pm*(delta-delta0) + mp*(integral of P(delta'))
    # For P(delta) = sin(delta): integral = -cos(delta)+cos(delta0)
    V = 0.5 * tau_p_l * W**2 - Pm * (D - delta0) + (-np.cos(D) + np.cos(delta0))
    V = np.clip(V, 0, 5)
    cf = a3.contourf(D * 180 / np.pi, W, V, levels=20, cmap="viridis")
    plt.colorbar(cf, ax=a3, shrink=0.8)
    a3.contour(D * 180 / np.pi, W, V, levels=[2.0], colors=["red"], linewidths=2)
    a3.scatter([delta0 * 180 / np.pi], [0], color="white", s=100, zorder=5,
               label=f"equilibrio δ₀={delta0*180/np.pi:.0f}°")
    a3.set_xlabel("δ [°]"); a3.set_ylabel("Δω [rad/s]")
    a3.set_title("(c) $V(\\delta,\\Delta\\omega)$ — función de Lyapunov GFM\ncurva roja: límite estimado de la ROA")
    a3.legend(fontsize=8.5)

    # (d) respuesta temporal dentro y fuera de la ROA
    def sim_gfm(delta0_init, domega0_init, nsteps=5000, dt=2e-4):
        d = delta0_init; w = domega0_init
        Pm_sim = 0.8; tau_s = 0.01; mp_s = 0.05
        d_traj = [d]; w_traj = [w]
        for _ in range(nsteps):
            Pdelta = np.sin(d)
            ddot = (Pm_sim - Pdelta) / tau_s - w / tau_s
            wdot = omega0 * w
            # simplification: delta dynamics
            d_new = d + dt * (omega0 * w)
            w_new = w + dt * ((Pm_sim - np.sin(d)) / tau_s - w / tau_s)
            d = d_new; w = w_new
            d_traj.append(d); w_traj.append(w)
        return np.array(d_traj), np.array(w_traj)

    t_ax = np.arange(0, 5001) * 2e-4
    # inside ROA
    d1, w1 = sim_gfm(delta0 + 0.3, 2.0)
    # outside ROA
    d2, w2 = sim_gfm(delta0 + 1.2, 5.0)
    a4.plot(t_ax, np.sin(d1), color=OK, lw=2.0, label="dentro ROA — converge")
    a4.plot(t_ax, np.sin(d2), color=BAD, lw=2.0, label="fuera ROA — diverge")
    a4.axhline(Pm, color="#888", ls=":", lw=1.2, label=f"$P_m$={Pm}")
    a4.set_xlabel("t [s]"); a4.set_ylabel("P(δ) = sin(δ)")
    a4.set_title("(d) Respuesta temporal del GFM\ndentro/fuera de la región de atracción")
    a4.legend(fontsize=8.5); a4.set_xlim(0, 1.0)

    fig.suptitle("Clasificación de estabilidad — análisis extendido  "
                 "(GFM: pequeña señal, Lyapunov, ROA, SCR crítico)",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _savefig(fig, "clasificacion-estabilidad-analisis.png")


# ===================================================================== #
#  armonicos-thd-analisis  (sin decorador @figura)
# ===================================================================== #
def _thdext():
    """4 paneles: (a) espectro iL2 antes/después LCL, (b) Bode LCL iL2/iL1,
    (c) THD_I en PCC vs L2, (d) APF: espectro antes y después compensación."""
    from scipy import signal as scsignal
    fig, axes = plt.subplots(2, 2, figsize=(12.0, 9.0))
    (a1, a2), (a3, a4) = axes

    f1 = 50.0; fsw = 10e3; Vdc = 800.0; m = 0.85
    fs = 200e3; N = int(fs / f1) * 20
    t = np.arange(N) / fs
    Vfund = m * Vdc / 2.0 * np.sqrt(2)
    sig = Vfund * np.sin(2 * np.pi * f1 * t)
    mf = int(fsw / f1)
    for k in [1, 2, 3]:
        A_k = Vdc / np.pi / k * 0.6
        for offset in [-2, 2]:
            fh = k * fsw + offset * f1
            if fh > 0:
                sig += A_k * np.sin(2 * np.pi * fh * t)
    # Armónicos tiempo muerto (5°, 7°, 11°, 13°)
    for h_ord, amp in [(5, 0.04), (7, 0.028), (11, 0.015), (13, 0.010)]:
        sig += Vfund * amp * np.sin(2 * np.pi * h_ord * f1 * t)

    win = np.hanning(N)
    X = np.abs(np.fft.rfft(sig * win)) * 2.0 / N
    freq = np.fft.rfftfreq(N, 1.0 / fs)

    L1 = 2e-3; L2 = 0.5e-3; Cf = 10e-6
    Leq = L1 * L2 / (L1 + L2)
    fres_lcl = 1.0 / (2 * np.pi * np.sqrt(Leq * Cf))

    def lcl_atten(f):
        x = (f / np.maximum(fres_lcl, 1.0)) ** 2
        return np.where(f < fres_lcl, np.ones_like(f),
                        1.0 / np.abs(1 - x) / np.maximum(x, 1e-12))

    X_after = X * lcl_atten(freq)

    # (a) Espectro antes y después del LCL
    f_kHz = freq / 1e3
    mask = freq <= 35e3
    a1.semilogy(f_kHz[mask], np.maximum(X[mask], 1e-2), color=BAD, lw=1.5,
                label="antes del LCL", alpha=0.85)
    a1.semilogy(f_kHz[mask], np.maximum(X_after[mask], 1e-2), color=ACC, lw=1.5,
                label="después del LCL", alpha=0.85)
    a1.axvline(fres_lcl / 1e3, color="#aaa", ls=":", lw=1.2,
               label=f"$f_{{res}}$={fres_lcl/1e3:.1f} kHz")
    a1.axvline(fsw / 1e3, color=ACC2, ls="--", lw=1.2,
               label=f"$f_{{sw}}$={fsw/1e3:.0f} kHz")
    a1.set_xlabel("f [kHz]"); a1.set_ylabel("|X(f)| [V]")
    a1.set_title(f"(a) Espectro corriente inversor: $f_{{sw}}$={fsw/1e3:.0f} kHz\n"
                 f"LCL: $L_1$={L1*1e3:.0f} mH, $L_2$={L2*1e3:.1f} mH, $C_f$={Cf*1e6:.0f} µF")
    a1.legend(fontsize=8.5)

    # (b) Bode del LCL: iL2/iL1 (función de transferencia)
    f_bode = np.logspace(1, 5, 500)
    w_bode = 2 * np.pi * f_bode
    # G(s) = 1 / (1 + s^2 * Leq * Cf)
    G_lcl = 1.0 / np.abs(1 - w_bode ** 2 * Leq * Cf)
    mag_db = 20 * np.log10(np.maximum(G_lcl, 1e-10))
    a2.semilogx(f_bode, mag_db, color=ACC, lw=2.0)
    a2.axvline(fres_lcl, color=BAD, ls="--", lw=1.2,
               label=f"$f_{{res}}$={fres_lcl:.0f} Hz")
    a2.axvline(fsw, color=ACC2, ls=":", lw=1.2, label=f"$f_{{sw}}$={fsw/1e3:.0f} kHz")
    a2.axhline(-60, color="#888", ls=":", lw=1.0, label="-60 dB")
    a2.set_xlabel("f [Hz]"); a2.set_ylabel("$|G_{LCL}|$ [dB]")
    a2.set_title("(b) Bode LCL $i_{L2}/v_{inv}$: −60 dB/dec tras $f_{res}$\n"
                 "atenuación en $f_{sw}$: −60 dB (factor 1000×)")
    a2.legend(fontsize=8.5); a2.set_ylim(-100, 20)

    # (c) THD_I en PCC vs L2
    L2_vals = np.linspace(0.1e-3, 3e-3, 40)
    thd_l2 = []
    I_fund_ref = Vfund / 100.0
    for L2v in L2_vals:
        Leq_v = L1 * L2v / (L1 + L2v)
        fres_v = 1.0 / (2 * np.pi * np.sqrt(Leq_v * Cf))
        Ihsq = 0.0
        for h in range(2, 60):
            fh = h * f1
            if fh > freq[-1]:
                break
            idx = np.argmin(np.abs(freq - fh))
            x_v = (fh / max(fres_v, 1.0)) ** 2
            att = 1.0 if fh < fres_v else 1.0 / abs(1 - x_v + 1e-12) / max(x_v, 1e-9)
            Ih = X[idx] * att / 100.0
            Ihsq += Ih ** 2
        thd_l2.append(100 * np.sqrt(Ihsq) / I_fund_ref)
    a3.plot(L2_vals * 1e3, thd_l2, color=ACC, lw=2.0)
    a3.axhline(5.0, color=BAD, ls="--", lw=1.2, label="Límite 5 % IEEE 519")
    a3.axvline(L2 * 1e3, color="#888", ls=":", lw=1.2,
               label=f"$L_2$={L2*1e3:.1f} mH (diseño)")
    a3.set_xlabel("$L_2$ [mH]"); a3.set_ylabel("THD_I en PCC [%]")
    a3.set_title("(c) THD_I en PCC vs inductancia $L_2$\n"
                 "mayor $L_2$ mejora THD (y sube reactancia)")
    a3.legend(fontsize=9); a3.set_ylim(0, None)

    # (d) APF: espectro antes y después de la compensación
    harm_orders_apf = [5, 7, 11, 13]
    orders_plot = np.arange(1, 25)
    amps_before, amps_after = [], []
    for h in orders_plot:
        fh = h * f1
        idx = np.argmin(np.abs(freq - fh))
        Ih_before = X_after[idx] / 100.0  # ya tras el LCL
        # APF compensa 5, 7, 11, 13 con 95 % de eficiencia
        if h in harm_orders_apf:
            Ih_after = Ih_before * 0.05
        else:
            Ih_after = Ih_before
        amps_before.append(Ih_before * 100)
        amps_after.append(Ih_after * 100)
    x_pos = np.arange(len(orders_plot))
    a4.bar(x_pos - 0.2, amps_before, width=0.35, color=BAD, alpha=0.7,
           label="sin APF")
    a4.bar(x_pos + 0.2, amps_after, width=0.35, color=ACC, alpha=0.8,
           label="con APF (5°, 7°, 11°, 13°)")
    a4.set_xticks(x_pos); a4.set_xticklabels([str(h) for h in orders_plot], fontsize=7)
    a4.set_xlabel("Orden armónico"); a4.set_ylabel("$I_h$ [% de $I_1$]")
    a4.set_title("(d) APF: espectro antes y después de la compensación\n"
                 "los 4 armónicos dominantes bajan >95 %")
    a4.legend(fontsize=9)

    fig.suptitle("Armónicos y THD: espectro LCL, Bode, THD vs $L_2$ y efecto APF",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    _savefig(fig, "armonicos-thd-analisis.png")


def _deteccion_islanding_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    ax = axes[0, 0]
    dP = np.linspace(-0.5, 0.5, 200); dQ = np.linspace(-0.5, 0.5, 200)
    DP, DQ = np.meshgrid(dP, dQ)
    NDZ = (np.abs(DP) < 0.05) & (np.abs(DQ) < 0.1)
    ax.contourf(dP, dQ, NDZ.astype(float), levels=[0.5, 1], colors=['red'], alpha=0.4)
    ax.axhline(0, color='k', ls='--'); ax.axvline(0, color='k', ls='--')
    ax.set_xlabel('ΔP (pu)'); ax.set_ylabel('ΔQ (pu)')
    ax.set_title('Zona de no-detección (NDZ)'); ax.grid(True, alpha=0.3)
    ax.text(0, 0, 'NDZ', ha='center', va='center', color='red', fontsize=14, fontweight='bold')
    ax = axes[0, 1]
    np.random.seed(42)
    t = np.linspace(0, 2, 1000)
    f_norm = 50 + 0.05*np.sin(2*np.pi*0.5*t) + 0.01*np.random.randn(len(t))
    f_isl = 50*np.ones(len(t))
    f_isl[t > 0.5] = 50 - 0.8*(t[t > 0.5] - 0.5)
    ax.plot(t, f_norm, 'b-', lw=1.5, label='Normal')
    ax.plot(t, f_isl, 'r-', lw=1.5, label='Islanding')
    ax.axhline(49.5, color='orange', ls='--', label='Límite UFP')
    ax.set_xlabel('Tiempo (s)'); ax.set_ylabel('Frecuencia (Hz)')
    ax.set_title('Frecuencia: normal vs islanding'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax = axes[1, 0]
    rocof_norm = np.gradient(f_norm, t)
    rocof_isl = np.gradient(f_isl, t)
    ax.plot(t, rocof_norm, 'b-', lw=1.5, label='Normal')
    ax.plot(t, rocof_isl, 'r-', lw=1.5, label='Islanding')
    ax.axhline(0.5, color='r', ls='--', label='Umbral 0.5 Hz/s')
    ax.axhline(-0.5, color='r', ls='--')
    ax.set_xlabel('Tiempo (s)'); ax.set_ylabel('ROCOF (Hz/s)')
    ax.set_title('ROCOF: detección de islanding'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax.set_ylim([-2, 2])
    ax = axes[1, 1]; ax.axis('off')
    eventos = [('0.0 s', 'Operación normal', 'green'),
               ('0.5 s', 'Apertura disyuntor red', 'red'),
               ('0.55 s', 'Detección ROCOF>0.5', 'orange'),
               ('0.6 s', 'Disparo inversor', 'red'),
               ('0.6-1.0 s', 'Espera ≥300 ms', 'yellow'),
               ('1.0 s', 'Verificar ΔV,Δf,Δθ', 'blue'),
               ('1.1 s', 'Reconexión suave', 'green')]
    for i, (tiempo, evento, col) in enumerate(eventos):
        ax.add_patch(plt.Rectangle((0.0, 0.9-i*0.13), 0.25, 0.1, color=col, alpha=0.6))
        ax.text(0.13, 0.95-i*0.13, tiempo, ha='center', va='center', fontsize=9, fontweight='bold')
        ax.text(0.3, 0.95-i*0.13, evento, va='center', fontsize=9)
    ax.set_xlim([0, 1]); ax.set_ylim([0, 1]); ax.set_title('Secuencia: detección → reconexión')
    fig.suptitle('Detección de islanding: NDZ, ROCOF y reconexión', fontsize=14, fontweight='bold')
    plt.tight_layout()
    _savefig(fig, 'deteccion-islanding-analisis')


def _fenomenos_oscilatorios_red_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    np.random.seed(42)
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    ax = axes[0, 0]
    fs = 10000; T = 2.0; t = np.arange(0, T, 1/fs)
    v = np.sin(2*np.pi*50*t) + 0.05*np.sin(2*np.pi*25*t)
    V_f = np.abs(np.fft.rfft(v))*2/len(t); f_fft = np.fft.rfftfreq(len(t), 1/fs)
    ax.plot(f_fft, V_f, 'b-', lw=1)
    ax.axvline(50, color='r', ls='--', label='Fundamental 50 Hz')
    ax.axvline(25, color='orange', ls='--', label='SSO 25 Hz')
    ax.set_xlim([0, 200]); ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Amplitud (pu)')
    ax.set_title('Espectro con SSO visible'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax = axes[0, 1]
    w = np.logspace(1, 4, 500); f_pll = 20; w_pll = 2*np.pi*f_pll
    Z_re = 0.5 - 1.5*w_pll**2/(w**2 + w_pll**2)
    ax.semilogx(w/(2*np.pi), Z_re, 'b-', lw=2, label='Re[Z_inv] GFL')
    ax.axhline(0, color='k', lw=1)
    ax.fill_between(w/(2*np.pi), Z_re, 0, where=Z_re < 0, alpha=0.2, color='red', label='Zona negativa')
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Re[Z] (pu)')
    ax.set_title('Impedancia GFL — zona negativa'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax = axes[1, 0]
    for scr, mk in [(1.5, 'o'), (2, 's'), (3, '^'), (5, 'D'), (10, 'v')]:
        sigma = -2*scr; wd = 2*np.pi*20/scr
        ax.scatter([sigma, sigma], [wd, -wd], s=100, marker=mk, label=f'SCR={scr}', zorder=5)
    ax.axvline(0, color='k', lw=1.5); ax.axhline(0, color='k', lw=0.5)
    ax.set_xlabel('Re(λ)'); ax.set_ylabel('Im(λ)')
    ax.set_title('Eigenvalores vs SCR'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax = axes[1, 1]
    t2 = np.linspace(0, 5, 1000); f_osc = 5
    P1 = 0.5 + 0.1*np.cos(2*np.pi*f_osc*t2)*np.exp(-t2*1.5)
    P2 = 0.5 - 0.1*np.cos(2*np.pi*f_osc*t2)*np.exp(-t2*1.5)
    ax.plot(t2, P1, 'b-', lw=2, label='P_inv1'); ax.plot(t2, P2, 'r-', lw=2, label='P_inv2')
    ax.axhline(0.5, color='k', ls='--', alpha=0.5)
    ax.set_xlabel('Tiempo (s)'); ax.set_ylabel('P (pu)')
    ax.set_title('Oscilación de droop entre inversores'); ax.legend(); ax.grid(True, alpha=0.3)
    fig.suptitle('Fenómenos oscilatorios: SSO, impedancia GFL y droop', fontsize=14, fontweight='bold')
    plt.tight_layout()
    _savefig(fig, 'fenomenos-oscilatorios-red-analisis')


def _virtual_oscillator_control_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    dt = 1e-5; T_sim = 0.5; mu = 0.5; w0 = 2*np.pi*50; N = int(T_sim/dt)
    v = np.zeros(N); dv = np.zeros(N); v[0] = 0.1
    for i in range(1, N):
        ddv = mu*(1-v[i-1]**2)*dv[i-1] - w0**2*v[i-1]
        dv[i] = dv[i-1] + ddv*dt; v[i] = v[i-1] + dv[i-1]*dt
    ax = axes[0, 0]; ax.plot(v[N//4:], dv[N//4:]/w0, 'b-', lw=1, alpha=0.8)
    ax.set_xlabel('v (pu)'); ax.set_ylabel('dv/dt / ω₀'); ax.set_title('Ciclo límite de Van der Pol')
    ax.grid(True, alpha=0.3); ax.set_aspect('equal')
    ax = axes[0, 1]; t_voc = np.arange(N)*dt
    ax.plot(t_voc*1000, v, 'b-', lw=1.5)
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Tensión (pu)')
    ax.set_title('Arranque VOC — convergencia al ciclo límite'); ax.grid(True, alpha=0.3); ax.set_xlim([0, 100])
    N2 = int(0.3/dt); K_coup = 5
    v1 = np.zeros(N2); dv1 = np.zeros(N2); v2 = np.zeros(N2); dv2 = np.zeros(N2)
    v1[0] = 0.5; dv2[0] = w0
    for i in range(1, N2):
        ddv1 = mu*(1-v1[i-1]**2)*dv1[i-1] - w0**2*v1[i-1] + K_coup*(v2[i-1]-v1[i-1])
        ddv2 = mu*(1-v2[i-1]**2)*dv2[i-1] - w0**2*v2[i-1] + K_coup*(v1[i-1]-v2[i-1])
        dv1[i] = dv1[i-1]+ddv1*dt; v1[i] = v1[i-1]+dv1[i-1]*dt
        dv2[i] = dv2[i-1]+ddv2*dt; v2[i] = v2[i-1]+dv2[i-1]*dt
    ax = axes[1, 0]; t2_voc = np.arange(N2)*dt
    ax.plot(t2_voc*1000, v1, 'b-', lw=1.5, label='VOC 1'); ax.plot(t2_voc*1000, v2, 'r-', lw=1.5, label='VOC 2')
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Tensión (pu)')
    ax.set_title('Sincronización de dos VOC acoplados'); ax.legend(); ax.grid(True, alpha=0.3); ax.set_xlim([0, 100])
    ax = axes[1, 1]; ax.axis('off')
    data = [['Propiedad', 'VOC', 'Droop', 'VSG'],
            ['Inercia', 'Ciclo límite', 'No', 'Sí (J)'],
            ['Est. gran señal', 'Muy alta', 'Media', 'Media'],
            ['Sincronización', 'Automática', 'Droop f', 'Droop f'],
            ['PLL necesario', 'No', 'No', 'No'],
            ['Complejidad', 'Media', 'Baja', 'Media-alta']]
    t_obj = ax.table(cellText=data[1:], colLabels=data[0], cellLoc='center', loc='center',
                     colWidths=[0.32, 0.22, 0.22, 0.24])
    t_obj.auto_set_font_size(False); t_obj.set_fontsize(9); t_obj.scale(1, 1.5)
    ax.set_title('Comparativa VOC / Droop / VSG')
    fig.suptitle('Virtual Oscillator Control: Van der Pol, sincronización y comparativa', fontsize=14, fontweight='bold')
    plt.tight_layout()
    _savefig(fig, 'virtual-oscillator-control-analisis')


def _validacion_cruzada_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    np.random.seed(42)
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    ax = axes[0, 0]
    N = 100; k = 5; fold = N // k
    colors_cv = ['#4C72B0', '#DD8452', '#55A868', '#C44E52', '#8172B2']
    for i in range(k):
        s = i*fold; e = (i+1)*fold
        ax.barh(0, fold, left=s, height=0.4, color=colors_cv[i], alpha=0.85, label=f'Fold {i+1}')
    ax.axvline(0.6*N, color='k', ls='--', lw=1.5, label='60% entrenamiento')
    ax.set_xlabel('Índice de muestra temporal'); ax.set_yticks([])
    ax.set_title('k-fold temporal (k=5): bloques consecutivos')
    ax.legend(fontsize=8, ncol=3); ax.set_xlim([0, N])
    ax = axes[0, 1]
    Ns = np.arange(10, 101, 5)
    err_train = 0.05 + 0.15*np.exp(-Ns/20)
    err_val = 0.25 - 0.15*np.exp(-Ns/30) + 0.02*np.random.randn(len(Ns))
    err_val = np.maximum(err_val, 0.08)
    ax.plot(Ns, err_train, 'b-o', ms=4, lw=1.5, label='Error entrenamiento')
    ax.plot(Ns, err_val, 'r-s', ms=4, lw=1.5, label='Error validación')
    ax.axhline(0.1, color='gray', ls='--', lw=1, label='Umbral aceptable')
    ax.set_xlabel('N muestras'); ax.set_ylabel('NRMSE')
    ax.set_title('Curva de aprendizaje'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax = axes[1, 0]
    ordenes = np.arange(1, 9)
    fit_train = np.clip(70 + 25*(1-np.exp(-ordenes*0.8)) + 1*np.random.randn(len(ordenes)), 40, 99)
    fit_val = np.clip(65 + 22*(1-np.exp(-ordenes*0.6)) - 2*(ordenes > 4)*(ordenes - 4)**1.5
                      + 0.5*np.random.randn(len(ordenes)), 40, 98)
    ax.plot(ordenes, fit_train, 'b-o', ms=6, lw=1.5, label='FIT% entrenamiento')
    ax.plot(ordenes, fit_val, 'r-s', ms=6, lw=1.5, label='FIT% validación')
    ax.axhline(80, color='g', ls='--', lw=1.5, label='Umbral 80%')
    ax.axvline(2, color='purple', ls=':', lw=2, label='Orden elegido (codo)')
    ax.set_xlabel('Orden del modelo'); ax.set_ylabel('FIT (%)')
    ax.set_title('FIT% vs orden del modelo — criterio del codo')
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax = axes[1, 1]
    f_vc = np.logspace(0, 3, 200); wc = 2*np.pi*500
    G_anal = 1/(1 + 1j*f_vc*2*np.pi/wc)
    G_ident = G_anal * (1 + 0.03*np.random.randn(len(f_vc)) + 0.02j*np.random.randn(len(f_vc)))
    ax.semilogx(f_vc, 20*np.log10(np.abs(G_anal)), 'b-', lw=2, label='Analítica')
    ax.semilogx(f_vc, 20*np.log10(np.abs(G_ident)), 'r--', lw=1.5, label='Identificada (PRBS)')
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('|G| (dB)')
    ax.set_title('Lazo corriente: analítica vs identificada'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    fig.suptitle('Validación cruzada: k-fold temporal, curva de aprendizaje y FIT% vs orden', fontsize=13, fontweight='bold')
    plt.tight_layout()
    _savefig(fig, 'validacion-cruzada-analisis')


def _niveles_validacion_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    ax = axes[0, 0]
    niveles_nv = ['SiL', 'HiL', 'PHiL', 'Prototipo', 'Campo']
    coste_nv = [1, 10, 100, 300, 1000]
    cobertura_nv = [95, 85, 70, 60, 40]
    colors_nv = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c', '#9b59b6']
    ax.barh(niveles_nv, coste_nv, color=colors_nv, alpha=0.8)
    ax2 = ax.twiny()
    ax2.plot(cobertura_nv, niveles_nv, 'ko--', ms=6, lw=1.5, label='Cobertura (%)')
    ax.set_xlabel('Coste relativo'); ax.set_xscale('log')
    ax2.set_xlabel('Cobertura lógica (%)'); ax2.set_xlim([0, 110])
    ax.set_title('Pirámide: coste vs cobertura por nivel'); ax2.legend(fontsize=9)
    ax = axes[0, 1]
    niveles_pm_nv = ['Lineal', 'Promediado', 'Conmutado', 'HiL']
    pm_nv = [72, 68, 54, 43]
    colores_pm_nv = ['green' if p >= 45 else 'red' for p in pm_nv]
    bars_nv = ax.bar(niveles_pm_nv, pm_nv, color=colores_pm_nv, alpha=0.8)
    ax.axhline(45, color='k', ls='--', lw=2, label='Límite PM=45°')
    ax.set_ylabel('Margen de fase (°)'); ax.set_title('PM por nivel: HiL detecta el problema')
    ax.legend(fontsize=9); ax.set_ylim([0, 90])
    for bar, val in zip(bars_nv, pm_nv):
        ax.text(bar.get_x()+bar.get_width()/2, val+1, f'{val}°', ha='center', fontsize=10, fontweight='bold')
    ax = axes[1, 0]
    niveles_err = ['SiL', 'HiL', 'PHiL', 'Prototipo', 'Campo']
    coste_corr = [1, 5, 20, 100, 500]
    ax.semilogy(niveles_err, coste_corr, 'ro-', ms=8, lw=2)
    ax.fill_between(range(len(niveles_err)), coste_corr, alpha=0.2, color='red')
    ax.set_ylabel('Coste relativo de corrección')
    ax.set_title('Coste de corrección de errores por nivel'); ax.grid(True, alpha=0.3, which='both')
    for i, (n, c) in enumerate(zip(niveles_err, coste_corr)):
        ax.text(i, c*1.3, f'{c}×', ha='center', fontsize=9, fontweight='bold')
    ax = axes[1, 1]; ax.axis('off')
    datos_nv = [['Nivel', 'Error típico detectado'],
                ['Lineal', 'Diseño de lazo, márgenes'],
                ['No lineal', 'Saturación, gran señal'],
                ['Conmutado', 'Rizado, retardo, THD'],
                ['SiL', 'Lógica, máquinas de estado'],
                ['HiL', 'Latencia ADC, overrun ISR'],
                ['PHiL', 'EMC, térmica, red real']]
    t_nv = ax.table(cellText=datos_nv[1:], colLabels=datos_nv[0], cellLoc='left', loc='center',
                    colWidths=[0.3, 0.7])
    t_nv.auto_set_font_size(False); t_nv.set_fontsize(9); t_nv.scale(1, 1.6)
    ax.set_title('Errores típicos detectados por nivel')
    fig.suptitle('Niveles de validación: coste, cobertura, PM y errores', fontsize=13, fontweight='bold')
    plt.tight_layout()
    _savefig(fig, 'niveles-validacion-analisis')


def _ciclo_diseno_control_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    np.random.seed(42)
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    ax = axes[0, 0]; ax.axis('off')
    fases_cdc = [('DISEÑAR', 0.5, 0.82, '#3498db'),
                 ('EVALUAR', 0.5, 0.50, '#e67e22'),
                 ('VALIDAR', 0.5, 0.18, '#2ecc71')]
    for nombre, x, y, col in fases_cdc:
        circ = plt.Circle((x, y), 0.13, color=col, alpha=0.8)
        ax.add_patch(circ)
        ax.text(x, y, nombre, ha='center', va='center', fontsize=11, fontweight='bold', color='white')
    ax.annotate('', xy=(0.5, 0.63), xytext=(0.5, 0.69), arrowprops=dict(arrowstyle='->', lw=2))
    ax.annotate('', xy=(0.5, 0.31), xytext=(0.5, 0.37), arrowprops=dict(arrowstyle='->', lw=2))
    ax.text(0.12, 0.35, 'Rediseño', rotation=90, va='center', fontsize=9, color='gray')
    ax.set_xlim([0, 1]); ax.set_ylim([0, 1]); ax.set_title('Ciclo Diseñar → Evaluar → Validar')
    ax = axes[0, 1]
    L1_n_cdc, L2_n_cdc = 2e-3, 1e-3; Td_cdc = 100e-6; fc_cdc = 500.0
    N_mc = 1000
    L1s = L1_n_cdc*(1+0.3*np.random.uniform(-1, 1, N_mc))
    L2s = L2_n_cdc*(1+0.3*np.random.uniform(-1, 1, N_mc))
    wc_cdc = 2*np.pi*fc_cdc
    pms_cdc = 90 - np.degrees(np.arctan(wc_cdc*(L1s+L2s))) - wc_cdc*Td_cdc*180/np.pi
    ax.hist(pms_cdc, bins=40, color='steelblue', alpha=0.8, edgecolor='k', lw=0.5)
    ax.axvline(45, color='r', ls='--', lw=2, label='Límite PM=45°')
    ax.axvline(np.mean(pms_cdc), color='g', ls='--', lw=2, label=f'Media={np.mean(pms_cdc):.1f}°')
    pct_ok = np.mean(pms_cdc >= 45)*100
    ax.set_xlabel('Margen de fase (°)'); ax.set_ylabel('Realizaciones')
    ax.set_title(f'Monte Carlo: PM con L1,L2 ±30%\n{pct_ok:.1f}% cumple PM≥45°')
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax = axes[1, 0]
    f_cdc = np.logspace(1, 4, 500); w_cdc = 2*np.pi*f_cdc
    L_tot = L1_n_cdc + L2_n_cdc; R_cdc = 0.1
    G_cdc = 1/(R_cdc + 1j*w_cdc*L_tot)
    Kp_cdc = 2; Ti_cdc = L_tot/R_cdc
    C_cdc = Kp_cdc*(1 + 1/(1j*w_cdc*Ti_cdc))
    loop_cdc = C_cdc*G_cdc*np.exp(-1j*w_cdc*Td_cdc)
    mag_db_cdc = 20*np.log10(np.abs(loop_cdc))
    fc_idx = np.argmin(np.abs(mag_db_cdc))
    ax.semilogx(f_cdc, mag_db_cdc, 'b-', lw=2, label='|L(jω)| dB')
    ax.axhline(0, color='k', lw=1)
    ax.axvline(f_cdc[fc_idx], color='g', ls='--', lw=1.5, label=f'fc={f_cdc[fc_idx]:.0f} Hz')
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Magnitud (dB)')
    ax.set_title('Bode lazo abierto — fc marcada'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax = axes[1, 1]; ax.axis('off')
    data_cdc = [['Requisito', 'Spec', 'Resultado'],
                ['Sobreimpulso<10%', 'ζ>0.59', 'Mp=7% ✓'],
                ['Robustez', 'PM≥45°', 'PM=54° ✓'],
                ['THD<5%', 'Filtro LCL', 'THD=3.8% ✓'],
                ['SCR crítico<3', 'Z análisis', 'SCR_c=3.35 ✓'],
                ['Falta: <1.5pu', 'Curr. lim.', '1.12 pu ✓']]
    t_cdc = ax.table(cellText=data_cdc[1:], colLabels=data_cdc[0], cellLoc='center', loc='center',
                     colWidths=[0.38, 0.28, 0.34])
    t_cdc.auto_set_font_size(False); t_cdc.set_fontsize(9); t_cdc.scale(1, 1.6)
    ax.set_title('Trazabilidad: requisito → spec → resultado')
    fig.suptitle('Ciclo de diseño de control: DEV, Monte Carlo y trazabilidad', fontsize=13, fontweight='bold')
    plt.tight_layout()
    _savefig(fig, 'ciclo-diseno-control-analisis')


def _calidad_potencia_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    ax = axes[0, 0]
    ordenes_cp = np.arange(1, 26)
    Ih_cp = np.zeros(len(ordenes_cp))
    Ih_cp[0] = 100.0
    for i, h in enumerate(ordenes_cp):
        if h in [5, 7]: Ih_cp[i] = 3.5
        elif h in [11, 13]: Ih_cp[i] = 1.8
        elif h in [17, 19]: Ih_cp[i] = 0.8
        elif h > 1: Ih_cp[i] = 0.3
    limites_cp = np.where(ordenes_cp < 11, 4.0, np.where(ordenes_cp < 17, 2.0,
                          np.where(ordenes_cp < 23, 1.5, 0.6)))
    limites_cp[0] = 120
    ax.bar(ordenes_cp, Ih_cp,
           color=['green' if Ih_cp[i] <= limites_cp[i] else 'red' for i in range(len(ordenes_cp))],
           alpha=0.7, label='Ih medido')
    ax.step(ordenes_cp, limites_cp, where='mid', color='k', lw=2, ls='--', label='Límite IEEE 519')
    ax.set_xlabel('Orden armónico'); ax.set_ylabel('Ih (% de I1)')
    ax.set_title('Espectro de corriente vs límites IEEE 519\n(SCR<20, THD_I<5%)')
    ax.legend(fontsize=8); ax.set_xlim([0, 26]); ax.grid(True, alpha=0.3)
    ax = axes[0, 1]
    f_fl = np.linspace(0.1, 35, 500)
    sens = 1.5*np.exp(-((np.log(f_fl/8.8))**2)/(2*0.8**2))
    ax.plot(f_fl, sens, 'b-', lw=2, label='Sensibilidad visual (IEC 61000-4-15)')
    ax.axvline(8.8, color='r', ls='--', lw=1.5, label='Máximo 8.8 Hz')
    ax.axhline(1.0, color='orange', ls='--', lw=1.5, label='Pst=1 (límite)')
    ax.fill_between(f_fl, sens, 1.0, where=sens > 1.0, alpha=0.2, color='red')
    ax.set_xlabel('Frecuencia de variación (Hz)'); ax.set_ylabel('Sensibilidad normalizada')
    ax.set_title('Curva de susceptibilidad visual al flicker'); ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3); ax.set_xlim([0, 35])
    ax = axes[1, 0]
    theta_vec = np.linspace(0, 2*np.pi, 300)
    Va_cp = np.exp(1j*0); Vb_cp = 0.95*np.exp(1j*(-2*np.pi/3)); Vc_cp = 1.03*np.exp(1j*(2*np.pi/3))
    for V_ph, lbl, col in [(Va_cp, 'Va', 'blue'), (Vb_cp, 'Vb', 'green'), (Vc_cp, 'Vc', 'red')]:
        ax.annotate('', xy=(V_ph.real, V_ph.imag), xytext=(0, 0),
                    arrowprops=dict(arrowstyle='->', color=col, lw=2))
        ax.text(V_ph.real*1.1, V_ph.imag*1.1, lbl, color=col, fontsize=10, fontweight='bold')
    ax.plot(np.cos(theta_vec), np.sin(theta_vec), 'gray', lw=0.5, ls='--', alpha=0.5)
    a_cp = np.exp(1j*2*np.pi/3)
    Vneg = abs(Va_cp + a_cp**2*Vb_cp + a_cp*Vc_cp)/3
    Vpos = abs(Va_cp + a_cp*Vb_cp + a_cp**2*Vc_cp)/3
    VUF = Vneg/Vpos*100
    ax.set_xlim([-1.3, 1.3]); ax.set_ylim([-1.3, 1.3]); ax.set_aspect('equal')
    ax.set_xlabel('Re'); ax.set_ylabel('Im')
    ax.set_title(f'Desequilibrio vectorial: VUF={VUF:.1f}%\n(límite EN 50160: VUF<2%)')
    ax.grid(True, alpha=0.3)
    ax = axes[1, 1]
    t_dc = np.linspace(0, 0.1, 2000); fsw_cp = 5000; Vdc_cp = 800
    rizado = 8*np.sin(2*np.pi*fsw_cp*t_dc) + 4*np.sin(2*np.pi*2*fsw_cp*t_dc)
    step_idx = int(0.05*len(t_dc))
    transitorio = np.zeros(len(t_dc))
    transitorio[step_idx:] = 30*np.exp(-(t_dc[step_idx:]-t_dc[step_idx])/0.005)
    Vbus = Vdc_cp + rizado + transitorio
    ax.plot(t_dc*1000, Vbus, 'b-', lw=1.2, label='V_dc')
    ax.axhline(Vdc_cp*1.01, color='r', ls='--', lw=1, label='±1% límite')
    ax.axhline(Vdc_cp*0.99, color='r', ls='--', lw=1)
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Tensión DC (V)')
    ax.set_title('Rizado bus DC: conmutación + transitorio\nΔVdc<1% en régimen permanente')
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    fig.suptitle('Calidad de potencia: IEEE 519, flicker, VUF y rizado DC', fontsize=13, fontweight='bold')
    plt.tight_layout()
    _savefig(fig, 'calidad-potencia-analisis')


def _integracion_edos_stiff_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    ax = axes[0, 0]
    lam_f = -100.0; lam_s = -1.0
    t_ex = np.linspace(0, 0.1, 1000)
    y_exact = np.exp(lam_f*t_ex) + np.exp(lam_s*t_ex)
    ax.plot(t_ex*1000, y_exact, 'k-', lw=2.5, label='Exacta', zorder=5)
    for h, col, lbl in [(0.005, 'blue', 'h=5ms'), (0.015, 'orange', 'h=15ms'), (0.025, 'red', 'h=25ms')]:
        t_num = np.arange(0, 0.1+h, h)
        y_e = np.zeros(len(t_num)); y_e[0] = 2.0
        for i in range(1, len(t_num)):
            y_e[i] = y_e[i-1] + h*(lam_f*y_e[i-1]*0.5 + lam_s*y_e[i-1]*0.5)
        ax.plot(t_num*1000, np.clip(y_e, -5, 5), '--', color=col, lw=1.5, label=f'Euler expl. {lbl}')
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('y(t)')
    ax.set_title('Euler explícito inestable en sistema stiff\nλ_fast=-100, λ_slow=-1')
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3); ax.set_ylim([-5, 5])
    ax = axes[0, 1]
    x_re = np.linspace(-3.5, 1.5, 400); y_im = np.linspace(-3, 3, 400)
    X_st, Y_st = np.meshgrid(x_re, y_im)
    Z_st = X_st + 1j*Y_st
    R_expl = np.abs(1 + Z_st)
    R_impl = np.abs(1/(1 - Z_st))
    ax.contourf(x_re, y_im, R_expl < 1, levels=[0.5, 1.5], colors=['#3498db'], alpha=0.5)
    ax.contourf(x_re, y_im, R_impl < 1, levels=[0.5, 1.5], colors=['#2ecc71'], alpha=0.3)
    ax.axvline(0, color='k', lw=1.5); ax.axhline(0, color='k', lw=0.5)
    ax.plot([], [], 's', color='#3498db', alpha=0.7, label='Euler explícito')
    ax.plot([], [], 's', color='#2ecc71', alpha=0.5, label='Euler implícito (semiplano izq.)')
    ax.set_xlabel('Re(hλ)'); ax.set_ylabel('Im(hλ)')
    ax.set_title('Regiones de estabilidad absoluta')
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax = axes[1, 0]
    solvers_st = ['RK45\n(explíc.)', 'RK23\n(explíc.)', 'BDF\n(implíc.)', 'Radau\n(implíc.)', 'LSODA\n(auto)']
    pasos_st = [31500, 15000, 450, 280, 500]
    colores_st = ['red', 'red', 'green', 'green', 'blue']
    bars_st = ax.bar(solvers_st, pasos_st, color=colores_st, alpha=0.75)
    ax.set_ylabel('Nº pasos efectivos (simular 10 s)')
    ax.set_title('Comparativa pasos efectivos por solver\n(sistema stiff S≈10³)')
    ax.set_yscale('log'); ax.grid(True, alpha=0.3, axis='y', which='both')
    for bar, val in zip(bars_st, pasos_st):
        ax.text(bar.get_x()+bar.get_width()/2, val*1.3, f'{val}', ha='center', fontsize=9, fontweight='bold')
    ax = axes[1, 1]; ax.axis('off')
    data_st = [['Solver', 'Orden', 'Estable', 'Uso'],
               ['RK45', '4–5', 'No stiff', 'S < 50'],
               ['BDF', '1–5', 'A-estable', 'S ~ 10³'],
               ['Radau', '5', 'L-estable', 'S > 10⁴'],
               ['LSODA', '1–12', 'Automático', 'Incertidumbre']]
    t_st = ax.table(cellText=data_st[1:], colLabels=data_st[0], cellLoc='center', loc='center',
                    colWidths=[0.22, 0.15, 0.22, 0.41])
    t_st.auto_set_font_size(False); t_st.set_fontsize(9); t_st.scale(1, 1.7)
    ax.set_title('Criterios de selección del solver')
    fig.suptitle('Integración EDOs rígidas: inestabilidad Euler, regiones y comparativa solvers',
                 fontsize=13, fontweight='bold')
    plt.tight_layout()
    _savefig(fig, 'integracion-edos-stiff-analisis')


def _hvdc_vsc_topologia_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Panel 1: configuraciones monopolar vs bipolar
    ax = axes[0, 0]; ax.axis('off')
    for y, label, col in [(0.75, 'Monopolar: +Vdc — tierra', 'blue'),
                          (0.45, 'Bipolar: +Vdc / -Vdc', 'green'),
                          (0.15, 'Simétrica monopolar: ±Vdc sin tierra', 'orange')]:
        ax.annotate('', xy=(0.7, y), xytext=(0.3, y),
                    arrowprops=dict(arrowstyle='->', color=col, lw=2.5))
        ax.text(0.5, y + 0.07, label, ha='center', fontsize=10, color=col, fontweight='bold')
    ax.set_xlim([0, 1]); ax.set_ylim([0, 1])
    ax.set_title('Configuraciones HVDC-VSC')

    # Panel 2: forma de onda MMC con N niveles
    ax = axes[0, 1]
    t = np.linspace(0, 0.02, 2000); f0 = 50
    ref = np.sin(2 * np.pi * f0 * t)
    for N, col, lab in [(4, 'r', 'N=4'), (10, 'g', 'N=10'), (50, 'b', 'N=50')]:
        levels = np.linspace(-1, 1, 2 * N + 1)
        v_out = np.array([levels[np.argmin(np.abs(levels - r))] for r in ref])
        ax.plot(t * 1000, v_out, color=col, lw=1.5, alpha=0.8, label=lab)
    ax.plot(t * 1000, ref, 'k--', lw=1.5, label='Referencia')
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Tensión (pu)')
    ax.set_title('Salida MMC para distintos N'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    # Panel 3: THD vs número de SMs
    ax = axes[1, 0]
    N_arr = np.array([2, 4, 8, 16, 32, 64, 128, 256])
    thd_approx = 100 / N_arr
    ax.loglog(N_arr, thd_approx, 'b-o', lw=2, markersize=6)
    ax.axhline(0.5, color='r', ls='--', label='THD < 0.5 % (objetivo)')
    ax.set_xlabel('Número de SMs por brazo N'); ax.set_ylabel('THD tensión (%)')
    ax.set_title('THD vs número de submódulos'); ax.legend(); ax.grid(True, alpha=0.3)

    # Panel 4: corriente de circulación con/sin CCSC
    ax = axes[1, 1]
    t2 = np.linspace(0, 0.02, 1000)
    i_circ_uncontrolled = 0.15 * np.cos(2 * 2 * np.pi * 50 * t2)
    i_circ_controlled = 0.008 * np.cos(2 * 2 * np.pi * 50 * t2 + 0.2)
    ax.plot(t2 * 1000, i_circ_uncontrolled, 'r-', lw=2, label='i_circ sin CCSC')
    ax.plot(t2 * 1000, i_circ_controlled, 'b-', lw=2, label='i_circ con CCSC')
    ax.axhline(0, color='k', ls='--', alpha=0.5)
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Corriente (pu)')
    ax.set_title('Corriente de circulación: sin/con CCSC'); ax.legend(); ax.grid(True, alpha=0.3)

    fig.suptitle('HVDC-VSC: topología, MMC y corriente de circulación', fontsize=14, fontweight='bold')
    plt.tight_layout()
    _savefig(fig, 'hvdc-vsc-topologia-analisis')


def _hvdc_control_potencia_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Panel 1: estructura de control en cascada
    ax = axes[0, 0]; ax.axis('off')
    blocks = [
        ('P*/Q*\nVdc*/Vac*', 0.10, 0.5, 'lightyellow'),
        ('Outer\nLoop PI', 0.32, 0.5, 'lightblue'),
        ('id*/iq*', 0.54, 0.5, 'lightyellow'),
        ('Inner\nLoop PI', 0.76, 0.5, 'lightblue'),
        ('VSC\nMMC', 0.92, 0.5, 'lightgreen'),
    ]
    for label, x, y, col in blocks:
        ax.add_patch(FancyBboxPatch((x - 0.08, y - 0.12), 0.16, 0.24,
                     boxstyle='round,pad=0.02', facecolor=col, edgecolor='navy'))
        ax.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold')
    for i in range(len(blocks) - 1):
        ax.annotate('', xy=(blocks[i + 1][1] - 0.08, 0.5), xytext=(blocks[i][1] + 0.08, 0.5),
                    arrowprops=dict(arrowstyle='->', color='navy', lw=1.5))
    ax.text(0.5, 0.2, 'BW outer ~50 Hz     BW inner ~1 kHz', ha='center', fontsize=9, color='gray')
    ax.set_xlim([0, 1]); ax.set_ylim([0.05, 0.95]); ax.set_title('Estructura de control VSC-HVDC')

    # Panel 2: respuesta de Vdc ante perturbación de P
    ax = axes[0, 1]
    t = np.linspace(0, 1.5, 1000)
    Vdc_nom = 1.0
    Vdc_ctrl = np.where(t > 0.2,
                        1 - 0.05 * (1 - np.exp(-(t - 0.2) / 0.1)) + 0.02 * np.exp(-(t - 0.2) / 0.3),
                        1.0)
    Vdc_no = np.where(t > 0.2, 1.0 + 0.3 * (1 - np.exp(-(t - 0.2) / 0.3)), 1.0)
    ax.plot(t, Vdc_ctrl, 'b-', lw=2, label='Con control Vdc')
    ax.plot(t, Vdc_no, 'r--', lw=2, label='Sin control Vdc')
    ax.axhline(Vdc_nom, color='k', ls=':', alpha=0.7, label='Nominal')
    ax.axvline(0.2, color='gray', ls=':')
    ax.set_xlabel('Tiempo (s)'); ax.set_ylabel('Vdc (pu)')
    ax.set_title('Respuesta Vdc ante perturbación de P'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    # Panel 3: droop DC — curvas P-Vdc para 3 terminales
    ax = axes[1, 0]
    Vdc_arr = np.linspace(0.9, 1.1, 200)
    Vdc0 = 1.0
    for P0, kd, col, lab in [(-0.8, 5, 'b', 'Terminal 1 (gen)'),
                              (0.3, 3, 'g', 'Terminal 2 (carga)'),
                              (0.5, 4, 'r', 'Terminal 3 (carga)')]:
        P = P0 + kd * (Vdc_arr - Vdc0)
        ax.plot(Vdc_arr, P, color=col, lw=2, label=lab)
    ax.axhline(0, color='k', lw=0.5); ax.axvline(Vdc0, color='k', ls='--', alpha=0.5)
    ax.set_xlabel('Vdc (pu)'); ax.set_ylabel('P (pu)')
    ax.set_title('Droop DC: 3 terminales MTDC'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    # Panel 4: FRT — Vdc durante falta AC en terminal inversor
    ax = axes[1, 1]
    t3 = np.linspace(0, 1, 1000)
    Vac = np.ones(len(t3)); Vac[(t3 > 0.2) & (t3 < 0.4)] = 0.2
    Vdc_frt = np.ones(len(t3))
    mask_fault = (t3 > 0.2) & (t3 < 0.4)
    mask_rec = t3 > 0.4
    Vdc_frt[mask_fault] = 1 + 0.15 * (1 - np.exp(-(t3[mask_fault] - 0.2) / 0.03))
    Vdc_frt[mask_rec] = 1 + 0.15 * np.exp(-(t3[mask_rec] - 0.4) / 0.1)
    P_chopper = np.zeros(len(t3))
    P_chopper[mask_fault] = np.clip((Vdc_frt[mask_fault] - 1.05) * 8, 0, 0.8)
    ax.plot(t3, Vac, 'b-', lw=2, label='Vac (pu)')
    ax.plot(t3, Vdc_frt, 'r-', lw=2, label='Vdc (pu)')
    ax.plot(t3, P_chopper, 'g--', lw=2, label='P_chopper (pu)')
    ax.axhline(1.05, color='orange', ls=':', label='Límite Vdc')
    ax.set_xlabel('Tiempo (s)'); ax.set_ylabel('Amplitud (pu)')
    ax.set_title('FRT: Vdc durante falta AC'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    fig.suptitle('Control HVDC-VSC: cascada, Vdc, droop MTDC y FRT', fontsize=14, fontweight='bold')
    plt.tight_layout()
    _savefig(fig, 'hvdc-control-potencia-analisis')


def _hvdc_cable_dc_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    L = 120e-3; C = 60e-6; R = 3.6; Vdc_kV = 640.0
    Zc = np.sqrt(L / C)
    fres = 1 / (2 * np.pi * np.sqrt(L * C))
    tau = R * C
    W_MJ = 0.5 * C * (Vdc_kV * 1e3) ** 2 / 1e6

    # Panel 1: parámetros del cable (texto)
    ax = axes[0, 0]; ax.axis('off')
    lines = ['Cable 300 km, ±320 kV, 500 MW:',
             f'  R = {R} Ω   L = {L * 1000:.0f} mH   C = {C * 1e6:.0f} µF',
             f'  Zc = √(L/C) = {Zc:.1f} Ω',
             f'  τ_RC = R·C = {tau * 1000:.0f} ms',
             f'  f_res = 1/(2π√LC) = {fres:.1f} Hz',
             f'  Energía almacenada = {W_MJ:.1f} MJ',
             '',
             'Modelo π concentrado:',
             '  dIdc/dt = (V1−V2−R·Idc)/L',
             '  dV1/dt = (I_VSC1−Idc)/(C/2)',
             '  dV2/dt = (Idc−I_VSC2)/(C/2)']
    for i, line in enumerate(lines):
        ax.text(0.05, 0.95 - i * 0.09, line, transform=ax.transAxes,
                fontsize=9, va='top', family='monospace')
    ax.set_title('Parámetros del cable DC')

    # Panel 2: respuesta Vdc ante escalón de carga
    ax = axes[0, 1]
    t = np.linspace(0, 1.5, 1000)
    Vdc_resp = np.where(
        t > 0.3,
        1 - 0.05 * (1 - np.exp(-(t - 0.3) / 0.2)) * (1 + 0.3 * np.cos(2 * np.pi * fres * (t - 0.3)) * np.exp(-(t - 0.3) / 0.15)),
        1.0)
    ax.plot(t, Vdc_resp, 'b-', lw=2, label='Vdc (pu)')
    ax.axvline(0.3, color='gray', ls=':')
    ax.axhline(1.0, color='k', ls='--', alpha=0.5)
    ax.set_xlabel('Tiempo (s)'); ax.set_ylabel('Vdc (pu)')
    ax.set_title('Respuesta Vdc ante escalón de carga'); ax.legend(); ax.grid(True, alpha=0.3)

    # Panel 3: impedancia del cable (resonancia LC)
    ax = axes[1, 0]
    w = np.logspace(0, 4, 1000)
    s = 1j * w
    Z_cable = R + s * L + 1 / (s * C)
    Z_C_only = np.abs(1 / (s * C))
    Z_L_only = np.abs(s * L)
    ax.loglog(w / (2 * np.pi), Z_C_only, 'r--', lw=1.5, label='|1/jωC|')
    ax.loglog(w / (2 * np.pi), Z_L_only, 'b--', lw=1.5, label='|jωL|')
    ax.loglog(w / (2 * np.pi), np.abs(Z_cable), 'g-', lw=2, label='|Z_cable|')
    ax.axvline(fres, color='orange', ls='--', lw=2, label=f'f_res={fres:.0f} Hz')
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Impedancia (Ω)')
    ax.set_title('Resonancia LC del cable DC'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    # Panel 4: corriente de falta DC
    ax = axes[1, 1]
    t_fault = np.linspace(0, 0.05, 500)
    i_fault_A = (Vdc_kV * 1e3) / Zc * np.sin(2 * np.pi * fres * t_fault) * np.exp(-t_fault * R / (2 * L))
    i_rated_A = 500e6 / (Vdc_kV * 1e3)
    ax.plot(t_fault * 1000, i_fault_A / i_rated_A, 'r-', lw=2, label='i_falta (pu)')
    ax.axhline(1, color='b', ls='--', label='Corriente nominal')
    ax.axhline(10, color='orange', ls=':', label='Límite IGBT (~10 pu)')
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Corriente (pu)')
    ax.set_title('Corriente de falta bipolar DC'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    fig.suptitle('Cable DC para HVDC: modelo π, resonancia y falta', fontsize=14, fontweight='bold')
    plt.tight_layout()
    _savefig(fig, 'hvdc-cable-dc-analisis')


def _mmc_modelo_control_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    t = np.linspace(0, 0.04, 4000); f0 = 50; w0 = 2 * np.pi * f0

    # Panel 1: energía de los brazos (variación a w0 y 2w0)
    ax = axes[0, 0]
    W_upper = 1.0 + 0.08 * np.cos(w0 * t) + 0.04 * np.cos(2 * w0 * t)
    W_lower = 1.0 - 0.08 * np.cos(w0 * t) + 0.04 * np.cos(2 * w0 * t)
    ax.plot(t * 1000, W_upper, 'b-', lw=2, label='Brazo superior')
    ax.plot(t * 1000, W_lower, 'r-', lw=2, label='Brazo inferior')
    ax.axhline(1.0, color='k', ls='--', alpha=0.5, label='Energía media')
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Energía normalizada')
    ax.set_title('Energía de los brazos del MMC'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    # Panel 2: corriente de circulación con/sin CCSC
    ax = axes[0, 1]
    i_circ_no = 0.15 * np.cos(2 * w0 * t) + 0.05 * np.cos(4 * w0 * t)
    i_circ_yes = 0.008 * np.cos(2 * w0 * t + 0.2)
    ax.plot(t * 1000, i_circ_no, 'r-', lw=2, label='Sin CCSC')
    ax.plot(t * 1000, i_circ_yes, 'b-', lw=2, label='Con CCSC')
    ax.axhline(0, color='k', ls='--', alpha=0.5)
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('i_circ (pu)')
    ax.set_title('Corriente de circulación MMC'); ax.legend(); ax.grid(True, alpha=0.3)

    # Panel 3: jerarquía de control MMC
    ax = axes[1, 0]; ax.axis('off')
    layers = [
        ('Lazo externo (P/Q/Vdc/Vac)\nBW ~50 Hz', 0.82, 'lightyellow'),
        ('Lazo de corriente AC (id/iq)\nBW ~1 kHz', 0.62, 'lightblue'),
        ('CCSC (i_circ → 0)\nBW ~300 Hz @ 2ω0', 0.42, 'lightgreen'),
        ('Balanceo de condensadores\n(sorting, cada Ts)', 0.22, 'lightsalmon'),
        ('NLM / PS-PWM (modulación)', 0.05, 'lavender'),
    ]
    for label, y, col in layers:
        ax.add_patch(FancyBboxPatch((0.05, y), 0.9, 0.16,
                     boxstyle='round,pad=0.02', facecolor=col, edgecolor='navy'))
        ax.text(0.5, y + 0.08, label, ha='center', va='center', fontsize=9)
    for i in range(len(layers) - 1):
        ax.annotate('', xy=(0.5, layers[i + 1][1] + 0.16),
                    xytext=(0.5, layers[i][1]),
                    arrowprops=dict(arrowstyle='->', color='navy', lw=1.5))
    ax.set_xlim([0, 1]); ax.set_ylim([0, 1]); ax.set_title('Jerarquía de control del MMC')

    # Panel 4: balanceo de tensiones de los SMs
    ax = axes[1, 1]
    np.random.seed(42)
    N_sm = 10
    t_bal = np.linspace(0, 0.1, 500)
    for k in range(N_sm):
        drift = (k - N_sm / 2) * 0.003
        Vc_unbal = 1.0 + drift * t_bal + 0.05 * np.sin(w0 * t_bal + k * 0.5)
        ax.plot(t_bal * 1000, Vc_unbal, 'r-', lw=0.8, alpha=0.4)
    for k in range(N_sm):
        Vc_bal = 1.0 + 0.03 * np.exp(-t_bal / 0.01) * np.sin(w0 * t_bal + k * 0.5)
        ax.plot(t_bal * 1000, Vc_bal, 'b-', lw=0.8, alpha=0.4)
    ax.plot([], [], 'r-', lw=2, label='Sin balanceo')
    ax.plot([], [], 'b-', lw=2, label='Con balanceo')
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('V_C (pu)')
    ax.set_title('Balanceo de tensiones de los SMs'); ax.legend(); ax.grid(True, alpha=0.3)

    fig.suptitle('MMC: energía de brazos, CCSC y jerarquía de control', fontsize=14, fontweight='bold')
    plt.tight_layout()
    _savefig(fig, 'mmc-modelo-control-analisis')


# ===================================================================== #
#  mtdc-proteccion-dc-analisis  (sin decorador @figura)
# ===================================================================== #
def _mtdc_proteccion_dc_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    # Panel 1: droop DC 3 terminales
    ax = axes[0, 0]
    Vdc = np.linspace(0.9, 1.1, 200); Vdc0 = 1.0
    for P0, kd, col, lab in [(-0.8, 8, 'b', 'Terminal 1 (gen, kd=8)'),
                               (0.4, 5, 'r', 'Terminal 2 (carga, kd=5)'),
                               (0.4, 3, 'g', 'Terminal 3 (carga, kd=3)')]:
        P = P0 + kd*(Vdc - Vdc0)
        ax.plot(Vdc, P, color=col, lw=2, label=lab)
    ax.axhline(0, color='k', lw=0.5); ax.axvline(Vdc0, color='k', ls='--', alpha=0.5)
    ax.set_xlabel('Vdc (pu)'); ax.set_ylabel('P (pu)')
    ax.set_title('Droop DC: 3 terminales MTDC'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    # Panel 2: corriente de falta DC
    ax = axes[0, 1]
    t = np.linspace(0, 0.05, 500)
    L = 0.12; C = 60e-6; Vdc_val = 640e3; Zc = np.sqrt(L/C)
    fres = 1/(2*np.pi*np.sqrt(L*C)); I_rated = 500e6/Vdc_val
    i_fault = Vdc_val/Zc * np.sin(2*np.pi*fres*t) * np.exp(-t*0.5/L)
    ax.plot(t*1000, i_fault/I_rated, 'r-', lw=2)
    ax.axhline(1, color='b', ls='--', label='I nominal')
    ax.axhline(10, color='orange', ls=':', label='Límite IGBT (~10pu)')
    ax.axvline(5, color='green', ls='--', label='Tiempo DCCB (5ms)')
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('Corriente (pu)')
    ax.set_title('Corriente de falta bipolar DC'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    # Panel 3: comparativa métodos de protección
    ax = axes[1, 0]; ax.axis('off')
    data = [['Método', 'Tiempo\naislamiento', 'Coste', 'Pérdidas\nnominal', 'Continuidad'],
            ['DCCB híbrido', '<5 ms', 'Alto', 'Mínimo', 'Completa'],
            ['MMC-FB', '<2 ms', 'Muy alto', 'Doble', 'Completa'],
            ['Handshaking', '200-500 ms', 'Bajo', 'Normal', 'Interrupción'],
            ['Bus splitting', '50-100 ms', 'Medio', 'Normal', 'Parcial']]
    t_obj = ax.table(cellText=data[1:], colLabels=data[0], cellLoc='center', loc='center',
                     colWidths=[0.22, 0.18, 0.15, 0.2, 0.2])
    t_obj.auto_set_font_size(False); t_obj.set_fontsize(9); t_obj.scale(1, 1.6)
    ax.set_title('Comparativa métodos de protección DC')
    # Panel 4: topología MTDC radial vs mallada
    ax = axes[1, 1]; ax.axis('off')
    nodes_r = [('Gen 1', 0.1, 0.75), ('Hub DC', 0.35, 0.75),
               ('Carga 1', 0.6, 0.9), ('Carga 2', 0.6, 0.6)]
    for label, x, y in nodes_r:
        col = 'lightblue' if 'Hub' in label else ('lightgreen' if 'Gen' in label else 'lightsalmon')
        ax.add_patch(mpatches.FancyBboxPatch((x-0.07, y-0.06), 0.14, 0.12,
                                             boxstyle='round,pad=0.01', facecolor=col, edgecolor='navy'))
        ax.text(x, y, label, ha='center', va='center', fontsize=8)
    for (l1, x1, y1), (l2, x2, y2) in [(nodes_r[0], nodes_r[1]),
                                          (nodes_r[1], nodes_r[2]),
                                          (nodes_r[1], nodes_r[3])]:
        ax.plot([x1+0.07, x2-0.07], [y1, y2], 'navy', lw=1.5)
    ax.text(0.35, 0.95, 'Radial', ha='center', fontsize=10, fontweight='bold', color='navy')
    nodes_m = [('Gen 1', 0.1, 0.3), ('Gen 2', 0.3, 0.15),
               ('Carga 1', 0.6, 0.3), ('Carga 2', 0.45, 0.45)]
    for label, x, y in nodes_m:
        col = 'lightgreen' if 'Gen' in label else 'lightsalmon'
        ax.add_patch(mpatches.FancyBboxPatch((x-0.07, y-0.06), 0.14, 0.12,
                                             boxstyle='round,pad=0.01', facecolor=col, edgecolor='darkred'))
        ax.text(x, y, label, ha='center', va='center', fontsize=8)
    for i in range(len(nodes_m)):
        for j in range(i+1, len(nodes_m)):
            x1, y1 = nodes_m[i][1], nodes_m[i][2]
            x2, y2 = nodes_m[j][1], nodes_m[j][2]
            ax.plot([x1, x2], [y1, y2], 'darkred', lw=1, alpha=0.6)
    ax.text(0.35, 0.52, 'Mallada', ha='center', fontsize=10, fontweight='bold', color='darkred')
    ax.set_xlim([0, 0.75]); ax.set_ylim([0.05, 1.0]); ax.set_title('Topologías MTDC')
    fig.suptitle('MTDC y protección DC: droop, faltas y métodos de protección',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    _savefig(fig, "mtdc-proteccion-dc-analisis")


# ===================================================================== #
#  python-control-scipy-analisis  (sin decorador @figura)
# ===================================================================== #
def _python_control_scipy_analisis():
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import signal
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    num = [100]; den = [1, 10, 100]
    sys_tf = signal.lti(num, den)
    # Panel 1: Bode
    ax = axes[0, 0]; ax2 = ax.twinx()
    w, mag, phase = signal.bode(sys_tf, n=500)
    ax.semilogx(w/(2*np.pi), mag, 'b-', lw=2, label='Ganancia')
    ax2.semilogx(w/(2*np.pi), phase, 'r--', lw=2, label='Fase')
    ax.axhline(-3, color='gray', ls=':', alpha=0.7)
    ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Ganancia (dB)', color='b')
    ax2.set_ylabel('Fase (°)', color='r'); ax.set_title('Bode con scipy.signal')
    ax.grid(True, alpha=0.3)
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, fontsize=8)
    # Panel 2: respuesta al escalón con anotaciones
    ax = axes[0, 1]
    t, y = signal.step(sys_tf)
    ax.plot(t, y, 'b-', lw=2)
    Mp_idx = np.argmax(y); Mp = (y[Mp_idx]-1)*100
    ts_idx = np.where(np.abs(y-1) < 0.02)[0]
    ts_val = t[ts_idx[0]] if len(ts_idx) > 0 else t[-1]
    ax.axhline(1, color='k', ls='--', alpha=0.5)
    ax.axhline(1.02, color='gray', ls=':', alpha=0.5)
    ax.axhline(0.98, color='gray', ls=':', alpha=0.5)
    ax.annotate(f'Mp={Mp:.1f}%', xy=(t[Mp_idx], y[Mp_idx]),
                xytext=(t[Mp_idx]+0.05, y[Mp_idx]+0.02), fontsize=9,
                arrowprops=dict(arrowstyle='->', color='red'), color='red')
    ax.axvline(ts_val, color='green', ls='--', label=f'ts={ts_val:.3f}s (2%)')
    ax.set_xlabel('Tiempo (s)'); ax.set_ylabel('y(t)')
    ax.set_title('Respuesta escalón con anotaciones'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    # Panel 3: lugar de raíces numérico
    ax = axes[1, 0]
    K_arr = np.linspace(0, 500, 200)
    poles_all = []
    for K in K_arr:
        r = np.roots([1, 10, 100+K])
        poles_all.append(r)
    poles_all = np.array(poles_all)
    ax.scatter(np.real(poles_all[:, 0]), np.imag(poles_all[:, 0]), s=2, c='blue', alpha=0.5)
    ax.scatter(np.real(poles_all[:, 1]), np.imag(poles_all[:, 1]), s=2, c='blue', alpha=0.5)
    ax.axvline(0, color='k', lw=1); ax.axhline(0, color='k', lw=1)
    p0 = np.roots([1, 10, 100])
    ax.scatter(np.real(p0), np.imag(p0), s=100, c='red', marker='x', zorder=5, label='K=0')
    ax.set_xlabel('Re(s)'); ax.set_ylabel('Im(s)'); ax.set_title('Lugar de raíces (K variable)')
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    # Panel 4: continuo vs discreto
    ax = axes[1, 1]
    t_cont = np.linspace(0, 0.3, 1000)
    _, y_cont = signal.step(sys_tf, T=t_cont)
    ax.plot(t_cont*1000, y_cont, 'b-', lw=2, label='Continuo')
    for Ts_d, col, lab in [(2e-3, 'r', 'Ts=2ms (Tustin)'), (5e-3, 'g', 'Ts=5ms (Tustin)')]:
        sys_d = signal.lti(num, den).to_discrete(Ts_d, method='bilinear')
        t_d2 = np.arange(0, 0.3, Ts_d)
        u_d2 = np.ones(len(t_d2))
        t_out_d2, y_d2 = signal.dlsim(sys_d, u_d2, t=t_d2)
        ax.step(t_out_d2.flatten()*1000, y_d2.flatten(), where='post', color=col, lw=1.5, label=lab)
    ax.set_xlabel('Tiempo (ms)'); ax.set_ylabel('y(t)')
    ax.set_title('Continuo vs discreto (Tustin)'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    fig.suptitle('Python para control: scipy.signal y análisis LTI', fontsize=14, fontweight='bold')
    plt.tight_layout()
    _savefig(fig, "python-control-scipy-analisis")


if __name__ == "__main__":
    main()
