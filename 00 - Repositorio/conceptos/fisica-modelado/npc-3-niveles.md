---
titulo: NPC de 3 niveles — topología, conmutación y balance de neutro
slug: npc-3-niveles
categoria: fisica-modelado
tipo: concepto
nivel: avanzado
proyectos: []
objetivos: [analizar la topologia NPC completa, derivar la tabla de conmutacion, modelar el balance del punto neutro, dimensionar sus componentes]
tags: [NPC, neutral-point-clamped, multinivel, 3-niveles, punto-neutro, PD-PWM, diodos-anclaje, THD, dv-dt, dimensionado, dq]
fecha_creacion: 2026-07-31
fecha_actualizacion: 2026-07-31
relacionados: [topologias-multinivel, convertidor-vsc, marco-dq, semiconductores-potencia, filtro-lcl, armonicos-thd, control-vectorial, control-cascada]
referencias:
  - "Nabae, Takahashi, Akagi, A New Neutral-Point-Clamped PWM Inverter, IEEE TIA 1981"
  - "Rodriguez, Lai, Peng, Multilevel Inverters: Survey of Topologies, IEEE TIE 2002"
  - "Holmes, Lipo, Pulse Width Modulation for Power Converters, IEEE Press 2003"
  - "Bruckner, Bernet, Guldner, The Active NPC Converter and Its Loss-Balancing Control, IEEE TIE 2005"
  - "Celanovic, Boroyevich, A Comprehensive Study of Neutral-Point Voltage Balancing in 3-Level NPC, IEEE TPEL 2000"
---

## Definición
El **NPC** (*Neutral-Point-Clamped*, también llamado *diode-clamped*) es el convertidor multinivel más
usado en la industria: una rama de fase con **4 interruptores** y **2 diodos de anclaje** al punto medio
("neutro") de un bus DC partido en dos condensadores. Sintetiza **3 niveles** de tensión de salida
(\(+V_{dc}/2\), \(0\), \(-V_{dc}/2\)), reduciendo a la mitad el \(dv/dt\) y a un cuarto el rizado de
corriente frente al puente de 2 niveles, al precio de un reto de control adicional: mantener equilibrados
los dos condensadores del bus (**balance del punto neutro**).

## Fundamento teórico
El bus DC se parte en dos condensadores \(C_1\) (entre P y O) y \(C_2\) (entre O y N), cada uno a
\(V_{dc}/2\) en régimen ideal. Cuatro interruptores en serie (\(T_1\)–\(T_4\)) y dos diodos de anclaje
(\(D_1\), \(D_2\)) conectan la salida de fase a P, O o N según qué par de interruptores adyacentes esté
activo. Cada dispositivo bloquea solo \(V_{dc}/2\): se pueden usar semiconductores de la mitad de tensión
que en un puente de 2 niveles para el mismo \(V_{dc}\), o doblar \(V_{dc}\) con la misma tecnología.

<div class="cfig"><img src="figuras/npc-topologia.png" alt="rama de fase del NPC de 3 niveles con los cuatro IGBTs T1-T4, los dos diodos de anclaje D1 y D2 al punto neutro O, y los dos condensadores de bus C1 y C2"><div class="cap">Rama de fase del NPC: \(T_1\)–\(T_4\) en serie entre P y N; \(D_1\) ancla el punto medio de \(T_1\)-\(T_2\) al neutro O cuando la salida está a \(0\) con \(i_o>0\); \(D_2\) hace lo mismo para \(i_o<0\). \(C_1\), \(C_2\) parten el bus DC.</div></div>

## 1 — Tabla de estados de conmutación (completa)

**Regla de complementariedad.** Para no cortocircuitar el bus, \(T_1\) y \(T_3\) son **complementarios**
(\(T_3=\overline{T_1}\)) y \(T_2\) y \(T_4\) también (\(T_4=\overline{T_2}\)). Con dos variables libres
(\(T_1\), \(T_2\)) hay 4 combinaciones binarias, pero **una es redundante** en corriente para el estado 0
(según el signo de \(i_o\)):

<div class="cfig"><img src="figuras/npc-conmutacion.png" alt="tabla de estados de conmutacion del NPC mostrando el estado de T1 T2 T3 T4 y la tension de salida para cada nivel P, O+ (io positivo), O- (io negativo) y N, junto con las formas de onda de la modulacion PD-PWM con dos portadoras y el espectro comparado con dos niveles"><div class="cap">(a) Tabla completa de estados: los cuatro niveles lógicos con el estado de cada interruptor y el diodo que conduce en el nivel 0. (b) Modulación PD-PWM: dos portadoras triangulares apiladas (una entre 0 y 1, otra entre −1 y 0) comparadas con la misma referencia generan directamente los 3 niveles. (c) El contenido armónico alrededor de \(f_{sw}\) cae mucho más rápido que en 2 niveles.</div></div>

**Deducción de la regla de complementariedad (por qué exactamente esos pares).** La rama tiene 4
interruptores en serie entre P y N. Si se permitieran combinaciones distintas de las de la tabla, dos casos
son físicamente inadmisibles:

- \(T_1=T_3=1\) simultáneamente: \(T_1\) conecta P al nudo entre \(T_1\)-\(T_2\), y \(T_3\) conecta ese
  mismo nudo (a través de \(T_2\), que en este caso también debe pensarse en su combinación) hacia el
  nudo O. Si además \(T_2=1\), P quedaría cortocircuitado a O a través de \(C_1\): corriente de
  cortocircuito limitada solo por la impedancia parásita del lazo → destrucción del dispositivo.
- Análogamente \(T_2=T_4=1\) cortocircuita O a N a través de \(C_2\).

Por tanto la única familia de combinaciones **seguras y que cubre los tres niveles** es la de la tabla:
\((T_1,T_2)\in\{(1,1),(0,1),(0,0)\}\) con \(T_3=\overline{T_1}\), \(T_4=\overline{T_2}\). La combinación
\((T_1,T_2)=(1,0)\) **no se usa**: dejaría al nudo intermedio T1-T2 conectado a P por \(T_1\) pero
desconectado de la salida (ni O ni N), un estado sin sentido para la síntesis de tensión.

| Estado | \(T_1\) | \(T_2\) | \(T_3\) | \(T_4\) | Dispositivo que conduce | \(v_{aO}\) |
|---|---|---|---|---|---|---|
| **P** | 1 | 1 | 0 | 0 | \(T_1, T_2\) | \(+V_{dc}/2\) |
| **O** (\(i_o>0\)) | 0 | 1 | 1 | 0 | \(D_1\), \(T_2\) | \(0\) |
| **O** (\(i_o<0\)) | 0 | 1 | 1 | 0 | \(D_2\), \(T_3\) | \(0\) |
| **N** | 0 | 0 | 1 | 1 | \(T_3, T_4\) | \(-V_{dc}/2\) |

**Por qué el estado O tiene dos caminos.** Con \(T_2\) y \(T_3\) en ON, la salida queda "flotando" entre P y
N a través de esos dos interruptores; el **diodo de anclaje** que realmente conduce lo decide el signo de
la corriente de fase \(i_o\), no una elección de control:
- Si \(i_o>0\) (la fase entrega corriente hacia la carga desde O), la corriente sale por \(T_2\) y
  **entra** por \(D_1\) desde el nudo O — \(D_1\) ancla la salida a O tirando de energía de \(C_1\).
- Si \(i_o<0\), la corriente circula al revés y es \(D_2\) quien conduce, tirando de \(C_2\).

**Verificación por KVL de cada estado.** Tomando O como referencia (\(v_O=0\)):
- Estado P: \(v_{aO}=v_P-v_O\). Como \(T_1,T_2\) conducen con caída ideal nula, \(v_a=v_P\), y
  \(v_P-v_O\) es la tensión de \(C_1\) → \(v_{aO}=+V_{dc}/2\). ✓
- Estado N: simétrico, \(v_a=v_N\), \(v_{aO}=v_N-v_O=-V_{dc}/2\) (tensión de \(C_2\) con signo). ✓
- Estado O: \(v_a=v_O\) directamente (por el diodo que ancla), luego \(v_{aO}=0\) por construcción,
  **independientemente** de \(i_o\) — el signo de \(i_o\) decide *qué diodo* ancla, pero el nivel de tensión
  resultante es el mismo (0), que es justamente la propiedad de anclaje que da nombre a la topología.

Esta dependencia del signo de \(i_o\) en **quién conduce** (aunque el nivel de tensión no cambie) es la
**raíz física** del problema de balance de neutro (apartado 3): cada vez que el convertidor está en el
estado O, uno de los dos condensadores se descarga un poco y el otro se carga, y quién lo hace depende de
\(i_o\), no de una decisión del modulador.

**Nunca usar T1 y T3 (o T2 y T4) a la vez:** cortocircuitaría directamente \(C_1\) o \(C_2\) a través de dos
interruptores en conducción simultánea (falta de brazo). El *deadtime* entre la orden de un interruptor y su
complementario debe respetarse igual que en 2 niveles (ver [[semiconductores-potencia]]), y en el NPC hay
un matiz adicional: durante el deadtime en la transición P↔O (o O↔N), la corriente de carga fuerza el paso
transitorio por el estado O a través de los diodos de anclaje — es decir, el propio deadtime **ya** pasa por
O, lo cual es seguro (a diferencia de 2 niveles, donde el deadtime deja la salida en alta impedancia).

## 2 — Modulación: PD-PWM con dos portadoras

**Idea.** Se apilan dos portadoras triangulares de amplitud unidad: una entre \([0,1]\) (rige la transición
P↔O) y otra entre \([-1,0]\) (rige la transición O↔N). La referencia \(r(\theta)=m\sin\theta\in[-1,1]\) se
compara contra ambas:

$$ v_{aO}^*(\theta) = \begin{cases} +\dfrac{V_{dc}}{2} & \text{si } r>\text{portadora superior} \\[4pt] -\dfrac{V_{dc}}{2} & \text{si } r<\text{portadora inferior} \\[4pt] 0 & \text{en el resto} \end{cases} $$

Es la generalización directa del comparador de 2 niveles (§2 de [[convertidor-back-to-back]]): con \(N\)
niveles hacen falta \(N-1\) portadoras apiladas (PD-PWM, *phase disposition*), todas en fase entre sí (de
ahí el nombre). Existen variantes POD (portadoras negativas desfasadas 180°) y APOD (todas alternadas), con
distinto reparto de armónicos entre bandas pero el mismo principio.

**Derivación del duty efectivo (paso a paso, generalizando el §5.2 de convertidor-back-to-back).**
Sea \(r(\theta)=m\sin\theta\) la referencia y \(x=r\) su valor instantáneo. Se distinguen dos regiones:

*Región superior* (\(0\le r\le1\), la salida conmuta entre P y O). La portadora superior recorre
\([0,1]\) en cada periodo de conmutación \(T_s\); el interruptor \(T_1\) está en ON mientras \(r\) supera la
portadora. Por la misma geometría del triángulo que en el caso de 2 niveles (donde la fracción de tiempo
por encima de una referencia \(x\in[0,1]\) sobre una rampa \([0,1]\) es \(x\)), el duty en P dentro de este
tramo es:

$$ d_P(\theta) = r(\theta) = m\sin\theta \qquad (0\le m\sin\theta\le 1) $$

y el resto del periodo, \(1-d_P\), la salida está en O.

*Región inferior* (\(-1\le r\le0\)), simétrica: el duty en N es \(d_N=-r=-m\sin\theta\) y el resto,
\(1-d_N\), en O.

**Duty medio en cada nivel a lo largo de un ciclo de red.** Integrando \(d_P(\theta)\) solo donde es
positivo (media onda) se recupera exactamente el mismo resultado que el corchete \((1+m\sin\theta)/2\)
visto para 2 niveles, pero repartido en dos comparaciones de rango mitad: es la razón por la que el "cero"
de referencia de cada comparación está desplazado (0.5 o −0.5 del rango \([0,1]\) o \([-1,0]\) en vez de 0
en un rango \([-1,1]\) único), lo que reduce a la mitad la excursión de portadora que ve cada comparación y,
con ello —según se deriva en el apartado 4— el rizado de corriente.

**Índice de modulación y zona lineal.** Igual que en 2 niveles, \(m\in[0,1]\) es la zona lineal con PD-PWM
senoidal pura; la inyección de secuencia cero (apartado 3, Paso 4) puede además extender el rango en
\(2/\sqrt3\approx1.15\) exactamente por el mismo mecanismo que en 2 niveles (§2.2 de
[[convertidor-back-to-back]]), con la ventaja añadida de que aquí esa misma inyección sirve **a la vez**
para el balance de neutro.

## 3 — El balance del punto neutro (derivación completa)

**Paso 1 — el origen físico.** Del apartado 1: en el estado O, según el signo de \(i_o\), conduce \(D_1\)
(descarga \(C_1\), carga \(C_2\)) o \(D_2\) (descarga \(C_2\), carga \(C_1\)). La corriente que fluye hacia
el nudo O durante ese estado es exactamente \(i_o\):

$$ i_O(t) = i_o(t)\cdot\mathbb{1}[\text{estado} = O] $$

**Paso 2 — la dinámica de los condensadores.** Con \(C_1=C_2=C\), el balance de carga en el nudo O da:

$$ C\,\frac{dV_{C1}}{dt} = -i_O(t), \qquad C\,\frac{dV_{C2}}{dt} = +i_O(t) $$

(si \(i_O>0\) se resta de \(C_1\) y se suma a \(C_2\), como en el Paso 1). Sumando ambas ecuaciones,
\(\dfrac{d(V_{C1}+V_{C2})}{dt}=0\): la tensión **total** del bus \(V_{dc}=V_{C1}+V_{C2}\) no la afecta el
estado O (es un balance interno, no una pérdida de energía total). El **desbalance**
\(\Delta V = V_{C1}-V_{C2}\) evoluciona restando la segunda ecuación de la primera:

$$ \frac{d(\Delta V)}{dt} = -\frac{2\,i_O(t)}{C} $$

**Paso 3 — generalización a las tres fases.** En un NPC trifásico, el nudo O es **común** a las tres ramas,
así que la corriente total hacia O es la suma de las contribuciones de cada fase, cada una activa solo
cuando esa fase está en su propio estado O:

$$ i_{O,total}(t) = \sum_{k\in\{a,b,c\}} i_k(t)\cdot\mathbb{1}[\text{fase }k\text{ en estado O}] $$

y la ecuación del desbalance se generaliza sustituyendo \(i_O\to i_{O,total}\) en el Paso 2. Esta suma sobre
las tres fases es la que se cancela en régimen equilibrado (Paso 4) y la que no se cancela con
desequilibrio (Paso 5).

**Paso 4 — por qué con carga equilibrada el desbalance no se acumula.** Con tensiones y corrientes
trifásicas equilibradas y factor de potencia \(\cos\varphi\), cada fase pasa por el estado O una fracción de
tiempo \(1-|d_k(\theta)|\) con \(d_k\) del apartado 2, desfasada \(120°\) de las otras. Puede demostrarse
(sumando las tres contribuciones \(i_k\cdot\mathbb{1}[\text{fase }k\text{ en O}]\) con sus desfases) que la
componente **media** de \(i_{O,total}\) sobre un periodo de red es exactamente cero para cualquier
\(\cos\varphi\) y cualquier \(m\) — es una propiedad de la simetría de 120°, no depende de los valores
concretos. Lo que **sí** queda es una componente oscilante a \(3\omega_0\) (el triple de la fundamental):
integrando esa componente en el Paso 2 el desbalance oscila con una amplitud pico-pico

$$ \Delta V_{pp,osc} \approx \frac{2\,\hat I\,m}{3\,\omega_0\,C}\cdot k(\cos\varphi) $$

donde \(k(\cos\varphi)\) es un factor adimensional del orden de la unidad que depende del ángulo de fase
(máximo cerca de \(\cos\varphi=1\)); esta oscilación es intrínseca a la topología y no se elimina, solo se
dimensiona con \(C\) suficientemente grande (apartado 7, Paso 4).

**Paso 5 — el problema real: componente neta con desequilibrio.** Con carga **desequilibrada** entre fases,
factor de potencia distinto por fase, o un transitorio asimétrico, la cancelación exacta del Paso 4 deja de
cumplirse y aparece una componente **media no nula** de \(i_{O,total}\). Como el Paso 2 es literalmente un
**integrador puro** en esa componente media, \(\Delta V\) no oscila: **deriva sin límite** con pendiente
constante hasta saturar la modulación o dañar los condensadores.

<div class="cfig"><img src="figuras/npc-neutro.png" alt="esquema de los dos caminos de corriente en el estado O segun el signo de la corriente de fase, y simulacion de la deriva de las tensiones de los dos condensadores del bus sin compensacion frente a la estabilizacion con compensacion proporcional al desbalance"><div class="cap">(a) En el estado O, \(D_1\) o \(D_2\) conducen según el signo de \(i_o\), descargando un condensador y cargando el otro. (b) Ante una componente neta de corriente hacia O (carga desequilibrada), sin compensación el desbalance \(V_{C1}-V_{C2}\) crece linealmente sin límite (Paso 2: es un integrador puro); con una compensación proporcional al desbalance medido, las dos tensiones se mantienen ancladas a \(V_{dc}/2\).</div></div>

**Paso 6 — la corrección: usar la redundancia del estado O.** El modulador **no puede** elegir directamente
qué diodo conduce (lo decide \(i_o\)), pero sí puede desplazar **cuándo** se está en el estado O respecto a
P o N, inyectando una pequeña componente de **secuencia cero** \(v_0\) (común a las tres fases, igual que el
3.er armónico de la modulación de 2 niveles — §2.2 de [[convertidor-back-to-back]]) en la referencia:

$$ r_k^*(\theta) = m\sin(\theta - \phi_k) + v_0, \qquad k\in\{a,b,c\} $$

Un \(v_0\) sesgado hacia el nivel P alarga el tiempo relativo en P/O⁺ y acorta O⁻/N (o viceversa),
cambiando el **tiempo neto** que cada fase pasa en cada tramo del estado O y, con ello, el signo neto del
desbalance que se corrige. Un lazo de control mide \(\Delta V = V_{C1}-V_{C2}\) y ajusta \(v_0\) en
proporción (o con un PI) para llevarlo a cero — es exactamente el mecanismo simulado en el panel (b) de la
figura anterior.

**Paso 7 — modelo del lazo de compensación.** Linealizando alrededor del punto de equilibrio, la corriente
correctiva que aporta un \(v_0\) pequeño es aproximadamente proporcional a \(v_0\) y a la corriente de
carga \(\hat I\) (más \(v_0\) desvía más tiempo relativo, y a mayor corriente esa desviación de tiempo
mueve más carga):

$$ i_{O,corr} \approx k_v\,\hat I\,v_0, \qquad k_v = \text{cte. geométrica del PD-PWM (del orden de }1\text{)} $$

con un controlador \(v_0 = -K_{bal}\,\Delta V\) (proporcional, o PI), la dinámica en lazo cerrado del
desbalance (sustituyendo en el Paso 2 con signo negativo de realimentación) es de **primer orden**:

$$ \frac{d(\Delta V)}{dt} = -\frac{2}{C}\big(i_{O,total,dist} - k_v\hat I K_{bal}\Delta V\big)
   \quad\Longrightarrow\quad \tau_{bal} = \frac{C}{2\,k_v\,\hat I\,K_{bal}} $$

Cuanto mayor \(K_{bal}\), más rápido el lazo (menor \(\tau_{bal}\)), pero un \(K_{bal}\) excesivo hace que
\(v_0\) sea grande y distorsione la modulación de las tres fases (satura antes la referencia,
\(|r_k^*+v_0|>1\)); de ahí el compromiso del apartado 8, Paso 5.

**Paso 8 — límite del método y alternativas.** La inyección de secuencia cero corrige desbalances
**lentos** (frecuencia de red y menores). Para desbalances instantáneos grandes (arranque, faltas
asimétricas), se recurre al **NPC activo** (ANPC, con interruptores adicionales que permiten forzar el
camino de corriente independientemente de \(i_o\)) o a un lazo de control más rápido sobre la propia
modulación de cada fase individualmente.

## 4 — \(dv/dt\) y contenido armónico (derivación cuantitativa completa)

**Paso 1 — tensión de bloqueo y \(dv/dt\).** Del desarrollo general de [[topologias-multinivel]] (apartado
1), con \(n=3\):

$$ V_{bloqueo} = \frac{V_{dc}}{n-1} = \frac{V_{dc}}{2}, \qquad \frac{dv}{dt}\bigg|_{NPC} = \frac12\,\frac{dv}{dt}\bigg|_{2L} $$

**Paso 2 — el rizado de corriente, derivado desde cero (no solo el factor final).** Se parte del mismo
razonamiento que en 2 niveles (§5.2, Paso 1-3 de [[convertidor-back-to-back]]): sobre la inductancia de
filtro \(L\), la corriente sube con pendiente \(v_L/L\) durante el tiempo que dura cada nivel de tensión
aplicado. El peor caso ocurre en el cruce por cero de la referencia (donde, en 2 niveles, el duty era 50%).
En el NPC, cerca de \(r\approx0\) la conmutación ocurre **entre O y el nivel adyacente** (P o N, alternando
según el signo instantáneo de \(r\)), con tensión aplicada sobre \(L\) de \(V_{dc}/2\) (en vez de \(V_{dc}\)
en 2 niveles) y con el mismo argumento de "duty ≈ 50% localmente":

$$ \Delta i_{L,NPC,max} \approx \frac{V_{dc}/2}{4\,f_s\,L} = \frac14\cdot\frac{V_{dc}}{4\,f_s\,L} = \frac14\,\Delta i_{L,2L,max} $$

Es la misma fórmula del rizado de 2 niveles (\(V_{dc}/(4f_sL)\)), pero con \(V_{dc}\to V_{dc}/2\): el
salto de tensión efectivo se reduce a la mitad y, como el rizado es lineal en ese salto (no cuadrático —
corrección respecto a un argumento habitual pero impreciso: el \(1/4\) sale de que **también** se reduce a
la mitad el intervalo de tiempo relevante, no de un cuadrado), el rizado cae a un cuarto:

$$ \boxed{\ \frac{\Delta i_{L,NPC}}{\Delta i_{L,2L}} = \frac12\text{(tensión)}\times\frac12\text{(tiempo efectivo)} = \frac14\ } $$

**Paso 3 — verificación por el argumento de energía.** Alternativamente, el rizado pico-pico es
proporcional a \(v_L\cdot t_{on}\); en el peor caso de 2 niveles \(v_L=V_{dc}/2\) durante \(t_{on}=T_s/2\).
En el NPC, al conmutar entre O y P (o N), la tensión aplicada localmente es también \(V_{dc}/2\), **pero**
el intervalo relevante entre conmutaciones dentro de esa transición es la mitad (\(T_s/4\) en vez de
\(T_s/2\), porque cada comparación de portadora cubre solo medio rango de amplitud, según se vio en el
apartado 2): \(\Delta i \propto (V_{dc}/2)\cdot(T_s/4)\) frente a \(V_{dc}\cdot(T_s/4)\)... trabajando ambos
términos con cuidado (ver la derivación completa paso a paso de 2 niveles en §5.2 de
[[convertidor-back-to-back]] y sustituyendo \(V_{dc}\to V_{dc}/2\)) se llega consistentemente al mismo
factor \(1/4\).

**Paso 4 — contenido armónico.** La onda de \(v_{aO}\) de 3 niveles tiene, en las bandas laterales
alrededor de \(f_{sw}\) y sus múltiplos, una amplitud que decae aproximadamente con el **cuadrado** del
número de niveles adicionales, porque cada nivel extra reduce tanto la amplitud del escalón como su
duración relativa (panel (c) de la figura del apartado 1: la caída del NPC frente a 2 niveles no es un
simple factor constante, sino que se acentúa en los armónicos de orden más alto). Esto es lo que permite,
para la misma \(THD\) objetivo, bajar \(f_{sw}\) (menos pérdidas de conmutación) o reducir el filtro de
salida.

**Consecuencia práctica:** esto permite **reducir \(L\) a un cuarto** manteniendo el mismo rizado, o
mantener \(L\) y cuadruplicar la calidad de corriente — ver la comparativa numérica del apartado 5 de
[[topologias-multinivel]]. En la práctica: NPC a 5 kHz + filtro LCL comparable a 2 niveles a 20 kHz.

## 5 — Modulación vectorial (SVM): posiciones, sectores y cálculo de tiempos

La modulación PD-PWM del apartado 2 trabaja **fase a fase**, comparando cada referencia con portadoras.
La **SVM** (Space Vector Modulation) es un método equivalente pero que trabaja directamente con el
**vector de tensión** en el plano αβ, y es el que se usa en los DSP modernos porque optimiza mejor la
secuencia de conmutación y el balance de neutro (aprovechando la redundancia del apartado 1) en el mismo
cálculo.

**Paso 1 — de los estados de conmutación (abc) al plano αβ.** Cada fase del NPC puede estar en el nivel
\(+1\) (P), \(0\) (O) o \(-1\) (N) — usando \(n_k\in\{-1,0,1\}\) como notación compacta del estado de la
fase \(k\). Aplicando la transformación de Clarke (§2.2 de [[convertidor-back-to-back]]) a la terna
\((n_a,n_b,n_c)\,V_{dc}/2\):

$$ \vec V = \frac23\Big(n_a + n_b\,e^{j2\pi/3} + n_c\,e^{j4\pi/3}\Big)\cdot\frac{V_{dc}}{2} $$

Con 3 niveles por fase hay \(3^3=27\) combinaciones \((n_a,n_b,n_c)\), pero al proyectarlas sobre el
plano αβ varias combinaciones distintas caen en el **mismo punto físico** (misma tensión de línea): el
resultado son **19 posiciones distintas** dispuestas en un hexágono con dos anillos y el centro (figura
siguiente, panel a).

<div class="cfig"><img src="figuras/npc-svm.png" alt="hexagono de space vector modulation del NPC con las 19 posiciones fisicas de los 27 estados de conmutacion, distinguiendo vectores cero redundantes triple, vectores medios redundantes doble y vectores largos unicos en las esquinas, y a la derecha el detalle de un triangulo con los tres vectores adyacentes y el vector de referencia descompuesto"><div class="cap">(a) Las 19 posiciones físicas de los 27 estados: el vector cero en el centro es redundante ×3 (PPP, OOO, NNN — no mueve el punto de trabajo), los 6 vectores medios (a media distancia, en los vértices del hexágono interior) son redundantes ×2 (cada uno alcanzable con dos combinaciones de estados, que es la palanca que se usa para el balance de neutro), y los 6 vectores largos de las esquinas son únicos (solo alcanzables con un estado, típicamente todo-P o todo-N combinados). (b) Dentro de cada uno de los 24 triángulos en que queda dividido el hexágono, el vector de referencia \(\vec V_{ref}\) se descompone en sus tres vértices adyacentes.</div></div>

**Paso 2 — clasificación de los vectores por magnitud.** Según su módulo, los 19 vectores se agrupan en
cuatro familias (visibles por color en la figura):

- **Vector cero** (\(|\vec V|=0\)): el origen. Redundante ×3 — los estados PPP, OOO y NNN dan la misma
  tensión de salida (cero en las tres fases), pero llevan corrientes distintas hacia P, O o N,
  respectivamente. Esta redundancia es una **palanca extra** para el balance de neutro (aparte de la del
  estado O individual del apartado 1): elegir PPP en vez de OOO evita tocar el punto neutro en absoluto.
- **Vectores cortos** (módulo pequeño, esquinas del hexágono interior más cercano): alcanzables con
  combinaciones tipo (P,O,O) o (O,N,N) — un único estado por posición en el hexágono de 3 niveles (a
  diferencia del vector medio, no son redundantes en el NPC de 3 niveles porque solo hay una forma de
  llegar a cada uno con niveles \(\{P,O,N\}\) sin repetir la misma posición dos veces).
- **Vectores medios** (módulo intermedio, vértices del hexágono interior mayor, marcados "2×" en la
  figura): redundantes ×2 — p. ej. (P,O,N) y su pareja con roles rotados dan la misma proyección αβ pero
  mueven la corriente de fase por caminos distintos hacia el neutro O, cambiando el signo con que afectan a
  \(\Delta V\). **Esta es la redundancia clave que explota el algoritmo de balance de neutro**: en tiempo
  real, para cada vector medio se elige la combinación que corrige el desbalance medido, sin cambiar en
  absoluto la tensión de salida sintetizada.
- **Vectores largos** (esquinas exteriores, p. ej. PPO, PON...): únicos, un solo estado por posición, no
  aportan grados de libertad para el balance de neutro.

**Paso 3 — sectores y triángulos.** El plano αβ se divide en **6 sectores** de 60° (como en la SVM
clásica de 2 niveles) y, dentro de cada sector, en **4 triángulos** (por los dos anillos de vectores
cortos/medios), dando 24 triángulos en total. El primer paso del algoritmo es identificar en qué sector y
triángulo cae \(\vec V_{ref}\) comparando su ángulo y módulo con los umbrales del hexágono.

**Paso 4 — cálculo de los tiempos (duty cycles) por combinación convexa.** Una vez identificado el
triángulo, sus tres vértices \(\vec V_1,\vec V_2,\vec V_0\) (dos vectores del hexágono más cercano y uno
del más externo, o viceversa según el triángulo) son la base sobre la que se **descompone** el vector de
referencia como combinación convexa — el mismo principio que la SVM clásica de 2 niveles, generalizado a
tres vértices en vez de dos:

$$ \vec V_{ref} = d_1\vec V_1 + d_2\vec V_2 + d_0\vec V_0, \qquad d_1+d_2+d_0=1,\quad d_i\geq0 $$

**Paso 5 — resolución del sistema.** Escribiendo cada vector por sus componentes \((V_{k,\alpha},
V_{k,\beta})\), el sistema anterior son **dos ecuaciones** (componentes α y β de \(\vec V_{ref}\)) más la
restricción \(d_1+d_2+d_0=1\) — **tres ecuaciones, tres incógnitas** (\(d_1,d_2,d_0\)), sistema lineal
resoluble en forma cerrada:

$$ \begin{pmatrix}V_{1,\alpha} & V_{2,\alpha} & V_{0,\alpha}\\ V_{1,\beta} & V_{2,\beta} & V_{0,\beta}\\ 1&1&1\end{pmatrix}\begin{pmatrix}d_1\\d_2\\d_0\end{pmatrix} = \begin{pmatrix}V_{ref,\alpha}\\V_{ref,\beta}\\1\end{pmatrix} $$

Con los tres vértices fijos por sector/triángulo, la matriz es constante para cada uno de los 24
triángulos y se invierte **una vez** fuera de línea (tabla precalculada); en tiempo real solo hay que
identificar el triángulo y multiplicar por la inversa correspondiente — es lo que hace viable ejecutar SVM
en un DSP a la frecuencia de conmutación.

**Paso 6 — tiempos de aplicación y secuencia.** Los duty cycles se convierten en tiempos dentro del
periodo de conmutación \(t_i=d_i\,T_s\), y se ordenan en una secuencia simétrica (p. ej.
\(V_1\to V_0\to V_2\to V_0\to V_1\)) que minimiza el número de conmutaciones por periodo — análogo a la
secuencia de 2 niveles pero con un vector intermedio adicional. Cuando el vector es de tipo **medio**
(redundante ×2, Paso 2), el algoritmo de balance de neutro elige en cada periodo cuál de las dos
combinaciones redundantes usar, según el signo de \(\Delta V\) medido — cerrando así, dentro del propio
cálculo de SVM, el mismo lazo de compensación que en PD-PWM se conseguía con la inyección de secuencia
cero \(v_0\) (apartado 3, Paso 6), pero de forma más directa y con más grados de libertad.

**Equivalencia con PD-PWM.** Ambos métodos son matemáticamente equivalentes en su valor medio de tensión
de salida (mismo \(\bar v_{aO}\), misma zona lineal hasta \(m=1\) extensible a \(2/\sqrt3\)); difieren en
el reparto de armónicos entre bandas laterales y, sobre todo, en que la SVM da acceso **explícito** a la
redundancia de vectores medios para el balance de neutro, mientras que PD-PWM lo consigue indirectamente
vía la inyección de \(v_0\) — dos caminos al mismo objetivo del apartado 3.

## 6 — Modelo dq del NPC (para el control de corriente)

**Por qué el modelo dq no cambia respecto a 2 niveles.** Desde el punto de vista del **valor medio** de la
tensión de salida (\(\bar v_{aO}\), lo que ve el filtro \(L\) tras promediar la conmutación), el NPC
sintetiza exactamente la misma referencia senoidal \(m\,\frac{V_{dc}}{2}\sin\theta\) que un puente de 2
niveles con el mismo \(V_{dc}\) — la única diferencia física es **cómo** se trocea esa tensión, no su valor
medio. Por tanto, la derivación completa del modelo dq (transformación de Clarke-Park, ecuación con
acoplamiento cruzado \(\pm\omega_0Li\), desacoplo feedforward, planta \(1/(Ls+R)\)) es **idéntica** a la de
[[convertidor-back-to-back]] §2, sustituyendo únicamente la etapa de modulación:

$$ L\frac{d}{dt}\begin{pmatrix}i_d\\i_q\end{pmatrix} = \begin{pmatrix}\bar v_{d,conv}\\\bar v_{q,conv}\end{pmatrix} - \begin{pmatrix}v_{d,g}\\v_{q,g}\end{pmatrix} - \begin{pmatrix}R & -\omega_0 L\\ \omega_0 L & R\end{pmatrix}\begin{pmatrix}i_d\\i_q\end{pmatrix} $$

con \(\bar v_{d,conv}\), \(\bar v_{q,conv}\) obtenidos del PI + feedforward exactamente como en la ficha del
back-to-back. **Lo único nuevo** que añade el NPC al lazo de control es la variable de estado extra
\(\Delta V=V_{C1}-V_{C2}\) del apartado 3, que se regula con un lazo **adicional y desacoplado** (ancho de
banda mucho menor) que actúa sobre la componente de secuencia cero \(v_0\), sin interferir con el control
vectorial de \(i_d,i_q\) (que solo ve componentes de secuencia positiva).

## 7 — Ejemplo numérico completo de dimensionado

Se dimensiona un NPC de \(P_{nom}=2\,\text{MW}\), \(V_{ac}=690\,\text{V}\) (línea), \(f_s=3\,\text{kHz}\),
\(m_{max}=0.9\) — mismos datos de partida que el ejemplo de [[convertidor-back-to-back]], para comparar
directamente el resultado con 2 niveles.

**Paso 1 — Tensión de bus.** Idéntico cálculo que en 2 niveles (§5.2 de
[[convertidor-back-to-back]]):

$$ \hat v_{fase} = \frac{\sqrt2\,690}{\sqrt3} = 563\,\text{V}, \qquad V_{dc}\geq\frac{2\times563}{0.9}=1251\,\text{V} $$

Se elige \(V_{dc}=1300\,\text{V}\) (algo más holgado que en 2 niveles, porque el NPC se usa típicamente en
aplicaciones de mayor tensión donde el ahorro en semiconductores es más relevante). Cada IGBT bloquea
\(V_{dc}/2 = 650\,\text{V}\): se puede usar tecnología de 1200 V con buen margen, en vez de los 1700-2000 V
que exigiría un puente de 2 niveles al mismo \(V_{dc}\).

**Paso 2 — Corriente de pico.** Igual que en 2 niveles:

$$ \hat I = \frac{2P_{nom}}{3\,\hat v_{fase}} = \frac{2\times2\times10^6}{3\times563} = 2366\,\text{A} $$

**Paso 3 — Inductancia del filtro.** Con \(\Delta i_{L,max}=20\,\%\,\hat I = 473\,\text{A}\) y el factor
\(1/4\) del apartado 4:

$$ L_{NPC} \geq \frac14\cdot\frac{V_{dc}}{4\,f_s\,\Delta i_{L,max}} = \frac14\cdot\frac{1300}{4\times3000\times473} = \frac14\times0.229\,\text{mH} = 0.057\,\text{mH} $$

Frente a los \(0.25\,\text{mH}\) de 2 niveles a \(V_{dc}=1150\,\text{V}\) del ejemplo de la ficha hermana
(y aún reduciéndolo a la mitad de la comparación directa por el cambio de \(V_{dc}\), sigue siendo varias
veces menor): se elige \(L=0.07\,\text{mH}\), una reducción sustancial de tamaño y coste de la bobina de
filtro. Verificación en pu: \(X_L=2\pi\times50\times0.07\times10^{-3}=0.022\,\Omega\);
\(Z_{base}=398^2/2\times10^6=0.079\,\Omega\) → \(x_L\approx0.28\,\text{pu}\) (razonable, frente al
\(\approx1\,\text{pu}\) que obligaba a considerar LCL en 2 niveles).

**Paso 4 — Condensadores de bus.** Con el mismo criterio energético que en 2 niveles pero **el doble** de
condensadores en serie (cada uno a la mitad de tensión, misma energía total almacenada requerida):

$$ C_1=C_2=C \approx 2\times C_{dc,2L}\Big|_{V_{dc}\to V_{dc}/2} $$

porque la energía almacenada por unidad de tensión es menor a mitad de tensión (\(E=\tfrac12CV^2\)) y hace
falta el doble de capacidad por rama para el mismo margen de energía; a esto se añade el 20–30 % extra por
el rizado de \(3\omega_0\) del balance de neutro (apartado 3, Paso 4). Para este ejemplo,
partiendo de \(C_{dc,2L}=20\,\text{mF}\) a 1150 V, y escalando por energía (\(C\propto1/V^2\) para la misma
energía, más el factor 2 de la partición, más el 25% de margen):

$$ C \approx 2\times\frac{(1150)^2}{(1300/2)^2}\times20\,\text{mF}\times1.25 \approx 2\times20\,\text{mF}\times1.25 \approx 50\,\text{mF (por condensador)} $$

(cálculo ilustrativo del orden de magnitud; el dimensionado fino requiere la simulación del Paso 6 de este
mismo apartado con el peor caso de desequilibrio real de la aplicación).

**Paso 5 — Lazo de balance de neutro.** Con \(\omega_{bal}\sim\omega_0/5\approx63\,\text{rad/s}\) (bastante
por debajo de \(\omega_0=314\,\text{rad/s}\), para no interferir con la dinámica de red), se sintoniza
\(K_{bal}\) con el modelo de primer orden del apartado 3, Paso 7, iterando hasta que la simulación del Paso
6 confirme \(\Delta V<5\,\%\,V_{dc}/2 = 32.5\,\text{V}\) en el peor caso de desequilibrio de diseño.

**Paso 6 — Verificación.** Repetir el Paso 6 de la metodología general (apartado 8 más abajo) con carga
desequilibrada (p. ej. una fase al 80% de las otras dos) y comprobar \(\Delta V\) y que \(|r_k^*+v_0|\le1\)
en todo el ciclo.

## 8 — Proceso de diseño iterativo (metodología resumida)

Siguiendo la misma metodología que [[convertidor-back-to-back]] (especificaciones → componentes →
control → verificación), para un NPC de potencia \(P_{nom}\), tensión de red \(V_{ac}\) y frecuencia de
conmutación \(f_s\):

| Paso | Qué se dimensiona | Criterio | Fórmula |
|---|---|---|---|
| 1 | \(V_{dc}\) y clase de IGBT | Sintetizar el pico de red; cada IGBT bloquea \(V_{dc}/2\) | \(V_{dc}\geq2\hat v_{fase}/m_{max}\) |
| 2 | \(L\) del filtro | Rizado de corriente objetivo, factor \(1/4\) frente a 2 niveles | \(L\geq\tfrac14\cdot V_{dc}/(4f_s\Delta i_{L,max})\) |
| 3 | \(C_1=C_2\) | Energía del transitorio + margen por rizado \(3\omega_0\) del neutro | ver apartado 7, Paso 4 |
| 4 | Lazo de corriente \(i_d,i_q\) | Igual que 2 niveles (IMC, cancelación de polo) | apartado 6 (idéntico a back-to-back §2.7) |
| 5 | Lazo de balance de neutro | Ancho de banda muy por debajo de \(\omega_0\) | \(\tau_{bal}\) del apartado 3, Paso 7 |
| 6 | Verificación | Simular con desequilibrio y comprobar \(\Delta V\) y saturación de \(v_0\) | apartado 3, Paso 8 |

## Errores comunes
- **Olvidar el balance de neutro creyendo que "se autorregula":** solo es cierto (y solo en promedio, con
  oscilación residual a \(3\omega_0\)) con carga trifásica perfectamente equilibrada; cualquier
  desequilibrio real lo desestabiliza como un integrador sin freno (apartado 3, Paso 5).
- **Confundir \(T_1\)-\(T_3\) complementarios con \(T_1\)-\(T_4\):** el par que nunca debe solaparse es
  \(T_1/T_3\) y \(T_2/T_4\), no las combinaciones cruzadas (apartado 1).
- **Dimensionar \(C_1, C_2\) con la fórmula de 2 niveles sin margen extra:** ignora el rizado de
  \(3\omega_0\) del desbalance de neutro y el hecho de que la energía por condensador escala distinto
  (apartado 7, Paso 4).
- **Sintonizar el lazo de balance de neutro demasiado rápido:** un \(K_{bal}\) alto reduce \(\tau_{bal}\)
  pero exige un \(v_0\) grande que puede saturar la modulación de las tres fases (apartado 3, Paso 7).
- **No verificar el nivel de corriente al elegir qué diodo debe soportar el peor caso térmico:** \(D_1\) y
  \(D_2\) solo conducen durante el estado O y con un signo de \(i_o\) cada uno — su corriente media es menor
  que la de los IGBTs pero su pico puede ser alto en cargas de bajo factor de potencia.

## Cuándo y por qué se usa
Accionamientos de media tensión, generación renovable (eólica, fotovoltaica) y STATCOM de potencias
medias-altas donde se necesita menor \(dv/dt\) y \(THD\) que 2 niveles sin llegar a la complejidad del MMC.
Es el punto de partida obligado antes de estudiar variantes (T-type, Flying Capacitor) o el escalado a MMC
(ver [[mmc-modelo-control]]) para HVDC.

## Conceptos relacionados
- [[topologias-multinivel]] · [[convertidor-vsc]] · [[mmc-modelo-control]] · [[semiconductores-potencia]]
- [[armonicos-thd]] · [[filtro-lcl]] · [[control-vectorial]] · [[control-cascada]]

## Referencias
- Nabae, Takahashi, Akagi, *A New Neutral-Point-Clamped PWM Inverter*, IEEE TIA 1981.
- Rodriguez, Lai, Peng, *Multilevel Inverters: Survey of Topologies*, IEEE TIE 2002.
- Holmes, Lipo, *Pulse Width Modulation for Power Converters*, IEEE Press 2003.
- Bruckner, Bernet, Guldner, *The Active NPC Converter and Its Loss-Balancing Control*, IEEE TIE 2005.
- Celanovic, Boroyevich, *A Comprehensive Study of Neutral-Point Voltage Balancing in 3-Level NPC*, IEEE TPEL 2000.
