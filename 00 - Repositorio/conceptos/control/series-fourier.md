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

## Conceptos relacionados
- [[fft-analisis-espectral]] · [[transformada-laplace]] · [[diagrama-bode]] · [[calidad-potencia]] · [[muestreo-aliasing]]

## Referencias
- Oppenheim & Willsky, *Señales y Sistemas*.
