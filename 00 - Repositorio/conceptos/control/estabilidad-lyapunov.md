---
titulo: Estabilidad de Lyapunov
slug: estabilidad-lyapunov
categoria: control
tipo: metodo
nivel: avanzado
proyectos: []
objetivos: [probar estabilidad de sistemas no lineales sin resolver sus ecuaciones]
tags: [lyapunov, estabilidad, no-lineal, energia, funcion-cuadratica, region-atraccion, droop, CPL]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-07-01
relacionados: [analisis-modal, estabilidad-bibo, clasificacion-estabilidad, impedancia-salida-estabilidad, ecuacion-oscilacion]
referencias:
  - "Khalil, Nonlinear Systems, Prentice Hall"
  - "Slotine & Li, Applied Nonlinear Control"
  - "Kundur, Power System Stability and Control, McGraw-Hill 1994"
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

<div class="cfig"><img src="figuras/estabilidad-lyapunov-V.png" alt="trayectoria descendiendo por V y V(t) decreciente"><div class="cap">Izquierda: la trayectoria atraviesa curvas de nivel de \(V\) cada vez menores hasta el equilibrio. Derecha: \(V(x(t))\) decrece de forma monótona (\(\dot V<0\)), lo que prueba estabilidad asintótica sin integrar las ecuaciones del sistema.</div></div>

## 1 — De \( V=\mathbf{x}^\top P\mathbf{x} \) a la ecuación de Lyapunov
**Paso 1 — la candidata cuadrática.** Para el sistema lineal \( \dot{\mathbf{x}}=A\mathbf{x} \) prueba la "energía" \( V(\mathbf{x})=\mathbf{x}^\top P\,\mathbf{x} \) con \( P=P^\top>0 \) (simétrica definida positiva). Es definida positiva por construcción: \( V(0)=0 \) y \( V(\mathbf{x})>0 \) para \( \mathbf{x}\neq0 \). Cumple la primera condición.

**Paso 2 — derivar a lo largo de las trayectorias.** Por la regla del producto sobre \( V=\mathbf{x}^\top P\mathbf{x} \):

$$ \dot V=\dot{\mathbf{x}}^\top P\,\mathbf{x}+\mathbf{x}^\top P\,\dot{\mathbf{x}} $$

**Paso 3 — sustituir la dinámica.** Como \( \dot{\mathbf{x}}=A\mathbf{x} \), entonces \( \dot{\mathbf{x}}^\top=\mathbf{x}^\top A^\top \). Sustituyendo:

$$ \dot V=\mathbf{x}^\top A^\top P\,\mathbf{x}+\mathbf{x}^\top P A\,\mathbf{x}=\mathbf{x}^\top\big(A^\top P+P A\big)\mathbf{x} $$

**Paso 4 — imponer \( \dot V<0 \).** Queremos que esta forma cuadrática sea definida negativa. Define la matriz \( -Q\equiv A^\top P+PA \), es decir, exige que exista \( Q=Q^\top>0 \) tal que:

$$ \boxed{\;A^\top P+P A=-Q\;} $$

Entonces \( \dot V=-\mathbf{x}^\top Q\,\mathbf{x}<0 \) para todo \( \mathbf{x}\neq0 \): el equilibrio es asintóticamente estable.

**Paso 5 — equivalencia con los autovalores.** El teorema de Lyapunov para sistemas lineales dice: dada cualquier \( Q>0 \), existe una solución única \( P>0 \) **si y solo si** todos los autovalores de \( A \) tienen parte real negativa. Así el método de energía y el [[analisis-modal]] coinciden. **Verificado** con \( A=\left[\begin{smallmatrix}0&1\\-2&-3\end{smallmatrix}\right] \) (autovalores \( -1,-2 \)) y \( Q=I \): la solución es \( P=\left[\begin{smallmatrix}1.25&0.25\\0.25&0.25\end{smallmatrix}\right] \), cuyos autovalores \( \{1.31,\,0.19\} \) son positivos, confirmando \( P>0 \) y por tanto estabilidad.

## 2 — Funciones de Lyapunov cuadráticas

La elección \( V(\mathbf{x}) = \mathbf{x}^\top P\,\mathbf{x} \) con \( P = P^\top > 0 \) (simétrica definida positiva) es la más común y la más conveniente en la práctica porque:

1. **Siempre es definida positiva** por construcción.
2. **Su derivada es cuadrática en \( \mathbf{x} \)**: fácil de evaluar el signo.
3. **Existe solución cerrada** para sistemas lineales: la ecuación de Lyapunov tiene solución única.

**Propiedades de \( P \) (necesario y suficiente).**

\( P>0 \) (definida positiva) se verifica de tres maneras equivalentes:
- Todos los autovalores de \( P \) son positivos.
- Todos los menores principales son positivos (criterio de Sylvester).
- La descomposición de Cholesky \( P = L L^\top \) existe.

**La ecuación de Lyapunov discreta.** Para sistemas en tiempo discreto \( \mathbf{x}_{k+1} = A_d\,\mathbf{x}_k \), la condición es \( A_d^\top P A_d - P = -Q \), con solución positiva única cuando todos los autovalores de \( A_d \) tienen módulo menor que 1.

**Solución numérica.**

```python
from scipy.linalg import solve_continuous_lyapunov
import numpy as np
A = np.array([[0., 1.], [-2., -3.]])
Q = np.eye(2)
P = solve_continuous_lyapunov(A.T, -Q)   # A^T P + P A = -Q
estable = np.all(np.linalg.eigvals(P) > 0)
```

**Curvas de nivel como regiones de seguridad.** Las curvas \( V(\mathbf{x}) = c \) son elipsoides en \( \mathbb{R}^n \) (para \( P \) cuadrática). Si \( \dot V < 0 \) en toda la región \( \mathcal{E}_c = \{\mathbf{x}: V(\mathbf{x}) \le c\} \), entonces \( \mathcal{E}_c \) es un **conjunto invariante**: cualquier trayectoria que empiece dentro nunca sale. Es la forma más directa de caracterizar la región de atracción.

## 3 — El teorema directo de Lyapunov

**Teorema (Lyapunov, 1892).** Sea \( \dot{\mathbf{x}} = f(\mathbf{x}) \) con \( f(0) = 0 \). Si existe \( V: \mathbb{R}^n \to \mathbb{R} \) continua y diferenciable tal que:

1. \( V(\mathbf{x}) > 0 \) para \( \mathbf{x} \neq 0 \), y \( V(0) = 0 \) (definida positiva)
2. \( \dot V(\mathbf{x}) = \nabla V \cdot f(\mathbf{x}) \leq 0 \) en un entorno de 0

entonces el equilibrio es **estable (en el sentido de Lyapunov)**.

Si adicionalmente \( \dot V < 0 \) para \( \mathbf{x} \neq 0 \): **asintóticamente estable**.

Si además \( V(\mathbf{x}) \to \infty \) cuando \( \|\mathbf{x}\| \to \infty \) (radialmente no acotada) y \( \dot V < 0 \) en todo \( \mathbb{R}^n \): **globalmente asintóticamente estable**.

**Para el caso lineal.** Con \( V = \mathbf{x}^\top P\mathbf{x} \) y \( \dot{\mathbf{x}} = A\mathbf{x} \):

$$ \dot V = \mathbf{x}^\top (A^\top P + PA)\,\mathbf{x} < 0 \iff A^\top P + PA < 0 $$

Lo cual requiere que exista \( Q > 0 \) con \( A^\top P + PA = -Q \). Por el teorema de Lyapunov lineal, esto ocurre exactamente cuando todos los autovalores de \( A \) tienen parte real negativa. Los métodos se confirman mutuamente.

**La inversa no es cierta.** Si no se encuentra una \( V \) válida, **no** se puede concluir inestabilidad: puede que la candidata propuesta simplemente no sea adecuada. La elección de \( V \) es el arte del método.

**Lema de LaSalle.** Cuando solo se tiene \( \dot V \leq 0 \) (no estrictamente negativa), el teorema de Lyapunov solo garantiza estabilidad, no estabilidad asintótica. El lema de LaSalle extiende la conclusión: si el único punto donde \( \dot V = 0 \) es el equilibrio, entonces el sistema converge al equilibrio aunque \( \dot V \) no sea estrictamente negativa en todas partes.

## 4 — La función de energía del convertidor: Lyapunov natural

La física sugiere candidatas de Lyapunov naturales: la energía almacenada en el sistema.

**Bus DC con condensador \( C \) y CPL de potencia \( P \).** La energía almacenada en el condensador es:

$$ V(v_{DC}) = \frac{1}{2}\,C\,v_{DC}^2 $$

Esta función cumple \( V \geq 0 \), \( V(0)=0 \) (con el equilibrio en el origen del estado \( v_{DC} \)). Su derivada temporal:

$$ \dot V = C\,v_{DC}\,\dot v_{DC} = v_{DC}\,(i_{src} - i_{CPL}) = v_{DC}\,i_{src} - P $$

donde se ha usado \( C\,\dot v_{DC} = i_{src} - P/v_{DC} \) y por tanto \( \dot V = v_{DC} i_{src} - P \).

**Condición de estabilidad vía Lyapunov.** Para que \( \dot V < 0 \) (el bus se estabiliza):

$$ v_{DC}\,i_{src} > P $$

Con una fuente con característica \( i_{src}(v_{DC}) = (V_{OC} - v_{DC})/R_{src} \) (fuente de Thevenin):

$$ v_{DC}\,\frac{V_{OC} - v_{DC}}{R_{src}} > P \quad\Longrightarrow\quad -\frac{v_{DC}^2}{R_{src}} + \frac{V_{OC}}{R_{src}}\,v_{DC} - P > 0 $$

Esta parábola en \( v_{DC} \) tiene discriminante positivo cuando \( P < V_{OC}^2/(4\,R_{src}) = P_{crit} \): exactamente la condición de colapso del bus. Para \( P > P_{crit} \) la parábola es siempre negativa: \( \dot V > 0 \), la energía crece → el bus colapsa.

**Con droop DC.** Si la fuente aumenta su corriente cuando \( v_{DC} \) baja (\( i_{src} = (V_{OC} + k_{droop}(V_0 - v_{DC}))/R_{src} \)), la condición \( v_{DC} i_{src} > P \) se cumple para un rango más amplio de \( P \). El droop DC extiende la región de operación estable actuando como realimentación que refuerza la estabilidad de Lyapunov.

## 5 — La región de atracción: cuánto puede desviarse el sistema

La **región de atracción** (o cuenca de atracción) \( \mathcal{R}(\mathbf{x}^*) \) de un equilibrio estable \( \mathbf{x}^* \) es el conjunto de condiciones iniciales \( \mathbf{x}_0 \) tales que la trayectoria converge a \( \mathbf{x}^* \):

$$ \mathcal{R}(\mathbf{x}^*) = \{\mathbf{x}_0: \lim_{t\to\infty} \mathbf{x}(t) = \mathbf{x}^*\} $$

**Para un sistema lineal estable:** \( \mathcal{R} = \mathbb{R}^n \) completo (atractor global). Cualquier condición inicial converge.

**Para el droop GFM (oscilación de potencia).** El sistema de potencia equivalente tiene la dinámica del ángulo de carga \( \delta \):

$$ M\,\ddot\delta + D\,\dot\delta = P_{ref} - \frac{EV}{X}\sin\delta $$

El equilibrio estable es \( \delta_0 = \arcsin(P_{ref} X/(EV)) \) y el inestable es \( \pi - \delta_0 \). La región de atracción se define en términos de la **función de energía transitoria** \( W(\delta) \):

$$ W(\delta) = -\frac{EV}{X}\cos\delta $$

El equilibrio estable es un mínimo local de \( W \); el inestable es un máximo. La región de atracción está delimitada por el nivel de energía del equilibrio inestable: cualquier trayectoria con \( W(\delta_0) \leq W(\pi - \delta_0) \) permanece en la cuenca.

La condición \( \delta < 90° \) es la condición de estabilidad transitoria del ángulo: si \( \delta \) supera los \( 90° \) y la energía cinética es suficiente para alcanzar \( \pi - \delta_0 \), el sistema pierde el sincronismo.

**Para el bus DC con CPL.** La región de atracción es el conjunto de tensiones \( v_{DC} \) para el que existe un equilibrio estable. Para \( P < P_{crit} \) hay dos equilibrios: el operativo (estable, \( v_{DC}^+ \)) y el de colapso (inestable, \( v_{DC}^- \)). La región de atracción del equilibrio operativo es \( v_{DC} > v_{DC}^- = V_{OC}/2 \): la tensión no puede caer por debajo de la mitad de la tensión en vacío sin colapsar.

## 6 — Lyapunov para diseñar impedancia virtual

El método de Lyapunov no solo analiza: permite **diseñar** lazos de control que garantizan estabilidad de gran señal.

**Motivación.** En el droop GFM, la reactancia entre el convertidor y la red es \( X_{grid} \). Si \( X_{grid} \) es pequeña (red rígida), el ángulo de carga \( \delta_0 \) para una potencia dada es grande:

$$ \delta_0 = \arcsin\!\left(\frac{P\,X_{grid}}{EV}\right) $$

Para \( P = S_n \) (potencia nominal) y \( X_{grid} = 0.1\,\text{pu} \): \( \delta_0 = \arcsin(0.1) \approx 5.7° \). El margen de estabilidad transitoria es \( 90° - 5.7° = 84.3° \): muy amplio. Pero con \( X_{grid} = 0.5\,\text{pu} \): \( \delta_0 = \arcsin(0.5) = 30° \). Margen de \( 60° \): todavía cómodo.

**Problema: red sin transformador o Xgrid ≪ 1.** En una microrred con conexión directa y SCR alto (red muy rígida), \( X_{grid} \approx 0 \) y el ángulo \( \delta_0 \approx 0° \): la potencia se transfiere casi sin ángulo. Cualquier transitorio grande (falta, reconexión) puede sacar al sistema de la región de atracción.

**Solución: reactancia virtual \( X_{virt} \).** Se añade al control un término de realimentación que emula una reactancia adicional:

$$ v^* = E\angle0 - jX_{virt}\,i $$

Esto hace que la función de transferencia de potencia vea una reactancia efectiva \( X_{eff} = X_{grid} + X_{virt} \). El ángulo de carga equivalente:

$$ P = \frac{EV}{X_{eff}}\sin\delta \quad\Longrightarrow\quad \delta_0 = \arcsin\!\left(\frac{P\,X_{eff}}{EV}\right) $$

Con \( X_{virt} \) creciente, \( \delta_0 \) crece. La región de atracción se mide por el margen hasta el equilibrio inestable:

$$ \Delta\delta = (\pi - \delta_0) - \delta_0 = \pi - 2\delta_0 $$

**Diseño mínimo de \( X_{virt} \).** Se requiere que en operación nominal (\( P = S_n \)) el ángulo no supere \( 60° \):

$$ \delta_0 < 60° \quad\Longrightarrow\quad \sin(60°) = \frac{S_n\,X_{eff}}{EV} \quad\Longrightarrow\quad X_{eff} > \frac{EV\sin(60°)}{S_n} $$

$$ X_{virt,min} = \frac{EV\sqrt{3}/2}{S_n} - X_{grid} $$

En valores por unidad con \( E \approx V \approx 1\,\text{pu} \), \( S_n = 1\,\text{pu} \): \( X_{virt,min} = \sqrt{3}/2 - X_{grid} \approx 0.87 - X_{grid} \).

**Análisis de Lyapunov del diseño.** Con la reactancia virtual, el potencial efectivo es:

$$ W(\delta) = -\frac{EV}{X_{eff}}\cos\delta $$

La profundidad del pozo de potencial (diferencia entre el máximo y el mínimo) es \( EV/X_{eff} \cdot (\cos\delta_0 - \cos(\pi-\delta_0)) = 2\,EV/X_{eff} \cdot \cos\delta_0 \). Con \( \delta_0 = 60° \): profundidad = \( 2 \cdot EV/(X_{eff}) \cdot 0.5 = EV/X_{eff} \). Aumentar \( X_{eff} \) reduce la profundidad pero aumenta el margen angular. El diseño balancea margen angular vs. pendiente de potencia (rigidez sincrónica \( K_s = EV\cos\delta_0/X_{eff} \)).

<div class="cfig"><img src="figuras/estabilidad-lyapunov-analisis.png" alt="lyapunov: curvas de nivel, energia bus DC, pendulo droop, Xvirt"><div class="cap">(a) Curvas de nivel de \(V=\mathbf{x}^T P\mathbf{x}\) para sistema 2D estable: las trayectorias cruzan cada curva de nivel hacia adentro (\(\dot V<0\)). (b) Derivada de energía del bus DC: \(\dot V<0\) solo para \(P<P_{crit}\); con mayor CPL el bus colapsa. (c) Péndulo equivalente del droop: pozo de potencial con equilibrio estable (mínimo), inestable (máximo) y región de atracción sombreada. (d) Añadir \(X_{virt}\) aumenta \(\delta_0\) y amplía la región de atracción (margen antes de perder sincronía).</div></div>

## Cuándo y por qué se usa
Cuando el sistema es **no lineal** y los autovalores no bastan: ecuación de oscilación del VSM,
estabilidad de gran señal, buses DC con carga de potencia constante, limitación de corriente. También
en diseño de control **basado en energía/pasividad**, donde se construye el control para que cierta
\( V \) decrezca.

## Procedimiento de diseño (genérico)
1. Propón una \( V(\mathbf{x}) \) candidata (a menudo la energía física del sistema).
2. Verifica que es definida positiva.
3. Calcula \( \dot V \) sobre las trayectorias y comprueba que es \( \leq 0 \) (o \( <0 \)).
4. Si \( \dot V<0 \): asintóticamente estable. Si solo \( \leq 0 \): usa LaSalle para concluir.
5. Caracteriza la región de atracción mediante las curvas de nivel de \( V \).

## Ejemplo de código
```python
from scipy.linalg import solve_continuous_lyapunov
import numpy as np
P = solve_continuous_lyapunov(A.T, -np.eye(A.shape[0]))   # A^T P + P A = -I
estable = np.all(np.linalg.eigvals(P) > 0)     # P>0  <=>  A estable
```

## Parámetros y valores típicos
No hay "parámetros": la dificultad está en **proponer** una buena \( V \). Para máquinas/VSM la
energía cinética \( \tfrac12 J\,\Delta\omega^2 \) más un término de potencial en \( \delta \) suele
funcionar (función de energía transitoria). Para buses DC: la energía del condensador \( \tfrac12 C\,v^2 \).

## Errores comunes
- No encontrar una \( V \) válida **no** demuestra inestabilidad (solo que esa candidata no sirve).
- La estabilidad puede ser **local**: la \( V \) define una región de atracción, no necesariamente todo el espacio.
- Confundir \( V>0 \) (sobre el estado) con \( \dot V<0 \) (la condición que realmente importa).
- Usar la energía física como candidata sin verificar que \( \dot V < 0 \) en la región de operación.

## Conceptos relacionados
- [[analisis-modal]] · [[estabilidad-bibo]] · [[clasificacion-estabilidad]] · [[impedancia-salida-estabilidad|resistencia negativa]] · [[ecuacion-oscilacion]]

## Referencias
- Khalil, *Nonlinear Systems*.
- Slotine & Li, *Applied Nonlinear Control*.
- Kundur, *Power System Stability and Control*, McGraw-Hill 1994.
