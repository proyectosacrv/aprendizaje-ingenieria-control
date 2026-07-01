---
titulo: Estabilidad por Bode — márgenes de ganancia, fase y módulo
slug: margenes-estabilidad
categoria: metodologia
tipo: metodo
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [decidir la estabilidad de un lazo desde el Bode de la ganancia de lazo, cuantificar cuánto margen queda antes de inestabilizarse, diseñar iterativamente para cumplir PM, GM y Ms, extender al caso MIMO]
tags: [margen-fase, margen-ganancia, M_s, bode, estabilidad, robustez, nyquist, retardo-digital, condicionalmente-estable, MIMO, diseño-iterativo]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [diagrama-bode, criterio-nyquist, funciones-sensibilidad, loop-shaping, robustez-parametrica, impedancia-salida-estabilidad]
referencias:
  - "Aström, Murray, Feedback Systems, Princeton 2008"
  - "Franklin, Powell, Emami-Naeini, Feedback Control of Dynamic Systems"
  - "Skogestad, Postlethwaite, Multivariable Feedback Design, Wiley 2005"
  - "Middleton, Goodwin, Digital Control and Estimation, Prentice Hall 1990"
---

## Definición
Los márgenes de estabilidad miden **cuánto puede cambiar** un lazo de control antes de volverse inestable. No dicen solo si el sistema es estable: cuantifican la **robustez** (cuánta ganancia, fase o retardo de más aguanta). Todo se lee sobre el **Bode de la ganancia de lazo** \( L(j\omega)=C(j\omega)\,G(j\omega) \), donde \( C \) es el controlador y \( G \) la planta.

## El punto crítico: por qué −1 (o −180° con ganancia 1)
Un lazo de realimentación negativa tiene función de transferencia en lazo cerrado
$$ T(s)=\frac{L(s)}{1+L(s)} $$
que se hace infinita (polos del lazo cerrado) donde \( 1+L(s)=0 \), es decir donde \( L(s)=-1 \). El número complejo \( -1 \) tiene módulo \( 1 \) y fase \( -180^\circ \). La idea física: si a alguna frecuencia la señal recorre el lazo y vuelve con la **misma amplitud** (\( |L|=1 \)) y **invertida** (\( -180^\circ \)), la realimentación —que debía ser negativa— se vuelve positiva y se sostiene sola: oscilación. Por eso toda la estabilidad se juega en cuán cerca pasa \( L(j\omega) \) del punto \( -1 \).

## Criterio de estabilidad por Bode
Para una ganancia de lazo **estable en lazo abierto y de fase mínima** (el caso habitual de un lazo de corriente/tensión bien planteado), el criterio es directo:

> El lazo cerrado es **estable** si, en la frecuencia de cruce de ganancia \( \omega_c \) (donde \( |L(j\omega_c)|=1 \), es decir 0 dB), la **fase está por encima de −180°**.

Equivalentemente, en la frecuencia de cruce de fase \( \omega_{180} \) (donde la fase vale −180°), la ganancia debe estar **por debajo de 0 dB**. De ahí salen las dos distancias al punto crítico:

- **Margen de fase (PM):** cuánta fase de más se puede perder en \( \omega_c \) antes de llegar a −180°:
$$ \mathrm{PM}=180^\circ+\angle L(j\omega_c) \qquad (|L(j\omega_c)|=1) $$
- **Margen de ganancia (GM):** cuánto se puede subir la ganancia en \( \omega_{180} \) antes de llegar a 0 dB:
$$ \mathrm{GM}=\frac{1}{|L(j\omega_{180})|} \qquad (\angle L(j\omega_{180})=-180^\circ) $$
(en dB, \( \mathrm{GM}_{dB}=-20\log_{10}|L(j\omega_{180})| \)). Ambos positivos ⇒ estable y con holgura; un PM o GM negativo señala inestabilidad.

<div class="cfig"><img src="figuras/margenes-estabilidad-bode.png" alt="márgenes de ganancia y fase sobre el Bode de la ganancia de lazo"><div class="cap">Sobre el Bode de \(L(j\omega)\): el margen de fase (PM) se mide en el cruce de ganancia (\(|L|=0\) dB) y el de ganancia (GM) en el cruce de fase (−180°). Aquí PM≈63°, GM≈27 dB (diseño holgado).</div></div>

### Cómo leerlo paso a paso sobre el Bode
1. Localiza el **cruce de ganancia** \( \omega_c \): donde la curva de magnitud corta 0 dB.
2. Baja a la curva de fase en esa misma \( \omega_c \) y mide cuánto falta hasta −180°: ese hueco es el **PM**.
3. Localiza el **cruce de fase** \( \omega_{180} \): donde la fase pasa por −180°.
4. Sube a la curva de magnitud en esa \( \omega_{180} \) y mide cuántos dB faltan hasta 0 dB: ese hueco (en valor absoluto) es el **GM**.

## Por qué el margen de fase fija el amortiguamiento y la sobreoscilación
El PM no es un número abstracto: gobierna cómo responde el lazo cerrado. Para un lazo dominado por dos polos, el amortiguamiento se aproxima por
$$ \zeta \approx \frac{\mathrm{PM}}{100} \quad (\mathrm{PM\ en\ grados}) $$
de modo que PM grande ⇒ \( \zeta \) grande ⇒ respuesta amortiguada; PM pequeño ⇒ \( \zeta \) pequeño ⇒ sobreoscilación y oscilaciones lentas de extinguir. Un PM \( \to 0 \) es un lazo al borde de oscilar de forma sostenida.

<div class="cfig"><img src="figuras/margenes-estabilidad-pm-respuesta.png" alt="comparación de tres diseños con distinto margen de fase y su respuesta al escalón en lazo cerrado"><div class="cap">Tres diseños del mismo lazo con distinto PM (izquierda, Bode con el cruce de ganancia marcado) y su respuesta al escalón en lazo cerrado (derecha). A menos PM, más sobreoscilación y más oscilación residual; a más PM, respuesta más amortiguada.</div></div>

## Margen de módulo (el más completo)
PM y GM miran solo dos frecuencias concretas. El **margen de módulo** mira la distancia mínima de \( L(j\omega) \) al punto \( -1 \) en **todas** las frecuencias, y es por eso la medida de robustez más fiable. Se define con el pico de la función de sensibilidad \( S=1/(1+L) \) (ver [[funciones-sensibilidad]]):
$$ M_s=\max_\omega |S(j\omega)|=\max_\omega \frac{1}{|1+L(j\omega)|}, \qquad \text{margen de módulo}=\frac{1}{M_s} $$
\( M_s \) es el inverso de esa distancia mínima: \( M_s<2 \) (≈6 dB) es buen objetivo. Un sistema puede tener PM y GM aparentemente buenos y aun así un \( M_s \) alto (la curva se acerca a −1 en una frecuencia intermedia): por eso conviene mirar \( M_s \).

## Margen de retardo
Un retardo puro \( e^{-s\tau} \) no cambia la magnitud pero resta fase \( \omega\tau \). El PM dice cuánto retardo aguanta el lazo antes de inestabilizarse:
$$ \tau_{max}=\frac{\mathrm{PM\ (rad)}}{\omega_c} $$
Es el chequeo clave en control digital: el retardo de cómputo más el de PWM (del orden de \( 1.5\,T_s \)) debe ser bastante menor que \( \tau_{max} \).

<div class="cfig"><img src="figuras/margenes-estabilidad-analisis.png" alt="Análisis completo: Bode con PM/GM/Ms, Nyquist con círculo Ms, escalón tres PM, sistema condicionalmente estable"><div class="cap">Panel (a): Bode con PM, GM y \(M_s\) marcados sobre la misma curva de \(L(j\omega)\). Panel (b): Nyquist con el círculo de margen de módulo (radio \(1/M_s\) centrado en −1) tangente a la curva de lazo. Panel (c): respuesta al escalón de lazo cerrado para PM=20°, 45°, 70°; a menor PM, mayor sobreoscilación y mayor \(M_s\). Panel (d): ejemplo condicionalmente estable con dos cruces de ganancia, uno estable (verde) y uno inestable (rojo).</div></div>

## 1 — De dónde sale \( \mathrm{PM}\approx100\,\zeta \)
**Paso 1 — el lazo canónico de segundo orden.** Tómese la ganancia de lazo prototipo de dos polos (un integrador y un polo, el caso de un PI bien planteado o de un doble integrador amortiguado):
$$ L(s)=\frac{\omega_n^2}{s\,(s+2\zeta\omega_n)} $$
En lazo cerrado da \( T(s)=\dfrac{\omega_n^2}{s^2+2\zeta\omega_n s+\omega_n^2} \), el segundo orden estándar con amortiguamiento \( \zeta \) y frecuencia natural \( \omega_n \). Así el PM del lazo abierto queda ligado al \( \zeta \) del lazo cerrado.

**Paso 2 — frecuencia de cruce de ganancia.** \( \omega_c \) cumple \( |L(j\omega_c)|=1 \):
$$ |L(j\omega_c)|=\frac{\omega_n^2}{\omega_c\sqrt{\omega_c^2+(2\zeta\omega_n)^2}}=1 \;\Rightarrow\; \omega_c^2\big(\omega_c^2+4\zeta^2\omega_n^2\big)=\omega_n^4 $$
Resolviendo la bicuadrática en \( (\omega_c/\omega_n)^2 \):
$$ \left(\frac{\omega_c}{\omega_n}\right)^2=\sqrt{1+4\zeta^4}-2\zeta^2 $$

**Paso 3 — fase en el cruce y margen de fase.** La fase de \( L \) es \( \angle L(j\omega_c)=-90^\circ-\arctan\!\dfrac{\omega_c}{2\zeta\omega_n} \). Por definición \( \mathrm{PM}=180^\circ+\angle L(j\omega_c) \), luego
$$ \mathrm{PM}=90^\circ-\arctan\frac{\omega_c}{2\zeta\omega_n}=\arctan\frac{2\zeta\omega_n}{\omega_c} $$
y sustituyendo \( \omega_c \) del Paso 2:
$$ \boxed{\;\mathrm{PM}=\arctan\frac{2\zeta}{\sqrt{\sqrt{1+4\zeta^4}-2\zeta^2}}\;} $$

**Paso 4 — la aproximación lineal.** Para \( \zeta \) pequeño/moderado el radical \( \to1 \) y \( \arctan x\approx x \) (en rad), así que \( \mathrm{PM}\approx\arctan(2\zeta)\approx2\zeta \) rad \( =2\zeta\cdot\frac{180}{\pi}\approx114.6\,\zeta \) grados. Ajustando a la curva exacta en el rango útil \( \zeta\in[0.3,0.7] \) la pendiente baja, y la regla de bolsillo que mejor encaja es
$$ \boxed{\;\mathrm{PM}\,[^\circ]\approx100\,\zeta\;} $$

**Paso 5 — verificación numérica.** Evaluando la fórmula exacta del Paso 3:

| \( \zeta \) | PM exacto | \( 100\zeta \) | sobreoscilación \( M_p \) |
|---|---|---|---|
| 0.30 | 33.3° | 30° | 37% |
| 0.45 | 47.6° | 45° | 21% |
| 0.63 | 61.1° | 63° | 8% |
| 0.70 | 65.2° | 70° | 5% |

La regla \( \mathrm{PM}\approx100\zeta \) acierta a ±3° hasta \( \zeta\approx0.6 \) y se queda algo corta después (conservadora). El \( M_p \) es \( e^{-\pi\zeta/\sqrt{1-\zeta^2}} \): de ahí la guía PM 45°↔20% y PM 65–70°↔apenas sobreoscila.

## 2 — GM exacto para un doble integrador con cero: derivación
Se busca el GM exacto cuando la ganancia de lazo tiene la forma
$$ L(s)=\frac{K(s+z)}{s^2(s+a)} $$
que corresponde al producto de una planta \( G(s)=K/[s(s+a)] \) (doble integrador amortiguado, planta de corriente típica cuando se incluye el polo de la red) con un controlador PI \( C(s)=(s+z)/s \).

**Paso 1 — fase de \( L(j\omega) \).** Escribiendo \( s=j\omega \):
$$ \angle L(j\omega)=\angle(j\omega+z)-2\cdot\angle(j\omega)-\angle(j\omega+a) $$
El término \( j\omega+z \) tiene fase \( +\arctan(\omega/z) \) (contribución positiva del cero del PI); el doble integrador \( (j\omega)^2 \) contribuye \( -180^\circ \) exactos; el polo \( j\omega+a \) contribuye \( -\arctan(\omega/a) \). Por lo tanto:
$$ \angle L(j\omega)=\arctan\frac{\omega}{z}-180^\circ-\arctan\frac{\omega}{a} $$

**Paso 2 — condición de cruce de fase.** El cruce de fase \( \omega_{180} \) es donde \( \angle L=-180^\circ \), es decir:
$$ \arctan\frac{\omega}{z}-\arctan\frac{\omega}{a}=0 $$
La diferencia de arctangentes es cero si y solo si sus argumentos son iguales, o equivalentemente si \( \omega/z=\omega/a \), lo que exigiría \( z=a \). En ese caso el cero del PI cancela exactamente el polo de la planta y el sistema se reduce a un doble integrador puro, cuya fase es \( -180^\circ \) en **todas** las frecuencias: el cruce de fase abarca todo el eje y el GM no está definido de forma única.

Cuando \( z\ne a \) la diferencia \( \arctan(\omega/z)-\arctan(\omega/a) \) es estrictamente positiva para \( z<a \) (el cero es más rápido que el polo) y el sistema **nunca llega a −180°**: el lazo tiene margen de ganancia infinito. Si \( z>a \) (el cero es más lento que el polo, lo que no es el diseño habitual), la diferencia se vuelve negativa a alta frecuencia y aparece un \( \omega_{180} \) finito.

**Paso 3 — caso de interés: \( z>a \) (cero más lento que el polo).** Aplicando la identidad \( \arctan u - \arctan v = \arctan\dfrac{u-v}{1+uv} \) con \( u=\omega/z \) y \( v=\omega/a \):
$$ \arctan\frac{\omega}{z}-\arctan\frac{\omega}{a}=\arctan\frac{\omega/z-\omega/a}{1+\omega^2/(za)}=\arctan\frac{\omega(a-z)}{za+\omega^2} $$
Esto debe ser cero, lo que se cumple solo si el argumento es cero y el numerador es nulo. Para \( \omega>0 \):
$$ \omega(a-z)=0 \;\Rightarrow\; a=z $$
No hay solución con \( \omega>0 \) y \( a\ne z \) a menos que el argumento del arctan no exista como número (denominador cero con numerador no nulo). Esto sucede si \( za+\omega^2=0 \), que no tiene solución real. La conclusión es que **el lazo de un PI sobre \( K/[s(s+a)] \) tiene margen de ganancia infinito siempre que \( z\le a \)**.

**Paso 4 — GM en función de K, a, z.** Para \( z\le a \), el análisis de fase muestra que la fase de \( L \) nunca baja de \( -180^\circ \) y por tanto no hay cruce de fase:
$$ \mathrm{GM}=+\infty \qquad (z\le a) $$
En cambio el margen de fase en \( \omega_c \) vale:
$$ \mathrm{PM}=\arctan\frac{\omega_c}{z}-\arctan\frac{\omega_c}{a} $$
donde \( \omega_c \) se determina numéricamente por \( |L(j\omega_c)|=1 \), es decir
$$ K\frac{\sqrt{\omega_c^2+z^2}}{\omega_c^2\sqrt{\omega_c^2+a^2}}=1 $$
Esta es la condición implícita que fija \( \omega_c \) en función de \( K,z,a \). La ganancia K desplaza \( \omega_c \) pero no crea cruce de fase, de ahí el GM infinito.

**Regla práctica:** en el diseño de un lazo de corriente con PI (que es exactamente esta estructura), el parámetro crítico es el **margen de fase**, no el de ganancia. Subir K mucho acaba haciendo que \( \omega_c \) se acerque a la frecuencia de resonancia del LCL o de otros polos rápidos, donde la fase cae bruscamente. El "GM infinito" del lazo ideal PI–planta se pierde en cuanto aparecen polos adicionales a alta frecuencia.

## 3 — Margen de retardo: derivación y límite digital
### Por qué un retardo solo resta fase
Un retardo puro se expresa como \( e^{-s\tau} \). En el eje de frecuencias \( s=j\omega \):
$$ |e^{-j\omega\tau}|=|e^{j\cdot(-\omega\tau)}|=1 \qquad \text{(módulo exactamente 1)} $$
El módulo es uno porque \( e^{j\theta} \) siempre tiene módulo uno. La fase es:
$$ \angle e^{-j\omega\tau}=-\omega\tau \quad [\mathrm{rad}] $$
La fase decrece linealmente con la frecuencia: a mayor frecuencia, más gira el fasor. En el Bode esto aparece como una curva de fase que cae indefinidamente a la derecha, con pendiente \( -\tau \) rad/(rad/s) sobre una escala lineal de \( \omega \), mientras la magnitud permanece fija en 0 dB.

### Efecto sobre el lazo: cómo se reduce el margen de fase
La ganancia de lazo con retardo es \( L_\tau(j\omega)=L(j\omega)\,e^{-j\omega\tau} \). Separando magnitud y fase:
$$ |L_\tau(j\omega)|=|L(j\omega)|\cdot 1=|L(j\omega)| $$
$$ \angle L_\tau(j\omega)=\angle L(j\omega)-\omega\tau $$
El cruce de ganancia \( \omega_c \) no cambia (porque el módulo no cambia), pero la fase en ese cruce sí:
$$ \mathrm{PM}_\tau=\mathrm{PM}_0-\omega_c\,\tau \quad [\mathrm{rad}] \;=\; \mathrm{PM}_0[\text{°}]-\omega_c\tau\cdot\frac{180}{\pi}[\text{°}] $$
donde \( \mathrm{PM}_0 \) es el PM sin retardo. El margen efectivo se reduce proporcionalmente a \( \omega_c\tau \).

### Retardo total en control digital
En un sistema digital con periodo de muestreo \( T_s \):

| Fuente de retardo | Valor típico |
|---|---|
| Retardo de cómputo (ADC→algoritmo→DAC) | \( \tau_c \approx T_s \) |
| Retardo del modulador PWM (ZOH) | \( \tau_{PWM} \approx 0.5\,T_s \) |
| **Total** | \( \tau_{total} \approx 1.5\,T_s \) |

El retardo de cómputo es \( T_s \) porque el resultado del cálculo se aplica en el siguiente ciclo. El del PWM es \( 0.5\,T_s \) porque el ZOH (Zero-Order Hold) introduce un retardo de medio periodo de muestreo. Ambos se suman:
$$ \tau_{total}\approx1.5\,T_s $$

### Margen de retardo \( \tau_{max} \)
El retardo máximo que el lazo aguanta antes de que PM caiga a cero es:
$$ \tau_{max}=\frac{\mathrm{PM}_0\,[\mathrm{rad}]}{\omega_c} $$
La condición de diseño es \( \tau_{total}\ll\tau_{max} \), con un margen razonable (factor 2–3 de seguridad al menos).

### Ejemplo numérico completo
Datos: \( f_c=\omega_c/(2\pi)=1\,\mathrm{kHz} \), \( \mathrm{PM}_0=60° \), \( T_s=100\,\mu\mathrm{s} \).

**Paso 1 — retardo total:**
$$ \tau_{total}=1.5\times100\,\mu\mathrm{s}=150\,\mu\mathrm{s} $$

**Paso 2 — margen de retardo:**
$$ \tau_{max}=\frac{60°\times\pi/180°}{2\pi\times1000\,\mathrm{Hz}}=\frac{1.047\,\mathrm{rad}}{6283\,\mathrm{rad/s}}\approx167\,\mu\mathrm{s} $$

**Paso 3 — PM efectivo con el retardo real:**
$$ \mathrm{PM}_{ef}=60°-\omega_c\,\tau_{total}\cdot\frac{180°}{\pi}=60°-2\pi\times1000\times150\times10^{-6}\times\frac{180°}{\pi} $$
$$ =60°-0.942\,\mathrm{rad}\times\frac{180°}{\pi}=60°-54°=6° $$
Solo 6° de margen efectivo: el diseño funciona pero es frágil ante cualquier variación. La solución habitual es reducir \( f_c \) a la mitad (o aumentar \( T_s \) a la mitad) o aceptar un \( \mathrm{PM}_0 \) de diseño mayor, por ejemplo 90°, que con el mismo retardo daría:
$$ \mathrm{PM}_{ef}=90°-54°=36° \quad\text{(robusto)} $$

**Regla práctica para control digital:** diseñar \( \omega_c\le0.1\,\omega_s \) (un décimo de la frecuencia de muestreo) para que el retardo de \( 1.5\,T_s \) reste como mucho \( 1.5\times0.1\times2\pi\times\frac{180°}{\pi}\approx54° \). Esto permite destinar la mitad del PM de diseño a combatir el retardo y la otra mitad a robustez real.

## 4 — El margen de módulo \( M_s \): distancia mínima al punto crítico
### La función de sensibilidad y su pico
La función de sensibilidad es
$$ S(j\omega)=\frac{1}{1+L(j\omega)} $$
Su módulo en frecuencia es
$$ |S(j\omega)|=\frac{1}{|1+L(j\omega)|} $$
El denominador \( |1+L(j\omega)| \) es exactamente la **distancia del punto \( L(j\omega) \) al punto \( -1 \)** en el plano complejo. Cuando \( L(j\omega) \) pasa cerca de \( -1 \), el denominador es pequeño y \( |S| \) es grande.

### Definición geométrica de \( M_s \)
El máximo de \( |S| \) sobre todas las frecuencias es
$$ M_s=\max_\omega|S(j\omega)|=\frac{1}{\min_\omega|1+L(j\omega)|}=\frac{1}{d_{min}} $$
donde \( d_{min} \) es la **distancia mínima** de la curva de Nyquist \( L(j\omega) \) al punto crítico \( -1 \). Por tanto:
$$ \boxed{M_s=\frac{1}{d_{min}}, \qquad d_{min}=\frac{1}{M_s}} $$
En el diagrama de Nyquist, la condición \( M_s<2 \) equivale a pedir que la curva de lazo no entre en el disco de radio \( 0.5 \) centrado en \( -1 \).

### Por qué PM y GM solos no son suficientes
PM y GM son medidas en **dos frecuencias específicas** (\( \omega_c \) y \( \omega_{180} \)). Entre esas frecuencias, la curva de Nyquist puede pasar cerca de \( -1 \) sin que ninguno de los dos márgenes lo detecte. Un ejemplo clásico: si \( L(j\omega) \) tiene una "joroba" que se acerca a \( -1 \) a una frecuencia intermedia, PM puede ser 45° y GM puede ser 10 dB, pero \( M_s \) puede ser 3 o más, señalando un sistema realmente poco robusto.

| Condición | PM | GM | \( M_s \) |
|---|---|---|---|
| Robusto | ≥45° | ≥6 dB | <2 |
| Límite | 30–44° | 4–6 dB | 2–2.5 |
| Frágil | <30° | <4 dB | >2.5 |
| Engañoso | 45° | 10 dB | 3 (peligroso) |

El caso "engañoso" es posible cuando la curva de Nyquist bordea \( -1 \) por una región que no corresponde a los dos cruces de eje. **La única métrica completa de robustez es \( M_s \).**

### Objetivos de diseño y círculo de Nyquist
El objetivo \( M_s<2 \) dibuja un círculo prohibido de radio \( 1/2=0.5 \) centrado en \( -1 \) en el plano de Nyquist. La curva \( L(j\omega) \) no debe entrar en ese círculo. El punto de máxima aproximación a \( -1 \) es donde \( |S| \) alcanza su pico; allí la curva de lazo es tangente al círculo.

La conexión con la respuesta temporal es directa: \( M_s \) es el pico de la función de sensibilidad, que amplifica las perturbaciones a esa frecuencia. Un \( M_s=2 \) significa que el lazo amplifica perturbaciones a esa frecuencia por un factor 2 (6 dB) antes de rechazarlas. Un \( M_s>3 \) suele producir transitorios oscilantes incluso cuando PM y GM parecen razonables.

## 5 — Sistema condicionalmente estable: cuándo falla el criterio simple
### Definición
Un sistema **condicionalmente estable** es aquel que es estable para un rango de ganancia \( K\in(K_{min},K_{max}) \), pero inestable si la ganancia **baja** de \( K_{min} \) o **sube** de \( K_{max} \). El criterio simple "PM>0 y GM>0 implica estabilidad" asume que el sistema es estable en lazo abierto y que la curva de Nyquist rodea \( -1 \) como mucho de una forma sencilla. Esto falla en la estabilidad condicional.

### Ejemplo: planta con fase que baja y sube
Considérese
$$ L(s)=\frac{K(s+1)^2}{s(s+0.01)^2(s+100)} $$
El cero doble en \( s=-1 \) produce una subida de fase (+180° en total) en la región intermedia. A bajas frecuencias la fase parte de \( -90° \) (polo simple en el origen); los dos polos en \( -0.01 \) la llevan hacia \( -270° \); los dos ceros en \( -1 \) la suben de vuelta hacia \( -90° \); el polo en \( -100 \) la lleva a \( -180° \) a alta frecuencia.

Esta variación hace que la curva de magnitud de \( |L(j\omega)| \) cruce 0 dB en **dos frecuencias**: \( \omega_{c1} \) (cruce inferior) y \( \omega_{c2} \) (cruce superior).

| Cruce | Frecuencia | Fase | PM |
|---|---|---|---|
| Inferior (\( \omega_{c1} \)) | baja (≈0.3 rad/s) | ~−120° | +60° (estable) |
| Superior (\( \omega_{c2} \)) | alta (≈3 rad/s) | ~−220° | −40° (inestable) |

El criterio simple no puede decidir: hay un PM positivo en un cruce y negativo en otro. La respuesta correcta viene del **criterio de Nyquist completo**: hay que contar cuántas veces la curva de Nyquist rodea \( -1 \) teniendo en cuenta la dirección.

### Por qué la reducción de ganancia puede inestabilizar
Si se baja K (por ejemplo por una caída de tensión de bus, una variación paramétrica o el arranque del convertidor), el Bode de magnitud desciende y \( \omega_{c1} \) desaparece, dejando solo \( \omega_{c2} \) con PM negativo. El sistema se vuelve inestable a **ganancia baja**, lo contrario del comportamiento habitual.

Este escenario aparece en la práctica en:
- Compensadores de adelanto muy agresivos (fase grande a frecuencias intermedias)
- Lazos de potencia con filtros resonantes (múltiples cruces)
- Compensadores de doble adelanto (dos ceros antes de dos polos)

**Regla:** ante cualquier sospecha de múltiples cruces de ganancia o comportamiento no estándar de la fase, usar el criterio de Nyquist completo y calcular \( M_s \) sobre todo el eje de frecuencias.

## 6 — Diseño iterativo: especificación → margen → planta → iteración
### Especificaciones de partida
Se diseña el lazo de corriente de un convertidor con los siguientes requisitos:

| Especificación | Objetivo |
|---|---|
| Margen de fase | PM ≥ 45° |
| Margen de ganancia | GM ≥ 6 dB |
| Margen de módulo | \( M_s < 2 \) |
| Ancho de banda | BW > 100 Hz (−3 dB en lazo cerrado) |
| Sobreoscilación | < 10% |
| Retardo digital | \( T_s=100\,\mu\mathrm{s} \) |

Planta: \( G(s)=\dfrac{1000}{s(s/1000+1)} \) (lazo de corriente con inductancia y polo del filtro).

### Iteración 1: PI simple \( C_1(s)=(1+\omega_z/s) \) con \( \omega_z=200 \)
La ganancia de lazo queda:
$$ L_1(s)=C_1(s)G(s)=\frac{K_1(s+200)}{s^2(s/1000+1)} $$
Eligiendo \( K_1=5 \) para situar \( \omega_c\approx2\pi\times120\approx754\,\mathrm{rad/s} \), la fase en el cruce resulta:
$$ \angle L_1(j\omega_c)=-180°+\arctan\frac{\omega_c}{200}-\arctan\frac{\omega_c}{1000}\approx-180°+75°-37°=-142° $$
$$ \mathrm{PM}_1=180°+(-142°)=38° \quad\Rightarrow\quad \text{insuficiente (objetivo 45°)} $$

### Iteración 2: añadir compensador de adelanto de fase
Un compensador de adelanto \( C_{lead}(s)=\alpha\,\dfrac{s/\omega_z+1}{s/\omega_p+1} \), con \( \omega_z<\omega_p \), aporta fase positiva máxima:
$$ \phi_{max}=\arcsin\frac{\alpha-1}{\alpha+1}, \qquad \alpha=\frac{\omega_p}{\omega_z} $$
Para conseguir \( +15° \) adicionales: \( \sin\phi_{max}=\sin15°=0.259 \), por lo que:
$$ \alpha=\frac{1+\sin15°}{1-\sin15°}=\frac{1.259}{0.741}=1.70 $$
Se elige \( \omega_z=500\,\mathrm{rad/s} \), \( \omega_p=850\,\mathrm{rad/s} \), que sitúa el pico de fase en \( \omega_{peak}=\sqrt{\omega_z\omega_p}=652\,\mathrm{rad/s}\approx\omega_c \). La nueva ganancia de lazo:
$$ L_2(s)=C_1(s)\cdot C_{lead}(s)\cdot G(s) $$
La evaluación numérica da \( \mathrm{PM}_2\approx45° \) ✓, aunque el cruce de ganancia sube ligeramente a \( \omega_c\approx820\,\mathrm{rad/s} \) por la ganancia que añade el adelanto.

### Iteración 2: verificar \( M_s \)
Con \( \omega_c=820\,\mathrm{rad/s} \), calcular \( S(j\omega)=1/(1+L_2(j\omega)) \) sobre la malla de frecuencias. Resultado:
$$ M_s=\max_\omega|S(j\omega)|\approx1.8 \quad\Rightarrow\quad M_s<2 \;\checkmark $$

### Iteración 2: verificar margen de retardo
$$ \tau_{max}=\frac{45°\times\pi/180°}{820\,\mathrm{rad/s}}=\frac{0.785}{820}\approx957\,\mu\mathrm{s} $$
$$ \tau_{total}=1.5\times T_s=150\,\mu\mathrm{s} $$
$$ \mathrm{PM}_{ef}=45°-820\times150\times10^{-6}\times\frac{180°}{\pi}=45°-7°=38° \quad\Rightarrow\quad\text{aceptable} $$

### Tabla resumen de iteraciones

| Iteración | Controlador | \( \omega_c \) [rad/s] | PM | GM | \( M_s \) | PM efectivo | Estado |
|---|---|---|---|---|---|---|---|
| 1 | PI simple | 754 | 38° | ∞ | 2.1 | 31° | ✗ PM bajo |
| 2 | PI + adelanto | 820 | 45° | ∞ | 1.8 | 38° | ✓ |

La iteración termina cuando todas las especificaciones se cumplen simultáneamente, incluyendo el PM efectivo con el retardo digital. Si \( M_s \) fuera alto, la siguiente acción sería reducir \( \omega_c \) (sacrificando BW) o rediseñar el adelanto con menos agresividad.

## 7 — Márgenes en sistemas MIMO: el Nyquist generalizado
### Por qué los márgenes escalares no son suficientes en MIMO
Un convertidor trifásico controlado en el marco \( dq \) es un sistema de dos entradas y dos salidas: las consignas de corriente \( i_d^* \) e \( i_q^* \) son las entradas, y las corrientes medidas \( i_d \), \( i_q \) son las salidas. El controlador y la planta son **matrices de funciones de transferencia**. En ese caso la ganancia de lazo no es un escalar sino una matriz:
$$ \mathbf{L}(s)=\mathbf{C}(s)\,\mathbf{G}(s) \in \mathbb{C}^{2\times2} $$
La condición \( \det(\mathbf{I}+\mathbf{L}(j\omega))=0 \) (el equivalente de \( 1+L=0 \)) ya no se puede leer como la proximidad de un punto a \( -1 \); depende de **cómo interactúan** los dos canales.

### El criterio de Nyquist generalizado
El criterio de estabilidad se generaliza de la siguiente forma. Sea \( \lambda_i(\mathbf{L}(j\omega)) \) el \( i \)-ésimo autovalor de la matriz de ganancia de lazo evaluada en frecuencia. El lazo cerrado es estable si y solo si la curva de Nyquist de **cada autovalor** no rodea el punto \( -1 \) (contando las inestabilidades de lazo abierto según el criterio de Nyquist estándar). En la práctica:

1. Calcular \( \lambda_1(j\omega) \) y \( \lambda_2(j\omega) \) para \( \omega \in [0,\infty) \).
2. Dibujar ambas curvas en el plano complejo (las "curvas de Nyquist de los autovalores").
3. Verificar que ninguna rodea \( -1 \).

### La \( \gamma \)-stability margin
El análogo a \( M_s \) en MIMO es la \( \gamma \)-margin (o margen de estabilidad por autovalores):
$$ \gamma=\min_{i,\omega}\left|1+\lambda_i(\mathbf{L}(j\omega))\right| $$
Es la distancia mínima de **cualquier** autovalor de \( \mathbf{L}(j\omega) \) al punto crítico \( -1 \). El margen de módulo MIMO es \( M_s^{MIMO}=1/\gamma \), y el objetivo de diseño es \( M_s^{MIMO}<2 \), igual que en el caso escalar.

### Conexión con la impedancia: lazo de corriente dq
En el análisis de estabilidad por impedancia de un sistema convertidor-red, la matriz de ganancia de lazo tiene la forma:
$$ \mathbf{L}(j\omega)=\mathbf{Z}_{red}(j\omega)\,\mathbf{Y}_{conv}(j\omega) $$
donde \( \mathbf{Z}_{red} \) es la impedancia de la red (incluyendo el transformador y la impedancia del cable) y \( \mathbf{Y}_{conv} \) es la admitancia de salida del convertidor. Ambas son matrices \( 2\times2 \) en el marco \( dq \) porque los términos de acoplamiento cruzado (\( L\omega \) en el filtro, el PLL en el GFL) crean efectos fuera de diagonal. El criterio de Nyquist generalizado sobre \( \mathbf{L} \) es entonces **el criterio de estabilidad por impedancia** exacto para sistemas trifásicos balanceados en marco \( dq \).

Para un GFM en red fuerte, \( \mathbf{Z}_{red} \) es pequeña y los autovalores de \( \mathbf{L} \) tienen módulo mucho menor que 1 en todas las frecuencias: el sistema está lejos de la inestabilidad. En red débil (SCR bajo), \( \mathbf{Z}_{red} \) crece y los autovalores de \( \mathbf{L} \) pueden acercarse a \( -1 \) en el rango de frecuencias del PLL o del lazo de potencia, señalando la inestabilidad.

Ver [[impedancia-salida-estabilidad]] para la derivación completa de \( \mathbf{Z}_{red} \) y \( \mathbf{Y}_{conv} \), y la aplicación al proyecto GFL (Fase 3).

## Cuándo y por qué se usa
Tras comprobar la estabilidad nominal: los márgenes dicen si el diseño aguanta variaciones de planta, retardos y errores de modelo. Es el chequeo imprescindible antes de validar en hardware. En problemas de interacción convertidor-red el equivalente es el criterio de impedancia / Nyquist generalizado (ver [[impedancia-salida-estabilidad]]).

## Procedimiento (genérico)
1. Calcula \( L(j\omega)=C(j\omega)G(j\omega) \) (o el minor loop gain en impedancia).
2. Lee PM y GM en los cruces (o con `control.margin`); calcula \( M_s \) como el pico de \( |S| \).
3. Comprueba contra objetivos: PM 45–60°, GM > 6 dB, \( M_s<2 \).
4. Convierte PM a margen de retardo \( \tau_{max}=\mathrm{PM}/\omega_c \) y compáralo con el retardo real (\( \approx1.5\,T_s \)).
5. Si hay múltiples cruces de ganancia o fase no monótona: usar Nyquist completo y calcular \( M_s \) para todas las frecuencias.
6. En sistemas MIMO: calcular autovalores de \( \mathbf{L}(j\omega) \) y la \( \gamma \)-margin.

## Ejemplo de código
```python
import control as ct
import numpy as np

gm, pm, wcg, wcp = ct.margin(L)          # GM, PM y sus frecuencias de cruce
S  = 1/(1+L)                              # sensibilidad
w  = np.logspace(0, 5, 5000)
_, S_mag = ct.frequency_response(S, w)
Ms = np.max(np.abs(S_mag))               # pico de |S| ; margen de modulo = 1/Ms
tau_max = (pm*np.pi/180)/wcp             # margen de retardo (PM en rad / wc)
tau_digital = 1.5 / fs                   # fs = frecuencia de muestreo
pm_efectivo = pm - wcp * tau_digital * 180/np.pi

print(f"PM={pm:.1f}°  GM={20*np.log10(gm):.1f}dB  Ms={Ms:.2f}")
print(f"tau_max={tau_max*1e6:.0f}µs  tau_digital={tau_digital*1e6:.0f}µs")
print(f"PM efectivo={pm_efectivo:.1f}°")
```

## Parámetros y valores típicos
PM 45–60°, GM > 6 dB, \( M_s<2 \). Margen de retardo > varios periodos de muestreo. Como guía: PM≈70° apenas sobreoscila; PM≈45° sobreoscila ≈20–25%; PM<30° ya es poco robusto. En control digital con \( T_s \) y cruce en \( \omega_c \), diseñar con \( \omega_c<0.1\,\omega_s \) para que el retardo de \( 1.5\,T_s \) no consuma más de la mitad del PM de diseño.

## Límites del criterio de Bode (cuándo NO basta)
El criterio simple "PM>0 y GM>0 ⇒ estable" vale para lazo abierto estable y de fase mínima con un único cruce de ganancia. Falla en:
- **Sistemas condicionalmente estables**: la magnitud cruza 0 dB varias veces y subir o bajar la ganancia puede inestabilizar. Hay que mirar todos los cruces.
- **Planta inestable en lazo abierto o de fase no mínima** (ceros en el semiplano derecho, retardos grandes): el conteo de fase engaña.
- **Sistemas MIMO / acoplados** (lazo de corriente dq, interacción convertidor-red): se usa el [[criterio-nyquist|Nyquist]] (o el generalizado) sobre \( \mathbf{L}(j\omega) \), que es el criterio exacto del que los márgenes son la versión rápida.

## Errores comunes
- Mirar solo PM/GM: pueden ser buenos y aun tener \( M_s \) alto (poco robusto). Usar \( M_s \).
- Olvidar el retardo de cómputo/PWM al evaluar el margen real (el PM efectivo puede ser 15–20° menor que el de diseño).
- Aplicar el criterio simple a un sistema condicionalmente estable o de fase no mínima.
- Confundir el cruce de ganancia (\( |L|=1 \)) con el de fase (\( -180^\circ \)): PM va en el primero, GM en el segundo.
- En MIMO: calcular PM/GM canal a canal (como si fueran dos lazos independientes) e ignorar el acoplamiento: el \( \gamma \)-margin puede ser mucho peor que los márgenes diagonales.

## Uso en proyectos
- **01 (GFM)**: el lazo de potencia tenía **margen de fase −86°** (inestable) — eso reveló la causa y guió la cura (impedancia virtual). El criterio de impedancia (Fase 3) es el Nyquist generalizado equivalente.
- **02 (GFL)**: el PLL en red débil (SCR<2) hacía que el lazo de corriente viera una planta con cero en el semiplano derecho → fase no mínima → el criterio simple fallaba; hubo que usar Nyquist completo sobre la \( \mathbf{L} \) de impedancia.

## Conceptos relacionados
- [[diagrama-bode]] · [[criterio-nyquist]] · [[funciones-sensibilidad]] · [[loop-shaping]] · [[robustez-parametrica]] · [[impedancia-salida-estabilidad]]

## Referencias
- Aström, Murray, *Feedback Systems*, 2008.
- Franklin, Powell, Emami-Naeini, *Feedback Control of Dynamic Systems*.
- Skogestad, Postlethwaite, *Multivariable Feedback Design*, Wiley 2005.
- Middleton, Goodwin, *Digital Control and Estimation*, Prentice Hall 1990.
