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
fecha_actualizacion: 2026-06-12
relacionados: [potencia-ac-fasores, marco-dq, transformada-clarke, sistema-por-unidad, componentes-simetricas]
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
- [[potencia-ac-fasores]] · [[marco-dq]] · [[transformada-clarke]] · [[sistema-por-unidad]]

## Referencias
- Chapman, *Máquinas Eléctricas*.
- Yazdani, Iravani, 2010.
