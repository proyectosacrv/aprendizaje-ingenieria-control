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
fecha_actualizacion: 2026-06-08
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
