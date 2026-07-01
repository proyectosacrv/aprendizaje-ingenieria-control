---
titulo: Teoría de linealización
slug: linealizacion-teoria
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [aproximar un sistema no lineal por uno lineal para analizar y disenar]
tags: [linealizacion, jacobiano, equilibrio, pequena-senal, validez]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [linealizacion-numerica, equilibrio-fsolve, representacion-espacio-estados, modelado-sistemas]
referencias:
  - "Khalil, Nonlinear Systems, Prentice Hall 2002 (cap. 4)"
---

## Definición
Aproximar un sistema no lineal \( \dot{\mathbf{x}}=\mathbf{f}(\mathbf{x},\mathbf{u}) \) por un
modelo **lineal** válido en un entorno de un punto de operación (equilibrio). Es lo que permite
aplicar toda la teoría de control lineal a sistemas que en realidad no lo son.

## Fundamento teórico
En un equilibrio \( (\mathbf{x}_e,\mathbf{u}_e) \) con \( \mathbf{f}(\mathbf{x}_e,\mathbf{u}_e)=0 \),
se desarrolla \( \mathbf{f} \) en serie de Taylor y se conserva el primer orden. Con las
desviaciones \( \Delta\mathbf{x}=\mathbf{x}-\mathbf{x}_e \):
$$ \Delta\dot{\mathbf{x}} = A\,\Delta\mathbf{x} + B\,\Delta\mathbf{u}, \qquad
   A=\left.\frac{\partial \mathbf{f}}{\partial \mathbf{x}}\right|_e, \quad
   B=\left.\frac{\partial \mathbf{f}}{\partial \mathbf{u}}\right|_e $$
\( A \) y \( B \) son los **Jacobianos** evaluados en el equilibrio.

**Validez** (teorema de Hartman–Grobman): si el equilibrio es **hiperbólico** (ningún autovalor
de \( A \) sobre el eje imaginario), el comportamiento cualitativo del no lineal cerca del
equilibrio coincide con el del linealizado. Es un resultado **local** (pequeña señal): vale
mientras las desviaciones sean pequeñas. Falla con no linealidades fuertes (saturación,
zona muerta) o en equilibrios no hiperbólicos.

<div class="cfig"><img src="figuras/linealizacion-teoria-validez.png" alt="respuesta no lineal vs linealizada en pequena y gran senal"><div class="cap">Un péndulo no lineal frente a su modelo linealizado: en pequeña señal ($\theta_0$ pequeño) ambas respuestas coinciden y el análisis lineal es válido; en gran señal divergen, porque la aproximación de primer orden solo vale en un entorno del equilibrio. El teorema de Hartman–Grobman garantiza la equivalencia local si el equilibrio es hiperbólico.</div></div>

## 1 — De dónde sale \( \Delta\dot{\mathbf{x}}=A\,\Delta\mathbf{x}+B\,\Delta\mathbf{u} \): Taylor de primer orden
La forma linealizada no se postula: es el primer término no nulo del desarrollo de Taylor de \( \mathbf{f} \) alrededor del equilibrio. Lo derivamos primero en escalar (una variable) y luego en vectorial, donde aparece el Jacobiano.

**Paso 1 — Taylor escalar.** Para una función suave \( f(x,u) \) de una entrada y un estado, el desarrollo alrededor de \( (x_e,u_e) \) hasta primer orden es:

$$ f(x,u)\approx f(x_e,u_e)+\left.\frac{\partial f}{\partial x}\right|_e (x-x_e)+\left.\frac{\partial f}{\partial u}\right|_e (u-u_e)+\;\underbrace{O(\|\cdot\|^2)}_{\text{se desprecia}} $$

**Paso 2 — usar la condición de equilibrio.** Por definición de equilibrio, \( f(x_e,u_e)=0 \). El término constante se **anula**: ese es el motivo de linealizar justo en el equilibrio (si se hiciera en otro punto quedaría un residuo \( \neq 0 \) y \( A \) perdería sentido). Quedan solo los términos lineales en las desviaciones \( \Delta x=x-x_e \), \( \Delta u=u-u_e \).

**Paso 3 — la derivada de la desviación es la de \( x \).** Como \( x_e \) es constante, \( \dot{\Delta x}=\dot x-\dot x_e=\dot x=f(x,u) \). Sustituyendo el Paso 1 ya sin término constante:

$$ \dot{\Delta x}\approx \left.\frac{\partial f}{\partial x}\right|_e \Delta x+\left.\frac{\partial f}{\partial u}\right|_e \Delta u $$

es decir \( \dot{\Delta x}=a\,\Delta x+b\,\Delta u \) con \( a,b \) escalares: ya es un sistema lineal.

**Paso 4 — caso vectorial: el Jacobiano.** Con \( \mathbf{x}\in\mathbb{R}^n \), \( \mathbf{u}\in\mathbb{R}^m \) y \( \mathbf{f} \) vectorial, la derivada parcial respecto a un vector es la **matriz Jacobiana**: la fila \( i \) son las derivadas de \( f_i \), la columna \( j \) la derivada respecto a \( x_j \):

$$ A=\left.\frac{\partial \mathbf{f}}{\partial \mathbf{x}}\right|_e=
\begin{bmatrix}\dfrac{\partial f_1}{\partial x_1}&\cdots&\dfrac{\partial f_1}{\partial x_n}\\[1.2em]\vdots&\ddots&\vdots\\[0.6em]\dfrac{\partial f_n}{\partial x_1}&\cdots&\dfrac{\partial f_n}{\partial x_n}\end{bmatrix}_{e},\qquad
B=\left.\frac{\partial \mathbf{f}}{\partial \mathbf{u}}\right|_e\in\mathbb{R}^{n\times m} $$

**Paso 5 — resultado.** El mismo argumento de los Pasos 1–3, componente a componente, da la ecuación de pequeña señal:

$$ \boxed{\;\Delta\dot{\mathbf{x}}=A\,\Delta\mathbf{x}+B\,\Delta\mathbf{u},\qquad A=\left.\frac{\partial \mathbf{f}}{\partial \mathbf{x}}\right|_e,\;\;B=\left.\frac{\partial \mathbf{f}}{\partial \mathbf{u}}\right|_e\;} $$

Los autovalores de este \( A \) son los polos del sistema en ese punto de operación, y alimentan directamente la [[representacion-espacio-estados]]. Cuando \( \mathbf{f} \) no se deriva a mano, las parciales se aproximan por diferencias finitas (ver [[linealizacion-numerica]]): perturbar cada \( x_j \) y medir el cambio en \( \mathbf{f} \) reconstruye columna a columna el Jacobiano.

## 2 — El punto de equilibrio: cómo encontrarlo y verificarlo

Antes de linealizar hay que saber dónde hacerlo. El punto de equilibrio \( (\mathbf{x}_e, \mathbf{u}_e) \) es aquel en que el sistema no cambia de estado:

$$ \mathbf{f}(\mathbf{x}_e,\mathbf{u}_e)=\mathbf{0} $$

Esto es un sistema de \( n \) ecuaciones (en general no lineales) en \( n \) incógnitas.

**Método analítico.** Cuando \( \mathbf{f} \) tiene estructura simple, las ecuaciones se pueden resolver a mano. Ejemplo: el péndulo \( \ddot\theta=-\frac{g}{l}\sin\theta \) tiene equilibrios en \( \theta_e=0 \) (estable) y \( \theta_e=\pi \) (inestable), ambos con \( \dot\theta_e=0 \).

**Método numérico con fsolve.** Para sistemas de orden alto (como el GFM de \( n=15 \)) se recurre a un solver de sistemas no lineales:

```python
from scipy.optimize import fsolve

def f_residuo(x_flat):
    x = x_flat[:n]; u = u_e   # entrada fija en el punto de operación
    return sistema_nl(x, u)   # retorna f(x,u) como vector

x_e = fsolve(f_residuo, x0=x_inicial, full_output=False)
```

La convergencia depende de la calidad del punto inicial \( x_0 \). Una estrategia robusta es simular el sistema con la entrada nominal hasta que la transitoria se amortigua, y usar el estado final como \( x_0 \).

**El equilibrio del GFM.** Para un generador GFM con droop de frecuencia, el equilibrio en potencia activa satisface

$$ P_e = \frac{EV}{X}\sin(\delta_e), \qquad P_e = P_\mathrm{ref} + \frac{1}{m_p}(\omega_0 - \omega_e) $$

En régimen permanente \( \omega_e=\omega_0 \) (la referencia es \( \omega_0 \)), luego \( P_e=P_\mathrm{ref} \) y

$$ \delta_e = \arcsin\!\left(\frac{P_\mathrm{ref}\,X}{EV}\right) $$

El equilibrio de potencia reactiva determina \( v_{Cd,e}, v_{Cq,e} \), y a partir de ahí los demás estados del filtro y del controlador en su valor estacionario.

**Unicidad y múltiples equilibrios.** La ecuación \( \sin(\delta_e)=\frac{P_\mathrm{ref}X}{EV} \) tiene **dos soluciones** en \( [0,\pi] \) para \( P_\mathrm{ref}>0 \): \( \delta_e \) y \( \pi-\delta_e \). El primero (\( \delta_e<90° \)) es estable; el segundo (\( \delta_e>90° \)) es inestable (autovalor del modo de potencia en el semiplano derecho). Ambos equilibrios coexisten, lo que implica que si una perturbación grande lleva el sistema más allá de \( \delta=90° \) sin recuperación, el GFM puede perder sincronismo.

**Verificación del equilibrio.** La prueba más directa es integrar el sistema no lineal partiendo de \( \mathbf{x}=\mathbf{x}_e \) y comprobar que \( \mathbf{x}(t)\equiv\mathbf{x}_e \):

```python
from scipy.integrate import solve_ivp

sol = solve_ivp(lambda t, x: f(x, u_e), [0, 1.0], x_e, max_step=1e-4)
error_max = np.max(np.abs(sol.y[:, -1] - x_e))
print(f"Deriva desde equilibrio: {error_max:.2e}")  # debe ser < 1e-10
```

Si el error no es numérico (< \( 10^{-10} \)) sino mayor, el punto hallado por `fsolve` no era un verdadero equilibrio (residuo numérico mal tolerado o función objetivo mal definida).

## 3 — Validez local: la región de linealización

El linealizado es una **aproximación**: solo es fiel al no lineal dentro de cierta región alrededor del equilibrio. Esta región no tiene una frontera exacta, pero se puede estimar comparando las respuestas.

**Criterio empírico.** Para la mayoría de no linealidades suaves en convertidores, el linealizado es una buena aproximación mientras

$$ \frac{\|\Delta\mathbf{x}\|}{\|\mathbf{x}_e\|} \lesssim 10{-}20\,\% $$

Más allá de ese rango, los términos de segundo orden del Taylor ya no son despreciables.

**Análisis cuantitativo de error.** La diferencia entre la respuesta no lineal y la linealizada es proporcional a la curvatura de \( \mathbf{f} \). Formalmente, si se define la perturbación inicial como \( \Delta\mathbf{x}_0=\epsilon\,\hat{\mathbf{v}} \) (de amplitud \( \epsilon \) en la dirección \( \hat{\mathbf{v}} \)):

$$ \|\mathbf{x}_\mathrm{NL}(t)-\mathbf{x}_\mathrm{lin}(t)\| = O(\epsilon^2) $$

el error crece cuadráticamente con la amplitud de la perturbación. Para \( \epsilon $ pequeño es despreciable; para \( \epsilon $ del orden del equilibrio, ya no.

**Comparación práctica.** Para caracterizar la región de validez se simulan tres casos con el mismo sistema a 1%, 10% y 30% de perturbación y se mide el error:

```python
x_e_nom = equilibrio(...)      # punto nominal
for frac in [0.01, 0.10, 0.30]:
    dx0 = frac * x_e_nom       # perturbación del frac%
    sol_nl  = solve_ivp(nl_ode,  [0, T], x_e_nom + dx0, ...)
    sol_lin = solve_ivp(lin_ode, [0, T], dx0, ...)  # linealizado, en desviaciones
    err_pico = np.max(np.abs(sol_nl.y.T - (x_e_nom + sol_lin.y.T)))
    print(f"{frac*100:.0f}% pert -> error pico: {err_pico:.3f} pu")
```

**Contexto en convertidores.** El análisis de impedancia (barrido en frecuencia con inyección de pequeña señal) trabaja con amplitudes del 1–5% de la nominal: el linealizado es totalmente válido. El análisis de faltas trifásicas (\( \Delta V=100\% \)) no lo es: la diferencia entre el modelo lineal y el real es del orden del propio estado, y las saturaciones de corriente hacen que el modelo lineal sea inútil.

<div class="cfig"><img src="figuras/linealizacion-teoria-analisis.png" alt="linealización: análisis avanzado"><div class="cap">(a) Péndulo no lineal (trazo continuo) vs linealizado (trazo discontinuo) para cuatro amplitudes iniciales: para θ₀=5° las curvas son indistinguibles; para θ₀=90° el linealizado predice un sinusoide que en realidad tarda más del doble en completar el ciclo. (b) La función sin(δ) y su tangente en δ₀=30°: la aproximación lineal tiene error inferior al 5% en un rango de ±20° alrededor del punto de operación. (c) Autovalores del modo de potencia del GFM a medida que P/Sn varía de 0 a 1: Re(λ) se acerca a cero (amortiguamiento se reduce) y |Im(λ)| también decrece porque Ks→0. (d) Respuesta del GFM ante perturbaciones del 5%, 20% y 40% de Sn: para 5% el linealizado es indistinguible del no lineal; para 40% la diferencia es apreciable.</div></div>

## 4 — Linealización de no linealidades frecuentes en convertidores

Muchas no linealidades que aparecen en el modelado de convertidores tienen estructura conocida. Derivar su linealización analíticamente es más fiable que el Jacobiano numérico y da más intuición.

**1. \( \sin(\delta) \) en el lazo de potencia.** En el ángulo de potencia \( \delta=\delta_0+\Delta\delta \):

$$ \sin(\delta_0+\Delta\delta)=\sin(\delta_0)\cos(\Delta\delta)+\cos(\delta_0)\sin(\Delta\delta) \approx \sin(\delta_0)+\cos(\delta_0)\,\Delta\delta $$

La potencia eléctrica \( P_e=\frac{EV}{X}\sin(\delta) \) se linealiza como

$$ \Delta P_e = \underbrace{\frac{EV}{X}\cos(\delta_0)}_{K_s}\,\Delta\delta $$

donde \( K_s \) es la **rigidez de sincronismo** (synchronizing coefficient). Es la pendiente de la curva \( P\text{-}\delta \) en el punto de operación. Disminuye cuando \( \delta_0 \) se acerca a 90° y se anula exactamente en \( \delta_0=90° \), lo que corresponde al límite de estabilidad estática.

**2. Producto \( v \cdot i \) (potencia).** Partiendo de \( (v_0+\Delta v)(i_0+\Delta i)=v_0 i_0+v_0\Delta i+i_0\Delta v+\Delta v\Delta i \), descartando el término cuadrático:

$$ \Delta(v\cdot i)=v_0\,\Delta i+i_0\,\Delta v $$

Esto aparece en la potencia \( p=vi \), en la fuerza contraelectromotriz de un motor \( e=k\omega i \), etc. El resultado es lineal en las dos perturbaciones, con los valores del punto de operación como coeficientes.

**3. Carga de potencia constante (CPL): \( P_0/V \).** La corriente que demanda una CPL es \( i_\mathrm{CPL}=P_0/V \). Expandiendo en serie alrededor de \( V_0 \):

$$ \frac{P_0}{V_0+\Delta V}=\frac{P_0}{V_0}\cdot\frac{1}{1+\Delta V/V_0}\approx\frac{P_0}{V_0}\left(1-\frac{\Delta V}{V_0}\right)=\frac{P_0}{V_0}-\frac{P_0}{V_0^2}\Delta V $$

La perturbación de corriente es \( \Delta i_\mathrm{CPL}=-\frac{P_0}{V_0^2}\Delta V \): el signo negativo revela la **resistencia incremental negativa** de la CPL. Cuando la tensión baja, la CPL demanda más corriente (para mantener \( P_0 \) constante), lo que puede desestabilizar el bus DC si la impedancia de la fuente no tiene suficiente margen de ganancia.

**4. La PLL.** Un PLL SRF busca \( v_q=V\sin(\Delta\theta)\approx V\cdot\Delta\theta=0 \). Linealizado alrededor de \( \Delta\theta=0 \):

$$ \Delta v_q = V_0\,\Delta\theta $$

La ganancia es \( V_0 \): si la tensión cae (red débil), la sensibilidad de la PLL se reduce y el lazo de seguimiento se vuelve más lento. Esto explica la inestabilidad de la PLL en red débil: el cociente \( K_p/(V_0) \) sube efectivamente si se mantiene \( K_p \) fijo y baja \( V_0 \), sobrexcitando el lazo de fase.

**Tabla resumen.**

| No linealidad | Linealización en \( (x_0,u_0) \) | Coeficiente clave |
|---------------|----------------------------------|-------------------|
| \( \sin(\delta) \) | \( \sin(\delta_0)+\cos(\delta_0)\,\Delta\delta \) | \( K_s=\frac{EV}{X}\cos(\delta_0) \) |
| \( v\cdot i \) | \( v_0\Delta i + i_0\Delta v \) | Coeficientes \( v_0, i_0 \) |
| \( P_0/V \) | \( P_0/V_0 - (P_0/V_0^2)\Delta V \) | Resistencia incremental \( -V_0^2/P_0 \) |
| \( V\sin(\Delta\theta) \) | \( V_0\,\Delta\theta \) | Ganancia de red \( V_0 \) |

## 5 — El Jacobiano numérico: diferencias finitas

Cuando \( \mathbf{f}(\mathbf{x},\mathbf{u}) \) no tiene expresión analítica cerrada (función definida implícitamente, modelo en bloques, código heredado), el Jacobiano se aproxima evaluando \( \mathbf{f} \) en puntos vecinos.

**Diferencia adelante (primer orden).** Para la columna \( j \) del Jacobiano:

$$ \frac{\partial \mathbf{f}}{\partial x_j}\bigg|_e \approx \frac{\mathbf{f}(\mathbf{x}_e+\varepsilon\,\mathbf{e}_j,\mathbf{u}_e)-\mathbf{f}(\mathbf{x}_e,\mathbf{u}_e)}{\varepsilon} $$

donde \( \mathbf{e}_j \) es el \( j \)-ésimo vector canónico. El error de truncación es \( O(\varepsilon) \): cuanto más pequeño \( \varepsilon \), mejor la aproximación... hasta que el error de redondeo empieza a dominar. El compromiso óptimo está en

$$ \varepsilon_\mathrm{opt} \approx \sqrt{\varepsilon_\mathrm{maq}} \approx \sqrt{2.2\times 10^{-16}} \approx 1.5\times 10^{-8} $$

para aritmética de doble precisión (float64).

**Diferencia centrada (segundo orden).** La fórmula centrada elimina el término de primer orden del error:

$$ \frac{\partial \mathbf{f}}{\partial x_j}\bigg|_e \approx \frac{\mathbf{f}(\mathbf{x}_e+\varepsilon\,\mathbf{e}_j,\mathbf{u}_e)-\mathbf{f}(\mathbf{x}_e-\varepsilon\,\mathbf{e}_j,\mathbf{u}_e)}{2\varepsilon} $$

El error es \( O(\varepsilon^2) \): con \( \varepsilon=10^{-5} \) el error de truncación es \( 10^{-10} \), mucho mejor que la diferencia adelante. El precio es el doble de evaluaciones de \( \mathbf{f} \). Para \( n \) estados se necesitan \( 2n+1 \) evaluaciones (una en el equilibrio más dos por estado) frente a \( n+1 \) de la diferencia adelante.

**Verificación contra el analítico.** La prueba de calidad del Jacobiano numérico es compararlo con el analítico calculado a mano, elemento a elemento:

```python
def jacobiano_numerico(f, x_e, u_e, eps=1e-7):
    n = len(x_e); f0 = f(x_e, u_e)
    A_num = np.zeros((n, n))
    for j in range(n):
        ej = np.zeros(n); ej[j] = 1.0
        fp = f(x_e + eps*ej, u_e)
        fm = f(x_e - eps*ej, u_e)
        A_num[:, j] = (fp - fm) / (2*eps)
    return A_num

A_num  = jacobiano_numerico(f_sistema, x_e, u_e)
A_anl  = jacobiano_analitico(x_e, u_e)   # calculado a mano
err_rel = np.max(np.abs(A_num - A_anl)) / np.max(np.abs(A_anl))
print(f"Error relativo máx: {err_rel:.2e}")   # debe ser < 1e-5
```

Si el error es mayor de \( 10^{-4} \), sospechar: error en el analítico, en el paso, o en la implementación de \( f \).

**Costo computacional.** Construir el Jacobiano numérico de un sistema de \( n=15 \) estados requiere 31 evaluaciones de \( \mathbf{f} \). Si \( \mathbf{f} \) incluye integraciones numéricas o llamadas a Simulink, el costo puede ser significativo; en ese caso la diferencia adelante (solo \( n+1=16 \) evaluaciones) puede ser más práctica.

## 6 — Linealizar el GFM en varios puntos de operación

Los parámetros del linealizado (autovalores, respuesta en frecuencia, margen de ganancia) dependen del punto de operación. Para el GFM esto se traduce en que la estabilidad no es global: el sistema puede estar bien en vacío y marginal cerca de la potencia nominal.

**Los tres puntos canónicos.** Se toman \( P=\{0,\,0.5S_n,\,S_n\} \) como representativos del rango de operación. En cada uno el ángulo de equilibrio y la rigidez de sincronismo son:

| Punto | \( \delta_0 \) | \( K_s=\frac{EV}{X}\cos(\delta_0) \) | Descripción |
|-------|----------------|---------------------------------------|-------------|
| \( P=0 \) | 0° | \( EV/X \) (máximo) | Vacío: máxima estabilidad |
| \( P=0.5S_n \) | 30° | \( 0.866\,EV/X \) | Nominal: operación habitual |
| \( P=S_n \) | 90° | \( \approx 0 \) | Límite: estabilidad marginal |

**Autovalores del modo de potencia en los tres puntos.** El sistema de 2 estados (simplificado: \( \delta, P_f \)) linealizado alrededor de \( (\delta_0, P_0) \) tiene

$$ A_\mathrm{pot}=\begin{bmatrix}0 & -m_p\omega_0 \\ \omega_f K_s & -\omega_f\end{bmatrix} $$

El polinomio característico es \( s^2+\omega_f s+\omega_f m_p\omega_0 K_s=0 \), con

$$ \omega_n=\sqrt{\omega_f m_p\omega_0 K_s}, \qquad \zeta=\frac{\omega_f}{2\omega_n}=\frac{1}{2}\sqrt{\frac{\omega_f}{m_p\omega_0 K_s}} $$

Con los parámetros nominales (\( L=0.1\,\mathrm{pu} \), \( E=V=1\,\mathrm{pu} \), \( m_p=0.5\% \), \( \omega_f=2\pi\cdot 10\,\mathrm{rad/s} \)):

| Punto | \( K_s \) | \( \omega_n \) [rad/s] | \( \zeta \) | \( \lambda_{1,2} \) |
|-------|-----------|------------------------|-------------|---------------------|
| \( P=0 \) | 10 pu | ~56 rad/s | ~0.56 | \( -31\pm j46 \) |
| \( P=0.5S_n \) | 8.66 pu | ~52 rad/s | ~0.60 | \( -31\pm j41 \) |
| \( P=S_n \) | ~0 | ~0 | →∞ | \( -63,\,-0 \) |

Cerca de \( P=S_n \) el modo de potencia pierde su carácter oscilatorio (los autovalores se separan en el eje real), y uno de ellos se aproxima a cero: el GFM está al límite de la estabilidad estática.

**Por qué el GFM puede perder sincronía.** Si \( K_s\to 0 \) un autovalor se acerca al origen. Cualquier perturbación de potencia que no pueda ser absorbida (por ejemplo, una bajada de tensión en la red que reduce \( V \)) puede hacer que ese autovalor cruce el eje imaginario. Una vez que \( \delta \) supera 90°, \( K_s \) se vuelve negativo y el autovalor entra en el semiplano derecho: el sistema es inestable y \( \delta \) diverge. Si no hay limitación de corriente, el inversor "cae" fuera de sincronismo.

```python
# Barrido de P/Sn y cálculo de autovalores del modo de potencia
mp = 0.005; wf = 2*np.pi*10; w0 = 2*np.pi*50; L_pu = 0.1
P_vec = np.linspace(0.01, 0.99, 300)
for P in P_vec:
    d0 = np.arcsin(P * L_pu)          # E=V=1
    Ks = np.cos(d0) / L_pu
    A2 = np.array([[0, -mp*w0], [wf*Ks, -wf]])
    eigs = np.linalg.eigvals(A2)
    ...
```

## 7 — Comparativa lineal vs no lineal: cuándo falla

El linealizado es la herramienta estándar de análisis de pequeña señal, pero tiene límites estructurales que el ingeniero debe conocer para no cometer errores de diseño graves.

**1. Saturación de corriente.** El inversor tiene un límite físico de corriente (tipicamente 1.1–1.5 pu). En el modelo lineal no existe ninguna saturación: si una perturbación grande lo lleva a estados donde la corriente debería saturarse, el linealizado predice una respuesta que el hardware nunca verá. Para diseñar el comportamiento durante satración (current limiting) se necesita el modelo no lineal completo o un modelo híbrido que incluya el clamp.

**2. Múltiples equilibrios.** El linealizado solo ve el entorno de un equilibrio. Si existen dos equilibrios estables (como ocurre en sistemas de osciladores acoplados), el linealizado no puede predecir hacia cuál converge el sistema tras una perturbación grande: eso depende de las cuencas de atracción, que son un concepto global no lineal.

**3. Faltas trifásicas (\( \Delta V=1\,\mathrm{pu} \)).** Una falta trifásica equivale a \( V\to 0 \), es decir, \( \Delta V=-V_0=-1\,\mathrm{pu} \). Esto es un 100% de la tensión nominal: el linealizado, válido para perturbaciones pequeñas, está completamente fuera de su dominio. La respuesta real incluye corriente de pico muy superior al límite de saturación, transitorios de modo común, y potencialmente pérdida de sincronismo. Solo la simulación no lineal en el dominio temporal captura este comportamiento.

**4. Sistemas con retardo puro.** Si el modelo incluye un retardo de computación \( e^{-sT_d} \), su linealización alrededor de cualquier punto es la misma función de transferencia (el retardo es ya una función lineal de la señal). Sin embargo, para análisis de estabilidad a alta frecuencia, aproximar \( e^{-sT_d}\approx 1-sT_d \) (Padé de orden 1) introduce un cero en el semiplano derecho que puede provocar conclusiones incorrectas sobre el margen de fase. Usar la aproximación de Padé de orden ≥2 o el modelo de tiempo discreto es más fiable.

**Tabla de fallas del linealizado.**

| Situación | Por qué falla | Alternativa |
|-----------|---------------|-------------|
| Saturación de corriente | No linealidad con discontinuidad de la derivada | Modelo híbrido o simulación completa |
| Múltiples equilibrios | Solo ve el entorno de uno | Análisis de cuencas de atracción, Lyapunov |
| Falta trifásica | \(\|\Delta V\|/\|V_0\|=1\gg 20\%\) | Simulación no lineal (EMT) |
| Retardo con Padé de orden 1 | Cero en SPD que no existe | Padé ≥2 o tiempo discreto |
| Control con zona muerta | No linealidad no diferenciable | Análisis de plano de fases o DF |

**Regla práctica para el proyecto.** En los proyectos GFM y GFL, el linealizado es la herramienta principal para todo el análisis de pequeña señal: rango de frecuencias de 0.1 Hz a 10 kHz, con perturbaciones del orden del 1–5% de la nominal. El modelo no lineal se reserva para validar el diseño en los escenarios de falta y para verificar que el control de saturación de corriente no destabiliza el lazo.

## Cuándo y por qué se usa
Para diseñar y analizar control con herramientas lineales (polos, Bode, impedancia, LQR). El
régimen de gran señal (faltas, saturación) requiere otros métodos (simulación no lineal).

## Procedimiento (genérico)
1. Halla el equilibrio resolviendo \( \mathbf{f}(\mathbf{x}_e,\mathbf{u}_e)=0 \) (ver [[equilibrio-fsolve]]).
2. Calcula los Jacobianos \( A,B \) (y \( C,D \) de la salida): analíticamente o
   **numéricamente** (ver [[linealizacion-numerica]]).
3. Comprueba que el equilibrio es hiperbólico (ningún autovalor en el eje imaginario).
4. Recuerda el rango de validez: solo pequeña señal alrededor de ese punto.

## Ejemplo de código
```python
# linealizacion analitica de un pendulo: d/dt[theta, w] ; equilibrio theta=0
# A = [[0,1],[-g/l*cos(theta_e), -b/m]]  evaluado en theta_e=0  -> [[0,1],[-g/l,-b/m]]
```

## Parámetros y valores típicos
La región de validez depende de la curvatura de \( \mathbf{f} \); en convertidores, las
perturbaciones de pequeña señal (p.ej. inyección de impedancia con amplitud pequeña) están en
régimen lineal; las faltas, no.

## Errores comunes
- Linealizar fuera del equilibrio (residuo \( \neq 0 \)) → \( A \) sin sentido.
- Aplicar conclusiones del linealizado en gran señal (cuando hay saturación/current limiting).
- Equilibrio no hiperbólico (autovalor en \( j\omega \)): el linealizado no decide la estabilidad.
- Usar diferencia adelante con \( \varepsilon \) demasiado grande (\(10^{-3}\)) o demasiado pequeño (\(10^{-15}\)): error de truncación o de redondeo dominan.

## Uso en proyectos
- **01/02**: todo el análisis de estabilidad e impedancia parte de la linealización en el punto
  de operación; el régimen de gran señal (faltas) se trató por simulación temporal.

## Conceptos relacionados
- [[linealizacion-numerica]] · [[equilibrio-fsolve]] · [[representacion-espacio-estados]] · [[modelado-sistemas]]

## Referencias
- Khalil, *Nonlinear Systems*, cap. 4.
