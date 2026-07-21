---
titulo: Óptimo simétrico (sintonía PI para plantas con integrador)
slug: optimo-simetrico
categoria: metodologia
tipo: metodo
nivel: intermedio
proyectos: []
objetivos: [sintonizar un PI sobre una planta con integrador colocando el cero simetricamente respecto al cruce, maximizar el margen de fase de un doble integrador]
tags: [optimo-simetrico, symmetric-optimum, kessler, sintonia, PI, integrador, margen-fase, bus-dc, modulo-optimo, doble-integrador]
fecha_creacion: 2026-07-14
fecha_actualizacion: 2026-07-14
relacionados: [sintonia-pi-pid, margenes-estabilidad, control-tension-bus-dc, convertidor-back-to-back, loop-shaping, controlador-pid, diagrama-bode]
referencias:
  - "Kessler, Das symmetrische Optimum, Regelungstechnik 1958"
  - "Åström, Hägglund, Advanced PID Control, ISA 2006"
  - "Leonhard, Control of Electrical Drives, Springer 2001"
---

## Definición
El **óptimo simétrico** (*symmetric optimum*, Kessler 1958) es un método de sintonía de un PI para plantas
que contienen un **integrador** más un retardo pequeño. Coloca el **cero del PI** y el **polo de la planta**
de forma **simétrica** respecto a la frecuencia de cruce \(\omega_c\) en escala logarítmica (\(\omega_c\) es
su media geométrica). Con esa colocación, la fase de la ganancia de lazo alcanza su **máximo** justo en
\(\omega_c\), es decir, se obtiene el **máximo margen de fase** posible para esa estructura.

## Fundamento teórico
La planta típica es un **integrador con un retardo pequeño equivalente** \(T_\Sigma\) (suma de retardos
rápidos: muestreo, PWM, lazo interno de corriente, filtros):

$$ G(s) = \frac{K_s}{s\,(1+sT_\Sigma)} $$

El integrador \(1/s\) aporta \(-90°\) fijos. Un PI añade **otro** integrador (\(1/s\) del término integral),
así que la ganancia de lazo tiene un **doble integrador** \(\to -180°\) a baja frecuencia. Sin ayuda, el
margen de fase sería nulo (inestable). El **cero del PI** es el que levanta la fase; la cuestión es **dónde
colocarlo**. El óptimo simétrico lo sitúa de forma que la fase suba lo máximo posible en el cruce.

<div class="cfig"><img src="figuras/optimo-simetrico-bode.png" alt="Bode de la ganancia de lazo del óptimo simétrico: la magnitud cruza 0 dB en omega_c y la fase forma una campana que alcanza su máximo justo en omega_c, con margen de fase arctan(a)-arctan(1/a)"><div class="cap">Ganancia de lazo del óptimo simétrico (\(a=3\)). La magnitud pasa de \(-40\) a \(-20\) dB/dec al cruzar el cero del PI \(1/T_i\), y vuelve a \(-40\) dB/dec en el polo de la planta \(1/T_\Sigma\); cruza 0 dB en \(\omega_c\). La fase forma una **campana** cuyo máximo cae exactamente en \(\omega_c\) = media geométrica de \(1/T_i\) y \(1/T_\Sigma\): ahí el margen de fase es \(\arctan a - \arctan(1/a)\).</div></div>

## 1 — Por qué no vale la cancelación de polo (módulo óptimo)
En una planta **sin** integrador (un polo estable \(1/(1+s\tau)\)), la sintonía habitual es cancelar el polo
con el cero del PI (\(T_i = \tau\)), dejando un integrador puro y \(PM=90°\) ([[sintonia-pi-pid]], IMC). Aquí
**no se puede**: el polo de la planta está en \(s=0\) (integrador) y no tiene sentido cancelarlo con el cero
del PI (perderías la acción integral y no rechazarías perturbaciones en continua). Por eso, para plantas con
integrador, se recurre al óptimo simétrico: en vez de cancelar, **coloca** el cero para maximizar la fase.

## 2 — Derivación de la sintonía (paso a paso)

**Paso 1 — Estructura.** PI y ganancia de lazo:

$$ C(s) = K_p\frac{1+sT_i}{sT_i}, \qquad L(s) = C(s)G(s) = K_p K_s\frac{1+sT_i}{s^2\,T_i\,(1+sT_\Sigma)} $$

**Paso 2 — La idea de simetría.** Se introduce un factor \(a>1\) y se sitúa el cruce como **media geométrica**
de las dos frecuencias de esquina, el cero \(1/T_i\) y el polo \(1/T_\Sigma\):

$$ \frac{1}{T_i} = \frac{\omega_c}{a}, \qquad \frac{1}{T_\Sigma} = a\,\omega_c
   \quad\Longrightarrow\quad \omega_c = \sqrt{\frac{1}{T_i}\cdot\frac{1}{T_\Sigma}} $$

En escala log, \(\log\omega_c\) es el punto medio entre \(\log(1/T_i)\) y \(\log(1/T_\Sigma)\): de ahí el
nombre **simétrico**.

**Paso 3 — Tiempo integral.** De \(1/T_\Sigma = a\omega_c\) sale \(\omega_c = 1/(aT_\Sigma)\); sustituyendo en
\(1/T_i = \omega_c/a\):

$$ \boxed{T_i = a^2\,T_\Sigma} $$

**Paso 4 — Ganancia proporcional desde \(|L(j\omega_c)|=1\).** Primero el módulo, factor a factor
(el módulo de un producto/cociente es el producto/cociente de módulos): un complejo \(1+j\omega T\) tiene
módulo \(\sqrt{1+(\omega T)^2}\), y \((j\omega)^2=-\omega^2\) tiene módulo \(\omega^2\):

$$ |L(j\omega)| = K_p K_s\cdot\frac{\overbrace{\sqrt{1+(\omega T_i)^2}}^{|1+j\omega T_i|}}
   {\underbrace{\omega^2}_{|(j\omega)^2|}\,T_i\,\underbrace{\sqrt{1+(\omega T_\Sigma)^2}}_{|1+j\omega T_\Sigma|}} $$

Se evalúa en el cruce usando las relaciones del Paso 2, \(\omega_c T_i = a\) y \(\omega_c T_\Sigma = 1/a\):

$$ \sqrt{1+(\omega_c T_i)^2}=\sqrt{1+a^2},\qquad
   \sqrt{1+(\omega_c T_\Sigma)^2}=\sqrt{1+\tfrac{1}{a^2}}=\frac{\sqrt{a^2+1}}{a},\qquad
   \omega_c^2 T_i = \Big(\tfrac{1}{aT_\Sigma}\Big)^2 a^2 T_\Sigma = \frac{1}{T_\Sigma} $$

Sustituyendo, las dos raíces \(\sqrt{1+a^2}\) se **cancelan**:

$$ |L(j\omega_c)| = K_p K_s\cdot\frac{\sqrt{1+a^2}}{\dfrac{1}{T_\Sigma}\cdot\dfrac{\sqrt{a^2+1}}{a}}
   = K_p K_s\,a\,T_\Sigma $$

Imponiendo \(|L(j\omega_c)|=1\):

$$ \boxed{K_p = \frac{1}{a\,K_s\,T_\Sigma}}, \qquad \omega_c = \frac{1}{a\,T_\Sigma} $$

**Paso 5 — Margen de fase (de dónde sale cada término).** La fase de \(L(j\omega)\), factor a factor
(la fase de un producto/cociente es la suma/resta de fases):

- \(K_p K_s > 0\) → \(0°\).
- Numerador \(1+j\omega T_i\) → \(+\arctan(\omega T_i)\).
- \((j\omega)^2\): \(j\omega\) tiene fase \(+90°\), al cuadrado \(+180°\); al estar en el denominador **resta**
  → \(-180°\).
- \(1+j\omega T_\Sigma\) en el denominador → \(-\arctan(\omega T_\Sigma)\).

$$ \angle L(j\omega) = -180° + \arctan(\omega T_i) - \arctan(\omega T_\Sigma) $$

El margen de fase es \(PM = 180° + \angle L(j\omega_c) = \arctan(\omega_c T_i) - \arctan(\omega_c T_\Sigma)\).
Con \(\omega_c T_i = a\) y \(\omega_c T_\Sigma = 1/a\):

$$ \boxed{PM = \arctan a - \arctan\frac{1}{a}} $$

**Por qué es el máximo:** la fase \(\arctan(\omega T_i) - \arctan(\omega T_\Sigma)\) es, en escala
logarítmica, una curva **simétrica** respecto a la media geométrica de \(1/T_i\) y \(1/T_\Sigma\); su derivada
se anula justo en \(\omega_c\). Colocar el cruce en esa media geométrica (el "óptimo simétrico")
**maximiza** el margen de fase disponible para esta estructura.

## 3 — Elección del factor \(a\)
El único parámetro libre es \(a\): compromiso entre rapidez, margen de fase y sobreoscilación.

| \(a\) | \(PM\) | Sobreoscilación al escalón (sin prefiltro) | Comentario |
|---|---|---|---|
| 2 | 36.9° | ~43 % | Rápido pero poco amortiguado |
| 2.4 | 43.6° | ~35 % | Compromiso habitual mínimo |
| 3 | 53.1° | ~28 % | Buen compromiso |
| 4 | 61.9° | ~20 % | Más robusto y lento |

Regla práctica: \(a = 2\text{–}4\). Cuanto mayor \(a\), más margen y menos sobreoscilación, pero menor ancho
de banda (\(\omega_c = 1/(aT_\Sigma)\) baja).

## 4 — Sobreoscilación y prefiltro de referencia
El lazo cerrado del óptimo simétrico tiene un **cero** en \(s=-1/T_i\) (heredado del PI). Ese cero provoca
una sobreoscilación grande ante un **escalón de referencia** (los % de la tabla). Se corrige con un
**prefiltro de referencia** que cancela ese cero:

$$ F_{ref}(s) = \frac{1}{1+sT_i} $$

El prefiltro solo actúa sobre la referencia, no sobre el rechazo de perturbaciones: la respuesta al escalón
se suaviza sin degradar la robustez ni la velocidad frente a perturbaciones. Por eso el óptimo simétrico es
especialmente bueno cuando lo importante es **rechazar perturbaciones** (el caso del bus DC).

## 5 — Aplicación: el lazo de tensión del bus DC
El caso canónico es el **lazo de tensión del bus DC** de un convertidor ([[convertidor-back-to-back]],
[[control-tension-bus-dc]]). Tras linealizar con \(w=V_{dc}^2\), la planta es un **integrador puro**
\(G_{dc}(s)=2/(C_{dc}s)\) (luego \(K_s = 2/C_{dc}\)), y el retardo pequeño \(T_\Sigma\) es el del lazo de
corriente interno, \(T_\Sigma \approx 1/\omega_{ci}\). Aplicando las fórmulas:

$$ K_{p,dc} = \frac{1}{a K_s T_\Sigma} = \frac{C_{dc}}{2\,a\,T_\Sigma} = \frac{C_{dc}\,\omega_{ci}}{2a}, \qquad
   \omega_{dc} = \frac{\omega_{ci}}{a} $$

Con la separación de escalas habitual \(a = \omega_{ci}/\omega_{dc} = 10\) (mayor que el \(2\text{–}4\)
clásico de la tabla del apartado 3, porque en este lazo en cascada la separación de escalas **fija** \(a\))
se obtiene \(K_{p,dc}=C_{dc}\omega_{dc}/2\) y \(PM \approx 79°\): un lazo DC muy amortiguado, robusto frente a la carga
de potencia constante (CPL) del otro convertidor. La razón de fondo es la misma que en cualquier planta con
integrador: no se puede cancelar el polo en el origen, así que se coloca el cero simétricamente para exprimir
el margen de fase.

## Errores comunes
- **Confundirlo con el óptimo de módulo (cancelación de polo).** El de módulo cancela un polo estable; el
  simétrico coloca el cero en una planta con integrador. Usar cancelación sobre un integrador destruye la
  acción integral.
- **Olvidar el prefiltro de referencia** y quejarse de la sobreoscilación: es inherente al cero del lazo
  cerrado, no un fallo de sintonía.
- **Tomar \(a\) demasiado pequeño** (\(a<2\)): margen de fase escaso y muy poca robustez ante la variación
  de \(T_\Sigma\).

## Cuándo y por qué se usa
Siempre que la planta a controlar con un PI **contenga un integrador**: lazos de tensión de bus DC, lazos de
velocidad de accionamientos (par → velocidad es un integrador), lazos de posición, control de nivel. Es el
método hermano del [[sintonia-pi-pid|óptimo de módulo]]: uno para plantas con polo estable (cancelación),
otro para plantas con integrador (colocación simétrica).

## Conceptos relacionados
- [[sintonia-pi-pid]] · [[margenes-estabilidad]] · [[diagrama-bode]] · [[loop-shaping]]
- [[control-tension-bus-dc]] · [[convertidor-back-to-back]] · [[controlador-pid]]

## Referencias
- Kessler, *Das symmetrische Optimum*, Regelungstechnik 1958.
- Åström, Hägglund, *Advanced PID Control*, ISA 2006.
- Leonhard, *Control of Electrical Drives*, Springer 2001.
