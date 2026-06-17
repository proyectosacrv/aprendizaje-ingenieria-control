---
titulo: Resonancia en circuitos RLC
slug: resonancia-rlc
categoria: fisica-modelado
tipo: concepto
nivel: basico
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [entender la resonancia del filtro LCL y por qué hay que amortiguarla]
tags: [resonancia, rlc, factor-calidad, filtro, basico]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-06-11
relacionados: [filtro-lcl, impedancia-reactancia, diagrama-bode, respuesta-segundo-orden]
referencias:
  - "Sedra & Smith, Microelectronic Circuits"
  - "Erickson & Maksimovic, Fundamentals of Power Electronics"
---

## Definición
En un circuito con inductancia \( L \) y capacidad \( C \), existe una frecuencia a la que sus
reactancias se cancelan: la **frecuencia de resonancia**. Cerca de ella, pequeñas excitaciones
producen tensiones/corrientes grandes (un pico de ganancia), tanto más agudo cuanto menor sea la
resistencia.

## Fundamento teórico
La reactancia inductiva \( \omega L \) crece con la frecuencia y la capacitiva \( 1/(\omega C) \)
decrece; se igualan en
$$ f_0 = \frac{1}{2\pi\sqrt{LC}} $$
En resonancia, un RLC **serie** presenta impedancia mínima (\( =R \)) y un **paralelo** impedancia
máxima. La agudeza del pico la da el **factor de calidad**
$$ Q = \frac{\omega_0 L}{R} = \frac{1}{R}\sqrt{\frac{L}{C}}, \qquad \zeta = \frac{1}{2Q} $$
con \( \zeta \) el amortiguamiento. \( Q \) alto (R pequeña) \( \Rightarrow \) pico agudo y poco
amortiguado. El filtro **LCL** tiene su resonancia en
$$ f_{res} = \frac{1}{2\pi}\sqrt{\frac{L_1+L_2}{L_1 L_2 C_f}} $$

<div class="cfig"><img src="figuras/resonancia-rlc-zf.png" alt="impedancia de un RLC serie con la frecuencia"><div class="cap">Impedancia de un RLC serie: cae a un mínimo (=R) en la resonancia f0. Con R baja (Q alto) el valle es profundo y agudo; con R alta (Q bajo) es suave.</div></div>

## Cuándo y por qué se usa
Aparece en todo filtro LC/LCL de convertidor. Su resonancia, si no se amortigua, hace **inestable**
cualquier lazo de control rápido. Entender \( f_0 \) y \( Q \) es el paso previo a diseñar el
amortiguamiento (pasivo con una resistencia, o activo por realimentación).

## Procedimiento de diseño (genérico)
1. Identifica \( L \) y \( C \) y calcula \( f_0 \).
2. Calcula \( Q \) (o \( \zeta \)) con la resistencia presente.
3. Si \( Q \) es alto (poco amortiguado), añade amortiguamiento: resistencia serie/paralelo
   (pasivo, con pérdidas) o realimentación (activo, sin pérdidas).
4. Coloca \( f_0 \) lejos del ancho de banda de control y por debajo de \( f_{sw}/2 \).

## Ejemplo de código
```python
import numpy as np
L, C, R = 2e-3, 20e-6, 0.1
f0 = 1/(2*np.pi*np.sqrt(L*C))          # frecuencia de resonancia
Q  = (1/R)*np.sqrt(L/C)                 # factor de calidad
```

## Parámetros y valores típicos
\( f_0 \) de un LCL: cientos de Hz a pocos kHz (≈1.1 kHz en el proyecto 01). \( \zeta \) natural casi
nulo; tras amortiguamiento activo se lleva a \( \zeta \approx 0.1\text{–}0.3 \).

## Errores comunes
- Dejar la resonancia sin amortiguar y subir el lazo de corriente \( \to \) inestabilidad.
- Confundir resonancia serie (mínimo de impedancia) con paralelo (máximo).
- Situar \( f_0 \) demasiado cerca del ancho de banda del control.

## Uso en proyectos
- **01 / 02 (filtro LCL):** la resonancia a ~1.1 kHz aparece como un par de polos poco amortiguados;
  se trata con amortiguamiento activo (realimentación de la corriente del condensador).

## Conceptos relacionados
- [[filtro-lcl]] · [[impedancia-reactancia]] · [[diagrama-bode]] · [[respuesta-segundo-orden]]

## Referencias
- Erickson & Maksimovic, *Fundamentals of Power Electronics*.
