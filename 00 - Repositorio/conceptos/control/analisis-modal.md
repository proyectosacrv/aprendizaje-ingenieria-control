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
fecha_actualizacion: 2026-06-30
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

<div class="cfig"><img src="figuras/analisis-modal-polos.png" alt="mapa de autovalores en el plano s"><div class="cap">Mapa de autovalores: cuanto más a la izquierda (σ más negativo), más amortiguado; la parte imaginaria da la frecuencia. El modo que preocupa es el cercano al eje con poco ζ (aquí, la resonancia LCL a 1.1 kHz).</div></div>

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

Es la herramienta que en **01 - GFM-Impedance** señaló \( P_m,Q_m \) (lazo de potencia) como dominantes del modo inestable. Conecta con [[estabilidad-bibo]] (la estabilidad la fija \( \max_i\mathrm{Re}(\lambda_i) \)).

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
