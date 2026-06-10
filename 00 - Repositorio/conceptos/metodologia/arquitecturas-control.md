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
fecha_actualizacion: 2026-06-08
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
