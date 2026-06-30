---
titulo: Rectificador y AFE (active front-end)
slug: rectificador-afe
categoria: fisica-modelado
tipo: concepto
nivel: basico
proyectos: [03-DataCenter-IA]
objetivos: [entender la conversión AC-DC controlada que alimenta el bus DC]
tags: [rectificador, afe, ac-dc, bidireccional, factor-potencia, basico]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-06-30
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

## Cuándo y por qué se usa
Para alimentar un bus DC de forma controlada y limpia: data centers, accionamientos, carga de
baterías, HVDC. En la microrred del proyecto 03 es el **puente** entre el lado AC (BESS
grid-forming) y el bus DC que abastece a los servidores.

## Procedimiento de diseño (genérico)
1. Dimensiona el VSC y el filtro AC (como un inversor).
2. Diseña la PLL para sincronizar con la red AC.
3. Lazo interno de corriente dq; lazo externo de tensión \( V_{dc} \) que fija la referencia.
4. Verifica el balance de potencia y el rizado del bus DC.

## Ejemplo de código
```python
# Balance de potencia AC<->DC (ideal) que acopla los dos dominios
Vbus, iL = 800.0, 150e3/800.0          # bus DC y corriente de carga
P_afe = Vbus*iL                         # potencia que el AFE toma del lado AC
```

## Parámetros y valores típicos
Ancho de banda del lazo de tensión DC: bajo (decenas de Hz) para no acoplar el rizado; lazo de
corriente: cientos de Hz a kHz. Tensión de bus por encima del pico de línea para modular linealmente.

## Errores comunes
- Usar rectificador de diodos donde se necesita FP unidad o bidireccionalidad.
- Ancho de banda del lazo de tensión demasiado alto (acopla rizado de 100/120 Hz).
- Olvidar que el AFE necesita PLL y sincronización robusta en red débil.

## Uso en proyectos
- **03 - DataCenter-IA:** el AFE traslada al BESS (lado AC) la potencia que demanda el bus DC
  (\( P_{afe}=V_{bus}\,i_L \)); así un pico de carga en DC se siente como caída de frecuencia en AC.

## Conceptos relacionados
- [[convertidor-vsc]] · [[control-tension-bus-dc]] · [[dinamica-bus-dc]] · [[microrred-hibrida-ac-dc]] · [[pll-srf]]

## Referencias
- Yazdani & Iravani, *Voltage-Sourced Converters in Power Systems*.
