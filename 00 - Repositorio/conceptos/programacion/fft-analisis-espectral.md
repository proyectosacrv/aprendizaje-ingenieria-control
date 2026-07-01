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
