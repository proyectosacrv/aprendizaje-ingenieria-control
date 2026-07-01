---
titulo: Sistema trifásico equilibrado
slug: sistema-trifasico
categoria: fisica-modelado
tipo: concepto
nivel: basico
proyectos: []
objetivos: [manejar tensiones y corrientes trifásicas y sus relaciones línea-fase]
tags: [trifasico, equilibrado, fasores, linea-fase, basico, modelado, potencia, delta-estrella]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-01
relacionados: [potencia-ac-fasores, marco-dq, sistema-por-unidad, componentes-simetricas]
referencias:
  - "Chapman, Máquinas Eléctricas, McGraw-Hill"
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
  - "Kundur, Power System Stability and Control, McGraw-Hill"
---

## Definición
Sistema de tres tensiones senoidales de igual amplitud y frecuencia, **desfasadas 120°**. Si las
cargas son iguales en las tres fases, el sistema es **equilibrado** y se reduce a un análisis
monofásico equivalente.

## Fundamento teórico
$$ v_a=\hat V\cos\omega t,\quad v_b=\hat V\cos(\omega t-120°),\quad v_c=\hat V\cos(\omega t+120°) $$
En equilibrio la suma instantánea es nula (\( v_a+v_b+v_c=0 \)) → no circula corriente por el
neutro. Relaciones línea-fase:
- **Estrella (Y):** \( V_{LL}=\sqrt3\,V_{fase} \), \( I_{L}=I_{fase} \).
- **Triángulo (Δ):** \( V_{LL}=V_{fase} \), \( I_{L}=\sqrt3\,I_{fase} \).

Potencia trifásica total (constante en equilibrio):
$$ P=\sqrt3\,V_{LL}I_L\cos\varphi,\qquad S=\sqrt3\,V_{LL}I_L $$
La potencia instantánea total es **constante** (no pulsa a \( 2\omega \) como la monofásica), lo
que motiva el control en [[marco-dq|dq]].

<div class="cfig"><img src="figuras/sistema-trifasico-ondas.png" alt="tensiones trifasicas y sus fasores"><div class="cap">Tres senoides de igual amplitud desfasadas 120°; sus fasores forman una estrella simétrica cuya suma instantánea es cero. Por eso la potencia trifásica total (en equilibrio) no pulsa.</div></div>

<div class="cfig"><img src="figuras/sistema-trifasico-analisis.png" alt="analisis completo sistema trifasico"><div class="cap">(a) Tensiones y potencias instantáneas de las tres fases: las pulsaciones a 2ω de p_a, p_b, p_c se cancelan y p_total es plana. (b) Diagrama fasorial con tensiones de fase y de línea: V_LL es √3 veces V_f y adelanta 30°. (c) Triángulo de potencia P=4 MW, Q=3 MVAr, S=5 MVA, FP=0.80. (d) Comparativa monofásico (pulsa a 2ω) vs trifásico equilibrado (constante).</div></div>

## 1 — Por qué \( V_{LL}=\sqrt3\,V_{fase} \) en estrella
**Paso 1 — la tensión de línea es una resta de fases.** En conexión estrella, la tensión de línea entre los bornes a y b es la diferencia de las dos tensiones de fase (ambas referidas al neutro):

$$ \bar V_{ab}=\bar V_a-\bar V_b $$

Con \( \bar V_a=V_f\angle0° \) y \( \bar V_b=V_f\angle{-120°} \) (terna equilibrada, ambas de módulo \( V_f \)).

**Paso 2 — restar los fasores.** Pasando a binómica, \( \bar V_b=V_f(\cos(-120°)+j\sin(-120°))=V_f(-\tfrac12-j\tfrac{\sqrt3}{2}) \):

$$ \bar V_{ab}=V_f(1+j0)-V_f\Big(-\tfrac12-j\tfrac{\sqrt3}{2}\Big)=V_f\Big(\tfrac32+j\tfrac{\sqrt3}{2}\Big) $$

**Paso 3 — tomar el módulo.** El módulo de \( \tfrac32+j\tfrac{\sqrt3}{2} \) es:

$$ \Big|\bar V_{ab}\Big|=V_f\sqrt{\Big(\tfrac32\Big)^2+\Big(\tfrac{\sqrt3}{2}\Big)^2}=V_f\sqrt{\tfrac94+\tfrac34}=V_f\sqrt{\tfrac{12}{4}}=V_f\sqrt3 $$

$$ \boxed{\;V_{LL}=\sqrt3\,V_{fase}\;} $$

El \( \sqrt3 \) sale de la geometría: dos fasores de igual módulo separados \( 120° \) tienen una diferencia \( \sqrt3 \) veces mayor (su ángulo además adelanta \( 30° \), \( \bar V_{ab}=\sqrt3\,V_f\angle30° \)). La corriente, en cambio, no se desdobla: \( I_L=I_{fase} \) porque la línea es el único camino de la fase. En triángulo el papel se invierte (las fases comparten la tensión de línea pero las corrientes se restan), de ahí \( V_{LL}=V_{fase} \), \( I_L=\sqrt3\,I_{fase} \).

## 2 — Por qué la potencia trifásica es constante (no pulsa a \( 2\omega \))
**Paso 1 — sumar las tres potencias instantáneas.** Cada fase tiene una potencia que pulsa a \( 2\omega \) (ver [[potencia-ac-fasores]]): \( p_k=V_fI_f\cos\varphi+V_fI_f\cos(2\omega t-\varphi+\phi_k) \), donde \( \phi_k=0,-240°,+240° \) son los desfases dobles de cada fase. La total:

$$ p_{3\phi}=\underbrace{3V_fI_f\cos\varphi}_{\text{constante}}+V_fI_f\big[\cos(2\omega t-\varphi)+\cos(2\omega t-\varphi-240°)+\cos(2\omega t-\varphi+240°)\big] $$

**Paso 2 — el corchete pulsante se anula.** Tres cosenos de igual frecuencia separados \( 120° \) (porque \( 240°\equiv-120° \)) suman cero: es la misma identidad \( 1+a+a^2=0 \) de [[componentes-simetricas]] proyectada sobre el eje real. El corchete vale 0 idénticamente para todo \( t \):

$$ \boxed{\;p_{3\phi}(t)=3V_fI_f\cos\varphi=\text{constante}=\sqrt3\,V_{LL}I_L\cos\varphi\;} $$

usando \( V_{LL}=\sqrt3 V_f \) e \( I_L=I_f \) del apartado 1 (de donde \( 3V_f=\sqrt3 V_{LL} \)). Que la potencia no pulse es la razón física de fondo para controlar en [[marco-dq|dq]]: en el marco giratorio las magnitudes son continuas y P, Q se vuelven escalares constantes en régimen.

## 3 — La secuencia de fases: ABC vs ACB y su importancia
La **secuencia de fases** especifica el orden en que cada tensión alcanza su pico. En una terna equilibrada hay solo dos posibilidades:

- **Secuencia positiva (ABC, directa):** \( v_a \) alcanza el pico primero, \( v_b \) después (120° más tarde), \( v_c \) el último (240° más tarde). Los desfases son \( 0°,-120°,+120° \). Es la secuencia estándar de los sistemas eléctricos europeos.
- **Secuencia negativa (ACB, inversa):** el orden se invierte: \( v_a \) va a \( 0° \), \( v_c \) a \( -120° \) y \( v_b \) a \( +120° \). Equivale a intercambiar dos fases cualesquiera de la terna ABC (por ejemplo, permutar b y c).

**Por qué importa en máquinas rotativas.** Un motor asíncrono trifásico gira en el sentido en que el campo magnético giratorio progresa. El campo giratorio avanza de a→b→c con secuencia positiva, y en sentido contrario con secuencia negativa. Permutar dos fases invierte el giro del motor. En bombas y compresores esto puede ser destructivo; en frenos regenerativos puede ser útil.

**Secuencias en sistemas desequilibrados y el papel de las componentes simétricas.** Un sistema desequilibrado (tensiones de distinta amplitud o desfases que no son exactamente 120°) siempre puede descomponerse en tres sistemas equilibrados: uno de secuencia positiva, uno negativo y uno homopolar (suma no nula). La secuencia negativa es especialmente dañina en motores porque genera un par frenante que compite con el par motor e induce corrientes parásitas elevadas en el rotor.

**Detección de secuencia en convertidores.** La [[pll-srf|PLL]] estándar (SRF-PLL) está diseñada para seguir la secuencia positiva: cuando el sistema tiene componente negativa (desequilibrio o falta asimétrica), la componente de secuencia negativa aparece en el marco \( \alpha\beta \) como un vector que gira a \( -\omega \) (en sentido contrario al de secuencia positiva). Un DSOGI (dual second-order generalized integrator) separa las dos componentes de giro antes de alimentar la PLL, evitando que la oscilación a \( 2\omega \) en las señales dq engañe al regulador de fase.

**Identificación rápida en el campo.** Con un fasímetro o un analizador de red se pueden medir los ángulos de las tres fases. Si la secuencia de los ángulos de \( v_a, v_b, v_c \) en orden creciente es positiva (el ángulo de \( v_b \) está 120° por detrás del de \( v_a \), y el de \( v_c \) otros 120° por detrás) la secuencia es ABC. Si el orden es \( v_a, v_c, v_b \) la secuencia es ACB.

## 4 — La conexión Δ: tensiones de fase = línea, corrientes se restan
En una carga o generador en **triángulo (Δ)** cada impedancia de fase está conectada directamente entre dos bornes de línea, sin punto neutro. Eso cambia radicalmente la relación entre tensiones y corrientes respecto a la estrella.

**Tensiones.** La tensión en cada rama del triángulo es directamente la tensión entre las dos líneas a las que se conecta:
$$ V_{fase,\Delta}=V_{LL} $$
No hay relación \( \sqrt3 \): la tensión de fase en triángulo ya es la tensión de línea.

**Corrientes — la resta de dos corrientes de fase da la corriente de línea.** Sea \( \bar I_{ab} \) la corriente que circula por la rama ab del triángulo (de a hacia b). La corriente de línea que llega al nudo a es la que entra por la rama ab menos la que sale por la rama ca:

$$ \bar I_{L,a}=\bar I_{ab}-\bar I_{ca} $$

Con \( \bar I_{ab}=I_\Delta\angle0° \) y \( \bar I_{ca}=I_\Delta\angle120° \) (sistema equilibrado, desfase de 120° entre corrientes de rama):

$$ \bar I_{L,a}=I_\Delta(1-e^{j120°})=I_\Delta\Big(1-\Big(-\tfrac12+j\tfrac{\sqrt3}{2}\Big)\Big)=I_\Delta\Big(\tfrac32-j\tfrac{\sqrt3}{2}\Big) $$

$$ \big|\bar I_{L,a}\big|=I_\Delta\sqrt{\Big(\tfrac32\Big)^2+\Big(\tfrac{\sqrt3}{2}\Big)^2}=I_\Delta\sqrt3 $$

$$ \boxed{\;I_L=\sqrt3\,I_{fase,\Delta}\;} $$

La corriente de línea retrasa 30° respecto a la corriente de fase del triángulo (análogo al adelanto de 30° de \( V_{LL} \) respecto a \( V_{fase,Y} \)).

**La potencia en triángulo es igual a la potencia en estrella equivalente.** Sustituyendo en la expresión de potencia:
$$ P_\Delta=3\,V_{fase,\Delta}\,I_{fase,\Delta}\cos\varphi=3\,V_{LL}\,\frac{I_L}{\sqrt3}\cos\varphi=\sqrt3\,V_{LL}\,I_L\cos\varphi $$
Idéntica a la fórmula de estrella, como debe ser: la potencia no depende de la forma en que se conecten las impedancias, sino del voltaje aplicado y la corriente absorbida.

**Conversión Δ↔Y (equivalente de Thevenin).** Una impedancia \( Z_\Delta \) en triángulo es eléctricamente equivalente (vista desde los terminales) a una impedancia \( Z_Y=Z_\Delta/3 \) en estrella:
$$ Z_Y=\frac{Z_\Delta}{3} $$
La demostración parte de igualar las admitancias vistas desde cada par de terminales. Para resistencias: \( R_Y=R_\Delta/3 \). Esto permite convertir siempre a estrella antes de aplicar el equivalente monofásico.

**Cuándo se usa triángulo.** Los transformadores de distribución (p.ej. Δ/Y) usan el lado Δ para eliminar las corrientes homopolares (de secuencia cero) en la red de MT, que no pueden circular en el triángulo. Los motores industriales se pueden conectar en Δ para funcionar a tensión de línea reducida (arranque estrella-triángulo). En convertidores de potencia los filtros LCL suelen tener el convertidor en Δ o en Y con neutro flotante.

## 5 — El equivalente monofásico: cuándo y cómo
En un sistema trifásico **equilibrado** y con **conexión Y** (o con carga Δ previamente convertida a Y), las tres fases son simétricas: misma amplitud, mismo ángulo de desfase con sus respectivas tensiones de fase. Por tanto basta analizar **una sola fase**.

**El método paso a paso:**

**Paso 1 — identificar la tensión de fase.** Si se conoce \( V_{LL} \) (línea a línea), la tensión de fase eficaz es \( V_f=V_{LL}/\sqrt3 \). Esta es la tensión que ve la fase a respecto al neutro.

**Paso 2 — colocar el fasor de referencia.** Por convención se toma \( \bar V_a=V_f\angle0° \). Las otras dos fases son \( \bar V_b=V_f\angle{-120°} \) y \( \bar V_c=V_f\angle{+120°} \), pero no se necesitan para el análisis monofásico.

**Paso 3 — resolver el circuito monofásico.** Con la impedancia de carga por fase \( Z \), la corriente de línea (= corriente de fase en Y) es:
$$ \bar I_a=\frac{\bar V_a}{Z}=\frac{V_f\angle0°}{|Z|\angle\varphi}=\frac{V_f}{|Z|}\angle(-\varphi) $$

**Paso 4 — escalar a la potencia total.** La potencia total se multiplica por 3:
$$ P_{total}=3\,\mathrm{Re}(\bar V_a\,\bar I_a^{*})=3\,V_f\,I_f\cos\varphi=\sqrt3\,V_{LL}\,I_L\cos\varphi $$

**Ejemplo numérico.** Carga R=10 Ω por fase en Y, \( V_{LL}=400\,\text{V} \): \( V_f=400/\sqrt3=231\,\text{V} \), \( I_f=231/10=23.1\,\text{A} \), \( P_{total}=3\times231\times23.1=16{,}000\,\text{W}=16\,\text{kW} \). Verificación: \( P=V_{LL}^2/(R\times\sqrt3^2\times1/3)=400^2/10/\sqrt3^2\times3=16\,\text{kW} \). ✓

**Conversión previa Δ→Y.** Si la carga es \( Z_\Delta \), se convierte primero a \( Z_Y=Z_\Delta/3 \) y se aplica el equivalente monofásico con esa impedancia.

**Cuándo NO vale el equivalente monofásico:**
- Cargas desequilibradas (las impedancias por fase son distintas): el neutro ya no es equipotencial y hay corriente en él. Hay que usar las tres fases o [[componentes-simetricas]].
- Faltas asimétricas (falta monofásica, bifásica): aparecen componentes de secuencia negativa y cero. Usar componentes simétricas.
- Análisis de armónicos con desequilibrio: similar, el 3.° armónico es homopolar y no circula en red sin neutro.

## 6 — Representación fasorial de un sistema trifásico: por qué se usa
Un fasor es la forma compacta de representar una senoide en **régimen permanente**. La idea central: si todos los voltajes y corrientes del circuito oscilan a la misma frecuencia \( \omega \), las relaciones entre ellos son lineales y constantes (en amplitud y fase). El álgebra de fasores explota eso.

**Definición formal.** La senoide \( f(t)=\hat F\cos(\omega t+\theta) \) se asocia al fasor:
$$ \bar F=\frac{\hat F}{\sqrt2}\,e^{j\theta}=F_{rms}\,e^{j\theta}\quad\text{(fasor eficaz)} $$
La relación con la señal temporal es \( f(t)=\sqrt2\,\mathrm{Re}\{\bar F\,e^{j\omega t}\} \): se puede imaginar el fasor \( \bar F \) girando a \( \omega \) en el plano complejo; la proyección sobre el eje real (multiplicada por \( \sqrt2 \)) da la senoide.

**Por qué la derivada temporal se convierte en \( j\omega \).** Si \( f(t)=\sqrt2\,\mathrm{Re}\{\bar F\,e^{j\omega t}\} \), entonces:
$$ \frac{df}{dt}=\sqrt2\,\mathrm{Re}\{j\omega\bar F\,e^{j\omega t}\}\quad\Rightarrow\quad \frac{d}{dt}\leftrightarrow j\omega $$
Esto transforma la ecuación diferencial de un inductor (\( v=L\,di/dt \)) en la relación algebraica \( \bar V=j\omega L\,\bar I \): la impedancia del inductor es \( Z_L=j\omega L \).

**Las leyes de Kirchhoff en fasores.** Puesto que KVL y KCL son sumas algebraicas que se cumplen para la senoide real, y la proyección (parte real) es lineal, se cumplen también para los fasores complejos: \( \sum\bar V=0 \), \( \sum\bar I=0 \). Esto convierte el análisis de circuitos AC en álgebra lineal compleja.

**Los tres fasores de un sistema equilibrado forman una estrella simétrica.** \( \bar V_a=V_f\angle0° \), \( \bar V_b=V_f\angle{-120°} \), \( \bar V_c=V_f\angle{+120°} \). Sus módulos son iguales y sus ángulos suman cero: \( \bar V_a+\bar V_b+\bar V_c=0 \). Geométricamente forman un triángulo equilátero en el plano complejo.

**La conexión con el marco dq.** En [[marco-dq|dq]] el vector de espacio \( \vec x_{dq}=x_d+jx_q \) es exactamente el fasor de la señal vista en un marco que gira a \( \omega \) con la red. Lo que en fasores estáticos es un número complejo constante, en el tiempo real es el vector dq: en régimen permanente el dq es DC, fuera de él el dq varía lentamente. Por eso el fasor solo captura el régimen permanente; los transitorios requieren modelos de espacio de estados.

**Limitación clave.** El análisis fasorial asume que la red es lineal y opera exactamente a \( \omega \). No describe transitorios de conmutación, armónicos o cambios de frecuencia. Para eso se usa el modelo promediado en dq o la simulación en tiempo discreto.

## 7 — Potencia en sistema trifásico: P, Q, S y el factor de potencia
Las expresiones de potencia del sistema trifásico equilibrado se derivan de la potencia monofásica multiplicada por 3 (o equivalentemente, en términos de magnitudes de línea).

**Potencia activa:**
$$ P=3\,V_f\,I_f\cos\varphi=\sqrt3\,V_{LL}\,I_L\cos\varphi $$

La sustitución \( V_f=V_{LL}/\sqrt3 \) e \( I_L=I_f \) (en Y) da el factor \( \sqrt3 \). En triángulo la misma expresión vale con \( I_L=\sqrt3\,I_\Delta \) y \( V_{LL}=V_{fase,\Delta} \).

**Potencia reactiva:**
$$ Q=3\,V_f\,I_f\sin\varphi=\sqrt3\,V_{LL}\,I_L\sin\varphi $$

\( Q>0 \) carga inductiva (corriente retrasada), \( Q<0 \) capacitiva (corriente adelantada). La reactiva no hace trabajo neto pero circula por los cables y eleva la corriente de línea.

**Potencia aparente:**
$$ S=\sqrt{P^2+Q^2}=\sqrt3\,V_{LL}\,I_L=3\,V_f\,I_f $$

Es el producto de tensión y corriente eficaces (sin desfase), en VA. Determina el dimensionado de cables, transformadores y convertidores.

**Factor de potencia:**
$$ \cos\varphi=\frac{P}{S} $$

Una planta con FP=0.7 consume \( I_L=P/(\sqrt3\,V_{LL}\times0.7) \) en lugar de \( P/(\sqrt3\,V_{LL}) \) con FP=1: la corriente es un 43 % mayor, con las pérdidas Joule correspondientes.

**Potencia en el marco dq (convención amplitud invariante).** Con la [[transformada-clarke|transformada dq]] de amplitud invariante, el vector de espacio de tensión tiene módulo \( \sqrt{2/3}\,\hat V \) y el de corriente \( \sqrt{2/3}\,\hat I \). La potencia instantánea total de las tres fases es:
$$ p_{3\phi}(t)=\frac32\,(v_d\,i_d+v_q\,i_q) $$
En régimen permanente \( p_{3\phi}=P \) (constante). Las componentes activa y reactiva:
$$ P=\frac32\,(v_d\,i_d+v_q\,i_q),\qquad Q=\frac32\,(v_q\,i_d-v_d\,i_q) $$

Con la PLL que alinea el eje d con la tensión de red (\( v_d=V \), \( v_q=0 \)):
$$ P=\frac32\,V\,i_d,\qquad Q=-\frac32\,V\,i_q $$

El control de potencia activa y reactiva se reduce a controlar \( i_d \) e \( i_q \) por separado (desacoplado en dq): esta es la base del control vectorial orientado a tensión ([[marco-dq]]).

**Por qué en trifásico equilibrado la potencia no pulsa.** Cada fase contribuye con \( p_k=P/3+P/3\cdot\cos(2\omega t+\phi_k) \). Los tres términos pulsantes están desfasados \( 120° \) entre sí (porque \( \phi_k=0,-120°,-240° \) en la frecuencia doble) y suman cero. Demostración completa en el apartado 2.

## 8 — Aplicación al dimensionado de un convertidor trifásico
Dimensionar un VSC (convertidor de fuente de tensión) que inyecta \( P=5\,\text{MW} \) con \( Q=2\,\text{MVAr} \) (inductivo) a una red de \( V_{LL}=33\,\text{kV} \).

**Paso 1 — potencia aparente.**
$$ S=\sqrt{P^2+Q^2}=\sqrt{5^2+2^2}\,\text{MVA}=\sqrt{29}\approx5.385\,\text{MVA} $$

**Paso 2 — corriente de línea.**
$$ I_L=\frac{S}{\sqrt3\,V_{LL}}=\frac{5.385\times10^6}{\sqrt3\times33000}\approx94.3\,\text{A} $$
Con factor de potencia \( \cos\varphi=P/S=5/5.385\approx0.929 \) (no es exactamente 0.93: el redondeo habitual introduce un 0.3 % de error).

**Paso 3 — tensión de fase pico (para el modulo PWM).**
$$ \hat V_f=\frac{V_{LL}\sqrt2}{\sqrt3}=V_{LL}\sqrt{\frac23}=33000\times\sqrt{\frac23}\approx26{,}943\,\text{V} $$
Esta es la amplitud pico que el convertidor debe generar en su salida AC. Define el índice de modulación máximo: con modulación sinusoidal pura \( m_a\leq1 \), la tensión de fase pico máxima que entrega el convertidor es \( \hat V_{f,max}=V_{dc}/2 \), de donde \( V_{dc,min}=2\hat V_f\approx53.9\,\text{kV} \). Con sobremodulación (tercer armónico inyectado): \( \hat V_{f,max}=V_{dc}/\sqrt3 \) y \( V_{dc,min}=\sqrt3\hat V_f\approx46.7\,\text{kV} \).

**Paso 4 — referencias dq en el control.** Alineando la PLL con \( v_d=V_f \), \( v_q=0 \):
$$ i_d^*=\frac{2P}{3V_f}=\frac{2\times5\times10^6}{3\times33000/\sqrt3}=\frac{10\times10^6}{3\times19053}\approx175\,\text{A} $$
$$ i_q^*=-\frac{2Q}{3V_f}=-\frac{2\times2\times10^6}{3\times19053}\approx-70\,\text{A} $$
(negativo porque \( Q>0 \) inductivo corresponde a corriente retrasada, \( i_q<0 \) con la convención Q=-3/2·V·iq).

**Paso 5 — tabla resumen.**

| Magnitud | Valor | Unidad |
|---|---|---|
| Potencia activa \( P \) | 5 | MW |
| Potencia reactiva \( Q \) | 2 | MVAr (inductivo) |
| Potencia aparente \( S \) | 5.385 | MVA |
| Factor de potencia | 0.929 | — |
| Tensión de línea \( V_{LL} \) | 33 | kV |
| Corriente de línea \( I_L \) | 94.3 | A |
| Tensión de fase RMS \( V_f \) | 19.05 | kV |
| Tensión de fase pico \( \hat V_f \) | 26.94 | kV |
| \( V_{dc,min} \) (sinusoidal) | 53.9 | kV |
| \( V_{dc,min} \) (3.er arm.) | 46.7 | kV |
| Referencia \( i_d^* \) | +175 | A |
| Referencia \( i_q^* \) | −70 | A |

**Margen de diseño práctico.** Se suele tomar \( V_{dc}=1.1\times V_{dc,min} \) para tener margen ante caídas de red y pérdidas en el filtro. La corriente nominal del IGBT debe soportar el pico: \( \hat I_L=\sqrt2\times94.3\approx133\,\text{A} \); con sobredimensionado del 20 % → módulo de 160 A.

## Cuándo y por qué se usa
Es el marco de todo el sistema eléctrico de potencia y de los convertidores de red. Las tensiones
nominales y los cálculos de potencia/corriente parten siempre de estas relaciones.

## Procedimiento (genérico)
1. Identifica conexión (Y/Δ) y si hay neutro.
2. Pasa a fasores y usa el **equivalente monofásico** (una fase) si está equilibrado.
3. Aplica relaciones línea-fase para tensiones/corrientes.
4. Para desequilibrio o falta, usa [[componentes-simetricas]].

## Ejemplo de aplicación real
**Problema:** Parque eólico de \( P=10\,\text{MW} \) a \( V_{LL}=33\,\text{kV} \), \( \cos\phi=0.95\,\text{retraso} \). Calcular corriente de línea, potencia reactiva y tensión de fase pico para dimensionar el convertidor.

Corriente de línea: \( I_L=P/(\sqrt{3}\,V_{LL}\cos\phi)=10\times10^6/(\sqrt{3}\times33000\times0.95)\approx184\,\text{A} \). Potencia reactiva inductiva: \( Q=P\tan(\arccos0.95)\approx3.29\,\text{MVAr} \). Potencia aparente: \( S=P/\cos\phi\approx10.53\,\text{MVA} \). Tensión de fase pico (para diseñar la modulación del VSC): \( \hat V_f=33000\sqrt{2}/\sqrt{3}\approx26.9\,\text{kV} \). Con estos datos se dimensiona el condensador del bus DC y se fijan las referencias \( i_d^*,i_q^* \) del control.

## Ejemplo de código
```python
import numpy as np
Vll = 690.0
Vf_pico = Vll*np.sqrt(2/3)             # pico de fase (amplitud)
P = np.sqrt(3)*Vll*IL*np.cos(phi)      # potencia activa trifásica
```

## Parámetros y valores típicos
Tensiones de línea típicas en convertidores: 400 V, 690 V (BT); frecuencia 50/60 Hz. Convención de
amplitud de fase: \( \hat V_{fase}=V_{LL}\sqrt{2/3} \).

## Errores comunes
- Confundir tensión de línea con tensión de fase (factor \( \sqrt3 \)).
- Mezclar valores de pico y RMS.
- Suponer suma nula con cargas o red desequilibradas (entonces circula homopolar).
- Aplicar el equivalente monofásico a un sistema desequilibrado sin hacer la conversión a componentes simétricas.
- Olvidar que la conversión Δ→Y divide la impedancia por 3 (no por \( \sqrt3 \)).

## Conceptos relacionados
- [[potencia-ac-fasores]] · [[marco-dq]] · [[sistema-por-unidad]] · [[componentes-simetricas]] · [[transformada-clarke]]

## Referencias
- Chapman, *Máquinas Eléctricas*.
- Yazdani, Iravani, 2010.
- Kundur, *Power System Stability and Control*, cap. 4.
