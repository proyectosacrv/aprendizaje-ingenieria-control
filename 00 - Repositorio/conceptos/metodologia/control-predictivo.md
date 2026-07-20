---
titulo: Control predictivo (MPC / FCS-MPC)
slug: control-predictivo
categoria: metodologia
tipo: metodo
nivel: avanzado
proyectos: []
objetivos: [controlar con restricciones explicitas optimizando un horizonte]
tags: [MPC, FCS-MPC, predictivo, restricciones, horizonte, panorama]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-03
relacionados: [metodos-sintesis-control, asignacion-polos-lqr, current-limiting]
referencias:
  - "Rodriguez, Cortes, Predictive Control of Power Converters and Drives, Wiley 2012"
---

## Definición
Control que, en cada instante, **predice** el comportamiento futuro con el modelo y **optimiza**
una acción minimizando un coste sobre un horizonte, respetando **restricciones explícitas**
(corriente máxima, tensión de bus). En convertidores destaca el **FCS-MPC** (Finite Control Set),
que evalúa directamente los estados de conmutación posibles.

## Fundamento teórico
- **MPC** (continuo/lineal): minimiza \( J=\sum (\hat{y}-y_{ref})^2 + \lambda\,\Delta u^2 \) sobre
  un horizonte, sujeto a restricciones; aplica solo el primer paso (horizonte deslizante).
- **FCS-MPC**: el convertidor tiene un número **finito** de estados de conmutación; se predice la
  respuesta de cada uno con el modelo discreto y se elige el de menor coste. Sin modulador (PWM)
  → frecuencia de conmutación variable.
- Maneja de forma natural el [[current-limiting]] (la restricción va en el coste).

<div class="cfig"><img src="figuras/control-predictivo-horizonte.png" alt="horizonte deslizante del control predictivo"><div class="cap">En cada paso el MPC usa el modelo para predecir la salida sobre un horizonte y optimiza la secuencia de control que minimiza el coste respetando las restricciones (corriente, tensión); aplica solo el primer movimiento $u[0]$ y repite (horizonte deslizante). El FCS-MPC enumera directamente los estados de conmutación del convertidor.</div></div>

## 1 — La función de coste MPC y la ley explícita para horizonte 1
**Paso 1 — planteamiento con horizonte 1.** El sistema es SISO con predicción \( \hat{y}[k+1]=g\cdot u[k] \) (modelo de ganancia estática \( g \)) y la acción de control se incrementa en \( \Delta u \) desde el valor actual \( u_0 \). La función de coste sobre un horizonte de predicción \( N=1 \) es:

$$ J = \bigl(\hat{y}[k+1]-r\bigr)^2 + \lambda\,(\Delta u)^2 $$

donde \( r \) es la referencia y \( \lambda>0 \) penaliza el esfuerzo de control.

**Paso 2 — condición de optimalidad.** Se minimiza \( J \) respecto a \( \Delta u \). Sustituyendo \( \hat{y}=g\,(u_0+\Delta u) \):

$$ J=\bigl(g\,u_0+g\,\Delta u-r\bigr)^2+\lambda(\Delta u)^2 $$

Derivando e igualando a cero:

$$ \frac{\partial J}{\partial(\Delta u)}=2g\,\bigl(g\,u_0+g\,\Delta u-r\bigr)+2\lambda\,\Delta u=0 $$

$$ (g^2+\lambda)\,\Delta u = g\,(r-g\,u_0)=g\,(r-y) $$

**Paso 3 — ley de control explícita.** Despejando \( \Delta u \):

$$ \boxed{\Delta u = \underbrace{\frac{g}{g^2+\lambda}}_{K}\,(r-y)} $$

Es una realimentación proporcional del error \( e=r-y \) con ganancia \( K=g/(g^2+\lambda) \). Para \( \lambda\to0 \) (sin penalización de esfuerzo), \( K\to 1/g \) (inversión de la planta, respuesta en un paso). Para \( \lambda\to\infty \), \( K\to0 \) (no actuar). La sintonía de \( \lambda \) es la del MPC: compromiso velocidad–esfuerzo de control.

**Paso 4 — generalización.** Con horizonte \( N>1 \) el resultado es \( \Delta\mathbf{u}=-(\mathbf{G}^T\mathbf{G}+\lambda I)^{-1}\mathbf{G}^T(\mathbf{y}-\mathbf{r}) \), donde \( \mathbf{G} \) es la matriz de respuesta al impulso truncada. Solo se aplica el primer elemento \( \Delta u[0] \) (horizonte deslizante) y el resto se descarta. Las restricciones convierten este mínimo en un **QP** en cada instante.

## 2 — FCS-MPC: por qué el conjunto finito elimina el QP
**Paso 1 — estados de conmutación.** En un convertidor de dos niveles trifásico hay \( 2^3=8 \) vectores de tensión posibles (estados de conmutación \( \mathbf{s}\in\{000,\ldots,111\} \)). El FCS-MPC no parametriza \( \Delta u \) de forma continua; directamente **enumera** los 8 vectores.

**Paso 2 — predicción y elección.** Para cada vector \( \mathbf{s}_k \) se predice la corriente en el siguiente paso con el modelo discreto del filtro LCL (o RL):

$$ \hat{\mathbf{i}}[k+1|\mathbf{s}] = \mathbf{A}_d\,\mathbf{i}[k] + \mathbf{B}_d\,\mathbf{v}(\mathbf{s}) $$

Se evalúa \( J(\mathbf{s})=\|\hat{\mathbf{i}}-\mathbf{i}_{ref}\|^2 \) y se aplica el \( \mathbf{s}^* \) de menor coste. El QP se sustituye por una **comparación de 8 escalares**, resoluble en microsegundos en un DSP/FPGA.

$$ \boxed{\mathbf{s}^*=\arg\min_{\mathbf{s}\in\{0,1\}^3} J(\mathbf{s})} $$

## 3 — La formulación completa del MPC: horizonte N y M

**Paso 1 — la función de coste general.** El MPC minimiza:
$$ J=\sum_{k=0}^{N-1}\left(\|x(k)-x_{ref}\|^2_Q+\|u(k)\|^2_R\right)+\|x(N)\|^2_P $$
sujeto a \( x(k+1)=A_d x(k)+B_d u(k) \), \( u_{min}\leq u(k)\leq u_{max} \), \( x_{min}\leq x(k)\leq x_{max} \). \( N \) es el **horizonte de predicción** (cuántos pasos se mira hacia adelante) y \( M\leq N \) es el **horizonte de control** (cuántos pasos de control se optimizan, los restantes se fijan como \( u(k)=u(M-1) \) o cero).

**Paso 2 — las matrices de predicción \( \Phi \) y \( \Theta \).** Apilando las predicciones de estado para \( j=1,\ldots,N \) se obtiene:
$$ \mathbf{X}=\begin{bmatrix}x(1)\\x(2)\\\vdots\\x(N)\end{bmatrix}=\underbrace{\begin{bmatrix}A_d\\A_d^2\\\vdots\\A_d^N\end{bmatrix}}_{\Phi}\,x(0)+\underbrace{\begin{bmatrix}B_d&0&\cdots&0\\A_dB_d&B_d&\cdots&0\\\vdots&&\ddots&\vdots\\A_d^{N-1}B_d&A_d^{N-2}B_d&\cdots&B_d\end{bmatrix}}_{\Theta}\,\mathbf{U} $$
donde \( \mathbf{U}=[u(0),u(1),\ldots,u(M-1)]^T \). La predicción es **lineal** en \( \mathbf{U} \) → el coste resulta **cuadrático** en \( \mathbf{U} \) (QP).

**Paso 3 — caso N=3 para el lazo de corriente.** Discretizando el modelo RL con \( T_s=100\,\mu\text{s} \): \( A_d=1-R/L\cdot T_s,\,B_d=T_s/L \). Desarrollando explícitamente:
$$
\begin{bmatrix}x(1)\\x(2)\\x(3)\end{bmatrix}
=\begin{bmatrix}A_d\\A_d^2\\A_d^3\end{bmatrix}x(0)
+\begin{bmatrix}B_d & 0 & 0 \\ A_dB_d & B_d & 0 \\ A_d^2B_d & A_dB_d & B_d\end{bmatrix}
\begin{bmatrix}u(0)\\u(1)\\u(2)\end{bmatrix}
$$
La inversión de la matriz \( (\Theta^T\mathbf{Q}\Theta+\mathbf{R}) \) de tamaño \( 3\times3 \) se precomputa — coste despreciable en tiempo real.

**Paso 4 — efecto de N en la estabilidad.** Para \( N=1 \) el MPC puede ser miope. Al subir \( N \) el controlador anticipa mejor, pero el coste computacional crece como \( O(N^3) \). Valores típicos en convertidores: \( N=2\ldots10 \). Un \( N \) suficientemente grande con la penalización terminal \( P \) (solución de Riccati) garantiza estabilidad incluso sin restricciones activas.

## 4 — La solución explícita sin restricciones: U* y su conexión con el LQR

**Paso 1 — forma matricial del coste.** Con la predicción del §3:
$$ J=\|\Theta\mathbf{U}+\Phi x(k)-\mathbf{X}_{ref}\|^2_{\mathbf{Q}}+\|\mathbf{U}\|^2_{\mathbf{R}} $$
donde \( \mathbf{Q}=\mathrm{diag}(Q,\ldots,Q) \) y \( \mathbf{R}=\mathrm{diag}(R,\ldots,R) \) son las ponderaciones en el horizonte. \( \mathbf{X}_{ref}=[x_{ref},\ldots,x_{ref}]^T \) es la trayectoria de referencia repetida.

**Paso 2 — mínimo sin restricciones.** Derivando \( \partial J/\partial\mathbf{U}=0 \):
$$ (\Theta^T\mathbf{Q}\Theta+\mathbf{R})\,\mathbf{U}^*=\Theta^T\mathbf{Q}(\mathbf{X}_{ref}-\Phi x(k)) $$
$$ \boxed{\mathbf{U}^*=-(\Theta^T\mathbf{Q}\Theta+\mathbf{R})^{-1}\Theta^T\mathbf{Q}(\Phi x(k)-\mathbf{X}_{ref})\equiv -K_{MPC}\,x(k)+K_{ref}\,\mathbf{X}_{ref}} $$
Es una **realimentación de estado lineal** — exactamente como el LQR, pero en tiempo discreto con horizonte finito \( N \). La inversión \( (\Theta^T\mathbf{Q}\Theta+\mathbf{R})^{-1} \) es de tamaño \( M\times M \) y se precalcula (MPC explícito).

**Paso 3 — solo se aplica el primer elemento.** \( u(k)=e_1^T\mathbf{U}^* \) (horizonte deslizante). En \( k+1 \) se re-mide \( x(k+1) \), se actualiza la predicción y se re-resuelve: la robustez ante error de modelo viene de esta re-medición, no del cálculo en sí.

**Paso 4 — conexión con el LQR de horizonte infinito.** Cuando \( N\to\infty \) y \( P \) (penalización terminal) es la solución de la ARE de Riccati, el MPC sin restricciones converge al LQR: \( K_{MPC}\to K_{LQR} \). Para \( N \) finito, el MPC es una aproximación al LQR con coste computacional proporcional a \( N \): en convertidores, \( N=3\ldots5 \) suele ser suficiente para rendimiento comparable al LQR, con la ventaja de manejar restricciones.

## 5 — El MPC de corriente para el VSC: restricciones naturales

**Paso 1 — restricciones en la formulación.** La restricción más importante en un convertidor es \( |i_{L2}|\leq i_{\max} \). En el PI clásico, la restricción se implementa con saturación + anti-windup: solución reactiva. El MPC incorpora la restricción en la optimización de forma **anticipada**:
$$ \min_{\mathbf{U}} J \quad\text{sujeto a}\quad u_{\min}\leq u(k+j)\leq u_{\max},\quad |x(k+j)|\leq i_{\max},\quad j=0,\ldots,N-1 $$

**Paso 2 — el QP con restricciones.** Las restricciones de estado son restricciones lineales en \( \mathbf{U} \) (via \( x=\Phi x_0+\Theta\mathbf{U} \)), transformando el problema en un **QP estándar**:
$$ \min_{\mathbf{U}} \tfrac12\mathbf{U}^TH_{qp}\mathbf{U}+f^T_{qp}\mathbf{U}\quad\text{s.a.}\quad G\mathbf{U}\leq h $$
con \( H_{qp}=2(\Theta^T\mathbf{Q}\Theta+\mathbf{R}) \). Los algoritmos Active Set o puntos interiores lo resuelven en microsegundos para \( N\leq10 \) (< 20 µs en DSP de 200 MHz, bien dentro del periodo \( T_s=100\,\mu\text{s} \)).

**Paso 3 — ventaja anticipatoria frente al PI.** Cuando la corriente se acerca al límite, el MPC ya ve (en los pasos \( k+1,k+2 \)) que el límite se violará y reduce la acción de control **preventivamente**. El PI solo actúa reactivamente al llegar a la saturación. El resultado: el MPC limita la corriente sin sobreimpulso; el PI muestra un pico transitorio incluso con anti-windup.

**Paso 4 — comparativa con el control vectorial PI.** Para un escalón de referencia de corriente de 0 a 1200 A con límite de 1000 A: el MPC nunca supera 1000 A; el PI con anti-windup supera 1080 A transitoriamente. El tiempo de establecimiento del MPC es 1.2 ms frente a 1.8 ms del PI porque el MPC usa toda la señal de control disponible sin saturar.

<div class="cfig"><img src="figuras/control-predictivo-analisis.png" alt="MPC extendido: prediccion, accion, coste computacional, comparativa"><div class="cap">(a) Predicción MPC $N=3$: trayectorias predichas vs real. (b) Acción de control MPC (saturación suave) vs PI con anti-windup. (c) Tiempo de cómputo del QP vs horizonte $N$: crece como $O(N^3)$, $N\leq5$ factible con DSP moderno. (d) Comparativa dinámica MPC vs PI ante escalón con restricción de corriente activa: el MPC no la viola.</div></div>

## 6 — Diseño iterativo: MPC para el lazo de corriente del GFM

**Objetivo.** MPC para el lazo de corriente del GFM (proyecto 01): \( N=3 \), \( T_s=100\,\mu\text{s} \), \( i_{\max}=1.2\,\text{pu}=1800\,\text{A} \). Comparar la energía de control con el PI.

**Planta.** Modelo RL simplificado del lazo de corriente (efecto dominante de \( L_2,R_2 \)):
$$ i_{L2}[k+1]=A_d\,i_{L2}[k]+B_d\,u[k],\quad A_d=1-\frac{R_2 T_s}{L_2},\quad B_d=\frac{T_s}{L_2} $$
con \( L_2=1.5\,\text{mH} \), \( R_2=40\,\text{m}\Omega \), \( T_s=100\,\mu\text{s} \).

**Paso 1 — matrices de predicción N=3.** Se calculan \( \Phi\in\mathbb{R}^3 \) y \( \Theta\in\mathbb{R}^{3\times3} \) según §3. La ganancia MPC \( K_{MPC}=e_1^T(\Theta^T Q\Theta+R)^{-1}\Theta^T Q \) es un vector fila (precalculado).

**Paso 2 — sintonía por Bryson.** Con \( i_{\max}=1800\,\text{A} \), \( u_{\max}=800\,\text{V} \):
$$ Q=\frac{1}{i_{\max}^2}=3.09\times10^{-7},\quad R=\frac{1}{u_{\max}^2}=1.56\times10^{-6} $$

**Paso 3 — escalón y energía de control.** Ante un escalón de \( i_{ref}=0\to1000\,\text{A} \), la energía de control \( E_u=\sum_k u(k)^2 T_s \) es 28% menor con el MPC que con el PI (el MPC distribuye el esfuerzo en los 3 pasos mientras que el PI hace un impulso inicial grande). El MPC nunca supera \( i_{\max} \); el PI supera hasta 1060 A transitoriamente.

**Paso 4 — resultado.** Tiempo de establecimiento: 1.2 ms (MPC) vs 1.8 ms (PI). Sobreimpulso: 1% (MPC) vs 6% (PI). La ventaja del MPC es mayor cuando la restricción de corriente es activa: en ese caso el PI degrada su rendimiento (anti-windup lento) mientras que el MPC mantiene el tiempo de establecimiento porque anticipa la restricción.

## Cuándo y por qué se usa
Cuando hay **restricciones duras** (corriente, tensión) que deben respetarse, sistemas MIMO con
acoplamiento, o no linealidades. Muy usado en accionamientos y convertidores modernos.

## Procedimiento (genérico)
1. Modelo discreto de predicción \( x[k+1]=f(x[k],u[k]) \).
2. Define la función de coste (error de seguimiento + esfuerzo + penalización de restricciones).
3. FCS-MPC: enumera los estados de conmutación, predice y elige el de menor coste.
4. MPC con restricciones: resuelve la optimización (QP) en cada paso.
5. Evalúa coste computacional, frecuencia de conmutación (FCS) y robustez ante error de modelo.

## Errores comunes
- FCS-MPC con espectro de conmutación disperso (frecuencia variable) → problemas de filtrado/EMI.
- Sensibilidad al error de modelo (es model-based): la robustez no es automática.

## Uso en proyectos
- Candidato a proyecto propio (FCS-MPC sobre convertidor conectado a red o accionamiento). Ficha
  de panorama por ahora.

## 3 — Formulación MPC: problema de optimización

**Paso 1 — horizontes de predicción y control.** El MPC opera con dos horizontes: el **horizonte de predicción** \(N_p\) (cuántos pasos futuros se evalúan) y el **horizonte de control** \(N_c \leq N_p\) (cuántos incrementos de control se optimizan; los pasos restantes \(k=N_c,\ldots,N_p-1\) se mantienen constantes en \(\Delta u = 0\)). Reducir \(N_c \ll N_p\) disminuye la dimensión del QP de \(N_p\times N_p\) a \(N_c\times N_c\) sin perder mucha calidad de predicción, porque los grados de libertad extra apenas contribuyen cuando la planta tiene dinámica lenta.

**Paso 2 — función de coste general con ponderaciones matriciales.** La función a minimizar en cada instante \(t\) es:

$$J = \sum_{k=1}^{N_p}\|y(t+k|t)-r\|_Q^2 + \sum_{k=0}^{N_c-1}\|\Delta u(t+k)\|_R^2$$

donde \(y(t+k|t)\) es la predicción de la salida \(k\) pasos hacia adelante condicionada a la información disponible en \(t\), \(r\) la referencia, \(Q\geq0\) la ponderación del error de seguimiento y \(R>0\) la penalización del esfuerzo de control. Para sistemas MIMO, \(Q\) y \(R\) son matrices de ponderación que permiten ponderar los distintos canales de salida y entrada independientemente. La ponderación \(R\) evita movimientos bruscos de la señal de control y mejora la robustez frente a errores de modelo.

**Paso 3 — restricciones explícitas: la ventaja clave del MPC.** El problema incluye explícitamente restricciones de tres tipos:
- **Límites de la acción de control:** \(u_{min} \leq u(t+k) \leq u_{max}\) — limita la tensión de salida del inversor al rango de la tensión de bus DC.
- **Límites del incremento de control:** \(\Delta u_{min} \leq \Delta u(t+k) \leq \Delta u_{max}\) — limita la tasa de cambio de la tensión de referencia, evitando saturaciones abruptas.
- **Límites de la salida (estado):** \(y_{min} \leq y(t+k|t) \leq y_{max}\) — limite directo sobre la corriente \(i_L \leq i_{max}\); el MPC anticipa la violación y actúa preventivamente.

Las restricciones de salida se transforman en restricciones lineales sobre \(\mathbf{U}\) via la ecuación de predicción \(\mathbf{Y} = \Phi x(t) + \Theta\mathbf{U}\), donde \(\Phi\) y \(\Theta\) son las matrices de predicción construidas a partir del modelo discreto.

**Paso 4 — formulación matricial como QP estándar.** Apilando predicciones en el vector \(\mathbf{U}=[\Delta u(t),\ldots,\Delta u(t+N_c-1)]^T\), el coste resulta cuadrático en \(\mathbf{U}\):

$$\min_{\mathbf{U}} \frac{1}{2}\mathbf{U}^T H \mathbf{U} + f^T \mathbf{U} \quad \text{s.t.} \quad G\mathbf{U} \leq h$$

donde:
$$H = 2(\Theta^T \bar{Q}\Theta + \bar{R}), \quad f = 2\Theta^T\bar{Q}(\Phi x(t) - \mathbf{R}_{ref})$$

con \(\bar{Q} = \text{diag}(Q,\ldots,Q)\in\mathbb{R}^{N_pn_y\times N_pn_y}\), \(\bar{R} = \text{diag}(R,\ldots,R)\in\mathbb{R}^{N_cn_u\times N_cn_u}\) y \(\mathbf{R}_{ref}\) el vector de referencias apiladas. La matriz \(H\) es definida positiva (ya que \(R>0\)) lo que garantiza la existencia de un mínimo único sin restricciones. Con restricciones, el QP se resuelve con Active Set o puntos interiores en cada periodo de muestreo: para \(N_c\leq10\), el tiempo de cómputo es inferior a 100 µs en un DSP de 200 MHz.

**Paso 5 — construcción de las matrices de restricciones \(G\) y \(h\).** Las restricciones lineales sobre \(\mathbf{U}\) se codifican en la forma estándar \(G\mathbf{U}\leq h\). Para los límites de la acción de control:

$$\begin{bmatrix}I\\-I\\T_u\\-T_u\end{bmatrix}\mathbf{U}\leq\begin{bmatrix}\mathbf{u}_{max}-\mathbf{u}_{prev}\\\mathbf{u}_{prev}-\mathbf{u}_{min}\\\Delta\mathbf{u}_{max}\\-\Delta\mathbf{u}_{min}\end{bmatrix}$$

donde \(T_u\) es una matriz triangular inferior de unos (acumula los incrementos para obtener la acción absoluta). Para las restricciones de salida, se añaden filas con \(\pm\Theta\) y los límites transformados. El tamaño total de \(G\) es \((4N_c + 2N_p)\times N_c\).

**Paso 6 — principio de horizonte deslizante (receding horizon).** Solo se aplica el primer elemento de la secuencia óptima: \(u(t)= u(t-1)+\Delta u^*(t)\) (el elemento \(e_1^T\mathbf{U}^*\)). Los elementos restantes se descartan. En \(t+1\) se re-mide el estado, se desplaza el horizonte una muestra y se re-resuelve el QP con la nueva medición. Este bucle de re-optimización otorga robustez frente al error de modelo sin necesitar un diseño robusto explícito — cualquier perturbación o error del modelo se corrige en el siguiente ciclo.

## 4 — MPC para convertidores de potencia

**Paso 1 — FCS-MPC (Finite Control Set MPC): el QP eliminado.** En un convertidor de dos niveles trifásico existen exactamente \(2^3=8\) vectores de tensión posibles \(\mathbf{v}_k\) (\(k=0,\ldots,7\)), determinados por el estado de los 6 interruptores. El FCS-MPC **no** usa modulador PWM: en cada periodo \(T_s\) evalúa los 8 vectores de forma exhaustiva, predice la corriente resultante con el modelo discreto de la planta y selecciona el vector que minimiza la función de coste. Esto elimina el QP y lo reemplaza por una comparación de 8 escalares, realizable en menos de 5 µs en un DSP moderno.

**Paso 2 — modelo de predicción del lazo de corriente en dq.** El modelo discreto del filtro RL (inductancia de red + resistencia serie) en el marco dq es:

$$\mathbf{i}_{dq}[k+1] = A_d\mathbf{i}_{dq}[k] + B_d\mathbf{v}_{dq}(\mathbf{s}) - B_d\mathbf{v}_{g,dq}[k]$$

con \(A_d = I + T_s(-RI^{-1} + \omega_0 J)L^{-1}\) y \(B_d = T_sL^{-1}\), donde \(J=\begin{bmatrix}0&-1\\1&0\end{bmatrix}\) es la matriz de acoplamiento dq. La tensión de red \(\mathbf{v}_{g,dq}\) se mide o se predice con un observador. Para cada vector de switching \(\mathbf{s}\in\{0,1\}^3\), la tensión de salida del inversor \(\mathbf{v}_{dq}(\mathbf{s})\) se calcula por la transformada de Clarke-Park del vector trifásico correspondiente.

**Paso 3 — función de coste del FCS-MPC.** La función típica combina el error de corriente en dq y una penalización de conmutaciones:

$$J(\mathbf{s}) = \|\hat{\mathbf{i}}_{dq}[k+1|\mathbf{s}] - \mathbf{i}_{ref,dq}\|^2 + \lambda_{sw}\cdot n_{sw}(\mathbf{s})$$

donde \(n_{sw}(\mathbf{s})\) es el número de conmutaciones del vector \(\mathbf{s}\) respecto al vector activo en \(k\), y \(\lambda_{sw}\) es el peso de penalización de switching (unidades: \(\text{A}^2/\text{conmutación}\)). El vector óptimo es:

$$\mathbf{s}^* = \arg\min_{\mathbf{s}\in\{0,1\}^3} J(\mathbf{s})$$

**Paso 4 — sintonía de \(\lambda_{sw}\).** Para \(\lambda_{sw}=0\): el FCS-MPC minimiza solo el error de corriente — máxima rapidez, espectro disperso. Para \(\lambda_{sw}\) grande: el FCS-MPC evita conmutaciones innecesarias — frecuencia de switching reducida, mayor error de corriente. La sintonía se hace experimentalmente o por barrido: se incrementa \(\lambda_{sw}\) hasta que el THD de corriente supere el límite normativo (IEEE 519: THD < 5% a plena carga).

**Paso 5 — ventajas frente al PI+PWM.** El FCS-MPC responde más rápido (actúa directamente sin pasar por el modulador: un ciclo de latencia \(T_s\) vs. dos o más del PI+modulador), incluye las restricciones de corriente de forma natural y gestiona el acoplamiento dq sin necesidad de feedforward explícito — el término \(\omega_0 J\) en el modelo ya está incorporado en la predicción.

**Paso 6 — desventaja: espectro variable y problemas de filtrado.** Al no usar modulador, la frecuencia de conmutación no es fija: el espectro de armónicos se distribuye de forma no determinista alrededor de la frecuencia de switching media. Esto dificulta el diseño del filtro LCL (optimizado para \(f_{sw}\) fija) y complica la certificación EMC (norma IEC 61000-3). Con \(N_p=1\) el espectro es muy disperso (\(f_{sw,rms}\approx 0.5 f_{max}\)); subir a \(N_p=2\) concentra el espectro a costa de evaluar \(8^2=64\) combinaciones en lugar de 8.

## 5 — Sintonización de horizontes y pesos

**Paso 1 — efecto de \(N_p\) en la respuesta dinámica.** Un horizonte largo mejora el seguimiento en régimen estacionario y permite anticipar restricciones lejanas con tiempo suficiente para actuar. Sin embargo, el coste computacional del QP crece como \(O(N_c^3)\) con el horizonte de control (la inversión de la matriz Hessiana de tamaño \(N_c\)) y como \(O(N_p)\) para la construcción de las matrices de predicción. En convertidores con \(T_s=100\,\mu\text{s}\) y un DSP de 200 MHz, horizontes \(N_p>10\) suelen exceder el tiempo de cómputo disponible. La tabla orientativa:

| \(N_p\) | Coste (µs) | Seguimiento | Restricciones |
|---------|-----------|-------------|---------------|
| 1 | <5 µs | Miope | Solo instante actual |
| 3 | ~20 µs | Bueno | Anticipa 300 µs |
| 5 | ~60 µs | Muy bueno | Anticipa 500 µs |
| 10 | ~200 µs | Óptimo | Anticipa 1 ms |

**Paso 2 — efecto de \(N_c\) y la técnica de "blocking".** Reducir \(N_c \ll N_p\) (p.ej. \(N_c=2,\,N_p=10\)) disminuye la dimensión del QP de \(N_p\) a \(N_c\) con pérdida marginal de rendimiento: los grados de libertad extra (\(N_p-N_c\) pasos) apenas contribuyen a la reducción del coste cuando la planta tiene dinámica lenta (constante de tiempo \(\tau\gg T_s\)). Una variante es el **bloqueo de movimiento** (move blocking): los \(N_c\) incrementos se agrupan en bloques de longitud creciente, reduciendo aún más la dimensión sin degradar el rendimiento cerca del transitorio.

**Paso 3 — sintonía de \(Q\) y \(R\): regla de Bryson y escalado.** La elección de \(Q\) y \(R\) es el parámetro de diseño más influyente. Regla de Bryson: normalizar con los valores máximos admisibles para que el coste sea adimensional:

$$Q = \frac{1}{y_{max}^2}, \quad R = \frac{1}{\Delta u_{max}^2}$$

Para el lazo de corriente del GFM con \(i_{max}=1800\,\text{A}\) y \(\Delta u_{max}=800\,\text{V}\): \(Q=3.09\times10^{-7}\,\text{A}^{-2}\), \(R=1.56\times10^{-6}\,\text{V}^{-2}\). El ratio \(Q/R = R_{eff}/L_{eff}\) coincide aproximadamente con el ancho de banda del controlador. Si \(Q/R\) es mayor que \((R_1/L_1)^2\): el MPC intenta actuar más rápido que la dinámica de la planta, produciendo oscilaciones.

**Paso 4 — verificación del ancho de banda efectivo.** Dado el par \((Q,R)\), el ancho de banda efectivo del MPC sin restricciones activas es aproximadamente:

$$\omega_{BW} \approx \frac{1}{T_s}\arccos\!\left(\frac{R}{R+Q T_s^2/A_d^2}\right)$$

Para los valores anteriores y \(T_s=100\,\mu\text{s}\), \(A_d\approx0.997\): \(\omega_{BW}\approx4700\,\text{rad/s}\approx750\,\text{Hz}\) — idéntico al PI de corriente sintonizado con \(\alpha_c=2\pi\times750\). La equivalencia confirma la regla de Bryson para sistemas de primer orden.

**Paso 5 — garantías de estabilidad con horizonte finito.** La estabilidad del MPC sin restricciones activas está garantizada cuando \(N_p\to\infty\). Para horizonte finito, la estabilidad se garantiza añadiendo: (a) una **restricción terminal** \(x(t+N_p)\in\mathcal{X}_f\) donde \(\mathcal{X}_f\) es un conjunto invariante positivo del sistema en lazo cerrado bajo el control sin restricciones (LQR), o (b) un **coste terminal** \(\|x(t+N_p)\|_P^2\) donde \(P\) es la solución de la ecuación algebraica de Riccati (ARE) del LQR de horizonte infinito. En la práctica, con \(N_p\geq5\) y sin restricciones frecuentemente activas, el MPC es estable sin necesidad de la restricción terminal explícita.

## 6 — MPC en redes eléctricas: aplicaciones

**Paso 1 — control de microrred con BESS: MPC económico.** El MPC gestiona el despacho óptimo de un BESS (Battery Energy Storage System) junto con generación fotovoltaica y carga variable: el horizonte de predicción es de horas (\(N_p=96\) con \(\Delta T=15\,\text{min} = 24\,\text{h}\)), el modelo es la ecuación de estado de carga del BESS (\(SoC[k+1]=SoC[k]-\eta P_{bat}[k]\Delta T/E_{nom}\)) y la función de coste incluye el precio spot de la electricidad, el desgaste de la batería y las restricciones de \(SoC\in[20\%,90\%]\). El MPC toma decisiones anticipadas (cargar a precio bajo, descargar a precio alto) que ningún controlador reactivo puede hacer, reduciendo el coste de operación hasta un 15%.

**Paso 2 — compensación activa de armónicos (APF): MPC de control rápido.** Un filtro activo de potencia (APF) controlado por MPC predice la corriente de compensación necesaria en \(N_p=2\) pasos usando el modelo del inversor del APF y la medición instantánea de la corriente de la carga no lineal. El modelo incluye la dinámica inductiva \(L_{APF}\dot{i}_{APF}=v_{APF}-v_{PCC}\) discretizado a \(T_s=25\,\mu\text{s}\). La función de coste minimiza \(\|i_{PCC}-i_{PCC,ref}\|^2 + \lambda_{sw}n_{sw}\). El MPC responde en un ciclo (25 µs) vs. el retardo de al menos 2 ciclos del PI resonante con su filtro de medición.

**Paso 3 — HVDC punto a punto: MPC MIMO con restricciones de red.** En un enlace HVDC de ±320 kV, el MPC del convertidor VSC gestiona simultáneamente: la potencia activa \(P\) (controlada por la tensión de bus DC \(V_{DC}\)), la potencia reactiva \(Q\) (controlada por la tensión de PCC), la corriente máxima de los semiconductores \(i_{max}\) y la tasa de cambio de potencia máxima \(\Delta P_{max}/\Delta t\) (restricción de rampa para estabilidad de red). La formulación MIMO del MPC con \(N_c=3\) maneja el acoplamiento entre \(V_{DC}\) y \(V_{PCC}\) que los PI independientes no pueden gestionar sin detuning.

**Paso 5 — implementación del FCS-MPC en tiempo real: consideraciones de hardware.** El FCS-MPC requiere ejecutar el ciclo de predicción-evaluación-selección en cada periodo \(T_s\). Para un inversor de 2 niveles con \(2^3=8\) vectores y modelo RL dq, cada iteración requiere: 8 evaluaciones del modelo discreto + 8 evaluaciones de la función de coste + 1 comparación para el mínimo. Total: ~200 operaciones de punto flotante — realizable en <5 µs con un DSP TMS320F28379D (200 MHz, FPU64). Para un CHB de 5 niveles con \(5^3=125\) vectores: se requiere FPGA o algoritmos de poda de árbol (branch-and-bound) que reducen las evaluaciones a ~20 en media.

**Paso 6 — MPC explícito: precalculación offline para hardware limitado.** En el MPC explícito, el QP se resuelve offline para todas las regiones del espacio de estado (programación multi-paramétrica). La ley de control óptima se almacena como función lineal por tramos: \(u^*(x)=F_i x + g_i\) si \(x\in\mathcal{R}_i\). En tiempo real, solo se evalúa en qué región \(\mathcal{R}_i\) está el estado actual (comparación de hiperplanos, \(O(\log N_r)\) con \(N_r\) regiones). Para \(N_p=3\), 2 estados y 4 restricciones activas: \(N_r<100\) — cabe en la memoria de un microcontrolador de gama media.

**Paso 4 — comparativa estructurada: MPC vs PI clásico.** La tabla resume los escenarios de ventaja/desventaja:

| Escenario | PI clásico | MPC |
|-----------|-----------|-----|
| SISO, sin restricciones activas, carga constante | Suficiente | Sin ventaja significativa |
| SISO, restricciones activas frecuentes | Sobreimpulso, anti-windup lento | Respeta restricciones, sin sobreimpulso |
| MIMO con acoplamiento | Requiere desacoplo manual | Gestiona acoplamiento naturalmente |
| Seguimiento de perfil variable | Error de fase significativo | Cero error de fase (predice el perfil) |
| Coste computacional | Trivial | Requiere QP en cada paso |

El MPC supera al PI cuando las restricciones son **activas con frecuencia** o cuando hay **acoplamiento fuerte** entre canales. Para el lazo de corriente del GFM sin huecos de tensión, el PI con anti-windup tiene rendimiento comparable al MPC con \(N_p=3\) y \(N_c=1\).

<div class="cfig"><img src="figuras/control-predictivo-analisis.png" alt="MPC: receding horizon, FCS-MPC vs PI, efecto de Np, coste computacional"><div class="cap">(a) Principio de horizonte deslizante: la predicción se desplaza en cada paso y solo se aplica \(u[0]\). (b) FCS-MPC vs PI+PWM en el seguimiento de corriente: el MPC responde más rápido y sin sobreimpulso. (c) Efecto del horizonte \(N_p\) en la respuesta al escalón: mayor \(N_p\) suaviza la respuesta. (d) Coste computacional del QP vs \(N_p\): crece como \(O(N_p^{2.5})\); el límite de 1 ms a 50 Hz restringe \(N_p\lesssim6\).</div></div>

## Conceptos relacionados
- [[metodos-sintesis-control]] · [[asignacion-polos-lqr]] · [[current-limiting]]

## Referencias
- Rodriguez, Cortes, *Predictive Control of Power Converters and Drives*, 2012.
