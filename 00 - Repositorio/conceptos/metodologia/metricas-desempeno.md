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

## Conceptos relacionados
- [[especificaciones-control]] · [[analisis-modal]] · [[funciones-sensibilidad]] · [[margenes-estabilidad]]

## Referencias
- Aström, Murray, *Feedback Systems*, 2008.
