---
titulo: Impedancia, reactancia y admitancia
slug: impedancia-reactancia
categoria: fisica-modelado
tipo: concepto
nivel: basico
proyectos: [01-GFM-Impedance, 02-GFL-Impedance, 03-DataCenter-IA]
objetivos: [base del análisis fasorial y del enfoque de impedancia]
tags: [impedancia, reactancia, admitancia, fasores, basico]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-06-30
relacionados: [potencia-ac-fasores, resonancia-rlc, impedancia-salida-estabilidad, red-thevenin-scr, filtro-lcl]
referencias:
  - "Sedra & Smith, Microelectronic Circuits"
---

## Definición
La **impedancia** \( Z \) es la "resistencia" generalizada de un elemento al paso de corriente
alterna: la relación (fasorial) entre tensión y corriente. Tiene parte resistiva \( R \) y parte
**reactiva** \( X \) (la que desfasa). La **admitancia** \( Y = 1/Z \) es su inversa.

## Fundamento teórico
En régimen senoidal, con fasores:
$$ Z = \frac{\hat V}{\hat I} = R + jX, \qquad Y = \frac{1}{Z} = G + jB $$
Para los elementos básicos:
$$ Z_R = R, \qquad Z_L = j\omega L, \qquad Z_C = \frac{1}{j\omega C} = -\frac{j}{\omega C} $$
La reactancia inductiva \( X_L=\omega L \) es positiva (la corriente atrasa); la capacitiva
\( X_C=-1/(\omega C) \) es negativa (la corriente adelanta). El módulo \( |Z|=\sqrt{R^2+X^2} \) y el
ángulo \( \angle Z = \arctan(X/R) \). Se combinan como las resistencias: **serie** suma \( Z \),
**paralelo** suma \( Y \). En sistemas trifásicos en el marco dq, la impedancia ya **no es un escalar
sino una matriz 2×2** por el acoplamiento entre ejes.

<div class="cfig"><img src="figuras/impedancia-reactancia-zf.png" alt="impedancia de R, L y C con la frecuencia"><div class="cap">Las reactancias dependen de la frecuencia: R es plana, la inductiva XL=ωL sube y la capacitiva XC=1/ωC baja. Donde se cruzan L y C aparece la resonancia.</div></div>

## 1 — Por qué \( Z_L=j\omega L \) (la reactancia inductiva \( X_L=\omega L \))
**Paso 1 — la ley física del inductor.** La ley de Faraday para un inductor relaciona tensión y derivada de la corriente:

$$ v(t)=L\frac{di(t)}{dt} $$

**Paso 2 — excitar con una corriente senoidal en forma compleja.** Usamos el fasor giratorio \( i(t)=\hat I\,e^{j\omega t} \) (la senoide real es su parte real). Derivar una exponencial solo la multiplica por \( j\omega \):

$$ \frac{di}{dt}=\frac{d}{dt}\big(\hat I\,e^{j\omega t}\big)=j\omega\,\hat I\,e^{j\omega t}=j\omega\,i(t) $$

**Paso 3 — sustituir en la ley.** Reemplazando:

$$ v(t)=L\cdot j\omega\,i(t)=j\omega L\,i(t) $$

**Paso 4 — tomar el cociente impedancia.** La impedancia es \( Z=v/i \), y \( i(t) \) se cancela:

$$ \boxed{\;Z_L=\frac{v}{i}=j\omega L\quad\Longrightarrow\quad X_L=\omega L\;} $$

La derivada temporal se ha convertido en una multiplicación por \( j\omega \): por eso el análisis fasorial sustituye ecuaciones diferenciales por álgebra. El factor \( j \) significa \( +90° \): la tensión adelanta a la corriente (equivalente: la corriente **atrasa**). \( X_L=\omega L \) crece con la frecuencia — la línea ascendente de la figura.

## 2 — Por qué \( Z_C=\dfrac{1}{j\omega C} \) (la reactancia capacitiva \( X_C=-1/\omega C \))
**Paso 1 — la ley física del condensador.** Ahora la corriente es la derivada de la tensión:

$$ i(t)=C\frac{dv(t)}{dt} $$

**Paso 2 — excitar con tensión senoidal compleja.** Con \( v(t)=\hat V\,e^{j\omega t} \), la derivada multiplica por \( j\omega \):

$$ i(t)=C\cdot j\omega\,v(t)=j\omega C\,v(t) $$

**Paso 3 — despejar la impedancia.** \( Z=v/i \), y \( v(t) \) se cancela:

$$ Z_C=\frac{v}{i}=\frac{1}{j\omega C} $$

**Paso 4 — racionalizar.** Multiplicando arriba y abajo por \( -j \) (con \( -j\cdot j=1 \)):

$$ \boxed{\;Z_C=\frac{1}{j\omega C}=\frac{-j}{\omega C}\quad\Longrightarrow\quad X_C=-\frac{1}{\omega C}\;} $$

El signo \( -j \) significa \( -90° \): la corriente **adelanta** a la tensión, justo lo contrario que en el inductor. Y \( X_C \) **decrece** con la frecuencia — la línea descendente de la figura. Donde \( |X_L|=|X_C| \), es decir \( \omega L=1/\omega C \), se cruzan: es la resonancia \( \omega_0=1/\sqrt{LC} \) (ver [[resonancia-rlc]]).

## Cuándo y por qué se usa
Es el lenguaje de todo el análisis AC: filtros, red Thévenin (\( Z_{red}=R_g+j\omega L_g \)),
resonancias y, sobre todo, el **enfoque de impedancia** para la estabilidad convertidor-red.

## Procedimiento de diseño (genérico)
1. Sustituye cada elemento por su impedancia \( Z(j\omega) \).
2. Combina por topología: serie \( \to \sum Z \); paralelo \( \to (\sum 1/Z)^{-1} \).
3. Evalúa \( |Z| \) y \( \angle Z \) en la banda de interés (o barre la frecuencia, Bode).

## Ejemplo de código
```python
import numpy as np
w = 2*np.pi*np.logspace(0, 4, 500)
ZL = 1j*w*2e-3; ZC = 1/(1j*w*20e-6)        # inductor y condensador
Zserie = 0.1 + ZL + ZC                      # R + L + C en serie
```

## Parámetros y valores típicos
Reactancias en pu: una inductancia de filtro suele ser 0.02–0.1 pu; la impedancia de red varía con el
SCR (\( |Z_{red}| = V_{ll}^2/(\mathrm{SCR}\cdot S_n) \)).

## Errores comunes
- Olvidar el signo negativo de la reactancia capacitiva.
- Confundir \( |Z| \) con \( \mathrm{Re}(Z) \) (la parte real es la que disipa/aporta energía).
- Tratar la impedancia dq como un escalar cuando es una matriz 2×2.

## Conceptos relacionados
- [[potencia-ac-fasores]] · [[resonancia-rlc]] · [[impedancia-salida-estabilidad]] · [[red-thevenin-scr]] · [[filtro-lcl]]

## Referencias
- Sedra & Smith, *Microelectronic Circuits*.
