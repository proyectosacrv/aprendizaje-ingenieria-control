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
fecha_actualizacion: 2026-06-30
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

<div class="cfig"><img src="figuras/valor-rms-factor-potencia-rms.png" alt="valor RMS de una senoide"><div class="cap">El valor eficaz (RMS) de una senoide es su pico dividido por √2: la continua que disiparía la misma potencia en una resistencia. Las magnitudes nominales (400 V, etc.) son RMS.</div></div>

## 1 — Por qué el RMS de una senoide es \( X_{pico}/\sqrt2 \)
**Paso 1 — partir de la definición.** El RMS es la raíz de la media del cuadrado. Para \( x(t)=X_{pico}\sin(\omega t) \) con periodo \( T=2\pi/\omega \):

$$ X_{rms}^2=\frac{1}{T}\int_0^T X_{pico}^2\sin^2(\omega t)\,dt=\frac{X_{pico}^2}{T}\int_0^T\sin^2(\omega t)\,dt $$

**Paso 2 — linealizar el seno al cuadrado.** Con la identidad \( \sin^2\theta=\tfrac12\big(1-\cos2\theta\big) \):

$$ \int_0^T\sin^2(\omega t)\,dt=\int_0^T\frac{1-\cos(2\omega t)}{2}\,dt=\underbrace{\frac{T}{2}}_{\text{término }1/2}-\underbrace{\frac{1}{2}\int_0^T\cos(2\omega t)\,dt}_{=\,0} $$

El segundo integrando es un coseno de frecuencia \( 2\omega \): sobre un periodo completo \( T \) caben exactamente dos ciclos suyos, así que su integral se anula (el área positiva cancela la negativa). Queda solo \( T/2 \).

**Paso 3 — sustituir y simplificar.** Reemplazando la integral por \( T/2 \):

$$ X_{rms}^2=\frac{X_{pico}^2}{T}\cdot\frac{T}{2}=\frac{X_{pico}^2}{2}\quad\Longrightarrow\quad \boxed{\;X_{rms}=\frac{X_{pico}}{\sqrt2}\;} $$

La \( T \) del prefactor cancela la \( T/2 \) de la integral y desaparece el periodo: el resultado vale para **cualquier** frecuencia. Numéricamente, \( X_{pico}=326{,}6 \) V de pico de fase da \( 326{,}6/\sqrt2=230{,}9 \) V RMS — la tensión nominal de fase de una red de 400 V de línea.

## 2 — Por qué \( P=V_{rms}I_{rms}\cos\varphi \)
**Paso 1 — potencia instantánea.** Con \( v(t)=V_{pico}\sin(\omega t) \) e \( i(t)=I_{pico}\sin(\omega t-\varphi) \), la potencia instantánea es el producto:

$$ p(t)=v(t)\,i(t)=V_{pico}I_{pico}\,\sin(\omega t)\sin(\omega t-\varphi) $$

**Paso 2 — producto de senos a suma.** Con \( \sin A\sin B=\tfrac12\big[\cos(A-B)-\cos(A+B)\big] \), siendo \( A=\omega t \), \( B=\omega t-\varphi \):

$$ p(t)=\frac{V_{pico}I_{pico}}{2}\Big[\underbrace{\cos\varphi}_{\text{constante}}-\underbrace{\cos(2\omega t-\varphi)}_{\text{oscila a }2\omega}\Big] $$

**Paso 3 — promediar sobre un periodo.** La potencia activa es el valor medio de \( p(t) \). El término \( \cos(2\omega t-\varphi) \) oscila a \( 2\omega \) y promedia cero (igual que en el apartado 1); solo sobrevive la constante:

$$ P=\frac{V_{pico}I_{pico}}{2}\cos\varphi $$

**Paso 4 — pasar a RMS.** Usando \( V_{pico}=\sqrt2\,V_{rms} \) e \( I_{pico}=\sqrt2\,I_{rms} \), el producto \( V_{pico}I_{pico}=2\,V_{rms}I_{rms} \) y el factor \( 2 \) cancela el \( \tfrac12 \):

$$ \boxed{\;P=V_{rms}I_{rms}\cos\varphi\;} $$

El \( \cos\varphi \) es el factor de potencia: la fracción de la potencia aparente \( S=V_{rms}I_{rms} \) que se convierte en activa. La misma cuenta en dq aparece en [[potencia-instantanea-dq]], donde el factor \( \tfrac32 \) sustituye a este \( \tfrac12 \) por sumar las tres fases con amplitud de pico.

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
