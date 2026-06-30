---
titulo: Control en cascada (lazos de corriente y tensión)
slug: control-cascada
categoria: control
tipo: tecnica
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [regular la tension del condensador con lazos anidados, sintonizar los PI por ancho de banda, respetar el limite que impone la resonancia LCL]
tags: [cascada, PI, desacoplo, dq, ancho-de-banda, separacion-de-escalas, cancelacion-de-polo, resonancia]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-30
relacionados: [filtro-lcl, marco-dq, desacoplo-dq, controlador-pid, sistema-primer-orden, diagrama-bode, margenes-estabilidad, droop-control]
referencias:
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
  - "Harnefors et al., Tuning of Grid-Connected Converter Current Controllers, IEEE TIE"
  - "Kazmierkowski, Krishnan, Blaabjerg, Control in Power Electronics, Academic Press 2002"
---

## Definición
Arquitectura de control con dos lazos PI **anidados**: un lazo **interno de corriente** (rápido) que regula la corriente de la bobina del convertidor \( i_{L1} \), metido dentro de un lazo **externo de tensión** (lento) que regula la tensión del condensador \( v_C \). Cada lazo es un PI en el marco \( dq \), con el desacoplo cruzado de los términos \( \pm\omega L,\ \pm\omega C \) (ver [[desacoplo-dq]]) ya aplicado, de modo que cada eje se controla como una planta SISO.

La idea central es la **separación de escalas temporales**: el lazo interno se hace tan rápido respecto al externo que, desde el punto de vista del lazo de tensión, la corriente "ya está donde se le pide" (la planta interna se comporta como una ganancia 1). Eso permite diseñar los dos lazos por separado, uno detrás de otro, en vez de resolver un sistema acoplado de cuarto orden de golpe.

## Qué hay antes y después de esta ficha
- **Antes:** el modelo \( dq \) de la planta ([[marco-dq]]), el desacoplo que convierte el lazo de corriente acoplado en dos SISO ([[desacoplo-dq]]) y la planta física a controlar ([[filtro-lcl]]).
- **Esta ficha:** cómo se eligen las ganancias de los dos PI (sintonía), por qué se anidan en ese orden, y qué límite le pone la resonancia del LCL al lazo externo.

## Diagrama de bloques
<div class="cfig"><img src="figuras/control-cascada-lazos.png" alt="lazos anidados de tension y corriente"><div class="cap">Lazos anidados: el lazo interno de corriente (rápido) regula \(i_{L1}\) dentro del lazo externo de tensión (lento) que regula \(v_C\). La salida del PI de tensión es la **referencia** del lazo de corriente, \(i_{L1}^*\). Cada PI vive en \(dq\) con su desacoplo cruzado.</div></div>

## Ecuaciones de partida
Dos plantas, una por lazo, ya desacopladas (un solo eje; el otro es idéntico):

- **Lazo de corriente** — la bobina \( L_1 \) con su resistencia \( R_1 \), excitada por la tensión de puente \( v_i \). De [[desacoplo-dq]], tras cancelar \( \pm\omega L_1 i_q \) y prealimentar \( v_C \):

$$ L_1\frac{di_{L1}}{dt}=v_i'-R_1 i_{L1} \;\Rightarrow\; \frac{i_{L1}}{v_i'}=\frac{1}{sL_1+R_1} $$

- **Lazo de tensión** — el condensador \( C_f \), cuya tensión la fija la corriente que le entra. Si el lazo interno es ideal (\( i_{L1}=i_{L1}^* \)) y la corriente de salida \( i_2 \) se trata como perturbación:

$$ C_f\frac{dv_C}{dt}=i_{L1}-i_2 \;\Rightarrow\; \frac{v_C}{i_{L1}^*}\approx\frac{1}{sC_f} $$

Las dos son de **primer orden** (un integrador con o sin polo). Por eso a cada una le basta un PI bien sintonizado.

## 1 — Sintonía del lazo de corriente (cancelación de polo)
**Idea.** La planta \( 1/(sL_1+R_1) \) tiene un polo en \( s=-R_1/L_1 \). Si el cero del PI se coloca **encima** de ese polo, ambos se cancelan y el lazo abierto queda como un integrador puro — el sistema más fácil de sintonizar que existe, porque su ancho de banda lo fija una sola ganancia.

**Paso 1 — forma del PI.** Se escribe el PI en forma con constante de tiempo integral \( T_i \):

$$ C_i(s)=K_{p,i}\left(1+\frac{1}{T_i s}\right)=K_{p,i}\,\frac{T_i s+1}{T_i s} $$

El factor \( (T_i s+1) \) es un cero en \( s=-1/T_i \).

**Paso 2 — cancelar el polo de la planta.** El lazo abierto es \( L(s)=C_i(s)\cdot\text{planta} \):

$$ L(s)=K_{p,i}\,\frac{T_i s+1}{T_i s}\cdot\frac{1}{sL_1+R_1}=K_{p,i}\,\frac{T_i s+1}{T_i s}\cdot\frac{1}{L_1\left(s+\frac{R_1}{L_1}\right)} $$

Para que el cero del PI \( (s+1/T_i) \) cancele el polo de la planta \( (s+R_1/L_1) \) hace falta \( 1/T_i=R_1/L_1 \), es decir:

$$ \boxed{\,T_i=\frac{L_1}{R_1}\,} $$

**Paso 3 — qué queda tras cancelar.** Sustituyendo \( T_i=L_1/R_1 \), el numerador del PI \( (T_i s+1) \) y el denominador de la planta \( L_1(s+R_1/L_1)=L_1 T_i^{-1}(T_i s+1) \) se cancelan término a término:

$$ L(s)=K_{p,i}\cdot\frac{1}{T_i s}\cdot\frac{1}{L_1\cdot\frac{1}{T_i}}=\frac{K_{p,i}}{L_1 s} $$

(usando \( L_1\cdot(1/T_i)\cdot T_i=L_1 \) en el denominador, queda \( L_1 s \)). El lazo abierto es **un integrador puro** \( K_{p,i}/(L_1 s) \): magnitud que cae a \( -20 \) dB/dec, fase constante \( -90^\circ \) (margen de fase \( 90^\circ \), incondicionalmente estable).

**Paso 4 — fijar el ancho de banda.** El cruce por 0 dB (\( |L(j\omega_{ci})|=1 \)) define la frecuencia de corte \( \omega_{ci} \) del lazo:

$$ \left|\frac{K_{p,i}}{L_1\,j\omega_{ci}}\right|=1 \;\Rightarrow\; \frac{K_{p,i}}{L_1\omega_{ci}}=1 \;\Rightarrow\; \boxed{\,K_{p,i}=L_1\,\omega_{ci}\,} $$

y de \( K_{i,i}=K_{p,i}/T_i=K_{p,i}\,R_1/L_1 \):

$$ \boxed{\,K_{i,i}=R_1\,\omega_{ci}\,} $$

**Paso 5 — lazo cerrado.** Con \( L(s)=\omega_{ci}/s \), el lazo cerrado es

$$ \frac{i_{L1}}{i_{L1}^*}=\frac{L(s)}{1+L(s)}=\frac{\omega_{ci}/s}{1+\omega_{ci}/s}=\frac{\omega_{ci}}{s+\omega_{ci}} $$

un **primer orden** con constante de tiempo \( \tau=1/\omega_{ci} \) y ancho de banda exactamente \( f_{ci} \). No hay sobreimpulso ni resonancia: la respuesta al escalón es \( 1-e^{-\omega_{ci}t} \), que alcanza el 95 % en \( 3\tau\approx0.48 \) ms para \( f_{ci}=1 \) kHz. El panel (a) de la figura siguiente muestra cómo el integrador atraviesa la planta tras la cancelación.

## 2 — Separación de escalas (por qué los lazos se anidan)
**Idea.** El lazo de tensión "ve" al de corriente como su actuador. Para poder diseñarlo como si la corriente fuera instantánea, el lazo interno tiene que estar **cerrado y plano (ganancia ≈1)** en toda la banda donde trabaja el externo. Eso obliga a \( f_{ci}\gg f_{cv} \).

**Cuánto más rápido.** El lazo de corriente cerrado, \( \omega_{ci}/(s+\omega_{ci}) \), tiene módulo 1 muy por debajo de \( f_{ci} \) y empieza a caer cerca de \( f_{ci} \). Si el lazo de tensión cruza en \( f_{cv} \), en esa frecuencia el interno debe valer aún \( \approx1 \). El módulo del interno en \( f_{cv} \) es

$$ \left|\frac{i_{L1}}{i_{L1}^*}(j\omega_{cv})\right|=\frac{\omega_{ci}}{\sqrt{\omega_{ci}^2+\omega_{cv}^2}}=\frac{1}{\sqrt{1+(f_{cv}/f_{ci})^2}} $$

Con \( f_{ci}/f_{cv}=5 \) esto vale \( 0.98 \) (error del 2 %); con \( 3 \), vale \( 0.95 \) (5 %). De ahí la **regla de oro**: \( f_{ci} \) entre 3 y 10 veces \( f_{cv} \). Menos de 3× y la aproximación "interno ideal" deja de valer (los dos lazos interactúan y el diseño separado falla); mucho más de 10× y se desperdicia ancho de banda del lazo interno (que está limitado por arriba por \( f_{sw} \)). El panel (b) lo muestra: la banda del lazo de tensión cae entera dentro de la zona donde el interno vale 1.

<div class="cfig"><img src="figuras/control-cascada-sintonia.png" alt="Izquierda: lazo abierto de corriente convertido en integrador puro tras cancelar el polo de planta con el cero del PI, cruzando 0dB en fci=1kHz. Derecha: lazo de corriente cerrado plano hasta cerca de fci, con la banda del lazo de tension (hasta fcv=350Hz) entera dentro de la zona de ganancia unidad"><div class="cap">(a) El cero del PI cancela el polo de la planta (8 Hz en el ejemplo) y el lazo abierto queda como un integrador puro que cruza 0 dB en \( f_{ci} \)=1 kHz, fijado solo por \( K_{p,i}=L_1\omega_{ci} \). (b) El lazo de corriente cerrado vale \( \approx1 \) en toda la banda del lazo de tensión (\( f_{cv} \)=350 Hz); la separación \( f_{ci}/f_{cv}\approx2.9\times \) en el proyecto está en el límite bajo de la regla 3–10× (ver Errores comunes).</div></div>

## 3 — Sintonía del lazo de tensión
**Idea.** Aceptado el interno como ganancia 1, el lazo de tensión ve la planta \( v_C/i_{L1}^*=1/(sC_f) \): un integrador puro. Un PI sobre un integrador da un lazo abierto con doble integración cerca del origen (90° + el cero del PI lo levanta), así que el **cero del PI de tensión es obligatorio** para tener margen de fase.

**Paso 1 — ganancia proporcional por ancho de banda.** El término proporcional fija el cruce. Con planta \( 1/(sC_f) \) y \( L_v(s)\approx K_{p,v}/(sC_f) \) lejos del cero, imponiendo \( |L_v(j\omega_{cv})|=1 \):

$$ \frac{K_{p,v}}{C_f\,\omega_{cv}}=1 \;\Rightarrow\; \boxed{\,K_{p,v}=C_f\,\omega_{cv}\,} $$

**Paso 2 — cero del PI para el margen de fase.** El cero \( 1/T_v \) se coloca **por debajo** de \( f_{cv} \) (típicamente en \( f_{cv}/3 \) a \( f_{cv}/5 \)) para que en el cruce ya aporte casi todo su \( +90^\circ \) de fase y el margen suba a un valor sano (45–60°). De ahí \( K_{i,v}=K_{p,v}/T_v \). Colocarlo demasiado abajo no estorba al margen pero ralentiza el rechazo de perturbación de baja frecuencia; demasiado arriba (cerca de \( f_{cv} \)) deja el margen de fase corto.

**Resultado.** El lazo de tensión cerrado es un segundo orden con \( \zeta\approx0.7 \) bien elegido el cero — respuesta al escalón con poco sobreimpulso y banda \( \approx f_{cv} \).

## 4 — El límite que impone la resonancia LCL
**Idea.** Todo lo anterior trató la planta de tensión como \( 1/(sC_f) \) limpio. Pero \( v_C \) está en medio de un filtro LCL, que tiene un **pico de resonancia** en \( f_{res} \) (ver [[filtro-lcl]], apartado 2). Si el lazo de tensión tiene ganancia apreciable en \( f_{res} \), lo excita: oscilación mantenida. Por eso \( f_{cv} \) (y, por encima, \( f_{ci} \)) deben quedar **claramente por debajo de \( f_{res} \)**.

**Jerarquía de frecuencias.** El diseño sano apila cuatro escalas:

$$ f_{cv} \;<\; f_{ci} \;<\; f_{res} \;\ll\; f_{sw} $$

En el proyecto (LCL con \( f_{res}\approx1.38 \) kHz): \( f_{cv}=350 \) Hz \( < f_{ci}=1 \) kHz \( < f_{res}=1378 \) Hz. El lazo de corriente queda justo por debajo de la resonancia, y el de tensión bastante más abajo — la ganancia de control en \( f_{res} \) ya ha caído lo suficiente como para no excitarla. El panel (a) de la figura siguiente lo sitúa todo sobre la planta resonante.

**Qué hacer si no cabe.** Si la especificación pide un \( f_{cv} \) tan alto que se acerca a \( f_{res} \), hay dos salidas, en este orden:
1. **Amortiguar la resonancia primero** (amortiguamiento activo \( K_{ad} \) o pasivo \( R_d \), ver [[filtro-lcl]] apartados 3–4): baja el pico y permite subir el control sin excitarlo. Es el motivo por el que en el proyecto 01 se añadió \( K_{ad}=6\,\Omega \) **antes** de poder subir el lazo de tensión a 350 Hz.
2. Si aun así no cabe, rediseñar el LCL para subir \( f_{res} \) (menos \( L \) o \( C \), ver [[filtro-lcl]] apartado 9).

El panel (b) muestra el contraste: con \( f_{cv} \) bajo y amortiguado, el escalón de \( v_C \) es limpio; subiendo \( f_{cv} \) hasta \( f_{res} \) sin amortiguar, la respuesta oscila sin apenas decaer.

<div class="cfig"><img src="figuras/control-cascada-lcl-limite.png" alt="Izquierda: modulo de la planta de tension con su pico de resonancia a 1378Hz, con fcv=350Hz y fci=1kHz marcadas a su izquierda dentro de la banda de control. Derecha: escalon de vC limpio con fcv=350Hz amortiguado frente a oscilacion mantenida al subir fcv a fres sin amortiguar"><div class="cap">(a) Las dos frecuencias de cruce del control (\( f_{cv} \), \( f_{ci} \)) caen a la izquierda del pico de resonancia \( f_{res} \): el control actúa donde la planta es un integrador limpio, no donde resuena. (b) Escalón de \( v_C \): con \( f_{cv} \)=350 Hz y la resonancia amortiguada, respuesta limpia (verde); subiendo \( f_{cv} \) hasta \( f_{res} \) sin amortiguar, el lazo excita la resonancia y oscila (rojo).</div></div>

## Cuándo y por qué se usa
Estándar en convertidores con control de tensión: grid-forming, UPS, alimentación de cargas en isla. El lazo de corriente da protección (limitar \( i_{L1} \)) y rechazo rápido de perturbaciones; el de tensión fija el punto de operación (la tensión de salida). La cascada también es la base sobre la que se montan los lazos externos de potencia/droop ([[droop-control]]) en grid-forming: la referencia \( v_C^* \) la genera el droop, y la cascada la sigue.

## Procedimiento de diseño (genérico)
1. **Lazo de corriente** (\( f_{ci}\sim f_{sw}/10 \)): cancelación de polo → \( T_i=L_1/R_1 \), \( K_{p,i}=L_1\omega_{ci} \), \( K_{i,i}=R_1\omega_{ci} \).
2. **Separación de escalas**: elegir \( f_{cv} \) con \( f_{ci}/f_{cv}\in[3,10] \).
3. **Lazo de tensión** (\( f_{cv}\sim f_{ci}/3 \) a \( /5 \)): \( K_{p,v}=C_f\omega_{cv} \); cero del PI en \( f_{cv}/3 \) a \( /5 \) → \( K_{i,v} \).
4. Añadir **desacoplo** \( \pm\omega L,\ \pm\omega C \) y feedforward de \( v_C \) y de red (ver [[desacoplo-dq]]).
5. **Verificar la resonancia LCL**: comprobar \( f_{cv}<f_{ci}<f_{res} \). Si la resonancia limita \( f_{cv} \), añadir [[filtro-lcl|amortiguamiento]] primero.
6. Comprobar márgenes de fase/ganancia ([[margenes-estabilidad]]) en lazo cerrado, en red fuerte **y** débil (la red baja \( f_{res} \), ver [[filtro-lcl]] apartado 8).

## Ejemplo de código
```python
import numpy as np

# Planta: L1=2mH, R1=0.1ohm, Cf=20uF; fsw=10kHz
L1, R1, Cf, fsw = 2e-3, 0.1, 20e-6, 10e3

# 1) lazo de corriente: fci = fsw/10 = 1 kHz, cancelacion de polo
fci = fsw/10;  wci = 2*np.pi*fci
Kp_i = L1*wci                 # = ancho de banda x inductancia
Ki_i = R1*wci                 # = Kp_i / Ti, con Ti = L1/R1 (cancela el polo de planta)

# 2) separacion de escalas: fcv = fci/3 (en el limite bajo de la regla)
fcv = fci/3;  wcv = 2*np.pi*fcv
Kp_v = Cf*wcv
Tv   = 1/(2*np.pi*(fcv/4))    # cero del PI de tension una decada-ish por debajo de fcv
Ki_v = Kp_v/Tv

print(f"corriente: Kp={Kp_i:.2f}  Ki={Ki_i:.1f}  (fci={fci:.0f} Hz)")
print(f"tension:   Kp={Kp_v*1e6:.1f}e-6  Ki={Ki_v*1e6:.1f}e-6  (fcv={fcv:.0f} Hz)")

# leyes de control (con desacoplo + feedforward, ver desacoplo-dq):
# iL1ref_d = Kp_v*ev_d + Ki_v*xvd - w*Cf*vcq          # lazo tension
# vid      = Kp_i*ei_d + Ki_i*xid - w*L1*iL1q + vcd   # lazo corriente
```

## Parámetros y valores típicos
- \( f_{ci}\approx0.5\text{–}1.5 \) kHz (regla \( f_{sw}/10 \)); \( f_{cv}\approx100\text{–}400 \) Hz.
- Separación \( f_{ci}/f_{cv}\in[3,10] \). Margen de fase objetivo del lazo de tensión 45–60°.
- Jerarquía completa: \( f_{cv}<f_{ci}<f_{res}\ll f_{sw} \).
- En el proyecto: \( f_{ci}=1 \) kHz, \( f_{cv}=350 \) Hz (separación \( \approx2.9\times \), justo bajo la regla 3×), con \( K_{ad}=6\,\Omega \) de amortiguamiento activo del LCL para poder subir el lazo de tensión sin excitar \( f_{res}\approx1.38 \) kHz.

## Errores comunes
- **Separación de escalas insuficiente** (\( f_{ci}/f_{cv}<3 \)): la aproximación "lazo interno = 1" deja de valer, los dos lazos interactúan y el diseño separado da márgenes peores que los calculados. En el proyecto la separación es \( 2.9\times \), ligeramente corta: funciona porque el amortiguamiento del LCL da margen extra, pero es un punto a vigilar.
- **Subir el lazo de tensión sin amortiguar la resonancia LCL** → la excita (oscilación mantenida, panel (b) de la figura del apartado 4).
- **Feedforward de corriente de carga mal usado**: en el proyecto desestabilizaba (creaba un lazo positivo). Verificar todos los feedforward en lazo cerrado, no solo en régimen.
- **Olvidar el signo del desacoplo cruzado** \( \pm\omega L,\ \pm\omega C \) (ver [[desacoplo-dq]]).
- **No re-verificar en red débil**: \( L_g \) baja \( f_{res} \) y puede meterla dentro de la banda de control que en red fuerte estaba holgada (ver [[filtro-lcl]] apartado 8).

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: regular \( v_C \)): cascada corriente (1 kHz) / tensión (350 Hz) con desacoplo. El feedforward de carga inicial se eliminó por desestabilizar; hubo que añadir \( K_{ad}=6\,\Omega \) de amortiguamiento activo del LCL **antes** de poder subir el lazo de tensión a 350 Hz sin excitar la resonancia.
- **02 - GFL-Impedance**: el lazo de corriente de la cascada es el que interactúa con la impedancia de red débil; su \( f_{ci} \) debe quedar por debajo de \( f_{res} \), que baja al debilitarse la red.

## Conceptos relacionados
- [[filtro-lcl]] · [[marco-dq]] · [[desacoplo-dq]] · [[controlador-pid]] · [[sistema-primer-orden]] · [[diagrama-bode]] · [[margenes-estabilidad]] · [[droop-control]]

## Referencias
- Yazdani, Iravani, *Voltage-Sourced Converters in Power Systems*, Wiley 2010.
- Harnefors et al., *Tuning of Grid-Connected Converter Current Controllers*, IEEE TIE.
- Kazmierkowski, Krishnan, Blaabjerg, *Control in Power Electronics*, Academic Press 2002.
