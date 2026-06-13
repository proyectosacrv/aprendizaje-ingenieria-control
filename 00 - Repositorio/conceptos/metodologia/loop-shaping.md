---
titulo: Loop-shaping (diseño en frecuencia)
slug: loop-shaping
categoria: metodologia
tipo: metodo
nivel: avanzado
proyectos: [01-GFM-Impedance]
objetivos: [disenar el controlador dando forma a la ganancia de lazo]
tags: [bode, ganancia-de-lazo, frecuencia, margen, diseno]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [metodos-sintesis-control, margenes-estabilidad, funciones-sensibilidad, sintonia-pi-pid]
referencias:
  - "Skogestad, Postlethwaite, Multivariable Feedback Control, Wiley 2005 (cap. 2-3)"
---

## Definición
Método de diseño que da forma a la **ganancia de lazo abierto** \( L(s)=C(s)G(s) \) en el dominio
de la frecuencia para cumplir las especificaciones, en vez de razonar sobre los polos cerrados.

## Fundamento teórico
Objetivos de forma de \( L(j\omega) \):
- **Baja frecuencia**: ganancia alta → buen seguimiento y rechazo (S pequeña).
- **Cruce \( \omega_c \)**: fija el ancho de banda; pendiente ≈ −20 dB/dec en el cruce para buen
  margen de fase.
- **Alta frecuencia**: ganancia baja → atenúa ruido y dinámica no modelada (T pequeña).
Compromiso fundamental (Bode): no se puede tener S y T pequeñas a la vez en la misma banda
(\( S+T=1 \)); ver [[funciones-sensibilidad]]. El margen de fase y \( M_s \) se leen directo de \( L \).

<div class="cfig"><img src="figuras/loop-shaping-ganancia.png" alt="forma deseada de la ganancia de lazo en frecuencia"><div class="cap">Forma objetivo de la ganancia de lazo $|L|$: alta a baja frecuencia (buen seguimiento y rechazo, $S$ pequeña), baja a alta frecuencia (atenúa ruido y dinámica no modelada, $T$ pequeña) y con pendiente $-20$ dB/dec en el cruce $f_c$ para un buen margen de fase. El diseño consiste en moldear esta curva con el controlador.</div></div>

## Cuándo y por qué se usa
Cuando se quiere control explícito del compromiso desempeño/robustez/ruido, o la planta tiene
resonancias/retardos que conviene modelar en frecuencia. Es el lenguaje natural del análisis de
impedancia.

## Procedimiento (genérico)
1. Traza \( G(j\omega) \) (Bode de la planta).
2. Diseña \( C(s) \) para situar el cruce en \( \omega_c \) con pendiente −20 dB/dec y margen de
   fase objetivo (añade ceros/polos, adelanto-retardo).
3. Comprueba S y T (sensibilidad/complementaria) y \( M_s \).
4. Itera hasta el compromiso deseado.

## Ejemplo de código
```python
import numpy as np
L = C(1j*w) * G(1j*w)                  # ganancia de lazo
wc = w[np.argmin(np.abs(np.abs(L)-1))] # cruce de ganancia
PM = 180 + np.degrees(np.angle(L[np.argmin(np.abs(np.abs(L)-1))]))  # margen de fase
```

## Parámetros y valores típicos
Margen de fase 45–60°, pendiente −20 dB/dec en el cruce, \( M_s<2 \).

## Errores comunes
- Cruce con pendiente −40 dB/dec → margen de fase pobre.
- Forzar S pequeña en banda donde T debe serlo (viola el compromiso de Bode).

## Uso en proyectos
- **01 (GFM)**: el diagnóstico del lazo de potencia se hizo en frecuencia (margen de fase −86°
  reveló la causa de la inestabilidad), lenguaje de loop-shaping.

## Conceptos relacionados
- [[metodos-sintesis-control]] · [[margenes-estabilidad]] · [[funciones-sensibilidad]]

## Referencias
- Skogestad, Postlethwaite, *Multivariable Feedback Control*, 2005.
