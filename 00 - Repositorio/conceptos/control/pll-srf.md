---
titulo: PLL de marco síncrono (SRF-PLL)
slug: pll-srf
categoria: control
tipo: tecnica
nivel: intermedio
proyectos: [02-GFL-Impedance]
objetivos: [sincronizar el inversor con la tension de red]
tags: [pll, sincronizacion, grid-following, dq, ancho-de-banda]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [grid-forming-vs-following, marco-dq, no-pasividad-resistencia-negativa, interaccion-pll-red-debil]
referencias:
  - "Kaura, Blasko, Operation of a Phase Locked Loop System Under Distorted Utility Conditions, IEEE TIA 1997"
  - "Teodorescu et al., Grid Converters for PV and Wind Power Systems, Wiley 2011"
---

## Definición
La **SRF-PLL** (Synchronous Reference Frame PLL) estima el ángulo y la frecuencia de la
tensión de red alineando el marco dq con dicha tensión: lleva la componente **q** a cero. Es
el bloque de sincronización del grid-following.

## Fundamento teórico
Mide la tensión, la pasa a dq con su ángulo estimado \( \theta_{pll} \) y regula \( v_q\to 0 \)
con un PI que ajusta la frecuencia:
$$ \omega_{pll}=\omega_0 + K_{p}\,v_q + K_{i}\!\int v_q,\qquad \dot\theta_{pll}=\omega_{pll} $$
Linealizada (\( v_q\approx V\,\Delta\theta \)) es un lazo de 2º orden:
$$ \omega_n=\sqrt{K_i V},\qquad \zeta=\frac{K_p V}{2\omega_n} $$
El **ancho de banda** de la PLL es \( \approx \omega_n \). Es el parámetro que gobierna la
robustez frente a la red (ver [[interaccion-pll-red-debil]]).

## Cuándo y por qué se usa
En todo inversor grid-following (PV, eólica GFL) y en cualquier control que necesite el ángulo
de red. No se usa en grid-forming (que genera su propio ángulo).

## Procedimiento de diseño (genérico)
1. Fija el ancho de banda \( f_{pll} \): compromiso entre rapidez de sincronización (rechazo de
   huecos, saltos) y **robustez** (una PLL rápida interactúa con la red débil → inestabilidad).
   Típico 10–50 Hz.
2. Con \( \zeta\approx 0.707 \): \( K_i=\omega_n^2/V \), \( K_p=2\zeta\omega_n/V \) (normaliza por
   la amplitud \( V \) de la tensión).
3. Si la red puede tener armónicos/desequilibrio, añade prefiltros (DSOGI, notch) o usa una
   variante (DDSRF, SOGI-PLL).
4. Verifica la interacción con la red en el rango de SCR esperado.

## Ejemplo de código
```python
wn = 2*np.pi*f_pll
Ki = wn**2 / V0;  Kp = 2*zeta*wn / V0
# dinamica de la PLL (v_q es la componente q de la tension medida en el marco PLL)
w_pll = w0 + Kp*v_q + Ki*eps
d_eps = v_q                # integrador
d_theta = w_pll            # angulo estimado
```

## Parámetros y valores típicos
\( f_{pll} \) 10–50 Hz (robusta) ; >80–100 Hz ya es "rápida" y arriesgada en red débil.
\( \zeta\approx 0.707 \).

## Errores comunes
- **PLL demasiado rápida** "para sincronizar mejor": desestabiliza en red débil (el gran
  pitfall del GFL).
- No normalizar por la amplitud → ganancias dependientes del punto de operación.
- Ignorar armónicos/desequilibrio → ángulo con rizado.

## Uso en proyectos
- **02 - GFL-Impedance** (objetivo: sincronizar): SRF-PLL sobre \( v_C \). Con \( f_{pll}=30 \) Hz
  el GFL es robusto en todo SCR; con \( f_{pll}=100 \) Hz se inestabiliza en red débil
  (SCR crítico ≈3.5). El ancho de banda de la PLL fija el SCR crítico.

## Conceptos relacionados
- [[grid-forming-vs-following]] · [[marco-dq]] · [[no-pasividad-resistencia-negativa]] · [[interaccion-pll-red-debil]]

## Referencias
- Teodorescu et al., *Grid Converters for PV and Wind Power Systems*, 2011.
