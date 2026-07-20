---
titulo: Calidad de potencia y normativa (IEEE 519, IEC 61000)
slug: calidad-potencia
categoria: metodologia
tipo: concepto
nivel: intermedio
proyectos: []
objetivos: [cuantificar y cumplir los límites de distorsión armónica, desequilibrio y flicker]
tags: [calidad-potencia, thd, armonicos, flicker, ieee519, iec61000, desequilibrio, intermedio]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-01
relacionados: [fft-analisis-espectral, convertidor-vsc, filtro-lcl, fenomenos-oscilatorios-red, deteccion-islanding]
referencias:
  - "IEEE Std 519-2022, Harmonic Control in Electric Power Systems"
  - "IEC 61000-3-2/3-12, Limits for Harmonic Current Emissions"
  - "IEC 61000-4-30, Power Quality Measurement Methods"
---

## Definición
Conjunto de métricas y límites normativos que caracterizan la **calidad de la tensión/corriente**
entregada a la red: armónicos, interarmónicos, desequilibrio, flicker (parpadeo), dips/swells y
transitorios. Define lo que el convertidor no debe inyectar en el punto de conexión común (PCC).

## Fundamento teórico
**Distorsión armónica total (THD):**
$$ \text{THD}_I = \frac{\sqrt{\sum_{h=2}^{\infty}I_h^2}}{I_1}\times100\,\% $$
En **IEEE 519-2022** los límites de corriente se fijan en el PCC en función de la relación
\( I_{sc}/I_L \) (relación de cortocircuito / carga): a mayor SCR más corriente armónica admisible.
Armónicos de tensión total < 5 %, individuales < 3 %.

**IEC 61000-3-2/3-12:** límites de emisión armónica de equipos individuales (hasta 16 A y hasta
75 A respectivamente) para 2–40 armónicos en valores absolutos (A) por fase.

**Desequilibrio de tensión** (NEMA / IEC 61000-2-2): factor de desequilibrio
\( V_{unb}=V_{neg}/V_{pos}\times100\,\% < 2\text{–}3\,\% \).

**Flicker (IEC 61000-3-3 / 61000-3-11):** \( P_{st} \) (flicker de corta duración, 10 min) y
\( P_{lt} \) (larga duración, 2 h) miden la sensación de parpadeo; causado por cargas pulsantes de
gran amplitud a 0.5–25 Hz. Límites: \( P_{st}<1 \), \( P_{lt}<0.65 \).

**Medición normativa (IEC 61000-4-30 clase A):** ventanas sincronizadas de 10/12 ciclos (200/166,7 ms);
agrupación en 3 s, 10 min, 2 h para estadísticas.

**Origen en convertidores:** la [[convertidor-vsc|conmutación PWM]] genera armónicos en torno a
\( f_{sw} \) y bandas laterales; el [[filtro-lcl]] los atenúa; la resonancia del LCL y la
[[fenomenos-oscilatorios-red|estabilidad armónica]] pueden amplificarlos. Las cargas pulsantes de data center (GPU en rafaga)
generan flicker e interarmónicos.

<div class="cfig"><img src="figuras/calidad-potencia-armonicos.png" alt="armonicos medidos frente al limite IEEE 519"><div class="cap">Comprobación de cumplimiento: cada armónico de corriente medido en el PCC se compara con el límite individual de IEEE 519 (que depende de la relación $I_{sc}/I_L$). Aquí todos cumplen salvo el 5º, que supera su límite; cumplir el THD global no basta si un armónico individual lo viola. La mitigación es más atenuación de filtro, filtro activo o resonantes.</div></div>

## 1 — Derivación del THD y aplicación del límite IEEE 519
**Paso 1 — descomposición de Fourier.** Cualquier señal de corriente periódica \( i(t) \) con fundamental \( I_1 \) a \( f_1=50 \) Hz se expande en serie de Fourier:

$$ i(t)=\sum_{h=1}^{\infty}I_h\sin(h\omega_1 t + \varphi_h) $$

La potencia RMS total es \( I_{rms}=\sqrt{\sum_{h=1}^\infty I_h^2} \). La componente fundamental \( I_1 \) es la que transfiere potencia activa a la red; el resto son **armónicos** que solo generan pérdidas y distorsión.

**Paso 2 — definición del THD.** El THD de corriente es la razón entre la energía armónica y la fundamental:

$$ \text{THD}_I = \frac{\sqrt{\sum_{h=2}^{\infty}I_h^2}}{I_1}\times100\,\% = \frac{\sqrt{I_{rms}^2-I_1^2}}{I_1}\times100\,\% $$

Para un VSC de dos niveles a \( f_{sw}=5 \) kHz con un filtro LCL que atenúa 60 dB los armónicos de conmutación, los armónicos relevantes quedan por debajo de \( 0.1\,\% \cdot I_1 \), y el THD es:

$$ \text{THD}\approx\sqrt{3^2+2^2+1^2}/100 = \sqrt{14}/100 \approx 3.74\,\% \quad \checkmark \text{ (límite IEEE 519: 5\%)} $$

**Paso 3 — límites normativos IEEE 519-2022.** Los límites de corriente en el PCC dependen de la relación de cortocircuito \( I_{sc}/I_L \): a mayor SCR (red más fuerte), la red puede absorber más armónicos:

| \( I_{sc}/I_L \) | THD límite | Armónico individual h<11 |
|---|---|---|
| < 20 (SCR bajo) | 5 % | 4 % |
| 20–50 | 8 % | 7 % |
| > 100 | 15 % | 12 % |

La tensión armónica total en el PCC siempre debe ser \( <5\,\% \) (armónico individual \( <3\,\% \)) independientemente del SCR. La corriente armónica inyectada genera tensión armónica mediante la impedancia de red: \( V_h=I_h\cdot Z_{red,h}\approx I_h\cdot h\omega_0 L_g \), de modo que la red débil (SCR bajo, \( L_g \) grande) tiene límites de corriente más estrictos.

$$ \boxed{\text{THD}_I < 5\,\%\ (\text{IEEE 519 en PCC, SCR }<20);\quad V_{h}<3\,\%\ \text{cada armónico}} $$

## Cuándo y por qué se usa
Como criterio de aceptación en el diseño del filtro y del control, en auditorías de conexión a red
y en el análisis de impacto de cargas de data center / renovables. Conecta los estudios de
simulación con los requisitos legales.

## Procedimiento de diseño (genérico)
1. Identifica la norma aplicable (IEEE 519 para red industrial US; IEC 61000 para Europa/equipos).
2. Mide o simula la corriente en el PCC con [[fft-analisis-espectral|FFT]] (ventana IEC 61000-4-30).
3. Compara con los límites por armónico y THD.
4. Si incumple: aumenta la atenuación del [[filtro-lcl]], añade filtro activo o [[control-repetitivo]],
   o reduce la carga armónica en el PCC.
5. Para flicker: evalúa la carga pulsante y mitiga con almacenamiento/bus DC correctamente
   dimensionado ([[dinamica-bus-dc]]).

## Ejemplo de código
```python
import numpy as np
def thd(spectrum_rms, fundamental_idx=1):
    harm = np.concatenate([spectrum_rms[:fundamental_idx], spectrum_rms[fundamental_idx+1:]])
    return np.sqrt(np.sum(harm**2)) / spectrum_rms[fundamental_idx] * 100  # %
```

## Parámetros y valores típicos
THD de corriente < 5 % (IEEE 519 en conexión típica); armónico individual 3–5 % (orden dependiente);
desequilibrio < 2 %; \( P_{st}<1 \). Armónicos dominantes de VSC 2-niveles: \( f_{sw}\pm 2f_1 \),
\( 2f_{sw}\pm f_1 \).

## Errores comunes
- Medir THD con ventana no sincronizada → fuga espectral que infla el THD artificialmente.
- Cumplir límites de armónicos individuales pero ignorar el THD total.
- Confundir límites de emisión de equipo (IEC 61000-3-2) con límites del PCC (IEEE 519).
- Ignorar el flicker en cargas pulsantes de data center (GPU workloads).

## Conceptos relacionados
- [[fft-analisis-espectral]] · [[convertidor-vsc|modulación PWM]] · [[filtro-lcl]] · [[fenomenos-oscilatorios-red|estabilidad armónica]] · [[deteccion-islanding]]

## Referencias
- IEEE Std 519-2022, *Harmonic Control in Electric Power Systems*.
- IEC 61000-3-2, *Limits for Harmonic Current Emissions*.
- IEC 61000-4-30, *Power Quality Measurement Methods*.

## 2 — Normativa aplicable: EN 50160, IEC 61000-4, IEEE 519-2022

Existen tres familias principales de normas de calidad de potencia, con ámbitos distintos:

**EN 50160 (Europa, usuario final):** define las características de la tensión de suministro en el punto de entrega al cliente. Establece límites de variación lenta de tensión (±10% en 95% del tiempo), armónicos de tensión totales < 8% (THD_V), flicker \( P_{lt} < 1 \), desequilibrio de tensión < 2% y discontinuidades. Es la norma del **distribuidor** hacia el cliente.

**IEC 61000-4 (inmunidad de equipos):** serie de pruebas de inmunidad electromagnética: huecos de tensión (IEC 61000-4-11), armónicos e interarmónicos (IEC 61000-4-7), fluctuaciones de tensión y flicker (IEC 61000-4-15), medición de calidad (IEC 61000-4-30 clase A). IEC 61000-4-7 define la metodología de medición armónica con ventanas de 10/12 ciclos sincrónicos. Es la norma de **pruebas de tipo de equipo**.

**IEEE 519-2022 (armónicos en PCC, EE.UU. y uso internacional):** define límites de corriente armónica en el **punto de conexión común** (PCC) entre la instalación y la red de distribución. Los límites dependen de la razón de cortocircuito \( I_{sc}/I_L \):

| \( I_{sc}/I_L \) | THD_I | Indiv. \( h < 11 \) |
|---|---|---|
| < 20 (red débil) | 5% | 4% |
| 20–50 | 8% | 7% |
| 50–100 | 12% | 10% |
| > 100 (red fuerte) | 15% | 12% |

La **tensión armónica** en el PCC siempre debe ser THD_V < 5% (individual < 3%) independientemente del SCR. IEEE 519-2022 añade el concepto de ventana de medición de 10 min para considerar el 99° percentil (no el valor máximo instantáneo).

## 3 — Flicker y variaciones rápidas de tensión

El **flicker** (parpadeo) es la sensación visual de fluctuación de la luminosidad causada por variaciones rápidas de la tensión de suministro a frecuencias de 0.5–25 Hz. La curva de susceptibilidad visual del ojo humano tiene su máximo hacia 8.8 Hz (variaciones a esa frecuencia con amplitudes > 0.3% son perceptibles).

**Métricas de flicker (IEC 61000-3-3 / EN 50160):**
- \( P_{st} \): flicker de corta duración, medido en ventanas de 10 min. Límite: \( P_{st} < 1 \).
- \( P_{lt} \): flicker de larga duración, combinación de 12 valores de \( P_{st} \) consecutivos (2 h). Límite: \( P_{lt} < 0.65 \).

$$ P_{lt} = \sqrt[3]{\frac{1}{12}\sum_{i=1}^{12} P_{st,i}^3} $$

**Causas en convertidores:** las modulaciones de potencia a frecuencias medias (e.g., control MPPT de una turbina eólica con variaciones de paso a 1–3 Hz) y las cargas pulsantes de data center (ciclos de trabajo de GPU a 10–20 Hz) generan flicker. La solución es añadir almacenamiento en el bus DC para suavizar la potencia entregada a la red.

## 4 — Desequilibrio de tensión: VUF y su impacto

El **desequilibrio de tensión** ocurre cuando las tres fases no tienen la misma amplitud o su separación angular no es exactamente 120°. Se cuantifica con el **Factor de Desequilibrio de Tensión** (VUF, Voltage Unbalance Factor):

$$ \text{VUF} = \frac{V_{neg}}{V_{pos}} \times 100\,\% < 2\,\% \quad (\text{EN 50160, IEC 61000-2-2}) $$

donde \( V_{neg} \) y \( V_{pos} \) son las componentes de secuencia negativa y positiva obtenidas por la transformada de componentes simétricas ([[componentes-simetricas]]).

**Impacto en motores:** un VUF del 1% genera una componente de secuencia negativa que produce un campo giratorio inverso. El par de frenado resultante puede suponer una reducción de potencia del 3–8% y un incremento del calentamiento.

**Impacto en convertidores trifásicos:** el desequilibrio genera componentes de segundo armónico (\( 2\omega_0 \)) en el bus DC y en las corrientes dq, que pueden superar los límites de THD si no se controlan. Un control de secuencia dual (lazo de corriente de secuencia negativa) es necesario cuando VUF > 1%.

$$ \boxed{V_{neg} = \frac{|V_a + a^2 V_b + a V_c|}{3},\quad a = e^{j2\pi/3};\quad\text{VUF} = V_{neg}/V_{pos} < 2\,\%} $$

## 5 — Calidad de potencia en bus DC: rizado y variaciones lentas

En sistemas con bus DC (microrredes DC, data centers, almacenamiento BESS), la calidad de potencia del bus DC es tan importante como la de la red AC:

**Rizado de tensión DC** (\( \Delta V_{dc} \)): producido por la conmutación del convertidor (rizado a \( f_{sw} \) y \( 2f_{sw} \)) y por las variaciones de carga. Límite típico: \( \Delta V_{dc}/V_{dc}^* < 1\,\% \) para cargas sensibles. Se diseña el condensador del bus:

$$ C_{bus} \approx \frac{P_{nom} \cdot \Delta t}{V_{dc}^* \cdot \Delta V_{dc}} $$

donde \( \Delta t \) es la duración del transitorio de carga más rápido que debe absorber el condensador.

**Variaciones lentas de tensión DC:** modulación de \( V_{dc} \) a baja frecuencia debida a variaciones de potencia de las fuentes renovables o de las cargas pulsantes. Un lazo de control externo (droop DC, [[droop-dc]]) regula \( V_{dc} \) en ±5% del nominal.

**Interacciones entre subsistemas:** en una microrred DC con múltiples convertidores, la impedancia de salida de cada convertidor interactúa con la impedancia de entrada de las cargas (CPL, Constant Power Loads). Si la CPL domina, el bus DC puede tener instabilidad de oscilación incluso si cada convertidor es estable individualmente. El criterio de Middlebrook ([[criterio-middlebrook]]) verifica la estabilidad de la interacción.

## 6 — Normativa aplicable: tabla de referencia cruzada

Las tres familias de normas tienen ámbitos distintos pero complementarios:

| Norma | Ámbito | Métrica principal | Límite clave |
|---|---|---|---|
| EN 50160 | Suministro al cliente (red distribución EU) | THD_V, variación lenta de V, flicker | THD_V<8%, \(P_{lt}<1\), VUF<2% |
| IEC 61000-4-7 | Medición armónica (metodología) | Ventana 10/12 ciclos sincrónicos | Resolución 5 Hz |
| IEC 61000-4-15 | Medición flicker (flickermeter) | \(P_{st}\) (10 min), \(P_{lt}\) (2 h) | \(P_{st}<1\), \(P_{lt}<0.65\) |
| IEC 61000-4-30 clase A | Medición calidad de potencia | Agregación 3 s, 10 min, 2 h | Clase A: alta precisión |
| IEC 61000-3-2 | Emisiones armónicas de equipos ≤16 A | Valores absolutos (A) por armónico | Tabla A/B/C/D según tipo |
| IEC 61000-3-12 | Emisiones armónicas equipos 16–75 A | Relación corriente cortocircuito | \(R_{sce}\) mínimo |
| IEEE 519-2022 | Armónicos en PCC (red industrial) | THD_I, armónico individual | 5% THD_I (SCR<20) |
| IEEE 1547-2018 | DER conectados a red distribución | Armónicos, flicker, desequilibrio | THD_I<5%, VUF<2% |

## 7 — Flicker: medición con IEC 61000-4-15 y causas en convertidores

El **flickermeter** de IEC 61000-4-15 simula la cadena de percepción del parpadeo: red → lámpara incandescente → ojo humano → cerebro. Produce \(P_{st}\) en ventanas de 10 min y \(P_{lt}\) en ventanas de 2 h.

**Curva de susceptibilidad visual:** el ojo humano es más sensible a variaciones de luminosidad a **8.8 Hz** (frecuencia de parpadeo más molesta); a esa frecuencia, variaciones de tensión de amplitud >0.3% son perceptibles (\(P_{st}=1\)). La sensibilidad cae por encima de 25 Hz y por debajo de 0.5 Hz.

**Causas en convertidores renovables:**
- Control MPPT de turbina eólica: variaciones de paso de pala a 1–3 Hz generan variaciones de potencia y tensión → flicker.
- GPU en ráfaga (data center): ciclos de trabajo a 10–20 Hz en la potencia drenada → \(P_{st}\) elevado en el bus de distribución.
- Convertidores con control de droop rápido: si el droop excita la frecuencia de resonancia mecánica del sistema, puede generar flicker en la tensión.

**Solución:** añadir almacenamiento en el bus DC (BESS o supercondensador) con un lazo de suavizado de potencia: filtro paso-bajo de la potencia entregada a la red con \(\tau_{filt}\approx100\,\text{ms}\) → \(P_{st}\) cae por debajo de 1.

## 8 — Desequilibrio de tensión: VUF y control de secuencia dual

**Definición y cálculo del VUF:**
$$V_{neg} = \frac{|V_a + a^2 V_b + a V_c|}{3},\quad a=e^{j2\pi/3};\quad\text{VUF}=\frac{V_{neg}}{V_{pos}}\times100\,\%$$

**Límite normativo:** VUF < 2% (EN 50160, IEC 61000-2-2, IEEE 1547-2018).

**Impacto en motores:** un VUF del 1% genera una componente de secuencia negativa con frecuencia \(-f_0\) (giro inverso). El par de frenado resultante reduce la potencia del motor en 3–8% y aumenta el calentamiento del devanado. Para VUF>2%: derate obligatorio del motor según NEMA MG-1.

**Impacto en convertidores trifásicos:** el desequilibrio genera componentes de 2° armónico (\(2\omega_0\)) en el bus DC y en las corrientes dq. Si el lazo de corriente no tiene ancho de banda suficiente para rechazar la perturbación a \(2f_0=100\,\text{Hz}\), esas componentes aparecen en la corriente de red como armónicos pares — que IEEE 519 también limita.

**Control de secuencia dual:** cuando VUF > 1%, se implementa un lazo de corriente adicional en secuencia negativa (DSOGI para separar secuencias). El lazo de secuencia negativa compensa activamente \(V_{neg}\), reduciendo el VUF a <0.5%.

## 9 — Calidad de potencia en bus DC: rizado, variaciones lentas e inestabilidad CPL

**Rizado de tensión DC:** producido por la conmutación del convertidor AC/DC a \(f_{sw}\) y \(2f_{sw}\), y por las variaciones de carga. Límite típico: \(\Delta V_{dc}/V_{dc}^* < 1\%\) para cargas sensibles (servidores, convertidores DC/DC de alta frecuencia).

**Dimensionado del condensador del bus:**
$$C_{bus}\approx\frac{P_{nom}\cdot\Delta t}{V_{dc}^*\cdot\Delta V_{dc}}$$
donde \(\Delta t\) es la duración del transitorio de carga más rápido. Para \(P_{nom}=100\,\text{kW}\), \(\Delta t=10\,\text{ms}\), \(V_{dc}^*=800\,\text{V}\), \(\Delta V_{dc}=8\,\text{V}\): \(C_{bus}\approx125\,\mu\text{F}\).

**Variaciones lentas:** modulación de \(V_{dc}\) a baja frecuencia por variaciones de las fuentes renovables o cargas pulsantes. Un lazo de droop DC ([[droop-dc]]) regula \(V_{dc}\) en ±5% del nominal con una constante de tiempo de ~100 ms.

**Inestabilidad CPL:** una carga de potencia constante (CPL, Constant Power Load — como un convertidor DC/DC regulado) presenta una impedancia de entrada negativa a baja frecuencia: \(Z_{CPL}(j\omega)\approx -V^2/P\) para \(\omega\to0\). Si la impedancia de salida del convertidor fuente \(Z_{src}(j\omega)\) viola el criterio de Middlebrook (\(|Z_{src}/Z_{CPL}|<1\) en toda \(\omega\)), el bus DC se inestabiliza.

<div class="cfig"><img src="figuras/calidad-potencia-analisis.png" alt="THD con límites IEEE 519, curva de susceptibilidad al flicker, VUF y rizado DC"><div class="cap">Calidad de potencia: (a) espectro de corriente con límites IEEE 519 por armónico individual, (b) curva de susceptibilidad visual al flicker Pst con máximo a 8.8 Hz, (c) diagrama vectorial de desequilibrio de tensión (VUF), (d) rizado de bus DC con condensador de filtrado y respuesta a transitorio de carga.</div></div>

## Conceptos relacionados
- [[fft-analisis-espectral]] · [[convertidor-vsc|modulación PWM]] · [[filtro-lcl]] · [[fenomenos-oscilatorios-red|estabilidad armónica]] · [[deteccion-islanding]]

## Referencias
- IEEE Std 519-2022, *Harmonic Control in Electric Power Systems*.
- IEC 61000-3-2, *Limits for Harmonic Current Emissions*.
- IEC 61000-4-30, *Power Quality Measurement Methods*.
