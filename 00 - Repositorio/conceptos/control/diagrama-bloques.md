---
titulo: Diagrama de bloques y álgebra de bloques
slug: diagrama-bloques
categoria: control
tipo: concepto
nivel: basico
proyectos: []
objetivos: [interconectar subsistemas y reducirlos a una función de transferencia equivalente]
tags: [diagrama-bloques, algebra-bloques, interconexion, lazo-cerrado, basico]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-01
relacionados: [funcion-transferencia, realimentacion, control-cascada, error-regimen-permanente]
referencias:
  - "Ogata, Ingeniería de Control Moderna, Pearson"
  - "Nise, Control Systems Engineering, Wiley"
---

## Definición
Representación gráfica de un sistema como **bloques** (funciones de transferencia) unidos por
señales, con **sumadores** y **puntos de bifurcación**. El álgebra de bloques permite reducirlo a
una única \( G_{eq}(s) \).

## Fundamento teórico
Reglas básicas de combinación:
- **Serie (cascada):** \( G_1G_2 \).
- **Paralelo:** \( G_1\pm G_2 \).
- **Realimentación:** lazo con planta \( G \) y sensor \( H \):
$$ \frac{Y}{R}=\frac{G}{1+GH}\quad(\text{negativa}),\qquad \frac{G}{1-GH}\quad(\text{positiva}) $$
\( L=GH \) es la **ganancia de lazo**; \( 1+L \) el **denominador característico**. Mover un
sumador o una bifurcación a través de un bloque exige multiplicar/dividir por ese bloque para
conservar las señales. Para topologías densas, la **regla de Mason** da \( G_{eq} \) directamente.

<div class="cfig"><img src="figuras/diagrama-bloques-reduccion.png" alt="reduccion de un lazo realimentado"><div class="cap">Reducción de un lazo: el bucle con planta G y sensor H equivale a G/(1+GH). Series → G1·G2, paralelo → G1±G2, realimentación → esta fórmula.</div></div>

## 1 — Álgebra de bloques: serie, paralelo y realimentación por sustitución algebraica

**Paso 1 — conexión en serie.** Dos bloques \( G_1 \) y \( G_2 \) en cascada: la salida del primero es la entrada del segundo. Si \( U \) es la entrada, \( W=G_1 U \) y \( Y=G_2 W = G_2 G_1 U \). Dividiendo por \( U \):

$$ \boxed{G_{serie}=G_1 G_2} $$

El orden de los bloques importa si son matrices (MIMO), pero en SISO la multiplicación de escalares es conmutativa.

**Paso 2 — conexión en paralelo.** Dos bloques con la misma entrada \( U \) cuyas salidas se suman: \( Y=G_1 U \pm G_2 U = (G_1\pm G_2)U \). Dividiendo por \( U \):

$$ \boxed{G_{paralelo}=G_1\pm G_2} $$

**Paso 3 — lazo de realimentación negativa.** La planta \( G \) y el sensor \( H \) forman el lazo. Definiendo las señales: error \( E=R-HY \), salida \( Y=GE \). Sustituyendo \( E \):

$$ Y = G\,(R-HY) = GR - GHY $$

Despejando \( Y \) al reagrupar el término \( GHY \) en la izquierda:

$$ Y(1+GH)=GR $$

$$ \boxed{\frac{Y}{R}=\frac{G}{1+GH}} $$

La ganancia de lazo es \( L=GH \); el denominador \( 1+L \) es el polinomio característico — sus raíces son los polos de lazo cerrado. Para realimentación positiva basta cambiar el signo: \( G/(1-GH) \).

## Cuándo y por qué se usa
Para modelar sistemas con varios lazos (corriente dentro de tensión dentro de potencia → ver
[[control-cascada]]), identificar la ganancia de lazo que entra en Nyquist/Bode y derivar las
[[funciones-sensibilidad]] \( S=1/(1+L) \), \( T=L/(1+L) \).

## Procedimiento (genérico)
1. Dibuja bloques y señales; marca entradas, salidas y perturbaciones.
2. Reduce series y paralelos.
3. Cierra lazos internos con la fórmula de realimentación (de dentro hacia afuera).
4. Obtén \( G_{eq} \); identifica \( L \), \( S \), \( T \).

## Ejemplo de aplicación real
**Problema:** Control en cascada: lazo interno de corriente con FT cerrada \( H_i(s)=\omega_{ci}/(s+\omega_{ci}) \) y planta capacitiva del bus \( G_v(s)=1/(Cs) \). Reducir el diagrama y hallar la FT de referencia de tensión a tensión de salida.

Paso 1: el lazo interno está ya reducido a \( H_i(s) \). Paso 2: la planta que ve el lazo externo es \( H_i\cdot G_v=\omega_{ci}/[(s+\omega_{ci})\,Cs] \). Paso 3: con PI externo \( C_v(s) \): la FT de lazo cerrado externo es \( G_{v,cl}=C_v H_i G_v/(1+C_v H_i G_v) \). Con \( \omega_{ci}\gg\omega_{cv} \) (separación de escalas), \( H_i\approx1 \) en la banda del lazo externo y el diagrama se simplifica a \( C_v/Cs/(1+C_v/(Cs)) \). La separación de escalas es la condición que hace válida esta simplificación.

## Ejemplo de código
```python
import control as ct
G = ct.tf([5], [1, 2]); H = ct.tf([1], [1])
T = ct.feedback(G, H)              # G/(1+GH): lazo cerrado
```

## Parámetros y valores típicos
En cascada, el lazo interno suele ser 5–10× más rápido que el externo, de modo que se aproxima a
ganancia unidad en la banda del externo.

## Errores comunes
- Mover un sumador/bifurcación sin compensar con el bloque → señales incorrectas.
- Confundir lazo abierto \( L \) con lazo cerrado \( T \).
- Reducir lazos acoplados como si fueran independientes.

## 3 — Álgebra de diagramas de bloques

Las cuatro reglas cubren cualquier topología plana:

**Serie (cascada).** \( G_{total} = G_1 G_2 \). La salida de \( G_1 \) es la entrada de \( G_2 \); la función de transferencia compuesta es el producto.

**Paralelo.** \( G_{total} = G_1 \pm G_2 \). Ambos bloques reciben la misma entrada; sus salidas se suman o restan.

**Realimentación.** Con planta \( G \) y sensor \( H \):
$$ G_{total} = \frac{G}{1 \pm GH} $$
El signo \( + \) corresponde a realimentación negativa (estabilizadora típica), el \( - \) a positiva.

**Movimiento de nodo sumador o de ramificación.** Para mover un sumador *antes* de un bloque \( G \): dividir la señal que se suma por \( G \) (o multiplica si se mueve *después*). Para mover un punto de bifurcación *después* de \( G \): multiplicar la señal bifurcada por \( G \). Estas equivalencias preservan exactamente la función de transferencia global.

## 4 — Función de transferencia de lazo cerrado

Para el lazo estándar con controlador \( C(s) \), planta \( G(s) \) y sensor \( H(s) \):
$$ T(s) = \frac{C(s)G(s)}{1 + C(s)G(s)H(s)} $$

Definiendo la ganancia de lazo \( L = C(s)G(s)H(s) \), surgen las funciones de sensibilidad:

- **Sensibilidad:** \( S = \dfrac{1}{1+L} \) — cuánto se atenúa una perturbación en el lazo.
- **Sensibilidad complementaria:** \( T = \dfrac{L}{1+L} \) — cómo se transmite la referencia.
- **Identidad fundamental:** \( S + T = 1 \) — una mejora en \( S \) implica degradación en \( T \) y viceversa.

**Rechazo de perturbación en la planta.** Si una perturbación \( D \) entra a la salida de la planta:
$$ \frac{Y}{D} = \frac{G}{1+CG} = S \cdot G $$
El lazo reduce la perturbación en \( 1+L \) en la banda donde \( |L| \gg 1 \).

**Rechazo de ruido en la medida.** Si un ruido \( N \) se suma a la señal medida:
$$ \frac{Y}{N} = -T = -\frac{L}{1+L} $$
El lazo transmite el ruido de medida con ganancia \( |T| \); como \( S + T = 1 \), no se puede tener a la vez gran atenuación de perturbaciones y gran atenuación de ruido en la misma frecuencia.

## 5 — Diagramas de señal (Mason)

El **grafo de flujo de señal** representa las señales del sistema como **nodos** y las ganancias directas entre ellos como **ramas** dirigidas. Cada lazo de realimentación queda visible como un ciclo en el grafo.

**Fórmula de Mason.** La ganancia total entre la entrada y la salida es:
$$ T = \frac{\sum_k M_k \Delta_k}{\Delta} $$
donde:
- \( M_k \): ganancia del \( k \)-ésimo camino directo (producto de las ganancias de sus ramas).
- \( \Delta \): determinante del grafo.
- \( \Delta_k \): cofactor del camino \( k \) (determinante del subgrafo que no toca el camino \( k \)).

**Determinante del grafo:**
$$ \Delta = 1 - \sum_i L_i + \sum_{i,j\,\text{no tocan}} L_i L_j - \sum_{i,j,k\,\text{no tocan}} L_i L_j L_k + \cdots $$
donde \( L_i \) es la ganancia de cada lazo individual. Los términos alternados en signo provienen de lazos que no comparten ningún nodo.

**Ventaja práctica.** Para sistemas con múltiples lazos cruzados (convertidores multivariable, cascadas complejas), Mason permite hallar \( T \) sin reducir gráficamente el diagrama paso a paso: basta enumerar caminos directos y lazos.

## 6 — Diagrama de bloques del lazo de corriente dq

En un convertidor trifásico controlado en el marco dq, la planta es el filtro RL: \( G(s) = 1/(Ls+R) \) por canal. El esquema completo incluye:

1. **Referencia:** \( i_d^* \), \( i_q^* \) → controladores PI → tensiones de modulación \( v_d^* \), \( v_q^* \).
2. **Planta:** la tensión aplicada a \( L \) y \( R \) produce la corriente \( i_d \), \( i_q \).

**Acoplamiento entre canales.** La inductancia en el marco dq introduce los términos \( \omega_0 L i_q \) (en el canal d) y \( -\omega_0 L i_d \) (en el canal q). Sin cancelación, la función de transferencia cruzada \( G_{dq}(s) \neq 0 \): una perturbación en el canal d genera respuesta en el canal q y viceversa.

**Feedforward de desacoplamiento.** Se añaden señales de feedforward que cancelan exactamente el acoplamiento:
- Canal d: sumar \( +\omega_0 L \hat{i}_q \) a la salida del PI.
- Canal q: sumar \( -\omega_0 L \hat{i}_d \) a la salida del PI.

Con feedforward activo y estimación precisa de \( \omega_0 L \), cada canal opera como un lazo de corriente SISO independiente \( G(s) = 1/(Ls+R) \), lo que simplifica el diseño del PI al de un sistema de primer orden. Sin feedforward, el acoplamiento actúa como perturbación que degrada la respuesta transitoria y aumenta el sobreimpulso cruzado.

<div class="cfig"><img src="../figuras/diagrama-bloques-analisis.png" alt="Algebra de bloques, lazo dq con y sin feedforward, sensibilidades S y T, rechazo de perturbacion"><div class="cap">Panel superior izquierdo: resumen del álgebra de bloques y funciones de sensibilidad. Superior derecho: efecto del feedforward de acoplamiento dq — con FF los canales quedan desacoplados. Inferior izquierdo: módulo de S y T del lazo de corriente; obsérvese S+T=1 (línea verde). Inferior derecho: respuesta ante perturbación atenuada por el lazo cerrado.</div></div>

## Conceptos relacionados
- [[funcion-transferencia]] · [[realimentacion]] · [[control-cascada]] · [[funciones-sensibilidad]]

## Referencias
- Ogata, *Ingeniería de Control Moderna*.
- Nise, *Control Systems Engineering*.
