---
titulo: Especificaciones de control (traducir requisitos a métricas)
slug: especificaciones-control
categoria: metodologia
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [fijar objetivos medibles antes de disenar]
tags: [especificaciones, ancho-de-banda, margen, requisitos, diseno]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [ciclo-diseno-control, metricas-desempeno, margenes-estabilidad, metodos-sintesis-control]
referencias:
  - "Aström, Murray, Feedback Systems, Princeton 2008 (cap. 11)"
---

## Definición
Primer paso del diseño: convertir requisitos cualitativos ("rápido", "estable", "robusto") en
**números objetivo** que guían la síntesis y sirven de criterio de aceptación.

## Fundamento teórico
Especificaciones típicas y su forma medible:
- **Velocidad / ancho de banda** \( \omega_c \) (frecuencia de cruce de ganancia). Regla:
  \( t_{s}\approx 4/(\zeta\omega_n) \), \( \omega_c \) marca la rapidez del lazo.
- **Amortiguamiento** \( \zeta \) (o sobreimpulso \( M_p\approx e^{-\pi\zeta/\sqrt{1-\zeta^2}} \)).
- **Robustez**: margen de fase \( \ge 40\text{–}60° \), margen de ganancia \( \ge 6 \) dB,
  pico de sensibilidad \( M_s \le 2 \) (≈6 dB).
- **Error en régimen**: tipo de sistema / ganancia DC para anular error a escalón/rampa.
- **Rechazo de perturbación** y atenuación de ruido (forma de S y T, ver [[funciones-sensibilidad]]).

En convertidores hay además restricciones físicas: \( \omega_c < \) (1/5–1/10) de \( f_{sw} \),
y separación de escalas entre lazos en cascada.

<div class="cfig"><img src="figuras/especificaciones-control-mp-zeta.png" alt="relacion entre sobreimpulso y amortiguamiento"><div class="cap">Ejemplo de traducción de un requisito a una métrica: el sobreimpulso de un sistema de 2º orden $M_p=e^{-\pi\zeta/\sqrt{1-\zeta^2}}$ depende solo del amortiguamiento. Fijar $M_p\le10\%$ se convierte en una especificación medible sobre el diseño: $\zeta\ge0.59$. Así cada requisito cualitativo pasa a número objetivo y criterio de aceptación.</div></div>

## 1 — Ejemplo cuantitativo: traducción de requisitos a números objetivo en un GFL
**Requisito 1 — rapidez:** el lazo de corriente debe seguir una rampa de 0 a 1 p.u. en menos de 2 ms. Ello impone \( t_s<2\,\text{ms} \) ↔ \( \omega_{ci}>4/t_s=4/0.002=2000 \) rad/s ↔ \( f_{ci}>318\,\text{Hz} \). Se elige \( f_{ci}=500\,\text{Hz} \) (con \( f_{sw}=5\,\text{kHz} \), factor 10 cumplido \( \checkmark \)).

**Requisito 2 — robustez:** margen de fase mínimo 45° para tolerancia al retardo de cómputo de \( T_s/2=100\,\mu\text{s} \). El retardo puro añade fase \( -\omega\,T_d \): a \( \omega_{ci}=2\pi\times500 \), la pérdida de fase es \( 2\pi\times500\times100\times10^{-6}\times180/\pi=18° \). Partiendo de 72° (cancelación de polo puro), se queda en 54° — cumple el límite de 45° \( \checkmark \).

**Requisito 3 — error en régimen.** Para anular error a escalón de corriente se necesita al menos un integrador en el lazo (acción integral del PI \( \checkmark \)).

**Traducción final:**

| Requisito | Métrica | Valor objetivo |
|---|---|---|
| Rapidez | \( f_{ci} \) | 500 Hz |
| Robustez | margen de fase | ≥ 45° |
| Precisión | error en escalón | 0 (integrador) |
| Compatibilidad PWM | \( f_{ci}/f_{sw} \) | ≤ 1/10 |

## Cuándo y por qué se usa
Antes de elegir cualquier método. Sin especificaciones medibles no hay forma de saber si el
diseño "está bien" ni de validarlo objetivamente.

## Procedimiento (genérico)
1. Lista los requisitos del sistema (rapidez, precisión, robustez, límites físicos).
2. Tradúcelos a métricas: \( \omega_c, \zeta/M_p, \) márgenes, \( M_s \), error, anchos de
   banda relativos de lazos en cascada.
3. Comprueba compatibilidad (p.ej. ancho de banda vs \( f_{sw} \), vs resonancia del filtro).
4. Documenta cada métrica como **criterio de aceptación** para la fase de evaluación/validación.

## Parámetros y valores típicos (convertidores)
Lazo de corriente: \( f_c \) ≈ \( f_{sw}/10 \). Lazo de tensión: ≈ \( f_{ci}/(3\text{–}5) \).
Margen de fase 45–60°, \( M_s \) < 2. Droop/PLL: el lazo más lento (Hz–decenas de Hz).

## Errores comunes
- "Ajustar hasta que vaya" sin objetivos → no es reproducible ni validable.
- Pedir ancho de banda incompatible con \( f_{sw} \) o con la resonancia del filtro.

## Uso en proyectos
- **01/02**: lazo de corriente ~1 kHz, tensión ~350 Hz, droop/PLL ~Hz; margen y \( \zeta \)
  objetivo guiaron la sintonía (modo de potencia GFM a \( \zeta=0.40 \)).

## Conceptos relacionados
- [[ciclo-diseno-control]] · [[metricas-desempeno]] · [[margenes-estabilidad]]

## Referencias
- Aström, Murray, *Feedback Systems*, cap. 11.
