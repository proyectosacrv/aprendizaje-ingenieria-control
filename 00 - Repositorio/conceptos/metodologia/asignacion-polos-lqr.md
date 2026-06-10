---
titulo: Control en espacio de estados (asignación de polos, LQR/LQG)
slug: asignacion-polos-lqr
categoria: metodologia
tipo: metodo
nivel: avanzado
proyectos: []
objetivos: [disenar control MIMO con realimentacion de estado]
tags: [espacio-estados, asignacion-polos, LQR, LQG, observador, MIMO]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [metodos-sintesis-control, linealizacion-numerica, analisis-modal, control-robusto-hinf]
referencias:
  - "Anderson, Moore, Optimal Control: Linear Quadratic Methods, 1990"
  - "Franklin, Powell, Feedback Control of Dynamic Systems"
---

## Definición
Familia de métodos que diseñan el control realimentando el **vector de estado**
\( u=-Kx \), eligiendo \( K \) por **asignación de polos** (colocar los autovalores donde se
quiera) o por **LQR** (minimizar un coste cuadrático). Naturales para sistemas MIMO y de muchos
estados como un convertidor.

## Fundamento teórico
- **Asignación de polos**: si el par \( (A,B) \) es controlable, existe \( K \) tal que los
  autovalores de \( A-BK \) son los deseados. Da control directo de la dinámica, pero elegir
  "buenos" polos en MIMO no es trivial.
- **LQR**: minimiza \( J=\int (x^TQx + u^TRu)\,dt \); la solución \( K=R^{-1}B^TP \) viene de la
  ecuación de Riccati. \( Q,R \) ponderan desempeño vs esfuerzo de control. Garantiza márgenes
  de robustez (≥60° de fase) en el caso de estado completo.
- **LQG**: LQR + **observador** (filtro de Kalman) cuando no se miden todos los estados.
- Requiere un modelo de estado fiable (ver [[linealizacion-numerica]]).

## Cuándo y por qué se usa
Cuando el sistema es MIMO y acoplado (varios estados que interactúan), o cuando se quiere un
diseño sistemático que pondere desempeño y esfuerzo. En convertidores: control de estado del
filtro LCL, MMC (muchos estados), accionamientos.

## Procedimiento (genérico)
1. Obtén \( (A,B,C,D) \) por linealización.
2. Comprueba controlabilidad/observabilidad.
3. LQR: elige \( Q,R \) (p.ej. Bryson: normaliza por máximos admisibles), resuelve Riccati → \( K \).
4. Si faltan medidas, diseña observador (Kalman) → LQG.
5. Evalúa márgenes y robustez (LQG pierde las garantías del LQR: comprobar).

## Ejemplo de código
```python
from scipy.linalg import solve_continuous_are
import numpy as np
P = solve_continuous_are(A, B, Q, R)
K = np.linalg.solve(R, B.T @ P)        # u = -K x
eig_cl = np.linalg.eigvals(A - B @ K)  # polos en lazo cerrado
```

## Parámetros y valores típicos
\( Q,R \) por regla de Bryson (inversos de los máximos al cuadrado). Ajustar la relación \( Q/R \)
para más desempeño (Q alto) o menos esfuerzo (R alto).

## Errores comunes
- Asignar polos demasiado rápidos → esfuerzo de control y ruido excesivos.
- Asumir que LQG hereda la robustez del LQR (no la garantiza: verificar márgenes).

## Uso en proyectos
- Pendiente de aplicar en un proyecto (candidato: control de estado del LCL o MMC). Ficha de
  panorama por ahora.

## Conceptos relacionados
- [[metodos-sintesis-control]] · [[linealizacion-numerica]] · [[analisis-modal]] · [[control-robusto-hinf]]

## Referencias
- Anderson, Moore, *Optimal Control*, 1990.
