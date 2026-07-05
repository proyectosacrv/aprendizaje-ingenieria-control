---
titulo: Componentes simétricas (Fortescue)
slug: componentes-simetricas
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: []
objetivos: [descomponer un sistema trifásico desequilibrado en secuencias tratables]
tags: [componentes-simetricas, secuencia, desequilibrio, fortescue, dsogi, falta, resonante-negativo, intermedio, modelado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-03
relacionados: [sistema-trifasico, potencia-ac-fasores, marco-dq, red-thevenin-scr]
referencias:
  - "Kundur, Power System Stability and Control, McGraw-Hill 1994"
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
  - "Rodriguez et al., Decoupled Double Synchronous Reference Frame PLL, IEEE TPEL 2007"
  - "Fortescue, Method of Symmetrical Coordinates Applied to the Solution of Polyphase Networks, AIEE 1918"
---

## Definición
Descomposición de tres fasores **desequilibrados** en la suma de tres conjuntos equilibrados:
secuencia **positiva** (+), **negativa** (−) y **homopolar/cero** (0). Permite analizar fallos y
desequilibrios con herramientas de sistema equilibrado.

## Fundamento teórico
Con el operador \( a=e^{j120^\circ} \):
$$ \begin{bmatrix}V_0\\V_+\\V_-\end{bmatrix}=
   \frac{1}{3}\begin{bmatrix}1&1&1\\1&a&a^2\\1&a^2&a\end{bmatrix}
   \begin{bmatrix}V_a\\V_b\\V_c\end{bmatrix} $$
- **Positiva:** terna equilibrada con la secuencia normal (a-b-c) → gira en \( +\omega \).
- **Negativa:** terna equilibrada de secuencia invertida → gira en \( -\omega \) (aparece en
  faltas asimétricas y cargas desequilibradas).
- **Homopolar:** tres fasores en fase, requiere camino de neutro/tierra.

Relación con dq: en marco dq a \( +\omega \), la secuencia positiva es **continua** y la negativa
aparece como rizado de **\( 2\omega \)** (100 Hz), motivo de los controles de doble secuencia.

<div class="cfig"><img src="figuras/componentes-simetricas-fasores.png" alt="fasores de secuencia positiva, negativa y homopolar"><div class="cap">Cualquier terna desequilibrada se descompone en tres equilibradas: positiva (gira +ω), negativa (secuencia invertida, −ω) y homopolar (tres fasores en fase).</div></div>

## 1 — De dónde sale la matriz de Fortescue
**Paso 1 — la síntesis (lo físico).** El punto de partida no es la matriz de análisis, sino su inversa: *cualquier* terna se **construye** sumando tres ternas equilibradas. Por definición de cada secuencia, sus fasores se desfasan \( 120° \) usando el operador \( a=e^{j120°} \) (que cumple \( a^3=1 \) y \( 1+a+a^2=0 \)). Tomando la fase A de cada secuencia (\( V_0,V_+,V_- \)) como referencia:

$$ \begin{aligned}
V_a&=V_0+V_++V_-\\
V_b&=V_0+a^2V_++a\,V_-\\
V_c&=V_0+a\,V_++a^2V_-
\end{aligned} $$

La secuencia **positiva** va a-b-c (la fase B retrasa \( 120° \): factor \( a^2 \)); la **negativa** va a-c-b (factor \( a \)); la **homopolar** es idéntica en las tres (factor \( 1 \)). En forma matricial:

$$ \begin{bmatrix}V_a\\V_b\\V_c\end{bmatrix}=
   \underbrace{\begin{bmatrix}1&1&1\\1&a^2&a\\1&a&a^2\end{bmatrix}}_{A^{-1}}
   \begin{bmatrix}V_0\\V_+\\V_-\end{bmatrix} $$

**Paso 2 — invertir para obtener el análisis.** Queremos \( (V_0,V_+,V_-) \) a partir de \( (V_a,V_b,V_c) \), es decir invertir \( A^{-1} \). En lugar de Gauss, usamos la **ortogonalidad** de las raíces de la unidad: \( 1+a+a^2=0 \). Multiplicando, por ejemplo, la primera fila de \( V_a,V_b,V_c \) por los pesos \( (1,a,a^2) \) y sumando:

$$ V_a+a\,V_b+a^2V_c=V_0(1+a+a^2)+V_+(1+a^3+a^3)+V_-(1+a^2+a^4) $$

**Paso 3 — colapsar con \( a^3=1 \).** Sustituyendo \( a^3=1 \) y \( a^4=a \):
- coeficiente de \( V_0 \): \( 1+a+a^2=0 \) → se anula;
- coeficiente de \( V_+ \): \( 1+1+1=3 \);
- coeficiente de \( V_- \): \( 1+a^2+a=0 \) → se anula.

Queda \( V_a+a\,V_b+a^2V_c=3V_+ \), de donde \( V_+=\tfrac13(V_a+a\,V_b+a^2V_c) \). Repitiendo con pesos \( (1,1,1) \) sale \( V_0=\tfrac13(V_a+V_b+V_c) \), y con \( (1,a^2,a) \) sale \( V_-=\tfrac13(V_a+a^2V_b+a\,V_c) \). Reunidos:

$$ \boxed{\;\begin{bmatrix}V_0\\V_+\\V_-\end{bmatrix}=
   \frac{1}{3}\begin{bmatrix}1&1&1\\1&a&a^2\\1&a^2&a\end{bmatrix}
   \begin{bmatrix}V_a\\V_b\\V_c\end{bmatrix}\;} $$

El factor \( 1/3 \) viene del \( 3 \) que dejó la ortogonalidad. La matriz de análisis es la conjugada (transpuesta) de la de síntesis salvo ese \( 1/3 \): por eso \( A^{-1}=3\bar A^{\top}/3 \) y todo encaja.

## 2 — La transformación de Fortescue: de ABC a secuencias 0, 1, 2

### El operador a y sus propiedades fundamentales

El operador \( a=e^{j2\pi/3}=e^{j120°} \) es simplemente un giro de \( 120° \) en el plano complejo. Sus potencias completan la trilogía:

$$ a^0=1,\quad a^1=e^{j120°}=-\tfrac12+j\tfrac{\sqrt3}{2},\quad a^2=e^{j240°}=-\tfrac12-j\tfrac{\sqrt3}{2} $$

Las tres propiedades esenciales que hacen posible Fortescue:
1. \( a^3=1 \) (gira tres veces 120° = vuelta completa)
2. \( 1+a+a^2=0 \) (los tres vértices de un triángulo equilátero suman cero)
3. \( (a^k)^*=a^{-k}=a^{3-k} \) (conjugar invierte el giro)

### La transformación directa y la inversa

La **transformación directa** (análisis, ABC → secuencias):

$$ \begin{bmatrix}V_0\\V_1\\V_2\end{bmatrix}=\frac{1}{3}
   \underbrace{\begin{bmatrix}1&1&1\\1&a&a^2\\1&a^2&a\end{bmatrix}}_{T}
   \begin{bmatrix}V_a\\V_b\\V_c\end{bmatrix} $$

donde la notación estándar usa \( V_1\equiv V_+ \) (positiva) y \( V_2\equiv V_- \) (negativa). La **transformación inversa** (síntesis, secuencias → ABC):

$$ \begin{bmatrix}V_a\\V_b\\V_c\end{bmatrix}=
   \underbrace{\begin{bmatrix}1&1&1\\1&a^2&a\\1&a&a^2\end{bmatrix}}_{T^{-1}}
   \begin{bmatrix}V_0\\V_1\\V_2\end{bmatrix} $$

La relación entre ellas: \( T^{-1}=3T^{H}/3 \) donde \( T^H \) es la hermítica (conjugada transpuesta). Como \( (a^k)^*=a^{-k} \), conjugar las columnas de \( T \) da exactamente \( T^{-1} \), de modo que la base de secuencias es **unitaria** (salvo el factor \( 1/3 \)). Esto tiene una consecuencia inmediata sobre la potencia.

### Demostración: sistema equilibrado abc → secuencia positiva pura

Sea \( V_a=V\angle 0 \), \( V_b=V\angle{-120°}=Va^2 \), \( V_c=V\angle{+120°}=Va \). Aplicando la transformada:

$$ V_0=\tfrac13\,V(1+a^2+a)=0 \qquad\text{(suma de raíces = 0)} $$
$$ V_1=\tfrac13\,V(1+a\cdot a^2+a^2\cdot a)=\tfrac13\,V(1+a^3+a^3)=\tfrac13\,V\cdot3=V $$
$$ V_2=\tfrac13\,V(1+a^2\cdot a^2+a\cdot a)=\tfrac13\,V(1+a^4+a^2)=\tfrac13\,V(1+a+a^2)=0 $$

El resultado \( V_1=V \), \( V_0=V_2=0 \) confirma que un sistema equilibrado es **puramente de secuencia positiva**.

### Potencia total = suma de potencias de secuencia (ortogonalidad)

La potencia compleja trifásica es \( S=\mathbf{V}_{abc}^H\mathbf{I}_{abc} \). Sustituyendo \( \mathbf{V}_{abc}=T^{-1}\mathbf{V}_{012} \) e \( \mathbf{I}_{abc}=T^{-1}\mathbf{I}_{012} \):

$$ S=(T^{-1}\mathbf{V}_{012})^H(T^{-1}\mathbf{I}_{012})=\mathbf{V}_{012}^H\underbrace{(T^{-1})^H T^{-1}}_{3I}\mathbf{I}_{012}=3(\mathbf{V}_{012}^H\mathbf{I}_{012}) $$

La clave es que \( (T^{-1})^H T^{-1}=3I \) porque los vectores columna de \( T^{-1} \) son ortogonales (producto escalar entre columnas distintas = 0 por \( 1+a+a^2=0 \); producto propio = 3). Expandiendo:

$$ \boxed{S=3(V_0^*I_0+V_1^*I_1+V_2^*I_2)=S_0+S_1+S_2} $$

La potencia total es la **suma de las potencias de cada secuencia** multiplicadas por 3. En un sistema equilibrado solo existe \( S_1 \); en uno con desequilibrio también \( S_2 \) (potencia "perdida" en el calentamiento diferencial de motores y transformadores).

## 3 — El DSOGI para separar secuencias en αβ

### Por qué trabajar en αβ en lugar de ABC

En los convertidores VSC el control trabaja en el marco \( dq \) (o \( \alpha\beta \) antes de la rotación). La detección de secuencias en ABC requiere fasores → FFT → latencia. El **DSOGI** (*Dual Second-Order Generalized Integrator*) opera directamente sobre señales instantáneas \( v_\alpha,\,v_\beta \) y separa secuencias con solo dos filtros adaptativos, consiguiendo un tiempo de respuesta de \( \approx 1/(k\omega_0) \).

### Por qué la secuencia positiva gira CCW y la negativa CW en αβ

En el marco estacionario αβ, una señal de secuencia positiva es \( v_\alpha^+=V^+\cos(\omega t) \), \( v_\beta^+=V^+\sin(\omega t) \): el fasor gira en sentido antihorario (CCW, convención positiva). Una señal de secuencia negativa tiene la fase b y c intercambiadas, lo que se traduce en \( v_\alpha^-=V^-\cos(\omega t) \), \( v_\beta^-=-V^-\sin(\omega t) \): el fasor gira en sentido horario (CW, frecuencia \( -\omega \)).

Esto es exactamente lo que la DSOGI explota: el cuadrante del operador \( q \) (adelanto de 90°) distingue los sentidos de giro.

### El operador q y la separación de secuencias

El DSOGI implementa el operador \( q \): dado \( v_\alpha \), produce \( qv_\alpha \) como la versión adelantada 90° de \( v_\alpha \) (en práctica, un integrador de segundo orden sintonizado a \( \omega_0 \) actúa como filtro en cuadratura). Para la señal compuesta \( v_\alpha=v_\alpha^++v_\alpha^- \):

$$ qv_\alpha=qv_\alpha^++qv_\alpha^-=V^+\sin(\omega t)+(-V^-\sin(\omega t))=V^+\sin(\omega t)-V^-\sin(\omega t) $$

Análogamente \( qv_\beta=V^+\cos(\omega t)+V^-\cos(\omega t) \) (la negativa adelanta en lugar de retrasar en β). Combinando:

**Secuencia positiva:**
$$ \boxed{V_\alpha^+=\frac{v_\alpha-qv_\beta}{2},\qquad V_\beta^+=\frac{qv_\alpha+v_\beta}{2}} $$

**Secuencia negativa:**
$$ \boxed{V_\alpha^-=\frac{v_\alpha+qv_\beta}{2},\qquad V_\beta^-=\frac{-qv_\alpha+v_\beta}{2}} $$

**Verificación para \( V^-=0 \) (sistema equilibrado):** Con solo secuencia positiva, \( v_\alpha=V^+\cos\omega t \) y \( v_\beta=V^+\sin\omega t \), luego \( qv_\alpha=V^+\sin\omega t \) y \( qv_\beta=-V^+\cos\omega t \). Entonces:
- \( V_\alpha^+=(V^+\cos\omega t-(-V^+\cos\omega t))/2=V^+\cos\omega t=v_\alpha\;\checkmark \)
- \( V_\alpha^-=(V^+\cos\omega t+(-V^+\cos\omega t))/2=0\;\checkmark \)

### Tiempo de convergencia ≈ 20 ms

El DSOGI es un filtro adaptativo de segundo orden con factor de amortiguamiento \( k \). Su respuesta al escalón converge con constante de tiempo \( \tau\approx1/(k\omega_0) \). Con \( k=1.41 \) y \( \omega_0=2\pi\cdot50 \) rad/s:

$$ \tau=\frac{1}{1.41\cdot314}=2.25\,\text{ms}\quad\Rightarrow\quad 5\tau\approx11\,\text{ms} $$

En la práctica, para \( k=1 \): \( \tau=3.18 \) ms, y la separación completa se logra en \( \approx20 \) ms (entre \( 1/(k\omega_0) \) y un ciclo de red). Ese ciclo de 20 ms es el mínimo tiempo de detección de desequilibrio que impone la norma de FRT (*fault ride-through*).

## 4 — La corriente de secuencia negativa: problemas y control

### Efecto del desequilibrio en motores

Bajo tensión desequilibrada con \( V_-/V_+=\epsilon \), la máquina de inducción ve dos campos giratorios:
- Campo positivo (a \( +\omega \)): produce par útil \( T_+\propto V_+^2 \).
- Campo negativo (a \( -\omega \)): produce par de frenado \( T_-\propto V_-^2 \).

El par neto oscila a \( 2\omega \) (100 Hz), produciendo vibraciones mecánicas. El calentamiento del rotor se duplica: la resistencia equivalente del rotor ante el campo negativo es \( R_r/(2-s)\approx R_r/2 \) (para \( s\approx0 \)), es decir el rotor "ve" la componente negativa a \( 2\omega_s \) y disipa potencia. Por eso la norma IEC 60034-26 limita el desequilibrio continuo a \( V_-/V_+<2\% \).

### GFL en dq: desequilibrio 10% → rizado 100 Hz en id, iq

En un convertidor GFL controlado en el marco \( dq^+ \) (girando a \( +\omega \)), la tensión de secuencia negativa \( \mathbf{V}^- \) aparece como un fasor girando a \( -2\omega \) en ese marco:

$$ v_d^-+jv_q^-=V^-e^{-j2\omega t} $$

El lazo PI de corriente, diseñado para seguir referencias constantes, no tiene ganancia infinita a \( 2\omega \): **no puede rechazar** esa perturbación. La respuesta en estado estacionario es:

$$ \Delta i_d(t)=\frac{V^-}{|Z_{PI}(j2\omega)|}\cos(2\omega t+\phi_{PI}) $$

Para \( V^-/V^+=10\% \), \( V^-=0.1 \) pu. Con \( Z_{PI}(j100\,\text{Hz})\approx j2\omega L_{total}\approx j\cdot628\cdot3\,\text{mH}=j1.88\,\text{m}\Omega \) y \( Z_{base}=476\,\text{m}\Omega \):

$$ |\Delta i_d|\approx\frac{0.1}{2\cdot2\pi\cdot100\cdot3\times10^{-3}/Z_{base}}=\frac{0.1\,\text{pu}}{0.394\,\text{pu}}\approx0.25\,\text{pu} $$

Es decir un rizado del **25%** de la corriente nominal a 100 Hz — inaceptable para THD de corriente. El rizado también afecta al lazo de tensión DC a través de la potencia \( P=v_d i_d+v_q i_q \).

### Solución: controlador resonante en secuencia negativa

Para eliminar el rizado se añade un controlador resonante sintonizado a \( -2\omega_0 \) (o equivalentemente a \( +2\omega_0 \) en el marco de secuencia negativa). Su función de transferencia:

$$ C_R(s)=\frac{2k_R s}{s^2+(2\omega_0)^2} $$

Con \( k_R=50\text{–}200 \), la ganancia en \( 2\omega_0 \) es \( \to\infty \), anulando el error en estado estacionario a esa frecuencia. El controlador total del lazo de corriente es \( C(s)=C_{PI}(s)+C_R(s) \).

**Tabla de parámetros típicos del controlador resonante:**

| Parámetro | Símbolo | Valor típico |
|---|---|---|
| Ganancia resonante | \( k_R \) | 50–200 |
| Frecuencia de resonancia | \( \omega_R \) | \( 2\omega_0=628 \) rad/s |
| Ancho de banda del resonante | \( \omega_c \) | 5–20 rad/s |
| Tiempo de convergencia | \( t_{conv} \) | \( 2/\omega_c \approx 0.1\text{–}0.4 \) s |

## 5 — El análisis de faltas con componentes simétricas

### Por qué usar secuencias para analizar faltas

Ante una falta asimétrica en un sistema trifásico, las tres fases dejan de ser equivalentes: no se puede usar el circuito monofásico equivalente directamente. Pero las **redes de secuencia** sí son simétricas entre sí (cada red de secuencia ve un sistema equilibrado). La clave es que, en el punto de falta, las condiciones de contorno (tensiones y corrientes) acoplan las tres redes de secuencia de una forma específica según el tipo de falta.

### Falta trifásica: solo secuencia positiva

En una falta trifásica simétrica (A-B-C a tierra simultáneamente), el sistema sigue siendo trifásico equilibrado y solo interviene la red de secuencia positiva. La corriente de falta:

$$ I_{f,3\phi}=\frac{V_{prefalta}}{Z_1} $$

donde \( Z_1 \) es la impedancia de Thévenin de secuencia positiva vista desde el punto de falta. Para \( Z_1=j0.1 \) pu y \( V=1 \) pu: \( I_{f,3\phi}=1/0.1=10 \) pu.

### Falta monofásica (A a tierra): las tres secuencias en serie

Las condiciones de contorno de una falta monofásica a tierra en la fase A son:
- \( V_a=0 \) en el punto de falta (tensión de fase A = 0)
- \( I_b=I_c=0 \) (las otras fases no tienen retorno de falta)

Aplicando la transformada de Fortescue a estas condiciones, resulta que las tres redes de secuencia se conectan **en serie** en el circuito de secuencia:

$$ I_{f,1\phi}=\frac{3V_{prefalta}}{Z_0+Z_1+Z_2} $$

### Falta bifásica (B-C): secuencias positiva y negativa en paralelo

Las condiciones de una falta B-C (sin tierra) obligan a \( I_a=0 \) y \( V_b=V_c \). Las redes de secuencia 1 y 2 quedan en paralelo; la secuencia 0 no interviene (no hay camino a tierra):

$$ I_{f,2\phi}=\frac{\sqrt{3}\,V_{prefalta}}{Z_1+Z_2} $$

### Ejemplo numérico: Z1=Z2=0.1 pu, Z0=0.05 pu

Suponiendo \( V_{prefalta}=1 \) pu:

$$ I_{f,3\phi}=\frac{1}{Z_1}=\frac{1}{0.1}=10\,\text{pu} $$

$$ I_{f,1\phi}=\frac{3}{Z_0+Z_1+Z_2}=\frac{3}{0.05+0.1+0.1}=\frac{3}{0.25}=12\,\text{pu} $$

$$ I_{f,2\phi}=\frac{\sqrt3}{Z_1+Z_2}=\frac{1.732}{0.2}=8.66\,\text{pu} $$

**La corriente de falta monofásica (12 pu) supera a la trifásica (10 pu)** porque \( Z_0<Z_1 \): la pequeña impedancia de secuencia cero (neutro sólido, baja resistencia de tierra) hace que el circuito serie \( Z_0+Z_1+Z_2 \) sea menor que \( Z_1 \) solo. Esto es crítico para la coordinación de protecciones: el relé de tierra debe calibrarse con esta corriente mayor.

### El papel de la puesta a tierra

La secuencia cero solo circula si existe un camino físico cerrado (neutro sólido o con impedancia, transformador con devanado triangulado). En un sistema con transformadores \( \Delta/Y \) o cables sin neutro, \( Z_0\to\infty \) y la falta monofásica no puede desarrollar corriente de secuencia cero: la protección diferencial de tierra no vería la falta.

<div class="cfig"><img src="figuras/componentes-simetricas-analisis.png" alt="Fortescue, DSOGI, rizado dq y magnitudes de secuencia por falta"><div class="cap">(a) Diagrama fasorial Fortescue: terna desequilibrada → secuencias positiva, negativa y homopolar. (b) DSOGI en αβ: separación de V⁺ y V⁻ a partir de la señal con 20% de secuencia negativa. (c) Rizado a 100 Hz en id/iq con desequilibrio 10%: sin compensación vs con controlador resonante de secuencia negativa. (d) Magnitudes de secuencia según tipo de falta: en la trifásica las tres son iguales; en la monofásica positiva y negativa y cero son iguales (1/3 pu); en la bifásica no hay secuencia cero.</div></div>

## 6 — Diseño iterativo: control de corriente con desequilibrio 10%

### Especificación del problema

Sistema GFL de 1 MVA/690 V conectado a una red con desequilibrio de tensión del 10% (\( V^-/V^+=0.1 \)). Objetivo: THD de corriente inyectada \( <5\% \). La componente dominante del THD bajo desequilibrio es la de 100 Hz (orden 2).

Bases: \( S_{base}=1\,\text{MVA} \), \( V_{base}=690\,\text{V} \) → \( I_{base}=836.7\,\text{A} \), \( Z_{base}=0.476\,\Omega \), \( L_{base}=1.52\,\text{mH} \).

Filtro LCL: \( L_1=1.5\,\text{mH} \), \( L_2=0.5\,\text{mH} \), \( C_f=20\,\mu\text{F} \) → \( L_{total}=2\,\text{mH}=1.32\,\text{pu} \).

### Estrategia 1: solo PI sobre secuencia positiva

El PI está sintonizado para el lazo de corriente a \( f_c=500\,\text{Hz} \): \( k_p=\omega_c L_{total}=2\pi\cdot500\cdot2\times10^{-3}=6.28\,\Omega \). A 100 Hz, la ganancia del PI:

$$ |C_{PI}(j2\omega_0)|=\sqrt{k_p^2+(k_i/2\omega_0)^2}\approx k_p=6.28\,\Omega $$

La perturbación a suprimir: \( V^-=0.1\,\text{pu}\cdot V_{base}/\sqrt2=48.8\,\text{V} \) (pico). El error de corriente resultante:

$$ |\Delta I_{100}|=\frac{|V^-|}{|C_{PI}(j2\omega_0)+j2\omega_0 L_{total}|}=\frac{48.8}{|6.28+j2.51|}=\frac{48.8}{6.77}=7.2\,\text{A} $$

En por unidad: \( 7.2/836.7=0.86\% \) de \( I_{base} \), pero como **amplitud del rizado** es \( \pm7.2\,\text{A} \) pico sobre una corriente nominal de \( 836.7\,\text{A}\cdot\sqrt2/\sqrt3 \)... Replanteando en pu directamente: \( |\Delta i_d|\approx V^-/(2\omega_0 L_{pu})\approx0.1/(0.83)=12\% \) de corriente nominal. El THD en corriente resulta \( \approx12\% \), claramente fuera de especificación.

### Estrategia 2: PI + resonante de secuencia negativa

Se añade el resonante \( C_R(s)=2k_R s/(s^2+4\omega_0^2) \) con \( k_R=100 \). La ganancia a \( 2\omega_0 \):

$$ |C_R(j2\omega_0)|\to\infty \quad\text{(polo en }j2\omega_0\text{)} $$

En estado estacionario, el error de corriente a 100 Hz → 0: \( id^-=iq^-=0 \). El THD de corriente resulta limitado solo por los armónicos de conmutación (\( <1\% \) a 10 kHz), bien dentro del 5% especificado.

### Comparativa de estrategias

| Estrategia | Control | Rizado \( i_d \) a 100 Hz | THD corriente | Complejidad |
|---|---|---|---|---|
| 1: PI solo (seq. positiva) | PI estándar en dq⁺ | ≈12% nominal | ≈12% | Baja |
| 2: PI + resonante neg. | PI en dq⁺ + \( C_R \) a \( 2\omega_0 \) | <0.1% | <1% | Media |

La estrategia 2 es el estándar industrial para sistemas con requisito de desequilibrio. La implementación digital requiere discretizar el resonante con Tustin o prewarping para mantener el polo exactamente en \( 2\omega_0 \).

## Cuándo y por qué se usa
Análisis de faltas asimétricas, requisitos de **fault ride-through**, control bajo desequilibrio
de red y diseño de lazos de secuencia negativa en convertidores. Complementa a [[marco-dq]] y
[[marco-dq|transformada de Clarke]].

## Procedimiento (genérico)
1. Mide los fasores de fase \( V_a,V_b,V_c \) (o las señales αβ instantáneas via Clarke).
2. Aplica la matriz de Fortescue (o el DSOGI si es en tiempo real) → \( V_0,V_1,V_2 \).
3. Analiza/regula cada secuencia por separado con su lazo de control propio.
4. Recompón (matriz inversa) para volver a magnitudes de fase si es necesario.

## Ejemplo de código
```python
import numpy as np
a = np.exp(1j*2*np.pi/3)
T = np.array([[1,1,1],[1,a,a**2],[1,a**2,a]])
V0, Vp, Vn = (T / 3) @ np.array([Va, Vb, Vc])   # fasores de fase complejos

# DSOGI en tiempo discreto (idea simplificada):
# qvalpha se obtiene con un SOGI sintonizado a omega0
Vp_alpha = (valpha - q_vbeta) / 2
Vp_beta  = (q_valpha + vbeta) / 2
Vn_alpha = (valpha + q_vbeta) / 2
Vn_beta  = (-q_valpha + vbeta) / 2
```

## Parámetros y valores típicos
| Magnitud | Valor | Condición |
|---|---|---|
| Desequilibrio máximo en red | \( V_-/V_+<2\% \) | IEC 61000-2-2 (red pública) |
| Desequilibrio en falta asimétrica | 10–50% | Depende del tipo de falta |
| Tiempo de convergencia DSOGI | ≈20 ms | \( k=1 \), \( f_0=50 \) Hz |
| Ganancia resonante típica | \( k_R=50\text{–}200 \) | Lazo de corriente digital |
| Impedancia \( Z_{cc,mono}/Z_{cc,3\phi} \) | >1 si \( Z_0<Z_1 \) | Neutro sólido |

## Errores comunes
- Aplicar el método a magnitudes instantáneas en vez de a **fasores** (régimen sinusoidal).
- Olvidar que sin neutro la secuencia 0 no circula: \( Z_0\to\infty \).
- Ignorar el rizado de \( 2\omega \) que la secuencia negativa induce en dq.
- Confundir el operador \( a=e^{j2\pi/3} \) (120°) con \( e^{j\pi/3} \) (60°).
- No adaptar el resonante a la frecuencia real de la red (si la red varía ±0.5 Hz, el resonante fijo pierde ganancia).

## Conceptos relacionados
- [[sistema-trifasico]] · [[potencia-ac-fasores]] · [[marco-dq]] · [[red-thevenin-scr]] · [[fault-ride-through]]

## Referencias
- Kundur, *Power System Stability and Control*, 1994.
- Yazdani, Iravani, *Voltage-Sourced Converters in Power Systems*, Wiley 2010.
- Rodriguez et al., *Decoupled Double Synchronous Reference Frame PLL*, IEEE TPEL 2007.
- Fortescue, *Method of Symmetrical Coordinates*, AIEE 1918.
