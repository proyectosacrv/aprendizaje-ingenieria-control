---
titulo: Grid-forming vs grid-following
slug: grid-forming-vs-following
categoria: control
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [elegir la arquitectura de control del inversor]
tags: [grid-forming, grid-following, PLL, red-debil, SCR, impedancia-salida, mapa-estabilidad, gran-senal, black-start, impedancia-virtual]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [droop-control, vsm-inercia, impedancia-salida-estabilidad, red-thevenin-scr, pll-srf, interaccion-pll-red-debil, impedancia-virtual]
referencias:
  - "Rocabert et al., Control of Power Converters in AC Microgrids, IEEE TPEL 2012"
  - "Lin et al., Research Roadmap on Grid-Forming Inverters, NREL 2020"
  - "Sun, Impedance-Based Stability Criterion for Grid-Connected Inverters, IEEE TPEL 2011"
  - "Harnefors et al., Passivity-Based Stability Assessment of Grid-Connected VSCs, IEEE JETCAS 2016"
  - "Taul et al., Current Limiting Control with Enhanced Dynamics of Grid-Forming Converters, IEEE JETCAS 2020"
  - "Denis et al., The Migrate Project: The Large Scale Demonstration of Frontier Solutions for the Integration of Wind and Solar, IET RPG 2018"
---

## Definición
Dos filosofías de control de un inversor conectado a red. El **grid-following (GFL)** se
sincroniza con la red mediante una PLL e **inyecta corriente**. El **grid-forming (GFM)** **impone una
tensión** con su propia frecuencia y ángulo, como una fuente de tensión detrás de una impedancia.
Su comportamiento frente a la red es opuesto: robustez en redes débiles para el GFM, en redes
fuertes para el GFL.

<div class="cfig"><img src="figuras/grid-forming-vs-following-comparativa.png" alt="comparativa GFM vs GFL"><div class="cap">GFM se comporta como una fuente de tensión tras una impedancia (impone V y f, genera su ángulo); GFL como una fuente de corriente que sigue el ángulo de la PLL. Esa diferencia explica su robustez opuesta frente a la red.</div></div>

## Fundamento teórico
- **GFL**: fuente de corriente controlada; depende de una PLL para conocer el ángulo de red.
  Su estabilidad se degrada en **red débil** (SCR bajo), porque la PLL y el lazo de corriente
  interactúan con la alta impedancia de red.
- **GFM**: fuente de tensión; el ángulo lo genera el propio control (droop/VSM), **sin PLL**.
  Aporta inercia/soporte y es robusto en red débil. Su impedancia de salida es **inductiva**
  en banda media (firma de fuente de tensión), igual que una máquina síncrona.

## 1 — Por qué la fuente de corriente (GFL) sufre en red débil y la de tensión (GFM) no

**Paso 1 — los dos equivalentes.** Cada filosofía es un equivalente de Thévenin/Norton distinto detrás de la impedancia de red \( Z_{red} \):
- **GFL** = fuente de **corriente** \( I \) (Norton, impedancia interna idealmente \( \infty \)): impone la corriente que inyecta y deja que la red fije la tensión del PCC.
- **GFM** = fuente de **tensión** \( E \) detrás de una impedancia interna \( Z_o \) pequeña (Thévenin): impone la tensión y deja que la red fije la corriente.

**Paso 2 — sensibilidad de la tensión del PCC en el GFL.** Con la fuente de corriente \( I \) inyectando contra la red \( V_g \) detrás de \( Z_{red} \), la tensión del nudo es
$$ V_{pcc}=V_g+Z_{red}\,I\;\Longrightarrow\;\frac{\partial V_{pcc}}{\partial I}=Z_{red} $$
La tensión que mide la PLL depende de \( Z_{red} \). En **red débil** \( |Z_{red}| \) es grande (SCR bajo): cada pequeño cambio de corriente mueve mucho \( V_{pcc} \). La PLL reacciona a ese movimiento corrigiendo el ángulo, lo que cambia \( I \), que vuelve a mover \( V_{pcc} \) — el lazo PLL–red se cierra con ganancia \( \propto Z_{red} \) y se desestabiliza (ver [[interaccion-pll-red-debil]]). Cuanto más débil la red, más alta la ganancia de ese lazo.

**Paso 3 — sensibilidad de la corriente en el GFM.** Con la fuente de tensión \( E \) detrás de \( Z_o \), la corriente que circula a la red es
$$ I=\frac{E-V_g}{Z_o+Z_{red}}\;\Longrightarrow\;\frac{\partial I}{\partial E}=\frac{1}{Z_o+Z_{red}} $$
Aquí \( Z_{red} \) está en el **denominador**: una red débil (\( |Z_{red}| \) grande) **reduce** la sensibilidad de la corriente a la tensión impuesta. El GFM no necesita medir el ángulo de la red —lo genera él (droop/VSM)— así que no hay lazo de medida que la impedancia alta pueda desestabilizar. Es robusto justo donde el GFL falla.

**Paso 4 — el espejo.** El mismo cociente explica el caso opuesto: en **red fuerte** (\( Z_{red}\to0 \)), \( \partial I/\partial E\to1/Z_o \) es grande, así que un GFM con droop **agresivo** (lazo de potencia de banda ancha) puede inestabilizar en red fuerte — el espejo exacto del GFL. Cada arquitectura es robusta en el extremo donde la otra falla; la elección la decide el SCR esperado ([[red-thevenin-scr]]).

## 2 — Impedancia de salida: la diferencia fundamental entre GFM y GFL

La impedancia de salida \( Z_o(s) \) de un convertidor se define como la relación entre la perturbación de tensión aplicada en sus bornes y la corriente que resulta, con la referencia interna fija:

$$ Z_o(s) = \left.\frac{\hat{v}_{pcc}}{\hat{i}_{pcc}}\right|_{ref=cte} $$

Es la firma eléctrica del convertidor vista desde la red. Para el análisis de estabilidad, la comparación entre \( Z_o \) y \( Z_{red} \) (criterio de impedancias de Sun/Middlebrook) determina si el sistema es estable o no.

**GFM como fuente de tensión (Zo pequeña e inductiva).** Un GFM controla la tensión del PCC mediante un lazo de tensión de alta ganancia. En lazo abierto, la impedancia de salida del inversor es simplemente la inductancia de filtro \( Z_{o,lp}=sL+R \). En lazo cerrado, la retroalimentación de tensión divide esa impedancia por \( 1+T_v(s) \) donde \( T_v \) es la ganancia de lazo de tensión. En la banda de paso del lazo, \( |T_v|\gg1 \), así que:

$$ Z_{o,GFM}(s) \approx \frac{sL+R}{1+T_v(s)} \approx \frac{sL}{T_v(s)} $$

Tanto en lazo abierto como en lazo cerrado, \( Z_{o,GFM} \) es **inductivo** (la fase sube de \( 0^\circ \) a \( +90^\circ \)). A 50 Hz, con \( L=2\,\text{mH} \): \( |Z_{o,GFM}(j\omega_0)| = \omega_0 L = 2\pi\cdot50\cdot0.002 = 0.628\,\Omega \), que a base 1 MVA / 690 V equivale a \( 0.628/0.476 \approx 0.13\,\text{pu} \). En lazo cerrado con \( |T_v(j\omega_0)|\approx20\,\text{dB} \) el módulo cae otro factor 10: \( Z_{o,GFM}\approx0.013\,\text{pu} \) —bajo, como corresponde a una fuente de tensión.

**GFL como fuente de corriente (Zo alta con región de fase negativa).** Un GFL controla la corriente mediante un lazo de corriente de alta ganancia. Para una fuente de corriente ideal, \( Z_o\to\infty \): la fuente mantiene la corriente independientemente de la tensión. En la práctica, el lazo de corriente tiene banda de paso finita y la PLL introduce dinámica adicional. El resultado es que \( Z_{o,GFL} \) es **grande** en magnitud (señal de fuente de corriente), pero su fase presenta una región **negativa** (parte real de \( Z_{o,GFL} \) negativa) en la banda de la PLL. Formalmente, en el marco síncronade la PLL el lazo de corriente en dq añade un término de \( -R_{neg} \) a la impedancia de salida equivalente en la frecuencia de cruce de la PLL:

$$ \text{Re}\{Z_{o,GFL}(j\omega_{pll})\} < 0 \quad\Rightarrow\quad \text{el GFL aporta energía en esa banda} $$

Esa resistencia negativa es la fuente de inestabilidad en red débil: si \( |R_{neg}| > R_{red} \) el sistema oscila. La condición cuantitativa (criterio de Nyquist al minor-loop gain) se desarrolla en [[interaccion-pll-red-debil]].

**Cómo se mide \( Z_o \) en la práctica.** Se inyecta una perturbación de tensión de pequeña amplitud \( \hat{v}_{inj} \) (por ejemplo 1% de Vn) en el PCC mientras el convertidor opera en estado estacionario; se mide la corriente resultante \( \hat{i}_{res} \); la impedancia de salida es \( \hat{Z}_o(j\omega)=\hat{v}_{inj}/\hat{i}_{res} \). Barriendo la frecuencia de inyección se obtiene el Bode de \( Z_o \). En simulación, esto equivale a añadir una fuente de tensión de perturbación y registrar las corrientes.

**La firma Bode de Zo y su lectura en estabilidad.** Un Bode de \( Z_o \) con:
- Fase mayoritariamente positiva (inductiva): **GFM bien diseñado**. Pasivo, estable con cualquier red inductiva.
- Región de fase negativa centrada en la banda PLL (10–100 Hz típicamente): **GFL**. Potencialmente inestable con \( Z_{red} \) grande en esa banda.

El criterio de impedancias de Sun dice: el sistema es estable si y solo si el minor-loop gain \( L(s)=Z_{red}(s)/Z_{o}(s) \) satisface el criterio de Nyquist. Si \( Z_o \) tiene fase negativa y \( Z_{red} \) tiene magnitud apreciable en esa banda, el minor-loop gain puede encirclar \( -1 \).

<div class="cfig"><img src="figuras/grid-forming-vs-following-analisis.png" alt="Análisis de impedancias, mapa de estabilidad, hueco de tensión y coexistencia GFL+GFM"><div class="cap">Cuatro paneles de análisis: (a) Bode de impedancia de salida: GFM inductivo y bajo, GFL alto con región de fase negativa en banda PLL. (b) Mapa de estabilidad: margen de fase del minor-loop gain vs SCR para GFL (se degrada en SCR bajo) y GFM (se degrada en SCR muy alto con droop agresivo). (c) Respuesta a hueco de tensión profundo: GFL pierde enganche de PLL, GFM limita la corriente y mantiene el ángulo. (d) Efecto de impedancia virtual del GFM sobre el SCR efectivo visto por el GFL coexistente.</div></div>

## 3 — El mapa de estabilidad: GFL en red débil, GFM en red fuerte

El **SCR** (Short-Circuit Ratio) del punto de conexión cuantifica la fortaleza de la red:

$$ SCR = \frac{S_{cc}}{S_n} = \frac{V_n^2/|Z_{red}|}{S_n} $$

Un SCR alto significa red fuerte (\( |Z_{red}| \) bajo); SCR bajo, red débil (\( |Z_{red}| \) alto). El mapa de estabilidad muestra cuál arquitectura funciona en cada región.

**GFL: inestable para SCR bajo.** El minor-loop gain del GFL es:

$$ L_{GFL}(s) = Z_{red}(s)\cdot Y_{GFL}(s) $$

donde \( Y_{GFL}=1/Z_{o,GFL} \) es la admitancia de salida del GFL. En SCR bajo, \( |Z_{red}| \) es grande; como \( Y_{GFL} \) tiene la región de fase negativa de la PLL, el producto \( Z_{red}\cdot Y_{GFL} \) tiene módulo alto con fase potencialmente adversa — el minor-loop puede encirclar \( -1 \). El SCR crítico para un GFL típico (PLL con BW de 20–50 Hz) está en el rango SCR\( _{crit,GFL} \approx 1.5\text{–}3 \). Por debajo de ese valor, oscilaciones subsíncronas o inestabilidad de la PLL llevan a la desconexión.

**GFM: potencialmente inestable para SCR muy alto.** El minor-loop del GFM es:

$$ L_{GFM}(s) = Z_{red}(s)\cdot Y_{GFM}(s) = \frac{Z_{red}(s)}{Z_{o,GFM}(s)} $$

Con un droop agresivo (lazo de potencia de banda ancha, frecuencia de cruce de droop \( f_{droop} \) alta), \( Z_{o,GFM} \) puede tener una región de fase negativa a frecuencias por encima de \( f_{droop} \). En red fuerte (\( Z_{red} \) bajo pero con inductancia dominante), el minor-loop gain aún puede tener margen de fase aceptable. Sin embargo, si el droop es muy agresivo y la red es muy fuerte y resistiva, el margen de fase del lazo de droop cae: SCR\( _{crit,GFM}\approx10\text{–}20 \) para droop agresivo (margen de fase \( PM < 30^\circ \) en red fuerte). Un GFM bien amortiguado (control de droop con integrador de potencia lento, \( f_{droop} < 5 \) Hz) es estable en todo el rango SCR normal de la red.

**La simetría entre SCR críticos.** Existe una relación aproximada:

$$ SCR_{crit,GFL} \cdot SCR_{crit,GFM} \approx K $$

donde \( K \) depende de los parámetros de control pero no del SCR. Esta simetría refleja que el mismo impedimento (\( Z_{red} \)) afecta a las dos arquitecturas en extremos opuestos. Para un convertidor típico de 1 MVA con los parámetros de esta ficha (\( L_1=2\,\text{mH} \), BW de PLL 30 Hz, droop moderado), \( SCR_{crit,GFL}\approx2{-}3 \) y \( SCR_{crit,GFM}\approx12\text{–}18 \): el producto cae en el rango 25–50, consistente con la literatura (Lin et al., NREL 2020).

**Implicación de diseño:** la elección de arquitectura la dicta el SCR esperado del punto de conexión:

| SCR del PCC | Arquitectura recomendada |
|---|---|
| SCR > 5 (red fuerte) | GFL: simple, eficiente, amplio historial |
| 3 < SCR < 5 (transición) | GFL con PLL robusta, o GFM con droop suave |
| SCR < 3 (red débil) | GFM obligatorio; GFL oscila o se desconecta |
| Isla / sin red | Solo GFM: el GFL no puede arrancar sin tensión externa |

## 4 — La PLL como diferenciador: por qué GFL necesita PLL y GFM no

**El problema de la sincronía.** Para que un inversor inyecte potencia activa (y no reactiva) a la red, su corriente de salida debe estar en fase con la tensión de red. En un convertidor en el marco dq, la potencia activa es \( P=\tfrac{3}{2}V_d\,i_d \) y la reactiva \( Q=-\tfrac{3}{2}V_d\,i_q \). Controlar \( P \) y \( Q \) independientemente requiere que el eje \( d \) esté alineado con la tensión de red. Eso exige conocer el ángulo instantáneo de la tensión en el PCC, \( \theta_{red}(t) \).

**GFL: el ángulo es una medida.** El GFL estima \( \theta_{red} \) midiendo \( v_{pcc} \) y filtrándola con una PLL (típicamente una PLL-SRF, ver [[pll-srf]]). La PLL convierte la tensión trifásica del PCC en el ángulo estimado \( \hat{\theta} \) que gira el marco dq. Con ese ángulo, el lazo de corriente impone \( i_d^*=2P^*/(3V_d) \) e \( i_q^*=-2Q^*/(3V_d) \). El problema es que \( v_{pcc} \) no es un dato externo puro: depende de la corriente que inyecta el propio GFL (vía \( Z_{red} \)):

$$ v_{pcc}(s) = V_g(s) + Z_{red}(s)\cdot i_{GFL}(s) $$

Así que el ángulo estimado \( \hat{\theta} \) que la PLL extrae de \( v_{pcc} \) depende de \( i_{GFL} \), que a su vez depende de \( \hat{\theta} \): el lazo se cierra. La ganancia de ese lazo es proporcional a \( |Z_{red}| \), de modo que en red débil la retroalimentación PLL→corriente→v\(_{pcc}\)→PLL tiene ganancia alta y puede desestabilizarse.

**GFM: el ángulo es una salida del control.** El GFM no mide \( \theta_{red} \): lo genera internamente integrando la frecuencia que calcula el control de droop:

$$ \omega(t) = \omega_0 + m_p(P_{set} - P_m(t)), \qquad \theta(t) = \int_0^t \omega(\tau)\,d\tau $$

El ángulo \( \theta \) es una variable de estado del control, no una medida de la red. La red no aparece en la ecuación de \( \theta \): el GFM impone su propio ángulo y la red se adapta. No hay lazo de realimentación de \( v_{pcc} \to \theta \): la medida de \( v_{pcc} \) entra solo en el lazo de tensión (para regular la amplitud \( E \)), pero no en el cálculo del ángulo.

**Por qué el GFM puede operar sin red.** Al no depender de \( v_{pcc} \) para su ángulo, el GFM puede generar tensión aunque \( v_{pcc}=0 \) (isla, arranque en negro). En esa condición la PLL de un GFL no puede sincronizar: sin tensión en el PCC, la PLL deriva y la inyección de corriente carece de referencia angular.

**Sincronización del GFM a la red existente.** En la práctica, cuando un GFM arranca con una red ya presente, el control de droop actúa como sincronizador natural: si la frecuencia interna del GFM es ligeramente distinta de la de la red, el flujo de potencia activa ajusta \( \omega \) hasta que el GFM se sincroniza en potencia (\( P_m\to P_{set} \)) y, por ello, en ángulo. Este mecanismo es idéntico al de sincronización de una máquina síncrona por oscilación del rotor: no necesita PLL, solo que el lazo de droop tenga dinámica convergente.

**Cuándo sí tiene PLL el GFM.** Algunos diseños de GFM incluyen una PLL como lazo secundario para mejorar la sincronización inicial o para condiciones de gran señal. En ese caso, la PLL está subordinada al control de droop y su BW es deliberadamente bajo (1–5 Hz), lo que la hace prácticamente invisible en la dinámica de pequeña señal. No es la PLL la que forma la tensión: solo asiste al arranque.

## 5 — Estabilidad en gran señal: huecos de tensión y cortocircuitos

La pequeña señal explica la estabilidad alrededor del punto de operación, pero las redes reales imponen perturbaciones grandes: huecos de tensión, cortocircuitos, conexión de cargas bruscas. La respuesta en gran señal diferencia aún más a GFL y GFM.

**El GFL ante un hueco profundo.** Cuando la tensión del PCC cae a \( v_{pcc}\to 0.2\,\text{pu} \) (hueco de categoría D según IEC 61000), la PLL del GFL recibe una tensión de entrada con amplitud muy reducida. La relación señal/ruido de la PLL cae: el integrador del filtro de lazo acumula error de fase. Si el descenso es suficientemente rápido (slew rate alto) o la profundidad suficientemente grande, la PLL puede perder el enganche ("phase slip"): el ángulo estimado \( \hat{\theta} \) se desvía más de \( \pi/2 \) del ángulo real de red. En ese punto, la corriente inyectada deja de estar sincronizada con la red: el control de corriente ve una referencia rotando en el marco equivocado y la corriente en el PCC puede dispararse. Los relés de protección detectan el evento como falta de sincronismo y desconectan el inversor.

**El GFM ante un hueco profundo.** El GFM tiene inercia de ángulo: su ecuación de swing,

$$ \frac{d^2\theta}{dt^2} = \frac{\omega_0}{2H}\left(P_{set} - P_m\right) $$

no depende directamente de \( v_{pcc} \). Ante un hueco, \( P_m \) cae (la potencia transmitida cae con la tensión), por lo que \( d^2\theta/dt^2 \) se hace positivo (el ángulo se acelera), pero la inercia \( H \) frena esa aceleración. El ángulo se desvía gradualmente —no instantáneamente— mientras dura el hueco. Si el hueco es breve (< varios ciclos) y la tensión se recupera antes de que el ángulo supere \( \pi/2 \) respecto a la red, el GFM vuelve a sincronizar naturalmente. Esta es la propiedad de **estabilidad transitoria** del GFM, análoga a la de una máquina síncrona.

**Limitación de corriente en el GFM.** Durante el hueco, la caída de \( v_{pcc} \) implica que \( \Delta V = E - v_{pcc} \) aumenta, y con ello la corriente \( I = \Delta V / Z_o \). Un GFM sin limitación de corriente puede circular hasta 5–10 pu de corriente si \( Z_o \) es pequeño y el hueco es profundo. Los semiconductores admiten 1.1–1.5 pu de corriente pico. Por eso todo GFM real incluye un limitador de corriente: cuando \( |i| > i_{max} \), el control cambia momentáneamente de modo tensión a modo corriente (o recorta la referencia de tensión interna \( E \)). La implementación de ese limitador sin perder las propiedades de formación de red es uno de los temas de investigación activa (Taul et al., 2020).

**Comparativa de respuesta a cortocircuito:**

| Aspecto | GFL | GFM |
|---|---|---|
| Corriente durante el cortocircuito | Controlada explícitamente por el lazo de corriente a \( i_{max} \) | Limitada implícitamente por \( Z_o \); sin limitador activo puede superar \( i_{max} \) |
| Pérdida de sincronía | Probable si \( v_{pcc} \) cae suficientemente o es brusco | Improbable para huecos breves; depende de la inercia \( H \) |
| Tensión durante el cortocircuito | El GFL no soporta \( v_{pcc} \): si la red colapsa, no hay tensión | El GFM sostiene \( v_{pcc} \) durante el evento (como una máquina síncrona) |
| Recuperación tras el evento | Necesita resincronización de PLL | Recuperación natural por el lazo de droop |

**El caso de red sin generadores síncronos.** Si todos los generadores síncronos se desconectan durante el evento, la red queda sin fuente de tensión. El GFL no puede arrancar en esas condiciones (no hay tensión para la PLL). El GFM sí: sostiene la tensión del PCC desde su referencia interna y permite el arranque de cargas y de otros inversores.

## 6 — La transición GFL→GFM: cuándo y cómo

**El escenario extremo.** Considera una microrred o red débil con varios inversores GFL y una única máquina síncrona pequeña. Si esa máquina se desconecta por una falta o por mantenimiento, la red pierde su única fuente de tensión y ángulo. Los GFL quedan sin referencia: la PLL de cada uno ve \( v_{pcc}=0 \) o una tensión sin sincronismo, no puede engancharse, y los inversores se desconectan por protección. La red colapsa en oscuridad (apagón).

**El rol del GFM como formador de red.** Un GFM evita ese colapso. Su control de droop integra su propio ángulo y genera la tensión del PCC desde sus condensadores de bus DC. En cuanto hay tensión en el PCC (incluso antes de que otros inversores arranquen), los GFL pueden sincronizarse y conectarse. El GFM es la "columna vertebral" de la red.

**Black start.** El arranque en negro (black start) es la capacidad de formar una red partiendo de cero (sin tensión externa). El GFM puede hacerlo: arranca generando tensión en isla, sincroniza cargas esenciales, y luego conecta unidades adicionales. Un GFL no puede: necesita tensión preexistente para operar.

**La transición durante operación (mode switching).** En algunos esquemas, un mismo inversor puede cambiar entre GFL y GFM según el estado de la red (transición en caliente, "fly mode switching"). El reto es que en el instante del cambio:
- El ángulo que tenía la PLL (\( \hat{\theta}_{PLL} \)) puede diferir del ángulo que el control de droop calcularía para la misma potencia.
- La corriente de referencia del modo GFL puede diferir de la que generaría la tensión del modo GFM.
- La diferencia de ángulo o corriente en el instante de transición produce un transitorio: un pico de corriente que puede disparar las protecciones si el cambio no se gestiona con preacondicionamiento.

La solución estándar es inicializar el integrador de ángulo del GFM con \( \hat{\theta}_{PLL} \) justo antes del cambio, y el estado del lazo de potencia del droop con la potencia real en ese instante. Así el transitorio de ángulo es nulo; la diferencia de corriente es pequeña y converge rápidamente.

**Requisitos regulatorios (grid codes).** La tendencia regulatoria en redes de alta penetración renovable es exigir capacidad GFM en un porcentaje creciente de la potencia instalada:
- ENTSO-E (Europa): borrador de requisito de que al menos el 30–50% de la potencia renovable cumpla características de formación de red (inertia response, voltage-forming) para 2030.
- AEMO (Australia): requisito de "strong grid support" en zonas con SCR esperado < 3 (South Australia, Victoria occidental).
- GB (National Grid ESO): "GC0137 Future of Distributed Inverters" — requisito de sincronización sin PLL para inversores > 1 MVA en redes débiles.

La tendencia es que GFM deje de ser una opción de diseño para convertirse en un requisito de conectividad.

## 7 — Diseño de la impedancia virtual para hacer coexistir GFL y GFM

En un parque real, no todos los inversores son GFM: los costos de control y los requisitos de tiempo de respuesta hacen que coexistan GFL y GFM en la misma barra. La pregunta de diseño es: ¿cómo hacer que el GFL coexistente sea estable aunque el SCR de la red sea bajo?

**La impedancia virtual del GFM como escudo para el GFL.** El GFM con impedancia virtual \( jX_{virt} \) (añadida en el control como un término de caída de tensión: \( E_{ref}=E_{set}-jX_{virt}\cdot i_{GFM} \)) presenta hacia la red una impedancia de salida:

$$ Z_{o,GFM}^{eff}(s) = Z_{o,GFM}^{base}(s) + jX_{virt} $$

Desde el punto de vista del GFL, la barra del PCC ya no tiene \( Z_{red} \) pura: tiene \( Z_{red} \) en paralelo con \( Z_{o,GFM}^{eff} \). La impedancia efectiva que el GFL ve en su minor-loop es:

$$ Z_{red,eff} = Z_{red} \,\|\, Z_{o,GFM}^{eff} = \frac{Z_{red}\cdot Z_{o,GFM}^{eff}}{Z_{red}+Z_{o,GFM}^{eff}} $$

Si \( |Z_{o,GFM}^{eff}| \gg |Z_{red}| \) (el GFM tiene mucha impedancia de salida), el paralelo es dominado por \( Z_{red} \) y el GFM no ayuda. Si \( |Z_{o,GFM}^{eff}| \sim |Z_{red}| \), el paralelo reduce la impedancia resultante, aumentando el SCR efectivo visto por el GFL.

**Ejemplo numérico (parámetros de la ficha).** Base: \( S_n=1\,\text{MVA} \), \( V_{LL}=690\,\text{V} \), \( Z_{base}=V_n^2/S_n=0.476\,\Omega \). SCR de red = 2 (red débil: \( |Z_{red}|=Z_{base}/SCR=0.238\,\Omega \approx 0.5\,\text{pu} \)).

Un GFL aislado con SCR = 2 estaría al límite o inestable (\( SCR_{crit,GFL}\approx2\text{–}3 \) para PLL de BW = 30 Hz).

Añadimos un GFM de la misma potencia nominal con impedancia virtual \( X_{virt}=0.1\,\text{pu} = 0.0476\,\Omega \). La impedancia de salida efectiva del GFM en pu:

$$ Z_{o,GFM}^{eff} \approx jX_{virt} = j0.1\,\text{pu} $$

El paralelo \( Z_{red}\| Z_{o,GFM}^{eff} \) a 50 Hz (con \( Z_{red}=j0.5\,\text{pu} \) para red puramente inductiva):

$$ Z_{red,eff} = \frac{j0.5 \cdot j0.1}{j0.5 + j0.1} = \frac{-0.05}{j0.6} = \frac{0.05}{0.6}\angle{-90^\circ} = j0.083\,\text{pu} $$

El SCR efectivo visto por el GFL:

$$ SCR_{eff} = \frac{1}{|Z_{red,eff}|} = \frac{1}{0.083} \approx 12 $$

Con \( X_{virt}=0.1\,\text{pu} \), el SCR efectivo sube de 2 a 12: el GFL que era inestable pasa a operar con margen de estabilidad amplio. La tabla completa:

| \( X_{virt} \) (pu) | \( |Z_{o,GFM}^{eff}| \) (pu) | \( |Z_{red,eff}| \) (pu) | \( SCR_{eff} \) |
|---|---|---|---|
| 0 (sin GFM) | — | 0.500 | 2.0 (inestable) |
| 0.05 | 0.05 | 0.042 | 4.0 (esterilidad límite) |
| 0.10 | 0.10 | 0.083 | 12.0 (estable) |
| 0.20 | 0.20 | 0.143 | 3.5 (estable con margen) |

Nota: el caso \( X_{virt}=0.20\,\text{pu} \) da SCR efectivo menor que \( X_{virt}=0.10 \) porque el paralelo de una impedancia grande con \( Z_{red} \) converge hacia \( Z_{red} \) cuando \( X_{virt}\gg|Z_{red}| \); el óptimo está en \( X_{virt}\approx|Z_{red}| \).

**Trade-off: regulación de tensión vs SCR efectivo.** La impedancia virtual hace caer la tensión del GFM ante una inyección de corriente: \( \Delta V = X_{virt}\cdot I \). Con \( X_{virt}=0.1\,\text{pu} \) e \( I=1\,\text{pu} \), la caída de tensión del GFM en régimen permanente es \( 0.1\,\text{pu} \) — un 10% de la nominal, lo cual puede exceder la banda de regulación del control de tensión (\( \pm5\% \) típicamente). Para mantener \( v_{pcc} \) dentro de límites, el lazo de tensión del GFM debe compensar esa caída en régimen permanente, lo que es posible con un integrador. En transitorio, la compensación no es instantánea, así que hay un período de algunos ciclos con tensión fuera de la banda nominal. El diseño debe equilibrar velocidad del lazo de tensión vs \( X_{virt} \).

**Resumen del procedimiento de diseño de coexistencia:**
1. Determinar el SCR de la red y el \( SCR_{crit,GFL} \) del inversor GFL a conectar.
2. Si \( SCR < SCR_{crit,GFL} \): añadir al menos un GFM.
3. Elegir \( X_{virt} \approx |Z_{red}| \) para maximizar la reducción de \( Z_{red,eff} \).
4. Verificar que la caída de tensión en régimen permanente sea compensable por el lazo de tensión del GFM.
5. Comprobar por simulación que el margen de fase del minor-loop del GFL con \( Z_{red,eff} \) es > 30° en toda la banda relevante (10–500 Hz).

## Cuándo y por qué se usa
- **GFL**: redes fuertes (SCR > 5), plantas que solo "siguen" la red. La mayoría del parque fotovoltaico y eólico instalado actualmente es GFL.
- **GFM**: alta penetración renovable, microrredes, operación en isla, redes débiles (SCR < 3), black start, requisitos de inertia response o voltage forming de los grid codes.

## Procedimiento de diseño (genérico)
1. Estima el **SCR** del punto de conexión (ver [[red-thevenin-scr]]).
2. SCR > 5 y solo aportar energía → GFL (más simple, amplio historial industrial).
3. SCR < 3 o requisito de formación de red → GFM con droop o VSM.
4. Coexistencia GFL+GFM en misma barra: dimensiona \( X_{virt} \) del GFM según el SCR efectivo requerido.
5. Comprueba estabilidad por impedancia: GFL tiende a inestabilizar en red débil; GFM con droop agresivo, en red **fuerte** (ver [[impedancia-salida-estabilidad]]).
6. Para transición de modo: inicializa el integrador del droop con \( \hat{\theta}_{PLL} \) para eliminar el transitorio de ángulo.

## Ejemplo de código
```python
# GFM: el angulo lo fija el control, no una PLL
w = w0 + mp*(Pset - Pm)      # frecuencia propia (droop)
theta += w*dt                # integra su propio angulo
E_ref = E_set - 1j*Xvirt*i  # caida en impedancia virtual

# GFL: el angulo viene de la PLL
# theta = pll(v_pcc)         # estima el angulo de la red
# id_ref = 2*P_ref/(3*Vd)   # consigna en dq
# iq_ref = -2*Q_ref/(3*Vd)
```

## Parámetros y valores típicos
- SCR: red fuerte > 10, media 3–10, débil < 3, isla = 0.
- \( X/R \) de red: 2–10 (transmisión más inductiva, distribución más resistiva).
- BW de PLL típico: 20–100 Hz; cuanto más ancho, más sensible a la impedancia de red.
- Droop de frecuencia: \( m_p = \Delta\omega/\Delta P \approx 0.031\,\text{rad/s/W} \) para 1 MVA con 5% de droop.
- \( X_{virt} \) típico: 0.05–0.15 pu.

## Errores comunes
- Usar GFL en red muy débil → oscilaciones subsíncronas o desconexión por pérdida de PLL.
- Asumir que GFM es estable siempre: con droop agresivo puede inestabilizar en red **fuerte** (lo opuesto al GFL).
- Poner \( X_{virt} \gg |Z_{red}| \): el SCR efectivo mejora poco pero la caída de tensión se vuelve inaceptable.
- Cambiar de GFL a GFM en caliente sin inicializar el integrador de ángulo → transitorio de corriente que dispara las protecciones.
- Creer que el GFM no necesita limitación de corriente: sin limitador activo, un hueco profundo puede causar corriente > 5 pu.

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: arquitectura): se eligió GFM con droop. En Fase 3 se vio
  que el GFM bien amortiguado es estable en todo el rango de SCR; el caso crítico (SCR≈3.35)
  solo aparece con control agresivo y en red fuerte.
- **02 - GFL-Impedance**: se usa GFL; la inestabilidad en SCR bajo (SCR < 2.8) se atribuye
  a la interacción de la PLL con la impedancia de red, confirmando el mapa de estabilidad.

## Conceptos relacionados
- [[droop-control]] · [[vsm-inercia]] · [[impedancia-salida-estabilidad]] · [[red-thevenin-scr]]
- [[interaccion-pll-red-debil]] · [[pll-srf]] · [[impedancia-virtual]]

## Referencias
- Lin et al., *Research Roadmap on Grid-Forming Inverters*, NREL 2020.
- Rocabert et al., *Control of Power Converters in AC Microgrids*, IEEE TPEL 2012.
- Sun, *Impedance-Based Stability Criterion for Grid-Connected Inverters*, IEEE TPEL 2011.
- Harnefors et al., *Passivity-Based Stability Assessment of Grid-Connected VSCs*, IEEE JETCAS 2016.
- Taul et al., *Current Limiting Control with Enhanced Dynamics of Grid-Forming Converters*, IEEE JETCAS 2020.
