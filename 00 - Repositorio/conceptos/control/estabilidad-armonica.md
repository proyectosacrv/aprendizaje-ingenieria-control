---
titulo: Estabilidad y resonancia armónica de red
slug: estabilidad-armonica
categoria: control
tipo: fenomeno
nivel: avanzado
proyectos: []
objetivos: [entender oscilaciones de media-alta frecuencia por interacción convertidor-red]
tags: [estabilidad-armonica, resonancia, interaccion, pasividad, multi-convertidor, avanzado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-09
relacionados: [impedancia-salida-estabilidad, no-pasividad-resistencia-negativa, nyquist-generalizado, amortiguamiento-activo-lcl, filtro-lcl]
referencias:
  - "Wang, Blaabjerg, Harmonic Stability in Power-Electronic-Based Power Systems, IEEE TPEL 2014"
  - "Wang et al., Unified Impedance Model of Grid-Connected VSCs, IEEE TPEL 2018"
---

## Definición
Inestabilidad de **media-alta frecuencia** (decenas de Hz a kHz) que surge de la interacción entre
las impedancias de los convertidores y la red, manifestada como **oscilaciones armónicas**
sostenidas o crecientes, distinta de la estabilidad electromecánica clásica.

## Fundamento teórico
Cada convertidor presenta una impedancia/admitancia de salida \( Z_o(j\omega) \) con regiones donde
se comporta como **resistencia negativa** (no pasivo), típicamente alrededor de la frecuencia de
cruce del control, de la PLL o por el retardo digital ([[no-pasividad-resistencia-negativa]]). Si
la **fase** de \( Z_o \) sale de \( (-90^\circ,+90^\circ) \) en una frecuencia donde coincide con
una **resonancia de red** (paralelo \( L_gC \) de cables/filtros), el amortiguamiento neto se vuelve
negativo y aparece la oscilación.

Marco de análisis (criterio de pasividad / impedancia):
- **Pasividad:** si \( \mathrm{Re}\{Z_o(j\omega)\}\ge0\ \forall\omega \), el convertidor no puede
  desestabilizar ninguna red pasiva. Diseño "passivity-based".
- **Impedancia:** aplicar [[nyquist-generalizado|Nyquist]] al cociente \( Z_o/Z_g \).
- **Multi-convertidor:** \( N \) convertidores en paralelo → resonancias adicionales y reparto de
  corriente armónica; el modelo de impedancia unificada agrega sus admitancias.

Causas frecuentes de no-pasividad: retardo de cómputo+PWM (\( 1.5\,T_s \)), ancho de banda de la
PLL, *feedforward* de tensión de red, y amortiguamiento insuficiente del [[filtro-lcl]].

<div class="cfig"><img src="figuras/estabilidad-armonica-pasividad.png" alt="parte real de la impedancia de salida con region no pasiva"><div class="cap">La parte real de la impedancia de salida $Z_o$ del convertidor se vuelve negativa en una banda (sobre todo por el retardo digital): ahí el convertidor es no pasivo. Si esa región coincide con una resonancia de red, el amortiguamiento neto es negativo y aparece la oscilación armónica.</div></div>

## Cuándo y por qué se usa
En parques eólicos/PV con cables largos (alta capacidad), HVDC, y redes con muchos convertidores,
donde aparecen oscilaciones de cientos de Hz a kHz no explicables por la dinámica electromecánica.
Es la versión de alta frecuencia del análisis por impedancia.

## Procedimiento de diseño (genérico)
1. Modela \( Z_o(j\omega) \) del convertidor (incluyendo retardo digital) y \( Z_g \) de la red.
2. Localiza resonancias de red y regiones no pasivas del convertidor.
3. Aplica criterio de impedancia/pasividad; identifica la frecuencia crítica.
4. Mitiga: amortiguamiento activo ([[amortiguamiento-activo-lcl]]), [[filtro-notch]], reducir banda
   de PLL/control, compensar retardo ([[compensacion-retardo]]) o **impedancia virtual**.
5. Re-verifica con barrido del SCR y del número de convertidores.

## Ejemplo de código
```python
import numpy as np
# region no pasiva: Re{Zo} < 0  => candidato a inestabilidad armonica
def passivity_violation(Zo, freqs):
    bad = np.where(np.real(Zo) < 0)[0]
    return freqs[bad]
```

## Parámetros y valores típicos
Rango típico de inestabilidad armónica: 100 Hz–3 kHz. Objetivo: \( \mathrm{Re}\{Z_o\}\ge0 \) o
margen de fase de impedancia > 30° en las resonancias de red esperadas.

## Errores comunes
- Analizar un solo convertidor e ignorar la interacción **paralelo** de varios.
- Despreciar el retardo digital (principal fuente de no-pasividad a alta frecuencia).
- Confiar solo en amortiguamiento pasivo (pérdidas) cuando el problema es el control.

## Conceptos relacionados
- [[impedancia-salida-estabilidad]] · [[no-pasividad-resistencia-negativa]] · [[nyquist-generalizado]] · [[amortiguamiento-activo-lcl]] · [[compensacion-retardo]]

## Referencias
- Wang, Blaabjerg, *Harmonic Stability in Power-Electronic-Based Power Systems*, IEEE TPEL 2014.
- Wang et al., *Unified Impedance Model of Grid-Connected VSCs*, IEEE TPEL 2018.
