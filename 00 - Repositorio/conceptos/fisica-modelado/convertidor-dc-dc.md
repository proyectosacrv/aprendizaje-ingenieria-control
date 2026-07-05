---
titulo: Convertidor DC-DC (buck / boost)
slug: convertidor-dc-dc
categoria: fisica-modelado
tipo: concepto
nivel: basico
proyectos: [03-DataCenter-IA]
objetivos: [entender la célula básica de conversión DC y el origen de la carga CPL]
tags: [dc-dc, buck, boost, duty, conmutado, espacio-estados, CPL, control-corriente, bidireccional, basico]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-07-03
relacionados: [dinamica-bus-dc, control-tension-bus-dc, fotovoltaica-mppt, convertidor-vsc]
referencias:
  - "Erickson & Maksimovic, Fundamentals of Power Electronics"
  - "Mohan, Undeland, Robbins, Power Electronics, Wiley"
---

## Definición
Convierte un nivel de tensión continua en otro, controlando el **ciclo de trabajo** \( D \) (fracción
del periodo en que el interruptor conduce). El **buck** reduce la tensión, el **boost** la eleva.
El **convertidor bidireccional** permite flujo de energía en ambos sentidos y es la base del BESS.

## Fundamento teórico
En régimen permanente, el balance volt-segundo en el inductor (su tensión media es cero) da las
relaciones de conversión en conducción continua (CCM):
$$ \text{Buck:}\quad V_o = D\,V_{in}, \qquad \text{Boost:}\quad V_o = \frac{V_{in}}{1-D} $$
La corriente de entrada/salida cumple el balance de potencia \( V_{in}I_{in}=V_o I_o \) (ideal). El
inductor y el condensador filtran el rizado; si la corriente del inductor llega a cero aparece la
**conducción discontinua** (DCM), con otras relaciones. El control regula \( V_o \) ajustando \( D \)
con un lazo (a menudo en cascada: tensión externa, corriente interna).

<div class="cfig"><img src="figuras/convertidor-dc-dc-ratio.png" alt="relacion de conversion buck y boost"><div class="cap">Relación de conversión en CCM: el buck reduce la tensión (Vo/Vin=D) y el boost la eleva (1/(1−D)). El control ajusta D para regular Vo.</div></div>

## 1 — Ganancia del buck \( V_o=D\,V_{in} \) por balance voltios-segundo

**Paso 1 — el principio.** En régimen permanente la corriente media del inductor no cambia de un ciclo al siguiente, luego su tensión media en un periodo es cero: \( \langle v_L\rangle=\frac1T\int_0^T v_L\,dt=0 \). Equivale a decir que el área voltios-segundo en el subintervalo de conducción cancela exactamente la del subintervalo de bloqueo.

**Paso 2 — las dos fases del buck.** El inductor une el nudo de conmutación con la salida \( V_o \).
- Interruptor cerrado (fracción \( D\,T \)): el nudo está a \( V_{in} \), así que \( v_L=V_{in}-V_o \).
- Interruptor abierto (fracción \( (1-D)\,T \)): el diodo conduce y el nudo está a \( 0 \), así que \( v_L=-V_o \).

**Paso 3 — igualar el área a cero.**

$$ (V_{in}-V_o)\,D\,T+(-V_o)\,(1-D)\,T=0 $$

Dividiendo por \( T \) y desarrollando:

$$ D\,V_{in}-D\,V_o-V_o+D\,V_o=0\;\Longrightarrow\;D\,V_{in}-V_o=0 $$

(los términos \( \pm D V_o \) se cancelan). Despejando:

$$ \boxed{\;V_o=D\,V_{in}\;} $$

Como \( 0\le D\le1 \), el buck siempre **reduce** la tensión. Con \( V_{in}=400 \) y \( D=0.5 \) da \( V_o=200\,\text{V} \).

## 2 — Ganancia del boost \( V_o=V_{in}/(1-D) \) por balance voltios-segundo

**Paso 1 — las dos fases del boost.** Ahora el inductor está entre la entrada \( V_{in} \) y el nudo de conmutación.
- Interruptor cerrado (\( D\,T \)): el inductor se conecta a tierra, \( v_L=V_{in} \) (se carga).
- Interruptor abierto (\( (1-D)\,T \)): el inductor descarga hacia la salida a través del diodo, \( v_L=V_{in}-V_o \).

**Paso 2 — balance voltios-segundo.**

$$ V_{in}\,D\,T+(V_{in}-V_o)\,(1-D)\,T=0 $$

Dividiendo por \( T \) y agrupando los términos en \( V_{in} \):

$$ V_{in}\big[D+(1-D)\big]-V_o\,(1-D)=0\;\Longrightarrow\;V_{in}-V_o\,(1-D)=0 $$

(\( D+(1-D)=1 \)). Despejando:

$$ \boxed{\;V_o=\frac{V_{in}}{1-D}\;} $$

Como \( 1-D<1 \), el boost siempre **eleva** la tensión, y diverge cuando \( D\to1 \). Con \( V_{in}=400 \) y \( D=0.5 \): \( V_o=800\,\text{V} \).

## 3 — El modelo en espacio de estados del buck (promediado)

El modelo promediado elimina la conmutación y reemplaza el interruptor por su valor medio \( D \). Los dos estados del buck en CCM son la corriente del inductor \( i_L \) y la tensión del condensador \( v_C \) (que es la salida \( v_o \)).

**Paso 1 — ecuaciones en el subintervalo ON (\( 0<t<DT \), interruptor cerrado).**

El inductor ve \( V_{in}-v_C \) y la carga pasiva:
$$ L\,\dot{i}_L = V_{in} - v_C - i_L\,r_L \approx V_{in} - v_C,\qquad C\,\dot{v}_C = i_L - \frac{v_C}{R} $$

(se desprecia \( r_L \) para simplificar). Matricialmente:
$$ \dot{\mathbf{x}} = \mathbf{A}_1\mathbf{x}+\mathbf{B}_1 u,\quad \mathbf{A}_1=\begin{bmatrix}0 & -1/L \\ 1/C & -1/(RC)\end{bmatrix},\quad \mathbf{B}_1=\begin{bmatrix}1/L \\ 0\end{bmatrix} $$

**Paso 2 — ecuaciones en el subintervalo OFF (\( DT<t<T \), interruptor abierto, diodo conduce).**

Ahora el nudo de conmutación está a tierra (\( v_{sw}=0 \)); la única diferencia con ON es que la entrada \( V_{in} \) desaparece de \( \dot{i}_L \):
$$ L\,\dot{i}_L = -v_C,\qquad C\,\dot{v}_C = i_L - \frac{v_C}{R} $$
$$ \mathbf{A}_2=\begin{bmatrix}0 & -1/L \\ 1/C & -1/(RC)\end{bmatrix}=\mathbf{A}_1,\qquad \mathbf{B}_2=\begin{bmatrix}0 \\ 0\end{bmatrix} $$

Para el buck, \( \mathbf{A}_1=\mathbf{A}_2 \), de modo que la matriz dinámica no cambia con el estado del interruptor; solo cambia la entrada.

**Paso 3 — promediar: \( \mathbf{A}_{avg}=D\,\mathbf{A}_1+(1-D)\,\mathbf{A}_2 \).**

$$ \mathbf{A}_{avg}=D\begin{bmatrix}0 & -1/L \\ 1/C & -1/(RC)\end{bmatrix}+(1-D)\begin{bmatrix}0 & -1/L \\ 1/C & -1/(RC)\end{bmatrix}=\begin{bmatrix}0 & -1/L \\ 1/C & -1/(RC)\end{bmatrix} $$

La entrada promediada: \( \mathbf{B}_{avg}\,u = D\,\mathbf{B}_1\,V_{in}+(1-D)\,\mathbf{B}_2\,V_{in}=D\,V_{in}/L\cdot\hat{e}_1 \). Reuniendo:

$$ \boxed{\;\dot{\mathbf{x}} = \begin{bmatrix}0 & -1/L \\ 1/C & -1/(RC)\end{bmatrix}\mathbf{x}+\begin{bmatrix}D/L \\ 0\end{bmatrix}V_{in}\;} $$

El punto de operación en régimen permanente sale de \( \dot{\mathbf{x}}=0 \): \( I_L=V_o/R \), \( V_C=D\,V_{in} \), que coincide con el balance voltios-segundo del §1.

## 4 — La función de transferencia control-salida \( G_{vd}(s) \)

Linealizando el modelo promediado alrededor de \( (D_0,V_{in}) \) se obtiene la dinámica de pequeña señal entre la perturbación de ciclo de trabajo \( \hat{d} \) y la tensión de salida \( \hat{v}_C \).

**Paso 1 — linealizar la ecuación de entrada.** El término de entrada es \( D\,V_{in}/L \). Al perturbar \( D=D_0+\hat{d} \):
$$ \frac{(D_0+\hat{d})V_{in}}{L}=\underbrace{\frac{D_0 V_{in}}{L}}_{\text{régimen permanente}}+\underbrace{\frac{V_{in}}{L}\hat{d}}_{\text{pequeña señal}} $$

**Paso 2 — modelo de pequeña señal.** Restando el régimen permanente:
$$ s\,\hat{\mathbf{x}}=\mathbf{A}\hat{\mathbf{x}}+\begin{bmatrix}V_{in}/L \\ 0\end{bmatrix}\hat{d} $$

Despejando \( \hat{\mathbf{x}}=(sI-\mathbf{A})^{-1}\mathbf{B}_d\,\hat{d} \). La salida \( \hat{v}_C=\mathbf{C}\hat{\mathbf{x}} \) con \( \mathbf{C}=[0,\,1] \):
$$ G_{vd}(s)=\mathbf{C}(sI-\mathbf{A})^{-1}\mathbf{B}_d $$

**Paso 3 — calcular \( (sI-\mathbf{A})^{-1} \).** La matriz característica es:
$$ sI-\mathbf{A}=\begin{bmatrix}s & 1/L \\ -1/C & s+1/(RC)\end{bmatrix} $$

Determinante: \( \Delta(s)=s^2+s/(RC)+1/(LC) \). Adjunta transpuesta:
$$ (sI-\mathbf{A})^{-1}=\frac{1}{\Delta(s)}\begin{bmatrix}s+1/(RC) & -1/L \\ 1/C & s\end{bmatrix} $$

**Paso 4 — extraer \( G_{vd}(s) \).**
$$ G_{vd}(s)=[0,1]\cdot\frac{1}{\Delta(s)}\begin{bmatrix}s+1/(RC) & -1/L \\ 1/C & s\end{bmatrix}\cdot\begin{bmatrix}V_{in}/L \\ 0\end{bmatrix}=\frac{V_{in}/LC}{\Delta(s)} $$

Normalizando con \( \omega_n^2=1/(LC) \) y \( 2\zeta\omega_n=1/(RC) \):

$$ \boxed{\;G_{vd}(s)=\frac{V_{in}\,\omega_n^2}{s^2+2\zeta\omega_n\,s+\omega_n^2},\quad \omega_n=\frac{1}{\sqrt{LC}},\quad \zeta=\frac{1}{2R}\sqrt{\frac{L}{C}}\;} $$

Con \( L=200\,\mu\text{H} \), \( C=200\,\mu\text{F} \), \( R=\approx2.3\,\Omega \) (\( P=500\,\text{W} \), \( V_o=24\,\text{V} \)):
\( \omega_n=2\pi\times796\,\text{rad/s} \), \( \zeta=0.12 \) → subamortiguado, resonancia pronunciada en la Bode.

## 5 — El cero en el semiplano derecho del boost (RHP zero)

El boost tiene una dinámica de no fase mínima que limita el ancho de banda del lazo de tensión. Este cero en el semiplano derecho (RHP) es una consecuencia directa de la estructura del circuito.

**Paso 1 — modelo de pequeña señal del boost.** El inductor del boost se carga durante ON y descarga hacia la salida durante OFF (al revés que en el buck). La dinámica de la corriente del inductor:
$$ L\,\dot{\hat{i}}_L = V_{in}\hat{d}\cdot0+\text{...} $$

El modelo estándar del boost, aplicando el mismo procedimiento de promediado que en §3:
$$ \hat{v}_C: \quad C\,\dot{\hat{v}}_C = (1-D)\hat{i}_L - \frac{\hat{v}_C}{R} - I_L\hat{d} $$

El término \( -I_L\hat{d} \) introduce un **cero en el numerador** de la función de transferencia.

**Paso 2 — la función de transferencia del boost.** Aplicando las transformadas de Laplace a las ecuaciones de pequeña señal:
$$ \hat{v}_C(s)\left(sC+\frac{1}{R}\right)=(1-D)\hat{i}_L - I_L\hat{d} $$
$$ \hat{i}_L = \frac{V_{in}\hat{d}+\hat{v}_C(1-D)}{sL} \;\text{(resolviendo el sistema)} $$

Sustituyendo y despejando \( G_{vd}^{boost}(s)=\hat{v}_C/\hat{d} \):
$$ \boxed{\;G_{vd}^{boost}(s)=\frac{V_{in}}{(1-D)^2}\cdot\frac{1-s\,L/(R(1-D)^2)}{s^2LC/(1-D)^2+sL/(R(1-D)^2)+1}\;} $$

**Paso 3 — el RHP zero.** El numerador tiene la forma \( (1-s\tau_z) \) con:
$$ \tau_z = \frac{L}{R(1-D)^2}\;\Longrightarrow\;s_z=\frac{R(1-D)^2}{L} $$

Este cero está en \( s_z>0 \) (semiplano derecho). Su efecto en la respuesta en frecuencia: la magnitud cae (-20 dB/dec desde \( f_z \)) pero la **fase sigue bajando** (en lugar de subir como en un cero de fase mínima). El cero del RHP limita el BW del lazo de tensión a no más de un tercio de \( f_z \):
$$ f_{z,boost}=\frac{R(1-D)^2}{2\pi L} $$

Para el boost 48 V → 400 V con \( D=0.88 \), \( R=400^2/10000=16\,\Omega \), \( L=100\,\mu\text{H} \):
\( f_z=16\times0.0144/(2\pi\times10^{-4})\approx367\,\text{Hz} \) → el BW del lazo de tensión debe limitarse a ~100 Hz.

## 6 — Diseño iterativo: buck 48 V → 24 V, 500 W

**Especificaciones:** \( V_{in}=48\,\text{V} \), \( V_o=24\,\text{V} \), \( P=500\,\text{W} \), \( L=200\,\mu\text{H} \), \( C=200\,\mu\text{F} \), \( f_{sw}=50\,\text{kHz} \).

**Paso 1 — ciclo de trabajo y punto de operación.**
$$ D=\frac{V_o}{V_{in}}=\frac{24}{48}=0.5,\qquad I_o=\frac{P}{V_o}=\frac{500}{24}=20.8\,\text{A},\qquad R=\frac{V_o}{I_o}=\frac{24}{20.8}=1.15\,\Omega $$

**Paso 2 — parámetros del modelo de segundo orden.**
$$ \omega_n=\frac{1}{\sqrt{LC}}=\frac{1}{\sqrt{200\times10^{-6}\times200\times10^{-6}}}=5000\,\text{rad/s}\;\;(f_n=796\,\text{Hz}) $$
$$ \zeta=\frac{1}{2R}\sqrt{\frac{L}{C}}=\frac{1}{2\times1.15}\sqrt{\frac{200\times10^{-6}}{200\times10^{-6}}}=\frac{1}{2\times1.15}=0.435 $$

**Paso 3 — PM del lazo de tensión sin compensar.** El lazo de tensión puro (ganancia unitaria de sensor, sin PI) cruza 0 dB a la frecuencia donde \( |G_{vd}(j\omega)|=1 \). Numéricamente, con \( G_{vd}(j\omega)=V_{in}\omega_n^2/\sqrt{(\omega_n^2-\omega^2)^2+(2\zeta\omega_n\omega)^2} \):

En el cruce a ~440 Hz la fase es aproximadamente \( -137° \) → PM ≈ 43°. Ligeramente bajo del objetivo de 45°, y sin amoriguamiento extra en el error de régimen no eliminado.

**Paso 4 — PI para PM ≥ 45°.** Un PI con frecuencia del zero en \( f_z=\omega_n/(2\pi)/5\approx160\,\text{Hz} \):
$$ C_{PI}(s)=K_p\frac{s+\omega_z}{s},\qquad \omega_z=2\pi\times160\approx1005\,\text{rad/s} $$
Se elige \( K_p \) para que el cruce de ganancia del lazo total sea a 400–500 Hz, obteniendo PM ≈ 48–52°.

**Verificación:** rizado de corriente en \( L \):
$$ \Delta i_L=\frac{(V_{in}-V_o)\,D}{L\,f_{sw}}=\frac{24\times0.5}{200\times10^{-6}\times50\times10^{3}}=1.2\,\text{A}\;\;(<6\%\text{ de }I_o) $$

Rizado de tensión: \( \Delta v_C=\Delta i_L/(8\,C\,f_{sw})=1.2/(8\times200\times10^{-6}\times50000)=15\,\text{mV}\;\;(<0.1\%) \).

<div class="cfig"><img src="../figuras/convertidor-dc-dc-analisis.png" alt="4 paneles: Bode Gvd buck, RHP zero boost, rizado iL y vC, diseño iterativo PM vs PI"><div class="cap">
(a) Bode de \(G_{vd}(s)\) del buck para R=1 Ω, 2 Ω, 5 Ω: el pico de resonancia se amortigua con más carga; (b) cero RHP del boost \(f_z\) vs D: a D=0.88 la frecuencia del cero cae por debajo de 400 Hz, limitando el BW; (c) rizado de \(i_L\) y \(v_C\) en función de L y C para el buck 48→24 V; (d) PM del lazo de tensión vs ganancia \(K_p\) del PI: el margen cruza 45° al aumentar \(K_p\).
</div></div>

## 7 — El boost con carga de potencia constante (CPL)

Una carga regulada que mantiene potencia constante \( P=V_{out}\cdot I_{out} \) presenta, vista desde el bus, una **resistencia incremental negativa**:

**Paso 1 — resistencia dinámica.** Derivando \( I=P/V \) respecto a \( V \):
$$ \frac{dI}{dV}=-\frac{P}{V^2}=-\frac{1}{R_{CPL}} $$

donde \( R_{CPL}=V^2/P \) es **negativa** (corriente disminuye si la tensión sube, al revés que una resistencia pasiva).

**Paso 2 — desamortiguamiento del condensador de bus.** El condensador \( C \) del bus DC ve la resistencia total \( R_{total}=R_{par}\,\|R_{CPL} \). Con \( R_{par}>0 \) y \( R_{CPL}<0 \):
$$ \frac{1}{R_{total}}=\frac{1}{R_{par}}-\frac{1}{R_{CPL}} $$

Si \( R_{CPL} < R_{par} \) en módulo, la parte real del polo del condensador se hace positiva → **inestabilidad**.

**Paso 3 — potencia crítica.** La condición de margen (\( R_{total}\to\infty \)) da:
$$ \boxed{\;P_{crit}=\frac{V_{out}^2\,R_{par}}{L}\;} $$

Para un boost con \( L=0.5\,\text{mH} \), \( R_{par}=0.1\,\Omega \), \( V_{out}=400\,\text{V} \): \( P_{crit}=32\,\text{kW} \). Si la CPL absorbe más de ese valor, el sistema es inestable sin amortiguamiento adicional (activo o pasivo) en el bus DC.

## 8 — Control en modo corriente: lazo interno + lazo externo

El control en modo corriente pico (o promedio) añade un lazo interno que realimenta \( i_L \) directamente, consiguiendo dos ventajas: la limitación intrínseca de corriente (protección natural) y la conversión del inductor en una fuente de corriente controlada, simplificando el lazo externo de tensión a un primer orden.

**Paso 1 — lazo interno de corriente.** La planta del lazo de corriente es:
$$ G_{id}(s)=\frac{\hat{i}_L}{\hat{u}}=\frac{1}{sL+R} $$
Un PI con ganancia \( K_p = \alpha_c L \), \( K_i = \alpha_c R \) (IMC, ancho de banda \( \alpha_c \)) cierra el lazo: la función lazo abierto es \( L_{cc}(s)=K_p(1+K_i/s)\cdot G_{id}(s)\cdot R_s \) donde \( R_s \) es la ganancia del sensor de corriente. El lazo interno se sintoniza típicamente a \( \alpha_c = 2\pi\cdot f_{sw}/10 \).

**Paso 2 — lazo externo de tensión.** Con el lazo de corriente cerrado, el inductor se convierte en una fuente de corriente controlada. El lazo externo ve la planta:
$$ G_{vc}(s)=\frac{\hat{v}_C}{\hat{i}^*_L}=\frac{1}{sC+1/R} $$

Un PI externo más lento (factor 5–10 más lento que el interno) regula \( V_o \).

**Paso 3 — limitación intrínseca de corriente.** El lazo interno satura cuando la consigna \( i^* \) supera el límite hardware (comparador de corriente). Esto protege el semiconductor sin retardo: el convertidor pasa automáticamente a modo de corriente constante (CC) durante arranques y cortocircuitos, y la protección es puramente analógica, sin lógica software.

## 9 — El convertidor bidireccional para BESS

Un convertidor bidireccional buck-boost permite cargar y descargar la batería usando el mismo puente de semiconductores activos (sin diodo de rueda libre → ambos transistores activos). El flujo de energía depende de \( D \):

**Regla de flujo:**
- \( D > 0.5 \): la tensión de salida supera la mitad de \( V_{bus} \) → la energía fluye del bus a la batería (**carga**).
- \( D < 0.5 \): la tensión de salida cae por debajo de la mitad → la energía fluye de la batería al bus (**descarga**).
- \( D = 0.5 \): punto de equilibrio (sin flujo neto, solo rizado).

**Ecuación unificada.** En promedio, la tensión de la batería es:
$$ V_{bat} = D\,V_{bus}\quad\text{(buck en descarga)},\qquad V_{bus} = \frac{V_{bat}}{1-D}\quad\text{(boost en carga)} $$

El control del BMS ajusta \( D \) para seguir la referencia de corriente de batería \( i^*_{bat} \) (definida positiva en descarga), limitada por los umbrales de SoC y C-rate. El lazo interno de corriente es idéntico al de §5, solo cambia el signo de la consigna.

## 10 — Diseño iterativo: boost 48 V → 400 V, 10 kW

**Especificaciones:** \( V_{in}=48\,\text{V} \), \( V_o=400\,\text{V} \), \( P_{nom}=10\,\text{kW} \), \( f_{sw}=20\,\text{kHz} \), rizado de corriente \( \Delta I_L \le 20\,\% \) de \( I_{in} \), rizado de tensión \( \Delta V_o\le 1\,\% \).

**Paso 1 — ciclo de trabajo.** \( D=1-V_{in}/V_o=1-48/400=0.88 \).

**Paso 2 — corriente de entrada.** \( I_{in}=P/V_{in}=10000/48=208\,\text{A} \). Rizado permitido: \( \Delta I_L=0.2\times208=41.6\,\text{A} \).

**Paso 3 — inductancia mínima.**
$$ L_{min}=\frac{V_{in}\,D}{\Delta I_L\,f_{sw}}=\frac{48\times0.88}{41.6\times20000}\approx51\,\mu\text{H} $$
Se elige \( L=100\,\mu\text{H} \) (margen × 2 para variaciones de la red y CCM asegurado).

**Paso 4 — condensador de salida.** El rizado de tensión en el boost es \( \Delta V_o=D/(R\,C\,f_{sw}) \):
$$ C_{min}=\frac{D\,I_o}{\Delta V_o\,f_{sw}}=\frac{0.88\times25}{4\times20000}\approx275\,\mu\text{F} $$
Se elige \( C=470\,\mu\text{F} \) (valor estándar, \( \Delta V_o\approx0.6\,\% \)).

**Verificación de la CPL:** Con \( R_{par}=0.15\,\Omega \) (ESR del inductor + cableado) y \( L=100\,\mu\text{H} \):
\( P_{crit}=400^2\times0.15/100\times10^{-6}=240\,\text{kW}\gg10\,\text{kW} \). El sistema es inherentemente estable en estas condiciones.


## Cuándo y por qué se usa
Es la base de las fuentes conmutadas, del MPPT fotovoltaico, y de los **POL** (point-of-load) que
alimentan los servidores. Es clave entender que un DC-DC **regulado** que mantiene su potencia de
salida constante se comporta, visto desde su entrada, como una **carga de potencia constante (CPL)**
con resistencia incremental negativa.

## Procedimiento de diseño (genérico)
1. Elige topología según \( V_o/V_{in} \) (buck si \( <1 \), boost si \( >1 \), bidireccional si hay almacenamiento).
2. Fija \( f_{sw} \) y dimensiona \( L \) (por el rizado de corriente) y \( C \) (por el rizado de tensión).
3. Obtén el modelo promediado \( G_{vd}(s) \) y sintoniza el lazo de corriente (IMC).
4. Diseña el lazo externo de tensión con margen de fase ≥ 45°.
5. Verifica la estabilidad frente a CPL si el convertidor alimenta cargas reguladas.

## Ejemplo de código
```python
Vin, D = 400.0, 0.5
Vo_buck  = D*Vin                 # 200 V
Vo_boost = Vin/(1-D)             # 800 V
# Modelo promediado buck: G_vd
import numpy as np
from scipy import signal
L, C, R = 100e-6, 470e-6, 5.0
num = [Vin]; den = [L*C, L/R, 1.0]
sys_gvd = signal.TransferFunction(num, den)
```

## Parámetros y valores típicos
\( D \) entre 0.1 y 0.9 (extremos comprometen el control). \( f_{sw} \) de decenas de kHz a MHz según
potencia. Rizado de corriente del inductor objetivo ≈ 20–40 % de la nominal. Ancho de banda lazo de
corriente: \( f_{sw}/10 \). Ancho de banda lazo de tensión: factor 5–10 menor que el de corriente.

## Errores comunes
- Confundir las relaciones de buck y boost (o ignorar pérdidas que las modifican).
- Operar muy cerca de \( D=0 \) o \( D=1 \) (mal condicionado).
- No reconocer que el lazo de regulación crea el comportamiento CPL (desamortigua el bus que lo alimenta).
- Sintonizar el lazo de corriente sin tener en cuenta la resonancia del modelo promediado.

## 11 — Eigenvalores del modelo promediado: frecuencia natural y amortiguamiento

El modelo promediado del buck en espacio de estados tiene la matriz dinámica:
$$ \mathbf{A} = \begin{bmatrix}0 & -1/L \\ 1/C & -1/(RC)\end{bmatrix} $$
Los eigenvalores determinan la estabilidad y la respuesta transitoria del convertidor.

**Paso 1 — polinomio característico.** \(\det(sI - \mathbf{A}) = 0\):
$$ s^2 + \frac{1}{RC}\,s + \frac{1}{LC} = 0 $$

**Paso 2 — identificar \(\omega_n\) y \(\zeta\).** Comparando con la forma estándar \(s^2 + 2\zeta\omega_n s + \omega_n^2\):
$$ \boxed{\;\omega_n = \frac{1}{\sqrt{LC}},\qquad \zeta = \frac{1}{2R}\sqrt{\frac{L}{C}}\;} $$

**Paso 3 — raíces.** \(s_{1,2} = -\zeta\omega_n \pm \omega_n\sqrt{\zeta^2 - 1}\). Para \(\zeta < 1\) (caso habitual en convertidores de potencia donde la carga es grande):
$$ s_{1,2} = -\zeta\omega_n \pm j\,\omega_n\sqrt{1 - \zeta^2} $$
Par conjugado en el semiplano izquierdo → sistema estable con respuesta oscilatoria subamortiguada.

**Paso 4 — ejemplo numérico.** Buck 48→24 V con \(L=200\,\mu\text{H}\), \(C=200\,\mu\text{F}\), \(R=1.15\,\Omega\):
$$ \omega_n = \frac{1}{\sqrt{200 \times 10^{-6} \times 200 \times 10^{-6}}} = 5000\,\text{rad/s}\quad(f_n = 796\,\text{Hz}) $$
$$ \zeta = \frac{1}{2 \times 1.15}\sqrt{\frac{200\times10^{-6}}{200\times10^{-6}}} = 0.435 $$
Los eigenvalores están en \(s_{1,2} = -2175 \pm j4441\,\text{rad/s}\). La resonancia pronunciada en la Bode de \(G_{vd}\) aparece precisamente a \(f_n = 796\,\text{Hz}\), donde el denominador tiene su mínimo.

**Punto a resaltar.** Cargas más ligeras (mayor \(R\)) reducen \(\zeta\) → más resonancia; cargas pesadas (menor \(R\)) amortiguan. Un convertidor en vacío puede ser muy subamortiguado y difícil de compensar.

## 12 — Control en modo corriente: lazo interno + lazo externo

La cascada tensión-corriente convierte el inductor, que en el lazo de tensión simple es un elemento de segundo orden, en una fuente de corriente controlada de primer orden. Esto simplifica el diseño y permite protección intrínseca de sobrecorriente.

**Paso 1 — planta del lazo interno de corriente.** La corriente del inductor responde a la tensión aplicada como:
$$ G_{id}(s) = \frac{\hat{i}_L}{\hat{u}} = \frac{1/L}{s + R/L} \approx \frac{1}{sL} \quad(R \ll \omega L) $$
La función de transferencia entrada de control → corriente es un integrador con polo en \(-R/L\).

**Paso 2 — sintonía IMC del lazo de corriente.** Con un PI de parámetros \(K_{p,i} = \alpha_c L\), \(K_{i,i} = \alpha_c R\) (cancelación del polo):
$$ L_{cc}(s) = K_{p,i}\!\left(1 + \frac{K_{i,i}/K_{p,i}}{s}\right)\!\cdot G_{id}(s) = \frac{\alpha_c\,L}{L}\cdot\frac{s + R/L}{s}\cdot\frac{1/L}{s + R/L} = \frac{\alpha_c}{s} $$
El lazo cerrado de corriente tiene función de transferencia \(T_{cc}(s) = \alpha_c/(s + \alpha_c)\): primer orden con \(\text{BW} = \alpha_c\). Típicamente \(\alpha_c = \omega_{sw}/10 = 2\pi f_{sw}/10\).

**Paso 3 — separación de escalas temporales.** Con el lazo de corriente cerrado, la corriente sigue \(i_L \approx i_L^*\) hasta la frecuencia \(\alpha_c\). El lazo externo de tensión ve:
$$ G_{vc}(s) = \frac{\hat{v}_C}{\hat{i}_L^*} = \frac{1/C}{s + 1/(RC)} $$
Primer orden puro. El lazo externo se sintoniza con BW \(\alpha_v = \alpha_c/5\ldots10\).

**Paso 4 — margen de fase en ambos lazos.** Con plantas de primer orden y PI, el PM es:
$$ \text{PM} = 90° - \arctan\!\left(\frac{\alpha}{|\omega_z|}\right) + \arctan\!\left(\frac{\alpha}{|\omega_z|}\right) \approx 72\text{°–}80\text{°} $$
(muy robusto por la cancelación del polo). La condición crítica es \(\alpha_v \ll \alpha_c\); si el lazo externo intenta ser tan rápido como el interno, la aproximación \(i_L \approx i_L^*\) deja de ser válida y el sistema puede oscilar.

**Limitación intrínseca de corriente.** La referencia \(i_L^*\) se satura en un límite hardware antes de enviarse al lazo interno. Cuando \(v_o < v_o^*\) (arranca o cortocircuito), el lazo de tensión pide más corriente de la que puede entregar; la saturación fija \(i_L^* = I_{max}\) y el convertidor opera en modo corriente constante (CC) de forma automática, sin lógica de supervisión.

## 13 — Carga CPL y estabilidad del bus DC

Una carga de potencia constante (CPL) presenta impedancia de entrada negativa a pequeña señal: cuando la tensión del bus sube, la corriente baja para mantener \(P = VI\) constante. Esto puede desestabilizar el bus.

**Paso 1 — impedancia incremental negativa.** Sea \(P = V \cdot I = \text{cte}\). La perturbación de corriente ante una perturbación de tensión:
$$ \frac{d I}{d V} = -\frac{P}{V^2} = -\frac{1}{R_{CPL}},\qquad R_{CPL} \equiv \frac{V^2}{P} > 0 $$
La resistencia incremental es \(-R_{CPL}\): **negativa**. En el modelo de pequeña señal del bus, la CPL aparece como una resistencia negativa en paralelo con el condensador de bus.

**Paso 2 — desamortiguamiento del condensador.** El polo del condensador de bus \(C_{bus}\) con resistencia de amortiguamiento \(R_{par}\) y CPL en paralelo:
$$ s_{polo} = -\frac{1}{C_{bus}}\!\left(\frac{1}{R_{par}} - \frac{1}{R_{CPL}}\right) $$
Si \(R_{CPL} < R_{par}\) (CPL domina), la parte real del polo es positiva → **inestabilidad**.

**Paso 3 — criterio de estabilidad en frecuencia.** Más general: la impedancia de salida del convertidor fuente \(Z_o(j\omega)\) debe ser menor que la impedancia de entrada de la CPL \(|Z_{CPL}|\) en toda frecuencia (criterio de Middlebrook):
$$ \|Z_o\|_\infty < |Z_{CPL}| = \frac{V^2}{P} $$

**Paso 4 — múltiples CPL en paralelo.** Si hay \(N\) cargas CPL de potencias \(P_1, \ldots, P_N\) en el mismo bus, sus conductancias negativas se suman:
$$ \frac{1}{R_{CPL,total}} = \sum_{k=1}^N \frac{P_k}{V^2} = \frac{P_{total}}{V^2} $$
En buses DC de data center con decenas de servidores (cada uno con su fuente regulada), \(P_{total}\) puede ser enorme y \(R_{CPL,total}\) muy pequeño → alto riesgo.

**Mitigaciones.** Damping virtual (resistencia activa en paralelo con el condensador mediante realimentación de corriente), control de tensión de bus con droop (limita la respuesta a la CPL), o condensador de bus sobredimensionado para reducir la ganancia a baja frecuencia.

## 14 — Dimensionado de L y C: criterios y tabla de ejemplo

El inductor y el condensador definen el rizado de señales y los eigenvalores del modelo. Hay criterios bien establecidos para cada topología.

**Rizado de corriente en el inductor (buck).** Durante el intervalo ON el inductor se carga con \(V_{in} - V_o\) durante \(DT_s\):
$$ \Delta i_L = \frac{(V_{in} - V_o)\,D}{f_s\,L} = \frac{V_{in}\,D\,(1-D)}{f_s\,L} $$
donde se usó \(V_o = D\,V_{in}\). El rizado es máximo en \(D = 0.5\): \(\Delta i_{L,max} = V_{in}/(4 f_s L)\).

**Criterio de diseño:** \(\Delta i_L < 30\,\%\,I_L\) (límite de CCM con margen). Despejando:
$$ L_{min} = \frac{V_{in}\,D\,(1-D)}{0.3\,I_L\,f_s} $$

**Rizado de tensión en el condensador (buck).** El rizado de \(v_C\) depende del rizado de \(i_L\) que carga/descarga el condensador durante medio periodo:
$$ \Delta v_C = \frac{\Delta i_L}{8\,f_s\,C} $$

**Criterio de diseño:** \(\Delta v_C < 1\,\%\,V_o\). Despejando:
$$ C_{min} = \frac{\Delta i_L}{8\,f_s \times 0.01\,V_o} $$

**Tabla de ejemplo:** \(V_{in}=400\,\text{V}\), \(V_o=200\,\text{V}\), \(P=10\,\text{kW}\), \(f_s=20\,\text{kHz}\), \(D=0.5\):

| Parámetro | Cálculo | Valor elegido |
|---|---|---|
| \(I_L = P/V_o\) | 50 A | — |
| \(L_{min}\) | \(400 \times 0.5 \times 0.5 / (0.3 \times 50 \times 20000)\) | \(\approx 333\,\mu\text{H}\) → elegir **500 µH** |
| \(\Delta i_L\) a \(L=500\,\mu\text{H}\) | \(400 \times 0.5 \times 0.5 / (20000 \times 500\text{e-6})\) | **10 A** (20 %) |
| \(C_{min}\) | \(10 / (8 \times 20000 \times 2)\) | \(\approx 31\,\mu\text{F}\) → elegir **100 µF** |
| \(\Delta v_C\) a \(C=100\,\mu\text{F}\) | \(10 / (8 \times 20000 \times 100\text{e-6})\) | **0.625 V** (0.31 %) |

<div class="cfig"><img src="../figuras/convertidor-dc-dc-analisis.png" alt="4 paneles: rizado iL, ganancia buck y boost, Bode lazo corriente, criterio estabilidad CPL"><div class="cap">
(a) Rizado de \(i_L\) en el buck con \(D=0.6\): la corriente sube lineal durante ON y baja durante OFF; la media (rojo) es la corriente de carga. (b) Ganancia de conversión del buck (\(V_o/V_{in}=D\)) y boost (\(1/(1-D)\)): el boost diverge cuando \(D \to 1\). (c) Bode del lazo de corriente \(G_{il}(j\omega)\): pendiente \(-20\,\text{dB/dec}\) con cruce natural determinado por \(R/L\). (d) Criterio de estabilidad CPL: la impedancia de salida \(|Z_o|\) debe quedar por debajo de \(|Z_{CPL}|\) (línea roja) en toda la banda para garantizar margen estable (zona verde).
</div></div>

## Uso en proyectos
- **03 - DataCenter-IA:** los servidores (POL DC-DC regulados) se modelan como CPL en el bus DC; su resistencia negativa es la causa de la inestabilidad estudiada.

## Conceptos relacionados
- [[dinamica-bus-dc]] · [[control-tension-bus-dc]] · [[fotovoltaica-mppt]] · [[convertidor-vsc|modelo promediado]]

## Referencias
- Erickson & Maksimovic, *Fundamentals of Power Electronics*.
- Mohan, Undeland, Robbins, *Power Electronics*, Wiley.
