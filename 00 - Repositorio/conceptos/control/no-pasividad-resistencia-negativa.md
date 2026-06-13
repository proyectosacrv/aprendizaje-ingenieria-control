---
titulo: No pasividad y resistencia negativa
slug: no-pasividad-resistencia-negativa
categoria: control
tipo: concepto
nivel: avanzado
proyectos: [02-GFL-Impedance, 03-DataCenter-IA]
objetivos: [explicar la inestabilidad por interaccion de impedancias]
tags: [pasividad, resistencia-negativa, impedancia, estabilidad, pll]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [impedancia-salida-estabilidad, pll-srf, interaccion-pll-red-debil, respuesta-frecuencia-ss]
referencias:
  - "Harnefors et al., Passivity-Based Stability Assessment of Grid-Connected VSCs, IEEE TIE 2016"
---

## Definición
Un puerto eléctrico es **pasivo** si no genera energía neta: en términos de impedancia,
\( \mathrm{Re}\{Z(j\omega)\}\ge 0 \) para todo \( \omega \). Cuando \( \mathrm{Re}\{Z\}<0 \) en
alguna banda, el puerto presenta **resistencia negativa** (es no pasivo) y puede entregar
energía a una resonancia → riesgo de inestabilidad al conectarse a la red.

## Fundamento teórico
Si tanto el inversor como la red son pasivos en todo el rango, su interconexión es estable
(criterio de pasividad, suficiente). La inestabilidad solo puede aparecer donde **al menos uno**
es no pasivo. En el grid-following, los lazos (sobre todo la **PLL**) introducen un desfase que
vuelve \( \mathrm{Re}\{Z\}<0 \) en su banda. Si la impedancia de la red (inductiva) cruza esa
región, se forma una resonancia mal amortiguada → oscilación.

Relación con [[impedancia-salida-estabilidad]]: la pasividad es una condición **suficiente** y
local en frecuencia; el Nyquist generalizado de \( Z_{red}Y_{inv} \) es el criterio exacto.

<div class="cfig"><img src="figuras/no-pasividad-resistencia-negativa-rez.png" alt="parte real de la impedancia negativa en la banda de la PLL"><div class="cap">La parte real de la impedancia de salida (eje q) del grid-following se vuelve negativa —no pasiva— en la banda de la PLL. Una PLL más rápida ensancha esa banda hacia frecuencias mayores; si la red inductiva resuena ahí, aparece la oscilación. La pasividad ($\mathrm{Re}\{Z\}\ge0$) es condición suficiente, no exacta.</div></div>

## Cuándo y por qué se usa
Para **explicar y prevenir** inestabilidades de convertidores: dar forma a la impedancia
(impedance shaping) de modo que sea pasiva en el rango de interés evita la inestabilidad sin
conocer la red exacta.

## Procedimiento de diseño (genérico)
1. Calcula/mide la impedancia de salida \( Z(j\omega) \) (ver [[respuesta-frecuencia-ss]]).
2. Localiza las bandas con \( \mathrm{Re}\{Z\}<0 \) (no pasivas).
3. Identifica la causa (PLL, retardo de cómputo, lazos lentos) y redúcela: PLL más lenta,
   compensación de retardo, resistencia/realimentación que aporte amortiguamiento.
4. Objetivo de diseño: \( \mathrm{Re}\{Z\}\ge 0 \) al menos donde la red pueda resonar.

## Ejemplo de código
```python
Z = impedance(A, B, C, D, freqs)          # matriz dq 2x2 por frecuencia
nopasiva = freqs[Z[:, 1, 1].real < 0]     # bandas no pasivas (eje q)
```

## Parámetros y valores típicos
La banda no pasiva del GFL coincide con el ancho de banda de la PLL. Una PLL rápida la ensancha
hacia frecuencias mayores.

## Errores comunes
- Confundir pasividad (suficiente, conservadora) con el criterio exacto de Nyquist: un sistema
  no pasivo **puede** ser estable con una red concreta; la no pasividad solo señala el riesgo.
- Mirar solo una componente: en dq es un sistema MIMO (la resistencia negativa apareció en
  \( \mathrm{Re}\{Z_{qq}\} \)).

## Uso en proyectos
- **02 - GFL-Impedance** (objetivo: explicar la inestabilidad): la impedancia de salida del GFL
  tiene \( \mathrm{Re}\{Z_{qq}\}<0 \) en la banda de la PLL; con PLL rápida se extiende a más
  frecuencia, lo que explica la inestabilidad en red débil.

## Conceptos relacionados
- [[impedancia-salida-estabilidad]] · [[pll-srf]] · [[interaccion-pll-red-debil]] · [[respuesta-frecuencia-ss]]

## Referencias
- Harnefors et al., *Passivity-Based Stability Assessment...*, IEEE TIE 2016.
