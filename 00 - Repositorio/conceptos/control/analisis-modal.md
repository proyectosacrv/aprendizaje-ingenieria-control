---
titulo: Análisis modal (autovalores, participación, amortiguamiento)
slug: analisis-modal
categoria: control
tipo: metodo
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance, 03-DataCenter-IA]
objetivos: [evaluar estabilidad e identificar el origen de cada modo]
tags: [autovalores, polos, participacion, zeta, estabilidad, sensibilidad, forma-modal, reduccion-orden]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [linealizacion-numerica, droop-control, impedancia-salida-estabilidad, filtro-lcl, control-cascada]
referencias:
  - "Kundur, Power System Stability and Control, McGraw-Hill 1994 (cap. 12)"
  - "Pal & Chaudhuri, Robust Control in Power Systems, Springer 2005 (cap. 2)"
  - "Verghese, Pérez-Arriaga, Schweppe, Selective Modal Analysis with Applications to Electric Power Systems, IEEE TPAS 1982"
---

## Definición
Estudio de la estabilidad de un sistema lineal a partir de los **autovalores** de \( A \)
(modos), su **amortiguamiento** \( \zeta \) y **frecuencia natural**, y los **factores de
participación** que revelan qué estados forman cada modo. Responde no solo a "¿es estable?"
sino a "¿qué modo falla y qué estado hay que tocar para corregirlo?".

## Fundamento teórico
Para un autovalor \( \lambda=\sigma\pm j\omega_d \):
$$ f=\frac{|\omega_d|}{2\pi}, \qquad \zeta=\frac{-\sigma}{|\lambda|} $$
Estable si \( \sigma<0 \) para todos los modos. El **factor de participación** del estado
\( k \) en el modo \( i \) es \( p_{ki}=|\psi_{ik}\,\phi_{ki}| \), donde \( \phi \) y
\( \psi \) son los autovectores derecho e izquierdo. Identifica qué dinámica domina cada
modo y guía el rediseño.

<div class="cfig"><img src="figuras/analisis-modal-polos.png" alt="mapa de autovalores en el plano s"><div class="cap">Mapa de autovalores: cuanto más a la izquierda (σ más negativo), más amortiguado; la parte imaginaria da la frecuencia. El modo que preocupa es el cercano al eje imaginario con poco ζ.</div></div>

## 1 — Por qué los autovalores de \( A \) son los modos
**Paso 1 — diagonalizar la dinámica.** El sistema libre es \( \dot{\mathbf{x}}=A\mathbf{x} \). Sea \( A\phi_i=\lambda_i\phi_i \): \( \lambda_i \) autovalor, \( \phi_i \) autovector derecho. Si \( A \) es diagonalizable, agrupa los autovectores en \( \Phi=[\phi_1\,\cdots\,\phi_n] \), de modo que \( A\Phi=\Phi\Lambda \) con \( \Lambda=\mathrm{diag}(\lambda_i) \), es decir \( \Phi^{-1}A\Phi=\Lambda \).

**Paso 2 — cambio a coordenadas modales.** Define \( \mathbf{x}=\Phi\mathbf{z} \). Sustituyendo y multiplicando por \( \Phi^{-1} \):

$$ \Phi\dot{\mathbf{z}}=A\Phi\mathbf{z}\;\Rightarrow\;\dot{\mathbf{z}}=\Phi^{-1}A\Phi\,\mathbf{z}=\Lambda\mathbf{z} $$

El sistema **se desacopla**: cada coordenada modal evoluciona sola, \( \dot z_i=\lambda_i z_i \), con solución \( z_i(t)=z_i(0)e^{\lambda_i t} \).

**Paso 3 — la respuesta es suma de modos.** Volviendo a \( \mathbf{x}=\Phi\mathbf{z} \), con autovector izquierdo \( \psi_i^\top \) (filas de \( \Phi^{-1} \), \( \psi_i^\top\phi_j=\delta_{ij} \)):

$$ \mathbf{x}(t)=\sum_{i=1}^{n}\phi_i\,\big(\psi_i^\top\mathbf{x}(0)\big)\,e^{\lambda_i t} $$

Cada término \( \phi_i e^{\lambda_i t} \) es un **modo**: \( \lambda_i=\sigma_i\pm j\omega_{d,i} \) fija su decaimiento y frecuencia; el autovector \( \phi_i \) fija su *forma* (cómo se reparte entre los estados). De aquí \( f=|\omega_d|/2\pi \) y \( \zeta=-\sigma/|\lambda| \).

**Paso 4 — factor de participación.** ¿Cuánto pesa el estado \( k \) en el modo \( i \)? El producto del autovector derecho \( \phi_{ki} \) (cómo el modo \( i \) aparece en el estado \( k \)) por el izquierdo \( \psi_{ik} \) (cuánto el estado \( k \) excita el modo \( i \)) es adimensional e invariante a la escala de los estados:

$$ \boxed{\;p_{ki}=|\psi_{ik}\,\phi_{ki}|\;} $$

Es la herramienta que en **01 - GFM-Impedance** señaló \( P_m,Q_m \) (lazo de potencia) como dominantes del modo inestable, orientando todo el rediseño. Conecta con [[estabilidad-bibo]]: la estabilidad la fija \( \max_i\mathrm{Re}(\lambda_i) \).

## Cuándo y por qué se usa
Para saber no solo **si** es estable, sino **qué** modo es problemático y **qué estados** lo
generan: clave para diagnosticar y corregir (¿es el lazo de potencia? ¿la resonancia LCL?).

## Procedimiento de diseño (genérico)
1. Linealiza para obtener \( A \) (ver [[linealizacion-numerica]]).
2. `eig(A)` → autovalores y autovectores.
3. Para cada modo de interés calcula \( f,\zeta \) y los factores de participación.
4. Si un modo está mal amortiguado/inestable, mira qué estados participan y actúa sobre esa parte (ganancia, filtro, impedancia virtual...).
5. Criterio práctico de aceptación: \( \zeta>0.1 \) (idealmente >0.3) en modos de control.

## Ejemplo de código
```python
import numpy as np
w, V = np.linalg.eig(A)                 # autovalores y autovectores derechos
Psi  = np.linalg.inv(V)                 # autovectores izquierdos (filas de Phi^-1)
i = np.argmax(w.real)                   # modo menos estable
f = abs(w[i].imag)/(2*np.pi)
zeta = -w[i].real/abs(w[i])
# factores de participacion (columna i)
P_col = np.abs(V[:, i] * Psi[i, :])
P_col /= P_col.sum()                    # normalizado a 1
print(f"f={f:.2f} Hz  zeta={zeta:.3f}")
print("participacion:", dict(zip(state_names, P_col)))
```

## Parámetros y valores típicos
\( \zeta \) objetivo: >0.1 aceptable, >0.3 bueno. Modos electromecánicos lentos (1–10 Hz),
resonancias de filtro (cientos de Hz–kHz). \( \zeta<0.05 \) requiere acción correctiva inmediata.

## Errores comunes
- Mirar solo \( \max\mathrm{Re}(\lambda) \) sin el amortiguamiento: un sistema "estable" puede tener un modo con \( \zeta \) pésimo.
- Ignorar los factores de participación → se ajusta a ciegas.
- Olvidar normalizar los autovectores antes de interpretar la forma modal.

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: diagnóstico): los factores de participación revelaron que el modo inestable inicial estaba dominado por \( P_m,Q_m \) (lazo de potencia), orientando todo el rediseño. Modo final de potencia: 3.3 Hz, \( \zeta=0.40 \).

## Conceptos relacionados
- [[linealizacion-numerica]] · [[droop-control]] · [[impedancia-salida-estabilidad]] · [[filtro-lcl]]

## Referencias
- Kundur, *Power System Stability and Control*, 1994.
- Verghese, Pérez-Arriaga, Schweppe, *Selective Modal Analysis*, IEEE TPAS 1982.

## 2 — Factores de participación: derivación y cálculo

### La matriz de participación y su definición
Los autovectores derechos \( \phi_i \) e izquierdos \( \psi_i \) (filas de \( \Psi=\Phi^{-1} \)) contienen información complementaria sobre cada modo:

- \( \phi_{ki} \) mide **cuánto oscila el estado \( k \)** dentro del modo \( i \): la amplitud relativa del estado en esa forma modal.
- \( \psi_{ik} \) mide **cuánto excita el estado \( k \)** al modo \( i \): el peso de la condición inicial \( x_k(0) \) en la amplitud de la coordenada modal \( z_i(0)=\psi_i^\top\mathbf{x}(0) \).

Su producto, elemento a elemento, forma la **matriz de participación**:

$$ \boxed{P_{ki} = \phi_{ki}\,\psi_{ik}} $$

Cada entrada \( P_{ki} \) cuantifica la participación del estado \( k \) en el modo \( i \). En la práctica se trabaja con el módulo \( |P_{ki}| \) para comparar magnitudes independientemente de la fase.

### Propiedad de normalización: \( \sum_k P_{ki}=1 \)
Que la suma de los factores de participación de **todos** los estados en un modo sea exactamente 1 es una consecuencia de la relación de biortogonalidad. La demostración parte de la definición:

$$ \sum_{k=1}^{n} P_{ki} = \sum_{k=1}^{n} \phi_{ki}\,\psi_{ik} $$

Esto es la suma de los productos de la columna \( i \) de \( \Phi \) con la fila \( i \) de \( \Psi=\Phi^{-1} \), que es el elemento \((i,i)\) del producto matricial:

$$ \sum_{k=1}^{n} \phi_{ki}\,\psi_{ik} = [\Phi^{-1}\Phi]_{ii} = [I]_{ii} = 1 $$

Cada fila de \( \Phi^{-1} \) es ortogonal a todas las columnas de \( \Phi \) salvo a la suya, por eso el producto es la identidad. La propiedad vale para **todos** los modos simultáneamente: la suma por columna de la matriz \( P \) siempre es 1, lo que la convierte en una distribución de probabilidad (no negativa si se usa \( |P_{ki}| \) y normalizada a 1).

La demostración alternativa via traza confirma la coherencia:

$$ \sum_{i=1}^{n}\sum_{k=1}^{n} P_{ki} = \mathrm{Tr}(\Phi^{-1}\Phi) = \mathrm{Tr}(I) = n $$

con lo que la suma total es \( n \) (el número de estados), y dividiendo entre \( n \) modos la media por modo es 1.

### Propiedades clave de los factores de participación
**Adimensionalidad.** Si se escala el estado \( k \) por una constante \( \alpha \) (un cambio de unidades), la columna \( k \) de \( \Phi \) se multiplica por \( \alpha \) y la fila \( k \) de \( \Psi \) se divide por \( \alpha \) (para que \( \Psi\Phi=I \) siga siendo la identidad). El producto \( \phi_{ki}\cdot\psi_{ik} \) es invariante a ese escalado. En contraste, los autovectores individuales sí cambian con el escalado de los estados.

**Independencia de la normalización de los autovectores.** En `numpy.linalg.eig`, los autovectores se devuelven normalizados (norma euclídea 1), pero cualquier reescalado uniforme de todos ellos se cancela en el producto \( \Phi\cdot\Psi \) (porque \( \Psi=\Phi^{-1} \)). Por eso los factores de participación son robustos frente a la elección de normalización.

**Simetría fila–columna.** La suma por fila \( \sum_i P_{ki} \) no tiene por qué ser 1 (suma la participación del estado \( k \) en todos los modos). La propiedad de normalización es por **columna** (por modo), no por fila (por estado).

### Ejemplo analítico completo
Se elige el sistema de segundo orden \( A=\bigl[\begin{smallmatrix}-1&2\\0&-3\end{smallmatrix}\bigr] \) porque los autovalores son reales y distintos, lo que permite verificar todo a mano sin números complejos.

**Autovalores.** El polinomio característico es:

$$ \det(A-\lambda I)=(-1-\lambda)(-3-\lambda)-0\cdot2 = \lambda^2+4\lambda+3 = (\lambda+1)(\lambda+3) $$

Por tanto \( \lambda_1=-1 \) y \( \lambda_2=-3 \). Ambos negativos → sistema estable.

**Autovectores derechos** \( A\phi_i=\lambda_i\phi_i \).

Para \( \lambda_1=-1 \): \( (A+I)\phi_1=0 \Rightarrow \bigl[\begin{smallmatrix}0&2\\0&-2\end{smallmatrix}\bigr]\phi_1=0 \Rightarrow \phi_1=\bigl[\begin{smallmatrix}1\\0\end{smallmatrix}\bigr] \) (o cualquier múltiplo).

Para \( \lambda_2=-3 \): \( (A+3I)\phi_2=0 \Rightarrow \bigl[\begin{smallmatrix}2&2\\0&0\end{smallmatrix}\bigr]\phi_2=0 \Rightarrow \phi_2=\bigl[\begin{smallmatrix}1\\-1\end{smallmatrix}\bigr] \).

Matriz de autovectores derechos:
$$ \Phi = \begin{bmatrix}1 & 1 \\ 0 & -1\end{bmatrix} $$

**Autovectores izquierdos** \( \Psi=\Phi^{-1} \). Para la matriz \( 2\times2 \):

$$ \Psi = \Phi^{-1} = \frac{1}{\det\Phi}\begin{bmatrix}-1 & -1 \\ 0 & 1\end{bmatrix} = \begin{bmatrix}1 & 1 \\ 0 & -1\end{bmatrix} $$

(ya que \( \det\Phi = 1\cdot(-1)-1\cdot0=-1 \), y el adjunto traspuesto es \( \bigl[\begin{smallmatrix}-1&0\\-1&1\end{smallmatrix}\bigr]^\top \), dividido entre \(-1\) da \( \Psi \)).

**Verificación de biortogonalidad:** \( \Psi\Phi=\bigl[\begin{smallmatrix}1&1\\0&-1\end{smallmatrix}\bigr]\bigl[\begin{smallmatrix}1&1\\0&-1\end{smallmatrix}\bigr]=\bigl[\begin{smallmatrix}1&0\\0&1\end{smallmatrix}\bigr]=I \). Correcto.

**Factores de participación.** La definición \( P_{ki}=\phi_{ki}\cdot\psi_{ik} \) usa la columna \( i \) de \( \Phi \) y la fila \( i \) de \( \Psi \):

Para el modo 1 (\( \lambda_1=-1 \)): columna 1 de \( \Phi \) es \( [1,\,0]^\top \) y fila 1 de \( \Psi \) es \( [1,\,1] \).

$$ P_{11}=1\cdot1=1, \qquad P_{21}=0\cdot1=0 $$

Para el modo 2 (\( \lambda_2=-3 \)): columna 2 de \( \Phi \) es \( [1,\,-1]^\top \) y fila 2 de \( \Psi \) es \( [0,\,-1] \).

$$ P_{12}=1\cdot0=0, \qquad P_{22}=(-1)\cdot(-1)=1 $$

**Interpretación.** \( P_{11}=1 \): el modo lento \( (\lambda_1=-1) \) está dominado exclusivamente por el estado \( x_1 \). \( P_{22}=1 \): el modo rápido \( (\lambda_2=-3) \) está dominado exclusivamente por el estado \( x_2 \). Suma por columna: \( P_{11}+P_{21}=1+0=1 \) ✓, \( P_{12}+P_{22}=0+1=1 \) ✓.

La interpretación física es coherente: el estado \( x_2 \) no aparece en el autovector del modo 1 (ya que \( A_{21}=0 \) desacopla \( x_2 \) de \( x_1 \) en esa dirección), así que \( x_2 \) no participa en ese modo.

**Respuesta libre.** Con \( \mathbf{x}(0)=[x_{10},\,x_{20}]^\top \):

$$ \mathbf{x}(t) = \phi_1\,(\psi_1^\top\mathbf{x}(0))\,e^{-t} + \phi_2\,(\psi_2^\top\mathbf{x}(0))\,e^{-3t} $$

$$ = \begin{bmatrix}1\\0\end{bmatrix}(x_{10}+x_{20})e^{-t} + \begin{bmatrix}1\\-1\end{bmatrix}(-x_{20})e^{-3t} $$

Esto confirma que \( x_1 \) participa en ambos modos (aparece en \( \phi_1 \) y en \( \phi_2 \)), mientras que \( x_2 \) solo aparece en el modo 2 a través de \( \phi_{22}=-1 \).

## 3 — Sensibilidad de los autovalores a parámetros

### La fórmula de primer orden
¿Cuánto se mueve el autovalor \( \lambda_i \) si se perturba un elemento de la matriz \( A \)? La respuesta de primer orden es:

$$ \boxed{\;\frac{\partial\lambda_i}{\partial A_{kj}} = \psi_{ik}\,\phi_{ji}\;} $$

donde \( \phi_{ji} \) es el elemento \( j \) del autovector derecho del modo \( i \), y \( \psi_{ik} \) es el elemento \( k \) del autovector izquierdo (fila \( i \) de \( \Phi^{-1} \)).

### Derivación paso a paso
**Punto de partida.** \( \lambda_i \) satisface \( A\phi_i=\lambda_i\phi_i \). Se diferencia esta ecuación respecto a un parámetro genérico \( \theta \):

$$ \frac{\partial A}{\partial\theta}\phi_i + A\frac{\partial\phi_i}{\partial\theta} = \frac{\partial\lambda_i}{\partial\theta}\phi_i + \lambda_i\frac{\partial\phi_i}{\partial\theta} $$

Reordenando:

$$ \frac{\partial A}{\partial\theta}\phi_i + (A-\lambda_i I)\frac{\partial\phi_i}{\partial\theta} = \frac{\partial\lambda_i}{\partial\theta}\phi_i $$

**Premultiplicar por \( \psi_i^\top \).** El autovector izquierdo satisface \( \psi_i^\top A=\lambda_i\psi_i^\top \), por tanto \( \psi_i^\top(A-\lambda_i I)=0 \). El segundo término del lado izquierdo se anula:

$$ \psi_i^\top\frac{\partial A}{\partial\theta}\phi_i = \frac{\partial\lambda_i}{\partial\theta}\,\underbrace{\psi_i^\top\phi_i}_{=\,1} $$

La normalización \( \psi_i^\top\phi_i=1 \) se cumple porque \( \Psi\Phi=I \Rightarrow [\Phi^{-1}]_i^\top[\Phi]_i=\delta_{ii}=1 \). Por tanto:

$$ \frac{\partial\lambda_i}{\partial\theta} = \psi_i^\top\frac{\partial A}{\partial\theta}\phi_i $$

**Perturbación de un solo elemento.** Si solo varía el elemento \( A_{kj} \), la diferencial de \( A \) es \( dA = e_k e_j^\top \) (la matriz que tiene un 1 en la posición \( (k,j) \) y cero en el resto). Entonces:

$$ \frac{\partial\lambda_i}{\partial A_{kj}} = \psi_i^\top(e_k e_j^\top)\phi_i = (\psi_i^\top e_k)(e_j^\top\phi_i) = \psi_{ik}\,\phi_{ji} $$

que es exactamente la fórmula enunciada.

### Conexión con los factores de participación
Para la **diagonal** \( A_{kk} \) (un elemento diagonal, que corresponde a la autorealimentación del estado \( k \)):

$$ \frac{\partial\lambda_i}{\partial A_{kk}} = \psi_{ik}\,\phi_{ki} = P_{ki} $$

La sensibilidad del autovalor \( \lambda_i \) a la autorealimentación del estado \( k \) es exactamente el factor de participación \( P_{ki} \). Este resultado justifica la definición de \( P_{ki} \): los estados que más participan en un modo son los que más mueven ese autovalor cuando se toca su dinámica propia. Cambiar la ganancia de un estado que no participa en el modo apenas desplaza ese autovalor.

### Sensibilidad a parámetros de diseño
En la práctica, la perturbación no es un elemento de \( A \) directamente, sino un parámetro de diseño \( \theta \) (una ganancia, una reactancia, un filtro). Por la regla de la cadena:

$$ \frac{\partial\lambda_i}{\partial\theta} = \sum_{k,j}\frac{\partial\lambda_i}{\partial A_{kj}}\frac{\partial A_{kj}}{\partial\theta} = \sum_{k,j}\psi_{ik}\,\phi_{ji}\,\frac{\partial A_{kj}}{\partial\theta} $$

Se evalúa numéricamente: linealizar con \( \theta \) y con \( \theta+\Delta\theta \), calcular los autovalores de ambas \( A \), y la diferencia dividida entre \( \Delta\theta \) da la sensibilidad.

### Ejemplo: sensibilidad al droop de potencia \( m_p \)
En el modelo GFM con droop, la rigidez de sincronización es \( K_s = EV/X \). La pendiente del droop \( m_p \) [rad/s/W] fija la inercia virtual equivalente: un \( m_p \) mayor reduce la inercia (el modo de potencia se vuelve más amortiguado pero también se mueve más rápido). La reactancia virtual \( X_{virt} \) actúa directamente sobre \( K_s = EV/(X+X_{virt}) \), reduciendo la rigidez y moviendo el autovalor hacia la izquierda (más amortiguado). El panel (c) de la figura siguiente muestra esta trayectoria al barrer \( X_{virt} \) de 0 a 0.30 pu.

<div class="cfig"><img src="figuras/analisis-modal-analisis.png" alt="4 paneles: mapa de autovalores, factores de participacion, trayectorias de autovalores al barrer Xvirt y Kad"><div class="cap">Los 4 paneles del análisis completo. (a) Mapa de autovalores del sistema GFM 5-estados: modo de potencia (~3 Hz, ζ≈0.40) y lazo de corriente (~900 Hz, ζ>0.7). (b) Factores de participación del modo de potencia: δ, ω y Pm dominan; id, iq apenas participan. (c) Trayectoria del autovalor de potencia al aumentar Xvirt (reduce Ks): se mueve a la izquierda, ganando amortiguamiento. (d) Trayectoria del autovalor de la resonancia LCL al aumentar Kad: con Kad=0 el ζ es ~0.02; con Kad=6 Ω sube a ~0.35.</div></div>

## 4 — Identificación de modos: el mapa de autovalores explicado

### Cómo leer el mapa
El plano de los autovalores, o **mapa de autovalores**, tiene en el eje horizontal la parte real \( \sigma \) y en el vertical la parte imaginaria \( \omega_d \):

- **Parte real \( \sigma \):** tasa de decaimiento exponencial. \( \sigma<0 \) → estable, el modo se amortigua. \( \sigma=0 \) → en el límite (oscilación sostenida). \( \sigma>0 \) → inestable. Cuanto más a la izquierda, más rápido se amortigua la perturbación.
- **Parte imaginaria \( \omega_d \):** frecuencia de oscilación amortiguada en rad/s. La frecuencia visible en simulación es \( f_d=\omega_d/(2\pi) \) Hz. Un autovalor real (sin parte imaginaria) corresponde a un modo puramente exponencial, sin oscilación.
- **Amortiguamiento \( \zeta=-\sigma/|\lambda| \):** el ángulo del vector \( \lambda \) respecto al eje real. Sobre el eje real, \( \zeta=1 \) (criticamente amortiguado). Sobre el eje imaginario, \( \zeta=0 \) (oscilación sin amortiguamiento).

### Círculos de amortiguamiento constante
Los lugares geométricos de amortiguamiento constante son arcos de círculo centrados en el origen. Para un \( \zeta \) fijo, todos los autovalores \( \lambda=-\zeta\omega_n\pm j\omega_n\sqrt{1-\zeta^2} \) tienen el mismo módulo \( |\lambda|=\omega_n \) y el mismo ángulo \( \angle\lambda=\pi-\arccos(\zeta) \) (entre \( \pi/2 \) y \( \pi \) para \( 0<\zeta<1 \)):

$$ \zeta = \frac{-\sigma}{|\lambda|} = \cos(\pi - \angle\lambda) \quad\Rightarrow\quad \angle\lambda=\arccos(-\zeta) $$

Los arcos de \( \zeta=0.1 \), \( \zeta=0.3 \) y \( \zeta=0.7 \) dividen el semiplano izquierdo en zonas de calidad decreciente: por encima de \( \zeta=0.1 \) el sistema es marginalmente aceptable; entre \( 0.1 \) y \( 0.3 \) el comportamiento transitorio tiene picos notables; por encima de \( 0.3 \) la respuesta es suave. En el panel (a) de la figura se dibujan estos tres arcos.

### Clasificación de modos en convertidores de potencia

| Tipo de modo | Rango típico de frecuencia | Origen físico |
|---|---|---|
| Modo de potencia (sincronización) | 0.5 – 10 Hz | Droop de potencia activa + inercia virtual |
| Modo de tensión / Q-V | 1 – 20 Hz | Droop de reactiva + filtros de potencia |
| Lazo de corriente | 100 – 2000 Hz | Controlador PI de corriente + filtro LCL |
| PLL | 10 – 200 Hz | Lazo de seguimiento de ángulo |
| Resonancia LCL | 500 – 5000 Hz | Red LC del filtro |
| Modo de bus DC | 5 – 500 Hz | Capacidad del bus DC + controlador |

La separación de escalas entre grupos es lo que permite la **reducción de orden** del apartado 6: los modos de alta frecuencia (lazo de corriente, resonancia LCL) decaen mucho antes de que los lentos (modo de potencia) se muevan, y se pueden reemplazar por su valor en régimen permanente.

### Los modos del proyecto 01 - GFM-Impedance
El sistema linealizado tiene 15 estados. Los tres modos más relevantes en el informe son:

| Modo | Autovalor \( \lambda \) | Frecuencia | \( \zeta \) | Estados dominantes |
|---|---|---|---|---|
| Potencia (tras rediseño) | \( -8.3\pm j20.7 \) | 3.3 Hz | 0.37 | \( P_m, Q_m, \delta \) |
| Resonancia LCL (sin Kad) | \( -130\pm j21\,380 \) | 3404 Hz | 0.006 | \( i_{L1}, v_C, i_{L2} \) |
| Resonancia LCL (con Kad=6) | \( -7540\pm j20\,260 \) | 3226 Hz | 0.35 | \( i_{L1}, v_C, i_{L2} \) |

El modo de potencia a 3.3 Hz es el que preocupa en la estabilidad de sincronización. La resonancia LCL aparece a 3404 Hz pero sin amortiguamiento activo tiene \( \zeta=0.006 \): es marginalmente estable y puede excitarse con perturbaciones de alta frecuencia (commutation noise). Con \( K_{ad}=6\,\Omega \) el amortiguamiento sube a 0.35, que es robusto.

### Qué hacer cuando \( \zeta<0.1 \)
1. **Calcular los factores de participación** del modo en cuestión.
2. **Identificar qué estados dominan**: los que tienen \( P_{ki}>0.2 \) (20% de la participación normalizada).
3. **Actuar sobre esos estados**: si domina \( P_m \) → reducir la rigidez de sincronización (reactancia virtual); si domina \( i_{L1} \) → añadir amortiguamiento activo; si domina \( v_{bus,DC} \) → revisar el controlador del bus DC.
4. **Verificar con sensibilidades** (apartado 3): calcular \( \partial\lambda/\partial\theta \) para el parámetro de diseño disponible y mover en la dirección que lleva \( \lambda \) al semiplano izquierdo con más \( \zeta \).

## 5 — Forma modal: qué estados forman cada modo

### El autovector derecho \( \phi_i \): forma del modo
El autovector derecho \( \phi_i \) describe cómo se distribuye la oscilación del modo \( i \) entre los estados físicos. Para el modo \( i \):

$$ \mathbf{x}(t)\big|_{\text{modo }i} = \phi_i\,z_i(0)\,e^{\lambda_i t} $$

La componente \( \phi_{ki} \) es la amplitud relativa (compleja) con que oscila el estado \( k \) dentro del modo. La magnitud \( |\phi_{ki}| \) da el tamaño de la oscilación; el argumento \( \angle\phi_{ki} \) da el desfase respecto al resto de estados en ese modo.

**Forma del modo de potencia:** Para el droop GFM de 5 estados \( [\delta,\omega,P_m,i_d,i_q] \), el autovector del modo de potencia tiene \( \phi_\delta \) y \( \phi_\omega \) en cuadratura \( (90°) \): el ángulo \( \delta \) y la velocidad angular \( \omega \) oscilan con 90° de diferencia, que es la firma del movimiento pendular de un oscilador de segundo orden. \( P_m \) sigue a \( \omega \) con un retraso adicional determinado por el filtro de potencia \( \omega_f \). Los estados de corriente \( i_d,i_q \) tienen amplitudes muy pequeñas en este modo porque el lazo de corriente es mucho más rápido (ver separación de escalas en el apartado 6).

**Forma del modo de resonancia LCL:** Para el modo LCL \( [i_{L1},v_C,i_{L2}] \), el autovector muestra tres componentes a la frecuencia de resonancia: \( i_{L1} \) y \( i_{L2} \) oscilan con amplitudes opuestas (fluyen en sentidos contrarios para cargar/descargar \( C_f \)), mientras que \( v_C \) va en cuadratura con ambas (el condensador almacena la energía cuando las corrientes cruzan por cero). Esta es la forma del modo de resonancia LC.

### El autovector izquierdo \( \psi_i \): observabilidad e impacto inicial
El autovector izquierdo \( \psi_i^\top \) (fila \( i \) de \( \Phi^{-1} \)) actúa como un detector: indica **qué señal medir** para observar bien el modo \( i \), y qué condición inicial excita más ese modo.

La amplitud de la coordenada modal al inicio es \( z_i(0)=\psi_i^\top\mathbf{x}(0) \). Si \( |\psi_{ik}| \) es grande para el estado \( k \), entonces una perturbación en ese estado excita fuertemente el modo \( i \). Esto define la **excitabilidad**: un estado muy excitable puede desencadenar oscilaciones de un modo peligroso.

Simétricamente, para **observar** el modo \( i \) hay que medir una combinación \( y=C\mathbf{x} \) tal que \( C\phi_i\neq0 \): la salida \( y \) "ve" el modo si y solo si el vector \( C \) no es ortogonal al autovector derecho. Por eso el modo de potencia se detecta fácilmente midiendo la potencia activa (directamente proporcional a \( \delta \) en el modelo linealizado), pero no es evidente en la tensión del bus si \( \phi_{V_{bus},i} \) es pequeño.

### Ejemplo: el modo de potencia del GFM
El estado más visible del modo de potencia en medición es \( P_m \) (la potencia filtrada): tiene la mayor amplitud en el autovector derecho y al mismo tiempo excita el modo si hay un error en la referencia de potencia. En el proyecto 01, el análisis de la forma modal confirmó que el modo de potencia era principalmente un intercambio de energía entre \( \delta \) (reactancia angular) y \( P_m \) (potencia filtrada), con \( \omega \) como la variable intermediaria. Esta comprensión orientó el rediseño: reducir la rigidez \( K_s \) (reactancia virtual) suaviza el acoplamiento entre \( \delta \) y \( P_m \), bajando la frecuencia del modo y aumentando su amortiguamiento.

## 6 — Reducción de orden: separación de escalas temporal

### El principio de separación de escalas
Cuando el sistema tiene modos con frecuencias muy distintas, los rápidos decaen en un tiempo mucho menor que el periodo de los lentos. Si el modo lento tiene parte real \( |\sigma_s| \) y el rápido \( |\sigma_f| \gg |\sigma_s| \), la respuesta del modo rápido a una excitación desaparece antes de que el modo lento haya cambiado apreciablemente. En ese caso, para el modelo del modo lento el estado rápido siempre parece estar en su valor de equilibrio condicionado por el estado lento.

Este es el fundamento de la **reducción de orden por régimen cuasi-estático**, que reemplaza las ecuaciones diferenciales de los estados rápidos por ecuaciones algebraicas.

### El método formal
Particiona los estados en rápidos \( \mathbf{x}_f \) (lazo de corriente, resonancia LCL...) y lentos \( \mathbf{x}_s \) (potencia, tensión de bus...). El sistema linealizado en bloques es:

$$ \begin{bmatrix}\dot{\mathbf{x}}_s\\\dot{\mathbf{x}}_f\end{bmatrix} = \begin{bmatrix}A_{ss}&A_{sf}\\A_{fs}&A_{ff}\end{bmatrix}\begin{bmatrix}\mathbf{x}_s\\\mathbf{x}_f\end{bmatrix} + \begin{bmatrix}B_s\\B_f\end{bmatrix}\mathbf{u} $$

**Condición cuasi-estática de los estados rápidos.** Para los estados rápidos \( \mathbf{x}_f \), la dinámica \( \dot{\mathbf{x}}_f \approx 0 \) (el estado "casi no se mueve" en la escala de tiempo de los lentos):

$$ 0 \approx A_{ff}\mathbf{x}_f + A_{fs}\mathbf{x}_s + B_f\mathbf{u} \quad\Rightarrow\quad \mathbf{x}_f \approx -A_{ff}^{-1}(A_{fs}\mathbf{x}_s + B_f\mathbf{u}) $$

Esto requiere que \( A_{ff} \) sea invertible, lo que equivale a que ningún autovalor del bloque rápido sea cero (todos los modos rápidos son estables, lo cual se cumple por hipótesis si son "rápidos" con \( \sigma_f\ll0 \)).

**Modelo reducido.** Sustituyendo \( \mathbf{x}_f \) en la ecuación de los estados lentos:

$$ \dot{\mathbf{x}}_s = A_{ss}\mathbf{x}_s + A_{sf}\mathbf{x}_f + B_s\mathbf{u} $$
$$ = (A_{ss} - A_{sf}A_{ff}^{-1}A_{fs})\mathbf{x}_s + (B_s - A_{sf}A_{ff}^{-1}B_f)\mathbf{u} $$

La matriz \( \tilde{A}_s = A_{ss} - A_{sf}A_{ff}^{-1}A_{fs} \) es la **matriz del modelo reducido**. El segundo término \( -A_{sf}A_{ff}^{-1}A_{fs} \) captura la influencia de los estados rápidos sobre los lentos a través de la respuesta estática de los primeros.

### Por qué el lazo de corriente se simplifica a \( 1/(1+s/\omega_{ci}) \)
El lazo de corriente cerrado (con un PI bien sintonizado) se comporta como un filtro de primer orden de ancho de banda \( \omega_{ci} \): la corriente sigue a su referencia con la dinámica \( I(s)=\omega_{ci}/(s+\omega_{ci})\cdot I^*(s) \). Cuando el lazo de tensión opera a una frecuencia \( \omega_{cv}\ll\omega_{ci} \) (condición de separación de escalas), la corriente puede considerarse siempre en régimen permanente para las perturbaciones de la tensión: \( i\approx i^* \). Esto es exactamente la reducción de orden: reemplazar la dinámica del lazo de corriente (varios polos) por la ganancia unitaria (el estado rápido en su cuasi-estático).

**Condición práctica.** La aproximación es válida cuando la frecuencia de cruce del lazo lento es al menos 5–10 veces menor que la del lazo rápido. En los proyectos del repositorio, el lazo de corriente tiene \( \omega_{ci}\approx2\pi\cdot900 \) rad/s y el lazo de potencia opera en torno a \( 2\pi\cdot10 \) rad/s: separación de factor 90, más que suficiente.

### Reducción del proyecto 01: de 15 a 4 estados
El sistema GFM completo tiene 15 estados:

| Grupo | Estados | Número | Escala temporal |
|---|---|---|---|
| Filtro LCL | \( i_{L1d}, i_{L1q}, v_{Cd}, v_{Cq}, i_{L2d}, i_{L2q} \) | 6 | ~ µs (resonancia a 3 kHz) |
| Lazo de corriente | \( \xi_{id}, \xi_{iq} \) (integradores del PI) | 2 | ~ ms (BW 900 Hz) |
| Potencias filtradas | \( P_m, Q_m \) | 2 | ~ 16 ms (BW 10 Hz) |
| PLL | \( \xi_{PLL}, \omega_{PLL} \) | 2 | ~ 20 ms (BW 8 Hz) |
| Bus DC | \( V_{DC} \) | 1 | ~ 10 ms |
| Integrador tensión | \( \xi_v \) | 1 | ~ 5 ms |
| Ángulo virtual | \( \delta \) | 1 | ~ 50 ms (modo potencia 3 Hz) |

Aplicando la reducción de orden en dos etapas: primero los estados del filtro LCL + lazo de corriente se reemplazan por la ganancia del lazo (corriente = referencia), quedando 7 estados; después la PLL en su valor cuasi-estático (reduce 2 más), quedando 5 estados efectivos \( [\delta, \omega, P_m, Q_m, V_{bus}] \). Estos 5 estados capturan los modos lentos (< 20 Hz) con error menor al 1% para análisis de estabilidad del lazo de potencia.

La validez de esta reducción se comprueba modalmente: los autovalores del modelo completo de 15 estados referentes a los modos de potencia coinciden con los del modelo reducido de 5 estados hasta la cuarta cifra significativa, mientras que los modos eliminados (lazo de corriente, LCL) desaparecen del espectro.

## 7 — Aplicación al proyecto 01: diagnóstico completo

### Los 15 estados del sistema GFM completo
El modelo del proyecto 01 (VSC de 1 MVA, filtro LCL, droop de potencia, control cascada corriente–tensión) tiene el siguiente vector de estados:

$$ \mathbf{x}=\bigl[i_{L1d},\,i_{L1q},\,v_{Cd},\,v_{Cq},\,i_{L2d},\,i_{L2q},\,\xi_{id},\,\xi_{iq},\,P_m,\,Q_m,\,\xi_{PLL},\,\omega_{PLL},\,V_{DC},\,\xi_v,\,\delta\bigr]^\top $$

Los parámetros principales: \( L_1=2 \) mH, \( L_2=0.5 \) mH, \( C_f=15\,\mu\text{F} \), \( R_1=50 \) mΩ; frecuencia de conmutación \( f_{sw}=10 \) kHz; droop \( m_p=1.571\times10^{-3} \) rad/s/W; ancho de banda del filtro de potencia \( \omega_f=2\pi\cdot10 \) rad/s; BW del lazo de corriente \( \omega_{ci}=2\pi\cdot900 \) rad/s.

### Los 3 modos más importantes: análisis antes del rediseño
**Modo 1: potencia (el problemático inicial).** Antes del rediseño (sin reactancia virtual, \( X_{virt}=0 \)) la rigidez de sincronización es alta: \( K_s=EV/X_{red}\approx 500 \) kW/rad. El autovalor del modo de potencia resulta:

$$ \lambda_{pot}^{ini} \approx -2.1\pm j22.4\ \text{rad/s} \quad\Rightarrow\quad f=3.6\ \text{Hz},\quad \zeta=0.094 $$

\( \zeta=0.094<0.1 \): el sistema es marginalmente aceptable. Cualquier perturbación de potencia produce oscilaciones que tardan varios segundos en amortiguarse.

**Modo 2: resonancia LCL (sin amortiguamiento activo).** Con \( K_{ad}=0 \), el único amortiguamiento de la resonancia LCL proviene de las resistencias parásitas:

$$ \lambda_{LCL}^{sin\ Kad} \approx -130\pm j21\,380\ \text{rad/s} \quad\Rightarrow\quad f=3404\ \text{Hz},\quad \zeta=0.006 $$

\( \zeta=0.006 \ll 0.1 \): la resonancia LCL está prácticamente sin amortiguamiento. Una perturbación de alta frecuencia (como el ruido de la modulación) puede excitar este modo.

**Modo 3: lazo de corriente.** Con BW \( \omega_{ci}=2\pi\cdot900 \) rad/s y PI bien sintonizado, los polos del lazo de corriente están en:

$$ \lambda_{ci} \approx -\omega_{ci}\pm j\omega_{ci}\sqrt{1-\zeta_{ci}^2} \quad\Rightarrow\quad f\approx900\ \text{Hz},\quad \zeta>0.70 $$

Bien amortiguado, invisible en simulaciones a escala de potencia, y justificado eliminarlo por reducción de orden.

### Factores de participación del modo de potencia (antes del rediseño)
Calculados sobre el modelo de 15 estados, los 5 estados con mayor participación en el modo de potencia (antes del rediseño, \( X_{virt}=0 \)) son:

| Estado | \( P_{ki} \) (normalizado) | Interpretación |
|---|---|---|
| \( P_m \) (potencia activa filtrada) | 0.38 | Lazo de potencia: el dominante |
| \( Q_m \) (reactiva filtrada) | 0.22 | Lazo de reactiva: acoplado al de potencia |
| \( \delta \) (ángulo virtual) | 0.19 | Ángulo de sincronización |
| \( \xi_v \) (integrador tensión) | 0.09 | Lazo de tensión |
| \( \omega_{PLL} \) (vel. angular PLL) | 0.06 | PLL: acoplamiento cruzado |

Los 10 estados restantes (filtro LCL, lazo de corriente) suman menos del 6% total. Esta distribución confirma que el modo de potencia está determinado principalmente por el lazo de droop (\( P_m, Q_m \)) y el ángulo (\( \delta \)): son los estados que hay que tocar para corregirlo.

### El rediseño: reactancia virtual \( X_{virt}=0.05 \) pu
La acción correctiva es añadir una reactancia virtual \( X_{virt} \) que reduce la rigidez de sincronización efectiva:

$$ K_s^{nuevo} = \frac{EV}{X_{red}+X_{virt}} < K_s^{ini} $$

Con \( X_{virt}=0.05 \) pu (la reactancia base del convertidor), el autovalor de potencia resulta:

$$ \lambda_{pot}^{red} \approx -8.3\pm j20.7\ \text{rad/s} \quad\Rightarrow\quad f=3.3\ \text{Hz},\quad \zeta=0.37 $$

El amortiguamiento pasa de 0.094 a 0.37: un factor 4 de mejora. La frecuencia del modo baja ligeramente (de 3.6 a 3.3 Hz) porque al reducir \( K_s \) se reduce la "rigidez" del oscilador equivalente. El autovalor se mueve hacia la izquierda en el mapa (panel (c) de la figura).

La corrección se justifica con la fórmula de sensibilidad:

$$ \frac{\partial\lambda_{pot}}{\partial X_{virt}} = \frac{\partial\lambda_{pot}}{\partial K_s}\cdot\frac{\partial K_s}{\partial X_{virt}} = P_{k_{P_m},pot}\cdot\left(-\frac{EV}{(X_{red}+X_{virt})^2}\right) $$

El signo es negativo: aumentar \( X_{virt} \) mueve \( \lambda_{pot} \) hacia la izquierda (más negativo en parte real), es decir, incrementa el amortiguamiento. La magnitud de la sensibilidad es proporcional al factor de participación de \( P_m \), que es 0.38: el estado más dominante del modo es el que más responde al cambio de parámetro.

### El amortiguamiento activo Kad: acción sobre la resonancia LCL
El amortiguamiento activo \( K_{ad} \) introduce una realimentación de la tensión del condensador \( v_C \) en la referencia del lazo de corriente: la tensión de control efectiva es \( v_i^{ref} = v_i^{ref,nominal} - K_{ad}(i_{L1}-i^{ref}) \). Esto equivale a añadir una resistencia virtual \( K_{ad} \) en serie con \( L_1 \), que desplaza el polo resonante hacia el semiplano izquierdo.

Derivación de la posición del polo resonante con \( K_{ad} \): el modelo del filtro LCL con amortiguamiento activo tiene una matriz \( A \) donde el elemento \( A_{11}=-(R_1+K_{ad})/L_1 \) (la amortiguación de \( i_{L1} \) aumenta). La traza del bloque LCL es:

$$ \mathrm{Tr}(A_{LCL}) = -\frac{R_1+K_{ad}}{L_1} - 0 - \frac{R_2}{L_2} $$

Por la fórmula de suma de autovalores (traza = suma), la parte real de los autovalores del bloque LCL se hace más negativa al aumentar \( K_{ad} \), y el amortiguamiento del modo resonante crece linealmente con \( K_{ad} \) para valores pequeños.

### Tabla comparativa antes/después del rediseño

| Grandeza | Antes (sin rediseño) | Después (con rediseño) | Mejora |
|---|---|---|---|
| \( \lambda_{pot} \) | \( -2.1\pm j22.4 \) | \( -8.3\pm j20.7 \) | σ × 4 |
| \( f_{pot} \) | 3.6 Hz | 3.3 Hz | — |
| \( \zeta_{pot} \) | 0.094 | 0.37 | × 4 |
| \( \lambda_{LCL} \) | \( -130\pm j21380 \) | \( -7540\pm j20260 \) | σ × 58 |
| \( f_{LCL} \) | 3404 Hz | 3226 Hz | — |
| \( \zeta_{LCL} \) | 0.006 | 0.35 | × 58 |
| Estado dominante (modo pot.) | \( P_m \) (38%) | \( P_m \) (36%) | redistribución leve |
| Estado dominante (modo LCL) | \( i_{L1}, v_C \) | \( i_{L1}, v_C \) | igual (el mecanismo no cambia) |

Los dos cambios actúan sobre modos distintos y pueden aplicarse de forma independiente: \( X_{virt} \) solo afecta al modo de potencia (opera a 3 Hz); \( K_{ad} \) solo afecta al modo LCL (opera a 3 kHz). La separación de escalas garantiza que no interfieren entre sí, lo cual confirma el análisis modal: la reducción de orden que proyecta cada modo sobre sus estados dominantes produce modelos completamente desacoplados para estas frecuencias tan diferentes.
