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
fecha_actualizacion: 2026-06-30
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

## 1 — De dónde salen \( P=VI\cos\varphi \) y \( Q=VI\sin\varphi \)
**Paso 1 — partir de la potencia compleja.** Define los fasores **eficaces** \( \bar V=V\,e^{j\theta_v} \), \( \bar I=I\,e^{j\theta_i} \). La potencia compleja se define con el conjugado de la corriente (así el ángulo resultante es el desfase \( \varphi=\theta_v-\theta_i \), no la suma):

$$ \bar S=\bar V\,\bar I^{*}=\big(V\,e^{j\theta_v}\big)\big(I\,e^{-j\theta_i}\big)=VI\,e^{j(\theta_v-\theta_i)}=VI\,e^{j\varphi} $$

**Paso 2 — pasar a forma binómica.** Con la fórmula de Euler \( e^{j\varphi}=\cos\varphi+j\sin\varphi \):

$$ \bar S=VI\cos\varphi+j\,VI\sin\varphi $$

**Paso 3 — identificar partes real e imaginaria.** Por definición \( \bar S=P+jQ \). Igualando componente a componente:

$$ \boxed{\;P=\mathrm{Re}\,\bar S=VI\cos\varphi,\qquad Q=\mathrm{Im}\,\bar S=VI\sin\varphi\;} $$

y el módulo \( S=|\bar S|=VI=\sqrt{P^2+Q^2} \) es la hipotenusa del triángulo de la figura. El **factor de potencia** es \( \cos\varphi=P/S \): la fracción de la aparente que hace trabajo. El uso del conjugado garantiza el signo correcto de \( Q \): carga inductiva (corriente retrasada, \( \theta_i<\theta_v \), \( \varphi>0 \)) da \( Q>0 \).

## 2 — Por qué la media de \( v(t)\,i(t) \) coincide con \( VI\cos\varphi \)
**Paso 1 — potencia instantánea.** Con \( v=\sqrt2\,V\cos\omega t \) e \( i=\sqrt2\,I\cos(\omega t-\varphi) \) (amplitud de pico \( =\sqrt2\times \) RMS):

$$ p(t)=v\,i=2VI\cos\omega t\,\cos(\omega t-\varphi) $$

**Paso 2 — producto de cosenos a suma.** Con \( \cos A\cos B=\tfrac12[\cos(A-B)+\cos(A+B)] \):

$$ p(t)=2VI\cdot\frac12\big[\cos\varphi+\cos(2\omega t-\varphi)\big]=\underbrace{VI\cos\varphi}_{\text{media}}+\underbrace{VI\cos(2\omega t-\varphi)}_{\text{pulsa a }2\omega} $$

**Paso 3 — promediar.** El término \( \cos(2\omega t-\varphi) \) promedia cero sobre un periodo; queda \( \langle p\rangle=VI\cos\varphi=P \). Esto reconcilia la definición fasorial del apartado 1 con la potencia instantánea: el \( 2 \) del pico cancela el \( \tfrac12 \) del producto de cosenos. (En trifásico equilibrado las tres pulsaciones de \( 2\omega \) se cancelan entre sí y la potencia total es constante: ver [[sistema-trifasico]] y [[potencia-instantanea-dq]].)

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
