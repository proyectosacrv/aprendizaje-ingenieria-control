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
relacionados: [convertidor-vsc, marco-dq, impedancia-salida-estabilidad, control-cascada, diagrama-bode]
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

**Por qué la función de transferencia de interés es i2/vi.** Antes de derivar conviene justificar qué entrada y qué salida se eligen, porque un sistema de tres almacenes de energía (L1, Cf, L2) tiene varias funciones de transferencia posibles y solo una es la planta natural del control. El razonamiento tiene dos patas:

- La salida es i2 (corriente de lado red) porque es la magnitud que físicamente se entrega a la red o a la carga: es la que transporta la potencia activa y reactiva útil, la que fija el factor de potencia en el PCC y la que la normativa de inyección de armónicos limita. El control de un convertidor conectado a red existe, en el fondo, para gobernar esa corriente i2 (o las potencias P y Q, que son i2 proyectada sobre la tensión). La corriente de lado fuente i1 y la tensión del condensador vC son estados internos del filtro, no el objetivo final.
- La entrada es vi (tensión de la fuente conmutada) porque es la única variable que el control puede manipular directamente: el modulador sintetiza vi a partir de la consigna del lazo. La otra tensión que actúa sobre el filtro, vpcc, no la decide el convertidor sino la red, así que es una perturbación, no una entrada de control. Por eso la planta del lazo se escribe como salida-controlada entre entrada-manipulable: i2 frente a vi.

En consecuencia, la función de transferencia de diseño es Gi2(s) = i2(s)/vi(s) evaluada con la red rígida (vpcc tratada como perturbación independiente, vpcc = 0 para la planta). La respuesta de i2 a la perturbación vpcc se calcula por separado (mismo denominador, distinto numerador) y entra como rechazo de perturbación. La derivación de abajo obtiene primero i2 en función de las dos entradas (paso 4) y de ahí aísla Gi2; como complemento se obtiene i1/vi (paso 5), que no es el objetivo de control pero explica por qué se realimenta i1 en el lazo interno (paso 6).

**Paso 1 — pasar las tres ecuaciones a Laplace.** Con R1 y R2 despreciables para ver la estructura (se reintroducen luego como amortiguamiento), las tres ecuaciones de partida en el dominio de Laplace son:

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

**Paso 5 — corriente de lado fuente i1.** Sustituyendo la I2 recién hallada en I1 = I2·(1 + s²·L2·Cf) + s·Cf·Vpcc, y tomando de nuevo Vpcc = 0:

Gi1(s) = I1 / Vi = (1 + s²·L2·Cf) / [ s·L1·L2·Cf·(s² + omega_res²) ]

Esta función tiene, además del mismo par de polos resonantes, un par de ceros en s = ±j·omega_ar con:

omega_ar = 1 / raiz(L2·Cf)     (antiresonancia)

**Paso 6 — interpretar resonancia vs antiresonancia.** Gi2 (lado red) tiene solo el pico de resonancia: la fase cae 180° de golpe al cruzarla, lo que hunde el margen de fase si se realimenta i2. Gi1 (lado fuente) tiene un cero de antiresonancia en omega_ar < omega_res que aporta +180° de fase justo antes del pico, de modo que la fase no se desploma tanto. Conclusión práctica que se usa en todo el repositorio: realimentar i1 (lado fuente) es mucho más fácil de estabilizar que realimentar i2 (lado red). Esta es la razón de fondo por la que el lazo de corriente rápido se cierra sobre i1.

**Paso 7 — efecto de las resistencias (amortiguamiento real).** Reintroduciendo R1 y R2, o una Rd en serie con Cf, los polos resonantes dejan de estar sobre el eje imaginario y adquieren parte real negativa. Con Rd en serie con el condensador el amortiguamiento del par resonante es:

zeta = (1/2)·Rd·raiz( Cf·(L1 + L2)/(L1·L2) )

es decir, a mayor Rd más amortiguado, a costa de pérdidas y de peor atenuación a fsw.

<div class="cfig"><img src="figuras/filtro-lcl-bode.png" alt="Respuesta en frecuencia del LCL: i2/vi con resonancia, i1/vi con antiresonancia, con y sin amortiguamiento"><div class="cap">Magnitud de i₂/vᵢ y i₁/vᵢ: i₂ presenta el pico de resonancia afilado (rojo, ζ≈0) en f_res; i₁ añade el cero de antiresonancia en f_ar que aporta +180° de fase antes del pico (por eso se realimenta i₁). Al amortiguar (azul) el pico se acota. Por debajo el filtro deja pasar la fundamental; por encima cae a −60 dB/dec.</div></div>

## Desarrollo 2 — frecuencia de resonancia
La frecuencia de resonancia es la de las dos bobinas en paralelo con Cf. La forma exacta usa la inductancia equivalente paralelo Leq = L1·L2/(L1+L2):

fres = 1 / (2·pi·raiz(Leq·Cf))

que es idéntica a la expresión habitual fres = (1/2pi)·raiz((L1+L2)/(L1·L2·Cf)). Una aproximación que aparece en algunos textos usa L1+L2 (suma serie) en lugar de Leq (paralelo) en el denominador:

fres_aprox = 1 / (2·pi·raiz((L1+L2)·Cf))

Esa aproximación subestima fres porque L1+L2 > Leq siempre. La diferencia es pequeña cuando L2 << L1 (relación r = L2/L1 pequeña) pero crece cuando L2 se acerca a L1. Usar siempre la fórmula exacta con Leq.

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

## Desarrollo 4 — factor de calidad Q
El factor Q mide cuántas veces amplifica el filtro una excitación en fres. Sin resistencias (R1=R2=0) Q tiende a infinito y el pico es teóricamente infinito. Con resistencias reales pequeñas Q sigue siendo alto (típico 10–50 en LCLs de potencia), lo que hace imprescindible el amortiguamiento. La resistencia de amortiguamiento pasivo óptima en serie con Cf es:

Rd = 1 / (3·omega_res·Cf)

Con Rd bien elegido Q baja a valores manejables (Q < 3) y el pico queda acotado. El inconveniente es que Rd disipa potencia P_Rd = Rd·iCf_rms². Por eso en inversores de potencia media-alta se prefiere el amortiguamiento activo por software (ver más abajo), que no tiene pérdidas.

## Desarrollo 5 — rizado de corriente y dimensionado de L1
La bobina de lado fuente se dimensiona por el rizado de conmutación que deja pasar. La base es vL = L·di/dt: mientras el puente aplica una tensión del orden de ±Vdc/2 sobre L1 durante una fracción del periodo Tsw = 1/fsw, la corriente sube/baja con pendiente vL/L1. El rizado pico-pico crece con Tsw (menos conmutaciones) y baja con L1. El caso peor con PWM senoidal de dos niveles da la regla de diseño habitual:

delta_i1pp ≈ Vdc / (8·fsw·L1)   ⟹   L1 = Vdc / (8·fsw·delta_i1pp)

con delta_i1pp típico del 10–20 % de la corriente nominal de pico In. Más inductancia = menos rizado pero más caída y volumen. (Si la etapa de entrada es de tres niveles, el escalón de tensión sobre L1 se reduce a la mitad y para el mismo rizado L1 baja; ver [[convertidor-vsc|modulación PWM]].)

## Desarrollo 6 — dimensionado de Cf (reactiva)
El condensador absorbe reactiva a la frecuencia de red: corriente Ic = omega0·Cf·V, luego Qc = V·Ic = omega0·Cf·V². Se limita a un ≤5 % de la potencia base para no cargar la fuente con reactiva inútil:

Qc = omega0·Cf·V² ≤ 0.05·Sn   ⟹   Cf ≤ 0.05·Sn / (omega0·V²)

## Desarrollo 7 — dimensionado de L2 (atenuación a fsw)
Muy por encima de fres, la impedancia del condensador 1/(omega·Cf) es mucho menor que omega·L2, así que casi todo el rizado se deriva por Cf. El divisor de corriente da la atenuación de lado fuente a lado red:

|i2/i1|(omega_sw) ≈ 1 / |1 − omega_sw²·L2·Cf| ≈ 1 / (omega_sw²·L2·Cf)

Para una atenuación objetivo k = i2/i1 a fsw se despeja:

L2 ≈ 1 / (k·Cf·omega_sw²)

Relación práctica L2/L1 entre 0.2 y 1. Conviene definir r = L2/L1 y comprobar después que fres cae en banda.

## Amortiguamiento activo (sin pérdidas)
En vez de disipar en una Rd física, se emula una resistencia de amortiguamiento por software. La técnica habitual realimenta la corriente del condensador iCf = i1 − i2 a la tensión de la fuente con ganancia Kad:

vi = vi_PI − Kad·(i1 − i2)

Esto añade un término disipativo en la dinámica de i1 que mueve los polos de resonancia desde el eje imaginario (zeta ≈ 0) hacia la izquierda (zeta útil), equivaliendo a una resistencia en serie con L1 pero sin pérdidas. Funciona en dq componente a componente.

<div class="cfig"><img src="figuras/amortiguamiento-activo-lcl-polos.png" alt="polos de resonancia LCL al barrer Kad"><div class="cap">Barrido de la ganancia K_ad: el par de polos de resonancia parte casi sobre el eje imaginario (ζ≈0) y, al subir K_ad, se desplaza a la izquierda (más amortiguado). Equivale a una resistencia en serie con L1 sin pérdidas.</div></div>

Procedimiento: identificar fres, medir o estimar iCf como i1 − i2, elegir Kad (del orden de unos pocos ohmios) para el zeta objetivo de la resonancia (0.3–0.7) barriendo Kad y observando los polos, y verificar que no degrada el margen de los lazos de corriente y tensión. Variantes: realimentación de i2 o de la derivada de vC en lugar de iCf.

Errores del amortiguamiento activo: ganancia excesiva amplifica ruido y puede provocar inestabilidad de alta frecuencia; estimar iCf con retardo de muestreo significativo le quita eficacia al damping.

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
