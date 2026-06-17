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
fecha_actualizacion: 2026-06-10
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

## Conceptos relacionados
- [[convertidor-vsc]] · [[dinamica-bus-dc]] · [[control-tension-bus-dc]] · [[eolica-mppt]]

## Referencias
- Yazdani, Iravani, 2010.
- Teodorescu, Liserre, Rodríguez, 2011.
