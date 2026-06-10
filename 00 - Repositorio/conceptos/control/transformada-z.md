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
fecha_actualizacion: 2026-06-10
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

## Cuándo y por qué se usa
Siempre que el control se ejecute en un procesador digital (la práctica totalidad de los
convertidores actuales): hay que discretizar los reguladores diseñados en continuo y comprobar que
sus polos quedan dentro del círculo unidad. También para diseñar directamente en discreto.

## Procedimiento de diseño (genérico)
1. Diseña el regulador en continuo \( G(s) \) (Bode, márgenes).
2. Elige el periodo de muestreo \( T_s \) (regla práctica: \( f_s \ge 10\text{–}20 \) veces el ancho
   de banda del lazo).
3. Discretiza con un método (ZOH, Tustin/bilineal) \( \to G(z) \).
4. Verifica que los polos de \( G(z) \) cumplen \( |z|<1 \) y que el ancho de banda no se ha
   degradado por el muestreo.

## Ejemplo de código
```python
from scipy.signal import cont2discrete
# PI continuo Kp + Ki/s  ->  discreto con ZOH, Ts=100 us
num, den = [Kp, Ki], [1, 0]
(bz, az, Ts) = cont2discrete((num, den), dt=1e-4, method='zoh')
```

## Parámetros y valores típicos
\( T_s \) entre 50 µs y 200 µs en convertidores (suele atarse a la frecuencia de conmutación
\( f_{sw} \) o a \( f_{sw}/2 \)). Cuanto mayor \( T_s \), más retardo y menos margen de fase.

## Errores comunes
- Confundir el criterio: en discreto es \( |z|<1 \), **no** \( \mathrm{Re}(z)<0 \).
- Muestrear demasiado lento: introduce retardo y puede provocar aliasing (ver [[muestreo-aliasing]]).
- Tustin sin pre-warping desplaza las frecuencias cerca de \( f_s/2 \).

## Conceptos relacionados
- [[transformada-laplace]] · [[discretizacion-controladores]] · [[muestreo-aliasing]] · [[estabilidad-bibo]]

## Referencias
- Ogata, *Sistemas de Control en Tiempo Discreto*.
- Åström & Wittenmark, *Computer-Controlled Systems*.
