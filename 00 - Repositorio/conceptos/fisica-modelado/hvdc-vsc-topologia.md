---
titulo: "HVDC-VSC: topología, cable DC, MTDC y protección"
slug: hvdc-vsc-topologia
categoria: fisica-modelado
tipo: concepto
nivel: avanzado
proyectos: []
objetivos: [comprender la arquitectura del HVDC-VSC y el MMC, modelar el cable DC y su falta, distinguir configuraciones punto a punto vs MTDC, entender el droop DC y la protección DC]
tags: [hvdc, vsc, mmc, lcc, monopolar, bipolar, punto-a-punto, multi-terminal, offshore, cable-dc, falta-dc, dccb, droop-dc, mtdc]
fecha_creacion: 2026-07-05
fecha_actualizacion: 2026-08-16
relacionados: [convertidor-back-to-back, topologias-multinivel, filtro-lcl, fenomenos-oscilatorios-red, mmc-modelo-control]
referencias:
  - "Cigré TB 604, Guide for the Development of Models for HVDC Converters"
  - "Lesnicar & Marquardt, An Innovative Modular Multilevel Converter Topology"
  - "Hertem, Gomis-Bellmunt, Liang, HVDC Grids: For Offshore and Supergrid of the Future, Wiley 2016"
  - "Beerten, Cole, Belmans, Generalized Steady-State VSC MTDC Model, IEEE TPWRS 2012"
---

## 1 — Definición y motivación del HVDC-VSC

HVDC-VSC (High Voltage Direct Current con Voltage Source Converter) transmite potencia eléctrica en
corriente continua usando convertidores de fuente de tensión en ambos extremos. A diferencia del HVDC
clásico con tiristores (LCC-HVDC, apartado 5), el VSC-HVDC:

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
enlaces HVDC-VSC de nueva construcción de cierta envergadura (DolWin, BorWin, NordLink — apartado 10) usan
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

**Topologías de red MTDC.** Cuando hay tres o más terminales en la misma red DC (apartado 4), la
disposición geométrica de los cables entre ellos define otra decisión de topología independiente de la
configuración de polos anterior:

<div class="cfig"><img src="figuras/hvdc-mtdc-topologias.png" alt="comparacion de topologias de red MTDC: radial con un nodo central conectado a cinco terminales VSC en estrella, y mallada con cuatro terminales VSC conectados por multiples caminos redundantes con un DCCB marcado en cada extremo de cada linea"><div class="cap">(a) Topología radial: cada terminal conectado por un único camino a un nodo central — barata pero sin redundancia, un fallo de cable aísla toda esa rama. (b) Topología mallada: múltiples caminos redundantes entre terminales, con un DCCB (cuadrado rojo) en cada extremo de cada línea para poder aislar solo el tramo en falta sin perder el resto de la red.</div></div>

La **radial** conecta cada terminal por un único camino a un nodo central (o a los demás terminales en
cadena): es simple y económica para 3–4 terminales, pero el nodo central (o cualquier tramo intermedio)
es un punto único de fallo — perderlo aísla toda esa rama de la red. La **mallada** añade conexiones
redundantes entre terminales de modo que existe más de un camino entre cualquier par de nodos: mayor
coste de cable y de disyuntores DC (uno en cada extremo de cada línea, apartado 8), pero sin punto único
de fallo — es la topología objetivo de las futuras superredes DC offshore (North Sea Wind Power Hub,
apartado 10).

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
VSC-HVDC moderno del VSC de dos niveles de la primera generación (BorWin1, apartado 9).

## 4 — Topología punto a punto vs MTDC, y el droop de tensión DC

**Punto a punto.** Dos terminales VSC conectados por un cable DC. Es la topología más sencilla: un
terminal controla \( V_{dc} \) (el regulador del balance de energía del cable) y el otro controla \( P \)
(inyecta o absorbe la potencia deseada). El control es centralizado y sencillo.

**MTDC (Multi-Terminal DC).** Tres o más terminales VSC conectados en la misma red DC. Los proyectos
actuales más relevantes son las redes offshore para integrar múltiples parques eólicos y entregarlos a
múltiples puntos de la red onshore (apartado 9, North Sea Wind Power Hub). Ventajas respecto a múltiples
enlaces punto a punto: redundancia (si un enlace falla, la potencia se redistribuye), menor coste
marginal por terminal (el cable ya existe), posibilidad de optimización del flujo de potencia en la red
DC.

**Topologías de red DC.** **Radial (árbol):** cada nodo conectado por un único camino al resto; simple y
barata, pero sin redundancia — un fallo de cable aísla la rama completa. **Mallada:** múltiples caminos
entre cualquier par de nodos; mayor redundancia y flexibilidad de despacho, a costa de mayor complejidad
de protección (la corriente de falta puede circular por varios caminos) y de necesitar un DCCB en cada
extremo de cada línea (apartado 8).

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

## 5 — Comparativa LCC-HVDC vs VSC-HVDC

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
\(\sim0.41\) en el rango simulado. El VSC, en cambio, con conmutación forzada no tiene este acoplamiento:
la tensión de salida se sintetiza libremente en módulo y fase respecto a la corriente, así que \(P\) y
\(Q\) se controlan mediante dos variables independientes (ver el modelo dq del MMC en
[[mmc-modelo-control]]).

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

## 6 — El cable DC: características y modelo π

**Diferencias con el cable AC.** En corriente continua la inductancia no tiene efecto reactivo
(\(\omega=0\)), por lo que la impedancia en régimen permanente es puramente resistiva. Esto elimina la
limitación de Ferranti y el problema de la potencia reactiva de carga que condena a los cables AC a
longitudes máximas de ~80–100 km. La capacidad del cable, en cambio, es incluso más importante en DC que
en AC: almacena energía \(W=\tfrac12 C_{cable}V_{dc}^2\) que actúa como reserva de energía y determina la
dinámica de la tensión DC durante los transitorios de control y las faltas (apartado 7).

| Parámetro | Cable AC 132 kV | Cable DC ±320 kV HVDC |
|---|---|---|
| Resistencia \( R \) | 0.05 Ω/km | 0.012 Ω/km (conductor mayor) |
| Inductancia \( L \) | 0.4 mH/km | 0.4 mH/km (irrelevante en DC) |
| Capacidad \( C \) | 0.2 µF/km | 0.15–0.25 µF/km |
| Longitud máxima operativa | ~80 km | ilimitada (prácticamente) |
| Pérdidas/100 km | > 1 % (reactiva) | ~0.3 % (solo Joule) |

La inductancia \(L\) sí importa en el análisis dinámico de transitorios y faltas DC — forma con la
capacidad el circuito resonante que determina la velocidad de crecimiento de la corriente de falta
(apartado 7).

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
\(C_{cable}=60\,\mu\text{F}\): \(f_{res}\approx59\,\text{Hz}\). Esta frecuencia cae dentro del ancho de
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
en la corriente de falta del apartado 7. En la práctica se discretiza el cable en \(n\) secciones π en
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

## 7 — Falta DC: dinámica, detección y protección

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
natural (la misma \(f_{res}\) del apartado 6). La solución general es
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
\(V_{dc}\) e \(I_{dc}\) (protección basada en ondas viajeras, apartado 6). El criterio de disparo
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

## 8 — Estrategias de protección sin DCCB, y coordinación en redes malladas

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
ondas viajeras del apartado 7, coordinado entre todos los extremos para que solo actúe el DCCB más
cercano a la falta.

## 9 — Parámetros típicos, dimensionado y ejemplo numérico completo

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

*Paso 5 — resonancia LC.* \(f_{res}=1/(2\pi\sqrt{L_{total}C_{total}})\approx59\,\text{Hz}\); modos SSO:
\(50\pm59\to9\,\text{Hz}\) (subsíncrono) y \(109\,\text{Hz}\) (supersíncrono).

*Paso 6 — corriente de falta DC pico* (apartado 7): \(Z_c=\sqrt{L_{total}/C_{total}}=44.7\,\Omega
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

## 10 — Proyectos reales: DolWin, BorWin, NordLink, North Sea Wind Power Hub

Los proyectos offshore en el Mar del Norte son la referencia técnica mundial del HVDC-VSC.

**BorWin1 (2009, ABB, ±150 kV, 400 MW, 200 km).** Primer enlace HVDC-VSC offshore para un parque eólico.
Terminal offshore con VSC de dos niveles (aún no MMC). Demostró la viabilidad del concepto pero tuvo
problemas de resonancias con el filtro AC — la razón por la que el MMC (sin filtro AC de potencia) se
convirtió en el estándar.

**DolWin1 (2015, ABB, ±320 kV, 800 MW, 165 km).** Primer HVDC con MMC de ABB (HVDC Light quinta
generación). \(N\approx400\) SMs por brazo, \(V_{C,nom}\approx1.6\,\text{kV}\),
\(f_{sw,IGBT}\approx150\,\text{Hz}\).

**BorWin3 (2019, Siemens, ±320 kV, 900 MW, 160 km).** Primer HVDC con MMC híbrido (HB+FB en proporción)
que puede bloquear faltas DC sin DCCB (apartado 8).

**NordLink (2021, ABB+Siemens, ±525 kV, 1400 MW, 623 km).** Interconexión Noruega–Alemania. Primer HVDC
a ±525 kV — el nivel de tensión más alto para cables HVDC (apartado 6), demostrando la viabilidad del
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
cables de 500–1000 km a ±525 kV, topología **mallada** con redundancia (apartado 4). Solución de
protección prevista: DCCB híbridos en todos los puntos de derivación, MMC-FB en terminales offshore
críticos, relés de ondas viajeras con detección < 2 ms (apartado 7). En fase de planificación avanzada
(2026), desarrollando estándares técnicos (IEC 62975, ENTSO-E HVDC Grid Guidelines). Su éxito técnico —
en particular la solución de protección DC — determinará si el MTDC puede escalar al nivel de gigavatios
necesario para la transición energética europea.

## Cuándo y por qué se usa

- Cables submarinos > 80 km, donde el cable AC queda limitado por la capacidad reactiva (efecto Ferranti).
- Interconexión de redes asíncronas o islas sin necesidad de sincronizar frecuencias.
- Conexión de parques eólicos offshore, especialmente en redes MTDC que integran múltiples parques.
- Cuando se necesita control independiente de \(P\) y \(Q\), *black start*, u operación con SCR bajo — el
  VSC lo permite, el LCC no (apartado 5).

## Errores comunes

- Asumir que el droop DC por sí solo mantiene \(V_{dc}\) en su valor nominal: sin control secundario, la
  tensión queda desviada permanentemente (\(\Delta V_{dc}\neq0\)) tras cada perturbación.
- Usar \(V_{dc}/Z_c\) como si fuera el pico exacto de la corriente de falta: es una cota superior
  (amortiguamiento nulo), no el valor real, que es unos puntos porcentuales menor (apartado 7).
- Subestimar la energía que debe absorber el MOV del DCCB: para cables largos son decenas de MJ, no kJ.
- Confundir seccionadores DC (para apertura sin carga) con DCCB (para interrupción de corriente de
  falta): los primeros no pueden abrir corriente de falta.
- Atribuir el límite \(SCR\gtrsim2\text{–}3\) del LCC a una regla empírica sin fundamento: es consecuencia
  directa de que el ángulo de extinción \(\gamma\) no puede caer por debajo de su mínimo (apartado 5).

## Conceptos relacionados

- [[mmc-modelo-control]] · [[convertidor-back-to-back]] · [[topologias-multinivel]] · [[filtro-lcl]] ·
  [[fenomenos-oscilatorios-red]]

## Referencias

- Cigré TB 604, *Guide for the Development of Models for HVDC Converters*.
- Lesnicar & Marquardt, *An Innovative Modular Multilevel Converter Topology*.
- Hertem, Gomis-Bellmunt, Liang, *HVDC Grids: For Offshore and Supergrid of the Future*, Wiley 2016.
- Beerten, Cole, Belmans, *Generalized Steady-State VSC MTDC Model*, IEEE TPWRS 2012.
