---
titulo: Transformada de Laplace
slug: transformada-laplace
categoria: control
tipo: concepto
nivel: basico
proyectos: []
objetivos: [pasar del dominio del tiempo al dominio s para analizar sistemas lineales, dominar tablas y teoremas, aplicar fracciones parciales]
tags: [laplace, dominio-s, transformada, fracciones-parciales, valor-final, convolusion, basico, control]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [funcion-transferencia, polos-ceros, diagrama-bode, transformada-z]
referencias:
  - "Ogata, Ingeniería de Control Moderna, Pearson"
  - "Kreyszig, Advanced Engineering Mathematics"
---

## Definición
Herramienta matemática que convierte una función del tiempo \( f(t) \) en una función de una
variable compleja \( s \). Transforma las ecuaciones diferenciales (difíciles) en ecuaciones
algebraicas (fáciles), y es la base de la función de transferencia.

## Fundamento teórico
La transformada se define como:
$$ F(s) = \mathcal{L}\{f(t)\} = \int_0^\infty f(t)\,e^{-st}\,dt, \qquad s=\sigma+j\omega $$
Su propiedad clave: **la derivación en el tiempo se convierte en multiplicar por \( s \)** (con
condiciones iniciales nulas):
$$ \mathcal{L}\!\left\{\frac{df}{dt}\right\} = s\,F(s), \qquad
   \mathcal{L}\!\left\{\int_0^t f\,d\tau\right\} = \frac{F(s)}{s} $$
Así, una ecuación diferencial lineal se vuelve un polinomio en \( s \). La parte real \( \sigma \)
gobierna el crecimiento/decaimiento y la imaginaria \( \omega \) la oscilación.

<div class="cfig"><img src="figuras/transformada-laplace-pares.png" alt="senales en el tiempo y sus polos en s"><div class="cap">Cada señal del tiempo tiene su imagen en el plano s: la exponencial e^{−2t} ↔ un polo en s=−2; la oscilación amortiguada ↔ un par de polos complejos. σ marca el decaimiento y ω la frecuencia.</div></div>

## 1 — Por qué \( \mathcal{L}\{f'\}=sF-f(0) \) (integración por partes)
**Paso 1 — partir de la definición.** Aplica la definición a la derivada:

$$ \mathcal{L}\!\left\{\frac{df}{dt}\right\}=\int_0^\infty f'(t)\,e^{-st}\,dt $$

**Paso 2 — integrar por partes.** Con \( u=e^{-st} \) (luego \( du=-s\,e^{-st}dt \)) y \( dv=f'(t)\,dt \) (luego \( v=f(t) \)), la fórmula \( \int u\,dv=uv-\int v\,du \) da:

$$ \int_0^\infty f'(t)e^{-st}dt=\Big[\,f(t)e^{-st}\,\Big]_0^\infty-\int_0^\infty f(t)\,(-s)e^{-st}\,dt $$

**Paso 3 — evaluar el término de frontera.** En \( t\to\infty \), \( e^{-st}\to0 \) (para \( \mathrm{Re}(s) \) suficientemente grande, región de convergencia); en \( t=0 \), \( f(0)e^{0}=f(0) \). El corchete vale \( 0-f(0)=-f(0) \).

**Paso 4 — reconocer la integral restante.** La integral que queda es \( s\int_0^\infty f(t)e^{-st}dt=s\,F(s) \). Reuniendo:

$$ \boxed{\;\mathcal{L}\{f'(t)\}=s\,F(s)-f(0)\;} $$

Con \( f(0)=0 \) se recupera la regla simple "derivar = multiplicar por \( s \)". El término \( f(0) \) es lo que inyecta las **condiciones iniciales** en el dominio \( s \).

## 2 — La transformada de la exponencial \( e^{at} \)
**Paso 1 — aplicar la definición.** Junta las dos exponenciales en una sola:

$$ \mathcal{L}\{e^{at}\}=\int_0^\infty e^{at}e^{-st}\,dt=\int_0^\infty e^{-(s-a)t}\,dt $$

**Paso 2 — integrar la exponencial.** La primitiva de \( e^{-(s-a)t} \) es \( -\dfrac{1}{s-a}e^{-(s-a)t} \). Evaluando entre \( 0 \) e \( \infty \), el límite superior se anula si \( \mathrm{Re}(s)>a \):

$$ \mathcal{L}\{e^{at}\}=\left[-\frac{1}{s-a}e^{-(s-a)t}\right]_0^\infty=0-\left(-\frac{1}{s-a}\right)=\boxed{\;\frac{1}{s-a}\;} $$

El polo en \( s=a \) refleja directamente la dinámica: \( a<0 \) (exponencial que decae) ⇒ polo en el semiplano izquierdo ⇒ estable. Con \( a=-1/\tau \) sale \( 1/(s+1/\tau) \), el polo del RC del ejemplo.

## 3 — Tabla de transformadas fundamentales: derivaciones de las más importantes

### Escalón unitario \( 1(t) \to 1/s \)
Aplica la definición con \( f(t)=1 \):
$$ \mathcal{L}\{1(t)\}=\int_0^\infty e^{-st}\,dt=\left[-\frac{1}{s}e^{-st}\right]_0^\infty=0-\left(-\frac{1}{s}\right)=\frac{1}{s} $$
El polo en \( s=0 \) refleja que el escalón no decae; si \( \mathrm{Re}(s)\leq0 \) la integral diverge (región de convergencia: \( \mathrm{Re}(s)>0 \)).

### Rampa \( t \to 1/s^2 \)
Usando la propiedad de integración \( \mathcal{L}\{\int_0^t f\,d\tau\}=F(s)/s \): la rampa es la integral del escalón, \( t=\int_0^t 1\,d\tau \). Luego:
$$ \mathcal{L}\{t\}=\frac{\mathcal{L}\{1\}}{s}=\frac{1/s}{s}=\frac{1}{s^2} $$
Doble polo en \( s=0 \) → diverge más lentamente en el plano \( s \) y da una respuesta rampa que crece sin límite.

### Senoide \( \sin(\omega t) \to \omega/(s^2+\omega^2) \)
Expresa la senoide mediante exponenciales complejas:
$$ \sin(\omega t)=\frac{e^{j\omega t}-e^{-j\omega t}}{2j} $$
Aplicando la transformada de \( e^{at} \) del Apartado 2 a cada término:
$$ \mathcal{L}\{\sin(\omega t)\}=\frac{1}{2j}\left(\frac{1}{s-j\omega}-\frac{1}{s+j\omega}\right)=\frac{1}{2j}\cdot\frac{2j\omega}{s^2+\omega^2}=\frac{\omega}{s^2+\omega^2} $$
Los polos en \( s=\pm j\omega \) están sobre el eje imaginario: la senoide no crece ni decae.

### Coseno \( \cos(\omega t) \to s/(s^2+\omega^2) \)
El coseno es la parte real de \( e^{j\omega t} \). Como \( \mathcal{L}\{e^{j\omega t}\}=1/(s-j\omega) \), la parte real es:
$$ \mathcal{L}\{\cos(\omega t)\}=\mathrm{Re}\!\left\{\frac{1}{s-j\omega}\right\}=\mathrm{Re}\!\left\{\frac{s+j\omega}{s^2+\omega^2}\right\}=\frac{s}{s^2+\omega^2} $$

### Impulso de Dirac \( \delta(t) \to 1 \)
El impulso se puede definir como el límite de un pulso rectangular de anchura \( \epsilon \) y altura \( 1/\epsilon \) cuando \( \epsilon\to0 \). Su transformada:
$$ \mathcal{L}\{\delta(t)\}=\int_0^\infty \delta(t)\,e^{-st}\,dt=e^{-s\cdot0}=1 $$
Por la propiedad de selección del impulso. Alternativamente: el escalón tiene Laplace \( 1/s \); el impulso es su derivada → Laplace \( s\cdot(1/s)=1 \).

### Tabla completa de los 8 pares fundamentales

| \( f(t) \), \( t\geq0 \) | \( F(s) \) | Polo(s) |
|---|---|---|
| \( \delta(t) \) | \( 1 \) | ninguno (polo en \(\infty\)) |
| \( 1(t) \) | \( 1/s \) | \( s=0 \) |
| \( t \) | \( 1/s^2 \) | doble en \( s=0 \) |
| \( e^{-at} \) | \( 1/(s+a) \) | \( s=-a \) |
| \( \sin(\omega t) \) | \( \omega/(s^2+\omega^2) \) | \( s=\pm j\omega \) |
| \( \cos(\omega t) \) | \( s/(s^2+\omega^2) \) | \( s=\pm j\omega \) |
| \( e^{-at}\sin(\omega t) \) | \( \omega/[(s+a)^2+\omega^2] \) | \( s=-a\pm j\omega \) |
| \( e^{-at}\cos(\omega t) \) | \( (s+a)/[(s+a)^2+\omega^2] \) | \( s=-a\pm j\omega \) |

## 4 — Teorema del valor inicial y final

### Teorema del valor inicial
Si \( f(t) \) y \( f'(t) \) son ambas transformables:
$$ \lim_{t\to 0^+}f(t)=\lim_{s\to\infty}s\,F(s) $$
**Derivación:** De la fórmula de derivación \( \mathcal{L}\{f'\}=sF(s)-f(0) \), cuando \( s\to\infty \) la integral \( \int_0^\infty f'(t)e^{-st}dt\to0 \) porque el factor \( e^{-st} \) aplasta la integral. Queda \( 0=\lim_{s\to\infty}[sF(s)-f(0^+)] \), de donde el resultado.

### Teorema del valor final
Si **todos los polos de \( s\,F(s) \) tienen parte real estrictamente negativa** (o en \( s=0 \)):
$$ \lim_{t\to\infty}f(t)=\lim_{s\to 0}s\,F(s) $$
**Derivación:** Igual que antes pero \( s\to0 \). En ese límite \( e^{-st}\to1 \) y la integral \( \int_0^\infty f'(t)dt=f(\infty)-f(0) \). Sustituyendo en la fórmula de derivación:
$$ f(\infty)-f(0^+)=\lim_{s\to0}[sF(s)-f(0^+)] \implies \lim_{s\to0}sF(s)=f(\infty) $$

### Aplicación al lazo de corriente
Sea el lazo de corriente PI con planta \( G(s)=1/L_1 s \) e integrador \( K_i/s \). La función de bucle cerrado al escalón \( I^*(s)=I^*/s \):
$$ I(s)=\frac{K_p s + K_i}{L_1 s^2 + K_p s + K_i}\cdot\frac{I^*}{s} $$
Por el teorema del valor final (los polos de \( sI(s) \) están en el SPIz si \( K_p,K_i>0 \)):
$$ \lim_{t\to\infty}i(t)=\lim_{s\to0}s\cdot I(s)=\frac{K_i}{K_i}\cdot I^*=I^* $$
La corriente llega exactamente al valor de referencia en régimen permanente, sin error estático, gracias al integrador.

### Peligro: el teorema no aplica a sistemas inestables
Si \( F(s) \) tiene polos con \( \mathrm{Re}>0 \), \( f(t)\to\infty \) pero \( \lim_{s\to0}sF(s) \) puede dar un valor finito falso. Antes de aplicar el teorema del valor final, verificar que el sistema es estable.

## 5 — El teorema de convolución: \( G(s)\cdot U(s) = g(t)*u(t) \)

### Enunciado
Si \( Y(s)=G(s)\cdot U(s) \) entonces:
$$ y(t)=\int_0^t g(\tau)\,u(t-\tau)\,d\tau = g(t)*u(t) $$

### Derivación
La convolución en el tiempo se demuestra partiendo de la definición de las dos transformadas. Sea \( y(t)=\mathcal{L}^{-1}\{G(s)U(s)\} \):
$$ G(s)U(s)=\left(\int_0^\infty g(\tau)e^{-s\tau}d\tau\right)\!\left(\int_0^\infty u(\sigma)e^{-s\sigma}d\sigma\right) $$

Agrupando los dos exponentes \( e^{-s(\tau+\sigma)} \) y haciendo el cambio de variable \( t=\tau+\sigma \) (con \( \sigma=t-\tau \geq0 \)):
$$ G(s)U(s)=\int_0^\infty e^{-st}\!\left(\int_0^t g(\tau)\,u(t-\tau)\,d\tau\right)dt=\mathcal{L}\{g*u\} $$

Por tanto \( Y(s)=G(s)U(s) \leftrightarrow y(t)=g(t)*u(t) \).

### Interpretación física
\( g(t) \) es la **respuesta al impulso** del sistema: cómo responde si la entrada es un pulso infinitamente estrecho y alto en \( t=0 \). Para una entrada genérica \( u(t) \), se puede pensar que \( u(t) \) es una sucesión de impulsos de peso \( u(\tau)\,d\tau \) en los instantes \( \tau \). La respuesta al impulso en \( \tau \) llega "retrasada" en \( (t-\tau) \) y escalada por \( u(\tau) \). La integral de convolución suma todas esas contribuciones. La función \( g(t) \) es literalmente la "memoria" del sistema: cuánto pesa cada entrada pasada en la salida presente.

### Ejemplo completo: G(s)=1/(s+1), u(t)=escalón
$$ Y(s)=\frac{1}{s+1}\cdot\frac{1}{s}=\frac{1}{s(s+1)} $$

Por fracciones parciales (ver Apartado 6): \( Y(s)=\tfrac{1}{s}-\tfrac{1}{s+1} \), luego \( y(t)=1-e^{-t} \).

Verificación por convolución directa (con \( g(t)=e^{-t} \), \( u(t)=1 \)):
$$ y(t)=\int_0^t e^{-\tau}\cdot1\,d\tau=\left[-e^{-\tau}\right]_0^t=1-e^{-t} \checkmark $$

## 6 — La transformada inversa: fracciones parciales

### Principio
Cualquier \( Y(s) \) racional (cociente de polinomios en \( s \)) se puede descomponer en una suma de términos simples cuya antitransformada se lee directamente de la tabla.

### Polo simple en \( s=p \)
Si \( Y(s)=N(s)/D(s) \) y \( D(s)=(s-p)\cdot\tilde D(s) \) con \( \tilde D(p)\neq0 \), el residuo de ese polo es:
$$ A_p = \lim_{s\to p}(s-p)\cdot Y(s) $$
y contribuye el término \( A_p\,e^{pt} \) a \( y(t) \). Si \( p=-a<0 \), ese término decae; si \( p>0 \), crece.

### Par de polos complejos conjugados
Si \( D(s) \) tiene el factor \( (s+\sigma)^2+\omega^2 \), el par de polos \( -\sigma\pm j\omega \) no se trata como dos polos simples reales (serían complejos): se deja el factor cuadrático y se determina \( (As+B) \) en el numerador. La antitransformada da \( e^{-\sigma t}(C\cos\omega t+D\sin\omega t) \).

### Ejemplo completo paso a paso: \( Y(s)=\dfrac{2s+3}{(s+1)(s+2)} \)

**Paso 1 — forma de fracciones parciales.** Dos polos simples reales, \( p_1=-1 \), \( p_2=-2 \):
$$ Y(s) = \frac{A}{s+1}+\frac{B}{s+2} $$

**Paso 2 — residuo en \( p_1=-1 \):**
$$ A=\lim_{s\to-1}(s+1)\cdot\frac{2s+3}{(s+1)(s+2)}=\frac{2(-1)+3}{-1+2}=\frac{1}{1}=1 $$

**Paso 3 — residuo en \( p_2=-2 \):**
$$ B=\lim_{s\to-2}(s+2)\cdot\frac{2s+3}{(s+1)(s+2)}=\frac{2(-2)+3}{-2+1}=\frac{-1}{-1}=1 $$

**Paso 4 — antitransformar:**
$$ Y(s)=\frac{1}{s+1}+\frac{1}{s+2} \implies \boxed{y(t)=e^{-t}+e^{-2t},\quad t\geq0} $$

**Verificación:** \( Y(0^+) \to \lim_{s\to\infty}sY(s)=\lim_{s\to\infty}s\cdot(2s+3)/(s^2+3s+2)=2 \). Y \( e^0+e^0=2 \). ✓

## 7 — Laplace vs Fourier vs transformada Z

### Fourier como caso particular
La transformada de Fourier se define con \( s=j\omega \) (solo el eje imaginario):
$$ \mathcal{F}\{f\}=\int_{-\infty}^\infty f(t)e^{-j\omega t}dt $$
Solo converge para señales con energía finita o para señales periódicas con distribuciones (impulsos en la frecuencia). La Laplace incluye el factor \( e^{-\sigma t} \) adicional que hace converger la integral incluso para señales crecientes (siempre que \( \sigma \) sea suficientemente grande). Geometricamente: Fourier evalúa la transformada solo sobre el eje \( s=j\omega \); Laplace la evalúa en todo el semiplano de convergencia.

### La transformada Z: el análogo discreto
En sistemas digitales el tiempo es discreto: \( t=k\,T_s \). La transformada Z es:
$$ X(z)=\sum_{k=0}^\infty x[k]\,z^{-k} $$
La relación con Laplace es \( z=e^{sT_s} \): un polo en \( s=-a \) (exponencial decreciente) corresponde a \( z=e^{-aT_s} \), dentro del círculo unidad. La estabilidad en Z: todos los polos con \( |z|<1 \) (análogo a \( \mathrm{Re}(s)<0 \)).

### Por qué Laplace para control
Laplace captura **transitorios** y **condiciones iniciales**: la fórmula \( \mathcal{L}\{f'\}=sF-f(0) \) inyecta el estado inicial directamente. La función de transferencia \( G(s)=Y(s)/U(s) \) con condiciones iniciales nulas describe la dinámica pura del sistema independientemente del estado de partida. Esto facilita el diseño de controladores (ganancia, márgenes de fase/ganancia) y el análisis de estabilidad (polos en el plano \( s \)).

<div class="cfig"><img src="figuras/transformada-laplace-analisis.png" alt="Analisis completo: pares, valor final, convolución, fracciones parciales"><div class="cap">Panel (a): seis señales fundamentales y la posición de sus polos en el plano s. (b): teorema del valor final aplicado a Y(s)=5/[s(s+3)]. (c): convolución g(t)=e^{-t} con escalón da y(t)=1-e^{-t}. (d): descomposición en fracciones parciales de Y(s)=(2s+3)/[(s+1)(s+2)] y su antitransformada.</div></div>

## Cuándo y por qué se usa
Para analizar y diseñar sistemas lineales: resolver su respuesta, obtener la función de
transferencia y razonar sobre estabilidad y frecuencia. Es el lenguaje común del control clásico.

## Procedimiento (genérico)
1. Escribe la ecuación diferencial del sistema.
2. Aplica la transformada (deriva → multiplica por \( s \)).
3. Despeja la relación salida/entrada → función de transferencia.
4. Analiza en \( s \) (polos, Bode) o antitransforma para volver al tiempo.
5. Para la antitransformada: fracciones parciales → tabla.
6. Antes de aplicar el valor final, verifica estabilidad del sistema.

## Ejemplo de aplicación real
**Problema:** Circuito RC con \( R=1\,\text{k}\Omega \), \( C=10\,\mu\text{F} \) excitado con un escalón de 10 V. Obtener la tensión de salida en el tiempo.

La ecuación diferencial es \( RC\,\dot{v}_o+v_o=v_{in} \). Aplicando Laplace con condiciones iniciales nulas: \( (\tau s+1)V_o(s)=V_{in}(s) \), con \( \tau=RC=10\,\text{ms} \). Para \( V_{in}(s)=10/s \): \( V_o(s)=10/[s(\tau s+1)] \). Fracciones parciales: \( V_o(s)=10/s-10\tau/(\tau s+1)=10/s-10/(s+1/\tau) \). Antitransformando: \( v_o(t)=10(1-e^{-t/\tau}) \). Valor final: \( \lim_{s\to0}s\cdot V_o(s)=10 \) V. ✓

## Ejemplo de código
```python
import sympy as sp
t, s = sp.symbols('t s'); f = sp.exp(-2*t)
F = sp.laplace_transform(f, t, s)[0]      # 1/(s+2)

# Fracciones parciales con sympy
Y = (2*s+3)/((s+1)*(s+2))
sp.apart(Y, s)   # 1/(s+1) + 1/(s+2)

# Valor final
Y_vf = 5/(s*(s+3))
vf = sp.limit(s*Y_vf, s, 0)   # 5/3
```

## Parámetros y valores típicos
Transformadas frecuentes: escalón \( \to 1/s \); exponencial \( e^{-at} \to 1/(s+a) \); senoide
\( \sin\omega t \to \omega/(s^2+\omega^2) \); rampa \( t \to 1/s^2 \). El teorema del valor final solo aplica si todos los polos de \( s\,F(s) \) tienen \( \mathrm{Re}<0 \) o están en \( s=0 \).

## Errores comunes
- Olvidar las condiciones iniciales (la regla simple vale con condiciones nulas).
- Aplicarla a sistemas no lineales (solo vale para lineales / linealizados).
- Aplicar el teorema del valor final a sistemas inestables: da un valor finito falso.
- Confundir la transformada de Laplace unilateral (\( t\geq0 \)) con la bilateral (\( -\infty<t<\infty \)).

## Conceptos relacionados
- [[funcion-transferencia]] · [[polos-ceros]] · [[diagrama-bode]]

## Referencias
- Ogata, *Ingeniería de Control Moderna*, Pearson.
- Kreyszig, *Advanced Engineering Mathematics*.
