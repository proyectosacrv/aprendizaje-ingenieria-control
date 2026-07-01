---
titulo: Bus DC — dinámica, dimensionado, CPL y estabilidad
slug: dinamica-bus-dc
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: [03-DataCenter-IA]
objetivos: [modelar y dimensionar el condensador del bus DC, modelar la carga de potencia constante y analizar la estabilidad del bus]
tags: [bus-dc, condensador, balance-energia, rizado, hold-up, CPL, resistencia-negativa, estabilidad, microrred-dc, datacenter, middlebrook, amortiguamiento-activo, droop-dc]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-01
relacionados: [control-tension-bus-dc, criterio-middlebrook, impedancia-salida-estabilidad, potencia-instantanea-dq, robustez-parametrica]
referencias:
  - "Mohan, Undeland, Robbins, Power Electronics, Wiley"
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
  - "Emadi et al., Constant Power Loads and Negative Impedance Instability, IEEE TVT 2006"
  - "Riccobono, Santi, Comprehensive Review of Stability Criteria for DC Power Systems, IEEE TIA 2014"
  - "Middlebrook, Input Filter Design for Switching Regulators, IEEE PESC 1976"
---

## Definición
El bus DC es el nudo de continua que une dos etapas de electrónica de potencia y absorbe el desbalance instantáneo de potencia entre ellas mediante un condensador. Esta ficha reúne tres líneas inseparables en cualquier estudio del bus: su dinámica y dimensionado (condensador, rizado, autonomía), el modelo de la carga característica que cuelga de él (la CPL, carga de potencia constante) y el análisis de estabilidad del conjunto. La CPL es precisamente lo que puede desestabilizar el bus, y entender por qué requiere recorrer toda la cadena desde la física hasta los autovalores.

## Qué hay a cada lado del bus (contexto genérico)
El condensador del bus no distingue qué etapas alimenta. Aguas arriba hay una fuente que entrega potencia \(P_{in}\) al bus: puede ser un rectificador activo, la etapa de red de un back-to-back, un convertidor DC-DC desde una batería o un panel PV. Aguas abajo hay una o varias cargas que extraen \(P_{out}\): un inversor que vierte a una red AC, un convertidor punto-de-carga (POL) que alimenta servidores, un accionamiento de motor. Para el bus, cada lado es simplemente una corriente inyectada o extraída; lo único que importa de cada etapa es su potencia y, para la estabilidad, cómo varía esa potencia cuando cambia la tensión del bus.

## Resumen ejecutivo
| Criterio | Fórmula | Domina cuando |
|---|---|---|
| Rizado 1φ | \(C \geq \dfrac{P}{\omega\,V_{dc}\,\Delta V_{pp}}\) | Conexión monofásica |
| Hold-up | \(C \geq \dfrac{2\,P_{out}\,t_h}{V_{dc0}^2 - V_{min}^2}\) | Siempre (factor 5-10×) |
| Estabilidad | \(P < P_{crit} = \dfrac{V^2 R_f C_{dc}}{L_f}\) | Con filtro inductivo y CPL |
| Amort. activo | \(\dfrac{1}{R_d} > \dfrac{P}{V^2} - \frac{R_f}{L_f/C_{dc}^{-1}}\) | CPL cercana a \(P_{crit}\) |

<div class="cfig"><img src="figuras/dinamica-bus-dc-respuesta.png" alt="respuesta del bus DC a un escalon de carga"><div class="cap">El condensador integra el desbalance: sin control (rojo) Vdc cae ante un exceso de carga; el lazo de tensión (azul) lo recupera ajustando Pin.</div></div>

<div class="cfig"><img src="figuras/dinamica-bus-dc-analisis.png" alt="analisis completo del bus DC: rizado, hold-up, locus de polos y amortiguamiento"><div class="cap">Los cuatro aspectos críticos del bus DC: (a) el rizado monofásico a 100 Hz domina en amplitud frente al trifásico equilibrado, donde solo queda el PWM; (b) la descarga exponencial del condensador fija el hold-up, con los círculos marcando el cruce de Vmin=665 V; (c) al subir la potencia CPL el par de polos del filtro LC se desplaza a la derecha y cruza el eje imaginario en Pcrit; (d) la parte real de la admitancia del bus es negativa sin amortiguamiento, y el activo la lleva a valores positivos sin pérdidas.</div></div>

## 1 — De la corriente del condensador a \( C\,dV_{dc}/dt = i_{in} - i_{out} \) y al balance de energía

**Paso 1 — ley constitutiva del condensador.** La carga almacenada es \(q = C\,V_{dc}\). Con \(C\) constante:

$$ i_C = \frac{dq}{dt} = \frac{d(C\,V_{dc})}{dt} = C\,\frac{dV_{dc}}{dt} $$

La corriente del condensador es proporcional a la tasa de cambio de tensión.

**Paso 2 — KCL en el nodo del bus.** Al nudo DC entra la corriente de la fuente \(i_{in}\) y salen la de la carga \(i_{out}\) y la del condensador \(i_C\):

$$ i_{in} = i_{out} + i_C \;\;\Longrightarrow\;\; i_C = i_{in} - i_{out} $$

**Paso 3 — ecuación de estado del bus.** Igualando Pasos 1 y 2:

$$ \boxed{\;C\,\frac{dV_{dc}}{dt} = i_{in} - i_{out}\;} $$

El condensador integra el **desbalance** de corriente. Sin control la tensión deriva; con control el lazo cierra la diferencia.

**Paso 4 — versión en energía.** La energía almacenada es \(E = \tfrac12 C V_{dc}^2\). Derivando con respecto al tiempo y usando el Paso 3:

$$ \frac{dE}{dt} = C\,V_{dc}\frac{dV_{dc}}{dt} = V_{dc}(i_{in} - i_{out}) = P_{in} - P_{out} $$

Por tanto:

$$ \boxed{\;\frac{dE}{dt} = P_{in} - P_{out}\;} $$

En la variable \(E\) (equivalentemente \(V_{dc}^2\)) la planta es **lineal**: la energía evoluciona exactamente como el integrador de la diferencia de potencias. Por eso el lazo de tensión se cierra sobre \(V_{dc}^2\) en lugar de sobre \(V_{dc}\) (ver [[control-tension-bus-dc]]): la planta linealizada en \(V_{dc}^2\) tiene ganancia constante \(1/C\) independiente del punto de operación, mientras que la planta en \(V_{dc}\) tiene una ganancia \(1/(C\,V_{dc})\) que varía con la tensión.

**Nota sobre la no linealidad.** Si la carga es una resistencia \(R\), entonces \(i_{out} = V_{dc}/R\) y la ecuación sí contiene \(V_{dc}\) en el lado derecho, haciendo el sistema no lineal pero estable (tiene un polo en \(-1/(RC)\)). La CPL, en cambio, hace \(i_{out} = P/V_{dc}\), lo que introduce una no linealidad con resistencia incremental negativa, como se verá en el apartado 2.

## 2 — Por qué la CPL da resistencia incremental negativa y fija \( P_{crit} \)

**Paso 1 — la relación i–V de la carga.** Una carga de potencia constante mantiene \(P = V\,i\) fija. La corriente es:

$$ i_{cpl}(V) = \frac{P}{V} $$

Es una hipérbola decreciente: a menor tensión, **más** corriente. Al revés que una resistencia, donde \(i = V/R\) crece con \(V\).

**Paso 2 — linealizar en torno al punto de operación \(V_0\).** La estabilidad de pequeña señal la determina la pendiente de la curva i–V:

$$ \left.\frac{di_{cpl}}{dV}\right|_{V_0} = -\frac{P}{V_0^2} < 0 $$

La conductancia incremental es negativa. Su inverso es la **resistencia incremental**:

$$ \boxed{\;r_{cpl} = \left(\frac{di_{cpl}}{dV}\right)^{-1} = -\frac{V_0^2}{P} < 0\;} $$

Una resistencia positiva disipa energía y amortigua; una resistencia **negativa** inyecta energía a la resonancia LC aguas arriba. Por eso la CPL desamortigua el bus (no pasividad; ver [[impedancia-salida-estabilidad]]).

<div class="cfig"><img src="figuras/carga-potencia-constante-cpl-iv.png" alt="curva i-V de una CPL con pendiente incremental negativa"><div class="cap">La CPL sigue i=P/V: si la tensión cae, la corriente sube para mantener la potencia. Su pendiente incremental ∂i/∂V=−P/V² es negativa (resistencia incremental −V²/P), al revés que una resistencia. Esa pendiente negativa desamortigua los filtros LC aguas arriba.</div></div>

**Paso 3 — modelo del filtro LC con CPL.** Con un filtro \(L_f, R_f\) aguas arriba y condensador de bus \(C_{dc}\) con la CPL, los estados son \((i_L, V_{dc})\). Las ecuaciones de estado son:

$$ L_f\,\dot{i}_L = V_{fuente} - R_f\,i_L - V_{dc} $$

$$ C_{dc}\,\dot{V}_{dc} = i_L - i_{cpl}(V_{dc}) = i_L - \frac{P}{V_{dc}} $$

Linealizando alrededor del punto \((I_{L0}, V_0)\) con \(\delta i_L = i_L - I_{L0}\), \(\delta V = V_{dc} - V_0\):

$$ \delta\dot{i}_L = -\frac{R_f}{L_f}\delta i_L - \frac{1}{L_f}\delta V $$

$$ \delta\dot{V} = \frac{1}{C_{dc}}\delta i_L - \frac{d}{dV}\!\left(\frac{P}{V}\right)\!\bigg|_{V_0}\!\cdot\,\delta V = \frac{1}{C_{dc}}\delta i_L + \frac{P}{V_0^2\,C_{dc}}\delta V $$

La matriz de estado del sistema linealizado es:

$$ A = \begin{bmatrix}-\dfrac{R_f}{L_f} & -\dfrac{1}{L_f}\\[0.9em]\dfrac{1}{C_{dc}} & \dfrac{P}{V_0^2\,C_{dc}}\end{bmatrix} $$

El término \(+P/(V_0^2\,C_{dc})\) en la posición (2,2) es la huella de la CPL: tiene signo positivo en la diagonal, reduce el amortiguamiento total. Con carga resistiva ese término sería \(-1/(R\,C_{dc}) < 0\), siempre estable.

**Paso 4 — condición de estabilidad por la traza.** Para un sistema \(2\times2\) con par de polos complejos conjugados, la parte real de los autovalores es \(\text{tr}(A)/2\). Los polos cruzan al semiplano derecho cuando la traza cambia de signo. Imponiendo \(\text{tr}(A) < 0\):

$$ -\frac{R_f}{L_f} + \frac{P}{V_0^2\,C_{dc}} < 0 \;\;\Longrightarrow\;\; \frac{P}{V_0^2\,C_{dc}} < \frac{R_f}{L_f} $$

Despejando la potencia máxima admisible:

$$ \boxed{\;P_{crit} = \frac{V_0^2\,R_f\,C_{dc}}{L_f}\;} $$

Por encima de \(P_{crit}\) la traza es positiva y el bus oscila de forma creciente. La fórmula revela las palancas de diseño: más resistencia de cable \(R_f\) o más capacidad de bus \(C_{dc}\) suben \(P_{crit}\); más inductancia de cable \(L_f\) lo baja. Como \(R_f\) es incierta (temperatura, longitud de cable), se opera con margen amplio (factor \(\geq 2\)) respecto a \(P_{crit}\).

## 3 — Rizado de tensión: derivación para monofásico y trifásico

### 3.1 Sistema monofásico

La potencia instantánea entregada por una fuente monofásica de fase con tensión pico \(V_p\) e intensidad pico \(I_p\) desfasada un ángulo \(\varphi\) es:

$$ p(t) = v(t)\,i(t) = V_p\cos(\omega t)\cdot I_p\cos(\omega t - \varphi) $$

Expandiendo con la identidad trigonométrica \(\cos A\cos B = \tfrac12[\cos(A-B)+\cos(A+B)]\):

$$ p(t) = \frac{V_p I_p}{2}\cos\varphi + \frac{V_p I_p}{2}\cos(2\omega t - \varphi) $$

El primer término es la potencia activa media \(P_0 = \tfrac12 V_p I_p\cos\varphi\). El segundo es la componente oscilatoria a doble frecuencia:

$$ p_{osc}(t) = P_0\cos(2\omega t - \varphi) $$

Esta componente no puede ser absorbida por la carga CPL (que extrae \(P_0\) constante), así que la absorbe el condensador. La corriente que fluye por el condensador es:

$$ i_C(t) = \frac{p_{osc}(t)}{V_{dc}} = \frac{P_0}{V_{dc}}\cos(2\omega t - \varphi) $$

Integrando para obtener el rizado de tensión:

$$ \Delta V_{dc}(t) = \frac{1}{C}\int i_C\,dt = \frac{P_0}{2\omega\,V_{dc}\,C}\sin(2\omega t - \varphi) $$

La amplitud pico del rizado es \(\Delta\hat{V} = P_0/(2\omega V_{dc} C)\). El valor pico a pico (máximo menos mínimo) es el doble:

$$ \boxed{\;\Delta V_{dc,pp} = \frac{P_0}{\omega\,V_{dc}\,C}\;} $$

**Criterio de diseño (rizado < 1%).** Imponiendo \(\Delta V_{dc,pp} < 0.01\,V_{dc}\):

$$ C \geq \frac{P_0}{\omega\,V_{dc}\cdot 0.01\,V_{dc}} = \frac{P_0}{0.01\,\omega\,V_{dc}^2} $$

Para \(P_0=100\) kW, \(\omega=2\pi\cdot50\), \(V_{dc}=700\) V:

$$ C \geq \frac{100\,000}{0.01\cdot 314\cdot 490\,000} \approx 6.5\;\text{mF} $$

### 3.2 Sistema trifásico equilibrado

En el sistema trifásico equilibrado en DQ, la potencia instantánea es (ver [[potencia-instantanea-dq]]):

$$ p(t) = \frac{3}{2}(v_d\,i_d + v_q\,i_q) = \text{constante} $$

No hay componente oscilatoria de red: la potencia es perfectamente constante si las tres fases están equilibradas. El condensador de bus no ve ningún rizado de red; el único rizado proviene de la conmutación PWM.

**Rizado por conmutación PWM.** La corriente del inductor del convertidor oscila con amplitud \(\Delta i_L\) a la frecuencia de conmutación \(f_{sw}\). En el caso más desfavorable (ciclo de trabajo 50%), la corriente del condensador es una onda triangular a \(f_{sw}\) de amplitud \(\Delta i_L/2\). El rizado de tensión resultante es:

$$ \Delta V_{dc,PWM} = \frac{\Delta i_L}{8\,C\,f_{sw}} $$

Para \(\Delta i_L = 10\) A, \(C = 10\) mF, \(f_{sw}=10\) kHz: \(\Delta V_{dc,PWM} \approx 12.5\) mV, completamente despreciable.

### 3.3 Comparativa numérica

| Parámetro | Valor | Rizado resultante |
|---|---|---|
| Monofásico, \(C=10\) mF, \(P=100\) kW, \(V_{dc}=700\) V | \(\omega=314\) rad/s | \(\Delta V_{pp}=4.55\) V (0.65%) |
| Trifásico equilibrado (red) | — | 0 V (red no aporta) |
| Trifásico PWM, \(\Delta i_L=10\) A, \(f_{sw}=10\) kHz | \(C=10\) mF | \(\approx 12.5\) mV (despreciable) |

El rizado monofásico es **tres órdenes de magnitud** mayor que el de conmutación trifásica.

## 4 — Hold-up time: derivación y criterio de dimensionado

### 4.1 Definición y derivación

El hold-up time \(t_h\) es el tiempo que el bus puede sostener \(V_{dc} > V_{min}\) cuando desaparece la potencia de entrada completamente (\(P_{in}=0\)).

**Paso 1 — energía disponible.** Al inicio del hold-up, la energía almacenada en el condensador es:

$$ E_0 = \frac{1}{2}\,C\,V_{dc0}^2 $$

La energía mínima aceptable (correspondiente a la tensión mínima \(V_{min}\)):

$$ E_{min} = \frac{1}{2}\,C\,V_{min}^2 $$

La energía disponible para alimentar la carga durante el hold-up:

$$ \Delta E = E_0 - E_{min} = \frac{1}{2}\,C\,(V_{dc0}^2 - V_{min}^2) $$

**Paso 2 — balance de energía durante el hold-up.** Con \(P_{in}=0\) y la carga extrayendo \(P_{out}\) constante (comportamiento CPL del sistema aguas abajo):

$$ \frac{dE}{dt} = -P_{out} \;\;\Longrightarrow\;\; \Delta E = P_{out}\,t_h $$

**Paso 3 — despejar la capacidad mínima.** Igualando las dos expresiones de \(\Delta E\):

$$ \frac{1}{2}\,C\,(V_{dc0}^2 - V_{min}^2) = P_{out}\,t_h $$

$$ \boxed{\;C \geq \frac{2\,P_{out}\,t_h}{V_{dc0}^2 - V_{min}^2}\;} $$

**Paso 4 — evolución temporal de la tensión.** Dado que \(E(t) = E_0 - P_{out}\,t\):

$$ \frac{1}{2}\,C\,V_{dc}(t)^2 = \frac{1}{2}\,C\,V_{dc0}^2 - P_{out}\,t $$

$$ V_{dc}(t) = \sqrt{V_{dc0}^2 - \frac{2\,P_{out}\,t}{C}} $$

La caída no es lineal sino con raíz cuadrada: más rápida al inicio (condensador lleno, cae rápido en tensión) y más lenta al acercarse a \(V_{min}\).

### 4.2 Cuándo domina hold-up vs rizado

Comparando las dos expresiones de \(C\) para los mismos parámetros (\(P=100\) kW, \(V_{dc}=700\) V, \(V_{min}=665\) V, \(t_h=20\) ms, rizado 1%):

$$ C_{holdup} = \frac{2\cdot100\,000\cdot0.02}{700^2 - 665^2} = \frac{4000}{47775} \approx 8.4\;\text{mF} $$

$$ C_{rizado,1\%} = \frac{100\,000}{314\cdot700\cdot7} \approx 6.5\;\text{mF} $$

El hold-up es ya 1.3× más exigente con rizado del 1%; con rizado del 2% sería 2.6× más exigente. En aplicaciones con PFC (hold-up de 20 ms a Vmin = Vdc − 5%), el criterio de hold-up **siempre domina** por un factor 5–10×.

### 4.3 Corriente eficaz del condensador

El dimensionado solo por capacidad es insuficiente: los condensadores electrolíticos tienen un límite de corriente RMS por calentamiento interno (\(\text{ESR}\cdot I_{rms}^2\)). La corriente eficaz a 100 Hz en el caso monofásico:

$$ I_{C,rms} = \frac{P_0}{\sqrt{2}\,V_{dc}} = \frac{100\,000}{\sqrt{2}\cdot700} \approx 101\;\text{A} $$

Este valor debe compararse con la hoja de datos del condensador. Para valores altos (>50 A a 100 Hz) se recurre a arrays de electrolíticos en paralelo o condensadores de film.

## 5 — Criterio de Middlebrook para el bus DC

### 5.1 Enunciado original y adaptación al bus DC

El criterio de Middlebrook [[criterio-middlebrook]] establece que, para un convertidor DC-DC alimentado por una red con impedancia de salida \(Z_s(j\omega)\), la estabilidad está garantizada si:

$$ |Z_s(j\omega)| < |Z_{in}(j\omega)| \;\;\forall\,\omega $$

donde \(Z_{in}\) es la impedancia de entrada del convertidor cargado con su regulación propia. Para el bus DC con CPL, la impedancia de entrada de la CPL vista desde el bus es la resistencia incremental negativa:

$$ Z_{cpl}(j\omega) = r_{cpl} = -\frac{V^2}{P} $$

El módulo \(|r_{cpl}| = V^2/P\) es constante con la frecuencia. La impedancia de la fuente (filtro de distribución) es:

$$ Z_s(j\omega) = R_f + j\omega L_f $$

### 5.2 Condición de Middlebrook para la CPL

La condición \(|Z_s| < |Z_{cpl}|\) para todo \(\omega\) se traduce en:

$$ |R_f + j\omega L_f| < \frac{V^2}{P} \;\;\forall\,\omega $$

**En DC (\(\omega = 0\)):** la condición es simplemente \(R_f < V^2/P\), es decir \(P < V^2/R_f\). Esto coincide exactamente con \(P < P_{crit}\) cuando \(C_{dc}/L_f = 1/R_f\); en general es una condición diferente (Middlebrook es más conservadora porque aplica para todo \(\omega\), no solo en DC).

**A alta frecuencia (\(\omega \to \infty\)):** \(|Z_s| \to \omega L_f \to \infty\), de modo que la condición de Middlebrook siempre se viola en alta frecuencia. Esto indica que el criterio de Middlebrook original es demasiado conservador para este caso: un sistema puede ser estable aunque viole Middlebrook en alta frecuencia si el margen de fase es suficiente.

**Aplicación práctica.** Para un bus DC con filtro \(L_f=0.5\) mH, \(R_f=0.1\) Ω, \(V_{dc}=700\) V, \(P_{CPL}=100\) kW:

$$ |r_{cpl}| = \frac{700^2}{100\,000} = 4.9\;\Omega $$

La condición Middlebrook en DC: \(R_f = 0.1\;\Omega < 4.9\;\Omega\). Se cumple con margen 49×. La cruce de \(|Z_s(\omega)| = |r_{cpl}|\) ocurre en:

$$ \omega_{cross} = \frac{\sqrt{|r_{cpl}|^2 - R_f^2}}{L_f} \approx \frac{4.9}{0.5\cdot10^{-3}} = 9800\;\text{rad/s}\;\;(1.56\;\text{kHz}) $$

Por encima de 1.56 kHz el módulo de la fuente supera al de la CPL: hay que verificar el margen de fase en esa frecuencia.

### 5.3 Relación entre Middlebrook y Pcrit

La condición de estabilidad por traza (\(P < P_{crit} = V^2 R_f C_{dc}/L_f\)) es equivalente a Middlebrook en DC multiplicado por \(C_{dc}/L_f\). Cuando el factor \(C_{dc}/L_f\) es grande (bus muy capacitivo, cable inductivo), \(P_{crit}\) puede ser varias veces mayor que \(V^2/R_f\); en ese caso la condición de traza es más laxa que Middlebrook. La diferencia es que la traza mide la estabilidad global del par de polos, mientras que Middlebrook garantiza estabilidad en todo el rango de frecuencias.

## 6 — Amortiguamiento activo del bus DC

### 6.1 Principio físico

El amortiguamiento activo consiste en que el convertidor fuente modula su corriente de referencia en función de la tensión del bus, emulando una resistencia sin disipar energía real. La ley de control añadida al convertidor es:

$$ i_{ref}(t) = i_{ref,0} - \frac{V_{dc}(t) - V_{dc,nom}}{R_d} $$

Cuando \(V_{dc}\) sube respecto al nominal, el convertidor reduce su corriente de referencia (inyecta menos); cuando baja, la aumenta. El efecto es una conductancia adicional \(1/R_d\) en el modelo del bus.

### 6.2 Modelo con amortiguamiento activo

El término de amortiguamiento activo modifica la ecuación de la corriente del bus:

$$ C_{dc}\,\dot{V}_{dc} = i_L + \frac{1}{R_d}(V_{dc,nom} - V_{dc}) - \frac{P}{V_{dc}} $$

Al linealizar:

$$ C_{dc}\,\delta\dot{V}_{dc} = \delta i_L - \frac{\delta V_{dc}}{R_d} + \frac{P}{V_0^2}\,\delta V_{dc} $$

La matriz \(A\) del sistema con amortiguamiento activo queda:

$$ A_{activo} = \begin{bmatrix}-\dfrac{R_f}{L_f} & -\dfrac{1}{L_f}\\[0.9em]\dfrac{1}{C_{dc}} & \dfrac{P}{V_0^2\,C_{dc}} - \dfrac{1}{R_d\,C_{dc}}\end{bmatrix} $$

### 6.3 Nueva condición de estabilidad y elección de \(R_d\)

La condición \(\text{tr}(A_{activo}) < 0\) es ahora:

$$ -\frac{R_f}{L_f} + \frac{P}{V_0^2\,C_{dc}} - \frac{1}{R_d\,C_{dc}} < 0 $$

Despejando la nueva potencia crítica:

$$ P_{crit,activo} = V_0^2\,C_{dc}\left(\frac{R_f}{L_f} + \frac{1}{R_d\,C_{dc}}\right) = P_{crit} + \frac{V_0^2}{R_d\,L_f/L_f} = P_{crit} + \frac{V_0^2}{R_d}\cdot\frac{C_{dc}}{C_{dc}} $$

Simplificando:

$$ \boxed{\;P_{crit,activo} = V_0^2\,C_{dc}\left(\frac{R_f}{L_f} + \frac{1}{R_d\,C_{dc}}\right) = P_{crit} + \frac{V_0^2}{R_d\,L_f}\cdot\frac{L_f}{1} \cdot\frac{1}{C_{dc}^{-1}} \;} $$

Forma compacta:

$$ P_{crit,activo} = \frac{V_0^2\,C_{dc}}{L_f}\left(R_f + \frac{L_f}{R_d\,C_{dc}}\right) = P_{crit} + \frac{V_0^2}{R_d} $$

El amortiguamiento activo con resistencia virtual \(R_d\) aumenta la potencia crítica en \(V_0^2/R_d\), independientemente del filtro.

**Elección de \(R_d\).** Para garantizar un margen de estabilidad \(k_m > 1\) sobre la potencia de operación \(P_{op}\):

$$ P_{crit,activo} \geq k_m\,P_{op} \;\;\Longrightarrow\;\; \frac{V_0^2}{R_d} \geq k_m\,P_{op} - P_{crit} $$

$$ R_d \leq \frac{V_0^2}{k_m\,P_{op} - P_{crit}} $$

Si \(P_{crit} > k_m\,P_{op}\), el sistema ya tiene margen suficiente sin amortiguamiento activo.

### 6.4 Ejemplo numérico

Parámetros: \(L_f = 0.5\) mH, \(R_f = 0.1\) Ω, \(C_{dc} = 10\) mF, \(V_0 = 700\) V, \(P_{op} = 100\) kW.

$$ P_{crit} = \frac{700^2 \cdot 0.1 \cdot 10\cdot10^{-3}}{0.5\cdot10^{-3}} = \frac{490\,000 \cdot 10^{-3}}{0.5\cdot10^{-3}} = 980\;\text{kW} $$

El margen sin amortiguamiento activo ya es \(980/100 = 9.8\times\), suficiente para este caso. Si se añade \(R_d = 5\) Ω:

$$ P_{crit,activo} = 980 + \frac{700^2}{5} = 980 + 98\,000 \;\text{kW} \approx 98.9\;\text{MW} $$

El incremento es enorme porque \(V_0^2/R_d\) es grande. En la práctica, la limitación es la dinámica del lazo de corriente del convertidor, que no puede seguir referencias por encima de su ancho de banda (\(\sim\) kHz).

**Ventaja vs amortiguamiento pasivo.** Una rama R-C pasiva en paralelo con el bus (amortiguamiento pasivo) disipa \(P_{disipada} = V^2_{rizado}/R_d\); con rizado de 4.5 V y \(R_d = 5\) Ω, la disipación es \(4.5^2/5 \approx 4\) W (despreciable, pero existe). El amortiguamiento activo no tiene pérdidas porque el convertidor ya está ahí y simplemente ajusta su referencia.

## 7 — Bus DC de microrred: múltiples fuentes y cargas en paralelo

### 7.1 Modelo generalizado

En una microrred DC hay \(N\) fuentes (rectificador, BESS, PV) cada una con su impedancia de salida \(Z_{i,fuente}(s)\) y \(M\) cargas CPL extrayendo potencias \(P_j\). El bus equivalente tiene:

- Condensador de bus: \(C_{dc}\) (o suma de condensadores de cada convertidor)
- Admitancia total de las fuentes: \(Y_{total}(s) = \displaystyle\sum_{i=1}^{N}\frac{1}{Z_{i,fuente}(s)}\)
- Resistencia incremental negativa total de las CPL: \(r_{cpl,total} = -\dfrac{V^2}{\sum_j P_j}\)

### 7.2 Condición de estabilidad colectiva

La condición de traza para el sistema generalizado es que la suma de las conductancias de las fuentes en DC supere la conductancia negativa total de las CPL:

$$ \sum_{i=1}^{N}\frac{R_{f,i}}{Z_{i,fuente}^2}\bigg|_{\omega=0} > \frac{\sum_j P_j}{V^2} $$

Con droop DC, cada fuente tiene la característica \(V_i = V_0 - R_{d,i}\,I_i\). La conductancia en DC de la fuente \(i\) es \(1/R_{d,i}\). La condición de estabilidad con droop DC es:

$$ \boxed{\;\sum_{i=1}^{N}\frac{1}{R_{d,i}} > \frac{\sum_j P_j}{V^2}\;} $$

Esta condición tiene una interpretación física clara: la conductancia total de las fuentes (cuanto más suelta corriente cuando cae la tensión) debe superar la conductancia incremental negativa total de las CPL (cuanto más corriente exigen cuando cae la tensión).

### 7.3 Reparto de carga por droop DC

Con droop DC, cada fuente regula su tensión de salida según \(V_i = V_0 - R_{d,i}\,I_i\). En estado estacionario todas las fuentes comparten la misma tensión de bus \(V_{bus}\), lo que impone:

$$ I_i = \frac{V_0 - V_{bus}}{R_{d,i}} $$

La corriente se reparte en proporción inversa a los droop: la fuente con menor droop aporta más corriente. Si se quiere reparto proporcional a la potencia nominal \(S_i\):

$$ R_{d,i} = \frac{\Delta V_{max}}{I_{max,i}} = \frac{0.05\,V_0}{S_i/V_0} $$

### 7.4 Ejemplo con tres fuentes y cinco CPL

Tres fuentes con \(R_{d,i} = 2\) Ω cada una, cinco CPL de 20 kW, \(V_{dc} = 700\) V:

$$ \text{Conductancia total fuentes:}\;\sum \frac{1}{R_{d,i}} = \frac{3}{2} = 1.5\;\text{S} $$

$$ \text{Conductancia CPL:}\;\frac{\sum P_j}{V^2} = \frac{100\,000}{490\,000} = 0.204\;\text{S} $$

Como \(1.5 > 0.204\), el sistema es estable. El margen es \(1.5/0.204 = 7.4\times\).

## 8 — Diseño iterativo: bus DC del datacenter IA

### 8.1 Especificaciones de partida

| Parámetro | Valor |
|---|---|
| Tensión nominal \(V_{dc}\) | 700 V ±5% (665–735 V) |
| Potencia CPL total | 100 kW |
| Hold-up | \(t_h = 20\) ms |
| Rizado máximo | 0.5% (\(\Delta V_{pp} < 3.5\) V) |
| Filtro de distribución | \(L_f = 0.5\) mH, \(R_f = 0.1\) Ω |
| Frecuencia de conmutación | \(f_{sw} = 10\) kHz |

### 8.2 Iteración 0 — primeras estimaciones

**C por hold-up (domina):**

$$ C_{holdup} = \frac{2\cdot100\,000\cdot0.02}{700^2 - 665^2} = \frac{4\,000}{47\,775} = 8.4\;\text{mF} $$

**C por rizado (trifásico equilibrado):** La red no aporta rizado; solo la conmutación. Con \(\Delta i_L = 5\) A (filtro bien diseñado):

$$ C_{ripple,PWM} = \frac{\Delta i_L}{8\cdot\Delta V_{pp}\cdot f_{sw}} = \frac{5}{8\cdot3.5\cdot10\,000} = 17.9\;\mu\text{F} $$

Completamente despreciable frente al hold-up.

**Elección inicial:** \(C = 10\) mF (holgura sobre el hold-up).

### 8.3 Iteración 1 — verificación de estabilidad

**Potencia crítica con \(C = 10\) mF:**

$$ P_{crit} = \frac{700^2 \cdot 0.1 \cdot 10\cdot10^{-3}}{0.5\cdot10^{-3}} = \frac{49\cdot10^4\cdot10^{-3}}{0.5\cdot10^{-3}} = 980\;\text{kW} $$

Margen: \(980/100 = 9.8\times\). Holgado. Se puede reducir \(C\) al mínimo de hold-up.

**Reducción a \(C = 8.5\) mF (mínimo):**

$$ P_{crit} = \frac{700^2 \cdot 0.1 \cdot 8.5\cdot10^{-3}}{0.5\cdot10^{-3}} = 833\;\text{kW} $$

Margen: \(833/100 = 8.3\times\). Aún holgado.

**Corriente RMS del condensador** (solo conmutación, trifásico):

$$ I_{C,rms,PWM} = \frac{\Delta i_L}{2\sqrt{3}} = \frac{5}{3.46} \approx 1.4\;\text{A} $$

Muy por debajo del límite térmico; el condensador no se calienta por corriente de conmutación.

### 8.4 Iteración 2 — amortiguamiento activo adicional

Aunque el margen de estabilidad (\(8.3\times\)) es más que suficiente, se añade amortiguamiento activo \(R_d = 5\) Ω para robustez ante variaciones de parámetros (cable más largo, temperatura):

$$ P_{crit,activo} = 833 + \frac{700^2}{5} = 833 + 98\,000 \approx 98.8\;\text{MW} $$

El margen nominal con amortiguamiento activo es \(988\times\). En la práctica el ancho de banda del convertidor limita la efectividad del amortiguamiento activo por encima de \(\sim 1\) kHz, pero para las perturbaciones relevantes del bus (tensiones de baja frecuencia) el margen es muy amplio.

### 8.5 Tabla de iteraciones

| Iteración | \(C\) [mF] | \(t_h\) [ms] | \(P_{crit}\) [kW] | Margen | \(\Delta V_{pp}\) [V] | Decisión |
|---|---|---|---|---|---|---|
| 0 (estimación) | 10.0 | 23.8 | 980 | 9.8× | 3.2 (PWM) | OK, reducir C |
| 1 (mínimo hold-up) | 8.5 | 20.2 | 833 | 8.3× | 2.7 | OK, añadir amort. activo |
| 2 (con \(R_d=5\) Ω) | 8.5 | 20.2 | \(\approx\)99 MW | \(\gg\)100× | 2.7 | Adoptar |

**Diseño adoptado:** \(C_{dc} = 8.5\) mF, amortiguamiento activo \(R_d = 5\) Ω en el convertidor de red.

## Cuándo y por qué se usa
Para elegir C (rizado, autonomía, vida útil), modelar el lazo de tensión, y analizar la estabilidad del bus frente a cargas CPL en microrredes DC, data centers, vehículos eléctricos, naval y aeronáutica.

## Procedimiento de diseño (genérico)
1. Identificar el tipo de fuente (1φ/3φ) y calcular el rizado dominante.
2. Dimensionar C por hold-up (criterio más exigente) y verificar el rizado.
3. Verificar la corriente eficaz del condensador (térmica); si excede el límite, poner condensadores en paralelo.
4. Modelar la CPL como resistencia incremental negativa \(-V^2/P\); calcular \(P_{crit} = V^2 R_f C_{dc}/L_f\).
5. Verificar el margen de estabilidad \(P_{crit}/P_{op} \geq 2\); si no, aumentar \(C_{dc}\) o añadir amortiguamiento activo.
6. Con múltiples fuentes y CPL, verificar la condición de droop DC: \(\sum 1/R_{d,i} > \sum P_j/V^2\).

## Ejemplo de código
```python
import numpy as np

# ---------- Parametros ----------
P, Vdc0, Vmin, th = 100e3, 700.0, 665.0, 20e-3
Lf, Rf, Cdc = 0.5e-3, 0.1, 8.5e-3
w = 2 * np.pi * 50

# ---------- Dimensionado ----------
C_holdup = 2 * P * th / (Vdc0**2 - Vmin**2)      # autonomia
C_ripple_1ph = P / (w * 0.01 * Vdc0**2)           # rizado 1φ < 1%
C = max(C_holdup, C_ripple_1ph)
print(f"C_holdup={C_holdup*1e3:.1f} mF  C_ripple={C_ripple_1ph*1e3:.1f} mF  → C={C*1e3:.1f} mF")

# ---------- Estabilidad: CPL ----------
P_crit = Vdc0**2 * Rf * Cdc / Lf
margen = P_crit / P
print(f"Pcrit={P_crit/1e3:.0f} kW  margen={margen:.1f}x")
A = np.array([[-Rf/Lf, -1/Lf], [1/Cdc, P/(Vdc0**2*Cdc)]])
print("autovalores:", np.linalg.eigvals(A))
estable = np.all(np.linalg.eigvals(A).real < 0)
print("estable:", estable)

# ---------- Amortiguamiento activo ----------
Rd = 5.0
P_crit_activo = P_crit + Vdc0**2 / Rd
print(f"Pcrit con amort. activo Rd={Rd}Ω: {P_crit_activo/1e3:.0f} kW")
```

## Parámetros y valores típicos
- Rizado \(\Delta V_{dc}\): 0.5–2% de \(V_{dc}\). Hold-up 10–20 ms (fuentes con PFC).
- Electrolíticos limitados por corriente RMS y temperatura; film para alta fiabilidad.
- En un rack de IA, P de la CPL de decenas a cientos de kW a \(V_{dc}\) = 400–800 V; resistencia incremental \(-V^2/P\) de fracciones de ohmio.
- Margen de estabilidad recomendado: \(P_{op}/P_{crit} \leq 0.5\) (factor 2), porque \(P_{crit}\) depende de parámetros inciertos.
- Droop DC típico: \(R_d = 2\)–\(5\) Ω para fuentes de 100 kW a 700 V (estatismo 0.3–0.7%).

## Errores comunes
- Dimensionar solo por capacidad e ignorar la corriente eficaz (sobrecalienta el condensador).
- Olvidar el rizado de \(2\omega\) en sistemas monofásicos o desequilibrados.
- Modelar la carga como resistencia constante (estable) cuando es CPL (puede inestabilizar).
- Asumir bus DC "rígido" cuando una CPL lo desestabiliza.
- Con múltiples fuentes, usar la condición de traza de una sola fuente en lugar de la condición de droop colectiva.
- Aplicar Middlebrook sin reconocer que es conservador en alta frecuencia para CPL.

## Uso en proyectos
- **03 - DataCenter-IA:** los servidores/GPUs (vía sus POL) son la CPL del bus DC; su resistencia incremental negativa fija la potencia crítica de estabilidad. Con \(L_f=0.5\) mH, \(R_f=0.1\) Ω, \(C_{dc}=8.5\) mF: \(P_{crit}=833\) kW, margen 8.3× sobre 100 kW. El hold-up de 20 ms fija el condensador mínimo en 8.4 mF.

## Conceptos relacionados
- [[control-tension-bus-dc]] · [[criterio-middlebrook]] · [[impedancia-salida-estabilidad]] · [[potencia-instantanea-dq]] · [[robustez-parametrica]]

## Referencias
- Mohan, Undeland, Robbins, Power Electronics, Wiley.
- Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010.
- Emadi et al., Constant Power Loads and Negative Impedance Instability, IEEE TVT 2006.
- Riccobono, Santi, Review of Stability Criteria for DC Power Systems, IEEE TIA 2014.
- Middlebrook, Input Filter Design for Switching Regulators, IEEE PESC 1976.
