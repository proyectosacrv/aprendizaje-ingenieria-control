---
titulo: Transformadas de Clarke y Park (marco αβ y dq)
slug: marco-dq
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [reducir las tres magnitudes trifásicas a dos ejes, llevar las senoides a continua y desacoplar el control]
tags: [clarke, park, alfa-beta, dq, transformada, acoplamiento, homopolar, trifasico, modelado, desacoplo, secuencia-negativa, dsogi]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [desacoplo-dq, potencia-instantanea-dq, componentes-simetricas, control-cascada, control-vectorial, filtro-lcl, pll-srf]
referencias:
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
  - "Akagi, Watanabe, Aredes, Instantaneous Power Theory, Wiley 2007"
  - "Teodorescu, Liserre, Rodriguez, Grid Converters for Photovoltaic and Wind Power Systems, Wiley 2011"
---

## Definición
Cadena de dos transformaciones que reducen las tres magnitudes trifásicas (abc) primero a dos ejes ortogonales estacionarios (αβ, transformada de Clarke) y luego a un marco giratorio sincronizado con la red (dq, transformada de Park). El resultado clave: en régimen permanente las senoides de 50 Hz se convierten en constantes, lo que permite usar PI con error nulo en continua y analizar el sistema trifásico como uno de continua. Esta ficha cubre las dos transformadas con derivaciones completas y el fenómeno del acoplamiento cruzado que origina la matriz \(\omega\mathbf{J}\).

## La idea en una figura

<div class="cfig"><img src="figuras/marco-dq-park.png" alt="senoides trifasicas que en dq se vuelven constantes"><div class="cap">Las tres senoides del marco abc (izquierda) se vuelven dos constantes en el marco dq (derecha): con el eje d alineado con la tensión, \(v_d\) es la amplitud y \(v_q\approx 0\).</div></div>

<div class="cfig"><img src="figuras/marco-dq-analisis.png" alt="Cuatro paneles: vector espacio en alfabeta, acoplamiento cruzado, desequilibrio y convenciones"><div class="cap">(a) Las tres senoides abc generan un vector espacio que traza un círculo en αβ; Park lo proyecta en el punto fijo dq. (b) Sin desacoplo, un escalón en \(v_d\) perturba también \(i_q\); con desacoplo los ejes son independientes. (c) Un desequilibrio del 10% aparece como oscilación a 100 Hz en dq. (d) Las dos convenciones dan valores numéricos distintos para la misma señal física.</div></div>

## 1 — De abc a αβ: la transformada de Clarke paso a paso

### Motivación: proyección ortogonal desde primeros principios

En un sistema trifásico equilibrado las tres fases suman cero en todo instante:
\(x_a(t) + x_b(t) + x_c(t) = 0\). Eso significa que los tres valores instantáneos solo tienen dos grados de libertad: basta con dos coordenadas para describir cualquier estado del sistema. Clarke construye esas dos coordenadas proyectando los tres fasores de fase sobre un par de ejes ortogonales fijos.

Los ejes de las tres fases apuntan en las direcciones (en el plano complejo):

$$\hat{e}_a = e^{j\cdot 0} = 1, \qquad \hat{e}_b = e^{-j2\pi/3}, \qquad \hat{e}_c = e^{+j2\pi/3}$$

El **vector espacio** se define como la suma ponderada de las contribuciones de cada fase proyectada sobre su eje:

$$\vec{x} = k\left(x_a\,\hat{e}_a + x_b\,\hat{e}_b + x_c\,\hat{e}_c\right)$$

donde \(k\) es un factor de escala que se fija según la convención elegida. Expandiendo la exponencial compleja de \(\hat{e}_b\) y \(\hat{e}_c\) en parte real e imaginaria:

$$\hat{e}_b = -\tfrac{1}{2} - j\tfrac{\sqrt{3}}{2}, \qquad \hat{e}_c = -\tfrac{1}{2} + j\tfrac{\sqrt{3}}{2}$$

La parte real del vector espacio es la componente α, y la parte imaginaria la componente β:

$$x_\alpha = k\!\left(x_a - \tfrac{1}{2}x_b - \tfrac{1}{2}x_c\right), \qquad x_\beta = k\!\left(\tfrac{\sqrt{3}}{2}x_b - \tfrac{\sqrt{3}}{2}x_c\right) = k\tfrac{\sqrt{3}}{2}\!\left(x_b - x_c\right)$$

La componente homopolar recoge el modo común:

$$x_0 = \tfrac{1}{3}\left(x_a + x_b + x_c\right)$$

En forma matricial (incluyendo el homopolar):

$$\begin{bmatrix}x_\alpha\\x_\beta\\x_0\end{bmatrix} = k\begin{bmatrix}1 & -\tfrac{1}{2} & -\tfrac{1}{2}\\0 & \tfrac{\sqrt{3}}{2} & -\tfrac{\sqrt{3}}{2}\\\tfrac{1}{3k} & \tfrac{1}{3k} & \tfrac{1}{3k}\end{bmatrix}\begin{bmatrix}x_a\\x_b\\x_c\end{bmatrix} \equiv \mathbf{T}_C\,\mathbf{x}_{abc}$$

El valor de \(k\) distingue las dos convenciones.

<div class="cfig"><img src="figuras/transformada-clarke-ejes.png" alt="ejes abc y alfa-beta de Clarke"><div class="cap">Clarke proyecta las tres fases (ejes a, b, c a 120°) sobre dos ejes ortogonales fijos: α (alineado con a) y β. Cualquier terna se reduce al vector espacial \(x = x_\alpha + jx_\beta\).</div></div>

### Por qué el homopolar es cero en un sistema equilibrado

En un sistema trifásico equilibrado la suma de las tres fases es idénticamente nula:

$$x_a + x_b + x_c = X_m\cos(\omega t) + X_m\cos\!\left(\omega t - \tfrac{2\pi}{3}\right) + X_m\cos\!\left(\omega t + \tfrac{2\pi}{3}\right)$$

Usando la identidad \(\cos\theta + \cos(\theta-\frac{2\pi}{3}) + \cos(\theta+\frac{2\pi}{3}) = 0\) (suma de exponenciales \(e^{j\theta}\), \(e^{j(\theta-2\pi/3)}\), \(e^{j(\theta+2\pi/3)}\) que son las tres raíces cúbicas de la unidad multiplicadas por \(e^{j\theta}\), y suman cero):

$$x_a + x_b + x_c = 0 \;\Rightarrow\; x_0 = \tfrac{1}{3}(x_a+x_b+x_c) = 0$$

El homopolar capta el modo común (desequilibrio de carga, corriente de neutro, armónico triplen). Con sistema equilibrado y sin neutro \(x_0=0\) exactamente y basta con el plano αβ.

### Las dos convenciones y cómo elegir

**Convención de amplitud invariante** (\(k = \frac{2}{3}\)):

$$\mathbf{T}_C^{amp} = \frac{2}{3}\begin{bmatrix}1 & -\frac{1}{2} & -\frac{1}{2}\\0 & \frac{\sqrt{3}}{2} & -\frac{\sqrt{3}}{2}\\\frac{1}{2} & \frac{1}{2} & \frac{1}{2}\end{bmatrix}$$

Con esta elección, si \(x_a = X_m\cos(\omega t)\) entonces \(x_\alpha = X_m\cos(\omega t)\): el pico de la fase se conserva en αβ. La inversa requiere multiplicar por \(\frac{3}{2}\).

**Convención de potencia invariante** (\(k = \sqrt{\frac{2}{3}}\)):

$$\mathbf{T}_C^{pot} = \sqrt{\frac{2}{3}}\begin{bmatrix}1 & -\frac{1}{2} & -\frac{1}{2}\\0 & \frac{\sqrt{3}}{2} & -\frac{\sqrt{3}}{2}\\\frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}}\end{bmatrix}$$

Con esta elección \(\mathbf{T}_C^{pot}\) es una matriz ortogonal (unitaria real): \(\left(\mathbf{T}_C^{pot}\right)^T \mathbf{T}_C^{pot} = \mathbf{I}\). Eso significa que la transformación conserva la norma, es decir, conserva la potencia instantánea directamente.

**Regla para elegir:** usar siempre la misma convención en todo el proyecto. La de amplitud invariante es la más común en control de convertidores porque las referencias dq (id\(^*\), iq\(^*\)) coinciden con las amplitudes de pico de las corrientes de fase. La de potencia invariante simplifica la fórmula de potencia (sin el factor \(\frac{3}{2}\)) pero los valores numéricos de dq son distintos.

### Demostración: \(P_{3\phi} = \frac{3}{2}(v_\alpha i_\alpha + v_\beta i_\beta)\) con amplitud invariante

La potencia trifásica instantánea es:

$$P_{3\phi} = v_a i_a + v_b i_b + v_c i_c$$

Con sistema equilibrado: \(v_a = V_m\cos(\omega t+\phi_v)\), \(v_b = V_m\cos(\omega t+\phi_v-\frac{2\pi}{3})\), \(v_c = V_m\cos(\omega t+\phi_v+\frac{2\pi}{3})\), y corrientes con desfase \(\phi\). Tras Clarke (amplitud invariante) se tiene \(v_\alpha = V_m\cos(\omega t+\phi_v)\), \(v_\beta = V_m\sin(\omega t+\phi_v)\), \(i_\alpha = I_m\cos(\omega t+\phi_v-\phi)\), \(i_\beta = I_m\sin(\omega t+\phi_v-\phi)\).

Calculando el producto escalar en αβ:

$$v_\alpha i_\alpha + v_\beta i_\beta = V_m I_m\cos(\omega t+\phi_v)\cos(\omega t+\phi_v-\phi) + V_m I_m\sin(\omega t+\phi_v)\sin(\omega t+\phi_v-\phi)$$

$$= V_m I_m \cos\!\big[(\omega t+\phi_v)-(\omega t+\phi_v-\phi)\big] = V_m I_m\cos\phi$$

Por otro lado, la potencia trifásica real con amplitudes de pico es \(P_{3\phi} = \frac{3}{2}V_m I_m\cos\phi\) (la suma de las tres fases en permanente suma el triple de la potencia de una fase, y la potencia de una fase es \(\frac{1}{2}V_m I_m\cos\phi\) para valores de pico). Comparando:

$$\boxed{P_{3\phi} = \tfrac{3}{2}(v_\alpha i_\alpha + v_\beta i_\beta)}$$

El factor \(\frac{3}{2}\) aparece porque la convención de amplitud invariante escala los vectores en αβ por \(\frac{2}{3}\) (factor \(k\)) pero la energía escala con el cuadrado: \(\left(\frac{2}{3}\right)^{-1} = \frac{3}{2}\). Con potencia invariante (\(k=\sqrt{2/3}\)) este factor sería exactamente 1.

### Verificación numérica

Instante \(t=0\), sistema equilibrado con \(V_m = 1\) pu, fase a en su pico:

$$\mathbf{x}_{abc} = \begin{bmatrix}1\\-\tfrac{1}{2}\\-\tfrac{1}{2}\end{bmatrix}$$

Aplicando Clarke (amplitud invariante, \(k=\frac{2}{3}\)):

$$x_\alpha = \frac{2}{3}\left(1 - \frac{1}{2}\cdot\left(-\tfrac{1}{2}\right) - \frac{1}{2}\cdot\left(-\tfrac{1}{2}\right)\right) = \frac{2}{3}\!\left(1 + \tfrac{1}{4} + \tfrac{1}{4}\right) = \frac{2}{3}\cdot\frac{3}{2} = 1$$

$$x_\beta = \frac{2}{3}\cdot\frac{\sqrt{3}}{2}\left(-\tfrac{1}{2} - \left(-\tfrac{1}{2}\right)\right) = 0$$

$$\Rightarrow \quad (x_\alpha, x_\beta) = (1,\; 0) = (V_m,\; 0) \checkmark$$

El vector espacio apunta en +α, exactamente donde está la fase a en \(t=0\). El homopolar: \(x_0 = \frac{1}{3}(1 - \frac{1}{2} - \frac{1}{2}) = 0 \checkmark\).

## 2 — De αβ a dq: la rotación de Park y el vector espacio

### El vector espacio como fasor giratorio

La clave de Clarke es que, en un sistema equilibrado, \(x_\alpha + jx_\beta\) es un fasor que gira a velocidad \(\omega\). Si \(x_a = X_m\cos(\omega t + \phi_0)\), la demostración directa:

$$x_\alpha = X_m\cos(\omega t+\phi_0), \qquad x_\beta = X_m\sin(\omega t+\phi_0)$$

$$\Rightarrow \quad x_\alpha + jx_\beta = X_m e^{j(\omega t + \phi_0)}$$

Es un número complejo de módulo constante \(X_m\) girando en el plano complejo a \(\omega\,\text{rad/s}\) (sentido antihorario = secuencia positiva). La fase en \(t=0\) es \(\phi_0\).

### Park: multiplicar por \(e^{-j\theta}\)

Park proyecta este fasor giratorio sobre un eje de referencia que también gira con el mismo ángulo \(\theta(t) = \omega t + \phi_0\). Matemáticamente es una multiplicación por el fasor conjugado:

$$x_d + jx_q = (x_\alpha + jx_\beta)\,e^{-j\theta}$$

$$= X_m e^{j(\omega t+\phi_0)}\cdot e^{-j(\omega t+\phi_0)} = X_m e^{j\cdot 0} = X_m$$

En componentes reales (expandiendo \(e^{-j\theta} = \cos\theta - j\sin\theta\)):

$$x_d = x_\alpha\cos\theta + x_\beta\sin\theta, \qquad x_q = -x_\alpha\sin\theta + x_\beta\cos\theta$$

O en forma matricial:

$$\begin{bmatrix}x_d\\x_q\end{bmatrix} = \underbrace{\begin{bmatrix}\cos\theta & \sin\theta\\-\sin\theta & \cos\theta\end{bmatrix}}_{\mathbf{R}(\theta)}\begin{bmatrix}x_\alpha\\x_\beta\end{bmatrix}$$

La matriz \(\mathbf{R}(\theta)\) es una rotación de \(-\theta\) (sentido horario), que corresponde a "montarse" en el marco que gira a \(+\theta\). El resultado es constante: senoide de 50 Hz → valor constante en dq.

### La condición de alineamiento

Cuando se elige \(\theta = \theta_v\) (el ángulo de la tensión de red), el eje d queda alineado con la tensión: \(v_d = V_m\) y \(v_q = 0\). Con este convenio:

- \(v_d \approx V_m\) (amplitud de fase): controla la tensión, relacionada con Q.
- \(v_q \approx 0\) en estado estacionario: la PLL mantiene \(v_q=0\) ajustando \(\theta\).
- \(i_d\): corriente activa (en fase con la tensión).
- \(i_q\): corriente reactiva (en cuadratura con la tensión).

La PLL SRF (ver [[pll-srf]]) cierra un PI sobre \(v_q\) para hacer que \(\theta\) converja al ángulo de la tensión.

### La transformada inversa

Para generar las modulantes PWM a partir de las referencias dq se aplica la cadena inversa:

**Paso 1 — Park inversa** (es \(\mathbf{R}^{-1}(\theta) = \mathbf{R}(-\theta) = \mathbf{R}^T(\theta)\)):

$$\begin{bmatrix}x_\alpha\\x_\beta\end{bmatrix} = \begin{bmatrix}\cos\theta & -\sin\theta\\\sin\theta & \cos\theta\end{bmatrix}\begin{bmatrix}x_d\\x_q\end{bmatrix}$$

**Paso 2 — Clarke inversa** (con amplitud invariante, la inversa de \(\mathbf{T}_C^{amp}\)):

$$\begin{bmatrix}x_a\\x_b\\x_c\end{bmatrix} = \begin{bmatrix}1 & 0\\-\frac{1}{2} & \frac{\sqrt{3}}{2}\\-\frac{1}{2} & -\frac{\sqrt{3}}{2}\end{bmatrix}\begin{bmatrix}x_\alpha\\x_\beta\end{bmatrix}$$

La verificación es inmediata: \(x_d = X_m\), \(x_q = 0\) → \(x_\alpha = X_m\cos\theta\), \(x_\beta = X_m\sin\theta\) → \(x_a = X_m\cos\theta\) (senoide).

## 3 — El acoplamiento cruzado ωL: de dónde sale exactamente

### La ecuación del inductor en αβ

Para una bobina \(L\) en αβ la ecuación es la misma que en el dominio del tiempo sin transformar (αβ es un marco fijo, no hay cambio de variables):

$$\mathbf{v}_{\alpha\beta} = L\frac{d\mathbf{i}_{\alpha\beta}}{dt}$$

donde \(\mathbf{v}_{\alpha\beta} = \begin{bmatrix}v_\alpha\\v_\beta\end{bmatrix}\) e \(\mathbf{i}_{\alpha\beta} = \begin{bmatrix}i_\alpha\\i_\beta\end{bmatrix}\). No hay términos cruzados porque los ejes αβ son fijos.

### Pasando al marco dq: la regla del producto

La relación entre αβ y dq es:

$$\mathbf{i}_{\alpha\beta} = \mathbf{R}^{-1}(\theta)\,\mathbf{i}_{dq} = \mathbf{R}^T(\theta)\,\mathbf{i}_{dq}$$

Derivando respecto al tiempo (regla del producto):

$$\frac{d\mathbf{i}_{\alpha\beta}}{dt} = \frac{d\mathbf{R}^T}{dt}\,\mathbf{i}_{dq} + \mathbf{R}^T\,\frac{d\mathbf{i}_{dq}}{dt}$$

Calculando \(\frac{d\mathbf{R}^T}{dt}\) con \(\theta = \omega t\) (velocidad constante, \(\dot\theta = \omega\)):

$$\mathbf{R}^T = \begin{bmatrix}\cos\theta & -\sin\theta\\\sin\theta & \cos\theta\end{bmatrix} \;\Rightarrow\; \frac{d\mathbf{R}^T}{dt} = \omega\begin{bmatrix}-\sin\theta & -\cos\theta\\\cos\theta & -\sin\theta\end{bmatrix}$$

Se observa que \(\frac{d\mathbf{R}^T}{dt} = \omega\,\mathbf{J}\,\mathbf{R}^T\) donde \(\mathbf{J} = \begin{bmatrix}0 & -1\\1 & 0\end{bmatrix}\) (rotación de 90°). Comprobación:

$$\omega\,\mathbf{J}\,\mathbf{R}^T = \omega\begin{bmatrix}0&-1\\1&0\end{bmatrix}\begin{bmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{bmatrix} = \omega\begin{bmatrix}-\sin\theta&-\cos\theta\\\cos\theta&-\sin\theta\end{bmatrix} \checkmark$$

Entonces:

$$\frac{d\mathbf{i}_{\alpha\beta}}{dt} = \omega\,\mathbf{J}\,\mathbf{R}^T\,\mathbf{i}_{dq} + \mathbf{R}^T\frac{d\mathbf{i}_{dq}}{dt}$$

### Proyectando en el marco dq

La ecuación del inductor en αβ era \(\mathbf{v}_{\alpha\beta} = L\frac{d\mathbf{i}_{\alpha\beta}}{dt}\). Sustituyendo la expresión de la derivada y multiplicando ambos lados por \(\mathbf{R}(\theta)\) (para pasar de αβ a dq):

$$\underbrace{\mathbf{R}\,\mathbf{v}_{\alpha\beta}}_{\mathbf{v}_{dq}} = L\,\mathbf{R}\left(\omega\,\mathbf{J}\,\mathbf{R}^T\mathbf{i}_{dq} + \mathbf{R}^T\frac{d\mathbf{i}_{dq}}{dt}\right)$$

$$\mathbf{v}_{dq} = \omega L\underbrace{\mathbf{R}\,\mathbf{J}\,\mathbf{R}^T}_{=\,\mathbf{J}}\,\mathbf{i}_{dq} + L\underbrace{\mathbf{R}\,\mathbf{R}^T}_{=\,\mathbf{I}}\frac{d\mathbf{i}_{dq}}{dt}$$

> **¿Por qué \(\mathbf{R}\mathbf{J}\mathbf{R}^T = \mathbf{J}\)?** Porque \(\mathbf{J}\) conmuta con las rotaciones (es el generador infinitesimal del grupo SO(2)). Demostración directa: \(\mathbf{R}\mathbf{J}\mathbf{R}^T = \det(\mathbf{R})\mathbf{J} = \mathbf{J}\) (para \(\det(\mathbf{R})=1\)).

El resultado es:

$$\boxed{\mathbf{v}_{dq} = L\frac{d\mathbf{i}_{dq}}{dt} + \omega L\,\mathbf{J}\,\mathbf{i}_{dq}}$$

### En componentes escalares

Expandiendo \(\mathbf{J}\,\mathbf{i}_{dq} = \begin{bmatrix}0&-1\\1&0\end{bmatrix}\begin{bmatrix}i_d\\i_q\end{bmatrix} = \begin{bmatrix}-i_q\\i_d\end{bmatrix}\):

$$\boxed{v_d = L\frac{di_d}{dt} - \omega L\,i_q, \qquad v_q = L\frac{di_q}{dt} + \omega L\,i_d}$$

Los términos \(-\omega L\,i_q\) y \(+\omega L\,i_d\) son el **acoplamiento cruzado**. No existen en la física original (en αβ o abc hay solo \(L\,di/dt\)); aparecen únicamente por el cambio al marco giratorio, exactamente como la fuerza de Coriolis en mecánica clásica.

### Idem para el condensador

La corriente en el condensador en αβ: \(\mathbf{i}_{\alpha\beta} = C_f\frac{d\mathbf{v}_{\alpha\beta}}{dt}\). Aplicando el mismo cambio de variables a la tensión del condensador \(\mathbf{v}_{\alpha\beta} = \mathbf{R}^T\mathbf{v}_{dq}\) y derivando:

$$\mathbf{i}_{dq}^C = C_f\frac{d\mathbf{v}_{dq}}{dt} + \omega C_f\,\mathbf{J}\,\mathbf{v}_{dq}$$

En componentes:

$$i_d^C = C_f\frac{dv_d}{dt} - \omega C_f\,v_q, \qquad i_q^C = C_f\frac{dv_q}{dt} + \omega C_f\,v_d$$

> A resaltar: el acoplamiento cruzado no viene de la física del inductor o el condensador. Viene del marco de referencia. Es la "fuerza de Coriolis" del sistema eléctrico en dq. El control lo cancela explícitamente sumando los términos \(\mp\omega L\,i_q\) y \(\pm\omega L\,i_d\) a la salida del PI (ver [[desacoplo-dq]]).

## 4 — Función de transferencia del inductor en dq (sistema MIMO)

### La planta dq es un sistema 2×2 acoplado

En el dominio de Laplace, la ecuación del inductor en dq \(\mathbf{v}_{dq} = L(s\,\mathbf{I} + \omega\mathbf{J})\,\mathbf{i}_{dq}\) (con condición inicial cero) se escribe matricialmente:

$$\begin{bmatrix}V_d(s)\\V_q(s)\end{bmatrix} = L\begin{bmatrix}s & -\omega\\\omega & s\end{bmatrix}\begin{bmatrix}I_d(s)\\I_q(s)\end{bmatrix}$$

La **matriz de impedancia** en dq es:

$$\mathbf{Z}_{dq}(s) = L\begin{bmatrix}s & -\omega\\\omega & s\end{bmatrix}$$

### La inversa: admitancia dq

Para encontrar \(\mathbf{Y}_{dq}(s) = \mathbf{Z}_{dq}^{-1}(s)\), se invierte la matriz \(2\times2\) con \(\det(\mathbf{Z}_{dq}) = L^2(s^2+\omega^2)\):

$$\mathbf{Y}_{dq}(s) = \frac{1}{L(s^2+\omega^2)}\begin{bmatrix}s & \omega\\-\omega & s\end{bmatrix}$$

Los cuatro elementos de la admitancia son funciones de transferencia. En forma explícita:

$$I_d = \frac{1}{L}\cdot\frac{s}{s^2+\omega^2}\,V_d + \frac{1}{L}\cdot\frac{\omega}{s^2+\omega^2}\,V_q$$
$$I_q = \frac{1}{L}\cdot\frac{-\omega}{s^2+\omega^2}\,V_d + \frac{1}{L}\cdot\frac{s}{s^2+\omega^2}\,V_q$$

### Los polos en ±jω y su significado

El denominador \(s^2 + \omega^2\) tiene raíces en \(s = \pm j\omega_0\) (donde \(\omega_0 = 2\pi\cdot50\,\text{rad/s}\)). En el dominio del tiempo, los polos en el eje imaginario puro son oscilaciones no amortiguadas a la frecuencia fundamental. Físicamente: el marco dq gira a \(\omega_0\); desde el punto de vista del marco, la señal estacionaria de red es continua (polo en \(s=0\) de un integrador en αβ se convierte en polo en \(s=j\omega_0\) en dq).

Este es el motivo por el que el PI clásico en dq tiene error nulo en continua: los polos de la planta en \(\pm j\omega_0\) quedan anulados si el controlador tiene un integrador alineado con la frecuencia de referencia. Cuando hay que rechazar perturbaciones a otras frecuencias se añaden resonantes (PR) en αβ.

### El desacoplo cancela el término cruzado

Si se añade la señal de desacoplo \(v_d^{dec} = +\omega L\,i_q\) (sumada a la salida del PI de d) y \(v_q^{dec} = -\omega L\,i_d\) (sumada a la salida del PI de q), la planta efectiva que ve el controlador pasa de la matriz acoplada a una diagonal:

$$\mathbf{Z}_{dq,des}(s) = L\begin{bmatrix}s & 0\\0 & s\end{bmatrix}$$

Cada eje ve simplemente \(sL\): un integrador puro de primer orden. Los dos ejes quedan independientes y se pueden sintonizar por separado con la fórmula del PI de corriente clásica.

> La tabla siguiente resume la cadena de causalidad:

| Origen | Consecuencia | Corrección |
|---|---|---|
| Marco dq gira a \(\omega_0\) | La derivada de \(\mathbf{i}_{dq}\) incluye el término \(\omega\mathbf{J}\,\mathbf{i}_{dq}\) | — |
| Término \(\omega\mathbf{J}\) en la planta | \(V_d\) afecta a \(I_q\) y viceversa (planta 2×2 acoplada) | Desacoplo: sumar \(\pm\omega L\,i_{q,d}\) |
| Sin desacoplo | Escalón en \(v_d\) genera transitorio en \(i_q\) (eje cruzado responde) | Ver panel (b) de la figura |
| Con desacoplo | Cada eje responde independientemente | Planta efectiva es \(sL\) por eje |

## 5 — Clarke y Park para señales desequilibradas

### Descomposición en secuencias

Un sistema trifásico desequilibrado se descompone en secuencia positiva (giro antihorario, frecuencia +ω), secuencia negativa (giro horario, frecuencia −ω) y secuencia homopolar. La componente de secuencia positiva tiene amplitudes iguales y desfases de −120°/+120°; la negativa tiene desfases de +120°/−120°.

En el plano αβ (usando la notación de fasor giratorio):

- **Secuencia positiva:** \(x^+_{\alpha\beta} = X^+e^{+j\omega t}\) (gira CCW)
- **Secuencia negativa:** \(x^-_{\alpha\beta} = X^-e^{-j\omega t}\) (gira CW)

La superposición forma una elipse en αβ en lugar de un círculo. La excentricidad de la elipse es proporcional al desequilibrio: con equilibrio perfecto el círculo tiene radio \(X^+\) y \(X^-=0\).

### En el marco dq alineado con la secuencia positiva

Aplicando Park con \(\theta = \omega t\) (alineado con positiva):

- Secuencia positiva → constante en dq: \(X^+e^{j\omega t}\cdot e^{-j\omega t} = X^+\) ✓
- Secuencia negativa → componente oscilatoria a \(-2\omega\): \(X^-e^{-j\omega t}\cdot e^{-j\omega t} = X^-e^{-2j\omega t}\)

La componente negativa aparece en dq como una oscilación a \(2\omega_0 = 2\pi\cdot100\,\text{rad/s}\), es decir, a **100 Hz** en una red de 50 Hz. Esta oscilación contamina las medidas de \(i_d\) e \(i_q\) con un ripple a doble frecuencia.

### Ejemplo numérico: desequilibrio del 10%

Parámetros: \(V_m = 563\,\text{V}\), desequilibrio negativo del 10%:

$$\mathbf{v}_{abc}(t) = \begin{bmatrix}563\cos(\omega t)\\-563\cdot0.9\cos(\omega t - 2\pi/3)\\-563\cdot1.1\cos(\omega t + 2\pi/3)\end{bmatrix} \quad\text{(b más baja, c más alta)}$$

La amplitud de la secuencia negativa es \(V^- \approx 0.1\cdot V_m\cdot\frac{\sqrt{3}}{2}\approx 0.05\cdot 2V_m/\sqrt{3}\). Para un desequilibrio del 10% (diferencia de amplitudes relativa), la secuencia negativa resulta en un ripple en \(v_d\) e \(i_d\) de amplitud aproximada \(V^- \approx 0.1\cdot V_m = 56.3\,\text{V}\) oscilando a 100 Hz. El control en dq no puede rechazar este ripple con un PI (que tiene ganancia finita a 100 Hz); se necesita un controlador resonante a 100 Hz o separar las secuencias.

### El DSOGI separa las secuencias antes de Park

El DSOGI (Dual Second-Order Generalized Integrator, ver [[pll-srf]]) implementa un filtro adaptativo en αβ que proporciona directamente las secuencias positiva y negativa:

$$\begin{aligned}x^+_\alpha &= \tfrac{1}{2}(x_\alpha - x'_\beta), & x^+_\beta &= \tfrac{1}{2}(x_\beta + x'_\alpha)\\x^-_\alpha &= \tfrac{1}{2}(x_\alpha + x'_\beta), & x^-_\beta &= \tfrac{1}{2}(x_\beta - x'_\alpha)\end{aligned}$$

donde \(x'\) denota la versión en cuadratura (desfasada 90°) obtenida por el SOGI. Así, aplicando Park a \(\mathbf{x}^+_{\alpha\beta}\) y \(\mathbf{x}^-_{\alpha\beta}\) por separado se obtienen dos marcos dq sin el ripple a 100 Hz.

<div class="cfig"><img src="figuras/marco-dq-analisis.png" alt="Cuatro paneles de análisis dq"><div class="cap">(c) Con desequilibrio del 10%, \(i_d\) e \(i_q\) presentan un ripple a 100 Hz de amplitud proporcional a la componente de secuencia negativa. El PI solo controla el valor medio; el ripple no se atenúa sin resonante o separación de secuencias.</div></div>

## 6 — La transformada inversa: de consignas dq a modulantes abc

### La cadena completa

La cadena de síntesis de las modulantes PWM es la inversa exacta de la cadena de medida:

$$\underbrace{x_d^*,\,x_q^*}_{\text{ref. control}}\;\xrightarrow{\text{Park}^{-1}}\;x_\alpha,\,x_\beta\;\xrightarrow{\text{Clarke}^{-1}}\;\underbrace{x_a,\,x_b,\,x_c}_{\text{modulantes}}$$

**Park inversa** (rotación de \(+\theta\)):

$$x_\alpha = x_d\cos\theta - x_q\sin\theta, \qquad x_\beta = x_d\sin\theta + x_q\cos\theta$$

**Clarke inversa** (amplitud invariante, sin homopolar):

$$x_a = x_\alpha, \quad x_b = -\tfrac{1}{2}x_\alpha + \tfrac{\sqrt{3}}{2}x_\beta, \quad x_c = -\tfrac{1}{2}x_\alpha - \tfrac{\sqrt{3}}{2}x_\beta$$

Se comprueba que las tres suman cero: \(x_a+x_b+x_c = x_\alpha + (-\frac{1}{2}+(-\frac{1}{2}))x_\alpha + (\frac{\sqrt{3}}{2}-\frac{\sqrt{3}}{2})x_\beta = 0\) ✓.

### Verificación de conservación de potencia

Con \(x_d = X_m\), \(x_q = 0\), \(\theta = \omega t\):
- αβ: \(x_\alpha = X_m\cos(\omega t)\), \(x_\beta = X_m\sin(\omega t)\)
- abc: \(x_a = X_m\cos(\omega t)\), \(x_b = X_m\cos(\omega t - \frac{2\pi}{3})\), \(x_c = X_m\cos(\omega t + \frac{2\pi}{3})\)
- Potencia en dq: \(P = \frac{3}{2}(v_d i_d + v_q i_q) = \frac{3}{2}V_m I_m\cos\phi\)
- Potencia en abc: \(P = v_a i_a + v_b i_b + v_c i_c = \frac{3}{2}V_m I_m\cos\phi\) ✓

### El modo común en la modulación

Las modulantes abc que salen de la Clarke inversa son señales bipolares centradas en cero. En el modulador de un inversor de dos niveles con bus de continua \(V_{dc}\), la referencia de tensión de cada fase respecto al punto medio del bus es:

$$m_a = \frac{x_a}{V_{dc}/2}, \quad m_b = \frac{x_b}{V_{dc}/2}, \quad m_c = \frac{x_c}{V_{dc}/2}$$

donde \(m \in [-1,+1]\). Se puede añadir un modo común (offset) que no afecta a las tensiones de línea pero reduce el índice de modulación efectivo (inyección de tercer armónico, SVPWM). Este modo común lo gestiona el modulador, no la transformada.

### Código de la cadena completa

```python
import numpy as np

# ── Convención: amplitud invariante (factor 2/3) ──────────────────────
def clarke(xa, xb, xc):
    al = (2/3)*(xa - 0.5*xb - 0.5*xc)
    be = (2/3)*(np.sqrt(3)/2)*(xb - xc)
    return al, be

def park(al, be, th):
    c, s = np.cos(th), np.sin(th)
    return c*al + s*be, -s*al + c*be      # (xd, xq)

def park_inv(xd, xq, th):
    c, s = np.cos(th), np.sin(th)
    return c*xd - s*xq, s*xd + c*xq      # (al, be)

def clarke_inv(al, be):
    xa =  al
    xb = -0.5*al + (np.sqrt(3)/2)*be
    xc = -0.5*al - (np.sqrt(3)/2)*be
    return xa, xb, xc

# ── Verificación rápida ───────────────────────────────────────────────
w0 = 2*np.pi*50
t  = np.linspace(0, 0.02, 10000)
va = np.cos(w0*t); vb = np.cos(w0*t - 2*np.pi/3); vc = np.cos(w0*t + 2*np.pi/3)
al, be = clarke(va, vb, vc)              # al = cos(wt), be = sin(wt)
th     = w0*t                            # PLL perfecta
vd, vq = park(al, be, th)               # vd ≈ 1.0, vq ≈ 0.0
# Vuelta a abc:
al2, be2   = park_inv(vd, vq, th)
va2,vb2,vc2 = clarke_inv(al2, be2)
print(np.allclose(va, va2))              # True
```

## Procedimiento de diseño (genérico)

1. Define el ángulo θ del marco (de la PLL en GFL, del droop/VSM en GFM).
2. Aplica Clarke y Park a tensiones y corrientes medidas; elige la convención (amplitud o potencia invariante) y mantenla en todo el proyecto.
3. Diseña el control en dq (referencias constantes, PI sin error), con desacoplo explícito de los términos \(\omega\mathbf{J}\). Si usas resonantes, quédate en αβ.
4. Antitransforma (dq→αβ→abc) para generar las modulantes del PWM.
5. Cuida el alineamiento (eje d con la tensión) y la convención. Documenta el factor de escala.

## Parámetros y valores típicos

- Sistema equilibrado, sin neutro: \(x_0 = 0\), basta con αβ. Convención de amplitud: pico de fase = componente α cuando la fase a está en su pico.
- Convención de amplitud usada en el proyecto: \(V_0 = V_{ll}\sqrt{2/3}\). El factor de potencia es \(P = \frac{3}{2}(v_d i_d + v_q i_q)\).
- Acoplamiento cruzado con L = 2 mH, ω = 314 rad/s, I = 100 A: \(\omega L = 0.628\,\Omega\), caída cruzada \(\approx 63\,\text{V}\) → no despreciable a plena carga.
- Ripple a 100 Hz por desequilibrio del 10%: amplitud de oscilación en dq \(\approx 10\%\) de la amplitud nominal de la fase (en unidades de la convención elegida).

## Errores comunes

- Mezclar convención de amplitud (factor \(\frac{2}{3}\)) y de potencia (factor \(\sqrt{\frac{2}{3}}\)) → factores \(\frac{3}{2}\) incorrectos en la potencia.
- Descartar el homopolar cuando hay neutro o desequilibrio relevante.
- Confundir Clarke (eje fijo, αβ) con Park (eje giratorio, dq).
- Olvidar los términos cruzados \(\omega\mathbf{J}\) al modelar la planta → planta dq incorrecta.
- No añadir el desacoplo → los lazos de corriente d y q se perturban mutuamente.
- No alinear bien el eje d con la tensión → el punto de operación en dq no es el esperado.
- Ignorar el ripple a 100 Hz en dq bajo desequilibrio → control incorrecto en red desequilibrada.

## Uso en proyectos

- **01 - GFM-Impedance (modelado):** todo el modelo (15 estados) vive en dq. Se usan dos marcos (red y control) ligados por el ángulo delta; el acoplamiento cruzado aparece en el modelo de estado como los bloques 2×2 antidiagonales.
- **02 - GFL-Impedance:** el marco dq se alinea con la red mediante la PLL; la respuesta en pequeña señal de la PLL interactúa con el lazo de corriente dq.

## Conceptos relacionados

- [[desacoplo-dq]] · [[potencia-instantanea-dq]] · [[componentes-simetricas]] · [[control-cascada]] · [[control-vectorial]] · [[filtro-lcl]] · [[pll-srf]]

## Referencias

- Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010.
- Akagi, Watanabe, Aredes, Instantaneous Power Theory, Wiley 2007.
- Teodorescu, Liserre, Rodriguez, Grid Converters for Photovoltaic and Wind Power Systems, Wiley 2011.
