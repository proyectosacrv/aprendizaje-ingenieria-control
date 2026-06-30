---
titulo: Componentes simétricas (Fortescue)
slug: componentes-simetricas
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: []
objetivos: [descomponer un sistema trifásico desequilibrado en secuencias tratables]
tags: [componentes-simetricas, secuencia, desequilibrio, fortescue, intermedio, modelado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-30
relacionados: [sistema-trifasico, potencia-ac-fasores, marco-dq]
referencias:
  - "Kundur, Power System Stability and Control, McGraw-Hill 1994"
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
---

## Definición
Descomposición de tres fasores **desequilibrados** en la suma de tres conjuntos equilibrados:
secuencia **positiva** (+), **negativa** (−) y **homopolar/cero** (0). Permite analizar fallos y
desequilibrios con herramientas de sistema equilibrado.

## Fundamento teórico
Con el operador \( a=e^{j120^\circ} \):
$$ \begin{bmatrix}V_0\\V_+\\V_-\end{bmatrix}=
   \frac{1}{3}\begin{bmatrix}1&1&1\\1&a&a^2\\1&a^2&a\end{bmatrix}
   \begin{bmatrix}V_a\\V_b\\V_c\end{bmatrix} $$
- **Positiva:** terna equilibrada con la secuencia normal (a-b-c) → gira en \( +\omega \).
- **Negativa:** terna equilibrada de secuencia invertida → gira en \( -\omega \) (aparece en
  faltas asimétricas y cargas desequilibradas).
- **Homopolar:** tres fasores en fase, requiere camino de neutro/tierra.

Relación con dq: en marco dq a \( +\omega \), la secuencia positiva es **continua** y la negativa
aparece como rizado de **\( 2\omega \)** (100 Hz), motivo de los controles de doble secuencia.

<div class="cfig"><img src="figuras/componentes-simetricas-fasores.png" alt="fasores de secuencia positiva, negativa y homopolar"><div class="cap">Cualquier terna desequilibrada se descompone en tres equilibradas: positiva (gira +ω), negativa (secuencia invertida, −ω) y homopolar (tres fasores en fase).</div></div>

## 1 — De dónde sale la matriz de Fortescue
**Paso 1 — la síntesis (lo físico).** El punto de partida no es la matriz de análisis, sino su inversa: *cualquier* terna se **construye** sumando tres ternas equilibradas. Por definición de cada secuencia, sus fasores se desfasan \( 120° \) usando el operador \( a=e^{j120°} \) (que cumple \( a^3=1 \) y \( 1+a+a^2=0 \)). Tomando la fase A de cada secuencia (\( V_0,V_+,V_- \)) como referencia:

$$ \begin{aligned}
V_a&=V_0+V_++V_-\\
V_b&=V_0+a^2V_++a\,V_-\\
V_c&=V_0+a\,V_++a^2V_-
\end{aligned} $$

La secuencia **positiva** va a-b-c (la fase B retrasa \( 120° \): factor \( a^2 \)); la **negativa** va a-c-b (factor \( a \)); la **homopolar** es idéntica en las tres (factor \( 1 \)). En forma matricial:

$$ \begin{bmatrix}V_a\\V_b\\V_c\end{bmatrix}=
   \underbrace{\begin{bmatrix}1&1&1\\1&a^2&a\\1&a&a^2\end{bmatrix}}_{A^{-1}}
   \begin{bmatrix}V_0\\V_+\\V_-\end{bmatrix} $$

**Paso 2 — invertir para obtener el análisis.** Queremos \( (V_0,V_+,V_-) \) a partir de \( (V_a,V_b,V_c) \), es decir invertir \( A^{-1} \). En lugar de Gauss, usamos la **ortogonalidad** de las raíces de la unidad: \( 1+a+a^2=0 \). Multiplicando, por ejemplo, la primera fila de \( V_a,V_b,V_c \) por los pesos \( (1,a,a^2) \) y sumando:

$$ V_a+a\,V_b+a^2V_c=V_0(1+a+a^2)+V_+(1+a^3+a^3)+V_-(1+a^2+a^4) $$

**Paso 3 — colapsar con \( a^3=1 \).** Sustituyendo \( a^3=1 \) y \( a^4=a \):
- coeficiente de \( V_0 \): \( 1+a+a^2=0 \) → se anula;
- coeficiente de \( V_+ \): \( 1+1+1=3 \);
- coeficiente de \( V_- \): \( 1+a^2+a=0 \) → se anula.

Queda \( V_a+a\,V_b+a^2V_c=3V_+ \), de donde \( V_+=\tfrac13(V_a+a\,V_b+a^2V_c) \). Repitiendo con pesos \( (1,1,1) \) sale \( V_0=\tfrac13(V_a+V_b+V_c) \), y con \( (1,a^2,a) \) sale \( V_-=\tfrac13(V_a+a^2V_b+a\,V_c) \). Reunidos:

$$ \boxed{\;\begin{bmatrix}V_0\\V_+\\V_-\end{bmatrix}=
   \frac{1}{3}\begin{bmatrix}1&1&1\\1&a&a^2\\1&a^2&a\end{bmatrix}
   \begin{bmatrix}V_a\\V_b\\V_c\end{bmatrix}\;} $$

El factor \( 1/3 \) viene del \( 3 \) que dejó la ortogonalidad. La matriz de análisis es la conjugada (transpuesta) de la de síntesis salvo ese \( 1/3 \): por eso \( A^{-1}=3\bar A^{\top}/3 \) y todo encaja. El ejemplo de la falta monofásica de más abajo aplica directamente esta matriz fila a fila.

## Cuándo y por qué se usa
Análisis de faltas asimétricas, requisitos de **fault ride-through**, control bajo desequilibrio
de red y diseño de lazos de secuencia negativa en convertidores. Complementa a [[marco-dq]] y
[[marco-dq|transformada de Clarke]].

## Procedimiento (genérico)
1. Mide los fasores de fase \( V_a,V_b,V_c \).
2. Aplica la matriz de Fortescue → \( V_0,V_+,V_- \).
3. Analiza/regula cada secuencia por separado.
4. Recompón (matriz inversa) para volver a magnitudes de fase.

## Ejemplo de aplicación real
**Problema:** Falta monofásica a tierra en la fase A. Tensiones de bus: \( V_a=0 \), \( V_b=1\angle{-120°}\,\text{p.u.} \), \( V_c=1\angle{+120°}\,\text{p.u.} \). Descomponer en secuencias e interpretar.

Aplicando la matriz de Fortescue: \( V_+=\tfrac{1}{3}(0+a\cdot1\angle{-120°}+a^2\cdot1\angle{120°}) \) donde \( a=e^{j120°} \). Numéricamente: \( V_+=\tfrac{1}{3}(0+1\angle0°+1\angle0°)=\tfrac{2}{3}\,\text{p.u.} \); \( V_-=\tfrac{1}{3}(0+a^2\cdot1\angle{-120°}+a\cdot1\angle{120°})=-\tfrac{1}{3}\,\text{p.u.} \); \( V_0=\tfrac{1}{3}(0+1\angle{-120°}+1\angle{120°})=-\tfrac{1}{3}\,\text{p.u.} \). Las tres secuencias son iguales en magnitud (\( 1/3 \) p.u.) — típico de falta monofásica. En el control del VSC, la secuencia negativa induce un rizado de \( 2\omega \) en la tensión del bus dq, que el lazo de tensión debe filtrar o compensar con un controlador de doble secuencia.

## Ejemplo de código
```python
import numpy as np
a = np.exp(1j*2*np.pi/3)
A = (1/3)*np.array([[1,1,1],[1,a,a**2],[1,a**2,a]])
V0, Vp, Vn = A @ np.array([Va, Vb, Vc])   # fasores de fase complejos
```

## Parámetros y valores típicos
Límite de desequilibrio en red (factor \( V_-/V_+ \)) típicamente < 2 %. En falta asimétrica
\( V_- \) puede subir a decenas de %.

## Errores comunes
- Aplicar el método a magnitudes instantáneas en vez de a **fasores** (régimen sinusoidal).
- Olvidar que sin neutro la secuencia 0 no circula.
- Ignorar el rizado de \( 2\omega \) que la secuencia negativa induce en dq.

## Conceptos relacionados
- [[sistema-trifasico]] · [[potencia-ac-fasores]] · [[marco-dq]]

## Referencias
- Kundur, *Power System Stability and Control*, 1994.
- Yazdani, Iravani, 2010.
