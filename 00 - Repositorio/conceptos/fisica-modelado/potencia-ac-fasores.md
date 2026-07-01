---
titulo: Potencia en AC y fasores (P, Q, S)
slug: potencia-ac-fasores
categoria: fisica-modelado
tipo: concepto
nivel: basico
proyectos: []
objetivos: [entender potencia activa, reactiva y aparente, el uso de fasores, la compensacion de reactiva y la conexion con el control en dq]
tags: [potencia, activa, reactiva, aparente, fasores, RMS, compensacion, dq, basico]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [potencia-instantanea-dq, marco-dq, droop-control, sistema-trifasico]
referencias:
  - "Irwin, Análisis Básico de Circuitos en Ingeniería"
  - "Mohan, Undeland, Robbins, Power Electronics, Wiley 2003"
---

## Definición
En corriente alterna senoidal, la potencia se descompone en **activa** \( P \) (la que hace
trabajo útil, en W), **reactiva** \( Q \) (la que oscila entre fuente y campos, en var) y
**aparente** \( S \) (el producto de tensión y corriente eficaces, en VA). Los **fasores**
representan magnitudes senoidales como números complejos para operar con ellas fácilmente.

## Fundamento teórico
Un fasor codifica amplitud y fase: \( v(t)=\hat V\cos(\omega t+\theta)\to \bar V=\tfrac{\hat V}{\sqrt2}\,e^{j\theta} \)
(valor **eficaz/RMS** \( =\hat V/\sqrt2 \)). Con tensión y corriente eficaces \( V, I \) y desfase
\( \varphi \) entre ellas:
$$ P = VI\cos\varphi, \qquad Q = VI\sin\varphi, \qquad S = VI = \sqrt{P^2+Q^2} $$
La **potencia compleja** es \( \bar S = \bar V\,\bar I^{*} = P + jQ \). El **factor de potencia**
es \( \cos\varphi = P/S \). Una carga inductiva absorbe \( Q>0 \); una capacitiva, \( Q<0 \).
En trifásico equilibrado, \( P=3\,V_{fase}I_{fase}\cos\varphi=\sqrt3\,V_{LL}I_L\cos\varphi \).

<div class="cfig"><img src="figuras/potencia-ac-fasores-triangulo.png" alt="triangulo de potencia"><div class="cap">Triángulo de potencia: la activa P y la reactiva Q son los catetos, la aparente S la hipotenusa, y el factor de potencia es cos φ = P/S.</div></div>

## 1 — De dónde salen \( P=VI\cos\varphi \) y \( Q=VI\sin\varphi \)
**Paso 1 — partir de la potencia compleja.** Define los fasores **eficaces** \( \bar V=V\,e^{j\theta_v} \), \( \bar I=I\,e^{j\theta_i} \). La potencia compleja se define con el conjugado de la corriente (así el ángulo resultante es el desfase \( \varphi=\theta_v-\theta_i \), no la suma):

$$ \bar S=\bar V\,\bar I^{*}=\big(V\,e^{j\theta_v}\big)\big(I\,e^{-j\theta_i}\big)=VI\,e^{j(\theta_v-\theta_i)}=VI\,e^{j\varphi} $$

**Paso 2 — pasar a forma binómica.** Con la fórmula de Euler \( e^{j\varphi}=\cos\varphi+j\sin\varphi \):

$$ \bar S=VI\cos\varphi+j\,VI\sin\varphi $$

**Paso 3 — identificar partes real e imaginaria.** Por definición \( \bar S=P+jQ \). Igualando componente a componente:

$$ \boxed{\;P=\mathrm{Re}\,\bar S=VI\cos\varphi,\qquad Q=\mathrm{Im}\,\bar S=VI\sin\varphi\;} $$

y el módulo \( S=|\bar S|=VI=\sqrt{P^2+Q^2} \) es la hipotenusa del triángulo de la figura. El **factor de potencia** es \( \cos\varphi=P/S \): la fracción de la aparente que hace trabajo. El uso del conjugado garantiza el signo correcto de \( Q \): carga inductiva (corriente retrasada, \( \theta_i<\theta_v \), \( \varphi>0 \)) da \( Q>0 \).

## 2 — Por qué la media de \( v(t)\,i(t) \) coincide con \( VI\cos\varphi \)
**Paso 1 — potencia instantánea.** Con \( v=\sqrt2\,V\cos\omega t \) e \( i=\sqrt2\,I\cos(\omega t-\varphi) \) (amplitud de pico \( =\sqrt2\times \) RMS):

$$ p(t)=v\,i=2VI\cos\omega t\,\cos(\omega t-\varphi) $$

**Paso 2 — producto de cosenos a suma.** Con \( \cos A\cos B=\tfrac12[\cos(A-B)+\cos(A+B)] \):

$$ p(t)=2VI\cdot\frac12\big[\cos\varphi+\cos(2\omega t-\varphi)\big]=\underbrace{VI\cos\varphi}_{\text{media}}+\underbrace{VI\cos(2\omega t-\varphi)}_{\text{pulsa a }2\omega} $$

**Paso 3 — promediar.** El término \( \cos(2\omega t-\varphi) \) promedia cero sobre un periodo; queda \( \langle p\rangle=VI\cos\varphi=P \). Esto reconcilia la definición fasorial del apartado 1 con la potencia instantánea: el \( 2 \) del pico cancela el \( \tfrac12 \) del producto de cosenos. (En trifásico equilibrado las tres pulsaciones de \( 2\omega \) se cancelan entre sí y la potencia total es constante: ver [[sistema-trifasico]] y [[potencia-instantanea-dq]].)

## 3 — El triángulo de potencia y la compensación de reactiva

### Por qué Q no hace trabajo pero sí circula
La reactiva \( Q \) corresponde a la componente de la corriente en cuadratura con la tensión. Esa corriente carga y descarga los campos magnéticos (inductancias) y eléctricos (condensadores) alternativamente: durante un semiciclo fluye energía de la fuente hacia el campo; durante el siguiente semiciclo la energía regresa. El balance neto por ciclo completo es cero — no se disipa trabajo. Pero la corriente **sí existe físicamente** en el conductor; las pérdidas Joule son \( R\,I^2 \), proporcionales al cuadrado de la corriente total (no solo a la activa). Una carga inductiva fuerza a la fuente a suministrar corriente reactiva adicional, elevando la corriente de línea y las pérdidas, aunque la potencia activa entregada no cambie.

### Compensación con condensadores
Un condensador conectado en paralelo con la carga inductiva genera reactiva negativa \( Q_C = -\omega C V_f^2 \) (por fase), compensando la positiva del inductor. La reactiva total se reduce sin tocar la carga activa:
$$ Q_{compensada} = Q_{inductiva} + Q_C = Q_{inductiva} - \omega C V_f^2 $$

La capacitancia necesaria para compensar de \( Q_1 \) a \( Q_2 \) en una red en estrella (Y) con tensión de fase \( V_f \):
$$ \boxed{C_{nec} = \frac{Q_1 - Q_2}{\omega\,V_f^2}} \quad [\text{por fase}] $$

Con la reactiva reducida, la corriente de línea baja de \( I_{L,1}=S_1/(\sqrt3\,V_{LL}) \) a \( I_{L,2}=S_2/(\sqrt3\,V_{LL}) \) y las pérdidas en la impedancia de la red caen proporcionalmente a \( I^2 \).

### Por qué no compensar hasta cos(φ) = 1
Con compensación perfecta \( Q_{total}=0 \), la admitancia del paralelo C-carga tiene una resonancia paralelo precisamente a la frecuencia de la red. Cualquier armónico o transitorio cerca de esa frecuencia puede excitar la resonancia y producir sobretensiones. En la práctica se deja un margen: cos(φ) objetivo ≈ 0.95–0.98, no 1.0.

## 4 — La potencia instantánea completa: activa, reactiva y fluctuante

La expansión del Apartado 2 se puede escribir de forma más reveladora expandiendo el coseno doble:

$$ p(t) = V I\cos\varphi + V I\cos(2\omega t-\varphi) $$

Expandiendo el segundo término con \( \cos(A-B)=\cos A\cos B+\sin A\sin B \):

$$ p(t) = P + P\cos(2\omega t) + Q\sin(2\omega t) $$

donde \( P=VI\cos\varphi \) y \( Q=VI\sin\varphi \). Interpretación de cada término:

- **\( P \)**: la media constante, el único trabajo neto. Es la potencia activa.
- **\( P\cos(2\omega t) \)**: la componente pulsante de la activa. Oscila entre \( +P \) y \( -P \) a frecuencia \( 2\omega \). Durante el semiciclo positivo, la fuente entrega; durante el negativo, la carga devuelve energía cinética (a la red, al volante de una máquina, etc.). El valor medio es cero.
- **\( Q\sin(2\omega t) \)**: la componente reactiva pulsante. Oscila entre \( +Q \) y \( -Q \) a \( 2\omega \). Representa la energía que entra y sale de los campos magnéticos y eléctricos; su media también es cero.

### En trifásico equilibrado: las pulsaciones se cancelan
Para la fase B la tensión y corriente van desfasadas \( 120° \) respecto a la fase A; para la C, \( 240° \). Al sumar \( p_a+p_b+p_c \):
- La suma de tres cosenos (o senos) a \( 2\omega \) desfasados \( 120° \) entre sí es exactamente cero para cualquier instante \( t \).
- Queda solo \( p_{total}=3P=\) constante.

Esto explica por qué los sistemas trifásicos son preferibles: la potencia instantánea total es constante, sin pulsaciones, lo que reduce las vibraciones en motores y simplifica el control de convertidores (ver [[potencia-instantanea-dq]]).

## 5 — El fasor en el plano complejo: rotación, proyección y régimen permanente

### El fasor como vector giratorio
Una tensión senoidal \( v(t)=\hat V\cos(\omega t+\theta) \) se puede escribir como la parte real de un número complejo que gira:
$$ v(t)=\mathrm{Re}\!\left\{\hat V\,e^{j\theta}\cdot e^{j\omega t}\right\} $$

El **fasor** \( \bar V=\tfrac{\hat V}{\sqrt2}e^{j\theta} \) es la "fotografía" a \( t=0 \): captura amplitud (módulo) y desfase (argumento). Todos los fasores del circuito giran a la misma \( \omega \), por lo que en régimen permanente basta con el vector estático.

### Ley de Ohm fasorial
Para un inductor \( L \), la relación diferencial \( v_L=L\,di/dt \) en el dominio fasor (derivar = multiplicar por \( j\omega \)):
$$ \bar V_L = j\omega L\,\bar I \quad\Rightarrow\quad Z_L = j\omega L $$

Para una impedancia genérica \( Z=R+j\omega L \):
$$ \bar V = Z\,\bar I \quad\Rightarrow\quad |\bar I|=\frac{|\bar V|}{|Z|},\quad \varphi=-\arctan\!\left(\frac{\omega L}{R}\right) $$

### Por qué usar RMS
Con fasores en valores eficaces (RMS), las fórmulas de potencia quedan limpias: \( P=\mathrm{Re}(\bar V\bar I^*)=VI\cos\varphi \) sin factores \( \tfrac12 \). Si se usaran amplitudes de pico \( \hat V,\hat I \), aparecería un \( \tfrac12 \) en todas las expresiones de potencia, ya que \( P=\tfrac12\hat V\hat I\cos\varphi \). El uso de RMS es la convención universal en análisis de circuitos de potencia.

### KVL y KCL funcionan en fasores
Las leyes de Kirchhoff son lineales: la suma de tensiones en un lazo es cero y la suma de corrientes en un nodo es cero. Como la transformación \( v(t)\to\bar V \) es lineal, KVL y KCL se preservan: la suma de fasores en un lazo es \( \bar 0 \), y en un nodo la suma es cero también. Esto es lo que permite resolver circuitos AC con álgebra compleja en lugar de ecuaciones diferenciales.

## 6 — Potencia en dq: la conexión con el control de convertidores

### Derivación del factor 3/2
La potencia trifásica instantánea total es \( p=v_a i_a+v_b i_b+v_c i_c \). Aplicando la transformación de Clarke (de abc a αβ, conservación de amplitud):
$$ \begin{bmatrix}\alpha\\\beta\end{bmatrix}=\frac{2}{3}\begin{bmatrix}1&-\frac12&-\frac12\\0&\frac{\sqrt3}{2}&-\frac{\sqrt3}{2}\end{bmatrix}\begin{bmatrix}a\\b\\c\end{bmatrix} $$

En sistema equilibrado sin homopolar, la potencia queda:
$$ p = \frac{3}{2}(v_\alpha i_\alpha + v_\beta i_\beta) $$

La rotación de Park de αβ a dq solo rota el plano — no cambia el producto escalar — así que:
$$ \boxed{P = \frac{3}{2}(v_d i_d + v_q i_q), \qquad Q = \frac{3}{2}(v_q i_d - v_d i_q)} $$

El factor \( \tfrac32 \) tiene el origen en el \( \tfrac23 \) de Clarke: transforma 3 magnitudes a 2 pero conserva la potencia, por lo que aparece ese factor.

### Con referencia dq alineada al vector de tensión
Si se alinea el eje d con la tensión de red (\( v_d=V_f \), \( v_q=0 \)):
$$ \boxed{P = \frac{3}{2}\,V_f\,i_d, \qquad Q = -\frac{3}{2}\,V_f\,i_q} $$

La potencia activa solo depende de \( i_d \) y la reactiva de \( i_q \). El control de P y Q se reduce a controlar dos corrientes independientes: el lazo de \( i_d \) regula la potencia activa (o la frecuencia en droop) y el de \( i_q \) regula la reactiva (o la tensión). Esta descomposición es la razón profunda por la que el marco dq simplifica el control de convertidores.

### Consignas de corriente del convertidor
Invirtiendo las expresiones:
$$ i_d^* = \frac{P^*\cdot(2/3)}{V_f}, \qquad i_q^* = \frac{-Q^*\cdot(2/3)}{V_f} $$

El convertidor inyecta la corriente activa y reactiva pedidas simplemente siguiendo estas referencias en el lazo de control.

## 7 — Diseño iterativo: compensación de reactiva y dimensionado del convertidor

### Datos de partida
Carga industrial trifásica: \( P=100\,\text{kW} \), \( \cos\varphi_1=0.70\) (inductivo), red 400 V L-L, 50 Hz.

### Paso 1 — estado inicial
$$ \tan\varphi_1 = \tan(\arccos0.70) = 1.020 \implies Q_1 = 100\,\text{kW}\times1.020 = 102\,\text{kVAr} $$
$$ S_1 = P/\cos\varphi_1 = 100/0.70 = 143\,\text{kVA}, \qquad I_{L,1} = S_1/(\sqrt3\times400) = 206\,\text{A} $$

### Paso 2 — objetivo de compensación
Objetivo: \( \cos\varphi_2=0.95 \). La reactiva objetivo:
$$ Q_2 = 100\times\tan(\arccos0.95) = 100\times0.329 = 32.9\,\text{kVAr} $$
Reactiva a compensar: \( \Delta Q = Q_1-Q_2 = 102-32.9 = 69.1\,\text{kVAr} \).

### Paso 3 — dimensionado del banco de condensadores
Tensión de fase: \( V_f = 400/\sqrt3 = 231\,\text{V} \). Capacitancia por fase (red en Y):
$$ C_{nec}=\frac{\Delta Q/3}{\omega\,V_f^2}=\frac{23030}{314.2\times231^2}=\frac{23030}{16\,775}=1.37\,\text{mF por fase} $$

La reactiva total del banco trifásico: \( Q_C = 3\,\omega C V_f^2 = 3\times314.2\times1.37\times10^{-3}\times231^2 = 69\,\text{kVAr} \). Comprobación: \( Q_1-Q_C=102-69=33\,\text{kVAr}\approx Q_2 \). ✓

### Paso 4 — verificación de corriente
$$ S_2 = \sqrt{P^2+Q_2^2} = \sqrt{100^2+32.9^2} = 105.3\,\text{kVA} $$
$$ I_{L,2} = S_2/(\sqrt3\times400) = 152\,\text{A} \qquad \text{(vs. 206 A inicial, reducción del 26 %)} $$

Las pérdidas Joule en la impedancia de red (proporcionales a \( I^2 \)) se reducen en \( 1-(152/206)^2 = 45\% \). Las pérdidas en la propia carga no cambian.

### Paso 5 — dimensionado del VSC en dq
Si se utiliza un convertidor VSC para suministrar la carga activa y compensar la reactiva restante:
$$ i_d^* = \frac{P^*\cdot(2/3)}{V_f} = \frac{100000\times0.667}{231} = 289\,\text{A (amplitud d-axis)} $$
$$ i_q^* = \frac{-Q_2^*\cdot(2/3)}{V_f} = \frac{-32900\times0.667}{231} = -95\,\text{A} $$

La corriente de pico del convertidor: \( \hat I=\sqrt{(289)^2+(95)^2}\times\sqrt{2}=433\,\text{A} \) (amplitud instantánea).

<div class="cfig"><img src="figuras/potencia-ac-fasores-analisis.png" alt="Analisis completo: potencia instantanea, triangulo compensacion, diagrama fasorial y control dq"><div class="cap">Panel (a): potencia instantánea p(t) con la componente media P y la fluctuante a 2ω. (b): triángulo de potencia antes y después de la compensación con condensadores. (c): diagrama fasorial con V, I y el ángulo φ. (d): linealidad P–id y Q–iq que permite el control desacoplado del convertidor.</div></div>

## Cuándo y por qué se usa
Es la base del análisis de sistemas de potencia: dimensionar equipos (por \( S \)), compensar
reactiva, y formular el control (el droop reparte \( P \) y \( Q \); ver
[[potencia-instantanea-dq]] para la versión instantánea en dq).

## Procedimiento (genérico)
1. Expresa tensiones y corrientes como fasores eficaces.
2. Calcula \( \bar S=\bar V\bar I^{*} \); separa \( P=\mathrm{Re}\,\bar S \), \( Q=\mathrm{Im}\,\bar S \).
3. Obtén \( S=|\bar S| \) y el factor de potencia \( P/S \).
4. Para compensar: calcula \( C_{nec}=(Q_1-Q_2)/(3\omega V_f^2) \) por fase en Y.
5. Para el convertidor en dq: \( i_d^*=P^*(2/3)/V_f \), \( i_q^*=-Q^*(2/3)/V_f \).

## Ejemplo de código
```python
import numpy as np
V = 230*np.exp(1j*0); I = 10*np.exp(-1j*np.deg2rad(30))   # fasores eficaces
S = V*np.conj(I); P, Q = S.real, S.imag; FP = P/abs(S)

# Compensación
w, Vf = 2*np.pi*50, 230.0
Q_target = P*np.tan(np.arccos(0.95))
C_nec = (Q - Q_target) / (w * Vf**2)  # F por fase en Y

# Control dq (factor 3/2 con convención amplitud-invariante)
id_star = P * (2/3) / Vf
iq_star = -Q_target * (2/3) / Vf
```

## Parámetros y valores típicos
Factor de potencia objetivo: 0.95–0.98 (no 1.0, riesgo de resonancia). Convenio de signo de \( Q \): positivo = inductivo (absorbe reactiva). Factor \( \tfrac32 \) con convención amplitud-invariante de Park; con potencia-invariante el factor sería 1.

## Errores comunes
- Mezclar valores de pico y eficaces (RMS) en las fórmulas de potencia.
- Olvidar el factor \( \sqrt3 \) o el 3 en trifásico.
- Compensar exactamente a cos(φ)=1 y generar resonancia con la red.
- Usar el factor \( \tfrac32 \) incorrecto (depende de la convención de Clarke/Park utilizada).

## Conceptos relacionados
- [[potencia-instantanea-dq]] · [[marco-dq]] · [[droop-control]] · [[sistema-trifasico]]

## Referencias
- Irwin, *Análisis Básico de Circuitos en Ingeniería*.
- Mohan, Undeland, Robbins, *Power Electronics*, Wiley 2003.
