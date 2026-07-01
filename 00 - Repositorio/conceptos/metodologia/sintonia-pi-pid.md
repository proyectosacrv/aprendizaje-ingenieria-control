---
titulo: Sintonía de PI/PID (cancelación de polo, óptimo de módulo)
slug: sintonia-pi-pid
categoria: metodologia
tipo: metodo
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [obtener las ganancias de un PI a partir del ancho de banda]
tags: [PI, PID, sintonia, cancelacion-polo, modulo-optimo]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [metodos-sintesis-control, control-cascada, especificaciones-control, loop-shaping]
referencias:
  - "Aström, Hägglund, Advanced PID Control, ISA 2006"
---

## Definición
Métodos sistemáticos para fijar las ganancias de un controlador PI/PID a partir del modelo de la
planta y del ancho de banda deseado, en lugar de prueba y error.

## Fundamento teórico
Para una planta de primer orden \( G(s)=\dfrac{K}{1+\tau s} \) (típico del lazo de corriente,
\( \tau=L/R \)) con PI \( C(s)=K_p+\dfrac{K_i}{s} \):
- **Cancelación de polo**: coloca el cero del PI sobre el polo de la planta
  (\( K_i/K_p = 1/\tau = R/L \)), dejando un lazo de primer orden con ancho de banda
  \( \omega_c \): \( K_p = L\,\omega_c \), \( K_i = R\,\omega_c \).
- **Óptimo de módulo** (plantas con retardo/2º orden): hace \( |T(j\omega)|\approx 1 \) en la
  banda; bueno para lazos internos.
- **Óptimo simétrico**: para plantas con integrador (lazos de tensión/posición), maximiza el
  margen de fase a la frecuencia de cruce.

<div class="cfig"><img src="figuras/sintonia-pi-pid-cancelacion.png" alt="cancelacion de polo y lazo resultante"><div class="cap">Cancelación de polo: el cero del PI se coloca sobre el polo de la planta; el lazo cerrado queda como un primer orden limpio del ancho de banda elegido (Kp=Lωc, Ki=Rωc).</div></div>

## 1 — Derivación de la cancelación de polo: de planta L,R a \( K_p, K_i \)
**Paso 1 — modelo del lazo.** La planta es el inductor de red: \( G(s)=\dfrac{1}{R+sL}=\dfrac{K}{1+\tau s} \) con \( K=1/R \), \( \tau=L/R \). El controlador PI es \( C(s)=K_p+\dfrac{K_i}{s}=K_p\dfrac{1+s\,K_p/K_i}{s} \). La ganancia de lazo abierto resulta:

$$ L(s)=C(s)\,G(s)=K_p\,\frac{1+s(K_p/K_i)}{s}\cdot\frac{1/R}{1+s\,L/R} $$

**Paso 2 — condición de cancelación.** Se elige el cero del PI en el polo de la planta, es decir \( K_p/K_i = \tau = L/R \). Con ello el factor \( (1+sL/R) \) del denominador de \( G \) se cancela exactamente con el cero del numerador del PI:

$$ L(s)\big|_{\text{cancelado}}=\frac{K_p/R}{s} $$

El lazo abierto queda como un **integrador puro** de ganancia \( K_p/R \).

**Paso 3 — imponer el ancho de banda.** La frecuencia de cruce de ganancia es el \( \omega \) donde \( |L(j\omega)|=1 \):

$$ \left|\frac{K_p/R}{j\omega_c}\right|=1 \;\Rightarrow\; \frac{K_p}{R\,\omega_c}=1 \;\Rightarrow\; \boxed{K_p = R\,\omega_c} $$

**Paso 4 — obtener \( K_i \).** De la condición de cancelación \( K_p/K_i=L/R \):

$$ K_i = K_p\,\frac{R}{L} = R\,\omega_c\cdot\frac{R}{L} = \frac{R^2\,\omega_c}{L} $$

Equivalentemente, con \( K_i = K_p/\tau \) y \( K_p = L\omega_c \) (fórmula alternativa donde \( K_p \) absorbe \( L \) para que quede en unidades de inductancia × frecuencia):

$$ \boxed{K_p = L\,\omega_c,\qquad K_i = R\,\omega_c} $$

El lazo cerrado \( T(s)=L/(1+L) \) es un **primer orden** de constante \( 1/\omega_c \): rapidez y amortiguamiento están completamente determinados por la elección de \( \omega_c \), sin sobreimpulso.

## 2 — Reglas de Ziegler-Nichols en bucle cerrado (Ku, Tu)
**Paso 1 — obtener Ku y Tu.** Con el controlador actuando solo como proporcional \( C=K \), se aumenta \( K \) hasta la ganancia **última** \( K_u \) en que el lazo presenta oscilaciones sostenidas de periodo \( T_u \) (Nyquist al límite). Para una planta de segundo orden con retardo, esto ocurre en la frecuencia donde la fase es −180°:

$$ |G(j\omega_{180})|\cdot K_u = 1 \;\Rightarrow\; K_u = \frac{1}{|G(j\omega_{180})|} $$

**Paso 2 — regla para el PI.** Ziegler y Nichols ajustaron empíricamente, maximizando rechazo de perturbación con margen de fase razonable:

$$ \boxed{K_p = 0.45\,K_u,\qquad T_i = \frac{T_u}{1.2},\qquad K_i = \frac{K_p}{T_i} = \frac{0.54\,K_u}{T_u}} $$

**Paso 3 — regla para el PID.** Añadiendo acción derivativa se puede usar más ganancia:

$$ \boxed{K_p = 0.6\,K_u,\qquad T_i = \frac{T_u}{2},\qquad T_d = \frac{T_u}{8}} $$

El PI de Z-N da margen de fase en torno a 45°, adecuado cuando no se conoce la planta analíticamente. Para convertidores se prefiere la cancelación de polo porque \( L,R \) son medibles y la relación directa con \( \omega_c \) es más predecible.

## Cuándo y por qué se usa
Es el método base en convertidores: rápido, intuitivo y con relación directa al ancho de banda.
Se combina con la arquitectura en [[control-cascada]].

## Procedimiento (genérico)
1. Modela la planta del lazo (orden, polos, ganancia).
2. Fija \( \omega_c \) desde [[especificaciones-control]].
3. Cancelación de polo: \( K_p=L\omega_c \), \( K_i=R\omega_c \) (lazo de corriente).
4. Verifica margen de fase y respuesta; si hay retardo, reduce \( \omega_c \) o usa óptimo de módulo.

## Ejemplo de código
```python
# PI de lazo de corriente por cancelacion de polo (planta L,R)
wc = 2*np.pi*f_c          # ancho de banda objetivo
Kp = L*wc;  Ki = R*wc     # cero del PI en R/L (cancela el polo de planta)
```

## Parámetros y valores típicos
\( f_c \) del lazo de corriente ≈ \( f_{sw}/10 \). Margen de fase resultante ≈ 60–90° (1er orden).

## Errores comunes
- Cancelar un polo mal identificado o variable → cancelación imperfecta.
- Ignorar el retardo de cómputo/PWM: reduce el margen real a alto \( \omega_c \).

## Uso en proyectos
- **01/02**: lazos de corriente sintonizados así (\( K_p=L_1\omega_{ci} \), \( K_i=R_1\omega_{ci} \)),
  \( f_{ci} \) ≈ 1 kHz / 800 Hz.

## Conceptos relacionados
- [[metodos-sintesis-control]] · [[control-cascada]] · [[loop-shaping]] · [[especificaciones-control]]

## Referencias
- Aström, Hägglund, *Advanced PID Control*, 2006.
