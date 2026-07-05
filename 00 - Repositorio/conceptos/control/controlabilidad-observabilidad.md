---
titulo: Controlabilidad y observabilidad
slug: controlabilidad-observabilidad
categoria: control
tipo: concepto
nivel: intermedio
proyectos: []
objetivos: [saber si se pueden gobernar y estimar todos los estados de un sistema]
tags: [controlabilidad, observabilidad, espacio-estados, gramian, kalman, cancelacion-polo-cero, intermedio]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-03
relacionados: [representacion-espacio-estados, asignacion-polos-lqr, variables-estado, funcion-transferencia, observador-estados]
referencias:
  - "Ogata, Ingeniería de Control Moderna, Pearson"
  - "Skogestad, Postlethwaite, Multivariable Feedback Control, Wiley 2005"
  - "Zhou, Doyle, Glover, Robust and Optimal Control, Prentice Hall 1996"
---

## Definición
Dos propiedades estructurales del modelo en espacio de estados. **Controlabilidad:** la entrada
puede llevar el estado a cualquier punto en tiempo finito. **Observabilidad:** el estado puede
reconstruirse a partir de la salida medida. Son los prerrequisitos para cualquier diseño de
realimentación de estado u observador.

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

<div class="cfig"><img src="figuras/controlabilidad-observabilidad-kalman.png" alt="descomposicion de Kalman en cuatro subsistemas"><div class="cap">Descomposición de Kalman: cada modo cae en uno de cuatro grupos según se pueda gobernar (controlable) y/o estimar (observable). Solo el bloque controlable+observable admite diseño completo; un modo no controlable o no observable inestable hace el diseño inviable.</div></div>

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

**Paso 5 — observabilidad por dualidad.** El mismo argumento aplicado a reconstruir \( \mathbf{x}(0) \) desde \( \mathbf{y}=C\mathbf{x} \): derivando la salida, \( y=Cx \), \( \dot y=CAx \), \( \ddot y=CA^2x \), …, hasta \( CA^{n-1}x \) (Cayley-Hamilton trunca). El estado se despeja si esas filas son independientes, es decir \( \mathrm{rank}\,\mathcal{O}=n \) con \( \mathcal{O}=[C;CA;\dots;CA^{n-1}] \). Problema **dual**: \( (A,C) \) observable \( \iff (A^\top,C^\top) \) controlable, lo que usa el [[observador-estados]] para calcular \( L \).

## 2 — El Gramian de controlabilidad: cuán controlable es cada modo

El criterio de rango dice *si* el sistema es controlable (sí/no). El **Gramian de controlabilidad** cuantifica *cuánto* esfuerzo de control se necesita para alcanzar cada dirección del espacio de estados, lo cual es fundamental para comparar modos o reducir modelos.

**Definición del Gramian.** Para un sistema estable (todos los autovalores de \( A \) con parte real negativa), el Gramian de controlabilidad en tiempo infinito es:

$$ W_c = \int_0^{\infty} e^{A\tau}BB^\top e^{A^\top\tau}\,d\tau $$

Es una matriz \( n\times n \) **definida positiva** si y solo si \( (A,B) \) es controlable. Sus autovalores cuantifican la "facilidad" de controlar en cada dirección: autovalor grande → esa dirección es fácil de alcanzar con poco esfuerzo de control; autovalor pequeño → esa dirección es difícil.

**La ecuación de Lyapunov.** En la práctica, \( W_c \) no se calcula con la integral: se obtiene resolviendo la ecuación de Lyapunov continua:

$$ A\,W_c + W_c\,A^\top + B B^\top = 0 $$

Esta ecuación tiene solución única si \( A \) es estable. En Python: `scipy.linalg.solve_continuous_lyapunov(A, B@B.T)`.

**Interpretación geométrica.** El conjunto de estados alcanzables con energía de control \( \int_0^\infty\|u\|^2 dt \le 1 \) es la **elipsoide** \( \{\mathbf{x}: \mathbf{x}^\top W_c^{-1}\mathbf{x}\le1\} \). Los ejes de la elipsoide son los autovectores de \( W_c \) y las longitudes de los semiejes son \( \sqrt{\lambda_i(W_c)} \). Una elipsoide muy alargada (un autovalor muy pequeño) indica que esa dirección es casi inalcanzable: sistema casi no controlable en esa dirección.

**Criterio de Kalman usando el Gramian.** Sistema controlable \( \iff W_c > 0 \) (definido positivo) \( \iff \mathrm{rank}(W_c)=n \). Para sistemas con mal condicionamiento numérico (como modelos de red eléctrica con grandes diferencias de escala), verificar \( \mathrm{rank}(W_c) \) con tolerancia es más robusto que verificar \( \mathrm{rank}(\mathcal{C}) \).

## 3 — El Gramian de observabilidad y la dualidad exacta

**Definición del Gramian de observabilidad.** Por dualidad con el Gramian de controlabilidad:

$$ W_o = \int_0^{\infty} e^{A^\top\tau}C^\top C\,e^{A\tau}\,d\tau $$

Satisface la ecuación de Lyapunov dual: \( A^\top W_o + W_o A + C^\top C = 0 \). El par \( (A,C) \) es observable \( \iff W_o > 0 \).

**Interpretación del Gramian de observabilidad.** El Gramian \( W_o \) mide cuánta "información" aporta la salida sobre cada dirección del estado inicial. Si \( \mathbf{x}(0) \) está en la dirección del autovector de \( W_o \) con autovalor grande, esa componente es fácil de estimar (deja una señal grande en \( y \)). Si el autovalor es pequeño, la componente apenas aparece en la salida: es casi no observable.

**La dualidad exacta.** Los sistemas \( (A,B) \) y \( (A^\top, C^\top) \) son duales: el Gramian de controlabilidad de \( (A^\top, C^\top) \) es exactamente el Gramian de observabilidad de \( (A,C) \). Formalmente:

$$ (A,B)\text{ controlable} \iff (A^\top, B^\top)\text{ observable} $$

Esta dualidad es la base del método de diseño del observador: calcular la ganancia \( L \) del observador es exactamente el mismo problema matemático que calcular la ganancia \( K \) de la realimentación de estado, pero sobre el sistema dual \( (A^\top, C^\top) \). De ahí la línea de código `L = place(A.T, C.T, obs_poles).T`.

**Reducción balanceada.** Si se normalizan las coordenadas de modo que \( W_c=W_o=\Sigma=\mathrm{diag}(\sigma_1,\dots,\sigma_n) \) (valores de Hankel), los estados con \( \sigma_i\approx0 \) son simultáneamente poco controlables Y poco observables: son candidatos a eliminar del modelo sin pérdida de información entrada-salida. Esta es la base de la reducción de orden balanceada (balanced truncation).

## 4 — Los modos no controlables y no observables: la cancelación polo-cero

**La cancelación polo-cero.** Cuando se calcula la función de transferencia \( G(s)=C(sI-A)^{-1}B \), puede haber un polo y un cero que se cancelen. Esta cancelación no es un error de cálculo: es la manifestación de que hay un modo del sistema que no aparece en la relación entrada-salida porque es no controlable, no observable, o ambas.

**Ejemplo concreto.** Sistema de segundo orden con \( A=\begin{bmatrix}-1&0\\0&-3\end{bmatrix} \), \( B=\begin{bmatrix}1\\0\end{bmatrix} \), \( C=\begin{bmatrix}1&0\end{bmatrix} \). La FDT es \( G(s)=1/(s+1) \): el polo en \( s=-3 \) ha desaparecido. ¿Por qué? Porque \( B \) no excita el segundo modo (\( B \) tiene cero en la segunda componente) y \( C \) no lo mide. El segundo modo existe en la dinámica del sistema pero no aparece en la relación entrada-salida: está **no controlable y no observable**.

**Por qué es peligroso.** Si el modo oculto es estable, el sistema funciona aparentemente bien: \( G(s) \) no muestra ningún problema y el controlador diseñado sobre \( G(s) \) estabiliza el lazo. Pero si el modo oculto es **inestable**, la energía de ese modo crece sin que ni la entrada ni la salida lo revelen. El sistema puede explotar internamente mientras el lazo de control parece estable. Este es el caso de un polo-cero inestable cancelado: el controlador lo cancela pero no lo estabiliza.

**La regla de oro.** Nunca cancelar deliberadamente un polo inestable con un cero: el polo sigue ahí y crece. Esto aparece frecuentemente cuando se intenta simplificar la planta de un convertidor con resonancias: si se cancela la resonancia del filtro LCL con un cero del controlador, la resonancia sigue activa y puede hacer explotar la corriente del condensador aunque la corriente de red parezca estable.

**Detectar modos ocultos.** La forma correcta de verificar si la cancelación es real (modo no observable/no controlable) o peligrosa (inestable) es:
1. Calcular los autovalores de \( A \) (todos los polos del sistema).
2. Calcular los polos de \( G(s) \) (solo los modos controlables y observables).
3. Los autovalores de \( A \) que no aparecen en los polos de \( G(s) \) son los modos ocultos.
4. Si alguno tiene parte real positiva: el sistema no es estabilizable o no detectable → el diseño es inviable.

## 5 — La forma canónica de Kalman: descomposición en cuatro subsistemas

Cualquier sistema lineal puede transformarse a la **forma canónica de Kalman** mediante un cambio de coordenadas que descompone el espacio de estados en cuatro subespacios invariantes según su controlabilidad y observabilidad. Esta descomposición es la respuesta estructural a la pregunta "¿qué partes del sistema son accesibles para el control y la observación?"

**Los cuatro bloques.** Con un cambio de coordenadas adecuado, el sistema toma la forma triangular por bloques:

$$ \dot{\mathbf{z}} = \begin{bmatrix}A_{co}&0&A_{13}&0\\ A_{21}&A_{\bar c o}&A_{23}&A_{24}\\ 0&0&A_{c\bar o}&0\\ 0&0&A_{43}&A_{\bar c\bar o}\end{bmatrix}\mathbf{z} + \begin{bmatrix}B_{co}\\0\\0\\0\end{bmatrix}u $$

$$ y = \begin{bmatrix}C_{co}&0&C_{c\bar o}&0\end{bmatrix}\mathbf{z} $$

donde los cuatro bloques de estado son:
- \( \mathbf{z}_{co} \): **controlable y observable** — el único que aparece en \( G(s) \); admite diseño completo.
- \( \mathbf{z}_{\bar c o} \): **no controlable y observable** — aparece en la salida pero la entrada no puede moverlo; si es estable, es detectable (el observador puede estimarlo).
- \( \mathbf{z}_{c\bar o} \): **controlable y no observable** — la entrada puede excitarlo pero no aparece en \( y \); hay que asegurar que sea estable o usar otro sensor.
- \( \mathbf{z}_{\bar c\bar o} \): **no controlable y no observable** — completamente oculto; debe ser estable para que el sistema completo lo sea.

**La función de transferencia solo ve \( \mathbf{z}_{co} \).** La FDT \( G(s) \) coincide exactamente con el subsistema controlable+observable:

$$ G(s) = C_{co}(sI-A_{co})^{-1}B_{co} $$

Por eso la FDT puede dar la impresión de estabilidad aunque los bloques \( \bar c\bar o \) o \( \bar c o \) sean inestables.

**Estabilizabilidad y detectabilidad.** Para el diseño de control no siempre se necesita controlabilidad/observabilidad total:
- **Estabilizable:** \( (A,B) \) estabilizable \( \iff \) los modos **no controlables** son todos estables (la entrada no los puede mover, pero tampoco hace falta: ya son estables por sí solos).
- **Detectable:** \( (A,C) \) detectable \( \iff \) los modos **no observables** son todos estables (no aparecen en \( y \), pero tampoco hace falta estimarlos: son estables).

Estabilizabilidad + detectabilidad son las condiciones mínimas para diseñar un controlador que estabilice el lazo cerrado y un observador que no diverja.

<div class="cfig"><img src="figuras/controlabilidad-observabilidad-analisis.png" alt="cuatro paneles: gramian de controlabilidad, rango vs estados, modo oculto, verificacion LCL"><div class="cap">(a) Gramian de controlabilidad: elipsoide de alcanzabilidad con sus ejes principales. (b) Valor singular mínimo de Mc vs número de estados: cuántos son controlables. (c) Cancelación polo-cero: el modo oculto crece aunque la salida parezca estable. (d) Verificación del LCL: rango(Mc) y rango(Mo) para distintas salidas medidas.</div></div>

## 6 — Diseño iterativo: verificar controlabilidad y observabilidad del modelo LCL (3 estados)

**Modelo del LCL.** Estados \( \mathbf{x}=[i_{L1},v_C,i_{L2}]^\top \), entrada \( u=v_i \) (tensión del convertidor), perturbación \( v_{pcc} \) (se ignora para el análisis de controlabilidad). Con \( R_1=R_2=0 \) (caso ideal):

$$ A = \begin{bmatrix}-R_1/L_1 & -1/L_1 & 0 \\ 1/C_f & 0 & -1/C_f \\ 0 & 1/L_2 & -R_2/L_2\end{bmatrix},\quad B=\begin{bmatrix}1/L_1\\0\\0\end{bmatrix} $$

**Controlabilidad.** La matriz de controlabilidad es:

$$ \mathcal{C}=[B\ \ AB\ \ A^2B] $$

Con los valores \( L_1=2\,\text{mH} \), \( C_f=20\,\mu\text{F} \), \( L_2=0{,}5\,\text{mH} \):
\( \det(\mathcal{C})=-1/(L_1^2 L_2 C_f^2)\neq0 \) → **controlable**. La entrada \( v_i \) puede llevar los tres estados a cualquier punto.

**Observabilidad según la variable medida.** Aquí es donde cambia el resultado:

| Salida medida | \( C \) | \( \mathrm{rank}(\mathcal{O}) \) | Observable? |
|---|---|---|---|
| \( i_{L1} \) | \( [1,0,0] \) | 3 | Sí — pero es la corriente del lado fuente |
| \( v_C \) | \( [0,1,0] \) | 3 | Sí — tensión del condensador |
| \( i_{L2} \) | \( [0,0,1] \) | 3 | Sí — corriente de red (la más común) |
| \( i_{L1},i_{L2} \) | \( [[1,0,0],[0,0,1]] \) | 3 | Sí (dos sensores) |

El LCL de 3 estados es **observable desde cualquiera de sus tres variables**, lo que permite diseñar un observador de orden 2 o 3 midiendo solo una de ellas. Esto justifica el amortiguamiento activo sin sensor de \( v_C \) (se estima \( v_C \) midiendo solo \( i_{L2} \)).

**Caso límite: observabilidad desde \( i_{L2} \) con \( R_1=R_2=0 \).** Con resistencias nulas exactas, el rango de \( \mathcal{O} \) cae a 2 (¡el sistema se vuelve no completamente observable!). La razón: sin amortiguamiento, los modos de la resonancia son polos puramente imaginarios y la dinámica de \( v_C \) no se transfiere a \( i_{L2} \) de forma distinguible. Por eso en la práctica siempre se incluyen al menos las resistencias parásitas, y la observabilidad se verifica con los valores reales de \( R_1 \), \( R_2 \), no con el modelo ideal.

**Implicación de diseño.** Para el amortiguamiento activo del LCL, el observador estimará \( v_C \) midiendo \( i_{L2} \). La condición de observabilidad garantiza que esto es posible, pero la calidad de la estimación depende del Gramian de observabilidad: si el autovalor mínimo de \( W_o \) es pequeño, \( v_C \) es difícil de estimar y el observador será sensible al ruido de medida.

## Cuándo y por qué se usa
Antes de diseñar realimentación de estado o un observador: la asignación de polos exige
controlabilidad y el [[observador-estados|observador]] exige observabilidad. En modelos grandes de
convertidor (15+ estados) detecta estados redundantes o desacoplados.

## Procedimiento (genérico)
1. Forma \( \mathcal{C} \) y \( \mathcal{O} \) (o sus Gramianos en sistemas mal escalados).
2. Comprueba el rango (o valores singulares > tolerancia).
3. Si hay déficit, identifica qué modo y si es estable (estabilizable/detectable basta para control).
4. Verifica que no hay cancelaciones polo-cero con modos inestables.
5. Reduce el modelo (elimina estados no controlables/observables) si procede.

## Ejemplo de aplicación real
**Problema:** Filtro LC de 2º orden con estados \( [i_L,\,v_C] \), entrada \( v_{sw} \), salida \( y=i_L \). Verificar controlabilidad y observabilidad para justificar un observador de \( v_C \).

Matrices: \( A=\bigl[\begin{smallmatrix}-r/L & -1/L \\ 1/C & 0\end{smallmatrix}\bigr] \), \( B=[1/L,\,0]^\top \), \( C=[1,\,0] \). Controlabilidad: \( \mathcal{C}=[B,\,AB] \), \( \det(\mathcal{C})=1/(L^2C)\neq0 \) → **controlable**. Observabilidad: \( \mathcal{O}=[C;\,CA] \), \( \det(\mathcal{O})=-1/L\neq0 \) → **observable** desde \( i_L \). Conclusión: con un único sensor de corriente se puede reconstruir \( v_C \) mediante un observador de Luenberger.

## Ejemplo de código
```python
import control as ct, numpy as np
sys = ct.ss(A, B, C, D)
Mc = ct.ctrb(A, B)
Mo = ct.obsv(A, C)
nc = np.linalg.matrix_rank(Mc, tol=1e-8)   # == n ?
no = np.linalg.matrix_rank(Mo, tol=1e-8)   # == n ?

# Gramian de controlabilidad (via Lyapunov)
import scipy.linalg
Wc = scipy.linalg.solve_continuous_lyapunov(A, -B @ B.T)
# Wc > 0 iff controlable; autovalores pequenos -> casi no controlable en esa dir
print("svd(Mc):", np.linalg.svd(Mc, compute_uv=False))
```

## Parámetros y valores típicos
Usar tolerancia relativa en el rango (sistemas mal condicionados). Los **Gramianos**
(`ct.gram`) cuantifican "cuán" controlable/observable es cada modo (útil para reducción balanceada).
El valor singular mínimo de \( \mathcal{C} \) o \( \mathcal{O} \) es la distancia a ser no controlable/observable.

## Errores comunes
- Decidir el rango sin tolerancia numérica en matrices mal escaladas.
- Confundir controlabilidad (estado) con estabilizabilidad (solo los modos inestables).
- Cancelar polo-cero en \( G(s) \) creyendo que simplifica, ocultando un modo inestable.
- Verificar con \( R=0 \) cuando las resistencias parásitas son las que dan observabilidad.

## 4 — Gramians de controlabilidad y observabilidad

**Gramian de controlabilidad \( W_c \).** Cuantifica el esfuerzo mínimo de control para alcanzar cada dirección del espacio de estados. Se define como:

$$ W_c = \int_0^\infty e^{A\tau}BB^T e^{A^T\tau}\,d\tau $$

En la práctica se calcula resolviendo la ecuación de Lyapunov continua:

$$ A\,W_c + W_c\,A^T + B\,B^T = 0 $$

cuya solución única existe si y solo si \( A \) es estable. El conjunto de estados alcanzables con energía unitaria de control es la elipsoide \( \{\mathbf{x}: \mathbf{x}^T W_c^{-1}\mathbf{x} \leq 1\} \); sus semiejes son \( \sqrt{\lambda_i(W_c)} \). Autovalor pequeño de \( W_c \) → esa dirección es casi inalcanzable.

**Gramian de observabilidad \( W_o \).** Por dualidad exacta, cuantifica cuánta información aporta la salida sobre cada componente del estado inicial:

$$ W_o = \int_0^\infty e^{A^T\tau}C^TC\,e^{A\tau}\,d\tau $$

Ecuación de Lyapunov dual: \( A^T W_o + W_o A + C^T C = 0 \). Autovalor pequeño de \( W_o \) → esa componente del estado apenas aparece en la salida medida.

**Interpretación conjunta.** Los valores propios de \( W_c \) y \( W_o \) miden el grado de controlabilidad/observabilidad de cada dirección del espacio de estados. Un modo con autovalor muy pequeño en \( W_c \) y también en \( W_o \) es un candidato directo a ser eliminado del modelo sin afectar la respuesta entrada-salida.

**Realización balanceada.** Existe un cambio de coordenadas tal que \( W_c = W_o = \Sigma = \text{diag}(\sigma_1,\ldots,\sigma_n) \) con \( \sigma_1 \geq \sigma_2 \geq \ldots \geq \sigma_n > 0 \). En estas coordenadas balanceadas, \( \sigma_i \) son los **valores de Hankel** del sistema: una sola escala mide simultáneamente cuán controlable y observable es cada modo.

## 5 — Reducción de orden por eliminación de modos

**Hankel Singular Values (HSV).** En la realización balanceada, los valores de Hankel \( \sigma_i \) ordenados de mayor a menor son los HSV del sistema. Representan la contribución de cada modo a la relación entrada-salida: \( \sigma_1 \gg \sigma_n \) indica que el sistema tiene una estructura de bajo orden efectivo.

**Truncamiento balanceado.** Se eliminan los estados \( i = r+1, \ldots, n \) con \( \sigma_i \ll \sigma_1 \). El error de la aproximación \( G_r(s) \) al sistema original \( G(s) \) está acotado:

$$ \|G(j\omega) - G_r(j\omega)\|_\infty \leq 2\sum_{i=r+1}^{n} \sigma_i $$

Esta cota en norma-\( H_\infty \) garantiza que el modelo reducido no introduce errores de ganancia superiores a \( 2\sum \sigma_i \) en ninguna frecuencia.

**Criterio de truncamiento.** La regla práctica habitual es mantener los estados con:

$$ \sigma_i > \frac{\sigma_1}{100} $$

Los estados con \( \sigma_i < \sigma_1/100 \) contribuyen menos del 1% de la ganancia del modo dominante y son seguros de eliminar.

**Aplicación en convertidores.** Un modelo de convertidor con filtro LCL, lazos de control discretos y red puede tener 10–15 estados. El truncamiento balanceado permite reducirlo a 3–5 estados sin perder la dinámica relevante para el análisis de estabilidad. Los modos de alta frecuencia (resonancias del PWM, retardos de cómputo de orden superior) se eliminan por tener HSV muy pequeños respecto a los modos dominantes de baja frecuencia.

## 6 — Observabilidad en convertidores: estimación de estado

**Estados observables desde el PCC.** Midiendo tensión y corriente en el punto de conexión común (PCC), los estados del filtro LCL son observables si el par \( (A,C) \) es de rango completo. La corriente de red \( i_{L2} \) y la tensión del condensador \( v_C \) son observables desde cualquier combinación de medidas del LCL (véase sección 6 de controlabilidad-observabilidad).

**Tensión de red \( v_g \).** Si la admitancia de red \( Y_{grid} \) es conocida, la tensión de red puede estimarse como estado aumentado. Si \( Y_{grid} \) varía (red débil con inductancia variable), la estimación introduce sesgo proporcional al error paramétrico.

**SOC de batería.** El estado de carga (SOC) de una batería no es directamente observable desde la tensión terminal porque la relación SOC-tensión es no lineal y depende de la temperatura. Se necesita un filtro de Kalman extendido (EKF) o un estimador de estado aumentado que incluya la dinámica electroquímica.

**Observador de Luenberger para el LCL.** La ecuación del observador:

$$ \dot{\hat{\mathbf{x}}} = A\hat{\mathbf{x}} + B\mathbf{u} + L(\mathbf{y} - C\hat{\mathbf{x}}) $$

Los polos de \( A - LC \) se colocan 3–5 veces más rápidos que los del lazo de corriente para que el error de estimación decaiga antes de afectar al control. Esto garantiza que el principio de separación sea válido en la práctica: el diseño del observador y del controlador son (aproximadamente) independientes.

**Velocidad del observador vs ruido.** Polos del observador más rápidos → el error decae más rápido pero la ganancia \( L \) es mayor → amplificación del ruido de medida en el estado estimado \( \hat{\mathbf{x}} \). En sistemas reales con ADC de 12 bits y ruido de cuantificación, existe un límite práctico a la velocidad del observador: tipicamente \( \omega_{obs} \leq 5\,\omega_{control} \).

<div class="cfig"><img src="../figuras/controlabilidad-observabilidad-analisis.png" alt="cuatro paneles: Hankel SVs, matriz controlabilidad, observador Luenberger, modos y controlabilidad modal"><div class="cap">(a) Hankel Singular Values: modos a eliminar en truncamiento balanceado. (b) Matriz de controlabilidad: visualización del rango. (c) Observador de Luenberger: estimación del estado real. (d) Controlabilidad modal: tamaño del símbolo proporcional a la proyección de B sobre cada modo.</div></div>

## Conceptos relacionados
- [[representacion-espacio-estados]] · [[variables-estado]] · [[asignacion-polos-lqr]] · [[observador-estados]]

## Referencias
- Ogata, *Ingeniería de Control Moderna*.
- Skogestad, Postlethwaite, *Multivariable Feedback Control*, 2005.
- Zhou, Doyle, Glover, *Robust and Optimal Control*, 1996.
