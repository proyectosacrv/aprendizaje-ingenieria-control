---
titulo: "Python para control: scipy.signal y control"
slug: python-control-scipy
categoria: programacion
tipo: metodo
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [analizar sistemas LTI con scipy.signal, diseñar controladores con python-control, discretizar y simular en tiempo discreto]
tags: [python, scipy, control, bode, nyquist, step-response, lti, state-space, pid, transfer-function]
fecha_creacion: 2026-07-08
fecha_actualizacion: 2026-07-08
relacionados: [respuesta-frecuencia-ss, linealizacion-numerica, discretizacion-controladores, barrido-parametrico]
referencias:
  - "scipy.signal documentation: https://docs.scipy.org/doc/scipy/reference/signal.html"
  - "python-control documentation: https://python-control.readthedocs.io"
---

## Definición

`scipy.signal` y `python-control` son las dos librerías principales para análisis y diseño de sistemas de control en Python. La primera cubre análisis de sistemas LTI (Bode, respuesta temporal, discretización); la segunda equivale a la MATLAB Control Toolbox (LQR, H-infinito, lugar de raíces, márgenes). Ambas son compatibles entre sí y con NumPy/Matplotlib.

## 1 — Librerías principales

**`scipy.signal`** — incluida en SciPy estándar (sin instalación adicional). Cubre:
- Definición de sistemas LTI: `TransferFunction`, `StateSpace`, `ZerosPolesGain`.
- Análisis en frecuencia: `bode()`, `freqresp()`.
- Respuesta temporal: `step()`, `impulse()`, `lsim()`.
- Discretización: `cont2discrete()` o método `.to_discrete()`.
- Procesado de señales: filtros, FFT, espectros.

**`python-control`** — equivalente a MATLAB Control Toolbox. Instalación: `pip install control`. Cubre:
- Definición de sistemas: `control.tf()`, `control.ss()`.
- Diseño: `control.lqr()`, `control.h2syn()`, `control.hinfsyn()`.
- Análisis: `control.margin()`, `control.damp()`, `control.rlocus()`.
- Sistemas MIMO: valores singulares, normas \( H_2 \) y \( H_\infty \).

**`slycot`** — solver numérico para ecuaciones de Riccati y balanceo de realizaciones. Requerido por `python-control` para LQR/LQE en sistemas de orden alto. Instalación: `pip install slycot` (requiere compilador C).

**Cuándo usar cada una:**
- `scipy.signal`: análisis rápido SISO, simulación, respuesta al escalón, Bode básico.
- `python-control`: diseño LQR, márgenes robustos MIMO, lugar de raíces con interactividad.
- Ambas juntas: `scipy.signal` para las funciones de transferencia, `python-control` para el diseño del controlador.

<div class="cfig"><img src="figuras/python-control-scipy-analisis.png" alt="Python para control: Bode, escalón, lugar de raíces y discretización"><div class="cap">Panel superior izquierdo: diagrama de Bode con doble eje (ganancia dB / fase °) calculado con scipy.signal.bode. Superior derecho: respuesta al escalón con anotaciones automáticas de Mp y ts. Inferior izquierdo: lugar de raíces numérico variando la ganancia K. Inferior derecho: comparativa continuo vs discreto con método Tustin para dos períodos de muestreo.</div></div>

## 2 — Sistemas LTI: definición y conversión

**Función de transferencia.** `scipy.signal.lti(num, den)` acepta los coeficientes en orden descendente de potencia de \( s \):

```python
from scipy import signal
import numpy as np

# G(s) = 100 / (s^2 + 10s + 100)
num = [100]
den = [1, 10, 100]
sys_tf = signal.lti(num, den)

# Polos y ceros
poles = sys_tf.poles
zeros = sys_tf.zeros
# Frecuencia natural y amortiguamiento (para par complejo conjugado)
wn = np.abs(poles[0])           # rad/s
zeta = -poles[0].real / wn      # amortiguamiento
print(f"wn = {wn:.1f} rad/s, zeta = {zeta:.3f}")
```

**Conversión a espacio de estados:**

```python
# Conversión automática FdT -> espacio de estados
sys_ss = sys_tf.to_ss()
print("A =\n", sys_ss.A)
print("B =\n", sys_ss.B)
print("C =\n", sys_ss.C)

# O definir directamente en espacio de estados
A = np.array([[-2, 1], [-5, -3]])
B = np.array([[0], [1]])
C = np.array([[1, 0]])
D = np.array([[0]])
sys_ss2 = signal.StateSpaceContinuous(A, B, C, D)
```

**Con python-control (sintaxis MATLAB-like):**

```python
import control

# Función de transferencia
G = control.tf([100], [1, 10, 100])

# Amortiguamiento y frecuencia natural de todos los polos
wn_arr, zeta_arr, poles_ctrl = control.damp(G, display=True)

# Conversión a espacio de estados
G_ss = control.ss(G)
```

**Aritmética de sistemas.** Las operaciones de sistemas (serie, paralelo, lazo cerrado) se hacen directamente con operadores Python:

```python
G = control.tf([100], [1, 10, 100])
C_pi = control.tf([10, 50], [1, 0])   # PI: Kp=10, Ki=50

L = G * C_pi                           # lazo abierto (serie)
T = control.feedback(L, 1)             # lazo cerrado (realimentación unitaria)
S = 1 - T                              # función de sensibilidad
```

## 3 — Análisis en frecuencia: Bode y márgenes

**Diagrama de Bode con `scipy.signal.bode`:**

```python
import matplotlib.pyplot as plt

# Bode del sistema
w, mag, phase = signal.bode(sys_tf, n=500)
# w en rad/s, mag en dB, phase en grados

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
ax1.semilogx(w / (2*np.pi), mag, 'b-', lw=2)
ax1.set_ylabel('Ganancia (dB)'); ax1.grid(True, which='both', alpha=0.3)
ax1.axhline(-3, color='gray', ls=':', label='-3 dB')

ax2.semilogx(w / (2*np.pi), phase, 'r-', lw=2)
ax2.set_ylabel('Fase (°)'); ax2.set_xlabel('Frecuencia (Hz)')
ax2.axhline(-180, color='gray', ls=':')
ax2.grid(True, which='both', alpha=0.3)
plt.tight_layout()
```

**Márgenes de estabilidad con `scipy.signal`:**

```python
# Calcular margen de fase manualmente desde el Bode del lazo abierto
w_arr = np.logspace(0, 4, 2000)

# Lazo abierto: PI * G(s)
C_num = np.polymul([10, 100], [1])      # PI: Kp*s + Ki en numerador
C_den = np.polymul([1, 0], [1])         # s en denominador
L_num = np.polymul(C_num, num)
L_den = np.polymul(C_den, den)
L_sys = signal.lti(L_num, L_den)

w_b, mag_b, phase_b = signal.bode(L_sys, w=w_arr)

# Margen de fase: fase en la frecuencia de cruce de ganancia (mag=0 dB)
wc_idx = np.argmin(np.abs(mag_b))
PM = 180 + phase_b[wc_idx]
print(f"Frecuencia de cruce: {w_b[wc_idx]/(2*np.pi):.1f} Hz")
print(f"Margen de fase: {PM:.1f}°")

# Margen de ganancia: 1/|L(jw)| en la frecuencia de cruce de fase (-180°)
wpc_idx = np.argmin(np.abs(phase_b + 180))
GM_dB = -mag_b[wpc_idx]
print(f"Margen de ganancia: {GM_dB:.1f} dB")
```

**Con python-control (más directo):**

```python
G_ctrl = control.tf([100], [1, 10, 100])
C_ctrl = control.tf([10, 100], [1, 0])
L_ctrl = G_ctrl * C_ctrl

gm, pm, wpc, wgc = control.margin(L_ctrl)
print(f"GM = {20*np.log10(gm):.1f} dB  (en {wpc/(2*np.pi):.1f} Hz)")
print(f"PM = {pm:.1f}°  (en {wgc/(2*np.pi):.1f} Hz)")
```

**Diagrama de Nyquist:**

```python
# Con python-control
control.nyquist_plot(L_ctrl)
plt.title('Nyquist del lazo abierto')
```

## 4 — Respuesta temporal: escalón, impulso y simulación

**Respuesta al escalón y extracción de métricas:**

```python
# Respuesta al escalón del lazo cerrado
C_pi = signal.lti([10, 100], [1, 0])
# Lazo cerrado: T(s) = L(s)/(1+L(s))
L_num2 = np.polymul([10, 100], [100])
L_den2 = np.polymul([1, 0], [1, 10, 100])
T_num = L_num2
T_den = np.polyadd(L_den2, L_num2)
T_sys = signal.lti(T_num, T_den)

t, y = signal.step(T_sys)

# Métricas automáticas
y_ss = y[-1]                              # valor en estado estacionario
Mp = (np.max(y) - y_ss) / y_ss * 100     # sobreoscilación (%)
idx_Mp = np.argmax(y)
tp = t[idx_Mp]                            # tiempo al pico

# Tiempo de asentamiento al 2%
band = 0.02 * y_ss
settled = np.where(np.abs(y - y_ss) < band)[0]
ts = t[settled[0]] if len(settled) > 0 else t[-1]

print(f"Valor en estado estacionario: {y_ss:.4f}")
print(f"Sobreoscilación: {Mp:.1f}%")
print(f"Tiempo al pico: {tp*1000:.1f} ms")
print(f"Tiempo de asentamiento (2%): {ts*1000:.1f} ms")
```

**Simulación con entrada arbitraria (`lsim`):**

```python
# Señal de entrada arbitraria: escalón + rampa
t_sim = np.linspace(0, 0.5, 50000)
u_step = np.ones(len(t_sim))
u_ramp = t_sim * 10                   # rampa de pendiente 10

# lsim devuelve (t_out, y_out, x_out)
t_out, y_out, x_out = signal.lsim(sys_tf, u_step, t_sim)

# Señal sinusoidal a la frecuencia de resonancia
w_res = np.sqrt(100)                  # wn del sistema de ejemplo
u_sin = np.sin(w_res * t_sim)
_, y_sin, _ = signal.lsim(sys_tf, u_sin, t_sim)
```

**Respuesta al impulso:**

```python
t_imp, y_imp = signal.impulse(sys_tf)
plt.plot(t_imp*1000, y_imp)
plt.xlabel('Tiempo (ms)'); plt.ylabel('Respuesta al impulso')
plt.title('Respuesta impulsional'); plt.grid(True)
```

**Espacio de estados con condiciones iniciales:**

```python
# lsim acepta el estado inicial X0
A_ex = np.array([[-2, 1], [-5, -3]])
B_ex = np.array([[0], [1]])
C_ex = np.array([[1, 0]])
D_ex = np.array([[0]])
sys_ss3 = signal.StateSpaceContinuous(A_ex, B_ex, C_ex, D_ex)

x0 = [0.5, -0.2]                      # condiciones iniciales no nulas
u_ex = np.zeros(len(t_sim))           # sin entrada (respuesta libre)
_, y_libre, x_libre = signal.lsim(sys_ss3, u_ex, t_sim, X0=x0)
```

## 5 — Diseño de controladores: LQR y sintonía PI

**LQR con python-control:**

```python
import control
import numpy as np

# Planta: doble integrador con amortiguamiento
A = np.array([[0, 1], [-5, -2]])
B = np.array([[0], [1]])
C = np.array([[1, 0]])
D = np.array([[0]])
sys_plant = control.ss(A, B, C, D)

# Pesos: Q penaliza el error de estado, R penaliza el esfuerzo de control
Q = np.diag([10, 1])     # penalización fuerte en posición, débil en velocidad
R = np.array([[1]])       # penalización del esfuerzo de control

# LQR: minimiza int_0^inf (x'Qx + u'Ru) dt
K_lqr, S_riccati, poles_cl = control.lqr(sys_plant, Q, R)
print(f"Ganancia LQR: K = {K_lqr}")
print(f"Polos lazo cerrado: {poles_cl}")

# Sistema en lazo cerrado: u = -K*x
A_cl = A - B @ K_lqr
sys_cl = control.ss(A_cl, B, C, D)

# Verificar estabilidad y márgenes
print("¿Estable?", all(np.real(np.linalg.eigvals(A_cl)) < 0))
```

**Sintonía PI por IMC (Internal Model Control):**

El método IMC para una planta de primer orden \( G(s) = K_p / (\tau s + 1) \) da directamente las ganancias del PI en función del parámetro de diseño \( \lambda \) (velocidad deseada del lazo cerrado):

$$ K_p^{PI} = \frac{\tau}{K_{plant} \lambda}, \quad T_i = \tau, \quad K_i = \frac{K_p^{PI}}{T_i} $$

```python
# Parámetros de la planta (lazo de corriente de un VSC)
K_plant = 1 / 0.005      # 1/R donde R = 5 mΩ... ajustado a ganancias razonables
tau_plant = 0.005 / 1.0  # L/R con L=5 mH, R=1 Ω -> tau=5 ms
K_plant_norm = 1.0        # ganancia DC normalizada
tau_plant = 5e-3          # constante de tiempo [s]

lambda_imc = 1e-3         # 1 ms -> BW lazo cerrado ~160 Hz
Kp_pi = tau_plant / (K_plant_norm * lambda_imc)
Ti_pi = tau_plant
Ki_pi = Kp_pi / Ti_pi
print(f"PI por IMC: Kp = {Kp_pi:.2f}, Ti = {Ti_pi*1000:.1f} ms, Ki = {Ki_pi:.1f}")

# Verificar márgenes con python-control
G = control.tf([K_plant_norm], [tau_plant, 1])
C_pi_ctrl = control.tf([Kp_pi, Ki_pi], [1, 0])
L_ctrl = G * C_pi_ctrl
gm, pm, wpc, wgc = control.margin(L_ctrl)
print(f"GM = {20*np.log10(gm):.1f} dB,  PM = {pm:.1f}°,  BW = {wgc/(2*np.pi):.0f} Hz")
```

**Criterio de Ziegler-Nichols (sintonía clásica):**

```python
# A partir del Bode del lazo abierto con solo proporcional
# Encontrar Ku (ganancia de oscilación) y Tu (periodo de oscilación)
G_plant = signal.lti([1], [tau_plant, 1])
w_test = np.logspace(1, 5, 5000)
_, mag_plant, phase_plant = signal.bode(G_plant, w=w_test)

# Frecuencia donde la fase = -180° (con proporcional puro)
pc_idx = np.argmin(np.abs(phase_plant + 180))
if pc_idx < len(w_test) - 1:
    Ku = 1 / (10**(mag_plant[pc_idx]/20))   # ganancia de oscilación
    Tu = 2*np.pi / w_test[pc_idx]            # periodo de oscilación
    Kp_zn = 0.6 * Ku
    Ti_zn = Tu / 2
    print(f"Ziegler-Nichols: Kp = {Kp_zn:.2f}, Ti = {Ti_zn*1000:.1f} ms")
```

## 6 — Discretización y simulación de sistemas digitales

**Discretización con `scipy.signal`:**

```python
from scipy import signal
import numpy as np

num = [100]; den = [1, 10, 100]
sys_cont = signal.lti(num, den)

Ts = 1e-4    # 100 µs (frecuencia de muestreo 10 kHz, típica en VSC)

# Método de Tustin (bilineal): conserva la respuesta en frecuencia hasta Nyquist
sys_d_tustin = sys_cont.to_discrete(Ts, method='bilinear')
print(f"Polos discretos (Tustin): {sys_d_tustin.poles}")

# Método ZOH: retención de orden cero (respuesta exacta al escalón)
sys_d_zoh = sys_cont.to_discrete(Ts, method='zoh')
print(f"Polos discretos (ZOH): {sys_d_zoh.poles}")

# Verificar que los polos estén dentro del círculo unitario (estabilidad)
print(f"Estable (Tustin): {all(np.abs(sys_d_tustin.poles) < 1)}")
```

**Simulación en tiempo discreto:**

```python
# Respuesta al escalón del sistema discreto
t_d = np.arange(0, 0.1, Ts)
u_d = np.ones(len(t_d))
t_out_d, y_out_d = signal.dlsim(sys_d_tustin, u_d, t=t_d)

# Comparativa continuo vs discreto
t_cont_ref = np.linspace(0, 0.1, 10000)
_, y_cont_ref = signal.step(sys_cont, T=t_cont_ref)

import matplotlib.pyplot as plt
plt.plot(t_cont_ref*1000, y_cont_ref, 'b-', lw=2, label='Continuo')
plt.step(t_out_d*1000, y_out_d.flatten(), where='post',
         color='r', lw=1.5, label=f'Discreto Tustin (Ts={Ts*1e6:.0f}µs)')
plt.xlabel('Tiempo (ms)'); plt.ylabel('Respuesta'); plt.legend(); plt.grid(True)
```

**Implementación de PI discreto para DSP/microcontrolador.**
La discretización Tustin del PI continuo \( C(s) = K_p + K_i/s \) da la ecuación en diferencias:

$$ u[k] = u[k-1] + b_0\, e[k] + b_1\, e[k-1] $$

con \( b_0 = K_p(1 + T_s/T_i) \) y \( b_1 = -K_p \):

```python
# Coeficientes del PI discreto (método Tustin)
Kp_val = 5.0
Ti_val = 5e-3   # = tau_plant (por IMC)
Ts_ctrl = 1e-4  # periodo de muestreo del controlador

b0 = Kp_val * (1 + Ts_ctrl / Ti_val)
b1 = -Kp_val
print(f"PI discreto: b0 = {b0:.4f}, b1 = {b1:.4f}")

# Simulación directa de la ecuación en diferencias (como en un DSP)
N_sim = 5000
e = np.zeros(N_sim); u = np.zeros(N_sim)
y_plant = np.zeros(N_sim)
ref = 1.0

# Planta discretizada: respuesta al escalón con lazo de corriente
A_p = np.exp(-Ts_ctrl / Ti_val)    # polo discreto de la planta de 1er orden
B_p = (1 - A_p) * K_plant_norm    # ganancia discreta

for k in range(1, N_sim):
    e[k] = ref - y_plant[k-1]
    u[k] = u[k-1] + b0*e[k] + b1*e[k-1]
    u_sat = np.clip(u[k], -10, 10)  # saturación del modulador
    y_plant[k] = A_p * y_plant[k-1] + B_p * u_sat

t_dsim = np.arange(N_sim) * Ts_ctrl
print(f"Error en estado estacionario: {e[-1]:.6f} (debe ser ~0)")
```

**Verificación de estabilidad con criterio de Jury (para sistemas discretos).**
Para un sistema de segundo orden discreto \( 1 + a_1 z^{-1} + a_2 z^{-2} = 0 \), las condiciones de Jury garantizan que todos los polos están dentro del círculo unitario:

$$ |a_2| < 1, \quad |a_1| < 1 + a_2, \quad \text{y} \quad 1 - a_1 + a_2 > 0 $$

```python
# Obtener denominador del sistema discreto
den_d = sys_d_tustin.den
# Normalizar: den_d[0]=1
a1 = den_d[1]; a2 = den_d[2]
jury_ok = (abs(a2) < 1) and (abs(a1) < 1 + a2) and (1 - a1 + a2 > 0)
print(f"Criterio de Jury satisfecho: {jury_ok}")
```
