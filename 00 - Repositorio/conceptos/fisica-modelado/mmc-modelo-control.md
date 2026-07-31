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

<div class="cfig"><img src="figuras/mmc-estructura.png" alt="estructura trifásica del MMC con seis brazos de submódulos e inductancias de brazo entre el bus DC y las salidas AC, y la descomposición de la corriente de una fase en corriente de brazo superior e inferior, corriente de salida y corriente de circulación"><div class="cap">(a) Estructura trifásica: seis brazos (superior e inferior por fase), cada uno con \(N\) submódulos en serie y una inductancia de brazo \(L_{arm}\), entre el bus DC y las salidas AC a/b/c. (b) La corriente de cada brazo (\(i_u\), \(i_l\)) se descompone en la <b>corriente de salida</b> \(i_{out}=i_u-i_l\) (va a la red) y la <b>corriente de circulación</b> \(i_{circ}=(i_u+i_l)/2\) (interna, entre brazos y el bus DC).</div></div>

<div class="cfig"><img src="figuras/mmc-submodulo-ccsc.png" alt="submodulo half-bridge del MMC en sus dos estados, insertado con el condensador en serie en el brazo y bypass con el condensador cortocircuitado, y diagrama de bloques de la jerarquia de las cuatro capas de control con sus anchos de banda sumando sus contribuciones en la referencia de tension de cada brazo"><div class="cap">(a) El submódulo half-bridge tiene solo dos estados útiles: <b>insertado</b> (\(S_1\) ON, \(S_2\) OFF), el condensador queda en serie en el brazo y aporta \(v_{SM}=V_C\); y <b>bypass</b> (\(S_1\) OFF, \(S_2\) ON), el condensador se cortocircuita y \(v_{SM}=0\). La corriente de brazo circula por el submódulo en ambos casos, cargando o no el condensador según el estado y el signo de la corriente. (b) La referencia de tensión de cada brazo es la <b>suma</b> de las contribuciones de las cuatro capas de control (apartado 5), cada una con un ancho de banda muy distinto.</div></div>

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

## 7 — Derivación completa de la corriente de circulación

La corriente de circulación es la componente de la corriente de modo común que fluye entre los
brazos de la misma fase sin salir al exterior del MMC. Su origen físico es el desequilibrio entre
la variación de energía del brazo superior e inferior.

**Paso 1 — tensiones insertadas en régimen permanente.** En operación normal, la modulación
genera estas tensiones en los brazos superior e inferior de la fase a:

$$v_{ua}(t) = \frac{V_{dc}}{2} - \hat{V}_{ac}\sin(\omega_0 t) + v_{circ}(t)$$
$$v_{la}(t) = \frac{V_{dc}}{2} + \hat{V}_{ac}\sin(\omega_0 t) + v_{circ}(t)$$

La componente DC (\( V_{dc}/2 \)) garantiza que la suma de los brazos cubre la tensión DC. La
componente AC (\( \hat{V}_{ac}\sin(\omega_0 t) \)) con signos opuestos sintetiza la tensión AC de
salida. La componente de circulación \( v_{circ}(t) \) es igual en ambos brazos.

**Paso 2 — corriente de fase y de modo común.** Las corrientes de los brazos son:

$$i_{ua}(t) = \frac{i_a}{2} + i_{circ,a}(t) + \frac{I_{dc}}{3}$$
$$i_{la}(t) = -\frac{i_a}{2} + i_{circ,a}(t) + \frac{I_{dc}}{3}$$

donde \( i_a \) es la corriente de fase (sale al exterior), \( I_{dc}/3 \) es la contribución
DC al bus, e \( i_{circ,a} \) es la corriente de circulación (suma de los dos brazos).

**Paso 3 — potencia absorbida por los condensadores.** La potencia instantánea del brazo superior:

$$p_{ua}(t) = v_{ua}\cdot i_{ua} = \left(\frac{V_{dc}}{2} - \hat{V}\sin\omega t\right)\left(\frac{I_{ac}}{2}\cos(\omega t-\phi) + \frac{I_{dc}}{3}\right)$$

Expandiendo el producto y usando \( \sin\cdot\cos = \tfrac12\sin + \tfrac12\sin(2\omega t-\phi) \):

$$p_{ua}(t) = \underbrace{\frac{V_{dc}I_{dc}}{6}}_{\text{DC}} + \underbrace{\frac{V_{dc}I_{ac}}{4}\cos(\omega t-\phi)}_{\omega_0} - \underbrace{\frac{\hat{V}I_{dc}}{3}\sin(\omega t)}_{\omega_0} - \underbrace{\frac{\hat{V}I_{ac}}{4}\sin(2\omega t-\phi)}_{2\omega_0}$$

**Paso 4 — desequilibrio a \( 2\omega_0 \).** El término a \( 2\omega_0 \) en \( p_{ua} \) integra
en el tiempo y produce variación de energía a \( 2\omega_0 \):

$$\Delta W_{ua,2\omega}(t) = +\frac{\hat{V}I_{ac}}{8\omega_0}\cos(2\omega_0 t - \phi)$$

Para el brazo inferior (con \( v_{la} \) con la componente AC de signo opuesto):

$$\Delta W_{la,2\omega}(t) = +\frac{\hat{V}I_{ac}}{8\omega_0}\cos(2\omega_0 t - \phi)$$

Ambos brazos tienen el mismo término a \( 2\omega_0 \) — el desequilibrio total entre superior e
inferior tiene componente a \( \omega_0 \), y la media entre ambos tiene componente a \( 2\omega_0 \).
Esta componente a \( 2\omega_0 \) de la energía media se traduce en variación de la tensión promedio
de condensadores a \( 2\omega_0 \), lo que impulsa una corriente a \( 2\omega_0 \) a través de la
inductancia de brazo — la corriente de circulación.

**Paso 5 — amplitud de la corriente de circulación sin control.** La tensión de conducción que
genera la variación de energía a \( 2\omega_0 \) impulsa una corriente a través de \( 2L_{arm} \):

$$\hat{I}_{circ} \approx \frac{\hat{V}_{ac}\hat{I}_{ac}}{4\cdot 2\omega_0\cdot 2L_{arm}\cdot V_{dc}/N}$$

Para valores típicos (\( \hat{V}_{ac}/V_{dc} = 0.5 \), \( \hat{I}_{ac}/I_{nom} = 1 \),
\( L_{arm} = 0.15\,\text{pu} \)):
\( \hat{I}_{circ} \approx 0.1\text{–}0.15\,\text{pu} \) — 10–15 % de la corriente nominal de fase.

## 8 — Control de la energía total del MMC

La corriente de circulación que elimina el CCSC garantiza que el promedio de las tensiones de
condensador sea \( V_{C,nom} \) en cada brazo. Pero si hay desequilibrios lentos (asimetría entre
fases, pequeñas diferencias en la capacidad de los SMs), la energía total del MMC puede derivar.
El control de energía total es una capa adicional por encima del CCSC.

**Energía total y por brazo.** La energía almacenada en los 6 brazos:

$$W_{total} = \sum_{j\in\{ua,la,ub,lb,uc,lc\}} W_j = 6\cdot\frac{N}{2}C_{SM}V_{C,nom}^2 = 3NC_{SM}V_{C,nom}^2$$

En operación normal, \( W_{total} \) debería ser constante. Cualquier pérdida neta (diferencia entre
potencia del bus DC y potencia AC) hace que \( W_{total} \) derive lentamente.

**Referencia de energía.** El valor de referencia de energía total:

$$W_{total}^* = 3NC_{SM}V_{C,nom}^{*2}$$

El control compara \( W_{total}^* - W_{total} \) y ajusta el componente DC de la corriente de brazo
para recargar o descargar los condensadores:

$$\Delta I_{dc,control} = K_{Wtot}(W_{total}^* - W_{total})$$

Esta corriente adicional no afecta a la corriente de fase AC ni a la de circulación — solo ajusta
el flujo de potencia DC hacia/desde los condensadores.

**Balanceo entre fases (horizontal).** Si una fase tiene más energía que las otras, se puede
redistribuir mediante componentes de tensión de frecuencia fundamental en modo común:

$$v_{circ,a}^*(t) = v_{circ,a,DC}^* + \hat{v}_{H}\sin(\omega_0 t)$$

La componente fundamental en modo común (\( \omega_0 \)) genera una corriente de circulación a
\( \omega_0 \) que transfiere potencia entre fases. Esta estrategia es más compleja que el control
de energía total y se implementa como capa adicional de balanceo.

**Balanceo superior-inferior (vertical).** El desequilibrio entre el brazo superior e inferior de
la misma fase se corrige mediante componentes de tensión de frecuencia fundamental en modo
diferencial:

$$v_{upper}^* += +\frac{\Delta v_V}{2}\sin(\omega_0 t + \phi_V)$$
$$v_{lower}^* += -\frac{\Delta v_V}{2}\sin(\omega_0 t + \phi_V)$$

donde \( \phi_V \) es el ángulo óptimo para maximizar la transferencia de energía entre los brazos
superior e inferior con la mínima perturbación a la corriente de fase.

## 9 — Modulación NLM con sorting: algoritmo de balanceo de condensadores

La modulación NLM (Nearest Level Modulation) con sorting es el algoritmo estándar en HVDC-MMC con
\( N > 20 \) SMs por brazo. Combina la selección del número de SMs a insertar (NLM) con el
reordenamiento de qué SMs específicos se insertan (sorting) para igualar sus tensiones de
condensador.

**Paso 1 — determinar el número de SMs a insertar.** En cada instante de control (período \( T_s \)):

$$n_{ins}(t_k) = \mathrm{round}\!\left(\frac{v_{arm}^*(t_k)}{\bar{V}_C(t_k)}\right)$$

donde \( \bar{V}_C \) es el promedio de las tensiones de todos los condensadores del brazo. El
resultado es un entero entre 0 y \( N \).

**Paso 2 — ordenar los SMs por tensión.** Se ordenan los \( N \) SMs del brazo según su tensión
de condensador \( V_{C,k} \) en orden ascendente o descendente.

**Paso 3 — seleccionar qué SMs insertar según el signo de la corriente.** La lógica de selección:

- Si \( i_{arm} > 0 \) (corriente carga los condensadores): insertar los \( n_{ins} \) SMs de
  **menor** tensión (los más descargados se cargan primero → tienden hacia la igualdad).
- Si \( i_{arm} < 0 \) (corriente descarga los condensadores): insertar los \( n_{ins} \) SMs de
  **mayor** tensión (los más cargados se descargan primero → tienden hacia la igualdad).

Este algoritmo converge hacia \( V_{C,k} \approx V_{C,nom} \) para todos los SMs sin necesidad
de ningún controlador PI por SM — solo con la lógica de sorting ejecutada cada período de control.

**Frecuencia de conmutación de cada IGBT.** Cada SM conmuta aproximadamente cada vez que es
seleccionado o deseleccionado. Con \( N = 300 \) SMs y un período de control \( T_s = 1\,\text{ms} \):

$$f_{sw,IGBT} \approx \frac{f_0\cdot n_{ins}(promedio)}{N} \approx \frac{50\cdot N/2}{N} = 25\,\text{Hz}$$

En la práctica, la conmutación no está perfectamente distribuida: los SMs con mayor error de
tensión conmutan más frecuentemente. La frecuencia efectiva por IGBT es 50–200 Hz dependiendo del
rizado de condensador tolerable.

**Histeresis en el sorting.** Para evitar conmutaciones innecesarias cuando las tensiones son muy
parecidas, se introduce una banda de histeresis: solo se reordena un SM si la diferencia de tensión
entre el SM seleccionado y el siguiente candidato supera un umbral
\( \Delta V_{hyst} \approx 0.5\text{–}1\,\% \cdot V_{C,nom} \).

## 10 — Limitación de corriente en el MMC: límite por brazo

La corriente en un MMC no se limita simplemente por la corriente de fase, sino por la corriente de
cada brazo individual, que incluye la componente de circulación y la componente DC.

**Corriente de brazo superior.** Para la fase a, el brazo superior conduce:

$$i_{ua}(t) = \frac{i_a(t)}{2} + i_{circ,a}(t) + \frac{I_{dc}}{3}$$

Los tres términos se suman instantáneamente. El pico de corriente de brazo ocurre cuando la
corriente de fase, la de circulación y la DC están en fase:

$$I_{ua,pico} = \frac{\hat{I}_{ac}}{2} + \hat{I}_{circ} + \frac{I_{dc}}{3}$$

Para un MMC con \( \hat{I}_{ac} = 1.5\,\text{pu} \) (sobrecarga), \( \hat{I}_{circ} = 0.15\,\text{pu} \),
\( I_{dc}/3 = 0.25\,\text{pu} \): \( I_{ua,pico} = 0.75 + 0.15 + 0.25 = 1.15\,\text{pu} \).
Esto es 15 % más que la corriente de fase — los IGBTs deben estar dimensionados para este pico.

**Limitación por brazo en el control.** La referencia de corriente del lazo de corriente AC
(\( i_d^* \), \( i_q^* \)) debe limitarse de forma que la corriente de brazo resultante no supere
\( I_{brazo,max} \):

$$\left|\frac{i_a}{2}\right| + |i_{circ}| + \left|\frac{I_{dc}}{3}\right| \leq I_{brazo,max}$$

El límite de \( i_d^* \) e \( i_q^* \) se recalcula en cada período teniendo en cuenta la
corriente de circulación actual y la corriente DC. Durante faltas AC donde \( i_q^* \) sube para
soportar la tensión de red, la corriente de brazo puede superar \( I_{brazo,max} \) aunque la
corriente de fase no supere el límite de fase — un error habitual es usar solo el limitador de
fase sin comprobar el límite de brazo.

**Corriente de falta DC y su distribución por brazo.** Ante una falta DC bipolar, la corriente de
falta se distribuye por los seis brazos del MMC a través de los diodos de antiparalelo (en MMC-HB).
La corriente instantánea máxima por brazo es:

$$I_{brazo,falta} \approx \frac{I_{fault,pico}}{3}$$

(con distribución uniforme en las tres fases). Para los valores del ejemplo (cable 300 km):
\( I_{brazo,falta} \approx 14.3\,\text{kA}/3 \approx 4.8\,\text{kA} \) — mucho mayor que la
corriente de brazo nominal (1–2 kA). Las restricciones de la corriente de falta son las que
determinan el rating de los IGBTs, no la operación nominal.

<div class="cfig"><img src="figuras/mmc-modelo-control-analisis.png" alt="MMC: energía de brazos, CCSC y jerarquía de control"><div class="cap">Variación de energía de los brazos superior e inferior (componentes a \( \omega_0 \) y \( 2\omega_0 \)), corriente de circulación con y sin CCSC, jerarquía de las cuatro capas de control del MMC, y efecto del balanceo de tensiones de los submódulos.</div></div>
