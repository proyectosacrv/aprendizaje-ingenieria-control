"""Diagnostico: que lazo causa la inestabilidad del modo de ~6 Hz."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from params import SystemParams
from model import GFMInverter

def max_re(p):
    gfm = GFMInverter(p)
    u = np.array([p.V0, 0.0])
    x, info = gfm.equilibrium(u)
    A, *_ = gfm.linearize(x, u)
    ev = np.linalg.eigvals(A)
    return ev.real.max(), info["residual"]

cases = {
    "baseline":            SystemParams(),
    "sin droop Q (nq=0)":  SystemParams(droop_q=0.0),
    "droop P /2":          SystemParams(droop_p=0.005),
    "filtro pot 5 Hz":     SystemParams(f_pow=5.0),
    "filtro pot 30 Hz":    SystemParams(f_pow=30.0),
    "lazo V x3":           SystemParams(f_cv=180.0),
}
for name, p in cases.items():
    mr, res = max_re(p)
    flag = "ESTABLE  " if mr < 0 else "INESTABLE"
    print(f"  {name:22s} -> max Re = {mr:>9.2f}  [{flag}]  (res {res:.1e})")
