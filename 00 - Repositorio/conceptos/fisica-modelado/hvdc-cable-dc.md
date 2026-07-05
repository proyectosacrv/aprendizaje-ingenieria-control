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

<div class="cfig"><img src="../figuras/hvdc-cable-dc-analisis.png" alt="Cable DC HVDC: modelo π, resonancia LC y corriente de falta"><div class="cap">Parámetros del cable de 300 km, respuesta de \( V_{dc} \) ante escalón de carga, impedancia del cable (resonancia LC a ~59 Hz), y corriente de falta bipolar DC (hasta ~18 pu en pocos ms).</div></div>
