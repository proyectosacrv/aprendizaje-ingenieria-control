---
titulo: Rectificador y AFE (active front-end)
slug: rectificador-afe
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: [03-DataCenter-IA]
objetivos: [entender la conversión AC-DC controlada que alimenta el bus DC]
tags: [rectificador, afe, ac-dc, bidireccional, factor-potencia, control-vectorial, basico]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-07-02
relacionados: [convertidor-vsc, control-tension-bus-dc, dinamica-bus-dc, microrred-hibrida-ac-dc, pll-srf]
referencias:
  - "Mohan, Undeland & Robbins, Power Electronics"
  - "Yazdani & Iravani, Voltage-Sourced Converters in Power Systems"
---

## Definición
Un **rectificador** convierte alterna en continua. El de **diodos** es pasivo y sencillo pero genera
armónicos y mal factor de potencia. El **AFE** (active front-end) es un VSC controlado que rectifica
de forma **activa**: regula la tensión del bus DC, trabaja con **factor de potencia unidad** y es
**bidireccional** (puede devolver energía a la red).

## Fundamento teórico
El AFE es topológicamente idéntico a un inversor VSC, pero su objetivo es controlar el lado DC:
mantiene constante la tensión del bus regulando la corriente AC que absorbe. Su control es en
**cascada**: un lazo externo de tensión \( V_{dc} \) fija la referencia de potencia/corriente, y un
lazo interno de corriente (en dq, con una PLL para sincronizar) la sigue. El balance de potencia liga
ambos lados:
$$ P_{ac} \approx P_{dc} = V_{dc}\,i_{dc} $$
Frente al rectificador de diodos, el AFE corrige armónicos (corriente senoidal), controla el FP y
permite el flujo de energía en los dos sentidos.

<div class="cfig"><img src="figuras/rectificador-afe-bloques.png" alt="diagrama de bloques del AFE"><div class="cap">El AFE es un VSC que rectifica de forma activa: con su PLL y sus lazos de corriente y tensión regula Vdc, trabaja a FP=1 y es bidireccional (puede devolver energía a la red).</div></div>

## 1 — Por qué el AFE da factor de potencia unidad

**Paso 1 — potencia en dq.** En el [[marco-dq]] alineado con la tensión de red por la [[pll-srf|PLL]], la tensión queda \( v_d=\hat V \) (pico de fase), \( v_q=0 \). La potencia activa y reactiva trifásicas son:

$$ P=\tfrac32\big(v_d i_d+v_q i_q\big),\qquad Q=\tfrac32\big(v_q i_d-v_d i_q\big) $$

**Paso 2 — anular el eje q.** Con \( v_q=0 \) ambas se simplifican:

$$ P=\tfrac32\,\hat V\,i_d,\qquad Q=-\tfrac32\,\hat V\,i_q $$

El control del AFE fija la referencia \( i_q^\*=0 \). Entonces \( Q=0 \): toda la potencia es activa.

**Paso 3 — factor de potencia.** Por definición \( \mathrm{FP}=\cos\varphi=P/\sqrt{P^2+Q^2} \). Con \( Q=0 \):

$$ \boxed{\;Q=0\;\Longrightarrow\;\mathrm{FP}=\frac{P}{\sqrt{P^2+0}}=1\;} $$

La corriente queda en fase con la tensión (senoidal y alineada), a diferencia del rectificador de diodos, que toma pulsos de corriente ricos en armónicos. El lazo de corriente solo tiene que mantener \( i_q^\* =0 \) para conservar FP=1, mientras \( i_d \) transporta toda la potencia.

## 2 — De dónde sale la referencia \( i_d^\* \) que regula \( V_{dc} \)

**Paso 1 — balance de potencia.** Despreciando pérdidas, la potencia que el AFE toma de la red iguala a la que entrega al bus DC:

$$ P_{ac}=P_{dc}=V_{dc}\,i_{dc} $$

**Paso 2 — sustituir la potencia AC.** Del desarrollo anterior \( P_{ac}=\tfrac32\hat V\,i_d \). Igualando:

$$ \tfrac32\,\hat V\,i_d = V_{dc}\,i_{dc} $$

**Paso 3 — despejar la corriente de referencia.** El lazo externo de tensión calcula la potencia \( P^\* \) necesaria para llevar \( V_{dc} \) a su consigna (compensando la corriente de carga del bus); de ahí la referencia del lazo interno:

$$ \boxed{\;i_d^\*=\frac{2}{3}\,\frac{P^\*}{\hat V}=\frac{2}{3}\,\frac{V_{dc}\,i_{dc}}{\hat V}\;}\qquad i_q^\*=0 $$

Así un aumento de la carga DC (sube \( i_{dc} \)) baja \( V_{dc} \), el lazo de tensión pide más \( i_d^\* \) y el AFE absorbe más potencia activa de la red, restaurando \( V_{dc} \) — siempre a FP=1. El ancho de banda del lazo de tensión se mantiene bajo (decenas de Hz) para no acoplar el rizado de \( 100/120\,\text{Hz} \) del bus.

## 3 — El modelo promediado del AFE

El AFE y el inversor VSC comparten la misma topología de puente; la diferencia es el sentido del flujo de energía y el objetivo del control. El modelo promediado (ver [[modelo-promediado]]) elimina la conmutación y conserva la dinámica relevante:

**Paso 1 — lado AC (filtro L).** Aplicando KVL en el inductor de filtro \( L \) (fase a, referenciado al neutro virtual):

$$ L\,\frac{di_a}{dt} = v_{a,\text{red}} - v_{a,\text{AFE}} $$

donde \( v_{a,\text{AFE}}=m_a\,V_{dc}/2 \) con \( m_a \in[-1,1] \) el ciclo de trabajo promediado.

**Paso 2 — transformar a dq.** Después de la transformada de Park ([[marco-dq]]) aparecen los términos de desacoplo:

$$ L\,\frac{di_d}{dt} = v_d - v_d^* - \omega_0 L\,i_q $$
$$ L\,\frac{di_q}{dt} = v_q - v_q^* + \omega_0 L\,i_d $$

Los términos \( \omega_0 L\,i_q \) y \( \omega_0 L\,i_d \) son los acoplos entre ejes; el [[desacoplo-dq]] los cancela con feedforward.

**Paso 3 — lado DC.** El condensador de bus integra el desbalance de potencia:

$$ C\,\frac{dV_{dc}}{dt} = i_{in,dc} - i_{carga} = \frac{3}{2}\,\frac{v_d i_d}{V_{dc}} - i_{carga} $$

Este es el mismo modelo que [[control-tension-bus-dc]] y [[dinamica-bus-dc]]. La planta del lazo de tensión es un integrador \( 1/(C\,s) \) (linealizado cerca de \( V_{dc,0} \)), lo que justifica usar un PI con ancho de banda moderado (10–50 Hz).

## 4 — El control vectorial del AFE: lazo de tensión DC y lazo de corriente dq

El control en **cascada** tiene dos niveles con anchos de banda muy distintos para garantizar separación de escalas:

**Lazo interno de corriente** (banda: 200–1000 Hz):

$$ v_d^*(s) = \underbrace{\left(K_{p,i}+\frac{K_{i,i}}{s}\right)}_{\text{PI}} (i_d^*-i_d) + v_d - \omega_0 L\,i_q \qquad \text{(desacoplo)} $$

El mismo esquema para el eje \( q \). Con desacoplo correcto la planta de cada eje es \( L\,s + R \), y el PI puede diseñarse por asignación de polo dominante: \( K_{p,i}=\alpha_c L \), \( K_{i,i}=\alpha_c R \), con \( \alpha_c \) el ancho de banda deseado.

**Lazo externo de tensión DC** (banda: 10–30 Hz, típico \( <\frac{1}{3}\) del lazo de corriente):

$$ i_d^*(s) = \left(K_{p,v}+\frac{K_{i,v}}{s}\right)(V_{dc}^*-V_{dc}) $$

La salida del PI de tensión es directamente \( i_d^\* \): la potencia activa que el AFE debe absorber de la red. El lazo de tensión es lento para atenuar el rizado de \( 2\omega_0 \) (100 Hz en Europa) que aparece porque la potencia AC instantánea oscila al doble de la frecuencia de red.

<div class="cfig"><img src="figuras/rectificador-afe-analisis.png" alt="control y respuesta del AFE 500 kW"><div class="cap">Los cuatro paneles muestran el lazo de control completo (cascada Vdc → id*), la comparativa de formas de onda (rectificador de diodos THD≈80% vs AFE THD≈3%), el diagrama de Bode del lazo de tensión DC, y la respuesta id*(t) y Vdc(t) ante un escalón de carga de 300 A a 625 A en el bus DC.</div></div>

## 5 — El AFE vs rectificador de diodos: THD y factor de potencia

La diferencia en calidad de red es drástica entre ambas tecnologías:

| Parámetro | Rectificador diodos 6-pulsos | AFE |
|---|---|---|
| THD corriente | \(\approx 80\,\%\) | \(<5\,\%\) (con filtro LCL) |
| Factor de potencia | \(\approx 0{,}7\text{–}0{,}8\) | \(\approx 1{,}0\) |
| Armónico dominante | 5º (orden \( 6k\pm1 \)) | Bandas de \( f_{sw} \) (fáciles de filtrar) |
| Bidireccionalidad | No | Sí (regenerativo) |
| Soporte de reactiva | No | Sí (\( i_q^*\ne0 \)) |
| Coste relativo | Bajo | Alto (VSC + control) |

**Por qué el rectificador de diodos tiene THD≈80 %.** Un puente trifásico de 6 diodos conduce solo cuando la tensión de fase es la máxima (o mínima). La corriente en cada fase es una onda cuasi-cuadrada de ancho \( 120°\) que contiene los armónicos de orden \( 6k\pm1 \): 5º, 7º, 11º, 13º… La amplitud del \( n\)-ésimo decae como \( 1/n \), pero la suma en cuadratura de todos los órdenes eleva el THD al 80–100 %.

**Por qué el AFE tiene THD≈3–5 %.** El lazo de corriente dq sigue la referencia senoidal con un error pequeño; los únicos residuos son las bandas de conmutación en \( f_{sw} \) y sus múltiplos, que el filtro LCL atenúa 40 dB/década. Los armónicos de bajo orden (5º, 7º) que pudieran quedar por tiempo muerto o desbalance se compensan con controladores resonantes o con compensación de tiempo muerto.

**El factor de potencia del rectificador de diodos.** Aunque la corriente fundamental está casi en fase con la tensión, la distorsión degrada el FP:

$$ \mathrm{FP} = \cos\varphi_1 \cdot \frac{1}{\sqrt{1+\mathrm{THD}^2}} \approx 0{,}95 \cdot \frac{1}{\sqrt{1+0{,}8^2}} \approx 0{,}75 $$

## 6 — Diseño iterativo: AFE 500 kW para bus DC de datacenter

**Datos de partida:**
- Potencia: \( P_n = 500\,\text{kW} \)
- Tensión de bus DC: \( V_{dc} = 800\,\text{V} \)
- Red AC: \( V_{LL} = 400\,\text{V} \), \( f_1 = 50\,\text{Hz} \)
- Frecuencia de conmutación: \( f_{sw} = 10\,\text{kHz} \)

**Paso 1 — corriente de red nominal:**

$$ I_n = \frac{P_n}{\sqrt{3}\,V_{LL}} = \frac{500\times10^3}{\sqrt{3}\times400} = 721\,\text{A} $$

**Paso 2 — tensión de bus DC mínima.** Para modular linealmente, \( V_{dc} \) debe superar el pico de línea:

$$ V_{dc,\min} = \sqrt{2}\,V_{LL} = \sqrt{2}\times400 = 566\,\text{V} $$
Se elige \( 800\,\text{V} \) con holgura (\( m_a = 566/800 = 0{,}71 \) — zona lineal).

**Paso 3 — inductancia del filtro (rizado de corriente ≤ 15 % de \( I_n \)):**

$$ L_1 = \frac{V_{dc}}{8\,f_{sw}\,\Delta i_{max}} = \frac{800}{8\times10\,000\times0{,}15\times721\sqrt{2}} \approx 0{,}52\,\text{mH} $$

**Paso 4 — condensador del bus DC (rizado de tensión ≤ 1 %):**

$$ C = \frac{P_n}{2\,\omega_0\,V_{dc}^2\,\Delta V_{rel}} = \frac{500\times10^3}{2\times314\times800^2\times0{,}01} \approx 125\,\text{mF} $$

En la práctica se usan condensadores de \( 50\text{–}100\,\text{mF} \) con limitación del ancho de banda del lazo de tensión para no excitar el rizado.

**Paso 5 — lazo de corriente.** Ancho de banda \( \alpha_c = 2\pi\times500\,\text{rad/s} \) (1/20 de \( f_{sw} \)):

$$ K_{p,i} = \alpha_c\,L_1 = 3\,140 \times 0{,}52\times10^{-3} \approx 1{,}63\,\text{V/A}, \quad K_{i,i} = \alpha_c\,R \approx 10\,\text{V/(A·s)} $$

**Paso 6 — lazo de tensión DC.** Ancho de banda \( \alpha_v = 2\pi\times20\,\text{rad/s} \) (1/25 de \( \alpha_c \)):

$$ K_{p,v} = \alpha_v\,C\,V_{dc,0} / (3\hat V/2) \approx 2\,\text{A/V}, \quad K_{i,v} \approx 50\,\text{A/(V·s)} $$

**Verificación:** el rizado del lazo de tensión a 100 Hz queda atenuado \( >20\,\text{dB} \) por debajo del ancho de banda. El THD de corriente con el filtro LCL dimensionado queda \( <3\,\% \), dentro del límite IEEE 519.

## Cuándo y por qué se usa
Para alimentar un bus DC de forma controlada y limpia: data centers, accionamientos, carga de
baterías, HVDC. En la microrred del proyecto 03 es el **puente** entre el lado AC (BESS
grid-forming) y el bus DC que abastece a los servidores.

## Errores comunes
- Usar rectificador de diodos donde se necesita FP unidad o bidireccionalidad.
- Ancho de banda del lazo de tensión demasiado alto (acopla rizado de 100/120 Hz).
- Olvidar que el AFE necesita PLL y sincronización robusta en red débil.
- Diseñar \( C \) sin considerar el ancho de banda: condensador pequeño + lazo rápido amplifica el rizado de 100 Hz en la corriente de red.
- Ignorar la saturación de \( i_d^\* \): si la carga supera la capacidad del AFE, \( V_{dc} \) cae sin recuperación hasta que el PI se satura completamente (windup).

## Ejemplo de código
```python
# Balance de potencia AC<->DC (ideal) que acopla los dos dominios
Vbus, P_carga = 800.0, 500e3
id_star = (2/3) * P_carga / (Vbus * np.sqrt(2) / np.sqrt(3))   # [A rms ref. pico]
```

## Parámetros y valores típicos
Ancho de banda del lazo de tensión DC: 10–30 Hz; lazo de corriente: 200–1000 Hz. Tensión de bus
por encima del pico de línea. THD objetivo \( <5\,\% \) (IEEE 519). Rizado de \( V_{dc} \): \( <1\,\% \).

## Uso en proyectos
- **03 - DataCenter-IA:** el AFE traslada al BESS (lado AC) la potencia que demanda el bus DC
  (\( P_{afe}=V_{bus}\,i_L \)); así un pico de carga en DC se siente como caída de frecuencia en AC.

## Conceptos relacionados
- [[convertidor-vsc]] · [[control-tension-bus-dc]] · [[dinamica-bus-dc]] · [[microrred-hibrida-ac-dc]] · [[pll-srf]] · [[filtro-lcl]] · [[armonicos-thd-convertidores]]

## Referencias
- Mohan, Undeland & Robbins, *Power Electronics*, Wiley.
- Yazdani & Iravani, *Voltage-Sourced Converters in Power Systems*.
