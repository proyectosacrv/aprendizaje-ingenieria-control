---
titulo: Series y transformada de Fourier
slug: series-fourier
categoria: control
tipo: concepto
nivel: basico
proyectos: []
objetivos: [descomponer señales en armónicos y razonar en el dominio de la frecuencia]
tags: [fourier, armonicos, espectro, frecuencia, basico]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-07-01
relacionados: [fft-analisis-espectral, transformada-laplace, diagrama-bode, calidad-potencia, muestreo-aliasing]
referencias:
  - "Oppenheim & Willsky, Señales y Sistemas, Prentice Hall"
---

## Definición
Toda señal **periódica** puede escribirse como suma de senoides cuyas frecuencias son múltiplos de
la fundamental: los **armónicos**. La **serie de Fourier** da esos coeficientes; la **transformada
de Fourier** extiende la idea a señales no periódicas, dando su **espectro** (contenido en
frecuencia).

## Fundamento teórico
Serie de Fourier de una señal de periodo \( T \) (\( \omega_0 = 2\pi/T \)):
$$ x(t) = \sum_{k=-\infty}^{\infty} c_k\,e^{jk\omega_0 t}, \qquad
   c_k = \frac{1}{T}\int_0^T x(t)\,e^{-jk\omega_0 t}\,dt $$
\( |c_k| \) es la amplitud del armónico \( k \). Para señales no periódicas, la **transformada de
Fourier**:
$$ X(j\omega) = \int_{-\infty}^{\infty} x(t)\,e^{-j\omega t}\,dt $$
Es el caso particular de la transformada de Laplace evaluada en el eje imaginario \( s = j\omega \):
por eso la respuesta en frecuencia (Bode) es \( G(j\omega) \). El teorema de Parseval relaciona la
energía en tiempo y en frecuencia.

<div class="cfig"><img src="figuras/series-fourier-cuadrada.png" alt="reconstruccion de una onda cuadrada con armonicos"><div class="cap">Una onda cuadrada es la suma de sus armónicos impares (amplitud ∝1/k): con más términos la aproximación mejora; el rizado de los flancos es el fenómeno de Gibbs.</div></div>

## 1 — Derivación de los coeficientes cn por ortogonalidad

**Paso 1 — ortogonalidad de los exponenciales complejos.** Las funciones \( e^{jn\omega_0 t} \) son ortogonales en el intervalo \( [0,T] \):

$$ \frac{1}{T}\int_0^T e^{jn\omega_0 t}\,e^{-jm\omega_0 t}\,dt = \frac{1}{T}\int_0^T e^{j(n-m)\omega_0 t}\,dt = \begin{cases}1 & n=m \\ 0 & n\neq m\end{cases} $$

Para \( n\neq m \), la integral de una exponencial compleja de periodo exactamente \( T/(n-m) \) sobre un número entero de periodos es cero.

**Paso 2 — multiplicar la serie por \( e^{-jm\omega_0 t} \) e integrar.** Partiendo de \( x(t)=\sum_{k=-\infty}^{\infty}c_k e^{jk\omega_0 t} \), se multiplican ambos lados por \( e^{-jm\omega_0 t} \) y se integra sobre un periodo:

$$ \frac{1}{T}\int_0^T x(t)\,e^{-jm\omega_0 t}\,dt = \sum_{k=-\infty}^{\infty}c_k\underbrace{\frac{1}{T}\int_0^T e^{j(k-m)\omega_0 t}\,dt}_{=\,\delta_{km}} = c_m $$

**Paso 3 — resultado.** Renombrando \( m\to n \):

$$ \boxed{c_n = \frac{1}{T}\int_0^T x(t)\,e^{-jn\omega_0 t}\,dt} $$

## 2 — THD desde los coeficientes de Fourier

**Paso 1 — potencia por armónico (Parseval).** La potencia media de \( x(t) \) es \( \sum_k |c_k|^2 \). La potencia de la fundamental es \( |c_1|^2+|c_{-1}|^2=2|c_1|^2 \) (para señal real \( c_{-k}=c_k^* \), así que \( |c_1|=|c_{-1}| \)).

**Paso 2 — definir THD.** El THD (Total Harmonic Distortion) es la razón entre la potencia de todos los armónicos \( k\ge2 \) y la de la fundamental:

$$ \mathrm{THD} = \frac{\sqrt{\displaystyle\sum_{k=2}^{\infty}|a_k|^2}}{|a_1|} $$

donde \( a_k \) son las amplitudes de los armónicos en forma real (\( a_k=2|c_k| \) para señal real).

**Paso 3 — ejemplo: onda cuadrada.** Para una onda cuadrada de amplitud 1, los coeficientes son \( c_k=2/(jk\pi) \) para \( k \) impar, cero para \( k \) par. La amplitud del armónico \( k \) impar es \( |a_k|=4/(k\pi) \). El THD resulta:

$$ \mathrm{THD}=\frac{\sqrt{\sum_{k=3,5,7,\dots}(4/(k\pi))^2}}{4/\pi}=\sqrt{\sum_{k=3,5,\dots}\frac{1}{k^2}}\bigg/1 \approx 48.1\,\% $$

(valor numérico obtenido con los primeros 100 armónicos impares).

## Cuándo y por qué se usa
Para cuantificar **armónicos** y distorsión (THD), para entender el espectro de una señal medida,
para la **respuesta en frecuencia** de un sistema, y como base de la FFT (su versión discreta y
calculable).

## Procedimiento de diseño (genérico)
1. Identifica el periodo \( T \) (o trata la señal como aperiódica).
2. Calcula los coeficientes \( c_k \) (analítico) o usa la FFT (numérico).
3. Interpreta el espectro: fundamental, armónicos, su amplitud y fase.

## Ejemplo de código
```python
import numpy as np
N = 1024; t = np.linspace(0, 1, N, endpoint=False)
x = np.sign(np.sin(2*np.pi*50*t))         # onda cuadrada 50 Hz
C = np.fft.rfft(x)/N                       # coeficientes (armonicos impares 1,3,5...)
```

## Parámetros y valores típicos
Una onda cuadrada solo tiene armónicos impares con amplitud \( \propto 1/k \). El PWM concentra
energía en torno a \( f_{sw} \) y sus bandas laterales. La fundamental de red es 50/60 Hz.

## Errores comunes
- Confundir serie (periódica, espectro discreto) con transformada (aperiódica, espectro continuo).
- Fuga espectral al usar FFT con ventana no entera de periodos (ver [[muestreo-aliasing]]).
- Olvidar que un sistema lineal solo escala/desfasa cada armónico (no crea frecuencias nuevas).

## 3 — Cálculo de coeficientes paso a paso

Tomamos la señal cuadrada de periodo \( T \), amplitud ±1: \( x(t) = \text{sgn}(\sin(\omega_0 t)) \), con \( \omega_0 = 2\pi/T \). Por simetría impar solo hay coeficientes de seno. Calculando \( b_n \) directamente:

$$ b_n = \frac{2}{T}\int_0^T x(t)\sin(n\omega_0 t)\,dt = \frac{4}{n\pi} \quad (n \text{ impar}), \qquad b_n = 0 \quad (n \text{ par}) $$

La serie resultante es:
$$ x(t) = \frac{4}{\pi}\!\left(\sin\omega_0 t + \frac{1}{3}\sin 3\omega_0 t + \frac{1}{5}\sin 5\omega_0 t + \cdots\right) $$

**Fenómeno de Gibbs.** En las discontinuidades de la señal cuadrada, la suma parcial de \( N \) términos presenta una sobreoscilación de aproximadamente el 9 % de la amplitud, independientemente del número de armónicos \( N \). Aumentar \( N \) reduce la anchura del pico pero no su altura: es un comportamiento intrínseco de la convergencia puntual de series de Fourier en discontinuidades.

## 4 — Transformada de Fourier y serie: relación

**Serie vs. transformada.** Para una señal periódica de periodo \( T \), la serie de Fourier genera un espectro **discreto** con líneas en \( f_n = n/T \) (armónicos). Para una señal aperiódica, la transformada de Fourier produce un espectro **continuo**:
$$ X(f) = \int_{-\infty}^{\infty} x(t)\,e^{-j2\pi ft}\,dt $$

**Teorema de Parseval.** La energía se conserva entre dominios:
$$ \frac{1}{T}\int_0^T x^2(t)\,dt = \sum_{n=-\infty}^{\infty} |c_n|^2 $$
La potencia media en tiempo es igual a la suma de las potencias de todos los armónicos.

**RMS a partir de la serie.** Usando Parseval directamente:
$$ X_{rms} = \sqrt{\sum_{n=-\infty}^{\infty} |c_n|^2} = \sqrt{|c_0|^2 + 2\sum_{n=1}^{\infty}|c_n|^2} $$
para señal real (donde \( c_{-n} = c_n^* \)). Esto permite calcular el RMS de una señal armónica sin integrar en tiempo.

## 5 — DFT y FFT en Python

**DFT.** La versión discreta de la transformada de Fourier:
$$ X[k] = \sum_{n=0}^{N-1} x[n]\,e^{-j2\pi kn/N}, \qquad k = 0, 1, \ldots, N-1 $$

**FFT.** El algoritmo de Cooley-Tukey reduce el coste de la DFT de \( O(N^2) \) a \( O(N \log N) \) cuando \( N \) es potencia de dos. En Python, `numpy.fft.rfft` calcula la mitad positiva del espectro para señales reales.

**Resolución frecuencial.** \( \Delta f = f_s/N \). Para mejorar la resolución se aumenta \( N \) (más muestras) o se reduce \( f_s \) (menor frecuencia de muestreo), con el compromiso habitual de aliasing.

**Leakage espectral.** Si la señal no es exactamente periódica en la ventana de análisis (duración \( N/f_s \)), la energía del pico se "derrama" hacia frecuencias adyacentes. Solución: multiplicar por una ventana (Hanning, Blackman) antes de la FFT; se sacrifica resolución frecuencial a cambio de minimizar el leakage.

## 6 — Aplicación en análisis de armónicos de convertidores

**Espectro de una señal PWM.** Una señal PWM con índice de modulación \( m \) y frecuencia de conmutación \( f_{sw} \) contiene:
- Componente fundamental a \( f_0 = 50 \) Hz (o 60 Hz).
- Portadora y sus armónicos en \( f_{sw} \), \( 2f_{sw} \), ...
- Bandas laterales en \( f_{sw} \pm k f_0 \), \( 2f_{sw} \pm k f_0 \), ..., donde \( k \) es impar para PWM sinusoidal.

**Ventana de análisis.** Para resolver la fundamental con precisión se necesitan al menos \( N_{ciclos} \geq 10 \) períodos de la fundamental. Con \( f_0 = 50 \) Hz y \( f_s = 20\,\text{kHz} \), una ventana de 0.1 s contiene 5 ciclos de fundamental y 2000 puntos: suficiente para resolver hasta \( f_{sw}/2 \).

**Armónicos subsincrónicos (SSO).** En sistemas HVDC y parques eólicos, frecuencias entre 10 y 45 Hz (subsincrónicos) pueden excitar modos de oscilación del sistema mecánico o del control. La FFT con ventana larga (varios segundos) permite identificarlos con resolución suficiente para distinguirlos de la fundamental.

**Herramienta en Python:**
```python
from scipy.fft import rfft, rfftfreq
X = rfft(x_signal)
freqs = rfftfreq(len(x_signal), 1/fs)
amplitude = np.abs(X) * 2 / len(x_signal)
```

<div class="cfig"><img src="figuras/series-fourier-analisis.png" alt="Reconstruccion de Fourier, espectro de amplitudes, FFT de PWM y efecto de ventana"><div class="cap">Superior izquierdo: reconstrucción de la onda cuadrada con 1, 5 y 20 armónicos — el fenómeno de Gibbs persiste en los flancos. Superior derecho: espectro de amplitudes (solo armónicos impares, decaimiento 1/n). Inferior izquierdo: espectro FFT de una señal PWM con portadora a 2 kHz y bandas laterales. Inferior derecho: efecto de la ventana — rectangular genera leakage severo; Hanning lo suprime.</div></div>

## Conceptos relacionados
- [[fft-analisis-espectral]] · [[transformada-laplace]] · [[diagrama-bode]] · [[calidad-potencia]] · [[muestreo-aliasing]]

## Referencias
- Oppenheim & Willsky, *Señales y Sistemas*.
