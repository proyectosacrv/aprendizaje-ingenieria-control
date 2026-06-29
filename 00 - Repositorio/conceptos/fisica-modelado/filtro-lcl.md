---
titulo: Filtro LCL
slug: filtro-lcl
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [atenuar armonicos de conmutacion, modelar la planta de potencia, gestionar la resonancia y amortiguarla]
tags: [filtro, resonancia, antiresonancia, amortiguamiento-activo, factor-Q, rizado, dimensionado, funcion-transferencia, LCL, dq]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-30
relacionados: [convertidor-vsc, marco-dq, impedancia-salida-estabilidad, control-cascada, diagrama-bode, antiresonancia, resonancia-rlc, amortiguamiento-pasivo-vs-activo, frecuencias-segundo-orden, factor-calidad-q, red-thevenin-scr]
referencias:
  - "Reznik et al., LCL Filter Design and Performance Analysis for Grid-Interconnected Systems, IEEE TIA 2014"
  - "Dannehl et al., Investigation of Active Damping Approaches for LCL Filters, IEEE TIA 2010"
  - "Wang, Blaabjerg, Harmonic Stability in Power-Electronic-Based Power Systems, IEEE TPEL 2014"
  - "Mohan, Undeland, Robbins, Power Electronics, Wiley 2003 (cap. rizado e inductancias)"
---

## Definición
El filtro LCL es una red de tercer orden \( L_1\!-\!C_f\!-\!L_2 \) que se coloca a la salida de cualquier fuente de tensión conmutada para entregar a la red (o a una carga) una corriente limpia a partir de una tensión troceada. Atenúa el rizado de conmutación con mejor relación tamaño/atenuación que un filtro L simple: por encima de su frecuencia de resonancia cae a \( -60 \) dB/dec (tres elementos reactivos) en lugar de \( -20 \) dB/dec. El precio de ese orden tres es una resonancia poco amortiguada que hay que gestionar.

## Qué hay antes del filtro (contexto genérico)
Aguas arriba de \( L_1 \) hay una etapa que impone una tensión media controlable pero troceada: un nudo cuya tensión instantánea conmuta entre niveles discretos a una frecuencia de conmutación \( f_{sw} \), y cuyo valor medio en cada periodo es la consigna que fija el control. Esa fuente de tensión conmutada puede ser un inversor de dos niveles, un convertidor multinivel, una rama de un convertidor DC-DC, un rectificador activo o cualquier otra etapa de electrónica de potencia: para el filtro es indiferente. Lo único que el filtro "ve" desde su entrada es:

- una tensión \( v_i \) con una componente fundamental útil (la consigna) más un espectro de armónicos concentrado alrededor de \( f_{sw} \) y sus múltiplos
- una resistencia/inductancia de fuente normalmente despreciable frente a \( L_1 \)

Por eso el diseño del LCL no depende de la naturaleza del convertidor, solo de tres datos de esa etapa: la tensión de bus disponible (que fija la amplitud del troceado), la frecuencia de conmutación \( f_{sw} \) (que fija dónde están los armónicos a atenuar) y la ganancia del modulador (que cambia si la etapa es de dos niveles, tres niveles, etc.). Aguas abajo de \( L_2 \) hay un punto de conexión (PCC) detrás del cual puede haber una red, un transformador, otras cargas o una isla; su inductancia se suma a \( L_2 \) y modifica la resonancia (ver apartado 8).

## Topología y diagrama
La rama serie \( L_1 \) (lado fuente) llega al nudo \( v_C \); del nudo cuelga el condensador \( C_f \) a tierra (opcionalmente con una resistencia \( R_d \) de amortiguamiento pasivo en serie); del nudo sale la rama serie \( L_2 \) (lado red/carga) hacia el PCC. \( R_1 \) y \( R_2 \) son las resistencias parásitas de las dos bobinas.

<div class="cfig"><img src="figuras/filtro-lcl-circuito.png" alt="Circuito del filtro LCL: fuente de tension conmutada, L1-R1, nudo vC con Cf a tierra, L2-R2, PCC"><div class="cap">Topología LCL por fase: rama serie \(L_1\)–\(C_f\)–\(L_2\) entre la fuente de tensión conmutada y el PCC; \(C_f\) deriva el rizado de conmutación a tierra.</div></div>

## Ecuaciones de partida (de dónde se sale)
Aplicando Kirchhoff a las tres ramas (tensión en las dos bobinas, corriente en el condensador) salen las tres ecuaciones de estado del filtro, con \( i_1,\,v_C,\,i_2 \) como estados:

$$ L_1\frac{d i_1}{dt}=v_i-v_C-R_1 i_1 \quad\text{(KVL rama }L_1\text{)} $$
$$ C_f\frac{d v_C}{dt}=i_1-i_2 \quad\text{(KCL nudo }v_C\text{)} $$
$$ L_2\frac{d i_2}{dt}=v_C-v_{pcc}-R_2 i_2 \quad\text{(KVL rama }L_2\text{)} $$

Estas tres ecuaciones son el modelo del LCL. En el marco \( dq \) (girando a \( \omega \)) cada derivada añade el acoplamiento cruzado de Park, \( +\omega\mathbf{J} \) con \( \mathbf{J}=\left[\begin{smallmatrix}0&-1\\1&0\end{smallmatrix}\right] \) (ver [[marco-dq]]):

$$ L_1\dot{\mathbf{i}}_1=\mathbf{v}_i-\mathbf{v}_C-R_1\mathbf{i}_1+\omega L_1\mathbf{J}\mathbf{i}_1,\quad
   C_f\dot{\mathbf{v}}_C=\mathbf{i}_1-\mathbf{i}_2+\omega C_f\mathbf{J}\mathbf{v}_C,\quad
   L_2\dot{\mathbf{i}}_2=\mathbf{v}_C-\mathbf{v}_{pcc}-R_2\mathbf{i}_2+\omega L_2\mathbf{J}\mathbf{i}_2 $$

## 1 — Funciones de transferencia (derivación completa)
El objetivo de esta sección es deducir, paso a paso, las funciones de transferencia que relacionan las dos corrientes del filtro (\( i_1 \) lado fuente, \( i_2 \) lado red) con las dos tensiones que actúan sobre él (\( v_i \) tensión de la fuente conmutada, \( v_{pcc} \) tensión en el PCC). Estas funciones son la planta que ve el control de corriente, así que de aquí salen la resonancia, la antiresonancia y la elección de qué corriente realimentar.

### El LCL como cuadripolo: dos entradas, varias salidas
El filtro tiene dos tensiones que actúan sobre él, y conviene verlo como un cuadripolo (dos puertos):
- \( v_i = V_1 \): la tensión de la fuente conmutada, en el puerto de entrada. Es la única variable que el control manipula (el modulador la sintetiza a partir de la consigna del lazo).
- \( v_{pcc} = V_2 \): la tensión en el PCC, en el puerto de salida. No la decide el convertidor sino la red/carga, así que es una perturbación, no una entrada de control.

Las salidas que interesan son las dos corrientes (\( i_1 \) lado fuente, \( i_2 \) lado red) y la tensión del condensador \( v_C \). Como el filtro es lineal, cada salida es la superposición de la respuesta a las dos entradas. Para la corriente de lado red, por ejemplo:

$$ i_2 = G_{i_2,v_i}(s)\,V_1 + G_{i_2,v_{pcc}}(s)\,V_2 $$

### Por qué se asume \( v_{pcc}=0 \) (\( V_2=0 \)) al calcular \( i_2/v_i \)
Esto es el principio de superposición de los sistemas lineales: la función de transferencia de una salida respecto a una entrada se define como la respuesta a esa entrada con todas las demás entradas anuladas. Por eso, para obtener \( G_{i_2,v_i}=i_2/v_i \) se pone \( v_{pcc}=0 \); y para obtener la respuesta a la red, \( G_{i_2,v_{pcc}}=i_2/v_{pcc} \), se pondría \( v_i=0 \). La respuesta total es la suma de ambas. Anular \( v_{pcc} \) no significa que la red no exista, sino que su efecto se contabiliza aparte, en su propia función de transferencia.

Tiene además un sentido físico directo: anular \( v_{pcc} \) en pequeña señal equivale a suponer la red rígida (un nudo de tensión fija, una fuente de tensión ideal cuya tensión no se mueve ante la corriente que le inyecta el convertidor). Para diseñar el lazo de control nos interesa primero cómo responde \( i_2 \) a lo que el control mueve (\( v_i \)); el efecto de las variaciones de \( v_{pcc} \) entra después como rechazo de perturbación. De hecho la respuesta a \( v_{pcc} \) con \( v_i=0 \) es justamente la admitancia de salida del conjunto, la magnitud central del análisis de estabilidad por impedancia (ver [[impedancia-salida-estabilidad]]).

### Objetivo de cada función de transferencia (para qué se calcula cada una)
Del mismo cuadripolo salen varias funciones de transferencia, y cada una sirve para una cosa distinta. Por eso se calculan \( i_2/v_i \), \( i_1/v_i \), \( v_C/v_i \) (y la cruzada \( i_2/v_{pcc} \)):

| Función | Se calcula con | Para qué sirve |
|---|---|---|
| \( i_2/v_i \) (transadmitancia directa) | \( v_{pcc}=0 \) | Planta del lazo de corriente de red. Es lo que el control gobierna; de su denominador sale la resonancia. |
| \( i_1/v_i \) | \( v_{pcc}=0 \) | Planta del lazo interno (corriente de lado fuente). Tiene un cero de antiresonancia que la hace fácil de estabilizar; es la corriente que se realimenta y la base del amortiguamiento activo. |
| \( v_C/v_i \) | \( v_{pcc}=0 \) | Tensión del condensador. Necesaria si se controla la tensión (modo grid-forming) y para sensar/estimar la corriente del condensador en el amortiguamiento. |
| \( i_2/v_{pcc} \) (admitancia de salida) | \( v_i=0 \) | Respuesta a la perturbación de red; es la admitancia de salida \( Y_o \) que entra en el criterio de estabilidad por impedancia frente a la red. |

La \( V_2/V_1 \) (relación de tensiones \( v_{pcc}/v_i \), o \( v_C/v_i \) como su versión interna) es la lectura clásica del filtro como "filtro de tensión": cuánto pasa de la tensión de entrada a la de salida en función de la frecuencia, y dónde está la resonancia. En el contexto de control de corriente la planta principal es \( i_2/v_i \), pero las demás se necesitan para el lazo interno, el amortiguamiento y la estabilidad frente a la red.

La derivación de abajo obtiene primero \( i_2 \) en función de las dos entradas (paso 4), de ahí aísla \( i_2/v_i \) anulando \( v_{pcc} \), y como complemento obtiene \( i_1/v_i \) (paso 5), que explica por qué se realimenta \( i_1 \) en el lazo interno (paso 6).

<div class="cfig"><img src="figuras/filtro-lcl-familia.png" alt="Magnitud de las tres FDT del LCL frente a vi: i2/vi, i1/vi y vC/vi"><div class="cap">Las tres FDT frente a \(v_i\) (con \(v_{pcc}=0\)): \(i_2/v_i\) (planta de red) solo tiene el pico de resonancia; \(i_1/v_i\) añade el valle de antiresonancia en \(f_{ar}\) antes del pico (por eso es fácil de realimentar); \(v_C/v_i\) es la tensión del condensador. Comparten denominador (misma resonancia), difieren en los ceros.</div></div>

### Versión reducida (sin resistencias, \( R_1=R_2=0 \))
**Paso 1 — pasar las tres ecuaciones a Laplace.** Con \( R_1 \) y \( R_2 \) despreciables para ver la estructura (se reintroducen en la versión completa de más abajo), las tres ecuaciones de partida en el dominio de Laplace son:

$$ s\,L_1\,I_1 = V_i - V_C, \qquad s\,C_f\,V_C = I_1 - I_2, \qquad s\,L_2\,I_2 = V_C - V_{pcc} $$

**Paso 2 — eliminar la tensión del condensador \( V_C \).** De la primera, \( V_C = V_i - s L_1 I_1 \). De la tercera, \( V_C = V_{pcc} + s L_2 I_2 \). Igualando:

$$ V_i - s L_1 I_1 = V_{pcc} + s L_2 I_2 $$

**Paso 3 — usar la ecuación del condensador para relacionar \( I_1 \) e \( I_2 \).** De la segunda, \( I_1 - I_2 = s C_f V_C \). Sustituyendo \( V_C = V_{pcc} + s L_2 I_2 \):

$$ I_1 = I_2 + s C_f (V_{pcc} + s L_2 I_2) = I_2(1 + s^2 L_2 C_f) + s C_f V_{pcc} $$

**Paso 4 — corriente de lado red \( i_2 \).** Sustituyendo esa \( I_1 \) en la igualdad del paso 2 y despejando \( I_2 \) se obtiene la respuesta de la corriente de lado red a las dos entradas:

$$ I_2 = \frac{V_i - V_{pcc}(1 + s^2 L_1 C_f)}{s^3 L_1 L_2 C_f + s(L_1 + L_2)} $$

De aquí, con red rígida (\( V_{pcc}=0 \)), la transferencia planta principal del control:

$$ G_{i_2}(s)=\frac{I_2}{V_i}=\frac{1}{s^3 L_1 L_2 C_f + s(L_1+L_2)} $$

**De dónde sale \( \omega_{res}^2 \) (no se asume, se factoriza).** El denominador es \( s^3 L_1 L_2 C_f + s(L_1+L_2) \). Sacando \( s\,L_1 L_2 C_f \) como factor común:

$$ s^3 L_1 L_2 C_f + s(L_1+L_2) = s\,L_1 L_2 C_f\left(s^2 + \frac{L_1+L_2}{L_1 L_2 C_f}\right) $$

El término constante que queda dentro del paréntesis es lo que se nombra

$$ \omega_{res}^2 \equiv \frac{L_1+L_2}{L_1 L_2 C_f} $$

**Por qué ese constante es \( \omega_{res}^2 \) (y no un nombre arbitrario).** Cualquier factor cuadrático con coeficiente líder unidad se escribe en su forma canónica de segundo orden

$$ s^2 + 2\zeta\omega_0\,s + \omega_0^2 $$

donde, por definición, \( \omega_0 \) es la frecuencia natural y \( \zeta \) el amortiguamiento. Comparando término a término con nuestro paréntesis \( s^2 + \dfrac{L_1+L_2}{L_1 L_2 C_f} \):
- el coeficiente de \( s \) es cero \( \Rightarrow 2\zeta\omega_0=0 \Rightarrow \zeta=0 \) (sin amortiguar);
- el término independiente es \( \omega_0^2 \Rightarrow \omega_0^2=\dfrac{L_1+L_2}{L_1 L_2 C_f} \).

Es decir, el constante que acompaña a \( s^2 \) es **por definición** el cuadrado de la frecuencia natural de ese modo. Otra forma de verlo: el factor \( s^2+\omega_{res}^2=0 \) tiene raíces \( s=\pm j\,\omega_{res} \), que en el dominio del tiempo son una oscilación sostenida \( e^{\pm j\omega_{res} t} \) de pulsación \( \omega_{res} \); la frecuencia de esa oscilación libre es justamente lo que llamamos resonancia. (Comprobación dimensional: \( 1/(L\,C) \) tiene unidades de \( \text{rad}^2/\text{s}^2 \), así que su raíz es una pulsación.) Por eso

$$ G_{i_2}(s)=\frac{1}{s\,L_1 L_2 C_f\,(s^2+\omega_{res}^2)} $$

No es una suposición: \( \omega_{res}^2 \) es, literalmente, el coeficiente que aparece al factorizar, y se identifica con la frecuencia natural por la forma canónica de segundo orden. El denominador se anula en \( s=0 \) y en \( s=\pm j\omega_{res} \): un par de polos sin parte real (\( \zeta\approx0 \)). Eso es la resonancia. El **porqué físico** (anular las dos fuentes y resolver el circuito libre) se deriva paso a paso en el apartado 2; aquí ha aparecido como consecuencia algebraica de la planta.

**Paso 4b — respuesta a la perturbación de red (admitancia de salida).** De la misma expresión del paso 4, anulando ahora \( v_i \) en vez de \( v_{pcc} \), sale la otra mitad de la superposición:

$$ Y_o(s)=\left.\frac{i_2}{v_{pcc}}\right|_{v_i=0}=\frac{-(1 + s^2 L_1 C_f)}{s\,L_1 L_2 C_f\,(s^2+\omega_{res}^2)} $$

Es la admitancia de salida del filtro: cómo responde la corriente de red a un movimiento de la tensión de red. Tiene el mismo denominador (misma resonancia) pero distinto numerador, y es la que se compara con la impedancia de la red en el criterio de estabilidad por impedancia (ver [[impedancia-salida-estabilidad]]). Confirma que anular una entrada u otra solo cambia el numerador: la resonancia (el denominador) es común a todas las FDT del filtro.

**Paso 5 — corriente de lado fuente \( i_1 \).** Sustituyendo la \( I_2 \) recién hallada en \( I_1 = I_2(1 + s^2 L_2 C_f) + s C_f V_{pcc} \), y tomando de nuevo \( V_{pcc}=0 \):

$$ G_{i_1}(s)=\frac{I_1}{V_i}=\frac{1 + s^2 L_2 C_f}{s\,L_1 L_2 C_f\,(s^2+\omega_{res}^2)} $$

Esta función tiene, además del mismo par de polos resonantes, un par de ceros en \( s=\pm j\omega_{ar} \) con:

$$ \omega_{ar}=\frac{1}{\sqrt{L_2 C_f}} \quad\text{(antiresonancia)} $$

**Paso 6 — interpretar resonancia vs antiresonancia.** \( G_{i_2} \) (lado red) tiene solo el pico de resonancia: la fase cae \( 180^\circ \) de golpe al cruzarla, lo que hunde el margen de fase si se realimenta \( i_2 \). \( G_{i_1} \) (lado fuente) tiene un cero de antiresonancia en \( \omega_{ar}<\omega_{res} \) que aporta \( +180^\circ \) de fase justo antes del pico, de modo que la fase no se desploma tanto. Conclusión práctica que se usa en todo el repositorio: realimentar \( i_1 \) (lado fuente) es mucho más fácil de estabilizar que realimentar \( i_2 \) (lado red). Esta es la razón de fondo por la que el lazo de corriente rápido se cierra sobre \( i_1 \) (desarrollo en [[antiresonancia]]).

### Versión completa (con \( R_1 \) y \( R_2 \) en serie con las bobinas)
Ahora sin despreciar nada. Conviene usar las impedancias de cada rama: \( Z_1=R_1+sL_1 \) (rama de lado fuente) y \( Z_2=R_2+sL_2 \) (rama de lado red). Las ecuaciones de Laplace pasan a ser \( Z_1 I_1 = V_i - V_C \), \( sC_f V_C = I_1 - I_2 \), \( Z_2 I_2 = V_C - V_{pcc} \). Repitiendo los mismos pasos (eliminar \( V_C \), anular \( v_{pcc} \)) se llega a forma cerrada:

$$ \frac{i_2}{v_i}=\frac{1}{Z_1+Z_2+sC_f Z_1 Z_2}, \qquad
   \frac{i_1}{v_i}=\frac{1+sC_f Z_2}{Z_1+Z_2+sC_f Z_1 Z_2} $$

Las dos comparten el denominador \( D(s)=Z_1+Z_2+sC_f Z_1 Z_2 \), que desarrollado es el polinomio característico completo (el mismo que el del apartado 2):

$$ D(s)=s^3 C_f L_1 L_2 + s^2 C_f(R_1 L_2 + R_2 L_1) + s\,(L_1+L_2+C_f R_1 R_2) + (R_1+R_2) $$

**Comprobación de coherencia:** con \( R_1=R_2=0 \) se tiene \( Z_1=sL_1 \), \( Z_2=sL_2 \), y \( D(s)\to s L_1 L_2 C_f(s^2+\omega_{res}^2) \); \( i_2/v_i \) e \( i_1/v_i \) recuperan exactamente las formas reducidas de los pasos 4 y 5. La versión reducida es el caso particular de la completa.

**Comparación de resultados (reducida vs completa).**

| Aspecto | Reducida (\( R_1=R_2=0 \)) | Completa (con \( R_1,R_2 \)) |
|---|---|---|
| Ganancia en baja frecuencia de \( i_2/v_i \) | infinita (polo en \( s=0 \), integrador puro) | finita: \( i_2/v_i(0)=1/(R_1+R_2) \). El polo del origen se convierte en un polo real de baja frecuencia en \( p_{lf}=(R_1+R_2)/(L_1+L_2) \) |
| Par resonante | \( s=\pm j\omega_{res} \) (\( \zeta=0 \), pico infinito) | desplazado al semiplano izquierdo, \( \zeta_{res}\approx\dfrac{R_1/L_1 + R_2/L_2 - (R_1+R_2)/(L_1+L_2)}{2\,\omega_{res}} \) |
| Ceros de antiresonancia de \( i_1 \) (en \( \omega_{ar} \)) | sobre el eje imaginario (\( 1+s^2 L_2 C_f \)) | amortiguados: \( 1+sC_f R_2+s^2 L_2 C_f \), con \( \zeta_{ar}=\tfrac{R_2}{2}\sqrt{C_f/L_2} \) |
| Frecuencias \( \omega_{res} \) y \( \omega_{ar} \) | exactas | casi idénticas (R desplaza poco la frecuencia, sí el amortiguamiento) |

La lectura práctica: las resistencias serie reales (parásitas) **sí** amortiguan algo —vuelven finitos el pico y la ganancia de continua— pero sus valores son tan pequeños que el \( \zeta_{res} \) resultante sigue siendo muy bajo y el pico, alto. Por eso no bastan: hace falta añadir amortiguamiento pasivo (\( R_d \)) o activo (\( K_{ad} \)). La versión reducida es útil para ver la estructura (frecuencias, ceros, pendientes); la completa, para cuantificar el amortiguamiento real y la ganancia de continua.

<div class="cfig"><img src="figuras/filtro-lcl-RvsnoR.png" alt="Comparacion de i2/vi sin R (pico infinito, integrador en baja frecuencia) vs con R1,R2 en serie (pico finito, meseta en baja frecuencia)"><div class="cap">\(i_2/v_i\) sin R (rojo) vs con \(R_1,R_2\) en serie (azul). Sin R: pico infinito en \(f_{res}\) y pendiente de integrador en baja frecuencia. Con R: el pico se vuelve finito (aunque sigue alto con valores parásitos) y la baja frecuencia se aplana a una meseta \(1/(R_1+R_2)\). La frecuencia de resonancia apenas cambia.</div></div>

<div class="cfig"><img src="figuras/filtro-lcl-bode.png" alt="Respuesta en frecuencia del LCL: i2/vi con resonancia, i1/vi con antiresonancia, con y sin amortiguamiento"><div class="cap">Magnitud de \(i_2/v_i\) e \(i_1/v_i\): \(i_2\) presenta el pico de resonancia afilado (rojo, \(\zeta\approx0\)) en \(f_{res}\); \(i_1\) añade el cero de antiresonancia en \(f_{ar}\) que aporta \(+180^\circ\) de fase antes del pico. Al amortiguar (azul) el pico se acota. Por debajo el filtro deja pasar la fundamental; por encima cae a \(-60\) dB/dec.</div></div>

## 2 — Frecuencia de resonancia (derivación completa)
La frecuencia de resonancia son los modos propios del filtro: las frecuencias a las que la red oscila por sí sola sin excitación externa. Para hallarlos se anulan las dos fuentes de tensión que actúan sobre el filtro (\( v_i=0 \) y \( v_{pcc}=0 \) en pequeña señal): lo que queda son los modos naturales del circuito \( L_1\!-\!C_f\!-\!L_2 \). Se presenta primero la versión reducida (sin resistencias parásitas), que da la fórmula limpia, y después la versión completa (con \( R_1,R_2 \) y la \( R_d \) de amortiguamiento), que muestra cómo esa resonancia ideal se convierte en un par de polos amortiguados.

### Versión reducida (\( R_1=R_2=0 \))
**Paso 1 — anular las fuentes y plantear las ecuaciones en Laplace.** Con \( v_i=0 \) y \( v_{pcc}=0 \), las tres ecuaciones de partida quedan:

$$ s L_1 I_1 = -V_C \;\Rightarrow\; I_1=\frac{-V_C}{sL_1}, \qquad s C_f V_C = I_1 - I_2, \qquad s L_2 I_2 = V_C \;\Rightarrow\; I_2=\frac{+V_C}{sL_2} $$

**Paso 2 — sustituir \( I_1 \) e \( I_2 \) en la ecuación del condensador.** Llevando las dos corrientes a \( s C_f V_C = I_1 - I_2 \):

$$ s C_f V_C = -\frac{V_C}{sL_1} - \frac{V_C}{sL_2} $$

**Paso 3 — dividir por \( V_C \) (modo no trivial, \( V_C\neq0 \)).** El condensador oscila, así que su tensión no es nula y se puede dividir:

$$ s C_f = -\frac{1}{sL_1} - \frac{1}{sL_2} $$

**Paso 4 — reordenar a la ecuación característica.** Multiplicando por \( s \) y pasando todo a un lado:

$$ s^2 C_f + \frac{1}{L_1} + \frac{1}{L_2} = 0 \;\Rightarrow\; s^2 C_f = -\left(\frac{1}{L_1}+\frac{1}{L_2}\right) = -\frac{L_1+L_2}{L_1 L_2} $$

**Paso 5 — despejar \( s \) y leer la frecuencia.** Queda:

$$ s^2 = -\frac{L_1+L_2}{L_1 L_2 C_f} \;\Rightarrow\; s=\pm j\,\omega_{res} $$

con un par de raíces puramente imaginarias (sin parte real, amortiguamiento nulo). De ahí:

$$ \boxed{\;\omega_{res}=\sqrt{\frac{L_1+L_2}{L_1 L_2 C_f}}, \qquad f_{res}=\frac{1}{2\pi}\sqrt{\frac{L_1+L_2}{L_1 L_2 C_f}}\;} $$

**Paso 6 — interpretación física (las dos bobinas en paralelo).** El término \( 1/L_1 + 1/L_2 \) es la suma de inversos típica de un paralelo. Al anular las fuentes, \( L_1 \) y \( L_2 \) quedan colgando del nudo \( v_C \) hacia masa (cada fuente cortocircuitada es un camino a masa), así que están en paralelo. Definiendo la inductancia equivalente paralelo:

$$ L_{eq}=\frac{L_1 L_2}{L_1+L_2} $$

la expresión se compacta en la de un tanque LC simple, \( L_{eq} \) resonando con \( C_f \):

$$ f_{res}=\frac{1}{2\pi\sqrt{L_{eq} C_f}} $$

que es idéntica a la del paso 5 (resonancia de \( C_f \) contra \( L_1 \) paralelo \( L_2 \)). Esto coincide con el denominador de las funciones de transferencia del apartado 1: \( s^3 L_1 L_2 C_f + s(L_1+L_2)=s L_1 L_2 C_f(s^2+\omega_{res}^2) \), cuyos ceros no nulos son justo \( s=\pm j\omega_{res} \).

> Aviso sobre una aproximación habitual: algunos textos usan \( L_1+L_2 \) (suma serie) en lugar de \( L_{eq} \) (paralelo) en el denominador, \( f_{res,aprox}=1/(2\pi\sqrt{(L_1+L_2)C_f}) \). Subestima \( f_{res} \) porque \( L_1+L_2>L_{eq} \) siempre. La diferencia es pequeña cuando \( L_2\ll L_1 \) (relación \( r=L_2/L_1 \) pequeña) pero crece al acercarse \( L_2 \) a \( L_1 \). Usar siempre la forma exacta con \( L_{eq} \).

### Versión completa (con \( R_1,R_2 \) y \( R_d \))
Sin despreciar nada, las ecuaciones con fuentes anuladas y resistencias incluidas (\( R_1 \) en serie con \( L_1 \), \( R_2 \) en serie con \( L_2 \); la \( R_d \) de amortiguamiento se añade luego en serie con \( C_f \)) son:

$$ s L_1 I_1 = -V_C - R_1 I_1 \;\Rightarrow\; I_1=\frac{-V_C}{R_1+sL_1}, \qquad s L_2 I_2 = V_C - R_2 I_2 \;\Rightarrow\; I_2=\frac{+V_C}{R_2+sL_2} $$

Sustituyendo en la ecuación del condensador \( sC_f V_C = I_1 - I_2 \) y dividiendo por \( V_C \):

$$ s C_f = -\frac{1}{R_1+sL_1} - \frac{1}{R_2+sL_2} $$

Multiplicando por \( (R_1+sL_1)(R_2+sL_2) \) se obtiene la ecuación característica exacta (cúbica en \( s \)):

$$ s^3 C_f L_1 L_2 + s^2 C_f(R_1 L_2 + R_2 L_1) + s\,[C_f R_1 R_2 + (L_1+L_2)] + (R_1+R_2) = 0 $$

Es el polinomio completo del filtro. Comprobación: con \( R_1=R_2=0 \) se reduce a \( s^3 C_f L_1 L_2 + s(L_1+L_2)=0 \), es decir \( s(s^2 C_f L_1 L_2 + L_1 + L_2)=0 \), que devuelve la versión reducida.

**Cómo se calcula \( \omega_{res} \) con resistencias.** La cúbica ya no factoriza como \( s(s^2+\omega_{res}^2) \); ahora tiene un polo real (de baja frecuencia) y un par complejo (el resonante, ya amortiguado). Se factoriza como

$$ C_f L_1 L_2\,(s+p_{lf})\,(s^2 + 2\zeta_{res}\omega_n\,s + \omega_n^2) $$

**Paso a — hacer la cúbica mónica.** Se divide toda la cúbica por su coeficiente líder \( C_f L_1 L_2 \) para que el término en \( s^3 \) quede con coeficiente 1 (así se puede comparar con la forma factorizada, que también es mónica). Cada coeficiente se simplifica:

$$ s^3 + \underbrace{\frac{C_f(R_1 L_2 + R_2 L_1)}{C_f L_1 L_2}}_{=\,R_1/L_1\,+\,R_2/L_2}\,s^2 + \underbrace{\frac{C_f R_1 R_2 + (L_1+L_2)}{C_f L_1 L_2}}_{=\,R_1 R_2/(L_1 L_2)\,+\,\omega_{res}^2}\,s + \underbrace{\frac{R_1+R_2}{C_f L_1 L_2}}_{=\,b_0} = 0 $$

donde se ha usado \( (L_1+L_2)/(L_1 L_2 C_f)=\omega_{res}^2 \). Llamamos a los tres coeficientes \( b_2=R_1/L_1+R_2/L_2 \), \( b_1=\omega_{res}^2+R_1 R_2/(L_1 L_2) \) y \( b_0=(R_1+R_2)/(C_f L_1 L_2) \).

**Paso b — expandir la forma factorizada propuesta.** El producto del polo real por el par de segundo orden, multiplicado término a término, es:

$$ (s+p_{lf})(s^2+2\zeta_{res}\omega_n s+\omega_n^2) = s^3 + (p_{lf}+2\zeta_{res}\omega_n)\,s^2 + (\omega_n^2+2\zeta_{res}\omega_n\,p_{lf})\,s + p_{lf}\,\omega_n^2 $$

**Paso c — igualar coeficiente a coeficiente.** Como los dos polinomios mónicos son el mismo, sus coeficientes de \( s^2 \), \( s^1 \) y \( s^0 \) deben coincidir uno a uno:

$$ \text{(I)}\quad p_{lf}+2\zeta_{res}\omega_n = b_2 = \frac{R_1}{L_1}+\frac{R_2}{L_2} $$
$$ \text{(II)}\quad \omega_n^2+2\zeta_{res}\omega_n\,p_{lf} = b_1 = \omega_{res}^2+\frac{R_1 R_2}{L_1 L_2} $$
$$ \text{(III)}\quad p_{lf}\,\omega_n^2 = b_0 = \frac{R_1+R_2}{C_f L_1 L_2} $$

**Paso d — resolver el sistema (I)(II)(III) por perturbación.** El sistema es no lineal (las ecuaciones (II) y (III) tienen productos de las incógnitas), pero las resistencias son pequeñas frente a las reactancias del filtro, así que se resuelve ordenando todo por potencias de R. El método consiste en clasificar cada cantidad por su "tamaño" cuando \( R\to0 \) y luego recorrer cada ecuación quedándose solo con los términos del mismo orden.

**Tamaño de cada incógnita (la idea de fondo).** Con \( R_1=R_2=0 \) el par resonante está sobre el eje imaginario: su parte real es nula. Por tanto, al encender las resistencias:
- el polo real \( p_{lf} \) y el amortiguamiento \( 2\zeta_{res}\omega_n \) **valen 0 cuando R=0**, así que son de **orden \( R \)** (proporcionales a las resistencias, se anulan con ellas);
- la frecuencia \( \omega_n^2 \) **vale \( \omega_{res}^2\neq0 \) cuando R=0**, así que es de **orden \( R^0 \)**: existe sin pérdidas y las resistencias solo la corrigen.

Conviene recordar también el tamaño de los coeficientes: \( b_2 \) y \( b_0 \) son de orden \( R \) (lineales en las resistencias), mientras que \( b_1=\omega_{res}^2+R_1R_2/(L_1L_2) \) es \( \omega_{res}^2 \) (orden \( R^0 \)) más una corrección de orden \( R^2 \).

**Orden 0 — términos sin R.** Se mira (II), que es la única con un término de orden \( R^0 \) en el lado izquierdo. El producto \( 2\zeta_{res}\omega_n\,p_{lf} \) es (orden \( R \))·(orden \( R \)) = orden \( R^2 \), despreciable aquí; y en el lado derecho \( R_1R_2/(L_1L_2) \) también es \( R^2 \). Queda solo:

$$ \omega_n^2\big|_{0} = \omega_{res}^2 $$

es decir, en primer orden la frecuencia natural del par es la misma que sin pérdidas.

**Orden 1 — términos lineales en R.**
- De (III), \( p_{lf}\,\omega_n^2=b_0 \). El lado izquierdo es (orden \( R \))·(orden \( R^0 \)) = orden \( R \), igual que \( b_0 \). Sustituyendo \( \omega_n^2\approx\omega_{res}^2 \) y desarrollando la división (los \( C_f L_1 L_2 \) se cancelan):

$$ p_{lf}=\frac{b_0}{\omega_{res}^2}=\frac{(R_1+R_2)/(C_f L_1 L_2)}{(L_1+L_2)/(L_1 L_2 C_f)} =\frac{R_1+R_2}{C_f L_1 L_2}\cdot\frac{L_1 L_2 C_f}{L_1+L_2}=\frac{R_1+R_2}{L_1+L_2} $$

- De (I), \( p_{lf}+2\zeta_{res}\omega_n=b_2 \), todo de orden \( R \); se despeja el amortiguamiento:

$$ 2\zeta_{res}\omega_n = b_2-p_{lf} = \frac{R_1}{L_1}+\frac{R_2}{L_2}-\frac{R_1+R_2}{L_1+L_2} $$

- En (II) al orden \( R \): el lado izquierdo no aporta nada lineal (\( \omega_n^2 \) es \( R^0 \) y \( 2\zeta_{res}\omega_n\,p_{lf} \) es \( R^2 \)) y el derecho tampoco (\( R_1R_2 \) es \( R^2 \)). Conclusión importante: **no hay corrección de orden \( R \) a la frecuencia**; el desplazamiento de \( \omega_n \) empieza en \( R^2 \). Por eso "la frecuencia apenas se mueve y lo que cambia es el amortiguamiento".

**Orden 2 — términos cuadráticos en R.** Para afinar \( \omega_n^2 \) se vuelve a (II) conservando ya los términos \( R^2 \), y se sustituyen \( 2\zeta_{res}\omega_n \) y \( p_{lf} \) (ambos de orden \( R \), su producto es el \( R^2 \) buscado):

$$ \omega_n^2 = b_1 - 2\zeta_{res}\omega_n\,p_{lf} = \omega_{res}^2 + \frac{R_1 R_2}{L_1 L_2} - \left(\frac{R_1}{L_1}+\frac{R_2}{L_2}-\frac{R_1+R_2}{L_1+L_2}\right)\frac{R_1+R_2}{L_1+L_2} $$

**El amortiguamiento como número.** Atención al orden lógico: el amortiguamiento **no sale del Orden 2** (que refina la frecuencia), sino del **Orden 1**. Allí se obtuvo el *producto* \( 2\zeta_{res}\omega_n \) (no \( \zeta_{res} \) suelto):

$$ 2\zeta_{res}\omega_n = \frac{R_1}{L_1}+\frac{R_2}{L_2}-\frac{R_1+R_2}{L_1+L_2} \quad\text{(del Orden 1)} $$

Para despejar \( \zeta_{res} \) solo falta dividir ese producto por \( 2\omega_n \); el valor de \( \omega_n \) que se usa es el del **Orden 0** (\( \omega_n\approx\omega_{res} \)). El Orden 2 (la corrección de \( \omega_n^2 \)) no interviene en el amortiguamiento, como se justifica a continuación.

**Por qué se puede usar \( \omega_n\approx\omega_{res} \).** \( \zeta_{res} \) ya es de orden \( R \) (la cantidad \( 2\zeta_{res}\omega_n \) es lineal en las resistencias). Y \( \omega_n=\omega_{res}+\mathcal{O}(R^2) \) (la frecuencia solo se corrige en segundo orden, Paso d). Al dividir, sustituir \( \omega_n \) por \( \omega_{res} \) introduce un error relativo de orden \( R^2 \), que sobre una cantidad ya de orden \( R \) da una corrección de orden \( R^3 \): despreciable. Por eso es lícito poner \( \omega_n\approx\omega_{res} \) sin perder precisión al primer orden:

$$ \zeta_{res}=\frac{2\zeta_{res}\omega_n}{2\omega_n}\approx\frac{1}{2\omega_{res}}\left(\frac{R_1}{L_1}+\frac{R_2}{L_2}-\frac{R_1+R_2}{L_1+L_2}\right) $$

**Simplificar el corchete a una sola fracción.** Las tres fracciones de dentro se reducen a común denominador \( L_1 L_2 (L_1+L_2) \):

$$ \frac{R_1}{L_1}+\frac{R_2}{L_2}-\frac{R_1+R_2}{L_1+L_2} = \frac{R_1 L_2(L_1+L_2)+R_2 L_1(L_1+L_2)-(R_1+R_2)L_1 L_2}{L_1 L_2 (L_1+L_2)} $$

Desarrollando el numerador:

$$ \underbrace{R_1 L_1 L_2 + R_1 L_2^2}_{R_1 L_2(L_1+L_2)} + \underbrace{R_2 L_1^2 + R_2 L_1 L_2}_{R_2 L_1(L_1+L_2)} - \underbrace{(R_1 L_1 L_2 + R_2 L_1 L_2)}_{(R_1+R_2)L_1 L_2} = R_1 L_2^2 + R_2 L_1^2 $$

(los términos \( R_1 L_1 L_2 \) y \( R_2 L_1 L_2 \) se cancelan). El corchete queda, limpio:

$$ \frac{R_1}{L_1}+\frac{R_2}{L_2}-\frac{R_1+R_2}{L_1+L_2} = \frac{R_1 L_2^2 + R_2 L_1^2}{L_1 L_2 (L_1+L_2)} $$

**Resultado cerrado del amortiguamiento.** Sustituyendo en la expresión de \( \zeta_{res} \):

$$ \boxed{\;\zeta_{res} = \frac{R_1 L_2^2 + R_2 L_1^2}{2\,\omega_{res}\,L_1 L_2 (L_1+L_2)}\;} $$

**Interpretación.** Las dos resistencias amortiguan, pero con pesos distintos: \( R_1 \) (lado fuente) entra multiplicada por \( L_2^2 \) y \( R_2 \) (lado red) por \( L_1^2 \). La resistencia que está en serie con la bobina **más pequeña** pesa más en el amortiguamiento. Caso simétrico \( R_1=R_2=R \): \( \zeta_{res}=R(L_1^2+L_2^2)/[2\omega_{res}L_1 L_2(L_1+L_2)] \).

**Comprobación numérica** (mismos valores del ejemplo: \( L_1=2 \) mH, \( L_2=1 \) mH, \( C_f=20\,\mu\text{F} \), \( R_1=R_2=0.1\,\Omega \), \( \omega_{res}=8660 \) rad/s):

$$ \zeta_{res}=\frac{0.1\cdot(10^{-3})^2 + 0.1\cdot(2\cdot10^{-3})^2}{2\cdot8660\cdot(2\cdot10^{-3})(10^{-3})(3\cdot10^{-3})} = \frac{5\times10^{-7}}{1.04\times10^{-4}} \approx 0.0048 $$

idéntico al \( \zeta \) que devolvió `numpy.roots` en el ejemplo numérico de arriba, lo que valida toda la cadena de perturbación.

Resumiendo, el polo real, el amortiguamiento del par y su frecuencia natural son:

$$ p_{lf}=\frac{R_1+R_2}{L_1+L_2} \quad\text{(polo real de baja frecuencia)} $$
$$ 2\zeta_{res}\,\omega_n = \frac{R_1}{L_1}+\frac{R_2}{L_2}-\frac{R_1+R_2}{L_1+L_2} \quad\text{(amortiguamiento del par)} $$
$$ \omega_n^2 = \underbrace{\frac{L_1+L_2}{L_1 L_2 C_f}}_{\omega_{res}^2\ \text{(sin R)}} + \frac{R_1 R_2}{L_1 L_2} - \left(\frac{R_1}{L_1}+\frac{R_2}{L_2}-\frac{R_1+R_2}{L_1+L_2}\right)\frac{R_1+R_2}{L_1+L_2} $$

\( \omega_n \) es la frecuencia natural del par (la "\( \omega_{res} \) con resistencias"). Las correcciones que añade R son de **segundo orden** (productos de resistencias), así que con valores parásitos \( \omega_n\approx\omega_{res} \): la frecuencia apenas se mueve, lo que cambia de verdad es el amortiguamiento \( \zeta_{res} \). Conviene además distinguir tres frecuencias:

$$ \omega_n\ \text{(natural)}, \qquad \omega_d=\omega_n\sqrt{1-\zeta_{res}^2}\ \text{(oscilación amortiguada real)}, \qquad \omega_{peak}=\omega_n\sqrt{1-2\zeta_{res}^2}\ \text{(pico del Bode)} $$

Para \( \zeta_{res} \) pequeño las tres casi coinciden. La deducción de estas tres frecuencias y cuándo se separan está en [[frecuencias-segundo-orden]]. Con R no despreciable, lo práctico es resolver la cúbica numéricamente (`numpy.roots`) y leer el par complejo \( s=-\sigma\pm j\omega_d \), de donde \( \omega_n=\sqrt{\sigma^2+\omega_d^2} \) y \( \zeta_{res}=\sigma/\omega_n \).

**Ejemplo numérico** (\( L_1=2 \) mH, \( L_2=1 \) mH, \( C_f=20\,\mu\text{F} \), \( R_1=R_2=0.1\,\Omega \)):

```python
import numpy as np
L1, L2, Cf, R1, R2 = 2e-3, 1e-3, 20e-6, 0.1, 0.1
# polinomio caracteristico D(s) = a3 s^3 + a2 s^2 + a1 s + a0
a3 = Cf*L1*L2
a2 = Cf*(R1*L2 + R2*L1)
a1 = Cf*R1*R2 + (L1 + L2)
a0 = R1 + R2
raices = np.roots([a3, a2, a1, a0])        # -> -66.7  y  -41.7 +- j8660
s = raices[raices.imag > 1][0]             # el par complejo (rama Im>0)
sigma, wd = -s.real, s.imag
wn   = np.hypot(sigma, wd)                  # 8660 rad/s  (natural, la "wres" con R)
zeta = sigma/wn                             # 0.0048      (amortiguamiento real)
wres0 = np.sqrt((L1+L2)/(L1*L2*Cf))         # 8660 rad/s  -> apenas cambia sin R
print(wn, wn/(2*np.pi), zeta)               # 8660 rad/s, 1378 Hz, 0.0048
```

El resultado confirma lo anterior: \( \omega_n\approx\omega_{res} \) (1378 Hz, igual que sin R) y \( \zeta_{res}\approx0.0048 \) (las resistencias parásitas amortiguan tan poco que el pico sigue alto; de ahí la necesidad de amortiguamiento pasivo o activo).

### Amortiguamiento con una \( R_d \) en serie con \( C_f \) (derivación paso a paso)
Cuando el amortiguamiento se introduce a propósito con una resistencia \( R_d \) en serie con el condensador, se deriva igual que la frecuencia (modos propios, fuentes anuladas), pero ahora con \( R_d \) en la rama del condensador. Se ponen \( R_1=R_2=0 \) para aislar el efecto de \( R_d \). La novedad es que la tensión del nudo ya no es la del condensador: el nudo está a \( v_{Cf}+R_d\,i_C \), con \( i_C=i_1-i_2 \).

**Paso 1 — ecuaciones de los modos propios.** Con las fuentes anuladas, la caída en cada bobina es la tensión del nudo \( (v_{Cf}+R_d(i_1-i_2)) \), y la del condensador su propia ley:

$$ s L_1 I_1 = -\big(V_{Cf}+R_d(I_1-I_2)\big), \qquad s L_2 I_2 = V_{Cf}+R_d(I_1-I_2), \qquad s C_f V_{Cf} = I_1 - I_2 $$

**Paso 2 — despejar \( I_1 \) e \( I_2 \) en función de \( V_{Cf} \).** De la tercera, \( I_1-I_2 = s C_f V_{Cf} \). Sustituyendo este \( R_d(I_1-I_2)=R_d\,sC_f V_{Cf} \) en las dos primeras:

$$ s L_1 I_1 = -V_{Cf}(1+s R_d C_f) \;\Rightarrow\; I_1=\frac{-V_{Cf}(1+sR_dC_f)}{sL_1}, \qquad I_2=\frac{+V_{Cf}(1+sR_dC_f)}{sL_2} $$

**Paso 3 — formar \( I_1-I_2 \) e igualar a \( sC_f V_{Cf} \).** Restando las dos corrientes:

$$ I_1-I_2 = -V_{Cf}(1+sR_dC_f)\left(\frac{1}{sL_1}+\frac{1}{sL_2}\right) = s C_f V_{Cf} $$

**Paso 4 — dividir por \( V_{Cf} \) (modo no trivial) y combinar las fracciones.** Con \( 1/(sL_1)+1/(sL_2)=(L_1+L_2)/(sL_1L_2) \):

$$ s C_f = -(1+sR_dC_f)\,\frac{L_1+L_2}{s L_1 L_2} $$

**Paso 5 — multiplicar por \( sL_1L_2 \) y desarrollar el paréntesis.**

$$ s^2 C_f L_1 L_2 = -(1+sR_dC_f)(L_1+L_2) = -(L_1+L_2) - s R_d C_f (L_1+L_2) $$

Pasando todo a un lado:

$$ s^2 C_f L_1 L_2 + s R_d C_f (L_1+L_2) + (L_1+L_2) = 0 $$

**Paso 6 — dividir por \( C_f L_1 L_2 \) para dejar la cuadrática del par resonante.**

$$ s^2 + s\,\frac{R_d(L_1+L_2)}{L_1 L_2} + \frac{L_1+L_2}{C_f L_1 L_2} = 0 $$

(la tercera raíz, real, se perdió al dividir por \( V_{Cf} \), igual que el \( s=0 \) del caso sin pérdidas.)

**Paso 7 — comparar con la forma canónica \( s^2+2\zeta\omega_n s+\omega_n^2 \).** Término a término:

$$ \omega_n^2 = \frac{L_1+L_2}{C_f L_1 L_2} = \omega_{res}^2 \qquad\Rightarrow\qquad \omega_n=\omega_{res}\ \text{(exacto: } R_d \text{ no cambia la frecuencia)} $$
$$ 2\zeta_{Rd}\,\omega_n = \frac{R_d(L_1+L_2)}{L_1 L_2} $$

**Paso 8 — despejar \( \zeta_{Rd} \) y sustituir \( \omega_{res}=\sqrt{(L_1+L_2)/(L_1 L_2 C_f)} \).**

$$ \zeta_{Rd}=\frac{R_d(L_1+L_2)}{2 L_1 L_2\,\omega_{res}} = \frac{R_d(L_1+L_2)}{2 L_1 L_2}\sqrt{\frac{L_1 L_2 C_f}{L_1+L_2}} = \boxed{\;\frac{R_d}{2}\sqrt{\frac{C_f(L_1+L_2)}{L_1 L_2}}\;} $$

A diferencia del caso de \( R_1,R_2 \) (que corrigen la frecuencia en orden \( R^2 \)), con \( R_d \) en serie con \( C_f \) la cuadrática es **exacta** y \( \omega_n=\omega_{res} \) sin corrección: \( R_d \) solo añade amortiguamiento, no mueve el pico.

### Comparación de los tres casos
| Caso | Amortiguamiento \( \zeta \) del par | Frecuencia natural \( \omega_n \) |
|---|---|---|
| Sin resistencias (\( R_1=R_2=R_d=0 \)) | \( 0 \) (pico infinito) | \( \omega_{res} \) exacta |
| Solo \( R_d \) en serie con \( C_f \) | \( \dfrac{R_d}{2}\sqrt{\dfrac{C_f(L_1+L_2)}{L_1 L_2}} \) | \( \omega_{res} \) **exacta** (no se mueve) |
| Solo \( R_1,R_2 \) en serie con las bobinas | \( \dfrac{R_1 L_2^2 + R_2 L_1^2}{2\,\omega_{res} L_1 L_2 (L_1+L_2)} \) | \( \omega_{res}+\mathcal{O}(R^2) \) (se mueve poco) |

Las tres contribuciones se suman a primer orden: con las tres a la vez, \( \zeta_{total}\approx\zeta_{Rd}+\zeta_{res}(R_1,R_2) \).

**Comparación numérica** (mismos valores, \( \omega_{res}=8660 \) rad/s): con las parásitas \( R_1=R_2=0.1\,\Omega \) sale \( \zeta_{res}\approx0.0048 \) (casi nada). Para llegar a un \( \zeta\approx0.17 \) útil con \( R_d \) hace falta \( R_d=1/(3\omega_{res}C_f)\approx1.93\,\Omega \): \( \zeta_{Rd}=\tfrac{1.93}{2}\sqrt{20\!\times\!10^{-6}\cdot 3\!\times\!10^{-3}/(2\!\times\!10^{-6})}=\tfrac{1.93}{2}\sqrt{0.03}\approx0.167 \). Es decir, una \( R_d \) deliberada de \( \sim2\,\Omega \) amortigua ~35 veces más que las parásitas de \( 0.1\,\Omega \) en las bobinas — porque está colocada donde más amortigua (en serie con \( C_f \)) y es mucho mayor. (Verificado: los autovalores del sistema con \( R_d \) dan \( \zeta=0.1667 \) y \( \omega_n=8660 \) rad/s, idénticos a la fórmula.)

> **¿Por qué \( \zeta_{res} \) (de \( R_1,R_2 \)) y \( \zeta_{Rd} \) (de \( R_d \)) son fórmulas distintas, y por qué poner \( R_1=R_2=0 \) no reproduce la de \( R_d \)?** Porque son **tres resistencias distintas en ramas distintas**: \( R_1 \) y \( R_2 \) van en serie con las bobinas \( L_1 \) y \( L_2 \); \( R_d \) va en serie con el condensador \( C_f \). Cada una amortigua por un camino diferente (las de las bobinas, por la caída proporcional a la corriente de bobina; la del condensador, por la caída proporcional a \( i_1-i_2 \)), así que cada una tiene su propia fórmula. Son contribuciones **independientes** que se suman a primer orden: \( \zeta_{total}\approx\zeta_{res}(R_1,R_2)+\zeta_{Rd}(R_d) \). Por eso anular \( R_1,R_2 \) en \( \zeta_{res} \) da 0 (has quitado esas resistencias), no la fórmula de \( R_d \), que es otro componente situado en otro sitio. Y con **todas** a cero, \( \zeta=0 \) exacto: sin ninguna resistencia no hay disipación (las bobinas y \( C_f \) solo almacenan energía), así que **no existe ningún amortiguamiento "solo con inductancias"** — el amortiguamiento siempre lo aporta una resistencia o el amortiguamiento activo.

### Caso general: \( R_1 \), \( R_2 \) y \( R_d \) a la vez (derivación completa)
Aquí están las tres resistencias presentes: \( R_1 \) en serie con \( L_1 \), \( R_2 \) en serie con \( L_2 \) y \( R_d \) en serie con \( C_f \). Se deriva sin asumir nada y se demuestra que el amortiguamiento total es la **suma** de las dos contribuciones.

**Paso 1 — impedancias de cada rama.** Conviene agrupar cada rama en su impedancia (fuentes anuladas):

$$ Z_1=R_1+sL_1\ \text{(rama de }L_1), \qquad Z_2=R_2+sL_2\ \text{(rama de }L_2), \qquad Z_c=R_d+\frac{1}{sC_f}\ \text{(rama de }C_f) $$

**Paso 2 — ecuaciones de las ramas.** La tensión del nudo \( V_A \) (donde se unen las tres ramas) cae por cada bobina y por la rama del condensador:

$$ I_1=\frac{-V_A}{Z_1}, \qquad I_2=\frac{+V_A}{Z_2}, \qquad V_A=Z_c\,(I_1-I_2) $$

**Paso 3 — formar \( I_1-I_2 \) y sustituir en la del condensador.** Restando las dos corrientes, \( I_1-I_2=-V_A\left(\frac{1}{Z_1}+\frac{1}{Z_2}\right) \). Metiéndolo en \( V_A=Z_c(I_1-I_2) \):

$$ V_A=-V_A\,Z_c\left(\frac{1}{Z_1}+\frac{1}{Z_2}\right) $$

**Paso 4 — dividir por \( V_A \) (modo no trivial) y juntar fracciones.** Con \( 1/Z_1+1/Z_2=(Z_1+Z_2)/(Z_1Z_2) \):

$$ 1=-Z_c\,\frac{Z_1+Z_2}{Z_1 Z_2} \;\Rightarrow\; \boxed{\;Z_1 Z_2 + Z_c\,(Z_1+Z_2)=0\;} $$

Esta es la ecuación característica compacta del filtro (vale para cualquier combinación de resistencias).

**Paso 5 — sustituir \( Z_c=R_d+1/(sC_f) \) y multiplicar por \( sC_f \).**

$$ s C_f\,Z_1 Z_2 + (sC_f R_d + 1)(Z_1+Z_2)=0 \;\Rightarrow\; sC_f Z_1 Z_2 + sC_f R_d(Z_1+Z_2) + (Z_1+Z_2)=0 $$

**Paso 6 — desarrollar con \( Z_1+Z_2=(R_1+R_2)+s(L_1+L_2) \) y \( Z_1 Z_2=R_1R_2+s(R_1L_2+R_2L_1)+s^2 L_1 L_2 \).** Agrupando por potencias de \( s \) se llega a la cúbica completa:

$$ s^3 C_f L_1 L_2 + s^2 C_f\big[R_1L_2+R_2L_1+R_d(L_1+L_2)\big] + s\big[C_f R_1 R_2 + C_f R_d(R_1+R_2)+(L_1+L_2)\big] + (R_1+R_2)=0 $$

**Comprobaciones:** con \( R_d=0 \) se recupera la cúbica de \( R_1,R_2 \) sola; con \( R_1=R_2=0 \) sale \( s\big[s^2 C_f L_1 L_2 + sC_f R_d(L_1+L_2)+(L_1+L_2)\big]=0 \), es decir la cuadrática de \( R_d \) más la raíz \( s=0 \). Todo encaja.

**Paso 7 — hacer mónica (dividir por \( C_f L_1 L_2 \)) e identificar coeficientes.** Los tres coeficientes quedan:

$$ b_2=\underbrace{\frac{R_1}{L_1}+\frac{R_2}{L_2}}_{\text{de }R_1,R_2}+\underbrace{R_d\Big(\frac{1}{L_1}+\frac{1}{L_2}\Big)}_{\text{de }R_d}, \quad b_1=\omega_{res}^2+\underbrace{\frac{R_1R_2+R_d(R_1+R_2)}{L_1 L_2}}_{\mathcal{O}(R^2)}, \quad b_0=\frac{R_1+R_2}{C_f L_1 L_2} $$

**Paso 8 — factorizar \( (s+p_{lf})(s^2+2\zeta\omega_n s+\omega_n^2) \) y resolver por perturbación** (como en el caso de \( R_1,R_2 \): \( p_{lf} \) y \( 2\zeta\omega_n \) de orden \( R \); \( \omega_n^2 \) de orden \( R^0 \)):
- Orden 0: \( \omega_n^2\approx\omega_{res}^2 \) (los términos de \( b_1 \) con R son \( R^2 \)).
- Orden 1, de \( p_{lf}\omega_n^2=b_0 \): \( p_{lf}=\dfrac{R_1+R_2}{L_1+L_2} \) — **solo depende de \( R_1,R_2 \)** (\( b_0 \) no tiene \( R_d \): la \( R_d \) no afecta al polo de baja frecuencia a primer orden).
- Orden 1, de \( p_{lf}+2\zeta\omega_n=b_2 \):

$$ 2\zeta\omega_n=b_2-p_{lf}=\underbrace{\Big(\frac{R_1}{L_1}+\frac{R_2}{L_2}-\frac{R_1+R_2}{L_1+L_2}\Big)}_{\text{parte de }R_1,R_2} + \underbrace{R_d\,\frac{L_1+L_2}{L_1 L_2}}_{\text{parte de }R_d} $$

**Paso 9 — dividir por \( 2\omega_n\approx2\omega_{res} \) y reconocer las dos fórmulas ya conocidas.** El primer corchete se simplifica a \( (R_1L_2^2+R_2L_1^2)/(L_1L_2(L_1+L_2)) \) (ya hecho antes) y el término de \( R_d \) da \( (R_d/2)\sqrt{C_f(L_1+L_2)/(L_1L_2)} \). Por tanto:

$$ \boxed{\;\zeta_{total}=\underbrace{\frac{R_1 L_2^2+R_2 L_1^2}{2\,\omega_{res} L_1 L_2 (L_1+L_2)}}_{\zeta_{res}(R_1,R_2)}+\underbrace{\frac{R_d}{2}\sqrt{\frac{C_f(L_1+L_2)}{L_1 L_2}}}_{\zeta_{Rd}}\;} $$

Esto **demuestra** la aditividad que antes se afirmaba: con las tres resistencias, el amortiguamiento del par resonante es exactamente (a primer orden) la suma del de las bobinas más el de \( R_d \). Cada resistencia entra por su propio camino y sus efectos no se mezclan a primer orden; los términos cruzados (\( R_d R_1 \), etc.) son de orden \( R^2 \) y solo afectan a la pequeña corrección de \( \omega_n \), no al amortiguamiento. La frecuencia, de nuevo, casi no se mueve: \( \omega_n\approx\omega_{res} \).

Por eso la versión reducida da la frecuencia (dónde está el pico) y la versión completa da el amortiguamiento (cómo de afilado es y por qué hay que amortiguarlo).

> A resaltar: sin amortiguar, cualquier lazo rápido o impedancia de red que excite \( f_{res} \) provoca oscilación sostenida. Es uno de los mecanismos típicos de inestabilidad armónica y de oscilaciones de alta frecuencia entre convertidor y red.

## 3 — Factor de calidad Q (derivación y efecto en la respuesta)
El factor de calidad \( Q \) mide cuántas veces amplifica el filtro una excitación justo en \( f_{res} \) (la altura del pico de resonancia).

**De dónde sale.** Para un par de polos de segundo orden con amortiguamiento \( \zeta \), la ganancia en el pico respecto a la banda de paso es \( Q=1/(2\zeta) \) (derivación general, energética y de ancho de banda, en [[factor-calidad-q]]). Combinándolo con el amortiguamiento que introduce una \( R_d \) en serie con \( C_f \) (apartado 2):

$$ Q=\frac{1}{2\zeta}=\frac{1}{R_d\sqrt{C_f(L_1+L_2)/(L_1 L_2)}}=\frac{1}{R_d}\sqrt{\frac{L_{eq}}{C_f}} $$

es decir, \( Q \) es la relación entre la impedancia característica del tanque \( \sqrt{L_{eq}/C_f} \) y la resistencia de amortiguamiento \( R_d \). Sin resistencias (\( R_d\to0 \)) \( Q\to\infty \) y el pico es teóricamente infinito; con resistencias reales pequeñas \( Q \) sigue siendo alto (típico 10–50 en LCLs de potencia), lo que hace imprescindible amortiguar.

**Caso de estudio: efecto de Q sobre la respuesta.** Al subir el amortiguamiento (bajar \( Q \)) el pico de resonancia baja y se ensancha, mientras la banda de paso y la caída de \( -60 \) dB/dec por encima quedan casi intactas. La resistencia de amortiguamiento pasivo óptima en serie con \( C_f \) es:

$$ R_d\approx\frac{1}{3\,\omega_{res} C_f} $$

que deja \( Q\approx3 \) (un compromiso entre acotar el pico y no degradar la atenuación a \( f_{sw} \)). Por debajo de eso el pico sigue siendo peligroso; muy por encima se sobre-amortigua y se pierde atenuación. De dónde sale exactamente ese "3" (el umbral de margen en dB frente al coste en pérdidas) se desarrolla en [[factor-calidad-q]].

<div class="cfig"><img src="figuras/filtro-lcl-factorQ.png" alt="Bode de |i2/vi| para varios valores de Q mostrando el pico de resonancia cada vez más bajo"><div class="cap">Efecto del factor \(Q\) sobre \(|i_2/v_i|\): sin amortiguar (\(Q\to\infty\)) el pico es enorme; al añadir \(R_d\) el pico baja y se ensancha. Con \(R_d\) óptimo (\(Q\approx3\)) queda acotado sin estropear la atenuación a \(f_{sw}\); sobre-amortiguar (\(Q\) bajo) no aporta y empeora el filtrado.</div></div>

El inconveniente del amortiguamiento pasivo es que \( R_d \) disipa potencia, \( P_{R_d}=R_d\,I_{C_f,rms}^2 \). Por eso en inversores de potencia media-alta se prefiere el amortiguamiento activo por software (ver apartado 4 y [[amortiguamiento-pasivo-vs-activo]]), que consigue el mismo \( \zeta \) sin pérdidas.

## 4 — Amortiguamiento activo (derivación, estudio de polos y diseño)
En vez de disipar en una \( R_d \) física, se emula una resistencia de amortiguamiento por software. La técnica habitual realimenta la corriente del condensador \( i_{C_f}=i_1-i_2 \) a la tensión de la fuente con ganancia \( K_{ad} \):

$$ v_i = v_{i,PI} - K_{ad}\,(i_1-i_2) $$

**Por qué equivale a una resistencia sin pérdidas (desarrollo).** La dinámica de \( i_1 \) sin amortiguar es \( L_1\,di_1/dt=v_i-v_C-R_1 i_1 \). Sustituyendo la ley de control:

$$ L_1\frac{di_1}{dt}=v_{i,PI}-v_C-R_1 i_1 - K_{ad}(i_1-i_2) $$

El término \( -K_{ad} i_1 \) actúa exactamente como una resistencia en serie con \( L_1 \) (su caída es proporcional a \( i_1 \)), y el \( -K_{ad}(-i_2) \) recupera que la corriente que pasa por el condensador es \( i_1-i_2 \): el conjunto emula una \( R_d \) vista por la rama del condensador. La diferencia con una resistencia física es que \( K_{ad} \) no disipa potencia real: es una consigna de tensión, no una caída óhmica. Por eso da el mismo amortiguamiento que \( R_d \) pero sin las pérdidas \( P_{R_d} \) (comparativa completa en [[amortiguamiento-pasivo-vs-activo]]).

**De dónde sale el modelo en espacio de estados (qué son las filas y columnas de \( A \)).** Un modelo en espacio de estados escribe la dinámica como \( \dot{\mathbf{x}}=A\mathbf{x}+B\mathbf{u} \), donde \( \mathbf{x} \) es el vector de estados — las variables que guardan la "memoria" del sistema, una por cada elemento que almacena energía — y \( \mathbf{u} \) las entradas externas. Aquí hay dos bobinas y un condensador, así que \( \mathbf{x}=[i_1,i_2,v_C]^T \): tres estados, matriz \( A \) de \( 3\times3 \). Cada **fila** de \( A \) es la ecuación de la derivada de un estado, en el mismo orden que \( \mathbf{x} \) (fila 1 → \( di_1/dt \), fila 2 → \( di_2/dt \), fila 3 → \( dv_C/dt \)); cada **columna** dice cuánto pesa cada estado, también en el orden \( i_1,i_2,v_C \), en esa derivada. Así, el elemento \( A_{ij} \) es el coeficiente con el que el estado \( j \)-ésimo entra en la ecuación de la derivada del estado \( i \)-ésimo; por ejemplo \( A_{12} \) (fila 1, columna 2) es cuánto pesa \( i_2 \) en \( di_1/dt \).

**Construcción paso a paso de \( A(K_{ad}) \).** Se parte de las tres ecuaciones de la sección **Ecuaciones de partida** (al principio de la ficha) y se despeja cada derivada dividiendo por su elemento de almacenamiento:

$$ \frac{di_1}{dt}=\frac{1}{L_1}\big(v_i-v_C-R_1 i_1\big), \qquad \frac{dv_C}{dt}=\frac{1}{C_f}(i_1-i_2), \qquad \frac{di_2}{dt}=\frac{1}{L_2}\big(v_C-v_{pcc}-R_2 i_2\big) $$

**Paso 1 — sustituir la ley de control.** \( v_i=v_{i,PI}-K_{ad}(i_1-i_2) \) es la tensión que el propio convertidor aplica en su terminal, así que solo entra en la ecuación de \( di_1/dt \) (las otras dos no dependen de \( v_i \)):

$$ \frac{di_1}{dt}=\frac{1}{L_1}\Big(v_{i,PI}-K_{ad}(i_1-i_2)-v_C-R_1 i_1\Big)=-\frac{R_1+K_{ad}}{L_1}\,i_1+\frac{K_{ad}}{L_1}\,i_2-\frac{1}{L_1}\,v_C+\frac{1}{L_1}\,v_{i,PI} $$

Es aquí donde nace el acoplamiento entre \( i_1 \) e \( i_2 \) que no existía antes: al meter \( K_{ad}\,i_2 \) dentro de la propia ecuación de \( i_1 \), ese término deja de ser una entrada externa y pasa a ser parte de la matriz de estados.

**Paso 2 — separar estados de entradas.** Los términos en \( i_1,i_2,v_C \) van a \( A \); los términos en \( v_{i,PI} \) y \( v_{pcc} \) no dependen de los estados, así que van a la matriz de entradas \( B \), no a \( A \):

$$ A=\begin{bmatrix} -\dfrac{R_1+K_{ad}}{L_1} & \dfrac{K_{ad}}{L_1} & -\dfrac{1}{L_1} \\[5pt] 0 & -\dfrac{R_2}{L_2} & \dfrac{1}{L_2} \\[5pt] \dfrac{1}{C_f} & -\dfrac{1}{C_f} & 0 \end{bmatrix}, \qquad B=\begin{bmatrix} 1/L_1 & 0 \\ 0 & -1/L_2 \\ 0 & 0\end{bmatrix},\qquad \mathbf{u}=\begin{bmatrix}v_{i,PI}\\ v_{pcc}\end{bmatrix} $$

**Paso 3 — aislar el efecto de \( K_{ad} \) (poner \( R_1=R_2=0 \)).** Las resistencias parásitas ya aportan su propio amortiguamiento, ya estudiado en el apartado 2; para ver solo lo que aporta \( K_{ad} \) se anulan \( R_1,R_2 \) y queda la matriz de la ficha:

$$ A(K_{ad})=\begin{bmatrix} -K_{ad}/L_1 & +K_{ad}/L_1 & -1/L_1 \\ 0 & 0 & 1/L_2 \\ 1/C_f & -1/C_f & 0 \end{bmatrix} $$

**Para qué se usa.** No es el modelo que se simula en el controlador real (ahí se usa la ley \( v_i=v_{i,PI}-K_{ad}(i_1-i_2) \) directamente). Sirve para **diseñar** \( K_{ad} \) sin tener que simular nada: anulando las entradas (\( v_{i,PI}=v_{pcc}=0 \), "anular las fuentes" — la misma técnica del apartado 2 para aislar la dinámica libre) los autovalores de \( A(K_{ad}) \) dan directamente el par de polos resonante para cada \( K_{ad} \), que es justo lo que se barre para producir la figura del lugar de polos de abajo.

**Cómo se implementa en el controlador real.** El lazo no añade hardware: son unas pocas líneas en el bucle de control digital que ya calcula la PWM. En cada periodo de muestreo:
1. Leer (o estimar) \( i_1[k] \) e \( i_2[k] \).
2. Calcular \( i_{C_f}[k]=i_1[k]-i_2[k] \).
3. Calcular \( v_i[k]=v_{i,PI}[k]-K_{ad}\,i_{C_f}[k] \), con \( v_{i,PI}[k] \) la salida normal de los lazos de tensión/corriente.
4. Enviar \( v_i[k] \) al modulador PWM como nueva consigna.

<div class="cfig"><img src="figuras/filtro-lcl-damping-bloques.png" alt="Diagrama de bloques del amortiguamiento activo: vi,PI menos Kad por (i1-i2) da vi, que entra al filtro LCL; i1 e i2 se realimentan y se restan para dar iCf, que multiplicado por Kad vuelve a la suma"><div class="cap">Lazo de amortiguamiento activo: \(i_1\) e \(i_2\) se miden, se resta uno del otro para obtener \(i_{C_f}\), se multiplica por \(K_{ad}\) y se resta a la salida del PI antes de generar \(v_i\). Es exactamente la sustitución del Paso 1: por eso \(K_{ad}\) acopla \(i_1\) e \(i_2\) dentro de \(A\).</div></div>

**Estudio de polos: cómo influye \( K_{ad} \) en el diseño (forma cerrada).** Los autovalores de \( A(K_{ad}) \) son las raíces de su polinomio característico, \( \det(sI-A(K_{ad}))=0 \): son los valores de \( s \) para los que el sistema homogéneo \( \dot{\mathbf{x}}=A\mathbf{x} \) admite una solución no trivial de la forma \( \mathbf{x}(t)=\mathbf{v}\,e^{st} \) (los modos propios de la dinámica libre), y por eso son exactamente los polos de la planta. A continuación se calcula ese determinante explícitamente, sin saltarse ningún paso.

**Paso 1 — formar \( sI-A(K_{ad}) \).** Restando \( A(K_{ad}) \) (apartado 4, Paso 3) de \( sI \) elemento a elemento:

$$ sI-A(K_{ad})=\begin{bmatrix} s+\dfrac{K_{ad}}{L_1} & -\dfrac{K_{ad}}{L_1} & \dfrac{1}{L_1} \\[6pt] 0 & s & -\dfrac{1}{L_2} \\[6pt] -\dfrac{1}{C_f} & \dfrac{1}{C_f} & s \end{bmatrix} $$

**Paso 2 — elegir cómo expandir el determinante.** Para una matriz \( 3\times3 \), \( \det(M)=\sum_j a_{1j}\,C_{1j} \) (expansión por cofactores de la primera fila), donde \( C_{1j}=(-1)^{1+j}M_{1j} \) y \( M_{1j} \) es el menor que queda al borrar la fila 1 y la columna \( j \). Conviene expandir por la primera fila porque ningún elemento de esa fila es cero, pero el resultado es el mismo por cualquier fila o columna que se elija.

**Paso 3 — los tres menores \( 2\times2 \).** Borrando fila 1 y cada columna a su vez:

$$ M_{11}=\det\begin{bmatrix} s & -1/L_2 \\ 1/C_f & s \end{bmatrix}=s^2-\left(-\frac{1}{L_2}\right)\!\left(\frac{1}{C_f}\right)=s^2+\frac{1}{L_2 C_f} $$

$$ M_{12}=\det\begin{bmatrix} 0 & -1/L_2 \\ -1/C_f & s \end{bmatrix}=0\cdot s-\left(-\frac{1}{L_2}\right)\!\left(-\frac{1}{C_f}\right)=-\frac{1}{L_2 C_f} $$

$$ M_{13}=\det\begin{bmatrix} 0 & s \\ -1/C_f & 1/C_f \end{bmatrix}=0\cdot\frac{1}{C_f}-s\left(-\frac{1}{C_f}\right)=\frac{s}{C_f} $$

(cada menor \( 2\times2 \) es, por definición, "producto de la diagonal principal menos producto de la diagonal secundaria"; no hace falta más que esa regla).

**Paso 4 — aplicar los signos de cofactor y sumar.** \( C_{11}=+M_{11} \), \( C_{12}=-M_{12} \), \( C_{13}=+M_{13} \) (signos \( +,-,+ \) alternados desde la posición \( (1,1) \)). Con los elementos de la primera fila del Paso 1:

$$ \det=\Big(s+\frac{K_{ad}}{L_1}\Big)\underbrace{\Big(s^2+\frac{1}{L_2C_f}\Big)}_{C_{11}} + \Big(-\frac{K_{ad}}{L_1}\Big)\underbrace{\Big(\frac{1}{L_2C_f}\Big)}_{C_{12}} + \Big(\frac{1}{L_1}\Big)\underbrace{\Big(\frac{s}{C_f}\Big)}_{C_{13}} $$

**Paso 5 — expandir el primer producto y agrupar.** Multiplicando \( \big(s+\tfrac{K_{ad}}{L_1}\big)\big(s^2+\tfrac{1}{L_2C_f}\big)=s^3+\dfrac{s}{L_2C_f}+\dfrac{K_{ad}}{L_1}s^2+\dfrac{K_{ad}}{L_1L_2C_f} \), y sumando los otros dos términos del Paso 4:

$$ \det=s^3+\frac{K_{ad}}{L_1}s^2+\frac{s}{L_2C_f}+\underbrace{\frac{K_{ad}}{L_1L_2C_f}-\frac{K_{ad}}{L_1L_2C_f}}_{=\,0}+\frac{s}{L_1C_f} $$

El término constante en \( K_{ad} \) (sin \( s \)) se cancela exactamente con el que viene del Paso 4: no es una casualidad numérica, es la razón por la que el polo en \( s=0 \) no depende de \( K_{ad} \) (si no se cancelara, \( K_{ad}=0 \) no sería raíz y \( s=0 \) no sería polo para ningún \( K_{ad} \), lo que contradice que sin amortiguar el filtro sigue teniendo ese integrador). Queda:

$$ \det=s^3+\frac{K_{ad}}{L_1}s^2+s\left(\frac{1}{L_1C_f}+\frac{1}{L_2C_f}\right)=s^3+\frac{K_{ad}}{L_1}s^2+s\cdot\frac{L_1+L_2}{L_1L_2C_f} $$

y como \( \omega_{res}^2=(L_1+L_2)/(L_1L_2C_f) \) (apartado 2), y todo término tiene al menos un factor \( s \):

$$ \det\!\big(sI-A(K_{ad})\big)=s\left(s^2+\frac{K_{ad}}{L_1}\,s+\omega_{res}^2\right) $$

que es el mismo \( s\,(s^2+\omega_{res}^2) \) que ya aparecía en el denominador de las funciones de transferencia del apartado 1, ahora con el término en \( s \) que aporta \( K_{ad} \). Comparando el factor entre paréntesis con la forma canónica \( s^2+2\zeta\omega_n s+\omega_n^2 \):

$$ \omega_n^2=\omega_{res}^2\ \Rightarrow\ \omega_n=\omega_{res}, \qquad 2\zeta\omega_n=\frac{K_{ad}}{L_1}\ \Rightarrow\ \boxed{\;\zeta=\frac{K_{ad}}{2\,L_1\,\omega_{res}}\;} $$

Es una fórmula **exacta**, no una aproximación: a diferencia de \( \zeta_{res}(R_1,R_2) \) (apartado 2, que sale de una perturbación a primer orden), aquí \( \omega_n \) no se mueve nada con \( K_{ad} \) — solo cambia \( \zeta \). Verificación numérica (\( L_1=2\,\text{mH},\,L_2=1\,\text{mH},\,C_f=20\,\mu\text{F} \), \( \omega_{res}=8660 \) rad/s): para \( K_{ad}=2,6,10,12\,\Omega \) la fórmula da \( \zeta=0.058,\,0.173,\,0.289,\,0.346 \), idéntico a los autovalores calculados numéricamente.

**Cómo ajustar \( K_{ad} \).** Al ser exacta, no hace falta barrer \( K_{ad} \) ni mirar el lugar de polos para diseñar: se despeja directamente para el \( \zeta \) objetivo (0.3–0.7, igual que en el amortiguamiento pasivo):

$$ K_{ad}=2\,\zeta_{objetivo}\,L_1\,\omega_{res} $$

Por ejemplo, con los valores de arriba y \( \zeta_{objetivo}=0.5 \): \( K_{ad}=2\times0.5\times(2\times10^{-3})\times8660\approx8.7\,\Omega \). El lugar de polos de la figura de abajo es la confirmación gráfica de esta fórmula (y la herramienta a usar si \( R_1,R_2 \) no son despreciables, donde la factorización exacta ya no se cumple), no el método de diseño en sí.

<div class="cfig"><img src="figuras/filtro-lcl-damping-polos.png" alt="lugar de los polos resonantes del LCL al barrer Kad, con lineas de zeta constante"><div class="cap">Lugar de los polos resonantes al barrer \(K_{ad}\) de 0 a 12 Ω: parten sobre el eje imaginario (\(\zeta\approx0\), rojo) y se mueven a la izquierda al subir \(K_{ad}\) (color), cruzando las líneas de \(\zeta\) constante. Coincide con \(\zeta=K_{ad}/(2L_1\omega_{res})\): la frecuencia (eje vertical) no se mueve, solo crece la parte real negativa.</div></div>

**Procedimiento de diseño.** Identificar \( f_{res} \) y elegir \( \zeta_{objetivo} \) (0.3–0.7); calcular \( K_{ad}=2\zeta_{objetivo}L_1\omega_{res} \); medir o estimar \( i_{C_f} \) como \( i_1-i_2 \); verificar en el lugar de polos que el resultado es razonable y que no degrada el margen de los lazos de corriente y tensión. Variantes: realimentar \( i_2 \) o la derivada de \( v_C \) en lugar de \( i_{C_f} \).

**Límites y errores.** Ganancia \( K_{ad} \) excesiva amplifica el ruido de medida y puede provocar inestabilidad de alta frecuencia; estimar \( i_{C_f} \) con retardo de muestreo significativo (\( 1.5\,T_s \)) le quita eficacia e incluso puede volver el damping negativo a frecuencias altas — por eso el retardo de cómputo acota el \( K_{ad} \) útil y, con él, el \( \zeta \) máximo alcanzable. En digital conviene compensar ese retardo (ver [[compensacion-retardo]]).

## 5 — Rizado de corriente y dimensionado de \( L_1 \) (derivación completa)
La bobina de lado fuente se dimensiona por el rizado de conmutación que deja pasar. Se deriva primero la versión reducida (tensión de salida constante dentro de un periodo de conmutación, que da la regla de diseño) y después el detalle (dependencia con el ciclo de trabajo y convención pico vs pico-pico).

### Versión reducida (tensión de salida ≈ constante en un periodo \( T_{sw} \))
**Paso 1 — punto de partida.** La ley de la bobina es \( v_L=L_1\,di_1/dt \), luego la corriente cambia con pendiente \( di_1/dt=v_L/L_1 \) mientras se le aplica una tensión \( v_L \). En un periodo de conmutación \( T_{sw}=1/f_{sw} \) el nudo \( v_C \) apenas se mueve (\( f_{sw}\gg \) frecuencia de red), así que se trata como constante e igual a la salida instantánea \( v_o \).

**Por qué la tensión del polo es cuadrada (y no continua).** Un IGBT o MOSFET de potencia solo tiene dos estados útiles: conduciendo a fondo (saturado, caída de tensión casi nula) o bloqueado (sin corriente). Operarlo en la región intermedia (lineal), para sacar una tensión de polo "analógica" cualquiera, significaría que el propio semiconductor cae una tensión intermedia mientras pasa toda la corriente de carga: disiparía \( V\cdot I \) como calor de forma continua, una potencia perdida del mismo orden que la potencia útil — inviable térmicamente a partir de unos pocos vatios, y completamente inviable en un convertidor de red de kW o MW. Por eso, en electrónica de potencia, el interruptor nunca se deja "a medias": el polo solo puede valer \( +V_{dc}/2 \) o \( -V_{dc}/2 \), nunca algo intermedio, y conmuta entre esos dos rails a \( f_{sw} \). La consigna "analógica" que sí importa (la tensión fundamental a 50/60 Hz) no se obtiene como un nivel de tensión propio, sino **repartiendo el tiempo** entre esos dos niveles dentro de cada periodo de conmutación: esa fracción de tiempo es el ciclo de trabajo \( d \), y variar \( d \) ciclo a ciclo para que el valor medio siga la consigna es exactamente la modulación PWM (ver [[convertidor-vsc|modulación PWM]]). El filtro LCL existe porque, aunque el polo es literalmente una onda cuadrada de amplitud \( V_{dc}/2 \), lo único que se quiere entregar a la carga es esa media — el resto (los armónicos de conmutación) hay que quitarlo, y de eso trata el rizado que se dimensiona a continuación.

**Paso 2 — tensión sobre \( L_1 \) en cada subintervalo.** El polo conmuta entre \( +V_{dc}/2 \) y \( -V_{dc}/2 \). La tensión sobre \( L_1 \) es la del polo menos \( v_o \):
- subintervalo "alto" (duración \( d\,T_{sw} \)): \( v_{L+}=+V_{dc}/2 - v_o \)
- subintervalo "bajo" (duración \( (1-d)T_{sw} \)): \( v_{L-}=-V_{dc}/2 - v_o \)

donde \( d \) es el ciclo de trabajo. Como el valor medio del polo debe igualar a \( v_o \), se cumple \( v_o=(2d-1)V_{dc}/2 \), de donde \( V_{dc}/2 - v_o = V_{dc}(1-d) \).

**Paso 3 — subida de corriente en el subintervalo alto.** La corriente sube con pendiente \( v_{L+}/L_1 \) durante \( d\,T_{sw} \), así que el rizado pico-pico es:

$$ \Delta i_{1,pp}=\frac{v_{L+}}{L_1}\,d\,T_{sw}=\frac{V_{dc}(1-d)}{L_1}\,d\,T_{sw}=\frac{V_{dc}\,T_{sw}}{L_1}\,d(1-d) $$

es decir, sustituyendo \( T_{sw}=1/f_{sw} \):

$$ \Delta i_{1,pp}=\frac{V_{dc}}{f_{sw} L_1}\,d(1-d) $$

<div class="cfig"><img src="figuras/filtro-lcl-rizado-onda.png" alt="Formas de onda: tension de polo conmutando entre +Vdc/2 y -Vdc/2 con los subintervalos d Tsw y (1-d)Tsw, y la corriente triangular subiendo y bajando"><div class="cap">Formas de onda durante un periodo de conmutación. Arriba: la tensión de polo conmuta entre \(+V_{dc}/2\) y \(-V_{dc}/2\); su media es \(v_o\); los subintervalos duran \(d\,T_{sw}\) y \((1-d)T_{sw}\). Abajo: la corriente de \(L_1\) sube con pendiente \(v_{L+}/L_1\) y baja con \(v_{L-}/L_1\), dibujando el rizado triangular \(\Delta i_{1,pp}\).</div></div>

**Paso 4 — caso peor (máximo rizado).** El producto \( d(1-d) \) es máximo en \( d=0.5 \) (salida instantánea nula, paso por cero de la senoide), donde vale \( 1/4 \). El rizado pico-pico máximo es:

$$ \Delta i_{1,pp,max}=\frac{V_{dc}}{4 f_{sw} L_1} $$

**Paso 5 — convención de la especificación y regla de diseño.** Si la especificación se da como amplitud del rizado (desviación de pico respecto a la media, que es la mitad del pico-pico), aparece el factor 8 habitual en la literatura de diseño de LCL:

$$ \Delta i_{1,amp}=\frac{\Delta i_{1,pp}}{2}=\frac{V_{dc}}{8 f_{sw} L_1} \;\Rightarrow\; \boxed{\,L_1=\frac{V_{dc}}{8 f_{sw}\,\Delta i_{1,amp}}\,} $$

(con pico-pico el factor es 4; con amplitud, 8 — conviene fijar cuál se usa). El valor objetivo típico es 10–20 % de la corriente nominal de pico \( I_n \). Más inductancia = menos rizado pero más caída y volumen.

<div class="cfig"><img src="figuras/filtro-lcl-rizado.png" alt="Izquierda: banda de rizado real sobre la fundamental i1, mas ancha en los pasos por cero y mas estrecha en los picos. Derecha: curva de diseno L1 minimo frente al rizado objetivo en porcentaje de In"><div class="cap">Izquierda: la banda de rizado sobre \(i_1\) (sombreado) se ensancha en los pasos por cero de \(v_o\) (\(d=0.5\), línea roja) y se estrecha en los picos (\(d\to0\) o \(1\), línea verde) — el mismo \(d(1-d)\) del Paso 4, visto sobre la corriente real. Derecha: curva de diseño directa — fijado el rizado objetivo (10–20 % de \(I_n\) es lo habitual) se lee el \(L_1\) mínimo necesario; menos rizado exige más inductancia.</div></div>

### Detalle (lo que la versión reducida obvia)
- La dependencia \( d(1-d) \) significa que el rizado no es constante a lo largo del ciclo de red: es máximo en el paso por cero (\( d\approx0.5 \)) y mínimo en los picos de la senoide (\( d\to0 \) o \( 1 \)). Dimensionar por \( d=0.5 \) es el caso peor.
- Se ha supuesto \( v_o \) constante en el periodo \( T_{sw} \); es exacto en el límite \( f_{sw}\gg f_0 \) y solo introduce un error de segundo orden.
- Efecto de \( R_1 \) (con vs sin resistencia serie): aquí es despreciable. Durante un subintervalo de conmutación (duración del orden de \( T_{sw} \), microsegundos) la caída \( R_1 i_1 \) apenas cambia frente a la tensión aplicada \( V_{dc}(1-d) \), así que la pendiente \( di_1/dt\approx v_L/L_1 \) no la fija \( R_1 \) sino \( L_1 \). La resistencia sí importa para la caída de tensión media y las pérdidas en régimen, pero no para el rizado de conmutación; por eso el dimensionado de \( L_1 \) se hace sin \( R_1 \).
- Si la etapa de entrada es de tres niveles, el escalón de tensión sobre \( L_1 \) se reduce a la mitad (\( \pm V_{dc}/4 \) efectivo por nivel), de modo que para el mismo rizado \( L_1 \) baja a la mitad; ver [[convertidor-vsc|modulación PWM]]. Con modulación vectorial (SVPWM) o inyección de tercer armónico el caso peor cambia ligeramente respecto al SPWM senoidal puro.

## 6 — Dimensionado de \( C_f \) (reactiva)
El condensador absorbe reactiva a la frecuencia de red. A continuación se deriva, sin saltarse ningún paso, de dónde sale \( I_C=\omega_0 C_f V \), por qué esa corriente es puramente reactiva (\( Q_C=VI_C \), sin parte activa) y por qué se limita al diseñar.

**Paso 1 — la tensión que ve \( C_f \) a la frecuencia fundamental.** En régimen permanente, e ignorando el rizado de conmutación de alta frecuencia (ya tratado en los apartados 5 y 7 — aquí solo interesa la componente a 50/60 Hz, que es la que fija cuánta reactiva hay que suministrar de forma continua), la tensión del nudo \( v_C \) sigue a la tensión de red:

$$ v_C(t)=\sqrt{2}\,V\sin(\omega_0 t) $$

donde \( V \) es el valor **RMS** de la tensión de fase (no de línea, no de pico — la distinción importa, ver Nota al final) y \( \omega_0=2\pi f_0 \). El factor \( \sqrt2 \) convierte el RMS, que es como se especifica habitualmente una tensión de red, en la amplitud de pico que aparece en la señal temporal.

**Paso 2 — corriente por \( C_f \) (ley constitutiva del condensador).** La rama del condensador ya se planteó en "Ecuaciones de partida": \( i_C=C_f\,dv_C/dt \). Derivando el Paso 1:

$$ i_C(t)=C_f\frac{d}{dt}\Big[\sqrt2\,V\sin(\omega_0 t)\Big]=\sqrt2\,V\,\omega_0 C_f\,\cos(\omega_0 t) $$

Es una señal senoidal con amplitud de pico \( \sqrt2\,V\,\omega_0 C_f \); dividiendo entre \( \sqrt2 \) (la misma conversión del Paso 1, ahora en sentido inverso) se obtiene su valor RMS:

$$ \boxed{\;I_C=\omega_0 C_f V\;} $$

**Paso 3 — por qué la corriente va en cuadratura (90°) con la tensión.** \( v_C(t)\propto\sin(\omega_0 t) \) e \( i_C(t)\propto\cos(\omega_0 t) \); como \( \cos\theta=\sin(\theta+90°) \), la corriente va adelantada 90° respecto a la tensión. Esto no es una coincidencia de este circuito: es la firma de cualquier elemento puramente reactivo. Al ser la derivada de un seno, la corriente es máxima exactamente donde la tensión pasa por cero, y nula donde la tensión es máxima — tensión y corriente nunca son grandes a la vez.

**Paso 4 — la potencia activa media es cero (de ahí "reactiva").** La potencia instantánea entregada al condensador es el producto:

$$ p(t)=v_C(t)\,i_C(t)=\big(\sqrt2\,V\sin\omega_0t\big)\big(\sqrt2\,V\omega_0C_f\cos\omega_0t\big)=2V^2\omega_0C_f\sin(\omega_0t)\cos(\omega_0t) $$

Usando la identidad trigonométrica \( 2\sin\theta\cos\theta=\sin2\theta \):

$$ p(t)=V^2\omega_0C_f\sin(2\omega_0t) $$

**De dónde sale \( I_C \) en vez de \( V^2 \).** El paso siguiente no añade nada nuevo: es sustituir, dentro de \( V^2\omega_0C_f \), la propia definición de \( I_C \) del Paso 2 (\( I_C=\omega_0C_fV \)). Separando un factor \( V \):

$$ V^2\omega_0C_f = V\cdot\big(V\,\omega_0C_f\big) = V\cdot I_C $$

— se reagrupan los mismos tres factores (\( V,\,V,\,\omega_0C_f \)) como \( V \) por (\( V\,\omega_0C_f \)), y ese paréntesis es exactamente \( I_C \). Por eso \( V^2 \) "desaparece": no se cancela ni se aproxima, se reescribe como \( V\cdot I_C \) porque \( I_C \) ya contiene un factor \( V \) dentro de su propia definición. Con esto:

$$ p(t)=V^2\omega_0C_f\sin(2\omega_0t)=V I_C\sin(2\omega_0t) $$

Esta forma con \( I_C \) es la que conviene seguir usando, porque \( Q_C=VI_C \) es la definición habitual de potencia reactiva (tensión por corriente, ambas RMS) y se generaliza igual a cualquier elemento reactivo, no solo a un condensador con su \( C_f \) explícito.

Esta potencia oscila al doble de la frecuencia de red (coherente con el Paso 3: cuando \( v_C \) e \( i_C \) tienen signos opuestos la potencia es negativa, el condensador devuelve energía) y su **media en un periodo es cero**: \( \overline{p(t)}=0 \). El condensador no disipa nada, solo intercambia energía dos veces por ciclo. Lo único que queda como número característico no nulo es la **amplitud** de esa oscilación de potencia — eso es, por definición, la potencia reactiva:

$$ Q_C \equiv \text{amplitud de } p(t) = V\,I_C $$

**Paso 5 — sustituir \( I_C \) del Paso 2.**

$$ Q_C=V\,I_C=V\,(\omega_0 C_f V)=\omega_0 C_f V^2 $$

que es la fórmula de partida de este apartado, ahora derivada en vez de enunciada.

**Paso 6 — por qué se limita (y de dónde sale el 5 %).** Esa reactiva no la "regala" la red: tiene que suministrarla el convertidor a través de \( L_1 \) (o, vista desde el otro lado, la red a través de \( L_2 \)), aunque no hace ningún trabajo útil — ocupa capacidad de corriente del convertidor, cuya corriente máxima está fijada por su potencia aparente nominal \( S_n=\sqrt{P^2+Q^2} \), y cambia el factor de potencia visto en el punto de conexión sin que lo pida la carga. El \( 5\% \) es una cifra de diseño habitual en la industria (no una constante física): suficientemente pequeña para que esa reactiva sea despreciable frente a la potencia activa, pero sin forzar a \( C_f \) a ser tan pequeño que perjudique la atenuación a \( f_{sw} \) que depende de él (apartado 7) — los apartados 6 y 7 compiten por el mismo grado de libertad (\( C_f \) grande ayuda a atenuar pero quita margen de reactiva). Imponiendo el límite sobre el resultado del Paso 5:

$$ Q_C=\omega_0 C_f V^2 \le 0.05\,S_n \;\Rightarrow\; C_f\le\frac{0.05\,S_n}{\omega_0 V^2} $$

**Nota — RMS, no de pico.** La fórmula del Paso 5 exige \( V \) en RMS porque así se definió en el Paso 1; \( Q=VI \) con magnitudes de pico daría el doble de lo correcto (un factor \( (\sqrt2)^2=2 \) de más). Es un error fácil de cometer porque en el apartado 5 (rizado de \( L_1 \)) las fórmulas usan magnitudes de pico, no RMS — convenciones distintas para preguntas distintas, conviene no mezclarlas.

## 7 — Dimensionado de \( L_2 \) (atenuación a \( f_{sw} \))
**Punto de partida — no hace falta un circuito nuevo.** La relación entre \( i_1 \) e \( i_2 \) ya se obtuvo en el apartado 1, Paso 3 (con \( v_{pcc}=0 \), red rígida): \( I_1=I_2(1+s^2L_2C_f) \). Es exactamente el divisor de corriente que se necesita aquí; solo falta despejar y evaluarlo en \( s=j\omega_{sw} \).

**Paso 1 — despejar \( i_2/i_1 \).**

$$ I_1=I_2\big(1+s^2L_2C_f\big) \;\Rightarrow\; \frac{I_2}{I_1}=\frac{1}{1+s^2L_2C_f} $$

**Paso 2 — evaluar en \( s=j\omega_{sw} \).** Sustituyendo \( s=j\omega_{sw} \) y usando \( (j\omega_{sw})^2=-\omega_{sw}^2 \):

$$ \frac{I_2}{I_1}(j\omega_{sw})=\frac{1}{1-\omega_{sw}^2L_2C_f} $$

Tomando módulo de ambos lados (cociente de complejos: el módulo de un cociente es el cociente de los módulos, y el numerador ya es real):

$$ \left|\frac{i_2}{i_1}\right|(\omega_{sw})=\frac{1}{\big|1-\omega_{sw}^2L_2C_f\big|} $$

que es exactamente la fórmula de partida de este apartado, ahora derivada en vez de enunciada.

**Paso 3 — por qué se puede despreciar el "1" del denominador.** \( f_{sw} \) (decenas de kHz) está muy por encima de la antiresonancia \( f_{ar}=\omega_{ar}/2\pi \) con \( \omega_{ar}=1/\sqrt{L_2C_f} \) (apartado 1, Paso 5; bajan ambas con la red, apartado 8).

**Por qué importa precisamente ese cociente \( \omega_{sw}/\omega_{ar} \) (y no el producto \( \omega_{sw}^2L_2C_f \) tal cual).** El producto \( \omega_{sw}^2L_2C_f \) tiene unidades (rad\(^2\)/s\(^2\) por F por H, que se cancelan hasta quedar adimensional, pero el VALOR concreto no dice nada por sí solo): no hay manera de "ver" si es mucho mayor que 1 sin calcularlo primero. Un cociente de dos frecuencias, en cambio, es directamente un número puro y comparable: \( \omega_{sw}/\omega_{ar} \) responde a la pregunta intuitiva "¿cuántas veces más alta es \( f_{sw} \) que \( f_{ar} \)?", que es exactamente lo que hay que saber para decidir si despreciar el "1". Para reescribir el producto como ese cociente basta usar la propia definición de \( \omega_{ar} \): de \( \omega_{ar}=1/\sqrt{L_2C_f} \) se eleva al cuadrado y se invierte, \( \omega_{ar}^2=1/(L_2C_f) \;\Rightarrow\; L_2C_f=1/\omega_{ar}^2 \), y sustituyendo en el producto:

$$ \omega_{sw}^2L_2C_f=\omega_{sw}^2\cdot\frac{1}{\omega_{ar}^2}=\left(\frac{\omega_{sw}}{\omega_{ar}}\right)^2 $$

Con \( f_{sw} \) en decenas de kHz y \( f_{ar} \) en pocos kHz (apartado 8: 2034 Hz o 1233 Hz en el ejemplo), ese cociente vale entre 5 y 10 largamente, de donde:

$$ \omega_{sw}^2L_2C_f=\left(\frac{\omega_{sw}}{\omega_{ar}}\right)^2\gg1 $$

y frente a un número mucho mayor que 1, el "\( 1 \)" no pesa:

$$ \big|1-\omega_{sw}^2L_2C_f\big|\approx\omega_{sw}^2L_2C_f \;\Rightarrow\; \left|\frac{i_2}{i_1}\right|(\omega_{sw})\approx\frac{1}{\omega_{sw}^2L_2C_f} $$

Dividiendo la condición \( \omega_{sw}^2L_2C_f\gg1 \) por \( \omega_{sw}C_f \) se obtiene \( \omega_{sw}L_2\gg1/(\omega_{sw}C_f) \): es la misma condición dicha de otra forma — la impedancia de \( L_2 \) a \( f_{sw} \) es mucho mayor que la de \( C_f \), así que casi toda la corriente de rizado prefiere el camino de menor impedancia (el condensador) en vez de seguir hacia \( L_2 \) y la red.

**Qué tan buena es la aproximación, en números.** El error relativo tiene forma cerrada. Dividiendo la aproximada entre la exacta y usando \( x\equiv\omega_{sw}/\omega_{ar}\gg1 \) (con lo que \( |1-x^2|=x^2-1 \)):

$$ \frac{\text{aprox.}}{\text{exacta}}=\frac{1/x^2}{1/(x^2-1)}=\frac{x^2-1}{x^2}=1-\frac{1}{x^2} $$

restando 1 a ambos lados se obtiene directamente el error relativo (aprox. menos exacta, dividido por exacta):

$$ \text{error}=\frac{\text{aprox.}-\text{exacta}}{\text{exacta}}=-\frac{1}{x^2}=-\left(\frac{f_{ar}}{f_{sw}}\right)^2 $$

el error cae con el **cuadrado** de cuánto se separan las dos frecuencias: con \( f_{sw}/f_{ar}=5 \) (separación todavía modesta) ya es solo del \( 4\,\% \); con \( 10 \), del \( 1\,\% \); con \( 20 \), del \( 0.25\,\% \). El panel izquierdo de la figura siguiente compara ambas curvas.

**Paso 4 — despejar \( L_2 \) para una atenuación objetivo \( k \).** Llamando \( k=|i_2/i_1| \) en \( f_{sw} \) al objetivo de diseño y despejando de la aproximación del Paso 3:

$$ k\approx\frac{1}{\omega_{sw}^2L_2C_f} \;\Rightarrow\; \boxed{\,L_2\approx\frac{1}{k\,C_f\,\omega_{sw}^2}\,} $$

**Qué valores de \( k \) se buscan en la práctica.** \( k \) no es un número libre: en la metodología de Reznik et al. (ya en la bibliografía de esta ficha) se diseña para un \( k \) de en torno al \( 10\text{–}20\,\% \) de la fundamental en \( f_{sw} \) — atenuar más exige más \( L_2 \) (más caída de tensión y coste de cobre/núcleo); atenuar menos delega más filtrado en \( C_f \) o en la inductancia de salida que ya exista (cableado, trafo — apartado 8). El panel derecho de la figura siguiente traza \( L_2 \) frente a \( k \) objetivo con los valores de este mismo ejemplo (\( C_f=29.8\,\mu\text{F} \), \( f_{sw}=10 \) kHz): para \( k=10\,\% \), \( L_2\approx85\,\mu\text{H} \); para \( k=20\,\% \), \( L_2\approx42\,\mu\text{H} \).

<div class="cfig"><img src="figuras/filtro-lcl-L2-atenuacion.png" alt="Izquierda: curvas exacta y aproximada de i2/i1 en funcion de fsw/far, con el error marcado en el rango tipico. Derecha: curva de diseno L2 en funcion de k objetivo, con los puntos k=10% y k=20% senalados y la banda de L2 que daria r entre 0.2 y 1"><div class="cap">Izquierda: la aproximación del Paso 3 (línea discontinua) prácticamente se solapa con la exacta (línea continua) en el rango típico \( f_{sw}/f_{ar}=5\text{–}15 \), con el error indicado en cada punto. Derecha: cuanto más exigente el \( k \) objetivo, menor el \( L_2 \) necesario; la banda verde marca el rango de \( L_2 \) que daría \( r=L_2/L_1 \) entre 0.2 y 1 con la \( L_1 \) de este ejemplo — nótese que no se solapa con la banda naranja de \( k \) típico, la tensión que se explica a continuación.</div></div>

**Por qué \( r=L_2/L_1 \) se comprueba después y no se fija antes.** \( L_1 \) ya se fijó por rizado (apartado 5) y \( L_2 \) se acaba de fijar por esta atenuación \( k \) (Paso 4): los dos cálculos son independientes, ninguno usa el resultado del otro. Por eso \( r=L_2/L_1 \) no es un parámetro que se elige al empezar el diseño, es una consecuencia que sale al final y que conviene comprobar.

**De dónde sale el rango práctico 0.2–1 (y qué significa salirse de él).** Dividiendo la definición de \( f_{res} \) (apartado 2) entre la de \( f_{ar} \) (apartado 1, Paso 5):

$$ \frac{f_{res}}{f_{ar}}=\sqrt{\frac{L_2}{L_{eq}}}=\sqrt{\frac{L_2\,(L_1+L_2)}{L_1L_2}}=\sqrt{\frac{L_1+L_2}{L_1}}=\sqrt{1+r} $$

(usando \( L_{eq}=L_1L_2/(L_1+L_2) \) del apartado 2 y \( r\equiv L_2/L_1 \)). Es una relación cerrada y exacta: cuánto se separan las dos frecuencias clave del filtro depende solo de \( r \), no de los valores absolutos de \( L_1,L_2,C_f \). Con \( r=0.2 \): \( f_{res}/f_{ar}=\sqrt{1.2}\approx1.10 \) (apenas un 10 % de separación, casi se solapan). Con \( r=1 \): \( f_{res}/f_{ar}=\sqrt2\approx1.41 \) (41 % de separación, claramente distinguibles). Por debajo de \( r\approx0.2 \) la antiresonancia que ayuda a estabilizar el lazo de \( i_1 \) (apartado 1, Paso 6) queda demasiado pegada a la resonancia, con poco margen entre ambas; por encima de \( r\approx1 \), \( L_2 \) pasa a ser mayor que \( L_1 \) — quien hace el trabajo más exigente, absorber el escalón completo de \( V_{dc} \) (apartado 5) — y si \( r \) sale ahí suele ser más barato revisar \( C_f \) (apartado 6) o relajar \( k \) que seguir subiendo \( L_2 \).

**Para qué sirve \( r \) en la práctica, más allá de comprobarlo al final.** Tres usos concretos:

1. **Diagnóstico de un conflicto de diseño entre apartados 6 y 7.** \( C_f \) (apartado 6) y \( L_2 \) (apartado 7) se calculan de forma independiente, pero comparten el mismo \( C_f \) en sus fórmulas — y eso los puede dejar incompatibles sin que ninguno de los dos cálculos, por separado, avise. En este mismo ejemplo (\( C_f=29.8\,\mu\text{F} \), el máximo que permite el \( 5\,\% \) de reactiva del apartado 6): con \( k=10\,\% \) (dentro del rango típico) sale \( L_2\approx85\,\mu\text{H} \) y por tanto \( r=L_2/L_1\approx0.03 \) — muy por debajo de 0.2. Para que \( r \) cayera en el rango práctico haría falta \( k\approx1.5\,\% \) (\( r=0.2 \)) o incluso \( k\approx0.3\,\% \) (\( r=1 \)), valores mucho más exigentes que el \( 10\text{–}20\,\% \) habitual — ver la banda naranja (\( k \) típico) y la banda verde (\( L_2 \) que da \( r \) en rango) en la figura anterior, que no se solapan. La lectura correcta no es "subir \( L_2 \) hasta que \( r \) entre en rango" (eso es justo lo que el Paso 4 — apartado anterior — desaconseja: sobredimensionar \( L_2 \) cuesta caída de tensión y cobre sin necesidad real de atenuación); es revisar si \( C_f \) se forzó sin necesidad al límite del \( 5\,\% \) (apartado 6 solo dice "como máximo", no "hay que usarlo todo") — un \( C_f \) menor sube \( L_2 \) para el mismo \( k \) y con ello sube \( r \) también, sin gastar más cobre del estrictamente necesario.
2. **Separación efectiva entre resonancia y antiresonancia**, ya cuantificada arriba con \( f_{res}/f_{ar}=\sqrt{1+r} \): \( r \) es, literalmente, la única variable de la que depende esa separación.
3. **Indicio (no verificado en una fuente primaria por quien escribe esta ficha) sobre el factor de potencia.** Algunas referencias de diseño de filtros LCL señalan que valores de \( r \) por encima de 0.5–0.6 empiezan a introducir una reducción apreciable (del orden de unos pocos puntos porcentuales) del factor de potencia visto desde la red, porque \( L_2 \) ya no es despreciable frente a la reactancia de magnetización/dispersión vista por la red. No se ha podido confirmar esta cifra contra el artículo original (acceso bloqueado), así que aquí se trata como una señal adicional para no quedarse en el extremo alto del rango 0.2–1 sin motivo, no como un límite con la misma solidez que el resto de fórmulas de este apartado.

## 8 — Efecto de la red y el trafo sobre el filtro
Hasta aquí el filtro se ha tratado aislado, con \( L_2 \) terminando en una fuente de tensión ideal. En la práctica, aguas abajo del PCC hay un transformador (inductancia de dispersión \( L_t \)) y la red real, vista como un equivalente Thévenin con inductancia \( L_g \) (mayor cuanto más débil la red — ver [[red-thevenin-scr]] para de dónde sale \( L_g \) a partir del SCR). A continuación se justifica, sin asumirlo, por qué ambas se suman en serie con \( L_2 \), y se deriva su efecto en cada magnitud ya calculada en los apartados anteriores.

**Paso 1 — por qué \( L_t \) y \( L_g \) se suman en serie con \( L_2 \) (justificar la topología).** La hipótesis necesaria es que la conexión es radial: entre el filtro, el transformador y el equivalente de red no hay ninguna otra rama ni carga conectada (si la hubiera, desviaría parte de la corriente y la suma directa que sigue ya no sería válida — es la única suposición real de este apartado, y conviene tenerla presente). Con esa hipótesis, la misma corriente \( i_2 \) que sale de \( L_2 \) es, por KCL en cada nudo intermedio, exactamente la misma que atraviesa \( L_t \) y luego \( L_g \): no hay otro camino para ella. Tres bobinas atravesadas por la misma corriente, una tras otra, son por definición una conexión en serie, y sus caídas de tensión (cada una proporcional a la misma \( di_2/dt \)) se suman:

$$ v_{L_2}+v_{L_t}+v_{L_g}=L_2\frac{di_2}{dt}+L_t\frac{di_2}{dt}+L_g\frac{di_2}{dt}=(L_2+L_t+L_g)\frac{di_2}{dt} $$

Esa suma tiene la misma forma que la ley de una sola bobina (\( v=L\,di/dt \)) con \( L=L_2+L_t+L_g \): vistas desde el filtro, las tres son indistinguibles de una sola inductancia equivalente

$$ \boxed{\;L_{2ef}=L_2+L_t+L_g\;} $$

**Paso 2 — por qué basta sustituir \( L_2\to L_{2ef} \) en las fórmulas ya derivadas.** El Paso 1 demuestra que, desde el punto de vista del filtro, \( L_{2ef} \) cumple exactamente la misma relación tensión-corriente que \( L_2 \) sola. Ninguna derivación anterior (apartados 1, 2, 3, 7) usó ninguna otra propiedad de \( L_2 \) más que esa relación \( v=L_2\,di_2/dt \); por tanto todas siguen siendo válidas sustituyendo \( L_2\to L_{2ef} \) sin repetir ningún paso:

| Magnitud | Fórmula (con \( L_2 \) aislado) | Con la red (\( L_2\to L_{2ef} \)) | Apartado de origen |
|---|---|---|---|
| Inductancia equivalente | \( L_{eq}=\dfrac{L_1L_2}{L_1+L_2} \) | \( L_{eq,ef}=\dfrac{L_1L_{2ef}}{L_1+L_{2ef}} \) | 2 |
| Resonancia | \( f_{res}=\dfrac{1}{2\pi\sqrt{L_{eq}C_f}} \) | \( f_{res,ef}=\dfrac{1}{2\pi}\sqrt{\dfrac{L_1+L_{2ef}}{L_1L_{2ef}C_f}} \) | 2 |
| Antiresonancia | \( f_{ar}=\dfrac{1}{2\pi\sqrt{L_2C_f}} \) | \( f_{ar,ef}=\dfrac{1}{2\pi\sqrt{L_{2ef}C_f}} \) | 1, Paso 5 |
| Factor \( Q \) (\( R_d \) fijo) | \( Q=\dfrac{1}{R_d}\sqrt{L_{eq}/C_f} \) | \( Q_{ef}=\dfrac{1}{R_d}\sqrt{L_{eq,ef}/C_f} \) | 3 |
| Atenuación a \( f_{sw} \) | \( k\approx\dfrac{1}{\omega_{sw}^2L_2C_f} \) | \( k_{ef}\approx\dfrac{1}{\omega_{sw}^2L_{2ef}C_f} \) | 7 |

**Paso 3 — ejemplo numérico (valores reales del proyecto 04).** Con \( L_1=40\,\mu\text{H},\ C_f=85\,\mu\text{F},\ L_2=8\,\mu\text{H},\ L_t=64\,\mu\text{H} \), dos escenarios:
- **Red fuerte** (\( L_g=0 \), SCR alto): \( L_{2ef}=L_2+L_t=72\,\mu\text{H} \).
- **Red débil** (\( L_g=124\,\mu\text{H} \), valor tomado directamente del modelo del proyecto 04 para su escenario de SCR≈2 — no se recalcula aquí con la fórmula simplificada de [[red-thevenin-scr]] porque esa fórmula necesita el \( X/R \) de la red, que en el modelo del proyecto no coincide con el del trafo): \( L_{2ef}=L_2+L_t+L_g=196\,\mu\text{H} \).

Aplicando la tabla del Paso 2 (cálculo directo, ningún paso adicional):

| | Red fuerte (\( L_{2ef}=72\,\mu\text{H} \)) | Red débil (\( L_{2ef}=196\,\mu\text{H} \)) | Variación |
|---|---|---|---|
| \( L_{eq,ef} \) | \( 25.7\,\mu\text{H} \) | \( 33.2\,\mu\text{H} \) | \( +29\% \) |
| \( f_{res,ef} \) | \( 3404 \) Hz | \( 2995 \) Hz | \( -12\% \) |
| \( f_{ar,ef} \) | \( 2034 \) Hz | \( 1233 \) Hz | \( -39\% \) |

**Paso 4 — por qué \( f_{ar} \) baja más deprisa que \( f_{res} \) (no es casualidad, sale de las propias fórmulas).** \( f_{ar,ef}\propto1/\sqrt{L_{2ef}} \): depende de \( L_{2ef} \) directamente. \( f_{res,ef}\propto1/\sqrt{L_{eq,ef}} \), y \( L_{eq,ef}=L_1L_{2ef}/(L_1+L_{2ef}) \) **satura** hacia \( L_1 \) cuando \( L_{2ef}\gg L_1 \) (en el límite, \( L_{eq,ef}\to L_1 \), constante, ya no crece con \( L_{2ef} \)). Por eso, al multiplicarse \( L_{2ef} \) por casi 3 (de 72 a 196 µH), \( L_{eq,ef} \) solo sube un 29 % en vez de también triplicarse, y \( f_{res,ef} \) (que depende de \( L_{eq,ef} \)) baja mucho menos que \( f_{ar,ef} \) (que depende de \( L_{2ef} \) sin atenuar). En red débil el margen de fase que aporta el cero de antiresonancia al usar \( i_1 \) como realimentación (apartado 1, Paso 6) se estrecha más de lo que sugeriría mirar solo \( f_{res} \).

**Paso 5 — efecto sobre el amortiguamiento \( \zeta \) y el factor \( Q \) (con \( R_d \) o \( K_{ad} \) ya fijados).** Si el amortiguamiento se diseñó para la red fuerte y no se retoca, \( R_d \) (o \( K_{ad} \)) queda fijo mientras \( L_{eq,ef} \) cambia. De la fórmula \( Q_{ef}=(1/R_d)\sqrt{L_{eq,ef}/C_f} \) (apartado 3) con \( R_d,C_f \) constantes, el cociente entre los dos escenarios es:

$$ \frac{Q_{ef,\text{débil}}}{Q_{ef,\text{fuerte}}}=\sqrt{\frac{L_{eq,ef,\text{débil}}}{L_{eq,ef,\text{fuerte}}}}=\sqrt{\frac{33.2}{25.7}}\approx1.14 $$

es decir, un \( 14\% \) más de \( Q \) (pico de resonancia algo más alto) en red débil, con el mismo \( R_d \) sin tocar. El amortiguamiento empeora ligeramente justo en el caso (red débil) donde más hace falta, así que hay que verificarlo ahí, no solo en la red fuerte.

**Paso 6 — efecto sobre la atenuación a \( f_{sw} \) (mejora, pero no es controlable).** De \( k_{ef}\approx1/(\omega_{sw}^2L_{2ef}C_f) \) (apartado 7) con \( \omega_{sw},C_f \) fijos, el cociente entre tener \( L_2 \) sola y tener \( L_{2ef} \) es simplemente \( L_2/L_{2ef} \):

$$ \frac{k_{ef}}{k}=\frac{L_2}{L_{2ef}} $$

Con los valores del Paso 3: en red fuerte, \( k_{ef}/k=8/72\approx0.11 \) (atenuación real \( \approx9\times \) mejor que si solo existiera \( L_2 \), gracias solo al trafo); en red débil, \( k_{ef}/k=8/196\approx0.041 \) (\( \approx24\times \) mejor). La mejora es real, pero depende de cuánta inductancia externa haya — algo que el diseñador no controla y que puede no estar ahí (p. ej. en pruebas en banco sin red ni trafo, o en isla) — así que nunca debe contarse como margen de diseño: el cálculo del apartado 7 sin red es el que define el \( L_2 \) propio del filtro, y esta mejora es solo un bonus cuando aparece.

**Regla de verificación.** Recalcular siempre \( f_{res} \), \( f_{ar} \), \( \zeta \) y \( Q \) — no solo \( f_{res} \) — con el peor caso de \( L_g \) (SCR mínimo esperado, y \( L_t \) del trafo real si lo hay), usando la sustitución \( L_2\to L_{2ef} \) del Paso 2, y comprobar que el amortiguamiento sigue siendo suficiente en todo el rango.

## Cuándo y por qué se usa
Estándar a la salida de cualquier convertidor conectado a red (PV, eólica, baterías, STATCOM) por la normativa de inyección de armónicos, y también alimentando cargas sensibles en isla. Se prefiere al filtro L cuando se busca menos inductancia total / menor caída para la misma atenuación. La resonancia aparece en cuanto un lazo rápido o la impedancia de red excita la zona de \( f_{res} \); es crítica en red débil, donde \( L_g \) baja \( f_{res} \) y la mete en la banda de control.

## Procedimiento de diseño (genérico)
1. \( L_1 \) por rizado: \( L_1=V_{dc}/(8 f_{sw}\,\Delta i_{1,amp}) \), con \( \Delta i_{1,amp}=10\text{–}20\% \) de \( I_n \).
2. \( C_f \) por reactiva: \( C_f\le0.05\,S_n/(\omega_0 V^2) \).
3. \( L_2 \) por atenuación a \( f_{sw} \): \( L_2\approx1/(k C_f\omega_{sw}^2) \), con \( r=L_2/L_1 \) entre 0.2 y 1.
4. Coloca \( f_{res} \) en banda holgada: \( 10 f_0 < f_{res} < f_{sw}/2 \).
5. Elige la corriente de realimentación: \( i_1 \) (lado fuente, con su cero de antiresonancia) da más margen que \( i_2 \).
6. Añade amortiguamiento: pasivo \( R_d\approx1/(3\omega_{res}C_f) \) en serie con \( C_f \), o activo por software (\( K_{ad} \) sobre \( i_{C_f} \)).
7. Verifica en red débil: recalcula \( f_{res} \) con \( L_2+L_{g,max} \) (SCR mínimo) y comprueba que el par resonante mantiene \( \zeta \) entre 0.1 y 0.3.

## Ejemplo de código
```python
import numpy as np
from control import tf

# Diseño: 10 kVA, 400 V (Vll), 50 Hz, Vdc=700 V, fsw=10 kHz, rizado 15% de In
Sn, Vll, f0, Vdc, fsw, rip = 10e3, 400, 50, 700, 10e3, 0.15
w0, wsw = 2*np.pi*f0, 2*np.pi*fsw
Vrms = Vll/np.sqrt(3)                      # rms de fase (para Qc=w0*Cf*Vrms^2, apartado 6)
In   = (Sn/(np.sqrt(3)*Vll))*np.sqrt(2)    # pico de fase nominal (para el rizado, apartado 5)

L1 = Vdc/(8*fsw*rip*In)                    # por rizado
Cf = 0.05*Sn/(w0*Vrms**2)                  # por reactiva (<=5%); Qc=V*Ic exige V en RMS, no de pico
L2 = 1/(0.10*Cf*wsw**2)                    # atenuacion objetivo k=0.10 a fsw

Leq   = L1*L2/(L1+L2)                       # inductancia equivalente paralelo
f_res = 1/(2*np.pi*np.sqrt(Leq*Cf))        # resonancia (exacta)
f_ar  = 1/(2*np.pi*np.sqrt(L2*Cf))         # antiresonancia (cero de i1)
Rd    = 1/(3*(2*np.pi*f_res)*Cf)           # amortiguamiento pasivo optimo

# Plantas (red rigida, R despreciable):
G_i2 = tf([1], [L1*L2*Cf, 0, (L1+L2), 0])              # lado red: solo resonancia
G_i1 = tf([L2*Cf, 0, 1], [L1*L2*Cf, 0, (L1+L2), 0])    # lado fuente: + antiresonancia
print(f"L1={L1*1e3:.2f} mH  Cf={Cf*1e6:.1f} uF  L2={L2*1e3:.2f} mH  f_res={f_res:.0f} Hz  f_ar={f_ar:.0f} Hz")
```

## Parámetros y valores típicos
- Banda de resonancia: \( 10 f_0 < f_{res} < f_{sw}/2 \).
- \( \Delta i_{1,pp} \): 10–20 % de \( I_n \). \( C_f \): \( \le5\% \) de \( S_n \) en reactiva. \( r=L_2/L_1 \): 0.2–1.
- Amortiguamiento objetivo del par resonante: \( \zeta \) entre 0.1 y 0.3. \( R_d \) pasivo de unos pocos ohmios; \( K_{ad} \) activo de unos pocos ohmios (en el proyecto, 6 Ω).
- Proyecto (10 kVA / 400 V / 50 Hz, \( f_{sw}=10 \) kHz): \( L_1=2 \) mH, \( C_f=20\,\mu\text{F} \), \( L_2=1 \) mH → \( f_{res}\approx1.38 \) kHz y \( f_{ar}\approx1.13 \) kHz (LCL aislado). En el modelo \( dq \) completo, con la inductancia de red, el modo resonante baja a \( \approx1.1 \) kHz con \( \zeta\approx0.13 \) (ya amortiguado).

## Errores comunes
- Realimentar \( i_2 \) (lado red) directamente: sin el cero de antiresonancia el margen de fase se desploma al acercarse a \( f_{res} \). Preferir \( i_1 \) o amortiguar.
- Dejar \( f_{res} \) demasiado cerca del ancho de banda de control → resonancia excitada.
- Olvidar el amortiguamiento → polos resonantes con \( \zeta\approx0 \).
- Ignorar \( L_g \) en red débil → \( f_{res} \) baja y entra en la banda del control.
- Sobredimensionar \( C_f \) (demasiada reactiva) o \( L_2 \) (caída y coste); sobre-amortiguar con \( R_d \) grande (pérdidas y peor atenuación a \( f_{sw} \)).
- Confundir resonancia (par de polos, vista en \( i_2 \)) con antiresonancia (par de ceros, en \( i_1 \)).

## Uso en proyectos
- 01 - GFM-Impedance (modelar la planta): el LCL aporta 6 de los 15 estados del modelo. Su modo resonante (≈1.1 kHz, \( \zeta\approx0.13 \)) obligó a añadir amortiguamiento activo con \( K_{ad}=6\,\Omega \) para poder subir el lazo de tensión a 350 Hz.
- 02 - GFL-Impedance (estabilidad en red débil): el mismo LCL obliga a mantener el lazo de corriente / PLL por debajo de \( f_{res} \), que además baja al debilitarse la red.

## Conceptos relacionados
- [[convertidor-vsc|modulación PWM]] · [[marco-dq]] · [[antiresonancia]] · [[resonancia-rlc]] · [[factor-calidad-q]] · [[amortiguamiento-pasivo-vs-activo]] · [[impedancia-salida-estabilidad]] · [[control-cascada]] · [[diagrama-bode]] · [[red-thevenin-scr]]

## Referencias
- Reznik et al., *LCL Filter Design...*, IEEE TIA 2014.
- Dannehl et al., *Investigation of Active Damping Approaches for LCL Filters*, IEEE TIA 2010.
- Wang, Blaabjerg, *Harmonic Stability in Power-Electronic-Based Power Systems*, IEEE TPEL 2014.
- Mohan, Undeland, Robbins, *Power Electronics*, Wiley 2003.
