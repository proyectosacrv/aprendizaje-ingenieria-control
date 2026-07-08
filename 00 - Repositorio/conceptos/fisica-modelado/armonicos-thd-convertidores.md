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
fecha_actualizacion: 2026-06-30
relacionados: [convertidor-vsc, calidad-potencia, fft-analisis-espectral, filtro-lcl, controlador-resonante, fenomenos-oscilatorios-red, valor-rms-factor-potencia]
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
- **De conmutación (alta frecuencia):** la [[convertidor-vsc|PWM]] sinusoidal genera bandas laterales
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

## 1 — De dónde sale la definición de THD
**Paso 1 — descomponer la señal en armónicos.** Una corriente periódica no senoidal se expande en serie de Fourier como suma de la fundamental más sus armónicos (ver [[series-fourier]]):

$$ i(t)=\sum_{h\ge1}\sqrt2\,I_h\sin(h\omega t+\phi_h)=\underbrace{\sqrt2\,I_1\sin(\omega t+\phi_1)}_{\text{fundamental}}+\underbrace{\sum_{h\ge2}\sqrt2\,I_h\sin(h\omega t+\phi_h)}_{\text{distorsión}} $$

donde \( I_h \) es el **RMS** del armónico de orden \( h \).

**Paso 2 — el RMS total se reparte por armónico.** El valor eficaz del conjunto es \( I_{rms}^2=\tfrac1T\int_0^T i^2\,dt \). Al elevar al cuadrado la suma aparecen los términos propios \( I_h^2 \) y los cruzados \( I_hI_k \) (\( h\ne k \)). Por **ortogonalidad** de los senos de distinta frecuencia, todo término cruzado promedia cero sobre un periodo (igual que en [[valor-rms-factor-potencia]]). Sobreviven solo los cuadrados:

$$ I_{rms}^2=\sum_{h\ge1}I_h^2=I_1^2+\sum_{h\ge2}I_h^2 $$

**Paso 3 — separar fundamental y distorsión.** Define el RMS de distorsión como todo lo que no es fundamental:

$$ I_{dist}=\sqrt{\sum_{h\ge2}I_h^2}\quad\Longrightarrow\quad I_{rms}^2=I_1^2+I_{dist}^2 $$

**Paso 4 — normalizar frente a la fundamental.** La THD es ese RMS de distorsión expresado como fracción de la fundamental:

$$ \boxed{\;\text{THD}=\frac{I_{dist}}{I_1}=\frac{\sqrt{\sum_{h\ge2}I_h^2}}{I_1}\times100\%\;} $$

De aquí sale también el **factor de distorsión** que degrada el factor de potencia: dividiendo \( I_{rms}^2=I_1^2+I_{dist}^2 \) entre \( I_1^2 \) y tomando la raíz, \( I_{rms}/I_1=\sqrt{1+\text{THD}^2} \), de modo que \( I_1/I_{rms}=1/\sqrt{1+\text{THD}^2} \) es el factor por el que la distorsión reduce el FP frente al \( \cos\varphi \) de la fundamental. Por eso con armónicos \( \mathrm{FP}<\cos\varphi \). La integral del Paso 2 es exactamente la que ejecuta la FFT del ejemplo de código.

## Cuándo y por qué se usa
Para **dimensionar el filtro** de salida (qué atenuación hace falta en \( f_{sw} \)), **cumplir el código
de red**, y diagnosticar resonancias: si un armónico coincide con la resonancia LCL o de la red puede
amplificarse ([[fenomenos-oscilatorios-red|estabilidad armónica]]). También guía el uso de [[controlador-resonante|controladores resonantes]]
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

## 3 — Origen de los armónicos en convertidores PWM

**Bandas laterales de la frecuencia de conmutación.** La modulación PWM sinusoidal genera un
espectro de tensión en la salida del VSC con componentes en:

$$ f_{harm} = m\,f_{sw} \pm k\,f_0 \quad m=1,2,3\ldots;\; k=0,1,2,3\ldots $$

Para \( f_{sw}=10\,\text{kHz} \), \( f_0=50\,\text{Hz} \): el primer grupo de armónicos cae en
torno a 10 kHz (laterales a 9950, 10050 Hz), el segundo en torno a 20 kHz (19950, 20050 Hz), etc.
Estas frecuencias son fácilmente filtradas por el filtro LCL, que atenúa a razón de –60 dB/década
por encima de su resonancia.

**Índice de modulación de frecuencia \( m_f \).** Para \( m_f = f_{sw}/f_0 \) impar y múltiplo de
3 (e.g. \( m_f=21, 39, 57 \)), los armónicos de conmutación recaen en frecuencias que no son
múltiplos de 3 de \( f_0 \) — ventaja para el trifásico porque los triples no circulan sin neutro.

**Armónicos de bajo orden (5°, 7°, 11°, 13°…).** No vienen del PWM sino de las no idealidades:

1. **Tiempo muerto (dead time).** Para evitar cortocircuitos en el semipuente, se introduce un
   retardo \( t_d \) (1–4 µs) entre el apagado de un IGBT y el encendido del otro. Durante \( t_d \),
   la tensión de fase queda indeterminada y depende del signo de la corriente. El error de tensión
   es aproximadamente cuadrado, en fase con la corriente:
   $$ \Delta V_h \approx \frac{4\,V_{dc}\,t_d\,f_{sw}}{\pi\,h} \qquad h=5,7,11,13\ldots $$
   (solo armónicos impares no triples). Con \( V_{dc}=700\,\text{V} \), \( t_d=2\,\mu\text{s} \),
   \( f_{sw}=10\,\text{kHz} \): \( \Delta V_5 \approx 11.2\,\text{V} \), que sobre 286 V pico es
   ~3.9% de 5° armónico.

2. **Caída en los IGBTs.** La caída de saturación \( V_{CE,sat} \) y la caída en los diodos de
   antiparalelo también distorsionan la tensión de salida. Menos importante que el dead time en
   sistemas de alta potencia.

3. **Distorsión de la tensión de red.** Si la tensión de red ya contiene armónicos (THD_V > 0), la
   referencia de corriente del convertidor debe compensarlos activamente o aparecerán en la corriente.

**Efecto del índice de modulación.** Cuando el índice de modulación \( m_a = V_{ref}/V_{triangular} \)
se acerca a 1 (sobremodulación inminente), aparecen armónicos de bajo orden adicionales. Por esto
los convertidores de alta calidad limitan \( m_a \leq 0.9 \) y reservan margen para el desacoplamiento
dq y los feedforward.

## 4 — Normas de calidad de potencia para convertidores

Los organismos normativos establecen límites de inyección de armónicos para proteger la calidad
de la tensión en la red compartida.

**IEEE 519-2022 (revisión de 2022).** Aplica en EE.UU. y es referencia mundial. Los límites de
distorsión de corriente (TDD, Total Demand Distortion) dependen de la razón \( I_{sc}/I_L \) en
el PCC, donde \( I_{sc} \) es la corriente de cortocircuito e \( I_L \) la corriente de carga
máxima a demanda completa:

| \( I_{sc}/I_L \) | Límite TDD (%) | Límite arm. individuales h<11 (%) |
|---|---|---|
| < 20 | 5 | 4 |
| 20–50 | 8 | 7 |
| 50–100 | 12 | 10 |
| 100–1000 | 15 | 12 |
| > 1000 | 20 | 15 |

Nótese que \( I_{sc}/I_L \approx \mathrm{SCR}\,S_n/(P_{carga}) \): una red más fuerte permite
más distorsión de corriente porque la impedancia de red es menor y la distorsión de tensión
resultante es también menor.

**IEC 61000-3-2.** Equipos monofásicos y trifásicos hasta 16 A por fase (electrónica de consumo,
pequeñas cargas industriales). Establece límites absolutos en amperios para cada armónico, no
relativos al fundamental. Esto hace que equipos de muy baja potencia puedan tener una THD muy alta
pero aún estar en norma porque los amperios absolutos son pequeños.

**IEC 61000-3-12.** Equipos de 16 A a 75 A por fase (medianas cargas industriales). Usa la razón
\( R_{sce} = S_{cc}/S_{eq} \) del punto de conexión, análoga al SCR de IEEE 519. El fabricante
debe declarar el \( R_{sce}^{min} \) para el que su equipo cumple.

**EN 50160.** Norma europea de calidad de tensión en redes de distribución. No limita la corriente
inyectada sino la tensión resultante en el PCC:

- Baja tensión (BT): THD_V ≤ 8 %, armónicos individuales ≤ 5 %
- Media tensión (MT): THD_V ≤ 8 %, igual
- Alta tensión (AT): THD_V ≤ 3 %

**Código de red para parques renovables.** Los parques eólicos y solares deben además cumplir con
los límites de emisión del código de red del operador del sistema (TSO), que suele ser más
restrictivo que la norma general. El punto de medición es el PCC en AT (transformador de conexión),
no en BT.

## 5 — Compensación de armónicos en el control

Los armónicos de bajo orden (5°, 7°, 11°, 13°…) no son filtrados por el LCL y deben compensarse
en el lazo de control. Tres estrategias principales:

**Control repetitivo (Repetitive Control, RC).** Un controlador repetitivo es esencialmente un
filtro peine que añade ganancia infinita (teórica) en todos los múltiplos de \( f_0 \). En
discreta, se implementa como una línea de retardo de un periodo \( T_0 = 1/f_0 \):

$$ C_{RC}(z) = \frac{Q(z)\,z^{-N_r}}{1-Q(z)\,z^{-N_r}} $$

donde \( N_r = f_s/f_0 \) es el número de muestras por periodo y \( Q(z) \) un filtro de suavizado
(paso bajo) que evita la inestabilidad de alta frecuencia. El RC elimina todos los armónicos
periódicos simultaneamente sin necesitar una ganancia separada para cada uno. Contrapartida: la
respuesta transitoria es lenta (del orden de varios periodos).

**Controlador PR multi-armónico.** Para compensar selectivamente el 5° y 7° (y opcionalmente el
11°/13°), se suman resonantes independientes:

$$ C_{PR}(s) = K_p + K_i/s + \sum_{h\in\{5,7,11,13\}} \frac{2K_{r,h}\,\omega_c\,s}{s^2+2\omega_c\,s+h^2\omega_0^2} $$

Cada resonante aporta una ganancia muy alta (pico de resonancia) en \( h\,\omega_0 \) y cero error
de seguimiento en esa frecuencia. La banda \( \omega_c \) controla la anchura del pico; un valor
pequeño (\( \omega_c \approx 5\text{–}10\,\text{rad/s} \)) da eliminación selectiva pero es
sensible a variaciones de \( f_0 \); uno grande (\( \omega_c \approx 30\text{–}50\,\text{rad/s} \))
es más robusto frente a fluctuaciones de red.

**Compensación de dead time.** La estrategia más directa: calcular el error de tensión introducido
por el tiempo muerto a cada instante y sumarlo a la referencia de tensión con signo opuesto. Para
el semiperiodo positivo de la corriente:

$$ v_{comp}(t) = +\frac{t_d\,V_{dc}}{T_{sw}/2}\,\mathrm{sign}(i_{fase}(t)) $$

Esto cancela el error de volt-segundo del dead time antes de que llegue a la planta. La precisión
depende de la medida de la corriente y del modelado de \( t_d \) (que varía con temperatura).

**Filtro activo de potencia (APF).** Para instalaciones con cargas no lineales pesadas (hornos de
arco, rectificadores de tiristores), un APF mide la corriente total y el armónico de la carga
\( i_{arm,carga} \) e inyecta su opuesto:

$$ i_{APF}(t) = -i_{arm,carga}(t) $$

El APF es un VSC de potencia menor que la carga (~15–20 % de la potencia de carga para compensar
5° y 7° hasta <3 % THD), controlado con un lazo de corriente de alta BW (>1 kHz) y un banco de
resonantes o un controlador repetitivo.

## 6 — Interarmónicos y ruido de alta frecuencia

Además de los armónicos (múltiplos exactos de \( f_0 \)), existen componentes espectrales no
periódicas que pueden causar problemas de compatibilidad electromagnética y degradar la calidad
de potencia.

**Interarmónicos.** Componentes de frecuencia que NO son múltiplos enteros de \( f_0 \). Sus
fuentes principales:

- **HVDC con LCC:** la conmutación de tiristores genera interarmónicos en \( |m\,f_{dc}\pm n\,f_{ac}| \)
  donde \( f_{dc} \) es la frecuencia de rizado DC y \( m,n \) son enteros.
- **Hornos de arco eléctrico:** el arco es caótico — genera un espectro continuo de interarmónicos
  y sub-armónicos que causa flicker severo.
- **Variadores de velocidad:** la modulación cruzada entre \( f_0 \) y la frecuencia de salida
  \( f_{motor} \) genera interarmónicos en \( |f_0 \pm f_{motor}| \).

**Flicker.** Variaciones rápidas de la luminosidad de las lámparas causadas por fluctuaciones de
tensión. La curva de sensibilidad del ojo humano tiene un pico en torno a 8.8 Hz — las variaciones
a esta frecuencia son las más molestas con menos amplitud. El índice de severidad de flicker \( P_{st} \)
(IEC 61000-4-15) mide el nivel percibido: \( P_{st} > 1 \) indica flicker perceptible.

**Ruido de alta frecuencia (EMI).** Las transiciones de tensión de los IGBTs (d\( V \)/d\( t \)
de 5–20 kV/µs) generan corrientes de modo común que se propagan por las capacidades parásitas del
cableado y del transformador. Los estándares de compatibilidad electromagnética aplican:

- IEC 61800-3: variadores de velocidad — define la categoría (C1–C4) en función de la instalación
  y los límites de emisión conducida y radiada.
- EN 55011 (CISPR 11): generadores eólicos y fotovoltaicos — límites de emisión en 150 kHz–30 MHz.
- Filtros EMI (condensadores de modo común + bobinas de modo diferencial en la entrada del convertidor)
  atenúan el ruido conducido.

**Resonancia paralela condensador-red.** Cuando se conectan bancos de condensadores para
compensación de reactiva, la capacidad total \( C_{comp} \) resuena con la inductancia de red \( L_{red} \):

$$ f_{res} = \frac{1}{2\pi\sqrt{L_{red}\,C_{comp}}} $$

Si esta frecuencia coincide con un armónico existente, la red amplifica ese armónico. El factor de
calidad de la resonancia puede ser 10–20 si la resistencia de red es baja. Mitigación: reactores
de desintonia que desplazan \( f_{res} \) a una frecuencia no armónica (habitualmente al 5.5°
o al 4.7°, entre el 5° y el 3° respectivamente).

<div class="cfig"><img src="../figuras/armonicos-thd-convertidores-analisis.png" alt="Armónicos en convertidores PWM: espectro, dead time, normas y resonancia"><div class="cap">Espectro de corriente de un convertidor PWM con armónicos de bajo orden (5°, 7°) y bandas de conmutación; efecto del tiempo muerto en la forma de onda; comparativa de THD medido con límites IEEE 519 por rango de SCR; y resonancia paralela condensador-red que puede amplificar armónicos específicos hasta 10×.</div></div>

## Conceptos relacionados
- [[convertidor-vsc|modulación PWM]] · [[calidad-potencia]] · [[fft-analisis-espectral]] · [[filtro-lcl]] · [[controlador-resonante]] · [[fenomenos-oscilatorios-red|estabilidad armónica]]

## Referencias
- Mohan, Undeland, Robbins, *Power Electronics*.
- IEEE Std 519-2014.
