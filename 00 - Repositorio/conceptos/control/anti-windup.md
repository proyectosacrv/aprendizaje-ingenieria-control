---
titulo: Anti-windup del integrador
slug: anti-windup
categoria: control
tipo: tecnica
nivel: basico
proyectos: []
objetivos: [evitar la sobrecarga del término integral cuando el actuador satura]
tags: [anti-windup, saturacion, integrador, back-calculation, clamping, cascada, basico, control]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-01
relacionados: [controlador-pid, current-limiting, sintonia-pi-pid, error-regimen-permanente, control-cascada]
referencias:
  - "Aström, Hägglund, PID Controllers, ISA 1995"
  - "Aström, Murray, Feedback Systems, Princeton 2008"
  - "Buso, Mattavelli, Digital Control in Power Electronics, Morgan & Claypool 2006"
---

## Definición
Conjunto de técnicas que **detienen o corrigen la integración** mientras el actuador está
saturado, para que el término integral no acumule un valor enorme ("wind-up") que retrasaría
gravemente la recuperación.

## Fundamento teórico
Al saturar, el lazo queda **abierto**: el error persiste y el integrador sigue cargando aunque la
salida ya no cambie. La recuperación exige "descargar" esa integral, causando gran sobreimpulso.
Esquema de **back-calculation**: se realimenta la diferencia entre la señal calculada \( u \) y la
saturada \( u_{sat} \) al integrador con ganancia \( 1/T_t \):
$$ \dot I = K_i e + \frac{1}{T_t}\,(u_{sat}-u) $$
Con \( u=K_p e + I \). Cuando no hay saturación, \( u_{sat}=u \) y el término extra desaparece.
Alternativas: **clamping** (congelar \( I \) si satura y el error empuja más a la saturación) o
forma **velocidad** (incremental), que es intrínsecamente anti-windup.

<div class="cfig"><img src="figuras/anti-windup-respuesta.png" alt="recuperacion con y sin anti-windup"><div class="cap">Tras una saturación prolongada y un cambio de referencia, sin anti-windup (rojo) el integrador "cargado" retrasa mucho la recuperación; con anti-windup (azul) la salida sigue la nueva referencia de inmediato.</div></div>

## 1 — Por qué satura sin AW dispara el integrador
**Paso 1 — el integrador sin saturar.** El estado integral evoluciona según \( \dot I=K_i\,e(t) \). Mientras el error \( e \) tenga un signo fijo (la referencia está lejos y el actuador no alcanza), \( I \) crece **sin límite**. Integrando con error constante \( e \) durante un tiempo \( t_{sat} \):

$$ I(t_{sat})=I_0+\int_0^{t_{sat}}K_i\,e\,d\tau = I_0 + K_i\,e\,t_{sat} $$

**Paso 2 — magnitud del windup.** Con los datos del ejemplo (\( K_i=315\ \text{s}^{-1} \), \( e=2\ \text{p.u.} \), \( t_{sat}=0{,}08\ \text{s} \)) y \( I_0=0 \):

$$ I=315\times 2\times 0{,}08 = 50{,}4\ \text{p.u.} $$

El integrador acumula **≈ 50 p.u.** aunque la salida ya esté clavada en \( u_{max}=1 \) p.u. desde hace rato: el lazo está **abierto** por la saturación y el integrador "no se entera". Para que la salida vuelva a bajar de la saturación, \( I \) debe **descargarse de 50 hasta ≈ 1**, lo que exige un error de signo contrario sostenido — y mientras tanto la salida permanece saturada, dando un sobreimpulso enorme y una recuperación lentísima.

## 2 — Anti-windup por clamping condicional

El **clamping** es la técnica más simple: se congela el integrador cuando la condición de windup está activa, sin necesidad de realimentar ninguna señal adicional.

**Condición de clamping.** El integrador se detiene (\( \dot I = 0 \)) cuando se cumple **simultáneamente**:
1. La salida está saturada: \( |u_{PI}| \geq u_{max} \)
2. El error sigue empujando en la misma dirección: \( e \cdot (u_{PI} - u_{sat}) > 0 \)

En caso contrario, el integrador evoluciona con normalidad. Formalmente:

$$ \dot I = \begin{cases} K_i\,e & \text{si } |u_{PI}|<u_{max} \text{ o } e\cdot(u_{PI}-u_{sat})\leq 0 \\ 0 & \text{en caso contrario} \end{cases} $$

**Implementación discreta:**
```python
def pi_clamp(e, I, Kp, Ki, umin, umax, dt):
    u_pi = Kp*e + I
    u_sat = min(max(u_pi, umin), umax)
    at_limit = (u_pi >= umax and e > 0) or (u_pi <= umin and e < 0)
    if not at_limit:
        I += Ki*e*dt        # solo integra si no está en windup
    return u_sat, I
```

**Limitación del clamping.** Cuando el sistema sale de saturación, el integrador lleva el valor que tenía en el momento en que se congeló. Si ese valor no coincide con el estado de equilibrio nuevo, la respuesta es "escalada": el sistema salta desde la condición congelada sin suavidad. En la práctica, el integrador se congela en \( I_{frozen} \approx u_{max} - K_p\,e \) (el último valor antes del clamping), que puede ser bastante diferente del valor de equilibrio \( I_{eq} \) tras la transición. Resultado: **el arranque desde la saturación es abrupto**, con un perfil de corriente que sube en escalón en lugar de seguir la rampa deseada. En aplicaciones donde importa la suavidad de la respuesta (arranques de motor, control de tensión), el clamping da un perfil peor que el back-calculation.

## 3 — Anti-windup por back-calculation
**Paso 1 — añadir la realimentación de saturación.** Se realimenta la diferencia \( (u_{sat}-u) \) al integrador con ganancia \( 1/T_t \):

$$ \dot I = K_i\,e + \frac{1}{T_t}\,(u_{sat}-u),\qquad u=K_p e + I $$

Mientras **no** hay saturación \( u_{sat}=u \), el término extra es 0 y el PI funciona normal. En **saturación**, \( u_{sat}=u_{max} \) está fijo mientras \( u=K_p e+I \) sigue creciendo con \( I \): el término \( (u_{sat}-u) \) se hace negativo y **resta** a \( \dot I \).

**Paso 2 — el integrador busca un equilibrio.** El estado deja de crecer cuando \( \dot I=0 \). Sustituyendo \( u=K_p e+I \) en \( u_{sat}-u=u_{max}-K_p e-I \):

$$ \dot I = K_i\,e + \frac{1}{T_t}\,(u_{max}-K_p e - I)=0 $$

**Paso 3 — despejar el valor acotado.** Multiplicando por \( T_t \) y despejando \( I \):

$$ K_i e\,T_t + u_{max}-K_p e - I = 0 \;\Longrightarrow\; \boxed{\;I_{eq}=u_{max}-K_p e + K_i\,T_t\,e\;} $$

A diferencia del caso sin AW (donde \( I\to\infty \)), aquí \( I \) se estabiliza en un valor **finito** dictado por \( u_{max} \): el integrador se "ancla" cerca de lo que el actuador puede dar, no de lo que el error pide.

**Ti óptimo para el lazo de corriente.** La constante de tiempo óptima para des-windupado en el lazo de corriente de un convertidor es la **constante de tiempo eléctrica**:

$$ T_t^* = \frac{L}{R} $$

Con este valor, la dinámica del des-windupado coincide con la dinámica natural de la planta. Si \( T_t < L/R \) el des-windupado es más agresivo (útil si los límites de corriente se activan brevemente), pero amplifica el ruido en la acción de control. Si \( T_t > L/R \) el des-windupado es lento y puede dejar un sobreimpulso residual.

**Comparativa clamping vs back-calculation.** Ambas técnicas evitan el crecimiento ilimitado del integrador, pero difieren en la calidad de la transición:

| Criterio | Clamping | Back-calculation |
|---|---|---|
| Implementación | Muy simple | Simple |
| Estado de \(I\) al salir de saturación | Valor congelado (puede ser incorrecto) | Valor anclado a \(u_{max}\) (suave) |
| Sobreimpulso residual | 10–20% (depende del punto congelado) | <5% con \(T_t = L/R\) |
| Sensibilidad al ruido | Baja | Media (decrece con \(T_t\) grande) |
| Recomendado para | Lazos lentos, prototipos | Lazos de corriente, producción |

<div class="cfig"><img src="figuras/anti-windup-analisis.png" alt="analisis comparativo anti-windup"><div class="cap">(a) Comparativa de $i_d(t)$ ante escalón 0→1000 A con $u_{max}$=800 V: sin AW el integrador se dispara y tarda décenas de ms en recuperarse; clamping mejora pero da un perfil abrupto; back-calculation con $T_i^{av}=L/R$ da la respuesta más suave. (b) Estado del integrador $\xi(t)$: sin AW se desborda; back-calc se ancla a $u_{max}$. (c) Efecto de $T_i^{av}$: valor pequeño→agresivo pero puede oscilar; valor grande→lento. (d) Cascada tensión→corriente: sin AW en el lazo externo, $V_{dc}$ sufre una caída sostenida porque el PI de tensión acumula indefinidamente.</div></div>

## 4 — Windup en sistemas en cascada: lazo de tensión → corriente

En un convertidor con control en cascada, el lazo de **tensión** genera la referencia de corriente \( i_d^* \) y el lazo de **corriente** la sigue. Si la corriente se limita (\( i_d^* \) se recorta por un saturador), el PI de tensión no "ve" que su salida está siendo recortada: su integrador acumula indefinidamente aunque la acción de control no pueda crecer más.

**Mecanismo del windup en cascada.**
1. El bus DC sufre una caída (p.ej. escalón de carga).
2. El PI de tensión genera \( i_d^* \) muy grande.
3. El saturador de corriente recorta \( i_d^* \) a \( i_{d,max} \).
4. El PI de tensión sigue integrando el error de tensión sin saber que su salida está limitada.
5. Cuando la tensión se recupera, el integrador del PI de tensión tiene un valor enorme → sobreimpulso de tensión.

**Solución: tracking anti-windup (AW de tracking).** El lazo de tensión recibe realimentación de la diferencia entre la referencia calculada \( i_d^* \) y la referencia realmente aplicada \( i_{d,lim} \):

$$ \dot I_v = K_{iv}\,e_v + \frac{1}{T_{t,v}}\,(i_{d,lim} - i_d^*) $$

**Dimensionado de \( T_{t,v} \).** El AW del lazo externo debe ser más lento que el lazo interno (para no interferir con la dinámica del lazo de corriente). Una regla práctica es:

$$ T_{t,v} \approx \frac{T_i^{corriente}}{5} \quad\text{a}\quad \frac{T_i^{corriente}}{3} $$

Con \( T_i^{corriente} = L/R = 40\ \text{ms} \) (parámetros de ejemplo), se elige \( T_{t,v} \approx 8\text{–}13\ \text{ms} \).

**Regla de diseño.** El criterio general para AW en cascada es que el des-windupado del lazo externo sea al menos 3–5 veces más lento que la dinámica del lazo interno. Si es más rápido, el AW externo puede excitar el lazo interno.

## 5 — Windup en la PLL: pérdida de enganche

La PLL (Phase-Locked Loop) usa un PI para estimar la frecuencia angular \( \hat\omega \) de la red. Si el sistema se desengancha (p.ej., hueco de tensión profundo, fallo de red), el error de ángulo \( \theta_{err} \) puede crecer sin límite y el integrador del PI de la PLL acumula, haciendo que \( \hat\omega \) se aleje rápidamente de \( \omega_0 \).

**Síntoma.** Al reengancharse, \( \hat\omega \) puede estar tan lejos de \( \omega_0 \) que el lazo necesita varios segundos para volver a la frecuencia nominal — tiempo durante el cual el convertidor actúa sobre una referencia de ángulo errónea y puede inyectar corrientes distorsionadas o perder sincronismo.

**Anti-windup en la PLL: limitación de \( \hat\omega \).** La solución habitual es limitar la frecuencia estimada a un rango tolerable:

$$ \hat\omega \in [\omega_0 - \Delta\omega_{max},\; \omega_0 + \Delta\omega_{max}] $$

y aplicar back-calculation sobre el integrador del PI de la PLL con este límite. El integrador no puede empujar \( \hat\omega \) más allá del rango incluso si el error de ángulo persiste.

**Dimensionado de \( \Delta\omega_{max} \).** En sistemas de distribución y transmisión, la variación de frecuencia está regulada. La norma europea (RfG) limita la frecuencia entre 47–52 Hz. Con un margen adicional de seguridad, se dimensiona:

$$ \Delta\omega_{max} = 2\pi\times5\ \text{rad/s} \quad(\text{equivalente a}\ \pm5\ \text{Hz sobre }50\ \text{Hz}) $$

Este margen cubre cualquier transitorio realista y garantiza que la PLL no sale de su rango operativo durante fallas de corta duración (\( < 150\ \text{ms} \) según EN 50160).

## 6 — Diseño iterativo: anti-windup para lazo de corriente

Parámetros del lazo: \( L=2\ \text{mH} \), \( R=50\ \text{m}\Omega \), \( \alpha_c=2\pi\cdot750\ \text{Hz} \), \( u_{max}=800\ \text{V} \), \( i_{d,target}=1000\ \text{A} \), \( T_s=100\ \mu\text{s} \).

De la sintonía por polo de cancelación: \( K_p = \alpha_c L = 9{,}42\ \text{V/A} \), \( K_i = \alpha_c R = 0{,}236\ \text{V/(A·s)} \). La constante de tiempo eléctrica \( L/R = 40\ \text{ms} \).

**Iteración 0 — sin anti-windup.**
El escalón de 0 a 1000 A con \( u_{max}=800\ \text{V} \) satura el convertidor durante \( t_{sat} \approx 35\ \text{ms} \).
El integrador acumula \( \xi \approx K_i \cdot 1000 \cdot 0{,}035 \approx 8{,}3\ \text{V}\cdot\text{s} \), equivalente a más de 10 veces \( u_{max} \).
Sobreimpulso al recuperar: **≈40 %** (\( i_d \) llega a 1400 A).

**Iteración 1 — clamping.**
El integrador se congela cuando \( u_{PI} > u_{max} \) y \( e > 0 \).
Sobreimpulso reducido a **≈15 %** (depende del estado congelado).
La respuesta es brusca: la corriente sube en escalón al salir de la saturación.

**Iteración 2 — back-calculation con \( T_t = L/R = 40\ \text{ms} \).**
El integrador se ancla en \( I_{eq} \approx u_{max} - K_p e \approx 790\ \text{V} \) durante la saturación.
Al salir de la saturación, la corriente sigue una rampa suave.
Sobreimpulso: **≈5 %**, tiempo de establecimiento: \( t_s \approx 12\ \text{ms} \) ✓

**Iteración 3 — verificar ruido.**
Con \( T_t = 10\ \text{ms} \) (más agresivo): el des-windupado es más rápido pero el ruido de medida de \( i_d \) produce una fluctuación de ±20 V en la acción de control.
Se mantiene \( T_t = L/R = 40\ \text{ms} \) como compromiso entre velocidad y ruido.

| Iteración | Técnica | \(T_t\) [ms] | Sobreimpulso | \(t_s\) [ms] | Observación |
|---|---|---|---|---|---|
| 0 | Sin AW | — | ~40 % | >100 | Inaceptable |
| 1 | Clamping | — | ~15 % | ~40 | Transición brusca |
| 2 | Back-calc | 40 (L/R) | ~5 % | ~12 | Aceptable ✓ |
| 3 | Back-calc | 10 | ~3 % | ~8 | Ruido ↑ en \(u\) |

## Cuándo y por qué se usa
En todo lazo PI con límites físicos: corriente, tensión de modulación, par. Imprescindible junto
al [[current-limiting]] de convertidores, donde la referencia se recorta con frecuencia. En
sistemas en cascada, el AW debe implementarse en **cada lazo**, no solo en el más interno.

## Procedimiento (genérico)
1. Modela el saturador real (límites de \( u \)).
2. Elige el esquema: back-calculation para lazos de corriente y tensión; clamping solo si el recursos computacionales son muy limitados.
3. Sintoniza \( T_t \): para lazos eléctricos usar \( T_t = L/R \); para lazos mecánicos \( T_t \approx J/(B) \).
4. En cascada, añade AW de tracking en el lazo externo con \( T_{t,ext} \approx 3\text{–}5\,T_{t,int} \).
5. Verifica recuperación sin sobreimpulso tras una saturación prolongada.

## Ejemplo de código
```python
def pi_aw(e, I, Kp, Ki, Tt, umin, umax, dt):
    u = Kp*e + I
    usat = min(max(u, umin), umax)
    I += (Ki*e + (usat-u)/Tt)*dt        # back-calculation
    return usat, I

def pi_clamp(e, I, Kp, Ki, umin, umax, dt):
    u_pi = Kp*e + I
    u_sat = min(max(u_pi, umin), umax)
    at_limit = (u_pi >= umax and e > 0) or (u_pi <= umin and e < 0)
    if not at_limit:
        I += Ki*e*dt
    return u_sat, I
```

## Parámetros y valores típicos
- \( T_t \) back-calculation: \( L/R \) para lazo de corriente; \( \sqrt{T_i T_d} \) para PID genérico.
- \( T_t \) en cascada (lazo externo): 3–5 veces el \( T_t \) del lazo interno.
- Límite PLL: \( \Delta\omega_{max} = 2\pi\cdot5\ \text{rad/s} \) (±5 Hz).

## Errores comunes
- Saturar la salida pero seguir integrando el error completo (windup clásico).
- Poner \( T_t \) sin relación con la dinámica del lazo.
- Olvidar el AW en el lazo externo de una cascada.
- En la PLL: no limitar \( \hat\omega \) → pierde enganche tras un hueco profundo.

## Conceptos relacionados
- [[controlador-pid]] · [[current-limiting]] · [[sintonia-pi-pid]] · [[error-regimen-permanente]] · [[control-cascada]]

## Referencias
- Aström, Hägglund, *PID Controllers*, 1995.
- Aström, Murray, *Feedback Systems*, 2008.
- Buso, Mattavelli, *Digital Control in Power Electronics*, 2006.
