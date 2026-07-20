---
titulo: Power Synchronization Control (PSC)
slug: power-synchronization-control
categoria: control
tipo: tecnica
nivel: avanzado
proyectos: []
objetivos: [sincronizar un convertidor a la red por potencia activa, sin PLL]
tags: [psc, sincronizacion, grid-forming, sin-pll, hvdc, red-debil, avanzado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-09
relacionados: [grid-forming-vs-following, vsm-inercia, droop-control, interaccion-pll-red-debil, ecuacion-oscilacion]
referencias:
  - "Zhang et al., Power Synchronization Control of Grid-Connected VSC, IEEE TPWRS 2010"
  - "Harnefors et al., Synchronization Stability of Grid-Connected VSCs, IEEE TPEL 2017"
---

## Definición
Estrategia grid-forming en la que el ángulo de salida del convertidor se genera **integrando el
error de potencia activa** —en vez de usar una PLL que mide la fase de la red— de forma análoga a
la sincronización electromagnética de un generador síncrono.

## Fundamento teórico
La idea central es que la **potencia activa** fluye entre dos fuentes de tensión según su diferencia
de ángulo \( \delta \). Usando esa relación como lazo de control:
$$ \dot\delta = K_{psc}(P^*-P) \implies \delta = \int K_{psc}(P^*-P)\,dt $$
con \( K_{psc} \) ganancia de sincronización. Esto produce la misma dinámica que la
[[ecuacion-oscilacion|swing equation]] sin inercia explícita: en régimen permanente \( P=P^* \) y
el ángulo \( \delta \) queda fijo. La acción integral acumula el ángulo relativo correcto.

Comparando con [[vsm-inercia|VSM]] y [[droop-control|droop P-f]]:

| Aspecto | Droop \(\omega-P\) | VSM | PSC |
|---|---|---|---|
| Variable de lazo | frecuencia | frecuencia (virtual) | ángulo |
| PLL | necesaria | puede evitarse | no, intrínseca |
| Inercia | no | sí (emulada) | no (puede añadirse) |
| Análisis | Bode de lazo P | modelo SS mecánico | sistema de 1er orden en \(\delta\) |

La **estabilidad** de PSC se analiza linearizando la potencia \( P=\frac{EV_g}{X}\sin\delta \) en
el punto de operación: la ganancia del lazo de sincronización es \( K_{psc}\cdot K_s \) (par
sincronizante \( K_s=EV_g\cos\delta_0/X \)). Un polo dominante en
\( s=-K_{psc}K_s \) → la sincronización es de **primer orden** (sin oscilación) mientras no haya
retardos importantes. La **limitación de corriente** se implementa reduciendo \( E \) (tensión
virtual) o cambiando la referencia de \( Q \); esto cambia dinámicamente la reactancia efectiva y
puede inestabilizar en red muy débil si no se coordina.

En red débil (bajo [[red-thevenin-scr|SCR]]), la PLL de un GFL desestabiliza
([[interaccion-pll-red-debil]]), mientras PSC opera estable porque no depende de medir la fase de
la red; fue propuesto originalmente para **HVDC** en red débil.

<div class="cfig"><img src="figuras/power-synchronization-control-sync.png" alt="sincronizacion de primer orden del PSC ante un escalon de potencia"><div class="cap">El PSC genera el ángulo integrando el error de potencia ($\dot\delta=K_{psc}(P^*-P)$), sin PLL. Linealizado en el punto de operación da un sistema de primer orden con polo en $s=-K_{psc}K_s$: la potencia sigue a $P^*$ sin oscilación. Por no medir la fase de la red, opera estable donde la PLL de un GFL fallaría (red muy débil).</div></div>

## 1 — Linealización del lazo P→δ: el polo de primer orden \( -K_{psc}K_s \)
**Paso 1 — el lazo de sincronización.** El ángulo de salida se genera integrando el error de potencia activa, sin PLL:
$$ \dot\delta=K_{psc}\,(P^*-P) $$

**Paso 2 — cómo el ángulo mueve la potencia.** La potencia transferida a la red a través de la reactancia total es \( P=\dfrac{EV_g}{X}\sin\delta \). En un punto de operación \( \delta_0 \), una pequeña variación \( \tilde\delta=\delta-\delta_0 \) la perturba según la derivada (par sincronizante):
$$ \tilde P=\frac{\partial P}{\partial\delta}\Big|_{\delta_0}\tilde\delta=\underbrace{\frac{EV_g}{X}\cos\delta_0}_{K_s}\;\tilde\delta $$
\( K_s \) es positivo mientras \( \delta_0<90° \): más ángulo entrega más potencia.

**Paso 3 — cerrar el lazo en pequeña señal.** Con \( P^* \) constante, \( \widetilde{(P^*-P)}=-\tilde P=-K_s\tilde\delta \). Sustituyendo en el lazo:
$$ \dot{\tilde\delta}=K_{psc}\,(-K_s\,\tilde\delta)=-K_{psc}K_s\,\tilde\delta $$

**Paso 4 — el polo.** Es una ecuación diferencial lineal de **primer orden**. En Laplace, \( s\tilde\delta=-K_{psc}K_s\tilde\delta \), cuya raíz es
$$ \boxed{\;s=-K_{psc}\,K_s,\qquad K_s=\frac{EV_g\cos\delta_0}{X}\;} $$
Un único polo real negativo (mientras \( \delta_0<90° \) → \( K_s>0 \)): la sincronización es **monótona, sin oscilación**, con constante de tiempo \( \tau=1/(K_{psc}K_s) \). No hay segundo estado (a diferencia del VSM, que con la inercia \( J \) es de 2º orden y puede oscilar). El polo se ajusta con \( K_{psc} \): más ganancia, sincronización más rápida.

**Paso 5 — los dos riesgos.** Si \( \delta_0\to90° \), \( \cos\delta_0\to0 \) → \( K_s\to0 \) → el polo se acerca al origen: par sincronizante mínimo, casi se pierde el sincronismo. Y la limitación de corriente, que actúa bajando \( E \), reduce \( K_s\propto E \): mueve el polo y, con retardos, puede inestabilizar en red muy débil. Por eso se diseña con \( \delta_0<30\text{–}45° \) y la limitación coordinada con \( E \).

## Cuándo y por qué se usa
Convertidores HVDC, almacenamiento y renovables en redes muy débiles (SCR < 1.5) donde la PLL
falla. Alternativa más simple que el VSM (sin ecuación de oscilación explícita) cuando no se
necesita emular inercia.

## Procedimiento de diseño (genérico)
1. Determina el punto de operación \( \delta_0 \) y calcula \( K_s=EV_g\cos\delta_0/X_{total} \).
2. Elige \( K_{psc} \) para el tiempo de respuesta de sincronización deseado; verifica que el polo
   \( -K_{psc}K_s \) sea suficientemente negativo.
3. Añade amortiguamiento si hay oscilación (derivada de potencia, similar a \( D\dot\delta \)).
4. Diseña el lazo de tensión/reactiva independiente (controla \( |E| \)).
5. Implementa limitación de corriente coordinada con la magnitud \( E \) y verifica estabilidad en
   todo el rango de SCR.

## Ejemplo de código
```python
def psc_angle(P_ref, P_meas, delta, K_psc, dt):
    delta += K_psc * (P_ref - P_meas) * dt   # integra el error de potencia
    return delta                              # angulo de referencia del convertidor
```

## Parámetros y valores típicos
\( K_{psc} \approx 1\text{–}10 \) rad/s/MW (p.u.). \( \delta_0 < 30\text{–}45° \) para operar lejos
del límite. Tiempo de sincronización: decenas de ms–s.

## Errores comunes
- Operar con \( \delta_0 \) cercano a 90° (margen de par sincronizante mínimo, pérdida de
  sincronismo ante perturbación).
- Acoplar la limitación de corriente sin analizar su efecto sobre \( K_s \) (puede hacer el lazo
  inestable).
- Confundir con droop: el droop varía la frecuencia; el PSC integra directamente el ángulo.

## 3 — Modelo del lazo PSC

**Ángulo de potencia.** La potencia activa e inactiva transferidas a través de una reactancia \( X \) entre el convertidor (tensión \( E \)) y la red (tensión \( V \)) son:
$$ P = \frac{VE}{X}\sin\delta, \qquad Q = \frac{V^2 - VE\cos\delta}{X} $$
donde \( \delta \) es el ángulo de potencia (diferencia de fase entre \( E \) y \( V \)).

**Lazo PSC.** El ángulo se genera integrando el error de potencia activa, sin PLL:
$$ \dot\delta = \omega_{ref} + K_{PSC}(P^* - P) $$
En régimen permanente, \( \dot\delta = \omega_{ref} \) y \( P = P^* \): el ángulo \( \delta \) queda fijo al valor que satisface la curva \( P\text{-}\delta \). La ganancia \( K_{PSC} \) controla la velocidad de sincronización.

**Analogía mecánica.** El lazo PSC es análogo a un regulador de velocidad sin inercia. Comparado con la [[vsm-inercia|máquina síncrona virtual]] que introduce \( J \ddot\delta + D\dot\delta = P^* - P \) (segundo orden), el PSC da un sistema de primer orden: más rápido pero sin la amortiguación natural de la inercia.

**Función de transferencia.** Linearizando en torno al punto de operación \( \delta_0 \), el lazo PSC tiene la función de transferencia de un integrador con ganancia de sincronización:
$$ \frac{\tilde\delta}{\widetilde{P^*}}(s) = \frac{K_{PSC}}{s + K_{PSC}K_s}, \qquad K_s = \frac{VE\cos\delta_0}{X} $$
El sistema es de primer orden con polo real en \( s = -K_{PSC}K_s \), sin oscilación en ausencia de retardos.

## 4 — Estabilidad del PSC en red fuerte y débil

**Red fuerte (SCR alto).** Con \( X \) pequeña, el par sincronizante \( K_s \) es grande: el polo \( -K_{PSC}K_s \) está muy a la izquierda → sistema rápido y bien amortiguado. El PSC se comporta como un droop de frecuencia convencional.

**Red débil (SCR < 2).** Al aumentar la reactancia de red \( X \), la pendiente \( dP/d\delta = K_s \) decrece. Con \( K_s \) pequeño, el polo se acerca al origen, alargando la constante de tiempo de sincronización y haciendo el sistema más sensible a perturbaciones. Si \( \delta_0 \to 90°\), \( \cos\delta_0 \to 0 \) y el par sincronizante se anula: pérdida de sincronismo.

**Amortiguamiento.** Para añadir amortiguamiento sin introducir inercia, se añade un término derivativo sobre la potencia filtrada:
$$ \dot\delta = \omega_{ref} + K_{PSC}(P^* - P) - K_D \dot{P}_{filtrado} $$
El término \( K_D\dot{P} \) actúa como amortiguador viscoso: reduce las oscilaciones ante perturbaciones sin cambiar el régimen permanente.

**Comparación PSC vs VSM:** el PSC es más simple (un integrador + curva \( P\text{-}\delta \)), el VSM añade la inercia virtual \( J \) que proporciona soporte natural de frecuencia ante huecos. A costa de mayor complejidad, el VSM tiene mejor respuesta dinámica ante escalones de carga.

## 5 — PSC en modo isla

**Sin red.** Cuando el convertidor alimenta una carga local (modo isla), la potencia medida \( P \) es la de la carga. El lazo PSC regula automáticamente:
$$ f = f_0 + K_{PSC}(P_{ref} - P_{load}) $$
Si \( P_{load} < P_{ref} \), la frecuencia sube por encima de \( f_0 \) hasta que el balance se restaura.

**Regulación de tensión.** El PSC controla \( \delta \) (y por tanto \( P \)); la tensión \( |E| \) se regula por un lazo externo de tipo Q-V droop:
$$ |E| = V_0 - n_q (Q - Q^*) $$
Ambos lazos son independientes: PSC para la sincronización/potencia activa, Q-V droop para la reactiva y la tensión.

**Multi-inversor en paralelo.** Varios convertidores con PSC operando en paralelo comparten la carga activa de forma proporcional a sus ganancias \( K_{PSC} \), exactamente como el droop de frecuencia convencional. La frecuencia de estado estacionario resulta:
$$ f_{ss} = f_0 - \frac{P_{load}}{\sum_i 1/K_{PSC,i}} \cdot \frac{1}{\sum_i (1/K_{PSC,i})} $$
Para igualdad de reparto con convertidores de igual potencia nominal, se usa \( K_{PSC,i} = K_{PSC,nom} / S_{n,i} \) (en pu).

## 6 — Implementación y sintonización

**Cálculo de \( K_{PSC} \).** Partiendo del coeficiente de droop \( m_p \) en Hz/pu:
$$ K_{PSC} = \frac{2\pi m_p}{V^2 / X} = \frac{2\pi m_p X}{V^2} $$
Tipicamente \( m_p = 1\text{–}5\,\%\) de variación de frecuencia a plena carga, lo que da \( K_{PSC} \approx 1\text{–}10\,\text{rad/s/pu} \).

**Filtro de potencia activa.** La potencia medida debe filtrarse con un LPF de constante de tiempo \( \tau_{pf} \approx 5\text{–}20\,\text{ms} \) para eliminar el rizado de doble frecuencia y el ruido de la conmutación. Un \( \tau_{pf} \) demasiado grande ralentiza el lazo de sincronización; demasiado pequeño introduce rizado en \( \dot\delta \) y puede excitar oscilaciones.

**Protección de corriente.** El lazo de corriente interno (PI en dq o PR en αβ) siempre opera activo, con límite de corriente configurado al 110–130 % de la corriente nominal. El PSC solo genera la referencia de ángulo: no es posible que el convertidor salga de los límites de corriente mientras el lazo interno funcione correctamente.

**Puesta en marcha.** Para evitar el salto de corriente al activar el PSC:
1. Arrancar en modo GFL con PLL activa.
2. Igualar el ángulo generado por el PSC al ángulo de la PLL.
3. Transferir gradualmente la referencia de ángulo del PLL al PSC (rampa de 50–200 ms).

<div class="cfig"><img src="figuras/power-synchronization-control-analisis.png" alt="Curva P-delta red fuerte y debil, respuesta dinamica PSC, comparacion PSC vs VSM y region de estabilidad vs SCR"><div class="cap">Superior izquierdo: curva P-δ — red fuerte (X=0.1 pu) tiene mayor pendiente y mayor par sincronizante que red débil (X=0.5 pu). Superior derecho: respuesta ante escalón de P* — red fuerte converge más rápido que red débil. Inferior izquierdo: PSC vs VSM ante perturbación de frecuencia — el VSM amortigua más lentamente pero con mejor soporte. Inferior derecho: región de estabilidad K_PSC máximo en función del SCR.</div></div>

## Conceptos relacionados
- [[grid-forming-vs-following]] · [[vsm-inercia]] · [[droop-control]] · [[interaccion-pll-red-debil]] · [[ecuacion-oscilacion]]

## Referencias
- Zhang et al., *Power Synchronization Control of Grid-Connected VSC*, IEEE TPWRS 2010.
- Harnefors et al., *Synchronization Stability of Grid-Connected VSCs*, IEEE TPEL 2017.
