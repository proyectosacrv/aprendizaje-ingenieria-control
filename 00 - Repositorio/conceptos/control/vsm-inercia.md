---
titulo: VSM — máquina síncrona virtual (inercia)
slug: vsm-inercia
categoria: control
tipo: tecnica
nivel: avanzado
proyectos: [01-GFM-Impedance, 03-DataCenter-IA]
objetivos: [aportar inercia y amortiguamiento ajustable]
tags: [grid-forming, VSM, inercia, swing, RoCoF, nadir, autovalores, AVR-virtual]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [droop-control, grid-forming-vs-following, analisis-modal]
referencias:
  - "Zhong, Weiss, Synchronverters: Inverters That Mimic Synchronous Generators, IEEE TIE 2011"
  - "Beck, Hesse, Virtual synchronous machine, EPQU 2007"
  - "Van Wesenbeeck et al., Grid interaction of a VSM, IET RPG 2009"
---

## Definición
Estrategia grid-forming que reproduce la **ecuación de swing** de un generador síncrono, dando
al inversor **inercia** virtual \( J \) y **amortiguamiento** \( D \) ajustables por software.
A diferencia del droop —donde la frecuencia es algebraica e instantánea— aquí la frecuencia es
un **estado**: no puede saltar, su tasa de cambio (RoCoF) queda acotada por \( J \).

<div class="cfig"><img src="figuras/vsm-inercia-rocof.png" alt="frecuencia tras escalon de carga: droop vs VSM"><div class="cap">Tras un escalón de carga, el droop puro salta a su nuevo valor de frecuencia de forma instantánea (sin inercia); el VSM la mueve con pendiente acotada (RoCoF \(\propto 1/J\)): la inercia virtual frena la caída inicial. Ambos asientan en el mismo punto (mismo droop estacionario).</div></div>

---

## 1 — De la ecuación de swing al RoCoF y la inercia sintética

**Paso 1 — balance de pares en el eje virtual.**
El VSM emula la 2.ª ley de Newton rotacional de un generador. La inercia \( J \) por la
aceleración angular iguala al par neto (par mecánico de entrada menos par eléctrico menos
amortiguamiento viscoso):
$$ J\,\dot\omega = T_{set} - T_e - D\,(\omega - \omega_0) $$

**Paso 2 — de par a potencia.**
Cerca de \( \omega_0 \), par y potencia se relacionan por \( T = P/\omega \approx P/\omega_0 \).
Sustituyendo \( T_{set} = P_{set}/\omega_0 \) y \( T_e = P/\omega_0 \):
$$ \boxed{\;J\,\dot\omega = \frac{P_{set}-P}{\omega_0} - D\,(\omega-\omega_0),\qquad \dot\delta = \omega - \omega_0\;} $$
Esta es la **swing equation**. A diferencia del droop, aquí \( \omega \) es un estado integrado:
no puede saltar, solo acelerar o desacelerar.

**Paso 3 — el RoCoF en el primer instante.**
Justo tras un escalón de carga \( \Delta P \), la frecuencia aún no se ha movido
(\( \omega = \omega_0 \)), así que el término de \( D \) es nulo. La tasa de cambio inicial es:
$$ \left.\dot\omega\right|_{t=0^+} = \frac{P_{set} - P_0 - \Delta P}{\omega_0\,J} = \frac{-\Delta P}{\omega_0\,J} $$
El **RoCoF** es inversamente proporcional a \( J \): más inercia virtual → caída de frecuencia
más lenta. Convertido a Hz/s:
$$ \text{RoCoF} = \frac{\Delta f}{\Delta t}\bigg|_{t=0^+} = \frac{-\Delta P}{2\pi\,J\,f_0} \qquad [\text{Hz/s}] $$

**Paso 4 — dimensionar \( J \) por la constante de inercia \( H \).**
\( H \) es la energía cinética almacenada a \( \omega_0 \) normalizada por \( S_n \) (segundos):
$$ H = \frac{\tfrac{1}{2}J\,\omega_0^2}{S_n} \qquad\Rightarrow\qquad J = \frac{2H\,S_n}{\omega_0^2} $$
Expresando el RoCoF en términos de \( H \):
$$ \text{RoCoF} = \frac{-\Delta P \cdot f_0}{H \cdot S_n} \qquad [\text{Hz/s}] $$
Con \( H = 4\,\text{s} \) y \( \Delta P = 10\%\,S_n \) se obtiene RoCoF = \(-f_0/(40) = -1.25\,\text{Hz/s}\)
a 50 Hz, comparable a una máquina de tamaño medio.

---

## 2 — Por qué en régimen permanente el VSM es un droop \( 1/(\omega_0 D) \)

**Paso 1 — anular la derivada.**
En régimen permanente \( \dot\omega = 0 \). La swing se reduce a un balance algebraico:
$$ 0 = \frac{P_{set} - P_{ss}}{\omega_0} - D\,(\omega_{ss} - \omega_0) $$

**Paso 2 — despejar la frecuencia.**
Aislando \( \omega_{ss} \):
$$ \omega_{ss} = \omega_0 + \frac{1}{\omega_0 D}\,(P_{set} - P_{ss}) $$

**Paso 3 — comparar con el droop.**
Esto es idéntico a la ley de droop \( \omega = \omega_0 + m_p(P_{set} - P) \) con pendiente
equivalente:
$$ \boxed{\;m_{p,eq} = \frac{1}{\omega_0 D} \;\Longleftrightarrow\; D = \frac{1}{\omega_0\,m_p}\;} $$

**Conclusión:** \( J \) solo gobierna el transitorio (RoCoF, inercia) y \( D \) fija el
estatismo estacionario. El reparto de carga en estado permanente es el mismo que un droop con
\( m_p = 1/(\omega_0 D) \). Por eso se pueden elegir \( D \) para igualar el droop deseado y
\( J \) para el soporte inercial, de forma **independiente** en primer orden.

---

## 3 — Respuesta dinámica de la frecuencia: la curva nadir

### 3.1 — Planteamiento
Ante un escalón de carga \( \Delta P \) que entra en \( t = 0 \), el VSM parte de
\( \omega(0) = \omega_0 \) y \( P_{set} - P_0 = 0 \) (equilibrio previo). La swing queda:
$$ J\,\dot\omega = \frac{-\Delta P}{\omega_0} - D\,(\omega - \omega_0) $$

### 3.2 — Cambio de variable
Definimos la desviación de frecuencia \( \Delta\omega = \omega - \omega_0 \). La ODE se convierte en:
$$ J\,\Delta\dot\omega = -\frac{\Delta P}{\omega_0} - D\,\Delta\omega $$

Introducimos \( y = \Delta\omega + \dfrac{\Delta P}{\omega_0 D} \) (desplazamiento al punto de
equilibrio estacionario). Entonces:
$$ \dot y = \Delta\dot\omega = -\frac{D}{J}\,y $$
La ODE es de primer orden con constante de tiempo \( \tau = J/D \).

### 3.3 — Solución analítica
Con la condición inicial \( \Delta\omega(0) = 0 \) se tiene \( y(0) = \dfrac{\Delta P}{\omega_0 D} \).
Integrando:
$$ y(t) = \frac{\Delta P}{\omega_0 D}\,e^{-D\,t/J} $$
Deshaciendo el cambio de variable:
$$ \boxed{\;\Delta\omega(t) = -\frac{\Delta P}{\omega_0 D}\,\bigl(1 - e^{-Dt/J}\bigr)\;} $$
En Hz: \( \Delta f(t) = \Delta\omega(t)/(2\pi) \).

### 3.4 — El nadir
Nótese que \( \Delta\omega(t) \) es **monótonamente decreciente** en este modelo de primer orden
(sin lazo de regulación primaria activo ni integrador de potencia). El valor mínimo (nadir) se
alcanza asintóticamente en \( t \to \infty \):
$$ \Delta f_{nadir} = -\frac{\Delta P}{\omega_0 D \cdot 2\pi} = -\frac{m_p}{2\pi}\,\Delta P \qquad [\text{Hz}] $$
Esto confirma que el nadir estacionario **no depende de** \( J \): inercia mayor retrasa el
nadir pero no lo reduce. La curva \( \Delta f(t) \) tiene pendiente inicial:
$$ \left.\frac{d\,\Delta f}{dt}\right|_{t=0^+} = -\frac{\Delta P}{J\,\omega_0 \cdot 2\pi} = \text{RoCoF inicial} $$

### 3.5 — Ejemplo numérico
Parámetros: \( S_n = 1\,\text{MVA} \), \( \omega_0 = 2\pi\cdot50\,\text{rad/s} \),
\( \Delta P = 200\,\text{kW} \), droop \( m_p = 0.5\% \Rightarrow D = 1/(\omega_0 m_p) = 2\,026\,\text{N·m·s/rad} \).

| \( H \) [s] | \( J \) [kg·m²] | RoCoF [Hz/s] | \( \tau = J/D \) [s] | \( \Delta f_{nadir} \) [Hz] |
|:---:|:---:|:---:|:---:|:---:|
| 1 | 12.7 | −5.0 | 0.006 | −0.30 |
| 4 | 50.7 | −1.25 | 0.025 | −0.30 |
| 10 | 126.6 | −0.50 | 0.062 | −0.30 |

El nadir es siempre −0.30 Hz (independiente de \( J \)), pero el RoCoF es 10× menor con
\( H=10\,\text{s} \) respecto a \( H=1\,\text{s} \).

---

## 4 — Autovalores del modo de potencia: \( \omega_n \), \( \zeta \), \( J \) y \( D \)

### 4.1 — Linealización del par (swing + línea)
El ángulo \( \delta \) controla el flujo de potencia eléctrica. Alrededor del punto de operación
\( (\delta_0, \omega_0) \), linealizando:
$$ P(\delta) \approx P_0 + K_s\,\tilde\delta, \qquad K_s = \left.\frac{\partial P}{\partial\delta}\right|_{\delta_0} $$
donde \( K_s \) [W/rad] es la **rigidez sincronizante** (stiffness). Para una línea inductiva
de reactancia \( X \) con tensiones \( E \) y \( V \): \( K_s = EV/X\cdot\cos\delta_0 \).

Las variables de estado linealizadas son \( \tilde\delta \) (desviación de ángulo) y
\( \tilde\omega = \Delta\omega \) (desviación de frecuencia). Las ecuaciones son:
$$ \dot{\tilde\delta} = \tilde\omega $$
$$ J\,\dot{\tilde\omega} = -\frac{K_s}{\omega_0}\,\tilde\delta - D\,\tilde\omega $$

### 4.2 — Matriz A y polinomio característico
La matriz del sistema es:
$$ A = \begin{pmatrix} 0 & 1 \\ -K_s/(J\,\omega_0) & -D/J \end{pmatrix} $$
El polinomio característico \( \det(\lambda I - A) = 0 \):
$$ \lambda^2 + \frac{D}{J}\,\lambda + \frac{K_s}{J\,\omega_0} = 0 $$

### 4.3 — Parámetros del modo oscilante
Comparando con la forma estándar \( \lambda^2 + 2\zeta\omega_n\lambda + \omega_n^2 \):
$$ \omega_n = \sqrt{\frac{K_s}{J\,\omega_0}} \qquad [\text{rad/s}] $$
$$ 2\zeta\omega_n = \frac{D}{J} \;\Rightarrow\; \zeta = \frac{D/J}{2\,\omega_n} = \frac{D}{2}\sqrt{\frac{\omega_0}{J\,K_s}} $$

En términos de la constante de inercia \( H = J\omega_0^2/(2S_n) \):
$$ \omega_n = \sqrt{\frac{K_s\,\omega_0}{2H\,S_n/\omega_0}} = \omega_0\sqrt{\frac{K_s}{2H\,S_n}} $$
$$ \zeta = \frac{D\,\omega_0}{2\sqrt{2H\,S_n\,K_s/\omega_0}} = \frac{D}{2}\sqrt{\frac{\omega_0^3}{2H\,S_n\,K_s}} $$

### 4.4 — Condición de amortiguamiento crítico
Para \( \zeta > 0.7 \) (sobreamortiguamiento suficiente):
$$ D > 2\cdot 0.7\cdot\omega_n J = 1.4\sqrt{\frac{J\,K_s}{\omega_0}} $$
o equivalentemente:
$$ D > 1.4\sqrt{\frac{2H\,S_n\,K_s}{\omega_0^3}} $$

### 4.5 — Ejemplo numérico
Con \( K_s = 500\,\text{kW/rad} \), \( S_n = 1\,\text{MVA} \), \( \omega_0 = 2\pi\cdot50\,\text{rad/s} \),
\( D = D_{droop} = 2\,026\,\text{N·m·s/rad} \) (droop 0.5 %):

| \( H \) [s] | \( J \) [kg·m²] | \( \omega_n \) [rad/s] | \( f_n \) [Hz] | \( \zeta \) | Régimen |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 0.5 | 6.3 | 11.1 | 1.77 | 14.4 | sobreamort. (dos reales) |
| 1 | 12.7 | 7.9 | 1.25 | 10.2 | sobreamort. |
| 4 | 50.7 | 3.95 | 0.63 | 5.1 | sobreamort. |
| 10 | 126.6 | 2.50 | 0.40 | 3.2 | sobreamort. |

Con \( D_{droop} \) el modo resulta muy amortiguado (casi no oscila). La frecuencia natural
\( f_n \approx 0.5\text{–}2\,\text{Hz} \) es propia del modo de potencia
(oscilaciones inter-área en redes reales caen en este rango).

---

## 5 — Interacción J-D-droop: los tres parámetros no son independientes

### 5.1 — D queda fijado por el droop
El requisito de estatismo (droop) impone directamente:
$$ D = \frac{1}{\omega_0\,m_p} = \frac{S_n}{\text{droop\%}\cdot\omega_0^2\cdot S_n/100} = \frac{100\,S_n}{\text{droop\%}\cdot\omega_0^2} $$
En números: para droop = 0.5 %, \( S_n = 1\,\text{MVA} \):
$$ D = \frac{1e6}{0.005\cdot(2\pi\cdot50)^2} = 2\,026\;\text{N·m·s/rad} $$

### 5.2 — J como único grado de libertad para \( \zeta \)
Con \( D \) fijo, sustituyendo en la expresión de \( \zeta \):
$$ \zeta = \frac{D}{2}\sqrt{\frac{\omega_0}{J\,K_s}} = \frac{D}{2}\sqrt{\frac{\omega_0^3}{2H\,S_n\,K_s}} $$
\( \zeta \) **disminuye al aumentar** \( J \) (o \( H \)). J es el único parámetro libre para
ajustar el amortiguamiento del modo de potencia.

### 5.3 — J óptimo para \( \zeta = 0.7 \)
Despejando \( J \) de la condición \( \zeta = 0.7 \):
$$ J_{opt} = \left(\frac{D}{2\cdot 0.7}\right)^2 \frac{\omega_0}{K_s} $$
o en términos de \( H \):
$$ H_{opt} = \left(\frac{D}{2\cdot 0.7}\right)^2 \frac{\omega_0^3}{2\,S_n\,K_s} $$

Con los parámetros anteriores (\( D = 2\,026 \), \( K_s = 500\,\text{kW/rad} \)):
$$ H_{opt} = \left(\frac{2026}{1.4}\right)^2 \frac{(2\pi\cdot50)^3}{2\cdot10^6\cdot500\times10^3} \approx 0.028\;\text{s} $$
Resultado sorprendente: con este droop tan bajo (0.5 %), cualquier \( H > 0.03\,\text{s} \) ya
implica modo sobre-amortiguado. En la práctica, para \( H \) de interés (1–10 s), el modo
siempre es sobre-amortiguado con el droop 0.5 %, y el ajuste de \( J \) afecta sobre todo a
la velocidad de respuesta (\( \omega_n \) y el tiempo de asentamiento), no al amortiguamiento.

### 5.4 — Tensión de diseño: droop ajustado vs amortiguamiento dinámico
La contradicción aparece cuando se busca a la vez droop pequeño (buen reparto de carga) y
modo de potencia rápido (rechazo de perturbaciones). Con droop pequeño, \( D \) es grande y
el sistema amortigua mucho pero se vuelve lento (\( \omega_n \) cae al aumentar \( J \)).
Las soluciones típicas son:

1. **Aumentar \( K_s \)**: usar impedancia virtual para elevar la rigidez aparente.
2. **Separar D estático y D dinámico**: añadir un filtro derivativo en la realimentación de
   \( \Delta\omega \) (lazo de amortiguamiento activo) de ganancia \( D_{extra} \), manteniendo
   el droop estático en \( 1/(\omega_0 D) \).
3. **Control de dos lazos**: lazo rápido de corriente + lazo lento de potencia con distinto \( D \).

---

## 6 — La constante \( H \) y comparación con máquinas reales

### 6.1 — Definición y significado físico
\( H \) cuantifica cuántos segundos puede la máquina sostener su potencia nominal solo con la
energía almacenada en su masa giratoria:
$$ H = \frac{E_{cinética,\,a\;\omega_0}}{S_n} = \frac{\tfrac{1}{2}J\,\omega_0^2}{S_n} \qquad [\text{s}] $$
Para una máquina real con masa rotante \( J_{masa} \):
\( H = \tfrac{1}{2}J_{masa}\,\omega_0^2/S_n \). El VSM puede fijar \( H \) arbitrariamente
ajustando el \( J \) virtual — no hay límite físico de masa.

### 6.2 — Valores típicos de la industria

| Tecnología | Potencia típica | \( H \) [s] |
|:---|:---:|:---:|
| Turboalternador vapor/gas | 50–1200 MW | 4–7 |
| Hidrogenerador | 5–700 MW | 2–4 |
| Motor síncrono industrial | 1–50 MW | 1–3 |
| Eólica con flywheel virtual | 0.5–5 MW | 2–5 |
| Eólica directa (sin inercia) | 0.5–5 MW | 0 |
| Solar FV (sin inercia) | 0.1–500 MW | 0 |
| **VSM típico** | cualquiera | **4** |
| **VSM alto H** | cualquiera | **10** |

### 6.3 — Límites del H virtual
**Límite inferior:** viene del RoCoF máximo admisible ante \( \Delta P_{max} \):
$$ H_{min} = \frac{\Delta P_{max}\cdot f_0}{\text{RoCoF}_{max}\cdot S_n} $$
Ejemplo: \( \Delta P_{max} = 10\%S_n \), RoCoF \(\leq 1\,\text{Hz/s}\):
$$ H_{min} = \frac{0.1\cdot50}{1} = 5\;\text{s} $$

**Límite superior:** la frecuencia natural \( \omega_n \) se vuelve muy baja, haciendo lento el
rechazo de perturbaciones y la sincronización con la red. En práctica \( H < 15\,\text{s} \)
para \( K_s \) de magnitud habitual.

### 6.4 — Tabla de prestaciones con \( K_s = 500\,\text{kW/rad} \), \( S_n = 1\,\text{MVA} \), droop 0.5 %

| \( H \) [s] | \( \omega_n \) [rad/s] | \( t_{2\%} \approx 4/\sigma \) [s] | RoCoF [Hz/s] (@10%\(S_n\)) | \( \Delta f_{nadir} \) [Hz] (@200 kW) |
|:---:|:---:|:---:|:---:|:---:|
| 1 | 7.9 | ~0.17 | 5.0 | −0.30 |
| 4 | 3.95 | ~0.34 | 1.25 | −0.30 |
| 10 | 2.50 | ~0.54 | 0.50 | −0.30 |

(\( t_{2\%} \approx 4J/D = 4\cdot 2H S_n/(\omega_0^2 D) \))

---

## 7 — El AVR virtual: control de tensión del VSM

### 7.1 — El lazo de tensión en la máquina síncrona real
En una máquina síncrona real el regulador automático de tensión (AVR) ajusta la corriente de
campo para mantener la tensión de bornes. El VSM debe reproducir este comportamiento para
controlar su FEM interna \( E \) y por tanto su intercambio de potencia reactiva.

### 7.2 — AVR virtual estático (droop Q-V)
La ley más simple es un droop reactivo:
$$ E = E_0 + k_q\,(Q_{set} - Q) $$
donde \( k_q \) [V/VAr] es la ganancia del droop reactivo y \( Q \) es la potencia reactiva
generada. En régimen permanente: \( Q_{ss} = Q_{set} + (E_{ss}-E_0)/k_q \). La caída de
tensión por pu de reactiva es \( \Delta E/Q = k_q \).

### 7.3 — AVR virtual dinámico (con filtro de primer orden)
Para suavizar la respuesta y limitar la dinámica:
$$ \tau_{avr}\,\dot E = -(E - E_0) + k_q\,(Q_{set} - Q) $$
Esta ODE tiene constante de tiempo \( \tau_{avr} \) [s]. En frecuencia:
$$ E(s) = E_0 + \frac{k_q}{\tau_{avr} s + 1}\,(Q_{set}(s) - Q(s)) $$

### 7.4 — Espacio de estados del VSM completo (P y Q)
El VSM completo (swing + AVR dinámico) tiene cuatro estados:

| Estado | Significado |
|:---|:---|
| \( \delta \) | ángulo de la FEM virtual |
| \( \omega \) | frecuencia angular virtual |
| \( E \) | amplitud de la FEM virtual |
| \( \varepsilon_q \) | integral del error reactivo (si hay integrador) |

Las ecuaciones de estado son:
$$ \dot\delta = \omega - \omega_0 $$
$$ J\,\dot\omega = \frac{P_{set} - P}{\omega_0} - D\,(\omega - \omega_0) $$
$$ \tau_{avr}\,\dot E = -(E - E_0) + k_q\,(Q_{set} - Q) $$

### 7.5 — Desacoplamiento P-Q e impedancia virtual
En una línea predominantemente **inductiva**, la potencia activa depende principalmente del
ángulo \( \delta \) y la potencia reactiva de la tensión \( E \):
$$ P \approx \frac{EV}{X}\sin\delta \approx \frac{EV}{X}\,\delta, \qquad Q \approx \frac{E^2 - EV\cos\delta}{X} \approx \frac{E(E-V)}{X} $$
El desacoplamiento es bueno si \( X \gg R \). En redes con baja relación X/R (baja tensión),
se añade una **impedancia virtual** \( X_{virt} \) en serie en el modelo del VSM para aumentar
la inductancia aparente y separar mejor los lazos P-Q:
$$ \mathbf{v}_{control} = \mathbf{e}_{vsm} - (R_{virt} + jX_{virt})\,\mathbf{i} $$
Esto mejora el desacoplamiento y la estabilidad del lazo de tensión sin modificar el hardware.

### 7.6 — Criterio de diseño del AVR
La dinámica del AVR debe ser más lenta que el lazo de corriente y más rápida que la dinámica
de la red:
$$ \tau_{corriente} \ll \tau_{avr} \ll \tau_{red} $$
Un criterio práctico: \( \tau_{avr} \approx 0.1\,\text{s} \), \( k_q \approx 0.05\text{–}0.1\,\text{V/VAr} \cdot S_n \).

---

## 8 — Diseño iterativo: de especificación de RoCoF a J y D

### 8.1 — Especificaciones de partida
| Especificación | Valor |
|:---|:---:|
| \( S_n \) | 1 MVA |
| Droop estacionario | 0.5 % |
| \( \Delta P_{diseño} \) | 10 % \( S_n \) = 100 kW |
| RoCoF máximo | 1 Hz/s |
| \( \zeta \) mínimo | 0.5 |
| \( K_s \) | 500 kW/rad |

### 8.2 — Paso 1: D por droop
El droop estacionario del 0.5 % fija directamente \( D \):
$$ D = \frac{S_n}{\text{droop}\cdot\omega_0^2} = \frac{10^6}{0.005\cdot(2\pi\cdot50)^2} = 2\,026\;\text{N·m·s/rad} $$

### 8.3 — Paso 2: J mínimo por RoCoF
La especificación RoCoF \(\leq 1\,\text{Hz/s}\) ante \( \Delta P = 100\,\text{kW}\):
$$ |\text{RoCoF}| = \frac{\Delta P}{J\,\omega_0\cdot 2\pi} \leq 1\;\text{Hz/s} $$
$$ J \geq \frac{\Delta P}{\omega_0\cdot(2\pi\cdot1)} = \frac{10^5}{2\pi\cdot50\cdot 2\pi} \approx 25.3\;\text{kg·m}^2 $$
Convertido a \( H \):
$$ H = \frac{J\,\omega_0^2}{2\,S_n} = \frac{25.3\cdot(2\pi\cdot50)^2}{2\cdot10^6} \approx 1.25\;\text{s} $$

### 8.4 — Paso 3: verificación de \( \zeta \)
Con \( J_{min} = 25.3\,\text{kg·m}^2 \) (\( H = 1.25\,\text{s} \)):
$$ \zeta = \frac{D}{2}\sqrt{\frac{\omega_0}{J\,K_s}} = \frac{2026}{2}\sqrt{\frac{2\pi\cdot50}{25.3\cdot500\times10^3}} = 1013\cdot\sqrt{\frac{314.16}{1.265\times10^7}} = 1013\cdot0.00499 = 5.05 $$
\( \zeta = 5.05 \gg 0.5 \): la especificación de amortiguamiento se cumple con holgura.

### 8.5 — Iteración completa

| Iteración | \( J \) [kg·m²] | \( H \) [s] | RoCoF [Hz/s] | \( \omega_n \) [rad/s] | \( \zeta \) | RoCoF ✓ | \( \zeta \) ✓ |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| It. 0 (mínimo) | 25.3 | 1.25 | 1.00 | 5.60 | 5.05 | ✓ | ✓ |
| It. 1 (H=2 s) | 40.5 | 2.00 | 0.63 | 4.42 | 4.00 | ✓ | ✓ |
| It. 2 (H=4 s) | 80.9 | 4.00 | 0.31 | 3.13 | 2.83 | ✓ | ✓ |
| It. 3 (H=10 s) | 202.4 | 10.0 | 0.13 | 1.97 | 1.79 | ✓ | ✓ |

**Resultado del diseño:** Con droop 0.5 % el mínimo \( J \) lo fija el RoCoF, no el
amortiguamiento (el modo siempre es sobre-amortiguado). Se elige **\( H = 4\,\text{s} \)** como
compromiso entre soporte inercial (\( \text{RoCoF} = 0.31\,\text{Hz/s} \)) y velocidad de
respuesta (\( \omega_n = 3.1\,\text{rad/s}\approx0.5\,\text{Hz} \)).

### 8.6 — Caso con droop más restrictivo
Si el droop se ajusta al 0.1 % (red con alta rigidez de tensión), entonces:
$$ D = \frac{10^6}{0.001\cdot(2\pi\cdot50)^2} = 10\,133\;\text{N·m·s/rad} $$
y para \( H = 4\,\text{s} \): \( \zeta = 14.1 \) — completamente sobre-amortiguado.
En este extremo, el VSM se comporta prácticamente como un integrador de potencia (sin
oscilaciones), y el nadir se alcanza muy lentamente.

### 8.7 — Flujo de diseño resumido
1. **Droop:** \( D = S_n / (\text{droop}\cdot\omega_0^2) \)
2. **Inercia mínima** por límite de RoCoF: \( J_{min} = \Delta P_{max} / (2\pi\,\text{RoCoF}_{max}\,\omega_0) \), con \( H_{min} = J_{min}\,\omega_0^2/(2 S_n) \)
3. **Verificar amortiguamiento:** \( \zeta = D/\big(2\sqrt{J K_s/\omega_0}\big) \ge 0.5 \). Si \( \zeta < 0.5 \): reducir \( J \) (subir \( \omega_n \)) o añadir \( D_{extra} \)
4. **Verificar ancho de banda:** \( \omega_n = \sqrt{K_s/(J\,\omega_0)} \ge \) banda deseada
5. **Elegir** \( H \in [H_{min},\,10\,\text{s}] \): compromiso RoCoF vs velocidad
6. **AVR virtual:** \( \tau_{avr},\ k_q \) por droop Q-V y dinámica del lazo de corriente

---

## Figuras de análisis extendido

<div class="cfig"><img src="figuras/vsm-inercia-analisis.png" alt="VSM analisis extendido: 4 paneles"><div class="cap">
(a) Respuesta de frecuencia ante escalón ΔP=200 kW para droop puro y VSM con H=1, 4, 10 s — el nadir estacionario es el mismo (−0.30 Hz), el triángulo marca el nadir instantáneo de cada curva.
(b) Mapa de autovalores del modo de potencia en el plano s al barrer H de 0.3 a 12 s con D fijado por droop 0.5 %; los puntos en el eje real corresponden al régimen sobre-amortiguado (H pequeño), la rama compleja aparece para H más alto; las líneas marcan ζ=0.7 y ζ=0.5.
(c) Mapa de contornos ζ(H,D): el color indica el amortiguamiento; la línea roja vertical es D fijado por el droop 0.5 %; a su derecha siempre ζ&gt;1 en este rango de H.
(d) Comparativa de la constante H por tecnología: el VSM puede igualar o superar la inercia de máquinas reales ajustando solo un parámetro software.
</div></div>

---

## Cuándo y por qué se usa
El VSM es preferible al droop cuando:
- La red tiene **bajo SCR** (red débil) y se necesita soporte inercial explícito.
- El pliego de condiciones exige un **RoCoF** máximo ante perturbaciones.
- Se quiere emular el comportamiento de una máquina síncrona real para integración en
  redes con requisitos de grid code (UK GC, ENTSO-E NC RfG).
- Se desea **ajustar dinámicamente** \( J \) y \( D \) en función del estado de la red
  (inercia adaptativa).

El droop puro es suficiente cuando solo se busca reparto estacionario de carga sin
requisitos de RoCoF ni integración en grid codes con exigencias de inercia.

---

## Procedimiento de diseño (genérico)
1. **D por droop:** \( D = 1/(\omega_0\,m_p) = S_n/(\text{droop}\cdot\omega_0^2) \).
2. **J por RoCoF:** \( J \geq \Delta P_{max}/(\omega_0\cdot 2\pi\cdot\text{RoCoF}_{max}) \).
3. **Verificar \( \zeta \):** \( \zeta = D/(2\sqrt{J\,K_s/\omega_0}) \). Si \( \zeta < 0.5 \),
   reducir \( J \) o añadir \( D_{extra} \) en lazo derivativo.
4. **Verificar \( \omega_n \):** \( \omega_n = \sqrt{K_s/(J\,\omega_0)} \). Asegurarse de que
   es mayor que la banda de perturbaciones relevante.
5. **AVR virtual:** elegir \( k_q \) y \( \tau_{avr} \) por droop reactivo deseado.

---

## Ejemplo de código
```python
# Parámetros
Sn   = 1e6          # VA
w0   = 2*np.pi*50   # rad/s
H    = 4.0          # s — constante de inercia
droop = 0.005       # 0.5 %
Ks   = 500e3        # W/rad (rigidez sincronizante)

# Parametros del VSM
J = 2*H*Sn / w0**2          # kg·m²
D = Sn / (droop * w0**2)    # N·m·s/rad

# Verificacion
wn   = np.sqrt(Ks / (J * w0))
zeta = D / (2 * np.sqrt(J * Ks / w0))
RoCoF_at_10pct = 0.1*Sn / (J * w0 * 2*np.pi)  # Hz/s

print(f"J = {J:.1f} kg·m²,  D = {D:.0f} N·m·s/rad")
print(f"ωn = {wn:.2f} rad/s ({wn/(2*np.pi):.3f} Hz),  ζ = {zeta:.2f}")
print(f"RoCoF (10%Sn) = {RoCoF_at_10pct:.2f} Hz/s")

# Integracion numerica (Euler explicito, dt pequeño)
def vsm_step(omega, delta, Pset, P_elec, dt):
    domega = ((Pset - P_elec)/w0 - D*(omega - w0)) / J
    ddelta = omega - w0
    return omega + domega*dt, delta + ddelta*dt
```

---

## Parámetros y valores típicos
| Parámetro | Símbolo | Rango típico | Unidad |
|:---|:---:|:---:|:---:|
| Constante de inercia | \( H \) | 2–10 | s |
| Inercia virtual | \( J = 2HS_n/\omega_0^2 \) | 25–1270 (para 1 MVA) | kg·m² |
| Amortiguamiento | \( D = 1/(\omega_0 m_p) \) | 500–5000 | N·m·s/rad |
| Droop equivalente | \( m_p = 1/(\omega_0 D) \) | 0.3–2 | % |
| Rigidez sincronizante | \( K_s \) | 100 kW–5 MW per rad | W/rad |
| Ganancia AVR virtual | \( k_q \) | 0.01–0.1 | pu/pu |
| Constante de tiempo AVR | \( \tau_{avr} \) | 0.05–0.2 | s |

---

## Errores comunes
- **\( J \) grande sin \( K_s \) suficiente:** \( \omega_n \) cae, la sincronización con la
  red se vuelve muy lenta y el sistema puede perder estabilidad transitoria ante grandes
  perturbaciones.
- **Olvidar el AVR:** un VSM sin lazo de tensión solo controla \( P \); la tensión se
  regula por el lazo externo (si existe) o queda a la deriva.
- **Usar \( D \) muy bajo** para aumentar \( \zeta \) y acelerar la respuesta: esto implica
  un droop muy alto y mala regulación de frecuencia en estado permanente.
- **Escalar \( J \) sin relimitar la corriente:** el VSM puede demandar corrientes altas
  durante transitorios largos; el limitador de corriente [[current-limiting]] debe estar activo.
- **Olvidar que \( K_s \) varía con el punto de operación:** en red débil \( K_s \) cae
  (menor margen de estabilidad transitoria), lo que puede hacer que \( \omega_n \) baje hasta
  valores muy bajos o que el sistema sea inestable.

---

## Uso en proyectos
- **01 - GFM-Impedance:** comparación VSM (H=4 s) vs droop puro ante escalón de potencia.
  El VSM suaviza el RoCoF (−1.25 Hz/s frente a salto instantáneo del droop).
  Implementado en `simulate.py`.
- **03 - Energia-DataCenter-IA:** el VSM actúa como generador virtual en la microrred híbrida
  AC+DC para sostener la frecuencia ante variaciones rápidas de carga de los servidores.

---

## Conceptos relacionados
- [[droop-control]] · [[grid-forming-vs-following]] · [[analisis-modal]]
- [[filtro-lcl]] (el LCL es la interfaz de red del VSM)
- [[control-cascada]] (el lazo de corriente es el lazo interno del VSM)

---

## Referencias
- Zhong, Weiss, *Synchronverters: Inverters That Mimic Synchronous Generators*, IEEE TIE 2011.
- Beck, Hesse, *Virtual synchronous machine*, EPQU 2007.
- Van Wesenbeeck et al., *Grid interaction of a virtual synchronous machine*, IET RPG 2009.
- D'Arco, Suul, *Virtual synchronous machines — classification of implementations and analysis
  of equivalence to droop controllers for microgrids*, IEEE Ind. Electron. 2014.
