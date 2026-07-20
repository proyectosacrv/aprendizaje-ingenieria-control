---
titulo: Control robusto (H∞, μ-síntesis)
slug: control-robusto-hinf
categoria: metodologia
tipo: metodo
nivel: avanzado
proyectos: []
objetivos: [garantizar estabilidad y desempeno ante incertidumbre]
tags: [robusto, H-infinito, mu-sintesis, incertidumbre, panorama]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [metodos-sintesis-control, funciones-sensibilidad, robustez-parametrica, margenes-estabilidad]
referencias:
  - "Skogestad, Postlethwaite, Multivariable Feedback Control, Wiley 2005 (cap. 8-9)"
---

## Definición
Métodos que diseñan el controlador para el **peor caso** de incertidumbre del modelo, ofreciendo
**garantías** de estabilidad y desempeño. \(H_\infty\) minimiza la norma infinito (el pico en
frecuencia) de funciones de transferencia ponderadas; la \(\mu\)-síntesis trata incertidumbre
estructurada.

## Fundamento teórico
Se formula con **pesos** \( W_S, W_T, W_u \) que dan forma a las funciones de [[funciones-sensibilidad]]:
$$ \min_C \left\| \begin{matrix} W_S S \\ W_u KS \\ W_T T \end{matrix} \right\|_\infty $$
El resultado garantiza que \( S, T \) quedan bajo las plantillas \( 1/W \). La incertidumbre del
modelo se modela como bloques \( \Delta \) acotados; el teorema de la ganancia pequeña / \( \mu \)
da la condición de robustez.

<div class="cfig"><img src="figuras/control-robusto-hinf-sensibilidad.png" alt="conformado de las funciones de sensibilidad S y T con sus plantillas"><div class="cap">El diseño $H_\infty$ conforma las funciones de sensibilidad: $|S|$ debe quedar baja a baja frecuencia (buen seguimiento/rechazo) y $|T|$ baja a alta frecuencia (robustez al ruido y a la incertidumbre). Los pesos $W_S,W_T$ fijan esas plantillas $1/W$ y el optimizador minimiza el pico de las transferencias ponderadas.</div></div>

## 1 — La norma \( H_\infty \): definición y por qué es el pico del Bode
**Paso 1 — norma de un sistema MIMO.** Para un sistema estable con matriz de transferencia \( \mathbf{H}(s) \), la norma \( H_\infty \) se define como la ganancia energética peor caso de entrada a salida:

$$ \|\mathbf{H}\|_\infty = \sup_{\omega\in\mathbb{R}}\,\bar\sigma\bigl(\mathbf{H}(j\omega)\bigr) $$

donde \( \bar\sigma \) es el valor singular máximo. En SISO reduce a \( \max_\omega|H(j\omega)| \), el pico de la respuesta en amplitud (pico del Bode). En MIMO es el pico de la ganancia máxima sobre todas las frecuencias **y** todas las direcciones de entrada.

**Paso 2 — interpretación energética.** Para señales en \( L_2 \) (energía finita), \( \|\mathbf{H}\|_\infty \) es la ganancia \( L_2\to L_2 \) inducida:

$$ \|\mathbf{H}\|_\infty = \sup_{u\neq0}\frac{\|y\|_{L_2}}{\|u\|_{L_2}} $$

Minimizar \( \|\mathbf{H}\|_\infty \) equivale a minimizar la amplificación máxima de energía: si \( \mathbf{H}=W_S S \), ello obliga a \( |S(j\omega)|<1/|W_S(j\omega)| \) en toda la banda, es decir el diseño queda acotado por la plantilla \( 1/W_S \).

**Paso 3 — el problema de síntesis.** El objetivo es encontrar \( C \) que minimice:

$$ \gamma^* = \min_C \left\|\begin{pmatrix}W_S S \\ W_u KS \\ W_T T\end{pmatrix}\right\|_\infty = \min_C \sup_\omega \bar\sigma\!\left[\begin{pmatrix}W_S S \\ W_u KS \\ W_T T\end{pmatrix}\!(j\omega)\right] $$

$$ \boxed{\text{El controlador } H_\infty \text{ garantiza: } |S(j\omega)|<1/|W_S(j\omega)|\ \forall\omega} $$

La solución se obtiene mediante ecuaciones de Riccati o LMIs; el orden del controlador es el de la planta aumentada (planta + pesos).

## 2 — Interpretación de los pesos y conexión con la robustez
**Paso 1 — peso \( W_S \).** \( W_S(s) \) es la plantilla inversa para la sensibilidad \( S=1/(1+L) \). Un peso de la forma \( W_S=(\omega_b/s+a)/(1+\omega_b M_s/s) \) (integrador a baja frecuencia) impone: cruce por debajo de \( 1/M_s \) a alta frecuencia (margen de pico) y atenuación creciente a baja frecuencia (rechazo de perturbación y seguimiento).

**Paso 2 — peso \( W_T \).** \( W_T \) conforma \( T=L/(1+L) \); un peso alto a alta frecuencia fuerza \( T \to 0 \) (caída de ganancia), lo que equivale a limitar el ancho de banda y garantizar robustez ante incertidumbre multiplicativa de alta frecuencia.

**Paso 3 — margen de robustez.** La condición de estabilidad robusta ante incertidumbre multiplicativa \( \Delta \) con \( \|\Delta\|_\infty\le 1/\|W_T^{-1}\|_\infty \) es exactamente \( \|W_T T\|_\infty<1 \), que el optimizador garantiza. Es la formalización en norma del límite empírico \( \|T\|_\infty < 1.5\text{–}2 \).

## 3 — Problema estándar \(H_\infty\): planta aumentada y bucle de Youla

El problema estándar formula el control como la minimización de la norma \(H_\infty\) del sistema de lazo cerrado generalizado \(F_l(P,K)\):

$$\min_{K \text{ estabilizante}} \|F_l(P_{aug}, K)\|_\infty < \gamma$$

La planta aumentada \(P_{aug}\) combina la planta real \(G\) con los pesos \(W_1, W_2, W_u\):

$$P_{aug}(s) = \begin{pmatrix} W_1(s) & -W_1(s)G(s) \\ 0 & W_u(s) \\ 0 & W_2(s)G(s) \\ I & -G(s) \end{pmatrix}$$

El controlador \(K\) cierra el lazo entre los puertos de error \(e\) y las señales de control \(u\). El resultado es que minimizar \(\|F_l(P_{aug},K)\|_\infty\) equivale a resolver simultáneamente:

$$\|W_1 S\|_\infty < 1, \quad \|W_u KS\|_\infty < 1, \quad \|W_2 T\|_\infty < 1$$

<div class="cfig"><img src="figuras/control-robusto-hinf-analisis.png" alt="Control robusto H-inf: pesos W1/W2, funciones S/T, región de incertidumbre y respuesta robusta"><div class="cap">(a) Pesos W1 y W2 en Bode: W1 grande a baja frecuencia, W2 grande a alta frecuencia. (b) S y T resultantes con y sin control H-inf. (c) Región de incertidumbre multiplicativa y disco de estabilidad robusta. (d) Respuesta robusta del sistema ante variación de Lgrid ×0.5 a ×2.</div></div>

## 4 — Diseño de pesos \(W_1(s)\), \(W_2(s)\): plantillas de sensibilidad

Los pesos son el lenguaje del diseñador para expresar los requisitos de desempeño:

**Peso \(W_1(s)\) para seguimiento y rechazo de perturbaciones:**

$$W_1(s) = \frac{s/M_s + \omega_b}{s + \omega_b\,\varepsilon}$$

- \(M_s\): máximo pico de sensibilidad permitido (típico: \(M_s = 2\), equivale a GM = 6 dB, PM = 29°)
- \(\omega_b\): ancho de banda de seguimiento (frecuencia donde \(|S|\) sube a 1)
- \(\varepsilon \ll 1\): asegura que \(|W_1(0)| = 1/\varepsilon \gg 1\) (alta ganancia DC = tracking)

**Peso \(W_2(s)\) para robustez a alta frecuencia:**

$$W_2(s) = \frac{s + \omega_t/\sqrt{M_t}}{(\sqrt{M_t}\,s + \omega_t)}$$

- \(M_t\): máximo pico de complementaria \(T\) (típico: \(M_t = 1.25\), equivale a 2 dB de pico)
- \(\omega_t\): frecuencia a partir de la cual se exige caída de \(T\)

**Selección práctica:** para un lazo de corriente de 1 kHz con incertidumbre de \(L_{grid}\) de ×2: \(\omega_b = 2\pi\cdot200\,\text{rad/s}\), \(\omega_t = 2\pi\cdot3000\,\text{rad/s}\), \(M_s = 2\), \(M_t = 1.25\).

## 5 — Solución: ecuaciones de Riccati y reducción de orden

**Teorema de Doyle-Glover-Khargonekar-Francis (1989):** existe \(K\) tal que \(\|F_l(P_{aug},K)\|_\infty < \gamma\) si y solo si:

1. Las ecuaciones de Riccati \(X_\infty \geq 0\) y \(Y_\infty \geq 0\) tienen soluciones estabilizantes.
2. \(\rho(X_\infty Y_\infty) < \gamma^2\) (producto de los radios espectrales).

El controlador óptimo tiene orden igual a la planta aumentada (orden de \(G\) + orden de los pesos). Para la planta de lazo de corriente de primer orden + 2 pesos de primer orden: orden del controlador = 3.

**Reducción de orden (truncamiento balanceado):**
1. Calcular la descomposición balanceada: \(W_c = W_o = \Sigma = \text{diag}(\sigma_1 \geq \sigma_2 \geq \ldots)\)
2. Retener los \(k\) estados con \(\sigma_i > 0.01\,\sigma_1\)
3. Verificar que el error \(\|G_{red} - G_{orig}\|_\infty \leq 2\sum_{i>k}\sigma_i\)

En la práctica, un controlador H\(\infty\) de orden 5–8 se reduce a un PI equivalente de orden 2 con pérdida de robustez < 0.5 dB.

## 6 — Aplicación en convertidores: armónicos, variación de \(L_{grid}\)

**Rechazo robusto de armónicos:** si la red inyecta perturbaciones de corriente en el armónico 5° (250 Hz), se añade un pico al peso \(W_1(s)\) en esa frecuencia:

$$W_1(s) \leftarrow W_1(s)\cdot\frac{s^2 + 2\zeta_n\omega_h s + \omega_h^2}{s^2 + 2\zeta_d\omega_h s + \omega_h^2}, \quad \omega_h = 2\pi\cdot250, \; \zeta_n \ll \zeta_d$$

Esto obliga al controlador a tener alta ganancia en 250 Hz (rechazo de perturbación armónica) sin necesidad de un controlador resonante explícito.

**Robustez ante variación de \(L_{grid}\):** en red débil, \(L_{grid}\) puede variar de \(L_{min}\) a \(L_{max} = 4\,L_{min}\). El modelo nominal usa \(L_{nom} = 2\,L_{min}\). La incertidumbre multiplicativa:

$$\Delta_m(s) = \frac{G(s,L) - G(s,L_{nom})}{G(s,L_{nom})}, \quad |\Delta_m(j\omega)| \leq \ell_m(\omega)$$

Se escoge \(W_2(s) \geq \ell_m(\omega)\) → el H\(\infty\) garantiza estabilidad para cualquier \(L_{grid} \in [L_{min}, L_{max}]\).

**Comparación con PI clásico:** el PI tiene PM = 45° en \(L_{nom}\); si \(L_{grid} = L_{max}\), el PM cae a 15° → riesgo de inestabilidad. El H\(\infty\) diseñado con la incertidumbre explícita mantiene PM > 30° en todo el rango.

## 7 — μ-síntesis: incertidumbre estructurada y el valor singular estructurado

El H∞ trata la incertidumbre como un bloque \(\Delta\) sin estructura (norma acotada). La μ-síntesis permite tratar incertidumbre **estructurada**: bloques \(\Delta\) que representan variaciones paramétricas específicas (p.ej. \(L\in[0.5L_0, 2L_0]\) y \(R\in[0.5R_0, 2R_0]\) de forma independiente).

**El valor singular estructurado.** Para un sistema con incertidumbre estructurada \(\Delta\in\mathbf{\Delta}\):

$$\mu_{\mathbf{\Delta}}(M) = \frac{1}{\min\{\bar{\sigma}(\Delta) : \Delta\in\mathbf{\Delta},\,\det(I-M\Delta)=0\}}$$

La condición de estabilidad robusta es \(\mu_{\mathbf{\Delta}}(M(j\omega)) < 1\) para todo \(\omega\). Comparado con el H∞ (que exige \(\bar{\sigma}(M)<1\) — conservador porque ignora la estructura), la μ-síntesis puede ser menos conservadora.

**Algoritmo D-K iteration.** La μ-síntesis se resuelve iterando:
1. **K-step:** dado \(D(\omega)\), resolver un H∞ estándar para obtener \(K\).
2. **D-step:** dado \(K\), calcular \(\mu\) y ajustar las escalas \(D(\omega)\) para minimizarla.

La convergencia no está garantizada en general, pero en la práctica 3–5 iteraciones suelen ser suficientes. El resultado es un controlador con garantías más precisas que el H∞ para la incertidumbre estructurada especificada.

## 8 — Robustez ante variación de Lgrid: diseño cuantitativo

**Problema.** Un inversor GFL diseñado para SCR=10 (\(L_g=L_{g,nom}\)) opera en una red donde \(L_g\) puede variar entre \(L_{g,nom}/4\) (SCR=40) y \(4L_{g,nom}\) (SCR=2.5). El margen de fase del PI clásico:

| \(L_g/L_{g,nom}\) | SCR | PM (PI clásico) | PM (H∞) |
|---|---|---|---|
| 0.25 | 40 | 58° | 48° |
| 1 (nominal) | 10 | 45° | 42° |
| 4 | 2.5 | **12°** | 32° |

El PI clásico colapsa el margen de fase a 12° con \(L_g=4L_{g,nom}\): riesgo real de inestabilidad. El controlador H∞ diseñado con \(W_2\geq|\Delta_m(j\omega)|\) mantiene PM>30° en todo el rango. Coste: el margen en el punto nominal es ligeramente menor (42° vs 45°), pero es el precio de la robustez.

**Procedimiento cuantitativo:**
1. Calcular la incertidumbre multiplicativa: \(\ell_m(\omega)=\max_{L_g}|G(j\omega,L_g)/G(j\omega,L_{nom})-1|\).
2. Ajustar \(W_2(j\omega)\geq\ell_m(\omega)\) en todo el barrido de frecuencias.
3. Resolver el H∞ → verificar PM en cada \(L_g\) del rango.

## 9 — Norma H2 vs H∞: cuándo usar cada una

La norma H2 de un sistema es la energía RMS de su respuesta al impulso:

$$\|H\|_2^2 = \frac{1}{2\pi}\int_{-\infty}^{\infty}\text{tr}[H(j\omega)^*H(j\omega)]\,d\omega = \int_0^\infty\text{tr}[h(t)^Th(t)]\,dt$$

Minimizar \(\|H\|_2\) corresponde a minimizar la varianza de la salida ante ruido blanco gaussiano → es la solución del LQG (Kalman + LQR). Es el criterio óptimo cuando las perturbaciones son **estocásticas** con distribución conocida.

La norma H∞ es el criterio correcto cuando las perturbaciones son **deterministas con energía acotada** (señales \(L_2\)), que es el caso de perturbaciones de red (huecos, armónicos) en convertidores de potencia. La solución H∞ es más conservadora que la H2 (tiene peor desempeño medio) pero garantiza el peor caso.

**Regla práctica.** Para convertidores de red: usar H∞ cuando la variación paramétrica (SCR, temperatura) supera el ±50 %; usar LQG/H2 cuando los parámetros son bien conocidos y las perturbaciones son estocásticas (ruido de medición, variación aleatoria de carga).

## 10 — Implementación práctica: reducción y discretización del controlador H∞

**Reducción de orden.** El controlador H∞ de orden \(n_K = n_G + n_{W1} + n_{W2}\) puede ser de orden 5–20 para un lazo de corriente sencillo. La reducción de orden usa el truncamiento balanceado:

```python
from scipy import linalg
import control

# Obtener el controlador H-inf (orden alto)
K_hinf = ...  # resultado del solver H-inf

# Reducción por truncamiento balanceado
K_red, hsv = control.balred(K_hinf, orders=range(1, n_K+1))
# Conservar el orden k tal que hsv[k]/hsv[0] > 0.01
k_opt = np.sum(hsv/hsv[0] > 0.01)
K_final = K_red[k_opt]
```

**Discretización.** El controlador reducido se discretiza con la transformación bilineal (Tustin) para preservar las propiedades de frecuencia:

$$s \to \frac{2}{T_s}\cdot\frac{z-1}{z+1}$$

La discretización bilineal preserva la estabilidad y los ceros de la función de transferencia, y su error de frecuencia es \(O(T_s^2)\). Para el lazo de corriente con \(T_s=100\,\mu\text{s}\) y ancho de banda 1 kHz, la bilineal da error de ganancia <1% en la banda de interés.

## 11 — Herramientas Python para H∞: python-control y slycot

```python
import control
import numpy as np
from control.matlab import hinfsyn

# Modelo nominal: inductor L1 con resistencia R1
L1 = 2e-3; R1 = 0.1
G = control.tf([1], [L1, R1])

# Pesos
wb = 2*np.pi*200; Ms = 2; eps = 0.01
W1 = control.tf([1/Ms, wb], [1, wb*eps])  # plantilla S
wt = 2*np.pi*3000; Mt = 1.25
W2 = control.tf([1, wt/np.sqrt(Mt)], [np.sqrt(Mt), wt])  # plantilla T

# Planta aumentada y síntesis H-inf
# (requiere slycot instalado: pip install slycot)
P = control.augw(G, W1, None, W2)
K, CL, gam, rcond = hinfsyn(P, nmeas=1, ncon=1)
print(f"gamma_opt = {gam:.4f}")
```

El parámetro `gam` es el valor óptimo de \(\gamma\); si \(\gam<1\), las plantillas de sensibilidad se cumplen estrictamente.

## 12 — μ-síntesis aplicada al GFL en red de SCR variable

**Problema concreto.** El inversor GFL opera en una red donde el SCR varía entre 1.5 y 20 según la configuración de la red (N-1, mantenimientos). El objetivo es garantizar PM>30° en todo el rango.

**Modelo de incertidumbre estructurada.** Definir el bloque de incertidumbre como:

$$\Delta = \begin{pmatrix}\delta_{Lg} & 0 \\ 0 & \delta_{Rg}\end{pmatrix}, \quad |\delta_{Lg}|, |\delta_{Rg}| \leq 1$$

donde \(\delta_{Lg}\) representa la variación normalizada de \(L_g\) en \([L_{min}, L_{max}]\) y \(\delta_{Rg}\) de \(R_g\). La planta perturbada:

$$G(s, \delta) = G_0(s)\left(1 + W_{\Delta}(s)\Delta\right)$$

**Resultado.** La μ-síntesis con esta estructura produce un controlador de orden 7 (planta 1er orden + 2 pesos 1er orden + 2 bloques de incertidumbre = 1+2+2 = 5 estados, reducido por truncamiento balanceado a 3 estados efectivos). El controlador garantiza PM>30° para SCR∈[1.5, 20] con una degradación del rendimiento nominal de menos del 5%.

## 13 — Loop shaping robusto: el método de McFarlane-Glover

El loop shaping de McFarlane-Glover ofrece una alternativa más intuitiva al H∞ estándar. El diseñador especifica directamente la forma deseada del lazo \(L_0(s)=G(s)K_0(s)\) y el algoritmo encuentra el controlador que "envuelve" ese lazo con garantías de robustez máxima:

1. **Diseñar \(K_0(s)\)** para que \(L_0(s)\) tenga la forma deseada en Bode (pendiente -20 dB/dec en el cruce, caída rápida a alta frecuencia).
2. **Calcular la robustez máxima** \(\varepsilon_{max} = 1/\|[I+L_0]^{-1}[I, G]\|_\infty\) — mide cuánta perturbación coprime puede soportar el sistema.
3. **Refinar el controlador** si \(\varepsilon_{max}>0.3\): el sistema tiene robustez amplia. Si \(\varepsilon_{max}<0.2\): la forma del lazo tiene algo que lo hace inherentemente difícil de controlar.

**Ventaja.** El diseñador mantiene la intuición del loop shaping clásico mientras obtiene garantías de robustez cuantificadas. Es el método preferido cuando se parte de un PI bien ajustado y se quiere añadir garantías formales sin reformular todo el problema desde cero.

## 14 — Ejemplo de código: síntesis H∞ con python-control

```python
import numpy as np
import control

# Planta: inductor L1 con R1 (lazo corriente convertidor)
L1 = 2e-3; R1 = 0.1
s = control.tf('s')
G = 1 / (L1*s + R1)

# Pesos de diseño
wb = 2*np.pi*200  # ancho de banda de seguimiento
Ms = 2.0          # pico máximo de S
eps = 0.01        # ganancia DC de S (alta ganancia DC)
W1 = (s/Ms + wb) / (s + wb*eps)

wt = 2*np.pi*3000  # frecuencia de caída de T
Mt = 1.25
W2 = (s + wt/np.sqrt(Mt)) / (np.sqrt(Mt)*s + wt)

# Planta aumentada (manual para fines didácticos)
# P = [W1; 0; 1] * [-W1*G; 0; W2*G; -G]  (forma estándar 2-bloques)
# Usando python-control:
P = control.augw(G, W1, None, W2)
K, CL, gam, rcond = control.hinfsyn(P, nmeas=1, ncon=1)
print(f"gamma_optimo = {gam:.4f}")
print(f"Orden del controlador: {K.nstates}")

# Verificar PM del controlador H-inf
L = K * G
gm, pm, wgc, wpc = control.margin(L)
print(f"PM = {pm:.1f}°, GM = {20*np.log10(gm):.1f} dB")
```

El resultado típico para esta planta con estos pesos: \(\gamma_{opt}\approx0.85<1\) (las plantillas se cumplen), PM\(\approx55°\), controlador de orden 3 (reducible a PI+lead).

## 15 — Conexión entre H∞ y el análisis de impedancia para estabilidad

El análisis de estabilidad por impedancia (criterio de Middlebrook, ESAC) y la síntesis H∞ son dos caras de la misma moneda: la primera verifica, la segunda diseña.

**H∞ como diseño de impedancia.** Si se define el peso de robustez \(W_2(s)=|Z_{red}(j\omega)|/Z_{ref}\) (escalado por la impedancia de referencia deseada), minimizar \(\|W_2 T\|_\infty<1\) equivale a diseñar un convertidor cuya impedancia de salida \(Z_{inv}\) satisface el criterio de Middlebrook frente a \(Z_{red}\):

$$\|W_2 T\|_\infty < 1 \implies |T(j\omega)| < |Z_{ref}/Z_{red}(j\omega)| \implies \text{Middlebrook cumplido}$$

El H∞ así formulado entrega directamente un controlador que garantiza la estabilidad del sistema convertidor-red para toda la clase de redes \(|Z_{red}|<Z_{ref}/W_2\).

**Ventaja.** El diseñador no necesita verificar el criterio de Middlebrook a posteriori: si el optimizador H∞ converge con \(\gamma<1\), la estabilidad está garantizada por construcción. Esto es especialmente valioso para redes con topología variable (N-1, mantenimientos) donde el criterio de Middlebrook puntual no es suficiente.

## 16 — Diseño iterativo: H∞ para el lazo de corriente GFL en SCR incierto

**Datos.** GFL, \(L_1=2\,\text{mH}\), \(R_1=0.1\,\Omega\). Red: \(L_g\in[0.5, 8]\,\text{mH}\) (SCR de 2 a 30). Objetivo: PM>35° en todo el rango.

**Paso 1 — calcular la incertidumbre.** La planta nominal con \(L_g=L_{g,nom}=2\,\text{mH}\): \(G_0(s)=1/(s(L_1+L_{g,nom})+R_1)=1/(0.004s+0.1)\). La incertidumbre multiplicativa a 1 kHz para \(L_g=8\,\text{mH}\): \(|\Delta_m(j\omega)|=|G(j\omega,8\text{mH})/G_0-1|\).

**Paso 2 — ajustar pesos.** \(\omega_b=2\pi\times100\), \(M_s=2\), \(\varepsilon=0.01\); \(\omega_t=2\pi\times3000\), \(M_t=1.25\). Incrementar \(M_t\) a 1.5 para permitir más robustez a expensas de un pico de T ligeramente mayor.

**Paso 3 — resolver y verificar.** Si \(\gamma_{opt}<0.9\): PM>35° garantizado. Verificar trazando el Bode del lazo \(K\cdot G\) para \(L_g\in[0.5, 8]\,\text{mH}\) y midiendo el PM en cada caso.

**Resultado típico.** El PI clásico tiene PM=12° para \(L_g=8\,\text{mH}\); el H∞ diseñado con esta incertidumbre tiene PM=38° — dentro de la especificación en todo el rango.

## 17 — El problema de la no unicidad: múltiples soluciones H∞

Para el mismo nivel de \(\gamma\), hay infinitos controladores estabilizantes. El H∞ encuentra el controlador de **orden mínimo** que garantiza \(\gamma\) mediante las ecuaciones de Riccati, pero no es el único. La parametrización de Youla-Kucera describe todos los controladores estabilizantes:

$$K = K_0 + Q(I + G K_0)^{-1}G, \quad Q\in H_\infty\text{ estable}$$

donde \(K_0\) es el controlador nominal y \(Q\) es el parámetro libre de Youla. El H∞ elige \(Q\) para minimizar \(\gamma\). Otras elecciones de \(Q\) producen controladores con distintas propiedades (p.ej. menor norma \(\|KS\|_\infty\) = menor esfuerzo de control, o mayor robustez ante incertidumbre no modelada).

**Implicación práctica.** Si el controlador H∞ estándar tiene un orden excesivamente alto, se puede explorar el espacio de Youla para encontrar un controlador equivalente (mismo \(\gamma\)) pero de menor orden, lo que facilita la implementación en DSP con recursos limitados.

## Cuándo y por qué se usa
Cuando la planta varía mucho (red de fortaleza desconocida, parámetros inciertos) y se necesitan
**garantías** en vez de comprobaciones puntuales. Conecta con el análisis de impedancia: se puede
exigir pasividad/robustez en bandas mediante los pesos.

## Procedimiento (genérico)
1. Modela la incertidumbre (multiplicativa, paramétrica) como \( \Delta \) acotado.
2. Elige pesos \( W_S, W_T, W_u \) que codifiquen las especificaciones.
3. Resuelve el problema \(H_\infty\) (solver dedicado) → controlador.
4. Verifica robustez (valor singular estructurado \( \mu \)) y reduce el orden del controlador si hace falta.

## Errores comunes
- Pesos mal elegidos → controlador conservador o de orden altísimo.
- Olvidar reducir el orden: \(H_\infty\) da controladores del orden de la planta + pesos.

## Uso en proyectos
- Candidato a proyecto propio (p.ej. control robusto de un GFL/GFM ante SCR incierto). Ficha de
  panorama por ahora.

## 18 — Resumen: diferencias entre H∞, H2 y μ-síntesis

| Aspecto | H∞ | H2 (LQG) | μ-síntesis |
|---|---|---|---|
| Criterio | \(\|H\|_\infty=\sup|H(j\omega)|\) | \(\|H\|_2=\sqrt{\int|H|^2d\omega}\) | \(\mu_\Delta(M(j\omega))\) |
| Perturbaciones | Energía acotada (\(L_2\)) | Estocásticas (ruido blanco) | Energía acotada + estructura |
| Incertidumbre | No estructurada | Estocástica | Estructurada (por bloques) |
| Conservatismo | Moderado | Bajo (óptimo para ruido blanco) | Menor que H∞ |
| Solución | Ecuaciones de Riccati / LMI | Riccati (Kalman + LQR) | D-K iteration |
| Aplicación | Variación paramétrica fuerte | Ruido de medición, carga aleatoria | Incertidumbre con estructura conocida |
| Reducción de orden | Truncamiento balanceado | Igual | Igual |

## 19 — Fórmulas de referencia para H∞ en convertidores

**Peso de tracking (sensibilidad S):**

$$W_1(s) = \frac{s/M_s + \omega_b}{s + \omega_b\varepsilon}, \quad M_s=2,\;\omega_b=2\pi\cdot f_{BW},\;\varepsilon=0.01$$

**Peso de robustez (complementaria T):**

$$W_2(s) = \frac{s + \omega_t/\sqrt{M_t}}{\sqrt{M_t}\,s + \omega_t}, \quad M_t=1.25,\;\omega_t=2\pi\cdot3f_{BW}$$

**Incertidumbre multiplicativa de \(L_g\) variable en \([L_{min}, L_{max}]\):**

$$\ell_m(\omega) = \max_{L\in[L_{min},L_{max}]}\left|\frac{G(j\omega,L)-G(j\omega,L_{nom})}{G(j\omega,L_{nom})}\right|$$

**Condición de estabilidad robusta:** \(\|W_2 T\|_\infty < 1 \Leftrightarrow |T(j\omega)| < 1/|W_2(j\omega)| \leq 1/\ell_m(\omega)\).

## 20 — Verificación de robustez con barrido de parámetros

Una vez obtenido el controlador H∞, la verificación robusta consiste en un barrido Monte Carlo o en grid sobre el espacio de incertidumbre:

```python
import numpy as np

def margin_pi(Kp, Ki, L, R, Td=1.5e-4):
    """PM del PI de corriente con retardo Td y planta L, R."""
    w = np.logspace(1, 5, 5000)
    s = 1j*w
    G = 1/(s*L + R)
    C = Kp + Ki/s
    Ld = C*G*np.exp(-s*Td)
    idx = np.argmin(np.abs(np.abs(Ld)-1))
    return 180 + np.degrees(np.angle(Ld[idx]))

def margin_hinf(K_hinf_num, K_hinf_den, L, R, Td=1.5e-4):
    """PM del controlador H-inf (representado como PI+lead de orden reducido)."""
    w = np.logspace(1, 5, 5000)
    s = 1j*w
    G = 1/(s*L + R)
    # Controlador H-inf reducido como PI+lead (aproximación)
    Kp, Ki, a, b = K_hinf_num  # parámetros del controlador reducido
    C = (Kp + Ki/s) * (s+a)/(s+b)
    Ld = C*G*np.exp(-s*Td)
    idx = np.argmin(np.abs(np.abs(Ld)-1))
    return 180 + np.degrees(np.angle(Ld[idx]))

# Barrido de L_g en [0.5mH, 8mH] — variación de SCR
L1 = 2e-3; R1 = 0.1
Lg_arr = np.linspace(0.5e-3, 8e-3, 20)
Kp_nom, Ki_nom = L1*2*np.pi*1000, R1*2*np.pi*1000

print("L_g(mH)  PM_PI(°)  PM>=30?")
for Lg in Lg_arr:
    L_total = L1 + Lg
    pm = margin_pi(Kp_nom, Ki_nom, L_total, R1)
    flag = "OK" if pm >= 30 else "FAIL"
    print(f"{Lg*1e3:7.1f}  {pm:8.1f}  {flag}")
```

## Conceptos relacionados
- [[metodos-sintesis-control]] · [[funciones-sensibilidad]] · [[robustez-parametrica]] · [[margenes-estabilidad]]

## Referencias
- Skogestad, Postlethwaite, *Multivariable Feedback Control*, cap. 8-9.
