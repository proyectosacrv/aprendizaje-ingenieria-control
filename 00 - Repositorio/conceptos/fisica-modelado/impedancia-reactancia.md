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
fecha_actualizacion: 2026-06-10
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
