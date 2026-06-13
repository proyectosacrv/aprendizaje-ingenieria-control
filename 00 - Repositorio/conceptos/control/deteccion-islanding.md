---
titulo: Detección de islanding (anti-islanding)
slug: deteccion-islanding
categoria: control
tipo: tecnica
nivel: intermedio
proyectos: []
objetivos: [detectar la separación de la red y desconectar el convertidor en tiempo normativo]
tags: [islanding, anti-islanding, deteccion, OUF, OUV, NDZ, grid-code, intermedio]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-09
relacionados: [pll-srf, dsogi-pll, fault-ride-through, servicios-red-soporte, calidad-potencia]
referencias:
  - "IEEE Std 1547-2018, Standard for Interconnection and Interoperability of DER"
  - "Mahat et al., A Hybrid Islanding Detection Technique, IEEE TPEL 2011"
---

## Definición
Conjunto de métodos que detectan que un convertidor distribuido ha quedado operando en una
**isla** (separado de la red principal) y lo desconectan dentro del tiempo exigido por la normativa
(típicamente < 2 s), evitando riesgos para el personal de mantenimiento y el equipamiento.

## Fundamento teórico
Cuando la red se desconecta, la isla puede quedar con potencia generada ≈ carga (coincidencia de P y Q),
por lo que la tensión y frecuencia permanecen dentro de límites durante un tiempo → **zona de no
detección (NDZ)**. Los métodos se clasifican en:

**Pasivos** (monitorizan parámetros de red):
- **OUF/OUV** (Over/Under Frequency/Voltage): umbrales normativos. Rápido pero con NDZ amplia.
- **ROCOF** (Rate of Change of Frequency): \( df/dt \) supera un umbral al desconectar la red.
  Sensible pero puede disparar falsamente en eventos de red (falta lejana).
- **Cambio de fase / vector shift**: salto de ángulo al perder la red; rápido, pero sensible a
  faltas y conmutación de cargas grandes.

**Activos** (perturban intencionadamente la salida):
- **Positive Feedback / Sandia Frequency Shift (SFS):** se añade una perturbación de frecuencia
  proporcional al ROCOF; en isla la frecuencia escapa rápidamente del rango → detección. En red
  fuerte la red absorbe la perturbación; en isla se amplifica.
- **Reactive Power Export (RPE):** inyección de Q perturbación; produce desvíos de tensión en isla.
- **Impedance Measurement:** inyecta un tono de prueba y mide la impedancia de red; sube mucho al
  aislar. Exacto pero más complejo y puede añadir distorsión.

**Comunicación** (más robusta):
- **SCADA/Teleprotección:** la apertura del interruptor envía una señal directa al inversor. Sin NDZ;
  depende de comunicaciones (falla si el enlace falla).

Compromiso: los métodos activos reducen la NDZ pero degradan la calidad de potencia; en
**grid-forming** la detección es más difícil porque el convertidor sostiene tensión/frecuencia
incluso en isla.

<div class="cfig"><img src="figuras/deteccion-islanding-ndz.png" alt="zona de no deteccion en el plano de desbalance de potencia"><div class="cap">Zona de no detección (NDZ): si al quedar en isla la generación casi iguala a la carga ($\Delta P\approx0$, $\Delta Q\approx0$), la tensión y la frecuencia permanecen dentro de umbrales y los métodos pasivos OUF/OUV no disparan. Los métodos activos perturban la salida para empujar el punto fuera de esta caja.</div></div>

## Cuándo y por qué se usa
Obligatorio por normativa (IEEE 1547, IEC 62116, VDE-AR-N 4105) para toda generación distribuida
conectada a red pública. Especialmente crítico en instalaciones con [[servicios-red-soporte|FRT y
inercia sintética]] que pueden mantener la isla activa más tiempo.

## Procedimiento de diseño (genérico)
1. Comprueba los umbrales normativos del grid code aplicable (OUF/OUV, ROCOF, tiempo de actuación).
2. Implementa métodos pasivos como primera línea (OUF/OUV + ROCOF/phase-jump).
3. Añade un método activo (SFS) para reducir NDZ si la normativa lo exige.
4. Coordina con [[fault-ride-through|FRT]]: durante un hueco no disparar anti-islanding; al despejar
   la falta, re-sincronizar ([[pll-srf]]) antes de reconectar.
5. Valida con escenarios de NDZ (carga resonante balanceada) y con perturbaciones de red que no
   deben causar falso disparo.

## Ejemplo de código
```python
def rocof_islanding(f_hist, dt, thresh=0.5):   # Hz/s
    if len(f_hist) < 2: return False
    rocof = (f_hist[-1] - f_hist[-2]) / dt
    return abs(rocof) > thresh                  # True = island detectado
```

## Parámetros y valores típicos
OUF: 47–52 Hz (EN 50549); OUV: 0.85–1.10 p.u.; ROCOF: 0.5–2 Hz/s; tiempo < 0.5–2 s según normativa.
NDZ de OUF/OUV ≈ zona donde generación ≈ carga con Q≈0.

## Errores comunes
- Umbrales de ROCOF demasiado sensibles → falso disparo durante faltas de red que no son islanding.
- Grid-forming sin método activo → sostiene la isla dentro de los umbrales pasivos indefinidamente.
- No coordinar FRT y anti-islanding (el FRT bloquea el disparo durante el hueco; al despejar puede
  haber islanding real).

## Conceptos relacionados
- [[pll-srf]] · [[dsogi-pll]] · [[fault-ride-through]] · [[servicios-red-soporte]] · [[calidad-potencia]]

## Referencias
- IEEE Std 1547-2018, *Standard for Interconnection and Interoperability of DER*.
- Mahat et al., *A Hybrid Islanding Detection Technique*, IEEE TPEL 2011.
