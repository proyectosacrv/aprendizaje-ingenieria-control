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

## Conceptos relacionados
- [[dinamica-bus-dc|carga de potencia constante (CPL)]] · [[vsm-inercia]]

## Referencias
- Informes de operadores de red sobre integración de data centers (2024-2025).
