---
titulo: Sintonía de PI/PID (cancelación de polo, óptimo de módulo)
slug: sintonia-pi-pid
categoria: metodologia
tipo: metodo
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [obtener las ganancias de un PI a partir del ancho de banda]
tags: [PI, PID, sintonia, cancelacion-polo, modulo-optimo, Ziegler-Nichols, IMC, especificacion-PM]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-02
relacionados: [metodos-sintesis-control, control-cascada, especificaciones-control, loop-shaping]
referencias:
  - "Aström, Hägglund, Advanced PID Control, ISA 2006"
  - "Rivera et al., Internal Model Control. A Unifying Review, Ind. Eng. Chem. Res. 1986"
  - "Ziegler, Nichols, Optimum Settings for Automatic Controllers, Trans. ASME 1942"
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

## 2 — El método de Ziegler-Nichols en lazo abierto (respuesta al escalón)

El método ZN en lazo abierto identifica el modelo de la planta a partir de la respuesta al escalón y aplica fórmulas empíricas para calcular las ganancias del PI/PID.

**Paso 1 — obtener la respuesta al escalón.** Se aplica un escalón de amplitud \( \Delta u \) a la entrada de la planta con el lazo abierto y se registra la salida \( y(t) \). Para plantas de tipo "S" (primer o segundo orden sin integrador), la respuesta tiene la forma característica: sube sigmoidal hasta el nuevo valor estacionario.

**Paso 2 — identificar el punto de inflexión.** En el punto de inflexión de la curva de respuesta, se traza la tangente. La tangente corta el eje de la respuesta inicial en \( t=\tau \) (tiempo de retardo aparente o "tiempo muerto") y el eje de la respuesta final en \( t=\tau+T \) (donde \( T \) es la constante de tiempo dominante). La ganancia estática es \( K=\Delta y/\Delta u \).

**Paso 3 — las fórmulas de ZN para PI:**
$$ \boxed{K_p = \frac{0.9\,T}{K\,\tau},\qquad T_i = 3.3\,\tau,\qquad K_i = \frac{K_p}{T_i}} $$

**Paso 4 — las fórmulas de ZN para PID:**
$$ \boxed{K_p = \frac{1.2\,T}{K\,\tau},\qquad T_i = 2\,\tau,\qquad T_d = 0.5\,\tau} $$

**Interpretación.** El PI de ZN da un margen de fase alrededor de 45–50°, adecuado para plantas con dinámica dominada por la constante de tiempo \( T \) y un retardo pequeño (\( \tau/T<0.3 \)). Para \( \tau/T>0.5 \) (retardo dominante), las fórmulas de ZN dan un sistema oscilatorio; en ese caso se prefiere el método IMC (apartado 4).

**La limitación principal.** ZN en lazo abierto asume que el diseñador puede obtener la respuesta al escalón de la planta sin cerrar el lazo. Para plantas inestables (como un convertidor con carga CPL que supera la potencia crítica) esto no es posible: la planta diverge antes de establecerse. Además, para plantas con acoplos o con resonancias, el modelo de primer orden con retardo puede ser inexacto.

## 3 — El método de Ziegler-Nichols en lazo cerrado (oscilación sostenida)

El método ZN en lazo cerrado es una alternativa que no requiere un modelo de la planta: trabaja directamente con el sistema en lazo cerrado, pero lleva la planta al borde de la inestabilidad.

**Paso 1 — obtener la ganancia última \( K_u \) y el período \( T_u \).**
Se conecta únicamente el controlador proporcional \( C(s)=K \) (sin término integral ni derivativo). Se aumenta \( K \) progresivamente hasta que el lazo cerrado presenta **oscilaciones sostenidas de amplitud constante**: la ganancia en ese punto es la ganancia última \( K_u \) y el período de oscilación es \( T_u \). Esto equivale a colocar el sistema exactamente en el límite de estabilidad (PM = 0°, GM = 1).

**Relación con la planta:** para una planta con retardo puro \( G(s)=e^{-\tau s}/(Ts+1) \), la oscilación sostenida ocurre en la frecuencia \( \omega_{180} \) donde la fase es \( -180° \):
$$ K_u = \frac{1}{|G(j\omega_{180})|},\qquad T_u = \frac{2\pi}{\omega_{180}} $$

**Paso 2 — las fórmulas de ZN para PI:**
$$ \boxed{K_p = 0.45\,K_u,\qquad T_i = \frac{T_u}{1.2},\qquad K_i = \frac{K_p}{T_i}} $$

**Paso 3 — las fórmulas de ZN para PID:**
$$ \boxed{K_p = 0.6\,K_u,\qquad T_i = \frac{T_u}{2},\qquad T_d = \frac{T_u}{8}} $$

**La limitación principal.** El método lleva la planta a la inestabilidad, lo que puede ser peligroso o imposible en sistemas reales (convertidores de potencia, procesos con restricciones duras). Además, \( K_u \) y \( T_u \) pueden ser difíciles de identificar si la oscilación no se estabiliza rápidamente. En sistemas con no-linealidades (saturación del actuador, histéresis), la oscilación puede no ser de amplitud constante.

## 4 — El método IMC (Internal Model Control): sintonía por cancelación

El IMC (Control por Modelo Interno) es un marco de diseño que produce el controlador óptimo cuando el modelo de la planta es exacto, y que degrada graciosamente ante incertidumbre.

**La idea del IMC.**
El controlador IMC \( Q(s) \) opera sobre el error entre la salida de la planta y la salida del modelo. Si el modelo es exacto, la señal de error es cero y el controlador actúa como en lazo abierto. El parámetro de ajuste \( \lambda \) (tiempo de respuesta objetivo) determina el compromiso velocidad/robustez.

**Para planta de primer orden \( G(s)=K/(1+\tau s) \):**
El controlador IMC perfecto sería \( Q(s)=G^{-1}(s)=(\tau s+1)/(K) \), que cancelaría la planta pero no sería propio. El filtro IMC de primer orden \( f(s)=1/(1+\lambda s) \) regulariza el problema:
$$ Q(s)=\frac{1+\tau s}{K(1+\lambda s)} $$
Trasladando al PI equivalente (la forma estándar de retroalimentación), el controlador IMC con filtro de primer orden da un **PI exacto**:
$$ C_{IMC}(s)=\frac{Q(s)}{1-Q(s)G(s)}=\frac{1}{K}\cdot\frac{\tau s+1}{\lambda s}=\frac{\tau}{K\lambda}\cdot\frac{1+1/(\tau s)}{1} $$
Es decir:
$$ \boxed{K_p = \frac{\tau}{K(\tau_d+\lambda)},\qquad T_i = \tau,\qquad K_i = \frac{K_p}{\tau}} $$
donde \( \tau_d \) es el retardo (si lo hay). Para planta sin retardo: \( K_p=\tau/(K\lambda) \), \( T_i=\tau \).

**Interpretación del parámetro \( \lambda \).**
- \( \lambda \) grande → controlador más lento, más robusto ante incertidumbre del modelo.
- \( \lambda \) pequeño → controlador más agresivo, menos robusto.
- Regla práctica: \( \lambda>\max(0.2\tau, \tau_d) \) para robustez mínima. Para sistemas con retardo significativo, \( \lambda>\tau_d \) es necesario para mantener el PM > 0.

**Para el lazo de corriente** con \( G(s)=1/(L_1 s+R_1) \) (es decir, \( K=1/R_1 \), \( \tau=L_1/R_1 \)) y retardo digital \( \tau_d=1.5T_s=150\,\mu\mathrm{s} \):
$$ K_p=\frac{L_1/R_1}{(1/R_1)(\tau_d+\lambda)}=\frac{L_1}{\tau_d+\lambda},\qquad T_i=\frac{L_1}{R_1},\qquad K_i=\frac{R_1}{\tau_d+\lambda} $$
Con \( \lambda=0.5 \) ms: \( K_p=2\times10^{-3}/(150\times10^{-6}+500\times10^{-6})=2\times10^{-3}/650\times10^{-6}\approx3.08 \), \( K_i=0.05/650\times10^{-6}\approx76.9 \).

**Ventaja del IMC:** el único parámetro de ajuste es \( \lambda \), con interpretación física directa (tiempo de respuesta del lazo cerrado). No requiere iteración: dado \( \lambda \), las ganancias quedan determinadas.

## 5 — El método de ajuste por especificación de PM

**Objetivo directo.** En lugar de usar un método heurístico, se especifica directamente el margen de fase deseado \( \mathrm{PM}_{deseado} \) y se calcula el controlador que lo logra.

**Para una planta de primer orden con PI por cancelación de polo.**
Tras la cancelación, el lazo es \( L(s)=(K_p/R)/s \): integrador puro, fase siempre \( -90° \) → PM = 90° (sin retardo). El margen de fase no depende de \( K_p \); solo el cruce depende de \( K_p \). Por tanto, **no se puede especificar el PM con solo el PI por cancelación en una planta sin retardo**: el PM siempre es 90°.

**Con retardo digital \( \tau_d=1.5T_s \).**
El retardo añade fase negativa \( -\omega\tau_d \) (en radianes) que depende de la frecuencia. En el cruce \( \omega_c \), la fase total es:
$$ \angle L(j\omega_c)=-90° - \omega_c\tau_d\cdot\frac{180°}{\pi} $$
El PM es:
$$ \mathrm{PM}=180°-90°-\omega_c\tau_d\cdot\frac{180°}{\pi}=90°-\omega_c\tau_d\cdot\frac{180°}{\pi} $$
Despejando \( \omega_c \) para un PM objetivo:
$$ \omega_c=\frac{(90°-\mathrm{PM}_{obj})\cdot\pi}{180°\cdot\tau_d} $$
Con PM = 50° y \( \tau_d=1.5\times10^{-4} \) s:
$$ \omega_c=\frac{40°\cdot\pi/180°}{1.5\times10^{-4}}=\frac{0.698}{1.5\times10^{-4}}\approx4654\ \text{rad/s}\approx740\ \text{Hz} $$

**Para PM = 45°:**
$$ \omega_c=\frac{45°\cdot\pi/180°}{1.5\times10^{-4}}=\frac{0.785}{1.5\times10^{-4}}\approx5236\ \text{rad/s}\approx833\ \text{Hz} $$

**Con resonancia del filtro LCL.** Para el LCL, la planta tiene un cero de antiresonancia antes de la resonancia, y la fase cae bruscamente tras la resonancia. Hay que verificar que la pendiente en el cruce no sea \( -40 \) dB/dec (que daría PM ≈ 0). El loop-shaping añade ceros de adelanto o polos adicionales para recuperar fase en el cruce (ver [[loop-shaping]]).

## 6 — Diseño iterativo: comparativa de métodos para el lazo de corriente

**Planta y datos:** \( G(s)=1/(L_1 s+R_1) \) con \( L_1=2 \) mH, \( R_1=50 \) mΩ, retardo digital \( \tau_d=1.5T_s=150\,\mu\mathrm{s} \).

**Método 1 — cancelación de polo (referencia):**
$$ K_p=L_1\omega_c=2\times10^{-3}\cdot2\pi\cdot750\approx9.42,\quad K_i=R_1\omega_c=0.05\cdot2\pi\cdot750\approx0.236 $$
$$ \mathrm{PM}=90°-2\pi\cdot750\cdot1.5\times10^{-4}\cdot\frac{180°}{\pi}\approx90°-40.1°=49.9° $$

**Método 2 — IMC con \( \lambda=0.5 \) ms:**
$$ K_p=\frac{L_1}{\tau_d+\lambda}=\frac{2\times10^{-3}}{6.5\times10^{-4}}\approx3.08,\quad T_i=\frac{L_1}{R_1}=0.04\ \text{s},\quad K_i=\frac{R_1}{\tau_d+\lambda}=\frac{0.05}{6.5\times10^{-4}}\approx76.9 $$
Ancho de banda efectivo: \( f_c\approx1/(2\pi(\tau_d+\lambda))\approx245 \) Hz. Más lento pero más robusto ante variaciones de \( L_1 \).

**Método 3 — especificación de PM = 50°:**
$$ \omega_c=\frac{40°\cdot\pi/180°}{\tau_d}\approx4654\ \text{rad/s},\quad K_p=L_1\omega_c\approx9.31,\quad K_i=R_1\omega_c\approx0.233 $$

**Tabla comparativa:**

| Método | \( K_p \) | \( K_i \) | PM (°) | BW (Hz) | \( M_s \) |
|---|---|---|---|---|---|
| Cancelación de polo | 9.42 | 0.236 | 49.9° | 750 | 1.31 |
| IMC (\( \lambda=0.5 \) ms) | 3.08 | 76.9 | 80°\* | 245 | ≈ 1.05 |
| PM = 50° | 9.31 | 0.233 | 50.0° | 740 | 1.30 |
| ZN lazo abierto | \(\approx 4\) | \(\approx 160\) | ≈ 45° | ≈ 360 | ≈ 1.45 |

\* El IMC con \( \lambda=0.5 \) ms tiene PM alto porque el BW es mucho menor que el límite impuesto por el retardo.

**Conclusión del diseño iterativo.** Para el lazo de corriente de un convertidor VSC con \( f_{sw}=10 \) kHz (\( T_s=100\,\mu\mathrm{s} \)):
- La **cancelación de polo** da el BW máximo compatible con PM ≥ 45° con el mínimo cálculo.
- El **IMC** es preferible cuando hay incertidumbre en \( L_1 \) (variaciones de \( \pm30\% \)): la robustez es mayor.
- La **especificación de PM** da resultados equivalentes a la cancelación de polo; es útil cuando se quiere afinar el PM con precisión.

<div class="cfig"><img src="figuras/sintonia-pi-pid-analisis.png" alt="Comparativa de métodos de sintonía para el lazo de corriente"><div class="cap">(a) Método ZN lazo abierto: respuesta al escalón de la planta con $\tau$ y $T$ marcados, y la tangente en el punto de inflexión. (b) Método IMC: el efecto de $\lambda$ en la respuesta del lazo cerrado para $\lambda=0.15$, 0.5, 1 ms — más $\lambda$ → más lento pero más robusto. (c) Comparativa de los tres métodos en el Bode del lazo: $|L(j\omega)|$ con cancelación de polo, IMC y PM-spec; se marcan los cruces y los PM de cada uno. (d) Respuesta al escalón del lazo cerrado con los tres métodos: cancelación da el BW más alto con PM ≥ 45°, IMC da la respuesta más lenta pero sin sobreimpulso.</div></div>

## Cuándo y por qué se usa
Es el método base en convertidores: rápido, intuitivo y con relación directa al ancho de banda.
Se combina con la arquitectura en [[control-cascada]].

## Procedimiento (genérico)
1. Modela la planta del lazo (orden, polos, ganancia).
2. Fija \( \omega_c \) desde [[especificaciones-control]].
3. Cancelación de polo: \( K_p=L\omega_c \), \( K_i=R\omega_c \) (lazo de corriente).
4. Verifica margen de fase con retardo; si no cumple, reduce \( \omega_c \) o usa IMC.
5. Si hay incertidumbre paramétrica significativa, usa IMC con \( \lambda>\max(0.2\tau, \tau_d) \).

## Ejemplo de código
```python
import numpy as np
from scipy import signal

L1, R1, Ts = 2e-3, 50e-3, 100e-6
tau_d = 1.5*Ts          # retardo digital

# Metodo 1: cancelacion de polo
fc = 750                  # Hz objetivo
wc = 2*np.pi*fc
Kp_cp = L1*wc; Ki_cp = R1*wc
PM_cp = 90 - wc*tau_d*180/np.pi
print(f"Cancelacion: Kp={Kp_cp:.3f}, Ki={Ki_cp:.4f}, PM={PM_cp:.1f}°")

# Metodo 2: IMC
lam = 0.5e-3            # lambda = 0.5 ms
Kp_imc = L1/(tau_d + lam); Ki_imc = R1/(tau_d + lam)
Ti_imc = L1/R1          # = 40 ms
wc_imc = 1/(tau_d+lam)
PM_imc = 90 - wc_imc*tau_d*180/np.pi
print(f"IMC: Kp={Kp_imc:.3f}, Ki={Ki_imc:.2f}, Ti={Ti_imc*1e3:.1f}ms, PM={PM_imc:.1f}°")

# Metodo 3: PM especificado
PM_obj = 50             # grados
wc_pm = (90-PM_obj)*np.pi/180 / tau_d
Kp_pm = L1*wc_pm; Ki_pm = R1*wc_pm
print(f"PM-spec: Kp={Kp_pm:.3f}, Ki={Ki_pm:.4f}, fc={wc_pm/(2*np.pi):.0f}Hz")
```

## Parámetros y valores típicos
\( f_c \) del lazo de corriente ≈ \( f_{sw}/10 \). Margen de fase ≥ 45° tras retardo digital.
IMC: \( \lambda\in[0.2\tau,2\tau] \). ZN: para sistemas lentos con retardo moderado.

## Errores comunes
- Cancelar un polo mal identificado o variable → cancelación imperfecta.
- Ignorar el retardo de cómputo/PWM: reduce el margen real a alto \( \omega_c \).
- Usar ZN en sistemas con restricciones de saturación (el método puede llevar a oscilaciones).
- Elegir \( \lambda \) demasiado pequeño en IMC (< \( \tau_d \)) → sistema inestable.

## Uso en proyectos
- **01/02**: lazos de corriente sintonizados así (\( K_p=L_1\omega_{ci} \), \( K_i=R_1\omega_{ci} \)),
  \( f_{ci} \) ≈ 1 kHz / 800 Hz.

## Conceptos relacionados
- [[metodos-sintesis-control]] · [[control-cascada]] · [[loop-shaping]] · [[especificaciones-control]]

## Referencias
- Aström, Hägglund, *Advanced PID Control*, 2006.
- Rivera et al., *Internal Model Control*, Ind. Eng. Chem. Res. 1986.
- Ziegler, Nichols, *Optimum Settings for Automatic Controllers*, Trans. ASME 1942.
