---
titulo: Estabilidad por Bode — márgenes de ganancia, fase y módulo
slug: margenes-estabilidad
categoria: metodologia
tipo: metodo
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [decidir la estabilidad de un lazo desde el Bode de la ganancia de lazo y cuantificar cuánto margen queda antes de inestabilizarse]
tags: [margen-fase, margen-ganancia, M_s, bode, estabilidad, robustez, nyquist]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-17
relacionados: [diagrama-bode, criterio-nyquist, funciones-sensibilidad, loop-shaping, robustez-parametrica, impedancia-salida-estabilidad]
referencias:
  - "Aström, Murray, Feedback Systems, Princeton 2008"
  - "Franklin, Powell, Emami-Naeini, Feedback Control of Dynamic Systems"
---

## Definición
Los márgenes de estabilidad miden **cuánto puede cambiar** un lazo de control antes de volverse inestable. No dicen solo si el sistema es estable: cuantifican la **robustez** (cuánta ganancia, fase o retardo de más aguanta). Todo se lee sobre el **Bode de la ganancia de lazo** \( L(j\omega)=C(j\omega)\,G(j\omega) \), donde \( C \) es el controlador y \( G \) la planta.

## El punto crítico: por qué −1 (o −180° con ganancia 1)
Un lazo de realimentación negativa tiene función de transferencia en lazo cerrado
$$ T(s)=\frac{L(s)}{1+L(s)} $$
que se hace infinita (polos del lazo cerrado) donde \( 1+L(s)=0 \), es decir donde \( L(s)=-1 \). El número complejo \( -1 \) tiene módulo \( 1 \) y fase \( -180^\circ \). La idea física: si a alguna frecuencia la señal recorre el lazo y vuelve con la **misma amplitud** (\( |L|=1 \)) y **invertida** (\( -180^\circ \)), la realimentación —que debía ser negativa— se vuelve positiva y se sostiene sola: oscilación. Por eso toda la estabilidad se juega en cuán cerca pasa \( L(j\omega) \) del punto \( -1 \).

## Criterio de estabilidad por Bode
Para una ganancia de lazo **estable en lazo abierto y de fase mínima** (el caso habitual de un lazo de corriente/tensión bien planteado), el criterio es directo:

> El lazo cerrado es **estable** si, en la frecuencia de cruce de ganancia \( \omega_c \) (donde \( |L(j\omega_c)|=1 \), es decir 0 dB), la **fase está por encima de −180°**.

Equivalentemente, en la frecuencia de cruce de fase \( \omega_{180} \) (donde la fase vale −180°), la ganancia debe estar **por debajo de 0 dB**. De ahí salen las dos distancias al punto crítico:

- **Margen de fase (PM):** cuánta fase de más se puede perder en \( \omega_c \) antes de llegar a −180°:
$$ \mathrm{PM}=180^\circ+\angle L(j\omega_c) \qquad (|L(j\omega_c)|=1) $$
- **Margen de ganancia (GM):** cuánto se puede subir la ganancia en \( \omega_{180} \) antes de llegar a 0 dB:
$$ \mathrm{GM}=\frac{1}{|L(j\omega_{180})|} \qquad (\angle L(j\omega_{180})=-180^\circ) $$
(en dB, \( \mathrm{GM}_{dB}=-20\log_{10}|L(j\omega_{180})| \)). Ambos positivos ⇒ estable y con holgura; un PM o GM negativo señala inestabilidad.

<div class="cfig"><img src="figuras/margenes-estabilidad-bode.png" alt="márgenes de ganancia y fase sobre el Bode de la ganancia de lazo"><div class="cap">Sobre el Bode de \(L(j\omega)\): el margen de fase (PM) se mide en el cruce de ganancia (\(|L|=0\) dB) y el de ganancia (GM) en el cruce de fase (−180°). Aquí PM≈63°, GM≈27 dB (diseño holgado).</div></div>

### Cómo leerlo paso a paso sobre el Bode
1. Localiza el **cruce de ganancia** \( \omega_c \): donde la curva de magnitud corta 0 dB.
2. Baja a la curva de fase en esa misma \( \omega_c \) y mide cuánto falta hasta −180°: ese hueco es el **PM**.
3. Localiza el **cruce de fase** \( \omega_{180} \): donde la fase pasa por −180°.
4. Sube a la curva de magnitud en esa \( \omega_{180} \) y mide cuántos dB faltan hasta 0 dB: ese hueco (en valor absoluto) es el **GM**.

## Por qué el margen de fase fija el amortiguamiento y la sobreoscilación
El PM no es un número abstracto: gobierna cómo responde el lazo cerrado. Para un lazo dominado por dos polos, el amortiguamiento se aproxima por
$$ \zeta \approx \frac{\mathrm{PM}}{100} \quad (\mathrm{PM\ en\ grados}) $$
de modo que PM grande ⇒ \( \zeta \) grande ⇒ respuesta amortiguada; PM pequeño ⇒ \( \zeta \) pequeño ⇒ sobreoscilación y oscilaciones lentas de extinguir. Un PM \( \to 0 \) es un lazo al borde de oscilar de forma sostenida.

<div class="cfig"><img src="figuras/margenes-estabilidad-pm-respuesta.png" alt="comparación de tres diseños con distinto margen de fase y su respuesta al escalón en lazo cerrado"><div class="cap">Tres diseños del mismo lazo con distinto PM (izquierda, Bode con el cruce de ganancia marcado) y su respuesta al escalón en lazo cerrado (derecha). A menos PM, más sobreoscilación y más oscilación residual; a más PM, respuesta más amortiguada.</div></div>

## Margen de módulo (el más completo)
PM y GM miran solo dos frecuencias concretas. El **margen de módulo** mira la distancia mínima de \( L(j\omega) \) al punto \( -1 \) en **todas** las frecuencias, y es por eso la medida de robustez más fiable. Se define con el pico de la función de sensibilidad \( S=1/(1+L) \) (ver [[funciones-sensibilidad]]):
$$ M_s=\max_\omega |S(j\omega)|=\max_\omega \frac{1}{|1+L(j\omega)|}, \qquad \text{margen de módulo}=\frac{1}{M_s} $$
\( M_s \) es el inverso de esa distancia mínima: \( M_s<2 \) (≈6 dB) es buen objetivo. Un sistema puede tener PM y GM aparentemente buenos y aun así un \( M_s \) alto (la curva se acerca a −1 en una frecuencia intermedia): por eso conviene mirar \( M_s \).

## Margen de retardo
Un retardo puro \( e^{-s\tau} \) no cambia la magnitud pero resta fase \( \omega\tau \). El PM dice cuánto retardo aguanta el lazo antes de inestabilizarse:
$$ \tau_{max}=\frac{\mathrm{PM\ (rad)}}{\omega_c} $$
Es el chequeo clave en control digital: el retardo de cómputo más el de PWM (del orden de \( 1.5\,T_s \)) debe ser bastante menor que \( \tau_{max} \).

## Cuándo y por qué se usa
Tras comprobar la estabilidad nominal: los márgenes dicen si el diseño aguanta variaciones de planta, retardos y errores de modelo. Es el chequeo imprescindible antes de validar en hardware. En problemas de interacción convertidor-red el equivalente es el criterio de impedancia / Nyquist generalizado (ver [[impedancia-salida-estabilidad]]).

## Procedimiento (genérico)
1. Calcula \( L(j\omega)=C(j\omega)G(j\omega) \) (o el minor loop gain en impedancia).
2. Lee PM y GM en los cruces (o con `control.margin`); calcula \( M_s \) como el pico de \( |S| \).
3. Comprueba contra objetivos: PM 45–60°, GM > 6 dB, \( M_s<2 \).
4. Convierte PM a margen de retardo \( \tau_{max}=\mathrm{PM}/\omega_c \) y compáralo con el retardo real (cómputo + PWM).

## Ejemplo de código
```python
import control as ct
gm, pm, wcg, wcp = ct.margin(L)          # GM, PM y sus frecuencias de cruce
S  = 1/(1+L)                              # sensibilidad
Ms = max(abs(S.frequency_response(w)[0])) # pico de |S| ; margen de modulo = 1/Ms
tau_max = (pm*3.14159/180)/wcp            # margen de retardo (PM en rad / wc)
```

## Parámetros y valores típicos
PM 45–60°, GM > 6 dB, \( M_s<2 \). Margen de retardo > varios periodos de muestreo. Como guía: PM≈70° apenas sobreoscila; PM≈45° sobreoscila ≈20–25%; PM<30° ya es poco robusto.

## Límites del criterio de Bode (cuándo NO basta)
El criterio simple "PM>0 y GM>0 ⇒ estable" vale para lazo abierto estable y de fase mínima con un único cruce de ganancia. Falla en:
- **Sistemas condicionalmente estables**: la magnitud cruza 0 dB varias veces y subir o bajar la ganancia puede inestabilizar. Hay que mirar todos los cruces.
- **Planta inestable en lazo abierto o de fase no mínima** (ceros en el semiplano derecho, retardos grandes): el conteo de fase engaña.
- **Sistemas MIMO / acoplados** (lazo de corriente dq, interacción convertidor-red): se usa el [[criterio-nyquist|Nyquist]] (o el generalizado) sobre \( L(j\omega) \), que es el criterio exacto del que los márgenes son la versión rápida.

## Errores comunes
- Mirar solo PM/GM: pueden ser buenos y aun tener \( M_s \) alto (poco robusto). Usar \( M_s \).
- Olvidar el retardo de cómputo/PWM al evaluar el margen real.
- Aplicar el criterio simple a un sistema condicionalmente estable o de fase no mínima.
- Confundir el cruce de ganancia (\( |L|=1 \)) con el de fase (\( -180^\circ \)): PM va en el primero, GM en el segundo.

## Uso en proyectos
- **01 (GFM)**: el lazo de potencia tenía **margen de fase −86°** (inestable) — eso reveló la causa y guió la cura (impedancia virtual). El criterio de impedancia (Fase 3) es el Nyquist generalizado equivalente.

## Conceptos relacionados
- [[diagrama-bode]] · [[criterio-nyquist]] · [[funciones-sensibilidad]] · [[loop-shaping]] · [[robustez-parametrica]] · [[impedancia-salida-estabilidad]]

## Referencias
- Aström, Murray, *Feedback Systems*, 2008.
- Franklin, Powell, Emami-Naeini, *Feedback Control of Dynamic Systems*.
