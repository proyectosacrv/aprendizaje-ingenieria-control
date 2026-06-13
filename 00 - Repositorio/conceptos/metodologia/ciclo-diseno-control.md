---
titulo: Ciclo de diseño de control (Diseñar → Evaluar → Validar)
slug: ciclo-diseno-control
categoria: metodologia
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [estructurar el proceso de diseno de control de un convertidor]
tags: [metodologia, diseno, evaluacion, validacion, proceso]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [especificaciones-control, metodos-sintesis-control, margenes-estabilidad, niveles-validacion, robustez-parametrica]
referencias:
  - "Aström, Murray, Feedback Systems, Princeton 2008"
  - "Skogestad, Postlethwaite, Multivariable Feedback Control, Wiley 2005"
---

## Definición
Marco de trabajo que organiza el diseño de un controlador en tres fases con realimentación entre
ellas: **Diseñar** (de la especificación al controlador), **Evaluar** (¿cumple y es robusto?) y
**Validar** (¿funciona en la realidad?). Es el hilo que da coherencia a todas las técnicas.

## Fundamento teórico
El principio que distingue "conocer técnicas" de "saber diseñar control" es la **trazabilidad**:
$$ \text{requisito} \rightarrow \text{especificación medible} \rightarrow \text{decisión de diseño}
   \rightarrow \text{métrica de evaluación} \rightarrow \text{prueba de validación} $$
Cada decisión de diseño debe tener un criterio de aceptación medible y una prueba que lo
confirme en un nivel de fidelidad adecuado.

<div class="cfig"><img src="figuras/ciclo-diseno-control-ciclo.png" alt="ciclo Diseñar Evaluar Validar con realimentacion"><div class="cap">El diseño de control se organiza en tres fases con realimentación: Diseñar (de la especificación al controlador), Evaluar (¿cumple márgenes y robustez?) y Validar (¿funciona subiendo niveles de fidelidad?); si una fase falla, se rediseña. El hilo conductor es la trazabilidad requisito → especificación → diseño → métrica → prueba.</div></div>

## Las tres fases (mapa)
**1 · Diseñar** — [[especificaciones-control]] · [[arquitecturas-control]] ·
[[metodos-sintesis-control]] (clásico: [[sintonia-pi-pid]], [[loop-shaping]]; estado:
[[asignacion-polos-lqr]]; avanzado: [[control-predictivo]], [[control-robusto-hinf]]).

**2 · Evaluar** — estabilidad ([[analisis-modal]], Nyquist) · [[margenes-estabilidad]] ·
[[funciones-sensibilidad]] · [[metricas-desempeno]] · [[robustez-parametrica]].

**3 · Validar** — [[niveles-validacion]] (lineal → no lineal → conmutado → HIL → real) ·
[[pruebas-validacion]] · [[validacion-cruzada]].

## Cuándo y por qué se usa
Siempre. Evita el error típico de "ajustar ganancias hasta que parezca ir": fuerza a fijar
objetivos medibles antes de diseñar y a validar lo diseñado en el nivel correcto.

## Procedimiento (genérico)
1. Especifica objetivos medibles (ancho de banda, margen de fase, rechazo, robustez).
2. Modela la planta al nivel adecuado (p.ej. promediado dq linealizado).
3. Elige arquitectura y método de síntesis; sintoniza.
4. Evalúa: estabilidad, márgenes, desempeño, robustez paramétrica.
5. Valida subiendo niveles de fidelidad; vuelve a (3) si falla.

## Uso en proyectos
- **01/02 (GFM/GFL)**: el ciclo completo — diseño (cascada/droop/PLL), evaluación (polos,
  impedancia, SCR crítico) y validación (lineal ↔ inyección ↔ conmutado).

## Conceptos relacionados
- [[especificaciones-control]] · [[metodos-sintesis-control]] · [[margenes-estabilidad]] · [[niveles-validacion]]

## Referencias
- Aström, Murray, *Feedback Systems*, 2008 · Skogestad, *Multivariable Feedback Control*, 2005.
