---
titulo: Representación en espacio de estados
slug: representacion-espacio-estados
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance, 03-DataCenter-IA]
objetivos: [escribir el modelo como x'=Ax+Bu y analizar sus propiedades]
tags: [espacio-estados, A-B-C-D, controlabilidad, observabilidad, MIMO]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-30
relacionados: [variables-estado, modelado-sistemas, asignacion-polos-lqr, respuesta-frecuencia-ss, linealizacion-teoria]
referencias:
  - "Kailath, Linear Systems, Prentice Hall 1980"
---

## Definición
Forma estándar de escribir un sistema dinámico lineal mediante sus variables de estado:
$$ \dot{\mathbf{x}} = A\,\mathbf{x} + B\,\mathbf{u}, \qquad \mathbf{y} = C\,\mathbf{x} + D\,\mathbf{u} $$
Es la base del análisis y diseño modernos, natural para sistemas MIMO y de orden alto.

<div class="cfig"><img src="figuras/representacion-espacio-estados-bloques.png" alt="diagrama de bloques del espacio de estados"><div class="cap">Diagrama del espacio de estados: B inyecta la entrada, el integrador produce x a partir de ẋ, A realimenta el estado y C lo proyecta a la salida (más D·u directo, omitido).</div></div>

## Fundamento teórico
Significado de las matrices:
- \( A \) (dinámica): sus **autovalores son los polos**; gobiernan estabilidad y modos.
- \( B \) (entrada): cómo actúan las entradas sobre los estados.
- \( C \) (salida): qué se mide.
- \( D \) (transmisión directa): efecto entrada→salida instantáneo.

Relación con la función de transferencia:
$$ G(s) = C\,(sI-A)^{-1}B + D $$
Dos propiedades estructurales clave:
- **Controlabilidad**: ¿puede la entrada llevar el estado a cualquier valor? Matriz
  \( \mathcal{C}=[B\;AB\;\dots\;A^{n-1}B] \) de rango \( n \). Necesaria para asignar polos / LQR.
- **Observabilidad**: ¿puede reconstruirse el estado a partir de la salida? Matriz
  \( \mathcal{O}=[C;\,CA;\,\dots;\,CA^{n-1}] \) de rango \( n \). Necesaria para el observador.

## 1 — De la función de transferencia a la forma canónica controlable
La relación \( G(s)=C(sI-A)^{-1}B+D \) va de estado a transferencia. El camino inverso —dado \( G(s) \), construir un \( (A,B,C,D) \)— se llama **realización**. Hay infinitas (cualquier cambio de base \( \mathbf{z}=T\mathbf{x} \) da otra), pero una es directa de leer: la **forma canónica controlable**, donde \( A,B \) salen de los denominadores y \( C,D \) de los numeradores.

**Paso 1 — partir de una transferencia estrictamente propia.** Sea, sin pérdida de generalidad, una transferencia de orden \( n \) con denominador mónico:

$$ G(s)=\frac{b_{n-1}s^{n-1}+\dots+b_1 s+b_0}{s^n+a_{n-1}s^{n-1}+\dots+a_1 s+a_0} $$

(Si el grado de numerador y denominador coincide, se hace primero la división polinómica: el cociente es \( D \) y el resto es esta fracción estrictamente propia.)

**Paso 2 — introducir una variable auxiliar.** Definimos \( V(s) \) por

$$ V(s)=\frac{U(s)}{s^n+a_{n-1}s^{n-1}+\dots+a_0}\;\;\Longrightarrow\;\; Y(s)=\big(b_{n-1}s^{n-1}+\dots+b_0\big)V(s) $$

El truco: el **denominador** actúa solo sobre \( v \), y el **numerador** solo reconstruye la salida. En el dominio temporal la primera relación es la EDO

$$ v^{(n)}+a_{n-1}v^{(n-1)}+\dots+a_1\dot v+a_0 v = u $$

**Paso 3 — estados = \( v \) y sus derivadas.** Igual que en [[variables-estado]], tomamos \( x_1=v,\;x_2=\dot v,\;\dots,\;x_n=v^{(n-1)} \). Las cadenas \( \dot x_k=x_{k+1} \) y el despeje de \( v^{(n)} \) de la EDO dan la matriz de dinámica y la de entrada:

$$ A=\begin{bmatrix}0&1&0&\cdots&0\\0&0&1&\cdots&0\\\vdots&&&\ddots&\vdots\\0&0&0&\cdots&1\\-a_0&-a_1&-a_2&\cdots&-a_{n-1}\end{bmatrix},\qquad
B=\begin{bmatrix}0\\0\\\vdots\\0\\1\end{bmatrix} $$

**Paso 4 — la salida lee los numeradores.** Como \( y=b_{n-1}v^{(n-1)}+\dots+b_1\dot v+b_0 v=b_0 x_1+b_1 x_2+\dots+b_{n-1}x_n \), la matriz de salida son directamente los coeficientes del numerador, y \( D=0 \) (por ser estrictamente propia):

$$ \boxed{\;C=\begin{bmatrix}b_0&b_1&\cdots&b_{n-1}\end{bmatrix},\qquad D=0\;} $$

**Paso 5 — por qué "controlable".** Con este \( (A,B) \), la matriz de controlabilidad \( \mathcal{C}=[\,B\;AB\;\cdots\;A^{n-1}B\,] \) resulta triangular con unos en la antidiagonal, luego de rango \( n \) **siempre**: esta realización es controlable por construcción, sea cual sea \( G(s) \). De ahí el nombre. Si además \( G(s) \) no tiene cancelaciones polo-cero, también es observable y es una realización **mínima** (orden \( n \) = grado del denominador).

## Cuándo y por qué se usa
Es el lenguaje del control en estado (LQR, observadores) y del análisis modal. Permite tratar de
forma unificada sistemas con muchos estados y varias entradas/salidas, como un convertidor.

## Procedimiento (genérico)
1. Elige las variables de estado (ver [[variables-estado]]).
2. Escribe las ecuaciones en forma \( \dot{\mathbf{x}}=A\mathbf{x}+B\mathbf{u} \) (o lineliza si es no lineal).
3. Define la salida \( \mathbf{y}=C\mathbf{x}+D\mathbf{u} \).
4. Comprueba controlabilidad y observabilidad antes de diseñar control/observador.
5. Úsalo para polos (autovalores), impedancia (\( G(s) \)) o diseño en estado (ver [[asignacion-polos-lqr]]).

## Ejemplo de código
```python
import numpy as np, control as ct
sys = ct.ss(A, B, C, D)
ctrb_rank = np.linalg.matrix_rank(ct.ctrb(A, B))   # = n si es controlable
obsv_rank = np.linalg.matrix_rank(ct.obsv(A, C))   # = n si es observable
```

## Parámetros y valores típicos
\( n \) = orden (nº de estados). En el proyecto GFM, \( n=15 \); GFL, \( n=10 \).

## Errores comunes
- Diseñar realimentación de estado sin comprobar controlabilidad (puede no existir solución).
- Invertir \( (sI-A) \) explícitamente en vez de resolver el sistema (peor numéricamente).

## Uso en proyectos
- **01/02**: el modelo linealizado \( (A,B,C,D) \) se usa para polos (estabilidad) e impedancia
  \( G(s)=C(sI-A)^{-1}B+D \). Ver [[respuesta-frecuencia-ss]].

## Conceptos relacionados
- [[variables-estado]] · [[asignacion-polos-lqr]] · [[respuesta-frecuencia-ss]] · [[linealizacion-teoria]]

## Referencias
- Kailath, *Linear Systems*, 1980.
