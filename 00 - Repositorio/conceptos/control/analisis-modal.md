---
titulo: Análisis modal (autovalores, participación, amortiguamiento)
slug: analisis-modal
categoria: control
tipo: metodo
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance, 03-DataCenter-IA]
objetivos: [evaluar estabilidad e identificar el origen de cada modo]
tags: [autovalores, polos, participacion, zeta, estabilidad]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [linealizacion-numerica, droop-control, impedancia-salida-estabilidad]
referencias:
  - "Kundur, Power System Stability and Control, McGraw-Hill 1994 (cap. 12)"
---

## Definición
Estudio de la estabilidad de un sistema lineal a partir de los **autovalores** de \( A \)
(modos), su **amortiguamiento** \( \zeta \) y **frecuencia**, y los **factores de participación**
que indican qué estados forman cada modo.

## Fundamento teórico
Para un autovalor \( \lambda=\sigma\pm j\omega_d \):
$$ f=\frac{|\omega_d|}{2\pi}, \qquad \zeta=\frac{-\sigma}{|\lambda|} $$
Estable si \( \sigma<0 \) para todos los modos. El **factor de participación** del estado \( k \)
en el modo \( i \) combina los autovectores derecho \( \phi \) e izquierdo \( \psi \):
\( p_{ki}=|\psi_{ik}\,\phi_{ki}| \). Identifica qué dinámica domina cada modo → guía el rediseño.

## Cuándo y por qué se usa
Para saber no solo **si** es estable, sino **qué** modo es problemático y **qué estados** lo
generan: clave para diagnosticar y corregir (¿es el lazo de potencia? ¿la resonancia LCL?).

## Procedimiento de diseño (genérico)
1. Linealiza para obtener \( A \) (ver [[linealizacion-numerica]]).
2. `eig(A)` → autovalores y autovectores.
3. Para cada modo de interés calcula \( f,\zeta \) y los factores de participación.
4. Si un modo está mal amortiguado/inestable, mira qué estados participan y actúa sobre esa
   parte (ganancia, filtro, impedancia virtual...).
5. Criterio práctico de aceptación: \( \zeta>0.1 \) (idealmente >0.3) en modos de control.

## Ejemplo de código
```python
import numpy as np
w, V = np.linalg.eig(A)                 # autovalores y autovectores derechos
i = np.argmax(w.real)                   # modo menos estable
f = abs(w[i].imag)/(2*np.pi); zeta = -w[i].real/abs(w[i])
part = np.abs(V[:, i]); part /= part.max()   # participacion aproximada
```

## Parámetros y valores típicos
\( \zeta \) objetivo: >0.1 aceptable, >0.3 bueno. Modos electromecánicos lentos (1–10 Hz),
resonancias de filtro (cientos de Hz–kHz).

## Errores comunes
- Mirar solo \( \max\text{Re} \) sin el amortiguamiento: un sistema "estable" puede tener un
  modo con \( \zeta \) pésimo.
- Ignorar los factores de participación → se ajusta a ciegas.

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: diagnóstico): los factores de participación revelaron que
  el modo inestable inicial estaba dominado por \( P_m,Q_m \) (lazo de potencia), lo que orientó
  todo el rediseño. Modo final de potencia: 3.3 Hz, \( \zeta=0.40 \).

## Conceptos relacionados
- [[linealizacion-numerica]] · [[droop-control]] · [[impedancia-salida-estabilidad]]

## Referencias
- Kundur, *Power System Stability and Control*, 1994.
