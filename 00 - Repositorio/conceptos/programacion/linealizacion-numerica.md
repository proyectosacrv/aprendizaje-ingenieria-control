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
fecha_actualizacion: 2026-06-11
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
