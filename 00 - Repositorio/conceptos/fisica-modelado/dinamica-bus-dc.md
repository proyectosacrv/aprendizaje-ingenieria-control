---
titulo: Dinámica y dimensionado del bus DC
slug: dinamica-bus-dc
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: []
objetivos: [modelar y dimensionar el condensador del bus DC y su tensión]
tags: [bus-dc, condensador, balance-energia, rizado, hold-up, intermedio, modelado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-12
relacionados: [convertidor-vsc, control-tension-bus-dc, estabilidad-bus-dc-cpl, carga-potencia-constante-cpl, potencia-instantanea-dq]
referencias:
  - "Mohan, Undeland, Robbins, Power Electronics, Wiley"
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
---

## Definición
Modelo del **condensador del bus DC** como elemento que integra el desbalance de corriente/potencia
entre las dos etapas del convertidor, y reglas para **dimensionarlo** según rizado admisible y
autonomía (*hold-up*).

## Fundamento teórico
Por la corriente del condensador:
$$ C\frac{dv_{dc}}{dt}=i_{in}-i_{out} $$
o en energía \( E=\tfrac12 C v_{dc}^2 \):
$$ \frac{dE}{dt}=P_{in}-P_{out} $$
La planta hacia la tensión es un **integrador no lineal** (de ahí controlar \( v_{dc}^2 \); ver
[[control-tension-bus-dc]]).

**Fuentes de rizado:**
- Monofásico: la potencia instantánea pulsa a \( 2\omega \) → rizado de \( v_{dc} \) a 100/120 Hz
  $$ \Delta v_{dc}\approx\frac{P}{2\omega\,C\,V_{dc}} $$
- Trifásico equilibrado: la potencia es constante ([[potencia-instantanea-dq]]); el rizado dominante
  viene de la **conmutación** (6·\( f \) en rectificadores, \( f_{sw} \) en VSC).

**Dimensionado por autonomía (hold-up):** ante pérdida de entrada, mantener \( v_{dc}>V_{min} \)
durante \( t_h \):
$$ C\ge\frac{2 P\, t_h}{V_{dc0}^2-V_{min}^2} $$

**Estabilidad:** una carga de potencia constante presenta **impedancia incremental negativa**
\( \partial v/\partial i<0 \), que puede desestabilizar el bus (ver
[[carga-potencia-constante-cpl]], [[estabilidad-bus-dc-cpl]]).

<div class="cfig"><img src="figuras/dinamica-bus-dc-respuesta.png" alt="respuesta del bus DC a un escalon de carga"><div class="cap">El condensador integra el desbalance: sin control (rojo) Vdc cae linealmente ante un exceso de carga; el lazo de tensión (azul) ajusta la potencia de entrada y lo recupera.</div></div>

## Cuándo y por qué se usa
Para elegir \( C \) (rizado, autonomía, vida útil), modelar el lazo de tensión y analizar la
estabilidad del bus frente a cargas CPL en microrredes DC y data centers.

## Procedimiento de diseño (genérico)
1. Calcula el rizado dominante (\( 2\omega \) en 1φ, conmutación en 3φ).
2. Dimensiona \( C \) por el criterio más exigente (rizado **o** hold-up).
3. Verifica corriente eficaz por el condensador (vida útil/térmica), no solo capacidad.
4. Modela \( v_{dc} \) (o \( v_{dc}^2 \)) para el [[control-tension-bus-dc|lazo de tensión]].
5. Comprueba estabilidad con la carga real (CPL → criterio de impedancia).

## Ejemplo de aplicación real
**Problema:** Bus DC de \( V_{dc0}=700\,\text{V} \), potencia 100 kW, rizado admisible <1 %. Dimensionar \( C \) por rizado (sistema monofásico) y por hold-up de 20 ms (\( V_{min}=600\,\text{V} \)).

Por rizado monofásico: \( \Delta v_{dc}=P/(2\omega C V_{dc0})=100000/(2\times314\times C\times700) \). Para \( \Delta v_{dc}/V_{dc0}<0.01 \): \( C\ge100000/(2\times314\times0.01\times700^2)\approx3.27\,\text{mF} \). Por hold-up: \( C\ge2P\,t_h/(V_{dc0}^2-V_{min}^2)=2\times100000\times0.02/(700^2-600^2)=4000/130000\approx30.8\,\text{mF} \). El criterio de hold-up es casi 10× más exigente. Se elige \( C=33\,\text{mF} \) con margen. La corriente RMS del condensador a 100 Hz se verifica con la hoja de datos (límite térmico del electrolítico): \( I_{rms}=P/(2V_{dc0})\approx71\,\text{A} \) — seleccionar un componente con margen de corriente adecuado.

## Ejemplo de código
```python
P, Vdc0, Vmin, th = 100e3, 700.0, 600.0, 20e-3
C_holdup = 2*P*th/(Vdc0**2 - Vmin**2)          # autonomia
w = 2*3.1416*50; dV = 0.01*Vdc0
C_ripple = P/(2*w*dV*Vdc0)                      # rizado 1-fase (<1%)
C = max(C_holdup, C_ripple)
```

## Parámetros y valores típicos
Rizado \( \Delta v_{dc} \) 1–2 % de \( V_{dc} \). Hold-up 10–20 ms (fuentes con PFC). Electrolíticos
limitados por corriente RMS y temperatura; film para alta fiabilidad.

## Errores comunes
- Dimensionar solo por capacidad e ignorar la **corriente eficaz** (sobrecalienta el condensador).
- Olvidar el rizado de \( 2\omega \) en sistemas monofásicos/desequilibrados.
- Asumir bus DC "rígido" cuando una carga CPL lo desestabiliza.

## Conceptos relacionados
- [[convertidor-vsc]] · [[control-tension-bus-dc]] · [[estabilidad-bus-dc-cpl]] · [[carga-potencia-constante-cpl]] · [[potencia-instantanea-dq]]

## Referencias
- Mohan, Undeland, Robbins, *Power Electronics*.
- Yazdani, Iravani, 2010.
