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
fecha_actualizacion: 2026-06-08
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
