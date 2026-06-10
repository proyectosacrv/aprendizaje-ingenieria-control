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
fecha_actualizacion: 2026-06-10
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
