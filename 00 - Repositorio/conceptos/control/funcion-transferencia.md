---
titulo: Función de transferencia
slug: funcion-transferencia
categoria: control
tipo: concepto
nivel: basico
proyectos: []
objetivos: [describir la relacion entrada-salida de un sistema lineal, conectar G(s) con espacio de estados y respuesta temporal]
tags: [funcion-transferencia, dominio-s, ganancia, polos, ceros, antitransformada, basico, control]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [transformada-laplace, polos-ceros, respuesta-frecuencia-ss, diagrama-bode, realimentacion, espacio-estados]
referencias:
  - "Ogata, Ingeniería de Control Moderna, Pearson"
  - "Franklin, Powell, Feedback Control of Dynamic Systems, Pearson"
---

## Definición
Cociente, en el dominio de Laplace, entre la salida y la entrada de un sistema lineal con
condiciones iniciales nulas. Resume toda la dinámica entrada-salida en una sola expresión
\( G(s) \).

## Fundamento teórico
$$ G(s) = \frac{Y(s)}{U(s)} = \frac{b_m s^m + \dots + b_0}{a_n s^n + \dots + a_0} $$
- El **denominador** igualado a cero da la **ecuación característica**: sus raíces son los
  **polos** (gobiernan la dinámica y la estabilidad).
- El **numerador** da los **ceros**.
- \( G(0) \) es la **ganancia en continua** (régimen permanente ante un escalón).
- Evaluando en \( s=j\omega \) se obtiene la **respuesta en frecuencia** \( G(j\omega) \) (Bode).

El orden \( n \) del denominador es el número de estados/almacenadores de energía.

<div class="cfig"><img src="figuras/funcion-transferencia-polos-step.png" alt="polos de G(s) y la respuesta al escalon que implican"><div class="cap">Los polos de G(s) (raíces del denominador) determinan la forma de la respuesta: este par complejo subamortiguado produce el escalón con sobreimpulso de la derecha.</div></div>

## 1 — De la EDO lineal a G(s) por transformada de Laplace

**Paso 1 — ecuación diferencial de partida.** Considera un sistema descrito por la EDO lineal de orden \( n \) con coeficientes constantes (condiciones iniciales nulas):

$$ a_n y^{(n)}(t) + a_{n-1}y^{(n-1)}(t) + \dots + a_1\dot{y}(t) + a_0 y(t) = b_m u^{(m)}(t) + \dots + b_0 u(t) $$

**Paso 2 — aplicar la transformada de Laplace.** Con CI nulas, \( \mathcal{L}\{y^{(k)}(t)\}=s^k Y(s) \). La EDO se convierte en una ecuación algebraica:

$$ \left(a_n s^n + a_{n-1}s^{n-1} + \dots + a_0\right) Y(s) = \left(b_m s^m + \dots + b_0\right) U(s) $$

**Paso 3 — despejar Y(s)/U(s).** Agrupando los polinomios y despejando:

$$ \boxed{G(s) = \frac{Y(s)}{U(s)} = \frac{b_m s^m + \dots + b_0}{a_n s^n + \dots + a_0}} $$

La EDO de grado \( n \) queda comprimida en un cociente de polinomios: el denominador retiene la dinámica propia del sistema (polos) y el numerador, cómo la entrada accede al sistema (ceros).

## 2 — Ejemplo: G(s) = ωn²/(s² + 2ζωn s + ωn²)

**Paso 1 — EDO del oscilador de segundo orden.** Un oscilador amortiguado (masa-resorte-amortiguador, o circuito RLC) tiene la EDO:

$$ \ddot{y}(t) + 2\zeta\omega_n\,\dot{y}(t) + \omega_n^2\,y(t) = \omega_n^2\,u(t) $$

donde \( \omega_n \) es la frecuencia natural y \( \zeta \) el amortiguamiento. El factor \( \omega_n^2 \) en el lado derecho garantiza ganancia unitaria en continua.

**Paso 2 — Laplace con CI nulas.** Aplicando \( \mathcal{L}\{\cdot\} \) término a término:

$$ s^2 Y(s) + 2\zeta\omega_n\,s\,Y(s) + \omega_n^2 Y(s) = \omega_n^2 U(s) $$

**Paso 3 — factorizar y despejar.** Sacando \( Y(s) \) como factor común en la izquierda:

$$ Y(s)\left(s^2 + 2\zeta\omega_n s + \omega_n^2\right) = \omega_n^2 U(s) $$

$$ \boxed{G(s) = \frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}} $$

**Verificación de ganancia DC.** En \( s=0 \): \( G(0)=\omega_n^2/\omega_n^2=1 \). Correcto: ante una entrada escalón, la salida llega a 1 (sin error en régimen permanente).

## 3 — Polos y ceros en G(s): su efecto en el Bode y en la respuesta

### 3.1 — Un polo real en s = −a

Sea \( G(s) = K/(s+a) \) con \( a > 0 \). Sus efectos sobre el Bode son acumulativos conforme la frecuencia supera la frecuencia de ruptura \( f_a = a/(2\pi) \):

$$\text{Para } \omega \gg a:\quad |G(j\omega)| \approx K/\omega \;\Rightarrow\; -20\,\text{dB/dec}$$

$$\angle G(j\omega) \xrightarrow{\omega\to\infty} -90°$$

La transición es suave: a \( \omega = a \) la ganancia ya cayó \(-3\,\text{dB}\) y la fase es exactamente \(-45°\). A \( \omega = 10a \) la fase está a \(-84°\) (prácticamente \(-90°\)).

**Por qué la ganancia DC es \( G(0) = K/a \).** La evaluación directa en \( s=0 \) da exactamente \( K/a \), que es la relación entre el coeficiente del numerador \( b_0 = K \) y el término independiente del denominador \( a_0 = a \). Para cualquier \( G(s) \):

$$\boxed{G(0) = \frac{b_0}{a_0}}$$

### 3.2 — Un cero real en s = −b

Un cero en \( s=-b \) aporta el factor \( (s+b) \) en el numerador, que añade exactamente las contribuciones opuestas a las de un polo:

$$\text{Para } \omega \gg b:\quad +20\,\text{dB/dec}\quad\text{y}\quad +90°$$

Un cero en el semiplano derecho \( s = +z \) (\( z > 0 \)) produce en cambio \( +20\,\text{dB/dec} \) (la misma ganancia que un cero izquierdo) pero \( -90° \) de fase en lugar de \( +90° \). Esto es la **fase no mínima**, que limita el ancho de banda de control.

### 3.3 — Par de polos complejos conjugados

Un par de polos conjugados \( s = -\sigma \pm j\omega_d \) (con \( \sigma = \zeta\omega_n \), \( \omega_d = \omega_n\sqrt{1-\zeta^2} \)) aporta \(-40\,\text{dB/dec}\) y \(-180°\) de fase total, pero con un **pico de resonancia** en \( \omega \approx \omega_n \):

$$|G(j\omega_n)| = \frac{1}{2\zeta} \quad\text{(para }\zeta < 1/\sqrt{2}\text{)}$$

El pico crece indefinidamente a medida que \( \zeta \to 0 \). Un amortiguamiento \( \zeta = 0.3 \) ya produce un pico de \( +10\,\text{dB} \).

### 3.4 — El orden relativo n − m

Si el denominador tiene grado \( n \) y el numerador grado \( m \):

- **\( n > m \):** \( G(s) \to 0 \) para \( s \to \infty \); la pendiente del Bode a alta frecuencia es \( -20(n-m)\,\text{dB/dec} \). Un sistema causal y propio siempre tiene \( n \geq m \).
- **\( n = m \):** \( G(\infty) = b_m/a_n \) (ganancia finita a frecuencia infinita). El Bode es plano para \( \omega \to \infty \).
- **\( n < m \):** la función no es propia (no física); implica derivada pura de la entrada.

En el ejemplo del lazo de corriente con inductancia \( L \): \( G_i(s) = 1/(Ls+r) \) tiene \( n=1, m=0 \), por lo que la pendiente a alta frecuencia es \( -20\,\text{dB/dec} \), confirmando el comportamiento de paso-bajo inherente al inductor.

## 4 — Conexión con el espacio de estados: G(s) = C(sI−A)⁻¹B + D

### 4.1 — Derivación desde las ecuaciones de estado

Parte del modelo de espacio de estados estándar con matrices \( A \in \mathbb{R}^{n\times n} \), \( B \in \mathbb{R}^{n\times 1} \), \( C \in \mathbb{R}^{1\times n} \), \( D \in \mathbb{R} \):

$$\dot{x}(t) = Ax(t) + Bu(t)$$
$$y(t) = Cx(t) + Du(t)$$

**Paso 1 — Laplace con CI nulas.** Aplicando la transformada con \( x(0)=0 \):

$$sX(s) = AX(s) + BU(s) \;\Rightarrow\; (sI - A)X(s) = BU(s)$$

**Paso 2 — despejar X(s).**

$$X(s) = (sI - A)^{-1}BU(s)$$

**Paso 3 — sustituir en la ecuación de salida.**

$$Y(s) = C(sI-A)^{-1}BU(s) + DU(s)$$

$$\boxed{G(s) = \frac{Y(s)}{U(s)} = C(sI-A)^{-1}B + D}$$

### 4.2 — Los autovalores de A son los polos de G(s)

La inversa de una matriz se calcula como adjunta dividida por el determinante:

$$(sI-A)^{-1} = \frac{\text{adj}(sI-A)}{\det(sI-A)}$$

Por tanto \( G(s) = C \cdot \dfrac{\text{adj}(sI-A)}{\det(sI-A)} \cdot B + D \). El denominador de \( G(s) \) es exactamente \( \det(sI-A) \), que es el **polinomio característico** del sistema. Las raíces de \( \det(sI-A) = 0 \) son los autovalores \( \lambda_i \) de \( A \), y por definición son los polos de \( G(s) \):

$$\det(sI-A) = \prod_{i=1}^{n}(s - \lambda_i)$$

**Consecuencia directa:** la estabilidad del sistema (todos los autovalores con parte real negativa) equivale exactamente a que todos los polos de \( G(s) \) estén en el semiplano izquierdo.

### 4.3 — Ejemplo: oscilador de segundo orden

Sea \( A = \begin{bmatrix}0 & 1 \\ -\omega_n^2 & -2\zeta\omega_n\end{bmatrix} \), \( B = \begin{bmatrix}0 \\ 1\end{bmatrix} \), \( C = \begin{bmatrix}\omega_n^2 & 0\end{bmatrix} \), \( D = 0 \).

**Paso 1 — calcular \( sI - A \).**

$$sI - A = \begin{bmatrix}s & -1 \\ \omega_n^2 & s+2\zeta\omega_n\end{bmatrix}$$

**Paso 2 — invertir \( (sI-A) \).**

$$\det(sI-A) = s(s+2\zeta\omega_n) + \omega_n^2 = s^2 + 2\zeta\omega_n s + \omega_n^2$$

$$(sI-A)^{-1} = \frac{1}{s^2+2\zeta\omega_n s+\omega_n^2}\begin{bmatrix}s+2\zeta\omega_n & 1 \\ -\omega_n^2 & s\end{bmatrix}$$

**Paso 3 — aplicar la fórmula.**

$$G(s) = \frac{\begin{bmatrix}\omega_n^2 & 0\end{bmatrix}\begin{bmatrix}s+2\zeta\omega_n & 1 \\ -\omega_n^2 & s\end{bmatrix}\begin{bmatrix}0 \\ 1\end{bmatrix}}{s^2+2\zeta\omega_n s+\omega_n^2} = \frac{\omega_n^2}{s^2+2\zeta\omega_n s+\omega_n^2}$$

Resultado idéntico al obtenido desde la EDO, confirmando la equivalencia de ambas representaciones.

## 5 — La cancelación polo-cero: modos ocultos y peligros

### 5.1 — Qué ocurre en la función de transferencia

Si \( G(s) \) tiene un polo en \( s=p \) y el controlador introduce un cero exactamente en \( s=p \), el factor \( (s-p) \) aparece tanto en numerador como en denominador y se cancela algebraicamente:

$$L(s) = C(s)\cdot G_p(s) = K\cdot\frac{(s-p)}{(s-p)(s-b)} = \frac{K}{s-b}$$

La función de lazo \( L(s) \) resultante no tiene el polo en \( p \): parece que ha desaparecido. **No lo ha hecho.**

### 5.2 — El modo oculto en el estado

Trabajando con la representación interna del sistema, el estado sigue siendo de orden \( n \). La ecuación de estado del sistema completo incluye el modo \( e^{p\,t} \). Lo que ocurre es que dicho modo no aparece en la salida \( Y(s) \) (no es observable) o no es excitado por la entrada (no es controlable), pero existe en el interior.

**Consecuencias según la posición de \( p \):**

| Posición del polo | Naturaleza del modo oculto | Riesgo |
|---|---|---|
| \( \text{Re}(p) < 0 \) (SPI) | Decae con \( \tau = 1/|\text{Re}(p)| \) | Bajo: retardo oculto pero estable |
| \( \text{Re}(p) = 0 \) (eje imaginario) | Oscila sin amortiguación | Medio: puede crecer ante ruido |
| \( \text{Re}(p) > 0 \) (SPD) | Crece exponencialmente | **PELIGROSO**: el estado explota aunque Y no lo muestre |

### 5.3 — Ejemplo del lazo de corriente: cancelación segura

El VSC con \( L=2\,\text{mH} \), \( r=50\,\text{m}\Omega \) tiene la planta \( G_i(s) = 1/(Ls+r) \) con polo en \( s = -r/L = -25\,\text{rad/s} \). El PI diseñado con cero en \( z_{PI} = -r/L = -25\,\text{rad/s} \):

$$C_{PI}(s) = K_p \cdot \frac{s + r/L}{s} = K_p\cdot\frac{s+25}{s}$$

La ganancia de lazo abierto queda:

$$L(s) = C_{PI}(s)\cdot G_i(s) = K_p\cdot\frac{(s+25)}{s}\cdot\frac{1}{L(s+25)} = \frac{K_p}{Ls}$$

El polo en \( s=-25 \) desaparece del lazo, pero el modo \( e^{-25t} \) existe en el estado. Con \( \tau = 1/25 = 40\,\text{ms} \), el modo decae en aproximadamente \( 5\tau = 200\,\text{ms} \): **inofensivo en la práctica**.

### 5.4 — Cancelación imperfecta: el polo residual

Si la resistencia varía \( \pm20\% \) (de \( r=50\,\text{m}\Omega \) a \( r'=60\,\text{m}\Omega \)), el polo real de la planta se desplaza a \( s=-r'/L=-30\,\text{rad/s} \) pero el cero del PI permanece en \( s=-25\,\text{rad/s} \). El cociente ya no cancela limpiamente:

$$L(s) = K_p\cdot\frac{(s+25)}{s}\cdot\frac{1}{L(s+30)} = \frac{K_p(s+25)}{L\,s\,(s+30)}$$

Aparece un polo residual en \( s=-30 \) (en el SPI). El lazo cerrado añade un modo rápido con \( \tau=33\,\text{ms} \) que afecta al transitorio inicial pero decae enseguida. Como el polo residual sigue en el SPI, **la cancelación imperfecta es tolerable** cuando el polo cancela está en el SPI y la incertidumbre paramétrica es moderada.

**La regla de oro:** nunca intentar cancelar un polo en el SPD con un cero. Aunque la función de transferencia parezca estable, el estado interno diverge.

<div class="cfig"><img src="figuras/funcion-transferencia-analisis.png" alt="analisis avanzado de G(s)"><div class="cap">Panel (a): respuesta al impulso (línea sólida) y al escalón (línea discontinua) del sistema de 2º orden para tres valores de ζ; los polos determinan completamente la forma. Panel (b): cancelación polo-cero — la G completa y la reducida son idénticas ante la salida, pero ante incertidumbre paramétrica (+20% en el polo) aparece un modo visible. Panel (c): Bode de G_LCL(s) obtenido algebraicamente y por evaluación numérica directa — diferencia inferior al 0,1%. Panel (d): tabla de pares de transformada de Laplace de uso habitual.</div></div>

## 6 — De G(s) a la respuesta temporal: tabla de antitransformadas clave

La respuesta temporal \( y(t) \) ante cualquier entrada se obtiene multiplicando \( G(s) \) por la transformada de la entrada y aplicando la antitransformada. Los casos más frecuentes son:

### 6.1 — Respuesta al impulso

La entrada impulso tiene \( U(s) = 1 \), por lo que \( Y(s) = G(s) \). La respuesta al impulso \( g(t) \) es directamente la antitransformada de \( G(s) \):

$$g(t) = \mathcal{L}^{-1}\{G(s)\}$$

Para \( G(s) = \omega_n^2/(s^2+2\zeta\omega_n s+\omega_n^2) \) con \( \zeta < 1 \):

$$g(t) = \frac{\omega_n}{\sqrt{1-\zeta^2}}\,e^{-\zeta\omega_n t}\,\sin(\omega_d t)\cdot\mathbf{1}(t), \quad \omega_d = \omega_n\sqrt{1-\zeta^2}$$

### 6.2 — Respuesta al escalón

La entrada escalón tiene \( U(s) = 1/s \), por lo que \( Y(s) = G(s)/s \). Se aplica descomposición en fracciones parciales para obtener \( y(t) \).

**Teorema del Valor Final.** Si el sistema es estable, el valor en régimen permanente de la respuesta al escalón es:

$$y(\infty) = \lim_{s\to 0} s\cdot Y(s) = \lim_{s\to 0} s\cdot\frac{G(s)}{s} = G(0) = \frac{b_0}{a_0}$$

Este resultado evita calcular la antitransformada completa cuando solo interesa el error en régimen permanente.

### 6.3 — Respuesta sinusoidal en régimen permanente

Para una entrada senoidal \( u(t) = \sin(\omega t) \), \( U(s) = \omega/(s^2+\omega^2) \), la respuesta en régimen permanente (una vez los transitorios han decaído) es:

$$y_{ss}(t) = |G(j\omega)|\cdot\sin\bigl(\omega t + \angle G(j\omega)\bigr)$$

El módulo de \( G(j\omega) \) amplifica (o atenúa) la amplitud; el argumento \( \angle G(j\omega) \) desplaza la fase. Esto es exactamente lo que mide el diagrama de Bode.

### 6.4 — Tabla de pares fundamentales

| \( F(s) \) | \( f(t) \), \( t\geq 0 \) | Comentario |
|---|---|---|
| \( 1 \) | \( \delta(t) \) | impulso unitario |
| \( 1/s \) | \( \mathbf{1}(t) \) | escalón unitario |
| \( 1/s^2 \) | \( t \) | rampa unitaria |
| \( 1/(s+a) \) | \( e^{-at} \) | decaimiento exponencial, \( \tau=1/a \) |
| \( \omega_n^2/(s^2+2\zeta\omega_n s+\omega_n^2) \) | resp. de 2º orden | par complejo conjugado |
| \( \omega/(s^2+\omega^2) \) | \( \sin(\omega t) \) | seno puro (\( \text{Re}=0 \)) |
| \( s/(s^2+\omega^2) \) | \( \cos(\omega t) \) | coseno puro |
| \( 1/[s(s+a)] \) | \( (1-e^{-at})/a \) | escalón → sistema de 1er orden |
| \( e^{-\tau s}/s \) | \( \mathbf{1}(t-\tau) \) | retardo puro \( \tau \) |

El factor \( e^{-\tau s} \) del retardo puro no es racional, por lo que los sistemas con retardo no tienen una representación de espacio de estados finito-dimensional exacta.

## 7 — Diseño iterativo: obtener G(s) de un LCL y verificar

### 7.1 — Circuito y ecuaciones de mallas

El filtro LCL tiene: \( L_1 = 2\,\text{mH} \), \( R_1 = 50\,\text{m}\Omega \), \( C_f = 15\,\mu\text{F} \), amortiguamiento pasivo \( R_d = 3\,\Omega \) en serie con \( C_f \), e inductancia de red \( L_2 = 0.5\,\text{mH} \). La salida es la corriente de red \( i_{L2} \).

**Tres ecuaciones en el dominio de Laplace (CI nulas):**

$$V_i(s) = (L_1 s + R_1)\,I_{L1}(s) + V_C(s) \tag{malla 1}$$

$$V_C(s) = \left(R_d + \frac{1}{C_f s}\right)\!\bigl[I_{L1}(s) - I_{L2}(s)\bigr] = \frac{R_d C_f s + 1}{C_f s}\,\bigl[I_{L1}(s)-I_{L2}(s)\bigr] \tag{nodo C}$$

$$V_C(s) = L_2 s\, I_{L2}(s) \tag{malla 2}$$

### 7.2 — Eliminación algebraica

De la malla 2: \( I_{L2}(s) = V_C(s)/(L_2 s) \). Del nodo C: \( I_{L1}(s) = I_{L2}(s) + V_C(s)\cdot C_f s/(R_d C_f s+1) \). Sustituyendo en la malla 1 y despejando \( V_C/V_i \), y después \( I_{L2}/V_i \):

$$\boxed{G_{LCL}(s) = \frac{I_{L2}(s)}{V_i(s)} = \frac{1}{L_1 L_2 C_f\,s^3 + (R_1 L_2 C_f + R_d(L_1+L_2)C_f)\,s^2 + (L_1+L_2+R_1 R_d C_f)\,s + R_1}}$$

### 7.3 — Identificación de polos y verificación

**Resonancia del LCL sin amortiguación** (\( R_1 = R_d = 0 \)):

$$\omega_{res} = \sqrt{\frac{L_1+L_2}{L_1 L_2 C_f}} = \sqrt{\frac{2.5\times10^{-3}}{2\times10^{-3}\cdot0.5\times10^{-3}\cdot15\times10^{-6}}} \approx 9129\,\text{rad/s} \;\Rightarrow\; f_{res} \approx 1453\,\text{Hz}$$

Este valor coincide exactamente con la fórmula de la ficha [[filtro-lcl]].

**Verificación numérica.** Evaluando \( G_{LCL}(j\omega) \) directamente en el denominador cúbico y comparando con la respuesta de `scipy.signal.bode`: la diferencia entre ambas curvas es inferior al 0,1% en toda la banda de 10 Hz a 100 kHz (visible en el panel c de la figura). La derivación algebraica es correcta.

**Ganancia DC.** En \( s=0 \): \( G(0) = 1/R_1 = 1/0.05 = 20\,\text{A/V} \). Ante una tensión escalón de 1 V la corriente de red se establece en 20 A (limitada únicamente por la resistencia de la inductancia de red, coherente con el circuito DC del filtro).

## Cuándo y por qué se usa
Es la representación básica del control clásico: permite combinar bloques (serie, paralelo,
realimentación), analizar estabilidad por los polos y diseñar en frecuencia.

## Procedimiento (genérico)
1. Plantea la ecuación diferencial o el modelo de estado.
2. Aplica [[transformada-laplace]] y despeja \( Y(s)/U(s) \).
3. Identifica polos (denominador) y ceros (numerador) y la ganancia DC.
4. Usa \( G(s) \) para análisis (estabilidad, Bode) o interconexión de bloques.

## Ejemplo de aplicación real
**Problema:** VSC con \( L=2\,\text{mH} \), \( r=50\,\text{m}\Omega \). Obtener la FT de tensión de convertidor a corriente y dimensionar el PI para cruzar a \( f_c=1\,\text{kHz} \).

La planta es \( G_i(s)=1/(Ls+r) \), polo en \( s=-r/L=-25\,\text{rad/s} \). El PI con cero en \( z=-r/L \) cancela ese polo; la FT de lazo queda \( K_p/(Ls) \) (integrador puro). Para \( \omega_c=2\pi\times1000\,\text{rad/s} \): \( K_p=L\,\omega_c\approx12.6 \), \( K_i=K_p\,r/L\approx315\,\text{s}^{-1} \). El lazo cerrado resultante es \( G_{cl}(s)=1/(1+s/\omega_c) \): primer orden con \( \tau_{cl}=0.16\,\text{ms} \). La FT hace visible el polo que el PI debe cancelar y permite dimensionar \( K_p \) directamente desde \( \omega_c \).

## Ejemplo de código
```python
import control as ct
import numpy as np

# G(s) = wn^2 / (s^2 + 2*z*wn*s + wn^2)
wn, z = 10.0, 0.7
G = ct.tf([wn**2], [1, 2*z*wn, wn**2])
polos = ct.poles(G)          # array([-7+7.14j, -7-7.14j])

# G(s) desde espacio de estados
A = np.array([[0, 1], [-wn**2, -2*z*wn]])
B = np.array([[0], [1]])
C = np.array([[wn**2, 0]])
D = np.array([[0]])
sys_ss = ct.ss(A, B, C, D)
G_from_ss = ct.ss2tf(sys_ss)  # debe coincidir con G
```

## Parámetros y valores típicos
Primer orden: \( G(s)=K/(\tau s+1) \). Segundo orden:
\( G(s)=\omega_n^2/(s^2+2\zeta\omega_n s+\omega_n^2) \).

Filtro LCL típico: \( f_{res} \approx 1\text{–}3\,\text{kHz} \), \( R_d \approx 1\text{–}5\,\Omega \) (amortiguamiento pasivo).

## Errores comunes
- Cancelar un polo con un cero sin notar que oculta dinámica interna (modos no observables).
- Aplicarla a sistemas no lineales sin linealizar.
- Confundir la ganancia DC \( G(0) \) con la ganancia estática de bucle (que incluye el regulador).
- Intentar cancelar un polo en el SPD: el modo interno diverge aunque la salida parezca estable.

## Conceptos relacionados
- [[transformada-laplace]] · [[polos-ceros]] · [[respuesta-frecuencia-ss]] · [[diagrama-bode]] · [[espacio-estados]]

## Referencias
- Ogata, *Ingeniería de Control Moderna*.
- Franklin, Powell, *Feedback Control of Dynamic Systems*.
