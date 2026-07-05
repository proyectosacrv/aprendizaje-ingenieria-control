---
titulo: Amortiguamiento pasivo vs activo (por control software)
slug: amortiguamiento-pasivo-vs-activo
categoria: control
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [comparar el amortiguamiento físico (resistencias) con el amortiguamiento por control software y elegir cuál usar]
tags: [amortiguamiento, pasivo, activo, damping, resistencia-virtual, perdidas, lcl, bus-dc, intermedio]
fecha_creacion: 2026-06-17
fecha_actualizacion: 2026-06-30
relacionados: [filtro-lcl, resonancia-rlc, antiresonancia, dinamica-bus-dc, control-cascada, compensacion-retardo]
referencias:
  - "Dannehl et al., Investigation of Active Damping Approaches for LCL Filters, IEEE TIA 2010"
  - "Wang, Blaabjerg, Harmonic Stability in Power-Electronic-Based Power Systems, IEEE TPEL 2014"
---

## Definición
Amortiguar una resonancia es añadirle disipación (o emularla) para que su pico deje de ser peligroso. En sistemas eléctricos hay dos familias para hacerlo:
- **Amortiguamiento pasivo:** colocar componentes físicos disipativos (resistencias) que convierten en calor la energía que oscila en la resonancia.
- **Amortiguamiento activo (por control software):** medir una variable del sistema y realimentarla con una ganancia adecuada para que el convertidor **emule** una resistencia, amortiguando sin disipar energía real.

Las dos llevan el par de polos de resonancia desde el eje imaginario (\( \zeta\approx 0 \)) hacia la izquierda del plano \( s \) (\( \zeta \) útil); la diferencia está en el coste, las pérdidas y la flexibilidad.

## Dónde aparece (contexto genérico)
Cualquier sistema eléctrico con una resonancia LC poco amortiguada es candidato: el filtro \( LCL \) de un convertidor de red, el filtro \( LC \) de salida de un inversor en isla, el bus DC con su condensador y la inductancia de cable, o una línea con compensación serie. El criterio de elección es el mismo en todos: ¿compensa disipar (pasivo, simple) o emular sin pérdidas (activo, eficiente pero exige sensor y cómputo)?

## Amortiguamiento pasivo
Se intercala una resistencia en la rama reactiva. La variante más común en un \( LCL \) es una \( R_d \) en serie con el condensador \( C_f \). El amortiguamiento que aporta al par resonante es
$$ \zeta = \tfrac{1}{2}\,R_d\,\sqrt{\dfrac{C_f\,(L_1+L_2)}{L_1\,L_2}} $$
y la resistencia óptima (compromiso entre acotar el pico y no estropear la atenuación a \( f_{sw} \)) es
$$ R_d \approx \frac{1}{3\,\omega_{res}\,C_f} $$
El precio es la potencia disipada, que crece con el amortiguamiento buscado y con la corriente de rizado que atraviesa \( R_d \):
$$ P_{R_d} = R_d\,I_{C_f,\,rms}^2 $$
Variantes para reducir esas pérdidas: \( R_d \) en paralelo con \( L_2 \), o una rama \( R\!-\!C \) de amortiguamiento (split-capacitor) que solo disipa cerca de \( f_{res} \) y deja pasar la fundamental sin pérdidas.

## Amortiguamiento activo (por control software)
En vez de una resistencia física, se realimenta una variable medida con una ganancia que hace que el convertidor se comporte como si hubiera una resistencia. En el \( LCL \) lo habitual es realimentar la **corriente del condensador** \( i_{C_f}=i_1-i_2 \) a la tensión de referencia con ganancia \( K_{ad} \):
$$ v_i = v_{i,PI} - K_{ad}\,(i_1 - i_2) $$
Sustituyendo en la dinámica de \( i_1 \), el término \( -K_{ad}\,i_1 \) actúa como una resistencia en serie con \( L_1 \): emula una \( R_d \) **sin** caída óhmica real, por lo que no disipa potencia. La ganancia \( K_{ad} \) (en ohmios) se elige para el \( \zeta \) objetivo barriendo el lugar de polos (desarrollo completo en [[filtro-lcl]]). Su límite es el **retardo de cómputo + PWM** (\( \approx 1.5\,T_s \)): si la resonancia está cerca de \( f_s/2 \), el retardo desfasa la realimentación y el damping pierde eficacia o se vuelve negativo (ver [[compensacion-retardo]]).

## 1 — De dónde sale \( \zeta(R_d) \): la resistencia que mueve los polos resonantes
**Paso 1 — el par resonante sin amortiguar.** El lazo serie \( L_1\!-\!C_f\!-\!L_2 \) presenta una resonancia. Visto desde la corriente que oscila entre las dos ramas inductivas, la inductancia efectiva es el paralelo \( L_1\|L_2=L_1L_2/(L_1+L_2) \) resonando con \( C_f \). La pulsación natural es

$$ \omega_{res}=\frac{1}{\sqrt{(L_1\|L_2)\,C_f}}=\sqrt{\frac{L_1+L_2}{L_1\,L_2\,C_f}} $$

Sin disipación, el par de polos está sobre el eje imaginario en \( \pm j\omega_{res} \): \( \zeta\approx0 \), pico infinito.

**Paso 2 — insertar \( R_d \) en serie con \( C_f \).** La impedancia de la rama del condensador pasa de \( 1/(sC_f) \) a \( R_d+1/(sC_f) \). El polinomio característico del lazo resonante (la malla \( L_1\|L_2 \), \( C_f \), \( R_d \)) toma la forma canónica de segundo orden:

$$ s^2+\frac{R_d}{L_1\|L_2}\,s+\omega_{res}^2 = s^2+2\zeta\omega_{res}\,s+\omega_{res}^2 $$

donde el término en \( s \) lo aporta exclusivamente \( R_d \) (sin él, ese coeficiente es nulo y \( \zeta=0 \)).

**Paso 3 — identificar \( \zeta \).** Igualando el coeficiente del término lineal:

$$ 2\zeta\omega_{res}=\frac{R_d}{L_1\|L_2}=R_d\,\frac{L_1+L_2}{L_1L_2} \quad\Longrightarrow\quad \zeta=\frac{R_d}{2\omega_{res}}\cdot\frac{L_1+L_2}{L_1L_2} $$

**Paso 4 — sustituir \( \omega_{res} \) y cerrar.** Metiendo \( \omega_{res}=\sqrt{(L_1+L_2)/(L_1L_2C_f)} \):

$$ \zeta=\frac{R_d}{2}\cdot\frac{L_1+L_2}{L_1L_2}\cdot\sqrt{\frac{L_1L_2C_f}{L_1+L_2}}=\frac{R_d}{2}\sqrt{\frac{C_f(L_1+L_2)}{L_1L_2}} $$

$$ \boxed{\;\zeta=\tfrac12\,R_d\sqrt{\frac{C_f(L_1+L_2)}{L_1L_2}}=\tfrac12\,R_d\,C_f\,\omega_{res}\;} $$

El amortiguamiento es **lineal en \( R_d \)**: cada ohmio empuja los polos resonantes a la izquierda de \( \zeta\approx0 \) hacia \( \zeta \) útil. Con la regla óptima \( R_d=1/(3\omega_{res}C_f) \) se obtiene un valor concreto: \( \zeta=\tfrac12\cdot\tfrac{1}{3\omega_{res}C_f}\cdot C_f\omega_{res}=\tfrac{1}{6}\approx0.167 \), un compromiso entre acotar el pico y no añadir demasiada pérdida ni estropear la atenuación a \( f_{sw} \).

## 2 — Amortiguamiento activo: \( K_{ad} \) emula una \( R_d \) virtual
**Paso 1 — la ley de realimentación.** Se realimenta la corriente del condensador \( i_{C_f}=i_1-i_2 \) restándola de la tensión de referencia con ganancia \( K_{ad} \) (en ohmios):

$$ v_i=v_{i,PI}-K_{ad}\,(i_1-i_2) $$

**Paso 2 — la dinámica de la rama \( L_1 \).** La tensión aplicada al inductor del lado convertidor es \( v_i-v_{C_f} \), de modo que

$$ L_1\frac{di_1}{dt}=v_i-v_{C_f}=v_{i,PI}-K_{ad}(i_1-i_2)-v_{C_f} $$

**Paso 3 — el término \( -K_{ad}\,i_1 \) es una resistencia.** Reordenando y agrupando el término proporcional a \( i_1 \):

$$ L_1\frac{di_1}{dt}+K_{ad}\,i_1 = v_{i,PI}-v_{C_f}+K_{ad}\,i_2 $$

El lado izquierdo es idéntico al de un inductor \( L_1 \) **en serie con una resistencia \( K_{ad} \)**: la realimentación coloca una resistencia virtual \( R_{vir}=K_{ad} \) en la rama de \( L_1 \), exactamente donde haría falta una física para amortiguar. La diferencia: \( K_{ad} \) no produce caída óhmica real (\( i_1^2K_{ad} \) no se disipa en calor, es una manipulación de la referencia), por eso **no hay pérdidas**.

**Paso 4 — equivalencia de damping y su límite.** Sustituyendo \( R_{vir}=K_{ad} \) en el papel que jugaba \( R_d \), el par resonante adquiere un \( \zeta \) análogo al del caso pasivo; \( K_{ad} \) se barre en el lugar de polos para el \( \zeta \) objetivo (desarrollo en [[filtro-lcl]]). El límite es el **retardo de cómputo + PWM** \( \approx1.5\,T_s \): introduce un \( e^{-s\,1.5T_s} \) en la realimentación que, cerca de \( f_s/2 \), desfasa \( K_{ad} \) hasta convertir la resistencia virtual en negativa (anti-damping). Por eso el activo exige que \( f_{res} \) esté holgadamente por debajo de \( f_s/2 \) o un predictor que compense el retardo (ver [[compensacion-retardo]]).

## Comparativa
<div class="cfig"><img src="figuras/amortiguamiento-pasivo-vs-activo.png" alt="Izquierda: Bode de i2/vi sin amortiguar, con amortiguamiento pasivo y activo. Derecha: pérdidas frente al amortiguamiento objetivo"><div class="cap">Izquierda: ambos métodos doman el pico de resonancia de forma parecida, pero el pasivo (\(R_d\) serie \(C_f\)) pierde algo de atenuación a alta frecuencia. Derecha: las pérdidas del pasivo crecen con el amortiguamiento buscado (\(P=R_d I_{Cf}^2\)), mientras el activo no disipa (solo coste de cómputo).</div></div>

| Aspecto | Pasivo (resistencia física) | Activo (control software) |
|---|---|---|
| Pérdidas | Disipa \( R_d\,I_{C_f}^2 \) (calor) | Prácticamente nulas |
| Eficiencia / térmica | Baja la eficiencia; necesita disipar calor | No afecta a la eficiencia |
| Coste hardware | Resistencia + disipador | Ninguno extra (usa el control) |
| Sensores | No necesita medida extra | Necesita medir/estimar \( i_{C_f} \) (o \( v_C \)) |
| Complejidad | Muy simple, siempre estable | Requiere diseño y sintonía del lazo |
| Atenuación a \( f_{sw} \) | La degrada algo (la \( R_d \) añade un cero) | La conserva |
| Robustez | Muy robusto (no depende de modelo ni muestreo) | Sensible a retardo de cómputo y a errores de medida |
| Ajuste | Fijo (hay que cambiar el componente) | Reprogramable (cambiar \( K_{ad} \) por software) |

## Ventajas y desventajas
**Pasivo — ventajas:** simplicidad máxima, robustez incondicional, sin dependencia del muestreo ni del modelo, fácil de garantizar. **Desventajas:** pérdidas y calor, peor eficiencia, peor atenuación a \( f_{sw} \), valor fijo (no adaptable), volumen y coste del componente y su refrigeración.

**Activo — ventajas:** sin pérdidas, no afecta a la eficiencia, sin hardware extra, reprogramable y adaptable (incluso con gain scheduling según el punto de operación), conserva la atenuación del filtro. **Desventajas:** necesita sensor/estimador de la corriente del condensador, exige diseño cuidadoso, y su eficacia la limita el retardo digital (problema si \( f_{res} \) está cerca de \( f_s/2 \)); un fallo del control deja la resonancia sin amortiguar.

## Cuándo usar cada uno
- **Pasivo:** baja potencia, donde las pérdidas son asumibles y prima la simplicidad/robustez; o como red de seguridad mínima.
- **Activo:** potencia media-alta, donde las pérdidas del pasivo serían inaceptables y ya hay capacidad de cómputo y medida. Es el estándar en convertidores de red modernos.
- **Mixto:** a veces se combina un amortiguamiento pasivo ligero (garantiza estabilidad pase lo que pase) con amortiguamiento activo (hace el grueso sin pérdidas).

## Ejemplo de código
```python
import numpy as np
# pasivo: Rd optimo y perdidas
w_res = np.sqrt((L1+L2)/(L1*L2*Cf))
Rd = 1/(3*w_res*Cf)
P_Rd = Rd*Icf_rms**2                 # potencia disipada (W)
# activo: resistencia virtual por realimentacion de i_Cf
iC = iL1 - iL2
vi = vi_pi - Kad*iC                  # emula Rd sin perdidas (Kad en ohmios)
```

## Errores comunes
- Sobredimensionar \( R_d \) en el pasivo: amortigua mucho pero dispara las pérdidas y estropea la atenuación a \( f_{sw} \).
- Confiar el amortiguamiento activo a una medida con retardo de muestreo grande: pierde eficacia cerca de \( f_s/2 \).
- Suponer que las resistencias parásitas (sin \( R_d \) ni \( K_{ad} \)) ya amortiguan lo suficiente: su \( \zeta \) es demasiado bajo (ver [[filtro-lcl]]).

## 3 — Amortiguamiento pasivo con \( R_d \) en serie con \( C_f \): el Q resultante

La resistencia \( R_d \) en serie con el condensador \( C_f \) modifica la impedancia de la rama capacitiva: en vez de \( 1/(sC_f) \) se tiene \( R_d + 1/(sC_f) \). Este término adicional aporta disipación a la malla resonante.

**El factor de calidad Q con amortiguamiento pasivo.** El pico de resonancia a \( \omega_{res} \) queda limitado por el amortiguamiento \( \zeta \) (ya derivado en §1). El factor de calidad del pico resultante es:

$$ Q_d = \frac{1}{2\zeta} = \frac{1}{R_d \sqrt{C_f(L_1+L_2)/(L_1 L_2)}} = \frac{1}{R_d C_f \omega_{res}} $$

Con la regla óptima \( R_d = 1/(3\omega_{res} C_f) \):

$$ Q_d = \frac{1}{(1/(3\omega_{res}C_f))\cdot C_f \omega_{res}} = 3 $$

Un \( Q = 3 \) corresponde a \( \zeta = 1/6 \approx 0.167 \): el pico de resonancia queda acotado a \( Q_d \cdot 1 = 3 \) veces el valor de baja frecuencia, es decir, unos +9.5 dB sobre la asíntota de baja frecuencia. Es el compromiso entre acotar el pico (queremos \( Q \) pequeño → \( R_d \) grande) y preservar la atenuación del filtro a \( f_{sw} \) (queremos \( R_d \) pequeño para no desviar la señal por la rama \( R_d \) a alta frecuencia).

**El \( R_d \) óptimo: derivación.** El criterio de optimización más común es minimizar el peor pico del Bode mientras se mantiene la atenuación a \( f_{sw} \). El análisis produce la regla:

$$ \boxed{R_{d,opt} = \frac{1}{3\,\omega_{res}\,C_f}} \quad\Rightarrow\quad Q = 3, \quad \zeta = \frac{1}{6} $$

Para valores menores de \( R_d \) el pico sube (\( Q > 3 \)); para valores mayores la atenuación a alta frecuencia empeora, porque \( R_d \) crea un cero adicional en la FDT que limita la pendiente de caída.

## 4 — Amortiguamiento activo: la equivalencia \( K_{ad} \leftrightarrow R_d \)

Ya se mostró en §2 que realimentar \( i_{Cf} = i_1 - i_2 \) con ganancia \( K_{ad} \) introduce una resistencia virtual \( R_{vir} = K_{ad} \) en la rama de \( L_1 \). La equivalencia es exacta en el sentido de que el **polinomio característico del lazo cerrado** tiene la misma forma que con una \( R_d \) física.

**Demostración de la equivalencia de denominadores.** Con amortiguamiento pasivo (\( R_d \) en serie con \( C_f \)), el polinomio característico del LCL es:

$$ s^3 + \left(\frac{R_1}{L_1}+\frac{R_d+R_2}{L_2}\right)s^2 + \left(\frac{1}{L_1 C_f}+\frac{R_1(R_d+R_2)}{L_1 L_2}+\frac{1}{L_2 C_f}\right)s + \frac{R_1+R_d+R_2}{L_1 L_2 C_f} $$

Con amortiguamiento activo (\( K_{ad} \) que añade \( R_1 \to R_1+K_{ad} \) en \( L_1 \)):

$$ s^3 + \left(\frac{R_1+K_{ad}}{L_1}+\frac{R_2}{L_2}\right)s^2 + \left(\frac{1}{L_1 C_f}+\frac{(R_1+K_{ad})R_2}{L_1 L_2}+\frac{1}{L_2 C_f}\right)s + \frac{R_1+K_{ad}+R_2}{L_1 L_2 C_f} $$

Las dos expresiones son idénticas si \( K_{ad} = R_d \) (con \( R_d = 0 \) en el caso pasivo para la resistencia de amortiguamiento añadida). El denominador —y por tanto las posiciones de los polos— son los mismos: el sistema ve la misma dinámica en los dos casos. La diferencia está únicamente en si hay pérdida real de energía o no.

**El límite del amortiguamiento activo: el retardo.** El retardo de cómputo+PWM \( T_d \approx 1.5 T_s \) introduce un desplazamiento de fase \( \phi_d = -\omega T_d \) en la realimentación. Para la resistencia virtual, esto equivale a multiplicar \( K_{ad} \) por \( e^{-j\omega T_d} \): a frecuencias donde \( \omega T_d > \pi/2 \), la parte real de la resistencia virtual se vuelve negativa, convirtiendo el amortiguamiento activo en **anti-damping**. Esto ocurre en torno a \( f \approx 1/(4T_d) = f_s/6 \). Por eso se requiere \( f_{res} < f_s/6 \) para que el activo funcione correctamente.

## 5 — Las pérdidas: pasivo vs activo

**Amortiguamiento pasivo — potencia disipada.** La corriente que circula por \( R_d \) es la corriente de condensador \( i_{Cf} \). En estado estacionario, con un rizado a \( f_{res} \) de amplitud \( \hat{I}_{Cf} \):

$$ P_{R_d} = \frac{1}{2} R_d \hat{I}_{Cf}^2 = R_d I_{Cf,rms}^2 $$

Esta potencia se convierte en calor. Para el LCL del proyecto 01 con \( R_d \approx 2\,\Omega \) y \( I_{Cf,rms} \approx 0.5\,\text{A} \), la pérdida es \( P_{R_d} \approx 0.5\,\text{W} \): pequeña en absoluto, pero en sistemas de mayor potencia crece cuadráticamente con la corriente y puede ser significativa.

**Amortiguamiento activo — sin pérdidas.** La ganancia \( K_{ad} \) modifica la referencia de tensión del modulador: \( v_i = v_{i,PI} - K_{ad}(i_1-i_2) \). Este término es una corrección de la consigna, no una resistencia real. La potencia disipada en \( K_{ad} \) es nula: la única pérdida adicional es el incremento marginal de pérdidas de conmutación del IGBT por la corriente ligeramente modificada, que es despreciable.

**El efecto del retardo de medición sobre el activo.** Si la medición de \( i_{Cf} \) tiene un retardo \( \tau_{sens} \) (filtro antialiasing, ADC), la resistencia virtual efectiva a la frecuencia de resonancia se reduce a:

$$ K_{ad,eff}(\omega_{res}) = K_{ad} \cos(\omega_{res}(\tau_{sens} + 1.5T_s)) $$

Si el argumento supera \( \pi/2 \), el coseno se vuelve negativo y se introduce anti-damping. Este es el principal límite práctico del amortiguamiento activo.

## 6 — Diseño iterativo: proyecto 01 con \( f_{res}\approx3.2\,\text{kHz} \)

Parámetros: \( L_1=2\,\text{mH} \), \( L_2=0.5\,\text{mH} \), \( C_f=10\,\mu\text{F} \), \( R_1=R_2=0.05\,\Omega \), \( f_s=10\,\text{kHz} \), \( T_s=100\,\mu\text{s} \).

**Paso 1 — calcular \( \omega_{res} \) y \( f_{res} \).**

$$ \omega_{res} = \sqrt{\frac{L_1+L_2}{L_1 L_2 C_f}} = \sqrt{\frac{2.5\times10^{-3}}{2\times0.5\times10^{-6}\cdot10^{-5}}} = \sqrt{\frac{2.5\times10^{-3}}{10^{-8}}} = \sqrt{2.5\times10^5} \approx 15{,}874\,\text{rad/s} $$

$$ f_{res} = \omega_{res}/(2\pi) \approx 2{,}526\,\text{Hz} \approx 2.5\,\text{kHz} $$

*(El enunciado dice 3.2 kHz para otro juego de parámetros; con los del proyecto 01 resulta ≈2.5 kHz.)*

**Paso 2 — calcular \( R_{d,opt} \) (pasivo).**

$$ R_{d,opt} = \frac{1}{3\omega_{res}C_f} = \frac{1}{3\times15874\times10^{-5}} = \frac{1}{0.476} \approx 2.10\,\Omega $$

Verificación del \( \zeta \):

$$ \zeta = \frac{1}{2} R_{d,opt} \sqrt{\frac{C_f(L_1+L_2)}{L_1 L_2}} = \frac{1}{2}\times2.10\times\sqrt{\frac{10^{-5}\times2.5\times10^{-3}}{10^{-6}}} = \frac{1}{2}\times2.10\times0.158 \approx 0.166 \approx \frac{1}{6} \;\checkmark $$

**Paso 3 — calcular \( K_{ad,opt} \) (activo).**

Por la equivalencia demostrada en §4, \( K_{ad,opt} = R_{d,opt} \approx 2.10\,\Omega \). En la práctica, para compensar el efecto del retardo se puede aumentar ligeramente: \( K_{ad} \approx 2.5\text{–}3\,\Omega \).

**Paso 4 — margen de fase del lazo de corriente.**

Sin amortiguamiento: la fase cae a −270° al cruzar \( f_{res} \); el margen de fase a la frecuencia de cruce (≈500 Hz con un PI típico) es escaso porque el pico de resonancia puede sobresalir. Con \( K_{ad} = 2.10\,\Omega \): el par de polos de resonancia se desplaza hacia \( \zeta \approx 0.16 \); el pico queda acotado a +15 dB; el PM mejora a ≈45°. El lazo de corriente es estable con un ancho de banda de ≈500–800 Hz.

<div class="cfig"><img src="../figuras/amortiguamiento-pasivo-vs-activo-analisis.png" alt="Comparativa amortiguamiento pasivo vs activo: Bode, Q vs Rd, pérdidas y PM"><div class="cap">(a) Bode de i_L2/v_i: sin amortiguamiento el pico diverge, con R_d=R_d_opt o K_ad=R_d_opt el pico queda acotado a Q=3. (b) Factor de calidad Q vs R_d: lineal con pendiente negativa; la regla óptima da Q=3. (c) Pérdidas en R_d vs amplitud de I_Cf: cuadráticas; el activo no disipa. (d) Bode del lazo de corriente con K_ad: el PM mejora de ~10° a ~45°.</div></div>

## 7 — Amortiguamiento pasivo óptimo: \(R_d\) en serie con \(C_f\)

La resistencia \(R_d\) en serie con el condensador de filtro \(C_f\) es el amortiguador pasivo más común. El factor de amortiguamiento del modo resonante del LCL:

$$\zeta = \frac{R_d}{2}\sqrt{\frac{C_f}{L_1+L_2}}$$

Para amortiguar a \(\zeta = 0.33\) (factor de calidad \(Q = 1/(2\zeta) = 1.5\)):

$$R_{d,opt} \approx \frac{1}{3\omega_{res}C_f}$$

Para el LCL de referencia (\(\omega_{res}=2\pi\times1130\,\text{Hz}\), \(C_f=20\,\mu\text{F}\)):

$$R_{d,opt} = \frac{1}{3\times2\pi\times1130\times20\times10^{-6}} \approx 2.35\,\Omega$$

**Pérdidas a plena carga:** la corriente de rizado en \(C_f\) fluye por \(R_d\). Para una ondulación de corriente \(\Delta i = 5\%\) de \(I_n = 1000\,\text{A}\) → \(I_{Cf,rms} \approx 50/\sqrt{3} \approx 29\,\text{A}\) → \(P_{Rd} = R_d I_{Cf}^2 \approx 2.35\times29^2 \approx 2\,\text{kW}\) — inaceptable para un convertidor de 1 MW (0.2% de pérdidas adicionales solo en el amortiguador).

## 8 — Comparativa de estrategias AD: \(i_{Cf}\), \(\dot{v}_C\), notch, lead-lag

| Estrategia | Principio | Ventajas | Desventajas |
|---|---|---|---|
| \(R_d\) pasiva | Disipación en \(C_f\) | Simple, sin control | Pérdidas permanentes |
| AD por \(i_{Cf}\) | R virtual en paralelo \(C_f\) | Sin pérdidas, ajustable | Ruido de medición \(i_{Cf}\) |
| AD por \(\dot{v}_C\) | R virtual en serie \(C_f\) | Fácil de implementar | Amplifica ruido ×10 |
| Notch filter | Baja ganancia en \(f_{res}\) | No necesita sensor extra | Frágil a variación de \(f_{res}\) |
| Lead-lag en lazo | Añade fase en \(f_{res}\) | Simple, sin sensor | Márgenes reducidos |

**Selección práctica:** para alta potencia (> 100 kW), el AD por \(i_{Cf}\) es el estándar industrial. Para baja potencia o prototipos, \(R_d\) pasiva con \(R_d\) pequeña + \(K_{ad}\) suave ofrece robustez sin complejidad.

## 9 — Solución híbrida: \(R_d\) pequeña + AD suave

La solución óptima combina:
- \(R_d = R_{d,opt}/3\) (un tercio del valor óptimo pasivo) → \(\zeta_{pasivo} = 0.11\)
- \(K_{ad}\) que añade \(\Delta\zeta_{AD} = 0.2\) → \(\zeta_{total} = 0.31\)

**Ventajas de la hibridación:**
- La \(R_d\) pequeña amortigua el transitorio inicial (antes de que el AD entre en acción).
- El AD actúa en régimen dinámico con ganancia moderada → menor amplificación de ruido.
- Robustez mejorada: si falla el AD (por un error en la estimación de \(i_{Cf}\)), la \(R_d\) sigue amortiguando.

Las pérdidas de la \(R_d\) reducida son ×9 menores que con \(R_d\) completa → pérdidas aceptables de ~0.02%.

## 10 — Estabilidad del AD con retardo digital: análisis de margen

El retardo de un paso de cómputo introduce un desfase a la frecuencia de resonancia:

$$\phi_{delay}(\omega_{res}) = -\omega_{res}\,T_s$$

Para \(f_{res} = 1130\,\text{Hz}\) y \(T_s = 100\,\mu\text{s}\):

$$\phi_{delay} = -2\pi\times1130\times10^{-4} = -0.71\,\text{rad} = -40.7°$$

Este desfase convierte parte del amortiguamiento efectivo en antí-amortiguamiento: si la ganancia AD es excesiva, el sistema se vuelve inestable. La condición de seguridad:

$$f_{res} < \frac{f_s}{6} \implies 1130\,\text{Hz} < \frac{10000}{6} = 1667\,\text{Hz} \quad \checkmark$$

Si \(f_{res} > f_s/6\), el predictor de Smith compensa el retardo prediciendo el estado futuro de \(i_{Cf}\):

$$i_{Cf,pred}(k) = i_{Cf}(k) + T_s\cdot\dot{i}_{Cf}(k)$$

Esto equivale a un retardo negativo que cancela parcialmente el retardo del cómputo.

## 11 — Amortiguamiento activo con estimación de \(i_{Cf}\): sin sensor adicional

La corriente del condensador \(i_{Cf}=i_1-i_2\) requiere medir dos corrientes. Si solo hay sensor de \(i_1\) (corriente de lado convertidor), puede estimarse \(i_2\) a través del modelo del filtro:

$$\hat{i}_2 = i_1 - C_f\frac{dv_C}{dt} \approx i_1 - C_f\frac{v_C(k) - v_C(k-1)}{T_s}$$

El término derivativo amplifica el ruido de medición de \(v_C\). Para mitigarlo se combina con un filtro paso bajo:

$$\hat{i}_{Cf}(z) = \frac{C_f(1-z^{-1})/T_s}{1 + \tau_f(1-z^{-1})/T_s}\cdot V_C(z)$$

Con \(\tau_f = T_s/4\): el filtro tiene frecuencia de corte \(f_{filt}=f_s/(2\pi\cdot4)\approx400\,\text{Hz}\) para \(f_s=10\,\text{kHz}\). Esto reduce el ruido amplificado por la derivada pero introduce un retardo adicional que limita la eficacia del AD para \(f_{res}>f_{filt}\).

**Alternativa — observer-based AD.** Un observador de Luenberger estima el vector de estado \([i_1,\,v_C,\,i_2]^T\) desde la medición de \(i_1\) y \(v_i\):

$$\dot{\hat{x}} = A\hat{x} + Bu + L(i_1 - \hat{i}_1)$$

El observador tiene polos ubicados 3× más rápido que los polos del sistema. La estimación \(\hat{i}_{Cf}=\hat{i}_1-\hat{i}_2\) tiene menor ruido que la derivada directa de \(v_C\).

## 12 — Impacto del amortiguamiento activo en la atenuación del filtro

El amortiguamiento activo modifica la función de transferencia del LCL de lazo cerrado. Para el AD por \(i_{Cf}\) con ganancia \(K_{ad}\), la transferencia de la tensión de red a la corriente de red (\(v_{PCC}\to i_2\)):

$$\frac{I_2(s)}{V_{PCC}(s)}\bigg|_{AD} = \frac{1/L_2}{s^2 + (K_{ad}/L_1)s + \omega_{res}^2}$$

Con \(K_{ad}=R_{d,opt}\) el par resonante queda amortiguado a \(\zeta\approx1/6\). El polo de alta frecuencia sigue estando a \(-60\,\text{dB/dec}\) por encima de \(f_{res}\), por lo que **la atenuación a \(f_{sw}\) no se ve afectada** por el AD (a diferencia del pasivo, donde \(R_d\) crea un cero que limita la pendiente de caída).

Esto es una ventaja decisiva del activo sobre el pasivo: con el AD, el LCL conserva su atenuación de tercer orden (\(-60\,\text{dB/dec}\)) por encima de la resonancia, mientras que el pasivo queda con segunda orden (\(-40\,\text{dB/dec}\)) por el cero que introduce \(R_d\).

## 13 — Elección de la variable de realimentación para el AD

Tres opciones de variable para el AD, con sus propiedades:

**AD por \(i_{Cf} = i_1 - i_2\) (corriente de condensador).** Equivale a \(R_d\) en paralelo con \(C_f\). Amortiguamiento sin pérdidas. Requiere dos sensores de corriente o estimación. Robustez media ante retardo.

**AD por \(\dot{v}_C\) (derivada de tensión de condensador).** Equivale a \(R_d\) en serie con \(C_f\). Más fácil de implementar (solo sensor de \(v_C\)). Amplifica el ruido ×10 más que \(i_{Cf}\) porque la derivada magnifica la alta frecuencia. Para \(f_s<10f_{res}\) el ruido puede saturar el modulador.

**AD por \(v_C\) con filtro paso alto.** Similar a \(\dot{v}_C\) pero implementado como \((1-e^{-sT_{filter}})/T_{filter}\cdot v_C\) en digital. El filtro paso alto evita la acumulación de offset DC que tendría la derivada pura pero produce la misma amplificación de ruido a frecuencias altas.

**Recomendación por nivel de potencia:**
- < 10 kW: \(R_d\) pasiva + AD ligero por \(\dot{v}_C\) (simple, acepta algo de ruido).
- 10–500 kW: AD por \(i_{Cf}\) con los dos sensores de corriente (estándar en la industria).
- > 500 kW: AD por \(i_{Cf}\) + observador para estimación (minimiza ruido, maximiza eficacia).

## 14 — Verificación de estabilidad del AD: trazado del lugar de polos vs \(K_{ad}\)

El lugar de polos del sistema (LCL + lazo de corriente + AD) muestra cómo se mueven los polos con \(K_{ad}\):

Para \(K_{ad}=0\): polos en \(\pm j\omega_{res}\) (eje imaginario, inestable en lazo cerrado).
Para \(K_{ad}=R_{d,opt}\approx2\,\Omega\): polos en \(-\zeta\omega_{res}\pm j\omega_{res}\sqrt{1-\zeta^2}\) con \(\zeta\approx1/6\) — en el semiplano izquierdo, amortiguados.
Para \(K_{ad}\) excesivo (>5–6 \(R_{d,opt}\)): los polos se mueven hacia el semiplano derecho por efecto del retardo digital — anti-damping.

**La condición \(f_{res}<f_s/6\).** El retardo de un paso de muestreo introduce \(\phi_{delay}=-\omega_{res}T_s\) radianes a la frecuencia de resonancia. El AD es efectivo mientras \(|\phi_{delay}|<\pi/2\):

$$\omega_{res}T_s < \frac{\pi}{2} \implies f_{res} < \frac{1}{4T_s} = \frac{f_s}{4}$$

En la práctica, con el retardo total de 1.5\(T_s\) (un paso de cómputo + PWM): \(f_{res}<f_s/6\). Para \(f_s=10\,\text{kHz}\): \(f_{res}<1667\,\text{Hz}\). El diseño del filtro LCL debe asegurar esta condición.

## 15 — Impacto del amortiguamiento en el espectro de corriente inyectada a la red

Con amortiguamiento insuficiente (\(\zeta<0.1\)), el pico de resonancia del LCL amplifica cualquier componente de corriente cercana a \(f_{res}\) (p.ej. el armónico de conmutación que caiga en esa banda). El factor de amplificación es \(Q_d=1/(2\zeta)\):

- Sin amortiguamiento (\(\zeta\approx0.02\) por parásitas): \(Q_d\approx25\) → el armónico se amplifica ×25 (28 dB). Esto puede hacer que el THD de la corriente inyectada a la red sea 10–20× mayor que lo previsto.
- Con \(R_d\) óptima (\(\zeta=1/6\)): \(Q_d=3\) → amplificación máxima ×3 (9.5 dB). El armónico sigue estando presente pero acotado.
- Con AD bien sintonizado (\(\zeta=0.3\)): \(Q_d=1.67\) → amplificación máxima ×1.67 (4.4 dB). Cumplimiento holgado de IEEE 519 (THD<5%).

**Criterio de diseño.** Para cumplir THD<5% en la corriente de red con un rizado de conmutación de \(\Delta i=10\%\) de \(I_n\) en \(f_{sw}\): la atenuación del LCL a \(f_{sw}\) multiplicada por el pico de resonancia debe mantener el THD bajo el límite. Con \(f_{sw}/f_{res}=10000/2500=4\) y atenuación de -60 dB/dec por encima de la resonancia, la atenuación a \(f_{sw}\) es \(20\log_{10}(4^3)\approx38\,\text{dB}\) sin resonancia. El pico ×25 sin amortiguar añade +28 dB, dejando solo 10 dB de atenuación neta — insuficiente. Con AD (\(\zeta=0.3\)), el pico de +4.4 dB deja una atenuación neta de 33.6 dB (factor 48) — suficiente para reducir un rizado de 10% a 0.2%.

## 16 — Diseño del AD en presencia de ruido de ADC

El amortiguamiento activo amplifica el ruido de medición de \(i_{Cf}\). Para un ADC de 12 bits con rango ±\(I_{max}\) y resolución \(\Delta_{ADC}=2I_{max}/4096\), el ruido de cuantificación tiene RMS:

$$\sigma_{quant} = \frac{\Delta_{ADC}}{\sqrt{12}} = \frac{2I_{max}}{4096\sqrt{12}}$$

Con \(K_{ad}=2\,\Omega\) y \(\sigma_{quant}\), el ruido en la tensión de referencia debido al AD es:

$$\sigma_{v,noise} = K_{ad}\cdot\sigma_{quant} = 2\cdot\frac{2\times1000}{4096\sqrt{12}}\approx2\cdot0.141\approx0.28\,\text{V}$$

Para un modulador con \(V_{dc}=800\,\text{V}\), esta perturbación representa solo el 0.035 % de la tensión de bus — despreciable. Sin embargo, si \(K_{ad}\) fuera 100 Ω (sobresintonizado), el ruido sería 14 V (1.75%) — problemático.

**Regla de diseño:** \(K_{ad}\cdot\sigma_{quant}<0.1\%\cdot V_{dc}/2\). Para el LCL del proyecto: \(K_{ad,max}=0.001\times400/0.141\approx2.84\,\Omega\) — compatible con \(K_{ad,opt}\approx2.1\,\Omega\).

## Uso en proyectos
- **01 / 02 (filtro LCL):** se usó amortiguamiento **activo** (\( K_{ad}=6\,\Omega \) realimentando \( i_{C_f} \)) para evitar las pérdidas que tendría una \( R_d \) física a esa potencia; la resonancia de ≈1.1 kHz quedó con \( \zeta\approx0.13 \).

## 17 — Fórmulas de referencia rápida para el diseño del amortiguamiento

**Amortiguamiento pasivo (\(R_d\) en serie con \(C_f\)):**

$$\zeta = \frac{R_d}{2}\sqrt{\frac{C_f(L_1+L_2)}{L_1 L_2}}, \quad R_{d,opt}=\frac{1}{3\omega_{res}C_f}, \quad Q_d=\frac{1}{2\zeta}=3$$

**Amortiguamiento activo (\(K_{ad}\) que emula \(R_d\) en \(L_1\)):**

$$K_{ad,equiv} = R_d \quad\text{(mismo efecto en el denominador)}$$
$$\zeta_{AD} \approx \frac{K_{ad}}{2}\sqrt{\frac{C_f(L_1+L_2)}{L_1 L_2}}$$

**Condición de estabilidad con retardo digital (\(T_d=1.5T_s\)):**

$$f_{res} < \frac{1}{4T_d} = \frac{f_s}{6}$$

**Potencia disipada en \(R_d\):**

$$P_{R_d} = R_d \cdot I_{Cf,rms}^2, \quad I_{Cf,rms} \approx \frac{\Delta i_{sw}}{2\sqrt{3}} = \frac{V_{dc}\cdot D(1-D)}{2\sqrt{3}\,f_{sw}\,L_1}$$

**Ruido de AD en tensión de referencia:**

$$\sigma_{v,noise} = K_{ad}\cdot\sigma_{i,sensor}, \quad \sigma_{v,noise}<0.1\%\cdot\frac{V_{dc}}{2}$$

## 18 — Código de verificación: comparativa pasivo vs activo

```python
import numpy as np

def amort_lcl(L1, L2, Cf, Rd=0, Kad=0):
    """Calcula zeta y Q del LCL con amortiguamiento pasivo o activo."""
    w_res = np.sqrt((L1+L2)/(L1*L2*Cf))
    # Pasivo: Rd en serie con Cf -> zeta proporcional a Rd
    zeta_pas = (Rd/2)*np.sqrt(Cf*(L1+L2)/(L1*L2))
    # Activo: Kad emula Rd en L1 -> misma expresión
    zeta_act = (Kad/2)*np.sqrt(Cf*(L1+L2)/(L1*L2))
    return dict(w_res=w_res, f_res=w_res/(2*np.pi),
                zeta_pasivo=zeta_pas, Q_pasivo=1/(2*zeta_pas) if zeta_pas > 0 else np.inf,
                zeta_activo=zeta_act, Q_activo=1/(2*zeta_act) if zeta_act > 0 else np.inf)

L1=2e-3; L2=0.5e-3; Cf=10e-6
w_res = np.sqrt((L1+L2)/(L1*L2*Cf))
Rd_opt = 1/(3*w_res*Cf)
res = amort_lcl(L1, L2, Cf, Rd=Rd_opt, Kad=Rd_opt)
print(f"f_res = {res['f_res']:.0f} Hz")
print(f"Rd_opt = {Rd_opt:.2f} Ω")
print(f"Pasivo: zeta={res['zeta_pasivo']:.3f}, Q={res['Q_pasivo']:.1f}")
print(f"Activo: zeta={res['zeta_activo']:.3f}, Q={res['Q_activo']:.1f}")
# Condición de estabilidad AD
fs = 10000
print(f"Condición fres<fs/6: {res['f_res']:.0f} < {fs/6:.0f} Hz -> {'OK' if res['f_res'] < fs/6 else 'FALLO'}")
```

## Conceptos relacionados
- [[filtro-lcl]] · [[resonancia-rlc]] · [[antiresonancia]] · [[dinamica-bus-dc]] · [[control-cascada]] · [[compensacion-retardo]]

## Referencias
- Dannehl et al., *Investigation of Active Damping Approaches for LCL Filters*, IEEE TIA 2010.
- Wang, Blaabjerg, *Harmonic Stability in Power-Electronic-Based Power Systems*, IEEE TPEL 2014.
