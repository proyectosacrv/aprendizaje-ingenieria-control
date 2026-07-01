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
fecha_actualizacion: 2026-07-01
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

<div class="cfig"><img src="figuras/polos-ceros-splano.png" alt="mapa de polos y ceros en el plano s"><div class="cap">Mapa polo-cero: todos los polos en el semiplano izquierdo ⇒ estable. La distancia al origen da la rapidez y el ángulo θ el amortiguamiento (ζ=cos θ). Los ceros (○) no afectan a la estabilidad.</div></div>

## 1 — Respuesta de un polo real: decaimiento e^{-at}

**Paso 1 — función de transferencia con un polo real.** Sea \( G(s)=K/(s+a) \) con \( a>0 \). La respuesta al impulso es la antitransformada de Laplace de \( G(s) \):

$$ \mathcal{L}^{-1}\!\left\{\frac{K}{s+a}\right\} = K\,e^{-at}\,\mathbf{1}(t) $$

**Paso 2 — interpretar el polo.** El polo está en \( s=-a \): parte real \( \sigma=-a<0 \) (semiplano izquierdo). La respuesta es un exponencial que **decae** con constante de tiempo \( \tau=1/a \): en \( t=\tau \) la amplitud cae al 37%; en \( t=5\tau \) es prácticamente cero. Cuanto más negativo el polo (mayor \( a \)), más rápido el decaimiento.

$$ \boxed{g(t)=K\,e^{-at},\quad \tau=\frac{1}{a}=-\frac{1}{\mathrm{Re}(p)}} $$

## 2 — Par complejo conjugado: oscilación amortiguada y cero en RHP

**Paso 1 — polos complejos conjugados.** Sea \( G(s)=\omega_n^2/\bigl[(s+\sigma)^2+\omega_d^2\bigr] \) con \( \sigma=\zeta\omega_n>0 \) y \( \omega_d=\omega_n\sqrt{1-\zeta^2} \). Los polos son \( s=-\sigma\pm j\omega_d \). La respuesta al impulso es:

$$ g(t)=\omega_n\,e^{-\sigma t}\frac{\sin(\omega_d t)}{\sqrt{1-\zeta^2}}\,\mathbf{1}(t) $$

**Paso 2 — leer la geometría del plano s.** La parte imaginaria \( \pm\omega_d \) da la frecuencia de oscilación; la parte real \( -\sigma \) da la tasa de decaimiento de la envolvente \( e^{-\sigma t} \). El módulo del polo es \( |p|=\omega_n \) y el ángulo respecto al eje real negativo cumple \( \cos\theta=\zeta \).

**Paso 3 — cero en el semiplano derecho (RHP).** Si \( G(s) \) tiene un cero en \( z=+b \) (\( b>0 \)), el factor \( (s-b) \) en el numerador produce un **signo negativo** en la respuesta para \( t\to0^+ \): la salida comienza moviéndose en dirección **contraria** a la entrada antes de girar. Esto es la **respuesta de fase no mínima**. Se verifica directamente: la antitransformada de \( (s-b)/[(s+a)(s+c)] \) tiene coeficiente de residuo negativo en la parte que corresponde al arranque.

$$ \boxed{z\in\mathrm{RHP}\;\Rightarrow\;\text{respuesta inversa inicial, margen de fase limitado}} $$

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
