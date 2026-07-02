---
titulo: Fault ride-through (LVRT/HVRT) e inyección de reactiva
slug: fault-ride-through
categoria: control
tipo: tecnica
nivel: avanzado
proyectos: []
objetivos: [mantener el convertidor conectado durante huecos y dar soporte de tensión]
tags: [frt, lvrt, hvrt, hueco-tension, reactiva, grid-code, desequilibrio, avanzado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-02
relacionados: [current-limiting, componentes-simetricas, pll-srf, servicios-red-soporte, droop-control]
referencias:
  - "ENTSO-E, Requirements for Generators (RfG) / Network Codes"
  - "Teodorescu, Liserre, Rodríguez, Grid Converters for PV and Wind Power Systems, Wiley 2011"
  - "Neumann & Erlich, Modelling and Control of Doubly Fed Induction Generator for Wind Turbines, IEEE TEC 2012"
---

## Definición
Capacidad —exigida por los grid codes— de un convertidor de **permanecer conectado** durante un
hueco (LVRT) o sobretensión (HVRT) de red y, además, **inyectar corriente reactiva** para sostener
la tensión durante la falta.

## Fundamento teórico
**Curva de tensión-tiempo.** El código define una envolvente \( V(t) \): por encima de la curva el
convertidor no debe desconectar (p.ej. soportar 0 p.u. durante 150–250 ms). HVRT es la envolvente
superior simétrica.

**Inyección de reactiva.** Durante el hueco se prioriza corriente reactiva según una pendiente
\( k \) (típ. \( k\ge2 \)):
$$ \Delta I_q = k\,\Delta V \quad (\text{p.u.}),\qquad \Delta V = 1-V_{pcc} $$
con \( I_q \) saturada a \( I_{max} \). La activa se recorta para respetar el límite de corriente
([[current-limiting]]).

**Faltas asimétricas.** La mayoría de huecos son desequilibrados → aparece **secuencia negativa**
([[componentes-simetricas]]). Hay que:
- Detectar secuencias rápido y limpio (PLL de doble secuencia, [[pll-srf|DSOGI-PLL]]).
- Decidir estrategia de referencia de corriente: inyectar solo secuencia positiva (tensión
  equilibrada del convertidor), o también negativa para soportar/equilibrar, controlando la
  oscilación de potencia de \( 2\omega \) que el desequilibrio induce en el bus DC.
$$ p(t)=P_0+P_{c2}\cos2\omega t+P_{s2}\sin2\omega t $$
Las referencias \( i_{dq}^{\pm*} \) se eligen para anular el rizado de potencia activa **o** de
reactiva (no ambos a la vez), según objetivo.

<div class="cfig"><img src="figuras/fault-ride-through-lvrt.png" alt="envolvente LVRT y curva de inyeccion de reactiva"><div class="cap">Izquierda: envolvente LVRT del grid code; mientras la tensión del PCC quede por encima de la curva, el convertidor no debe desconectar (debe soportar 0 pu durante ~150 ms). Derecha: durante el hueco se prioriza corriente reactiva proporcional a la caída, $\Delta I_q=k\,\Delta V$, saturada a $I_{max}$.</div></div>

## 1 — Derivación de Δiq = k·ΔV/Vn desde el requisito del grid code

**Paso 1 — objetivo normativo.** Durante un hueco de tensión, el grid code exige que el convertidor aporte corriente reactiva para sostener la tensión en el PCC. La norma (p.ej. ENTSO-E RfG, VDE-AR-N 4120) establece que el incremento de corriente reactiva sea proporcional al hueco:

$$ \Delta I_q = k\,\frac{\Delta V}{V_n}, \qquad \Delta V = V_n - V_{pcc} $$

con \( k\ge2 \) p.u./p.u. (al menos 2 A de reactiva por cada 1 p.u. de caída de tensión).

**Paso 2 — sustento físico.** La tensión en el PCC se puede aproximar como \( V_{pcc}\approx V_{grid}-X_{red}\,I_q \) (para red predominantemente inductiva). Un aumento \( \Delta I_q \) en la corriente reactiva produce una subida de tensión \( \Delta V_{pcc}\approx X_{red}\,\Delta I_q \). La pendiente \( k \) establece cuánta reactiva se inyecta por unidad de caída: cuanto mayor \( k \), mayor soporte de tensión, pero también mayor riesgo de sobrepasar \( I_{max} \).

**Paso 3 — límite de corriente.** La corriente total está limitada por la capacidad del puente (\( I_{max} \)), por lo que la corriente reactiva inyectada se satura:

$$ I_q^* = \min\!\left(k\,\Delta V,\; I_{max}\right) $$

y la activa se recorta al valor restante:

$$ I_d^* = \sqrt{\max\!\left(I_{max}^2 - (I_q^*)^2,\;0\right)} $$

**Paso 4 — ejemplo numérico.** Para un hueco \( \Delta V=0.3 \) p.u. y \( k=2 \): \( \Delta I_q=2\times0.3=0.6 \) p.u. Si \( I_{max}=1.0 \) p.u., la activa disponible queda \( I_d^*=\sqrt{1-0.36}=0.8 \) p.u.

$$ \boxed{\Delta I_q = k\,\Delta V,\quad k\ge2\;\text{p.u./p.u.}} $$

## 2 — Tipos de huecos y clasificación (IEC 61400-21)

La norma IEC 61400-21 (y su equivalente EN 50160) clasifica los huecos en **siete tipos** (A–G)
según la simetría de la falta. El tipo determina qué componentes simétricas aparecen y, por tanto,
cómo debe responder el control.

**Paso 1 — hueco simétrico (tipo A, trifásico).** Los tres terminales caen igual: solo aparece
secuencia positiva. La PLL convencional ve una tensión reducida pero equilibrada y puede seguirla
sin problema. El control DQ estándar es suficiente:

$$ \mathbf{V}_{pcc} = V_{ret}\angle\theta \quad (\text{solo }+),\qquad v_{ret}=\frac{V_{pcc}}{V_{nom}} $$

**Paso 2 — huecos asimétricos (tipos B–G).** Cualquier falta monofásica (tipo B/C) o bifásica
(tipo D–G) rompe la simetría. Aparece **secuencia negativa** giratoria a \(-\omega_1\):

$$ \mathbf{V}_{pcc} = V^+\angle(+\omega_1 t + \phi^+) + V^-\angle(-\omega_1 t + \phi^-) $$

La componente negativa produce en el marco DQ una oscilación a \( 2\omega_1 \) (100 Hz en sistemas
de 50 Hz). Una PLL de lazo único intenta seguirla y oscila → hay que usar [[pll-srf|DSOGI-PLL]] o
DDSRF-PLL para separar secuencias.

**Paso 3 — clasificación por profundidad y duración.** Se define la retención de tensión
\( v_{ret}=V_{pcc}/V_{nom} \). Los valores típicos del P.O. 12.3 (España) son:
- Duración de 0 pu: hasta 150 ms
- Recuperación a 0.8 pu: en 500 ms totales
- Recuperación completa (≈1 pu): en ~1500 ms

La **duración** del hueco (150–250 ms para faltas despejadas por protección de distancia en 220 kV)
determina cuánta energía acumula el bus DC y si el chopper de freno es necesario.

**Paso 4 — tabla de los siete tipos de hueco.**

| Tipo | Falta | Fases afectadas | Seq. negativa | Seq. homopolar |
|------|-------|-----------------|---------------|----------------|
| A | Trifásica simétrica | a, b, c | No | No |
| B | Monofásica a tierra | a | Sí | Sí |
| C | Bifásica (sin tierra) | b-c | Sí | No |
| D | Bifásica a tierra | b-c-g | Sí | Sí |
| E | Trifásica a tierra | a-b-c-g | No | Sí |
| F | Bifásica con despl. ángulo | b-c variante | Sí | No |
| G | Bifásica a tierra con despl. | variante | Sí | Sí |

La presencia de secuencia negativa exige descomponer la medida de \( V_{pcc} \) y generar
referencias \( i_{dq}^{+*} \) e \( i_{dq}^{-*} \) separadas. Sin DSOGI, la oscilación a \( 2\omega_1 \)
contamina la referencia y la corriente oscila visiblemente.

## 3 — La corriente durante el hueco: límite de sobrecorriente

El problema más inmediato no es el control: es que la corriente puede dispararse antes de que
cualquier algoritmo reaccione.

**Paso 1 — el escenario sin limitación.** Si el convertidor opera a \( P=P_n \) y la tensión cae
de 1 pu a 0.1 pu con potencia constante, la corriente activa debe subir \( 10\times \):

$$ I_d = \frac{P}{V_{pcc}} = \frac{P_n}{0.1\,V_n} = 10\,I_n $$

Los IGBT/SiC pueden soportar 1.5–2 pu de corriente de pico durante microsegundos, no 10 pu. El
disparo por sobrecorriente (desaturación de IGBT o activo) ocurre en \( <1\,\text{ms} \) —antes
de que el PI de corriente pueda actuar.

**Paso 2 — current limiting activo.** La solución es imponer \( |\mathbf{i}|\le I_{max} \) en la
referencia antes de entrar al controlador. Se limita el módulo del vector de corriente:

$$ |\mathbf{i}^*| = \sqrt{(i_d^*)^2 + (i_q^*)^2} \le I_{max} \quad (1.1\text{–}1.5\,\text{pu}) $$

Se eligen 1.1 pu para dejar margen térmico sostenido (régimen de falta puede durar 150 ms).
Hasta 1.5 pu si el disipador admite la energía.

**Paso 3 — prioridad reactiva.** El grid code exige soporte de tensión → \( i_q^* \) tiene
prioridad. Una vez determinada \( i_q^* \), la activa usa el margen sobrante:

$$ i_q^* = k\,(1-V_{pcc}), \quad i_d^* = \sqrt{\max(I_{max}^2 - (i_q^*)^2,\;0)} $$

Ejemplo para hueco grave (\( V_{pcc}=0.2 \) pu, \( k=4 \), \( I_{max}=1.1 \) pu):

$$ i_q^* = 4\times0.8 = 3.2\;\text{pu} \;\to\;\text{satura a }1.1\;\text{pu},
   \quad i_d^* = \sqrt{1.21-1.21} = 0\;\text{pu} $$

La potencia activa cae a **cero**: todo el convertidor inyecta reactiva. El bus DC absorbe la
energía de la fuente (PV/viento): entra el chopper o se limita la entrada de fuente.

**Paso 4 — implementación con anti-windup.** El limitador de corriente crea saturación en la
referencia → el integrador del PI puede seguir integrando hacia el infinito (windup). Se necesita
[[anti-windup]] en el lazo de corriente durante el hueco, con back-calculation referenciada a la
saturación del limitador de corriente (no del modulador).

## 4 — Soporte de tensión: la curva k·ΔV y su derivación

El soporte de tensión es el fundamento del FRT moderno: no se trata solo de sobrevivir el hueco,
sino de **ayudar a recuperar la tensión del PCC**.

**Paso 1 — modelo de la red en el PCC.** Para una red predominantemente inductiva (\( R\ll X \)):

$$ V_{pcc} \approx V_{grid} - X_{red}\,i_q $$

donde \( i_q \) es la corriente reactiva inyectada (positiva = inductiva desde la red, capacitiva
desde el convertidor → sube tensión). El incremento de iq produce:

$$ \Delta V_{pcc} = X_{red}\,\Delta i_q $$

**Paso 2 — la pendiente k del grid code.** El grid code exige que cuando la tensión cae
\( \Delta V = 1 - V_{pcc} \), el convertidor inyecte:

$$ i_q^* = k\,\Delta V = k\,(1 - V_{pcc}) $$

La tensión en el PCC sube en:

$$ \Delta V_{PCC} = X_{red}\,k\,(1-V_{pcc}) $$

La condición para que el soporte sea eficaz es que este incremento sea significativo frente a la
caída. Para \( X_{red}=0.1 \) pu y \( k=4 \):
si \( V_{pcc}=0.5 \) pu → \( i_q^*=2 \) pu → sube \( 0.2 \) pu → PCC sube a 0.7 pu. Si está
saturado a \( I_{max}=1.1 \) pu → sube \( 0.11 \) pu → PCC sube a 0.61 pu.

**Paso 3 — diseño de k en función de la red.** La pendiente óptima depende de \( X_{red} \):
cuanto más débil la red, mayor \( X_{red} \) y mayor efecto de la inyección de reactiva. En red
muy fuerte (\( X_{red}\to0 \)) el soporte de tensión es ineficaz y lo que importa es no disparar.

| \( X_{red} \) [pu] | \( k=2 \) | \( k=4 \) | \( k=6 \) |
|---------------------|-----------|-----------|-----------|
| 0.05 | +5% V por pu | +10% V por pu | saturado |
| 0.10 | +10% V por pu | +20% V por pu | saturado |
| 0.20 | +20% V por pu | saturado | saturado |

**Paso 4 — ejemplo completo:** \( V_{pcc}=0.5 \) pu, \( k=4 \), \( I_{max}=1.1 \) pu:
\( i_q^*=4\times0.5=2\;\text{pu}\to\text{satura a }1.1\;\text{pu} \).
\( i_d^*=\sqrt{1.21-1.21}=0\;\text{pu} \). Potencia activa entregada = 0. Toda la capacidad del
convertidor va al soporte de tensión.

$$ \boxed{i_q^* = \min(k\,(1-V_{pcc}),\; I_{max}),\quad i_d^* = \sqrt{\max(I_{max}^2-(i_q^*)^2,\;0)}} $$

## 5 — FRT en grid-forming: diferencias con GFL

El grid-forming (GFM) tiene una arquitectura fundamentalmente diferente que cambia cómo afronta
el hueco.

**Paso 1 — la fuente de tensión como punto de partida.** El GFM es una fuente de tensión
controlada: mantiene \( E\angle\delta \) constante en sus terminales (o casi). Cuando la red cae a
\( V_{pcc}=0.2 \) pu, la diferencia \( E-V_{pcc}\approx0.8 \) pu impulsa corriente a través de
\( Z_{filtro} \):

$$ I = \frac{E - V_{pcc}}{Z_{LCL}} $$

La corriente sube sola sin que el control haga nada. El GFM **no** tiene inherentemente current
limiting: hay que añadirlo explícitamente.

**Paso 2 — current limiting en GFM: impedancia virtual.** La estrategia más efectiva es aumentar
la impedancia de salida del GFM durante el hueco (impedancia virtual):

$$ V^*_{conv} = E\angle\delta - Z_{virt}\,\mathbf{i} $$

donde \( Z_{virt} \) se sube cuando \( |\mathbf{i}|>I_{max} \). Esto reduce la corriente sin
cambiar la referencia de tensión del GFM (el GFM sigue siendo fuente de tensión para la red).

**Paso 3 — la sincronía en el GFM.** El GFM sincroniza mediante droop de potencia o VSM: el
ángulo \( \delta \) integra el error de potencia \( P^*-P \). Durante el hueco, \( P_{inyectada} \)
cae (porque la tensión es baja), entonces \( \delta \) intenta aumentar para entregar más potencia.
Hay una **oscilación de rotor virtual** amortiguada por la constante D del droop, pero el sistema
**no pierde sincronía** porque el polo del swing siempre tiene parte real negativa si el
amortiguamiento D es adecuado.

El GFL, en cambio, tiene una PLL que puede perder sincronía si \( V_{pcc} \) cae demasiado rápido
(la fase de la tensión del PCC salta y la PLL no puede seguirla).

**Paso 4 — comparativa FRT: GFL vs GFM.**

| Característica | GFL | GFM |
|----------------|-----|-----|
| Referencia de control | corriente \( i_{dq}^* \) | tensión \( E\angle\delta \) |
| Current limiting | limitar \( i^* \) directo | subir \( Z_{virt} \) |
| Riesgo de pérdida de sincronía | Alto (PLL falla si \( V<0.3\,\text{pu} \)) | Bajo (droop integra) |
| Soporte de tensión | Activo (inyecta \( i_q^* \)) | Inherente (fuente de tensión) |
| Hueco soportable | Hasta ~0.2–0.3 pu sin perder sincronía | Hasta 0.0 pu (con limitador) |
| Complejidad del FRT | Media (prioridad de \( i_q \)) | Alta (coordinación \( Z_{virt} \)) |

<div class="cfig"><img src="figuras/fault-ride-through-analisis.png" alt="analisis completo FRT: curva LVRT, corrientes prioridad reactiva, Vpcc con soporte, GFL vs GFM"><div class="cap">(a) Curva LVRT del P.O. 12.3: 0 pu durante 150 ms, recuperación a 0.8 pu en 500 ms. (b) Prioridad reactiva: con k=4 e Imax=1.1 pu, la corriente reactiva satura y la activa cae a cero para huecos profundos. (c) V_pcc con y sin soporte FRT: la inyección de reactiva sube la tensión en el PCC. (d) GFL vs GFM durante hueco profundo 0.1 pu: el ángulo de la PLL del GFL deriva, el GFM oscila pero mantiene la sincronía.</div></div>

## 6 — Diseño iterativo: FRT para convertidor 1 MVA

Se diseña el sistema FRT para un convertidor trifásico de 1 MVA, 400 V, conectado a red con
\( X_{red}=0.1 \) pu. Grid code: P.O. 12.3. Especificaciones: \( I_{max}=1.1 \) pu, \( k=4 \).

**Paso 1 — detector de hueco.** El umbral de activación del modo FRT:

$$ V_{det} = \frac{|V_{pcc}|}{V_{nom}} < 0.85 \;\text{pu} $$

El filtrado de la medida de tensión es crítico: un MAF (Moving Average Filter) de un período de
red (20 ms) elimina el rizado pero da 20 ms de retardo → demasiado para una detección rápida.
Se prefiere un filtro paso bajo de \( \tau=5\,\text{ms} \) o un DSOGI que ya separa secuencias.
Se añade un **debounce de 10 ms**: la condición debe mantenerse 10 ms antes de activar FRT (evitar
activaciones por transitorios breves de 1-2 ciclos de conmutación).

**Paso 2 — transición al modo FRT.** Al detectar el hueco, se activa la lógica de prioridad
reactiva. Las referencias cambian suavemente (rampa de 2 ms) para evitar escalones de corriente:

```python
def frt_refs(Vpcc, Imax, k=4.0):
    dV = max(0.0, 1.0 - Vpcc)
    iq = min(k * dV, Imax)
    id_ = (max(Imax**2 - iq**2, 0.0)) ** 0.5
    return id_, iq
```

El [[anti-windup]] se activa durante el FRT: la referencia de potencia activa se congela (evita
que el droop DC siga integrando) y el integrador del PI de corriente usa back-calculation.

**Paso 3 — recuperación post-falta.** Al despejarse el hueco, la tensión puede subir bruscamente
y la potencia activa intentar recuperarse instantáneamente → sobrecorriente. Se aplica una **rampa
de recuperación de potencia activa de 100 ms**:

$$ i_d^*(t) = i_{d,min}^* + \frac{t_{rec}}{100\,\text{ms}}\,(i_{d,nom}^* - i_{d,min}^*) $$

donde \( t_{rec} \) es el tiempo desde que \( V_{pcc}>0.85 \) pu de nuevo y \( i_{d,min}^* \) es
el valor final del FRT.

**Tabla resumen: referencias por nivel de hueco.**

| \( V_{pcc} \) [pu] | \( i_q^* \) [pu] | \( i_d^* \) [pu] | \( P_{iny} \) [pu] |
|---------------------|------------------|------------------|---------------------|
| 1.00 | 0.00 | 1.00 | 1.00 |
| 0.85 | 0.60 | 0.90 | 0.77 |
| 0.70 | 1.10 (sat.) | 0.00 | 0.00 |
| 0.50 | 1.10 (sat.) | 0.00 | 0.00 |
| 0.20 | 1.10 (sat.) | 0.00 | 0.00 |
| 0.00 | 1.10 (sat.) | 0.00 | 0.00 |

Para huecos menores de \( V_{pcc}<0.725 \) pu (con \( k=4 \), \( I_{max}=1.1 \) pu), toda la
capacidad del convertidor va a reactiva y la potencia activa entregada es cero. El bus DC debe
absorber esa energía mediante chopper o limitación de la fuente primaria.

## Cuándo y por qué se usa
Obligatorio para conexión a red de PV/eólica/almacenamiento. Crítico en grid-forming, donde además
hay que limitar corriente sin perder la fuente de tensión (transición a modo limitado).

## Procedimiento de diseño (genérico)
1. Toma la curva LVRT/HVRT y la pendiente \( k \) del grid code aplicable.
2. Implementa detección rápida de secuencias ([[pll-srf|DSOGI-PLL]]).
3. Genera referencias \( i_{dq}^{\pm*} \) priorizando reactiva, con la estrategia de rizado elegida.
4. Aplica [[current-limiting]] con prioridad a \( I_q \) y anti-windup.
5. Gestiona el bus DC durante la falta (chopper/recorte de activa) y la **recuperación** post-falta.
6. Valida con huecos simétricos y asimétricos a distintas profundidades.

## Ejemplo de código
```python
def frt_refs(Vpcc, Imax, k=2.0):
    dV = 1.0 - Vpcc
    iq = min(k*dV, Imax)                 # reactiva prioritaria (p.u.)
    id_ = (max(Imax**2 - iq**2, 0.0))**0.5  # activa con la corriente restante
    return id_, iq
```

## Parámetros y valores típicos
LVRT: soportar 0 p.u. durante 150–250 ms; pendiente \( k=2\text{–}6 \). Tiempo de respuesta de
reactiva < 30–60 ms. Límite de corriente 1.0–1.2 p.u.

## Errores comunes
- Detección de secuencia lenta → respuesta de reactiva tardía y disparo por sobrecorriente.
- Saturar corriente sin prioridad clara → ni soporta tensión ni protege el puente.
- Olvidar el rizado de \( 2\omega \) en el bus DC durante faltas asimétricas.
- No gestionar la **recuperación** (sobretensión/sobrecorriente al despejar la falta).
- En GFM: no activar la limitación de corriente virtual → la diferencia \( E-V_{pcc} \) impulsa corriente ilimitada.

## Conceptos relacionados
- [[current-limiting]] · [[componentes-simetricas]] · [[pll-srf|DSOGI-PLL]] · [[servicios-red-soporte]] · [[droop-control]] · [[impedancia-virtual]]

## Referencias
- ENTSO-E, *Requirements for Generators (RfG)*.
- Teodorescu, Liserre, Rodríguez, *Grid Converters for PV and Wind Power Systems*, 2011.
- Neumann & Erlich, *Modelling and Control of DFIG for Wind Turbines*, IEEE TEC 2012.
