---
titulo: Generador síncrono — modelo dq y dinámica
slug: generador-sincrono
categoria: fisica-modelado
tipo: concepto
nivel: avanzado
proyectos: []
objetivos: [modelar la dinámica electromagnética y mecánica del generador síncrono]
tags: [generador-sincrono, dq-park, swing, amortiguador, AVR, avanzado, modelado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-02
relacionados: [ecuacion-oscilacion, vsm-inercia, marco-dq, representacion-espacio-estados, clasificacion-estabilidad]
referencias:
  - "Kundur, Power System Stability and Control, McGraw-Hill 1994"
  - "Anderson, Fouad, Power System Control and Stability, IEEE Press 2003"
---

## Definición
Modelo matemático del generador síncrono en el marco **dq de Park** (referencial del rotor), que
desacopla las dinámicas de circuito electromagnético y mecánico y es la base de todos los estudios
de estabilidad de sistemas de potencia y de la emulación virtual (VSM).

## Fundamento teórico
**Circuito electromagnético.** En el eje d (flujo del rotor) y q (en cuadratura), con devanados
de campo \( f \) y amortiguadores \( D \) (eje d) y \( Q \) (eje q):
$$ \psi_d = -L_d i_d + L_{md}(i_f+i_D),\quad \psi_q=-L_q i_q+L_{mq}i_Q $$
Las tensiones de estátor (con velocidad del rotor \( \omega_r \)):
$$ v_d = -R_s i_d + \dot\psi_d - \omega_r\psi_q,\quad v_q=-R_s i_q+\dot\psi_q+\omega_r\psi_d $$
Esto es el **modelo de orden completo** (5–6 estados eléctricos). Se simplifican:
- **Modelo de 4º orden** (subtransitorio): \( \psi_d,\psi_q,\psi_D,\psi_Q \) como estados; \( E'_d,E'_q \) tensiones transitorias.
- **Modelo clásico** (2 estados: \( \delta,\omega \)): solo la [[ecuacion-oscilacion|swing equation]] con \( E' \) constante; suficiente para estabilidad transitoria.

**Mecánica** ([[ecuacion-oscilacion]]):
$$ 2H\frac{d\omega}{dt}=T_m-T_e-D\Delta\omega,\quad \frac{d\delta}{dt}=\omega_0\Delta\omega $$
Par electromagnético: \( T_e=\psi_d i_q - \psi_q i_d \).

**Regulación**: AVR (Automatic Voltage Regulator) cierra el lazo \( V_{terminal}\to E_f \) (campo);
el governor cierra \( \omega\to T_m \). Su dinámica (tiempo \( \sim100\,\)ms–s) es la base de los
[[servicios-red-soporte|servicios de soporte de frecuencia/tensión]].

**Relevancia para convertidores.** El VSM ([[vsm-inercia]]) emula exactamente este modelo pero
sobre un convertidor; entender el original clarifica qué se emula, sus límites y las aproximaciones.

<div class="cfig"><img src="figuras/generador-sincrono-pdelta.png" alt="curva potencia-angulo del generador sincrono"><div class="cap">La potencia transferida sigue $P=\frac{EV}{X}\sin\delta$. La pendiente en el punto de operación es el par sincronizante $K_s=\partial P/\partial\delta$, que mantiene la máquina en paso; el máximo de transferencia está en $\delta=90°$, y más allá el par sincronizante se vuelve negativo y se pierde el sincronismo. El VSM emula exactamente esta dinámica sobre un convertidor.</div></div>

## 1 — De dónde sale \( P=\dfrac{E V}{X_s}\sin\delta \)
**Paso 1 — el circuito.** Tras la reactancia síncrona \( X_s \), el generador es una FEM interna \( E\angle\delta \) conectada a la red \( V\angle 0 \). Se desprecia la resistencia de estátor frente a \( X_s \). La corriente que circula es:

$$ \bar I=\frac{\bar E-\bar V}{jX_s}=\frac{E\angle\delta-V\angle 0}{jX_s} $$

**Paso 2 — potencia compleja entregada a la red.** En el nudo de red, \( S=P+jQ=\bar V\,\bar I^\* \). Con \( \bar V=V\angle 0 \) (real):

$$ S=V\left(\frac{E\angle\delta-V}{jX_s}\right)^{\!\*}=V\cdot\frac{E\angle(-\delta)-V}{-jX_s}=\frac{V\,E\angle(-\delta)-V^2}{-jX_s} $$

(conjugar invierte el signo del ángulo y de la \( j \)).

**Paso 3 — separar partes real e imaginaria.** Usando \( E\angle(-\delta)=E\cos\delta-jE\sin\delta \) y \( 1/(-j)=j \):

$$ S=j\,\frac{V E\cos\delta-jV E\sin\delta-V^2}{X_s}=\frac{V E\sin\delta}{X_s}+j\,\frac{V E\cos\delta-V^2}{X_s} $$

(el término \( -j\cdot jVE\sin\delta=+VE\sin\delta \) pasa a la parte real). Identificando \( P=\mathrm{Re}\,S \) y \( Q=\mathrm{Im}\,S \):

$$ \boxed{\;P=\frac{E V}{X_s}\sin\delta\;}\qquad Q=\frac{E V\cos\delta-V^2}{X_s} $$

**Paso 4 — lectura física.** \( P \) es máxima en \( \delta=90^\circ \) (límite de estabilidad estática). La pendiente \( K_s=\partial P/\partial\delta=(EV/X_s)\cos\delta_0 \) es el **par sincronizante** que mantiene la máquina en paso; se anula en \( 90^\circ \) y se vuelve negativo más allá, perdiéndose el sincronismo. Esta \( P(\delta) \) es la que entra como \( P_e \) en la [[ecuacion-oscilacion|swing equation]] y la que el VSM ([[vsm-inercia]]) reproduce sobre un convertidor.

## 2 — El modelo dq de la máquina síncrona: las ecuaciones de Park

**Los estados del modelo de 5º orden.** El modelo estándar de Park incluye los devanados de campo, amortiguadores y estátor:

$$  \mathbf{x}=\bigl[i_d,\; i_q,\; \psi_{fd},\; \psi_{1d},\; \psi_{1q},\; \omega_r,\; \delta\bigr]^T $$

**Las tensiones de estátor en dq** (con el marco dq fijado al rotor, \( \omega=\omega_r \)):

$$  v_d = -R_s\,i_d + \omega_r\,\psi_q + \frac{d\psi_d}{dt} $$
$$  v_q = -R_s\,i_q - \omega_r\,\psi_d + \frac{d\psi_q}{dt} $$

El término \( \omega_r\psi_q \) (en la ecuación d) y \( -\omega_r\psi_d \) (en la ecuación q) son las **tensiones de rotación**: acoplan las dos ecuaciones y son los responsables de la acción de generación a frecuencia \( \omega_r \).

**Los flujos.** En la máquina cilíndrica (\( L_d=L_q=L_s \)) se simplifica, pero en la máquina de polo saliente (\( L_d\ne L_q \)):

$$  \psi_d = -L_d\,i_d + L_{md}\,i_{fd}, \qquad \psi_q = -L_q\,i_q $$

donde \( i_{fd} \) es la corriente de excitación (referida al estátor). El primer término es la reacción de armadura; el segundo es la FEM debida al campo.

**El par electromagnético** (en pu, con potencia de base \( S_n \) y velocidad de base \( \omega_0 \)):

$$  \boxed{T_e = \psi_d\,i_q - \psi_q\,i_d = L_{md}\,i_{fd}\,i_q - (L_d-L_q)\,i_d\,i_q} $$

El primer término es el par de alineación (como en la máquina cilíndrica); el segundo es el par de reluctancia (solo existe si \( L_d\ne L_q \)).

**La reducción a modelo clásico.** Despreciando las dinámicas del devanado (rápidas respecto a la mecánica) y tomando \( E'=L_{md}\,i_{fd}=\text{cte} \), se obtiene el modelo de 2 estados (\( \delta,\omega_r \)) con:
\( P_e=(E'\cdot V/X'_d)\sin\delta \), que es la curva potencia-ángulo transitoria. Es suficiente para estudios de estabilidad transitoria de primer oscilo.

## 3 — La ecuación de swing y la inercia

**La ecuación de swing.** La dinámica mecánica del rotor es el balance entre par motor y par eléctrico, con amortiguamiento \( D \):

$$  \boxed{\;2H\frac{d\omega_r}{dt}=T_m - T_e - D(\omega_r-\omega_0)\;}, \qquad \frac{d\delta}{dt}=\omega_0(\omega_r-\omega_0) $$

donde \( H \) es la constante de inercia en segundos, \( \omega_0=2\pi f_0 \) la velocidad de sincronismo.

**La constante de inercia H.** Se define como la energía cinética almacenada en el rotor a velocidad nominal, normalizada a la potencia nominal:

$$  H = \frac{\tfrac12 J\omega_0^2}{S_n} \quad[\text{segundos}] $$

Valores típicos: \( H=2\text{–}4\,\text{s} \) (turbinas de gas, velocidad rápida), \( H=4\text{–}6\,\text{s} \) (turbinas de vapor), \( H=6\text{–}10\,\text{s} \) (turbinas hidráulicas, rotor muy masivo). \( H \) es una propiedad física del rotor: no se puede ajustar sin cambiar la masa o la velocidad nominal.

**El RoCoF ante un desequilibrio de potencia.** Inmediatamente tras un escalón de carga \( \Delta P \):

$$  \frac{d\omega_r}{dt}\bigg|_{t=0^+} = \frac{T_m-T_e}{2H/\omega_0} \approx -\frac{\Delta P\,\omega_0}{2H\,S_n} $$

Para \( \Delta P=100\,\text{MW} \), \( S_n=1000\,\text{MVA} \), \( H=5\,\text{s} \): \( d\omega/dt=-(0.1\times314)/(10)=-3.14\,\text{rad/s}^2 \), equivalente a \( df/dt=-0.5\,\text{Hz/s} \). Este RoCoF determina si la protección de subfrecuencia actúa antes de que la respuesta primaria lo estabilice.

**Por qué H de una máquina real no es ajustable.** \( J \) es la inercia del rotor (masa física) y \( \omega_0 \) es fija por la frecuencia de red. Para cambiar \( H \) habría que cambiar el material del rotor o la velocidad nominal, lo que no es viable en operación. El VSM ([[vsm-inercia]]) supera esta limitación: \( H_{VSM} \) es un parámetro de software, ajustable en tiempo real.

## 4 — La regulación de tensión: el AVR y el PSS

**El AVR (Automatic Voltage Regulator).** Mantiene la tensión terminal \( |V_t| \) en su valor nominal ajustando la corriente de excitación \( i_{fd} \). El lazo del AVR:

$$  V_{fd}=K_{AVR}(|V_t^*|-|V_t|)+\text{PSS output} $$

El excitador aplica \( V_{fd} \) al devanado de campo, cambiando \( i_{fd} \) con la constante de tiempo del campo \( T'_{d0}=L_{fd}/R_{fd}\approx3\text{–}10\,\text{s} \). Esto modifica el flujo \( \psi_d \) y con él la tensión terminal \( V_q \approx \omega_r\psi_d \approx E'_q \).

**La respuesta lenta del AVR.** La constante de tiempo del campo (\( T'_{d0} \)) es de varios segundos: el AVR no puede responder rápidamente. Por eso el VSC, que puede cambiar su tensión de salida en milisegundos, proporciona un soporte de tensión mucho más rápido que el generador síncrono. El GFM con \( Q \)-droop puede responder en 5–10 ms frente a los 100–300 ms del AVR con excitador estático.

**El PSS (Power System Stabilizer).** El AVR por sí solo puede desestabilizar las oscilaciones electromecánicas entre generadores (modos de oscilación intergeneradores, 0.5–3 Hz): al aumentar la excitación para sostener la tensión, puede reducir el amortiguamiento del modo. El PSS añade una señal de amortiguamiento (proporcional a \( d\omega/dt \) o a la potencia activa) sobre la referencia del AVR:

$$  V_{PSS}=K_{PSS}\cdot\frac{T_1s+1}{T_2s+1}\cdot\frac{s}{1+T_ws}\cdot\Delta\omega $$

La función de transferencia del PSS es un filtro paso-banda sintonizado sobre los modos de interés: introduce avance de fase para recuperar el amortiguamiento perdido.

**La diferencia con el VSM.** El VSM emula el AVR, el governor y la swing equation en software, pero con dos ventajas: (1) los parámetros (\( H \), \( D \), droop de \( Q \)) son ajustables en tiempo real; (2) la respuesta de tensión es mucho más rápida (el lazo de corriente del convertidor, a 200–1000 Hz, sustituye al excitador de campo).

## 5 — La conexión a red y la sincronización

**Condiciones de sincronismo.** Para cerrar el interruptor de conexión a la red sin perturbación, la máquina debe tener:
1. **Frecuencia igual** a la de la red: \( f_{gen}=f_{red} \) (error <0.05 Hz).
2. **Tensión igual** en módulo: \( |V_{gen}|=|V_{red}| \) (error <5%).
3. **Fase igual**: \( \angle V_{gen}=\angle V_{red} \) (error <0.1 rad ≈ 5.7°).
4. **Secuencia de fases igual**: abc en ambos lados.

**El sincronizador automático (syncrocheck).** Ajusta la velocidad del motor primo hasta que la frecuencia diferencial \( \Delta f = f_{gen}-f_{red} \) es pequeña (el vector diferencial \( \Delta V \) gira lentamente). Cuando \( \Delta\theta<\theta_{max} \) y \( \Delta V<V_{max} \), el relay de sincronismo da la orden de cierre.

**Tras el cierre.** La red "arrastra" a la máquina: el par sincronizante \( K_s\cdot\Delta\theta \) alinea el rotor con la red en oscilaciones amortiguadas. Cuanto mayor es \( H \), más suave es la transición (menor RoCoF) pero la oscilación dura más.

**Comparación con el GFM (VSM/droop).** Un convertidor GFM puede conectarse a la red sin un sincronizador explícito: la dinámica del droop de potencia actua como un sincronizador implícito. En la práctica se añade un pre-sincronizador suave (rampa de potencia) para evitar el pico de corriente en el momento del cierre. La diferencia fundamental es que el GFM **siempre está listo para conectarse** (no necesita esperar a que el motor primo alcance la velocidad) y la **transición isla→red es imperceptible** si el GFM ya está imponiendo la misma frecuencia y tensión que la red.

**Estabilidad en red fuerte.** Un resultado contra-intuitivo: las máquinas síncronas, igual que los GFM agresivos, pueden volverse inestables en red fuerte (SCR muy alto) si el par sincronizante supera la capacidad de amortiguamiento. La diferencia es que \( H \) y \( D \) de la máquina real están fijados por el diseño mecánico, mientras que el GFM puede ajustar su \( D \) virtual para estabilizarse.

## 6 — Diseño iterativo: modelar el equivalente Thevenin de la máquina síncrona

**Parámetros dados:** \( X_d=1.05\,\text{pu} \), \( X_q=0.65\,\text{pu} \), \( R_a=0.01\,\text{pu} \), \( H=5\,\text{s} \), \( D=5\,\text{pu} \), \( S_n=1\,\text{MVA} \), \( \omega_0=2\pi\times50 \).

**Paso 1 — punto de operación.** Operando a \( P_0=0.7\,\text{pu} \), \( V=1\,\text{pu} \), \( E=1.1\,\text{pu} \):

$$  \delta_0=\arcsin\!\left(\frac{P_0\,X_d}{E\,V}\right)=\arcsin\!\left(\frac{0.7\times1.05}{1.1\times1}\right)=\arcsin(0.668)\approx41.9° $$

**Paso 2 — par sincronizante.** La pendiente de la curva \( P(\delta) \) en el punto de operación:

$$  K_s=\frac{EV}{X_d}\cos\delta_0=\frac{1.1\times1}{1.05}\times\cos(41.9°)=1.048\times0.745=0.780\,\text{pu/rad} $$

Un \( K_s \) positivo indica que la máquina es estable en pequeña señal en este punto. Si \( \delta_0>90° \), \( K_s<0 \) y la máquina está en zona inestable.

**Paso 3 — oscilaciones electromecánicas.** La frecuencia natural y el factor de amortiguamiento del modo electromecánico:

$$  \omega_n=\sqrt{\frac{K_s\,\omega_0}{2H}}=\sqrt{\frac{0.780\times314}{10}}=\sqrt{24.5}\approx4.95\,\text{rad/s}\quad(0.79\,\text{Hz}) $$

$$  \zeta=\frac{D\,\omega_0}{4H\,\omega_n}=\frac{5\times314}{4\times5\times4.95}=\frac{1570}{99}\approx 0.16 $$

El modo es levemente amortiguado (\( \zeta=0.16 \)): el transitorio tarda \( 5\tau=5/(0.16\times4.95)\approx6.3\,\text{s} \) en amortiguarse. Un PSS típico elevaría \( \zeta \) a 0.3–0.4.

**Paso 4 — equivalente para el VSM.** Para que un VSM de 1 MVA replique esta dinámica:
- \( H_{VSM}=5\,\text{s} \) (parámetro del integrador de velocidad).
- \( D_{VSM}=5\,\text{pu} \) (amortiguamiento virtual).
- \( K_{droop,Q}=(E-V)/Q_0 \) (droop de tensión para emular el AVR).
- El VSM no tiene \( T'_{d0} \): la respuesta de tensión es instantánea (lazo de corriente en ms).

La única diferencia en la respuesta de frecuencia es que el VSM puede ajustar \( H \) y \( D \) en tiempo real para optimizar la estabilidad de la red.

<div class="cfig"><img src="figuras/generador-sincrono-analisis.png" alt="análisis completo del generador síncrono"><div class="cap">Panel (a): circuito equivalente dq con los dos ejes, las tensiones de rotación y el par. Panel (b): curva de capabilidad con los límites de armadura y de excitación mínima/máxima; el punto de operación (P=0.7, Q=0.2) es factible. Panel (c): ecuación de swing para H=2, 5, 10 s ante un escalón ΔP=0.3 pu; mayor H implica RoCoF menor pero oscilación más prolongada. Panel (d): comparativa GS real vs VSM ajustado al equivalente; la respuesta de frecuencia es prácticamente idéntica.</div></div>

## Cuándo y por qué se usa
Para estudios de estabilidad de red mixta (generadores + convertidores), para entender la base
física del VSM/PSC/matching, y para modelar el lado AC de sistemas back-to-back con máquina.

## Procedimiento de diseño (genérico)
1. Elige el orden del modelo según el estudio: clásico (ángulo), 4º (transitorio), completo (cortocircuito).
2. Parametriza \( L_d,L_q,L'_d,L'_q,T'_{d0},T'_{q0},H,D \) de la hoja de datos.
3. Implementa en espacio de estados ([[representacion-espacio-estados]]) y linealiza en el punto de operación.
4. Cierra AVR y governor para estudios de régimen dinámico.
5. Conecta al modelo de red (Thevenin o nodos) y verifica estabilidad.

## Ejemplo de código
```python
def sg_swing(delta, dw, Tm, Te, H, D, w0):
    return [w0*dw, (Tm - Te - D*dw)/(2*H)]   # [d(delta)/dt, d(omega)/dt]

def Te_elec(psi_d, psi_q, id_, iq):
    return psi_d*iq - psi_q*id_               # par electromagnetico

def Ks_sync(E, V, Xd, delta0):
    """Par sincronizante (pendiente de la curva P-delta)."""
    return E*V/Xd * np.cos(delta0)

def omega_n_swing(Ks, w0, H):
    """Frecuencia natural del modo electromecánico."""
    return np.sqrt(Ks*w0/(2*H))
```

## Parámetros y valores típicos
\( H=2\text{–}9 \) s; \( X_d=0.8\text{–}2.0 \) p.u.; \( X'_d=0.1\text{–}0.35 \) p.u.;
\( T'_{d0}=3\text{–}10 \) s; \( T''_{d0}=0.02\text{–}0.05 \) s. \( X_d>X_q \) (polo saliente) o
\( X_d=X_q \) (cilíndrico).

## Errores comunes
- Usar el modelo clásico (2 estados) para estudios subtransitorios → no captura la dinámica de los amortiguadores.
- Olvidar que \( X_d\ne X_q \) en máquinas de polo saliente (PMSG, hidro) → error en \( T_e \).
- Parametrizar el VSM con \( H \) del generador real sin considerar la limitación de corriente del convertidor.
- Confundir el ángulo de carga \( \delta \) (entre \( E \) y \( V \)) con el ángulo de potencia en el fàsor de tensión terminal.

## Conceptos relacionados
- [[ecuacion-oscilacion]] · [[vsm-inercia]] · [[marco-dq]] · [[representacion-espacio-estados]] · [[clasificacion-estabilidad]]

## Referencias
- Kundur, *Power System Stability and Control*, 1994.
- Anderson, Fouad, *Power System Control and Stability*, IEEE Press 2003.
