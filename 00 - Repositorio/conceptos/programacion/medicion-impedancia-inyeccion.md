---
titulo: Medición de impedancia por inyección de perturbación
slug: medicion-impedancia-inyeccion
categoria: programacion
tipo: metodo
nivel: avanzado
proyectos: [01-GFM-Impedance]
objetivos: [medir Z_dq en simulacion/hardware y validar el modelo]
tags: [impedancia, inyeccion, demodulacion, MIMO, validacion, PLECS]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [impedancia-salida-estabilidad, respuesta-frecuencia-ss, convertidor-vsc]
referencias:
  - "Roinila et al., Frequency-Response Measurement of Converters, IEEE TPEL"
---

## Definición
Procedimiento para **medir** la impedancia/admitancia dq de un convertidor (en simulación
conmutada, PLECS o hardware) inyectando perturbaciones y analizando la respuesta. Es la
contraparte experimental del cálculo analítico \( Y=C(sI-A)^{-1}B+D \).

## Fundamento teórico
A cada frecuencia \( f_p \) se inyecta una perturbación senoidal de tensión. Como el sistema dq
es **MIMO 2×2**, se necesitan **dos** inyecciones linealmente independientes (eje d y eje q)
para identificar la matriz completa. Con los fasores de tensión \( \mathbf{V} \) y corriente
\( \mathbf{I} \) (columnas = experimentos):
$$ \mathbf{I}=\mathbf{G}\,\mathbf{V}\;\Rightarrow\;\mathbf{G}=\mathbf{I}\,\mathbf{V}^{-1},\qquad
   \mathbf{Y}=-\mathbf{G},\quad \mathbf{Z}=\mathbf{Y}^{-1} $$
Los fasores se extraen por **demodulación** (correlación con sin/cos sobre un número entero de
periodos).

<div class="cfig"><img src="figuras/medicion-impedancia-inyeccion-bode.png" alt="impedancia medida por inyeccion frente a la analitica"><div class="cap">La impedancia medida inyectando perturbaciones y demodulando los fasores (en simulación conmutada, PLECS o hardware) se superpone a la calculada analíticamente con $Y=C(sI-A)^{-1}B+D$. El acuerdo (error medio ~0.2 %) valida el modelo promediado en pequeña señal; deja de valer si la amplitud activa el current limiting.</div></div>

## 1 — De la perturbación inyectada al fasor: proceso completo a una frecuencia
**Paso 1 — inyección de un tono.** A la frecuencia \( f_p \) se superpone una perturbación senoidal de tensión de amplitud \( A \) sobre el punto de equilibrio:

$$ v_{pert}(t) = A\sin(2\pi f_p t) $$

La amplitud \( A \) debe ser **pequeña señal**: suficiente para que la relación señal/ruido (SNR) en la medición de la respuesta sea adecuada, pero sin activar saturaciones ni el current limiting. En la práctica \( A \approx 0.01\text{–}0.05\,\text{p.u.} \) del nominal.

**Paso 2 — medición y demodulación.** Se miden \( v(t) \) e \( i(t) \) durante \( N_{ciclos} \) periodos completos de \( f_p \). Los fasores se extraen por correlación (DFT a una única frecuencia):

$$ \hat{V}(f_p) = \frac{2}{T}\int_0^T v(t)\,e^{-j2\pi f_p t}\,dt \approx \frac{2}{N}\sum_{k=1}^N v[k]\,e^{-j2\pi f_p k/N} $$

Usar un número **entero** de periodos evita fuga espectral: si la ventana no es exactamente \( N_{ciclos}/f_p \), el fasor tiene error por el espectro de las frecuencias vecinas.

**Paso 3 — relación señal/ruido vs amplitud.** El SNR de la medición a \( f_p \) es:

$$ \text{SNR} \approx \frac{A \cdot |Z(f_p)|}{v_{ruido,rms}} $$

Un SNR \( >20\,\text{dB} \) (factor 10 en amplitud) garantiza errores de fasor \( <1\,\% \). Si la impedancia \( |Z| \) es pequeña (frecuencias altas, donde el inductor domina) se necesita \( A \) mayor; si es grande (cerca de resonancias), con \( A \) pequeña basta. El compromiso: \( A \) grande mejora el SNR pero puede excitar no linealidades.

**Paso 4 — construcción de la matriz \( \mathbf{Z} \).** Con las dos inyecciones (eje d y eje q) se forman las matrices \( 2\times2 \) de fasores y se invierte:

$$ \mathbf{Z}(f_p) = -\mathbf{V}\,\mathbf{I}^{-1} $$

$$ \boxed{Z_{dd},Z_{dq},Z_{qd},Z_{qq} \text{ en un punto de frecuencia con 2 experimentos MIMO}} $$

## Cuándo y por qué se usa
Para **validar** el modelo promediado contra la planta conmutada/real, y para caracterizar
convertidores comerciales "caja negra" cuya impedancia no se conoce analíticamente.

## Procedimiento de diseño (genérico)
1. Lleva el sistema al punto de operación.
2. Para cada \( f_p \): inyecta en d (exp.1) y en q (exp.2), pequeña amplitud (pequeña señal).
3. Simula hasta régimen permanente (descarta el transitorio).
4. Demodula \( v,i \) a \( f_p \) (correlación sobre periodos enteros) → fasores.
5. Monta \( \mathbf{G}=\mathbf{I}\,\mathbf{V}^{-1} \), \( Z=(-G)^{-1} \). Repite en frecuencia.
6. Compara con el analítico (debe coincidir en pequeña señal).

## Ejemplo de código
```python
def phasor(t, x, fp):                 # demodulacion sobre periodos enteros
    w = 2*np.pi*fp; T = t[-1]-t[0]
    c = np.trapz(x*np.cos(w*t), t); s = np.trapz(x*np.sin(w*t), t)
    return (2/T)*(c - 1j*s)
# dos inyecciones (d, q) -> columnas de V e I
G = I @ np.linalg.inv(V); Y = -G; Z = np.linalg.inv(Y)
```

## Parámetros y valores típicos
Amplitud pequeña (pequeña señal); ventana de varios periodos tras el asentamiento. Validez solo
mientras no haya saturación (si entra el current limiting, deja de ser lineal).

## Errores comunes
- Una sola inyección en un sistema dq acoplado → no identifica la matriz 2×2.
- Ventana no entera de periodos → fuga espectral en la demodulación.
- Amplitud grande que activa no linealidades → la "impedancia" deja de tener sentido.

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: validar el modelo): la Z medida por inyección coincidió con
  la analítica con **error medio 0.21%**. En `inject.py` / `main_phase4.py`. El mismo código
  procesa datos exportados de PLECS.

## Conceptos relacionados
- [[impedancia-salida-estabilidad]] · [[respuesta-frecuencia-ss]] · [[convertidor-vsc|modelo promediado]]

## Referencias
- Roinila et al., medición de respuesta en frecuencia de convertidores.

---

## 3 — Método de inyección de señal

**Inyección de la perturbación.** Se superpone una señal senoidal de tensión en el punto de medida:

$$ v_p(t) = A\sin(\omega t), \quad \omega = 2\pi f_p $$

La amplitud \( A \) es un compromiso entre relación señal/ruido (requiere \( A \) grande) y linealidad del sistema (requiere \( A \) pequeña). En convertidores de potencia, \( A \approx 1\text{–}5\,\% \) del valor nominal garantiza ambas condiciones.

**Medición de tensión y corriente.** Se registran simultáneamente \( v(t) \) e \( i(t) \) en el punto de inyección. La impedancia se calcula como:

$$ Z(j\omega) = \frac{V(j\omega)}{I(j\omega)} $$

donde \( V(j\omega) \) e \( I(j\omega) \) son los fasores a frecuencia \( f_p \) obtenidos por DFT.

**Amplitud de perturbación.** La elección práctica de \( A \) depende del nivel de ruido \( v_{ruido,rms} \) y de la impedancia esperada:

$$ \text{SNR} \approx \frac{A \cdot |Z(f_p)|}{v_{ruido,rms}} > 20\,\text{dB} $$

<div class="cfig"><img src="../figuras/medicion-impedancia-inyeccion-analisis.png" alt="Medición de impedancia por inyección de señal"><div class="cap">Panel superior izquierdo: señal inyectada y respuesta en corriente. Superior derecho: espectro DFT mostrando el tono inyectado. Inferior izquierdo: comparación impedancia teórica vs medida en barrido de frecuencia. Inferior derecho: coherencia del barrido — válido solo donde γ²>0.9.</div></div>

## 4 — DFT y sincronización

**Ventana coherente.** La DFT asume señales periódicas. Si la ventana de análisis no contiene exactamente \( N_{ciclos} \) períodos completos de la señal inyectada, aparece **fuga espectral**: energía de la frecuencia de inyección se dispersa hacia frecuencias vecinas, contaminando la estimación del fasor.

**Condición de coherencia:**

$$ T_{ventana} = \frac{N_{ciclos}}{f_p} \quad (N_{ciclos} \in \mathbb{Z}^+) $$

Si no se puede garantizar coherencia (p.ej. el muestreo no es síncrono con la inyección), se aplica una **ventana de Hanning** que atenúa la fuga a costa de reducir la resolución espectral.

**Rango de frecuencias analizables:**
- Mínimo: \( f_{min} = f_p \) (una resolución de la DFT)
- Máximo: \( f_{max} \approx f_{sw}/2 \) (Nyquist del muestreo de control)
- Límite práctico: evitar frecuencias múltiplos de \( f_0=50\,\text{Hz} \) donde el ruido de red es mayor

**Supresión de interarmónicos.** El muestreo coherente con la señal inyectada asegura que los armónicos del convertidor (múltiplos de \( f_{sw} \)) caen en bins separados de la DFT, sin solaparse con \( f_p \).

## 5 — Analizador de impedancias en lazo cerrado

**Inyección en el lazo de control.** Al inyectar la perturbación después del regulador (entre el control y el modulador), se mide la impedancia de lazo cerrado \( Z_{cl}(j\omega) \). Esta es la magnitud relevante para el criterio de estabilidad de Middlebrook.

**Inyección en la red.** Al inyectar en la red (entre el convertidor y el transformador), se mide \( Z_{grid}(j\omega) \), útil para detectar variaciones del SCR sin interrumpir la operación.

**Separación fuente/carga.** Para separar la impedancia de la fuente \( Z_s \) de la de la carga \( Z_l \), se realizan dos inyecciones en puntos distintos o una perturbación diferencial; la combinación lineal de las respuestas da cada impedancia por separado.

**Criterio de validez de la medición:** el SNR debe superar 20 dB en la frecuencia de análisis. Por debajo de este umbral el fasor estimado tiene error angular \( > 5.7° \), que puede confundirse con una variación real de impedancia.

## 7 — Código Python completo: inyección, DFT y barrido de frecuencia

El siguiente módulo implementa la medición de impedancia por inyección de señal sinusoidal, demodulación con DFT coherente y estimación de la coherencia con `scipy.signal.csd`:

```python
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


def inject_and_measure(Z_func, freqs_hz, A_inj=0.05, fs=10000.0, n_cycles=10):
    """Simula la medición de impedancia por inyección de señal.

    Z_func  : función que acepta frecuencia en Hz y retorna Z complejo (modelo teórico)
    freqs_hz: array de frecuencias a medir [Hz]
    A_inj   : amplitud de la perturbación inyectada [pu]
    fs      : frecuencia de muestreo [Hz]
    n_cycles: número de ciclos completos a registrar (ventana coherente)

    Retorna: Z_meas (array complejo), coherence (array real)
    """
    Z_meas = np.zeros(len(freqs_hz), dtype=complex)
    coherence = np.zeros(len(freqs_hz))

    np.random.seed(0)   # reproducibilidad
    noise_level = A_inj * 0.05   # 5% de ruido sobre la amplitud inyectada

    for k, fp in enumerate(freqs_hz):
        # Duración exacta de n_cycles periodos completos (ventana coherente)
        T_window = n_cycles / fp
        N = int(np.round(T_window * fs))
        t = np.arange(N) / fs

        # Señal inyectada: senoidal pura
        v_inj = A_inj * np.sin(2*np.pi*fp*t)

        # Respuesta de corriente: i = v/Z + ruido
        Z_k = Z_func(fp)
        i_resp = (A_inj / np.abs(Z_k)) * np.sin(2*np.pi*fp*t - np.angle(Z_k))
        i_resp += noise_level * np.random.randn(N)
        v_inj_noisy = v_inj + noise_level * 0.5 * np.random.randn(N)

        # Demodulación: fasor por correlación sobre ventana completa
        def phasor_dft(sig, f, t_arr):
            """Extrae el fasor a frecuencia f por correlación (DFT a un único bin)."""
            T = t_arr[-1] - t_arr[0] + 1/fs
            c = np.trapz(sig * np.cos(2*np.pi*f*t_arr), t_arr)
            s = np.trapz(sig * np.sin(2*np.pi*f*t_arr), t_arr)
            return (2/T) * (c - 1j*s)

        V_phasor = phasor_dft(v_inj_noisy, fp, t)
        I_phasor = phasor_dft(i_resp, fp, t)

        # Impedancia medida: Z = V/I
        Z_meas[k] = V_phasor / I_phasor

        # Coherencia estimada con scipy.signal.csd (requiere señal suficientemente larga)
        if N >= 64:
            f_csd, Pvv = signal.welch(v_inj_noisy, fs=fs, nperseg=min(N, 256))
            f_csd, Pii = signal.welch(i_resp, fs=fs, nperseg=min(N, 256))
            f_csd, Pvi = signal.csd(v_inj_noisy, i_resp, fs=fs, nperseg=min(N, 256))
            # Índice del bin más cercano a fp
            idx = np.argmin(np.abs(f_csd - fp))
            gamma2 = np.abs(Pvi[idx])**2 / (Pvv[idx] * Pii[idx] + 1e-30)
            coherence[k] = np.real(gamma2)
        else:
            coherence[k] = 1.0   # ventana corta: asumir coherente

    return Z_meas, coherence


# --- Ejemplo de aplicación: bus DC de data center con CPL ---
def Z_bus_dc(f):
    """Impedancia del bus DC: condensador + inductancia del cable + CPL negativa."""
    s = 2j * np.pi * f
    C_bus = 1e-3   # 1 mF condensador del bus
    L_cable = 50e-6  # 50 µH cable rack-PDU
    R_cable = 0.01   # 10 mΩ
    Z_cap = 1 / (s * C_bus)
    Z_ind = s * L_cable + R_cable
    # CPL: impedancia incremental negativa Z_CPL = -V_dc^2/P_cpl
    V_dc = 380.0; P_cpl = 5000.0
    Z_cpl = -V_dc**2 / P_cpl   # resistencia negativa
    # Paralelo de Z_cap con Z_cpl
    Z_load = (Z_cap * Z_cpl) / (Z_cap + Z_cpl)
    return Z_ind + Z_load


freqs_sweep = np.logspace(1, 3.8, 40)   # 10 Hz a 6 kHz
Z_meas_dc, gamma2_dc = inject_and_measure(Z_bus_dc, freqs_sweep, A_inj=5.0, fs=20000, n_cycles=8)
Z_analytic_dc = np.array([Z_bus_dc(f) for f in freqs_sweep])

# Identificar frecuencias válidas (coherencia > 0.9)
valid = gamma2_dc > 0.9
print(f"Puntos válidos (γ²>0.9): {np.sum(valid)}/{len(freqs_sweep)}")

# Error de la medición
err_mag = 20*np.log10(np.abs(Z_meas_dc[valid])) - 20*np.log10(np.abs(Z_analytic_dc[valid]))
print(f"Error medición (puntos válidos): {np.mean(np.abs(err_mag)):.2f} dB medio")
```

## 8 — Coherencia \( \gamma^2 \) con `scipy.signal.welch` y `csd`

La función de coherencia mide qué fracción de la potencia de la corriente a la frecuencia \( f \) se debe a la tensión inyectada (y no al ruido u otras perturbaciones):

$$ \gamma^2(f) = \frac{|S_{vi}(f)|^2}{S_{vv}(f)\,S_{ii}(f)} $$

donde \( S_{vv} \), \( S_{ii} \) son las densidades espectrales de potencia (PSD) y \( S_{vi} \) es la densidad espectral cruzada. Se calculan con Welch (promediado de ventanas solapadas):

```python
from scipy import signal
import numpy as np

def medir_coherencia_barrido(v_signals, i_signals, freqs_hz, fs):
    """Calcula la coherencia para cada frecuencia de un barrido.

    v_signals: lista de arrays (uno por frecuencia) con la tensión registrada
    i_signals: lista de arrays (uno por frecuencia) con la corriente registrada
    freqs_hz:  array de frecuencias del barrido [Hz]
    fs:        frecuencia de muestreo [Hz]

    Retorna: gamma2 (array), Z_valid (array complejo, NaN donde γ²<0.9)
    """
    gamma2 = np.zeros(len(freqs_hz))
    Z_valid = np.full(len(freqs_hz), np.nan, dtype=complex)

    for k, (v, i_sig, fp) in enumerate(zip(v_signals, i_signals, freqs_hz)):
        nperseg = min(len(v), 512)
        f_w, Pvv = signal.welch(v, fs=fs, nperseg=nperseg)
        f_w, Pii = signal.welch(i_sig, fs=fs, nperseg=nperseg)
        f_w, Pvi = signal.csd(v, i_sig, fs=fs, nperseg=nperseg)

        idx = np.argmin(np.abs(f_w - fp))
        g2 = np.abs(Pvi[idx])**2 / (Pvv[idx] * Pii[idx] + 1e-30)
        gamma2[k] = np.real(g2)

        if gamma2[k] > 0.9:
            # Estimar Z en el bin de frecuencia
            Z_valid[k] = Pvv[idx] / (np.conj(Pvi[idx]) + 1e-30)

    return gamma2, Z_valid


# Visualización del barrido con zona de coherencia
def plot_impedance_sweep(freqs, Z_meas, Z_model, gamma2, threshold=0.9):
    """Grafica impedancia medida vs modelo y la coherencia."""
    valid = gamma2 > threshold
    fig, axes = plt.subplots(3, 1, figsize=(10, 9), sharex=True)

    ax = axes[0]
    ax.semilogx(freqs[valid], 20*np.log10(np.abs(Z_meas[valid])), 'ro', ms=5, label='Medida (γ²>0.9)')
    ax.semilogx(freqs[~valid], 20*np.log10(np.abs(Z_meas[~valid])), 'rx', ms=5,
                alpha=0.4, label='Medida (γ²<0.9, no válida)')
    ax.semilogx(freqs, 20*np.log10(np.abs(Z_model)), 'b-', lw=2, label='Modelo analítico')
    ax.set_ylabel('|Z| (dB Ω)'); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    ax.set_title('Impedancia bus DC: medida vs modelo')

    ax = axes[1]
    ax.semilogx(freqs[valid], np.degrees(np.angle(Z_meas[valid])), 'ro', ms=5)
    ax.semilogx(freqs, np.degrees(np.angle(Z_model)), 'b-', lw=2)
    ax.set_ylabel('∠Z (°)'); ax.axhline(0, color='k', lw=0.5); ax.grid(True, alpha=0.3)

    ax = axes[2]
    ax.semilogx(freqs, gamma2, 'g-', lw=2)
    ax.axhline(threshold, color='r', ls='--', label=f'γ²={threshold} (umbral)')
    ax.fill_between(freqs, 0, gamma2, where=gamma2 > threshold,
                    alpha=0.2, color='green', label='Zona válida')
    ax.set_ylabel('Coherencia γ²'); ax.set_xlabel('Frecuencia (Hz)')
    ax.set_ylim([0, 1.05]); ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig


# Aplicar al ejemplo del bus DC
fig_dc = plot_impedance_sweep(freqs_sweep, Z_meas_dc, Z_analytic_dc, gamma2_dc)
```

## 9 — Aplicación: criterio de Middlebrook en bus DC de data center

El **criterio de Middlebrook** establece que el bus DC con fuente \( Z_s \) y carga \( Z_l \) es estable si:

$$ |Z_s(j\omega)| < |Z_l(j\omega)| \quad \forall\omega $$

Con cargas CPL (potencia constante), la impedancia incremental de carga tiene parte real negativa: \( \text{Re}(Z_{CPL}) < 0 \). Si \( |Z_s| > |Z_{CPL}| \) en alguna frecuencia, el bus puede oscilar.

```python
def middlebrook_criterion(freqs_hz, Z_source, Z_load):
    """Evalúa el criterio de estabilidad de Middlebrook.

    Retorna el minor loop gain T = Z_source/Z_load y la frecuencia crítica.
    El sistema es estable si |T(jω)| < 1 para toda ω (Middlebrook estricto).
    """
    T = Z_source / Z_load
    T_mag_dB = 20 * np.log10(np.abs(T))

    # Frecuencia de cruce (|T|=0 dB)
    crossings = np.where(np.diff(np.sign(T_mag_dB)))[0]
    if len(crossings) > 0:
        f_cross = freqs_hz[crossings[0]]
        PM_middlebrook = 180 + np.degrees(np.angle(T[crossings[0]]))
        print(f"Cruce de Middlebrook en {f_cross:.1f} Hz, PM_mid = {PM_middlebrook:.1f}°")
    else:
        print("No hay cruce: |T|<1 en todo el rango — sistema estable por Middlebrook")

    return T, T_mag_dB


# Impedancia de fuente: convertidor DC/DC (lazo cerrado)
def Z_source_dcdc(f):
    """Impedancia de salida del convertidor DC/DC en lazo cerrado."""
    s = 2j * np.pi * f
    # Aproximación: Z_out_cl = Z_out_ol / (1 + L(jw)) con L = K/(tau*s+1)
    K = 10; tau = 1e-3
    L_loop = K / (tau * s + 1)
    R_out = 0.05   # 50 mΩ salida del convertidor
    return R_out / (1 + L_loop)

Z_src = np.array([Z_source_dcdc(f) for f in freqs_sweep])
Z_lod = np.array([Z_bus_dc(f) for f in freqs_sweep])
T_mid, T_dB = middlebrook_criterion(freqs_sweep, Z_src, Z_lod)
```

## 6 — Herramientas Python y aplicación práctica

**Estimación espectral con ruido.** Para señales ruidosas, `scipy.signal.welch` calcula la densidad espectral de potencia (PSD) promediando sobre ventanas solapadas de Welch, reduciendo la varianza de la estimación de \( |Z|^2 \) a costa de resolución temporal.

**Coherencia.** El índice de coherencia entre tensión y corriente indica la fiabilidad de la estimación de impedancia:

$$ \gamma^2(f) = \frac{|S_{vi}(f)|^2}{S_{vv}(f)\,S_{ii}(f)} \in [0,1] $$

Un valor \( \gamma^2 > 0.9 \) indica que al menos el 90% de la varianza de la corriente a esa frecuencia se explica por la tensión inyectada: la medición es válida. Valores menores indican ruido excesivo, no-linealidades, o que la señal inyectada es demasiado débil.

**Aplicación en bus DC de data center.** Para caracterizar la estabilidad de un bus DC con cargas de potencia constante (CPL) se mide \( Z_{bus}(j\omega) \) a distintas cargas:
1. Inyectar una perturbación de tensión \( \Delta v_{dc} \) a la frecuencia de interés.
2. Medir la corriente de respuesta \( \Delta i_{dc} \).
3. Calcular \( Z_{bus}(j\omega) = \Delta V_{dc}(j\omega)/\Delta I_{dc}(j\omega) \).
4. Verificar el **criterio de Middlebrook**: el sistema es estable si \( |Z_{source}(j\omega)| < |Z_{load}(j\omega)| \) para toda \( \omega \). Si la CPL hace que \( Z_{load} \) tenga parte real negativa y su módulo sea menor que \( Z_{source} \), hay riesgo de oscilación.
