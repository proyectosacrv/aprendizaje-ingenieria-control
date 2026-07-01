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

## Generalización — válido para cualquier función derivable
Nada en esta derivación usa que \( f \) sea \( e^{-x} \) o \( \sqrt{1-x} \): solo que tenga suficientes derivadas en \( a \). Por eso el mismo procedimiento da \( \sin\theta\approx\theta \) (linealizar un ángulo pequeño), \( (1+x)^n\approx1+nx \) (binomio para \( x \) pequeño), o la linealización de un modelo de estados \( \dot{\mathbf{x}}=\mathbf{f}(\mathbf{x},\mathbf{u}) \) alrededor de un punto de equilibrio (ver [[linealizacion-teoria]] y, en su versión numérica con Jacobianos, [[linealizacion-numerica]]).

<div class="cfig"><img src="figuras/series-taylor-aprox.png" alt="comparacion de e^-x y su aproximacion de Taylor de orden 1, 2 y 3 mostrando como mejora la aproximacion cerca de x=0 y se degrada lejos"><div class="cap">\(e^{-x}\) (negro) frente a sus polinomios de Taylor de orden 1, 2 y 3 en \(a=0\): cerca de \(x=0\) todos coinciden con la curva real; lejos, cada orden adicional retrasa un poco más dónde empieza a separarse, pero todos acaban divergiendo.</div></div>

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

## Uso en proyectos
- 01 / 02: la linealización del modelo no lineal en el punto de operación ([[linealizacion-teoria]]) y las aproximaciones de \( \omega_d\approx\omega_n \) y \( 1-e^{-4\pi\zeta}\approx4\pi\zeta \) en la deducción de \( Q=1/(2\zeta) \) ([[factor-calidad-q]]) son aplicaciones directas de esta serie.

## Conceptos relacionados
- [[linealizacion-teoria]] · [[linealizacion-numerica]] · [[frecuencias-segundo-orden]] · [[factor-calidad-q]] · [[resonancia-rlc]]

## Referencias
- Apostol, *Calculus*, Vol. 1.
- Strang, *Calculus*, MIT OpenCourseWare.
