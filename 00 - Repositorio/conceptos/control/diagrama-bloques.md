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

## Conceptos relacionados
- [[funcion-transferencia]] · [[realimentacion]] · [[control-cascada]] · [[funciones-sensibilidad]]

## Referencias
- Ogata, *Ingeniería de Control Moderna*.
- Nise, *Control Systems Engineering*.
