---
titulo: Desacoplo dq y feedforward de red
slug: desacoplo-dq
categoria: control
tipo: tecnica
nivel: intermedio
proyectos: []
objetivos: [convertir el lazo de corriente dq acoplado en dos lazos SISO independientes]
tags: [desacoplo, feedforward, acoplamiento-cruzado, dq, lazo-corriente, intermedio, control, MIMO, robustez, diseno]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-01
relacionados: [marco-dq, control-cascada, control-vectorial, controlador-pid, filtro-lcl]
referencias:
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
  - "Kazmierkowski, Krishnan, Blaabjerg, Control in Power Electronics, Academic Press 2002"
---

## Definición
Técnica que **cancela el acoplamiento cruzado** \( \pm\omega L \) entre los ejes d y q del lazo de
corriente de un convertidor, y compensa por **prealimentación (feedforward)** la tensión de red,
dejando dos plantas SISO de primer orden controlables con sendos PI.

## Fundamento teórico
La dinámica del filtro en dq incluye los términos de Coriolis del marco giratorio (ver [[marco-dq]]):
$$ L\frac{di_d}{dt}=v_d-e_d+\omega L\,i_q-R i_d,\qquad
   L\frac{di_q}{dt}=v_q-e_q-\omega L\,i_d-R i_q $$
con \( v_{dq} \) tensión del convertidor y \( e_{dq} \) tensión de red. Eligiendo la ley de control
$$ v_d=v_d'-\omega L\,i_q+e_d,\qquad v_q=v_q'+\omega L\,i_d+e_q $$
los términos cruzados y la perturbación de red **se cancelan**, y queda
$$ L\frac{di_d}{dt}=v_d'-R i_d \ \Rightarrow\ \frac{i_d}{v_d'}=\frac{1}{Ls+R} $$
es decir, dos plantas de primer orden idénticas y **desacopladas**, donde \( v_{dq}' \) lo fija el
PI. El feedforward de \( e_{dq} \) mejora el rechazo de perturbación de red y la respuesta ante
huecos; el desacoplo de \( \omega L \) elimina el sobreimpulso cruzado en transitorios de par.

<div class="cfig"><img src="figuras/desacoplo-dq-bloques.png" alt="lazo de corriente con desacoplo"><div class="cap">Lazo de corriente del eje d: el término de desacoplo −ωL·iq se inyecta antes de la planta para cancelar el acoplamiento cruzado +ωL·iq, dejando una planta SISO 1/(Ls+R) que el PI controla sin interferencia del eje q.</div></div>

<div class="cfig"><img src="figuras/desacoplo-dq-analisis.png" alt="analisis ampliado: simulacion temporal, rechazo de red, bode MIMO, sensibilidad L"><div class="cap">Análisis ampliado: (a) escalón id*=1000 A con iq*=0: sin desacoplo iq se excursiona ~50 A, con desacoplo iq≈0; (b) perturbación ed=100 V: feedforward cancela antes de actuar; (c) Bode MIMO, el acoplamiento |Zdq|=ωL es constante; (d) acoplamiento residual vs error en L: lineal y pequeño para ±10%.</div></div>

## 1 — Sintonía IMC del PI sobre la planta SISO \( 1/(Ls+R) \)

Tras cancelar los términos \( \pm\omega L \) por desacoplo, cada eje queda con la planta de primer orden:
$$ G(s)=\frac{i_d}{v_d'}=\frac{1}{Ls+R} $$

**Paso 1 — forma IMC del PI.** El método *Internal Model Control* elige el PI de manera que la función de lazo abierto sea un integrador puro de ganancia \( \alpha_c \) (ancho de banda en rad/s). Con \( C(s)=K_p+K_i/s \):

$$ L_{OL}(s)=C(s)\,G(s)=\frac{K_p s+K_i}{s}\cdot\frac{1}{Ls+R} $$

Para que se cancele el polo de la planta, se pide que el cero del PI coincida con ese polo:

$$ \frac{K_i}{K_p}=\frac{R}{L}\quad\Rightarrow\quad K_p=L\,\alpha_c,\quad K_i=R\,\alpha_c $$

siendo \( \alpha_c \) la frecuencia de cruce deseada.

**Paso 2 — lazo abierto resultante.** Sustituyendo:

$$ L_{OL}(s)=\frac{\alpha_c(Ls+R)}{s(Ls+R)}=\frac{\alpha_c}{s} $$

Integrador puro: pendiente \(-20\) dB/dec y fase \(-90°\) constante — margen de fase de **90°** independientemente de \( \alpha_c \).

**Paso 3 — lazo cerrado.** Con la retroalimentación unitaria:

$$ \frac{i_d}{i_d^*}=\frac{L_{OL}}{1+L_{OL}}=\frac{\alpha_c/s}{1+\alpha_c/s}=\boxed{\frac{\alpha_c}{s+\alpha_c}} $$

Sistema de **primer orden** con constante de tiempo \( \tau_c=1/\alpha_c \): la corriente sigue la referencia con ancho de banda exactamente igual a \( \alpha_c \), sin sobreimpulso y sin depender de \( L \) ni \( R \) (están cancelados).

**Paso 4 — valores numéricos de ejemplo.** Para \( L=2\,\text{mH} \), \( R=0.05\,\Omega \), \( \alpha_c=2\pi\cdot1000\,\text{rad/s} \):

$$ K_p=L\,\alpha_c=0.002\times6283=\mathbf{12.57}\,\Omega,\qquad K_i=R\,\alpha_c=0.05\times6283=\mathbf{314}\,\text{Ω/s} $$

La relación \( T_i=K_p/K_i=L/R=0.04\,\text{s} \) es la constante de tiempo eléctrica del filtro.

## 2 — El acoplamiento dq como perturbación: sin desacoplo vs con desacoplo

Sin desacoplo, las ecuaciones del lazo de corriente son:
$$
L\dot{i}_d = v_d - e_d + \omega L\,i_q - R\,i_d, \qquad
L\dot{i}_q = v_q - e_q - \omega L\,i_d - R\,i_q
$$

El término \( +\omega L\,i_q \) en la ecuación de \( i_d \) actúa como una perturbación sobre el eje d cuando varía \( i_q \), y viceversa.

**Paso 1 — cuantificar la perturbación cruzada.** Ante un escalón de referencia \( \Delta i_d^* \), durante el transitorio \( i_d \) varía de 0 a \( \Delta i_d \). Este cambio acopla a la ecuación de \( i_q \) mediante el término \( -\omega L\,i_d \). En régimen de pequeña señal, el PI intenta rechazar esta perturbación, pero hasta que el integrador actúa, la corriente \( i_q \) se desvía. La amplitud máxima del error cruzado puede estimarse como:

$$
\Delta i_{q,\max}\approx\frac{\omega L\,\Delta i_d}{K_p}
$$

La razón es que \( K_p \) es la ganancia proporcional que se opone inmediatamente a la perturbación; el integrador solo actúa después. Esta expresión muestra que el acoplamiento crece con \( \omega \) (peor a alta frecuencia fundamental o en arranques a frecuencia nominal) y disminuye al aumentar \( K_p \).

**Paso 2 — ejemplo numérico sin desacoplo.** Para \( L=2\,\text{mH} \), \( \omega=314\,\text{rad/s} \), \( K_p=12.6\,\Omega \), \( \Delta i_d=1000\,\text{A} \):
$$
\Delta i_{q,\max}\approx\frac{314\times0.002\times1000}{12.6}\approx\mathbf{50}\,\text{A}
$$
Sobre una corriente base de 1000 A, esto representa el **5%** — significativo para control de calidad de energía, aunque no siempre problemático para protecciones.

**Paso 3 — con desacoplo.** La ley de control \( v_d=v_d'-\omega L\,i_q \) cancela exactamente el término \( +\omega L\,i_q \) antes de que llegue al PI. El desacoplo es un bloque de **prealimentación** (feedforward), no retroalimentación: no cierra ningún lazo adicional y no afecta a la estabilidad del lazo de corriente. Con desacoplo perfecto, \( \Delta i_q=0 \) durante el escalón de \( i_d^* \).

**Paso 4 — error residual con ω incorrecto.** Si se usa una estimación \( \hat{\omega} \) en lugar de \( \omega \) real, el término cancelado es \( \hat{\omega}L\,i_q \) y queda un residuo \( (\omega-\hat{\omega})L\,i_q \). Este residuo entra a la planta como perturbación no cancelada pero es pequeño mientras \( |\omega-\hat{\omega}| \) sea pequeño.

## 3 — Feedforward de tensión de red: rechazo de perturbación

La tensión de red \( e_d, e_q \) actúa como perturbación sobre el lazo de corriente. Sin feedforward, el PI debe rechazarla; con feedforward, se cancela algebraicamente antes de que actúe.

**Paso 1 — función de transferencia de perturbación sin feedforward.** Considerando solo el eje d con planta \( 1/(Ls+R) \) y PI \( C(s)=K_p+K_i/s \), la FDT de perturbación \( e_d\to i_d \) con retroalimentación es:

$$
\frac{i_d}{e_d}\bigg|_{\text{sin FF}}=\frac{-1/(Ls+R)}{1+C(s)/(Ls+R)}=\frac{-1}{Ls+R+C(s)}=\frac{-s}{Ls^2+(R+K_p)s+K_i}
$$

Para frecuencias bajas (\( s\to0 \)): \( i_d/e_d\to 0 \) (el integrador rechaza la perturbación en DC). Pero la **velocidad de rechazo** es limitada: el tiempo de recuperación es \( \approx 1/\alpha_c \).

**Paso 2 — con feedforward de ed.** Si la ley de control añade \( v_d\leftarrow v_d+\hat{e}_d \) (donde \( \hat{e}_d \) es la estimación de \( e_d \)), la perturbación se cancela directamente:

$$
L\dot{i}_d=(v_d'+\hat{e}_d)-e_d-R\,i_d=v_d'-(e_d-\hat{e}_d)-R\,i_d
$$

Con \( \hat{e}_d=e_d \) (cancelación perfecta), \( i_d/e_d=0 \) — rechazo instantáneo e independiente del ancho de banda.

**Paso 3 — por qué filtrar ed antes del feedforward.** En la práctica, \( \hat{e}_d \) proviene de una medida de tensión que contiene ruido. Si \( \hat{e}_d \) se inyecta directamente, el ruido de alta frecuencia entra a la modulación y se traduce en distorsión de la tensión de salida del convertidor. La solución es pasar \( e_d \) medida por un filtro pasa-bajos \( F(s)=\omega_f/(s+\omega_f) \) con \( \omega_f \ll \omega_{sw} \). El feedforward filtrado cancela la componente fundamental y las perturbaciones lentas (huecos de red, variaciones de frecuencia) sin amplificar el ruido de conmutación.

**Paso 4 — compromiso.** Un filtro más estrecho (\( \omega_f \) pequeño) reduce más el ruido pero introduce un retardo que degrada la cancelación rápida de perturbaciones. El compromiso habitual es \( \omega_f\approx(0.1\text{–}0.3)\,\alpha_c \): filtra suficiente sin retardar la cancelación.

## 4 — La planta MIMO 2×2 en dq: función de transferencia matricial

Sin desacoplo, el par \( (i_d,\,i_q) \) responde a la pareja \( (v_d,\,v_q) \) como un sistema MIMO 2×2. Comprender esta estructura matricial explica por qué los polos del lazo no están en el eje real y qué significa el acoplamiento.

**Paso 1 — ecuación de estado vectorial.** Definiendo \( \mathbf{i}=[i_d\;i_q]^\top \), \( \mathbf{v}=[v_d\;v_q]^\top \), \( \mathbf{e}=[e_d\;e_q]^\top \), y la matriz antisimétrica \( \mathbf{J}=\bigl[\begin{smallmatrix}0&-1\\1&0\end{smallmatrix}\bigr] \):

$$
L\dot{\mathbf{i}}=\mathbf{v}-\mathbf{e}-R\mathbf{i}+\omega L\mathbf{J}\mathbf{i}
$$

**Paso 2 — transformada de Laplace.** En frecuencia:
$$
(sL+R)\mathbf{I}-\omega L\mathbf{J}\mathbf{I}=\mathbf{V}-\mathbf{E}
\;\Longrightarrow\;
\mathbf{Z}_{dq}(s)\,\mathbf{I}=\mathbf{V}-\mathbf{E}
$$
con la **matriz de impedancia** del sistema dq:
$$
\mathbf{Z}_{dq}(s)=\begin{bmatrix}sL+R & -\omega L \\ \omega L & sL+R\end{bmatrix}
$$

**Paso 3 — función de transferencia matricial (planta MIMO).** La planta vista por el controlador es \( \mathbf{Z}_{dq}^{-1}(s) \):

$$
\mathbf{I}=\mathbf{Z}_{dq}^{-1}(s)(\mathbf{V}-\mathbf{E}),
\qquad
\mathbf{Z}_{dq}^{-1}=\frac{1}{(sL+R)^2+(\omega L)^2}
\begin{bmatrix}sL+R & \omega L \\ -\omega L & sL+R\end{bmatrix}
$$

Los términos diagonales \( Z_{dd}^{-1}=Z_{qq}^{-1}=(sL+R)/[(sL+R)^2+(\omega L)^2] \) son la planta directa de cada eje, y los términos cruzados \( \pm\omega L/[(sL+R)^2+(\omega L)^2] \) son el acoplamiento.

**Paso 4 — polos de la planta MIMO.** Los polos están donde el denominador se anula:
$$
(sL+R)^2+(\omega L)^2=0 \;\Longrightarrow\; s=-\frac{R}{L}\pm j\omega
$$

Los polos del sistema dq sin desacoplo están en \( -R/L\pm j\omega \): tienen una **parte imaginaria de \( \pm j\omega_0 \)** (en nuestro caso \( \pm j314\,\text{rad/s} \)). Esto significa que la planta MIMO tiene una **resonancia a la frecuencia fundamental** en el marco giratorio, lo que dificulta el control directo (el Bode de la planta tiene un pico a \( f_0=50\,\text{Hz} \) en el marco estacionario).

**Paso 5 — efecto del desacoplo.** Con la ley de desacoplo completa \( \mathbf{v}=\mathbf{v}'-\omega L\mathbf{J}\mathbf{i}+\mathbf{e} \), la planta se convierte en:
$$
\mathbf{Z}_{dq,\text{desacopl}}(s)=\begin{bmatrix}sL+R & 0 \\ 0 & sL+R\end{bmatrix}
$$
**Dos SISO independientes**, cada uno con polo en \( s=-R/L \) (sin parte imaginaria) — planta trivial de sintonizar con IMC.

## 5 — Robustez del desacoplo: incertidumbre en L y en ω

En la práctica, \( L \) y \( \omega \) se conocen con error. Cuantificar el acoplamiento residual que queda permite decidir si el desacoplo sigue siendo útil.

**Paso 1 — incertidumbre en L.** Sea \( L_{\text{real}}=L_{\text{nom}}(1+\delta_L) \) con \( |\delta_L|<0.1 \) (10% de incertidumbre). El término de desacoplo calculado es \( \omega L_{\text{nom}} i_q \), pero el acoplamiento real es \( \omega L_{\text{real}} i_q \). El residuo que no se cancela es:

$$
\Delta v_d^{\text{res}}=\omega\,\delta_L\,L_{\text{nom}}\,i_q
$$

Este residuo actúa como perturbación sobre el eje d. El acoplamiento cruzado residual inducido en \( i_q \) ante un escalón de \( i_d \) es:

$$
\Delta i_{q,\text{res}}\approx\frac{\omega\,\delta_L\,L_{\text{nom}}\,\Delta i_d}{K_p}=\delta_L\cdot\frac{\omega L_{\text{nom}}}{K_p}\,\Delta i_d
$$

Para \( \delta_L=0.10 \): \( \Delta i_{q,\text{res}}=0.10\times50\,\text{A}=5\,\text{A} \), es decir el 0.5% de \( \Delta i_d=1000\,\text{A} \) — despreciable.

**Paso 2 — variación de ω (arranque).** A baja frecuencia (arranque desde \( f=0 \)), el término de acoplamiento \( \omega L i_q \) es pequeño porque \( \omega\to0 \). El desacoplo no es necesario durante el arranque; conforme \( \omega \) sube, el acoplamiento crece proporcionalmente y el desacoplo va siendo más importante.

**Paso 3 — efecto del retardo digital.** El DSP calcula \( \omega L_{\text{nom}} i_q[k] \) usando la muestra \( i_q[k] \) del instante actual, pero la salida se aplica a la modulación un ciclo más tarde (\( T_s \)). Durante ese ciclo, \( i_q \) puede variar en \( \Delta i_q=T_s\,\dot{i}_q \). El error en el desacoplo por retardo es:

$$
\delta v_d^{\text{ret}}=\omega L_{\text{nom}}\,T_s\,\dot{i}_q\approx\omega L_{\text{nom}}\,T_s\,\frac{\alpha_c\,\Delta i_q}{1}
$$

Para corrientes que varían lentamente respecto a \( 1/T_s \), este término es despreciable. Solo a frecuencias de commutation comparables a \( 1/T_s \) podría importar, pero en ese rango el lazo de corriente ya no tiene ganancia.

**Tabla de robustez — parámetros del ejemplo (L=2 mH, R=50 mΩ, αc=2π·750 Hz):**

| Fuente de error | δ | Δiq residual | % de Δid=1000 A |
|-----------------|---|-------------|-----------------|
| Sin desacoplo | — | 50 A | 5% |
| δL = 5% | 0.05 | 2.5 A | 0.25% |
| δL = 10% | 0.10 | 5 A | 0.5% |
| δL = 20% | 0.20 | 10 A | 1% |
| Retardo Ts=100 µs | — | <1 A (para αc<1kHz) | <0.1% |

El desacoplo es robusto: incluso con 20% de error en L, el acoplamiento residual es 5 veces menor que sin desacoplo.

## 6 — Diseño iterativo: lazo de corriente completo con desacoplo y feedforward

**Especificación:** \( \alpha_c=2\pi\cdot1000\,\text{Hz} \), margen de fase \( \text{PM}\ge45° \) con retardo total \( 1.5\,T_s=150\,\mu\text{s} \), acoplamiento residual \( \Delta i_q/\Delta i_d<5\% \).

**Paso 1 — sintonía IMC sin retardo.** Cancelando el polo de la planta:
$$
K_p=L\,\alpha_c=0.002\times6283=12.57\,\Omega,\qquad K_i=R\,\alpha_c=0.05\times6283=314\,\text{Ω/s}
$$
El lazo abierto ideal es \( L_{OL}(s)=\alpha_c/s \), con PM=90°.

**Paso 2 — efecto del retardo digital.** El retardo total \( \tau_d=1.5\,T_s=150\,\mu\text{s} \) añade fase negativa en la frecuencia de cruce:
$$
\Delta\phi=-\alpha_c\,\tau_d\cdot\frac{180°}{\pi}=-6283\times150\times10^{-6}\times\frac{180°}{\pi}=-54°
$$
$$
\text{PM}_{\text{real}}=90°-54°=36°\quad\textbf{✗ no cumple PM}\ge45°
$$

**Paso 3 — reducir αc a 750 Hz.** Con \( \alpha_c=2\pi\times750=4712\,\text{rad/s} \):
$$
K_p=0.002\times4712=9.42\,\Omega,\qquad K_i=0.05\times4712=236\,\text{Ω/s}
$$
$$
\Delta\phi=-4712\times150\times10^{-6}\times\frac{180°}{\pi}=-40.5°\;\Rightarrow\;\text{PM}=90°-40.5°=\mathbf{49.5°}\quad\checkmark
$$

**Paso 4 — verificar acoplamiento sin desacoplo.** Con \( \alpha_c=750\,\text{Hz} \) y \( K_p=9.42 \):
$$
\frac{\Delta i_q}{\Delta i_d}\bigg|_{\text{sin des.}}=\frac{\omega L}{K_p}=\frac{314\times0.002}{9.42}=0.0667\quad\Rightarrow\;\mathbf{6.7\%}\quad\textbf{✗ no cumple <5%}
$$

**Paso 5 — añadir desacoplo.** Con la cancelación algebraica \( v_d\leftarrow v_d-\omega L\,i_q \):
$$
\frac{\Delta i_q}{\Delta i_d}\bigg|_{\text{con des.}}\approx 0\quad\checkmark
$$

**Paso 6 — verificar con L incierto ±10%.** El acoplamiento residual con \( \delta_L=10\% \):
$$
\frac{\Delta i_q}{\Delta i_d}\bigg|_{\delta_L=10\%}=\frac{0.10\times\omega L}{K_p}=\frac{0.10\times0.628}{9.42}=0.0067\;\Rightarrow\;\mathbf{0.67\%}\quad\checkmark
$$

**Tabla de iteraciones completa:**

| Paso | αc [Hz] | Kp [Ω] | PM [°] | Δiq/Δid [%] | Estado |
|------|---------|--------|--------|------------|--------|
| 1 (sin retardo) | 1000 | 12.57 | 90° | 5.0% sin des | ref |
| 2 (con retardo) | 1000 | 12.57 | 36° | 5.0% sin des | PM ✗ |
| 3 | 750 | 9.42 | 49.5° | 6.7% sin des | PM ✓, Δiq ✗ |
| 4 (+ desacoplo) | 750 | 9.42 | 49.5° | ≈0% ideal | ✓✓ |
| 5 (δL=10%) | 750 | 9.42 | 49.5° | 0.67% res | ✓✓✓ |

El diseño final es \( \alpha_c=750\,\text{Hz} \), \( K_p=9.42\,\Omega \), \( K_i=236\,\text{Ω/s} \), con desacoplo \( \omega L\,i_q / \omega L\,i_d \) y feedforward de \( e_{dq} \) filtrado con \( \omega_f\approx200\,\text{rad/s} \).

## Cuándo y por qué se usa
En todo control vectorial de corriente de convertidores y máquinas, sobre todo cuando \( \omega L \)
es grande (alta frecuencia o inductancia), donde el acoplamiento degrada notablemente la respuesta.
Es la base del lazo interno de la [[control-cascada]].

## Procedimiento de diseño (genérico)
1. Modela el filtro en dq e identifica los términos \( \pm\omega L \) y \( e_{dq} \).
2. Implementa el desacoplo (resta/suma \( \omega L\,i \)) y el feedforward de \( e_{dq} \) filtrada.
3. Diseña los PI sobre la planta SISO \( 1/(Ls+R) \) con IMC: \( K_p=L\,\alpha_c \), \( K_i=R\,\alpha_c \).
4. Verifica PM con el retardo digital \( 1.5\,T_s \) y reduce \( \alpha_c \) si es necesario.
5. Verifica robustez al error de estimación de \( L \) y \( \omega \).

## Ejemplo de aplicación real
**Problema:** VSC trifásico con \( L=2\,\text{mH} \), \( R=0.05\,\Omega \), \( \omega=314\,\text{rad/s} \). Cuantificar el acoplamiento sin desacoplo y verificar que tras añadir el feedforward desaparece.

Sin desacoplo: una referencia \( i_d^*=1000\,\text{A} \), \( i_q^*=0 \) produce, durante el transitorio, un error cruzado en \( i_q \) de amplitud \( \approx\omega L\Delta i_d/K_p=314\times0.002\times1000/12.6\approx50\,\text{A} \). Con desacoplo: se añade \( v_d\leftarrow v_d-\omega L i_q \) y \( v_q\leftarrow v_q+\omega L i_d \). El término cruzado se cancela algebraicamente y \( i_q \) permanece en 0 durante el escalón de \( i_d^* \). Con \( L \) con error del 10%: el residuo de acoplamiento es \( 0.1\times50\approx5\,\text{A} \), despreciable en la mayoría de aplicaciones.

## Ejemplo de código
```python
def current_ctrl(id_ref, iq_ref, id_, iq_, ed, eq, w, L, pi_d, pi_q):
    vd = pi_d(id_ref - id_) - w*L*iq_ + ed      # desacoplo + feedforward
    vq = pi_q(iq_ref - iq_) + w*L*id_ + eq
    return vd, vq
```

## Parámetros y valores típicos
Ancho de banda del lazo de corriente \( \alpha_c \approx (1/10\text{–}1/5)\,\omega_{sw} \).
El desacoplo importa cuando \( \omega L \gtrsim R \) (casi siempre en convertidores de red).
Para \( L=2\,\text{mH} \), \( \omega=314 \): \( \omega L=0.628\,\Omega \gg R=0.05\,\Omega \) — el desacoplo es esencial.

## Errores comunes
- Usar \( L \) o \( \omega \) erróneos → desacoplo imperfecto y acoplamiento residual.
- Feedforward de \( e_{dq} \) ruidoso (medida sucia) → inyecta ruido en la modulación; filtrar.
- Olvidar el retardo digital, que reintroduce acoplamiento efectivo a alta frecuencia.
- Ignorar que la planta MIMO sin desacoplo tiene polos en \( -R/L\pm j\omega \): la respuesta en frecuencia tiene un pico a 50 Hz que puede complicar la sintonía si se diseña ignorando el marco dq.

## Conceptos relacionados
- [[marco-dq]] · [[control-cascada]] · [[control-vectorial]] · [[controlador-pid]] · [[filtro-lcl]] · [[respuesta-segundo-orden]]

## Referencias
- Yazdani, Iravani, 2010.
- Kazmierkowski, Krishnan, Blaabjerg, *Control in Power Electronics*, 2002.
