---
titulo: Resonancia en circuitos RLC
slug: resonancia-rlc
categoria: fisica-modelado
tipo: concepto
nivel: basico
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [entender la resonancia LC, el factor de calidad y por qué hay que amortiguarla]
tags: [resonancia, rlc, factor-calidad, ancho-de-banda, amortiguamiento, filtro, basico]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-07-01
relacionados: [filtro-lcl, impedancia-reactancia, diagrama-bode, respuesta-segundo-orden]
referencias:
  - "Sedra & Smith, Microelectronic Circuits"
  - "Erickson & Maksimovic, Fundamentals of Power Electronics"
---

## Definición
Siempre que en un circuito coexisten una inductancia L (que almacena energía en forma de corriente) y una capacidad C (que la almacena en forma de tensión), existe una frecuencia a la que sus reactancias se cancelan y la energía oscila entre ambas: la frecuencia de resonancia. Cerca de ella, una excitación pequeña produce tensiones o corrientes grandes (un pico de ganancia), tanto más agudo cuanto menor sea la resistencia que disipa la energía.

## Dónde aparece (contexto genérico)
La resonancia RLC no es de ningún componente concreto: surge en cualquier lazo donde un elemento inductivo y uno capacitivo intercambian energía con poca disipación. Da igual que la L sea la bobina de un filtro, la inductancia de un cable o la de dispersión de un transformador, y que la C sea un condensador de filtro, la capacidad de un cable largo o la de un banco. Lo único que fija la resonancia es el par L–C que forman y la resistencia en serie con ellos. Por eso este desarrollo se aplica igual al filtro LCL, a una línea con compensación serie, o a un bus DC con su condensador.

## Desarrollo 1 — frecuencia de resonancia (versión reducida, sin pérdidas)
**Paso 1 — las dos reactancias.** La reactancia de la bobina crece con la frecuencia, \( X_L=\omega L \); la del condensador decrece, \( X_C=1/(\omega C) \). En un lazo LC la reactancia total es \( X_L-X_C \).

**Paso 2 — condición de resonancia.** La resonancia es donde las dos reactancias se cancelan (reactancia total nula), es decir donde el circuito deja de comportarse como inductivo o capacitivo y solo queda la resistencia:

$$ \omega L = \frac{1}{\omega C} $$

**Paso 3 — despejar.** Multiplicando por \( \omega \) y dividiendo por \( L \):

$$ \omega_0^2=\frac{1}{LC} \;\Rightarrow\; \omega_0=\frac{1}{\sqrt{LC}} \;\Rightarrow\; f_0=\frac{1}{2\pi\sqrt{LC}} $$

**Paso 4 — qué pasa en resonancia.** Un RLC serie presenta impedancia mínima (igual a R, porque las reactancias se anulan): a f0 deja pasar la máxima corriente. Un RLC paralelo presenta impedancia máxima: a f0 bloquea. Son la misma resonancia vista desde la conexión serie o paralelo.

## Desarrollo 2 — factor de calidad y amortiguamiento (versión completa, con R)
Sin despreciar la resistencia, conviene cuantificar cómo de agudo es el pico. La impedancia del RLC serie completa es Z(s) = R + s·L + 1/(s·C).

**Factor de calidad Q.** Mide la energía almacenada frente a la disipada por ciclo; equivale a la relación entre la reactancia en resonancia y la resistencia:

$$ Q=\frac{\omega_0 L}{R}=\frac{1}{R}\sqrt{\frac{L}{C}} $$

El término \( \sqrt{L/C} \) es la impedancia característica del tanque: \( Q \) es esa impedancia dividida por \( R \). \( Q \) alto (R pequeña) significa poca disipación → pico agudo; \( Q \) bajo (R grande) → pico suave.

**Amortiguamiento \( \zeta \) y de dónde sale \( Q=1/(2\zeta) \).** \( \zeta \) y \( Q \) miden lo mismo (el amortiguamiento del par de polos) con dos definiciones distintas; al juntarlas, su producto resulta ser exactamente \( 1/2 \). Para verlo se parte del denominador de la respuesta del RLC serie. Dividiendo \( Z(s)=R+sL+1/(sC) \) por \( L \), la ecuación característica es:

$$ s^2 + \frac{R}{L}\,s + \frac{1}{LC} = 0 $$

Comparándola término a término con la forma canónica de segundo orden \( s^2+2\zeta\omega_0 s+\omega_0^2=0 \):

$$ \omega_0^2=\frac{1}{LC}\ \checkmark, \qquad 2\zeta\omega_0=\frac{R}{L} \;\Rightarrow\; \zeta=\frac{R}{2L\,\omega_0}=\frac{R}{2L}\sqrt{LC}=\frac{R}{2}\sqrt{\frac{C}{L}} $$

Y como \( Q=(1/R)\sqrt{L/C} \), el producto de ambos da \( 1/2 \):

$$ \zeta\,Q=\frac{R}{2}\sqrt{\frac{C}{L}}\cdot\frac{1}{R}\sqrt{\frac{L}{C}}=\frac{1}{2} \;\Rightarrow\; \boxed{\;\zeta=\frac{1}{2Q}\;} $$

**Lectura energética equivalente.** \( Q=2\pi\,\dfrac{\text{energía almacenada}}{\text{energía disipada por ciclo}} \). La amplitud de la oscilación decae como \( e^{-\zeta\omega_0 t} \), luego la energía (\( \propto \) amplitud\( ^2 \)) como \( e^{-2\zeta\omega_0 t} \); en un ciclo (\( T\approx2\pi/\omega_0 \)) se pierde una fracción \( \approx 2\zeta\omega_0 T=4\pi\zeta \), de donde \( Q=2\pi/(4\pi\zeta)=1/(2\zeta) \), el mismo resultado.

Sin resistencia (\( R\to0 \)) se tiene \( Q\to\infty \) y \( \zeta\to0 \): el pico es teóricamente infinito y la oscilación, no amortiguada. Con \( R \) real el pico es finito.

**Ancho de banda.** El pico no solo sube con \( Q \), también se estrecha: el ancho de banda a \( -3 \) dB es

$$ \Delta f=\frac{f_0}{Q} $$

es decir, doblar \( Q \) duplica la altura del pico y reduce a la mitad su anchura. Esta es la relación clave para el diseño del amortiguamiento.

**Caso de estudio: efecto de Q en la respuesta.** La gráfica de la izquierda muestra el mínimo de impedancia del RLC serie (más profundo y agudo si R baja); la de la derecha, el pico de resonancia para varios Q: su altura es aproximadamente Q y su anchura f0/Q.

<div class="cfig"><img src="figuras/resonancia-rlc-zf.png" alt="Izquierda: impedancia del RLC serie para Q alto y bajo. Derecha: pico de resonancia para varios Q mostrando altura proporcional a Q y anchura f0/Q"><div class="cap">Izquierda: |Z| del RLC serie cae a un mínimo (=R) en f₀, más agudo cuanto menor es R (mayor Q). Derecha: el pico de resonancia tiene altura ≈ Q y anchura ≈ f₀/Q; a más Q, pico más alto y estrecho (menos amortiguado).</div></div>

## 1 — Resonancia paralela: impedancia máxima y dualidad con la serie

**El circuito RLC paralelo.** R, L y C están conectados en paralelo entre los mismos dos nodos: la misma tensión cae sobre los tres. Una fuente de corriente externa alimenta la combinación. La variable observable es la tensión en los bornes o la corriente por cada rama.

**Paso 1 — admitancia total.** La admitancia de cada rama se suma en paralelo:

$$ Y(s) = \frac{1}{R} + sC + \frac{1}{sL} $$

La impedancia de entrada es el recíproco:

$$ Z_{par}(s) = \frac{1}{Y(s)} = \frac{sL}{s^2LC + \frac{sL}{R} + 1} $$

**Paso 2 — resonancia paralela.** En resonancia las admitancias de L y C se cancelan mutuamente:

$$ sC + \frac{1}{sL}\bigg|_{s=j\omega_0} = j\omega_0 C - \frac{j}{\omega_0 L} = 0 \;\Rightarrow\; \omega_0 = \frac{1}{\sqrt{LC}} $$

La misma condición que la resonancia serie. En \( \omega_0 \), la admitancia total se reduce a \( 1/R \), es decir \( Z_{par}(\omega_0)=R \): **la impedancia es máxima** (igual a R). La fuente de corriente "ve" la mayor impedancia posible; con R grande, la impedancia en resonancia es muy elevada.

**Paso 3 — factor Q para el paralelo.** En el paralelo, la energía se almacena en L y C y se disipa en R. El Q se define igual (energía almacenada / disipada por ciclo) pero la expresión toma la forma dual:

$$ Q_{par} = \frac{R}{\omega_0 L} = R\sqrt{\frac{C}{L}} $$

Comparando con el serie \( Q_{ser} = \frac{\omega_0 L}{R} = \frac{1}{R}\sqrt{\frac{L}{C}} \): en el serie R está en el denominador (más R → menos Q → menos pico); en el paralelo R está en el numerador (más R → más Q → pico más agudo). La física es dual: en el serie una R grande amortigua la corriente; en el paralelo una R grande reduce la fuga de energía y acentúa la resonancia.

**Paso 4 — tabla de dualidad completa.**

| Magnitud | RLC serie | RLC paralelo |
|---|---|---|
| Excitación | tensión \( v_s \) | corriente \( i_s \) |
| Respuesta en resonancia | corriente máxima (\( Z = R_{min} \)) | tensión máxima (\( Z = R_{max} \)) |
| Reactancias en resonancia | \( X_L = X_C \), se cancelan en serie | \( B_L = B_C \), se cancelan en paralelo |
| Factor Q | \( Q = \omega_0 L / R \) | \( Q = R / (\omega_0 L) = R\sqrt{C/L} \) |
| \( \zeta \) | \( \zeta = R/(2\omega_0 L) \) | \( \zeta = 1/(2R\omega_0 C) = \frac{1}{2}\sqrt{L/C}/R \) |
| Ancho de banda | \( \Delta\omega = R/L = \omega_0/Q \) | \( \Delta\omega = 1/(RC) = \omega_0/Q \) |

**Ejemplo numérico.** Con \( L=2\,\text{mH} \), \( C=20\,\mu\text{F} \):

$$ f_0 = \frac{1}{2\pi\sqrt{2\times10^{-3}\cdot20\times10^{-6}}} = \frac{1}{2\pi\cdot200\times10^{-6}} \approx 796\,\text{Hz} $$

Con \( R_{ser}=10\,\Omega \) en serie:
\( Q_{ser} = \omega_0 L / R_{ser} = (2\pi\cdot796\cdot2\times10^{-3})/10 \approx 1.0 \) → amortiguado.

Con \( R_{par}=1\,\text{k}\Omega \) en paralelo:
\( Q_{par} = R_{par}/(\omega_0 L) = 1000/(2\pi\cdot796\cdot2\times10^{-3}) \approx 100 \) → muy agudo.

<div class="cfig"><img src="figuras/resonancia-rlc-analisis.png" alt="Cuatro paneles: serie vs paralelo, amortiguamiento pasivo, fres/far vs L_red, activo vs pasivo"><div class="cap">Panel (a): |Z| del RLC serie (mínimo en f₀) y paralelo (máximo en f₀) — dualidad visual. Paneles (b)–(d): amortiguamiento pasivo (Rd en Cf), efecto de L_red en las frecuencias de resonancia, y comparativa activo vs pasivo para el filtro LCL.</div></div>

## 2 — Amortiguamiento pasivo: resistencia serie vs paralelo

El amortiguamiento pasivo es la forma más directa de limitar el pico de resonancia: se añade una resistencia que disipa la energía en la frecuencia de resonancia. La pregunta de dónde colocarla depende de qué tipo de pico se quiere suprimir.

**Resistencia serie con C (el caso del filtro LCL).** En el filtro LCL la resonancia surge del intercambio de energía entre \( L_1 \), \( L_2 \) y \( C_f \). Si se pone una resistencia \( R_d \) en serie con \( C_f \):

- A la frecuencia fundamental (50 Hz): la reactancia de \( C_f \) es grande → casi toda la corriente evita la rama del condensador → \( R_d \) casi no ve corriente → pérdidas ínfimas.
- En resonancia (\( f_{res}\approx1{,}1\,\text{kHz} \)): la corriente del condensador es grande → \( R_d \) disipa energía → pico aplastado.

La impedancia del shunt es \( Z_{sh}(s) = R_d + 1/(sC_f) \). La FDT de corriente de red \( i_{L2}/v_i \) del LCL con amortiguamiento pasivo es (modelo simplificado):

$$ H_{LCL,Rd}(s) = \frac{Z_{par}(s)}{(R_1 + sL_1 + Z_{par}(s))\cdot sL_2} $$

donde \( Z_{par}(s) = Z_{sh}(s) \cdot sL_2 / (Z_{sh}(s)+sL_2) \). La resonancia se convierte en un pico de altura aproximada:

$$ Q_d \approx \frac{1}{\omega_{res}\,C_f\,R_d} $$

lo que da \( \zeta_d \approx \omega_{res}\,C_f\,R_d / 2 \).

**Resistencia paralelo con L.** Si en cambio se pone \( R_d \) en paralelo con una de las inductancias, la corriente resonante que circula por la bobina se desvía parcialmente por \( R_d \). Efecto dual: es más efectivo cuando la corriente de la inductancia es la variable problemática.

**Valor óptimo de \( R_d \).** El compromiso es entre amortiguar suficiente y no atenuar la fundamental ni crear pérdidas excesivas. Una regla empírica muy usada es:

$$ R_{d,opt} = \frac{1}{3\,\omega_{res}\,C_f} $$

Con esta elección se obtiene \( Q_d \approx 3 \), \( \zeta_d \approx 1/6 \approx 0{,}17 \): suficiente para que el pico quede por debajo de 0 dB referenciado a la ganancia de paso.

**Cuantificación de pérdidas.** La corriente pico en \( C_f \) en la frecuencia fundamental es \( \hat{i}_{Cf} = \hat{v}_i / |Z_{sh}(j\omega_1)| \approx \hat{v}_i \cdot \omega_1 C_f \) (ya que \( R_d \ll 1/(\omega_1 C_f) \) si \( R_d = R_{d,opt} \)). Las pérdidas por efecto Joule en \( R_d \) son:

$$ P_{R_d} = \frac{1}{2}\,R_d\,\hat{i}_{Cf}^2 \approx \frac{R_d}{2}\,(\hat{v}_i\,\omega_1 C_f)^2 $$

**Ejemplo numérico.** Con \( L_1=2\,\text{mH} \), \( L_2=0{,}5\,\text{mH} \), \( C_f=15\,\mu\text{F} \):

$$ L_{eq}=\frac{L_1 L_2}{L_1+L_2}=\frac{2\times0{,}5}{2{,}5}\,\text{mH}=0{,}4\,\text{mH} $$

$$ f_{res}=\frac{1}{2\pi\sqrt{0{,}4\times10^{-3}\cdot15\times10^{-6}}} \approx 1{,}030\,\text{kHz} $$

$$ R_{d,opt}=\frac{1}{3\cdot2\pi\cdot1030\cdot15\times10^{-6}} \approx 3{,}44\,\Omega $$

Con \( \hat{v}_i = 325\,\text{V} \) (pico de tensión del convertidor a 50 Hz) y \( \omega_1=2\pi\cdot50 \):

$$ P_{R_d}\approx\frac{3{,}44}{2}\cdot(325\cdot314\cdot15\times10^{-6})^2\approx3{,}44/2\cdot(1{,}53)^2\approx4\,\text{W} $$

Prácticamente despreciable (< 0,001% de la potencia nominal). En sistemas de mayor potencia o con condensadores más grandes el término crece proporcionalmente a \( C_f^2 \).

## 3 — Amortiguamiento activo: sin pérdidas, por realimentación

El amortiguamiento activo consigue la misma supresión del pico de resonancia que el pasivo, pero sin añadir resistencias físicas: el convertidor mismo actúa como una resistencia virtual usando la información de la corriente del condensador.

**Idea fundamental.** En el filtro LCL, la corriente \( i_{Cf} \) que circula por el condensador es la que "alimenta" la resonancia. Si se mide \( i_{Cf} \) y se añade a la referencia de tensión del convertidor una componente proporcional a ella:

$$ v_i^* = v_i^*_{CC} + K_{ad}\,i_{Cf} $$

el convertidor "ve" esa corriente y la contrarresta. Equivalentemente, el lazo de control introduce un término de amortiguamiento que imita el efecto de una resistencia \( K_{ad} \) en serie con \( C_f \), pero sin disipación real.

**Paso 1 — el modelo.** Con amortiguamiento activo ideal (sin retardo), la FDT de \( i_{L2}/v_i \) del LCL se transforma como si \( R_d = K_{ad} \) estuviera en serie con \( C_f \):

$$ H_{act}(s) = H_{LCL,Rd}(s)\bigg|_{R_d = K_{ad}} $$

Esto es exactamente el mismo resultado que el amortiguamiento pasivo con \( R_d = K_{ad} \): la física es equivalente, solo que sin pérdidas.

**Paso 2 — el retardo digital.** En una implementación discreta con período de muestreo \( T_s \), la acción de amortiguamiento activo llega al convertidor con un retardo de \( 1{,}5\,T_s \) (un semiciclo de PWM más el retardo de cálculo). Este retardo introduce una fase que hace que la resistencia virtual \( K_{ad} \) sea efectiva solo hasta cierta frecuencia:

$$ Z_{ad}(j\omega) = K_{ad}\,e^{-j1{,}5T_s\omega} $$

La parte real de \( Z_{ad} \) (que es la que amortigua) decae al crecer \( \omega \):

$$ \text{Re}\{Z_{ad}(j\omega)\} = K_{ad}\cos(1{,}5\,T_s\,\omega) $$

En la frecuencia de resonancia \( \omega_{res} \), el ángulo de retardo es \( 1{,}5\,T_s\,\omega_{res} \). Si este ángulo supera \( \pi/2 \), la parte real se vuelve negativa: el amortiguamiento activo excita en vez de amortiguar.

**Paso 3 — límite de \( K_{ad} \).** Para garantizar amortiguamiento positivo en toda la banda útil:

$$ 1{,}5\,T_s\,\omega_{res} < \frac{\pi}{2} \;\Rightarrow\; f_{res} < \frac{1}{6\,T_s} $$

Con \( T_s = 100\,\mu\text{s} \) (conmutación a 10 kHz): \( f_{res} < 1667\,\text{Hz} \). Con \( f_{res} \approx 1\,\text{kHz} \) del proyecto 01, el ángulo de retardo es \( 1{,}5\cdot10^{-4}\cdot2\pi\cdot1000 \approx 54° \) → \( \cos(54°) \approx 0{,}59 \): el amortiguamiento efectivo es un 41% menor que el nominal. Hay que compensar subiendo \( K_{ad} \).

**Paso 4 — el \( \zeta \) resultante.** Con el retardo, el amortiguamiento activo equivale a \( R_{d,eff} = K_{ad}\cos(1{,}5\,T_s\,\omega_{res}) \). El \( \zeta \) resultante es el mismo que el del amortiguamiento pasivo con \( R_{d,eff} \):

$$ \zeta_{AD} \approx \frac{\omega_{res}\,C_f\,K_{ad}\cos(1{,}5\,T_s\,\omega_{res})}{2} $$

**Ejemplo: proyecto 01.** Con \( K_{ad}=6\,\Omega \), \( f_{res}=1{,}030\,\text{kHz} \), \( T_s=100\,\mu\text{s} \), \( C_f=15\,\mu\text{F} \):

$$ \zeta_{AD} \approx \frac{2\pi\cdot1030\cdot15\times10^{-6}\cdot6\cdot\cos(1{,}5\cdot6{,}47\times10^{-1})}{2} \approx \frac{0{,}582\cdot0{,}796}{2} \approx 0{,}23 $$

Suficiente para estabilidad práctica (\( \zeta > 0{,}1 \)).

## 4 — Frecuencia de resonancia con red: el efecto de \( L_{red} \)

Cuando el filtro LCL se conecta a una red que tiene inductancia (transformador, cable largo, red débil), la inductancia de red \( L_{red} \) se añade en serie con \( L_2 \), formando una inductancia efectiva \( L_{2,eff} = L_2 + L_{red} \).

**Paso 1 — la nueva frecuencia de resonancia.** Con \( L_{2,eff} \) en lugar de \( L_2 \):

$$ L_{eq,D} = \frac{L_1\,L_{2,eff}}{L_1+L_{2,eff}}, \qquad f_{res,D} = \frac{1}{2\pi\sqrt{L_{eq,D}\,C_f}} $$

Como \( L_{2,eff} > L_2 \), la inductancia equivalente paralelo crece → \( f_{res,D} \) baja respecto al caso sin red.

**Paso 2 — la antirresonancia.** El filtro LCL con red tiene también un cero (antirresonancia) en:

$$ f_{ar,D} = \frac{1}{2\pi\sqrt{L_{2,eff}\,C_f}} $$

Esta frecuencia corresponde al cero de transmisión: en \( f_{ar,D} \), la rama \( L_{2,eff}C_f \) resuena internamente y no deja pasar señal hacia la red.

**Paso 3 — las dos frecuencias se acercan.** La relación entre resonancia y antirresonancia es:

$$ \frac{f_{res,D}}{f_{ar,D}} = \sqrt{\frac{L_{2,eff}}{L_{eq,D}}} = \sqrt{1+\frac{L_{2,eff}}{L_1}} $$

Cuando \( L_{red} \to \infty \), \( L_{2,eff}/L_1 \to \infty \) y la relación crece; sin embargo, como \( L_{eq,D} \to L_1 \), ambas frecuencias se estabilizan: \( f_{res,D} \to 1/(2\pi\sqrt{L_1 C_f}) \) y \( f_{ar,D} \to 0 \). En la práctica, con \( L_{red} \) moderada (1–5 mH) las dos frecuencias se desplazan hacia abajo y se acercan entre sí, lo que complica el amortiguamiento.

**Paso 4 — implicación para el amortiguamiento.** Un \( K_{ad} \) diseñado para \( f_{res} = 1\,\text{kHz} \) puede ser insuficiente si en red débil la resonancia cae a 600 Hz (el coseno de retardo mejora, pero el \( \zeta \) requerido para estabilidad también cambia). El caso peor es el de red débil (red fuerte → \( L_{red}\approx0 \)).

**Tabla numérica.** Parámetros: \( L_1=2\,\text{mH} \), \( L_2=0{,}5\,\text{mH} \), \( C_f=15\,\mu\text{F} \).

| \( L_{red} \) | \( L_{2,eff} \) | \( f_{res,D} \) | \( f_{ar,D} \) | \( \zeta_{req} \) (aprox.) |
|---|---|---|---|---|
| 0 mH | 0,5 mH | 1 030 Hz | 2 910 Hz | 0,17 |
| 1 mH | 1,5 mH | 816 Hz | 1 682 Hz | 0,17 |
| 2 mH | 2,5 mH | 713 Hz | 1 300 Hz | 0,17 |
| 5 mH | 5,5 mH | 563 Hz | 877 Hz | 0,17 |

El \( \zeta_{req} \) mínimo es el mismo (fijado por el criterio de estabilidad del lazo de corriente), pero el \( K_{ad} \) necesario para alcanzarlo crece con la caída de \( f_{res,D} \) porque \( \omega_{res,D}\,C_f \) baja.

## 5 — Diseño iterativo del amortiguamiento: de spec a \( R_d \) o \( K_{ad} \)

El objetivo del diseño es llegar a una configuración de amortiguamiento que cumpla las especificaciones de margen de estabilidad sin comprometer las pérdidas ni la atenuación armónica.

**Especificación.** Pico de resonancia en \( |H_{LCL}(j2\pi f_{res})| < 0\,\text{dB} \) (referido a la ganancia de baja frecuencia), \( \zeta > 0{,}1 \), pérdidas < 100 W.

**Opción 1: amortiguamiento pasivo.**

Con la regla \( R_d = 1/(3\omega_{res}C_f) \):

$$ R_d = \frac{1}{3\cdot2\pi\cdot1030\cdot15\times10^{-6}} \approx 3{,}44\,\Omega $$

\( Q = 3 \), \( \zeta = 1/6 \approx 0{,}17 \) ✓. Pérdidas: \( \approx 4\,\text{W} \) (calculadas en §2). El pico queda por debajo de 10 dB sobre la ganancia DC → la atenuación del LCL funciona normalmente a partir de \( 2f_{res} \).

**Opción 2: amortiguamiento activo, iteraciones.**

*Iteración 0 — \( K_{ad}=3\,\Omega \):*

$$ \zeta_{AD} \approx \frac{2\pi\cdot1030\cdot15\times10^{-6}\cdot3\cdot0{,}796}{2} \approx 0{,}116 $$

Cumple el mínimo (\( \zeta > 0{,}1 \)) pero con poco margen. Ante perturbaciones o variación de \( f_{res} \) con la red → insuficiente.

*Iteración 1 — \( K_{ad}=6\,\Omega \):*

$$ \zeta_{AD} \approx 0{,}23 $$

\( \zeta > 0{,}1 \) con margen ✓. Sin pérdidas adicionales. El margen de fase del lazo de corriente no se degrada significativamente porque el amortiguamiento activo no modifica la ganancia en el cruce de fase del lazo principal.

*Iteración 2 — \( K_{ad}=10\,\Omega \):*

$$ \zeta_{AD} \approx 0{,}39 $$

Amortiguamiento excelente, pero la retracción de fase del término \( K_{ad}\,e^{-j1{,}5T_s s} \) empieza a afectar el margen de fase del lazo de corriente en \( f_{ci}=1\,\text{kHz} \): reducción de \( \approx 8° \). Aceptable si el PM original es \( >50° \).

**Tabla de iteraciones.**

| Configuración | \( R_d \) o \( K_{ad} \) | \( \zeta \) | Pérdidas | PM lazo i | Veredicto |
|---|---|---|---|---|---|
| Sin amortiguamiento | — | \( \approx 0 \) | 0 W | nominal | ✗ inestable |
| Pasivo \( R_{d,opt} \) | 3,44 Ω | 0,17 | 4 W | nominal | ✓ |
| Activo It.0 | 3 Ω | 0,12 | 0 W | −1° | marginal |
| Activo It.1 | 6 Ω | 0,23 | 0 W | −3° | ✓ preferido |
| Activo It.2 | 10 Ω | 0,39 | 0 W | −8° | ✓ si PM > 50° |

La elección final es \( K_{ad}=6\,\Omega \) como equilibrio entre amortiguamiento y margen de fase.

## Relación con el filtro LCL
El filtro LCL es un caso de resonancia con dos inductancias: \( L_1 \) y \( L_2 \) resuenan contra \( C_f \), y el papel de \( L \) en las fórmulas lo hace la inductancia equivalente paralelo \( L_{eq}=L_1 L_2/(L_1+L_2) \), de modo que \( f_{res}=1/(2\pi\sqrt{L_{eq} C_f}) \). El factor \( Q \) y el amortiguamiento se calculan igual. La derivación completa está en [[filtro-lcl]].

## Cuándo y por qué se usa
Aparece en todo filtro LC/LCL de convertidor y en cualquier lazo L–C de la red. Su resonancia, si no se amortigua, hace inestable cualquier lazo de control rápido que la excite. Entender f0 y Q es el paso previo a diseñar el amortiguamiento (pasivo con una resistencia, o activo por realimentación).

## Procedimiento de diseño (genérico)
1. Identifica el par L y C y calcula f0.
2. Calcula Q (o zeta) con la resistencia presente.
3. Si Q es alto (poco amortiguado), añade amortiguamiento: resistencia serie/paralelo (pasivo, con pérdidas) o realimentación (activo, sin pérdidas).
4. Comprueba si hay inductancia de red y recalcula f0 con \( L_{2,eff}=L_2+L_{red} \) (caso peor).
5. Coloca f0 lejos del ancho de banda de control y por debajo de fsw/2.
6. Itera Rd o Kad hasta que \( \zeta > 0{,}1 \) con margen de fase aceptable en el lazo de corriente.

## Ejemplo de código
```python
import numpy as np
L, C, R = 2e-3, 20e-6, 0.1
f0 = 1/(2*np.pi*np.sqrt(L*C))          # frecuencia de resonancia
Q  = (1/R)*np.sqrt(L/C)                 # factor de calidad (serie)
zeta = 1/(2*Q)                          # amortiguamiento
bw  = f0/Q                              # ancho de banda a -3 dB

# Resonancia paralelo: Q = R*sqrt(C/L)
R_par = 1e3
Q_par = R_par * np.sqrt(C/L)

# Amortiguamiento pasivo optimo
wres = 2*np.pi*f0
Cf = 15e-6
Rd_opt = 1/(3*wres*Cf)                  # regla empirica

# Amortiguamiento activo con retardo
Kad = 6.0; Ts = 100e-6
zeta_AD = wres*Cf*Kad*np.cos(1.5*Ts*wres)/2
```

## Parámetros y valores típicos
f0 de un LCL: cientos de Hz a pocos kHz (≈1.1 kHz en el proyecto 01). zeta natural casi nulo; tras amortiguamiento activo se lleva a zeta ≈ 0.2–0.4 (Q ≈ 1.3–2.5). Rd_opt ≈ 0.2–5 Ω dependiendo de Cf y fres. Kad_típico ≈ 3–10 Ω. fres baja un 15–40% en red débil (Lred = 1–5 mH).

## Errores comunes
- Dejar la resonancia sin amortiguar y subir el lazo de corriente → inestabilidad.
- Confundir resonancia serie (mínimo de impedancia) con paralelo (máximo).
- Situar f0 demasiado cerca del ancho de banda del control.
- Olvidar que la inductancia de red se suma a L2 y baja f0 (caso peor en red débil).
- Con amortiguamiento activo: no comprobar que \( f_{res} < 1/(6T_s) \) para que el retardo no invierta la fase del amortiguamiento.
- Calcular Q del paralelo con la fórmula del serie (o viceversa): R está en posición opuesta.

## Uso en proyectos
- 01 / 02 (filtro LCL): la resonancia a ~1.1 kHz aparece como un par de polos poco amortiguados; se trata con amortiguamiento activo (realimentación de la corriente del condensador), Kad=6 Ω → ζ≈0.23.

## Conceptos relacionados
- [[filtro-lcl]] · [[impedancia-reactancia]] · [[diagrama-bode]] · [[respuesta-segundo-orden]]

## Referencias
- Sedra & Smith, Microelectronic Circuits.
- Erickson & Maksimovic, Fundamentals of Power Electronics.
