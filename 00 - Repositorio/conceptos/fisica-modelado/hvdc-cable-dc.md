---
titulo: Cable DC para HVDC
slug: hvdc-cable-dc
categoria: fisica-modelado
tipo: concepto
nivel: avanzado
proyectos: []
objetivos: [modelar el cable DC del enlace HVDC, entender la resonancia LC y el comportamiento ante faltas]
tags: [hvdc, cable-dc, modelo-pi, constante-rc, resonancia-dc, falta-dc]
fecha_creacion: 2026-07-05
fecha_actualizacion: 2026-07-05
relacionados: [convertidor-back-to-back, topologias-multinivel, filtro-lcl, fenomenos-oscilatorios-red]
referencias:
  - "Cigré TB 604, Guide for the Development of Models for HVDC Converters"
  - "Lesnicar & Marquardt, An Innovative Modular Multilevel Converter Topology"
---

## 1 — Características del cable submarino HVDC

El cable DC difiere del cable AC en un aspecto fundamental: en corriente continua la inductancia no
tiene efecto reactivo (\( \omega=0 \)), por lo que la impedancia en régimen permanente es puramente
resistiva. Esto elimina la limitación de Ferranti y el problema de la potencia reactiva de carga que
condena a los cables AC a longitudes máximas de ~80–100 km.

La capacidad del cable, en cambio, es incluso más importante en DC que en AC: almacena energía
\( W = \tfrac{1}{2}C_{cable}V_{dc}^2 \) que actúa como reserva de energía y determina la dinámica
de la tensión DC durante los transitorios de control y las faltas.

Comparación con cable AC equivalente:

| Parámetro | Cable AC 132 kV | Cable DC ±320 kV HVDC |
|---|---|---|
| Resistencia \( R \) | 0.05 Ω/km | 0.012 Ω/km (conductor mayor) |
| Inductancia \( L \) | 0.4 mH/km | 0.4 mH/km (irrelevante en DC) |
| Capacidad \( C \) | 0.2 µF/km | 0.15–0.25 µF/km |
| Longitud máxima operativa | ~80 km | ilimitada (prácticamente) |
| Pérdidas/100 km | > 1 % (reactiva) | ~0.3 % (solo Joule) |

La inductancia \( L \) sí importa en el análisis dinámico de transitorios y faltas DC — forma con la
capacidad el circuito resonante que determina la velocidad de crecimiento de la corriente de falta.

## 2 — Modelo π del cable DC

Para el diseño de controladores (frecuencias < 100 Hz) y el análisis de estabilidad de lazo, el modelo
π concentrado con parámetros totales es suficiente.

**Paso 1 — topología del modelo π.** Se concentra la resistencia y la inductancia en la rama serie
central, y la capacidad total se reparte en dos shunts de \( C/2 \) en los extremos:

$$\frac{dI_{dc}}{dt} = \frac{V_{dc1} - V_{dc2} - R\cdot I_{dc}}{L_{cable}}$$

$$\frac{dV_{dc1}}{dt} = \frac{I_{VSC1} - I_{dc}}{C/2}, \qquad \frac{dV_{dc2}}{dt} = \frac{I_{dc} - I_{VSC2}}{C/2}$$

donde \( V_{dc1} \), \( V_{dc2} \) son las tensiones DC en los terminales 1 y 2, \( I_{dc} \) la
corriente en la rama serie, e \( I_{VSC1,2} \) las corrientes inyectadas por los convertidores.

**Paso 2 — constante de tiempo RC.** La constante de tiempo del cable en bucle abierto (sin
convertidor activo):

$$\tau_{dc} = R_{total} \cdot C_{total} = (R_{km}\cdot\ell)(C_{km}\cdot\ell) = R_{km}C_{km}\ell^2$$

La dependencia cuadrática con la longitud \( \ell \) es la razón por la que cables muy largos tienen
dinámicas lentas. Para \( R_{km}=0.012\,\Omega/\text{km} \), \( C_{km}=0.2\,\mu\text{F/km} \),
\( \ell=300\,\text{km} \):

$$\tau_{dc} = 0.012 \times 0.2 \times 10^{-3} \times 300^2 = 216\,\text{ms}$$

Este valor limita el ancho de banda del lazo de control de \( V_{dc} \): no se puede hacer el
controlador más rápido que \( \sim 1/\tau_{dc} \) sin excitar la resonancia LC.

**Paso 3 — modelo en espacio de estados.** El sistema de tres variables de estado
\( \mathbf{x} = [V_{dc1},\; I_{dc},\; V_{dc2}]^T \):

$$\dot{\mathbf{x}} = \begin{pmatrix} 0 & -\tfrac{2}{C} & 0 \\ \tfrac{1}{L} & -\tfrac{R}{L} & -\tfrac{1}{L} \\ 0 & \tfrac{2}{C} & 0 \end{pmatrix}\mathbf{x} + \begin{pmatrix} \tfrac{2}{C} & 0 \\ 0 & 0 \\ 0 & -\tfrac{2}{C} \end{pmatrix}\begin{pmatrix}I_{VSC1}\\I_{VSC2}\end{pmatrix}$$

Los eigenvalores de la matriz de estado determinan la dinámica natural del cable: un modo lento real
(la constante \( \tau_{RC} \)) y un par de modos complejos conjugados (la resonancia LC).

## 3 — Resonancia LC del sistema HVDC

La inductancia efectiva del sistema HVDC incluye la inductancia del cable y las inductancias de brazo
de los dos MMC (que aparecen en serie desde el punto de vista del bus DC):

$$L_{total} = L_{cable} + \frac{2L_{arm}}{3} \times 2 \approx L_{cable} + \frac{4}{3}L_{arm}$$

La frecuencia de resonancia del circuito LC formado por \( L_{total} \) y \( C_{cable} \):

$$f_{res} = \frac{1}{2\pi\sqrt{L_{total}\cdot C_{cable}}}$$

**Paso 1 — cálculo numérico.** Para \( L_{total}=120\,\text{mH} \) y \( C_{cable}=60\,\mu\text{F} \):

$$f_{res} = \frac{1}{2\pi\sqrt{0.12 \times 60\times10^{-6}}} = \frac{1}{2\pi \times 2.68\times10^{-3}} \approx 59\,\text{Hz}$$

**Paso 2 — implicación para el control.** Esta frecuencia de resonancia cae dentro del ancho de
banda del lazo de corriente del MMC (~1 kHz) y cerca del del lazo de \( V_{dc} \) (~10–50 Hz). Si el
control excita la resonancia (p. ej. por un escalón brusco de referencia o por una ganancia excesiva),
el sistema oscila a \( f_{res} \).

**Paso 3 — modos sub/supersíncronos.** La resonancia DC a \( f_{res} \) aparece en el dominio AC como
modos a \( f_{red} \pm f_{res} \). Para \( f_{red}=50\,\text{Hz} \) y \( f_{res}=59\,\text{Hz} \):

$$f_{sub} = |50 - 59| = 9\,\text{Hz}, \qquad f_{super} = 50 + 59 = 109\,\text{Hz}$$

Estos modos subsíncronos/supersíncronos son los **SSO** (Sub-Synchronous Oscillations) que han
causado disparos en sistemas HVDC reales ([[fenomenos-oscilatorios-red]]).

## 4 — Falta DC y protección

Una falta bipolar en el cable DC (cortocircuito entre los dos polos) descarga bruscamente los
condensadores del MMC y del cable. La corriente de falta crece inicialmente como:

$$i_{fault}(t) \approx \frac{V_{dc}}{Z_c}\sin\left(\frac{t}{\sqrt{L_{total}C_{cable}}}\right) \cdot e^{-\frac{R}{2L}t}$$

donde \( Z_c = \sqrt{L_{total}/C_{cable}} \) es la impedancia característica. Para los valores típicos
del ejemplo (\( V_{dc}=640\,\text{kV} \), \( Z_c=44.7\,\Omega \)):

$$I_{fault,pico} \approx \frac{640\,\text{kV}}{44.7\,\Omega} \approx 14.3\,\text{kA}$$

La corriente nominal del enlace de 500 MW es \( I_{nom} = 500/(640) \approx 781\,\text{A} \), por lo
que la corriente de falta pico es \( \sim 18\,\text{pu} \) — un orden de magnitud por encima de la
nominal.

**Limitaciones de los MMC-HB.** Los IGBTs de los submódulos half-bridge no pueden bloquear una falta
DC: aunque se apaguen las compuertas, los diodos de antiparalelo conducen la corriente de falta desde
la red AC hacia el punto de falta. El sistema funciona como un rectificador no controlado hasta que
se abre el disyuntor AC del terminal.

**Soluciones:**

- **MMC-FB (full-bridge):** al bloquear los IGBTs, todos los condensadores de los SMs quedan
  polarizados en oposición a la corriente de falta. Puede extinguir la falta en pocos ms sin
  disyuntor DC, pero añade pérdidas y coste (~1.5× vs HB).
- **DC circuit breaker (DCCB):** interruptor DC que corta en < 5 ms. Tecnologías: híbrido
  (ABB, 2012) con semiconductor principal + breaker mecánico, o completamente sólido. Coste
  todavía elevado, en fase de despliegue comercial.
- **Handshaking method:** abrir el disyuntor AC del terminal más cercano, esperar que la
  corriente de falta se extinga naturalmente (varias decenas de ms), reconectar. Solo válido
  en sistemas punto a punto — inaceptable en MTDC.

## 5 — Parámetros de diseño del cable

El cable submarino HVDC de alta tensión tiene capas coaxiales: conductor de cobre o aluminio,
aislamiento de XLPE (polyethylene entrecruzado), pantalla metálica y armadura de acero. La resistencia
por km es inversamente proporcional a la sección del conductor:

$$R_{km} = \frac{\rho_{Cu}}{A_{cond}} \approx \frac{17.2\,\text{n}\Omega\cdot\text{m}}{A_{cond}}$$

Para potencias de 500 MW a ±320 kV, la corriente nominal es ~781 A, lo que requiere secciones de
\( \sim 1600\,\text{mm}^2 \) y conduce a \( R_{km} \approx 0.011\,\Omega/\text{km} \).

La capacidad por km depende de la geometría del cable (dieléctrico y diámetros), con valores típicos
de 0.15–0.25 µF/km para cables de ±320 kV.

| Parámetro | Ejemplo: 300 km, ±320 kV, 500 MW |
|---|---|
| \( R_{cable} \) total | 3.3 Ω |
| \( L_{cable} \) total | 120 mH |
| \( C_{cable} \) total | 60 µF |
| \( Z_c = \sqrt{L/C} \) | 44.7 Ω |
| \( \tau_{RC} = RC \) | 198 ms |
| \( f_{res,LC} \) | 59 Hz |
| Energía almacenada | 3.1 MJ |
| Pérdidas en el cable | 1.63 MW (0.33 %) |

## 6 — Validación del modelo π y limitaciones

El modelo π concentrado es válido cuando la longitud eléctrica del cable es mucho menor que la
longitud de onda a la frecuencia de análisis. En DC puro (0 Hz) siempre es válido. Para transitorios
de control (< 100 Hz), la longitud de onda en el cable es:

$$\lambda = \frac{v_{prop}}{f} = \frac{1/\sqrt{LC_{km}/\text{km}}}{f} \approx \frac{1.6\times10^5\,\text{m/s}}{100\,\text{Hz}} = 1600\,\text{km}$$

Para un cable de 300 km, \( \ell/\lambda \approx 0.19 \) — el modelo π introduce un error < 5 %
para frecuencias de control. Para análisis de faltas (tiempos < 1 ms, frecuencias > 1 kHz), se
necesitan modelos de línea distribuida con al menos 10–20 secciones π en cascada.

La validación del modelo se realiza comparando la impedancia calculada con medidas de reflexión
de pulsos (TDR) en el cable real o con el modelo de parámetros distribuidos de referencia.

## 7 — Modelo de línea distribuida para análisis de transitorios rápidos

Para transitorios de falta DC (tiempos < 1 ms, frecuencias > 1 kHz), el modelo π concentrado no
es suficiente: la longitud eléctrica del cable ya no es despreciable frente a la longitud de onda.
En este régimen hay que usar el modelo de línea distribuida (ecuaciones del telegrafista).

**Ecuaciones del telegrafista.** Para un cable de parámetros uniformes \( R', L', C', G' \)
por unidad de longitud, la tensión y corriente como función de la posición \( x \) y el tiempo \( t \):

$$ \frac{\partial V}{\partial x} = -R'\,I - L'\,\frac{\partial I}{\partial t} $$
$$ \frac{\partial I}{\partial x} = -G'\,V - C'\,\frac{\partial V}{\partial t} $$

En DC con \( G' \approx 0 \) (aislamiento XLPE de muy alta resistividad), el régimen permanente
es trivial (\( V = V_0 - R'xI \)), pero los transitorios rápidos (ondas de tensión debidas a
faltas o maniobras) se propagan como ondas viajeras con velocidad:

$$ v_{prop} = \frac{1}{\sqrt{L'C'}} \approx 1.5\text{–}1.7 \times 10^8\,\text{m/s} $$

(aproximadamente la mitad de la velocidad de la luz en el vacío, debido a la permitividad del
aislamiento XLPE: \( \varepsilon_r \approx 2.3 \)).

**Impedancia característica.** La impedancia de onda del cable:

$$ Z_c = \sqrt{\frac{R' + j\omega L'}{G' + j\omega C'}} \approx \sqrt{\frac{L'}{C'}} \quad (\omega \gg R'/L') $$

Para \( L'=0.4\,\text{mH/km} \) y \( C'=0.2\,\mu\text{F/km} \):
\( Z_c = \sqrt{0.4\times10^{-3}/0.2\times10^{-6}} = \sqrt{2000} \approx 44.7\,\Omega \).

**Onda de falta.** Cuando se produce un cortocircuito en el punto \( x_0 \) del cable, se genera
una onda de tensión que se propaga hacia ambos terminales con amplitud inicial \( -V_{dc}/2 \) y
la misma velocidad \( v_{prop} \). El frente de onda llega al terminal 1 a tiempo:

$$ t_{arribo} = \frac{x_0}{v_{prop}} $$

Para un cable de 300 km y falta en el punto medio: \( t = 150000/1.6\times10^8 = 0.94\,\text{ms} \).

**Modelado práctico.** Para análisis de protecciones DC, se discretiza el cable en \( n \) secciones
π en cascada. Con \( n = 10 \) secciones para un cable de 300 km, cada sección representa 30 km y
el error en la velocidad de propagación es < 5 % para frecuencias < 5 kHz. Para precisión mayor
(análisis EMC o estudios de coordinación de protecciones a < 1 ms), se necesitan \( n \geq 50 \)
secciones o modelos de línea con parámetros dependientes de la frecuencia.

## 8 — Comparativa XLPE vs cable de papel impregnado

La tecnología del aislamiento del cable ha evolucionado desde el papel impregnado en aceite (MIND/PPLP)
hasta el XLPE (polietileno entrecruzado) en los últimos 20 años. La elección del aislamiento afecta
a la tensión máxima de operación, la capacidad de transmisión y la vida útil del cable.

**XLPE (Cross-Linked Polyethylene).** El polietileno se entrecruza químicamente durante la
fabricación para mejorar sus propiedades térmicas. Ventajas principales:

- Temperatura de operación continua: 90°C (frente a 70°C del PE termoplástico)
- Sin aceite ni masa de impregnación: no hay riesgo de fugas, mantenimiento más sencillo
- Más ligero y flexible: más fácil de instalar en grandes profundidades
- Reversibilidad de la tensión: en AC no hay problema; en DC, la distribución de campo
  eléctrico depende de la temperatura (conductividad del polímero sube con temperatura),
  lo que genera acumulación de cargas espaciales en la interfaz conductor-aislamiento

**Limitación de tensión del XLPE en DC.** La acumulación de cargas espaciales en el XLPE sometido
a tensión DC continua degrada el aislamiento y puede provocar ruptura dieléctrica con el tiempo.
Esta fue la razón por la que históricamente el cable XLPE se limitó a ±200–250 kV en DC mientras
el papel impregnado llegaba a ±500 kV. Las mejoras en la formulación del XLPE (compuestos "DC-grade")
han elevado el límite a ±320 kV (DolWin, BorWin) y ya ±525 kV (NordLink, 2021).

**Papel impregnado (MIND, Mass Impregnated Non-Draining).** El papel es impregnado con aceite de
alta viscosidad que no fluye en posición vertical. Ventajas:

- Mayor tensión de operación: probado hasta ±600 kV (en desarrollo)
- Sin riesgo de cargas espaciales en DC
- Mejor resistencia a los transitorios de tensión (impulso de rayo)

Desventajas:
- Temperatura máxima: 55–60°C (limitada por la viscosidad del aceite)
- Más pesado y rígido: más difícil de instalar offshore
- Radios de curvatura mínimo mayor → buques posacables especializados

| Parámetro | XLPE DC-grade | MIND |
|---|---|---|
| Tensión máxima comercial | ±525 kV (NordLink) | ±500 kV (Svindvik) |
| Temperatura operación | 70–90°C | 50–60°C |
| Capacidad corriente | Mayor (por temperatura) | Menor |
| Cargas espaciales DC | Problema a considerar | No problema |
| Instalación offshore | Más flexible y ligero | Más pesado y rígido |
| Vida útil estimada | 40 años | 40–50 años |

## 9 — Protección diferencial del cable DC

La protección diferencial es el método de protección principal para cables HVDC en MTDC, por su
selectividad intrínseca: solo actúa si hay diferencia entre las corrientes en los dos extremos del
cable, lo que es la huella inequívoca de una falta en el cable.

**Principio.** En funcionamiento normal, la corriente que entra por el terminal 1 (\( I_1 \)) es
igual a la que sale por el terminal 2 (\( I_2 \)) más la corriente que carga la capacidad del cable
(\( I_C = C_{cable}\,dV_{dc}/dt \)):

$$ I_1 - I_2 = I_C = C_{cable}\,\frac{dV_{dc}}{dt} $$

En régimen permanente, \( I_C = 0 \) e \( I_1 = I_2 \). En transitorio de control normal,
\( I_C \) es pequeño y predecible. Ante una falta en el cable, parte de la corriente se deriva
hacia el punto de falta: \( I_1 - I_2 = I_{falta} \gg I_C \).

**Implementación.** La función diferencial compara las corrientes medidas en ambos extremos con
compensación de la corriente capacitiva:

$$ I_{diff} = I_1 - I_2 - C_{cable}\,\frac{dV_{dc}}{dt} > I_{diff,umbral} \quad\Rightarrow\quad \text{FALTA DC} $$

La latencia de comunicación entre los dos extremos (fibra óptica integrada en el cable DC) es
\( \tau_{comm} \approx \ell/v_{fibra} \approx 300\,\text{km}/2\times10^5\,\text{km/s} = 1.5\,\text{ms} \).
Esta latencia limita la velocidad de actuación de la protección diferencial.

**Sensibilidad y estabilidad.** El umbral \( I_{diff,umbral} \) debe ser mayor que el error de
medición + la corriente capacitiva máxima durante transitorios normales (para evitar disparos
intempestivos), y menor que la corriente de falta mínima (para detectar faltas de alta impedancia).
Típicamente: \( I_{diff,umbral} \approx 5\text{–}10\,\% \) de la corriente nominal.

## 10 — Ejemplo de cálculo completo: cable 300 km ±320 kV 500 MW

Este ejemplo integra todos los parámetros del cable para un enlace HVDC-VSC offshore representativo.

**Datos del sistema:**
- Potencia nominal: \( P_{nom} = 500\,\text{MW} \)
- Tensión DC: \( \pm 320\,\text{kV} \Rightarrow V_{dc} = 640\,\text{kV} \)
- Longitud del cable: \( \ell = 300\,\text{km} \)
- Cable XLPE DC-grade, conductor de cobre

**Paso 1 — Corriente nominal.**

$$ I_{nom} = \frac{P_{nom}}{V_{dc}} = \frac{500\,\text{MW}}{640\,\text{kV}} = 781\,\text{A} $$

**Paso 2 — Sección del conductor.** Para \( I_{nom} = 781\,\text{A} \) en XLPE submarino con
refrigeración por agua de mar, la temperatura máxima es 70°C. La densidad de corriente típica
admisible es ~400–500 A/\(\text{mm}^2 \) depende del número de cables paralelos y la enterramiento. Con
\( J = 500\,\text{A/m}^2\rightarrow A_{cond}=781/500 \approx 1.6\,\text{mm}^2 \) — para conductores
en mm² habituales se elige 1600 mm² (sección normalizada). Con cobre:

$$ R_{km} = \frac{\rho_{Cu}}{A_{cond}} = \frac{17.2\,\text{n}\Omega\cdot\text{m}}{1600\times10^{-6}\,\text{m}^2} = 0.01075\,\Omega/\text{km} $$

**Paso 3 — Parámetros totales del cable.**

$$ R_{total} = R_{km}\times\ell = 0.01075\times300 = 3.22\,\Omega $$
$$ L_{total} = L_{km}\times\ell = 0.4\,\text{mH/km}\times300 = 120\,\text{mH} $$
$$ C_{total} = C_{km}\times\ell = 0.2\,\mu\text{F/km}\times300 = 60\,\mu\text{F} $$

**Paso 4 — Pérdidas Joule en el cable.**

$$ P_{cable} = I_{nom}^2\times R_{total} = 781^2\times3.22 = 1.96\,\text{MW} \quad (0.39\,\%) $$

**Paso 5 — Frecuencia de resonancia LC.**

$$ f_{res} = \frac{1}{2\pi\sqrt{L_{total}\,C_{total}}} = \frac{1}{2\pi\sqrt{0.12\times60\times10^{-6}}} \approx 59\,\text{Hz} $$

Modos SSO resultantes: 50 ± 59 Hz → 9 Hz (subsíncrono) y 109 Hz (supersíncrono).

**Paso 6 — Corriente de falta DC pico** (cortocircuito bipolar en el punto medio):

$$ Z_c = \sqrt{L_{total}/C_{total}} = \sqrt{120\times10^{-3}/60\times10^{-6}} = 44.7\,\Omega $$
$$ I_{fault,pico} \approx \frac{V_{dc}}{Z_c} = \frac{640\,\text{kV}}{44.7\,\Omega} = 14.3\,\text{kA} \approx 18\,I_{nom} $$

**Paso 7 — Energía almacenada en el cable.**

$$ W_{cable} = \frac{1}{2}\,C_{total}\,V_{dc}^2 = \frac{1}{2}\times60\times10^{-6}\times(640\times10^3)^2 = 12.3\,\text{MJ} $$

Esta energía es comparable a la almacenada en el propio MMC (~17.5 MJ para 500 MVA a 35 kJ/MVA)
y constituye la reserva de energía del sistema que amortigua los transitorios de potencia durante
cambios de despacho o faltas AC parciales.

| Resultado | Valor |
|---|---|
| \( I_{nom} \) | 781 A |
| \( R_{total} \) | 3.22 Ω |
| \( C_{total} \) | 60 µF |
| Pérdidas Joule | 1.96 MW (0.39 %) |
| \( f_{res,LC} \) | 59 Hz |
| \( I_{fault,pico} \) | 14.3 kA (18 pu) |
| \( W_{cable} \) | 12.3 MJ |

<div class="cfig"><img src="../figuras/hvdc-cable-dc-analisis.png" alt="Cable DC HVDC: modelo π, resonancia LC y corriente de falta"><div class="cap">Parámetros del cable de 300 km, respuesta de \( V_{dc} \) ante escalón de carga, impedancia del cable (resonancia LC a ~59 Hz), y corriente de falta bipolar DC (hasta ~18 pu en pocos ms).</div></div>
