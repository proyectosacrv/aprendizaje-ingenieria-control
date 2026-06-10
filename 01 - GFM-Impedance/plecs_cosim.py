"""Co-simulacion Python <-> PLECS via XML-RPC: mide la impedancia del modelo
CONMUTADO y la compara con la analitica (modelo promediado) para cerrar la Fase 4.

Patron: Python orquesta (fija parametros, lanza simulaciones, demodula y compara);
PLECS ejecuta el modelo conmutado (IGBTs + PWM).

REQUISITOS EN PLECS
  - Modelo gfm_switched.plecs construido segun PLECS_GUIA.md, con el control del
    bloque C-Script (plecs_control_gfm.c).
  - Servidor XML-RPC activo: Preferences > XML-RPC Interface > Enable (puerto 1080).
  - El modelo expone, en sus 'Model initialization commands', las variables:
        f_pert, amp_pert, axis_d   (fuente de perturbacion en el PCC)
        Lg, Rg                     (red Thevenin, para el barrido de SCR)
    y deja en la estructura de salida (orden de las senales del bloque 'Outport' o
    'To File') las series:  [t]  vpcc_d  vpcc_q  ig_d  ig_q   ( + i_L1 para faltas ).

Sin PLECS este archivo no simula, pero el codigo de demodulacion y comparacion es el
mismo (correcto) que se usa en inject.py / main_phase4.py.
    python plecs_cosim.py        # imprime instrucciones si PLECS no esta accesible
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import xmlrpc.client
from params import SystemParams
from impedance import build_linear, impedance
from inject import _phasor          # reutilizamos la demodulacion por correlacion

PLECS_URL = "http://localhost:1080/RPC2"
MODEL = "gfm_switched"               # nombre del .plecs (sin extension)
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), MODEL + ".plecs")


# --------------------------------------------------------------------- #
def connect():
    """Conecta con PLECS y carga el modelo. Lanza si no esta accesible."""
    server = xmlrpc.client.ServerProxy(PLECS_URL)
    server.plecs.load(MODEL_PATH)
    return server


def _simulate(server, model_vars):
    """Lanza una simulacion con las variables dadas; devuelve (t, Y) con
    Y de forma (n_senales, n_tiempo)."""
    opts = {"ModelVars": {k: float(v) for k, v in model_vars.items()}}
    out = server.plecs.simulate(MODEL, opts)
    t = np.asarray(out["Time"], dtype=float)
    Y = np.asarray(out["Values"], dtype=float)
    return t, Y


# --------------------------------------------------------------------- #
def measure_point(server, fp, amp, axis, settle_frac=0.6):
    """Una inyeccion a frecuencia fp en eje 'd' o 'q' sobre el modelo conmutado.
    Demodula la ventana final (regimen permanente) y devuelve (Vd,Vq,Id,Iq)."""
    t, Y = _simulate(server, {"f_pert": fp, "amp_pert": amp,
                              "axis_d": 1.0 if axis == "d" else 0.0})
    vpcc_d, vpcc_q, ig_d, ig_q = Y[0], Y[1], Y[2], Y[3]
    # ventana de medicion: ultimo tramo, recortado a un numero entero de periodos
    t0 = t[0] + settle_frac * (t[-1] - t[0])
    m = t >= t0
    tm = t[m]
    Tp = 1.0 / fp
    n_per = int((tm[-1] - tm[0]) / Tp)        # periodos enteros
    tend = tm[0] + n_per * Tp
    w = tm <= tend
    tm = tm[w]
    return (_phasor(tm, vpcc_d[m][w], fp), _phasor(tm, vpcc_q[m][w], fp),
            _phasor(tm, ig_d[m][w], fp),   _phasor(tm, ig_q[m][w], fp))


def measure_Z(server, freqs, amp=2.0):
    """Barrido MIMO 2x2: dos inyecciones (d y q) por frecuencia -> Z (N,2,2)."""
    Z = np.zeros((len(freqs), 2, 2), dtype=complex)
    for k, fp in enumerate(freqs):
        Vd1, Vq1, Id1, Iq1 = measure_point(server, fp, amp, "d")
        Vd2, Vq2, Id2, Iq2 = measure_point(server, fp, amp, "q")
        V = np.array([[Vd1, Vd2], [Vq1, Vq2]])
        I = np.array([[Id1, Id2], [Iq1, Iq2]])
        G = I @ np.linalg.inv(V)
        Z[k] = np.linalg.inv(-G)              # Z = (-G)^-1 = Y^-1
        print(f"  {fp:7.1f} Hz  |Zdd|={abs(Z[k,0,0]):7.3f}  |Zqq|={abs(Z[k,1,1]):7.3f}")
    return Z


def compare_with_analytic(freqs, Z_plecs, out_csv="datos/impedancia_plecs_vs_analitica.csv"):
    """Compara Z medida en PLECS con la analitica y guarda CSV + error."""
    p = SystemParams()
    A, B, C, D, _ = build_linear(p)
    Za = impedance(A, B, C, D, freqs)
    err = np.array([100*abs(Z_plecs[k,0,0]-Za[k,0,0])/abs(Za[k,0,0]) for k in range(len(freqs))])
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    np.savetxt(out_csv,
               np.column_stack([freqs,
                                np.abs(Za[:,0,0]), np.abs(Z_plecs[:,0,0]),
                                np.abs(Za[:,1,1]), np.abs(Z_plecs[:,1,1]), err]),
               delimiter=",",
               header="f_Hz,absZdd_analitica,absZdd_plecs,absZqq_analitica,absZqq_plecs,err_pct",
               comments="", fmt="%.6g")
    print(f"\nError medio |Zdd| (PLECS vs analitica): {err.mean():.2f}%  (max {err.max():.2f}%)")
    print(f"CSV: {out_csv}")
    return err


def sweep_scr(server, scr_list, xr=5.0):
    """Barrido de SCR sobre el modelo conmutado: pico de i_L1 (p.ej. bajo falta)."""
    p = SystemParams()
    res = {}
    for scr in scr_list:
        Zg = p.Vll**2 / (scr * p.Sn)
        Rg = Zg / np.sqrt(1 + xr**2)
        Lg = Rg * xr / p.w0
        t, Y = _simulate(server, {"Lg": Lg, "Rg": Rg})
        iL1_peak = float(np.max(np.abs(Y[4])))   # ajustar indice de i_L1 a tu modelo
        res[scr] = iL1_peak
        print(f"  SCR={scr:5.2f}  pico i_L1 = {iL1_peak:.1f} A")
    return res


# --------------------------------------------------------------------- #
if __name__ == "__main__":
    freqs = np.array([2, 3.3, 5, 8, 13, 20, 35, 60, 100, 180, 320, 500.0])
    try:
        srv = connect()
        print("PLECS conectado. Midiendo impedancia en el modelo conmutado...")
        Zp = measure_Z(srv, freqs, amp=2.0)
        compare_with_analytic(freqs, Zp)
    except Exception as e:
        print("PLECS no accesible (esto es normal si no esta abierto):")
        print(f"  {type(e).__name__}: {e}")
        print("\nPara usarlo:")
        print("  1) Construye gfm_switched.plecs siguiendo PLECS_GUIA.md")
        print("     (control: pega plecs_control_gfm.c en un bloque C-Script).")
        print("  2) Activa el servidor XML-RPC en PLECS (puerto 1080).")
        print("  3) Vuelve a ejecutar: python plecs_cosim.py")
