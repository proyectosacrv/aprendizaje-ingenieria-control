---
titulo: Márgenes de estabilidad (ganancia, fase, módulo)
slug: margenes-estabilidad
categoria: metodologia
tipo: metodo
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [cuantificar cuanto margen tiene el diseno antes de inestabilizarse]
tags: [margen-fase, margen-ganancia, M_s, robustez, nyquist]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-11
relacionados: [funciones-sensibilidad, loop-shaping, robustez-parametrica, impedancia-salida-estabilidad]
referencias:
  - "Aström, Murray, Feedback Systems, Princeton 2008"
---

## Definición
Medidas de **cuánto puede cambiar** el sistema antes de volverse inestable. Cuantifican la
robustez del diseño, no solo si es estable.

## Fundamento teórico
Sobre la ganancia de lazo \( L(j\omega) \):
- **Margen de ganancia** (GM): cuánto se puede subir la ganancia antes de inestabilizar (a la
  frecuencia donde la fase es −180°).
- **Margen de fase** (PM): retardo de fase admisible en el cruce de ganancia (\( |L|=1 \)).
  Se relaciona con el amortiguamiento: \( \zeta\approx \mathrm{PM}/100 \).
- **Margen de módulo** \( = 1/M_s \), con \( M_s=\max_\omega |S(j\omega)| \) (pico de
  sensibilidad): distancia mínima de \( L(j\omega) \) al punto crítico −1. Es el más completo
  (resume GM y PM). \( M_s<2 \) (≈6 dB) es buen objetivo.
- **Margen de retardo**: \( \mathrm{PM}/\omega_c \) → retardo de cómputo/PWM admisible.

<div class="cfig"><img src="figuras/margenes-estabilidad-bode.png" alt="margenes de ganancia y fase sobre el Bode"><div class="cap">Sobre el Bode de la ganancia de lazo: el margen de fase (PM) se mide en el cruce de ganancia (|L|=0 dB) y el de ganancia (GM) en el cruce de fase (−180°). Aquí PM≈63°, GM≈27 dB (diseño holgado).</div></div>

## Cuándo y por qué se usa
Tras comprobar estabilidad nominal: dice si el diseño aguanta variaciones de planta, retardos y
errores de modelo. Imprescindible antes de validar en hardware.

## Procedimiento (genérico)
1. Calcula \( L(j\omega)=C(j\omega)G(j\omega) \) (o el minor loop gain en impedancia).
2. PM y GM con `control.margin` o leyendo el cruce; \( M_s \) como pico de \( |S| \).
3. Comprueba contra los objetivos (PM 45–60°, GM>6 dB, \( M_s<2 \)).
4. Convierte PM a margen de retardo y compáralo con el retardo real (cómputo + PWM).

## Ejemplo de código
```python
import control as ct
gm, pm, wcg, wcp = ct.margin(L)        # L: ganancia de lazo (sistema LTI)
Ms = (1/(1+L)).frequency_response(w)   # pico = M_s ; margen de modulo = 1/Ms
```

## Parámetros y valores típicos
PM 45–60°, GM > 6 dB, \( M_s < 2 \). Margen de retardo > varios periodos de muestreo.

## Errores comunes
- Mirar solo PM/GM: pueden ser buenos y aún tener \( M_s \) alto (poco robusto). Usar \( M_s \).
- Olvidar el retardo de cómputo/PWM al evaluar el margen real.

## Uso en proyectos
- **01 (GFM)**: el lazo de potencia tenía **margen de fase −86°** (inestable) — eso reveló la
  causa y guió la cura (impedancia virtual). El criterio de impedancia (Fase 3) es el Nyquist
  generalizado equivalente.

## Conceptos relacionados
- [[funciones-sensibilidad]] · [[loop-shaping]] · [[impedancia-salida-estabilidad]] · [[robustez-parametrica]]

## Referencias
- Aström, Murray, *Feedback Systems*, 2008.
