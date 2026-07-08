---
titulo: Respuesta en frecuencia de un sistema en espacio de estados
slug: respuesta-frecuencia-ss
categoria: programacion
tipo: metodo
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [calcular Y(s)/Z(s) y Bode desde A,B,C,D]
tags: [espacio-estados, bode, transferencia, frecuencia, numpy]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [linealizacion-numerica, impedancia-salida-estabilidad, medicion-impedancia-inyeccion]
referencias:
  - "Skogestad, Postlethwaite, Multivariable Feedback Control, Wiley 2005"
---

## Definición
Cálculo de la matriz de transferencia \( \mathbf{G}(s)=\mathbf{C}(s\mathbf{I}-\mathbf{A})^{-1}\mathbf{B}+\mathbf{D} \)
evaluada en \( s=j\omega \), a partir del modelo en espacio de estados. Base para Bode,
impedancia y análisis de estabilidad.

## Fundamento teórico
Para cada frecuencia se resuelve un sistema lineal en vez de invertir explícitamente
\( (j\omega\mathbf{I}-\mathbf{A}) \) (más estable numéricamente con `np.linalg.solve`). En MIMO,
\( \mathbf{G}(j\omega) \) es una matriz; la admitancia de salida del convertidor es \( Y=-G \) y
la impedancia \( Z=Y^{-1} \).

<div class="cfig"><img src="figuras/respuesta-frecuencia-ss-bode.png" alt="Bode de magnitud y fase calculado desde el espacio de estados"><div class="cap">Bode obtenido directamente del modelo en espacio de estados: para cada frecuencia se resuelve $G(j\omega)=C(j\omega I-A)^{-1}B+D$ con <code>np.linalg.solve</code> (más estable que invertir). De aquí salen la impedancia analítica $Y=-G$, $Z=Y^{-1}$ y el minor loop gain del criterio por impedancia. La malla logarítmica debe ser fina para no perder resonancias agudas.</div></div>

## 1 — De las matrices \( A,B,C,D \) a \( G(j\omega) \): derivación y ejemplo numérico
**Paso 1 — origen de la fórmula.** En espacio de estados, con entrada \( u(t) \) y salida \( y(t)=C\,x+D\,u \), tomando la transformada de Laplace con condiciones iniciales nulas:

$$ s\,X(s) = A\,X(s) + B\,U(s) \;\Rightarrow\; (sI-A)\,X(s) = B\,U(s) \;\Rightarrow\; X(s)=(sI-A)^{-1}B\,U(s) $$

Sustituyendo en la salida:

$$ Y(s) = \bigl[C(sI-A)^{-1}B + D\bigr]\,U(s) = \mathbf{G}(s)\,U(s) $$

Evaluar en \( s=j\omega \) da la respuesta en frecuencia: \( \mathbf{G}(j\omega)=C(j\omega I-A)^{-1}B+D \).

**Paso 2 — ejemplo numérico \( 2\times2 \).** Sistema RL acoplado en dq: \( \dot{i}_d=-(R/L)\,i_d+\omega_0\,i_q+v_d/L \), \( \dot{i}_q=-(R/L)\,i_q-\omega_0\,i_d+v_q/L \). Con \( R/L=50 \), \( \omega_0=314 \):

$$ A=\begin{bmatrix}-50 & 314 \\ -314 & -50\end{bmatrix},\quad B=\frac{1}{L}I_{2\times2},\quad C=I_{2\times2},\quad D=0 $$

A \( f=50\,\text{Hz} \) (\( \omega=314 \) rad/s):

$$ j\omega I - A = \begin{bmatrix}j314+50 & -314 \\ 314 & j314+50\end{bmatrix} $$

$$ \det = (50+j314)^2 + 314^2 = 2500 - 98596 + j\cdot2\times50\times314 + 314^2 = 314^2(j^2-1)+j31400+2500+314^2 $$

Al invertir y multiplicar por \( B,C \) se obtiene la admitancia \( Y(j\omega) \) que muestra el acoplamiento d-q: la excitación en el eje d produce respuesta tanto en d como en q (términos fuera de la diagonal de la matriz \( 2\times2 \)).

**Paso 3 — por qué usar `solve` en vez de `inv`.** Calcular \( (j\omega I-A)^{-1}B \) como \( [(j\omega I-A)^{-1}]\cdot B \) requiere invertir la matriz; numéricamente equivale a resolver \( n \) sistemas lineales. `np.linalg.solve(sI-A, B)` lo hace directamente con factorización LU, con mejor estabilidad numérica (condicionamiento similar, pero evita la amplificación de errores al multiplicar la inversa completa).

$$ \boxed{\mathbf{G}(j\omega)=C\,(j\omega I-A)^{-1}B+D\;\equiv\;\text{FDT evaluada en }s=j\omega} $$

## Cuándo y por qué se usa
Para obtener la impedancia analítica del inversor (Fase 2), trazar Bode de lazos, o construir el
*minor loop gain* del criterio de estabilidad por impedancia.

## Procedimiento de diseño (genérico)
1. Parte de \( A,B,C,D \) (de la linealización).
2. Define la malla de frecuencias (logarítmica).
3. Para cada \( \omega \): \( G=C\,(j\omega I-A)^{-1}B+D \) vía `solve`.
4. Deriva lo que necesites: \( Y=-G \), \( Z=Y^{-1} \), magnitud/fase para Bode.

## Ejemplo de código
```python
import numpy as np
def freqresp(A, B, C, D, freqs):
    n = A.shape[0]; I = np.eye(n)
    G = np.zeros((len(freqs), C.shape[0], B.shape[1]), dtype=complex)
    for k, f in enumerate(freqs):
        s = 2j*np.pi*f
        G[k] = C @ np.linalg.solve(s*I - A, B) + D
    return G
```

## Parámetros y valores típicos
Malla logarítmica (p.ej. 0.1 Hz–5 kHz, 300–2000 puntos). Usar `solve`, no `inv`.

## Errores comunes
- Invertir \( (sI-A) \) explícitamente → menos preciso/eficiente que `solve`.
- Malla de frecuencias demasiado gruesa → pierde resonancias agudas.

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: impedancia y estabilidad): `impedance.py` calcula \( Y \) y
  \( Z \) así; `main_phase3.py` lo usa para el Nyquist generalizado.

## Conceptos relacionados
- [[linealizacion-numerica]] · [[impedancia-salida-estabilidad]] · [[medicion-impedancia-inyeccion]]

## Referencias
- Skogestad, Postlethwaite, *Multivariable Feedback Control*, 2005.

---

## 3 — De la representación en espacio de estados a la FdT

La función de transferencia del sistema \( \dot{x}=Ax+Bu \), \( y=Cx+Du \) se obtiene en el dominio de Laplace por:

$$ \mathbf{G}(s) = \mathbf{C}(s\mathbf{I}-\mathbf{A})^{-1}\mathbf{B} + \mathbf{D} $$

**Evaluación numérica eficiente.** Para cada frecuencia \( \omega \), en lugar de invertir explícitamente la matriz, se resuelve el sistema lineal:

$$ (j\omega \mathbf{I} - \mathbf{A})\,\mathbf{X} = \mathbf{B}\mathbf{U} \quad\Rightarrow\quad \mathbf{G}(j\omega) = \mathbf{C}\,\mathbf{X} + \mathbf{D} $$

En Python: `X = np.linalg.solve(1j*w*np.eye(n) - A, B)` seguido de `G = C @ X + D`. Esto evita la inversión matricial simbólica y es numéricamente más estable (factorización LU directa).

**Sistema MIMO.** Para un sistema de \( p \) salidas y \( m \) entradas, \( \mathbf{G}(j\omega) \) es una matriz \( p\times m \). El elemento \( G_{ij}(j\omega) \) es la respuesta en frecuencia desde la entrada \( j \) a la salida \( i \). En el convertidor VSC en coordenadas dq, la planta es \( 2\times2 \) con acoplamiento cruzado.

<div class="cfig"><img src="../figuras/respuesta-frecuencia-ss-analisis.png" alt="Respuesta en frecuencia desde espacio de estados"><div class="cap">Panel superior izquierdo: Bode calculado directamente con np.linalg.solve. Superior derecho: valores singulares de planta MIMO 2×2. Inferior izquierdo: pérdida de fase por retardo de cómputo Td. Inferior derecho: validación modelo vs medida con ruido.</div></div>

## 4 — Diagrama de Bode desde matrices de estado

**Algoritmo.** Para cada frecuencia \( \omega_k \) de la malla logarítmica \( [\omega_{min}, \omega_{max}] \):

1. Resolver \( (j\omega_k I - A) X_k = B \) con `np.linalg.solve`.
2. Calcular \( G_k = C X_k + D \).
3. Extraer módulo: \( |G_k| \) (dB = \( 20\log_{10}|G_k| \)); fase: \( \angle G_k \) (grados).

**Margen de fase.** Se busca la frecuencia de cruce de ganancia \( \omega_c \) donde \( |G(j\omega_c)| = 1 \):

$$ PM = 180° + \angle G(j\omega_c) $$

**Margen de ganancia.** Se busca \( \omega_{pc} \) donde \( \angle G(j\omega_{pc}) = -180° \):

$$ GM = \frac{1}{|G(j\omega_{pc})|} \quad (\text{en dB: } -20\log_{10}|G(j\omega_{pc})|) $$

**Herramienta alternativa.** `scipy.signal.bode(sys)` acepta instancias de `StateSpace` o `TransferFunction` y devuelve arrays de magnitud y fase. Para MIMO usar la evaluación directa con `solve`.

## 5 — Respuesta en frecuencia de convertidores

**Modelo dq del VSC.** La planta en coordenadas dq es una matriz \( 2\times2 \) con acoplamiento cruzado:

$$ G_{dq}(j\omega) = \frac{1}{R+j\omega L}\begin{bmatrix}1 & -j\omega_0 L/R \\ j\omega_0 L/R & 1\end{bmatrix} \approx \frac{1}{R+j\omega L} \mathbf{I}_{2\times2} + \text{acoplamiento} $$

El término fuera de la diagonal es \( \pm\omega_0 L \), que a \( f=50\,\text{Hz} \) equivale a una reactancia significativa.

**Desacoplamiento feedforward.** Se añaden términos \( \pm\omega_0 L \, i_{q,d} \) a la salida del regulador para cancelar el acoplamiento cruzado. La planta desacoplada es diagonal, lo que simplifica el diseño del PI de corriente a dos lazos SISO independientes.

**Respuesta en frecuencia del lazo cerrado.** El pico de resonancia \( M_p = \|T\|_\infty \) (donde \( T=(I+GC)^{-1}GC \)) está relacionado con el margen de fase por \( M_p \approx 1/(2\zeta) \). Un pico \( > 6\,\text{dB} \) indica margen de fase \( < 29° \): problema de robustez ante variación de inductancia.

**Medición experimental.** En operación real se inyecta una señal de frecuencia variable en la referencia \( v_{ref} \) o \( i_{ref} \) y se mide la respuesta; la relación entrada-salida construye el Bode medido.

## 6 — Validación cruzada modelo-medida

**Procedimiento.** Se inyecta una perturbación senoidal de amplitud pequeña (1-5% del nominal) en la referencia y se mide la respuesta en estado estacionario. La relación fasorial a cada frecuencia construye el Bode experimental.

**Criterio de aceptación.** Diferencias \( > 3\,\text{dB} \) en ganancia o \( > 15° \) en fase indican un error de modelado: posibles causas son el retardo de cómputo/modulación no modelado, saturaciones activas, o no-linealidades del convertidor.

**Retardo de cálculo.** Un retardo puro \( T_d \) añade fase:

$$ G_{delay}(s) = e^{-sT_d} \approx \frac{1-sT_d/2}{1+sT_d/2} \quad\text{(aproximación de Padé primer orden)} $$

A \( f_c = 1\,\text{kHz} \) y \( T_d = 100\,\mu\text{s} \), la pérdida de fase es \( \Delta\phi = 2\pi f_c T_d \cdot 180°/\pi \approx 36° \): impacto severo que debe incluirse en el modelo.

**Fuentes de discrepancia típicas:**
- Retardo de muestreo y ZOH: \( \approx T_s/2 \) adicional.
- Filtros antialiasing del ADC: atenúan la respuesta cerca de \( f_s/4 \).
- Saturación del modulador PWM: modifica la ganancia efectiva a amplitudes grandes.

## 7 — Código Python: evaluación numérica completa de \( G(j\omega) \)

El siguiente bloque implementa la evaluación eficiente de \( G(j\omega) = C(j\omega I - A)^{-1}B + D \) para sistemas SISO y MIMO, con cálculo de márgenes y comparación analítico vs medida:

```python
import numpy as np
import matplotlib.pyplot as plt

def freqresp_ss(A, B, C, D, freqs_hz):
    """Respuesta en frecuencia desde matrices de estado.
    
    Parámetros
    ----------
    A, B, C, D : matrices del sistema (numpy arrays)
    freqs_hz   : array de frecuencias en Hz
    
    Retorna
    -------
    G : array complejo de forma (N_freq, n_out, n_in)
    """
    n = A.shape[0]
    I = np.eye(n)
    G = np.zeros((len(freqs_hz), C.shape[0], B.shape[1]), dtype=complex)
    for k, f in enumerate(freqs_hz):
        s = 2j * np.pi * f
        # np.linalg.solve es más estable que @ np.linalg.inv(s*I - A)
        X = np.linalg.solve(s * I - A, B)
        G[k] = C @ X + D
    return G


# --- Ejemplo: lazo de corriente VSC dq (MIMO 2x2) ---
R = 0.5; L = 5e-3; w0 = 2*np.pi*50

# Matrices del estado: inductor RL con acoplamiento dq
A_dq = np.array([[-R/L,  w0],
                  [-w0, -R/L]])
B_dq = np.eye(2) / L
C_dq = np.eye(2)
D_dq = np.zeros((2, 2))

freqs = np.logspace(0, 4, 300)   # 1 Hz a 10 kHz
G_dq = freqresp_ss(A_dq, B_dq, C_dq, D_dq, freqs)

# Valores singulares de la matriz G(jw): representan el "Bode MIMO"
sigma_max = np.array([np.linalg.svd(G_dq[k], compute_uv=False)[0] for k in range(len(freqs))])
sigma_min = np.array([np.linalg.svd(G_dq[k], compute_uv=False)[-1] for k in range(len(freqs))])

# Términos diagonal y fuera de diagonal
G_dd = G_dq[:, 0, 0]    # d->d
G_dq_cross = G_dq[:, 0, 1]  # q->d (acoplamiento cruzado)

fig, axes = plt.subplots(2, 2, figsize=(12, 8))

ax = axes[0, 0]
ax.semilogx(freqs, 20*np.log10(np.abs(G_dd)), 'b-', lw=2, label='G_dd (diagonal)')
ax.semilogx(freqs, 20*np.log10(np.abs(G_dq_cross)), 'r--', lw=2, label='G_dq (cruzado)')
ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Ganancia (dB)')
ax.set_title('Elementos de G(jω) — lazo corriente dq')
ax.legend(); ax.grid(True, alpha=0.3)

ax = axes[0, 1]
ax.semilogx(freqs, 20*np.log10(sigma_max), 'b-', lw=2, label='σ_max')
ax.semilogx(freqs, 20*np.log10(sigma_min), 'r--', lw=2, label='σ_min')
ax.set_xlabel('Frecuencia (Hz)'); ax.set_ylabel('Valor singular (dB)')
ax.set_title('Valores singulares de G(jω) MIMO')
ax.legend(); ax.grid(True, alpha=0.3)
```

## 8 — Aproximación de Padé para retardo de cómputo

El retardo de cómputo \( T_d \) (un período de muestreo en control digital) se modela con la aproximación de Padé:

$$ e^{-sT_d} \approx \frac{1 - sT_d/2}{1 + sT_d/2} \quad \text{(1er orden)} \qquad e^{-sT_d} \approx \frac{1 - sT_d/2 + (sT_d)^2/12}{1 + sT_d/2 + (sT_d)^2/12} \quad \text{(2º orden)} $$

```python
def pade_delay(Td, order=1):
    """Aproximación de Padé del retardo puro e^{-sTd}.
    
    Retorna (num, den) de la función de transferencia racional.
    order=1: Padé de primer orden
    order=2: Padé de segundo orden
    """
    if order == 1:
        num = [-Td/2, 1]
        den = [ Td/2, 1]
    elif order == 2:
        num = [Td**2/12, -Td/2, 1]
        den = [Td**2/12,  Td/2, 1]
    else:
        raise ValueError("Solo orden 1 o 2")
    return np.array(num), np.array(den)


# Comparar la pérdida de fase real vs Padé
Td = 100e-6    # 100 µs (1 muestra a Ts=100 µs)
freqs_val = np.logspace(1, 4, 300)
w_val = 2 * np.pi * freqs_val

# Retardo exacto
phase_exact = -np.degrees(w_val * Td)

# Padé 1er orden
num_p1, den_p1 = pade_delay(Td, order=1)
G_p1 = np.polyval(num_p1, 1j*w_val) / np.polyval(den_p1, 1j*w_val)
phase_p1 = np.degrees(np.angle(G_p1))

# Padé 2º orden
num_p2, den_p2 = pade_delay(Td, order=2)
G_p2 = np.polyval(num_p2, 1j*w_val) / np.polyval(den_p2, 1j*w_val)
phase_p2 = np.degrees(np.angle(G_p2))

# Error de fase (Padé vs exacto)
print("Error máx Padé 1er orden:", np.max(np.abs(phase_p1 - phase_exact)), "grados")
print("Error máx Padé 2º orden: ", np.max(np.abs(phase_p2 - phase_exact)), "grados")

# Frecuencia a la que el error del Padé 1er orden supera 5°
err_mask = np.abs(phase_p1 - phase_exact) > 5
if err_mask.any():
    f_err = freqs_val[np.argmax(err_mask)]
    print(f"Padé 1er orden pierde >5° de exactitud a partir de {f_err:.0f} Hz")
```

**Regla práctica.** El Padé de primer orden es exacto hasta \( f \approx 1/(4\pi T_d) \). Para \( T_d = 100\,\mu\text{s} \), esto es \( \approx 800\,\text{Hz} \): válido para el diseño del lazo de corriente pero no para el análisis de resonancias del filtro LCL (1–2 kHz).

## 9 — Validación modelo vs medida con código Python

```python
def validate_model_vs_measurement(A, B, C, D, freqs_meas, G_meas, Td=0):
    """Compara la respuesta analítica del modelo con datos medidos.
    
    G_meas: array complejo de forma (N_freq,) — datos experimentales
    Td: retardo de cómputo en segundos (opcional)
    
    Retorna: error_mag_dB, error_phase_deg para cada frecuencia
    """
    G_model = freqresp_ss(A, B, C, D, freqs_meas)[:, 0, 0]  # SISO: elemento (0,0)
    
    # Incluir retardo si se especifica
    if Td > 0:
        num_p, den_p = pade_delay(Td, order=2)
        w_arr = 2 * np.pi * np.array(freqs_meas)
        G_delay = np.polyval(num_p, 1j*w_arr) / np.polyval(den_p, 1j*w_arr)
        G_model = G_model * G_delay
    
    error_mag = 20*np.log10(np.abs(G_model)) - 20*np.log10(np.abs(G_meas))
    error_phase = np.degrees(np.angle(G_model)) - np.degrees(np.angle(G_meas))
    # Normalizar la diferencia de fase al rango [-180, 180]
    error_phase = (error_phase + 180) % 360 - 180
    
    # Criterio de aceptación
    max_err_mag = np.max(np.abs(error_mag))
    max_err_phase = np.max(np.abs(error_phase))
    ok = (max_err_mag < 3) and (max_err_phase < 15)
    print(f"Error máx ganancia: {max_err_mag:.2f} dB  (límite: 3 dB)")
    print(f"Error máx fase:     {max_err_phase:.1f}°  (límite: 15°)")
    print(f"Validación: {'PASS' if ok else 'FAIL'}")
    return error_mag, error_phase


# Simular datos "medidos" con ruido y retardo para el ejemplo
np.random.seed(42)
freqs_test = np.logspace(1, 3.5, 50)
G_analytic = freqresp_ss(A_dq, B_dq, C_dq, D_dq, freqs_test)[:, 0, 0]

# Datos "medidos": modelo analítico + retardo 100µs + ruido 2%
Td_real = 100e-6
w_test = 2 * np.pi * np.array(freqs_test)
G_delay_sim = np.exp(-1j * w_test * Td_real)
noise = 0.02 * (np.random.randn(len(freqs_test)) + 1j*np.random.randn(len(freqs_test)))
G_measured_sim = G_analytic * G_delay_sim + noise

# Validar sin retardo (debería fallar por la fase del retardo)
print("--- Sin retardo en el modelo:")
validate_model_vs_measurement(A_dq, B_dq, C_dq, D_dq, freqs_test, G_measured_sim, Td=0)

# Validar con retardo (debería pasar)
print("--- Con retardo Padé 2º orden:")
validate_model_vs_measurement(A_dq, B_dq, C_dq, D_dq, freqs_test, G_measured_sim, Td=Td_real)
```
