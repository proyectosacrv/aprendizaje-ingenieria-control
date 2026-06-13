---
titulo: Resonancia del filtro LCL
slug: resonancia-lcl
categoria: fisica-modelado
tipo: fenomeno
nivel: avanzado
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [entender y acotar el pico resonante que desestabiliza los lazos rapidos]
tags: [resonancia, LCL, damping, estabilidad, factor-Q, dq]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-06-10
relacionados: [filtro-lcl, amortiguamiento-activo-lcl, impedancia-salida-estabilidad, diagrama-bode]
referencias:
  - "Reznik et al., LCL Filter Design and Performance Analysis for Grid-Interconnected Systems, IEEE TIA 2014"
  - "Dannehl et al., Investigation of Active Damping Approaches for LCL Filters, IEEE TIA 2010"
  - "Wang, Blaabjerg, Harmonic Stability in Power-Electronic-Based Power Systems, IEEE TPEL 2014"
---

## Definición
El filtro LCL es una red \( L_1\!-\!C_f\!-\!L_2 \) de tercer orden, así que tiene un **par de
polos complejos con amortiguamiento casi nulo** (\( \zeta\approx 0 \)). A su frecuencia de
resonancia \( f_{res} \) la red presenta un **pico afilado** (impedancia serie muy baja / paralelo
muy alta) en el que una excitación pequeña genera corrientes oscilantes grandes. Es el precio de
ganar la caída de 60 dB/dec frente a un filtro L simple: ese tercer orden introduce la resonancia.

## Fundamento teórico
La frecuencia de resonancia (sin amortiguar) sale de poner las dos bobinas en paralelo con \( C_f \):

$$ \omega_{res}=\sqrt{\frac{L_1+L_2}{L_1 L_2 C_f}}\,,\qquad
   f_{res}=\frac{1}{2\pi}\sqrt{\frac{L_1+L_2}{L_1 L_2 C_f}} $$

**De qué variable depende.** Con red rígida (\( v_g\!=\!0 \) en pequeña señal) y \( R\approx 0 \),
la corriente de **lado red** \( i_2 \) frente a la tensión del puente \( v_i \) es:

$$ \frac{i_2(s)}{v_i(s)}=\frac{1}{s\,L_1 L_2 C_f\,(s^2+\omega_{res}^2)} $$

con polos en \( s=0 \) y \( s=\pm j\omega_{res} \): el par resonante **no tiene parte real**, de ahí
\( \zeta\approx 0 \). En cambio la corriente de **lado inversor** \( i_1 \) añade un cero:

$$ \frac{i_1(s)}{v_i(s)}=\frac{1+s^2 L_2 C_f}{s\,L_1 L_2 C_f\,(s^2+\omega_{res}^2)}\,,\qquad
   f_{ar}=\frac{1}{2\pi\sqrt{L_2 C_f}} $$

Ese cero (**anti-resonancia** \( f_{ar} \)) aporta \( +180^\circ \) de fase antes del pico, lo que
hace que **realimentar \( i_1 \) sea mucho más fácil de estabilizar que realimentar \( i_2 \)**.

**Factor de calidad.** Con una resistencia de amortiguamiento \( R_d \) en serie con \( C_f \), el par
pasa a \( \zeta=\tfrac{1}{2}R_d\sqrt{C_f(L_1+L_2)/(L_1 L_2)} \): a mayor \( R_d \), más amortiguado
(pero más pérdidas y peor atenuación a \( f_{sw} \)).

**En marco dq.** Al pasar al marco giratorio (a \( \omega_0 \)) el par resonante aparece como dos
modos propios cerca de \( \pm f_{res} \); en el proyecto se ven como autovalores a \( \approx 1.1 \)
kHz con \( \zeta\approx 0.13 \) (ya con amortiguamiento activo).

<div class="cfig"><img src="figuras/resonancia-lcl-bode.png" alt="bode de i2/vi y i1/vi mostrando resonancia y antiresonancia"><div class="cap">La corriente de lado red $i_2/v_i$ presenta un pico de resonancia afilado ($\zeta\approx0$) en $f_{res}$. La de lado inversor $i_1/v_i$ añade un cero de antiresonancia en $f_{ar}$ que aporta $+180°$ de fase antes del pico; por eso realimentar $i_1$ es mucho más fácil de estabilizar que $i_2$. En red débil, $L_g$ se suma a $L_2$ y baja $f_{res}$ hacia la banda de control.</div></div>

## Cuándo y por qué se usa
Aparece en **todo convertidor con filtro LCL/LC** en cuanto un lazo rápido (corriente, tensión) o la
propia impedancia de red excita la zona de \( f_{res} \). Es crítico en **red débil**: la inductancia
de red \( L_g \) se suma a \( L_2 \), **baja \( f_{res} \)** y la mete dentro del ancho de banda de
control. Es uno de los mecanismos típicos de inestabilidad armónica / oscilaciones de alta frecuencia.

## Procedimiento de diseño (genérico)
Cómo acotar/gestionar la resonancia en cualquier diseño:
1. **Calcula \( f_{res} \)** y colócala holgada: \( 10\,f_0 < f_{res} < f_{sw}/2 \).
2. **Compara con el cruce del lazo** \( f_c \): deja margen \( f_c \lesssim f_{res}/3 \ldots f_{res}/5 \)
   si no amortiguas.
3. **Elige variable de realimentación**: \( i_1 \) (con su cero de anti-resonancia) da más margen que
   \( i_2 \).
4. **Añade amortiguamiento**: pasivo (\( R_d\approx 1/(3\,\omega_{res} C_f) \), simple pero disipa) o
   **activo** por software (realimentar \( i_{C_f} \) / resistor virtual) — ver
   [[amortiguamiento-activo-lcl]].
5. **Caso peor en red débil**: recalcula \( f_{res} \) con \( L_2+L_{g,\max} \) (mínimo SCR) y verifica
   que el par resonante mantiene \( \zeta\gtrsim 0.1\text{–}0.3 \) por autovalores o Bode.

## Ejemplo de código
```python
import numpy as np
from control import tf

L1, L2, Cf = 2e-3, 1e-3, 20e-6
w_res = np.sqrt((L1 + L2) / (L1 * L2 * Cf))       # rad/s
f_res = w_res / (2 * np.pi)                        # ~1.1 kHz
f_ar  = 1 / (2 * np.pi * np.sqrt(L2 * Cf))         # anti-resonancia (i1)
Rd    = 1 / (3 * w_res * Cf)                        # resistor de amortiguamiento pasivo

# i2/vi sin amortiguar: den = s^3 L1L2Cf + s(L1+L2)  -> pico (Q -> inf) en f_res
G_i2 = tf([1], [L1 * L2 * Cf, 0, (L1 + L2), 0])
```

## Parámetros y valores típicos
- Banda recomendada: \( 10\,f_0 < f_{res} < f_{sw}/2 \).
- Amortiguamiento objetivo del par resonante: \( \zeta \in [0.1,\,0.3] \).
- Resistor pasivo: \( R_d\approx 1/(3\,\omega_{res} C_f) \) (unos pocos ohmios).
- Proyecto (10 kVA / 400 V, \( L_1=2 \) mH, \( C_f=20\,\mu\text{F} \), \( L_2=1 \) mH, \( f_{sw}=10 \)
  kHz): \( f_{res}\approx 1.38 \) kHz (LCL aislado), \( f_{ar}\approx 1.13 \) kHz. En el **modelo dq
  completo** del proyecto, con la inductancia de red, el modo resonante baja a \( \approx 1.1 \) kHz con
  \( \zeta\approx 0.13 \) (ya amortiguado).

## Errores comunes
- **Realimentar \( i_2 \)** (lado red) directamente: sin el cero de anti-resonancia el margen de fase
  se desploma al acercarse a \( f_{res} \). Preferir \( i_1 \) o amortiguar.
- **Ignorar \( L_g \)**: en red débil \( f_{res} \) baja y entra en la banda del control → resonancia
  excitada.
- **Sobre-amortiguar** con \( R_d \) grande: añade pérdidas y degrada la atenuación a \( f_{sw} \).
- Confundir resonancia (serie, vista en \( i_2 \)) con anti-resonancia (paralelo, cero en \( i_1 \)).

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: modelar la planta): el par resonante a 1.1 kHz con \( \zeta\approx
  0.13 \) limitaba el ancho de banda del lazo de tensión; se resolvió con amortiguamiento activo. El
  LCL aporta 6 de los 15 estados del modelo.
- **02 - GFL-Impedance** (objetivo: estabilidad en red débil): el mismo LCL obliga a mantener el lazo
  de corriente / PLL por debajo de \( f_{res} \), que además baja al debilitarse la red.

## Conceptos relacionados
- [[filtro-lcl]] · [[amortiguamiento-activo-lcl]] · [[impedancia-salida-estabilidad]] · [[diagrama-bode]]

## Referencias
- Reznik et al., *LCL Filter Design...*, IEEE TIA 2014.
- Dannehl et al., *Investigation of Active Damping Approaches for LCL Filters*, IEEE TIA 2010.
- Wang, Blaabjerg, *Harmonic Stability in Power-Electronic-Based Power Systems*, IEEE TPEL 2014.
