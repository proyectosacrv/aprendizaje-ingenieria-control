---
titulo: Impedancia virtual
slug: impedancia-virtual
categoria: control
tipo: tecnica
nivel: avanzado
proyectos: [01-GFM-Impedance]
objetivos: [estabilizar el lazo de potencia, amortiguar oscilaciones, desacoplar P-Q]
tags: [grid-forming, droop, reactancia, dq, amortiguamiento]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-02
relacionados: [droop-control, control-cascada, grid-forming-vs-following]
referencias:
  - "Rocabert et al., Control of Power Converters in AC Microgrids, IEEE Trans. Power Electron., 2012"
  - "Wang, Blaabjerg, Harmonic Stability in Power-Electronic-Based Power Systems, IEEE TPEL 2019"
---

## Definición
La **impedancia virtual** es una impedancia emulada por software que el inversor añade a su
salida **restándola de la referencia de tensión**, sin componentes físicos. Sirve para dar
forma a la impedancia de salida del convertidor: amortiguar, desacoplar P–Q y limitar
corriente.

## Fundamento teórico
La referencia de tensión del lazo se corrige con la caída sobre una impedancia
\( Z_v = R_v + jX_v \) recorrida por la corriente de salida \( \mathbf{i} \):

$$ \mathbf{v}_{C}^{*} = \mathbf{v}_{ref} - Z_v\,\mathbf{i} $$

En el marco dq (síncrono a \( \omega \)) la caída se expresa con el acoplamiento cruzado:

$$ v^{*}_{Cd} = v_{ref,d} - R_v i_d + \omega L_v i_q, \qquad
   v^{*}_{Cq} = v_{ref,q} - R_v i_q - \omega L_v i_d $$

El efecto clave: la ganancia del lazo de potencia de un grid-forming es
\( \partial P/\partial\delta \approx 1.5\,V^2/X \). Aumentar la reactancia efectiva con
\( X_v \) **reduce esa ganancia** y, por tanto, el riesgo de inestabilidad del lazo de
potencia, sin añadir un polo de planta lento (es algebraica sobre la referencia).

<div class="cfig"><img src="figuras/impedancia-virtual-pd.png" alt="curva P-delta con y sin impedancia virtual"><div class="cap">Curva $P(\delta)=1.5\,V^2/X\,\sin\delta$. Sumar reactancia virtual $X_v$ (azul) aplana la curva: la pendiente en el punto de operación $\partial P/\partial\delta$ —la ganancia del lazo de potencia— se reduce, amortiguando el lazo sin introducir un polo lento de planta.</div></div>

## 1 — Por qué restar \( Z_v\,\mathbf{i} \) de la referencia emula una impedancia
**Paso 1 — el lazo de tensión sigue su referencia.** El lazo interno de tensión es rápido y de alta ganancia, así que en su banda hace \( \mathbf{v}_C\approx\mathbf{v}_C^* \): la tensión del condensador sigue a la referencia que le damos. Esa es la palanca: lo que escribamos en \( \mathbf{v}_C^* \) aparece en bornes.

**Paso 2 — inyectar la caída de una impedancia ficticia.** Definimos la referencia como la consigna deseada menos la caída de una impedancia \( Z_v \) recorrida por la corriente de salida medida \( \mathbf{i} \):
$$ \mathbf{v}_C^*=\mathbf{v}_{ref}-Z_v\,\mathbf{i} $$
Combinando con \( \mathbf{v}_C\approx\mathbf{v}_C^* \):
$$ \mathbf{v}_C\approx\mathbf{v}_{ref}-Z_v\,\mathbf{i} $$

**Paso 3 — leerlo como Thévenin.** Esta ecuación es exactamente la de una fuente ideal \( \mathbf{v}_{ref} \) detrás de una impedancia serie \( Z_v \): la tensión en bornes cae \( Z_v\,\mathbf{i} \) conforme sube la corriente, igual que si hubiera un \( R_v+jX_v \) **físico** en serie. La impedancia de salida de pequeña señal que el equipo presenta hacia la red gana ese término:
$$ Z_o^{eff}(s)=Z_{o,fis}(s)+Z_v(s) $$
pero sin disipar potencia ni añadir hardware: es una caída calculada y reescrita en la referencia. Por eso tampoco mete un polo de planta lento — la operación es **algebraica** sobre \( \mathbf{v}_C^* \), instantánea dentro de la banda del lazo de tensión.

**Paso 4 — en dq el término reactivo se cruza.** Una reactancia es \( Z_v=R_v+j\omega L_v \); en el marco dq el producto \( j\omega L_v\cdot\mathbf{i} \) rota \( 90° \) los ejes, dando los términos cruzados de la ficha:
$$ v_{Cd}^*=v_{ref,d}-R_v i_d+\omega L_v i_q,\qquad v_{Cq}^*=v_{ref,q}-R_v i_q-\omega L_v i_d $$
(el \( +\omega L_v i_q \) en d y el \( -\omega L_v i_d \) en q son el "\( j \)" de la reactancia visto en componentes).

## 2 — La impedancia virtual como realimentación de corriente

La impedancia virtual no es solo un truco algebraico: es **una realimentación negativa de la corriente de salida sobre la consigna de tensión**, con una función de transferencia \( Z_v(s) \) como ganancia de realimentación.

### Diagrama de bloques

El lazo de control con impedancia virtual tiene la siguiente estructura:

$$
v_{ref} \xrightarrow{-Z_v(s)\cdot i} \underbrace{[\,+\,]}_{\text{suma}} \xrightarrow{} \underbrace{H_v(s)}_{\text{lazo tensión}} \xrightarrow{} v_C \xrightarrow{} \underbrace{G_{planta}(s)}_{\text{LCL+red}} \xrightarrow{} i
$$

La corriente \( i \) realimenta negativamente a través de \( Z_v(s) \). La impedancia de salida efectiva resultante es:

$$ Z_o^{eff}(s) = \frac{Z_{o,fis}(s)}{1 + H_v(s)\,Z_{o,fis}(s)/Z_v(s)} + Z_v(s) $$

que en el límite de lazo de tensión ideal (\( H_v\to\infty \)) se simplifica a:

$$ Z_o^{eff}(s) \approx Z_v(s) $$

La impedancia virtual **domina** la impedancia de salida cuando el lazo de tensión es rápido. El convertidor se ve desde la red como una fuente de tensión con impedancia serie \( Z_v \): exactamente un generador síncrono con su impedancia de campo.

### El desacoplo P-Q: hacer la red "efectivamente inductiva"

En una red con \( X/R \ll 1 \) (distribución, baja tensión), el flujo de potencia tiene una mezcla de P y Q dependiendo tanto del ángulo como de la amplitud. Esto hace que los controles de droop P-f y Q-V estén acoplados.

Añadiendo \( X_v \gg R_{red} \) (reactancia virtual mucho mayor que la resistencia de la línea), la impedancia total vista desde el PCC es:

$$ Z_{tot} = R_{red} + jX_{red} + jX_v \approx j(X_{red}+X_v) = jX_{tot} $$

La red se vuelve **efectivamente inductiva**: \( X_{tot}/R_{tot} \gg 1 \). En este límite, el flujo de potencia se desacopla:

$$ P \approx \frac{E\,V}{X_{tot}}\sin\delta, \qquad Q \approx \frac{V(E\cos\delta - V)}{X_{tot}} $$

con P controlado por el ángulo \( \delta \) y Q por la amplitud \( E \), sin interferencia. Los droops P-f y Q-V funcionan correctamente.

### Aplicación al amortiguamiento del lazo de potencia

La ganancia del lazo de potencia del GFM droop es:

$$ K_s = \frac{\partial P}{\partial\delta} = \frac{3}{2}\cdot\frac{E\,V\cos\delta_0}{X_{tot}} $$

Con \( X_v \) añadida: \( X_{tot}=X_{fis}+X_v \), así que:

$$ K_s(X_v) = \frac{3}{2}\cdot\frac{E\,V\cos\delta_0}{X_{fis}+X_v} = K_s(0)\cdot\frac{X_{fis}}{X_{fis}+X_v} $$

El amortiguamiento del modo de potencia es \( \zeta\propto1/\sqrt{K_s} \), luego:

$$ \frac{\zeta(X_v)}{\zeta(0)} = \sqrt{\frac{X_{fis}+X_v}{X_{fis}}} = \sqrt{1+\frac{X_v}{X_{fis}}} $$

Para doblar el amortiguamiento (\( \zeta\to2\zeta_0 \)) se necesita \( X_v = 3\,X_{fis} \). Para alcanzar \( \zeta=0.7 \) partiendo de \( \zeta_0=0.15 \):

$$ X_v = X_{fis}\left[\left(\frac{0.7}{0.15}\right)^2 - 1\right] = X_{fis}\cdot(21.8-1) = 20.8\,X_{fis} $$

Un valor tan alto implicaría una caída de tensión inaceptable (ver apartado 6). En la práctica se combina \( X_v \) moderada con resistencia virtual transitoria (apartado 5) para alcanzar el objetivo de amortiguamiento.

<div class="cfig"><img src="figuras/impedancia-virtual-analisis.png" alt="Impedancia virtual: diagrama bloques, amortiguamiento, Bode Zo, caída tensión"><div class="cap">Panel (a): diagrama de bloques del lazo de tensión con realimentación de corriente a través de $Z_v$. Panel (b): $\zeta$ del modo de potencia vs $X_{virt}$; se marca el $X_v$ para $\zeta=0.7$. Panel (c): Bode de la impedancia de salida $|Z_o(j\omega)|$ sin y con $X_v=8\,\text{mH}$. Panel (d): caída de tensión en PCC vs $X_{virt}$, con y sin feedforward de corriente.</div></div>

## 3 — La impedancia virtual resistiva para redes resistivas

### El problema de las redes con \( X/R \) bajo

En redes de distribución de baja y media tensión, la relación \( X/R \) de las líneas es típicamente menor que 1 (líneas cortas y cables con resistencia significativa). En estas condiciones:

- La potencia activa \( P \) depende tanto de \( \delta \) como de \( E-V \) (tensión).
- La potencia reactiva \( Q \) depende tanto de \( E-V \) como de \( \delta \) (ángulo).
- Los droops \( P\text{-}f \) y \( Q\text{-}V \) convencionales intercambian roles: el droop P-f regula mal la potencia activa y el droop Q-V regula mal la reactiva.

### La solución: \( R_{virt} \gg R_{línea} \)

Añadiendo una resistencia virtual grande, la impedancia total vista desde el PCC se vuelve dominantemente resistiva:

$$ Z_{tot} = (R_{linea}+R_v) + jX_{linea} \approx R_v \qquad\text{si }R_v\gg\sqrt{R_{linea}^2+X_{linea}^2} $$

La ley de control es simplemente:

$$ \mathbf{v}_{C}^* = \mathbf{v}_{ref} - R_v\,\mathbf{i}_d $$

(solo el componente d, que es el que lleva la potencia activa en coordenadas orientadas por tensión). El flujo de potencia activa se vuelve:

$$ P \approx \frac{E\,V}{R_v}(E-V) $$

que permite usar un droop \( P\text{-}V \) (potencia activa controlada por amplitud de tensión) en lugar del droop \( P\text{-}f \) convencional.

### El compromiso de la resistencia virtual

La resistencia virtual introduce una caída de tensión en el eje d proporcional a la corriente activa:

$$ \Delta V_{PCC} \approx R_v\,I_d $$

Para \( R_v=0.1\,\text{pu} \) e \( I_d=1\,\text{pu} \), la caída es del 10 %, lo que viola los límites de regulación (típicamente ±5 %). Las soluciones son:

1. **Límitar \( R_v \)** a un valor pequeño (0.02–0.05 pu): mejora el desacoplo pero no elimina el acoplamiento.
2. **Feedforward de corriente** para compensar la caída estática: \( v_{ref,d} += R_v\,I_{d,0} \).
3. **Usar \( R_v \) solo en el transitorio** (resistencia virtual transitoria, apartado 5): no hay caída estática porque en régimen permanente la componente de alta frecuencia de \( i \) es cero.

## 4 — La impedancia virtual inductiva para mejorar el amortiguamiento

### El efecto sobre la ganancia de planta \( K_s \)

Como se derivó en el apartado 2, añadir \( X_v \) reduce la ganancia del modo de potencia:

$$ K_s = \frac{EV\cos\delta_0}{X_{fis}+X_v} $$

El amortiguamiento sube como \( \sqrt{(X_{fis}+X_v)/X_{fis}} \). Para el proyecto 01 (GFM-Impedance) con \( X_{fis}=0.05\,\text{pu} \):

| \( X_{virt} \) [pu] | \( X_{tot} \) [pu] | \( K_s/K_{s0} \) | \( \zeta/\zeta_0 \) |
|--|--|--|--|
| 0 (sin impedancia virtual) | 0.05 | 1.00 | 1.00 → \( \zeta_0=0.15 \) |
| 0.03 | 0.08 | 0.625 | 1.26 → \( \zeta=0.19 \) |
| 0.05 | 0.10 | 0.500 | 1.41 → \( \zeta=0.21 \) |
| 0.10 | 0.15 | 0.333 | 1.73 → \( \zeta=0.26 \) |

Partiendo de \( \zeta_0=0.15 \), la reactancia virtual inductiva por sí sola es insuficiente para alcanzar \( \zeta=0.40 \) sin valores de \( X_v \) que implican caídas de tensión excesivas. Sin embargo, la combinación con resistencia virtual transitoria (apartado 5) permite alcanzar el objetivo.

**Resultado del proyecto 01:** con \( X_v=0.05\,\text{pu}\approx8\,\text{mH} \), \( \zeta \) del modo de potencia pasa de 0.15 a 0.21 (aumento del 40 %). La combinación con \( R_{v,tr}=0.15\,\text{pu} \) lleva \( \zeta \) a 0.40.

### Implementación en dq

En coordenadas dq síncronas a \( \omega_0 \), la caída sobre una inductancia virtual \( L_v=X_v/\omega_0 \) es:

$$ \Delta v_d = -\omega_0 L_v\,i_q + L_v\,\frac{di_d}{dt} \approx -\omega_0 L_v\,i_q $$
$$ \Delta v_q = +\omega_0 L_v\,i_d + L_v\,\frac{di_q}{dt} \approx +\omega_0 L_v\,i_d $$

donde se desprecia el término derivado (es la componente de alta frecuencia, dominada por el lazo de corriente). Las referencias de tensión con impedancia virtual se escriben:

$$ v_{Cd}^* = v_{ref,d} - R_v\,i_d + \omega_0 L_v\,i_q $$
$$ v_{Cq}^* = v_{ref,q} - R_v\,i_q - \omega_0 L_v\,i_d $$

El signo del término cruzado inductivo (\( +\omega_0 L_v\,i_q \) en d, \( -\omega_0 L_v\,i_d \) en q) es consistente con la representación dq de una inductancia: la corriente en q afecta a la tensión en d y viceversa, con el signo de la rotación de Park.

### El límite: no mover la resonancia del LCL

La inductancia virtual \( L_v \) se suma algebraicamente a la inductancia de lado fuente \( L_1 \) del filtro LCL desde el punto de vista de la impedancia de salida. Sin embargo, **no mueve la resonancia del LCL físico** porque la operación es sobre la referencia de tensión del condensador, no sobre la bobina física. La frecuencia de resonancia del filtro LCL sigue siendo:

$$ f_{res} = \frac{1}{2\pi}\sqrt{\frac{L_1+L_2}{L_1 L_2 C_f}} $$

sin cambios. Esto es la ventaja clave frente a añadir inductancia física: la virtual no perturba la resonancia del filtro ni el margen del lazo de corriente.

## 5 — El amortiguamiento activo como impedancia virtual capacitiva

### La corriente del condensador como señal de amortiguamiento

En el filtro LCL, la corriente del condensador \( i_{Cf} = C_f \dot v_C \) es la señal que contiene la información de la resonancia: en la frecuencia de resonancia, \( i_{Cf} \) tiene un pico mientras \( i_2 \) (corriente de red) ya ha empezado a caer. Realimentar \( i_{Cf} \) sobre la referencia de tensión equivale a añadir una **impedancia virtual capacitiva** (o más exactamente, una admitancia derivativa) que amortigua la resonancia.

### La ley de amortiguamiento activo

El amortiguamiento activo por realimentación de corriente del condensador es:

$$ \mathbf{v}_C^* = \mathbf{v}_{ref} - Z_v\,\mathbf{i} - K_{ad}\,\mathbf{i}_{Cf} $$

donde \( K_{ad} \) [Ω] es la ganancia de amortiguamiento activo e \( \mathbf{i}_{Cf} \) es la corriente medida (o estimada) del condensador. En la práctica \( i_{Cf} \) se calcula como:

$$ i_{Cf} = i_1 - i_2 $$

(diferencia entre la corriente de lado fuente y la corriente de red), sin necesidad de un sensor adicional si se miden ambas corrientes.

### La equivalencia con una resistencia en serie con \( C_f \)

Analíticamente, el lazo de amortiguamiento activo equivale a colocar una resistencia virtual \( R_d^{virt} = K_{ad}/(\omega_f L_1) \) en serie con el condensador del filtro LCL. La frecuencia de resonancia no cambia; solo se añade amortiguamiento al polo resonante.

La demostración: la función de transferencia del LCL con amortiguamiento activo por \( i_{Cf} \) con ganancia \( K_{ad} \) tiene el mismo polinomio caracteristico que el LCL con \( R_d \) físico en serie con \( C_f \), bajo la identificación \( R_d = K_{ad} \) (a la frecuencia de resonancia).

### Sin pérdidas: la ventaja sobre el amortiguamiento pasivo

Una \( R_d \) física en serie con \( C_f \) disipa potencia: \( P_{diss}=R_d\,I_{Cf}^2 \). El amortiguamiento activo realiza la misma función **sin disipación**: la resistencia es virtual, calculada, y no introduce pérdidas reales. La potencia que "disipa" virtualmente se redirige al lazo de corriente, que la inyecta a la red.

### El límite: el retardo digital

El amortiguamiento activo tiene una limitación práctica importante: el **retardo de cómputo digital** \( T_d \approx 1.5\,T_{sw} \) (uno o dos periodos de muestreo). La corriente del condensador a la frecuencia de resonancia \( f_{res} \) tiene un retardo de fase:

$$ \phi_{retardo} = 2\pi f_{res}\,T_d $$

Si \( \phi_{retardo} > 90° \), la realimentación de \( i_{Cf} \) cambia de amortiguante a excitadora: el amortiguamiento activo **inestabiliza** la resonancia en lugar de amortiguarla.

Condición de límite estable:

$$ f_{res} < \frac{1}{4\,T_d} = \frac{f_{sw}}{6} \qquad\text{(para }T_d=1.5T_{sw}\text{)} $$

Para \( f_{sw}=5\,\text{kHz} \), el amortiguamiento activo es estable para resonancias por debajo de 833 Hz. Resonancias más altas requieren amortiguamiento pasivo.

## 6 — El límite de la impedancia virtual: la regulación de tensión

### La caída de tensión en el PCC

La impedancia virtual inductiva introduce una caída de tensión en el PCC proporcional a la corriente y a \( X_v \):

$$ \Delta V_{PCC} \approx \frac{X_v\,I}{V_0} \quad\text{[en pu: }\Delta V_{PCC}\approx X_v\cdot I\text{]} $$

donde todo está en pu (\( X_v \) en pu, \( I \) en pu respecto a la corriente nominal, \( V_0=1\,\text{pu} \)).

**Ejemplo numérico:** con \( X_v=0.1\,\text{pu} \) e \( I=1\,\text{pu} \) (corriente nominal):

$$ \Delta V_{PCC} \approx 0.1\,\text{pu} = 10\,\% $$

Este valor viola el límite de regulación de tensión de ±5 % de los estándares de conexión a red (EN 50160, IEEE 1547). El diseño de \( X_v \) debe equilibrar la mejora de amortiguamiento con el cumplimiento de la regulación de tensión.

### El diagrama \( \Delta V \) vs \( X_v \): el triángulo de diseño

El diseño de la impedancia virtual tiene tres restricciones que se pueden visualizar en el plano \( (X_v, \zeta) \):

- **Restricción de amortiguamiento mínimo:** \( \zeta > \zeta_{min} \) → exige \( X_v > X_{v,min} \).
- **Restricción de regulación de tensión:** \( \Delta V < \Delta V_{max} \) → impone \( X_v < \Delta V_{max} \) (en pu con \( I=1\,\text{pu} \)).
- **Restricción de ángulo de operación:** \( \delta < 60° \) (límite práctico de estabilidad estática) → limita \( X_{tot} \) máxima.

Si el amortiguamiento objetivo requiere más \( X_v \) de la que permite la regulación de tensión, la única salida es:

1. Añadir **feedforward de corriente** para compensar la caída estática.
2. Usar **resistencia virtual transitoria** (solo actúa en transitorios, no en régimen permanente).
3. Aceptar un amortiguamiento menor y complementar con otros métodos (gain scheduling, PSS).

### La solución: feedforward de corriente

El feedforward compensa la caída estática de la impedancia virtual sumando la caída esperada a la referencia de tensión:

$$ v_{ref,d}^{nuevo} = v_{ref,d} + R_v\,I_{d,0} - \omega_0 L_v\,I_{q,0} $$

donde \( I_{d,0} \), \( I_{q,0} \) son los valores en régimen permanente de la corriente (filtrados paso-bajo). En transitorio, el feedforward no actúa (la señal filtrada no sigue el transitorio rápido) y la impedancia virtual trabaja normalmente. En régimen permanente, el feedforward cancela la caída:

$$ \Delta V_{PCC}^{con\,FF} \approx 0 $$

Con feedforward, la restricción de regulación de tensión prácticamente desaparece y \( X_v \) puede elegirse libremente según el amortiguamiento deseado.

## 7 — Diseño iterativo: impedancia virtual para el proyecto 01

El proyecto 01 (GFM-Impedance) arrancó con un diseño inestable del lazo de potencia. A continuación se muestra el proceso de iteración de la impedancia virtual hasta alcanzar las especificaciones.

### Especificaciones del proyecto

- Sistema: GFM de 1 MVA, \( X_{fis}=0.05\,\text{pu} \) (incluye \( L_2 \) del LCL y trafo de MT).
- Objetivo: \( \zeta \geq 0.40 \) del modo de potencia.
- Restricción de tensión: \( \Delta V_{PCC} \leq 5\,\% \) en régimen permanente.

### Iteración 0: sin impedancia virtual

\( X_v=0 \), \( R_v=0 \), \( R_{v,tr}=0 \). El análisis de autovalores del modelo linealizado da:

| Modo | Frecuencia (Hz) | \( \zeta \) | Estado |
|------|-----------------|-------------|--------|
| Potencia | 3.3 | 0.15 | Marginalmente estable (oscila) |
| Corriente \( L_1 \) | 820 | 0.04 | Resonancia LCL (amortiguamiento activo) |
| Corriente \( L_2 \) | 820 | 0.04 | — |

\( \zeta=0.15 \) es insuficiente: la respuesta ante escalones de potencia oscila durante varios segundos.

### Iteración 1: \( X_v=0.03\,\text{pu} \)

Se añade \( L_v = X_v/\omega_0 = 0.03/(314.16)\approx4.8\,\text{mH} \). Resultado:

| Modo | \( \zeta \) | \( \Delta V_{PCC} \) |
|------|-------------|---------------------|
| Potencia | 0.19 | 3.0 % |

Mejora del 27 %, aún insuficiente.

### Iteración 2: \( X_v=0.05\,\text{pu} \)

\( L_v\approx8\,\text{mH} \). Resultado:

| Modo | \( \zeta \) | \( \Delta V_{PCC} \) |
|------|-------------|---------------------|
| Potencia | 0.21 | 5.0 % |

Límite de tensión alcanzado (\( \Delta V=5\,\% \)) con un amortiguamiento de 0.21, todavía insuficiente. Sin feedforward, no se puede subir más \( X_v \).

### Iteración 3: \( X_v=0.05\,\text{pu} \) + feedforward de corriente

Se añade feedforward de corriente (componente paso-bajo filtrada a 1 Hz) que cancela la caída estática. El resultado en régimen permanente es \( \Delta V_{PCC} < 1\,\% \). El amortiguamiento no cambia respecto a It.2 (el feedforward no afecta a la dinámica transitoria).

Ahora con la restricción de tensión eliminada (gracias al feedforward), se puede añadir **resistencia virtual transitoria** para aumentar el amortiguamiento:

\( R_{v,tr}=0.15\,\text{pu} \) con filtro paso-alto a \( f_{ht}=4\,\text{Hz} \) (por debajo del modo de potencia a 3.3 Hz):

| Modo | \( \zeta \) | \( \Delta V_{PCC} \) |
|------|-------------|---------------------|
| Potencia | 0.40 | < 1 % |

Objetivo alcanzado. La tabla completa de iteraciones:

| It. | \( X_v \) [pu] | \( R_{v,tr} \) [pu] | FF | \( \zeta \) | \( \Delta V \) [%] | ¿OK? |
|-----|-----------------|----------------------|----|-------------|-------------------|------|
| 0   | 0               | 0                    | No | 0.15 | 0   | No |
| 1   | 0.03            | 0                    | No | 0.19 | 3.0 | No |
| 2   | 0.05            | 0                    | No | 0.21 | 5.0 | No (\( \zeta \) bajo) |
| 3   | 0.05            | 0.15                 | Sí | 0.40 | <1  | Sí |

### Conclusión del diseño iterativo

La lección del proceso es que **ninguna técnica aislada es suficiente**: la reactancia virtual mejora el amortiguamiento pero viola la regulación de tensión; el feedforward quita esa restricción; la resistencia virtual transitoria añade el amortiguamiento que falta sin coste en régimen permanente. La combinación de las tres es la solución óptima para el proyecto 01.

## Cuándo y por qué se usa
- Cuando la reactancia de acoplamiento real es pequeña → \( \partial P/\partial\delta \)
  enorme → el lazo de potencia tiene poco margen de fase y oscila o se inestabiliza.
- Para **desacoplar** P (ángulo) de Q (tensión) haciendo la red vista más inductiva.
- Como base del **current limiting** (impedancia virtual adaptativa en faltas).

## Procedimiento de diseño (genérico)
1. **Elige la parte inductiva \( X_v \)** para fijar la impedancia de acoplamiento total
   deseada (típico 0.1–0.3 pu): \( X_{tot} = X_{fisica} + X_v \). Más \( X_v \) → menor
   \( \partial P/\partial\delta \) → lazo de potencia más amortiguado, pero más caída de
   tensión y mayor \( \delta \) en operación.
2. **Verifica el equilibrio**: la parte **resistiva \( R_v \)** estática introduce una caída
   en el eje d que el droop Q–V intenta compensar generando reactiva → puede disparar
   \( Q_{eq} \). Usa \( R_v \) pequeña.
3. **Para amortiguar sin distorsionar el equilibrio**, usa **resistencia virtual transitoria**:
   aplica \( R_v \) solo a la componente de alta frecuencia de la corriente (filtro paso-alto),
   con corte **por debajo** del modo a amortiguar:
   $$ v_{virt} = R_{v,tr}\,\big(i - \text{LPF}_{f_{ht}}(i)\big) $$
4. **Añade feedforward de corriente** si la caída de tensión estática supera el ±5 %:
   suma la caída estática esperada a la referencia de tensión.
5. **Comprueba con autovalores**: barre \( X_v, R_{v,tr} \) y maximiza el amortiguamiento
   \( \zeta \) del modo de potencia manteniendo \( Q_{eq} \) y \( \delta \) razonables.

## Ejemplo de código
```python
# Impedancia virtual estatica + resistencia virtual transitoria (marco dq)
wht = 2*np.pi*f_ht                      # corte del HPF
iL2_hp = iL2 - iL2_lp                   # componente transitoria (estado iL2_lp = LPF)
vvirt_d = Rv*iL2d - w*Lv*iL2q + Rvt*iL2_hp[0]
vvirt_q = Rv*iL2q + w*Lv*iL2d + Rvt*iL2_hp[1]
vcref_d, vcref_q = Vref - vvirt_d, 0.0 - vvirt_q
diL2_lp = wht*(iL2 - iL2_lp)            # dinamica del filtro paso-bajo

# Feedforward de corriente para compensar caida estatica (componente LP)
vcref_d += Rv*iL2_lp[0] - w*Lv*iL2_lp[1]  # cancela caida estacionaria
```

## Parámetros y valores típicos
- \( X_v \): 0.05–0.15 pu (en el proyecto, \( L_v = 8\,\text{mH} \approx 0.05\,\text{pu} \)).
- \( R_v \) estática: pequeña (≈0.02–0.05 pu) para no disparar Q.
- \( R_{v,tr} \): mayor (≈0.10–0.20 pu) porque solo actúa en transitorios; corte \( f_{ht} \)
  por debajo del modo (en el proyecto, 4 Hz para un modo de 3.3 Hz).
- Feedforward: filtro paso-bajo a 1–2 Hz para extraer la componente estacionaria de \( i \).

## Errores comunes
- **Usar \( R_v \) resistiva grande** para amortiguar → dispara \( Q_{eq} \) (pelea con el
  droop Q–V). Solución: inductiva para ganancia, transitoria para amortiguamiento.
- **Confundir \( L_v \) virtual con subir \( L_2 \) físico**: el físico añade un polo lento de
  planta y mueve la resonancia LCL; la virtual no.
- Poner el corte del HPF por encima del modo → la resistencia transitoria no actúa donde se
  necesita.
- **Omitir el feedforward** cuando \( X_v > 0.05\,\text{pu} \): la caída de tensión viola la norma.

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: estabilizar el lazo de potencia): el primer diseño era
  inestable porque \( \partial P/\partial\delta \) era enorme. Añadir \( L_v = 8\,\text{mH} \)
  estabilizó sin distorsionar el equilibrio, y la \( R_{v,tr} \) subió el amortiguamiento del
  modo de potencia de \( \zeta=0.15 \) a \( \zeta=0.40 \). Implementado en `simulate.py` y
  `model.py`.

## Conceptos relacionados
- [[droop-control]] — la impedancia virtual moldea el lazo de potencia del droop.
- [[control-cascada]] — se aplica sobre la referencia del lazo de tensión.
- [[grid-forming-vs-following]] — pieza casi obligatoria en grid-forming.

## Referencias
- Rocabert et al., *Control of Power Converters in AC Microgrids*, IEEE TPEL 2012.
- Wang, Blaabjerg, *Harmonic Stability in Power-Electronic-Based Power Systems*, IEEE TPEL 2019.
