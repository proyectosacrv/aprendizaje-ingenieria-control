---
titulo: Modelo de línea (π, RL) y relación X/R
slug: modelo-linea-distribucion
categoria: fisica-modelado
tipo: modelo
nivel: intermedio
proyectos: []
objetivos: [modelar la impedancia entre convertidor y red, justificar el droop P-f/Q-V]
tags: [linea, pi, rl, impedancia, x-r, distribucion, transmision, dq, modelado]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-06-30
relacionados: [transferencia-potencia-linea, red-thevenin-scr, impedancia-reactancia, droop-control, marco-dq, sistema-por-unidad]
referencias:
  - "Kundur, Power System Stability and Control, McGraw-Hill 1994"
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
---

## Definición
Representación de un tramo de línea/cable como **impedancia serie** \( Z=R+j\omega L \) y, si es largo,
**admitancia shunt** \( Y=j\omega C \) repartida en un esquema **π**. Es el elemento que une el
convertidor con el resto de la red y fija cuánta potencia fluye y cómo se acoplan \( P \) y \( Q \).

## Fundamento teórico
**Línea corta** (distribución, < 80 km): solo serie \( Z=R+j X \), \( X=\omega L \). **Media/larga**:
modelo π con la mitad de \( C \) en cada extremo. En el marco síncrono [[marco-dq|dq]], el tramo serie RL es:
$$ L\frac{di_{d}}{dt}=v_{1d}-v_{2d}-R\,i_d+\omega L\,i_q,\qquad
   L\frac{di_{q}}{dt}=v_{1q}-v_{2q}-R\,i_q-\omega L\,i_d $$
con el **acoplamiento cruzado** \( \pm\omega L \) entre ejes. La transferencia de potencia entre dos nudos
(ver [[transferencia-potencia-linea]]) depende de la relación **X/R**:
$$ P\approx\frac{V_1 V_2}{X}\sin\delta,\qquad Q\approx\frac{V_1(V_1-V_2\cos\delta)}{X} $$
válido **solo si \( X\gg R \)**. La relación \( X/R \) decide qué controla qué:

| Nivel | X/R típico | Acoplamiento dominante |
|---|---|---|
| Transmisión (AT) | 5–20 | \( P\!\leftrightarrow\!\delta \), \( Q\!\leftrightarrow\!V \) (droop clásico) |
| Distribución (MT/BT) | 0.3–2 | \( P \) y \( Q \) **acoplados** (R no despreciable) |

<div class="cfig"><img src="figuras/modelo-linea-distribucion-pi.png" alt="modelo pi de linea con impedancia serie RL y capacidad shunt"><div class="cap">Modelo π de un tramo de línea/cable: impedancia serie $Z=R+j\omega L$ y capacidad shunt $C/2$ en cada extremo (solo necesaria en líneas largas/cables). La relación $X/R$ decide el acoplamiento: con $X\gg R$ (transmisión) $P\leftrightarrow\delta$ y $Q\leftrightarrow V$ se desacoplan y vale el droop clásico; en distribución ($X/R\sim1$) $P$ y $Q$ quedan acoplados.</div></div>

## 1 — De dónde sale el acoplamiento cruzado \( \pm\omega L \) en dq
**Paso 1 — la ley del tramo RL en abc.** Por fase, la tensión sobre el tramo serie es la caída resistiva más la inductiva (vector espacial \( \vec{x}=x_d+jx_q \) en marco **estacionario** \( \alpha\beta \)):

$$ \vec{v}_1-\vec{v}_2=R\,\vec{i}+L\frac{d\vec{i}}{dt} $$

**Paso 2 — pasar al marco giratorio.** El marco dq gira a \( \omega \): un vector estacionario \( \vec{i}^{s} \) se relaciona con el del marco giratorio \( \vec{i} \) por \( \vec{i}^{s}=\vec{i}\,e^{j\omega t} \). Sustituyendo y derivando el producto:

$$ \frac{d\vec{i}^{s}}{dt}=\frac{d}{dt}\big(\vec{i}\,e^{j\omega t}\big)=\left(\frac{d\vec{i}}{dt}+j\omega\,\vec{i}\right)e^{j\omega t} $$

El término extra \( j\omega\,\vec{i} \) aparece **solo** por derivar dentro de un marco que gira (regla del producto): es el origen del acoplamiento.

**Paso 3 — escribir la ecuación en dq.** Sustituyendo todo (\( \vec{v}=\vec{v}\,e^{j\omega t} \)) y cancelando el factor común \( e^{j\omega t} \):

$$ \vec{v}_1-\vec{v}_2=R\,\vec{i}+L\left(\frac{d\vec{i}}{dt}+j\omega\,\vec{i}\right)\quad\Longrightarrow\quad L\frac{d\vec{i}}{dt}=\vec{v}_1-\vec{v}_2-R\,\vec{i}-j\omega L\,\vec{i} $$

**Paso 4 — separar parte real (d) e imaginaria (q).** Con \( \vec{i}=i_d+ji_q \), el término \( -j\omega L\,\vec{i}=-j\omega L(i_d+ji_q)=\omega L\,i_q-j\omega L\,i_d \). Igualando componente real y componente imaginaria:

$$ \boxed{\;L\frac{di_d}{dt}=v_{1d}-v_{2d}-R\,i_d+\omega L\,i_q,\qquad
   L\frac{di_q}{dt}=v_{1q}-v_{2q}-R\,i_q-\omega L\,i_d\;} $$

El \( +\omega L\,i_q \) en la ecuación de d y el \( -\omega L\,i_d \) en la de q son el **acoplamiento cruzado**: el eje q empuja al d y viceversa, con signos opuestos. No es un artificio de modelado — nace literalmente del \( j\omega \) de derivar en un marco giratorio (Paso 2). Por eso el lazo de corriente añade términos de **desacoplo** \( \mp\omega L\,i_{q,d} \) en la referencia, para cancelarlos. El mismo \( \omega L_g \) aparece en la red ([[red-thevenin-scr]]) y en el [[filtro-lcl]].

## 3 — Los parámetros de la línea: \( R', L', C', G' \) por unidad de longitud

**Paso 1 — el modelo de línea de transmisión.** Una línea real es un sistema de parámetros distribuidos: en cada diferencial de longitud \( dz \), hay una resistencia \( R'\,dz \), una inductancia \( L'\,dz \), una conductancia shunt \( G'\,dz \) y una capacidad shunt \( C'\,dz \). Las ecuaciones del telegrafista en el dominio de la frecuencia son:

$$ \frac{dV}{dz}=-(R'+j\omega L')\,I,\qquad\frac{dI}{dz}=-(G'+j\omega C')\,V $$

**Paso 2 — constante de propagación e impedancia característica.** Combinando las dos ecuaciones:

$$ \gamma=\sqrt{(R'+j\omega L')(G'+j\omega C')}\quad\text{[1/m]} $$

$$ Z_c=\sqrt{\frac{R'+j\omega L'}{G'+j\omega C'}}\quad\text{[Ω]} $$

A alta frecuencia (\( \omega L'\gg R' \), \( \omega C'\gg G' \)): \( \gamma\approx j\omega\sqrt{L'C'} \) (puramente propagativo) y \( Z_c\approx\sqrt{L'/C'} \) (real, sin pérdidas).

**Paso 3 — parámetros típicos de MT.** Para una línea aérea de 20 kV:

| Parámetro | Valor típico |
|---|---|
| \( R' \) | 0.3 Ω/km |
| \( L' \) | 1 mH/km (\( X'=0.314\,\Omega/\text{km} \) a 50 Hz) |
| \( C' \) | 10 nF/km (\( B'=3.14\,\mu\text{S/km} \) a 50 Hz) |
| \( G' \) | ≈ 0 (despreciable en líneas aéreas) |
| \( X/R \) | 0.3–2 (distribución MT) |

Para un **cable subterráneo** de 20 kV: \( R'\approx0.2\,\Omega/\text{km} \), \( L'\approx0.35\,\text{mH/km} \), pero \( C'\approx200\,\text{nF/km} \) — ×20 más que la línea aérea, lo que hace relevante el efecto Ferranti y la resonancia serie en cables de decenas de km.

**Paso 4 — la impedancia característica a 50 Hz.** Para la línea aérea MT:

$$ Z_c\approx\sqrt{\frac{L'}{C'}}=\sqrt{\frac{10^{-3}}{10^{-8}}}=\sqrt{10^5}=316\,\Omega $$

Es del orden de centenares de ohmios para líneas aéreas. La potencia natural de la línea (\( P_n=V^2/Z_c \)) a 20 kV: \( P_n=20000^2/316\approx1.27\,\text{MW} \). Por encima de \( P_n \) la línea consume reactiva (inductiva); por debajo la genera.

## 4 — El modelo \( \pi \) y el modelo exacto de parámetros distribuidos

**Paso 1 — el modelo π para líneas cortas.** Para longitudes \( l<80\,\text{km} \) a 50 Hz, la distribución de parámetros puede concentrarse: la impedancia serie total \( Z=Z'l \) y la admitancia shunt total \( Y=Y'l \) se reparten simétricamente. En el modelo π:

- **Impedancia serie:** \( Z_{serie}=(R'+j\omega L')\,l \) centrada en la línea.
- **Admitancias shunt:** \( Y_{shunt}/2=j\omega C'\,l/2 \) en cada extremo.

La ecuación de la corriente en el emisor: \( I_E=I_R+V_R\cdot Y_{shunt}/2 \) (corriente de carga + corriente shunt del receptor); la tensión en el emisor: \( V_E=V_R+I_R\cdot Z_{serie} \).

**Paso 2 — el modelo exacto para líneas largas.** Para longitudes > 80 km (o cables largos de MT), la solución exacta de las ecuaciones del telegrafista da:

$$ \boxed{Z_{serie,exacto}=Z_c\,\sinh(\gamma l),\qquad Y_{shunt,exacto}=\frac{1}{Z_c}\,\tanh\!\left(\frac{\gamma l}{2}\right)} $$

Estas expresiones reemplazan \( Z_{serie}=Z'l \) y \( Y_{shunt}/2=Y'l/2 \) del modelo π. Para \( l\to0 \): \( \sinh(\gamma l)\approx\gamma l \), recuperando el modelo π. El error del modelo π respecto al exacto crece con la frecuencia y la longitud.

**Paso 3 — comparación numérica.** Línea aérea 100 km, \( R'=0.1\,\Omega/\text{km} \), \( L'=1\,\text{mH/km} \):

| Frecuencia | \( |Z_{π}| \) | \( |Z_{exacto}| \) | Error |
|---|---|---|---|
| 50 Hz | 32.1 Ω | 31.8 Ω | 0.9 % |
| 500 Hz | 314 Ω | 296 Ω | 6 % |
| 1 kHz | 628 Ω | 541 Ω | 16 % |

A 50 Hz el modelo π es suficiente; a alta frecuencia (para EMC o ferroresonancia), hay que usar el modelo distribuido.

## 5 — La caída de tensión y la regulación de la línea

**Paso 1 — la caída de tensión aproximada.** En una red con ángulo pequeño (\( \delta\ll1 \)), la variación de módulo de tensión entre emisor \( V_1 \) y receptor \( V_2 \) es:

$$ \Delta V=V_1-|V_2|\approx\frac{P\,R+Q\,X}{V_1} $$

donde \( P \) y \( Q \) son la potencia activa y reactiva en la carga, \( R \) y \( X \) las impedancias totales de la línea. Esta expresión es exacta para redes puramente resistivas (\( X=0 \)) o puramente inductivas (\( R=0 \)).

**Paso 2 — contribuciones de \( P \) y \( Q \).** El término \( P\,R \) domina en distribución donde \( R \) es significativo; el término \( Q\,X \) domina en transmisión donde \( X\gg R \). En distribución urbana con \( X/R\approx0.5 \): ambos términos son comparables → tanto inyectar potencia reactiva como reducir la carga activa ayuda a regular la tensión.

**Paso 3 — el perfil de tensión con cargas repartidas.** Si la línea tiene \( n \) cargas uniformemente repartidas, la caída de tensión máxima (en el extremo) es la mitad que con la misma carga concentrada en el extremo:

$$ \Delta V_{repartida}=\frac{1}{2}\,\Delta V_{concentrada} $$

Esto justifica usar alimentadores con cargas repartidas en lugar de derivaciones largas con carga concentrada al final.

**Paso 4 — la regulación de tensión.** La regulación es:

$$ \varepsilon=\frac{V_{vacío}-V_{carga}}{V_{carga}}\approx\frac{\Delta V}{V_2}=\frac{P\,R+Q\,X}{V_2^2} $$

Para la distribución (20 kV, 10 km, \( R=3\,\Omega \), \( X=4\,\Omega \), carga 3 MVA a FP=0.85 lag): \( P=2.55\,\text{MW} \), \( Q=1.58\,\text{MVAr} \), \( V_2\approx V_{nom}=11.55\,\text{kV} \) (fase):

$$ \Delta V=\frac{2.55\times10^6\times3+1.58\times10^6\times4}{11550}=\frac{7.65\times10^6+6.32\times10^6}{11550}=\frac{13.97\times10^6}{11550}=1210\,\text{V} $$

$$ \varepsilon=\frac{1210}{11550}=10.5\,\% $$

Supera el límite típico del ±5 %. Se necesita regulador de tensión o inyección de reactiva.

## 6 — Diseño iterativo: línea de 10 km, 20 kV, 3 MVA

**Datos.** \( l=10\,\text{km} \), \( V_{LL}=20\,\text{kV} \), \( S=3\,\text{MVA} \), \( FP=0.85\,\text{lag} \), \( R'=0.3\,\Omega/\text{km} \), \( X'=0.4\,\Omega/\text{km} \), \( C'=10\,\text{nF/km} \).

**Paso 1 — parámetros totales.**

$$ R=0.3\times10=3\,\Omega,\quad X=0.4\times10=4\,\Omega,\quad C_{shunt}=10\times10^{-9}\times10=100\,\text{nF} $$

$$ |Z|=\sqrt{3^2+4^2}=5\,\Omega,\quad X/R=4/3=1.33\quad\text{(distribución: P y Q acoplados)} $$

**Paso 2 — corrientes y potencias.**

$$ I_L=\frac{S}{\sqrt3\,V_{LL}}=\frac{3\times10^6}{\sqrt3\times20000}=86.6\,\text{A} $$

$$ P=S\cos\varphi=3\times10^6\times0.85=2.55\,\text{MW},\quad Q=S\sin\varphi=3\times10^6\times0.527=1.58\,\text{MVAr} $$

**Paso 3 — caída de tensión con modelo π.**

$$ \Delta V_{fase}=\frac{P\,R+Q\,X}{V_{fase}}=\frac{2.55\times10^6\times3+1.58\times10^6\times4}{11547}=\frac{7.65+6.32}{11.547}\times\frac{10^6}{10^3}=1210\,\text{V} $$

$$ \varepsilon=\frac{1210}{11547}=10.5\,\%\quad\text{(fuera del ±5\%)} $$

**Paso 4 — comparación con el modelo distribuido.** Para esta longitud (10 km) y frecuencia (50 Hz), la diferencia entre modelo π y distribuido es despreciable (<1 %). La constante eléctrica de la línea:

$$ \lambda_e=\frac{1}{\omega\sqrt{L'C'}}=\frac{1}{2\pi\times50\times\sqrt{10^{-3}\times10^{-8}}}=\frac{1}{314\times10^{-5.5}}=1007\,\text{km} $$

La longitud de 10 km representa solo \( l/\lambda_e\approx1\,\% \) de la longitud de onda eléctrica: el modelo π es completamente adecuado.

**Paso 5 — corrección con banco de condensadores.** Para reducir \( Q \) de 1.58 MVAr a 0:

$$ C_{banco}=\frac{Q}{\omega V_{LL}^2}=\frac{1.58\times10^6}{2\pi\times50\times(20000)^2}=\frac{1.58\times10^6}{1.257\times10^8}=12.6\,\mu\text{F (trifásico)} $$

Con el banco: \( \Delta V=P\,R/V_{fase}=2.55\times10^6\times3/11547=662\,\text{V} \), \( \varepsilon=5.7\,\% \). Aún supera el ±5 %. Habría que agregar regulación de tensión adicional o reducir la longitud del alimentador (subdivisiónde la red).

<div class="cfig"><img src="figuras/modelo-linea-distribucion-analisis.png" alt="perfil de tensión, modelo π vs distribuido, ΔV vs Q y capacidad de transporte"><div class="cap">Panel (a): perfil de tensión a lo largo de la línea de 10 km para cargas de 1, 2 y 3 MW a FP=0.85 — la caída supera el ±5% a plena carga. Panel (b): comparativa del modelo π vs parámetros distribuidos: el error es pequeño a 50 Hz pero crece a alta frecuencia. Panel (c): caída de tensión ΔV vs Q inyectada — la compensación reactiva puede reducir ΔV pero no la elimina del todo cuando R es significativa. Panel (d): potencia máxima transportable vs longitud de línea: el límite térmico domina en líneas cortas, la caída de tensión en líneas largas.</div></div>

## Cuándo y por qué se usa
Para dimensionar lazos de corriente (la \( L \) es la planta del lazo), calcular la [[red-thevenin-scr|SCR]]
del punto de conexión, justificar el [[droop-control|droop]] P-f/Q-V (válido con \( X/R \) alto) y explicar
por qué en redes de **distribución** el droop clásico falla y se necesita droop con transformación o
virtual-impedance. También define la impedancia de red \( Z_g \) en el análisis de estabilidad por impedancia.

## Procedimiento de diseño (genérico)
1. Clasifica la línea (corta/media/larga) → elige RL serie o π completo.
2. Obtén \( R,L,C \) por unidad de longitud (tablas del conductor) y multiplica por la longitud; pásalo a
   [[sistema-por-unidad|pu]].
3. Calcula \( X/R \) para decidir si \( P\!-\!\delta \)/\( Q\!-\!V \) están desacoplados.
4. En dq, incluye los términos \( \pm\omega L \) en el modelo de estado.
5. Para estabilidad, combina \( Z_{linea} \) con la \( Z_{th} \) de la red ([[red-thevenin-scr]]).

## Ejemplo de aplicación real
**Problema:** cable de MT de 10 km, \( R'=0.16\,\Omega/\text{km} \), \( L'=0.35\,\text{mH/km} \),
red de 20 kV, 50 Hz. ¿X/R y SCR de un parque de 5 MW conectado en su extremo?

\( R=1.6\,\Omega \), \( X=\omega L=2\pi 50\times3.5\,\text{mH}=1.10\,\Omega \) →
\( X/R\approx0.69 \): **distribución, P y Q acoplados** (el droop clásico no sirve sin compensar R).
Potencia de cortocircuito \( S_{cc}=V^2/|Z|=20000^2/\sqrt{1.6^2+1.10^2}=4\times10^8/1.94\approx206\,\text{MVA} \)
(despreciando la red aguas arriba). SCR \( =S_{cc}/S_{nom}=206/5\approx41 \): red **fuerte**. Si el cable
fuese de 80 km, \( |Z|\approx15.5\,\Omega \), \( S_{cc}\approx26\,\text{MVA} \), SCR\( \approx5 \): ya débil.

## Ejemplo de código
```python
import numpy as np
def linea_rl_dq(i, v1, v2, R, L, w):
    # i, v1, v2 = vectores [d, q]; devuelve di/dt en dq con acoplamiento +-wL
    did = (v1[0]-v2[0]-R*i[0]+w*L*i[1])/L
    diq = (v1[1]-v2[1]-R*i[1]-w*L*i[0])/L
    return np.array([did, diq])
```

## Parámetros y valores típicos
Líneas aéreas AT: \( X/R\sim10 \). Cables MT: \( X/R\sim0.5\text{–}1 \) (R alto, mucha \( C \)).
\( L'\approx0.3\text{–}1\,\text{mH/km} \), \( C'\approx0.1\text{–}0.3\,\mu\text{F/km} \) (más en cable).
Regla: usar π cuando \( \omega C \) del tramo no es despreciable frente a la carga (líneas largas/cables).

## 7 — Modelo π: aplicación a redes de distribución y media tensión

El modelo \(\pi\) lumped concentra la impedancia serie en el centro y la admitancia shunt en los dos extremos:

$$Z_{serie} = (R'+j\omega L')\ell, \qquad Y_{shunt}/2 = j\omega C'\ell/2 \quad \text{en cada extremo}$$

Para líneas aéreas de distribución de 20 kV, 10 km: \(R'\approx0.3\,\Omega/\text{km}\), \(L'\approx1\,\text{mH/km}\), \(C'\approx10\,\text{nF/km}\). La admitancia shunt a 50 Hz representa solo \(j\pi\,\text{mS}\) total — despreciable para \(\ell<30\,\text{km}\). Para cables de media tensión, \(C'\approx200\,\text{nF/km}\) → el shunt ya importa a 5 km.

El modelo en cascada (varios segmentos π en serie) permite representar líneas largas sin resolver la ecuación de onda; con 5–10 segmentos el error < 1% hasta la frecuencia de resonancia del cable.

<div class="cfig"><img src="../figuras/modelo-linea-distribucion-analisis.png" alt="Análisis de línea de distribución: modelo π, perfil de tensión, cargabilidad y efecto Ferranti"><div class="cap">(a) Modelo π con parámetros típicos aérea vs cable. (b) Perfil de tensión a lo largo de la línea a distintas cargas. (c) Diagrama de cargabilidad: límite térmico, límite de estabilidad y SIL. (d) Efecto Ferranti: sobretensión en vacío vs longitud de línea.</div></div>

## 8 — Caída de tensión y cargabilidad

La caída de tensión aproximada (pequeño ángulo):

$$\Delta V \approx \frac{PR + QX}{V}$$

Para maximizar la transferencia de potencia activa en distribución (R dominante) conviene minimizar \(Q\) mediante compensación local. El límite térmico se alcanza cuando la corriente supera la capacidad del conductor (tipicamente 200–500 A para cables de 240 mm²).

El límite de estabilidad de ángulo se alcanza cuando \(\delta = 90°\) (\(P = P_{max} = V_1 V_2/X\)); en distribución de baja \(X/R\) el límite térmico llega antes.

**SIL (Surge Impedance Loading):** \(P_{SIL} = V^2/Z_c\), con \(Z_c = \sqrt{L'/C'}\). Para líneas aéreas de 400 kV, \(Z_c\approx300\,\Omega\), \(P_{SIL}\approx500\,\text{MW}\). En la carga SIL, el perfil de tensión es plano y no hay flujo de reactiva.

## 9 — Efecto Ferranti en líneas largas y cables

En una línea de longitud \(\ell\) sin carga, la corriente capacitiva shunt crea una caída de tensión inductiva que eleva la tensión en el extremo receptor:

$$V_{receptor} \approx V_{emisor}\cdot\cos(\beta\ell)^{-1} \approx V_{emisor}\left(1 + \frac{(\omega\ell)^2 L'C'}{2}\right)$$

Para líneas aéreas de 400 kV y \(\ell=300\,\text{km}\): sobretensión \(\approx8\%\).
Para cables submarinos (HVDC DC AC, \(C'=200\,\text{nF/km}\)): la sobretensión aparece ya a \(\ell=50\,\text{km}\).

**Compensación:** reactor shunt en el extremo receptor de valor \(Q_L = \omega C'\ell V^2\) absorbe la corriente capacitiva y elimina la sobretensión.

## 10 — Cables submarinos vs líneas aéreas: limitaciones de longitud AC

| Parámetro | Línea aérea 400 kV | Cable submarino 400 kV |
|---|---|---|
| \(C'\) [nF/km] | 10–15 | 150–250 |
| \(L'\) [mH/km] | 1.0–1.3 | 0.3–0.5 |
| \(Z_c\) [\(\Omega\)] | 280–340 | 30–50 |
| \(v_p/c\) | \(\approx1.0\) | \(\approx0.4\) |
| Longitud máx. AC | > 500 km | 50–80 km |

La alta capacidad del cable limita la longitud útil AC: más de ~80 km toda la corriente de la línea se gasta en cargar el cable y no llega potencia activa al receptor. Por eso los cables de alta mar > 100 km usan HVDC con conversión AC/DC en los extremos (tecnología VSC-HVDC).

La velocidad de propagación en cables \(v_p = 1/\sqrt{L'C'}\approx 0.35\,c\) también reduce la frecuencia de resonancia capacitiva, importante para el análisis de transitorios de conmutación en redes de distribución.

## 11 — Impedancia de secuencia y desequilibrios de fase

En redes trifásicas desequilibradas o con faltas, la teoría de componentes simétricas descompone las corrientes en secuencias positiva, negativa y cero. Las impedancias de la línea son distintas para cada secuencia:

$$Z_1 = R_1 + j\omega L_1 \quad\text{(secuencia positiva, ≈ Z de la línea normal)}$$
$$Z_2 = Z_1 \quad\text{(líneas transposadas: secuencia negativa = positiva)}$$
$$Z_0 = R_0 + j\omega L_0 \quad\text{(secuencia cero: R_0≈3R_1, L_0≈3L_1 si el retorno es por tierra)}$$

Para líneas no transpostas, \(Z_1\neq Z_2\) y aparece acoplamiento entre secuencias (desequilibrio estructural de la línea). En cables con pantalla, la impedancia de cero depende de si la pantalla está aterrada en uno o ambos extremos.

**Aplicación al análisis de faltas.** La corriente de falta monofásica a tierra es \(I_f=3V_{fase}/(Z_1+Z_2+Z_0)\). En líneas con alta impedancia de cero (redes en triángulo sin neutro), \(Z_0\to\infty\) y la falta monofásica no produce corriente: es el fundamento de las redes IT (redes aisladas de tierra) en hospitales y procesos continuos.

## 12 — Regulación de tensión en distribución activa: aporte de DER

Los DER (Distributed Energy Resources) conectados en la red de distribución modifican el perfil de tensión de forma favorable o desfavorable según su control:

**Inversor FV en PQ (sin control Q):** solo inyecta potencia activa. En MT con \(R/X\approx1\), la caída de tensión \(\Delta V\approx PR/V\) se reduce, mejorando la tensión en el punto de conexión. Con muchos FV, puede producir sobretensión en el extremo de la línea durante horas de alta generación y baja carga.

**Inversor FV con control Q-V (Volt-Var):** el inversor ajusta su potencia reactiva en función de la tensión local \(Q=f(V_{PCC})\). Cuando \(V_{PCC}>1.05\,\text{pu}\) absorbe reactiva (lagging); cuando \(V_{PCC}<0.95\,\text{pu}\) inyecta reactiva (leading). Esto amortigua las variaciones de tensión sin necesidad de reguladores mecánicos.

**Límite de penetración FV.** La penetración máxima de FV sin regulación Q en una red de distribución típica de 20 kV, 10 km es aproximadamente el 30–40 % de la potencia de cortocircuito del punto de conexión. Por encima, la sobretensión en horas de máxima generación supera el ±10 % del valor nominal.

## 13 — Flujo de potencia en redes malladas vs radiales

Las redes de distribución son mayoritariamente radiales (árbol): un único camino desde la subestación hasta cada carga. Esto simplifica el cálculo del flujo: la potencia fluye en un solo sentido y la caída de tensión se acumula desde el nudo cabecera hasta el extremo.

**Flujo radial.** Barrido hacia adelante/atrás (Forward-Backward Sweep): calcular las corrientes de carga en cada nudo, sumar hacia la cabecera para obtener las corrientes de línea, y luego calcular las tensiones de nudo empezando por la cabecera con voltaje conocido.

**Redes malladas** (transmisión): la potencia puede fluir por múltiples caminos. El flujo se calcula mediante el método de Newton-Raphson en las ecuaciones de potencia nodal \(P=\text{Re}(\mathbf{V}\mathbf{I}^*)\), \(Q=\text{Im}(\mathbf{V}\mathbf{I}^*)\). La admitancia nodal \(\mathbf{Y}_{bus}\) codifica la topología: \(Y_{ii}=\sum_k 1/Z_{ik}\) (diagonal), \(Y_{ij}=-1/Z_{ij}\) (fuera de diagonal).

**Impacto de DER en redes radiales.** Un generador DER en el extremo de la línea invierte el flujo de potencia en condiciones de alta generación y baja carga. Las protecciones diseñadas para flujo unidireccional (relés de sobreintensidad direccional) pueden no detectar la falta o disparar errónea­mente. Se necesita reubicar o actualizar las protecciones para flujo bidireccional.

## 14 — La línea en el modelo dq del control: impacto en el lazo de corriente

Cuando el convertidor está conectado a la red a través de un cable largo, la inductancia del cable \(L_g\) se suma a la inductancia del filtro \(L_2\) del LCL en el lazo de corriente. Esto afecta a la planta vista por el controlador de corriente:

$$G_{corriente}(s) = \frac{1}{s(L_2+L_g) + (R_2+R_g)}$$

Si \(L_g\) varía con la longitud del cable (p.ej. en parques con alimentadores de longitud variable), la ganancia de cruce del lazo de corriente cambia, alterando el margen de fase. Regla: re-sintonizar el lazo de corriente si \(L_g>0.5L_2\).

Además, en el modelo dq, el acoplamiento cruzado cambia de \(\pm\omega L_2\) a \(\pm\omega(L_2+L_g)\). Si el feedforward de desacoplamiento usa \(L_{2,nominal}\) y la red real tiene \(L_g\neq0\), el desacoplamiento es imperfecto y quedan residuos cruzados del orden de \(\omega L_g/(\omega(L_2+L_g))\).

## 15 — Parámetros de cable subterráneo vs línea aérea a 20 kV

| Parámetro | Línea aérea 20 kV | Cable subterráneo 20 kV |
|---|---|---|
| \(R'\) [Ω/km] | 0.2–0.4 | 0.1–0.2 |
| \(L'\) [mH/km] | 0.8–1.2 | 0.25–0.45 |
| \(C'\) [nF/km] | 8–12 | 150–300 |
| \(X/R\) | 1–4 | 0.3–1.5 |
| Ferranti (50 km) | <0.1 % | 2–5 % |
| Long. max. AC útil | > 500 km | 30–80 km |

El cable subterráneo tiene una capacidad 20–30× mayor que la línea aérea. Esto:
1. Hace necesario el modelo π incluso para longitudes de 5–10 km.
2. Genera corriente capacitiva reactiva que reduce la potencia activa transportable.
3. Eleva la tensión en vacío (efecto Ferranti) para longitudes >30 km.
4. Reduce la impedancia característica a \(Z_c=\sqrt{L'/C'}\approx35\,\Omega\) (vs ≈300 Ω en línea aérea), lo que significa que el SIL de un cable de 33 kV es solo \(33^2/35\approx31\,\text{MW}\).

## 16 — Compensación serie: condensadores en serie con la línea

En líneas largas de transmisión, los condensadores en serie compensan parte de la reactancia inductiva de la línea, aumentando la potencia transportable:

$$X_{eff} = X_L - X_C = \omega L\ell - \frac{1}{\omega C_{serie}}$$

El **grado de compensación** \(\alpha = X_C/X_L\) (típicamente 30–70 %). Con \(\alpha=50\%\), la potencia máxima transferible se duplica:

$$P_{max,comp} = \frac{V_1 V_2}{X_{eff}} = \frac{V_1 V_2}{(1-\alpha)X_L} = \frac{P_{max,sin}}{1-\alpha} = 2P_{max,sin}$$

**Riesgo de ferroresonancia y subsincronismo.** La resonancia serie del condensador con la inductancia de la máquina síncrona puede producir oscilaciones subsíncronas (Subsynchronous Resonance, SSR) en la frecuencia:

$$f_{SSR} = f_0\sqrt{\alpha\cdot X_L/X_{tot}} < f_0$$

El fenómeno SSR puede excitar modos mecánicos de la turbina-generador y producir daños estructurales. La detección y protección SSR es un requisito en líneas con compensación serie > 40 %.

## 17 — Droop virtual y resistencia virtual para distribución de X/R bajo

En redes de distribución con \(X/R\approx1\), el droop P-f/Q-V clásico no funciona correctamente porque \(P\) y \(Q\) están acoplados. La solución es el **droop con resistencia virtual** (virtual impedance droop):

$$\begin{pmatrix}P_{ref}\\\delta_{ref}\end{pmatrix} = \begin{pmatrix}\cos\theta & \sin\theta \\ -\sin\theta & \cos\theta\end{pmatrix}\begin{pmatrix}P_{med}\\Q_{med}\end{pmatrix}\cdot\begin{pmatrix}1/m_p\\1/m_q\end{pmatrix}$$

donde \(\theta=\arctan(R/X)\) es el ángulo de impedancia de la línea. Esta rotación desacopla el control en la base de la línea (en vez de la base dq clásica), de forma que el droop opera sobre las variables \(P'\) y \(Q'\) que sí están desacopladas en esa base.

**Implementación simplificada.** Se añade una impedancia virtual \(Z_{virt}=R_{virt}+jX_{virt}\) tal que la impedancia total (línea + virtual) tenga \(X/R\) alto (>5), restaurando la validez del droop clásico. Se elige \(X_{virt}\) para que \((X_{linea}+X_{virt})/(R_{linea}+R_{virt})\geq5\).

## Errores comunes
- Aplicar \( P=\frac{V_1V_2}{X}\sin\delta \) en distribución (R no despreciable) → reparto P/Q erróneo.
- Despreciar la \( C \) shunt en cables largos → se pierden resonancias y el efecto Ferranti.
- Olvidar \( \pm\omega L \) en el modelo dq → lazos de corriente mal desacoplados.
- Mezclar magnitudes de fase y de línea al pasar a pu.

## 18 — Pérdidas en líneas de distribución: eficiencia energética

Las pérdidas Joule en una línea de distribución cargada al \(x\%\) de su capacidad nominal:

$$P_{loss} = 3\,R\,I_L^2 = 3\,R\,\left(\frac{x\,S_n}{\sqrt{3}\,V_{LL}}\right)^2 = \frac{x^2\,S_n^2\,R}{V_{LL}^2}$$

**Eficiencia de la línea.** La fracción de la potencia entregada que se pierde en la línea:

$$\varepsilon_{loss} = \frac{P_{loss}}{P_{entregada}} = \frac{x\,S_n\,R}{V_{LL}^2}\cdot x = x^2\cdot\frac{S_n\,R}{V_{LL}^2}$$

Para la línea del diseño iterativo (R=3Ω, V=20 kV, S=3 MVA a x=100%): \(\varepsilon_{loss}=1\times\frac{3\times10^6\times3}{(20\times10^3)^2}=\frac{9\times10^6}{4\times10^8}=2.25\%\). A carga media (x=50%): \(\varepsilon_{loss}=0.25\times2.25\%=0.56\%\).

**Estrategia para reducir pérdidas.** Operar las líneas de MT a mayor tensión (33 kV en vez de 20 kV) reduce las pérdidas en un factor \((20/33)^2\approx0.37\), es decir, a menos del 40 % del valor original con la misma potencia y la misma longitud. Esta es la justificación técnica de la tendencia a subir los niveles de tensión en distribución conforme aumenta la penetración de renovables (y la potencia por alimentador).

## 19 — Impacto de la longitud de la línea en el SCR del punto de conexión

Para un parque renovable conectado al final de una línea de distribución, el SCR efectivo en el PCC depende directamente de la impedancia de la línea:

$$Z_{red,total} = Z_{red,grid} + Z_{linea}$$

$$\text{SCR}_{PCC} = \frac{V_{LL}^2}{|Z_{red,total}|\cdot P_n}$$

A medida que la línea es más larga, \(|Z_{linea}|\) aumenta y el SCR cae. Para un parque de 5 MW en una red de 20 kV con \(Z_{grid}\) equivalente a SCR=50:

| Longitud [km] | \(|Z_{linea}|\) [Ω] | \(|Z_{red,total}|\) [Ω] | SCR |
|---|---|---|---|
| 0 | 0 | 8 | 50 |
| 5 | 2.5 | 10.5 | 38 |
| 20 | 10 | 18 | 22 |
| 50 | 25 | 33 | 12 |
| 80 | 40 | 48 | 8.3 |

Con 80 km de línea el SCR ya ha caído a 8 — todavía fuerte, pero si la red aguas arriba es más débil (SCR=10 en lugar de 50), el SCR efectivo a 80 km podría ser 3 o menos, requiriendo GFM en lugar de GFL.

## Conceptos relacionados
- [[transferencia-potencia-linea]] · [[red-thevenin-scr]] · [[impedancia-reactancia]] · [[droop-control]] · [[marco-dq]]

## Referencias
- Kundur, 1994.
- Yazdani, Iravani, 2010.
