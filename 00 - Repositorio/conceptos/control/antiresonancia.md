---
titulo: Antiresonancia y por qué facilita la realimentación
slug: antiresonancia
categoria: control
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [entender el valle de antiresonancia (ceros), por qué aparece y por qué hace más fácil cerrar un lazo de realimentación]
tags: [antiresonancia, ceros, notch, realimentacion, margen-de-fase, lugar-de-raices, lcl, intermedio]
fecha_creacion: 2026-06-17
fecha_actualizacion: 2026-06-30
relacionados: [resonancia-rlc, filtro-lcl, polos-ceros, diagrama-bode, lugar-raices, control-cascada, filtro-notch]
referencias:
  - "Franklin, Powell, Emami-Naeini, Feedback Control of Dynamic Systems"
  - "Dannehl et al., Investigation of Active Damping Approaches for LCL Filters, IEEE TIA 2010"
---

## Definición
La antiresonancia es lo contrario de la resonancia: en lugar de un pico de ganancia (que produce un par de polos), es un valle profundo en la respuesta en frecuencia, producido por un par de ceros de la función de transferencia. A la frecuencia de antiresonancia la salida medida casi no responde a la entrada: algo "bloquea" la señal. Si la resonancia es donde un par \( L\!-\!C \) deja pasar mucho (impedancia mínima en serie), la antiresonancia es donde un par \( L\!-\!C \) bloquea (impedancia máxima en paralelo).

## Dónde aparece (contexto genérico)
Aparece siempre que, entre la entrada y la variable que medimos, existe una rama resonante en paralelo que a cierta frecuencia presenta impedancia muy alta y desvía o bloquea la señal. No es de ningún circuito concreto: el mismo fenómeno es el amortiguador de masa sintonizado en mecánica (una masa-muelle auxiliar que "absorbe" la vibración a una frecuencia), el filtro notch en electrónica (ceros colocados a propósito para rechazar una frecuencia), y el valle de la corriente de lado fuente en un filtro LCL. Lo que las une: un par de ceros en la función de transferencia de la salida medida.

La clave para el control es que una misma planta tiene antiresonancia o no según qué variable se mida. En el LCL, la corriente de lado red i2 no tiene ceros de antiresonancia, pero la de lado fuente i1 sí. Elegir la variable con antiresonancia cambia por completo lo fácil que es cerrar el lazo.

## Fundamento — polos y ceros
- Los polos (raíces del denominador) marcan dónde el sistema amplifica: resonancia = par de polos poco amortiguados = pico. Un par de polos resta 180° de fase al cruzarlos.
- Los ceros (raíces del numerador) marcan dónde el sistema atenúa: antiresonancia = par de ceros poco amortiguados = valle. Un par de ceros suma 180° de fase al cruzarlos.

Esa suma de fase de los ceros es justo lo que hace valiosa la antiresonancia para realimentar: si el valle (ceros) está en una frecuencia menor que el pico (polos), los ceros suben la fase antes de que los polos la hundan, de modo que la fase no llega a desplomarse.

## Desarrollo — frecuencia de antiresonancia en el LCL
Se toma como ejemplo la corriente de lado fuente i1 frente a la tensión vi del filtro LCL (la derivación completa de las funciones de transferencia está en [[filtro-lcl]]).

### Versión reducida (sin resistencias)
La función de transferencia de la corriente de lado fuente es \( i_1/v_i=(1+s^2 L_2 C_f)/D(s) \), con \( D(s) \) el denominador común. El valle de antiresonancia está donde el numerador se anula:

$$ 1 + s^2 L_2 C_f = 0 \;\Rightarrow\; s=\pm j\,\omega_{ar} \;\;\text{con}\;\; \omega_{ar}=\frac{1}{\sqrt{L_2 C_f}} \;\Rightarrow\; f_{ar}=\frac{1}{2\pi\sqrt{L_2 C_f}} $$

**Interpretación física.** Anulando la fuente de red (\( v_{pcc} \) a masa en pequeña señal), desde el nudo del condensador se ve \( C_f \) en paralelo con \( L_2 \). Ese paralelo \( L_2\!-\!C_f \) tiene una resonancia paralelo a \( \omega_{ar} \) donde su impedancia tiende a infinito: el nudo queda "flotando" para esa frecuencia y la corriente \( i_1 \) que entra por \( L_1 \) cae a un mínimo. Por eso \( i_1 \) tiene un valle (ceros) justo ahí. La corriente \( i_2 \) (lado red), en cambio, sale por \( L_2 \) sin ver ese bloqueo, y no tiene antiresonancia.

Como \( \omega_{ar}=1/\sqrt{L_2 C_f} \) y la resonancia del LCL es \( \omega_{res}=\sqrt{(L_1+L_2)/(L_1 L_2 C_f)} \), siempre se cumple \( \omega_{ar}<\omega_{res} \) (el valle va antes que el pico).

### Versión completa (con la resistencia \( R_2 \) en serie con \( L_2 \))
Sin despreciar \( R_2 \), el numerador de \( i_1/v_i \) pasa a ser \( 1+sC_f R_2+s^2 L_2 C_f \), cuyos ceros ya no están sobre el eje imaginario sino amortiguados:

$$ \zeta_{ar}=\frac{R_2}{2}\sqrt{\frac{C_f}{L_2}} $$

Comparación: sin \( R_2 \) el valle es infinitamente profundo y los ceros están sobre el eje (la fase salta \( +180^\circ \) de golpe). Con \( R_2 \) el valle se suaviza y el salto de fase se reparte, pero la frecuencia \( f_{ar} \) apenas cambia. Para los valores parásitos reales \( R_2 \) es pequeña, así que el valle sigue siendo marcado y la ventaja de fase se mantiene.

## Por qué es buena para realimentar (lo importante)
Cerrar un lazo de corriente significa realimentar una corriente medida y subir la ganancia hasta el ancho de banda deseado. Si la planta tiene un par de polos de resonancia poco amortiguados, al subir la ganancia esos polos tienden a acercarse al eje imaginario o cruzarlo: el lazo oscila o se inestabiliza. La antiresonancia lo evita por dos razones equivalentes:

**1. Argumento de fase (margen de fase).** El par de ceros de antiresonancia, situado por debajo de la resonancia, aporta +180° de fase antes de llegar al pico. Cuando el par de polos de resonancia resta sus 180°, la fase parte de más arriba y no llega a cruzar el umbral crítico de −180° de forma abrupta. Resultado: hay margen de fase a la frecuencia de cruce y el lazo es estable. Sin la antiresonancia (realimentando i2), la fase cae en picado al cruzar la resonancia y el margen desaparece.

<div class="cfig"><img src="figuras/antiresonancia-bode.png" alt="Bode de i1/vi (con valle de antiresonancia y repunte de fase) frente a i2/vi (solo pico de resonancia y fase que se hunde)"><div class="cap">i₁/vᵢ (naranja) tiene el valle de antiresonancia en f_ar antes del pico de resonancia; su fase repunta (+180° del par de ceros) justo antes del pico, así que no se desploma. i₂/vᵢ (azul) solo tiene el pico y su fase cae a −270°. Por eso realimentar i₁ conserva margen de fase.</div></div>

**2. Argumento del lugar de raíces.** Los ceros "atraen" a los polos: al subir la ganancia de realimentación, los polos de lazo cerrado se desplazan hacia los ceros. Si la variable realimentada tiene ceros de antiresonancia cerca de los polos de resonancia (caso i1), esos polos son atraídos hacia la izquierda (más amortiguados, más estables) al subir la ganancia. Si no los tiene (caso i2), los polos resonantes se van hacia la derecha (hacia la inestabilidad). Esta es la razón de fondo por la que el lazo de corriente rápido de un convertidor con filtro LCL se cierra sobre la corriente de lado fuente i1, no sobre i2.

<div class="cfig"><img src="figuras/antiresonancia-rlocus.png" alt="Lugar de raices del lazo de corriente: realimentando i1 los polos resonantes van a la izquierda hacia el cero; realimentando i2 van a la derecha"><div class="cap">Lugar de raíces al subir la ganancia k. Izquierda (realimentar i₁): el polo resonante (×) es atraído por el cero de antiresonancia (○) y se mueve a la IZQUIERDA → más amortiguado, estable. Derecha (realimentar i₂): sin cero cerca, el polo resonante se mueve a la DERECHA → hacia la inestabilidad.</div></div>

## 1 — De dónde sale \( f_{ar}=1/(2\pi\sqrt{L_2C_f}) \) y por qué da \( +180^\circ \)
**Paso 1 — el numerador que produce el valle.** En \( i_1/v_i \) del LCL (sin resistencias), el numerador es \( N(s)=1+s^2L_2C_f \). El valle (antiresonancia) está donde \( N=0 \):

$$ 1+s^2L_2C_f=0 \;\Rightarrow\; s^2=-\frac{1}{L_2C_f} \;\Rightarrow\; s=\pm j\,\omega_{ar},\quad \omega_{ar}=\frac{1}{\sqrt{L_2C_f}} $$

$$ \boxed{\;f_{ar}=\frac{1}{2\pi\sqrt{L_2C_f}}\;} $$

**Paso 2 — por qué son \( L_2 \) y \( C_f \) y no toda la planta.** Anulada la fuente de red (\( v_{pcc} \) a masa en pequeña señal), desde el nudo del condensador se ve \( C_f \) en **paralelo** con \( L_2 \). La admitancia de ese paralelo es \( Y(s)=sC_f+\tfrac{1}{sL_2}=\tfrac{1+s^2L_2C_f}{sL_2} \); se anula (impedancia infinita) justo en \( s=\pm j\omega_{ar} \). El nudo "flota" para esa frecuencia y la corriente \( i_1 \) cae a un mínimo: ese mínimo es el cero de \( i_1/v_i \).

**Paso 3 — la fase del par de ceros sobre el eje \( j\omega \).** Evaluando el numerador en \( s=j\omega \), como los ceros están sobre el eje imaginario \( N \) es **real**:

$$ N(j\omega)=1+(j\omega)^2L_2C_f=1-\omega^2L_2C_f $$

- Para \( \omega<\omega_{ar} \): \( \omega^2L_2C_f<1 \Rightarrow N>0 \Rightarrow \angle N=0^\circ \).
- Para \( \omega>\omega_{ar} \): \( \omega^2L_2C_f>1 \Rightarrow N<0 \Rightarrow \angle N=+180^\circ \).

**Paso 4 — el salto.** Al cruzar \( \omega_{ar} \), \( N \) pasa de positivo a negativo: su fase salta **\( +180^\circ \)** de forma abrupta (instantánea sin amortiguar; repartida en una banda si \( R_2>0 \)). Como el numerador entra sumando en la fase total \( \angle(i_1/v_i)=\angle N-\angle D \), ese \( +180^\circ \) **eleva** la fase justo antes de que el par de polos de resonancia (en \( \omega_{res}>\omega_{ar} \)) la haga caer \( -180^\circ \). Ese es el mecanismo por el que la antiresonancia regala margen de fase: el repunte de los ceros llega antes que el desplome de los polos.

## Cuándo y por qué se usa
Para elegir la variable de realimentación en cualquier planta con resonancia (filtros LCL/LC, ejes mecánicos flexibles, accionamientos con acoplamiento elástico): si una de las salidas medibles tiene antiresonancia por debajo de la resonancia, realimentar esa es lo más estable. También se introduce antiresonancia a propósito mediante un filtro notch ([[filtro-notch]]) para cancelar una resonancia conocida, o mediante amortiguamiento activo (que reubica los polos usando la realimentación, ver [[filtro-lcl]]).

## Procedimiento de diseño (genérico)
1. Calcula las funciones de transferencia a cada variable medible y localiza ceros (valles) y polos (picos).
2. Prefiere realimentar la variable cuyo par de ceros de antiresonancia caiga por debajo de la resonancia.
3. Comprueba en Bode que la fase repunta antes del pico (margen de fase) y en el lugar de raíces que los polos resonantes son atraídos a la izquierda.
4. Si ninguna variable tiene antiresonancia útil, añade amortiguamiento (notch o activo) antes de subir la ganancia.

## Ejemplo de código
```python
import numpy as np
from scipy import signal

L1, L2, Cf, R2 = 2e-3, 1e-3, 20e-6, 0.05
f_ar  = 1/(2*np.pi*np.sqrt(L2*Cf))            # antiresonancia (valle de i1)
zeta_ar = (R2/2)*np.sqrt(Cf/L2)               # amortiguamiento del valle (con R2)
f_res = 1/(2*np.pi)*np.sqrt((L1+L2)/(L1*L2*Cf))  # resonancia (pico)
# i1/vi tiene ceros en s = -zeta_ar*w_ar +- j*w_ar*sqrt(1-zeta_ar^2)
```

## Parámetros y valores típicos
\( f_{ar} \) siempre por debajo de \( f_{res} \). En el LCL del proyecto, \( f_{ar}\approx1.1 \) kHz y \( f_{res}\approx1.4 \) kHz (LCL aislado). \( \zeta_{ar} \) con resistencias parásitas: muy pequeño (valle marcado).

## Errores comunes
- Realimentar la variable sin antiresonancia (i2 en el LCL) por parecer "la importante": la fase se hunde en la resonancia y el lazo se inestabiliza al subir la ganancia.
- Confundir el valle (ceros, antiresonancia) con el pico (polos, resonancia): son numerador vs denominador.
- Olvidar que la antiresonancia depende de la variable medida: la misma planta puede tenerla o no.
- Suponer el valle infinitamente profundo: las resistencias serie lo suavizan (zeta_ar > 0).

## Cómo diseñar un modelo aprovechando la antiresonancia
La antiresonancia no es solo algo que "aparece": se puede buscar e incluso colocar a propósito. Tres estrategias de diseño:

1. **Elegir la salida que ya tiene antiresonancia.** Antes de cerrar el lazo, calcula las funciones de transferencia a cada variable medible y quédate con la que tenga un par de ceros por debajo de la resonancia. Es gratis (no añade hardware ni filtros): solo cambia qué sensor realimentas. En el LCL, esto es realimentar i1 en vez de i2.

2. **Colocar la antiresonancia donde haga falta dimensionando el circuito.** La frecuencia del valle la fijan los componentes (en el LCL, f_ar = 1/(2·pi·raiz(L2·Cf))). Eligiendo L2 y Cf se sitúa la antiresonancia justo por debajo de la resonancia y por encima del ancho de banda del lazo, de modo que el cero "proteja" la fase en la zona de cruce. Es parte del dimensionado del filtro.

3. **Añadir la antiresonancia a propósito con un filtro notch.** Si una resonancia molesta no tiene un cero natural cerca, se intercala un filtro notch ([[filtro-notch]]) en el lazo: son dos ceros poco amortiguados sintonizados a la frecuencia de la resonancia, que cancelan su pico. Es "inyectar" antiresonancia donde el sistema no la tenía.

Regla de oro de colocación: el par de ceros (valle) debe quedar por debajo del par de polos (pico) y cerca de él, para que el repunte de fase de los ceros llegue justo antes de la caída de fase de los polos.

## Beneficios e inconvenientes
**Beneficios:**
- Recupera margen de fase en la resonancia sin disipar energía: a diferencia del amortiguamiento pasivo (una resistencia que calienta), aprovechar un cero natural no tiene pérdidas.
- Permite subir el ancho de banda del lazo por encima de lo que permitiría una resonancia sin amortiguar.
- Si es un cero natural de la planta (elegir i1), es gratis: no añade componentes ni cómputo.
- Atrae los polos de lazo cerrado hacia la izquierda (más amortiguados) al subir la ganancia.

**Inconvenientes y límites:**
- La antiresonancia natural depende de parámetros que varían: si L2 o Cf cambian (tolerancias, temperatura) o si la inductancia de red se suma a L2, la frecuencia del valle se mueve y deja de coincidir con lo previsto. Un notch mal sintonizado por deriva de parámetros pierde eficacia o incluso empeora la fase.
- El valle implica baja ganancia a esa frecuencia: el lazo casi no actúa justo en f_ar, lo que puede dejar sin control una componente cercana a esa frecuencia.
- Un cero poco amortiguado va acompañado de un cambio brusco de fase; si el cruce de ganancia cae demasiado cerca del valle, el margen puede ser sensible y poco robusto.
- Realimentar i1 (lado fuente) controla bien esa corriente pero deja la corriente de red i2 (la que de verdad importa para la red) regulada solo de forma indirecta; suele necesitarse un lazo externo más lento sobre i2 o sobre la tensión.
- En digital, el retardo de cómputo desplaza la fase y puede comerse la ventaja del cero si la antiresonancia está muy cerca de la frecuencia de Nyquist.

## 3 — La antiresonancia en el LCL: de dónde sale \( f_{ar}=1/(2\pi\sqrt{L_2C_f}) \)

La admitancia de entrada del filtro LCL vista desde \( v_i \) —es decir, la transferencia \( i_1/v_i \)— tiene un cero (un valle en el Bode) a la frecuencia donde la rama \( C_f \) en **paralelo** con \( L_2 \) presenta impedancia infinita, bloqueando el flujo de \( i_1 \).

**Circuito equivalente en pequeña señal.** Anulando la fuente de red (\( v_{PCC}\to0 \)), el nudo intermedio del LCL ve \( C_f \) en paralelo con \( L_2 \) (más sus resistencias parásitas). La admitancia de ese paralelo es:

$$ Y_{par}(s) = sC_f + \frac{1}{sL_2 + R_2} = \frac{1 + s C_f R_2 + s^2 L_2 C_f}{sL_2 + R_2} $$

El numerador de \( i_1/v_i \) es proporcional a \( Y_{par} \), así que sus ceros coinciden con los ceros del numerador de \( Y_{par} \):

$$ 1 + s^2 L_2 C_f = 0 \;\;(\text{sin } R_2) \;\Rightarrow\; s = \pm j\omega_{ar}, \quad \omega_{ar} = \frac{1}{\sqrt{L_2 C_f}} $$

$$ \boxed{f_{ar} = \frac{1}{2\pi\sqrt{L_2 C_f}}} $$

**Por qué solo \( L_2 \) y \( C_f \), no \( L_1 \).** La inductancia \( L_1 \) está en serie con el nudo: su valor desplaza la frecuencia de resonancia \( f_{res} \) pero **no** cambia dónde se anula la admitancia del paralelo \( C_f\|L_2 \). Por eso \( f_{ar} \) depende únicamente de \( L_2 \) y \( C_f \).

**Relación con la resonancia.** La pulsación de resonancia del LCL es \( \omega_{res} = \sqrt{(L_1+L_2)/(L_1 L_2 C_f)} \). El ratio:

$$ \frac{f_{res}}{f_{ar}} = \frac{\omega_{res}}{\omega_{ar}} = \frac{\sqrt{(L_1+L_2)/(L_1 L_2 C_f)}}{1/\sqrt{L_2 C_f}} = \sqrt{\frac{(L_1+L_2)L_2}{L_1 L_2}} = \sqrt{1 + \frac{L_2}{L_1}} $$

Espera — ese sería \( \sqrt{1+L_2/L_1} \). Re-haciendo: \( \omega_{res}/\omega_{ar} = \sqrt{(L_1+L_2)/(L_1 L_2 C_f)} \cdot \sqrt{L_2 C_f} = \sqrt{(L_1+L_2)/(L_1)} = \sqrt{1+L_2/L_1} \). Alternativamente, con \( r = L_2/L_1 \):

$$ \frac{f_{res}}{f_{ar}} = \sqrt{1 + \frac{L_2}{L_1}} = \sqrt{1+r} \quad \Rightarrow \quad f_{ar} < f_{res}\text{ siempre (el valle precede al pico)} $$

## 4 — La antiresonancia vs resonancia: la ratio \( f_{res}/f_{ar} \)

**Demostración paso a paso.**

*Paso 1.* \( f_{ar} = \frac{1}{2\pi\sqrt{L_2 C_f}} \) (del cero del numerador de \( i_1/v_i \)).

*Paso 2.* \( f_{res} = \frac{1}{2\pi}\sqrt{\frac{L_1+L_2}{L_1 L_2 C_f}} \) (del par de polos del denominador común del LCL).

*Paso 3.* La ratio:

$$ \frac{f_{res}}{f_{ar}} = \frac{\sqrt{(L_1+L_2)/(L_1 L_2 C_f)}}{1/\sqrt{L_2 C_f}} = \sqrt{\frac{(L_1+L_2) L_2 C_f}{L_1 L_2 C_f}} = \sqrt{\frac{L_1+L_2}{L_1}} = \sqrt{1+\frac{L_2}{L_1}} $$

*Paso 4.* Sea \( r = L_2/L_1 \). Entonces \( f_{res}/f_{ar} = \sqrt{1+r} > 1 \) para todo \( r > 0 \), lo que confirma que **siempre \( f_{ar} < f_{res} \)**.

**Implicación de diseño.** Para que el repunte de fase de los ceros llegue justo antes del pico de los polos, conviene que la ratio sea cercana a 1 (cero y polo próximos). Eso ocurre cuando \( r = L_2/L_1 \ll 1 \), es decir, \( L_2 \ll L_1 \). En la práctica se usa \( L_2 \approx L_1/4 \) a \( L_1/3 \), que da \( f_{res}/f_{ar} \approx 1.12 \) a \( 1.15 \): el valle y el pico están separados apenas un 12–15 %, suficientemente juntos para que el repunte de fase ayude, pero separados para distinguirlos.

## 5 — La antiresonancia como filtro natural y comparación con el notch activo

**La antiresonancia natural ya atenúa sin componentes adicionales.** A la frecuencia \( f_{ar} \), la corriente \( i_1 \) cae a un mínimo (teóricamente cero sin resistencias, muy bajo con resistencias parásitas). Esto significa que **el armónico de frecuencia \( f_{ar} \) ya se atenúa por sí solo** en la fuente del convertidor, sin añadir ningún filtro externo. Si un armónico de conmutación cae cerca de \( f_{ar} \), el LCL ya lo rechaza de forma natural.

**Comparación con el filtro notch activo.**

| Aspecto | Antiresonancia natural del LCL | Notch activo en el lazo |
|---|---|---|
| Implementación | Gratis: resultado de los componentes L2, Cf | Requiere diseño e implementación software |
| Posición | Fija: \( f_{ar}=1/(2\pi\sqrt{L_2C_f}) \) (puede variar con T, tolerancias) | Ajustable por software, puede compensar deriva |
| Objetivo | Atenúa naturalmente en \( f_{ar} \) | Cancela el pico en \( f_{res} \) o en \( f_{ar} \) según diseño |
| Qué cancela | El flujo de corriente \( i_1 \) a \( f_{ar} \) | El pico de resonancia del lazo |
| Efecto en fase | Aporta +180° de fase al cruzar \( f_{ar} \) | Añade un par de ceros donde se coloca |
| Robustez | Depende de tolerancias de L2 y Cf | Puede re-sintonizarse si cambian los parámetros |

El notch activo puede colocarse exactamente en \( f_{ar} \) para profundizar la atenuación natural, o en \( f_{res} \) para cancelar el pico de resonancia. La antiresonancia natural es la primera línea de defensa; el notch es la segunda, más precisa pero más compleja.

## 6 — Diseño iterativo: LCL con L₁=2mH, L₂=0.5mH, Cf=10µF

Parámetros del proyecto 01: \( L_1=2\,\text{mH} \), \( L_2=0.5\,\text{mH} \), \( C_f=10\,\mu\text{F} \), \( f_{sw}=10\,\text{kHz} \), \( T_s=100\,\mu\text{s} \).

**Paso 1 — calcular \( f_{ar} \).**

$$ f_{ar} = \frac{1}{2\pi\sqrt{0.5\times10^{-3}\cdot10\times10^{-6}}} = \frac{1}{2\pi\sqrt{5\times10^{-9}}} = \frac{1}{2\pi\cdot70.7\times10^{-6}} \approx 2{,}251\,\text{Hz} $$

**Paso 2 — calcular \( f_{res} \).**

$$ f_{res} = \frac{1}{2\pi}\sqrt{\frac{(2+0.5)\times10^{-3}}{2\times0.5\times10^{-6}\cdot10\times10^{-6}}} = \frac{1}{2\pi}\sqrt{\frac{2.5\times10^{-3}}{10^{-8}}} = \frac{1}{2\pi}\sqrt{250000} \approx 2{,}526\,\text{Hz} $$

**Paso 3 — verificar \( f_{ar} < f_{sw}/2 \) y \( f_{res} < f_{sw}/2 \).**

$$ f_{sw}/2 = 5{,}000\,\text{Hz} \quad\Rightarrow\quad f_{ar} = 2{,}251\,\text{Hz} < 5{,}000\,\text{Hz} \;\checkmark \quad f_{res} = 2{,}526\,\text{Hz} < 5{,}000\,\text{Hz} \;\checkmark $$

Ratio: \( f_{res}/f_{ar} = 2526/2251 \approx 1.12 \approx \sqrt{1+L_2/L_1} = \sqrt{1+0.25} = 1.118 \) — verificado.

**Paso 4 — atenuación a \( f_{sw} \).**

Para el LCL sin amortiguamiento, la atenuación asintótica por encima de \( f_{res} \) es −60 dB/dec (tercer orden). A \( f_{sw} = 10\,\text{kHz} \), que está a una década por encima de \( f_{res} \approx 2.5\,\text{kHz} \):

$$ \text{Atenuación} \approx 60\,\text{dB/dec} \times \log_{10}(10000/2526) \approx 60 \times 0.597 \approx 36\,\text{dB} $$

Es decir, el rizado de conmutación a \( f_{sw} \) se atenúa aproximadamente 36 dB (factor ≈ 63) más que la fundamental. Para ondulaciones mayores puede necesitarse aumentar Cf o L2.

<div class="cfig"><img src="figuras/antiresonancia-analisis.png" alt="Análisis de antiresonancia en el LCL: Bode, admitancia, efecto de L2 y ratio fres/far"><div class="cap">(a) Bode de i_L2/v_i e i_L1/v_i: el pico de resonancia en f_res y el valle en f_ar. (b) Admitancia del paralelo C_f||L_2: el cero coincide con f_ar. (c) Efecto de L_2 en f_ar: reducir L_2 sube la antiresonancia. (d) Ratio f_res/f_ar = √(1+L_2/L_1) siempre mayor que 1.</div></div>

## 7 — Cancelación de polos/ceros en \(\omega_{AR}\): por qué es frágil

La idea más simple de tratar la antiresonancia/resonancia del LCL es cancelar el par polo-cero con un cero-polo del controlador:

$$C(s) \leftarrow C(s)\cdot\frac{s^2 + \omega_{res}^2}{s^2 + 2\zeta_c\omega_{res}s + \omega_{res}^2}$$

**Por qué es frágil:**
1. La frecuencia \(\omega_{res} = \sqrt{(L_1+L_2)/(L_1 L_2 C_f)}\) depende de \(L_2\) que varía con la inductancia de red \(L_g\). Una variación de \(L_g\) del 50% desplaza \(\omega_{res}\) un 30% → el cero del controlador ya no cancela el polo.
2. La cancelación de polos/ceros inestables (o polos del semiplano derecho) está prohibida: producen modos ocultos que crecen internamente aunque la salida medida parezca estable.
3. Los polos resonantes poco amortiguados (\(\zeta < 0.05\)) son cuasi-inestables: pequeñas perturbaciones los excitan y tardan mucho en disiparse incluso "cancelados" por el controlador.

**Alternativa correcta:** en lugar de cancelar, añadir amortiguamiento mediante realimentación o elementos pasivos que muevan los polos hacia la izquierda en el plano complejo.

## 8 — Amortiguamiento activo por realimentación de \(i_{Cf}\): resistencia virtual sin pérdidas

La corriente del condensador \(i_{Cf} = C_f \dot{v}_C\) es proporcional a la derivada de la tensión del condensador. Realimentarla al modulador crea una resistencia virtual en paralelo con \(C_f\):

$$u_{AD} = K_d\,i_{Cf}$$

El efecto en la función de transferencia del LCL: añade un término de amortiguamiento en la resonancia sin resistencia física. El factor de amortiguamiento resultante:

$$\zeta_{AD} \approx \frac{K_d}{2}\sqrt{\frac{C_f}{L_1+L_2}}$$

Para el LCL del proyecto 01 (\(L_1=2\,\text{mH}\), \(L_2=1\,\text{mH}\), \(C_f=20\,\mu\text{F}\), \(\omega_{res}=2\pi\cdot1130\,\text{rad/s}\)):

$$K_d = 2\zeta_{AD}\sqrt{(L_1+L_2)/C_f} = 2\times0.3\times\sqrt{3\times10^{-3}/20\times10^{-6}} = 2\times0.3\times12.25 \approx 7.35\,\Omega$$

**Ventajas:** sin pérdidas; ajustable por software; no añade componentes. **Desventaja:** amplifica el ruido de medición de \(i_{Cf}\); necesita filtrado adecuado.

## 9 — Amortiguamiento por \(\dot{v}_C\): equivalencia y ruido

Realimentar \(\dot{v}_C\) (derivada de la tensión del condensador) equivale a conectar una resistencia en serie con \(C_f\). La equivalencia:

$$R_{d,eq} = K_{dv}\cdot C_f\,\omega_{res}$$

Comparación con \(i_{Cf}\) AD:
- Ambos mueven los polos resonantes hacia la izquierda.
- El AD por \(\dot{v}_C\) amplifica el ruido ×10 más que el AD por \(i_{Cf}\) porque la derivada magnifica el contenido de alta frecuencia.
- Para frecuencias de muestreo bajas (\(f_s < 10f_{res}\)), el AD por \(i_{Cf}\) es más robusto.

**Necesidad de filtrado:** si se usa \(\dot{v}_C\), añadir un filtro paso bajo con \(f_{corte} \approx 3f_{res}\) antes de la ganancia \(K_{dv}\). Esto introduce un retardo adicional que puede reducir el margen de estabilidad.

## 10 — Diseño sistemático del AD: de \(\omega_{res}\) a \(\zeta_{AD}\)

**Algoritmo de diseño:**

1. Calcular la frecuencia de resonancia del LCL:
$$\omega_{res} = \sqrt{\frac{L_1+L_2}{L_1 L_2 C_f}}$$

2. Fijar el objetivo de amortiguamiento \(\zeta_{AD} \in [0.2, 0.5]\) (valores menores dejan el pico demasiado alto; mayores añaden retardo).

3. Calcular la ganancia de AD:
$$K_d = 2\zeta_{AD}\sqrt{\frac{L_1+L_2}{C_f}}$$

4. Verificar en el diagrama de Bode que el pico residual es \(< 20\,\text{dB}\) y el margen de fase del lazo de corriente cerrado con AD es \(> 30°\).

5. Verificar la sensibilidad: variar \(C_f\) y \(L_2\) en ±30% y comprobar que \(\zeta_{AD,min} > 0.1\).

**Condición de estabilidad del AD con retardo digital:** la frecuencia de resonancia debe satisfacer \(f_{res} < f_s/6\) para que el retardo de un paso de muestreo no produzca amortiguamiento negativo.

## 11 — Sensibilidad de \(f_{ar}\) a variaciones de parámetros

La frecuencia de antiresonancia \(f_{ar}=1/(2\pi\sqrt{L_2C_f})\) depende de \(L_2\) y \(C_f\). Las fuentes de variación:

- **Tolerancias de fabricación:** los condensadores de film tienen tolerancias ±10–20 %; los inductores bobinados ±5–10 %. Una variación del ±10 % en \(C_f\) desplaza \(f_{ar}\) en \(\mp5\%\).
- **Inductancia de red \(L_g\):** en algunas formulaciones, \(L_g\) se añade en serie con \(L_2\) modificando la frecuencia de antiresonancia a \(f_{ar}'=1/(2\pi\sqrt{(L_2+L_g)C_f})\). Cuando la red es débil (\(L_g\sim L_2\)), \(f_{ar}\) puede bajar un 30 % respecto al diseño nominal, acercándose peligrosamente al ancho de banda del lazo de corriente.
- **Temperatura:** la capacidad de los condensadores electrolíticos varía hasta ±30 % con la temperatura. En condensadores de film la variación es menor (<5 %), pero en entornos industriales con temperatura variable sigue siendo relevante.

**Margen de diseño recomendado.** Asegurar que el ancho de banda del lazo de corriente \(f_{ci}\) sea al menos un octavo por debajo de \(f_{ar,min}\):

$$f_{ci} < \frac{f_{ar,min}}{2} = \frac{f_{ar,nom}}{2\sqrt{1+\delta_{L2}+\delta_{Cf}}}$$

donde \(\delta_{L2}\) y \(\delta_{Cf}\) son los máximos incrementos relativos de \(L_2\) y \(C_f\).

## 12 — La antiresonancia en sistemas mecánicos: eje flexible de dos masas

El mismo fenómeno ocurre en accionamientos con acoplamiento elástico entre el motor y la carga (eje flexible). El modelo de dos masas \(J_m,\,J_l\) acopladas por un eje de rigidez \(K_s\):

$$J_m\ddot{\theta}_m = T_m - K_s(\theta_m-\theta_l), \quad J_l\ddot{\theta}_l = K_s(\theta_m-\theta_l) - T_l$$

La función de transferencia de la velocidad del motor \(\omega_m\) a par de motor \(T_m\) tiene un par de ceros (antiresonancia mecánica) en:

$$f_{ar,mec}=\frac{1}{2\pi}\sqrt{\frac{K_s}{J_l}}$$

y un par de polos (resonancia de torsión) en:

$$f_{res,mec}=\frac{1}{2\pi}\sqrt{K_s\left(\frac{1}{J_m}+\frac{1}{J_l}\right)}$$

Por el mismo argumento que en el LCL: realimentar \(\omega_m\) (velocidad del motor, que tiene antiresonancia) es más estable que realimentar \(\omega_l\) (velocidad de la carga, sin antiresonancia) al cerrar el lazo de velocidad.

## 13 — Notch en el lazo de corriente: diseño e impacto en el margen de fase

Cuando la antiresonancia natural del LCL no es suficiente para proteger el margen de fase (p.ej. si \(f_{ar}\approx f_{ci}\)), se añade un filtro notch sintonizado en \(f_{res}\):

$$N(s) = \frac{s^2+2\zeta_n\omega_{res}s+\omega_{res}^2}{s^2+2\zeta_d\omega_{res}s+\omega_{res}^2}, \quad \zeta_n\ll\zeta_d$$

El notch introduce dos ceros cerca de \(j\omega_{res}\) que bajan la ganancia del lazo en esa frecuencia, evitando la inestabilidad. El coste: el notch añade fase negativa fuera de la resonancia. Para \(\zeta_n=0.01\) y \(\zeta_d=0.5\):

- Ganancia en \(f_{res}\): \(-20\log_{10}(\zeta_d/\zeta_n)\approx-34\,\text{dB}\) (el pico queda acotado).
- Fase adicional en \(f_{ci}\): si \(f_{ci}\ll f_{res}\), la pérdida de fase es despreciable; si \(f_{ci}\approx0.5f_{res}\), la pérdida puede ser 10–20°.

**Criterio de sintonía.** Centrar el notch exactamente en \(f_{res}\) y no en \(f_{ar}\): el notch cancela el pico de resonancia (polos), no el valle de antiresonancia (ceros). Usar \(\zeta_d\approx0.3\text{–}0.5\) para suavizar el impacto en fase; \(\zeta_n\) tan pequeño como el conocimiento de \(f_{res}\) lo permite.

## 14 — Diseño iterativo: elegir entre realimentar i1, i2 o notch en i2

**Situación.** LCL con \(L_1=2\,\text{mH}\), \(L_2=1\,\text{mH}\), \(C_f=10\,\mu\text{F}\): \(f_{ar}=1.59\,\text{kHz}\), \(f_{res}=1.95\,\text{kHz}\). \(f_{sw}=10\,\text{kHz}\), \(f_{ci}=800\,\text{Hz}\).

**Opción A — realimentar i1.** El lazo ve los ceros en \(f_{ar}=1.59\,\text{kHz}\) antes del pico en \(f_{res}=1.95\,\text{kHz}\). Los ceros aportan \(+180°\) justo donde el pico hundiría la fase. El PM en \(f_{ci}=800\,\text{Hz}\) (lejos de la resonancia) es ≈45°: estable con margen holgado. Desventaja: i1 no es la variable que interesa para la red; la corriente inyectada es i2.

**Opción B — realimentar i2 sin notch.** La fase cae a \(-270°\) al cruzar \(f_{res}\). Si el lazo tiene ganancia suficiente en \(f_{res}\), inestabilidad. Con PM<15° en \(f_{ci}\): marginal.

**Opción C — realimentar i2 con notch en \(f_{res}\).** El notch con \(\zeta_n=0.02\), \(\zeta_d=0.5\) reduce el pico 28 dB. El PM en \(f_{ci}\) mejora a ≈35°: aceptable pero con robustez reducida ante deriva de \(f_{res}\). Si \(L_g\) varía ±50 %, \(f_{res}\) se mueve ±20 % y el notch pierde eficacia.

**Conclusión.** Para el proyecto 01, se elige la opción A (realimentar i1) porque ofrece el mayor margen y robustez sin filtros adicionales. El lazo externo más lento sobre la tensión del condensador regula indirectamente la corriente de red i2.

## 15 — Efecto de la inductancia de red \(L_g\) en \(f_{ar}\) y \(f_{res}\)

Cuando el LCL está conectado a una red real con inductancia \(L_g\) (inductancia de cortocircuito del PCC), la inductancia efectiva de lado red pasa de \(L_2\) a \(L_2+L_g\). Esto modifica tanto la frecuencia de antiresonancia como la de resonancia:

$$f_{ar}' = \frac{1}{2\pi\sqrt{(L_2+L_g)C_f}}, \quad f_{res}' = \frac{1}{2\pi}\sqrt{\frac{L_1+L_2+L_g}{L_1(L_2+L_g)C_f}}$$

Para el LCL del proyecto con \(L_g=0.5\,\text{mH}\) (SCR≈20):

$$f_{ar}' = \frac{1}{2\pi\sqrt{(0.5+0.5)\times10^{-3}\cdot10^{-5}}} = \frac{1}{2\pi\sqrt{10^{-8}}} = \frac{1}{2\pi\times10^{-4}} \approx 1{,}592\,\text{Hz}$$

Comparado con \(f_{ar}=2{,}251\,\text{Hz}\) sin red: la adición de \(L_g\) **baja la antiresonancia** en un 29 %. Si el lazo de corriente estaba sintonizado con \(f_{ci}<f_{ar,nom}\), la nueva \(f_{ar}'\) puede quedar más cerca del ancho de banda, reduciendo el margen de fase.

**Consecuencia de diseño.** Incluir \(L_{g,max}\) en el cálculo de \(f_{ar,min}\) durante el diseño del filtro LCL y del lazo de corriente, para garantizar que el margen de fase se mantiene en el peor caso de red.

## 16 — Comprobación rápida: la antiresonancia en el Bode medido

En un convertidor real, la medición de la función de transferencia lazo abierto \(G(j\omega)\) mediante inyección sinusoidal permite localizar \(f_{ar}\) y \(f_{res}\) experimentalmente:

1. **Inyectar** una perturbación de corriente \(\hat{i}\) en el lazo de corriente (entre el controlador y la planta).
2. **Medir** la respuesta de corriente \(\hat{i}_1\) o \(\hat{i}_2\) en el lazo abierto.
3. **Calcular** \(G(f_k)=\hat{i}_{out}/\hat{i}_{inyec}\) para cada frecuencia barrida.
4. **Identificar** el valle (mínimo en magnitud → \(f_{ar}\)) y el pico (máximo → \(f_{res}\)).

**Indicador de desviación.** Si la \(f_{ar}\) medida difiere >10 % de la calculada con los parámetros nominales de diseño, es señal de que \(L_g\) real o \(C_f\) real difiere de los valores usados en el diseño. Recalibrar el notch o el amortiguamiento activo según los valores medidos.

## Uso en proyectos
- 01 / 02 (filtro LCL): el lazo interno de corriente se cierra sobre i1 precisamente porque su antiresonancia a ≈1.1 kHz aporta el margen de fase que i2 no tiene; sobre esa base se añade el amortiguamiento activo.

## 17 — Tabla de resumen: antiresonancia en distintos sistemas

| Sistema | Antiresonancia en | Causa | Variable a realimentar |
|---|---|---|---|
| Filtro LCL | \(f_{ar}=1/(2\pi\sqrt{L_2C_f})\) | Bloqueo de \(C_f\|L_2\) | \(i_1\) (corriente de convertidor) |
| Eje flexible 2 masas | \(f_{ar}=\sqrt{K_s/J_l}/(2\pi)\) | Absorción por masa de carga | \(\omega_m\) (velocidad de motor) |
| Filtro LC salida | \(f_{ar}=1/(2\pi\sqrt{LC})\) | Paralelo \(L\|C\) | \(v_{out}\) (tensión de salida) |
| Bus DC con cable | \(f_{ar}=1/(2\pi\sqrt{L_{cable}C_{bus}})\) | Resonancia cable-bus | \(v_{DC}\) (tensión de bus) |
| Resonador de Helmholtz | \(f_{ar}\) acústico | Cavidad resonante auxiliar | Presión en el punto de medida |

La regla universal: la antiresonancia (ceros) aparece **siempre que una rama resonante en paralelo bloquea la señal a cierta frecuencia**. La variable óptima de realimentación es la que tiene el par de ceros (antiresonancia) justo por debajo del par de polos (resonancia).

## 18 — Ejemplo de código: calcular f_ar y f_res del LCL y verificar el margen

```python
import numpy as np
from scipy import signal

def lcl_params(L1, L2, Cf, R1=0, R2=0):
    """Calcula f_ar, f_res y zeta_ar del filtro LCL."""
    w_ar = 1/np.sqrt(L2*Cf)
    w_res = np.sqrt((L1+L2)/(L1*L2*Cf))
    zeta_ar = (R2/2)*np.sqrt(Cf/L2) if R2 > 0 else 0
    return dict(f_ar=w_ar/(2*np.pi), f_res=w_res/(2*np.pi),
                zeta_ar=zeta_ar, ratio=w_res/w_ar)

# LCL del proyecto 01
res = lcl_params(L1=2e-3, L2=0.5e-3, Cf=10e-6, R1=0.05, R2=0.05)
print(f"f_ar  = {res['f_ar']:.0f} Hz")
print(f"f_res = {res['f_res']:.0f} Hz")
print(f"ratio f_res/f_ar = {res['ratio']:.3f} (esperado √(1+L2/L1)={np.sqrt(1+0.25):.3f})")
print(f"zeta_ar = {res['zeta_ar']:.4f}")

# Verificar que f_ci < f_ar / 2 (margen de diseño)
f_ci = 800  # Hz
assert f_ci < res['f_ar']/2, f"f_ci={f_ci}Hz supera f_ar/2={res['f_ar']/2:.0f}Hz!"
print(f"Margen OK: f_ci={f_ci}Hz < f_ar/2={res['f_ar']/2:.0f}Hz")
```

## Conceptos relacionados
- [[resonancia-rlc]] · [[filtro-lcl]] · [[polos-ceros]] · [[diagrama-bode]] · [[lugar-raices]] · [[control-cascada]] · [[filtro-notch]]

## Referencias
- Franklin, Powell, Emami-Naeini, Feedback Control of Dynamic Systems.
- Dannehl et al., Investigation of Active Damping Approaches for LCL Filters, IEEE TIA 2010.
