---
titulo: Compensador de adelanto-atraso (lead-lag)
slug: compensador-adelanto-atraso
categoria: control
tipo: tecnica
nivel: intermedio
proyectos: []
objetivos: [moldear fase y ganancia del lazo para fijar margen y ancho de banda]
tags: [lead-lag, adelanto, atraso, compensador, frecuencia, intermedio, control]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-30
relacionados: [loop-shaping, lugar-raices, diagrama-bode, margenes-estabilidad, controlador-pid]
referencias:
  - "Ogata, Ingeniería de Control Moderna, Pearson"
  - "Franklin, Powell, Feedback Control of Dynamic Systems, Pearson"
---

## Definición
Compensador clásico de primer orden que **aporta fase** (adelanto) o **reduce ganancia en alta
frecuencia / mejora la de baja** (atraso) para moldear la respuesta en frecuencia del lazo. Es la
versión analógica/continua del moldeo que en digital harías con un PID filtrado.

## Fundamento teórico
**Adelanto (lead)** \( (\alpha>1) \):
$$ C(s)=K_c\,\frac{1+\alpha T s}{1+T s},\qquad
   \phi_{max}=\arcsin\frac{\alpha-1}{\alpha+1}\ \text{ en }\ \omega_m=\frac{1}{T\sqrt{\alpha}} $$
Aporta hasta \( \phi_{max} \) de fase (≈55–65° por etapa con \( \alpha\le10 \)) cerca del cruce de
ganancia → **sube el margen de fase y el ancho de banda**; eleva la ganancia en alta (más rápido,
pero más ruido). Es análogo a un PD filtrado.

**Atraso (lag)** \( (\alpha<1) \): misma forma; añade ganancia en baja frecuencia
(**reduce el error en régimen permanente**) y atenúa en alta, a costa de un poco de fase negativa
que se coloca lejos del cruce. Análogo a un PI aproximado.

**Lead-lag** combina ambos: el lag mejora el error estacionario y el lead recupera el margen y la
velocidad.

<div class="cfig"><img src="figuras/compensador-adelanto-atraso-bode.png" alt="Bode de un compensador de adelanto"><div class="cap">El compensador de adelanto inyecta un máximo de fase φmax en ωm=1/(T√α); colocándolo en el cruce de ganancia sube el margen de fase, a costa de más ganancia (y ruido) en alta frecuencia.</div></div>

## 1 — De dónde sale \( \phi_{max} \) y la frecuencia \( \omega_m \) donde ocurre
**Paso 1 — la fase del lead.** El compensador de adelanto \( C(s)=K_c\dfrac{1+\alpha Ts}{1+Ts} \) (con \( \alpha>1 \)) tiene un cero en \( \omega_z=1/(\alpha T) \) y un polo en \( \omega_p=1/T \), con \( \omega_z<\omega_p \). Su fase en \( s=j\omega \) es la del cero menos la del polo:

$$ \phi(\omega)=\arctan(\alpha T\omega)-\arctan(T\omega) $$

**Paso 2 — maximizar: derivar e igualar a cero.** Usando \( \dfrac{d}{d\omega}\arctan(a\omega)=\dfrac{a}{1+a^2\omega^2} \):

$$ \frac{d\phi}{d\omega}=\frac{\alpha T}{1+(\alpha T\omega)^2}-\frac{T}{1+(T\omega)^2}=0 $$

Multiplicando en cruz: \( \alpha T\,[1+(T\omega)^2]=T\,[1+(\alpha T\omega)^2] \). Dividiendo por \( T \) y reordenando:

$$ \alpha+\alpha T^2\omega^2=1+\alpha^2T^2\omega^2 \;\Rightarrow\; \alpha-1=\alpha T^2\omega^2(\alpha-1) \;\Rightarrow\; \omega^2=\frac{1}{\alpha T^2} $$

$$ \boxed{\;\omega_m=\frac{1}{T\sqrt{\alpha}}\;} $$

Es la **media geométrica** del cero y el polo: \( \omega_m=\sqrt{\omega_z\,\omega_p}=\sqrt{\tfrac{1}{\alpha T}\cdot\tfrac{1}{T}} \). En escala logarítmica (Bode), justo el punto medio entre cero y polo.

**Paso 3 — evaluar la fase en \( \omega_m \).** Sustituyendo \( \omega_m \), con \( \alpha T\omega_m=\sqrt{\alpha} \) y \( T\omega_m=1/\sqrt{\alpha} \):

$$ \phi_{max}=\arctan\sqrt{\alpha}-\arctan\frac{1}{\sqrt{\alpha}} $$

**Paso 4 — cerrar en forma de arcoseno.** Aplicando \( \tan(\phi_{max})=\dfrac{\sqrt\alpha-1/\sqrt\alpha}{1+\sqrt\alpha\cdot(1/\sqrt\alpha)}=\dfrac{\alpha-1}{2\sqrt\alpha} \) (resta de arcotangentes). De ahí, construyendo el triángulo (\( \text{op}=\alpha-1 \), \( \text{ady}=2\sqrt\alpha \), \( \text{hip}=\sqrt{(\alpha-1)^2+4\alpha}=\alpha+1 \)):

$$ \boxed{\;\sin\phi_{max}=\frac{\alpha-1}{\alpha+1}\quad\Longleftrightarrow\quad \alpha=\frac{1+\sin\phi_{max}}{1-\sin\phi_{max}}\;} $$

Esta última forma es la de diseño: fijado el \( \phi_{max} \) que falta para el margen, da \( \alpha \) directamente. Con \( \alpha\le10 \), \( \phi_{max}\lesssim55^\circ \) por etapa.

## 2 — El ejemplo numérico, paso a paso, y la corrección de \( K_c \)
**Paso 1 — fase a aportar.** Margen actual 22°, objetivo 45°; faltan 23°, más 5° de colchón (porque el propio lead mueve algo el cruce) → \( \phi_{max}=28^\circ \).

**Paso 2 — factor \( \alpha \).** \( \alpha=\dfrac{1+\sin28^\circ}{1-\sin28^\circ}=\dfrac{1+0.469}{1-0.469}=2.77 \).

**Paso 3 — constante de tiempo.** Para que el máximo de fase caiga en el cruce, \( \omega_m=\omega_c=200\,\text{rad/s} \):

$$ T=\frac{1}{\omega_c\sqrt{\alpha}}=\frac{1}{200\times1.664}=3.0\times10^{-3}\,\text{s},\qquad \alpha T=8.3\times10^{-3}\,\text{s} $$

$$ C(s)=\frac{1+8.3\times10^{-3}s}{1+3.0\times10^{-3}s} $$

**Paso 4 — corregir \( K_c \).** El lead no es transparente en ganancia: en \( \omega_m \) su módulo es

$$ |C(j\omega_m)|=\sqrt{\alpha}=1.66\;(+4.4\,\text{dB}) $$

Ese +4.4 dB **adelantaría el cruce** a una frecuencia mayor (donde la fase aportada ya no es el máximo). Para mantener el cruce en \( \omega_c \) se baja \( K_c \) en \( 1/\sqrt\alpha \). Resultado: margen \( \approx22^\circ+28^\circ=50^\circ \) ✓ (los 5° de colchón cubren el pequeño residuo del reescalado). Si hicieran falta \( \alpha>10 \), el \( \sqrt\alpha \) de ganancia amplificaría demasiado el ruido de alta frecuencia: se encadenan dos etapas de menos \( \alpha \) cada una.

## Cuándo y por qué se usa
Cuando un P/PI no basta para cumplir simultáneamente margen, ancho de banda y error, o cuando se
prefiere un compensador propio (sin el polo en el origen del integrador) y bien condicionado para
discretizar. Encaja con el enfoque de [[loop-shaping]] y se diseña sobre [[diagrama-bode]] o
[[lugar-raices]].

## Procedimiento de diseño (genérico)
1. Fija especificaciones: margen de fase y \( \omega_c \) objetivo (de las [[especificaciones-control]]).
2. Evalúa la fase que falta en \( \omega_c \) → fase a aportar por el **lead** (margen extra 5–10°).
3. Calcula \( \alpha=\dfrac{1+\sin\phi_{max}}{1-\sin\phi_{max}} \) y \( T=\dfrac{1}{\omega_c\sqrt\alpha} \).
4. Ajusta \( K_c \) para que el cruce caiga en \( \omega_c \).
5. Si falla el error estacionario, añade una etapa **lag** en baja frecuencia.
6. Verifica márgenes ([[margenes-estabilidad]]) y discretiza ([[discretizacion-controladores]]).

## Ejemplo de aplicación real
**Problema:** Lazo de posición de un accionamiento con margen de fase de 22° (objetivo 45°). Diseñar un compensador de adelanto de una etapa que aporte los 23° necesarios sin degradar el cruce.

Fase a aportar con 5° de margen extra: \( \phi_{max}=28° \). Factor: \( \alpha=(1+\sin28°)/(1-\sin28°)\approx2.77 \). Constante de tiempo: \( T=1/(\omega_c\sqrt{\alpha})=1/(200\times1.66)=3.0\,\text{ms} \). Compensador: \( C(s)=(1+\alpha T s)/(1+Ts)=(1+8.3\times10^{-3}s)/(1+3.0\times10^{-3}s) \). A \( \omega_c=200\,\text{rad/s} \), la ganancia del compensador es \( \sqrt{\alpha}\approx1.66 \) (+4.4 dB): reducir \( K_c \) en esa proporción para mantener el cruce en \( \omega_c \). Resultado final: margen de fase \( \approx22+28=50° \) ✓. Si \( \alpha>10 \) la amplificación de ruido sería inaceptable: encadenar dos etapas en lugar de una.

## Ejemplo de código
```python
import control as ct, numpy as np
phi = np.deg2rad(50); wc = 200.0
alpha = (1+np.sin(phi))/(1-np.sin(phi)); T = 1/(wc*np.sqrt(alpha))
lead = ct.tf([alpha*T, 1], [T, 1])      # 1 etapa de adelanto
```

## Parámetros y valores típicos
Por etapa de adelanto: \( \alpha \le 10 \) (\( \phi_{max}\lesssim 55^\circ \)); para más fase,
**encadena** etapas. La separación lead/lag suele ser de una década respecto a \( \omega_c \).

## Errores comunes
- Pedir demasiada fase a una sola etapa (\( \alpha \) enorme) → amplifica ruido en alta frecuencia.
- Colocar el cero/polo del lag cerca de \( \omega_c \) → resta fase donde más duele.
- Olvidar reescalar \( K_c \) tras añadir el compensador (el cruce se mueve).

## 4 — Diseño paso a paso del compensador de adelanto

**Paso 1 — calcular la fase adicional necesaria.** Evaluar el margen de fase actual a la frecuencia de cruce deseada \( \omega_c^* \); la fase a aportar es:
$$ \phi_{max} = PM_{deseado} - PM_{actual} + 5° $$
El margen extra de 5° compensa la ligera caída de fase producida al reescalar la ganancia tras el compensador.

**Paso 2 — calcular el factor \( \alpha \).** La relación polo-cero del compensador:
$$ \alpha = \frac{p}{z} = \frac{1+\sin\phi_{max}}{1-\sin\phi_{max}} $$
El máximo aporte de fase del compensador ocurre en \( \omega_{max}=\sqrt{zp} \).

**Paso 3 — ubicar \( \omega_{max} \) en la nueva frecuencia de cruce.** Para que el máximo aporte de fase coincida con el nuevo cruce: \( \omega_{max} = \omega_c^* \). Entonces \( T = 1/(\omega_c^*\sqrt{\alpha}) \), y el compensador es \( C(s) = (\alpha T s + 1)/(Ts + 1) \).

**Paso 4 — reescalar la ganancia.** El compensador aporta \( +\sqrt{\alpha} \) de ganancia en \( \omega_{max} \), lo que desplaza el cruce. Reducir \( K_c \) en \( 1/\sqrt{\alpha} \) restaura el cruce en \( \omega_c^* \). Resultado: el PM real es aproximadamente \( PM_{actual} + \phi_{max} \).

## 5 — Compensador de atraso: reducción del error en régimen

El compensador de atraso coloca un cero-polo por debajo de \( \omega_c \) con \( z > p \):
$$ C_{lag}(s) = \frac{s/z + 1}{s/p + 1}, \quad z, p \ll \omega_c \quad (\text{factor 10 mínimo}) $$

La ganancia DC del compensador es \( K_{dc} = z/p > 1 \), que aumenta el coeficiente de error de posición \( K_v \) en ese mismo factor, reduciendo el error en régimen permanente. Como la fase del compensador en \( \omega_c \) es pequeña y negativa (la fase de atraso a esa frecuencia es \( \approx-5° \)), el PM se reduce ligeramente. Para compensarlo se aumenta la ganancia \( K_c \) marginalmente.

**Diseño rápido:** elegir \( p = \omega_c/10 \) y \( z = K_{dc} \cdot p \); ajustar \( K_{dc} \) según la reducción de error deseada.

## 6 — Aplicación: lazo de tensión del inversor

El lazo de tensión de un inversor con filtro LC tiene como planta aproximada el condensador de filtro:
$$ G_v(s) \approx \frac{1}{C_f s} \quad \text{(integradora)} $$

Un controlador PI actúa como compensador de atraso puro con cero en \( s = -1/T_i \):
$$ C_v(s) = K_p\!\left(1 + \frac{1}{T_i s}\right) = K_p\,\frac{T_i s + 1}{T_i s} $$

**Criterio de separación de escalas:** el lazo de tensión debe ser unas 10 veces más lento que el lazo de corriente interno: \( \omega_{cv} \approx \omega_{ci}/10 \). Esta separación garantiza que cuando el lazo de tensión genera \( i^* \), el lazo de corriente ya está en régimen y la corriente sigue fielmente la referencia.

**Verificación:** PM > 45° en el lazo de tensión; \( t_s < 20\,\text{ms} \) ante perturbación de carga; ausencia de sobreoscilación de tensión superior al 5 % ante un escalón de carga del 100 %.

<div class="cfig"><img src="../figuras/compensador-adelanto-atraso-analisis.png" alt="Compensador adelanto-atraso: Bode, ratio alfa, efecto del escalón y margen de fase vs Kp"><div class="cap">Superior izquierdo: Bode del compensador de adelanto (fase positiva en la banda media) y de atraso (fase negativa, ganancia DC > 1). Superior derecho: ratio α en función del adelanto de fase máximo — α crece exponencialmente con φ_max. Inferior izquierdo: respuesta al escalón con y sin compensador de adelanto — el mayor PM produce menor sobreoscilación. Inferior derecho: margen de fase aproximado en función de Kp — la zona verde es la región de diseño válida.</div></div>

## Conceptos relacionados
- [[loop-shaping]] · [[lugar-raices]] · [[diagrama-bode]] · [[margenes-estabilidad]] · [[controlador-pid]]

## Referencias
- Ogata, *Ingeniería de Control Moderna*.
- Franklin, Powell, *Feedback Control of Dynamic Systems*.
