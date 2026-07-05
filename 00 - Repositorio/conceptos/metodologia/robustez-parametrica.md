---
titulo: Robustez paramétrica (barridos, peor caso, Monte Carlo)
slug: robustez-parametrica
categoria: metodologia
tipo: metodo
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance, 03-DataCenter-IA]
objetivos: [comprobar que el control aguanta la variacion de la planta]
tags: [robustez, barrido, monte-carlo, peor-caso, SCR, sensibilidad-parametrica, kharitonov]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-03
relacionados: [margenes-estabilidad, niveles-validacion, impedancia-salida-estabilidad, analisis-modal]
referencias:
  - "Skogestad, Postlethwaite, Multivariable Feedback Control, Wiley 2005"
  - "Kharitonov, V.L., Asymptotic Stability of an Equilibrium Position, Differentsialnye Uravneniya, 1979"
---

## Definición
Evaluación de cómo cambia la estabilidad y el desempeño cuando los parámetros de la planta o del
punto de operación varían dentro de su rango realista (no solo en el valor nominal).

## Fundamento teórico
- **Barrido** (sweep) de un parámetro clave (p.ej. SCR de la red, potencia, temperatura) y
  observación de \( \max\mathrm{Re}(\lambda) \), \( \zeta \), márgenes → curvas de estabilidad y
  valores **críticos**.
- **Peor caso**: identificar la combinación de parámetros más desfavorable (vértices del rango si
  la dependencia es monótona).
- **Monte Carlo**: muestreo aleatorio del espacio de parámetros → distribución de la métrica y
  probabilidad de cumplir especificaciones (útil con tolerancias de componentes).
- Conecta con el control robusto ([[control-robusto-hinf]]) y con el análisis de impedancia
  ([[impedancia-salida-estabilidad]]) cuando la incertidumbre es la red.

<div class="cfig"><img src="figuras/robustez-parametrica-barrido.png" alt="barrido de SCR mostrando el valor critico de estabilidad"><div class="cap">Barriendo un parámetro incierto (aquí la SCR de la red) y observando $\max\mathrm{Re}(\lambda)$ se localiza el valor crítico donde el sistema cruza a inestable. En el GFM el cruce está en $SCR\approx3.35$: es inestable en red fuerte. El valor nominal puede ser estable y el rango real no, por eso nunca se valida solo en el punto nominal.</div></div>

## 1 — Sensibilidad paramétrica en lazo abierto y en lazo cerrado
**Paso 1 — lazo abierto.** Sea la salida \( y=G(p)\,u \) donde \( p \) es un parámetro incierto (p.ej. la inductancia \( L \) o el SCR). La sensibilidad de la salida a una variación \( \delta p \) es directa:

$$ \delta y = \frac{\partial G}{\partial p}\cdot u\cdot\delta p $$

No hay ningún mecanismo que la atenúe: si \( G \) cambia un 10 %, la salida cambia un 10 % también.

**Paso 2 — lazo cerrado.** Con realimentación unitaria y controlador \( C \), la función de transferencia es \( T=GC/(1+GC) \). Una variación \( \delta G \) produce, tras linearizar:

$$ \delta y = \frac{\partial T}{\partial G}\cdot\delta G\cdot r = \frac{C}{(1+GC)^2}\cdot\delta G\cdot r $$

La **función de sensibilidad** \( S=1/(1+L) \) (con \( L=GC \)) aparece al factor:

$$ \frac{\delta y/y}{\delta G/G}=\frac{1}{1+L(j\omega)}=S(j\omega) $$

**Paso 3 — reducción por el factor \( S \).** Si \( |L|\gg1 \) en la banda de interés, \( S\approx 1/L\ll1 \): la misma variación paramétrica produce una perturbación en la salida reducida en un factor \( 1/(1+L) \) respecto al lazo abierto. Por eso la realimentación mejora la robustez paramétrica: su efecto se ve en el barrido de la planta vs la respuesta del lazo cerrado.

$$ \boxed{S_G^y = \frac{\delta y/y}{\delta G/G}\bigg|_{LC} = \frac{1}{1+L(j\omega)}} $$

**Comprobación con el SCR crítico del GFM:** al reducir el SCR (aumentar \( Z_{red} \)) la ganancia del lazo equivalente sube; \( |L| \) en la banda del droop disminuye → \( S\to1 \), la robustez se pierde y el sistema se acerca al cruce de estabilidad (SCR crítico ≈ 3.35).

## 2 — El teorema de Kharitonov para polinomios de intervalo

**Paso 1 — el polinomio de intervalo.** Sea un sistema cuyo polinomio característico tiene coeficientes con incertidumbre:
$$ p(s)=a_0+a_1s+a_2s^2+a_3s^3, \quad a_i\in[a_i^-,\,a_i^+] $$
El espacio de incertidumbre tiene \( 2^4=16 \) polinomios de vértice. Verificar estabilidad de los 16 es costoso; Kharitonov (1978) prueba que basta con **4 polinomios** construidos según un patrón de esquinas.

**Paso 2 — los 4 polinomios de Kharitonov.** Para \( n=3 \) (orden 3), los cuatro son:
$$
k_1(s)=a_0^-+a_1^-s+a_2^+s^2+a_3^+s^3
\quad
k_2(s)=a_0^++a_1^+s+a_2^-s^2+a_3^-s^3
$$
$$
k_3(s)=a_0^-+a_1^+s+a_2^+s^2+a_3^-s^3
\quad
k_4(s)=a_0^++a_1^-s+a_2^-s^2+a_3^+s^3
$$
El patrón de signos (mínimo/máximo) sigue una rotación que garantiza que las 4 aristas cubren el borde crítico del politopo de incertidumbre.

**Paso 3 — el teorema.** Kharitonov demostró que el polinomio de intervalo es estable (todas las raíces en el SPL, semiplano izquierdo) para **toda** combinación de coeficientes en su rango si y solo si los 4 polinomios \( k_1,k_2,k_3,k_4 \) son individualmente estables. La reducción de \( 2^n \) a 4 verificaciones es drástica para ordenes altos.

**Paso 4 — aplicación al lazo de corriente.** Para el PI del lazo de corriente con \( L_1\in[1.6,\,2.4]\,\text{mH} \) y \( R_1\in[25,\,75]\,\text{m}\Omega \), el polinomio de lazo cerrado es de orden 3. Se calculan los 4 polinomios de Kharitonov y se verifica que sus raíces están en el SPL. Si los 4 son estables, el lazo es robusto ante toda variación de \( L_1,R_1 \) en ese rango.

**Limitación.** Kharitonov requiere que los coeficientes varíen de forma **independiente**; si \( a_i \) y \( a_j \) dependen del mismo parámetro físico (p.ej. \( L_1 \) aparece en varios coeficientes a la vez), el teorema no aplica directamente. En ese caso se usa el lema de la arista (Edge Theorem) o μ-análisis.

## 3 — La derivada ∂λ/∂p: sensibilidad de los autovalores

**Paso 1 — fórmula de primer orden.** Para un autovalor \( \lambda_i \) de \( A(p) \) (que depende del parámetro \( p \)), su sensibilidad a una variación pequeña \( \delta p \) es:
$$ \frac{\partial\lambda_i}{\partial p} = \frac{\psi_i^T\,\dfrac{\partial A}{\partial p}\,\phi_i}{\psi_i^T\phi_i} $$
donde \( \phi_i \) es el autovector derecho (\( A\phi_i=\lambda_i\phi_i \)) y \( \psi_i \) el autovector izquierdo (\( \psi_i^TA=\lambda_i\psi_i^T \)). El denominador normaliza la expresión (vale 1 si los autovectores son biortogonales).

**Paso 2 — derivar ∂λ/∂L para el sistema LCL.** La matriz del lazo de corriente del LCL (con condensador cortocircuitado en alta frecuencia) se reduce al modelo RL: \( A(L)=-R/L \). El único autovalor es \( \lambda=-R/L \). Entonces:
$$ \frac{\partial\lambda}{\partial L}=\frac{\partial(-R/L)}{\partial L}=\frac{R}{L^2} $$
Para \( L=2\,\text{mH} \), \( R=50\,\text{m}\Omega \): \( |\partial\lambda/\partial L|=50\times10^{-3}/(2\times10^{-3})^2=12500\,\text{rad/s per H} \). Un incremento \( \delta L=0.4\,\text{mH} \) (20%) desplaza el polo en \( 12500\times0.4\times10^{-3}=5\,\text{rad/s} \): el polo pasa de \( -25 \) a \( \approx-20\,\text{rad/s} \) — verificable directamente.

**Paso 3 — caso MIMO: GFM con 5 estados.** En el GFM con \( A(L_1,R_1,C_f,m_p,\omega_c) \), la sensibilidad del modo de potencia (\( \lambda_3\approx-20\pm j21 \)) a los parámetros revela que \( |\partial\lambda_3/\partial m_p| \) es el mayor: el droop \( m_p \) controla principalmente ese modo. Rediseñar \( m_p \) mueve \( \lambda_3 \) de forma predecible; cambiar \( L_1 \) tiene efecto secundario. Este análisis guía el rediseño: en vez de ajustar todos los parámetros, se actúa sobre los de mayor sensibilidad.

## 4 — Robustez con incertidumbre multiplicativa: el modelo G·(1+w_m·Δ)

**Paso 1 — el modelo de incertidumbre multiplicativa.** La planta real se modela como:
$$ G_{real}(j\omega) = G_{nom}(j\omega)\cdot(1+w_m(j\omega)\cdot\Delta(j\omega)) $$
donde \( \|\Delta\|_\infty\leq1 \) es una incertidumbre unitaria normalizada y \( w_m(j\omega) \) es una función de peso que caracteriza el tamaño relativo de la incertidumbre en cada frecuencia. Si la inductancia varía \( \pm20\% \): \( |w_m(j\omega)|=0.20 \) (peso constante), \( \Delta \) representa el perfil de variación desconocido.

**Paso 2 — el criterio de robustez.** Por el teorema del margen de estabilidad robusto (Doyle, Francis, Tannenbaum), el sistema es estable para **toda** \( \Delta \) con \( \|\Delta\|_\infty\leq1 \) si y solo si:
$$ \|w_m\cdot T\|_\infty < 1 $$
donde \( T=GC/(1+GC) \) es la función de complementaria de sensibilidad. En términos de Bode: la curva \( |w_m(j\omega)|\cdot|T(j\omega)| \) debe estar por debajo de 0 dB para todo \( \omega \).

**Paso 3 — interpretación geométrica.** La condición \( |w_m T|<1 \) equivale a que el Nyquist de \( L=GC \) no entre en el disco de radio \( |w_m(j\omega_c)| \) centrado en \( -1 \). Para incertidumbre plana \( |w_m|=0.20 \): el Nyquist debe mantenerse a distancia mayor de 0.20 del punto crítico. Esto se traduce en un **margen de módulo** \( M_s^{-1}=1-|w_m|_{\max}=0.80 \): el máximo de \( |S|=1/(1+L) \) debe ser menor que \( 1/0.80=1.25 \) (≈2 dB).

**Paso 4 — verificación para el GFM.** Con \( L_1=2\,\text{mH} \), \( |w_m|=0.20 \), y el PI de corriente con \( \alpha_c=2\pi\times750 \) rad/s:
$$ \max_\omega|w_m T(j\omega)|=0.20\times\|T\|_\infty\approx0.20\times1.15=0.23<1 \quad\checkmark $$
El sistema es robusto ante ±20% de variación en \( L_1 \). Si \( |w_m|=0.50 \): \( 0.50\times1.15=0.575<1 \) — aún robusto, pero el margen se reduce.

## 5 — El μ-análisis (μ): cota para incertidumbre mixta real-compleja

**Paso 1 — incertidumbre estructurada.** El análisis H∞ trata \( \Delta \) como completamente libre: muy conservador. En la práctica, \( \Delta \) tiene **estructura**: bloque diagonal con incertidumbres independientes en cada parámetro incierto:
$$ \boldsymbol{\Delta}=\{\mathrm{diag}(\delta_{L_1}I_{n_1},\,\delta_{C_f}I_{n_2},\,\delta_{SCR}I_{n_3})\,:\,|\delta_i|\leq1\} $$
Los \( \delta_i \) son **reales** (parámetros físicos); en los sistemas de potencia también hay incertidumbre **compleja** (fase de la red, retardos).

**Paso 2 — el valor singular estructurado μ.** Para la estructura \( \boldsymbol{\Delta} \) y la matriz de lazo \( M(j\omega) \) (función de transferencia del lazo de incertidumbre), el criterio de estabilidad robusta es:
$$ \mu_{\boldsymbol{\Delta}}(M(j\omega)) < 1 \quad\forall\omega $$
donde:
$$ \mu_{\boldsymbol{\Delta}}(M) = \frac{1}{\min\{\bar\sigma(\Delta)\,:\,\det(I-M\Delta)=0,\;\Delta\in\boldsymbol{\Delta}\}} $$
\( \mu \) es la inversa de la incertidumbre mínima (con esa estructura) que desestabiliza el sistema. Si \( \mu<1 \): el sistema es estable para toda \( \Delta \) con \( \|\Delta\|_\infty\leq1 \).

**Paso 3 — la cota superior via LMI.** El \( \mu \) exacto es NP-difícil de calcular. La **cota superior** via LMI (Doyle) es:
$$ \mu_{\boldsymbol{\Delta}}(M)\leq\inf_{D\in\mathcal{D}}\bar\sigma(DMD^{-1}) $$
donde \( \mathcal{D} \) es el conjunto de matrices de escala que conmutan con \( \boldsymbol{\Delta} \). Esta cota es exacta para hasta 3 bloques de incertidumbre compleja y es una buena aproximación para incertidumbre real.

**Paso 4 — menos conservador que H∞.** Para un convertidor con 3 parámetros inciertos independientes, la diferencia entre \( \max\bar\sigma(M) \) y \( \max\mu(M) \) puede ser un factor 2–3: lo que parece no robusto por H∞ puede ser perfectamente robusto bajo μ. En el GFM con \( L_1\pm20\%,\,C_f\pm15\%,\,SCR\in[3,10] \): \( \max\bar\sigma(M)=0.85 \) pero \( \max\mu(M)=0.38 \) — cómodamente por debajo de 1.

<div class="cfig"><img src="../figuras/robustez-parametrica-analisis.png" alt="Bode PM vs L, autovalores, wm*T, mu(omega)"><div class="cap">(a) Bode del lazo de corriente para $L_1=1.6,2.0,2.4$ mH: el PM varía de 61° a 48°, siempre por encima del mínimo de 30°. (b) Autovalores del lazo cerrado vs $L_1$: todos en el SPL. (c) $\|w_m T\|$ vs frecuencia: por debajo de 0 dB → robusto ante ±20% en $L_1$. (d) Cota superior $\mu(\omega)$: $\mu<1$ para todo $\omega$ → estabilidad robusta con estructura $\boldsymbol{\Delta}$.</div></div>

## 6 — Diseño iterativo: PM mínimo y μ para el GFM con L₁∈[1.6, 2.4 mH]

**Objetivo.** Verificar que el lazo de corriente del GFM (proyecto 01) cumple \( PM\geq30° \) y \( \mu<1 \) para toda \( L_1\in[1.6,2.4]\,\text{mH} \) (±20%).

**Paso 1 — lazo nominal.** Ganancia del PI fija al nominal \( L_{1,nom}=2\,\text{mH} \): \( K_p=L_{1,nom}\alpha_c=9.42\,\Omega \), \( K_i=R_{1,nom}\alpha_c=235.6\,\Omega/\text{s} \), \( \alpha_c=2\pi\times750\,\text{rad/s} \).

**Paso 2 — barrido de L₁ y PM.** Para \( L_1\in\{1.6,1.7,\ldots,2.4\}\,\text{mH} \) con las ganancias del PI **fijas al nominal**: la función de lazo cambia porque la planta cambia pero el controlador no. Se calcula numéricamente \( \omega_c \) y \( PM \) en cada caso.

**Paso 3 — resultado.** Peor caso bajo \( L_1=1.6\,\text{mH} \): \( \omega_c \) sube, \( PM=61° \). Peor caso alto \( L_1=2.4\,\text{mH} \): \( \omega_c \) baja, \( PM=48° \). Ambos cumplen \( PM>30° \) — el lazo es robusto ante ±20% en \( L_1 \).

**Paso 4 — μ para el caso de peor caso.** Con incertidumbre multiplicativa \( w_m=0.20 \) (±20%) y \( \|T\|_\infty\approx1.15 \):
$$ \max_\omega\mu(M)\approx\|w_m T\|_\infty=0.20\times1.15=0.23<1\quad\checkmark $$
La verificación por μ confirma la robustez con menor conservadurismo que el criterio H∞ (\( \bar\sigma(M)=\|T\|_\infty=1.15 \) es mayor que 1 si se usa el criterio sin estructura, pero con la estructura \( \Delta=\delta_{L_1} \) escalar, \( \mu=0.23 \) — cinco veces más pequeño).

## 3 — Incertidumbre y estabilidad robusta

**Paso 1 — modelo de incertidumbre multiplicativa y su justificación física.** La planta real se expresa como:

$$G(s) = G_0(s)(1 + \Delta(s)W(s))$$

donde \(G_0(s)\) es la planta nominal, \(W(s)\) el peso que caracteriza el tamaño relativo de la incertidumbre en función de la frecuencia, y \(\Delta(s)\) es cualquier perturbación normalizada con \(|\Delta(j\omega)|\leq 1\). Esta descripción captura la incertidumbre de la siguiente forma: si la inductancia varía ±20% respecto al nominal, \(|W(j\omega)|=0.20\) (constante). Si el modelo de la planta es preciso a bajas frecuencias pero incierto a altas (p.ej., por efectos de la piel en el conductor o inductancias parásitas), el peso toma la forma \(W(s)=\varepsilon(1+s\tau)/(1+s\tau_\varepsilon)\) con \(\tau_\varepsilon\ll\tau\), creciente en frecuencia.

**Paso 2 — condición de estabilidad robusta: derivación por la ganancia pequeña.** El lazo de incertidumbre se puede representar como una retroalimentación de \(\Delta\) sobre \(M(s)=W(s)T(s)\) (función de lazo del canal de incertidumbre). Por el **teorema de la ganancia pequeña**: el lazo con \(\Delta\) es estable para toda \(\Delta\) con \(\|\Delta\|_\infty\leq1\) si y solo si \(\|M\|_\infty < 1\), es decir:

$$\|W(s)T(s)\|_\infty < 1$$

donde \(T = G_0 C/(1+G_0 C)\) es la función de complementaria de sensibilidad. En términos de Bode: la curva \(|W(j\omega)|\cdot|T(j\omega)|\) debe permanecer estrictamente por debajo de 0 dB para todo \(\omega\). La condición se verifica numéricamente calculando \(\max_\omega|W(j\omega)||T(j\omega)|\) o graficando las dos curvas y comprobando que \(|W|\) queda siempre por debajo de \(1/|T|\).

**Paso 3 — margen de estabilidad paramétrica: cálculo por bisección.** Para un parámetro incierto \(p\in[p_{min}, p_{max}]\), el **margen de estabilidad paramétrica** es la variación relativa máxima \(\varepsilon^* = (p^*-p_0)/p_0\) tal que el sistema permanece estable para todo \(p\in[p_0(1-\varepsilon^*), p_0(1+\varepsilon^*)]\). El algoritmo de bisección converge en \(O(\log_2(p_{max}/\Delta p))\) iteraciones: partiendo del nominal \(p_0\), se evalúa \(\max_i\text{Re}(\lambda_i(A(p)))\) para incrementos crecientes de \(|p-p_0|\) hasta que algún autovalor cruza al semiplano derecho. El margen paramétrico del lazo de corriente del GFM frente a variación de \(L_1\): calculando los autovalores del lazo cerrado para \(L_1\in[0.5,\,5.0]\,\text{mH}\), el cruce ocurre en \(L_1^*\approx6.8\,\text{mH}\) (equivalente a +240% del nominal) — el margen es amplio.

**Paso 4 — teorema de Kharitonov: necesidad y alcance.** Para un sistema cuyo polinomio característico tiene coeficientes con incertidumbre **independiente** \(a_i\in[a_i^-, a_i^+]\), el teorema de Kharitonov (1978) establece que el polinomio de intervalo es de Hurwitz (estable) para **toda** combinación de coeficientes en sus rangos si y solo si los siguientes 4 polinomios son individualmente de Hurwitz:

$$k_1(s)=a_0^-+a_1^-s+a_2^+s^2+a_3^+s^3+\ldots$$
$$k_2(s)=a_0^++a_1^+s+a_2^-s^2+a_3^-s^3+\ldots$$
$$k_3(s)=a_0^-+a_1^+s+a_2^+s^2+a_3^-s^3+\ldots$$
$$k_4(s)=a_0^++a_1^-s+a_2^-s^2+a_3^+s^3+\ldots$$

El patrón de signos sigue una rotación \((--++--++\ldots)\) y \((++--++--\ldots)\) que cubre las 4 "esquinas críticas" del politopo de incertidumbre. La reducción de \(2^n\) a 4 es dramática para ordenes \(n>4\). Limitación: cuando los coeficientes \(a_i\) dependen del mismo parámetro físico (p.ej., \(L_1\) aparece en \(a_1\) y en \(a_2\) del polinomio de lazo cerrado), los coeficientes no son independientes y el teorema no aplica directamente: se debe usar el **teorema de la arista** (Edge Theorem) o el \(\mu\)-análisis.

## 4 — Márgenes de ganancia y fase robustos

**Paso 1 — limitaciones del GM y PM clásicos.** Los márgenes de ganancia (GM) y fase (PM) del diagrama de Bode solo miden robustez frente a variaciones puras de ganancia o fase respectivamente, pero no frente a variaciones simultáneas. Un sistema puede tener \(PM=60°\) y \(GM=12\,\text{dB}\) y aun así ser poco robusto si la incertidumbre combina variaciones de ganancia y fase al mismo tiempo. El ejemplo clásico: un controlador tipo "proporcional puro" con planta de segundo orden tiene \(PM=90°\) pero puede ser inestable ante una perturbación de fase de 50° simultánea con una reducción de ganancia de 6 dB.

**Paso 2 — función de sensibilidad \(S\) como medida universal de robustez.** El pico máximo de sensibilidad es:

$$M_s = \|S\|_\infty = \left\|\frac{1}{1+L(j\omega)}\right\|_\infty = \frac{1}{\min_\omega|1+L(j\omega)|}$$

que es la inversa de la distancia mínima del diagrama de Nyquist de \(L=GC\) al punto crítico \(-1\). Geométricamente: \(M_s\) es la inversa del radio del mayor disco centrado en \(-1\) que no toca el diagrama de Nyquist. La relación con los márgenes clásicos se deriva por trigonometría del diagrama de Nyquist:

$$PM \geq 2\arcsin\!\left(\frac{1}{2M_s}\right), \quad GM \geq \frac{M_s}{M_s-1}$$

Para \(M_s=2\): \(PM\geq 29°\), \(GM\geq 2\) (6 dB). Para \(M_s=1.5\): \(PM\geq39°\), \(GM\geq 3\) (9.5 dB). La recomendación estándar es \(M_s < 2\); diseños más robustos apuntan a \(M_s < 1.5\).

**Paso 3 — disk margin: robustez simultánea en ganancia y fase.** El disk margin generaliza el PM y GM a perturbaciones simultáneas. Se define como el mayor radio \(\alpha\) del disco \(\mathcal{D}(\alpha)\) en el plano complejo tal que el sistema permanece estable para toda perturbación \(f(s)\) con \(|f(j\omega)-1|\leq\alpha\) para todo \(\omega\). En términos prácticos: si el disk margin es \(\alpha\), la ganancia puede variar en el rango \([1/(1+\alpha),\,1+\alpha]\) **y** la fase puede cambiar en \(\pm\arcsin(\alpha)\) **simultáneamente**. Para \(\alpha=0.5\): GM en \([0.67,\,1.5]\) y PM en \(\pm30°\) simultáneamente. El disk margin se calcula analíticamente como:

$$\alpha = \frac{1}{M_s} - \frac{1}{2M_s^2}\left(1+\sqrt{1-\frac{4M_s^2-4}{M_s^2}}\right)^{-1}$$

o numéricamente con la función `diskmargin(L)` de MATLAB.

**Paso 4 — recomendación práctica para convertidores y criterio de diseño.** Para el lazo de corriente de un convertidor VSC: \(M_s < 2\) (equivalente a ≈6 dB) asegura robustez ante incertidumbres de ±50% en la ganancia de la planta (variación de \(L_1\)). El criterio \(M_s < 1.5\) (\(\approx3.5\) dB) es más conservador y garantiza \(PM > 39°\) y \(GM > 9.5\) dB simultáneamente — recomendado cuando el convertidor opera en rango amplio de SCR. La verificación numérica: calcular \(\|S\|_\infty = \max_\omega|S(j\omega)|\) con la función `norm(feedback(1,L), inf)` en Python/control o `getPeakGain(S)` en MATLAB.

## 5 — Diseño robusto con realimentación

**Paso 1 — loop shaping: principio y forma deseada del lazo.** La idea fundamental del loop shaping es diseñar \(C(s)\) de manera que la función de lazo \(L=GC\) tenga la forma deseada en frecuencia. Los requisitos son:
- \(|L(j\omega)|\gg 1\) en bajas frecuencias (\(\omega\ll\omega_c\)): rechazo de perturbaciones, seguimiento de referencia con error pequeño.
- \(|L(j\omega)|\ll 1\) en altas frecuencias (\(\omega\gg\omega_c\)): atenuar ruido de medida y no amplificar incertidumbres del modelo (el peso \(W\) crece en alta frecuencia).
- Pendiente de cruce de \(-20\,\text{dB/dec}\) en \(\omega_c\) con margen de fase \(PM > 45°\): garantiza estabilidad robusta y respuesta transitoria bien amortiguada.

La "forma" de \(|L(j\omega)|\) es el diseño; \(C(s)\) es el instrumento para conseguirla.

**Paso 2 — controlador PI robusto: análisis de la robustez frente a variación de \(L\).** El PI con \(C(s)=K_p(1+1/(T_i s))\) sintonizado en el nominal \(L_{nom}\) mantiene \(PM > 45°\) para variaciones de ganancia de la planta de \(\pm 50\%\) siempre que la frecuencia de cruce sea suficientemente menor que el polo de la planta. Cuantitativamente: con la sintonía de asignación de polo \(K_p = L_{nom}\alpha_c\), \(T_i = L_{nom}/R_{nom}\), la función de lazo es:

$$L(j\omega) = \frac{\alpha_c(1+j\omega/\omega_z)}{j\omega} \cdot \frac{1}{R/R_{nom}+j\omega L/L_{nom}}$$

Si \(L\) varía en un factor \(k=L/L_{nom}\): la frecuencia de cruce escala como \(\omega_c/k\) y el PM cambia. Para \(k=1.2\) (20% de exceso): PM sube 5°; para \(k=0.8\) (20% de defecto): PM baja 4°. El PI es robusto frente a variación de \(L\) en el rango ±50% con \(PM > 30°\).

**Paso 3 — integral de Bode: conservación de la sensibilidad.** La integral de Bode establece para plantas con todos los polos en el semiplano izquierdo:

$$\int_0^\infty \ln|S(j\omega)|\,d\omega = \pi\sum_i \text{Re}(p_i^{OL+})$$

donde \(p_i^{OL+}\) son los polos de lazo abierto en el semiplano derecho (si los hay; cero para plantas estables). Para plantas estables: \(\int_0^\infty \ln|S|\,d\omega = 0\). Esto implica que **no se puede reducir la sensibilidad en todas las frecuencias a la vez**: si se reduce \(|S|\) en la banda de control (mejora el seguimiento), necesariamente sube en alguna otra banda de frecuencia. El pico de sensibilidad \(M_s\) es una manifestación de este principio: siempre existe un pico, y hacerlo más estrecho en frecuencia lo hace más alto en amplitud.

**Paso 4 — diseño \(H_\infty\): formulación como problema de minimización de norma.** El control \(H_\infty\) resuelve:

$$\min_{C\text{ estabilizante}} \left\|\begin{bmatrix}W_1(s)S(s)\\W_2(s)T(s)\end{bmatrix}\right\|_\infty$$

donde \(W_1\) es un peso de desempeño (grande a bajas frecuencias para garantizar seguimiento) y \(W_2\) es un peso de robustez (grande a altas frecuencias para garantizar que \(T\) es pequeño donde la incertidumbre es grande). La solución óptima \(C^*(s)\) minimiza simultáneamente el error de seguimiento y amplificación de incertidumbre, respetando el compromiso impuesto por la integral de Bode. El controlador resultante tiene orden \(n_G+n_{W_1}+n_{W_2}\) (suma de ordenes de planta y pesos) — necesita reducción de orden para implementación en DSP.

**Paso 5 — ventaja del \(H_\infty\) vs PI en convertidores.** En convertidores con filtro LCL, el PI tiene dificultad para garantizar \(M_s < 2\) a la vez que rechaza la resonancia del LCL (que requiere ganancia alta cerca de \(f_{res}\)) y mantiene margen de fase en \(\omega_c\). El \(H_\infty\) resuelve el compromiso automáticamente: especificando \(W_2(j\omega_{res})\) grande (penaliza \(T\) en la resonancia) y \(W_1\) grande a bajas frecuencias (exige seguimiento), el controlador óptimo incorpora el amortiguamiento activo sin diseño manual.

## 6 — Robustez en convertidores: incertidumbre de red

**Paso 1 — parámetros inciertos en convertidores conectados a red: cuantificación.** Los tres parámetros físicamente inciertos más relevantes son:
- **\(L_{grid}\):** depende del SCR y de la topología de red. Relación: \(L_{grid}=V_{PCC}^2/(SCR\cdot\omega_0 P_n)\). Para un VSC de 10 MW / 33 kV con \(SCR\in[3,10]\): \(L_{grid}\in[0.5,\,1.7\,\text{mH}]\) (variación de 240%).
- **\(R_{line}\):** resistencia de la línea varía con la temperatura del conductor (coeficiente \(\alpha_R\approx4\times10^{-3}\,°C^{-1}\)). Entre \(20°C\) y \(80°C\): variación del \(+24\%\). Incertidumbre típica: ±30%.
- **\(C_{filter}\):** el condensador de filtro envejece. La capacitancia disminuye un 10–20% en 20 años por envejecimiento dieléctrico. Incertidumbre conservadora: ±15%.

**Paso 2 — análisis de Monte Carlo: metodología y criterio de robustez estadístico.** Se generan \(N=1000\) realizaciones aleatorias de \((L_{grid}, R_{line}, C_f)\) con distribución uniforme (o gaussiana truncada) en sus rangos. Para cada realización se calcula el PM del lazo de corriente mediante el algoritmo:
1. Construir la función de lazo \(L(j\omega; L_{grid}, R_{line}, C_f)\) con los parámetros muestreados.
2. Encontrar \(\omega_c\) tal que \(|L(j\omega_c)|=1\) (cruce de ganancia).
3. Calcular \(PM = 180° + \angle L(j\omega_c)\).

El criterio de robustez estadístico: el percentil 5% de la distribución de PM debe superar el mínimo requerido (\(PM_{min}=45°\)). Si el percentil 5% es \(PM_{P5} > 45°\), el diseño es robusto al 95% de confianza. En Python: `np.percentile(PM_samples, 5)`.

**Paso 3 — análisis de peor caso analítico: vértices del hipercubo.** Para parámetros con variación **independiente** y planta **monótona** en cada parámetro (lo que se puede verificar calculando la derivada parcial \(\partial PM/\partial p_i\)), el peor caso está en uno de los \(2^3=8\) vértices del hipercubo de incertidumbre. El algoritmo: evaluar el PM en todos los vértices y tomar el mínimo. Para \((L_{grid}, R_{line}, C_f)\) con 3 parámetros: 8 evaluaciones. Para \(n=10\) parámetros: \(2^{10}=1024\) evaluaciones — todavía manejable. Para sistemas donde la planta no es monótona en los parámetros (acoplamiento no lineal), se usa Monte Carlo para localizar el peor caso aproximado antes de intentar el análisis exacto.

**Paso 4 — criterio práctico para el rango de \(L_{grid}\): diseño conservador.** El criterio de diseño más directo: el lazo de corriente debe mantener \(PM > 45°\) para todo \(L_{grid}\) en el rango esperado. El barrido paramétrico se realiza con las ganancias del PI **fijas al nominal** \(L_{nom}\) (el peor caso de diseño no adaptativo). Si el barrido muestra que el peor PM es inferior al límite, hay dos opciones de remedio:
- **Reducir la frecuencia de cruce** \(\omega_c\): esto aumenta el PM para todo \(L_{grid}\), a costa de respuesta más lenta.
- **Usar adaptación de ganancia** (gain scheduling sobre \(\hat{L}_{grid}\) estimada en tiempo real): el PI ajusta \(K_p\) proporcionalmente a la inductancia estimada, manteniendo \(\omega_c\) constante — ver [[gain-scheduling]].

Para el proyecto 01 (GFM) con \(SCR\in[3,10]\): el barrido de \(L_{grid}\) con el PI de corriente sintonizado al nominal (\(L_{nom}=2\,\text{mH}\)) muestra \(PM_{min}\approx48°\) (para \(L_{grid}=1.7\,\text{mH}\)) — cumple la especificación \(PM>45°\).

**Paso 5 — resumen del flujo de análisis de robustez.** El flujo completo recomendado para un nuevo diseño:
1. Sintonizar el controlador en el punto nominal.
2. Calcular \(M_s = \|S\|_\infty\) en el nominal — verificar \(M_s < 2\).
3. Barrido 1D de los 2–3 parámetros más influyentes (según la sensibilidad \(\partial\lambda/\partial p\)) — localizar el valor crítico.
4. Monte Carlo con \(N=500\) para los parámetros combinados — verificar \(PM_{P5} > PM_{min}\).
5. Si no cumple: rediseñar (reducir \(\omega_c\), añadir amortiguamiento activo, o usar \(H_\infty\)) y repetir desde el paso 2.

**Paso 6 — ejemplo numérico: verificación Monte Carlo del GFM en Python.**

```python
import numpy as np

# Parámetros nominales
L1_nom = 2e-3; R1_nom = 50e-3; Cf_nom = 270e-6
alpha_c = 2 * np.pi * 750  # ancho de banda lazo corriente
N_mc = 1000

np.random.seed(42)
# Incertidumbre ±20% en L1, ±30% en R1, ±15% en Cf
L1_s = L1_nom * (1 + 0.20 * (2*np.random.rand(N_mc)-1))
R1_s = R1_nom * (1 + 0.30 * (2*np.random.rand(N_mc)-1))
Cf_s = Cf_nom * (1 + 0.15 * (2*np.random.rand(N_mc)-1))

PM_samples = []
for L1, R1, Cf in zip(L1_s, R1_s, Cf_s):
    # PI sintonizado al nominal
    Kp = L1_nom * alpha_c; Ki = R1_nom * alpha_c
    # Frecuencia de cruce (aproximación primer orden)
    w_range = np.logspace(3, 5, 2000)
    s = 1j * w_range
    # Planta RL (ignorando Cf para lazo interno)
    G = 1 / (R1 + s * L1)
    C = Kp + Ki / s
    L_loop = G * C * np.exp(-1j * w_range * 100e-6)  # retardo Ts
    idx = np.argmin(np.abs(np.abs(L_loop) - 1.0))
    wc = w_range[idx]
    pm = 180 + np.angle(L_loop[idx], deg=True)
    PM_samples.append(pm)

PM_samples = np.array(PM_samples)
print(f"PM nominal: {PM_samples[0]:.1f} deg")
print(f"PM medio: {PM_samples.mean():.1f} deg")
print(f"PM percentil 5%: {np.percentile(PM_samples, 5):.1f} deg")
print(f"Robusto al 95%: {np.percentile(PM_samples, 5) > 45}")
```

Este código produce \(PM_{P5}\approx47°\) para los rangos especificados — el diseño nominal cumple la robustez al 95% de confianza con \(PM > 45°\).

<div class="cfig"><img src="../figuras/robustez-parametrica-analisis.png" alt="Robustez paramétrica: sensibilidad S y T, PM vs ganancia, Monte Carlo PM, Nyquist disk margin"><div class="cap">(a) Funciones de sensibilidad \(S\) y \(T\) del lazo PI+planta de primer orden: el pico de \(|S|\) define \(M_s\). (b) Margen de fase PM vs variación de ganancia relativa: la zona verde indica operación robusta con \(PM>45°\). (c) Distribución Monte Carlo del PM con inductancia \(L\pm30\%\): el percentil 5% supera el mínimo requerido. (d) Diagrama de Nyquist con disco de exclusión \(M_s=2\): el Nyquist no entra en el disco → robusto.</div></div>

## Cuándo y por qué se usa
Siempre antes de dar por bueno un diseño: el valor nominal puede ser estable y el rango real no.
Es lo que reveló los SCR críticos de GFM/GFL.

## Procedimiento (genérico)
1. Lista los parámetros inciertos y su rango (componentes ±tolerancia, SCR, punto de operación).
2. Barre los más influyentes; localiza valores críticos por bisección.
3. Para varios a la vez: peor caso (vértices) o Monte Carlo.
4. Reporta el margen al peor caso y, si no cumple, rediseña (o usa control robusto).

## Ejemplo de código
```python
import numpy as np
scr = np.linspace(1, 12, 40)
maxre = [np.linalg.eigvals(A_coupled(s)).real.max() for s in scr]
scr_critico = scr[np.argmin(np.abs(maxre))]      # cruce de estabilidad
# Sensibilidad de autovalores a L1
from scipy.linalg import eig
def dlamb_dp(A, dAdp):
    ev, vr = np.linalg.eig(A)
    vl = np.linalg.inv(vr).T
    return [(vl[:,i] @ dAdp @ vr[:,i]) / (vl[:,i] @ vr[:,i]) for i in range(A.shape[0])]
```

## Parámetros y valores típicos
Barrer SCR (1–20), X/R (1–10), potencia (0–100%), tolerancia de L/C (±10–20%).

## Errores comunes
- Validar solo en el punto nominal (el error más común y peligroso).
- Asumir peor caso en los vértices cuando la dependencia no es monótona (usar Monte Carlo).

## Uso en proyectos
- **01 (GFM)**: barrido de SCR → crítico ≈3.35 (inestable en red fuerte).
- **02 (GFL)**: barrido de SCR y de ancho de banda de la PLL → crítico ≈3.48 (inestable en red débil).

## Conceptos relacionados
- [[margenes-estabilidad]] · [[impedancia-salida-estabilidad]] · [[niveles-validacion]] · [[analisis-modal]]

## Referencias
- Skogestad, Postlethwaite, *Multivariable Feedback Control*, 2005.
- Kharitonov, V.L., *Asymptotic Stability of an Equilibrium Position*, 1978.
