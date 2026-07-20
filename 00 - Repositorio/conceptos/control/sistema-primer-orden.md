---
titulo: Sistema de primer orden
slug: sistema-primer-orden
categoria: control
tipo: concepto
nivel: basico
proyectos: []
objetivos: [entender la respuesta de un sistema de un solo polo]
tags: [primer-orden, constante-de-tiempo, polo, respuesta-escalon, bode, ancho-de-banda, basico]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-03
relacionados: [polos-ceros, respuesta-segundo-orden, funcion-transferencia, sintonia-pi-pid, control-cascada]
referencias:
  - "Ogata, Ingeniería de Control Moderna, Pearson"
  - "Franklin, Powell, Feedback Control of Dynamic Systems, Pearson"
---

## Definición
Sistema con un único polo (un solo almacenador de energía dominante). Su respuesta no oscila:
sube o baja exponencialmente hacia su valor final. Es el ladrillo más simple del control y el modelo
reducido más usado en diseño de lazos en cascada.

## Fundamento teórico
$$ G(s) = \frac{K}{\tau s + 1} $$
- \( K \): ganancia en continua (valor final ante un escalón unitario).
- \( \tau \): **constante de tiempo** (s). El polo está en \( s=-1/\tau \).
Respuesta a un escalón de amplitud \( A \):
$$ y(t) = A\,K\left(1 - e^{-t/\tau}\right) $$
Alcanza el 63% del valor final en \( t=\tau \) y el 99% en \( t\approx 5\tau \).
Cuanto menor \( \tau \) (polo más a la izquierda), más rápido.
El ancho de banda es \( \omega_{BW}=1/\tau \), exactamente la frecuencia del polo: donde \( |G(j\omega_{BW})|=-3\,\text{dB} \).

<div class="cfig"><img src="figuras/sistema-primer-orden-escalon.png" alt="respuesta al escalon de primer orden"><div class="cap">Respuesta al escalón de primer orden: alcanza el 63% del valor final en t=τ y el 99% en 5τ. El polo en −1/τ fija la rapidez.</div></div>

## 1 — De la FDT a la respuesta al escalón \( 1-e^{-t/\tau} \)
**Paso 1 — salida en Laplace.** Un escalón de amplitud \( A \) es \( R(s)=A/s \). La salida es el producto de la planta por la entrada:

$$ Y(s)=G(s)\,R(s)=\frac{K}{\tau s+1}\cdot\frac{A}{s}=\frac{AK}{s\,(\tau s+1)} $$

**Paso 2 — fracciones parciales.** Descomponemos en dos términos para poder antitransformar cada uno:

$$ \frac{AK}{s\,(\tau s+1)}=\frac{B}{s}+\frac{C}{\tau s+1} $$

Multiplicando por \( s(\tau s+1) \): \( AK=B(\tau s+1)+C\,s \). Evaluando en \( s=0 \): \( AK=B \). Evaluando en \( s=-1/\tau \): \( AK=C\,(-1/\tau)\Rightarrow C=-AK\tau \). Sustituyendo:

$$ Y(s)=\frac{AK}{s}-\frac{AK\tau}{\tau s+1}=\frac{AK}{s}-\frac{AK}{s+1/\tau} $$

(en el último paso se dividió numerador y denominador del segundo término por \( \tau \)).

**Paso 3 — antitransformar.** Usando \( \mathcal{L}^{-1}\{1/s\}=1 \) y \( \mathcal{L}^{-1}\{1/(s+1/\tau)\}=e^{-t/\tau} \):

$$ \boxed{\;y(t)=AK\left(1-e^{-t/\tau}\right)\;} $$

**Paso 4 — leer la constante de tiempo.** En \( t=\tau \): \( y=AK(1-e^{-1})=AK\cdot 0{,}632 \), el **63,2 %** del valor final. En \( t=5\tau \): \( y=AK(1-e^{-5})=AK\cdot 0{,}993 \), prácticamente el **100 %**. La velocidad la fija enteramente \( \tau \): polo más a la izquierda ⟹ \( \tau \) menor ⟹ exponencial más rápida.

## 2 — La respuesta al escalón: y(t)=K·(1−e^(−t/τ)), el 63% en τ, el 99% en 5τ

La exponencial \( e^{-t/\tau} \) es el único ingrediente de la dinámica. Conviene tener interiorizados sus valores en los hitos clave:

| \( t/\tau \) | \( e^{-t/\tau} \) | \( 1-e^{-t/\tau} \) | Lectura práctica |
|---|---|---|---|
| 1 | 0,368 | **0,632** | 63,2 % → lee \( \tau \) en el experimento |
| 2 | 0,135 | 0,865 | 86,5 % |
| 3 | 0,050 | 0,950 | 95,0 % → criterio al 5 % |
| 4 | 0,018 | 0,982 | 98,2 % → criterio al 2 % |
| 5 | 0,007 | **0,993** | 99,3 % → considerado "establecido" |

**Interpretación geométrica.** La recta tangente a \( y(t) \) en \( t=0 \) tiene pendiente \( \frac{AK}{\tau} \) (la derivada inicial). Si se prolonga esa recta hasta alcanzar el valor final \( AK \), lo hace exactamente en \( t=\tau \). Esto da el método gráfico para identificar \( \tau \) sin buscar el 63%: traza la tangente inicial y mide dónde corta al valor final.

**Identificación experimental.** Dado el gráfico de la respuesta escalón de un sistema desconocido pero de primer orden:
1. Lee el valor final \( y_\infty \) → ganancia \( K=y_\infty/A \).
2. Localiza \( y=0{,}632\,y_\infty \) en el eje y → el tiempo correspondiente es \( \hat\tau \).
3. Verifica que en \( 5\hat\tau \) la señal es >99 % (confirma el orden uno).

**Relación con el tiempo de establecimiento.** Los criterios habituales de tiempo de establecimiento (\( t_s \)) usan bandas del ±2 % o ±5 % del valor final:

$$ t_s^{(2\%)} \approx 4\tau, \qquad t_s^{(5\%)} \approx 3\tau $$

No confundirlos con \( \tau \): el establecimiento al 2 % tarda cuatro veces la constante de tiempo.

## 3 — La función de transferencia: G(s)=K/(τs+1), polo en s=−1/τ, ancho de banda ω_BW=1/τ

**El polo y la respuesta temporal.** La función de transferencia tiene un único polo en \( s=-1/\tau \). La posición de ese polo en el plano complejo determina completamente el comportamiento dinámico: su parte real \( -1/\tau \) fija la tasa de decaimiento de la exponencial. Polo real negativo → respuesta exponencial sin oscilación. Polo más a la izquierda ↔ \( \tau \) menor ↔ sistema más rápido.

**El ancho de banda como medida de rapidez.** En frecuencia, la rapidez se expresa como ancho de banda: la frecuencia \( \omega_{BW} \) en la que la ganancia cae 3 dB respecto al valor DC. Para \( G(s)=K/(\tau s+1) \):

$$ |G(j\omega)|=\frac{K}{\sqrt{1+(\omega\tau)^2}} $$

La caída de 3 dB ocurre cuando el denominador vale \( \sqrt{2} \):

$$ \sqrt{1+(\omega_{BW}\tau)^2}=\sqrt{2} \;\Rightarrow\; \omega_{BW}\tau=1 \;\Rightarrow\; \boxed{\;\omega_{BW}=\frac{1}{\tau}\;} $$

El ancho de banda coincide exactamente con la frecuencia del polo. Esto es la razón por la que se habla indistintamente de "polo en \( \omega_c \)" y "ancho de banda \( \omega_c \)": son la misma magnitud.

**Bode del primer orden.** La magnitud en dB es \( 20\log_{10}(K)-20\log_{10}\sqrt{1+(\omega\tau)^2} \). Tiene dos asíntotas: \( 20\log_{10}K \) (plano) para \( \omega\ll1/\tau \), y \( 20\log_{10}K-20\log_{10}(\omega\tau) \) (pendiente −20 dB/dec) para \( \omega\gg1/\tau \). Las asíntotas se cortan exactamente en \( \omega=1/\tau \) (frecuencia de polo). La fase va de 0° (baja frecuencia) a −90° (alta frecuencia), pasando por −45° exactamente en \( \omega=1/\tau \).

**Implicación de diseño.** Especificar el tiempo de establecimiento al 2% equivale a especificar el ancho de banda:

$$ t_s \approx 4\tau = \frac{4}{\omega_{BW}} \;\Rightarrow\; \omega_{BW}=\frac{4}{t_s} $$

Si se diseña un lazo de corriente con tiempo de establecimiento de 1 ms, se necesita \( \omega_{BW}=4000\,\text{rad/s}\approx637\,\text{Hz} \). El PI se sintoniza para colocar el polo de lazo cerrado en \( -\omega_{BW} \), lo que da exactamente ese tiempo de respuesta.

## 4 — La respuesta a la rampa y a la entrada senoidal

### Respuesta a la rampa

Una rampa es \( r(t)=Rt \) (pendiente \( R \) en unidades/s). En Laplace: \( R(s)=R/s^2 \). La salida:

$$ Y(s)=\frac{K}{\tau s+1}\cdot\frac{R}{s^2}=\frac{KR}{s^2(\tau s+1)} $$

Fracciones parciales: \( KR/(s^2(\tau s+1)) = A/s^2 + B/s + C/(\tau s+1) \). Evaluando:
- \( s^2 \) en \( s=0 \): \( A=KR \)
- Derivada en \( s=0 \): \( B=-KR\tau \)
- \( \tau s+1 \) en \( s=-1/\tau \): \( C=KR\tau^2 \)

Antitransformando:

$$ y(t)=KRt - KR\tau\left(1-e^{-t/\tau}\right) $$

En régimen permanente (\( t\gg\tau \), el transitorio exponencial ya decayó):

$$ y(\infty)\approx KRt-KR\tau $$

El sistema **sigue** la rampa con error de posición nulo (para \( K=1 \), la salida es paralela a la entrada) pero con un **retraso constante** de \( K\tau \) en el tiempo, lo que equivale a un **error de velocidad**:

$$ \boxed{\;e_{rampa}=K\cdot\tau\cdot R\;} $$

Para atenuar este error hace falta reducir \( \tau \) (lazo más rápido) o añadir un integrador (que convierte el sistema en tipo 2 y anula el error ante rampa).

### Respuesta senoidal

Para una entrada \( u(t)=\sin(\omega t) \), la salida en régimen permanente es:

$$ y_{ss}(t)=K\cdot\frac{1}{\sqrt{1+(\omega\tau)^2}}\sin\!\left(\omega t - \arctan(\omega\tau)\right) $$

- **Amplitud:** \( |G(j\omega)|=K/\sqrt{1+(\omega\tau)^2} \) — se atenúa progresivamente a partir de \( \omega=1/\tau \).
- **Desfase:** \( \angle G(j\omega)=-\arctan(\omega\tau) \) — siempre negativo (la salida va retrasada respecto a la entrada).
  - \( \omega\tau\ll1 \): desfase ≈ 0° (la salida copia la entrada).
  - \( \omega\tau=1 \): desfase = −45°, amplitud = \( K/\sqrt{2} \) (el punto −3 dB).
  - \( \omega\tau\gg1 \): desfase → −90°, amplitud → 0 (la salida no sigue la entrada).

Esta es la razón física por la que un lazo de control no puede tener ancho de banda mayor que \( 1/\tau_{planta} \): por encima de esa frecuencia la planta introduce más de 45° de desfase, y el lazo cierra con margen de fase negativo.

## 5 — El primer orden como modelo reducido: el lazo de corriente cerrado como 1/(1+s/α_c)

En el diseño de convertidores en cascada (tensión → corriente), el lazo de corriente cerrado se aproxima por un primer orden. Esta aproximación es el fundamento del método de diseño en cascada y vale la pena derivarla desde cero.

**El lazo de corriente con PI sobre inductor.** La planta del lazo de corriente es \( G_i(s)=1/(Ls+R) \). El PI tiene \( C(s)=K_p(1+\omega_i/s)=K_p(s+\omega_i)/s \) con cero en \( s=-\omega_i=-R/L \) (cancelación del polo de la planta). El lazo abierto tras la cancelación es:

$$ L(s)=C(s)\cdot G_i(s)\approx\frac{K_p}{Ls}\cdot\frac{1}{1+s/\omega_{sw}} $$

donde \( \omega_{sw}\gg\alpha_c \) agrupa los retardos de cómputo/PWM. Eligiendo \( K_p=\alpha_c L \), el lazo cerrado es:

$$ G_{cl}(s)=\frac{L(s)}{1+L(s)}\approx\frac{1}{1+s/\alpha_c} $$

**Resultado clave.** El lazo de corriente cerrado actúa como un primer orden con constante de tiempo \( 1/\alpha_c \) y ganancia DC unitaria. Esto es válido mientras \( \alpha_c \) sea bastante menor que la frecuencia de conmutación/muestreo (típico: \( \alpha_c < f_{sw}/10 \)).

**Por qué justifica el diseño en cascada.** Si el lazo de corriente es \( 1/(1+s/\alpha_c) \), el lazo de tensión exterior ve esa dinámica como una "planta aumentada": condensador de bus DC con el lazo de corriente ya cerrado. El diseñador del lazo de tensión puede ignorar la dinámica interna de corriente siempre que su ancho de banda sea suficientemente más lento (\( \alpha_v \ll \alpha_c \), típico \( \alpha_v \approx \alpha_c/5 \)). La separación de escalas de tiempo hace que los dos lazos sean casi independientes y cada uno se sintonice como un primer orden.

**Validez del modelo reducido.** La aproximación falla cuando:
- El inductor tiene saturación (no lineal → ganancia variable).
- Hay resonancias del filtro LCL cerca de \( \alpha_c \) (el cero de antirresonancia cambia el orden efectivo).
- Los retardos de cómputo son comparables a \( 1/\alpha_c \) (hay que incluirlos en el modelo).

<div class="cfig"><img src="figuras/sistema-primer-orden-analisis.png" alt="cuatro paneles: escalon con tau y 5tau, rampa con error, Bode -3dB en 1/tau, lazo de corriente como primer orden equivalente"><div class="cap">(a) Respuesta al escalón con τ y 5τ marcados. (b) Seguimiento de rampa: error en régimen = Kτ·R. (c) Bode del primer orden: −3 dB en ω = 1/τ, −45° de fase. (d) Lazo de corriente cerrado: la aproximación 1/(1+s/α_c) permite el diseño en cascada.</div></div>

## 6 — Diseño iterativo: el bus DC como primer orden, τ=RC

El condensador del bus DC con una carga de potencia constante es, en pequeña señal, un primer orden. Entender este modelo permite especificar directamente el ancho de banda del lazo de tensión.

**El circuito.** Un condensador \( C \) alimenta una carga resistiva equivalente \( R_{eq}=V_{dc}^2/P_{carga} \). La dinámica de la tensión es:

$$ C\frac{dv_{dc}}{dt}=i_{in}-\frac{v_{dc}}{R_{eq}} $$

Linealizando alrededor del punto de operación \( V_{dc} \):

$$ \frac{\hat v_{dc}(s)}{\hat i_{in}(s)}=\frac{R_{eq}}{1+s\,R_{eq}C}=\frac{R_{eq}}{\tau_{dc}\,s+1},\qquad \tau_{dc}=R_{eq}C $$

Este es exactamente un primer orden con \( \tau_{dc}=R_{eq}C \) y ganancia DC \( R_{eq} \).

**Especificaciones del lazo de tensión.** El lazo de tensión tiene que ser:
- Lo suficientemente rápido para rechazar perturbaciones de carga: \( \alpha_v > 1/\tau_{perturbacion} \).
- Lo suficientemente lento respecto al lazo de corriente: \( \alpha_v \lesssim \alpha_c/5 \).
- Con margen de fase suficiente (>45°): no sobrepasar \( \omega_{BW,planta}/3 \) para no ver la dinámica del condensador como retardo puro.

**Ejemplo numérico.** Bus DC de 1200 V, \( C=10\,\text{mF} \), carga nominal 50 kW.
\( R_{eq}=1200^2/50000=28{,}8\,\Omega \), \( \tau_{dc}=28{,}8\times0{,}01=0{,}288\,\text{s} \).
Ancho de banda del lazo de tensión: \( \alpha_v \approx 30\,\text{rad/s}\approx 5\,\text{Hz} \) (típico: 5–30 rad/s para lazos de bus DC).
Lazo de corriente: \( \alpha_c \approx 5\alpha_v=150\,\text{rad/s} \) mínimo, típico \( 2\pi\cdot500\,\text{rad/s} \).
Tiempo de establecimiento del lazo de tensión ante escalón de carga: \( t_s\approx4/\alpha_v=133\,\text{ms} \).

**Diseño del PI de tensión.** Usando el modelo de primer orden de la planta como guía:
\( K_{p,v}=\alpha_v\,C/2 \) (para cancelar el polo de la planta y colocar el polo de lazo cerrado en \( -\alpha_v \)). La constante integral se elige para rechazo de perturbación: \( \omega_{i,v}=\alpha_v/5 \).

## Cuándo y por qué se usa
Muchos lazos internos (corriente sobre un inductor) son de primer orden. Entenderlo permite
sintonizar por cancelación de polo, estimar tiempos de respuesta y justificar el diseño en cascada.

## Procedimiento (genérico)
1. Identifica el polo dominante y la ganancia DC.
2. Lee \( \tau \) (rapidez) y \( K \) (valor final).
3. Estima el tiempo de establecimiento \( \approx 4\tau \) (criterio 2%) o \( 3\tau \) (criterio 5%).
4. El ancho de banda \( \omega_{BW}=1/\tau \) es la frecuencia de polo.
5. Para acelerar, diseña un control que mueva el polo a la izquierda (aumenta \( K_p \)).

## Ejemplo de aplicación real
**Problema:** Lazo de corriente diseñado para \( \alpha_c=2\pi\cdot 750\,\text{rad/s} \) (\( \tau_{cl}=1/\alpha_c\approx0{,}21\,\text{ms} \)). Verificar midiendo la respuesta escalón en simulación.

Se aplica un escalón de referencia de 1 A. La corriente debe llegar al 63,2% (0,632 A) en \( \tau_{cl}\approx0{,}21\,\text{ms} \). En simulación se mide \( t_{63\%}=0{,}22\,\text{ms} \): error del 5%, aceptable. La ganancia DC se verifica como \( K=i(\infty)/i_{ref}=1{,}0 \): error en régimen nulo (el PI integra). El tiempo de asentamiento al 2% es \( t_s\approx4\tau_{cl}=0{,}84\,\text{ms} \). El ancho de banda medido: \( \omega_{BW}=1/\tau_{cl}\approx4712\,\text{rad/s}\approx750\,\text{Hz} \).

## Ejemplo de código
```python
import control as ct
G = ct.tf([2], [0.1, 1])           # K=2, tau=0.1 s
t, y = ct.step_response(G)         # sube hacia 2 con tau=0.1

# Lazo de corriente como primer orden
alpha_c = 2*np.pi*750              # BW deseado rad/s
L, R = 2e-3, 0.05                  # inductor
Kp = alpha_c * L; Ki = alpha_c * R # sintonía PI (cancelación de polo)
Gcl = ct.tf([alpha_c], [1, alpha_c]) # lazo cerrado: 1/(1+s/alpha_c)
```

## Parámetros y valores típicos
\( t \) al 63% = \( \tau \); al 95% ≈ \( 3\tau \); al 98% ≈ \( 4\tau \); al 99% ≈ \( 5\tau \).
Lazo de corriente típico: \( \alpha_c = 2\pi\cdot(300\text{–}1000)\,\text{Hz} \).
Lazo de tensión: \( \alpha_v = \alpha_c/5\text{–}\alpha_c/10 \).

## Errores comunes
- Confundir constante de tiempo con tiempo de establecimiento (este es ~4 veces mayor).
- Tratar como primer orden un sistema con dinámica oculta (segundo orden mal amortiguado).
- Olvidar que la aproximación de lazo cerrado como primer orden falla si hay resonancias del LCL cerca del ancho de banda.
- Confundir \( \omega_{BW} \) (rad/s) con \( f_{BW} \) (Hz): \( \omega_{BW}=2\pi f_{BW} \).

## 4 — Respuesta en frecuencia del sistema de primer orden

La función de transferencia evaluada en \( s=j\omega \):

$$ G(j\omega) = \frac{K}{j\omega\tau + 1} $$

- **Ganancia DC:** \( |G(0)| = K \) — el valor de la señal de salida en régimen permanente ante una entrada senoidal de amplitud unidad y frecuencia tendiendo a cero.
- **Cruce de −3 dB:** ocurre exactamente en \( \omega = 1/\tau \):

$$ |G(j/\tau)| = \frac{K}{\sqrt{1+(1/\tau\cdot\tau)^2}} = \frac{K}{\sqrt{2}} \approx 0{,}707\,K $$

**Diagrama de Bode asintótico.** La magnitud en dB es:

$$ |G(j\omega)|_{dB} = 20\log K - 20\log\sqrt{1+(\omega\tau)^2} $$

Dos asíntotas: recta horizontal a \( 20\log K \) dB hasta \( \omega = 1/\tau \); luego caída a −20 dB/dec para \( \omega \gg 1/\tau \). El error máximo respecto a la curva real es 3 dB exactamente en la frecuencia de polo.

**Fase:**

$$ \angle G(j\omega) = -\arctan(\omega\tau) $$

- \( \omega \to 0 \): fase → 0°
- \( \omega = 1/\tau \): fase = −45°
- \( \omega \to \infty \): fase → −90° (asíntota)

**Relación tiempo de establecimiento / ancho de banda.** Para el criterio del 2 %:

$$ t_s \approx 4\tau = \frac{4}{\omega_{BW}}, \qquad BW = \frac{1}{\tau} $$

Cuantifica el compromiso diseño temporal-frecuencial: duplicar el BW (mover el polo al doble de frecuencia) reduce \( t_s \) a la mitad.

## 5 — Primer orden como filtro y su realización

**Filtro paso bajo RC.** Con un condensador \( C \) y resistencia \( R \) en serie, la tensión en el condensador vale:

$$ G_{RC}(s) = \frac{1}{RCs+1}, \qquad \tau = RC $$

La constante de tiempo es el producto de la resistencia y la capacidad. Es el filtro analógico de primer orden más simple: un polo en \( s=-1/RC \), sin ceros.

**Filtro digital IIR de primer orden.** La equivalencia discreta más común (Tustin o exponencial exacta) para un polo en \( s=-1/\tau \):

$$ y[n] = \alpha\,y[n-1] + (1-\alpha)\,x[n], \qquad \alpha = e^{-T_s/\tau} $$

donde \( T_s \) es el período de muestreo. Cuando \( \alpha \to 1 \) (filtro lento, \( T_s \ll \tau \)), el filtro suaviza fuertemente. Cuando \( \alpha \to 0 \), la salida sigue directamente la entrada sin filtrado.

**Aplicaciones:**
- **Filtro anti-aliasing:** antes del ADC, \( f_{-3\text{dB}} < f_s/2 \) para cumplir Nyquist.
- **Suavizado de referencia (ramp filter):** evitar escalones bruscos en la referencia de corriente.
- **Medición de potencia:** el cálculo instantáneo de \( p(t)=vi \) tiene rizado al doble de la frecuencia de red; un filtro IIR extrae la potencia media.

**Limitación.** Un solo polo ofrece solo −20 dB/dec de roll-off. Para atenuar ruido de alta frecuencia más eficazmente (p. ej. armónico de conmutación) se necesita orden superior (Butterworth, Chebyshev) o un filtro notch sintonizado.

## 6 — Sistema de primer orden en convertidores: lazo de corriente

**La planta inductor-resistencia.** En el lazo de corriente más simple (solo inductancia de filtro, sin condensador LCL) la planta es:

$$ G_{il}(s) = \frac{1}{Ls+R} = \frac{1/R}{(L/R)s+1} $$

Un primer orden con ganancia DC \( 1/R \) y polo en \( s=-R/L \). La constante de tiempo del inductor es \( \tau_L = L/R \).

**Con PI y cancelación de polo.** Un controlador PI con cero en \( s=-R/L \) cancela el polo de la planta:

$$ C(s) = K_p\frac{s+R/L}{s}, \qquad K_p = \omega_{ci}\,L $$

El lazo abierto tras la cancelación es \( L(s) \approx \omega_{ci}/s \) (un integrador puro) y el lazo cerrado resulta un primer orden:

$$ G_{cl}(s) \approx \frac{1}{\frac{1}{\omega_{ci}}s+1} $$

**Ancho de banda de corriente.** Se elige \( \omega_{ci} = 1/\tau_{ci} \) con la restricción:

$$ \omega_{ci} \lesssim \frac{\omega_{sw}}{10} $$

para asegurar que los retardos de cómputo y PWM (modelados como \( e^{-sT_d} \approx 1/(T_d s + 1) \)) no degraden el margen de fase. Con \( f_{sw}=10\,\text{kHz} \), el BW de corriente típico es \( \omega_{ci} \lesssim 2\pi\cdot1000\,\text{rad/s} \).

**Impacto de la red.** En sistemas con impedancia de red \( L_{grid} \), el polo real de la planta es \( s = -R/(L+L_{grid}) \). Si la red varía (p. ej. variación de la red entre modo isla y modo conectado), el cero del PI ya no cancela el polo y aparece un polo residual que puede degradar el margen de fase. Solución: ajustar \( K_p \) en función de \( L_{grid} \) estimado, o usar gain-scheduling.

<div class="cfig"><img src="figuras/sistema-primer-orden-analisis.png" alt="cuatro paneles: escalon multi-tau, Bode primer orden, filtro IIR en señal ruidosa, BW lazo corriente vs L"><div class="cap">(a) Respuesta al escalón para distintos τ. (b) Bode del primer orden con punto de −3 dB. (c) Filtro IIR primer orden sobre señal ruidosa. (d) Ancho de banda del lazo de corriente en función de la inductancia.</div></div>

## Conceptos relacionados
- [[polos-ceros]] · [[respuesta-segundo-orden]] · [[sintonia-pi-pid]] · [[control-cascada]]

## Referencias
- Ogata, *Ingeniería de Control Moderna*.
- Franklin, Powell, *Feedback Control of Dynamic Systems*, Pearson.
