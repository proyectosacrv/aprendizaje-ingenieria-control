---
titulo: "HVDC-VSC: topología, modelado, control, cable DC, MTDC y protección"
slug: hvdc-vsc-topologia
categoria: fisica-modelado
tipo: concepto
nivel: avanzado
proyectos: []
objetivos: [comprender la arquitectura del HVDC-VSC y el MMC, modelar el balance de potencia y la dinamica de Vdc del enlace, disenar el control jerarquico de un terminal VSC-HVDC, modelar el cable DC y su falta, distinguir configuraciones punto a punto vs MTDC, entender el droop DC y la proteccion DC, comparar con LCC]
tags: [hvdc, vsc, mmc, lcc, monopolar, bipolar, punto-a-punto, multi-terminal, offshore, cable-dc, falta-dc, dccb, droop-dc, mtdc, modelado-vdc, control-jerarquico, lazo-dq]
fecha_creacion: 2026-07-05
fecha_actualizacion: 2026-08-16
relacionados: [convertidor-back-to-back, topologias-multinivel, filtro-lcl, fenomenos-oscilatorios-red, mmc-modelo-control, dinamica-bus-dc, control-tension-bus-dc]
referencias:
  - "Cigré TB 604, Guide for the Development of Models for HVDC Converters"
  - "Lesnicar & Marquardt, An Innovative Modular Multilevel Converter Topology"
  - "Hertem, Gomis-Bellmunt, Liang, HVDC Grids: For Offshore and Supergrid of the Future, Wiley 2016"
  - "Beerten, Cole, Belmans, Generalized Steady-State VSC MTDC Model, IEEE TPWRS 2012"
---

## 1 — Definición y motivación del HVDC-VSC

HVDC-VSC (High Voltage Direct Current con Voltage Source Converter) transmite potencia eléctrica en
corriente continua usando convertidores de fuente de tensión en ambos extremos. A diferencia del HVDC
clásico con tiristores (LCC-HVDC, apartado 12), el VSC-HVDC:

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

La arquitectura de la red DC define el número de conductores y el comportamiento ante faltas. Las tres
opciones comparten el mismo bloque básico en cada extremo — red AC, transformador de acoplamiento y
convertidor VSC — y se diferencian solo en cuántos conductores DC hay entre los dos extremos y cómo (o
si) se conectan a tierra.

**Monopolar con retorno por tierra.** Un único conductor transporta la corriente de ida a \(+V_{dc}\); el
circuito se cierra por tierra o por el lecho marino a través de un electrodo de tierra en cada estación,
sin ningún conductor de retorno metálico dedicado.

<div class="cfig"><img src="figuras/hvdc-config-monopolar.png" alt="esquema de HVDC monopolar con retorno por tierra: dos estaciones VSC con transformador de acoplamiento a red AC unidas por un unico conductor DC a tension positiva, con electrodo de tierra real en cada extremo cerrando el circuito por tierra o mar"><div class="cap">Configuración monopolar: un único conductor a \(+V_{dc}\) entre las dos estaciones; el retorno de la corriente se produce por tierra/mar, con un electrodo de tierra dedicado en cada extremo (símbolo de tierra clásico).</div></div>

Es la configuración más barata (la mitad del cobre/aluminio que cualquier alternativa de dos
conductores), pero la corriente de retorno circulando por tierra genera **corrientes vagabundas**
(*stray currents*) que se difunden por el terreno o el fondo marino y aceleran la corrosión electrolítica
de tuberías, estructuras metálicas enterradas y armaduras de otros cables cercanos — es el mismo
mecanismo de la protección catódica pero en sentido indeseado. Por esta razón está en desuso en
instalaciones modernas salvo en aplicaciones muy específicas de bajo coste y corta duración.

**Bipolar.** Dos conductores independientes, uno a \(+V_{dc}\) y otro a \(-V_{dc}\) respecto a tierra,
cada uno con su propia pareja de convertidores (dos "polos" que en la práctica son dos enlaces monopolares
en paralelo, compartiendo trazado de cable pero eléctricamente independientes). Existe además un conductor
metálico de retorno/neutro de baja sección, que en operación normal apenas lleva corriente (solo el
pequeño desequilibrio entre polos) pero que permite seguir cerrando el circuito sin depender de tierra.

<div class="cfig"><img src="figuras/hvdc-config-bipolar.png" alt="esquema de HVDC bipolar: dos pares de estaciones VSC independientes, uno para el polo positivo y otro para el polo negativo, unidos por un conductor metalico de retorno de baja corriente con electrodo de tierra en ambos extremos"><div class="cap">Configuración bipolar: dos polos eléctricamente independientes (\(+V_{dc}\) en rojo, \(-V_{dc}\) en azul), cada uno con su propio convertidor en cada estación, más un conductor metálico de retorno/neutro (línea punteada) que en operación normal lleva muy poca corriente.</div></div>

Es el **estándar moderno** por su combinación de coste razonable y redundancia real: si el polo negativo
falla (por una avería en su convertidor o una falta en su conductor), el polo positivo puede seguir
transmitiendo el 50 % de la potencia nominal usando temporalmente tierra como camino de retorno (el modo
"monopolar de emergencia"), sin necesidad de intervención manual inmediata — la mitad de la capacidad se
recupera automáticamente mientras se repara el polo averiado. Esta es la razón por la que casi todos los
enlaces HVDC-VSC de nueva construcción de cierta envergadura (DolWin, BorWin, NordLink — apartado 11) usan
esta configuración.

**Simétrica monopolar.** Dos conductores a \(\pm V_{dc}/2\) que salen del mismo convertidor (el punto
medio del bus DC interno, no dos convertidores separados como en bipolar), sin ningún punto de conexión a
tierra en todo el enlace: ambos polos quedan simétricamente flotantes respecto a tierra.

<div class="cfig"><img src="figuras/hvdc-config-simetrica.png" alt="esquema de HVDC simetrica monopolar: dos estaciones VSC unidas por dos conductores a mas menos Vdc medio, sin ningun electrodo ni conexion a tierra en ninguno de los extremos, marcado explicitamente con una cruz"><div class="cap">Configuración simétrica monopolar: dos conductores a \(\pm V_{dc}/2\) desde el mismo convertidor, sin conexión a tierra en ningún extremo (marcado con ✕) — el punto medio del enlace flota eléctricamente.</div></div>

Al no necesitar transformadores ni electrodos de puesta a tierra dedicados, es **más económica** que la
bipolar y más ligera — una ventaja relevante en plataformas offshore donde el peso de cada equipo se
traduce directamente en coste de la estructura. El precio es la ausencia de la redundancia de la bipolar:
al ser un único convertidor por extremo, una falta en cualquiera de los dos conductores obliga a parar el
enlace completo, no solo la mitad de la potencia.

**La tensión nominal como decisión económica.** En cualquiera de las tres configuraciones, la tensión
nominal del enlace resulta de equilibrar el coste del cable (que crece con la sección de cobre necesaria
para una corriente dada, pero baja si se sube la tensión para la misma potencia) frente al coste del
convertidor y su aislamiento (que crece con la tensión). Tensiones típicas actuales:
\(\pm320\,\text{kV}\) en cables submarinos, \(\pm500\,\text{kV}\) en líneas aéreas; potencias de
200 MW a 2 GW por enlace punto a punto.

**Topologías de red MTDC.** Cuando hay tres o más terminales en la misma red DC (apartado 6), la
disposición geométrica de los cables entre ellos define otra decisión de topología independiente de la
configuración de polos anterior:

<div class="cfig"><img src="figuras/hvdc-mtdc-topologias.png" alt="comparacion de topologias de red MTDC: radial con un nodo central conectado a cinco terminales VSC en estrella, y mallada con cuatro terminales VSC conectados por multiples caminos redundantes con un DCCB marcado en cada extremo de cada linea"><div class="cap">(a) Topología radial: cada terminal conectado por un único camino a un nodo central — barata pero sin redundancia, un fallo de cable aísla toda esa rama. (b) Topología mallada: múltiples caminos redundantes entre terminales, con un DCCB (cuadrado rojo) en cada extremo de cada línea para poder aislar solo el tramo en falta sin perder el resto de la red.</div></div>

La **radial** conecta cada terminal por un único camino a un nodo central (o a los demás terminales en
cadena): es simple y económica para 3–4 terminales, pero el nodo central (o cualquier tramo intermedio)
es un punto único de fallo — perderlo aísla toda esa rama de la red. La **mallada** añade conexiones
redundantes entre terminales de modo que existe más de un camino entre cualquier par de nodos: mayor
coste de cable y de disyuntores DC (uno en cada extremo de cada línea, apartado 9), pero sin punto único
de fallo — es la topología objetivo de las futuras superredes DC offshore (North Sea Wind Power Hub,
apartado 11).

## 3 — El convertidor: el MMC (resumen — desarrollo completo en [[mmc-modelo-control]])

El MMC (Modular Multilevel Converter) es el convertidor dominante en HVDC moderno desde ~2010,
sustituyendo al VSC de dos niveles con IGBT de alta tensión por su mejor calidad de forma de onda,
menores pérdidas y mayor escalabilidad. Cada fase tiene dos brazos (superior e inferior), cada uno con
\(N\) submódulos (SM) en serie más una inductancia de brazo \(L_{arm}\); cada SM aporta \(v_{SM}=V_C\)
(insertado) o \(0\) (bypass), y con \(N=200\)–400 SMs por brazo la tensión de salida tiene \(N{+}1\)
niveles, con THD despreciable sin filtro AC de potencia.

Este apartado no repite ese desarrollo. La ficha [[mmc-modelo-control]] cubre en detalle: el modelo
eléctrico completo (ecuaciones de brazo, descomposición en corriente de fase/circulación), el balance de
energía de los brazos, la derivación completa de la corriente de circulación a \(2\omega_0\) y su
control (CCSC), la modulación (NLM con sorting de condensadores), la jerarquía de cuatro capas de
control, el dimensionado (energía almacenada, \(V_{C,nom}\), \(C_{SM}\)) y las pérdidas por submódulo.
Lo relevante para este capítulo (arquitectura y sistema HVDC) es que el MMC es lo que hace posible operar
sin filtro AC de potencia y con pérdidas de conmutación mínimas — las dos propiedades que distinguen al
VSC-HVDC moderno del VSC de dos niveles de la primera generación (BorWin1, apartado 11).

## 4 — Modelado del enlace: balance de potencia y dinámica de \(V_{dc}\)

**Qué problema resuelve este apartado.** Los apartados anteriores describen la topología (cómo está
construido el enlace); este describe su **comportamiento dinámico**: qué ecuación gobierna la tensión del
bus DC de cada terminal, por qué esa ecuación no es lineal en \(V_{dc}\), y qué variable conviene usar
para poder diseñar un controlador con las herramientas lineales habituales.

**El sistema de dos terminales como cadena de bloques.** Un enlace punto a punto es, eléctricamente, una
cadena: red AC 1 → convertidor 1 → bus DC 1 (condensador \(C_1\)) → cable DC → bus DC 2 (condensador
\(C_2\)) → convertidor 2 → red AC 2. Cada convertidor VSC actúa como una interfaz de potencia entre su
lado AC y su lado DC: intercambia con la red AC la potencia \(P_{ACi}\) que su control decide, y esa misma
potencia (menos las pérdidas de conmutación y conducción, que se desprecian en el modelo de primer orden)
es la que carga o descarga el condensador del bus DC de su lado.

<div class="cfig"><img src="figuras/hvdc-modelado-enlace.png" alt="esquema del sistema de dos terminales HVDC-VSC mostrando el balance de potencia desde la red AC 1 a traves del convertidor VSC 1, el condensador del bus DC 1, el cable DC con su corriente Iline, el condensador del bus DC 2, el convertidor VSC 2 hasta la red AC 2, con la ecuacion del balance de potencia del condensador; y grafica de la respuesta temporal de Vdc del terminal maestro ante un escalon de carga en el terminal esclavo, usando un PI disenado sobre la variable de energia W en vez de sobre Vdc directamente"><div class="cap">(a) Cadena de bloques del enlace punto a punto: cada convertidor intercambia \(P_{ACi}\) con su red AC, y esa potencia (menos la que fluye por el cable) carga o descarga el condensador de su bus DC — de ahí sale la ecuación de balance de potencia del apartado. (b) Respuesta de \(V_{dc}\) del terminal maestro (el que fija la tensión) ante un escalón de potencia demandada por el terminal esclavo: el PI está diseñado sobre la variable de energía \(W=\tfrac12CV_{dc}^2\), cuya dinámica es exactamente lineal, no sobre \(V_{dc}\) directamente.</div></div>

**Ecuación de balance del bus DC — resultado (derivación completa en [[dinamica-bus-dc]] §1 y
[[control-tension-bus-dc]] §1 y §3).** Ya existe en el repositorio la derivación paso a paso, desde la ley
constitutiva del condensador (\(i_C=dq/dt\)) y el KCL del nudo, de por qué la energía almacenada
\(W=\tfrac12CV_{dc}^2\) obedece \(\dot W=P_{in}-P_{out}\) — **exactamente lineal**, sin ningún término que
dependa de \(W\) mismo — mientras que la ecuación en la propia \(V_{dc}\) sí es no lineal (ganancia
\(1/(CV_{dc})\), variable con el punto de operación). Esta ficha no repite esa derivación: solo la aplica,
adaptando la notación al enlace HVDC (\(P_{in}\to P_{AC}\), la potencia que el convertidor intercambia con
su red; \(P_{out}\to P_{line}=V_{dc}I_{line}\), la que sale hacia el cable):

$$ \frac{dW}{dt} = P_{AC} - P_{line} \qquad\Longleftrightarrow\qquad \frac{dV_{dc}}{dt} = \frac{P_{AC}-P_{line}}{C\,V_{dc}} $$

y hereda la misma conclusión de diseño: el lazo de tensión se cierra sobre \(V_{dc}^2\) (equivalentemente
\(W\)), no sobre \(V_{dc}\) en crudo, precisamente porque esa es la variable en la que la planta es un
integrador puro lineal — la sintonía del PI por ese camino está desarrollada en
[[control-tension-bus-dc]] §2 y §4.

**Lo específico de HVDC: dos condensadores unidos por un cable, no uno solo.** La diferencia real de este
apartado frente a las fichas genéricas de bus DC es que aquí hay **dos** condensadores (uno por terminal)
acoplados por la dinámica del cable (apartado 7) en vez de un único bus alimentando cargas locales: la
potencia que un terminal "pierde" hacia el cable es la que el otro terminal "gana" en su propio balance,
con el retraso y la resonancia LC que introduce el cable de por medio. Es esa cadena de dos plantas
acopladas, no la ecuación de un solo bus, lo que hace falta modelar para diseñar el control jerárquico del
apartado 5.

**Ejemplo verificado: respuesta ante un escalón de carga en el enlace de dos terminales.** El panel (b) de
la figura simula esa cadena completa: el terminal 1 (maestro de \(V_{dc}\)) tiene un PI diseñado sobre
\(W\) con \(\omega_n=100\,\text{rad/s}\) (\(K_{p,W}=2\omega_n\), \(K_{i,W}=\omega_n^2\), el criterio
estándar de segundo orden con amortiguamiento crítico para una planta integradora — método de
[[control-tension-bus-dc]] §2), y el terminal 2 (esclavo de \(P\)) pasa de \(P_2=0\) a
\(P_2=-400\,\text{MW}\) (empieza a absorber potencia) en \(t=8\,\text{ms}\). La tensión del terminal
maestro cae transitoriamente (hasta \(\sim600\,\text{kV}\), un \(6\,\%\) por debajo de la nominal
\(640\,\text{kV}\)) mientras su condensador se descarga entregando la potencia que aún no ha compensado el
lazo, y se recupera en unas pocas decenas de milisegundos — el comportamiento esperado de un sistema de
segundo orden bien amortiguado.

## 5 — Control de un terminal VSC-HVDC: jerarquía de dos lazos

**Qué problema resuelve este apartado.** El apartado 4 estableció la ecuación de la planta
(\(\dot W=P_{AC}-P_{line}\)); este apartado desarrolla el controlador que decide, en cada instante, qué
\(P_{AC}\) pedirle al convertidor. La estructura es exactamente la misma que la del control vectorial de
cualquier VSC conectado a red (idéntica en su forma al lazo de corriente del MSC del PMSG, ver
[[aerogenerador-pmsg-dfig]]): un **lazo interno de corriente** rápido en el marco dq, y un **lazo externo**
más lento que decide las referencias de corriente según el modo de operación del terminal.

<div class="cfig"><img src="figuras/hvdc-control-jerarquia.png" alt="diagrama de bloques del control jerarquico de un terminal VSC-HVDC mostrando el lazo externo en modo maestro de tension Vdc (con el PI sobre la variable de energia) o modo esclavo de potencia P, junto al lazo de potencia reactiva Q, ambos generando las referencias de corriente id* e iq*, que entran al lazo interno de corriente dq compartido con desacoplo feedforward, generando las referencias de tension vd* y vq* que van al modulador PWM del MMC"><div class="cap">Control jerárquico de un terminal VSC-HVDC. El lazo externo decide el modo del terminal (maestro de \(V_{dc}\) o esclavo de \(P\), más el lazo independiente de \(Q\)/tensión AC) y genera las referencias \(i_d^*\), \(i_q^*\); el lazo interno de corriente, con estructura idéntica en todos los modos, las convierte en \(v_d^*\), \(v_q^*\) con desacoplo feedforward, que alimentan el modulador del MMC.</div></div>

**El lazo interno de corriente dq, y por qué desacopla \(P\) y \(Q\).** Con el eje d del marco dq
orientado al vector de tensión de la red en el punto de conexión (\(v_q=0\), el convenio estándar de
control orientado a tensión), la potencia activa y reactiva que el convertidor intercambia con la red se
escriben:

$$ P = \frac{3}{2}\big(v_d i_d + v_q i_q\big) = \frac{3}{2}v_d i_d, \qquad Q = \frac{3}{2}\big(v_q i_d - v_d i_q\big) = -\frac{3}{2}v_d i_q $$

(sustituyendo \(v_q=0\) en la expresión general de potencia instantánea en dq). El resultado —verificado
directamente arriba, no asumido— es que con esta orientación **\(P\) depende únicamente de \(i_d\), y
\(Q\) únicamente de \(i_q\)**: son dos variables de control completamente independientes. Esta es la
propiedad central que distingue al VSC del LCC (apartado 12): el VSC puede fijar \(P\) sin que eso le
imponga ningún valor de \(Q\), simplemente ajustando \(i_d\) e \(i_q\) por separado.

El lazo de corriente en sí (dos PI, uno por eje, con el mismo desacoplo feedforward de los términos
cruzados \(\omega L\,i_q\) y \(\omega L\,i_d\) que ya se derivó para el MSC del PMSG) genera las
referencias de tensión \(v_d^*\), \(v_q^*\) que el modulador del MMC sintetiza en los brazos. Es el lazo
más rápido de la jerarquía, y su estructura **no cambia** según el modo del terminal — lo único que cambia
entre modos es de dónde vienen las referencias \(i_d^*\), \(i_q^*\) que ese lazo recibe. El resto de este
apartado desarrolla, con números reales, **la planta que ve ese lazo de corriente** (que en un MMC no es
la inductancia de conexión a red sin más, sino la de brazo, reducida a la mitad), **la planta que ve el
lazo maestro de \(V_{dc}\)** (que, a diferencia de un bus DC genérico, incluye la dinámica completa del
cable acoplando los dos terminales) y **cómo diseñar ambos lazos, en ambos terminales, de forma
coordinada** — que es precisamente lo que el apartado 4 dejó pendiente.

**Planta del lazo de corriente en un MMC: por qué la inductancia efectiva es \(L_{arm}/2\), no
\(L_{arm}\).** Antes de derivarla algebraicamente, así es la planta reducida a la que llega esta sección
(circuito equivalente entre la tensión que sintetiza el convertidor, \(v_{conv}\), y la tensión de fase de
la red, \(v_a\)):

<div class="cfig"><img src="figuras/hvdc-planta-corriente.png" alt="circuito equivalente reducido de la planta del lazo de corriente del MMC, con Req y Leq en serie entre la fuente de tension del convertidor vconv y la tension de red va, recorrido por la corriente iout, junto a la ecuacion diferencial de la que sale"><div class="cap">Planta reducida del lazo de corriente del MMC: resultado de la derivación que sigue, mostrado antes para tener la referencia visual a mano. \(R_{eq}\), \(L_{eq}\) en serie entre \(v_{conv}\) y \(v_a\), recorridos por \(i_{out}\).</div></div>

A diferencia de un VSC de dos niveles, en el MMC la corriente de fase no ve directamente
\(L_{arm}\): la ve a través de **dos** brazos en paralelo (superior e inferior), y hay que derivarlo desde
las ecuaciones de brazo para no asumirlo. Partiendo de las ecuaciones de KVL de cada brazo de la fase
\(a\) (ya establecidas en [[mmc-modelo-control]] §1, con \(v_a\equiv v_{a0}\) la tensión del punto medio
de fase y \(v_u,v_l\) las tensiones insertadas por los SMs de cada brazo):

$$ L_{arm}\frac{di_u}{dt} = \frac{V_{dc}}{2} - v_u - R_{arm}i_u - v_a, \qquad
   L_{arm}\frac{di_l}{dt} = \frac{V_{dc}}{2} - v_l - R_{arm}i_l + v_a $$

Restando la segunda de la primera y definiendo la corriente de salida \(i_{out}\equiv i_u-i_l\) (la
corriente de fase real hacia la red, salvo un factor 2) y la tensión de convertidor equivalente
\(v_{conv}\equiv(v_l-v_u)/2\), los términos en \(V_{dc}/2\) se cancelan exactamente y queda:

$$ \boxed{\ \frac{L_{arm}}{2}\frac{di_{out}}{dt} = v_{conv} - v_a - \frac{R_{arm}}{2}\,i_{out}\ } $$

Esta es, en forma, **idéntica** a la planta de un VSC de dos niveles conectado a red por una inductancia
\(L\) y resistencia \(R\) (la misma que aparece en [[convertidor-back-to-back]] §2.6): un integrador de
primer orden \(G_i(s)=1/(L_{eq}s+R_{eq})\), pero con **\(L_{eq}=L_{arm}/2\), \(R_{eq}=R_{arm}/2\)** — la
mitad de los valores de un solo brazo, no el valor completo. Este es el resultado que la literatura de MMC
cita como atajo de diseño; aquí queda derivado desde el KVL, no asumido.

**Sintonía numérica del lazo de corriente (cancelación de polo, método de [[convertidor-back-to-back]]
§2.7).** Con \(L_{arm}=0.15\,\text{pu}\) sobre base \(S_{nom}=500\,\text{MVA}\) y \(V_{dc}/2=320\,\text{kV}\)
(apartado 10): \(Z_{base}=(320\,\text{kV})^2/500\,\text{MVA}=204.8\,\Omega\), y con \(\omega_0=2\pi\cdot
50=314.2\,\text{rad/s}\):

$$ L_{arm} = 0.15\times\frac{204.8}{314.2} = 0.0978\,\text{H} = 97.8\,\text{mH} \quad\Longrightarrow\quad
   L_{eq}=48.9\,\text{mH} $$

Para \(R_{arm}\) no hay un valor normalizado único — se fija por el factor de calidad del reactor de
brazo. Tomando \(Q=\omega_0L_{arm}/R_{arm}=30\) (típico de un reactor de núcleo de aire de bajas pérdidas):
\(R_{arm}=\omega_0L_{arm}/30=1.02\,\Omega\), luego \(R_{eq}=0.512\,\Omega\). El PI por cancelación de polo
(\(K_p=\omega_{ci}L_{eq}\), \(T_i=L_{eq}/R_{eq}\), \(K_i=\omega_{ci}R_{eq}\)) necesita elegir \(\omega_{ci}\):
en un VSC de dos niveles el límite superior lo fija la frecuencia de conmutación (\(\omega_{ci}<\omega_{sw}/10\));
en un MMC con NLM y cientos de SMs por brazo la tensión sintetizada es prácticamente continua, así que el
límite real es la **tasa de muestreo del controlador digital** (típicamente 5–10 kHz). Con
\(f_s=10\,\text{kHz}\) y el mismo margen ×10: \(\omega_{ci}\approx2\pi\cdot1000=6283\,\text{rad/s}\)
(1 kHz), y:

$$ K_p=\omega_{ci}L_{eq}=307.2\,\text{V/A}, \qquad T_i=\frac{L_{eq}}{R_{eq}}=0.0955\,\text{s}, \qquad
   K_i=\omega_{ci}R_{eq}=3216\,\text{V/(A·s)} $$

con margen de fase teórico \(90°\) (planta cancelada exactamente), \(60\)–\(75°\) en la práctica por el
retraso de muestreo y modulación — igual que en [[convertidor-back-to-back]] §2.7.

**Lazo cerrado exacto y respuesta al escalón.** Con la cancelación de polo, el lazo abierto se simplifica
algebraicamente a \(L(s)=\text{PI}(s)\,G_i(s)=\omega_{ci}/s\) — un integrador puro — y el lazo cerrado a

$$ T(s)=\frac{L(s)}{1+L(s)}=\frac{\omega_{ci}}{s+\omega_{ci}} $$

un primer orden puro con constante de tiempo \(\tau_{ci}=1/\omega_{ci}=0.159\,\text{ms}\): el escalón de
\(i_d^*\) se sigue al 63 % en \(0.16\,\text{ms}\) y al 99 % en \(\approx0.8\,\text{ms}\) (\(5\tau_{ci}\)) —
casi dos órdenes de magnitud más rápido que la constante de tiempo del cable (\(\tau_{dc}=216\,\text{ms}\),
apartado 7), la separación temporal que justifica tratar este lazo como "instantáneo" al diseñar el lazo
maestro más abajo.

<div class="cfig"><img src="figuras/hvdc-lazo-corriente-respuesta.png" alt="diagrama de bloques del lazo cerrado de corriente con PI y desacoplo feedforward, y respuesta al escalon del lazo cerrado mostrando el primer orden puro con tau igual a un partido de omega ci"><div class="cap">(a) Lazo cerrado (PI + desacoplo feedforward de \(v_a\) + planta + realimentación) — estructura idéntica en todos los modos del terminal. (b) Respuesta al escalón con los valores numéricos diseñados: cancelación de polo exacta \(\Rightarrow\) primer orden puro, \(\tau_{ci}=1/\omega_{ci}\).</div></div>

**El lazo externo, y los dos modos del eje d.** La referencia \(i_d^*\) (que fija \(P\)) puede generarse
de dos formas distintas, según el papel que ese terminal desempeñe en el enlace:

- **Modo maestro de \(V_{dc}\).** Un PI compara \(V_{dc}^*\) con la medida (diseñado, según el apartado 4,
  sobre la variable \(W=\tfrac12CV_{dc}^2\) para tener una planta lineal) y su salida es directamente
  \(i_d^*\). Este terminal no fija su propia potencia: la deja flotar a lo que haga falta para mantener
  \(V_{dc}\) en su consigna, absorbiendo o cediendo automáticamente cualquier diferencia entre lo que el
  resto del sistema pide y lo que hay disponible — es el papel del "regulador de balance" de todo el
  enlace o red DC.
- **Modo esclavo de \(P\).** El terminal recibe una consigna de potencia activa \(P^*\) fija (por ejemplo,
  la potencia que un parque eólico offshore quiere evacuar) y la convierte directamente en referencia de
  corriente despejando de la fórmula de potencia activa:

$$ P^* = \frac{3}{2}v_d\,i_d^* \quad\Longrightarrow\quad i_d^* = \frac{2P^*}{3v_d} $$

  Este terminal no participa en absoluto en la regulación de \(V_{dc}\): inyecta o absorbe exactamente la
  potencia que se le pide, pase lo que pase con la tensión del bus.

**Por qué tiene que haber exactamente un maestro de \(V_{dc}\) (o un droop, apartado 6).** En un enlace
punto a punto, el balance de potencia del apartado 4 (\(\dot W_{total}=P_{AC1}+P_{AC2}-\text{pérdidas}\))
exige que, si un terminal fija \(P\) de forma rígida, el **otro** tiene que absorber cualquier diferencia
para que la energía total del sistema no derive sin control — ese es exactamente el papel del modo
maestro. Si **ambos** terminales intentasen operar en modo esclavo de \(P\) simultáneamente con consignas
que no casen exactamente (lo habitual, porque las pérdidas nunca son cero y las consignas se fijan por
separado), no habría ningún elemento absorbiendo el desajuste: la energía del bus DC (y por tanto
\(V_{dc}\)) derivaría sin límite hasta disparar las protecciones de sobretensión o colapsar por
infratensión. Por la misma razón, tampoco puede haber dos maestros de \(V_{dc}\) simultáneos con la misma
referencia: ambos PI competirían por fijar la misma variable con ganancias independientes, lo que en
general es inestable o, en el mejor caso, indeterminado (ninguno de los dos "sabe" cuánta corriente le
corresponde aportar). En redes con más de dos terminales (MTDC), esta rigidez del maestro único se
sustituye por el droop de tensión DC del apartado 6, que reparte la función de "sostener \(V_{dc}\)" entre
varios terminales a la vez sin que ninguno la asuma en solitario.

**La planta real del maestro: no un bus aislado, sino el cable acoplando los dos terminales.** Antes de la
derivación, así es esa planta (el modelo π de dos terminales que ya aparece en el apartado 7, aquí dibujado
como circuito para que sirva de referencia visual a lo que sigue):

<div class="cfig"><img src="figuras/hvdc-planta-maestro.png" alt="circuito del modelo pi de dos terminales, con las capacidades shunt C medio en cada extremo, la rama serie R y L en el medio recorrida por Idc, y las fuentes de corriente IVSC1 e IVSC2 inyectando en cada nodo Vdc1 y Vdc2"><div class="cap">Planta real del lazo maestro: el modelo π de dos terminales del apartado 7, mostrado antes de resolverlo — las dos fuentes de corriente \(I_{VSC1}\), \(I_{VSC2}\) son las variables manipuladas de los dos terminales; \(V_{dc1}\), \(V_{dc2}\) son las tensiones que cada uno controla o deja flotar.</div></div>

El apartado 4 diseñó el PI del maestro tratando \(P_{line}\) como una perturbación de potencia sobre su propio
condensador \(C_1\). Eso es correcto y suficiente para elegir el ancho de banda por el método de
[[control-tension-bus-dc]] §2, pero deja una pregunta sin responder: ¿qué tan rápido puede ir realmente ese
lazo antes de excitar la dinámica propia del cable? Para responderla hace falta la planta completa
\(V_{dc1}(s)/I_{VSC1}(s)\), no la aproximación de bus aislado — y esa planta ya está en este mismo
repositorio: es el sistema de tres estados del apartado 7 (\(\mathbf{x}=[V_{dc1},I_{dc},V_{dc2}]^T\),
matrices \(A\), \(B\) ya dadas). Resolviendo \((sI-A)\mathbf{X}=B\mathbf{U}\) para \(V_{dc1}(s)\) en
función de las dos corrientes de convertidor:

$$ V_{dc1}(s) = \frac{2I_{VSC1}(s)\big(CLs^2+CRs+2\big) - 4I_{VSC2}(s)}{Cs\big(CLs^2+CRs+4\big)} $$

de donde se separan la planta propia del maestro y el acoplo desde el otro terminal:

$$ G_{master}(s)\equiv\frac{V_{dc1}(s)}{I_{VSC1}(s)}\bigg|_{I_{VSC2}=0} = \frac{2(CLs^2+CRs+2)}{Cs(CLs^2+CRs+4)},
   \qquad G_{dist}(s)\equiv\frac{V_{dc1}(s)}{I_{VSC2}(s)}\bigg|_{I_{VSC1}=0} = \frac{-4}{Cs(CLs^2+CRs+4)} $$

\(G_{master}\) tiene un polo en \(s=0\) (el modo integrador de energía total, el mismo del apartado 4) más
el par de polos complejos del denominador cuadrático \(CLs^2+CRs+4\) — la resonancia del cable, ahora
vista **desde dentro** de la planta que el PI del maestro realmente controla, no como un fenómeno aparte.

**La resonancia exacta es el doble de la estimación del apartado 7 — y por qué.** El polinomio
característico completo del sistema de tres estados es \(s(CLs^2+CRs+4)/(CL)\): el término resonante es
\(s^2+(R/L)s+4/(LC)=0\), no \(s^2+(R/L)s+1/(LC)=0\). Eso da:

$$ \boxed{\ \omega_{n,exact}=\frac{2}{\sqrt{LC}} = 2\,\omega_{n,simple}\ } \qquad\text{con}\qquad
   \omega_{n,simple}=\frac{1}{\sqrt{LC}} $$

exactamente **el doble** de la fórmula aproximada \(f_{res}=1/(2\pi\sqrt{L_{total}C_{cable}})\) del
apartado 7 — no una corrección de segundo orden, un factor 2 limpio, verificado tanto simbólicamente como
con los autovalores numéricos de la matriz \(A\). Físicamente, la razón es la partición \(C/2\)–\(C/2\) del
modelo π: para el modo *diferencial* (el que oscila, distinto del modo común de carga total que da el polo
en \(s=0\)), los dos condensadores de extremo no cargan en paralelo — cargan **en serie** desde el punto de
vista de la oscilación, porque es la diferencia \(V_{dc1}-V_{dc2}\) la que impulsa la corriente resonante a
través de \(L\). Dos capacidades \(C/2\) en serie dan \(C_{eff}=C/4\), y

$$ \omega_n=\frac{1}{\sqrt{L\,C_{eff}}}=\frac{1}{\sqrt{L\,C/4}}=\frac{2}{\sqrt{LC}} $$

que reproduce exactamente el resultado de los autovalores. Con los valores reales del ejemplo del apartado
10 (\(L=120\,\text{mH}\), \(R=3.22\,\Omega\), \(C=60\,\mu\text{F}\)): autovalores exactos
\(-13.42\pm j745.2\) y \(0\), es decir \(\omega_{n,exact}\approx745\,\text{rad/s}\) (\(118.6\,\text{Hz}\),
el **doble** del \(\approx59\,\text{Hz}\) del apartado 7) con amortiguamiento \(\zeta\approx0.018\) —
extremadamente bajo, un factor de calidad \(Q\approx28\): esta resonancia, si se excita, apenas se amortigua
por sí sola. Esto no contradice el apartado 7 (que ya la presenta como aproximación, "\(\approx\)"): lo que
aporta este apartado es el valor exacto que hace falta para fijar con margen real el ancho de banda del
lazo maestro, y de paso corrige a la baja los modos SSO citados allí y en el apartado 10
(\(50\pm118.6\,\text{Hz}\to\) subsíncrono en realidad más cercano a \(50\,\text{Hz}\) reflejado con menor
separación de lo que sugiere la cifra aproximada de 59 Hz — el efecto físico es el mismo, solo cambia la
cifra concreta).

**Qué capacidad "ve" realmente el maestro a baja frecuencia.** Tomando el límite \(s\to0\) de
\(s\,G_{master}(s)\) (el residuo del polo integrador) se obtiene \(1/C\) — **la capacidad total del cable**,
no la mitad local del maestro. Esto explica, a posteriori, por qué la simulación del apartado 4 usó
\(C=60\,\mu\text{F}\) (el \(C_{total}\) del cable de 300 km, apartado 10) en vez de un valor arbitrario de
condensador local: a frecuencias muy por debajo de la resonancia (que es exactamente el régimen en el que
debe operar el lazo maestro, ver el criterio siguiente), el maestro efectivamente "ve" su propio condensador
y el del otro extremo fundidos en uno solo a través del cable — la planta simplificada de bus único del
apartado 4 y la planta exacta de tres estados de este apartado **coinciden** en ese límite, con la misma
\(C\). El acoplo \(G_{dist}(s)\) tiene el mismo residuo en magnitud (\(-1/C\)): una inyección sostenida de
corriente en cualquiera de los dos extremos termina repartiéndose por igual entre ambos condensadores, tal
como exige la conservación de carga del modo común.

**El lazo maestro no solo debe evitar la resonancia — puede amortiguarla activamente.** La primera
intuición (por analogía con la separación ×10 genérica de [[convertidor-back-to-back]] §3) sería exigir
\(\omega_{master}\ll\omega_{n,exact}\) sin más. Pero eso trata la resonancia como algo que solo hay que
"esquivar", y el análisis riguroso de pequeña señal dice algo más interesante: **el propio lazo maestro,
bien ajustado, amortigua activamente el modo resonante del cable**, en vez de limitarse a no excitarlo.
Linealizando el PI del maestro alrededor del punto de operación (\(\Delta W\approx C V_{dc,0}\Delta V_{dc1}\),
así que \(\Delta I_{VSC1}(s)=-C(K_{p,W}+K_{i,W}/s)\,\Delta V_{dc1}(s)\), con \(V_{dc,0}\) cancelándose
exactamente) y cerrando el lazo sobre \(G_{master}(s)\), la ecuación característica es

$$ 1 + C\left(K_{p,W}+\frac{K_{i,W}}{s}\right)G_{master}(s) = 0 \quad\Longrightarrow\quad
   CLs^4+(CR+4\omega_nCL)s^3+(4+4\omega_nCR+2\omega_n^2CL)s^2+(8\omega_n+2\omega_n^2CR)s+4\omega_n^2=0 $$

(con \(K_{p,W}=2\omega_n\), \(K_{i,W}=\omega_n^2\); polinomio verificado simbólicamente). De sus cuatro
raíces, un par complejo conjugado es la continuación, **en lazo cerrado**, del modo resonante del cable.
Barriendo \(\omega_n\) y siguiendo ese par: el amortiguamiento \(\zeta\) que el lazo le da a la resonancia
**no es monótono en \(\omega_n\)** — sube desde el valor en lazo abierto (\(\zeta_{ol}\approx0.018\)), pasa
por un máximo, y vuelve a bajar para \(\omega_n\) muy grande (el lazo, si es demasiado rápido, deja de
"ver" el modo resonante como algo que pueda corregir y el par de polos regresa hacia su posición de lazo
abierto). Para los números de este cable, el máximo está en \(\omega_n\approx261\,\text{rad/s}\) con
\(\zeta_{max}\approx0.30\) — **diecisiete veces más amortiguado que en lazo abierto**. Con
\(\omega_{master}=100\,\text{rad/s}\) (el valor ya usado, sin justificar, en la figura del apartado 4) el
par resonante en lazo cerrado tiene \(\zeta\approx0.15\): lejos del óptimo pero, aun así, muchísimo mejor
que el cable desnudo. El único límite que sigue siendo un límite estricto es el de validez del propio
modelo: por encima de \(\omega_{ci}/10\approx628\,\text{rad/s}\) deja de ser razonable tratar el lazo de
corriente (interno) como instantáneo frente al lazo maestro, la hipótesis usada para linealizar arriba.

<div class="cfig"><img src="figuras/hvdc-diseno-ancho-banda.png" alt="grafica del amortiguamiento zeta del modo resonante en lazo cerrado frente al ancho de banda omega n del PI maestro, mostrando un maximo no monotono en 261 rad por segundo con zeta 0.30 frente al zeta 0.018 en lazo abierto, con el valor omega n igual a 100 usado marcado en zeta 0.15; y lugar de las raices del par de polos resonante en el plano s al barrer omega n, mostrando la trayectoria desde el polo en lazo abierto hasta el limite cuando omega n tiende a infinito, pasando por el punto de amortiguamiento maximo"><div class="cap">(a) Amortiguamiento \(\zeta\) del modo resonante del cable, en lazo cerrado, frente al ancho de banda \(\omega_n\) del PI maestro: no es monótono, tiene un máximo (\(\omega_n\approx261\,\text{rad/s}\), \(\zeta_{max}\approx0.30\)) muy por encima del \(\zeta_{ol}\approx0.018\) en lazo abierto. El valor ya usado en la figura del apartado 4 (\(\omega_n{=}100\)) da \(\zeta\approx0.15\). (b) Lugar de las raíces del par de polos resonante al barrer \(\omega_n\): desde el polo en lazo abierto (\(\omega_n\to0\)) hasta el límite \(\omega_n\to\infty\), pasando por el punto de máximo amortiguamiento.</div></div>

**Ejemplo coordinado: ambos terminales a la vez, con los números anteriores.** Retomando la simulación ya
presentada en el apartado 4 (terminal 1 maestro, terminal 2 esclavo), pero ahora con el modelo **exacto**
de tres estados en vez del integrador simplificado: el terminal 2 (esclavo) recibe \(P_2^*=-400\,
\text{MW}\) en \(t=8\,\text{ms}\); su lazo de corriente (\(K_p=307.2\), \(T_i=0.0955\,\text{s}\)) sigue la
referencia \(i_d^*=2P_2^*/(3v_d)\) en \(\approx0.8\,\text{ms}\) — mucho más rápido que cualquier dinámica
del cable, así que desde el punto de vista del terminal 1 el escalón de \(P_2\) es, en la práctica,
instantáneo. El terminal 1 (maestro), con el PI externo sobre \(W=\tfrac12CV_{dc}^2\) y
\(\omega_{master}=100\,\text{rad/s}\), absorbe la diferencia de potencia: \(V_{dc1}\) muestra un
sobreimpulso inicial y **una oscilación visible a \(\approx745\,\text{rad/s}\)** — el modo resonante del
cable, inevitablemente excitado por un escalón de potencia tan brusco — pero esa oscilación decae en
\(\sim15\)–\(20\,\text{ms}\), coherente con el \(\zeta\approx0.15\) de lazo cerrado calculado arriba, no con
el \(\zeta\approx0.018\) de un cable sin control (que apenas decaería en ese tiempo). \(V_{dc2}\) muestra la
misma oscilación, desfasada, y \(I_{dc}\) (que es, físicamente, la variable que más directamente "ve" la
resonancia LC) la muestra con la mayor amplitud relativa de las tres. Esta es la lectura correcta y
completa del diseño: el ancho de banda del maestro no hace desaparecer la física del cable —eso no está en
su mano, la excita cualquier escalón suficientemente brusco— pero si se elige en la región de amortiguamiento
activo (arriba), el propio lazo la atenúa con bastante más eficacia que dejar el cable sin regular.

<div class="cfig"><img src="figuras/hvdc-lazo-maestro-respuesta.png" alt="diagrama de bloques del sistema de control coordinado con el terminal maestro en lazo cerrado sobre la planta del cable de tres estados y el terminal esclavo en lazo abierto, y respuesta temporal simulada con el modelo exacto mostrando Vdc1, Vdc2 e Idc ante el escalon de potencia con el modo resonante visible pero amortiguado"><div class="cap">(a) Sistema de control coordinado de los dos terminales sobre la planta compartida (\(G_{master}(s)\), \(G_{dist}(s)\)): el maestro cierra el lazo sobre \(V_{dc1}\); el esclavo inyecta \(I_{VSC2}\) en lazo abierto, sin realimentar \(V_{dc2}\). (b) Respuesta simulada con el modelo exacto de tres estados ante el mismo escalón de \(P_2\) de la figura del apartado 4: el modo resonante del cable es visible en \(V_{dc1}\), \(V_{dc2}\) e \(I_{dc}\), pero amortiguado por el lazo maestro (\(\zeta\approx0.15\)) en vez de persistir como en lazo abierto.</div></div>

**El lazo de \(Q\) / tensión AC.** En paralelo y de forma independiente al lazo de \(V_{dc}\)/\(P\), cada
terminal tiene un lazo sobre el eje q que genera \(i_q^*\) a partir de una consigna de potencia reactiva
\(Q^*\) o de tensión AC \(V_{ac}^*\) en el punto de conexión (control de tensión, útil cuando el terminal
alimenta una red débil o aislada — parques offshore sin generación síncrona propia, apartado 1). Como
\(Q\) depende solo de \(i_q\) (verificado arriba), este lazo es completamente independiente del lazo de
\(P\)/\(V_{dc}\): se pueden sintonizar y operar sin interferencia mutua, la ventaja de control que el LCC
no tiene (apartado 12).

## 6 — Topología punto a punto vs MTDC, y el droop de tensión DC

**Punto a punto.** Dos terminales VSC conectados por un cable DC. Es la topología más sencilla: un
terminal controla \( V_{dc} \) (el regulador del balance de energía del cable) y el otro controla \( P \)
(inyecta o absorbe la potencia deseada). El control es centralizado y sencillo.

**MTDC (Multi-Terminal DC).** Tres o más terminales VSC conectados en la misma red DC. Los proyectos
actuales más relevantes son las redes offshore para integrar múltiples parques eólicos y entregarlos a
múltiples puntos de la red onshore (apartado 11, North Sea Wind Power Hub). Ventajas respecto a múltiples
enlaces punto a punto: redundancia (si un enlace falla, la potencia se redistribuye), menor coste
marginal por terminal (el cable ya existe), posibilidad de optimización del flujo de potencia en la red
DC.

**Topologías de red DC.** **Radial (árbol):** cada nodo conectado por un único camino al resto; simple y
barata, pero sin redundancia — un fallo de cable aísla la rama completa. **Mallada:** múltiples caminos
entre cualquier par de nodos; mayor redundancia y flexibilidad de despacho, a costa de mayor complejidad
de protección (la corriente de falta puede circular por varios caminos) y de necesitar un DCCB en cada
extremo de cada línea (apartado 9).

**El problema del control centralizado de \(V_{dc}\).** Si un único terminal controla \(V_{dc}\) (modo
*slack*), actúa como referencia absoluta para toda la red. Si ese terminal falla, el bus DC pierde su
referencia de tensión y colapsa en décimas de segundo. En un sistema con \(N\geq3\) terminales este
diseño no es admisible — hace falta que varios terminales compartan la regulación.

**Droop de tensión DC — derivación desde el balance de potencia del sistema.** Cada terminal \(i\)
implementa una característica P-V:

$$ P_i = P_{0,i} + k_{d,i}(V_{dc}-V_{dc,0}) $$

donde \(P_i\) es la potencia que el terminal **inyecta** al bus DC (positiva si genera, negativa si
consume — un terminal de carga onshore es simplemente un \(P_i<0\)), \(P_{0,i}\) la consigna nominal,
\(V_{dc,0}\) la tensión de referencia (igual para todos) y \(k_{d,i}\) [MW/kV] el coeficiente de droop —
equivalente a una **conductancia virtual** entre el bus DC y el punto de consigna de potencia. La red DC
en régimen cuasi-estacionario no almacena potencia neta, así que en todo instante la suma de lo inyectado
por los \(N\) terminales es cero (despreciando pérdidas del cable):

$$ \sum_{i=1}^{N} P_i = 0 $$

Antes de una perturbación, el sistema está en equilibrio con \(V_{dc}=V_{dc,0}\), cada terminal en
\(P_i=P_{0,i}\) y \(\sum_i P_{0,i}=0\). Ocurre ahora una perturbación de carga: el terminal de carga
demanda \(\Delta P_{carga}\) MW **más** que antes, es decir su inyección baja en esa cantidad
(\(P_{0,k}\to P_{0,k}-\Delta P_{carga}\)). El nuevo balance, con cada terminal siguiendo su recta de
droop, debe seguir sumando cero:

$$ \sum_{i=1}^{N}\Big[P_{0,i}+k_{d,i}(V_{dc}-V_{dc,0})\Big] - \Delta P_{carga} = 0 $$

Restando la condición de equilibrio inicial (\(\sum_i P_{0,i}=0\)) y usando \(\Delta V_{dc}\equiv
V_{dc}-V_{dc,0}\):

$$ \Delta V_{dc}\sum_i k_{d,i} - \Delta P_{carga} = 0 \quad\Longrightarrow\quad \boxed{\ \Delta V_{dc} = \frac{\Delta P_{carga}}{\sum_i k_{d,i}}\ } $$

y como cada terminal se mueve sobre su propia recta con la misma \(\Delta V_{dc}\) (común a todo el bus):

$$ \Delta P_i = k_{d,i}\,\Delta V_{dc} = \frac{k_{d,i}}{\sum_j k_{d,j}}\,\Delta P_{carga} $$

Con \(\Delta P_{carga}>0\) definido como demanda **adicional**, la fórmula da \(\Delta V_{dc}>0\): esto
parece contradecir la intuición de que "más demanda hunde la tensión", pero es solo el signo del
convenio (\(P_i\) inyectada, \(\Delta P_{carga}\) restado a la inyección del terminal de carga). Si en
cambio se define \(\Delta P_{carga}\) directamente como el incremento neto que hay que **cubrir** entre
los generadores (el signo habitual en la literatura), la relación se escribe
\(\Delta V_{dc}=-\Delta P_{carga}/\sum_i k_{d,i}\) — el resultado físico es idéntico en ambos casos (la
tensión cae cuando sube la demanda neta). Lo que **no** depende del convenio es la conclusión central:
cada terminal absorbe una fracción \(k_{d,i}/\sum_j k_{d,j}\) de la perturbación total, **exactamente
proporcional a su propio droop**, sin que ningún terminal necesite conocer la ganancia de los demás en
tiempo real.

<div class="cfig"><img src="figuras/mtdc-droop-derivacion.png" alt="rectas de potencia frente a tension de tres terminales MTDC con distinto coeficiente de droop, mostrando el punto de operacion inicial y el punto tras una perturbacion de carga con el desplazamiento de tension marcado; y grafico de barras del reparto de la perturbacion entre los tres terminales, proporcional al coeficiente de droop de cada uno"><div class="cap">(a) Rectas \(P_i(V_{dc})\) de tres terminales con distinto \(k_{d,i}\): el punto de operación inicial (círculos, \(\sum P_i=0\)) se desplaza tras una perturbación de carga \(\Delta P_{carga}=50\) MW en el terminal onshore hasta un nuevo punto (cuadrados) en \(V_{dc,0}+\Delta V_{dc}\), el mismo para los tres terminales. (b) El reparto de la perturbación entre terminales es exactamente proporcional a \(k_{d,i}\): el terminal con droop doble absorbe el doble de variación de potencia.</div></div>

El terminal con mayor \(k_d\) absorbe más variación de potencia — por la misma lógica de un divisor de
corriente, una conductancia virtual mayor conectada al mismo nudo de tensión común se lleva una fracción
mayor del total. Si \(k_d\to\infty\) para un terminal, su fracción tiende a 1 y \(\Delta V_{dc}\to0\):
actúa como el *slack* clásico (control de tensión puro, sin caída, absorbiendo toda la perturbación).

**Comunicación requerida.** El droop primario no necesita comunicación: cada terminal mide localmente
\(V_{dc}\) y ajusta su potencia según su propia característica. El control secundario (restauración de
\(V_{dc}\) al valor nominal tras la perturbación, que el droop por sí solo no hace — deja un error
permanente \(\Delta V_{dc}\neq0\)) sí puede requerir comunicación entre terminales para calcular la
corrección global.

**Consideración de diseño.** Un droop grande \(k_d\) hace que el terminal sea un buen regulador de
tensión (variación pequeña de \(V_{dc}\) ante perturbaciones) pero puede provocar cambios bruscos de
potencia. Un droop pequeño limita la variación de potencia pero deja \(V_{dc}\) oscilar más. El diseño
equilibra ambos requisitos según la rigidez requerida del bus DC.

## 7 — El cable DC: características y modelo π

**Diferencias con el cable AC.** En corriente continua la inductancia no tiene efecto reactivo
(\(\omega=0\)), por lo que la impedancia en régimen permanente es puramente resistiva. Esto elimina la
limitación de Ferranti y el problema de la potencia reactiva de carga que condena a los cables AC a
longitudes máximas de ~80–100 km. La capacidad del cable, en cambio, es incluso más importante en DC que
en AC: almacena energía \(W=\tfrac12 C_{cable}V_{dc}^2\) que actúa como reserva de energía y determina la
dinámica de la tensión DC durante los transitorios de control y las faltas (apartado 8).

| Parámetro | Cable AC 132 kV | Cable DC ±320 kV HVDC |
|---|---|---|
| Resistencia \( R \) | 0.05 Ω/km | 0.012 Ω/km (conductor mayor) |
| Inductancia \( L \) | 0.4 mH/km | 0.4 mH/km (irrelevante en DC) |
| Capacidad \( C \) | 0.2 µF/km | 0.15–0.25 µF/km |
| Longitud máxima operativa | ~80 km | ilimitada (prácticamente) |
| Pérdidas/100 km | > 1 % (reactiva) | ~0.3 % (solo Joule) |

La inductancia \(L\) sí importa en el análisis dinámico de transitorios y faltas DC — forma con la
capacidad el circuito resonante que determina la velocidad de crecimiento de la corriente de falta
(apartado 8).

**Modelo π concentrado.** Para el diseño de controladores (frecuencias < 100 Hz) y el análisis de
estabilidad de lazo, el modelo π con parámetros totales concentrados es suficiente: la resistencia e
inductancia en la rama serie central, y la capacidad total repartida en dos shunts de \(C/2\) en los
extremos:

$$\frac{dI_{dc}}{dt} = \frac{V_{dc1} - V_{dc2} - R\cdot I_{dc}}{L_{cable}}, \qquad \frac{dV_{dc1}}{dt} = \frac{I_{VSC1} - I_{dc}}{C/2}, \qquad \frac{dV_{dc2}}{dt} = \frac{I_{dc} - I_{VSC2}}{C/2}$$

La constante de tiempo del cable en bucle abierto es \(\tau_{dc}=R_{total}C_{total}=R_{km}C_{km}\ell^2\):
la dependencia **cuadrática** con la longitud \(\ell\) es la razón por la que cables muy largos tienen
dinámicas lentas. Para \(R_{km}=0.012\,\Omega\text{/km}\), \(C_{km}=0.2\,\mu\text{F/km}\),
\(\ell=300\,\text{km}\): \(\tau_{dc}=0.012\times0.2\times10^{-3}\times300^2=216\,\text{ms}\) — este valor
limita el ancho de banda del lazo de control de \(V_{dc}\): no se puede hacer el controlador más rápido
que \(\sim1/\tau_{dc}\) sin excitar la resonancia LC.

El sistema de tres variables de estado \(\mathbf{x}=[V_{dc1},\,I_{dc},\,V_{dc2}]^T\):

$$\dot{\mathbf{x}} = \begin{pmatrix} 0 & -\tfrac{2}{C} & 0 \\ \tfrac{1}{L} & -\tfrac{R}{L} & -\tfrac{1}{L} \\ 0 & \tfrac{2}{C} & 0 \end{pmatrix}\mathbf{x} + \begin{pmatrix} \tfrac{2}{C} & 0 \\ 0 & 0 \\ 0 & -\tfrac{2}{C} \end{pmatrix}\begin{pmatrix}I_{VSC1}\\I_{VSC2}\end{pmatrix}$$

Los eigenvalores de la matriz de estado determinan la dinámica natural del cable: un modo lento real (la
constante \(\tau_{RC}\)) y un par de modos complejos conjugados (la resonancia LC, apartado siguiente).

**Resonancia LC del sistema HVDC.** La inductancia efectiva incluye la del cable y las de brazo de los
dos MMC (en serie desde el punto de vista del bus DC): \(L_{total}=L_{cable}+\tfrac43 L_{arm}\). La
frecuencia de resonancia del circuito LC formado por \(L_{total}\) y \(C_{cable}\):
\(f_{res}=1/(2\pi\sqrt{L_{total}C_{cable}})\). Para \(L_{total}=120\,\text{mH}\),
\(C_{cable}=60\,\mu\text{F}\): \(f_{res}\approx59\,\text{Hz}\) — esta es la resonancia de un único LC
equivalente; el valor **exacto**, obtenido de los autovalores del sistema de tres estados de más abajo, es
el doble (\(\approx119\,\text{Hz}\)), derivado en el apartado 5 donde es lo que fija el margen de diseño
del lazo maestro de \(V_{dc}\). Esta frecuencia cae dentro del ancho de
banda del lazo de corriente del MMC (~1 kHz) y cerca del de \(V_{dc}\) (~10–50 Hz): si el control excita
la resonancia (escalón brusco de referencia, ganancia excesiva), el sistema oscila a \(f_{res}\). En el
dominio AC, esa resonancia DC aparece como modos a \(f_{red}\pm f_{res}\): para \(f_{red}=50\,\text{Hz}\)
y \(f_{res}=59\,\text{Hz}\), \(f_{sub}=9\,\text{Hz}\) (subsíncrono) y \(f_{super}=109\,\text{Hz}\)
(supersíncrono) — los **SSO** (Sub-Synchronous Oscillations) que han causado disparos en sistemas HVDC
reales (ver [[fenomenos-oscilatorios-red]]).

**Validez del modelo π y modelo de línea distribuida.** El modelo π concentrado es válido cuando la
longitud eléctrica del cable es mucho menor que la longitud de onda a la frecuencia de análisis; en DC
puro (0 Hz) siempre es válido, y para transitorios de control (< 100 Hz) la longitud de onda es
\(\lambda\approx1600\,\text{km}\) — para un cable de 300 km, \(\ell/\lambda\approx0.19\), error < 5 %. Para
transitorios de falta (< 1 ms, > 1 kHz) hace falta el modelo de línea distribuida (ecuaciones del
telegrafista, \(\partial V/\partial x=-R'I-L'\partial I/\partial t\), \(\partial I/\partial x=-G'V-C'
\partial V/\partial t\)), cuya velocidad de propagación es \(v_{prop}=1/\sqrt{L'C'}\approx1.5\text{–}
1.7\times10^8\,\text{m/s}\) (aprox. mitad de la luz, por la permitividad del XLPE \(\varepsilon_r
\approx2.3\)) y cuya impedancia característica es \(Z_c\approx\sqrt{L'/C'}\), la misma \(Z_c\) que aparece
en la corriente de falta del apartado 8. En la práctica se discretiza el cable en \(n\) secciones π en
cascada (\(n\approx10\) para 300 km da error < 5 % hasta 5 kHz; \(n\geq50\) para coordinación de
protecciones a < 1 ms).

**XLPE vs papel impregnado.** El aislamiento del cable ha evolucionado del papel impregnado en aceite
(MIND) al XLPE (polietileno entrecruzado). El **XLPE** opera a mayor temperatura (90 °C vs 55–60 °C), sin
aceite ni riesgo de fugas, más ligero — pero en DC sufre acumulación de cargas espaciales (la
conductividad del polímero sube con la temperatura, distorsionando el reparto de campo eléctrico), lo que
históricamente limitó su tensión a ±200–250 kV; los compuestos "DC-grade" modernos han elevado el límite a
±320 kV (DolWin, BorWin) y ya ±525 kV (NordLink, 2021). El **MIND** no tiene ese problema de cargas
espaciales y llega a mayor tensión (±500–600 kV) pero es más pesado, rígido y limitado a menor
temperatura — más difícil de instalar offshore.

## 8 — Falta DC: dinámica, detección y protección

**Planteamiento: el cable en falta es un RLC serie en descarga.** Una falta bipolar (cortocircuito entre
los dos polos) pone en cortocircuito el extremo del cable. En el instante \(t=0^+\), el condensador
\(C_{cable}\) tiene su tensión previa \(v_C(0)=V_{dc}\) y la corriente por la inductancia se aproxima a
\(i(0)\approx0\) (mucho menor que la corriente de falta que va a aparecer). El circuito que queda —
condensador cargado, descargándose a través de \(R_{total}\) y \(L_{total}\) hacia el cortocircuito— es
exactamente un **RLC serie en descarga libre**:

$$ L\frac{di}{dt} + Ri + \frac{1}{C}\int i\,dt = 0 $$

<div class="cfig"><img src="figuras/hvdc-cable-falta-rlc.png" alt="esquema del circuito RLC serie equivalente en el instante de la falta bipolar, con el condensador cargado a Vdc y la bobina con corriente inicial nula, y grafica comparando la solucion exacta de la corriente de falta con amortiguamiento frente a la aproximacion de amortiguamiento nulo Vdc entre Zc, mostrando que esta ultima es una cota superior y no el pico real"><div class="cap">(a) Circuito equivalente en el instante de la falta: el condensador del cable, cargado a \(V_{dc}\), se descarga a través de \(R\) y \(L\) hacia el cortocircuito bipolar — un RLC serie con condiciones iniciales \(v_C(0)=V_{dc}\), \(i(0)=0\). (b) La solución exacta (roja) incluye el decaimiento exponencial desde el primer instante; la aproximación habitual \(V_{dc}/Z_c\) (azul, línea de puntos) es una cota superior que solo se alcanzaría con amortiguamiento nulo — el pico real es un \(5\,\%\) menor y ocurre ligeramente antes.</div></div>

**Derivación paso a paso.** Derivando una vez para eliminar la integral: \(L\,d^2i/dt^2+R\,di/dt+i/C=0\).
Ecuación característica \(Ls^2+Rs+1/C=0\), con raíces

$$ s_{1,2} = -\frac{R}{2L} \pm \sqrt{\left(\frac{R}{2L}\right)^2 - \frac{1}{LC}} \equiv -\sigma \pm j\omega_d $$

Para un cable HVDC (\(R\) pequeña, caso **subamortiguado**), \(\sigma\equiv R/(2L)\) y
\(\omega_d=\sqrt{1/(LC)-\sigma^2}=\sqrt{\omega_n^2-\sigma^2}\) con \(\omega_n=1/\sqrt{LC}\) la frecuencia
natural (la misma \(f_{res}\) del apartado 7). La solución general es
\(i(t)=e^{-\sigma t}(A\cos\omega_d t+B\sin\omega_d t)\). De \(i(0)=0\) sale \(A=0\); derivando y usando
\(L\,di/dt(0)=v_C(0)-Ri(0)=V_{dc}\) (toda la tensión inicial cae en la bobina, sin caída aún en \(R\)) se
despeja \(B=V_{dc}/(L\omega_d)\):

$$ \boxed{\ i_{fault}(t) = \frac{V_{dc}}{L\,\omega_d}\,e^{-\sigma t}\sin(\omega_d t)\ } \qquad \sigma=\frac{R}{2L},\quad \omega_d=\sqrt{\frac{1}{LC}-\sigma^2} $$

Esta es la solución exacta — cada constante sale de una condición inicial física real del circuito, no de
una fórmula supuesta.

**La aproximación habitual \(V_{dc}/Z_c\) es una cota, no el pico real.** Con amortiguamiento pequeño
(\(\sigma\ll\omega_n\), el caso típico de un cable HVDC), aproximando \(\omega_d\approx\omega_n\) y
despreciando el decaimiento durante el primer cuarto de ciclo: \(i_{fault}(t)\approx(V_{dc}/L\omega_n)
\sin(\omega_n t)=(V_{dc}/Z_c)\sin(\omega_n t)\), con \(Z_c\equiv\sqrt{L/C}\) (usando
\(L\omega_n=\sqrt{L/C}\)). El pico de esta aproximación es exactamente \(V_{dc}/Z_c\) en
\(\omega_n t=\pi/2\) — pero es una **cota superior**: la solución exacta decae desde \(t=0\), así que su
máximo real es menor y ocurre un poco antes del cuarto de ciclo. Para el ejemplo (\(R_{total}=3.22\,
\Omega\), \(L_{total}=120\,\text{mH}\), \(C_{total}=60\,\mu\text{F}\), \(\zeta=\sigma/\omega_n\approx
0.036\)): \(Z_c=44.7\,\Omega\Rightarrow V_{dc}/Z_c\approx14.31\,\text{kA}\) (cota), frente al pico real
\(I_{fault,pico}\approx13.54\,\text{kA}\) (verificado numéricamente) — una diferencia de \(\sim5\,\%\),
pequeña porque \(\zeta\) es pequeño, pero no nula. Para diseño conservador la cota es aceptable
(sobreestima el peor caso); para el instante y valor exacto del pico hay que usar la solución exacta.

**Fases del transitorio de falta.** (1) *Descarga de condensadores*: los condensadores del MMC y del
cable se descargan hacia el punto de falta, con la dinámica RLC de arriba; la corriente crece a razón
inicial \(di/dt|_{t=0}=V_{dc}/L_{total}\) — para \(V_{dc}=640\,\text{kV}\), \(L_{total}=120\,\text{mH}\),
\(di/dt\approx5.3\,\text{MA/s}\), superando 5 kA en 1 ms. (2) *Alimentación desde la red AC*: una vez
descargados los condensadores, la corriente sigue siendo alimentada desde la red AC a través de los
diodos de rueda libre del MMC-HB — esta componente **no** se puede bloquear sin submódulos full-bridge.
(3) *Pico*: la corriente puede alcanzar 10–20 pu en menos de 10 ms; los IGBTs toleran sobreintensidades de
2–3 pu durante máximo 10 µs antes de fallar por sobretemperatura o *latch-up*.

**Limitaciones de los MMC-HB.** Los IGBTs de los submódulos half-bridge no pueden bloquear una falta DC:
aunque se apaguen las compuertas, los diodos de antiparalelo conducen la corriente desde la red AC hacia
el punto de falta — el sistema funciona como un rectificador no controlado hasta que se abre el disyuntor
AC del terminal.

**Por qué la protección AC no basta.** Los disyuntores AC convencionales interrumpen en el cruce por
cero (cada 10 ms a 50 Hz). Para aislar una falta DC, el disyuntor AC debe esperar el cruce por cero — hasta
10 ms adicionales, demasiado para los IGBTs — y mientras tanto la corriente de falta sigue fluyendo desde
la red AC.

**Detección de la falta.** Los relés de distancia DC detectan la falta en 1–2 ms midiendo la derivada de
\(V_{dc}\) e \(I_{dc}\) (protección basada en ondas viajeras, apartado 7). El criterio de disparo
compara la velocidad de crecimiento de la corriente con un umbral:

$$ \text{Falta detectada si:}\quad \frac{di_{DC}}{dt} > \text{umbral} \approx 0.5\,\text{kA/ms} $$

Este umbral puede ser superado por transitorios de control normales — la discriminación debe completarse
en < 2 ms para que la protección actúe antes de que la corriente destruya los IGBTs. El tiempo total de
eliminación (detección + apertura) debe ser < 5 ms.

**DCCB (DC Circuit Breaker).** En AC la corriente cruza por cero dos veces por periodo, facilitando la
interrupción; en DC no hay cruce por cero, así que el interruptor debe crear activamente las condiciones
para extinguir la corriente.

| Tecnología | Tiempo apertura | Pérdidas nominales | Coste relativo |
|---|---|---|---|
| Mecánico (vacío) | 30–100 ms | Mínimas | Bajo |
| Híbrido (semiconductor + mecánico) | 2–5 ms | Muy bajas | Alto |
| Totalmente semiconductor | < 1 ms | Altas (~0.1–0.2 % de la potencia) | Muy alto |

**DCCB híbrido (solución estándar actual, ABB 2012).** Camino de conducción nominal mecánico (pérdidas
mínimas). Al detectar la falta: (1) abre el interruptor mecánico, la corriente se transfiere al camino de
IGBT en < 2 ms; (2) el IGBT abre, la energía inductiva del cable
\(E_{MOV}=\tfrac12 L_{cable}I_{fault}^2\) es absorbida por el **varistor de óxido metálico (MOV)**, que
clampa la tensión mientras la corriente decae; (3) la corriente cae a cero en < 5 ms desde el inicio de la
apertura. Para \(L_{cable}=200\,\text{mH}\) e \(I_{fault}=20\,\text{kA}\):
\(E_{MOV}=\tfrac12\times0.2\times20000^2=40\,\text{MJ}\) — este valor determina el dimensionado del MOV,
el componente más costoso del DCCB híbrido.

**Protección diferencial del cable.** Es el método de protección principal en MTDC, por su selectividad
intrínseca: solo actúa si hay diferencia entre las corrientes en los dos extremos del cable. En
funcionamiento normal, \(I_1-I_2=I_C=C_{cable}\,dV_{dc}/dt\) (pequeño y predecible); ante una falta en el
cable, \(I_1-I_2=I_{falta}\gg I_C\). La función diferencial compara ambas corrientes con compensación de
la capacitiva:

$$ I_{diff} = I_1 - I_2 - C_{cable}\,\frac{dV_{dc}}{dt} > I_{diff,umbral} \quad\Rightarrow\quad \text{FALTA DC} $$

La latencia de comunicación entre extremos (fibra óptica integrada en el cable) es
\(\tau_{comm}\approx\ell/v_{fibra}\approx300\,\text{km}/2\times10^5\,\text{km/s}=1.5\,\text{ms}\), que
limita la velocidad de actuación. El umbral \(I_{diff,umbral}\) debe ser mayor que el error de medición
más la corriente capacitiva máxima en transitorios normales, y menor que la corriente de falta mínima
detectable — típicamente \(5\text{–}10\,\%\) de la corriente nominal.

## 9 — Estrategias de protección sin DCCB, y coordinación en redes malladas

El alto coste de los DCCB ha impulsado alternativas que evitan o reducen su necesidad:

**MMC de puente completo (FB-MMC).** Cada submódulo tiene 4 IGBTs (en vez de 2), lo que permite generar
tensión negativa: al detectar la falta, los brazos invierten su tensión y bloquean activamente la
corriente de falta en < 2 ms sin necesidad de DCCB, sin energía inductiva que disipar externamente.
Desventaja: el doble de IGBTs, ~2× las pérdidas nominales y mayor coste de submódulo. El **MMC híbrido**
(BorWin3) combina HB y FB en proporción, aprovechando la ventaja de bloqueo de los FB con menos coste que
un FB puro.

**Método de apretón de manos (*handshaking*).** Secuencia: (1) detectar la falta y abrir los disyuntores
AC de **todos** los terminales; (2) esperar la extinción natural de la corriente DC (la inductancia la
reduce a cero en 50–200 ms); (3) aislar el segmento defectuoso con seccionadores DC (de seccionamiento,
no de interrupción de falta); (4) reconectar los terminales sanos. Tiempo total 200–500 ms — aceptable
solo en sistemas punto a punto sin requisito de continuidad estricta; **inaceptable en MTDC**.

**Bus splitting.** La red DC se divide en zonas separadas por interruptores de seccionamiento; ante una
falta se aísla la zona afectada y el resto continúa operando. Los seccionadores no interrumpen corriente
de falta (para eso hace falta DCCB o FB-MMC), pero limitan el impacto a la zona defectuosa.

**Protección por sobrecorriente del convertidor.** El MMC limita la corriente de brazo por saturación del
regulador; si supera el umbral (1.5–2 pu), bloquea los IGBTs. Protege al convertidor pero no aísla el
cable — la corriente de falta puede seguir fluyendo desde otros terminales por los diodos.

**Combinaciones prácticas.** Los proyectos reales combinan FB-MMC en terminales críticos (máxima rapidez)
con DCCB híbridos en los cables más propensos a faltas y *handshaking* como respaldo para faltas en buses.

**Coordinación de protecciones en redes malladas.** La selectividad (interrumpir solo el tramo en falta
sin desconectar toda la red) requiere DCCB en cada extremo de cada línea y el algoritmo de detección de
ondas viajeras del apartado 8, coordinado entre todos los extremos para que solo actúe el DCCB más
cercano a la falta.

## 10 — Parámetros típicos, dimensionado y ejemplo numérico completo

**MMC (remite a [[mmc-modelo-control]] para la derivación de estas fórmulas).** Energía almacenada
\(W_{stored}\approx35\,\text{kJ/MVA}\times S_{nom}\); tensión de condensador \(V_{C,nom}=V_{dc}/N\);
capacidad de SM \(C_{SM}=W_{stored}N/(3V_{dc}^2)\).

| Parámetro MMC | Valor típico |
|---|---|
| Tensión DC | \( \pm 320\,\text{kV} \) (cables), \( \pm 500\,\text{kV} \) (aéreo) |
| Potencia nominal | 500 MW–2 GW |
| Inductancia de brazo \( L_{arm} \) | 0.15 pu |
| Energía almacenada | 30–40 kJ/MVA |
| Número de SMs por brazo \( N \) | 200–400 |
| Frecuencia de conmutación SM | 150–300 Hz |
| Pérdidas totales por terminal | 0.8–1.2 % |

**Ejemplo numérico completo: cable de 300 km, ±320 kV, 500 MW.**

*Paso 1 — corriente nominal.* \(I_{nom}=P_{nom}/V_{dc}=500\,\text{MW}/640\,\text{kV}=781\,\text{A}\).

*Paso 2 — sección del conductor.* Con densidad de corriente admisible ~500 A/mm² para XLPE submarino
refrigerado por agua de mar, se elige una sección normalizada de 1600 mm² (cobre):
\(R_{km}=\rho_{Cu}/A_{cond}=17.2\,\text{nΩ·m}/1600\times10^{-6}\,\text{m}^2=0.01075\,\Omega/\text{km}\).

*Paso 3 — parámetros totales.* \(R_{total}=R_{km}\ell=3.22\,\Omega\); \(L_{total}=L_{km}\ell=120\,
\text{mH}\); \(C_{total}=C_{km}\ell=60\,\mu\text{F}\).

*Paso 4 — pérdidas Joule.* \(P_{cable}=I_{nom}^2 R_{total}=781^2\times3.22=1.96\,\text{MW}\ (0.39\,\%)\).

*Paso 5 — resonancia LC.* \(f_{res}=1/(2\pi\sqrt{L_{total}C_{total}})\approx59\,\text{Hz}\) (estimación de
un único LC; el valor exacto, derivado en el apartado 5 a partir de los autovalores del sistema de tres
estados, es el doble: \(\approx119\,\text{Hz}\)); modos SSO con la estimación aproximada:
\(50\pm59\to9\,\text{Hz}\) (subsíncrono) y \(109\,\text{Hz}\) (supersíncrono).

*Paso 6 — corriente de falta DC pico* (apartado 8): \(Z_c=\sqrt{L_{total}/C_{total}}=44.7\,\Omega
\Rightarrow V_{dc}/Z_c\approx14.3\,\text{kA}\) (cota); con el amortiguamiento real
(\(\zeta\approx0.036\)), la solución exacta da \(I_{fault,pico}\approx13.5\,\text{kA}\approx17\,I_{nom}\)
(cota: \(\approx18\,I_{nom}\)).

*Paso 7 — energía almacenada en el cable.* \(W_{cable}=\tfrac12 C_{total}V_{dc}^2=12.3\,\text{MJ}\) —
comparable a la del propio MMC (~17.5 MJ para 500 MVA a 35 kJ/MVA), constituyendo la reserva de energía
del sistema que amortigua transitorios de potencia.

| Resultado | Valor |
|---|---|
| \( I_{nom} \) | 781 A |
| \( R_{total} \) | 3.22 Ω |
| \( C_{total} \) | 60 µF |
| Pérdidas Joule | 1.96 MW (0.39 %) |
| \( f_{res,LC} \) | 59 Hz |
| \( I_{fault,pico} \) | 13.5 kA (17 pu), cota 14.3 kA (18 pu) |
| \( W_{cable} \) | 12.3 MJ |

## 11 — Proyectos reales: DolWin, BorWin, NordLink, North Sea Wind Power Hub

Los proyectos offshore en el Mar del Norte son la referencia técnica mundial del HVDC-VSC.

**BorWin1 (2009, ABB, ±150 kV, 400 MW, 200 km).** Primer enlace HVDC-VSC offshore para un parque eólico.
Terminal offshore con VSC de dos niveles (aún no MMC). Demostró la viabilidad del concepto pero tuvo
problemas de resonancias con el filtro AC — la razón por la que el MMC (sin filtro AC de potencia) se
convirtió en el estándar.

**DolWin1 (2015, ABB, ±320 kV, 800 MW, 165 km).** Primer HVDC con MMC de ABB (HVDC Light quinta
generación). \(N\approx400\) SMs por brazo, \(V_{C,nom}\approx1.6\,\text{kV}\),
\(f_{sw,IGBT}\approx150\,\text{Hz}\).

**BorWin3 (2019, Siemens, ±320 kV, 900 MW, 160 km).** Primer HVDC con MMC híbrido (HB+FB en proporción)
que puede bloquear faltas DC sin DCCB (apartado 9).

**NordLink (2021, ABB+Siemens, ±525 kV, 1400 MW, 623 km).** Interconexión Noruega–Alemania. Primer HVDC
a ±525 kV — el nivel de tensión más alto para cables HVDC (apartado 7), demostrando la viabilidad del
XLPE DC-grade a tensiones antes reservadas al papel impregnado.

| Proyecto | Año | Tensión DC | Potencia | Longitud | Tecnología |
|---|---|---|---|---|---|
| BorWin1 | 2009 | ±150 kV | 400 MW | 200 km | VSC 2 niveles |
| DolWin1 | 2015 | ±320 kV | 800 MW | 165 km | MMC-HB |
| BorWin3 | 2019 | ±320 kV | 900 MW | 160 km | MMC híbrido |
| NordLink | 2021 | ±525 kV | 1400 MW | 623 km | MMC-HB cable XLPE |
| Dogger Bank | 2024+ | ±320 kV | 1200 MW×3 | ~130 km | MMC |

**North Sea Wind Power Hub (NSWPH).** El proyecto de mayor escala de MTDC planificado: una plataforma o
isla artificial que agrega 10–15 GW de eólica offshore de múltiples parques y la distribuye a cuatro
países europeos (Alemania, Dinamarca, Países Bajos, Bélgica). Arquitectura: 4–6 terminales VSC-HVDC,
cables de 500–1000 km a ±525 kV, topología **mallada** con redundancia (apartado 6). Solución de
protección prevista: DCCB híbridos en todos los puntos de derivación, MMC-FB en terminales offshore
críticos, relés de ondas viajeras con detección < 2 ms (apartado 8). En fase de planificación avanzada
(2026), desarrollando estándares técnicos (IEC 62975, ENTSO-E HVDC Grid Guidelines). Su éxito técnico —
en particular la solución de protección DC — determinará si el MTDC puede escalar al nivel de gigavatios
necesario para la transición energética europea.

## 12 — Comparativa LCC-HVDC vs VSC-HVDC

Todo lo anterior (apartados 1–11) trata exclusivamente HVDC-VSC, la tecnología dominante en las
instalaciones nuevas de hoy. Este último apartado la sitúa frente a su predecesora histórica, el HVDC
clásico con tiristores (LCC), que **no ha desaparecido**: sigue siendo la opción más barata y eficiente en
el extremo superior de potencia y tensión (Itaipu, Three Gorges, más abajo), aunque para todo lo demás
—y en particular para todo lo que motivó este capítulo: parques eólicos offshore, MTDC, redes débiles— el
VSC la ha desplazado casi por completo desde mediados de la década de 2010.

La tecnología HVDC clásica (LCC, Line Commutated Converter) usa tiristores que se conmutan
naturalmente por la tensión de red. El VSC-HVDC usa IGBTs con conmutación forzada. Las diferencias
son fundamentales para el diseño de sistemas:

**Por qué el tiristor necesita conmutación natural (y el IGBT no).** Un tiristor, una vez encendido por
la puerta, conduce mientras la corriente sea positiva — la puerta no tiene ningún control sobre el
apagado. Para apagarlo hace falta que la propia corriente del circuito caiga a cero y se invierta durante
un tiempo mínimo (tiempo de recuperación inversa). En un puente LCC, ese apagado ocurre porque el
**siguiente** tiristor de la secuencia se enciende y, gracias a la tensión de línea instantáneamente más
positiva en esa fase, fuerza a la corriente del tiristor saliente a decaer hasta cero — es la red, no el
dispositivo, quien "decide" cuándo puede ocurrir la conmutación. El IGBT, en cambio, tiene control de
puerta también en el apagado: puede cortar la corriente en el instante que el control decida, sin depender
de que la tensión externa se lo permita — de ahí "conmutación forzada".

**El ángulo de solape \(\mu\): la conmutación no es instantánea.** Mientras el tiristor entrante se
enciende y el saliente aún no se ha apagado, ambos conducen simultáneamente durante un intervalo angular
\(\mu\) (el "solape" o *commutation overlap*): la corriente no puede saltar de golpe de una rama a otra
porque tiene que atravesar la inductancia de conmutación \(X_c\) (esencialmente la reactancia de
cortocircuito del transformador convertidor) — ver panel (a) de la figura. Durante ese intervalo, la
tensión de línea se reparte entre ambas ramas en vez de aplicarse íntegra al puente, lo que reduce la
tensión media de salida por debajo del valor ideal \(\cos\alpha\) puro:

$$ \cos\alpha - \cos(\alpha+\mu) = \frac{2\,I_{dc}\,X_c}{\sqrt6\,V_{LL}} $$

Esta relación (derivada de igualar el área de tensión perdida durante el solape a la caída inductiva que
sufre la corriente) muestra que \(\mu\) **crece con la corriente de continua** \(I_{dc}\): a más potencia
transmitida, más ángulo de solape.

**El ángulo de extinción \(\gamma\), y el límite de red débil.** Para que el tiristor saliente recupere su
capacidad de bloqueo antes de que la tensión vuelva a hacerse positiva sobre él, tiene que disponer de un
margen angular mínimo tras el fin de la conducción:

$$ \gamma = 180° - \alpha - \mu \qquad \text{debe cumplir} \qquad \gamma > \gamma_{min}\approx15\text{–}18° $$

Si \(\gamma\) cae por debajo de \(\gamma_{min}\) (tiempo insuficiente de recuperación), el tiristor
saliente vuelve a conducir cuando no debía — un **fallo de conmutación** (*commutation failure*), que
colapsa la tensión DC durante varios ciclos. Esto es precisamente lo que ocurre con una **red débil**: si
el sistema AC tiene poca potencia de cortocircuito (SCR bajo), cualquier perturbación (una falta cercana,
un escalón de potencia) provoca una caída de tensión \(V_{LL}\) más pronunciada, lo que —por la relación de
arriba— aumenta \(\mu\) para la misma corriente y reduce \(\gamma\) por debajo del margen de seguridad. De
ahí el requisito práctico \(SCR\gtrsim2\text{–}3\) para operación fiable del LCC: no es un límite arbitrario,
sino la condición para que \(\gamma\) no colapse ante las perturbaciones normales de una red débil.

**Por qué el LCC no puede desacoplar \(P\) y \(Q\).** El propio ángulo de disparo \(\alpha\) que fija la
tensión DC (y por tanto \(P\)) determina también, junto con \(\mu\), el factor de potencia del lado AC —
aproximadamente \(\cos\varphi\approx(\cos\alpha+\cos(\alpha+\mu))/2\), la misma expresión que da la caída
de tensión por conmutación. El puente **siempre** consume reactiva del lado AC (nunca la genera, por la
propia naturaleza de la conmutación natural), y esa reactiva no es una variable de control independiente:
queda fijada por el punto de operación de \(P\). El panel (b) de la figura lo cuantifica: a ángulo de
disparo fijo, al subir \(I_{dc}\) (y por tanto \(P_{dc}\)), el ángulo \(\mu\) crece, el factor de potencia
empeora, y \(Q\) crece **más que proporcionalmente** con \(P\) — la razón \(Q/P\) pasa de \(\sim0.30\) a
\(\sim0.41\) en el rango simulado. El VSC, en cambio, con conmutación forzada no tiene este acoplamiento
(apartado 5): la tensión de salida se sintetiza libremente en módulo y fase respecto a la corriente, así
que \(P\) y \(Q\) se controlan mediante dos variables independientes.

<div class="cfig"><img src="figuras/lcc-conmutacion-natural.png" alt="forma de onda de la conmutacion entre dos tiristores de un puente LCC mostrando el angulo de disparo alpha y el angulo de solape mu durante el cual ambos tiristores conducen simultaneamente, con el angulo de extincion gamma marcado; y grafica de la potencia reactiva consumida frente a la potencia activa a angulo de disparo fijo, mostrando que Q crece mas que proporcionalmente a P"><div class="cap">(a) Conmutación entre dos tiristores de un puente LCC: la corriente tarda un ángulo \(\mu\) (solape) en transferirse del saliente al entrante, porque debe atravesar la reactancia de conmutación. El ángulo de extinción \(\gamma=180°-\alpha-\mu\) debe mantenerse por encima de un mínimo para evitar el fallo de conmutación — la condición que impone el límite de SCR. (b) A ángulo de disparo \(\alpha\) fijo, la potencia reactiva consumida crece más que proporcionalmente con la potencia activa: el LCC no puede pedir \(P\) sin pedir \(Q\), a diferencia del VSC.</div></div>

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

## Cuándo y por qué se usa

- Cables submarinos > 80 km, donde el cable AC queda limitado por la capacidad reactiva (efecto Ferranti).
- Interconexión de redes asíncronas o islas sin necesidad de sincronizar frecuencias.
- Conexión de parques eólicos offshore, especialmente en redes MTDC que integran múltiples parques.
- Cuando se necesita control independiente de \(P\) y \(Q\), *black start*, u operación con SCR bajo — el
  VSC lo permite, el LCC no (apartado 12).

## Errores comunes

- Asumir que el droop DC por sí solo mantiene \(V_{dc}\) en su valor nominal: sin control secundario, la
  tensión queda desviada permanentemente (\(\Delta V_{dc}\neq0\)) tras cada perturbación.
- Diseñar el PI de \(V_{dc}\) sobre \(V_{dc}\) directamente en vez de sobre \(W=\tfrac12CV_{dc}^2\): la
  planta en \(V_{dc}\) no es lineal, así que las ganancias que funcionan bien cerca de un punto de
  operación pueden no valer en otro (apartado 4).
- Poner dos terminales en modo maestro de \(V_{dc}\) simultáneo, o ninguno: en el primer caso los PI
  compiten por la misma variable: en el segundo, nada absorbe el desbalance de potencia (apartado 5).
- Usar \(V_{dc}/Z_c\) como si fuera el pico exacto de la corriente de falta: es una cota superior
  (amortiguamiento nulo), no el valor real, que es unos puntos porcentuales menor (apartado 8).
- Subestimar la energía que debe absorber el MOV del DCCB: para cables largos son decenas de MJ, no kJ.
- Confundir seccionadores DC (para apertura sin carga) con DCCB (para interrupción de corriente de
  falta): los primeros no pueden abrir corriente de falta.
- Atribuir el límite \(SCR\gtrsim2\text{–}3\) del LCC a una regla empírica sin fundamento: es consecuencia
  directa de que el ángulo de extinción \(\gamma\) no puede caer por debajo de su mínimo (apartado 12).

## Conceptos relacionados

- [[mmc-modelo-control]] · [[convertidor-back-to-back]] · [[topologias-multinivel]] · [[filtro-lcl]] ·
  [[fenomenos-oscilatorios-red]]

## Referencias

- Cigré TB 604, *Guide for the Development of Models for HVDC Converters*.
- Lesnicar & Marquardt, *An Innovative Modular Multilevel Converter Topology*.
- Hertem, Gomis-Bellmunt, Liang, *HVDC Grids: For Offshore and Supergrid of the Future*, Wiley 2016.
- Beerten, Cole, Belmans, *Generalized Steady-State VSC MTDC Model*, IEEE TPWRS 2012.
