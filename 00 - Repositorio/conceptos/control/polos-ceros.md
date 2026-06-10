---
titulo: Polos y ceros
slug: polos-ceros
categoria: control
tipo: concepto
nivel: basico
proyectos: []
objetivos: [interpretar la dinamica y la estabilidad a partir de los polos y ceros]
tags: [polos, ceros, estabilidad, plano-s, basico]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [funcion-transferencia, sistema-primer-orden, respuesta-segundo-orden, estabilidad-bibo, analisis-modal]
referencias:
  - "Franklin, Powell, Feedback Control of Dynamic Systems"
---

## Definición
Los **polos** son las raíces del denominador de la función de transferencia (la ecuación
característica); los **ceros**, las del numerador. Los polos determinan la **forma** de la
respuesta y la **estabilidad**; los ceros, cómo se ponderan los modos.

## Fundamento teórico
Cada polo \( p=\sigma+j\omega \) aporta un modo \( e^{\sigma t}(\cos\omega t,\sin\omega t) \):
- \( \sigma<0 \) (semiplano **izquierdo**): el modo **decae** → contribuye a la estabilidad.
- \( \sigma>0 \) (semiplano derecho): el modo **crece** → inestable.
- \( \omega\neq 0 \): el modo **oscila** a esa frecuencia.
La distancia al origen marca la rapidez; el ángulo respecto al eje real, el amortiguamiento
\( \zeta=-\sigma/|p| \). Un sistema lineal es **estable** si y solo si **todos** sus polos están
en el semiplano izquierdo. Los ceros no afectan a la estabilidad, pero un **cero en el semiplano
derecho** (fase no mínima) produce respuesta inicial en sentido contrario y limita el control.

## Cuándo y por qué se usa
Es la lectura básica de cualquier diseño: mirar el mapa de polos dice de un vistazo si es estable,
cómo de rápido y cómo de amortiguado. Es la base del análisis modal.

## Procedimiento (genérico)
1. Obtén la función de transferencia o el modelo de estado.
2. Calcula los polos (raíces del denominador / autovalores de \( A \)).
3. Comprueba estabilidad (todos con parte real negativa).
4. Lee rapidez (\( |\sigma| \)) y amortiguamiento (\( \zeta \)) de los polos dominantes.

## Ejemplo de aplicación real
**Problema:** PI de corriente con \( K_p=5 \), cero en \( z=-10 \), planta \( G(s)=1/(s+10) \). Identificar la cancelación polo-cero y su efecto en la respuesta.

El PI tiene numerador \( K_p(s+10) \); la planta tiene polo en \( s=-10 \). Al multiplicar, el factor \( (s+10) \) se cancela: la ganancia de lazo abierto queda \( L(s)=5/s \) (integrador puro). El lazo cerrado es \( G_{cl}(s)=5/(s+5) \): polo único en \( s=-5 \), sin oscilación. Si el polo de la planta varía un 10 % (\( r'=11 \)), queda un polo residual en \( s=-11 \) no cancelado: como sigue en el SPD, el sistema permanece estable y el efecto sobre la respuesta transitoria es mínimo. La cancelación imperfecta es aceptable siempre que el residuo esté en el semiplano izquierdo.

## Ejemplo de código
```python
import numpy as np
polos = np.roots([1, 2, 5])             # raices del denominador s^2+2s+5
estable = np.all(polos.real < 0)
```

## Parámetros y valores típicos
Polos dominantes: los más cercanos al eje imaginario (los más lentos) dominan la respuesta.
\( \zeta>0.3 \) suele dar respuesta aceptable.

## Errores comunes
- Mirar solo la parte real e ignorar el amortiguamiento (un polo poco amortiguado oscila).
- Cancelar un polo inestable con un cero (cancelación no robusta, peligrosa).

## Conceptos relacionados
- [[funcion-transferencia]] · [[respuesta-segundo-orden]] · [[estabilidad-bibo]] · [[analisis-modal]]

## Referencias
- Franklin, Powell, *Feedback Control of Dynamic Systems*.
