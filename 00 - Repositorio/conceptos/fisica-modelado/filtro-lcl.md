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
fecha_actualizacion: 2026-06-16
relacionados: [convertidor-vsc, marco-dq, impedancia-salida-estabilidad, control-cascada, diagrama-bode, antiresonancia, resonancia-rlc]
referencias:
  - "Reznik et al., LCL Filter Design and Performance Analysis for Grid-Interconnected Systems, IEEE TIA 2014"
  - "Dannehl et al., Investigation of Active Damping Approaches for LCL Filters, IEEE TIA 2010"
  - "Wang, Blaabjerg, Harmonic Stability in Power-Electronic-Based Power Systems, IEEE TPEL 2014"
  - "Mohan, Undeland, Robbins, Power Electronics, Wiley 2003 (cap. rizado e inductancias)"
---

## Definición
El filtro LCL es una red de tercer orden L1–Cf–L2 que se coloca a la salida de cualquier fuente de tensión conmutada para entregar a la red (o a una carga) una corriente limpia a partir de una tensión troceada. Atenúa el rizado de conmutación con mejor relación tamaño/atenuación que un filtro L simple: por encima de su frecuencia de resonancia cae a −60 dB/dec (tres elementos reactivos) en lugar de −20 dB/dec. El precio de ese orden tres es una resonancia poco amortiguada que hay que gestionar.

## Qué hay antes del filtro (contexto genérico)
Aguas arriba de L1 hay una etapa que impone una tensión media controlable pero troceada: un nudo cuya tensión instantánea conmuta entre niveles discretos a una frecuencia de conmutación fsw, y cuyo valor medio en cada periodo es la consigna que fija el control. Esa fuente de tensión conmutada puede ser un inversor de dos niveles, un convertidor multinivel, una rama de un convertidor DC-DC, un rectificador activo o cualquier otra etapa de electrónica de potencia: para el filtro es indiferente. Lo único que el filtro "ve" desde su entrada es:

- una tensión vi con una componente fundamental útil (la consigna) más un espectro de armónicos concentrado alrededor de fsw y sus múltiplos
- una resistencia/inductancia de fuente normalmente despreciable frente a L1

Por eso el diseño del LCL no depende de la naturaleza del convertidor, solo de tres datos de esa etapa: la tensión de bus disponible (que fija la amplitud del troceado), la frecuencia de conmutación fsw (que fija dónde están los armónicos a atenuar) y la ganancia del modulador (que cambia si la etapa es de dos niveles, tres niveles, etc.). Aguas abajo de L2 hay un punto de conexión (PCC) detrás del cual puede haber una red, un transformador, otras cargas o una isla; su inductancia se suma a L2 y modifica la resonancia (ver Desarrollo "efecto de la red").

## Topología y diagrama
La rama serie L1 (lado fuente) llega al nudo vC; del nudo cuelga el condensador Cf a tierra (opcionalmente con una resistencia Rd de amortiguamiento pasivo en serie); del nudo sale la rama serie L2 (lado red/carga) hacia el PCC. R1 y R2 son las resistencias parásitas de las dos bobinas.

<div class="cfig"><img src="figuras/filtro-lcl-circuito.png" alt="Circuito del filtro LCL: fuente de tension conmutada, L1-R1, nudo vC con Cf a tierra, L2-R2, PCC"><div class="cap">Topología LCL por fase: rama serie L₁–Cf–L₂ entre la fuente de tensión conmutada y el PCC; Cf deriva el rizado de conmutación a tierra.</div></div>

## Ecuaciones de partida (de dónde se sale)
Aplicando Kirchhoff a las tres ramas (tensión en las dos bobinas, corriente en el condensador) salen las tres ecuaciones de estado del filtro, con i1, vC, i2 como estados:

- L1·di1/dt = vi − vC − R1·i1     (KVL rama L1)
- Cf·dvC/dt = i1 − i2             (KCL nudo vC)
- L2·di2/dt = vC − vpcc − R2·i2   (KVL rama L2)

Estas tres ecuaciones son el modelo del LCL. En el marco dq (girando a omega) cada derivada añade el acoplamiento cruzado de Park, +omega· J con J = [[0, −1],[1, 0]] (ver [[marco-dq]]):

- L1·di1/dt = vi − vC − R1·i1 + omega·L1·J·i1
- Cf·dvC/dt = i1 − i2 + omega·Cf·J·vC
- L2·di2/dt = vC − vpcc − R2·i2 + omega·L2·J·i2

## Desarrollo 1 — funciones de transferencia (derivación completa)
El objetivo de esta sección es deducir, paso a paso, las funciones de transferencia que relacionan las dos corrientes del filtro (i1 lado fuente, i2 lado red) con las dos tensiones que actúan sobre él (vi tensión de la fuente conmutada, vpcc tensión en el PCC). Estas funciones son la planta que ve el control de corriente, así que de aquí salen la resonancia, la antiresonancia y la elección de qué corriente realimentar.

### El LCL como cuadripolo: dos entradas, varias salidas
El filtro tiene dos tensiones que actúan sobre él, y conviene verlo como un cuadripolo (dos puertos):
- vi = V1: la tensión de la fuente conmutada, en el puerto de entrada. Es la única variable que el control manipula (el modulador la sintetiza a partir de la consigna del lazo).
- vpcc = V2: la tensión en el PCC, en el puerto de salida. No la decide el convertidor sino la red/carga, así que es una perturbación, no una entrada de control.

Las salidas que interesan son las dos corrientes (i1 lado fuente, i2 lado red) y la tensión del condensador vC. Como el filtro es lineal, cada salida es la superposición de la respuesta a las dos entradas. Para la corriente de lado red, por ejemplo:

i2 = G_i2,vi(s)·V1 + G_i2,vpcc(s)·V2

### Por qué se asume vpcc = 0 (V2 = 0) al calcular i2/vi
Esto es el principio de superposición de los sistemas lineales: la función de transferencia de una salida respecto a una entrada se define como la respuesta a esa entrada con todas las demás entradas anuladas. Por eso, para obtener G_i2,vi = i2/vi se pone vpcc = 0; y para obtener la respuesta a la red, G_i2,vpcc = i2/vpcc, se pondría vi = 0. La respuesta total es la suma de ambas. Anular vpcc no significa que la red no exista, sino que su efecto se contabiliza aparte, en su propia función de transferencia.

Tiene además un sentido físico directo: anular vpcc en pequeña señal equivale a suponer la red rígida (un nudo de tensión fija, una fuente de tensión ideal cuya tensión no se mueve ante la corriente que le inyecta el convertidor). Para diseñar el lazo de control nos interesa primero cómo responde i2 a lo que el control mueve (vi); el efecto de las variaciones de vpcc entra después como rechazo de perturbación. De hecho la respuesta a vpcc con vi = 0 es justamente la admitancia de salida del conjunto, la magnitud central del análisis de estabilidad por impedancia (ver [[impedancia-salida-estabilidad]]).

### Objetivo de cada función de transferencia (para qué se calcula cada una)
Del mismo cuadripolo salen varias funciones de transferencia, y cada una sirve para una cosa distinta. Por eso se calculan i2/vi, i1/vi, vC/vi (y la cruzada i2/vpcc):

| Función | Se calcula con | Para qué sirve |
|---|---|---|
| i2/vi (transadmitancia directa) | vpcc = 0 | Planta del lazo de corriente de red. Es lo que el control gobierna; de su denominador sale la resonancia. |
| i1/vi | vpcc = 0 | Planta del lazo interno (corriente de lado fuente). Tiene un cero de antiresonancia que la hace fácil de estabilizar; es la corriente que se realimenta y la base del amortiguamiento activo. |
| vC/vi | vpcc = 0 | Tensión del condensador. Necesaria si se controla la tensión (modo grid-forming) y para sensar/estimar la corriente del condensador en el amortiguamiento. |
| i2/vpcc (admitancia de salida) | vi = 0 | Respuesta a la perturbación de red; es la admitancia de salida Yo que entra en el criterio de estabilidad por impedancia frente a la red. |

La V2/V1 (relación de tensiones vpcc/vi, o vC/vi como su versión interna) es la lectura clásica del filtro como "filtro de tensión": cuánto pasa de la tensión de entrada a la de salida en función de la frecuencia, y dónde está la resonancia. En el contexto de control de corriente la planta principal es i2/vi, pero las demás se necesitan para el lazo interno, el amortiguamiento y la estabilidad frente a la red.

La derivación de abajo obtiene primero i2 en función de las dos entradas (paso 4), de ahí aísla i2/vi anulando vpcc, y como complemento obtiene i1/vi (paso 5), que explica por qué se realimenta i1 en el lazo interno (paso 6).

<div class="cfig"><img src="figuras/filtro-lcl-familia.png" alt="Magnitud de las tres FDT del LCL frente a vi: i2/vi, i1/vi y vC/vi"><div class="cap">Las tres FDT frente a vᵢ (con v_pcc=0): i₂/vᵢ (planta de red) solo tiene el pico de resonancia; i₁/vᵢ añade el valle de antiresonancia en f_ar antes del pico (por eso es fácil de realimentar); v_C/vᵢ es la tensión del condensador. Comparten denominador (misma resonancia), difieren en los ceros.</div></div>

### Versión reducida (sin resistencias, R1 = R2 = 0)
**Paso 1 — pasar las tres ecuaciones a Laplace.** Con R1 y R2 despreciables para ver la estructura (se reintroducen en la versión completa de más abajo), las tres ecuaciones de partida en el dominio de Laplace son:

- s·L1·I1 = Vi − Vc
- s·Cf·Vc = I1 − I2
- s·L2·I2 = Vc − Vpcc

**Paso 2 — eliminar la tensión del condensador Vc.** De la primera, Vc = Vi − s·L1·I1. De la tercera, Vc = Vpcc + s·L2·I2. Igualando:

Vi − s·L1·I1 = Vpcc + s·L2·I2

**Paso 3 — usar la ecuación del condensador para relacionar I1 e I2.** De la segunda, I1 − I2 = s·Cf·Vc. Sustituyendo Vc = Vpcc + s·L2·I2:

I1 = I2 + s·Cf·(Vpcc + s·L2·I2) = I2·(1 + s²·L2·Cf) + s·Cf·Vpcc

**Paso 4 — corriente de lado red i2.** Sustituyendo esa I1 en la igualdad del paso 2 y despejando I2 se obtiene la respuesta de la corriente de lado red a las dos entradas:

I2 = [ Vi − Vpcc·(1 + s²·L1·Cf) ] / [ s³·L1·L2·Cf + s·(L1 + L2) ]

De aquí, con red rígida (Vpcc = 0), la transferencia planta principal del control:

Gi2(s) = I2 / Vi = 1 / [ s³·L1·L2·Cf + s·(L1 + L2) ] = 1 / [ s·L1·L2·Cf·(s² + omega_res²) ]

con omega_res² = (L1 + L2)/(L1·L2·Cf). El denominador se anula en s = 0 y en s = ±j·omega_res: hay un par de polos sin parte real (zeta ≈ 0). Eso es la resonancia.

**Paso 4b — respuesta a la perturbación de red (admitancia de salida).** De la misma expresión del paso 4, anulando ahora vi en vez de vpcc, sale la otra mitad de la superposición:

Yo(s) = i2 / vpcc | vi=0 = −(1 + s²·L1·Cf) / [ s·L1·L2·Cf·(s² + omega_res²) ]

Es la admitancia de salida del filtro: cómo responde la corriente de red a un movimiento de la tensión de red. Tiene el mismo denominador (misma resonancia) pero distinto numerador, y es la que se compara con la impedancia de la red en el criterio de estabilidad por impedancia (ver [[impedancia-salida-estabilidad]]). Confirma que anular una entrada u otra solo cambia el numerador: la resonancia (el denominador) es común a todas las FDT del filtro.

**Paso 5 — corriente de lado fuente i1.** Sustituyendo la I2 recién hallada en I1 = I2·(1 + s²·L2·Cf) + s·Cf·Vpcc, y tomando de nuevo Vpcc = 0:

Gi1(s) = I1 / Vi = (1 + s²·L2·Cf) / [ s·L1·L2·Cf·(s² + omega_res²) ]

Esta función tiene, además del mismo par de polos resonantes, un par de ceros en s = ±j·omega_ar con:

omega_ar = 1 / raiz(L2·Cf)     (antiresonancia)

**Paso 6 — interpretar resonancia vs antiresonancia.** Gi2 (lado red) tiene solo el pico de resonancia: la fase cae 180° de golpe al cruzarla, lo que hunde el margen de fase si se realimenta i2. Gi1 (lado fuente) tiene un cero de antiresonancia en omega_ar < omega_res que aporta +180° de fase justo antes del pico, de modo que la fase no se desploma tanto. Conclusión práctica que se usa en todo el repositorio: realimentar i1 (lado fuente) es mucho más fácil de estabilizar que realimentar i2 (lado red). Esta es la razón de fondo por la que el lazo de corriente rápido se cierra sobre i1.

### Versión completa (con R1 y R2 en serie con las bobinas)
Ahora sin despreciar nada. Conviene usar las impedancias de cada rama: Z1 = R1 + s·L1 (rama de lado fuente) y Z2 = R2 + s·L2 (rama de lado red). Las ecuaciones de Laplace pasan a ser Z1·I1 = Vi − Vc, sCf·Vc = I1 − I2, Z2·I2 = Vc − Vpcc. Repitiendo los mismos pasos (eliminar Vc, anular vpcc) se llega a forma cerrada:

i2/vi = 1 / (Z1 + Z2 + sCf·Z1·Z2)
i1/vi = (1 + sCf·Z2) / (Z1 + Z2 + sCf·Z1·Z2)

Las dos comparten el denominador D(s) = Z1 + Z2 + sCf·Z1·Z2, que desarrollado es el polinomio característico completo (el mismo que el del Desarrollo 2):

D(s) = s³·Cf·L1·L2 + s²·Cf·(R1·L2 + R2·L1) + s·(L1 + L2 + Cf·R1·R2) + (R1 + R2)

**Comprobación de coherencia:** con R1 = R2 = 0 se tiene Z1 = sL1, Z2 = sL2, y D(s) → s·L1·L2·Cf·(s² + omega_res²); i2/vi e i1/vi recuperan exactamente las formas reducidas de los pasos 4 y 5. La versión reducida es el caso particular de la completa.

**Comparación de resultados (reducida vs completa).**

| Aspecto | Reducida (R1=R2=0) | Completa (con R1, R2) |
|---|---|---|
| Ganancia en baja frecuencia de i2/vi | infinita (polo en s=0, integrador puro) | finita: i2/vi(0) = 1/(R1+R2). El polo del origen se convierte en un polo real de baja frecuencia en p_lf = (R1+R2)/(L1+L2) |
| Par resonante | s = ±j·omega_res (zeta = 0, pico infinito) | desplazado al semiplano izquierdo, zeta_res ≈ [R1/L1 + R2/L2 − (R1+R2)/(L1+L2)] / (2·omega_res) |
| Ceros de antiresonancia de i1 (en omega_ar) | sobre el eje imaginario (1 + s²·L2·Cf) | amortiguados: 1 + s·Cf·R2 + s²·L2·Cf, con zeta_ar = (R2/2)·raiz(Cf/L2) |
| Frecuencias omega_res y omega_ar | exactas | casi idénticas (R desplaza poco la frecuencia, sí el amortiguamiento) |

La lectura práctica: las resistencias serie reales (parásitas) **sí** amortiguan algo —vuelven finitos el pico y la ganancia de continua— pero sus valores son tan pequeños que el zeta_res resultante sigue siendo muy bajo y el pico, alto. Por eso no bastan: hace falta añadir amortiguamiento pasivo (Rd) o activo (Kad). La versión reducida es útil para ver la estructura (frecuencias, ceros, pendientes); la completa, para cuantificar el amortiguamiento real y la ganancia de continua.

<div class="cfig"><img src="figuras/filtro-lcl-RvsnoR.png" alt="Comparacion de i2/vi sin R (pico infinito, integrador en baja frecuencia) vs con R1,R2 en serie (pico finito, meseta en baja frecuencia)"><div class="cap">i₂/vᵢ sin R (rojo) vs con R1,R2 en serie (azul). Sin R: pico infinito en f_res y pendiente de integrador en baja frecuencia. Con R: el pico se vuelve finito (aunque sigue alto con valores parásitos) y la baja frecuencia se aplana a una meseta 1/(R1+R2). La frecuencia de resonancia apenas cambia.</div></div>

<div class="cfig"><img src="figuras/filtro-lcl-bode.png" alt="Respuesta en frecuencia del LCL: i2/vi con resonancia, i1/vi con antiresonancia, con y sin amortiguamiento"><div class="cap">Magnitud de i₂/vᵢ y i₁/vᵢ: i₂ presenta el pico de resonancia afilado (rojo, ζ≈0) en f_res; i₁ añade el cero de antiresonancia en f_ar que aporta +180° de fase antes del pico (por eso se realimenta i₁). Al amortiguar (azul) el pico se acota. Por debajo el filtro deja pasar la fundamental; por encima cae a −60 dB/dec.</div></div>

## Desarrollo 2 — frecuencia de resonancia (derivación completa)
La frecuencia de resonancia son los modos propios del filtro: las frecuencias a las que la red oscila por sí sola sin excitación externa. Para hallarlos se anulan las dos fuentes de tensión que actúan sobre el filtro (vi = 0 y vpcc = 0 en pequeña señal): lo que queda son los modos naturales del circuito L1–Cf–L2. Se presenta primero la versión reducida (sin resistencias parásitas), que da la fórmula limpia, y después la versión completa (con R1, R2 y la Rd de amortiguamiento), que muestra cómo esa resonancia ideal se convierte en un par de polos amortiguados.

### Versión reducida (R1 = R2 = 0)
**Paso 1 — anular las fuentes y plantear las ecuaciones en Laplace.** Con vi = 0 y vpcc = 0, las tres ecuaciones de partida quedan:

- s·L1·I1 = −Vc          ⟹  I1 = −Vc / (s·L1)
- s·Cf·Vc = I1 − I2
- s·L2·I2 = Vc           ⟹  I2 = +Vc / (s·L2)

**Paso 2 — sustituir I1 e I2 en la ecuación del condensador.** Llevando las dos corrientes a s·Cf·Vc = I1 − I2:

s·Cf·Vc = −Vc/(s·L1) − Vc/(s·L2)

**Paso 3 — dividir por Vc (modo no trivial, Vc ≠ 0).** El condensador oscila, así que su tensión no es nula y se puede dividir:

s·Cf = −1/(s·L1) − 1/(s·L2)

**Paso 4 — reordenar a la ecuación característica.** Multiplicando por s y pasando todo a un lado:

s²·Cf + 1/L1 + 1/L2 = 0   ⟹   s²·Cf = −(1/L1 + 1/L2) = −(L1 + L2)/(L1·L2)

**Paso 5 — despejar s y leer la frecuencia.** Queda:

s² = −(L1 + L2)/(L1·L2·Cf)   ⟹   s = ±j·omega_res

con un par de raíces puramente imaginarias (sin parte real → amortiguamiento nulo). De ahí:

omega_res = raiz( (L1 + L2)/(L1·L2·Cf) )   y   fres = (1/(2·pi))·raiz( (L1 + L2)/(L1·L2·Cf) )

**Paso 6 — interpretación física (las dos bobinas en paralelo).** El término 1/L1 + 1/L2 es la suma de inversos típica de un paralelo. Al anular las fuentes, L1 y L2 quedan colgando del nudo vC hacia masa (cada fuente cortocircuitada es un camino a masa), así que están en paralelo. Definiendo la inductancia equivalente paralelo:

Leq = L1·L2 / (L1 + L2)

la expresión se compacta en la de un tanque LC simple, Leq resonando con Cf:

fres = 1 / (2·pi·raiz(Leq·Cf))

que es idéntica a la del paso 5 (resonancia de Cf contra L1 paralelo L2). Esto coincide con el denominador de las funciones de transferencia del Desarrollo 1: s³·L1·L2·Cf + s·(L1 + L2) = s·L1·L2·Cf·(s² + omega_res²), cuyos ceros no nulos son justo s = ±j·omega_res.

> Aviso sobre una aproximación habitual: algunos textos usan L1+L2 (suma serie) en lugar de Leq (paralelo) en el denominador, fres_aprox = 1/(2·pi·raiz((L1+L2)·Cf)). Subestima fres porque L1+L2 > Leq siempre. La diferencia es pequeña cuando L2 << L1 (relación r = L2/L1 pequeña) pero crece al acercarse L2 a L1. Usar siempre la forma exacta con Leq.

### Versión completa (con R1, R2 y Rd)
Sin despreciar nada, las ecuaciones con fuentes anuladas y resistencias incluidas (R1 en serie con L1, R2 en serie con L2; la Rd de amortiguamiento se añade luego en serie con Cf) son:

- s·L1·I1 = −Vc − R1·I1   ⟹  I1 = −Vc / (R1 + s·L1)
- s·Cf·Vc = I1 − I2
- s·L2·I2 = Vc − R2·I2    ⟹  I2 = +Vc / (R2 + s·L2)

**Sustituyendo en la ecuación del condensador y dividiendo por Vc:**

s·Cf = −1/(R1 + s·L1) − 1/(R2 + s·L2)

**Multiplicando por (R1 + s·L1)·(R2 + s·L2)** se obtiene la ecuación característica exacta (cúbica en s):

s³·(Cf·L1·L2) + s²·Cf·(R1·L2 + R2·L1) + s·[Cf·R1·R2 + (L1 + L2)] + (R1 + R2) = 0

Es el polinomio completo del filtro. Comprobación: con R1 = R2 = 0 se reduce a s³·Cf·L1·L2 + s·(L1+L2) = 0, es decir s·(s²·Cf·L1·L2 + L1 + L2) = 0, que devuelve la versión reducida. Las dos raíces complejas de la cúbica son el par resonante; ahora tienen parte real negativa (las resistencias amortiguan). Para R pequeñas la frecuencia amortiguada apenas se mueve de omega_res, y el amortiguamiento del par resonante introducido por una Rd en serie con Cf es:

zeta = (1/2)·Rd·raiz( Cf·(L1 + L2)/(L1·L2) )

es decir, sin resistencias zeta = 0 (la versión reducida) y crece linealmente con Rd. Por eso la versión reducida da la frecuencia (dónde está el pico) y la versión completa da el amortiguamiento (cómo de afilado es y por qué hay que amortiguarlo).

> A resaltar: sin amortiguar, cualquier lazo rápido o impedancia de red que excite fres provoca oscilación sostenida. Es uno de los mecanismos típicos de inestabilidad armónica y de oscilaciones de alta frecuencia entre convertidor y red.

## Desarrollo 3 — efecto de la red y el trafo sobre fres
Cuando el filtro no trabaja en vacío sino conectado a una red con inductancia Lg (y a un trafo con Lt), esas inductancias se suman en serie con L2. La frecuencia de resonancia efectiva baja:

L2ef = L2 + Lt + Lg
fres_ef = 1 / (2·pi·raiz( L1·L2ef/(L1+L2ef) · Cf ))

Esto es crítico en red débil: un SCR bajo significa Lg grande, lo que empuja fres hacia abajo y puede acercarla al ancho de banda del control. Regla de verificación: calcular siempre fres con el peor caso de Lg (SCR mínimo esperado).

Ejemplo con valores del proyecto 04 (L1=40 µH, Cf=85 µF, L2=8 µH, Lt=64 µH):
- SCR 5 (Lg=0): L2ef=72 µH, Leq=25.7 µH, fres=3406 Hz
- SCR 2 (Lg=124 µH): L2ef=196 µH, Leq=33.2 µH, fres=2997 Hz

La resonancia baja unos 400 Hz al pasar de SCR 5 a SCR 2. El amortiguamiento debe funcionar en todo ese rango.

## Desarrollo 4 — factor de calidad Q (derivación y efecto en la respuesta)
El factor de calidad Q mide cuántas veces amplifica el filtro una excitación justo en fres (la altura del pico de resonancia).

**De dónde sale.** Para un par de polos de segundo orden con amortiguamiento zeta, la ganancia en el pico respecto a la banda de paso es Q = 1/(2·zeta). Combinándolo con el amortiguamiento que introduce una Rd en serie con Cf (Desarrollo 2), zeta = (1/2)·Rd·raiz(Cf·(L1+L2)/(L1·L2)), queda:

Q = 1/(2·zeta) = 1 / ( Rd·raiz( Cf·(L1+L2)/(L1·L2) ) ) = (1/Rd)·raiz( L1·L2/(Cf·(L1+L2)) ) = (1/Rd)·raiz(Leq/Cf)

es decir, Q es la relación entre la impedancia característica del tanque raiz(Leq/Cf) y la resistencia de amortiguamiento Rd. Sin resistencias (Rd→0, R1=R2=0) Q→infinito y el pico es teóricamente infinito; con resistencias reales pequeñas Q sigue siendo alto (típico 10–50 en LCLs de potencia), lo que hace imprescindible amortiguar.

**Caso de estudio: efecto de Q sobre la respuesta.** Al subir el amortiguamiento (bajar Q) el pico de resonancia baja y se ensancha, mientras la banda de paso y la caída de −60 dB/dec por encima quedan casi intactas. La resistencia de amortiguamiento pasivo óptima en serie con Cf es:

Rd = 1 / (3·omega_res·Cf)

que deja Q ≈ 3 (un compromiso entre acotar el pico y no degradar la atenuación a fsw). Por debajo de eso el pico sigue siendo peligroso; muy por encima se sobre-amortigua y se pierde atenuación.

<div class="cfig"><img src="figuras/filtro-lcl-factorQ.png" alt="Bode de |i2/vi| para varios valores de Q mostrando el pico de resonancia cada vez más bajo"><div class="cap">Efecto del factor Q sobre |i₂/vᵢ|: sin amortiguar (Q→∞) el pico es enorme; al añadir R_d el pico baja y se ensancha. Con R_d óptimo (Q≈3) queda acotado sin estropear la atenuación a fsw; sobre-amortiguar (Q bajo) no aporta y empeora el filtrado.</div></div>

El inconveniente del amortiguamiento pasivo es que Rd disipa potencia, P_Rd = Rd·iCf_rms². Por eso en inversores de potencia media-alta se prefiere el amortiguamiento activo por software (ver más abajo), que consigue el mismo zeta sin pérdidas.

## Desarrollo 5 — rizado de corriente y dimensionado de L1 (derivación completa)
La bobina de lado fuente se dimensiona por el rizado de conmutación que deja pasar. Se deriva primero la versión reducida (tensión de salida constante dentro de un periodo de conmutación, que da la regla de diseño) y después el detalle (dependencia con el ciclo de trabajo y convención pico vs pico-pico).

### Versión reducida (tensión de salida ≈ constante en un periodo Tsw)
**Paso 1 — punto de partida.** La ley de la bobina es vL = L1·di1/dt, luego la corriente cambia con pendiente di1/dt = vL/L1 mientras se le aplica una tensión vL. En un periodo de conmutación Tsw = 1/fsw el nudo vC apenas se mueve (fsw >> frecuencia de red), así que se trata como constante e igual a la salida instantánea vo.

**Paso 2 — tensión sobre L1 en cada subintervalo.** El polo conmuta entre +Vdc/2 y −Vdc/2. La tensión sobre L1 es la del polo menos vo:
- subintervalo "alto" (duración d·Tsw): vL+ = +Vdc/2 − vo
- subintervalo "bajo" (duración (1−d)·Tsw): vL− = −Vdc/2 − vo

donde d es el ciclo de trabajo. Como el valor medio del polo debe igualar a vo, se cumple vo = (2d − 1)·Vdc/2, de donde Vdc/2 − vo = Vdc·(1 − d).

**Paso 3 — subida de corriente en el subintervalo alto.** La corriente sube con pendiente vL+/L1 durante d·Tsw, así que el rizado pico-pico es:

delta_i1pp = (vL+/L1)·(d·Tsw) = [Vdc·(1 − d)/L1]·d·Tsw = (Vdc·Tsw/L1)·d·(1 − d)

es decir, sustituyendo Tsw = 1/fsw:

delta_i1pp = (Vdc/(fsw·L1))·d·(1 − d)

**Paso 4 — caso peor (máximo rizado).** El producto d·(1 − d) es máximo en d = 0.5 (salida instantánea nula, paso por cero de la senoide), donde vale 1/4. El rizado pico-pico máximo es:

delta_i1pp,max = Vdc / (4·fsw·L1)

**Paso 5 — convención de la especificación y regla de diseño.** Si la especificación se da como amplitud del rizado (desviación de pico respecto a la media, que es la mitad del pico-pico), aparece el factor 8 habitual en la literatura de diseño de LCL:

delta_i1,amp = delta_i1pp/2 = Vdc / (8·fsw·L1)   ⟹   L1 = Vdc / (8·fsw·delta_i1,amp)

(con pico-pico el factor es 4; con amplitud, 8 — conviene fijar cuál se usa). El valor objetivo típico es 10–20 % de la corriente nominal de pico In. Más inductancia = menos rizado pero más caída y volumen.

<div class="cfig"><img src="figuras/filtro-lcl-rizado.png" alt="Izquierda: rizado a lo largo del ciclo de red para dos L1. Derecha: rizado pico-pico máximo frente a L1 con las líneas de 10% y 20% de In"><div class="cap">Izquierda: el rizado sigue d(1−d), máximo en el paso por cero de la senoide y mínimo en los picos; doblar L₁ lo reduce a la mitad. Derecha: rizado p-p máximo frente a L₁; fijar el objetivo (10–20 % de Iₙ) determina el L₁ mínimo — diseñar para menos rizado exige más inductancia.</div></div>

### Detalle (lo que la versión reducida obvia)
- La dependencia d·(1 − d) significa que el rizado no es constante a lo largo del ciclo de red: es máximo en el paso por cero (d ≈ 0.5) y mínimo en los picos de la senoide (d → 0 o 1). Dimensionar por d = 0.5 es el caso peor.
- Se ha supuesto vo constante en el periodo Tsw; es exacto en el límite fsw >> f0 y solo introduce un error de segundo orden.
- Efecto de R1 (con vs sin resistencia serie): aquí es despreciable. Durante un subintervalo de conmutación (duración del orden de Tsw, microsegundos) la caída R1·i1 apenas cambia frente a la tensión aplicada Vdc·(1−d), así que la pendiente di1/dt ≈ vL/L1 no la fija R1 sino L1. La resistencia sí importa para la caída de tensión media y las pérdidas en régimen, pero no para el rizado de conmutación; por eso el dimensionado de L1 se hace sin R1.
- Si la etapa de entrada es de tres niveles, el escalón de tensión sobre L1 se reduce a la mitad (±Vdc/4 efectivo por nivel), de modo que para el mismo rizado L1 baja a la mitad; ver [[convertidor-vsc|modulación PWM]]. Con modulación vectorial (SVPWM) o inyección de tercer armónico el caso peor cambia ligeramente respecto al SPWM senoidal puro.

## Desarrollo 6 — dimensionado de Cf (reactiva)
El condensador absorbe reactiva a la frecuencia de red: corriente Ic = omega0·Cf·V, luego Qc = V·Ic = omega0·Cf·V². Se limita a un ≤5 % de la potencia base para no cargar la fuente con reactiva inútil:

Qc = omega0·Cf·V² ≤ 0.05·Sn   ⟹   Cf ≤ 0.05·Sn / (omega0·V²)

## Desarrollo 7 — dimensionado de L2 (atenuación a fsw)
Muy por encima de fres, la impedancia del condensador 1/(omega·Cf) es mucho menor que omega·L2, así que casi todo el rizado se deriva por Cf. El divisor de corriente da la atenuación de lado fuente a lado red:

|i2/i1|(omega_sw) ≈ 1 / |1 − omega_sw²·L2·Cf| ≈ 1 / (omega_sw²·L2·Cf)

Para una atenuación objetivo k = i2/i1 a fsw se despeja:

L2 ≈ 1 / (k·Cf·omega_sw²)

Relación práctica L2/L1 entre 0.2 y 1. Conviene definir r = L2/L1 y comprobar después que fres cae en banda.

## Amortiguamiento activo (derivación, estudio de polos y diseño)
En vez de disipar en una Rd física, se emula una resistencia de amortiguamiento por software. La técnica habitual realimenta la corriente del condensador iCf = i1 − i2 a la tensión de la fuente con ganancia Kad:

vi = vi_PI − Kad·(i1 − i2)

**Por qué equivale a una resistencia sin pérdidas (desarrollo).** La dinámica de i1 sin amortiguar es L1·di1/dt = vi − vC − R1·i1. Sustituyendo la ley de control vi = vi_PI − Kad·(i1 − i2):

L1·di1/dt = vi_PI − vC − R1·i1 − Kad·(i1 − i2)

El término −Kad·i1 actúa exactamente como una resistencia en serie con L1 (su caída es proporcional a i1), y el −Kad·(−i2) recupera que la corriente que pasa por el condensador es i1 − i2: el conjunto emula una Rd vista por la rama del condensador. La diferencia con una resistencia física es que Kad no disipa potencia real: es una consigna de tensión, no una caída óhmica. Por eso da el mismo amortiguamiento que Rd pero sin las pérdidas P_Rd.

**Estudio de polos: cómo influye Kad en el diseño.** Anulando las fuentes y reescribiendo el modelo con la realimentación activa, la matriz de estado del filtro (estados i1, i2, vC; R1 = R2 = 0 para aislar el efecto) es:

A(Kad) = [[ −Kad/L1, +Kad/L1, −1/L1 ], [ 0, 0, 1/L2 ], [ 1/Cf, −1/Cf, 0 ]]

Los autovalores de A(Kad) son el par resonante. En Kad = 0 están sobre el eje imaginario en ±j·omega_res (zeta = 0). Al subir Kad, el par se desplaza hacia la izquierda (parte real negativa creciente): el amortiguamiento sube de forma casi proporcional a Kad mientras la frecuencia del par apenas cambia. Esto convierte el diseño en directo: se barre Kad hasta cruzar la línea de zeta objetivo.

<div class="cfig"><img src="figuras/filtro-lcl-damping-polos.png" alt="lugar de los polos resonantes del LCL al barrer Kad, con lineas de zeta constante"><div class="cap">Lugar de los polos resonantes al barrer K_ad de 0 a 12 Ω: parten sobre el eje imaginario (ζ≈0, rojo) y se mueven a la izquierda al subir K_ad (color), cruzando las líneas de ζ constante. El diseño consiste en elegir el K_ad que lleva el par al ζ objetivo (0.3–0.7) sin pasarse.</div></div>

**Procedimiento de diseño.** Identificar fres; medir o estimar iCf como i1 − i2; barrer Kad (del orden de unos pocos ohmios) observando el lugar de polos hasta el zeta objetivo de la resonancia (0.3–0.7); verificar que no degrada el margen de los lazos de corriente y tensión. Variantes: realimentar i2 o la derivada de vC en lugar de iCf.

**Límites y errores.** Ganancia Kad excesiva amplifica el ruido de medida y puede provocar inestabilidad de alta frecuencia; estimar iCf con retardo de muestreo significativo (1.5·Ts) le quita eficacia e incluso puede volver el damping negativo a frecuencias altas — por eso el retardo de cómputo acota el Kad útil y, con él, el zeta máximo alcanzable. En digital conviene compensar ese retardo (ver [[compensacion-retardo]]).

## Cuándo y por qué se usa
Estándar a la salida de cualquier convertidor conectado a red (PV, eólica, baterías, STATCOM) por la normativa de inyección de armónicos, y también alimentando cargas sensibles en isla. Se prefiere al filtro L cuando se busca menos inductancia total / menor caída para la misma atenuación. La resonancia aparece en cuanto un lazo rápido o la impedancia de red excita la zona de fres; es crítica en red débil, donde Lg baja fres y la mete en la banda de control.

## Procedimiento de diseño (genérico)
1. L1 por rizado: L1 = Vdc / (8·fsw·delta_i1pp), con delta_i1pp = 10–20 % de In.
2. Cf por reactiva: Cf ≤ 0.05·Sn / (omega0·V²).
3. L2 por atenuación a fsw: L2 ≈ 1 / (k·Cf·omega_sw²), con r = L2/L1 entre 0.2 y 1.
4. Coloca fres en banda holgada: 10·f0 < fres < fsw/2.
5. Elige la corriente de realimentación: i1 (lado fuente, con su cero de antiresonancia) da más margen que i2.
6. Añade amortiguamiento: pasivo Rd ≈ 1/(3·omega_res·Cf) en serie con Cf, o activo por software (Kad sobre iCf).
7. Verifica en red débil: recalcula fres con L2 + Lg_max (SCR mínimo) y comprueba que el par resonante mantiene zeta entre 0.1 y 0.3.

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
- Banda de resonancia: 10·f0 < fres < fsw/2.
- delta_i1pp: 10–20 % de In. Cf: ≤5 % de Sn en reactiva. r = L2/L1: 0.2–1.
- Amortiguamiento objetivo del par resonante: zeta entre 0.1 y 0.3. Rd pasivo de unos pocos ohmios; Kad activo de unos pocos ohmios (en el proyecto, 6 Ω).
- Proyecto (10 kVA / 400 V / 50 Hz, fsw=10 kHz): L1=2 mH, Cf=20 µF, L2=1 mH → fres ≈ 1.38 kHz y far ≈ 1.13 kHz (LCL aislado). En el modelo dq completo, con la inductancia de red, el modo resonante baja a ≈ 1.1 kHz con zeta ≈ 0.13 (ya amortiguado).

## Errores comunes
- Realimentar i2 (lado red) directamente: sin el cero de antiresonancia el margen de fase se desploma al acercarse a fres. Preferir i1 o amortiguar.
- Dejar fres demasiado cerca del ancho de banda de control → resonancia excitada.
- Olvidar el amortiguamiento → polos resonantes con zeta ≈ 0.
- Ignorar Lg en red débil → fres baja y entra en la banda del control.
- Sobredimensionar Cf (demasiada reactiva) o L2 (caída y coste); sobre-amortiguar con Rd grande (pérdidas y peor atenuación a fsw).
- Confundir resonancia (par de polos, vista en i2) con antiresonancia (par de ceros, en i1).

## Uso en proyectos
- 01 - GFM-Impedance (modelar la planta): el LCL aporta 6 de los 15 estados del modelo. Su modo resonante (≈1.1 kHz, zeta ≈ 0.13) obligó a añadir amortiguamiento activo con Kad = 6 Ω para poder subir el lazo de tensión a 350 Hz.
- 02 - GFL-Impedance (estabilidad en red débil): el mismo LCL obliga a mantener el lazo de corriente / PLL por debajo de fres, que además baja al debilitarse la red.

## Conceptos relacionados
- [[convertidor-vsc|modulación PWM]] · [[marco-dq]] · [[impedancia-salida-estabilidad]] · [[control-cascada]] · [[diagrama-bode]]

## Referencias
- Reznik et al., LCL Filter Design..., IEEE TIA 2014.
- Dannehl et al., Investigation of Active Damping Approaches for LCL Filters, IEEE TIA 2010.
- Wang, Blaabjerg, Harmonic Stability in Power-Electronic-Based Power Systems, IEEE TPEL 2014.
- Mohan, Undeland, Robbins, Power Electronics, Wiley 2003.
