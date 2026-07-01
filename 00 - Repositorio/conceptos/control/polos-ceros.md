---
titulo: Polos y ceros
slug: polos-ceros
categoria: control
tipo: concepto
nivel: basico
proyectos: [01-gfm-impedance]
objetivos: [interpretar la dinamica y la estabilidad a partir de los polos y ceros, disenar con el lugar de las raices, entender los limites que imponen los ceros RHP]
tags: [polos, ceros, estabilidad, plano-s, lugar-raices, sensibilidad, fase-no-minima, basico]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [funcion-transferencia, sistema-primer-orden, respuesta-segundo-orden, estabilidad-bibo, analisis-modal, margenes-estabilidad]
referencias:
  - "Franklin, Powell, Feedback Control of Dynamic Systems, Pearson"
  - "Ogata, Ingeniería de Control Moderna, Pearson"
  - "Skogestad, Postlethwaite, Multivariable Feedback Control, Wiley"
---

## Definición
Los **polos** son las raíces del denominador de la función de transferencia (la ecuación
característica); los **ceros**, las del numerador. Los polos determinan la **forma** de la
respuesta y la **estabilidad**; los ceros, cómo se ponderan los modos.

## Fundamento teórico
Cada polo \( p=\sigma+j\omega \) aporta un modo \( e^{\sigma t}(\cos\omega t,\sin\omega t) \):
- \( \sigma<0 \) (semiplano **izquierdo**): el modo **decae** → contribuye a la estabilidad.
- \( \sigma>0 \) (semiplano derecho): el modo **crece** → inestable.
- \( \omega\neq 0 \): el modo **oscila** a esa frecuencia.
La distancia al origen marca la rapidez; el ángulo respecto al eje real, el amortiguamiento
\( \zeta=-\sigma/|p| \). Un sistema lineal es **estable** si y solo si **todos** sus polos están
en el semiplano izquierdo. Los ceros no afectan a la estabilidad, pero un **cero en el semiplano
derecho** (fase no mínima) produce respuesta inicial en sentido contrario y limita el control.

<div class="cfig"><img src="figuras/polos-ceros-splano.png" alt="mapa de polos y ceros en el plano s"><div class="cap">Mapa polo-cero: todos los polos en el semiplano izquierdo ⇒ estable. La distancia al origen da la rapidez y el ángulo θ el amortiguamiento (ζ=cos θ). Los ceros (○) no afectan a la estabilidad.</div></div>

## 1 — Respuesta de un polo real: decaimiento e^{-at}

**Paso 1 — función de transferencia con un polo real.** Sea \( G(s)=K/(s+a) \) con \( a>0 \). La respuesta al impulso es la antitransformada de Laplace de \( G(s) \):

$$ \mathcal{L}^{-1}\!\left\{\frac{K}{s+a}\right\} = K\,e^{-at}\,\mathbf{1}(t) $$

**Paso 2 — interpretar el polo.** El polo está en \( s=-a \): parte real \( \sigma=-a<0 \) (semiplano izquierdo). La respuesta es un exponencial que **decae** con constante de tiempo \( \tau=1/a \): en \( t=\tau \) la amplitud cae al 37%; en \( t=5\tau \) es prácticamente cero. Cuanto más negativo el polo (mayor \( a \)), más rápido el decaimiento.

$$ \boxed{g(t)=K\,e^{-at},\quad \tau=\frac{1}{a}=-\frac{1}{\mathrm{Re}(p)}} $$

## 2 — Par complejo conjugado: oscilación amortiguada y cero en RHP

**Paso 1 — polos complejos conjugados.** Sea \( G(s)=\omega_n^2/\bigl[(s+\sigma)^2+\omega_d^2\bigr] \) con \( \sigma=\zeta\omega_n>0 \) y \( \omega_d=\omega_n\sqrt{1-\zeta^2} \). Los polos son \( s=-\sigma\pm j\omega_d \). La respuesta al impulso es:

$$ g(t)=\omega_n\,e^{-\sigma t}\frac{\sin(\omega_d t)}{\sqrt{1-\zeta^2}}\,\mathbf{1}(t) $$

**Paso 2 — leer la geometría del plano s.** La parte imaginaria \( \pm\omega_d \) da la frecuencia de oscilación; la parte real \( -\sigma \) da la tasa de decaimiento de la envolvente \( e^{-\sigma t} \). El módulo del polo es \( |p|=\omega_n \) y el ángulo respecto al eje real negativo cumple \( \cos\theta=\zeta \).

**Paso 3 — cero en el semiplano derecho (RHP).** Si \( G(s) \) tiene un cero en \( z=+b \) (\( b>0 \)), el factor \( (s-b) \) en el numerador produce un **signo negativo** en la respuesta para \( t\to0^+ \): la salida comienza moviéndose en dirección **contraria** a la entrada antes de girar. Esto es la **respuesta de fase no mínima**. Se verifica directamente: la antitransformada de \( (s-b)/[(s+a)(s+c)] \) tiene coeficiente de residuo negativo en la parte que corresponde al arranque.

$$ \boxed{z\in\mathrm{RHP}\;\Rightarrow\;\text{respuesta inversa inicial, margen de fase limitado}} $$

## 3 — El lugar de las raíces: cómo se mueven los polos con la ganancia

### 3.1 — El problema del diseño en lazo cerrado

Al cerrar el lazo con ganancia \( K \), los polos del sistema realimentado ya no son los de la planta \( G(s) \). Son las raíces del polinomio característico:

$$1 + K\,G(s) = 0 \;\Leftrightarrow\; T(s) = \frac{KG(s)}{1+KG(s)}: \quad \text{denom.} = 1 + KG(s)$$

Conforme \( K \) varía de 0 a \( \infty \), los polos de \( T(s) \) recorren trayectorias en el plano \( s \) que forman el **lugar de las raíces**.

### 3.2 — Valores extremos de K

**En \( K = 0 \):** \( 1 + 0 \cdot G(s) = 0 \) se reduce a \( 1 = 0 \): sin solución finita. Por continuidad, los polos de \( T \) parten desde los **polos de \( G \)** (donde \( G \to \infty \)).

**En \( K \to \infty \):** \( 1 + KG(s) = 0 \;\Rightarrow\; G(s) = -1/K \to 0 \). Los polos de \( T \) convergen a los **ceros de \( G \)**. Si \( G \) tiene menos ceros que polos (orden relativo \( n-m > 0 \)), los \( n-m \) polos restantes van a infinito por las **asíntotas**.

### 3.3 — Reglas del lugar de las raíces

Para \( G(s) = N(s)/D(s) \) con \( n \) polos y \( m \) ceros:

**Regla 1 — número de ramas:** el lugar tiene \( n \) ramas (una por polo de \( G \)).

**Regla 2 — origen y destino:** cada rama parte de un polo de \( G \) (\( K=0 \)) y termina en un cero de \( G \) o en \( \infty \) (\( K\to\infty \)).

**Regla 3 — simetría:** el lugar es simétrico respecto al eje real (los coeficientes de los polinomios son reales).

**Regla 4 — asíntotas:** las \( n-m \) ramas que van a \( \infty \) siguen asíntotas con ángulo:

$$\phi_k = \frac{(2k+1)\cdot 180°}{n-m}, \quad k = 0, 1, \dots, (n-m-1)$$

que parten del centroide:

$$\sigma_c = \frac{\sum\text{polos de }G - \sum\text{ceros de }G}{n-m}$$

### 3.4 — Ejemplo: G(s) = K/[s(s+2)(s+4)]

Tres polos: \( s=0 \), \( s=-2 \), \( s=-4 \). Sin ceros finitos (\( m=0 \), \( n=3 \)).

**Centroide:** \( \sigma_c = (0-2-4)/3 = -2 \).

**Asíntotas:** ángulos \( 60°, 180°, 300° \) partiendo de \( \sigma_c = -2 \).

**Punto de ruptura en el eje real:** donde el lugar abandona el eje real. Se busca imponiendo \( dK/ds = 0 \). Aquí el lugar ocupa el eje real entre \( s=0 \) y \( s=-2 \), y también desde \( s=-4 \) a \( -\infty \); el punto de ruptura entre \( 0 \) y \( -2 \) ocurre aproximadamente en \( s \approx -0.85 \).

**Encontrar K para ζ = 0.7:** los polos con \( \zeta = 0.7 \) cumplen \( \sigma/|p| = 0.7 \). La condición de módulo \( |KG(j\omega)| = 1 \) en el punto \( s=-\sigma \pm j\omega_d \) del lugar da \( K \approx 3.5 \).

### 3.5 — Cómo se usa en diseño

El lugar de las raíces responde a la pregunta: ¿dónde van a caer los polos de lazo cerrado si aumento la ganancia? Permite:
- Ver si el sistema puede volverse inestable al aumentar \( K \) (las ramas cruzan el eje imaginario).
- Elegir \( K \) para un \( \zeta \) dado (encontrar el punto del lugar con el ángulo correcto desde el origen).
- Colocar un compensador (polo/cero adicional) que doble el lugar hacia una región deseada del plano \( s \).

## 4 — Polos dominantes y la aproximación de orden reducido

### 4.1 — El concepto de polo dominante

En un sistema con múltiples polos, los modos asociados a polos con parte real muy negativa (lejos del eje imaginario) decaen mucho más rápido que los modos asociados a polos cercanos al eje. A efectos prácticos, solo los polos **más lentos** —los **polos dominantes**— determinan el comportamiento observable en el transitorio.

**Criterio cuantitativo:** un polo en \( s=-\sigma_2 \) es dominado por el polo en \( s=-\sigma_1 \) si:

$$\sigma_2 \geq 5\,\sigma_1 \;\Rightarrow\; \tau_2 = 1/\sigma_2 \leq \tau_1/5$$

El modo rápido decae en un tiempo 5 veces menor que el lento, por lo que en el transitorio del modo lento el modo rápido ya ha desaparecido.

### 4.2 — Reducción de orden

Si \( \sigma_2 \gg \sigma_1 \), se puede aproximar la función de transferencia eliminando el polo rápido. Para una planta de segundo orden:

$$G(s) = \frac{K}{(s+\sigma_1)(s+\sigma_2)} \approx \frac{K/\sigma_2}{s+\sigma_1} = \frac{K'}{s+\sigma_1}, \quad K' = K/\sigma_2$$

La ganancia DC se conserva: \( G(0) = K/(\sigma_1\sigma_2) \) antes y \( K'/\sigma_1 = K/(\sigma_2\sigma_1) \) después.

**Error de la aproximación:** en el transitorio inicial (para \( t < 1/\sigma_2 \)) la diferencia puede ser notable porque el modo rápido aún existe. A largo plazo la aproximación es buena. Si se necesita precisión en el transitorio rápido, la reducción de orden no es válida.

### 4.3 — Ejemplo: proyecto 01 GFM

El sistema GFM linealizado tiene polos en tres rangos de frecuencia bien separados:

| Modo | Polo típico | Frecuencia | Origen |
|---|---|---|---|
| Potencia | \( -8.3 \pm j21\,\text{rad/s} \) | 3.3 Hz | lazo de potencia droop |
| Corriente | \( \approx -2\pi\cdot1000\,\text{rad/s} \) | 1 kHz | PI de corriente |
| LCL | \( \approx -2\pi\cdot1450\,\text{rad/s} \) | 1450 Hz | resonancia LCL |

El modo de potencia a 3.3 Hz es el **polo dominante**: determina la respuesta dinámica del intercambio de potencia activa. Los modos de corriente y LCL son 300 veces más rápidos y se pueden ignorar en el análisis del lazo de potencia. Esto justifica el uso de modelos reducidos para el diseño del droop y la impedancia virtual.

## 5 — Ceros en el semiplano derecho: límites fundamentales del control

### 5.1 — Respuesta inversa: demostración

Sea \( G(s) = K(1 - s/z)/(s+a) \) con \( z > 0 \) (cero en el SPD). La respuesta al escalón por fracciones parciales:

$$Y(s) = G(s)\cdot\frac{1}{s} = \frac{K(1-s/z)}{s(s+a)} = \frac{A}{s} + \frac{B}{s+a}$$

Los residuos:
$$A = \left.\frac{K(1-s/z)}{s+a}\right|_{s=0} = \frac{K}{a}, \quad B = \left.\frac{K(1-s/z)}{s}\right|_{s=-a} = \frac{K(1+a/z)}{-a}$$

La respuesta temporal:

$$y(t) = \frac{K}{a}\left[1 - \left(1 + \frac{a}{z}\right)e^{-at}\right]$$

Para \( t \to 0^+ \): \( y(0^+) = K/a - K(1+a/z)/a = -K/z < 0 \). **La respuesta arranca en sentido negativo** aunque el escalón sea positivo. La velocidad inicial es:

$$\dot{y}(0^+) = K\cdot B\cdot(-a) = -K\left(1+\frac{a}{z}\right) < 0$$

### 5.2 — Límite en el ancho de banda de control

Un cero RHP en \( s=+z \) impone un techo al ancho de banda de cualquier controlador que estabilice el sistema. La demostración se basa en la función de sensibilidad complementaria \( T = 1-S \): para un sistema estable con cero RHP en \( z \), necesariamente:

$$|T(jz)| \geq 1 \;\Rightarrow\; \omega_c \lesssim z/2$$

Si el cruce de ganancia se sitúa por encima de \( z \), el margen de fase se degrada irrecuperablemente. La regla práctica conservadora es:

$$\boxed{\omega_c < \frac{z}{2}}$$

### 5.3 — El caso del convertidor buck en modo discontinuo

En el convertidor buck operando en modo discontinuo, la función de transferencia del inductor a la salida incluye un cero en:

$$z_{RHP} = \frac{R(1-D)^2}{L}$$

donde \( D \) es el ciclo de trabajo, \( R \) la carga y \( L \) la inductancia. Un aumento del ciclo de trabajo inicialmente reduce la corriente (respuesta inversa) antes de que el condensador de salida comience a cargarse. Para \( D=0.5 \), \( R=10\,\Omega \), \( L=100\,\mu\text{H} \): \( z_{RHP} = 10\cdot0.25/10^{-4} = 25\,\text{krad/s} = 3.98\,\text{kHz} \). El ancho de banda del control de tensión queda limitado a menos de 2 kHz, aunque la frecuencia de conmutación sea 100 kHz.

### 5.4 — El caso del STATCOM con desequilibrio

Bajo condiciones de desequilibrio de red, la matriz de impedancia en el marco \( dq \) incluye términos fuera de la diagonal que acoplan los ejes \( d \) y \( q \). Estos términos cruzados pueden producir ceros en el SPD en la función de transferencia de lazo, limitando el ancho de banda del control de corriente y requiriendo estrategias de desacoplo explícito o control en el marco de secuencia positiva/negativa.

### 5.5 — Consecuencia de diseño

El cero RHP establece un límite **fundamental** que no puede superarse con ningún regulador causal:
- Mayor agresividad (mayor \( K_p \)) no mejora sino empeora: fuerza el polo de lazo cerrado hacia el SPD.
- La solución es reducir la frecuencia del cero RHP cambiando el diseño del sistema (inductancia mayor, modo continuo, etc.) o aceptar un ancho de banda reducido.

## 6 — Sensibilidad del sistema a variación de parámetros: la función S

### 6.1 — Definición de la sensibilidad

La **función de sensibilidad** mide cuánto varía la ganancia de lazo cerrado \( T \) ante variaciones relativas de la planta \( G \):

$$S_T^G \triangleq \frac{\partial T/T}{\partial G/G}$$

Para el lazo de realimentación unitaria \( T = KG/(1+KG) \), derivando respecto a \( G \):

$$\frac{\partial T}{\partial G} = \frac{K(1+KG) - KG\cdot K}{(1+KG)^2} = \frac{K}{(1+KG)^2}$$

Dividiendo por \( T/G = K/(1+KG)^2\cdot(1+KG)/G = K/[(1+KG)G] \)... simplificando:

$$\boxed{S(s) = \frac{1}{1+K G(s)}}$$

Esta es la **función de sensibilidad de Bode**, que depende de la frecuencia. En el diseño en frecuencia se trabaja con \( |S(j\omega)| \).

### 6.2 — Interpretación física

- **\( |S(j\omega)| < 1 \) (SPI):** el lazo **atenúa** la influencia de perturbaciones que entran en la planta. Esto es lo que se quiere a frecuencias bajas.
- **\( |S(j\omega)| > 1 \):** el lazo **amplifica** las perturbaciones. Ocurre inevitablemente a frecuencias altas.
- **El pico de sensibilidad \( M_s = \max_\omega|S(j\omega)| \):** se relaciona con el margen de fase y de ganancia. Para un sistema bien diseñado: \( M_s < 2 \) (\( 6\,\text{dB} \)), lo que garantiza \( PM > 29° \) y \( GM > 6\,\text{dB} \).

También: \( S = 1 - T \) (con \( T = KG/(1+KG) \) la complementaria). La función de sensibilidad y su complementaria satisfacen \( S + T = 1 \): atenuar perturbaciones y seguir referencias son objetivos en tensión.

### 6.3 — La integral de Bode: no se puede ganar en toda la banda

Para un sistema de lazo cerrado estable con al menos dos polos más que ceros (**sin polos inestables de lazo abierto**), se cumple:

$$\int_0^\infty \ln\bigl|S(j\omega)\bigr|\,d\omega = 0$$

**Interpretación:** el área bajo la curva \( \ln|S(j\omega)| \) es nula. Si se fuerza \( |S| < 1 \) (atenuación) en una banda, la función debe compensar con \( |S| > 1 \) (amplificación) en otra. La reducción de sensibilidad a baja frecuencia siempre tiene un coste en alta frecuencia: el **water-bed effect** (Horowitz).

### 6.4 — Límites por polos y ceros RHP

Si el sistema en lazo abierto tiene un **polo inestable** en \( p \) (\( \text{Re}(p) > 0 \)):

$$\int_0^\infty \ln|S(j\omega)|\,d\omega \geq \pi\,\text{Re}(p)$$

El mínimo integral posible crece con la parte real del polo inestable. Un polo inestable más agresivo obliga a más amplificación de sensibilidad en algún rango de frecuencia.

Si hay un **cero RHP** en \( z \), la función complementaria \( T \) satisface \( |T(jz)| \geq 1 \) y la sensibilidad no puede hacerse pequeña para frecuencias superiores a \( z \). Ambos efectos se combinan y establecen los **límites fundamentales de rendimiento** del lazo de control.

### 6.5 — Relación con el margen de fase

El pico de sensibilidad \( M_s \) y el margen de fase \( PM \) están relacionados geométricamente: \( M_s \) es el inverso de la distancia mínima del diagrama de Nyquist al punto crítico \( (-1, 0j) \). Para \( M_s = 2 \):

$$PM = \arcsin\!\left(\frac{1}{2M_s}\right)\cdot 2 \approx 29°$$

Un margen de fase de \( 45°\text{–}60° \) (recomendado) garantiza \( M_s < 2 \).

## 7 — Análisis de polos del proyecto 01: de inestable a estable

### 7.1 — Modelo linealizado del GFM

El inversor grid-forming del proyecto 01 (50 MVA, 380 kV) se controla con droop de potencia activa. La linealización alrededor del punto de operación nominal produce un modelo de estados con \( A \in \mathbb{R}^{5\times5} \) (estados: \( \delta \), \( \omega \), \( P_m \), \( i_d \), \( i_q \)).

Los autovalores de \( A \) son los polos del sistema en lazo cerrado. El modo de potencia está determinado principalmente por el par de autovalores complejo conjugado asociado a \( [\delta, P_m] \).

### 7.2 — Configuración inicial: sistema inestable

Con los parámetros de diseño iniciales (\( m_p = 1.57\times10^{-3}\,\text{rad/s/W} \), \( \omega_f = 2\pi\cdot30\,\text{rad/s} \)):

$$\lambda_{pot}^{(0)} = +3.5 \pm j18\,\text{rad/s}$$

La parte real positiva confirma que el modo de potencia es **inestable**. La causa es que el filtro de potencia \( \omega_f \) es demasiado grande (30 Hz), lo que hace que la estimación de potencia sea demasiado rápida y el lazo de droop entra en resonancia con la dinámica de la red.

### 7.3 — Intervención 1: reducir ωf

Al reducir el ancho de banda del filtro de potencia de \( 30\,\text{Hz} \) a \( 10\,\text{Hz} \) (\( \omega_f = 2\pi\cdot10 \)):

$$\lambda_{pot}^{(1)} \approx -1.2 \pm j14\,\text{rad/s}$$

El polo se mueve hacia el SPI pero queda muy poco amortiguado (\( \zeta \approx 0.085 \)). El sistema es marginalmente estable, con un transitorio muy oscilatorio que tarda varios segundos en disiparse.

### 7.4 — Intervención 2: impedancia virtual Xvirt

La impedancia virtual actúa como una reactancia serie adicional que reduce la **rigidez de sincronización** \( K_s = \partial P/\partial\delta \):

$$K_s = \frac{EV}{X_{total}} \approx \frac{EV}{X_{line} + X_{virt}}$$

Al aumentar \( X_{virt} \), \( K_s \) disminuye y los polos del modo de potencia se desplazan hacia la izquierda (menor frecuencia natural \( \omega_n \)) y hacia afuera del eje real (mayor amortiguamiento \( \zeta \)).

Con \( X_{virt} \) dimensionado para \( K_s \to K_s/2 \) y \( \omega_f = 2\pi\cdot10\,\text{Hz} \):

$$\boxed{\lambda_{pot}^{(2)} = -8.3 \pm j21.0\,\text{rad/s}, \quad \zeta = 0.37, \quad f_n = 3.3\,\text{Hz}}$$

### 7.5 — Verificación: autovalores de A vs polos de G(s)

Los autovalores de la matriz \( A \) linealizada se calculan con `numpy.linalg.eigvals(A)`. Los polos de la función de transferencia \( G(s) = C(sI-A)^{-1}B + D \) son las raíces de \( \det(sI-A) \). Por construcción, ambos son idénticos.

La verificación numérica del proyecto 01 confirma:

$$\text{eigvals}(A)\bigr|_{modo\,potencia} = -8.3 \pm j21.0\,\text{rad/s}$$
$$\text{poles}(G(s))\bigr|_{modo\,potencia} = -8.3 \pm j21.0\,\text{rad/s}$$

Diferencia: \( < 10^{-10}\,\text{rad/s} \) (error numérico de máquina). Los dos métodos de calcular los polos son equivalentes; el preferido depende de la representación disponible.

<div class="cfig"><img src="figuras/polos-ceros-analisis.png" alt="analisis avanzado de polos y ceros"><div class="cap">Panel (a): lugar de las raíces de G=K/[s(s+2)(s+4)]; asíntotas a 60°/180°/300° partiendo del centroide s=−2; estrella verde marca K≈3.5 para ζ=0.7. Panel (b): cero RHP en s=+5 produce respuesta inversa inicial (curva roja) frente a la respuesta normal de la versión de fase mínima (curva verde discontinua). Panel (c): función de sensibilidad |S(jω)| para un PI con PM≈60°; zona verde es atenuación de perturbaciones; línea roja discontinua marca el límite Ms=6dB. Panel (d): mapa de polos del proyecto-01 — las cruces rojas (parte real positiva, SPD) representan el modo de potencia inestable inicial; las flechas muestran el movimiento al reducir ωf y añadir Xvirt; las cruces verdes son el resultado final (ζ=0.37, f=3.3Hz).</div></div>

## Cuándo y por qué se usa
Es la lectura básica de cualquier diseño: mirar el mapa de polos dice de un vistazo si es estable,
cómo de rápido y cómo de amortiguado. Es la base del análisis modal y del lugar de las raíces.

## Procedimiento (genérico)
1. Obtén la función de transferencia o el modelo de estado.
2. Calcula los polos (raíces del denominador / autovalores de \( A \)).
3. Comprueba estabilidad (todos con parte real negativa).
4. Lee rapidez (\( |\sigma| \)) y amortiguamiento (\( \zeta \)) de los polos dominantes.
5. Si hay ceros RHP, identifica el techo de ancho de banda \( \omega_c < z/2 \).

## Ejemplo de aplicación real
**Problema:** PI de corriente con \( K_p=5 \), cero en \( z=-10 \), planta \( G(s)=1/(s+10) \). Identificar la cancelación polo-cero y su efecto en la respuesta.

El PI tiene numerador \( K_p(s+10) \); la planta tiene polo en \( s=-10 \). Al multiplicar, el factor \( (s+10) \) se cancela: la ganancia de lazo abierto queda \( L(s)=5/s \) (integrador puro). El lazo cerrado es \( G_{cl}(s)=5/(s+5) \): polo único en \( s=-5 \), sin oscilación. Si el polo de la planta varía un 10 % (\( r'=11 \)), queda un polo residual en \( s=-11 \) no cancelado: como sigue en el SPD, el sistema permanece estable y el efecto sobre la respuesta transitoria es mínimo. La cancelación imperfecta es aceptable siempre que el residuo esté en el semiplano izquierdo.

## Ejemplo de código
```python
import numpy as np
from scipy import signal

# Lugar de las raices de G = K/[s(s+2)(s+4)]
den = [1, 6, 8, 0]   # s^3 + 6s^2 + 8s = s(s+2)(s+4)
Ks  = np.linspace(0, 60, 2000)
roots_all = np.array([np.roots(np.array(den) + [0, 0, 0, K]) for K in Ks])

# Funcion de sensibilidad
wc = 3.0; wi = wc * np.tan(np.radians(30))
jw_c = 1j*wc
Kp = abs(jw_c*(jw_c+1)) / abs(jw_c + wi)
w = np.logspace(-2, 2, 2000)
jw = 1j*w
L = Kp*(jw+wi)/(jw*(jw+1))
S = 1/(1+L)
Ms_dB = 20*np.log10(np.max(np.abs(S)))

# Autovalores del modelo GFM linealizado
A = np.array([...])   # rellenar con A del modelo
lambdas = np.linalg.eigvals(A)
estable  = np.all(lambdas.real < 0)
```

## Parámetros y valores típicos
Polos dominantes: los más cercanos al eje imaginario (los más lentos) dominan la respuesta.
\( \zeta>0.3 \) suele dar respuesta aceptable. \( M_s < 2 \) (\( 6\,\text{dB} \)) para control robusto.
Cero RHP en convertidores: \( z_{RHP} = R(1-D)^2/L \), limita \( \omega_c < z_{RHP}/2 \).

## Errores comunes
- Mirar solo la parte real e ignorar el amortiguamiento (un polo poco amortiguado oscila).
- Cancelar un polo inestable con un cero (cancelación no robusta, estado diverge).
- Ignorar el efecto del water-bed: reducir sensibilidad aquí siempre amplifica allá.
- Confundir el pico de resonancia Bode (\( 1/(2\zeta) \)) con el pico de sensibilidad \( M_s \) (son distintos).

## Conceptos relacionados
- [[funcion-transferencia]] · [[respuesta-segundo-orden]] · [[estabilidad-bibo]] · [[analisis-modal]] · [[margenes-estabilidad]]

## Referencias
- Franklin, Powell, *Feedback Control of Dynamic Systems*.
- Ogata, *Ingeniería de Control Moderna*.
- Skogestad, Postlethwaite, *Multivariable Feedback Control*.
