---
titulo: Carga de potencia constante (CPL)
slug: carga-potencia-constante-cpl
categoria: fisica-modelado
tipo: concepto
nivel: avanzado
proyectos: [03-DataCenter-IA]
objetivos: [modelar la carga de convertidores regulados y su efecto desestabilizante]
tags: [CPL, potencia-constante, resistencia-negativa, bus-dc, datacenter]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [no-pasividad-resistencia-negativa, estabilidad-bus-dc-cpl, criterio-middlebrook, modelado-sistemas]
referencias:
  - "Emadi et al., Constant Power Loads and Negative Impedance Instability, IEEE TVT 2006"
---

## Definición
Una **carga de potencia constante (CPL)** consume una potencia fija \( P \) independientemente de
su tensión de alimentación. Es el comportamiento típico de un convertidor con su salida bien
regulada (un POL de servidor, un motor con control de velocidad): aunque caiga la tensión de
entrada, mantiene su potencia subiendo la corriente.

## Fundamento teórico
La corriente de una CPL en función de la tensión del bus es:
$$ i_{cpl} = \frac{P}{V} $$
Su **conductancia incremental** (pendiente \( \partial i/\partial V \)) es **negativa**:
$$ \frac{\partial i_{cpl}}{\partial V} = -\frac{P}{V^2} < 0 $$
Equivale a una **resistencia incremental negativa** \( -V^2/P \). Esta resistencia negativa
**desamortigua** los filtros LC aguas arriba: aporta energía a la resonancia en lugar de
disiparla, lo que puede inestabilizar el bus (ver [[estabilidad-bus-dc-cpl]]). Es un caso
concreto de [[no-pasividad-resistencia-negativa]].

<div class="cfig"><img src="figuras/carga-potencia-constante-cpl-iv.png" alt="curva i-V de una CPL con pendiente incremental negativa"><div class="cap">La CPL sigue $i=P/V$: si la tensión cae, la corriente sube para mantener la potencia. Su pendiente incremental $\partial i/\partial V=-P/V^2$ es negativa (resistencia incremental $-V^2/P$), al revés que una resistencia. Esa pendiente negativa desamortigua los filtros LC aguas arriba y puede inestabilizar el bus.</div></div>

## Cuándo y por qué se usa
Aparece siempre que la carga es un convertidor regulado: microrredes DC, data centers,
electrificación de transporte, accionamientos. Modelarla como CPL (y no como resistencia) es
imprescindible para predecir la estabilidad.

## Procedimiento (genérico)
1. Identifica si la carga regula su salida (entonces es CPL en su entrada).
2. Modela \( i_{cpl}=P/V \); para análisis lineal, usa la resistencia incremental \( -V^2/P \).
3. Evalúa la estabilidad del bus con esa resistencia negativa (autovalores o impedancia).
4. Si desestabiliza, añade amortiguamiento (pasivo, activo) o más capacidad de bus.

## Ejemplo de código
```python
# carga CPL en el balance del bus DC
i_cpl = P_cpl / Vdc                 # no lineal
# linealizada: conductancia incremental negativa
g_incr = -P_cpl / Vdc**2
```

## Parámetros y valores típicos
En un rack de IA, \( P \) de decenas a cientos de kW a \( V_{dc}=400\text{–}800 \) V. La
resistencia incremental \( -V^2/P \) es de fracciones de ohmio.

## Errores comunes
- Modelar la carga como resistencia constante (estable) cuando en realidad es CPL (puede inestabilizar).
- Olvidar que el efecto desestabilizante crece con \( P \) y con tensión de bus baja.

## Uso en proyectos
- **03 - DataCenter-IA**: los servidores/GPUs (vía sus POL) son la CPL del bus DC; su resistencia
  incremental negativa fija la potencia crítica de estabilidad del filtro de distribución.

## Conceptos relacionados
- [[no-pasividad-resistencia-negativa]] · [[estabilidad-bus-dc-cpl]] · [[criterio-middlebrook]]

## Referencias
- Emadi et al., *Constant Power Loads and Negative Impedance Instability*, IEEE TVT 2006.
