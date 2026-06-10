---
titulo: Análisis MIMO por valores singulares (SVD, RGA)
slug: valores-singulares-mimo
categoria: metodologia
tipo: metodo
nivel: avanzado
proyectos: []
objetivos: [cuantificar ganancia, direccionalidad y robustez de sistemas multivariable]
tags: [svd, valores-singulares, rga, h-infinito, direccionalidad, mimo, avanzado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-09
relacionados: [nyquist-generalizado, control-robusto-hinf, funciones-sensibilidad, margenes-estabilidad, respuesta-frecuencia-ss]
referencias:
  - "Skogestad, Postlethwaite, Multivariable Feedback Control, Wiley 2005"
  - "Maciejowski, Multivariable Feedback Design, Addison-Wesley 1989"
---

## Definición
Conjunto de herramientas para analizar sistemas multivariable mediante la **descomposición en
valores singulares** de su respuesta en frecuencia: cuantifica la **ganancia máxima/mínima**, la
**direccionalidad** (qué entradas amplifica más) y la robustez, donde el Bode escalar ya no basta.

## Fundamento teórico
Para \( \mathbf{G}(j\omega)\in\mathbb{C}^{m\times m} \), la SVD es
\( \mathbf{G}=\mathbf{U}\,\Sigma\,\mathbf{V}^H \), con \( \Sigma=\mathrm{diag}(\sigma_1\ge\dots\ge\sigma_m) \):
$$ \bar\sigma(\mathbf{G})=\sigma_{max}=\max_{\|u\|=1}\|\mathbf{G}u\|,\qquad
   \underline\sigma(\mathbf{G})=\sigma_{min}=\min_{\|u\|=1}\|\mathbf{G}u\| $$
- \( \bar\sigma,\underline\sigma \) son la **ganancia máxima y mínima** según la dirección de la
  entrada; las columnas de \( \mathbf{V} \) (entrada) y \( \mathbf{U} \) (salida) dan esas direcciones.
- **Norma \( H_\infty \):** \( \|\mathbf{G}\|_\infty=\max_\omega \bar\sigma(\mathbf{G}(j\omega)) \)
  (pico de ganancia sobre todas las direcciones y frecuencias) → enlaza con [[control-robusto-hinf]].
- **Número de condición:** \( \gamma(\omega)=\bar\sigma/\underline\sigma \); \( \gamma\gg1 \) indica
  planta **mal condicionada** (direcciones fuertes y débiles), difícil de controlar.
- **Margen robusto MIMO:** picos de \( \bar\sigma(\mathbf{S}) \) y \( \bar\sigma(\mathbf{T}) \)
  (versiones MIMO de las [[funciones-sensibilidad]]); el margen de módulo es \( 1/\|\mathbf{S}\|_\infty \).

**RGA (Relative Gain Array):** \( \Lambda=\mathbf{G}\circ(\mathbf{G}^{-1})^T \) (producto de
Hadamard), evaluada en DC y en \( \omega_c \). Indica **qué entrada controlar con qué salida**
(emparejamiento) y mide el acoplamiento: \( \Lambda \) cerca de la identidad → desacoplado;
elementos grandes/negativos → acoplamiento fuerte, evitar ese emparejamiento.

**Incertidumbre estructurada (μ):** el valor singular estructurado \( \mu \) generaliza
\( \bar\sigma \) cuando la incertidumbre tiene estructura; \( \mu<1 \) → estabilidad/desempeño robusto.

## Cuándo y por qué se usa
Para diseñar y validar control de convertidores como sistema \( 2\times2 \) en dq (acoplamiento
d-q), evaluar robustez MIMO real (no lazo a lazo), decidir el emparejamiento de variables y conectar
con \( H_\infty \)/μ. Complementa al [[nyquist-generalizado]] (eigenloci) con una medida de magnitud
y dirección.

## Procedimiento de diseño (genérico)
1. Obtén \( \mathbf{G}(j\omega) \) (de [[respuesta-frecuencia-ss]]).
2. Calcula \( \bar\sigma,\underline\sigma \) en cada \( \omega \) → "Bode" de valores singulares.
3. Evalúa el número de condición y la RGA (DC y \( \omega_c \)) para acoplamiento/emparejamiento.
4. Forma \( \mathbf{S},\mathbf{T} \) y mide sus picos \( \bar\sigma \) (robustez).
5. Si hay incertidumbre estructurada, analiza \( \mu \).

## Ejemplo de código
```python
import numpy as np
def sigma_bode(G):                       # G: (Nf, m, m)
    s = np.array([np.linalg.svd(Gk, compute_uv=False) for Gk in G])
    return s[:,0], s[:,-1]               # sigma_max, sigma_min
def rga(G0):                             # en una frecuencia
    return G0 * np.linalg.inv(G0).T
```

## Parámetros y valores típicos
Picos \( \|\mathbf{S}\|_\infty<2 \) (≈6 dB), \( \|\mathbf{T}\|_\infty<1.5 \). Número de condición
\( \gamma>10 \) ⇒ planta difícil. RGA con elementos \( \approx1 \) en la diagonal del emparejamiento elegido.

## Errores comunes
- Analizar márgenes lazo-a-lazo en un sistema acoplado (oculta interacciones) → usar SVD/μ.
- Emparejar variables con RGA grande o negativo (acoplamiento severo, inestabilidad de integridad).
- Confundir \( \bar\sigma \) (magnitud direccional) con los eigenloci (estabilidad por rodeos).

## Conceptos relacionados
- [[nyquist-generalizado]] · [[control-robusto-hinf]] · [[funciones-sensibilidad]] · [[margenes-estabilidad]] · [[respuesta-frecuencia-ss]]

## Referencias
- Skogestad, Postlethwaite, *Multivariable Feedback Control*, 2005.
- Maciejowski, *Multivariable Feedback Design*, 1989.
