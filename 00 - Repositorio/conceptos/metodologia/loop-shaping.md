---
titulo: Loop-shaping (diseño en frecuencia)
slug: loop-shaping
categoria: metodologia
tipo: metodo
nivel: avanzado
proyectos: [01-GFM-Impedance]
objetivos: [disenar el controlador dando forma a la ganancia de lazo]
tags: [bode, ganancia-de-lazo, frecuencia, margen, diseno, rolloff, loop-shaping-robusto]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-02
relacionados: [metodos-sintesis-control, margenes-estabilidad, funciones-sensibilidad, sintonia-pi-pid, control-robusto-hinf]
referencias:
  - "Skogestad, Postlethwaite, Multivariable Feedback Control, Wiley 2005 (cap. 2-3)"
  - "McFarlane, Glover, A Loop-Shaping Design Procedure Using H-infinity Synthesis, IEEE TAC 1992"
---

## Definición
Método de diseño que da forma a la **ganancia de lazo abierto** \( L(s)=C(s)G(s) \) en el dominio
de la frecuencia para cumplir las especificaciones, en vez de razonar sobre los polos cerrados.
El diseñador traza primero la curva objetivo \( |L_{obj}(j\omega)| \) que satisface todos los
requisitos (seguimiento, rechazo, robustez, atenuación de ruido) y después calcula el controlador
que la logra.

## Fundamento teórico
Objetivos de forma de \( L(j\omega) \):
- **Baja frecuencia**: ganancia alta → buen seguimiento y rechazo (S pequeña).
- **Cruce \( \omega_c \)**: fija el ancho de banda; pendiente ≈ −20 dB/dec en el cruce para buen
  margen de fase.
- **Alta frecuencia**: ganancia baja → atenúa ruido y dinámica no modelada (T pequeña).
Compromiso fundamental (Bode): no se puede tener S y T pequeñas a la vez en la misma banda
(\( S+T=1 \)); ver [[funciones-sensibilidad]]. El margen de fase y \( M_s \) se leen directo de \( L \).

<div class="cfig"><img src="figuras/loop-shaping-ganancia.png" alt="forma deseada de la ganancia de lazo en frecuencia"><div class="cap">Forma objetivo de la ganancia de lazo $|L|$: alta a baja frecuencia (buen seguimiento y rechazo, $S$ pequeña), baja a alta frecuencia (atenúa ruido y dinámica no modelada, $T$ pequeña) y con pendiente $-20$ dB/dec en el cruce $f_c$ para un buen margen de fase. El diseño consiste en moldear esta curva con el controlador.</div></div>

## 1 — La forma deseada de \( L \) y de dónde sale la regla de la pendiente
**Paso 1 — qué pide cada banda.** El desempeño y la robustez se traducen en cotas sobre \( |L| \):
- **Baja frecuencia** (\( \omega\ll\omega_c \)): rechazo y seguimiento exigen \( |S|=\frac1{|1+L|}\le\varepsilon \), o sea \( |L|\ge 1/\varepsilon\gg1 \). Ganancia alta. Un integrador \( 1/s \) la hace \( \to\infty \) en DC (error de posición nulo).
- **Alta frecuencia** (\( \omega\gg\omega_c \)): atenuar ruido y dinámica no modelada exige \( |T|\approx|L|\le\delta\ll1 \). Ganancia baja, con caída rápida.
- **Cruce** \( \omega_c \): \( |L(j\omega_c)|=1 \); ahí se fija el ancho de banda.

**Paso 2 — por qué \( -20 \) dB/dec en el cruce.** Para un \( L \) de fase mínima, la fase está atada a la pendiente de la magnitud (relación de Bode magnitud-fase): una pendiente local de \( -n\cdot20 \) dB/dec corresponde aproximadamente a una fase de \( -n\cdot90^\circ \). En el cruce:
$$ \text{pendiente }-20\text{ dB/dec}\Rightarrow\angle L\approx-90^\circ\Rightarrow \mathrm{PM}\approx90^\circ $$
$$ \text{pendiente }-40\text{ dB/dec}\Rightarrow\angle L\approx-180^\circ\Rightarrow \mathrm{PM}\approx0^\circ\ (\text{al borde}) $$
Por eso se busca cruzar 0 dB con pendiente \( -20 \) dB/dec: es la única que garantiza margen de fase holgado. La forma ideal es entonces "\( \approx-20 \) dB/dec sostenida alrededor del cruce, cayendo más rápido lejos".

## 2 — Los requisitos sobre el Bode de la ganancia de lazo \( L(j\omega) \)
**La función de sensibilidad traduce los requisitos a cotas sobre \( |L| \).** No hay que especificar el controlador: basta con especificar \( |L| \), y la sensibilidad queda determinada.

**A bajas frecuencias: ganancia alta para error pequeño.**
La sensibilidad en baja frecuencia vale \( |S(j\omega)|\approx1/|L(j\omega)| \) cuando \( |L|\gg1 \).
Si se exige que el error a una perturbación de paso sea menor que un 2%, entonces:
$$ |S|\le0.02 \;\Rightarrow\; |L|\ge50\ (34\,\mathrm{dB}) $$
Un integrador en el lazo, \( L(s)\supset 1/s \), garantiza \( |L|\to\infty \) en DC y error de posición nulo para cualquier referencia escalón. Para rampa: se necesitan dos integradores.

**En el cruce: pendiente \( -20 \) dB/dec para PM ≥ 45°.**
El margen de fase es la distancia entre la fase de \( L(j\omega_c) \) y \( -180^\circ \). Una pendiente local de \( -20 \) dB/dec da una fase de aproximadamente \( -90^\circ \) (contribución del integrador) más la fase que añaden los demás polos y ceros. Para que la suma deje \( \mathrm{PM}\ge45^\circ \), no puede haber más polos que ceros cerca del cruce (sin otro cero que compense, cada polo adicional resta \( 90^\circ \)).

**A altas frecuencias: ganancia baja para rechazar ruido.**
El ruido de medida entra a través de \( T=L/(1+L) \). Para \( \omega\gg\omega_c \), \( |T|\approx|L| \), así que atenuar el ruido 40 dB requiere \( |L|<0.01 \) en esa banda. Se logra con polos de rolloff: añadir un polo doble en \( 10\omega_c \) hace que \( L \) caiga a \( -60 \) dB/dec por encima.

**La integral de Bode: conservación de la sensibilidad.**
Para sistemas de fase mínima, la integral de Bode establece:
$$ \int_0^\infty \log|S(j\omega)|\,d\omega = 0 $$
La consecuencia es que bajar \( |S| \) en una banda (buen rechazo) obliga a que suba en otra (el pico \( M_s \)). No se puede tener alta atenuación de perturbaciones en toda la banda: el área de atenuación \( (\log|S|<0) \) debe compensarse con área de amplificación \( (\log|S|>0) \). El compromiso entre ancho de banda y pico de sensibilidad es matemáticamente inevitable.

**La curva objetivo de \( |L(j\omega)| \)** es entonces la especificación que el diseñador traza antes de calcular el controlador: integrador para DC, pendiente \( -20 \) dB/dec en el cruce, rolloff a alta frecuencia. Todo el proceso de diseño consiste en conseguir esa forma con un controlador realizable.

## 3 — La forma ideal de \( L(j\omega) \): el diseño por objetivos

La curva objetivo de \( |L| \) se construye a partir de cuatro objetivos independientes que se traducen directamente en la forma del Bode:

**Objetivo 1 — error DC nulo: integrador en el lazo.**
\( L(s)\supset 1/s \) garantiza \( L(0)=\infty \), lo que hace que \( S(0)=0 \): error en régimen permanente nulo ante cualquier referencia o perturbación de tipo escalón. En el Bode, el integrador da una pendiente inicial de \( -20 \) dB/dec que sube indefinidamente hacia DC.

**Objetivo 2 — ancho de banda = \( \omega_c \): cruce en 0 dB.**
La frecuencia de cruce de ganancia \( \omega_c \) define el ancho de banda del lazo cerrado: \( |T(j\omega_c)|\approx -3 \) dB. La curva objetivo de \( |L| \) debe cruzar el eje 0 dB exactamente en \( \omega_c \). Esto se logra ajustando la ganancia del controlador.

**Objetivo 3 — PM ≥ 45°: pendiente \( -20 \) dB/dec en el cruce.**
Como se demostró en el apartado 1, cruzar 0 dB con pendiente \( -20 \) dB/dec da \( \mathrm{PM}\approx90^\circ \) (sistema sin retardo). Con retardo digital \( \tau_d=1.5T_s \), la fase se reduce:
$$ \mathrm{PM_{efectivo}}=90^\circ - \omega_c\,\tau_d\cdot\frac{180^\circ}{\pi} $$
Eligiendo \( \omega_c \) tal que \( \omega_c\,\tau_d\le 45^\circ\,(\pi/180^\circ) \) se garantiza PM ≥ 45° incluso con el retardo digital.

**Objetivo 4 — rechazo de ruido: rolloff para \( \omega>10\omega_c \).**
Por encima del cruce, \( L \) debe caer rápidamente para atenuar el ruido de medida. Un polo doble en \( \omega_{ro}=10\omega_c \) añade \( -40 \) dB/dec adicionales, dejando la caída total a \( -60 \) dB/dec. Cuanto más lejos esté \( \omega_{ro} \), menor el efecto sobre el PM (la fase del polo doble en el cruce es \( 2\arctan(\omega_c/\omega_{ro}) \approx 2\arctan(0.1)\approx11^\circ \), tolerable).

**La curva objetivo resultante** tiene la forma:
$$ L_{obj}(j\omega)=\frac{\omega_c}{j\omega}\cdot\frac{1}{\left(1+\dfrac{j\omega}{\omega_{ro}}\right)^2} $$
con \( \omega_c \) ajustado por la ganancia y \( \omega_{ro}=10\omega_c \) para el rolloff. El primer factor es el integrador (pendiente \( -20 \) dB/dec sostenida); el segundo añade el rolloff sin tocar el cruce.

## 4 — De la curva objetivo al controlador: la división \( L_{obj}/G \)

Una vez trazada la curva objetivo \( L_{obj}(s) \), el controlador se obtiene directamente como:
$$ C(s) = \frac{L_{obj}(s)}{G(s)} $$
siempre que la división sea propia (grado del numerador ≤ grado del denominador, condición de realizabilidad).

**Cancelación de los polos de \( G \) en el SPD.**
Si \( G(s) \) tiene polos en el semiplano derecho estable (polos en el SPD, con parte real negativa), el controlador puede cancelarlos exactamente: los polos de \( G \) se convierten en ceros de \( C \), y se simplifican. En la práctica, para una planta de primer orden \( G(s)=1/(Ls+R) \), el polo en \( -R/L \) se cancela con el cero del PI, dejando un integrador puro.

**Lo que no se puede cancelar: los ceros en el semiplano derecho (RHP).**
Si \( G(s) \) tiene ceros con parte real positiva (sistema de fase no mínima), cancelarlos con el controlador requeriría polos en el SPD, lo que inestabiliza el sistema. Por ello, los ceros RHP de \( G \) **limitan** la forma que puede tener \( L_{obj} \):
- La restricción de Bode-Zames establece que si \( G \) tiene un cero RHP en \( z \), entonces
  \( |L(z)|<1 \) necesariamente.
- En términos de ancho de banda: \( \omega_c<|z|/2 \) (aproximadamente) para no excitar el cero RHP.

**Realizabilidad: \( L_{obj}/G \) debe ser propia.**
Si \( G \) tiene grado relativo \( r \) (diferencia entre grado del denominador y del numerador), entonces \( L_{obj} \) debe tener grado relativo \( \ge r \) para que \( C \) sea propia. En la práctica se añaden los polos de rolloff de \( L_{obj} \) precisamente para aumentar el grado relativo y hacer \( C \) realizable.

**Ejemplo concreto — lazo de corriente con \( G(s)=1/(Ls+R) \):**
$$ L_{obj}(s)=\frac{\omega_c}{s}\cdot\frac{1}{\left(1+s/\omega_{ro}\right)^2} $$
$$ C(s)=\frac{L_{obj}}{G}=\frac{\omega_c}{s}\cdot\frac{1}{(1+s/\omega_{ro})^2}\cdot(Ls+R)=\omega_c\,\frac{Ls+R}{s}\cdot\frac{1}{(1+s/\omega_{ro})^2} $$
El primer factor \( \omega_c(Ls+R)/s \) es el PI por cancelación de polo con ganancia \( \omega_c \); el segundo factor es el polo doble de rolloff. El resultado es un PI con dos polos de rolloff: exactamente la estructura de controlador que sale del loop-shaping.

## 5 — Loop-shaping robusto: el método H∞ de McFarlane-Glover

El loop-shaping clásico da forma a \( L \) con criterio del diseñador, pero no optimiza formalmente la robustez. El método H∞ de McFarlane-Glover (1992) formaliza el proceso en dos pasos:

**Paso 1 — dar forma con un compensador previo \( W \).**
El diseñador especifica la forma deseada de \( L \) mediante un compensador previo (o "preacondicionador") \( W \), que puede ser un PI, un adelanto-retraso, o cualquier transferencia que dé la forma objetivo a \( G_s=WG \).

**Paso 2 — estabilizar robustamente con un regulador \( K \).**
Una vez dada la forma, se calcula el regulador \( K \) que maximiza el margen de estabilidad robusta del sistema en lazo cerrado. La robustez se mide mediante la factorización coprimera normalizada:
$$ G_s=N M^{-1},\quad N,M\text{ coprimas normalizadas} $$
El margen de estabilidad robusta es la distancia mínima entre la planta perturbada y la nominal, medida en la norma \( H_\infty \):
$$ \varepsilon_{max}=\frac{1}{\left\|\begin{bmatrix}K\\I\end{bmatrix}(I-G_sK)^{-1}\begin{bmatrix}N & M\end{bmatrix}\right\|_\infty} $$

**Interpretación del margen \( \varepsilon_{max} \).**
Valores típicos: \( \varepsilon_{max}>0.3 \) indica robustez buena; \( \varepsilon_{max}<0.1 \) indica sistema frágil. El valor \( \varepsilon_{max}=1 \) sería el óptimo inalcanzable. Para sistemas bien condicionados, el método maximiza \( \varepsilon \) calculando \( K \) mediante la solución de dos ecuaciones de Riccati.

**En la práctica del diseño de convertidores.**
El método H∞ de McFarlane-Glover raramente se aplica directamente: el loop-shaping clásico con verificación de \( M_s<2 \) es suficiente para la mayoría de las aplicaciones. El valor añadido del método robusto es su conexión formal con la incertidumbre de modelo: si la planta tiene variaciones paramétricas \( \Delta G \), la condición \( \varepsilon_{max}>\|\Delta G\|/(1+\|\Delta G\|) \) garantiza estabilidad ante todas las perturbaciones admisibles.

**Criterio práctico:** en diseño de lazos de corriente para convertidores, se usa loop-shaping clásico con PM ≥ 45° y \( M_s<2 \) como objetivos, y se verifica robustez mediante las cuatro sensibilidades. Solo en sistemas con fuerte variación paramétrica (inductancia variable, SCR incierto) se recurre al diseño H∞ formal.

## 6 — Diseño iterativo: loop-shaping para el lazo de corriente

**Datos del diseño:** inductor de filtro LCL lado fuente, \( L_1=2 \) mH, \( R_1=50 \) mΩ, periodo de muestreo \( T_s=100\,\mu\mathrm{s} \). Retardo equivalente: \( \tau_d=1.5\,T_s=150\,\mu\mathrm{s} \).

**Paso 1 — trazar la curva objetivo \( L_{obj}(j\omega) \).**
Especificaciones: ancho de banda \( f_c=750 \) Hz (\( \omega_c=2\pi\cdot750 \) rad/s), PM ≥ 45°, rechazo de perturbaciones \( >40 \) dB para \( f<50 \) Hz:
- Integrador \( 1/s \) en el lazo (error DC nulo, pendiente \( -20 \) dB/dec desde DC hasta \( \omega_c \)).
- La ganancia de \( L_{obj} \) en 50 Hz debe ser \( \ge100 \) (40 dB): con un integrador puro de ganancia \( \omega_c \), se tiene \( |L_{obj}(j2\pi\cdot50)|=\omega_c/(2\pi\cdot50)=750/50=15 \) (24 dB). Insuficiente → se añade ganancia adicional en la banda baja.
- Rolloff doble a partir de \( f_{ro}=7500 \) Hz (\( 10\,f_c \)).

**Paso 2 — calcular el controlador \( C(s) = L_{obj}(s)/G(s) \).**
Con \( G(s)=1/(L_1 s + R_1) \):
$$ L_{obj}(s)=\frac{\omega_c}{s}\cdot\frac{1}{(1+s/\omega_{ro})^2} $$
$$ C(s)=\omega_c\,\frac{L_1 s+R_1}{s}\cdot\frac{1}{(1+s/\omega_{ro})^2} $$
El factor PI: \( K_p=\omega_c L_1=2\pi\cdot750\cdot2\times10^{-3}\approx9.42 \), \( K_i=\omega_c R_1=2\pi\cdot750\cdot0.05\approx0.236 \). El rolloff añade dos polos en \( f_{ro}=7500 \) Hz para atenuar ruido.

**Paso 3 — verificar el margen de fase con el retardo digital.**
Con retardo \( \tau_d=1.5\,T_s \), la fase en el cruce:
$$ \angle L(j\omega_c)=-90^\circ - \omega_c\,\tau_d\cdot\frac{180^\circ}{\pi} - 2\arctan\!\left(\frac{\omega_c}{\omega_{ro}}\right) $$
$$ =-90^\circ - 2\pi\cdot750\cdot1.5\times10^{-4}\cdot\frac{180^\circ}{\pi} - 2\arctan(0.1) $$
$$ =-90^\circ - 40.1^\circ - 11.4^\circ = -141.5^\circ $$
$$ \mathrm{PM}=180^\circ-141.5^\circ=38.5^\circ $$
Insuficiente. Se reduce \( f_c \) a 600 Hz:
$$ \mathrm{PM}=180^\circ -90^\circ - 2\pi\cdot600\cdot1.5\times10^{-4}\cdot\frac{180^\circ}{\pi} - 2\arctan(0.08)\approx180-90-32.2-9.1=48.7^\circ\ \checkmark $$

**Paso 4 — verificar \( M_s<2 \).**
Con PM = 48.7°, la estimación aproximada \( M_s\approx1/\sin(\mathrm{PM})\approx1/\sin(48.7^\circ)\approx1.33<2 \). \( \checkmark \)

**Resultado del diseño:**

| Parámetro | Valor |
|---|---|
| \( K_p=\omega_c L_1 \) | \( 2\pi\cdot600\cdot2\times10^{-3}\approx7.54 \) |
| \( K_i=\omega_c R_1 \) | \( 2\pi\cdot600\cdot0.05\approx0.188 \) |
| \( f_{ro} \) (rolloff) | 6000 Hz |
| PM resultante | ≈ 49° |
| \( M_s \) | ≈ 1.33 |

<div class="cfig"><img src="figuras/loop-shaping-analisis.png" alt="Análisis completo de loop-shaping: curva objetivo, controlador, sensibilidades y robustez"><div class="cap">(a) La curva objetivo $|L_{obj}|$: integrador puro con rolloff doble en $10f_c$. Los tres requisitos (error DC, PM, ruido) se leen directamente del Bode. (b) Las tres curvas $G$ (planta), $C$ (controlador) y $L=CG$ (lazo): la planta cae a $-20$ dB/dec, el controlador sube en baja frecuencia (integrador) y cae en alta (rolloff), y el lazo tiene la forma objetivo. (c) Las cuatro sensibilidades $|S|$, $|T|$, $|PS|$, $|CS|$ del diseño resultante. (d) Verificación de robustez: $|S(j\omega)|$ con el pico $M_s$ marcado, comparación con el límite $M_s<2$.</div></div>

## Cuándo y por qué se usa
Cuando se quiere control explícito del compromiso desempeño/robustez/ruido, o la planta tiene
resonancias/retardos que conviene modelar en frecuencia. Es el lenguaje natural del análisis de
impedancia.

## Procedimiento (genérico)
1. Traza \( G(j\omega) \) (Bode de la planta).
2. Traza \( L_{obj}(j\omega) \): integrador, pendiente \( -20 \) dB/dec en el cruce, rolloff.
3. Calcula \( C(s)=L_{obj}(s)/G(s) \) (cancelación de los polos estables de \( G \)).
4. Verifica PM con el retardo digital; ajusta \( \omega_c \) si necesario.
5. Verifica \( M_s<2 \) y las cuatro sensibilidades.

## Ejemplo de código
```python
import numpy as np
from scipy import signal

L1, R1, Ts = 2e-3, 50e-3, 100e-6
wc = 2*np.pi*600        # 600 Hz, ajustado por PM
wro = 10*wc             # rolloff una decada por encima

# Controlador: PI * rolloff doble
Kp = wc*L1; Ki = wc*R1
C_num = [Kp, Ki]        # Kp*s + Ki
C_den = [1, 0]          # integrador

# Rolloff doble: 1/(1+s/wro)^2
roll_num = [wro**2]
roll_den = [1, 2*wro, wro**2]

# Lazo L = C*G con G=1/(L1*s+R1)
G_num = [1]; G_den = [L1, R1]

# Verificar PM
f = np.logspace(1, 4, 2000); w = 2*np.pi*f
L = (Kp*1j*w + Ki)/(1j*w) / (L1*1j*w + R1) / (1 + 1j*w/wro)**2
wc_idx = np.argmin(np.abs(np.abs(L)-1))
PM = 180 + np.degrees(np.angle(L[wc_idx]))
print(f"PM = {PM:.1f}°, fc = {f[wc_idx]:.0f} Hz")
```

## Parámetros y valores típicos
Margen de fase 45–60°, pendiente −20 dB/dec en el cruce, \( M_s<2 \), rolloff a \( 10\omega_c \).

## Errores comunes
- Cruce con pendiente −40 dB/dec → margen de fase pobre.
- No incluir el retardo digital en el cálculo del PM → sobreestimación del margen real.
- Forzar S pequeña en banda donde T debe serlo (viola el compromiso de Bode).
- Cancelar ceros RHP de G con el controlador → inestabilidad.

## Uso en proyectos
- **01 (GFM)**: el diagnóstico del lazo de potencia se hizo en frecuencia (margen de fase −86°
  reveló la causa de la inestabilidad), lenguaje de loop-shaping.

## Conceptos relacionados
- [[metodos-sintesis-control]] · [[margenes-estabilidad]] · [[funciones-sensibilidad]] · [[sintonia-pi-pid]]

## Referencias
- Skogestad, Postlethwaite, *Multivariable Feedback Control*, 2005.
- McFarlane, Glover, *A Loop-Shaping Design Procedure Using H∞ Synthesis*, IEEE TAC 1992.
