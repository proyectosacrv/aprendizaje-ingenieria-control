---
titulo: Valor eficaz (RMS), valor medio y factor de potencia
slug: valor-rms-factor-potencia
categoria: fisica-modelado
tipo: concepto
nivel: basico
proyectos: []
objetivos: [manejar magnitudes AC y el convenio pico/RMS del marco dq]
tags: [rms, valor-eficaz, factor-potencia, potencia, basico]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-06-10
relacionados: [potencia-ac-fasores, sistema-trifasico, potencia-instantanea-dq, calidad-potencia, series-fourier]
referencias:
  - "Mohan, Undeland & Robbins, Power Electronics"
---

## Definición
El **valor eficaz (RMS)** de una señal es el valor de continua que disiparía la misma potencia en una
resistencia. El **factor de potencia (FP)** mide qué fracción de la potencia aparente se convierte en
potencia activa útil.

## Fundamento teórico
El valor eficaz y el medio de una señal periódica:
$$ X_{rms} = \sqrt{\frac{1}{T}\int_0^T x^2(t)\,dt}, \qquad X_{med} = \frac{1}{T}\int_0^T x(t)\,dt $$
Para una senoide pura, \( X_{rms} = X_{pico}/\sqrt{2} \) y \( X_{med}=0 \). Las potencias en AC
monofásica:
$$ S = V_{rms} I_{rms}, \quad P = V_{rms} I_{rms}\cos\varphi, \quad Q = V_{rms} I_{rms}\sin\varphi $$
$$ \mathrm{FP} = \frac{P}{S} = \cos\varphi \ \text{(senoidal)} $$
En trifásico equilibrado \( P = \sqrt{3}\,V_{LL} I_L \cos\varphi \). **Convenio del proyecto:** se
trabaja con **amplitud de pico de fase**, \( V_0 = V_{LL}\sqrt{2/3} \), y por eso la potencia
trifásica instantánea en dq lleva el factor \( \tfrac32 \): \( P = \tfrac32(v_d i_d + v_q i_q) \).

## Cuándo y por qué se usa
Para dimensionar (las corrientes/tensiones nominales son RMS), medir potencia, y —crucial en este
repositorio— para no equivocarse con el **convenio pico vs RMS** al pasar al marco dq.

## Procedimiento de diseño (genérico)
1. Para una senoide: \( X_{rms} = X_{pico}/\sqrt{2} \).
2. Potencia aparente \( S = V_{rms} I_{rms} \); activa \( P = S\cos\varphi \).
3. En dq con amplitud de pico, recuerda el factor \( \tfrac32 \) en la potencia.

## Ejemplo de código
```python
import numpy as np
t = np.linspace(0, 0.02, 1000, endpoint=False)
x = 326.6*np.sin(2*np.pi*50*t)             # pico de fase ~ 230 Vrms
rms = np.sqrt(np.mean(x**2))               # ~ 230.9 V
```

## Parámetros y valores típicos
Red de 400 V (línea, RMS) \( \to V_0 = 326.6 \) V de pico de fase. FP objetivo en convertidores ≈ 1
(inyección con \( Q\approx 0 \)). Con armónicos, FP real = \( \cos\varphi \times \) factor de
distorsión (\( < \cos\varphi \)).

## Errores comunes
- Mezclar pico y RMS en la misma expresión.
- Olvidar el factor \( \tfrac32 \) (o \( \sqrt{3} \)) al pasar de fase a trifásico.
- Asumir FP \( =\cos\varphi \) cuando hay armónicos (entonces interviene la distorsión).

## Conceptos relacionados
- [[potencia-ac-fasores]] · [[sistema-trifasico]] · [[potencia-instantanea-dq]] · [[calidad-potencia]] · [[series-fourier]]

## Referencias
- Mohan, Undeland & Robbins, *Power Electronics*.
