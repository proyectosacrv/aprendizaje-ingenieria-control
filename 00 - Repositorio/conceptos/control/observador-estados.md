---
titulo: Observador de estados (Luenberger)
slug: observador-estados
categoria: control
tipo: metodo
nivel: intermedio
proyectos: []
objetivos: [estimar estados no medidos a partir de entradas y salidas]
tags: [observador, luenberger, estimador, separacion, espacio-estados, kalman, orden-reducido, intermedio, control]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-03
relacionados: [controlabilidad-observabilidad, asignacion-polos-lqr, representacion-espacio-estados, variables-estado]
referencias:
  - "Ogata, Ingeniería de Control Moderna, Pearson"
  - "Franklin, Powell, Feedback Control of Dynamic Systems, Pearson"
  - "Anderson, Moore, Optimal Filtering, Dover 2005"
---

## Definición
Sistema dinámico que **reconstruye el vector de estado** \( \hat{\mathbf{x}} \) de una planta a
partir de su entrada \( \mathbf{u} \) y su salida medida \( \mathbf{y} \), cuando no todos los
estados se miden. Permite cerrar realimentación de estado usando estimaciones en lugar de medidas
directas. La versión óptima ante ruido es el filtro de Kalman.

## Fundamento teórico
Para \( \dot{\mathbf{x}}=A\mathbf{x}+B\mathbf{u} \), \( \mathbf{y}=C\mathbf{x} \), el observador
copia la planta y corrige con el error de salida:
$$ \dot{\hat{\mathbf{x}}}=A\hat{\mathbf{x}}+B\mathbf{u}+L\,(\mathbf{y}-C\hat{\mathbf{x}}) $$
El error \( \mathbf{e}=\mathbf{x}-\hat{\mathbf{x}} \) evoluciona como
$$ \dot{\mathbf{e}}=(A-LC)\,\mathbf{e} $$
así que **converge a cero** si \( A-LC \) es estable. Los autovalores de \( A-LC \) se sitúan
libremente mediante \( L \) **si y solo si el par \( (A,C) \) es observable**. El **principio de
separación** garantiza que diseñar control (\( K \)) y observador (\( L \)) por separado conserva
los polos de ambos en el lazo combinado.

<div class="cfig"><img src="figuras/observador-estados-convergencia.png" alt="estado estimado convergiendo y error decayendo"><div class="cap">Izquierda: el observador arranca con $\hat x\neq x$ y su estimación del estado no medido $x_2$ alcanza a la real. Derecha: la norma del error $\|x-\hat x\|$ cae varios órdenes de magnitud porque los polos de $A-LC$ son estables y más rápidos que la planta.</div></div>

## 1 — De dónde sale \( \dot{\mathbf{e}}=(A-LC)\mathbf{e} \) y la colocación de \( L \)
**Paso 1 — definir el error.** El error de estimación es \( \mathbf{e}=\mathbf{x}-\hat{\mathbf{x}} \). Derivando, \( \dot{\mathbf{e}}=\dot{\mathbf{x}}-\dot{\hat{\mathbf{x}}} \).

**Paso 2 — restar las dos dinámicas.** La planta da \( \dot{\mathbf{x}}=A\mathbf{x}+B\mathbf{u} \); el observador, \( \dot{\hat{\mathbf{x}}}=A\hat{\mathbf{x}}+B\mathbf{u}+L(\mathbf{y}-C\hat{\mathbf{x}}) \). Restando, el término \( B\mathbf{u} \) (idéntico en ambos) se cancela:

$$ \dot{\mathbf{e}}=A\mathbf{x}-A\hat{\mathbf{x}}-L(\mathbf{y}-C\hat{\mathbf{x}})=A(\mathbf{x}-\hat{\mathbf{x}})-L(\mathbf{y}-C\hat{\mathbf{x}}) $$

**Paso 3 — sustituir la salida.** Como \( \mathbf{y}=C\mathbf{x} \), el término corrector es \( L(C\mathbf{x}-C\hat{\mathbf{x}})=LC(\mathbf{x}-\hat{\mathbf{x}})=LC\,\mathbf{e} \). Sustituyendo y sacando factor \( \mathbf{e} \):

$$ \dot{\mathbf{e}}=A\mathbf{e}-LC\,\mathbf{e}=(A-LC)\,\mathbf{e} $$

**Paso 4 — convergencia.** Es una ecuación lineal homogénea: \( \mathbf{e}(t)=e^{(A-LC)t}\mathbf{e}(0) \). El error tiende a cero si y solo si:

$$ \boxed{\;\text{todos los autovalores de }(A-LC)\text{ tienen }\mathrm{Re}<0\;} $$

La dinámica del error **no depende de \( \mathbf{u} \)**: por eso el observador funciona con cualquier entrada.

**Paso 5 — colocación de \( L \) por dualidad.** Los autovalores de \( A-LC \) coinciden con los de \( (A-LC)^\top=A^\top-C^\top L^\top \). Esto tiene la forma exacta de una realimentación de estado \( A_d-B_d K_d \) con \( A_d=A^\top \), \( B_d=C^\top \), \( K_d=L^\top \). Por tanto, colocar los polos del observador equivale a un problema de asignación de polos sobre el par \( (A^\top,C^\top) \), que tiene solución libre **si y solo si \( (A,C) \) es observable** (ver [[controlabilidad-observabilidad]]). En código: `L = place(A.T, C.T, polos).T`. Se eligen los polos 2–5× más rápidos que los de control para que el error decaiga antes de afectar al lazo.

## 2 — El observador de Luenberger: dinámica, convergencia y elección de velocidad

**El mecanismo de corrección.** El término \( L(\mathbf{y}-C\hat{\mathbf{x}}) \) es el motor del observador: \( \mathbf{y}-C\hat{\mathbf{x}} \) es la **innovación** (la diferencia entre lo que la salida mide y lo que el observador predice). La ganancia \( L \) pondera cuánto se corrige el estado estimado por cada unidad de innovación. Sin \( L=0 \): el observador es una copia abierta de la planta y el error converge con los polos de \( A \) (que pueden ser lentos o inestables). Con \( L\neq0 \): los polos de la dinámica del error se mueven a \( \mathrm{eig}(A-LC) \), que se colocan a elección.

**La regla empírica: polos del observador 3–5× más rápidos.** Sea \( \lambda_i(A-BK) \) los polos del lazo de control (realimentación de estado) que se quieren imponer. Los polos del observador se suelen elegir:

$$ \lambda_i^{obs} = (3\text{–}5)\cdot\lambda_i^{ctrl} $$

El factor 3–5 asegura que el error de estimación decae mucho más rápido que la dinámica del lazo, de modo que el principio de separación es válido en la práctica (no solo en teoría). Si los polos son demasiado rápidos: el observador amplifica el ruido de medida (porque responde agresivamente a cada innovación). Si son demasiado lentos: el error de estimación persiste durante los transitorios del lazo y degrada la respuesta.

**Dónde colocar los polos: criterios prácticos.**
1. Más rápidos que el doble del ancho de banda del lazo de control.
2. No más de 5–10× el ancho de banda del lazo (compromiso ruido/velocidad).
3. Evitar polos complejos con amortiguamiento bajo (ζ < 0,5): el observador oscilaría antes de converger.
4. En discreto: mantener los polos dentro del círculo unitario y lejos de \( z=-1 \).

**Ejemplo numérico.** Sistema LCL con resonancia en \( f_{res}=2\,\text{kHz} \), lazo de control con ancho de banda \( \alpha_c=2\pi\cdot750\,\text{rad/s} \). Los polos del control están en \( s\approx-4712\,\text{rad/s} \). Los polos del observador se eligen en \( s\approx-3\cdot f_{res}\cdot2\pi\approx-37700\,\text{rad/s} \) (factores 8× más rápidos). La constante de tiempo del error es \( \tau_{obs}=1/37700\approx26\,\mu\text{s} \): el error decae en \( 5\tau_{obs}=130\,\mu\text{s} \), mucho antes del período fundamental de 20 ms.

## 3 — El observador de orden reducido

Cuando algunos estados se miden directamente, el observador no necesita estimarlos: su valor exacto ya es conocido. El **observador de orden reducido** estima solo los \( n-p \) estados no medidos (donde \( p \) es el número de salidas medidas), reduciendo el coste computacional.

**Partición del sistema.** Si \( C=[I_p\ 0] \) (los primeros \( p \) estados se miden directamente), se particiona el vector de estado en \( \mathbf{x}=[\mathbf{y}^\top,\ \mathbf{z}^\top]^\top \) donde \( \mathbf{y}\in\mathbb{R}^p \) es medido y \( \mathbf{z}\in\mathbb{R}^{n-p} \) no lo es. La dinámica es:

$$ \dot{\mathbf{y}} = A_{11}\mathbf{y} + A_{12}\mathbf{z} + B_1\mathbf{u} $$
$$ \dot{\mathbf{z}} = A_{21}\mathbf{y} + A_{22}\mathbf{z} + B_2\mathbf{u} $$

El observador de orden reducido estima solo \( \mathbf{z} \). Como \( \mathbf{y} \) es conocido, la primera ecuación se puede usar directamente para calcular \( \dot{\mathbf{y}} \), lo que genera información adicional. Reescribiendo la segunda ecuación:

$$ \dot{\mathbf{z}} = A_{22}\mathbf{z} + \underbrace{A_{21}\mathbf{y} + B_2\mathbf{u}}_{\text{término conocido}} $$

El observador de orden reducido para \( \mathbf{z} \) es:

$$ \dot{\hat{\mathbf{z}}} = A_{22}\hat{\mathbf{z}} + A_{21}\mathbf{y} + B_2\mathbf{u} + L_r(\dot{\mathbf{y}} - A_{11}\mathbf{y} - A_{12}\hat{\mathbf{z}} - B_1\mathbf{u}) $$

donde \( L_r \in\mathbb{R}^{(n-p)\times p} \) es la ganancia del observador reducido, y el término de corrección usa la diferencia entre \( \dot{\mathbf{y}} \) medido y la predicción del modelo.

**Problema práctico: \( \dot{\mathbf{y}} \) implica derivación numérica.** Derivar una señal medida amplifica el ruido. La solución habitual es un cambio de variable: \( \mathbf{w}=\hat{\mathbf{z}}-L_r\mathbf{y} \), que transforma el observador en una ecuación diferencial sin derivadas de las salidas medidas.

**Ventaja del orden reducido.** Para el LCL con 3 estados y medida de \( i_{L2} \) (1 salida), el observador de orden completo tiene 3 estados; el reducido tendría 2 estados (estima \( i_{L1} \) y \( v_C \)). Esto reduce el coste computacional y la necesidad de condiciones iniciales para los estados estimados.

## 4 — El filtro de Kalman: el observador óptimo con ruido

El filtro de Kalman es el observador de Luenberger óptimo cuando hay ruido de proceso y de medida. Su ganancia \( K_K \) minimiza la covarianza del error de estimación en régimen permanente.

**El modelo con ruido.** La planta real tiene perturbaciones no modeladas (\( \mathbf{w} \), ruido de proceso) y el sensor tiene ruido (\( \mathbf{v} \), ruido de medida):

$$ \dot{\mathbf{x}} = A\mathbf{x} + B\mathbf{u} + \mathbf{w},\quad \mathbf{w}\sim\mathcal{N}(0,Q_{noise}) $$
$$ \mathbf{y} = C\mathbf{x} + \mathbf{v},\quad \mathbf{v}\sim\mathcal{N}(0,R_{noise}) $$

donde \( Q_{noise}\ge0 \) es la matriz de covarianza del ruido de proceso y \( R_{noise}>0 \) es la del ruido de medida (ambas simétricas).

**La ecuación de Riccati.** La ganancia óptima \( K_K \) se calcula a partir de la solución \( P \) de la **ecuación algebráica de Riccati continua (CARE)**:

$$ A\,P + P\,A^\top - P\,C^\top\,R_{noise}^{-1}\,C\,P + Q_{noise} = 0 $$

donde \( P \) es la covarianza del error de estimación en régimen permanente (\( P=E[\mathbf{e}\mathbf{e}^\top] \)). La ganancia óptima de Kalman es:

$$ \boxed{\;K_K = P\,C^\top\,R_{noise}^{-1}\;} $$

Esta ganancia equilibra dos efectos opuestos: si \( R_{noise} \) es grande (sensor ruidoso), \( K_K \) es pequeño (confío poco en la medida, el observador sigue más el modelo). Si \( Q_{noise} \) es grande (modelo incierto), \( K_K \) es grande (confío más en la medida). El filtro de Kalman encuentra el equilibrio óptimo.

**Kalman vs Luenberger: cuándo usar cada uno.**
- **Luenberger:** modelo bien conocido, ruido bajo, diseño intuitivo por colocación de polos. Adecuado para el amortiguamiento activo del LCL en laboratorio.
- **Kalman:** ruido de medida significativo, modelo con incertidumbre paramétrica, se quiere minimizar el error RMS. Adecuado para estimación de parámetros en tiempo real o aplicaciones con sensores ruidosos.

**Dualidad LQR-Kalman.** El filtro de Kalman es el problema dual del regulador cuadrático lineal (LQR): si el LQR minimiza \( \int(x^\top Q x + u^\top R u)dt \), el filtro de Kalman minimiza la covarianza del error con matrices \( Q_{noise} \) y \( R_{noise} \). Ambos se resuelven con la misma ecuación de Riccati. Esta dualidad es la base del **regulador LQG** (LQR + Kalman): el controlador óptimo ante ruido.

<div class="cfig"><img src="figuras/observador-estados-analisis.png" alt="cuatro paneles: error de estimacion para distintas velocidades, estimacion vs real, Kalman vs Luenberger con ruido, observador de orden reducido LCL"><div class="cap">(a) Error de estimación e(t) para polos del observador 3× y 10× más rápidos que la planta. (b) Estimación x̂(t) vs estado real durante un transitorio. (c) Kalman vs Luenberger en presencia de ruido de medida. (d) Observador de orden reducido para el LCL: estimar iL2 desde vC.</div></div>

## 5 — Observador en convertidores de potencia

**Estimación sensorless de la tensión de red.** En aplicaciones donde no hay sensor de tensión de red, \( v_g \) puede estimarse como estado aumentado del modelo del convertidor. Se añade \( v_g \) al vector de estado con dinámica modelada como \( \dot{v}_g = 0 \) (disturbio constante o cuasi-estático). El observador estima simultáneamente los estados del filtro y \( v_g \) desde la corriente medida.

**MRAC (Model Reference Adaptive Control).** Si los parámetros de la planta (inductancias, resistencias) varían lentamente, el observador acumulará un sesgo que no converge a cero. El MRAC actualiza en tiempo real los parámetros del modelo del observador comparando la salida estimada con la medida. La ley de adaptación tiene la forma:

$$ \dot{\hat\theta} = -\Gamma\,\mathbf{e}_{obs}\,\phi $$

donde \( \hat\theta \) son los parámetros estimados, \( \Gamma \) es una matriz de ganancia de adaptación positiva definida y \( \phi \) es el vector de regresión (señales medidas).

**Observador de corriente armónica.** Para implementar control repetitivo o de armónicos específicos, el observador puede incluir estados adicionales que representen los coeficientes de los armónicos del error de corriente. Un estado aumentado con el modelo de los armónicos 3°, 5°, 7° permite al observador estimar y el controlador compensar esos componentes periódicos sin necesidad de un FFT explícito.

**Velocidad del observador.** La regla empírica es:

$$ \omega_{obs} = (3\text{–}5)\,\omega_{control} $$

En convertidores de potencia con lazo de corriente en \( \omega_{ci} = 2\pi \cdot 750\,\text{rad/s} \), los polos del observador se colocan en \( \omega_{obs} \approx 2\pi \cdot 2250\text{–}3750\,\text{rad/s} \). La constante de tiempo del error de estimación resultante es \( \tau_{obs} = 1/\omega_{obs} \approx 40\text{–}70\,\mu\text{s} \): converge en menos de 5 períodos de muestreo (con \( T_s = 100\,\mu\text{s} \)).

## 6 — Implementación práctica

**Sesgo por discrepancia modelo-planta.** En el observador de Luenberger, si la planta real difiere del modelo (\( A \neq A_{modelo} \), \( B \neq B_{modelo} \)), el error de estimación \( \mathbf{e} = \mathbf{x} - \hat{\mathbf{x}} \) no converge a cero sino a un valor de sesgo proporcional al error de modelado. La ecuación del error modificada es:

$$ \dot{\mathbf{e}} = (A-LC)\,\mathbf{e} + (A-A_{modelo})\,\mathbf{x} + (B-B_{modelo})\,\mathbf{u} $$

El término de fuerza \( (A-A_{modelo})\mathbf{x} + (B-B_{modelo})\mathbf{u} \) actúa como una perturbación persistente que genera sesgo en \( \hat{\mathbf{x}} \).

**Solución: estado aumentado con disturbio.** Se extiende el vector de estado con un término de perturbación \( d \) que agrupa los errores de modelado:

$$ \begin{bmatrix}\dot{\mathbf{x}} \\ \dot{d}\end{bmatrix} = \begin{bmatrix}A & B_d \\ 0 & 0\end{bmatrix}\begin{bmatrix}\mathbf{x} \\ d\end{bmatrix} + \begin{bmatrix}B \\ 0\end{bmatrix}\mathbf{u} $$

El observador aumentado estima simultáneamente \( \mathbf{x} \) y \( d \), eliminando el sesgo. La ganancia de observador aumentado \( L_{aug} \) se diseña para el sistema aumentado, que tiene un polo adicional en \( s=0 \) (integrador del disturbio).

**Ruido de cuantificación del ADC.** Un ADC de \( b \) bits con rango \( [\text{-}V_{max}, V_{max}] \) introduce ruido de cuantificación de varianza \( \sigma_q^2 = \Delta^2/12 \) con \( \Delta = 2V_{max}/2^b \). Para un ADC de 12 bits y rango ±1000 A: \( \Delta \approx 0{,}49\,\text{A} \), \( \sigma_q \approx 0{,}14\,\text{A} \). Esto es el ruido de medida \( R_{noise} \) de entrada al filtro de Kalman. Elegir \( R_{noise} = \sigma_q^2 \) garantiza que el Kalman pese óptimamente el modelo frente a la medida ruidosa.

**Verificación en puesta en marcha.** Durante la puesta en marcha del convertidor, antes de cerrar el lazo de control:
1. Alimentar el observador con \( u_{real} \) y \( y_{real} \) durante 5–10 ms (tiempo de convergencia del observador).
2. Comparar \( \hat{\mathbf{x}} \) con una medida directa de los estados no medidos (si está disponible temporalmente).
3. Verificar que el error de estimación es menor que el 5% del rango nominal.
4. Solo entonces cerrar el lazo con \( \mathbf{u} = -K\hat{\mathbf{x}} \).

<div class="cfig"><img src="../figuras/observador-estados-analisis.png" alt="cuatro paneles: ganancia Kalman vs Q/R, Kalman 1D sobre señal ruidosa, Luenberger vs Kalman error, observador con disturbio"><div class="cap">(a) Ganancia de Kalman en función de la relación Q/R. (b) Filtro de Kalman 1D: tracking de señal ruidosa. (c) Comparación del error de estimación Luenberger vs Kalman. (d) Observador con disturbio estimado: estado real, estimado y disturbio.</div></div>

## 5 — Resumen: observador completo vs reducido vs Kalman

| Tipo | Orden | Diseño | Cuándo usar |
|---|---|---|---|
| Luenberger completo | \( n \) | Colocación de polos (dualidad) | Todos los estados no medidos, modelo preciso |
| Luenberger reducido | \( n-p \) | Colocación de polos reducido | \( p \) estados ya medidos, ahorro computacional |
| Filtro de Kalman | \( n \) | CARE + covarianzas \( Q,R \) | Ruido significativo, modelo incierto |
| Filtro de Kalman extendido (EKF) | \( n \) | Linealización local + CARE | Sistema no lineal, ej. estimación de ángulo de rotor |

## 6 — Diseño iterativo: observador para estimar iL2 del LCL midiendo solo vC

**El escenario.** En el filtro LCL, la variable más relevante para el control de corriente es \( i_{L2} \) (corriente de red). Si no hay sensor de corriente de red disponible, pero sí hay sensor de tensión en el condensador (\( v_C \)), se puede diseñar un observador para estimar \( i_{L2} \).

**Verificación de observabilidad.** Con \( C_{obs}=[0,1,0] \) (medida \( v_C \)), la matriz de observabilidad del LCL:

$$ \mathcal{O} = \begin{bmatrix}C_{obs}\\ C_{obs}A\\ C_{obs}A^2\end{bmatrix} = \begin{bmatrix}0&1&0\\ 1/C_f & 0 & -1/C_f \\ -R_1/(L_1 C_f) & -(1/L_1+1/L_2)/C_f & R_2/(L_2 C_f)\end{bmatrix} $$

Con valores reales (\( R_1, R_2 > 0 \)): \( \mathrm{rank}(\mathcal{O})=3 \) → **observable desde \( v_C \)**.

**Elección de los polos del observador.** Resonancia del LCL: \( f_{res}\approx2\,\text{kHz} \). Polos del observador en \( s=-3\cdot2\pi\cdot f_{res}\approx-37\,700\,\text{rad/s} \) (3 polos reales iguales para minimizar el sobreimpulso de estimación).

**Cálculo de L.** `L = ct.place(A.T, C_obs.T, [-3.77e4, -3.77e4, -3.77e4]).T`

**Comportamiento en simulación.** Con \( L \) calculado y polos en \( -37\,700\,\text{rad/s} \):
- Error de estimación de \( i_{L2} \): decae a cero en \( \approx5/37700\approx133\,\mu\text{s} \).
- La estimación sigue \( i_{L2} \) durante los transitorios del lazo de control (período de control: 100 µs → el observador converge en ≈1,3 períodos de control).
- El observador estima también \( i_{L1} \): permite implementar el amortiguamiento activo con realimentación de \( v_C \) estimado sin sensor adicional.

**Kalman para el mismo sistema.** Si el sensor de \( v_C \) tiene ruido (\( \sigma_v=0{,}1\,\text{V} \)):
- \( R_{noise}=\sigma_v^2=0{,}01\,\text{V}^2 \).
- \( Q_{noise}=\mathrm{diag}(0{,}1, 0{,}01, 0{,}01) \) (incertidumbre paramétrica en las inductancias).
- La CARE da \( K_K \) que balancea modelo y medida → error de estimación RMS ≈50% menor que el Luenberger con los mismos polos.

## Cuándo y por qué se usa
Cuando faltan sensores (estimar flujo, tensión de condensador, par de carga), para filtrar ruido,
o en control "sensorless". Imprescindible junto a realimentación de estado/LQR cuando el estado no
es accesible.

## Procedimiento de diseño (genérico)
1. Verifica observabilidad de \( (A,C) \) (ver [[controlabilidad-observabilidad]]).
2. Si algunos estados son medidos directamente: considera el observador de orden reducido.
3. Elige los polos del observador **3–5× más rápidos** que los de control (compromiso velocidad/ruido).
4. Calcula \( L \) por asignación de polos (dual) o resuelve Kalman si hay modelo de ruido.
5. Implementa el observador en discreto y comprueba convergencia y rechazo de ruido.
6. Cierra el lazo con \( \mathbf{u}=-K\hat{\mathbf{x}} \) (principio de separación).

## Ejemplo de aplicación real
**Problema:** Filtro LCL con estados \( [i_{L1},\,v_C,\,i_{L2}] \). Solo se mide \( i_{L2} \). Diseñar un observador de Luenberger que estime \( v_C \) e \( i_{L1} \) para implementar amortiguamiento activo sin sensor en el condensador.

El par \( (A,C) \) con \( C=[0,0,1] \) es observable. Se colocan los polos del observador a \( 3\times\omega_{res,LCL}\approx38\,700\,\text{rad/s} \). \( L \) se calcula con `ct.place(A.T, C.T, obs_poles).T`. El \( v_C \) estimado se usa en el lazo de amortiguamiento activo: el pico de resonancia del filtro a 2 kHz cae >20 dB respecto al caso sin observador.

## Ejemplo de código
```python
import control as ct, numpy as np, scipy.linalg

# Luenberger
obs_poles = [-3.77e4, -3.77e4*1.01, -3.77e4*1.02]  # 3 polos casi iguales
L = ct.place(A.T, C.T, obs_poles).T

# Kalman
Q_n = np.diag([0.1, 0.01, 0.01])   # ruido de proceso
R_n = np.array([[0.01]])             # ruido de medida
P = scipy.linalg.solve_continuous_are(A.T, C.T, Q_n, R_n)
K_kalman = P @ C.T @ np.linalg.inv(R_n)

# Simulacion del observador (Euler explícito, dt=Ts)
xh = np.zeros(3)
for k in range(N):
    y_meas = C @ x_real[k]
    innov  = y_meas - C @ xh
    xh     = xh + Ts * (A @ xh + B * u[k] + L @ innov)
    x_hat[k] = xh.copy()
```

## Parámetros y valores típicos
Polos del observador 3–5× los del control. Compromiso: rápido → converge antes pero
amplifica ruido de medida; lento → suave pero arrastra error durante transitorios.

## Errores comunes
- Observador más lento que la planta → estimación retrasada, lazo degradado.
- Polos demasiado rápidos → ruido de medida amplificado en \( \hat{\mathbf{x}} \).
- Diseñar con \( (A,C) \) no observable (o casi) → \( L \) no estabiliza ciertos modos.
- Modelo \( A,B,C \) mal identificado → sesgo permanente en la estimación.
- En el LCL: verificar observabilidad con las resistencias parásitas reales, no con \( R=0 \).

## Conceptos relacionados
- [[controlabilidad-observabilidad]] · [[asignacion-polos-lqr]] · [[representacion-espacio-estados]] · [[variables-estado]]

## Referencias
- Ogata, *Ingeniería de Control Moderna*.
- Franklin, Powell, *Feedback Control of Dynamic Systems*.
- Anderson, Moore, *Optimal Filtering*, Dover 2005.
