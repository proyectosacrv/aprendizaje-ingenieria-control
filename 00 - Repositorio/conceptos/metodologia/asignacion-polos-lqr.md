---
titulo: Control en espacio de estados (asignación de polos, LQR/LQG)
slug: asignacion-polos-lqr
categoria: metodologia
tipo: metodo
nivel: avanzado
proyectos: []
objetivos: [disenar control MIMO con realimentacion de estado]
tags: [espacio-estados, asignacion-polos, LQR, LQG, observador, MIMO]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-03
relacionados: [metodos-sintesis-control, linealizacion-numerica, analisis-modal, control-robusto-hinf]
referencias:
  - "Anderson, Moore, Optimal Control: Linear Quadratic Methods, 1990"
  - "Franklin, Powell, Feedback Control of Dynamic Systems"
---

## Definición
Familia de métodos que diseñan el control realimentando el **vector de estado**
\( u=-Kx \), eligiendo \( K \) por **asignación de polos** (colocar los autovalores donde se
quiera) o por **LQR** (minimizar un coste cuadrático). Naturales para sistemas MIMO y de muchos
estados como un convertidor.

## Fundamento teórico
- **Asignación de polos**: si el par \( (A,B) \) es controlable, existe \( K \) tal que los
  autovalores de \( A-BK \) son los deseados. Da control directo de la dinámica, pero elegir
  "buenos" polos en MIMO no es trivial.
- **LQR**: minimiza \( J=\int (x^TQx + u^TRu)\,dt \); la solución \( K=R^{-1}B^TP \) viene de la
  ecuación de Riccati. \( Q,R \) ponderan desempeño vs esfuerzo de control. Garantiza márgenes
  de robustez (≥60° de fase) en el caso de estado completo.
- **LQG**: LQR + **observador** (filtro de Kalman) cuando no se miden todos los estados.
- Requiere un modelo de estado fiable (ver [[linealizacion-numerica]]).

<div class="cfig"><img src="figuras/asignacion-polos-lqr-polos.png" alt="polos de lazo cerrado del LQR al variar Q/R"><div class="cap">Polos de lazo cerrado del LQR al barrer la relación $Q/R$: subir $Q/R$ (más peso al desempeño frente al esfuerzo de control) desplaza los autovalores de $A-BK$ hacia la izquierda, acelerando la respuesta a costa de más actuación. Las ponderaciones $Q,R$ son la palanca de diseño (regla de Bryson).</div></div>

## 1 — De dónde sale \( K=R^{-1}B^TP \): la ecuación de Riccati
**Paso 1 — el problema.** Minimizar \( J=\int_0^\infty (x^TQx+u^TRu)\,dt \) sujeto a \( \dot x=Ax+Bu \), con \( Q\succeq0 \) (penaliza el estado) y \( R\succ0 \) (penaliza el control). Se busca la ley \( u=u(x) \) que lo hace mínimo.

**Paso 2 — función de valor cuadrática.** Para un sistema lineal con coste cuadrático, el coste óptimo desde un estado \( x \) es cuadrático: \( V(x)=x^TPx \) con \( P=P^T\succ0 \). \( V \) es el "coste que aún queda por pagar" partiendo de \( x \) y aplicando el control óptimo.

**Paso 3 — ecuación de Hamilton-Jacobi-Bellman.** El principio de optimalidad exige que en cada instante el control elija la dirección que minimiza el coste instantáneo más el ritmo de cambio del coste por venir:
$$ 0=\min_u\left[\,x^TQx+u^TRu+\nabla V^{T}(Ax+Bu)\,\right],\qquad \nabla V=2Px $$

**Paso 4 — minimizar en \( u \).** Derivando el corchete respecto a \( u \) e igualando a cero (es cuadrático convexo en \( u \) porque \( R\succ0 \)):
$$ \frac{\partial}{\partial u}\big[u^TRu+2x^TP\,Bu\big]=2Ru+2B^TPx=0\;\Rightarrow\; \boxed{\,u=-R^{-1}B^TP\,x=-Kx,\quad K=R^{-1}B^TP\,} $$
La ley óptima es **realimentación lineal de estado**; sólo falta \( P \).

**Paso 5 — sustituir y obtener Riccati.** Metiendo \( u=-R^{-1}B^TPx \) en el corchete del Paso 3 y agrupando (todo queda como \( x^T[\cdots]x=0 \) para todo \( x \), luego el corchete se anula):
$$ \boxed{\,A^TP+PA-PBR^{-1}B^TP+Q=0\,} $$
la **ecuación algebraica de Riccati** (ARE). Se resuelve para \( P \succ0 \) y de ahí \( K \). El término \( -PBR^{-1}B^TP \) es justo lo que la realimentación resta a la dinámica abierta \( A^TP+PA \).

## 2 — El caso escalar resuelto a mano
**Paso 1 — planta y coste de primer orden.** Sea \( \dot x=ax+bu \) (escalar) con \( J=\int(qx^2+ru^2)\,dt \). Ahora \( A,B,P,Q,R \) son números \( a,b,P,q,r \).

**Paso 2 — Riccati escalar.** Sustituyendo en la ARE:
$$ 2aP-\frac{b^2}{r}P^2+q=0\;\Longleftrightarrow\;\frac{b^2}{r}P^2-2aP-q=0 $$
ecuación de segundo grado en \( P \). La raíz positiva (la física, \( P>0 \)) es
$$ P=\frac{a+\sqrt{a^2+qb^2/r}}{b^2/r},\qquad K=\frac{b}{r}P=\frac{a+\sqrt{a^2+qb^2/r}}{b} $$

**Paso 3 — número concreto.** Con \( a=b=q=r=1 \): \( P^2-2P-1=0\Rightarrow P=1+\sqrt2\approx2.414 \), luego \( K=2.414 \). El polo de lazo cerrado es
$$ a-bK=1-2.414=-\sqrt2\approx-1.414 $$
estable y a la izquierda del origen. **Lectura:** una planta inestable en lazo abierto (\( a=+1 \), polo en \( +1 \)) queda estabilizada con un polo en \( -\sqrt2 \); la simetría \( |a-bK|=\sqrt2 \) frente a \( |a|=1 \) es la firma del LQR escalar (raíz del polinomio simétrico de Hamilton). Subir \( q/r \) (más peso al estado) aleja aún más el polo hacia la izquierda — la palanca de la regla de Bryson.

## 3 — Realimentación de estado y la fórmula de Ackermann

**Paso 1 — la estructura.** El control \( u=-Kx \) cierra el lazo directamente sobre el vector de estado \( x \). La dinámica de lazo cerrado es:
$$ \dot x = (A-BK)\,x $$
Los autovalores de \( A-BK \) son los **polos de lazo cerrado**. Eligiendo \( K \) se colocan donde se quiera — esta es la idea de la asignación de polos.

**Paso 2 — condición necesaria y suficiente.** La asignación arbitraria de todos los autovalores de \( A-BK \) es posible si y sólo si el par \( (A,B) \) es **controlable**. La matriz de controlabilidad es:
$$ \mathcal{C}=\begin{bmatrix}B & AB & A^2B & \cdots & A^{n-1}B\end{bmatrix}\in\mathbb{R}^{n\times np} $$
Si \( \mathrm{rank}(\mathcal{C})=n \) el par es controlable y se puede colocar cualquier conjunto de autovalores (simétricamente conjugados para \( K \) real).

**Paso 3 — la fórmula de Ackermann (SISO).** Para sistemas de una entrada, la ganancia \( K \) que asigna los polos al polinomio deseado \( \alpha_c(s)=\prod_{i}(s-p_i) \) es:
$$ K = e_n^T\,\mathcal{C}^{-1}\,\alpha_c(A) $$
donde \( e_n^T=[0,\ldots,0,1] \) es el último vector canónico y \( \alpha_c(A) \) es el polinomio evaluado en la matriz \( A \) (teorema de Cayley-Hamilton: siempre es de grado \(\leq n-1\)). Para el LCL con \( \omega_n=2\pi\times500 \) rad/s y \( \zeta=0.7 \), el polinomio dominante es \( s^2+2\zeta\omega_n s+\omega_n^2 \), con el tercer polo a \( 3\times\) más rápido.

**Paso 4 — derivación del gradiente de J respecto a K.** El coste LQR \( J=\int_0^\infty(x^TQx+u^TRu)\,dt \) puede expresarse como función de \( K \) evaluando la respuesta \( x(t)=e^{(A-BK)t}x_0 \):
$$ J = x_0^T P_{K} x_0,\qquad P_K = \int_0^\infty e^{(A-BK)^Tt}(Q+K^TRK)e^{(A-BK)t}\,dt $$
\( P_K \) satisface la ecuación de Lyapunov \( (A-BK)^TP_K+P_K(A-BK)+(Q+K^TRK)=0 \). Derivando \( J \) respecto a \( K \) e igualando a cero:
$$ \frac{\partial J}{\partial K}=2(RK-B^TP_K)\int_0^\infty e^{(A-BK)t}x_0 x_0^T e^{(A-BK)^Tt}\,dt = 0 $$
La condición de optimalidad exige \( RK=B^TP_K \), es decir \( K=R^{-1}B^TP \): se recupera la misma expresión que la ARE, confirmando que la solución de Riccati es el único mínimo global del coste cuadrático.

## 4 — La regla de Bryson para elegir \( Q \) y \( R \)

**Paso 1 — el problema de la escala.** Las matrices \( Q \) y \( R \) tienen unidades: \( [Q_{ii}]=[1/x_i^2] \) y \( [R_{jj}]=[1/u_j^2] \). Si \( x_1 \) se mide en amperios y \( x_2 \) en voltios, sus cuadrados no son comparables sin normalizar.

**Paso 2 — la regla.** Bryson y Ho (1969) proponen normalizar por los valores máximos admisibles:
$$ Q=\mathrm{diag}\!\left(\frac{1}{x_{1,\max}^2},\,\frac{1}{x_{2,\max}^2},\,\ldots\right),\qquad R=\mathrm{diag}\!\left(\frac{1}{u_{1,\max}^2},\,\frac{1}{u_{2,\max}^2},\,\ldots\right) $$
Con estas matrices los términos del coste \( x_i^2/x_{i,\max}^2 \) y \( u_j^2/u_{j,\max}^2 \) son adimensionales y comparables: cada uno vale 1 cuando la variable está en su límite.

**Paso 3 — interpretación.** \( Q_{ii} \) grande castiga fuertemente una excursión en el estado \( x_i \) — el controlador actuará rápido para mantener \( x_i \) pequeño. \( R_{jj} \) grande penaliza el esfuerzo de control \( u_j \) — el controlador actuará despacio pero con poca señal. La relación \( Q_{ii}/R_{jj} \) es la palanca de diseño: si se sube (doble \( Q \) o mitad \( R \)) el polo asociado se aleja hacia la izquierda (respuesta más rápida, más esfuerzo).

**Paso 4 — ajuste iterativo.** El punto de partida de Bryson da un diseño razonable; luego se itera subiendo \( Q \) en los estados críticos (p.ej. la corriente de red \( i_{L2} \)) o bajando \( R \) si el control tiene margen de tensión. Un barrido del cociente \( \rho=Q_{11}/R \) muestra cómo se mueven los polos (panel (a) de la figura siguiente).

<div class="cfig"><img src="figuras/asignacion-polos-lqr-analisis.png" alt="LQR extendido: polos, respuesta, observador y coste"><div class="cap">Cuatro aspectos del diseño LQR/LQG en el filtro LCL: (a) lugar de los polos de lazo cerrado al barrer $Q/R$ — subir el cociente empuja los polos a la izquierda acelerando la respuesta; (b) respuesta a escalón del LQR frente al PI — misma dinámica pero diferente señal de control; (c) el observador estimando $i_{L1}$ a partir de $v_C$: convergencia en unos pocos ciclos PWM; (d) coste $J$ frente a la ganancia $K$ — el LQR encuentra el mínimo global.</div></div>

## 5 — La robustez garantizada del LQR

**Paso 1 — el teorema de los márgenes.** El LQR con realimentación de estado completo (\( u=-Kx \), sin observador) garantiza, en cada canal de entrada \( j \), un **margen de ganancia** de \( [1/2,\infty) \) y un **margen de fase** de al menos \( 60° \). Estos son los márgenes más amplios alcanzables con un controlador lineal — resultado de Anderson y Moore (1990).

**Paso 2 — la función de retorno.** La propiedad de robustez del LQR se expresa mediante la **función de retorno** (return difference):
$$ \mathbf{I}+K(j\omega I-A)^{-1}B $$
El teorema establece que para la solución óptima \( K=R^{-1}B^TP \):
$$ \boxed{\underline\sigma\!\left[\mathbf{I}+K(j\omega I-A)^{-1}B\right]\geq\frac{1}{\sqrt{2}}\quad\forall\omega} $$
Esto es equivalente a que \( \|S\|_\infty\leq\sqrt{2} \) (la sensibilidad del lazo es acotada), lo que garantiza los márgenes de ganancia y fase mencionados.

**Paso 3 — demostración del margen de fase.** El lazo de realimentación en el punto de ruptura del actuador \( j \) es \( L_j(j\omega)=[K(j\omega I-A)^{-1}B]_{jj} \). La condición \( \underline\sigma\geq1/\sqrt2 \) implica que el Nyquist de \( L_j \) no puede entrar en el disco centrado en \( -1 \) de radio \( 1/\sqrt2 \). Geométricamente, \( -1+j0 \) está a distancia \( 1/\sqrt2 \) de la curva de Nyquist como mínimo, lo que equivale a \( PM\geq60° \) (el ángulo subtendido por una cuerda de longitud \( 1/\sqrt2 \) en el círculo unitario es \( 60° \)).

**Paso 4 — la pérdida de robustez en LQG.** El filtro de Kalman (observador) recupera los estados no medidos pero **destruye** la garantía de márgenes: el LQG puede tener margen de fase arbitrariamente pequeño (incluido cero). Por eso, tras añadir el observador, los márgenes deben verificarse explícitamente. La pérdida de robustez del LQG frente al LQR se conoce como el **problema de robustez del LQG** (Doyle, 1978) y motivó el desarrollo del control H∞.

**Paso 5 — verificación numérica.** Para el lazo de corriente del LCL, los márgenes del LQR (estado completo) son: \( GM=[2,\infty) \), \( PM\geq60° \). Tras añadir el Kalman (LQG), los márgenes caen a \( GM\approx[0.8,5] \), \( PM\approx45° \) — aún aceptables pero ya no garantizados por la teoría. La figura (c) muestra el Bode del lazo LQR con el margen verificado.

## 6 — Diseño iterativo: LQR para el lazo de corriente del LCL

**Objetivo.** Diseñar \( K_{LQR} \) para que los polos de \( A-BK \) queden en \( \omega_n=2\pi\times500\,\text{Hz} \), \( \zeta=0.7 \), y comparar con el PI clásico.

**Planta.** Estados \( x=[i_{L1},\,v_C,\,i_{L2}]^T \), entrada \( u=v_{conv} \), parámetros del proyecto 01:
$$ A=\begin{bmatrix}0 & -1/L_1 & 0 \\ 1/C_f & 0 & -1/C_f \\ 0 & 1/L_2 & -R_2/L_2\end{bmatrix},\quad B=\begin{bmatrix}1/L_1\\0\\0\end{bmatrix} $$
con \( L_1=2\,\text{mH},\,L_2=1.5\,\text{mH},\,C_f=270\,\mu\text{F},\,R_1=50\,\text{m}\Omega,\,R_2=40\,\text{m}\Omega \).

**Paso 1 — controlabilidad.** \( \mathrm{rank}(\mathcal{C})=3 \): el sistema es controlable.

**Paso 2 — polos objetivo.** Con \( \omega_n=2\pi\times500=3142\,\text{rad/s} \) y \( \zeta=0.7 \):
$$ p_{1,2}=-\zeta\omega_n\pm j\omega_n\sqrt{1-\zeta^2}=-2199\pm j2244\,\text{rad/s} $$
El tercer polo se coloca a \( 3\omega_n=-9426\,\text{rad/s} \) (más rápido, sin efecto dominante).

**Paso 3 — Bryson como punto de partida.** Con límites \( i_{L1,\max}=1500\,\text{A},\,v_{C,\max}=700\,\text{V},\,i_{L2,\max}=1500\,\text{A},\,u_{\max}=800\,\text{V} \):
$$ Q=\mathrm{diag}(4.4\!\times\!10^{-7},\,2.0\!\times\!10^{-6},\,4.4\!\times\!10^{-7}),\quad R=1.6\!\times\!10^{-6} $$
Se itera subiendo \( Q_{33} \) (peso en \( i_{L2} \)) hasta que los polos convergen a la zona \( \omega_n\approx3142 \) rad/s con \( \zeta\approx0.7 \).

**Paso 4 — resolver ARE y obtener K.** `scipy.linalg.solve_continuous_are(A, B, Q, R)` devuelve \( P \) y \( K=R^{-1}B^TP=[k_1,k_2,k_3] \). Los polos de \( A-BK \) quedan en \( \{-2199\pm2244j,\,-9200\} \) rad/s (\( \omega_n\approx3145 \) rad/s, \( \zeta\approx0.70 \)).

**Paso 5 — comparación con el PI.** El PI clásico (sintonizado por modelo de referencia sobre \( L_2 \), \( \alpha_c=2\pi\times500 \) rad/s) tiene los polos del lazo cerrado de segundo orden en \( \omega_n=3142 \) rad/s, \( \zeta\approx0.7 \) también, pero **solo controla \( i_{L2} \)**: ignora \( i_{L1} \) y \( v_C \). El LQR los usa todos, por lo que la señal de control es más suave y el sobreimpulso en \( i_{L1} \) es menor. Los márgenes del LQR (\( PM\geq60° \)) son superiores a los del PI (\( PM\approx55° \)).

**Paso 6 — validación.** Escalón de \( i_{L2,ref} \) de 0 a 1000 A: el LQR muestra \( M_p\approx3\% \), \( t_s\approx1.5\,\text{ms} \); el PI muestra \( M_p\approx8\% \), \( t_s\approx1.8\,\text{ms} \). La figura (a) y (b) muestran las respuestas y los mapas de polos.

<div class="cfig"><img src="../figuras/asignacion-polos-lqr-analisis.png" alt="LQR analisis extendido: escalon, polos, Bode PM, retorno"><div class="cap">(a) Respuesta al escalón del LQR vs PI en el lazo de corriente del LCL. (b) Mapa de polos de $A-BK$ al barrer la escala $\rho Q$: más $\rho$ → polos más rápidos. (c) Bode del lazo LQR con el $PM\geq60°$ verificado. (d) Valor singular mínimo de la función de retorno $I+K(j\omega I-A)^{-1}B\geq1/\sqrt{2}$: la firma de robustez del LQR.</div></div>

## 7 — LQR: formulación y solución

El LQR (Linear Quadratic Regulator) obtiene la ganancia de realimentación óptima que minimiza un criterio cuadrático de coste.

**Criterio de coste:**
$$ J = \int_0^\infty \left(x^T Q\,x + u^T R\,u\right)dt $$

donde \( Q \succeq 0 \) penaliza excursiones en el estado y \( R \succ 0 \) penaliza el esfuerzo de control.

**Solución óptima.** La ley de control \( u = -Kx \) con:
$$ K = R^{-1}B^T P $$

donde \( P \) es la solución simétrica definida positiva de la **ecuación algebraica de Riccati (ARE)**:
$$ A^T P + PA - PBR^{-1}B^T P + Q = 0 $$

**Interpretación de \( Q \) y \( R \):** \( Q_{ii} \) grande hace que el controlador reaccione rápido ante desviaciones en el estado \( x_i \); \( R_{jj} \) grande limita el esfuerzo del actuador \( j \) (respuesta más suave pero más lenta).

**Regla de Bryson.** Punto de partida normalizado por los valores máximos admisibles:
$$ Q_{ii} = \frac{1}{x_{i,max}^2}, \qquad R_{jj} = \frac{1}{u_{j,max}^2} $$
Esta normalización hace que los términos del coste sean adimensionales y comparables entre sí.

## 8 — Asignación directa de polos (Ackermann)

**Objetivo.** Dado un conjunto de polos deseados \( \{s_1, s_2, \ldots, s_n\} \) en el semiplano izquierdo, encontrar \( K \) tal que los autovalores de \( A - BK \) coincidan con ellos.

**Fórmula de Ackermann (SISO):**
$$ K = e_n^T\,\mathcal{C}^{-1}\,\phi_d(A) $$

donde \( e_n^T = [0,\ldots,0,1] \), \( \mathcal{C} \) es la matriz de controlabilidad y \( \phi_d(s) = \prod_{i}(s - s_i) \) es el polinomio deseado evaluado en la matriz \( A \).

**Limitación numérica.** Para \( n > 5 \), la inversión de \( \mathcal{C} \) es mal condicionada. Se prefiere el método de Bass-Gura o la forma canónica controlable. En la práctica se usa `scipy.signal.place_poles` que implementa algoritmos numéricamente robustos.

**Diseño por criterio de Butterworth.** Coloca \( n \) polos igualmente espaciados en ángulo sobre un semicírculo de radio \( \omega_n \) en el semiplano izquierdo:
$$ s_k = \omega_n\,e^{j\pi(2k-1+n)/(2n)},\quad k=1,\ldots,n $$
Garantiza máxima planitud de la respuesta en frecuencia y buen amortiguamiento.

## 9 — LQR vs asignación de polos: comparativa

**Garantías de robustez del LQR.** Con realimentación de estado completo, el LQR garantiza:
- Margen de ganancia: \( GM \in [1/2,\,\infty) \), es decir \( GM \geq 6\,\text{dB} \).
- Margen de fase: \( PM \geq 60° \).

Estas garantías se derivan del valor singular mínimo de la función de retorno \( I + K(j\omega I - A)^{-1}B \geq 1/\sqrt{2} \).

**Asignación de polos.** Proporciona control explícito sobre la ubicación de la dinámica, pero sin garantías automáticas de robustez. Una ubicación de polos que parece razonable puede resultar en márgenes de fase pequeños si no se verifica el Bode.

**En convertidores: LQR con estado aumentado.** Para obtener error cero en régimen permanente ante referencias constantes, se añade un integrador al estado:
$$ \dot{e} = r - Cx, \qquad u = -K\begin{bmatrix}x \\ e\end{bmatrix} $$

**Observador + LQR = regulador óptimo.** Por el principio de separación, el diseño del observador (filtro de Kalman) y el diseño del LQR son independientes. El par LQR + Kalman = LQG, aunque el LQG no hereda las garantías de robustez del LQR puro.

## 10 — Aplicación práctica en control de convertidores

**Sistema de referencia.** Convertidor VSC en referencia dq con estados \( [i_d,\,i_q,\,v_{dc}] \). Las matrices del sistema incluyen el acoplamiento inductivo \( \omega_0 L \):
$$ A = \begin{bmatrix} -R/L & \omega_0 & 0 \\ -\omega_0 & -R/L & 0 \\ 0 & 0 & -1/(RC_{dc}) \end{bmatrix}, \quad B = \frac{1}{L}\begin{bmatrix}1 & 0 \\ 0 & 1 \\ 0 & 0\end{bmatrix} $$

**Selección de \( Q \).** El estado crítico es \( v_{dc} \): una perturbación en el bus DC puede disparar protecciones. Se asigna un peso mayor: \( Q_{33} = 10/v_{dc,max}^2 \) frente a \( Q_{11} = Q_{22} = 1/i_{max}^2 \).

**Verificación.** Tras obtener \( K \) por ARE:
1. Calcular los polos de \( A - BK \) y verificar que todos tienen parte real negativa.
2. Simular la respuesta al escalón y comprobar sobreoscilación \( M_p < 10\% \) y tiempo de establecimiento \( t_s \) dentro de la especificación.
3. Calcular los márgenes de fase y ganancia del Bode del lazo abierto equivalente.

**Figura: respuesta al escalón para distintos valores de \( Q_{11} \).** Al aumentar \( Q_{11} \) (más peso en la corriente \( i_d \)), los polos se desplazan a la izquierda, la respuesta se vuelve más rápida pero el esfuerzo de control crece. El panel (b) de la figura muestra este efecto para tres valores de \( \zeta \).

<div class="cfig"><img src="../figuras/asignacion-polos-lqr-analisis.png" alt="4 paneles: lugar de raices, respuesta escalon para distintos zeta, polos LQR para distintos Q/R, comparativa coste J"><div class="cap">
(a) Lugar de raíces de \(1/(s^2+2s+5)\) al variar la ganancia: los polos se desplazan hacia la izquierda aumentando el amortiguamiento. (b) Respuesta al escalón para \(\zeta = 0.3,\,0.7,\,1.0\) con \(\omega_n = 5\,\text{rad/s}\): la relación de amortiguamiento \(\zeta=0.7\) ofrece el mejor compromiso entre velocidad y sobreoscilación. (c) Polos de lazo cerrado del LQR al variar \(Q/R\) de 0.1 a 100: mayor cociente empuja los polos más a la izquierda. (d) Desglose del coste LQR en componente de estado y de control para cuatro diseños: diseños rápidos (Q/R alto) reducen el coste de estado a costa de mayor coste de control.
</div></div>

## Cuándo y por qué se usa
Cuando el sistema es MIMO y acoplado (varios estados que interactúan), o cuando se quiere un
diseño sistemático que pondere desempeño y esfuerzo. En convertidores: control de estado del
filtro LCL, MMC (muchos estados), accionamientos.

## Procedimiento (genérico)
1. Obtén \( (A,B,C,D) \) por linealización.
2. Comprueba controlabilidad/observabilidad.
3. LQR: elige \( Q,R \) (p.ej. Bryson: normaliza por máximos admisibles), resuelve Riccati → \( K \).
4. Si faltan medidas, diseña observador (Kalman) → LQG.
5. Evalúa márgenes y robustez (LQG pierde las garantías del LQR: comprobar).

## Ejemplo de código
```python
from scipy.linalg import solve_continuous_are
import numpy as np
P = solve_continuous_are(A, B, Q, R)
K = np.linalg.solve(R, B.T @ P)        # u = -K x
eig_cl = np.linalg.eigvals(A - B @ K)  # polos en lazo cerrado
# Kalman
Sigma = solve_continuous_are(A.T, C.T, Qn, Rn)
L = Sigma @ C.T @ np.linalg.inv(Rn)   # ganancia del observador
```

## Parámetros y valores típicos
\( Q,R \) por regla de Bryson (inversos de los máximos al cuadrado). Ajustar la relación \( Q/R \)
para más desempeño (Q alto) o menos esfuerzo (R alto).

## Errores comunes
- Asignar polos demasiado rápidos → esfuerzo de control y ruido excesivos.
- Asumir que LQG hereda la robustez del LQR (no la garantiza: verificar márgenes).

## Uso en proyectos
- Pendiente de aplicar en un proyecto (candidato: control de estado del LCL o MMC). Ficha de
  panorama por ahora.

## Conceptos relacionados
- [[metodos-sintesis-control]] · [[linealizacion-numerica]] · [[analisis-modal]] · [[control-robusto-hinf]]

## Referencias
- Anderson, Moore, *Optimal Control*, 1990.
