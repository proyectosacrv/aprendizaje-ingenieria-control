---
titulo: Robustez paramétrica (barridos, peor caso, Monte Carlo)
slug: robustez-parametrica
categoria: metodologia
tipo: metodo
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance, 03-DataCenter-IA]
objetivos: [comprobar que el control aguanta la variacion de la planta]
tags: [robustez, barrido, monte-carlo, peor-caso, SCR, sensibilidad-parametrica]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [margenes-estabilidad, niveles-validacion, impedancia-salida-estabilidad, analisis-modal]
referencias:
  - "Skogestad, Postlethwaite, Multivariable Feedback Control, Wiley 2005"
---

## Definición
Evaluación de cómo cambia la estabilidad y el desempeño cuando los parámetros de la planta o del
punto de operación varían dentro de su rango realista (no solo en el valor nominal).

## Fundamento teórico
- **Barrido** (sweep) de un parámetro clave (p.ej. SCR de la red, potencia, temperatura) y
  observación de \( \max\mathrm{Re}(\lambda) \), \( \zeta \), márgenes → curvas de estabilidad y
  valores **críticos**.
- **Peor caso**: identificar la combinación de parámetros más desfavorable (vértices del rango si
  la dependencia es monótona).
- **Monte Carlo**: muestreo aleatorio del espacio de parámetros → distribución de la métrica y
  probabilidad de cumplir especificaciones (útil con tolerancias de componentes).
- Conecta con el control robusto ([[control-robusto-hinf]]) y con el análisis de impedancia
  ([[impedancia-salida-estabilidad]]) cuando la incertidumbre es la red.

<div class="cfig"><img src="figuras/robustez-parametrica-barrido.png" alt="barrido de SCR mostrando el valor critico de estabilidad"><div class="cap">Barriendo un parámetro incierto (aquí la SCR de la red) y observando $\max\mathrm{Re}(\lambda)$ se localiza el valor crítico donde el sistema cruza a inestable. En el GFM el cruce está en $SCR\approx3.35$: es inestable en red fuerte. El valor nominal puede ser estable y el rango real no, por eso nunca se valida solo en el punto nominal.</div></div>

## 1 — Sensibilidad paramétrica en lazo abierto y en lazo cerrado
**Paso 1 — lazo abierto.** Sea la salida \( y=G(p)\,u \) donde \( p \) es un parámetro incierto (p.ej. la inductancia \( L \) o el SCR). La sensibilidad de la salida a una variación \( \delta p \) es directa:

$$ \delta y = \frac{\partial G}{\partial p}\cdot u\cdot\delta p $$

No hay ningún mecanismo que la atenúe: si \( G \) cambia un 10 %, la salida cambia un 10 % también.

**Paso 2 — lazo cerrado.** Con realimentación unitaria y controlador \( C \), la función de transferencia es \( T=GC/(1+GC) \). Una variación \( \delta G \) produce, tras linearizar:

$$ \delta y = \frac{\partial T}{\partial G}\cdot\delta G\cdot r = \frac{C}{(1+GC)^2}\cdot\delta G\cdot r $$

La **función de sensibilidad** \( S=1/(1+L) \) (con \( L=GC \)) aparece al factor:

$$ \frac{\delta y/y}{\delta G/G}=\frac{1}{1+L(j\omega)}=S(j\omega) $$

**Paso 3 — reducción por el factor \( S \).** Si \( |L|\gg1 \) en la banda de interés, \( S\approx 1/L\ll1 \): la misma variación paramétrica produce una perturbación en la salida reducida en un factor \( 1/(1+L) \) respecto al lazo abierto. Por eso la realimentación mejora la robustez paramétrica: su efecto se ve en el barrido de la planta vs la respuesta del lazo cerrado.

$$ \boxed{S_G^y = \frac{\delta y/y}{\delta G/G}\bigg|_{LC} = \frac{1}{1+L(j\omega)}} $$

**Comprobación con el SCR crítico del GFM:** al reducir el SCR (aumentar \( Z_{red} \)) la ganancia del lazo equivalente sube; \( |L| \) en la banda del droop disminuye → \( S\to1 \), la robustez se pierde y el sistema se acerca al cruce de estabilidad (SCR crítico ≈ 3.35).

## Cuándo y por qué se usa
Siempre antes de dar por bueno un diseño: el valor nominal puede ser estable y el rango real no.
Es lo que reveló los SCR críticos de GFM/GFL.

## Procedimiento (genérico)
1. Lista los parámetros inciertos y su rango (componentes ±tolerancia, SCR, punto de operación).
2. Barre los más influyentes; localiza valores críticos por bisección.
3. Para varios a la vez: peor caso (vértices) o Monte Carlo.
4. Reporta el margen al peor caso y, si no cumple, rediseña (o usa control robusto).

## Ejemplo de código
```python
import numpy as np
scr = np.linspace(1, 12, 40)
maxre = [np.linalg.eigvals(A_coupled(s)).real.max() for s in scr]
scr_critico = scr[np.argmin(np.abs(maxre))]      # cruce de estabilidad
```

## Parámetros y valores típicos
Barrer SCR (1–20), X/R (1–10), potencia (0–100%), tolerancia de L/C (±10–20%).

## Errores comunes
- Validar solo en el punto nominal (el error más común y peligroso).
- Asumir peor caso en los vértices cuando la dependencia no es monótona (usar Monte Carlo).

## Uso en proyectos
- **01 (GFM)**: barrido de SCR → crítico ≈3.35 (inestable en red fuerte).
- **02 (GFL)**: barrido de SCR y de ancho de banda de la PLL → crítico ≈3.48 (inestable en red débil).

## Conceptos relacionados
- [[margenes-estabilidad]] · [[impedancia-salida-estabilidad]] · [[niveles-validacion]] · [[analisis-modal]]

## Referencias
- Skogestad, Postlethwaite, *Multivariable Feedback Control*, 2005.
