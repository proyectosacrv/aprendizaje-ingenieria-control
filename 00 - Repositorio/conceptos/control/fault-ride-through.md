---
titulo: Fault ride-through (LVRT/HVRT) e inyección de reactiva
slug: fault-ride-through
categoria: control
tipo: tecnica
nivel: avanzado
proyectos: []
objetivos: [mantener el convertidor conectado durante huecos y dar soporte de tensión]
tags: [frt, lvrt, hvrt, hueco-tension, reactiva, grid-code, desequilibrio, avanzado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-09
relacionados: [current-limiting, componentes-simetricas, dsogi-pll, servicios-red-soporte, droop-control]
referencias:
  - "ENTSO-E, Requirements for Generators (RfG) / Network Codes"
  - "Teodorescu, Liserre, Rodríguez, Grid Converters for PV and Wind Power Systems, Wiley 2011"
---

## Definición
Capacidad —exigida por los grid codes— de un convertidor de **permanecer conectado** durante un
hueco (LVRT) o sobretensión (HVRT) de red y, además, **inyectar corriente reactiva** para sostener
la tensión durante la falta.

## Fundamento teórico
**Curva de tensión-tiempo.** El código define una envolvente \( V(t) \): por encima de la curva el
convertidor no debe desconectar (p.ej. soportar 0 p.u. durante 150–250 ms). HVRT es la envolvente
superior simétrica.

**Inyección de reactiva.** Durante el hueco se prioriza corriente reactiva según una pendiente
\( k \) (típ. \( k\ge2 \)):
$$ \Delta I_q = k\,\Delta V \quad (\text{p.u.}),\qquad \Delta V = 1-V_{pcc} $$
con \( I_q \) saturada a \( I_{max} \). La activa se recorta para respetar el límite de corriente
([[current-limiting]]).

**Faltas asimétricas.** La mayoría de huecos son desequilibrados → aparece **secuencia negativa**
([[componentes-simetricas]]). Hay que:
- Detectar secuencias rápido y limpio (PLL de doble secuencia, [[dsogi-pll]]).
- Decidir estrategia de referencia de corriente: inyectar solo secuencia positiva (tensión
  equilibrada del convertidor), o también negativa para soportar/equilibrar, controlando la
  oscilación de potencia de \( 2\omega \) que el desequilibrio induce en el bus DC.
$$ p(t)=P_0+P_{c2}\cos2\omega t+P_{s2}\sin2\omega t $$
Las referencias \( i_{dq}^{\pm*} \) se eligen para anular el rizado de potencia activa **o** de
reactiva (no ambos a la vez), según objetivo.

## Cuándo y por qué se usa
Obligatorio para conexión a red de PV/eólica/almacenamiento. Crítico en grid-forming, donde además
hay que limitar corriente sin perder la fuente de tensión (transición a modo limitado).

## Procedimiento de diseño (genérico)
1. Toma la curva LVRT/HVRT y la pendiente \( k \) del grid code aplicable.
2. Implementa detección rápida de secuencias ([[dsogi-pll]]).
3. Genera referencias \( i_{dq}^{\pm*} \) priorizando reactiva, con la estrategia de rizado elegida.
4. Aplica [[current-limiting]] con prioridad a \( I_q \) y anti-windup.
5. Gestiona el bus DC durante la falta (chopper/recorte de activa) y la **recuperación** post-falta.
6. Valida con huecos simétricos y asimétricos a distintas profundidades.

## Ejemplo de código
```python
def frt_refs(Vpcc, Imax, k=2.0):
    dV = 1.0 - Vpcc
    iq = min(k*dV, Imax)                 # reactiva prioritaria (p.u.)
    id_ = (max(Imax**2 - iq**2, 0.0))**0.5  # activa con la corriente restante
    return id_, iq
```

## Parámetros y valores típicos
LVRT: soportar 0 p.u. durante 150–250 ms; pendiente \( k=2\text{–}6 \). Tiempo de respuesta de
reactiva < 30–60 ms. Límite de corriente 1.0–1.2 p.u.

## Errores comunes
- Detección de secuencia lenta → respuesta de reactiva tardía y disparo por sobrecorriente.
- Saturar corriente sin prioridad clara → ni soporta tensión ni protege el puente.
- Olvidar el rizado de \( 2\omega \) en el bus DC durante faltas asimétricas.
- No gestionar la **recuperación** (sobretensión/sobrecorriente al despejar la falta).

## Conceptos relacionados
- [[current-limiting]] · [[componentes-simetricas]] · [[dsogi-pll]] · [[servicios-red-soporte]] · [[droop-control]]

## Referencias
- ENTSO-E, *Requirements for Generators (RfG)*.
- Teodorescu, Liserre, Rodríguez, *Grid Converters for PV and Wind Power Systems*, 2011.
