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
fecha_actualizacion: 2026-06-10
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
