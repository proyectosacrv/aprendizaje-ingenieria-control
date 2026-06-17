---
titulo: Sincronización por PLL (SRF-PLL y DSOGI/FLL)
slug: pll-srf
categoria: control
tipo: tecnica
nivel: intermedio
proyectos: [02-GFL-Impedance]
objetivos: [estimar ángulo y frecuencia de una tensión trifásica para sincronizar el control, también bajo desequilibrio y distorsión]
tags: [pll, sincronizacion, srf, dsogi, sogi, fll, secuencia, desequilibrio, dq, ancho-de-banda]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-16
relacionados: [grid-forming-vs-following, marco-dq, componentes-simetricas, impedancia-salida-estabilidad, interaccion-pll-red-debil, fault-ride-through]
referencias:
  - "Kaura, Blasko, Operation of a Phase Locked Loop System Under Distorted Utility Conditions, IEEE TIA 1997"
  - "Teodorescu et al., Grid Converters for PV and Wind Power Systems, Wiley 2011"
  - "Rodríguez et al., Advanced Grid Synchronization System for Power Converters under Unbalanced and Distorted Conditions, IEEE TIE 2007"
  - "Rodríguez et al., Multiresonant Frequency-Locked Loop for Grid Synchronization, IEEE TIE 2011"
---

## Definición
Una PLL (phase-locked loop) estima en tiempo real el ángulo y la frecuencia de una tensión trifásica de referencia para que el control pueda trabajar en un marco dq sincronizado con ella. Es el bloque de sincronización que cualquier equipo necesita cuando tiene que seguir a una tensión que no genera él mismo: el caso típico es el inversor grid-following, pero el mismo bloque aparece en rectificadores activos, STATCOM, filtros activos y en la re-sincronización previa a cerrar un interruptor contra una red viva. Esta ficha cubre las dos variantes habituales: la SRF-PLL (simple, para tensión equilibrada y limpia) y la DSOGI-PLL/FLL (robusta frente a desequilibrio y armónicos).

## Qué se sincroniza (contexto genérico)
La entrada de la PLL es siempre una terna de tensiones medida en algún punto: el PCC, el condensador del filtro, los bornes de una máquina, etc. La PLL no distingue de dónde viene esa tensión; solo necesita que tenga una componente fundamental dominante a frecuencia cercana a la nominal. La salida es un ángulo theta que se usa para las transformadas de Park del resto del control, y una estimación de frecuencia. La calidad de esa estimación (rizado, retardo, robustez en falta) determina cuánto puede fiarse el control de su marco dq.

## SRF-PLL (marco síncrono)
La SRF-PLL (Synchronous Reference Frame PLL) alinea el marco dq con la tensión llevando su componente q a cero.

### Diagrama de bloques
Park con el ángulo estimado → vq → PI → suma omega0 → integrador → theta_pll, que realimenta a la Park.

<div class="cfig"><img src="figuras/pll-srf-bloques.png" alt="diagrama de bloques de la SRF-PLL"><div class="cap">Lazo de la SRF-PLL: el PI ajusta la frecuencia para llevar vq a cero; el integrador genera el ángulo θpll, que cierra el lazo realimentando la transformada de Park.</div></div>

### Fundamento — de dónde se sale
Se mide la tensión y se pasa a dq con el ángulo estimado theta_pll. Si el error de ángulo es delta_theta = theta − theta_pll, la componente q vale vq = V·sin(delta_theta) ≈ V·delta_theta para error pequeño. El PI lleva vq a cero ajustando la frecuencia:

omega_pll = omega0 + Kp·vq + Ki·∫vq,    dtheta_pll/dt = omega_pll

Linealizando con vq ≈ V·delta_theta y d(delta_theta)/dt = omega − omega_pll, el lazo cerrado es de segundo orden con ecuación característica:

s² + Kp·V·s + Ki·V = 0   ⟹   omega_n = raiz(Ki·V),   zeta = Kp·V / (2·omega_n)

El ancho de banda de la PLL es aproximadamente omega_n. Es el parámetro que gobierna la robustez frente a la red.

> A resaltar: una PLL rápida (omega_n alto) sincroniza antes pero interactúa con la impedancia de la red débil y puede inestabilizar (resistencia negativa de la PLL, ver [[impedancia-salida-estabilidad|resistencia negativa]] y [[interaccion-pll-red-debil]]). El ancho de banda de la PLL fija el SCR crítico.

## DSOGI-PLL / FLL (robusta a desequilibrio y distorsión)
Cuando la tensión está desequilibrada o distorsionada, la SRF-PLL simple deja pasar un rizado de 2·omega al ángulo. La DSOGI usa dos SOGI (second-order generalized integrators) en cuadratura para filtrar y separar las componentes de secuencia positiva y negativa antes de cerrar el lazo.

### Fundamento
Un SOGI es un filtro adaptativo resonante sintonizado a omega' que entrega la señal filtrada v' y su versión en cuadratura qv' (90° de retraso):

- v'/v   = k·omega'·s / (s² + k·omega'·s + omega'²)
- qv'/v  = k·omega'² / (s² + k·omega'·s + omega'²)

Aplicando un SOGI a v_alpha y otro a v_beta (tras Clarke, ver [[marco-dq|transformada de Clarke]]) se tienen las cuatro señales v'a, qv'a, v'b, qv'b. El cálculo de componentes de secuencia instantáneas (Fortescue en alfa-beta) da:

- v_alfabeta_pos = (1/2)·(v'a − qv'b)
- v_alfabeta_neg = (1/2)·(v'a + qv'b)

Sobre la secuencia positiva se cierra una SRF-PLL o, mejor, un FLL (frequency-locked loop): la frecuencia se estima de la realimentación del error del SOGI sin lazo de fase, lo que lo hace insensible a saltos de fase y muy robusto en faltas. El FLL adapta omega' de los SOGI, dando seguimiento de frecuencia sin la no linealidad de la PLL. Frente a la SRF-PLL simple, la DSOGI rechaza el rizado de 2·omega que la secuencia negativa provoca en dq, dando un ángulo limpio para el control y para el fault ride-through.

<div class="cfig"><img src="figuras/dsogi-pll-sogi.png" alt="respuesta en frecuencia del SOGI: banda y cuadratura"><div class="cap">Cada SOGI es un filtro resonante sintonizado a f0: v'/v es un paso-banda centrado en la fundamental y qv'/v entrega la misma señal retrasada 90° (cuadratura). Con un SOGI por eje αβ se calculan las secuencias positiva y negativa instantáneas, dando un ángulo limpio incluso con desequilibrio.</div></div>

## Cuándo y por qué se usa
SRF-PLL: en todo equipo grid-following con red equilibrada y limpia, y en cualquier control que solo necesite el ángulo de una tensión sana. DSOGI-PLL/FLL: sincronización bajo desequilibrio y armónicos, imprescindible para [[fault-ride-through]] (necesita secuencia positiva limpia y secuencia negativa para el soporte) y para redes débiles/distorsionadas. Ninguna se usa en grid-forming, que genera su propio ángulo.

## Procedimiento de diseño (genérico)
SRF-PLL:
1. Fija el ancho de banda f_pll: compromiso entre rapidez (rechazo de huecos y saltos) y robustez (una PLL rápida se desestabiliza en red débil). Típico 10–50 Hz.
2. Con zeta ≈ 0.707: Ki = omega_n²/V, Kp = 2·zeta·omega_n/V (normaliza por la amplitud V de la tensión).
3. Si la red tiene armónicos/desequilibrio, pasa a DSOGI o añade prefiltros (notch).
4. Verifica la interacción con la red en el rango de SCR esperado.

DSOGI-PLL/FLL:
1. Clarke abc→alfa-beta de la tensión medida.
2. Dos SOGI (uno por eje) con ganancia k ≈ raiz(2) (compromiso filtrado/velocidad).
3. Calcula secuencia positiva/negativa instantánea (combinación de v', qv').
4. Cierra PLL/FLL sobre la secuencia positiva; usa la negativa para FRT/monitorización.
5. Sintoniza la banda del FLL/PLL (compromiso velocidad vs rechazo de 2·omega, armónicos y ruido).

## Ejemplo de código
```python
import numpy as np

# --- SRF-PLL ---
wn = 2*np.pi*f_pll
Ki = wn**2 / V0;  Kp = 2*zeta*wn / V0
w_pll = w0 + Kp*v_q + Ki*eps   # v_q: componente q de la tension en el marco de la PLL
d_eps = v_q                    # integrador
d_theta = w_pll                # angulo estimado

# --- SOGI (1 eje, para DSOGI) ---
def sogi(v, v_prev, qv_prev, w, k, dt):
    err = k*(v - v_prev)*w
    dvp = (err - qv_prev*w)    # v'  (resonante)
    dqv = v_prev*w             # qv' (cuadratura)
    return v_prev + dvp*dt, qv_prev + dqv*dt
# secuencia +: v_alpha_pos = 0.5*(vp_a - qv_b)
```

## Parámetros y valores típicos
- SRF-PLL: f_pll 10–50 Hz (robusta); >80–100 Hz ya es "rápida" y arriesgada en red débil. zeta ≈ 0.707.
- DSOGI: ganancia SOGI k ≈ 1.41 (zeta ≈ 0.7). Banda PLL/FLL 20–60 rad/s. Tiempo de detección de secuencia < medio ciclo a un ciclo.

## Errores comunes
- PLL demasiado rápida "para sincronizar mejor": desestabiliza en red débil (el gran pitfall del GFL).
- No normalizar por la amplitud V → ganancias dependientes del punto de operación.
- Usar SRF-PLL simple en falta asimétrica → ángulo contaminado por 2·omega; usar DSOGI.
- En DSOGI: banda de PLL/FLL demasiado ancha pasa rizado de secuencia negativa/armónicos al ángulo; k mal elegido (alto = rápido pero poco filtrado, bajo = limpio pero lento).
- Olvidar que una PLL de banda ancha empeora la impedancia en red débil (ver [[interaccion-pll-red-debil]]).

## Uso en proyectos
- 02 - GFL-Impedance (sincronizar): SRF-PLL sobre vC. Con f_pll = 30 Hz el GFL es robusto en todo SCR; con f_pll = 100 Hz se inestabiliza en red débil (SCR crítico ≈ 3.5).

## Conceptos relacionados
- [[grid-forming-vs-following]] · [[marco-dq]] · [[componentes-simetricas]] · [[impedancia-salida-estabilidad|resistencia negativa]] · [[interaccion-pll-red-debil]] · [[fault-ride-through]]

## Referencias
- Kaura, Blasko, IEEE TIA 1997.
- Teodorescu et al., Grid Converters for PV and Wind Power Systems, Wiley 2011.
- Rodríguez et al., Advanced Grid Synchronization..., IEEE TIE 2007.
- Rodríguez et al., Multiresonant Frequency-Locked Loop..., IEEE TIE 2011.
