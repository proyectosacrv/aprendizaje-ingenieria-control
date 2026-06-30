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

## Errores comunes
- Aplicar \( P=\frac{V_1V_2}{X}\sin\delta \) en distribución (R no despreciable) → reparto P/Q erróneo.
- Despreciar la \( C \) shunt en cables largos → se pierden resonancias y el efecto Ferranti.
- Olvidar \( \pm\omega L \) en el modelo dq → lazos de corriente mal desacoplados.
- Mezclar magnitudes de fase y de línea al pasar a pu.

## Conceptos relacionados
- [[transferencia-potencia-linea]] · [[red-thevenin-scr]] · [[impedancia-reactancia]] · [[droop-control]] · [[marco-dq]]

## Referencias
- Kundur, 1994.
- Yazdani, Iravani, 2010.
