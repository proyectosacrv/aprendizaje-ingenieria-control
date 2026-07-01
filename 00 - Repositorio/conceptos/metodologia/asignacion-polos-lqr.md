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
fecha_actualizacion: 2026-06-30
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

<div class="cfig"><img src="figuras/asignacion-polos-lqr-polos.png" alt="polos de lazo cerrado del LQR al variar Q/R"><div class="cap">Polos de lazo cerrado del LQR al barrer la relación $Q/R$: subir $Q/R$ (más peso al desempeño frente al esfuerzo de control) desplaza los autovalores de $A-BK$ hacia la izquierda, acelerando la respuesta a costa de más actuación. Las ponderaciones $Q,R$ son la palanca de diseño (regla de Bryson).</div></div>

## 1 — De dónde sale \( K=R^{-1}B^TP \): la ecuación de Riccati
**Paso 1 — el problema.** Minimizar \( J=\int_0^\infty (x^TQx+u^TRu)\,dt \) sujeto a \( \dot x=Ax+Bu \), con \( Q\succeq0 \) (penaliza el estado) y \( R\succ0 \) (penaliza el control). Se busca la ley \( u=u(x) \) que lo hace mínimo.

**Paso 2 — función de valor cuadrática.** Para un sistema lineal con coste cuadrático, el coste óptimo desde un estado \( x \) es cuadrático: \( V(x)=x^TPx \) con \( P=P^T\succ0 \). \( V \) es el "coste que aún queda por pagar" partiendo de \( x \) y aplicando el control óptimo.

**Paso 3 — ecuación de Hamilton-Jacobi-Bellman.** El principio de optimalidad exige que en cada instante el control elija la dirección que minimiza el coste instantáneo más el ritmo de cambio del coste por venir:
$$ 0=\min_u\left[\,x^TQx+u^TRu+\nabla V^{T}(Ax+Bu)\,\right],\qquad \nabla V=2Px $$

**Paso 4 — minimizar en \( u \).** Derivando el corchete respecto a \( u \) e igualando a cero (es cuadrático convexo en \( u \) porque \( R\succ0 \)):
$$ \frac{\partial}{\partial u}\big[u^TRu+2x^TP\,Bu\big]=2Ru+2B^TPx=0\;\Rightarrow\; \boxed{\,u=-R^{-1}B^TP\,x=-Kx,\quad K=R^{-1}B^TP\,} $$
La ley óptima es **realimentación lineal de estado**; sólo falta \( P \).

**Paso 5 — sustituir y obtener Riccati.** Metiendo \( u=-R^{-1}B^TPx \) en el corchete del Paso 3 y agrupando (todo queda como \( x^T[\cdots]x=0 \) para todo \( x \), luego el corchete se anula):
$$ \boxed{\,A^TP+PA-PBR^{-1}B^TP+Q=0\,} $$
la **ecuación algebraica de Riccati** (ARE). Se resuelve para \( P \succ0 \) y de ahí \( K \). El término \( -PBR^{-1}B^TP \) es justo lo que la realimentación resta a la dinámica abierta \( A^TP+PA \).

## 2 — El caso escalar resuelto a mano
**Paso 1 — planta y coste de primer orden.** Sea \( \dot x=ax+bu \) (escalar) con \( J=\int(qx^2+ru^2)\,dt \). Ahora \( A,B,P,Q,R \) son números \( a,b,P,q,r \).

**Paso 2 — Riccati escalar.** Sustituyendo en la ARE:
$$ 2aP-\frac{b^2}{r}P^2+q=0\;\Longleftrightarrow\;\frac{b^2}{r}P^2-2aP-q=0 $$
ecuación de segundo grado en \( P \). La raíz positiva (la física, \( P>0 \)) es
$$ P=\frac{a+\sqrt{a^2+qb^2/r}}{b^2/r},\qquad K=\frac{b}{r}P=\frac{a+\sqrt{a^2+qb^2/r}}{b} $$

**Paso 3 — número concreto.** Con \( a=b=q=r=1 \): \( P^2-2P-1=0\Rightarrow P=1+\sqrt2\approx2.414 \), luego \( K=2.414 \). El polo de lazo cerrado es
$$ a-bK=1-2.414=-\sqrt2\approx-1.414 $$
estable y a la izquierda del origen. **Lectura:** una planta inestable en lazo abierto (\( a=+1 \), polo en \( +1 \)) queda estabilizada con un polo en \( -\sqrt2 \); la simetría \( |a-bK|=\sqrt2 \) frente a \( |a|=1 \) es la firma del LQR escalar (raíz del polinomio simétrico de Hamilton). Subir \( q/r \) (más peso al estado) aleja aún más el polo hacia la izquierda — la palanca de la regla de Bryson.

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
