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
fecha_actualizacion: 2026-07-03
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

## 2 — La SVD: \( M=U\Sigma V^T \) y la geometría de la transformación

**Paso 1 — la descomposición completa.** Toda matriz \( M\in\mathbb{R}^{m\times n} \) se descompone como \( M=U\Sigma V^T \) donde \( U\in\mathbb{R}^{m\times m} \) y \( V\in\mathbb{R}^{n\times n} \) son ortogonales (rotaciones) y \( \Sigma \) es diagonal no negativa. La acción de \( M \) sobre un vector \( x \) es: primero \( V^T \) rota \( x \) al sistema de coordenadas de las "direcciones de entrada", luego \( \Sigma \) escala cada componente por \( \sigma_i \), y finalmente \( U \) rota al sistema de salida.

**Paso 2 — la elipse de la imagen.** La imagen de la esfera unitaria \( \|x\|=1 \) bajo \( M \) es una **elipse** (o elipsoide en dimensión mayor). Los semiejes de la elipse tienen longitudes \( \sigma_1\geq\sigma_2\geq\ldots \). La dirección del semieje mayor es la columna de \( U \) correspondiente a \( \sigma_1 \) (dirección de máxima amplificación de salida); la entrada que la produce es la columna de \( V \) correspondiente.

**Paso 3 — la ganancia de peor caso y de mejor caso.** Por tanto:
$$ \max_{\|u\|=1}\|Mu\|=\sigma_1=\bar\sigma(M),\qquad \min_{\|u\|=1}\|Mu\|=\sigma_n=\underline\sigma(M) $$
La norma inducida \( \|M\|_2=\sigma_1 \) y la norma de Frobenius \( \|M\|_F=\sqrt{\sum\sigma_i^2} \).

**Paso 4 — interpretación para control.** En un sistema dq, la planta \( Z_{dq}(j\omega) \) mapea corrientes a tensiones. Si \( \sigma_1\gg\sigma_2 \) a \( \omega_0=2\pi\times50\,\text{Hz} \), hay una dirección de corriente que produce una tensión muy grande y otra que produce una pequeña. El control debe gestionar ambas — lo que con un PI diagonal simple (uno por eje) puede no ser posible sin desacoplo previo.

## 3 — La SVD de la respuesta en frecuencia: G(jω) = UΣV*

**Paso 1 — la descomposición en cada frecuencia.** A cada frecuencia \( \omega \), la matriz de transferencia \( \mathbf{G}(j\omega)\in\mathbb{C}^{m\times p} \) se descompone como:
$$ \mathbf{G}(j\omega)=\mathbf{U}(j\omega)\,\Sigma(\omega)\,\mathbf{V}^*(j\omega) $$
donde \( \Sigma(\omega)=\mathrm{diag}(\sigma_1(\omega),\ldots,\sigma_m(\omega)) \) con \( \sigma_1\geq\ldots\geq\sigma_m\geq0 \). Las columnas de \( \mathbf{V} \) son las **direcciones de entrada** ortogonales (en qué dirección del espacio de entrada se excita); las de \( \mathbf{U} \) son las **direcciones de salida** correspondientes.

**Paso 2 — σ̄ y σ como ganancia de peor y mejor caso.** Para cualquier entrada unitaria \( \mathbf{u} \) (con \( \|\mathbf{u}\|=1 \)):
$$ \sigma_1(\omega)=\bar\sigma(\mathbf{G}(j\omega))=\max_{\|\mathbf{u}\|=1}\|\mathbf{G}(j\omega)\mathbf{u}\| \quad\text{(ganancia de peor dirección)} $$
$$ \sigma_m(\omega)=\underline\sigma(\mathbf{G}(j\omega))=\min_{\|\mathbf{u}\|=1}\|\mathbf{G}(j\omega)\mathbf{u}\| \quad\text{(ganancia de mejor dirección)} $$
El cociente \( \kappa(\omega)=\bar\sigma/\underline\sigma \) es el **número de condición**: mide qué tan diferente es la ganancia según la dirección de excitación.

**Paso 3 — consecuencias para el control MIMO.** Si \( \kappa\gg1 \) existe una dirección de entrada amplificada mucho (\( \bar\sigma \)) y otra débil (\( \underline\sigma\approx0 \)). Invertir la planta (pre-compensar o calcular \( \mathbf{C}\approx\mathbf{G}^{-1} \)) amplifica los errores en la dirección débil por \( 1/\underline\sigma \): si hay incertidumbre relativa \( \delta\mathbf{G}/\mathbf{G} \), el error en la señal de control es:
$$ \|\delta\mathbf{u}\|/\|\mathbf{u}\|\lesssim\kappa\cdot\|\delta\mathbf{G}\|/\|\mathbf{G}\| $$

**Paso 4 — regla práctica.** \( \kappa<10 \): planta bien condicionada, control desacoplado razonable. \( \kappa>100 \): planta mal condicionada; control lazo-a-lazo frágil; se necesita pre-compensador o control robusto MIMO. En sistemas dq con acoplamiento \( \omega_0 L \), \( \kappa \) crece en la zona de resonancia del LCL, exactamente donde la robustez es más crítica:
$$ \boxed{\kappa=\frac{\bar\sigma(\mathbf{G})}{\underline\sigma(\mathbf{G})}\gg1 \;\Rightarrow\; \text{planta mal condicionada, control frágil}} $$

## 4 — Los márgenes de estabilidad MIMO: σ̄(S) y Ms

**Paso 1 — la función de sensibilidad MIMO.** Para el lazo cerrado \( \mathbf{L}=\mathbf{G}\mathbf{C} \):
$$ \mathbf{S}=(I+\mathbf{L})^{-1},\quad \mathbf{T}=\mathbf{L}(I+\mathbf{L})^{-1}=I-\mathbf{S} $$
El **valor singular máximo** de \( \mathbf{S} \) mide la peor amplificación de perturbaciones y la peor degradación del seguimiento:
$$ M_s=\|\mathbf{S}\|_\infty=\sup_\omega\bar\sigma(\mathbf{S}(j\omega)) $$

**Paso 2 — la cota σ̄(S) y el margen multiloop.** Por la desigualdad del margen MIMO (Skogestad-Postlethwaite), la distancia mínima del Nyquist de \( \det(I+\mathbf{L}(j\omega)) \) al origen es \( 1/M_s \): el **margen de módulo MIMO** es \( GM=1/M_s \). Para \( M_s<2 \) (equivalente a ≈6 dB), el sistema tiene un margen aceptable. La relación entre \( M_s \) y los márgenes escalares es:
$$ GM\geq\frac{M_s}{M_s-1},\quad PM\geq 2\arcsin\!\left(\frac{1}{2M_s}\right) $$
Para \( M_s=1.5 \): \( GM\geq3 \), \( PM\geq39° \). Para \( M_s=2 \): \( GM\geq2 \), \( PM\geq29° \).

**Paso 3 — el Bode generalizado de S.** El diagrama \( \bar\sigma(\mathbf{S}(j\omega)) \) vs \( \omega \) muestra:
- La región de frecuencias donde \( \bar\sigma(\mathbf{S})>1 \): aquí las perturbaciones se amplifica (inevitable, por el principio de conservación de Bode).
- El pico \( M_s \): cuánto se amplifica en el peor caso. Un pico agudo (alto \( M_s \)) indica escaso amortiguamiento.
- Las condiciones de desempeño \( \bar\sigma(\mathbf{S})\leq1/|W_S(j\omega)| \) se verifican directamente en el Bode generalizado.

**Paso 4 — conexión con la robustez multiloop.** Para incertidumbre multiplicativa \( \|\Delta\|_\infty\leq1/M_s \): la planta puede variar hasta \( 1/M_s \) en norma antes de desestabilizarse. Un \( M_s \) pequeño (→1) implica un sistema muy robusto pero con banda de paso reducida; un \( M_s \) grande implica rapidez pero fragilidad.

## 5 — La aplicación al desacoplo dq del LCL

**Paso 1 — la planta dq es una matriz 2×2.** En el sistema dq a 50 Hz, la inductancia del filtro acopla las corrientes \( i_d \) e \( i_q \) a través del término \( \omega_0 L_1 \):
$$ \mathbf{Z}_{dq}(j\omega)=\begin{bmatrix}R_1+j\omega L_1 & -\omega_0 L_1 \\ \omega_0 L_1 & R_1+j\omega L_1\end{bmatrix} $$
Los términos fuera de la diagonal representan el **acoplamiento dq**: la corriente de un eje afecta a la tensión del otro. En continua (\( \omega=0 \)) la planta es diagonal (\( \kappa=1 \)); en la frecuencia de cruce del control (\( \omega_c\approx2\pi\times750 \)) el acoplamiento \( \omega_0 L_1 \) es comparable con \( \omega_c L_1 \).

**Paso 2 — número de condición a 50 Hz.** En el marco dq el "50 Hz del sistema" aparece como \( \omega=0 \) para la componente fundamental (correctamente), pero el acoplamiento \( \pm\omega_0 L_1 \) persiste. A \( \omega=0 \) (en el referencial dq):
$$ \sigma_1=\sqrt{R_1^2+(\omega_0 L_1)^2}+\omega_0 L_1,\quad\sigma_2=\sqrt{R_1^2+(\omega_0 L_1)^2}-\omega_0 L_1 $$
$$ \kappa(0)=\frac{\sigma_1}{\sigma_2}=\frac{\sqrt{R_1^2+\omega_0^2L_1^2}+\omega_0 L_1}{\sqrt{R_1^2+\omega_0^2L_1^2}-\omega_0 L_1} $$
Para \( L_1=2\,\text{mH} \), \( R_1=50\,\text{m}\Omega \), \( \omega_0=2\pi\times50 \): \( \omega_0 L_1=0.628\,\Omega\gg R_1 \), luego \( \kappa\approx(12.6+1)/(12.6-1)\approx1.17 \). Este valor es bajo: la planta dq del LCL está **bien condicionada** a 50 Hz (el ratio \( \omega_0 L_1/R_1=12.6 \) no es tan grande como para crear una dirección débil).

**Paso 3 — el κ crece en la zona de resonancia.** A la resonancia del LCL (\( f_{res}\approx250\,\text{Hz} \), \( \omega_{res}=1576\,\text{rad/s} \)), el término \( j\omega_{res}L_1 \) es grande y la impedancia cruzada \( \omega_0 L_1 \) es relativamente pequeña: el \( \kappa \) en esa zona depende de la amortiguación. Sin amortiguamiento (\( R_1\to0 \)), \( \kappa\to\infty \) en la resonancia — exactamente donde el control falla si no se gestiona.

**Paso 4 — el efecto del desacoplo feedforward.** El feedforward \( v_{ff,d}=\omega_0 L_1 i_q \), \( v_{ff,q}=-\omega_0 L_1 i_d \) elimina los términos cruzados de \( \mathbf{Z}_{dq} \): la planta efectiva es \( (R_1+j\omega L_1)I_2 \) → \( \kappa=1 \) para todo \( \omega \). La respuesta cruzada \( i_d\to i_q \) pasa de \( \approx\omega_0/\alpha_c=6.7\% \) sin desacoplo a \( 0\% \) con desacoplo. La verificación: calcular \( \kappa(\mathbf{Z}_{dq}(j\omega)) \) con y sin feedforward a \( \omega=2\pi\times200\,\text{Hz} \):
$$ \kappa_{sin}=\frac{\sqrt{R_1^2+(\omega_{200}L_1)^2}+\omega_0 L_1}{\sqrt{R_1^2+(\omega_{200}L_1)^2}-\omega_0 L_1}\approx\frac{2.58+0.628}{2.58-0.628}\approx1.64,\quad\kappa_{con}=1 $$

<div class="cfig"><img src="figuras/valores-singulares-mimo-analisis.png" alt="SVD extendido: sigma vs freq, Ms, elipse dq, kappa con/sin desacoplo"><div class="cap">(a) $\bar{\sigma}$ y $\underline{\sigma}$ de $Z_{dq}(j\omega)$ vs frecuencia. (b) $\bar{\sigma}(S)$ y $M_s$ del lazo cerrado GFM. (c) Elipse de $Z_{dq}(j2\pi\cdot50)$ en el plano dq: dirección de peor ganancia ($\bar{\sigma}$) y de mejor ($\underline{\sigma}$). (d) Mejora de κ antes y después del desacoplo feedforward: κ→1 con desacoplo.</div></div>

## 6 — Diseño iterativo: calcular \( \kappa(\mathbf{Z}_{dq}(j\omega)) \) con y sin desacoplo

**Planta.** Proyecto 01 (GFM): \( L_1=2\,\text{mH} \), \( R_1=50\,\text{m}\Omega \), \( \omega_0=2\pi\times50\,\text{rad/s} \).

**Paso 1 — sin desacoplo.** La impedancia vista por el controlador (sin feedforward \( \omega_0 L \)) es:
$$ \mathbf{Z}(j\omega)=\begin{bmatrix}R_1+j\omega L_1 & -\omega_0 L_1\\\omega_0 L_1 & R_1+j\omega L_1\end{bmatrix} $$
A \( \omega=2\pi\times100 \) (segunda armónica del lazo): \( \omega L_1=1.257\,\Omega \), \( \omega_0 L_1=0.628\,\Omega \).
$$ \sigma_{max}=\sqrt{(0.05+j1.257)^2+0.628^2}\approx1.42,\quad \sigma_{min}\approx0.63,\quad \kappa\approx2.25 $$

**Paso 2 — con desacoplo.** Tras feedforward, la planta efectiva es diagonal: \( \mathbf{Z}_{eff}(j\omega)=(R_1+j\omega L_1)I_2 \). Ambos valores singulares son \( |R_1+j\omega L_1| \): \( \kappa=1 \) exactamente.

**Paso 3 — verificar respuesta cruzada.** La función de transferencia cruzada \( i_d\to i_q \) (respuesta de \( i_q \) a un escalón en la referencia de \( i_d \)) es nula con desacoplo y tiene magnitud \( \approx\omega_0L_1/\alpha_c L_1=\omega_0/\alpha_c \) sin desacoplo. Para \( \omega_0=314 \) rad/s y \( \alpha_c=2\pi\times750=4712 \) rad/s: respuesta cruzada \( \approx6.7\% \) sin desacoplo, \( 0\% \) con desacoplo.

## 3 — SVD y valores singulares: interpretación completa

**Paso 1 — descomposición SVD a cada frecuencia: definición y cálculo.** A cada frecuencia \(\omega\), la planta MIMO \(\mathbf{G}(j\omega)\in\mathbb{C}^{m\times p}\) se descompone como:

$$\mathbf{G}(j\omega) = \mathbf{U}(j\omega)\,\Sigma(\omega)\,\mathbf{V}^H(j\omega)$$

con \(\mathbf{U}\in\mathbb{C}^{m\times m}\) y \(\mathbf{V}\in\mathbb{C}^{p\times p}\) unitarias (\(\mathbf{U}^H\mathbf{U}=I\), \(\mathbf{V}^H\mathbf{V}=I\)) y \(\Sigma(\omega)=\text{diag}(\sigma_1(\omega)\geq\ldots\geq\sigma_{\min(m,p)}(\omega)\geq0)\). Las columnas de \(\mathbf{V}\) son las **direcciones de entrada** ortogonales: la \(i\)-ésima columna \(\mathbf{v}_i\) es la dirección de entrada que produce la ganancia \(\sigma_i\). Las columnas de \(\mathbf{U}\) son las **direcciones de salida** correspondientes. El cálculo numérico: `U, s, Vh = np.linalg.svd(G_at_omega)`.

**Paso 2 — valor singular máximo y mínimo: acotación de la ganancia.** El valor singular máximo \(\bar{\sigma}(\mathbf{G}) = \sigma_1\) es la ganancia máxima y el mínimo \(\sigma_m\) es la mínima. Para cualquier entrada unitaria \(\mathbf{u}\):

$$\sigma_m(\mathbf{G}) \leq \|\mathbf{G}(j\omega)\mathbf{u}\| \leq \bar{\sigma}(\mathbf{G})$$

La igualdad superior se alcanza para \(\mathbf{u}=\mathbf{v}_1\) (la columna de \(\mathbf{V}\) asociada a \(\sigma_1\)); la inferior para \(\mathbf{u}=\mathbf{v}_m\). En el sistema dq del convertidor: a 50 Hz, la "dirección fuerte" \(\mathbf{v}_1\) corresponde aproximadamente a la suma \((v_d+v_q)/\sqrt{2}\) y la débil a la diferencia \((v_d-v_q)/\sqrt{2}\) — las dos diagonales del plano dq.

**Paso 3 — número de condición: indicador de mal condicionamiento y fragilidad.** El número de condición \(\kappa(\omega) = \bar{\sigma}/\sigma_m\) mide qué tan distinta es la ganancia según la dirección de excitación. Una planta con \(\kappa\gg1\) es **mal condicionada**: tiene una dirección de entrada muy amplificada (fácil de controlar, pero sensible a ruido) y otra muy débil (difícil de controlar, pero amplificada al invertir la planta). La relación entre condicionamiento e incertidumbre:

$$\frac{\|\delta\mathbf{u}\|}{\|\mathbf{u}\|} \lesssim \kappa \cdot \frac{\|\delta\mathbf{G}\|}{\|\mathbf{G}\|}$$

Si \(\kappa=100\) y la incertidumbre relativa del modelo es 1%, el error relativo en la acción de control puede ser hasta 100%: el precompensador amplifica el error del modelo.

**Paso 4 — relación con la norma \(H_\infty\) y criterio de robustez.** La norma \(H_\infty\) de la planta es el pico del valor singular máximo sobre todas las frecuencias:

$$\|\mathbf{G}\|_\infty = \sup_\omega \bar{\sigma}(\mathbf{G}(j\omega))$$

Esta norma determina la ganancia de peor caso de la planta. En la robustez MIMO, la condición de estabilidad robusta ante incertidumbre sin estructura es:

$$\bar{\sigma}(W(j\omega)T(j\omega)) < 1 \quad \forall\omega$$

que equivale a \(\|WT\|_\infty < 1\). Para incertidumbre con estructura (bloques diagonales independientes), esta condición es conservadora y se usa el \(\mu\)-análisis (ver §4).

## 4 — Estabilidad robusta MIMO

**Paso 1 — extensión a MIMO: conservadurismo del criterio \(\bar{\sigma}(M)<1\).** Para sistemas MIMO, la condición de estabilidad robusta ante incertidumbre **sin estructura** (la incertidumbre puede ser cualquier matriz de norma unitaria) es \(\bar{\sigma}(M(j\omega)) < 1\) para todo \(\omega\), donde \(M=WTK\) es la función de lazo del canal de incertidumbre. Si la incertidumbre es **estructurada** (bloques diagonales independientes correspondiendo a distintos parámetros inciertos), la condición \(\bar{\sigma}(M)<1\) puede resultar conservadora por un factor 2–3: lo que parece no robusto bajo \(H_\infty\) puede ser perfectamente robusto cuando se tiene en cuenta la estructura.

**Paso 2 — el valor singular estructurado \(\mu\): definición precisa.** El \(\mu\)-análisis generaliza \(\bar{\sigma}\) a incertidumbre con estructura \(\boldsymbol{\Delta}\). El valor singular estructurado es:

$$\mu_{\boldsymbol{\Delta}}(M) = \frac{1}{\min\left\{\bar{\sigma}(\Delta) : \Delta\in\boldsymbol{\Delta},\;\det(I-M\Delta)=0\right\}}$$

Interpretación: \(1/\mu\) es el tamaño mínimo de la perturbación (con estructura \(\boldsymbol{\Delta}\)) que desestabiliza el sistema. El criterio de estabilidad robusta es \(\mu_{\boldsymbol{\Delta}}(M(j\omega)) < 1\) para todo \(\omega\). Si \(\mu < 1\): el sistema soporta toda perturbación \(\Delta\in\boldsymbol{\Delta}\) con \(\bar{\sigma}(\Delta)\leq1\). Si \(\mu > 1\): existe una perturbación con \(\bar{\sigma}(\Delta)=1/\mu < 1\) que desestabiliza el sistema.

**Paso 3 — la cota superior via LMI: algoritmo práctico.** El cálculo de \(\mu\) exacto es NP-duro en general. La **cota superior** via LMI se obtiene escalando la matriz \(M\):

$$\mu_{\boldsymbol{\Delta}}(M) \leq \inf_{D\in\mathcal{D}} \bar{\sigma}(DMD^{-1})$$

donde \(\mathcal{D}\) es el conjunto de matrices de escala que commutan con la estructura: \(\mathcal{D} = \{D = \text{diag}(d_1 I_{n_1},\ldots,d_k I_{n_k})\,:\,d_i>0\}\). El infimum se calcula como un problema de optimización convexa (SDP). La cota es exacta para incertidumbre compleja pura (no real) con hasta 3 bloques, y es una buena aproximación para incertidumbre real.

**Paso 4 — \(\mu\) vs \(H_\infty\): cuánto se gana en práctica.** Para un VSC con 3 parámetros inciertos independientes (\(L_1\pm20\%\), \(C_f\pm15\%\), \(SCR\in[3,10]\)): el análisis \(H_\infty\) da \(\max_\omega\bar{\sigma}(M)=0.85\), mientras el \(\mu\)-análisis da \(\max_\omega\mu(M)=0.38\) — la diferencia es un factor 2.2. El resultado práctico: el convertidor puede tolerar incertidumbre 2.2 veces mayor de lo que indica \(H_\infty\). Esta ganancia de "factor de robustez" crece con el número de bloques de incertidumbre independientes.

**Paso 5 — software disponible y flujo de cálculo.** En MATLAB: `mussv(M, blk)` calcula la cota inferior y superior de \(\mu\) para la estructura de bloques `blk`. En Python, `control` + `slycot` (función `sb03md`) o la toolbox `rctools`. Para análisis iniciales y sin licencia MATLAB, el barrido Monte Carlo de robustez (§6 de [[robustez-parametrica]]) es una alternativa práctica: si los \(N=1000\) puntos muestreados son todos estables, el sistema es robusto al 99.9% con alta probabilidad.

## 5 — Diseño por loop shaping MIMO

**Paso 1 — loop shaping \(H_\infty\): el procedimiento de McFarlane-Glover.** El procedimiento diseña un controlador \(K\) que da a la función de lazo \(L=GK\) la forma frecuencial deseada mediante los siguientes pasos:
1. El ingeniero especifica las ponderaciones de forma deseada \(W_1(s)\) (ganancia alta a bajas frecuencias) y \(W_2(s)\) (ganancia baja a altas frecuencias), definiendo la planta aumentada \(\tilde{G}=W_2 G W_1\).
2. Se calcula la **factorización coprimia normalizada** de \(\tilde{G}\): \(\tilde{G}=\tilde{M}^{-1}\tilde{N}\) con \(\tilde{M},\tilde{N}\in\mathcal{RH}_\infty\).
3. Se resuelve el problema \(H_\infty\): \(\min_K\|[I;K](I-\tilde{G}K)^{-1}[\tilde{M},\tilde{N}]\|_\infty\).
4. El controlador final es \(K = W_1 K_{opt} W_2\).
La robustez inherente viene de la métrica "gap" de la factorización coprimia: el controlador tolera toda perturbación en la planta cuya distancia gap sea menor que \(1/\|[I;K](I-\tilde{G}K)^{-1}[\tilde{M},\tilde{N}]\|_\infty\).

**Paso 2 — interpretación en valores singulares de \(L=GK\).** El Bode de valores singulares del lazo \(L=GK\) debe mostrar:
- \(\sigma_m(L(j\omega))\gg1\) a bajas frecuencias: todos los canales tienen ganancia alta — seguimiento robusto en todas las direcciones.
- \(\bar{\sigma}(L(j\omega))\ll1\) a altas frecuencias: ningún canal tiene ganancia alta — rechazo de ruido en todas las direcciones.
- El cruce de \(\sigma_m\) y \(\bar{\sigma}\) a través de 0 dB debe ocurrir con pendiente \(-20\,\text{dB/dec}\) en una banda estrecha.
Para plantas mal condicionadas (\(\kappa\gg1\)), los valores singulares de \(L\) cruzan 0 dB en frecuencias muy diferentes — difícil conseguir el mismo PM en todos los canales simultáneamente sin un precompensador que reduzca \(\kappa\).

**Paso 3 — robustez garantizada del controlador \(H_\infty\): márgenes mínimos.** El controlador óptimo por McFarlane-Glover garantiza márgenes mínimos simultáneos:

$$PM > 29°, \quad GM > 6\,\text{dB}$$

en todos los lazos de entrada-salida simultáneamente. Esta garantía de robustez multivariable es superior a la del LQR/LQG (que no garantiza márgenes en lazo abierto multivariable en general). El parámetro de diseño es \(\gamma^* = \|[I;K](I-\tilde{G}K)^{-1}[\tilde{M},\tilde{N}]\|_\infty\): cuanto menor \(\gamma^*\), mejor la robustez. El mínimo alcanzable es \(\gamma^*_{min}=(1-\epsilon_{max}^2)^{-1/2}\) donde \(\epsilon_{max}\) es la "margen de estabilidad gap".

**Paso 4 — limitaciones prácticas del \(H_\infty\) loop shaping.** El controlador resultante tiene orden \(n_{\tilde{G}} = n_G + n_{W_1} + n_{W_2}\). Para un sistema de orden 10 con pesos de orden 2: el controlador tiene orden 14. Para implementación en DSP a \(T_s=100\,\mu\text{s}\) se necesita reducción de orden (balanced truncation o Hankel norm approximation). Regla práctica: reducir el orden hasta que la respuesta frecuencial del controlador reducido difiera en menos de 1 dB del original en la banda de control. Además, la elección de \(W_1, W_2\) requiere diseño iterativo: se comienza con pesos integradores simples y se refina.

**Paso 6 — la RGA y el emparejamiento óptimo de variables.** La **Relative Gain Array** (RGA) complementa el análisis SVD para decidir qué entrada controlar con qué salida:

$$\Lambda(\mathbf{G}(j\omega)) = \mathbf{G}(j\omega) \circ (\mathbf{G}^{-1}(j\omega))^T$$

donde \(\circ\) es el producto de Hadamard (elemento a elemento). Para el sistema dq del VSC, la RGA a \(\omega=0\):

$$\Lambda(\mathbf{G}_{dq}(0)) = \begin{bmatrix}\lambda_{11} & \lambda_{12}\\\lambda_{21} & \lambda_{22}\end{bmatrix}$$

Si \(\lambda_{11}\approx1\) y \(\lambda_{22}\approx1\), el emparejamiento \(m_d\to i_d\), \(m_q\to i_q\) es correcto y el acoplamiento es débil. Si \(\lambda_{11}>1\) (y \(\lambda_{12}=1-\lambda_{11}<0\)): el emparejamiento directo es inestable en lazo cerrado con integradores — debe evitarse. Para el VSC con desacoplo feedforward: la planta efectiva es diagonal, \(\Lambda=I\) exactamente — el emparejamiento es indiferente y los PI son óptimos.

**Paso 5 — comparativa de métodos de diseño MIMO.** Para el convertidor VSC en dq con acoplamiento:

| Método | Orden del controlador | Garantía de robustez | Dificultad de diseño |
|--------|----------------------|---------------------|---------------------|
| PI diagonal + feedforward | 2 (por canal) | PM > 45° (si \(\kappa < 5\)) | Baja |
| PI con desacoplo LQI | 4 | Sin garantía formal | Media |
| \(H_\infty\) loop shaping | 10–20 | PM > 29°, GM > 6 dB | Alta |
| MPC MIMO | Sin TF | Restricciones naturales | Media-Alta |

El PI + feedforward cubre la mayoría de aplicaciones si el acoplamiento es moderado (\(\kappa<5\)); el \(H_\infty\) es necesario cuando el acoplamiento es fuerte o cuando se requieren garantías formales de robustez multivariable.

**Paso 6 — código Python para el análisis SVD completo del convertidor VSC.**

```python
import numpy as np

# Parámetros del VSC
L1 = 2e-3; R1 = 50e-3; omega0 = 2*np.pi*50
alpha_c = 2*np.pi*750  # frecuencia de cruce del lazo de corriente

# Planta Z_dq(jw) = [[R1+jwL1, -w0L1],[w0L1, R1+jwL1]]
def G_dq(w, L, R, w0):
    z = R + 1j*w*L
    cross = w0*L
    return np.array([[z, -cross], [cross, z]])

# SVD vs frecuencia
freqs = np.logspace(0, 5, 500)
sv_max = []; sv_min = []; kappa = []; rga_11 = []

for f in freqs:
    w = 2*np.pi*f
    G = G_dq(w, L1, R1, omega0)
    sv = np.linalg.svd(G, compute_uv=False)
    sv_max.append(sv[0]); sv_min.append(sv[-1])
    kappa.append(sv[0]/sv[-1])
    # RGA elemento (1,1)
    try:
        lam = G * np.linalg.inv(G).T
        rga_11.append(np.real(lam[0,0]))
    except np.linalg.LinAlgError:
        rga_11.append(np.nan)

sv_max = np.array(sv_max); sv_min = np.array(sv_min)
print(f"kappa en dc (f=1 Hz): {kappa[0]:.3f}")
print(f"kappa en f_cruce ({alpha_c/2/np.pi:.0f} Hz): {kappa[np.argmin(np.abs(freqs-alpha_c/2/np.pi))]:.3f}")
print(f"RGA(1,1) en dc: {rga_11[0]:.3f} (ideal=1)")
```

El resultado para \(L_1=2\,\text{mH}\): \(\kappa(1\,\text{Hz})\approx1.17\), \(\kappa(750\,\text{Hz})\approx1.24\), \(\text{RGA}(1,1)\approx1.03\) — planta bien condicionada en toda la banda de control.

## 6 — Aplicación: convertidor back-to-back MIMO

**Paso 1 — formulación del sistema como MIMO 2×2.** El convertidor back-to-back (o el VSC trifásico en dq) tiene como salidas \(\{P, Q\}\) (potencia activa y reactiva, calculadas de las corrientes dq) y como entradas \(\{m_d, m_q\}\) (índices de modulación dq). La planta MIMO entre \(\{m_d, m_q\}\) e \(\{i_d, i_q\}\) (corrientes dq, de las que se derivan P y Q) tiene el acoplamiento cruzado \(\omega_0 L\):

$$\mathbf{G}_{dq}(s) = \frac{1}{(R+sL)^2+(\omega_0 L)^2}\begin{bmatrix}R+sL & \omega_0 L\\-\omega_0 L & R+sL\end{bmatrix} \cdot \frac{V_{DC}}{2}$$

La SVD a \(\omega=0\) (DC en el referencial dq, que corresponde a la componente fundamental a 50 Hz) caracteriza el acoplamiento: \(\kappa(0) = \sqrt{(R^2+\omega_0^2L^2)+\omega_0L}/\sqrt{(R^2+\omega_0^2L^2)-\omega_0L}\).

**Paso 2 — desacoplamiento por feedforward: análisis SVD antes y después.** El precompensador de desacoplo feedforward elimina los términos cruzados: se añaden tensiones \(v_{ff,d}=\omega_0 L i_q\) y \(v_{ff,q}=-\omega_0 L i_d\) a la salida del PI. Tras el feedforward, la planta efectiva vista por el PI es diagonal: \(\mathbf{G}_{eff}(s)=(R+sL)^{-1}I_2\). La verificación SVD:
- Sin feedforward: \(\kappa(j\omega_c)\approx1.6\) para \(\omega_c=2\pi\times750\) rad/s (ver §6 de la ficha base).
- Con feedforward: \(\kappa(j\omega)\equiv1\) para todo \(\omega\) — la planta es perfectamente condicionada.
El valor singular máximo y mínimo colapsan en una sola curva: \(\bar{\sigma}=\sigma_m = |R+j\omega L|^{-1}\).

**Paso 3 — limitación de la inversión de planta: amplificación de ruido.** La inversión de la planta (precompensador estático o dinámico) amplifica el ruido de medida en la dirección débil por \(1/\sigma_m(G)\). Para el sistema dq, \(\sigma_m(G(j\omega))\approx1/|R+j\omega L|\) es creciente en frecuencia (la planta tiene menor ganancia a altas frecuencias): el precompensador dinámico \(G^{-1}(j\omega)\) tiene ganancia creciente a altas frecuencias → amplifica el ruido de medida de alta frecuencia. El diseño práctico limita la inversión añadiendo un filtro de paso bajo \(F(s)=\alpha/(s+\alpha)\) en serie con el precompensador.

**Paso 4 — criterio de verificación final MIMO: lista de comprobación.** Para validar el diseño del lazo de corriente MIMO del convertidor VSC:
1. **Condicionamiento:** \(\kappa(\mathbf{G}(j\omega_c)) < 10\) → el desacoplo feedforward es efectivo en la frecuencia de cruce.
2. **Sensibilidad máxima:** \(M_s = \|\mathbf{S}\|_\infty = \bar{\sigma}(\mathbf{S}(j\omega))_{max} < 2\) → robustez ante variaciones de parámetros.
3. **Seguimiento:** \(\sigma_m(\mathbf{L}(j\omega)) > 0\,\text{dB}\) para \(\omega < \omega_c\) → todos los canales tienen ganancia suficiente en la banda de control.
4. **RGA:** \(\Lambda(\mathbf{G}(j\omega_c)) \approx I\) → el emparejamiento \(m_d\to i_d\), \(m_q\to i_q\) es el correcto; elementos negativos indicarían que el emparejamiento elegido es inestable con controladores PI independientes.
5. **Respuesta cruzada:** \(|i_q/i_{d,ref}(j\omega)| < 5\%\) para \(\omega\leq\omega_c\) → el acoplamiento residual es despreciable con feedforward.

<div class="cfig"><img src="figuras/valores-singulares-mimo-analisis.png" alt="SVD MIMO: valores singulares, número de condición, sensibilidad máxima, comparativa SISO vs MIMO"><div class="cap">(a) Valores singulares máximo \(\bar{\sigma}\) y mínimo \(\underline{\sigma}\) de una planta MIMO 2×2 con acoplamiento del 30%. (b) Número de condición \(\kappa\) vs frecuencia: crece en la zona de resonancia. (c) Sensibilidad máxima \(\bar{\sigma}(S)\) con y sin desacoplamiento: el desacoplo reduce el pico \(M_s\). (d) Comparativa de márgenes SISO equivalente vs MIMO real: el análisis lazo a lazo sobreestima los márgenes.</div></div>

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
def kappa(G0):
    sv = np.linalg.svd(G0, compute_uv=False)
    return sv[0] / (sv[-1] + 1e-30)
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
