---
titulo: Observador de estados (Luenberger)
slug: observador-estados
categoria: control
tipo: metodo
nivel: intermedio
proyectos: []
objetivos: [estimar estados no medidos a partir de entradas y salidas]
tags: [observador, luenberger, estimador, separacion, espacio-estados, intermedio, control]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-09
relacionados: [controlabilidad-observabilidad, asignacion-polos-lqr, representacion-espacio-estados, variables-estado]
referencias:
  - "Ogata, Ingeniería de Control Moderna, Pearson"
  - "Franklin, Powell, Feedback Control of Dynamic Systems, Pearson"
---

## Definición
Sistema dinámico que **reconstruye el vector de estado** \( \hat{\mathbf{x}} \) de una planta a
partir de su entrada \( \mathbf{u} \) y su salida medida \( \mathbf{y} \), cuando no todos los
estados se miden. Permite cerrar realimentación de estado usando estimaciones.

## Fundamento teórico
Para \( \dot{\mathbf{x}}=A\mathbf{x}+B\mathbf{u} \), \( \mathbf{y}=C\mathbf{x} \), el observador
copia la planta y corrige con el error de salida:
$$ \dot{\hat{\mathbf{x}}}=A\hat{\mathbf{x}}+B\mathbf{u}+L\,(\mathbf{y}-C\hat{\mathbf{x}}) $$
El error \( \mathbf{e}=\mathbf{x}-\hat{\mathbf{x}} \) evoluciona como
$$ \dot{\mathbf{e}}=(A-LC)\,\mathbf{e} $$
así que **converge a cero** si \( A-LC \) es estable. Los autovalores de \( A-LC \) se sitúan
libremente mediante \( L \) **si y solo si el par \( (A,C) \) es observable** (problema dual de la
[[asignacion-polos-lqr|asignación de polos]]: \( L^\top \) se calcula como una realimentación sobre
\( (A^\top,C^\top) \)). El **principio de separación** garantiza que diseñar control (ganancia
\( K \)) y observador (ganancia \( L \)) por separado conserva los polos de ambos en el lazo
combinado. La versión **óptima** ante ruido es el filtro de Kalman (\( L \) de la ecuación de
Riccati). Existe el observador de **orden reducido** (estima solo los estados no medidos).

<div class="cfig"><img src="figuras/observador-estados-convergencia.png" alt="estado estimado convergiendo y error decayendo"><div class="cap">Izquierda: el observador arranca con $\hat x\neq x$ y su estimación del estado no medido $x_2$ alcanza a la real. Derecha: la norma del error $\|x-\hat x\|$ cae varios órdenes de magnitud porque los polos de $A-LC$ son estables y más rápidos que la planta.</div></div>

## Cuándo y por qué se usa
Cuando faltan sensores (estimar flujo, tensión de condensador, par de carga), para filtrar ruido,
o en control "sensorless". Imprescindible junto a realimentación de estado/LQR cuando el estado no
es accesible.

## Procedimiento de diseño (genérico)
1. Verifica observabilidad de \( (A,C) \) (ver [[controlabilidad-observabilidad]]).
2. Elige los polos del observador **2–5× más rápidos** que los de control (pero no tanto que
   amplifiquen ruido).
3. Calcula \( L \) por asignación de polos (dual) o resuelve Kalman si hay modelo de ruido.
4. Implementa el observador en discreto y comprueba convergencia y rechazo de ruido.
5. Cierra el lazo con \( \mathbf{u}=-K\hat{\mathbf{x}} \) (principio de separación).

## Ejemplo de aplicación real
**Problema:** Filtro LCL con estados \( [i_{L1},\,v_C,\,i_{L2}] \). Solo se mide \( i_{L2} \). Diseñar un observador de Luenberger que estime \( v_C \) e \( i_{L1} \) para implementar amortiguamiento activo sin sensor en el condensador.

El par \( (A,C) \) con \( C=[0,0,1] \) es observable (verificar \( \text{rank}(\mathcal{O})=3 \)). Se colocan los polos del observador a \( 3\times\omega_{res,LCL}\approx3\times2\pi\times2050\approx38\,700\,\text{rad/s} \) (3× más rápidos que la resonancia del filtro), dando convergencia del error de estimación en \( <3/(3\omega_{res})\approx75\,\mu\text{s} \). \( L \) se calcula con `ct.place(A.T, C.T, obs_poles).T`. El \( v_C \) estimado se usa en el lazo de amortiguamiento activo ([[amortiguamiento-activo-lcl]]): en simulación, el pico de resonancia del filtro a 2 kHz cae >20 dB respecto al caso sin observador.

## Ejemplo de código
```python
import control as ct, numpy as np
L = ct.place(A.T, C.T, obs_poles).T     # dualidad: polos del observador
# x_hat[k+1] = A@x_hat + B@u + L@(y - C@x_hat)   (discretizar A,B,L)
```

## Parámetros y valores típicos
Polos del observador 2–5× los del control. Compromiso clásico: rápido → converge antes pero
amplifica ruido de medida; lento → suave pero arrastra error.

## Errores comunes
- Observador más lento que la planta → estimación retrasada, lazo degradado.
- Polos demasiado rápidos → ruido de medida amplificado en \( \hat{\mathbf{x}} \).
- Diseñar con \( (A,C) \) no observable (o casi) → \( L \) no estabiliza ciertos modos.
- Modelo \( A,B,C \) mal identificado → sesgo permanente en la estimación.

## Conceptos relacionados
- [[controlabilidad-observabilidad]] · [[asignacion-polos-lqr]] · [[representacion-espacio-estados]] · [[variables-estado]]

## Referencias
- Ogata, *Ingeniería de Control Moderna*.
- Franklin, Powell, *Feedback Control of Dynamic Systems*.
