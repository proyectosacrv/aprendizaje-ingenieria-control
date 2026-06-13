---
titulo: Gain scheduling (ganancias programadas)
slug: gain-scheduling
categoria: control
tipo: tecnica
nivel: avanzado
proyectos: []
objetivos: [adaptar el controlador al punto de operación en plantas no lineales o de parámetros variables]
tags: [gain-scheduling, no-lineal, punto-operacion, lpv, adaptacion, scr-variable, control]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-06-10
relacionados: [linealizacion-teoria, asignacion-polos-lqr, sintonia-pi-pid, robustez-parametrica, interaccion-pll-red-debil, control-robusto-hinf]
referencias:
  - "Rugh, Shamma, Research on gain scheduling, Automatica 2000"
  - "Åström, Wittenmark, Adaptive Control, Addison-Wesley 1995"
---

## Definición
Estrategia para plantas **no lineales o de parámetros variables**: se diseñan varios controladores
lineales en distintos **puntos de operación** y sus ganancias se **interpolan** en función de una variable
medible (la *variable de scheduling*). Equivale a un controlador cuyos parámetros cambian con el régimen.

## Fundamento teórico
La planta no lineal \( \dot x=f(x,u) \) se **[[linealizacion-teoria|lineariza]]** en una rejilla de puntos
de equilibrio \( \{x_i^\*,u_i^\*\} \) parametrizados por la variable de scheduling \( \rho \) (carga,
tensión, velocidad, SCR…). En cada punto se sintoniza un controlador \( K(\rho_i) \) y se programa:
$$ u=u^\*(\rho)+K(\rho)\,\big(x-x^\*(\rho)\big),\qquad K(\rho)=\text{interp}\big(K(\rho_i)\big) $$
Garantías y advertencias:
- Si \( \rho \) varía **lentamente** frente a la dinámica del lazo, la estabilidad local en cada punto se
  traslada al sistema global (principio cuasi-estacionario). Regla práctica: *"schedule slowly"*.
- Si \( \rho \) varía **rápido**, aparecen términos de variación \( \dot\rho \) no capturados → puede
  desestabilizar aunque cada punto sea estable. La formulación **LPV** (Linear Parameter-Varying) trata
  \( \rho \) explícitamente y da garantías globales.
- Conviene programar sobre **variables internas de la planta** (no sobre la salida del propio lazo) para no
  crear realimentaciones ocultas.

Es el puente entre el control lineal de un punto ([[sintonia-pi-pid]], [[asignacion-polos-lqr]]) y un
funcionamiento robusto en **todo el rango**, sin recurrir necesariamente a [[control-robusto-hinf|H∞]] de
peor caso (que sacrifica desempeño por robustez).

<div class="cfig"><img src="figuras/gain-scheduling-scr.png" alt="ganancia de lazo con Kp fijo y con Kp programado segun SCR"><div class="cap">Con un $K_p$ fijo sintonizado en red fuerte, la ganancia de lazo $K_pX_g$ (con $X_g\propto1/$SCR) se dispara al debilitarse la red y cruza el umbral de inestabilidad. Programando $K_p$ proporcional a la SCR estimada, el producto $K_pX_g$ se mantiene constante y el margen se conserva en todo el rango.</div></div>

## Cuándo y por qué se usa
Cuando un único juego de ganancias no sirve en todo el rango: aerogenerador con punto de operación variable
(MPPT, pitch), convertidor cuya planta depende de la **SCR de red** ([[interaccion-pll-red-debil]]: PLL
agresiva sirve en red fuerte pero inestabiliza en débil), \( V_{dc} \) variable que cambia la ganancia del
modulador, control de motor por velocidad. Alternativa pragmática al control robusto cuando el peor caso
sería demasiado conservador.

## Procedimiento de diseño (genérico)
1. Elige la **variable de scheduling** \( \rho \): medible, lenta, que capture la no linealidad.
2. Define la rejilla de puntos de operación que cubre el rango esperado.
3. Lineariza en cada punto y sintoniza \( K(\rho_i) \) con el método que prefieras.
4. Interpola entre puntos (lineal, tabla, o parametriza \( K \) en función de \( \rho \)).
5. Verifica la transición: barridos de \( \rho \) a la **velocidad real** (no solo en cada punto fijo) y
   comprobar estabilidad; si \( \dot\rho \) importa, pasa a diseño LPV.

## Ejemplo de aplicación real
**Problema:** un [[grid-forming-vs-following|GFL]] con PLL debe operar con SCR entre 10 (fuerte) y 2 (débil).
La planta del lazo de potencia escala \( \approx X_g\propto1/\text{SCR} \). Si se sintoniza el PI a SCR=10,
¿qué pasa a SCR=2 y cómo lo resuelve el scheduling?

A SCR=10 la \( X_g \) es pequeña y se elige un PI rápido. Al bajar a SCR=2, \( X_g \) se multiplica por 5:
la ganancia de lazo \( \approx K_p X_g \) sube ×5, el margen de fase se desploma y el sistema oscila o se
inestabiliza ([[interaccion-pll-red-debil]]). **Scheduling sobre la SCR estimada** (vía impedancia de red
estimada): se baja \( K_p \) proporcionalmente a la SCR de modo que \( K_p X_g\approx \) cte, manteniendo el
margen de fase en todo el rango. La SCR cambia en segundos (mucho más lento que el lazo de ms) → la hipótesis
cuasi-estacionaria se cumple y la interpolación es segura.

## Ejemplo de código
```python
import numpy as np
def scheduled_kp(scr, scr_grid, kp_grid):
    # interpola Kp en funcion de la SCR estimada (variable de scheduling)
    return float(np.interp(scr, scr_grid, kp_grid))
# scr_grid=[2,5,10], kp_grid=[0.2,0.5,1.0] -> Kp baja en red debil
```

## Parámetros y valores típicos
Nº de puntos de la rejilla: 3–7 por variable. Separación temporal de escalas: \( \rho \) al menos 5–10×
más lento que el lazo. Interpolación: lineal o spline suave (evitar saltos de ganancia).

## Errores comunes
- Programar sobre la **salida del propio lazo** → realimentación oculta que puede inestabilizar.
- Suponer que "estable en cada punto" implica "estable en transición": falso si \( \dot\rho \) es grande.
- Rejilla demasiado dispersa → huecos donde ninguna sintonía es buena.
- Saltos bruscos de ganancia entre puntos → transitorios de conmutación; interpola suave.

## Conceptos relacionados
- [[linealizacion-teoria]] · [[asignacion-polos-lqr]] · [[sintonia-pi-pid]] · [[robustez-parametrica]] · [[interaccion-pll-red-debil]] · [[control-robusto-hinf]]

## Referencias
- Rugh, Shamma, *Research on gain scheduling*, Automatica 2000.
- Åström, Wittenmark, *Adaptive Control*, 1995.
