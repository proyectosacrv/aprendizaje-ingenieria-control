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
fecha_actualizacion: 2026-06-08
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
