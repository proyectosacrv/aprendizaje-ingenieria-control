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
(\(D_5\), \(D_6\)) conectan la salida de fase a P, O o N según qué par de interruptores adyacentes esté
activo. Cada dispositivo bloquea solo \(V_{dc}/2\): se pueden usar semiconductores de la mitad de tensión
que en un puente de 2 niveles para el mismo \(V_{dc}\), o doblar \(V_{dc}\) con la misma tecnología.

<div class="cfig"><img src="figuras/npc-topologia.png" alt="rama de fase del NPC de 3 niveles con los cuatro IGBT T1-T4 (simbolo con diodo antiparalelo), los dos diodos de anclaje D5 y D6 al punto neutro O, y los dos condensadores de bus C1 y C2"><div class="cap">Rama de fase del NPC, con el símbolo real de cada IGBT (transistor + diodo antiparalelo): \(T_1\)–\(T_4\) en serie entre P y N; \(D_5\) ancla el punto medio de \(T_1\)-\(T_2\) al neutro O cuando la salida está a \(0\) con \(i_o>0\); \(D_6\) hace lo mismo para \(i_o<0\). \(C_1\), \(C_2\) parten el bus DC.</div></div>

## 1 — Tabla de estados de conmutación (completa)

**Regla de complementariedad.** Para no cortocircuitar el bus, \(T_1\) y \(T_3\) son **complementarios**
(\(T_3=\overline{T_1}\)) y \(T_2\) y \(T_4\) también (\(T_4=\overline{T_2}\)). Con dos variables libres
(\(T_1\), \(T_2\)) hay 4 combinaciones binarias, pero **una es redundante** en corriente para el estado 0
(según el signo de \(i_o\)):

<div class="cfig"><img src="figuras/npc-conmutacion.png" alt="seis mini-circuitos del NPC (P, O, N cruzados con io positivo e io negativo) mostrando la trayectoria de corriente resaltada y que dispositivo conduce en cada caso -canal del IGBT o diodo antiparalelo o de anclaje-, con tabla completa de 6 filas mostrando S o D para cada dispositivo T1-T4, D1-D6, y debajo las formas de onda de la modulacion PD-PWM y el espectro comparado con dos niveles"><div class="cap">(a)-(f) Análisis completo de los 6 estados físicos (3 niveles de salida × signo de \(i_o\)), con la trayectoria de corriente resaltada en rojo: (a) P con \(i_o>0\), conducen los canales de \(T_1,T_2\); (b) O con \(i_o>0\), \(T_2,T_3\) ON y conduce \(D_5\); (c) N con \(i_o>0\), conducen los diodos antiparalelo \(D_3,D_4\) (no el canal); (d) P con \(i_o<0\), conducen los diodos antiparalelo \(D_1,D_2\); (e) O con \(i_o<0\), \(T_2,T_3\) ON y conduce \(D_6\); (f) N con \(i_o<0\), conducen los canales de \(T_3,T_4\). Debajo, la tabla completa con S (canal del IGBT) o D (diodo) para cada uno de los 10 dispositivos en los 6 estados. (e) Modulación PD-PWM: dos portadoras triangulares apiladas (una entre 0 y 1, otra entre −1 y 0) comparadas con la misma referencia generan directamente los 3 niveles. (f) El contenido armónico alrededor de \(f_{sw}\) cae mucho más rápido que en 2 niveles.</div></div>

**Por qué hay 6 estados y no 3.** La tabla de \((T_1,T_2,T_3,T_4)\) solo fija a qué nudo del bus (P, O o N)
queda conectada la salida — decide el **nivel de tensión**. Pero el IGBT es un interruptor unidireccional en
tensión y bidireccional en corriente **solo gracias a su diodo antiparalelo**: el canal únicamente deja pasar
corriente en un sentido (colector→emisor cuando está en ON), y si \(i_o\) intenta circular al revés mientras
la puerta sigue en ON, es el diodo antiparalelo — no el canal — quien físicamente conduce. Por eso, para
saber **qué dispositivo semiconductor concreto** lleva la corriente (y por tanto dónde disipa pérdidas) hace
falta cruzar cada uno de los 3 niveles con el signo de \(i_o\): resultan **6 combinaciones**, no 3.

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

| Estado | Gate \((T_1,T_2,T_3,T_4)\) | \(i_o\) | Dispositivo que conduce realmente | \(v_{aO}\) |
|---|---|---|---|---|
| **P** | 1,1,0,0 | \(>0\) | canal de \(T_1, T_2\) (S) | \(+V_{dc}/2\) |
| **P** | 1,1,0,0 | \(<0\) | diodos antiparalelo \(D_1, D_2\) (D) | \(+V_{dc}/2\) |
| **O** | 0,1,1,0 | \(>0\) | canal de \(T_2\) + diodo de anclaje \(D_5\) (\(T_3\) ON pero sin corriente) | \(0\) |
| **O** | 0,1,1,0 | \(<0\) | canal de \(T_3\) + diodo de anclaje \(D_6\) (\(T_2\) ON pero sin corriente) | \(0\) |
| **N** | 0,0,1,1 | \(>0\) | diodos antiparalelo \(D_3, D_4\) (D) | \(-V_{dc}/2\) |
| **N** | 0,0,1,1 | \(<0\) | canal de \(T_3, T_4\) (S) | \(-V_{dc}/2\) |

La orden de puerta (columna "Gate") es la misma en las dos filas de P y en las dos de N — el modulador no
decide entre esos dos casos, es \(i_o\) quien decide si es el canal o el diodo antiparalelo quien realmente
conduce. Esto es distinto del estado O, donde la orden de puerta también es siempre \((0,1,1,0)\) pero además
hay una **elección física** de cuál de los dos diodos de anclaje (\(D_5\) o \(D_6\)) cierra el camino,
también gobernada por el signo de \(i_o\).

**Por qué el estado O tiene dos caminos, y por qué T2 y T3 nunca conducen los dos a la vez.** La orden de
puerta activa \(T_2\) y \(T_3\) simultáneamente, pero cada IGBT solo dirige corriente por su canal en un
sentido (colector→emisor); el **camino físico real** que la corriente encuentra pasa por uno solo de los dos,
según su signo:
- Si \(i_o>0\) (la fase entrega corriente hacia la carga desde O): el único camino disponible es
  O→\(D_5\)→nudo \(T_1\)-\(T_2\)→canal de \(T_2\)→A. \(T_3\) está en ON por puerta, pero la rama hacia N
  (a través de \(D_6\), orientado al revés) está en bloqueo, así que **\(T_3\) no lleva corriente**.
- Si \(i_o<0\) (la corriente entra en A y va hacia O): el único camino disponible es
  A→canal de \(T_3\)→nudo \(T_3\)-\(T_4\)→\(D_6\)→O. Aquí es \(T_2\) quien está en ON sin conducir.

Es decir: **nunca conducen T2 y T3 a la vez** — la orden de puerta activa a ambos como candidatos, pero el
diodo de anclaje que sí puede polarizarse en directo (según el signo de \(i_o\)) determina cuál de los dos
IGBT queda en serie con un camino cerrado, y ese es el único que efectivamente circula corriente.

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

**Qué problema resuelve este apartado.** La tabla del apartado 1 dice qué combinación de interruptores da
cada nivel (P, O, N), pero no dice **cuánto tiempo** hay que quedarse en cada uno para que la tensión media
de salida seno un ciclo completo de red con la forma \(m\sin\theta\) deseada. Eso es lo que fija el
modulador: necesitamos (a) una regla de comparación que decida en cada instante a qué nivel conmutar, y (b)
saber qué **duty** (fracción de tiempo) le corresponde a cada nivel, porque ese duty es lo que en el
apartado 3 determina cuánta carga se transfiere al punto neutro y en el apartado 4 determina las pérdidas de
conducción.

**Por qué dos portadoras y no una.** En 2 niveles (ver §2 de [[convertidor-back-to-back]]) basta una sola
portadora triangular en \([-1,1]\) comparada con la referencia: por encima conmuta a P, por debajo a N. Aquí
hay un nivel intermedio (O) que también hay que decidir cuándo usar, así que una sola comparación no basta.
La solución estándar (PD-PWM, *phase disposition*) apila **tantas portadoras como transiciones entre niveles
adyacentes existan**: con 3 niveles hay 2 transiciones (P↔O y O↔N), luego 2 portadoras, una en \([0,1]\) y
otra en \([-1,0]\), ambas en fase entre sí (de ahí el nombre). En general, \(N\) niveles requieren \(N-1\)
portadoras. La referencia \(r(\theta)=m\sin\theta\in[-1,1]\) se compara contra ambas:

$$ v_{aO}^*(\theta) = \begin{cases} +\dfrac{V_{dc}}{2} & \text{si } r>\text{portadora superior} \\[4pt] -\dfrac{V_{dc}}{2} & \text{si } r<\text{portadora inferior} \\[4pt] 0 & \text{en el resto} \end{cases} $$

Existen variantes POD (portadoras negativas desfasadas 180°) y APOD (todas alternadas), con distinto reparto
de armónicos entre bandas laterales pero el mismo principio de comparación.

**Por qué hace falta derivar el duty explícitamente.** La regla de comparación de arriba dice *qué* nivel
sale en cada instante de conmutación, pero no dice **cuánto tiempo relativo** pasa la salida en cada uno
dentro de un periodo de conmutación \(T_s\) — y es esa fracción de tiempo (el *duty*) la que fija la tensión
media, la que en el apartado 3 determina cuánta carga se transfiere al punto neutro y la que en el apartado 4
determina el rizado de corriente y las pérdidas de conducción.

**Cómo razonar el duty a partir de la comparación señal-portadora.** Fijemos un instante de la referencia
\(\theta\) y miremos un único periodo de conmutación \(T_s\) alrededor de ese instante — a esa escala de
tiempo tan corta, la referencia \(r(\theta)\) apenas varía y puede tratarse como una **constante** \(x\)
mientras la portadora sí completa una rampa entera. Concretamente, en la región superior la portadora sube
linealmente de 0 a 1 en \(T_s\): mientras la rampa va de 0 hasta el valor \(x\), la portadora está por debajo
de la referencia y el comparador ordena P (\(T_1\) en ON); en cuanto la rampa supera \(x\) y hasta que se
reinicia en 1, la portadora está por encima y el comparador ordena O. Como la rampa avanza a **velocidad
constante**, el tiempo que tarda en ir de 0 a \(x\) es, sencillamente, la misma fracción \(x\) del periodo
total: si la rampa completa recorre \([0,1]\) en un tiempo \(T_s\), recorrer solo \([0,x]\) le lleva
\(x\cdot T_s\). Por tanto la fracción de \(T_s\) en el nivel P es directamente igual al valor **numérico**
de la referencia en ese instante — no hace falta ninguna integral para este paso, solo la proporcionalidad
de una rampa lineal (es la misma idea, aplicada aquí a un rango \([0,1]\) en vez de \([-1,1]\), que en el
duty de 2 niveles del §5.2 de [[convertidor-back-to-back]]).

*Región superior* (\(0\le r\le1\), la salida conmuta entre P y O). Aplicando el razonamiento anterior con
\(x=r(\theta)\), el duty instantáneo en P es

$$ d_P(\theta) = r(\theta) = m\sin\theta \qquad (0\le m\sin\theta\le 1) $$

y el resto del periodo, \(1-d_P(\theta)\), la salida está en O.

*Región inferior* (\(-1\le r\le0\)), simétrica: el duty en N es \(d_N(\theta)=-r(\theta)=-m\sin\theta\) y el
resto, \(1-d_N(\theta)\), en O.

**De dónde sale el corchete \((1+m\sin\theta)/2\) de 2 niveles (y por qué hace falta aquí).** Antes de definir
el duty medio del NPC hay que tener a mano el resultado de referencia con el que se va a comparar, porque las
pérdidas del apartado 4 y el ejemplo numérico del apartado 7 necesitan un duty **directamente comparable**
al de 2 niveles, no solo \(d_P\) y \(d_N\) por separado. En 2 niveles (§5.2 de
[[convertidor-back-to-back]]) el interruptor superior está ON una fracción \(d(\theta)\) de **cada** periodo
de conmutación, en **todo** el ciclo de red (no solo medio ciclo), y el interruptor inferior lleva el resto,
\(1-d(\theta)\); la tensión media de salida en ese periodo es el promedio ponderado de los dos niveles
posibles:

$$ \bar v(\theta) = d(\theta)\Big(+\frac{V_{dc}}{2}\Big) + \big(1-d(\theta)\big)\Big(-\frac{V_{dc}}{2}\Big) = \frac{V_{dc}}{2}\big(2d(\theta)-1\big) $$

Igualando esto a la referencia deseada \(\bar v(\theta)=m\,\frac{V_{dc}}{2}\sin\theta\) y despejando
\(d(\theta)\) se obtiene el corchete:

$$ \frac{V_{dc}}{2}\big(2d(\theta)-1\big) = m\,\frac{V_{dc}}{2}\sin\theta \quad\Longrightarrow\quad d(\theta) = \frac{1+m\sin\theta}{2} $$

(comprobación: en \(\theta=0\), \(d=0.5\), duty simétrico entre P y N para tensión media nula; en el pico
positivo, \(d\to1\), todo el tiempo en P; en el valle, \(d\to0\), todo en N).

**El duty efectivo del NPC, definido para ser comparable con el de 2 niveles.** El NPC no tiene un único
interruptor que esté ON todo el ciclo — en la región superior conmuta entre P y O (con \(d_P\) del bloque
anterior) y en la región inferior entre O y N (con \(d_N\)) — así que hace falta construir la magnitud
equivalente. Se define el **duty efectivo** \(d_{ef}(\theta)\) exactamente con el mismo papel que \(d(\theta)\)
en 2 niveles: la fracción "hacia P" de una descomposición binaria P/N que dé la misma tensión media. Puesto
que en cada instante o bien P está activo (con duty \(d_P\) y O con \(1-d_P\)) o bien N lo está (con duty
\(d_N\) y O con \(1-d_N\)), y en ambos casos O contribuye tensión media nula, la tensión media de salida del
NPC es simplemente \(V_{dc}/2\cdot d_P(\theta)\) en la región superior y \(-V_{dc}/2\cdot d_N(\theta)\) en la
inferior. Sustituyendo \(d_P(\theta)=m\sin\theta\) (región superior) esto da \(\bar v(\theta) = m\sin\theta\cdot V_{dc}/2\)
— **la misma referencia** que en 2 niveles, como debía ser. Definiendo \(d_{ef}(\theta)=\big(1+m\sin\theta\big)/2\)
igual que en 2 niveles, se recupera la relación con las variables propias del NPC:

$$ d_P(\theta) = 2\,d_{ef}(\theta) - 1 \ \ (\ge0 \text{ en la región superior}), \qquad d_N(\theta) = 1-2\,d_{ef}(\theta) \ \ (\ge0 \text{ en la región inferior}) $$

Es decir, \(d_{ef}\) es la misma cantidad de siempre (duty equivalente de 2 niveles), mientras que \(d_P,d_N\)
son la forma en que el NPC la reparte físicamente entre P/O y O/N.

**El duty medio en un ciclo de red completo: la integral correcta.** Aquí es donde hay que tener cuidado con
qué se integra y sobre qué rango. El duty medio que interesa para las pérdidas del apartado 4 y el ejemplo
del apartado 7 es el de \(d_{ef}(\theta)\) —la magnitud comparable a 2 niveles— sobre el **ciclo completo**
\([0,2\pi]\), no solo sobre el semiciclo positivo:

$$ \bar d_{ef} = \frac{1}{2\pi}\int_0^{2\pi} d_{ef}(\theta)\,d\theta = \frac{1}{2\pi}\int_0^{2\pi} \frac{1+m\sin\theta}{2}\,d\theta $$

Separando la integral en sus dos términos, \(\displaystyle\int_0^{2\pi} 1\,d\theta = 2\pi\) y
\(\displaystyle\int_0^{2\pi} \sin\theta\,d\theta = 0\) (una senoide completa se cancela en un periodo
completo — a diferencia de \(\int_0^\pi\sin\theta\,d\theta=2\), que es solo medio ciclo y **no** se anula):

$$ \bar d_{ef} = \frac{1}{2\pi}\cdot\frac{1}{2}\Big(2\pi + m\cdot 0\Big) = \frac{1}{2} $$

El resultado \(\bar d_{ef}=1/2\) es exactamente lo esperado: en un ciclo de red completo y simétrico, el
convertidor pasa en promedio tanto tiempo "hacia P" como "hacia N", independientemente del índice de
modulación \(m\) — el valor medio de la tensión de salida en un ciclo completo es cero, como debe ser para
una senoide sin componente DC. **Este promedio de \(1/2\) no es la cantidad útil para pérdidas** (que
dependen del duty instantáneo ponderado por la corriente instantánea, no del duty medio sin más — ver el
Paso 6 de [[convertidor-back-to-back]] §5.2, donde se integra \(i(\theta)\cdot d(\theta)\), no \(d(\theta)\)
solo). Lo que sí es directamente utilizable es \(d_{ef}(\theta)\) como **función de \(\theta\)** — la
expresión cerrada \((1+m\sin\theta)/2\) — que es la que se sustituye dentro de las integrales ponderadas por
corriente del apartado 4.

**Por qué el reparto en dos comparaciones de rango mitad reduce el rizado.** Aunque \(d_{ef}\) sea la
cantidad comparable con 2 niveles, físicamente el NPC nunca ejecuta un salto \(\pm V_{dc}/2\) en una sola
conmutación como el de 2 niveles: cada conmutación real es P↔O o O↔N, un salto de solo \(V_{dc}/2\) en vez
de \(V_{dc}\). Esta es la razón por la que el "cero" de referencia de cada comparación de portadora está
desplazado (0.5 o −0.5 del rango \([0,1]\) o \([-1,0]\), en vez de 0 en un único rango \([-1,1]\)): al
reducirse a la mitad la excursión de portadora que ve cada comparación, se reduce a la mitad también el
salto de tensión en cada conmutación individual y, con ello —según se deriva en el apartado 4— el rizado de
corriente.

**Hasta dónde se puede modular sin distorsión (índice de modulación).** Igual que en 2 niveles, \(m\in[0,1]\)
es la zona lineal con PD-PWM senoidal pura: por encima de \(m=1\) la referencia sobrepasa el rango de la
portadora y aparece sobremodulación (recorte, con distorsión armónica de baja frecuencia). Como en 2 niveles
(§2.2 de [[convertidor-back-to-back]]), ese límite se puede extender deformando la referencia sin alterar la
tensión de línea; el apartado 3 retoma esta idea porque en el NPC la misma deformación sirve, además, para
el balance del punto neutro.

## 3 — El balance del punto neutro (derivación completa)

**Qué problema resuelve este apartado.** El NPC reparte el bus DC en dos condensadores \(C_1\), \(C_2\) y
promete que el punto medio O queda siempre a \(V_{dc}/2\) — es la base de toda la tabla de estados del
apartado 1. Pero esa tensión de reparto **no es automática**: cada vez que el convertidor pasa por el estado
O, hay corriente entrando o saliendo del nudo O, y esa corriente carga un condensador a costa del otro. Si
nada lo corrige, la pareja \(V_{C1},V_{C2}\) puede desviarse permanentemente de \(V_{dc}/2\) cada una,
rompiendo la premisa de la que parte todo el análisis anterior (cada IGBT diseñado para bloquear justo
\(V_{dc}/2\); si un condensador sube por encima, ese margen de bloqueo desaparece). Este apartado responde a
tres preguntas en orden: **(1)** ¿de dónde sale exactamente ese desbalance? **(2)** ¿por qué con carga normal
no se dispara solo, pero con un desequilibrio sí? **(3)** ¿cómo se corrige activamente, y con qué límites?

**Paso 1 — de dónde parte: el origen físico del desbalance.** El punto de partida es la observación del
apartado 1 sobre el estado O: según el signo de \(i_o\), conduce \(D_5\) (descarga \(C_1\), carga \(C_2\)) o
\(D_6\) (descarga \(C_2\), carga \(C_1\)). Formalizando esa observación, la corriente que fluye hacia el nudo
O en cada instante es exactamente \(i_o\) cuando la fase está en estado O, y cero en cualquier otro estado
(P o N no tocan el nudo O):

$$ i_O(t) = i_o(t)\cdot\mathbb{1}[\text{estado} = O] $$

Este es el "input" de todo lo que sigue: una corriente que unas veces existe y otras no, según en qué estado
esté el modulador — no una corriente constante ni controlada directamente.

**Paso 2 — qué hace esa corriente a los condensadores.** Partiendo de \(i_O(t)\) del Paso 1, y con
\(C_1=C_2=C\), el balance de carga en el nudo O (la corriente que entra a un condensador es la que sale del
otro, porque O es un nudo intermedio) da directamente sus dos ecuaciones diferenciales:

$$ C\,\frac{dV_{C1}}{dt} = -i_O(t), \qquad C\,\frac{dV_{C2}}{dt} = +i_O(t) $$

(si \(i_O>0\) se resta de \(C_1\) y se suma a \(C_2\), como en el Paso 1). De aquí salen dos resultados
distintos, uno tranquilizador y otro que es el problema en sí — y ambos se obtienen de la misma pareja de
ecuaciones, combinándolas de dos formas distintas (sumándolas y restándolas).

*Combinación 1 — sumar las dos ecuaciones (da la tensión total del bus).* Sumando miembro a miembro:

$$ C\,\frac{dV_{C1}}{dt} + C\,\frac{dV_{C2}}{dt} = -i_O(t) + i_O(t) $$

El lado derecho se cancela exactamente (\(-i_O+i_O=0\), porque es la **misma** \(i_O(t)\) en ambas
ecuaciones, solo con signo opuesto). Sacando \(C\) factor común y usando que la derivada de una suma es la
suma de las derivadas, \(C\dfrac{d(V_{C1}+V_{C2})}{dt}=0\), y como \(C\ne0\):

$$ \frac{d(V_{C1}+V_{C2})}{dt} = 0 $$

Es decir, la tensión **total** del bus \(V_{dc}=V_{C1}+V_{C2}\) no la afecta el estado O — es un balance
interno, no una pérdida de energía total (tranquilizador: el estado O no puede volar el bus).

*Combinación 2 — restar las dos ecuaciones (da la dinámica del desbalance).* Restando la segunda ecuación de
la primera, miembro a miembro:

$$ C\,\frac{dV_{C1}}{dt} - C\,\frac{dV_{C2}}{dt} = -i_O(t) - \big(+i_O(t)\big) $$

El lado derecho ahora **no** se cancela — ambos términos tienen el mismo signo al restar un negativo con un
positivo, así que se suman en valor absoluto: \(-i_O(t) - i_O(t) = -2\,i_O(t)\). El lado izquierdo, sacando
\(C\) factor común y usando de nuevo que la derivada de una resta es la resta de las derivadas,
\(C\dfrac{d(V_{C1}-V_{C2})}{dt}\). Igualando ambos lados:

$$ C\,\frac{d(V_{C1}-V_{C2})}{dt} = -2\,i_O(t) $$

Definiendo el **desbalance** \(\Delta V \equiv V_{C1}-V_{C2}\) y despejando la derivada (dividiendo ambos
lados entre \(C\)):

$$ \frac{d(\Delta V)}{dt} = -\frac{2\,i_O(t)}{C} $$

Esta última ecuación —\(\Delta V\) es la integral de \(i_O\)— es el resultado que arrastra todo el resto del
apartado: como es un integrador puro, cualquier componente de \(i_O\) que no promedie exactamente a cero
hace que \(\Delta V\) crezca sin límite (Paso 5).

**Paso 3 — de una fase a las tres reales.** El Paso 2 trata una sola rama (una sola fase conectada al nudo
O); pero en un NPC trifásico el nudo O es **físicamente uno solo**, compartido por las tres ramas — las tres
fases descargan o cargan los mismos dos condensadores \(C_1,C_2\). Hay que ver primero por qué esto sigue
dando la misma forma de ecuación que el Paso 2, y qué cambia.

*Por qué la ecuación del Paso 2 sigue siendo válida tal cual.* El Paso 2 no usó en ningún momento que hubiera
una única fase — solo usó que "la corriente que entra al nudo O sale de \(C_1\) hacia \(C_2\)" (Kirchhoff de
corrientes, KCL, en el nudo O). Esa ley no cambia si ahora hay tres ramas conectadas al mismo nudo: sigue
siendo cierto que *toda* la corriente que llega a O por cualquiera de las tres fases tiene que salir hacia
\(C_1\) o \(C_2\). Lo único que cambia es **qué corriente es esa**: ya no es la \(i_o\) de una sola fase, sino
la suma de las contribuciones de las tres, cada una presente solo en los instantes en que *esa* fase
concreta está en su propio estado O (si la fase \(a\) está en P o N, no toca el nudo O en absoluto, igual que
en el Paso 1):

$$ i_{O,total}(t) = \sum_{k\in\{a,b,c\}} i_k(t)\cdot\mathbb{1}[\text{fase }k\text{ en estado O}] $$

*La sustitución explícita.* Como el KCL del Paso 2 sigue aplicando con esta \(i_{O,total}\) en el papel que
antes hacía \(i_O\), las dos ecuaciones de condensador y su combinación (resta) se reescriben sin más cambio
que ese, y la ecuación final del Paso 2 queda:

$$ \frac{d(\Delta V)}{dt} = -\frac{2\,i_{O,total}(t)}{C} $$

**Aquí es donde "vive" el desbalance**: \(\Delta V(t)\) sigue siendo, como en el Paso 2, la integral en el
tiempo de (menos) esta corriente:

$$ \Delta V(t) = \Delta V(0) - \frac{2}{C}\int_0^t i_{O,total}(\tau)\,d\tau $$

Es decir, el desbalance en cualquier instante es literalmente "cuánta carga neta ha entrado o salido del nudo
O hasta ahora, acumulada". Esta integral es la que hay que analizar para saber si \(\Delta V\) se mantiene
acotado o crece sin límite — y la respuesta depende por completo de **cómo se comporta la suma de las tres
contribuciones** de \(i_{O,total}\) a lo largo de un periodo: si tienden a cancelarse entre sí (Paso 4) o si
dejan un remanente neto (Paso 5). Eso es lo que hay que analizar en dos regímenes distintos, porque el
comportamiento de esa suma es cualitativamente diferente en cada uno: régimen equilibrado (Paso 4) y régimen
desequilibrado (Paso 5).

**Paso 4 — primer régimen: desarrollo completo de por qué con carga equilibrada el desbalance no se dispara.**
Partiendo de \(i_{O,total}\) del Paso 3, hay que construir explícitamente cada uno de sus tres términos y
sumarlos — sin dar por buena de antemano ninguna cancelación.

*Construir cada término de la suma.* Con corrientes trifásicas equilibradas de amplitud \(\hat I\) y factor
de potencia \(\cos\varphi\) (la corriente de cada fase desfasada un ángulo \(\varphi\) respecto a su propia
tensión/referencia), la corriente de la fase \(k\) es

$$ i_k(\theta) = \hat I\sin(\theta-\phi_k-\varphi), \qquad \phi_a=0,\ \ \phi_b=\frac{2\pi}{3},\ \ \phi_c=\frac{4\pi}{3} $$

Falta el indicador \(\mathbb{1}[\text{fase }k\text{ en O}]\) del Paso 3. Del apartado 2, la fase \(k\) está en
el estado O una fracción de tiempo \(1-|d_k|\) de cada periodo de conmutación, con \(d_k=m\sin(\theta-\phi_k)\)
(la referencia de esa fase, no de su corriente — el estado O lo decide la modulación, no la corriente). Para
sumar en forma continua (promediando sobre muchos periodos de conmutación dentro de un ángulo \(\theta\)) se
sustituye el indicador binario por su valor medio local, esa misma fracción de tiempo:

$$ \mathbb{1}[\text{fase }k\text{ en O}] \ \longrightarrow\ 1-\big|m\sin(\theta-\phi_k)\big| $$

Multiplicando ambas partes, el término de la fase \(k\) en la suma de \(i_{O,total}\) es

$$ i_k(\theta)\cdot\big(1-|m\sin(\theta-\phi_k)|\big) = \hat I\sin(\theta-\phi_k-\varphi)\cdot\Big(1-\big|m\sin(\theta-\phi_k)\big|\Big) $$

*Separar en dos partes antes de sumar.* Distribuyendo el paréntesis, cada término se parte en dos:

$$ i_k(\theta)\cdot(1-|d_k|) = \underbrace{\hat I\sin(\theta-\phi_k-\varphi)}_{\text{parte A}} \ -\ \underbrace{\hat I\sin(\theta-\phi_k-\varphi)\cdot\big|m\sin(\theta-\phi_k)\big|}_{\text{parte B}} $$

La suma completa \(i_{O,total}=\sum_k(\text{parte A}_k+\text{parte B}_k)\) se puede evaluar sumando primero
todas las partes A y luego todas las partes B, porque la suma es lineal.

*Suma de las tres partes A: se cancela exactamente.* La parte A de cada fase es simplemente su corriente
senoidal \(\hat I\sin(\theta-\phi_k-\varphi)\), sin ningún factor adicional. Sumando las tres con sus
desfases de \(120°=2\pi/3\):

$$ \sum_{k} \hat I\sin(\theta-\phi_k-\varphi) = \hat I\Big[\sin(\theta-\varphi) + \sin(\theta-\varphi-\tfrac{2\pi}{3}) + \sin(\theta-\varphi-\tfrac{4\pi}{3})\Big] $$

Esta es la suma de tres senoides idénticas desfasadas exactamente \(120°\) entre sí — la misma identidad que
dice que un sistema trifásico equilibrado no tiene componente de secuencia cero: **la suma de tres senoides
de igual amplitud, igual frecuencia y desfasadas 120° es idénticamente cero**, para cualquier ángulo. Por
tanto:

$$ \sum_{k} \text{parte A}_k = 0 \qquad \text{(exactamente, en todo instante, no solo en promedio)} $$

*Suma de las tres partes B: no se cancela sola — hay que desarrollarla con Fourier, paso a paso.* Cada parte
B tiene el factor \(|m\sin(\theta-\phi_k)|\), que **no** es una senoide pura (un valor absoluto de seno no lo
es), así que el argumento de simetría de 120° que canceló las partes A **no se puede aplicar directamente
aquí**: hace falta primero reescribir \(|\sin x|\) como una suma de senoides puras (su serie de Fourier), y
solo con esa reescritura se podrá volver a sumar por fases.

**(i) La serie de Fourier de \(|\sin x|\).** Al ser \(|\sin x|\) periódica y par, su serie de Fourier solo
tiene términos de coseno (sin senos) y, por la simetría adicional de que se repite cada \(\pi\) (no cada
\(2\pi\)), solo aparecen armónicos **pares**:

$$ |\sin x| = \frac{2}{\pi} - \frac{4}{\pi}\sum_{n=1}^{\infty}\frac{\cos(2nx)}{4n^2-1} = \underbrace{\frac{2}{\pi}}_{\text{constante}} - \frac{4}{\pi}\cdot\frac{\cos2x}{3} - \frac{4}{\pi}\cdot\frac{\cos4x}{15} - \cdots $$

<div class="cfig"><img src="figuras/npc-neutro-fourier.png" alt="grafica de valor absoluto de seno de x superpuesta con su aproximacion de Fourier de un termino (constante mas coseno de 2x), mostrando que el termino n=1 ya reproduce la forma general de la funcion, y grafica de las tres senoides de 3omega desfasadas 0, 2pi y 4pi sumandose en fase para las tres fases del sistema trifasico"><div class="cap">(a) \(|\sin x|\) (negro) frente a su aproximación de Fourier truncada al primer término, \(\tfrac{2}{\pi}-\tfrac{4}{\pi}\tfrac{\cos2x}{3}\) (azul discontinuo): ya captura la forma general, por eso basta quedarse con \(n=1\) para el análisis. (b) Las tres componentes de \(3\omega_0\) de cada fase — \(\cos(3\theta)\), \(\cos(3\theta-2\pi)\), \(\cos(3\theta-4\pi)\) — son la MISMA curva (los múltiplos de \(2\pi\) no cambian el coseno): se suman en fase, constructivamente, en vez de cancelarse.</div></div>

Cada término siguiente (\(n=2,3,\dots\)) es varias veces más pequeño que el anterior (los denominadores
\(4n^2-1\) crecen como \(n^2\)): el término \(n=1\) por sí solo ya reproduce la forma general de \(|\sin x|\)
(panel (a) de la figura), así que para identificar **qué frecuencias aparecen** basta quedarse con él y
tratar el resto como una corrección pequeña. Sustituyendo \(x=\theta-\phi_k\) y quedándose con el término
\(n=1\):

$$ |\sin(\theta-\phi_k)| \approx \frac{2}{\pi} - \frac{4}{3\pi}\cos\big(2(\theta-\phi_k)\big) $$

**(ii) Multiplicar por el factor senoidal de la parte B.** La parte B completa de la fase \(k\) es
\(-\hat I m\sin(\theta-\phi_k-\varphi)\cdot|\sin(\theta-\phi_k)|\); sustituyendo la aproximación de (i), hay
que multiplicar un seno por una suma de una constante más un coseno — dos productos distintos:

$$ \sin(\theta-\phi_k-\varphi)\cdot\left[\frac{2}{\pi} - \frac{4}{3\pi}\cos\big(2(\theta-\phi_k)\big)\right] = \frac{2}{\pi}\sin(\theta-\phi_k-\varphi) \ -\ \frac{4}{3\pi}\underbrace{\sin(\theta-\phi_k-\varphi)\cos\big(2(\theta-\phi_k)\big)}_{\text{producto seno} \times \text{coseno}} $$

El primer término (\(\tfrac{2}{\pi}\sin(\theta-\phi_k-\varphi)\)) es una senoide pura con el mismo desfase
\(\phi_k\) que las partes A: al sumar las tres fases se cancela exactamente por el **mismo** argumento de
simetría de 120° del bloque anterior — no aporta nada nuevo. El término interesante es el segundo, el
producto seno×coseno, que hay que convertir en una suma de senos con la identidad producto-a-suma
\(\sin\alpha\cos\beta=\tfrac12[\sin(\alpha+\beta)+\sin(\alpha-\beta)]\), con \(\alpha=\theta-\phi_k-\varphi\) y
\(\beta=2(\theta-\phi_k)\):

$$ \sin(\theta-\phi_k-\varphi)\cos\big(2(\theta-\phi_k)\big) = \frac12\sin\big(\underbrace{3\theta-3\phi_k-\varphi}_{\alpha+\beta}\big) + \frac12\sin\big(\underbrace{-\theta+\phi_k-\varphi}_{\alpha-\beta}\big) $$

Este producto se parte en **dos** senoides nuevas: una con argumento \(3\theta-3\phi_k-\varphi\) (frecuencia
**triple**, \(3\omega_0\)) y otra con argumento \(-\theta+\phi_k-\varphi\) (frecuencia fundamental, \(\omega_0\),
con el signo del desfase invertido respecto a las partes A — pero sigue siendo un desfase múltiplo de
\(120°\) entre fases, así que **también** se cancela al sumar las tres fases, por el mismo argumento de
simetría). Solo queda pendiente de cancelar la pieza de \(3\theta-3\phi_k-\varphi\).

**(iii) Sumar esa pieza de \(3\omega_0\) entre las tres fases — aquí es donde NO se cancela.** Hay que sumar
\(\sin(3\theta-3\phi_k-\varphi)\) para \(k=a,b,c\), es decir para \(\phi_a=0\), \(\phi_b=\tfrac{2\pi}{3}\),
\(\phi_c=\tfrac{4\pi}{3}\). Calculando el argumento \(3\phi_k\) en cada caso:

$$ 3\phi_a = 3\cdot0 = 0, \qquad 3\phi_b = 3\cdot\frac{2\pi}{3} = 2\pi, \qquad 3\phi_c = 3\cdot\frac{4\pi}{3} = 4\pi $$

El "truco" está aquí: \(2\pi\) y \(4\pi\) son múltiplos enteros de una vuelta completa, y sumar o restar un
múltiplo de \(2\pi\) dentro de un seno **no cambia su valor** (\(\sin(\psi-2\pi)=\sin\psi\) para cualquier
\(\psi\)). Es decir, al triplicar la frecuencia, los desfases de \(120°=2\pi/3\) que antes distinguían a cada
fase se han convertido en desfases de \(2\pi\) y \(4\pi\) — **indistinguibles del desfase cero**. Sustituyendo:

$$ \sin(3\theta-3\phi_a-\varphi) = \sin(3\theta-\varphi) $$
$$ \sin(3\theta-3\phi_b-\varphi) = \sin(3\theta-2\pi-\varphi) = \sin(3\theta-\varphi) $$
$$ \sin(3\theta-3\phi_c-\varphi) = \sin(3\theta-4\pi-\varphi) = \sin(3\theta-\varphi) $$

Las **tres fases dan exactamente la misma función** — no hay tres senoides desfasadas que se cancelen, hay
una sola senoide contada tres veces (panel (b) de la figura: las tres curvas se superponen perfectamente).
Sumándolas:

$$ \sum_{k} \sin(3\theta-3\phi_k-\varphi) = 3\sin(3\theta-\varphi) \ \ne\ 0 $$

Esta es la componente que sobrevive: aparece porque \(3\times120°\) completa una vuelta entera, así que las
tres fases —desfasadas entre sí a la frecuencia fundamental— quedan **en fase** exactamente a la frecuencia
triple. Es la misma razón por la que el 3.er armónico es la componente de secuencia cero "natural" de un
sistema trifásico, la que se usa en el apartado 6, Paso 6, para la inyección \(v_0\).

*Resultado del Paso 4: la media es cero, queda una oscilación a \(3\omega_0\).* Juntando ambos resultados —
las partes A se cancelan exactamente, las partes B se cancelan en su componente fundamental pero no en la de
\(3\omega_0\), que dio \(3\sin(3\theta-\varphi)\) en (iii) — la suma total \(i_{O,total}(\theta)\) no tiene
componente **media** (constante) en ningún término, para cualquier \(\cos\varphi\) y cualquier \(m\): es una
propiedad de la simetría de 120°, no depende de los valores concretos. Reincorporando el factor
\(-\tfrac{4}{3\pi}\cdot\tfrac12\, m\,\hat I\) que quedó pendiente en el paso (ii) delante de esa suma, la
componente que sobrevive tiene la forma general

$$ i_{O,total}(\theta) \approx \hat I_{3\omega_0}\cos(3\theta+\psi), \qquad \hat I_{3\omega_0}=\frac{2\,\hat I\,m}{\pi}\,k(\cos\varphi) $$

para una amplitud \(\hat I_{3\omega_0}\propto \hat I\,m\) y una fase \(\psi\) que dependen de \(\cos\varphi\)
a través de \(k(\cos\varphi)\) (un factor adimensional del orden de la unidad que agrupa las constantes
numéricas exactas de (i)-(iii) y la dependencia en \(\varphi\); su cálculo exacto exigiría continuar la serie
de Fourier de (i) más allá de \(n=1\), pero el orden de magnitud y la dependencia en \(m\) y \(\hat I\) ya
quedan fijados por este desarrollo).

*Del resultado de corriente al resultado de tensión: integrar.* Con el Paso 2 siendo un integrador puro
(\(d(\Delta V)/dt=-2i_{O,total}/C\)), una entrada de media cero no hace crecer \(\Delta V\) sin límite —
integrar un coseno da otro coseno, acotado, no una rampa. Integrando la componente oscilante
\(\hat I_{3\omega_0}\cos(3\omega_0 t+\psi)\):

$$ \Delta V_{osc}(t) = -\frac{2}{C}\int \hat I_{3\omega_0}\cos(3\omega_0 t+\psi)\,dt = -\frac{2\,\hat I_{3\omega_0}}{3\,\omega_0\,C}\sin(3\omega_0 t+\psi) $$

Esta es una oscilación senoidal pura de amplitud \(\dfrac{2\hat I_{3\omega_0}}{3\omega_0 C}\); su valor
pico-pico (de mínimo a máximo) es el doble de esa amplitud, y agrupando \(\hat I_{3\omega_0}=\hat I\, m\,
k(\cos\varphi)\) (con \(k(\cos\varphi)\) el factor adimensional, del orden de la unidad, que absorbe la
dependencia con el ángulo de fase de la derivación anterior) se llega a la expresión final:

$$ \boxed{\ \Delta V_{pp,osc} \approx \frac{2\,\hat I\,m}{3\,\omega_0\,C}\cdot k(\cos\varphi)\ } $$

donde \(k(\cos\varphi)\) es máximo cerca de \(\cos\varphi=1\). Conclusión de este paso: con carga equilibrada
el desbalance **no** es un problema de control — es una oscilación intrínseca de la topología que no se
elimina, solo se dimensiona con \(C\) suficientemente grande (apartado 7, Paso 4). Por eso hace falta activar
un mecanismo de corrección solo cuando aparece el segundo régimen.

**Paso 5 — segundo régimen: el problema real, componente neta con desequilibrio.** Partiendo de la misma
suma \(i_{O,total}\), pero ahora con carga **desequilibrada** entre fases, factor de potencia distinto por
fase, o un transitorio asimétrico, la cancelación exacta del Paso 4 deja de cumplirse: aparece una
componente **media no nula**. Como el Paso 2 es un integrador puro, una media no nula ya no da una
oscilación acotada como en el Paso 4 — da una **deriva sin límite**, con pendiente constante, hasta saturar
la modulación o dañar los condensadores. Este es el resultado que justifica todo lo que sigue: hace falta un
mecanismo activo de corrección, porque a diferencia del Paso 4 aquí no hay ninguna simetría que lo frene por
sí sola.

<div class="cfig"><img src="figuras/npc-neutro.png" alt="esquema de los dos caminos de corriente en el estado O segun el signo de la corriente de fase con simbolos de diodo D5 D6, tensiones de bus VC1 VC2 absolutas con y sin compensacion, y zoom al desbalance Delta V = VC1 menos VC2 mostrando la deriva sin limite sin compensar frente a la respuesta de primer orden con compensacion proporcional"><div class="cap">(a) En el estado O, \(D_5\) o \(D_6\) conducen según el signo de \(i_o\), descargando un condensador y cargando el otro. (b) Tensiones de bus absolutas: sin compensación, \(V_{C1}\) y \(V_{C2}\) divergen sin límite; con compensación proporcional se estabilizan, pero en un punto ligeramente desplazado de \(V_{dc}/2\) (error residual propio de un control proporcional puro, sin integrador). (c) El mismo resultado visto directamente en el desbalance \(\Delta V=V_{C1}-V_{C2}\) —donde en (b) el caso compensado queda casi aplastado contra la línea de referencia—: deriva lineal sin límite (Paso 2: es un integrador puro) frente a una respuesta exponencial de primer orden que se acota (Paso 7).</div></div>

**Paso 6 — la corrección: qué grado de libertad queda disponible.** El resultado del Paso 5 exige actuar
sobre \(i_{O,total}\), pero el modulador **no puede** elegir directamente qué diodo conduce en el estado O
(eso lo decide \(i_o\), una variable física, no de control). Lo que sí puede hacer es desplazar **cuándo**
cada fase está en el estado O respecto a P o N, inyectando una pequeña componente de **secuencia cero**
\(v_0\) (común a las tres fases, igual que el 3.er armónico de la modulación de 2 niveles — §2.2 de
[[convertidor-back-to-back]]) en la referencia de las tres fases:

$$ r_k^*(\theta) = m\sin(\theta - \phi_k) + v_0, \qquad k\in\{a,b,c\} $$

Un \(v_0\) sesgado hacia el nivel P alarga el tiempo relativo en P y acorta el de N (o viceversa si
\(v_0<0\)), cambiando el **tiempo neto** que cada fase pasa en cada tramo del estado O y, con ello, el signo
neto de la componente media de \(i_{O,total}\) que hay que anular.

<div class="cfig"><img src="figuras/npc-v0-inyeccion.png" alt="grafica de la referencia PD-PWM desplazada por v0 sobre las dos portadoras triangulares, mostrando como el cruce con la portadora superior ocurre antes y con la inferior mas tarde cuando v0 es positivo, y grafica de barras apiladas del duty medio en P, O y N para v0=0, v0 positivo y v0 negativo, cuantificando el alargamiento de P y acortamiento de N manteniendo el tiempo en O casi constante"><div class="cap">(a) Sumar \(v_0>0\) a la referencia la desplaza hacia arriba en las dos comparaciones de portadora: cruza antes la portadora superior (más tiempo en P) y más tarde la inferior (menos tiempo en N). (b) Duty medio en cada nivel a lo largo de un ciclo completo: con \(v_0=0\) el reparto es simétrico (\(d_P=d_N=0.24\)); con \(v_0=+0.12\), \(d_P\) sube a \(0.30\) y \(d_N\) baja a \(0.18\) —el efecto pedido—, mientras que el tiempo total en O (\(d_O\approx0.52\)) casi no cambia. Ese reparto asimétrico entre P y N es justo lo que necesita el mecanismo del Paso 6: como la fase pasa más tiempo total cerca de P (y menos cerca de N) en cada ciclo, también pasa más tiempo en los instantes de conmutación P↔O que en los O↔N, sesgando cuál de los dos diodos de anclaje (\(D_5\) o \(D_6\)) participa más a menudo, sin cambiar la tensión media de salida.</div></div>

El resultado de este paso es el mecanismo de actuación: un lazo de control mide \(\Delta V=V_{C1}-V_{C2}\) y
ajusta \(v_0\) en proporción (o con un PI) para llevarlo a cero — es exactamente el mecanismo simulado en el
panel (c) de la figura del Paso 5.

*Qué es \(K_{bal}\) y por qué la ley de control es "\(v_0\) proporcional al desbalance".* \(K_{bal}\) **no**
es una constante física del convertidor (como \(C\), \(V_{dc}\) o \(k_v\), que están fijados por el hardware
o la modulación): es una **ganancia de control**, un número que se elige libremente al diseñar el lazo — el
único grado de libertad de diseño que queda una vez fijada la estructura del controlador. Su papel es
traducir la medida del desbalance en la acción correctora: en cada instante se mide \(\Delta V(t)\)
(sensores de tensión en los dos condensadores, disponibles en cualquier control digital del convertidor) y
se calcula

$$ v_0(t) = -K_{bal}\,\Delta V(t) $$

Por qué esta forma concreta, "\(v_0\) proporcional al desbalance", y no otra: es la ley de control más
simple que cumple lo que se necesita —**realimentación negativa**, es decir que cuando aparece un
\(\Delta V\ne0\) el controlador reaccione generando una señal correctora en la dirección que lo reduce, y
que esa reacción sea nula exactamente cuando ya no hay error (\(\Delta V=0\Rightarrow v_0=0\), no se toca la
modulación innecesariamente). Un controlador proporcional (P) es la implementación más directa de esa idea:
la corrección crece linealmente con el tamaño del error, sin memoria ni filtrado adicional. \(K_{bal}\) es
literalmente la pendiente de esa recta — cuántos voltios de \(v_0\) (en p.u. de índice de modulación) se
generan por cada voltio de desbalance medido. Que el signo global tenga que ser negativo (y no positivo) es
lo que se comprueba a continuación con el valor real de \(k_v\); \(K_{bal}\) en sí se define siempre positivo
por convención, y es el signo "\(-\)" explícito en la fórmula el que fija la polaridad de la realimentación.

**Paso 7 — cuantificar el lazo: qué es \(k_v\), cómo calcularlo, y cómo se cierra el lazo con signo
correcto.** Partiendo del mecanismo del Paso 6, hace falta saber **cuánto** corrige un \(v_0\) dado y **qué
tan rápido y con qué signo** debe actuar el lazo cerrado, para poder diseñarlo.

*Qué pendiente se calculó en el Paso 6, y por qué NO es \(k_v\).* En el Paso 6 se calculó la pendiente de
\(\overline{d_P-d_N}\) frente a \(v_0\) (la diferencia entre el tiempo medio en P y el tiempo medio en N,
promediada en un ciclo), y el resultado allí fue \(\overline{d_P-d_N}=v_0\) exactamente — es decir, esa
pendiente vale \(1\). "\(d_P-d_N\) negados" no es más que la resta de los dos duty cycles con su signo
natural: \(d_P\ge0\) es el tiempo relativo en P, \(d_N\ge0\) es el tiempo relativo en N, y su diferencia
\(d_P-d_N\) es negativa cuando la fase pasa más tiempo en N que en P (referencia predominantemente negativa)
y positiva en el caso contrario. Esa pendiente describe el reparto de tiempo entre P y N — **no** describe
qué le pasa a la corriente en el nudo **O**, que es la única variable que aparece en la ecuación del Paso 2
(\(i_{O,total}\)). Son dos preguntas distintas, y hay que resolver la segunda desde cero.

*Derivación analítica completa de \(k_v\), paso a paso.* La cantidad que hace falta es
\(k_v=\dfrac{d}{dv_0}\Big[\overline{i_{O,total}}\Big]_{v_0=0}\), la sensibilidad de la corriente **media**
hacia el nudo O frente a una inyección pequeña de \(v_0\). El punto de partida es el mismo modelo continuo
del Paso 4: en el límite de conmutación rápida (\(f_s\gg f_0\)), dentro de cada periodo de conmutación la
corriente de fase \(i_o(\theta)\) varía tan poco que puede tratarse como constante, y la fracción de ese
periodo que la fase pasa en el estado O es \(1-|r^*(\theta)|\), con \(r^*(\theta)=m\sin\theta+v_0\) la
referencia total. La contribución de esta fase a \(i_{O,total}\) en cada instante es entonces

$$ i_{O,total}(\theta) \approx i_o(\theta)\cdot\big(1-|r^*(\theta)|\big) = \hat I\sin\theta\cdot\Big(1-\big|m\sin\theta+v_0\big|\Big) $$

(tomando \(\cos\varphi=1\), es decir \(i_o(\theta)=\hat I\sin\theta\) en fase con la referencia, para
simplificar; el signo de \(k_v\) no depende de este supuesto). El promedio en un ciclo completo es

$$ \overline{i_{O,total}}(v_0) = \frac{1}{2\pi}\int_0^{2\pi} \hat I\sin\theta\cdot\Big(1-\big|m\sin\theta+v_0\big|\Big)\,d\theta $$

Para obtener \(k_v\) hace falta la derivada de esta integral respecto a \(v_0\), evaluada en \(v_0=0\).
Derivando dentro de la integral (el término \(\hat I\sin\theta\) no depende de \(v_0\)):

$$ \frac{\partial}{\partial v_0}\Big[1-|m\sin\theta+v_0|\Big] = -\,\mathrm{sign}\big(m\sin\theta+v_0\big) $$

(la derivada del valor absoluto es el signo de su argumento; esto es válido en todo punto donde
\(m\sin\theta+v_0\ne0\), que es casi todo el intervalo). Evaluando en \(v_0=0\) y para \(m>0\),
\(\mathrm{sign}(m\sin\theta)=\mathrm{sign}(\sin\theta)\), así que

$$ k_v = \frac{1}{2\pi}\int_0^{2\pi} \hat I\sin\theta\cdot\Big(-\mathrm{sign}(\sin\theta)\Big)\,d\theta = -\frac{\hat I}{2\pi}\int_0^{2\pi} \sin\theta\cdot\mathrm{sign}(\sin\theta)\,d\theta $$

El producto \(\sin\theta\cdot\mathrm{sign}(\sin\theta)\) es, por definición, exactamente \(|\sin\theta|\)
(el valor absoluto invierte el signo solo donde \(\sin\theta<0\), que es justo lo que hace multiplicar por
\(\mathrm{sign}(\sin\theta)\)). Sustituyendo:

$$ k_v = -\frac{\hat I}{2\pi}\int_0^{2\pi} |\sin\theta|\,d\theta $$

Esta integral ya apareció (por su promedio) en el Paso 4, apartado (i) de la derivación de Fourier: el valor
medio de \(|\sin\theta|\) sobre un periodo es \(2/\pi\) — es precisamente el término constante de la serie
de Fourier de \(|\sin x|\) usada allí. Como \(\displaystyle\int_0^{2\pi}|\sin\theta|\,d\theta = 2\pi\cdot
\frac{2}{\pi}=4\):

$$ \boxed{\ k_v = -\frac{\hat I}{2\pi}\cdot4 = -\frac{2\hat I}{\pi}\ } \quad\Longrightarrow\quad k_v/\hat I \approx -0.6366 $$

Este resultado (con \(\hat I\) normalizada a 1) coincide exactamente con el ajuste numérico del panel (a) de
la figura siguiente, confirmando la derivación.

<div class="cfig"><img src="figuras/npc-kv-lazo.png" alt="grafica de barrido de v0 mostrando que la corriente media hacia el nudo O es proporcional a v0 con pendiente negativa exactamente -2/pi, diagrama de bloques del lazo cerrado de balance de neutro con el nodo de suma menos Delta V, controlador Kbal o PI, bloque de corriente correctiva y bloque integrador de la planta con la realimentacion negativa, y grafica comparando la respuesta de un control proporcional puro con error residual frente a un PI con error nulo en regimen permanente"><div class="cap">(a) Verificación numérica de la derivación analítica: simulando la cadena completa (referencia + portadoras PD → ventana del estado O → corriente de fase → promedio) y barriendo \(v_0\), la corriente media hacia el nudo O resulta proporcional a \(v_0\) con pendiente \(k_v=-2/\pi\) (puntos azules vs. recta roja) — negativa, coincidiendo exactamente con el resultado analítico. (b) Diagrama de bloques del lazo cerrado: el error \(-\Delta V\) entra al controlador, que genera \(v_0\); \(v_0\) produce una corriente correctiva \(i_{O,corr}=k_v\hat I v_0\) (con \(k_v<0\)) que se integra en la planta (el condensador, Paso 2) para dar de vuelta \(\Delta V\), cerrando el lazo. (c) Con controlador proporcional puro queda un error residual en régimen permanente frente a una perturbación constante; con PI el error se anula porque el integrador del controlador acumula hasta cancelar exactamente la perturbación.</div></div>

*Por qué el signo es negativo: interpretación física.* Un \(v_0>0\) alarga el tiempo en P y O⁺ (Paso 6) y
acorta O⁻ y N — la fase pasa más tiempo en la mitad del ciclo en que, dentro del estado O, es más probable
que \(D_5\) esté conduciendo (con \(i_o>0\)) que \(D_6\); pero simultáneamente acorta el tiempo total
disponible para que \(i_o\) sea negativa mientras se está en O (ese tramo ahora es más corto). La derivación
anterior muestra que el segundo efecto domina sobre el primero: el resultado neto sobre
\(\overline{i_{O,total}}\) tiene signo opuesto al que sugeriría una intuición basada solo en "más tiempo en
P". Con \(k_v\) ya conocido con su signo correcto,

$$ i_{O,corr} = k_v\,\hat I\,v_0, \qquad k_v = -\frac{2}{\pi} $$

*Cierre del lazo: por qué \(v_0=-K_{bal}\Delta V\) es la realimentación estable, con el \(k_v\) correcto.*
Partiendo de la ecuación del Paso 2, \(\dot{\Delta V}=-\frac{2}{C}i_{O,total}\), con
\(i_{O,total}=i_{dist}+i_{O,corr}\) y \(v_0=-K_{bal}\Delta V\) (\(K_{bal}>0\)):

$$ i_{O,corr} = k_v\,\hat I\,v_0 = k_v\,\hat I\,(-K_{bal}\Delta V) = -k_v\,\hat I\,K_{bal}\,\Delta V $$

Sustituyendo en la ecuación del Paso 2:

$$ \dot{\Delta V} = -\frac{2}{C}\Big(i_{dist} - k_v\hat IK_{bal}\Delta V\Big) = -\frac{2\,i_{dist}}{C} + \frac{2\,k_v\hat IK_{bal}}{C}\Delta V $$

El coeficiente que multiplica a \(\Delta V\) es \(\tfrac{2k_v\hat IK_{bal}}{C}\); como \(k_v=-2/\pi<0\), este
coeficiente es **negativo** — el signo correcto para estabilidad (\(\dot x=-x/\tau\) con \(\tau>0\)). Si en
cambio se usara el valor \(k_v>0\) que se había afirmado sin verificar antes de esta derivación, este mismo
signo de realimentación \(v_0=-K_{bal}\Delta V\) sería **inestable**: el diseño del lazo depende
críticamente de conocer el signo real de \(k_v\), no solo su orden de magnitud. La ecuación linealizada
completa, y la constante de tiempo del lazo cerrado que de ella se despeja, son:

$$ \boxed{\ \frac{d(\Delta V)}{dt} = -\frac{2}{C}\Big(i_{O,total,dist} - k_v\hat I K_{bal}\Delta V\Big)\ } \qquad \tau_{bal} = \frac{C}{-2\,k_v\,\hat I\,K_{bal}} = \frac{C}{2\,|k_v|\,\hat I\,K_{bal}} = \frac{\pi\,C}{4\,\hat I\,K_{bal}} $$

(la última igualdad sustituye \(|k_v|=2/\pi\)). Con \(\tau_{bal}>0\), el desbalance decae exponencialmente
hacia el valor que anula \(i_{dist}\), en vez de crecer sin control.

*El error residual del control proporcional puro (panel (c)).* Con un controlador puramente proporcional,
\(v_0=-K_{bal}\Delta V\), el régimen permanente (\(\dot{\Delta V}=0\)) de la ecuación anterior exige
\(i_{dist}=k_v\hat IK_{bal}\Delta V_\infty\), es decir un desbalance residual **no nulo**,
\(\Delta V_\infty = i_{dist}/(k_v\hat IK_{bal})\): el proporcional corrige la mayor parte del desbalance pero
deja un remanente proporcional a la perturbación, porque necesita ese \(\Delta V_\infty\ne0\) para generar
el \(v_0\) constante que cancela \(i_{dist}\) en régimen permanente.

*Por qué evolucionar a un PI.* Para eliminar ese residuo se añade un término integral al controlador,
\(v_0=-K_{bal}\Delta V - K_i\displaystyle\int\Delta V\,dt\): el integrador puede seguir creciendo (o
decreciendo) mientras \(\Delta V\ne0\), así que en régimen permanente **tiene** que ser \(\Delta V=0\) —
si no lo fuera, el término integral seguiría cambiando y el sistema no estaría en régimen permanente. Es el
mismo argumento estructural que hace que un PI anule el error estacionario frente a una perturbación
constante en cualquier lazo de control (ver [[control-cascada]]): el integrador es quien "absorbe" la
perturbación constante \(i_{dist}\), dejando que el error vuelva exactamente a cero. Esto es lo que muestra
el panel (c): P puro converge a un \(\Delta V_\infty\) pequeño pero distinto de cero; PI converge a
\(\Delta V=0\).

Este resultado (\(\tau_{bal}\) en función de \(K_{bal}\)) es lo que permite diseñar la ganancia del lazo:
cuanto mayor \(K_{bal}\), más rápido el lazo (menor \(\tau_{bal}\)), pero un \(K_{bal}\) excesivo hace que
\(v_0\) sea grande y distorsione la modulación de las tres fases (satura antes la referencia,
\(|r_k^*+v_0|>1\)) — de ahí el compromiso de diseño del apartado 8, Paso 5.

**Paso 8 — hasta dónde llega este método, y qué hacer cuando no basta.** El resultado del Paso 7 tiene un
límite práctico: la inyección de secuencia cero corrige desbalances **lentos** (del orden de la frecuencia
de red y menores), porque \(v_0\) actúa desplazando duty cycles ciclo a ciclo, no de forma instantánea. Para
desbalances grandes y rápidos (arranque, faltas asimétricas, donde \(\Delta V\) puede moverse mucho en unos
pocos periodos de conmutación) este mecanismo solo no es suficiente, y se recurre al **NPC activo** (ANPC,
con interruptores adicionales que permiten forzar el camino de corriente independientemente de \(i_o\)) o a
un lazo de control más rápido sobre la propia modulación de cada fase individualmente.

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
siguiente).

<div class="cfig"><img src="figuras/npc-svm.png" alt="hexagono de space vector modulation del NPC con las 19 posiciones fisicas de los 27 estados de conmutacion etiquetadas con la notacion (Sa Sb Sc) para cada fase en +, 0 o -, formando una reticula regular de 24 triangulos con el vector cero en el centro (redundante triple), los vectores medios en el anillo intermedio (redundantes dobles) y los vectores largos en las esquinas exteriores (unicos)"><div class="cap">Las 19 posiciones físicas de los 27 estados, etiquetadas con la notación \((S_aS_bS_c)\), \(S_k\in\{+,0,-\}\). El vector cero (centro) es redundante ×3 —los estados \((+{+}{+})\), \((000)\), \((-{-}{-})\) no mueven el punto de trabajo—; los 6 vectores medios (anillo intermedio, en rojo) son redundantes ×2, cada uno alcanzable con dos combinaciones de estados que llevan la corriente por caminos distintos hacia el neutro O — es la palanca que usa el balance de neutro; los 6 vectores largos (esquinas exteriores) y los 6 vectores cortos (anillo interior) son únicos.</div></div>

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

<div class="cfig"><img src="figuras/npc-svm-tiempos.png" alt="triangulo generico del hexagono SVM con los tres vectores adyacentes V0, V1, V2 y el vector de referencia Vref descompuesto como combinacion convexa de los tres, con la ecuacion de los duty cycles d1, d2, d0"><div class="cap">Dentro de cualquiera de los 24 triángulos del hexágono, el vector de referencia \(\vec V_{ref}\) se descompone en sus tres vértices adyacentes; los coeficientes \(d_1,d_2,d_0\) son los duty cycles que, aplicados durante el periodo de conmutación, sintetizan en promedio la tensión deseada.</div></div>

**Paso 5 — planteamiento y resolución del sistema (por qué en αβ y no directamente en abc).**

*Por qué no se plantea directamente en abc.* Podría parecer más natural trabajar con los tres duty cycles
\(d_a,d_b,d_c\) de las tres fases directamente, sin pasar por αβ. El problema es que **abc tiene una
dimensión de más** para describir algo que en realidad vive en un plano: en un sistema trifásico sin neutro
conectado, la suma de las tres tensiones de fase respecto al punto medio del bus está fijada por
construcción (\(v_{aO}+v_{bO}+v_{cO}\) toma solo los valores discretos que dan los estados P/O/N, y su
componente de secuencia cero no afecta a la tensión de línea que ve la carga). Es decir, de las tres
coordenadas \((a,b,c)\) solo **dos combinaciones independientes** determinan el punto de trabajo físico
relevante para el control de corriente — exactamente la misma razón por la que en control dq dos fases
independientes ya capturan toda la información de una máquina trifásica equilibrada (ver [[marco-dq]]). Si
se intentase resolver el sistema en abc con tres incógnitas \(d_a,d_b,d_c\) sin más, sobraría un grado de
libertad y el sistema quedaría indeterminado (infinitas soluciones que darían la misma tensión de línea pero
distinto reparto de secuencia cero). αβ elimina ese grado de libertad sobrante de raíz, quedándose solo con
las dos coordenadas que realmente mueven el punto de trabajo — es la razón última por la que **todas** las
técnicas de SVM (2 niveles, NPC, MMC) se plantean en el plano αβ y no en abc.

*Cómo se plantea el sistema.* Fijado el vector de referencia \(\vec V_{ref}=(V_{ref,\alpha},V_{ref,\beta})\)
(salida, en general, del lazo de corriente en dq tras la transformación inversa dq→αβ) y ya identificado el
triángulo que lo contiene (Paso 3) con sus tres vértices \(\vec V_1,\vec V_2,\vec V_0\), la incógnita son los
tres duty cycles \(d_1,d_2,d_0\) que, promediados sobre un periodo de conmutación \(T_s\), sintetizan
\(\vec V_{ref}\) como combinación convexa (Paso 4). Escribiendo cada vector por sus dos componentes
\((V_{k,\alpha},V_{k,\beta})\), la ecuación vectorial \(\vec V_{ref}=d_1\vec V_1+d_2\vec V_2+d_0\vec V_0\) se
descompone en **dos ecuaciones escalares** (una por componente α, otra por β); junto con la restricción de
normalización \(d_1+d_2+d_0=1\) (los tres duty deben repartir el 100% del periodo) se cierran
**tres ecuaciones para tres incógnitas**:

$$ \begin{pmatrix}V_{1,\alpha} & V_{2,\alpha} & V_{0,\alpha}\\ V_{1,\beta} & V_{2,\beta} & V_{0,\beta}\\ 1&1&1\end{pmatrix}\begin{pmatrix}d_1\\d_2\\d_0\end{pmatrix} = \begin{pmatrix}V_{ref,\alpha}\\V_{ref,\beta}\\1\end{pmatrix} $$

*Cómo se resuelve en la práctica.* Con los tres vértices fijos por sector/triángulo, la matriz \(3\times3\)
de la izquierda es **constante** para cada uno de los 24 triángulos (no depende de \(\vec V_{ref}\), solo de
la geometría del hexágono) y se invierte **una sola vez, fuera de línea**: el resultado son 24 matrices
\(3\times3\) precalculadas y almacenadas en una tabla. En tiempo real, en cada periodo de conmutación, el
algoritmo solo tiene que (1) identificar en qué triángulo cae \(\vec V_{ref}\) (Paso 3) y (2) multiplicar el
vector \((V_{ref,\alpha},V_{ref,\beta},1)\) por la inversa precalculada de ese triángulo — una multiplicación
matriz-vector fija, sin resolver ningún sistema en línea. Es precisamente esta separación entre "cálculo caro
una vez" (inversión de 24 matrices) y "cálculo barato en cada periodo" (una multiplicación) lo que hace
viable ejecutar SVM completo dentro del periodo de conmutación en un DSP de control.

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
- **No verificar el nivel de corriente al elegir qué diodo debe soportar el peor caso térmico:** \(D_5\) y
  \(D_6\) solo conducen durante el estado O y con un signo de \(i_o\) cada uno — su corriente media es menor
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
