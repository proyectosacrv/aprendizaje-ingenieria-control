---
titulo: "Convertidor fuente de tensión (VSC): topología, PWM, modelo promediado y análisis completo"
slug: convertidor-vsc
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance]
objetivos: [entender la topología del convertidor controlado por tensión, cómo sintetiza tensión por PWM, modelo promediado en espacio de estados, balance de potencia DC↔AC, rizado, tiempo muerto, dimensionado de Vdc y límites del promediado]
tags: [vsc, inversor, dos-niveles, pwm, ciclo-de-trabajo, modelo-promediado, averaging, conmutado, modulacion, modelado, espacio-de-estados, dq, rizado, tiempo-muerto, balance-potencia, dimensionado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-01
relacionados: [topologias-multinivel, semiconductores-potencia, filtro-lcl, marco-dq, sistema-trifasico, medicion-impedancia-inyeccion, potencia-instantanea-dq]
referencias:
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
  - "Mohan, Undeland, Robbins, Power Electronics, Wiley"
  - "Erickson, Maksimovic, Fundamentals of Power Electronics, Springer (averaging)"
  - "Holmes, Lipo, Pulse Width Modulation for Power Converters, IEEE Press 2003"
---

## Definición

El convertidor fuente de tensión (VSC, voltage-sourced converter) es la familia de convertidores que parten de un bus DC de tensión fija (un condensador) y sintetizan tensiones AC controladas conmutando interruptores entre niveles fijos. Esta ficha cubre las cuatro cosas inseparables para entenderlo y usarlo: su topología (el puente de dos niveles), cómo impone la tensión que pide el control (modulación SPWM), cómo se modela para diseño y análisis (modelo promediado y su linealización en dq), y los fenómenos prácticos que determinan el dimensionado real: balance de potencia DC↔AC, rizado de corriente, tiempo muerto y elección del bus DC con margen. Las variantes multinivel están en [[topologias-multinivel]] y los semiconductores en [[semiconductores-potencia]].

## Topología

Cada una de las tres ramas (a, b, c) conecta su salida a \(+V_{dc}\) o a \(0\) según cuál de sus dos interruptores conduce —nunca los dos a la vez, de ahí el **tiempo muerto**. La tensión de fase respecto al negativo del bus depende del ciclo de trabajo \(d_x \in [0,1]\):

\[ v_{x\_N} = d_x \cdot V_{dc} \]

La tensión de fase respecto al neutro virtual de la carga (punto equidistante de las tres ramas) elimina el modo común:

\[ v_{xn} = v_{x\_N} - \frac{1}{3}\sum_k v_{k\_N} \]

El índice de modulación \(m = \hat{V}_{fase}/(V_{dc}/2)\) llega a 1 en SPWM lineal y a \(2/\sqrt{3}\approx1{,}15\) con inyección de tercer armónico o SVPWM. Del lado DC, el balance de potencia es: \(V_{dc}\,I_{dc} = \sum_x v_{xn}\,i_x\).

<div class="cfig"><img src="figuras/convertidor-vsc-rama.png" alt="una rama del VSC de dos niveles"><div class="cap">Una de las tres ramas idénticas (a, b, c): S₁ cierra la salida a +Vdc y S₂ la cierra a 0. Nunca los dos a la vez: el intervalo de tiempo muerto tdead protege contra el cortocircuito del bus DC. Las tres ramas juntas forman el VSC trifásico de 2 niveles.</div></div>

## Modulación PWM (cómo impone la tensión)

PWM es la técnica con la que el convertidor genera la tensión media que pide el control conmutando entre niveles fijos. El ciclo de trabajo \(d\) (entre 0 y 1) es la fracción del periodo de conmutación en que el interruptor superior está cerrado; la tensión media en un periodo de conmutación es:

\[ \langle v_{x\_N} \rangle_{T_{sw}} = d_x \cdot V_{dc} \]

Comparando una señal moduladora \(m(t)\) (la referencia senoidal del control) con una portadora triangular a frecuencia \(f_{sw}\) se generan los pulsos: cuando la moduladora supera la portadora, el interruptor superior conduce. El valor medio de la tensión de salida sigue a la moduladora. La conmutación introduce armónicos alrededor de \(f_{sw}\) y sus múltiplos, que el filtro LC de salida atenúa.

<div class="cfig"><img src="figuras/convertidor-vsc-analisis.png" alt="análisis extendido del VSC: PWM, rizado, impedancia y mapa de operación"><div class="cap">Panel (a): portadora triangular, moduladora senoidal (m=0.85), tensión conmutada y tensión promediada durante 3 periodos de conmutación. Panel (b): rizado pico-pico de corriente en L₁ vs L₁ para tres frecuencias de conmutación. Panel (c): impedancia de salida del modelo promediado frente al conmutado; la divergencia aparece cerca de f_sw. Panel (d): mapa de operación en el plano m vs Vdc normalizado, con las zonas lineal, sobremodulación y saturación.</div></div>

## Modelo promediado vs conmutado (cómo se modela)

El **modelo promediado** sustituye la tensión conmutada del puente por su valor medio en cada periodo de conmutación (\(d_x \cdot V_{dc}\) por rama). El **modelo conmutado** simula los interruptores y el PWM reales con su rizado de alta frecuencia.

**Fundamento:** si \(f_{sw}\) es mucho mayor que el ancho de banda de control y que la frecuencia de resonancia del filtro, el promedio del puente reproduce la dinámica útil; el filtro atenúa el rizado de conmutación. El error entre conmutado y promediado es pequeño y de alta frecuencia. Formalmente es el método de **state-space averaging** (Erickson & Maksimovic): se promedia \(\dot{\mathbf{x}} = \mathbf{f}(\mathbf{x}, u)\) sobre el periodo de conmutación.

Para diseñar y analizar (control, impedancia, estabilidad) se usa el promediado: es continuo, linealizable y rápido de simular. El conmutado se reserva para validar y para estudiar fenómenos de conmutación (rizado, pérdidas, EMI).

## 1 — De dónde sale \(\hat{V}_{fase} = m\,V_{dc}/2\) en SPWM

**Paso 1 — qué genera una rama.** Cada rama conmuta su salida entre \(+V_{dc}\) y \(0\) según el ciclo de trabajo \(d_x(t)\in[0,1]\). Su valor medio en un periodo de conmutación es \(v_{x\_N}=d_x V_{dc}\). En SPWM el ciclo de trabajo se modula de forma sinusoidal en torno al punto medio \(1/2\) con amplitud \(m/2\):

$$ d_x(t)=\frac{1}{2}+\frac{m}{2}\cos(\omega_0 t),\qquad 0\le m\le 1 $$

\(m\) es el **índice de modulación**: la amplitud de la moduladora normalizada a la amplitud de la portadora. Con \(m\le 1\) la moduladora no rebasa la portadora → zona lineal.

**Paso 2 — tensión respecto al punto medio del bus DC.** El offset constante \(+V_{dc}/2\) (modo común, igual en las tres ramas) se resta al referenciarnos al punto medio del bus:

$$ v_{x\_0}=v_{x\_N}-\frac{V_{dc}}{2}=\left(d_x-\frac{1}{2}\right)V_{dc}=\frac{m}{2}\cos(\omega_0 t)\,V_{dc} $$

**Paso 3 — leer la amplitud.** La componente fundamental de fase es \(v_{x\_0}(t)=\hat{V}_{fase}\cos(\omega_0 t)\), con:

$$ \boxed{\;\hat{V}_{fase}=m\,\frac{V_{dc}}{2}\;}\qquad\Longrightarrow\qquad m=\frac{\hat{V}_{fase}}{V_{dc}/2} $$

**Paso 4 — por qué el modo común no llega a la carga.** El offset \(V_{dc}/2\) es idéntico en las tres ramas. Al calcular \(v_{an}-v_{bn}\) o cualquier tensión de línea, ese modo común se cancela exactamente. La carga trifásica equilibrada ve únicamente los términos sinusoidales; el modo común no circula por ella.

**Paso 5 — SVPWM y el 15 % extra.** Inyectando un tercer armónico de amplitud \(m/6\) en la moduladora (SVPWM), la envolvente de la moduladora compuesta se reduce a \(m/\sqrt{3}\), lo que permite llegar hasta \(m_{max}=2/\sqrt{3}\approx1{,}155\) antes de recortar la portadora. El tercer armónico es de secuencia cero, también se cancela entre fases y la tensión de línea en la carga crece un 15 % con el mismo \(V_{dc}\).

**Paso 6 — sobremodulación y onda cuadrada.** Si \(m>1\) la moduladora supera la portadora en parte del ciclo de red: la tensión de salida ya no es proporcional a \(m\) (zona no lineal). Los armónicos impares (3.°, 5.°, ...) crecen rápidamente. En el límite \(m\to\infty\), la señal de salida es una **onda cuadrada** de amplitud \(V_{dc}/2\) con componente fundamental de valor pico \((4/\pi)(V_{dc}/2)\approx1{,}273\,V_{dc}/2\). El índice de modulación equivalente de la onda cuadrada es \(m_{sq}=4/\pi\approx1{,}273\), que es el límite superior absoluto de la zona de sobremodulación. La relación entre tensión de salida fundamental y \(m\) se puede aproximar en la sobremodulación (Holmes & Lipo):

$$ \hat{V}_{fase} \approx \frac{V_{dc}}{2}\left[1 + \frac{1}{\pi}\left(\arcsin\frac{2}{m\pi}-\sqrt{1-\left(\frac{2}{m\pi}\right)^2}\right)\right]\quad (1\le m\le4/\pi) $$

En la práctica, diseñar para \(m\le0{,}95\) asegura operación lineal con margen frente a transitorios.

## 2 — El modelo promediado en espacio de estados: derivación completa

### 2.1 Circuito y variables de estado

Tomamos una rama del VSC con un filtro LC de salida (representativo de la rama \(d\) en el marco rotante). Las variables de estado son:

- \(\tilde{i}_L\): corriente en el inductor \(L_1\)
- \(\tilde{v}_C\): tensión en el condensador de filtro \(C_f\)

La tensión promediada que la rama aplica al inductorcircuito es \(v_i = d \cdot V_{dc}\). La red (o la carga) aparece como una fuente de tensión \(v_{pcc}\) al otro lado del circuito.

### 2.2 Ecuaciones diferenciales del circuito (ciclo completo promediado)

Kirchhoff sobre el inductor (tensión = \(L\,\dot{i}\)):

$$ L_1\,\dot{i}_L = v_i - v_C - R_1\,i_L = d\,V_{dc} - v_C - R_1\,i_L $$

Kirchhoff sobre el condensador (corriente = \(C\,\dot{v}\)), suponiendo que la corriente que sale del condensador es \(i_L - i_2\) (donde \(i_2\) es la corriente que va a la red):

$$ C_f\,\dot{v}_C = i_L - i_2 $$

En la forma matricial \(\dot{\mathbf{x}} = A\mathbf{x} + B\mathbf{u}\):

$$ \frac{d}{dt}\begin{bmatrix}i_L\\v_C\end{bmatrix} = \underbrace{\begin{bmatrix}-R_1/L_1 & -1/L_1 \\ 1/C_f & 0\end{bmatrix}}_{\displaystyle A}\begin{bmatrix}i_L\\v_C\end{bmatrix} + \underbrace{\begin{bmatrix}V_{dc}/L_1 & 0 \\ 0 & -1/C_f\end{bmatrix}}_{\displaystyle B}\begin{bmatrix}d\\i_2\end{bmatrix} $$

Esto es válido mientras el promediado sea aplicable (\(f_{sw}\gg f_{control}\)).

### 2.3 Punto de operación estacionario

En régimen permanente, \(\dot{\mathbf{x}}=0\). Igualando a cero:

$$-\frac{R_1}{L_1}I_L - \frac{V_C}{L_1} + \frac{D\,V_{dc}}{L_1} = 0 \;\Rightarrow\; V_C = D\,V_{dc} - R_1\,I_L$$

$$\frac{I_L}{C_f} - \frac{I_2}{C_f} = 0 \;\Rightarrow\; I_L = I_2$$

Con \(R_1\) pequeño y \(I_2=I_L\) nominal: \(V_C \approx D\,V_{dc}\). El ciclo de trabajo en el punto de operación es \(D = V_C / V_{dc}\).

### 2.4 Linealización: perturbaciones pequeñas

Definimos perturbaciones pequeñas alrededor del punto \((D, I_L, V_C)\):

$$ d = D + \hat{d},\quad i_L = I_L + \hat{i}_L,\quad v_C = V_C + \hat{v}_C $$

Sustituyendo en las ecuaciones de estado y descartando términos de segundo orden \((\hat{d}\cdot\hat{i}_L,\; \hat{d}\cdot\hat{v}_C)\):

**Inductor:**
$$ L_1\,\dot{\hat{i}}_L = (D+\hat{d})\,V_{dc} - (V_C+\hat{v}_C) - R_1(I_L+\hat{i}_L) $$

Los términos de régimen permanente se cancelan (\(D\,V_{dc}-V_C-R_1\,I_L=0\)); quedan solo los de primer orden:

$$ L_1\,\dot{\hat{i}}_L = \hat{d}\,V_{dc} - \hat{v}_C - R_1\,\hat{i}_L $$

**Condensador** (con \(\hat{i}_2 \approx 0\) para análisis de transferencia control→planta):

$$ C_f\,\dot{\hat{v}}_C = \hat{i}_L $$

### 2.5 Funciones de transferencia en el dominio s

Aplicando la transformada de Laplace a las ecuaciones linealizadas:

$$ sL_1\,\hat{I}_L(s) = V_{dc}\,\hat{D}(s) - \hat{V}_C(s) - R_1\,\hat{I}_L(s) \tag{1}$$

$$ sC_f\,\hat{V}_C(s) = \hat{I}_L(s) \tag{2}$$

De (2): \(\hat{V}_C = \hat{I}_L / (sC_f)\). Sustituyendo en (1):

$$ \hat{I}_L\left(sL_1 + R_1 + \frac{1}{sC_f}\right) = V_{dc}\,\hat{D}(s) $$

Multiplicando numerador y denominador por \(s\):

$$ \boxed{\frac{\hat{I}_L(s)}{\hat{D}(s)} = \frac{V_{dc}\,s C_f}{L_1 C_f s^2 + R_1 C_f s + 1} = \frac{V_{dc}/L_1\cdot s}{s^2 + (R_1/L_1)\,s + 1/(L_1 C_f)}} $$

Esta es la función de transferencia **control de ciclo de trabajo → corriente inductora**. Tiene un cero en el origen (el condensador es un circuito abierto a frecuencias bajas) y un par de polos complejos conjugados en:

$$ \omega_{res} = \frac{1}{\sqrt{L_1 C_f}},\qquad \zeta = \frac{R_1}{2}\sqrt{\frac{C_f}{L_1}} $$

La función de transferencia **control → tensión de condensador** se obtiene multiplicando por \(1/(sC_f)\):

$$ \boxed{\frac{\hat{V}_C(s)}{\hat{D}(s)} = \frac{V_{dc}}{L_1 C_f s^2 + R_1 C_f s + 1}} $$

Tiene los mismos polos y **ningún cero**: es la respuesta de un sistema de segundo orden puro, útil para el lazo de tensión.

### 2.6 Ejemplo numérico: respuesta en frecuencia del modelo promediado

Con los parámetros de diseño \(L_1=2\) mH, \(R_1=0{,}1\,\Omega\), \(C_f=15\,\mu\)F, \(V_{dc}=1200\) V:

**Frecuencia de resonancia LC:**
$$ \omega_{res} = \frac{1}{\sqrt{L_1 C_f}} = \frac{1}{\sqrt{2\times10^{-3}\times15\times10^{-6}}} = \frac{1}{\sqrt{3\times10^{-8}}} = \frac{1}{1{,}732\times10^{-4}} \approx 5773 \text{ rad/s} $$
$$ f_{res} = \frac{5773}{2\pi} \approx 919 \text{ Hz} $$

**Factor de amortiguamiento natural:**
$$ \zeta = \frac{R_1}{2}\sqrt{\frac{C_f}{L_1}} = \frac{0{,}1}{2}\sqrt{\frac{15\times10^{-6}}{2\times10^{-3}}} = 0{,}05\sqrt{7{,}5\times10^{-3}} = 0{,}05\times0{,}0866 = 0{,}00433 $$

Un \(\zeta\approx0{,}004\) implica un pico de resonancia de \(20\log_{10}(1/(2\zeta))=20\log_{10}(115)\approx41\) dB. El filtro LC sin amortiguamiento pasivo resonará violentamente a 919 Hz si el lazo de control no incluye amortiguamiento activo.

**Ganancia en DC** (\(s\to0\)) de \(\hat{I}_L/\hat{D}\):

La FDT es \(G_i(s)=V_{dc}\,sC_f/(L_1C_fs^2+R_1C_fs+1)\). En DC (\(s=0\)), la ganancia es \(0\): tiene un cero en el origen, como se esperaba (no hay respuesta DC de la corriente a una perturbación del ciclo de trabajo porque el condensador bloquea la DC).

**Ganancia en la resonancia** de \(\hat{V}_C/\hat{D}\):

$$ G_v(j\omega_{res}) = \frac{V_{dc}}{R_1 C_f\,\omega_{res}} = \frac{1200}{0{,}1\times15\times10^{-6}\times5773} \approx \frac{1200}{0{,}00866} \approx 138\,600 \text{ V/unidad} $$

Este pico enorme (\(\approx105\) dB) justifica la necesidad de amortiguar activamente la resonancia en el lazo de control antes de llegar a esta frecuencia.

### 2.7 Extensión al VSC trifásico en coordenadas dq

En el marco dq (rotante a \(\omega_0\)), las ecuaciones de estado del inductor se acoplan:

$$ L_1\,\dot{i}_d = v_d^{conv} - v_d^{pcc} - R_1\,i_d + \omega_0 L_1\,i_q $$
$$ L_1\,\dot{i}_q = v_q^{conv} - v_q^{pcc} - R_1\,i_q - \omega_0 L_1\,i_d $$

con \(v_d^{conv} = d_d \cdot V_{dc}/2\) y \(v_q^{conv} = d_q \cdot V_{dc}/2\) los ciclos de trabajo en dq. El acoplamiento cruzado \(\pm\omega_0 L_1 i_{q,d}\) aparece como un término conocido en el punto de operación; en el modelo linealizado se trata como perturbación o se cancela con feedforward. La función de transferencia por canal (d o q) es la misma que en §2.5, siempre que se aplique el desacoplamiento.

**Desacoplamiento feedforward:** El control añade en la referencia de tensión:
$$ v_d^{ref} = v_d^{pcc} - \omega_0 L_1\,i_q + K_p\,\tilde{i}_d + K_i\int\tilde{i}_d\,dt $$
$$ v_q^{ref} = v_q^{pcc} + \omega_0 L_1\,i_d + K_p\,\tilde{i}_q + K_i\int\tilde{i}_q\,dt $$

Así, el término cruzado \(\pm\omega_0 L_1\) queda cancelado por los términos de feedforward, y cada canal dq ve solo \(R_1 + sL_1\) como planta → la misma FDT de primer orden que en continua, simplificando el diseño del PI.

## 3 — De la tensión AC a la potencia: balance DC↔AC

### 3.1 Potencia instantánea en el marco dq

En el marco dq (amplitud invariante, convención de amplitud pico), la potencia trifásica instantánea es exactamente:

$$ P = \frac{3}{2}(v_d\,i_d + v_q\,i_q),\qquad Q = \frac{3}{2}(v_q\,i_d - v_d\,i_q) $$

**¿De dónde viene el factor 3/2? Derivación explícita paso a paso.**

La potencia trifásica instantánea en el dominio natural (abc) es la suma de las potencias individuales:

$$ p(t) = v_a i_a + v_b i_b + v_c i_c $$

Con señales sinusoidales simétricas y equilibradas de amplitud pico \(\hat{V}\), \(\hat{I}\) y desfase \(\phi\) entre tensión y corriente de cada fase:

$$ v_a = \hat{V}\cos\omega_0 t,\quad i_a = \hat{I}\cos(\omega_0 t - \phi) $$
$$ v_b = \hat{V}\cos(\omega_0 t - 2\pi/3),\quad i_b = \hat{I}\cos(\omega_0 t - 2\pi/3 - \phi) $$
$$ v_c = \hat{V}\cos(\omega_0 t + 2\pi/3),\quad i_c = \hat{I}\cos(\omega_0 t + 2\pi/3 - \phi) $$

**Paso 1:** Calcular el producto \(v_a i_a\) usando la identidad \(\cos\alpha\cos\beta = \frac{1}{2}[\cos(\alpha-\beta)+\cos(\alpha+\beta)]\):

$$ v_a i_a = \hat{V}\hat{I}\cos\omega_0 t\cdot\cos(\omega_0 t-\phi) = \frac{\hat{V}\hat{I}}{2}\left[\cos\phi + \cos(2\omega_0 t - \phi)\right] $$

**Paso 2:** Los tres términos a doble frecuencia se suman con desfases de \(120°\) entre sí:

$$ \cos(2\omega_0 t-\phi)+\cos(2\omega_0 t-\phi-2\pi\cdot2/3)+\cos(2\omega_0 t-\phi+2\pi\cdot2/3)=0 $$

(suma de tres fasores iguales en módulo y desfasados 120° = 0).

**Paso 3:** Solo sobreviven los términos constantes:

$$ p(t) = \frac{\hat{V}\hat{I}}{2}\cdot3\cdot\cos\phi = \frac{3}{2}\hat{V}\hat{I}\cos\phi $$

**Paso 4:** Conectar con dq. La transformada de Park con normalización de amplitud transforma las tres fases en:

$$ v_d = \hat{V}\cos\theta_{PLL},\quad v_q = -\hat{V}\sin\theta_{PLL} $$

Con el PLL alineado (\(\theta_{PLL}=0\)): \(v_d=\hat{V}\), \(v_q=0\), \(i_d=\hat{I}\cos\phi\), \(i_q=\hat{I}\sin\phi\) (convención de flujo de potencia positivo hacia la red). Entonces:

$$ P = \frac{3}{2}(v_d\,i_d + v_q\,i_q) = \frac{3}{2}\hat{V}\hat{I}\cos\phi \;\checkmark $$

El factor \(3/2\) es consecuencia de usar amplitudes **pico**: con valores eficaces (\(V_{RMS}=\hat{V}/\sqrt{2}\)), la fórmula sería \(P=3\,V_{RMS}\,I_{RMS}\cos\phi\) (factor 3 en vez de 3/2). En la convención de potencia invariante (donde la transformada incluye el factor \(\sqrt{2/3}\)), el factor desaparecería: \(P=v_d i_d + v_q i_q\).

### 3.2 Balance de potencia DC↔AC

Despreciando las pérdidas en los semiconductores, la potencia que entra por el bus DC iguala la que sale hacia la red AC:

$$ P_{DC} = V_{dc}\,I_{dc} = P_{AC} = \frac{3}{2}(v_d\,i_d + v_q\,i_q) $$

Despejando la corriente DC que el VSC demanda al condensador de bus:

$$ \boxed{I_{dc} = \frac{3}{2}\cdot\frac{v_d\,i_d + v_q\,i_q}{V_{dc}}} $$

Esta ecuación es fundamental para el control del bus DC: si \(P_{AC}\) varía (por ejemplo, cambio de referencia de potencia activa), la demanda de corriente DC cambia instantáneamente, y el condensador de bus debe absorber o suministrar la diferencia.

### 3.3 Caso particular: alineación con la red (\(v_q=0\))

El control vectorial alinea el eje d con el vector de tensión de red: \(v_d = \hat{V}_f,\; v_q = 0\). Entonces:

$$ P = \frac{3}{2}v_d\,i_d,\qquad Q = -\frac{3}{2}v_d\,i_q $$

La potencia activa la controla solo \(i_d\) y la reactiva solo \(i_q\): **desacoplo de P y Q**.

### 3.4 Ejemplo numérico verificado

**Datos:** VSC de \(S_n = 1\) MVA, \(V_{ll}=690\) V (RMS), \(V_{dc}=1200\) V, factor de potencia unitario.

**Tensión de fase pico:**
$$ \hat{V}_f = \frac{690\sqrt{2}}{\sqrt{3}} = \frac{690 \times 1{,}4142}{1{,}7321} \approx 563{,}4 \text{ V} $$

**Corriente AC de fase (pico)** a FP=1:
$$ \hat{I}_{f} = \frac{2\,P_{n}}{3\,\hat{V}_f} = \frac{2 \times 10^6}{3 \times 563{,}4} \approx 1183 \text{ A} $$

*Verificación:* \(P_{AC}=(3/2)\times563{,}4\times1183=10^6\) W ✓

**Corriente DC:**
$$ I_{dc} = \frac{P_n}{V_{dc}} = \frac{10^6}{1200} \approx 833 \text{ A} $$

*Verificación por fórmula dq* (con \(v_d=\hat{V}_f=563{,}4\) V, \(i_d=\hat{I}_f=1183\) A, \(v_q=i_q=0\)):
$$ I_{dc} = \frac{3/2 \times 563{,}4 \times 1183}{1200} = \frac{844\,900 \cdot 1{,}5}{1200} = \frac{1\,267\,350}{1200} \approx 1056 \text{ A} $$

Atención: la diferencia surge porque \(\hat{I}_f\) es el valor **pico** y \(I_{dc}\) se calculó usando potencia nominal RMS. La fórmula dq con amplitudes pico da la corriente DC real (que es continua, no RMS). Usando valores RMS: \(I_{f,RMS}=\hat{I}_f/\sqrt{2}\approx836\) A → \(I_{dc}=(3/2)\times563{,}4\times836\times\sqrt{2}/V_{dc}=833\) A ✓. La coherencia exige usar la misma convención en todo el cálculo.

### 3.5 Dimensionado del condensador de bus DC

El condensador \(C_{dc}\) debe limitar el rizado de tensión del bus. La corriente que demanda el VSC al condensador es \(I_{dc}=(3/2)(v_d i_d+v_q i_q)/V_{dc}\), que varía a doble frecuencia de red cuando el sistema no está perfectamente equilibrado, y a la frecuencia de conmutación por el rizado PWM.

**Rizado a doble frecuencia de red** (sistema levemente desequilibrado, potencia no constante):

Si la potencia fluctúa en \(\Delta P\) a frecuencia \(2\omega_0\), la tensión de bus varía:

$$ \Delta V_{dc} = \frac{\Delta P}{2\omega_0\,C_{dc}\,V_{dc}} $$

Despejando \(C_{dc}\) para un rizado objetivo \(\Delta V_{dc}/V_{dc}\leq r\):

$$ \boxed{C_{dc} \ge \frac{\Delta P}{2\omega_0\,r\,V_{dc}^2}} $$

**Ejemplo:** \(P_n=10^6\) W, rizado \(\Delta P=5\%\,P_n=50\,000\) W, \(r=1\%\), \(V_{dc}=1200\) V, \(f_0=50\) Hz:

$$ C_{dc} \ge \frac{50\,000}{2\pi\times100\times0{,}01\times1{,}44\times10^6} = \frac{50\,000}{9{,}047\times10^6} \approx 5{,}5\,\text{mF} $$

Con condensadores electrolíticos de 2.2 mF/1350 V (serie), bastarían 3 condensadores en paralelo.

## 4 — Rizado de corriente y tensión: cuánto filtra el LC

### 4.1 Origen del rizado: la tensión de polo es cuadrada

Durante el intervalo en que \(S_1\) conduce (\(d\,T_{sw}\)), la tensión en el extremo del inductor es \(+V_{dc}/2\) (respecto al punto medio del bus). Durante \((1-d)\,T_{sw}\), es \(-V_{dc}/2\). La tensión media promediada es \(v_o=(2d-1)V_{dc}/2\). La tensión aplicada al inductor alterna entre \(+V_{dc}/2-v_o\) y \(-V_{dc}/2-v_o\), dos valores de signo contrario. Eso genera una **rampa triangular** de corriente en \(L_1\).

### 4.2 Rizado de corriente pico-pico en L₁

Durante el subintervalo de subida (\(d\,T_{sw}\)), el inductor ve la tensión \(V_{dc}/2 - v_o = V_{dc}(1-d)\):

$$ \Delta i_{L,pp} = \frac{V_{dc}/2 - v_o}{L_1}\cdot d\,T_{sw} = \frac{V_{dc}(1-d)\,d}{L_1\,f_{sw}} $$

Esta expresión es máxima cuando \(d = 1/2\) (tensión de salida cero, \(d(1-d)\) máximo = \(1/4\)):

$$ \boxed{\Delta i_{L,pp}^{max} = \frac{V_{dc}}{4\,L_1\,f_{sw}}} $$

Esta fórmula corresponde al **máximo absoluto de rizado** durante el ciclo de red (ocurre cuando la tensión de salida cruza el cero). En el pico de la sinusoide, \(d\approx(1+m)/2\), y el rizado es menor (el tiempo de subida es más largo pero la tensión de polo es menor). La **amplitud** (semi-oscilación, valor habitual en el diseño de filtros) es la mitad:

$$ \Delta i_{L,amp}^{max} = \frac{V_{dc}}{8\,L_1\,f_{sw}} $$

### 4.3 Rizado de tensión en el condensador de filtro

El condensador \(C_f\) se carga con la corriente de rizado de \(L_1\). Suponiendo que la corriente de red \(i_2\) es prácticamente senoidal pura (el filtro hace bien su trabajo), toda la corriente de rizado de \(i_L\) fluye por \(C_f\). La carga/descarga triangular de amplitud \(\Delta i_{L,amp}\) durante medio periodo de conmutación \(T_{sw}/2\) produce un rizado de tensión:

$$ \Delta v_{C,pp} = \frac{\Delta i_{L,amp}}{C_f\,f_{sw}} = \frac{V_{dc}}{8\,L_1\,C_f\,f_{sw}^2} $$

### 4.4 Ejemplo numérico: \(L_1=2\) mH, \(C_f=15\) µF, \(f_{sw}=10\) kHz, \(V_{dc}=1200\) V

**Rizado de corriente (máximo):**

$$ \Delta i_{L,pp}^{max} = \frac{1200}{4 \times 2\times10^{-3}\times 10\times10^3} = \frac{1200}{80} = 15{,}0 \text{ A}_{pp} $$

Con \(I_{n}\approx836\) A (RMS) → amplitud \(=836\sqrt{2}\approx1182\) A pico, el rizado relativo es:

$$ \frac{\Delta i_{L,pp}^{max}/2}{I_{n,pico}} = \frac{7{,}5}{1182} \approx 0{,}63\% $$

Para un sistema de 1 MVA con corriente nominal de 836 A RMS, 7.5 A de amplitud de rizado es **muy bajo**, típico para aplicaciones de red donde se permite hasta 20-30%.

**Rizado de tensión:**

$$ \Delta v_{C,pp} = \frac{1200}{8 \times 2\times10^{-3}\times 15\times10^{-6}\times (10\times10^3)^2} = \frac{1200}{24{,}0} = 50{,}0 \text{ mV}_{pp} $$

Relativo a la tensión de fase pico (563 V): \(50\,\text{mV}/563\,\text{V}\approx0{,}009\%\) → despreciable.

**Conclusión de diseño:** Con \(L_1=2\) mH y \(C_f=15\) µF a 10 kHz, el filtro atenúa el rizado de corriente al 0.6% y el de tensión al 0.01%. El diseño está muy confortable; si se quisiera reducir \(L_1\) (coste/peso) manteniendo 5% de rizado, bastaría con \(L_1^{min}=1200/(4\times0{,}05\times1182\times10\,000)\approx0{,}5\) mH.

### 4.5 Proceso de diseño: de la restricción al componente

El diseñador fija un **objetivo de rizado máximo** (típicamente 10–20% de la corriente nominal pico) y despeja \(L_1\):

$$ L_1^{min} = \frac{V_{dc}}{4\,\Delta i_{L,pp}^{obj}\,f_{sw}} = \frac{V_{dc}}{4\,r\,\hat{I}_n\,f_{sw}} $$

donde \(r\) es la fracción de rizado respecto a \(\hat{I}_n\).

**Iteración 1 — fijar \(r=20\%\):**
$$ L_1^{min} = \frac{1200}{4\times0{,}20\times1182\times10\,000} = \frac{1200}{9{,}456\times10^6} \approx 0{,}127\,\text{mH} $$

Resultado: 0.13 mH, muy pequeño. El rizado estaría en el límite, sin margen para variaciones de \(V_{dc}\) o de la carga.

**Iteración 2 — fijar \(r=5\%\):**
$$ L_1^{min} = \frac{1200}{4\times0{,}05\times1182\times10\,000} = \frac{1200}{2{,}364\times10^6} \approx 0{,}508\,\text{mH} $$

Elegir el inductor normalizado más próximo por encima: \(L_1=0{,}5\,\text{mH}\) (ligeramente por debajo del mínimo calculado: recalcular rizado).

**Verificación con \(L_1=0{,}5\,\text{mH}\):**
$$ \Delta i_{pp} = \frac{1200}{4\times0{,}5\times10^{-3}\times10^4} = \frac{1200}{20} = 60\,\text{A} = \frac{60}{1182}\approx5{,}1\%\;\hat{I}_n \quad ✓ $$

**Iteración 3 — restricción adicional: el inductorcondensador no puede resonar por debajo de 2 kHz** (demasiado cerca del ancho de banda de control de 1 kHz):

$$ f_{res} = \frac{1}{2\pi\sqrt{L_1 C_f}} > 2\,\text{kHz} \;\Rightarrow\; C_f < \frac{1}{(2\pi\times2000)^2\times L_1} $$

Con \(L_1=0{,}5\,\text{mH}\):
$$ C_f < \frac{1}{(12566)^2\times5\times10^{-4}} = \frac{1}{7{,}9\times10^7} \approx 12{,}6\,\mu\text{F} $$

Elegir \(C_f=10\,\mu\text{F}\) → \(f_{res}=1/(2\pi\sqrt{5\times10^{-4}\times10^{-5}})=2{,}25\) kHz ✓.

**Verificación del rizado de tensión con \(C_f=10\,\mu\text{F}\):**
$$ \Delta v_{C,pp} = \frac{1200}{8\times0{,}5\times10^{-3}\times10^{-5}\times10^8} = \frac{1200}{400} = 3{,}0\,\text{V} = 0{,}53\%\;\hat{V}_f \quad ✓ $$

**Resumen del diseño iterativo:**

| Iteración | \(r\) obj. | \(L_1\) mín. [mH] | \(L_1\) elegido [mH] | \(\Delta i_{pp}\) real [%] | \(f_{res}\) [Hz] |
|---|---|---|---|---|---|
| 1 | 20% | 0.127 | — | — | — |
| 2 | 5% | 0.508 | 0.5 | 5.1% | — |
| 3 | 5% | 0.508 | 0.5 | 5.1% | 2250 ✓ |

Con \(L_1=0{,}5\) mH y \(C_f=10\,\mu\text{F}\) se cumple tanto la restricción de rizado (5.1%) como la de resonancia (2.25 kHz > 2 kHz). El diseño original \(L_1=2\,\text{mH}\), \(C_f=15\,\mu\text{F}\) es más conservador (rizado 0.63%, \(f_{res}=919\) Hz → requiere amortiguamiento activo explícito).

## 5 — Tiempo muerto: efecto sobre la tensión media y distorsión

### 5.1 Qué es el tiempo muerto y por qué existe

Cuando se ordena un cambio de estado en una rama (p.ej. pasar de \(S_1\) abierto a \(S_1\) cerrado), hay un retardo de propagación en el driver y el interruptor no abre/cierra instantáneamente. Si ambos interruptores de la rama condujesen a la vez aunque sea un instante, pondrían \(+V_{dc}\) directamente a \(0\) → cortocircuito del bus DC → corriente de pico destructiva. Por eso se inserta un **tiempo muerto** \(t_d\) (típicamente 1–3 µs) entre el apagado de un interruptor y el encendido del otro.

### 5.2 Pérdida de tensión media por tiempo muerto

Durante \(t_d\), ningún interruptor conduce; la corriente de fase circula por los diodos de libre circulación. Dependiendo del **signo de la corriente**, la salida de la rama queda conectada a \(0\) o a \(+V_{dc}\), lo opuesto a lo que el control pide. En cada periodo de conmutación hay **dos transiciones** (subida y bajada), cada una con un error de \(t_d\). La tensión media perdida por ciclo es:

$$ \Delta v_{td} = \pm\,V_{dc}\,t_d\,f_{sw} $$

El signo depende del signo de \(i_x\):
- Si \(i_x > 0\): el tiempo muerto conecta la salida a 0 cuando debería estar en \(+V_{dc}\) → **tensión media menor** que la pedida.
- Si \(i_x < 0\): el diodo superior conduce → salida queda en \(+V_{dc}\) cuando debería estar en 0 → **tensión media mayor**.

### 5.3 Ejemplo numérico

Con \(t_d=2\,\mu\)s, \(f_{sw}=10\) kHz, \(V_{dc}=1200\) V:

$$ \Delta v_{td} = 1200 \times 2\times10^{-6} \times 10\times10^3 = 24 \text{ V} $$

Relativo a la tensión de fase pico (563 V): \(24/563\approx4{,}3\%\). No es despreciable: causa distorsión visible y error en el lazo de corriente si no se compensa.

### 5.4 Contribución a armónicos en el sistema trifásico

El error de tiempo muerto es proporcional al signo de la corriente: \(\Delta v_{td}(t) \propto \text{sign}(i_x(t))\). La función signo de una senoide es una onda cuadrada a la frecuencia fundamental, cuya descomposición en Fourier contiene armónicos impares:

$$ \text{sign}(\cos\omega_0 t) = \frac{4}{\pi}\sum_{k=0}^{\infty}\frac{(-1)^k}{2k+1}\cos((2k+1)\omega_0 t) = \frac{4}{\pi}\left[\cos\omega_0 t - \frac{\cos 3\omega_0 t}{3} + \frac{\cos 5\omega_0 t}{5} - \cdots\right] $$

En el sistema trifásico, los armónicos de secuencia cero (orden \(3k\): 3.°, 9.°, 15.°, ...) se cancelan entre fases porque son iguales en las tres y no circulan por la carga trifásica equilibrada. Los armónicos de secuencia positiva y negativa que sí llegan a la red son los de orden \(6k\pm1\): **5.°, 7.°, 11.°, 13.°,** etc. La amplitud de cada armónico de tiempo muerto en la tensión de fase es:

$$ \hat{V}_{h} = \frac{4}{\pi}\cdot\frac{1}{h}\cdot V_{dc}\,t_d\,f_{sw},\qquad h=6k\pm1 $$

**Ejemplo:** Con \(V_{dc}=1200\) V, \(t_d=2\,\mu\)s, \(f_{sw}=10\) kHz y \(\hat{V}_f=563\) V:
- 5.° armónico: \(\hat{V}_5 = (4/\pi)\cdot(1/5)\cdot24 = 6{,}1\) V = 1.1% de \(\hat{V}_f\)
- 7.° armónico: \(\hat{V}_7 = (4/\pi)\cdot(1/7)\cdot24 = 4{,}4\) V = 0.78% de \(\hat{V}_f\)

La normativa IEC 61000-3-2 limita el 5.° armónico a típicamente 3–4% del fundamental para inversores de red: la compensación de tiempo muerto es necesaria para cumplir.

### 5.5 Compensación del tiempo muerto

La estrategia más sencilla es añadir en el software del control la corrección:

$$ v_{ref,compensado} = v_{ref} + \text{sign}(i_x)\cdot V_{dc}\,t_d\,f_{sw} $$

Para ello se necesita conocer el signo de la corriente de fase (medición o estimación). En implementaciones reales se añade una pequeña histéresis alrededor de cero para evitar oscilaciones en el flanco de cruce.

## 6 — Dimensionado de \(V_{dc}\) desde la red: caso completo con margen

### 6.1 Tensión mínima teórica del bus DC

Para que el VSC pueda sintetizar la tensión de fase pedida por el control sin saturar la modulación, el bus DC debe satisfacer \(\hat{V}_{fase} = m\,V_{dc}/2\leq m_{max}\,V_{dc}/2\). Despejando \(V_{dc}\):

$$ V_{dc} \ge \frac{2\,\hat{V}_{fase}}{m_{max}} $$

Con \(\hat{V}_{fase} = V_{ll}\sqrt{2}/\sqrt{3}\) (tensión de línea RMS → tensión de fase pico):

$$ V_{dc,min} = \frac{2\,V_{ll}\sqrt{2}/\sqrt{3}}{m_{max}} = \frac{2\sqrt{2}\,V_{ll}}{\sqrt{3}\,m_{max}} $$

Los valores de \(m_{max}\) dependen del tipo de modulación:
- SPWM lineal: \(m_{max}=1{,}00\)
- SPWM con inyección de 3.er armónico / SVPWM: \(m_{max}=2/\sqrt{3}\approx1{,}155\)

### 6.2 Margen adicional por pérdidas y caídas

En la práctica hay que añadir margen por:
- **Caída en \(L_1\)**: \(\Delta V_{L1} = \omega_0 L_1 I_{n,pico}\) (caída resistiva es menor pero también existe)
- **Caída en el transformador** o cable de conexión
- **Dinámica transitoria**: el lazo de corriente necesita margen de tensión para seguir las rampas de referencia
- **Variaciones de la tensión de red**: si la red puede subir un 10%, \(V_{dc}\) también debe subir

Factor de margen típico: \(k_{margin}=1{,}05\) a \(1{,}10\).

$$ V_{dc,elegido} = k_{margin}\cdot V_{dc,min} $$

### 6.3 Proceso iterativo: elegir \(V_{dc}\) → calcular \(m\) → verificar

**Iteración 1 — estimación inicial:**
$$ V_{dc}^{(0)} = 1{,}05 \times V_{dc,min} $$

**Calcular m real:**
$$ m = \frac{2\,\hat{V}_{fase}}{V_{dc}^{(0)}} $$

**Verificar:** si \(m < m_{max}\) y el margen \((m_{max}-m)/m_{max}\) es suficiente (p.ej. >5 %), el diseño es válido. Si no, aumentar \(V_{dc}\) y repetir.

**Verificar rizado de bus DC:** una vez elegido \(V_{dc}\), el condensador de bus debe limitar el rizado: \(\Delta V_{dc}/V_{dc} < 1\%\) ─ esto determina \(C_{dc}\).

### 6.4 Ejemplo completo: \(V_{ll}=690\) V, SPWM, \(m_{max}=0{,}95\)

**Tensión de fase pico:**
$$ \hat{V}_f = \frac{690\sqrt{2}}{\sqrt{3}} = \frac{975{,}8}{1{,}7321} = 563{,}4 \text{ V} $$

**Vdc mínimo sin margen:**
$$ V_{dc,min,teorico} = \frac{2\times563{,}4}{0{,}95} = \frac{1126{,}8}{0{,}95} = 1186 \text{ V} $$

**Iteración 1** — aplicar margen 5 %:
$$ V_{dc}^{(1)} = 1{,}05\times 1186 = 1245 \text{ V} \quad\Rightarrow\quad m^{(1)} = \frac{2\times563{,}4}{1245} = 0{,}905 < 0{,}95\ ✓$$

Margen restante: \((0{,}95-0{,}905)/0{,}95 = 4{,}7\%\). Suficiente para la dinámica, un poco justo.

**Iteración 2** — elegir nivel de condensador estándar más próximo: \(V_{dc}=1200\) V.
$$ m^{(2)} = \frac{2\times563{,}4}{1200} = \frac{1126{,}8}{1200} = 0{,}939 $$

Margen: \((0{,}95-0{,}939)/0{,}95 = 1{,}2\%\). Muy ajustado: si la red sube un 5%, \(m\) llegaría a \(0{,}985\), cerca del límite. Para ser conservador se elige \(V_{dc}=1300\) V:
$$ m = \frac{1126{,}8}{1300} = 0{,}867 $$
Margen: \((0{,}95-0{,}867)/0{,}95 = 8{,}7\%\). Cómodo.

**Resumen del proceso:**

| \(V_{dc}\) [V] | \(m\) | Margen [%] | Decisión |
|---|---|---|---|
| 1186 | 0.950 | 0 | Límite exacto: no usar |
| 1200 | 0.939 | 1.2 | Muy ajustado |
| 1245 | 0.905 | 4.7 | Aceptable |
| 1300 | 0.867 | 8.7 | Cómodo ✓ |

**Conclusión:** \(V_{dc}=1300\) V con SPWM (o 1200 V si se usa SVPWM con \(m_{max}=1{,}10\), que daría \(m=0{,}939/1{,}10=0{,}85\) y margen del 22%).

### 6.5 Verificación del margen de caída resistivo-inductiva

El \(V_{dc}\) elegido debe soportar la caída de tensión en \(R_1\) y \(L_1\) a plena carga, manteniendo \(m<m_{max}\):

**Caída resistiva en \(L_1\)** (con \(R_1=0{,}1\,\Omega\), \(\hat{I}_n=1182\) A pico):
$$ \Delta V_{R1} = R_1\,\hat{I}_n = 0{,}1\times1182 = 118 \text{ V} $$

**Caída reactiva en \(L_1\)** (a 50 Hz, con \(L_1=2\) mH):
$$ \Delta V_{X1} = \omega_0 L_1\,\hat{I}_n = 2\pi\times50\times2\times10^{-3}\times1182 = 742 \text{ V} $$

La tensión que debe sintetizar el convertidor para mantener \(\hat{I}_n\) a la entrada del filtro cuando la tensión de red es \(\hat{V}_f=563\) V:

$$ \hat{V}_{conv} = \sqrt{(\hat{V}_f + \Delta V_{R1})^2 + (\Delta V_{X1})^2} = \sqrt{681^2 + 742^2} = \sqrt{463\,761 + 550\,564} \approx 1007 \text{ V} $$

Con \(V_{dc}=1300\) V: \(m=2\times1007/1300=1{,}549\). Esto supera \(m_{max}\): **¡el diseño falla!**

**¿Qué pasó?** La caída en \(L_1=2\) mH es muy grande a la corriente nominal de un VSC de 1 MVA. Esta corriente es para un filtro LCL donde \(L_2\) absorbe gran parte de la caída; para un filtro LC simple a 1 MVA la inductancia debe ser mucho menor. Recalculando con \(L_1=50\,\mu\)H:

$$ \Delta V_{X1} = 2\pi\times50\times50\times10^{-6}\times1182 = 18{,}5 \text{ V} $$
$$ \hat{V}_{conv} = \sqrt{(563+12)^2+18{,}5^2} \approx 575 \text{ V},\quad m=\frac{2\times575}{1300}=0{,}885 \quad ✓ $$

**Conclusión del recálculo:** El parámetro \(L_1=2\) mH es apropiado para VSC de baja potencia (10–50 kVA) o como \(L_1\) de un filtro LCL donde solo una fracción de la corriente total fluye por él. Para un VSC de 1 MVA directo a red, \(L_1\lesssim0{,}1\) mH y la inductancia principal la aporta el transformador.

## 7 — Comparación conmutado vs promediado: dónde divergen

### 7.1 A qué frecuencia empieza la diferencia

El modelo promediado es exacto mientras los armónicos de conmutación sean despreciables en la respuesta dinámica de interés. El criterio formal es el teorema de Nyquist aplicado al muestreo implícito que hace el PWM: el promediado solo captura frecuencias menores que \(f_{sw}/2\). Por encima de esa frecuencia, el modelo promediado extrapolará de forma incorrecta. En la práctica, la diferencia se hace visible ya desde \(\approx 0{,}3\,f_{sw}\) en la función de transferencia (empiezan a divergir las fases).

### 7.2 Por qué la impedancia de salida diverge cerca de \(f_{sw}\)

El convertidor conmutado actúa como un muestreador ZOH (zero-order hold) a la frecuencia \(f_{sw}\): el ciclo de trabajo se actualiza una vez por periodo de conmutación. El equivalente en frecuencia de un ZOH añade un retraso de \(T_{sw}/2\) y un módulo:

$$ H_{ZOH}(f) = T_{sw}\,\frac{\sin(\pi f/f_{sw})}{\pi f/f_{sw}}\,e^{-j\pi f/f_{sw}} $$

Este factor reduce la magnitud de la impedancia efectiva y añade fase negativa. El modelo promediado, al no incluir este retraso, sobreestima la ganancia y subestima el retraso para frecuencias \(f > f_{sw}/5\).

### 7.3 Cuándo usar cada modelo

| Propósito | Modelo recomendado | Razón |
|---|---|---|
| Diseño de lazos de control | Promediado | Continuo, linealizable, estable en simulación |
| Análisis de impedancia (< \(f_{sw}/3\)) | Promediado | Coincide con el conmutado |
| Análisis de impedancia (> \(f_{sw}/3\)) | Conmutado | El ZOH importa |
| EMI y armónicos de conmutación | Conmutado | El promediado los ignora |
| Pérdidas de conmutación | Conmutado | El promediado asume pérdidas cero en el puente |
| Diseño del filtro de salida | Ambos | Rizado con conmutado, dinámica con promediado |
| Validación rápida del control | Promediado | 100× más rápido en simulación |

### 7.4 Dato del proyecto GFM-Impedance

En el análisis de impedancia del proyecto 01-GFM-Impedance, el script `switched.py` comparó la impedancia de salida del convertidor en modo promediado y conmutado barriendo desde 10 Hz hasta 2 kHz (bien por debajo de \(f_{sw}=10\) kHz). La diferencia de módulo máxima fue **0.67%** y la diferencia de fase máxima fue **0.23°**. Este resultado valida que el modelo promediado es suficiente para el diseño de lazos y el análisis de estabilidad en la banda de control (hasta 1–2 kHz con \(f_{sw}=10\) kHz).

### 7.5 Límite de validez como regla práctica

$$ f_{control,max} = \frac{f_{sw}}{10} $$

Esta regla garantiza que el retraso de ZOH (\(\approx T_{sw}/2\)) y los armónicos de conmutación no degraden el margen de fase del lazo de control en más de 5°–10°. Para \(f_{sw}=10\) kHz: \(f_{control,max}=1\) kHz, coherente con anchos de banda típicos de lazos de corriente en inversores de red.

## 8 — State-space averaging: fundamento formal y condición de validez

### 8.1 El problema: el circuito tiene dos topologías

Durante el subintervalo ON (\(d\,T_{sw}\)), el interruptor superior \(S_1\) conduce y el circuito obedece:

$$ \dot{\mathbf{x}} = A_1\,\mathbf{x} + B_1\,\mathbf{u} \tag{ON}$$

Durante el subintervalo OFF (\((1-d)\,T_{sw}\)), \(S_2\) conduce y el circuito obedece:

$$ \dot{\mathbf{x}} = A_2\,\mathbf{x} + B_2\,\mathbf{u} \tag{OFF}$$

La pregunta es: ¿cuál es el modelo simplificado que describe la dinámica media a escala de tiempos mucho más largos que \(T_{sw}\)?

### 8.2 El método del promediado (Erickson & Maksimovic, Cap. 7)

**Hipótesis:** el ciclo de trabajo \(d(t)\) varía lentamente comparado con \(T_{sw}\); es decir, \(|{\dot d}|\ll f_{sw}\). En ese caso, el estado \(\mathbf{x}(t)\) varía poco en un periodo de conmutación y puede aproximarse como constante para hacer el promedio.

**Paso 1:** Se promedia la ecuación de estado sobre \(T_{sw}\):

$$ \langle\dot{\mathbf{x}}\rangle = \frac{1}{T_{sw}}\int_0^{T_{sw}}\dot{\mathbf{x}}\,dt = \frac{1}{T_{sw}}\left[\int_0^{dT_{sw}}(A_1\mathbf{x}+B_1\mathbf{u})\,dt + \int_{dT_{sw}}^{T_{sw}}(A_2\mathbf{x}+B_2\mathbf{u})\,dt\right] $$

Bajo la hipótesis de variación lenta de \(\mathbf{x}\) y \(\mathbf{u}\):

$$ \langle\dot{\mathbf{x}}\rangle \approx \left[d\,A_1 + (1-d)\,A_2\right]\mathbf{x} + \left[d\,B_1 + (1-d)\,B_2\right]\mathbf{u} $$

**Paso 2:** Se define el modelo promediado:

$$ \dot{\overline{\mathbf{x}}} = \bar{A}(d)\,\overline{\mathbf{x}} + \bar{B}(d)\,\mathbf{u} $$

con \(\bar{A}(d) = d\,A_1 + (1-d)\,A_2\) y \(\bar{B}(d) = d\,B_1 + (1-d)\,B_2\).

### 8.3 Aplicación al VSC: los dos subintervalos

Para la rama del VSC con un filtro LC, las matrices de estado en cada subintervalo son:

**Subintervalo ON** (\(S_1\) cerrado, tensión de entrada \(+V_{dc}\) al inductor):
$$ A_1 = \begin{bmatrix}-R_1/L_1 & -1/L_1 \\ 1/C_f & 0\end{bmatrix},\quad B_1\mathbf{u} = \begin{bmatrix}V_{dc}/L_1 \\ -i_2/C_f\end{bmatrix} $$

**Subintervalo OFF** (\(S_2\) cerrado, tensión de entrada \(0\) al inductor, pero el inductor sigue conduciendo por el diodo de libre circulación):
$$ A_2 = \begin{bmatrix}-R_1/L_1 & -1/L_1 \\ 1/C_f & 0\end{bmatrix},\quad B_2\mathbf{u} = \begin{bmatrix}0/L_1 \\ -i_2/C_f\end{bmatrix} $$

Nótese que \(A_1 = A_2 = A\) (las ramas de estado no cambian entre subintervalos, solo cambia la forzada). Entonces:

$$ \bar{A}(d) = d\,A + (1-d)\,A = A $$
$$ \bar{B}(d)\,\mathbf{u} = d\begin{bmatrix}V_{dc}/L_1\\-i_2/C_f\end{bmatrix} + (1-d)\begin{bmatrix}0\\-i_2/C_f\end{bmatrix} = \begin{bmatrix}d\,V_{dc}/L_1\\-i_2/C_f\end{bmatrix} $$

Que es exactamente el modelo de §2.2. El promediado no cambia \(A\) porque la topología del filtro LC es la misma en ambos subintervalos (el inductor siempre está en serie y el condensador siempre en paralelo); solo cambia la tensión de entrada.

### 8.4 Condición de validez: separación de escalas de tiempo

El error del promediado en la respuesta en frecuencia crece con la frecuencia. La condición formal para que el error sea menor que \(\epsilon\) es:

$$ \frac{f}{f_{sw}} \ll 1 \quad\Longleftrightarrow\quad \omega\,T_{sw} \ll 2\pi $$

En la práctica, para un error de módulo \(<1\%\) en la respuesta de \(\hat{I}_L/\hat{D}\):

$$ f < 0{,}05\,f_{sw} $$

Para \(f_{sw}=10\) kHz, eso significa que el modelo promediado es cuantitativamente preciso (error <1%) hasta \(\approx500\) Hz. Por encima de esa frecuencia el error crece pero sigue siendo cualitativo hasta \(f_{sw}/3\approx3{,}3\) kHz. El dato del proyecto (error 0.67% a 2 kHz) confirma que incluso cerca del límite, el error sigue siendo pequeño.

**Condición de separación de escalas:** la hipótesis de Erickson es válida si las constantes de tiempo del circuito son mucho mayores que \(T_{sw}\):

$$ \tau_{circuito} = L_1/R_1 \gg T_{sw} = 1/f_{sw} $$

Con \(L_1=2\) mH, \(R_1=0{,}1\,\Omega\): \(\tau=L_1/R_1=20\) ms vs \(T_{sw}=0{,}1\) ms → ratio 200. La condición se cumple sobradamente. El condensador también: \(\tau_{RC}=R_1 C_f=0{,}1\times15\times10^{-6}=1{,}5\,\mu\text{s}\), que es mayor que \(T_{sw}/20=5\,\mu\text{s}\) pero más ajustado. En la práctica, la condición para \(C_f\) no es \(\tau_{RC}\gg T_{sw}\) sino que la variación de \(v_C\) en un periodo sea pequeña en comparación con \(V_C\): \(\Delta v_C/V_C\ll1\), que ya verificamos (\(0{,}009\%\)). Ambas condiciones se cumplen y el promediado es válido.

### 8.5 Error del promediado cuantificado: el retraso de ZOH

El convertidor conmutado actualiza el ciclo de trabajo una vez por periodo (al inicio del triángulo de la portadora). Esto equivale a un **muestreador seguido de un ZOH** con tiempo de retención \(T_{sw}\). La función de transferencia exacta de ese ZOH es:

$$ H_{ZOH}(f) = \frac{1-e^{-j2\pi f T_{sw}}}{j2\pi f T_{sw}} = \text{sinc}\!\left(\frac{f}{f_{sw}}\right)e^{-j\pi f/f_{sw}} $$

donde \(\text{sinc}(x)=\sin(\pi x)/(\pi x)\). Su módulo es \(|\text{sinc}(f/f_{sw})|\) y su fase es \(-\pi f/f_{sw}\) radianes. El modelo promediado tiene \(H_{ZOH}=1\) (ignora este retraso).

**Error de módulo** en función de la frecuencia:

| \(f/f_{sw}\) | \(|\text{sinc}|\) [dB] | \(\Delta\phi\) [°] |
|---|---|---|
| 0.05 | −0.03 dB | −9° |
| 0.10 | −0.13 dB | −18° |
| 0.20 | −0.53 dB | −36° |
| 0.33 | −1.50 dB | −60° |
| 0.50 | −3.92 dB | −90° |

La diferencia de fase en la frecuencia de cruce \(f_c\) del lazo de corriente introduce un error de margen de fase:

$$ \Delta\phi_{ZOH}(f_c) = \frac{180°\,f_c}{f_{sw}} $$

Para \(f_c=1\) kHz, \(f_{sw}=10\) kHz: \(\Delta\phi_{ZOH}=18°\). Este margen de fase se "consume" por el retraso digital: si el objetivo es un margen de 45°, el lazo de control diseñado con el modelo promediado debe mostrar 63° de margen de fase en la función de lazo promediada. La diferencia de 18° será aportada por el ZOH real.

**Regla de diseño derivada:** para que la degradación del margen de fase sea menor que \(\Delta\phi_{max}\):

$$ f_c < \frac{\Delta\phi_{max}[\°]}{180°}\cdot f_{sw} $$

Con \(\Delta\phi_{max}=10°\) y \(f_{sw}=10\) kHz: \(f_c<556\) Hz. En la práctica se usa \(f_c\approx f_{sw}/10=1\) kHz aceptando una degradación de 18°.

## Cuándo y por qué se usa

El VSC aparece siempre que se necesita intercambiar potencia AC↔DC de forma controlada y bidireccional: conexión a red de renovables (fotovoltaica, eólica), STATCOM, accionamientos de motor, HVDC y back-to-back. La modulación PWM es el modo estándar de imponer la tensión con bajas pérdidas en prácticamente todos los convertidores modernos. Su salida exige un [[filtro-lcl|filtro LC o LCL]] para atenuar la conmutación.

## Procedimiento (genérico)

1. Calcular \(\hat{V}_f = V_{ll}\sqrt{2}/\sqrt{3}\) y elegir \(m_{max}\) según tipo de modulación.
2. Dimensionar \(V_{dc}\): aplicar \(V_{dc} \ge 2\hat{V}_f/m_{max}\) con margen 5–10 %; iterar hasta tener \(m\) cómodo.
3. Fijar \(f_{sw}\) y diseñar el filtro LC/LCL: \(L_1 = V_{dc}/(4\,\Delta i_{L,max}\,f_{sw})\).
4. Modelar en promediado (ciclos de trabajo en dq), linealizar y diseñar los lazos de corriente/tensión con \(f_{control}<f_{sw}/10\).
5. Implementar compensación de tiempo muerto; cuantificar \(\Delta v_{td}=V_{dc}\,t_d\,f_{sw}\).
6. Validar en modelo conmutado (PLECS, simulink, o Python): comparar impedancia y formas de onda. Si la diferencia es <1% en la banda de control, el promediado es suficiente.

## Ejemplo de aplicación real

VSC de 1 MVA en red de 690 V (LL, RMS), FP unitario, \(f_{sw}=10\) kHz.

- \(\hat{V}_f = 563{,}4\) V, \(V_{dc}=1300\) V elegido → \(m=0{,}867\), margen 8.7%.
- \(I_n=836\) A RMS → \(\hat{I}_f=1182\) A pico → en dq: \(i_d^*=1182\) A, \(i_q^*=0\).
- Rizado máximo: \(\Delta i_{pp}=1300/(4\times2\times10^{-3}\times10^4)=16{,}25\) A → 1.4% de \(\hat{I}_f\). ✓
- Error de tiempo muerto (\(t_d=2\) µs): \(\Delta v_{td}=1300\times2\times10^{-6}\times10^4=26\) V = 4.6% de \(\hat{V}_f\) → compensación necesaria.
- Ancho de banda de lazo de corriente: 1 kHz < \(f_{sw}/10\). ✓

## Ejemplo de código

```python
import numpy as np

def vsc_avg(d_abc, vdc):
    """Modelo promediado: tensión de fase-neutro a partir de ciclos de trabajo."""
    vN = d_abc * vdc                    # tensión rama-N (d en [0,1])
    return vN - vN.mean()               # elimina modo común → fase-neutro

def pwm(t, m, fsw):
    """Generación conmutada: estado del interruptor superior (0 o 1)."""
    tri = 1.0 - 2.0 * np.abs(2.0 * ((t * fsw) % 1.0) - 1.0)
    return np.where(m > tri, 1.0, 0.0)

def idc_from_dq(vd, id_, vq, iq, vdc):
    """Corriente DC equivalente al intercambio de potencia AC (conv. amplitud)."""
    return 1.5 * (vd * id_ + vq * iq) / vdc

def deadtime_compensate(vref, ix, vdc, td, fsw):
    """Compensación de tiempo muerto: añade corrección según signo de corriente."""
    return vref + np.sign(ix) * vdc * td * fsw

# Ejemplo: VSC 1 MVA, 690 V, 1300 V DC
Vdc = 1300.0; Vll = 690.0; Vf = Vll * np.sqrt(2) / np.sqrt(3)
m = 2 * Vf / Vdc
print(f"m = {m:.3f}, margen = {(0.95-m)/0.95*100:.1f}%")   # m=0.867, margen=8.7%
```

## Parámetros y valores típicos

- \(f_{sw}\): 2–20 kHz (red). Índice de modulación de diseño \(m\approx0{,}8\)–\(0{,}95\) (lineal \(\le1\); SVPWM hasta 1.15).
- Tiempo muerto: 1–3 µs. Error de tensión: \(V_{dc}\,t_d\,f_{sw}\approx2\)–\(4\%\) de \(\hat{V}_f\).
- Rizado de corriente objetivo: 10–20% de \(I_n\) en red; determina \(L_1\).
- Validez del promediado: \(f_{sw}/f_{control}\gtrsim10\). En el proyecto: \(f_{sw}=10\) kHz, diferencia conmutado-promediado 0.67%.
- Rizado de bus DC: \(<1\)–\(2\%\) de \(V_{dc}\); determina \(C_{dc}\).

## Errores comunes

- Elegir \(V_{dc}\) demasiado bajo → saturación de modulación y distorsión.
- Sobremodular (\(m>1\)) sin querer → armónicos bajos y pérdida de control lineal.
- Pedir ancho de banda de control demasiado cercano a \(f_{sw}\) → el retraso ZOH reduce el margen de fase.
- Despreciar el tiempo muerto → distorsión de armónicos y error en el lazo de corriente; es especialmente relevante a cargas bajas donde el signo de la corriente cambia con frecuencia cerca de cero.
- Usar el modelo promediado más allá de \(f_{sw}/3\) → oculta inestabilidades de conmutación.
- Comparar conmutado y promediado sin filtrar el rizado y concluir que "no coinciden".
- Confundir las convenciones de amplitud (pico) y eficaz (RMS) en las fórmulas de potencia dq: el factor \(3/2\) es correcto con amplitudes pico; con RMS el factor es \(3\) (o \(1\) si se usa la convención de potencia invariante).

## Uso en proyectos

- **01 - GFM-Impedance** (justificar el modelo): `switched.py` demostró que el promediado captura la dinámica útil (diferencia 0.67%). Todo el análisis se hizo con el promediado. La función \(\hat{I}_{dc}=1{,}5\,(v_d i_d+v_q i_q)/V_{dc}\) se usó para el balance de potencia en el bus DC.

## Conceptos relacionados

[[topologias-multinivel]] · [[semiconductores-potencia]] · [[filtro-lcl]] · [[marco-dq]] · [[sistema-trifasico]] · [[potencia-instantanea-dq]] · [[medicion-impedancia-inyeccion]]

## Referencias

- Yazdani, Iravani, *Voltage-Sourced Converters in Power Systems*, Wiley 2010.
- Mohan, Undeland, Robbins, *Power Electronics*, Wiley.
- Erickson, Maksimovic, *Fundamentals of Power Electronics*, Springer.
- Holmes, Lipo, *Pulse Width Modulation for Power Converters*, IEEE Press 2003.
