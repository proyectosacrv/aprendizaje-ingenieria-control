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
fecha_actualizacion: 2026-06-30
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

## 1 — De dónde salen las asíntotas de un polo simple (±20 dB/dec, ±90°)
**Paso 1 — evaluar el polo en \( j\omega \).** Toma un polo simple \( G(s)=\dfrac{1}{1+s/\omega_p} \). En \( s=j\omega \):

$$ G(j\omega)=\frac{1}{1+j\,\omega/\omega_p} $$

**Paso 2 — módulo y fase.** El módulo de un cociente es el cociente de módulos; la fase, la diferencia de fases. El numerador \( 1 \) tiene módulo \( 1 \) y fase \( 0 \); el denominador \( 1+j\,\omega/\omega_p \) tiene módulo \( \sqrt{1+(\omega/\omega_p)^2} \) y fase \( \arctan(\omega/\omega_p) \):

$$ |G(j\omega)|=\frac{1}{\sqrt{1+(\omega/\omega_p)^2}},\qquad \angle G(j\omega)=-\arctan\!\frac{\omega}{\omega_p} $$

**Paso 3 — pasar a decibelios.** Por definición \( |G|_{dB}=20\log_{10}|G| \). Como \( \log\) de un cociente resta y \( \log\sqrt{x}=\tfrac12\log x \):

$$ |G(j\omega)|_{dB}=-20\log_{10}\sqrt{1+(\omega/\omega_p)^2}=-10\log_{10}\!\Big(1+(\omega/\omega_p)^2\Big) $$

**Paso 4 — asíntota de baja frecuencia.** Si \( \omega\ll\omega_p \), \( (\omega/\omega_p)^2\ll1 \), el argumento del log tiende a \( 1 \) y \( |G|_{dB}\to0 \). La asíntota es **plana a 0 dB**. La fase tiende a \( -\arctan 0=0^\circ \).

**Paso 5 — asíntota de alta frecuencia (la pendiente).** Si \( \omega\gg\omega_p \), \( 1+(\omega/\omega_p)^2\approx(\omega/\omega_p)^2 \), luego:

$$ |G(j\omega)|_{dB}\approx-20\log_{10}\frac{\omega}{\omega_p} $$

Cada vez que \( \omega \) se multiplica por 10 (una década), \( \log_{10}(\omega/\omega_p) \) crece en 1 y la magnitud cae \( 20 \) dB: **pendiente \( -20 \) dB/dec**. La fase tiende a \( -\arctan(\infty)=-90^\circ \). Verificado: en \( \omega=10\,\omega_p \) la fórmula exacta da \( -20.04 \) dB.

$$ \boxed{\;\text{polo simple: } 0\text{ dB} \to -20\text{ dB/dec},\quad \text{fase } 0^\circ\to-90^\circ\;} $$

**Paso 6 — la frecuencia de esquina.** En \( \omega=\omega_p \): \( 1+1=2 \), \( |G|_{dB}=-10\log_{10}2\approx-3.01 \) dB (el conocido "punto de \( -3 \) dB") y \( \angle G=-\arctan1=-45^\circ \) (verificado). Un **cero** simple \( 1+s/\omega_z \) es idéntico con signo opuesto: \( +20 \) dB/dec y \( +90^\circ \). Un **integrador** \( 1/s \) es el caso límite \( \omega_p\to0 \): pendiente \( -20 \) dB/dec y fase \( -90^\circ \) constantes en todo el rango.

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

Frecuencia de resonancia: \( f_{res}=\tfrac{1}{2\pi}\sqrt{(L_1+L_2)/(L_1 L_2 C_f)}\approx2.05\,\text{kHz} \). En el Bode, por debajo de \( f_{res} \) la pendiente es \( -40\,\text{dB/dec} \) (dos inductores en serie); en \( f_{res} \) la ganancia sube >40 dB y la fase cae \( -180° \). El lazo de corriente debe cruzar **por debajo de \( f_{res} \)**: con objetivo \( f_c\approx1\,\text{kHz} \) hay un margen de factor 2× frente a la resonancia. El amortiguamiento activo ([[filtro-lcl|amortiguamiento activo]]) neutraliza el pico para permitir \( f_c \) más alto si se requiere.

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
