---
titulo: Anti-windup del integrador
slug: anti-windup
categoria: control
tipo: tecnica
nivel: basico
proyectos: []
objetivos: [evitar la sobrecarga del término integral cuando el actuador satura]
tags: [anti-windup, saturacion, integrador, back-calculation, basico, control]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-30
relacionados: [controlador-pid, current-limiting, sintonia-pi-pid, error-regimen-permanente]
referencias:
  - "Aström, Hägglund, PID Controllers, ISA 1995"
  - "Aström, Murray, Feedback Systems, Princeton 2008"
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

## 2 — Cómo el término de back-calculation frena el integrador
**Paso 1 — añadir la realimentación de saturación.** Se realimenta la diferencia \( (u_{sat}-u) \) al integrador con ganancia \( 1/T_t \):

$$ \dot I = K_i\,e + \frac{1}{T_t}\,(u_{sat}-u),\qquad u=K_p e + I $$

Mientras **no** hay saturación \( u_{sat}=u \), el término extra es 0 y el PI funciona normal. En **saturación**, \( u_{sat}=u_{max} \) está fijo mientras \( u=K_p e+I \) sigue creciendo con \( I \): el término \( (u_{sat}-u) \) se hace negativo y **resta** a \( \dot I \).

**Paso 2 — el integrador busca un equilibrio.** El estado deja de crecer cuando \( \dot I=0 \). Sustituyendo \( u=K_p e+I \) en \( u_{sat}-u=u_{max}-K_p e-I \):

$$ \dot I = K_i\,e + \frac{1}{T_t}\,(u_{max}-K_p e - I)=0 $$

**Paso 3 — despejar el valor acotado.** Multiplicando por \( T_t \) y despejando \( I \):

$$ K_i e\,T_t + u_{max}-K_p e - I = 0 \;\Longrightarrow\; \boxed{\;I_{eq}=u_{max}-K_p e + K_i\,T_t\,e\;} $$

A diferencia del caso sin AW (donde \( I\to\infty \)), aquí \( I \) se estabiliza en un valor **finito** dictado por \( u_{max} \): el integrador se "ancla" cerca de lo que el actuador puede dar, no de lo que el error pide. Al salir de la saturación no hay carga que descargar y la salida sigue la referencia de inmediato. La constante \( T_t \) fija la **rapidez** con que \( I \) converge a \( I_{eq} \): pequeña → frena rápido (pero sensible a ruido), grande → frena despacio (anti-windup débil).

## Cuándo y por qué se usa
En todo lazo PI con límites físicos: corriente, tensión de modulación, par. Imprescindible junto
al [[current-limiting]] de convertidores, donde la referencia se recorta con frecuencia.

## Procedimiento (genérico)
1. Modela el saturador real (límites de \( u \)).
2. Elige el esquema (back-calculation suele ser el más robusto).
3. Sintoniza \( T_t \): regla habitual \( T_t\approx\sqrt{T_i T_d} \) o \( T_t\in[T_i/2,\,T_i] \).
4. Verifica recuperación sin sobreimpulso tras una saturación prolongada.

## Ejemplo de aplicación real
**Problema:** PI de corriente con límite de modulación \( |u|_{max}=1\,\text{p.u.} \). Se aplica una referencia de 2 p.u. durante 80 ms (saturación inevitable). Comparar recuperación con y sin back-calculation (\( T_t=T_i/2 \)).

Sin anti-windup: durante la saturación el integrador acumula hasta \( I\approx K_i\times2\,\text{p.u.}\times0.08\,\text{s}\approx50\,\text{p.u.} \) (con \( K_i=315 \)). Al liberar la saturación, el integrador debe descargarse desde 50 a ~1 p.u. generando un sobreimpulso de corriente de muchas veces la nominal. Con back-calculation: el término \( (u_{sat}-u)/T_t \) mantiene \( I\approx1\,\text{p.u.} \) durante la saturación. Al liberar, el sobreimpulso queda por debajo del 5 %. Ajuste: \( T_t\approx T_i/3\ldots T_i/2 \). Demasiado pequeño → ruidoso; demasiado grande → anti-windup ineficaz.

## Ejemplo de código
```python
def pi_aw(e, I, Kp, Ki, Tt, umin, umax, dt):
    u = Kp*e + I
    usat = min(max(u, umin), umax)
    I += (Ki*e + (usat-u)/Tt)*dt        # back-calculation
    return usat, I
```

## Parámetros y valores típicos
\( T_t \) del orden del tiempo integral \( T_i \) (un poco menor). Demasiado pequeño → ruidoso;
demasiado grande → anti-windup ineficaz.

## Errores comunes
- Saturar la salida pero seguir integrando el error completo (windup clásico).
- Poner \( T_t \) sin relación con \( T_i \).
- Olvidar que en cascada el lazo externo también necesita anti-windup si su salida (referencia
  del interno) se limita.

## Conceptos relacionados
- [[controlador-pid]] · [[current-limiting]] · [[sintonia-pi-pid]] · [[error-regimen-permanente]]

## Referencias
- Aström, Hägglund, *PID Controllers*, 1995.
- Aström, Murray, *Feedback Systems*, 2008.
