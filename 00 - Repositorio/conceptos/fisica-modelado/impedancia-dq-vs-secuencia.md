---
titulo: Impedancia en dq vs en secuencia
slug: impedancia-dq-vs-secuencia
categoria: fisica-modelado
tipo: concepto
nivel: avanzado
proyectos: []
objetivos: [elegir y relacionar los dos formalismos de modelado de impedancia de convertidor]
tags: [impedancia, dq, secuencia, mirror-frequency, acoplamiento, avanzado, modelado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-09
relacionados: [impedancia-salida-estabilidad, marco-dq, componentes-simetricas, nyquist-generalizado, medicion-impedancia-inyeccion]
referencias:
  - "Wang, Blaabjerg, Harmonic Stability in Power-Electronic-Based Power Systems, IEEE TPEL 2014"
  - "Rygg et al., A Modified Sequence-Domain Impedance Definition, IEEE JESTPE 2016"
  - "Sun, Impedance-Based Stability Criterion for Grid-Connected Inverters, IEEE TPEL 2011"
---

## Definición
Dos representaciones equivalentes de la **impedancia de pequeña señal** de un convertidor: la
**dq** (matriz \( 2\times2 \) en marco síncrono giratorio) y la **de secuencia** (impedancias
\( Z_+,Z_- \) en marco estacionario, definidas por inyección de secuencia positiva/negativa). Ambas
alimentan el [[nyquist-generalizado|criterio de estabilidad por impedancia]].

## Fundamento teórico
**Marco dq.** Se linealiza el convertidor en el marco síncrono y se obtiene
$$ \begin{bmatrix}\Delta v_d\\\Delta v_q\end{bmatrix}=
   \begin{bmatrix}Z_{dd}&Z_{dq}\\Z_{qd}&Z_{qq}\end{bmatrix}
   \begin{bmatrix}\Delta i_d\\\Delta i_q\end{bmatrix} $$
Los términos cruzados \( Z_{dq},Z_{qd} \) capturan el acoplamiento (PLL, lazo de potencia,
[[marco-dq|términos \( \pm\omega \)]]). Es el marco natural cuando el control vive en dq (GFL con
PLL, GFM con droop/VSM).

**Marco de secuencia.** Inyectando una pequeña tensión de secuencia positiva a frecuencia \( f_p \),
el convertidor responde a \( f_p \) **y** a la **frecuencia espejo** \( f_p-2f_1 \) (mirror
frequency coupling), por la asimetría que introducen PLL/control. Esto obliga a una definición
\( 2\times2 \) (impedancia de secuencia **modificada**):
$$ \begin{bmatrix}\Delta V_p\\\Delta V_m^*\end{bmatrix}=
   \begin{bmatrix}Z_{pp}&Z_{pm}\\Z_{mp}&Z_{mm}\end{bmatrix}
   \begin{bmatrix}\Delta I_p\\\Delta I_m^*\end{bmatrix} $$
con \( f_m=f_p-2f_1 \). Si el acoplamiento es débil, se reduce a dos escalares \( Z_+,Z_- \)
desacoplados.

**Equivalencia.** Hay una transformación lineal exacta entre ambas (un cambio de variable complejo
\( s_{dq}\leftrightarrow s\mp j\omega_1 \)): el acoplamiento d-q en dq ⇔ acoplamiento de frecuencia
espejo en secuencia. No son fenómenos distintos, son **el mismo** visto en dos marcos.

| Aspecto | dq | Secuencia |
|---|---|---|
| Marco | giratorio | estacionario |
| Variable | \( Z_{dd},Z_{qq},Z_{dq},Z_{qd} \) | \( Z_{pp},Z_{mm},Z_{pm},Z_{mp} \) |
| Medida | inyección en dq (necesita ángulo) | inyección de secuencia (frecuencia real) |
| Intuición | acoplamiento de control | resonancia/espejo físico |

<div class="cfig"><img src="figuras/impedancia-dq-vs-secuencia-espejo.png" alt="acoplamiento de frecuencia espejo entre dq y secuencia"><div class="cap">Al inyectar una perturbación de secuencia a frecuencia $f_p$, la asimetría que introducen PLL/control hace que el convertidor responda también a la frecuencia espejo $f_p-2f_1$. Ese acoplamiento de frecuencia espejo en el marco de secuencia es exactamente el mismo fenómeno que el acoplamiento d-q en el marco dq, relacionados por $s_{dq}=s\mp j\omega_1$.</div></div>

## Cuándo y por qué se usa
**dq** cuando el modelo analítico del control está en dq (tus proyectos GFM/GFL) y para casar con
el [[nyquist-generalizado|GNC]]. **Secuencia** cuando mides experimentalmente con inyección de
frecuencia real, o para razonar sobre resonancias y armónicos de red ([[estabilidad-armonica]]).

## Procedimiento de diseño (genérico)
1. Define el punto de operación y linealiza ([[linealizacion-numerica]]).
2. Elige marco: dq (analítico) o secuencia (experimental/físico).
3. Obtén la matriz \( 2\times2 \) por columnas (dos inyecciones independientes).
4. Si necesitas el otro marco, aplica la transformación \( s\mp j\omega_1 \).
5. Lleva la impedancia al criterio de estabilidad ([[nyquist-generalizado]]).

## Ejemplo de código
```python
# Conversión conceptual dq -> secuencia (par de frecuencias espejo)
# Z_seq(f_p) se arma con Z_dq evaluada en s = j2*pi*(f_p - f1)
import numpy as np
def dq_to_seq_freq(fp, f1):
    return 2*np.pi*(fp - f1)        # desplazamiento de frecuencia del marco
```

## Parámetros y valores típicos
Acoplamiento d-q (o espejo) relevante cuando la PLL/lazo de potencia es de banda ancha o la red es
débil (bajo [[red-thevenin-scr|SCR]]); entonces los términos cruzados no se pueden despreciar.

## Errores comunes
- Usar impedancia **escalar** (SISO) cuando hay acoplamiento fuerte → estabilidad mal evaluada.
- Ignorar la **frecuencia espejo** al medir en secuencia (subestima el acoplamiento).
- Mezclar convenciones de marco/ángulo entre la impedancia de fuente y la de carga.

## Conceptos relacionados
- [[impedancia-salida-estabilidad]] · [[marco-dq]] · [[componentes-simetricas]] · [[nyquist-generalizado]] · [[medicion-impedancia-inyeccion]]

## Referencias
- Wang, Blaabjerg, *Harmonic Stability in Power-Electronic-Based Power Systems*, IEEE TPEL 2014.
- Rygg et al., *A Modified Sequence-Domain Impedance Definition*, IEEE JESTPE 2016.
- Sun, *Impedance-Based Stability Criterion*, IEEE TPEL 2011.
