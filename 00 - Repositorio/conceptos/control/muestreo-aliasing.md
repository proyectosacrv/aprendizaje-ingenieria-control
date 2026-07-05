---
titulo: Muestreo y aliasing (teorema de Nyquist-Shannon)
slug: muestreo-aliasing
categoria: control
tipo: concepto
nivel: basico
proyectos: [01-GFM-Impedance]
objetivos: [elegir la frecuencia de muestreo y evitar el solapamiento espectral]
tags: [muestreo, aliasing, nyquist-shannon, adc, control-digital, basico]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-07-02
relacionados: [transformada-z, fft-analisis-espectral, discretizacion-controladores, convertidor-vsc, series-fourier]
referencias:
  - "Oppenheim & Willsky, Señales y Sistemas, Prentice Hall"
  - "Franklin, Powell, Digital Control of Dynamic Systems, Addison-Wesley"
---

## Definición
Muestrear es tomar valores de una señal continua a intervalos regulares \( T_s \) (frecuencia
\( f_s = 1/T_s \)). El **teorema de Nyquist-Shannon** dice cuándo esas muestras bastan para
reconstruir la señal sin perder información; si no se cumple, aparece **aliasing** (una frecuencia
alta se "disfraza" de una baja).

## Fundamento teórico
Al muestrear, el espectro de la señal se **repite** cada \( f_s \). Para que las réplicas no se
solapen, todo el contenido debe estar por debajo de la **frecuencia de Nyquist** \( f_s/2 \):
$$ f_s > 2\,f_{\max} $$
Si una componente de frecuencia \( f > f_s/2 \) se muestrea, aparece como un **alias** a
$$ f_{\text{alias}} = \lvert\, f - k\,f_s \,\rvert,\quad k\in\mathbb{Z} $$
indistinguible de una señal real de esa frecuencia baja. Por eso, antes del conversor A/D se pone un
**filtro antialiasing** (paso-bajo analógico) que corta por encima de \( f_s/2 \).

<div class="cfig"><img src="figuras/muestreo-aliasing-alias.png" alt="aliasing de una senoide"><div class="cap">Una señal de 900 Hz muestreada a 1 kHz (puntos) es indistinguible de una de 100 Hz (alias): el contenido por encima de fs/2 se "pliega" a baja frecuencia. De ahí el filtro antialiasing antes del A/D.</div></div>

## 1 — De dónde sale \( f_{alias} = |f - k\,f_s| \)

**Paso 1 — muestreo como modulación impulsional.** Muestrear una señal continua \( x(t) \) a intervalos \( T_s \) equivale a multiplicarla por el tren de impulsos de Dirac \( p(t)=\sum_{n=-\infty}^{\infty}\delta(t-nT_s) \):

$$ x_s(t) = x(t)\,p(t) $$

**Paso 2 — espectro del tren de impulsos.** El espectro de \( p(t) \) es también un tren de impulsos en frecuencia:

$$ P(f) = f_s \sum_{k=-\infty}^{\infty} \delta(f - k\,f_s) $$

**Paso 3 — espectro de la señal muestreada.** Por el teorema de convolución, la multiplicación en tiempo equivale a convolución en frecuencia:

$$ X_s(f) = X(f) * P(f) = f_s\sum_{k=-\infty}^{\infty} X(f - k\,f_s) $$

El espectro original \( X(f) \) se **replica** en torno a cada múltiplo de \( f_s \).

**Paso 4 — condición de Nyquist.** Para que las réplicas no se solapen, la réplica centrada en \( k=1 \) (que llega desde abajo a \( f_s - f_{max} \)) debe quedar a la derecha de la réplica central (que llega hasta \( f_{max} \)):

$$ f_s - f_{max} > f_{max} \quad\Rightarrow\quad \boxed{f_s > 2\,f_{max}} $$

**Paso 5 — frecuencia del alias.** Una componente a \( f > f_s/2 \) (violación de Nyquist) queda en la réplica \( k=1 \) centrada en \( f_s \). Su posición dentro de esa réplica, vista en el baseband \( [0, f_s/2] \), es:

$$ \boxed{f_{alias} = |f - k\,f_s|} $$

con \( k \) el entero que minimiza el resultado.

**Paso 6 — ejemplo numérico verificado.** Señal a \( f=6\,\text{kHz} \), \( f_s=10\,\text{kHz} \) (\( f > f_s/2=5\,\text{kHz} \), aliasing inevitable):

$$ f_{alias} = |6000 - 1\times10000| = \mathbf{4000\,\text{Hz}} $$

Una componente de 6 kHz aparece en el espectro digital como si fuera 4 kHz. Verificado: `alias=4000 Hz`.

## 2 — Teorema de Nyquist-Shannon: \( F_s(f) = f_s\sum_k F(f-k f_s) \)

La ecuación del paso 3 anterior *es* el teorema de Nyquist-Shannon en el dominio frecuencial. Merece expandirse con sus consecuencias operativas.

**Enunciado exacto.** Si \( x(t) \) es una señal de banda limitada con \( X(f)=0 \) para \( |f|>B \), y se muestrea a \( f_s \geq 2B \), entonces el espectro de la señal muestreada es:

$$ X_s(f) = f_s \sum_{k=-\infty}^{\infty} X(f - k\,f_s) $$

y la señal original se puede recuperar exactamente aplicando un filtro paso-bajo ideal de ganancia \( 1/f_s \) y frecuencia de corte \( f_s/2 \).

**¿Qué ocurre si \( f_s < 2B \)?** La réplica \( k=1 \) solapará con la réplica \( k=0 \): la componente en \( f=B > f_s/2 \) aparece en \( f_s - B < f_s/2 \) y ya no se puede separar del contenido legítimo. Es el aliasing. Una vez ocurre, es **irreversible**: el filtro de reconstrucción no puede deshacer el solapamiento.

**Margen práctico.** El teorema es exacto para señales perfectamente limitadas en banda — algo que no existe en la práctica (los filtros analógicos tienen roll-off finito). Por eso se usa \( f_s \geq 5\text{–}10\times f_{max} \) en sistemas de control de convertidores, que da margen para que el filtro antialiasing corte suficientemente antes de \( f_s/2 \) sin desfasar la banda de control.

**Relación con la frecuencia de conmutación.** En un convertidor con \( f_{sw}=10\,\text{kHz} \), el rizado de corriente tiene componentes en \( f_{sw} \) y sus armónicos. Si el control muestrea a \( f_s=f_{sw} \), el rizado está exactamente en Nyquist (\( f_{sw}/f_s=1 \)) y puede crear alias en DC si el muestreo no está sincronizado con el pico de la portadora. La solución estándar: **sincronizar** el ADC al pico/valle de la portadora triangular, donde el rizado de corriente cruza su valor medio. Así el contenido a \( f_{sw} \) cae en la frecuencia de Nyquist con amplitud mínima, y el alias sobre DC es despreciable.

## 3 — Filtro antialiasing: compromiso \( f_c \) vs retardo de fase vs margen de fase

El filtro antialiasing (AA) tiene que atenuar suficientemente por encima de \( f_s/2 \) y, al mismo tiempo, no introducir demasiado retardo de fase en la banda de control (donde el lazo de corriente trabaja a \( f_c \approx 750\,\text{Hz} \)).

**Compromiso básico.** Un filtro de Butterworth de orden \( n \) tiene: mayor orden → mayor atenuación en \( f_s/2 \) → pero también mayor fase en \( f_c \). La caída de fase en \( f_c \) consume **margen de fase**:

$$
\Delta\phi_{AA}(f_c) = -\sum_{i=1}^{n}\arctan\!\left(\frac{f_c}{f_{p,i}}\right)
$$

Para un segundo orden con \( f_c^{AA} = 0.4\,f_s \) (filtro Butterworth con polos en \( 0.4\,f_s \)):

$$
\Delta\phi_{AA}(750\,\text{Hz}) \approx -8^\circ \quad (f_s = 10\,\text{kHz})
$$

Solo 8° de penalización sobre los ~90° que cuesta el lazo inductivo y el retardo de cálculo. Aceptable.

**Si \( f_c^{AA} \) baja.** Subir la atenuación colocando \( f_c^{AA} \) cerca de \( f_c^{control} \) inflige fases de \( -20^\circ \) a \( -40^\circ \), que consumen gran parte del margen de fase. Regla práctica: \( f_c^{AA} \geq 5\,f_c^{control} \).

**Retardo de grupo equivalente.** El filtro AA equivale a un retardo puro de aproximadamente \( T_{AA}\approx n/(2\pi f_c^{AA}) \) (polo a polo). Con \( n=2 \) y \( f_c^{AA}=4\,\text{kHz} \): \( T_{AA}\approx80\,\mu\text{s} \), suma al retardo de cálculo y ZOH que ya valen \( 1.5\,T_s \).

## 4 — El ZOH: \( H_{ZOH}(s) \approx e^{-sT_s/2} \), retardo total \( 1.5\,T_s \)

El **retentor de orden cero (ZOH)** es el primer bloque del camino digital-a-analógico. Toma la muestra calculada en el instante \( kT_s \) y la mantiene constante durante todo el intervalo \( [kT_s, (k+1)T_s) \) hasta que llega la siguiente. Su función de transferencia exacta es:

$$
H_{ZOH}(s) = \frac{1 - e^{-sT_s}}{s}
$$

**Aproximación como retardo puro.** Expandiendo: \( 1 - e^{-sT_s} = e^{-sT_s/2}\cdot 2\sinh(sT_s/2) \). Para \( |sT_s|\ll1 \) (frecuencias \( f\ll f_s \)):

$$ \boxed{H_{ZOH}(s) \approx T_s\,e^{-sT_s/2}} $$

Es decir, el ZOH aporta una **ganancia** \( T_s \) (que se cancela con la normalización) y un **retardo de \( T_s/2 \)**.

**Retardo total del lazo digital.** La cadena típica incluye: (1) ADC y cálculo del controlador, que tarda \( T_s \) en el peor caso (el resultado se aplica en el siguiente ciclo); (2) ZOH con retardo \( T_s/2 \). El retardo total de lazo abierto es:

$$
T_{total} = T_s + \frac{T_s}{2} = \frac{3T_s}{2} = 1.5\,T_s
$$

Como retardo puro \( e^{-s\cdot1.5T_s} \), cada \( 100\,\mu\text{s} \) de \( T_s \) consume aproximadamente:

$$
\Delta\phi = -\omega_c \cdot 1.5\,T_s = -2\pi\cdot750\cdot1.5\times10^{-4}\approx-40.5^\circ
$$

Lo que explica por qué el margen de fase cae ~40° al doblar \( T_s \) de 50 µs a 100 µs, como muestra el panel (d) de la figura.

**Verificación numérica:** con \( T_s=100\,\mu\text{s} \), \( f_c=750\,\text{Hz} \), \( K_p=L\omega_c \): el lazo abierto \( K_p/(Ls)\cdot e^{-j\omega_c\cdot1.5T_s} \) tiene módulo 1 en \( \omega_c \) y ángulo \( -90^\circ - 40.5^\circ=-130.5^\circ \). El margen de fase es \( 180-130.5=49.5^\circ \).

<div class="cfig"><img src="figuras/muestreo-aliasing-analisis.png" alt="analisis completo muestreo y aliasing"><div class="cap">Cuatro paneles: (a) espectro muestreado con y sin aliasing — la réplica de la señal de 7 kHz solapa la banda base; (b) Bode del filtro AA con la fase en la frecuencia de cruce del lazo; (c) ZOH en señal escalón — el retardo Ts/2 es visible; (d) margen de fase vs Ts al aumentar el período de muestreo.</div></div>

## 5 — Diseño iterativo: elegir \( T_s \) para \( \omega_c = 2\pi\cdot750\,\text{Hz} \) con PM ≥ 45°

**Objetivo.** Lazo de corriente con \( f_c=750\,\text{Hz} \), planta inductiva \( L=2\,\text{mH} \), controlador PI con cancelación de polo (\( K_p=L\omega_c \)). Elegir \( T_s \) tal que el PM sea ≥ 45° (objetivo 60°).

**Paso 1 — modelar el retardo total.** El lazo abierto es:

$$
L(j\omega_c) = K_p\cdot\frac{1}{Lj\omega_c}\cdot e^{-j\omega_c\cdot 1.5T_s}
$$

En \( \omega_c \): el PI aporta ganancia unitaria y \( \approx 0°\) de fase (al cancelar el polo), la planta aporta \( -90° \), el retardo aporta \( -\omega_c\cdot 1.5T_s \) rad. El margen de fase es:

$$
\text{PM} = 180 - 90 - \omega_c\cdot 1.5T_s\cdot\frac{180}{\pi} = 90 - \frac{1.5T_s\cdot 750\cdot 360}{1}
$$

En notación más limpia:

$$
\text{PM} = 90^\circ - \frac{1.5\,T_s\,\omega_c\,180^\circ}{\pi}
$$

**Paso 2 — despejar \( T_s \) para PM = 45°.**

$$
45^\circ = 90^\circ - \frac{1.5\,T_s\cdot 2\pi\cdot750\cdot180^\circ}{\pi}
\quad\Rightarrow\quad
T_s = \frac{(90-45)\pi}{1.5\cdot2\pi\cdot750\cdot180}\approx28\,\mu\text{s}
$$

Para PM = 60°: \( T_s \approx 14\,\mu\text{s} \). Ambos valores son muy exigentes; en la práctica se acepta:

- \( T_s = 100\,\mu\text{s} \) (\( f_s = 10\,\text{kHz} \)) → PM ≈ 49° (**aceptable** con margen moderado).
- \( T_s = 50\,\mu\text{s} \) (\( f_s = 20\,\text{kHz} \)) → PM ≈ 65° (**cómodo**).

**Paso 3 — iteración con el filtro AA.** El filtro AA resta fase adicional. Con Butterworth 2° y \( f_c^{AA}=4\,\text{kHz} \), la fase en 750 Hz es \( \approx -8° \), bajando el PM en 8°. Para mantener PM ≥ 45°: o bien usar \( T_s \leq 100\,\mu\text{s} \) o reducir \( \omega_c \).

**Resultado del diseño.** \( T_s=100\,\mu\text{s} \), \( f_s=10\,\text{kHz}=f_{sw} \), muestreo sincronizado al pico de portadora, filtro AA Butterworth 2° con \( f_c^{AA}=4\,\text{kHz} \). PM total ≈ 49° − 8° = **41°** (justo en el límite). Para holgura, se puede bajar \( \omega_c \) a 600 Hz y recuperar ~10° de PM.

## Cuándo y por qué se usa
En todo control digital (elegir \( f_s \) del lazo), en la FFT (la malla temporal fija qué
frecuencias se pueden ver), en la simulación conmutada (el paso debe resolver \( f_{sw} \)) y en la
medición de impedancia por inyección (la ventana define la resolución).

## Procedimiento de diseño (genérico)
1. Determina la frecuencia máxima de interés \( f_{\max} \).
2. Elige \( f_s \ge 2 f_{\max} \) con margen práctico (5–10×) para no quedar al límite.
3. Coloca un filtro antialiasing analógico con corte \( < f_s/2 \) antes del muestreo.
4. Calcula el retardo total \( 1.5\,T_s + T_{AA} \) y verifica PM ≥ 45°.
5. En la FFT, usa una ventana de un número **entero** de periodos para no introducir fugas.

## Ejemplo de código
```python
import numpy as np
fs = 1000.0                      # muestreo a 1 kHz -> Nyquist 500 Hz
t = np.arange(0, 1, 1/fs)
x = np.sin(2*np.pi*900*t)        # 900 Hz > 500 Hz -> se vera como alias de 100 Hz
# |900 - 1000| = 100 Hz

# Retardo de grupo del ZOH
Ts = 1/fs
Td_total = 1.5 * Ts              # retardo lazo digital (ZOH + calculo)
wc = 2*np.pi*750
PM_ZOH = 90 - np.degrees(wc * Td_total)  # margen de fase aproximado
print(f"PM con solo ZOH y calculo: {PM_ZOH:.1f} deg")
```

## Parámetros y valores típicos
En convertidores, \( f_s \) del control suele coincidir con \( f_{sw} \) (p.ej. 10 kHz) o
\( f_{sw}/2 \); el muestreo se sincroniza con el pico/valle de la portadora PWM para promediar el
rizado de conmutación de forma natural. Retardo total \( 1.5\,T_s \).

## Errores comunes
- Muestrear sin filtro antialiasing: el ruido de alta frecuencia se pliega sobre la banda útil.
- Olvidar que el rizado de conmutación (a \( f_{sw} \)) puede aliasar si \( f_s = f_{sw} \) sin sincronizar.
- En FFT, ventana no entera de periodos \( \to \) fuga espectral (leakage).
- Ignorar el retardo del filtro AA en el presupuesto de margen de fase.

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: medir impedancia por inyección): la ventana de demodulación se
  ajusta a un número entero de periodos de la perturbación para extraer el fasor sin fuga.

## Conceptos relacionados
- [[transformada-z]] · [[fft-analisis-espectral]] · [[discretizacion-controladores]] · [[convertidor-vsc|modulación PWM]] · [[series-fourier]]

## Referencias
- Oppenheim & Willsky, *Señales y Sistemas*.
- Franklin, Powell, *Digital Control of Dynamic Systems*.
