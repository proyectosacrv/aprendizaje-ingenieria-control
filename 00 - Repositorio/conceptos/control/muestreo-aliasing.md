---
titulo: Muestreo y aliasing (teorema de Nyquist-Shannon)
slug: muestreo-aliasing
categoria: control
tipo: concepto
nivel: basico
proyectos: [01-GFM-Impedance]
objetivos: [elegir la frecuencia de muestreo y evitar el solapamiento espectral]
tags: [muestreo, aliasing, nyquist-shannon, adc, control-digital, basico]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-06-10
relacionados: [transformada-z, fft-analisis-espectral, discretizacion-controladores, modulacion-pwm, series-fourier]
referencias:
  - "Oppenheim & Willsky, Señales y Sistemas, Prentice Hall"
---

## Definición
Muestrear es tomar valores de una señal continua a intervalos regulares \( T_s \) (frecuencia
\( f_s = 1/T_s \)). El **teorema de Nyquist-Shannon** dice cuándo esas muestras bastan para
reconstruir la señal sin perder información; si no se cumple, aparece **aliasing** (una frecuencia
alta se "disfraza" de una baja).

## Fundamento teórico
Al muestrear, el espectro de la señal se **repite** cada \( f_s \). Para que las réplicas no se
solapen, todo el contenido debe estar por debajo de la **frecuencia de Nyquist** \( f_s/2 \):
$$ f_s > 2\,f_{\max} $$
Si una componente de frecuencia \( f > f_s/2 \) se muestrea, aparece como un **alias** a
$$ f_{\text{alias}} = \lvert\, f - k\,f_s \,\rvert,\quad k\in\mathbb{Z} $$
indistinguible de una señal real de esa frecuencia baja. Por eso, antes del conversor A/D se pone un
**filtro antialiasing** (paso-bajo analógico) que corta por encima de \( f_s/2 \).

## Cuándo y por qué se usa
En todo control digital (elegir \( f_s \) del lazo), en la FFT (la malla temporal fija qué
frecuencias se pueden ver), en la simulación conmutada (el paso debe resolver \( f_{sw} \)) y en la
medición de impedancia por inyección (la ventana define la resolución).

## Procedimiento de diseño (genérico)
1. Determina la frecuencia máxima de interés \( f_{\max} \).
2. Elige \( f_s \ge 2 f_{\max} \) con margen práctico (5–10×) para no quedar al límite.
3. Coloca un filtro antialiasing analógico con corte \( < f_s/2 \) antes del muestreo.
4. En la FFT, usa una ventana de un número **entero** de periodos para no introducir fugas.

## Ejemplo de código
```python
import numpy as np
fs = 1000.0                      # muestreo a 1 kHz -> Nyquist 500 Hz
t = np.arange(0, 1, 1/fs)
x = np.sin(2*np.pi*900*t)        # 900 Hz > 500 Hz -> se vera como alias de 100 Hz
# |900 - 1000| = 100 Hz
```

## Parámetros y valores típicos
En convertidores, \( f_s \) del control suele coincidir con \( f_{sw} \) (p.ej. 10 kHz) o
\( f_{sw}/2 \); el muestreo se sincroniza con el pico/valle de la portadora PWM para promediar el
rizado de conmutación de forma natural.

## Errores comunes
- Muestrear sin filtro antialiasing: el ruido de alta frecuencia se pliega sobre la banda útil.
- Olvidar que el rizado de conmutación (a \( f_{sw} \)) puede aliasar si \( f_s = f_{sw} \) sin sincronizar.
- En FFT, ventana no entera de periodos \( \to \) fuga espectral (leakage).

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: medir impedancia por inyección): la ventana de demodulación se
  ajusta a un número entero de periodos de la perturbación para extraer el fasor sin fuga.

## Conceptos relacionados
- [[transformada-z]] · [[fft-analisis-espectral]] · [[discretizacion-controladores]] · [[modulacion-pwm]] · [[series-fourier]]

## Referencias
- Oppenheim & Willsky, *Señales y Sistemas*.
