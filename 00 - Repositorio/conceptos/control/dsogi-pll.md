---
titulo: DSOGI-PLL / FLL y detección de secuencia
slug: dsogi-pll
categoria: control
tipo: tecnica
nivel: avanzado
proyectos: []
objetivos: [sincronizar y extraer secuencia positiva/negativa bajo desequilibrio y distorsión]
tags: [dsogi, sogi, fll, pll, secuencia, desequilibrio, sincronizacion, avanzado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-09
relacionados: [pll-srf, componentes-simetricas, transformada-clarke, fault-ride-through, interaccion-pll-red-debil]
referencias:
  - "Rodríguez et al., Advanced Grid Synchronization System for Power Converters under Unbalanced and Distorted Conditions, IEEE TIE 2007"
  - "Rodríguez et al., Multiresonant Frequency-Locked Loop for Grid Synchronization, IEEE TIE 2011"
---

## Definición
Método de sincronización robusto que usa dos **SOGI** (second-order generalized integrators) en
cuadratura para filtrar y separar las **componentes de secuencia positiva y negativa** de una red
desequilibrada/distorsionada, combinado con una PLL o un **FLL** (frequency-locked loop) para seguir
la frecuencia.

## Fundamento teórico
**SOGI:** filtro adaptativo resonante sintonizado a \( \omega' \) que entrega la señal filtrada
\( v' \) y su versión en cuadratura \( qv' \) (90° de retraso):
$$ \frac{v'}{v}=\frac{k\omega' s}{s^2+k\omega' s+\omega'^2},\qquad
   \frac{qv'}{v}=\frac{k\omega'^2}{s^2+k\omega' s+\omega'^2} $$
Aplicando un SOGI a \( v_\alpha \) y otro a \( v_\beta \) (tras [[transformada-clarke|Clarke]]) se
tienen las cuatro señales \( v'_{\alpha},qv'_{\alpha},v'_{\beta},qv'_{\beta} \). El **cálculo de
componentes de secuencia instantáneas** (método de Fortescue en αβ) da:
$$ v_{\alpha\beta}^{+}=\tfrac12\big(v'_{\alpha}-q v'_{\beta}\big),\qquad
   v_{\alpha\beta}^{-}=\tfrac12\big(v'_{\alpha}+q v'_{\beta}\big) $$
(usando \( q=e^{-j90^\circ} \)). Sobre la secuencia positiva se cierra una **SRF-PLL**
([[pll-srf]]) o, mejor, un **FLL**: la frecuencia se estima de la realimentación del error del SOGI
(sin lazo de fase), lo que lo hace **insensible a saltos de fase** y muy robusto en faltas. El FLL
adapta \( \omega' \) de los SOGI → seguimiento de frecuencia sin la no linealidad de la PLL.

Frente a la SRF-PLL simple: la DSOGI rechaza el rizado de \( 2\omega \) que la secuencia negativa
provoca en dq, dando un ángulo limpio para el control y FRT.

## Cuándo y por qué se usa
Sincronización de convertidores de red bajo **desequilibrio y armónicos**, imprescindible para
[[fault-ride-through]] (necesita secuencia positiva limpia y secuencia negativa para soporte) y para
operar en redes débiles/distorsionadas.

## Procedimiento de diseño (genérico)
1. Clarke abc→αβ de la tensión medida.
2. Dos SOGI (uno por eje) con ganancia \( k\approx\sqrt2 \) (compromiso filtrado/velocidad).
3. Calcula secuencia positiva/negativa instantánea (combinación de \( v',qv' \)).
4. Cierra PLL/FLL sobre la secuencia positiva; usa la negativa para FRT/monitorización.
5. Sintoniza la banda del FLL/PLL (compromiso velocidad vs rechazo de armónicos y ruido).

## Ejemplo de código
```python
def sogi(v, v_prev, qv_prev, w, k, dt):     # 1 eje (discretización simple)
    err = k*(v - v_prev)*w
    dvp = (err - qv_prev*w)                 # v'  (resonante)
    dqv = v_prev*w                          # qv' (cuadratura)
    return v_prev + dvp*dt, qv_prev + dqv*dt
# secuencia +: v_alpha_pos = 0.5*(vp_a - qv_b)
```

## Parámetros y valores típicos
Ganancia SOGI \( k\approx1.41 \) (\( \zeta\approx0.7 \)). Banda PLL/FLL 20–60 rad/s (compromiso con
rechazo de \( 2\omega \) y armónicos). Tiempo de detección de secuencia < medio ciclo–1 ciclo.

## Errores comunes
- Banda de PLL/FLL demasiado ancha → pasa rizado de secuencia negativa/armónicos al ángulo.
- \( k \) mal elegido: alto → rápido pero poco filtrado; bajo → limpio pero lento.
- Usar SRF-PLL simple en falta asimétrica (ángulo contaminado por \( 2\omega \)).
- Olvidar que una PLL de banda ancha empeora la [[interaccion-pll-red-debil|impedancia en red débil]].

## Conceptos relacionados
- [[pll-srf]] · [[componentes-simetricas]] · [[transformada-clarke]] · [[fault-ride-through]] · [[interaccion-pll-red-debil]]

## Referencias
- Rodríguez et al., *Advanced Grid Synchronization ... Unbalanced and Distorted Conditions*, IEEE TIE 2007.
- Rodríguez et al., *Multiresonant Frequency-Locked Loop for Grid Synchronization*, IEEE TIE 2011.
