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

## 3 — Sistema rígido: razón de rigidez y consecuencias para Euler explícito

Un sistema es **rígido** cuando la razón de rigidez \( S \) es grande:

$$ S = \frac{\max_i |\text{Re}(\lambda_i)|}{\min_i |\text{Re}(\lambda_i)|} \gg 1 $$

En un convertidor con filtro LCL (\( f_{res} \approx 1\,\text{kHz} \), \( \tau_{rápido} = 1/(2\pi \times 10^3) \approx 0.16\,\text{ms} \)) y lazo de droop (\( \tau_{lento} \approx 160\,\text{ms} \)): \( S \approx 10^3 \).

**Euler explícito** es inestable si \( h > 2/|\lambda_{max}| \). Para la resonancia LCL (\( \lambda \approx -2\pi \times 10^3 \)): \( h_{max} < 318\,\mu\text{s} \). Simular 10 s de operación requiere \( 10/318\times10^{-6} \approx 31500 \) pasos mínimos — limitados por una dinámica que ya está extinguida a los 1 ms.

**Implicación práctica:** para un sistema de 16 estados (GFM con VSM, LCL, droop, PLL), RK45 puede necesitar \( > 10^7 \) pasos para simular 1 s, tardando minutos. BDF/LSODA con paso adaptativo resuelve el mismo caso en < 1000 pasos efectivos.

$$ \boxed{S = \frac{|\lambda_{max}|}{|\lambda_{min}|} \approx 10^3;\quad h_{Euler} < \frac{2}{|\lambda_{max}|} = 318\,\mu\text{s};\quad h_{BDF} \sim \frac{T_{lento}}{20} \approx 8\,\text{ms}} $$

## 4 — Euler implícito: incondicionalmente estable, primer orden

**Euler hacia atrás (implícito):** evalúa la derivada en el punto nuevo \( x_{n+1} \):

$$ x_{n+1} = x_n + h\,f(x_{n+1}) $$

Para la EDO de prueba \( \dot x = \lambda x \): \( x_{n+1} = x_n + h\lambda x_{n+1} \Rightarrow x_{n+1} = x_n/(1 - h\lambda) \). El factor de amplificación \( R(h\lambda) = 1/(1-h\lambda) \).

**Estabilidad incondicional:** para \( \text{Re}(\lambda) < 0 \) y cualquier \( h > 0 \):

$$ |1 - h\lambda| = \sqrt{(1-h\text{Re}\lambda)^2 + (h\text{Im}\lambda)^2} > 1 \Rightarrow |R| < 1 \quad \forall h > 0 $$

La región de estabilidad cubre todo el semiplano izquierdo (método A-estable). El paso lo dicta la **precisión**, no la estabilidad.

**Coste computacional:** cada paso requiere resolver el sistema lineal \( (I - hJ)\Delta x = -hf(x_n) \) donde \( J = \partial f/\partial x \). Para un sistema de \( n \) estados, el coste es \( O(n^3) \) por factorización LU (o \( O(n^2) \) si \( J \) es esparsa). Los solvers modernos (LSODA, BDF) reutilizan la factorización LU durante varias iteraciones y la recomputan solo cuando el Jacobiano cambia significativamente.

**Precisión:** Euler implícito es de **primer orden** — el error global es \( O(h) \). Para alta precisión, se prefieren métodos de orden superior como BDF de orden 2–5 o Radau de orden 5.

## 5 — Runge-Kutta implícito Radau y BDF: alta precisión + estabilidad

**BDF (Backward Differentiation Formulas):** métodos multipaso implícitos de orden 1–5. La fórmula de orden \( k \) usa los \( k \) últimos valores de \( x \):

$$ \sum_{i=0}^{k} \alpha_i x_{n+1-i} = h\,\beta_0 f(x_{n+1}) $$

Los coeficientes \( \alpha_i, \beta_0 \) se eligen para que el método sea de orden \( k \) y A-estable (o A(\alpha)-estable para órdenes > 2). BDF-2 es popular: 2° orden, A-estable, buen compromiso.

`scipy.integrate.solve_ivp(method='BDF')` implementa BDF adaptativo con paso y orden variables (VODE).

**Radau IIA (Runge-Kutta implícito):** método de alto orden (orden 5) con excelentes propiedades de estabilidad (L-estable: atenúa fuertemente los modos rígidos). Usa una fórmula de Runge-Kutta con coeficientes implícitos que requiere resolver un sistema de ecuaciones no lineales en cada paso:

$$ \mathbf{k}_i = f\left(x_n + h\sum_j a_{ij}\mathbf{k}_j\right) $$

`scipy.integrate.solve_ivp(method='Radau')` implementa Radau IIA de orden 5. Para sistemas muy rígidos con alta precisión requerida, Radau supera a BDF en robustez (aunque es más caro por paso).

## 6 — Selección del solver: criterios y comparativa

| Solver | Orden | Stiff | Paso | Coste/paso | Uso |
|---|---|---|---|---|---|
| RK45 (Dormand-Prince) | 4–5 | No | Adaptativo | Bajo | Sistemas no rígidos |
| RK23 | 2–3 | No | Adaptativo | Muy bajo | No rígidos, baja precisión |
| BDF | 1–5 | Sí | Adaptativo | Medio | Sistemas rígidos general |
| Radau | 5 | Sí | Adaptativo | Alto | Muy rígidos, alta precisión |
| LSODA | 1–12 | Sí/No | Adaptativo | Medio | Detecta rigidez automáticamente |

**Regla de selección:**
- Sistema de control de lazo de corriente (no muy rígido, \( S < 100 \)): RK45 funciona.
- Convertidor con filtro LCL + control (\( S \sim 10^3 \)): BDF o LSODA.
- Sistema completo con resonancia LCL + droop + red (\( S > 10^4 \)): Radau.
- Incertidumbre sobre la rigidez: LSODA (detecta automáticamente y cambia de Adams a BDF).

**Paso adaptativo:** todos los solvers modernos ajustan el paso para mantener el error relativo < `rtol` y el error absoluto < `atol`. Con `rtol=1e-6, atol=1e-8`, los solvers stiff dan típicamente 10–100× menos pasos que el equivalente explícito.

```python
from scipy.integrate import solve_ivp

# Para sistema rígido general: BDF
sol_bdf = solve_ivp(rhs, (0, 1.0), x0, method='BDF',
                    rtol=1e-7, atol=1e-9, t_eval=t_grid)

# Para sistema muy rígido con alta precisión: Radau
sol_rad = solve_ivp(rhs, (0, 1.0), x0, method='Radau',
                    rtol=1e-8, atol=1e-10, t_eval=t_grid)

# Comparar número de pasos efectivos:
print(f"BDF pasos: {sol_bdf.t.size}, Radau: {sol_rad.t.size}")
```

## 7 — Sistema rígido en convertidores: razón de rigidez y solvers recomendados

Los modelos de convertidores de potencia son inherentemente rígidos por la coexistencia de escalas de tiempo muy distintas:

| Dinámica | Constante de tiempo típica | \(|\lambda|\) |
|---|---|---|
| Resonancia LCL (\(f_{res}\sim1\,\text{kHz}\)) | \(\tau\sim0.16\,\text{ms}\) | \(\sim6283\,\text{rad/s}\) |
| Lazo de corriente (\(f_c\sim500\,\text{Hz}\)) | \(\tau\sim0.32\,\text{ms}\) | \(\sim3142\,\text{rad/s}\) |
| Lazo de tensión (\(f_c\sim150\,\text{Hz}\)) | \(\tau\sim1\,\text{ms}\) | \(\sim942\,\text{rad/s}\) |
| PLL (\(f_{PLL}\sim20\,\text{Hz}\)) | \(\tau\sim8\,\text{ms}\) | \(\sim125\,\text{rad/s}\) |
| Droop de potencia (\(\tau_f\sim30\,\text{ms}\)) | \(\tau\sim30\,\text{ms}\) | \(\sim33\,\text{rad/s}\) |
| Inercia virtual (\(H=5\,\text{s}\)) | \(\tau\sim160\,\text{ms}\) | \(\sim6.3\,\text{rad/s}\) |

Razón de rigidez: \(S=|\lambda_{max}|/|\lambda_{min}|\approx6283/6.3\approx10^3\).

**Consecuencia:** RK45 (explícito) necesitaría \(h<2/6283\approx318\,\mu\text{s}\) durante toda la simulación aunque la resonancia LCL esté amortiguada en los primeros milisegundos. Para simular 1 s de operación: >3000 pasos mínimos por estabilidad. BDF/LSODA detecta que la dinámica rápida ya está extinguida y amplía el paso a ~8 ms → <125 pasos efectivos.

**Recomendaciones para proyectos de convertidores:**
- Sistema de 8–16 estados (lazo de corriente + LCL + PLL): `method='LSODA'` con `rtol=1e-7, atol=1e-9`.
- Sistema completo con VSM + red (\(S>10^4\)): `method='Radau'` con `rtol=1e-8, atol=1e-10`.
- `max_step=1e-3`: limita el paso máximo para no saltar transitorios importantes (escalones, faltas).

## 8 — Euler explícito vs implícito: comparativa paso a paso

**Euler explícito (hacia adelante):** \(x_{n+1}=x_n+h\,f(x_n)\)
- Región de estabilidad: disco de radio 1 en el plano \(h\lambda\) centrado en \(-1\).
- Para \(\lambda\) real negativo: \(h<2/|\lambda|\).
- Coste por paso: \(O(n)\) — solo evalúa \(f\).
- Sin resolver sistemas lineales: barato por paso, pero muchos pasos en sistemas rígidos.

**Euler implícito (hacia atrás):** \(x_{n+1}=x_n+h\,f(x_{n+1})\)
- Requiere resolver \((I-hJ)x_{n+1}=x_n+h\,f_0\) con factorización LU \(O(n^3)\).
- Región de estabilidad: todo el semiplano izquierdo (A-estable).
- Paso dictado por la precisión, no la estabilidad: puede ser 10–1000× mayor.
- Error global \(O(h)\): primer orden — adecuado para validación rápida pero no para alta precisión.

**BDF de orden k:** extiende Euler implícito usando los últimos \(k\) puntos para extrapolación de orden superior. BDF-2 (segundo orden) es A-estable; BDF-3 a BDF-5 son A(\(\alpha\))-estables con ángulo de estabilidad >70°. `scipy` implementa BDF con orden y paso adaptativos (VODE).

**Radau IIA (orden 5):** L-estable — atenúa fuertemente los modos rígidos incluso con pasos grandes. Resuelve un sistema de ecuaciones no lineales en cada paso (Runge-Kutta implícito de 3 etapas). Más robusto que BDF para sistemas muy rígidos o con discontinuidades frecuentes (saturaciones).

## 9 — Discontinuidades y saturaciones: cómo manejarlas

Las saturaciones repetidas (current limiting en cada ciclo de 20 ms) crean **discontinuidades** en la derivada que los solvers de paso adaptativo manejan reduciendo el paso al mínimo en cada discontinuidad:

**Síntoma:** `solve_ivp` termina con `status=-1` ("Required step size is less than spacing between numbers") o tarda 100× más de lo esperado.

**Soluciones:**
1. **Suavizar la saturación:** reemplazar la saturación dura \(\text{sat}(x,x_{max})\) por una función suave:
$$\text{sat}_{soft}(x,x_m)=x_m\,\tanh(x/x_m)$$
La derivada existe en todo punto; el solver mantiene pasos razonables.

2. **Usar `events`:** definir un evento de cruce cuando \(|x|=x_{max}\) — el solver detecta la discontinuidad exactamente y reinicia el paso adaptativo desde el punto de cruce.

3. **Paso fijo:** si las discontinuidades son muy frecuentes y regulares (saturación en cada período), usar un integrador de paso fijo (Euler implícito con \(h=T_s/10\)) implementado manualmente. Pierde la eficiencia del paso adaptativo pero es predecible.

4. **`t_eval` en vez de `dense_output`:** con `dense_output=True` el solver acumula todos los pasos internos en memoria; con saturación frecuente puede agotar la RAM. `t_eval` acota la memoria al número de puntos de salida deseados.

<div class="cfig"><img src="../figuras/integracion-edos-stiff-analisis.png" alt="Euler explícito inestable, región estabilidad, paso adaptativo Radau y comparativa solvers"><div class="cap">Integración de EDOs rígidas: (a) Euler explícito explota con paso grande en sistema stiff; Euler implícito se mantiene estable. (b) Regiones de estabilidad: disco (explícito) vs semiplano izquierdo completo (implícito). (c) Paso adaptativo de Radau: paso grande durante la dinámica lenta, reducido en el transitorio. (d) Comparativa pasos efectivos vs error para RK45, BDF y Radau.</div></div>

## Conceptos relacionados
- [[current-limiting]] · [[vsm-inercia]]

## Referencias
- SciPy `integrate.solve_ivp`.
- Hairer, Wanner, *Solving Ordinary Differential Equations II: Stiff Problems*, Springer 1996.
