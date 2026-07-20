---
titulo: Clasificación de la estabilidad del sistema de potencia
slug: clasificacion-estabilidad
categoria: metodologia
tipo: concepto
nivel: intermedio
proyectos: []
objetivos: [ubicar cada fenómeno de estabilidad en un marco común y elegir la herramienta]
tags: [estabilidad, clasificacion, converter-driven, frecuencia, tension, angulo, intermedio]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-03
relacionados: [fenomenos-oscilatorios-red, ecuacion-oscilacion, interaccion-pll-red-debil, grid-forming-vs-following]
referencias:
  - "Hatziargyriou et al., Definition and Classification of Power System Stability Revisited & Extended, IEEE TPWRS 2021"
  - "Kundur, Power System Stability and Control, McGraw-Hill 1994"
---

## Definición
Marco taxonómico (IEEE/CIGRE 2021) que organiza **todos** los fenómenos de estabilidad de un
sistema eléctrico según la variable física afectada, la magnitud de la perturbación y la escala de
tiempo. Permite ubicar cada concepto del repositorio y elegir el modelo/criterio adecuado.

## Fundamento teórico
Categorías principales:
- **Estabilidad de ángulo del rotor:** capacidad de las máquinas síncronas de mantener sincronismo.
  Subdivisiones: *pequeña señal* (oscilaciones, [[ecuacion-oscilacion|modo electromecánico]]) y
  *transitoria* (gran perturbación, criterio de áreas iguales).
- **Estabilidad de frecuencia:** equilibrio generación-carga tras un desbalance grande; depende de
  inercia y reservas (FFR, droop). Escala: segundos a minutos.
- **Estabilidad de tensión:** capacidad de mantener tensiones aceptables; *pequeña* y *gran*
  perturbación; ligada a límites de reactiva y colapso de tensión.
- **Estabilidad de resonancia:** intercambio de energía oscilatorio — *eléctrica* (serie, SSR) y
  *electromecánica* (torsional); ver [[fenomenos-oscilatorios-red|oscilaciones subsíncronas]].
- **Estabilidad impulsada por convertidor (converter-driven):** la categoría **nueva** de 2021,
  por la dinámica rápida de la electrónica de potencia. Dos bandas:
  - *Interacción lenta* (< ~10 Hz): PLL en red débil, lazo de potencia/sincronización
    ([[interaccion-pll-red-debil]], GFM vs GFL).
  - *Interacción rápida* (decenas de Hz–kHz): resonancia/[[fenomenos-oscilatorios-red|estabilidad armónica]].

Eje transversal: **pequeña señal** (linealización, autovalores/impedancia) vs **gran perturbación**
(simulación no lineal en el tiempo).

<div class="cfig"><img src="figuras/clasificacion-estabilidad-bandas.png" alt="bandas de frecuencia de los fenomenos de estabilidad"><div class="cap">La frecuencia de la oscilación ubica el fenómeno: modos electromecánicos de ángulo/frecuencia (0.1–2 Hz), interacción converter-driven lenta (PLL en red débil, 1–10 Hz), resonancia SSR/SSCI (5–100 Hz) e interacción rápida / armónica (100 Hz–3 kHz). Cada banda dicta el modelo (electromecánico, fasorial, conmutado), la herramienta y la mitigación.</div></div>

## 1 — Ejemplo cuantitativo: diagnóstico de una oscilación por su frecuencia
**Caso A — oscilación a 3.3 Hz.** En el proyecto GFM, el análisis modal da un modo dominante a \( f=3.3\,\text{Hz} \) con \( \zeta=0.40 \). Por la taxonomía: \( f<10\,\text{Hz} \), origen en el lazo de potencia/droop (converter-driven lento). Herramienta adecuada: modelo lineal dq + autovalores. No es un modo electromecánico (no hay máquina síncrona) ni resonancia armónica (demasiado lenta).

**Caso B — oscilación a 250 Hz.** Si en el modelo conmutado aparece una resonancia a 250 Hz, la taxonomía indica: converter-driven rápido (10 Hz–kHz), posiblemente resonancia del filtro LCL (\( f_{res}=1/(2\pi\sqrt{L_2 C_f})\approx250\,\text{Hz} \) con \( L_2=1.5\,\text{mH} \), \( C_f=270\,\mu\text{F} \)). Herramienta: impedancia dq, criterio Nyquist generalizado. Mitigación: amortiguamiento activo o resistor de damping en el filtro.

**Caso C — colapso de tensión en 2 s.** Oscilación lenta que colapsa en segundos → estabilidad de tensión (no converter-driven). Herramienta: flujo de carga dinámico, margen de reactiva. Modelo adecuado: fasorial lento, no dq de alta frecuencia.

La frecuencia de la oscilación es el primer clasificador; la variable afectada (ángulo, tensión, corriente) y el origen físico (inercia, PLL, filtro) son el segundo nivel de clasificación.

## 2 — Estabilidad de pequeña señal

**Paso 1 — linealización.** Alrededor de un punto de operación \( (x_0,u_0) \), el sistema no lineal \( \dot x = f(x,u) \) se aproxima por:
$$ \dot{\delta x}=A\,\delta x+B\,\delta u,\qquad A=\left.\frac{\partial f}{\partial x}\right|_{x_0} $$
La pequeña señal es válida para \( \|\delta x\|\ll\|x_0\| \): perturbaciones "pequeñas" que no abandonan la vecindad lineal del equilibrio.

**Paso 2 — condición de estabilidad.** El equilibrio es **estable en pequeña señal** si y sólo si todos los autovalores de \( A \) tienen parte real negativa: \( \text{Re}(\lambda_i)<0 \;\forall i \). El margen de estabilidad es cuantificado por el amortiguamiento del modo más crítico:
$$ \zeta_i = \frac{-\text{Re}(\lambda_i)}{|\lambda_i|} $$
El criterio de diseño habitual es \( \zeta_{\min}>0.05 \) (5 % de amortiguamiento mínimo) para todos los modos.

**Paso 3 — el margen de fase como proxy.** Para un sistema SISO, el margen de fase \( PM \) es el indicador de estabilidad de pequeña señal en frecuencia: \( PM>0\Leftrightarrow\text{estable} \). La relación aproximada entre PM y amortiguamiento del modo de cruce es \( \zeta\approx PM[\text{rad}]/2 \) (válida solo para sistemas de segundo orden equivalente, pero útil como guía).

**Paso 4 — análisis modal.** La descomposición en modos (autovalores + factores de participación) identifica cuáles estados son los más activos en cada modo y qué parámetros los controlan. En el GFM, el modo de potencia (\( \lambda\approx-20\pm j21 \), \( f=3.3\,\text{Hz} \), \( \zeta=0.40 \)) está controlado principalmente por el droop \( m_p \) y el filtro de potencia \( \omega_c \).

## 3 — Estabilidad de gran señal

**Paso 1 — por qué la linealización no basta.** Ante una falta trifásica, el sistema sale de la vecindad lineal del punto de operación: la aproximación \( A\delta x \) deja de ser válida. La pregunta es si el sistema regresa al mismo equilibrio (o a uno nuevo) tras la perturbación grande.

**Paso 2 — la región de atracción.** El conjunto \( \mathcal{R}(x_0) \) de estados iniciales desde los cuales el sistema converge a \( x_0 \) es la **región de atracción**. Dentro de \( \mathcal{R} \), el sistema es estable ante perturbaciones grandes. Estimar \( \mathcal{R} \) es el problema central de la estabilidad de gran señal.

**Paso 3 — el criterio de Lyapunov.** Si existe una función \( V(x)\geq0 \) con \( V(x_0)=0 \) y \( \dot V<0 \) fuera de \( x_0 \), el sistema es estable. El nivel \( V(x)=c \) contenido en \( \{x:\dot V<0\} \) es un **conjunto invariante** y da una estimación conservadora de \( \mathcal{R} \). Para el péndulo del droop (modelo equivalente del GFM con ángulo \( \delta \) y velocidad \( \Delta\omega \)):
$$ V(\delta,\Delta\omega)=\frac{1}{2}\tau_p\Delta\omega^2 - m_p P_{ref}(\delta-\delta_0) + m_p\int_{\delta_0}^{\delta}P(\delta')\,d\delta' $$
Esta función (energía cinética + energía potencial eléctrica) es una función de Lyapunov si \( P(\delta) \) es monótonamente creciente en la región de interés.

**Paso 4 — el criterio de áreas iguales (CAI).** Para el GFM o la máquina síncrona, el CAI establece que el sistema es estable tras una falta si el **área acelerante** (energía ganada durante la falta) es menor que el **área decelerante** (energía que puede absorber después). Gráficamente: el área entre la curva \( P(\delta) \) y la potencia mecánica, desde el ángulo inicial hasta el ángulo de apertura de la falta, es el límite. El margen de estabilidad transitoria (TSM) es la diferencia de áreas.

## 4 — Estabilidad de tensión: la curva PV

**Paso 1 — el modelo del nudo de carga.** Considerar un nudo de carga conectado a la red a través de una impedancia \( Z=R+jX \) (la línea) con tensión de fuente \( V_s\angle0 \). La tensión en el nudo de carga \( V_r \) satisface la ecuación de flujo de carga:
$$ P+jQ=V_r^*\cdot\frac{V_s-V_r}{Z^*} $$
Fijada \( P+jQ \) (la carga), esta ecuación determina \( V_r \). Tiene hasta dos soluciones: la de alta tensión (operación normal) y la de baja tensión (inestable).

**Paso 2 — la curva PV (nose curve).** Variando la potencia activa \( P \) de la carga (con factor de potencia constante) y calculando \( |V_r| \), se obtiene la curva \( V_r(P) \). Tiene forma de nariz: la rama superior es estable (operación normal), la rama inferior es inestable. El **punto de colapso** (nose point) es el máximo de \( P \): no existe solución para cargas mayores.

**Paso 3 — el margen de estabilidad de tensión.** La distancia del punto de operación al punto de colapso en la dirección de aumento de carga es el margen de estabilidad de tensión (VSM). En por unidad:
$$ VSM = \frac{P_{max}-P_{op}}{P_{max}} $$
Criterios típicos: \( VSM>10\% \) para operación normal, \( VSM>5\% \) en contingencia \( N-1 \).

**Paso 4 — el índice de estabilidad de tensión.** La sensibilidad \( dV/dP \) en el punto de operación es un indicador: si \( dV/dP\to-\infty \), el sistema está cerca del colapso. En la práctica se usa la **matriz Jacobiana del flujo de carga**: si el menor valor propio de la parte de tensión del Jacobiano \( J \) es pequeño, la tensión es poco robusta.

## 5 — Estabilidad de frecuencia

**Paso 1 — el desbalance P.** Tras la pérdida de un generador de potencia \( \Delta P_{gen} \), la ecuación de balance es:
$$ 2H\,\frac{d\Delta\omega}{\omega_0 dt}=-\Delta P_{gen}+\Delta P_{droop}+\Delta P_{AGC}+\Delta P_{carga} $$
donde \( H \) es la constante de inercia (en segundos) y \( \omega_0=2\pi\times50 \). En ausencia de respuesta de control, la frecuencia cae a una tasa inicial (RoCoF):

**Paso 2 — el RoCoF.** La tasa de cambio de frecuencia inmediatamente después del evento es:
$$ \text{RoCoF}=\frac{d\omega/dt}{\omega_0}\bigg|_{t=0}=\frac{-\Delta P_{gen}}{2H} \quad [\text{Hz/s}] $$
Para una red con \( H=5\,\text{s} \) y pérdida de \( \Delta P=0.10\,\text{pu} \): \( \text{RoCoF}=-0.01\,\text{Hz/s} \). Para una red de poca inercia (\( H=2\,\text{s} \)): \( \text{RoCoF}=-0.025\,\text{Hz/s} \), que puede disparar las protecciones de frecuencia (típicamente activan a \( |\text{RoCoF}|>0.5\,\text{Hz/s} \) en algunos países).

**Paso 3 — la respuesta primaria (droop).** El control droop de frecuencia \( \Delta P=-K_d\Delta\omega \) (respuesta primaria) detiene la caída de frecuencia y establece un nuevo equilibrio:
$$ \Delta\omega_{ss}=\frac{-\Delta P_{gen}}{K_d+D_L} $$
donde \( D_L \) es la dependencia frecuencial de la carga (alivio natural). La frecuencia se estabiliza en el **nadir** \( f_{min} \) antes de que la respuesta primaria actúe; el nadir es el punto más bajo y su diferencia con \( f_0=50\,\text{Hz} \) mide la severidad del evento.

**Paso 4 — la respuesta secundaria (AGC).** El regulador automático de generación (AGC) actúa en \( \sim30\,\text{s}\to\text{min} \) y restaura \( \omega\to\omega_0 \) eliminando el error en régimen permanente que deja el droop. La respuesta terciaria (despacho económico) actúa en minutos-horas.

<div class="cfig"><img src="figuras/clasificacion-estabilidad-analisis.png" alt="arbol IEEE, curva PV, respuesta frecuencia, region de atraccion"><div class="cap">Cuatro aspectos de la clasificación de estabilidad: (a) árbol de clasificación IEEE/CIGRE 2021 con las categorías principales; (b) la curva PV (nose curve) del nudo de carga — el punto de colapso y el margen de estabilidad de tensión; (c) la respuesta de frecuencia ante pérdida de generación: RoCoF, nadir y recuperación primaria/secundaria; (d) la región de atracción del GFM en el plano $(\delta,\Delta\omega)$: el pozo de potencial y el límite de estabilidad de gran señal.</div></div>

## 6 — Clasificación de la inestabilidad del proyecto 01 (GFM)

**Tipo 1: pequeña señal — modo de potencia.** El análisis modal del proyecto 01 revela el modo dominante \( \lambda_{3,4}=-20\pm j21\,\text{rad/s} \) (\( f=3.3\,\text{Hz} \), \( \zeta=0.40 \)). Sin rediseño del droop, el modo tiene \( \zeta=0.15 \) (insuficiente). Herramienta: linealización dq, autovalores, factor de participación. Mitigación: filtro de potencia más rápido o incremento del amortiguamiento activo (Kad).

**Tipo 2: transitoria ante un hueco.** Una caída de tensión de 80 % durante 150 ms hace que el GFM exceda el límite de corriente. La estabilidad transitoria se analiza por simulación no lineal: el ángulo interno \( \delta \) puede salir de la región de atracción y el sistema pierde sincronismo. El critrio de áreas iguales sobre la curva \( P(\delta) \) del GFM da el tiempo de despeje máximo \( t_{cl,\max}\approx200\,\text{ms} \).

**Tipo 3: estabilidad de tensión en red débil.** Para SCR < 2, la tensión del nudo PCC cae debajo del 90 % en régimen permanente a plena carga. La curva PV del nudo PCC (tensión vs potencia activa despachada) muestra un VSM de solo 8 % — límite de la especificación. Esto se cuantifica con flujo de carga paramétrico variando SCR: para SCR < 1.8 no existe solución de flujo de carga a plena carga.

## 3 — Estabilidad de Lyapunov

**Paso 1 — definición formal y jerarquía de nociones.** Para el sistema \(\dot{x}=f(x)\) con equilibrio \(x^*=0\), se distinguen las siguientes nociones de estabilidad, de menor a mayor exigencia:
- **Estable (S. Lyapunov):** para todo \(\varepsilon>0\) existe \(\delta>0\) tal que \(\|x_0\|<\delta \Rightarrow \|x(t)\|<\varepsilon\) para todo \(t\geq0\). El sistema no se aleja del equilibrio ante perturbaciones pequeñas, pero no necesariamente regresa.
- **Asintóticamente estable (A.S.):** es estable y además \(x(t)\to0\) cuando \(t\to\infty\). Requiere convergencia.
- **Globalmente asintóticamente estable (G.A.S.):** es A.S. para cualquier condición inicial (toda la región de estado es de atracción).
- **Inestable:** negación de estable — existe \(\varepsilon>0\) tal que para todo \(\delta>0\) hay \(x_0\) con \(\|x_0\|<\delta\) y \(\|x(t_1)\|\geq\varepsilon\) para algún \(t_1>0\).

Para convertidores, la estabilidad asintótica local es el mínimo requerido; la global garantiza fault-ride-through desde cualquier condición inicial.

**Paso 2 — teorema de Lyapunov: condiciones suficientes.** Una función \(V:D\to\mathbb{R}\) de clase \(C^1\) es una **función de Lyapunov** si en un entorno \(D\) del equilibrio:
1. \(V(0)=0\) y \(V(x)>0\) para \(x\in D\setminus\{0\}\) (definida positiva).
2. \(\dot{V}(x) = \nabla V(x)^T f(x) < 0\) para \(x\in D\setminus\{0\}\) (derivada definida negativa).

Si existe tal \(V\), el equilibrio es asintóticamente estable. Si \(D=\mathbb{R}^n\) y además \(V(x)\to\infty\) cuando \(\|x\|\to\infty\) (radialmente no acotada), el equilibrio es G.A.S.

**Paso 3 — función de Lyapunov cuadrática para sistemas lineales: derivación.** Para \(\dot{x}=Ax\), la candidata natural es \(V(x)=x^TPx\) con \(P=P^T>0\) (definida positiva por construcción). La derivada temporal es:

$$\dot{V}(x) = \dot{x}^TPx + x^TP\dot{x} = x^T(A^TP+PA)x$$

Para que \(\dot{V}<0\) se requiere \(A^TP+PA<0\) (definida negativa). Eligiendo \(Q>0\) arbitraria y resolviendo la **ecuación de Lyapunov continua**:

$$A^TP + PA = -Q$$

existe solución \(P>0\) única si y solo si todos los autovalores de \(A\) tienen parte real negativa (teorema de Lyapunov para matrices). La solución es \(P = \int_0^\infty e^{A^Tt}Qe^{At}\,dt\).

**Paso 4 — cálculo práctico y estimación de la región de atracción.** En Python: `P = scipy.linalg.solve_continuous_lyapunov(A.T, -Q)`. Si todos los eigenvalores de \(P\) son positivos, \(P>0\) y el sistema es estable (para la \(Q>0\) elegida). Para la estimación de la ROA: se busca el mayor valor \(c\) tal que el conjunto de nivel \(\Omega_c = \{x: x^TPx\leq c\}\) satisface \(\dot{V}(x)<0\) para todo \(x\in\Omega_c\). Para sistemas no lineales, esto requiere verificar \(\dot{V}(x)=\nabla V\cdot f(x)<0\) en el elipsoide \(\Omega_c\), lo que se puede hacer con métodos de suma de cuadrados (SOS) o por muestreo.

**Paso 5 — ejemplo: péndulo del droop GFM.** Para el modelo del droop del GFM \(\dot{\delta}=\omega_0\Delta\omega\), \(\dot{\Delta\omega}=(P_{ref}-\sin\delta)/\tau_p - \Delta\omega/\tau_p\), la función de energía total es una función de Lyapunov natural:

$$V(\delta,\Delta\omega) = \frac{\tau_p}{2}\Delta\omega^2 + \int_{\delta_0}^{\delta}(\sin\delta'-P_{ref})\,d\delta' = \frac{\tau_p}{2}\Delta\omega^2 + (P_{ref}(\delta_0-\delta) - \cos\delta + \cos\delta_0)$$

\(\dot{V}=-\Delta\omega^2/\tau_p \leq 0\): la función es no creciente — el sistema es estable. La ROA está acotada por el nivel \(V(\delta_{us},0)\) donde \(\delta_{us}=\pi-\delta_0\) es el ángulo inestable (el segundo cruce de \(\sin\delta=P_{ref}\)).

## 4 — Estabilidad de pequeña señal (linealización)

**Paso 1 — jacobiano en el punto de operación: derivación.** Para el sistema no lineal \(\dot{x}=f(x,u)\) con punto de equilibrio \((x^*, u^*)\) (solución de \(f(x^*,u^*)=0\)), la expansión de Taylor de primer orden alrededor del equilibrio da la **dinámica linealizada**:

$$\dot{\delta x} = A\,\delta x + B\,\delta u, \quad A = \left.\frac{\partial f}{\partial x}\right|_{(x^*,u^*)}, \quad B = \left.\frac{\partial f}{\partial u}\right|_{(x^*,u^*)}$$

donde \(\delta x = x - x^*\) y \(\delta u = u - u^*\). El **Jacobiano** \(A\in\mathbb{R}^{n\times n}\) se calcula analíticamente (derivando las ecuaciones del modelo) o numéricamente (perturbación finita: \(A_{ij}\approx[f_i(x^*+h e_j)-f_i(x^*)]/h\)). La linealización es válida para perturbaciones pequeñas \(\|\delta x\|\ll\|x^*\|\) — en convertidores, típicamente para variaciones menores del 10% de los valores en régimen permanente.

**Paso 2 — condición de estabilidad local: teorema de Lyapunov para sistemas no lineales.** El teorema de Lyapunov (versión para sistemas no lineales) establece: si todos los eigenvalores de \(A\) tienen parte real **estrictamente negativa** (\(\text{Re}(\lambda_i)<0\) para todo \(i\)), el equilibrio \(x^*\) es asintóticamente estable **localmente**. Si algún eigenvalor tiene \(\text{Re}(\lambda_i)>0\), el equilibrio es inestable. Si algún eigenvalor tiene \(\text{Re}(\lambda_i)=0\) exactamente (caso marginal), el análisis lineal no es concluyente: la estabilidad depende de los términos no lineales y se requiere análisis de Lyapunov o simulación.

**Paso 3 — amortiguamiento modal: cálculo y criterios de diseño.** Para un par de eigenvalores complejos conjugados \(\lambda_{i,i+1}=-\sigma_i\pm j\omega_{d,i}\), el amortiguamiento modal y la frecuencia natural son:

$$\zeta_i = \frac{\sigma_i}{\sqrt{\sigma_i^2+\omega_{d,i}^2}} = \frac{-\text{Re}(\lambda_i)}{|\lambda_i|}, \quad \omega_{n,i} = |\lambda_i| = \sqrt{\sigma_i^2+\omega_{d,i}^2}$$

Los criterios de diseño estándar para sistemas de potencia (IEEE Std 1110):
- \(\zeta_i > 0.05\) (5%): mínimo aceptable — oscilaciones perceptibles pero estables.
- \(\zeta_i > 0.10\) (10%): recomendado para operación normal.
- \(\zeta_i > 0.20\) (20%): para modos de frecuencia baja (< 1 Hz) para evitar oscilaciones sostenidas.

Para el GFM (proyecto 01): el modo de potencia tiene \(\zeta\approx0.40\) con el diseño nominal — ampliamente satisfecho. Sin rediseño del droop sería \(\zeta\approx0.15\) — justo sobre el mínimo.

**Paso 4 — análisis modal: factores de participación y guía de rediseño.** Los **factores de participación** cuantifican la contribución de cada estado a cada modo:

$$p_{ki} = \phi_{ki}\cdot\psi_{ki}^*$$

donde \(\phi_{ki}\) es el \(k\)-ésimo elemento del autovector derecho del modo \(i\) (\(A\phi_i=\lambda_i\phi_i\)) y \(\psi_{ki}\) el del autovector izquierdo (\(\psi_i^TA=\lambda_i\psi_i^T\)). Por la biortogonalidad, \(\sum_k p_{ki}=1\) para cada modo. Los factores de participación son adimensionales e independientes del escalado de los estados — ideales para comparar la influencia de distintos estados.

Interpretación para el rediseño: el estado con mayor \(|p_{ki}|\) en el modo de interés es el que más contribuye a ese modo. Para el GFM con modo de potencia \(\lambda_3\), si el mayor \(|p_{k3}|\) corresponde al estado de energía filtrada de potencia \(P_f\), el parámetro de control más efectivo es la constante de tiempo del filtro de potencia \(\omega_c\) — no el droop \(m_p\).

**Paso 5 — cálculo numérico en Python.** El flujo completo de análisis modal:
```python
import numpy as np
from scipy.linalg import eig
eigenvalues, vr = np.linalg.eig(A)   # vr: autovectores derechos columna
vl = np.linalg.inv(vr).T              # autovectores izquierdos
P = vr * vl.conj()                    # matriz de factores de participacion
zeta = -eigenvalues.real / np.abs(eigenvalues)
f_osc = eigenvalues.imag / (2*np.pi)  # frecuencia de oscilacion
```
El modo más crítico es el de menor \(\zeta_i>0\). El estado más activo en ese modo es `np.argmax(np.abs(P[:, i_critico]))` — señala qué parámetro rediseñar.

## 5 — Estabilidad de gran señal

**Paso 1 — por qué la linealización no basta: el problema de la ROA.** Ante perturbaciones grandes (huecos de tensión, pérdida de generación, faltas), el sistema sale de la vecindad lineal del equilibrio: la aproximación \(\dot{\delta x}\approx A\delta x\) deja de ser válida. Un sistema puede ser localmente estable (todos los autovalores de \(A\) en el SPL) pero **diverger** ante una perturbación que lleve el estado fuera de la **región de atracción** (ROA). La ROA puede ser pequeña — especialmente en convertidores con limitadores de corriente que crean saturaciones efectivas en el espacio de estado.

**Paso 2 — región de atracción: definición y estimación.** La ROA es el conjunto:

$$\mathcal{R}(x^*) = \{x_0\in\mathbb{R}^n : \lim_{t\to\infty} x(t; x_0) = x^*\}$$

Para estimar \(\mathcal{R}\), se construye una función de Lyapunov \(V(x)\) y se busca el mayor nivel \(c^*\) tal que el **conjunto de nivel** \(\Omega_{c^*} = \{x: V(x)\leq c^*\}\) está completamente contenido en la región donde \(\dot{V}(x)<0\). El algoritmo: calcular \(c^* = \min_{x\in\partial\mathcal{S}^c}V(x)\) donde \(\mathcal{S}^c = \{x:\dot{V}(x)>0\}\) es el conjunto donde la derivada es positiva. El conjunto \(\Omega_{c^*}\) es invariante positivo y satisface \(\Omega_{c^*}\subseteq\mathcal{R}(x^*)\).

**Paso 3 — fault-ride-through como requisito de ROA: criterio de áreas iguales.** La norma ENTSO-E RED requiere FRT: mantenerse conectado durante huecos de hasta 0% por 150 ms. Para el GFM equivalente al péndulo (con función de Lyapunov de energía del §3), la condición FRT es que la energía acumulada durante el hueco sea menor que la energía disponible en la parte decelerante:

$$\int_{\delta_0}^{\delta_{cl}}(P_m - P_{sin}(\delta,V_{fault}))\,d\delta < \int_{\delta_{cl}}^{\delta_{us}}(P_{sin}(\delta,V_n)-P_m)\,d\delta$$

donde \(\delta_{cl}\) es el ángulo en el instante de despeje de la falta, \(\delta_{us}=\pi-\delta_0\) el ángulo inestable, y \(V_{fault}\) la tensión durante la falta. Esto es el **criterio de áreas iguales** (CAI): área acelerante < área decelerante. El tiempo de despeje máximo \(t_{cl,max}\) es el valor límite: despejar la falta antes de \(t_{cl,max}\) garantiza estabilidad transitoria.

**Paso 4 — método de Zames-Falb para no linealidades con sector acotado.** Cuando el sistema tiene no linealidades del tipo saturation \(\phi(y)=\text{sat}(y,y_{max})\) (en la corriente de referencia) o limiter, el método de Zames-Falb generaliza el criterio del círculo. Si la no linealidad pertenece al **sector** \([0, K]\) (es decir, \(0\leq\phi(y)y\leq Ky^2\)), el sistema en lazo cerrado es globalmente asintóticamente estable si existe un multiplicador de Zames-Falb \(\rho(t)\) tal que:

$$\text{Re}[(1+\rho(j\omega))\cdot G_{cl}(j\omega)] + 1/K > 0 \quad \forall\omega$$

En la práctica, el criterio del círculo (versión simplificada sin multiplicador) es suficiente para saturaciones simétricas: el lazo de Nyquist de \(K\cdot G_{cl}\) no debe rodear el círculo \(|z+1/2|=1/2\) (disco de cero a \(-1/K\)). Para el limitador de corriente del GFM: \(K=i_{max}/\Delta v_{max}\), y el criterio garantiza que la corriente no oscila al alcanzar el límite.

**Paso 5 — simulación no lineal como verificación.** La simulación en dominio temporal con el modelo completo (no linealizado) es la herramienta de verificación final para la estabilidad de gran señal. El procedimiento estándar:
1. Simular el sistema en régimen permanente durante 0.5 s para verificar el punto de operación.
2. Aplicar el hueco de tensión (0% durante 150 ms).
3. Verificar que el ángulo \(\delta\) y la frecuencia \(\Delta\omega\) permanecen acotados y convergen al equilibrio post-falta.
4. Repetir para huecos asimétricos (fase a tierra, doble fase) que generan componentes de secuencia negativa.
Si la simulación muestra convergencia para el hueco más severo especificado, el requisito FRT está satisfecho.

## 6 — Estabilidad en redes: criterio de impedancia

**Paso 1 — sistema fuente-carga como lazo de realimentación: derivación del criterio.** Un sistema DC o AC con una fuente de tensión (impedancia de salida \(Z_s\)) conectada a una carga (impedancia de entrada \(Z_l\)) se puede representar como un lazo de realimentación con función de lazo \(T(s) = Z_s(s)/Z_l(s)\). La tensión en el bus es:

$$V_{bus}(s) = \frac{V_{s}(s)}{1 + Z_s(s)/Z_l(s)} = \frac{V_{s}(s)}{1 + T(s)}$$

La transferencia \(1/(1+T(s))\) tiene la misma forma que la sensibilidad de un sistema realimentado. Por el criterio de Nyquist, el sistema es estable (la tensión de bus es acotada ante perturbaciones de fuente) si y solo si el Nyquist de \(T(j\omega)=Z_s(j\omega)/Z_l(j\omega)\) no rodea el punto \(-1\). Para cargas de potencia constante (CPL), \(Z_l(s)\) es negativa en bajas frecuencias — el criterio de Nyquist puede indicar inestabilidad.

**Paso 2 — criterio de Middlebrook: condición suficiente conservadora.** El criterio de Middlebrook (1976) establece como condición suficiente de estabilidad:

$$|Z_s(j\omega)| \ll |Z_l(j\omega)| \quad \forall\omega$$

Si se cumple, \(|T(j\omega)| = |Z_s/Z_l| \ll 1\) para todo \(\omega\), y el diagrama de Nyquist de \(T\) está completamente dentro del disco unitario centrado en el origen — trivialmente no rodea \(-1\). La condición práctica: \(|Z_s/Z_l| < 0.3\) en toda frecuencia (margen de 10 dB). Esta condición es **muy conservadora**: un sistema con \(|Z_s/Z_l|=0.8\) a alguna frecuencia puede ser perfectamente estable si la fase es favorable.

**Paso 3 — criterio ESAC: relajación basada en fase.** El criterio ESAC (Energy Source Analysis Consortium) relaja Middlebrook permitiendo que \(|Z_s|>|Z_l|\) en algunas frecuencias, siempre que la fase de \(T=Z_s/Z_l\) no cause que el Nyquist de \(T\) rodee \(-1\). La condición ESAC: para cada frecuencia donde \(|T(j\omega)|\geq1\):

$$|\angle T(j\omega)| < 180° - PM_{ESAC}$$

con \(PM_{ESAC}=30°\) típicamente. Esto permite diseños más agresivos que Middlebrook, manteniendo un margen de estabilidad explícito. La verificación: graficar el contorno de \(T(j\omega)\) y verificar que no entra en el semicírculo izquierdo del disco unitario.

**Paso 4 — aplicación MVDC: bus DC con múltiples convertidores.** En un sistema MVDC con \(N\) convertidores conectados al bus DC, la impedancia equivalente del bus es la paralela de todas las impedancias de salida \(Z_{s,k}\) más la paralela de todas las impedancias de entrada \(Z_{l,j}\). El sistema es estable si la función de lazo generalizada:

$$T_{total}(s) = Z_{s,total}(s)/Z_{l,total}(s) = \frac{\left(\sum_k Z_{s,k}^{-1}\right)^{-1}}{\left(\sum_j Z_{l,j}^{-1}\right)^{-1}}$$

satisface el criterio de Nyquist. En la práctica, la estabilidad del bus MVDC es **emergente**: un convertidor añadido puede desestabilizar el bus aunque individualmente sea estable con la red. La medición experimental: se inyecta una señal de perturbación en el bus a través de un amplificador de potencia y se mide \(V_{bus}/I_{inj}\) con un analizador de impedancia — el Nyquist de \(T\) se obtiene directamente.

**Paso 5 — cargas de potencia constante (CPL): el caso más problemático.** Las cargas CPL (reguladores de tensión DC regulados en potencia) presentan impedancia de entrada negativa a bajas frecuencias:

$$Z_{l,CPL}(j\omega) \approx -\frac{V_{bus,0}^2}{P_0} \quad \text{para }\omega\ll\omega_{BW,CPL}$$

donde \(P_0\) es la potencia de la CPL y \(\omega_{BW,CPL}\) es el ancho de banda de su lazo de control interno. La impedancia negativa significa que la CPL absorbe más corriente cuando la tensión baja (lo opuesto a una resistencia), lo que puede llevar al colapso de tensión del bus. El criterio de estabilidad: \(|Z_{s,total}(j\omega)| < |Z_{l,CPL}(j\omega)| = V_{bus,0}^2/P_0\) para \(\omega < \omega_{BW,CPL}\). Esto impone un límite superior a la potencia CPL que puede absorber el bus sin volverse inestable.

<div class="cfig"><img src="figuras/clasificacion-estabilidad-analisis.png" alt="Clasificación estabilidad: plano de fase, eigenvalores con amortiguamiento, Lyapunov, criterio impedancia"><div class="cap">(a) Plano de fase de un sistema con espiral estable: las trayectorias desde distintas condiciones iniciales convergen al equilibrio. (b) Eigenvalores en el plano \(s\) con líneas de amortiguamiento constante: el modo con \(\zeta=0.05\) está en el límite de la especificación. (c) Curvas de nivel de la función de Lyapunov \(V(x)\): los elipsoides son conjuntos invariantes y acotan la ROA. (d) Criterio de impedancia: \(|Z_s|\) vs \(|Z_l|\) en frecuencia — la zona roja (\(|Z_s|>|Z_l|\)) requiere verificación de fase (criterio ESAC).</div></div>

## Cuándo y por qué se usa
Como mapa para diagnosticar: ante una oscilación o colapso, su frecuencia y causa la sitúan en una
categoría, lo que dicta el modelo (electromecánico, fasorial, conmutado), la herramienta (modal,
impedancia, dominio del tiempo) y la mitigación.

## Procedimiento de diseño (genérico)
1. Caracteriza el evento: variable afectada (ángulo/frecuencia/tensión), frecuencia de oscilación,
   tamaño de la perturbación.
2. Ubícalo en la categoría correspondiente.
3. Elige el modelo y el criterio (modal/impedancia/temporal) acorde a la escala.
4. Aplica la mitigación propia de esa categoría.

## Ejemplo de código
```text
f_osc < 1 Hz  ........ ángulo (modo electromecánico) / frecuencia
1–10 Hz ............. converter-driven lento (PLL, red débil)
10 Hz–kHz ........... converter-driven rápido (resonancia/armónica)
```

## Parámetros y valores típicos
Modo electromecánico 0.1–2 Hz; interárea 0.1–0.8 Hz; converter-driven lento 1–10 Hz; armónico
100 Hz–3 kHz; SSR/SSCI 5–100 Hz.

## Errores comunes
- Aplicar modelos electromecánicos (fasor a 50 Hz) a fenómenos converter-driven rápidos.
- Tratar como "estabilidad de tensión" una oscilación que es resonancia de impedancia.
- Olvidar que en sistemas dominados por convertidores la inercia ya no garantiza estabilidad.

## Conceptos relacionados
- [[fenomenos-oscilatorios-red|estabilidad armónica]] · [[ecuacion-oscilacion]] · [[interaccion-pll-red-debil]] · [[grid-forming-vs-following]]

## Referencias
- Hatziargyriou et al., *Definition and Classification of Power System Stability Revisited & Extended*, IEEE TPWRS 2021.
- Kundur, *Power System Stability and Control*, 1994.
