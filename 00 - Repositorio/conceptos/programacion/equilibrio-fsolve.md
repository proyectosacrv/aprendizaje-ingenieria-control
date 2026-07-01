---
titulo: Cálculo del punto de equilibrio (fsolve)
slug: equilibrio-fsolve
categoria: programacion
tipo: metodo
nivel: basico
proyectos: [01-GFM-Impedance, 02-GFL-Impedance, 03-DataCenter-IA]
objetivos: [hallar el punto de operacion antes de linealizar]
tags: [equilibrio, fsolve, scipy, punto-operacion, raices]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-30
relacionados: [linealizacion-numerica, analisis-modal]
referencias:
  - "SciPy docs: scipy.optimize.fsolve"
---

## Definición
Resolver \( \mathbf{f}(\mathbf{x}_e,\mathbf{u}_e)=0 \) numéricamente para hallar el **punto de
equilibrio** (régimen permanente) de un sistema no lineal, paso previo imprescindible a la
linealización.

## Fundamento teórico
`fsolve` (método híbrido de Powell) busca la raíz del campo vectorial partiendo de una
estimación inicial \( \mathbf{x}_0 \). La calidad del resultado se mide por el **residuo**
\( \lVert\mathbf{f}(\mathbf{x}_e)\rVert \), que debe ser ~0 (p.ej. <1e-9).

<div class="cfig"><img src="figuras/equilibrio-fsolve-convergencia.png" alt="convergencia del residuo de fsolve con buen y mal guess inicial"><div class="cap">Convergencia de fsolve: partiendo de una estimación inicial física (corrientes desde la potencia, tensión nominal) el residuo $\|f(x)\|$ cae hasta ~$10^{-11}$ en pocas iteraciones; con un guess pobre el método se estanca en una raíz espuria sin sentido físico. Por eso el paso crítico es construir un buen $x_0$ y verificar siempre el residuo.</div></div>

## 1 — De dónde sale la iteración de Newton-Raphson
**Paso 1 — el problema.** Buscamos \( \mathbf{x}_e \) tal que \( \mathbf{f}(\mathbf{x}_e)=0 \), con \( \mathbf{f}:\mathbb{R}^n\to\mathbb{R}^n \) no lineal. No hay fórmula cerrada; iteramos desde un \( \mathbf{x}_0 \).

**Paso 2 — linealizar alrededor del iterado actual.** Cerca de \( \mathbf{x}_k \), el desarrollo de Taylor de primer orden del campo vectorial es:

$$ \mathbf{f}(\mathbf{x}_k+\Delta\mathbf{x})\approx \mathbf{f}(\mathbf{x}_k)+J(\mathbf{x}_k)\,\Delta\mathbf{x},\qquad J_{ij}=\frac{\partial f_i}{\partial x_j} $$

donde \( J \) es la matriz **Jacobiana** evaluada en \( \mathbf{x}_k \).

**Paso 3 — imponer que el modelo lineal valga cero.** Pedimos que el incremento \( \Delta\mathbf{x} \) lleve la aproximación a la raíz, \( \mathbf{f}(\mathbf{x}_k)+J(\mathbf{x}_k)\Delta\mathbf{x}=0 \). Resolviendo el sistema lineal:

$$ \Delta\mathbf{x}=-J(\mathbf{x}_k)^{-1}\mathbf{f}(\mathbf{x}_k) $$

**Paso 4 — actualizar.** El nuevo iterado es \( \mathbf{x}_{k+1}=\mathbf{x}_k+\Delta\mathbf{x} \), es decir:

$$ \boxed{\;\mathbf{x}_{k+1}=\mathbf{x}_k-J(\mathbf{x}_k)^{-1}\,\mathbf{f}(\mathbf{x}_k)\;} $$

(En la práctica no se invierte \( J \): se resuelve \( J\,\Delta\mathbf{x}=-\mathbf{f} \) por factorización LU. `fsolve` usa una variante híbrida de Powell que combina Newton con descenso de gradiente cuando \( J \) está mal condicionada, y aproxima \( J \) por diferencias finitas si no se da.)

## 2 — Por qué la convergencia es cuadrática
**Paso 1 — definir el error.** Sea \( \mathbf{x}_e \) la raíz y \( e_k=\mathbf{x}_k-\mathbf{x}_e \) el error del iterado \( k \). Queremos relacionar \( e_{k+1} \) con \( e_k \).

**Paso 2 — Taylor de segundo orden de la raíz.** Como \( \mathbf{f}(\mathbf{x}_e)=0 \), desarrollando \( \mathbf{f} \) en \( \mathbf{x}_k \) y evaluando en la raíz (caso escalar para ver el mecanismo):

$$ 0=f(\mathbf{x}_e)=f(\mathbf{x}_k)+f'(\mathbf{x}_k)(\mathbf{x}_e-\mathbf{x}_k)+\tfrac12 f''(\xi)(\mathbf{x}_e-\mathbf{x}_k)^2 $$

con \( \xi \) entre \( \mathbf{x}_k \) y \( \mathbf{x}_e \).

**Paso 3 — sustituir la actualización de Newton.** Dividiendo entre \( f'(\mathbf{x}_k) \) y usando \( \mathbf{x}_{k+1}=\mathbf{x}_k-f(\mathbf{x}_k)/f'(\mathbf{x}_k) \), el término \( f(\mathbf{x}_k)/f'(\mathbf{x}_k) \) se reescribe como \( \mathbf{x}_k-\mathbf{x}_{k+1} \). Reagrupando, los términos lineales en el error se cancelan y queda:

$$ e_{k+1}=\mathbf{x}_{k+1}-\mathbf{x}_e=\frac{f''(\xi)}{2f'(\mathbf{x}_k)}\,e_k^2 $$

**Paso 4 — la cota cuadrática.** Tomando módulos, con \( C=\big|f''/2f'\big| \) acotado cerca de la raíz:

$$ \boxed{\;|e_{k+1}|\le C\,|e_k|^2\;} $$

El error **se eleva al cuadrado** en cada paso: si \( |e_k|\sim10^{-3} \), entonces \( |e_{k+1}|\sim10^{-6} \), luego \( \sim10^{-12} \). El número de dígitos correctos **se duplica** por iteración. Por eso el residuo cae a \( \sim10^{-11} \) en pocas iteraciones (en el ejemplo, <20). La condición es que \( f'(\mathbf{x}_e)\neq0 \) (Jacobiana no singular en la raíz) y que \( \mathbf{x}_0 \) esté en la **cuenca de atracción**: de ahí la importancia del guess físico, pues un \( \mathbf{x}_0 \) lejano puede caer en otra cuenca y converger a una raíz espuria.

## Cuándo y por qué se usa
Siempre que se quiera linealizar o analizar alrededor de un punto de operación concreto
(potencia, tensión dadas). Un buen equilibrio garantiza que \( A,B,C,D \) tienen sentido físico.

## Procedimiento de diseño (genérico)
1. Implementa \( \mathbf{f}(\mathbf{x},\mathbf{u}) \).
2. Construye una **estimación inicial física**: corrientes desde la potencia
   (\( i_d\approx P/(1.5V) \)), tensión ≈ nominal, ángulos pequeños. Un buen \( x_0 \) evita
   raíces espurias.
3. Llama a `fsolve` con `full_output=True` y `xtol` ajustado.
4. **Verifica el residuo** y que las magnitudes son físicas (P, Q, |v| coherentes).

## Ejemplo de aplicación real
**Problema:** Convertidor GFM de 5 kW operando a \( P^*=5\,\text{kW} \), \( Q^*=0 \), tensión de red \( V_g=325\,\text{V} \). Verificar que `fsolve` converge a un equilibrio físico con residuo <1e-6.

Se inicializa \( x_0 \) con estimaciones físicas: \( i_d\approx P/(1.5V_g)\approx10.3\,\text{A} \), \( i_q=0 \), \( v_d=V_g \), ángulo \( \delta\approx0 \). `fsolve` converge en <20 iteraciones con residuo \( \approx5\times10^{-11} \). Las magnitudes del equilibrio se verifican: \( P_{eq}\approx5000\,\text{W} \), \( Q_{eq}\approx0 \), \( |v_{dq}|=325\,\text{V} \). Si el guess inicial es pobre (todo ceros), puede converger a un equilibrio espurio (\( P=0 \)): por eso el paso crítico es construir estimaciones físicas. Desde este \( x_e \) se linealiza para obtener la matriz \( A \) y analizar los modos.

## Ejemplo de código
```python
from scipy.optimize import fsolve
import numpy as np
x0 = np.zeros(n)
x0[idx_id] = Pset/(1.5*Vg); x0[idx_vd] = Vg      # guess fisico
xe, info, ier, msg = fsolve(lambda x: f(x, u), x0, full_output=True, xtol=1e-12)
res = np.linalg.norm(f(xe, u))
assert res < 1e-6, f"equilibrio no converge: {res}"
```

## Parámetros y valores típicos
`xtol` 1e-10–1e-12; residuo aceptable <1e-6 (en el proyecto ~1e-10).

## Errores comunes
- Guess inicial pobre → converge a una raíz sin sentido o no converge.
- No comprobar el residuo y asumir que convergió.

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: punto de operación): equilibrio para P=5 kW, Q=0 con
  residuo ~1e-10; de ahí salen P_eq, Q_eq, δ. En `model.py` (`equilibrium`).

## Conceptos relacionados
- [[linealizacion-numerica]] · [[analisis-modal]]

## Referencias
- SciPy `optimize.fsolve`.
