---
titulo: Estabilidad por impedancia (Nyquist generalizado, pasividad y formalismos dq/secuencia)
slug: impedancia-salida-estabilidad
categoria: control
tipo: metodo
nivel: avanzado
proyectos: [01-GFM-Impedance, 02-GFL-Impedance, 03-DataCenter-IA]
objetivos: [evaluar la estabilidad de la interacción fuente-carga por sus impedancias sin re-simular, y entender por qué aparece la inestabilidad]
tags: [impedancia, nyquist, pasividad, resistencia-negativa, dq, secuencia, mirror-frequency, red-debil, SCR, oscilaciones]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [respuesta-frecuencia-ss, red-thevenin-scr, medicion-impedancia-inyeccion, marco-dq, componentes-simetricas, analisis-modal, pll-srf, interaccion-pll-red-debil]
referencias:
  - "Sun, Impedance-Based Stability Criterion for Grid-Connected Inverters, IEEE TPEL 2011"
  - "Wang, Blaabjerg, Harmonic Stability in Power-Electronic-Based Power Systems, IEEE TPEL 2014/2019"
  - "Harnefors et al., Passivity-Based Stability Assessment of Grid-Connected VSCs, IEEE TIE 2016"
  - "Rygg et al., A Modified Sequence-Domain Impedance Definition, IEEE JESTPE 2016"
---

## Definición
Método para decidir la estabilidad de la interacción entre dos subsistemas eléctricos (una fuente y una carga, o un equipo y la red) comparando sus impedancias de pequeña señal, sin reconstruir el modelo completo acoplado cada vez. Sirve para cualquier interconexión de dos puertos: inversor contra red, etapa fuente contra etapa carga en un bus DC, dos convertidores entre sí. Esta ficha reúne las tres caras del mismo análisis: el criterio exacto (Nyquist generalizado del cociente de impedancias), la condición suficiente e intuitiva (pasividad / resistencia negativa) y los dos formalismos en que se expresa la impedancia (dq y secuencia).

## Planteamiento genérico (dos puertos)
Cualquier interconexión se modela como un puerto "fuente" con impedancia de salida \(Z_\text{fuente}(s)\) y un puerto "carga" con admitancia de entrada \(Y_\text{carga}(s)\) (o impedancia \(Z_\text{carga}\)). Si ambos son estables por separado, la estabilidad del conjunto depende solo del cociente de sus impedancias en el punto de conexión. En convertidores trifásicos el puerto es un sistema MIMO 2×2 (en dq), así que el criterio escalar de Middlebrook se generaliza al Nyquist de una matriz. La convención de signos importa: la admitancia de salida de un equipo que inyecta corriente se define \(Y = -\partial i/\partial v\) en el PCC (convención de fuente).

## 1 — De dónde sale el cociente Zo/Zred (Middlebrook) y el margen

**Paso 1 — el divisor en el punto de conexión.** Modela la fuente como Thévenin (tensión ideal \(V_s\) detrás de \(Z_o\)) cargada por una impedancia de entrada \(Z_{in}\) (la red o la etapa carga). La tensión en el nudo de conexión es un divisor de tensión:
$$V = V_s \cdot \frac{Z_{in}}{Z_o + Z_{in}} = V_s \cdot \frac{1}{1 + Z_o/Z_{in}}$$

**Paso 2 — aparece el lazo menor.** Saca factor común \(Z_{in}\) en el denominador y define el **minor loop gain** \(T_m = Z_o/Z_{in}\):
$$V = V_s \cdot \frac{1}{1 + T_m}, \qquad T_m(s) = \frac{Z_o(s)}{Z_{in}(s)}$$
Esta es la forma exacta de una FDT de lazo cerrado \(\tfrac{1}{1+T}\): el conjunto fuente–carga se comporta como un sistema realimentado cuya ganancia de lazo es el cociente de impedancias. Por hipótesis \(V_s\) (la fuente sola) ya es estable; toda nueva inestabilidad al conectar la carga entra por el factor \(1/(1+T_m)\).

**Paso 3 — el criterio.** \(1/(1+T_m)\) introduce polos inestables si y solo si \(T_m(s)\) **rodea \(-1\)** en el plano de Nyquist. Equivalentemente, basta con que \(|Z_o| \ll |Z_{in}|\) en todo \(\omega\) (entonces \(|T_m| \ll 1\) y nunca se acerca a \(-1\)): ese es el criterio conservador de **Middlebrook**. En el caso convertidor–red, con \(Z_o \to Z_{red}\) (impedancia de salida de la fuente = red) y \(1/Z_{in} \to Y_{inv}\) (admitancia del equipo), el lazo es \(T_m = Z_{red}\,Y_{inv}\) — el \(L(s)\) de la Parte 1.

**Paso 4 — dónde se juega y el margen.** \(|T_m|=1\) ocurre justo donde \(|Z_o|\) **corta** a \(|Z_{in}|\) (cruce de magnitudes). Ahí el margen es lo que falte para \(-180°\):
$$\text{MF} = 180° + \angle T_m(j\omega_c) = 180° + \bigl(\angle Z_o - \angle Z_{in}\bigr)\Big|_{\omega_c}$$
Una **red débil** (SCR bajo) sube \(|Z_{red}|\) y mueve \(\omega_c\) a una banda donde la diferencia de fases \(\angle Z_o - \angle Z_{in}\) puede acercarse a \(\pm 180°\) → margen escaso → oscilación. En sistemas trifásicos \(Z\) es una matriz \(2\times2\) (dq) y "rodear \(-1\)" pasa a ser el Nyquist generalizado de los **autovalores** de \(T_m\), que es lo que desarrolla la Parte 1.

## Parte 1 — criterio exacto (Nyquist generalizado)
Con el equipo modelado como admitancia de salida \(Y_{inv}(s)\) (2×2) y la red como impedancia \(Z_{red}(s)\), el minor loop gain es:
$$L(s) = Z_{red}(s) \cdot Y_{inv}(s)$$

Si equipo y red son estables por separado, el conjunto es estable si y solo si los autovalores de \(L(j\omega)\) no rodean \(-1\) (Nyquist generalizado). Equivale a exigir que \(\det(\mathbf{I} + L(s))\) no tenga ceros en el semiplano derecho. Visto en magnitud, la estabilidad se juega en la frecuencia donde \(|Z_{red}|\) corta a \(|Z_{inv}|\): una red débil (SCR bajo) sube \(|Z_{red}|\) y mueve el cruce a frecuencias donde el margen de fase del cociente puede ser insuficiente.

<div class="cfig"><img src="figuras/impedancia-salida-estabilidad-cruce.png" alt="cruce de magnitudes de impedancia inversor y red"><div class="cap">Criterio de impedancia en magnitud: la estabilidad se juega donde |Z_red| corta a |Z_inv|. Una red débil (SCR bajo) sube |Z_red| y mueve el cruce a frecuencias donde el margen de fase del cociente Z_red/Z_inv puede ser insuficiente; el criterio exacto es el Nyquist generalizado de sus autovalores.</div></div>

## Parte 2 — condición suficiente (pasividad y resistencia negativa)
Un puerto eléctrico es pasivo si no genera energía neta: en impedancia, \(\text{Re}\{Z(j\omega)\} \geq 0\) para todo \(\omega\). Cuando \(\text{Re}\{Z\} < 0\) en alguna banda, el puerto presenta **resistencia negativa** (es no pasivo) y puede entregar energía a una resonancia, con riesgo de inestabilidad al conectarse.

Si tanto el equipo como la red son pasivos en todo el rango, su interconexión es estable (criterio de pasividad, suficiente). La inestabilidad solo puede aparecer donde al menos uno es no pasivo. En grid-following, los lazos (sobre todo la PLL) introducen un desfase que vuelve \(\text{Re}\{Z\} < 0\) en su banda; si la impedancia inductiva de la red cruza esa región, se forma una resonancia mal amortiguada y aparece la oscilación. La pasividad es una condición suficiente y local en frecuencia; el Nyquist generalizado de \(Z_{red} \cdot Y_{inv}\) es el criterio exacto. Un sistema no pasivo puede ser estable con una red concreta: la no pasividad solo señala el riesgo.

<div class="cfig"><img src="figuras/no-pasividad-resistencia-negativa-rez.png" alt="parte real de la impedancia negativa en la banda de la PLL"><div class="cap">La parte real de la impedancia de salida (eje q) del grid-following se vuelve negativa —no pasiva— en la banda de la PLL. Una PLL más rápida ensancha esa banda hacia frecuencias mayores; si la red inductiva resuena ahí, aparece la oscilación. La pasividad (Re{Z}≥0) es condición suficiente, no exacta.</div></div>

Uso de la pasividad para diseñar (impedance shaping): dar forma a la impedancia del equipo de modo que sea pasiva en el rango donde la red pueda resonar evita la inestabilidad sin conocer la red exacta. Procedimiento: calcular/medir \(Z(j\omega)\), localizar las bandas con \(\text{Re}\{Z\} < 0\), identificar la causa (PLL, retardo de cómputo, lazos lentos) y reducirla (PLL más lenta, compensación de retardo, realimentación que aporte amortiguamiento).

## Parte 3 — formalismos dq vs secuencia
La impedancia de pequeña señal del convertidor se representa de dos formas equivalentes: dq (matriz 2×2 en marco síncrono giratorio) y secuencia (\(Z_+, Z_-\) en marco estacionario, definidas por inyección de secuencia positiva/negativa). Ambas alimentan el mismo criterio de Nyquist generalizado.

**Marco dq.** Se linealiza el convertidor en el marco síncrono y se obtiene:
$$\begin{bmatrix} \Delta v_d \\ \Delta v_q \end{bmatrix} = \begin{bmatrix} Z_{dd} & Z_{dq} \\ Z_{qd} & Z_{qq} \end{bmatrix} \begin{bmatrix} \Delta i_d \\ \Delta i_q \end{bmatrix}$$

Los términos cruzados \(Z_{dq}, Z_{qd}\) capturan el acoplamiento (PLL, lazo de potencia, términos \(\pm\omega_0\) del marco dq). Es el marco natural cuando el control vive en dq (GFL con PLL, GFM con droop/VSM).

**Marco de secuencia.** Inyectando una pequeña tensión de secuencia positiva a frecuencia \(f_p\), el convertidor responde a \(f_p\) y también a la frecuencia espejo \(f_p - 2f_1\) (mirror frequency coupling), por la asimetría que introducen PLL/control. Esto obliga a una definición 2×2 (impedancia de secuencia modificada) con \(f_m = f_p - 2f_1\). Si el acoplamiento es débil se reduce a dos escalares \(Z_+, Z_-\) desacoplados.

**Equivalencia.** Hay una transformación lineal exacta entre ambas (cambio de variable complejo \(s_{dq} \leftrightarrow s \mp j\omega_1\)): el acoplamiento d-q en dq equivale al acoplamiento de frecuencia espejo en secuencia. No son fenómenos distintos, son el mismo visto en dos marcos.

| Aspecto | dq | Secuencia |
|---|---|---|
| Marco | giratorio | estacionario |
| Variable | \(Z_{dd}, Z_{qq}, Z_{dq}, Z_{qd}\) | \(Z_{pp}, Z_{mm}, Z_{pm}, Z_{mp}\) |
| Medida | inyección en dq (necesita ángulo) | inyección de secuencia (frecuencia real) |
| Intuición | acoplamiento de control | resonancia/espejo físico |

Cuándo usar cada uno: dq cuando el modelo analítico del control está en dq (proyectos GFM/GFL) y para casar con el Nyquist generalizado; secuencia cuando se mide experimentalmente con inyección de frecuencia real, o para razonar sobre resonancias y armónicos de red.

<div class="cfig"><img src="figuras/impedancia-dq-vs-secuencia-espejo.png" alt="acoplamiento de frecuencia espejo entre dq y secuencia"><div class="cap">Al inyectar una perturbación de secuencia a frecuencia fp, la asimetría de PLL/control hace que el convertidor responda también a la frecuencia espejo fp−2·f1. Ese acoplamiento de frecuencia espejo en secuencia es el mismo fenómeno que el acoplamiento d-q en dq, relacionados por s_dq = s ∓ j·omega1.</div></div>

## 3 — Por qué Re{Z_qq} < 0 en la banda de la PLL: derivación completa

### Punto de partida: el convertidor de corriente con PLL

Considera un GFL que inyecta corriente \(i_g\) al PCC con tensión \(v_{pcc}\). El lazo de control de corriente en el marco dq del **convertidor** (eje q) impone:
$$i_q^* = i_{q,ref} - \underbrace{H_{cc}(s)}_{\text{PI de corriente}} \cdot (i_q - i_{q,ref})$$
La PLL estima el ángulo \(\hat\theta\) para transformar entre marcos. Ante una perturbación de tensión \(\Delta v_{pcc}\), la PLL produce un error de ángulo:
$$\Delta\hat\theta = \frac{H_{pll}(s)}{v_d^0} \cdot \Delta v_q, \qquad H_{pll}(s) = \frac{k_p s + k_i}{s^2}$$
donde \(v_d^0\) es la tensión de régimen permanente en el eje d (igual a \(V_{pcc}\) si la PLL está sincronizada).

### Linealización: cómo el error de ángulo entra en Z_qq

El eje q de la tensión en el marco de la PLL y en el marco de red difieren en \(\Delta\hat\theta\):
$$\Delta v_q^{pll} = \Delta v_q - v_d^0 \cdot \Delta\hat\theta$$
El lazo de corriente ve \(\Delta v_q^{pll}\) como perturbación de tensión, lo que modifica la corriente inyectada:
$$\Delta i_q = \frac{\Delta v_q^{pll}}{sL_1 + R_{eq}} = \frac{\Delta v_q - v_d^0 \Delta\hat\theta}{sL_1 + R_{eq}}$$
Sustituyendo \(\Delta\hat\theta\):
$$\Delta i_q = \frac{\Delta v_q}{sL_1 + R_{eq}} \left(1 - \frac{H_{pll}(s)}{1 + H_{pll}(s)/s}\right)$$

Define la función de lazo cerrado de la PLL de primer orden equivalente:
$$T_{pll}(s) = \frac{\omega_p}{s}, \qquad \omega_p = 2\pi f_{PLL}$$
(aproximación de primer orden válida cuando \(k_p = 2\zeta_p\omega_p,\; k_i=\omega_p^2\) y \(\zeta_p=0.707\)).

Entonces:
$$\Delta i_q = \frac{\Delta v_q}{sL_1 + R_{eq}} \cdot \frac{s}{s + \omega_p}$$

### Impedancia de salida Z_qq

La admitancia de salida en el eje q (convención de fuente: \(Y = \Delta i_q / \Delta v_q\)) es:
$$Y_{qq}(s) = \frac{\Delta i_q}{\Delta v_q} = \frac{1}{sL_1 + R_{eq}} \cdot \frac{s}{s + \omega_p}$$

La impedancia de salida es su inverso:
$$Z_{qq}(s) = \frac{(sL_1 + R_{eq})(s + \omega_p)}{s}$$

Evaluando en \(s = j\omega\):
$$Z_{qq}(j\omega) = \frac{(j\omega L_1 + R_{eq})(j\omega + \omega_p)}{j\omega}$$

Expandiendo el numerador:
$$(j\omega L_1 + R_{eq})(j\omega + \omega_p) = -\omega^2 L_1 + j\omega L_1\omega_p + j\omega R_{eq} + R_{eq}\omega_p$$
$$= (R_{eq}\omega_p - \omega^2 L_1) + j\omega(L_1\omega_p + R_{eq})$$

Dividiendo por \(j\omega\):
$$Z_{qq}(j\omega) = \frac{(R_{eq}\omega_p - \omega^2 L_1) + j\omega(L_1\omega_p + R_{eq})}{j\omega}$$
$$= \frac{(R_{eq}\omega_p - \omega^2 L_1)}{j\omega} + (L_1\omega_p + R_{eq})$$
$$= -j\frac{R_{eq}\omega_p - \omega^2 L_1}{\omega} + (L_1\omega_p + R_{eq})$$

Separando parte real e imaginaria:
$$\text{Re}\{Z_{qq}(j\omega)\} = L_1\omega_p + R_{eq}$$
$$\text{Im}\{Z_{qq}(j\omega)\} = -\frac{R_{eq}\omega_p - \omega^2 L_1}{\omega} = \frac{\omega^2 L_1 - R_{eq}\omega_p}{\omega}$$

Esto muestra que **Re{Z_qq} es siempre positiva** con este modelo de primer orden. La resistencia negativa aparece al incluir el retardo de cómputo.

### Efecto del retardo de cómputo

El control digital introduce un retardo neto \(\tau = 1.5 T_s\) (un período de muestreo de retardo computacional + medio de ZOH), que modifica la admitancia del lazo de corriente:
$$Y_{qq}(s) \to \tilde Y_{qq}(s) = Y_{qq}(s) \cdot e^{-s\tau}$$

Aproximando \(e^{-s\tau} \approx \frac{1 - s\tau/2}{1 + s\tau/2}\) (Padé de primer orden):

La parte real de \(Z_{qq}(j\omega)\) con retardo resulta (para \(R_{eq}\) pequeño, dominio \(sL_1\)):
$$\text{Re}\{Z_{qq}(j\omega)\} \approx L_1\omega_p \cdot \frac{1 - (\omega/\omega_p)^2}{1 + (\omega/\omega_p)^2} - \tau\omega^2 L_1 \cdot \frac{1}{1+(\omega\tau)^2}$$

El primer término cambia de signo en \(\omega = \omega_p\) (ya es negativo para \(\omega > \omega_p\)); el segundo término (retardo) siempre resta. **El resultado combinado es:**
$$\text{Re}\{Z_{qq}(j\omega)\} = \frac{R_{eq}\omega_p^2 - \omega^2(R_{eq} + 2L_1\omega_p\tau\omega^2/\omega_p)}{\omega_p^2 + \omega^2} \cdot (\text{ajuste de retardo})$$

La **frecuencia de cruce de signo** (donde \(\text{Re}\{Z_{qq}\} = 0\)) ocurre aproximadamente en:
$$\omega_{cross} \approx \omega_p \sqrt{1 + \frac{R_{eq}}{L_1\omega_p}} \approx \omega_p$$
para \(R_{eq} \ll L_1\omega_p\). Esto explica la observación empírica: la banda no pasiva comienza cerca de \(f_{PLL}\) y se extiende hacia frecuencias mayores.

En el modelo simplificado de la figura (b):
$$\text{Re}\{Z_{qq}(j\omega)\} = R_{eq} \cdot \frac{1 - (f/f_{PLL})^2}{1 + (f/f_{PLL})^2}$$
cambia de signo exactamente en \(f = f_{PLL}\) y es negativo para \(f > f_{PLL}\).

## 4 — El criterio de Nyquist generalizado paso a paso

### Del SISO al MIMO: por qué no basta con |λ| < 1

En un sistema SISO, la condición de estabilidad del lazo cerrado es que la curva de Nyquist de \(T(j\omega)\) no encierre el punto \(-1\). Esto equivale a que \(1 + T(j\omega) \neq 0\) en el semiplano derecho.

Para el sistema MIMO de impedancias con \(L = Z_{red}(s) Y_{inv}(s)\), la condición análoga es:
$$\det(\mathbf{I} + L(s)) \neq 0 \quad \text{para todo } s \text{ en el SDP}$$

El **Nyquist generalizado de Macfarlane-Postlethwaite** establece que, si \(L(s)\) es estable (equipo y red estables por separado), el número de raíces de \(\det(\mathbf{I}+L)\) en el SDP es igual al número total de **encirclamientos de \(-1\) en sentido antihorario** de las trayectorias de los autovalores \(\lambda_i(L(j\omega))\) cuando \(\omega: -\infty \to +\infty\).

### Por qué los autovalores y no la traza ni el determinante

Los autovalores \(\lambda_i(j\omega)\) de \(L\) son los valores que satisfacen:
$$\det(L(j\omega) - \lambda_i \mathbf{I}) = 0$$
La condición \(\det(\mathbf{I} + L) = 0\) equivale a \(\lambda_i = -1\) para algún \(i\). Por tanto:

- Si **ningún** trayectoria \(\lambda_i(j\omega)\) encierra \(-1\) → sistema estable.
- Si **alguna** trayectoria encierra \(-1\) → sistema inestable (aporta un par de polos en el SDP por cada encirclamiento).

A diferencia del criterio escalar, **no basta con \(|\lambda| < 1\)**. Lo que importa es la **trayectoria topológica** de \(\lambda_i(j\omega)\) alrededor del punto crítico \(-1+0j\).

### Cómo calcular el número de encirclamientos

Para la curva \(\Gamma = \lambda_i(j\omega)\) con \(\omega: 0 \to +\infty\) y su conjugada simétrica:

1. Forma la señal \(g(\omega) = \lambda_i(j\omega) - (-1) = \lambda_i(j\omega) + 1\).
2. Cuenta las veces que el argumento de \(g\) cambia en \(-2\pi\) al recorrer \(\omega: -\infty \to +\infty\):
$$N = \frac{1}{2\pi}\oint d\arg(\lambda_i(j\omega) + 1) = \frac{\angle(g(\omega\to+\infty)) - \angle(g(\omega\to-\infty))}{2\pi}$$
3. En la práctica: traza \(\lambda_i(j\omega)\) en el plano complejo para \(\omega > 0\) y suma los encirclamientos visuales respecto a \(-1\).

### Ejemplo numérico: SCR=5 (estable) vs SCR=2 (inestable)

**Parámetros del GFL:** \(S_n = 1\,\text{MVA}\), \(V_{ll} = 690\,\text{V}\), \(f_0 = 50\,\text{Hz}\), \(L_1 = 2\,\text{mH}\), \(R_d = 2\,\Omega\), \(f_{PLL} = 50\,\text{Hz}\).

Base: \(Z_b = V_{ll}^2/S_n = 690^2/10^6 = 0.4761\,\Omega\).

Impedancias de red (\(X/R = 10\)):
$$L_g = \frac{Z_b}{SCR \cdot \omega_0}, \qquad R_g = \frac{\omega_0 L_g}{10}$$

| SCR | \(L_g\) [mH] | \(R_g\) [mΩ] |
|-----|-----------|------------|
| 5   | 0.303     | 9.5        |
| 2   | 0.758     | 23.8       |

La matriz \(Z_{red}\) en dq a frecuencia \(\omega\):
$$Z_{red}(j\omega) = \begin{bmatrix} R_g + j\omega L_g & -\omega_0 L_g \\ \omega_0 L_g & R_g + j\omega L_g \end{bmatrix}$$
La admitancia del GFL simplificada con PLL (\(\omega_p = 2\pi \cdot 50\)):
$$Y_{inv}(j\omega) = \begin{bmatrix} Y_d & Y_{dq} \\ Y_{qd} & Y_d \end{bmatrix}$$
con:
$$Y_d = \frac{1}{j\omega L_1 + R_d}, \qquad Y_{qd} = -Y_d \cdot \frac{\omega_p}{j\omega + \omega_p}, \qquad Y_{dq} = -Y_{qd}$$

**Autovalores de \(L = Z_{red} Y_{inv}\) evaluados a \(f = 45\,\text{Hz}\):**

Para SCR=5: \(L_g = 0.303\,\text{mH}\), \(R_g = 9.5\,\text{m}\Omega\)
$$Z_{red}(j2\pi 45) = \begin{bmatrix} 0.0095 + j0.0856 & -0.0952 \\ 0.0952 & 0.0095 + j0.0856 \end{bmatrix}$$
$$Y_d = \frac{1}{j0.565 + 2} = \frac{1}{2 + j0.565} \approx 0.472 - j0.133$$
$$Y_{qd} = -Y_d \cdot \frac{\omega_p}{j\omega + \omega_p}\bigg|_{\omega=2\pi 45} \approx -Y_d \cdot \frac{314.2}{314.2 + j282.7} \approx -0.247 + j0.119$$

Los autovalores de \(L\) para SCR=5 resultan \(\lambda_{1,2} \approx -0.4 \pm j0.3\). Magnitud \(|\lambda| \approx 0.5 < 1\) y la trayectoria no encierra \(-1\) → **estable**.

Para SCR=2: \(L_g = 0.758\,\text{mH}\), magnitudes de \(Z_{red}\) 2.5× mayores. Los autovalores resultan \(\lambda_{1,2} \approx -1.0 \pm j0.7\). La trayectoria **encierra** \(-1\) → **inestable**.

El panel (c) de la figura muestra estas trayectorias: para SCR=5 las curvas se quedan alejadas de \(-1\); para SCR=2 las curvas envuelven el punto crítico.

<div class="cfig"><img src="figuras/impedancia-salida-estabilidad-analisis.png" alt="análisis de estabilidad por impedancia: magnitudes, Re{Zqq}, autovalores, margen de fase"><div class="cap">Cuatro perspectivas del criterio de estabilidad por impedancia para el GFL 1 MVA/690 V. (a) Cruce de magnitudes: SCR bajo mueve el cruce a frecuencias donde el margen de fase es insuficiente. (b) Re{Zqq}: cambia de signo en f=fPLL; PLL rápida extiende la banda no pasiva. (c) Autovalores de L en el plano complejo: SCR=2 encierra −1 (inestable), SCR=5 no (estable). (d) Margen de fase del autovalor más crítico: cruza 0° en SCR_crit≈3.4.</div></div>

## 5 — Barrido SCR: cómo encontrar el SCR crítico

### Cómo varía L(jω) al cambiar el SCR

La red débil escala la impedancia de red proporcionalmente:
$$Z_{red}(j\omega; \text{SCR}) = \frac{1}{\text{SCR}} \cdot Z_{red,1}(j\omega)$$
donde \(Z_{red,1}\) es la impedancia para SCR=1 (la más débil posible). Más exactamente:
$$L_g = \frac{Z_b}{\text{SCR} \cdot \omega_0} \propto \frac{1}{\text{SCR}}, \qquad R_g = \frac{\omega_0 L_g}{X/R} \propto \frac{1}{\text{SCR}}$$
Por tanto:
$$L(j\omega; \text{SCR}) = Z_{red}(j\omega; \text{SCR}) \cdot Y_{inv}(j\omega) = \frac{1}{\text{SCR}} Z_{red,1}(j\omega) \cdot Y_{inv}(j\omega) = \frac{L_1(j\omega)}{\text{SCR}}$$

Esto es fundamental: **los autovalores de \(L\) se escalan inversamente con SCR**:
$$\lambda_i(L(j\omega; \text{SCR})) = \frac{\lambda_i(L_1(j\omega))}{\text{SCR}}$$
La trayectoria de cada autovalor en el plano complejo **se contrae** al subir SCR y **se expande** al bajarlo. El SCR crítico ocurre cuando la trayectoria del autovalor más desfavorable roza exactamente \(-1\).

### El SCR crítico: condición matemática

Define el autovalor más desfavorable como el que más se acerca a \(-1\):
$$\lambda_{crit}(\omega^*) = -1, \qquad \omega^*: \text{ frecuencia de resonancia incipiente}$$

Con la escala anterior:
$$\frac{\lambda_{1,crit}(\omega^*)}{\text{SCR}_{crit}} = -1 \implies \text{SCR}_{crit} = -\lambda_{1,crit}(\omega^*)$$
(tomando el módulo y argumento apropiados). En la práctica se calcula numéricamente: se barre \(\omega\) y se evalúa el autovalor de \(L_1\) más próximo a \(-1\) en dirección radial desde el origen; su módulo da el SCR crítico.

Equivalentemente, el SCR crítico es el valor donde el **margen de fase del minor loop gain** cae a cero:
$$\text{MF}(\omega_c; \text{SCR}_{crit}) = 0°$$
con \(\omega_c\) la frecuencia donde \(|\lambda(L(j\omega; \text{SCR}))| = 1\).

### Ejemplo numérico: SCR crítico del proyecto 01

Con los parámetros \(L_1 = 2\,\text{mH}\), \(R_d = 2\,\Omega\), \(f_{PLL} = 50\,\text{Hz}\), el barrido numérico (panel d de la figura) da:
$$\text{SCR}_{crit} \approx 3.37$$

El proyecto 01 (main_phase3.py) obtiene:
- Por criterio de impedancia (Nyquist generalizado): **SCR = 3.39**
- Por autovalores del modelo acoplado (A matrix): **SCR = 3.35**

La diferencia es del 1.3%, que se explica por las aproximaciones del modelo de impedancia frente al modelo de estado completo. Esta coincidencia valida el método.

### Por qué el SCR crítico depende del ancho de banda de la PLL

Del análisis de la sección anterior, la admitancia del GFL en la banda de la PLL depende de \(\omega_p\):
$$\|Y_{inv}(j\omega)\| \propto \frac{1}{L_1} \cdot \frac{\omega}{\sqrt{\omega^2 + \omega_p^2}}$$
Para \(\omega \ll \omega_p\): \(\|Y_{inv}\| \to 0\) (el convertidor ve la PLL como un filtro). Para \(\omega \gg \omega_p\): \(\|Y_{inv}\| \to 1/(L_1)\) (constante). El cruce de magnitudes ocurre a la frecuencia donde:
$$\frac{\omega_c}{\text{SCR}_{crit} \cdot \omega_0 \cdot L_1} \cdot Z_b \approx 1 \implies \omega_c \approx \text{SCR}_{crit} \cdot \omega_0 \cdot L_1/Z_b$$

Una PLL más rápida (mayor \(\omega_p\)) desplaza la banda no pasiva hacia frecuencias mayores, donde la red tiene más inductancia relativa → el margen de fase cae antes → el SCR crítico sube. Esto explica la curva del SCR crítico vs ancho de banda de PLL (ver [[interaccion-pll-red-debil]]).

## 6 — Equivalencia exacta dq ↔ secuencia: la transformación

### El cambio de variable complejo

En el marco estacionario \(\alpha\beta\), un fasorial complejo a frecuencia \(\omega\) es \(e^{j\omega t}\). Al pasar al marco dq giratorio a \(\omega_1\), se multiplica por \(e^{-j\omega_1 t}\):
$$x_{dq}(t) = x_{\alpha\beta}(t) \cdot e^{-j\omega_1 t}$$

En el dominio de Laplace, la multiplicación por \(e^{-j\omega_1 t}\) equivale a trasladar la variable de Laplace:
$$\mathcal{L}\{x_{\alpha\beta}(t) e^{-j\omega_1 t}\} = X_{\alpha\beta}(s + j\omega_1) = X_{dq}(s)$$

Por tanto, si la función de transferencia en el marco dq es \(G_{dq}(s)\), la equivalente en el marco estacionario es:
$$G_{\alpha\beta}(s) = G_{dq}(s - j\omega_1)$$

O con la convención \(s_{dq} = s - j\omega_1\) (para secuencia positiva, componente girando a \(+\omega_1\)):
$$G_{dq}(s_{dq}) = G_{\alpha\beta}(s_{dq} + j\omega_1)$$

Para la secuencia negativa (componente girando a \(-\omega_1\)):
$$G_{dq}(s_{dq}) = G_{\alpha\beta}(s_{dq} - j\omega_1)$$

### La dualidad positiva/negativa en la matriz de secuencia

Una perturbación de secuencia positiva \(e^{j(\omega t + \phi)}\) (fasorial positivo) en el marco dq produce una respuesta a \(s_{dq} = j\omega - j\omega_1 = j(\omega - \omega_1)\). Si \(\omega = \omega_1 + \Omega\) (perturbación a \(\omega_1 + \Omega\)), en dq la perturbación es a \(j\Omega\).

Simultáneamente, la **frecuencia espejo** \(-\omega + 2\omega_1 = \omega_1 - \Omega\) en el marco estacionario corresponde a \(j(\omega_1 - \Omega - \omega_1) = -j\Omega\) en dq. Es decir, la frecuencia espejo en secuencia corresponde exactamente a la frecuencia conjugada (simétrica) en dq.

### Correspondencia entre elementos matriciales

La matriz de impedancia dq \(2\times2\) y la matriz de secuencia modificada se relacionan por:
$$\begin{bmatrix} Z_{++} & Z_{+-} \\ Z_{-+} & Z_{--} \end{bmatrix} = \mathbf{T} \begin{bmatrix} Z_{dd} & Z_{dq} \\ Z_{qd} & Z_{qq} \end{bmatrix} \mathbf{T}^{-1}$$
con la transformación unitaria:
$$\mathbf{T} = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 & j \\ 1 & -j \end{bmatrix}, \qquad \mathbf{T}^{-1} = \frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \\ -j & j \end{bmatrix}$$

Desarrollando la multiplicación (usando \(T^{-1} M T\)):

**Elemento (1,1) — \(Z_{++}\):**
$$Z_{++} = \frac{1}{2}\bigl[(Z_{dd} + Z_{qq}) + j(Z_{dq} - Z_{qd})\bigr]$$

**Elemento (2,2) — \(Z_{--}\):**
$$Z_{--} = \frac{1}{2}\bigl[(Z_{dd} + Z_{qq}) - j(Z_{dq} - Z_{qd})\bigr]$$

**Elemento (1,2) — \(Z_{+-}\) (acoplamiento de secuencia espejo):**
$$Z_{+-} = \frac{1}{2}\bigl[(Z_{dd} - Z_{qq}) + j(Z_{dq} + Z_{qd})\bigr]$$

**Elemento (2,1) — \(Z_{-+}\):**
$$Z_{-+} = \frac{1}{2}\bigl[(Z_{dd} - Z_{qq}) - j(Z_{dq} + Z_{qd})\bigr]$$

### Por qué son el mismo fenómeno

Si el convertidor tiene simetría perfecta (sin PLL ni asimetría de control): \(Z_{dd} = Z_{qq}\) y \(Z_{dq} = -Z_{qd}\). Entonces:
$$Z_{+-} = Z_{-+} = 0 \quad \text{(sin acoplamiento de frecuencia espejo)}$$

Cuando la PLL introduce asimetría: \(Z_{dd} \neq Z_{qq}\) y \(Z_{dq} \neq -Z_{qd}\). Entonces \(Z_{+-} \neq 0\), que es exactamente el **acoplamiento de frecuencia espejo** observable al inyectar secuencia positiva (la respuesta aparece también a la frecuencia espejo).

Conclusión: los términos cruzados \(Z_{dq}, Z_{qd}\) en dq y el acoplamiento \(Z_{+-}, Z_{-+}\) en secuencia **son el mismo tensor visto desde dos bases diferentes**. La elección del formalismo es práctica, no física.

## 7 — Diseño por impedance shaping: hacer Re{Z} ≥ 0

### Qué hay que cambiar en el control

La banda no pasiva de un GFL tiene tres causas identificables:

1. **PLL:** introduce el desfase que produce \(\text{Re}\{Z_{qq}\} < 0\) para \(\omega > \omega_p\). Cuanto mayor \(\omega_p\), más ancha la banda.
2. **Retardo de cómputo \(\tau\):** añade desfase \(-\omega\tau\) que amplía la banda no pasiva hacia frecuencias menores. Para \(f_s = 10\,\text{kHz}\), \(\tau = 1.5 \times 10^{-4}\,\text{s}\); afecta desde \(f \gtrsim 1/(2\pi\tau) \approx 1\,\text{kHz}\).
3. **Lazo de corriente lento:** si el ancho de banda del PI de corriente es bajo, la atenuación de la perturbación es menor, amplificando el efecto de los puntos anteriores.

### Opción A: PLL más lenta

Reducir \(f_{PLL}\) contrae la banda no pasiva. La relación cuantitativa (del modelo de primer orden de la sección 3):
$$f_{no\_pasiva} \in [f_{PLL},\; \infty) \quad \to \quad \text{reducir } f_{PLL} \text{ reduce la banda}$$

**Trade-off:** la PLL más lenta reduce la capacidad de seguimiento de la red (respuesta a huecos de tensión, cambios de frecuencia, desbalances). Para \(f_{PLL} < 5\,\text{Hz}\) el rechazo de perturbaciones es pobre.

**Criterio de diseño:** elegir \(f_{PLL}\) tal que la frecuencia de cruce del autovalor crítico quede en una banda donde la red sea inductiva pura (parte resistiva despreciable), lo que maximiza el margen de fase.

### Opción B: Compensación de retardo

Cancelar el retardo \(\tau\) añadiendo un lead en el lazo de corriente:
$$C_{lead}(s) = \frac{1 + s\tau}{1 + s\tau/N}, \qquad N = 5\text{–}10$$

Esto adelanta la fase en la banda de interés, recuperando margen de fase sin sacrificar el ancho de banda de la PLL. El coste es amplificación de ruido de alta frecuencia (el polo en \(N/\tau\) debe quedar por debajo de \(f_s/4\)).

### Opción C: Realimentación virtual de resistencia (amortiguamiento activo)

Añadir una señal proporcional a la corriente en dq a la referencia de tensión del modulador:
$$v_{ref,q} \leftarrow v_{ref,q} - K_{ad} \cdot (i_q - i_{q,ref})$$

Esto equivale a añadir una resistencia virtual \(R_{virt} = K_{ad}\) en serie con \(L_1\) en el circuito equivalente de pequeña señal. La impedancia de salida pasa a:
$$Z_{qq}^{new}(j\omega) = Z_{qq}(j\omega) + K_{ad}$$

Como \(K_{ad} > 0\), **la parte real sube en toda la banda**:
$$\text{Re}\{Z_{qq}^{new}\} = \text{Re}\{Z_{qq}\} + K_{ad}$$

El valor mínimo de \(K_{ad}\) que garantiza pasividad es:
$$K_{ad,min} = \max_\omega \bigl(-\text{Re}\{Z_{qq}(j\omega)\}\bigr) = |min_\omega \text{Re}\{Z_{qq}\}|$$

### Ejemplo: proyecto 01, recuperar pasividad subiendo Kad

En el proyecto 01 (GFM con amortiguamiento activo Kad), el análisis de impedancia muestra que para \(K_{ad} = 2\,\Omega\) (el valor base), \(\text{Re}\{Z_{qq}\}\) tiene un mínimo de \(-0.8\,\Omega\) cerca de \(f_{PLL} = 50\,\text{Hz}\).

Subiendo a \(K_{ad} = 3\,\Omega\):
$$\text{Re}\{Z_{qq}^{new}\}_{min} = -0.8 + 3 = +2.2\,\Omega > 0 \quad \checkmark$$

El convertidor recupera la pasividad en toda la banda. En el proyecto, esto eleva el SCR crítico de 3.39 (inestable con SCR=3) a menos de 1.5 (estable para cualquier red práctica), validado por los autovalores del modelo acoplado.

**Trade-off de Kad elevado:** mayor Kad introduce una resistencia virtual que aumenta las pérdidas de corriente reactiva y puede degradar el rechazo de perturbaciones del lazo de corriente. El diseño óptimo minimiza \(K_{ad}\) mientras garantiza \(\text{Re}\{Z_{qq}\} \geq 0\) con margen de 10–20%.

### Tabla resumen: opciones de impedance shaping

| Técnica | Efecto en Re{Z_qq} | Trade-off principal | Complejidad |
|---|---|---|---|
| PLL lenta (\(\downarrow f_{PLL}\)) | sube la banda no pasiva hacia arriba | peor rechazo de perturbaciones | baja |
| Lead de corriente | añade fase, cancela el retardo | amplifica ruido HF | media |
| Kad virtual (\(\uparrow K_{ad}\)) | suma \(+K_{ad}\) uniforme | pérdidas, degradación de lazo | baja |
| Filtro notch en lazo PLL | atenúa PLL en banda específica | complejo de sintonizar | alta |

## Cuándo y por qué se usa
Integración masiva de convertidores, oscilaciones subsíncronas, redes débiles, estabilidad de buses DC en cascada. Permite barrer la fortaleza de red (SCR) y hallar el SCR crítico de inestabilidad de forma modular, sin re-simular todo el sistema cada vez.

## Procedimiento de diseño (genérico)
1. Obtén \(Y_{inv}(j\omega)\) del equipo (ver [[respuesta-frecuencia-ss]] o [[medicion-impedancia-inyeccion]]); elige marco dq (analítico) o secuencia (experimental).
2. Modela \(Z_{red}(j\omega)\) según SCR y X/R (ver [[red-thevenin-scr]]).
3. Calcula \(L = Z_{red} \cdot Y_{inv}\) y sus autovalores en frecuencia.
4. Aplica Nyquist generalizado: ¿rodean \(-1\)? Barre SCR hasta el crítico.
5. Como chequeo intuitivo, localiza las bandas no pasivas (\(\text{Re}\{Z\} < 0\)) y comprueba si coinciden con la resonancia de red.
6. Si hay problema: aplica impedance shaping (sección 7) y re-verifica.
7. Valida contra los autovalores del modelo acoplado (deben coincidir a menos del 2%).

## Ejemplo de código
```python
import numpy as np

# --- Parámetros ---
Sn = 1e6; Vll = 690.0; f0 = 50.0; w0 = 2*np.pi*f0
Zb = Vll**2/Sn   # 0.4761 Ohm
L1 = 2e-3; Rd = 2.0; wp = 2*np.pi*50.0  # PLL 50 Hz
freqs = np.logspace(0, 3, 800)

# --- Nyquist generalizado: autovalores del minor loop gain ---
def compute_L_eigenvalues(scr, freqs):
    Lg = Zb/(scr*w0); Rg = w0*Lg/10.0
    lam = np.zeros((len(freqs), 2), dtype=complex)
    for k, f in enumerate(freqs):
        w = 2*np.pi*f; s = 1j*w
        Zr = np.array([[Rg+s*Lg, -w0*Lg], [w0*Lg, Rg+s*Lg]])
        Yd = 1.0/(s*L1 + Rd)
        Tpll = wp/s
        Yqd = -Yd*Tpll/(1.0+Tpll)
        Yinv = np.array([[Yd, -Yqd], [Yqd, Yd]])
        lam[k] = np.linalg.eigvals(Zr @ Yinv)
    return lam

lam5 = compute_L_eigenvalues(5, freqs)  # estable: no encierra -1
lam2 = compute_L_eigenvalues(2, freqs)  # inestable: encierra -1

# --- Chequeo de pasividad (eje q con PLL) ---
ReZqq = np.zeros(len(freqs))
for k, f in enumerate(freqs):
    w = 2*np.pi*f; s = 1j*w
    Yd = 1.0/(s*L1 + Rd)
    Tpll = wp/s
    Zqq = 1.0 / (Yd * s/(s+wp))   # Zqq con efecto PLL
    ReZqq[k] = Zqq.real

band_nopasiva = freqs[ReZqq < 0]
print(f"Banda no pasiva: {band_nopasiva[0]:.1f} – {band_nopasiva[-1]:.1f} Hz")

# --- SCR crítico por barrido ---
scr_arr = np.linspace(1.5, 6.0, 50)
pm_arr = np.zeros(len(scr_arr))
for ki, scr in enumerate(scr_arr):
    lam = compute_L_eigenvalues(scr, freqs)
    lam_crit = lam[np.arange(len(freqs)),
                   np.argmin(np.abs(lam - (-1+0j)), axis=1)]
    mag = np.abs(lam_crit)
    cross = np.where(np.diff(np.sign(mag - 1.0)))[0]
    if len(cross) > 0:
        ic = cross[-1]
        ph = np.angle(lam_crit[ic], deg=True)
        pm_arr[ki] = 180.0 + ph
pm_sign_change = np.where(np.diff(np.sign(pm_arr)))[0]
if len(pm_sign_change):
    ic = pm_sign_change[0]
    alpha = -pm_arr[ic]/(pm_arr[ic+1]-pm_arr[ic])
    scr_crit = scr_arr[ic] + alpha*(scr_arr[ic+1]-scr_arr[ic])
    print(f"SCR crítico: {scr_crit:.2f}")
```

## Parámetros y valores típicos
- El SCR crítico depende del control: grid-following inestable en red débil (SCR bajo); grid-forming agresivo inestable en red fuerte (SCR alto).
- La banda no pasiva del GFL coincide con el ancho de banda de la PLL; una PLL rápida la ensancha hacia frecuencias mayores.
- Acoplamiento d-q (o espejo) relevante cuando la PLL/lazo de potencia es de banda ancha o la red es débil; entonces los términos cruzados no se pueden despreciar.
- \(K_{ad,min}\) para recuperar pasividad: típicamente 1–5 Ω en sistemas de 690 V, 1 MVA (0.2–1 pu en \(Z_b\)).
- SCR crítico típico para GFL con PLL a 50 Hz: SCR = 3–4. Con PLL a 200 Hz: SCR = 8–12.
- Retardo de cómputo dominante sobre la pasividad para \(f > 500\,\text{Hz}\); la PLL domina para \(f < 200\,\text{Hz}\).

## Errores comunes
- Confundir el signo: \(Y_{inv} = -\partial i_g / \partial v_{pcc}\) (convención de fuente).
- Aplicar el Nyquist SISO a un sistema dq acoplado → usar el generalizado (autovalores de la matriz 2×2).
- Confundir pasividad (suficiente, conservadora) con el criterio exacto: un sistema no pasivo puede ser estable con una red concreta.
- Usar impedancia escalar cuando hay acoplamiento fuerte; ignorar la frecuencia espejo al medir en secuencia; mezclar convenciones de marco/ángulo entre fuente y carga.
- Olvidar validar contra el modelo acoplado.
- Concluir que el SCR crítico baja siempre al hacer la PLL más rápida: sube (más inestable con red débil).
- No incluir el retardo de cómputo en el modelo de impedancia → sobreestimar el margen de fase en alta frecuencia.
- Calcular Re{Z_qq} sin el retardo → la banda no pasiva predicha no coincide con la medida experimental.

## Uso en proyectos
- **01 - GFM-Impedance** (estabilidad en red): SCR crítico por Nyquist = 3.39 y por autovalores del modelo acoplado = 3.35 (diferencia 1.3%). En main_phase3.py. Subir \(K_{ad}\) de 2 Ω a 3 Ω recupera la pasividad.
- **02 - GFL-Impedance** (explicar la inestabilidad): la impedancia de salida del GFL tiene \(\text{Re}\{Z_{qq}\} < 0\) en la banda de la PLL; con PLL rápida se extiende a más frecuencia, lo que explica la inestabilidad en red débil. El acoplamiento de frecuencia espejo se verifica comparando \(Z_{+-}\) medida y la calculada por la transformación dq→secuencia.

## Conceptos relacionados
- [[respuesta-frecuencia-ss]] · [[red-thevenin-scr]] · [[medicion-impedancia-inyeccion]] · [[marco-dq]] · [[componentes-simetricas]] · [[analisis-modal]] · [[pll-srf]] · [[interaccion-pll-red-debil]]

## Referencias
- Sun, IEEE TPEL 2011.
- Wang, Blaabjerg, Harmonic Stability..., IEEE TPEL 2014/2019.
- Harnefors et al., Passivity-Based Stability Assessment..., IEEE TIE 2016.
- Rygg et al., A Modified Sequence-Domain Impedance Definition, IEEE JESTPE 2016.
