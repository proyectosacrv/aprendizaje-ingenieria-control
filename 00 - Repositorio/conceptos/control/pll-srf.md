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
fecha_actualizacion: 2026-06-11
relacionados: [grid-forming-vs-following, marco-dq, no-pasividad-resistencia-negativa, interaccion-pll-red-debil]
referencias:
  - "Kaura, Blasko, Operation of a Phase Locked Loop System Under Distorted Utility Conditions, IEEE TIA 1997"
  - "Teodorescu et al., Grid Converters for PV and Wind Power Systems, Wiley 2011"
---

## Definición
La **SRF-PLL** (Synchronous Reference Frame PLL) estima el ángulo y la frecuencia de la tensión de red
alineando el marco dq con dicha tensión: lleva la componente **q** a cero. Es el bloque de
sincronización del grid-following.

## Diagrama de bloques
Park con el ángulo estimado → \( v_q \) → PI → suma \( \omega_0 \) → integrador → \( \theta_{pll} \),
que realimenta a la Park:

<div class="cfig"><img src="figuras/pll-srf-bloques.png" alt="diagrama de bloques de la SRF-PLL"><div class="cap">Lazo de la SRF-PLL: el PI ajusta la frecuencia para llevar vq a cero; el integrador genera el ángulo θpll, que cierra el lazo realimentando la transformada de Park.</div></div>

## Fundamento teórico — de dónde se sale
Se mide la tensión y se pasa a dq con el ángulo **estimado** \( \theta_{pll} \). Si el error de ángulo
es \( \Delta\theta=\theta-\theta_{pll} \), la componente q vale \( v_q=V\sin(\Delta\theta)\approx
V\,\Delta\theta \) para error pequeño. El PI lleva \( v_q\to0 \) ajustando la frecuencia:
$$ \omega_{pll}=\omega_0+K_p\,v_q+K_i\!\int v_q,\qquad \dot\theta_{pll}=\omega_{pll} $$

**Linealización (lazo de 2º orden).** Con \( v_q\approx V\,\Delta\theta \) y
\( \dot{\Delta\theta}=\omega-\omega_{pll} \), el lazo cerrado tiene la ecuación característica:
$$ s^2+K_p V\,s+K_i V=0\;\;\Longrightarrow\;\;
   \boxed{\;\omega_n=\sqrt{K_i V}\,,\qquad \zeta=\frac{K_p V}{2\,\omega_n}\;} $$
El **ancho de banda** de la PLL es \( \approx\omega_n \). Es el parámetro que gobierna la robustez
frente a la red.

> **A resaltar:** una PLL **rápida** (ωn alto) sincroniza antes pero **interactúa con la impedancia de
> la red débil** y puede inestabilizar (resistencia negativa de la PLL, ver
> [[no-pasividad-resistencia-negativa]] y [[interaccion-pll-red-debil]]). El ancho de banda de la PLL
> fija el SCR crítico.

## Cuándo y por qué se usa
En todo inversor grid-following (PV, eólica GFL) y en cualquier control que necesite el ángulo de red.
No se usa en grid-forming (que genera su propio ángulo).

## Procedimiento de diseño (genérico)
1. Fija el ancho de banda \( f_{pll} \): compromiso entre rapidez (rechazo de huecos, saltos) y
   **robustez** (una PLL rápida se desestabiliza en red débil). Típico 10–50 Hz.
2. Con \( \zeta\approx0.707 \): \( K_i=\omega_n^2/V \), \( K_p=2\zeta\omega_n/V \) (normaliza por la
   amplitud \( V \) de la tensión).
3. Si la red tiene armónicos/desequilibrio, añade prefiltros (DSOGI, notch) o usa una variante
   (DDSRF, SOGI-PLL).
4. Verifica la interacción con la red en el rango de SCR esperado.

## Ejemplo de código
```python
wn = 2*np.pi*f_pll
Ki = wn**2 / V0;  Kp = 2*zeta*wn / V0
# v_q es la componente q de la tension medida en el marco de la PLL
w_pll = w0 + Kp*v_q + Ki*eps
d_eps = v_q                # integrador
d_theta = w_pll            # angulo estimado
```

## Parámetros y valores típicos
\( f_{pll} \) 10–50 Hz (robusta); >80–100 Hz ya es "rápida" y arriesgada en red débil.
\( \zeta\approx0.707 \).

## Errores comunes
- **PLL demasiado rápida** "para sincronizar mejor": desestabiliza en red débil (el gran pitfall del GFL).
- No normalizar por la amplitud \( V \) → ganancias dependientes del punto de operación.
- Ignorar armónicos/desequilibrio → ángulo con rizado.

## Uso en proyectos
- **02 - GFL-Impedance** (objetivo: sincronizar): SRF-PLL sobre \( v_C \). Con \( f_{pll}=30 \) Hz el
  GFL es robusto en todo SCR; con \( f_{pll}=100 \) Hz se inestabiliza en red débil (SCR crítico ≈3.5).

## Conceptos relacionados
- [[grid-forming-vs-following]] · [[marco-dq]] · [[no-pasividad-resistencia-negativa]] · [[interaccion-pll-red-debil]]

## Referencias
- Teodorescu et al., *Grid Converters for PV and Wind Power Systems*, 2011.
