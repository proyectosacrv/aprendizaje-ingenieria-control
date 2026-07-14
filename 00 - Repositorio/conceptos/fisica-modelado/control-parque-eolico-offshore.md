---
titulo: Control de parque eólico offshore
slug: control-parque-eolico-offshore
categoria: fisica-modelado
tipo: concepto
nivel: avanzado
proyectos: []
objetivos: [entender la arquitectura de control de un parque eólico offshore conectado por HVDC]
tags: [parque-eolico, offshore, hvdc, wpp, wpc, agc, despacho, wake-effect, mppt-colectivo, black-start]
fecha_creacion: 2026-07-08
fecha_actualizacion: 2026-07-08
relacionados: [eolica-mppt, aerogenerador-pmsg-dfig, hvdc-vsc-topologia, hvdc-control-potencia, servicios-red-soporte]
referencias:
  - "Zhao et al., Power System Support Functions Provided by Wind Power Plants, CIGRE 2013"
  - "Sørensen et al., Wind Farm Models and Control Strategies, Risø DTU 2011"
  - "IEC 61400-25: Communications for Monitoring and Control of Wind Power Plants"
---

## Definición
Un **parque eólico offshore** (WPP, Wind Power Plant) conectado a tierra mediante HVDC-VSC es un sistema multinivel: los aerogeneradores generan en 33 kV, una subestación offshore eleva a 155–220 kV AC, el terminal HVDC convierte a ±320 kV DC y el cable submarino transmite la potencia hasta la red onshore. El **control del parque** coordina estos niveles para maximizar la producción, cumplir las consignas del TSO, proporcionar servicios de red y gestionar contingencias (FRT, black start). La arquitectura jerárquica de control abarca desde el lazo de par del aerogenerador individual (milisegundos) hasta el despacho económico del operador (minutos).

## Fundamento teórico

**Efecto estela (wake effect).** La velocidad del viento en la estela de un aerogenerador, según el modelo de Jensen:

$$v_{wake}(x) = v_\infty\!\left(1 - \frac{2a}{\left(1 + \alpha\,x/r_0\right)^2}\right)$$

donde \( a \) es el factor de inducción axial (~0.33 para MPPT), \( \alpha \) el coeficiente de expansión de la estela (~0.04 en mar abierto), \( x \) la distancia aguas abajo y \( r_0 \) el radio del rotor. La velocidad en la estela puede ser un 5–15 % menor que la velocidad libre, con efecto acumulativo en filas sucesivas.

**Potencia del parque.** Con \( N \) aerogeneradores, la potencia total:

$$P_{park} = \sum_{i=1}^{N} P_{wt,i}(v_{i}) = \sum_{i=1}^{N} \frac{1}{2}\rho\pi R^2 C_p(\lambda_i,\beta_i)\,v_i^3$$

donde \( v_i \) es la velocidad efectiva sobre cada aerogenerador \( i \), que depende de la posición relativa y el efecto estela de los aerogeneradores upstream.

**Control de frecuencia por enlace HVDC.** La respuesta de frecuencia del parque sobre la red onshore:

$$\Delta P_{HVDC} = -\frac{1}{R_f}\Delta f - 2H_{park}\frac{d\Delta f}{dt}$$

El primer término es el droop (regulación primaria); el segundo es la inercia sintética. \( R_f \) es la ganancia de caída de frecuencia (típicamente 2–5 %) y \( H_{park} \) la constante de inercia equivalente del parque (3–6 s según el nivel de derating).

<div class="cfig"><img src="../figuras/control-parque-eolico-offshore-analisis.png" alt="Control de parque eólico offshore"><div class="cap">Layout del parque con efecto estela (color = P/Pnom), respuesta FRT basada en frecuencia de la red del parque, curvas de despacho MPPT vs delta-control con reserva de regulación, y servicios de red FFR y droop por el enlace HVDC.</div></div>

## 1 — Arquitectura del sistema: del aerogenerador al PCC onshore

La cadena completa de un parque eólico offshore con conexión HVDC:

<div class="cfig"><img src="../figuras/parque-offshore-cadena.png" alt="Cadena eléctrica del parque offshore: aerogeneradores, subestación offshore, terminal HVDC offshore, cable submarino DC, terminal HVDC onshore, PCC y red continental, con sus niveles de control"><div class="cap">Cadena completa desde los aerogeneradores (33 kV inter-array) hasta la red de transmisión continental, pasando por la subestación offshore, los dos terminales HVDC MMC-VSC unidos por el cable submarino DC y el PCC onshore. A la derecha, el nivel de control asociado a cada etapa (del MPPT local al TSO/AGC).</div></div>

**Niveles de control y escalas de tiempo:**

- **Nivel 0 (aerogenerador individual, 1–100 ms):** lazo de par y corriente del convertidor, MPPT local, control de pitch, FRT individual. El aerogenerador recibe una consigna de potencia activa y reactiva del nivel 1 y la ejecuta con sus propios lazos de control.

- **Nivel 1 (WPC — Wind Power Controller, 100 ms–10 s):** recibe la consigna global del TSO \( P_{ref}^{park} \), la distribuye entre aerogeneradores minimizando el efecto estela, gestiona los límites de rampa, ejecuta el delta-control (reserva de regulación) y supervisa la tensión en los nodos de la red inter-array.

- **Nivel 2 (HVDC, 10 ms–1 s):** control del enlace DC (tensión del bus DC, corriente DC), FRT del parque, FFR (Fast Frequency Response), sincronización con la red onshore. El terminal offshore actúa en modo GFM para los aerogeneradores; el onshore actúa en modo GFL hacia la red continental (o GFM si la red es débil).

- **Nivel 3 (AGC/TSO, 1 s–varios minutos):** consignas de potencia activa, reserva de frecuencia, banda de regulación. Comunicación SCADA según IEC 61400-25. El TSO puede ordenar una reducción de potencia (curtailment) por congestión de red o exceso de generación.

**Topología de la red inter-array.** Los aerogeneradores se conectan en strings de 6–10 unidades a 33 kV. Las strings convergen en la subestación offshore. La topología estándar es radial; topologías en anillo o malladas están estudiadas para alta disponibilidad pero su coste adicional rara vez se justifica.

**Dimensionado del enlace HVDC.** Para un parque de 1 GW a 500 km:

$$I_{dc} = \frac{P_{park}}{2V_{dc}} = \frac{1000\,\text{MW}}{2 \times 320\,\text{kV}} = 1563\,\text{A}$$

Las pérdidas del cable (resistencia típica 0.015 Ω/km por polo):

$$\Delta P_{cable} = 2 \times I_{dc}^2 \times R_{cable} = 2 \times 1563^2 \times 0.015 \times 500 = 36.6\,\text{MW} \approx 3.7\,\%$$

Este nivel de pérdidas, sumado a las pérdidas del MMC (~1 % por terminal), hace que la eficiencia total del enlace sea ~94–96 %, competitiva frente al 90–92 % de un cable AC a 500 km (que además requiere compensación reactiva shunt).

## 2 — Terminal HVDC offshore: modo GFM para los aerogeneradores

El terminal HVDC offshore crea la red AC del parque: es el **único elemento grid-forming** en la red inter-array. Los aerogeneradores operan en modo GFL (grid-following), sincronizándose con la referencia de tensión y frecuencia que impone el terminal HVDC.

**Función de formación de red.** El MMC offshore mantiene:
- \( V_{OSS} = 1.00\,\text{pu} \) en las barras de la subestación offshore
- \( f_{OSS} = 50.00\,\text{Hz} \) (referencia para los PLLs de los aerogeneradores)

El control del terminal offshore no necesita PLL: la frecuencia la genera él mismo con un oscilador interno de referencia. Implementa un control de tensión con droop en caso de múltiples terminales offshore (configuración multiterminal).

**Arranque del parque (energización de la red inter-array).** El terminal offshore realiza la pre-carga de los transformadores y cables AC del parque antes de que los aerogeneradores se conecten, evitando corrientes de irrupción excesivas. El procedimiento: rampa de tensión desde 0 hasta 1 pu en ~5 s, luego conexión secuencial de los aerogeneradores.

**Balance de potencia reactiva en la red inter-array.** Los cables submarinos de 33 kV generan potencia reactiva capacitiva. Para un cable de 33 kV, 20 km de longitud y 40 MVA de capacidad:

$$Q_C = B_C\,V^2 = \omega\,C_{km}\,l\,V^2 \approx 0.25\,\text{MVAR/km} \times 20\,\text{km} = 5\,\text{MVAR}$$

Esta potencia reactiva debe ser absorbida por los aerogeneradores o el terminal HVDC para evitar sobretensiones en condiciones de baja carga (viento bajo).

## 3 — Despacho de potencia activa (Active Power Dispatch)

El WPC (Wind Power Controller) recibe la consigna de potencia total \( P_{ref}^{park} \) del TSO y la distribuye entre los \( N \) aerogeneradores. Los objetivos son:

1. **Minimizar el efecto estela** — reducir la potencia de los aerogeneradores delanteros para que los traseros reciban más viento
2. **Mantener la reserva de regulación** — dejar un margen por encima de la producción actual para poder aumentar la potencia ante una caída de frecuencia
3. **Equilibrar el desgaste** — distribuir la producción para igualar las horas de funcionamiento y la fatiga de los componentes

**Delta-control (curtailment absoluto).** Todos los aerogeneradores operan a \( P_{ref} = P_{mppt} - \Delta P \), donde \( \Delta P \) es la reserva de regulación. Ventajas: sencillez, respuesta rápida (todos pueden aumentar simultáneamente). Inconveniente: pérdida de energía igual en todos los aerogeneradores, independientemente de su posición en el parque.

**Balance control (curtailment selectivo).** Los aerogeneradores delanteros (primera fila) operan en derating: producen menos del MPPT para reducir el déficit de velocidad en la estela, aumentando la producción de las filas traseras. El WPC resuelve un problema de optimización:

$$\max_{P_1,\ldots,P_N} \sum_{i=1}^N P_i \quad \text{sujeto a} \quad \sum P_i = P_{ref}^{park},\quad 0 \leq P_i \leq P_{mppt,i}$$

En condiciones de viento homogéneo y alineado con las filas, el balance control puede aumentar la producción total del parque un 1–3 % respecto al delta-control.

**Limitación de rampa.** El TSO impone una tasa máxima de cambio de potencia (ramp rate), típicamente 10 % \( P_{nom} \)/min. El WPC filtra la consigna recibida para no superar este límite, lo que evita sobretensiones en la red de transporte causadas por escalones bruscos de potencia.

**Derating por temperatura.** Los aerogeneradores con temperatura elevada en el generador o el convertidor reciben una consigna reducida para limitar el estrés térmico. El WPC tiene acceso a los datos SCADA de temperatura de cada aerogenerador (IEC 61400-25) y ajusta la distribución en tiempo real.

## 4 — Control de frecuencia y servicios de red

El enlace HVDC permite al parque offshore proporcionar servicios de frecuencia a la red onshore con tiempos de respuesta inalcanzables para grupos generadores convencionales:

**FFR (Fast Frequency Response, <500 ms).** El terminal HVDC onshore detecta la desviación de frecuencia \( \Delta f \) mediante la medida local de la frecuencia de la red. Antes de que los aerogeneradores individuales respondan, el terminal onshore puede aumentar instantáneamente la corriente DC extraída del bus DC, aumentando la potencia inyectada a la red. La fuente de energía es el bus DC (energía almacenada en la capacidad del bus) y la inercia cinética de los aerogeneradores. La respuesta:

$$\Delta P_{FFR}(t) = -K_{FFR}\,\Delta f(t) \quad \text{para } |\Delta f| > \Delta f_{dead}$$

con \( K_{FFR} \) la ganancia de respuesta rápida y \( \Delta f_{dead} \approx 0.05\,\text{Hz} \) la banda muerta.

**Inercia sintética (inertia emulation).** El parque emula la respuesta inercial de un generador síncrono convencional:

$$\Delta P_{inertia} = -2H_{park}\frac{d\Delta f}{dt}$$

La constante de inercia equivalente \( H_{park} \) se puede ajustar entre 0 y el valor limitado por la energía cinética disponible en los rotores de los aerogeneradores. Para no reducir \( \omega_r \) por debajo del mínimo operacional (~0.7 pu), la inercia sintética solo puede actuar durante 5–15 s antes de que los aerogeneradores deban reducir la extracción de energía cinética para volver a la velocidad óptima MPPT.

**Droop de frecuencia (regulación primaria).** El parque actúa como generador con caída de frecuencia:

$$\Delta P_{droop} = -\frac{P_{nom}}{R_f\,\Delta f_{nom}}\Delta f$$

Para \( R_f = 0.04 \) (4 %) y \( \Delta f_{nom} = 0.5\,\text{Hz} \): un \( \Delta f = 0.25\,\text{Hz} \) provoca \( \Delta P = P_{nom}/0.04 \times 0.25/0.5 = 12.5\,\%\,P_{nom} \). Esto requiere una reserva previa (delta-control al 90 % del MPPT, reservando el 10 % para la regulación al alza).

**Control de tensión en el PCC.** El terminal HVDC onshore puede controlar la tensión en el PCC inyectando o absorbiendo potencia reactiva dentro de los límites de la capacidad del MMC. Para un MMC de 1000 MVA:

$$Q_{max} = \sqrt{S_{nom}^2 - P_{park}^2}$$

A plena potencia activa \( P_{park} = 1000\,\text{MW} \), no hay margen para reactiva. A \( P_{park} = 800\,\text{MW} \): \( Q_{max} = \sqrt{1000^2-800^2} = 600\,\text{MVAR} \). El TSO puede exigir un perfil de potencia reactiva según la hora del día y el estado de la red.

## 5 — FRT del parque offshore: frequency-based FRT

Cuando se produce un hueco de tensión en la red onshore, el terminal HVDC onshore no puede inyectar la potencia normal porque \( P_{out} \propto V_{red}^2 \) (para un MMC en modo GFL). El bus DC sube porque \( P_{in} \) (del parque) supera \( P_{out} \) (a la red). La estrategia **frequency-based FRT** coordina la respuesta sin necesidad de comunicación directa entre el terminal offshore y cada aerogenerador:

**Paso 1 — detección del hueco por el terminal offshore.** El terminal offshore monitoriza continuamente la tensión del bus DC \( V_{dc} \). Cuando \( V_{dc} > V_{dc,th} \) (umbral de sobretensión, típicamente 1.05 pu), deduce que hay un desequilibrio \( P_{in} > P_{out} \) (causado por un hueco onshore o por un fallo del cable).

**Paso 2 — señalización por frecuencia.** El terminal offshore reduce la frecuencia de la red del parque según:

$$f_{park} = f_0 - k_{dc}(V_{dc} - V_{dc,0})$$

con \( k_{dc} \approx 10\,\text{Hz/pu} \) (ganancia de la señalización). Para \( V_{dc} = 1.10\,\text{pu} \): \( f_{park} = 50 - 10 \times 0.10 = 49\,\text{Hz} \).

**Paso 3 — respuesta de los aerogeneradores.** Los aerogeneradores operan en modo GFL con PLL. Al detectar la bajada de frecuencia, el control MPPT interpreta que la velocidad de giro está por encima del óptimo y reduce la potencia de referencia. En modo delta-control, los aerogeneradores responden con droop de frecuencia, reduciendo \( P \) en proporción a \( \Delta f \).

**Paso 4 — disipación del exceso en el chopper.** Mientras la frecuencia del parque cae y los aerogeneradores reducen potencia, el exceso transitorio de energía en el bus DC se disipa en el **braking resistor** del bus DC (chopper). Dimensionado del chopper:

$$P_{chopper} \geq P_{park,max} - P_{HVDC,min,FRT}$$

Para un parque de 1 GW con FRT al 20 % de tensión (\( P_{HVDC} = 0.04\,P_{nom} = 40\,\text{MW} \)):

$$P_{chopper} \geq 1000 - 40 = 960\,\text{MW}$$

En la práctica, el chopper se dimensiona para la potencia máxima del parque (1 pu) durante 150–200 ms.

**Paso 5 — recuperación post-falta.** Cuando la tensión onshore se recupera, \( P_{out} \) aumenta, \( V_{dc} \) vuelve a nominal, la frecuencia del parque sube de vuelta a 50 Hz y los aerogeneradores recuperan gradualmente su producción MPPT. La tasa de recuperación se limita para evitar una sobrecarga súbita de la red onshore (second dip).

## 6 — Black start y operación en isla

**Black start del enlace HVDC.** En caso de fallo total de la red onshore, el parque puede restaurar el enlace sin alimentación externa:

**Secuencia de black start (tiempo de arranque: 20–40 min):**

1. **Pre-carga del bus DC (t = 0–2 min).** El terminal HVDC onshore dispone de una batería de arranque (o UPS) que pre-carga el bus DC a través de resistencias limitadoras. No se necesita la red onshore en este paso.

2. **Arranque del MMC offshore (t = 2–5 min).** El terminal offshore, con el bus DC pre-cargado, arranca en modo GFM y crea la red AC del parque con tensión y frecuencia nominales. Los transformadores de la subestación offshore se energizan con rampa de tensión controlada.

3. **Conexión de aerogeneradores (t = 5–20 min).** Los aerogeneradores se conectan en secuencia (grupos de 3–5), aumentando gradualmente la potencia. El terminal onshore ajusta la corriente DC extraída para mantener \( V_{dc} \) constante mientras la red onshore aún no está disponible.

4. **Sincronización con la red onshore (t = 20–40 min).** El terminal onshore sincroniza la salida AC del MMC con la red onshore (verificación de tensión, frecuencia y ángulo de fase) y cierra el disyuntor de conexión. El parque pasa a modo normal de operación.

**Operación en isla (islanded mode).** Si la red onshore falla pero el enlace HVDC permanece operativo (por ejemplo, el fallo está en el transformador onshore), el terminal HVDC offshore puede alimentar cargas locales offshore:

- Plataformas de compresión o procesado de gas
- Subestaciones de producción offshore
- Instalaciones de alojamiento del personal

En este modo, el terminal offshore actúa como generador GFM para las cargas; los aerogeneradores se regulan para igualar la carga + pérdidas. El reto es el balance de potencia: si el viento varía, los aerogeneradores deben ajustar la producción rápidamente para evitar colapsos de frecuencia. El pitch control actúa como regulador principal de frecuencia en isla.

**Requisitos de grid code para black start.** El código de red de algunos TSOs (por ejemplo, National Grid ESO en UK) ya requiere capacidad de black start para parques offshore de nueva construcción conectados por HVDC de >500 MW. El coste estimado de la función de black start representa el 0.5–1.5 % del CAPEX del parque.
