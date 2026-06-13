---
titulo: Armónicos y THD en convertidores
slug: armonicos-thd-convertidores
categoria: fisica-modelado
tipo: fenomeno
nivel: intermedio
proyectos: []
objetivos: [cuantificar la distorsión que inyecta el convertidor y cumplir códigos de red]
tags: [armonicos, thd, pwm, calidad-potencia, ieee-519, tiempo-muerto, conmutacion, modelado]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-06-10
relacionados: [modulacion-pwm, calidad-potencia, fft-analisis-espectral, filtro-lcl, controlador-resonante, estabilidad-armonica, valor-rms-factor-potencia]
referencias:
  - "Mohan, Undeland, Robbins, Power Electronics, Wiley"
  - "IEEE Std 519-2014, Harmonic Control in Electric Power Systems"
---

## Definición
Componentes de frecuencia múltiplo (o no) de la fundamental que el convertidor inyecta por la
**conmutación** y por **no idealidades**. La **THD** (Total Harmonic Distortion) resume su peso
relativo frente a la fundamental y es la métrica que fijan los códigos de red.

## Fundamento teórico
Para una señal con fundamental \( X_1 \) y armónicos \( X_h \):
$$ \text{THD}=\frac{\sqrt{\sum_{h\ge2}X_h^2}}{X_1}\times100\% $$
Dos familias de armónicos:
- **De conmutación (alta frecuencia):** la [[modulacion-pwm|PWM]] sinusoidal genera bandas laterales
  centradas en \( m_f f_1 \) y sus múltiplos, con \( m_f=f_{sw}/f_1 \). Aparecen en \( m_f\pm2,\,m_f\pm4,\dots \)
  y \( 2m_f\pm1,\dots \). Los atenúa el [[filtro-lcl|filtro LCL]].
- **De baja frecuencia (5º, 7º, 11º, 13º…):** vienen de **no idealidades**: tiempo muerto, caída en los
  IGBT, distorsión de la tensión de red, desbalance. El tiempo muerto \( t_d \) introduce un error de
  tensión casi cuadrado en fase con la corriente:
  $$ \Delta V\approx\frac{t_d\,f_{sw}}{T_{sw}/2}\,V_{dc}\;\text{(error de volt-seg por conmutación)} $$
  que se proyecta sobre todo en 5º y 7º. En trifásico equilibrado los **triples** (3º, 9º…) son de
  secuencia homopolar y no circulan sin neutro.

Códigos tipo **IEEE 519** limitan THD de corriente (TDD) en función de la \( I_{sc}/I_L \) del punto de
conexión, y la tensión a \( \le5\% \) THD en BT/MT.

<div class="cfig"><img src="figuras/armonicos-thd-convertidores-espectro.png" alt="espectro de un convertidor PWM con bajos ordenes y bandas de conmutacion"><div class="cap">Espectro típico: junto a la fundamental aparecen armónicos de bajo orden (5º, 7º…) que vienen de no idealidades como el tiempo muerto, y las bandas de conmutación centradas en $m_f f_1$ y sus múltiplos. El filtro LCL atenúa las bandas de alta frecuencia; los bajos órdenes se compensan con resonantes y compensación de tiempo muerto.</div></div>

## Cuándo y por qué se usa
Para **dimensionar el filtro** de salida (qué atenuación hace falta en \( f_{sw} \)), **cumplir el código
de red**, y diagnosticar resonancias: si un armónico coincide con la resonancia LCL o de la red puede
amplificarse ([[estabilidad-armonica]]). También guía el uso de [[controlador-resonante|controladores resonantes]]
para cancelar 5º/7º.

## Procedimiento de diseño (genérico)
1. Identifica el espectro esperado: bandas en \( m_f f_1 \) (PWM) + bajos órdenes (tiempo muerto, red).
2. Fija el límite aplicable (IEEE 519 / código local) según \( I_{sc}/I_L \).
3. Dimensiona el [[filtro-lcl]] para cumplir en \( f_{sw} \) y sitúa su resonancia lejos de armónicos.
4. Compensa los bajos órdenes: compensación de tiempo muerto + [[controlador-resonante|resonantes]] en 5º/7º.
5. Verifica con [[fft-analisis-espectral|FFT]] sobre la corriente simulada/medida que el TDD cumple.

## Ejemplo de aplicación real
**Problema:** inversor con \( f_1=50\,\text{Hz} \), \( f_{sw}=5\,\text{kHz} \), \( t_d=2\,\mu\text{s} \),
\( V_{dc}=700\,\text{V} \). ¿Dónde caen los armónicos de conmutación y cuánto distorsiona el tiempo muerto?

Índice de frecuencia \( m_f=5000/50=100 \): el primer grupo de armónicos PWM está en torno a
\( 100\times50=5\,\text{kHz} \) (laterales en \( 98,102\to4.9,5.1\,\text{kHz} \)) — fácil de filtrar con LCL.
El tiempo muerto da un error de volt-segundo por conmutación de
\( \Delta V\approx t_d f_{sw} V_{dc}=2\times10^{-6}\times5000\times700\approx7\,\text{V} \) sobre la
fundamental (\( \approx \)286 V pico), es decir \( \sim2.4\% \) concentrado en 5º/7º. Sin compensación de
tiempo muerto, esos bajos órdenes dominan la THD aunque el LCL esté perfecto.

## Ejemplo de código
```python
import numpy as np
def thd(signal, fs, f1):
    N = len(signal); X = np.abs(np.fft.rfft(signal*np.hanning(N)))/N
    f = np.fft.rfftfreq(N, 1/fs)
    k1 = np.argmin(abs(f-f1)); fund = X[k1]
    harm = np.sqrt(sum(X[np.argmin(abs(f-h*f1))]**2 for h in range(2,41)))
    return 100*harm/fund
```

## Parámetros y valores típicos
THD de corriente objetivo en red: < 5 % (TDD por IEEE 519). \( m_f=f_{sw}/f_1 \): 40–400. Tiempo muerto:
1–3 µs (genera 1–3 % de bajos órdenes). Atenuación LCL en \( f_{sw} \): 20–40 dB.

## Errores comunes
- Mirar solo la THD global e ignorar que un **único** armónico (p. ej. 5º) viola el límite individual.
- Situar la resonancia LCL sobre un armónico → amplificación en vez de atenuación.
- FFT sin ventana ni número entero de ciclos → fugas espectrales que falsean la THD.
- Despreciar el tiempo muerto en el modelo: la THD simulada sale mucho mejor que la real.

## Conceptos relacionados
- [[modulacion-pwm]] · [[calidad-potencia]] · [[fft-analisis-espectral]] · [[filtro-lcl]] · [[controlador-resonante]] · [[estabilidad-armonica]]

## Referencias
- Mohan, Undeland, Robbins, *Power Electronics*.
- IEEE Std 519-2014.
