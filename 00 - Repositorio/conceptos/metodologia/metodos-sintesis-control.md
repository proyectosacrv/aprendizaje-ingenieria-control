---
titulo: Métodos de síntesis de control (panorama)
slug: metodos-sintesis-control
categoria: metodologia
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [elegir el metodo de diseno adecuado al problema]
tags: [sintesis, clasico, estado, robusto, predictivo, panorama]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [ciclo-diseno-control, sintonia-pi-pid, loop-shaping, asignacion-polos-lqr, control-predictivo, control-robusto-hinf]
referencias:
  - "Skogestad, Postlethwaite, Multivariable Feedback Control, Wiley 2005"
---

## Definición
Catálogo de familias de métodos para obtener el controlador a partir del modelo y las
especificaciones, con sus compromisos. Sirve para **elegir** el método antes de detallarlo.

## Fundamento teórico (familias)
- **Clásico SISO** — lugar de raíces y [[loop-shaping]] en Bode; sintonía [[sintonia-pi-pid]]
  (cancelación de polo, módulo/simetría óptima). Intuitivo, lazo a lazo. Base de los convertidores.
- **Espacio de estados** — [[asignacion-polos-lqr]]: asignación de polos (colocar autovalores) y
  **LQR/LQG** (óptimo cuadrático + observador). Natural para sistemas MIMO y de muchos estados.
- **Robusto / óptimo** — [[control-robusto-hinf]] (\(H_\infty\), \(\mu\)-síntesis): diseña para el
  peor caso de incertidumbre, con garantías de robustez.
- **Predictivo** — [[control-predictivo]] (MPC, FCS-MPC): optimiza sobre un horizonte con
  restricciones explícitas; muy usado en convertidores y máquinas.
- **Específicos de convertidores** — separación de escalas, impedancia virtual, amortiguamiento
  activo: dan forma a la dinámica aprovechando la estructura física.

<div class="cfig"><img src="figuras/metodos-sintesis-control-escalera.png" alt="escalera de familias de metodos de sintesis de control"><div class="cap">Las familias de síntesis forman una escalera de complejidad: se empieza por el control clásico SISO (Bode, lugar de raíces, PI/PID) y se sube a espacio de estados (LQR/LQG), robusto ($H_\infty$/μ) o predictivo (MPC) a medida que el problema exige manejar acoplamiento MIMO, restricciones duras o incertidumbre con garantías.</div></div>

## 1 — Ejemplo cuantitativo: comparación de métodos sobre el mismo lazo de corriente
**Planta:** inductor \( L=2\,\text{mH} \), \( R=0.1\,\Omega \). Objetivo: \( f_c=1\,\text{kHz} \), \( \zeta\ge0.7 \).

**Método clásico (cancelación de polo):** directo y exacto para esta planta de primer orden.
\( K_p=L\omega_c=0.002\times6283=12.6 \), \( K_i=R\omega_c=0.1\times6283=628 \). Lazo cerrado: primer orden exacto en \( \omega_c \), \( \zeta=\infty \) (sin sobreimpulso). Tiempo de diseño: segundos.

**Espacio de estados (LQR):** para la misma planta \( \dot{x}=-Rx/L+u/L \) se elige \( Q=q \), \( R_u=1 \). La ganancia óptima es \( K_{LQR}=\sqrt{q/L} \) (solución de Riccati escalar). Para \( K_{LQR}=12.6 \) se necesita \( q=L\cdot K^2=0.002\times12.6^2=0.318 \). Resultado idéntico, pero requiere formular el espacio de estados. Ventaja aparece en MIMO (acoplamiento d-q).

**Robusto \( H_\infty \):** con pesos \( W_S=\omega_b/s \) (\( \omega_b=2\pi\times100 \)) y \( W_T=s/\omega_t \) (\( \omega_t=2\pi\times2000 \)) el solver da un controlador de 2º orden equivalente al PI + lead en la franja de interés, con garantía explícita de \( \|S\|_\infty<M_s \). Tiempo de diseño: minutos pero mayor orden del controlador.

**Conclusión:** para un lazo SISO sencillo, clásico y LQR convergen. El \( H_\infty \) añade garantías pero no mejora el resultado en este caso. La escalera de métodos tiene sentido cuando el problema añade restricciones, incertidumbre o acoplamiento MIMO.

## Cuándo elegir cada uno (guía rápida)
| Situación | Método recomendado |
|---|---|
| SISO, intuición física, convertidor estándar | clásico (Bode/lugar de raíces) + cascada |
| MIMO acoplado, muchos estados | espacio de estados (LQR) |
| Incertidumbre fuerte, garantías | \(H_\infty\) / robusto |
| Restricciones de corriente/tensión explícitas | MPC / FCS-MPC |
| Resonancias de filtro, redes débiles | impedance shaping + damping |

## Procedimiento (genérico)
1. Clasifica el problema (SISO/MIMO, lineal, restricciones, incertidumbre).
2. Elige la familia según la tabla y la experiencia del equipo.
3. Diseña, evalúa (márgenes, sensibilidad) y valida.
4. Si no cumple robustez/restricciones, sube de familia (clásico → estado → robusto/predictivo).

## 2 — Lugar de raíces: construcción y diseño de PD/PI/PID

El lugar de raíces (root locus) muestra cómo se mueven los polos de lazo cerrado cuando varía la ganancia \(K\):

$$1 + K\,G(s) = 0 \implies \text{lugar de los } s \text{ que satisfacen } G(s) = -1/K$$

**Reglas de construcción (Evans):**
1. El lugar parte de los polos de \(G(s)\) (para \(K=0\)) y termina en los ceros (para \(K\to\infty\)).
2. Ramas en el eje real: el tramo real pertenece al lugar si hay un número impar de polos/ceros a su derecha.
3. Asíntotas: \(n_p - n_z\) ramas van a infinito con ángulos \((2k+1)\pi/(n_p-n_z)\), partiendo del centroide \(\sigma_a = (\sum p_i - \sum z_i)/(n_p - n_z)\).
4. Ángulo de salida de un polo complejo: \(\angle G(j\omega) - 180°\) desde los demás polos menos los ceros.

**Diseño de compensadores:**
- **PD:** añade un cero en \(s=-z_c\); el lugar se dobla hacia la izquierda → mayor amortiguamiento.
- **PI:** añade un polo en el origen y un cero en \(s=-z_c\); el lugar se tuerce hacia la derecha a baja frecuencia → error nulo en régimen permanente.
- **PID:** combina ambos; los dos ceros permiten ubicar dos polos dominantes en la posición deseada.

**Ventaja:** visualización directa del compromiso entre velocidad (parte real) y oscilación (parte imaginaria).

<div class="cfig"><img src="../figuras/metodos-sintesis-control-analisis.png" alt="Síntesis de control: lugar de raíces, loop shaping, pesos H-inf y tabla comparativa"><div class="cap">(a) Lugar de raíces de un sistema de segundo orden con ganancia variable K. (b) Loop shaping: Bode de L con PM y GM marcados. (c) Pesos W1/W2 para diseño H-inf: plantillas de S y T. (d) Tabla comparativa de métodos de síntesis.</div></div>

## 3 — Loop shaping en Bode: diseño por forma del lazo

El loop shaping diseña \(C(s)\) de forma que el lazo abierto \(L(s) = C(s)G(s)\) tenga la forma deseada:

- **Baja frecuencia:** \(|L| \gg 1\) (alta ganancia → buen seguimiento y rechazo de perturbaciones)
- **Cruce de 0 dB:** pendiente de –20 dB/dec (garantiza margen de fase)
- **Alta frecuencia:** \(|L| \ll 1\) (atenuación de ruido y robustez ante incertidumbre)

**Criterios cuantitativos:**
$$\text{PM} = 180° + \angle L(j\omega_c) > 45°, \qquad \text{GM} = \frac{1}{|L(j\omega_{pc})|} > 6\,\text{dB}$$

**Procedimiento:**
1. Calcular \(G(j\omega)\) (Bode de la planta).
2. Identificar el ancho de banda objetivo \(\omega_c\).
3. Diseñar \(C(s)\) para que \(|L|\) cruce 0 dB en \(\omega_c\) con la pendiente y fase correctas.
4. Añadir notches o lag compensators para armónicos o perturbaciones específicas.

Para un integrador puro \(G = 1/(sL)\): un controlador PI da lazo de -20 dB/dec con cruce en \(\omega_c = K_p/L\). Para PI + notch del filtro LCL: el notch baja la ganancia en \(f_{res}\) sin afectar \(\omega_c\).

## 4 — Síntesis \(H_\infty\): pesos, problema estándar y solución

El problema estándar de \(H_\infty\) minimiza:

$$\min_K \|F_l(P_{aug}, K)\|_\infty = \min_K \left\|\begin{pmatrix}W_1 S \\ W_2 T\end{pmatrix}\right\|_\infty$$

donde \(P_{aug}\) es la planta aumentada que incluye los pesos \(W_1(s)\) y \(W_2(s)\).

**Diseño de pesos:**
- \(W_1(s) = \frac{s/M_s + \omega_b}{s + \omega_b A}\): pico limitado a \(M_s\), ganancia DC \(1/A\), ancho de banda \(\omega_b\).
- \(W_2(s) = \frac{s + \omega_t/\sqrt{M_t}}{s\sqrt{M_t} + \omega_t}\): limita \(\|T\|_\infty < M_t\) y pasa la banda \(\omega > \omega_t\).

**Solución:** las ecuaciones de Riccati de dos Riccati acopladas (Doyle-Glover-Khargonekar-Francis 1989), o equivalentemente LMI. El controlador óptimo tiene orden igual al de \(P_{aug}\) (planta + pesos).

**Reducción de orden:** el controlador de orden alto se reduce mediante truncamiento balanceado o aproximación por Hankel. Regla: retener los \(k\) estados con valores de Hankel > 1% del máximo.

## 5 — IMC y SIMC: sintonía directa desde el modelo

**IMC (Internal Model Control):** el controlador ideal sería la inversa del modelo, pero eso no es estable ni propio. Se introduce un filtro paso bajo de orden \(r\):

$$C_{IMC}(s) = \tilde{G}^{-1}(s)\cdot f(s), \quad f(s) = \frac{1}{(\lambda s + 1)^r}$$

donde \(\lambda\) es el único parámetro de sintonía: \(\lambda\) grande → más robusto pero más lento.

**SIMC (Skogestad IMC):** versión simplificada para obtener PI/PID directamente. Para una planta de primer orden con retardo \(G(s) = K e^{-\theta s}/(\tau s+1)\):

$$K_p = \frac{\tau}{K(\lambda+\theta)}, \qquad \tau_I = \min(\tau,\, 4(\lambda+\theta))$$

Para segundo orden con dos polos reales \(\tau_1 > \tau_2\): \(K_p = \tau_1/[K(\lambda+\theta)]\), \(\tau_I = \tau_1\), \(\tau_D = \tau_2\).

**Elección de \(\lambda\):** \(\lambda \geq \theta\) para robustez mínima; \(\lambda = \tau/2\) para equilibrio velocidad/robustez. A diferencia de ZN, SIMC permite ajuste directo.

## 6 — Tabla comparativa y guía de elección

| Método | Tipo | Aplicación típica | Complejidad | Robustez garantizada |
|---|---|---|---|---|
| Lugar de raíces | Analítico SISO | Ajuste de ganancias, PD/PI | Baja | No explícita |
| Loop shaping / Bode | Analítico SISO | PI/PID, lazo de corriente | Baja | PM/GM empíricos |
| SIMC / ZN | Empírico | PI/PID desde modelo 1er/2° orden | Muy baja | No |
| LQR / LQG | Espacio estados | MIMO, muchos estados | Media | No directa |
| \(H_\infty\) | Óptimo robusto | Incertidumbre fuerte, MIMO | Alta | Sí, \(\|S\|_\infty\) |
| MPC | Predictivo | Restricciones duras, tiempo real | Muy alta | No (sin garantías estándar) |

**Guía de selección:**
- SISO lineal sin incertidumbre fuerte → loop shaping / SIMC
- SISO con perturbaciones armónicas → loop shaping + resonante / notch
- MIMO acoplado → LQR o desacoplamiento + lazos independientes
- Incertidumbre paramétrica fuerte → \(H_\infty\) / \(\mu\)-síntesis
- Restricciones físicas explícitas → MPC / FCS-MPC
- No lineal con gran rango de operación → gain scheduling + loop shaping por punto

## 7 — Síntesis por espacio de estados: LQR y observador de Luenberger

El LQR (Linear Quadratic Regulator) encuentra la ganancia de realimentación de estado \(K\) que minimiza el funcional cuadrático:

$$J = \int_0^\infty (x^T Q x + u^T R u)\,dt$$

La solución es \(K = R^{-1}B^T P\) donde \(P\) es la solución de la ecuación de Riccati algebraica \(A^T P + P A - P B R^{-1} B^T P + Q = 0\). Los autovalores del sistema en lazo cerrado quedan en el semiplano izquierdo por construcción.

**Elección de Q y R.** \(Q=C^T C\) penaliza la salida; \(R\) penaliza el esfuerzo de control. La regla de Bryson: normalizar \(Q_{ii}=1/x_{i,max}^2\), \(R_{jj}=1/u_{j,max}^2\) para que los estados/entradas críticos sean los que dominan el criterio.

**Observador de Luenberger.** Si el estado no es completamente medible, se estima con un observador:

$$\dot{\hat{x}} = A\hat{x} + Bu + L(y - C\hat{x})$$

La ganancia \(L\) coloca los polos del observador unas 3–5 veces más a la izquierda que los del controlador. En presencia de ruido de medición se usa el filtro de Kalman (LQG = LQR + Kalman).

**Ventaja sobre el PI clásico para el dq.** El LQR diseñado para el sistema dq completo (matriz \(A\) con acoplamiento \(\pm\omega L\)) incluye automáticamente el desacoplamiento sin necesidad de feedforward explícito.

## 8 — Sintonía por cancelación de polo (cancelación directa)

El método de cancelación de polo es el más usado para el lazo de corriente de un convertidor. Para una planta de primer orden \(G(s) = 1/(sL+R)\):

$$C(s) = K_p\frac{s+K_i/K_p}{s} = K_p\frac{s+R/L}{s}$$

Eligiendo \(K_i/K_p = R/L\), el cero del controlador cancela el polo de la planta y el lazo abierto queda como un integrador con ganancia \(K_p/L\). El ancho de banda es \(\omega_c = K_p/L\).

**Criterio de elección del ancho de banda.** El retardo digital de un convertidor con periodo de muestreo \(T_s\) limita el ancho de banda a:

$$\omega_c < \frac{1}{3\,T_d}, \quad T_d \approx 1.5\,T_s$$

Para \(T_s=100\,\mu\text{s}\): \(\omega_c < 1/(3\times150\times10^{-6}) = 2222\,\text{rad/s} \approx 354\,\text{Hz}\). En la práctica se usa \(\omega_c = f_s/10\) como regla conservadora.

**Validez.** La cancelación es válida si el polo del proceso \(R/L\) está holgadamente por debajo de \(\omega_c\) (lo que sería siempre para inductancias de filtro). No se debe cancelar polos de proceso en el semiplano derecho (inestables) porque crea modos internos ocultos.

## 9 — Sintonía de lazo de tensión: integrador más amortiguamiento

El lazo externo de tensión sobre el condensador \(C_f\) ve la dinámica del lazo de corriente cerrado como un primer orden aproximado (si la separación de escalas se cumple). La planta efectiva vista por el lazo de tensión es:

$$G_v(s) \approx \frac{1}{C_f\,s}\cdot\frac{1}{1+s/\omega_{ci}}$$

Con un PI de tensión \(C_v(s) = K_{pv}(1+\omega_{iv}/s)\):

$$\omega_{cv} = K_{pv}/C_f, \quad \omega_{iv} = \omega_{cv}/5\quad\text{(para amortiguamiento }\zeta\approx0.7\text{)}$$

**Regla.** El cero del PI de tensión \(\omega_{iv}=\omega_{cv}/5\) asegura que la fase del lazo de tensión sea \(-90°+\arctan(\omega_{cv}/\omega_{iv})\approx-90°+78°=-12°\) en \(\omega_{cv}\), dejando margen de fase adecuado incluyendo el polo del lazo de corriente.

## 10 — Resonadores y controladores PR: seguimiento de señales periódicas

Para seguimiento de referencias periódicas (armónicos de la corriente) o rechazo de perturbaciones armónicas, el controlador proporcional-resonante (PR) añade un integrador sintonizado a la frecuencia objetivo:

$$C_{PR}(s) = K_p + \frac{2K_r\omega_c s}{s^2 + 2\omega_c s + \omega_0^2}$$

donde \(\omega_0\) es la frecuencia del armónico a controlar y \(\omega_c\) es el ancho de banda del resonador. Con \(\omega_c\to0\) la ganancia en \(\omega_0\) tiende a infinito (seguimiento/rechazo perfecto), pero el ancho de banda se reduce y la robustez ante variaciones de frecuencia empeora.

**Diseño.** Para seguimiento del armónico de 5ª de la corriente inyectada a 250 Hz: \(\omega_0=2\pi\times250\), \(\omega_c=2\pi\times5\) (±5 Hz de ancho de banda), \(K_r\approx K_p/3\) para no degradar el margen de fase del lazo principal. Se puede implementar en paralelo con el PI principal para controlar simultáneamente la componente fundamental y los armónicos.

## 11 — Control de corriente predictivo (FCS-MPC) en convertidores

El FCS-MPC (Finite Control Set MPC) evalúa todos los posibles vectores de tensión del convertidor (7 vectores para un inversor de 3 niveles: 6 activos + 1 cero) y aplica el que minimiza un criterio de coste:

$$J = \lambda_i(i_d^{ref}-i_d^{pred})^2 + \lambda_q(i_q^{ref}-i_q^{pred})^2 + \lambda_{sw}\,N_{switch}$$

donde \(i^{pred}\) es la corriente predicha al siguiente paso usando el modelo de la planta. No necesita PWM (el convertidor conmuta directamente al vector óptimo), lo que reduce la latencia a un periodo de muestreo.

**Ventajas:** seguimiento rápido de referencia (ideal para control de par en tracción), manejo implícito de la saturación de corriente, posibilidad de incluir múltiples restricciones en el criterio de coste. **Desventajas:** frecuencia de conmutación variable (dificulta el diseño del filtro), sensibilidad al modelo de la planta, coste computacional que crece con el número de vectores (NPC 3 niveles: 27 vectores).

## 12 — Diseño de notch filter para armónico específico en el lazo

Cuando una perturbación de frecuencia conocida \(\omega_h=2\pi f_h\) no puede rechazarse con el lazo PI (porque \(\omega_h\gg\omega_c\)), se añade un controlador resonante (PR) o un notch en la planta:

**Controlador PR paralelo al PI.** El resonador \(G_{res}(s)=2K_r\omega_c s/(s^2+2\omega_c s+\omega_h^2)\) tiene ganancia infinita en \(\omega_h\) (para \(\omega_c\to0\)). En paralelo con el PI, el lazo combinado tiene seguimiento perfecto a \(\omega_h\) sin afectar el margen de fase en \(\omega_c\).

**Notch en la planta (feedforward de rechazo).** Si el armónico \(\omega_h\) es una perturbación de red medible (p.ej. tensión de 5ª armónica conocida), se puede cancelar con un feedforward \(u_{ff}(t)=-\hat{V}_h\sin(\omega_h t+\hat{\phi}_h)\) estimado con un FLL (Frequency Locked Loop) o PLL armónico.

**Selección.** Para armónicos de red que entran como perturbaciones: feedforward (si se pueden medir y estimar). Para armónicos de referencia que hay que seguir (p.ej. corriente no sinusoidal): PR. El PI solo es suficiente cuando los armónicos están holgadamente por debajo del ancho de banda del lazo.

## 13 — Síntesis por asignación de polos con espacio de estados: el método de Ackermann

Para una planta en espacio de estados \(\dot{x}=Ax+Bu\), \(y=Cx\), la asignación de polos mediante realimentación de estado \(u=-Kx\) coloca los autovalores de \(A-BK\) en posiciones deseadas \(\{s_1,\ldots,s_n\}\).

**Fórmula de Ackermann (SISO).** La ganancia de realimentación de estado es:

$$K = e_n^T W_c^{-1} \Phi_d(A)$$

donde \(e_n^T=[0,\ldots,0,1]\), \(W_c\) es la matriz de controlabilidad y \(\Phi_d(s)=\prod_i(s-s_i)\) es el polinomio característico deseado. El sistema es controlable si y solo si \(\text{rank}(W_c)=n\).

**Aplicación al lazo de corriente dq.** La planta dq es un sistema de 2° orden con acoplamiento: \(A=\begin{pmatrix}-R/L & \omega \\ -\omega & -R/L\end{pmatrix}\), \(B=I/L\). Para polos en \(s_{1,2}=-\zeta\omega_c\pm j\omega_c\sqrt{1-\zeta^2}\), la asignación por Ackermann da una ganancia matricial \(K\in\mathbb{R}^{2\times2}\) que incluye automáticamente el desacoplamiento cruzado, siendo equivalente al PI con feedforward de desacoplamiento.

## 14 — Flujo de diseño: de las especificaciones al controlador

El flujo completo de diseño de un lazo de control para convertidores sigue estos pasos:

1. **Especificaciones.** \(f_c\) (ancho de banda), PM (margen de fase), \(\varepsilon_{ss}\) (error en régimen permanente), \(\|S\|_\infty\) (pico de sensibilidad).
2. **Modelo de planta.** Identificar la función de transferencia \(G(s)\): linealizar si no lineal, obtener los parámetros \(L,\,R,\,C\) del circuito.
3. **Elección del método.** Usar la tabla de la sección 6 para seleccionar la familia.
4. **Diseño del controlador.** Aplicar el método (cancelación de polo, loop shaping, LQR, etc.).
5. **Verificación.** Calcular PM, GM, \(\|S\|_\infty\), \(\|T\|_\infty\), respuesta al escalón.
6. **Robustez.** Comprobar que las especificaciones se mantienen con variaciones paramétricas (±20 % en L, ±50 % en SCR).
7. **Implementación digital.** Discretizar (\(T_s=f_s^{-1}\)) y verificar la pérdida de PM por retardo.

**Regla de retardo digital.** Un retardo total \(T_d=1.5T_s\) (PWM + cómputo) introduce una pérdida de fase de \(\Delta\phi=-\omega_c T_d\) en el cruce. Para \(f_c=1\,\text{kHz}\) y \(T_d=150\,\mu\text{s}\): \(\Delta\phi=-2\pi\times1000\times150\times10^{-6}\times\frac{180°}{\pi}\approx-54°\). El diseño analógico debe tener PM>45°+54°=99° para que el digital quede con PM>45°.

## 15 — Relación entre métodos: cómo convergen en el mismo resultado

Para un lazo de corriente de primer orden (\(G(s)=1/(sL+R)\)), todos los métodos de síntesis convergen a resultados equivalentes cuando se aplican correctamente:

| Método | Controlador resultante | Parámetros |
|---|---|---|
| Cancelación de polo | \(PI: K_p+K_i/s\) | \(K_p=L\omega_c\), \(K_i=R\omega_c\) |
| Loop shaping | \(PI: K_p+K_i/s\) | misma forma, cruce en \(\omega_c\) |
| SIMC | \(PI: K_p+K_i/s\) | \(K_p=\tau/[K(\lambda+\theta)]\) |
| LQR (SISO) | \(K_{LQR}\) | equivalente a PI con \(K_p=\sqrt{q/L}\) |
| H∞ (bajo orden) | Controlador de 2°-3° orden | ≈ PI + lead a alta frecuencia |

La diferencia aparece en sistemas de mayor orden (MIMO, con resonancias) o con incertidumbre explícita. Para un simple lazo RL, el PI por cancelación de polo es óptimo en el sentido de que es el controlador de menor orden que satisface las especificaciones sin residuo.

## 16 — Ganancia adaptativa (gain scheduling): extensión al rango de operación

Los métodos lineales diseñan el controlador en un punto de operación nominal. Cuando la planta varía significativamente (p.ej. la inductancia de red varía con el SCR según la configuración N-1), el gain scheduling adapta las ganancias del controlador según una variable de programación medible (\(\text{SCR}\), \(P\), \(T\)):

$$K_p(\text{SCR}) = K_{p,nom}\cdot f(\text{SCR}), \quad K_i(\text{SCR}) = K_{i,nom}\cdot g(\text{SCR})$$

donde \(f\) y \(g\) son funciones diseñadas para que el lazo tenga el mismo PM y ancho de banda en cada punto de operación. La condición de estabilidad del sistema con gain scheduling (bajo cambio lento de las ganancias):

$$\left|\frac{d K}{dt}\right| \ll \omega_c \cdot K$$

Esto garantiza que el sistema no ve una perturbación de ganancias demasiado rápida para que el lazo la rechace. En la práctica, el gain scheduling solo es estable si la variable de programación cambia lentamente comparada con la dinámica del lazo.

## 17 — Herramientas de validación del diseño: sensibilidad e indicadores

Tras diseñar el controlador, los indicadores de calidad que se calculan antes de la implementación:

1. **\(\|S\|_\infty\)** (pico de sensibilidad): debe ser <2 (6 dB). Equivale a PM>29°.
2. **\(\|T\|_\infty\)** (pico de complementaria): debe ser <1.5 (3.5 dB). Robustez ante incertidumbre multiplicativa.
3. **\(\|KS\|_\infty\)** (esfuerzo de control): debe ser finito y razonable. Evita saturación del actuador.
4. **Márgenes clásicos:** PM>45°, GM>6 dB.
5. **Respuesta al escalón:** tiempo de subida \(t_r\approx1/\omega_c\), sobreimpulso <20% (\(\zeta>0.4\)).

**Generación del informe de diseño.** En el repositorio, cada ficha de proyecto incluye un Bode del lazo abierto con los márgenes marcados, la respuesta al escalón y el diagrama de Nichols. Esto es la "evidencia de que funciona" exigida por el ciclo de diseño antes de la implementación en hardware.

## 22 — Criterio de validación: de la simulación al hardware

El ciclo completo de validación de un método de síntesis incluye:

1. **Simulación en tiempo continuo** (Python/MATLAB): verificar PM, GM, \(\|S\|_\infty\) con el modelo linealizado.
2. **Simulación discreta** (Simulink/Python con \(T_s\)): verificar que la discretización no degrada los márgenes más del 5°.
3. **Simulación conmutada** (PLECS/PSCAD): verificar que las no linealidades (PWM, saturación) no producen oscilaciones no previstas.
4. **HIL (Hardware-in-the-Loop)**: ejecutar el controlador real (DSP/FPGA) sobre el modelo simulado de la planta. Detectar problemas de latencia, overflow aritmético, resolución ADC.
5. **PHIL (Power-HIL)**: el convertidor real alimenta una carga o red emulada. Primer contacto con la planta física.
6. **Prueba de campo**: operación en las condiciones reales de la instalación.

En cada etapa, los indicadores clave son: PM medido (puede diferir del diseñado por model-plant mismatch), THD de la corriente inyectada, respuesta a perturbaciones (huecos, escalones de carga), y comportamiento en fallo (protecciones, FRT).

## Uso en proyectos
- **01/02**: método clásico (cascada + sintonía por ancho de banda) + técnicas de convertidor
  (impedancia virtual, damping activo, PLL). Los demás métodos se abordarán en proyectos propios.

## 18 — Síntesis basada en datos (data-driven): identificación + control

Cuando el modelo analítico es incierto o no disponible, los métodos basados en datos identifican la planta y luego sintetizan el controlador directamente:

**VRFT (Virtual Reference Feedback Tuning).** Dado un dataset de entrada-salida \(\{u_k, y_k\}\) del sistema en lazo abierto y una función de transferencia de referencia deseada \(M(z)\), calcula los parámetros del controlador \(\theta^*\) que minimizan:

$$\theta^* = \arg\min_\theta \|y - M(z) r_v\|^2$$

donde \(r_v=M^{-1}(z)\,y\) es la referencia virtual. No requiere identificación explícita del modelo, solo datos de lazo abierto. Aplicable a PI, PID, PD+filtro.

**FRIT (Fictitious Reference Iterative Tuning).** Variante de VRFT que itera para mejorar la estimación. Útil cuando el modelo de referencia \(M\) no se puede invertir directamente (sistemas de fase no mínima).

**Limitaciones.** Los métodos basados en datos no dan garantías de robustez sin información de incertidumbre; solo minimizan el error cuadrático en el punto de diseño. Para garantías formales, se combina con H∞ o μ-síntesis usando el modelo identificado + una banda de incertidumbre.

## 19 — El compromiso fundamental: velocidad vs robustez (waterbed effect)

La limitación más profunda de cualquier sistema de control realimentado es el **waterbed effect** (efecto del colchón de agua): no se puede reducir la sensibilidad en toda la banda de frecuencias simultáneamente. Si se reduce \(|S(j\omega)|\) en una banda, necesariamente crece en otra:

$$\int_0^\infty \ln|S(j\omega)|\,d\omega = \pi\sum_{k} \text{Re}(p_k)$$

donde la suma es sobre todos los polos inestables de la planta en lazo abierto. Para una planta estable (sin polos de lazo abierto en el SPD): \(\int_0^\infty \ln|S|\,d\omega=0\). Esto significa que si se reduce el pico de S a baja frecuencia (mejor seguimiento), S debe compensarlo con un pico mayor a alta frecuencia — exactamente el pico \(M_s=\|S\|_\infty\) que se quiere limitar.

**Implicación de diseño.** El ancho de banda \(\omega_c\) y el pico \(M_s\) están relacionados: aumentar \(\omega_c\) sin reducir \(M_s\) requiere reducir la sensibilidad a alta frecuencia, lo que degrada la robustez ante incertidumbre de alta frecuencia. El compromiso es inevitable: no existe un controlador que sea simultáneamente rápido, robusto y con mínimo error en régimen permanente en todas las frecuencias.

## 20 — Resumen de fórmulas clave por método

| Método | Fórmula clave | Parámetro de diseño |
|---|---|---|
| Cancelación de polo | \(K_p=L\omega_c\), \(K_i=R\omega_c\) | \(\omega_c\) (ancho de banda) |
| Loop shaping | \(\text{PM}=180°+\angle L(j\omega_c)>45°\) | Forma de \(L(s)\) |
| SIMC | \(K_p=\tau/[K(\lambda+\theta)]\), \(\tau_I=\tau\) | \(\lambda\) (filtro IMC) |
| LQR | \(K=R_u^{-1}B^TP_\infty\) | Matrices \(Q\), \(R_u\) |
| H∞ | \(\|W_S S\|_\infty<1\) y \(\|W_T T\|_\infty<1\) | Pesos \(W_S\), \(W_T\) |
| Lugar de raíces | Polos en \(s^*\): \(\angle G(s^*)=-180°\) | Posición de polos deseados |
| PR resonante | \(G_{res}=2K_r\omega_c s/(s^2+2\omega_c s+\omega_0^2)\) | \(\omega_0\) (frecuencia armónica) |
| Asignación de polos | \(K=e_n^T W_c^{-1}\Phi_d(A)\) | Polinomio deseado \(\Phi_d\) |

## 21 — Ejemplo integrado: síntesis del lazo de corriente con todas las familias

```python
import numpy as np

# Planta: inductor L1=2mH, R1=0.1 Ohm
L1 = 2e-3; R1 = 0.1; Ts = 1e-4

# Método 1: cancelación de polo (clásico)
wc = 2*np.pi*1000  # ancho de banda 1 kHz
Kp_cp = L1*wc; Ki_cp = R1*wc
print(f"Cancelación de polo: Kp={Kp_cp:.4f}, Ki={Ki_cp:.2f}")

# Método 2: SIMC (lambda = tau/2)
tau = L1/R1; K_gain = 1/R1; theta = 1.5*Ts  # retardo 1.5Ts
lam = tau/2
Kp_simc = tau/(K_gain*(lam+theta)); Ti_simc = min(tau, 4*(lam+theta))
print(f"SIMC: Kp={Kp_simc:.4f}, Ti={Ti_simc*1000:.2f}ms, Ki={Kp_simc/Ti_simc:.2f}")

# Método 3: loop shaping (criterio de cruce en wc con PM=60°)
# Para planta 1/(sL+R), PI con cero en R/L cancela el polo
# mismo resultado que cancelación de polo
Kp_ls = Kp_cp; Ki_ls = Ki_cp
print(f"Loop shaping: Kp={Kp_ls:.4f}, Ki={Ki_ls:.2f} (idéntico a cancelación de polo)")

# Verificación: PM de cada diseño incluyendo retardo
w_arr = np.logspace(1, 5, 5000)
s = 1j*w_arr
G = 1/(s*L1 + R1)
delay = np.exp(-s*1.5*Ts)  # retardo 1.5Ts
for label, Kp, Ki in [("Cancel.polo", Kp_cp, Ki_cp), ("SIMC", Kp_simc, Kp_simc/Ti_simc)]:
    C = Kp + Ki/s
    L_loop = C * G * delay
    idx = np.argmin(np.abs(np.abs(L_loop) - 1))
    PM = 180 + np.degrees(np.angle(L_loop[idx]))
    print(f"{label}: PM = {PM:.1f}°")
```

## Conceptos relacionados
- [[sintonia-pi-pid]] · [[loop-shaping]] · [[asignacion-polos-lqr]] · [[control-predictivo]] · [[control-robusto-hinf]]

## Referencias
- Skogestad, Postlethwaite, *Multivariable Feedback Control*, 2005.
