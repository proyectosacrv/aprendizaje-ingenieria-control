---
titulo: Series de Taylor — aproximar una función por un polinomio
slug: series-taylor
categoria: control
tipo: concepto
nivel: basico
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [entender de dónde sale el polinomio de Taylor, cómo se deduce término a término y cuánto error comete al truncarlo]
tags: [taylor, aproximacion, linealizacion, serie, basico]
fecha_creacion: 2026-06-27
fecha_actualizacion: 2026-07-01
relacionados: [linealizacion-teoria, frecuencias-segundo-orden, factor-calidad-q, resonancia-rlc, linealizacion-numerica]
referencias:
  - "Apostol, Calculus, Vol. 1"
  - "Strang, Calculus, MIT OpenCourseWare"
---

## Definición
Una serie de Taylor sustituye una función \( f(x) \), que puede ser complicada, por un **polinomio** que coincide con ella (y con sus derivadas) en un punto \( x=a \). Cerca de \( a \) el polinomio es casi indistinguible de \( f \); lejos de \( a \) se separa. Es la herramienta detrás de casi toda aproximación "para \( x \) pequeño" que aparece en este repositorio: \( \sin\theta\approx\theta \), \( e^{-x}\approx1-x \), \( \sqrt{1-\zeta^2}\approx1-\zeta^2/2 \), la linealización de un modelo no lineal, etc. No es una propiedad de una función concreta: es un procedimiento genérico que se le puede aplicar a cualquier función derivable.

## Punto de partida — qué se le pide al polinomio
Se busca un polinomio \( P_n(x) \) de grado \( n \) que **comparta con \( f \) el valor y las primeras \( n \) derivadas** en el punto \( x=a \):

$$ P_n(a)=f(a), \quad P_n'(a)=f'(a), \quad P_n''(a)=f''(a),\ \dots,\ P_n^{(n)}(a)=f^{(n)}(a) $$

Esa es toda la idea: en vez de copiar \( f \) en todos sus puntos (imposible si es complicada), se le exige al polinomio que se "parezca" en un punto y en cómo cambia ahí (su pendiente, su curvatura, etc.). Cuantas más derivadas coincidan, mejor se pega el polinomio a \( f \) alrededor de \( a \).

## Desarrollo 1 — construir el polinomio término a término
Se escribe \( P_n(x) \) en potencias de \( (x-a) \), con coeficientes \( c_k \) por determinar:

$$ P_n(x)=c_0+c_1(x-a)+c_2(x-a)^2+c_3(x-a)^3+\dots+c_n(x-a)^n $$

**Paso 1 — coincidir el valor.** En \( x=a \) todos los términos con \( (x-a) \) se anulan, así que \( P_n(a)=c_0 \). Imponiendo \( P_n(a)=f(a) \):

$$ c_0=f(a) $$

**Paso 2 — coincidir la primera derivada.** Derivando \( P_n \): \( P_n'(x)=c_1+2c_2(x-a)+3c_3(x-a)^2+\dots \). En \( x=a \) solo sobrevive \( c_1 \), así que \( P_n'(a)=c_1 \). Imponiendo \( P_n'(a)=f'(a) \):

$$ c_1=f'(a) $$

**Paso 3 — coincidir la segunda derivada.** Derivando otra vez: \( P_n''(x)=2c_2+6c_3(x-a)+\dots \), luego \( P_n''(a)=2c_2 \). Imponiendo \( P_n''(a)=f''(a) \):

$$ c_2=\frac{f''(a)}{2} $$

**Paso 4 — el patrón general.** Cada vez que se deriva \( k \) veces el término \( c_k(x-a)^k \), el factor que sale al bajar los exponentes es \( k\cdot(k-1)\cdot(k-2)\cdots1=k! \) (las potencias mayores se anulan en \( x=a \) por tener todavía algún \( (x-a) \) sin derivar del todo). Así que, en general, \( P_n^{(k)}(a)=k!\,c_k \). Imponiendo \( P_n^{(k)}(a)=f^{(k)}(a) \):

$$ \boxed{\;c_k=\frac{f^{(k)}(a)}{k!}\;} $$

**Paso 5 — el polinomio de Taylor.** Sustituyendo los \( c_k \):

$$ f(x)\approx P_n(x)=\sum_{k=0}^{n}\frac{f^{(k)}(a)}{k!}\,(x-a)^k = f(a)+f'(a)(x-a)+\frac{f''(a)}{2!}(x-a)^2+\dots $$

Si \( a=0 \) se llama serie de Maclaurin (el caso más habitual en este repositorio: aproximar cerca de "sin perturbación").

## Desarrollo 2 — el error que se comete al truncar (por qué hace falta "\( x \) pequeño")
\( P_n \) no es \( f \): hay un resto \( R_n(x)=f(x)-P_n(x) \). La forma de Lagrange del resto dice que existe algún punto \( \xi \) entre \( a \) y \( x \) tal que:

$$ R_n(x)=\frac{f^{(n+1)}(\xi)}{(n+1)!}\,(x-a)^{n+1} $$

Es decir, el primer término que se descarta (el de orden \( n+1 \)) **domina el error**, y ese término crece con \( (x-a)^{n+1} \). Por eso la aproximación solo es buena si \( x \) está cerca de \( a \): el error decae con la distancia elevada a una potencia, así que alejarse poco ya penaliza mucho menos que alejarse del todo, pero alejarse del todo lo destruye. Truncar a primer orden (\( n=1 \)) es la aproximación más común ("linealizar"); el error que se comete es de orden \( (x-a)^2 \).

## Desarrollo 3 — dos ejemplos resueltos que aparecen en este repositorio
**Ejemplo A: \( e^{-x} \) en \( a=0 \).** Derivando: \( f(x)=e^{-x} \), \( f'(x)=-e^{-x} \), \( f''(x)=e^{-x} \), \( f'''(x)=-e^{-x} \)… cada derivada introduce un signo menos, así que \( f^{(k)}(0)=(-1)^k \). Con \( c_k=f^{(k)}(0)/k!=(-1)^k/k! \):

$$ e^{-x}=1-x+\frac{x^2}{2}-\frac{x^3}{6}+\dots $$

Truncando al primer orden, \( e^{-x}\approx1-x \); este es exactamente el paso que se usa en [[factor-calidad-q]] para aproximar \( 1-e^{-4\pi\zeta}\approx4\pi\zeta \).

**Ejemplo B: \( \sqrt{1-x} \) en \( a=0 \) (de dónde sale \( \omega_d\approx\omega_n \)).** Aquí \( f(x)=(1-x)^{1/2} \). Derivando con la regla de la cadena:

$$ f'(x)=\frac{1}{2}(1-x)^{-1/2}\cdot(-1)=-\frac{1}{2}(1-x)^{-1/2} \;\Rightarrow\; f'(0)=-\frac{1}{2} $$

$$ f''(x)=-\frac{1}{2}\cdot\left(-\frac{1}{2}\right)(1-x)^{-3/2}\cdot(-1)=-\frac{1}{4}(1-x)^{-3/2} \;\Rightarrow\; f''(0)=-\frac{1}{4} $$

Con \( c_1=f'(0)=-\tfrac12 \) y \( c_2=f''(0)/2=-\tfrac18 \):

$$ \sqrt{1-x}=1-\frac{x}{2}-\frac{x^2}{8}-\dots $$

**Por qué la serie entre \( \omega_d \) y \( \omega_n \) tiene exactamente esta forma.** La relación es \( \omega_d/\omega_n=\sqrt{1-\zeta^2} \) ([[frecuencias-segundo-orden]]). Sustituyendo \( x=\zeta^2 \) en el resultado de arriba:

$$ \frac{\omega_d}{\omega_n}=\sqrt{1-\zeta^2}=1-\frac{\zeta^2}{2}-\frac{\zeta^4}{8}-\dots $$

No es una fórmula nueva: es la misma serie binomial de \( \sqrt{1-x} \), con \( x \) sustituido por \( \zeta^2 \). Que solo aparezcan potencias **pares** de \( \zeta \) (\( \zeta^2 \), \( \zeta^4 \)…) no es casualidad: como la sustitución es \( x=\zeta^2 \), cada potencia \( x^m \) de la serie en \( x \) se convierte en \( \zeta^{2m} \), así que nunca puede salir un término en \( \zeta^1 \) o \( \zeta^3 \). Esto explica, de paso, por qué la aproximación \( \omega_d\approx\omega_n \) es tan buena incluso para \( \zeta \) moderado: su primer error es de orden \( \zeta^2 \) (cuadrático), mientras que el de \( e^{-x} \) en el Ejemplo A es de orden \( x=4\pi\zeta \) (lineal en \( \zeta \)) — de ahí que en [[factor-calidad-q]] la aproximación de la exponencial sea la que realmente domina el error, no la de \( \omega_d\approx\omega_n \).

## Desarrollo 4 — linealización de sin(δ) ≈ δ para δ pequeño

**Paso 1 — función de partida.** Se quiere aproximar \( f(\delta)=\sin\delta \) alrededor del punto de operación \( \delta=0 \) (ángulo nulo).

**Paso 2 — calcular derivadas en δ = 0.**

$$ f(0)=\sin0=0,\quad f'(\delta)=\cos\delta\;\Rightarrow\; f'(0)=1,\quad f''(\delta)=-\sin\delta\;\Rightarrow\; f''(0)=0 $$
$$ f'''(\delta)=-\cos\delta\;\Rightarrow\; f'''(0)=-1 $$

**Paso 3 — montar el polinomio de Maclaurin (\( a=0 \)).**

$$ \sin\delta = 0 + 1\cdot\delta + \frac{0}{2!}\delta^2 + \frac{-1}{3!}\delta^3 + \dots = \delta - \frac{\delta^3}{6} + \frac{\delta^5}{120} - \dots $$

**Paso 4 — truncar a primer orden.**

$$ \boxed{\sin\delta \approx \delta} \quad (\delta\text{ en radianes, }\delta\ll1) $$

El primer término descartado es \( -\delta^3/6 \), de modo que el error relativo es \( |\sin\delta-\delta|/|\delta|\approx\delta^2/6 \). Para \( \delta=10°\approx0.175\,\text{rad} \): error \( \approx0.175^2/6\approx0.5\,\% \). Para \( \delta=30°\approx0.524\,\text{rad} \): error \( \approx4.6\,\% \).

**Aplicación directa.** En la swing equation y en el modelo de línea de transmisión, la potencia transferida es \( P=P_{max}\sin\delta \). Para ángulos de operación pequeños (\( \delta<15° \)), la linealización \( \sin\delta\approx\delta \) convierte la ecuación no lineal en una EDO lineal, lo que permite diseñar reguladores lineales (estabilizadores de sistema de potencia, PSS).

## Generalización — válido para cualquier función derivable
Nada en esta derivación usa que \( f \) sea \( e^{-x} \) o \( \sqrt{1-x} \): solo que tenga suficientes derivadas en \( a \). Por eso el mismo procedimiento da \( \sin\theta\approx\theta \) (linealizar un ángulo pequeño), \( (1+x)^n\approx1+nx \) (binomio para \( x \) pequeño), o la linealización de un modelo de estados \( \dot{\mathbf{x}}=\mathbf{f}(\mathbf{x},\mathbf{u}) \) alrededor de un punto de equilibrio (ver [[linealizacion-teoria]] y, en su versión numérica con Jacobianos, [[linealizacion-numerica]]).

<div class="cfig"><img src="figuras/series-taylor-aprox.png" alt="comparacion de e^-x y su aproximacion de Taylor de orden 1, 2 y 3 mostrando como mejora la aproximacion cerca de x=0 y se degrada lejos"><div class="cap">\(e^{-x}\) (negro) frente a sus polinomios de Taylor de orden 1, 2 y 3 en \(a=0\): cerca de \(x=0\) todos coinciden con la curva real; lejos, cada orden adicional retrasa un poco más dónde empieza a separarse, pero todos acaban divergiendo.</div></div>

## 4 — Serie de Taylor para funciones de varias variables y el jacobiano

**Extensión a dos variables.** Para \( f(x,y) \) derivable en \( (x_0, y_0) \), la expansión de Taylor a primer orden es:

$$ f(x,y) \approx f(x_0,y_0) + \frac{\partial f}{\partial x}\bigg|_{(x_0,y_0)}\Delta x + \frac{\partial f}{\partial y}\bigg|_{(x_0,y_0)}\Delta y + O(\Delta^2) $$

donde \( \Delta x = x - x_0 \) y \( \Delta y = y - y_0 \). El término de primer orden es el **gradiente** de \( f \) evaluado en el punto de operación: un vector fila que contiene las derivadas parciales.

**Extensión vectorial: el jacobiano.** Para un sistema de \( n \) funciones de \( n \) variables \( \dot{\mathbf{x}} = \mathbf{f}(\mathbf{x}) \), la linealización alrededor del punto de equilibrio \( \mathbf{x}_0 \) produce:

$$ \Delta\dot{\mathbf{x}} = J\,\Delta\mathbf{x}, \qquad J_{ij} = \frac{\partial f_i}{\partial x_j}\bigg|_{\mathbf{x}_0} $$

La matriz \( J \) es el **jacobiano** de \( \mathbf{f} \), la extensión matricial del concepto de derivada para funciones vectoriales. Los autovalores de \( J \) determinan la estabilidad local del punto de equilibrio:
- Si todos los autovalores tienen parte real negativa: el equilibrio es estable.
- Si algún autovalor tiene parte real positiva: el equilibrio es inestable.
- Si algún autovalor está sobre el eje imaginario: hay que ir al análisis no lineal (Lyapunov).

**El jacobiano 8×8 del GFM.** Un modelo simplificado de GFM con droop tiene 8 estados: \( (\theta, \omega, P_{filtrada}, Q_{filtrada}, \varphi_d, \varphi_q, \gamma_d, \gamma_q) \) donde \( \varphi \) son los integradores del lazo de corriente y \( \gamma \) los del lazo de tensión. La linealización alrededor del punto de operación \( (\theta_0, \omega_0, P_0, Q_0, \dots) \) produce un jacobiano \( 8\times8 \) cuyos autovalores dan los modos del sistema: el modo electromecánico lento (droop, \( \approx 1\text{–}10\,\text{Hz} \)), los modos del lazo de corriente (rápido, \( \approx 0.5\text{–}2\,\text{kHz} \)) y los modos del filtro LCL.

## 5 — El radio de convergencia práctico: cuándo la linealización falla

**El error de la aproximación lineal de \( P(\delta) = (EV/X)\sin\delta \).** La linealización a primer orden alrededor de \( \delta_0 \) da:

$$ P(\delta) \approx P_0 + K_s \Delta\delta, \qquad P_0 = \frac{EV}{X}\sin\delta_0, \qquad K_s = \frac{EV}{X}\cos\delta_0 $$

El error relativo de esta aproximación para una perturbación \( \Delta\delta \) es:

$$ \epsilon_{rel} = \frac{|P_{exacta} - P_{lineal}|}{P_{max}} = \left|\sin(\delta_0+\Delta\delta) - \sin\delta_0 - \cos\delta_0\,\Delta\delta\right| $$

Usando la expansión de Taylor de \( \sin(\delta_0+\Delta\delta) \):

$$ \sin(\delta_0+\Delta\delta) = \sin\delta_0 + \cos\delta_0\,\Delta\delta - \frac{\sin\delta_0}{2}\,\Delta\delta^2 - \frac{\cos\delta_0}{6}\,\Delta\delta^3 + \dots $$

Así que el primer error es el término cuadrático:

$$ \epsilon_{rel} \approx \frac{\sin\delta_0}{2}\,\Delta\delta^2 $$

Para un umbral de error del 10% (\( \epsilon_{rel} < 0.1 \)):

$$ \Delta\delta_{max} = \sqrt{\frac{0.2}{\sin\delta_0}} $$

- Para \( \delta_0 = 30° \): \( \Delta\delta_{max} = \sqrt{0.2/0.5} = 0.632\,\text{rad} = 36.2° \). La aproximación es buena para perturbaciones de hasta ±36°.
- Para \( \delta_0 = 45° \): \( \Delta\delta_{max} = \sqrt{0.2/0.707} = 0.532\,\text{rad} = 30.5° \). El margen se reduce al aumentar \( \delta_0 \).
- Para \( \delta_0 = 60° \): \( \Delta\delta_{max} = \sqrt{0.2/0.866} = 0.481\,\text{rad} = 27.5° \).

**Regla práctica.** La linealización de \( P(\delta) \) es fiable (error < 10%) para \( |\Delta\delta| < 30° \) si \( \delta_0 < 30° \), y menos fiable para puntos de operación con ángulos altos (\( \delta_0 > 45° \)). En diseño de sistemas de potencia se suele limitar \( \delta_0 < 35° \) para tener margen de linealización razonable.

**Punto de linealización vs estabilidad transitoria.** La linealización solo es válida localmente cerca de \( \delta_0 \). Para perturbaciones grandes (cortocircuito, pérdida de generación), el sistema puede salir del dominio de validez de la linealización y hay que usar el análisis de la curva \( P\text{–}\delta \) no lineal (criterio del área igual, análisis de Lyapunov).

## 6 — Diseño iterativo: precisión de la linealización para el GFM del proyecto 01

Parámetros: \( E = V = 1\,\text{pu} \), \( X = 0.2\,\text{pu} \) (reactancia total), \( P_{max} = EV/X = 5\,\text{pu} \).

**Punto de operación 1: \( P_{ref} = 0.3\,\text{pu} \).**

$$ \delta_0 = \arcsin\!\left(\frac{P_{ref}}{P_{max}}\right) = \arcsin(0.3/5) = \arcsin(0.06) \approx 3.44° $$

Para \( \Delta P = 0.1\,\text{pu} \), la perturbación en ángulo es \( \Delta\delta = \Delta P / K_s \), con \( K_s = P_{max}\cos\delta_0 \approx 5 \times 0.998 = 4.99\,\text{pu/rad} \):

$$ \Delta\delta = 0.1/4.99 = 0.020\,\text{rad} = 1.15° $$

Error relativo: \( \epsilon \approx \sin(3.44°)/2 \times (0.020)^2 \approx 0.060/2 \times 4\times10^{-4} \approx 1.2\times10^{-5} \) → error despreciable.

**Punto de operación 2: \( P_{ref} = 0.5\,\text{pu} \).**

$$ \delta_0 = \arcsin(0.5/5) = \arcsin(0.10) \approx 5.74° $$

\( K_s = 5\cos(5.74°) \approx 4.975\,\text{pu/rad} \); \( \Delta\delta \approx 0.1/4.975 = 0.0201\,\text{rad} = 1.15° \).

Error relativo: \( \epsilon \approx \sin(5.74°)/2 \times (0.0201)^2 \approx 0.010/2 \times 4\times10^{-4} \approx 2\times10^{-6} \) → error aún menor.

**Punto de operación 3: \( P_{ref} = 0.7\,\text{pu} \).**

$$ \delta_0 = \arcsin(0.7/5) = \arcsin(0.14) \approx 8.05° $$

\( K_s = 5\cos(8.05°) \approx 4.951\,\text{pu/rad} \); \( \Delta\delta \approx 0.1/4.951 = 0.0202\,\text{rad} \).

Error relativo: \( \epsilon \approx \sin(8.05°)/2 \times (0.0202)^2 \approx 3\times10^{-6} \) → igualmente despreciable.

**Conclusión.** Para los ángulos de operación típicos de este GFM (\( \delta_0 < 10° \)), la linealización de \( P(\delta) \) introduce errores menores de \( 10^{-5} \) para perturbaciones de \( \Delta P = 0.1\,\text{pu} \). El modelo lineal es excelente para diseño de controladores en torno al punto de operación nominal. Solo pierde validez ante perturbaciones grandes (> 20° de oscilación de ángulo), que corresponden a situaciones de falta grave o pérdida de gran generación.

<div class="cfig"><img src="../figuras/series-taylor-analisis.png" alt="Series de Taylor: sin(x), P(delta), CPL y error de linealización"><div class="cap">(a) sin(x) y sus aproximaciones de Taylor de orden 1, 3, 5, 7: cada orden adicional extiende la validez a un rango mayor. (b) P(δ)=EV/X·sin(δ) y la linealización en δ₀=15°, 30°, 45°: el error crece con δ₀. (c) La CPL i=P/V y su linealización: pendiente negativa (resistencia negativa virtual). (d) Error de linealización del GFM vs ángulo de operación.</div></div>

## Cuándo y por qué se usa
Siempre que una expresión exacta es transcendente o no lineal y hace falta una fórmula cerrada y manejable: linealizar un sistema no lineal para diseñar un control lineal, simplificar \( 1-e^{-x} \) a \( x \), o \( \sqrt{1-\zeta^2} \) a \( 1-\zeta^2/2 \). Siempre a costa de un error que crece al alejarse del punto de expansión, y que conviene cuantificar (con el resto \( R_n \) o, más sencillo en la práctica, comparando numéricamente la aproximación con el valor exacto, como se hace en [[factor-calidad-q]]).

## Procedimiento (genérico)
1. Elige el punto de expansión \( a \) (normalmente \( a=0 \), el caso "sin perturbación").
2. Calcula \( f(a), f'(a), f''(a),\dots \) hasta el orden que necesites.
3. Forma \( c_k=f^{(k)}(a)/k! \) y monta el polinomio.
4. Decide cuántos términos conservar: cuantos más, mejor la aproximación, pero más complicada la fórmula. El primer término descartado da una estimación del error.
5. Comprueba numéricamente el rango de \( x \) donde el error es aceptable para tu aplicación.

## Ejemplo de código
```python
import numpy as np

def taylor_coefs(f, a, n, h=1e-4):
    """Coeficientes de Taylor por diferencias finitas (sin sympy)."""
    # derivadas sucesivas con diferencias centradas
    import math
    ck = []
    for k in range(n+1):
        # derivada k-esima aproximada
        coef = sum((-1)**i * math.comb(k, i) * f(a + (k/2 - i)*h) for i in range(k+1)) / h**k
        ck.append(coef / math.factorial(k))
    return ck

f = lambda x: np.exp(-x)
c = taylor_coefs(f, 0.0, 3)          # ~ [1, -1, 0.5, -0.1667]
x = np.linspace(-0.3, 0.3, 5)
P = sum(c[k]*x**k for k in range(len(c)))
print(np.exp(-x), P)                  # deben casi coincidir cerca de x=0
```

## Parámetros y valores típicos
- Aproximaciones de primer orden (linealización): error \( O(x^2) \), aceptable para \( |x|\lesssim0.1\text{–}0.2 \) según la función.
- En este repositorio: \( \zeta\lesssim0.05\text{–}0.1 \) es el rango donde \( e^{-4\pi\zeta}\approx1-4\pi\zeta \) y \( \sqrt{1-\zeta^2}\approx1-\zeta^2/2 \) son ambas fiables (ver tabla numérica en [[factor-calidad-q]]).

## Errores comunes
- Usar la aproximación lejos del punto de expansión sin comprobar el error (el polinomio diverge de \( f \) tarde o temprano, incluso si parece razonable cerca de \( a \)).
- Confundir "más términos siempre ayuda" con "siempre converge": fuera del radio de convergencia, añadir términos puede empeorar la aproximación.
- Olvidar que el orden del primer término descartado es el que manda en el error, no el número de términos conservados en sí.
- Mezclar el punto de expansión \( a \) con el punto de operación final \( x \): la serie es buena cerca de \( a \), no cerca de donde a uno le gustaría que fuera buena.

## 7 — Linealización mediante Taylor: Jacobiano y perturbaciones pequeñas

Para un sistema vectorial \(\dot{\mathbf{x}} = f(\mathbf{x}, \mathbf{u})\), la linealización alrededor del punto de equilibrio \((\mathbf{x}_0, \mathbf{u}_0)\) usa el Jacobiano:

$$\dot{\Delta\mathbf{x}} \approx \underbrace{\frac{\partial f}{\partial \mathbf{x}}\bigg|_{\mathbf{x}_0,\mathbf{u}_0}}_{A}\,\Delta\mathbf{x} + \underbrace{\frac{\partial f}{\partial \mathbf{u}}\bigg|_{\mathbf{x}_0,\mathbf{u}_0}}_{B}\,\Delta\mathbf{u}$$

El error de la linealización es \(O(\|\Delta\mathbf{x}\|^2)\): para perturbaciones pequeñas \(\|\Delta\mathbf{x}\| \ll 1\), el sistema linealizado es una buena aproximación. Para perturbaciones grandes (p.ej. cortocircuito), la no linealidad domina y el modelo lineal falla.

**Ejemplo: convertidor GFM con droop.** El modelo no lineal incluye \(P = (EV/X)\sin(\delta)\). Alrededor de \(\delta_0\):

$$\Delta P \approx \underbrace{\frac{EV}{X}\cos\delta_0}_{K_s}\,\Delta\delta$$

El Jacobiano para el sistema [δ, ω] es \(A = \begin{pmatrix}0 & 1 \\ -K_s/(m_p J) & -D/(m_p J)\end{pmatrix}\), con autovalores \(\lambda = -\zeta\omega_n \pm j\omega_n\sqrt{1-\zeta^2}\).

## 8 — Aproximación de Padé para retardos

El retardo puro \(e^{-sT}\) no es racional, pero se puede aproximar por una función racional usando Padé de orden (m,n):

$$e^{-sT} \approx \frac{N_m(s)}{D_n(s)}$$

La aproximación de Padé (1,1) es la más usada en control de convertidores:

$$e^{-sT} \approx \frac{1 - sT/2}{1 + sT/2}$$

Esta tiene el mismo módulo unitario que el retardo exacto (es una función todo-paso) y la misma fase hasta el primer orden. El error de fase:

$$\phi_{error} = \angle e^{-j\omega T} - \angle\frac{1-j\omega T/2}{1+j\omega T/2} \approx \frac{(\omega T)^3}{12}$$

Error < 5% para \(|\omega T| < 2\), es decir, para frecuencias hasta \(f < 1/(\pi T)\). Para \(T = 100\,\mu\text{s}\) (\(f_s = 10\,\text{kHz}\)): válido hasta \(f < 3.2\,\text{kHz}\) — cubre todo el rango de interés del control.

## 9 — Radio de convergencia y singularidades

La serie de Taylor de \(f(x)\) converge para \(|x - a| < R\), donde \(R\) es la distancia desde el punto de expansión \(a\) hasta la singularidad más cercana en el plano complejo:

$$R = |a - z_{sing,nearest}|$$

**Ejemplos relevantes:**
- \(1/(1+s/\omega_p)\): singularidad en \(s = -\omega_p\); la serie en \(s=0\) converge para \(|s| < \omega_p\).
- \(\sqrt{1-\zeta^2}\): singularidades en \(\zeta = \pm 1\); la serie en \(\zeta=0\) converge para \(|\zeta| < 1\) — toda la banda de sistemas subamortiguados.
- \(\ln(1+x)\): singularidad en \(x = -1\); la serie en \(x=0\) converge solo para \(|x| < 1\).

Para el control de convertidores, la variable de perturbación suele satisfacer \(|\Delta x| < 0.1\,\text{pu}\) en condiciones normales → bien dentro del radio de convergencia de las linealizaciones típicas.

## 10 — Taylor en modelos de convertidores: buck linealizado y perturbación de ciclo de trabajo

El convertidor buck con control de ciclo de trabajo \(d\) tiene el modelo en valor promediado:

$$v_o = d\cdot V_{dc}$$

Para una perturbación \(\hat{d}\) alrededor del ciclo de trabajo nominal \(D_0\):

$$\hat{v}_o = V_{dc}\,\hat{d}$$

Esta es exactamente la linealización de primer orden. El término de segundo orden \((\hat{d})^2 V_{dc}/2\) solo importa para perturbaciones grandes (\(|\hat{d}| > 0.05\)).

**Modelo dinámico linealizado del buck (control de modo corriente):**

$$\frac{\hat{v}_o(s)}{\hat{d}(s)} = \frac{V_{dc}/LC}{s^2 + s/(RC) + 1/(LC)}$$

El denominador es el polinomio de segundo orden del LCsalida, con \(\zeta = 1/(2R)\sqrt{L/C}\). Este modelo es válido para \(|\hat{v}_o| \ll V_{dc}\) — condición que el lazo de control debe garantizar en régimen permanente.

## Uso en proyectos
- 01 / 02: la linealización del modelo no lineal en el punto de operación ([[linealizacion-teoria]]) y las aproximaciones de \( \omega_d\approx\omega_n \) y \( 1-e^{-4\pi\zeta}\approx4\pi\zeta \) en la deducción de \( Q=1/(2\zeta) \) ([[factor-calidad-q]]) son aplicaciones directas de esta serie.

## Conceptos relacionados
- [[linealizacion-teoria]] · [[linealizacion-numerica]] · [[frecuencias-segundo-orden]] · [[factor-calidad-q]] · [[resonancia-rlc]]

## Referencias
- Apostol, *Calculus*, Vol. 1.
- Strang, *Calculus*, MIT OpenCourseWare.
