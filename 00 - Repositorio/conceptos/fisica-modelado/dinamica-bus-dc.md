---
titulo: Bus DC — dinámica, dimensionado, CPL y estabilidad
slug: dinamica-bus-dc
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: [03-DataCenter-IA]
objetivos: [modelar y dimensionar el condensador del bus DC, modelar la carga de potencia constante y analizar la estabilidad del bus]
tags: [bus-dc, condensador, balance-energia, rizado, hold-up, CPL, resistencia-negativa, estabilidad, microrred-dc, datacenter]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-30
relacionados: [control-tension-bus-dc, criterio-middlebrook, impedancia-salida-estabilidad, potencia-instantanea-dq, robustez-parametrica]
referencias:
  - "Mohan, Undeland, Robbins, Power Electronics, Wiley"
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
  - "Emadi et al., Constant Power Loads and Negative Impedance Instability, IEEE TVT 2006"
  - "Riccobono, Santi, Comprehensive Review of Stability Criteria for DC Power Systems, IEEE TIA 2014"
---

## Definición
El bus DC es el nudo de continua que une dos etapas de electrónica de potencia y absorbe el desbalance instantáneo de potencia entre ellas mediante un condensador. Esta ficha reúne tres cosas inseparables en cualquier estudio del bus: su dinámica y dimensionado (condensador, rizado, autonomía), el modelo de la carga característica que cuelga de él (la CPL, carga de potencia constante) y el análisis de estabilidad del conjunto, porque la CPL es precisamente lo que puede desestabilizar el bus.

## Qué hay a cada lado del bus (contexto genérico)
El condensador del bus no distingue qué etapas alimenta. Aguas arriba hay una fuente que entrega potencia Pin al bus: puede ser un rectificador activo, la etapa de red de un back-to-back, un convertidor DC-DC elevador desde un generador o una batería, un panel PV. Aguas abajo hay una o varias cargas que extraen Pout: un inversor que vierte a una red AC, un convertidor punto-de-carga (POL) que alimenta servidores, un motor con su accionamiento. Para el bus, cada lado es simplemente una corriente inyectada o extraída; lo único que importa de cada etapa es su potencia y, para la estabilidad, cómo varía esa potencia cuando cambia la tensión del bus (de ahí el papel central de la CPL).

## Parte 1 — dinámica y dimensionado
Por la corriente del condensador:

C·dvdc/dt = i_in − i_out

o en energía E = (1/2)·C·vdc²:

dE/dt = P_in − P_out

La planta hacia la tensión es un integrador no lineal (de ahí controlar vdc²; ver [[control-tension-bus-dc]]).

Fuentes de rizado:
- Monofásico: la potencia instantánea pulsa a 2·omega → rizado de vdc a 100/120 Hz, delta_vdc ≈ P / (2·omega·C·Vdc).
- Trifásico equilibrado: la potencia es constante (ver [[potencia-instantanea-dq]]); el rizado dominante viene de la conmutación (6·f en rectificadores, fsw en VSC).

Dimensionado por autonomía (hold-up): ante pérdida de entrada, mantener vdc > Vmin durante un tiempo th:

C ≥ 2·P·th / (Vdc0² − Vmin²)

<div class="cfig"><img src="figuras/dinamica-bus-dc-respuesta.png" alt="respuesta del bus DC a un escalon de carga"><div class="cap">El condensador integra el desbalance: sin control (rojo) Vdc cae linealmente ante un exceso de carga; el lazo de tensión (azul) ajusta la potencia de entrada y lo recupera.</div></div>

## Parte 2 — carga de potencia constante (CPL)
Una CPL consume una potencia fija P independientemente de su tensión de alimentación. Es el comportamiento típico de un convertidor con su salida bien regulada (un POL de servidor, un motor con control de velocidad): aunque caiga la tensión de entrada, mantiene su potencia subiendo la corriente. Su corriente en función de la tensión del bus es:

i_cpl = P / V

Su conductancia incremental (pendiente di/dV) es negativa:

di_cpl/dV = −P / V² < 0

Equivale a una resistencia incremental negativa −V²/P. Esta resistencia negativa desamortigua los filtros LC aguas arriba: aporta energía a la resonancia en lugar de disiparla, lo que puede inestabilizar el bus. Es un caso concreto de no pasividad / resistencia negativa (ver [[impedancia-salida-estabilidad]]).

<div class="cfig"><img src="figuras/carga-potencia-constante-cpl-iv.png" alt="curva i-V de una CPL con pendiente incremental negativa"><div class="cap">La CPL sigue i=P/V: si la tensión cae, la corriente sube para mantener la potencia. Su pendiente incremental ∂i/∂V=−P/V² es negativa (resistencia incremental −V²/P), al revés que una resistencia. Esa pendiente negativa desamortigua los filtros LC aguas arriba.</div></div>

## Parte 3 — estabilidad del bus con CPL
Para un filtro Lf, Rf que alimenta un condensador Cdc con una CPL de potencia P, el modelo linealizado tiene matriz:

A = [[ −Rf/Lf, −1/Lf ],[ 1/Cdc, P/(V²· Cdc) ]]

El término P/(V²·Cdc) de la CPL es positivo en la diagonal: reduce el amortiguamiento. La traza se hace positiva (inestable) cuando:

P > P_crit = V²·Rf·Cdc / Lf

Es decir: más potencia, menos resistencia o menos condensador → inestable. Soluciones:
- Amortiguamiento pasivo: aumentar R (disipa) o rama R-C de damping.
- Más capacidad de bus Cdc (sube P_crit).
- Amortiguamiento activo: el convertidor fuente emula resistencia sin pérdidas.
- Impedance shaping y verificación por [[criterio-middlebrook]] / criterio de impedancia.

Es el análogo DC de la inestabilidad por impedancia que en AC aparece en el grid-following.

<div class="cfig"><img src="figuras/estabilidad-bus-dc-cpl-polos.png" alt="polos del bus DC con CPL al subir la potencia"><div class="cap">Al aumentar la potencia de la CPL, el término P/(V²Cdc) resta amortiguamiento y el par de polos del filtro L-C se desplaza a la derecha, cruzando el eje imaginario en P_crit=V²RfCdc/Lf. Por encima de esa potencia el bus oscila: hay que dejar margen o subir Cdc.</div></div>

## 1 — De la corriente del condensador a \( C\,dV_{dc}/dt=i_{in}-i_{out} \) y al balance de energía
**Paso 1 — ley constitutiva del condensador.** La carga almacenada es \( q=C\,V_{dc} \). Su corriente es la tasa de cambio de carga, y con \( C \) constante:

$$ i_C=\frac{dq}{dt}=\frac{d(C\,V_{dc})}{dt}=C\,\frac{dV_{dc}}{dt} $$

**Paso 2 — Kirchhoff de corrientes en el nodo del bus.** Al nudo DC entra la corriente de la fuente \( i_{in} \) y salen la de la carga \( i_{out} \) y la del condensador \( i_C \). La conservación de carga (lo que entra = lo que sale) impone:

$$ i_{in}=i_{out}+i_C\;\;\Longrightarrow\;\; i_C=i_{in}-i_{out} $$

**Paso 3 — igualar ambas expresiones de \( i_C \).** Combinando Pasos 1 y 2:

$$ \boxed{\;C\,\frac{dV_{dc}}{dt}=i_{in}-i_{out}\;} $$

El condensador integra el **desbalance** de corriente: si entra más de lo que sale, \( V_{dc} \) sube. Es un integrador puro (no hay término en \( V_{dc} \) en el lado derecho si las corrientes no dependen de él), de ahí que sin control la tensión derive.

**Paso 4 — versión en energía.** La energía del condensador es \( E=\tfrac12 C V_{dc}^2 \). Derivando y usando el Paso 3:

$$ \frac{dE}{dt}=C\,V_{dc}\frac{dV_{dc}}{dt}=V_{dc}\,(i_{in}-i_{out})=P_{in}-P_{out} $$

es decir \( \boxed{\,\dfrac{dE}{dt}=P_{in}-P_{out}\,} \). En la variable \( E \) (equivalentemente \( V_{dc}^2 \)) la planta es **lineal**: por eso el lazo de tensión se cierra sobre \( V_{dc}^2 \) y no sobre \( V_{dc} \) (ver [[control-tension-bus-dc]]). Este es el balance genérico de [[modelado-sistemas]] aplicado a la energía del bus.

## 2 — Por qué la CPL da resistencia incremental negativa y fija \( P_{crit} \)
**Paso 1 — la relación i–V de la carga.** Una carga de potencia constante mantiene \( P=V\,i \) fija. Despejando la corriente:

$$ i_{cpl}(V)=\frac{P}{V} $$

Es una hipérbola decreciente: a menor tensión, **más** corriente (al revés que una resistencia óhmica, donde \( i=V/R \) crece con \( V \)).

**Paso 2 — linealizar en torno al punto de operación.** La estabilidad de pequeña señal no la ve la curva entera, sino su **pendiente** en el punto \( V_0 \). Derivando \( i_{cpl}=P/V \):

$$ \left.\frac{di_{cpl}}{dV}\right|_{V_0}=-\frac{P}{V_0^2}<0 $$

La conductancia incremental es negativa. Su inverso es la **resistencia incremental**:

$$ \boxed{\;r_{cpl}=\left(\frac{di_{cpl}}{dV}\right)^{-1}=-\frac{V_0^2}{P}<0\;} $$

Físicamente: una resistencia disipa y amortigua; una resistencia **negativa** inyecta energía a la resonancia LC aguas arriba, la desamortigua. Por eso la CPL puede inestabilizar un bus que con carga resistiva sería estable (no pasividad; ver [[impedancia-salida-estabilidad]]).

**Paso 3 — meter esa pendiente en el modelo del filtro.** Con un filtro \( L_f,R_f \) que alimenta \( C_{dc} \) con la CPL, los estados son \( (i_{L},V_{dc}) \). La ecuación del condensador es \( C_{dc}\dot V_{dc}=i_L-i_{cpl}(V_{dc}) \); al linealizar, \( i_{cpl} \) aporta la derivada del Paso 2 con signo cambiado (sale del nodo), dejando un término **positivo** \( +P/(V_0^2 C_{dc}) \) en la diagonal de \( A \):

$$ A=\begin{bmatrix}-\dfrac{R_f}{L_f}&-\dfrac{1}{L_f}\\[0.9em]\dfrac{1}{C_{dc}}&\dfrac{P}{V_0^2\,C_{dc}}\end{bmatrix} $$

**Paso 4 — condición de estabilidad por la traza.** Para un sistema \( 2\times2 \), un par de polos complejos cruza al semiplano derecho cuando la **traza** de \( A \) pasa de negativa a positiva (la traza es la suma de las partes reales de los autovalores). Imponiendo \( \mathrm{tr}(A)<0 \):

$$ -\frac{R_f}{L_f}+\frac{P}{V_0^2\,C_{dc}}<0\;\;\Longrightarrow\;\; \frac{P}{V_0^2\,C_{dc}}<\frac{R_f}{L_f} $$

Despejando la potencia se obtiene la potencia crítica:

$$ \boxed{\;P_{crit}=\frac{V_0^2\,R_f\,C_{dc}}{L_f}\;} $$

Por encima de \( P_{crit} \) la traza es positiva y el bus oscila de forma creciente. La lectura de diseño es directa: más resistencia o más capacidad de bus suben \( P_{crit} \); menos inductancia de cable también. Como \( R_f \) (resistencia de cable) es incierta, se opera con margen amplio (factor 2 o más) respecto a \( P_{crit} \).

## Cuándo y por qué se usa
Para elegir C (rizado, autonomía, vida útil), modelar el lazo de tensión, y analizar la estabilidad del bus frente a cargas CPL en microrredes DC, data centers, vehículos eléctricos, naval y aeronáutica.

## Procedimiento de diseño (genérico)
1. Calcula el rizado dominante (2·omega en 1φ, conmutación en 3φ).
2. Dimensiona C por el criterio más exigente (rizado o hold-up).
3. Verifica la corriente eficaz por el condensador (vida útil/térmica), no solo la capacidad.
4. Modela vdc (o vdc²) para el lazo de tensión.
5. Modela la carga real como CPL (resistencia incremental −V²/P), calcula P_crit = V²·R·C/L y compáralo con el rango de carga.
6. Verifica la estabilidad por autovalores y por impedancia ([[criterio-middlebrook]]); si P_op se acerca a P_crit, sube Cdc o añade amortiguamiento.

## Ejemplo de aplicación real
Bus DC de Vdc0 = 700 V, 100 kW, rizado admisible < 1 %. Por rizado monofásico: C ≥ 100000/(2·314·0.01·700²) ≈ 3.27 mF. Por hold-up de 20 ms (Vmin = 600 V): C ≥ 2·100000·0.02/(700²−600²) ≈ 30.8 mF. El hold-up es casi 10× más exigente; se elige C = 33 mF con margen. La corriente RMS del condensador a 100 Hz (≈ 71 A) se verifica contra la hoja de datos (límite térmico del electrolítico).

## Ejemplo de código
```python
import numpy as np

# Dimensionado
P, Vdc0, Vmin, th = 100e3, 700.0, 600.0, 20e-3
C_holdup = 2*P*th/(Vdc0**2 - Vmin**2)          # autonomia
w = 2*np.pi*50; dV = 0.01*Vdc0
C_ripple = P/(2*w*dV*Vdc0)                      # rizado 1-fase (<1%)
C = max(C_holdup, C_ripple)

# CPL + estabilidad
i_cpl  = P / Vdc0                               # no lineal
g_incr = -P / Vdc0**2                           # conductancia incremental negativa
A = np.array([[-Rf/Lf, -1/Lf],
              [ 1/Cdc,  P/(Vdc0**2*Cdc)]])      # el termino CPL resta amortiguamiento
estable = np.all(np.linalg.eigvals(A).real < 0)
P_crit  = Vdc0**2 * Rf * Cdc / Lf
```

## Parámetros y valores típicos
- Rizado delta_vdc 1–2 % de Vdc. Hold-up 10–20 ms (fuentes con PFC). Electrolíticos limitados por corriente RMS y temperatura; film para alta fiabilidad.
- En un rack de IA, P de la CPL de decenas a cientos de kW a Vdc = 400–800 V; resistencia incremental −V²/P de fracciones de ohmio.
- Margen recomendado: operar con P_op bastante por debajo de P_crit (factor 2 o más), porque P_crit depende de parámetros inciertos (resistencia de cable, longitud, temperatura).

## Errores comunes
- Dimensionar solo por capacidad e ignorar la corriente eficaz (sobrecalienta el condensador).
- Olvidar el rizado de 2·omega en sistemas monofásicos/desequilibrados.
- Modelar la carga como resistencia constante (estable) cuando es CPL (puede inestabilizar); olvidar que el efecto desestabilizante crece con P y con tensión de bus baja.
- Asumir bus DC "rígido" cuando una CPL lo desestabiliza; confiar solo en el amortiguamiento resistivo natural del cable (pequeño); no dejar margen frente a P_crit.

## Uso en proyectos
- 03 - DataCenter-IA: los servidores/GPUs (vía sus POL) son la CPL del bus DC; su resistencia incremental negativa fija la potencia crítica de estabilidad. P_crit ≈ 128 kW para el filtro de distribución, validado por autovalores y por Middlebrook (134 kW). El condensador del rack se dimensiona por el pico de carga.

## Conceptos relacionados
- [[control-tension-bus-dc]] · [[criterio-middlebrook]] · [[impedancia-salida-estabilidad]] · [[potencia-instantanea-dq]] · [[robustez-parametrica]]

## Referencias
- Mohan, Undeland, Robbins, Power Electronics, Wiley.
- Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010.
- Emadi et al., Constant Power Loads and Negative Impedance Instability, IEEE TVT 2006.
- Riccobono, Santi, Review of Stability Criteria for DC Power Systems, IEEE TIA 2014.
