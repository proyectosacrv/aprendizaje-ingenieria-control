---
titulo: Respuesta de segundo orden (ζ, ωn)
slug: respuesta-segundo-orden
categoria: control
tipo: concepto
nivel: basico
proyectos: []
objetivos: [relacionar amortiguamiento y frecuencia natural con la respuesta]
tags: [segundo-orden, amortiguamiento, frecuencia-natural, sobreimpulso, basico]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [sistema-primer-orden, polos-ceros, metricas-desempeno, funcion-transferencia]
referencias:
  - "Ogata, Ingeniería de Control Moderna, Pearson"
---

## Definición
Sistema con dos polos que puede **oscilar**. Su respuesta queda descrita por dos parámetros: la
**frecuencia natural** \( \omega_n \) (rapidez) y el **amortiguamiento** \( \zeta \) (cuánto
oscila). Es el modelo de referencia para especificar desempeño.

## Fundamento teórico
$$ G(s) = \frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2} $$
Polos: \( s=-\zeta\omega_n \pm j\omega_n\sqrt{1-\zeta^2} \). Según \( \zeta \):
- \( \zeta>1 \): **sobreamortiguado** (no oscila, lento).
- \( \zeta=1 \): **crítico** (lo más rápido sin oscilar).
- \( 0<\zeta<1 \): **subamortiguado** (oscila y se asienta).
- \( \zeta=0 \): oscilación permanente (al límite de estabilidad).

Métricas (caso subamortiguado):
$$ M_p = e^{-\pi\zeta/\sqrt{1-\zeta^2}}\;(\text{sobreimpulso}), \qquad
   t_s \approx \frac{4}{\zeta\omega_n}\;(\text{establecimiento al 2\%}) $$

## Cuándo y por qué se usa
Es el patrón con el que se fijan especificaciones (sobreimpulso, tiempo de establecimiento) y se
interpretan los polos dominantes de sistemas de orden mayor.

## Procedimiento (genérico)
1. Identifica los dos polos dominantes → calcula \( \omega_n \) y \( \zeta \).
2. Estima sobreimpulso \( M_p \) y tiempo de establecimiento \( t_s \).
3. Ajusta el control para mover los polos al \( \zeta \) y \( \omega_n \) deseados.

## Ejemplo de aplicación real
**Problema:** El lazo de potencia de un GFM con droop muestra sobreimpulso del 25 % y frecuencia de oscilación de 3.3 Hz. Determinar \( \zeta \) y \( \omega_n \), y juzgar si cumple \( \zeta\ge0.6 \).

Del sobreimpulso: \( M_p=0.25\Rightarrow\zeta=\sqrt{\ln^2(M_p)/(\pi^2+\ln^2(M_p))}\approx0.40 \). De la frecuencia amortiguada \( \omega_d=2\pi\times3.3\approx20.7\,\text{rad/s} \): \( \omega_n=\omega_d/\sqrt{1-\zeta^2}\approx22.6\,\text{rad/s} \). Con \( \zeta=0.40 \) el sistema **no cumple** \( \zeta\ge0.6 \) (sobreimpulso objetivo \(\le10\,\%\)). Para subir \( \zeta \): reducir \( m_p \) del droop (baja la ganancia del lazo de potencia) o añadir [[impedancia-virtual]] (introduce amortiguamiento sin cambiar \( \omega_n \)). Con \( \zeta=0.7 \): sobreimpulso \(\approx4.6\,\%\), modo bien amortiguado.

## Ejemplo de código
```python
import numpy as np, control as ct
wn, z = 10.0, 0.5
G = ct.tf([wn**2], [1, 2*z*wn, wn**2])
Mp = np.exp(-np.pi*z/np.sqrt(1-z**2))      # ~16% para z=0.5
```

## Parámetros y valores típicos
\( \zeta=0.7 \): ~5% de sobreimpulso, buen compromiso. \( \zeta=0.5 \): ~16%. Diseño habitual
\( \zeta=0.5\text{–}0.8 \).

## Errores comunes
- Aplicar las fórmulas de 2º orden a un sistema de orden alto sin verificar que hay polos dominantes.
- Buscar \( \zeta \) muy alto (lento) o muy bajo (oscilatorio) sin compromiso.

## Conceptos relacionados
- [[sistema-primer-orden]] · [[polos-ceros]] · [[metricas-desempeno]]

## Referencias
- Ogata, *Ingeniería de Control Moderna*.
