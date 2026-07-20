---
titulo: Métricas de desempeño (temporal y frecuencial)
slug: metricas-desempeno
categoria: metodologia
tipo: concepto
nivel: basico
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [medir si el control cumple los objetivos de desempeno]
tags: [sobreimpulso, tiempo-establecimiento, ancho-de-banda, zeta, metricas]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [especificaciones-control, analisis-modal, funciones-sensibilidad, margenes-estabilidad]
referencias:
  - "Aström, Murray, Feedback Systems, Princeton 2008"
---

## Definición
Conjunto de números que cuantifican cómo de bien se comporta el lazo cerrado, en el dominio del
tiempo y de la frecuencia. Son los criterios de aceptación frente a las especificaciones.

## Fundamento teórico
**Temporal** (respuesta a escalón):
- Sobreimpulso \( M_p \), tiempo de subida \( t_r \), tiempo de establecimiento
  \( t_s\approx 4/(\zeta\omega_n) \), error en régimen \( e_{ss} \).
- Para 2º orden: \( M_p=e^{-\pi\zeta/\sqrt{1-\zeta^2}} \) → relación directa con \( \zeta \).

**Frecuencial**:
- Ancho de banda (donde \( |T|=-3 \) dB), pico de resonancia \( M_r \), \( M_s=\max|S| \).
- Amortiguamiento de cada modo \( \zeta_i=-\sigma_i/|\lambda_i| \) (ver [[analisis-modal]]).

Para sistemas de orden alto (un convertidor), las fórmulas de 2º orden son orientativas; lo
riguroso es mirar polos dominantes + simulación.

<div class="cfig"><img src="figuras/metricas-desempeno-escalon.png" alt="respuesta a escalon con metricas temporales anotadas"><div class="cap">Sobre la respuesta a escalón se leen las métricas temporales: el sobreimpulso $M_p$ (ligado a $\zeta$), el tiempo de establecimiento $t_s\approx4/(\zeta\omega_n)$ dentro de la banda del 2 %, el tiempo de subida y el error en régimen $e_{ss}$. Son los criterios de aceptación frente a las especificaciones; en sistemas de orden alto se complementan con polos dominantes y simulación.</div></div>

## 1 — IAE e ITAE: definición y por qué ITAE penaliza más los errores tardíos
**Paso 1 — IAE (Integral of Absolute Error).** El índice IAE acumula el valor absoluto del error de seguimiento a lo largo del tiempo:

$$ \text{IAE} = \int_0^\infty |e(t)|\,dt $$

Cada instante de tiempo contribuye igual, con peso unitario. Para un sistema de segundo orden con respuesta al escalón, el IAE está dominado por el pico del error inicial (sobreimpulso) y por el tiempo de establecimiento, pero **todos los momentos valen lo mismo**.

**Paso 2 — ITAE (Integral of Time-weighted Absolute Error).** El índice ITAE pondera el error con el tiempo transcurrido:

$$ \text{ITAE} = \int_0^\infty t\,|e(t)|\,dt $$

Un error \( e_0 \) que ocurre en \( t=0 \) aporta \( 0 \) a la integral (peso cero). El mismo error en \( t=10\,\text{s} \) aporta \( 10\,e_0 \): la penalización **crece linealmente** con el tiempo. Así, el ITAE es insensible a los errores transitorios iniciales inevitables y muy sensible a los errores que persisten.

**Paso 3 — consecuencia en el diseño.** Minimizar el ITAE produce controladores que liquidan rápidamente el error de régimen permanente y el error oscilatorio tardío, aunque puedan tolerar un sobreimpulso inicial algo mayor que el IAE. Para sistemas con perturbaciones de baja frecuencia lentas (p.ej. variación de carga en minutos), el ITAE es el índice más representativo del coste real.

$$ \boxed{\text{ITAE} > \text{IAE si el error persiste en el tiempo}\;(t>0)} $$

**Comprobación:** para \( e(t)=e^{-\zeta\omega_n t}\sin(\omega_d t) \), a medida que \( \zeta \) decrece los errores tardan más en extinguirse y el peso \( t \) amplifica la diferencia; el ITAE óptimo impone mayor amortiguamiento que el IAE óptimo.

## Cuándo y por qué se usa
En la fase de evaluación, para comprobar objetivamente contra las [[especificaciones-control]].
También guían el rediseño (qué métrica falla → qué tocar).

## Procedimiento (genérico)
1. Respuesta a escalón (simulación o `control.step_response`) → \( M_p, t_s, e_{ss} \).
2. Respuesta en frecuencia → ancho de banda, \( M_r, M_s \).
3. Autovalores → \( \zeta \) de cada modo (criterio \( \zeta>0.1 \), idealmente >0.3).
4. Compara con objetivos; identifica el modo/métrica limitante.

## Ejemplo de aplicación real
**Problema:** El lazo de tensión de un microgrid ante un escalón de carga del 50 % muestra: caída pico de 7 %, recuperación en 80 ms, sobreimpulso de retorno de 3 %. Evaluar contra especificaciones habituales y calcular el amortiguamiento del modo dominante.

Métricas medidas vs. límites típicos de microrredes: caída \( 7\,\%<10\,\% \) (\(\checkmark\)), tiempo de asentamiento \( 80\,\text{ms}<100\,\text{ms} \) (\(\checkmark\)), sobreimpulso de retorno \( 3\,\%<5\,\% \) (\(\checkmark\)). El modo dominante tiene frecuencia de oscilación \( \approx3\,\text{Hz} \): con el sobreimpulso del 3 %, \( \zeta\approx0.65 \). Comparar con un diseño más agresivo (caída 4 %, 50 ms, retorno 8 %): mejora caída y asentamiento pero viola el límite de retorno. Las métricas no son independientes — el optimum no es siempre el más rápido.

## Ejemplo de código
```python
import control as ct, numpy as np
t, y = ct.step_response(T)
Mp = (y.max()-y[-1])/y[-1]*100
ts = t[np.where(np.abs(y-y[-1])>0.02*y[-1])[0][-1]]   # banda del 2%
```

## Parámetros y valores típicos
\( \zeta>0.3 \) bueno, \( M_p<10\% \), \( M_s<2 \). En convertidores el modo electromecánico
(droop/PLL) suele ser el limitante.

## Errores comunes
- Aplicar fórmulas de 2º orden a un sistema de orden alto sin verificar polos dominantes.
- Medir solo en un punto de operación (ver [[robustez-parametrica]]).

## Uso en proyectos
- **01 (GFM)**: modo de potencia 3.3 Hz con \( \zeta=0.40 \) (objetivo cumplido).
- **02 (GFL)**: modo de la PLL 21 Hz con \( \zeta=0.71 \).

## 3 — Métricas en el dominio del tiempo

Las métricas integrales del error se calculan sobre la respuesta al escalón y permiten cuantificar el desempeño con un único número:

**IAE (Integral of Absolute Error):** acumula el error en valor absoluto con peso uniforme.

$$ \text{IAE} = \int_0^\infty |e(t)|\,dt $$

Penaliza errores pequeños y grandes por igual; es fácil de calcular y tiene sentido físico directo (área del error).

**ISE (Integral of Squared Error):** eleva al cuadrado el error, penalizando mucho más los errores grandes.

$$ \text{ISE} = \int_0^\infty e^2(t)\,dt $$

Produce controladores más agresivos (respuesta más rápida con mayor sobreimpulso) porque el cuadrado amplifica los picos del error.

**ITAE (Integral of Time-weighted Absolute Error):** pondera el error con el tiempo transcurrido, penalizando los errores tardíos.

$$ \text{ITAE} = \int_0^\infty t\,|e(t)|\,dt $$

Un sobreimpulso inicial aporta poco (el tiempo es pequeño); un error que persiste a \( t = 10\,\text{s} \) aporta mucho. El ITAE favorece respuestas sin oscilación tardía, lo que lo hace especialmente útil para sistemas de seguimiento de referencia en control de potencia.

**ITSE (Integral of Time-weighted Squared Error):**

$$ \text{ITSE} = \int_0^\infty t\,e^2(t)\,dt $$

Combinación del peso temporal (ITAE) con la penalización cuadrática (ISE): produce controladores con respuesta intermedia.

## 4 — Métricas en el dominio de la frecuencia

Las métricas frecuenciales miden el comportamiento del lazo cerrado en función de la frecuencia de excitación:

**Ancho de banda \( \omega_{bw} \):** frecuencia a la que \( |T(j\omega)| = -3\,\text{dB} \) (función de transferencia lazo cerrado). Es la velocidad del lazo: un sistema con \( \omega_{bw} = 100\,\text{rad/s} \) sigue referencias hasta ~16 Hz.

**Pico de resonancia \( M_r = \max_\omega |T(j\omega)| \):** relacionado con el amortiguamiento del modo dominante. Para un segundo orden, \( M_r = 1/(2\zeta\sqrt{1-\zeta^2}) \) para \( \zeta < 0.707 \). Un \( M_r > 2 \) indica amortiguamiento insuficiente.

**Márgenes de ganancia (GM) y de fase (PM):** distancia del lazo abierto a la inestabilidad. Son las métricas de robustez por excelencia (ver [[margenes-estabilidad]]). Un \( PM > 45° \) y \( GM > 6\,\text{dB} \) son requisitos mínimos habituales.

**Sensibilidad máxima \( M_s = \|S\|_\infty \):** el pico de la función de sensibilidad \( S = 1/(1+L) \). Cuantifica la robustez frente a incertidumbres: \( M_s < 2 \) (\( < 6\,\text{dB} \)) es el criterio habitual. Se relaciona con los márgenes: \( GM \geq M_s/(M_s-1) \) y \( PM \geq 2\arcsin(1/(2M_s)) \).

## 5 — Métricas de calidad de potencia

Para convertidores conectados a la red, se añaden métricas específicas de calidad de la potencia suministrada:

**THD de corriente:** la distorsión armónica total de la corriente inyectada en la red debe ser inferior al 5 % (IEEE 519) para sistemas de distribución:

$$ \text{THD}_I = \frac{\sqrt{\sum_{h=2}^{\infty} I_h^2}}{I_1} \times 100\,\% $$

**Factor de potencia:** \( FP = P/S = P/(\sqrt{P^2+Q^2}) \). Un FP bajo significa que el convertidor consume reactiva de la red innecesariamente. El objetivo habitual es \( FP > 0.95 \).

**Desequilibrio de tensión (VUF):** \( VUF = V_{neg}/V_{pos} \times 100\,\% \), donde \( V_{neg} \) y \( V_{pos} \) son las componentes de secuencia negativa y positiva (ver [[componentes-simetricas]]). La norma EN 50160 exige \( VUF < 2\,\% \) para redes de baja tensión.

**Flicker:** medida de la variación rápida de la tensión que causa molestias visuales en la iluminación. Se cuantifica con \( P_{st} \) (severidad de corto plazo, 10 min) y \( P_{lt} \) (largo plazo, 2 h). Los límites normativos son \( P_{st} < 1.0 \) y \( P_{lt} < 0.65 \) (EN 50160).

## 6 — Compromiso entre métricas

Las métricas no son independientes y maximizar una suele empeorar otra:

**IAE vs ISE:** el ISE selecciona controladores más agresivos (mayor \( K_p \)) que minimizan el pico del error a costa de mayor sobreimpulso. El IAE es más conservador. Para control de potencia donde el sobreimpulso puede disparar protecciones, IAE o ITAE son preferibles.

**ITAE:** es la métrica más adecuada para sistemas de seguimiento de referencia en control de potencia, porque refleja el coste acumulado de un error que persiste mientras la carga no se equilibra.

**Diagrama de Pareto BW vs PM:** existe un tradeoff fundamental entre velocidad del lazo (ancho de banda) y robustez (margen de fase). Aumentar el ancho de banda reduciendo la ganancia cruzada del lazo abierto reduce el PM disponible. La frontera de Pareto muestra los diseños que maximizan BW para cada PM mínimo dado: no existe un diseño que sea simultáneamente el más rápido y el más robusto.

**Ejemplo numérico:** optimizar \( K_p, T_i \) de un PI minimizando ITAE con restricción \( PM > 45° \). El ITAE sin restricción puede dar \( PM = 30° \) (inestable en la práctica); añadir la restricción mueve la solución a un controlador más lento pero robusto. Este es el problema de diseño multiobjetivo típico del ajuste de un PI de control de corriente.

<div class="cfig"><img src="figuras/metricas-desempeno-analisis.png" alt="Métricas de desempeño: IAE/ISE/ITAE comparadas, diagrama de Pareto BW vs PM, y calidad de potencia vs carga"><div class="cap">Cuatro paneles: respuestas al escalón para distintos amortiguamientos con las métricas visualizadas; gráfico de barras comparando IAE, ISE e ITAE para cada caso; diagrama de Pareto entre ancho de banda y margen de fase; curvas de THD de corriente y factor de potencia en función del nivel de carga.</div></div>

## Conceptos relacionados
- [[especificaciones-control]] · [[analisis-modal]] · [[funciones-sensibilidad]] · [[margenes-estabilidad]]

## Referencias
- Aström, Murray, *Feedback Systems*, 2008.
