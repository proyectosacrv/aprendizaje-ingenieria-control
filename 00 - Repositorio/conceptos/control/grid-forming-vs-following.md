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
fecha_actualizacion: 2026-06-08
relacionados: [droop-control, vsm-inercia, impedancia-salida-estabilidad, red-thevenin-scr, pll-srf, interaccion-pll-red-debil]
referencias:
  - "Rocabert et al., Control of Power Converters in AC Microgrids, IEEE TPEL 2012"
  - "Lin et al., Research Roadmap on Grid-Forming Inverters, NREL 2020"
---

## Definición
Dos filosofías de control de un inversor conectado a red. El **grid-following (GFL)** se
sincroniza con la red (PLL) e **inyecta corriente**. El **grid-forming (GFM)** **impone una
tensión** con su propia frecuencia y ángulo, como una fuente de tensión detrás de una impedancia.

## Fundamento teórico
- **GFL**: fuente de corriente controlada; depende de una PLL para conocer el ángulo de red.
  Su estabilidad se degrada en **red débil** (SCR bajo), porque la PLL y el lazo de corriente
  interactúan con la alta impedancia de red.
- **GFM**: fuente de tensión; el ángulo lo genera el propio control (droop/VSM), **sin PLL**.
  Aporta inercia/soporte y es robusto en red débil. Su impedancia de salida es **inductiva**
  en banda media (firma de fuente de tensión), igual que una máquina síncrona.

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
