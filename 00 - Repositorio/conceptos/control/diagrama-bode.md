---
titulo: Diagrama de Bode
slug: diagrama-bode
categoria: control
tipo: concepto
nivel: basico
proyectos: []
objetivos: [leer la respuesta en frecuencia: magnitud y fase]
tags: [bode, frecuencia, magnitud, fase, decibelios, basico]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-11
relacionados: [funcion-transferencia, margenes-estabilidad, loop-shaping, respuesta-frecuencia-ss]
referencias:
  - "Ogata, Ingeniería de Control Moderna, Pearson"
---

## Definición
Par de gráficas que muestran cómo responde un sistema lineal a senoides de distinta frecuencia:
la **magnitud** (en dB) y la **fase** (en grados) de \( G(j\omega) \) frente a la frecuencia (en
escala logarítmica). Es la herramienta visual del diseño en frecuencia.

## Fundamento teórico
Se evalúa la función de transferencia en \( s=j\omega \):
$$ |G(j\omega)|_{dB}=20\log_{10}|G(j\omega)|, \qquad \angle G(j\omega) $$
Reglas de lectura (asíntotas):
- Cada **polo** añade \( -20 \) dB/década de pendiente y hasta \( -90° \) de fase.
- Cada **cero**, \( +20 \) dB/década y hasta \( +90° \).
- Un **integrador** \( 1/s \): \( -20 \) dB/dec y \( -90° \) constantes.
La **frecuencia de cruce de ganancia** (donde \( |G|=0 \) dB) marca el ancho de banda; en ella se
lee el **margen de fase**. La ventaja del logaritmo: multiplicar bloques = sumar sus Bode.

<div class="cfig"><img src="figuras/diagrama-bode-ejemplo.png" alt="diagrama de Bode de ejemplo"><div class="cap">Bode (magnitud y fase): cada polo dobla la pendiente en −20 dB/dec y añade hasta −90°. Las frecuencias de esquina (líneas) marcan dónde entra en juego cada polo.</div></div>

## Cuándo y por qué se usa
Para diseñar por loop-shaping, leer márgenes de estabilidad y entender el filtrado (qué
frecuencias pasan o se atenúan). Es el lenguaje del análisis de impedancia.

## Procedimiento (genérico)
1. Calcula \( G(j\omega) \) en un rango de frecuencias (escala log).
2. Dibuja magnitud (dB) y fase (deg).
3. Localiza el cruce de ganancia y lee el margen de fase; localiza el cruce de fase (−180°) y lee
   el margen de ganancia.
4. Da forma a la curva para cumplir las especificaciones.

## Ejemplo de aplicación real
**Problema:** Filtro LCL con \( L_1=2\,\text{mH} \), \( L_2=0.5\,\text{mH} \), \( C_f=15\,\mu\text{F} \). Identificar la resonancia en el Bode y determinar la zona válida para cruzar con el lazo de corriente.

Frecuencia de resonancia: \( f_{res}=\tfrac{1}{2\pi}\sqrt{(L_1+L_2)/(L_1 L_2 C_f)}\approx2.05\,\text{kHz} \). En el Bode, por debajo de \( f_{res} \) la pendiente es \( -40\,\text{dB/dec} \) (dos inductores en serie); en \( f_{res} \) la ganancia sube >40 dB y la fase cae \( -180° \). El lazo de corriente debe cruzar **por debajo de \( f_{res} \)**: con objetivo \( f_c\approx1\,\text{kHz} \) hay un margen de factor 2× frente a la resonancia. El amortiguamiento activo ([[amortiguamiento-activo-lcl]]) neutraliza el pico para permitir \( f_c \) más alto si se requiere.

## Ejemplo de código
```python
import control as ct, numpy as np
G = ct.tf([1], [1, 2, 1])
mag, phase, w = ct.frequency_response(G, np.logspace(-1, 2, 500))
```

## Parámetros y valores típicos
Pendiente \( -20 \) dB/dec en el cruce → buen margen de fase. Margen de fase objetivo 45–60°.

## Errores comunes
- Confundir frecuencia (rad/s) con Hz al leer la gráfica.
- Cruce con pendiente \( -40 \) dB/dec → margen de fase pobre (cerca de inestable).

## Conceptos relacionados
- [[funcion-transferencia]] · [[margenes-estabilidad]] · [[loop-shaping]] · [[respuesta-frecuencia-ss]]

## Referencias
- Ogata, *Ingeniería de Control Moderna*.
