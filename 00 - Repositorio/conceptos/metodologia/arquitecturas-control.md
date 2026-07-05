---
titulo: Arquitecturas de control (cascada, feedforward, 2-DOF)
slug: arquitecturas-control
categoria: metodologia
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [elegir la estructura del lazo antes de sintonizar]
tags: [arquitectura, cascada, feedforward, 2-DOF, desacoplo]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [ciclo-diseno-control, control-cascada, metodos-sintesis-control]
referencias:
  - "Aström, Hägglund, Advanced PID Control, ISA 2006"
---

## Definición
Decisión, previa a la sintonía, de **cómo se estructura** el control: qué se mide, qué lazos hay
y cómo se combinan. La estructura suele importar más que el ajuste fino de ganancias.

## Fundamento teórico
Patrones principales:
- **Cascada**: lazos anidados (interno rápido, externo lento). Mejora el rechazo de
  perturbaciones internas y da protección. Requiere **separación de escalas**. Ver [[control-cascada]].
- **Feedforward / desacoplo**: cancela perturbaciones medibles o acoplamientos conocidos
  (p.ej. términos \( \pm\omega L \) del marco dq) antes de que afecten. No afecta a la
  estabilidad del lazo (es de lazo abierto) pero mejora el desempeño.
- **2-DOF** (dos grados de libertad): separa el seguimiento de referencia (prefiltro) del
  rechazo de perturbación (realimentación), permitiendo optimizarlos por separado.
- **Específicos de convertidores**: impedancia virtual, amortiguamiento activo, que dan forma a
  la dinámica sin un lazo clásico adicional.

<div class="cfig"><img src="figuras/arquitecturas-control-cascada.png" alt="diagrama de arquitectura en cascada con feedforward"><div class="cap">Arquitectura en cascada: el lazo interno rápido (corriente) se anida dentro del externo lento (tensión), lo que mejora el rechazo de perturbaciones internas y protege el equipo, exigiendo separación de escalas. El feedforward/desacoplo cancela perturbaciones y acoplamientos medibles ($v_{red}$, $\pm\omega L$) sin tocar la estabilidad del lazo, solo el desempeño.</div></div>

## 1 — Ejemplo cuantitativo: separación de escalas en la cascada tensión/corriente
**Situación.** Convertidor GFM con lazo de corriente en el inductor \( L_1=2\,\text{mH} \), \( R_1=0.1\,\Omega \), y lazo de tensión sobre el condensador \( C_f=50\,\mu\text{F} \). Se quiere lazo de corriente con ancho de banda \( f_{ci}=1\,\text{kHz} \), \( f_{sw}=10\,\text{kHz} \).

**Paso 1 — lazo de corriente.** Cancelación de polo: \( \omega_{ci}=2\pi\times1000 \) rad/s.

$$ K_p^i = L_1\,\omega_{ci} = 0.002\times6283 = 12.57\,\text{V/A},\qquad K_i^i = R_1\,\omega_{ci} = 0.1\times6283 = 628\,\text{A/s/A} $$

Lazo cerrado de corriente: primer orden con \( \tau_i = 1/\omega_{ci} = 0.16\,\text{ms} \).

**Paso 2 — lazo de tensión.** Para separación de escalas de factor 5: \( \omega_{cv}=\omega_{ci}/5=2\pi\times200 \) rad/s. La planta del lazo de tensión es el condensador: \( G_v(s)=1/(C_f s) \), pero vista a través del lazo de corriente cerrado, es aproximadamente \( 1/(C_f s) \) (el lazo interno ya es transparente a esa frecuencia). Integral puro → se sintoniza como \( K_p^v=C_f\,\omega_{cv}^2/\omega_{ci} \).

**Paso 3 — verificación de separación.** \( f_{ci}/f_{cv}=1000/200=5 \): los dos lazos están suficientemente separados para no interactuar. Si se redujera a factor 2–3, los márgenes del lazo externo degradarían al lazo interno y viceversa. La regla práctica "factor 5–10" es la condición de separación de escalas cuantitativa.

## Cuándo y por qué se usa
Elegir bien la arquitectura simplifica la sintonía y mejora robustez. La cascada es estándar en
convertidores con control de tensión; el feedforward/desacoplo es casi obligatorio en dq.

## Procedimiento (genérico)
1. Identifica qué variables puedes medir y cuáles quieres controlar.
2. Si hay dinámica rápida interna controlable, usa cascada (interno = la rápida).
3. Añade feedforward para perturbaciones/acoplamientos medibles.
4. Si seguimiento y rechazo tienen requisitos distintos, considera 2-DOF.
5. Verifica que cada feedforward realmente ayuda **en lazo cerrado** (no asumir).

## 2 — Separación de escalas: cuantificación del requisito

La condición de separación de escalas en una cascada de \(n\) lazos exige:

$$\omega_{c,i} \geq 5\cdot\omega_{c,i+1} \quad \forall\, i$$

Con esta condición, el lazo externo "ve" el lazo interno cerrado como una dinámica de primer orden pura en \(1/\omega_{c,i}\), sin interacción apreciable. Si la separación cae a factor 2–3:

- Los márgenes del lazo externo se degradan porque la fase aportada por el lazo interno cerrado es ya apreciable a \(\omega_{c,i+1}\).
- La respuesta transitoria muestra modos acoplados (latidos entre lazos).

**Regla práctica en convertidores:**
- Lazo de corriente: \(f_{ci} = f_s/10\) (límite de retardo digital)
- Lazo de tensión: \(f_{cv} = f_{ci}/5 = f_s/50\)
- Lazo de frecuencia (droop/VSM): \(f_{cf} = f_{cv}/5 = f_s/250\)

Para \(f_s=10\,\text{kHz}\): \(f_{ci}=1\,\text{kHz}\), \(f_{cv}=200\,\text{Hz}\), \(f_{cf}=40\,\text{Hz}\).

<div class="cfig"><img src="../figuras/arquitecturas-control-analisis.png" alt="Arquitecturas de control: cascada, feedforward, acoplamiento dq y comparativa"><div class="cap">(a) Diagrama de cascada con separación de escalas entre lazos de corriente y tensión. (b) Respuesta ante perturbación con y sin feedforward. (c) Acoplamiento dq sin y con desacoplamiento explícito. (d) Tabla comparativa de arquitecturas de control.</div></div>

## 3 — Control feedforward: cancelación de perturbaciones medibles

El feedforward ideal cancela la perturbación \(d\) antes de que afecte a la salida:

$$u_{ff} = -\frac{G_{dist}(s)}{G_{planta}(s)}\cdot d(s)$$

En el lazo dq del convertidor, los términos cruzados \(\pm\omega L\) actúan como perturbaciones acopladas. El feedforward de desacoplamiento:

$$u_{d,ff} = +\omega L\,i_q, \qquad u_{q,ff} = -\omega L\,i_d$$

cancela exactamente el acoplamiento, dejando dos lazos SISO independientes. Si el modelo de \(L\) tiene un error del 10%, el residuo sin cancelar es el 10% del acoplamiento — todavía una mejora significativa respecto a no desacoplar.

**Feedforward de tensión de red:** \(u_{ff} = v_{red}\) permite al lazo de corriente concentrar su ganancia en el error de corriente, sin tener que rechazar también la perturbación de tensión. Reduce el pico de corriente ante huecos de tensión.

**Limitación:** el feedforward no debe usarse si el modelo es muy impreciso; un feedforward erróneo puede amplificar en vez de cancelar. Siempre verificar en lazo cerrado.

## 4 — Control MIMO y descentralizado: acoplamiento dq

El sistema dq es inherentemente MIMO 2×2 por el acoplamiento cruzado. La planta aumentada en dq:

$$\begin{pmatrix}\dot{i}_d\\\dot{i}_q\end{pmatrix} = \begin{pmatrix}-R/L & \omega \\ -\omega & -R/L\end{pmatrix}\begin{pmatrix}i_d\\i_q\end{pmatrix} + \frac{1}{L}\begin{pmatrix}u_d\\u_q\end{pmatrix}$$

**MIMO centralizado:** diseñar un controlador 2×2 que trate el acoplamiento como parte de la planta. Requiere herramientas MIMO (\(H_\infty\), LQR), pero da la solución óptima.

**Descentralizado con desacoplamiento:** aplicar el feedforward de desacoplamiento + dos PI independientes. Funciona bien si \(\omega L \ll R + K_p\) (el acoplamiento residual es pequeño comparado con la ganancia del lazo). En convertidores de alta potencia con \(L\) grande, la condición no se cumple sin desacoplamiento explícito.

**Criterio de Gershgorin:** el sistema descentralizado es estable si los discos de Gershgorin de la planta desacoplada no contienen el punto crítico \(-1/K\). Con desacoplamiento aplicado, los discos se reducen y el criterio se satisface con mayor margen.

## 5 — Arquitecturas para convertidores VSC: resumen estándar

**GFL (Grid-Following):**
- Lazo interno: PI de corriente en dq con feedforward de tensión y desacoplamiento dq
- Lazo externo: PI de potencia activa/reactiva o P/Q desde referencia externa
- PLL: SRF-PLL para seguimiento del ángulo de red
- Restricción: no puede operar en isla; necesita red fuerte (SCR > 2–3)

**GFM (Grid-Forming) — control de tensión:**
- Lazo interno doble: PI de corriente (1 kHz) anidado en PI de tensión (200 Hz)
- Sincronización: droop P/f + Q/V, o VSM con inercia virtual, o PSC
- Amortiguamiento activo: realimentación de \(i_{Cf}\) para el filtro LCL
- Puede operar en isla y en red

**PSC (Power Synchronization Control):** referencia de ángulo generada por integración de \(P_{err}/D\); equivale a droop con constante de inercia \(J\). Más robusto en redes débiles que el PLL.

## 6 — Tendencias en arquitecturas de control avanzadas

**MPC centralizado para microrredes:** un MPC de horizonte \(N_p = 20\) pasos, \(T_s = 1\,\text{ms}\), optimiza simultáneamente los setpoints de potencia de todos los convertidores de la microrred. Maneja restricciones de corriente y tensión explícitas. Desafío: tiempo de cómputo — requiere QP rápida (OSQP, ECOS) en FPGA o DSP de alta gama.

**Control basado en datos (RL):** el agente Reinforcement Learning aprende una política \(\pi(\text{estado}) = \text{acción}\) directamente de interacciones con el simulador. Ventaja: no necesita modelo lineal; puede adaptarse a no linealidades. Desafío: garantías de estabilidad, interpretabilidad.

**Arquitecturas híbridas GFM+GFL:** algunos estándares (IEEE P2800) permiten que un convertidor opere como GFL en red fuerte y conmute a GFM en eventos de red. La transición requiere bumpless transfer (coincidencia de estados del integrador) y detección de islanding rápida.

## 7 — La arquitectura 2-DOF (dos grados de libertad)

El control clásico de un grado de libertad (1-DOF) usa la misma ganancia para seguir la referencia y para rechazar perturbaciones. Estos dos objetivos suelen estar en conflicto: una ganancia alta mejora el seguimiento pero amplifica el ruido; una ganancia baja atenúa el ruido pero degrada el seguimiento.

La arquitectura 2-DOF separa los dos objetivos mediante un **prefiltro** \(F(s)\) sobre la referencia:

$$u = C(s)(r\cdot F(s) - y)$$

El controlador \(C(s)\) se diseña para el rechazo de perturbaciones (margen de fase, estabilidad robusta). El prefiltro \(F(s)\) se diseña para el seguimiento de referencia sin afectar a la función sensibilidad complementaria.

**Diseño práctico.** Para un PI de corriente con polo en el origen y cero en \(-\omega_{ci}\), el prefiltro típico es:

$$F(s) = \frac{\omega_{ci}}{s + \omega_{ci}}$$

que elimina el sobreimpulso ante un escalón de referencia sin cambiar los márgenes del lazo. Resultado: respuesta al escalón sin sobreimpulso (propiedad del prefiltro) y buen rechazo de perturbaciones (propiedad del PI).

## 8 — Impedancia virtual: arquitectura de amortiguamiento sin resistencia física

La impedancia virtual es un feedforward que suma al bucle de control un término proporcional a la corriente de salida, emulando una impedancia física en el punto de conexión:

$$v_{ref} = v_{ctrl} - Z_{virt}(s)\cdot i_{out}$$

Para \(Z_{virt}(j\omega) = R_v + j\omega L_v\), el convertidor se comporta como si tuviera una impedancia adicional \(Z_{virt}\) en su salida. Esto es útil para:

1. **Amortiguamiento de resonancias del filtro LCL**: \(Z_{virt} = K_{ad}\) (resistivo) equivale a la resistencia virtual del amortiguamiento activo.
2. **Compartición de carga en paralelo**: en microrred con varios convertidores en paralelo, una \(L_v\) virtual crea una caída de tensión proporcional a la corriente que distribuye la carga entre convertidores.
3. **Modificar la impedancia de salida para cumplir Middlebrook**: si \(|Z_{out}| < |Z_{load}|\) no se cumple, añadir \(Z_{virt}\) inductivo aumenta \(|Z_{out}|\) hasta que el criterio se satisfaga.

**Límite.** El feedforward de impedancia virtual actúa en lazo abierto: si el modelo de la planta tiene error, la impedancia virtual no coincide exactamente con la deseada. Variaciones de \(L_1\) del ±20% producen un error similar en \(Z_{virt}\).

## 9 — Arquitecturas de control avanzadas: PSC y VSM en GFM

**Power Synchronization Control (PSC).** El PSC genera la referencia de ángulo integrando el error de potencia activa dividido por la constante de damping \(D_p\):

$$\dot{\theta}_{ref} = \omega_0 + \frac{P^* - P}{D_p}$$

Es matemáticamente equivalente al droop P-f con constante de droop \(m_p=1/D_p\). La diferencia operativa: el PSC no necesita medición directa de frecuencia de red (no tiene PLL), solo mide \(P\) instantánea. Esto lo hace más robusto en redes débiles donde el PLL puede perder el seguimiento.

**Virtual Synchronous Machine (VSM).** El VSM añade inercia virtual emulando la ecuación de oscilación de un generador síncrono:

$$J\ddot{\theta} = T^* - T - D(\dot{\theta} - \omega_0)$$

La inercia virtual \(J\) ralentiza la respuesta de frecuencia, lo que proporciona soporte de inercia a la red. El droop de frecuencia clásico (sin inercia) es el caso límite \(J=0\) del VSM. En la práctica, \(J\) equivalente se elige para un tiempo de respuesta de frecuencia de 0.5–2 s (similar a un generador físico de potencia comparable).

## 10 — Tendencias: MPC centralizado y control basado en datos (RL)

**MPC para microrredes.** El MPC centralizado opera con un modelo del sistema completo (varios convertidores, líneas, cargas) y optimiza simultáneamente los setpoints de potencia con horizonte de predicción \(N_p\):

$$\min_{u_{0:Np}} \sum_{k=0}^{N_p}\|y_k - y_k^{ref}\|_Q^2 + \|u_k\|_R^2 \quad \text{s.t. } u_{min} \leq u_k \leq u_{max}$$

La solución es un QP (problema cuadrático) que puede resolverse eficientemente con OSQP o ECOS en ~1 ms en hardware moderno. Restricciones de corriente y tensión se incluyen como desigualdades.

**Control por RL.** El agente de aprendizaje por refuerzo aprende la política \(\pi(s)=a\) que maximiza la recompensa acumulada \(R=\sum\gamma^t r_t\) interactuando con un simulador del sistema. Las redes de política (actor-critic) pueden representar comportamientos no lineales que un PI no puede capturar (p.ej. gestión adaptativa de la corriente de cortocircuito en GFM). Desafíos: garantías de estabilidad, tiempo de entrenamiento, transferencia sim-to-real.

## 11 — Diseño iterativo: arquitectura completa del GFM del proyecto 01

El proyecto 01 usa una arquitectura de 4 capas:

**Capa 1 — lazo de corriente (1 kHz):** PI con cancelación de polo sobre \(L_1\), feedforward de desacoplamiento dq (\(\pm\omega L_1 i_{d,q}\)), amortiguamiento activo (\(K_{ad}\,i_{Cf}\)).

**Capa 2 — lazo de tensión (200 Hz):** PI sobre \(C_f\), feedforward de corriente de carga (\(i_2\)), impedancia virtual resistiva para compartir carga.

**Capa 3 — sincronización (PSC, ~40 Hz):** integración de \(P_{err}/D_p\) para el ángulo de referencia; droop Q-V para la amplitud de referencia.

**Capa 4 — despacho energético (<<1 Hz):** setpoints de \(P^*,\,Q^*\) desde la capa primaria/secundaria de la microrred.

**Separación de escalas:** \(1000:200:40:1\) Hz — cada capa ve la siguiente como estática → tratables independientemente. La verificación de la estabilidad global se hace con el modelo linealizado de todas las capas acopladas.

## 12 — Arquitectura GFL: lazo de corriente con PLL

El GFL (Grid-Following) es la arquitectura dominante en parques solares y eólicos actuales. Su estructura:

**Lazo de corriente (1 kHz).** PI en dq con cancelación de polo (\(K_p=L\omega_c\), \(K_i=R\omega_c\)), feedforward de tensión de red (\(u_{ff}=v_{PCC}\)) y desacoplamiento cruzado (\(\pm\omega L\)).

**PLL (20–100 Hz).** Detecta el ángulo de la tensión de red para orientar el marco dq. El SRF-PLL cierra un lazo PI sobre \(v_q\) (que debe ser cero en el marco orientado a la tensión de red).

**Lazo de potencia (10–50 Hz).** Convierte las referencias de \(P^*\) y \(Q^*\) en referencias de corriente dq:

$$i_d^* = \frac{2P^*}{3v_d}, \quad i_q^* = -\frac{2Q^*}{3v_d}$$

**Limitación principal.** El GFL necesita que la red proporcione un ángulo de referencia para el PLL. En isla o en red muy débil (SCR<1.5), el PLL pierde el seguimiento y el GFL se inestabiliza. Esta limitación es el motor del cambio hacia GFM en sistemas con alta penetración de renovables.

## 13 — Estabilidad de la cascada con acoplamiento: análisis cuantitativo

En la arquitectura en cascada, la función de transferencia del lazo externo de tensión \(L_v(s)\) incluye la dinámica del lazo interno de corriente cerrado \(T_i(s)\):

$$L_v(s) = C_v(s)\cdot\frac{1}{sC_f}\cdot T_i(s)$$

Si \(\omega_{cv}\ll\omega_{ci}\), \(T_i(j\omega_{cv})\approx1\) y el lazo de tensión ve la planta "pura" \(1/(sC_f)\). La degradación real se cuantifica con la fase residual del lazo interno a \(\omega_{cv}\):

$$\Delta\phi_{residual} = \angle T_i(j\omega_{cv}) = -\arctan\left(\frac{\omega_{cv}/\omega_{ci}}{1-(\omega_{cv}/\omega_{ci})^2}\right)$$

Para separación de factor 5 (\(\omega_{cv}=\omega_{ci}/5\)): \(\Delta\phi=\arctan(0.2/(1-0.04))\approx\arctan(0.208)\approx11.7°\). El lazo de tensión "pierde" 12° de margen de fase por la interacción con el lazo de corriente. Con factor 10: pérdida de solo 5.7°.

**Implicación de diseño.** El PM objetivo del lazo de voltaje analógico debe ser PM\(_{objetivo}+\Delta\phi_{residual}\) para que el sistema real tenga el PM mínimo deseado.

## 14 — Arquitecturas de control para microrred en isla: reparto de carga

En una microrred con varios GFM en isla, el reparto de carga entre convertidores se controla mediante el droop:

$$\omega = \omega_0 - m_p(P - P^*), \quad V = V_0 - m_q(Q - Q^*)$$

La constante de droop \(m_p\) (rad/s/W) determina la participación de cada unidad en el reparto de potencia activa: una unidad con \(m_p\) mayor cede más frecuencia ante perturbaciones y por tanto asume menos carga. Para reparto proporcional a la potencia nominal \(S_n\):

$$m_p = \frac{\Delta\omega_{max}}{P_n} = \frac{2\pi\times0.5\,\text{Hz}}{P_n}$$

**Problema de desviación de frecuencia.** Con droop, cualquier desbalance de carga produce una desviación permanente de frecuencia (\(\Delta\omega=m_p\Delta P\)). La restauración de frecuencia a \(\omega_0\) requiere un lazo secundario más lento (\(f_{cf}\approx0.1\,\text{Hz}\)) que ajusta \(P^*\) en cada unidad.

**Reparto de Q.** El droop de tensión funciona bien en redes inductivas (\(X\gg R\)). En redes de distribución de baja \(X/R\), el Q queda mal distribuido y se necesita una transformación de droop que considera la impedancia real de la línea o el uso de impedancias virtuales.

## 15 — Bumpless transfer entre GFL y GFM

La transición de GFL a GFM (o viceversa) requiere bumpless transfer: los estados internos del controlador (integradores) deben coincidir para que no haya salto en la señal de control al cambiar de modo:

**Problema.** El lazo de corriente GFL tiene un integrador \(\xi_d\) que almacena el error acumulado de corriente. El lazo de tensión GFM tiene integradores \(\xi_v\) para el error de tensión. Si se cambia de GFL a GFM sin inicializar los integradores, la diferencia entre el estado almacenado y el requerido por GFM produce un transitorio de corriente que puede disparar la protección.

**Solución.** Antes de la transición:
1. El controlador GFM estima la referencia de tensión de condensador \(v_C^*\) necesaria para reproducir la corriente actual del GFL.
2. Pre-inicializa el integrador de tensión con ese valor.
3. Cambia el selector de modo cuando la diferencia de señales de control es <1 % del valor nominal.

**Detección de isla.** La condición de isla debe detectarse en <100 ms (requisito IEEE 1547-2018). Los métodos activos (inyección de perturbación en el PLL) detectan la isla antes de que el ROCOF pasivo alcance el umbral, permitiendo la transición suave a GFM.

## 16 — Implementación digital de los lazos: discretización y antiwindup

La implementación digital del PI usa la aproximación de Euler hacia delante o bilineal (Tustin):

**Euler hacia atrás (Backward Euler):**

$$\xi(k) = \xi(k-1) + T_s\cdot e(k), \quad u(k) = K_p\,e(k) + K_i\,\xi(k)$$

**Bilineal (Tustin):**

$$\xi(k) = \xi(k-1) + \frac{T_s}{2}[e(k) + e(k-1)], \quad u(k) = K_p\,e(k) + K_i\,\xi(k)$$

La bilineal preserva mejor las propiedades de frecuencia del continuo (error \(O(T_s^2)\) vs \(O(T_s)\) del Euler). Para \(f_{ci}=1\,\text{kHz}\) y \(T_s=100\,\mu\text{s}\): el error de ganancia de la bilineal es <1 % en la banda de interés.

**Antiwindup.** Cuando la salida del controlador satura en \(\pm u_{max}\), el integrador debe dejar de acumular error (windup). La estrategia back-calculation:

$$\xi(k) = \xi(k-1) + T_s\,e(k) - \frac{T_s}{T_{AW}}[u_{sat}(k-1) - u_{lin}(k-1)]$$

donde \(T_{AW}=L/(R+K_p)\approx1/\omega_c\) es la constante de tiempo de antiwindup. Esto descarga el integrador al ritmo de la planta, reduciendo el tiempo de recuperación de saturación.

## 17 — Tabla de elección de arquitectura según la aplicación

| Aplicación | Arquitectura estándar | Frecuencias típicas | Observaciones |
|---|---|---|---|
| Inversor FV residencial | GFL lazo corriente + PLL | \(f_{ci}=1\,\text{kHz}\), \(f_{PLL}=10\,\text{Hz}\) | Sin lazo de tensión |
| Inversor FV comercial | GFL + Q-V droop | \(f_{ci}=1\,\text{kHz}\), \(f_{QV}=5\,\text{Hz}\) | Volt-Var support |
| Aerogenerador DFIG | GFL + control de par | \(f_{ci}=1\,\text{kHz}\), \(f_P=30\,\text{Hz}\) | Lazo de velocidad exterior |
| Batería BESS | GFM cascada | \(f_{ci}=1\,\text{kHz}\), \(f_{cv}=200\,\text{Hz}\) | Soporte de inertia y black start |
| HVDC back-to-back | GFM en isla + GFL en red | \(f_{ci}=1\,\text{kHz}\) | Desacoplamiento de frecuencias |
| Microrred en isla | GFM con droop | \(f_{ci}=1\,\text{kHz}\), \(f_{droop}=40\,\text{Hz}\) | Reparto de carga entre GFMs |
| STATCOM | GFL sin lazo P | \(f_{ci}=500\,\text{Hz}\) | Solo control de Q y tensión |

## 22 — Anti-islanding y detección de pérdida de red en GFL

La normativa IEEE 1547-2018 exige que los inversores GFL detecten la pérdida de la red y desconecten en <100 ms (para potencias <30 kVA) o <160 ms (para potencias mayores).

**Métodos pasivos.** El ROCOF (Rate Of Change Of Frequency) mide \(df/dt\): si supera el umbral (típicamente 0.5–1 Hz/s), se detecta la isla. El problema: en sistemas de alta inercia, el ROCOF puede ser pequeño incluso en isla, produciendo fallo de detección (Non-Detection Zone, NDZ).

**Métodos activos.** El Sandia Frequency Shift (SFS) introduce una perturbación de frecuencia en el PLL proporcional al error de frecuencia. En red conectada, la perturbación es absorbida por la red. En isla, la perturbación se realimenta positivamente y la frecuencia diverge rápidamente hasta superar el umbral de protección. El SFS elimina prácticamente la NDZ con una perturbación de solo el 0.1–0.5 % de la frecuencia nominal.

**Integración con la arquitectura.** En la práctica, el anti-islanding se implementa en la capa del PLL (para GFL) o en la capa de sincronización PSC (para GFM cuando opera en modo GFL). La detección de isla dispara la desconexión del inversor y la congelación de los integradores, preparando el bumpless reconnect cuando la red vuelva.

## Errores comunes
- Feedforward que desestabiliza (en el GFM, el feedforward de carga lo hacía): siempre verificar.
- Cascada sin separación de escalas → los lazos interactúan.

## Uso en proyectos
- **01 (GFM)**: cascada tensión/corriente + desacoplo dq + impedancia virtual + damping activo.
- **02 (GFL)**: lazo de corriente + PLL; sin lazo de tensión externo.

## 18 — Control de limitación de corriente en GFM: de tensión a corriente

El GFM opera normalmente en modo de control de tensión. Durante una falta de red o sobrecarga, la corriente puede superar el límite del convertidor. La transición debe ser:

**Saturación con prioridad de \(i_d\) o \(i_q\).** Si \(i_{ref}^2 = i_d^{*2}+i_q^{*2} > I_{max}^2\), escalar ambos proporcionalmente:

$$i_{d,lim}^* = i_d^*\cdot\frac{I_{max}}{\sqrt{i_d^{*2}+i_q^{*2}}}, \quad i_{q,lim}^* = i_q^*\cdot\frac{I_{max}}{\sqrt{i_d^{*2}+i_q^{*2}}}$$

O dar prioridad a \(i_d\) (potencia activa) saturando solo \(i_q\), o viceversa. En sistemas con requisitos de fault ride-through (FRT), la prioridad suele ser \(i_q\) (potencia reactiva) para soportar la tensión de red durante la falta.

**Transición GFM→modo corriente.** Durante el clamp de corriente, el GFM se comporta como un GFL temporalmente: sigue el ángulo de red (o el ángulo interno previo) e inyecta la corriente limitada. La transición de vuelta a GFM cuando la corriente vuelve al rango nominal requiere bumpless transfer del integrador del lazo de tensión.

## 19 — Checklist de diseño de arquitectura de control

Antes de pasar a la sintonía fina, verificar:

- [ ] ¿La variable de control (tensión o corriente) está bien elegida para el modo de operación (GFL vs GFM)?
- [ ] ¿La separación de escalas entre lazos es al menos factor 5?
- [ ] ¿El feedforward de desacoplamiento dq usa el valor correcto de \(L\) (incluyendo \(L_g\) si es relevante)?
- [ ] ¿El amortiguamiento activo del filtro LCL está sintonizado con \(f_{res}<f_s/6\)?
- [ ] ¿El antiwindup está implementado en todos los integradores con saturación de salida?
- [ ] ¿El bumpless transfer está previsto para la transición GFL↔GFM?
- [ ] ¿La limitación de corriente preserva el modo de operación correcto durante la falta?
- [ ] ¿El feedforward de tensión de red está filtrado para no amplificar ruido a alta frecuencia?

## 20 — Resumen de arquitecturas y sus parámetros de diseño clave

| Arquitectura | Lazos / elementos clave | Parámetros de diseño |
|---|---|---|
| GFL lazo corriente | PI \(i_d\), PI \(i_q\) + SRF-PLL | \(f_{ci}=f_s/10\), \(f_{PLL}<f_{ci}/5\) |
| GFM cascada | PI \(i\) + PI \(v\) + PSC/VSM | \(f_{ci}:f_{cv}:f_{sync}=1000:200:40\) Hz |
| Feedforward dq | \(u_{d,ff}=\omega L i_q\), \(u_{q,ff}=-\omega L i_d\) | \(L\) exacto para cancelación |
| Impedancia virtual | \(v_{ref}=v_{ctrl}-Z_{virt}(s)i_{out}\) | \(R_{virt}\), \(L_{virt}\) según objetivo |
| Droop P-f/Q-V | \(\omega=\omega_0-m_p(P-P^*)\), \(V=V_0-m_q(Q-Q^*)\) | \(m_p=\Delta\omega_{max}/P_n\) |
| Amortiguamiento activo | \(v_i=v_{PI}-K_{ad}(i_1-i_2)\) | \(K_{ad}=R_{d,opt}\), \(f_{res}<f_s/6\) |
| 2-DOF | \(u=C(r\cdot F-y)\) | \(F(s)\) para seguimiento sin sobreimpulso |

## 21 — Ejemplo de código: estructura de lazo GFM completo en Python

```python
import numpy as np

class GFM_Controller:
    """Controlador GFM en cascada: corriente + tensión + sincronización PSC."""
    def __init__(self, L1, Cf, wci, wcv, Dp, V0, w0, Ts):
        self.Ts = Ts
        # Lazo de corriente (PI por cancelación de polo)
        R1 = 0.1  # ohm
        self.Kp_i = L1*wci; self.Ki_i = R1*wci; self.xi_d = 0; self.xi_q = 0
        # Lazo de tensión (PI puro)
        self.Kp_v = Cf*wcv**2/wci; self.Ki_v = wcv/5; self.xv_d = 0; self.xv_q = 0
        # PSC
        self.Dp = Dp; self.theta = 0; self.V0 = V0; self.w0 = w0
    
    def step(self, id_ref, iq_ref, id_meas, iq_meas, vd_meas, vq_meas, P_meas):
        Ts = self.Ts
        # Lazo corriente
        ed = id_ref - id_meas; eq = iq_ref - iq_meas
        self.xi_d += Ts*ed; self.xi_q += Ts*eq
        ud = self.Kp_i*ed + self.Ki_i*self.xi_d
        uq = self.Kp_i*eq + self.Ki_i*self.xi_q
        # Desacoplamiento dq (feedforward)
        ud += -self.w0*0.002*iq_meas  # -wL*iq
        uq +=  self.w0*0.002*id_meas  # +wL*id
        # PSC
        self.theta += Ts*(self.w0 + (0 - P_meas)/self.Dp)  # P*=0 por simplificación
        return ud, uq, self.theta
```

## Conceptos relacionados
- [[control-cascada]] · [[metodos-sintesis-control]] · [[ciclo-diseno-control]]

## Referencias
- Aström, Hägglund, *Advanced PID Control*, 2006.
