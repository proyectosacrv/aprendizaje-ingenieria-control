---
titulo: Matching control (control por emparejamiento)
slug: matching-control
categoria: control
tipo: tecnica
nivel: avanzado
proyectos: []
objetivos: [emparejar la dinámica del bus DC con la frecuencia de red para sincronización natural]
tags: [matching, grid-forming, bus-dc, sincronizacion, energia, avanzado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-02
relacionados: [grid-forming-vs-following, vsm-inercia, power-synchronization-control, dinamica-bus-dc, ecuacion-oscilacion]
referencias:
  - "Arghir, Jouini, Dörfler, Grid-Forming Control for Power Converters based on Matching, Automatica 2018"
  - "Dörfler et al., Taming Instabilities in Power Grid Networks, Physica D 2016"
---

## Definición
Estrategia grid-forming que **empareja** la dinámica del condensador del bus DC con la ecuación de
sincronización de un generador síncrono: la tensión del bus \( v_{dc} \) actúa como variable de
frecuencia, de modo que la sincronización se produce de forma **física y natural** sin bucles de
control artificiales.

## Fundamento teórico
En un generador síncrono la variable de sincronización es la velocidad \( \omega \). En un
convertidor, el equivalente natural es la tensión del bus DC \( v_{dc} \) (su cuadrado es la
energía almacenada \( E=\tfrac12 Cv_{dc}^2 \), igual que la cinética \( E=\tfrac12 J\omega^2 \)).
La idea del matching es **asignar el ángulo** del convertidor directamente proporcional al bus DC:
$$ \dot\theta = k_{match}\,v_{dc} $$
y diseñar el control de modulación para que el balance de energía del condensador sea
$$ C\,v_{dc}\dot v_{dc} = P_s - P_e $$
idéntico a la swing equation con \( \omega\equiv k_{match}v_{dc} \). El resultado es:
- La tensión del bus **oscila** con la potencia, como la frecuencia de un generador.
- La sincronización con la red emerge de la dinámica física del almacenamiento DC.
- No se necesita PLL ni lazo de frecuencia artificial.
- **Ventaja**: la inercia es la del condensador real (no virtual), la estabilidad es intrínseca.
- **Limitación**: el bus DC oscila con la carga (no regulado a tensión constante), lo que requiere
  dimensionar \( C \) para el rizado de frecuencia admisible y es incompatible con topologías que
  exigen bus DC estricto.

La conexión formal con el VSM: tomando \( J_{v}=C/k_{match}^2 \) se recupera la inercia virtual
equivalente del condensador. El matching es el camino más corto desde la física del convertidor
hasta la dinámica del generador.

<div class="cfig"><img src="figuras/matching-control-swing.png" alt="tension del bus DC oscilando como un swing tras un escalon de potencia"><div class="cap">Al asignar $\dot\theta=k\,v_{dc}$, la tensión del bus DC hace de frecuencia: ante un escalón de potencia oscila y se asienta igual que el ángulo de un generador síncrono (ecuación de swing), con la inercia del condensador real. La sincronización emerge de la física del almacenamiento, sin PLL ni lazo de frecuencia.</div></div>

## 1 — Analogía bus DC ↔ frecuencia: derivación de la dinámica equivalente

**Paso 1 — energía en el bus DC.** El condensador de bus almacena energía:

$$ E_{DC} = \tfrac{1}{2}C\,v_{dc}^2 $$

La derivada temporal da el balance de potencia:

$$ \frac{dE_{DC}}{dt} = C\,v_{dc}\frac{dv_{dc}}{dt} = P_{in} - P_{out} \quad\Rightarrow\quad \frac{dv_{dc}}{dt}=\frac{P_{in}-P_{out}}{C\,v_{dc}} $$

**Paso 2 — ecuación de swing del generador síncrono.** La segunda ley de Newton para el rotor (en pu con \( \omega_0 \) la pulsación nominal) es:

$$ \frac{2H}{\omega_0}\frac{d\omega}{dt} = P_m - P_e $$

donde \( H \) [s] es la constante de inercia, \( P_m \) la potencia mecánica y \( P_e \) la eléctrica.

**Paso 3 — emparejamiento.** El matching asigna:

$$ \dot\theta = k_{match}\,v_{dc} \quad\Leftrightarrow\quad \omega \equiv k_{match}\,v_{dc} $$

Derivando esta relación:

$$ \dot\omega = k_{match}\,\dot v_{dc} = k_{match}\,\frac{P_{in}-P_{out}}{C\,v_{dc}} = \frac{k_{match}^2}{C\,\omega}\,(P_{in}-P_{out}) $$

**Paso 4 — identificación del parámetro equivalente.** Comparando con la swing equation:

$$ \frac{2H}{\omega_0}\dot\omega = P_m - P_e \quad\Leftrightarrow\quad \frac{C}{k_{match}^2}\,\omega\,\dot\omega = (P_{in}-P_{out})\,\omega $$

En el entorno de \( \omega\approx\omega_0 \), la inercia virtual equivalente del condensador es:

$$ \boxed{J_v = \frac{C}{k_{match}^2}, \qquad H_v = \frac{J_v\,\omega_0^2}{2\,S_n}} $$

El condensador físico hace el papel de la masa rotante: más \( C \) → más inercia; más \( k_{match} \) → misma \( C \) da menos inercia (el ángulo es más sensible a \( v_{dc} \)). La sincronización emerge del balance energético sin ningún lazo de frecuencia artificial.

## 2 — La idea: la dinámica del bus DC = la dinámica de la máquina

La analogía del apartado anterior se puede expresar de forma compacta en una tabla de equivalencias que muestra que **las dos ecuaciones son matemáticamente idénticas**.

### La swing equation y el balance DC: la misma ecuación

La swing equation del generador:

$$ J\,\omega\,\frac{d\omega}{dt} = P_{mec} - P_{elec} $$

El balance de energía del bus DC (usando \( E_{DC}=\tfrac12 C\,v_{dc}^2 \)):

$$ C\,v_{dc}\,\frac{dv_{dc}}{dt} = P_{in} - P_{out} $$

Estas dos ecuaciones son idénticas bajo la correspondencia:

| Generador síncrono | Matching control (convertidor) |
|---|---|
| \( J \) [kg·m²] (inercia del rotor) | \( C \) [F] (capacidad del bus DC) |
| \( \omega \) [rad/s] (velocidad angular) | \( V_{dc} \) [V] (tensión del bus) |
| \( E_{cin}=\tfrac12 J\omega^2 \) [J] | \( E_{DC}=\tfrac12 C V_{dc}^2 \) [J] |
| \( P_{mec} \) (turbina, primotractor) | \( P_{in} \) (generación: FV, batería, viento) |
| \( P_{elec} \) (salida a la red) | \( P_{out} \) (inversor → red) |
| \( \theta = \int\omega\,dt \) (ángulo del rotor) | \( \theta = k\int V_{dc}\,dt \) (ángulo de la portadora) |
| \( H \) [s] (constante de inercia) | \( H_v = C\omega_0^2/(2S_n k^2) \) |

### El matching como realimentación "gratuita"

La clave del matching es que **no necesita lazo de control explícito para la sincronización**. El mecanismo es:

1. Supón que la carga aumenta: \( P_{out} \) sube.
2. El balance del bus: \( C\,V_{dc}\,\dot V_{dc} = P_{in} - P_{out} < 0 \) → \( V_{dc} \) baja.
3. El ángulo: \( \dot\theta = k\,V_{dc} \) → \( \dot\theta \) baja → la frecuencia del convertidor baja.
4. Una frecuencia más baja significa que el convertidor se está desacelerando respecto a la red → su ángulo de carga \( \delta \) aumenta.
5. Mayor \( \delta \) → mayor \( P_{out} = (EV/X)\sin\delta \) → el sistema se reequilibra.

Este mecanismo de realimentación negativa emerge de la física del almacenamiento, igual que el droop natural de un generador síncrono. El control solo necesita asignar \( \dot\theta = k\,V_{dc} \); todo lo demás ocurre solo.

### La constante de emparejamiento \( k_{match} \)

El parámetro \( k_{match} \) [rad/(s·V)] es la única constante de diseño del matching:

$$ k_{match} = \frac{\omega_0}{V_{dc0}} $$

Esta elección es la más natural: cuando \( V_{dc} = V_{dc0} \) (tensión nominal del bus), el convertidor oscila a exactamente \( \omega_0 \) (frecuencia nominal de red). Si el bus baja un 1 % (\( V_{dc}=0.99\,V_{dc0} \)), la frecuencia baja un 1 % (\( \omega=0.99\,\omega_0 \)): la desviación de frecuencia es proporcional a la desviación de tensión del bus, con factor \( k_{match} \).

<div class="cfig"><img src="figuras/matching-control-analisis.png" alt="Matching control: analogía, respuesta Vdc, comparativa droop, BESS y SOC"><div class="cap">Panel (a): tabla de equivalencia máquina síncrona vs matching. Panel (b): $V_{dc}(t)$ ante escalón de 200 kW; el matching oscila (como una máquina) mientras el PI mantiene $V_{dc}$ constante. Panel (c): droop vs matching en pequeña y gran señal. Panel (d): $V_{dc}(t)$ y SOC(t) durante soporte de frecuencia con BESS; la inercia desaparece cuando SOC→0 %.</div></div>

## 3 — La ley de control del matching

### Cómo se genera la potencia activa

En un convertidor VSC con modulación sinusoidal, la tensión interna generada es:

$$ E = \frac{m}{2}\,V_{dc} $$

donde \( m \) es el índice de modulación (adimensional, típicamente \( m\approx0.9 \) para maximizar la tensión de salida sin sobremodulación). La potencia activa entregada a la red (con reactancia de acoplamiento \( X \) y tensión de red \( V \)) es:

$$ P = \frac{3}{2}\cdot\frac{E\,V}{X}\sin\delta = \frac{3}{2}\cdot\frac{m\,V_{dc}\,V}{2X}\sin\delta $$

### El lazo de realimentación implícito

Supongamos que \( V_{dc} \) sube (por ejemplo, porque \( P_{in} \) aumentó). Entonces:

1. \( E = m\,V_{dc}/2 \) sube → \( P \) sube (con el mismo \( \delta \)).
2. El bus DC transfiere más potencia a la red → \( C\,V_{dc}\,\dot V_{dc} = P_{in} - P < 0 \) → \( V_{dc} \) baja de vuelta.

Este es un lazo de realimentación negativo **intrínseco**: el bus DC regula su propia tensión mediante la variación de potencia, sin ningún lazo PI externo. La ganancia de este lazo depende de:

$$ \frac{\partial P}{\partial V_{dc}} = \frac{3}{2}\cdot\frac{m\,V\,\sin\delta}{2X} $$

### La sintonía del matching: elegir \( m \)

El índice de modulación \( m \) fija la ganancia del lazo de realimentación. Un \( m \) grande → más potencia por voltio de variación de \( V_{dc} \) → el bus se regula más rápido pero la tensión oscila menos (el sistema es más rígido). Un \( m \) pequeño → menos ganancia → el bus oscila más (más inercia efectiva).

La condición de sintonía es que la inercia equivalente \( H_v \) sea la deseada:

$$ H_v = \frac{C\,\omega_0^2}{2\,S_n\,k_{match}^2} = \frac{C\,V_{dc0}^2}{2\,S_n} $$

(sustituyendo \( k_{match}=\omega_0/V_{dc0} \)). Para un sistema de 1 MVA con \( V_{dc0}=700\,\text{V} \) y \( H_v=4\,\text{s} \):

$$ C = \frac{2\,H_v\,S_n}{V_{dc0}^2} = \frac{2\cdot4\cdot10^6}{700^2} \approx 16.3\,\text{mF} $$

Este es el condensador necesario para emular 4 s de inercia. A mayor \( H_v \) deseado, mayor \( C \) necesario.

## 4 — Matching vs droop: dos caras de la misma moneda

### La diferencia conceptual

El droop GFM y el matching control producen comportamientos similares en pequeña señal, pero parten de conceptos opuestos:

**Droop:** toma la frecuencia de red como referencia explícita. Mide la potencia, la filtra, y ajusta la frecuencia del oscilador virtual: \( \omega = \omega_0 + m_p(P_{set}-P) \). La frecuencia *de red* \( \omega_0 \) es el punto de referencia. El ángulo se integra sobre esa referencia.

**Matching:** no usa la frecuencia de red como referencia. El ángulo se integra sobre \( k\,V_{dc} \): la frecuencia del convertidor es \( k\,V_{dc} \), que varía con la potencia a través del balance del bus DC. La red no entra explícitamente en el lazo de sincronización.

### En estado estacionario: el mismo resultado

En régimen permanente, ambos dan el mismo punto de operación. Para el droop, en el equilibrio:
\( \omega=\omega_0 \), \( m_p(P_{set}-P_0)=0 \) → \( P_0=P_{set} \).

Para el matching, en el equilibrio: \( \dot V_{dc}=0 \) → \( P_{in}=P_{out} \) → el bus está equilibrado en \( V_{dc}=V_{dc0} \) → \( \dot\theta=k\,V_{dc0}=\omega_0 \). Ambos operan a frecuencia nominal con la misma potencia de consigna.

### Ante perturbaciones pequeñas: comportamiento igual

En pequeña señal, el droop con filtro de potencia de primer orden tiene la función de transferencia:

$$ \Delta\omega(s) = \frac{-m_p\,\omega_f}{s+\omega_f}\,\Delta P(s) $$

El matching tiene la dinámica del bus DC, que en pequeña señal alrededor de \( V_{dc0} \):

$$ \Delta\dot V_{dc} = \frac{\Delta P_{in}-\Delta P_{out}}{C\,V_{dc0}} \quad\Rightarrow\quad \Delta\omega = k\,\Delta V_{dc} $$

Ambas respuestas son equivalentes cuando \( k_{match}^2/C \equiv m_p\,\omega_f/\omega_0 \). La inercia del matching emula exactamente la del droop con la sintonía correcta.

### Ante perturbaciones grandes: el matching es más robusto

La diferencia aparece en gran señal. El droop usa \( \sin\delta \) para la potencia, pero la medida de \( P \) se filtra y puede retrasarse durante transitorios rápidos. El matching, en cambio, regula el balance energético directamente: la potencia sale del bus DC sin lazo de medición intermedio. Para perturbaciones bruscas (falta de generación, cortocircuito cercano), el matching responde más rápido porque la realimentación es física, no calculada.

Adicionalmente, el matching no tiene el problema de la inicialización de la referencia de frecuencia: el droop necesita conocer \( \omega_0 \) de la red; el matching simplemente sigue \( V_{dc} \) y se sincroniza.

## 5 — El matching en sistemas con BESS

La aplicación más directa del matching es en sistemas con batería en el bus DC (**BESS: Battery Energy Storage System**).

### El SOC como "inercia disponible"

En un sistema de almacenamiento, la energía cinética de un generador tiene su equivalente en el estado de carga de la batería:

$$ E_{cin} = \tfrac12 J\omega^2 \;\leftrightarrow\; E_{BESS} = Q_{bat}\,V_{bat}\cdot\text{SOC} $$

Mientras el SOC está entre el 20 % y el 80 %, la batería puede ceder o absorber potencia libremente: el convertidor ofrece inercia virtual plena. Cuando el SOC alcanza sus límites (0 % o 100 %), la batería no puede seguir cediendo ni absorbiendo energía: la "inercia virtual" **desaparece**.

### La consecuencia sobre el matching

Con el matching activo y SOC alto:
- \( P_{in} \) (batería) puede subir libremente cuando la red pide más potencia.
- \( V_{dc} \) se mantiene cerca de \( V_{dc0} \) gracias al balance del bus.
- La inercia efectiva es \( H_v = C V_{dc0}^2/(2S_n) \), que es la del condensador del filtro (pequeña, del orden de ms).

**Nota:** la inercia del matching viene del condensador del bus, no de la batería. La batería aporta la energía para el soporte de frecuencia sostenido, pero no la inercia instantánea (que es del condensador). Para obtener más inercia con matching hay que aumentar \( C \), no la capacidad de la batería.

Cuando el SOC llega a 0 %:
- \( P_{in}\to0 \): la batería no puede dar más energía.
- El balance del bus ya no se satisface: \( C\,V_{dc}\,\dot V_{dc} = 0 - P_{out} < 0 \) → \( V_{dc} \) cae.
- El matching ya no puede mantener \( \dot\theta = k\,V_{dc0} \): la frecuencia del convertidor cae por debajo de la red → el inversor pierde la sincronización.
- El convertidor debe desconectarse o reducir su potencia a cero.

### Dimensionado del bus DC para soporte de frecuencia

Para un soporte de frecuencia de duración \( T_{sop} \) a potencia \( P_{sop} \), la energía que debe dar la batería es:

$$ E_{sop} = P_{sop}\cdot T_{sop} $$

La variación de SOC durante el soporte:

$$ \Delta\text{SOC} = \frac{E_{sop}}{E_{bat}} = \frac{P_{sop}\cdot T_{sop}}{Q_{bat}\cdot V_{bat}} $$

Para que el SOC no llegue a 0 % durante el soporte, se necesita \( \text{SOC}_{inicial} > \Delta\text{SOC} \). Con \( P_{sop}=200\,\text{kW} \), \( T_{sop}=30\,\text{s} \) y \( E_{bat}=500\,\text{kWh}=1800\,\text{MJ} \):

$$ \Delta\text{SOC} = \frac{200\times10^3\cdot30}{1.8\times10^9} \approx 0.33\,\% $$

La batería de 500 kWh tiene energía más que suficiente: el SOC apenas varía en un soporte de 30 s.

## 6 — Diseño iterativo

El diseño del matching control para emular \( H=4\,\text{s} \) con un sistema de 1 MVA en un bus DC de 700 V.

### Especificación de partida

- Inercia deseada: \( H_v = 4\,\text{s} \).
- Rizado de tensión del bus admisible: \( \Delta V_{dc} < 5\,\% \) ante \( \Delta P = 10\,\%\,S_n = 100\,\text{kW} \) durante \( H_v = 4\,\text{s} \).
- Frecuencia del convertidor debe seguir al bus DC con fidelidad.

### Paso 1: calcular \( C \) para la inercia requerida

De la fórmula \( H_v = C V_{dc0}^2 / (2 S_n) \):

$$ C = \frac{2\,H_v\,S_n}{V_{dc0}^2} = \frac{2\cdot4\cdot10^6}{700^2} = \frac{8\times10^6}{490000} \approx 16.3\,\text{mF} $$

Verificación del rizado: ante \( \Delta P = 100\,\text{kW} \) durante \( \Delta t \approx H_v = 4\,\text{s} \):

$$ \Delta V_{dc} \approx \frac{\Delta P\cdot\Delta t}{C\cdot V_{dc0}} = \frac{10^5\cdot4}{16.3\times10^{-3}\cdot700} \approx \frac{4\times10^5}{11.4} \approx 35\,\text{kV} $$

Este resultado es absurdo porque durante un escalón de potencia de 100 kW el bus no carga solo 4 s de inercia: la batería también responde. El rizado de \( V_{dc} \) durante un escalón transitorio es mucho menor porque la corriente de entrada del rectificador/batería reacciona en milisegundos. El cálculo correcto del rizado de alta frecuencia (durante 1–2 periodos de conmutación) da:

$$ \Delta V_{dc,HF} \approx \frac{P_{sw}\cdot T_{sw}}{C\cdot V_{dc0}} \approx \frac{10^5\cdot\frac{1}{5000}}{16.3\times10^{-3}\cdot700} \approx 1.75\,\text{V} \approx 0.25\,\% $$

dentro del requisito del 5 %.

### Paso 2: verificar la ganancia del lazo de potencia

Con \( k_{match} = \omega_0/V_{dc0} = 314.16/700 = 0.449\,\text{rad/(s·V)} \), la inercia equivalente es:

$$ J_v = C/k_{match}^2 = 16.3\times10^{-3}/0.449^2 \approx 80.8\,\text{kg·m}^2 $$

$$ H_v = J_v\omega_0^2/(2S_n) = 80.8\times314.16^2/(2\times10^6) \approx 3.99\,\text{s} \approx 4\,\text{s} \checkmark $$

### Verificación por simulación ante escalón de carga

Los resultados de la simulación (ver figura) confirman:
- \( V_{dc}(t) \) ante escalón de 200 kW: el matching permite una oscilación de \( V_{dc} \) de ±5 V (0.7 %) que se asienta en \( \approx2\,\text{s} \). El control PI clásico mantiene \( V_{dc} \) constante pero no ofrece inercia.
- Respuesta de frecuencia: el matching da el mismo comportamiento que el droop equivalente en pequeña señal; la diferencia aparece en escalones grandes (>20 % de \( S_n \)) donde el matching es más suave.
- BESS: el SOC baja linealmente durante el soporte; cuando llega a 0 %, \( V_{dc} \) colapsa y la inercia desaparece bruscamente.

## Cuándo y por qué se usa
Convertidores con fuente de energía en el bus DC (BESS, supercondensadores) donde el rizado de
tensión DC es aceptable, y donde se quiere la máxima simplicidad de control con inercia genuina.
Es un marco teórico que también justifica y conecta VSM, PSC y droop.

## Procedimiento de diseño (genérico)
1. Elige \( k_{match} \) de modo que el rango de \( v_{dc} \) corresponda al rango de frecuencia
   admisible: \( \Delta\omega=k_{match}\Delta v_{dc} \).
2. Dimensiona \( C \) para la inercia efectiva deseada \( J_v=C/k_{match}^2 \).
3. Diseña el control de modulación para imponer \( \dot\theta=k_{match}v_{dc} \) y eliminar el
   término de acoplo d-q.
4. Añade regulación de Q/tensión AC de forma independiente (desacoplada).
5. Verifica rizado de \( v_{dc} \) bajo perturbaciones de potencia.

## Ejemplo de código
```python
def matching_angle(vdc, theta, k_match, dt):
    theta += k_match * vdc * dt     # angulo directo del bus DC
    return theta % (2*3.14159)

def matching_C_for_H(H_sec, Sn_VA, Vdc0_V, omega0=314.16):
    """Calcula C [F] para emular la inercia H [s]."""
    k = omega0 / Vdc0_V
    return 2 * H_sec * Sn_VA / (Vdc0_V**2)

# Ejemplo: H=4s, Sn=1 MVA, Vdc0=700V -> C = 16.3 mF
C = matching_C_for_H(4.0, 1e6, 700.0)
```

## Parámetros y valores típicos
\( k_{match} \) tal que \( \Delta v_{dc}\approx1\text{–}5\,\% \) de \( V_{dc0} \) corresponda a
\( \Delta\omega/\omega_0\approx0.5\text{–}2\,\% \). Inercia equivalente según la constante \( H \)
deseada.

## Errores comunes
- Ignorar que el bus DC no está regulado: incompatible con cargas que necesitan tensión DC estable.
- Confundir con PSC: el PSC regula \( P \) directamente; el matching deja que la física haga la
  sincronización sin lazo explícito de potencia.
- Dimensionar \( C \) solo por rizado de tensión y olvidar la inercia resultante.
- Confundir la inercia del matching (del condensador del bus, milisegundos) con el soporte de frecuencia de la batería (segundos a minutos): son fenómenos distintos.

## Conceptos relacionados
- [[grid-forming-vs-following]] · [[vsm-inercia]] · [[power-synchronization-control]] · [[dinamica-bus-dc]] · [[ecuacion-oscilacion]]

## Referencias
- Arghir, Jouini, Dörfler, *Grid-Forming Control for Power Converters based on Matching*, Automatica 2018.
- Dörfler et al., *Taming Instabilities in Power Grid Networks*, Physica D 2016.
