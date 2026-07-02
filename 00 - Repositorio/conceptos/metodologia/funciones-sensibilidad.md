---
titulo: Funciones de sensibilidad (S y T)
slug: funciones-sensibilidad
categoria: metodologia
tipo: concepto
nivel: avanzado
proyectos: [01-GFM-Impedance]
objetivos: [evaluar rechazo de perturbacion, ruido y robustez]
tags: [sensibilidad, S, T, PS, CS, rechazo, ruido, compromiso-bode, waterbed, Ms]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-02
relacionados: [margenes-estabilidad, loop-shaping, metricas-desempeno, control-robusto-hinf, sintonia-pi-pid]
referencias:
  - "Skogestad, Postlethwaite, Multivariable Feedback Control, Wiley 2005"
  - "Aström, Murray, Feedback Systems: An Introduction for Scientists and Engineers, 2008"
---

## Definición
Las **cuatro funciones de sensibilidad** describen cómo el lazo cerrado responde a referencia,
perturbación de entrada de planta, perturbación de salida y ruido de medida. La
sensibilidad \( S \) y la complementaria \( T \) resumen el desempeño y la robustez; las funciones
\( PS \) y \( CS \) completan el cuadro con la respuesta a perturbaciones de actuación y la
demanda al actuador.

## Fundamento teórico
Con ganancia de lazo \( L=CG \):
$$ S=\frac{1}{1+L}, \qquad T=\frac{L}{1+L}, \qquad PS=\frac{G}{1+L}, \qquad CS=\frac{C}{1+L} $$
$$ S+T=1\quad\forall\omega $$
- \( S \): de la perturbación de salida y de la referencia al error. \( M_s=\max|S| \): margen de módulo.
- \( T \): de la referencia a la salida y del ruido de medida a la salida.
- \( PS \): de la perturbación de entrada de planta a la salida.
- \( CS \): de la referencia al control (demanda al actuador).

<div class="cfig"><img src="figuras/funciones-sensibilidad-st.png" alt="funciones de sensibilidad S y T frente a la frecuencia"><div class="cap">$S$ pequeña a baja frecuencia da buen rechazo y seguimiento; $T$ pequeña a alta frecuencia atenúa el ruido de medida. Como $S+T=1$ no pueden ser ambas pequeñas en la misma banda (compromiso de Bode): el pico $M_s=\max|S|$ resume la robustez (objetivo $<2$).</div></div>

## 1 — Por qué \( S+T=1 \) (y por qué no se pueden bajar ambas)
**Paso 1 — definir las dos.** Con lazo de realimentación negativa y ganancia de lazo \( L=CG \), la sensibilidad y la complementaria son
$$ S=\frac{1}{1+L},\qquad T=\frac{L}{1+L} $$
\( S \) va de la perturbación/referencia al error; \( T \) va de la referencia (o del ruido de medida) a la salida.

**Paso 2 — sumarlas.** Con el mismo denominador \( 1+L \):
$$ S+T=\frac{1}{1+L}+\frac{L}{1+L}=\frac{1+L}{1+L}=\boxed{1}\quad\forall\,\omega $$
Es una **identidad algebraica**, no un objetivo de diseño: se cumple a toda frecuencia, en todo lazo de un grado de libertad.

**Paso 3 — la consecuencia.** Como \( S(j\omega)+T(j\omega)=1 \) para cada \( \omega \), por la desigualdad triangular \( 1=|S+T|\le|S|+|T| \): es imposible que \( |S| \) y \( |T| \) sean ambas pequeñas en la misma frecuencia. Si \( |S|\ll1 \) (buen rechazo) entonces \( T\approx1 \) (pasa el ruido); si \( |T|\ll1 \) (atenúa ruido) entonces \( S\approx1 \) (no rechaza). De ahí el reparto natural: \( S \) pequeña en **baja** frecuencia (rechazo/seguimiento) y \( T \) pequeña en **alta** (ruido).

**Paso 4 — número.** Si en una banda \( |L|=100 \) (40 dB), entonces \( |S|\approx1/100=0.01 \) (rechazo de −40 dB) y \( |T|\approx1 \) (0 dB): el control rechaza bien y, a la vez, sigue la referencia casi sin error. Donde \( |L|=1 \) (cruce), \( |S| \) y \( |T| \) valen \( \sim1/\sqrt2 \) cada una y su suma sigue siendo 1.

## 2 — La complementariedad \( S+T=1 \): el pico de sensibilidad y el trade-off

**El pico de sensibilidad \( M_s=\max|S| \)** es la distancia mínima del Nyquist de \( L(j\omega) \) al punto \( -1 \):
$$ M_s=\max_\omega|S(j\omega)|=\max_\omega\frac{1}{|1+L(j\omega)|}=\frac{1}{d_{\min}} $$
donde \( d_{\min} \) es la distancia mínima de la curva de Nyquist de \( L \) al punto \( -1+j0 \). Cuanto más cerca pasa \( L(j\omega) \) del punto \( -1 \), mayor es \( M_s \) y peor la robustez. El objetivo estándar es \( M_s<2 \) (equivalente a que \( L \) no entre en el disco de radio 0.5 centrado en \( -1 \)).

**El pico complementario \( M_t=\max|T| \)** mide cuánto amplifica el lazo cerrado las referencias en las frecuencias cercanas al cruce. Para un sistema bien amortiguado, \( M_t\lesssim1 \). La relación entre \( M_s \) y \( M_t \) no es exacta, pero en la práctica:
- \( M_s<2 \) implica típicamente \( M_t<1.5 \) (depende del diseño concreto).
- Sistemas con PM cercano a 45° dan \( M_s\approx1.3 \), \( M_t\approx1.05 \).
- Sistemas con PM ≈ 30° pueden tener \( M_s>2 \) y \( M_t\approx1.3 \) con sobreimpulso del 30%.

**El trade-off fundamental:** donde \( |S| \) es pequeño (buen rechazo de perturbaciones, baja frecuencia), \( |T|=1-S\approx1 \) (no se atenúa ruido). Donde \( |T| \) es pequeño (buena atenuación de ruido, alta frecuencia), \( |S|=1-T\approx1 \) (no se rechazan perturbaciones). La transición ocurre en la banda del cruce. No hay forma de evitar esta cesión: \( S+T=1 \) es una ley de conservación del diseño de control.

**Diseño con peso en \( S \) y \( T \).** En el diseño \( H_\infty \), los pesos \( W_S \) y \( W_T \) formalizan los requisitos:
$$ \|W_S\,S\|_\infty<1,\quad \|W_T\,T\|_\infty<1 $$
La inconsistencia de pesos (pedir \( W_S\gg1 \) y \( W_T\gg1 \) en la misma banda) hace el problema infactible, lo que evidencia que la restricción \( S+T=1 \) es un límite matemático, no un límite de herramientas.

## 3 — La función \( PS \): sensibilidad de la planta a perturbaciones de actuación

**La perturbación de entrada de planta** \( D \) actúa aguas arriba del actuador (en la entrada de \( G \)): puede ser un par de disturbio en un motor, una variación de tensión de alimentación de un convertidor, o una corriente de cortocircuito que inyecta potencia en el bus. La salida del sistema ante \( D \) es:
$$ Y = T\cdot R + PS\cdot D $$
donde \( R \) es la referencia y \( D \) es la perturbación. La función \( PS = G/(1+L) \) actúa como el "filtro" que ve \( D \) antes de llegar a la salida.

**Forma de \( |PS(j\omega)| \):**
- A baja frecuencia: si \( L \) tiene integrador, \( |PS|\approx|G|/|L|=1/|C|\to0 \) (el control rechaza las perturbaciones DC).
- A alta frecuencia: \( |L|\ll1 \), entonces \( |PS|\approx|G| \): la perturbación pasa directamente a la salida sin rechazo.
- En el cruce: transición entre rechazo y paso directo; el pico de \( |PS| \) ocurre cerca de \( \omega_c \).

**El pico de \( |PS| \):** puede ser grande si hay un modo lento no controlado en \( G \). Por ejemplo, si \( G \) tiene un polo en \( -a \) con \( a\ll\omega_c \) y el controlador no cancela ese polo, \( |PS| \) tendrá un pico en \( \omega\approx a \) de magnitud \( \approx 1/(|C(ja)|\cdot a) \). La cancelación de polo del PI precisamente elimina ese pico.

**Parámetros de diseño para \( |PS| \):**
- Si se pide rechazo \( >40 \) dB a \( f<f_p \): necesita \( |PS(j2\pi f_p)|<0.01 \), que requiere \( |L(j2\pi f_p)|>100 \) (40 dB de ganancia de lazo en ese punto).
- Para un PI puro (\( L=K_i/(j\omega) \)): \( |L(j2\pi f_p)|=K_i/(2\pi f_p) \), luego \( K_i>100\cdot2\pi f_p \).

## 4 — La función \( CS \): la señal de control que genera el controlador

La función \( CS = C/(1+L) \) es la señal de control normalizada: indica cuánto control demanda el controlador por unidad de referencia. Tiene importancia directa en el diseño porque la señal de control no puede ser ilimitada: el actuador tiene saturación.

**La transferencia de la referencia al control:**
$$ U = CS\cdot R - CS\cdot D_{out} $$
donde \( D_{out} \) es una perturbación aguas abajo (en la salida de \( G \)), y \( U \) es la señal de control (tensión de consigna al modulador, par de referencia, etc.).

**Forma de \( |CS(j\omega)| \):**
- A baja frecuencia: \( |CS|\approx|C|/|L|=1/|G| \). Para planta de primer orden \( G=K/(Ts+1) \), \( |CS(j0)|=1/K \): ganancia finita (el PI en DC tiene ganancia de \( K_i/(s\to0) \to\infty \), pero \( |L|\to\infty \) también, así que el cociente es finito).
- A alta frecuencia con PI: \( |C(j\omega)|\to K_p \) (ganancia proporcional), \( |L|\to0 \), luego \( |CS|\to K_p \). La señal de control en alta frecuencia está limitada por \( K_p \), no va a infinito.
- Con polo de rolloff en \( \omega_{ro} \): \( |CS| \) cae para \( \omega>\omega_{ro} \), reduciendo la excitación del actuador por el ruido de alta frecuencia.

**El filtro D del PID.** El diferenciador puro \( C_D=K_d\,s \) hace \( |CS|\to\infty \) en alta frecuencia: amplifica el ruido indefinidamente. Por ello el PID práctico filtra la derivada:
$$ C(s)=K_p+\frac{K_i}{s}+\frac{K_d\,s}{1+s/N} $$
con \( N \) el factor de filtro (típicamente \( N=5 \dots 20 \)). Esto limita \( |CS|\le K_p+K_d\,N \) en alta frecuencia.

**Criterio de diseño para \( |CS| \):** \( |CS(j\omega)| \) no debe superar \( U_{max}/R_{max} \) en ninguna frecuencia (donde \( U_{max} \) es la saturación del actuador y \( R_{max} \) es la amplitud máxima de referencia). Si \( |CS| \) es demasiado grande, el actuador saturaría ante perturbaciones de alta frecuencia (ruido).

## 5 — La integral de Bode: la conservación de la sensibilidad

**El teorema de Bode (versión sensibilidad):**
Para un lazo \( L(s) \) estable, estrictamente propio (cae al menos como \( 1/s^2 \)) y con \( G \) y \( C \) de fase mínima (todos los polos y ceros en el semiplano izquierdo), la integral logarítmica de la sensibilidad es exactamente cero:
$$ \boxed{\int_0^\infty \log|S(j\omega)|\,d\omega = 0} $$

**Interpretación geométrica: el colchón de agua ("waterbed").**
El integrando \( \log|S(j\omega)| \) es:
- **Negativo** donde \( |S|<1 \): frecuencias donde el lazo rechaza bien (baja frecuencia).
- **Positivo** donde \( |S|>1 \): el pico de sensibilidad, por encima del cruce.

La integral nula obliga a que el área positiva y el área negativa se cancelen exactamente. Esto es el efecto "waterbed" (colchón de agua): apretar \( |S| \) hacia abajo en una banda (más rechazo) lo hace salir hacia arriba en otra (pico \( M_s \) mayor). **No se puede mejorar el rechazo de perturbaciones sin empeorar el pico de sensibilidad**, y viceversa.

**El coste cuantitativo.** Si se exige \( |S|\le\varepsilon \) en la banda \( [0,\omega_1] \), el área negativa comprometida es \( \approx\omega_1\log\varepsilon \). Esta área debe recuperarse como área positiva. Si el pico se concentra en una banda \( [\omega_1,\omega_2] \), la magnitud del pico mínimo es:
$$ \log M_s \ge \frac{\omega_1}{\omega_2-\omega_1}\log\frac{1}{\varepsilon} $$
Más rechazo (\( \varepsilon\downarrow \)) o más estrecha la banda de recuperación → mayor \( M_s \) mínimo.

**Con polos inestables en \( G \) o en \( C \).** Si \( L(s) \) tiene polos inestables (semiplano derecho) con partes reales \( \text{Re}(p_k)>0 \):
$$ \int_0^\infty \log|S(j\omega)|\,d\omega = \pi\sum_k\text{Re}(p_k) > 0 $$
El margen de integración es positivo (mayor que cero), lo que significa que el pico \( M_s \) es obligatoriamente más grande: los polos inestables "cuestan" en términos de sensibilidad. Esta es la razón por la que los sistemas inestables (como los que deben controlar una planta con dinámica inversa) son inherentemente más difíciles de controlar con buen rechazo de perturbaciones.

## 6 — Diseño iterativo: las cuatro sensibilidades del lazo de corriente

**Datos del diseño:** planta \( G(s)=1/(L_1 s+R_1) \) con \( L_1=2 \) mH, \( R_1=50 \) mΩ. PI por cancelación de polo: \( C(s)=K_p(1+R_1/(L_1\,s))=\omega_{ci}(L_1 s+R_1)/s \) con \( \omega_{ci}=2\pi\cdot750 \) rad/s.

**Ganancia de lazo \( L(j\omega) \):**
$$ L(j\omega)=C(j\omega)\cdot G(j\omega)=\frac{\omega_{ci}(L_1 j\omega+R_1)}{j\omega}\cdot\frac{1}{L_1 j\omega+R_1}=\frac{\omega_{ci}}{j\omega} $$
Integrador puro de ganancia \( \omega_{ci} \): el cero del PI cancela exactamente el polo de la planta.

**Sensibilidad \( S(j\omega) \):**
$$ S(j\omega)=\frac{1}{1+\omega_{ci}/(j\omega)}=\frac{j\omega}{j\omega+\omega_{ci}} $$
Filtro de paso alto de primer orden, frecuencia de corte \( \omega_{ci} \). En DC: \( S(0)=0 \) (error nulo). En el cruce \( \omega=\omega_{ci} \): \( |S|=1/\sqrt{2}\approx-3 \) dB. No hay pico (\( M_s=1 \): el lazo integrador puro tiene sensibilidad monótonamente creciente hasta 1). **Nota:** con retardo digital, la sensibilidad real tiene pico \( M_s>1 \) cerca del cruce.

**Complementaria \( T(j\omega) \):**
$$ T(j\omega)=\frac{\omega_{ci}}{j\omega+\omega_{ci}} $$
Filtro de paso bajo de primer orden, BW = \( \omega_{ci} \). Sin sobreimpulso, sin oscilación. \( |T(-3\,\mathrm{dB})|=\omega_{ci} \): el ancho de banda del lazo cerrado es exactamente \( \omega_{ci} \).

**Función \( PS(j\omega) \):**
$$ PS(j\omega)=\frac{G(j\omega)}{1+L(j\omega)}=\frac{1}{L_1 j\omega+R_1}\cdot\frac{j\omega}{j\omega+\omega_{ci}}=\frac{j\omega}{(j\omega+\omega_{ci})(L_1 j\omega+R_1)} $$
A baja frecuencia: \( |PS|\approx\omega/(\omega_{ci}\cdot R_1)\to0 \) (cae como \( +20 \) dB/dec hasta el cruce). A alta frecuencia: \( |PS|\approx1/(L_1\omega) \) (cae como \( -20 \) dB/dec). Pico en \( \omega\approx\sqrt{\omega_{ci}R_1/L_1}=\sqrt{\omega_{ci}/\tau} \).

**Función \( CS(j\omega) \):**
$$ CS(j\omega)=\frac{C(j\omega)}{1+L(j\omega)}=\frac{\omega_{ci}(L_1 j\omega+R_1)}{j\omega}\cdot\frac{j\omega}{j\omega+\omega_{ci}}=\frac{\omega_{ci}(L_1 j\omega+R_1)}{j\omega+\omega_{ci}} $$
A alta frecuencia (\( j\omega\gg\omega_{ci} \)): \( |CS|\approx\omega_{ci}\,L_1 = K_p \) (la ganancia proporcional del PI). La señal de control queda limitada por \( K_p \) en alta frecuencia: no crece indefinidamente.

**Resumen numérico para \( f_{ci}=750 \) Hz, \( L_1=2 \) mH, \( R_1=50 \) mΩ:**

| Función | DC | Cruce \( f_{ci} \) | Alta freq. |
|---|---|---|---|
| \( \|S\| \) | 0 | \( 1/\sqrt{2}\approx-3 \) dB | → 1 |
| \( \|T\| \) | 1 | \( 1/\sqrt{2}\approx-3 \) dB | → 0 |
| \( \|PS\| \) | 0 | pico ≈ \( 0.5/R_1 \) | cae \( -20 \) dB/dec |
| \( \|CS\| \) | → \( K_i/\omega_{ci}=R_1 \) | — | → \( K_p=\omega_{ci}L_1 \) |

<div class="cfig"><img src="figuras/funciones-sensibilidad-analisis.png" alt="Las cuatro sensibilidades, trade-off S vs T, integral de Bode y efecto de Ms"><div class="cap">(a) Las cuatro funciones $|S|$, $|T|$, $|PS|$, $|CS|$ para el lazo de corriente con PI a 750 Hz: $S$ y $T$ se cruzan en el ancho de banda, $PS$ tiene un pico de paso limitado y $CS$ satura en $K_p$. (b) El trade-off $S$ vs $T$: donde $|S|<1$, $|T|\approx1$ y viceversa — la banda del cruce es la única transición posible. (c) La integral de Bode: el área negativa ($|S|<1$, baja frecuencia) se compensa con el área positiva ($M_s$): la integral total es cero. (d) El efecto de $M_s$: para $M_s=1.5$, 2, 3 la forma del Bode de $|S|$ cambia; $M_s>2$ indica poca robustez (distancia al punto $-1$ menor de 0.5).</div></div>

## Cuándo y por qué se usa
Para evaluar de un vistazo rechazo (S), atenuación de ruido (T), demanda al actuador (CS),
robustez ante perturbaciones de planta (PS) y robustez global (\( M_s \)). Es el diagnóstico
estándar tras cualquier diseño de lazo: un solo conjunto de cuatro curvas revela todo.

## Procedimiento (genérico)
1. Calcula \( L(j\omega)=C(j\omega)\,G(j\omega) \).
2. Obtén las cuatro sensibilidades: \( S, T, PS, CS \).
3. Verifica: \( |S| \) pequeña en baja frecuencia, \( |T| \) pequeña en alta, \( M_s=\max|S|<2 \).
4. Verifica \( |CS|<U_{max}/R_{max} \) (no saturación del actuador).
5. Si no cumple, ajusta \( \omega_c \) o la estructura del controlador.

## Ejemplo de código
```python
import numpy as np

L1, R1 = 2e-3, 50e-3
wci = 2*np.pi*750
f = np.logspace(-1, 4, 2000); w = 2*np.pi*f

# Lazo tras cancelación de polo: integrador puro
L = wci / (1j*w)
S = 1/(1+L); T = L/(1+L)
G = 1/(L1*1j*w + R1)
PS = G*S
C = wci*(L1*1j*w + R1)/(1j*w)
CS = C*S

Ms = np.max(np.abs(S))
BW = f[np.argmin(np.abs(np.abs(T) - 1/np.sqrt(2)))]
print(f"Ms = {Ms:.3f}, BW = {BW:.0f} Hz")
```

## Parámetros y valores típicos
\( M_s<2 \) (6 dB). BW de \( T \) ≈ \( \omega_c/(2\pi) \). \( |CS|\le K_p \) a alta frecuencia.
\( |PS| \) con pico en \( \sqrt{\omega_{ci}/\tau} \), valor pico \( \approx1/(\sqrt{\omega_{ci}\tau}\cdot 2R) \).

## Errores comunes
- Intentar S y T pequeñas a la vez en la misma banda (imposible, \( S+T=1 \)).
- No mirar \( |CS| \): un PI con \( K_p \) grande puede saturar el actuador ante ruido de medida.
- Subir ganancia para mejorar rechazo sin mirar el pico de \( S \) (empeora robustez).
- Interpretar \( M_s<2 \) como condición suficiente de buena robustez: también hay que verificar PM y GM.

## Uso en proyectos
- **01 (GFM)**: el comportamiento de la impedancia de salida y el pico del modo de potencia se
  interpretan como sensibilidad; el buen \( \zeta \) evita un pico de \( S \) alto.

## Conceptos relacionados
- [[margenes-estabilidad]] · [[loop-shaping]] · [[metricas-desempeno]] · [[control-robusto-hinf]]

## Referencias
- Skogestad, Postlethwaite, *Multivariable Feedback Control*, 2005.
- Aström, Murray, *Feedback Systems*, 2008.
