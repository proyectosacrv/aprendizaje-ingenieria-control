---
titulo: Análisis espectral con FFT
slug: fft-analisis-espectral
categoria: programacion
tipo: tecnica
nivel: basico
proyectos: []
objetivos: [obtener el contenido en frecuencia de señales medidas o simuladas]
tags: [fft, espectro, thd, ventana, muestreo, basico, programacion]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-30
relacionados: [medicion-impedancia-inyeccion, convertidor-vsc, diagrama-bode, respuesta-frecuencia-ss]
referencias:
  - "Oppenheim, Schafer, Discrete-Time Signal Processing, Prentice Hall"
  - "Harris, On the Use of Windows for Harmonic Analysis with the DFT, IEEE 1978"
---

## Definición
Algoritmo eficiente para calcular la **Transformada Discreta de Fourier** (DFT) de una señal
muestreada, obteniendo su amplitud y fase por frecuencia. Base para medir armónicos, THD y
respuestas en frecuencia experimentales.

## Fundamento teórico
La DFT de \( N \) muestras a \( f_s=1/T_s \):
$$ X_k=\sum_{n=0}^{N-1} x_n\,e^{-j2\pi kn/N},\qquad f_k=\frac{k f_s}{N} $$
- **Resolución:** \( \Delta f=f_s/N \) → más resolución exige ventanas más largas.
- **Nyquist:** solo es válido hasta \( f_s/2 \); por encima hay **aliasing** (filtrar antes).
- **Fuga espectral (leakage):** si la ventana no contiene un nº entero de periodos, la energía se
  reparte; se mitiga con **ventanas** (Hann, Hamming, Blackman) o muestreo **coherente**.
La distorsión armónica total se calcula sobre el espectro:
$$ \text{THD}=\frac{\sqrt{\sum_{h\ge2} X_h^2}}{X_1} $$

<div class="cfig"><img src="figuras/fft-analisis-espectral-fuga.png" alt="fuga espectral con ventana rectangular frente a ventana Hann"><div class="cap">Si la ventana no contiene un número entero de periodos de la señal, la energía del tono se reparte entre frecuencias vecinas (fuga espectral), ensanchando el pico y falseando la THD. Aplicar una ventana (Hann) o muestreo coherente concentra la energía y limpia el espectro. Es imprescindible al medir armónicos.</div></div>

## 1 — De dónde sale la DFT y la resolución \( \Delta f \)
**Paso 1 — proyectar sobre exponenciales.** Una señal continua periódica se descompone en serie de Fourier: suma de exponenciales complejas \( e^{j2\pi f t} \). Con la señal **muestreada** \( x_n=x(nT_s) \), \( n=0,\dots,N-1 \), solo disponemos de \( N \) muestras, así que únicamente podemos resolver \( N \) frecuencias. La DFT proyecta la señal sobre las \( N \) exponenciales discretas \( e^{j2\pi kn/N} \):

$$ X_k=\sum_{n=0}^{N-1} x_n\,e^{-j2\pi kn/N},\qquad k=0,\dots,N-1 $$

El coeficiente \( X_k \) mide cuánta energía de la señal está alineada con la sinusoide de índice \( k \) (el signo negativo del exponente es el producto interno con el conjugado).

**Paso 2 — a qué frecuencia física corresponde cada índice.** La exponencial de índice \( k \) completa \( k \) ciclos en la ventana de \( N \) muestras, es decir en un tiempo \( T=N T_s \). Su frecuencia es número de ciclos partido por duración:

$$ f_k=\frac{k}{N T_s}=\frac{k\,f_s}{N},\qquad f_s=\frac1{T_s} $$

**Paso 3 — la resolución es la separación entre índices.** La distancia en frecuencia entre dos bins consecutivos \( k \) y \( k+1 \) es:

$$ \boxed{\;\Delta f=f_{k+1}-f_k=\frac{f_s}{N}=\frac{1}{N T_s}=\frac1T\;} $$

La resolución es el **inverso de la duración total** de la ventana \( T=N T_s \). Para distinguir dos tonos separados \( \delta f \) hay que capturar al menos \( T>1/\delta f \) segundos: más resolución exige ventanas más largas, no más rápido muestreo. Aumentar \( f_s \) sin cambiar \( N \) **ensancha** los bins; aumentar \( N \) los afina.

**Paso 4 — el límite superior (Nyquist).** Los índices \( k>N/2 \) corresponden, por periodicidad de la exponencial, a frecuencias negativas (o equivalentemente a tonos por encima de \( f_s/2 \) que se "doblan"). Solo el rango \( 0\le f_k< f_s/2 \) es físicamente unívoco; por eso `rfft` devuelve únicamente \( N/2+1 \) bins.

## 2 — Fuga espectral (leakage) y por qué se aplica una ventana
**Paso 1 — la hipótesis oculta de la DFT.** La DFT trata las \( N \) muestras como **un periodo de una señal periódica**: implícitamente repite el bloque indefinidamente. Si la ventana contiene un número entero de periodos del tono, la repetición empalma sin saltos y toda la energía cae en un único bin (muestreo **coherente**).

**Paso 2 — qué pasa si no encaja.** Si la frecuencia del tono no es múltiplo exacto de \( \Delta f \), la frecuencia cae **entre** dos bins. La repetición periódica introduce una discontinuidad en el empalme de los extremos de la ventana. Una discontinuidad tiene contenido en todas las frecuencias: la energía del tono se **reparte** entre el bin más cercano y sus vecinos, ensanchando el pico. Esto es la **fuga espectral (leakage)**.

**Paso 3 — el origen matemático.** Truncar la señal a \( N \) muestras equivale a multiplicarla por una ventana rectangular \( w_n=1 \). En frecuencia, multiplicar por \( w_n \) es **convolucionar** el espectro del tono (una delta) con el espectro de la ventana. El espectro de la rectangular es un sinc:

$$ W(f)=\frac{\sin(\pi f N/f_s)}{\sin(\pi f/f_s)} $$

cuyos lóbulos laterales decaen lentamente (\( \sim1/f \), solo \( -13\,\text{dB} \) el primero). Esos lóbulos son la fuga: el sinc "unta" la delta sobre los bins vecinos.

**Paso 4 — la solución: ventanas suaves.** Una ventana que va a cero suavemente en los bordes (Hann, Hamming, Blackman) **elimina la discontinuidad** del empalme. Su transformada tiene lóbulos laterales mucho más bajos (Hann: \( -31\,\text{dB} \)) a costa de un lóbulo principal más ancho. La Hann es

$$ w_n=\tfrac12\!\left(1-\cos\tfrac{2\pi n}{N}\right) $$

**Paso 5 — corrección de amplitud.** Multiplicar por \( w_n \) atenúa la señal: la suma de la ventana ya no es \( N \) sino \( \sum_n w_n \) (para Hann, \( \approx N/2 \)). Para recuperar la amplitud real del tono hay que normalizar por la ganancia coherente de la ventana, no por \( N \):

$$ \boxed{\;A_k=\frac{2\,|X_k|}{\sum_{n} w_n}\;} $$

(el factor 2 recupera la energía del bin de frecuencia negativa al usar espectro de un solo lado). Sin esta corrección, la THD y las magnitudes de armónicos salen falseadas; es el error común del código de abajo si se omite `np.sum(np.hanning(...))`.

## Cuándo y por qué se usa
Para verificar calidad de onda (armónicos de [[convertidor-vsc|PWM]]), validar modelos contra
simulación y extraer la **impedancia/respuesta en frecuencia** por inyección (FFT del estímulo y
la respuesta → cociente), enlazando con [[medicion-impedancia-inyeccion]].

## Procedimiento (genérico)
1. Asegura \( f_s>2f_{max} \) y filtra antialiasing.
2. Toma \( N \) muestras (potencia de 2 ayuda); usa muestreo coherente o ventana.
3. `fft`, normaliza por \( N \) (y por la ganancia de la ventana), toma un lado del espectro.
4. Extrae fundamental, armónicos, THD o el cociente respuesta/estímulo.

## Ejemplo de aplicación real
**Problema:** Corriente de red de un VSC con 6 pulsos presenta armónicos en 250, 350, 550, 650 Hz (5ª, 7ª, 11ª, 13ª) con magnitudes 4.2, 2.8, 1.1, 0.8 % de la fundamental. Calcular el THD y verificar frente a IEEE 519.

\( \text{THD}=\sqrt{4.2^2+2.8^2+1.1^2+0.8^2}\,\%=\sqrt{17.64+7.84+1.21+0.64}\,\%\approx5.23\,\% \). Supera el límite IEEE 519 del 5 % (para SCR > 20): **incumplimiento leve**. Acción correctiva: un [[filtro-notch]] sintonizado en el 5º armónico (250 Hz) reduce su magnitud a <0.5 %; el THD resultante baja a \( \sqrt{0.25+7.84+1.21+0.64}\approx3.13\,\% \): cumple con margen. Alternativamente, [[control-repetitivo]] suprime simultáneamente todos los armónicos de red con un único bloque de control. El análisis FFT es el primer paso para decidir qué acción tomar.

## Ejemplo de código
```python
import numpy as np
X = np.fft.rfft(x*np.hanning(len(x)))      # ventana Hann
f = np.fft.rfftfreq(len(x), 1/fs)
mag = 2*np.abs(X)/np.sum(np.hanning(len(x)))   # amplitud corregida por ventana
```

## Parámetros y valores típicos
\( N \) potencia de 2 (1024–65536). Para armónicos de red, ventana de un nº entero de ciclos de
50/60 Hz (muestreo coherente) evita fuga sin ventana.

## Errores comunes
- No filtrar antes de muestrear → aliasing irreversible.
- Olvidar la corrección de amplitud por la ventana y por \( N \).
- Resolución insuficiente (\( \Delta f \) grande) para separar componentes próximas.

## Conceptos relacionados
- [[medicion-impedancia-inyeccion]] · [[convertidor-vsc|modulación PWM]] · [[respuesta-frecuencia-ss]] · [[diagrama-bode]]

## Referencias
- Oppenheim, Schafer, *Discrete-Time Signal Processing*.
- Harris, *On the Use of Windows for Harmonic Analysis with the DFT*, 1978.

## 3 — Resolución, leakage y ventanas espectrales

La **resolución frecuencial** \( \Delta f = f_s/N \) es el inverso de la duración total de la ventana \( T = N/f_s \). Para resolver dos tonos separados \( \delta f = 5\,\text{Hz} \) (e.g., 50 Hz y 55 Hz): \( T > 1/\delta f = 200\,\text{ms} \Rightarrow N > 200\,\text{ms} \times f_s \).

**Comparativa de ventanas:**

| Ventana | Lóbulo principal | Lóbulo lateral | Uso |
|---|---|---|---|
| Rectangular | Más estrecho (1 bin) | -13 dB | Solo si la señal es coherente |
| Hann (Hanning) | 2 bins | -31 dB | Uso general, armónicos de red |
| Hamming | 2 bins | -41 dB | Comunicaciones |
| Blackman | 3 bins | -57 dB | Cuando el leakage es crítico |
| Flat-top | 4 bins | -93 dB | Calibración de amplitudes |

**Corrección de amplitud:** cada ventana atenúa la señal; la amplitud del pico debe dividirse por la **ganancia coherente** CG \( = \sum_n w_n / N \):
- Rectangular: CG = 1.0
- Hann: CG = 0.5
- Blackman: CG ≈ 0.42

$$ A_k = \frac{2|X_k|}{N \cdot \text{CG}} = \frac{2|X_k|}{\sum_n w_n} $$

Sin esta corrección, la THD calculada puede estar subestimada en un factor de 2 (para ventana Hann).

## 4 — STFT y espectrograma: análisis tiempo-frecuencia

La **STFT (Short-Time Fourier Transform)** aplica la FFT a ventanas deslizantes de longitud \( L \) con solapamiento \( H \) (hop size), obteniendo un espectro local para cada posición temporal:

$$ X(n, k) = \sum_{m=0}^{L-1} x(nH + m)\, w(m)\, e^{-j2\pi km/L} $$

El **compromiso tiempo-frecuencia** es fundamental: ventanas cortas (\( L \) pequeño) dan buena resolución temporal pero mala frecuencial; ventanas largas dan buena resolución frecuencial pero mala temporal. Este trade-off es el principio de incertidumbre de Heisenberg-Gabor:

$$ \Delta t \cdot \Delta f \geq \frac{1}{4\pi} $$

**Parámetros típicos para análisis de convertidores:**
- Resolución frecuencial < 5 Hz: \( L > f_s / 5 \). Para \( f_s = 10\,\text{kHz} \): \( L > 2000 \) muestras.
- Resolución temporal < 10 ms: \( H < 100 \) muestras.
- Solapamiento del 75%: buen compromiso entre densidad temporal y suavidad del espectrograma.

**Aplicación:** detectar interarmónicos (frecuencias no múltiplo de \( f_1 \)) en convertidores durante transitorios, e.g., la frecuencia de oscilación de un modo SSO (Sub-Synchronous Oscillation) que aparece durante un transitorio de red.

## 5 — Welch y PSD: estimación robusta del espectro de potencia

El **periodograma de Welch** reduce la varianza del estimador espectral dividiendo la señal en \( K \) segmentos con solapamiento del 50%, calculando el periodograma de cada uno y promediando:

$$ \hat{S}_{Welch}(f_k) = \frac{1}{K} \sum_{i=1}^{K} |X_i(f_k)|^2 $$

La varianza del estimador se reduce en un factor \( \approx K/1.5 \) respecto al periodograma simple (el 1.5 es el factor de solapamiento del 50%). Con \( K = 10 \) segmentos, la varianza se reduce ~6.7 veces, equivalente a la desviación estándar dividida por \( \sqrt{6.7} \approx 2.6 \).

**PSD (Power Spectral Density):** el Welch da la PSD en unidades de \( \text{V}^2/\text{Hz} \) o \( \text{A}^2/\text{Hz} \). Para señales de ruido estacionario es el estimador estándar; para armónicos deterministas, el periodograma de una sola ventana larga es mejor (no tiene ruido aleatorio que promediar).

```python
from scipy.signal import welch
f, Pxx = welch(x, fs=fs, window='hann', nperseg=1024, noverlap=512)
# Pxx en V²/Hz; para amplitud RMS: sqrt(Pxx * df)
```

## 6 — SSO e interarmónicos en convertidores PWM

Los convertidores de potencia generan un espectro específico que el análisis FFT debe identificar correctamente:

**Armónicos de conmutación:** en un VSC de dos niveles con portadora triangular a \( f_{sw} \), el espectro de la tensión de salida (antes del filtro) tiene componentes a:

$$ f_{h} = m \cdot f_{sw} \pm n \cdot f_1, \quad m = 1, 2, 3, \ldots;\; n = 0, 1, 2, \ldots $$

Las bandas laterales más importantes son \( f_{sw} \pm 2f_1 \) (índice de modulación impar) y \( 2f_{sw} \pm f_1 \).

**Interarmónicos y SSO:** las oscilaciones sub-síncronas (SSO) generan componentes a frecuencias como \( f_1 \pm f_{SSO} \) (p.ej. 50 ± 12 Hz = 38 Hz y 62 Hz). Estas componentes no son múltiplos de \( f_1 \) — son interarmónicos. Para detectarlas se necesita \( \Delta f < f_{SSO}/10 \approx 1.2\,\text{Hz} \Rightarrow T > 833\,\text{ms} \) de registro.

**Ventana de 10 ciclos (IEC 61000-4-7):** para medición normativa de armónicos de red, se usa una ventana de exactamente 10 ciclos de \( f_1 \) (200 ms a 50 Hz). Esta es la ventana de muestreo coherente que pone toda la energía fundamental en un único bin y separa perfectamente los armónicos 50, 100, 150... Hz.

$$ \boxed{T_{ventana} = 10/f_1 = 200\,\text{ms (50 Hz)};\quad \Delta f = 1/T = 5\,\text{Hz};\quad\text{armónicos en bins }k=1,2,3,\ldots} $$

<div class="cfig"><img src="../figuras/fft-analisis-espectral-analisis.png" alt="comparativa ventanas, espectrograma STFT, PSD Welch y espectro de convertidor PWM"><div class="cap">Análisis espectral avanzado: comparativa de ventanas (Rectangular vs Hann vs Blackman) mostrando el leakage, espectrograma STFT de un transitorio, PSD de Welch vs periodograma simple, y espectro de un convertidor PWM con armónicos de conmutación y bandas laterales.</div></div>

## 7 — Implementacion Python completa para medicion normativa de THD

```python
import numpy as np

def calcular_thd_normativo(i_pcc, fs, f1=50.0, N_ciclos=10, h_max=50):
    """
    Calcula THD de corriente segun IEC 61000-4-7 con ventana de N ciclos.

    Parametros
    ----------
    i_pcc : array, corriente en el PCC muestreada a fs Hz
    fs    : float, frecuencia de muestreo (Hz)
    f1    : float, frecuencia fundamental (Hz, def. 50)
    N_ciclos : int, numero de ciclos de f1 en la ventana (def. 10)
    h_max : int, maximo orden armonico a calcular (def. 50)

    Retorna
    -------
    dict con: THD_pct, I1, Ih (array de amplitudes), frecuencias
    """
    N = int(round(N_ciclos * fs / f1))
    if len(i_pcc) < N:
        raise ValueError(f"Se necesitan >= {N} muestras, se tienen {len(i_pcc)}")

    # usar el ultimo bloque de N muestras (regimen permanente)
    x = i_pcc[-N:]

    # muestreo coherente si fs es multiplo de f1 (ideal)
    # de lo contrario, ventana Hann para reducir leakage
    coherente = abs((fs / f1) - round(fs / f1)) < 0.01
    if coherente:
        w = np.ones(N)
        ganancia = N
    else:
        w = np.hanning(N)
        ganancia = np.sum(w)

    X = np.fft.rfft(x * w)
    f_bins = np.fft.rfftfreq(N, 1.0/fs)
    amps = 2.0 * np.abs(X) / ganancia

    # fundamental
    idx1 = np.argmin(np.abs(f_bins - f1))
    I1 = amps[idx1]

    # armonicos 2..h_max
    Ih = np.zeros(h_max - 1)
    f_harm = np.zeros(h_max - 1)
    for h in range(2, h_max + 1):
        fh = h * f1
        idx_h = np.argmin(np.abs(f_bins - fh))
        Ih[h - 2] = amps[idx_h]
        f_harm[h - 2] = fh

    THD_pct = np.sqrt(np.sum(Ih**2)) / I1 * 100

    return {
        'THD_pct': THD_pct,
        'I1': I1,
        'Ih': Ih,
        'f_harm': f_harm,
        'pass_thd': THD_pct < 5.0,
        'pass_individual': all(Ih[:9] / I1 * 100 < 4.0),  # h<11: limite 4%
        'coherente': coherente,
    }

# Verificar cumplimiento IEEE 519-2022
def verificar_ieee519(Ih_pct, h_orders, Isc_IL_ratio):
    """
    Compara cada armonico con el limite individual de IEEE 519-2022.
    Isc_IL_ratio = I_cortocircuito / I_carga
    """
    if Isc_IL_ratio < 20:
        limites = {(0,11): 4.0, (11,17): 2.0, (17,23): 1.5, (23,35): 0.6, (35,1000): 0.3}
    elif Isc_IL_ratio < 50:
        limites = {(0,11): 7.0, (11,17): 3.5, (17,23): 2.5, (23,35): 1.0, (35,1000): 0.5}
    else:
        limites = {(0,11): 12.0, (11,17): 5.5, (17,23): 5.0, (23,35): 2.0, (35,1000): 1.0}

    resultados = []
    for h, Ih in zip(h_orders, Ih_pct):
        lim = next(v for (a,b), v in limites.items() if a < h <= b)
        resultados.append({'h': h, 'Ih_pct': Ih, 'limite': lim, 'pass': Ih <= lim})
    return resultados
```

## 8 — Aplicacion en medicion de impedancia por inyeccion

La FFT es la base del metodo de medicion de impedancia por inyeccion de pequena senal (ver [[medicion-impedancia-inyeccion]]). El proceso es:

1. Inyectar una senal de perturbacion de pequena amplitud \( v_{inj}(t) = A_{inj} \sin(2\pi f_{inj} t) \) en el lazo de tension o de corriente.
2. Medir la respuesta \( \Delta v(t) \) y \( \Delta i(t) \) con alta resolucion frecuencial.
3. Calcular la impedancia en la frecuencia de inyeccion:

$$ Z(f_{inj}) = \frac{\Delta V(f_{inj})}{\Delta I(f_{inj})} = \frac{\text{FFT}[\Delta v](f_{inj})}{\text{FFT}[\Delta i](f_{inj})} $$

La precision del resultado depende de:
- **Amplitud de la inyeccion:** debe ser suficientemente pequena para no excitar la no linealidad (\( < 5\,\% \) de la amplitud de la fundamental) pero suficientemente grande para tener una buena SNR (\( > 20\,\text{dB} \)).
- **Coherencia de la ventana:** el numero de periodos de la senal de inyeccion en la ventana debe ser entero para evitar leakage.
- **Promediado:** promediar varias mediciones reduce la varianza del estimador y elimina el efecto del ruido de medicion.

La funcion `calcular_thd_normativo` anterior puede adaptarse directamente para la medicion de impedancia cambiando la senyal de entrada por \( \Delta v \) o \( \Delta i \).
