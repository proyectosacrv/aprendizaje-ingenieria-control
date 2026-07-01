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
fecha_actualizacion: 2026-06-30
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

## 1 — La región de estabilidad de Euler explícito y el límite de paso
**Paso 1 — la ecuación de prueba.** El comportamiento de un integrador se estudia sobre la EDO escalar lineal \( \dot x=\lambda x \), cuya solución exacta \( x(t)=x_0 e^{\lambda t} \) decae si \( \operatorname{Re}\lambda<0 \). Un sistema lineal \( \dot{\mathbf x}=A\mathbf x \) se diagonaliza y cada modo se comporta como esta ecuación con \( \lambda \) un autovalor de \( A \).

**Paso 2 — aplicar Euler explícito (hacia adelante).** El esquema avanza con la derivada en el punto actual: \( x_{n+1}=x_n+h\,f(x_n)=x_n+h\lambda x_n \). Factorizando:

$$ x_{n+1}=(1+h\lambda)\,x_n\;\Longrightarrow\;x_n=(1+h\lambda)^n x_0 $$

**Paso 3 — condición de no divergencia.** La solución numérica \( x_n \) permanece acotada (no explota) solo si el **factor de amplificación** tiene módulo \( \le1 \):

$$ \boxed{\;|1+h\lambda|<1\;} $$

Esta es la **región de estabilidad absoluta** de Euler explícito: un disco en el plano complejo \( h\lambda \) de radio 1 centrado en \( -1 \).

**Paso 4 — el límite de paso para un modo real.** Para un modo real \( \lambda<0 \), la condición \( |1+h\lambda|<1 \) se reduce a \( -1<1+h\lambda<1 \), es decir \( -2<h\lambda<0 \). Como \( \lambda<0 \):

$$ \boxed{\;h<\frac{2}{|\lambda|}\;} $$

El paso queda atado a la dinámica **más rápida** (mayor \( |\lambda| \)). Para la resonancia LCL a \( \sim1\,\text{kHz} \) (\( \lambda\approx-2\pi\cdot10^3 \)), el límite es \( h<2/6283\approx318\,\mu\text{s} \): por estabilidad numérica, no por precisión.

## 2 — Por qué un sistema stiff exige un paso implícito
**Paso 1 — definir la rigidez.** Un sistema es **stiff** cuando coexisten autovalores de magnitudes muy dispares. Se mide con la razón de rigidez:

$$ S=\frac{\max_i|\operatorname{Re}\lambda_i|}{\min_i|\operatorname{Re}\lambda_i|} $$

En un convertidor con resonancia LCL (\( \tau_{rápido}\sim0{,}16\,\text{ms} \)) y droop (\( \tau_{lento}\sim0{,}16\,\text{s} \)), \( S\sim10^3 \) o más.

**Paso 2 — el conflicto.** El modo rápido ya está prácticamente extinguido tras unos pocos \( \tau_{rápido} \), pero sigue **presente en el espectro de \( A \)**. Euler explícito debe respetar \( h<2/|\lambda_{máx}| \) por el modo rápido **durante toda la simulación**, aunque ese modo ya no aporte nada a la solución. Para cubrir el transitorio lento (\( \sim5\tau_{lento}=0{,}8\,\text{s} \)) con \( h\approx318\,\mu\text{s} \) hacen falta \( \sim2500 \) pasos, todos limitados por una dinámica irrelevante.

**Paso 3 — la solución implícita.** Euler hacia atrás (implícito) evalúa la derivada en el punto **nuevo**: \( x_{n+1}=x_n+h\lambda x_{n+1} \). Despejando:

$$ x_{n+1}=\frac{1}{1-h\lambda}\,x_n,\qquad\text{factor de amplificación }=\frac{1}{1-h\lambda} $$

**Paso 4 — estabilidad incondicional.** Para \( \operatorname{Re}\lambda<0 \) y cualquier \( h>0 \), el denominador \( |1-h\lambda|>1 \), luego \( \big|\tfrac{1}{1-h\lambda}\big|<1 \) **siempre**:

$$ \boxed{\;\operatorname{Re}\lambda<0\;\Rightarrow\;\left|\frac{1}{1-h\lambda}\right|<1\quad\forall\,h>0\;} $$

La región de estabilidad cubre todo el semiplano izquierdo (método **A-estable**). El paso ya no lo dicta la estabilidad sino la **precisión** deseada sobre la dinámica lenta, así que puede ser \( \sim10^3 \) veces mayor. Por eso los solvers stiff de `solve_ivp` (BDF, LSODA, ambos implícitos) absorben la rigidez: pagan resolver un sistema de ecuaciones por paso (con la Jacobiana) a cambio de dar pasos enormes. RK45, explícito, conserva el límite \( h<2/|\lambda_{máx}| \) y se vuelve lentísimo o falla.

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
