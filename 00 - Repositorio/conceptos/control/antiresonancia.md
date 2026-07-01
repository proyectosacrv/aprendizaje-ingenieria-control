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

## Uso en proyectos
- 01 / 02 (filtro LCL): el lazo interno de corriente se cierra sobre i1 precisamente porque su antiresonancia a ≈1.1 kHz aporta el margen de fase que i2 no tiene; sobre esa base se añade el amortiguamiento activo.

## Conceptos relacionados
- [[resonancia-rlc]] · [[filtro-lcl]] · [[polos-ceros]] · [[diagrama-bode]] · [[lugar-raices]] · [[control-cascada]] · [[filtro-notch]]

## Referencias
- Franklin, Powell, Emami-Naeini, Feedback Control of Dynamic Systems.
- Dannehl et al., Investigation of Active Damping Approaches for LCL Filters, IEEE TIA 2010.
