---
titulo: Transformada Z
slug: transformada-z
categoria: control
tipo: concepto
nivel: basico
proyectos: []
objetivos: [analizar y diseñar control en tiempo discreto (digital)]
tags: [transformada-z, discreto, control-digital, muestreo, basico]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-07-02
relacionados: [transformada-laplace, discretizacion-controladores, muestreo-aliasing, estabilidad-bibo]
referencias:
  - "Ogata, Sistemas de Control en Tiempo Discreto, Pearson"
  - "Åström & Wittenmark, Computer-Controlled Systems"
---

## Definición
Es el equivalente discreto de la transformada de Laplace: convierte una secuencia de muestras
\( x[n] \) en una función de la variable compleja \( z \). Es el lenguaje del **control digital**
(el que se implementa en un DSP o microcontrolador, que trabaja por muestras, no en continuo).

## Fundamento teórico
Se define como
$$ X(z) = \sum_{n=0}^{\infty} x[n]\,z^{-n} $$
Su propiedad clave: **un retardo de una muestra equivale a multiplicar por \( z^{-1} \)**, igual que
en Laplace derivar era multiplicar por \( s \). La relación entre ambos dominios, con periodo de
muestreo \( T_s \), es
$$ z = e^{s T_s} $$
Esto mapea el semiplano izquierdo de \( s \) (estable) al **interior del círculo unidad** de \( z \).
Por tanto, el criterio de estabilidad discreto es:
$$ \text{estable} \iff |z_i| < 1 \ \ \forall \text{ polo } z_i $$
El eje \( j\omega \) de \( s \) se convierte en la circunferencia \( |z|=1 \), y la frecuencia de
Nyquist \( \omega_s/2 \) cae en \( z=-1 \).

<div class="cfig"><img src="figuras/transformada-z-planos.png" alt="mapeo plano s a plano z"><div class="cap">La relación z=e^{sTs} mapea el semiplano izquierdo de s (estable en continuo) al interior del círculo unidad de z (estable en discreto). Por eso el criterio digital es |z|<1, no Re(z)<0.</div></div>

## 1 — De dónde sale \( z=e^{sT_s} \) (muestrear Laplace)
**Paso 1 — la señal muestreada.** Muestrear \( x(t) \) cada \( T_s \) es modelarla como un tren de impulsos pesados por las muestras \( x[n]=x(nT_s) \):

$$ x^*(t)=\sum_{n=0}^{\infty}x[n]\,\delta(t-nT_s) $$

**Paso 2 — aplicar Laplace.** La transformada de un impulso desplazado es \( \mathcal{L}\{\delta(t-nT_s)\}=e^{-snT_s} \). Por linealidad:

$$ X^*(s)=\mathcal{L}\{x^*(t)\}=\sum_{n=0}^{\infty}x[n]\,e^{-s n T_s} $$

**Paso 3 — el cambio de variable.** Esta suma depende de \( s \) solo a través del bloque \( e^{sT_s} \). Define:

$$ \boxed{\;z\equiv e^{sT_s}\;} $$

**Paso 4 — aparece la transformada Z.** Sustituyendo \( e^{snT_s}=(e^{sT_s})^n=z^n \), o sea \( e^{-snT_s}=z^{-n} \):

$$ X^*(s)\big|_{e^{sT_s}=z}=\sum_{n=0}^{\infty}x[n]\,z^{-n}=X(z) $$

que es exactamente la definición de la transformada Z. El **retardo** de una muestra, \( x[n-1] \), corresponde a \( \mathcal{L}\{\delta(t-T_s)\}=e^{-sT_s}=z^{-1} \): por eso \( z^{-1} \) es "atrasar un paso".

**Paso 5 — el mapeo de estabilidad.** El semiplano izquierdo es \( s=\sigma+j\omega \) con \( \sigma<0 \). Su imagen es \( z=e^{\sigma T_s}e^{j\omega T_s} \), de módulo \( |z|=e^{\sigma T_s} \). Como \( \sigma<0 \) y \( T_s>0 \) ⇒ \( |z|<1 \): el SPI estable se mapea al **interior del círculo unidad**. El eje \( j\omega \) (\( \sigma=0 \)) da \( |z|=1 \), la circunferencia unidad. De ahí el criterio discreto \( |z_i|<1 \), heredado del \( \mathrm{Re}(s_i)<0 \) de [[estabilidad-bibo]].

## 2 — Tabla de transformadas Z

La tabla siguiente reúne los seis pares más útiles en control digital. Se derivan aplicando la definición \( X(z)=\sum_{n=0}^{\infty}x[n]z^{-n} \) y las propiedades de series geométricas.

| \( x[n] \) | \( X(z) \) | ROC | notas |
|---|---|---|---|
| \( \delta[n] \) | \( 1 \) | todo \( z \) | impulso unitario |
| \( u[n] \) | \( \dfrac{z}{z-1} \) | \( |z|>1 \) | escalón: serie geométrica \( \sum z^{-n}=z/(z-1) \) |
| \( a^n u[n] \) | \( \dfrac{z}{z-a} \) | \( |z|>|a| \) | polo en \( z=a \); estable si \( |a|<1 \) |
| \( n\,u[n] \) | \( \dfrac{z}{(z-1)^2} \) | \( |z|>1 \) | rampa; doble polo en \( z=1 \) |
| \( \sin(n\Omega_0)u[n] \) | \( \dfrac{z\sin\Omega_0}{z^2-2z\cos\Omega_0+1} \) | \( |z|>1 \) | \( \Omega_0=\omega_0 T_s \) (frecuencia digital) |
| \( \cos(n\Omega_0)u[n] \) | \( \dfrac{z(z-\cos\Omega_0)}{z^2-2z\cos\Omega_0+1} \) | \( |z|>1 \) | par conjugado de polos en \( z=e^{\pm j\Omega_0} \) |

**Derivación del par \( u[n]\to z/(z-1) \).** Por definición:
$$
\mathcal{Z}\{u[n]\}=\sum_{n=0}^{\infty}1\cdot z^{-n}=\frac{1}{1-z^{-1}}=\frac{z}{z-1}, \quad |z|>1
$$
Es una serie geométrica de razón \( z^{-1} \), convergente para \( |z^{-1}|<1 \), es decir fuera del círculo unidad. El polo en \( z=1 \) refleja la naturaleza de la señal escalón: energía a frecuencia cero, análogo al polo \( 1/s \) de la transformada de Laplace.

**Derivación del par \( \sin(n\Omega_0)\to\ldots \).** Se expande con la fórmula de Euler \( \sin(n\Omega_0)=\frac{e^{jn\Omega_0}-e^{-jn\Omega_0}}{2j} \) y se aplica el par \( a^n\to z/(z-a) \) con \( a=e^{\pm j\Omega_0} \). Sumando las dos fracciones y simplificando:

$$
\mathcal{Z}\{\sin(n\Omega_0)\}=\frac{z\sin\Omega_0}{z^2-2z\cos\Omega_0+1}
$$

Polos en \( z=e^{\pm j\Omega_0} \) — sobre la circunferencia unidad (señal sostenida, no amortiguada). Si \( |a|<1 \), los polos se contraen al interior y la sinusoide decae.

## 3 — Relación \( z=e^{sT_s} \) y mapeo del plano \( s \) al plano \( z \)

El mapeo \( z=e^{sT_s} \) no es lineal; crea **distorsión de frecuencia** que hay que entender para diseñar en discreto.

**Líneas de \( \sigma \) constante en \( s \).** Corresponden a círculos de radio \( e^{\sigma T_s} \) en \( z \). El eje \( j\omega \) (línea \( \sigma=0 \)) mapea a la circunferencia unidad \( |z|=1 \).

**Líneas de \( \omega \) constante en \( s \).** Corresponden a rayos desde el origen con ángulo \( \omega T_s \). La frecuencia \( \omega=\pi/T_s \) (Nyquist) mapea a \( z=e^{j\pi}=-1 \).

**Curvas de \( \zeta \) constante.** En el plano \( s \), los polos con \( \zeta \) dado se ubican en las semirrectas \( s=-\zeta\omega_n\pm j\sqrt{1-\zeta^2}\omega_n \). En el plano \( z \), esas semirrectas se curvan: para \( \zeta=0.7 \), la curva en \( z \) empieza en \( z=1 \) (DC), se contrae al interior y se dobla hacia el eje real cuando \( \omega_n \to \pi/T_s \). El panel (a) de la figura muestra las curvas iso-\( \zeta \) para \( T_s=100\,\mu\text{s} \).

**Periodicidad en \( \omega \).** El mapeo es periódico con periodo \( 2\pi/T_s \) en frecuencia: los polos \( s_0 \) y \( s_0+j\cdot2\pi k/T_s \) para cualquier entero \( k \) dan el mismo \( z \). Esto es el reflejo del aliasing en el dominio de polos: no se puede distinguir un polo a \( \omega_0 \) de uno a \( \omega_0 + k\omega_s \).

**Círculo unidad como frontera de estabilidad.** En \( s \), la frontera es el eje imaginario \( \sigma=0 \). Al mapear: \( |e^{j\omega T_s}|=1 \), luego la frontera en \( z \) es exactamente la circunferencia unidad. Estable \( \Leftrightarrow \) polos dentro del círculo, inestable \( \Leftrightarrow \) fuera, marginalmente estable \( \Leftrightarrow \) sobre la circunferencia.

## 4 — Análisis de estabilidad en \( z \): polos dentro del círculo unitario

El criterio de estabilidad discreto es inmediato de la sección anterior, pero conviene apreciarlo con un ejemplo numérico.

**Sistema de primer orden.** Un integrador discretizado con Euler hacia adelante: \( y[k+1]=y[k]+T_s\,u[k] \). En \( z \): \( z\,Y(z)=Y(z)+T_s\,U(z) \), luego \( H(z)=T_s/(z-1) \). Polo en \( z=1 \): justo en la circunferencia, marginalmente estable (acumula sin diverger ni amortiguar). Si se cierra con realimentación proporcional \( K \): polo en lazo cerrado en \( z=1-K\,T_s \). Estable si \( |1-K\,T_s|<1 \), es decir \( 0<K<2/T_s \).

**Equivalencia con el criterio continuo.** El polo de lazo cerrado es \( z_{cl}=1-K\,T_s \). En el plano \( s \) (aproximación Euler): \( z\approx1+sT_s \Rightarrow s_{cl}=-K \). Estable si \( \text{Re}(s_{cl})<0 \Leftrightarrow K>0 \). La condición superior \( K<2/T_s \) no aparece en el análisis continuo: es un **artefacto de la discretización** (para \( K\,T_s>2 \) el polo sale por el otro lado del eje real, \( z<-1 \), y oscila en cada muestra con amplitud creciente).

**Verificación numérica.** Para \( T_s=100\,\mu\text{s} \), \( K=2\pi\cdot750\approx4712 \): el polo de lazo cerrado es \( z=1-4712\times10^{-4}=0.529 \), bien dentro del círculo. Si se sube \( K \) hasta \( 2/T_s=20000 \), el polo llega a \( z=-1 \): oscilación de Nyquist, sistema marginalmente inestable.

## 5 — Discretización del PI: Euler atrás vs Tustin

El controlador PI continuo es:
$$
C(s) = K_p + \frac{K_i}{s}
$$

Para implementarlo en un procesador, hay que convertirlo a una ecuación en diferencias. Los dos métodos más comunes difieren en cómo aproximan \( 1/s \) (el integrador).

**Euler hacia atrás (backward Euler).** Aproxima la integral con rectángulos retrospectivos. La sustitución en \( s \) es:

$$
s \;\leftarrow\; \frac{z-1}{T_s\,z} = \frac{1-z^{-1}}{T_s}
$$

El PI discreto resulta:

$$
C_{EB}(z) = K_p + K_i\,\frac{T_s\,z}{z-1}
$$

Ecuación en diferencias: \( u[k]=u[k-1]+K_p\bigl(e[k]-e[k-1]\bigr)+K_i\,T_s\,e[k] \).

Coeficientes numéricos (con \( K_p=L\omega_c \), \( K_i=R\omega_c \), \( L=2\,\text{mH} \), \( R=50\,\text{m}\Omega \), \( \omega_c=2\pi750 \), \( T_s=100\,\mu\text{s} \)):

$$
K_p=9.42\,\Omega, \quad K_i=235\,\Omega/\text{s}, \quad K_i\,T_s=0.0235\,\Omega
$$

**Tustin (bilineal).** Aproxima el integrador con el trapecio — más preciso en frecuencia. La sustitución es:

$$
s \;\leftarrow\; \frac{2}{T_s}\cdot\frac{z-1}{z+1}
$$

El PI discreto resulta:

$$
C_{TU}(z) = K_p + K_i\,\frac{T_s}{2}\cdot\frac{z+1}{z-1}
$$

Ecuación en diferencias: \( u[k]=u[k-1]+\bigl(K_p+K_i\,T_s/2\bigr)e[k]+\bigl(-K_p+K_i\,T_s/2\bigr)e[k-1] \).

Coeficientes numéricos (\( K_i T_s/2=0.01175 \)):

$$
b_0 = K_p + K_i\,T_s/2 = 9.432, \quad b_1 = -K_p + K_i\,T_s/2 = -9.408
$$

**Comparación práctica.** Euler atrás introduce un **retardo adicional** de \( T_s/2 \) respecto al PI continuo (subestima la integral), lo que consume margen de fase. Tustin preserva mejor la magnitud y fase hasta frecuencias cercanas a Nyquist, y es el método estándar. Con **pre-warping** se puede corregir exactamente la frecuencia de cruce: \( s \leftarrow \omega_c/\tan(\omega_c T_s/2) \cdot (z-1)/(z+1) \), pero en control de corriente de convertidores con \( f_c \ll f_s \) la diferencia es menor del 1% y el pre-warping no suele necesitarse.

<div class="cfig"><img src="figuras/transformada-z-analisis.png" alt="analisis completo transformada z"><div class="cap">Cuatro paneles: (a) mapeo s→z con curvas iso-ζ — el círculo unidad es la frontera estable; (b) lugar de raíces del lazo cerrado en el plano z al variar Kp; (c) Bode del PI continuo vs Euler atrás vs Tustin; (d) margen de fase vs Ts con método Tustin.</div></div>

## 6 — Diseño iterativo: efecto de \( T_s \) en la estabilidad del lazo

**Problema.** Lazo de corriente PI con planta \( L=2\,\text{mH} \), \( R=50\,\text{m}\Omega \), \( \omega_c=2\pi\cdot750\,\text{rad/s} \). Usar el método Tustin para discretizar. ¿Para qué \( T_s \) se cumple PM ≥ 45°?

**Paso 1 — función de lazo abierto discreta.** Con Tustin, el PI en \( z \) aplicado a la planta discretizada (Tustin también):

$$
L_{OL}(e^{j\Omega}) = C_{TU}(e^{j\Omega})\cdot H_{planta}(e^{j\Omega}), \quad \Omega=\omega T_s
$$

Para evaluar el PM en \( \omega_c \), basta calcular el ángulo de \( L_{OL} \) en \( z=e^{j\omega_c T_s} \).

**Paso 2 — evaluación numérica.** Con \( T_s=100\,\mu\text{s} \): \( \Omega_c=\omega_c T_s=0.471\,\text{rad} \). El PI Tustin en ese punto:

$$
s_{Tustin} = \frac{2}{T_s}\cdot\frac{e^{j\Omega_c}-1}{e^{j\Omega_c}+1} = j\cdot\frac{2}{T_s}\tan(\Omega_c/2) = j\cdot4800\,\text{rad/s}
$$

La planta en \( j\omega_c=j\cdot4712 \): \( H_{planta}\approx1/(j\omega_c L)=1/(j\cdot9.42) \). La ganancia del PI en \( s_{Tustin} \): \( C\approx K_p + K_i/(j4800)\approx9.42-j0.049 \approx K_p \). El lazo abierto tiene ángulo \( \approx-90°-0.5° \approx -90.5° \), PM \( \approx89.5° \). Este resultado demasiado optimista se debe a que la planta Tustin no incluye el retardo de cálculo; el modelo completo debe añadir \( e^{-j\omega_c T_s} \) (un ciclo de cálculo), que resta ~27° más, dando PM ≈ 62°.

**Paso 3 — tabla PM vs \( T_s \).** El panel (d) de la figura muestra PM calculado con Tustin + retardo de cálculo de un ciclo:

| \( T_s \) [µs] | \( f_s \) [kHz] | PM [°] |
|---|---|---|
| 50 | 20 | 76 |
| 75 | 13.3 | 63 |
| 100 | 10 | 51 |
| 150 | 6.7 | 29 |
| 200 | 5 | 8 |
| 300 | 3.3 | inestable |

**Conclusión.** Para PM ≥ 45° con \( \omega_c=2\pi\cdot750\,\text{Hz} \), hay que usar \( T_s \leq 100\,\mu\text{s} \) (\( f_s \geq 10\,\text{kHz} \)). A \( f_{sw}=10\,\text{kHz} \) se cumple con margen; a \( f_{sw}=5\,\text{kHz} \) (con \( T_s=200\,\mu\text{s} \)) el lazo se vuelve marginalmente estable y hay que reducir \( \omega_c \).

## Cuándo y por qué se usa
Siempre que el control se ejecute en un procesador digital (la práctica totalidad de los
convertidores actuales): hay que discretizar los reguladores diseñados en continuo y comprobar que
sus polos quedan dentro del círculo unidad. También para diseñar directamente en discreto.

## Procedimiento de diseño (genérico)
1. Diseña el regulador en continuo \( G(s) \) (Bode, márgenes).
2. Elige el periodo de muestreo \( T_s \) (regla práctica: \( f_s \ge 10\text{–}20 \) veces el ancho
   de banda del lazo).
3. Discretiza con Tustin \( \to G(z) \).
4. Verifica que los polos de \( G(z) \) cumplen \( |z|<1 \) y que el PM no se ha degradado.

## Ejemplo de código
```python
from scipy.signal import cont2discrete
# PI continuo Kp + Ki/s  ->  discreto con ZOH, Ts=100 us
L, R, wc = 2e-3, 50e-3, 2*3.14159*750
Kp, Ki = L*wc, R*wc
num, den = [Kp, Ki], [1, 0]
(bz, az, Ts) = cont2discrete((num, den), dt=1e-4, method='bilinear')
# Tustin: bz = [b0, b1], az = [1, -1]
print(f"b0={bz[0][0]:.4f}, b1={bz[0][1]:.4f}")
# u[k] = u[k-1] + b0*e[k] + b1*e[k-1]
```

## Parámetros y valores típicos
\( T_s \) entre 50 µs y 200 µs en convertidores (suele atarse a la frecuencia de conmutación
\( f_{sw} \) o a \( f_{sw}/2 \)). Cuanto mayor \( T_s \), más retardo y menos margen de fase.

## Errores comunes
- Confundir el criterio: en discreto es \( |z|<1 \), **no** \( \mathrm{Re}(z)<0 \).
- Muestrear demasiado lento: introduce retardo y puede provocar aliasing (ver [[muestreo-aliasing]]).
- Tustin sin pre-warping desplaza las frecuencias cerca de \( f_s/2 \).
- Olvidar el retardo de un ciclo de cálculo al evaluar el PM del lazo discreto.

## Conceptos relacionados
- [[transformada-laplace]] · [[discretizacion-controladores]] · [[muestreo-aliasing]] · [[estabilidad-bibo]]

## Referencias
- Ogata, *Sistemas de Control en Tiempo Discreto*.
- Åström & Wittenmark, *Computer-Controlled Systems*.
