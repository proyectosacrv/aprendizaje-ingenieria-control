---
titulo: Factor de calidad Q — definición general y relación con ζ
slug: factor-calidad-q
categoria: fisica-modelado
tipo: concepto
nivel: basico
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [entender Q como concepto universal de cualquier resonador de 2º orden y deducir Q=1/(2ζ) y el ancho de banda f0/Q sin referirse a ningún componente concreto]
tags: [factor-calidad, amortiguamiento, resonancia, ancho-de-banda, segundo-orden, basico]
fecha_creacion: 2026-06-27
fecha_actualizacion: 2026-06-27
relacionados: [resonancia-rlc, filtro-lcl, frecuencias-segundo-orden, respuesta-segundo-orden, diagrama-bode, series-taylor]
referencias:
  - "Ogata, Ingeniería de Control Moderna, Pearson"
  - "Franklin, Powell, Emami-Naeini, Feedback Control of Dynamic Systems"
---

## Definición
El factor de calidad \( Q \) mide cuánto "suena" un resonador de segundo orden antes de apagarse, o equivalentemente, cuánto amplifica una excitación cerca de su frecuencia natural. Su definición original es **energética y no depende de qué tipo de sistema sea**:

$$ Q \equiv 2\pi\,\frac{\text{energía almacenada}}{\text{energía disipada por ciclo}} $$

Esta definición vale igual para un circuito RLC, un filtro LCL, una masa-resorte-amortiguador, una cavidad óptica o un péndulo: solo exige que el sistema sea de segundo orden con un mecanismo de pérdida lento frente a la oscilación. \( Q \) no es un parámetro físico independiente: es una forma de expresar el amortiguamiento \( \zeta \) de los polos del sistema.

## Punto de partida — el resonador genérico de 2º orden
Cualquier resonador de 2º orden, sea cual sea su naturaleza física, tiene la misma forma canónica de denominador:

$$ s^2+2\zeta\omega_n s+\omega_n^2=0 $$

con polos complejos (si \( \zeta<1 \)) \( s=-\zeta\omega_n\pm j\omega_d \), \( \omega_d=\omega_n\sqrt{1-\zeta^2} \) (ver [[frecuencias-segundo-orden]]). Toda la derivación de \( Q \) que sigue parte únicamente de esta forma y de la definición energética anterior — en ningún paso se usa una \( R \), una \( L \) o una \( C \) concretas, por eso el resultado es general.

## Desarrollo 1 — de la definición energética a \( Q=1/(2\zeta) \)
**Paso 1 — cómo decae la amplitud.** La respuesta libre de cualquier sistema con esos polos es de la forma

$$ x(t)=A\,e^{-\zeta\omega_n t}\cos(\omega_d t+\varphi) $$

sea \( x \) una corriente, una tensión, una posición o cualquier otra variable de estado. El amortiguamiento se ve en la envolvente \( e^{-\zeta\omega_n t} \).

**Paso 2 — cómo decae la energía.** En cualquier sistema lineal de 2º orden la energía almacenada es proporcional al cuadrado de la amplitud (\( \tfrac12 LI^2 \), \( \tfrac12 kx^2 \), etc.), así que:

$$ E(t)\propto x(t)^2 \;\Rightarrow\; E(t)=E_0\,e^{-2\zeta\omega_n t} $$

el doble del exponente de la amplitud, porque al elevar al cuadrado el exponente se duplica.

**Paso 3 — energía perdida en un periodo.** Un ciclo completo dura \( T_d=2\pi/\omega_d \). La energía perdida entre \( t \) y \( t+T_d \) es:

$$ \Delta E = E(t)-E(t+T_d) = E(t)\left[1-e^{-2\zeta\omega_n T_d}\right] $$

**Paso 4 — aproximar para \( \zeta \) pequeño (son dos aproximaciones, no una).** Este paso suele leerse rápido, pero esconde dos aproximaciones distintas y conviene separarlas para saber qué error comete cada una. Ambas son series de Taylor; el procedimiento general para construirlas (y de dónde sale el error al truncarlas) está en [[series-taylor]].

*Qué son \( \omega_n \) y \( \omega_d \), otra vez.* \( \omega_n \) es la frecuencia natural: la que tendría el oscilador si no perdiera nada de energía (\( \zeta=0 \)), el módulo del polo en el plano \( s \). \( \omega_d=\omega_n\sqrt{1-\zeta^2} \) es la frecuencia amortiguada: la frecuencia a la que realmente oscila el sistema, siempre algo menor que \( \omega_n \) porque cada vuelta se "frena" un poco al perder energía (la derivación completa de ambas está en [[frecuencias-segundo-orden]]). Solo son idénticas si \( \zeta=0 \); para cualquier \( \zeta>0 \), \( \omega_d<\omega_n \).

*Aproximación (i) — usar \( \omega_d\approx\omega_n \) para el periodo.* Se usa para escribir \( T_d=2\pi/\omega_d\approx2\pi/\omega_n \) y así no tener que arrastrar la raíz cuadrada. El error que comete viene de su propio Taylor:

$$ \frac{\omega_d}{\omega_n}=\sqrt{1-\zeta^2}=1-\frac{\zeta^2}{2}-\frac{\zeta^4}{8}-\dots $$

Es un error de **segundo orden en \( \zeta \)**: para \( \zeta=0.1 \) es del \( 0.5\,\% \); para \( \zeta=0.3 \), del \( 4.6\,\% \). Esta aproximación, sola, es buena incluso para \( \zeta \) no tan pequeño.

*Aproximación (ii) — Taylor de la exponencial.* La cantidad que de verdad hace falta aproximar es \( 1-e^{-4\pi\zeta} \), que no tiene forma cerrada simple. Se usa el desarrollo de \( e^{-x} \) en \( x=0 \):

$$ e^{-x}=1-x+\frac{x^2}{2}-\frac{x^3}{6}+\dots \;\Rightarrow\; 1-e^{-x}=x-\frac{x^2}{2}+\frac{x^3}{6}-\dots $$

y se trunca al primer término, \( 1-e^{-x}\approx x \) con \( x=4\pi\zeta \):

$$ \frac{\Delta E}{E}\approx 4\pi\zeta $$

Esto solo es válido si \( x=4\pi\zeta\ll1 \), es decir \( \zeta\ll1/(4\pi)\approx0.08 \). El error relativo de cortar en el primer término es, al orden siguiente, \( \approx x/2=2\pi\zeta \): crece **linealmente** con \( \zeta \) y es el que domina (mucho mayor que el de la aproximación (i)).

*Por qué hace falta \( \zeta \) pequeño y no vale para cualquier \( \zeta \).* El argumento de "energía perdida por ciclo" solo describe bien lo que pasa cuando el sistema oscila varias veces antes de apagarse. Si \( \zeta \) no es pequeño, en un solo periodo ya se pierde casi toda la energía y "fracción perdida por ciclo" deja de tener un significado claro (se acerca a 1 y se queda ahí). El Taylor de la exponencial es, además, lo que permite pasar de la expresión transcendente \( 1-e^{-4\pi\zeta} \) a la fórmula cerrada \( Q=1/(2\zeta) \); sin él habría que dejar \( Q \) en función de una exponencial, mucho menos manejable.

*Cuánto cuesta la aproximación — comparación con el resultado sin aproximar.* Puede calcularse \( Q \) desde la misma definición energética pero sin usar ninguna de las dos aproximaciones, con \( \omega_d \) y la exponencial exactos:

$$ Q_{exacto}(\zeta)=\frac{2\pi}{1-\exp\!\left(-4\pi\zeta/\sqrt{1-\zeta^2}\right)} $$

y compararlo con \( Q_{Taylor}=1/(2\zeta) \):

| \( \zeta \) | \( Q_{Taylor}=1/(2\zeta) \) | \( Q_{exacto} \) | error |
|---|---|---|---|
| 0.01 | 50.00 | 53.21 | −6.0 % |
| 0.05 | 10.00 | 13.46 | −25.7 % |
| 0.10 | 5.00 | 8.76 | −42.9 % |
| 0.30 | 1.67 | 6.41 | −74.0 % |
| 0.707 | 0.71 | 6.28 | −88.7 % |

El error crece deprisa con \( \zeta \): para \( \zeta\lesssim0.02\text{–}0.05 \) (típico de una resonancia LCL sin amortiguar) la aproximación es excelente; en \( \zeta=0.1 \) ya infravalora claramente la energía perdida por ciclo. Para \( \zeta \) grande, \( Q_{exacto} \) ni siquiera tiende a 0: **se satura en \( 2\pi\approx6.28 \)**, porque "toda la energía se pierde en un ciclo" es el límite físico de la definición energética — llegado ese punto, \( Q\equiv1/(2\zeta) \) ya no coincide con "energía almacenada / disipada por ciclo": se usa **por extensión**, como una forma cómoda de seguir hablando de amortiguamiento con un solo número, no porque la cuenta energética literal lo respalde. Por eso el resto del repositorio limita el uso fiable de \( Q\leftrightarrow\zeta \) a \( \zeta\lesssim0.3 \) (ver "Errores comunes").

<div class="cfig"><img src="figuras/factor-calidad-q-taylor.png" alt="comparacion de Q exacto sin aproximar Taylor frente a Q=1/(2 zeta) aproximado, y error relativo entre ambos en funcion de zeta"><div class="cap">Izquierda: \(Q_{Taylor}=1/(2\zeta)\) (la fórmula cerrada) frente a \(Q_{exacto}\) (misma definición energética, sin aproximar \(\omega_d\) ni la exponencial); coinciden para \(\zeta\) pequeño y se separan al crecer \(\zeta\), con \(Q_{exacto}\) saturándose en \(2\pi\). Derecha: error relativo de la aproximación, ya significativo (>25 %) a partir de \(\zeta\approx0.05\).</div></div>

**Paso 5 — aplicar la definición de Q.** Sustituyendo en la definición del Paso 0:

$$ Q=2\pi\,\frac{E}{\Delta E}\approx2\pi\,\frac{1}{4\pi\zeta} \;\Rightarrow\; \boxed{\;Q=\frac{1}{2\zeta}\;} $$

Ningún paso ha usado la naturaleza física del sistema: solo la forma canónica de los polos y la proporcionalidad energía–amplitud². Por eso esta relación es universal para sistemas de 2º orden, y no una propiedad particular del RLC (la aplicación al RLC, comparando \( s^2+(R/L)s+1/(LC) \) con la forma canónica, está en [[resonancia-rlc]]).

## Desarrollo 2 — de \( Q \) al ancho de banda \( \Delta f=f_0/Q \)
La otra cara de \( Q \) es geométrica: cuánto se ensancha el pico de resonancia en la respuesta en frecuencia. Se parte de la magnitud al cuadrado del resonador genérico:

$$ |H(j\omega)|^2=\frac{\omega_n^4}{(\omega_n^2-\omega^2)^2+(2\zeta\omega_n\omega)^2} $$

**Paso 1 — valor en el pico.** Para \( \zeta \) pequeño el pico está prácticamente en \( \omega\approx\omega_n \) (ver [[frecuencias-segundo-orden]] para la corrección exacta \( \omega_{peak}=\omega_n\sqrt{1-2\zeta^2} \)); evaluando ahí:

$$ |H(j\omega_n)|^2=\frac{\omega_n^4}{(2\zeta\omega_n^2)^2}=\frac{1}{4\zeta^2}=Q^2 $$

es decir, la altura del pico es exactamente \( Q \) (coherente con que \( Q \) mide cuánto se amplifica la excitación en resonancia).

**Paso 2 — condición de media potencia.** Los puntos de \( -3\,\)dB son donde \( |H|^2 \) cae a la mitad de su valor en el pico, \( Q^2/2 \). Una propiedad general de esta curva es que, en esos puntos, los dos términos del denominador se igualan entre sí (cada uno aporta la mitad de la caída):

$$ (\omega_n^2-\omega^2)^2=(2\zeta\omega_n\omega)^2 $$

**Paso 3 — resolver cerca de la resonancia.** Cerca de \( \omega\approx\omega_n \) se puede aproximar \( \omega_n^2-\omega^2=(\omega_n-\omega)(\omega_n+\omega)\approx2\omega_n(\omega_n-\omega) \), y en el lado derecho \( \omega\approx\omega_n \). Sustituyendo:

$$ \left[2\omega_n(\omega_n-\omega)\right]^2=(2\zeta\omega_n^2)^2 \;\Rightarrow\; (\omega_n-\omega)^2=\zeta^2\omega_n^2 \;\Rightarrow\; \omega_n-\omega=\pm\zeta\omega_n $$

**Paso 4 — los dos puntos de media potencia.** Hay dos soluciones, una por debajo y otra por encima de \( \omega_n \):

$$ \omega_1=\omega_n(1-\zeta), \qquad \omega_2=\omega_n(1+\zeta) $$

**Paso 5 — el ancho de banda.** Restando:

$$ \Delta\omega=\omega_2-\omega_1=2\zeta\omega_n=\frac{\omega_n}{Q} \;\Rightarrow\; \boxed{\;\Delta f=\frac{f_0}{Q}\;} $$

usando \( Q=1/(2\zeta) \) del Desarrollo 1. De nuevo, ningún paso depende del tipo de resonador: es geometría de la curva canónica de 2º orden.

<div class="cfig"><img src="figuras/factor-calidad-q-peak.png" alt="curvas de magnitud normalizadas para varios Q mostrando que el pico vale Q y el ancho de banda a media potencia es wn/Q"><div class="cap">Para cualquier resonador de 2º orden, el pico en \(\omega_n\) vale \(Q\) y el ancho de banda a media potencia (líneas punteadas, en \(Q/\sqrt2\)) es \(\omega_n/Q\): a más \(Q\), pico más alto y más estrecho — la misma relación, sea el resonador un RLC, un LCL o un sistema mecánico.</div></div>

## Generalización — por qué esto no depende del componente
\( Q \) y \( \zeta \) describen lo mismo (el amortiguamiento de un par de polos) desde dos ángulos: \( \zeta \) desde la ubicación del polo, \( Q \) desde la energía o la forma del pico. Por eso \( Q=1/(2\zeta) \) y \( \Delta f=f_0/Q \) aparecen idénticos en:
- Un RLC serie o paralelo ([[resonancia-rlc]]).
- El par resonante de un filtro LCL, con \( \omega_n=\omega_{res} \) ([[filtro-lcl]]).
- Un oscilador mecánico masa-resorte-amortiguador, una cavidad óptica, una antena, etc.

Lo único que cambia de un sistema a otro es **cómo se calculan \( \omega_n \) y \( \zeta \) a partir de sus componentes físicos** (por ejemplo \( \zeta=(R/2)\sqrt{C/L} \) en el RLC, o las fórmulas con \( R_1,R_2,R_d \) del LCL). La relación entre \( Q \), \( \zeta \) y el ancho de banda, en cambio, es siempre la misma.

## Cuándo y por qué se usa
\( Q \) es la forma más intuitiva de comunicar "cuánto pico" o "cuánto suena" un resonador sin tener que dar \( \zeta \) explícitamente: un ingeniero de RF habla de \( Q \) de una bobina, uno de potencia del \( Q \) de la resonancia de un filtro LCL, uno de acústica del \( Q \) de una caja resonante. Conociendo \( Q \) (o \( \zeta \)) se sabe de inmediato la altura del pico y su anchura, los dos datos que importan para decidir si hace falta amortiguar.

## Procedimiento (genérico)
1. Identifica el par de polos de 2º orden del sistema y obtén \( \zeta \) (de su ecuación característica o de su geometría en el plano \( s \), ver [[frecuencias-segundo-orden]]).
2. Calcula \( Q=1/(2\zeta) \).
3. La altura del pico de resonancia es \( \approx Q \) y su ancho de banda a \( -3\,\)dB es \( \approx f_0/Q \).
4. Si \( Q \) es demasiado alto para la aplicación, hay que aumentar \( \zeta \) (amortiguar), lo que baja y ensancha el pico.

## Ejemplo de código
```python
import numpy as np
zeta = 0.05
Q = 1/(2*zeta)                 # factor de calidad desde el amortiguamiento
f0 = 1100.0                    # Hz, frecuencia de resonancia
bw = f0/Q                      # ancho de banda a -3 dB

# verificación numérica de la altura del pico y del ancho de banda
wn = 2*np.pi*f0
r = np.linspace(0.5, 1.5, 200001)
H = 1/np.sqrt((1 - r**2)**2 + (2*zeta*r)**2)
peak = H.max()                          # ~ Q
mask = H >= peak/np.sqrt(2)
bw_num = (r[mask].max() - r[mask].min())*f0   # ~ f0/Q
```

## Parámetros y valores típicos
- RLC o LCL sin amortiguar: \( Q \) de 10 a varios cientos (\( \zeta \) de 0.001 a 0.05).
- Tras amortiguamiento (activo o pasivo) en electrónica de potencia: \( Q\approx2\text{–}5 \) (\( \zeta\approx0.1\text{–}0.25 \)), buen compromiso entre pico acotado y banda de paso intacta.
- \( Q=1/\sqrt2\approx0.71 \) (\( \zeta=0.707 \)): el pico desaparece (ver [[frecuencias-segundo-orden]]).

## Errores comunes
- Pensar que \( Q \) es una propiedad de un componente (una bobina, un condensador) y no del par de polos completo: dos sistemas con la misma bobina pero distinta resistencia o distinta carga tienen \( Q \) distinto.
- Aplicar las aproximaciones de este desarrollo (\( \omega_d\approx\omega_n \), \( \omega_n^2-\omega^2\approx2\omega_n(\omega_n-\omega)\)) cuando \( \zeta \) no es pequeño (a partir de \( \zeta\gtrsim0.3\text{–}0.4 \) empiezan a desviarse de los valores exactos).
- Confundir el ancho de banda a media potencia \( f_0/Q \) con el ancho de banda de un lazo de control (son conceptos relacionados pero no iguales).

## Uso en proyectos
- 01 / 02 (filtro LCL): \( Q \) se usa para dimensionar la \( R_d \) de amortiguamiento pasivo (Desarrollo 4 de [[filtro-lcl]]) y para leer de un vistazo cuánto pico de resonancia queda tras amortiguar.

## Conceptos relacionados
- [[resonancia-rlc]] · [[filtro-lcl]] · [[frecuencias-segundo-orden]] · [[respuesta-segundo-orden]] · [[diagrama-bode]] · [[series-taylor]]

## Referencias
- Ogata, *Ingeniería de Control Moderna*, Pearson.
- Franklin, Powell, Emami-Naeini, *Feedback Control of Dynamic Systems*.
