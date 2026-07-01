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

## Uso en proyectos
- **01/02**: método clásico (cascada + sintonía por ancho de banda) + técnicas de convertidor
  (impedancia virtual, damping activo, PLL). Los demás métodos se abordarán en proyectos propios.

## Conceptos relacionados
- [[sintonia-pi-pid]] · [[loop-shaping]] · [[asignacion-polos-lqr]] · [[control-predictivo]] · [[control-robusto-hinf]]

## Referencias
- Skogestad, Postlethwaite, *Multivariable Feedback Control*, 2005.
