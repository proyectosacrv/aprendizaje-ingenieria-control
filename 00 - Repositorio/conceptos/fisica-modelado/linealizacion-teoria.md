---
titulo: Teoría de linealización
slug: linealizacion-teoria
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [aproximar un sistema no lineal por uno lineal para analizar y disenar]
tags: [linealizacion, jacobiano, equilibrio, pequena-senal, validez]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-30
relacionados: [linealizacion-numerica, equilibrio-fsolve, representacion-espacio-estados, modelado-sistemas]
referencias:
  - "Khalil, Nonlinear Systems, Prentice Hall 2002 (cap. 4)"
---

## Definición
Aproximar un sistema no lineal \( \dot{\mathbf{x}}=\mathbf{f}(\mathbf{x},\mathbf{u}) \) por un
modelo **lineal** válido en un entorno de un punto de operación (equilibrio). Es lo que permite
aplicar toda la teoría de control lineal a sistemas que en realidad no lo son.

## Fundamento teórico
En un equilibrio \( (\mathbf{x}_e,\mathbf{u}_e) \) con \( \mathbf{f}(\mathbf{x}_e,\mathbf{u}_e)=0 \),
se desarrolla \( \mathbf{f} \) en serie de Taylor y se conserva el primer orden. Con las
desviaciones \( \Delta\mathbf{x}=\mathbf{x}-\mathbf{x}_e \):
$$ \Delta\dot{\mathbf{x}} = A\,\Delta\mathbf{x} + B\,\Delta\mathbf{u}, \qquad
   A=\left.\frac{\partial \mathbf{f}}{\partial \mathbf{x}}\right|_e, \quad
   B=\left.\frac{\partial \mathbf{f}}{\partial \mathbf{u}}\right|_e $$
\( A \) y \( B \) son los **Jacobianos** evaluados en el equilibrio.

**Validez** (teorema de Hartman–Grobman): si el equilibrio es **hiperbólico** (ningún autovalor
de \( A \) sobre el eje imaginario), el comportamiento cualitativo del no lineal cerca del
equilibrio coincide con el del linealizado. Es un resultado **local** (pequeña señal): vale
mientras las desviaciones sean pequeñas. Falla con no linealidades fuertes (saturación,
zona muerta) o en equilibrios no hiperbólicos.

<div class="cfig"><img src="figuras/linealizacion-teoria-validez.png" alt="respuesta no lineal vs linealizada en pequena y gran senal"><div class="cap">Un péndulo no lineal frente a su modelo linealizado: en pequeña señal ($\theta_0$ pequeño) ambas respuestas coinciden y el análisis lineal es válido; en gran señal divergen, porque la aproximación de primer orden solo vale en un entorno del equilibrio. El teorema de Hartman–Grobman garantiza la equivalencia local si el equilibrio es hiperbólico.</div></div>

## 1 — De dónde sale \( \Delta\dot{\mathbf{x}}=A\,\Delta\mathbf{x}+B\,\Delta\mathbf{u} \): Taylor de primer orden
La forma linealizada no se postula: es el primer término no nulo del desarrollo de Taylor de \( \mathbf{f} \) alrededor del equilibrio. Lo derivamos primero en escalar (una variable) y luego en vectorial, donde aparece el Jacobiano.

**Paso 1 — Taylor escalar.** Para una función suave \( f(x,u) \) de una entrada y un estado, el desarrollo alrededor de \( (x_e,u_e) \) hasta primer orden es:

$$ f(x,u)\approx f(x_e,u_e)+\left.\frac{\partial f}{\partial x}\right|_e (x-x_e)+\left.\frac{\partial f}{\partial u}\right|_e (u-u_e)+\;\underbrace{O(\|\cdot\|^2)}_{\text{se desprecia}} $$

**Paso 2 — usar la condición de equilibrio.** Por definición de equilibrio, \( f(x_e,u_e)=0 \). El término constante se **anula**: ese es el motivo de linealizar justo en el equilibrio (si se hiciera en otro punto quedaría un residuo \( \neq 0 \) y \( A \) perdería sentido). Quedan solo los términos lineales en las desviaciones \( \Delta x=x-x_e \), \( \Delta u=u-u_e \).

**Paso 3 — la derivada de la desviación es la de \( x \).** Como \( x_e \) es constante, \( \dot{\Delta x}=\dot x-\dot x_e=\dot x=f(x,u) \). Sustituyendo el Paso 1 ya sin término constante:

$$ \dot{\Delta x}\approx \left.\frac{\partial f}{\partial x}\right|_e \Delta x+\left.\frac{\partial f}{\partial u}\right|_e \Delta u $$

es decir \( \dot{\Delta x}=a\,\Delta x+b\,\Delta u \) con \( a,b \) escalares: ya es un sistema lineal.

**Paso 4 — caso vectorial: el Jacobiano.** Con \( \mathbf{x}\in\mathbb{R}^n \), \( \mathbf{u}\in\mathbb{R}^m \) y \( \mathbf{f} \) vectorial, la derivada parcial respecto a un vector es la **matriz Jacobiana**: la fila \( i \) son las derivadas de \( f_i \), la columna \( j \) la derivada respecto a \( x_j \):

$$ A=\left.\frac{\partial \mathbf{f}}{\partial \mathbf{x}}\right|_e=
\begin{bmatrix}\dfrac{\partial f_1}{\partial x_1}&\cdots&\dfrac{\partial f_1}{\partial x_n}\\[1.2em]\vdots&\ddots&\vdots\\[0.6em]\dfrac{\partial f_n}{\partial x_1}&\cdots&\dfrac{\partial f_n}{\partial x_n}\end{bmatrix}_{e},\qquad
B=\left.\frac{\partial \mathbf{f}}{\partial \mathbf{u}}\right|_e\in\mathbb{R}^{n\times m} $$

**Paso 5 — resultado.** El mismo argumento de los Pasos 1–3, componente a componente, da la ecuación de pequeña señal:

$$ \boxed{\;\Delta\dot{\mathbf{x}}=A\,\Delta\mathbf{x}+B\,\Delta\mathbf{u},\qquad A=\left.\frac{\partial \mathbf{f}}{\partial \mathbf{x}}\right|_e,\;\;B=\left.\frac{\partial \mathbf{f}}{\partial \mathbf{u}}\right|_e\;} $$

Los autovalores de este \( A \) son los polos del sistema en ese punto de operación, y alimentan directamente la [[representacion-espacio-estados]]. Cuando \( \mathbf{f} \) no se deriva a mano, las parciales se aproximan por diferencias finitas (ver [[linealizacion-numerica]]): perturbar cada \( x_j \) y medir el cambio en \( \mathbf{f} \) reconstruye columna a columna el Jacobiano.

## Cuándo y por qué se usa
Para diseñar y analizar control con herramientas lineales (polos, Bode, impedancia, LQR). El
régimen de gran señal (faltas, saturación) requiere otros métodos (simulación no lineal).

## Procedimiento (genérico)
1. Halla el equilibrio resolviendo \( \mathbf{f}(\mathbf{x}_e,\mathbf{u}_e)=0 \) (ver [[equilibrio-fsolve]]).
2. Calcula los Jacobianos \( A,B \) (y \( C,D \) de la salida): analíticamente o
   **numéricamente** (ver [[linealizacion-numerica]]).
3. Comprueba que el equilibrio es hiperbólico (ningún autovalor en el eje imaginario).
4. Recuerda el rango de validez: solo pequeña señal alrededor de ese punto.

## Ejemplo de código
```python
# linealizacion analitica de un pendulo: d/dt[theta, w] ; equilibrio theta=0
# A = [[0,1],[-g/l*cos(theta_e), -b/m]]  evaluado en theta_e=0  -> [[0,1],[-g/l,-b/m]]
```

## Parámetros y valores típicos
La región de validez depende de la curvatura de \( \mathbf{f} \); en convertidores, las
perturbaciones de pequeña señal (p.ej. inyección de impedancia con amplitud pequeña) están en
régimen lineal; las faltas, no.

## Errores comunes
- Linealizar fuera del equilibrio (residuo \( \neq 0 \)) → \( A \) sin sentido.
- Aplicar conclusiones del linealizado en gran señal (cuando hay saturación/current limiting).
- Equilibrio no hiperbólico (autovalor en \( j\omega \)): el linealizado no decide la estabilidad.

## Uso en proyectos
- **01/02**: todo el análisis de estabilidad e impedancia parte de la linealización en el punto
  de operación; el régimen de gran señal (faltas) se trató por simulación temporal.

## Conceptos relacionados
- [[linealizacion-numerica]] · [[equilibrio-fsolve]] · [[representacion-espacio-estados]] · [[modelado-sistemas]]

## Referencias
- Khalil, *Nonlinear Systems*, cap. 4.
