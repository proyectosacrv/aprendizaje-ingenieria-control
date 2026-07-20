---
titulo: Frecuencias natural, amortiguada y de pico (ωn, ωd, ω_peak)
slug: frecuencias-segundo-orden
categoria: control
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [distinguir y deducir las tres frecuencias de un sistema de segundo orden resonante y saber cuándo coinciden o difieren]
tags: [segundo-orden, frecuencia-natural, frecuencia-amortiguada, pico-resonante, amortiguamiento, polos, intermedio]
fecha_creacion: 2026-06-24
fecha_actualizacion: 2026-07-01
relacionados: [respuesta-segundo-orden, resonancia-rlc, filtro-lcl, polos-ceros, diagrama-bode]
referencias:
  - "Ogata, Ingeniería de Control Moderna, Pearson"
  - "Franklin, Powell, Emami-Naeini, Feedback Control of Dynamic Systems"
---

## Definición
Un sistema resonante de segundo orden tiene **tres frecuencias** que se parecen pero no son la misma, y conviene no confundirlas:
- \( \omega_n \) — **frecuencia natural** (no amortiguada): la que tendría el sistema si no hubiera amortiguamiento.
- \( \omega_d \) — **frecuencia amortiguada**: la frecuencia real a la que oscila el transitorio en el tiempo.
- \( \omega_{peak} \) — **frecuencia de pico** (resonante): la frecuencia a la que la respuesta en frecuencia alcanza su máximo.

Para amortiguamiento pequeño las tres casi coinciden; al crecer el amortiguamiento se separan, y \( \omega_{peak} \) llega incluso a desaparecer. Aparecen en cualquier sistema de dos polos: un filtro LCL (donde el par resonante las hace surgir), un RLC, un lazo de control, un eje mecánico.

## Punto de partida — el sistema canónico de segundo orden
$$ H(s)=\frac{\omega_n^2}{s^2+2\zeta\omega_n s+\omega_n^2} $$
con \( \zeta \) el amortiguamiento. Sus dos polos son las raíces del denominador:
$$ s = -\zeta\omega_n \pm \sqrt{(\zeta\omega_n)^2-\omega_n^2} = -\zeta\omega_n \pm \omega_n\sqrt{\zeta^2-1} $$
Para \( 0\le\zeta<1 \) (subamortiguado) el radicando es negativo y los polos son complejos conjugados:
$$ s = -\zeta\omega_n \pm j\,\omega_n\sqrt{1-\zeta^2} $$

## Desarrollo 1 — ωn, la frecuencia natural (módulo del polo)
\( \omega_n \) es la frecuencia de oscilación **sin amortiguamiento**: poniendo \( \zeta=0 \) los polos quedan en \( s=\pm j\omega_n \), oscilación pura. Geométricamente es la **distancia del origen al polo** en el plano \( s \): tomando el polo \( s=-\zeta\omega_n+j\omega_n\sqrt{1-\zeta^2} \),
$$ |s|^2 = (\zeta\omega_n)^2 + \left(\omega_n\sqrt{1-\zeta^2}\right)^2 = \omega_n^2\zeta^2 + \omega_n^2(1-\zeta^2) = \omega_n^2 \;\Rightarrow\; |s|=\omega_n $$
La parte real del polo es \( \sigma=\zeta\omega_n \) (marca la velocidad de decaimiento) y el ángulo \( \theta \) que forma el polo con el eje real negativo cumple \( \cos\theta=\zeta \).

<div class="cfig"><img src="figuras/frecuencias-segundo-orden-splano.png" alt="polo de segundo orden en el plano s con omega_n como modulo, omega_d como parte imaginaria y sigma como parte real"><div class="cap">Geometría del polo: \(\omega_n\) es el módulo (distancia al origen), \(\omega_d\) la parte imaginaria, \(\sigma=\zeta\omega_n\) la parte real, y \(\cos\theta=\zeta\). De aquí se leen las tres relaciones de un vistazo.</div></div>

## Desarrollo 2 — ωd, la frecuencia amortiguada (parte imaginaria del polo)
Es la frecuencia a la que **realmente oscila el transitorio** en el dominio del tiempo. La respuesta al impulso o al escalón de un sistema subamortiguado contiene el factor
$$ e^{-\sigma t}\sin(\omega_d t+\varphi) $$
donde \( \omega_d \) es exactamente la parte imaginaria del polo, leída directamente de las raíces:
$$ \boxed{\;\omega_d=\omega_n\sqrt{1-\zeta^2}\;} $$
La envolvente \( e^{-\sigma t} \) decae con \( \sigma=\zeta\omega_n \), y entre dos picos consecutivos pasa el periodo \( T_d=2\pi/\omega_d \). Como \( \sqrt{1-\zeta^2}\le1 \), siempre \( \omega_d\le\omega_n \): el amortiguamiento ralentiza la oscilación. En \( \zeta=1 \) (crítico) \( \omega_d=0 \): deja de oscilar.

## Desarrollo 3 — ω_peak, la frecuencia de pico (máximo de la respuesta en frecuencia)
Es la frecuencia a la que la **magnitud** de la respuesta en frecuencia es máxima (el pico de resonancia que se ve en el Bode). Se obtiene maximizando \( |H(j\omega)| \), o equivalentemente **minimizando su denominador**. Con \( s=j\omega \):
$$ |H(j\omega)|^2 = \frac{\omega_n^4}{(\omega_n^2-\omega^2)^2 + (2\zeta\omega_n\omega)^2} $$
El máximo de \( |H| \) está donde el denominador \( D(\omega)=(\omega_n^2-\omega^2)^2+4\zeta^2\omega_n^2\omega^2 \) es mínimo. Derivando e igualando a cero:
$$ \frac{dD}{d\omega} = 2(\omega_n^2-\omega^2)(-2\omega) + 8\zeta^2\omega_n^2\omega = 4\omega\left[\omega^2-\omega_n^2+2\zeta^2\omega_n^2\right]=0 $$
Descartando \( \omega=0 \), el corchete da \( \omega^2=\omega_n^2(1-2\zeta^2) \), es decir:
$$ \boxed{\;\omega_{peak}=\omega_n\sqrt{1-2\zeta^2}\;} $$

**Condición de existencia.** El radicando \( 1-2\zeta^2 \) debe ser positivo, así que **solo hay pico resonante si \( \zeta<1/\sqrt{2}\approx0.707 \)**. Para \( \zeta\ge0.707 \) la magnitud decrece de forma monótona desde \( \omega=0 \): no hay pico. Por eso \( \zeta=0.707 \) es la frontera "plana" (máximamente plana, Butterworth).

**Altura del pico (factor de resonancia).** Sustituyendo \( \omega_{peak} \) en \( |H| \) se obtiene el valor del pico:
$$ M_r=|H(j\omega_{peak})| = \frac{1}{2\zeta\sqrt{1-\zeta^2}} $$
que crece sin límite cuando \( \zeta\to0 \) (pico infinito, no amortiguado) y vale 1 en \( \zeta=1/\sqrt{2} \).

<div class="cfig"><img src="figuras/frecuencias-segundo-orden-resp.png" alt="izquierda magnitud para varios zeta marcando omega_peak; derecha omega_d y omega_peak normalizadas frente a zeta"><div class="cap">Izquierda: \(|H(j\omega)|\) para varios \(\zeta\); el pico (○) está en \(\omega_{peak}\) y desaparece para \(\zeta\ge0.707\). Derecha: \(\omega_d/\omega_n\) y \(\omega_{peak}/\omega_n\) frente a \(\zeta\); ambas salen de 1 con \(\zeta\) pequeño, \(\omega_{peak}\) se anula en \(\zeta=0.707\) y \(\omega_d\) en \(\zeta=1\).</div></div>

## Desarrollo 4 — altura del pico resonante Mr = 1/(2ζ√(1−ζ²))

**Paso 1 — sustituir ωpeak en |H(jω)|.** Se tiene \( \omega_{peak}^2=\omega_n^2(1-2\zeta^2) \). Sustituyendo en el denominador de \( |H|^2 \):

$$ (\omega_n^2-\omega_{peak}^2)^2 = \left(\omega_n^2-\omega_n^2(1-2\zeta^2)\right)^2 = \left(2\zeta^2\omega_n^2\right)^2 = 4\zeta^4\omega_n^4 $$

$$ (2\zeta\omega_n\omega_{peak})^2 = 4\zeta^2\omega_n^2\cdot\omega_n^2(1-2\zeta^2) = 4\zeta^2\omega_n^4(1-2\zeta^2) $$

**Paso 2 — sumar los dos términos del denominador.**

$$ D(\omega_{peak}) = 4\zeta^4\omega_n^4 + 4\zeta^2\omega_n^4(1-2\zeta^2) = 4\zeta^2\omega_n^4\left[\zeta^2+(1-2\zeta^2)\right] = 4\zeta^2\omega_n^4(1-\zeta^2) $$

**Paso 3 — calcular |H|²(ωpeak) y tomar raíz.**

$$ |H|^2(\omega_{peak})=\frac{\omega_n^4}{4\zeta^2\omega_n^4(1-\zeta^2)}=\frac{1}{4\zeta^2(1-\zeta^2)} $$

$$ \boxed{M_r=|H(j\omega_{peak})|=\frac{1}{2\zeta\sqrt{1-\zeta^2}}} $$

**Verificación de límites.** Para \( \zeta\to0 \): \( M_r\to\infty \) (pico infinito, sin amortiguamiento). Para \( \zeta=1/\sqrt{2} \): \( M_r=1/(2\cdot\tfrac{1}{\sqrt{2}}\cdot\tfrac{1}{\sqrt{2}})=1 \) (pico exactamente unitario, coincide con la ganancia DC).

## Orden y relaciones entre las tres
Para \( 0<\zeta<1/\sqrt{2} \) se cumple siempre:
$$ \omega_{peak} = \omega_n\sqrt{1-2\zeta^2} \;\le\; \omega_d = \omega_n\sqrt{1-\zeta^2} \;\le\; \omega_n $$
- Con \( \zeta \) pequeño (típico de una resonancia LCL sin amortiguar, \( \zeta\approx0.005 \)): las tres son prácticamente iguales a \( \omega_n \). Por eso a menudo se habla de "la frecuencia de resonancia" sin distinguir.
- Al subir \( \zeta \) se separan: primero desaparece el pico (\( \zeta\ge0.707 \)), luego la oscilación temporal (\( \zeta\ge1 \)).

## Cuándo y por qué se usa
Cada frecuencia responde a una pregunta distinta: \( \omega_n \) para situar el polo (diseño, asignación de polos), \( \omega_d \) para predecir la frecuencia del transitorio y su periodo de oscilación, \( \omega_{peak} \) y \( M_r \) para acotar el pico de resonancia en frecuencia (filtros, resonancia LCL, márgenes). Confundirlas lleva a errores: medir el periodo del ringing da \( \omega_d \), no \( \omega_n \); el pico del Bode está en \( \omega_{peak} \), no en \( \omega_n \).

## Procedimiento (genérico)
1. Identifica los dos polos dominantes y de ahí \( \omega_n=|s| \) y \( \zeta=\cos\theta \) (o \( \zeta=-\mathrm{Re}(s)/|s| \)).
2. Si quieres la oscilación temporal: \( \omega_d=\mathrm{Im}(s)=\omega_n\sqrt{1-\zeta^2} \).
3. Si quieres el pico en frecuencia: comprueba \( \zeta<0.707 \); si lo cumple, \( \omega_{peak}=\omega_n\sqrt{1-2\zeta^2} \) y \( M_r=1/(2\zeta\sqrt{1-\zeta^2}) \).

## Ejemplo de código
```python
import numpy as np
zeta, wn = 0.3, 8660.0
wd = wn*np.sqrt(1 - zeta**2)                 # frecuencia amortiguada
if zeta < 1/np.sqrt(2):
    w_peak = wn*np.sqrt(1 - 2*zeta**2)       # frecuencia de pico
    Mr = 1/(2*zeta*np.sqrt(1 - zeta**2))     # altura del pico
else:
    w_peak, Mr = None, None                  # no hay pico resonante
# desde un polo complejo s = -sigma + j*wd:
s = -2598 + 1j*8261
wn_, zeta_ = abs(s), -s.real/abs(s)
```

## Parámetros y valores típicos
- Resonancia LCL sin amortiguar: \( \zeta\approx0.005 \) → las tres frecuencias coinciden, pico enorme (\( M_r\approx100 \)).
- Lazo de control bien amortiguado: \( \zeta=0.7 \) → no hay pico de resonancia, \( \omega_d\approx0.71\,\omega_n \).
- \( \zeta=1/\sqrt{2}\approx0.707 \): frontera, respuesta máximamente plana.

## Errores comunes
- Confundir \( \omega_n \) (módulo del polo) con \( \omega_d \) (parte imaginaria) o con \( \omega_{peak} \) (pico del Bode).
- Buscar \( \omega_{peak} \) cuando \( \zeta\ge0.707 \): no existe (no hay pico).
- Tomar el periodo del ringing como \( 2\pi/\omega_n \): es \( 2\pi/\omega_d \).
- Olvidar que para \( \zeta \) pequeño las tres coinciden, lo que esconde la distinción hasta que el amortiguamiento crece.

## Uso en proyectos
- 01 / 02 (filtro LCL): el par resonante del LCL se describe con estas tres frecuencias; con amortiguamiento parásito (\( \zeta\approx0.005 \)) las tres son ≈ \( \omega_{res} \); tras amortiguamiento activo (\( \zeta\approx0.1\text{–}0.3 \)) empiezan a separarse y el pico baja. La derivación de \( \omega_n \) y \( \zeta \) del LCL con resistencias está en [[filtro-lcl]].

## 4 — Parámetros de rendimiento: cálculo explícito

Para el sistema de segundo orden estándar \( T(s) = \omega_n^2 / (s^2 + 2\zeta\omega_n s + \omega_n^2) \), los parámetros de la respuesta al escalón tienen expresiones cerradas:

**Tiempo de pico:**
$$ t_p = \frac{\pi}{\omega_d} = \frac{\pi}{\omega_n\sqrt{1-\zeta^2}} $$

**Sobreoscilación porcentual:**
$$ M_p = e^{-\pi\zeta/\sqrt{1-\zeta^2}} \times 100\,\% \quad (\zeta < 1) $$
Para \( \zeta = 0.5 \): \( M_p \approx 16.3\,\% \); para \( \zeta = 0.707 \): \( M_p \approx 4.3\,\% \).

**Tiempo de establecimiento al 2 %:**
$$ t_s \approx \frac{4}{\zeta\omega_n} $$
Esta regla del envolvente de la exponencial es precisa para \( 0.2 \leq \zeta \leq 0.8 \).

**Tiempo de subida (10 % al 90 %):** \( t_r \approx 1.8/\omega_n \) para \( \zeta \approx 0.7 \). Hay un compromiso fundamental: reducir \( t_r \) (aumentar \( \omega_n \)) tiende a aumentar \( M_p \) (si no se ajusta \( \zeta \) a la vez).

## 5 — Segundo orden como modelo del lazo de corriente

El lazo de corriente cerrado con un PI se puede aproximar como un sistema de segundo orden. Con planta \( G(s) = 1/(Ls+R) \) y controlador PI \( C(s) = K_p + K_i/s \):

$$ T_{ci}(s) = \frac{K_p s/L + K_i/L}{s^2 + (R+K_p)/L\,s + K_i/L} = \frac{\omega_{ci}^2(s/z_{ci}+1)}{s^2 + 2\zeta_{ci}\omega_{ci}s + \omega_{ci}^2} $$

Identificando: \( \omega_{ci} = \sqrt{K_i/L} \) y \( \zeta_{ci} = (R+K_p)/(2\sqrt{K_i L}) \). Para la **cancelación polo-cero IMC**, se elige \( K_i/K_p = R/L \) (cero del PI cancela el polo de la planta), lo que simplifica la FT cerrada a un primer orden:

$$ T_{ci}(s) \approx \frac{1}{\tau_{ci}s + 1}, \quad \tau_{ci} = L/K_p $$

**Elección \( \zeta = 0.707 \):** mínima sobreoscilación aceptable con máxima velocidad. El lazo de tensión externo ve el lazo de corriente como un polo de primer orden \( 1/(\tau_{ci}s+1) \), válido en la banda de trabajo del lazo de tensión (\( \omega_{cv} \ll 1/\tau_{ci} \)).

## 6 — Resonancia y pico de lazo cerrado

Para \( \zeta < 1/\sqrt{2} \approx 0.707 \), la FT cerrada presenta un pico de resonancia:

**Frecuencia del pico:**
$$ \omega_r = \omega_n\sqrt{1-2\zeta^2} $$

**Altura del pico:**
$$ M_r = \frac{1}{2\zeta\sqrt{1-\zeta^2}} $$

Para \( \zeta = 0.2 \): \( M_r \approx 2.55 \) (+8.1 dB); para \( \zeta = 0.5 \): \( M_r \approx 1.15 \) (+1.2 dB); para \( \zeta = 0.707 \): no hay pico (\( M_r = 1 \), respuesta máximamente plana).

**Ancho de banda:**
$$ \omega_{bw} = \omega_n\sqrt{(1-2\zeta^2)+\sqrt{4\zeta^4-4\zeta^2+2}} $$

**Aplicación al filtro LCL:** la resonancia del LCL actúa como un pico de lazo cerrado si no se amortigua. Con \( \zeta_{LCL} \approx 0.005 \) (sin amortiguamiento), \( M_r \approx 100 \) (40 dB): el pico domina la respuesta y hace inestable el lazo si cae dentro de la banda de control. El amortiguamiento activo eleva \( \zeta \) a 0.1–0.3 reduciendo el pico a 1.7–5.1 dB.

<div class="cfig"><img src="figuras/frecuencias-segundo-orden-analisis.png" alt="Sistema de segundo orden: diagrama de polos, Mp y ts vs zeta, respuesta al escalon y pico de resonancia"><div class="cap">Superior izquierdo: lugar de los polos en función de ζ — a medida que ζ crece desde 0 los polos se alejan del eje imaginario y se aproximan al real. Superior derecho: sobreoscilación Mp y tiempo de establecimiento ts en función de ζ — el óptimo ζ=0.707 equilibra ambas. Inferior izquierdo: respuesta al escalón para cuatro valores de ζ. Inferior derecho: pico de resonancia del lazo cerrado — solo existe para ζ < 0.707.</div></div>

## Conceptos relacionados
- [[respuesta-segundo-orden]] · [[resonancia-rlc]] · [[filtro-lcl]] · [[polos-ceros]] · [[diagrama-bode]]

## Referencias
- Ogata, *Ingeniería de Control Moderna*, Pearson.
- Franklin, Powell, Emami-Naeini, *Feedback Control of Dynamic Systems*.
