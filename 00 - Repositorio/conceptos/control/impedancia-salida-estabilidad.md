---
titulo: Estabilidad por impedancia (Nyquist generalizado, pasividad y formalismos dq/secuencia)
slug: impedancia-salida-estabilidad
categoria: control
tipo: metodo
nivel: avanzado
proyectos: [01-GFM-Impedance, 02-GFL-Impedance, 03-DataCenter-IA]
objetivos: [evaluar la estabilidad de la interacción fuente-carga por sus impedancias sin re-simular, y entender por qué aparece la inestabilidad]
tags: [impedancia, nyquist, pasividad, resistencia-negativa, dq, secuencia, mirror-frequency, red-debil, SCR, oscilaciones]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-16
relacionados: [respuesta-frecuencia-ss, red-thevenin-scr, medicion-impedancia-inyeccion, marco-dq, componentes-simetricas, analisis-modal, pll-srf, interaccion-pll-red-debil]
referencias:
  - "Sun, Impedance-Based Stability Criterion for Grid-Connected Inverters, IEEE TPEL 2011"
  - "Wang, Blaabjerg, Harmonic Stability in Power-Electronic-Based Power Systems, IEEE TPEL 2014/2019"
  - "Harnefors et al., Passivity-Based Stability Assessment of Grid-Connected VSCs, IEEE TIE 2016"
  - "Rygg et al., A Modified Sequence-Domain Impedance Definition, IEEE JESTPE 2016"
---

## Definición
Método para decidir la estabilidad de la interacción entre dos subsistemas eléctricos (una fuente y una carga, o un equipo y la red) comparando sus impedancias de pequeña señal, sin reconstruir el modelo completo acoplado cada vez. Sirve para cualquier interconexión de dos puertos: inversor contra red, etapa fuente contra etapa carga en un bus DC, dos convertidores entre sí. Esta ficha reúne las tres caras del mismo análisis: el criterio exacto (Nyquist generalizado del cociente de impedancias), la condición suficiente e intuitiva (pasividad / resistencia negativa) y los dos formalismos en que se expresa la impedancia (dq y secuencia).

## Planteamiento genérico (dos puertos)
Cualquier interconexión se modela como un puerto "fuente" con impedancia de salida Z_fuente(s) y un puerto "carga" con admitancia de entrada Y_carga(s) (o impedancia Z_carga). Si ambos son estables por separado, la estabilidad del conjunto depende solo del cociente de sus impedancias en el punto de conexión. En convertidores trifásicos el puerto es un sistema MIMO 2×2 (en dq), así que el criterio escalar de Middlebrook se generaliza al Nyquist de una matriz. La convención de signos importa: la admitancia de salida de un equipo que inyecta corriente se define Y = −∂i/∂v en el PCC (convención de fuente).

## Parte 1 — criterio exacto (Nyquist generalizado)
Con el equipo modelado como admitancia de salida Y_inv(s) (2×2) y la red como impedancia Z_red(s), el minor loop gain es:

L(s) = Z_red(s)·Y_inv(s)

Si equipo y red son estables por separado, el conjunto es estable si y solo si los autovalores de L(j·omega) no rodean −1 (Nyquist generalizado). Equivale a exigir que det(I + L(s)) no tenga ceros en el semiplano derecho. Visto en magnitud, la estabilidad se juega en la frecuencia donde |Z_red| corta a |Z_inv|: una red débil (SCR bajo) sube |Z_red| y mueve el cruce a frecuencias donde el margen de fase del cociente puede ser insuficiente.

<div class="cfig"><img src="figuras/impedancia-salida-estabilidad-cruce.png" alt="cruce de magnitudes de impedancia inversor y red"><div class="cap">Criterio de impedancia en magnitud: la estabilidad se juega donde |Z_red| corta a |Z_inv|. Una red débil (SCR bajo) sube |Z_red| y mueve el cruce a frecuencias donde el margen de fase del cociente Z_red/Z_inv puede ser insuficiente; el criterio exacto es el Nyquist generalizado de sus autovalores.</div></div>

## Parte 2 — condición suficiente (pasividad y resistencia negativa)
Un puerto eléctrico es pasivo si no genera energía neta: en impedancia, Re{Z(j·omega)} ≥ 0 para todo omega. Cuando Re{Z} < 0 en alguna banda, el puerto presenta resistencia negativa (es no pasivo) y puede entregar energía a una resonancia, con riesgo de inestabilidad al conectarse.

Si tanto el equipo como la red son pasivos en todo el rango, su interconexión es estable (criterio de pasividad, suficiente). La inestabilidad solo puede aparecer donde al menos uno es no pasivo. En grid-following, los lazos (sobre todo la PLL) introducen un desfase que vuelve Re{Z} < 0 en su banda; si la impedancia inductiva de la red cruza esa región, se forma una resonancia mal amortiguada y aparece la oscilación. La pasividad es una condición suficiente y local en frecuencia; el Nyquist generalizado de Z_red·Y_inv es el criterio exacto. Un sistema no pasivo puede ser estable con una red concreta: la no pasividad solo señala el riesgo.

<div class="cfig"><img src="figuras/no-pasividad-resistencia-negativa-rez.png" alt="parte real de la impedancia negativa en la banda de la PLL"><div class="cap">La parte real de la impedancia de salida (eje q) del grid-following se vuelve negativa —no pasiva— en la banda de la PLL. Una PLL más rápida ensancha esa banda hacia frecuencias mayores; si la red inductiva resuena ahí, aparece la oscilación. La pasividad (Re{Z}≥0) es condición suficiente, no exacta.</div></div>

Uso de la pasividad para diseñar (impedance shaping): dar forma a la impedancia del equipo de modo que sea pasiva en el rango donde la red pueda resonar evita la inestabilidad sin conocer la red exacta. Procedimiento: calcular/medir Z(j·omega), localizar las bandas con Re{Z} < 0, identificar la causa (PLL, retardo de cómputo, lazos lentos) y reducirla (PLL más lenta, compensación de retardo, realimentación que aporte amortiguamiento).

## Parte 3 — formalismos dq vs secuencia
La impedancia de pequeña señal del convertidor se representa de dos formas equivalentes: dq (matriz 2×2 en marco síncrono giratorio) y secuencia (Z+, Z− en marco estacionario, definidas por inyección de secuencia positiva/negativa). Ambas alimentan el mismo criterio de Nyquist generalizado.

Marco dq. Se linealiza el convertidor en el marco síncrono y se obtiene:

[dvd; dvq] = [[Zdd, Zdq],[Zqd, Zqq]]· [did; diq]

Los términos cruzados Zdq, Zqd capturan el acoplamiento (PLL, lazo de potencia, términos ±omega del marco dq). Es el marco natural cuando el control vive en dq (GFL con PLL, GFM con droop/VSM).

Marco de secuencia. Inyectando una pequeña tensión de secuencia positiva a frecuencia fp, el convertidor responde a fp y también a la frecuencia espejo fp − 2·f1 (mirror frequency coupling), por la asimetría que introducen PLL/control. Esto obliga a una definición 2×2 (impedancia de secuencia modificada) con fm = fp − 2·f1. Si el acoplamiento es débil se reduce a dos escalares Z+, Z− desacoplados.

Equivalencia. Hay una transformación lineal exacta entre ambas (cambio de variable complejo s_dq ↔ s ∓ j·omega1): el acoplamiento d-q en dq equivale al acoplamiento de frecuencia espejo en secuencia. No son fenómenos distintos, son el mismo visto en dos marcos.

| Aspecto | dq | Secuencia |
|---|---|---|
| Marco | giratorio | estacionario |
| Variable | Zdd, Zqq, Zdq, Zqd | Zpp, Zmm, Zpm, Zmp |
| Medida | inyección en dq (necesita ángulo) | inyección de secuencia (frecuencia real) |
| Intuición | acoplamiento de control | resonancia/espejo físico |

Cuándo usar cada uno: dq cuando el modelo analítico del control está en dq (proyectos GFM/GFL) y para casar con el Nyquist generalizado; secuencia cuando se mide experimentalmente con inyección de frecuencia real, o para razonar sobre resonancias y armónicos de red.

<div class="cfig"><img src="figuras/impedancia-dq-vs-secuencia-espejo.png" alt="acoplamiento de frecuencia espejo entre dq y secuencia"><div class="cap">Al inyectar una perturbación de secuencia a frecuencia fp, la asimetría de PLL/control hace que el convertidor responda también a la frecuencia espejo fp−2·f1. Ese acoplamiento de frecuencia espejo en secuencia es el mismo fenómeno que el acoplamiento d-q en dq, relacionados por s_dq = s ∓ j·omega1.</div></div>

## Cuándo y por qué se usa
Integración masiva de convertidores, oscilaciones subsíncronas, redes débiles, estabilidad de buses DC en cascada. Permite barrer la fortaleza de red (SCR) y hallar el SCR crítico de inestabilidad de forma modular, sin re-simular todo el sistema cada vez.

## Procedimiento de diseño (genérico)
1. Obtén Y_inv(j·omega) del equipo (ver [[respuesta-frecuencia-ss]] o [[medicion-impedancia-inyeccion]]); elige marco dq (analítico) o secuencia (experimental).
2. Modela Z_red(j·omega) según SCR y X/R (ver [[red-thevenin-scr]]).
3. Calcula L = Z_red·Y_inv y sus autovalores en frecuencia.
4. Aplica Nyquist generalizado: ¿rodean −1? Barre SCR hasta el crítico.
5. Como chequeo intuitivo, localiza las bandas no pasivas (Re{Z} < 0) y comprueba si coinciden con la resonancia de red.
6. Valida contra los autovalores del modelo acoplado (deben coincidir).

## Ejemplo de código
```python
import numpy as np

# Nyquist generalizado: autovalores del minor loop gain en cada frecuencia
for k, f in enumerate(freqs):
    s = 2j*np.pi*f
    G    = C @ np.linalg.solve(s*np.eye(n) - A, B) + D
    Yinv = -G                                              # convencion de fuente
    Zg   = np.array([[Rg+s*Lg, -w0*Lg], [w0*Lg, Rg+s*Lg]])
    lam[k] = np.linalg.eigvals(Zg @ Yinv)                 # no deben rodear -1

# Chequeo de pasividad (banda no pasiva en eje q)
Z = impedance(A, B, C, D, freqs)          # matriz dq 2x2 por frecuencia
nopasiva = freqs[Z[:, 1, 1].real < 0]     # Re{Zqq} < 0
```

## Parámetros y valores típicos
- El SCR crítico depende del control: grid-following inestable en red débil (SCR bajo); grid-forming agresivo inestable en red fuerte (SCR alto).
- La banda no pasiva del GFL coincide con el ancho de banda de la PLL; una PLL rápida la ensancha hacia frecuencias mayores.
- Acoplamiento d-q (o espejo) relevante cuando la PLL/lazo de potencia es de banda ancha o la red es débil; entonces los términos cruzados no se pueden despreciar.

## Errores comunes
- Confundir el signo: Y_inv = −∂i_g/∂v_pcc (convención de fuente).
- Aplicar el Nyquist SISO a un sistema dq acoplado → usar el generalizado (autovalores de la matriz 2×2).
- Confundir pasividad (suficiente, conservadora) con el criterio exacto: un sistema no pasivo puede ser estable con una red concreta.
- Usar impedancia escalar cuando hay acoplamiento fuerte; ignorar la frecuencia espejo al medir en secuencia; mezclar convenciones de marco/ángulo entre fuente y carga.
- Olvidar validar contra el modelo acoplado.

## Uso en proyectos
- 01 - GFM-Impedance (estabilidad en red): SCR crítico por Nyquist = 3.39 y por autovalores del modelo acoplado = 3.35 (diferencia 1.3%). En main_phase3.py.
- 02 - GFL-Impedance (explicar la inestabilidad): la impedancia de salida del GFL tiene Re{Zqq} < 0 en la banda de la PLL; con PLL rápida se extiende a más frecuencia, lo que explica la inestabilidad en red débil.

## Conceptos relacionados
- [[respuesta-frecuencia-ss]] · [[red-thevenin-scr]] · [[medicion-impedancia-inyeccion]] · [[marco-dq]] · [[componentes-simetricas]] · [[analisis-modal]] · [[pll-srf]] · [[interaccion-pll-red-debil]]

## Referencias
- Sun, IEEE TPEL 2011.
- Wang, Blaabjerg, Harmonic Stability..., IEEE TPEL 2014/2019.
- Harnefors et al., Passivity-Based Stability Assessment..., IEEE TIE 2016.
- Rygg et al., A Modified Sequence-Domain Impedance Definition, IEEE JESTPE 2016.
