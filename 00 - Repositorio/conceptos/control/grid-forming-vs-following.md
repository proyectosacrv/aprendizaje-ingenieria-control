---
titulo: Grid-forming vs grid-following
slug: grid-forming-vs-following
categoria: control
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [elegir la arquitectura de control del inversor]
tags: [grid-forming, grid-following, PLL, red-debil, SCR]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-30
relacionados: [droop-control, vsm-inercia, impedancia-salida-estabilidad, red-thevenin-scr, pll-srf, interaccion-pll-red-debil]
referencias:
  - "Rocabert et al., Control of Power Converters in AC Microgrids, IEEE TPEL 2012"
  - "Lin et al., Research Roadmap on Grid-Forming Inverters, NREL 2020"
---

## Definición
Dos filosofías de control de un inversor conectado a red. El **grid-following (GFL)** se
sincroniza con la red (PLL) e **inyecta corriente**. El **grid-forming (GFM)** **impone una
tensión** con su propia frecuencia y ángulo, como una fuente de tensión detrás de una impedancia.

<div class="cfig"><img src="figuras/grid-forming-vs-following-comparativa.png" alt="comparativa GFM vs GFL"><div class="cap">GFM se comporta como una fuente de tensión tras una impedancia (impone V y f, genera su ángulo); GFL como una fuente de corriente que sigue el ángulo de la PLL. Esa diferencia explica su robustez opuesta frente a la red.</div></div>

## Fundamento teórico
- **GFL**: fuente de corriente controlada; depende de una PLL para conocer el ángulo de red.
  Su estabilidad se degrada en **red débil** (SCR bajo), porque la PLL y el lazo de corriente
  interactúan con la alta impedancia de red.
- **GFM**: fuente de tensión; el ángulo lo genera el propio control (droop/VSM), **sin PLL**.
  Aporta inercia/soporte y es robusto en red débil. Su impedancia de salida es **inductiva**
  en banda media (firma de fuente de tensión), igual que una máquina síncrona.

## 1 — Por qué la fuente de corriente (GFL) sufre en red débil y la de tensión (GFM) no
**Paso 1 — los dos equivalentes.** Cada filosofía es un equivalente de Thévenin/Norton distinto detrás de la impedancia de red \( Z_{red} \):
- **GFL** = fuente de **corriente** \( I \) (Norton, impedancia interna idealmente \( \infty \)): impone la corriente que inyecta y deja que la red fije la tensión del PCC.
- **GFM** = fuente de **tensión** \( E \) detrás de una impedancia interna \( Z_o \) pequeña (Thévenin): impone la tensión y deja que la red fije la corriente.

**Paso 2 — sensibilidad de la tensión del PCC en el GFL.** Con la fuente de corriente \( I \) inyectando contra la red \( V_g \) detrás de \( Z_{red} \), la tensión del nudo es
$$ V_{pcc}=V_g+Z_{red}\,I\;\Longrightarrow\;\frac{\partial V_{pcc}}{\partial I}=Z_{red} $$
La tensión que mide la PLL depende de \( Z_{red} \). En **red débil** \( |Z_{red}| \) es grande (SCR bajo): cada pequeño cambio de corriente mueve mucho \( V_{pcc} \). La PLL reacciona a ese movimiento corrigiendo el ángulo, lo que cambia \( I \), que vuelve a mover \( V_{pcc} \) — el lazo PLL–red se cierra con ganancia \( \propto Z_{red} \) y se desestabiliza (ver [[interaccion-pll-red-debil]]). Cuanto más débil la red, más alta la ganancia de ese lazo.

**Paso 3 — sensibilidad de la corriente en el GFM.** Con la fuente de tensión \( E \) detrás de \( Z_o \), la corriente que circula a la red es
$$ I=\frac{E-V_g}{Z_o+Z_{red}}\;\Longrightarrow\;\frac{\partial I}{\partial E}=\frac{1}{Z_o+Z_{red}} $$
Aquí \( Z_{red} \) está en el **denominador**: una red débil (\( |Z_{red}| \) grande) **reduce** la sensibilidad de la corriente a la tensión impuesta. El GFM no necesita medir el ángulo de la red —lo genera él (droop/VSM)— así que no hay lazo de medida que la impedancia alta pueda desestabilizar. Es robusto justo donde el GFL falla.

**Paso 4 — el espejo.** El mismo cociente explica el caso opuesto: en **red fuerte** (\( Z_{red}\to0 \)), \( \partial I/\partial E\to1/Z_o \) es grande, así que un GFM con droop **agresivo** (lazo de potencia de banda ancha) puede inestabilizar en red fuerte — el espejo exacto del GFL. Cada arquitectura es robusta en el extremo donde la otra falla; la elección la decide el SCR esperado ([[red-thevenin-scr]]).

## Cuándo y por qué se usa
- **GFL**: redes fuertes, plantas que solo "siguen" la red (la mayoría del parque PV actual).
- **GFM**: alta penetración renovable, microrredes, operación en isla, redes débiles. Es la
  tendencia para mantener estabilidad cuando hay pocos generadores síncronos.

## Procedimiento de diseño (genérico)
1. Estima el **SCR** del punto de conexión (ver [[red-thevenin-scr]]).
2. SCR alto y solo aportar energía → GFL (más simple).
3. SCR bajo, soporte de red, isla → GFM (droop o VSM) + [[impedancia-virtual]].
4. Comprueba estabilidad por impedancia: GFL tiende a inestabilizar en red débil; GFM, si el
   control es agresivo, en red **fuerte** (ver [[impedancia-salida-estabilidad]]).

## Ejemplo de código
```python
# GFM: el angulo lo fija el control, no una PLL
w = w0 + mp*(Pset - Pm)      # frecuencia propia (droop)
theta += w*dt                # integra su propio angulo
# GFL seria: theta = PLL(v_red); i* = control_corriente(P*,Q*)
```

## Parámetros y valores típicos
SCR: red fuerte > 10, débil < 3. X/R de red: 2–10 (transmisión más inductiva).

## Errores comunes
- Usar GFL en red muy débil → oscilaciones por la PLL.
- Asumir que GFM es estable siempre: con droop agresivo puede inestabilizar en red **fuerte**
  (lo opuesto al GFL).

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: arquitectura): se eligió GFM con droop. En Fase 3 se vio
  que el GFM bien amortiguado es estable en todo el rango de SCR; el caso crítico (SCR≈3.35)
  solo aparece con control agresivo y en red fuerte.

## Conceptos relacionados
- [[droop-control]] · [[vsm-inercia]] · [[impedancia-salida-estabilidad]] · [[red-thevenin-scr]]

## Referencias
- Lin et al., *Research Roadmap on Grid-Forming Inverters*, NREL 2020.
