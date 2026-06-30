---
titulo: Transferencia de potencia en una línea (P-δ, Q-V)
slug: transferencia-potencia-linea
categoria: fisica-modelado
tipo: concepto
nivel: basico
proyectos: [01-GFM-Impedance]
objetivos: [fundamento del droop y de la rigidez sincronizante del grid-forming]
tags: [flujo-potencia, angulo, p-delta, q-v, basico]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-06-30
relacionados: [droop-control, generador-sincrono, ecuacion-oscilacion, impedancia-virtual, grid-forming-vs-following]
referencias:
  - "Kundur, Power System Stability and Control, McGraw-Hill"
---

## Definición
Describe cuánta potencia activa y reactiva fluye entre dos nudos conectados por una impedancia, en
función de la **diferencia de ángulo** y de las **tensiones**. Es el fundamento del reparto de carga
por droop y de la sincronización de máquinas y grid-forming.

## Fundamento teórico
Para dos tensiones \( V\angle\delta \) y \( E\angle 0 \) unidas por una reactancia \( X \) (línea
predominantemente inductiva), la potencia transmitida es:
$$ P = \frac{V E}{X}\sin\delta, \qquad Q = \frac{V(V - E\cos\delta)}{X} $$
Dos lecturas clave:
- La **activa** depende sobre todo del **ángulo** \( \delta \); la **reactiva** de la **diferencia de
  módulos** \( V-E \). De ahí el droop \( P\text{–}f \) (ajustar \( \delta \) vía frecuencia) y
  \( Q\text{–}V \) (ajustar \( |V| \)).
- Para \( \delta \) pequeño, \( P \approx \dfrac{VE}{X}\,\delta \), y la **rigidez sincronizante** es
$$ \frac{\partial P}{\partial \delta}\bigg|_{\delta\to 0} \approx \frac{VE}{X} $$
Si \( X \) es **pequeña** (red fuerte o poca reactancia de acoplamiento), \( \partial P/\partial\delta \)
es **enorme**: el lazo de potencia se vuelve muy sensible y difícil de estabilizar. Esta es,
exactamente, la razón por la que el grid-forming añade **impedancia virtual** (aumentar \( X \)).

<div class="cfig"><img src="figuras/transferencia-potencia-linea-pdelta.png" alt="curva P-delta"><div class="cap">La potencia transmitida crece con sen δ (máxima a 90°). Cerca de δ=0 es casi lineal: la pendiente ∂P/∂δ=VE/X es la rigidez sincronizante; con X pequeña se dispara y el lazo de potencia se vuelve difícil de estabilizar.</div></div>

## 1 — De dónde sale \( P=\dfrac{VE}{X}\sin\delta \)
**Paso 1 — la corriente por la reactancia.** Entre el nudo emisor \( \bar V=V\angle\delta \) y el receptor \( \bar E=E\angle0 \) hay solo una reactancia \( jX \) (línea inductiva pura, \( R=0 \)). Por la ley de Ohm fasorial:

$$ \bar I=\frac{\bar V-\bar E}{jX}=\frac{V\angle\delta-E\angle0}{jX} $$

**Paso 2 — potencia compleja que sale del nudo \( V \).** Usando \( \bar S=\bar V\,\bar I^{*} \) (conjugado, ver [[potencia-ac-fasores]]). Conjugar \( \bar I \) cambia el signo de su parte imaginaria; como \( (jX)^{*}=-jX \):

$$ \bar S=\bar V\,\bar I^{*}=V\angle\delta\cdot\left(\frac{V\angle\delta-E\angle0}{jX}\right)^{*}=V\angle\delta\cdot\frac{V\angle{-\delta}-E\angle0}{-jX} $$

**Paso 3 — multiplicar el numerador.** Distribuyendo \( V\angle\delta \):

$$ \bar S=\frac{V^2\angle0-VE\angle\delta}{-jX}=\frac{V^2-VE(\cos\delta+j\sin\delta)}{-jX} $$

**Paso 4 — racionalizar el \( -jX \).** Multiplicar arriba y abajo por \( j \) (porque \( \tfrac{1}{-j}=j \)):

$$ \bar S=\frac{j\big[V^2-VE\cos\delta-jVE\sin\delta\big]}{X}=\frac{VE\sin\delta}{X}+j\,\frac{V^2-VE\cos\delta}{X} $$

(el término \( -j\cdot j=+1 \) pasa a la parte real, y el resto queda imaginario).

**Paso 5 — separar P y Q.** Con \( \bar S=P+jQ \):

$$ \boxed{\;P=\frac{VE}{X}\sin\delta,\qquad Q=\frac{V(V-E\cos\delta)}{X}\;} $$

El \( \sin\delta \) sale del término cruzado \( VE\angle\delta \) al proyectarlo sobre el eje imaginario tras racionalizar — por eso **la activa la gobierna el ángulo**. La reactiva contiene \( V-E\cos\delta\approx V-E \) para \( \delta \) pequeño, así que **la gobierna la diferencia de módulos**. Esto justifica el droop \( P\text{–}f \) (mover \( \delta \) vía frecuencia) y \( Q\text{–}V \) (mover \( |V| \)). Comprobado numéricamente: \( P \) y \( Q \) de \( \bar V\bar I^{*} \) coinciden con estas fórmulas para \( \delta=0{,}1; 0{,}5; 1{,}0 \) rad.

## 2 — La rigidez sincronizante \( \partial P/\partial\delta \)
**Paso 1 — derivar \( P(\delta) \).** De \( P=\tfrac{VE}{X}\sin\delta \), tratando \( V,E,X \) como constantes:

$$ \frac{\partial P}{\partial\delta}=\frac{VE}{X}\cos\delta $$

**Paso 2 — evaluar en el punto de operación.** En torno a \( \delta\to0 \) (operación normal, pocos grados), \( \cos\delta\to1 \):

$$ \boxed{\;\frac{\partial P}{\partial\delta}\bigg|_{\delta\to0}=\frac{VE}{X}\;} $$

Es la pendiente de la curva P-δ en el origen: la "constante de muelle" que devuelve la máquina al sincronismo. Con \( X \) **pequeña** (red fuerte) la pendiente se dispara y el lazo de potencia se vuelve agresivo; por eso el grid-forming añade [[impedancia-virtual]] para aumentar \( X \) y bajar esta rigidez. En el proyecto 01 dio \( \approx 127 \) kW/rad.

## Cuándo y por qué se usa
En el reparto de carga (droop), en la estabilidad de ángulo de máquinas síncronas, y en el diseño del
lazo de sincronización del grid-forming. La derivación \( \partial P/\partial\delta \) del proyecto 01
sale de aquí.

## Procedimiento de diseño (genérico)
1. Identifica \( V \), \( E \), \( X \) y el ángulo de operación \( \delta_0 \).
2. Calcula \( P(\delta) \) y la rigidez \( \partial P/\partial\delta \) en el punto.
3. Si la rigidez es excesiva (X pequeña), añade reactancia (física o virtual) para recuperar margen.

## Ejemplo de código
```python
import numpy as np
V, E, X = 326.6, 326.6, 0.5
delta = np.linspace(0, np.pi/2, 100)
P = 1.5*V*E/X*np.sin(delta)          # factor 1.5 por convenio trifasico de pico
dPdd = 1.5*V*E/X                      # rigidez sincronizante en delta=0
```

## Parámetros y valores típicos
El ángulo de operación es pequeño (unos pocos grados; 5.1° en el proyecto 01). La reactancia de
acoplamiento total (filtro + virtual + red) determina la rigidez; la virtual se ajusta a
\( X_v \approx 0.1\text{–}0.2 \) pu.

## Errores comunes
- Aplicar las fórmulas P-δ / Q-V a una línea **resistiva**: el acoplamiento se invierte (entonces P
  depende de \( V \) y Q de \( \delta \)).
- Olvidar que \( X \) pequeña \( \Rightarrow \) lazo de potencia agresivo e inestable.
- Confundir el ángulo de potencia \( \delta \) con la fase instantánea de la tensión.

## Uso en proyectos
- **01 - GFM-Impedance:** la rigidez \( \partial P/\partial\delta \approx 127 \) kW/rad explica la
  inestabilidad del primer diseño; la inductancia virtual la reduce y estabiliza el lazo de potencia.

## Conceptos relacionados
- [[droop-control]] · [[generador-sincrono]] · [[ecuacion-oscilacion]] · [[impedancia-virtual]] · [[grid-forming-vs-following]]

## Referencias
- Kundur, *Power System Stability and Control*.
