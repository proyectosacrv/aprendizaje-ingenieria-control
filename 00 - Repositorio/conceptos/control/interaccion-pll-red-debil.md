---
titulo: Interacción PLL–red débil (inestabilidad del grid-following)
slug: interaccion-pll-red-debil
categoria: control
tipo: fenomeno
nivel: avanzado
proyectos: [02-GFL-Impedance]
objetivos: [entender y evitar la inestabilidad del GFL en red debil]
tags: [pll, red-debil, SCR, grid-following, oscilaciones, estabilidad]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [pll-srf, impedancia-salida-estabilidad, grid-forming-vs-following, red-thevenin-scr]
referencias:
  - "Dong et al., Analysis of Phase-Locked Loop Low-Frequency Stability in DG, IEEE TIE 2015"
---

## Definición
Inestabilidad característica del inversor grid-following en **red débil** (SCR bajo): la PLL y
la impedancia de red forman un lazo de realimentación positiva que produce oscilaciones de baja
frecuencia.

## Fundamento teórico
La PLL mide la tensión en el PCC para estimar el ángulo. En red débil (alta \( L_g \)), la
**corriente inyectada perturba esa tensión**: al inyectar, cae/gira la tensión del PCC, la PLL
malinterpreta el ángulo y corrige la corriente, que vuelve a perturbar la tensión. Si la PLL es
rápida, esta realimentación se cierra con fase desfavorable → inestable. En términos de
impedancia, la PLL hace \( \mathrm{Re}\{Z\}<0 \) (ver [[impedancia-salida-estabilidad|resistencia negativa]]) y al
cruzarse con la red inductiva se viola el Nyquist (ver [[impedancia-salida-estabilidad]]).

Es el **espejo** del grid-forming: el GFL se inestabiliza en red DÉBIL; el GFM (con control
agresivo) en red FUERTE.

<div class="cfig"><img src="figuras/interaccion-pll-red-debil-mapa.png" alt="SCR critico en funcion del ancho de banda de la PLL"><div class="cap">Mapa de estabilidad del grid-following: cuanto más rápida es la PLL, mayor es el SCR crítico por debajo del cual el sistema oscila, es decir, más amplia la región de red débil inestable. La palanca principal de diseño es reducir el ancho de banda de la PLL.</div></div>

## 1 — Por qué \( \Delta i_d \) perturba \( V_q \) en red débil: la realimentación positiva

**Paso 1 — modelo Thévenin de la red en dq.** La red vista desde el PCC es una fuente \( \mathbf{V}_g \) detrás de \( Z_{red}=R_g+jX_g \). La tensión en el PCC en αβ es:

$$ \mathbf{V}_{PCC} = \mathbf{V}_g - (R_g+jX_g)\,\mathbf{I} $$

**Paso 2 — linealización en el punto de operación.** El control orientado a \( \mathbf{V}_{PCC} \) mantiene \( V_d = V \), \( V_q = 0 \) en equilibrio. Una perturbación pequeña \( \Delta\mathbf{I}=\Delta i_d + j\Delta i_q \) produce una variación en el PCC. Separando partes real (eje d) e imaginaria (eje q) y tomando \( \Delta i_q = 0 \) para aislar el efecto de \( \Delta i_d \):

$$ \Delta V_d = -R_g\,\Delta i_d, \qquad \Delta V_q = -X_g\,\Delta i_d $$

**Paso 3 — por qué importa el signo de \( \Delta V_q \).** La PLL cierra un lazo PI sobre \( V_q \) para forzarla a cero. Una perturbación \( \Delta V_q < 0 \) (producida por \( \Delta i_d > 0 \) con \( X_g > 0 \)) hace que la PLL acelere el ángulo estimado \( \hat\theta \) para "recuperar" \( V_q = 0 \). El nuevo ángulo modifica \( i_d \) en sentido que amplifica \( \Delta i_d \):

$$ \boxed{\Delta V_q \approx -X_g\,\Delta i_d}, \qquad \frac{\partial \hat\omega_{PLL}}{\partial V_q} > 0 $$

**Paso 4 — la ganancia del lazo parásito.** La cadena completa es:

$$ \Delta i_d \xrightarrow{\times(-X_g)} \Delta V_q \xrightarrow{H_{PLL}(s)} \Delta\hat\theta \xrightarrow{\text{lazo corriente}} \Delta i_d $$

La ganancia de lazo en la frecuencia crítica es \( \approx K_{PPLL}\,X_g \). Cuando \( X_g \) crece (red débil, SCR bajo) y \( K_{PPLL} \) es grande (PLL rápida), el producto supera la unidad con fase desfavorable y el lazo se inestabiliza. La condición límite es:

$$ K_{PPLL}\,X_g\big|_{\text{fase}=-180°} = 1 \quad\Rightarrow\quad \text{oscilación sostenida} $$

Esto explica el **mapa de estabilidad**: a \( X_g \) fija, aumentar la PLL lleva antes al límite; a PLL fija, una red más débil (\( X_g \) mayor) cruza el límite con menos margen.

## Cuándo y por qué se usa (cómo se evita)
Aparece en parques PV/eólicos GFL conectados por líneas largas (red débil). Se previene
limitando el ancho de banda de la PLL, con impedance shaping, o migrando a grid-forming.

## Procedimiento de diseño (genérico)
1. Estima el SCR del punto de conexión (ver [[red-thevenin-scr]]).
2. Calcula la impedancia del GFL y verifica el Nyquist de \( Z_{red}Y_{inv} \) en el SCR mínimo.
3. Si hay riesgo: **reduce el ancho de banda de la PLL** (es la palanca principal), añade
   amortiguamiento/impedance shaping, o usa grid-forming.
4. Verifica el SCR crítico vs el ancho de banda de la PLL.

## Ejemplo de código
```python
# barrer SCR y ancho de banda de la PLL -> mapa de estabilidad
for fpll in [40, 60, 100, 150]:
    scr_crit = biseccion(lambda scr: maxre_acoplado(scr, fpll))  # inestable por debajo
```

## Parámetros y valores típicos
PLL lenta (≈30 Hz): robusta hasta SCR≈1. PLL rápida (≈100 Hz): inestable por debajo de
SCR≈3.5. PLL muy rápida (≈170 Hz): inestable hasta SCR≈8 (casi cualquier red).

## Errores comunes
- Acelerar la PLL para "mejorar" el seguimiento sin comprobar la red débil.
- Diseñar con red fuerte y desplegar en red débil sin reevaluar.

## Uso en proyectos
- **02 - GFL-Impedance** (objetivo: entender la inestabilidad): SCR crítico validado por dos
  vías (acoplado 3.48 vs Nyquist 3.55). La curva SCR_crítico(f_pll) muestra que la PLL rápida
  amplía la región débil inestable. Comparación directa con el GFM en `main_compare.py`.

## Conceptos relacionados
- [[pll-srf]] · [[impedancia-salida-estabilidad|resistencia negativa]] · [[grid-forming-vs-following]] · [[red-thevenin-scr]]

## Referencias
- Dong et al., *Analysis of PLL Low-Frequency Stability in DG*, IEEE TIE 2015.
