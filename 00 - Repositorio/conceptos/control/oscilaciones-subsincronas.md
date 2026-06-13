---
titulo: Oscilaciones subsíncronas (SSO / SSCI)
slug: oscilaciones-subsincronas
categoria: control
tipo: fenomeno
nivel: avanzado
proyectos: []
objetivos: [entender y mitigar oscilaciones por interacción convertidor-compensación serie]
tags: [sso, ssci, ssr, compensacion-serie, subsincrono, eolica, avanzado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-09
relacionados: [estabilidad-armonica, clasificacion-estabilidad, interaccion-pll-red-debil, impedancia-salida-estabilidad, red-thevenin-scr]
referencias:
  - "IEEE SSR Working Group, Terms, Definitions and Symbols for Subsynchronous Oscillations, IEEE 1985"
  - "Irwin et al., Sub-synchronous control interactions between Type-3 wind turbines and series compensated transmission, IEEE PES 2011"
---

## Definición
Oscilaciones de frecuencia **inferior a la fundamental** (típ. 5–100 Hz) que se amplifican por la
interacción entre convertidores (o generadores) y elementos de red, sobre todo **líneas con
compensación serie**. La variante moderna sin partes mecánicas es la **SSCI** (subsynchronous
control interaction), propia de eólica Tipo-3/4.

## Fundamento teórico
Una línea con condensador serie \( C_s \) y reactancia \( X_L \) resuena a
$$ f_n=f_1\sqrt{\frac{X_{C_s}}{X_L}}<f_1 $$
A esa frecuencia subsíncrona, la red presenta baja impedancia. Tres mecanismos clásicos (SSR):
- **IGE** (induction generator effect): a \( f_n \) la resistencia equivalente del generador es
  **negativa** → autoexcitación eléctrica.
- **TI** (torsional interaction): \( f_n \) excita modos torsionales del eje turbina-generador.
- **TA** (transient torque): pares de eje grandes tras faltas.

**SSCI:** no hay modo mecánico; es puramente **control–red**. El control del convertidor (lazo de
corriente, PLL) presenta a frecuencias subsíncronas una **resistencia negativa** que, combinada con
la resonancia serie, da amortiguamiento neto negativo. Es rápida (puede crecer en ciclos) y depende
fuertemente del nivel de compensación y del [[red-thevenin-scr|SCR]]. Se analiza con el modelo de
[[impedancia-salida-estabilidad|impedancia]]: la inestabilidad aparece donde
\( \mathrm{Re}\{Z_{conv}+Z_{red}\}<0 \) cerca de \( f_n \).

<div class="cfig"><img src="figuras/oscilaciones-subsincronas-resonancia.png" alt="frecuencia de resonancia serie y oscilacion subsincrona creciente"><div class="cap">Izquierda: una línea con compensación serie resuena a $f_n=f_1\sqrt{X_{Cs}/X_L}$, que cae en la banda subsíncrona (≈10–45 Hz). Derecha: si el convertidor presenta resistencia negativa cerca de $f_n$, el amortiguamiento neto es negativo y la oscilación (SSCI) crece en pocos ciclos, sin necesidad de modos mecánicos.</div></div>

## Cuándo y por qué se usa
En parques eólicos conectados por líneas compensadas serie (causa de eventos reales, p.ej. ERCOT
2009), en HVDC y en redes débiles con alta penetración de convertidores. Es una subclase
"resonancia" de la [[clasificacion-estabilidad|clasificación de estabilidad]].

## Procedimiento de diseño (genérico)
1. Identifica resonancias serie de la red \( f_n \) según el nivel de compensación.
2. Modela la impedancia del convertidor a frecuencias subsíncronas (incluye control y PLL).
3. Busca resistencia negativa neta cerca de \( f_n \) (criterio de impedancia).
4. Mitiga: ajustar banda de PLL/lazo de corriente, **damping subsíncrono** dedicado (SSDC), filtros
   o impedancia virtual; a nivel red, TCSC/bypass del condensador.
5. Valida con barrido del nivel de compensación y SCR ([[barrido-parametrico]]).

## Ejemplo de código
```python
import numpy as np
def series_resonance(f1, XL, XCs):       # frecuencia subsincrona de red
    return f1*np.sqrt(XCs/XL)
# inestable si Re{Z_conv(fn)+Z_red(fn)} < 0
```

## Parámetros y valores típicos
Compensación serie 20–75 % → \( f_n\approx 10\text{–}45 \) Hz. SSCI puede crecer en 0.1–1 s. Modos
torsionales 10–50 Hz.

## Errores comunes
- Suponer que sin masas rotativas no hay riesgo subsíncrono (la SSCI es de control).
- Modelar el convertidor solo a la fundamental (no captura la resistencia negativa subsíncrona).
- Diseñar la PLL solo por respuesta nominal, sin ver su efecto en impedancia subsíncrona.

## Conceptos relacionados
- [[estabilidad-armonica]] · [[clasificacion-estabilidad]] · [[interaccion-pll-red-debil]] · [[impedancia-salida-estabilidad]] · [[red-thevenin-scr]]

## Referencias
- IEEE SSR WG, *Terms, Definitions and Symbols for Subsynchronous Oscillations*, 1985.
- Irwin et al., *Sub-synchronous control interactions ... series compensated transmission*, IEEE PES 2011.
