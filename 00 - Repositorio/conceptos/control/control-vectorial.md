---
titulo: Control vectorial (orientación de campo / red)
slug: control-vectorial
categoria: control
tipo: tecnica
nivel: avanzado
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [controlar corriente trifasica desacoplando par/flujo o P/Q en dq]
tags: [control-vectorial, FOC, VOC, dq, orientacion-de-campo, desacoplo, PLL, sensorless]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [marco-dq, control-cascada, potencia-instantanea-dq, pll-srf, desacoplo-dq]
referencias:
  - "Kazmierkowski, Krishnan, Blaabjerg, Control in Power Electronics, Academic Press 2002"
  - "Vas, Sensorless Vector and Direct Torque Control, Oxford 1998"
  - "Blaabjerg et al., Overview of Control and Grid Synchronization for Distributed Power Generation Systems, IEEE TIE 2006"
---

## Definición
Estrategia que controla las magnitudes trifásicas como **vectores espaciales** en un marco dq
**orientado** con una variable física (el flujo del rotor en máquinas, la tensión de red en
convertidores). Al orientar el marco, las dos componentes \( d \) y \( q \) controlan magnitudes
desacopladas.

## Fundamento teórico
Un sistema trifásico equilibrado se representa por un **vector espacial** que, llevado a dq con
el ángulo de orientación \( \theta \) (ver [[marco-dq]]), queda constante en régimen permanente.
Con la orientación adecuada:
- **Máquinas (FOC, Field-Oriented Control)**: marco alineado con el flujo de rotor. Entonces
  \( i_d \) controla el **flujo** y \( i_q \) controla el **par**:
  \( T \propto \psi\, i_q \). Se controla la máquina como una de continua.
- **Convertidor conectado a red (VOC, Voltage-Oriented Control)**: marco alineado con la tensión
  de red (\( v_q=0 \), vía [[pll-srf]]). Entonces \( i_d \leftrightarrow P \) e
  \( i_q \leftrightarrow Q \) (ver [[potencia-instantanea-dq]]).

En ambos casos se cierran **lazos de corriente PI sobre \( i_d, i_q \)** con **desacoplo** de los
términos cruzados \( \pm\omega L\,i \) que introduce el marco giratorio. Es la base de los lazos
internos de casi todos los convertidores y accionamientos.

<div class="cfig"><img src="figuras/control-vectorial-orientacion.png" alt="diagrama de orientacion dq con la tension en el eje d"><div class="cap">Al orientar el marco dq con la tensión de red (\(v_q=0\), vía PLL), la corriente se descompone en \(i_d\) —que gobierna la potencia activa P— e \(i_q\) —que gobierna la reactiva Q—, controlables de forma independiente con dos PI. En máquinas el marco se alinea con el flujo y entonces \(i_d\) es flujo e \(i_q\) es par.</div></div>

## 1 — Orientación del marco dq: por qué \( v_d=V \), \( v_q=0 \) desacopla P de Q

**Paso 1 — vector espacial de tensión de red en αβ.** La red trifásica equilibrada produce una tensión \( \mathbf{v}_{red}(t) \) que, transformada con Clarke, es un fasor giratorio de módulo \( V \) y ángulo \( \theta(t)=\omega t \). En αβ:

$$ \mathbf{v}_{\alpha\beta} = V\,e^{j\theta} $$

**Paso 2 — elección del ángulo de orientación.** Se lleva ese fasor al marco dq girante con el mismo \( \theta \) extraído por la PLL (ver [[pll-srf]]). La transformada de Park alinea el eje d con \( \mathbf{v}_{red} \):

$$ \begin{pmatrix}v_d\\v_q\end{pmatrix} = \begin{pmatrix}\cos\theta & \sin\theta\\-\sin\theta & \cos\theta\end{pmatrix}\begin{pmatrix}v_\alpha\\v_\beta\end{pmatrix} = \begin{pmatrix}V\\0\end{pmatrix} $$

El vector de tensión cae exactamente sobre el eje d, de modo que \( v_d = V \) y \( v_q = 0 \) en régimen permanente.

**Paso 3 — potencia instantánea en dq.** Con la convención de potencia instantánea trifásica (ver [[potencia-instantanea-dq]]) y el factor \( \tfrac{3}{2} \) de la transformada de Park normalizada:

$$ P = \tfrac{3}{2}(v_d\,i_d + v_q\,i_q),\qquad Q = \tfrac{3}{2}(v_q\,i_d - v_d\,i_q) $$

**Paso 4 — sustitución de la orientación.** Sustituyendo \( v_d=V \), \( v_q=0 \):

$$ \boxed{P = \tfrac{3}{2}\,V\,i_d}, \qquad \boxed{Q = -\tfrac{3}{2}\,V\,i_q} $$

**Conclusión.** La potencia activa depende únicamente de \( i_d \) y la reactiva únicamente de \( i_q \). Cerrar un lazo PI sobre \( i_d \) controla P sin perturbar Q, y viceversa: el control vectorial orientado a la tensión de red produce **desacoplo P–Q natural** a partir de la geometría de la transformada, no de cancelaciones complicadas.

## 2 — La transformación Park en el control vectorial

La orientación del vector de referencia (flujo del rotor en FOC, tensión de red en VOC) en el eje d es la operación que hace posible el control vectorial. No es un truco algebraico: es la consecuencia de elegir \( \theta \) tal que \( \mathbf{v}_{ref} \) sea paralelo al eje d.

**Para motores de inducción (FOC).** El vector de flujo del rotor \( \boldsymbol{\Psi}_r \) tiene módulo \( |\Psi_r| \) y un ángulo \( \theta_r \) que depende de la velocidad del rotor y del deslizamiento. Si se orienta el marco dq con ese ángulo exacto:

$$ \Psi_{r,d} = |\Psi_r|, \qquad \Psi_{r,q} = 0 $$

El par electromagético del motor de inducción en el marco orientado al flujo es exactamente:

$$ T_e = \frac{3}{2}\,\frac{L_m}{L_r}\,|\Psi_r|\,i_q $$

Con \( |\Psi_r| \) constante (controlado lentamente vía \( i_d \)), el par es proporcional a \( i_q \) solo. La máquina AC se comporta como una de continua con excitación separada.

**Para convertidores de red (VOC).** La PLL extrae \( \theta_{PLL} \) de la tensión en el PCC. La orientación \( v_q=0 \) garantiza:

$$ P = \tfrac{3}{2}\,V_{PCC}\,i_d, \qquad Q = -\tfrac{3}{2}\,V_{PCC}\,i_q $$

La jerarquía de control es: PLL → \( \theta \) → lazo de corriente dq → lazo exterior de potencia/tensión. La calidad de la orientación limita directamente la precisión del desacoplo P/Q.

**Error de orientación.** Si \( \theta \) tiene un error \( \Delta\theta \), la corriente medida en el marco erróneo tiene componentes cruzadas:

$$ i_{d,meas} = i_d\cos\Delta\theta + i_q\sin\Delta\theta, \qquad i_{q,meas} = -i_d\sin\Delta\theta + i_q\cos\Delta\theta $$

Un error de \( \Delta\theta = 10° \) introduce un acoplamiento del orden de \( \sin(10°)\approx 17\% \): la referencia de reactiva afecta a la potencia activa y viceversa. Mantener \( \Delta\theta < 5° \) es el requisito de precisión típico para la PLL.

## 3 — FOC para motores de inducción

El motor de inducción en el marco dq orientado al flujo del rotor obedece las siguientes ecuaciones de estado (notación estándar: \( L_s, L_r, L_m \) inductancias propio, rotor, mutua; \( R_s, R_r \) resistencias; \( \sigma = 1 - L_m^2/(L_s L_r) \) coeficiente de dispersión; \( \omega \) velocidad angular eléctrica):

$$ \sigma L_s \frac{d i_d}{dt} = v_d - R_s i_d + \omega \sigma L_s i_q - \frac{L_m}{L_r}\frac{d |\Psi_r|}{dt} $$

$$ \sigma L_s \frac{d i_q}{dt} = v_q - R_s i_q - \omega \sigma L_s i_d - \frac{L_m}{L_r}\omega_r |\Psi_r| $$

$$ \frac{d |\Psi_r|}{dt} = -\frac{R_r}{L_r}|\Psi_r| + \frac{R_r L_m}{L_r} i_d $$

donde \( \omega_r = \omega - \omega_{slip} \) es la velocidad del rotor. La **constante de tiempo del rotor** es:

$$ \tau_r = \frac{L_r}{R_r} $$

En un motor típico de media tensión, \( \tau_r \sim 0.1\text{–}1\,\text{s} \). El lazo de corriente tiene un ancho de banda de varios cientos de Hz. La **separación temporal** entre la dinámica del flujo (\( 1/\tau_r \)) y la del par (\( \alpha_c \)) es:

$$ \tau_r \gg \frac{1}{\alpha_c} $$

Esto valida el supuesto FOC estándar: durante un transitorio de par (variación de \( i_q^* \)), el flujo \( |\Psi_r| \) permanece prácticamente constante, así que el par responde instantáneamente a \( i_q^* \) sin afectar al flujo.

**El lazo de control FOC tiene dos ramas:**

- **Rama de flujo (lenta):** \( i_d^* = |\Psi_r^*|/L_m \). El PI externo regula \( |\Psi_r| \) con ancho de banda \( \alpha_\psi \approx 1/(3\tau_r) \). En operación nominal \( i_d \) es constante.

- **Rama de par (rápida):** \( i_q^* = T_e^* / \bigl(\tfrac{3}{2}\tfrac{L_m}{L_r}|\Psi_r|\bigr) \). Responde al PI de corriente con \( \alpha_c \gg \alpha_\psi \). El par varía en pocos milisegundos.

**Cálculo del ángulo de deslizamiento.** Para conocer \( \theta_r \) hay que integrar \( \omega_{slip} \):

$$ \omega_{slip} = \frac{R_r L_m i_q^*}{L_r |\Psi_r^*|}, \qquad \theta_r = \int_0^t (\omega_{mec} + \omega_{slip})\,d\tau $$

Este cálculo usa \( R_r \) y \( L_r \), que varían con la temperatura y la saturación. Es la principal fuente de error en FOC sin sensor.

## 4 — VOC para convertidores de red

En convertidores conectados a red, el FOC se llama **VOC (Voltage-Oriented Control)**: el vector de referencia es la tensión en el PCC en lugar del flujo del rotor.

**Estructura completa del VOC:**

1. **PLL** mide \( v_{\alpha\beta} \) y extrae \( \theta_{PLL} \) y \( V_{PCC} \).
2. **Transformada de Park** lleva las corrientes medidas \( i_{abc} \rightarrow i_{dq} \) con \( \theta_{PLL} \).
3. **Lazo de corriente dq** (ver [[desacoplo-dq]]): dos PI con desacoplo cruzado \( \mp\omega L \) y feedforward de tensión:

$$ v_d^* = K_p(i_d^* - i_d) + K_i \int e_d\,dt - \omega L\,i_q + v_d^{ff} $$
$$ v_q^* = K_p(i_q^* - i_q) + K_i \int e_q\,dt + \omega L\,i_d + v_q^{ff} $$

4. **Lazo exterior** de potencia o tensión: genera \( i_d^* \) e \( i_q^* \) a partir de referencias de \( P, Q \) o \( V_{PCC} \).
5. **Antitransformada** \( v_{dq}^* \rightarrow v_{abc}^* \) y modulación PWM.

**Diseño del lazo de corriente.** Con cancelación de polo (ver [[control-cascada]]):

$$ K_p = L\,\alpha_c, \qquad K_i = R\,\alpha_c $$

El ancho de banda \( \alpha_c \) se limita por el retardo digital \( \tau_d = 1.5\,T_s \):

$$ \alpha_c < \frac{PM}{\tau_d} = \frac{PM}{1.5\,T_s} $$

Con \( PM=45° \) y \( T_s=100\,\mu\text{s} \): \( \alpha_c < \frac{\pi/4}{150\,\mu\text{s}} \approx 5236\,\text{rad/s} \approx 833\,\text{Hz} \). En la práctica se usa \( \alpha_c = 2\pi \cdot 750\,\text{Hz} \) para dejar margen.

**Robustez ante red débil.** El VOC depende de la PLL para orientar el marco. En red débil (SCR < 3), la tensión en el PCC es muy sensible a la corriente inyectada: la PLL tiende a oscilar porque la tensión que mide ya contiene el efecto de la corriente que ella misma genera (lazo positivo). La condición aproximada de estabilidad de la PLL en red débil es:

$$ K_{p,PLL}\,\omega_0\,X_{th} \ll V_{PCC} $$

Cuando esto no se cumple, la PLL destabiliza el lazo de potencia. La solución es reducir el ancho de banda de la PLL, añadir filtros, o pasar a control grid-forming que no necesita PLL (ver [[grid-forming-vs-following]]).

## 5 — Control vectorial sin sensores

En muchas aplicaciones no se puede medir el ángulo directamente (sin encoder en el motor, sin PMU en red débil). El control vectorial sin sensores estima el vector de referencia a partir de las medidas eléctricas.

**Estimador de flujo por voltaje (integración pura).** En αβ:

$$ \hat{\Psi}_\alpha = \int (v_\alpha - R_s i_\alpha)\,dt, \qquad \hat{\Psi}_\beta = \int (v_\beta - R_s i_\beta)\,dt $$

El módulo y el ángulo del flujo estimado son:

$$ |\hat{\Psi}_r| = \sqrt{\hat{\Psi}_\alpha^2 + \hat{\Psi}_\beta^2}, \qquad \hat{\theta}_r = \mathrm{atan2}(\hat{\Psi}_\beta, \hat{\Psi}_\alpha) $$

**Problema práctico.** El integrador puro acumula el offset de tensión y la incertidumbre de \( R_s \), produciendo deriva a baja velocidad. La solución estándar es el **filtro de paso bajo de baja frecuencia** o el integrador con saturación regenerativa.

**Observador MRAS (Model Reference Adaptive System) de Gopinath.** Se tienen dos modelos:

- **Modelo de referencia** (independiente de \( \omega \)): ecuaciones de la corriente de estátor que dan \( \hat{\Psi}_r^{ref} \) sin usar la velocidad.
- **Modelo adaptable**: ecuaciones del rotor que usan \( \hat{\omega} \) estimada y dan \( \hat{\Psi}_r^{adj} \).

El error entre ambas estimaciones alimenta un mecanismo adaptativo (PI) que ajusta \( \hat{\omega} \) hasta anularlo:

$$ \varepsilon_{MRAS} = \hat{\Psi}_\alpha^{ref}\,\hat{\Psi}_\beta^{adj} - \hat{\Psi}_\beta^{ref}\,\hat{\Psi}_\alpha^{adj} $$

$$ \hat{\omega} = K_p^{MRAS}\,\varepsilon_{MRAS} + K_i^{MRAS}\int \varepsilon_{MRAS}\,dt $$

El MRAS es estable bajo condiciones de persistencia de excitación (la corriente no puede ser constante).

**Para convertidores sin medida de tensión de red.** En lugar de la PLL, se puede estimar \( v_d \) a partir del modelo de la planta:

$$ \hat{v}_d = v_d^* - (sL + R)\,i_d + \omega L\,i_q $$

Esto solo funciona si el modelo de \( L \) y \( R \) es preciso. Variaciones del 10% de \( L \) producen un error de orientación de \( \sim 10° \) que introduce el 17% de acoplamiento P/Q que cuantifica el panel (c) de la figura.

**Sensibilidad paramétrica.**
- \( R \) varía entre 1 p.u. en frío y 1.3 p.u. a temperatura nominal (cobre). Afecta principalmente al estimador de flujo por voltaje (error \( \propto \Delta R \cdot i \)).
- \( L \) varía con la saturación magnética hasta ±20% en máquinas. Afecta al cálculo del deslizamiento y al desacoplo cruzado del lazo de corriente.

## 6 — Diseño iterativo: VOC para convertidor de red 1 MVA

**Datos de partida:**
- Potencia nominal: \( S_n = 1\,\text{MVA} \), \( V_{LL} = 400\,\text{V} \), \( I_n = 1443\,\text{A} \)
- Inductancia de filtro: \( L = 2\,\text{mH} \), resistencia: \( R = 50\,\text{m}\Omega \)
- Periodo de muestreo/conmutación: \( T_s = 100\,\mu\text{s} \)
- Objetivo de margen de fase: \( PM \geq 45° \)
- SCR mínimo esperado: \( SCR_{min} = 3 \)

**Iteración 1: ancho de banda sin restricciones.** La constante de tiempo de la planta es \( \tau = L/R = 40\,\text{ms} \). Con cancelación de polo se elige \( \alpha_c \) libremente. Objetivo agresivo: \( \alpha_c = 2\pi \cdot 2000\,\text{Hz} \Rightarrow K_p = L\alpha_c = 25.1\,\Omega \), \( K_i = R\alpha_c = 628\,\text{s}^{-1} \). El retardo \( 1.5\,T_s = 150\,\mu\text{s} \) produce a esta frecuencia una pérdida de fase de \( 1.5\,T_s\,\alpha_c = 1.88\,\text{rad} = 108° \): el sistema es inestable.

**Iteración 2: reducir \( \alpha_c \) por el retardo.** Para garantizar \( PM = 45° \) con el retardo:

$$ \alpha_c < \frac{\pi/4}{1.5\,T_s} = \frac{0.785}{150\,\mu\text{s}} = 5236\,\text{rad/s} $$

Se elige \( \alpha_c = 2\pi \cdot 750\,\text{Hz} = 4712\,\text{rad/s} \) (margen adicional). Entonces:

$$ K_p = L\,\alpha_c = 2\cdot10^{-3} \cdot 4712 = 9.42\,\Omega $$
$$ K_i = R\,\alpha_c = 0.05 \cdot 4712 = 235.6\,\text{s}^{-1} $$

La pérdida de fase por retardo a \( \omega_c = \alpha_c \): \( \phi_{delay} = 1.5\,T_s\,\alpha_c = 0.707\,\text{rad} = 40.5° \). El PI en la frecuencia de cruce aporta fase adicional positiva (cero del PI por debajo de \( \alpha_c \)), resultando \( PM \approx 50° \). Verificado por la figura.

**Iteración 3: añadir desacoplo y feedforward.** Sin desacoplo \( \omega L \), el término cruzado actúa como perturbación sobre el eje opuesto con ganancia \( \omega_0 L = 2\pi \cdot 50 \cdot 2\cdot10^{-3} = 0.628\,\Omega \). A corriente nominal (\( I_n = 1443\,\text{A} \)) esto equivale a \( 0.628 \times 1443 \approx 906\,\text{V} \) de perturbación: enorme. El desacoplo explícito cancela este término. El feedforward de tensión de red cancela la perturbación de la fuente de tensión.

**Iteración 4: verificar con SCR mínimo.** Con \( SCR = 3 \): \( X_{th} = V_{PCC}^2/(SCR \cdot S_n) \). La inductancia de red efectiva se suma a \( L \): \( L_{eff} = L + L_{th} \). Con \( K_p = L\,\alpha_c \) calculado para \( L \) solo, el exceso de inductancia desplaza el cero de la planta y reduce el margen de fase. Para \( SCR = 3 \) la reducción típica es \( \sim 5° \): el margen queda en \( \sim 45° \), justo en el límite. Para \( SCR < 2 \) hay que reducir \( \alpha_c \) o añadir amortiguamiento virtual.

<div class="cfig"><img src="figuras/control-vectorial-analisis.png" alt="control vectorial: orientacion, respuesta vectorial, error PLL, Bode VOC"><div class="cap">(a) Orientación del vector de tensión de red en el eje d del marco dq: \(v_d=V\), \(v_q=0\). (b) Escalón de par \(i_q^*\): con desacoplo correcto \(i_d\) permanece constante —el flujo no se ve perturbado. (c) Error de PLL de 10° introduce acoplamiento residual \(i_d\neq0\) aunque \(i_d^*=0\). (d) Bode del lazo de corriente VOC con cancelación de polo y retardo \(1.5\,T_s\): fc≈750 Hz, PM≈50°.</div></div>

## Cuándo y por qué se usa
En accionamientos de máquinas AC (PMSM, inducción) y en convertidores conectados a red. Permite
control independiente y de alto desempeño de par/flujo o de P/Q.

## Procedimiento (genérico)
1. Determina el ángulo de orientación \( \theta \) (estimador de flujo en FOC; PLL en red).
2. Mide corrientes y transfórmalas a dq con \( \theta \) (Clarke + Park).
3. Cierra lazos PI sobre \( i_d, i_q \) con **desacoplo** \( \pm\omega L \) y feedforward.
4. Antitransforma la tensión de referencia (dq→abc) y genera el PWM.
5. Sintoniza los PI por ancho de banda (ver [[control-cascada]], [[sintonia-pi-pid]]).

## Ejemplo de código
```python
# lazo de corriente vectorial (dq) con desacoplo
e_d, e_q = id_ref - id, iq_ref - iq
vd = Kp*e_d + Ki*xd - w*L*iq     # desacoplo cruzado
vq = Kp*e_q + Ki*xq + w*L*id
```

## Parámetros y valores típicos
Ancho de banda del lazo de corriente ≈ \( f_{sw}/10 \). En FOC, \( i_d=0 \) (PMSM de imanes
superficiales) para par máximo por amperio; debilitamiento de campo con \( i_d<0 \) a alta velocidad.
En VOC: \( K_p = L\alpha_c \), \( K_i = R\alpha_c \), \( \alpha_c \leq PM/(1.5\,T_s) \).

## Errores comunes
- Orientación incorrecta (error en \( \theta \)) → acoplamiento par/flujo o P/Q.
- Olvidar el desacoplo \( \pm\omega L \) → lazos d y q acoplados, peor desempeño.
- Sobredimensionar \( \alpha_c \) sin considerar el retardo digital → inestabilidad.
- En red débil: PLL inestable → VOC pierde su orientación → protecciones disparan.

## Uso en proyectos
- **01/02**: los lazos de corriente dq con desacoplo son control vectorial aplicado a un
  convertidor de red (orientación a la tensión por la PLL en el GFL). El FOC de máquina es
  candidato a proyecto propio.

## Conceptos relacionados
- [[marco-dq]] · [[control-cascada]] · [[potencia-instantanea-dq]] · [[pll-srf]] · [[desacoplo-dq]]

## Referencias
- Kazmierkowski et al., *Control in Power Electronics*, 2002.
- Vas, *Sensorless Vector and Direct Torque Control*, 1998.
- Blaabjerg et al., *Overview of Control and Grid Synchronization*, IEEE TIE 2006.
