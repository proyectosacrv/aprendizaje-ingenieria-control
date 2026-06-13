---
titulo: Sistema eólico DFIG/PMSG y MPPT
slug: eolica-mppt
categoria: fisica-modelado
tipo: concepto
nivel: avanzado
proyectos: []
objetivos: [modelar la turbina eólica y extraer la máxima potencia según el viento]
tags: [eolica, dfig, pmsg, mppt, cp-lambda, back-to-back, tipo-3, tipo-4, avanzado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-09
relacionados: [generador-sincrono, convertidor-vsc, control-vectorial, ecuacion-oscilacion, servicios-red-soporte]
referencias:
  - "Hansen, Aerodynamics of Wind Turbines, Earthscan 2008"
  - "Abad et al., Doubly Fed Induction Machine, Wiley 2011"
  - "Blaabjerg, Ma, Future on Power Electronics for Wind Turbine Systems, IEEE JESTPE 2013"
---

## Definición
Modelos aerodinámico, mecánico y eléctrico de una turbina eólica con generador **DFIG** (Tipo-3,
doblemente alimentado) o **PMSG** (Tipo-4, velocidad variable full-converter), y los algoritmos
**MPPT** para seguir la curva óptima de par/potencia en función de la velocidad del viento.

## Fundamento teórico
**Aerodinámica.** La potencia extraíble del viento:
$$ P=\frac{1}{2}\rho\pi R^2 v_w^3\,C_p(\lambda,\beta) $$
con \( \rho \) densidad del aire, \( R \) radio, \( v_w \) velocidad del viento y \( C_p \) el
coeficiente de potencia (límite de Betz: 16/27 ≈ 0.593). \( C_p \) depende de la **velocidad
específica** \( \lambda=\omega_r R/v_w \) y del ángulo de paso \( \beta \). Existe un \( \lambda^* \)
óptimo que maximiza \( C_p^{max} \approx0.45\text{–}0.50 \).

**MPPT:** mantener \( \lambda=\lambda^* \) a viento variable ajustando la velocidad de giro:
\( \omega_r^*=\lambda^* v_w/R \). Para evitar anemómetro, estrategia **OTC** (Optimal Torque
Control): la curva óptima \( T^*=k_{opt}\omega_r^2 \) (par ∝ cuadrado de velocidad), o
**Speed-mode**: regular \( \omega_r \) a la referencia calculada del viento medido.

**Drivetrain (tren de transmisión).** Modelo de dos masas (rotor aerodinámico + generador):
$$ 2H_t\dot\omega_t=T_{aero}-K_{dt}\theta_{tw}-D_{dt}(\omega_t-\omega_g)/\omega_0 $$
$$ 2H_g\dot\omega_g=K_{dt}\theta_{tw}+D_{dt}(\omega_t-\omega_g)/\omega_0-T_e $$
El modo de torsión del eje (1–3 Hz) puede excitar SSR con compensación serie (ver [[oscilaciones-subsincronas]]).

**DFIG (Tipo-3).** El rotor se alimenta por un convertidor back-to-back de potencia parcial
(\(\sim30\,\%\)). Control vectorial del rotor: eje d alineado con el flujo de estátor → desacopla
\( T_e \) (por \( i_{rq} \)) y flujo/reactiva (por \( i_{rd} \)). El lado red del convertidor regula
el bus DC y la reactiva de red. Opera ±30 % alrededor de la velocidad síncrona (rango de deslizamiento).

**PMSG (Tipo-4).** El generador (imanes permanentes, sin escobillas) se desacopla completamente de
la red por un convertidor back-to-back de potencia total. Control vectorial del lado máquina: MPPT
vía par; lado red: [[control-tension-bus-dc|regula bus DC y potencia reactiva]]. Sin contribución
de cortocircuito natural, pero el convertidor puede proveer [[fault-ride-through|FRT]] controlado.

**Regulación de paso (pitch).** Por encima de velocidad nominal se reduce \( \beta \) para limitar
\( P \) a la potencia nominal (control de \( \beta \) con PI sobre \( P \) o \( \omega_r \)).

<div class="cfig"><img src="figuras/eolica-mppt-cp.png" alt="curvas de potencia de la turbina por viento y locus MPPT"><div class="cap">Para cada velocidad de viento, la potencia de la turbina tiene un máximo a una velocidad de rotor distinta (donde $\lambda=\lambda^*$). El MPPT mantiene ese óptimo: la curva de par $T^*=k\,\omega_r^2$ (locus $\propto\omega^3$) pasa justo por los picos, así que basta seguirla —sin medir el viento— para extraer la máxima potencia.</div></div>

## Cuándo y por qué se usa
Para modelar el comportamiento de un parque eólico en estudios de estabilidad, diseño de control
de parque, servicios de frecuencia ([[servicios-red-soporte]]) y análisis de interacción con la red.

## Procedimiento de diseño (genérico)
1. Parametriza la curva \( C_p(\lambda,\beta) \) del fabricante; halla \( \lambda^*,C_p^{max} \).
2. Implementa el drivetrain de dos masas y la referencia MPPT (\( T^*=k_{opt}\omega_r^2 \)).
3. Diseña el control vectorial del generador (DFIG o PMSG): lazos de par y flujo/reactiva.
4. Diseña el lado red: bus DC ([[control-tension-bus-dc]]) y Q de red.
5. Añade pitch control para viento > nominal y protecciones de alta velocidad.
6. Verifica FRT e inyección de reactiva según grid code.

## Ejemplo de código
```python
def cp_lambda(lam, beta, cp_table):     # interpolacion de la tabla Cp(lambda,beta)
    import scipy.interpolate as sp
    return sp.interpn((lam_ax, beta_ax), cp_table, [lam, beta])[0]

def mppt_otc(wr, kopt):
    return kopt * wr**2                 # par optimo sin anemometro
```

## Parámetros y valores típicos
\( C_p^{max}\approx0.45\text{–}0.50 \); \( \lambda^*\approx6\text{–}9 \); \( H_t\approx3\text{–}5 \) s;
\( H_g\approx0.5\text{–}1 \) s. DFIG: deslizamiento ±30 %, potencia convertidor ∼30 %. PMSG:
convertidor 100 %.

## Errores comunes
- Modelar la turbina sin el drivetrain de dos masas → no captura el modo torsional (crítico para SSR).
- DFIG con control solo de lado rotor sin regular el bus DC → tensión DC no controlada.
- MPPT más rápido que el drivetrain → excita la resonancia torsional.

## Conceptos relacionados
- [[generador-sincrono]] · [[convertidor-vsc]] · [[control-vectorial]] · [[ecuacion-oscilacion]] · [[servicios-red-soporte]]

## Referencias
- Hansen, *Aerodynamics of Wind Turbines*, Earthscan 2008.
- Abad et al., *Doubly Fed Induction Machine*, Wiley 2011.
- Blaabjerg, Ma, *Future on Power Electronics for Wind Turbine Systems*, IEEE JESTPE 2013.
