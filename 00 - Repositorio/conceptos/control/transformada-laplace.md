---
titulo: Transformada de Laplace
slug: transformada-laplace
categoria: control
tipo: concepto
nivel: basico
proyectos: []
objetivos: [pasar del dominio del tiempo al dominio s para analizar sistemas lineales]
tags: [laplace, dominio-s, transformada, basico, control]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-30
relacionados: [funcion-transferencia, polos-ceros, diagrama-bode]
referencias:
  - "Ogata, Ingeniería de Control Moderna, Pearson"
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

El polo en \( s=a \) refleja directamente la dinámica: \( a<0 \) (exponencial que decae) ⇒ polo en el semiplano izquierdo ⇒ estable. Con \( a=-1/\tau \) sale \( 1/(s+1/\tau) \), el polo del RC del ejemplo. Para la senoide basta usar \( \sin\omega t=\tfrac{1}{2j}(e^{j\omega t}-e^{-j\omega t}) \) y sumar dos de estas.

## Cuándo y por qué se usa
Para analizar y diseñar sistemas lineales: resolver su respuesta, obtener la función de
transferencia y razonar sobre estabilidad y frecuencia. Es el lenguaje común del control clásico.

## Procedimiento (genérico)
1. Escribe la ecuación diferencial del sistema.
2. Aplica la transformada (deriva → multiplica por \( s \)).
3. Despeja la relación salida/entrada \( \to \) función de transferencia.
4. Analiza en \( s \) (polos, Bode) o antitransforma para volver al tiempo.

## Ejemplo de aplicación real
**Problema:** Circuito RC con \( R=1\,\text{k}\Omega \), \( C=10\,\mu\text{F} \) excitado con un escalón de 10 V. Obtener la tensión de salida en el tiempo.

La ecuación diferencial es \( RC\,\dot{v}_o+v_o=v_{in} \). Aplicando Laplace con condiciones iniciales nulas: \( (\tau s+1)V_o(s)=V_{in}(s) \), con \( \tau=RC=10\,\text{ms} \). Para \( V_{in}(s)=10/s \): \( V_o(s)=10/[s(\tau s+1)] \). Antitransformando: \( v_o(t)=10(1-e^{-t/\tau}) \). El 63 % se alcanza en \( \tau=10\,\text{ms} \), el 99 % en \( 5\tau=50\,\text{ms} \). La transformada convierte la ODE en álgebra, permite identificar el polo en \( s=-1/\tau=-100\,\text{rad/s} \) y prever directamente la velocidad de respuesta.

## Ejemplo de código
```python
import sympy as sp
t, s = sp.symbols('t s'); f = sp.exp(-2*t)
F = sp.laplace_transform(f, t, s)[0]      # 1/(s+2)
```

## Parámetros y valores típicos
Transformadas frecuentes: escalón \( \to 1/s \); exponencial \( e^{-at} \to 1/(s+a) \); senoide
\( \sin\omega t \to \omega/(s^2+\omega^2) \).

## Errores comunes
- Olvidar las condiciones iniciales (la regla simple vale con condiciones nulas).
- Aplicarla a sistemas no lineales (solo vale para lineales / linealizados).

## Conceptos relacionados
- [[funcion-transferencia]] · [[polos-ceros]] · [[diagrama-bode]]

## Referencias
- Ogata, *Ingeniería de Control Moderna*.
