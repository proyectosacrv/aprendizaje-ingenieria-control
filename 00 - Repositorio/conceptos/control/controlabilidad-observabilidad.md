---
titulo: Controlabilidad y observabilidad
slug: controlabilidad-observabilidad
categoria: control
tipo: concepto
nivel: intermedio
proyectos: []
objetivos: [saber si se pueden gobernar y estimar todos los estados de un sistema]
tags: [controlabilidad, observabilidad, espacio-estados, gramian, kalman, intermedio]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-30
relacionados: [representacion-espacio-estados, asignacion-polos-lqr, variables-estado, funcion-transferencia]
referencias:
  - "Ogata, Ingeniería de Control Moderna, Pearson"
  - "Skogestad, Postlethwaite, Multivariable Feedback Control, Wiley 2005"
---

## Definición
Dos propiedades estructurales del modelo en espacio de estados. **Controlabilidad:** la entrada
puede llevar el estado a cualquier punto en tiempo finito. **Observabilidad:** el estado puede
reconstruirse a partir de la salida medida.

## Fundamento teórico
Para \( \dot{\mathbf{x}}=A\mathbf{x}+B\mathbf{u} \), \( \mathbf{y}=C\mathbf{x} \), criterio de
rango de Kalman:
$$ \mathcal{C}=[\,B\ \ AB\ \ A^2B\ \dots\ A^{n-1}B\,],\qquad
   \mathcal{O}=\begin{bmatrix}C\\CA\\\vdots\\CA^{n-1}\end{bmatrix} $$
Controlable \( \iff \mathrm{rank}\,\mathcal{C}=n \); observable \( \iff \mathrm{rank}\,\mathcal{O}=n \).
Un modo (autovalor) **no controlable** no se puede mover con realimentación; uno **no observable**
no aparece en \( y \). Si además es **inestable**, el diseño es inviable (no estabilizable / no
detectable). La pérdida de rango suele venir de **cancelaciones polo-cero** ocultas en
\( G(s)=C(sI-A)^{-1}B \).

<div class="cfig"><img src="figuras/controlabilidad-observabilidad-kalman.png" alt="descomposicion de Kalman en cuatro subsistemas"><div class="cap">Descomposición de Kalman: cada modo cae en uno de cuatro grupos según se pueda gobernar (controlable) y/o estimar (observable). Solo el bloque controlable+observable admite diseño completo; un modo no controlable o no observable inestable hace el diseño inviable (no estabilizable / no detectable).</div></div>

## 1 — De dónde sale la matriz \( \mathcal{C}=[B\ AB\ \dots\ A^{n-1}B] \)
**Paso 1 — el estado alcanzado por la entrada.** La solución de \( \dot{\mathbf{x}}=A\mathbf{x}+B\mathbf{u} \) con \( \mathbf{x}(0)=0 \) es la integral de convolución con la exponencial matricial:

$$ \mathbf{x}(t)=\int_0^{t} e^{A(t-\tau)}B\,\mathbf{u}(\tau)\,d\tau $$

Controlable = este integral puede alcanzar **cualquier** \( \mathbf{x}(t) \) eligiendo \( \mathbf{u} \). Es decir, los vectores generados por \( e^{A\xi}B \) (al variar \( \xi \)) deben **abarcar todo** \( \mathbb{R}^n \).

**Paso 2 — desarrollar la exponencial.** Por definición \( e^{A\xi}=\sum_{k=0}^{\infty}\frac{\xi^k}{k!}A^k \). Entonces \( e^{A\xi}B \) es una combinación de los vectores \( B,\,AB,\,A^2B,\,A^3B,\dots \) con coeficientes escalares \( \xi^k/k! \). El subespacio alcanzable es exactamente \( \mathrm{span}\{A^kB:\ k\ge0\} \).

**Paso 3 — truncar por Cayley-Hamilton.** El teorema de Cayley-Hamilton dice que \( A \) satisface su propio polinomio característico de grado \( n \), luego \( A^n \) (y toda potencia superior) es combinación lineal de \( I,A,\dots,A^{n-1} \). Por tanto \( A^nB,A^{n+1}B,\dots \) **no añaden** direcciones nuevas: el subespacio alcanzable se genera ya con las \( n \) primeras potencias.

**Paso 4 — el criterio de rango.** Reuniendo esos generadores en una matriz \( n\times(n\cdot m) \):

$$ \mathcal{C}=[\,B\ \ AB\ \ A^2B\ \dots\ A^{n-1}B\,] $$

El espacio alcanzable es \( \mathrm{Im}(\mathcal{C}) \). Se llena todo \( \mathbb{R}^n \) si y solo si:

$$ \boxed{\;\mathrm{rank}\,\mathcal{C}=n\;} $$

**Paso 5 — observabilidad por dualidad.** El mismo argumento aplicado a reconstruir \( \mathbf{x}(0) \) desde \( \mathbf{y}=C\mathbf{x} \): derivando la salida, \( y=Cx \), \( \dot y=CAx \), \( \ddot y=CA^2x \), …, hasta \( CA^{n-1}x \) (otra vez Cayley-Hamilton trunca). El estado se despeja si esas filas son independientes, es decir \( \mathrm{rank}\,\mathcal{O}=n \) con \( \mathcal{O}=[C;CA;\dots;CA^{n-1}] \). Es el problema **dual**: \( (A,C) \) observable \( \iff (A^\top,C^\top) \) controlable, lo que usa el [[observador-estados]] para calcular \( L \).

## Cuándo y por qué se usa
Antes de diseñar realimentación de estado o un observador: la [[asignacion-polos-lqr|asignación de
polos]] exige controlabilidad y el observador exige observabilidad. En modelos grandes de
convertidor (15+ estados) detecta estados redundantes o desacoplados.

## Procedimiento (genérico)
1. Forma \( \mathcal{C} \) y \( \mathcal{O} \) (o sus gramianos en sistemas mal escalados).
2. Comprueba el rango (o valores singulares > tolerancia).
3. Si hay déficit, identifica qué modo y si es estable (estabilizable/detectable basta para control).
4. Reduce el modelo (elimina estados no controlables/observables) si procede.

## Ejemplo de aplicación real
**Problema:** Filtro LC de 2º orden con estados \( [i_L,\,v_C] \), entrada \( v_{sw} \) (tensión del convertidor), salida \( y=i_L \) (único sensor). Verificar controlabilidad y observabilidad para justificar un observador de \( v_C \).

Matrices: \( A=\bigl[\begin{smallmatrix}-r/L & -1/L \\ 1/C & 0\end{smallmatrix}\bigr] \), \( B=[1/L,\,0]^\top \), \( C=[1,\,0] \). Controlabilidad: \( \mathcal{C}=[B,\,AB]=[1/L,\,-r/L^2-1/(LC);\;0,\,1/(LC)] \). \( \det(\mathcal{C})=1/(L^2C)\neq0 \) (\( n=2 \)) → **controlable**. Observabilidad: \( \mathcal{O}=[C;\,CA]=[1,0;\,-r/L,-1/L] \). \( \det(\mathcal{O})=-1/L\neq0 \) → **observable** desde \( i_L \). Conclusión: con un único sensor de corriente se puede reconstruir \( v_C \) mediante un observador de Luenberger, evitando un sensor de tensión adicional.

## Ejemplo de código
```python
import control as ct, numpy as np
sys = ct.ss(A, B, C, D)
nc = np.linalg.matrix_rank(ct.ctrb(A, B))   # == n ?
no = np.linalg.matrix_rank(ct.obsv(A, C))   # == n ?
```

## Parámetros y valores típicos
Usar tolerancia relativa en el rango (sistemas mal condicionados). Los **gramianos**
(`ct.gram`) cuantifican "cuán" controlable/observable es cada modo (útil para reducción balanceada).

## Errores comunes
- Decidir el rango sin tolerancia numérica en matrices mal escaladas.
- Confundir controlabilidad (estado) con estabilizabilidad (solo los modos inestables).
- Cancelar polo-cero en \( G(s) \) creyendo que simplifica, ocultando un modo inestable.

## Conceptos relacionados
- [[representacion-espacio-estados]] · [[variables-estado]] · [[asignacion-polos-lqr]]

## Referencias
- Ogata, *Ingeniería de Control Moderna*.
- Skogestad, Postlethwaite, *Multivariable Feedback Control*, 2005.
