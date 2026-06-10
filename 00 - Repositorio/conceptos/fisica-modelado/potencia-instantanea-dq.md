---
titulo: Potencia instantánea en dq (P, Q)
slug: potencia-instantanea-dq
categoria: fisica-modelado
tipo: concepto
nivel: basico
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [medir P y Q para el droop y el reparto de carga]
tags: [potencia, activa, reactiva, dq, medida]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [marco-dq, droop-control]
referencias:
  - "Akagi et al., Instantaneous Power Theory, Wiley-IEEE 2007"
---

## Definición
Cálculo de las potencias activa (P) y reactiva (Q) a partir de tensiones y corrientes en el
marco dq, sin necesidad de promediar sobre un periodo de red (medida "instantánea").

## Fundamento teórico
Con convención de **amplitud de pico de fase**:
$$ P=\tfrac{3}{2}(v_d i_d + v_q i_q), \qquad Q=\tfrac{3}{2}(v_q i_d - v_d i_q) $$
(Con convención de potencia invariante el factor 3/2 desaparece.) Si el eje d se alinea con la
tensión (\( v_q=0 \)): \( P=\tfrac{3}{2}v_d i_d \), \( Q=-\tfrac{3}{2}v_d i_q \) → P↔\( i_d \),
Q↔\( i_q \).

## Cuándo y por qué se usa
Para el droop (que reacciona a P y Q), el reparto de carga y la supervisión. Se suele **filtrar**
(paso-bajo) para eliminar el rizado de conmutación y los transitorios rápidos.

## Procedimiento de diseño (genérico)
1. Elige el punto de medida (condensador, PCC) y el alineamiento del marco.
2. Aplica las fórmulas con la convención coherente con tu transformada dq.
3. Filtra P y Q (corte 5–20 Hz) para el droop.

## Ejemplo de aplicación real
**Problema:** VSC con \( V_d=325\,\text{V} \), \( V_q=0 \) (marco orientado a la tensión). Calcular las referencias de corriente para inyectar \( P^*=500\,\text{kW} \) y absorber \( Q^*=100\,\text{kVAr} \) (inductivo).

Con el marco orientado: \( P=\tfrac{3}{2}V_d i_d \) y \( Q=-\tfrac{3}{2}V_d i_q \). Despejando: \( i_d^*=2P^*/(3V_d)=2\times500000/(3\times325)\approx1026\,\text{A} \); \( i_q^*=-2Q^*/(3V_d)=-2\times100000/(3\times325)\approx-205\,\text{A} \) (negativo porque absorción inductiva exige corriente reactiva en fase −q). Estas son las referencias que el lazo de corriente en dq debe seguir. Verificación: \( P_{real}=\tfrac{3}{2}\times325\times1026\approx500\,\text{kW} \) ✓.

## Ejemplo de código
```python
P = 1.5*(vd*id + vq*iq)
Q = 1.5*(vq*id - vd*iq)
dPm = wf*(P - Pm); dQm = wf*(Q - Qm)   # filtrado para el droop
```

## Parámetros y valores típicos
Corte del filtro de potencia 5–20 Hz. Factor 3/2 con amplitud de pico.

## Errores comunes
- Mezclar la convención de la transformada con la de la potencia (factor 3/2).
- Signo de Q según convención (inductivo/capacitivo): verifícalo en el equilibrio.

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: alimentar el droop): P,Q medidas en el condensador y
  filtradas a 15 Hz alimentan el droop P-f/Q-V. Son 2 de los 15 estados (\( P_m,Q_m \)).

## Conceptos relacionados
- [[marco-dq]] · [[droop-control]]

## Referencias
- Akagi et al., *Instantaneous Power Theory*, 2007.
