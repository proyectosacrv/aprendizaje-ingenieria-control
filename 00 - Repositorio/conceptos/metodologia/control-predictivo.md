---
titulo: Control predictivo (MPC / FCS-MPC)
slug: control-predictivo
categoria: metodologia
tipo: metodo
nivel: avanzado
proyectos: []
objetivos: [controlar con restricciones explicitas optimizando un horizonte]
tags: [MPC, FCS-MPC, predictivo, restricciones, horizonte, panorama]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [metodos-sintesis-control, asignacion-polos-lqr, current-limiting]
referencias:
  - "Rodriguez, Cortes, Predictive Control of Power Converters and Drives, Wiley 2012"
---

## Definición
Control que, en cada instante, **predice** el comportamiento futuro con el modelo y **optimiza**
una acción minimizando un coste sobre un horizonte, respetando **restricciones explícitas**
(corriente máxima, tensión de bus). En convertidores destaca el **FCS-MPC** (Finite Control Set),
que evalúa directamente los estados de conmutación posibles.

## Fundamento teórico
- **MPC** (continuo/lineal): minimiza \( J=\sum (\hat{y}-y_{ref})^2 + \lambda\,\Delta u^2 \) sobre
  un horizonte, sujeto a restricciones; aplica solo el primer paso (horizonte deslizante).
- **FCS-MPC**: el convertidor tiene un número **finito** de estados de conmutación; se predice la
  respuesta de cada uno con el modelo discreto y se elige el de menor coste. Sin modulador (PWM)
  → frecuencia de conmutación variable.
- Maneja de forma natural el [[current-limiting]] (la restricción va en el coste).

<div class="cfig"><img src="figuras/control-predictivo-horizonte.png" alt="horizonte deslizante del control predictivo"><div class="cap">En cada paso el MPC usa el modelo para predecir la salida sobre un horizonte y optimiza la secuencia de control que minimiza el coste respetando las restricciones (corriente, tensión); aplica solo el primer movimiento $u[0]$ y repite (horizonte deslizante). El FCS-MPC enumera directamente los estados de conmutación del convertidor.</div></div>

## 1 — La función de coste MPC y la ley explícita para horizonte 1
**Paso 1 — planteamiento con horizonte 1.** El sistema es SISO con predicción \( \hat{y}[k+1]=g\cdot u[k] \) (modelo de ganancia estática \( g \)) y la acción de control se incrementa en \( \Delta u \) desde el valor actual \( u_0 \). La función de coste sobre un horizonte de predicción \( N=1 \) es:

$$ J = \bigl(\hat{y}[k+1]-r\bigr)^2 + \lambda\,(\Delta u)^2 $$

donde \( r \) es la referencia y \( \lambda>0 \) penaliza el esfuerzo de control.

**Paso 2 — condición de optimalidad.** Se minimiza \( J \) respecto a \( \Delta u \). Sustituyendo \( \hat{y}=g\,(u_0+\Delta u) \):

$$ J=\bigl(g\,u_0+g\,\Delta u-r\bigr)^2+\lambda(\Delta u)^2 $$

Derivando e igualando a cero:

$$ \frac{\partial J}{\partial(\Delta u)}=2g\,\bigl(g\,u_0+g\,\Delta u-r\bigr)+2\lambda\,\Delta u=0 $$

$$ (g^2+\lambda)\,\Delta u = g\,(r-g\,u_0)=g\,(r-y) $$

**Paso 3 — ley de control explícita.** Despejando \( \Delta u \):

$$ \boxed{\Delta u = \underbrace{\frac{g}{g^2+\lambda}}_{K}\,(r-y)} $$

Es una realimentación proporcional del error \( e=r-y \) con ganancia \( K=g/(g^2+\lambda) \). Para \( \lambda\to0 \) (sin penalización de esfuerzo), \( K\to 1/g \) (inversión de la planta, respuesta en un paso). Para \( \lambda\to\infty \), \( K\to0 \) (no actuar). La sintonía de \( \lambda \) es la del MPC: compromiso velocidad–esfuerzo de control.

**Paso 4 — generalización.** Con horizonte \( N>1 \) el resultado es \( \Delta\mathbf{u}=-(\mathbf{G}^T\mathbf{G}+\lambda I)^{-1}\mathbf{G}^T(\mathbf{y}-\mathbf{r}) \), donde \( \mathbf{G} \) es la matriz de respuesta al impulso truncada. Solo se aplica el primer elemento \( \Delta u[0] \) (horizonte deslizante) y el resto se descarta. Las restricciones convierten este mínimo en un **QP** en cada instante.

## 2 — FCS-MPC: por qué el conjunto finito elimina el QP
**Paso 1 — estados de conmutación.** En un convertidor de dos niveles trifásico hay \( 2^3=8 \) vectores de tensión posibles (estados de conmutación \( \mathbf{s}\in\{000,\ldots,111\} \)). El FCS-MPC no parametriza \( \Delta u \) de forma continua; directamente **enumera** los 8 vectores.

**Paso 2 — predicción y elección.** Para cada vector \( \mathbf{s}_k \) se predice la corriente en el siguiente paso con el modelo discreto del filtro LCL (o RL):

$$ \hat{\mathbf{i}}[k+1|\mathbf{s}] = \mathbf{A}_d\,\mathbf{i}[k] + \mathbf{B}_d\,\mathbf{v}(\mathbf{s}) $$

Se evalúa \( J(\mathbf{s})=\|\hat{\mathbf{i}}-\mathbf{i}_{ref}\|^2 \) y se aplica el \( \mathbf{s}^* \) de menor coste. El QP se sustituye por una **comparación de 8 escalares**, resoluble en microsegundos en un DSP/FPGA.

$$ \boxed{\mathbf{s}^*=\arg\min_{\mathbf{s}\in\{0,1\}^3} J(\mathbf{s})} $$

## Cuándo y por qué se usa
Cuando hay **restricciones duras** (corriente, tensión) que deben respetarse, sistemas MIMO con
acoplamiento, o no linealidades. Muy usado en accionamientos y convertidores modernos.

## Procedimiento (genérico)
1. Modelo discreto de predicción \( x[k+1]=f(x[k],u[k]) \).
2. Define la función de coste (error de seguimiento + esfuerzo + penalización de restricciones).
3. FCS-MPC: enumera los estados de conmutación, predice y elige el de menor coste.
4. MPC con restricciones: resuelve la optimización (QP) en cada paso.
5. Evalúa coste computacional, frecuencia de conmutación (FCS) y robustez ante error de modelo.

## Errores comunes
- FCS-MPC con espectro de conmutación disperso (frecuencia variable) → problemas de filtrado/EMI.
- Sensibilidad al error de modelo (es model-based): la robustez no es automática.

## Uso en proyectos
- Candidato a proyecto propio (FCS-MPC sobre convertidor conectado a red o accionamiento). Ficha
  de panorama por ahora.

## Conceptos relacionados
- [[metodos-sintesis-control]] · [[asignacion-polos-lqr]] · [[current-limiting]]

## Referencias
- Rodriguez, Cortes, *Predictive Control of Power Converters and Drives*, 2012.
