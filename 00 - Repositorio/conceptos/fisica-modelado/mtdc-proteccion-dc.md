---
titulo: MTDC y protección DC
slug: mtdc-proteccion-dc
categoria: fisica-modelado
tipo: concepto
nivel: avanzado
proyectos: []
objetivos: [entender la arquitectura MTDC, el droop DC, la dinámica de falta y los métodos de protección]
tags: [mtdc, hvdc, proteccion-dc, dccb, interruptor-dc, falta-dc, droop-dc, offshore]
fecha_creacion: 2026-07-08
fecha_actualizacion: 2026-07-08
relacionados: [hvdc-vsc-topologia, hvdc-cable-dc, hvdc-control-potencia]
referencias:
  - "Hertem, Gomis-Bellmunt, Liang, HVDC Grids: For Offshore and Supergrid of the Future, Wiley 2016"
  - "Beerten, Cole, Belmans, Generalized Steady-State VSC MTDC Model, IEEE TPWRS 2012"
---

## Definición

Red HVDC Multi-Terminal DC (MTDC): tres o más terminales VSC conectados a la misma infraestructura de cable DC. El control del bus DC requiere coordinación entre terminales, y la protección ante faltas en el cable DC es el principal desafío técnico que distingue al MTDC del punto a punto.

## 1 — Motivación del MTDC

**¿Por qué más de dos terminales?** Los enlaces HVDC punto a punto (dos terminales) no aprovechan la infraestructura del cable cuando hay múltiples fuentes y cargas que interconectar. El MTDC añade terminales VSC al mismo bus DC con tres ventajas fundamentales:

- **Redundancia:** si un terminal falla, los demás redistribuyen la potencia automáticamente. En un enlace punto a punto, el fallo de un terminal corta toda la transferencia.
- **Coste marginal decreciente por terminal:** el cable ya existe; añadir un terminal solo cuesta la subestación VSC, sin duplicar la infraestructura de cable.
- **Integración multirecurso:** parques eólicos offshore, baterías (BESS), interconexiones nacionales y cargas pueden compartir el mismo bus DC, optimizando el despacho global.

**Aplicaciones reales:**
- *Parques eólicos offshore:* el North Sea Wind Power Hub conecta 10–15 GW de eólica de varios países a una red DC común.
- *Interconexiones nacionales:* el proyecto IberDrola-RTE en el Golfo de Vizcaya utiliza un cable HVDC compartido con posibilidad de derivaciones MTDC.
- *BESS distribuidos:* distintos puntos de almacenamiento conectados al mismo bus DC permiten gestión centralizada de la carga/descarga.

**Topologías de red DC:**

- **Radial (árbol):** cada nodo está conectado por un único camino al resto. Simple, bajo coste, pero sin redundancia: un fallo de cable aísla la rama completa.
- **Mallada (con bucles):** existen múltiples caminos entre cualquier par de nodos. Mayor redundancia y flexibilidad de despacho, pero mayor complejidad de protección (la corriente de falta puede circular por varios caminos).

<div class="cfig"><img src="../figuras/mtdc-proteccion-dc-analisis.png" alt="MTDC: droop DC, corriente de falta, comparativa de protección y topologías"><div class="cap">Panel superior izquierdo: curvas droop DC para tres terminales MTDC — el punto de operación es la intersección de las tres rectas con la condición de balance de potencia. Superior derecho: corriente de falta bipolar DC desde el instante de la falta hasta la apertura del DCCB (5 ms). Inferior izquierdo: comparativa cuantitativa de los métodos de protección. Inferior derecho: esquemas de topología radial y mallada.</div></div>

## 2 — Droop de tensión DC para MTDC

**El problema del control centralizado.** Si un único terminal controla \( V_{dc} \) (modo *slack*), actúa como referencia absoluta. Si ese terminal falla, el bus DC pierde su referencia de tensión y colapsa en décimas de segundo. En un sistema con \( N \geq 3 \) terminales, este diseño no es admisible.

**Solución: droop de tensión DC.** Cada terminal \( i \) implementa una característica P-V:

$$ P_i = P_{0,i} + k_{d,i}(V_{dc} - V_{dc,0}) $$

donde \( P_{0,i} \) es la consigna de potencia nominal, \( V_{dc,0} \) es la tensión de referencia (igual para todos), y \( k_{d,i} \) [MW/kV] es el coeficiente de droop. Esta ecuación es equivalente a colocar una **conductancia virtual** \( G_{d,i} = k_{d,i} \) entre el bus DC y el punto de consigna de potencia.

**Reparto de la regulación.** Ante una perturbación \( \Delta P_{carga} \), la variación de tensión se reparte entre los terminales proporcional a su droop:

$$ \Delta V_{dc} = -\frac{\Delta P_{carga}}{\sum_i k_{d,i}}, \qquad \Delta P_i = k_{d,i} \Delta V_{dc} $$

El terminal con mayor \( k_d \) absorbe más variación de potencia. Si \( k_d \to \infty \) para un terminal, ese terminal actúa como el *slack* clásico (control de tensión puro, sin caída).

**Comunicación requerida.** El droop primario no necesita comunicación: cada terminal mide localmente \( V_{dc} \) y ajusta su potencia según la característica. El control secundario (restauración de \( V_{dc} \) al valor nominal tras la perturbación) sí puede requerir comunicación entre terminales para calcular la corrección global.

**Consideración de diseño.** Un droop grande \( k_d \) hace que el terminal sea un buen regulador de tensión (variación pequeña de \( V_{dc} \) ante perturbaciones) pero puede provocar cambios bruscos de potencia. Un droop pequeño limita la variación de potencia pero deja \( V_{dc} \) oscilar más. El diseño equilibra ambos requisitos según la rigidez requerida del bus DC.

## 3 — Falta DC: dinámica y peligro

**Tipo de falta.** La falta bipolar (cortocircuito entre el polo positivo y el polo negativo del cable HVDC) es la más severa. Las fases del transitorio son:

1. **Descarga de condensadores:** los condensadores de los submódulos (SMs) del MMC se descargan hacia el punto de falta a través de la inductancia del cable. La corriente sube con tasa:

$$ \frac{di}{dt} \approx \frac{V_{dc}}{L_{cable}} $$

Para \( V_{dc} = 640\,\text{kV} \) y \( L_{cable} = 0.12\,\text{H} \), la tasa inicial es \( \approx 5.3\,\text{MA/s} \). En 1 ms la corriente supera 5 kA.

2. **Alimentación desde la red AC:** una vez que los condensadores se descargan, la corriente de falta es alimentada desde la red AC a través de los diodos de roue libre del MMC de semipuente (HB-MMC). Esta componente no se puede bloquear sin submódulos de puente completo (FB-SM).

3. **Pico de corriente:** la corriente de falta puede alcanzar **10–20 pu** en menos de **10 ms**. Los IGBTs toleran sobreintensidades de 2–3 pu durante máximo 10 µs antes del fallo por sobretemperatura o latchup.

**Tiempo de detección.** Los relés de distancia DC detectan la falta en **1–2 ms** midiendo la derivada de \( V_{dc} \) y la derivada de \( I_{dc} \) (protección basada en la onda viajera). El tiempo de eliminación total (detección + apertura del interruptor) debe ser inferior a **5 ms** para proteger los IGBTs.

**Por qué la protección AC no es suficiente.** Los disyuntores AC convencionales interrumpen la corriente en el cruce por cero (cada 10 ms en 50 Hz). Para aislar una falta DC, el disyuntor AC debe esperar el cruce por cero, lo que puede tardar hasta 10 ms adicionales — demasiado para los IGBTs. Además, la corriente de falta DC continúa fluyendo desde la red AC mientras el disyuntor AC no abra.

## 4 — Interruptores DC (DCCB)

**El reto fundamental.** En AC, la corriente cruza por cero naturalmente dos veces por período (a 50 Hz, cada 10 ms), lo que facilita la interrupción. En DC, no hay cruce por cero: el interruptor debe crear activamente las condiciones para extinguir el arco y disipar la energía almacenada en la inductancia del cable.

**Tecnologías de DCCB:**

| Tecnología | Tiempo apertura | Pérdidas nominales | Coste relativo |
|---|---|---|---|
| Mecánico (vacío) | 30–100 ms | Mínimas | Bajo |
| Híbrido (semiconductor + mecánico) | 2–5 ms | Muy bajas | Alto |
| Totalmente semiconductor | < 1 ms | Altas (~0.1–0.2% de la potencia) | Muy alto |

**DCCB híbrido ABB (solución estándar actual).** El camino de conducción nominal es mecánico (interruptor de vacío), con pérdidas mínimas. Al detectar la falta:

1. Abre el interruptor mecánico → la corriente se transfiere al camino de IGBT en **< 2 ms** (los IGBT conducen durante este período).
2. El IGBT abre → la energía inductiva del cable (\( \frac{1}{2}L_{cable}I_{fault}^2 \)) es absorbida por el **varistor de óxido metálico (MOV)**, que clamp la tensión a un valor controlado mientras la corriente decae.
3. La corriente cae a cero en **< 5 ms** desde el inicio de la apertura.

**Energía que debe absorber el MOV:**

$$ E_{MOV} = \frac{1}{2}L_{cable}I_{fault}^2 $$

Para \( L_{cable} = 200\,\text{mH} \) (cable de 200 km) e \( I_{fault} = 20\,\text{kA} \):

$$ E_{MOV} = \frac{1}{2} \times 0.2 \times (20000)^2 = 40\,\text{MJ} $$

Este valor determina el dimensionado del MOV, que es el componente más costoso del DCCB híbrido.

## 5 — Estrategias de protección sin DCCB

El alto coste de los DCCB ha impulsado soluciones alternativas que evitan o reducen su necesidad:

**MMC de puente completo (FB-MMC).** Cada submódulo tiene 4 IGBTs en lugar de 2, lo que permite generar tensión negativa. Al detectar la falta, los brazos invierten su tensión, bloqueando activamente la corriente de falta en < 2 ms sin necesidad de DCCB. Ventaja: tiempo de respuesta muy rápido, sin energía inductiva que disipar externamente. Desventaja: el número de IGBTs se duplica, lo que aumenta las pérdidas nominales (~2× respecto al HB-MMC) y el coste de los submódulos.

**Método de apretón de manos (*Handshaking*).** Secuencia coordinada:
1. Detectar la falta y abrir los disyuntores AC de **todos** los terminales MTDC.
2. Esperar la extinción natural de la corriente DC (la inductancia del cable la reduce a cero en 50–200 ms).
3. Aislar el segmento de cable defectuoso con seccionadores DC (no son interruptores de falta, solo de seccionamiento).
4. Reconectar los terminales sanos.

Tiempo total: **200–500 ms**. Aceptable si la red AC puede soportar la interrupción momentánea y no hay requisito de continuidad de servicio (p.ej. en un parque eólico offshore no crítico).

**Bus splitting (seccionamiento de bus).** La red DC se divide en zonas separadas por interruptores de seccionamiento. Ante una falta, se aísla la zona afectada; el resto de la red continúa operando. Los seccionadores no interrumpen corriente de falta (para eso sí se necesita DCCB o FB-MMC), pero limitan el impacto a la zona defectuosa.

**Protección por sobrecorriente del convertidor.** El MMC limita la corriente de los brazos mediante saturación del regulador de corriente. Si la corriente supera el umbral de protección (típicamente 1.5–2 pu), el MMC bloquea los IGBTs. Esto protege el convertidor pero no aísla el cable: la corriente de falta puede seguir fluyendo desde otros terminales a través de los diodos.

**Combinaciones prácticas.** Los proyectos reales suelen combinar: FB-MMC en terminales críticos (máxima rapidez) + DCCB híbridos en los cables más propensos a faltas + Handshaking como respaldo para faltas en buses.

## 6 — Proyecto North Sea Wind Power Hub

**Concepto.** El North Sea Wind Power Hub (NSWPH) es el proyecto de mayor escala de MTDC planificado: una plataforma o isla artificial en el Mar del Norte que agrega **10–15 GW de energía eólica offshore** de múltiples parques y la distribuye a cuatro países europeos.

**Arquitectura MTDC:**
- **Terminales:** 4–6 terminales VSC-HVDC que conectan Alemania, Dinamarca, Países Bajos y Bélgica.
- **Cables:** longitud 500–1000 km, tensión ±525 kV (el estándar actual más alto para HVDC).
- **Topología:** mallada, con redundancia para asegurar la entrega de potencia incluso con un cable en falta.
- **Potencia:** cada terminal maneja 1–3 GW de transferencia nominal.

**Solución de protección prevista:**
- DCCB híbridos en todos los puntos de derivación de la red mallada.
- MMC-FB en los terminales offshore críticos (donde la interrupción del suministro eléctrico a la plataforma sería problemática).
- Relés de protección basados en ondas viajeras con tiempo de detección < 2 ms.

**Estado (2026).** En fase de planificación avanzada y desarrollo de estándares técnicos (IEC 62975, ENTSO-E HVDC Grid Guidelines). Los primeros cables de la fase 1 están en proceso de licitación entre Dinamarca y Países Bajos.

**Por qué es relevante.** El NSWPH representa el primer MTDC de gran escala. Su éxito técnico (en particular la solución de protección DC) determinará si la tecnología MTDC puede escalar al nivel de gigavatios necesario para la transición energética europea.

## Cuándo y por qué se usa

- Para interconectar múltiples parques eólicos offshore o fuentes renovables sin multiplicar la infraestructura de cable.
- Para crear redundancia en la transmisión HVDC: un terminal fuera de servicio no interrumpe la transferencia total.
- Cuando el coste marginal de añadir un terminal es inferior al beneficio de la flexibilidad operativa.

## Errores comunes

- Asumir que el droop DC es suficiente sin control secundario: sin restauración secundaria, la tensión DC se desvía permanentemente de \( V_{dc,0} \) tras cada perturbación.
- Subestimar la energía de falta: los cálculos de \( E_{MOV} \) para cables largos dan decenas de MJ, no kJ.
- Confundir seccionadores DC (para apertura sin carga) con DCCB (para interrupción de falta): los primeros no pueden abrir corriente de falta.

## Conceptos relacionados

- [[hvdc-vsc-topologia]] · [[hvdc-cable-dc]] · [[hvdc-control-potencia]] · [[droop-dc]] · [[mmc-modelo-control]]

## Referencias

- Hertem, Gomis-Bellmunt, Liang, *HVDC Grids: For Offshore and Supergrid of the Future*, Wiley 2016.
- Beerten, Cole, Belmans, *Generalized Steady-State VSC MTDC Model*, IEEE TPWRS 2012.
