---
titulo: Filtro notch (rechazo de banda) para resonancias
slug: filtro-notch
categoria: control
tipo: tecnica
nivel: intermedio
proyectos: []
objetivos: [atenuar una resonancia estrecha en el lazo sin perder ancho de banda]
tags: [notch, rechazo-banda, resonancia, lcl, filtro, intermedio, control]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-12
relacionados: [amortiguamiento-activo-lcl, filtro-lcl, diagrama-bode, loop-shaping]
referencias:
  - "Yepes et al., Analysis and design of resonant current controllers, IEEE TIE 2011"
  - "Peña-Alzola et al., LCL-filter design for grid converters, IEEE TPEL 2014"
---

## Definición
Filtro selectivo que **atenúa una banda estrecha** centrada en \( \omega_n \) dejando pasar el
resto del espectro casi intacto. En convertidores se usa para cancelar el pico de resonancia del
[[filtro-lcl]] dentro del lazo de control.

## Fundamento teórico
Forma general con cero y polo amortiguados:
$$ N(s)=\frac{s^2+2\zeta_z\,\omega_n s+\omega_n^2}{s^2+2\zeta_p\,\omega_n s+\omega_n^2},
   \qquad \zeta_z<\zeta_p $$
- La profundidad del *notch* la fija \( \zeta_z/\zeta_p \) (cuanto menor el cociente, más profundo).
- El ancho de la muesca lo fija \( \zeta_p \): estrecho (selectivo) → muy sensible a que \( \omega_n \)
  coincida con la resonancia real; ancho → más robusto pero introduce **más retardo de fase** en la
  banda de control.
- Penalización clave: el notch **resta fase** por debajo de \( \omega_n \), reduciendo el margen del
  lazo si \( \omega_n \) está cerca del cruce de ganancia.

Frente al **amortiguamiento activo** ([[amortiguamiento-activo-lcl]]): el notch es más simple (no
necesita sensar la corriente del condensador) pero menos robusto a la deriva de \( \omega_{res} \)
(con \( L \), \( C \) variando con el punto de operación o tolerancias).

<div class="cfig"><img src="figuras/filtro-notch-respuesta.png" alt="respuesta en frecuencia de un filtro notch"><div class="cap">El notch atenúa profundamente una banda estrecha en fn (la resonancia LCL) dejando el resto casi intacto; el precio es algo de fase restada por debajo de fn.</div></div>

## Cuándo y por qué se usa
Para estabilizar el lazo de corriente con filtro LCL sin recurrir a sensores extra de
amortiguamiento activo, o para eliminar un armónico/oscilación concreta. Encaja en el moldeo de
[[loop-shaping]].

## Procedimiento de diseño (genérico)
1. Identifica la frecuencia de resonancia \( \omega_{res}=\sqrt{\frac{L_1+L_2}{L_1 L_2 C}} \) del LCL.
2. Sitúa \( \omega_n=\omega_{res} \); elige \( \zeta_p \) (ancho) y \( \zeta_z\ll\zeta_p \) (profundidad).
3. Comprueba la fase introducida cerca de \( \omega_c \): si daña el margen, aleja el cruce o ensancha.
4. Verifica robustez: barre \( L,C \) (ver [[barrido-parametrico]]) y confirma que el pico queda
   atenuado en todo el rango.
5. Discretiza con Tustin/*prewarp* en \( \omega_n \).

## Ejemplo de aplicación real
**Problema:** Lazo de corriente con filtro LCL a \( f_{res}=2.05\,\text{kHz} \). Sin notch, el pico de resonancia de +38 dB impide subir \( f_c \) de 800 Hz sin oscilar. Diseñar un notch y verificar la mejora de margen.

Se elige \( \omega_n=2\pi\times2050\,\text{rad/s} \), \( \zeta_z=0.02 \) (muesca profunda), \( \zeta_p=0.5 \) (moderadamente ancho para robustez a ±5 % de variación en \( f_{res} \)). El notch atenúa el pico a <5 dB. Ahora se puede subir \( f_c \) a 1.2 kHz. Penalización de fase: a \( f_c=1.2\,\text{kHz} \), el notch resta \( \approx8° \). Margen final: si antes con \( f_c=800\,\text{Hz} \) era 42°, ahora con el notch y \( f_c=1.2\,\text{kHz} \) queda \( \approx38° \) — ligeramente reducido pero aceptable. Verificar robustez: desplazar \( f_{res} \) ±10 % (cambio de \( L_g \) de la red); si la atenuación cae de 38 dB a 15 dB, aun así suficiente para evitar inestabilidad.

## Ejemplo de código
```python
import control as ct
wn, zz, zp = 2*3.1416*2500, 0.02, 0.5
notch = ct.tf([1, 2*zz*wn, wn**2], [1, 2*zp*wn, wn**2])
```

## Parámetros y valores típicos
\( \zeta_z \approx 0.01\text{–}0.05 \), \( \zeta_p \approx 0.3\text{–}0.7 \). Profundidad de muesca
20–40 dB. \( \omega_n \) en la resonancia LCL (típica 1–5 kHz).

## Errores comunes
- Notch muy estrecho con \( \omega_{res} \) mal estimada → no atenúa nada (queda al lado del pico).
- Colocar \( \omega_n \) cerca de \( \omega_c \) → la pérdida de fase desestabiliza el lazo.
- Ignorar la deriva de la resonancia con el punto de operación/tolerancias.

## Conceptos relacionados
- [[amortiguamiento-activo-lcl]] · [[filtro-lcl]] · [[loop-shaping]] · [[diagrama-bode]] · [[barrido-parametrico]]

## Referencias
- Yepes et al., *Resonant current controllers*, IEEE TIE 2011.
- Peña-Alzola et al., *LCL-filter design for grid converters*, IEEE TPEL 2014.
