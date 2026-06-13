---
titulo: Potencia en AC y fasores (P, Q, S)
slug: potencia-ac-fasores
categoria: fisica-modelado
tipo: concepto
nivel: basico
proyectos: []
objetivos: [entender potencia activa, reactiva y aparente, y el uso de fasores]
tags: [potencia, activa, reactiva, aparente, fasores, RMS, basico]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-12
relacionados: [potencia-instantanea-dq, marco-dq, droop-control]
referencias:
  - "Irwin, Análisis Básico de Circuitos en Ingeniería"
---

## Definición
En corriente alterna senoidal, la potencia se descompone en **activa** \( P \) (la que hace
trabajo útil, en W), **reactiva** \( Q \) (la que oscila entre fuente y campos, en var) y
**aparente** \( S \) (el producto de tensión y corriente eficaces, en VA). Los **fasores**
representan magnitudes senoidales como números complejos para operar con ellas fácilmente.

## Fundamento teórico
Un fasor codifica amplitud y fase: \( v(t)=\hat V\cos(\omega t+\theta)\to \bar V=\tfrac{\hat V}{\sqrt2}\,e^{j\theta} \)
(valor **eficaz/RMS** \( =\hat V/\sqrt2 \)). Con tensión y corriente eficaces \( V, I \) y desfase
\( \varphi \) entre ellas:
$$ P = VI\cos\varphi, \qquad Q = VI\sin\varphi, \qquad S = VI = \sqrt{P^2+Q^2} $$
La **potencia compleja** es \( \bar S = \bar V\,\bar I^{*} = P + jQ \). El **factor de potencia**
es \( \cos\varphi = P/S \). Una carga inductiva absorbe \( Q>0 \); una capacitiva, \( Q<0 \).
En trifásico equilibrado, \( P=3\,V_{fase}I_{fase}\cos\varphi=\sqrt3\,V_{LL}I_L\cos\varphi \).

<div class="cfig"><img src="figuras/potencia-ac-fasores-triangulo.png" alt="triangulo de potencia"><div class="cap">Triángulo de potencia: la activa P y la reactiva Q son los catetos, la aparente S la hipotenusa, y el factor de potencia es cos φ = P/S.</div></div>

## Cuándo y por qué se usa
Es la base del análisis de sistemas de potencia: dimensionar equipos (por \( S \)), compensar
reactiva, y formular el control (el droop reparte \( P \) y \( Q \); ver
[[potencia-instantanea-dq]] para la versión instantánea en dq).

## Procedimiento (genérico)
1. Expresa tensiones y corrientes como fasores (eficaces).
2. Calcula \( \bar S=\bar V\bar I^{*} \); separa \( P=\mathrm{Re}\,\bar S \), \( Q=\mathrm{Im}\,\bar S \).
3. Obtén \( S=|\bar S| \) y el factor de potencia \( P/S \).
4. Para trifásico, multiplica por 3 (por fase) o usa la fórmula de línea.

## Ejemplo de aplicación real
**Problema:** Carga industrial trifásica de \( P=10\,\text{kW} \), \( \cos\phi=0.85\,\text{retraso} \), \( V_{LL}=400\,\text{V} \). Calcular la corriente de línea y la capacitancia de compensación para elevar el fp a 0.98.

Corriente: \( I=P/(\sqrt{3}\,V_{LL}\cos\phi)=10000/(\sqrt{3}\times400\times0.85)\approx17.0\,\text{A} \). Reactiva actual: \( Q_1=P\tan\phi_1=10000\times0.619\approx6190\,\text{VAr} \). Reactiva objetivo: \( Q_2=P\tan(\arccos0.98)\approx2020\,\text{VAr} \). A compensar: \( Q_C=Q_1-Q_2=4170\,\text{VAr} \). Capacitancia (monofásica por fase): \( C=Q_C/(\omega\,V_f^2)=4170/(314\times231^2)\approx249\,\mu\text{F} \). La corriente baja de 17.0 a \( 10000/(\sqrt{3}\times400\times0.98)\approx14.7\,\text{A} \): ahorro del 13 % en pérdidas Joule.

## Ejemplo de código
```python
import numpy as np
V = 230*np.exp(1j*0); I = 10*np.exp(-1j*np.deg2rad(30))   # fasores eficaces
S = V*np.conj(I); P, Q = S.real, S.imag; FP = P/abs(S)
```

## Parámetros y valores típicos
Factor de potencia objetivo cercano a 1. Convenio de signo de \( Q \): positivo = inductivo
(absorbe reactiva).

## Errores comunes
- Mezclar valores de pico y eficaces (RMS) en las fórmulas de potencia.
- Olvidar el factor \( \sqrt3 \) o el 3 en trifásico.

## Conceptos relacionados
- [[potencia-instantanea-dq]] · [[marco-dq]] · [[droop-control]]

## Referencias
- Irwin, *Análisis Básico de Circuitos en Ingeniería*.
