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
fecha_actualizacion: 2026-07-01
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

## 1 — La norma \( H_\infty \): definición y por qué es el pico del Bode
**Paso 1 — norma de un sistema MIMO.** Para un sistema estable con matriz de transferencia \( \mathbf{H}(s) \), la norma \( H_\infty \) se define como la ganancia energética peor caso de entrada a salida:

$$ \|\mathbf{H}\|_\infty = \sup_{\omega\in\mathbb{R}}\,\bar\sigma\bigl(\mathbf{H}(j\omega)\bigr) $$

donde \( \bar\sigma \) es el valor singular máximo. En SISO reduce a \( \max_\omega|H(j\omega)| \), el pico de la respuesta en amplitud (pico del Bode). En MIMO es el pico de la ganancia máxima sobre todas las frecuencias **y** todas las direcciones de entrada.

**Paso 2 — interpretación energética.** Para señales en \( L_2 \) (energía finita), \( \|\mathbf{H}\|_\infty \) es la ganancia \( L_2\to L_2 \) inducida:

$$ \|\mathbf{H}\|_\infty = \sup_{u\neq0}\frac{\|y\|_{L_2}}{\|u\|_{L_2}} $$

Minimizar \( \|\mathbf{H}\|_\infty \) equivale a minimizar la amplificación máxima de energía: si \( \mathbf{H}=W_S S \), ello obliga a \( |S(j\omega)|<1/|W_S(j\omega)| \) en toda la banda, es decir el diseño queda acotado por la plantilla \( 1/W_S \).

**Paso 3 — el problema de síntesis.** El objetivo es encontrar \( C \) que minimice:

$$ \gamma^* = \min_C \left\|\begin{pmatrix}W_S S \\ W_u KS \\ W_T T\end{pmatrix}\right\|_\infty = \min_C \sup_\omega \bar\sigma\!\left[\begin{pmatrix}W_S S \\ W_u KS \\ W_T T\end{pmatrix}\!(j\omega)\right] $$

$$ \boxed{\text{El controlador } H_\infty \text{ garantiza: } |S(j\omega)|<1/|W_S(j\omega)|\ \forall\omega} $$

La solución se obtiene mediante ecuaciones de Riccati o LMIs; el orden del controlador es el de la planta aumentada (planta + pesos).

## 2 — Interpretación de los pesos y conexión con la robustez
**Paso 1 — peso \( W_S \).** \( W_S(s) \) es la plantilla inversa para la sensibilidad \( S=1/(1+L) \). Un peso de la forma \( W_S=(\omega_b/s+a)/(1+\omega_b M_s/s) \) (integrador a baja frecuencia) impone: cruce por debajo de \( 1/M_s \) a alta frecuencia (margen de pico) y atenuación creciente a baja frecuencia (rechazo de perturbación y seguimiento).

**Paso 2 — peso \( W_T \).** \( W_T \) conforma \( T=L/(1+L) \); un peso alto a alta frecuencia fuerza \( T \to 0 \) (caída de ganancia), lo que equivale a limitar el ancho de banda y garantizar robustez ante incertidumbre multiplicativa de alta frecuencia.

**Paso 3 — margen de robustez.** La condición de estabilidad robusta ante incertidumbre multiplicativa \( \Delta \) con \( \|\Delta\|_\infty\le 1/\|W_T^{-1}\|_\infty \) es exactamente \( \|W_T T\|_\infty<1 \), que el optimizador garantiza. Es la formalización en norma del límite empírico \( \|T\|_\infty < 1.5\text{–}2 \).

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
