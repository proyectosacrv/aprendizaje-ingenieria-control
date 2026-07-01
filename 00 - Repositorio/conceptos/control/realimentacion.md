---
titulo: Realimentación (lazo abierto y cerrado)
slug: realimentacion
categoria: control
tipo: concepto
nivel: basico
proyectos: []
objetivos: [entender por que se realimenta y que aporta el lazo cerrado]
tags: [realimentacion, lazo-cerrado, feedback, error, basico, sensibilidad, robustez, integral]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [funcion-transferencia, controlador-pid, funciones-sensibilidad, margenes-estabilidad, error-regimen-permanente]
referencias:
  - "Aström, Murray, Feedback Systems, Princeton 2008"
  - "Ogata, Ingeniería de Control Moderna, Pearson"
---

## Definición
**Realimentar** es medir la salida, compararla con la referencia y actuar sobre la diferencia
(el **error**). El **lazo cerrado** usa esa medida; el **lazo abierto** actúa sin medir. La
realimentación es la idea central del control automático.

## Fundamento teórico
Con planta \( G(s) \) y controlador \( C(s) \) en lazo cerrado con realimentación unitaria, la
transferencia referencia → salida es:
$$ T(s) = \frac{C(s)G(s)}{1 + C(s)G(s)} $$
y el error responde según la **sensibilidad** \( S(s)=1/(1+CG) \). Lo que aporta el lazo cerrado:
- **Reduce el error** ante perturbaciones y errores de modelo (si la ganancia de lazo \( CG \) es
  grande, \( S \) es pequeña).
- **Modifica la dinámica** (mueve los polos) y puede estabilizar una planta inestable.
- **Riesgo**: una ganancia mal puesta puede **inestabilizar** (de ahí los márgenes).

El lazo abierto es simple pero no corrige perturbaciones ni errores de modelo.

<div class="cfig"><img src="figuras/realimentacion-lazo.png" alt="lazo de control realimentado"><div class="cap">Lazo cerrado: el error e=r−y entra al controlador C(s), que actúa sobre la planta G(s); la salida se mide y realimenta (signo −). Es lo que permite corregir perturbaciones y errores de modelo.</div></div>

## 1 — Cómo sale \( T=L/(1+L) \) del diagrama
**Paso 1 — escribir las relaciones del lazo.** En el lazo cerrado con realimentación unitaria hay tres ecuaciones de bloques (ver [[diagrama-bloques]]): el error es la resta, la salida es la cadena directa actuando sobre el error, y abreviamos la **ganancia de lazo** \( L(s)\equiv C(s)G(s) \):

$$ E=R-Y,\qquad Y=C\,G\,E = L\,E $$

**Paso 2 — eliminar el error.** Sustituyendo \( E=R-Y \) en \( Y=L\,E \):

$$ Y = L\,(R-Y) = L\,R - L\,Y $$

**Paso 3 — agrupar \( Y \).** Pasando \( L\,Y \) a la izquierda y sacando factor común:

$$ Y + L\,Y = L\,R \;\Longrightarrow\; Y(1+L)=L\,R $$

de donde la transferencia referencia → salida (la **función de transferencia complementaria**):

$$ \boxed{\;T(s)=\frac{Y}{R}=\frac{L}{1+L}=\frac{CG}{1+CG}\;} $$

El denominador \( 1+L=0 \) es la **ecuación característica**: sus raíces son los polos del lazo cerrado. De ahí que realimentar **mueva los polos** (y pueda estabilizar o inestabilizar según \( L \)).

## 2 — La sensibilidad \( S \) y la identidad \( S+T=1 \)
**Paso 1 — transferencia referencia → error.** Partiendo de \( E=R-Y \) y \( Y=T\,R \) del apartado anterior:

$$ E = R - T\,R = (1-T)\,R $$

**Paso 2 — sustituir \( T \) y combinar fracciones.** Con \( T=\dfrac{L}{1+L} \), poniendo \( 1=\dfrac{1+L}{1+L} \):

$$ 1-T = \frac{1+L}{1+L}-\frac{L}{1+L} = \frac{1+L-L}{1+L}=\frac{1}{1+L} $$

Se define esa transferencia como **sensibilidad** \( S \):

$$ \boxed{\;S(s)=\frac{E}{R}=\frac{1}{1+L},\qquad S+T=1\;} $$

**Paso 3 — interpretar.** El error en el lazo es \( E=S\,R \). Si la ganancia de lazo es **grande** en una frecuencia (\( |L|\gg 1 \)), entonces \( S\approx 1/L\to 0 \): el error se reduce en ese rango — por eso el integrador del PI, que hace \( |L|\to\infty \) en continua, **anula el error en régimen** ante escalón (ver [[error-regimen-permanente]]). La identidad \( S+T=1 \) impone el compromiso fundamental: no se puede hacer \( S \) pequeña (rechazo) y \( T\approx 1 \) (seguimiento) más allá de lo que suman a 1 en cada frecuencia.

## 3 — Las cuatro funciones de transferencia fundamentales

Hay cuatro FDT que describen completamente el comportamiento del lazo cerrado. Todas comparten el denominador \( 1+L \) (la ecuación característica) y se obtienen variando qué señal del lazo se estudia como entrada o salida.

**\( T(s) \) — función complementaria (seguimiento de referencia).**
Ya derivada: es la respuesta de la salida ante la referencia cuando la perturbación es cero.
$$ \boxed{T(s)=\frac{L}{1+L}=\frac{CG}{1+CG}} $$
Bien diseñada: \( |T|\approx 1 \) en el ancho de banda (la salida sigue la referencia), \( |T|\to 0 \) a alta frecuencia (no amplifican ruido).

**\( S(s) \) — sensibilidad (rechazo de perturbaciones, error ante referencia).**
Ya derivada: es la respuesta del error ante la referencia, o de la salida ante una perturbación que entra a la salida de la planta.
$$ \boxed{S(s)=\frac{1}{1+L}} $$
Bien diseñada: \( |S|\ll 1 \) en la banda donde hay perturbaciones o donde se quiere buen seguimiento. El **máximo de \( |S| \)** se llama \( M_s \) y es una medida de robustez: si \( M_s > 2 \) el diseño es frágil.

**\( PS(s) \) — sensibilidad de la planta (o sensibilidad a perturbaciones aguas arriba de la planta).**
Si la perturbación \( d \) entra directamente en la entrada de la planta (no en la salida), la respuesta de la salida es:
$$ Y = G\,(C\cdot E + d) $$
Resolviendo con \( E=R-Y \): \( Y=T\,R + G\,S\,d \). La FDT perturbación→salida es:
$$ \boxed{PS(s)=G(s)\,S(s)=\frac{G}{1+CG}} $$
Representa cómo el lazo filtra las perturbaciones que entran antes de la planta (p.ej. una tensión de red como perturbación al lazo de corriente).

**\( CS(s) \) — sensibilidad del controlador (señal de control).**
La señal de control \( U=C\,E=C\,S\,R \). La FDT referencia→señal de control es:
$$ \boxed{CS(s)=C(s)\,S(s)=\frac{C}{1+CG}} $$
Muestra qué esfuerzo de control exige el regulador. Si \( |CS| \) es grande a alta frecuencia, el actuador saturará ante escalones o ruido de medida. Un PI tiene \( |C|\propto 1/\omega \) a baja frecuencia (por la acción integral) y \( |C|\propto K_p \) a alta frecuencia, de modo que \( |CS| \) queda acotado.

**La identidad \( S+T=1 \) — consecuencia algebraica directa.**
Sumando la definición de \( S \) y \( T \):
$$ S + T = \frac{1}{1+L} + \frac{L}{1+L} = \frac{1+L}{1+L} = 1 \quad \forall s $$
Esto es una restricción absoluta. En cualquier frecuencia donde \( T\approx 1 \) (buen seguimiento), forzosamente \( S\approx 0 \) (bajo error). Donde \( T \) cae (\( |T|\ll 1 \), fuera del ancho de banda), \( S\to 1 \) — el lazo ya no ayuda. La identidad explica el **trade-off fundamental**: no se puede pedir simultáneamente buen seguimiento y buen rechazo en todas las frecuencias — solo puede haber una región donde el lazo actúa eficazmente.

<div class="cfig"><img src="figuras/realimentacion-analisis.png" alt="las cuatro FDT y el trade-off S vs T"><div class="cap">Análisis de las cuatro FDT fundamentales con \(L=10/[s(s+1)]\). (a) Las cuatro magnitudes de Bode: \(|T|\) y \(|S|\) se complementan hasta sumar 1, \(|PS|\) y \(|CS|\) cuantifican el esfuerzo del actuador y el rechazo a perturbaciones de planta. (b) La sensibilidad \(|S|\) disminuye al subir \(K\): mayor ganancia → mayor robustez a baja frecuencia. (c) Tabla de error en régimen: el tipo del sistema determina qué clase de entradas puede seguir con error nulo. (d) Trade-off: la zona de bajo \(|S|\) (rechazo) y la zona de \(|T|\approx 0\;dB\) (seguimiento) no pueden coexistir en todas las frecuencias.</div></div>

## 4 — La ecuación característica y los polos del lazo cerrado

Los **polos del lazo cerrado** son las raíces de la ecuación característica:
$$ 1 + L(s) = 0 \;\Longleftrightarrow\; 1 + C(s)G(s) = 0 $$

Esta ecuación gobierna toda la dinámica del lazo: si tiene raíces en el semiplano derecho (\( \mathrm{Re}(s)>0 \)), el sistema es **inestable**. En lazo abierto los polos son los de \( C \) y \( G \) por separado; al cerrar el lazo los polos se mueven.

**Efecto de subir la ganancia \( K \).** Escribiendo el controlador como \( C(s)=K\cdot C_0(s) \), con \( K \) escalar:
$$ 1 + K\,C_0(s)G(s) = 0 $$
Al barrer \( K \) de 0 a \( \infty \), las raíces trazan el **lugar de las raíces** (ver [[lugar-raices]]). Las conclusiones cualitativas son:

- Para \( K=0 \): los polos del lazo cerrado coinciden con los polos de la planta \( G \) (la planta domina).
- Para \( K\to\infty \): los polos migran hacia los **ceros** de la ganancia de lazo \( L \) (el controlador domina).
- Para \( K \) intermedio: los polos siguen trayectorias continuas — en algún punto pueden cruzar el eje imaginario e inestabilizar el lazo.

**El cruce del eje imaginario — condición de oscilación sostenida.**
En el cruce \( s=j\omega_c \), la ecuación característica impone:
$$ L(j\omega_c) = -1 \;\Longrightarrow\; |L(j\omega_c)|=1,\quad \angle L(j\omega_c)=-180° $$
La primera condición fija la ganancia crítica; la segunda la frecuencia de cruce. Esta es exactamente la condición que estudia el criterio de [[criterio-nyquist|Nyquist]] y de la que se derivan los [[margenes-estabilidad|márgenes de ganancia y de fase]].

**Intuición física.** Una ganancia de lazo alta "gira" más los polos hacia la izquierda (buena atenuación de perturbaciones) pero eventualmente los lleva a la derecha (inestabilidad). El diseño es encontrar el \( K \) que equilibra ambos efectos manteniendo los márgenes deseados.

## 5 — Efectos de la retroalimentación en la robustez

**Lazo abierto: la variación de la planta pasa íntegra a la salida.**
Si la planta cambia de \( G \) a \( G+\Delta G \), la salida del lazo abierto cambia de \( G\,U \) a \( (G+\Delta G)\,U \). La variación relativa de la salida es igual a la variación relativa de la planta:
$$ \frac{\Delta Y_{LA}}{Y_{LA}} = \frac{\Delta G}{G} $$
Un error del 10% en \( G \) produce directamente un error del 10% en la salida.

**Lazo cerrado: la sensibilidad atenúa el efecto de la variación.**
Con realimentación, \( T=CG/(1+CG) \). Al variar \( G\to G+\Delta G \):
$$ T + \Delta T = \frac{C(G+\Delta G)}{1+C(G+\Delta G)} $$
Haciendo \( \Delta G \) pequeño y restando \( T \):
$$ \frac{\partial T}{\partial G} = \frac{C}{(1+CG)^2} = \frac{T}{G}\cdot\frac{1}{1+CG} = \frac{T}{G}\cdot S $$
La **sensibilidad relativa** de \( T \) respecto a \( G \) es:
$$ \frac{\Delta T/T}{\Delta G/G} = S(s) $$
Si \( |L|\gg 1 \) (ganancia de lazo alta), \( |S|\approx 1/|L|\ll 1 \). El mismo error del 10% en \( G \) ahora produce solo \( |S|\times 10\% \) en \( T \). **La retroalimentación reduce el efecto de la incertidumbre en la planta exactamente en el factor \( |S| \).**

**Ejemplo numérico.** Con \( L=10 \) a cierta frecuencia: \( |S|=1/11\approx 0.09 \). Una variación del 10% en \( G \) produce una variación de apenas \( 0.9\% \) en \( T \). Con \( L=100 \): \( |S|\approx 0.01 \), y la variación en \( T \) es \( 0.1\% \). La retroalimentación compra robustez a cambio de un sistema más complejo (que puede inestabilizarse si la ganancia se diseña mal).

**El módulo de sensibilidad \( M_s = \max_\omega |S(j\omega)| \)** cuantifica la robustez globalmente. Si \( M_s < 2 \) el sistema puede tolerar variaciones de planta del orden de \( 1/M_s > 50\% \) antes de inestabilizarse. Valores \( M_s > 2 \) indican diseño frágil.

## 6 — Realimentación integral: por qué el PI elimina el error en régimen

**El integrador como polo en el origen.**
Un controlador PI tiene la forma \( C(s)=K_p + K_i/s = (K_p s + K_i)/s \). El polo en \( s=0 \) hace que \( |C(j\omega)|\to\infty \) cuando \( \omega\to 0 \), y por tanto:
$$ |L(j0)| = |C(j0)G(j0)| = \infty \;\Longrightarrow\; S(0) = \frac{1}{1+L(0)} = 0 $$
El error en régimen ante cualquier referencia o perturbación con componente DC es entonces:
$$ e_{ss} = \lim_{s\to 0} s\,S(s)\,R(s) = \lim_{s\to 0}\frac{s\,R(s)}{1+L(s)} $$
Para un escalón \( R(s)=1/s \): el \( s \) cancela, y \( 1+L(s)\to\infty \) → \( e_{ss}=0 \).

**La "clase" del sistema — cada integrador sube un nivel.**
Se define el **tipo** (o clase) del sistema como el número de integradores \( 1/s \) en la ganancia de lazo:

| Tipo | Integradores | Error ante escalón | Error ante rampa |
|---|---|---|---|
| 0 | 0 | \( \neq 0 \) (error constante) | \( \infty \) |
| 1 | 1 | \( 0 \) | \( \neq 0 \) (error constante) |
| 2 | 2 | \( 0 \) | \( 0 \) |

La interpretación física: el integrador "acumula" el error hasta que la planta lo compensa exactamente. Si hay error residual, el integrador sigue acumulando y empujando la salida hacia la referencia. Cuando la salida coincide con la referencia, el error es cero y el integrador deja de acumular — es el único punto de equilibrio del lazo con integrador.

**Por qué "clase 0" tiene error ante escalón.**
Sin integrador, \( L(0)=K_p \) finito. El error en régimen ante escalón es \( e_{ss}=1/(1+K_p) \). Para reducirlo hay que subir \( K_p \) — pero eso reduce el margen de fase. El integrador resuelve este dilema: anula el error sin comprometer la ganancia a alta frecuencia.

**Costo del integrador: 90° de fase a baja frecuencia.**
Cada integrador aporta −90° de desfase extra a la ganancia de lazo. Esto reduce el margen de fase en 90°, lo que obliga a diseñar el cero del PI suficientemente por debajo de la frecuencia de cruce para recuperar margen. El cero del PI en \( \omega_z = K_i/K_p \) aporta un avance de fase máximo en \( \omega \approx \omega_z \cdot\sqrt{K_p/\omega_z} \) (ver [[controlador-pid]]).

## Cuándo y por qué se usa
Siempre que se quiera precisión y robustez ante incertidumbre: regular tensión, corriente,
velocidad. La práctica totalidad del control de convertidores es en lazo cerrado.

## Procedimiento (genérico)
1. Mide la salida y forma el error \( e = \text{ref} - \text{salida} \).
2. El controlador \( C(s) \) actúa sobre \( e \).
3. Diseña \( C \) para que \( T \) cumpla las especificaciones y el lazo sea estable (márgenes).
4. Verifica robustez (sensibilidad, márgenes).

## Ejemplo de aplicación real
**Problema:** Bus DC con carga CPL (resistencia diferencial negativa \( -R_{neg}=-200\,\Omega \)): el polo del modelo linealizado está en \( s=1/(C\cdot R_{neg})>0 \) (inestable). Diseñar la realimentación mínima para estabilizarlo.

Planta: \( G(s)=1/(Cs-1/R_{neg}) \) con \( C=10\,\text{mF} \). Con realimentación proporcional \( K \), el polo del lazo cerrado es \( p_{cl}=(1/R_{neg}-K)/C \). Para estabilizar: \( K>1/R_{neg}=0.005 \). Con \( K=0.01 \): \( p_{cl}=(−0.005−0.01)/0.01=−1.5\,\text{s}^{-1} \). Sistema estable. En la práctica se implementa como una **resistencia virtual activa**: el control inyecta potencia adicional proporcional a \( \Delta V_{dc} \), emulando una resistencia de amortiguamiento que no disipa calor.

## Ejemplo de código
```python
import control as ct
L = C * G                          # ganancia de lazo abierto
T = ct.feedback(L, 1)              # lazo cerrado con realimentacion unitaria
S = 1 - T                          # identidad S+T=1
Ms = max(abs(S(1j*w)))             # pico de sensibilidad (robustez)
```

## Parámetros y valores típicos
Ganancia de lazo alta en baja frecuencia (buen seguimiento), baja en alta (robustez/ruido).
Pico de sensibilidad \( M_s < 2 \) (6 dB) como criterio de robustez habitual en convertidores.

## Errores comunes
- Subir la ganancia para reducir el error sin mirar la estabilidad (margen de fase).
- Confiar en lazo abierto cuando hay perturbaciones o incertidumbre.
- Olvidar que \( S+T=1 \): intentar hacer \( |S|<1 \) y \( |T|<1 \) simultáneamente es imposible — en un cruce uno debe ser \( >1 \).

## Conceptos relacionados
- [[funcion-transferencia]] · [[controlador-pid]] · [[funciones-sensibilidad]] · [[margenes-estabilidad]] · [[error-regimen-permanente]]

## Referencias
- Aström, Murray, *Feedback Systems*, 2008.
- Ogata, *Ingeniería de Control Moderna*.
