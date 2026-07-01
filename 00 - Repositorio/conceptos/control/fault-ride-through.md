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
fecha_actualizacion: 2026-07-01
relacionados: [current-limiting, componentes-simetricas, pll-srf, servicios-red-soporte, droop-control]
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
- Detectar secuencias rápido y limpio (PLL de doble secuencia, [[pll-srf|DSOGI-PLL]]).
- Decidir estrategia de referencia de corriente: inyectar solo secuencia positiva (tensión
  equilibrada del convertidor), o también negativa para soportar/equilibrar, controlando la
  oscilación de potencia de \( 2\omega \) que el desequilibrio induce en el bus DC.
$$ p(t)=P_0+P_{c2}\cos2\omega t+P_{s2}\sin2\omega t $$
Las referencias \( i_{dq}^{\pm*} \) se eligen para anular el rizado de potencia activa **o** de
reactiva (no ambos a la vez), según objetivo.

<div class="cfig"><img src="figuras/fault-ride-through-lvrt.png" alt="envolvente LVRT y curva de inyeccion de reactiva"><div class="cap">Izquierda: envolvente LVRT del grid code; mientras la tensión del PCC quede por encima de la curva, el convertidor no debe desconectar (debe soportar 0 pu durante ~150 ms). Derecha: durante el hueco se prioriza corriente reactiva proporcional a la caída, $\Delta I_q=k\,\Delta V$, saturada a $I_{max}$.</div></div>

## 1 — Derivación de Δiq = k·ΔV/Vn desde el requisito del grid code

**Paso 1 — objetivo normativo.** Durante un hueco de tensión, el grid code exige que el convertidor aporte corriente reactiva para sostener la tensión en el PCC. La norma (p.ej. ENTSO-E RfG, VDE-AR-N 4120) establece que el incremento de corriente reactiva sea proporcional al hueco:

$$ \Delta I_q = k\,\frac{\Delta V}{V_n}, \qquad \Delta V = V_n - V_{pcc} $$

con \( k\ge2 \) p.u./p.u. (al menos 2 A de reactiva por cada 1 p.u. de caída de tensión).

**Paso 2 — sustento físico.** La tensión en el PCC se puede aproximar como \( V_{pcc}\approx V_{grid}-X_{red}\,I_q \) (para red predominantemente inductiva). Un aumento \( \Delta I_q \) en la corriente reactiva produce una subida de tensión \( \Delta V_{pcc}\approx X_{red}\,\Delta I_q \). La pendiente \( k \) establece cuánta reactiva se inyecta por unidad de caída: cuanto mayor \( k \), mayor soporte de tensión, pero también mayor riesgo de sobrepasar \( I_{max} \).

**Paso 3 — límite de corriente.** La corriente total está limitada por la capacidad del puente (\( I_{max} \)), por lo que la corriente reactiva inyectada se satura:

$$ I_q^* = \min\!\left(k\,\Delta V,\; I_{max}\right) $$

y la activa se recorta al valor restante:

$$ I_d^* = \sqrt{\max\!\left(I_{max}^2 - (I_q^*)^2,\;0\right)} $$

**Paso 4 — ejemplo numérico.** Para un hueco \( \Delta V=0.3 \) p.u. y \( k=2 \): \( \Delta I_q=2\times0.3=0.6 \) p.u. Si \( I_{max}=1.0 \) p.u., la activa disponible queda \( I_d^*=\sqrt{1-0.36}=0.8 \) p.u.

$$ \boxed{\Delta I_q = k\,\Delta V,\quad k\ge2\;\text{p.u./p.u.}} $$

## Cuándo y por qué se usa
Obligatorio para conexión a red de PV/eólica/almacenamiento. Crítico en grid-forming, donde además
hay que limitar corriente sin perder la fuente de tensión (transición a modo limitado).

## Procedimiento de diseño (genérico)
1. Toma la curva LVRT/HVRT y la pendiente \( k \) del grid code aplicable.
2. Implementa detección rápida de secuencias ([[pll-srf|DSOGI-PLL]]).
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
- [[current-limiting]] · [[componentes-simetricas]] · [[pll-srf|DSOGI-PLL]] · [[servicios-red-soporte]] · [[droop-control]]

## Referencias
- ENTSO-E, *Requirements for Generators (RfG)*.
- Teodorescu, Liserre, Rodríguez, *Grid Converters for PV and Wind Power Systems*, 2011.
