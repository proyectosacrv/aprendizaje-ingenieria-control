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
fecha_actualizacion: 2026-07-01
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

## 2 — Controlabilidad y observabilidad: derivación del rango

Controlar un sistema significa poder llevar su estado desde cualquier condición inicial a cualquier estado destino en tiempo finito, usando entradas acotadas. Que esto sea posible tiene una condición algebraica exacta sobre \( (A,B) \).

**¿Por qué la matriz de controlabilidad?** La solución de \( \dot{\mathbf{x}}=A\mathbf{x}+B\mathbf{u} \) con \( \mathbf{x}(0)=\mathbf{x}_0 \) es

$$ \mathbf{x}(T)=e^{AT}\mathbf{x}_0+\int_0^T e^{A(T-\tau)}B\,\mathbf{u}(\tau)\,d\tau $$

Para llevar \( \mathbf{x}(T) \) al origen necesitamos que el vector \( -e^{AT}\mathbf{x}_0 \) caiga en el rango de la integral. Expandiendo \( e^{A(T-\tau)} \) en serie de potencias de \( A \) y evaluando la integral, el rango de esa integral coincide exactamente con el rango de la matriz de Gram de controlabilidad

$$ W_c=\int_0^T e^{A\tau}BB^\top e^{A^\top\tau}\,d\tau $$

cuyo rango es idéntico al rango de

$$ \boxed{\;\mathcal{C}=\begin{bmatrix}B & AB & A^2B & \cdots & A^{n-1}B\end{bmatrix}\;} $$

Esto se sigue del teorema de Cayley–Hamilton: \( A^n \) es combinación lineal de \( I,A,\ldots,A^{n-1} \), de modo que las columnas de \( e^{A\tau}B \) no añaden direcciones nuevas más allá de las \( n-1 \) potencias. El **criterio de Kalman** establece:

> El par \( (A,B) \) es completamente controlable si y solo si \( \text{rank}(\mathcal{C})=n \).

Si \( \text{rank}(\mathcal{C})<n \) existe un subespacio de \( \mathbb{R}^n \) que ninguna entrada puede alcanzar. En la práctica, un motor con una variable de estado sin conectar a ninguna entrada sería un ejemplo: ese modo oscila libre, indiferente al control.

**Observabilidad: el dual exacto.** Observar significa reconstruir \( \mathbf{x}(0) \) a partir de \( \mathbf{y}(t) \) en \( [0,T] \). Escribiendo la salida

$$ \mathbf{y}(t)=C\,e^{At}\mathbf{x}(0)+(\text{términos conocidos}) $$

y expandiendo \( e^{At} \), el conjunto de \( \mathbf{x}(0) \) que produce \( \mathbf{y}\equiv 0 \) (espacio nulo observable) es el núcleo de la **matriz de observabilidad**:

$$ \boxed{\;\mathcal{O}=\begin{bmatrix}C\\CA\\CA^2\\\vdots\\CA^{n-1}\end{bmatrix}\;} $$

El par \( (A,C) \) es completamente observable si y solo si \( \text{rank}(\mathcal{O})=n \), equivalentemente si \( \ker(\mathcal{O})=\{0\} \).

**Dualidad.** Existe una simetría algebraica exacta: si se define el sistema dual con matrices \( (A^\top, C^\top, B^\top, D^\top) \), la controlabilidad del original equivale a la observabilidad del dual y viceversa:

$$ (A,B)\text{ controlable} \;\Longleftrightarrow\; (A^\top,B^\top)\text{ observable} $$

Esto tiene consecuencias prácticas: los teoremas sobre controlabilidad se "trasladan" a observabilidad con solo transponer, y los algoritmos de cómputo son los mismos.

**Verificación numérica.** En Python con NumPy y la librería `control`:

```python
import numpy as np
import control as ct

# construir el sistema
sys = ct.ss(A, B, C, D)

# rango de la matriz de controlabilidad
Mc = ct.ctrb(A, B)          # shape (n, n*m)
rank_c = np.linalg.matrix_rank(Mc)
print(f"Controlable: {rank_c == A.shape[0]}")

# rango de la matriz de observabilidad
Mo = ct.obsv(A, C)          # shape (n*p, n)
rank_o = np.linalg.matrix_rank(Mo)
print(f"Observable:  {rank_o == A.shape[0]}")
```

Nota sobre condicionamiento: `matrix_rank` usa descomposición en valores singulares (SVD) y un umbral relativo al mayor singular value. Para sistemas de orden alto (como \( n=15 \) del proyecto GFM) conviene también inspeccionar el número de condición de \( \mathcal{C} \): si es muy alto (~\(10^{10}\)), la controlabilidad existe en teoría pero el sistema está cerca del límite práctico.

## 3 — La solución analítica: \( e^{At} \)

La ecuación \( \dot{\mathbf{x}}=A\mathbf{x}+B\mathbf{u} \) es una EDO lineal de coeficientes constantes. Su solución tiene la misma forma que la ecuación escalar \( \dot x = ax+bu \), salvo que ahora los exponenciales son de matrices.

**La integral de variación de constantes.** Multiplicando por el factor integrante \( e^{-At} \) y usando la regla del producto para \( \frac{d}{dt}(e^{-At}\mathbf{x}) \):

$$ \frac{d}{dt}\bigl(e^{-At}\mathbf{x}\bigr) = e^{-At}(\dot{\mathbf{x}}-A\mathbf{x}) = e^{-At}B\,\mathbf{u}(t) $$

Integrando de 0 a \( t \):

$$ \boxed{\;\mathbf{x}(t)=e^{At}\mathbf{x}(0)+\int_0^t e^{A(t-\tau)}B\,\mathbf{u}(\tau)\,d\tau\;} $$

El primer término es la **respuesta libre** (depende solo de \( \mathbf{x}(0) \)) y el segundo la **respuesta forzada** (convolución de la entrada con la respuesta al impulso de la matriz).

**La serie de la matriz exponencial.** La función \( e^{At} \) se define por la misma serie de Taylor que el escalar, reemplazando el número por la matriz:

$$ e^{At}=I+At+\frac{(At)^2}{2!}+\frac{(At)^3}{3!}+\cdots=\sum_{k=0}^\infty\frac{(At)^k}{k!} $$

La serie converge para toda matriz \( A \) y todo \( t \), pero calcularla término a término es ineficiente. Para uso numérico se emplean algoritmos de escala y cuadrado (Padé), que es lo que hace `scipy.linalg.expm`. Para uso analítico importa la forma cerrada.

**Caso diagonal.** Si \( A=\Lambda=\mathrm{diag}(\lambda_1,\ldots,\lambda_n) \), entonces \( \Lambda^k=\mathrm{diag}(\lambda_1^k,\ldots,\lambda_n^k) \) y la serie da simplemente

$$ e^{\Lambda t}=\mathrm{diag}\!\left(e^{\lambda_1 t},\;\ldots,\;e^{\lambda_n t}\right) $$

Cada estado evoluciona independientemente, con su propio modo \( e^{\lambda_i t} \).

**Caso general: diagonalización.** Si \( A \) es diagonalizable con \( A=\Phi\Lambda\Phi^{-1} \) (donde las columnas de \( \Phi \) son los autovectores derechos), entonces

$$ e^{At}=\Phi\,e^{\Lambda t}\,\Phi^{-1} $$

lo que muestra que la dinámica es siempre una **suma de modos** \( e^{\lambda_i t} \), ponderados por los autovectores. Si \( A \) no es diagonalizable (autovalores repetidos con déficit de autovectores) se usa la forma de Jordan, que introduce términos \( t^k e^{\lambda t} \).

**Condición de estabilidad.** De la expresión modal se ve directamente:

$$ e^{At}\to 0 \;\;\text{cuando}\;\; t\to\infty \;\;\Longleftrightarrow\;\; \mathrm{Re}(\lambda_i)<0\;\;\forall i $$

Todos los modos deben decaer, es decir, todos los autovalores de \( A \) deben estar en el semiplano izquierdo abierto. Un solo autovalor con parte real positiva o nula basta para que el sistema sea inestable (o marginalmente estable).

**Ejemplo numérico.** Para \( A=\begin{bmatrix}-1&2\\0&-3\end{bmatrix} \), los autovalores son \( \lambda_1=-1, \lambda_2=-3 \). Los elementos de \( e^{At} \) son combinaciones de \( e^{-t} \) y \( e^{-3t} \): el panel (b) de la figura muestra cómo decaen los tres elementos independientes.

<div class="cfig"><img src="figuras/representacion-espacio-estados-analisis.png" alt="espacio de estados: análisis avanzado"><div class="cap">(a) Diagrama de bloques del espacio de estados: B inyecta la entrada, el integrador acumula x, A realimenta y C proyecta a la salida. (b) Elementos de e^(At) para A 2×2 con λ₁=−1, λ₂=−3: todos decaen, el elemento (1,2) tiene un máximo antes de caer porque el modo lento tarda en dominar. (c) Polos de G(s) para el filtro LCL 3×3: par complejo conjugado en la frecuencia de resonancia (~1.3 kHz). (d) Respuesta al impulso del LCL: la solución analítica Ce^(At)B coincide con Euler explícito a Δt=2 µs.</div></div>

## 4 — De \( (A,B,C,D) \) a \( G(s) \): la fórmula \( C(sI-A)^{-1}B+D \)

La función de transferencia aparece aplicando la transformada de Laplace a las ecuaciones de estado. La derivación es corta pero merece hacerse explícita porque aclara por qué los polos son los autovalores de \( A \).

**Derivación.** Partiendo de \( \dot{\mathbf{x}}=A\mathbf{x}+B\mathbf{u} \) con condición inicial nula \( \mathbf{x}(0^-)=0 \), la transformada de Laplace da

$$ s\,X(s) = A\,X(s)+B\,U(s) $$

Despejando \( X(s) \):

$$ (sI-A)\,X(s)=B\,U(s) \;\;\Longrightarrow\;\; X(s)=(sI-A)^{-1}B\,U(s) $$

La inversa existe mientras \( \det(sI-A)\neq 0 \), es decir, fuera de los autovalores de \( A \). Aplicando la ecuación de salida \( Y(s)=C\,X(s)+D\,U(s) \):

$$ \boxed{\;G(s)=C\,(sI-A)^{-1}B+D\;} $$

**El denominador es el polinomio característico.** Por la fórmula de la inversa de una matriz,

$$ (sI-A)^{-1}=\frac{\mathrm{adj}(sI-A)}{\det(sI-A)} $$

El denominador de \( G(s) \) es siempre \( \det(sI-A) \), que es exactamente el **polinomio característico** \( p(\lambda)=\det(\lambda I-A)=\prod_{i=1}^n(\lambda-\lambda_i) \). Por tanto los **polos de \( G(s) \) son los autovalores de \( A \)** (salvo posibles cancelaciones polo-cero si hay raíces comunes con el numerador).

**Ejemplo: filtro LCL 3×3.** Con \( L_1=2\,\mathrm{mH} \), \( L_2=0.5\,\mathrm{mH} \), \( C_f=15\,\mu\mathrm{F} \), \( R_1=0.05\,\Omega \) y estados \( (i_{L1}, i_{L2}, v_C) \):

$$ A=\begin{bmatrix}-R_1/L_1 & 0 & -1/L_1 \\ 0 & 0 & 1/L_2 \\ 1/C_f & -1/C_f & 0\end{bmatrix},\quad B=\begin{bmatrix}1/L_1\\0\\0\end{bmatrix},\quad C=\begin{bmatrix}0&1&0\end{bmatrix} $$

El polinomio \( \det(sI-A) \) es de grado 3; tiene un polo real (amortiguado por \( R_1 \)) y un par complejo conjugado en la frecuencia de resonancia

$$ f_\mathrm{res}=\frac{1}{2\pi}\sqrt{\frac{L_1+L_2}{L_1 L_2 C_f}}\approx 1{.}3\,\mathrm{kHz} $$

visible en el panel (c) de la figura como un par de cruces (polos) en el eje imaginario (casi sin amortiguamiento). La respuesta al impulso en el panel (d) es la oscilación sinusoidal amortiguada que corresponde a esos dos polos complejos más el decaimiento rápido del polo real.

**Cálculo en Python.**

```python
from scipy.signal import ss2tf
num, den = ss2tf(A, B, C, D)   # G(s) = num(s)/den(s)
poles = np.roots(den)           # = autovalores de A (salvo cancelaciones)
```

## 5 — Cambio de coordenadas: base modal vs física vs normalizada

El espacio de estados no es único: el mismo sistema físico admite infinitas representaciones \( (A,B,C,D) \), una por cada elección de base en \( \mathbb{R}^n \). Comprender qué cambia y qué queda invariante permite elegir la base más conveniente para cada tarea.

**Transformación general.** Si \( \mathbf{z}=T\,\mathbf{x} \) (con \( T \) invertible), las ecuaciones en la nueva base son:

$$ \dot{\mathbf{z}}=\underbrace{TAT^{-1}}_{A_\mathrm{new}}\mathbf{z}+\underbrace{TB}_{B_\mathrm{new}}\mathbf{u}, \qquad \mathbf{y}=\underbrace{CT^{-1}}_{C_\mathrm{new}}\mathbf{z}+D\,\mathbf{u} $$

El cambio de base transforma \( A\mapsto TAT^{-1} \), que es una **semejanza** de matrices. Toda semejanza preserva:
- Los **autovalores** (y por tanto los polos de \( G(s) \)).
- El **rango** de las matrices de controlabilidad y observabilidad.
- La **función de transferencia** \( G(s) \) (se puede verificar sustituyendo).

Lo que sí cambia: las entradas numéricas de \( A_\mathrm{new}, B_\mathrm{new}, C_\mathrm{new} \), y en general el condicionamiento numérico del sistema.

**Base modal (\( T=\Phi^{-1} \)).** Si las columnas de \( \Phi \) son los autovectores derechos de \( A \), entonces \( A_\mathrm{modal}=\Phi^{-1}A\Phi=\Lambda=\mathrm{diag}(\lambda_1,\ldots,\lambda_n) \) es diagonal. En esta base cada estado \( z_i \) evoluciona como \( \dot z_i=\lambda_i z_i \) más entradas acopladas por \( B_\mathrm{modal}=\Phi^{-1}B \). Ventaja: el análisis se simplifica (cada modo separado). Desventaja: los estados modales \( z_i \) son combinaciones complejas de variables físicas, difíciles de implementar en un controlador real. Esta base es para **análisis y comprensión**, no para implementación.

**Base física (\( T=I \)).** Es la representación natural que surge directamente de las ecuaciones de circuito o mecánicas. Los estados son variables medibles o al menos comprensibles (corrientes, tensiones, ángulos). Esta base es la que se **implementa** en el controlador digital.

**Base por unidad (\( T=\mathrm{diag}(S_n, V_n, I_n, \ldots) \)).** En sistemas de potencia se normalizan las variables por valores base (potencia nominal \( S_n \), tensión nominal \( V_n \), corriente \( I_n=S_n/V_n \)). Las nuevas variables son adimensionales y de orden unidad, lo que permite:
- Comparar convertidores de distinta potencia (el LCL de 1 MVA y el de 10 MVA tienen el mismo \( A \) en p.u. si los parámetros son iguales en p.u.).
- Evitar problemas numéricos cuando estados con distintas magnitudes físicas (\( 10^{-3}\,\mathrm{A} \) junto a \( 10^3\,\mathrm{V} \)) hacen que \( A \) esté mal condicionada en unidades SI.

```python
# Cambio a base modal
lam, Phi = np.linalg.eig(A)
T = np.linalg.inv(Phi)          # T = Phi^{-1}
A_modal = T @ A @ np.linalg.inv(T)   # ≈ diag(lam)

# Normalización por unidad: estados x = [iL1, iL2, vC], bases [In, In, Vn]
In, Vn = 100.0, 400.0           # A, V
T_pu = np.diag([In, In, Vn])   # T: SI -> pu
A_pu = T_pu @ A @ np.linalg.inv(T_pu)
```

## 6 — El observador de Luenberger

El realimentador de estado requiere conocer \( \mathbf{x}(t) \). En la práctica no todos los estados son medibles: un filtro LCL tiene tres estados (dos corrientes y la tensión del condensador), pero puede que solo se mida la corriente de red y la tensión de red. El **observador** reconstruye el estado a partir de lo que sí se mide.

**Estructura.** El observador de Luenberger es una copia del sistema original más una corrección proporcional al error de salida:

$$ \boxed{\;\dot{\hat{\mathbf{x}}}=A\,\hat{\mathbf{x}}+B\,\mathbf{u}+L\,(\mathbf{y}-C\,\hat{\mathbf{x}})\;} $$

Aquí \( \hat{\mathbf{x}} \) es el estado estimado y \( L\in\mathbb{R}^{n\times p} \) la **ganancia del observador**. El término \( L(\mathbf{y}-C\hat{\mathbf{x}}) \) corrige la deriva que el modelo solo tendría por incertidumbre de condición inicial o perturbaciones.

**Dinámica del error.** Definiendo el error de estimación \( \tilde{\mathbf{x}}=\mathbf{x}-\hat{\mathbf{x}} \), la ecuación del error es:

$$ \dot{\tilde{\mathbf{x}}}=\dot{\mathbf{x}}-\dot{\hat{\mathbf{x}}}=(A\mathbf{x}+B\mathbf{u})-(A\hat{\mathbf{x}}+B\mathbf{u}+L(C\mathbf{x}-C\hat{\mathbf{x}})) = (A-LC)\,\tilde{\mathbf{x}} $$

El error evoluciona con la dinámica \( (A-LC) \), independientemente de la entrada \( \mathbf{u} \) y del estado real \( \mathbf{x} \). Si se elige \( L \) de modo que todos los autovalores de \( (A-LC) \) tengan parte real suficientemente negativa, el error \( \tilde{\mathbf{x}}(t)\to 0 \) exponencialmente.

**Condición necesaria: observabilidad.** La ganancia \( L \) puede colocar los autovalores de \( (A-LC) \) en posiciones arbitrarias **si y solo si** el par \( (A,C) \) es completamente observable. Si no lo es, existen modos que la salida no "ve" y que \( L \) no puede corregir. La dualidad con el problema de asignación de polos es exacta: colocar los autovalores de \( A-LC \) equivale a colocar los de \( A^\top-C^\top L^\top \), que es un problema de realimentación de estado para el sistema dual.

**Elección de L.** Regla práctica: ubicar los autovalores de \( (A-LC) \) unas 3–10 veces más rápidos (más negativos) que los autovalores del lazo cerrado con realimentación de estado \( (A-BK) \), para que el observador converja antes de que el control necesite el estado. Con la librería `control`:

```python
import control as ct

# Polos deseados del observador (3x más rápidos que el lazo cerrado)
poles_obs = [3*p for p in poles_closed_loop]

# Equivalente a colocar polos del sistema dual
L = ct.place(A.T, C.T, poles_obs).T   # shape (n, p)

# Verificar autovalores del error de observación
print(np.linalg.eigvals(A - L @ C))
```

**Ejemplo: estimar \( i_{L2} \) del LCL desde solo \( v_C \).** El filtro LCL tiene \( C=\begin{bmatrix}0&0&1\end{bmatrix} \) (se mide solo la tensión del condensador). El par \( (A,C) \) es observable (rango \( \mathcal{O}=3 \)). Con \( L \) bien elegida, \( \hat{i}_{L2} \) converge a \( i_{L2} \) en unos milisegundos, permitiendo un control de corriente de red sin sensor de corriente de red. Esto reduce coste y mejora la robustez ante fallos del sensor.

**Separación de principios.** Si se diseña \( K \) para realimentación de estado y \( L \) para el observador de forma independiente, y luego se usa \( \hat{\mathbf{x}} \) en lugar de \( \mathbf{x} \) en la ley de control \( \mathbf{u}=-K\hat{\mathbf{x}} \), los autovalores del lazo cerrado total son la unión de los autovalores de \( (A-BK) \) y los de \( (A-LC) \). Este resultado —el **principio de separación**— permite diseñar el control y el observador por separado.

## 7 — Aplicación al proyecto 01: modelo de 15 estados

El modelo linealizado del inversor GFM del proyecto 01 tiene \( n=15 \) estados. Entender la estructura en bloques de su matriz \( A \) y la correspondencia entre sus autovalores y los modos físicos es el núcleo del análisis de estabilidad.

**Los cuatro bloques de A.** La partición en bloques refleja la física del sistema:

| Bloque | Tamaño | Estados | Descripción |
|--------|--------|---------|-------------|
| LCL dq | 6×6 | \( i_{L1d}, i_{L1q}, i_{L2d}, i_{L2q}, v_{Cd}, v_{Cq} \) | Corrientes y tensión del filtro en coordenadas dq rotantes |
| Control dq | 4×4 | \( \xi_{id}, \xi_{iq}, \xi_{vd}, \xi_{vq} \) | Estados integradores de los lazos de corriente y tensión |
| Droop + ángulo | 3×3 | \( \omega, \delta, P_f \) | Gobernador droop, ángulo del inversor, potencia filtrada |
| Acoplamiento | fuera diagonal | — | Términos que acoplan bloques (aparecen porque dq rota a \( \omega \)) |

Los términos fuera de la diagonal principal de bloques son proporcionales a \( \omega_0 \) (acoplamiento por rotación del marco dq) y a las ganancias del controlador; son los responsables de que los modos no sean simplemente los modos independientes de cada bloque.

**Los tres modos principales y sus autovalores.** En el punto de operación nominal (\( P=0.5\,S_n \), \( \omega=\omega_0 \)):

| Modo | Autovalores típicos | Origen físico |
|------|---------------------|---------------|
| Resonancia LCL | \( -160 \pm j\,8400 \) rad/s | Par complejo del filtro, \( f_\mathrm{res}\approx 1.3\,\mathrm{kHz} \) |
| Lazos de corriente | \( -2500 \pm j\,1800 \) rad/s | Ancho de banda del control de corriente (~400 Hz) |
| Modo de potencia | \( -8 \pm j\,62 \) rad/s | Droop + sincronismo, \( f\approx 10\,\mathrm{Hz} \) |

Los autovalores de potencia son los más lentos y los más sensibles a las condiciones de red (reactancia de red, punto de operación). Los de la resonancia LCL son los más rápidos y dominan la respuesta a altas frecuencias.

**Por qué los autovalores de A son los polos de G(s).** Ya se estableció en el apartado 4: el denominador de \( G(s)=C(sI-A)^{-1}B \) es \( \det(sI-A) \), cuyas raíces son los autovalores de \( A \). En el proyecto 01 esto se verificó numéricamente: los picos del diagrama de Bode de impedancia de salida \( Z_o(j\omega) \) coinciden con las partes imaginarias de los autovalores complejos de \( A \).

**Efecto de los parámetros de control.** Dos parámetros mueven significativamente los autovalores:

- **\( X_\mathrm{virt} \)** (reactancia virtual): aumentarla desplaza los autovalores de resonancia LCL hacia la izquierda (más amortiguamiento). El precio es reducir el ancho de banda efectivo de corriente.
- **\( K_\mathrm{ad} \)** (amortiguamiento activo en el lazo de tensión): actúa sobre los estados del condensador. Aumentarlo mueve el par de resonancia aún más a la izquierda, pero si se excede puede desestabilizar los lazos de corriente (los autovalores del lazo de corriente se acercan al eje imaginario).

Este intercambio se visualiza en el lugar de las raíces paramétrico (barrido de \( K_\mathrm{ad} \)): hay un valor óptimo donde la parte real más positiva del conjunto de autovalores se minimiza (punto de máximo margen de estabilidad).

```python
# Barrido de Kad y cálculo de autovalores
Kad_vec = np.linspace(0, 0.5, 100)
re_max  = []
for Kad in Kad_vec:
    A_k = build_A(Kad=Kad, Xvirt=0.05)   # función del proyecto
    eigs = np.linalg.eigvals(A_k)
    re_max.append(np.max(eigs.real))

# El mínimo de re_max es el Kad óptimo
Kad_opt = Kad_vec[np.argmin(re_max)]
```

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
- Usar la base modal para implementar el controlador (los estados modales no son medibles).
- Olvidar que los polos de \( G(s) \) pueden ser un subconjunto de los autovalores de \( A \) si hay cancelaciones polo-cero (par no mínimo).

## Uso en proyectos
- **01/02**: el modelo linealizado \( (A,B,C,D) \) se usa para polos (estabilidad) e impedancia
  \( G(s)=C(sI-A)^{-1}B+D \). Ver [[respuesta-frecuencia-ss]].

## Conceptos relacionados
- [[variables-estado]] · [[asignacion-polos-lqr]] · [[respuesta-frecuencia-ss]] · [[linealizacion-teoria]]

## Referencias
- Kailath, *Linear Systems*, 1980.
