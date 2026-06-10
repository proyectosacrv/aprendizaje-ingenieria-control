---
titulo: Filtro LCL
slug: filtro-lcl
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [atenuar armonicos de conmutacion, modelar la planta de potencia]
tags: [filtro, resonancia, convertidor, LCL, dq]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [amortiguamiento-activo-lcl, marco-dq, modelo-promediado]
referencias:
  - "Reznik et al., LCL Filter Design and Performance Analysis for Grid-Interconnected Systems, IEEE TIA 2014"
---

## Definición
Filtro de tercer orden (\( L_1 \)–\( C_f \)–\( L_2 \)) entre el puente del inversor y la red.
Atenúa los armónicos de conmutación con mejor relación tamaño/atenuación que un filtro L
simple (caída de 60 dB/década por encima de la resonancia).

## Fundamento teórico
La frecuencia de resonancia (sin amortiguar) es:

$$ f_{res} = \frac{1}{2\pi}\sqrt{\frac{L_1+L_2}{L_1 L_2 C_f}} $$

Por encima de \( f_{res} \) atenúa a 60 dB/dec. El problema: a \( f_{res} \) la impedancia se
hace muy pequeña (o muy grande según el punto) con **amortiguamiento casi nulo** (\( \zeta\approx0 \)),
lo que puede inestabilizar cualquier lazo rápido que la excite. Modelo en dq (marco a \( \omega \)),
con \( \mathbf{J}=\left[\begin{smallmatrix}0&-1\\1&0\end{smallmatrix}\right] \):

$$ L_1\dot{\mathbf{i}}_{L1}=\mathbf{v}_i-\mathbf{v}_C-R_1\mathbf{i}_{L1}+\omega L_1\mathbf{J}\mathbf{i}_{L1} $$
$$ C_f\dot{\mathbf{v}}_C=\mathbf{i}_{L1}-\mathbf{i}_{L2}+\omega C_f\mathbf{J}\mathbf{v}_C $$
$$ L_2\dot{\mathbf{i}}_{L2}=\mathbf{v}_C-\mathbf{v}_{pcc}-R_2\mathbf{i}_{L2}+\omega L_2\mathbf{J}\mathbf{i}_{L2} $$

## Cuándo y por qué se usa
Estándar en inversores conectados a red (PV, eólica, baterías) por la normativa de inyección
de armónicos. Se prefiere a un filtro L cuando se quiere menos inductancia total / menor caída.

## Procedimiento de diseño (genérico)
1. **\( L_1 \) (lado inversor)** por el rizado de corriente admisible:
   \( L_1 = \dfrac{V_{dc}}{8\,f_{sw}\,\Delta i_{L,pp}} \) (típico \( \Delta i \) = 10–20% de \( I_n \)).
2. **\( C_f \)** por la reactiva absorbida (≤ 5% de la potencia base):
   \( C_f \le 0.05\,\dfrac{S_n}{\omega_0 V^2} \).
3. **\( L_2 \)** para fijar la atenuación a \( f_{sw} \) (relación \( L_2/L_1 \) = 0.2–1).
4. **Coloca \( f_{res} \)** holgada: \( 10 f_0 < f_{res} < f_{sw}/2 \).
5. **Añade amortiguamiento** (pasivo con \( R \) en serie con \( C_f \), o **activo** por
   software — ver [[amortiguamiento-activo-lcl]]).

## Ejemplo de código
```python
import numpy as np
L1, L2, Cf = 2e-3, 1e-3, 20e-6
f_res = 1/(2*np.pi)*np.sqrt((L1+L2)/(L1*L2*Cf))   # ~1.1 kHz
```

## Parámetros y valores típicos
Para 10 kVA / 400 V / 50 Hz (proyecto): \( L_1=2\,\text{mH} \), \( C_f=20\,\mu\text{F} \),
\( L_2=1\,\text{mH} \) → \( f_{res}\approx 1.1\,\text{kHz} \), con \( f_{sw}=10\,\text{kHz} \).

## Errores comunes
- Dejar \( f_{res} \) demasiado cerca del ancho de banda de control → resonancia excitada.
- Olvidar el amortiguamiento → polos de resonancia con \( \zeta\approx 0 \) (en el proyecto
  apareció a 1.1 kHz con \( \zeta\approx 0.13 \)).

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: modelar la planta): el LCL son 6 de los 15 estados del
  modelo. Su resonancia (1.1 kHz) obligó a añadir amortiguamiento activo para poder subir el
  lazo de tensión.

## Conceptos relacionados
- [[amortiguamiento-activo-lcl]] · [[marco-dq]] · [[modelo-promediado]]

## Referencias
- Reznik et al., *LCL Filter Design...*, IEEE TIA 2014.
