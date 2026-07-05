---
titulo: Ecuación de oscilación (swing equation)
slug: ecuacion-oscilacion
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: []
objetivos: [describir la dinámica ángulo-frecuencia de una fuente síncrona]
tags: [swing, inercia, angulo, frecuencia, par-sincronizante, intermedio, modelado, vsm, area-igual]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-02
relacionados: [vsm-inercia, droop-control, grid-forming-vs-following, potencia-ac-fasores, red-thevenin-scr]
referencias:
  - "Kundur, Power System Stability and Control, McGraw-Hill 1994"
  - "Machowski, Bialek, Bumby, Power System Dynamics, Wiley 2008"
---

## Definición
Ecuación que relaciona el **desbalance de potencia** de una máquina (o convertidor) síncrono con la
aceleración de su **ángulo y frecuencia**. Es el modelo electromecánico básico que gobierna la
estabilidad transitoria y la respuesta de frecuencia, y la base de la [[vsm-inercia|inercia
virtual]] y del [[droop-control|droop]].

## Fundamento teórico
En por unidad, con **constante de inercia** \( H \) (energía cinética almacenada / potencia base,
en s):
$$ \frac{2H}{\omega_0}\frac{d^2\delta}{dt^2}=P_m-P_e-D\,\frac{\Delta\omega}{\omega_0} $$
o en forma de estado con \( \Delta\omega=\dot\delta \):
$$ 2H\,\frac{d\Delta\omega}{dt}=P_m-P_e-D\,\Delta\omega,\qquad \frac{d\delta}{dt}=\omega_0\,\Delta\omega $$
- \( P_m \): potencia mecánica/de entrada; \( P_e \): potencia eléctrica entregada; \( D \):
  amortiguamiento.
- Para una fuente tras una reactancia \( X \) hacia una red \( V_g\angle 0 \):
  \( P_e=\dfrac{E V_g}{X}\sin\delta \).

**Linealizando** en \( \delta_0 \) aparece el modo electromecánico:
$$ 2H\,\Delta\ddot\delta + D\,\Delta\dot\delta + \omega_0 K_s\,\Delta\delta=0,\quad
   K_s=\frac{\partial P_e}{\partial\delta}=\frac{E V_g}{X}\cos\delta_0 $$
$$ \omega_{n}=\sqrt{\frac{\omega_0 K_s}{2H}},\qquad \zeta=\frac{D}{2}\sqrt{\frac{\omega_0}{2H K_s}} $$
\( K_s \) es el **par/potencia sincronizante**: si \( K_s<0 \) (p.ej. \( \delta_0>90^\circ \)) se
pierde el sincronismo. Menos inercia \( H \) → oscilaciones más rápidas; red débil (\( X \) grande,
bajo [[red-thevenin-scr|SCR]]) → \( K_s \) pequeño → modo lento y poco amortiguado.

<div class="cfig"><img src="figuras/ecuacion-oscilacion-swing.png" alt="oscilacion del angulo tras un escalon de potencia"><div class="cap">Tras un escalón de potencia, el ángulo δ oscila a la frecuencia del modo electromecánico √(ω0·Ks/2H) y se asienta en el nuevo equilibrio; menos inercia o amortiguamiento → más oscilatorio.</div></div>

## 1 — La swing equation \( 2H\,\dot{\Delta\omega}=P_m-P_e \) desde el par y la energía cinética

**Paso 1 — segunda ley de Newton en rotación.** El rotor de momento de inercia \( J \) acelera según el par neto: el par mecánico de entrada \( T_m \) menos el electromagnético de salida \( T_e \):

$$ J\,\frac{d\omega_m}{dt}=T_m-T_e $$

con \( \omega_m \) la velocidad mecánica del rotor en rad/s.

**Paso 2 — definir la constante de inercia \( H \).** \( H \) normaliza la energía cinética almacenada a velocidad nominal frente a la potencia base \( S_B \) (unidades: segundos):

$$ H=\frac{\tfrac12 J\,\omega_{m0}^2}{S_B}\;\Longrightarrow\;J=\frac{2H\,S_B}{\omega_{m0}^2} $$

\( H \) es "cuántos segundos puede la máquina entregar potencia nominal solo con su energía cinética".

**Paso 3 — pasar a por unidad.** Sustituyendo \( J \) en la ley de Newton y multiplicando por \( \omega_{m0} \) para convertir par en potencia (\( P=T\omega \)):

$$ \frac{2H\,S_B}{\omega_{m0}^2}\,\frac{d\omega_m}{dt}=T_m-T_e $$

$$ \frac{2H\,S_B}{\omega_{m0}}\,\frac{d(\omega_m/\omega_{m0})}{dt}=T_m-T_e $$

Multiplicando ambos lados por \( \omega_{m0}/S_B \): el lado derecho se vuelve \( (T_m-T_e)\,\omega_{m0}/S_B\approx (P_m-P_e)/S_B \) (cerca del nominal \( \omega_m\approx\omega_{m0} \), par×velocidad ≈ potencia), es decir potencias en p.u.; y con la velocidad en p.u. \( \omega=\omega_m/\omega_{m0} \), \( \Delta\omega=\omega-1 \):

$$ \boxed{\;2H\,\frac{d\Delta\omega}{dt}=P_m-P_e\;} $$

**Paso 4 — añadir amortiguamiento y la relación ángulo-frecuencia.** Las cargas dependientes de la velocidad y los devanados amortiguadores aportan un par \( \propto\Delta\omega \); se añade \( -D\,\Delta\omega \). El ángulo del rotor \( \delta \) es la integral de la desviación de frecuencia respecto a la red (\( \dot\delta=\omega_0\Delta\omega \), con \( \omega_0 \) en rad eléctricos/s):

$$ 2H\,\frac{d\Delta\omega}{dt}=P_m-P_e-D\,\Delta\omega,\qquad \frac{d\delta}{dt}=\omega_0\,\Delta\omega $$

Sustituyendo \( P_e=\dfrac{EV}{X}\sin\delta \) ([[potencia-ac-fasores]]) se cierra el modelo electromecánico de 2 estados. Esta es exactamente la ecuación que el [[vsm-inercia|VSM]] integra en software para que un convertidor exhiba inercia.

## 2 — Derivación desde Newton: \( J\alpha = T_{mec} - T_{elec} - T_{amort} \)

La swing equation es simplemente la Segunda Ley de Newton aplicada al rotor. La derivación completa muestra cada término físico:

**El par mecánico \( T_m \).** Lo aporta la turbina (vapor, gas, hidro, viento). En estado estacionario iguala exactamente el par eléctrico. Ante un disturbio cambia lentamente (gobernador de velocidad, constante de tiempo de 0,5–5 s en turbinas de vapor).

**El par electromagnético \( T_e \).** Lo genera la interacción entre el flujo del rotor y las corrientes del estátor. En el modelo clásico de 2 estados:

$$ T_e \approx \frac{P_e}{\omega_0} = \frac{E\,V_g}{\omega_0\,X}\sin\delta $$

Esta dependencia sinusoidal del ángulo \( \delta \) es lo que hace no lineal el sistema y limita la región de estabilidad.

**El par amortiguador \( T_D \).** Dos mecanismos físicos: (a) las **corrientes de Foucault** en los devanados amortiguadores del rotor que disipan energía en transitorios, y (b) la **carga dependiente de frecuencia** que absorbe más potencia cuando \( \omega>\omega_0 \). Ambos se modelan como \( T_D=D\,\Delta\omega \) con \( D \) la constante de amortiguamiento.

**La ecuación completa en par físico:**

$$ J\,\dot\omega_m = T_m - T_e - D_J\,(\omega_m-\omega_{m0}) $$

**Paso — normalizar a potencia en pu.** Multiplicando por \( \omega_{m0}/S_B \) y usando \( P=T\omega\approx T\omega_0 \) cerca del nominal:

$$ \frac{J\,\omega_{m0}}{S_B}\,\frac{d\Delta\omega_m}{dt} = P_m - P_e - D\,\Delta\omega $$

Y con \( J\omega_{m0}^2/S_B = 2H \):

$$ \boxed{\;2H\,\frac{d\Delta\omega}{dt} = P_m - P_e - D\,\Delta\omega\;} $$

La constante de inercia \( H \) concentra en un solo número (segundos) toda la información del rotor: más \( J \) (rotor pesado), más \( \omega_{m0} \) (alta velocidad de giro) o menos \( S_B \) (máquina pequeña) → más \( H \).

## 3 — El factor de amortiguamiento y los modos electromecánicos

**Linealización alrededor de \( \delta_0 \).** Sea \( \Delta\delta=\delta-\delta_0 \) una perturbación pequeña. Expandiendo \( P_e=P_{max}\sin\delta \) en Taylor:

$$ P_e \approx P_{max}\sin\delta_0 + P_{max}\cos\delta_0\,\Delta\delta = P_{m,0} + K_s\,\Delta\delta $$

con el **par sincronizante** \( K_s = P_{max}\cos\delta_0 = (EV_g/X)\cos\delta_0 \).

Sustituyendo en la swing equation linealizada:

$$ 2H\,\Delta\ddot\omega + D\,\Delta\dot\omega + \omega_0 K_s\,\Delta\delta = 0 $$

Esta es la ecuación de un oscilador de segundo orden. Comparándola con \( \ddot x+2\zeta\omega_n\dot x+\omega_n^2 x=0 \):

$$ \boxed{\;\omega_n = \sqrt{\frac{\omega_0\,K_s}{2H}}\;},\qquad \boxed{\;\zeta = \frac{D}{2}\sqrt{\frac{\omega_0}{2H\,K_s}} = \frac{D\,\omega_0}{4H\,\omega_n}\;} $$

**Interpretación física de \( K_s \):**
- \( K_s>0 \): equilibrio estable (el ángulo perturbado genera una fuerza restauradora).
- \( K_s=0 \): \( \delta_0=90° \), el modo se hace no oscilatorio (neutro).
- \( K_s<0 \): \( \delta_0>90° \), el equilibrio es inestable → pérdida de sincronismo.

**Efecto de la inercia sobre el modo.** Menos \( H \) → \( \omega_n \) mayor (modo más rápido) pero también \( \zeta \) menor (peor amortiguado, ya que \( \zeta\propto D/(H\,\omega_n)\propto D/\sqrt{H} \)). El compromiso: \( H \) grande da oscilaciones lentas y bien amortiguadas pero exige más energía almacenada.

**Efecto de la red.** En red débil (alto \( X_{th} \), bajo [[red-thevenin-scr|SCR]]), la reactancia equivalente \( X=X_s+X_{th} \) crece, \( K_s=EV_g/X\cdot\cos\delta_0 \) cae → modo lento y poco amortiguado. Por eso la inercia es especialmente crítica en redes débiles o islas.

## 4 — El análisis de estabilidad de área igual

El criterio de área igual (Equal Area Criterion, EAC) permite determinar gráficamente si el sistema sobrevive un transitorio grande sin linealización:

**Energía en el espacio de fase.** La swing equation puede reescribirse como una ecuación de conservación de energía. Definiendo la función de Lyapunov:

$$ W(\delta,\Delta\omega) = H\,\Delta\omega^2 - \int_{\delta_0}^{\delta}(P_m-P_e)\,d\delta' $$

Para el sistema sin amortiguamiento (\( D=0 \)), \( W \) se conserva. El sistema es estable si, tras el disturbio, \( W \) no supera el valor en el punto de equilibrio inestable (UEP):

$$ W_{crit} = W(\delta_u, 0) = -\int_{\delta_0}^{\delta_u}(P_m-P_e)\,d\delta $$

**La interpretación gráfica.** En la curva \( P(\delta) \), el criterio se visualiza como áreas:
- **Área de aceleración** (\( A_{acc} \)): la zona entre \( P_m \) y \( P_e(\delta) \) donde \( P_m>P_e \) — el rotor gana velocidad.
- **Área de deceleración** (\( A_{dec} \)): la zona donde \( P_m<P_e \) — el rotor pierde velocidad.

Para que el sistema vuelva al equilibrio, el rotor debe poder frenar antes de llegar al UEP. La condición es:

$$ A_{dec,\max} \geq A_{acc} $$

El **margen de estabilidad transitoria** es \( A_{dec,\max} - A_{acc} \). Aumentar \( H \) no cambia directamente las áreas, pero sí la velocidad con que el rotor recorre la curva, lo que afecta al amortiguamiento real (con \( D>0 \)) y por tanto al margen efectivo.

**Aplicación: falta trifásica seguida de despeje.** Sea una falta en \( t=0 \) que elimina \( P_e \) (cortocircuito cerca de la máquina). El rotor acelera desde \( \delta_0 \) hasta \( \delta_{cl} \) (ángulo al despejar la falta). El área de aceleración es:

$$ A_{acc} = P_m\,(\delta_{cl}-\delta_0) $$

Para sobrevivir el transitorio se necesita \( \delta_{cl} < \delta_{cr} \), el **ángulo crítico de despeje** tal que \( A_{dec,max}=A_{acc} \). El tiempo máximo de despeje (**CCT**, Critical Clearing Time) es el tiempo en que el relé debe actuar antes de que el ángulo supere \( \delta_{cr} \).

## 5 — La VSM y la inercia sintética: \( J \) virtual ajustable

El [[vsm-inercia|VSM (Virtual Synchronous Machine)]] implementa la swing equation en software dentro del control de un inversor. Al integrar numéricamente:

$$ 2H_{virt}\,\frac{d\Delta\omega}{dt} = P_m^* - P_e - D\,\Delta\omega $$

el convertidor se comporta externamente como una máquina síncrona con constante de inercia \( H_{virt} \), aunque físicamente solo tenga el pequeño condensador de su bus DC.

**Ventajas respecto a la máquina real:**

1. **\( H \) ajustable en tiempo real.** En una máquina real \( H \) lo fija el rotor (no cambia). En el VSM, \( H_{virt} \) puede variarse de 0 a \( H_{max} \) instantáneamente, adaptando la respuesta a la condición de red.

2. **\( H_{virt} \) mayor que el físico.** La inercia real del convertidor es \( H_{fis}=\frac{1}{2}C_{dc}V_{dc}^2/S_n \), típicamente 5–20 ms. El VSM puede emular \( H_{virt}=4\,\text{s} \) o más, tomando prestada energía del bus DC (que se descarga ligeramente). El límite real es la variación de tensión admisible en el bus DC:

$$ \Delta V_{dc,max} = V_{dc,0}\,\sqrt{1 - \frac{2P_{max}\,t_{soporte}}{C_{dc}\,V_{dc,0}^2}} $$

3. **Combinable con almacenamiento.** Si hay baterías en el bus DC, la inercia efectiva es casi ilimitada durante el tiempo que dure la batería.

**La inercia sintética en la red.** El beneficio sistémico de los VSM es que estabilizan la RoCoF (Rate of Change of Frequency) ante perturbaciones, igual que las máquinas convencionales. A medida que las centrales térmicas (alta \( H \)) se sustituyen por renovables sin inercia, el VSM es el mecanismo para mantener la robustez dinámica de la red.

## 6 — Diseño iterativo: emular H = 4 s con un inversor de 1 MVA

**Datos del sistema:**
- Potencia del inversor: \( S_n = 1\,\text{MVA} \)
- Inercia a emular: \( H_{virt} = 4\,\text{s} \)
- Bus DC nominal: \( V_{dc} = 800\,\text{V} \)
- Variación máxima admisible del bus DC durante soporte: \( \pm 5\,\%\ (40\,\text{V}) \)
- Red: \( X = 0{,}2\,\text{pu} \), \( E = 1{,}05\,\text{pu} \), \( V_g = 1{,}0\,\text{pu} \), punto de operación \( P_0 = 0{,}8\,\text{pu} \)

**Paso 1 — momento de inercia virtual equivalente.**
Despejando \( J_{virt} \) de la definición de \( H \):

$$ J_{virt} = \frac{2H_{virt}\,S_n}{\omega_{m0}^2} = \frac{2\times4\times10^6}{(2\pi\times50)^2} = \frac{8\times10^6}{9{,}87\times10^4} \approx 81\,\text{kg·m}^2 $$

Este \( J_{virt} \) se programa como parámetro en el integrador del VSM. Físicamente, una turbina de vapor de 1 MVA tiene \( J\approx 2\text{–}5\,\text{kg·m}^2 \): el VSM emula 16–40 veces más inercia que el rotor real equivalente.

**Paso 2 — condensador de bus DC para el soporte.**
La energía que el bus DC debe ceder durante el soporte de frecuencia es:

$$ \Delta E_{DC} = H_{virt}\,S_n\,\Delta t_{soporte} \approx 4\times10^6\times1 = 4\,\text{MJ/s}\times\Delta t $$

El condensador almacena \( E_{DC}=\tfrac{1}{2}C_{dc}V_{dc}^2 \). Para \( \Delta V_{dc}=40\,\text{V} \) durante \( \Delta t = 0{,}5\,\text{s} \) de soporte máximo:

$$ C_{dc} \geq \frac{2\,P_{soporte}\,\Delta t}{V_{dc,0}^2 - V_{dc,min}^2} \approx \frac{2\times0{,}3\times10^6\times0{,}5}{800^2-760^2} \approx 9{,}7\,\text{F} $$

Esto es impracticable con condensadores convencionales. La solución real: (a) batería en el bus DC (kWh en segundos), (b) reducir \( \Delta t_{soporte} \) a 100–200 ms (tiempo de respuesta del gobernador), (c) reducir la potencia de soporte a un 20–30 % de \( S_n \). Con \( C_{dc}=100\,\text{mF} \) y soporte durante 100 ms a 300 kW, la caída de \( V_{dc} \) es:

$$ \Delta V_{dc} = \frac{P_{soporte}\,\Delta t}{C_{dc}\,V_{dc,0}} = \frac{300\times10^3\times0{,}1}{0{,}1\times800} = 37{,}5\,\text{V} \approx 4{,}7\,\% \quad \checkmark $$

**Paso 3 — parámetros del modo electromecánico.**
Punto de equilibrio: \( \delta_0 = \arcsin(P_0\,X/(E\,V_g)) = \arcsin(0{,}8\times0{,}2/1{,}05) \approx 8{,}8° \).

Par sincronizante: \( K_s = (EV_g/X)\cos\delta_0 = (1{,}05/0{,}2)\cos8{,}8° \approx 5{,}19\,\text{pu} \).

Frecuencia del modo: \( \omega_n = \sqrt{\omega_0 K_s/(2H)} = \sqrt{314\times5{,}19/8} \approx 14{,}3\,\text{rad/s} \approx 2{,}3\,\text{Hz} \).

Amortiguamiento con \( D=10 \): \( \zeta = D\omega_0/(4H\omega_n) = 10\times314/(4\times4\times14{,}3) \approx 0{,}14 \).

Para llegar a \( \zeta=0{,}5 \) con el mismo \( H \): \( D = 4H\omega_n\times0{,}5/\omega_0 = 4\times4\times14{,}3\times0{,}5/314 \approx 0{,}36 \) — droop de frecuencia del 3{,}6 %.

<div class="cfig"><img src="figuras/ecuacion-oscilacion-analisis.png" alt="curva P(delta), mapa de fase y respuesta de frecuencia"><div class="cap">Cuatro paneles: (a) curva P(δ) con el punto de equilibrio estable (SEP), el inestable (UEP) y las áreas de aceleración/deceleración del criterio de área igual; (b) mapa de fase δ-Δω con la separatriz que delimita la cuenca de atracción; (c) f(t) ante un escalón de carga del 20% para H=2, 4 y 8 s — más inercia reduce el RoCoF y la caída máxima; (d) comparativa máquina síncrona vs VSM con H emulado igual y H virtual doble.</div></div>

## Cuándo y por qué se usa
Para analizar estabilidad de frecuencia/ángulo, dimensionar inercia y droop, y entender por qué los
convertidores grid-forming (VSM) emulan esta ecuación. Conecta el lazo de potencia con la dinámica
de red.

## Ejemplo de código
```python
import numpy as np
def swing(t, x, Pm, E, Vg, X, H, D, w0):
    delta, dw = x
    Pe = E*Vg/X*np.sin(delta)
    return [w0*dw, (Pm - Pe - D*dw)/(2*H)]
```

## Parámetros y valores típicos
Generadores: \( H\approx 2\text{–}9 \) s. VSM: \( H \) emulada 1–6 s. Modo electromecánico
0.1–2 Hz. \( \delta_0 \) de diseño \( <30\text{–}45° \). Amortiguamiento típico \( \zeta=0{,}1\text{–}0{,}3 \); objetivo \( >0{,}1 \) para no oscilar indefinidamente.

## Errores comunes
- Operar con \( \delta_0 \) cercano a 90° (poco par sincronizante, riesgo de pérdida de sincronismo).
- Despreciar \( D \): sin amortiguamiento el modo oscila indefinidamente.
- Usar el modelo lineal para transitorios grandes (la no linealidad \( \sin\delta \) domina).
- Confundir \( H \) con \( J \): \( H \) depende de \( S_B \) y es por unidad, \( J \) es el momento físico en kg·m².
- En VSM: dimensionar \( C_{dc} \) solo para el rizado de PWM y no para el soporte de inercia → la tensión del bus colapsa en el primer transitorio.

## Conceptos relacionados
- [[vsm-inercia]] · [[droop-control]] · [[grid-forming-vs-following]] · [[red-thevenin-scr]] · [[potencia-ac-fasores]] · [[generador-sincrono]]

## Referencias
- Kundur, *Power System Stability and Control*, 1994.
- Machowski, Bialek, Bumby, *Power System Dynamics*, 2008.
