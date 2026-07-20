---
titulo: Sistema fotovoltaico y MPPT
slug: fotovoltaica-mppt
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: []
objetivos: [modelar la célula PV y extraer la máxima potencia con MPPT]
tags: [pv, fotovoltaica, mppt, p-and-o, inc-cond, curva-iv, diodo-unico, inc, conductancia-incremental, intermedio, modelado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-03
relacionados: [modelo-bateria-bess, convertidor-vsc, dinamica-bus-dc, control-tension-bus-dc, sistema-por-unidad]
referencias:
  - "Sera et al., PV Panel Model Based on Datasheet Values, IEEE ISIE 2007"
  - "Esram, Chapman, Comparison of Photovoltaic Array MPPT Techniques, IEEE TEC 2007"
---

## Definición
Modelo eléctrico de la célula/módulo fotovoltaico (curva I-V no lineal) y algoritmos de
**Maximum Power Point Tracking (MPPT)** que ajustan el punto de operación para extraer la máxima
potencia disponible ante variaciones de irradiancia y temperatura.

## Fundamento teórico
**Modelo de diodo único:**
$$ I = I_{ph} - I_0\left(\exp\!\frac{V+IR_s}{nV_T}-1\right) - \frac{V+IR_s}{R_{sh}} $$
con \( V_T=kT/q \) (tensión térmica, \( \approx26 \) mV a 25 °C), \( n \) factor de idealidad,
\( I_{ph} \) fotocorriente (proporcional a irradiancia G), \( I_0 \) corriente de saturación inversa
(fuertemente dependiente de T). La curva I-V tiene:
- **Isc** (cortocircuito, \( V=0 \)): corriente máxima ≈ \( I_{ph} \).
- **Voc** (circuito abierto, \( I=0 \)): tensión máxima.
- **MPP** (máxima potencia): punto de tangente \( dP/dV=0 \); típicamente 70–80 % de \( V_{oc} \).

<div class="cfig"><img src="figuras/fotovoltaica-mppt-iv.png" alt="curva I-V y P-V de un modulo PV"><div class="cap">La curva I-V del PV (azul) es no lineal; la potencia P=V·I (rojo) tiene un máximo único, el MPP (~76 % de Voc), que el MPPT persigue ante cambios de irradiancia y temperatura.</div></div>

La irradiancia eleva \( I_{ph}\sim G \); la temperatura sube → \( V_{oc} \) cae (\( -2.3 \) mV/°C
por célula).

**MPPT — algoritmos:**
- **Perturba y observa (P&O):** incrementa/decrementa la tensión de referencia y compara \( P \) con
  el ciclo anterior. Simple; oscila alrededor del MPP en régimen permanente (amplitud \( \propto \Delta V_{step} \)).
- **Conductancia incremental (INC):** condición exacta del MPP: \( dI/dV=-I/V \). Sin oscilación en permanente; más costoso.
- **MPPT por tensión constante (Voc fracción):** \( V_{MPP}\approx0.76 V_{oc} \). Muy simple, impreciso ante sombreado.
- **MPP global con sombreado parcial:** la curva P-V tiene **múltiples máximos locales** (bypass diodes). Se requieren técnicas globales (barrido periódico, PSO).

**Integración al convertidor:** el MPPT genera la referencia de tensión DC \( V^*_{dc} \). Un boost DC/DC intermedio adapta la tensión del string al bus DC; el VSC controla el bus DC hacia la red ([[control-tension-bus-dc]]).

## 1 — El modelo eléctrico del panel: derivación de la ecuación del diodo único

El modelo de diodo único captura el comportamiento esencial de la unión p-n fotovoltaica con solo cinco parámetros.

**Paso 1 — origen de la fotocorriente \( I_{ph} \).** Los fotones crean pares electrón-hueco en la región de deplexión. El campo eléctrico de la unión p-n separa las cargas y produce una corriente \( I_{ph} \) proporcional a la irradiancia: \( I_{ph}=I_{sc,STC}\cdot(G/G_{STC}) \). Esta corriente fluye en el sentido de la corriente de carga (fotogenerada), es decir, desde la cara iluminada al circuito externo.

**Paso 2 — el diodo interno.** La unión p-n polarizada en directo por la propia fotocorriente conduce una corriente oscura inversa a la fotogeneración:
$$ I_{diodo}=I_0\left(\exp\frac{q(V+IR_s)}{nkT}-1\right) $$
donde \( V+IR_s \) es la tensión real en la unión (teniendo en cuenta la caída en la resistencia serie \( R_s \) de los contactos y el semiconductor).

**Paso 3 — las pérdidas por fugas \( R_{sh} \).** La resistencia paralela \( R_{sh} \) (shunt resistance) modela las fugas en la unión: \( I_{sh}=(V+IR_s)/R_{sh} \). En módulos buenos \( R_{sh}\gg1\,\text{k}\Omega \) y esta corriente es despreciable, pero en celdas degradadas o con microfisuras puede ser significativa.

**Paso 4 — balance de corrientes (KCL en el nudo de la celda).**
$$ \boxed{\;I = I_{ph} - I_0\!\left(\exp\frac{V+IR_s}{nV_T}-1\right) - \frac{V+IR_s}{R_{sh}}\;} $$

La ecuación es **implícita** en \( I \) (aparece en el exponente por \( R_s \)); se resuelve numéricamente por Newton-Raphson en cada punto de la curva. Para análisis de MPPT y control basta con la forma simplificada \( I\approx I_{sc}-I_0\,e^{q(V+R_s I)/(nkT)} \) (despreciar \( R_{sh} \) y la constante \( -1 \) del exponente a \( V>3V_T \)).

**Dependencia de temperatura.** \( V_T=kT/q \) sube linealmente con \( T \), lo que baja el exponente y reduce \( V_{oc} \). La corriente de saturación \( I_0\propto T^3\exp(-E_g/(nkT)) \) es muy sensible a la temperatura, lo que explica que el aumento de \( T \) reduzca \( V_{oc} \) en \( -2.3\,\text{mV/°C} \) por célula (y sube ligeramente \( I_{sc} \)).

## 2 — La curva P-V y el MPP: condición de máximo

**Paso 1 — escribir la potencia y derivar.** Con \( P(V)=V\cdot I(V) \):
$$ \frac{dP}{dV}=\frac{d(V\,I)}{dV}=I+V\,\frac{dI}{dV} $$

**Paso 2 — imponer máximo.** En el MPP la potencia no crece ni decrece: \( dP/dV=0 \). Igualando a cero:
$$ I+V\,\frac{dI}{dV}=0 $$

**Paso 3 — despejar la condición de conductancia incremental.** Pasando \( I \) al otro lado y dividiendo por \( V \):
$$ \boxed{\;\frac{dI}{dV}=-\frac{I}{V}\;} $$

Lectura: la **conductancia incremental** \( dI/dV \) (pendiente local de la curva I-V) iguala en magnitud a la **conductancia instantánea** \( I/V \), con signo opuesto. El signo de \( dP/dV=I+V\,dI/dV \) dice de qué lado del MPP estamos:

$$ \frac{dI}{dV}>-\frac{I}{V}\Rightarrow\text{a la izquierda del MPP (subir }V),\qquad \frac{dI}{dV}<-\frac{I}{V}\Rightarrow\text{a la derecha (bajar }V) $$

**Por qué la curva P-V tiene un único máximo.** La función \( I(V) \) del diodo es monótonamente decreciente (cada vez más empinada hacia \( V_{oc} \)). La potencia \( P=VI \) empieza en cero (\( V=0 \)), sube (mientras \( I \) cae poco), alcanza un máximo y vuelve a cero en \( V_{oc} \) (donde \( I=0 \)). Hay exactamente un punto donde la pendiente se anula, siempre que la irradiancia sea uniforme. Con sombreado parcial la curva P-V puede tener múltiples máximos locales (uno por cada grupo de módulos en distintas condiciones).

## 3 — El modelo del panel: ecuación del diodo y derivación del MPP

La ecuación del diodo único captura la física de la celda fotovoltaica. El MPP emerge de imponer \( dP/dV=0 \) sobre esa ecuación.

**Paso 1 — la corriente del diodo.** Una unión p-n en oscuridad conduce corriente oscura regida por la ecuación de Shockley:
$$ I_{diodo}=I_0\!\left(\exp\frac{q\,V}{n\,k\,T}-1\right) $$
donde \( I_0 \) es la corriente de saturación inversa, \( n \) el factor de idealidad (\( 1\le n\le2 \)), y \( V_T=kT/q\approx26\,\text{mV} \) a 25 °C. Esta corriente **se opone** a la fotogeneración.

**Paso 2 — la fotocorriente.** Los fotones de energía \( E>E_g \) crean pares electrón-hueco; el campo de la unión los separa y produce:
$$ I_{ph}=I_{sc,STC}\cdot\frac{G}{G_{STC}}\cdot[1+\alpha_T(T-T_{STC})] $$
con \( \alpha_T\approx0.04\%/°C \) para Si-c. En primera aproximación \( I_{ph}\approx I_{sc}\propto G \).

**Paso 3 — KCL y ecuación de la celda.** Balanceando corrientes en el nudo de la celda: la fotocorriente generada menos la que consume el diodo menos la que fuga por \( R_{sh} \):
$$ I=I_{ph}-I_0\!\left(\exp\frac{V+I\,R_s}{n\,V_T}-1\right)-\frac{V+I\,R_s}{R_{sh}} $$

**Paso 4 — condición del MPP por \( dP/dV=0 \).** La potencia es \( P=V\cdot I(V) \). Derivando:
$$ \frac{dP}{dV}=I+V\frac{dI}{dV}=0\;\Longrightarrow\;\frac{dI}{dV}=-\frac{I}{V} $$

Derivando la ecuación del diodo implícita respecto a \( V \) (manteniendo la dependencia implícita de \( I \) en \( V \)):
$$ \frac{dI}{dV}=-\frac{I_0\exp(\ldots)/(n\,V_T)+1/R_{sh}}{1+R_s\,I_0\exp(\ldots)/(n\,V_T)+R_s/R_{sh}} $$

Igualando a \( -I/V \) y despejando \( V_{MPP} \) se obtiene la condición transcendente que el MPPT resuelve numéricamente en línea o que el fabricante reporta como \( V_{MPP}\approx0.76\,V_{oc} \).

## 4 — El algoritmo P&O: pseudocódigo y diagrama de estados

**Paso 1 — la base del algoritmo.** El signo de \( \Delta P/\Delta V \) dice de qué lado del MPP estamos. Se perturba \( V_{ref} \) y se evalúa la respuesta:

```
pseudocódigo P&O:
  medir V_k, I_k
  P_k = V_k · I_k
  ΔP = P_k − P_{k−1}
  ΔV = V_k − V_{k−1}
  si ΔP > 0:
    si ΔV > 0: V_{k+1} = V_k + ΔV_step   (seguir en mismo sentido)
    si ΔV < 0: V_{k+1} = V_k − ΔV_step
  si ΔP < 0:
    si ΔV > 0: V_{k+1} = V_k − ΔV_step   (invertir)
    si ΔV < 0: V_{k+1} = V_k + ΔV_step
  si ΔP ≈ 0: V_{k+1} = V_k               (en el MPP, no perturbar)
```

**Paso 2 — el error de seguimiento dinámico.** Cuando la irradiancia cambia rápidamente (ráfaga de nube en < 1 s), la potencia cae por el cambio de condiciones, **no** por estar en el lado incorrecto del MPP. El algoritmo P&O puede entonces interpretar erróneamente \( \Delta P \) y moverse en la dirección equivocada, alejándose del nuevo MPP durante varios pasos. El error dinámico es:
$$ \varepsilon_{dyn}\approx\left|\frac{\dot G}{G}\right|\cdot T_{MPPT}\cdot\Delta V_{step} \cdot \left|\frac{d^2P}{dV^2}\right|_{MPP}^{-1} $$

Cuanto más rápido cambia \( G \), más pasos puede dar en la dirección incorrecta antes de corregir. InC es más robusto porque detecta el signo de \( dI/dV+I/V \) directamente, independientemente de la causa del cambio de potencia.

**Paso 3 — diagrama de estados del P&O.**

<div class="cfig"><img src="figuras/fotovoltaica-po-flowchart.png" alt="Diagrama de flujo del algoritmo P&O: medir V e I, calcular incrementos de P y V, decidir el sentido de la perturbación según los signos y actualizar la referencia"><div class="cap">El algoritmo mide \(V_k, I_k\), calcula \(\Delta P\) y \(\Delta V\) respecto al paso anterior y decide el sentido de la perturbación: si \(\Delta P>0\) sigue en la misma dirección de \(\Delta V\), si \(\Delta P<0\) invierte el sentido, y si \(\Delta P\approx 0\) mantiene la tensión. Luego guarda el estado y repite. Este vaivén permanente alrededor del MPP es la causa del rizado en régimen permanente.</div></div>

## 5 — El MPPT con control de corriente

En lugar de regular la **tensión** \( V_{ref}=V_{MPP} \), se puede regular la **corriente** \( I_{ref}=I_{MPP} \). Esta estrategia es más rápida para transitorios bruscos de irradiancia.

**Paso 1 — la curva I(V) en el MPP.** La corriente en el MPP se puede aproximar a partir de la derivada de la curva I-V:
$$ I_{MPP}\approx I_{sc}\left(1-\exp\frac{V_{MPP}-V_{oc}}{n\,V_T\,N_s}\right)\approx I_{sc}\cdot\frac{V_{MPP}}{V_{oc}}\cdot k_{fill} $$
donde \( k_{fill} \) es el factor de forma del módulo (\( \approx0.92 \) para módulos de calidad). Más preciso: el fabricante da directamente \( I_{MPP} \) a STC.

**Paso 2 — MPPT por corriente constante.** Generar directamente la referencia de corriente:
$$ I_{ref}^*=I_{MPP,STC}\cdot\frac{G}{G_{STC}} $$
Esta referencia no necesita buscar el MPP: es proporcional a la irradiancia medida (o estimada por el sensor de corriente de cortocircuito). La ventaja es que el convertidor responde en un ciclo de control (el ancho de banda del lazo de corriente), en lugar del tiempo de convergencia del MPPT iterativo (decenas a cientos de ms).

**Paso 3 — ventajas e inconvenientes.**

| Criterio | MPPT por tensión (P&O/InC) | MPPT por corriente |
|---|---|---|
| Velocidad de respuesta | Lenta (convergencia iterativa) | Rápida (un ciclo de corriente) |
| Precisión en régimen permanente | Alta (converge al MPP exacto) | Media (depende de \( G \) medida) |
| Robustez a temperatura | Alta | Baja (T afecta \( V_{MPP} \) más que \( I_{MPP} \)) |
| Complejidad | Media | Baja |
| Uso típico | Instalaciones fijas | Sistemas de respuesta rápida (vehículos, trackers) |

## 6 — Diseño iterativo: panel 300 W, paso ΔV óptimo del P&O

**Especificaciones:** panel JA Solar 300 Wp, \( V_{MPP}=37\,\text{V} \), \( I_{MPP}=8.1\,\text{A} \), convertidor boost con \( f_{sw}=20\,\text{kHz} \), lazo de tensión a \( f_{bw,V}=200\,\text{Hz} \).

**Paso 1 — rizado de tensión del convertidor como cota inferior de ΔV.**

El rizado de tensión del boost a la salida del inductor de entrada (donde está el PV):
$$ \Delta v_{L1}=\frac{V_{in}\cdot D}{L_1\,f_{sw}} $$
Con \( L_1=1\,\text{mH} \), \( V_{in}=37\,\text{V} \), \( D\approx0.5 \): \( \Delta v_{L1}=37\times0.5/(10^{-3}\times20\times10^3)=0.93\,\text{V} \). Para evitar que el MPPT confunda el rizado del convertidor con su propia perturbación:
$$ \Delta V_{step}\geq 2\,\Delta v_{L1}\approx2\,\text{V} $$

**Paso 2 — cota superior de ΔV por rizado de potencia.**

El rizado de potencia alrededor del MPP cuesta eficiencia. La curvatura de la curva P(V) en el MPP:
$$ \frac{d^2P}{dV^2}\bigg|_{MPP}\approx -\frac{2I_{MPP}}{V_{MPP}} \cdot \frac{1}{n V_T N_s} $$
Para \( n=1.3 \), \( N_s=72 \), \( V_T=26\,\text{mV} \): \( d^2P/dV^2\approx-8.1\,\text{W/V}^2 \). La pérdida de eficiencia por el rizado:
$$ \frac{\Delta P_{rizado}}{P_{MPP}}\approx\frac{1}{2}\cdot\frac{|d^2P/dV^2|}{P_{MPP}}\cdot(\Delta V)^2=\frac{4.05}{300}\cdot(\Delta V)^2=0.0135\cdot(\Delta V)^2 $$
Para \( \Delta V=2\,\text{V} \): pérdida \( \approx0.054=5.4\% \). Para \( \Delta V=1\,\text{V} \): pérdida \( \approx1.35\% \).

**Paso 3 — ΔV óptimo: compromiso velocidad vs precisión.**

Velocidad de convergencia: el P&O parte de \( V_{init}\approx0.76\,V_{oc}\approx28\,\text{V} \) (si arranca lejos) y necesita \( N_{conv}=(37-28)/\Delta V \) pasos para llegar al MPP.

Con \( T_{MPPT}=100\,\text{ms} \): tiempo de convergencia \( t_{conv}=N_{conv}\times T_{MPPT} \).

| ΔV [V] | Pérdida en permanente | N pasos | t_conv |
|---|---|---|---|
| 0.5 | 0.34 % | 18 | 1.8 s |
| 1.0 | 1.35 % | 9 | 0.9 s |
| 2.0 | 5.4 % | 4.5 | 0.45 s |
| 3.0 | 12.2 % | 3 | 0.3 s |

**Óptimo:** \( \Delta V=1.0\text{–}1.5\,\text{V} \) equilibra eficiencia en permanente y respuesta aceptable (< 1 s). Para sistemas con irradiancia muy variable (nubes frecuentes), \( \Delta V=2\,\text{V} \) con \( T_{MPPT}=50\,\text{ms} \) mejora el seguimiento dinámico.

<div class="cfig"><img src="figuras/fotovoltaica-mppt-analisis.png" alt="4 paneles: curvas IV/PV, P&O trayectoria, MPPT dinámico, ΔV óptimo vs eficiencia"><div class="cap">
(a) Curva P(V) e I(V) del panel 300 W a distintas irradiancias G=200/500/800/1000 W/m²: el MPP se desplaza con G. (b) El P&O trazando su trayectoria en la curva PV: los puntos convergen al MPP real (estrella) con oscilación ±ΔV. (c) MPPT dinámico cuando una nube pasa en 2 s: P&O pierde el MPP brevemente; InC lo sigue mejor. (d) ΔV óptimo: la curva de eficiencia en permanente (roja) baja con ΔV grande; la curva de tiempo de convergencia (azul) mejora; el óptimo está en la región sombreada.
</div></div>

## 7 — El algoritmo P&O clásico: convergencia y rizado (resumen)

**Paso 1 — la pendiente cambia de signo en el MPP.** De la curva P-V (un único máximo en condiciones uniformes):
$$ \frac{dP}{dV}>0 \text{ a la izquierda del MPP},\qquad \frac{dP}{dV}<0 \text{ a la derecha} $$

**Paso 2 — aproximar la pendiente por incrementos.** Entre dos pasos de control con perturbación \( \Delta V=V_k-V_{k-1} \) y respuesta \( \Delta P=P_k-P_{k-1} \):
$$ \frac{dP}{dV}\approx\frac{\Delta P}{\Delta V} $$

**Paso 3 — regla de decisión.** Para subir por la curva hacia el máximo hay que moverse en el sentido en que \( P \) aumenta:
$$ \boxed{\;V_{k+1}=V_k+\Delta V_{step}\cdot\operatorname{sign}(\Delta P)\cdot\operatorname{sign}(\Delta V)\;} $$

Si la última perturbación subió la potencia (\( \Delta P>0 \)), se repite el mismo sentido de \( \Delta V \); si la bajó (\( \Delta P<0 \)), se invierte. Por eso, en permanente, P&O **oscila** en torno al MPP con amplitud \( \propto\Delta V_{step} \): nunca se queda quieto porque necesita perturbar para medir.

**Rizado en permanente.** El rizado de potencia alrededor del MPP vale aproximadamente:
$$ \Delta P_{rizado}\approx\frac{1}{2}\left|\frac{d^2P}{dV^2}\right|_{V_{MPP}}\cdot(\Delta V_{step})^2 $$

La segunda derivada de \( P \) en el MPP es negativa (máximo cóncavo), de modo que un paso más grande duplica el rizado. La eficiencia MPPT en permanente es \( \eta\approx1-\Delta P/(2P_{MPP}) \).

## 8 — El algoritmo InC: condición exacta, sin rizado

El algoritmo de conductancia incremental (InC) implementa la condición \( dI/dV+I/V=0 \) directamente:

**Paso 1 — estimar \( dI/dV \) por diferencias.** En cada ciclo de control:
$$ \Delta I=I_k-I_{k-1},\quad \Delta V=V_k-V_{k-1},\quad \frac{dI}{dV}\approx\frac{\Delta I}{\Delta V} $$

**Paso 2 — evaluar la condición y decidir.** Definiendo el error de conductancia:
$$ \varepsilon = \frac{dI}{dV}+\frac{I}{V} $$

- \( \varepsilon=0 \): estamos **en el MPP** → no perturbar (\( \Delta V=0 \)).
- \( \varepsilon>0 \): estamos a la izquierda del MPP → subir \( V \).
- \( \varepsilon<0 \): estamos a la derecha → bajar \( V \).

**Por qué InC no oscila.** Cuando \( \varepsilon=0 \) exactamente, el algoritmo no emite perturbación → la tensión se queda fija en el MPP. Esto es imposible en P&O, que siempre perturba para evaluar. La desventaja de InC es la sensibilidad al ruido en \( \Delta I/\Delta V \) (división que puede ser grande o mal condicionada cerca de \( V_{oc} \) donde \( \Delta I\approx0 \)).

**Comparativa práctica:**

| Criterio | P&O | InC |
|---|---|---|
| Complejidad de implementación | Baja | Media |
| Oscilación en permanente | Sí (\( \pm\Delta V \)) | No (idealmente) |
| Respuesta a irradiancia rápida | Puede equivocarse de dirección | Más robusto |
| Sensibilidad al ruido | Moderada | Alta (división \( \Delta I/\Delta V \)) |
| Uso típico | Aplicaciones de bajo coste | Aplicaciones de alta precisión |

## 9 — Diseño iterativo: array 60 kWp, P&O vs InC bajo nubosidad variable

**Especificaciones:** 60 kWp de capacidad instalada, módulos de 300 Wp, irradiancia variable entre 200 y 1000 W/m², temperatura 25–50 °C.

**Paso 1 — punto de operación.** A STC (\( G=1000\,\text{W/m}^2 \), \( T=25\,°\text{C} \)):
\( V_{MPP,string}\approx30\,\text{V}\times N_{serie} \), \( I_{string}\approx 8.5\,\text{A}\times N_{paralelo} \). La tensión de bus del boost típico: 600–800 V.

**Paso 2 — paso de P&O.** El rizado de tensión del convertidor boost a \( f_{sw}=20\,\text{kHz} \) introduce un rizado de tensión natural \( \Delta V_{conv}\approx1\,\text{V} \). El paso MPPT debe ser \( \Delta V_{MPPT}\geq 2\Delta V_{conv} \) para no confundir el rizado del convertidor con el del MPPT. Se elige \( \Delta V_{step}=2\,\text{V} \).

**Paso 3 — periodo de muestreo MPPT.** El lazo de tensión del boost debe responder antes del siguiente paso MPPT. Si el lazo de tensión tiene \( f_{bw}\approx200\,\text{Hz} \) (constante de tiempo \( \tau_v\approx0.8\,\text{ms} \)), el MPPT debe ser al menos 10× más lento: \( T_{MPPT}\geq50\,\text{ms} \). Se elige \( T_{MPPT}=100\,\text{ms} \).

**Resultado comparativo.** Bajo nubosidad rápida (irradiancia cae de 1000 a 300 W/m² en 2 s):
- P&O con \( \Delta V=2\,\text{V} \) converge en ~500 ms pero puede equivocarse de dirección brevemente durante la transición (la potencia cae por el cambio de G, no por estar en el lado incorrecto de la curva).
- InC detecta el cambio de signo de \( dI/dV+I/V \) sin ambigüedad y sigue el MPP con retraso \( \leq T_{MPPT} \).
- Pérdida de energía estimada durante una transición de 2 s: P&O \( \approx2\,\% \), InC \( <0.5\,\% \).


## 10 — Modelo del panel PV: parámetros y sensibilidades

Los cinco parámetros del modelo de diodo único (\(I_{ph}\), \(I_0\), \(n\), \(R_s\), \(R_{sh}\)) se extraen de la hoja de datos del fabricante. Las curvas a distintas condiciones ambientales permiten calibrar las dependencias de temperatura e irradiancia.

**Parámetros clave en el MPP (STC: \(G=1000\,\text{W/m}^2\), \(T=25\,°\text{C}\)):**

| Parámetro | Símbolo | Valor típico (300 Wp) | Significado |
|---|---|---|---|
| Corriente cortocircuito | \(I_{sc}\) | 9.0 A | Máxima corriente, proporcional a G |
| Tensión circuito abierto | \(V_{oc}\) | 45 V | Máxima tensión, logarítmica en G |
| Corriente MPP | \(I_{mpp}\) | 8.3 A | ≈ 92 % de \(I_{sc}\) |
| Tensión MPP | \(V_{mpp}\) | 36 V | ≈ 80 % de \(V_{oc}\) |
| Factor de forma | FF | 0.74 | \(P_{mpp}/(V_{oc}\,I_{sc})\) |

**Efecto de temperatura.** La tensión de circuito abierto cae aproximadamente \(-2.3\,\text{mV/°C}\) por célula (coeficiente de temperatura negativo). Para un módulo de 60 células:
$$ \frac{\partial V_{oc}}{\partial T} \approx -0.138\,\text{V/°C},\qquad \frac{\partial I_{sc}}{\partial T} \approx +0.06\,\%/°\text{C} $$
El efecto dominante es la caída de \(V_{oc}\): a 50 °C (módulo caliente en verano), la potencia del MPP cae \(\approx 8\,\%\) respecto a STC.

**Efecto de irradiancia.** La fotocorriente es lineal en \(G\): \(I_{ph} = I_{sc,STC} \cdot G/G_{STC}\). La tensión de circuito abierto tiene dependencia logarítmica:
$$ V_{oc}(G) \approx V_{oc,STC} + n\,V_T\,\ln\!\left(\frac{G}{G_{STC}}\right) $$
A \(G = 200\,\text{W/m}^2\) (día nublado), \(V_{oc}\) cae solo \(\approx 10\,\%\) pero \(I_{sc}\) cae al 20 %: la potencia disponible es 5 veces menor aunque la tensión del MPP apenas varía.

**Implicación para el MPPT.** La tensión del MPP se mueve poco con la irradiancia (± 2–3 V sobre 36 V), pero sí con la temperatura (hasta ± 5 V). El arranque del MPPT desde \(0.76\,V_{oc}\) es robusto en cualquier condición porque \(V_{mpp}/V_{oc} \approx 0.80\) se mantiene aproximadamente constante.

## 11 — Algoritmo P&O: paso a paso con pseudocódigo completo

El algoritmo Perturba y Observa es el más usado por su simplicidad. Su lógica central: el signo del cambio de potencia, junto con el signo de la perturbación, indica la dirección hacia el MPP.

**Variables del algoritmo:**
- \(V_k, I_k\): tensión y corriente medidos en el instante \(k\)
- \(P_k = V_k\,I_k\): potencia actual
- \(\Delta P = P_k - P_{k-1}\), \(\Delta V = V_k - V_{k-1}\): incrementos respecto al paso anterior
- \(\Delta V_{step}\): paso de perturbación (parámetro de diseño)
- \(\varepsilon_{th}\): umbral anti-oscilación (\(|\Delta P| < \varepsilon_{th}\) → en el MPP)

**Pseudocódigo completo:**
```
Inicialización: V_ref = 0.76 * Voc; P_prev = 0; V_prev = V_ref

Bucle periódico (cada T_MPPT):
  medir V_k, I_k
  P_k = V_k * I_k
  ΔP = P_k − P_prev
  ΔV = V_k − V_prev

  si |ΔP| < ε_th:              # en el MPP, no perturbar
      V_ref = V_k
  sino si ΔP > 0:
      si ΔV > 0: V_ref = V_k + ΔV_step    # potencia sube al subir V → seguir subiendo
      sino:      V_ref = V_k − ΔV_step    # potencia sube al bajar V → seguir bajando
  sino:                                    # ΔP < 0
      si ΔV > 0: V_ref = V_k − ΔV_step    # potencia baja al subir V → invertir
      sino:      V_ref = V_k + ΔV_step    # potencia baja al bajar V → invertir

  V_prev = V_k; P_prev = P_k
  enviar V_ref al lazo de tensión del convertidor
```

**Paso de perturbación \(\Delta V_{step}\):** compromiso fundamental:
- **\(\Delta V_{step}\) pequeño** (0.5 V): baja oscilación en régimen permanente, convergencia lenta (\(\sim 1\,\text{s}\)).
- **\(\Delta V_{step}\) grande** (2–3 V): rápida convergencia, pero alta oscilación permanente y pérdidas de eficiencia (\(\sim 5\text{–}10\,\%\)).
- Regla práctica: \(\Delta V_{step} \geq 2\,\Delta v_{rizado,convertidor}\) para no confundir el rizado del DC/DC con la perturbación del MPPT.

**P&O vs INC.** El algoritmo de conductancia incremental (INC) implementa la condición exacta del MPP: \(dI/dV = -I/V\). Diferencia clave: cuando \(\varepsilon = dI/dV + I/V = 0\), el INC no emite perturbación y se queda fijo, sin oscilar. P&O siempre perturba para medir. El INC es más robusto ante cambios rápidos de irradiancia porque distingue si \(\Delta P < 0\) se debe a estar en el lado incorrecto del MPP o a una caída de irradiancia.

## 12 — Respuesta dinámica y sombra parcial

**Tiempo de convergencia.** Partiendo de \(V_{init} = 0.76\,V_{oc}\) (estimación inicial), el número de pasos hasta el MPP:
$$ N_{conv} = \frac{|V_{MPP} - V_{init}|}{\Delta V_{step}} $$
Con \(T_{MPPT} = 100\,\text{ms}\): \(t_{conv} = N_{conv} \times 100\,\text{ms}\). Para \(\Delta V_{step} = 1\,\text{V}\) y diferencia de 9 V: \(t_{conv} = 0.9\,\text{s}\).

**Error dinámico ante cambio rápido de irradiancia.** Si la irradiancia cambia mientras el MPPT está convergiendo, la potencia varía por el cambio ambiental, no por estar en el lado equivocado del MPP. El P&O interpreta \(\Delta P < 0\) como "ir en la dirección incorrecta" y puede alejarse del nuevo MPP durante varios pasos. Este error dinámico es proporcional a la velocidad de cambio de \(G\):
$$ \varepsilon_{dyn} \propto \frac{\dot{G}}{G} \cdot T_{MPPT} \cdot \Delta V_{step} $$

**Sombra parcial y máximos múltiples.** Cuando parte del campo fotovoltaico queda en sombra (un árbol, una nube localizada, un edificio próximo), los módulos afectados producen menos corriente. Los diodos bypass (normalmente uno por cada 18–24 células) cortocircuitan los módulos sombreados, pero la curva P-V resultante tiene **múltiples máximos locales** (uno por cada grupo de módulos en distintas condiciones). El P&O simple queda atrapado en el máximo local más cercano, que puede ser hasta un 30–50 % menos que el máximo global.

**Solución: MPPT global.** Periódicamente (cada 1–10 minutos o cuando se detecta una caída brusca de potencia) se realiza un barrido completo de \(V_{ref}\) desde cero hasta \(V_{oc}\) y se localiza el máximo global. Esta fase de barrido puede costar 0.5–2 segundos de seguimiento subóptimo, pero garantiza que el sistema no queda atrapado.

**Integración con el inversor.** El MPPT genera \(V_{ref}^*\) para el boost DC/DC que conecta el campo PV al bus DC. El inversor VSC regula la tensión del bus DC y controla la potencia reactiva inyectada a la red. La referencia de potencia activa que el MPPT envía al inversor es la potencia disponible en el MPP, con limitación por el despacho del operador de la red si es necesario.

## 13 — Dimensionado del string y protecciones

**Número de módulos en serie.** La tensión del bus DC del inversor define el rango MPPT: la suma de tensiones \(V_{mpp}\) de los módulos en serie debe quedar dentro del rango:
$$ N_s = \frac{V_{dc,bus}}{V_{mpp,modulo}} $$
Para un bus de 750 V y módulos con \(V_{mpp} = 36\,\text{V}\): \(N_s = 750/36 \approx 20\,\text{módulos}\).

**Corrección por temperatura.** En invierno frío (\(T = -10\,°\text{C}\)), \(V_{oc}\) sube. La tensión máxima del string no debe superar el límite del inversor:
$$ V_{oc,max} = N_s \times V_{oc,STC} \times [1 + \alpha_V (T_{min} - 25)] $$
Con \(\alpha_V = -0.31\,\%/°\text{C}\) y \(T_{min} = -10\,°\text{C}\): factor de corrección \(1 + 0.0031 \times 35 = 1.109\). Hay que verificar que \(V_{oc,max} < V_{dc,max,inversor}\).

**Número de strings en paralelo.** La potencia instalada y la corriente de entrada del inversor definen cuántos strings en paralelo:
$$ N_p = \frac{P_{pico}}{N_s \times P_{modulo}},\qquad I_{string,total} = N_p \times I_{mpp,modulo} $$

**Diodos bypass y bloqueo.**
- **Diodos bypass** (integrados en el junction box): protegen las células sombreadas de la corriente inversa de los módulos iluminados en el mismo string. Sin ellos, las células sombreadas disiparían potencia y se calentarían (hot spot), degradándose.
- **Diodos de bloqueo** (en la caja de combiners): protegen contra circulación de corriente entre strings en paralelo con distintas irradiancias. Hoy en día muchos inversores tienen la función de bloqueo integrada con MOSFETs.

**Rango MPPT del inversor.** El datasheet del inversor especifica \([V_{mpp,min}, V_{mpp,max}]\). Se debe verificar que a temperatura extrema alta (módulo a 70 °C), \(V_{mpp}\) no caiga por debajo de \(V_{mpp,min}\).

<div class="cfig"><img src="figuras/fotovoltaica-mppt-analisis.png" alt="4 paneles: curvas IV y PV, convergencia P&O, variación Voc con temperatura, efecto irradiancia"><div class="cap">
(a) Curvas I-V para \(G=400, 700, 1000\,\text{W/m}^2\): la corriente es proporcional a \(G\) mientras la tensión de circuito abierto varía poco. (b) Curvas P-V correspondientes: el MPP se desplaza principalmente en potencia (eje vertical) y poco en tensión (eje horizontal). (c) Convergencia del P&O: la tensión de referencia oscila alrededor de \(V_{mpp}\) (línea roja) con amplitud decreciente. (d) Variación de \(V_{oc}\) con la temperatura: caída de \(-0.138\,\text{V/°C}\) para módulo de 60 células; a 50 °C, \(V_{oc}\) cae \(\approx 3.5\,\text{V}\) respecto a STC.
</div></div>

## Cuándo y por qué se usa
En toda instalación PV conectada a red o a microrred. El MPPT es la capa de control más exterior
(más lenta, decenas de ms) sobre el lazo de tensión/corriente del DC/DC.

## Procedimiento de diseño (genérico)
1. Parametriza el modelo de diodo único con los datos de la hoja (Isc, Voc, Impp, Vmpp a STC).
2. Elige el algoritmo MPPT (P&O para simplicidad; INC para menos rizado; global si hay sombreado).
3. Sintoniza el paso \( \Delta V \) (P&O): pequeño → poco rizado, respuesta lenta; grande → rápido, mucho rizado.
4. Conecta el MPPT al lazo de tensión del DC/DC; separa bandas (MPPT \( \ll \) lazo de tensión).
5. Verifica comportamiento con irradiancia variable y sombreado parcial.

## Ejemplo de código
```python
def mppt_po(V_ref, P_now, P_prev, V_prev, dV=0.5):
    if P_now >= P_prev:
        return V_ref + dV if V_ref >= V_prev else V_ref - dV
    else:
        return V_ref - dV if V_ref >= V_prev else V_ref + dV

def mppt_inc(V_ref, I_now, I_prev, V_prev, dV=0.5):
    dI = I_now - I_prev; dVv = V_ref - V_prev
    if abs(dVv) < 1e-6:
        return V_ref
    cond = dI/dVv + I_now/V_ref
    if abs(cond) < 0.01:
        return V_ref          # en el MPP
    return V_ref - np.sign(cond)*dV
```

## Parámetros y valores típicos
Paso P&O \( \Delta V \) 0.5–2 V; periodo MPPT 10–100 ms. \( V_{MPP}/V_{oc}\approx0.76 \);
\( I_{MPP}/I_{sc}\approx0.92 \). Eficiencia MPPT > 99 % en condiciones uniformes.

## Errores comunes
- Paso \( \Delta V \) grande en P&O → rizado permanente significativo en potencia.
- Usar P&O simple con sombreado parcial → queda en máximo local (pérdidas de hasta 30–50 %).
- MPPT más rápido que el lazo de tensión del convertidor → interacción y oscilación.
- InC con resolución insuficiente en los ADC → \( \Delta I/\Delta V \) ruidoso → decisiones erráticas.

## Conceptos relacionados
- [[convertidor-vsc]] · [[dinamica-bus-dc]] · [[control-tension-bus-dc]] · [[modelo-bateria-bess]] · [[sistema-por-unidad]]

## Referencias
- Sera et al., *PV Panel Model Based on Datasheet Values*, IEEE ISIE 2007.
- Esram, Chapman, *Comparison of PV Array MPPT Techniques*, IEEE TEC 2007.
