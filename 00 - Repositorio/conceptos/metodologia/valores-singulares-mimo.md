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
fecha_actualizacion: 2026-07-01
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

<div class="cfig"><img src="figuras/valores-singulares-mimo-bode.png" alt="bode de valores singulares maximo y minimo"><div class="cap">Bode de valores singulares de una planta $2\times2$: $\sigma_{max}$ y $\sigma_{min}$ acotan la ganancia según la dirección de la entrada. La franja entre ambos es el número de condición $\gamma=\sigma_{max}/\sigma_{min}$: si es grande, la planta está mal condicionada (direcciones fuertes y débiles) y es difícil de controlar. El pico de $\sigma_{max}$ es la norma $H_\infty$.</div></div>

## 1 — De dónde salen los valores singulares: SVD desde eigenvalores de \( \mathbf{A}^H\mathbf{A} \)
**Paso 1 — planteamiento.** Para una matriz \( \mathbf{G}\in\mathbb{C}^{m\times p} \), la **ganancia** en la dirección de entrada \( \mathbf{v} \) (normalizada) es \( \|\mathbf{G}\mathbf{v}\| \). El máximo y el mínimo de esa ganancia son los valores singulares extremos. Buscarlos equivale a un problema de autovalores: se maximiza \( \mathbf{v}^H\mathbf{G}^H\mathbf{G}\mathbf{v} \) con \( \|\mathbf{v}\|=1 \), que por el teorema variacional de Rayleigh se alcanza en los autovectores de la matriz hermitica semidefinida positiva \( \mathbf{G}^H\mathbf{G} \).

**Paso 2 — conexión con la SVD.** Si \( \mathbf{G}=\mathbf{U}\Sigma\mathbf{V}^H \), entonces:

$$ \mathbf{G}^H\mathbf{G}=\mathbf{V}\Sigma^H\mathbf{U}^H\mathbf{U}\Sigma\mathbf{V}^H=\mathbf{V}(\Sigma^H\Sigma)\mathbf{V}^H $$

Los autovalores de \( \mathbf{G}^H\mathbf{G} \) son los cuadrados de los valores singulares:

$$ \boxed{\sigma_i = \sqrt{\lambda_i(\mathbf{G}^H\mathbf{G})},\quad \sigma_1\ge\sigma_2\ge\dots\ge0} $$

Las columnas de \( \mathbf{V} \) (entrada, dirección de máxima ganancia) y \( \mathbf{U} \) (salida) son los autovectores correspondientes.

**Paso 3 — ejemplo numérico \( 2\times2 \).** Para \( \mathbf{G}=\bigl[\begin{smallmatrix}3&1\\0&2\end{smallmatrix}\bigr] \):

$$ \mathbf{G}^T\mathbf{G}=\begin{bmatrix}9&3\\3&5\end{bmatrix},\quad \lambda_{1,2}=7\pm\sqrt{9}=10.62,\,3.38 $$

$$ \sigma_{\max}=\sqrt{10.62}=3.26,\quad \sigma_{\min}=\sqrt{3.38}=1.84,\quad \kappa=\sigma_{\max}/\sigma_{\min}=1.77 $$

## 2 — El número de condición \( \kappa \) y su significado para robustez
**Paso 1 — definición.** \( \kappa(\omega)=\bar\sigma/\underline\sigma \). Si \( \kappa\gg1 \) existe una dirección de entrada que la planta amplifica mucho (\( \bar\sigma \)) y otra que casi colapsa (\( \underline\sigma\approx0 \)): inversión numérica de \( \mathbf{G} \) amplifica los errores en la dirección débil por un factor \( 1/\underline\sigma \).

**Paso 2 — consecuencia para el control.** Para invertir la planta (descentralizar, pre-compensar o calcular \( \mathbf{C}\approx\mathbf{G}^{-1} \)), la incertidumbre relativa \( \delta\mathbf{G}/\mathbf{G} \) se amplifica por \( \kappa \) en la señal de control:

$$ \|\delta\mathbf{u}\|/\|\mathbf{u}\|\lesssim\kappa\cdot\|\delta\mathbf{G}\|/\|\mathbf{G}\| $$

**Paso 3 — regla práctica.** \( \kappa < 10 \): planta bien condicionada, control desacoplado razonable. \( \kappa > 100 \): planta mal condicionada; control lazo-a-lazo es frágil; se necesita control robusto MIMO o pre-compensador. En sistemas dq con acoplamiento fuerte, \( \kappa \) crece en la zona de resonancia del filtro LCL, exactamente donde la robustez es más crítica.

$$ \boxed{\kappa=\frac{\bar\sigma(\mathbf{G})}{\underline\sigma(\mathbf{G})}\gg1 \;\Rightarrow\; \text{planta mal condicionada, control frágil}} $$

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
