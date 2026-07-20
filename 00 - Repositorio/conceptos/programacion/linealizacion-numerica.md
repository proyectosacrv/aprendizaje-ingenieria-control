---
titulo: Linealización numérica (Jacobiano por diferencias finitas)
slug: linealizacion-numerica
categoria: programacion
tipo: metodo
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance, 03-DataCenter-IA]
objetivos: [obtener el modelo lineal A,B,C,D para analisis de estabilidad e impedancia]
tags: [linealizacion, jacobiano, espacio-estados, numerico, scipy]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [equilibrio-fsolve, analisis-modal, impedancia-salida-estabilidad]
referencias:
  - "Khalil, Nonlinear Systems, 3rd ed., cap. 4 (linealizacion)"
---

## Definición
Obtener las matrices de estado \( A,B,C,D \) de un sistema no lineal
\( \dot{\mathbf{x}}=\mathbf{f}(\mathbf{x},\mathbf{u}) \) **derivando numéricamente** el Jacobiano
en un punto de equilibrio, en lugar de hacer el álgebra a mano.

## Fundamento teórico
Alrededor de un equilibrio \( (\mathbf{x}_e,\mathbf{u}_e) \) con \( \mathbf{f}(\mathbf{x}_e,\mathbf{u}_e)=0 \):

$$ \Delta\dot{\mathbf{x}} = A\,\Delta\mathbf{x} + B\,\Delta\mathbf{u}, \quad
   A=\left.\frac{\partial \mathbf{f}}{\partial \mathbf{x}}\right|_e, \;
   B=\left.\frac{\partial \mathbf{f}}{\partial \mathbf{u}}\right|_e $$

Cada columna del Jacobiano se aproxima por **diferencias centradas** (error \( O(h^2) \)):

$$ A_{:,j} \approx \frac{\mathbf{f}(\mathbf{x}_e+h\mathbf{e}_j,\mathbf{u}_e)-\mathbf{f}(\mathbf{x}_e-h\mathbf{e}_j,\mathbf{u}_e)}{2h} $$

<div class="cfig"><img src="figuras/linealizacion-numerica-tangente.png" alt="linealizacion: tangente por diferencias centradas"><div class="cap">La linealización sustituye f(x) por su tangente en x0; numéricamente la pendiente A se aproxima con los dos puntos f(x0±h) (diferencias centradas, error O(h²)).</div></div>

## 1 — Jacobiano numérico: elección óptima de \( \varepsilon \) y el compromiso truncamiento/redondeo
**Paso 1 — diferencia hacia adelante (primer orden).** La derivada se aproxima por:

$$ A_{ij}\approx\frac{f_i(x_e+\varepsilon\,\mathbf{e}_j)-f_i(x_e)}{\varepsilon} $$

El **error de truncamiento** (de la serie de Taylor) es \( O(\varepsilon) \): decrece linealmente con \( \varepsilon \). El **error de redondeo** es \( O(\varepsilon_{mach}/\varepsilon) \) (el numerador tiene error de \( \varepsilon_{mach}\cdot|f| \) y se divide por \( \varepsilon \)): crece al reducir \( \varepsilon \). El mínimo del error total es:

$$ \varepsilon_{opt,\text{forward}}\approx\sqrt{\varepsilon_{mach}}\approx\sqrt{2.22\times10^{-16}}\approx1.49\times10^{-8} $$

**Paso 2 — diferencias centradas (segundo orden).** La fórmula centrada cancela el término de primer orden del error de truncamiento (error \( O(\varepsilon^2) \)):

$$ A_{ij}\approx\frac{f_i(x_e+\varepsilon\,\mathbf{e}_j)-f_i(x_e-\varepsilon\,\mathbf{e}_j)}{2\varepsilon} $$

El error total mínimo ahora es:

$$ \varepsilon_{opt,\text{central}}\approx\varepsilon_{mach}^{1/3}\approx(2.22\times10^{-16})^{1/3}\approx6.1\times10^{-6} $$

y el error mínimo alcanzable es \( \approx\varepsilon_{mach}^{2/3}\approx3.7\times10^{-11} \), mucho menor que con diferencias hacia adelante (\( \approx\varepsilon_{mach}^{1/2}\approx1.5\times10^{-8} \)).

**Paso 3 — \( \varepsilon \) relativo para estados de magnitudes distintas.** Cuando los estados tienen magnitudes muy distintas (corriente ~10 A, tensión ~300 V), un \( \varepsilon \) absoluto fijo produce un paso relativo enorme para la corriente y microscópico para la tensión. La solución es:

$$ h_j = \varepsilon\cdot\max(1,|x_{e,j}|) $$

$$ \boxed{\varepsilon\approx10^{-6}\text{ (centradas)} \;\Rightarrow\; \text{error }\sim10^{-11}\text{ en }f,\; \text{aplicable a estados de cualquier magnitud}} $$

## 2 — Verificación del Jacobiano: prueba de norma residual
**Paso 1 — verificar el equilibrio antes de linearizar.** Si \( \|\mathbf{f}(\mathbf{x}_e,\mathbf{u}_e)\|>\delta \) (p.ej. \( \delta=10^{-8} \)) el punto no es un equilibrio real y \( A \) carece de sentido. Siempre verificar antes de llamar a la rutina de linealización.

**Paso 2 — comprobación por Taylor.** Para un desplazamiento pequeño \( \Delta\mathbf{x} \), la aproximación lineal debería coincidir con la respuesta real:

$$ \|\mathbf{f}(\mathbf{x}_e+\Delta\mathbf{x})-A\,\Delta\mathbf{x}\| = O(\|\Delta\mathbf{x}\|^2) $$

Si la norma del residuo crece cuadráticamente al duplicar \( \|\Delta\mathbf{x}\| \), el Jacobiano es correcto; si crece linealmente, hay un error de cálculo.

## Cuándo y por qué se usa
Cuando el modelo es complejo (muchos estados, no linealidades como rotaciones dq, droop,
impedancia virtual) y derivar \( A,B,C,D \) a mano es laborioso y propenso a errores. Solo se
escriben las ecuaciones físicas \( \mathbf{f} \); el ordenador deriva. **Escala** a cualquier
cambio de control sin rehacer álgebra.

## Procedimiento de diseño (genérico)
1. Implementa \( \mathbf{f}(\mathbf{x},\mathbf{u}) \) y la salida \( \mathbf{y}=\mathbf{g}(\mathbf{x},\mathbf{u}) \).
2. Halla el equilibrio (ver [[equilibrio-fsolve]]).
3. Elige el paso \( h \) **relativo** a cada estado: \( h_j=\varepsilon\max(1,|x_{e,j}|) \),
   con \( \varepsilon\sim10^{-6} \) (compromiso entre error de truncamiento y de redondeo).
4. Construye \( A,C \) perturbando estados y \( B,D \) perturbando entradas, con diferencias
   centradas.
5. Verifica: autovalores plausibles, modos físicos donde la teoría los espera.

## Ejemplo de código
```python
import numpy as np
def linearize(f, g, xe, ue, eps=1e-6):
    n, m = len(xe), len(ue); q = len(g(xe, ue))
    A = np.zeros((n, n)); B = np.zeros((n, m))
    C = np.zeros((q, n)); D = np.zeros((q, m))
    for j in range(n):
        h = eps*max(1.0, abs(xe[j])); e = np.zeros(n); e[j] = h
        A[:, j] = (f(xe+e, ue) - f(xe-e, ue)) / (2*h)
        C[:, j] = (g(xe+e, ue) - g(xe-e, ue)) / (2*h)
    for j in range(m):
        h = eps*max(1.0, abs(ue[j])); e = np.zeros(m); e[j] = h
        B[:, j] = (f(xe, ue+e) - f(xe, ue-e)) / (2*h)
        D[:, j] = (g(xe, ue+e) - g(xe, ue-e)) / (2*h)
    return A, B, C, D
```

## Parámetros y valores típicos
- \( \varepsilon \approx 10^{-6} \) con diferencias centradas (con `float64`). Demasiado
  pequeño → ruido de redondeo; demasiado grande → error de truncamiento.

## Errores comunes
- Linealizar fuera del equilibrio (residuo grande) → \( A \) sin sentido. Verifica
  \( \lVert\mathbf{f}(\mathbf{x}_e)\rVert \approx 0 \) antes.
- Paso \( h \) absoluto en vez de relativo: falla con estados de magnitudes muy distintas
  (corrientes ~10 vs tensiones ~300).

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: obtener A,B,C,D): los 15 estados se linealizan así en
  `model.py`. Con esto se calculan polos (Fase 1) e impedancia \( Y=C(sI-A)^{-1}B+D \) (Fase 2).

## Conceptos relacionados
- [[equilibrio-fsolve]] · [[analisis-modal]] · [[impedancia-salida-estabilidad]]

## Referencias
- Khalil, *Nonlinear Systems*, cap. 4.

---

## 3 — Diferencias finitas para el Jacobiano

**Diferencia hacia adelante** (primer orden, error \( O(h) \)):

$$ \frac{\partial f_i}{\partial x_j} \approx \frac{f_i(\mathbf{x}+h\mathbf{e}_j)-f_i(\mathbf{x})}{h} $$

Requiere solo una evaluación adicional por columna, pero el error de truncamiento decrece lentamente: para minimizarlo hay que tomar \( h \approx \sqrt{\varepsilon_{mach}} \approx 1.5\times10^{-8} \).

**Diferencia central** (segundo orden, error \( O(h^2) \)):

$$ \frac{\partial f_i}{\partial x_j} \approx \frac{f_i(\mathbf{x}+h\mathbf{e}_j)-f_i(\mathbf{x}-h\mathbf{e}_j)}{2h} $$

Cancela el término de primer orden de la serie de Taylor. El paso óptimo es mayor (\( h \approx \varepsilon_{mach}^{1/3} \approx 6\times10^{-6} \)) y el error mínimo es \( O(\varepsilon_{mach}^{2/3}) \approx 3.7\times10^{-11} \), dos órdenes de magnitud mejor que la diferencia hacia adelante.

**Derivada compleja (complex-step):** evalúa la función con argumento complejo \( x+ih \) y toma la parte imaginaria:

$$ \frac{\partial f}{\partial x} \approx \frac{\mathrm{Im}[f(x+ih)]}{h} $$

No hay cancelación de dígitos porque la perturbación es en el eje imaginario: el error es puramente de truncamiento \( O(h^2) \) y funciona con \( h \sim 10^{-200} \) en float64. Requiere que \( f \) sea analítica y acepte números complejos.

**Regla de elección de \( h \):**

| Método | \( h \) óptimo | Error mínimo |
|--------|---------------|--------------|
| Hacia adelante | \( \sqrt{\varepsilon_{mach}} \approx 1.5\times10^{-8} \) | \( O(\varepsilon_{mach}^{1/2}) \) |
| Central | \( \varepsilon_{mach}^{1/3} \approx 6\times10^{-6} \) | \( O(\varepsilon_{mach}^{2/3}) \) |
| Complex-step | cualquier \( h \ll 1 \) | \( O(h^2) \) arbitrariamente pequeño |

<div class="cfig"><img src="figuras/linealizacion-numerica-analisis.png" alt="Errores de diferencias finitas y Jacobiano numérico"><div class="cap">Error de diferencias finitas vs paso h (paneles superiores): la diferencia hacia adelante tiene mínimo a h≈√ε; la diferencia central a h≈ε^(1/3); el complex-step no muestra cancelación de dígitos. Panel inferior izquierdo: error del Jacobiano numérico en un sistema 2D. Panel inferior derecho: respuesta lineal vs no-lineal ante escalón pequeño.</div></div>

## 4 — Matrices de estado \( A, B, C, D \) numéricas

Para el sistema \( \dot{\mathbf{x}}=\mathbf{f}(\mathbf{x},\mathbf{u}) \), \( \mathbf{y}=\mathbf{g}(\mathbf{x},\mathbf{u}) \), en el punto de operación \( (\mathbf{x}_0,\mathbf{u}_0) \):

$$ A_{ij} = \left.\frac{\partial f_i}{\partial x_j}\right|_{x_0,u_0}, \quad B_{ij} = \left.\frac{\partial f_i}{\partial u_j}\right|_{x_0,u_0}, \quad C_{ij} = \left.\frac{\partial g_i}{\partial x_j}\right|_{x_0,u_0}, \quad D_{ij} = \left.\frac{\partial g_i}{\partial u_j}\right|_{x_0,u_0} $$

Se calculan todos con diferencias centrales usando la función `linearize` del apartado *Ejemplo de código*.

**Verificación por eigenvalores.** Los eigenvalores de \( A \) son los polos del sistema linealizado. Si se dispone de un modelo analítico de referencia, deben coincidir con error relativo \( < 1\,\% \) cuando la no-linealidad es suave y \( h \) está bien elegido.

**Tolerancia práctica.** Para convertidores de potencia con saturaciones suaves (droop, limitadores de corriente), el error en los eigenvalores dominantes es típicamente \( < 0.1\,\% \) con diferencias centrales y \( \varepsilon=10^{-6} \).

## 5 — Linealización de convertidores en dq

El vector de estado de un VSC con PLL y lazo de corriente es, por ejemplo:

$$ \mathbf{x} = [i_d,\; i_q,\; v_{dc},\; \theta_{pll},\; \xi_d,\; \xi_q]^\top $$

donde \( \xi_{d,q} \) son los estados del integrador del PI de corriente.

**Perturbación del punto de operación.** Se perturban individualmente \( \Delta V_{dc} \), \( \Delta i_d \), \( \Delta \omega_{pll} \) para construir las columnas correspondientes de \( A \). La perturbación de la entrada \( \Delta v_{ref} \) construye las columnas de \( B \).

**Código Python — función genérica:**

```python
def linearize(f, x0, u0, eps=1e-6):
    """Diferencias centrales. f: callable(x, u) -> array."""
    n, m = len(x0), len(u0)
    A = np.zeros((n, n)); B = np.zeros((n, m))
    for j in range(n):
        h = eps * max(1.0, abs(x0[j])); e = np.zeros(n); e[j] = h
        A[:, j] = (f(x0+e, u0) - f(x0-e, u0)) / (2*h)
    for j in range(m):
        h = eps * max(1.0, abs(u0[j])); e = np.zeros(m); e[j] = h
        B[:, j] = (f(x0, u0+e) - f(x0, u0-e)) / (2*h)
    return A, B
```

**Validación.** Ante un escalón pequeño \( \Delta u = 0.01\,\mathrm{p.u.} \), la respuesta del modelo lineal \( \dot{\Delta x}=A\Delta x+B\Delta u \) debe coincidir con la simulación no-lineal con error \( < 2\,\% \) durante los primeros ciclos (antes de que la no-linealidad acumule divergencia).

## 6 — Errores y precauciones

**Paso \( h \) demasiado pequeño.** Al restar \( f(x+h) - f(x-h) \), si \( h \to 0 \), ambos valores son casi idénticos en punto flotante y la resta pierde dígitos significativos (cancelación catastrófica). El error de redondeo crece como \( \varepsilon_{mach}/(2h) \).

**Paso \( h \) demasiado grande.** El término de truncamiento de la serie de Taylor (del orden \( h^2 f'''/6 \) para diferencias centrales) domina: la derivada numérica refleja la curvatura de \( f \), no solo su pendiente en \( x_0 \).

**Punto de operación en singularidad.** Si \( A \) es singular (determinante nulo) el sistema tiene un modo no observable o no controlable en ese punto; los eigenvalores en cero no indican estabilidad ni inestabilidad — requieren análisis de orden superior (forma normal de Birkhoff).

**Sistemas rígidos (stiff).** Si algunos eigenvalores de \( A \) tienen \( |\mathrm{Re}(\lambda)| \gg 1 \), los estados asociados varían en escalas de tiempo muy distintas. La integración numérica del modelo no-lineal para calcular la perturbación debe usarse entonces con un integrador implícito (p.ej. `solve_ivp` con `method='Radau'`), o directamente evaluar \( f \) en el equilibrio sin simular en el tiempo.
