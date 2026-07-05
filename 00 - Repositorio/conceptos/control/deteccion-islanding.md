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
fecha_actualizacion: 2026-07-01
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

## 1 — ROCOF desde la swing equation

**Paso 1 — ecuación de oscilación (swing equation).** Un generador (o convertidor con inercia virtual) de inercia \( H \) (en segundos) y potencia nominal \( S_n \) obedece:

$$ \frac{2H}{\omega_0}\frac{d\omega}{dt} = P_{mec}-P_{elec} = \Delta P $$

donde \( \omega_0=2\pi f_0 \) es la pulsación nominal y \( \Delta P \) el desequilibrio de potencia (en p.u. sobre \( S_n \)).

**Paso 2 — pasar a variación de frecuencia.** Como \( \omega=2\pi f \), dividiendo por \( 2\pi \):

$$ \frac{2H}{f_0}\frac{df}{dt} = \Delta P $$

Despejando la tasa de cambio de frecuencia:

$$ \boxed{\frac{df}{dt} = \frac{\Delta P\,f_0}{2H}} \quad [\text{Hz/s}] $$

**Paso 3 — interpretar el umbral.** En isla, si la generación excede a la carga en \( \Delta P=0.1 \) p.u., con \( H=5\,\text{s} \) y \( f_0=50\,\text{Hz} \):

$$ \frac{df}{dt}=\frac{0.1\times50}{2\times5}=0.5\,\text{Hz/s} $$

Un umbral típico de ROCOF es \( 0.5\text{–}2\,\text{Hz/s} \). Si el desequilibrio es mayor, el ROCOF supera el umbral antes del tiempo de actuación normativo (< 0.5–2 s).

**Paso 4 — límite de sensibilidad.** En red conectada, la red absorbe o aporta \( \Delta P \) sin cambiar \( f \) (la red tiene inercia efectiva enorme: \( H_{red}\to\infty \)). Al abrir el interruptor toda la inercia disponible se reduce a \( H \) del convertidor → \( df/dt \) salta bruscamente, lo que el ROCOF detecta.

## 3 — Métodos pasivos: OUV/OUF, ROCOF y la zona de no detección (NDZ)

Los métodos pasivos monitorizan parámetros de la red sin perturbar la salida del convertidor. Son los más simples y siempre obligatorios, pero presentan una limitación estructural: la **zona de no detección (NDZ)**.

**OVP/UVP (Over/Under Voltage Protection).** Compara \( |V_{PCC}| \) con umbrales \( V_{max} \) y \( V_{min} \). Si al quedar en isla la potencia reactiva del convertidor coincide con la demanda de la carga (\( \Delta Q \approx 0 \)), la tensión no se mueve y la protección no dispara.

**OFP/UFP (Over/Under Frequency Protection).** Compara \( f \) con umbrales \( f_{max} \) y \( f_{min} \). Si la potencia activa del convertidor coincide con la demanda (\( \Delta P \approx 0 \)), la frecuencia no se desvía y la protección no dispara.

**ROCOF (Rate of Change of Frequency).** Mide \( df/dt \). Al desconectarse la red, la inercia disponible cae de \( H_{red} \to \infty \) a \( H \) del convertidor (finita), y el ROCOF salta bruscamente. El umbral típico es \( |df/dt| > 0.5\text{–}2\,\text{Hz/s} \).

**La NDZ: la región donde ningún método pasivo funciona.** Si al quedar en isla se cumple simultáneamente \( |\Delta P| < \epsilon_P \) y \( |\Delta Q| < \epsilon_Q \) (la generación casi iguala la carga en \( P \) y \( Q \)), entonces:
- \( \Delta P \approx 0 \Rightarrow df/dt \approx 0 \) y \( f \) no sale del rango: OFP y ROCOF no disparan.
- \( \Delta Q \approx 0 \Rightarrow |V| \) no cambia: OVP no dispara.

La NDZ es el rectángulo \( |\Delta P/P_{carga}| < \epsilon_P \) y \( |\Delta Q/Q_{carga}| < \epsilon_Q \) en el plano de desbalance de potencia. Su tamaño depende de los umbrales normativos: umbrales más amplios implican NDZ más grande.

**ROCOF: sensibilidad vs falsas alarmas.** El umbral de ROCOF es un compromiso:
- Umbral bajo (\( <0.5\,\text{Hz/s} \)): detecta islanding rápido pero puede disparar falsamente durante eventos de red (pérdida de una línea, reconexión de cargas grandes) que también causan ROCOF transitorio.
- Umbral alto (\( >2\,\text{Hz/s} \)): inmune a eventos de red pero puede no detectar islanding cuando \( \Delta P \) es pequeño.

## 4 — Métodos activos: AFD y SMS

Los métodos activos perturban intencionadamente la salida del convertidor para escapar de la NDZ.

**AFD (Active Frequency Drift / Sandia Frequency Shift, SFS).** Se añade una pequeña desviación de frecuencia \( \Delta f_{inj} \) proporcional a la desviación de frecuencia medida, con retroalimentación positiva:

$$ f_{ref}(t) = f_0 + k_{SFS} \cdot (f_{medida} - f_0) $$

- **En red conectada:** la red tiene inercia enorme y absorbe la perturbación sin que \( f \) se desvíe: \( f_{medida} \approx f_0 \) siempre, la retroalimentación positiva no se amplifica y el impacto sobre la calidad de potencia es mínimo.
- **En isla:** sin la red que "ancle" la frecuencia, la retroalimentación positiva amplifica cualquier pequeño desvío de \( f \). La frecuencia deriva rápidamente hacia afuera del rango \( [f_{min}, f_{max}] \) y la protección OFP dispara, incluso cuando \( \Delta P \approx 0 \).

La ganancia \( k_{SFS} \) debe elegirse lo suficientemente alta para detectar rápido, pero lo suficientemente baja para no distorsionar la calidad de potencia en red.

**SMS (Slip Mode Frequency Shift).** Variante que desplaza la fase de la tensión de referencia cuando la frecuencia se desvía, creando una aceleración acumulativa en isla. Más efectivo que el AFD puro pero con mayor impacto en THD.

**Inyección de reactiva perturbada (RPE).** Se inyecta periódicamente un pulso de \( Q \) para producir una variación de \( |V| \) en isla, detectable con OVP/UVP incluso dentro de la NDZ en \( \Delta Q \).

## 5 — El ROCOF desde la swing equation: umbral y tiempo de detección

**La ecuación de oscilación (swing equation)** para un convertidor o generador con inercia \( H \):

$$ \frac{2H}{\omega_0}\frac{d\omega}{dt} = \Delta P \quad\Rightarrow\quad \frac{df}{dt} = \frac{\Delta P \cdot f_0}{2H} $$

donde \( \Delta P = P_{gen} - P_{carga} \) (en pu sobre \( S_n \)), \( f_0 \) es la frecuencia nominal y \( H \) la constante de inercia en segundos.

**Tiempo hasta salir del rango.** Si el ROCOF es aproximadamente constante para \( \Delta P \) pequeño:

$$ t_{det} = \frac{\Delta f_{max}}{|df/dt|} = \frac{\Delta f_{max} \cdot 2H}{\Delta P \cdot f_0} $$

donde \( \Delta f_{max} \) es la distancia desde la frecuencia nominal hasta el umbral de OFP.

**Relación entre ROCOF y inercia.** Un GFM con inercia virtual grande (\( H \) grande) tiene ROCOF más lento: más robusto frente a perturbaciones de red pero más lento para detectar islanding. Un GFL sin inercia (\( H \to 0 \)) tiene ROCOF instantáneo: detecta islanding muy rápido pero también puede disparar falsamente ante escalones de carga.

## 6 — Diseño iterativo: GFM del proyecto 01 (1MVA, H=5s)

Parámetros: \( S_n = 1\,\text{MVA} \), \( H = 5\,\text{s} \), \( f_0 = 50\,\text{Hz} \), carga en isla \( P_{carga} = 0.9\,\text{pu} \), \( P_{gen} = 0.9\,\text{pu} + \Delta P \).

**Paso 1 — ROCOF esperado para un desequilibrio típico de \( \Delta P = 0.1\,\text{pu} \).**

$$ \frac{df}{dt} = \frac{0.1 \times 50}{2 \times 5} = \frac{5}{10} = 0.5\,\text{Hz/s} $$

Un desequilibrio del 10% de la potencia nominal produce exactamente el ROCOF umbral típico: la detección ocurre en \( t \to \infty \) para este caso límite. Para \( \Delta P = 0.2\,\text{pu} \), \( df/dt = 1\,\text{Hz/s} \) y se detecta rápidamente.

**Paso 2 — tiempo hasta que f sale del rango ±0.5 Hz.**

Con rango \( f \in [49.5, 50.5]\,\text{Hz} \) y ROCOF \( = 0.5\,\text{Hz/s} \):

$$ t_{out} = \frac{0.5\,\text{Hz}}{0.5\,\text{Hz/s}} = 1\,\text{s} $$

Con ROCOF = 1 Hz/s (\( \Delta P = 0.2\,\text{pu} \)): \( t_{out} = 0.5\,\text{s} \). Ambos dentro del límite normativo < 2 s.

**Paso 3 — verificar detección < 2 s para la peor NDZ.**

La peor NDZ es cuando \( \Delta P \to 0 \). Para \( \Delta P = 0.05\,\text{pu} \), \( df/dt = 0.25\,\text{Hz/s} \): tiempo para salir de ±0.5 Hz es \( t = 2\,\text{s} \), en el límite. Se recomienda añadir AFD con \( k_{SFS} = 0.05 \) para empujar la frecuencia hacia afuera de la NDZ cuando \( \Delta P < 0.05\,\text{pu} \).

**Paso 4 — selección del umbral ROCOF.**

Umbral de ROCOF = 0.5 Hz/s: detecta \( \Delta P \geq 0.1\,\text{pu} \) en ≤ 1 s. Para eventos de red típicos en esta red (pérdida de línea: ROCOF < 0.3 Hz/s durante < 100 ms), el umbral de 0.5 Hz/s no dispara falsamente si se exige que el ROCOF supere el umbral durante al menos 200 ms (filtro de ventana temporal).

<div class="cfig"><img src="../figuras/deteccion-islanding-analisis.png" alt="Detección de islanding: NDZ, ROCOF, AFD y trade-off de umbral"><div class="cap">(a) Zona de no detección (NDZ) en el plano ΔP-ΔQ: dentro de la caja, OFP/OVP no disparan. (b) f(t) ante islanding: sin detección la frecuencia se estabiliza en la isla; con ROCOF dispara a 200 ms. (c) AFD: en isla la frecuencia escapa del rango; en red, se absorbe la perturbación. (d) Trade-off umbral ROCOF: umbral bajo = detección rápida pero más falsas alarmas.</div></div>

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

## 7 — Métodos pasivos: OVP/UVP, OFP/UFP y ROCOF — zona de no detección

Los métodos pasivos monitorizan las variables eléctricas en el PCC y disparan cuando superan umbrales:

| Método | Señal | Umbral típico | NDZ |
|---|---|---|---|
| OVP/UVP | \|V\| en PCC | ±10–20% de \(V_n\) | \(\Delta P \approx 0\), \(\Delta Q \approx 0\) |
| OFP/UFP | Frecuencia PCC | ±0.5–1 Hz de \(f_n\) | Potencia/reactiva equilibrada |
| ROCOF | \(df/dt\) | > 0.5 Hz/s | \(\Delta P < 0.1\,\text{pu}\) |
| Vector shift | Salto de fase | > 6–12° | \(\Delta P \approx 0\) |

La **zona de no detección (NDZ)** es el conjunto de condiciones (\(\Delta P\), \(\Delta Q\)) para las que ningún método pasivo detecta el islanding. Para OFP/UFP con umbral ±0.5 Hz, la NDZ se extiende hasta el par (\(P_{carga}/P_{gen} \in [0.95,1.05]\), \(Q_{carga}/Q_{gen}=0\)): un desequilibrio de carga del 5% puede no detectarse.

<div class="cfig"><img src="../figuras/deteccion-islanding-analisis.png" alt="Detección de islanding: NDZ, frecuencia, ROCOF y secuencia detección-reconexión"><div class="cap">(a) Zona de no detección (NDZ) en el plano P-Q normalizado para OFP/UFP ±0.5 Hz. (b) Evolución de frecuencia en operación normal vs islanding con carga desequilibrada. (c) ROCOF comparado: islanding real vs perturbación de red (trip de línea). (d) Secuencia temporal detección → apertura → espera → resincronización → cierre.</div></div>

## 8 — Métodos activos: AFD, SFS y umbral de inyección reactiva

Los métodos activos perturban deliberadamente el punto de operación para crear una condición detectable:

**AFD (Active Frequency Drift):** distorsiona ligeramente la forma de onda de corriente para crear un pequeño desvío de frecuencia en isla. En red conectada, la red "ancla" la frecuencia y la perturbación es absorbida sin desvío. En isla, la frecuencia se desplaza y activa OFP.

**SFS (Sandia Frequency Shift):** realimenta positivamente el desvío de frecuencia: si \(f > f_0\), aumenta el ángulo de la corriente para empujar la frecuencia más arriba, saliendo de la NDZ en < 100 ms.

**Inyección de corriente reactiva:** periódicamente inyectar un pulso de \(Q\) y medir si la tensión cambia. En red conectada \(\Delta V \approx 0\); en isla \(\Delta V = Q\,X_{carga}\) → detectable.

**Umbral de activación:** para no perturbar la calidad de energía en operación normal, la perturbación inyectada debe ser < 1% de la corriente nominal. El SFS con \(k_{SFS} = 0.05\) genera un desvío de frecuencia de \(\approx 0.5\,\text{Hz/s}\) en isla.

## 9 — Protección remota: transfer trip e IEEE 1547-2018

Los métodos locales (pasivos + activos) tienen NDZ residual. La **protección remota** elimina la NDZ:

**Transfer trip:** la subestación de distribución envía una señal de apertura directa a todos los inversores GFL/GFM del alimentador cuando detecta apertura del interruptor principal. Tiempo de comunicación: < 20 ms (fibra óptica o PLC). Costo: infraestructura de comunicación.

**Relé de sincronía 25:** verifica \(|\Delta V| < 0.1\,\text{pu}\), \(|\Delta f| < 0.1\,\text{Hz}\), \(|\Delta\theta| < 10°\) antes de cerrar el interruptor. Evita la reconexión fuera de sincronismo.

**IEEE 1547-2018:** requiere que los DER:
- Cesen de energizar la red en < 2 s al detectar islanding
- Implementen al menos un método activo para reducir la NDZ
- Cumplan la secuencia de reconexión (espera mínima de 5 minutos para < 1 MVA o ajuste del SO)

## 10 — Reconexión: condiciones y secuencia

La reconexión tras un islanding detectado sigue la secuencia:

1. **Detección:** método activo/pasivo dispara → apertura del interruptor del PCC.
2. **Espera:** mínimo 300 ms para sistemas pequeños; hasta 5 minutos si hay duda sobre el estado de la red.
3. **Verificación de sincronismo:** relé 25 comprueba \(|\Delta V| < 0.05\,\text{pu}\), \(|\Delta f| < 0.1\,\text{Hz}\), \(|\Delta\theta| < 20°\).
4. **Cierre suave:** GFM entra en modo "resincronización" reduciendo la velocidad del integrador del ángulo hasta alinear con la red; GFL activa el PLL con rampa de fase.
5. **Restablecimiento:** retorno al modo normal de operación.

**Transición bumpless:** el GFM debe igualar el estado del integrador de ángulo antes del cierre para evitar un escalón de fase → pico de corriente. Se logra inicializando el integrador del VSM/droop con el ángulo medido en el PCC.

## 11 — Métodos pasivos detallados: OVP/UVP, OFP/UFP y ROCOF

**OVP/UVP:** dispara cuando \(|V_{PCC}|\notin[0.88,\,1.1]\) pu. Tiempo de actuación < 100 ms. Es la protección más sencilla, presente en cualquier inversor de red; su NDZ es amplia porque si \(\Delta Q \approx 0\) la tensión no se mueve al aislar.

**OFP/UFP:** dispara cuando \(f\notin[49.5,\,50.5]\) Hz. Eficaz si la carga no balancea exactamente la generación activa (\(\Delta P \neq 0\)), pero ineficaz dentro de la NDZ (\(\Delta P \approx 0\)).

**ROCOF:** \(|df/dt|>0.5\,\text{Hz/s}\) típico. Más rápido que OFP/UFP porque detecta el cambio brusco de inercia disponible al abrir el disyuntor de red; sin embargo, es propenso a falsos positivos ante perturbaciones bruscas de la red (pérdida de línea, reconexión de cargas grandes) que también producen ROCOF transitorio sin islanding real.

**Zona de no-detección (NDZ):** cuando la carga local equilibra exactamente la generación (\(\Delta P \approx 0\) y \(\Delta Q \approx 0\)), ningún método pasivo detecta el islanding porque ni la frecuencia ni la tensión se desvían de sus umbrales normativos. El tamaño de la NDZ crece con umbrales más amplios.

## 12 — Métodos activos detallados: AFD, SFS e inyección reactiva

**AFD (Active Frequency Drift):** el inversor introduce un sesgo de frecuencia en la corriente inyectada. En red conectada la red absorbe la perturbación; en isla, sin referencia de frecuencia externa, la frecuencia se aleja del nominal y activa OFP. Elimina una parte significativa de la NDZ.

**SFS (Sandia Frequency Shift):** retroalimentación positiva del error de frecuencia:
$$f_{ref}(t) = f_0 + k_{SFS}\,(f_{meas} - f_0)$$
En isla, cualquier pequeño desvío de \(f\) se amplifica hasta salir del rango en <100 ms. Elimina la NDZ; la ganancia \(k_{SFS}\) debe limitarse (típicamente 0.05) para no degradar la calidad de potencia.

**Inyección de perturbación reactiva periódica:** varía \(i_q\) de forma conocida (pulso de Q de 5–10% cada 100 ms). En isla, la tensión varía de forma distinta a la de red (\(\Delta V = Q \cdot X_{carga}\)); en red conectada \(\Delta V \approx 0\). Ventaja: elimina la NDZ. Desventaja: degrada la calidad de potencia e introduce interacción entre múltiples inversores con perturbaciones superpuestas.

## 13 — Protección remota: transfer trip e IEEE 1547-2018

**Transfer trip:** cuando el disyuntor de red abre, la subestación envía una señal de disparo directa a todos los inversores del alimentador (fibra óptica o PLC, latencia < 20 ms). Elimina completamente la NDZ; su debilidad es que depende de la integridad de la infraestructura de comunicación.

**IEEE 1547-2018** exige:
- Cesar de energizar la red en < 2 s para toda la NDZ.
- Implementar al menos un método activo (AFD, SFS o similar).
- Cumplir la secuencia de reconexión con espera mínima de 300 ms (o según SO).

**Condición de reconexión (relé 25 de sincronía):** \(|\Delta V|<0.1\,\text{pu}\), \(|\Delta f|<0.1\,\text{Hz}\), \(|\Delta\theta|<20°\); espera mínima 300 ms tras restablecer la tensión de red.

**Secuencia completa:** detección → disparo del interruptor de PCC → espera obligatoria → verificación de condiciones \(\Delta V\), \(\Delta f\), \(\Delta\theta\) → reconexión suave (GFM en modo resincronización o GFL con rampa de PLL).

<div class="cfig"><img src="../figuras/deteccion-islanding-analisis.png" alt="NDZ, ROCOF, frecuencia islanding y secuencia detección-reconexión"><div class="cap">(a) Zona de no-detección (NDZ) en el plano ΔP-ΔQ: dentro de la región roja ningún método pasivo dispara. (b) Frecuencia normal vs islanding con carga desequilibrada. (c) ROCOF: islanding real supera el umbral en <0.5 s; perturbación de red produce un pico transitorio que se extingue. (d) Secuencia temporal detección → apertura → espera → verificación → reconexión suave.</div></div>

## Conceptos relacionados
- [[pll-srf]] · [[fault-ride-through]] · [[servicios-red-soporte]] · [[calidad-potencia]] · [[power-synchronization-control]] · [[current-limiting]] · [[grid-forming-vs-following]]

## Referencias
- IEEE Std 1547-2018, *Standard for Interconnection and Interoperability of DER*.
- Mahat et al., *A Hybrid Islanding Detection Technique*, IEEE TPEL 2011.
