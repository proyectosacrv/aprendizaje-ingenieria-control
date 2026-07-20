---
titulo: "HVDC-VSC: topología y arquitectura"
slug: hvdc-vsc-topologia
categoria: fisica-modelado
tipo: concepto
nivel: avanzado
proyectos: []
objetivos: [comprender la arquitectura del HVDC-VSC y el MMC, distinguir configuraciones y modos de operación]
tags: [hvdc, vsc, mmc, monopolar, bipolar, punto-a-punto, multi-terminal, offshore]
fecha_creacion: 2026-07-05
fecha_actualizacion: 2026-07-05
relacionados: [convertidor-back-to-back, topologias-multinivel, filtro-lcl, fenomenos-oscilatorios-red]
referencias:
  - "Cigré TB 604, Guide for the Development of Models for HVDC Converters"
  - "Lesnicar & Marquardt, An Innovative Modular Multilevel Converter Topology"
---

## 1 — Definición y motivación del HVDC-VSC

HVDC-VSC (High Voltage Direct Current con Voltage Source Converter) transmite potencia eléctrica en
corriente continua usando convertidores de fuente de tensión en ambos extremos. A diferencia del HVDC
clásico con tiristores (LCC-HVDC), el VSC-HVDC:

- Controla \( P \) y \( Q \) de forma independiente en cada extremo
- Puede conectarse a redes débiles o isladas (no necesita conmutación natural)
- Invierte el flujo de potencia cambiando el signo de la corriente DC (no la tensión)
- Es la tecnología estándar para conexión de parques eólicos offshore

La ausencia de conmutación natural es la diferencia fundamental: el LCC-HVDC necesita una red fuerte
para conmutar los tiristores, mientras que el VSC puede **formar** su propia tensión de referencia
mediante el control. Esto abre aplicaciones imposibles para el LCC: parques eólicos offshore sin red
local, conexión de islas, sistemas MTDC (Multi-Terminal DC).

Aplicaciones principales: cables submarinos > 80 km, interconexiones asíncronas (p. ej. Gran Bretaña–
Irlanda, Cataluña–Baleares), conexión de parques eólicos offshore (Dogger Bank, Hornsea), MTDC para
redes DC offshore.

## 2 — Configuraciones: monopolar, bipolar y simétrica

La arquitectura de la red DC define el número de conductores y el comportamiento ante faltas.

**Monopolar con retorno por tierra.** Un solo conductor a \( +V_{dc} \); el retorno es por tierra o
lecho marino. Es la configuración más barata, pero genera corrientes vagabundas que corroen tuberías y
estructuras metálicas. En desuso para instalaciones modernas.

**Bipolar.** Dos conductores a \( \pm V_{dc} \) respecto a tierra. Es el estándar moderno. Ventaja
clave: si un polo falla, el otro puede seguir operando al 50 % de potencia con retorno por tierra.
La potencia nominal se recupera parcialmente sin intervención manual.

**Simétrica monopolar.** Dos conductores a \( \pm V_{dc} \) sin punto de conexión a tierra —
más económica que la bipolar al eliminar los transformadores de puesta a tierra, pero sin redundancia
ante falta de polo. Usada en algunos proyectos offshore donde el peso del transformador es crítico.

La tensión nominal del enlace es una decisión económica entre coste del cable (crece con la sección) y
coste del convertidor (crece con la tensión). Tensiones típicas actuales: \( \pm 320\,\text{kV} \)
(cables submarinos), \( \pm 500\,\text{kV} \) (líneas aéreas); potencias: 200 MW–2 GW por enlace
punto a punto.

## 3 — El MMC: Modular Multilevel Converter

El MMC es el convertidor dominante en HVDC moderno desde ~2010. Sustituyó al VSC de dos niveles con
IGBT de alta tensión porque ofrece mejor calidad de forma de onda, menores pérdidas y mayor
escalabilidad.

Estructura: cada fase tiene dos **brazos** (arm), uno superior (upper) y uno inferior (lower). Cada
brazo contiene \( N \) submódulos (SM) en serie más una inductancia de brazo \( L_{arm} \):

$$v_{arm} = \sum_{k=1}^{N} v_{SM,k}, \qquad v_{SM} = \begin{cases} V_C & \text{SM insertado} \\ 0 & \text{SM bypasseado} \end{cases}$$

La tensión de fase de salida es la diferencia entre las tensiones insertadas en los brazos superior
e inferior. Controlando cuántos SMs se insertan en cada brazo en cada instante de tiempo se sintetiza
la tensión AC deseada:

$$v_{phase} = \frac{V_{dc}}{2} - L_{arm}\frac{di_{arm,upper}}{dt} - \sum_{\text{SM upper inserted}} V_C$$

**Submódulo half-bridge (HB-SM).** Dos IGBTs (\( S_1 \), \( S_2 \)) y un condensador. En estado
insertado (\( S_1 \) ON, \( S_2 \) OFF) el condensador está en serie con el brazo: \( v_{SM}=V_C \).
En estado bypasseado (\( S_2 \) ON, \( S_1 \) OFF): \( v_{SM}=0 \). No puede generar tensión negativa,
por lo que no puede bloquear una falta DC. Es el más común por menor coste (2 IGBTs) y menores pérdidas.

**Submódulo full-bridge (FB-SM).** Cuatro IGBTs en puente. Puede generar \( v_{SM}\in\{-V_C, 0, +V_C\} \).
Al bloquear los IGBTs en falta DC, todos los condensadores quedan en serie oponiéndose a la corriente
de falta — extingue la falta sin disyuntor DC. Coste mayor (4 IGBTs) y pérdidas ~1.5× respecto al HB.

Con \( N=200 \)–400 SMs por brazo, la tensión de salida tiene \( N+1 \) niveles → THD despreciable
sin filtro AC de potencia. Esta es la razón por la que el MMC no necesita el filtro LCL del VSC de
dos niveles.

## 4 — Energía almacenada y corriente de circulación

Cada brazo almacena energía en los condensadores de sus SMs. Para el brazo superior de la fase a:

$$W_{ua} = \frac{1}{2} C_{SM} \sum_{k=1}^{N} V_{C,uk}^2 \approx \frac{N}{2} C_{SM} V_{C,nom}^2$$

La energía total del MMC es considerable — del orden de 30–40 kJ/MVA. Actúa como reserva de energía
interna que amortigua los transitorios de potencia, similar al volante de inercia de un generador.

**Corriente de circulación.** Es la componente que circula entre los brazos de la misma fase sin salir
al exterior del convertidor. Definición formal:

$$i_{circ,a} = \frac{i_{upper,a} + i_{lower,a}}{2} - \frac{I_{dc}}{3}$$

En estado estacionario, \( i_{circ} \) tiene principalmente segunda armónica (\( 2\omega_0 \)). Su
origen físico: la tensión de condensador de cada brazo varía a \( \omega_0 \), y esta variación no es
perfectamente simétrica entre el brazo superior e inferior, lo que genera un voltaje diferencial
interno a \( 2\omega_0 \) que impulsa una corriente a esa frecuencia.

Si no se controla, \( i_{circ} \) aumenta las pérdidas en las inductancias y resistencias de brazo y
amplifica el rizado de tensión de los condensadores. El **CCSC** (Circulating Current Suppression
Controller) la elimina actuando sobre la tensión de inserción de cada brazo.

## 5 — Topología punto a punto vs MTDC

**Punto a punto.** Dos terminales VSC conectados por un cable DC. Es la topología más sencilla: un
terminal controla \( V_{dc} \) (el rector del balance de energía del cable) y el otro controla \( P \)
(inyecta o absorbe la potencia deseada). El control es centralizado y sencillo.

**MTDC (Multi-Terminal DC).** Tres o más terminales VSC conectados en la misma red DC. Los proyectos
actuales más relevantes son las redes offshore para integrar múltiples parques eólicos y entregarlos
a múltiples puntos de la red onshore.

Ventajas del MTDC respecto a múltiples enlaces punto a punto: redundancia (si un enlace falla, la
potencia se redistribuye), menor coste por terminal compartido, posibilidad de optimización del flujo
de potencia en la red DC.

**Control MTDC — droop de tensión DC.** Si un solo terminal controla \( V_{dc} \), su fallo colapsa
toda la red DC. La solución estándar es el droop:

$$P_i = P_{0,i} + k_{d,i}(V_{dc} - V_{dc,0})$$

Cada terminal ajusta su inyección de potencia en función del error de tensión DC, con ganancia
\( k_{d,i} \). Ventajas: sin comunicación entre terminales — acción local e instantánea; varios
terminales comparten el control de \( V_{dc} \) proporcionalmente a sus ganancias de droop.

**Protección DC en MTDC.** El gran reto tecnológico: los disyuntores DC (DC circuit breakers, DCCB)
deben interrumpir corrientes de falta en < 5 ms (vs. los 50–100 ms de un disyuntor AC). ABB, Alstom
y GE tienen diseños comerciales, pero su coste es aún muy elevado.

## 6 — Parámetros típicos y dimensionado

El dimensionado del MMC parte de la energía almacenada especificada (habitualmente 30–40 kJ/MVA):

$$W_{stored} \approx 35\,\text{kJ/MVA} \times S_{nom}$$

La tensión nominal de los condensadores se determina por el número de SMs y la tensión DC:

$$V_{C,nom} = \frac{V_{dc}}{N}$$

Y la capacidad de cada SM se obtiene de la energía por brazo (\( W_{stored}/6 \)) y la tensión:

$$C_{SM} = \frac{2\,W_{stored}}{6\,N\,V_{C,nom}^2} = \frac{W_{stored}\,N}{3\,V_{dc}^2}$$

| Parámetro | Valor típico |
|---|---|
| Tensión DC | \( \pm 320\,\text{kV} \) (cables), \( \pm 500\,\text{kV} \) (aéreo) |
| Potencia nominal | 500 MW–2 GW |
| Inductancia de brazo \( L_{arm} \) | 0.15 pu |
| Energía almacenada | 30–40 kJ/MVA |
| Número de SMs por brazo \( N \) | 200–400 |
| Frecuencia de conmutación SM | 150–300 Hz |
| Pérdidas totales por terminal | 0.8–1.2 % |

La frecuencia de conmutación de cada IGBT es baja (150–300 Hz) porque el NLM (Nearest Level
Modulation) distribuye la conmutación entre los \( N \) SMs. La frecuencia efectiva de la tensión de
salida es \( N \) veces mayor, lo que explica la excelente calidad de forma de onda sin filtros.

## 7 — Comparativa LCC-HVDC vs VSC-HVDC

La tecnología HVDC clásica (LCC, Line Commutated Converter) usa tiristores que se conmutan
naturalmente por la tensión de red. El VSC-HVDC usa IGBTs con conmutación forzada. Las diferencias
son fundamentales para el diseño de sistemas:

| Característica | LCC-HVDC | VSC-HVDC (MMC) |
|---|---|---|
| Dispositivo | Tiristor (sin disparo de apagado) | IGBT (disparo de encendido y apagado) |
| Control de Q | No independiente: absorbe Q de la red | Independiente: controla P y Q por separado |
| Conmutación | Natural (depende de la tensión de red) | Forzada (no depende de la red) |
| Red débil | Requiere SCR ≥ 2–3; falla con red débil | Opera con SCR = 0 (isla, parques offshore) |
| Black start | No: necesita tensión de red para conmutar | Sí: puede energizar una red muerta |
| Inversión de flujo | Invertir \( V_{dc} \) (la corriente no cambia de signo) | Invertir \( I_{dc} \) (la tensión no cambia de signo) |
| Pérdidas totales | ~0.7–0.8 % por terminal | ~0.8–1.2 % por terminal (MMC) |
| Potencia máxima | > 7 GW (Itaipu, ±600 kV) | ~2 GW por enlace actual |
| Filtros AC | Grandes (capacidad reactiva) | No necesarios (MMC multinivel) |
| Aplicación típica | Interconexiones continentales de muy alta potencia | Cables submarinos, offshore, redes MTDC |

**Por qué el LCC sigue siendo relevante.** Para potencias > 2 GW y tensiones > ±500 kV, el LCC
sigue siendo más barato y con menores pérdidas. El Itaipu (Brasil-Paraguay, 6.3 GW) y el Three
Gorges–Shanghai (China, 6.4 GW a ±500 kV DC) son ejemplos de LCC que no tienen equivalente VSC.

**La inversión de flujo en LCC.** Como el tiristor no puede apagarse por la compuerta, la
corriente DC siempre fluye en la misma dirección. Para invertir el flujo de potencia hay que
invertir la tensión DC (el rectificador pasa a comportarse como inversor y viceversa). Esto hace
que la red HVDC LCC no sea adecuada para sistemas MTDC con múltiples terminales que necesitan
cambiar de dirección el flujo de potencia frecuentemente.

## 8 — Proyectos HVDC-VSC reales: DolWin, BorWin, NordLink

Los proyectos offshore en el Mar del Norte son la referencia técnica mundial del HVDC-VSC.

**BorWin1 (2009, ABB, ±150 kV, 400 MW, 200 km).** Primer enlace HVDC-VSC offshore para un parque
eólico. Terminal offshore en la plataforma con un convertidor VSC de dos niveles (aún no MMC).
Demostró la viabilidad del concepto pero tuvo problemas de resonancias con el filtro AC.

**DolWin1 (2015, ABB, ±320 kV, 800 MW, 165 km).** Primer HVDC con MMC de ABB (HVDC Light de
quinta generación). Conecta el parque Alpha Ventus y otros en la zona DolWin al nodo de Dörpen.
Parámetros del MMC: N ≈ 400 SMs por brazo, \( V_{C,nom} \approx 1.6\,\text{kV} \),
\( f_{sw,IGBT} \approx 150\,\text{Hz} \).

**BorWin3 (2019, Siemens, ±320 kV, 900 MW, 160 km).** Primer HVDC con MMC híbrido (HB+FB en
proporción) que puede bloquear faltas DC sin DCCB — los FB-SMs se polarizan inversamente.

**NordLink (2021, ABB+Siemens, ±525 kV, 1400 MW, 623 km).** Interconexión Noruega–Alemania.
Primer HVDC a ±525 kV — el nivel de tensión más alto para cables HVDC. Cable XLPE de 516 km
submarino + 107 km terrestre. Demuestra que los cables XLPE son viables a tensiones superiores
a las históricas para papel impregnado (≤±500 kV).

| Proyecto | Año | Tensión DC | Potencia | Longitud | Tecnología |
|---|---|---|---|---|---|
| BorWin1 | 2009 | ±150 kV | 400 MW | 200 km | VSC 2 niveles |
| DolWin1 | 2015 | ±320 kV | 800 MW | 165 km | MMC-HB |
| BorWin3 | 2019 | ±320 kV | 900 MW | 160 km | MMC híbrido |
| NordLink | 2021 | ±525 kV | 1400 MW | 623 km | MMC-HB cable XLPE |
| Dogger Bank | 2024+ | ±320 kV | 1200 MW×3 | ~130 km | MMC |

## 9 — Pérdidas del MMC por submódulo

Las pérdidas del MMC son inferiores a las del VSC de dos niveles porque cada IGBT conmuta a baja
frecuencia (150–300 Hz con NLM frente a 1–5 kHz del VSC-2L).

**Pérdidas de conducción.** Cada SM half-bridge tiene 2 IGBTs y 2 diodos. En cada instante,
la corriente de brazo fluye por un IGBT (SM insertado) o por un diodo (SM bypasseado). Las
pérdidas de conducción por SM:

$$ P_{cond,SM} = V_{CE,sat}\,|i_{brazo}| \cdot d_{ins} + V_F\,|i_{brazo}|\,(1-d_{ins}) $$

donde \( d_{ins} \) es el ciclo de inserción del SM, \( V_{CE,sat} \approx 2\text{–}3\,\text{V} \)
la caída de saturación del IGBT y \( V_F \approx 1.5\text{–}2\,\text{V} \) la caída en el diodo.
Sumando sobre los \( 2N \) SMs de cada brazo y los 6 brazos:

$$ P_{cond,total} \approx 6\,(V_{CE,sat}+V_F)\,I_{brazo,rms}\,N $$

Para un MMC de 500 MW, \( N=300 \), \( I_{brazo,rms} \approx 1.2\,\text{kA} \):
\( P_{cond} \approx 6\times3.5\times1200\times300/10^6 \approx 7.5\,\text{MW} \) (1.5 % de 500 MW).

**Pérdidas de conmutación.** Proporcionales a la frecuencia de conmutación de cada IGBT:

$$ P_{sw,SM} = f_{sw,IGBT}\,(E_{on}+E_{off}+E_{rec})\cdot\frac{i_{brazo}}{I_{test}} $$

Con NLM, \( f_{sw,IGBT} \approx f_0 = 50\,\text{Hz} \) — las pérdidas de conmutación son una
fracción pequeña del total (<0.1 % por terminal). Esto es la ventaja clave del MMC.

**Total por terminal.** Las pérdidas completas (conducción + conmutación + transformador) de un
terminal MMC-HVDC moderno son 0.8–1.0 % de la potencia nominal a plena carga. A carga parcial
(50 %), las pérdidas de conducción caen pero las de transformador son fijas → el rendimiento
relativo baja.

## 10 — HVDC multi-terminal (MTDC): topologías y protección

**Topología radial.** Todos los terminales se conectan en estrella a un nodo central. Simple y
económica para 3–4 terminales. El nodo central es un punto único de fallo — si falla, se pierde
toda la red MTDC.

**Topología mallada.** Múltiples conexiones redundantes entre terminales. Mayor coste de cables y
DCCB (uno por conexión), pero sin punto único de fallo. Es la topología objetivo de las futuras
superredes DC offshore (North Sea Network, European Supergrid).

**Protección DC: el reto central del MTDC.** En una red AC, los disyuntores tienen 50–100 ms
para interrumpir una falta — tiempo suficiente para que el arco AC se extinga naturalmente en el
paso por cero. En DC no hay paso por cero: hay que interrumpir la corriente artificialmente.
La corriente de falta DC crece a razón de:

$$ \frac{di_{fault}}{dt}\bigg|_{t=0} = \frac{V_{dc}}{L_{total}} $$

Para \( V_{dc}=640\,\text{kV} \) y \( L_{total}=100\,\text{mH} \): \( di/dt = 6.4\,\text{kA/ms} \).
En 5 ms (tiempo objetivo de interrupción), la corriente ya es 32 kA — 40× la nominal.

**DCCB (DC Circuit Breaker).** Tipos disponibles:

- **Mecánico puro:** lento (50–100 ms), solo válido si los SMs-FB pueden bloquear la falta mientras
  el breaker se abre.
- **Híbrido (ABB, 2012):** breaker mecánico de baja pérdidas en serie con un thyristor de
  desvío. En falta, el thyristor desvía la corriente al semiconductor principal que la interrumpe
  en <5 ms. Pérdidas < 0.01 % en operación normal.
- **Completamente sólido:** solo semiconductores, interrupción en < 1 ms. Pérdidas de conducción
  mayores (~0.1 %) pero más compacto y sin partes móviles.

**Coordinación de protecciones en MTDC.** La selectividad (interrumpir solo el tramo en falta sin
desconectar toda la red) requiere una combinación de DCCB en cada extremo de cada línea DC y un
algoritmo de detección de falta basado en la velocidad de crecimiento de la corriente:

$$ \text{Falta detectada si:}\quad \frac{di_{DC}}{dt} > \text{umbral} \approx 0.5\,\text{kA/ms} $$

Este umbral puede ser superado por transitorios de control en condiciones normales — la
discriminación debe completarse en < 2 ms para que el DCCB pueda actuar antes de que la corriente
destruya los IGBTs.

<div class="cfig"><img src="figuras/hvdc-vsc-topologia-analisis.png" alt="HVDC-VSC topología MMC y corriente de circulación"><div class="cap">Configuraciones HVDC-VSC (monopolar/bipolar), síntesis de tensión multinivel del MMC para distintos N, THD vs. número de submódulos, y corriente de circulación con y sin CCSC.</div></div>
