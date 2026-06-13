---
titulo: Control robusto (H∞, μ-síntesis)
slug: control-robusto-hinf
categoria: metodologia
tipo: metodo
nivel: avanzado
proyectos: []
objetivos: [garantizar estabilidad y desempeno ante incertidumbre]
tags: [robusto, H-infinito, mu-sintesis, incertidumbre, panorama]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [metodos-sintesis-control, funciones-sensibilidad, robustez-parametrica, margenes-estabilidad]
referencias:
  - "Skogestad, Postlethwaite, Multivariable Feedback Control, Wiley 2005 (cap. 8-9)"
---

## Definición
Métodos que diseñan el controlador para el **peor caso** de incertidumbre del modelo, ofreciendo
**garantías** de estabilidad y desempeño. \(H_\infty\) minimiza la norma infinito (el pico en
frecuencia) de funciones de transferencia ponderadas; la \(\mu\)-síntesis trata incertidumbre
estructurada.

## Fundamento teórico
Se formula con **pesos** \( W_S, W_T, W_u \) que dan forma a las funciones de [[funciones-sensibilidad]]:
$$ \min_C \left\| \begin{matrix} W_S S \\ W_u KS \\ W_T T \end{matrix} \right\|_\infty $$
El resultado garantiza que \( S, T \) quedan bajo las plantillas \( 1/W \). La incertidumbre del
modelo se modela como bloques \( \Delta \) acotados; el teorema de la ganancia pequeña / \( \mu \)
da la condición de robustez.

<div class="cfig"><img src="figuras/control-robusto-hinf-sensibilidad.png" alt="conformado de las funciones de sensibilidad S y T con sus plantillas"><div class="cap">El diseño $H_\infty$ conforma las funciones de sensibilidad: $|S|$ debe quedar baja a baja frecuencia (buen seguimiento/rechazo) y $|T|$ baja a alta frecuencia (robustez al ruido y a la incertidumbre). Los pesos $W_S,W_T$ fijan esas plantillas $1/W$ y el optimizador minimiza el pico de las transferencias ponderadas.</div></div>

## Cuándo y por qué se usa
Cuando la planta varía mucho (red de fortaleza desconocida, parámetros inciertos) y se necesitan
**garantías** en vez de comprobaciones puntuales. Conecta con el análisis de impedancia: se puede
exigir pasividad/robustez en bandas mediante los pesos.

## Procedimiento (genérico)
1. Modela la incertidumbre (multiplicativa, paramétrica) como \( \Delta \) acotado.
2. Elige pesos \( W_S, W_T, W_u \) que codifiquen las especificaciones.
3. Resuelve el problema \(H_\infty\) (solver dedicado) → controlador.
4. Verifica robustez (valor singular estructurado \( \mu \)) y reduce el orden del controlador si hace falta.

## Errores comunes
- Pesos mal elegidos → controlador conservador o de orden altísimo.
- Olvidar reducir el orden: \(H_\infty\) da controladores del orden de la planta + pesos.

## Uso en proyectos
- Candidato a proyecto propio (p.ej. control robusto de un GFL/GFM ante SCR incierto). Ficha de
  panorama por ahora.

## Conceptos relacionados
- [[metodos-sintesis-control]] · [[funciones-sensibilidad]] · [[robustez-parametrica]] · [[margenes-estabilidad]]

## Referencias
- Skogestad, Postlethwaite, *Multivariable Feedback Control*, cap. 8-9.
