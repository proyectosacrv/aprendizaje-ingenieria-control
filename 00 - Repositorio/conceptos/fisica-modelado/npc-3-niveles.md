---
titulo: NPC de 3 niveles — topología, conmutación y balance de neutro
slug: npc-3-niveles
categoria: fisica-modelado
tipo: concepto
nivel: avanzado
proyectos: []
objetivos: [analizar la topologia NPC completa, derivar la tabla de conmutacion, modelar el balance del punto neutro, dimensionar sus componentes]
tags: [NPC, neutral-point-clamped, multinivel, 3-niveles, punto-neutro, PD-PWM, diodos-anclaje, THD, dv-dt, dimensionado]
fecha_creacion: 2026-07-31
fecha_actualizacion: 2026-07-31
relacionados: [topologias-multinivel, convertidor-vsc, marco-dq, semiconductores-potencia, filtro-lcl, armonicos-thd, control-vectorial]
referencias:
  - "Nabae, Takahashi, Akagi, A New Neutral-Point-Clamped PWM Inverter, IEEE TIA 1981"
  - "Rodriguez, Lai, Peng, Multilevel Inverters: Survey of Topologies, IEEE TIE 2002"
  - "Holmes, Lipo, Pulse Width Modulation for Power Converters, IEEE Press 2003"
  - "Bruckner, Bernet, Guldner, The Active NPC Converter and Its Loss-Balancing Control, IEEE TIE 2005"
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

Esta dependencia del signo de \(i_o\) es la **raíz física** del problema de balance de neutro (apartado 3):
cada vez que el convertidor está en el estado O, uno de los dos condensadores se descarga un poco y el
otro se carga, y quién lo hace depende de \(i_o\), no de una decisión del modulador.

**Nunca usar T1 y T3 (o T2 y T4) a la vez:** cortocircuitaría directamente \(C_1\) o \(C_2\) a través de dos
interruptores en conducción simultánea (falta de brazo). El *deadtime* entre la orden de un interruptor y su
complementario debe respetarse igual que en 2 niveles (ver [[semiconductores-potencia]]).

## 2 — Modulación: PD-PWM con dos portadoras

**Idea.** Se apilan dos portadoras triangulares de amplitud unidad: una entre \([0,1]\) (rige la transición
P↔O) y otra entre \([-1,0]\) (rige la transición O↔N). La referencia \(r(\theta)=m\sin\theta\in[-1,1]\) se
compara contra ambas:

$$ v_{aO}^*(\theta) = \begin{cases} +\dfrac{V_{dc}}{2} & \text{si } r>\text{portadora superior} \\[4pt] -\dfrac{V_{dc}}{2} & \text{si } r<\text{portadora inferior} \\[4pt] 0 & \text{en el resto} \end{cases} $$

Es la generalización directa del comparador de 2 niveles (§2 de [[convertidor-back-to-back]]): con \(N\)
niveles hacen falta \(N-1\) portadoras apiladas (PD-PWM, *phase disposition*), todas en fase entre sí (de
ahí el nombre). Existen variantes POD (portadoras negativas desfasadas 180°) y APOD (todas alternadas), con
distinto reparto de armónicos entre bandas pero el mismo principio.

**Duty efectivo de cada tramo.** Igual que en 2 niveles (§5.2 de [[convertidor-back-to-back]]), dentro de
cada semiperiodo de conmutación el duty relativo entre los dos niveles activos es lineal en \(r\); la
diferencia es que aquí el "cero" de referencia para cada comparación está desplazado (0.5 o −0.5 en vez de
0), lo que reduce a la mitad la excursión de portadora que ve cada comparación y, con ello, el rizado.

## 3 — El balance del punto neutro (derivación completa)

**Paso 1 — el origen físico.** Del apartado 1: en el estado O, según el signo de \(i_o\), conduce \(D_1\)
(descarga \(C_1\), carga \(C_2\)) o \(D_2\) (descarga \(C_2\), carga \(C_1\)). La corriente que fluye hacia
el nudo O durante ese estado es exactamente \(i_o\):

$$ i_O(t) = i_o(t)\cdot\mathbb{1}[\text{estado} = O] $$

**Paso 2 — la dinámica de los condensadores.** Con \(C_1=C_2=C\), el balance de carga en el nudo O da:

$$ C\,\frac{dV_{C1}}{dt} = -i_O(t), \qquad C\,\frac{dV_{C2}}{dt} = +i_O(t) $$

(si \(i_O>0\) se resta de \(C_1\) y se suma a \(C_2\), como en el Paso 1 del apartado 1). El **desbalance**
\(\Delta V = V_{C1}-V_{C2}\) evoluciona como:

$$ \frac{d(\Delta V)}{dt} = -\frac{2\,i_O(t)}{C} $$

**Paso 3 — por qué con carga equilibrada el desbalance no se acumula.** Promediando \(i_O(t)\) sobre un
periodo de red con una carga trifásica **equilibrada**, la componente media de \(i_O\) es cero (las tres
fases se reparten simétricamente los pasos por el estado O): el desbalance oscila a \(3\omega_0\)
(el triple de la fundamental) pero no **deriva**. El problema aparece con **cargas desequilibradas**,
**factor de potencia bajo**, o **transitorios**, donde sí aparece una componente neta de \(i_O\) que integra
sin freno (Paso 2 es literalmente un integrador: sin corrección, \(\Delta V\) crece sin límite).

<div class="cfig"><img src="figuras/npc-neutro.png" alt="esquema de los dos caminos de corriente en el estado O segun el signo de la corriente de fase, y simulacion de la deriva de las tensiones de los dos condensadores del bus sin compensacion frente a la estabilizacion con compensacion proporcional al desbalance"><div class="cap">(a) En el estado O, \(D_1\) o \(D_2\) conducen según el signo de \(i_o\), descargando un condensador y cargando el otro. (b) Ante una componente neta de corriente hacia O (carga desequilibrada), sin compensación el desbalance \(V_{C1}-V_{C2}\) crece linealmente sin límite (Paso 2: es un integrador puro); con una compensación proporcional al desbalance medido, las dos tensiones se mantienen ancladas a \(V_{dc}/2\).</div></div>

**Paso 4 — la corrección: usar la redundancia del estado O.** El modulador **no puede** elegir directamente
qué diodo conduce (lo decide \(i_o\)), pero sí puede desplazar **cuándo** se está en el estado O respecto a
P o N, inyectando una pequeña componente de **secuencia cero** \(v_0\) (común a las tres fases, igual que el
3.er armónico de la modulación de 2 niveles — §2.2 de [[convertidor-back-to-back]]) en la referencia:

$$ r_k^*(\theta) = m\sin(\theta - \phi_k) + v_0, \qquad k\in\{a,b,c\} $$

Un \(v_0\) sesgado hacia el nivel P alarga el tiempo relativo en P/O+ y acorta O−/N (o viceversa),
cambiando el **tiempo neto** que cada fase pasa en cada tramo del estado O y, con ello, el signo neto del
desbalance que se corrige. Un lazo de control mide \(\Delta V = V_{C1}-V_{C2}\) y ajusta \(v_0\) en
proporción (o con un PI) para llevarlo a cero — es exactamente el mecanismo simulado en el panel (b).

**Paso 5 — límite del método y alternativas.** La inyección de secuencia cero corrige desbalances
**lentos** (frecuencia de red y menores). Para desbalances instantáneos grandes (arranque, faltas
asimétricas), se recurre al **NPC activo** (ANPC, con interruptores adicionales que permiten forzar el
camino de corriente independientemente de \(i_o\)) o a un lazo de control más rápido sobre la propia
modulación de cada fase individualmente.

## 4 — \(dv/dt\) y contenido armónico (cuantitativo)

Del desarrollo general de [[topologias-multinivel]] (apartado 1), con \(n=3\):

$$ V_{bloqueo} = \frac{V_{dc}}{n-1} = \frac{V_{dc}}{2}, \qquad \frac{dv}{dt}\bigg|_{NPC} = \frac12\,\frac{dv}{dt}\bigg|_{2L} $$

**Rizado de corriente.** El salto de tensión efectivo sobre el filtro \(L\) en cada conmutación es
\(V_{dc}/2\) en vez de \(V_{dc}\) — la mitad. Como el rizado (§5.2 de [[convertidor-back-to-back]]) escala
con el **cuadrado** de ese salto dividido por el intervalo efectivo (que también se reduce a la mitad,
porque cada comparación de portadora cubre solo medio rango):

$$ \frac{\Delta i_{L,NPC}}{\Delta i_{L,2L}} = \left(\frac{V_{dc}/2}{V_{dc}}\right)\cdot\frac{T_s/2}{T_s} \cdot \text{(factor por comparación)} = \frac{1}{4} $$

En la práctica esto permite **reducir \(L\) a un cuarto** manteniendo el mismo rizado, o mantener \(L\) y
cuadruplicar la calidad de corriente — ver la comparativa numérica del apartado 5 de [[topologias-multinivel]].

## 5 — Dimensionado iterativo (proceso de diseño)

Siguiendo la misma metodología que [[convertidor-back-to-back]] (especificaciones → componentes →
control), para un NPC de potencia \(P_{nom}\), tensión de red \(V_{ac}\) y frecuencia de conmutación
\(f_s\):

**Paso 1 — Tensión de bus y elección de semiconductores.** Igual que en 2 niveles,
\(V_{dc}\geq 2\hat v_{fase}/m_{max}\); pero ahora cada IGBT solo bloquea \(V_{dc}/2\), lo que permite elegir
dispositivos de la mitad de tensión nominal (p. ej. 1700 V en vez de 3300 V para \(V_{dc}\approx2.8\) kV),
más rápidos y con menores pérdidas de conmutación por unidad de tensión bloqueada.

**Paso 2 — Inductancia del filtro.** Con el rizado 4 veces menor del apartado 4, se aplica directamente:

$$ L_{NPC} \geq \frac{1}{4}\cdot\frac{V_{dc}}{4\,f_s\,\Delta i_{L,max}} $$

**Paso 3 — Condensadores de bus.** \(C_1=C_2=C\), dimensionados por el mismo criterio energético que el
bus DC de 2 niveles (Iteración 3 de [[convertidor-back-to-back]]) **más** un margen para el rizado de
\(3\omega_0\) del desbalance del Paso 3 del apartado 3 de esta ficha; en la práctica se sobredimensiona un
20–30 % respecto al cálculo de 2 niveles para dar margen al balance de neutro.

**Paso 4 — Diseño del lazo de balance de neutro.** Un PI simple sobre \(\Delta V = V_{C1}-V_{C2}\), con
ancho de banda muy inferior al de los lazos de corriente (varias décadas por debajo, típicamente
\(\omega_{bal}\sim\omega_0/5\) a \(\omega_0\)): es un lazo lento porque el propio Paso 3 del apartado 3
muestra que el desbalance en carga equilibrada solo oscila (no hay urgencia), y forzarlo demasiado rápido
distorsiona la modulación de las tres fases.

**Paso 5 — Verificación.** Simular con carga desequilibrada (peor caso realista) y comprobar que
\(\Delta V\) se mantiene dentro de un margen admisible (típicamente \(<5\,\%\) de \(V_{dc}/2\)) sin que la
inyección de \(v_0\) sature la modulación (\(|r_k^*+v_0|\leq1\)).

## Errores comunes
- **Olvidar el balance de neutro creyendo que "se autorregula":** solo es cierto con carga trifásica
  perfectamente equilibrada y factor de potencia constante; cualquier desequilibrio real lo desestabiliza
  (apartado 3, Paso 3).
- **Confundir \(T_1$-$T_3\) complementarios con \(T_1$-$T_4\):** el par que nunca debe solaparse es
  \(T_1/T_3\) y \(T_2/T_4\), no las combinaciones cruzadas.
- **Dimensionar \(C_1, C_2\) con la fórmula de 2 niveles sin margen extra:** ignora el rizado de
  \(3\omega_0\) del desbalance de neutro, que en la práctica exige sobredimensionar (Paso 3 del apartado 5).
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
- [[armonicos-thd]] · [[filtro-lcl]] · [[control-vectorial]]

## Referencias
- Nabae, Takahashi, Akagi, *A New Neutral-Point-Clamped PWM Inverter*, IEEE TIA 1981.
- Rodriguez, Lai, Peng, *Multilevel Inverters: Survey of Topologies*, IEEE TIE 2002.
- Holmes, Lipo, *Pulse Width Modulation for Power Converters*, IEEE Press 2003.
- Bruckner, Bernet, Guldner, *The Active NPC Converter and Its Loss-Balancing Control*, IEEE TIE 2005.
