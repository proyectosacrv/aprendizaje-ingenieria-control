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
fecha_actualizacion: 2026-06-09
relacionados: [medicion-impedancia-inyeccion, modulacion-pwm, diagrama-bode, respuesta-frecuencia-ss]
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

## Cuándo y por qué se usa
Para verificar calidad de onda (armónicos de [[modulacion-pwm|PWM]]), validar modelos contra
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
- [[medicion-impedancia-inyeccion]] · [[modulacion-pwm]] · [[respuesta-frecuencia-ss]] · [[diagrama-bode]]

## Referencias
- Oppenheim, Schafer, *Discrete-Time Signal Processing*.
- Harris, *On the Use of Windows for Harmonic Analysis with the DFT*, 1978.
