---
titulo: Cálculo del punto de equilibrio (fsolve)
slug: equilibrio-fsolve
categoria: programacion
tipo: metodo
nivel: basico
proyectos: [01-GFM-Impedance, 02-GFL-Impedance, 03-DataCenter-IA]
objetivos: [hallar el punto de operacion antes de linealizar]
tags: [equilibrio, fsolve, scipy, punto-operacion, raices]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-30
relacionados: [linealizacion-numerica, analisis-modal]
referencias:
  - "SciPy docs: scipy.optimize.fsolve"
---

## Definición
Resolver \( \mathbf{f}(\mathbf{x}_e,\mathbf{u}_e)=0 \) numéricamente para hallar el **punto de
equilibrio** (régimen permanente) de un sistema no lineal, paso previo imprescindible a la
linealización.

## Fundamento teórico
`fsolve` (método híbrido de Powell) busca la raíz del campo vectorial partiendo de una
estimación inicial \( \mathbf{x}_0 \). La calidad del resultado se mide por el **residuo**
\( \lVert\mathbf{f}(\mathbf{x}_e)\rVert \), que debe ser ~0 (p.ej. <1e-9).

<div class="cfig"><img src="figuras/equilibrio-fsolve-convergencia.png" alt="convergencia del residuo de fsolve con buen y mal guess inicial"><div class="cap">Convergencia de fsolve: partiendo de una estimación inicial física (corrientes desde la potencia, tensión nominal) el residuo $\|f(x)\|$ cae hasta ~$10^{-11}$ en pocas iteraciones; con un guess pobre el método se estanca en una raíz espuria sin sentido físico. Por eso el paso crítico es construir un buen $x_0$ y verificar siempre el residuo.</div></div>

## 1 — De dónde sale la iteración de Newton-Raphson
**Paso 1 — el problema.** Buscamos \( \mathbf{x}_e \) tal que \( \mathbf{f}(\mathbf{x}_e)=0 \), con \( \mathbf{f}:\mathbb{R}^n\to\mathbb{R}^n \) no lineal. No hay fórmula cerrada; iteramos desde un \( \mathbf{x}_0 \).

**Paso 2 — linealizar alrededor del iterado actual.** Cerca de \( \mathbf{x}_k \), el desarrollo de Taylor de primer orden del campo vectorial es:

$$ \mathbf{f}(\mathbf{x}_k+\Delta\mathbf{x})\approx \mathbf{f}(\mathbf{x}_k)+J(\mathbf{x}_k)\,\Delta\mathbf{x},\qquad J_{ij}=\frac{\partial f_i}{\partial x_j} $$

donde \( J \) es la matriz **Jacobiana** evaluada en \( \mathbf{x}_k \).

**Paso 3 — imponer que el modelo lineal valga cero.** Pedimos que el incremento \( \Delta\mathbf{x} \) lleve la aproximación a la raíz, \( \mathbf{f}(\mathbf{x}_k)+J(\mathbf{x}_k)\Delta\mathbf{x}=0 \). Resolviendo el sistema lineal:

$$ \Delta\mathbf{x}=-J(\mathbf{x}_k)^{-1}\mathbf{f}(\mathbf{x}_k) $$

**Paso 4 — actualizar.** El nuevo iterado es \( \mathbf{x}_{k+1}=\mathbf{x}_k+\Delta\mathbf{x} \), es decir:

$$ \boxed{\;\mathbf{x}_{k+1}=\mathbf{x}_k-J(\mathbf{x}_k)^{-1}\,\mathbf{f}(\mathbf{x}_k)\;} $$

(En la práctica no se invierte \( J \): se resuelve \( J\,\Delta\mathbf{x}=-\mathbf{f} \) por factorización LU. `fsolve` usa una variante híbrida de Powell que combina Newton con descenso de gradiente cuando \( J \) está mal condicionada, y aproxima \( J \) por diferencias finitas si no se da.)

## 2 — Por qué la convergencia es cuadrática
**Paso 1 — definir el error.** Sea \( \mathbf{x}_e \) la raíz y \( e_k=\mathbf{x}_k-\mathbf{x}_e \) el error del iterado \( k \). Queremos relacionar \( e_{k+1} \) con \( e_k \).

**Paso 2 — Taylor de segundo orden de la raíz.** Como \( \mathbf{f}(\mathbf{x}_e)=0 \), desarrollando \( \mathbf{f} \) en \( \mathbf{x}_k \) y evaluando en la raíz (caso escalar para ver el mecanismo):

$$ 0=f(\mathbf{x}_e)=f(\mathbf{x}_k)+f'(\mathbf{x}_k)(\mathbf{x}_e-\mathbf{x}_k)+\tfrac12 f''(\xi)(\mathbf{x}_e-\mathbf{x}_k)^2 $$

con \( \xi \) entre \( \mathbf{x}_k \) y \( \mathbf{x}_e \).

**Paso 3 — sustituir la actualización de Newton.** Dividiendo entre \( f'(\mathbf{x}_k) \) y usando \( \mathbf{x}_{k+1}=\mathbf{x}_k-f(\mathbf{x}_k)/f'(\mathbf{x}_k) \), el término \( f(\mathbf{x}_k)/f'(\mathbf{x}_k) \) se reescribe como \( \mathbf{x}_k-\mathbf{x}_{k+1} \). Reagrupando, los términos lineales en el error se cancelan y queda:

$$ e_{k+1}=\mathbf{x}_{k+1}-\mathbf{x}_e=\frac{f''(\xi)}{2f'(\mathbf{x}_k)}\,e_k^2 $$

**Paso 4 — la cota cuadrática.** Tomando módulos, con \( C=\big|f''/2f'\big| \) acotado cerca de la raíz:

$$ \boxed{\;|e_{k+1}|\le C\,|e_k|^2\;} $$

El error **se eleva al cuadrado** en cada paso: si \( |e_k|\sim10^{-3} \), entonces \( |e_{k+1}|\sim10^{-6} \), luego \( \sim10^{-12} \). El número de dígitos correctos **se duplica** por iteración. Por eso el residuo cae a \( \sim10^{-11} \) en pocas iteraciones (en el ejemplo, <20). La condición es que \( f'(\mathbf{x}_e)\neq0 \) (Jacobiana no singular en la raíz) y que \( \mathbf{x}_0 \) esté en la **cuenca de atracción**: de ahí la importancia del guess físico, pues un \( \mathbf{x}_0 \) lejano puede caer en otra cuenca y converger a una raíz espuria.

## Cuándo y por qué se usa
Siempre que se quiera linealizar o analizar alrededor de un punto de operación concreto
(potencia, tensión dadas). Un buen equilibrio garantiza que \( A,B,C,D \) tienen sentido físico.

## Procedimiento de diseño (genérico)
1. Implementa \( \mathbf{f}(\mathbf{x},\mathbf{u}) \).
2. Construye una **estimación inicial física**: corrientes desde la potencia
   (\( i_d\approx P/(1.5V) \)), tensión ≈ nominal, ángulos pequeños. Un buen \( x_0 \) evita
   raíces espurias.
3. Llama a `fsolve` con `full_output=True` y `xtol` ajustado.
4. **Verifica el residuo** y que las magnitudes son físicas (P, Q, |v| coherentes).

## Ejemplo de aplicación real
**Problema:** Convertidor GFM de 5 kW operando a \( P^*=5\,\text{kW} \), \( Q^*=0 \), tensión de red \( V_g=325\,\text{V} \). Verificar que `fsolve` converge a un equilibrio físico con residuo <1e-6.

Se inicializa \( x_0 \) con estimaciones físicas: \( i_d\approx P/(1.5V_g)\approx10.3\,\text{A} \), \( i_q=0 \), \( v_d=V_g \), ángulo \( \delta\approx0 \). `fsolve` converge en <20 iteraciones con residuo \( \approx5\times10^{-11} \). Las magnitudes del equilibrio se verifican: \( P_{eq}\approx5000\,\text{W} \), \( Q_{eq}\approx0 \), \( |v_{dq}|=325\,\text{V} \). Si el guess inicial es pobre (todo ceros), puede converger a un equilibrio espurio (\( P=0 \)): por eso el paso crítico es construir estimaciones físicas. Desde este \( x_e \) se linealiza para obtener la matriz \( A \) y analizar los modos.

## Ejemplo de código
```python
from scipy.optimize import fsolve
import numpy as np
x0 = np.zeros(n)
x0[idx_id] = Pset/(1.5*Vg); x0[idx_vd] = Vg      # guess fisico
xe, info, ier, msg = fsolve(lambda x: f(x, u), x0, full_output=True, xtol=1e-12)
res = np.linalg.norm(f(xe, u))
assert res < 1e-6, f"equilibrio no converge: {res}"
```

## Parámetros y valores típicos
`xtol` 1e-10–1e-12; residuo aceptable <1e-6 (en el proyecto ~1e-10).

## Errores comunes
- Guess inicial pobre → converge a una raíz sin sentido o no converge.
- No comprobar el residuo y asumir que convergió.

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: punto de operación): equilibrio para P=5 kW, Q=0 con
  residuo ~1e-10; de ahí salen P_eq, Q_eq, δ. En `model.py` (`equilibrium`).

## Conceptos relacionados
- [[linealizacion-numerica]] · [[analisis-modal]]

## Referencias
- SciPy `optimize.fsolve`.

## 3 — Newton-Raphson: convergencia cuadrática y sensibilidad al punto inicial

El método de Newton-Raphson converge cuadráticamente cerca de la solución: el error en el iterado \( k+1 \) es proporcional al cuadrado del error en el iterado \( k \):

$$ \mathbf{x}_{k+1} = \mathbf{x}_k - J(\mathbf{x}_k)^{-1}\,\mathbf{f}(\mathbf{x}_k),\quad |e_{k+1}| \leq C\,|e_k|^2 $$

**Convergencia en la práctica:** si \( |e_0| = 0.1 \), tras 5 iteraciones el error es \( \sim 10^{-32} \) (con \( C \sim 1 \)). Por eso `fsolve` converge en < 20 iteraciones cuando el guess inicial es bueno.

**Sensibilidad al punto inicial:** el método solo converge si \( \mathbf{x}_0 \) está en la **cuenca de atracción** de la raíz deseada. Lejos de la raíz, el Jacobiano puede estar mal condicionado (\( \det J \approx 0 \)) y el paso \( J^{-1}\mathbf{f} \) dispara el iterado a una región sin significado físico. Señales de alerta:
- El residuo \( \|\mathbf{f}(\mathbf{x}_e)\| \) no cae por debajo de \( 10^{-6} \).
- La solución tiene magnitudes físicamente imposibles (corrientes negativas, tensiones > \( V_{dc} \)).
- El flag `ier` de `fsolve` es 5 (máximo de iteraciones alcanzado).

**Inicialización física:** construir \( \mathbf{x}_0 \) desde relaciones de régimen permanente conocidas:
- Corriente dq: \( i_d^* \approx P/(1.5\,V_g) \), \( i_q^* = Q/(1.5\,V_g) \).
- Ángulo de potencia: \( \delta \approx \arctan(X \cdot P / (V^2)) \) (pequeño en red fuerte).
- Tensión del bus: \( V_{dc} \approx V_{dc}^{nom} \).

## 4 — `scipy.optimize.fsolve`: interfaz y tolerancias

`fsolve` envuelve la rutina MINPACK `hybrd`, que combina Newton-Raphson con descenso de gradiente (método híbrido de Powell). Cuando la Jacobiana está mal condicionada, `hybrd` cambia automáticamente a descenso de gradiente para mantenerse estable.

**Parámetros clave:**
- `ftol` (tolerancia en la función): el solver para cuando \( \|\mathbf{f}(\mathbf{x})\| < \text{ftol} \). Defecto: \( 1.49 \times 10^{-8} \). Para modelos con variables de muy distinta escala (A y V mezclados), usar `ftol=1e-10`.
- `xtol` (tolerancia en la variable): el solver para cuando el paso en \( \mathbf{x} \) es \( < \text{xtol} \). Defecto: \( 1.49 \times 10^{-8} \).
- `full_output=True`: retorna además el diccionario `infodict` con el número de evaluaciones de función, el residuo en cada iteración y la Jacobiana estimada.

```python
from scipy.optimize import fsolve
import numpy as np

xe, info, ier, msg = fsolve(
    lambda x: f(x, u), x0,
    full_output=True, xtol=1e-12, ftol=1e-10
)
res = np.linalg.norm(f(xe, u))
if ier != 1:
    print(f"ADVERTENCIA: fsolve no converge — {msg}")
if res > 1e-6:
    raise ValueError(f"Residuo demasiado grande: {res:.2e}")
```

**Jacobiana analítica vs diferencias finitas:** `fsolve` estima la Jacobiana por diferencias finitas por defecto. Si el modelo tiene derivadas analíticas disponibles, pasarlas con `fprime=jacobian` acelera la convergencia y mejora la robustez con parámetros mal escalados.

## 5 — Múltiples soluciones: bifurcación en red débil

En sistemas de potencia AC, la ecuación de flujo de potencia \( P = V \cdot I \cdot \cos\phi \) puede tener dos soluciones reales (o ninguna) dependiendo del SCR de la red y de la potencia demandada:

**Curva P-V:** para un convertidor inyectando potencia \( P \) en una red con impedancia \( Z_g = R_g + jX_g \), la tensión en el PCC \( V_{PCC} \) sigue la curva P-V. Para \( P < P_{max} \) hay dos soluciones:
- **Punto de operación estable (alto voltaje):** el convertidor opera en la parte superior de la curva. Perturbaciones pequeñas se atenúan.
- **Punto inestable (bajo voltaje):** la tensión es baja y el sistema no puede mantener el equilibrio con una perturbación.

En SCR bajo (red débil), \( P_{max} \) es pequeño y la bifurcación ocurre a potencias de operación normales. El `fsolve` con diferentes inicializaciones \( \mathbf{x}_0 \) converge a uno u otro punto:

$$ P_{max} = \frac{V_g^2}{2\,Z_g}\left(1 + \cos(2\phi_{Zg})\right)^{1/2} $$

Solo el punto de alto voltaje es estable (los autovalores del Jacobiano del sistema dinámico tienen parte real negativa). El análisis modal ([[analisis-modal]]) confirma cuál es estable.

## 6 — Buenas prácticas: barrido del punto inicial y validación

**Barrido del punto inicial:** cuando no se conoce si el sistema tiene múltiples equilibrios, barrer \( \mathbf{x}_0 \) en una malla de valores plausibles y coleccionar todas las soluciones distintas que `fsolve` encuentra:

```python
equilibrios = set()
for P_guess in np.linspace(0.1, 1.5, 10):
    x0 = construir_x0(P_guess)
    xe = fsolve(f_eq, x0, xtol=1e-12)
    if np.linalg.norm(f_eq(xe)) < 1e-6:
        # redondear para identificar soluciones únicas
        key = tuple(np.round(xe, 4))
        equilibrios.add(key)
```

**Verificar condicionamiento del Jacobiano:** un número de condición \( \kappa(J) > 10^{10} \) indica que el sistema está mal condicionado en ese punto y que la solución puede ser espuria o inestable:

```python
from scipy.linalg import cond
J_num = info['fjac']  # Jacobiana estimada por fsolve
print(f"Condición de J: {cond(J_num):.2e}")
```

**Comparar con solución analítica:** cuando existe, la solución analítica del régimen permanente (p.ej. las expresiones de \( i_d, i_q \) en régimen para un PI) es la referencia para verificar que `fsolve` ha encontrado el equilibrio físico correcto y no un artefacto numérico.

<div class="cfig"><img src="../figuras/equilibrio-fsolve-analisis.png" alt="convergencia Newton-Raphson, curva P-V con dos equilibrios, sensibilidad al punto inicial y error vs iteración"><div class="cap">Newton-Raphson: convergencia cuadrática del residuo. Curva P-V en red débil con dos puntos de equilibrio (solo el de alto voltaje es estable). Sensibilidad al punto inicial: distintas inicializaciones convergen a distintas raíces. Comparativa de convergencia entre Newton-Raphson, bisección y secante.</div></div>

## 7 — Equilibrio del convertidor GFM: ecuaciones y solucion numerica

Para un convertidor GFM con control droop de potencia, el sistema en regimen permanente debe satisfacer las siguientes ecuaciones (en el marco dq sincronizado con la tension del terminal del convertidor):

**Ecuaciones del filtro LCL en regimen:**

$$ 0 = v_{di} - R_1 i_{d1} + \omega_0 L_1 i_{q1} - v_{Cd} $$
$$ 0 = v_{qi} - R_1 i_{q1} - \omega_0 L_1 i_{d1} - v_{Cq} $$
$$ 0 = i_{d1} - i_{d2} + \omega_0 C_f v_{Cq} $$
$$ 0 = i_{q1} - i_{q2} - \omega_0 C_f v_{Cd} $$

**Ecuaciones de la red:**

$$ 0 = v_{Cd} - R_g i_{d2} + \omega_0 L_g i_{q2} - V_{gd} $$
$$ 0 = v_{Cq} - R_g i_{q2} - \omega_0 L_g i_{d2} - V_{gq} $$

**Ecuaciones del droop:**

$$ 0 = \delta - \delta_{ref} - m_P (P - P^*) $$
$$ P = \frac{3}{2}(v_{Cd} i_{d2} + v_{Cq} i_{q2}) $$

Este sistema de 8 ecuaciones en las 8 incognitas \( (i_{d1}, i_{q1}, v_{Cd}, v_{Cq}, i_{d2}, i_{q2}, \delta, P) \) se resuelve con `fsolve`:

```python
from scipy.optimize import fsolve
import numpy as np

def f_equilibrio_gfm(x, params):
    """Campo vectorial del GFM en regimen permanente. x = [id1,iq1,vCd,vCq,id2,iq2,delta,P]."""
    id1, iq1, vCd, vCq, id2, iq2, delta, P = x
    R1, L1, Cf, R2, L2, Rg, Lg = params['R1'], params['L1'], params['Cf'], \
                                    params['R2'], params['L2'], params['Rg'], params['Lg']
    w0, Vdc, mP, Pstar = params['w0'], params['Vdc'], params['mP'], params['Pstar']
    Vgd, Vgq = params['Vgd'], params['Vgq']

    # tension del inversor: modulacion en dq
    vid = Vdc / 2  # simplificado (modulacion lineal)
    viq = 0.0

    eq = [
        vid - R1*id1 + w0*L1*iq1 - vCd,              # LCL d
        viq - R1*iq1 - w0*L1*id1 - vCq,              # LCL q
        id1 - id2 + w0*Cf*vCq,                         # condensador d
        iq1 - iq2 - w0*Cf*vCd,                         # condensador q
        vCd - Rg*id2 + w0*Lg*iq2 - Vgd,              # red d
        vCq - Rg*iq2 - w0*Lg*id2 - Vgq,              # red q
        delta - 0.0 - mP*(P - Pstar),                  # droop: delta_ref = 0
        P - 1.5*(vCd*id2 + vCq*iq2),                  # potencia activa
    ]
    return eq

params = {
    'R1': 0.05, 'L1': 2e-3, 'Cf': 20e-6,
    'R2': 0.02, 'L2': 1e-3,
    'Rg': 0.1, 'Lg': 5e-3,
    'w0': 2*np.pi*50, 'Vdc': 650, 'mP': 0.05,
    'Pstar': 5000.0, 'Vgd': 325.0, 'Vgq': 0.0
}

# Estimacion inicial fisica
Vg = 325.0; P_est = 5000.0
x0 = [P_est / (1.5*Vg), 0.0, Vg, 0.0, P_est/(1.5*Vg), 0.0, 0.01, P_est]

xe, info, ier, msg = fsolve(f_equilibrio_gfm, x0, args=(params,), full_output=True)
res = np.linalg.norm(f_equilibrio_gfm(xe, params))
print(f"Convergido: {ier==1}, residuo: {res:.2e}")
id1e, iq1e, vCde, vCqe, id2e, iq2e, delta_e, P_e = xe
print(f"P_eq = {P_e:.1f} W, delta = {np.degrees(delta_e):.2f} deg")
print(f"id2 = {id2e:.3f} A, iq2 = {iq2e:.3f} A")
```

## 8 — Validacion del equilibrio: comparacion con la solucion analitica

Para el caso simplificado con \( R_1 = R_g = 0 \) (inductancias puras), la solucion analitica del flujo de potencia es:

$$ P = \frac{V_i V_g}{X_{total}} \sin\delta, \quad Q = \frac{V_i^2 - V_i V_g \cos\delta}{X_{total}} $$

donde \( X_{total} = \omega_0(L_1 + L_2 + L_g) \). Para \( P^* = 5\,\text{kW} \), \( V_i = V_g = 325\,\text{V} \):

$$ \sin\delta = \frac{P \cdot X_{total}}{V_g^2} = \frac{5000 \times 0.628}{325^2} = 0.030 \Rightarrow \delta = 1.7° $$

La solucion numerica de `fsolve` deberia dar un angulo de potencia \( \delta \approx 1.7° \pm 0.5° \) (la diferencia es por las resistencias no nulas). Si la discrepancia es mayor, hay un error en la implementacion de las ecuaciones o en la inicializacion.

$$ \boxed{\text{Criterio de validacion}: |\delta_{fsolve} - \delta_{analitico}| < 0.5°;\quad \|f(x_e)\| < 10^{-8}} $$
