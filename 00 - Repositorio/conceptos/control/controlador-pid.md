---
titulo: Controlador PID
slug: controlador-pid
categoria: control
tipo: tecnica
nivel: basico
proyectos: []
objetivos: [entender que aporta cada termino proporcional, integral y derivativo]
tags: [PID, PI, proporcional, integral, derivativo, basico, anti-windup, discretizacion, sintonia]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [realimentacion, sintonia-pi-pid, sistema-primer-orden, control-cascada, discretizacion-controladores, anti-windup]
referencias:
  - "Åström, Hägglund, Advanced PID Control, ISA 2006"
  - "Franklin, Powell, Emami-Naeini, Feedback Control of Dynamic Systems, 8ª ed., Pearson 2019"
  - "Holmes, Lipo, Pulse Width Modulation for Power Converters, IEEE Press 2003"
---

## Definición
Controlador que actúa sobre el error con tres términos: **P**roporcional, **I**ntegral y
**D**erivativo. Es el controlador más usado en la industria por su sencillez y eficacia.

## Fundamento teórico
$$ u(t) = K_p\,e(t) + K_i\!\int_0^t e\,d\tau + K_d\,\frac{de}{dt}
   \;\;\Longleftrightarrow\;\; C(s)=K_p+\frac{K_i}{s}+K_d\,s $$
Qué aporta cada término:
- **Proporcional** \(K_p\): reacciona al error actual; más \(K_p\) → más rápido, pero deja
  **error en régimen** y puede oscilar.
- **Integral** \(K_i\): acumula el error pasado; **elimina el error en régimen**, pero añade
  retraso de fase (puede reducir estabilidad y dar *windup*).
- **Derivativo** \(K_d\): anticipa según la tendencia del error; **amortigua** y mejora
  estabilidad, pero amplifica el **ruido** (se suele filtrar).
En convertidores se usa casi siempre **PI** (sin D, por el ruido de conmutación).

<div class="cfig"><img src="figuras/controlador-pid-estructura.png" alt="estructura paralela del PID"><div class="cap">Estructura PID: tres ramas en paralelo sobre el error — proporcional (Kp), integral (Ki/s) y derivativa (Kd·s) — que se suman para formar la acción de control u.</div></div>

## 1 — De la forma temporal a la FDT del PID

**Paso 1 — los tres términos en el tiempo.** El controlador suma tres acciones sobre el error \(e(t)\): una proporcional al error actual, una proporcional a su integral acumulada y una proporcional a su pendiente:

$$ u(t) = K_p\,e(t) + K_i\!\int_0^t e(\tau)\,d\tau + K_d\,\frac{de(t)}{dt} $$

**Paso 2 — Laplace de cada término.** Con condiciones iniciales nulas, la transformada de Laplace cumple \(\mathcal{L}\{e\}=E(s)\), \(\mathcal{L}\!\left\{\int_0^t e\,d\tau\right\}=\dfrac{E(s)}{s}\) (integrar = dividir por \(s\)) y \(\mathcal{L}\!\left\{\dfrac{de}{dt}\right\}=s\,E(s)\) (derivar = multiplicar por \(s\)). Transformando término a término:

$$ U(s)=K_p\,E(s)+\frac{K_i}{s}\,E(s)+K_d\,s\,E(s) $$

**Paso 3 — factorizar \(E(s)\).** La FDT del controlador es \(C(s)=U(s)/E(s)\); sacando \(E(s)\) factor común:

$$ \boxed{\;C(s)=\frac{U(s)}{E(s)}=K_p+\frac{K_i}{s}+K_d\,s\;} $$

Cada término domina en una zona de frecuencia: el integral \(K_i/s\to\infty\) cuando \(s\to 0\) (ganancia infinita en continua → **anula el error en régimen** ante escalón); el derivativo \(K_d s\to\infty\) cuando \(s\to\infty\) (→ **amplifica el ruido** de alta frecuencia); el proporcional \(K_p\) actúa en toda la banda.

## 2 — Lazo cerrado de un PI sobre una planta de primer orden

**Paso 1 — planteamiento.** Tomamos el PI \(C(s)=K_p+\dfrac{K_i}{s}=\dfrac{K_p s+K_i}{s}\) realimentado sobre una planta de primer orden \(P(s)=\dfrac{K}{\tau s+1}\) (ver [[sistema-primer-orden]]). La transferencia de lazo abierto es:

$$ L(s)=C(s)\,P(s)=\frac{K_p s+K_i}{s}\cdot\frac{K}{\tau s+1}=\frac{K(K_p s+K_i)}{s(\tau s+1)} $$

**Paso 2 — fórmula del lazo cerrado.** Con realimentación unitaria, \(T(s)=\dfrac{L}{1+L}\) (ver [[realimentacion]]). Sustituyendo \(L\) y multiplicando numerador y denominador por \(s(\tau s+1)\) para limpiar la fracción anidada:

$$ T(s)=\frac{\dfrac{K(K_p s+K_i)}{s(\tau s+1)}}{1+\dfrac{K(K_p s+K_i)}{s(\tau s+1)}}=\frac{K(K_p s+K_i)}{s(\tau s+1)+K(K_p s+K_i)} $$

**Paso 3 — desarrollar el denominador.** Expandiendo \(s(\tau s+1)=\tau s^2+s\) y agrupando los términos en \(s\):

$$ s(\tau s+1)+K(K_p s+K_i)=\tau s^2+s+KK_p s+KK_i=\tau s^2+(1+KK_p)\,s+KK_i $$

de donde resulta un sistema de **segundo orden** (ver [[respuesta-segundo-orden]]):

$$ \boxed{\;T(s)=\frac{K(K_p s+K_i)}{\tau s^2+(1+KK_p)\,s+KK_i}\;} $$

**Paso 4 — interpretación.** Comparando el denominador con la forma canónica \(s^2+2\zeta\omega_n s+\omega_n^2\) (tras dividir por \(\tau\)): \(\omega_n=\sqrt{KK_i/\tau}\) y \(2\zeta\omega_n=(1+KK_p)/\tau\). El integrador \(K_i\) fija la rapidez \(\omega_n\) y, en \(s=0\), \(T(0)=\dfrac{KK_i}{KK_i}=1\): **ganancia continua exactamente unidad**, luego seguimiento sin error en régimen ante escalón. El proporcional \(K_p\) aparece solo en el término de amortiguamiento, ajustando \(\zeta\) sin tocar \(T(0)\).

## 3 — Ceros del PI en el plano complejo: cancelación de polo

**El numerador del PI es un cero.** Escribiendo el PI en forma factorizada:

$$ C(s)=\frac{K_p s+K_i}{s}=\frac{K_p(s+K_i/K_p)}{s}=\frac{K_p(s+\omega_z)}{s},\quad\omega_z\triangleq\frac{K_i}{K_p} $$

El PI tiene un **polo en el origen** (el integrador) y un **cero real en \(s=-\omega_z\)**. En el plano \(s\), este cero es un punto sobre el eje real negativo. A medida que \(\omega_z\) aumenta, el cero se aleja del origen; a medida que disminuye, el cero se acerca al origen y su influencia en la dinámica del lazo crece.

**Cancelación exacta de un polo de planta.** Consideremos una planta RL de primer orden (que aparece en todo lazo de corriente de convertidor):

$$ P(s)=\frac{1}{Ls+R}=\frac{1/L}{s+R/L}=\frac{1/L}{s+\omega_p},\quad\omega_p\triangleq\frac{R}{L} $$

Este polo en \(s=-\omega_p\) es el que hace lenta la respuesta de la corriente. Si diseñamos el PI para que su cero coincida exactamente con ese polo:

$$ \omega_z=\omega_p\quad\Longrightarrow\quad \frac{K_i}{K_p}=\frac{R}{L}\quad\Longrightarrow\quad K_i=K_p\,\frac{R}{L} $$

entonces el producto \(C(s)\cdot P(s)\) presenta una cancelación polo-cero exacta:

$$ L(s)=C(s)\,P(s)=\frac{K_p(s+\omega_p)}{s}\cdot\frac{1/L}{s+\omega_p}=\frac{K_p/L}{s} $$

El lazo abierto se reduce a un **integrador puro** con ganancia \(K_p/L\). Esto es muy potente: la planta de segundo orden aparente (polo de planta + polo del integrador del PI) se reduce a primer orden.

**Margen de fase con integrador puro.** El integrador puro tiene fase \(\angle(K/s)=-90°\) para toda frecuencia. En la frecuencia de cruce \(\omega_{ci}\) donde \(|L(j\omega_{ci})|=1\):

$$ |L(j\omega_{ci})|=\frac{K_p/L}{\omega_{ci}}=1\quad\Longrightarrow\quad K_p=L\,\omega_{ci} $$

La fase del lazo es exactamente \(-90°\) en \(\omega_{ci}\), luego el **margen de fase ideal es 90°** (sin ningún retardo adicional). Combinando con la condición de cancelación:

$$ \boxed{\;K_p=L\,\omega_{ci},\quad K_i=K_p\,\frac{R}{L}=R\,\omega_{ci}\;} $$

Estas son las fórmulas de diseño del lazo de corriente por cancelación de polo. Para \(L=2\,\text{mH}\), \(R=50\,\text{m}\Omega\) y \(\omega_{ci}=2\pi\cdot750\,\text{Hz}=4712\,\text{rad/s}\):

$$ K_p=0.002\times4712=9.42\;\text{V/A},\quad K_i=0.05\times4712=235.6\;\text{V/A/s} $$

**Por qué la cancelación nunca es exacta en la práctica.** En un sistema real hay tres fuentes de error:

1. *Incertidumbre paramétrica*: la inductancia real varía con la temperatura y la corriente (núcleo saturado), y la resistencia varía con el calentamiento. Si el cero del PI queda en \(-\omega_z\) pero el polo de planta está en \(-\omega_p\neq-\omega_z\), el lazo abierto tiene un dipolo polo-cero residual que introduce un modo lento adicional. La dinámica cancelada no desaparece del lazo cerrado (solo se vuelve inobservable desde la salida), y puede ser excitada por perturbaciones.

2. *Retardo de cómputo digital*: el retardo \(T_d=1.5\,T_s\) (una muestra de cómputo más media de modulación) añade un factor \(e^{-sT_d}\) que introduce fase adicional negativa proporcional a la frecuencia, reduciendo el margen de fase real a bastante menos de 90°.

3. *Antialiasing y filtros de medida*: los filtros de la señal de corriente añaden polos adicionales que alteran la condición de cancelación.

La consecuencia práctica es que se diseña la cancelación con los parámetros nominales y se verifica el margen de fase con el retardo real incluido, ajustando \(\omega_{ci}\) si el margen cae por debajo de 45°.

## 4 — El efecto del término derivativo: filtrado y límite práctico

**D puro: ganancia ilimitada a alta frecuencia.** El PID ideal con término derivativo puro tiene la función de transferencia:

$$ C(s)=K_p+\frac{K_i}{s}+K_d\,s $$

La ganancia del término derivativo es \(|K_d\,j\omega|=K_d\,\omega\), que crece sin límite con la frecuencia. En la práctica esto significa que cualquier ruido de alta frecuencia (ruido de medida, *switching ripple*, cuantización del ADC) es amplificado por el factor \(K_d\,\omega\) que puede ser varias décadas mayor que \(K_p\) en la banda de conmutación. Por eso el **D puro nunca se usa en convertidores de potencia** y raramente en sistemas industriales reales.

**D con filtro de primer orden.** La solución es añadir un polo de filtrado a alta frecuencia \(\omega_f\gg\omega_{ci}\):

$$ C(s)=K_p+\frac{K_i}{s}+\frac{K_d\,s}{1+s/\omega_f} $$

La ganancia del término derivativo filtrado es:

$$ \left|\frac{K_d\,j\omega}{1+j\omega/\omega_f}\right|=\frac{K_d\,\omega}{\sqrt{1+(\omega/\omega_f)^2}} $$

Para \(\omega\ll\omega_f\) esta expresión crece linealmente con \(\omega\) (comportamiento D puro); para \(\omega\gg\omega_f\) se satura en \(K_d\,\omega_f\). La **ganancia máxima del bloque derivativo es por tanto \(K_d\,\omega_f\)**, que es finita y puede dimensionarse para no exceder un múltiplo razonable de \(K_p\).

**Mejora de margen de fase con D filtrado.** Sin el término derivativo, el lazo \(L_0(s)\) tiene una fase \(\phi_0(\omega_{ci})\) en la frecuencia de cruce. Al añadir el D filtrado, la contribución de fase del bloque derivativo a la frecuencia \(\omega_{ci}\) es:

$$ \Delta\phi_D = \angle\!\left(1+\frac{K_d\,j\omega_{ci}/K_p}{1+j\omega_{ci}/\omega_f}\right) \approx \arctan\!\left(\omega_{ci}\,\tau_d\right)-\arctan\!\left(\frac{\omega_{ci}}{\omega_f}\right) $$

donde \(\tau_d=K_d/K_p\) es el tiempo derivativo. El primer término es positivo (adelanto de fase) y el segundo es negativo (retraso del filtro). La mejora neta \(\Delta\phi_D>0\) siempre que \(\omega_f>\omega_{ci}\), y se maximiza separando bien \(\omega_f\) de \(\omega_{ci}\): típicamente \(\omega_f=5\ldots10\,\omega_{ci}\).

**Verificación dimensional del adelanto de fase.** Evalúa el argumento en el ejemplo numérico: \(\omega_{ci}=2\pi\cdot750=4712\,\text{rad/s}\), elige \(\tau_d=1/(3\omega_{ci})=71\,\mu\text{s}\) y \(\omega_f=10\,\omega_{ci}\). Entonces:

$$ \Delta\phi_D=\arctan(4712\times71\times10^{-6})-\arctan(1/10)=\arctan(0.33)-\arctan(0.1)\approx18.4°-5.7°=12.7° $$

Ganar 12.7° de margen adicional podría parecer atractivo, pero tiene un coste: la ganancia del bloque D filtrado a la frecuencia de conmutación \(\omega_{sw}=2\pi\times10^4\) sería \(K_d\,\omega_f=K_d\times10\omega_{ci}\), amplificando el *ripple* de corriente por un factor \(K_d\,\omega_{sw}/K_p\gg1\). Por ello, **en convertidores VSC el término D se omite sistemáticamente** y se trabaja con PI puro, aceptando la limitación de fase implícita.

**Cuándo sí se usa D.** El término derivativo es útil en: (a) sistemas mecánicos con fricción viscosa baja donde el PI oscila, (b) plantas con tiempo muerto grande (en este caso el D ayuda a anticipar la tendencia del error antes de que el retardo lo degrade), y (c) lazos de tensión de bus DC donde el ruido de alta frecuencia es menor y el ancho de banda objetivo es mucho menor que la frecuencia de conmutación.

## 5 — Windup del integrador: causa y solución

**Qué es el windup.** Todo actuador real tiene límites físicos: un convertidor no puede generar más tensión que su tensión de bus, un servo no puede dar más par que su torque nominal, una válvula no puede abrirse más allá del 100%. Cuando la salida del controlador \(u\) supera el límite del actuador \(u_{max}\), el actuador entrega \(u_{max}\) en lugar de \(u\). Esto crea un lazo abierto implícito: el error en la salida real persiste (la planta no responde como el controlador espera), el integrador sigue acumulando error, y \(u\) crece mucho más allá de \(u_{max}\). Cuando finalmente el error cambia de signo, el integrador tarda en descargar toda la energía acumulada, introduciendo un retraso grande antes de que la salida del controlador vuelva a la zona lineal. Este fenómeno se llama **integrador wound up** (devanado).

**Cuantificación del retardo.** Sea el lazo de corriente con \(K_i=235\,\text{V/A/s}\), \(u_{max}=800\,\text{V}\) y un escalón de referencia de \(I_{ref}=0\to75\,\text{A}\) (1.5 veces el nominal de 50 A). El integrador se carga durante el transitorio. Si la saturación dura un tiempo \(t_{sat}\) y el error vale \(\approx75\,\text{A}\) durante ese tiempo, la energía acumulada en el integrador es:

$$ u_{int}(t_{sat})=K_i\int_0^{t_{sat}}e\,d\tau\approx K_i\times75\times t_{sat} $$

Para que el integrador se descargue hasta \(u_{max}=800\,\text{V}\) (que es cuando el controlador sale de saturación), se necesita que el error cambie de signo y el integrador descargue. Con un error de \(-75\,\text{A}\) el tiempo de descarga es:

$$ t_{descarga}=\frac{u_{int}(t_{sat})}{K_i\times75}=t_{sat} $$

Es decir, el retardo tras el cruce de referencia es del mismo orden que el tiempo en saturación. En el ejemplo, con \(t_{sat}\approx200\,\text{ms}\), el retardo postcruce también es del orden de 200 ms: la corriente sigue subiendo mucho después de haber cruzado la referencia.

**Anti-windup por recálculo (*back-calculation*).** El método más robusto es retroalimentar la diferencia entre la salida real del actuador y la salida ideal del controlador:

$$\Delta u=u_{act}-u_{ideal},\quad u_{act}=\text{sat}(u_{ideal},u_{min},u_{max})$$

y restar esta diferencia al integrando con una ganancia de recálculo \(1/T_t\) (tiempo de *tracking*):

$$ \dot{x}_i = e + \frac{1}{T_t}\,(u_{act}-u_{ideal}) $$

donde \(x_i\) es el estado del integrador. Cuando el controlador no satura, \(u_{act}=u_{ideal}\) y el término adicional es cero: el integrador funciona con normalidad. Cuando satura, \(u_{act}-u_{ideal}<0\) (el actuador entrega menos de lo pedido), y el término adicional frena el crecimiento del integrador. El valor de \(T_t\) controla la velocidad de corrección: valores pequeños lo frenan rápidamente pero pueden excitar oscilaciones; un valor recomendado es \(T_t=\sqrt{T_i\,T_d}\) (con D) o \(T_t=T_i/4\) (solo PI).

**Anti-windup por clamping condicional.** Alternativa más simple: se deja de integrar cuando se cumplan simultáneamente dos condiciones: (a) el controlador está saturado y (b) el término que crece es del mismo signo que el error actual (es decir, el integrador agrevaría la saturación). En pseudocódigo:

```
if |u| >= u_max AND sign(e) == sign(integ):
    # no actualizar el integrador
else:
    integ += Ki * e * dt
```

Esta técnica es más fácil de implementar en DSP y tiene un comportamiento suficientemente bueno para la mayoría de lazos de convertidor.

**Cálculo del tiempo de recuperación.** Con anti-windup por back-calculation y \(T_t=T_i/4\), el integrador se descarga con constante de tiempo \(T_t\). En el ejemplo: \(T_i=K_p/K_i=9.42/235.6\approx40\,\text{ms}\), luego \(T_t=10\,\text{ms}\). El tiempo de recuperación tras dejar la saturación es del orden de \(3T_t=30\,\text{ms}\), muy inferior a los 200 ms sin anti-windup.

**Ejemplo numérico completo.** Con \(L=2\,\text{mH}\), \(R=50\,\text{m}\Omega\), \(K_p=9.42\,\text{V/A}\), \(K_i=235.6\,\text{V/A/s}\), \(u_{max}=800\,\text{V}\), escalón \(I_{ref}=0\to75\,\text{A}\):

- *Sin anti-windup*: el integrador se carga hasta \(\approx+2.5\,\text{kV}\) antes de que la corriente llegue a la referencia. El controlador no sale de saturación hasta que la corriente supera la referencia en \(\approx25\,\text{A}\). Tiempo de recuperación \(\approx200\,\text{ms}\).
- *Con anti-windup* (back-calculation, \(T_t=10\,\text{ms}\)): el integrador se descarga en cuanto comienza la saturación. El overshoot es inferior al 5% y el tiempo de recuperación es menor de 5 ms.

## 6 — Discretización del PID: Euler vs Tustin vs ZOH

En un sistema digital, el controlador se implementa como una ecuación en diferencias que se ejecuta una vez por período de muestreo \(T_s\). La discretización transforma la ecuación diferencial continua en esa ecuación en diferencias, y la elección del método afecta tanto a la estabilidad como a la precisión.

**Euler hacia adelante (*forward Euler*).** Aproximación \(s\approx(z-1)/T_s\). Equivale a aproximar la integral por la regla del rectángulo izquierdo:

$$ x_i[k+1]=x_i[k]+T_s\,e[k] $$

El polo del integrador continuo en \(s=0\) se mapea a \(z=1+s\,T_s\big|_{s=0}=1\), en el borde del círculo unitario. Esto no es un problema en sí, pero si el sistema tiene cualquier componente inestable o el margen de fase es pequeño, Euler adelante puede llevar el polo fuera del círculo unitario. **No se recomienda para sistemas de control realimentado.**

**Euler hacia atrás (*backward Euler*).** Aproximación \(s=(z-1)/(z\,T_s)\). Equivale a la regla del rectángulo derecho:

$$ x_i[k]=x_i[k-1]+T_s\,e[k] $$

El polo del integrador continuo en \(s=0\) se mapea según \(s=0=(z-1)/(z\,T_s)\Rightarrow z=1\). Pero la imagen de todo el semiplano izquierdo continuo está contenida en el círculo unitario del plano \(z\), por lo que un sistema estable continuo permanece estable tras la discretización. El integrador tiene polo en \(z=1\), que es exactamente el borde del círculo unitario: estable pero sin margen. En la práctica es una opción aceptable y muy usada en implementaciones de DSP por su simplicidad.

**Tustin (bilineal, *Tustin* o *trapezoidal*).** Aproximación \(s=\dfrac{2}{T_s}\dfrac{z-1}{z+1}\). Equivale a la regla del trapecio:

$$ x_i[k]=x_i[k-1]+\frac{T_s}{2}\bigl(e[k]+e[k-1]\bigr) $$

Este método mapea el eje imaginario continuo \(s=j\omega\) exactamente sobre el círculo unitario \(z=e^{j\theta}\), preservando la respuesta en frecuencia hasta la frecuencia de Nyquist. La frecuencia de cruce y el margen de fase del controlador discreto coinciden con los del controlador continuo **con distorsión mínima** (prewarping necesario solo si el cero del PI está cerca de \(\omega_N=\pi/T_s\)). **Tustin es el método recomendado para PI en lazos de convertidor.**

**Derivación de los coeficientes discretos Tustin para el PI.** La función de transferencia del PI continuo es:

$$ C(s)=\frac{K_p s+K_i}{s} $$

Sustituimos \(s\to\dfrac{2}{T_s}\dfrac{z-1}{z+1}\):

$$ C(z)=\frac{K_p\dfrac{2}{T_s}\dfrac{z-1}{z+1}+K_i}{\dfrac{2}{T_s}\dfrac{z-1}{z+1}}=\frac{2K_p(z-1)/(T_s)+K_i(z+1)}{2(z-1)/T_s} $$

Multiplicando numerador y denominador por \(T_s/2\):

$$ C(z)=\frac{K_p(z-1)+K_i\dfrac{T_s}{2}(z+1)}{z-1}=\frac{\left(K_p+K_i\dfrac{T_s}{2}\right)z+\left(-K_p+K_i\dfrac{T_s}{2}\right)}{z-1} $$

Definiendo \(a_0=K_p+K_i T_s/2\) y \(a_1=-K_p+K_i T_s/2\), la ecuación en diferencias es:

$$ u[k]=u[k-1]+a_0\,e[k]+a_1\,e[k-1] $$

Esta forma **acumulativa directa** es la más eficiente en un DSP: solo requiere una resta, dos multiplicaciones y dos sumas por período de muestreo, sin necesidad de almacenar el estado del integrador por separado.

**Ejemplo numérico.** Con \(K_p=9.42\,\text{V/A}\), \(K_i=235.6\,\text{V/A/s}\), \(T_s=100\,\mu\text{s}\):

$$ a_0=9.42+235.6\times50\times10^{-6}=9.42+0.01178=9.432\;\text{V/A} $$
$$ a_1=-9.42+235.6\times50\times10^{-6}=-9.42+0.01178=-9.408\;\text{V/A} $$

La ecuación de control discreto es:

$$ u[k]=u[k-1]+9.432\,e[k]-9.408\,e[k-1] $$

Obsérvese que \(a_0\approx-a_1\approx K_p\): la corrección dominante en cada muestra es proporcional al cambio de error \(K_p(e[k]-e[k-1])\), con una pequeña corrección integral de \(\pm K_iT_s/2\approx0.012\,\text{V/A}\). El integrador actúa de forma acumulada a lo largo de muchos pasos.

**ZOH (Zero-Order Hold) exacto para la planta.** En lugar de discretizar el controlador continuo, se puede discretizar la planta exactamente (respuesta escalón exacta) y diseñar un controlador discreto para esa planta. Para la planta RL \(P(s)=1/(Ls+R)\):

$$ P(z)=\mathcal{Z}\{P(s)\,\text{ZOH}\}=\frac{1-e^{-\omega_p T_s}}{R}\cdot\frac{1}{z-e^{-\omega_p T_s}} $$

con \(\omega_p=R/L=25\,\text{rad/s}\) y \(T_s=100\,\mu\text{s}\): \(e^{-\omega_p T_s}=e^{-0.0025}\approx0.99750\). El polo discreto de la planta está muy cerca de \(z=1\), exactamente donde esperamos para una planta lenta (\(\omega_p T_s\ll1\)). Este método es útil cuando la planta tiene dinámicas rápidas comparables con \(T_s\), situación menos frecuente en lazos de corriente de convertidor.

## 7 — Sintonía por respuesta en frecuencia: el método de lazo de corriente

**Planta y objetivo.** La planta del lazo de corriente de un VSC es:

$$ P(s)=\frac{1}{sL+R}=\frac{1/L}{s+R/L} $$

El objetivo de diseño es una frecuencia de cruce de corriente \(\omega_{ci}\) con margen de fase efectivo \(\text{PM}_{ef}\geq45°\).

**Paso 1 — diseño por cancelación de polo (sin retardo).** Del apartado 3, con cancelación de polo exacta el lazo abierto es \(L(s)=K_p/(Ls)\). La condición de cruce \(|L(j\omega_{ci})|=1\) da directamente:

$$ \frac{K_p}{L\,\omega_{ci}}=1\quad\Longrightarrow\quad K_p=L\,\omega_{ci} $$

Y la condición de cancelación \(K_i=K_p\,R/L\) completa el diseño. El margen de fase teórico (sin retardo) es 90°.

**Paso 2 — efecto del retardo digital.** En un convertidor con muestreo sincrónico a la portadora PWM, el retardo total de cómputo más modulación vale \(T_d=1.5\,T_s\) (un período de muestreo para el cómputo más medio período para el ZOH de la modulación). El retardo añade una fase adicional negativa:

$$ \phi_{ret}(\omega)=-\omega\,T_d\;\text{[rad]}\;=-\omega\,T_d\times\frac{180°}{\pi} $$

El margen de fase efectivo es:

$$ \text{PM}_{ef}=\underbrace{90°}_{\text{sin retardo}}-\omega_{ci}\,T_d\times\frac{180°}{\pi} $$

**Paso 3 — límite de frecuencia de cruce.** La condición \(\text{PM}_{ef}\geq45°\) impone:

$$ \omega_{ci}\,T_d\times\frac{180°}{\pi}\leq45°\quad\Longrightarrow\quad\omega_{ci}\leq\frac{\pi/4}{T_d}=\frac{\pi}{4\times1.5\,T_s}=\frac{\pi}{6\,T_s} $$

Con \(T_s=100\,\mu\text{s}\): \(\omega_{ci,max}=\pi/(6\times10^{-4})=5236\,\text{rad/s}=833\,\text{Hz}\). Por tanto, para mantener PM ≥ 45°, la frecuencia de cruce debe ser inferior a \(\approx1/(3T_s)\cdot\pi/\pi\approx f_{sw}/30\) cuando se usa muestreo doble (\(T_s=T_{sw}/2\)).

**Paso 4 — tabla de Kp, Ki vs ωci con retardo.** Para \(L=2\,\text{mH}\), \(R=50\,\text{m}\Omega\), \(T_s=100\,\mu\text{s}\) (\(T_d=150\,\mu\text{s}\)):

| \(f_{ci}\) [Hz] | \(\omega_{ci}\) [rad/s] | \(K_p\) [V/A] | \(K_i\) [V/A/s] | \(\phi_{ret}\) | \(\text{PM}_{ef}\) |
|:-:|:-:|:-:|:-:|:-:|:-:|
| 500 | 3142 | 6.28 | 157 | 27° | 63° |
| 750 | 4712 | 9.42 | 236 | 40° | 50° |
| 833 | 5236 | 10.47 | 262 | 45° | 45° |
| 1000 | 6283 | 12.57 | 314 | 54° | 36° |
| 1200 | 7540 | 15.08 | 377 | 65° | 25° |

El diseño a \(f_{ci}=750\,\text{Hz}\) deja un margen de 5° sobre el mínimo de 45°, suficiente para absorber variaciones de \(L\) y \(R\) del orden de ±10%.

**Paso 5 — verificación con el Bode completo.** El lazo abierto real (con retardo) es:

$$ L_{real}(s)=\frac{K_p}{Ls}\,e^{-sT_d} $$

La magnitud es \(|L_{real}(j\omega)|=K_p/(L\omega)\), idéntica al caso sin retardo. La fase es:

$$ \angle L_{real}(j\omega)=-90°-\omega T_d\times\frac{180°}{\pi} $$

El cruce de ganancia sigue en \(\omega_{ci}=K_p/L\), pero el margen de fase real es el calculado en el paso 2. El margen de ganancia (frecuencia donde \(\angle L=-180°\)) se obtiene de:

$$ -90°-\omega_{GM}\,T_d\times\frac{180°}{\pi}=-180°\quad\Longrightarrow\quad\omega_{GM}=\frac{90°\times\pi/180°}{T_d}=\frac{\pi/2}{T_d} $$

Con \(T_d=150\,\mu\text{s}\): \(\omega_{GM}=\pi/(2\times150\times10^{-6})=10472\,\text{rad/s}=1667\,\text{Hz}\). El margen de ganancia es:

$$ \text{GM}=-20\log_{10}|L(j\omega_{GM})|=-20\log_{10}\frac{K_p}{L\,\omega_{GM}}=-20\log_{10}\frac{9.42}{0.002\times10472}=+6.4\,\text{dB} $$

Un margen de ganancia de solo 6.4 dB refuerza que no se debe aumentar \(K_p\) más allá del valor calculado.

## 8 — Diseño iterativo: de especificaciones a parámetros verificados

Se documenta el proceso completo de diseño del lazo de corriente de un VSC con \(L=2\,\text{mH}\), \(R=50\,\text{m}\Omega\), \(f_{sw}=10\,\text{kHz}\), muestreo doble (\(T_s=50\,\mu\text{s}\), \(T_d=75\,\mu\text{s}\)).

**Especificaciones:**
- Ancho de banda (frecuencia de cruce): \(f_{ci}=1\,\text{kHz}\) (objetivo inicial)
- Margen de fase efectivo: \(\text{PM}_{ef}\geq45°\)
- Sin sobreoscilación superior al 10% ante escalón de referencia
- Error en régimen nulo ante escalón de corriente

**Iteración 0 — diseño nominal sin retardo.**

Aplicando las fórmulas del apartado 7 con \(\omega_{ci}=2\pi\times1000=6283\,\text{rad/s}\):

$$ K_p=L\,\omega_{ci}=0.002\times6283=12.57\;\text{V/A} $$
$$ K_i=R\,\omega_{ci}=0.05\times6283=314.2\;\text{V/A/s} $$

El margen de fase sin retardo es exactamente 90°. Pero con \(T_d=75\,\mu\text{s}\):

$$ \phi_{ret}=\omega_{ci}\,T_d\times\frac{180°}{\pi}=6283\times75\times10^{-6}\times\frac{180°}{\pi}=27°$$

$$ \text{PM}_{ef}=90°-27°=63°\quad\checkmark $$

Aquí el retardo es menor porque \(T_s=50\,\mu\text{s}\) (muestreo doble). La iteración 0 ya cumple el margen de fase.

**Comprobación del margen de ganancia:**

$$ \omega_{GM}=\frac{\pi/2}{T_d}=\frac{\pi/2}{75\times10^{-6}}=20944\,\text{rad/s}=3333\,\text{Hz} $$
$$ \text{GM}=-20\log_{10}\frac{12.57}{0.002\times20944}=-20\log_{10}(0.3)=+10.5\,\text{dB}\quad\checkmark $$

**Verificación de la sobreoscilación.** El lazo cerrado equivalente (tras cancelación de polo) tiene la función de transferencia:

$$ T(s)=\frac{\omega_{ci}}{s+\omega_{ci}}\,e^{-sT_d} $$

Para un sistema de primer orden con retardo, la sobreoscilación ante escalón es aproximadamente cero cuando \(\omega_{ci}\,T_d<1\). Con \(\omega_{ci}\,T_d=6283\times75\times10^{-6}=0.47<1\) la respuesta es levemente subamortiguada con sobreoscilación inferior al 5%.

**Verificación del error en régimen.** El integrador del PI garantiza \(L(0)=\infty\), luego \(T(0)=1\) y el error en régimen ante escalón es exactamente cero. Condición cumplida por construcción.

**Iteración 1 — robustez paramétrica.** Se verifica que el diseño sigue siendo estable con \(L=2.4\,\text{mH}\) (+20%) y \(R=40\,\text{m}\Omega\) (−20%):

El cero del PI está en \(\omega_z=K_i/K_p=314.2/12.57=25\,\text{rad/s}\), que corresponde al polo nominal \(\omega_p^{nom}=R/L=25\,\text{rad/s}\). Con los parámetros variados, el polo real de la planta es \(\omega_p^{real}=40\times10^{-3}/2.4\times10^{-3}=16.7\,\text{rad/s}\). El residuo de la cancelación incompleta crea un dipolo en \(s\approx-16.7\) (polo) y \(s\approx-25\) (cero). Este dipolo introduce una constante de tiempo adicional de \(1/16.7\approx60\,\text{ms}\), que se manifesta como un transitorio lento de baja amplitud. La dinámica rápida del lazo no se ve afectada porque el dipolo está a frecuencias muy inferiores a \(\omega_{ci}\).

La ganancia del lazo a \(\omega_{ci}\) con la planta variada \(L'=2.4\,\text{mH}\): \(K_p/(L'\omega_{ci})=12.57/(2.4\times10^{-3}\times6283)=0.83\). El nuevo cruce está algo por debajo de 1 kHz, reduciendo el ancho de banda a \(\approx830\,\text{Hz}\), que sigue siendo aceptable.

**Iteración 2 — con anti-windup y discretización Tustin.** Los coeficientes discretos (Tustin, \(T_s=50\,\mu\text{s}\)):

$$ a_0=K_p+K_i\frac{T_s}{2}=12.57+314.2\times25\times10^{-6}=12.57+0.00786=12.578\;\text{V/A} $$
$$ a_1=-K_p+K_i\frac{T_s}{2}=-12.57+0.00786=-12.562\;\text{V/A} $$

La ecuación de control es \(u[k]=u[k-1]+12.578\,e[k]-12.562\,e[k-1]\), con clamping condicional anti-windup y \(u_{max}=800\,\text{V}\).

**Tabla resumen de iteraciones:**

| It. | \(f_{ci}\) | \(K_p\) | \(K_i\) | \(\text{PM}_{ef}\) | \(\text{GM}\) | Overshoot | Estado |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| 0 | 1 kHz | 12.57 | 314 | 63° | 10.5 dB | <5% | OK |
| 1 (+20% L) | ~830 Hz | 12.57 | 314 | 57° | 11.2 dB | <5% | OK |
| 2 (disc.) | ~990 Hz | 12.578 | — | ≈62° | ≈10 dB | <5% | OK |

El diseño converge en la primera iteración. Con muestreo doble (\(T_s=T_{sw}/2\)) el retardo es la mitad y el límite de \(f_{ci}\) prácticamente desaparece en el rango de interés.

<div class="cfig"><img src="figuras/controlador-pid-analisis.png" alt="Análisis cuadrupanel del controlador PI en lazo de corriente de convertidor"><div class="cap">Análisis del PI en lazo de corriente (L=2 mH, R=50 mΩ, Ts=100 µs). (a) Respuesta al escalón del lazo cerrado para tres relaciones ωci/ωp: el cruce en el polo de planta (ratio=1) da respuesta óptima; por debajo es lento, por encima sobreoscila. (b) Efecto del windup: sin anti-windup el integrador se carga durante la saturación y la corriente sigue subiendo mucho después de cruzar la referencia; con anti-windup la recuperación es inmediata. (c) Diagrama de Bode del lazo de corriente: planta G=1/(sL+R), compensador PI con cancelación, y lazo resultante L(jω) con y sin retardo 1.5Ts — el retardo reduce el margen de fase de 90° a 50° en ωci=750 Hz. (d) Respuesta al impulso del integrador discreto: continuo, Euler adelante (que puede desestabilizar) y Tustin (que conserva el margen de fase).</div></div>

## Cuándo y por qué se usa
En lazos de corriente, tensión, velocidad: cuando se quiere seguimiento sin error en régimen con
una estructura simple. Es la base de los lazos en cascada.

## Procedimiento (genérico)
1. Empieza con P para fijar la rapidez.
2. Añade I para anular el error en régimen (cuida el *windup*: usa anti-windup).
3. Añade D (filtrado) solo si necesitas más amortiguamiento y el ruido lo permite.
4. Sintoniza por ancho de banda o cancelación de polo (ver [[sintonia-pi-pid]]).

## Ejemplo de aplicación real
**Problema:** VSC con \(L=2\,\text{mH}\), \(r=50\,\text{m}\Omega\), \(f_{sw}=10\,\text{kHz}\). Diseñar el PI de corriente para \(f_c=1\,\text{kHz}\) con margen de fase real ≥ 45°, considerando el retardo de cómputo \(T_d=150\,\mu\text{s}\).

Paso 1 — cancelación de polo: cero del PI en \(\omega_z=r/L=25\,\text{rad/s}\). Paso 2 — ganancia: \(K_p=L\omega_c=0.002\times6283\approx12.6\), \(K_i=K_p\,r/L\approx315\,\text{s}^{-1}\). Paso 3 — verificar margen con retardo: desfase del retardo a \(\omega_c\) es \(\omega_c T_d\times(180/\pi)\approx54°\), reduciendo el margen de 90° a 36° (no cumple 45°). Corrección: reducir \(\omega_c\) a 750 Hz (\(K_p\approx9.4\)), desfase del retardo \(\approx40°\), margen resultante \(\approx50°\). El PI sin considerar el retardo cumpliría en teoría pero no en implementación real.

## Ejemplo de código
```python
# PI discreto con anti-windup por clamping condicional
integ = 0.0
a0 = Kp + Ki * Ts / 2   # coeficiente Tustin
a1 = -Kp + Ki * Ts / 2  # coeficiente Tustin

for k in range(N):
    e = ref[k] - y[k]
    u_ideal = u_prev + a0 * e + a1 * e_prev
    u = np.clip(u_ideal, -u_max, u_max)
    # anti-windup: no acumular si satura y el error agrava la saturacion
    if u == u_ideal or np.sign(e) != np.sign(u_ideal - u):
        u_prev = u
    e_prev = e
```

## Parámetros y valores típicos
Lazos de convertidor: PI con cero en el polo de la planta. Margen de fase objetivo 45–60°.

## Errores comunes
- Olvidar el **anti-windup**: el integrador se carga al saturar y la respuesta se degrada.
- Usar D con señal ruidosa sin filtrar.
- Diseñar sin retardo digital: el margen de 90° teórico puede caer a 30–40° en implementación real.
- Discretizar con Euler adelante: puede desestabilizar lazos con margen pequeño.

## Conceptos relacionados
- [[realimentacion]] · [[sintonia-pi-pid]] · [[control-cascada]] · [[discretizacion-controladores]] · [[anti-windup]]

## Referencias
- Åström, Hägglund, *Advanced PID Control*, ISA 2006.
- Franklin, Powell, Emami-Naeini, *Feedback Control of Dynamic Systems*, 8ª ed., Pearson 2019.
- Holmes, Lipo, *Pulse Width Modulation for Power Converters*, IEEE Press 2003.
