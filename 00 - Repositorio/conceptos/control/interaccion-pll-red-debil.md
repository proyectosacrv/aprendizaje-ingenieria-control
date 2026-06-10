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
fecha_actualizacion: 2026-06-08
relacionados: [pll-srf, no-pasividad-resistencia-negativa, impedancia-salida-estabilidad, grid-forming-vs-following, red-thevenin-scr]
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
impedancia, la PLL hace \( \mathrm{Re}\{Z\}<0 \) (ver [[no-pasividad-resistencia-negativa]]) y al
cruzarse con la red inductiva se viola el Nyquist (ver [[impedancia-salida-estabilidad]]).

Es el **espejo** del grid-forming: el GFL se inestabiliza en red DÉBIL; el GFM (con control
agresivo) en red FUERTE.

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
- [[pll-srf]] · [[no-pasividad-resistencia-negativa]] · [[impedancia-salida-estabilidad]] · [[grid-forming-vs-following]] · [[red-thevenin-scr]]

## Referencias
- Dong et al., *Analysis of PLL Low-Frequency Stability in DG*, IEEE TIE 2015.
