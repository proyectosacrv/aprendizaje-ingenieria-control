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
fecha_actualizacion: 2026-06-11
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
