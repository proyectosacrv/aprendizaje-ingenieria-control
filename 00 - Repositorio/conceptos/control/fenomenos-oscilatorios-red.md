---
titulo: Fenómenos oscilatorios de red (armónica y subsíncrona)
slug: fenomenos-oscilatorios-red
categoria: control
tipo: fenomeno
nivel: avanzado
proyectos: []
objetivos: [entender y mitigar las oscilaciones por interacción convertidor-red, tanto subsíncronas como de media-alta frecuencia]
tags: [estabilidad-armonica, oscilaciones-subsincronas, sso, ssci, resonancia, pasividad, resistencia-negativa, multi-convertidor, avanzado]
fecha_creacion: 2026-06-16
fecha_actualizacion: 2026-07-01
relacionados: [impedancia-salida-estabilidad, clasificacion-estabilidad, interaccion-pll-red-debil, filtro-lcl, red-thevenin-scr, compensacion-retardo, filtro-notch]
referencias:
  - "Wang, Blaabjerg, Harmonic Stability in Power-Electronic-Based Power Systems, IEEE TPEL 2014"
  - "Wang et al., Unified Impedance Model of Grid-Connected VSCs, IEEE TPEL 2018"
  - "IEEE SSR Working Group, Terms, Definitions and Symbols for Subsynchronous Oscillations, IEEE 1985"
  - "Irwin et al., Sub-synchronous control interactions between Type-3 wind turbines and series compensated transmission, IEEE PES 2011"
---

## Definición
Familia de inestabilidades oscilatorias que surgen de la interacción entre la impedancia de los convertidores (o generadores) y la de la red, distintas de la estabilidad electromecánica clásica. Se ordenan por banda de frecuencia: las oscilaciones subsíncronas (por debajo de la fundamental, típ. 5–100 Hz) y la resonancia/estabilidad armónica (de media-alta frecuencia, decenas de Hz a kHz). Las dos comparten el mismo mecanismo de fondo —resistencia negativa del control frente a una resonancia de red— y la misma herramienta de análisis (el criterio de impedancia / pasividad), por eso se tratan juntas.

## Mecanismo común (contexto genérico)
Cualquier equipo conectado a la red presenta una impedancia/admitancia de salida Z_o(j·omega) que, por culpa de sus lazos de control, su PLL y su retardo digital, tiene bandas donde se comporta como resistencia negativa (no pasivo): ahí Re{Z_o} < 0. Si esa banda coincide en frecuencia con una resonancia de la red (un paralelo o serie de inductancias y capacidades de cables, filtros o compensación serie), el amortiguamiento neto del lazo formado por ambas impedancias se vuelve negativo y aparece una oscilación sostenida o creciente. El convertidor no necesita ser "el malo": basta con que su no pasividad caiga sobre una resonancia que la red ya tenía. El equipo aguas arriba puede ser un parque eólico, una planta PV, un HVDC o cualquier conjunto de convertidores; el razonamiento es el mismo.

Marco de análisis (común a las dos bandas):
- Pasividad: si Re{Z_o(j·omega)} ≥ 0 para todo omega, el equipo no puede desestabilizar ninguna red pasiva (diseño passivity-based).
- Impedancia: aplicar Nyquist generalizado al cociente Z_o/Z_g (ver [[impedancia-salida-estabilidad]]).
- Multi-convertidor: N equipos en paralelo añaden resonancias y reparto de corriente; el modelo de impedancia unificada agrega sus admitancias.

Causas frecuentes de no pasividad: retardo de cómputo+PWM (del orden de 1.5·Ts), ancho de banda de la PLL, feedforward de tensión de red, y amortiguamiento insuficiente del [[filtro-lcl]].

## Parte 1 — oscilaciones subsíncronas (SSO / SSCI)
Oscilaciones de frecuencia inferior a la fundamental que se amplifican por la interacción entre convertidores (o generadores) y elementos de red, sobre todo líneas con compensación serie. Una línea con condensador serie Cs y reactancia XL resuena a:

fn = f1·raiz(X_Cs / XL) < f1

A esa frecuencia subsíncrona la red presenta baja impedancia. Mecanismos clásicos (SSR, con máquina rotativa):
- IGE (induction generator effect): a fn la resistencia equivalente del generador es negativa → autoexcitación eléctrica.
- TI (torsional interaction): fn excita modos torsionales del eje turbina-generador.
- TA (transient torque): pares de eje grandes tras faltas.

SSCI (subsynchronous control interaction): la variante moderna sin partes mecánicas, propia de eólica Tipo-3/4. Es puramente control-red: el control del convertidor (lazo de corriente, PLL) presenta a frecuencias subsíncronas una resistencia negativa que, combinada con la resonancia serie, da amortiguamiento neto negativo. Es rápida (puede crecer en ciclos) y depende fuertemente del nivel de compensación y del SCR. La inestabilidad aparece donde Re{Z_conv + Z_red} < 0 cerca de fn.

<div class="cfig"><img src="figuras/oscilaciones-subsincronas-resonancia.png" alt="frecuencia de resonancia serie y oscilacion subsincrona creciente"><div class="cap">Izquierda: una línea con compensación serie resuena a fn=f1·raiz(X_Cs/XL), que cae en la banda subsíncrona (≈10–45 Hz). Derecha: si el convertidor presenta resistencia negativa cerca de fn, el amortiguamiento neto es negativo y la oscilación (SSCI) crece en pocos ciclos, sin modos mecánicos.</div></div>

## Parte 2 — estabilidad y resonancia armónica
Inestabilidad de media-alta frecuencia (decenas de Hz a kHz) que se manifiesta como oscilaciones armónicas sostenidas o crecientes. Cada convertidor presenta Z_o(j·omega) con regiones de resistencia negativa (no pasivo), típicamente alrededor de la frecuencia de cruce del control, de la PLL o por el retardo digital. Si la fase de Z_o sale de (−90°, +90°) en una frecuencia donde coincide con una resonancia de red (paralelo Lg-C de cables/filtros), el amortiguamiento neto se vuelve negativo y aparece la oscilación. Es la versión de alta frecuencia del mismo análisis por impedancia, y la banda donde es crítico el amortiguamiento del filtro LCL.

<div class="cfig"><img src="figuras/estabilidad-armonica-pasividad.png" alt="parte real de la impedancia de salida con region no pasiva"><div class="cap">La parte real de la impedancia de salida Z_o del convertidor se vuelve negativa en una banda (sobre todo por el retardo digital): ahí es no pasivo. Si esa región coincide con una resonancia de red, el amortiguamiento neto es negativo y aparece la oscilación armónica.</div></div>

## 3 — Modos oscilatorios electromecánicos: la ecuación de swing y el PSS

**La ecuación de swing.** El ángulo del rotor \( \delta \) de un generador (o convertidor con inercia virtual) obedece:

$$ M\frac{d^2\delta}{dt^2} + D\frac{d\delta}{dt} + K_s \sin\delta = T_m $$

donde \( M = 2H/\omega_0 \) es la inercia, \( D \) el coeficiente de amortiguamiento, \( K_s = EV/X \) la rigidez sincronizante y \( T_m \) el par mecánico de entrada. Linealizando en torno a un punto de operación \( \delta_0 \) (con \( \sin\delta \approx \sin\delta_0 + \cos\delta_0 \cdot \Delta\delta \)):

$$ M\Delta\ddot{\delta} + D\Delta\dot{\delta} + K_s \cos\delta_0 \cdot \Delta\delta = 0 $$

Esta es una EDO de segundo orden con frecuencia natural:

$$ \omega_n = \sqrt{\frac{K_s \cos\delta_0}{M}}, \qquad \zeta = \frac{D}{2\omega_n M} $$

**Modos locales y modos inter-área.**

- **Modos locales (1–3 Hz):** oscilación del rotor de un grupo generador frente al resto del sistema. Frecuencia dominada por la reactancia de la máquina y de la línea de transmisión local. Se amortiguan con el PSS local.
- **Modos inter-área (0.1–0.8 Hz):** oscilación de un grupo de generadores de una región frente a los de otra región. Involucra la inercia agregada de subsistemas y la reactancia de las líneas de interconexión. Más difíciles de amortiguar porque la frecuencia es muy baja y el lazo es de gran escala.

**El PSS (Power System Stabilizer).** El PSS es un controlador que añade amortiguamiento activo al modo electromecánico inyectando una señal adicional \( \Delta v_{PSS} \) en la excitación de la máquina. La señal se construye a partir de la velocidad angular \( \Delta\omega \) (o la aceleración \( d\Delta\omega/dt \) o la potencia eléctrica \( \Delta P_e \)) filtrada para estar en fase con \( \Delta\omega \) a la frecuencia del modo:

$$ \Delta v_{PSS} = K_{PSS} \cdot T_{wash}(s) \cdot T_{lead-lag}(s) \cdot \Delta\omega $$

donde \( T_{wash}(s) = sT_w/(1+sT_w) \) es un filtro paso-alto (washout) que elimina el error en régimen permanente y \( T_{lead-lag}(s) \) compensa el retraso de fase del bloque excitación-generador para que la señal llegue en fase con \( \Delta\omega \) a la frecuencia del modo.

**El PSS virtual en convertidores GFM.** En un GFM con droop o VSM, la ganancia de droop de potencia activa actúa como \( D \): \( D_{droop} = 1/R_p \). Aumentar \( D_{droop} \) es el PSS más simple: amortigua todos los modos pero puede degradar la respuesta transitoria. Un PSS virtual más sofisticado añade un filtro pasa-banda centrado en la frecuencia del modo, similar al PSS clásico.

## 4 — Oscilaciones subsíncronas (SSR / SSCI): el circuito resonante subsíncrono

**Resonancia serie en la línea.** Una línea de transmisión de reactancia \( X_L \) con compensación serie (condensador serie \( X_{Cs} \)) resuena a:

$$ f_{sub} = f_0 \sqrt{\frac{X_{Cs}}{X_L}} < f_0 $$

Para compensación del 40% (\( X_{Cs} = 0.4 X_L \)): \( f_{sub} = 50\sqrt{0.4} \approx 31.6\,\text{Hz} \). Esta es la frecuencia eléctrica subsíncrona a la que la impedancia de la línea compensada es mínima (resonancia serie).

**SSR con máquina rotativa (IEEE First Benchmark).** El IEEE First Benchmark Model (1977) demostró que la resonancia eléctrica a \( f_{sub} \) puede interaccionar con los modos torsionales del eje turbina-generador. Si \( f_{tor} \approx f_0 - f_{sub} \) (frecuencia de complemento), el modo eléctrico excita el modo mecánico y viceversa, en un bucle de retroalimentación positiva. Tres mecanismos:
- **IGE (Induction Generator Effect):** a \( f_{sub} \) la resistencia equivalente del generador sincrónico es negativa → autoexcitación eléctrica sin interacción mecánica.
- **TI (Torsional Interaction):** el modo eléctrico a \( f_{sub} \) excita el modo torsional a \( f_{tor} = f_0 - f_{sub} \) → oscilaciones crecientes del eje.
- **TA (Transient Torque):** pares de eje grandes tras faltas → excitación transitoria severa.

**SSCI (Subsynchronous Control Interaction):** el mecanismo moderno, sin partes mecánicas. El control del convertidor Tipo-3 o Tipo-4 presenta a frecuencias subsíncronas una resistencia negativa (no pasividad del lazo de corriente y la PLL). Si esa resistencia negativa cancela la resistencia positiva de la red en \( f_{sub} \), el amortiguamiento neto se vuelve negativo y aparece una oscilación que puede crecer en pocos ciclos (mucho más rápida que el SSR clásico, que tardaba segundos). El evento de ERCOT de 2009 es el caso más documentado.

## 5 — Oscilaciones de alta frecuencia por convertidores: armónicos del PWM y resonancias de cables

**Armónicos del PWM.** El modulador PWM produce corrientes a las frecuencias \( k f_{sw} \pm m f_0 \) (armónicos de banda lateral: \( f_{sw} \pm 2f_0 \), \( 2f_{sw} \pm f_0 \), etc.). Estos armónicos no son problem por sí solos en el bus de tensión, pero sí lo son si excitan una resonancia de red en esa frecuencia.

**Resonancias de cables en parques eólicos.** Un parque eólico offshore tiene cables de colección con capacidad distribuida significativa (típ. \( C_{cable} \approx 0.1\text{–}1\,\mu\text{F/km} \) × decenas de km). La inductancia del transformador eleva (1–10 mH) junto con esa capacidad produce resonancias paralelas a:

$$ f_{res,cable} = \frac{1}{2\pi\sqrt{L_{trafo} C_{cable}}} $$

típicamente en el rango 100–2000 Hz. Si \( f_{res,cable} \approx f_{sw} \pm m f_0 \), el armónico de PWM excita la resonancia y la corriente a esa frecuencia puede crecer hasta niveles que disparan las protecciones de THD.

**El problema del harmonic resonance en parques eólicos (harmonic amplification).** Con \( N \) turbinas en paralelo, la capacidad total se multiplica por \( N \) y la frecuencia de resonancia baja: \( f_{res} \propto 1/\sqrt{N} \). A medida que el parque crece, la resonancia de cables puede "bajar" hasta coincidir con armónicos de baja frecuencia del PWM, agravando el problema.

## 6 — Diseño iterativo: el GFM como amortiguador de modo inter-área de 0.5 Hz

Sistema: convertidor GFM de 1 MVA conectado a una red con un modo inter-área de 0.5 Hz y amortiguamiento natural \( \zeta_{red} = 0.02 \) (2%, casi sin amortiguar).

**Paso 1 — la ecuación de swing del modo inter-área.**

$$ M\Delta\ddot{\delta} + D_{red}\Delta\dot{\delta} + K_s \Delta\delta = 0, \quad \omega_n = 2\pi \times 0.5 = 3.14\,\text{rad/s} $$

Con \( \zeta_{red} = 0.02 \): \( D_{red} = 2\zeta_{red}\omega_n M = 2\times0.02\times3.14\times M \).

**Paso 2 — coeficiente de amortiguamiento necesario.** Para elevar \( \zeta \) a 0.10 (10%), se necesita:

$$ D_{total} = 2\times0.10\times\omega_n\times M \quad\Rightarrow\quad D_{GFM} = D_{total} - D_{red} = 2\omega_n M(\zeta_{target}-\zeta_{red}) = 2\times3.14\times M\times0.08 = 0.503\,M $$

**Paso 3 — el PSS virtual.** El GFM añade un término de amortiguamiento a través del droop de frecuencia:

$$ \Delta P_{GFM} = D_{droop}\,\Delta\omega = \frac{1}{R_p}\Delta\omega $$

Para que \( D_{droop} = D_{GFM} \) en el modo de 0.5 Hz, filtrando con un pasa-banda centrado en 0.5 Hz:

$$ K_{PSS,GFM} = D_{GFM} \cdot S_n = 0.503\,M \cdot S_n $$

Con \( H = 5\,\text{s} \), \( M = 2H/\omega_0 = 10/(2\pi\times50) = 0.032\,\text{s}^2 \), \( S_n = 1\,\text{MVA} \):

$$ K_{PSS,GFM} = 0.503\times0.032\times10^6 \approx 16\,\text{kW/(rad/s)} $$

Este valor se traduce en un estatismo virtual de frecuencia de \( R_p = 1/K_{PSS} \approx 60\,\mu\text{rad/s/W} \), compatible con el despacho normal del convertidor.

<div class="cfig"><img src="figuras/fenomenos-oscilatorios-red-analisis.png" alt="Fenómenos oscilatorios de red: mapa de frecuencias, modo inter-área, SSR y resonancia armónica"><div class="cap">(a) Mapa de fenómenos oscilatorios por banda de frecuencia: inter-área (0.1–2 Hz), modos locales (1–3 Hz), SSR/SSCI (5–50 Hz) y armónica HF (100–3000 Hz). (b) Modo inter-área de 0.5 Hz: el GFM inyecta amortiguamiento, zeta sube de 0.02 a 0.12. (c) SSR: componente subsíncrona creciente al activarse compensación serie. (d) Resonancia armónica HF: resonancia cable-transformador excitada por el PWM.</div></div>

## 1 — Condición de oscilación: \( \mathrm{Re}\{Z_{conv}+Z_{red}\}=0 \)

**Paso 1 — circuito equivalente.** Convertidor y red se conectan en serie desde el punto de vista de la impedancia. El convertidor GFL presenta una impedancia de salida \( Z_{conv}(j\omega) \) (determinada por sus lazos de control, PLL y retardo digital); la red aporta \( Z_{red}(j\omega) = R_g + j\omega L_g \). La corriente total de lazo circula por ambas en serie.

**Paso 2 — condición de resonancia con amortiguamiento nulo.** Para que exista una oscilación sostenida a la frecuencia \( \omega^* \) sin excitación externa, la impedancia total debe ser nula en esa frecuencia (condición de Barkhausen generalizada para impedancias en serie):

$$ Z_{conv}(j\omega^*) + Z_{red}(j\omega^*) = 0 $$

Separando en parte real e imaginaria:

$$ \mathrm{Re}\{Z_{conv}(j\omega^*)\} + \mathrm{Re}\{Z_{red}(j\omega^*)\} = 0 $$
$$ \mathrm{Im}\{Z_{conv}(j\omega^*)\} + \mathrm{Im}\{Z_{red}(j\omega^*)\} = 0 $$

**Paso 3 — interpretación física.** La red es pasiva: \( \mathrm{Re}\{Z_{red}\} = R_g \geq 0 \). Para que se cumpla la primera ecuación, es necesario que:

$$ \mathrm{Re}\{Z_{conv}(j\omega^*)\} = -R_g \leq 0 $$

Es decir, el convertidor debe presentar **resistencia negativa** en \( \omega^* \) que cancele exactamente la resistencia de red. La segunda ecuación fija la frecuencia de oscilación: \( \omega^* \) es la resonancia donde las partes imaginarias se anulan entre sí.

**Paso 4 — criterio práctico.** En la práctica, la oscilación crece si la condición es más que cumplida:

$$ \boxed{\mathrm{Re}\{Z_{conv}(j\omega^*) + Z_{red}(j\omega^*)\} < 0} $$

La frecuencia crítica \( \omega^* \) se busca en el barrido de \( \omega \): es donde \( \mathrm{Im}\{Z_{total}\}\approx0 \) y simultáneamente \( \mathrm{Re}\{Z_{total}\}<0 \). En la banda subsíncrona, \( \omega^* = \omega_n = \omega_0\sqrt{X_{Cs}/X_L} \); en la banda armónica, coincide con la resonancia paralelo de cables/filtros.

## Cuándo y por qué se usa
Subsíncrona: parques eólicos conectados por líneas compensadas serie (causa de eventos reales, p.ej. ERCOT 2009), HVDC y redes débiles con alta penetración de convertidores. Armónica: parques eólicos/PV con cables largos (alta capacidad), HVDC y redes con muchos convertidores, donde aparecen oscilaciones de cientos de Hz a kHz no explicables por la dinámica electromecánica. Ambas son subclases "resonancia" de la [[clasificacion-estabilidad|clasificación de estabilidad]].

## Procedimiento de diseño (genérico)
1. Modela Z_o(j·omega) del convertidor incluyendo control, PLL y retardo digital, y Z_g de la red.
2. Localiza las resonancias de red (serie por compensación → fn subsíncrona; paralelo de cables → resonancia armónica) y las regiones no pasivas del convertidor.
3. Aplica el criterio de impedancia/pasividad; identifica la frecuencia crítica (Re{Z_conv + Z_red} < 0).
4. Mitiga: ajustar banda de PLL/lazo de corriente, amortiguamiento activo del LCL, filtro notch, compensar retardo o impedancia virtual; damping subsíncrono dedicado (SSDC) para SSCI; a nivel red, TCSC/bypass del condensador serie.
5. Re-verifica con barrido del SCR, del nivel de compensación y del número de convertidores.

## Ejemplo de código
```python
import numpy as np

def series_resonance(f1, XL, XCs):        # frecuencia subsincrona de red
    return f1*np.sqrt(XCs/XL)

def passivity_violation(Zo, freqs):       # bandas no pasivas (candidatas)
    return freqs[np.real(Zo) < 0]
# inestable si Re{Z_conv(f) + Z_red(f)} < 0 cerca de una resonancia de red
```

## Parámetros y valores típicos
- Subsíncrona: compensación serie 20–75 % → fn ≈ 10–45 Hz; la SSCI puede crecer en 0.1–1 s; modos torsionales 10–50 Hz.
- Armónica: rango típico de inestabilidad 100 Hz–3 kHz; objetivo Re{Z_o} ≥ 0 o margen de fase de impedancia > 30° en las resonancias de red esperadas.

## Errores comunes
- Suponer que sin masas rotativas no hay riesgo subsíncrono (la SSCI es de control).
- Modelar el convertidor solo a la fundamental (no captura la resistencia negativa subsíncrona ni la de alta frecuencia).
- Diseñar la PLL solo por respuesta nominal, sin ver su efecto en la impedancia.
- Analizar un solo convertidor e ignorar la interacción paralelo de varios.
- Despreciar el retardo digital (principal fuente de no pasividad a alta frecuencia).
- Confiar solo en amortiguamiento pasivo (pérdidas) cuando el problema es el control.

## 7 — SSO en HVDC y sistemas de alta penetración: 10–45 Hz

Las oscilaciones subsíncronas (SSO) en sistemas HVDC y redes con alta penetración de convertidores se producen en la banda 10–45 Hz, fuera del rango electromecánico clásico (0.1–2 Hz):

**Mecanismo en HVDC:** el controlador de corriente del HVDC tiene un ancho de banda de ~50 Hz. A frecuencias subsíncronas (\(f_{sub} = f_0 - f_{osc}\)), la parte real de la impedancia del convertidor HVDC puede ser negativa. Si la red presenta una resonancia (por compensación serie o capacidad de cables) en esa banda, la condición \(\text{Re}\{Z_{conv}+Z_{red}\} < 0\) se satisface → crecimiento de la oscilación.

**Detección:** FFT de la corriente o tensión en el punto de conexión HVDC. Un pico a \(f_{sub}\) que crece con el tiempo indica inestabilidad subsíncrona. El umbral de alarma es \(I_{sub} > 2\%\,I_{1}\).

**Mitigación:** limitación del ancho de banda del lazo de corriente HVDC (< 30 Hz en red débil), filtros SSDC (Sub-Synchronous Damping Controller) que añaden amortiguamiento activo en la banda 10–45 Hz.

## 8 — Interacción PLL-red débil: inestabilidad alrededor de \(f_{PLL}\)

El PLL de un convertidor GFL presenta una región de impedancia con parte real negativa alrededor de su frecuencia de cruce \(f_{PLL}\):

$$\text{Re}\{Z_{conv}(j\omega)\}\bigg|_{\omega \approx \omega_{PLL}} < 0$$

En red débil (SCR < 3), la impedancia de red \(Z_{red}\) es grande, y el criterio \(\text{Re}\{Z_{conv}+Z_{red}\} < 0\) puede cumplirse → inestabilidad de pequeña señal a \(f \approx f_{PLL}\).

**Solución:** reducir \(f_{PLL}\) hasta \(f_{PLL} < 0.5/\sqrt{\text{SCR}}\). Para SCR = 2: \(f_{PLL} < 17\,\text{Hz}\). Esto alarga la dinámica de seguimiento de ángulo pero mantiene la estabilidad.

**Alternativa GFM:** el GFM no tiene PLL explícito; su impedancia es pasiva (resistiva-inductiva) en toda la banda → compatible con red muy débil (SCR → 1).

## 9 — Modos de droop en microrredes y análisis modal

Una microrred con \(N\) inversores GFM interconectados tiene \(2N\) modos de pequeña señal para frecuencia y ángulo. Los modos de droop (frecuencia compartida) tienen la frecuencia natural:

$$\omega_{droop} \approx \frac{1}{2\pi}\sqrt{\frac{1}{m_p J_{eq}}}$$

donde \(m_p\) es el estatismo de potencia [rad/s/W] y \(J_{eq}\) es la inercia virtual equivalente. Para \(m_p = 2\times10^{-4}\,\text{rad/s/W}\) y \(J_{eq} = 5\,\text{kg}\cdot\text{m}^2\): \(f_{droop} \approx 1.6\,\text{Hz}\).

**Factores de participación:** el análisis modal calcula la contribución de cada estado al modo oscilatorio. Para el modo de droop, los ángulos de referencia \(\theta_i\) tienen el mayor factor de participación; las corrientes dq tienen participación despreciable.

**Requisito de amortiguamiento:** todos los modos deben tener \(\zeta > 0.05\) para evitar oscilaciones perceptibles. El diseño de droop debe incluir un filtro de potencia \(\omega_{LPF} > \omega_{droop}\) para evitar que los modos rápidos de corriente exciten los modos lentos de droop.

## 10 — Análisis modal del sistema linealizado: eigenvalores y estabilidad

El sistema linealizado de la microrred completa tiene la forma:

$$\dot{\mathbf{x}} = A\,\mathbf{x}, \qquad A \in \mathbb{R}^{n\times n}$$

Los eigenvalores \(\lambda_i = \sigma_i + j\omega_i\) de \(A\) determinan la estabilidad:
- \(\sigma_i < 0\) para todo \(i\): sistema estable
- \(\sigma_i > 0\) para algún \(i\): inestable; el modo crece con constante \(e^{\sigma_i t}\)
- \(\zeta_i = -\sigma_i/|\lambda_i|\): factor de amortiguamiento del modo \(i\)

**Requisito normativo y de diseño:** \(\zeta_i > 0.05\) para todos los modos en el rango 0.1–20 Hz (modos electromecánicos y de droop). Para los modos de corriente (> 100 Hz): \(\sigma_i < 0\) es suficiente.

**Barrido paramétrico:** calcular los eigenvalores vs SCR, vs \(K_{ad}\), vs \(\omega_{PLL}\) permite identificar los márgenes de diseño. En sistemas de más de 10 inversores, el cálculo es de orden \(O(n^3)\) pero factorizable por la estructura en bloques de la red.

## 11 — SSO en HVDC: mecanismo, detección y mitigación

Las oscilaciones subsíncronas en sistemas HVDC se producen en la banda **10–45 Hz**. El controlador de corriente del convertidor HVDC tiene un ancho de banda de ~50 Hz; a frecuencias subsíncronas la parte real de su impedancia puede ser negativa. Si la red presenta una resonancia (por compensación serie o capacidad de cables) en esa banda, la condición \(\text{Re}\{Z_{conv}+Z_{red}\}<0\) se satisface y la oscilación crece.

**Condición de inestabilidad:**
$$\text{Re}[Z_{conv}(j\omega)] < 0 \quad\text{en la frecuencia de resonancia del cable} \Rightarrow \text{energía neta positiva por ciclo}$$

**Detección:** ventana FFT de 200 ms sobre la señal de tensión/corriente en el punto de conexión; umbral de alarma cuando la componente en \(f_{sub}\) supera el 0.1% de la fundamental en amplitud.

**Mitigación:** (1) filtro SSD (Sub-Synchronous Damping) en el lazo de corriente, que añade amortiguamiento activo en la banda 10–45 Hz; (2) reducción del ancho de banda del PLL (\(f_{PLL} < 0.5/\sqrt{SCR}\)); (3) en red, bypass del condensador serie o TCSC.

## 12 — Interacción entre inversores GFL en red débil

Dos o más inversores GFL con PLL en red débil (SCR < 3) pueden inestabilizarse mutuamente a través de la impedancia de red compartida:

- **Frecuencia crítica:** alrededor de \(f_{PLL}\) (típicamente 5–30 Hz), donde la parte real de la impedancia de cada inversor es negativa.
- **Criterio de estabilidad multi-inversor:** la suma de admitancias de entrada de los \(N\) inversores debe satisfacer el criterio de Nyquist con la admitancia de red:
$$Y_{eq}(j\omega) = \sum_{i=1}^N Y_{inv,i}(j\omega);\quad \text{estable si } \text{Re}\{Y_{eq}+Y_{red}\} > 0$$
- **Solución:** reducir el BW del PLL de todos los inversores, o reemplazar alguno por GFM (cuya impedancia es pasiva — sin zona de resistencia negativa).

## 13 — Análisis modal del sistema completo linealizado

El sistema completo de \(N\) inversores más red se linealiza en el punto de operación: \(\dot{\mathbf{x}}=A\,\mathbf{x}\), con \(A\in\mathbb{R}^{n\times n}\).

**Eigenvalores:** \(\lambda_i = -\sigma_i \pm j\omega_{d,i}\); el amortiguamiento del modo \(i\) es:
$$\zeta_i = \frac{\sigma_i}{|\lambda_i|}$$

**Requisito de diseño:** todos los modos deben tener \(\zeta_i > 0.05\); para modos oscilatorios en la banda de droop (0.1–5 Hz) se exige \(\zeta_i > 0.1\) para evitar oscilaciones perceptibles en la potencia.

**Factores de participación:** \(p_{ki} = x_{ki}\,y_{ik}\) (producto del eigenvector derecho e izquierdo), indica qué estado \(k\) contribuye más al modo \(i\). Para el modo de droop: ángulos \(\theta_i\) tienen mayor participación; para el modo del PLL: estados del integrador del PLL. Los factores de participación guían qué parámetro ajustar (droop vs BW de PLL) para modificar el modo objetivo sin afectar a los demás.

**Barrido paramétrico:** calcular eigenvalores vs SCR, vs ganancia de droop, vs \(\omega_{PLL}\) para trazar el mapa de estabilidad y encontrar los márgenes de diseño.

<div class="cfig"><img src="figuras/fenomenos-oscilatorios-red-analisis.png" alt="SSO HVDC, impedancia negativa GFL, eigenvalores vs SCR y oscilación de droop"><div class="cap">(a) Espectro de tensión con componente SSO visible a 25 Hz. (b) Parte real de la impedancia GFL: zona negativa alrededor de f_PLL que puede inestabilizar la red. (c) Eigenvalores en el plano complejo vs SCR: a SCR bajo los modos se acercan al semiplano derecho. (d) Oscilación de potencia entre dos inversores GFM con droop: amortiguamiento insuficiente produce intercambio oscilatorio de P.</div></div>

## Conceptos relacionados
- [[impedancia-salida-estabilidad]] · [[clasificacion-estabilidad]] · [[interaccion-pll-red-debil]] · [[filtro-lcl]] · [[red-thevenin-scr]] · [[compensacion-retardo]] · [[filtro-notch]]

## Referencias
- Wang, Blaabjerg, Harmonic Stability in Power-Electronic-Based Power Systems, IEEE TPEL 2014.
- Wang et al., Unified Impedance Model of Grid-Connected VSCs, IEEE TPEL 2018.
- IEEE SSR WG, Terms, Definitions and Symbols for Subsynchronous Oscillations, 1985.
- Irwin et al., Sub-synchronous control interactions... series compensated transmission, IEEE PES 2011.
