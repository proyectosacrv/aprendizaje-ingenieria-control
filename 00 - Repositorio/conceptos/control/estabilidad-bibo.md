---
titulo: Estabilidad (concepto)
slug: estabilidad-bibo
categoria: control
tipo: concepto
nivel: basico
proyectos: []
objetivos: [definir que significa que un sistema sea estable]
tags: [estabilidad, BIBO, polos, equilibrio, cancelacion-polo-cero, estabilidad-interna]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [polos-ceros, margenes-estabilidad, analisis-modal, linealizacion-teoria, estabilidad-lyapunov]
referencias:
  - "Khalil, Nonlinear Systems, Prentice Hall 2002"
  - "Skogestad & Postlethwaite, Multivariable Feedback Control, Wiley 2005"
---

## Definición
Un sistema es **estable** si su respuesta no crece sin límite. La idea básica: ante una entrada
acotada, la salida permanece acotada (**estabilidad BIBO**); y ante una perturbación, el sistema
vuelve (o no se aleja) de su punto de equilibrio.

## Fundamento teórico
Para un sistema **lineal** (o linealizado), la condición es sencilla y exacta:
$$ \text{estable} \iff \text{todos los polos tienen parte real negativa} $$
(autovalores de \( A \) en el semiplano izquierdo). Tipos de estabilidad:
- **Asintóticamente estable**: vuelve al equilibrio (polos con \( \mathrm{Re}<0 \)).
- **Marginal**: ni crece ni decae (polos sobre el eje imaginario; p.ej. un integrador).
- **Inestable**: al menos un polo con \( \mathrm{Re}>0 \).
En sistemas **no lineales**, la estabilidad es **local** (depende del punto de operación) y se
estudia por linealización (ver [[linealizacion-teoria]]) o por métodos de Lyapunov (ver
[[estabilidad-lyapunov]]). No basta con ser estable: interesa el **margen** (cuánto se puede
variar antes de inestabilizar).

<div class="cfig"><img src="figuras/estabilidad-bibo-respuestas.png" alt="respuesta estable vs inestable"><div class="cap">Con todos los polos en Re<0 la respuesta decae y queda acotada (izq.); si algún polo tiene Re>0, crece sin límite (der.). Esa es la frontera de la estabilidad.</div></div>

## 1 — Por qué polos en el SPI ⇒ BIBO (vía la convolución)
**Paso 1 — la salida como convolución.** Para un sistema lineal invariante con respuesta al impulso \( h(t) \), la salida ante cualquier entrada \( u(t) \) es la convolución:

$$ y(t)=\int_0^{t} h(\tau)\,u(t-\tau)\,d\tau $$

**Paso 2 — acotar la salida.** Si la entrada está acotada, \( |u(t)|\le M \) para todo \( t \). Acotamos el valor absoluto de la integral: el módulo de una integral es \( \le \) la integral del módulo, y \( |u(t-\tau)|\le M \):

$$ |y(t)|=\left|\int_0^{t} h(\tau)\,u(t-\tau)\,d\tau\right|\le\int_0^{t}|h(\tau)|\,|u(t-\tau)|\,d\tau\le M\int_0^{\infty}|h(\tau)|\,d\tau $$

**Paso 3 — la condición BIBO.** La salida queda acotada por \( M \) veces una constante **si y solo si** esa integral converge. Esa es la condición exacta de estabilidad BIBO (respuesta al impulso *absolutamente integrable*):

$$ \boxed{\;\int_0^{\infty}|h(\tau)|\,d\tau<\infty\;} $$

**Paso 4 — conectar con los polos.** Para un sistema racional, \( h(t) \) es suma de términos \( t^k e^{p_i t} \), uno por cada polo \( p_i \) (con multiplicidad). El módulo de cada término es \( t^k e^{\mathrm{Re}(p_i)\,t} \). La integral \( \int_0^\infty t^k e^{\mathrm{Re}(p_i)t}\,dt \) converge **únicamente si** \( \mathrm{Re}(p_i)<0 \) (la exponencial decreciente domina cualquier potencia \( t^k \)). Si algún \( \mathrm{Re}(p_i)\ge0 \), ese término no decae y la integral diverge.

**Paso 5 — conclusión.** Por tanto:

$$ \text{BIBO estable}\iff \text{todos los polos cumplen }\mathrm{Re}(p_i)<0 $$

Un solo polo con \( \mathrm{Re}(p_i)\ge0 \) basta para romper la integrabilidad y, por tanto, la estabilidad. Esto explica por qué \( G_2(s)=10/(s^2-2s+5) \) del ejemplo (polos en \( +1\pm j2 \)) crece como \( e^{t}\cos 2t \): el factor \( e^{+t} \) hace divergir la convolución.

## 2 — BIBO vs estabilidad asintótica: cuándo coinciden y cuándo no

**Estabilidad asintótica** se refiere al comportamiento del **estado** \( \mathbf{x}(t) \): todos los modos \( e^{\lambda_i t} \) decaen, o equivalentemente, todos los autovalores de \( A \) tienen parte real negativa. Se comprueba sobre la matriz \( A \) completa, sin reducción algebraica.

**Estabilidad BIBO** se refiere a la relación entrada–salida \( G(s) \): la salida queda acotada ante cualquier entrada acotada. La condición es que todos los polos de \( G(s) \) (los de la FDT observable y controlable) estén en el semiplano izquierdo.

**¿Cuándo coinciden?** En sistemas **completamente controlables y observables**, los polos de \( G(s) \) son exactamente los autovalores de \( A \). Entonces BIBO ↔ asintóticamente estable.

**El peligro de cancelar un polo inestable.** Suponga que el sistema tiene un polo en \( s=+1 \) y un cero también en \( s=+1 \). La FDT resultante cancela ese factor:

$$ G(s) = \frac{s-1}{(s+2)(s-1)} \longrightarrow G_{red}(s) = \frac{1}{s+2} $$

La FDT reducida tiene solo el polo en \( s=-2 \): parece BIBO estable. Sin embargo, el **estado** correspondiente al modo \( e^{+t} \) sigue creciendo —es un modo no observable desde la salida. El sistema es **BIBO estable pero internamente inestable**: la salida no lo delata, pero cualquier perturbación sobre ese estado (ruido, nonlinealidades) activa el modo inestable.

**Regla práctica:** nunca cancelar polos en el semiplano derecho. Un cero de la planta en el SPD se llama **cero de fase no mínima** (NMP) y no se puede cancelar sin crear inestabilidad interna.

**Por qué BIBO no garantiza estabilidad interna.** La estabilidad BIBO solo garantiza que la salida medida es acotada. El estado interno puede tener modos no observables desde la salida. En una implementación real, ese estado crece hasta que alguna limitación física (saturación del actuador, desbordamiento del integrador, sobrecalentamiento) hace colapsar el sistema.

## 3 — La condición en términos de \( g(t) \): integrabilidad absoluta

Ya se demostró en el apartado 1 que BIBO equivale a:

$$ \int_0^{\infty}|g(\tau)|\,d\tau < \infty $$

Veamos cómo esta condición da intuición sobre casos típicos.

**Polo en \( s = \sigma + j\omega \), \( \sigma < 0 \) (estable).** La respuesta al impulso asociada es \( g(t) = e^{\sigma t}\cos(\omega t) \). El módulo:

$$ \int_0^\infty |e^{\sigma t}\cos(\omega t)|\,dt \le \int_0^\infty e^{\sigma t}\,dt = -\frac{1}{\sigma} < \infty \qquad (\sigma < 0) $$

La integral converge: el polo en el SPI garantiza integrabilidad.

**Polo en \( s = +\sigma \), \( \sigma > 0 \) (inestable).** La integral de \( e^{+\sigma t} \) diverge exponencialmente. Un solo polo en el SPD hace que \( g \) no sea absolutamente integrable.

**El integrador \( G(s) = 1/s \), polo en \( s=0 \).** Su respuesta al impulso es \( g(t) = 1 \) (escalón unitario). La integral:

$$ \int_0^\infty 1\,d\tau = \infty $$

No converge: el integrador **no es BIBO estable**. Ante una entrada escalón acotada (\( u(t)=1 \) para \( t\ge0 \)), la salida \( y(t) = t \) crece sin límite. Este es el caso exacto del panel (c) de la figura. El integrador solo es aceptable dentro de un lazo de realimentación cerrado que incluya un polo adicional que lo estabilice.

**El caso general: \( g(t) = \sum_i A_i\,t^{k_i}\,e^{\sigma_i t} \).** Cada término \( t^k e^{\sigma t} \) es absolutamente integrable si y solo si \( \sigma < 0 \). La potencia \( t^k \) no altera la condición: siempre la domina la exponencial para \( t \) suficientemente grande. Solo los polos con \( \mathrm{Re} \ge 0 \) rompen la condición.

## 4 — Sistemas con retardo: el criterio de Nyquist

El retardo puro \( e^{-s\tau} \) tiene infinitos polos en el plano \( s \) (todos sobre el eje imaginario) y no es un sistema racional. El análisis de polos no aplica directamente.

**Norma del retardo en lazo cerrado.** Para un lazo de realimentación con planta \( G(s) \) y controlador \( C(s) \):

$$ L(s) = C(s)\,G(s)\,e^{-s\tau} $$

El **criterio de Nyquist** (ver [[criterio-nyquist]]) sigue siendo válido para funciones de lazo con retardo: se traza el contorno de Nyquist de \( L(j\omega) \) y se cuenta los encirclements de \( -1 \). Un retardo puro \( e^{-j\omega\tau} \) rota el diagrama de Nyquist sin alterar su módulo, pero puede hacer que el contorno encierre el punto \( -1 \) cuando sin el retardo no lo haría.

**El límite de estabilidad: margen de retardo.** Si el lazo sin retardo tiene margen de fase \( PM \) en la frecuencia de cruce \( \omega_c \), la adición de un retardo \( \tau \) sustrae una fase \( \omega_c\,\tau \) (en radianes). Para que el lazo cerrado siga siendo estable:

$$ \omega_c\,\tau < PM \quad\Longrightarrow\quad \tau < \frac{PM}{\omega_c} $$

El margen de retardo es \( \tau_{max} = PM/\omega_c \).

**Para el lazo digital: \( \tau = 1.5\,T_s \).** La aproximación estándar del retardo computacional en control digital (un periodo de cálculo más medio de ZOH) da \( \tau = 1.5\,T_s \). La condición de estabilidad:

$$ 1.5\,T_s\,\omega_c < PM \quad\Longrightarrow\quad \omega_c < \frac{PM}{1.5\,T_s} $$

Ejemplo: \( T_s = 100\,\mu\text{s} \), \( PM = 45° = \pi/4 \,\text{rad} \):

$$ \omega_c < \frac{\pi/4}{1.5 \times 10^{-4}} = 5236\,\text{rad/s} \approx 833\,\text{Hz} $$

Este es exactamente el límite que aparece en el diseño del lazo de corriente del VOC (ver [[control-vectorial]]).

**Sistemas con retardo y polos en el SPI.** Un sistema estable (todos los polos con \( \mathrm{Re}<0 \)) puede destabilizarse con suficiente retardo. El criterio de Nyquist lo detecta automáticamente. No existe una condición simple de polos para sistemas con retardo puro: hay que usar Nyquist o la aproximación de Padé seguida del criterio de Routh (ver [[routh-hurwitz]]).

## 5 — BIBO en sistemas no lineales: la CPL

En sistemas no lineales no existe un criterio de polos universal. La condición BIBO es la misma en esencia (salida acotada ante entrada acotada) pero su verificación requiere otros métodos.

**El bus DC con carga de potencia constante (CPL).** Un bus DC alimenta una CPL de potencia \( P \). La corriente de carga es \( i_{CPL} = P/v_{DC} \): acotada si \( v_{DC} > 0 \), pero diverge si \( v_{DC} \to 0 \). La dinámica del condensador de bus:

$$ C\frac{dv_{DC}}{dt} = i_{src} - \frac{P}{v_{DC}} $$

Esta ecuación no es lineal. Linealizando en el punto de operación \( V_0 \):

$$ \delta \dot{v} = -\frac{1}{RC_{th}}\,\delta v + \frac{P}{V_0^2}\,\delta v = \left(\frac{P}{C V_0^2} - \frac{1}{R C}\right)\delta v $$

El polo linealizado es \( \lambda = P/(CV_0^2) - 1/(RC) \). Para \( \lambda < 0 \) (BIBO estable localmente):

$$ P < \frac{V_0^2}{R} = P_{crit} $$

Si \( P > P_{crit} \), el polo linealizado cruza el eje imaginario al origen: la CPL tiene **resistencia negativa incremental** que desestabiliza el bus. La condición \( P < P_{crit} \) es la condición de BIBO en gran señal aproximada.

**La condición de BIBO en gran señal.** La tensión del bus colapsa cuando no hay equilibrio estable, es decir, cuando la intersección entre la característica de la fuente (\( i_{src}(v_{DC}) \)) y la carga (\( P/v_{DC} \)) desaparece. El criterio geométrico es:

$$ P_{max} = \frac{(V_{OC})^2}{4\,R_{src}} $$

donde \( V_{OC} \) es la tensión de circuito abierto y \( R_{src} \) es la resistencia de Thevenin de la fuente. Para \( P > P_{max} \) no existe punto de operación estable: la tensión colapsa inevitablemente (inestabilidad de gran señal, no solo local).

**Remedio: droop DC y resistencia virtual.** Añadir un lazo de droop DC (\( v_{DC} \) baja → la fuente sube su potencia) amplía la región de operación estable. Equivale a reducir la resistencia Thevenin efectiva de la fuente, elevando \( P_{max} \).

## 6 — Verificación en el proyecto 01

El proyecto 01 (GFM-Impedance) tiene un sistema linealizado con \( n = 15 \) autovalores. La verificación de estabilidad BIBO es inmediata con NumPy:

```python
import numpy as np
evals = np.linalg.eigvals(A)
bibo_estable = np.all(evals.real < 0)
```

**Los 15 modos del sistema:**
- **Modos de potencia** (droop + oscilación VSM): \( \lambda_{P} = -8.3 \pm j\,21.0\,\text{rad/s} \), amortiguamiento \( \zeta = 0.37 \). Es el modo más lento y el más cercano al eje imaginario tras el rediseño.
- **Modo de tensión DC** (lazo de bus): \( \lambda_{DC} = -50\,\text{rad/s} \).
- **Modos de resonancia LCL** (amortiguamiento activo Kad): \( \lambda_{LCL} = -400 \pm j\,21400\,\text{rad/s} \).
- **Modos de corriente** (lazo corriente): \( \lambda_{cc} \approx -800\,\text{rad/s} \).

**Sin Kad:** el filtro LCL tiene un par de polos en \( \pm j\,\omega_{res} \approx \pm j\,21400\,\text{rad/s} \): exactamente sobre el eje imaginario. Un sistema con polos en el eje imaginario es marginalmente estable (no BIBO estable), porque la respuesta al impulso contiene un término oscilatorio que no decae: \( g(t) \sim \cos(\omega_{res} t) \), cuya integral \( \int_0^\infty |\cos(\omega_{res} t)|\,dt \) diverge.

**Con Kad = 6 Ω:** los polos del LCL se desplazan a \( -400 \pm j\,21400\,\text{rad/s} \). La parte real \( -400\,\text{rad/s} \) garantiza \( \int_0^\infty e^{-400 t}|\cos(\omega_{res} t)|\,dt < \infty \): BIBO estable.

El modo más crítico final es \( \lambda_{potencia} = -8.3 \pm j\,21.0 \): amortiguamiento bajo (\( \zeta = 0.37 \)) pero Re < 0. Un aumento de la ganancia de droop o del par de inercia virtual puede mover este modo hacia el eje imaginario: el [[analisis-modal]] lo detectaría antes de que el sistema se vuelva inestable.

<div class="cfig"><img src="figuras/estabilidad-bibo-analisis.png" alt="estabilidad BIBO: tres sistemas, cancelacion polo-cero, integrador, autovalores proy01"><div class="cap">(a) Respuesta al escalón con polos en −1 (estable), 0 (marginal) y +0.5 (inestable): solo el polo en el SPI produce salida acotada. (b) Cancelación polo-cero inestable: la FDT reducida parece estable, pero la respuesta al impulso crece como \(e^t\). (c) El integrador 1/s es BIBO-inestable ante entrada escalón acotada: la salida crece sin límite. (d) Autovalores del proyecto 01: sin Kad los polos del LCL están sobre el eje imaginario (NO BIBO); con Kad=6Ω se trasladan al semiplano izquierdo.</div></div>

## Cuándo y por qué se usa
Es el primer requisito de cualquier diseño de control: un sistema inestable es inutilizable o
peligroso. Toda evaluación empieza por comprobar estabilidad.

## Procedimiento (genérico)
1. Obtén el modelo lineal (o linealiza en el punto de operación).
2. Calcula los polos / autovalores.
3. Estable si todos tienen parte real negativa.
4. Si es no lineal, recuerda que la conclusión es local; valida con simulación de gran señal.

## Ejemplo de aplicación real
**Problema:** Dos buses DC con modelos linealizados: \( G_1(s)=10/(s^2+2s+5) \) (carga resistiva) y \( G_2(s)=10/(s^2-2s+5) \) (carga CPL no compensada). Determinar cuál es BIBO estable.

Para \( G_1 \): polos en \( s=-1\pm j2 \), parte real \( -1<0 \) → **BIBO estable**. Ante un escalón acotado la respuesta oscila y se asienta. Para \( G_2 \): polos en \( s=+1\pm j2 \), parte real \( +1>0 \) → **no BIBO estable**. Ante el mismo escalón, la respuesta crece como \( e^t\cos(2t) \) hasta que alguna limitación física (saturación, protección) interviene. El diagnóstico toma segundos con `np.linalg.eigvals(A)`.

## Ejemplo de código
```python
import numpy as np
estable = np.all(np.linalg.eigvals(A).real < 0)
```

## Parámetros y valores típicos
Se busca margen: no basta \( \mathrm{Re}<0 \), interesa que sea bastante negativo y con
amortiguamiento suficiente (ver [[margenes-estabilidad]]).

## Errores comunes
- Confundir estabilidad con buen desempeño (un sistema estable puede ser lentísimo u oscilatorio).
- Extender la estabilidad local de un linealizado a gran señal (saturaciones, faltas).
- Cancelar un polo inestable algebraicamente y concluir que el sistema es BIBO estable: la estabilidad interna queda comprometida.
- Ignorar el polo del integrador en lazos abiertos: 1/s no es BIBO estable por sí solo.

## Conceptos relacionados
- [[polos-ceros]] · [[margenes-estabilidad]] · [[analisis-modal]] · [[linealizacion-teoria]] · [[estabilidad-lyapunov]] · [[criterio-nyquist]] · [[routh-hurwitz]]

## Referencias
- Khalil, *Nonlinear Systems*, 2002.
- Skogestad & Postlethwaite, *Multivariable Feedback Control*, 2005.
