---
titulo: Compensación de retardo (Smith predictor, retardo digital)
slug: compensacion-retardo
categoria: control
tipo: tecnica
nivel: intermedio
proyectos: []
objetivos: [recuperar margen y desempeño perdidos por el retardo de cómputo y PWM]
tags: [retardo, smith-predictor, computo, pwm, prediccion, fase, lead, intermedio, control]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-01
relacionados: [discretizacion-controladores, margenes-estabilidad, desacoplo-dq, fenomenos-oscilatorios-red, controlador-pid]
referencias:
  - "Buso, Mattavelli, Digital Control in Power Electronics, Morgan & Claypool 2006"
  - "Åström, Hägglund, Advanced PID Control, ISA 2006"
  - "Franklin, Powell, Emami-Naeini, Feedback Control of Dynamic Systems, 2015"
---

## Definición
Conjunto de técnicas para **contrarrestar el efecto desestabilizador del retardo** del control
digital (cómputo + modulación), que resta fase y limita el ancho de banda. Incluye la predicción de
estados y el **predictor de Smith** para retardos dominantes.

## Fundamento teórico
En un convertidor digital el retardo total es típicamente \( T_d\approx1.5\,T_s \) (un periodo de
cómputo + medio de PWM/ZOH). Su efecto en frecuencia es fase pura:
$$ e^{-sT_d}\ \Rightarrow\ \Delta\phi(\omega)=-\omega T_d $$
que **resta margen de fase** proporcional a \( \omega_c \) y empuja la impedancia hacia la
no-pasividad ([[fenomenos-oscilatorios-red|estabilidad armónica]]). Compensaciones:
- **Predicción de estados / corriente:** estimar el valor de la variable \( T_d \) por delante
  (modelo del filtro, observador) y controlar sobre la predicción → cancela el retardo dentro de la
  banda del modelo.
- **Predictor de Smith:** para una planta \( G(s)e^{-sT_d} \), realimenta una predicción **sin
  retardo** usando un modelo \( \hat G \):
  $$ C_{eq}(s)=\frac{C(s)}{1+C(s)\hat G(s)\,(1-e^{-sT_d})} $$
  Así el controlador "ve" \( \hat G(s) \) sin retardo y se sintoniza como si no lo hubiera; el
  retardo queda fuera del lazo característico (si el modelo es exacto).
- **Adelanto de ángulo:** en dq, rotar la referencia/medida \( \omega T_d \) compensa el giro del
  marco durante el retardo (mejora el [[desacoplo-dq|desacoplo]]).

Limitación: todas dependen de la **exactitud del modelo**; un \( \hat G \) o \( T_d \) erróneo
reintroduce error y puede empeorar la robustez.

<div class="cfig"><img src="figuras/compensacion-retardo-fase.png" alt="fase restada por el retardo en funcion de la frecuencia"><div class="cap">El retardo $T_d=1.5\,T_s$ resta fase pura $\Delta\phi=-\omega T_d$, que crece linealmente con la frecuencia. A la frecuencia de cruce $f_c=f_s/10$ ya se pierden ~54° de margen: por eso en lazos rápidos hay que compensarlo (predicción de estados, Smith, adelanto de ángulo).</div></div>

## 1 — De dónde sale \( e^{-sT_d} \) y la pérdida de fase \( -\omega T_d \)
**Paso 1 — el retardo en el tiempo.** El control digital aplica la acción calculada con un retraso \( T_d \): la medida del instante \( t \) no se actúa hasta \( t+T_d \). En el dominio del tiempo, retrasar una señal \( x(t) \) en \( T_d \) es \( x(t-T_d) \).

**Paso 2 — su transformada de Laplace.** Aplicando la definición \( \mathcal{L}\{x(t-T_d)\}=\int_0^\infty x(t-T_d)e^{-st}\,dt \); con el cambio \( \tau=t-T_d \):

$$ \int_{-T_d}^\infty x(\tau)\,e^{-s(\tau+T_d)}\,d\tau = e^{-sT_d}\!\int_0^\infty x(\tau)e^{-s\tau}\,d\tau = e^{-sT_d}\,X(s) $$

$$ \boxed{\;\text{retraso }T_d \;\Longleftrightarrow\; \text{factor } e^{-sT_d}\;} $$

**Paso 3 — composición del retardo total.** El retardo lo forman el cómputo (un periodo \( T_s \): la muestra de un ciclo se aplica al siguiente) más la actualización del PWM/ZOH (que en promedio retrasa medio periodo, \( T_s/2 \)):

$$ T_d=T_s+\tfrac12 T_s=\tfrac32 T_s\approx1.5\,T_s $$

**Paso 4 — efecto en frecuencia: fase pura.** Evaluando en \( s=j\omega \): \( e^{-j\omega T_d} \) tiene módulo \( |e^{-j\omega T_d}|=1 \) (no atenúa) y argumento

$$ \angle e^{-j\omega T_d}=-\omega T_d \quad\Longrightarrow\quad \Delta\phi(\omega)=-\omega T_d $$

Es **fase pura negativa que crece linealmente** con \( \omega \): a baja frecuencia apenas se nota, pero en el cruce \( \omega_c \) resta \( \omega_c T_d \) directamente del margen de fase.

**Paso 5 — números.** Con \( T_d=1.5\,T_s \) y un cruce ambicioso \( f_c=f_s/10 \):

$$ \Delta\phi=-\omega_c T_d=-2\pi f_c\cdot1.5T_s=-2\pi\frac{f_s}{10}\cdot\frac{1.5}{f_s}=-2\pi\cdot0.15=-54^\circ $$

Se pierden 54° de margen solo por el retardo — inadmisible sin compensar. Esto motiva la compensación.

## 2 — Los 1.5·Ts de retardo digital: de dónde vienen

El valor \( T_d = 1.5\,T_s \) no es un resultado arbitrario: es la composición de **dos retardos físicos distintos** del sistema digital.

**Retardo de cómputo: \( T_s \).** En la implementación estándar, el DSP o FPGA realiza el ciclo:
1. Al inicio del periodo \( k \): captura la medida \( i_d[k] \).
2. Durante el periodo \( k \): ejecuta el algoritmo de control → calcula \( u[k] \).
3. Al inicio del periodo \( k+1 \): aplica \( u[k] \) al modulador.

La acción calculada con la muestra de \( t=kT_s \) no se aplica hasta \( t=(k+1)T_s \): **un periodo completo de retardo**.

**Retardo del PWM/ZOH: \( T_s/2 \).** El convertidor de potencia aplica la tensión media en cada periodo mediante modulación por anchura de pulso (PWM). El valor \( u[k] \) actualiza el ciclo de trabajo al inicio del periodo, pero la tensión media que produce ese ciclo se promedia a lo largo de todo el periodo de PWM. Para una señal que varía lentamente respecto a \( T_s \), este efecto es equivalente a un retardo adicional de medio periodo:

$$ \text{ZOH}: \quad G_{ZOH}(s)=\frac{1-e^{-sT_s}}{s}\approx e^{-sT_s/2}\;\text{para }\omega T_s\ll1 $$

**Composición total.** Sumando ambos retardos:

$$ \boxed{T_d = T_s + \frac{T_s}{2} = \frac{3}{2}T_s = 1.5\,T_s} $$

**Efecto en Bode.** El factor \( e^{-j\omega T_d} \) solo afecta a la fase, no a la magnitud: \( |e^{-j\omega T_d}|=1 \) para todo \( \omega \). La pérdida de margen de fase es:

$$ \Delta PM = -\omega_c\,T_d \cdot \frac{180°}{\pi} \quad\text{(en grados)} $$

**Ejemplo numérico.** Con \( \omega_c = 2\pi\cdot1000\ \text{rad/s} \) y \( T_s = 100\ \mu\text{s} \):

$$ T_d = 1.5\times10^{-4}\ \text{s} \quad\Longrightarrow\quad \Delta PM = -2\pi\cdot1000\cdot1.5\times10^{-4}\cdot\frac{180}{\pi} = -54° $$

Un lazo diseñado con PM = 60° sin contar el retardo tiene en realidad PM = 60° - 54° = 6°: **prácticamente inestable**.

## 3 — Compensación por adelanto de fase

El compensador **lead** (adelanto de fase) es un filtro pasivo de primer orden que aporta fase positiva en una banda de frecuencias centrada en \( \omega_c \):

$$ C_{lead}(s) = \frac{1+s\tau_z}{1+s\tau_p}, \qquad \tau_z > \tau_p > 0 $$

**Fase aportada en el cruce.** Evaluando en \( s=j\omega_c \):

$$ \angle C_{lead}(j\omega_c) = \arctan(\omega_c\tau_z) - \arctan(\omega_c\tau_p) = \Delta\phi_{lead} $$

**Diseño para máxima fase en \( \omega_c \).** El parámetro \( \alpha = \tau_z/\tau_p \) controla la fase máxima:

$$ \phi_{max} = \arcsin\!\left(\frac{\alpha-1}{\alpha+1}\right) \quad\Rightarrow\quad \boxed{\alpha = \frac{1+\sin\phi_{max}}{1-\sin\phi_{max}}} $$

Los tiempos se eligen para que \( \phi_{max} \) ocurra exactamente en \( \omega_c \):

$$ \tau_z = \frac{\sqrt{\alpha}}{\omega_c}, \qquad \tau_p = \frac{1}{\sqrt{\alpha}\,\omega_c} $$

**El adelanto también sube la ganancia.** En \( \omega_c \), el lead aporta una magnitud \( |C_{lead}(j\omega_c)| > 1 \). Para mantener el mismo cruce de ganancia, se reduce \( K_p \) del PI por un factor \( 1/\sqrt{\alpha} \):

$$ K_p^{lead} = \frac{K_p}{\sqrt{\alpha}} $$

**Limitaciones prácticas.** La fase máxima de un lead de primer orden es 90° (\( \alpha\to\infty \)), pero en la práctica \( \alpha < 10 \) para evitar amplificación excesiva del ruido de medida en las frecuencias altas (el lead sube la ganancia a alta frecuencia por su polo en \( 1/\tau_p \)). Para \( \Delta\phi_{lead} \leq 30° \) se recomienda \( \alpha \leq 3 \). Para compensar más de 30° se usan dos leads en cascada o se reduce directamente \( \omega_c \).

## 4 — El predictor de Smith: para retardos grandes conocidos

**Paso 1 — la planta con retardo.** La planta real es \( G(s)\,e^{-sT_d} \). Cerrar el lazo con un controlador \( C(s) \) da la característica \( 1+C(s)G(s)e^{-sT_d}=0 \): el \( e^{-sT_d} \) está **dentro**, y es lo que come el margen.

**Paso 2 — la idea: predecir la salida sin retardo.** Con un modelo \( \hat G(s) \) de la planta (sin retardo), se construye en paralelo una estimación de cuánto valdría la salida si no hubiera retardo. La señal que se realimenta al controlador es la salida medida **corregida** con la diferencia entre el modelo sin retardo \( \hat G \) y el modelo con retardo \( \hat G\,e^{-sT_d} \).

**Paso 3 — el controlador equivalente.** Esa estructura es algebraicamente equivalente a sustituir \( C(s) \) por

$$ \boxed{\;C_{eq}(s)=\frac{C(s)}{1+C(s)\,\hat G(s)\,(1-e^{-sT_d})}\;} $$

**Paso 4 — qué ve el lazo si el modelo es exacto.** Si \( \hat G=G \), la función de transferencia de lazo cerrado resulta

$$ T(s)=\frac{C_{eq}\,G\,e^{-sT_d}}{1+C_{eq}\,G\,e^{-sT_d}}=\frac{C\,G}{1+C\,G}\;e^{-sT_d} $$

El denominador característico es \( 1+C(s)G(s) \): **el \( e^{-sT_d} \) ha salido del lazo**. El controlador se sintoniza sobre \( G(s) \) sin retardo (margen completo).

**Por qué no se usa en convertidores.** El predictor de Smith requiere un modelo exacto del retardo \( T_d \) y de la planta \( G(s) \). En convertidores de potencia:
- El retardo \( T_d = 1.5T_s \) es pequeño (\( <200\ \mu\text{s} \)) y bien conocido.
- La planta \( G_p(s) = 1/(Ls+R) \) es de primer orden, fácil de modelar.
- La predicción de estados (un paso adelante) es equivalente al Smith para retardo de un paso y es más simple de implementar sin el filtro de modelo en paralelo.

El Smith es útil cuando el retardo domina la dinámica (\( T_d \gg L/R \)), que no es el caso en lazos de corriente de convertidores donde \( T_d \approx 0.15\ \text{ms} \ll L/R = 40\ \text{ms} \).

## 5 — Compensación por predicción en el tiempo

En lugar de compensar en frecuencia, se puede **predecir el valor futuro** de la variable controlada y usarlo como entrada al controlador.

**Predicción de un paso.** Para la planta \( L\,\dot i_d = v_{conv} - e_d - R\,i_d \), discretizando por Euler:

$$ i_d[k+1] \approx i_d[k] + \frac{T_s}{L}\,(v_{conv}[k] - e_d[k] - R\,i_d[k]) $$

El controlador actúa sobre la predicción \( \hat i_d[k+1] \) en lugar de sobre \( i_d[k] \): equivale a eliminar un \( T_s \) del retardo total, dejando solo el medio periodo del PWM.

**Implementación:**
```python
def predict_id(i_d, v_conv, e_d, L, R, Ts):
    """Predicción de corriente un paso adelante (modelo Euler)."""
    return i_d + Ts/L * (v_conv - e_d - R*i_d)

# En el bucle de control:
i_d_pred = predict_id(i_d_meas, u_prev, e_d_meas, L, R, Ts)
e_pred = i_d_ref - i_d_pred          # error sobre la predicción
u_new  = pi.update(e_pred)           # PI actúa sobre la predicción
```

**Limitación: amplificación del ruido.** La predicción implica una derivada numérica de \( i_d \): el término \( (v_{conv} - e_d - R\,i_d)/L \) es sensible a cualquier ruido de medida en \( i_d \) o \( e_d \). Con \( L = 2\ \text{mH} \), un ruido de 1 A en \( i_d \) genera un error de predicción de:

$$ \delta\hat i_d \approx \frac{T_s\cdot R}{L}\delta i_d = \frac{100\times10^{-6}\times0.05}{2\times10^{-3}}\times1 = 2.5\ \text{mA} $$

Este nivel es tolerable. Pero si \( e_d \) se mide con mayor ruido (p.ej., tensión de bus DC), la predicción puede degradarse. En ese caso se filtra \( e_d \) con un polo a 2–5 veces \( \omega_c \) antes de usarla en la predicción.

## 6 — Diseño iterativo: compensar retardo en lazo de corriente

Parámetros: \( L=2\ \text{mH} \), \( R=50\ \text{m}\Omega \), \( T_s=100\ \mu\text{s} \), \( T_d=150\ \mu\text{s} \).

**Iteración 0 — diseño sin contar el retardo.**
Objetivo inicial: \( \alpha_c = 2\pi\cdot1000\ \text{Hz} \).
Sin retardo: \( PM = 90° \) (lazo de primer orden con PI de cancelación de polo).
Con retardo real \( T_d=1.5T_s \): \( \Delta PM = -\omega_c T_d\cdot\frac{180°}{\pi} = -2\pi\cdot1000\cdot150\times10^{-6}\cdot\frac{180°}{\pi} = -54° \).
\( PM_{real} = 90° - 54° = 36° \) ✗ (insuficiente, riesgo de sobreoscilación >30 %).

**Iteración 1 — reducir \( \alpha_c \) para recuperar margen.**
Reducir a \( \alpha_c = 2\pi\cdot750\ \text{Hz} \).
Pérdida de fase: \( \Delta PM = -2\pi\cdot750\cdot1.5\times10^{-4}\cdot\frac{180°}{\pi} = -40° \).
\( PM_{real} = 90° - 40° = 50° \) ✓ (aceptable, sobreoscilación <15 %).
Contra: el ancho de banda se ha reducido un 25 %.

**Iteración 2 — añadir lead para recuperar ancho de banda.**
Objetivo: aportar \( \Delta\phi_{lead} = 15° \) en \( f_c = 750\ \text{Hz} \).
\( \alpha = (1+\sin15°)/(1-\sin15°) = (1+0.259)/(1-0.259) = 1.70 \).
\( \tau_z = \sqrt{1.70}/(2\pi\cdot750) = 275\ \mu\text{s} \), \( \tau_p = 162\ \mu\text{s} \).
Reducir \( K_p \) por \( 1/\sqrt{1.70} = 0.77 \): \( K_p^{lead} = 0.77 K_p \).
\( PM_{real} = 50° + 15° = 65° \) ✓. Ahora se puede subir \( \alpha_c \) a \( 2\pi\cdot900\ \text{Hz} \) manteniendo PM > 45°.

**Iteración 3 — verificar robustez a variación de L.**
Con \( L+20\% = 2.4\ \text{mH} \): \( K_p \) del PI era diseñado para \( L=2\ \text{mH} \), ahora la ganancia de lazo baja un 17 %.
El cruce se desplaza de 750 Hz a ≈ 620 Hz. La pérdida adicional de fase: \( \Delta = -2\pi\cdot(750-620)\cdot150\times10^{-6}\cdot\frac{180°}{\pi} \approx -7° \).
\( PM_{min} = 65° - 7° = 58° \) ✓ → el diseño es robusto a variaciones de L de ±20 %.

<div class="cfig"><img src="figuras/compensacion-retardo-analisis.png" alt="analisis compensacion retardo"><div class="cap">(a) Bode del lazo de corriente: sin retardo PM=90°; con retardo 1.5Ts PM≈50°; con compensador lead PM≈65°. (b) Escalón de $i_d$=100 A: el retardo introduce sobreoscilación; el lead la reduce. (c) Bode del compensador lead solo: aporta Δφ≈15° en $f_c$ a costa de subir la ganancia (se corrige reduciendo Kp). (d) PM vs $\tau/T_s$: la línea $\alpha_c T_s=0.3$ (cruce a 750 Hz con Ts=100µs) marca el límite práctico de diseño sin compensación.</div></div>

| Iteración | \(\alpha_c\) [Hz] | Lead | \(PM\) [°] | Sobreoscilación | Observación |
|---|---|---|---|---|---|
| 0 | 1000 | No | 36 | >30% | ✗ Inestable en práctica |
| 1 | 750  | No | 50 | ~15% | ✓ Conservador |
| 2 | 750  | Sí (Δφ=15°) | 65 | ~5% | ✓ Bueno |
| 3 | 900  | Sí | 58 | ~8% | ✓ Más rápido |

## Cuándo y por qué se usa
En lazos rápidos (corriente) con \( f_c \) cercano a \( f_s/10 \), donde el retardo ya cuesta varios
grados de margen; en convertidores de alta frecuencia de cruce; y para mejorar la pasividad de la
impedancia a alta frecuencia.

## Procedimiento de diseño (genérico)
1. Cuantifica \( T_d \) real (cómputo + actualización PWM) y su \( \Delta\phi \) en \( \omega_c \).
2. Decide técnica: predicción de estados (robusta, sencilla) o Smith (retardos grandes).
3. Si usas lead: calcula \( \alpha \) para la fase deseada, ajusta \( K_p \) para mantener el cruce.
4. Re-evalúa [[margenes-estabilidad|márgenes]] e impedancia con el compensador.
5. Verifica robustez a variación de \( L \) ±20 %.
6. Discretiza con cuidado ([[discretizacion-controladores]]).

## Ejemplo de código
```python
import numpy as np

def angle_advance(theta, w, Td):
    """Adelanto de angulo en dq para compensar el retardo de computo+PWM."""
    return theta + w*Td

def lead_discrete(e, e_prev, tau_z, tau_p, Ts):
    """Compensador lead discreto (Euler adelante)."""
    return (e + tau_z/Ts*(e - e_prev)) / (1 + tau_p/Ts)

def predict_id(i_d, v_conv, e_d, L, R, Ts):
    """Prediccion de corriente un paso adelante."""
    return i_d + Ts/L * (v_conv - e_d - R*i_d)
```

## Parámetros y valores típicos
\( T_d\approx1.5\,T_s \). Lead: \( \alpha=(1+\sin\Delta\phi)/(1-\sin\Delta\phi) \), \( \Delta\phi\leq30° \) por etapa.
Regla práctica: \( \alpha_c T_s \leq 0.3 \) sin compensación; hasta \( 0.5 \) con lead.

## Errores comunes
- Despreciar \( T_d \) al diseñar (márgenes optimistas que no se cumplen en hardware).
- Predictor de Smith con modelo pobre → peor que sin compensar.
- Sobre-compensar (lead excesivo) → ruido amplificado a alta frecuencia.
- No reducir \( K_p \) tras añadir el lead → cruce sube, margen baja de nuevo.

## Conceptos relacionados
- [[discretizacion-controladores]] · [[margenes-estabilidad]] · [[desacoplo-dq]] · [[fenomenos-oscilatorios-red|estabilidad armónica]] · [[controlador-pid]]

## Referencias
- Buso, Mattavelli, *Digital Control in Power Electronics*, 2006.
- Åström, Hägglund, *Advanced PID Control*, 2006.
- Franklin, Powell, Emami-Naeini, *Feedback Control of Dynamic Systems*, 2015.
