---
titulo: Estabilidad de Lyapunov
slug: estabilidad-lyapunov
categoria: control
tipo: metodo
nivel: avanzado
proyectos: []
objetivos: [probar estabilidad de sistemas no lineales sin resolver sus ecuaciones]
tags: [lyapunov, estabilidad, no-lineal, energia, basico]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-06-10
relacionados: [analisis-modal, estabilidad-bibo, clasificacion-estabilidad, no-pasividad-resistencia-negativa, ecuacion-oscilacion]
referencias:
  - "Khalil, Nonlinear Systems, Prentice Hall"
  - "Slotine & Li, Applied Nonlinear Control"
---

## Definición
Método para demostrar la estabilidad de un punto de equilibrio **sin resolver** las ecuaciones del
sistema, usando una función escalar tipo "energía" \( V(\mathbf{x}) \) que, si decrece con el
tiempo, garantiza que el sistema tiende al equilibrio. Es la herramienta natural para sistemas **no
lineales**, donde los autovalores solo valen tras linealizar.

## Fundamento teórico
Para un sistema \( \dot{\mathbf{x}} = f(\mathbf{x}) \) con equilibrio en el origen, se busca una
función \( V(\mathbf{x}) \) **definida positiva** (\( V(0)=0 \), \( V(\mathbf{x})>0 \) alrededor).
El equilibrio es estable si su derivada a lo largo de las trayectorias es no creciente, y
**asintóticamente estable** si decrece estrictamente:
$$ \dot{V}(\mathbf{x}) = \nabla V \cdot f(\mathbf{x}) < 0 $$
Para un sistema **lineal** \( \dot{\mathbf{x}}=A\mathbf{x} \), una \( V = \mathbf{x}^\top P\,\mathbf{x} \)
funciona si existe \( P>0 \) que resuelve la **ecuación de Lyapunov**:
$$ A^\top P + P A = -Q, \qquad Q>0 $$
La existencia de tal \( P \) equivale a que todos los autovalores de \( A \) tengan parte real
negativa: conecta el método con el análisis modal.

<div class="cfig"><img src="figuras/estabilidad-lyapunov-V.png" alt="trayectoria descendiendo por V y V(t) decreciente"><div class="cap">Izquierda: la trayectoria atraviesa curvas de nivel de $V$ cada vez menores hasta el equilibrio. Derecha: $V(x(t))$ decrece de forma monótona ($\dot V<0$), lo que prueba estabilidad asintótica sin integrar las ecuaciones del sistema.</div></div>

## Cuándo y por qué se usa
Cuando el sistema es **no lineal** y los autovalores no bastan: ecuación de oscilación del VSM,
estabilidad de gran señal, buses DC con carga de potencia constante, limitación de corriente. También
en diseño de control **basado en energía/pasividad**, donde se construye el control para que cierta
\( V \) decrezca.

## Procedimiento de diseño (genérico)
1. Propón una \( V(\mathbf{x}) \) candidata (a menudo la energía física del sistema).
2. Verifica que es definida positiva.
3. Calcula \( \dot V \) sobre las trayectorias y comprueba que es \( \le 0 \) (o \( <0 \)).
4. Si \( \dot V<0 \): asintóticamente estable. Si solo \( \le 0 \): usa LaSalle para concluir.

## Ejemplo de código
```python
from scipy.linalg import solve_lyapunov
import numpy as np
P = solve_lyapunov(A.T, -np.eye(A.shape[0]))   # A^T P + P A = -I
estable = np.all(np.linalg.eigvals(P) > 0)     # P>0  <=>  A estable
```

## Parámetros y valores típicos
No hay "parámetros": la dificultad está en **proponer** una buena \( V \). Para máquinas/VSM la
energía cinética \( \tfrac12 J\,\Delta\omega^2 \) más un término de potencial en \( \delta \) suele
funcionar (función de energía transitoria).

## Errores comunes
- No encontrar una \( V \) válida **no** demuestra inestabilidad (solo que esa candidata no sirve).
- La estabilidad puede ser **local**: la \( V \) define una región de atracción, no necesariamente todo el espacio.
- Confundir \( V>0 \) (sobre el estado) con \( \dot V<0 \) (la condición que realmente importa).

## Conceptos relacionados
- [[analisis-modal]] · [[estabilidad-bibo]] · [[clasificacion-estabilidad]] · [[no-pasividad-resistencia-negativa]] · [[ecuacion-oscilacion]]

## Referencias
- Khalil, *Nonlinear Systems*.
- Slotine & Li, *Applied Nonlinear Control*.
