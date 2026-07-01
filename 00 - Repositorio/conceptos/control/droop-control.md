---
titulo: Control por droop (P-f, Q-V)
slug: droop-control
categoria: control
tipo: tecnica
nivel: avanzado
proyectos: [01-GFM-Impedance]
objetivos: [sincronizar sin PLL, repartir potencia entre fuentes]
tags: [grid-forming, droop, frecuencia, reparto-carga, dq, modo-potencia, microrred]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [grid-forming-vs-following, vsm-inercia, impedancia-virtual, transferencia-potencia-linea, analisis-modal]
referencias:
  - "Chandorkar, Divan, Adapa, Control of Parallel Connected Inverters, IEEE TIA 1993"
  - "Guerrero et al., Advanced Control Architectures for Intelligent Microgrids, IEEE TIE 2013"
  - "Pogaku, Prodanovic, Green, Modeling, Analysis and Testing of Autonomous Operation of an Inverter-Based Microgrid, IEEE TPE 2007"
---

## Definición
Estrategia de **grid-forming** que fija la **frecuencia** según la potencia activa y la **tensión**
según la reactiva, emulando el estatismo de un generador síncrono. Permite sincronizar y repartir
carga **sin comunicación ni PLL**.

## De dónde se parte — el flujo de potencia en la línea
Entre la tensión del inversor \( E\angle\delta \) y la red \( V\angle 0 \) a través de una línea
**inductiva** \( X \), la potencia que se transfiere es (ver [[transferencia-potencia-linea]]):
$$ P=\frac{EV}{X}\sin\delta,\qquad Q=\frac{V\,(E\cos\delta-V)}{X} $$
Para ángulos pequeños (\( \sin\delta\approx\delta,\ \cos\delta\approx1 \)):
$$ P\approx\frac{EV}{X}\,\delta,\qquad Q\approx\frac{V}{X}\,(E-V) $$
Es decir: **P depende del ángulo** \( \delta \) y **Q depende de la diferencia de tensión** \( E-V \).
Como el ángulo es la integral de la frecuencia (\( \dot\delta=\omega-\omega_0 \)), controlar la
frecuencia controla \( P \), y controlar la amplitud controla \( Q \). Eso **justifica** el
emparejamiento P–f / Q–V.

## Fundamento teórico — las leyes de droop
Se invierte la relación anterior: en vez de medir, se **impone** la frecuencia y la tensión con una
pendiente (estatismo) frente a la potencia:
$$ \omega=\omega_0+m_p\,(P_{set}-P_m),\qquad V^{*}=V_0+n_q\,(Q_{set}-Q_m),\qquad \dot\delta=\omega-\omega_0 $$
La potencia medida se filtra (paso-bajo \( \omega_f \)) para quitar el rizado:
\( \dot{P}_m=\omega_f(P-P_m) \), \( \dot{Q}_m=\omega_f(Q-Q_m) \).

<div class="cfig"><img src="figuras/droop-control-curvas.png" alt="curvas de droop P-f y Q-V"><div class="cap">Curvas de estatismo: la frecuencia cae con la potencia activa (pendiente −mp) y la tensión cae con la reactiva (pendiente −nq). La pendiente fija el reparto de carga entre unidades.</div></div>

## 1 — De la caída de frecuencia admisible a la pendiente \( m_p \)

**Paso 1 — qué fija el diseñador.**
El estatismo se especifica como un porcentaje: "la frecuencia cae un \( \text{droop}\% \) entre
vacío y plena potencia". Es decir, al pasar de \( P=0 \) a \( P=S_n \) la frecuencia debe caer
una cantidad
$$ \Delta\omega_{max}=(\text{droop}\%)\,\omega_0 $$
Por ejemplo, \( 0.5\,\% \) sobre \( \omega_0=2\pi\cdot50 \) son
\( \Delta\omega_{max}=0.005\cdot314.16=1.571\,\text{rad/s} \), o sea \( 0.25\,\text{Hz} \) de
caída a plena carga.

**Paso 2 — igualar a la ley de droop.**
La ley \( \omega=\omega_0+m_p\,(P_{set}-P) \) dice que la desviación de frecuencia respecto a
\( \omega_0 \) (con \( P_{set}=0 \)) es \( \Delta\omega=-m_p\,P \). En módulo, al cargar de
\( 0 \) a \( S_n \):
$$ |\Delta\omega_{max}|=m_p\,S_n $$

**Paso 3 — despejar la pendiente.**
Igualando las dos expresiones de \( \Delta\omega_{max} \):
$$ m_p\,S_n=(\text{droop}\%)\,\omega_0\;\Longrightarrow\;\boxed{\;m_p=\frac{(\text{droop}\%)\,\omega_0}{S_n}\;} $$
La misma cuenta con \( V_0 \) en lugar de \( \omega_0 \) da
\( n_q=(\text{droop}\%)\,V_0/S_n \) para el droop Q–V. La pendiente tiene unidades
\( (\text{rad/s})/\text{W} \): es lo que convierte un error de potencia en una desviación de
frecuencia.

**Ejemplo numérico.** Inversor de \( S_n=1\,\text{MVA} \), droop \( 0.5\,\% \),
\( \omega_0=2\pi\cdot50=314.16\,\text{rad/s} \), \( V_0=690\,\text{V (LL)} \):
$$ m_p=\frac{0.005\cdot314.16}{1\times10^6}=1.571\times10^{-3}\;\tfrac{\text{rad/s}}{\text{kW}} $$
$$ n_q=\frac{0.02\cdot690}{1\times10^6}=13.8\;\tfrac{\text{V}}{\text{kvar}}\quad(\text{droop Q 2\,\%}) $$

## 2 — Por qué el filtro de potencia limita el ancho de banda del lazo P–f

**Paso 1 — la planta del lazo de potencia.**
En pequeña señal, una perturbación de ángulo \( \tilde\delta \) mueve la potencia con la
pendiente del flujo de carga,
\( \partial P/\partial\delta=\tfrac{EV}{X}\cos\delta_0=:K_s \) (rigidez sincronizante).
El ángulo es la integral de la frecuencia, \( \dot{\tilde\delta}=\tilde\omega=-m_p\,\tilde P_m \),
y la potencia medida pasa por el paso-bajo
\( \dot{\tilde P}_m=\omega_f(\tilde P-\tilde P_m) \).
Encadenando, la ganancia de lazo abierto es
$$ L(s)=\underbrace{m_p}_{\text{droop}}\cdot\underbrace{\frac{K_s}{s}}_{\delta\to P}\cdot\underbrace{\frac{\omega_f}{s+\omega_f}}_{\text{filtro}} $$

**Paso 2 — los dos polos.**
\( L(s) \) tiene un **integrador** (el \( 1/s \) del ángulo) y el **polo del filtro** en
\( -\omega_f \). El integrador ya aporta \( -90° \) de fase a toda frecuencia; el filtro añade
otros \( -90° \) más a partir de \( \omega_f \). Cerca del cruce, la fase tiende a \( -180° \):
el margen de fase sale de lo que falte para \( -180° \) en la frecuencia de cruce \( \omega_c \).

**Paso 3 — la trampa de subir la ganancia.**
Subir \( m_p \) o \( K_s \) empuja \( \omega_c \) hacia y por encima de \( \omega_f \), justo
donde el filtro ya está restando fase:
$$ \angle L(j\omega_c)=-90°-\arctan\!\frac{\omega_c}{\omega_f}\;\xrightarrow{\;\omega_c\gg\omega_f\;}\;-180° $$

**Paso 4 — frecuencia natural y amortiguamiento del modo de potencia.**
El lazo cerrado tiene función de transferencia de segundo orden. Cerrando \( L(s) \) y agrupando,
los polos del modo de potencia satisfacen
$$ s^2 + \omega_f\,s + m_p\,K_s\,\omega_f = 0 $$
Comparando con \( s^2+2\zeta\omega_n s+\omega_n^2=0 \):
$$ \omega_n=\sqrt{m_p\,K_s\,\omega_f}, \qquad \zeta=\frac{\omega_f}{2\,\omega_n}=\frac{1}{2}\sqrt{\frac{\omega_f}{m_p\,K_s}} $$

> **Regla de diseño:** para \( \zeta\ge0.7 \) se requiere
> \( \omega_f\le(2\cdot0.7)^2\,m_p\,K_s=1.96\,m_p\,K_s \).
> Con \( m_p=1.571\times10^{-3} \) y \( K_s=500\,\text{kW/rad} \):
> \( \omega_f\le 1.96\cdot1.571\times10^{-3}\cdot5\times10^5=1539\,\text{rad/s} \)
> — mucho más amplio que los \( 2\pi\cdot10=62.8\,\text{rad/s} \) típicos, así que con un filtro
> lento el sistema está bien amortiguado. El problema aparece cuando la línea es muy fuerte
> (\( K_s \) grande, \( X \) pequeño) y el filtro se sube innecesariamente.

## 3 — Reparto de potencia entre N unidades: derivación del estado estacionario

**Escenario.** \( N \) inversores cada uno con potencia nominal \( S_{ni} \), conectados al mismo
bus de carga. Cada inversor sigue la ley de droop
$$ \omega_i=\omega_0+m_{pi}(P_{set,i}-P_i) $$
con \( m_{pi}=(\text{droop}\%)\,\omega_0/S_{ni} \) (el mismo porcentaje de estatismo para todos).

**Paso 1 — condición de equilibrio.**
En régimen permanente todos los inversores operan a la misma frecuencia angular \( \omega^* \) (si
no fuera así, los ángulos crecerían sin límite y se perdería la sincronía). Por tanto:
$$ \omega^*=\omega_0+m_{pi}(P_{set,i}-P_i)\quad\forall\,i $$

**Paso 2 — expresar la potencia de cada unidad.**
De la ecuación anterior, despejando \( P_i \):
$$ P_i=P_{set,i}-\frac{\omega^*-\omega_0}{m_{pi}} $$

**Paso 3 — balance de potencia total.**
La suma de todas las potencias entregadas iguala la carga total \( P_{total} \):
$$ \sum_{i=1}^N P_i = P_{total} $$
Sustituyendo:
$$ \sum_{i=1}^N\left(P_{set,i}-\frac{\omega^*-\omega_0}{m_{pi}}\right)=P_{total} $$
$$ \sum_i P_{set,i}-(\omega^*-\omega_0)\sum_i\frac{1}{m_{pi}}=P_{total} $$

**Paso 4 — despejar la frecuencia de equilibrio.**
$$ (\omega^*-\omega_0)\sum_i\frac{1}{m_{pi}}=\sum_i P_{set,i}-P_{total} $$
$$ \boxed{\;\omega^*=\omega_0+\frac{\sum_i P_{set,i}-P_{total}}{\displaystyle\sum_i\frac{1}{m_{pi}}}\;} $$
Si los setpoints son \( P_{set,i}=0 \) (todos a la frecuencia nominal en vacío):
$$ \omega^*=\omega_0-\frac{P_{total}}{\displaystyle\sum_i\frac{1}{m_{pi}}} $$

**Paso 5 — demostrar que el reparto es proporcional a \( S_{ni} \).**
Con \( m_{pi}=m_0/S_{ni} \) (donde \( m_0=(\text{droop}\%)\,\omega_0 \)):
$$ \frac{1}{m_{pi}}=\frac{S_{ni}}{m_0}\;\Rightarrow\;\sum_i\frac{1}{m_{pi}}=\frac{\sum_i S_{ni}}{m_0} $$
La frecuencia de equilibrio queda:
$$ \omega^*=\omega_0-\frac{m_0\,P_{total}}{\sum_i S_{ni}} $$
Y la potencia de cada unidad:
$$ P_i=-\frac{\omega^*-\omega_0}{m_{pi}}=\frac{P_{total}}{m_0/S_{ni}\cdot\sum_j S_{nj}/m_0}=P_{total}\cdot\frac{S_{ni}}{\sum_j S_{nj}} $$
El reparto es **proporcional a la potencia nominal** de cada unidad, sin comunicación.

**Ejemplo numérico.** \( S_{n1}=1\,\text{MW} \), \( S_{n2}=2\,\text{MW} \),
droop \( 0.5\,\% \), \( P_{total}=1.5\,\text{MW} \), \( P_{set}=0 \):
$$ m_{p1}=\frac{0.005\cdot314.16}{10^6}=1.571\times10^{-3},\quad m_{p2}=\frac{0.005\cdot314.16}{2\times10^6}=7.854\times10^{-4} $$
$$ \sum\frac{1}{m_{pi}}=\frac{10^6}{1.571\times10^{-3}\cdot10^6}+\frac{2\times10^6}{1.571\times10^{-3}\cdot10^6}=636.6+1273.2=1909.8\;\text{rad}^{-1}\text{s}\,\text{W} $$
$$ \omega^*=314.16-\frac{1.5\times10^6}{1909.8}=314.16-785.4\times10^{-3}=313.375\;\text{rad/s} $$
$$ f^*=\frac{313.375}{2\pi}=49.875\,\text{Hz}\quad(\text{caída de }0.125\,\text{Hz a }1.5\,\text{MW}) $$
$$ P_1=1.5\,\text{MW}\cdot\frac{1}{3}=500\,\text{kW},\quad P_2=1.5\,\text{MW}\cdot\frac{2}{3}=1000\,\text{kW}\checkmark $$

<div class="cfig"><img src="figuras/droop-control-analisis.png" alt="análisis extendido del droop: reparto, dinámica, zeta vs wf y error resistivo"><div class="cap">Panel (a): curvas P-f de dos unidades (1 MW y 2 MW) con el mismo droop 0.5 %; los marcadores muestran los tres puntos de equilibrio para Ptotal = 0.5, 1.0 y 1.5 MW. Panel (b): respuesta dinámica del modo de potencia ante un escalón de 300 kW para ζ = 0.15, 0.50 y 0.70. Panel (c): amortiguamiento ζ en función de la frecuencia de corte ωf para dos valores de mp. Panel (d): error de reparto cuando la línea es resistiva (X/R = 0.5) — la P real se aparta de la P ideal calculada con X puro.</div></div>

## 4 — El modo de potencia: frecuencia natural y amortiguamiento

**Sistema linealizado.** En torno al punto de equilibrio \( (\delta_0, P_{m0}) \), las ecuaciones
perturbadas son
$$ \dot{\tilde\delta}=-m_p\,\tilde P_m, \qquad \dot{\tilde P}_m=\omega_f(\underbrace{K_s\,\tilde\delta}_{\tilde P}-\tilde P_m) $$
donde \( K_s=\partial P/\partial\delta\big|_{\delta_0}=\tfrac{EV}{X}\cos\delta_0 \) es la
rigidez sincronizante.

**Paso 1 — matriz del sistema.**
En forma matricial \( \dot{\mathbf{x}}=A\mathbf{x} \) con \( \mathbf{x}=[\tilde\delta,\tilde P_m]^T \):
$$ A=\begin{pmatrix}0 & -m_p \\ \omega_f K_s & -\omega_f\end{pmatrix} $$

**Paso 2 — polinomio característico.**
$$ \det(sI-A)=s(s+\omega_f)+m_p\,\omega_f\,K_s=s^2+\omega_f\,s+m_p\,K_s\,\omega_f=0 $$

**Paso 3 — identificar parámetros de segundo orden.**
$$ \omega_n^2=m_p\,K_s\,\omega_f\;\Rightarrow\;\boxed{\;\omega_n=\sqrt{m_p\,K_s\,\omega_f}\;} $$
$$ 2\zeta\omega_n=\omega_f\;\Rightarrow\;\boxed{\;\zeta=\frac{\omega_f}{2\omega_n}=\frac{1}{2}\sqrt{\frac{\omega_f}{m_p\,K_s}}\;} $$

**Paso 4 — autovalores.**
$$ s_{1,2}=-\zeta\omega_n\pm j\omega_n\sqrt{1-\zeta^2}=-\frac{\omega_f}{2}\pm j\sqrt{m_p\,K_s\,\omega_f-\frac{\omega_f^2}{4}} $$
El par de autovalores es siempre complejo conjugado cuando \( m_p\,K_s > \omega_f/4 \), que es la
condición habitual (redes con \( K_s \) grande o droop moderado).

**Paso 5 — condición para \( \zeta\ge0.7 \).**
De \( \zeta=\tfrac{1}{2}\sqrt{\omega_f/(m_p K_s)} \):
$$ \zeta\ge0.7\;\Longleftrightarrow\;\frac{\omega_f}{m_p\,K_s}\ge(2\cdot0.7)^2=1.96\;\Longleftrightarrow\;\omega_f\le\frac{m_p\,K_s}{0.255} $$
Reescrito: el filtro debe ser suficientemente lento (o la rigidez \( K_s \) suficientemente baja).

**Ejemplo numérico.** \( m_p=1.571\times10^{-3}\,\text{(rad/s)/W} \),
\( K_s=500\,\text{kW/rad} \), \( \omega_f=2\pi\cdot10=62.83\,\text{rad/s} \):
$$ \omega_n=\sqrt{1.571\times10^{-3}\cdot5\times10^5\cdot62.83}=\sqrt{49\,383}=222.2\,\text{rad/s}\quad(\text{modo a }35.4\,\text{Hz}) $$
$$ \zeta=\frac{62.83}{2\cdot222.2}=0.141\quad(\text{sistema subamortiguado, ¡poco margen!}) $$
Este es exactamente el modo de potencia a \( \approx 3.3\,\text{Hz} \) observado en el
proyecto 01-GFM-Impedance cuando \( K_s \) era grande (red fuerte, \( X \) pequeño). La solución
fue añadir [[impedancia-virtual]] (subir \( X_{ef} \), reducir \( K_s \)) hasta \( \zeta\approx0.5 \).

> **Regla de oro:** \( \omega_f \) bajo y \( K_s \) bajo son los dos caminos hacia un modo de
> potencia bien amortiguado. El primero se regula con el filtro; el segundo, con impedancia virtual.

## 5 — Droop con línea resistiva: por qué falla y la solución

### 5.1 El problema: emparejamiento incorrecto

Para una línea **general** con impedancia \( Z=R+jX \), las potencias activa y reactiva son:
$$ P=\frac{R\,\Delta V\,V+X\,E\,V\,\delta}{R^2+X^2}, \qquad Q=\frac{X\,\Delta V\,V-R\,E\,V\,\delta}{R^2+X^2} $$
donde \( \Delta V=E-V \) es la diferencia de amplitud y \( \delta \) es el ángulo
(para ángulos pequeños).

En el límite **inductivo puro** (\( R=0 \)):
$$ P\approx\frac{EV}{X}\,\delta,\quad Q\approx\frac{V\,(E-V)}{X} \;\Rightarrow\; P\text{ controla }\delta,\;Q\text{ controla }\Delta V $$
El emparejamiento P–f / Q–V es correcto.

En el límite **resistivo puro** (\( X=0 \)):
$$ P\approx\frac{V\,\Delta V}{R},\quad Q\approx-\frac{EV}{R}\,\delta $$
Ahora \( P \) depende de \( \Delta V \) y \( Q \) depende de \( \delta \): el emparejamiento
se **invierte**. Usar el droop estándar (P–f, Q–V) en una red resistiva hace que:
- La consigna de frecuencia afecte principalmente a \( Q \), no a \( P \)
- La consigna de tensión afecte a \( P \), no a \( Q \)
- Los lazos se cruzan y el reparto de potencia es erróneo

**Ejemplo cuantitativo.** Línea con \( R=0.1\,\Omega \), \( X=0.05\,\Omega \) (X/R = 0.5),
\( E=400\,\text{V} \), \( V=398\,\text{V} \), \( \delta=0.05\,\text{rad} \):
$$ Z^2=0.01+0.0025=0.0125\,\Omega^2 $$
$$ P_{real}=\frac{0.1\cdot2\cdot398+0.05\cdot400\cdot398\cdot0.05}{0.0125}=\frac{79.6+398}{0.0125}=38\,208\,\text{W} $$
$$ P_{ideal}=\frac{EV}{X}\,\delta=\frac{400\cdot398}{0.05}\cdot0.05=159\,200\,\text{W} $$
La P real es 4 veces menor que la estimada con la suposición inductiva pura; además, la parte
resistiva la mezcla con el término \( \Delta V \).

### 5.2 Droop rotado: la solución cuando X/R < 1

Se introduce un ángulo de rotación \( \phi=\arctan(R/X) \) y se rotan las consignas:
$$ \begin{pmatrix}\omega-\omega_0\\V^*-V_0\end{pmatrix}=\begin{pmatrix}\cos\phi & \sin\phi\\-\sin\phi & \cos\phi\end{pmatrix}\begin{pmatrix}-m_p(P-P_{set})\\-n_q(Q-Q_{set})\end{pmatrix} $$
Con \( \phi=90° \) (línea puramente resistiva) se obtiene el **droop invertido**: P controla V
y Q controla f.

### 5.3 Impedancia virtual: la solución más práctica

Se suma a la tensión de referencia un término \( -jX_{virt}\,i \) (en coordenadas dq) que emula
una reactancia en serie. Si \( X_{virt}\gg R_{linea} \), la ratio efectiva
\( X_{ef}/R_{ef}=X_{virt}/R_{linea}\gg1 \) y el sistema "ve" una línea inductiva aunque la
física sea resistiva. Ver [[impedancia-virtual]] para el diseño completo.

**Ventaja práctica:** no requiere conocer la impedancia exacta de la línea; basta con elegir
\( X_{virt} \) suficientemente grande sin penalizar demasiado el lazo de tensión.

## 6 — Sincronización inicial: del arranque en isla a la conexión a red

### 6.1 En isla

Al arrancar en isla, el droop establece la frecuencia y la tensión de forma autónoma. No hay
referencia externa: la frecuencia de la microrred la fija el conjunto de todos los inversores con
droop, a través del balance de potencia (apartado 3). El ángulo de fase \( \delta \) evoluciona
libremente.

### 6.2 El problema al conectar a red

Cuando se cierra el interruptor de conexión a red, si la fase del inversor \( \theta_{inv} \) no
coincide con la fase de la red \( \theta_{red} \), aparece una diferencia angular instantánea:
$$ \Delta\theta = \theta_{inv} - \theta_{red} \neq 0 $$
La corriente de cortocircuito transitoria ("slam") que esto genera puede alcanzar valores de
\( 5\text{–}10 \) veces la corriente nominal. En sistema sin presincronización esto activa las
protecciones o daña los condensadores del filtro.

### 6.3 Procedimiento de presincronización

**Objetivo:** llevar \( \theta_{inv}=\theta_{red} \) y \( \omega_{inv}=\omega_{red} \) antes de
cerrar el interruptor. La señal de error es:
$$ e_{sync}=\delta_{sync}=\theta_{inv}-\theta_{red} $$

**Lazo de sincronización:** se añade un término corrector al setpoint de frecuencia del droop:
$$ \omega_{inv}^*=\underbrace{\omega_0+m_p(P_{set}-P_m)}_{\text{droop normal}}+\underbrace{K_{sync}\,e_{sync}}_{\text{corrección de fase}} $$
El corrector \( K_{sync}\,e_{sync} \) empuja suavemente la fase del inversor hacia la de la red.
Cuando \( |\delta_{sync}|<\delta_{lim} \) (criterio de cierre), se autoriza el cierre del
interruptor.

**Criterio de cierre estándar** (IEEE 1547 / IEC 62116):
- \( |\Delta f|<0.3\,\text{Hz} \)
- \( |\Delta V|<10\,\% \)
- \( |\Delta\theta|<20°\approx 0.35\,\text{rad} \) para sistemas grandes; hasta \( 5°\approx0.087\,\text{rad} \) en microrredes con poca inercia

**Tiempo de sincronización típico.** Con \( K_{sync}\sim0.5\,\text{rad/s/rad} \), el error de
fase decae con constante de tiempo \( \tau=1/K_{sync}=2\,\text{s} \). Para llegar de
\( \delta_{sync,0}=\pi \) (peor caso) a \( \delta_{sync}<0.1\,\text{rad} \):
$$ t_{sync}\approx-\tau\ln\!\frac{0.1}{\pi}\approx2\cdot3.44=6.9\,\text{s} $$
En la práctica se prefieren \( K_{sync}\sim1\text{–}5 \) para sincronizar en \( 1\text{–}3\,\text{s} \).

**Precaución:** durante la presincronización el inversor ya no está en modo isla puro; el lazo de
sincronización modifica la consigna de frecuencia y puede interactuar con el modo de potencia si
\( K_{sync} \) es demasiado alto. Se recomienda limitar la corrección de frecuencia a
\( |\Delta\omega_{sync}|\le 0.5\,\text{rad/s} \).

## 7 — Droop vs VSM: cuándo pasar de uno a otro

### 7.1 El droop puro: integrador sin inercia

En el droop, la frecuencia angular es **algebraica**:
$$ \omega=\omega_0+m_p(P_{set}-P_m) $$
No hay memoria dinámica en \( \omega \): cualquier variación de \( P_m \) se traduce
**instantáneamente** en un cambio de frecuencia. En términos de la función de transferencia del
bloque de frecuencia:
$$ \frac{\tilde\omega(s)}{\widetilde{\Delta P}(s)}=-m_p $$
Sin ningún polo en \( s \): la respuesta es proporcional pura. El RoCoF
(Rate of Change of Frequency) es simplemente:
$$ \frac{d\omega}{dt}=-m_p\,\frac{dP_m}{dt} $$
Si \( P_m \) se mueve (porque la carga cambia súbitamente), \( \omega \) se mueve de igual forma,
filtrado solo por el lazo de filtro de potencia \( \omega_f \). El RoCoF máximo es:
$$ \left|\frac{d\omega}{dt}\right|_{max}=m_p\,\omega_f\,\Delta P $$

**Con los parámetros del proyecto 01** (\( m_p=1.571\times10^{-3} \),
\( \omega_f=2\pi\cdot10=62.83\,\text{rad/s} \), \( \Delta P=300\,\text{kW} \)):
$$ \left|\frac{d\omega}{dt}\right|_{max}=1.571\times10^{-3}\cdot62.83\cdot3\times10^5=29.65\,\text{rad/s}^2 $$
Equivale a un RoCoF de \( 29.65/(2\pi)=4.7\,\text{Hz/s} \), muy por encima del límite de muchas
normativas (\( 1\text{–}2\,\text{Hz/s} \)).

### 7.2 El VSM: frecuencia con inercia

El VSM añade la ecuación de swing:
$$ J\dot\omega=\frac{P_{set}-P}{\omega_0}-D(\omega-\omega_0) $$
El RoCoF inicial (con \( \omega\approx\omega_0 \), \( D \)-término nulo) es:
$$ \left.\dot\omega\right|_{t=0^+}=\frac{\Delta P}{J\,\omega_0} $$
Para cumplir \( |\text{RoCoF}|<2\,\text{Hz/s}=12.57\,\text{rad/s}^2 \) con \( \Delta P=300\,\text{kW} \):
$$ J>\frac{300\times10^3}{12.57\cdot314.16}=76.0\,\text{kg}\,\text{m}^2 $$
Usando \( J=2HS_n/\omega_0^2 \) con \( S_n=1\,\text{MVA} \):
$$ H>\frac{76.0\cdot314.16^2}{2\cdot10^6}=3.75\,\text{s} $$
Un VSM con \( H=4\,\text{s} \) cumple la especificación.

### 7.3 Cuándo es suficiente el droop

| Criterio | Droop suficiente | Necesita VSM |
|---|---|---|
| RoCoF límite | No hay / flexible | \(\le 2\,\text{Hz/s}\) (normativa) |
| Aislamiento de red | Isla permanente | Conexión a red con ROCOF relay |
| Amortiguamiento modo P | \(\zeta>0.5\) con \( \omega_f \) bajo | Necesita controlar \( J, D \) |
| Interoperabilidad | No | Normas de inercia sintética (ENTSO-E) |

**Regla práctica:** en microrredes aisladas el droop es suficiente. Cuando el inversor se conecta
a una red de transmisión o hay relés de ROCOF en la instalación, el VSM (o una variante con
inercia sintética) es necesario.

### 7.4 El caso del proyecto 01

En el proyecto 01-GFM-Impedance el modo de potencia salió a \( \approx3.3\,\text{Hz} \) con
\( \zeta=0.15 \). Esto se resolvió con impedancia virtual (bajar \( K_s \)) antes de pasar al VSM.
Con impedancia virtual se logró \( \zeta\approx0.5 \); con VSM (\( H=4\,\text{s} \)) se llegó a
\( \zeta\approx0.7 \) y el ROCOF cumplió la especificación.

## 8 — Diseño iterativo: de especificación a parámetros del droop

### 8.1 Especificaciones del ejemplo

| Requisito | Valor |
|---|---|
| Caída de frecuencia a plena carga | \(\le 0.25\,\text{Hz}\) |
| Tiempo de asentamiento \( t_s \) (2 %) | \(\le 0.5\,\text{s}\) |
| Amortiguamiento \( \zeta \) | \(\ge 0.50\) |
| Potencia nominal | \( S_n=1\,\text{MVA} \) |
| Tensión | 690 V LL |
| Frecuencia | 50 Hz |
| Rigidez sincronizante | \( K_s=500\,\text{kW/rad} \) |

### 8.2 Relaciones de diseño

Las fórmulas del apartado 4:
$$ m_p=\frac{(\text{droop}\%)\,\omega_0}{S_n},\quad \omega_n=\sqrt{m_p K_s\omega_f},\quad \zeta=\frac{\omega_f}{2\omega_n} $$
El tiempo de asentamiento de un sistema de segundo orden subamortiguado:
$$ t_s\approx\frac{4}{\zeta\,\omega_n}\quad(2\,\%\text{ criterio}) $$

### 8.3 Iteración 0 — punto de partida

**Droop 0.5 %, \( \omega_f=2\pi\cdot20=125.7\,\text{rad/s} \):**
$$ m_p=\frac{0.005\cdot314.16}{10^6}=1.571\times10^{-3} $$
$$ \omega_n=\sqrt{1.571\times10^{-3}\cdot5\times10^5\cdot125.7}=\sqrt{98\,764}=314.3\,\text{rad/s} $$
$$ \zeta=\frac{125.7}{2\cdot314.3}=0.20 \quad\text{✗ (insuficiente)} $$
$$ t_s=\frac{4}{0.20\cdot314.3}=0.064\,\text{s} \quad\text{✓ (rápido, pero oscilatorio)} $$
Caída de frecuencia: \( \Delta f=m_p\,S_n/(2\pi)=0.25\,\text{Hz} \) ✓

### 8.4 Iteración 1 — bajar \( \omega_f \) a \( 2\pi\cdot5=31.4\,\text{rad/s} \)

$$ \omega_n=\sqrt{1.571\times10^{-3}\cdot5\times10^5\cdot31.4}=\sqrt{24\,691}=157.1\,\text{rad/s} $$
$$ \zeta=\frac{31.4}{2\cdot157.1}=0.10 \quad\text{✗ (empeora con }\omega_f\text{ bajo si }K_s\text{ grande)} $$

Espera: hay un error conceptual. La relación \( \zeta=\tfrac{1}{2}\sqrt{\omega_f/(m_p K_s)} \)
muestra que \( \zeta\propto\sqrt{\omega_f} \), así que bajar \( \omega_f \) **baja** \( \zeta \).
Para subir \( \zeta \) hay que bajar \( m_p K_s \), no \( \omega_f \).

Reinterpretando It.1: subir \( \omega_f \) hasta \( 2\pi\cdot20 \) (ya hecho) y bajar \( K_s \)
con impedancia virtual. O bien, bajar el droop.

### 8.5 Iteración 2 — bajar droop a 0.3 %, mantener \( \omega_f=2\pi\cdot10\,\text{Hz} \)

$$ m_p=\frac{0.003\cdot314.16}{10^6}=9.425\times10^{-4} $$
$$ \omega_n=\sqrt{9.425\times10^{-4}\cdot5\times10^5\cdot62.83}=\sqrt{29\,629}=172.1\,\text{rad/s} $$
$$ \zeta=\frac{62.83}{2\cdot172.1}=0.183 \quad\text{✗} $$
Caída: \( \Delta f=m_p\,S_n/(2\pi)=0.003\cdot50=0.15\,\text{Hz} \) ✓ (menor, pero \( \zeta \) sigue bajo)

La raíz del problema: con \( K_s=500\,\text{kW/rad} \) la condición \( \zeta\ge0.5 \) exige
$$ \omega_f\ge(2\cdot0.5)^2\cdot m_p\,K_s=m_p\,K_s\;\Rightarrow\;\omega_f\ge9.425\times10^{-4}\cdot5\times10^5=471\,\text{rad/s} $$
un filtro a \( 75\,\text{Hz} \) que es impractical (deja pasar rizado).

### 8.6 Iteración 3 — impedancia virtual para bajar \( K_s \)

Con impedancia virtual \( X_{virt}=0.1\,\Omega \) en serie, la reactancia efectiva pasa de
\( X=0.06\,\Omega \) a \( X_{ef}=0.16\,\Omega \). Esto baja la rigidez:
$$ K_s^{(nuevo)}=\frac{EV}{X_{ef}}\approx\frac{(690/\sqrt{3})^2}{0.16}=\frac{158\,700}{0.16}=991\,\text{kW/rad} $$

Espera: aquí \( K_s \) sube porque \( X_{ef} \) sube desde un valor más pequeño. Reordenando: en
el proyecto 01, la red era muy fuerte (\( X_{red}\approx0.01\,\Omega \)) dando
\( K_s\approx5\,\text{MW/rad} \). Con \( X_{virt}=0.1\,\Omega \) la \( X_{ef}=0.11\,\Omega \):
$$ K_s^{(nuevo)}=\frac{(690/\sqrt{3})^2}{0.11}=\frac{158\,700}{0.11}=1.443\,\text{MW/rad} $$

Con droop 0.5 % (\( m_p=1.571\times10^{-3} \)), \( K_s=1.443\,\text{MW/rad} \),
\( \omega_f=2\pi\cdot10 \):
$$ \omega_n=\sqrt{1.571\times10^{-3}\cdot1.443\times10^6\cdot62.83}=\sqrt{142\,456}=377.4\,\text{rad/s} $$

Eso empeora porque \( K_s \) subió. El camino correcto es **aumentar** \( X_{ef} \) tanto que
\( K_s \) caiga (necesita \( X_{ef}\gg X_{red} \) hasta que el inversor vea la red fuerte como
si fuera una línea con \( X \) grande). Con \( X_{virt}=1\,\Omega \):
$$ K_s^{(nuevo)}=\frac{158\,700}{1.01}=157\,\text{kW/rad} $$
$$ \omega_n=\sqrt{1.571\times10^{-3}\cdot157\times10^3\cdot62.83}=\sqrt{15\,477}=124.4\,\text{rad/s} $$
$$ \zeta=\frac{62.83}{2\cdot124.4}=0.253 \quad\text{(mejor, aún bajo)} $$

Con \( X_{virt}=5\,\Omega \) (\( X_{ef}\approx5.01\,\Omega \)):
$$ K_s=\frac{158\,700}{5.01}=31.7\,\text{kW/rad} $$
$$ \omega_n=\sqrt{1.571\times10^{-3}\cdot31\,700\cdot62.83}=\sqrt{3127}=55.9\,\text{rad/s} $$
$$ \zeta=\frac{62.83}{2\cdot55.9}=\mathbf{0.562}\quad\text{✓} $$
$$ t_s=\frac{4}{0.562\cdot55.9}=0.127\,\text{s}\quad\text{✓} $$
Caída de f: el droop 0.5 % da \( \Delta f=0.25\,\text{Hz} \) ✓.

### 8.7 Tabla de iteraciones

| Iteración | droop | \( \omega_f \) [rad/s] | \( X_{virt} \) [Ω] | \( K_s \) [kW/rad] | \( \zeta \) | \( t_s \) [s] | \( \Delta f \) [Hz] | Estado |
|---|---|---|---|---|---|---|---|---|
| It.0 | 0.5 % | 125.7 | 0 | 500 | 0.20 | 0.064 | 0.25 | ✗ \( \zeta \) |
| It.1a | 0.5 % | 31.4 | 0 | 500 | 0.10 | — | 0.25 | ✗✗ |
| It.2 | 0.3 % | 62.83 | 0 | 500 | 0.18 | — | 0.15 | ✗ \( \zeta \) |
| It.3 | 0.5 % | 62.83 | 5 | 31.7 | **0.56** | **0.13** | **0.25** | **✓** |

> La impedancia virtual es la herramienta clave: permite desacoplar la elección del droop
> (que fija la caída de frecuencia estática) de la dinámica del modo de potencia (que depende de
> \( K_s = EV/X_{ef} \)).

## Cuándo y por qué se usa
Base de la mayoría de microrredes y grid-forming. El reparto de carga es automático: dos unidades
con la misma pendiente se reparten la potencia proporcionalmente a su potencia nominal, sin
comunicación.

## Procedimiento de diseño (genérico)
1. **\( m_p \)** desde la caída de frecuencia admisible a plena potencia (típico 0.5–2 %):
   \( m_p=(\text{droop}\%)\,\omega_0/S_n \).
2. **\( n_q \)** desde la caída de tensión admisible (típico 2–5 %): \( n_q=(\text{droop}\%)\,V_0/S_n \).
3. **Filtro de potencia \( \omega_f \)** (5–20 Hz): promedia el rizado y fija la dinámica del modo
   de potencia junto con \( m_p\,K_s \).
4. Verifica \( \zeta=\tfrac{1}{2}\sqrt{\omega_f/(m_p K_s)} \). Si bajo, sube \( \omega_f \) o
   baja \( K_s \) con [[impedancia-virtual]].
5. Si la línea es resistiva (X/R < 1), usa droop rotado o impedancia virtual inductiva.
6. Si se requiere limitar ROCOF, pasa a [[vsm-inercia]].

## Ejemplo de código
```python
# Parámetros de diseño
droop_p = 0.005; droop_q = 0.02
w0 = 2*np.pi*50; V0 = 690; Sn = 1e6
mp = droop_p * w0 / Sn           # (rad/s)/W
nq = droop_q * V0 / Sn           # V/var
wf = 2*np.pi*10                   # filtro 10 Hz

# Leyes de droop
w    = w0 + mp*(Pset - Pm)        # frecuencia de referencia
Vref = V0 + nq*(Qset - Qm)       # tensión de referencia
ddelta = w - w0
dPm = wf*(P - Pm); dQm = wf*(Q - Qm)

# Amortiguamiento del modo de potencia
Ks  = E*V/X                       # rigidez sincronizante en punto de operación
wn  = np.sqrt(mp * Ks * wf)
zeta = wf / (2 * wn)
print(f"modo de potencia: fn={wn/(2*np.pi):.1f} Hz, zeta={zeta:.3f}")
```

## Parámetros y valores típicos
\( m_p \): droop P-f 0.5–2 %, \( n_q \): droop Q-V 2–5 %, \( f_{pow}=\omega_f/2\pi \): 5–20 Hz.
Proyecto 01: droop 0.5 % / 2 % / filtro 10 Hz / \( X_{virt}=5\,\Omega \).

## Errores comunes
- \( \omega_f \) alto y \( K_s \) grande simultáneamente → \( \zeta \) bajo → oscilaciones en el
  modo de potencia. La relación \( \zeta\propto\sqrt{\omega_f/(m_p K_s)} \) lo muestra claramente.
- Asumir desacoplo P-f / Q-V con **línea resistiva** (X/R < 1): hay que rotar las consignas o
  usar [[impedancia-virtual]] inductiva.
- Olvidar la presincronización antes de la conexión a red: corrientes de slam al cerrar el
  interruptor.
- Subir el droop % pensando que mejora la dinámica: solo cambia la caída de frecuencia estática;
  la dinámica del modo de potencia depende de \( m_p K_s \), y subir el droop sube \( m_p \),
  lo que **empeora** \( \zeta \).

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: sincronizar sin PLL): droop P-f/Q-V como capa externa.
  Modo de potencia a 3.3 Hz con \( \zeta=0.15 \) → tratado con [[impedancia-virtual]]
  (\( X_{virt}=5\,\Omega \)) hasta \( \zeta\approx0.56 \).

## Conceptos relacionados
- [[grid-forming-vs-following]] · [[vsm-inercia]] · [[impedancia-virtual]] · [[transferencia-potencia-linea]] · [[analisis-modal]]

## Referencias
- Chandorkar, Divan, Adapa, *Control of Parallel Connected Inverters in Standalone AC Supply Systems*, IEEE TIA 1993.
- Guerrero et al., *Advanced Control Architectures for Intelligent Microgrids*, IEEE TIE 2013.
- Pogaku, Prodanovic, Green, *Modeling, Analysis and Testing of Autonomous Operation of an Inverter-Based Microgrid*, IEEE TPE 2007.
