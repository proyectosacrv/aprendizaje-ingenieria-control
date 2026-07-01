---
titulo: Funciones de sensibilidad (S y T)
slug: funciones-sensibilidad
categoria: metodologia
tipo: concepto
nivel: avanzado
proyectos: [01-GFM-Impedance]
objetivos: [evaluar rechazo de perturbacion, ruido y robustez]
tags: [sensibilidad, S, T, rechazo, ruido, compromiso-bode]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-30
relacionados: [margenes-estabilidad, loop-shaping, metricas-desempeno, control-robusto-hinf]
referencias:
  - "Skogestad, Postlethwaite, Multivariable Feedback Control, Wiley 2005"
---

## Definición
Las funciones que describen cómo el lazo cerrado responde a referencia, perturbación y ruido. La
**sensibilidad** \( S \) y la **complementaria** \( T \) resumen casi todo el desempeño y la
robustez en un solo par de curvas.

## Fundamento teórico
Con ganancia de lazo \( L=CG \):
$$ S=\frac{1}{1+L}, \qquad T=\frac{L}{1+L}, \qquad S+T=1 $$
- \( S \): de la perturbación de salida y de la referencia al error. Pequeña \( S \) (baja
  frecuencia) → buen rechazo y seguimiento.
- \( T \): de la referencia a la salida y del **ruido** de medida a la salida. Pequeña \( T \)
  (alta frecuencia) → atenúa ruido y dinámica no modelada.
- **Compromiso de Bode**: como \( S+T=1 \), no pueden ser ambas pequeñas en la misma banda;
  además \( \int \ln|S|\,d\omega = 0 \) (área de "waterbed"): reducir \( S \) en una banda la
  aumenta en otra. \( M_s=\max|S| \) es el [[margenes-estabilidad|margen de módulo]].

<div class="cfig"><img src="figuras/funciones-sensibilidad-st.png" alt="funciones de sensibilidad S y T frente a la frecuencia"><div class="cap">$S$ pequeña a baja frecuencia da buen rechazo y seguimiento; $T$ pequeña a alta frecuencia atenúa el ruido de medida. Como $S+T=1$ no pueden ser ambas pequeñas en la misma banda (compromiso de Bode): el pico $M_s=\max|S|$ resume la robustez (objetivo $<2$).</div></div>

## 1 — Por qué \( S+T=1 \) (y por qué no se pueden bajar ambas)
**Paso 1 — definir las dos.** Con lazo de realimentación negativa y ganancia de lazo \( L=CG \), la sensibilidad y la complementaria son
$$ S=\frac{1}{1+L},\qquad T=\frac{L}{1+L} $$
\( S \) va de la perturbación/referencia al error; \( T \) va de la referencia (o del ruido de medida) a la salida.

**Paso 2 — sumarlas.** Con el mismo denominador \( 1+L \):
$$ S+T=\frac{1}{1+L}+\frac{L}{1+L}=\frac{1+L}{1+L}=\boxed{1}\quad\forall\,\omega $$
Es una **identidad algebraica**, no un objetivo de diseño: se cumple a toda frecuencia, en todo lazo de un grado de libertad.

**Paso 3 — la consecuencia.** Como \( S(j\omega)+T(j\omega)=1 \) para cada \( \omega \), por la desigualdad triangular \( 1=|S+T|\le|S|+|T| \): es imposible que \( |S| \) y \( |T| \) sean ambas pequeñas en la misma frecuencia. Si \( |S|\ll1 \) (buen rechazo) entonces \( T\approx1 \) (pasa el ruido); si \( |T|\ll1 \) (atenúa ruido) entonces \( S\approx1 \) (no rechaza). De ahí el reparto natural: \( S \) pequeña en **baja** frecuencia (rechazo/seguimiento) y \( T \) pequeña en **alta** (ruido).

**Paso 4 — número.** Si en una banda \( |L|=100 \) (40 dB), entonces \( |S|\approx1/100=0.01 \) (rechazo de −40 dB) y \( |T|\approx1 \) (0 dB): el control rechaza bien y, a la vez, sigue la referencia casi sin error. Donde \( |L|=1 \) (cruce), \( |S| \) y \( |T| \) valen \( \sim1/\sqrt2 \) cada una y su suma sigue siendo 1.

## 2 — La integral de Bode (efecto "waterbed")
**Paso 1 — el resultado.** Para un lazo \( L \) estable, estrictamente propio (cae al menos como \( 1/s^2 \) en alta) y de fase mínima, la sensibilidad cumple la integral de Bode:
$$ \boxed{\;\int_0^\infty \ln|S(j\omega)|\,d\omega=0\;} $$
(con polos inestables \( p_k \) en \( L \) el cero pasa a \( \pi\sum\mathrm{Re}(p_k)>0 \), aún peor).

**Paso 2 — interpretación de áreas.** El integrando \( \ln|S| \) es **negativo** donde \( |S|<1 \) (frecuencias donde el lazo rechaza, baja f) y **positivo** donde \( |S|>1 \) (donde amplifica). Que la integral total sea cero obliga a que el **área de atenuación** (\( \ln|S|<0 \)) y el **área de amplificación** (\( \ln|S|>0 \)) se compensen exactamente.

**Paso 3 — el "waterbed".** Empujar \( |S| \) hacia abajo en una banda (más rechazo) sube necesariamente \( |S| \) en otra: como apretar un colchón de agua. No se gana rechazo gratis; se traslada. Por eso siempre aparece un pico \( M_s=\max_\omega|S|>1 \) algo por encima del cruce.

**Paso 4 — el coste concreto.** Si se exige \( |S|\le\varepsilon \) (muy pequeño) en una banda de ancho \( \Delta\omega_1 \), el área negativa \( \approx\Delta\omega_1\ln\varepsilon \) debe devolverse como área positiva. Repartida en una banda \( \Delta\omega_2 \), fuerza un pico aproximado
$$ \ln M_s\;\gtrsim\;\frac{\Delta\omega_1}{\Delta\omega_2}\,\ln\frac1\varepsilon $$
cuanto más rechazo (\( \varepsilon\downarrow \)) o más estrecha la banda de recuperación, mayor el pico \( M_s \) — y peor el [[margenes-estabilidad|margen de módulo]] \( 1/M_s \). El compromiso \( S \)/\( T \) es, en el fondo, este reparto de área.

## Cuándo y por qué se usa
Para evaluar de un vistazo rechazo (S), atenuación de ruido (T) y robustez (\( M_s \)), y para
diseñar por [[loop-shaping]] o \(H_\infty\) (los pesos dan forma a S y T).

## Procedimiento (genérico)
1. Calcula \( L(j\omega) \), luego \( S \) y \( T \).
2. Verifica: \( |S| \) pequeña en baja frecuencia (rechazo), \( |T| \) pequeña en alta (ruido).
3. Lee \( M_s=\max|S| \) (objetivo < 2) y el ancho de banda (donde \( |T|=-3 \) dB).
4. Si el compromiso no cumple, reubica el cruce o cambia de método.

## Ejemplo de código
```python
S = 1/(1+L);  T = L/(1+L)
Ms = np.max(np.abs(S(1j*w)));  BW = w[np.argmin(np.abs(np.abs(T(1j*w))-1/np.sqrt(2)))]
```

## Parámetros y valores típicos
\( M_s<2 \) (6 dB). Ancho de banda de \( T \) ≈ \( \omega_c \). \( |T| \) cae en alta frecuencia.

## Errores comunes
- Intentar S y T pequeñas a la vez en la misma banda (imposible, \( S+T=1 \)).
- Subir ganancia para mejorar rechazo sin mirar el pico de \( S \) (empeora robustez).

## Uso en proyectos
- **01 (GFM)**: el comportamiento de la impedancia de salida y el pico del modo de potencia se
  interpretan como sensibilidad; el buen \( \zeta \) evita un pico de \( S \) alto.

## Conceptos relacionados
- [[margenes-estabilidad]] · [[loop-shaping]] · [[metricas-desempeno]] · [[control-robusto-hinf]]

## Referencias
- Skogestad, Postlethwaite, *Multivariable Feedback Control*, 2005.
