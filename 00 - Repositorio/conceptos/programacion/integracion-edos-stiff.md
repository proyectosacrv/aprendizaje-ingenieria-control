---
titulo: Integración de EDOs rígidas (solve_ivp)
slug: integracion-edos-stiff
categoria: programacion
tipo: metodo
nivel: intermedio
proyectos: [01-GFM-Impedance, 03-DataCenter-IA]
objetivos: [simular en el tiempo el modelo no lineal]
tags: [solve_ivp, stiff, LSODA, BDF, simulacion, saturacion]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [current-limiting, vsm-inercia]
referencias:
  - "SciPy docs: scipy.integrate.solve_ivp"
---

## Definición
Simulación temporal de \( \dot{\mathbf{x}}=\mathbf{f}(\mathbf{x},\mathbf{u},t) \) con un
integrador adecuado. Los modelos de convertidores son **rígidos** (stiff): conviven dinámicas
muy rápidas (resonancia LCL ~kHz) y lentas (droop ~Hz), lo que exige solvers implícitos.

## Fundamento teórico
Un sistema es **stiff** cuando la relación entre la constante de tiempo más rápida y la más
lenta es grande. Los métodos explícitos (RK45) necesitan pasos minúsculos por estabilidad
numérica; los **implícitos** (BDF, LSODA) manejan la rigidez con pasos mayores.

<div class="cfig"><img src="figuras/integracion-edos-stiff-comparativa.png" alt="integrador explicito inestable frente a implicito estable en sistema stiff"><div class="cap">En un sistema stiff (dinámica rápida $\tau\sim20$ ms junto a una lenta), un método explícito con paso grande viola su límite de estabilidad numérica y oscila o diverge, mientras un método implícito (BDF/LSODA) absorbe la rigidez y sigue la solución con pasos mayores. Por eso los modelos de convertidor (resonancia LCL + droop) exigen solvers implícitos.</div></div>

## Cuándo y por qué se usa
Para validar el diseño en el dominio del tiempo (transitorios, faltas, gran señal) que el
análisis lineal no captura.

## Procedimiento de diseño (genérico)
1. Usa `method='LSODA'` o `'BDF'` (implícitos) para sistemas rígidos.
2. Fija `rtol/atol` ajustados (1e-7/1e-9) y un `max_step` que resuelva la dinámica rápida.
3. Para muestrear, usa `t_eval` (acota memoria) o `dense_output` (interpolación).
4. **Cuidado con discontinuidades** (saturaciones, escalones): el paso adaptativo se reduce
   mucho. Para saturación cíclica sostenida, suaviza el límite o usa eventos; `dense_output`
   puede agotar memoria al acumular millones de pasos internos.

## Ejemplo de código
```python
from scipy.integrate import solve_ivp
sol = solve_ivp(rhs, (0, t_end), x0, args=(...,),
                method="LSODA", rtol=1e-7, atol=1e-9,
                max_step=1e-3, t_eval=t_grid)   # t_eval acota memoria
```

## Parámetros y valores típicos
`rtol` 1e-6–1e-8, `max_step` ~1/(20·f_max). Escalón único: manejable; saturación en cada ciclo:
costosa (suavizar o paso fijo).

## Errores comunes
- Usar RK45 en sistema stiff → lentísimo o falla.
- `dense_output=True` con saturación dura → MemoryError por exceso de pasos internos (usar
  `t_eval`).
- Discontinuidades duras repetidas → el integrador se "atasca".

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: gran señal): `simulate.py` integra los 16 estados (con VSM)
  para el escalón de potencia y la falta. La saturación cíclica obligó a acotar el alcance del
  experimento de inyección con límite.

## Conceptos relacionados
- [[current-limiting]] · [[vsm-inercia]]

## Referencias
- SciPy `integrate.solve_ivp`.
