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
fecha_actualizacion: 2026-06-08
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
