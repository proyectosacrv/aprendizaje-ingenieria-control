---
titulo: "MMC: modelo y control"
slug: mmc-modelo-control
categoria: fisica-modelado
tipo: concepto
nivel: avanzado
proyectos: []
objetivos: [modelar eléctricamente el MMC, diseñar el CCSC y entender la jerarquía de control de brazos]
tags: [mmc, modular-multilevel, submódulo, ccsc, energia-brazo, balanceo, hvdc]
fecha_creacion: 2026-07-05
fecha_actualizacion: 2026-07-05
relacionados: [convertidor-back-to-back, topologias-multinivel, filtro-lcl, fenomenos-oscilatorios-red]
referencias:
  - "Cigré TB 604, Guide for the Development of Models for HVDC Converters"
  - "Lesnicar & Marquardt, An Innovative Modular Multilevel Converter Topology"
---

## 1 — Modelo eléctrico del MMC

El MMC de tres fases tiene seis brazos (dos por fase). La ecuación de tensión-corriente de cada brazo
se obtiene aplicando la KVL entre el bus DC y el punto medio de la fase. Para el brazo superior de
la fase a:

$$L_{arm}\frac{di_{ua}}{dt} = \frac{V_{dc}}{2} - v_{ua} - v_{a0}$$

donde \( v_{ua} = \sum_{k=1}^{N} S_{uk}V_{C,uk} \) es la tensión insertada por los SMs del brazo
superior (\( S_{uk}\in\{0,1\} \) es el estado del SM \( k \)), y \( v_{a0} \) es la tensión del
punto medio de la fase a respecto al potencial de referencia DC.

Para el brazo inferior de la misma fase:

$$L_{arm}\frac{di_{la}}{dt} = -\frac{V_{dc}}{2} + v_{la} + v_{a0}$$

**Descomposición de corrientes.** Las corrientes de los brazos se pueden descomponer en componentes
de diferente naturaleza física:

- **Corriente de fase** (sale al exterior, va a la red AC): \( i_a = i_{ua} - i_{la} \)
- **Corriente de modo común** (fluye hacia el bus DC): \( i_{dc,a} = (i_{ua}+i_{la})/2 \), de la que
  \( I_{dc}/3 \) es la componente DC y el resto es la corriente de circulación
- **Corriente de circulación** (interna, no sale al exterior): \( i_{circ,a} = (i_{ua}+i_{la})/2 - I_{dc}/3 \)

**Suma de las dos ecuaciones de brazo** (modo diferencial):

$$2L_{arm}\frac{d}{dt}\left(\frac{i_{ua}+i_{la}}{2}\right) = -\frac{v_{ua}+v_{la}}{2} + \frac{v_{ua,ref}-v_{la,ref}}{2} - R_{arm}\frac{i_{ua}+i_{la}}{2}$$

Esta ecuación gobierna la corriente de modo común y, en particular, la corriente de circulación
\( i_{circ,a} \). Es independiente de la corriente de fase.

## 2 — Balance de energía de los brazos

La energía almacenada en el brazo superior de la fase a es la suma de las energías de sus \( N \) SMs:

$$W_{ua} = \sum_{k=1}^{N}\frac{1}{2}C_{SM}V_{C,uk}^2$$

**Paso 1 — potencia instantánea de un brazo.** La potencia absorbida por el brazo superior es el
producto de su tensión insertada por la corriente que circula:

$$p_{ua}(t) = v_{ua}(t) \cdot i_{ua}(t)$$

Si los SMs están bien balanceados (\( V_{C,uk} \approx V_C \) para todo \( k \)), la potencia
absorbida por los condensadores es exactamente esta potencia.

**Paso 2 — variación temporal de la energía.** En régimen permanente, la energía media por brazo es
constante. Las variaciones de energía tienen la forma:

$$\Delta W_{ua}(t) = W_0 + \hat{W}_1\cos(\omega_0 t + \phi_1) + \hat{W}_2\cos(2\omega_0 t + \phi_2)$$

La componente a \( \omega_0 \) proviene del producto de la corriente de fase (a \( \omega_0 \)) por
la tensión DC del brazo (CC): \( \hat{W}_1 \propto \hat{I}_{fase} V_{dc}/2 \).

La componente a \( 2\omega_0 \) proviene del producto de la corriente AC de fase por la tensión AC del
brazo: ambas varían a \( \omega_0 \), y su producto tiene componente DC (energía media) y a \( 2\omega_0 \).

**Paso 3 — control de energía.** El control de energía de los brazos tiene dos niveles:

1. **Balanceo global (inter-arm balancing):** iguala la energía total entre los seis brazos
   inyectando componentes de tensión adicionales. El brazo superior e inferior de la misma fase
   intercambian energía mediante una componente de corriente de circulación controlada.
2. **Balanceo individual (intra-arm balancing):** dentro de cada brazo, el algoritmo de balanceo
   ordena los SMs para que los de mayor \( V_C \) se inserten cuando la corriente los descargue
   (corriente negativa) y los de menor \( V_C \) cuando la corriente los cargue (corriente positiva).
   Esto tiende a igualar las tensiones de todos los SMs del brazo.

## 3 — Control de la corriente de circulación (CCSC)

La corriente de circulación tiene principalmente componente a \( 2\omega_0 = 2\times 2\pi\times 50 = 628\,\text{rad/s} \).
Su origen: el desequilibrio entre la variación de energía del brazo superior e inferior de cada fase
genera un voltaje diferencial a \( 2\omega_0 \) que impulsa una corriente a esa frecuencia a través
de las inductancias de brazo.

**Paso 1 — modelo del CCSC.** La corriente de circulación obedece (sumando las ecuaciones de los dos
brazos de la fase a):

$$2L_{arm}\frac{di_{circ,a}}{dt} + 2R_{arm}i_{circ,a} = v_{circ,a}$$

donde \( v_{circ,a} = (v_{ua,ref}-v_{la,ref})/2 - (v_{ua,nat}-v_{la,nat})/2 \) es la tensión de
control de circulación (natural más inyectada).

**Paso 2 — marco de referencia a \( 2\omega_0 \).** El CCSC transforma la corriente de circulación
al marco dq giratorio a \( 2\omega_0 \):

$$\begin{pmatrix}i_{circ,d2}\\i_{circ,q2}\end{pmatrix} = R(2\omega_0 t)\begin{pmatrix}i_{circ,a}\\i_{circ,b}\\i_{circ,c}\end{pmatrix}$$

En este marco, la componente de \( 2\omega_0 \) aparece como señal DC → se puede controlar con un PI
clásico con error nulo en régimen permanente.

**Paso 3 — ley de control CCSC.** Con referencia \( i_{circ,dq2}^* = 0 \):

$$v_{circ,dq2}^* = K_{p,cc}(0 - i_{circ,dq2}) + K_{i,cc}\int(0 - i_{circ,dq2})\,dt$$

Transformando de vuelta al marco abc, la tensión \( v_{circ}^* \) se añade a la referencia de inserción
del brazo superior e inferior con signos opuestos, sin afectar a la tensión de salida AC.

**Ancho de banda del CCSC.** Dado que la corriente de circulación a \( 2\omega_0 \) es ~628 rad/s, el
CCSC debe ser más rápido: \( \omega_{CCSC} \approx 3 \times 628 \approx 1900\,\text{rad/s} \)
(~300 Hz). Es más lento que el lazo de corriente AC (1 kHz) pero más rápido que el lazo de \( V_{dc} \).

## 4 — Modulación: NLM y PS-PWM

El MMC puede usar dos estrategias principales de modulación, con características muy diferentes:

**NLM (Nearest Level Modulation).** En cada instante, se inserta el número entero de SMs más cercano
a la referencia de tensión. Formalmente, si la referencia de tensión de brazo es \( v_{arm}^*(t) \) y
la tensión promedio de los condensadores es \( \bar{V}_C \):

$$n_{insert}(t) = \text{round}\left(\frac{v_{arm}^*(t)}{\bar{V}_C}\right)$$

No usa portadora — adecuado para \( N > 20 \). La frecuencia de conmutación de cada IGBT es
\( f_{sw,IGBT} \approx f_0 \) (50 Hz), pero la frecuencia efectiva de la tensión de salida es
\( \sim N\times f_0 \). Las pérdidas de conmutación son mínimas. Es el estándar en HVDC-MMC.

**PS-PWM (Phase-Shifted PWM).** Cada SM tiene su propia portadora triangular de frecuencia \( f_{sw} \),
desfasada \( 360°/N \) respecto al SM anterior. La frecuencia efectiva de la tensión de salida es
\( N\times f_{sw} \). Produce mejor control de rizado en el condensador pero mayor frecuencia de
conmutación. Adecuado para \( N < 20 \) (p. ej. MMC de distribución o STATCOM).

**THD con NLM.** La distorsión armónica de la tensión de salida del NLM decrece aproximadamente como:

$$THD \approx \frac{V_{dc}}{N\,\sqrt{3}} \cdot \frac{1}{V_1} \approx \frac{1}{N}$$

Para \( N = 300 \), \( THD < 0.1\,\% \) sin filtro AC — razón por la que el MMC-HVDC no necesita
filtro de potencia.

## 5 — Control completo del MMC: jerarquía de cuatro capas

La referencia de tensión de inserción de cada brazo se construye sumando las contribuciones de cuatro
capas de control con anchos de banda bien separados:

**Capa 1 — Lazo de corriente AC (BW ~1 kHz).** Controla las corrientes de fase \( i_d \), \( i_q \)
en el marco dq síncrono (igual que en el VSC de dos niveles). Genera una referencia de tensión AC
\( v_{AC}^* \) que se distribuye entre los brazos superior e inferior:

$$v_{upper,AC}^* = -\frac{v_{AC}^*}{2}, \qquad v_{lower,AC}^* = +\frac{v_{AC}^*}{2}$$

**Capa 2 — Lazo externo P/Q/Vdc/Vac (BW ~50 Hz).** Genera las referencias \( i_d^* \), \( i_q^* \)
para la capa 1 en función del modo de operación del terminal.

**Capa 3 — CCSC (BW ~300 Hz a \( 2\omega_0 \)).** Genera una referencia de tensión de circulación
\( v_{circ}^* \) que se añade a los dos brazos de cada fase con signos iguales (modo común):

$$v_{upper,circ}^* = +\frac{v_{circ}^*}{2}, \qquad v_{lower,circ}^* = +\frac{v_{circ}^*}{2}$$

**Capa 4 — Balanceo de condensadores (cada período de control \( T_s \)).** Para el NLM, ordena los
SMs del brazo en función de su tensión de condensador y el signo de la corriente de brazo, para igualar
todas las tensiones \( V_{C,k} \) sin necesidad de un controlador PI por SM.

La referencia final de inserción de tensión de cada brazo es la suma de todas las capas:

$$v_{upper}^* = \frac{V_{dc}}{2} + v_{upper,AC}^* + v_{upper,circ}^*$$
$$v_{lower}^* = \frac{V_{dc}}{2} + v_{lower,AC}^* + v_{lower,circ}^*$$

## 6 — Parámetros de diseño del MMC

**Energía almacenada.** El criterio de diseño estándar es 30–40 kJ/MVA, que garantiza que el rizado
de tensión de los condensadores sea < 10 % en condición nominal:

$$W_{stored,total} \approx 35\,\frac{\text{kJ}}{\text{MVA}} \times S_{nom}$$

**Tensión nominal de condensador.** Para un MMC de tensión DC \( V_{dc} \) y \( N \) SMs por brazo:

$$V_{C,nom} = \frac{V_{dc}}{N}$$

**Capacidad de cada SM.** De la energía por brazo (\( W_{stored}/6 \), seis brazos) y la tensión:

$$C_{SM} = \frac{2\,W_{stored}/6}{N\,V_{C,nom}^2} = \frac{W_{stored}}{3\,N\,V_{C,nom}^2} = \frac{W_{stored}\,N}{3\,V_{dc}^2}$$

**Inductancia de brazo.** \( L_{arm} \) limita el \( di/dt \) ante faltas y reduce el rizado de la
corriente de circulación. Valor típico: \( L_{arm} \approx 0.15\,\text{pu} \) basado en \( S_{nom} \)
y \( V_{dc}/2 \).

Ejemplo para 500 MW, ±320 kV, \( N=300 \) SMs:

| Parámetro | Cálculo | Resultado |
|---|---|---|
| \( V_{C,nom} \) | \( 640\,\text{kV}/300 \) | 2.13 kV |
| \( W_{stored} \) | \( 35\,\text{kJ/MVA}\times500\,\text{MVA} \) | 17.5 MJ |
| \( C_{SM} \) | \( 17.5\times10^6\times300/(3\times640^2\times10^6) \) | 4.3 mF |
| Rizado \( \Delta V_C/V_{C,nom} \) | \( < 10\,\% \) objetivo | 9.8 % |

<div class="cfig"><img src="../figuras/mmc-modelo-control-analisis.png" alt="MMC: energía de brazos, CCSC y jerarquía de control"><div class="cap">Variación de energía de los brazos superior e inferior (componentes a \( \omega_0 \) y \( 2\omega_0 \)), corriente de circulación con y sin CCSC, jerarquía de las cuatro capas de control del MMC, y efecto del balanceo de tensiones de los submódulos.</div></div>
