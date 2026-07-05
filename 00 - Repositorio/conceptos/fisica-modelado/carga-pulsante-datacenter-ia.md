---
titulo: Carga pulsante de data centers de IA
slug: carga-pulsante-datacenter-ia
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: [03-DataCenter-IA]
objetivos: [modelar la demanda electrica caracteristica de la computacion de IA]
tags: [datacenter, IA, carga-pulsante, RoCoF, microrred, GPU]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-30
relacionados: [dinamica-bus-dc, vsm-inercia]
referencias:
  - "Informes de operadores de red sobre integracion de cargas de data center (2024-2025)"
---

## Definición
La carga eléctrica de un data center de IA tiene un perfil distintivo: **escalones de potencia
grandes, rápidos y sincronizados**. Miles de GPUs entran o salen de un mismo *job* de
entrenamiento casi a la vez, lo que produce saltos de potencia de MW en milisegundos.

## Fundamento teórico
Dos rasgos clave para el sistema de energía:
- **Pulsos sincronizados**: el paralelismo de un entrenamiento hace que las GPUs cambien de estado
  coordinadamente → la demanda agregada salta como un escalón, no de forma suave.
- **Comportamiento de potencia constante**: cada servidor, vía su POL, es una
  [[dinamica-bus-dc|CPL]] en el bus DC.
El escalón de potencia \( \Delta P \) impacta:
- En **frecuencia** (lado AC): impone un RoCoF inicial \( \dfrac{df}{dt}\approx \dfrac{\Delta P\,f_0}{2HS} \),
  que el soporte inercial del BESS ([[vsm-inercia]]) debe limitar.
- En **tensión de bus DC**: hundimiento transitorio que el condensador de bus amortigua, y riesgo
  de inestabilidad si la potencia supera la crítica del filtro ([[dinamica-bus-dc|estabilidad del bus DC con CPL]]).

<div class="cfig"><img src="figuras/carga-pulsante-datacenter-ia-impacto.png" alt="escalon de potencia de un data center de IA y su impacto en frecuencia"><div class="cap">La carga de IA salta como un escalón sincronizado (miles de GPUs entran a un job a la vez). Ese $\Delta P$ impone un RoCoF inicial $\approx\Delta P f_0/(2HS)$ y una caída de frecuencia que el soporte inercial del BESS debe limitar; en el bus DC produce un hundimiento que amortigua el condensador. Es el caso de diseño más exigente.</div></div>

## 1 — De dónde sale el RoCoF \( df/dt\approx\Delta P\,f_0/(2HS) \)
**Paso 1 — ecuación de oscilación (swing).** La inercia de las máquinas (reales o emuladas por el BESS, ver [[vsm-inercia]]) liga el desbalance de potencia con la aceleración del rotor. En por unidad, con constante de inercia \( H \) (segundos) y frecuencia normalizada \( \bar\omega=\omega/\omega_0 \):

$$ 2H\,\frac{d\bar\omega}{dt}=P_m-P_e=-\Delta P_{pu} $$

Un escalón de **carga** \( +\Delta P \) es un \( P_e \) que sube sin que \( P_m \) lo siga: el desbalance \( P_m-P_e=-\Delta P_{pu} \) es negativo y el rotor desacelera.

**Paso 2 — pasar a unidades físicas.** El desbalance en por unidad es \( \Delta P_{pu}=\Delta P/S \) (potencia base = potencia aparente del sistema \( S \)) y la frecuencia física es \( f=f_0\,\bar\omega \), luego \( d\bar\omega/dt=(1/f_0)\,df/dt \). Sustituyendo en el Paso 1:

$$ 2H\,\frac{1}{f_0}\frac{df}{dt}=-\frac{\Delta P}{S} $$

**Paso 3 — despejar el RoCoF inicial.** El instante del escalón es el peor caso (aún no actúa ninguna regulación), de modo que el RoCoF inicial es:

$$ \boxed{\;\frac{df}{dt}=-\frac{\Delta P\,f_0}{2\,H\,S}\;} $$

El signo negativo es el hundimiento de frecuencia ante un escalón de carga; en magnitud, la ficha lo escribe como \( |df/dt|\approx\Delta P f_0/(2HS) \). **Comprobación numérica** (\( \Delta P=130 \) kW, \( f_0=50 \) Hz, \( H=5 \) s, \( S=2 \) MVA): \( df/dt=130000\cdot50/(2\cdot5\cdot2\cdot10^6)\approx0.33 \) Hz/s. Más inercia \( H \) o más potencia base \( S \) → menor RoCoF: por eso el BESS aporta inercia sintética para frenar la caída.

## 2 — Dimensionado del condensador de bus por la caída admisible: \( C=I\,\Delta t/\Delta V \)
**Paso 1 — el condensador cubre el déficit transitorio.** Cuando el pulso \( \Delta P \) golpea el bus DC, la fuente aguas arriba (rectificador, ILC) no puede subir su corriente instantáneamente: tarda un tiempo de respuesta \( \Delta t \). Durante ese intervalo, **todo** el exceso de corriente lo entrega el condensador. De la dinámica del bus (ver [[dinamica-bus-dc]]):

$$ C_{dc}\,\frac{dV_{dc}}{dt}=i_{in}-i_{out}=-\Delta I $$

donde \( \Delta I=\Delta P/V_{dc} \) es el escalón de corriente que la carga demanda de más y que la fuente todavía no cubre.

**Paso 2 — integrar en el intervalo de respuesta.** Suponiendo \( \Delta I \) y \( V_{dc} \) aproximadamente constantes durante \( \Delta t \), la caída de tensión es:

$$ \Delta V=\frac{\Delta I}{C_{dc}}\,\Delta t $$

**Paso 3 — despejar la capacidad mínima.** Imponiendo que la caída no supere un valor admisible \( \Delta V \):

$$ \boxed{\;C_{dc}\ge\frac{\Delta I\,\Delta t}{\Delta V}=\frac{\Delta P\,\Delta t}{V_{dc}\,\Delta V}\;} $$

Cuanto más rápido reacciona la fuente (\( \Delta t \) pequeño) o más caída se tolera (\( \Delta V \) grande), menos condensador hace falta. **Comprobación numérica** (\( \Delta P=130 \) kW, \( V_{dc}=700 \) V → \( \Delta I\approx186 \) A; \( \Delta t=2 \) ms; \( \Delta V=20 \) V): \( C_{dc}\ge186\cdot0.002/20\approx18.6 \) mF. Este criterio por pulso convive con el de rizado y hold-up de [[dinamica-bus-dc]]; se elige el más exigente.

## Cuándo y por qué se usa
Para dimensionar la generación/almacenamiento y el control de la microrred del data center: la
carga pulsante es el caso de diseño más exigente (peor que una carga suave de igual potencia media).

## Procedimiento (genérico)
1. Caracteriza el perfil: potencia media, amplitud del pulso \( \Delta P \), tiempo de subida.
2. Modela el pulso como escalón (peor caso) en P (CPL).
3. Evalúa el impacto en frecuencia (RoCoF, nadir) y en el bus DC (hundimiento, estabilidad).
4. Dimensiona inercia/almacenamiento (AC) y condensador de bus (DC) para los límites admisibles.

## Ejemplo de código
```python
# pico de carga IA como escalon de potencia
P_cpl = lambda t: 100e3 if t < 0.1 else 230e3      # arranque de un job de entrenamiento
```

## Parámetros y valores típicos
Pods de IA de 100 kW–varios MW; saltos \( \Delta P \) de decenas a cientos de kW en ms; RoCoF
admisible de red típico ≈ 0.5–1 Hz/s.

## Errores comunes
- Dimensionar por potencia media e ignorar los pulsos (subdimensiona inercia y bus).
- Tratar la carga como suave: el escalón sincronizado es mucho más exigente.

## Uso en proyectos
- **03 - DataCenter-IA**: un escalón de 100→230 kW se usa como caso de diseño; el soporte inercial
  del BESS limita el RoCoF y el condensador de bus el hundimiento de \( V_{dc} \).

## 3 — Modelo de la carga pulsante

La potencia activa pulsante se expresa como:

$$ p(t) = P_0 + \Delta P \cdot f(t) $$

donde \( P_0 \) es la potencia base del data center y \( f(t) \) es el patrón de carga: escalón unitario en el peor caso, ráfaga rectangular de duración \( t_{burst} \) para un *job* de inferencia, o periódica si los *jobs* se repiten con cadencia fija.

En tiempo discreto, los ciclos de inferencia de IA tienen una correlación directa con la escala temporal: un token de inferencia LLM tarda ~1–5 ms por GPU; un *batch* completo puede durar de decenas de ms a varios segundos; un *job* de entrenamiento puede durar horas con escalones de potencia a la entrada y salida. La consecuencia es que las ráfagas de \( \Delta P \) ocurren en ms a 10 s, justo la banda de respuesta del bus DC y del BESS local.

**Modelo CPL:** cada servidor regula su tensión de entrada con un convertidor POL, comportándose como carga de potencia constante en el bus DC:

$$ i(t) = \frac{p(t)}{v_{bus}(t)} $$

La impedancia de entrada incremental es negativa: \( Z_{CPL} = -v_{bus}^2 / P \). Esto es el origen del amortiguamiento negativo que puede desestabilizar el bus DC.

La perturbación en el bus DC ante un escalón de corriente \( \Delta i_{CPL} \) vale aproximadamente:

$$ \Delta v_{bus} \approx -Z_{bus}(j\omega) \cdot \Delta i_{CPL} $$

donde \( Z_{bus} \) es la impedancia de salida del sistema de alimentación (convertidor + filtro). Si \( |Z_{bus}| \) es elevada a la frecuencia de la perturbación, el hundimiento de tensión es severo.

<div class="cfig"><img src="../figuras/carga-pulsante-datacenter-analisis.png" alt="Análisis de la carga pulsante de data center IA: perfiles, bus DC, Middlebrook y dimensionado BESS"><div class="cap">Cuatro paneles: perfil de potencia con ráfagas de inferencia IA, respuesta de la tensión del bus DC con y sin BESS ante un escalón, criterio de Middlebrook para estabilidad del bus, y energía mínima del BESS en función de la duración de la ráfaga para distintos niveles de $\Delta P$.</div></div>

## 4 — Impacto en el bus DC y estabilidad

La combinación de inductancia de distribución \( L_{bus} \) y CPL forma un circuito LC con **amortiguamiento negativo**: el término de potencia constante introduce una conductancia incremental negativa \( G_{CPL} = -P/V_{bus}^2 \) que, si supera las pérdidas reales del circuito, produce oscilaciones crecientes.

**Criterio de Middlebrook:** el sistema fuente-carga es estable si la impedancia de la fuente es menor que la de la carga en todo el rango de frecuencias:

$$ |Z_{source}(j\omega)| < |Z_{load}(j\omega)| \quad \forall\,\omega $$

Para un bus DC de data center a \( V_{bus} = 380\,\text{V} \) con carga total \( P = 280\,\text{kW} \), la impedancia CPL vale \( |Z_{CPL}| = V_{bus}^2/P \approx 0.52\,\Omega \). Si la impedancia de la fuente supera ese valor a alguna frecuencia, el sistema es inestable.

El condensador de desacoplo mínimo para limitar el \( dv/dt \) máximo admisible \( \dot{v}_{max} \) ante un escalón de potencia \( \Delta P \) es:

$$ C_{dec} = \frac{\Delta P}{v_{bus} \cdot \dot{v}_{max}} $$

Para un data center con \( V_{bus} = 380\,\text{V} \), \( \Delta P \) hasta \( 100\,\text{kW} \) en menos de 1 ms, y un \( \dot{v}_{max} = 5\,\text{kV/s} \): \( C_{dec} \geq 100000 / (380 \times 5000) \approx 52.6\,\text{mF} \).

## 5 — Estrategias de mitigación

El **BESS en el bus DC** es la estrategia más efectiva: absorbe la potencia pulsante \( \Delta P \) y mantiene \( v_{bus} \) dentro del margen admisible. El control de droop de tensión del BESS:

$$ v_{ref} = v_0 - R_d \cdot i_{BESS} $$

donde \( R_d \) es la resistencia de droop virtual (típ. 1–5 % del valor base), permite compartir la carga dinámica entre varios BESS en paralelo de forma proporcional a su capacidad.

El **filtro activo de potencia (APF)** complementa al BESS para las frecuencias más altas: mide \( \Delta i_{CPL} \) e inyecta \( i_{APF} = -\Delta i_{CPL} \) de forma anticipativa, cancelando la perturbación antes de que afecte al bus. El APF es especialmente eficaz para ráfagas de alta frecuencia (> 100 Hz) que el BESS, con su lazo de control más lento, no puede seguir.

La **predicción de carga** cierra el lazo más rápido que cualquier realimentación: el sistema de orquestación del clúster GPU (p. ej. Kubernetes con telemetría de potencia) envía una señal anticipada al controlador del BESS con la referencia de potencia del próximo *batch*, reduciendo el retardo efectivo del lazo de control en un orden de magnitud.

## 6 — Dimensionado del BESS para carga IA

El BESS debe cumplir simultáneamente tres criterios:

**Potencia mínima:** debe poder absorber la variación de potencia más rápida y más grande:

$$ P_{BESS} \geq \Delta P_{max} $$

**Energía mínima:** debe almacenar la energía total de una ráfaga, es decir, el área bajo la curva de potencia pulsante:

$$ E = \int_0^{t_{burst}} \Delta P(t)\,dt $$

Para una ráfaga rectangular de amplitud \( \Delta P \) y duración \( t_{burst} \): \( E = \Delta P \cdot t_{burst} \).

**Tiempo de respuesta:** el lazo de control del BESS debe ser suficientemente rápido para contener el transitorio antes de que la tensión del bus supere el límite. La regla de los tres tiempos de constante requiere:

$$ \tau_{BESS} < \frac{t_{rise,load}}{3} $$

**Ejemplo numérico:** un *batch* de inferencia levanta \( \Delta P = 50\,\text{kW} \) en \( t_{rise} = 2\,\text{ms} \). Entonces:
- \( P_{BESS} \geq 50\,\text{kW} \) (potencia de pico)
- \( E_{BESS} \geq 50000 \times 0.002 = 100\,\text{J} = 27.8\,\mu\text{Wh} \) (ínfimo en kWh, dominante en potencia)
- \( \tau_{BESS} < 0.67\,\text{ms} \) → requiere convertidor DC-DC de alta dinámica (> 1.5 kHz de ancho de banda)

La energía es trivial; la potencia y la dinámica son el verdadero reto de diseño.

## Conceptos relacionados
- [[dinamica-bus-dc|carga de potencia constante (CPL)]] · [[vsm-inercia]]

## Referencias
- Informes de operadores de red sobre integración de data centers (2024-2025).
