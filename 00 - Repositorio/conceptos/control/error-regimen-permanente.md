---
titulo: Error en régimen permanente y tipo de sistema
slug: error-regimen-permanente
categoria: control
tipo: concepto
nivel: basico
proyectos: []
objetivos: [predecir el error estacionario según el número de integradores del lazo]
tags: [error-permanente, tipo-sistema, Kp, Kv, Ka, basico, control, resonante, perturbacion, trade-off]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-01
relacionados: [realimentacion, metricas-desempeno, controlador-pid, funcion-transferencia, anti-windup, funciones-sensibilidad]
referencias:
  - "Ogata, Ingeniería de Control Moderna, Pearson"
  - "Franklin, Powell, Feedback Control of Dynamic Systems, Pearson"
---

## Definición
Error que persiste entre referencia y salida cuando el transitorio se ha extinguido. Depende del
**tipo de sistema** (número de integradores \( 1/s \) en la ganancia de lazo) y de la clase de
entrada.

## Fundamento teórico
Por el teorema del valor final, para realimentación unitaria con lazo \( L(s) \):
$$ e_{ss}=\lim_{s\to0} \frac{s\,R(s)}{1+L(s)} $$
Se definen las **constantes de error estático**:
$$ K_p=\lim_{s\to0}L(s),\quad K_v=\lim_{s\to0}sL(s),\quad K_a=\lim_{s\to0}s^2L(s) $$

| Tipo (nº integradores) | Escalón \(1/s\) | Rampa \(1/s^2\) | Parábola \(1/s^3\) |
|---|---|---|---|
| 0 | \(1/(1+K_p)\) | \(\infty\) | \(\infty\) |
| 1 | 0 | \(1/K_v\) | \(\infty\) |
| 2 | 0 | 0 | \(1/K_a\) |

Cada integrador añade un tipo → anula el error ante una entrada de un orden más alto, **a costa**
de margen de fase (90° menos por integrador).

<div class="cfig"><img src="figuras/error-regimen-permanente-step.png" alt="error en regimen tipo 0 vs tipo 1"><div class="cap">Ante un escalón, el sistema tipo 0 (solo P) deja un error en régimen e_ss; el tipo 1 (con integrador) lo anula, a costa de más sobreimpulso / menos margen de fase.</div></div>

## 1 — Error ante escalón: por qué el integrador lo anula
**Paso 1 — punto de partida.** El error en el dominio de Laplace es \( E(s)=S(s)\,R(s)=\dfrac{R(s)}{1+L(s)} \) (sensibilidad, ver [[realimentacion]]). El **teorema del valor final** da su valor estacionario \( e_{ss}=\lim_{t\to\infty}e(t)=\lim_{s\to 0}sE(s) \):

$$ e_{ss}=\lim_{s\to0}\frac{s\,R(s)}{1+L(s)} $$

**Paso 2 — entrada escalón.** Para un escalón \( r(t)=1 \), \( R(s)=1/s \). El \( s \) del teorema cancela el \( 1/s \) del escalón:

$$ e_{ss}=\lim_{s\to0}\frac{s\,(1/s)}{1+L(s)}=\frac{1}{1+\lim_{s\to0}L(s)}=\frac{1}{1+K_p} $$

donde \( K_p=\lim_{s\to0}L(s) \) es la constante de error de posición.

**Paso 3 — tipo 0 vs tipo 1.** Si el lazo **no** tiene integrador (tipo 0), \( L(0)=K_p \) es un número finito y \( e_{ss}=\dfrac{1}{1+K_p}\neq 0 \): queda error. Si el lazo tiene un integrador \( 1/s \) (tipo 1, p.ej. un PI), al evaluar \( s\to 0 \):

$$ K_p=\lim_{s\to0}\frac{K(\cdots)}{s(\cdots)}\to\infty \;\Longrightarrow\; e_{ss}=\frac{1}{1+\infty}=0 $$

El integrador hace \( |L|\to\infty \) en continua, llevando el error de escalón **exactamente a cero**. Esa es la razón física de poner acción integral.

## 2 — Error ante rampa: por qué hace falta un tipo más
**Paso 1 — entrada rampa.** Para una rampa \( r(t)=t \), \( R(s)=1/s^2 \). El teorema del valor final deja un \( s \) en el denominador:

$$ e_{ss}=\lim_{s\to0}\frac{s\,(1/s^2)}{1+L(s)}=\lim_{s\to0}\frac{1}{s\,(1+L(s))}=\lim_{s\to0}\frac{1}{s+sL(s)} $$

Como \( s\to0 \), el sumando \( s \) se va y queda \( e_{ss}=\dfrac{1}{\lim_{s\to0}sL(s)}=\dfrac{1}{K_v} \), con \( K_v=\lim_{s\to0}sL(s) \) la constante de velocidad.

**Paso 2 — evaluar según el tipo.** Con un lazo tipo 1, \( L(s)=\dfrac{K}{s(s+a)} \): \( sL(s)=\dfrac{K}{s+a} \), luego \( K_v=\dfrac{K}{a} \) es **finito** y el error de rampa es:

$$ \boxed{\;e_{ss,\text{rampa}}=\frac{1}{K_v}=\frac{a}{K}\neq 0\;} $$

Un solo integrador sigue el escalón sin error pero deja **error constante** ante la rampa. Para anularlo haría falta tipo 2 (dos integradores), que haría \( sL\to\infty \) y \( K_v\to\infty \) — al precio de 90° más de pérdida de fase. Esto justifica la tabla: cada integrador "sube de nivel" la entrada que puede seguir con error nulo.

## 3 — Las tres constantes de error: posición, velocidad y aceleración

Las constantes de error estático son el resumen compacto del comportamiento en régimen de cualquier lazo de control. Se calculan todas con un límite en \( s=0 \).

**Constante de posición \( K_p \).**
$$ K_p = \lim_{s\to0} L(s) $$
Relacionada con el error ante un **escalón** de amplitud \( A \):
$$ e_{ss,\text{pos}} = \frac{A}{1+K_p} $$
- Tipo 0: \( K_p = L(0) < \infty \) → error finito.
- Tipo 1 o superior: \( K_p = \infty \) → \( e_{ss}=0 \).

**Constante de velocidad \( K_v \).**
$$ K_v = \lim_{s\to0} s\,L(s) $$
Relacionada con el error ante una **rampa** de pendiente \( A \) (en las mismas unidades que la salida por segundo):
$$ e_{ss,\text{vel}} = \frac{A}{K_v} $$
- Tipo 0: \( K_v = 0 \) → error infinito ante rampa.
- Tipo 1: \( K_v = K/a \) finito → error finito.
- Tipo 2 o superior: \( K_v = \infty \) → \( e_{ss}=0 \).

**Constante de aceleración \( K_a \).**
$$ K_a = \lim_{s\to0} s^2\,L(s) $$
Relacionada con el error ante una **señal parabólica** \( r(t)=At^2/2 \):
$$ e_{ss,\text{acel}} = \frac{A}{K_a} $$
- Tipos 0 y 1: \( K_a = 0 \) → error infinito.
- Tipo 2: \( K_a = K/b \) finito → error finito.
- Tipo 3 o superior: \( K_a = \infty \) → \( e_{ss}=0 \).

**Tabla completa:**

| Tipo | \( K_p \) | \( K_v \) | \( K_a \) | Esc. (A) | Rampa (A) | Parábola (A) |
|------|-----------|-----------|-----------|-----------|-----------|--------------|
| 0 | \(K_0\) finito | 0 | 0 | \(\frac{A}{1+K_0}\) | \(\infty\) | \(\infty\) |
| 1 | \(\infty\) | \(K_v\) finito | 0 | 0 | \(\frac{A}{K_v}\) | \(\infty\) |
| 2 | \(\infty\) | \(\infty\) | \(K_a\) finito | 0 | 0 | \(\frac{A}{K_a}\) |

**La clase del sistema y los integradores.** El tipo es simplemente el exponente de \( s \) que hace que \( L(s)/s^n \) tenga un límite finito y no nulo en \( s=0 \). Un PI tiene tipo 1 (\( C(s)=K_p+K_i/s \), un polo en cero). Un PID con doble integrador (raro) sería tipo 2. En convertidores, el tipo 1 (con PI o con resonante en DC, que es lo mismo que un integrador) es el estándar para lazos de corriente y tensión.

## 4 — Error por perturbación y la función de sensibilidad

El análisis anterior cubre el error ante la referencia. Las perturbaciones son igualmente importantes.

**Perturbación aguas abajo de la planta.**
Si una perturbación \( d(s) \) entra en la salida de la planta (modelando por ejemplo un armónico de tensión de red), la ecuación del lazo es:
$$ Y = G\,C\,(R-Y) + D $$
Resolviendo: \( Y = \underbrace{\frac{GC}{1+GC}}_{T}\,R + \underbrace{\frac{1}{1+GC}}_{S}\,D \)

El error ante la perturbación \( D \) con \( R=0 \) es:
$$ E = R - Y = -S\,D $$
El **error de salida es igual a \( S(s)\,D(s) \)**. Para que una perturbación DC (\( D = A/s \)) no cause error permanente, se necesita \( S(0)=0 \), lo que equivale a que \( L(0)=\infty \) — es decir, al menos un integrador.

**Perturbación aguas arriba de la planta.**
Si la perturbación entra en la entrada de la planta (por ejemplo, un escalón de corriente en un bus DC que perturba la tensión antes del controlador):
$$ Y = G\,(C\,(R-Y) + D_u) $$
Resolviendo: \( Y = T\,R + \underbrace{\frac{G}{1+GC}}_{PS}\,D_u \)

La FDT perturbación→salida es \( PS=G\cdot S \). Para rechazarla con error nulo a DC también se necesita \( S(0)=0 \), igual que antes.

**Con integrador en C: \( S(0)=0 \).**
Si \( C(s) = K_i/s + K_p \), entonces \( L(s)=C(s)G(s) \to \infty \) cuando \( s\to0 \), y:
$$ S(0) = \frac{1}{1+L(0)} = \frac{1}{\infty} = 0 $$
El error DC a cualquier perturbación aditiva (aguas arriba o aguas abajo) es cero. Es el fundamento del PI para rechazar perturbaciones constantes (escalón de carga, tensión de perturbación DC).

**Rechazo a armónicos: controlador resonante.**
Para una perturbación armónica de frecuencia \( \omega_0 \) (p.ej. el 5° armónico de 50 Hz = 250 Hz), se necesita \( |S(j\omega_0)|=0 \), lo que equivale a \( |L(j\omega_0)|=\infty \). Un **controlador resonante** proporciona esa ganancia infinita a la frecuencia exacta:
$$ C_{res}(s) = \frac{K_{res}\,s}{s^2+\omega_0^2} \quad\text{(polo en }s=\pm j\omega_0\text{)} $$
En la práctica se añade un amortiguamiento pequeño \( \omega_i \) para robustez ante variaciones de \( \omega_0 \):
$$ C_{res}(s) = \frac{K_{res}\,s}{s^2+2\omega_i s+\omega_0^2} $$
Esta estructura es el análogo frecuencial del integrador: así como el integrador da ganancia infinita en DC para anular el error a frecuencia cero, el resonante da ganancia infinita en \( \omega_0 \) para anular el error a esa frecuencia.

## 5 — Ganancia vs error vs estabilidad: el trade-off

**El dilema del sistema tipo 0 (solo P).**
Para un lazo tipo 0 con controlador proporcional \( C=K \) y planta \( G=1/(s+a) \):
- Error de posición: \( e_{ss}=a/(K+a) \). Para error pequeño hay que subir \( K \).
- Frecuencia de cruce: \( \omega_c=\sqrt{K^2-a^2} \) (aproximadamente \( K \) para \( K\gg a \)).
- Margen de fase: \( \text{PM}=90°-\arctan(\omega_c/a) \). Al subir \( K \) sube \( \omega_c \) y baja PM.

Los tres objetivos — bajo error, alta ganancia de cruce, buen PM — están en tensión mutua. No es posible conseguirlos todos a la vez sin cambiar la estructura del controlador.

**La solución del integrador (tipo 1, PI).**
Un PI añade un integrador que garantiza \( K_p=\infty \) → \( e_{ss}=0 \) ante escalón, independientemente de \( K_p \). Con el integrador, el error de posición desaparece del trade-off. El costo es la pérdida de 90° de fase que obliga a colocar el cero del PI (\( \omega_z=K_i/K_p \)) por debajo de \( \omega_c \) para recuperar margen.

**PM objetivo y posición del cero del PI.**
Para un margen de fase de \( \phi_m \) en \( \omega_c \), el cero del PI debe estar en:
$$ \omega_z = \omega_c\,\tan(\phi_{PI}) $$
donde \( \phi_{PI} \) es el avance de fase que debe aportar el PI para compensar su propia pérdida de 90°. En la práctica: \( \omega_z \approx \omega_c/5 \) a \( \omega_c/10 \) para sistemas de segundo orden.

**Para P puro (sin integrador).**
El error es inevitable pero el sistema puede diseñarse estable con margen amplio. En aplicaciones donde se tolera error en régimen (p.ej. lazo de potencia con droop, donde el error de frecuencia ante una carga constante es precisamente la señal de droop que reparte la carga), un controlador proporcional es adecuado. El error proporcional al droop es el precio que se paga por la distribución de carga pasiva y sin comunicación.

## 6 — El controlador resonante como "integrador frecuencial"

**Analogía con el integrador.**
El integrador \( C_{int}=K_i/s \) tiene un polo en \( s=0 \) que produce ganancia infinita a \( \omega=0 \) → error nulo ante señales DC.
El resonante \( C_{res}=K_{res}\,s/(s^2+\omega_0^2) \) tiene polos en \( s=\pm j\omega_0 \) que producen ganancia infinita a \( \omega=\omega_0 \) → error nulo ante señales de frecuencia \( \omega_0 \).

La analogía es exacta: el resonante hace en \( \omega_0 \) lo mismo que el integrador hace en 0. En el diagrama de Nyquist, el resonante produce un arco de radio \( \infty \) alrededor del eje imaginario exactamente en \( \omega_0 \) (al igual que el integrador produce el arco al rodear \( s=0 \)).

**Derivación de \( e_{ss}=0 \) para una sinusoide de frecuencia \( \omega_0 \).**
Con perturbación \( D(s)=A\omega_0/(s^2+\omega_0^2) \) (sinusoide permanente):
$$ e_{ss} = \lim_{s\to j\omega_0} (s-j\omega_0)\,S(s)\,D(s) $$
Para que el límite sea cero, basta con que \( |S(j\omega_0)|=0 \). Esto ocurre si \( |L(j\omega_0)|=\infty \), lo que el resonante garantiza al tener su polo en \( \pm j\omega_0 \). El resultado es el teorema del valor final **en frecuencia**: un polo del controlador en \( \pm j\omega_0 \) anula el error ante una señal de esa frecuencia.

**Aplicación práctica: filtro activo o control en \( \alpha\beta \).**
En el marco \( \alpha\beta \) (sin transformación al marco síncrono), la referencia de corriente es una señal sinusoidal a 50 Hz y sus armónicos. Un PI en \( \alpha\beta \) no anula el error ante la fundamental (porque su integrador está en 0, no en 50 Hz). Se usa un **integrador generalizado** o resonante en \( \omega_1=2\pi\cdot50 \) rad/s:

$$ C_{res,\omega_1}(s) = \frac{K_{res}\,s}{s^2+\omega_1^2} $$

que da ganancia infinita a 50 Hz → error nulo a la fundamental. Para rechazar el 5° y 7° armónico (los más significativos en sistemas trifásicos con cargas no lineales), se añaden resonantes en \( \omega_5=5\omega_1 \) y \( \omega_7=7\omega_1 \).

**Síntesis del controlador PR (Proporcional-Resonante).**
En marcos estacionarios (\( \alpha\beta \)) el controlador estándar para seguimiento de referencia sinusoidal y rechazo de armónicos es:
$$ C_{PR}(s) = K_p + \sum_{h\in\{1,5,7,11,13,\ldots\}} \frac{K_{res,h}\,s}{s^2+2\omega_i s+(h\,\omega_1)^2} $$
Cada término cubre un armónico. En comparación con el PI + frame síncrono dq (que también puede rechazar armónicos mediante resonantes en los armónicos de deslizamiento), el PR en \( \alpha\beta \) evita la transformación de Park pero requiere más términos resonantes.

<div class="cfig"><img src="figuras/error-regimen-permanente-analisis.png" alt="constantes de error, sensibilidad, trade-off y resonante"><div class="cap">Análisis completo del error en régimen permanente. (a) Respuesta al escalón para tipos 0, 1, 2: el tipo 0 deja error $e_{ss}=1/(1+K)$, los tipos 1 y 2 lo anulan (el tipo 2 con más oscilación). (b) $|S(j\omega)|$ con PI: la acción integral garantiza $|S(0)|=0$ y buen rechazo de perturbaciones a baja frecuencia. (c) Trade-off en tipo 0: subir $K$ reduce el error pero también el margen de fase PM. (d) Controlador PI + resonante en el 5° armónico: pico de $|L|$ en $\omega_5=250$ Hz que garantiza error nulo al armónico de esa frecuencia.</div></div>

## Cuándo y por qué se usa
Para decidir si hace falta acción **integral**: seguir una referencia constante sin error exige
tipo ≥1; seguir una rampa sin error, tipo ≥2. Es el motivo de usar PI en lazos de corriente/tensión.

## Procedimiento (genérico)
1. Identifica integradores en \( L(s) \) → tipo del sistema.
2. Calcula \( K_p,K_v,K_a \) según la entrada relevante.
3. Si el error no cumple, añade integración (sube el tipo) y re-sintoniza.
4. Verifica que el margen de fase sigue siendo aceptable.

## Ejemplo de aplicación real
**Problema:** Lazo de corriente tipo I (PI) ante dos entradas: referencia escalón de 10 A y perturbación escalón de 1 V de tensión de red. Calcular el error en régimen para cada caso.

Para la **referencia escalón**: el PI tiene un integrador → tipo 1, \( K_p=\infty \) → \( e_{ss}=1/(1+K_p)=0 \). El PI integra hasta que el error desaparece. Para la **perturbación escalón** que entra después del controlador (tensión de red, componente \( d \)): el integrador del PI sigue estando en el camino de retroalimentación y también la anula → \( e_{ss}=0 \). Verificación: simular un escalón de perturbación de 5 V: la corriente se desviará transitoriamente pero regresará a los 10 A de referencia. Si se usa solo control P (sin integrador, tipo 0), el error ante la perturbación escalón sería \( 5/(R\cdot K_p) \neq 0 \).

## Ejemplo de código
```python
import sympy as sp, numpy as np
s = sp.symbols('s'); L = 20/(s*(s+5))      # tipo 1
Kv = sp.limit(s*L, s, 0)                    # error de rampa = 1/Kv
print(f"Kv={Kv}, error de rampa={1/Kv}")

# Controlador resonante en w0=250 Hz (5° armonico de 50 Hz)
w0 = 2*np.pi*250; Kres = 80; wi = 1       # wi: damping para robustez
# Respuesta en frecuencia:
ww = np.logspace(0, 4, 5000)
C_res = Kres * 1j*ww / (-ww**2 + 2j*wi*ww + w0**2)
# Pico en w0: |C_res(jw0)| → Kres/(2*wi) >> 1
print(f"Pico resonante: {abs(Kres/(2*wi)):.1f}")
```

## Parámetros y valores típicos
Lazos de convertidor con PI → tipo 1 (error nulo a referencia constante en dq). Tipo 2 es raro
por la pérdida de fase. Resonantes en armónicos 5°, 7°, 11°, 13° para filtros activos.

## Errores comunes
- Subir el tipo sin vigilar el margen de fase → oscilación o inestabilidad.
- Olvidar que la integración pura sufre **windup** ante saturación → ver [[anti-windup]].
- Aplicar las fórmulas a lazos no unitarios sin reducir primero el diagrama.
- Usar resonante sin amortiguamiento \( \omega_i \): cualquier variación de \( \omega_0 \) impide la cancelación.

## Conceptos relacionados
- [[realimentacion]] · [[controlador-pid]] · [[metricas-desempeno]] · [[anti-windup]] · [[funciones-sensibilidad]]

## Referencias
- Ogata, *Ingeniería de Control Moderna*.
- Franklin, Powell, *Feedback Control of Dynamic Systems*.
