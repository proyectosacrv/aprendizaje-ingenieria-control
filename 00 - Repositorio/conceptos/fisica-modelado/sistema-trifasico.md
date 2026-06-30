---
titulo: Sistema trifásico equilibrado
slug: sistema-trifasico
categoria: fisica-modelado
tipo: concepto
nivel: basico
proyectos: []
objetivos: [manejar tensiones y corrientes trifásicas y sus relaciones línea-fase]
tags: [trifasico, equilibrado, fasores, linea-fase, basico, modelado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-30
relacionados: [potencia-ac-fasores, marco-dq, sistema-por-unidad, componentes-simetricas]
referencias:
  - "Chapman, Máquinas Eléctricas, McGraw-Hill"
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
---

## Definición
Sistema de tres tensiones senoidales de igual amplitud y frecuencia, **desfasadas 120°**. Si las
cargas son iguales en las tres fases, el sistema es **equilibrado** y se reduce a un análisis
monofásico equivalente.

## Fundamento teórico
$$ v_a=\hat V\cos\omega t,\quad v_b=\hat V\cos(\omega t-120^\circ),\quad v_c=\hat V\cos(\omega t+120^\circ) $$
En equilibrio la suma instantánea es nula (\( v_a+v_b+v_c=0 \)) → no circula corriente por el
neutro. Relaciones línea-fase:
- **Estrella (Y):** \( V_{LL}=\sqrt3\,V_{fase} \), \( I_{L}=I_{fase} \).
- **Triángulo (Δ):** \( V_{LL}=V_{fase} \), \( I_{L}=\sqrt3\,I_{fase} \).

Potencia trifásica total (constante en equilibrio):
$$ P=\sqrt3\,V_{LL}I_L\cos\varphi,\qquad S=\sqrt3\,V_{LL}I_L $$
La potencia instantánea total es **constante** (no pulsa a \( 2\omega \) como la monofásica), lo
que motiva el control en [[marco-dq|dq]].

<div class="cfig"><img src="figuras/sistema-trifasico-ondas.png" alt="tensiones trifasicas y sus fasores"><div class="cap">Tres senoides de igual amplitud desfasadas 120°; sus fasores forman una estrella simétrica cuya suma instantánea es cero. Por eso la potencia trifásica total (en equilibrio) no pulsa.</div></div>

## 1 — Por qué \( V_{LL}=\sqrt3\,V_{fase} \) en estrella
**Paso 1 — la tensión de línea es una resta de fases.** En conexión estrella, la tensión de línea entre los bornes a y b es la diferencia de las dos tensiones de fase (ambas referidas al neutro):

$$ \bar V_{ab}=\bar V_a-\bar V_b $$

Con \( \bar V_a=V_f\angle0° \) y \( \bar V_b=V_f\angle{-120°} \) (terna equilibrada, ambas de módulo \( V_f \)).

**Paso 2 — restar los fasores.** Pasando a binómica, \( \bar V_b=V_f(\cos(-120°)+j\sin(-120°))=V_f(-\tfrac12-j\tfrac{\sqrt3}{2}) \):

$$ \bar V_{ab}=V_f(1+j0)-V_f\Big(-\tfrac12-j\tfrac{\sqrt3}{2}\Big)=V_f\Big(1+\tfrac12+j\tfrac{\sqrt3}{2}\Big)=V_f\Big(\tfrac32+j\tfrac{\sqrt3}{2}\Big) $$

**Paso 3 — tomar el módulo.** El módulo de \( \tfrac32+j\tfrac{\sqrt3}{2} \) es:

$$ \Big|\bar V_{ab}\Big|=V_f\sqrt{\Big(\tfrac32\Big)^2+\Big(\tfrac{\sqrt3}{2}\Big)^2}=V_f\sqrt{\tfrac94+\tfrac34}=V_f\sqrt{\tfrac{12}{4}}=V_f\sqrt3 $$

$$ \boxed{\;V_{LL}=\sqrt3\,V_{fase}\;} $$

El \( \sqrt3 \) sale de la geometría: dos fasores de igual módulo separados \( 120° \) tienen una diferencia \( \sqrt3 \) veces mayor (su ángulo además adelanta \( 30° \), \( \bar V_{ab}=\sqrt3\,V_f\angle30° \)). La corriente, en cambio, no se desdobla: \( I_L=I_{fase} \) porque la línea es el único camino de la fase. En triángulo el papel se invierte (las fases comparten la tensión de línea pero las corrientes se restan), de ahí \( V_{LL}=V_{fase} \), \( I_L=\sqrt3\,I_{fase} \).

## 2 — Por qué la potencia trifásica es constante (no pulsa a \( 2\omega \))
**Paso 1 — sumar las tres potencias instantáneas.** Cada fase tiene una potencia que pulsa a \( 2\omega \) (ver [[potencia-ac-fasores]]): \( p_k=V_fI_f\cos\varphi+V_fI_f\cos(2\omega t-\varphi+\phi_k) \), donde \( \phi_k=0,-240°,+240° \) son los desfases dobles de cada fase. La total:

$$ p_{3\phi}=\underbrace{3V_fI_f\cos\varphi}_{\text{constante}}+V_fI_f\big[\cos(2\omega t-\varphi)+\cos(2\omega t-\varphi-240°)+\cos(2\omega t-\varphi+240°)\big] $$

**Paso 2 — el corchete pulsante se anula.** Tres cosenos de igual frecuencia separados \( 120° \) (porque \( 240°\equiv-120° \)) suman cero: es la misma identidad \( 1+a+a^2=0 \) de [[componentes-simetricas]] proyectada sobre el eje real. El corchete vale 0 idénticamente para todo \( t \):

$$ \boxed{\;p_{3\phi}(t)=3V_fI_f\cos\varphi=\text{constante}=\sqrt3\,V_{LL}I_L\cos\varphi\;} $$

usando \( V_{LL}=\sqrt3 V_f \) e \( I_L=I_f \) del apartado 1 (de donde \( 3V_f=\sqrt3 V_{LL} \)). Que la potencia no pulse es la razón física de fondo para controlar en [[marco-dq|dq]]: en el marco giratorio las magnitudes son continuas y P, Q se vuelven escalares constantes en régimen.

## Cuándo y por qué se usa
Es el marco de todo el sistema eléctrico de potencia y de los convertidores de red. Las tensiones
nominales y los cálculos de potencia/corriente parten siempre de estas relaciones.

## Procedimiento (genérico)
1. Identifica conexión (Y/Δ) y si hay neutro.
2. Pasa a fasores y usa el **equivalente monofásico** (una fase) si está equilibrado.
3. Aplica relaciones línea-fase para tensiones/corrientes.
4. Para desequilibrio o falta, usa [[componentes-simetricas]].

## Ejemplo de aplicación real
**Problema:** Parque eólico de \( P=10\,\text{MW} \) a \( V_{LL}=33\,\text{kV} \), \( \cos\phi=0.95\,\text{retraso} \). Calcular corriente de línea, potencia reactiva y tensión de fase pico para dimensionar el convertidor.

Corriente de línea: \( I_L=P/(\sqrt{3}\,V_{LL}\cos\phi)=10\times10^6/(\sqrt{3}\times33000\times0.95)\approx184\,\text{A} \). Potencia reactiva inductiva: \( Q=P\tan(\arccos0.95)\approx3.29\,\text{MVAr} \). Potencia aparente: \( S=P/\cos\phi\approx10.53\,\text{MVA} \). Tensión de fase pico (para diseñar la modulación del VSC): \( \hat V_f=33000\sqrt{2}/\sqrt{3}\approx26.9\,\text{kV} \). Con estos datos se dimensiona el condensador del bus DC y se fijan las referencias \( i_d^*,i_q^* \) del control.

## Ejemplo de código
```python
import numpy as np
Vll = 690.0
Vf_pico = Vll*np.sqrt(2/3)             # pico de fase (amplitud)
P = np.sqrt(3)*Vll*IL*np.cos(phi)      # potencia activa trifásica
```

## Parámetros y valores típicos
Tensiones de línea típicas en convertidores: 400 V, 690 V (BT); frecuencia 50/60 Hz. Convención de
amplitud de fase: \( \hat V_{fase}=V_{LL}\sqrt{2/3} \).

## Errores comunes
- Confundir tensión de línea con tensión de fase (factor \( \sqrt3 \)).
- Mezclar valores de pico y RMS.
- Suponer suma nula con cargas o red desequilibradas (entonces circula homopolar).

## Conceptos relacionados
- [[potencia-ac-fasores]] · [[marco-dq]] · [[sistema-por-unidad]]

## Referencias
- Chapman, *Máquinas Eléctricas*.
- Yazdani, Iravani, 2010.
