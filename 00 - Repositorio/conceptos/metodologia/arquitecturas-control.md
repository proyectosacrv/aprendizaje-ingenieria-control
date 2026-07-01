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

## Errores comunes
- Feedforward que desestabiliza (en el GFM, el feedforward de carga lo hacía): siempre verificar.
- Cascada sin separación de escalas → los lazos interactúan.

## Uso en proyectos
- **01 (GFM)**: cascada tensión/corriente + desacoplo dq + impedancia virtual + damping activo.
- **02 (GFL)**: lazo de corriente + PLL; sin lazo de tensión externo.

## Conceptos relacionados
- [[control-cascada]] · [[metodos-sintesis-control]] · [[ciclo-diseno-control]]

## Referencias
- Aström, Hägglund, *Advanced PID Control*, 2006.
