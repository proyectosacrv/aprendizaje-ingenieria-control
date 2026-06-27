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
fecha_actualizacion: 2026-06-17
relacionados: [convertidor-vsc, marco-dq, impedancia-salida-estabilidad, control-cascada, diagrama-bode, antiresonancia, resonancia-rlc, amortiguamiento-pasivo-vs-activo, frecuencias-segundo-orden, factor-calidad-q]
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

Por eso el diseño del LCL no depende de la naturaleza del convertidor, solo de tres datos de esa etapa: la tensión de bus disponible (que fija la amplitud del troceado), la frecuencia de conmutación \( f_{sw} \) (que fija dónde están los armónicos a atenuar) y la ganancia del modulador (que cambia si la etapa es de dos niveles, tres niveles, etc.). Aguas abajo de \( L_2 \) hay un punto de conexión (PCC) detrás del cual puede haber una red, un transformador, otras cargas o una isla; su inductancia se suma a \( L_2 \) y modifica la resonancia (ver Desarrollo 3).

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

## Desarrollo 1 — funciones de transferencia (derivación completa)
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

No es una suposición: \( \omega_{res}^2 \) es, literalmente, el coeficiente que aparece al factorizar, y se identifica con la frecuencia natural por la forma canónica de segundo orden. El denominador se anula en \( s=0 \) y en \( s=\pm j\omega_{res} \): un par de polos sin parte real (\( \zeta\approx0 \)). Eso es la resonancia. El **porqué físico** (anular las dos fuentes y resolver el circuito libre) se deriva paso a paso en el Desarrollo 2; aquí ha aparecido como consecuencia algebraica de la planta.

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

Las dos comparten el denominador \( D(s)=Z_1+Z_2+sC_f Z_1 Z_2 \), que desarrollado es el polinomio característico completo (el mismo que el del Desarrollo 2):

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

## Desarrollo 2 — frecuencia de resonancia (derivación completa)
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

que es idéntica a la del paso 5 (resonancia de \( C_f \) contra \( L_1 \) paralelo \( L_2 \)). Esto coincide con el denominador de las funciones de transferencia del Desarrollo 1: \( s^3 L_1 L_2 C_f + s(L_1+L_2)=s L_1 L_2 C_f(s^2+\omega_{res}^2) \), cuyos ceros no nulos son justo \( s=\pm j\omega_{res} \).

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

## Desarrollo 3 — efecto de la red y el trafo sobre \( f_{res} \)
Cuando el filtro no trabaja en vacío sino conectado a una red con inductancia \( L_g \) (y a un trafo con \( L_t \)), esas inductancias se suman en serie con \( L_2 \). La frecuencia de resonancia efectiva baja:

$$ L_{2ef}=L_2+L_t+L_g, \qquad f_{res,ef}=\frac{1}{2\pi}\sqrt{\frac{L_1+L_{2ef}}{L_1 L_{2ef} C_f}} $$

Esto es crítico en red débil: un SCR bajo significa \( L_g \) grande, lo que empuja \( f_{res} \) hacia abajo y puede acercarla al ancho de banda del control. Regla de verificación: calcular siempre \( f_{res} \) con el peor caso de \( L_g \) (SCR mínimo esperado).

Ejemplo con valores del proyecto 04 (\( L_1=40\,\mu\text{H},\ C_f=85\,\mu\text{F},\ L_2=8\,\mu\text{H},\ L_t=64\,\mu\text{H} \)):
- SCR 5 (\( L_g=0 \)): \( L_{2ef}=72\,\mu\text{H} \), \( L_{eq}=25.7\,\mu\text{H} \), \( f_{res}=3406 \) Hz
- SCR 2 (\( L_g=124\,\mu\text{H} \)): \( L_{2ef}=196\,\mu\text{H} \), \( L_{eq}=33.2\,\mu\text{H} \), \( f_{res}=2997 \) Hz

La resonancia baja unos 400 Hz al pasar de SCR 5 a SCR 2. El amortiguamiento debe funcionar en todo ese rango.

## Desarrollo 4 — factor de calidad Q (derivación y efecto en la respuesta)
El factor de calidad \( Q \) mide cuántas veces amplifica el filtro una excitación justo en \( f_{res} \) (la altura del pico de resonancia).

**De dónde sale.** Para un par de polos de segundo orden con amortiguamiento \( \zeta \), la ganancia en el pico respecto a la banda de paso es \( Q=1/(2\zeta) \) (derivación general, energética y de ancho de banda, en [[factor-calidad-q]]). Combinándolo con el amortiguamiento que introduce una \( R_d \) en serie con \( C_f \) (Desarrollo 2):

$$ Q=\frac{1}{2\zeta}=\frac{1}{R_d\sqrt{C_f(L_1+L_2)/(L_1 L_2)}}=\frac{1}{R_d}\sqrt{\frac{L_{eq}}{C_f}} $$

es decir, \( Q \) es la relación entre la impedancia característica del tanque \( \sqrt{L_{eq}/C_f} \) y la resistencia de amortiguamiento \( R_d \). Sin resistencias (\( R_d\to0 \)) \( Q\to\infty \) y el pico es teóricamente infinito; con resistencias reales pequeñas \( Q \) sigue siendo alto (típico 10–50 en LCLs de potencia), lo que hace imprescindible amortiguar.

**Caso de estudio: efecto de Q sobre la respuesta.** Al subir el amortiguamiento (bajar \( Q \)) el pico de resonancia baja y se ensancha, mientras la banda de paso y la caída de \( -60 \) dB/dec por encima quedan casi intactas. La resistencia de amortiguamiento pasivo óptima en serie con \( C_f \) es:

$$ R_d\approx\frac{1}{3\,\omega_{res} C_f} $$

que deja \( Q\approx3 \) (un compromiso entre acotar el pico y no degradar la atenuación a \( f_{sw} \)). Por debajo de eso el pico sigue siendo peligroso; muy por encima se sobre-amortigua y se pierde atenuación.

<div class="cfig"><img src="figuras/filtro-lcl-factorQ.png" alt="Bode de |i2/vi| para varios valores de Q mostrando el pico de resonancia cada vez más bajo"><div class="cap">Efecto del factor \(Q\) sobre \(|i_2/v_i|\): sin amortiguar (\(Q\to\infty\)) el pico es enorme; al añadir \(R_d\) el pico baja y se ensancha. Con \(R_d\) óptimo (\(Q\approx3\)) queda acotado sin estropear la atenuación a \(f_{sw}\); sobre-amortiguar (\(Q\) bajo) no aporta y empeora el filtrado.</div></div>

El inconveniente del amortiguamiento pasivo es que \( R_d \) disipa potencia, \( P_{R_d}=R_d\,I_{C_f,rms}^2 \). Por eso en inversores de potencia media-alta se prefiere el amortiguamiento activo por software (ver más abajo y [[amortiguamiento-pasivo-vs-activo]]), que consigue el mismo \( \zeta \) sin pérdidas.

## Desarrollo 5 — rizado de corriente y dimensionado de \( L_1 \) (derivación completa)
La bobina de lado fuente se dimensiona por el rizado de conmutación que deja pasar. Se deriva primero la versión reducida (tensión de salida constante dentro de un periodo de conmutación, que da la regla de diseño) y después el detalle (dependencia con el ciclo de trabajo y convención pico vs pico-pico).

### Versión reducida (tensión de salida ≈ constante en un periodo \( T_{sw} \))
**Paso 1 — punto de partida.** La ley de la bobina es \( v_L=L_1\,di_1/dt \), luego la corriente cambia con pendiente \( di_1/dt=v_L/L_1 \) mientras se le aplica una tensión \( v_L \). En un periodo de conmutación \( T_{sw}=1/f_{sw} \) el nudo \( v_C \) apenas se mueve (\( f_{sw}\gg \) frecuencia de red), así que se trata como constante e igual a la salida instantánea \( v_o \).

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

<div class="cfig"><img src="figuras/filtro-lcl-rizado.png" alt="Izquierda: rizado a lo largo del ciclo de red para dos L1. Derecha: rizado pico-pico máximo frente a L1 con las líneas de 10% y 20% de In"><div class="cap">Izquierda: el rizado sigue \(d(1-d)\), máximo en el paso por cero de la senoide y mínimo en los picos; doblar \(L_1\) lo reduce a la mitad. Derecha: rizado p-p máximo frente a \(L_1\); fijar el objetivo (10–20 % de \(I_n\)) determina el \(L_1\) mínimo — diseñar para menos rizado exige más inductancia.</div></div>

### Detalle (lo que la versión reducida obvia)
- La dependencia \( d(1-d) \) significa que el rizado no es constante a lo largo del ciclo de red: es máximo en el paso por cero (\( d\approx0.5 \)) y mínimo en los picos de la senoide (\( d\to0 \) o \( 1 \)). Dimensionar por \( d=0.5 \) es el caso peor.
- Se ha supuesto \( v_o \) constante en el periodo \( T_{sw} \); es exacto en el límite \( f_{sw}\gg f_0 \) y solo introduce un error de segundo orden.
- Efecto de \( R_1 \) (con vs sin resistencia serie): aquí es despreciable. Durante un subintervalo de conmutación (duración del orden de \( T_{sw} \), microsegundos) la caída \( R_1 i_1 \) apenas cambia frente a la tensión aplicada \( V_{dc}(1-d) \), así que la pendiente \( di_1/dt\approx v_L/L_1 \) no la fija \( R_1 \) sino \( L_1 \). La resistencia sí importa para la caída de tensión media y las pérdidas en régimen, pero no para el rizado de conmutación; por eso el dimensionado de \( L_1 \) se hace sin \( R_1 \).
- Si la etapa de entrada es de tres niveles, el escalón de tensión sobre \( L_1 \) se reduce a la mitad (\( \pm V_{dc}/4 \) efectivo por nivel), de modo que para el mismo rizado \( L_1 \) baja a la mitad; ver [[convertidor-vsc|modulación PWM]]. Con modulación vectorial (SVPWM) o inyección de tercer armónico el caso peor cambia ligeramente respecto al SPWM senoidal puro.

## Desarrollo 6 — dimensionado de \( C_f \) (reactiva)
El condensador absorbe reactiva a la frecuencia de red: corriente \( I_C=\omega_0 C_f V \), luego \( Q_C=V I_C=\omega_0 C_f V^2 \). Se limita a un \( \le5\% \) de la potencia base para no cargar la fuente con reactiva inútil:

$$ Q_C=\omega_0 C_f V^2 \le 0.05\,S_n \;\Rightarrow\; C_f\le\frac{0.05\,S_n}{\omega_0 V^2} $$

## Desarrollo 7 — dimensionado de \( L_2 \) (atenuación a \( f_{sw} \))
Muy por encima de \( f_{res} \), la impedancia del condensador \( 1/(\omega C_f) \) es mucho menor que \( \omega L_2 \), así que casi todo el rizado se deriva por \( C_f \). El divisor de corriente da la atenuación de lado fuente a lado red:

$$ \left|\frac{i_2}{i_1}\right|(\omega_{sw})\approx\frac{1}{|1-\omega_{sw}^2 L_2 C_f|}\approx\frac{1}{\omega_{sw}^2 L_2 C_f} $$

Para una atenuación objetivo \( k=i_2/i_1 \) a \( f_{sw} \) se despeja:

$$ L_2\approx\frac{1}{k\,C_f\,\omega_{sw}^2} $$

Relación práctica \( L_2/L_1 \) entre 0.2 y 1. Conviene definir \( r=L_2/L_1 \) y comprobar después que \( f_{res} \) cae en banda.

## Amortiguamiento activo (derivación, estudio de polos y diseño)
En vez de disipar en una \( R_d \) física, se emula una resistencia de amortiguamiento por software. La técnica habitual realimenta la corriente del condensador \( i_{C_f}=i_1-i_2 \) a la tensión de la fuente con ganancia \( K_{ad} \):

$$ v_i = v_{i,PI} - K_{ad}\,(i_1-i_2) $$

**Por qué equivale a una resistencia sin pérdidas (desarrollo).** La dinámica de \( i_1 \) sin amortiguar es \( L_1\,di_1/dt=v_i-v_C-R_1 i_1 \). Sustituyendo la ley de control:

$$ L_1\frac{di_1}{dt}=v_{i,PI}-v_C-R_1 i_1 - K_{ad}(i_1-i_2) $$

El término \( -K_{ad} i_1 \) actúa exactamente como una resistencia en serie con \( L_1 \) (su caída es proporcional a \( i_1 \)), y el \( -K_{ad}(-i_2) \) recupera que la corriente que pasa por el condensador es \( i_1-i_2 \): el conjunto emula una \( R_d \) vista por la rama del condensador. La diferencia con una resistencia física es que \( K_{ad} \) no disipa potencia real: es una consigna de tensión, no una caída óhmica. Por eso da el mismo amortiguamiento que \( R_d \) pero sin las pérdidas \( P_{R_d} \) (comparativa completa en [[amortiguamiento-pasivo-vs-activo]]).

**Estudio de polos: cómo influye \( K_{ad} \) en el diseño.** Anulando las fuentes y reescribiendo el modelo con la realimentación activa, la matriz de estado del filtro (estados \( i_1,i_2,v_C \); \( R_1=R_2=0 \) para aislar el efecto) es:

$$ A(K_{ad})=\begin{bmatrix} -K_{ad}/L_1 & +K_{ad}/L_1 & -1/L_1 \\ 0 & 0 & 1/L_2 \\ 1/C_f & -1/C_f & 0 \end{bmatrix} $$

Los autovalores de \( A(K_{ad}) \) son el par resonante. En \( K_{ad}=0 \) están sobre el eje imaginario en \( \pm j\omega_{res} \) (\( \zeta=0 \)). Al subir \( K_{ad} \), el par se desplaza hacia la izquierda (parte real negativa creciente): el amortiguamiento sube de forma casi proporcional a \( K_{ad} \) mientras la frecuencia del par apenas cambia. Esto convierte el diseño en directo: se barre \( K_{ad} \) hasta cruzar la línea de \( \zeta \) objetivo.

<div class="cfig"><img src="figuras/filtro-lcl-damping-polos.png" alt="lugar de los polos resonantes del LCL al barrer Kad, con lineas de zeta constante"><div class="cap">Lugar de los polos resonantes al barrer \(K_{ad}\) de 0 a 12 Ω: parten sobre el eje imaginario (\(\zeta\approx0\), rojo) y se mueven a la izquierda al subir \(K_{ad}\) (color), cruzando las líneas de \(\zeta\) constante. El diseño consiste en elegir el \(K_{ad}\) que lleva el par al \(\zeta\) objetivo (0.3–0.7) sin pasarse.</div></div>

**Procedimiento de diseño.** Identificar \( f_{res} \); medir o estimar \( i_{C_f} \) como \( i_1-i_2 \); barrer \( K_{ad} \) (del orden de unos pocos ohmios) observando el lugar de polos hasta el \( \zeta \) objetivo de la resonancia (0.3–0.7); verificar que no degrada el margen de los lazos de corriente y tensión. Variantes: realimentar \( i_2 \) o la derivada de \( v_C \) en lugar de \( i_{C_f} \).

**Límites y errores.** Ganancia \( K_{ad} \) excesiva amplifica el ruido de medida y puede provocar inestabilidad de alta frecuencia; estimar \( i_{C_f} \) con retardo de muestreo significativo (\( 1.5\,T_s \)) le quita eficacia e incluso puede volver el damping negativo a frecuencias altas — por eso el retardo de cómputo acota el \( K_{ad} \) útil y, con él, el \( \zeta \) máximo alcanzable. En digital conviene compensar ese retardo (ver [[compensacion-retardo]]).

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
V  = Vll*np.sqrt(2/3)                      # pico de fase
In = (Sn/(np.sqrt(3)*Vll))*np.sqrt(2)      # pico de fase nominal

L1 = Vdc/(8*fsw*rip*In)                    # por rizado
Cf = 0.05*Sn/(w0*V**2)                     # por reactiva (<=5%)
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
- [[convertidor-vsc|modulación PWM]] · [[marco-dq]] · [[antiresonancia]] · [[resonancia-rlc]] · [[factor-calidad-q]] · [[amortiguamiento-pasivo-vs-activo]] · [[impedancia-salida-estabilidad]] · [[control-cascada]] · [[diagrama-bode]]

## Referencias
- Reznik et al., *LCL Filter Design...*, IEEE TIA 2014.
- Dannehl et al., *Investigation of Active Damping Approaches for LCL Filters*, IEEE TIA 2010.
- Wang, Blaabjerg, *Harmonic Stability in Power-Electronic-Based Power Systems*, IEEE TPEL 2014.
- Mohan, Undeland, Robbins, *Power Electronics*, Wiley 2003.
