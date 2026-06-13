---
titulo: Compensador de adelanto-atraso (lead-lag)
slug: compensador-adelanto-atraso
categoria: control
tipo: tecnica
nivel: intermedio
proyectos: []
objetivos: [moldear fase y ganancia del lazo para fijar margen y ancho de banda]
tags: [lead-lag, adelanto, atraso, compensador, frecuencia, intermedio, control]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-12
relacionados: [loop-shaping, lugar-raices, diagrama-bode, margenes-estabilidad, controlador-pid]
referencias:
  - "Ogata, Ingeniería de Control Moderna, Pearson"
  - "Franklin, Powell, Feedback Control of Dynamic Systems, Pearson"
---

## Definición
Compensador clásico de primer orden que **aporta fase** (adelanto) o **reduce ganancia en alta
frecuencia / mejora la de baja** (atraso) para moldear la respuesta en frecuencia del lazo. Es la
versión analógica/continua del moldeo que en digital harías con un PID filtrado.

## Fundamento teórico
**Adelanto (lead)** \( (\alpha>1) \):
$$ C(s)=K_c\,\frac{1+\alpha T s}{1+T s},\qquad
   \phi_{max}=\arcsin\frac{\alpha-1}{\alpha+1}\ \text{ en }\ \omega_m=\frac{1}{T\sqrt{\alpha}} $$
Aporta hasta \( \phi_{max} \) de fase (≈55–65° por etapa con \( \alpha\le10 \)) cerca del cruce de
ganancia → **sube el margen de fase y el ancho de banda**; eleva la ganancia en alta (más rápido,
pero más ruido). Es análogo a un PD filtrado.

**Atraso (lag)** \( (\alpha<1) \): misma forma; añade ganancia en baja frecuencia
(**reduce el error en régimen permanente**) y atenúa en alta, a costa de un poco de fase negativa
que se coloca lejos del cruce. Análogo a un PI aproximado.

**Lead-lag** combina ambos: el lag mejora el error estacionario y el lead recupera el margen y la
velocidad.

<div class="cfig"><img src="figuras/compensador-adelanto-atraso-bode.png" alt="Bode de un compensador de adelanto"><div class="cap">El compensador de adelanto inyecta un máximo de fase φmax en ωm=1/(T√α); colocándolo en el cruce de ganancia sube el margen de fase, a costa de más ganancia (y ruido) en alta frecuencia.</div></div>

## Cuándo y por qué se usa
Cuando un P/PI no basta para cumplir simultáneamente margen, ancho de banda y error, o cuando se
prefiere un compensador propio (sin el polo en el origen del integrador) y bien condicionado para
discretizar. Encaja con el enfoque de [[loop-shaping]] y se diseña sobre [[diagrama-bode]] o
[[lugar-raices]].

## Procedimiento de diseño (genérico)
1. Fija especificaciones: margen de fase y \( \omega_c \) objetivo (de las [[especificaciones-control]]).
2. Evalúa la fase que falta en \( \omega_c \) → fase a aportar por el **lead** (margen extra 5–10°).
3. Calcula \( \alpha=\dfrac{1+\sin\phi_{max}}{1-\sin\phi_{max}} \) y \( T=\dfrac{1}{\omega_c\sqrt\alpha} \).
4. Ajusta \( K_c \) para que el cruce caiga en \( \omega_c \).
5. Si falla el error estacionario, añade una etapa **lag** en baja frecuencia.
6. Verifica márgenes ([[margenes-estabilidad]]) y discretiza ([[discretizacion-controladores]]).

## Ejemplo de aplicación real
**Problema:** Lazo de posición de un accionamiento con margen de fase de 22° (objetivo 45°). Diseñar un compensador de adelanto de una etapa que aporte los 23° necesarios sin degradar el cruce.

Fase a aportar con 5° de margen extra: \( \phi_{max}=28° \). Factor: \( \alpha=(1+\sin28°)/(1-\sin28°)\approx2.77 \). Constante de tiempo: \( T=1/(\omega_c\sqrt{\alpha})=1/(200\times1.66)=3.0\,\text{ms} \). Compensador: \( C(s)=(1+\alpha T s)/(1+Ts)=(1+8.3\times10^{-3}s)/(1+3.0\times10^{-3}s) \). A \( \omega_c=200\,\text{rad/s} \), la ganancia del compensador es \( \sqrt{\alpha}\approx1.66 \) (+4.4 dB): reducir \( K_c \) en esa proporción para mantener el cruce en \( \omega_c \). Resultado final: margen de fase \( \approx22+28=50° \) ✓. Si \( \alpha>10 \) la amplificación de ruido sería inaceptable: encadenar dos etapas en lugar de una.

## Ejemplo de código
```python
import control as ct, numpy as np
phi = np.deg2rad(50); wc = 200.0
alpha = (1+np.sin(phi))/(1-np.sin(phi)); T = 1/(wc*np.sqrt(alpha))
lead = ct.tf([alpha*T, 1], [T, 1])      # 1 etapa de adelanto
```

## Parámetros y valores típicos
Por etapa de adelanto: \( \alpha \le 10 \) (\( \phi_{max}\lesssim 55^\circ \)); para más fase,
**encadena** etapas. La separación lead/lag suele ser de una década respecto a \( \omega_c \).

## Errores comunes
- Pedir demasiada fase a una sola etapa (\( \alpha \) enorme) → amplifica ruido en alta frecuencia.
- Colocar el cero/polo del lag cerca de \( \omega_c \) → resta fase donde más duele.
- Olvidar reescalar \( K_c \) tras añadir el compensador (el cruce se mueve).

## Conceptos relacionados
- [[loop-shaping]] · [[lugar-raices]] · [[diagrama-bode]] · [[margenes-estabilidad]] · [[controlador-pid]]

## Referencias
- Ogata, *Ingeniería de Control Moderna*.
- Franklin, Powell, *Feedback Control of Dynamic Systems*.
