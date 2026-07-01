---
titulo: Controlador resonante (proporcional-resonante, PR)
slug: controlador-resonante
categoria: control
tipo: tecnica
nivel: intermedio
proyectos: []
objetivos: [seguir y rechazar senoides y armónicos sin error en marco estacionario]
tags: [resonante, pr, modelo-interno, armonicos, alfa-beta, intermedio, control]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-30
relacionados: [controlador-pid, marco-dq, filtro-lcl, error-regimen-permanente]
referencias:
  - "Teodorescu et al., Proportional-resonant controllers and filters for grid-connected converters, IET 2006"
  - "Yepes et al., Effects of discretization methods on the performance of resonant controllers, IEEE TPEL 2010"
---

## Definición
Controlador que añade a una parte proporcional un **término resonante** sintonizado a una
frecuencia \( \omega_0 \). Proporciona **ganancia muy alta** justo en esa frecuencia, de modo que
sigue (o rechaza) una senoide de \( \omega_0 \) con error nulo en régimen permanente, trabajando
directamente en marco **estacionario** (αβ o monofásico), sin rotar a dq.

## Fundamento teórico
Por el **principio del modelo interno**: para anular el error ante una entrada, el lazo debe
contener un modelo del generador de esa señal. El de una senoide de frecuencia \( \omega_0 \) es
\( s^2+\omega_0^2 \). El PR **ideal** es:
$$ G_{PR}(s)=K_p+\frac{2K_r\,s}{s^2+\omega_0^2} $$
con ganancia \( \to\infty \) en \( \omega_0 \) (equivale a un PI en marco giratorio: el resonante
es la "imagen" de un integrador rotado \( \pm\omega_0 \)). En la práctica se usa la forma **no
ideal** con amortiguamiento \( \omega_c \) (banda finita, robusta a desviaciones de frecuencia):
$$ G_{PR}(s)=K_p+\frac{2K_r\,\omega_c\,s}{s^2+2\omega_c s+\omega_0^2} $$
La ganancia de pico es \( K_p+K_r \) y el ancho de banda \( \approx 2\omega_c \). Para corregir
varios armónicos se suman **compensadores armónicos (HC)** en \( h\omega_0 \) (típico 5, 7, 11, 13):
$$ G(s)=K_p+\sum_{h}\frac{2K_{rh}\,\omega_c\,s}{s^2+2\omega_c s+(h\omega_0)^2} $$

<div class="cfig"><img src="figuras/controlador-resonante-respuesta.png" alt="respuesta del controlador PR"><div class="cap">El controlador PR tiene una ganancia altísima justo en f0: por el principio del modelo interno, eso anula el error ante una senoide de esa frecuencia trabajando en marco estacionario (sin dq).</div></div>

## 1 — Por qué el resonante da ganancia infinita en \( \omega_0 \)
**Paso 1 — evaluar en la frecuencia física.** La respuesta en frecuencia se obtiene sustituyendo \( s=j\omega \). El término resonante ideal es \( R(s)=\dfrac{2K_r s}{s^2+\omega_0^2} \); en \( s=j\omega \), usando \( (j\omega)^2=-\omega^2 \):

$$ R(j\omega)=\frac{2K_r\,(j\omega)}{(j\omega)^2+\omega_0^2}=\frac{2K_r\,j\omega}{\omega_0^2-\omega^2} $$

**Paso 2 — el denominador se anula en \( \omega_0 \).** Cuando la frecuencia de la señal coincide con la de sintonía, \( \omega=\omega_0 \), el denominador \( \omega_0^2-\omega^2=0 \), mientras el numerador \( 2K_r j\omega_0\neq 0 \). Por tanto:

$$ \lim_{\omega\to\omega_0}\big|R(j\omega)\big|=\left|\frac{2K_r\,j\omega_0}{0}\right|\;\to\;\infty $$

Esto equivale a que \( R(s) \) tiene **polos en \( s=\pm j\omega_0 \)** (raíces de \( s^2+\omega_0^2 \)) justo sobre el eje imaginario, en la frecuencia exacta de la senoide.

**Paso 3 — ganancia infinita ⟹ error cero.** En lazo cerrado el error es \( E=\dfrac{R_{ref}}{1+G_{PR}P} \) (ver [[realimentacion]]). A \( \omega=\omega_0 \), como \( G_{PR}(j\omega_0)\to\infty \), el denominador \( 1+G_{PR}P\to\infty \) y por tanto \( E(j\omega_0)\to 0 \): la senoide de \( \omega_0 \) se sigue (o se rechaza, si es perturbación) con **error nulo en régimen**. Es el principio del modelo interno: \( s^2+\omega_0^2 \) es el modelo del generador de una senoide de \( \omega_0 \).

## 2 — La forma no ideal: ganancia finita pero acotada
**Paso 1 — añadir amortiguamiento.** El polo sobre el eje imaginario es frágil: si \( \omega_0 \) de la red se desvía un poco, el pico infinito ya no cae sobre la señal. La forma no ideal desplaza los polos un poco a la izquierda con un término \( 2\omega_c s \): \( R_{ni}(s)=\dfrac{2K_r\omega_c s}{s^2+2\omega_c s+\omega_0^2} \). Evaluando en \( s=j\omega \):

$$ R_{ni}(j\omega)=\frac{2K_r\omega_c\,(j\omega)}{(\omega_0^2-\omega^2)+2\omega_c\,(j\omega)} $$

**Paso 2 — valor en el pico.** En \( \omega=\omega_0 \) el término \( \omega_0^2-\omega^2=0 \) y queda solo la parte imaginaria del denominador:

$$ R_{ni}(j\omega_0)=\frac{2K_r\omega_c\,j\omega_0}{2\omega_c\,j\omega_0}=K_r $$

El \( 2\omega_c j\omega_0 \) del numerador y del denominador **se cancela exactamente**, dejando ganancia de pico **finita** \( =K_r \) (con la parte proporcional, \( K_p+K_r \)). Ya no es infinita, pero sigue siendo enorme frente a \( K_p \), suficiente para reducir el error a casi cero, y ahora con **banda finita \( \approx 2\omega_c \)** que tolera desviaciones de \( \omega_0 \). Por eso es la forma usada en la práctica.

## Cuándo y por qué se usa
Control de corriente/tensión de convertidores de red en αβ (evita los dos marcos dq y el desacoplo),
rechazo selectivo de armónicos (filtros activos), y sistemas monofásicos donde no hay un dq natural.
Es la alternativa estacionaria al PI+[[marco-dq]].

## Procedimiento de diseño (genérico)
1. Diseña \( K_p \) como en un P puro para el ancho de banda y margen objetivo (planta del lazo de
   corriente \( \approx 1/(sL+R) \)).
2. Fija \( \omega_0 \) (frecuencia de red) y elige \( \omega_c \) (1–15 rad/s) según la robustez a
   variación de frecuencia deseada.
3. Ajusta \( K_r \) para la velocidad de convergencia del término resonante sin degradar el margen.
4. Añade HC en los armónicos relevantes (cada uno resta algo de fase: vigílalo).
5. **Discretiza con cuidado** (Tustin con *prewarp* en \( \omega_0 \), o métodos que preserven la
   posición del pico): ver [[discretizacion-controladores]]. Considera frecuencia **adaptativa**
   (tomar \( \omega_0 \) de la PLL) si la red varía.

## Ejemplo de aplicación real
**Problema:** VSC monofásico controlado en marco estacionario. Un PI genera error en régimen para la referencia sinusoidal de 50 Hz. Implementar un PR no ideal para eliminar el error y añadir compensación del 5º armónico (250 Hz).

El PI tiene ganancia finita a 50 Hz, dejando un error proporcional. El término resonante \( 2K_r\omega_c s/(s^2+2\omega_c s+\omega_0^2) \) con \( \omega_0=314\,\text{rad/s} \) y \( \omega_c=5\,\text{rad/s} \) añade una ganancia de pico \( \approx K_p+K_r \) en ±5 rad/s alrededor de 50 Hz: el error cae a casi cero. Para el 5º armónico (250 Hz): se añade un segundo resonante en \( h\omega_0=5\times314=1570\,\text{rad/s} \). Cada HC resta fase al lazo — con 2 HC la pérdida acumulada cerca del cruce de ganancia debe verificarse con `ct.margin()`. Si el margen baja a <30°, reducir \( K_r \) de los HC.

## Ejemplo de código
```python
import control as ct
w0, wc = 2*3.1416*50, 5.0
Kp, Kr = 20.0, 2000.0
PR = ct.tf([Kp, 2*(Kr*wc+Kp*wc), Kp*w0**2],
           [1, 2*wc, w0**2])           # Kp + termino resonante no ideal
```

## Parámetros y valores típicos
\( \omega_c \approx 2\pi\cdot(0.5\text{–}2) \) Hz (compromiso selectividad/robustez), pico de
ganancia 40–80 dB sobre \( K_p \). HC hasta el 13º armónico en filtros activos.

## Errores comunes
- Discretizar con métodos que **desplazan el pico** (Euler) → el resonante deja de cancelar a
  \( \omega_0 \) y empeora con la frecuencia de muestreo.
- PR ideal (\( \omega_c=0 \)) en sistema real: oscila si la frecuencia de red se desvía.
- Apilar muchos HC sin vigilar la pérdida acumulada de margen de fase.
- Olvidar el límite/anti-windup del actuador (también aplica a resonantes).

## Conceptos relacionados
- [[controlador-pid]] · [[marco-dq|transformada de Clarke]] · [[filtro-lcl|amortiguamiento activo]] · [[discretizacion-controladores]]

## Referencias
- Teodorescu et al., *PR controllers and filters for grid-connected converters*, IET 2006.
- Yepes et al., *Effects of discretization methods on resonant controllers*, IEEE TPEL 2010.
