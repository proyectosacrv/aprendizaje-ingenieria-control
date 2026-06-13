---
titulo: Realimentación (lazo abierto y cerrado)
slug: realimentacion
categoria: control
tipo: concepto
nivel: basico
proyectos: []
objetivos: [entender por que se realimenta y que aporta el lazo cerrado]
tags: [realimentacion, lazo-cerrado, feedback, error, basico]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-12
relacionados: [funcion-transferencia, controlador-pid, funciones-sensibilidad, margenes-estabilidad]
referencias:
  - "Aström, Murray, Feedback Systems, Princeton 2008"
---

## Definición
**Realimentar** es medir la salida, compararla con la referencia y actuar sobre la diferencia
(el **error**). El **lazo cerrado** usa esa medida; el **lazo abierto** actúa sin medir. La
realimentación es la idea central del control automático.

## Fundamento teórico
Con planta \( G(s) \) y controlador \( C(s) \) en lazo cerrado con realimentación unitaria, la
transferencia referencia → salida es:
$$ T(s) = \frac{C(s)G(s)}{1 + C(s)G(s)} $$
y el error responde según la **sensibilidad** \( S(s)=1/(1+CG) \). Lo que aporta el lazo cerrado:
- **Reduce el error** ante perturbaciones y errores de modelo (si la ganancia de lazo \( CG \) es
  grande, \( S \) es pequeña).
- **Modifica la dinámica** (mueve los polos) y puede estabilizar una planta inestable.
- **Riesgo**: una ganancia mal puesta puede **inestabilizar** (de ahí los márgenes).

El lazo abierto es simple pero no corrige perturbaciones ni errores de modelo.

<div class="cfig"><img src="figuras/realimentacion-lazo.png" alt="lazo de control realimentado"><div class="cap">Lazo cerrado: el error e=r−y entra al controlador C(s), que actúa sobre la planta G(s); la salida se mide y realimenta (signo −). Es lo que permite corregir perturbaciones y errores de modelo.</div></div>

## Cuándo y por qué se usa
Siempre que se quiera precisión y robustez ante incertidumbre: regular tensión, corriente,
velocidad. La práctica totalidad del control de convertidores es en lazo cerrado.

## Procedimiento (genérico)
1. Mide la salida y forma el error \( e = \text{ref} - \text{salida} \).
2. El controlador \( C(s) \) actúa sobre \( e \).
3. Diseña \( C \) para que \( T \) cumpla las especificaciones y el lazo sea estable (márgenes).
4. Verifica robustez (sensibilidad, márgenes).

## Ejemplo de aplicación real
**Problema:** Bus DC con carga CPL (resistencia diferencial negativa \( -R_{neg}=-200\,\Omega \)): el polo del modelo linealizado está en \( s=1/(C\cdot R_{neg})>0 \) (inestable). Diseñar la realimentación mínima para estabilizarlo.

Planta: \( G(s)=1/(Cs-1/R_{neg}) \) con \( C=10\,\text{mF} \). Con realimentación proporcional \( K \), el polo del lazo cerrado es \( p_{cl}=(1/R_{neg}-K)/C \). Para estabilizar: \( K>1/R_{neg}=0.005 \). Con \( K=0.01 \): \( p_{cl}=(−0.005−0.01)/0.01=−1.5\,\text{s}^{-1} \). Sistema estable. En la práctica se implementa como una **resistencia virtual activa**: el control inyecta potencia adicional proporcional a \( \Delta V_{dc} \), emulando una resistencia de amortiguamiento que no disipa calor.

## Ejemplo de código
```python
import control as ct
L = C * G                          # ganancia de lazo abierto
T = ct.feedback(L, 1)              # lazo cerrado con realimentacion unitaria
```

## Parámetros y valores típicos
Ganancia de lazo alta en baja frecuencia (buen seguimiento), baja en alta (robustez/ruido).

## Errores comunes
- Subir la ganancia para reducir el error sin mirar la estabilidad (margen de fase).
- Confiar en lazo abierto cuando hay perturbaciones o incertidumbre.

## Conceptos relacionados
- [[funcion-transferencia]] · [[controlador-pid]] · [[funciones-sensibilidad]] · [[margenes-estabilidad]]

## Referencias
- Aström, Murray, *Feedback Systems*, 2008.
