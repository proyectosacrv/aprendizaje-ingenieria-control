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
relacionados: [pll-srf, fault-ride-through, servicios-red-soporte, calidad-potencia]
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

## Transición automática GFL → GFM (bumpless transfer)
Cuando se detecta islanding y la desconexión de la red es intencionada (microrred que entra en isla),
la detección dispara un cambio de modo de **grid-following a grid-forming**. La clave es la
**transferencia sin golpe** (*bumpless transfer*): evitar escalones en la corriente y la tensión.

### Estados que se transfieren
Al momento de la detección (\(t=t_{det}\)):
1. **Ángulo inicial del GFM** \(\theta_0 = \theta_{PLL}(t_{det})\): el GFM hereda el ángulo de la
   PLL para no crear un escalón de fase en la tensión de salida.
2. **Integradores del lazo de corriente**: se precargan con las salidas actuales del modulador
   (cero error inicial).
3. **Referencia de tensión del lazo externo**: se inicializa a la tensión medida en PCC en ese instante.
4. **Referencia de potencia del droop**: se parte de \(P^*\) igual a la potencia medida antes del
   evento, para no hacer un escalón de potencia al arrancar el GFM.

### Lógica de modo
```
GFL_ACTIVE → (detección islanding) → TRANSICION → GFM_ACTIVE
                                         ↑
                            freeze PLL + precargar estados GFM
```
En el modo `TRANSICION` (típico 1–2 ciclos = 20–40 ms): se congela la PLL, se precarga el GFM y
se abre el interruptor de red. El GFM arranca con los estados ya inicializados; el PCC no ve
discontinuidad de tensión.

### Re-sincronización para reconexión (GFM → GFL)
Al recuperar la red, antes de cerrar el interruptor:
1. Medir el ángulo de red con DSOGI-PLL ([[pll-srf|DSOGI-PLL]]).
2. Sincronizar el ángulo del GFM al de la red (lazo de sincronización lento, similar al PSC
   [[power-synchronization-control]]) hasta que \(|\Delta\theta| < 5°\) y \(|\Delta f| < 0.1\,\text{Hz}\).
3. Cerrar el interruptor; volver a modo GFL; descongelar PLL.

## Ejemplo de código
```python
def rocof_islanding(f_hist, dt, thresh=0.5):   # Hz/s
    if len(f_hist) < 2: return False
    rocof = (f_hist[-1] - f_hist[-2]) / dt
    return abs(rocof) > thresh                  # True = island detectado

def bumpless_gfl_to_gfm(state_gfl):
    """Inicializa el estado del GFM a partir del estado GFL en el instante de detección."""
    theta0   = state_gfl['theta_pll']           # hereda el angulo PLL
    Vref_dq  = state_gfl['vpcc_dq']             # tensión medida como referencia inicial
    xi_i_d   = state_gfl['xi_id']               # integradores del lazo de corriente
    xi_i_q   = state_gfl['xi_iq']
    P0       = state_gfl['P_meas']              # potencia inicial del droop
    return dict(theta=theta0, Vref=Vref_dq, xi_id=xi_i_d, xi_iq=xi_i_q, P_droop=P0)
```

## Parámetros y valores típicos
OUF: 47–52 Hz (EN 50549); OUV: 0.85–1.10 p.u.; ROCOF: 0.5–2 Hz/s; tiempo < 0.5–2 s según normativa.
NDZ de OUF/OUV ≈ zona donde generación ≈ carga con Q≈0. Tiempo de transición GFL→GFM: 20–40 ms
(1–2 ciclos). Umbral de re-sincronización: \(|\Delta\theta|<5°\), \(|\Delta f|<0.1\,\text{Hz}\).

## Errores comunes
- Umbrales de ROCOF demasiado sensibles → falso disparo durante faltas de red que no son islanding.
- Grid-forming sin método activo → sostiene la isla dentro de los umbrales pasivos indefinidamente.
- No coordinar FRT y anti-islanding (el FRT bloquea el disparo durante el hueco; al despejar puede
  haber islanding real).
- **No hacer bumpless transfer**: arrancar el GFM con ángulo cero cuando la red estaba en \(\theta\neq0\)
  produce un escalón de fase → pico de corriente que puede disparar el current limiting.
- **Reconectar sin re-sincronizar**: cerrar el interruptor con \(\Delta\theta\) grande genera una
  corriente de igualación impulsiva (similar a sincronizar un generador fuera de fase).

## Conceptos relacionados
- [[pll-srf]] · [[fault-ride-through]] · [[servicios-red-soporte]] · [[calidad-potencia]] · [[power-synchronization-control]] · [[current-limiting]] · [[grid-forming-vs-following]]

## Referencias
- IEEE Std 1547-2018, *Standard for Interconnection and Interoperability of DER*.
- Mahat et al., *A Hybrid Islanding Detection Technique*, IEEE TPEL 2011.
