---
titulo: Convertidor back-to-back (dos VSC, bus DC común)
slug: convertidor-back-to-back
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: []
objetivos: [desacoplar dos sistemas AC con flujo de potencia bidireccional, modelar el bus DC compartido]
tags: [back-to-back, vsc, bus-dc, hvdc, eolica, full-converter, bidireccional, modelado]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-06-30
relacionados: [convertidor-vsc, dinamica-bus-dc, control-tension-bus-dc, eolica-mppt, modelo-bateria-bess]
referencias:
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
  - "Teodorescu, Liserre, Rodríguez, Grid Converters for PV and Wind Power Systems, Wiley 2011"
---

## Definición
Dos [[convertidor-vsc|VSC]] conectados por un **bus DC común** (condensador compartido). Cada
convertidor mira a un sistema AC distinto; el bus DC los **desacopla** y permite flujo de potencia
**bidireccional** entre ambos lados. Es la topología base del aerogenerador full-converter (Tipo 4),
el lado-rotor del DFIG (Tipo 3), los accionamientos regenerativos y el HVDC-VSC.

## Fundamento teórico
El acoplamiento entre los dos convertidores es **solo energético**, a través del condensador de bus:
$$ C\,\frac{dV_{dc}}{dt}=i_{dc,1}-i_{dc,2}=\frac{P_1-P_{loss}-P_2}{V_{dc}} $$
donde \( P_1 \) entra por el convertidor 1 (p. ej. lado-máquina/generación) y \( P_2 \) sale por el
convertidor 2 (lado-red). En equilibrio \( P_1\approx P_2 \) y \( V_{dc} \) es constante; cualquier
desbalance carga o descarga el condensador. La **energía** almacenada \( E=\tfrac12 C V_{dc}^2 \) actúa
de pulmón: dimensionarla fija cuánto cae \( V_{dc} \) ante un transitorio de potencia.

Reparto típico de tareas (un convertidor fija la tensión del bus, el otro la potencia):
- **Lado-red (VSC-2):** regula \( V_{dc} \) (lazo externo) y \( Q \) hacia red. Su \( i_d^\* \) sale del
  lazo de tensión DC; ver [[control-tension-bus-dc]].
- **Lado-máquina/fuente (VSC-1):** impone par/velocidad o sigue MPPT ([[eolica-mppt]]). Inyecta o
  extrae \( P_1 \), que el lado-red debe evacuar para mantener \( V_{dc} \).

Visto desde el bus DC, **el convertidor que controla potencia se comporta como una [[dinamica-bus-dc|CPL]]**
(impedancia incremental negativa) → puede desestabilizar el lazo de tensión si el condensador es pequeño.

<div class="cfig"><img src="figuras/convertidor-back-to-back-topologia.png" alt="topologia back-to-back de dos VSC con bus DC comun"><div class="cap">Dos VSC comparten un único condensador de bus DC: el acoplamiento entre ambos lados es solo energético ($C\,\dot V_{dc}=(P_1-P_2)/V_{dc}$). Uno regula la tensión del bus y el otro controla la potencia/par; cada lado ve al otro como una simple fuente o sumidero de potencia, lo que desacopla dos redes AC distintas en frecuencia y fase.</div></div>

## 1 — La dinámica del bus DC desde el balance de potencia
**Paso 1 — energía almacenada en el condensador.** El bus DC es un condensador \( C \) cargado a \( V_{dc} \). Su energía es

$$ E=\tfrac12\,C\,V_{dc}^2 $$

**Paso 2 — balance de potencia.** La energía del condensador sube cuando entra más potencia de la que sale. El convertidor 1 inyecta \( P_1 \), el convertidor 2 extrae \( P_2 \), y las pérdidas internas consumen \( P_{loss} \):

$$ \frac{dE}{dt}=P_1-P_{loss}-P_2 $$

**Paso 3 — derivar la energía.** Derivando \( E=\tfrac12 C V_{dc}^2 \) respecto al tiempo (regla de la cadena, \( C \) constante):

$$ \frac{dE}{dt}=\tfrac12\,C\cdot 2\,V_{dc}\,\frac{dV_{dc}}{dt}=C\,V_{dc}\,\frac{dV_{dc}}{dt} $$

**Paso 4 — igualar y despejar.** Igualando los dos pasos anteriores:

$$ C\,V_{dc}\,\frac{dV_{dc}}{dt}=P_1-P_{loss}-P_2 $$

$$ \boxed{\;C\,\frac{dV_{dc}}{dt}=\frac{P_1-P_{loss}-P_2}{V_{dc}}=i_{dc,1}-i_{dc,2}\;} $$

donde se ha identificado \( i_{dc,k}=P_k/V_{dc} \) (corriente DC equivalente de cada puente). En equilibrio \( dV_{dc}/dt=0 \) exige \( P_1=P_2+P_{loss} \): el lado-red debe evacuar toda la potencia que el lado-máquina inyecta, o \( V_{dc} \) deriva. Esta es la razón física de por qué un lado regula \( V_{dc} \): es el único grado de libertad que cierra el balance. Linealizada en torno a \( V_{dc0} \) da el modelo del lazo de tensión ([[control-tension-bus-dc]]); el término \( P_2/V_{dc} \) con \( P_2 \) fija es el que aporta la pendiente negativa de la [[dinamica-bus-dc|CPL]].

## Cuándo y por qué se usa
Siempre que haya que **interconectar dos redes AC desacopladas en frecuencia/fase** con control
independiente y bidireccionalidad: evacuación de eólica/PV de velocidad variable, HVDC-VSC, BESS
([[modelo-bateria-bess]]) con convertidor de red + DC-DC, motores con frenado regenerativo. El bus DC
permite que cada lado vea al otro como una simple fuente/sumidero de potencia.

## Procedimiento de diseño (genérico)
1. Define el reparto: qué convertidor regula \( V_{dc} \) (normalmente el de **red rígida**) y cuál
   controla \( P/par \).
2. Dimensiona \( C \) por la **caída admisible de \( V_{dc} \)** ante el mayor escalón de potencia y por
   el rizado de conmutación: \( C\ge \dfrac{P_{max}\,\Delta t}{V_{dc}\,\Delta V_{dc}} \).
3. Diseña los lazos de corriente de ambos VSC (rápidos, idénticos) y por encima el lazo de \( V_{dc} \)
   (lento, \( \sim\!1/10 \) del de corriente).
4. Añade **feedforward de la potencia del otro lado** ([[control-feedforward]]): mide \( P_1 \) y úsala
   como referencia anticipada en el lazo de \( V_{dc} \) para que el escalón no lo vea como perturbación.
5. Verifica margen del lazo DC frente al efecto CPL ([[dinamica-bus-dc|carga de potencia constante (CPL)]]).

## Ejemplo de aplicación real
**Problema:** aerogenerador Tipo 4 de 2 MW, \( V_{dc}=1100\,\text{V} \). Una ráfaga sube \( P_1 \) de 1 a
2 MW en 50 ms; el lado-red tarda \( \Delta t=5\,\text{ms} \) en seguir. ¿Qué \( C \) limita la
sobretensión de bus a \( \Delta V_{dc}\le 50\,\text{V} \)?

El exceso transitorio es \( \Delta P\approx1\,\text{MW} \) durante \( \Delta t \). Energía a absorber:
\( \Delta E=\Delta P\cdot\Delta t=10^6\times5\times10^{-3}=5\,\text{kJ} \). Como
\( \Delta E\approx C V_{dc}\,\Delta V_{dc} \): \( C\ge \dfrac{5000}{1100\times50}\approx 91\,\text{mF} \).
Se elige \( C=100\,\text{mF} \). Con feedforward de \( P_1 \) el lado-red sube \( i_d^\* \) casi al instante
y el condensador real puede ser bastante menor; sin él, hay que sobredimensionarlo.

## Ejemplo de código
```python
def bus_dc_dynamics(vdc, P1, P2, C, Ploss=0.0):
    # P1 entra (lado-maquina), P2 sale (lado-red); devuelve dVdc/dt
    idc1 = P1 / vdc
    idc2 = (P2 + Ploss) / vdc
    return (idc1 - idc2) / C
```

## Parámetros y valores típicos
\( V_{dc} \): 1.1–1.2 kV (BT) a ±320 kV (HVDC). Energía de bus \( E/S \): 5–40 ms (J por VA). Rizado de
\( V_{dc} \): 1–2 %. Ancho de banda lazo de tensión DC: 10–50 Hz; lazo de corriente: 0.5–2 kHz.

## Errores comunes
- Que **ambos** convertidores intenten fijar \( V_{dc} \) → conflicto; solo uno lo regula.
- Condensador subdimensionado → sobre/subtensiones de bus y disparo por el efecto CPL.
- Olvidar el feedforward de potencia → el lazo de \( V_{dc} \) lento ve cada cambio de viento/carga como
  perturbación y oscila.
- Chopper de frenado ausente: ante hueco de red el lado-red no evacúa y \( V_{dc} \) se dispara.

## 3 — Modelo en dq del back-to-back

Cada VSC se modela en el marco de referencia dq síncrono (ver [[marco-dq]]). Para el VSC1 (grid-side converter, GSC), la ecuación vectorial del filtro de acoplamiento \( L \) con resistencia de pérdidas \( R \) es:

$$ L\,\frac{d}{dt}\begin{pmatrix}i_d\\i_q\end{pmatrix} = \begin{pmatrix}v_{d,conv}\\v_{q,conv}\end{pmatrix} - \begin{pmatrix}v_{d,grid}\\v_{q,grid}\end{pmatrix} - \begin{pmatrix}R & -\omega_0 L\\ \omega_0 L & R\end{pmatrix}\begin{pmatrix}i_d\\i_q\end{pmatrix} $$

Los términos de acoplamiento cruzado \( \pm\omega_0 L i_{q,d} \) se cancelan con desacoplo feedforward (ver [[desacoplo-dq]]), reduciendo cada eje a un lazo PI independiente. El reparto habitual de tareas es:

- **VSC1 (GSC):** regula la tensión del bus DC (eje d) y la potencia reactiva hacia la red (eje q). La referencia de corriente \( i_d^* \) viene del lazo externo de \( V_{dc} \).
- **VSC2 (MSC, machine-side converter):** regula el par eléctrico y el flujo (si es una máquina síncrona de imanes permanentes, PMSG) o la tensión y frecuencia de una carga pasiva. Su referencia de par sigue la curva MPPT del generador.

El desacoplo entre VSC1 y VSC2 es completo a nivel eléctrico: el único nexo es la potencia que fluye por el bus DC.

## 4 — Control del bus DC

La variable de control natural del bus DC es \( v_{dc}^2 \) (proporcional a la energía), cuya dinámica es lineal respecto a la potencia:

$$ \frac{d}{dt}\left(\frac{1}{2}C_{dc}v_{dc}^2\right) = P_{VSC1} - P_{losses} - P_{VSC2} $$

Definiendo \( w = v_{dc}^2 \), la planta del lazo de tensión DC es un integrador puro: \( \dot{w} = (2/C_{dc})(P_{in} - P_{out}) \). Un controlador PI con esta planta es el diseño estándar:

$$ i_{d,VSC1}^* = \frac{C_{dc}}{2V_{dc0}}\left(K_p(v_{dc}^*{}^2 - v_{dc}^2) + K_i\int(v_{dc}^*{}^2 - v_{dc}^2)\,dt\right) $$

**Balance de potencia:** \( P_{VSC1} + P_{VSC2} = P_{losses} \). En régimen permanente, el GSC debe evacuar exactamente la potencia que inyecta el MSC. Cualquier desbalance deriva \( v_{dc} \).

**Separación de escalas:** el ancho de banda del lazo DC debe ser unas 10 veces menor que el del lazo de corriente:

$$ \omega_{dc} \approx \frac{\omega_{ci}}{10} $$

Esta separación garantiza que cuando el lazo DC genera una referencia de corriente \( i_d^* \), el lazo de corriente ya está establecido y la corriente real sigue fielmente la referencia. Si los anchos de banda se solapan, el lazo DC ve la dinámica del lazo de corriente como parte de su planta y el diseño del PI se complica.

## 5 — Aplicación en eólica DFIG y PMSG

El back-to-back es la topología estándar para aerogeneradores de velocidad variable de potencia media-alta:

**PMSG (generador síncrono de imanes permanentes):** el VSC2 rectifica la potencia del generador operando a velocidad variable (seguimiento MPPT con par \( T_{ref} = K_{opt}\omega_r^2 \)). El VSC1 inyecta potencia a la red a frecuencia fija (50 Hz), manteniendo el bus DC. Todo el flujo de potencia pasa por el back-to-back: es un **full-converter** (Tipo 4). El desacoplo es total: la frecuencia del generador es independiente de la de la red.

**DFIG (generador de inducción doblemente alimentado):** solo una fracción de la potencia total (la potencia de deslizamiento \( P_{slip} = s \cdot P_{total} \), con \( s \) el deslizamiento, típ. ±30 %) fluye por el back-to-back vía el rotor. El estátor se conecta directamente a la red. Esto reduce el tamaño del convertidor al 30 % de la potencia nominal, una ventaja económica importante en aerogeneradores multi-MW.

**FRT (Fault Ride-Through):** durante un hueco de tensión de red, el VSC1 no puede evacuar potencia (la tensión de red es baja); el bus DC sube. Las estrategias son:
1. **Chopper de freno (braking resistor):** disipa el exceso de potencia en una resistencia conectada al bus DC, limitando la sobretensión.
2. **Limitación de potencia del VSC2:** reduce \( P_{VSC2} \) para no sobrecargar el bus DC; implica reducir el par del generador y cambiar el punto de operación.

## 6 — Pérdidas y eficiencia

Las pérdidas de un VSC se dividen en dos componentes principales:

**Pérdidas de conducción** en los semiconductores (IGBT, SiC MOSFET): proporcionales a \( I^2 R_{on} \), donde \( R_{on} \) es la resistencia de conducción en directa. Dominan a alta corriente (alta carga).

**Pérdidas de conmutación** proporcionales a la energía por conmutación \( E_{sw} \) y a la frecuencia de conmutación \( f_s \): \( P_{sw} = E_{sw} \cdot f_s \). Dominan a alta frecuencia y a tensión de bus elevada.

**Pérdidas de cobre** en el filtro de acoplamiento: \( P_{Cu} = R_{filtro} \cdot \langle i^2 \rangle \), donde \( \langle i^2 \rangle \) es el valor cuadrático medio de la corriente, incluyendo el rizado de conmutación.

La eficiencia típica es del 97–98 % por convertidor individual, lo que da una eficiencia total del back-to-back de 94–96 %. Este valor depende fuertemente de la frecuencia de conmutación, la tecnología de semiconductores (Si vs SiC) y el punto de carga.

**Gestión térmica:** la temperatura de unión \( T_j \) de los semiconductores debe mantenerse por debajo de \( T_{j,max} \) (tipicalmente 150–175 °C para Si, 175–200 °C para SiC). La resistencia térmica unión-disipador \( R_{th,j-h} \) fija la temperatura de unión: \( T_j = T_{h} + P_{loss} \cdot R_{th,j-h} \). El límite térmico, no el eléctrico, es frecuentemente el que impone la corriente máxima continua del convertidor.

<div class="cfig"><img src="../figuras/convertidor-back-to-back-analisis.png" alt="Modelo y control del convertidor back-to-back: esquema de potencias, bus DC, eficiencia y FRT"><div class="cap">Cuatro paneles: esquema de flujo de potencia del back-to-back con VSC1 y VSC2; respuesta de la tensión del bus DC ante un escalón de referencia; curva de eficiencia en función de la carga para cada convertidor y el sistema completo; comportamiento de potencias y tensión DC durante un hueco de tensión (FRT).</div></div>

## Conceptos relacionados
- [[convertidor-vsc]] · [[dinamica-bus-dc]] · [[control-tension-bus-dc]] · [[eolica-mppt]]

## Referencias
- Yazdani, Iravani, 2010.
- Teodorescu, Liserre, Rodríguez, 2011.
