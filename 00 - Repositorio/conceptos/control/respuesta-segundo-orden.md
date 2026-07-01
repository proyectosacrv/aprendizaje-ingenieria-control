---
titulo: Respuesta de segundo orden (ζ, ωn)
slug: respuesta-segundo-orden
categoria: control
tipo: concepto
nivel: basico
proyectos: []
objetivos: [relacionar amortiguamiento y frecuencia natural con la respuesta]
tags: [segundo-orden, amortiguamiento, frecuencia-natural, sobreimpulso, basico, tiempo-pico, resonancia, sobreamortiguado, cero-finito, diseno]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [sistema-primer-orden, polos-ceros, metricas-desempeno, funcion-transferencia]
referencias:
  - "Ogata, Ingeniería de Control Moderna, Pearson"
  - "Franklin, Powell, Emami-Naeini, Feedback Control of Dynamic Systems, Pearson"
---

## Definición
Sistema con dos polos que puede **oscilar**. Su respuesta queda descrita por dos parámetros: la
**frecuencia natural** \( \omega_n \) (rapidez) y el **amortiguamiento** \( \zeta \) (cuánto
oscila). Es el modelo de referencia para especificar desempeño.

## Fundamento teórico
$$ G(s) = \frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2} $$
Polos: \( s=-\zeta\omega_n \pm j\omega_n\sqrt{1-\zeta^2} \). Según \( \zeta \):
- \( \zeta>1 \): **sobreamortiguado** (no oscila, lento).
- \( \zeta=1 \): **crítico** (lo más rápido sin oscilar).
- \( 0<\zeta<1 \): **subamortiguado** (oscila y se asienta).
- \( \zeta=0 \): oscilación permanente (al límite de estabilidad).

Métricas (caso subamortiguado):
$$ M_p = e^{-\pi\zeta/\sqrt{1-\zeta^2}}\;(\text{sobreimpulso}), \qquad
   t_s \approx \frac{4}{\zeta\omega_n}\;(\text{establecimiento al 2\%}) $$

<div class="cfig"><img src="figuras/respuesta-segundo-orden-familia.png" alt="respuestas al escalon segun zeta"><div class="cap">Respuesta al escalón según ζ: ζ&lt;1 oscila (más sobreimpulso cuanto menor ζ), ζ=1 es lo más rápido sin oscilar, ζ&gt;1 es lento sin oscilar. ζ≈0.7 es el compromiso habitual.</div></div>

<div class="cfig"><img src="figuras/respuesta-segundo-orden-analisis.png" alt="analisis ampliado: familia escalon, resonancia en frecuencia, efecto del cero, diagrama de diseno"><div class="cap">Análisis ampliado: (a) familia de escalones con tp y ts marcados para ζ=0.5; (b) pico de resonancia en frecuencia según ζ, desaparece para ζ≥1/√2; (c) efecto del cero adicional sobre el sobreimpulso; (d) diagrama de diseño con iso-Mp e iso-ts en el plano (ζ, ωn).</div></div>

## 1 — Sobreimpulso Mp desde la envolvente del escalón

**Paso 1 — respuesta al escalón del sistema subamortiguado.** Para \( G(s)=\omega_n^2/(s^2+2\zeta\omega_n s+\omega_n^2) \) con entrada escalón unitario \( U(s)=1/s \), la antitransformada da:

$$ y(t)=1-\frac{e^{-\zeta\omega_n t}}{\sqrt{1-\zeta^2}}\sin\!\left(\omega_d t+\phi\right), \quad \omega_d=\omega_n\sqrt{1-\zeta^2},\quad \phi=\arccos\zeta $$

La respuesta oscila alrededor del valor final 1, modulada por la envolvente \( e^{-\zeta\omega_n t}/\sqrt{1-\zeta^2} \).

**Paso 2 — localizar el primer pico.** El primer máximo ocurre cuando \( \dot{y}(t)=0 \) por primera vez para \( t>0 \). Derivando y simplificando, la condición reduce a \( \sin(\omega_d t)=0 \) con \( \omega_d t>0 \), es decir \( t_p=\pi/\omega_d \).

**Paso 3 — calcular el sobreimpulso.** Evaluando \( y(t_p) \) y restando el valor final 1:

$$ M_p = y(t_p)-1 = \frac{e^{-\zeta\omega_n\cdot\pi/\omega_d}}{\sqrt{1-\zeta^2}}\cdot\sin(\pi+\phi)\cdot(-1) $$

Como \( \sin(\pi+\phi)=-\sin\phi \) y \( \sin\phi=\sqrt{1-\zeta^2} \) (porque \( \phi=\arccos\zeta \)), los factores \( \sqrt{1-\zeta^2} \) se cancelan:

$$ \boxed{M_p = e^{-\pi\zeta/\sqrt{1-\zeta^2}}} $$

Para \( \zeta=0.5 \): \( M_p=e^{-\pi\cdot0.5/0.866}=e^{-1.814}\approx0.163 \) (16.3%).

## 2 — Tiempo de establecimiento ts ≈ 4/(ζωn) desde el criterio del 2%

**Paso 1 — banda de tolerancia del 2%.** Se define \( t_s \) como el instante a partir del cual \( |y(t)-1|\le0.02 \) para siempre. La cota superior del error es la envolvente:

$$ |y(t)-1|\le\frac{e^{-\zeta\omega_n t}}{\sqrt{1-\zeta^2}} $$

**Paso 2 — imponer la cota.** Para \( \zeta \) moderado (\( 0.3\lesssim\zeta\lesssim0.8 \)), \( \sqrt{1-\zeta^2}\approx1 \). Igualando la envolvente a 0.02:

$$ e^{-\zeta\omega_n t_s}=0.02 \;\Rightarrow\; \zeta\omega_n t_s=\ln(50)\approx3.91 $$

**Paso 3 — fórmula práctica.** Redondeando \( \ln(50)\approx4 \):

$$ \boxed{t_s \approx \frac{4}{\zeta\omega_n}} $$

Esta fórmula es exacta solo si la envolvente domina el criterio del 2%; para \( \zeta \) muy pequeño las oscilaciones permanecen dentro de la banda más tiempo, pero la fórmula es un buen orden de magnitud de diseño.

## 3 — El tiempo de pico tp: de la condición dy/dt=0

El tiempo de pico \( t_p \) es el instante del **primer máximo** de la respuesta al escalón. Localizarlo requiere derivar la expresión exacta de \( y(t) \) e igualar a cero.

**Paso 1 — derivada de la respuesta.** Partiendo de:
$$ y(t)=1-\frac{e^{-\zeta\omega_n t}}{\sqrt{1-\zeta^2}}\sin(\omega_d t+\phi) $$
se aplica la regla del producto al término oscilatorio. Con \( \omega_d=\omega_n\sqrt{1-\zeta^2} \):

$$
\frac{dy}{dt}=\frac{e^{-\zeta\omega_n t}}{\sqrt{1-\zeta^2}}\Big[\zeta\omega_n\sin(\omega_d t+\phi)-\omega_d\cos(\omega_d t+\phi)\Big]
$$

Expandiendo \( \zeta\omega_n\sin(\omega_d t+\phi)-\omega_d\cos(\omega_d t+\phi) \) en la forma \( A\sin(\omega_d t+\phi-\delta) \) y usando \( \phi=\arccos\zeta \), la expresión colapsa a:

$$
\frac{dy}{dt}=\frac{\omega_n}{\sqrt{1-\zeta^2}}\,e^{-\zeta\omega_n t}\,\sin(\omega_d t)
$$

**Paso 2 — condición de máximo.** El exponencial \( e^{-\zeta\omega_n t} \) nunca se anula para \( t>0 \). Luego la condición \( dy/dt=0 \) se reduce a:
$$ \sin(\omega_d t_p)=0 \;\Longrightarrow\; \omega_d t_p=k\pi,\quad k=1,2,\ldots $$

El **primer** máximo corresponde a \( k=1 \):

$$
\boxed{t_p=\frac{\pi}{\omega_d}=\frac{\pi}{\omega_n\sqrt{1-\zeta^2}}}
$$

**Paso 3 — por qué es ωd y no ωn quien fija tp.** La envolvente \( e^{-\zeta\omega_n t} \) solo controla la **amplitud** de las oscilaciones, no su posición temporal: decae monotónicamente y no tiene ceros. Los ceros de \( dy/dt \) provienen exclusivamente del seno amortiguado \( \sin(\omega_d t) \), que oscila a la frecuencia \( \omega_d < \omega_n \). Por tanto, tp depende solo de \( \omega_d \); reducir \( \zeta \) acerca \( \omega_d \) a \( \omega_n \) y adelanta el pico, pero nunca llega a \( \pi/\omega_n \) salvo en el límite \( \zeta\to 0 \).

**Tabla de tp para ωn=10 rad/s:**

| ζ | ωd [rad/s] | tp [ms] | Nota |
|---|-----------|---------|------|
| 0.3 | 9.54 | 329 | Pico temprano, Mp alto |
| 0.5 | 8.66 | 363 | Compromiso |
| 0.7 | 7.14 | 440 | ζ de diseño habitual |
| 1.0 | 0 → ∞ | ∞ | Caso crítico: sin pico |

En el caso crítico (\( \zeta=1 \)) la respuesta es monotónicamente creciente sin máximo local; la fórmula \( t_p=\pi/\omega_d \) diverge porque \( \omega_d=0 \).

## 4 — El régimen subamortiguado crítico: ζ=1/√2≈0.707

El valor \( \zeta=1/\sqrt{2}\approx0.707 \) es especial porque separa dos comportamientos cualitativamente distintos en la **respuesta en frecuencia**, no en el dominio temporal.

**Paso 1 — módulo de la función de transferencia en frecuencia.** Para \( s=j\omega \):
$$
|G(j\omega)|=\frac{\omega_n^2}{\sqrt{(\omega_n^2-\omega^2)^2+(2\zeta\omega_n\omega)^2}}
$$

**Paso 2 — condición de pico de resonancia.** Se busca el \( \omega \) que maximiza \( |G(j\omega)| \), equivalente a minimizar el denominador \( D(\omega)=(\omega_n^2-\omega^2)^2+(2\zeta\omega_n\omega)^2 \). Derivando:
$$
\frac{dD}{d\omega}=4\omega\Big[-(\omega_n^2-\omega^2)+2\zeta^2\omega_n^2\Big]=0
$$
La solución no trivial (\( \omega\ne0 \)) es:
$$
\omega_n^2-\omega_r^2=2\zeta^2\omega_n^2 \;\Longrightarrow\; \omega_r^2=\omega_n^2(1-2\zeta^2)
$$
Esta solución existe solo si \( 1-2\zeta^2>0 \), es decir \( \zeta<1/\sqrt{2} \). Para \( \zeta\ge1/\sqrt{2} \), el denominador es monótonamente creciente con \( \omega \) y **no hay pico**.

**Paso 3 — frecuencia y amplitud del pico.** Cuando existe:
$$
\boxed{\omega_r=\omega_n\sqrt{1-2\zeta^2}}, \qquad |G(j\omega_r)|_{\max}=\frac{1}{2\zeta\sqrt{1-\zeta^2}}
$$

Para \( \zeta=1/\sqrt{2} \): \( \omega_r=0 \) (el pico se desplaza a frecuencia cero y desaparece), y \( |G(0)|=1 \) — la respuesta es máximamente plana. Este es el criterio del **filtro de Butterworth** de segundo orden.

**Tabla resumen ζ → pico de resonancia y sobreimpulso:**

| ζ | Pico \|G\|_max [dB] | ωr/ωn | Mp escalón [%] |
|---|--------------------|---------|----|
| 0.1 | +14.0 | 0.990 | 73 |
| 0.3 | +5.1 | 0.906 | 37 |
| 0.5 | +1.25 | 0.707 | 16 |
| 0.7 | +0.06 | 0.141 | 4.6 |
| 0.707 | 0 (plano) | 0 | 4.3 |

Nótese que el sobreimpulso no desaparece en \( \zeta=1/\sqrt{2} \): la condición "sin pico en frecuencia" y "sin sobreimpulso en escalón" son distintas. El sobreimpulso llega a cero solo en \( \zeta=1 \) (caso crítico).

## 5 — El caso sobreamortiguado ζ>1: dos polos reales

Para \( \zeta>1 \), el discriminante \( \zeta^2-1>0 \) y los dos polos son reales y negativos:
$$
s_{1,2}=-\zeta\omega_n\pm\omega_n\sqrt{\zeta^2-1}
$$

**Paso 1 — separación de los polos.** Definiendo \( a=\omega_n\sqrt{\zeta^2-1} \):
$$
s_1=-\zeta\omega_n+a \quad(\text{polo lento: módulo pequeño}), \qquad
s_2=-\zeta\omega_n-a \quad(\text{polo rápido: módulo grande})
$$

**Paso 2 — aproximación para ζ>>1.** Cuando \( \zeta\gg1 \), \( \sqrt{\zeta^2-1}\approx\zeta-1/(2\zeta) \):
$$
s_1\approx -\frac{\omega_n}{2\zeta}\quad(\text{polo dominante lento}),\qquad
s_2\approx -2\zeta\omega_n\quad(\text{polo rápido, despreciable})
$$

El polo rápido se amortigua en un tiempo \( 1/|s_2|\approx 1/(2\zeta\omega_n) \) muy corto. La respuesta queda dominada por el polo lento con constante de tiempo:
$$
\tau_1=\frac{1}{|s_1|}\approx\frac{2\zeta}{\omega_n}
$$

**Paso 3 — tiempo de establecimiento sobreamortiguado.** Aplicando el criterio del 2% al polo dominante:
$$
t_{s,\text{sobre}}\approx 4\tau_1=\frac{8\zeta}{\omega_n}
$$

Comparando con el caso subamortiguado óptimo (\( \zeta=0.7 \)): \( t_{s,0.7}=4/(0.7\,\omega_n)\approx 5.7/\omega_n \). Para \( \zeta=2 \): \( t_{s}=16/\omega_n \), es decir **2.8 veces más lento** sin ninguna ventaja: el sobreimpulso ya es cero para \( \zeta=1 \).

**Ejemplo numérico. ζ=2, ωn=10 rad/s:**
$$
s_1=-20+10\sqrt{3}=-2.68\,\text{rad/s},\quad s_2=-20-10\sqrt{3}=-37.3\,\text{rad/s}
$$
$$
\tau_1=\frac{1}{2.68}\approx0.37\,\text{s},\qquad t_s\approx4\times0.37=1.49\,\text{s}
$$
Con \( \zeta=0.7 \) y el mismo \( \omega_n \): \( t_s=4/(0.7\times10)=0.57\,\text{s} \). El sobreamortiguamiento cuesta un factor 2.6 en tiempo de respuesta.

**Moraleja:** nunca se diseña intencionalmente con \( \zeta>1 \) en un lazo de control de velocidad o potencia. Si aparece, significa que \( \omega_n \) se ha reducido innecesariamente (por ejemplo, por exceso de filtrado o ganancias demasiado bajas).

## 6 — Efecto de los ceros sobre el sobreimpulso: el cero finito

En muchos sistemas reales la función de transferencia en lazo cerrado tiene un **cero finito** adicional. Comprender su efecto es esencial para predecir el sobreimpulso real.

**Paso 1 — forma con cero.** Sea:
$$
G(s)=\frac{\omega_n^2\left(1+s/\omega_z\right)}{s^2+2\zeta\omega_n s+\omega_n^2}
$$

El cero está en \( s=-\omega_z \). El numerador puede reescribirse como:
$$
\omega_n^2\left(1+\frac{s}{\omega_z}\right)=\omega_n^2+\frac{\omega_n^2}{\omega_z}\,s
$$

**Paso 2 — descomposición en respuesta base más derivada.** En el dominio temporal, multiplicar por \( (1+s/\omega_z) \) equivale a sumar la respuesta original más su derivada escalada:
$$
y_{\text{cero}}(t)=y_{\text{base}}(t)+\frac{1}{\omega_z}\dot{y}_{\text{base}}(t)
$$

En el instante del pico \( t_p \), \( \dot{y}_{\text{base}}(t_p)=0 \) por definición. Pero **antes** del pico la derivada es positiva y **eleva** la respuesta, aumentando el sobreimpulso.

**Paso 3 — análisis según la posición del cero:**

- \( \omega_z\gg\omega_n \): el cero está lejos del origen, \( 1/\omega_z\to0 \) — la derivada contribuye poco, el sobreimpulso es casi el de la base.
- \( \omega_z\approx\omega_n \): el cero amplifica significativamente la oscilación.
- \( \omega_z=2\zeta\omega_n \): el cero coincide con la parte real de los polos — máxima contribución de la derivada.

**Tabla: ωz/ωn → Mp para ζ=0.5, ωn=10 rad/s:**

| ωz/ωn | ωz [rad/s] | Mp [%] | Nota |
|--------|-----------|--------|------|
| 0.5 | 5 | ≈65 | Cero muy cercano: enorme Mp |
| 1.0 | 10 | ≈46 | Cero al nivel de ωn |
| 2.0 | 20 | ≈26 | Contribución moderada |
| 5.0 | 50 | ≈18 | Casi como sin cero |
| ∞ | — | 16.3 | Sin cero (referencia) |

**Relevancia práctica — el PI con cancelación de polo.** Cuando un PI cancela exactamente el polo de la planta de primer orden (\( T_i=K_p/K_i=L/R \)), la función de lazo cerrado resultante es:
$$
\frac{i}{i^*}=\frac{\alpha_c}{s+\alpha_c}
$$
un **primer orden sin cero** → sobreimpulso nulo. Este es el principio del método IMC/cancelación de polo aplicado al lazo de corriente (ver [[desacoplo-dq]]). Si la cancelación es imperfecta (error en \( L \) o \( R \)), aparece un cero residual que introduce sobreimpulso, pero el efecto es pequeño mientras el error sea <10%.

## 7 — Diseño iterativo de un lazo de segundo orden para el modo de potencia

**Especificación de partida:** sobreimpulso \( M_p<10\% \), tiempo de establecimiento \( t_s<0.5\,\text{s} \), frecuencia de oscilación visible \( f_{osc}<5\,\text{Hz} \).

**Paso 1 — traducir Mp a ζ.** De \( M_p<0.10 \):
$$
e^{-\pi\zeta/\sqrt{1-\zeta^2}}<0.10 \;\Rightarrow\; \frac{\pi\zeta}{\sqrt{1-\zeta^2}}>\ln(10)\approx2.303
\;\Rightarrow\; \zeta>0.591
$$
Se elige **ζ=0.7** para dar margen.

**Paso 2 — traducir ts a ωn mínimo.** De \( t_s<0.5\,\text{s} \):
$$
\frac{4}{\zeta\omega_n}<0.5 \;\Rightarrow\; \omega_n>\frac{4}{0.7\times0.5}=11.4\,\text{rad/s}
$$

**Paso 3 — traducir f_osc a ωn máximo.** La frecuencia de oscilación visible es \( \omega_d=\omega_n\sqrt{1-\zeta^2} \). Para \( f_{osc}<5\,\text{Hz}=31.4\,\text{rad/s} \):
$$
\omega_n\sqrt{1-0.49}<31.4 \;\Rightarrow\; \omega_n<\frac{31.4}{0.714}=43.9\,\text{rad/s}
$$

**Rango válido:** \( 11.4<\omega_n<43.9\,\text{rad/s} \). Se elige **ωn=20 rad/s** (centro del rango).

**Paso 4 — verificar las tres especificaciones:**

| Especificación | Límite | Valor con ζ=0.7, ωn=20 | Estado |
|---------------|--------|------------------------|--------|
| Mp | <10% | 4.6% | ✓ |
| ts | <0.5s | 4/(0.7·20)=0.29s | ✓ |
| f_osc | <5Hz | ωd/(2π)=20·0.714/6.28=2.27Hz | ✓ |

**Paso 5 — vincular con los parámetros físicos del droop.** En el modo de potencia de un GFM con droop y filtro de medida de primera orden:
$$
\omega_n=\sqrt{m_p\,K_s\,\omega_f},\qquad \zeta=\frac{\omega_f}{2\omega_n}
$$
donde \( m_p \) es la ganancia del droop [rad/s/W], \( K_s \) es la rigidez del enlace [W/rad], y \( \omega_f \) es el ancho de banda del filtro de potencia. Despejando con \( \omega_n=20 \), \( \zeta=0.7 \):
$$
\omega_f=2\zeta\omega_n=2\times0.7\times20=28\,\text{rad/s}\;\;(f_f=4.5\,\text{Hz})
$$
$$
m_p=\frac{\omega_n^2}{\omega_f\,K_s}=\frac{400}{28\,K_s}
$$
Si \( K_s=10^5\,\text{W/rad} \) (red con SCR moderado): \( m_p=1.43\times10^{-4}\,\text{rad/s/W}=0.143\,\text{rad/s/kW} \).

**Tabla de iteración:**

| Iteración | ζ | ωn | Mp [%] | ts [s] | f_osc [Hz] | Estado |
|-----------|---|-----|--------|-------|-----------|--------|
| 1 | 0.5 | 20 | 16.3 | 0.40 | 2.76 | Mp ✗ |
| 2 | 0.7 | 20 | 4.6 | 0.29 | 2.27 | ✓✓✓ |
| 3 | 0.7 | 30 | 4.6 | 0.19 | 3.40 | Más rápido, válido |
| 4 | 0.7 | 10 | 4.6 | 0.57 | 1.13 | ts ✗ |

La iteración 2 (ζ=0.7, ωn=20) es el punto de diseño: cumple todas las especificaciones con margen razonable.

## Cuándo y por qué se usa
Es el patrón con el que se fijan especificaciones (sobreimpulso, tiempo de establecimiento) y se
interpretan los polos dominantes de sistemas de orden mayor.

## Procedimiento (genérico)
1. Identifica los dos polos dominantes → calcula \( \omega_n \) y \( \zeta \).
2. Estima sobreimpulso \( M_p \) y tiempo de establecimiento \( t_s \).
3. Ajusta el control para mover los polos al \( \zeta \) y \( \omega_n \) deseados.

## Ejemplo de aplicación real
**Problema:** El lazo de potencia de un GFM con droop muestra sobreimpulso del 25 % y frecuencia de oscilación de 3.3 Hz. Determinar \( \zeta \) y \( \omega_n \), y juzgar si cumple \( \zeta\ge0.6 \).

Del sobreimpulso: \( M_p=0.25\Rightarrow\zeta=\sqrt{\ln^2(M_p)/(\pi^2+\ln^2(M_p))}\approx0.40 \). De la frecuencia amortiguada \( \omega_d=2\pi\times3.3\approx20.7\,\text{rad/s} \): \( \omega_n=\omega_d/\sqrt{1-\zeta^2}\approx22.6\,\text{rad/s} \). Con \( \zeta=0.40 \) el sistema **no cumple** \( \zeta\ge0.6 \) (sobreimpulso objetivo \(\le10\,\%\)). Para subir \( \zeta \): reducir \( m_p \) del droop (baja la ganancia del lazo de potencia) o añadir [[impedancia-virtual]] (introduce amortiguamiento sin cambiar \( \omega_n \)). Con \( \zeta=0.7 \): sobreimpulso \(\approx4.6\,\%\), modo bien amortiguado.

## Ejemplo de código
```python
import numpy as np, control as ct
wn, z = 10.0, 0.5
G = ct.tf([wn**2], [1, 2*z*wn, wn**2])
Mp = np.exp(-np.pi*z/np.sqrt(1-z**2))      # ~16% para z=0.5
tp = np.pi / (wn * np.sqrt(1 - z**2))       # tiempo de pico
ts = 4 / (z * wn)                           # tiempo de establecimiento al 2%
wr = wn * np.sqrt(1 - 2*z**2) if z < 1/np.sqrt(2) else None  # frecuencia de resonancia
```

## Parámetros y valores típicos
\( \zeta=0.7 \): ~5% de sobreimpulso, buen compromiso. \( \zeta=0.5 \): ~16%. Diseño habitual
\( \zeta=0.5\text{–}0.8 \). Para \( \zeta\ge1/\sqrt{2}\approx0.707 \): sin pico de resonancia en frecuencia. Para \( \zeta\ge1 \): sin sobreimpulso en escalón pero respuesta significativamente más lenta.

## Errores comunes
- Aplicar las fórmulas de 2º orden a un sistema de orden alto sin verificar que hay polos dominantes.
- Buscar \( \zeta \) muy alto (lento) o muy bajo (oscilatorio) sin compromiso.
- Confundir la condición "sin pico de resonancia" (\( \zeta\ge1/\sqrt{2} \)) con "sin sobreimpulso" (\( \zeta\ge1 \)): son distintas.
- Ignorar el efecto de los ceros al predecir el sobreimpulso real en lazo cerrado.

## Conceptos relacionados
- [[sistema-primer-orden]] · [[polos-ceros]] · [[metricas-desempeno]] · [[desacoplo-dq]]

## Referencias
- Ogata, *Ingeniería de Control Moderna*.
- Franklin, Powell, Emami-Naeini, *Feedback Control of Dynamic Systems*.
