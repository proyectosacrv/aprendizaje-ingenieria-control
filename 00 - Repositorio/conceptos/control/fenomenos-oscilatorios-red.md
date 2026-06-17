---
titulo: Fenómenos oscilatorios de red (armónica y subsíncrona)
slug: fenomenos-oscilatorios-red
categoria: control
tipo: fenomeno
nivel: avanzado
proyectos: []
objetivos: [entender y mitigar las oscilaciones por interacción convertidor-red, tanto subsíncronas como de media-alta frecuencia]
tags: [estabilidad-armonica, oscilaciones-subsincronas, sso, ssci, resonancia, pasividad, resistencia-negativa, multi-convertidor, avanzado]
fecha_creacion: 2026-06-16
fecha_actualizacion: 2026-06-16
relacionados: [impedancia-salida-estabilidad, clasificacion-estabilidad, interaccion-pll-red-debil, filtro-lcl, red-thevenin-scr, compensacion-retardo, filtro-notch]
referencias:
  - "Wang, Blaabjerg, Harmonic Stability in Power-Electronic-Based Power Systems, IEEE TPEL 2014"
  - "Wang et al., Unified Impedance Model of Grid-Connected VSCs, IEEE TPEL 2018"
  - "IEEE SSR Working Group, Terms, Definitions and Symbols for Subsynchronous Oscillations, IEEE 1985"
  - "Irwin et al., Sub-synchronous control interactions between Type-3 wind turbines and series compensated transmission, IEEE PES 2011"
---

## Definición
Familia de inestabilidades oscilatorias que surgen de la interacción entre la impedancia de los convertidores (o generadores) y la de la red, distintas de la estabilidad electromecánica clásica. Se ordenan por banda de frecuencia: las oscilaciones subsíncronas (por debajo de la fundamental, típ. 5–100 Hz) y la resonancia/estabilidad armónica (de media-alta frecuencia, decenas de Hz a kHz). Las dos comparten el mismo mecanismo de fondo —resistencia negativa del control frente a una resonancia de red— y la misma herramienta de análisis (el criterio de impedancia / pasividad), por eso se tratan juntas.

## Mecanismo común (contexto genérico)
Cualquier equipo conectado a la red presenta una impedancia/admitancia de salida Z_o(j·omega) que, por culpa de sus lazos de control, su PLL y su retardo digital, tiene bandas donde se comporta como resistencia negativa (no pasivo): ahí Re{Z_o} < 0. Si esa banda coincide en frecuencia con una resonancia de la red (un paralelo o serie de inductancias y capacidades de cables, filtros o compensación serie), el amortiguamiento neto del lazo formado por ambas impedancias se vuelve negativo y aparece una oscilación sostenida o creciente. El convertidor no necesita ser "el malo": basta con que su no pasividad caiga sobre una resonancia que la red ya tenía. El equipo aguas arriba puede ser un parque eólico, una planta PV, un HVDC o cualquier conjunto de convertidores; el razonamiento es el mismo.

Marco de análisis (común a las dos bandas):
- Pasividad: si Re{Z_o(j·omega)} ≥ 0 para todo omega, el equipo no puede desestabilizar ninguna red pasiva (diseño passivity-based).
- Impedancia: aplicar Nyquist generalizado al cociente Z_o/Z_g (ver [[impedancia-salida-estabilidad]]).
- Multi-convertidor: N equipos en paralelo añaden resonancias y reparto de corriente; el modelo de impedancia unificada agrega sus admitancias.

Causas frecuentes de no pasividad: retardo de cómputo+PWM (del orden de 1.5·Ts), ancho de banda de la PLL, feedforward de tensión de red, y amortiguamiento insuficiente del [[filtro-lcl]].

## Parte 1 — oscilaciones subsíncronas (SSO / SSCI)
Oscilaciones de frecuencia inferior a la fundamental que se amplifican por la interacción entre convertidores (o generadores) y elementos de red, sobre todo líneas con compensación serie. Una línea con condensador serie Cs y reactancia XL resuena a:

fn = f1·raiz(X_Cs / XL) < f1

A esa frecuencia subsíncrona la red presenta baja impedancia. Mecanismos clásicos (SSR, con máquina rotativa):
- IGE (induction generator effect): a fn la resistencia equivalente del generador es negativa → autoexcitación eléctrica.
- TI (torsional interaction): fn excita modos torsionales del eje turbina-generador.
- TA (transient torque): pares de eje grandes tras faltas.

SSCI (subsynchronous control interaction): la variante moderna sin partes mecánicas, propia de eólica Tipo-3/4. Es puramente control-red: el control del convertidor (lazo de corriente, PLL) presenta a frecuencias subsíncronas una resistencia negativa que, combinada con la resonancia serie, da amortiguamiento neto negativo. Es rápida (puede crecer en ciclos) y depende fuertemente del nivel de compensación y del SCR. La inestabilidad aparece donde Re{Z_conv + Z_red} < 0 cerca de fn.

<div class="cfig"><img src="figuras/oscilaciones-subsincronas-resonancia.png" alt="frecuencia de resonancia serie y oscilacion subsincrona creciente"><div class="cap">Izquierda: una línea con compensación serie resuena a fn=f1·raiz(X_Cs/XL), que cae en la banda subsíncrona (≈10–45 Hz). Derecha: si el convertidor presenta resistencia negativa cerca de fn, el amortiguamiento neto es negativo y la oscilación (SSCI) crece en pocos ciclos, sin modos mecánicos.</div></div>

## Parte 2 — estabilidad y resonancia armónica
Inestabilidad de media-alta frecuencia (decenas de Hz a kHz) que se manifiesta como oscilaciones armónicas sostenidas o crecientes. Cada convertidor presenta Z_o(j·omega) con regiones de resistencia negativa (no pasivo), típicamente alrededor de la frecuencia de cruce del control, de la PLL o por el retardo digital. Si la fase de Z_o sale de (−90°, +90°) en una frecuencia donde coincide con una resonancia de red (paralelo Lg-C de cables/filtros), el amortiguamiento neto se vuelve negativo y aparece la oscilación. Es la versión de alta frecuencia del mismo análisis por impedancia, y la banda donde es crítico el amortiguamiento del filtro LCL.

<div class="cfig"><img src="figuras/estabilidad-armonica-pasividad.png" alt="parte real de la impedancia de salida con region no pasiva"><div class="cap">La parte real de la impedancia de salida Z_o del convertidor se vuelve negativa en una banda (sobre todo por el retardo digital): ahí es no pasivo. Si esa región coincide con una resonancia de red, el amortiguamiento neto es negativo y aparece la oscilación armónica.</div></div>

## Cuándo y por qué se usa
Subsíncrona: parques eólicos conectados por líneas compensadas serie (causa de eventos reales, p.ej. ERCOT 2009), HVDC y redes débiles con alta penetración de convertidores. Armónica: parques eólicos/PV con cables largos (alta capacidad), HVDC y redes con muchos convertidores, donde aparecen oscilaciones de cientos de Hz a kHz no explicables por la dinámica electromecánica. Ambas son subclases "resonancia" de la [[clasificacion-estabilidad|clasificación de estabilidad]].

## Procedimiento de diseño (genérico)
1. Modela Z_o(j·omega) del convertidor incluyendo control, PLL y retardo digital, y Z_g de la red.
2. Localiza las resonancias de red (serie por compensación → fn subsíncrona; paralelo de cables → resonancia armónica) y las regiones no pasivas del convertidor.
3. Aplica el criterio de impedancia/pasividad; identifica la frecuencia crítica (Re{Z_conv + Z_red} < 0).
4. Mitiga: ajustar banda de PLL/lazo de corriente, amortiguamiento activo del LCL, filtro notch, compensar retardo o impedancia virtual; damping subsíncrono dedicado (SSDC) para SSCI; a nivel red, TCSC/bypass del condensador serie.
5. Re-verifica con barrido del SCR, del nivel de compensación y del número de convertidores.

## Ejemplo de código
```python
import numpy as np

def series_resonance(f1, XL, XCs):        # frecuencia subsincrona de red
    return f1*np.sqrt(XCs/XL)

def passivity_violation(Zo, freqs):       # bandas no pasivas (candidatas)
    return freqs[np.real(Zo) < 0]
# inestable si Re{Z_conv(f) + Z_red(f)} < 0 cerca de una resonancia de red
```

## Parámetros y valores típicos
- Subsíncrona: compensación serie 20–75 % → fn ≈ 10–45 Hz; la SSCI puede crecer en 0.1–1 s; modos torsionales 10–50 Hz.
- Armónica: rango típico de inestabilidad 100 Hz–3 kHz; objetivo Re{Z_o} ≥ 0 o margen de fase de impedancia > 30° en las resonancias de red esperadas.

## Errores comunes
- Suponer que sin masas rotativas no hay riesgo subsíncrono (la SSCI es de control).
- Modelar el convertidor solo a la fundamental (no captura la resistencia negativa subsíncrona ni la de alta frecuencia).
- Diseñar la PLL solo por respuesta nominal, sin ver su efecto en la impedancia.
- Analizar un solo convertidor e ignorar la interacción paralelo de varios.
- Despreciar el retardo digital (principal fuente de no pasividad a alta frecuencia).
- Confiar solo en amortiguamiento pasivo (pérdidas) cuando el problema es el control.

## Conceptos relacionados
- [[impedancia-salida-estabilidad]] · [[clasificacion-estabilidad]] · [[interaccion-pll-red-debil]] · [[filtro-lcl]] · [[red-thevenin-scr]] · [[compensacion-retardo]] · [[filtro-notch]]

## Referencias
- Wang, Blaabjerg, Harmonic Stability in Power-Electronic-Based Power Systems, IEEE TPEL 2014.
- Wang et al., Unified Impedance Model of Grid-Connected VSCs, IEEE TPEL 2018.
- IEEE SSR WG, Terms, Definitions and Symbols for Subsynchronous Oscillations, 1985.
- Irwin et al., Sub-synchronous control interactions... series compensated transmission, IEEE PES 2011.
