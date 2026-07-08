---
titulo: Control de tensión del bus DC
slug: control-tension-bus-dc
categoria: control
tipo: tecnica
nivel: intermedio
proyectos: []
objetivos: [mantener constante la tensión del bus DC regulando el intercambio de potencia]
tags: [bus-dc, lazo-externo, balance-energia, rectificador-activo, back-to-back, intermedio]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-30
relacionados: [control-cascada, dinamica-bus-dc, convertidor-vsc, controlador-pid]
referencias:
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
  - "Blaabjerg et al., Overview of Control and Grid Synchronization, IEEE TIE 2006"
---

## Definición
Lazo **externo** que regula la tensión del condensador del bus DC a su referencia, generando la
**referencia de corriente activa** \( i_d^* \) (o de potencia) para el lazo interno de corriente.
Es el lazo que cierra el balance de energía en rectificadores activos y convertidores back-to-back.

## Fundamento teórico
El bus DC es un integrador de potencia (ver [[dinamica-bus-dc]]). En términos de energía
\( E=\tfrac12 C v_{dc}^2 \):
$$ \frac{dE}{dt}=\tfrac12 C\frac{d(v_{dc}^2)}{dt}=P_{in}-P_{out} $$
La planta \( v_{dc}\!\leftarrow\!P \) es **no lineal** (aparece \( v_{dc}^2 \)). Dos enfoques:
- **Linealizar** en torno a \( V_{dc0} \): \( C V_{dc0}\,\dot{\tilde v}_{dc}=\tilde P \) → planta
  integradora \( 1/(C V_{dc0}\,s) \), se cierra con un PI.
- Controlar **\( v_{dc}^2 \)** (la energía) como variable: la planta se vuelve **lineal exacta**
  \( \tfrac{C}{2}\,\dot{(v_{dc}^2)}=P \).

Con tensión de red alineada al eje d (\( e_q=0 \)), \( P\approx \tfrac32 e_d i_d \), así que el PI
de tensión produce \( i_d^* \). El **feedforward** de la potencia de carga \( P_{out} \) acelera el
rechazo. La **separación de bandas** es crítica: el lazo de tensión debe ser bastante más lento que
el de corriente (factor ~5–10) y, en monofásico, más lento que el rizado de \( 2\omega \).

<div class="cfig"><img src="figuras/control-tension-bus-dc-escalon.png" alt="tension del bus DC ante un escalon de carga con y sin feedforward"><div class="cap">Tras un escalón de carga, el PI solo deja caer $V_{dc}$ hasta que su integrador rehace el balance de potencia; el feedforward de la potencia de carga aporta esa potencia de inmediato y la caída casi desaparece. El lazo se controla sobre $v_{dc}^2$ (energía) para que la planta sea lineal exacta.</div></div>

## 1 — Por qué se controla \( v_{dc}^2 \) y no \( v_{dc} \): linealizar el integrador de energía
**Paso 1 — el balance de energía es exacto.** La energía almacenada en el condensador es \( E=\tfrac12 C v_{dc}^2 \). Su derivada es la potencia neta que entra al bus:

$$ \frac{dE}{dt}=P_{in}-P_{out}\equiv P $$

Esto es una ley física exacta, sin aproximaciones.

**Paso 2 — la planta en \( v_{dc} \) es no lineal.** Si se elige \( v_{dc} \) como variable controlada, hay que derivar \( E \) por la regla de la cadena:

$$ \frac{dE}{dt}=\frac{d}{dt}\!\left(\tfrac12 C v_{dc}^2\right)=C\,v_{dc}\,\dot v_{dc}=P \quad\Longrightarrow\quad \dot v_{dc}=\frac{P}{C\,v_{dc}} $$

La planta \( v_{dc}\!\leftarrow\!P \) tiene a \( v_{dc} \) **multiplicando** (en el denominador): la ganancia del integrador depende del propio estado. Es un sistema **no lineal**; un PI diseñado para \( V_{dc0} \) ve otra ganancia cuando \( v_{dc} \) se aleja.

**Paso 3 — cambio de variable \( u=v_{dc}^2 \).** Definimos la nueva variable de control \( u\equiv v_{dc}^2 \). Su derivada es:

$$ \dot u=\frac{d(v_{dc}^2)}{dt}=2\,v_{dc}\,\dot v_{dc} $$

Sustituyendo en el balance de energía \( \tfrac12 C\,\dot u = \tfrac12 C\cdot 2 v_{dc}\dot v_{dc}=C v_{dc}\dot v_{dc}=P \):

$$ \boxed{\;\frac{C}{2}\,\dot u = P \quad\Longleftrightarrow\quad \frac{u(s)}{P(s)}=\frac{2}{C\,s}\;} $$

La planta es ahora un **integrador puro lineal exacto**, sin dependencia del punto de operación: ganancia \( 2/(Cs) \) constante para cualquier \( v_{dc} \). Por eso el lazo trabaja sobre \( v_{dc}^{*2}-v_{dc}^2 \) en vez de \( v_{dc}^*-v_{dc} \): no es una preferencia, es lo que vuelve la planta invariante y permite un PI con margen garantizado en todo el rango.

**Paso 4 — comprobación de la linealización clásica.** Si en vez del cambio de variable se linealiza \( \dot v_{dc}=P/(C v_{dc}) \) en torno a \( V_{dc0} \) con \( v_{dc}=V_{dc0}+\tilde v_{dc} \), \( P=\tilde P \) pequeña, se obtiene \( C V_{dc0}\,\dot{\tilde v}_{dc}=\tilde P \), planta \( 1/(C V_{dc0}\,s) \). Es lineal **solo cerca** de \( V_{dc0} \); el enfoque en \( u=v_{dc}^2 \) la hace exacta en todo punto, que es la ventaja decisiva durante arranques y huecos.

## 2 — Sintonía del PI de tensión por asignación de cruce
**Paso 1 — lazo abierto.** Con la planta lineal \( G(s)=2/(Cs) \) y un PI \( C(s)=K_{pv}\bigl(1+\tfrac{1}{T_{iv}s}\bigr) \), la ganancia de lazo es

$$ L(s)=K_{pv}\!\left(1+\frac{1}{T_{iv}s}\right)\frac{2}{Cs} $$

**Paso 2 — dominio del término proporcional en el cruce.** Se elige \( 1/T_{iv}\ll\omega_{cv} \) (cero del PI una década por debajo del cruce) para que en \( \omega_{cv} \) el PI se comporte casi como ganancia pura \( K_{pv} \). Entonces el módulo de lazo en el cruce es

$$ |L(j\omega_{cv})|\approx K_{pv}\frac{2}{C\,\omega_{cv}}=1 $$

**Paso 3 — despejar la ganancia.** De \( |L|=1 \):

$$ \boxed{\;K_{pv}=\frac{C\,\omega_{cv}}{2}\;} $$

**Paso 4 — números del ejemplo.** Con \( C=10\,\text{mF} \) y \( f_{cv}=200\,\text{Hz} \Rightarrow \omega_{cv}=2\pi\cdot200=1257\,\text{rad/s} \):

$$ K_{pv}=\frac{0.01\times1257}{2}=6.3\ \text{(en base }P\text{–}v_{dc}^2) $$

y el tiempo integral \( T_{iv}\approx10/\omega_{cv}\approx8\,\text{ms} \) deja el cero una década por debajo, aportando el margen de fase. La regla \( \omega_{cv}\approx\omega_{ci}/5 \) (ver [[control-cascada]]) garantiza que el lazo interno de corriente sea "instantáneo" para este lazo; y \( \omega_{cv}<2\omega_{red} \) evita realimentar el rizado de \( 100\,\text{Hz} \) como referencia de corriente.

## Cuándo y por qué se usa
En el lado red de cualquier rectificador activo / convertidor back-to-back (el del usuario), en
STATCOM con almacenamiento, y en general cuando el bus DC alimenta una carga y hay que mantener su
tensión pese a perturbaciones de potencia.

## Procedimiento de diseño (genérico)
1. Modela el bus (\( C \), \( V_{dc0} \)) y linealiza, o usa \( v_{dc}^2 \) como variable.
2. Diseña el lazo interno de corriente primero ([[desacoplo-dq]], [[control-cascada]]).
3. Sintoniza el PI de tensión con \( \omega_{v}\approx(1/5\text{–}1/10)\,\omega_{c,i} \).
4. En monofásico/desequilibrio, filtra o haz \( \omega_v < 2\omega \) (evitar realimentar el rizado
   de 100 Hz como referencia de corriente).
5. Añade feedforward de \( P_{out} \) y **anti-windup** ([[anti-windup]]) al límite de \( i_d^* \).

## Ejemplo de aplicación real
**Problema:** Convertidor back-to-back lado red, \( C=10\,\text{mF} \), \( V_{dc0}=1.2\,\text{kV} \), carga de 500 kW. El lazo de corriente ya diseñado croza a \( f_{ci}=1\,\text{kHz} \). Diseñar el lazo de tensión DC.

Planta (usando \( v_{dc}^2 \) como variable): \( P\to\tfrac{C}{2}\dot{(v_{dc}^2)} \), ganancia \( 2/(Cs) \). Ancho de banda objetivo: \( f_{cv}=f_{ci}/5=200\,\text{Hz} \), \( \omega_{cv}=1257\,\text{rad/s} \). PI: \( K_{pv}=C\,\omega_{cv}/2=0.01\times1257/2=6.3\,\text{(W/V}^2\text{)/...} \); aplicando la fórmula en la base de \( v_{dc}^2 \) y \( P \). Con feedforward de carga: ante un escalón de carga del 10 % (50 kW), la caída de \( V_{dc} \) se reduce de 22 V a 6 V (factor 3.7 de mejora). Si \( \omega_{cv} \) se sube a 500 Hz: el rizado de \( 2\times50=100\,\text{Hz} \) del bus se realimenta y distorsiona la corriente de red — este es el límite superior para \( f_{cv} \).

## Ejemplo de código
```python
def dc_voltage_loop(vdc_ref, vdc, P_load, ed, pi_v, C):
    # control sobre energia (planta lineal): error en vdc^2
    e = vdc_ref**2 - vdc**2
    P_ref = pi_v(e) + P_load                 # feedforward de carga
    id_ref = (2/3)*P_ref/max(ed, 1e-3)       # referencia de corriente activa
    return id_ref
```

## Parámetros y valores típicos
Ancho de banda del lazo de tensión: 10–50 Hz (muy por debajo del de corriente). Rizado de
\( v_{dc} \) admisible 1–2 %. \( V_{dc} > 2\sqrt2\,V_{LL}/\sqrt3 \) para no saturar la modulación.

## Errores comunes
- Lazo de tensión demasiado rápido → realimenta el rizado de \( 2\omega \) y distorsiona la corriente.
- Tratar la planta como lineal lejos de \( V_{dc0} \) sin usar \( v_{dc}^2 \).
- Olvidar anti-windup en el límite de \( i_d^* \) (saturación durante arranques/huecos).
- Ignorar que una carga CPL añade impedancia negativa ([[dinamica-bus-dc|estabilidad del bus DC con CPL]]).

## 3 — Modelo dinámico del bus DC

**Balance de potencias.** El condensador del bus DC acumula la diferencia entre potencia entrante
\( P_{in} \) y saliente \( P_{out} \). En términos de la tensión del condensador:

$$ C_{dc}\,V_{dc}\,\dot V_{dc} = P_{in} - P_{out} $$

Esto se puede reescribir como la derivada de la energía \( W = \tfrac12 C_{dc}V_{dc}^2 \):

$$ \dot W = P_{in} - P_{out} \qquad \Leftrightarrow \qquad \frac{C_{dc}}{2}\frac{d(V_{dc}^2)}{dt} = P_{in}-P_{out} $$

**Linealización alrededor de \( V_{dc,0} \).** Con pequeñas perturbaciones
\( V_{dc} = V_{dc,0}+\tilde v_{dc} \), \( P = \tilde P \) (perturbación de potencia):

$$ C_{dc}\,V_{dc,0}\,\dot{\tilde v}_{dc} = \tilde P \quad\Rightarrow\quad G_{lin}(s) = \frac{1}{C_{dc}\,V_{dc,0}\,s} $$

Planta integradora con ganancia que depende de \( V_{dc,0} \): el PI diseñado para el nominal pierde
margen cuando \( V_{dc} \) se aleja (p. ej. durante un hueco de red).

**Control en \( V_{dc}^2 \): planta lineal exacta.** Cambiando la variable de salida a \( u = V_{dc}^2 \):

$$ \frac{C_{dc}}{2}\,\dot u = P_{in}-P_{out} \quad\Rightarrow\quad G_{exact}(s) = \frac{2}{C_{dc}\,s} $$

La ganancia es constante en todo el rango de operación: el PI diseñado para el nominal funciona
igual durante el arranque, la recuperación tras un hueco y la operación a carga parcial. Esta es
la razón por la que el lazo de tensión industrial siempre opera sobre \( V_{dc}^{*2}-V_{dc}^2 \).

**Corriente del condensador.** La corriente que fluye por el condensador es la diferencia entre la
corriente aportada por el convertidor y la absorbida por la carga:

$$ i_C = i_{conv} - i_{carga} = C_{dc}\,\dot V_{dc} $$

En régimen permanente \( i_C = 0 \) y toda la corriente del convertidor va a la carga. Los
transitorios de potencia (escalones de carga, cambios de referencia) descargan o cargan el condensador
hasta que el lazo de control restablece el equilibrio.

## 4 — Diseño del lazo de control de \( V_{dc} \)

**Planta en \( V_{dc}^2 \).** Integrador puro \( G_v(s) = 2/(C_{dc}\,s) \). El lazo de corriente
(más rápido) se trata como ganancia unitaria en la banda del lazo de tensión.

**Controlador PI.** \( C_v(s) = K_{pv}(1+1/(T_{iv}\,s)) \). La función de lazo es:

$$ L_v(s) = K_{pv}\!\left(1+\frac{1}{T_{iv}\,s}\right)\frac{2}{C_{dc}\,s} $$

Se elige el cero del PI una década por debajo del cruce: \( 1/T_{iv} \ll \omega_{cv} \).

**Sintonía por asignación de cruce.** En \( \omega_{cv} \), el PI se aproxima a ganancia pura
\( K_{pv} \) y la condición \( |L_v(j\omega_{cv})| = 1 \) da:

$$ \boxed{K_{pv} = \frac{C_{dc}\,\omega_{cv}}{2}} \qquad T_{iv} = \frac{10}{\omega_{cv}} $$

Con \( T_{iv} = 10/\omega_{cv} \), el cero del PI está una década por debajo del cruce y el margen
de fase es ~84° — la integral prácticamente no afecta en el cruce.

**Regla de separación de escalas.** El lazo de corriente debe ser ~5–10 veces más rápido:

$$ \omega_{cv} \approx \frac{\omega_{ci}}{5\text{–}10} $$

Y el lazo de tensión debe ser más lento que el doble de la frecuencia de red para no realimentar
el rizado de 100 Hz (en monofásico) o el de 300 Hz (en trifásico ideal, pero con desbalance el
rizado de 100 Hz también aparece):

$$ \omega_{cv} < 2\omega_0 = 2\times2\pi\times50 = 628\,\text{rad/s} \quad(\approx 100\,\text{Hz}) $$

**Feedforward de la potencia de carga.** Si se mide o estima \( P_{out} \), se puede sumar
directamente a la referencia de potencia del lazo:

$$ P_{ref} = C_v(s)(V_{dc}^{*2}-V_{dc}^2) + P_{out} $$

El feedforward cancela la perturbación de carga antes de que el integrador tenga que actuar,
reduciendo la caída de \( V_{dc} \) en un factor 3–5.

**Anti-windup.** Cuando la referencia de corriente \( i_d^* \) se limita (por saturación del lazo
de corriente o por la limitación de corriente del convertidor), el integrador del PI de tensión sigue
integrando el error aunque la salida ya está saturada — esto es el wind-up. La solución es el
back-calculation: cuando la salida se satura, se alimenta al integrador con la diferencia entre la
salida real y la saturada con una ganancia \( 1/T_{aw} \).

## 5 — CPL y estabilidad del bus DC

**Carga de potencia constante (CPL, Constant Power Load).** Una carga regulada (p. ej. un
convertidor DC-DC con lazo de tensión en la salida) mantiene su potencia constante
\( P_{CPL} = V_{dc}\,I_{CPL} = \text{const} \). Si \( V_{dc} \) cae, \( I_{CPL} \) sube para
mantener la potencia — impedancia de entrada negativa:

$$ Z_{CPL}(j\omega) = -\frac{V_{dc}^2}{P_{CPL}} \quad (\text{resistencia negativa en baja frecuencia}) $$

Esta impedancia negativa es la raíz de la inestabilidad del bus DC: el condensador del bus ve una
"resistencia de descarga" negativa que, si supera la resistencia de amortiguamiento del bus, hace
crecer exponencialmente las oscilaciones de tensión.

**Criterio de Middlebrook (pequeña señal).** El sistema es estable si la impedancia de la fuente
\( Z_S(j\omega) \) (el convertidor fuente con su lazo de control) es menor que la impedancia de
la carga \( Z_L(j\omega) \) en todo el rango de frecuencias:

$$ |Z_S(j\omega)| < |Z_L(j\omega)| \quad \forall\,\omega $$

Para una CPL: \( |Z_L| = V_{dc}^2/P_{CPL} = \) constante. Para el convertidor con lazo PI de
tensión: \( |Z_S| \) crece a baja frecuencia (el lazo de control impone baja impedancia en la BW)
pero tiene un pico en la resonancia LC del filtro de salida. Si ese pico supera \( V_{dc}^2/P_{CPL} \),
el sistema es inestable.

**Efecto de múltiples CPL.** Si hay \( n \) CPL con potencias \( P_1, \ldots, P_n \), sus
impedancias negativas se suman:

$$ R_{neg} = -\sum_{k=1}^{n}\frac{V_{dc}^2}{P_k} = -\frac{V_{dc}^2}{P_{total}} $$

El riesgo aumenta linealmente con la potencia total de las CPL. En microrredes DC con múltiples
convertidores DC-DC regulados (servidores, drives), la estabilidad del bus es una preocupación
de diseño crítica.

**Mitigaciones:**

1. **Amortiguamiento virtual.** Añadir una componente de realimentación de la derivada de la
   tensión DC al lazo de tensión, equivalente a colocar una resistencia virtual en paralelo con
   el condensador sin pérdidas reales.
2. **BESS con droop.** Una batería con control droop amortece las oscilaciones del bus: si
   \( V_{dc} \) cae, la batería inyecta corriente, actuando como amortiguador activo.
3. **Aumentar \( C_{dc} \).** Incrementar la capacidad del bus reduce la frecuencia de resonancia
   y el pico de impedancia, aleja el riesgo de Middlebrook.
4. **Limitar el BW del lazo de carga.** Si el lazo del convertidor CPL es más lento, su
   impedancia negativa solo aparece a baja frecuencia donde la fuente tiene baja impedancia.

## 6 — Droop de tensión DC y reparto de carga

En sistemas con varios convertidores alimentando el mismo bus DC (microrredes DC, HVDC MTDC), se
necesita un mecanismo para que compartan la potencia sin comunicación centralizada.

**Característica droop.** Cada convertidor \( i \) implementa una relación lineal entre la tensión
del bus y su corriente de salida:

$$ V_{dc,i} = V_{dc,0} - R_{d,i}\,I_{dc,i} $$

donde \( R_{d,i} = \Delta V_{dc,max}/I_{dc,i,max} \) es el coeficiente de droop. El convertidor
"cede" tensión a medida que entrega más corriente, igual que la regulación de una fuente de
alimentación con resistencia interna.

**Reparto de carga.** Con dos convertidores de coeficientes \( R_{d,1} \), \( R_{d,2} \), la
corriente se reparte en razón inversa a los coeficientes:

$$ \frac{I_{dc,1}}{I_{dc,2}} = \frac{R_{d,2}}{R_{d,1}} $$

Para reparto igualitario se elige \( R_{d,1} = R_{d,2} \). Para que el convertidor 1 aporte el
doble: \( R_{d,1} = R_{d,2}/2 \).

**Compromiso regulación–reparto.** Un \( R_d \) grande mejora el reparto pero empeora la
regulación de \( V_{dc} \) (caída mayor). Un \( R_d \) pequeño mejora la regulación pero empeora
el reparto (el convertidor más cercano al bus acapara más carga). El compromiso estándar es una
caída de \( 5\,\% \) de \( V_{dc} \) a plena carga.

**Restauración secundaria.** El droop solo deja \( V_{dc} \) en el valor nominal si la potencia
demandada es exactamente la nominal. Para cargas parciales o ante pérdidas, \( V_{dc} \) se aleja
de \( V_{dc,0} \). Un lazo secundario lento (tiempo de respuesta de segundos, comunicación admisible)
ajusta el punto base \( V_{dc,0} \) de todos los convertidores para restaurar la tensión nominal.
La latencia de la comunicación no es crítica porque el lazo secundario opera en escala de segundos.

**Aplicación HVDC MTDC.** En una red HVDC con 3–4 terminales, si el terminal rector del bus DC
(que controla \( V_{dc} \)) falla, todos los demás ven una tensión libre. Con droop:

$$ \Delta V_{dc} = \frac{\Delta P_{desequilibrio}}{\sum_i k_{d,i}} $$

La variación de tensión DC es proporcional al desequilibrio de potencia e inversamente proporcional
a la suma de las ganancias de droop. Los demás terminales compensan automáticamente la pérdida del
terminal rectificador en menos de 100 ms — sin comunicación, solo por la variación de \( V_{dc} \).

<div class="cfig"><img src="../figuras/control-tension-bus-dc-analisis.png" alt="Control del bus DC: lazo Vdc, CPL y droop entre convertidores"><div class="cap">Respuesta de \( V_{dc} \) ante un escalón de carga con y sin control; Bode del lazo de tensión (planta integradora + PI); criterio de Middlebrook para CPL — zona de riesgo donde la impedancia de la fuente supera a la de la carga negativa; y característica droop de tres convertidores compartiendo el bus DC.</div></div>

## Conceptos relacionados
- [[dinamica-bus-dc]] · [[control-cascada]] · [[convertidor-vsc]] · [[desacoplo-dq]]

## Referencias
- Yazdani, Iravani, 2010.
- Blaabjerg et al., *Overview of Control and Grid Synchronization*, IEEE TIE 2006.
