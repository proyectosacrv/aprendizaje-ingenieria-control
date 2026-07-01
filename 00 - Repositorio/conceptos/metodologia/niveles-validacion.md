---
titulo: Niveles de validación (fidelidad creciente)
slug: niveles-validacion
categoria: metodologia
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [validar el control subiendo niveles de realismo hasta el hardware]
tags: [validacion, fidelidad, conmutado, HIL, hardware, PLECS]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [validacion-cruzada, pruebas-validacion, convertidor-vsc, medicion-impedancia-inyeccion]
referencias:
  - "Lauss et al., Characteristics and Design of Power-HIL Simulations, IEEE TIE 2016"
---

## Definición
Escalera de modelos de **realismo creciente** por la que pasa un control antes de llegar al
hardware. Cada nivel añade efectos que el anterior ignoraba; subir solo cuando el nivel previo
está validado.

## Fundamento teórico
1. **Modelo lineal** (análisis): polos, impedancia, márgenes. Donde se **diseña**. Rápido pero
   solo pequeña señal alrededor de un punto.
2. **Modelo no lineal / promediado** (simulación temporal): gran señal, saturaciones, faltas,
   escalones grandes. Captura no linealidades pero no la conmutación. Ver [[convertidor-vsc|modelo promediado]].
3. **Modelo conmutado** (PLECS/Spice): IGBTs, PWM, rizado, retardo de cómputo, muestreo,
   cuantización. La "verdad" de simulación.
4. **HIL** (Hardware-in-the-Loop): el control **real** (DSP/FPGA) contra la planta simulada en
   tiempo real. Valida el código, los tiempos y la implementación digital sin arriesgar potencia.
5. **Prototipo / hardware**: la realidad (parásitos, EMI, térmica, tolerancias).

Cada salto añade riesgo de descubrir algo nuevo; el coste y el tiempo también crecen.

<div class="cfig"><img src="figuras/niveles-validacion-escalera.png" alt="escalera de niveles de validacion de fidelidad creciente"><div class="cap">Escalera de validación de realismo creciente: del modelo lineal (donde se diseña) al no lineal (gran señal, faltas), al conmutado (PWM, retardo, rizado), al HIL (control real contra planta en tiempo real) y al hardware. Cada salto añade física, coste y riesgo de descubrir algo nuevo; se sube solo cuando el nivel previo está validado.</div></div>

## 1 — Ejemplo cuantitativo: qué aparece en cada salto de nivel en el GFM
**Nivel 1 → Nivel 2 (lineal → no lineal/promediado).** En el lineal, el modo de potencia aparece a \( f_n=3.3\,\text{Hz} \) con \( \zeta=0.40 \). En el no lineal, ante un escalón de carga del 50 %, la corriente pico es 1.12 p.u. (inside del current limiting de 1.5 p.u. \( \checkmark \)) y el sobreimpulso de tensión es 7 %. Nuevo hallazgo: el feedforward de carga, estable en el lineal, provoca un pico transitorio del 12 % en el no lineal (no linealidad de la saturación del modulador) → se elimina.

**Nivel 2 → Nivel 3 (promediado → conmutado).** El promediado predice THD de corriente 0 % (no modela conmutación). El conmutado a \( f_{sw}=10\,\text{kHz} \) mide THD = 3.2 % (rizado en los armónicos \( f_{sw}\pm 2f_1 \)). El filtro LCL dimensionado cumple el límite de 5 % \( \checkmark \). Nuevo hallazgo: el retardo de cómputo de \( 1\,T_s=100\,\mu\text{s} \) reduce el margen de fase de corriente de 72° a 54° — aún cumple 45° \( \checkmark \) pero ajusta el margen.

**Nivel 3 → Nivel 4 (conmutado → HIL).** El firmware en DSP introduce una latencia adicional de \( 0.5\,T_s \) por el muestreo del ADC — el margen baja a 48°, límite. El HIL detecta esto sin riesgo; en hardware habría sido un rediseño costoso.

La escalera es económicamente eficiente: cada nivel nuevo detecta un problema diferente y el coste de arreglarlo crece con el nivel.

## Cuándo y por qué se usa
Para no llevar a hardware un diseño que falla por algo que un nivel intermedio habría detectado
barato. Estructura el "de la teoría a la realidad".

## Procedimiento (genérico)
1. Diseña y evalúa en el nivel lineal.
2. Sube a no lineal: prueba gran señal (faltas, current limiting).
3. Sube a conmutado: comprueba que el promediado seguía siendo válido (rizado, retardos).
4. HIL: porta el control al hardware de control contra planta en tiempo real.
5. Hardware: pruebas finales con todas las protecciones.
Vuelve atrás si un nivel revela un problema.

## Parámetros y valores típicos
Validez del promediado: \( f_{sw}/f_{control}\gtrsim 10 \). HIL: paso de tiempo del simulador
~µs. El retardo de cómputo (1–1.5 periodos de muestreo) suele aparecer en conmutado/HIL.

## Errores comunes
- Saltarse niveles ("del lineal al hardware"): caro y peligroso.
- No re-evaluar márgenes al añadir el retardo de cómputo (aparece en conmutado/HIL).

## Uso en proyectos
- **01/02**: niveles 1 (lineal: polos, impedancia) y 2 (no lineal: faltas, gran señal). El nivel
  3 (conmutado/PLECS) se valida con [[medicion-impedancia-inyeccion]]; HIL y hardware, pendientes.

## Conceptos relacionados
- [[validacion-cruzada]] · [[pruebas-validacion]] · [[convertidor-vsc|modelo promediado]] · [[medicion-impedancia-inyeccion]]

## Referencias
- Lauss et al., *Power-HIL Simulations*, IEEE TIE 2016.
