---
titulo: Controlador PID
slug: controlador-pid
categoria: control
tipo: tecnica
nivel: basico
proyectos: []
objetivos: [entender que aporta cada termino proporcional, integral y derivativo]
tags: [PID, PI, proporcional, integral, derivativo, basico]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-30
relacionados: [realimentacion, sintonia-pi-pid, sistema-primer-orden, control-cascada]
referencias:
  - "Aström, Hägglund, Advanced PID Control, ISA 2006"
---

## Definición
Controlador que actúa sobre el error con tres términos: **P**roporcional, **I**ntegral y
**D**erivativo. Es el controlador más usado en la industria por su sencillez y eficacia.

## Fundamento teórico
$$ u(t) = K_p\,e(t) + K_i\!\int_0^t e\,d\tau + K_d\,\frac{de}{dt}
   \;\;\Longleftrightarrow\;\; C(s)=K_p+\frac{K_i}{s}+K_d\,s $$
Qué aporta cada término:
- **Proporcional** \( K_p \): reacciona al error actual; más \( K_p \) → más rápido, pero deja
  **error en régimen** y puede oscilar.
- **Integral** \( K_i \): acumula el error pasado; **elimina el error en régimen**, pero añade
  retraso de fase (puede reducir estabilidad y dar *windup*).
- **Derivativo** \( K_d \): anticipa según la tendencia del error; **amortigua** y mejora
  estabilidad, pero amplifica el **ruido** (se suele filtrar).
En convertidores se usa casi siempre **PI** (sin D, por el ruido de conmutación).

<div class="cfig"><img src="figuras/controlador-pid-estructura.png" alt="estructura paralela del PID"><div class="cap">Estructura PID: tres ramas en paralelo sobre el error — proporcional (Kp), integral (Ki/s) y derivativa (Kd·s) — que se suman para formar la acción de control u.</div></div>

## 1 — De la forma temporal a la FDT del PID
**Paso 1 — los tres términos en el tiempo.** El controlador suma tres acciones sobre el error \( e(t) \): una proporcional al error actual, una proporcional a su integral acumulada y una proporcional a su pendiente:

$$ u(t) = K_p\,e(t) + K_i\!\int_0^t e(\tau)\,d\tau + K_d\,\frac{de(t)}{dt} $$

**Paso 2 — Laplace de cada término.** Con condiciones iniciales nulas (ver [[funcion-transferencia]]), la transformada de Laplace es lineal y cumple \( \mathcal{L}\{e\}=E(s) \), \( \mathcal{L}\!\left\{\int_0^t e\,d\tau\right\}=\dfrac{E(s)}{s} \) (integrar = dividir por \( s \)) y \( \mathcal{L}\!\left\{\dfrac{de}{dt}\right\}=s\,E(s) \) (derivar = multiplicar por \( s \)). Transformando término a término:

$$ U(s)=K_p\,E(s)+\frac{K_i}{s}\,E(s)+K_d\,s\,E(s) $$

**Paso 3 — factorizar \( E(s) \).** La FDT del controlador es \( C(s)=U(s)/E(s) \); sacando \( E(s) \) factor común:

$$ \boxed{\;C(s)=\frac{U(s)}{E(s)}=K_p+\frac{K_i}{s}+K_d\,s\;} $$

Cada término domina en una zona de frecuencia: el integral \( K_i/s \to\infty \) cuando \( s\to 0 \) (ganancia infinita en continua, de ahí que **anule el error en régimen** ante escalón, ver [[error-regimen-permanente]]); el derivativo \( K_d s \to\infty \) cuando \( s\to\infty \) (de ahí que **amplifique el ruido** de alta frecuencia); el proporcional \( K_p \) actúa en toda la banda.

## 2 — Lazo cerrado de un PI sobre una planta de primer orden
**Paso 1 — planteamiento.** Tomamos el PI \( C(s)=K_p+\dfrac{K_i}{s}=\dfrac{K_p s+K_i}{s} \) realimentado sobre una planta de primer orden \( P(s)=\dfrac{K}{\tau s+1} \) (ver [[sistema-primer-orden]]). La transferencia de lazo abierto es:

$$ L(s)=C(s)\,P(s)=\frac{K_p s+K_i}{s}\cdot\frac{K}{\tau s+1}=\frac{K(K_p s+K_i)}{s(\tau s+1)} $$

**Paso 2 — fórmula del lazo cerrado.** Con realimentación unitaria, \( T(s)=\dfrac{L}{1+L} \) (ver [[realimentacion]]). Sustituyendo \( L \) y multiplicando numerador y denominador por \( s(\tau s+1) \) para limpiar la fracción anidada:

$$ T(s)=\frac{\dfrac{K(K_p s+K_i)}{s(\tau s+1)}}{1+\dfrac{K(K_p s+K_i)}{s(\tau s+1)}}=\frac{K(K_p s+K_i)}{s(\tau s+1)+K(K_p s+K_i)} $$

**Paso 3 — desarrollar el denominador.** Expandiendo \( s(\tau s+1)=\tau s^2+s \) y agrupando los términos en \( s \):

$$ s(\tau s+1)+K(K_p s+K_i)=\tau s^2+s+KK_p s+KK_i=\tau s^2+(1+KK_p)\,s+KK_i $$

de donde resulta un sistema de **segundo orden** (ver [[respuesta-segundo-orden]]):

$$ \boxed{\;T(s)=\frac{K(K_p s+K_i)}{\tau s^2+(1+KK_p)\,s+KK_i}\;} $$

**Paso 4 — interpretación.** Comparando el denominador con la forma canónica \( s^2+2\zeta\omega_n s+\omega_n^2 \) (tras dividir por \( \tau \)): \( \omega_n=\sqrt{KK_i/\tau} \) y \( 2\zeta\omega_n=(1+KK_p)/\tau \). El integrador \( K_i \) fija la rapidez \( \omega_n \) y, en \( s=0 \), \( T(0)=\dfrac{KK_i}{KK_i}=1 \): **ganancia continua exactamente unidad**, luego seguimiento sin error en régimen ante escalón. El proporcional \( K_p \) aparece solo en el término de amortiguamiento, ajustando \( \zeta \) sin tocar \( T(0) \).

## Cuándo y por qué se usa
En lazos de corriente, tensión, velocidad: cuando se quiere seguimiento sin error en régimen con
una estructura simple. Es la base de los lazos en cascada.

## Procedimiento (genérico)
1. Empieza con P para fijar la rapidez.
2. Añade I para anular el error en régimen (cuida el *windup*: usa anti-windup).
3. Añade D (filtrado) solo si necesitas más amortiguamiento y el ruido lo permite.
4. Sintoniza por ancho de banda o cancelación de polo (ver [[sintonia-pi-pid]]).

## Ejemplo de aplicación real
**Problema:** VSC con \( L=2\,\text{mH} \), \( r=50\,\text{m}\Omega \), \( f_{sw}=10\,\text{kHz} \). Diseñar el PI de corriente para \( f_c=1\,\text{kHz} \) con margen de fase real ≥ 45°, considerando el retardo de cómputo \( T_d=150\,\mu\text{s} \).

Paso 1 — cancelación de polo: cero del PI en \( \omega_z=r/L=25\,\text{rad/s} \). Paso 2 — ganancia: \( K_p=L\omega_c=0.002\times6283\approx12.6 \), \( K_i=K_p\,r/L\approx315\,\text{s}^{-1} \). Paso 3 — verificar margen con retardo: desfase del retardo a \( \omega_c \) es \( \omega_c T_d\times(180/\pi)\approx54° \), reduciendo el margen de 90° a 36° (no cumple 45°). Corrección: reducir \( \omega_c \) a 750 Hz (\( K_p\approx9.4 \)), desfase del retardo \( \approx40° \), margen resultante \( \approx50° \). El PI sin considerar el retardo cumpliría en teoría pero no en implementación real.

## Ejemplo de código
```python
# PI discreto con anti-windup (saturacion de la salida)
integ += Ki*e*dt
u = Kp*e + integ
if u > umax: u = umax; integ -= Ki*e*dt    # no acumular si satura
```

## Parámetros y valores típicos
Lazos de convertidor: PI con cero en el polo de la planta. Margen de fase objetivo 45–60°.

## Errores comunes
- Olvidar el **anti-windup**: el integrador se carga al saturar y la respuesta se degrada.
- Usar D con señal ruidosa sin filtrar.

## Conceptos relacionados
- [[realimentacion]] · [[sintonia-pi-pid]] · [[control-cascada]]

## Referencias
- Aström, Hägglund, *Advanced PID Control*, 2006.
