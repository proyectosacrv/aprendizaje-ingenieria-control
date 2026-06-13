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
fecha_actualizacion: 2026-06-08
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
