---
titulo: Barrido paramétrico y sensibilidad numérica
slug: barrido-parametrico
categoria: programacion
tipo: tecnica
nivel: intermedio
proyectos: []
objetivos: [evaluar cómo cambian polos y márgenes al variar parámetros del sistema]
tags: [barrido, sweep, sensibilidad, autovalores, robustez, intermedio, programacion]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-30
relacionados: [robustez-parametrica, respuesta-frecuencia-ss, analisis-modal, margenes-estabilidad, red-thevenin-scr]
referencias:
  - "Skogestad, Postlethwaite, Multivariable Feedback Control, Wiley 2005"
  - "Saltelli et al., Global Sensitivity Analysis, Wiley 2008"
---

## Definición
Procedimiento numérico que **recalcula indicadores de estabilidad/desempeño** (autovalores,
márgenes, pico de sensibilidad \( M_s \)) mientras se **varía uno o varios parámetros** del modelo,
para localizar el caso crítico y cuantificar la robustez. Es la implementación práctica de la
[[robustez-parametrica]].

## Fundamento teórico
Dado el modelo \( A(\theta) \) (o \( L(s;\theta) \)) función de un parámetro \( \theta \) (SCR de
red, \( L \), \( C \), ganancia, retardo):
- **Barrido 1-D:** se recorre \( \theta\in[\theta_{min},\theta_{max}] \) y se calculan
  \( \lambda_i(\theta)=\mathrm{eig}\,A(\theta) \) → **root-loci numérico** (trayectoria de polos).
- **Barrido 2-D:** dos parámetros → **mapa de calor** de \( \max\mathrm{Re}\,\lambda \) o de
  \( M_s \); la curva \( \max\mathrm{Re}\,\lambda=0 \) es la **frontera de estabilidad**.
- **Sensibilidad local:** \( \partial\lambda_i/\partial\theta \) (vía autovectores derecho/izquierdo
  \( w_i,v_i \)): \( \dfrac{\partial\lambda_i}{\partial\theta}=\dfrac{w_i^\top (\partial A/\partial\theta)\,v_i}{w_i^\top v_i} \),
  que indica qué parámetro mueve más cada modo (enlaza con el [[analisis-modal|análisis modal]]).

Para muchos parámetros a la vez, el barrido en rejilla escala mal (maldición de la dimensión) → se
usa muestreo (Latin Hypercube, Monte Carlo) o análisis de sensibilidad global (Sobol).

<div class="cfig"><img src="figuras/barrido-parametrico-mapa.png" alt="mapa de calor 2D de max Re lambda frente a SCR y ancho de banda de PLL"><div class="cap">Barrido 2-D: para cada combinación de SCR y ancho de banda de la PLL se recalcula $\max\mathrm{Re}(\lambda)$ del modelo. El mapa de calor revela la región inestable (rojo) y la línea negra $\max\mathrm{Re}(\lambda)=0$ es la frontera de estabilidad. Una PLL más rápida desplaza la frontera hacia SCR mayores, reduciendo el margen en red débil.</div></div>

## 1 — Cómo se barre un parámetro y se traza el polo dominante
**Paso 1 — parametrizar la matriz de estado.** Se escribe el modelo de pequeña señal como \( \dot x=A(\theta)\,x \), donde \( \theta \) es el parámetro físico que se quiere variar (aquí el SCR de red). La dependencia entra por la inductancia de red: con \( L_g=1/(\mathrm{SCR}\cdot\omega_0) \), cada valor de \( \theta=\mathrm{SCR} \) produce una matriz \( A(\theta) \) distinta porque \( L_g \) aparece en las filas del inductor de red.

**Paso 2 — definir la rejilla.** Se elige el rango \( [\theta_{min},\theta_{max}] \) y un número de puntos. Si el rango abarca varios órdenes (SCR de 1 a 20), se usa espaciado logarítmico para no malgastar puntos en el extremo alto:

$$ \theta_k = \theta_{min}\left(\frac{\theta_{max}}{\theta_{min}}\right)^{k/(N-1)},\qquad k=0,\dots,N-1 $$

**Paso 3 — autovalores en cada punto.** Para cada \( \theta_k \) se resuelve el problema de autovalores \( \det\!\big(A(\theta_k)-\lambda I\big)=0 \), obteniendo el espectro \( \{\lambda_i(\theta_k)\} \). Los polos del sistema lineal son exactamente esos autovalores.

**Paso 4 — extraer el indicador escalar.** De cada espectro se condensa un único número: la **abscisa espectral**, la parte real más a la derecha, que decide la estabilidad:

$$ \alpha(\theta_k)=\max_i \operatorname{Re}\lambda_i(\theta_k) $$

El sistema es estable en \( \theta_k \) si y solo si \( \alpha(\theta_k)<0 \). El autovalor que alcanza ese máximo es el **modo dominante** (el más lento en amortiguarse, o el que primero se desestabiliza).

**Paso 5 — localizar la frontera.** Se busca el cruce \( \alpha(\theta)=0 \). Numéricamente es el primer \( k \) en que \( \alpha \) cambia de signo; el \( \theta \) crítico se afina por interpolación lineal entre \( \theta_{k-1} \) y \( \theta_k \):

$$ \boxed{\;\theta_{crit}\approx\theta_{k-1}-\alpha(\theta_{k-1})\,\frac{\theta_k-\theta_{k-1}}{\alpha(\theta_k)-\alpha(\theta_{k-1})}\;} $$

**Paso 6 — interpretar.** Trazar \( \operatorname{Re}\lambda \) (o todo \( \lambda \) en el plano complejo) frente a \( \theta \) da el **root-locus numérico**: la trayectoria del modo dominante. El punto donde cruza el eje imaginario es el límite de estabilidad, y la distancia entre el \( \theta \) nominal y \( \theta_{crit} \) es el **margen de robustez** (en el ejemplo de abajo, SCR nominal frente a \( \mathrm{SCR}_{crit}\approx2.3 \)).

## 2 — Sensibilidad modal: qué parámetro mueve más cada polo
**Paso 1 — derivar la ecuación del autovalor.** Para un autovalor simple \( \lambda_i \) con autovector derecho \( v_i \) (cumple \( A v_i=\lambda_i v_i \)) e izquierdo \( w_i \) (cumple \( w_i^\top A=\lambda_i w_i^\top \)). Se deriva \( A v_i=\lambda_i v_i \) respecto de \( \theta \):

$$ \frac{\partial A}{\partial\theta}v_i + A\frac{\partial v_i}{\partial\theta}=\frac{\partial\lambda_i}{\partial\theta}v_i+\lambda_i\frac{\partial v_i}{\partial\theta} $$

**Paso 2 — proyectar sobre el autovector izquierdo.** Se multiplica por la izquierda por \( w_i^\top \). El término \( w_i^\top A\,\partial_\theta v_i=\lambda_i w_i^\top\partial_\theta v_i \) (porque \( w_i^\top A=\lambda_i w_i^\top \)) se cancela exactamente con \( \lambda_i w_i^\top\partial_\theta v_i \) del otro lado. Queda solo el término del autovector derecho desaparecido:

$$ w_i^\top\frac{\partial A}{\partial\theta}v_i=\frac{\partial\lambda_i}{\partial\theta}\,w_i^\top v_i $$

**Paso 3 — despejar la sensibilidad.** Dividiendo entre el producto \( w_i^\top v_i\neq0 \):

$$ \boxed{\;\frac{\partial\lambda_i}{\partial\theta}=\frac{w_i^\top\,(\partial A/\partial\theta)\,v_i}{w_i^\top v_i}\;} $$

**Paso 4 — leer el resultado.** Es un número complejo: su parte real dice cuánto se desplaza el amortiguamiento del modo \( i \) por unidad de \( \theta \), y su parte imaginaria cuánto cambia su frecuencia. Comparando \( |\partial\lambda_i/\partial\theta| \) entre todos los parámetros se identifica **cuál mueve más** el modo crítico, es decir, dónde actuar para estabilizar. Esta fórmula es de primer orden (válida cerca del punto de evaluación) y enlaza con el [[analisis-modal|análisis modal]]; el barrido completo del apartado 1 es su versión exacta y no lineal.

## Cuándo y por qué se usa
Para hallar el **margen de robustez** ante variación de red/planta (p.ej. estabilidad vs
[[red-thevenin-scr|SCR]]), identificar el parámetro crítico, validar el diseño en el peor caso y
generar las figuras de robustez del informe.

## Procedimiento de diseño (genérico)
1. Parametriza el modelo: \( A(\theta) \) o \( L(s;\theta) \).
2. Define el rango y la rejilla (o el muestreo) de \( \theta \).
3. Para cada valor: calcula autovalores / \( M_s \) / márgenes ([[respuesta-frecuencia-ss]]).
4. Localiza la frontera de estabilidad y el caso peor.
5. Reporta margen (distancia al límite) y, si procede, sensibilidad modal del parámetro dominante.

## Ejemplo de aplicación real
**Problema:** Lazo de corriente de GFL: ¿para qué SCR mínimo el sistema se vuelve inestable con el control diseñado? Barrer SCR de 1 a 20 y trazar la trayectoria del modo más crítico.

Se parametriza \( A(\text{SCR}) \): la inductancia de red varía como \( L_g=1/(\text{SCR}\times\omega_0) \). Para cada valor del barrido (50 puntos log-espaciados de SCR=1 a 20) se calculan los autovalores de \( A \). El modo de la PLL mueve su parte real: a SCR=20 tiene \( \text{Re}(\lambda)\approx-25 \) (estable); a SCR=2.3 cruza a \( \text{Re}(\lambda)=0 \) (frontera de estabilidad). El SCR crítico \( \approx2.3 \) da el margen de robustez: el sistema aguanta una red 2.3 veces más débil que la nominal. Frente al requisito del código de red (SCR>2.0), el margen es del 15 %: ajustado. Reducir el ancho de banda de la PLL desplaza el límite a SCR<1.5.

## Ejemplo de código
```python
import numpy as np
scr = np.linspace(1.0, 10.0, 50)
worst = [np.max(np.real(np.linalg.eigvals(A_of(s)))) for s in scr]
scr_lim = scr[np.argmax(np.array(worst) > 0)]    # primer SCR inestable
```

## Parámetros y valores típicos
Rejilla 1-D: 50–500 puntos (logarítmica si el rango es amplio). Objetivo: estable en todo el rango
esperado con \( M_s<2 \) y margen al límite > 20–30 %.

## Errores comunes
- Rejilla gruesa que **salta** una franja de inestabilidad estrecha.
- Reordenamiento de autovalores entre puntos (el "tracking" de modos requiere emparejar por
  continuidad/autovectores).
- Barrer un solo parámetro cuando el peor caso aparece por **combinación** de varios.

## Conceptos relacionados
- [[robustez-parametrica]] · [[respuesta-frecuencia-ss]] · [[analisis-modal]] · [[margenes-estabilidad]] · [[red-thevenin-scr]]

## Referencias
- Skogestad, Postlethwaite, *Multivariable Feedback Control*, 2005.
- Saltelli et al., *Global Sensitivity Analysis*, 2008.

---

## 3 — Barrido 1D y curvas de sensibilidad

**Procedimiento.** Se elige un parámetro \( p \in [p_{min}, p_{max}] \) con \( N \) puntos logarítmicamente espaciados (si el rango cubre varios órdenes) o linealmente espaciados (si el rango es estrecho). Para cada punto se calculan los indicadores de interés: eigenvalores, margen de fase (PM), ancho de banda (\( \omega_c \)), o pico de sensibilidad \( M_s \).

**Representación.** Curvas del tipo `plt.semilogx(p_arr, PM_arr)` con:
- Zona sombreada verde: región de cumplimiento (\( PM > 45° \))
- Línea roja discontinua: límite del requisito
- Marcador vertical: valor nominal del parámetro

**Detección de bifurcaciones.** Una bifurcación de Hopf ocurre cuando un par de eigenvalores complejos conjugados cruza el eje imaginario: \( \mathrm{Re}(\lambda_i(\theta)) = 0 \) con \( \mathrm{Im}(\lambda_i) \neq 0 \). En el barrido aparece como un cambio de signo en \( \mathrm{Re}(\lambda_{dominante}) \). Una bifurcación de silla-nodo (fold) ocurre cuando un eigenvalue real cruza el origen.

**Regla práctica.** Usar al menos 100 puntos en el barrido para no perder franjas de inestabilidad estrechas (ver sección *Errores comunes*).

<div class="cfig"><img src="../figuras/barrido-parametrico-analisis.png" alt="Barrido paramétrico 1D, 2D y trayectoria de eigenvalores"><div class="cap">Panel superior izquierdo: margen de fase vs Kp con zona verde de cumplimiento. Superior derecho: mapa de estabilidad 2D en el espacio (Kp, Ti). Inferior izquierdo: trayectoria de eigenvalores (verde=estable, rojo=inestable) durante barrido de ganancia. Inferior derecho: respuesta al escalón para distintos Kp.</div></div>

## 4 — Barrido 2D: mapa de estabilidad

**Configuración.** Dos parámetros: \( p_1 \in [a_1, b_1] \) con \( N_1 \) puntos, \( p_2 \in [a_2, b_2] \) con \( N_2 \) puntos. Para cada par \( (p_1^i, p_2^j) \) se calcula la métrica de estabilidad (PM, \( \|S\|_\infty \), \( \max\mathrm{Re}(\lambda) \)) y se almacena en una matriz \( N_2 \times N_1 \).

**Visualización:**

```python
KP, TI = np.meshgrid(Kp_arr, Ti_arr)
PM = calcular_pm(KP, TI)  # vectorizado o con doble bucle
plt.contourf(Kp_arr, Ti_arr, PM, levels=20, cmap='RdYlGn')
plt.contour(Kp_arr, Ti_arr, PM, levels=[45], colors='white', lw=2)  # frontera PM=45°
```

**La línea de nivel \( \max\mathrm{Re}(\lambda)=0 \)** (o \( PM=45° \)) es la frontera de estabilidad: divide el espacio de parámetros en región estable y región inestable.

**Coste computacional.** El barrido 2D tiene coste \( O(N_1 N_2) \) evaluaciones. Para \( N_1 = N_2 = 50 \), son 2500 evaluaciones de eigenvalores. Si cada evaluación tarda \( 1\,\text{ms} \), el total es \( \approx 2.5\,\text{s} \). Para modelos más costosos, paralelizar con `concurrent.futures.ProcessPoolExecutor` o `joblib.Parallel`.

## 5 — Optimización paramétrica del controlador

**Formulación.** El problema de diseño óptimo del controlador puede plantearse como:

$$ \min_{K_p, T_i} \|T(s)\|_\infty \quad \text{sujeto a} \quad PM > 45°, \quad \omega_c > \omega_{min} $$

donde \( T = (I+GC)^{-1}GC \) es la función de transferencia de lazo cerrado.

**Algoritmo de optimización global.** Para evitar mínimos locales, usar `scipy.optimize.differential_evolution`:

```python
from scipy.optimize import differential_evolution
bounds = [(0.1, 100), (0.001, 1)]   # [Kp, Ti]
result = differential_evolution(objetivo, bounds, tol=1e-4, seed=42)
```

**Espacio de búsqueda.** Para un PI de corriente de VSC:
- \( K_p \in [0.1, 100] \): rango de una decade antes y después del valor nominal
- \( T_i \in [0.001, 1]\,\text{s} \): desde control muy agresivo (1 ms) a muy lento (1 s)

**Post-proceso.** Trazar la curva de Pareto entre velocidad de respuesta (\( \omega_c \)) y robustez (\( PM \)) permite elegir el punto de diseño óptimo según el requisito del sistema. Un PM alto suele costar ancho de banda.

## 6 — Barrido en lazo de hardware en el loop (HiL)

**Automatización.** Python puede controlar un simulador en tiempo real (OPAL-RT, Typhoon HiL) vía scripting para lanzar barridos automáticos de parámetros del controlador:
1. Escribir el parámetro \( K_p \) en el registro del simulador.
2. Ejecutar la simulación durante \( T_{sim} \) segundos.
3. Capturar las formas de onda y calcular el PM/sobreoscilación.
4. Repetir para el siguiente punto del barrido.

**Almacenamiento.** Con `h5py`, las matrices de resultados se guardan en formato HDF5, eficiente para lectura/escritura de grandes arrays numéricos:

```python
import h5py
with h5py.File('barrido_kp.h5', 'w') as f:
    f.create_dataset('Kp', data=Kp_arr)
    f.create_dataset('PM', data=PM_arr)
    f.create_dataset('escalones', data=escalones_3D)  # shape: (N_Kp, N_t)
```

**Criterio de parada automático.** Si un punto del barrido produce oscilación sostenida (indicada por \( \max\mathrm{Re}(\lambda) > 0 \) o por la amplitud de las formas de onda superando un umbral), el punto se marca como inestable y el barrido continúa sin interrumpirse. Esto permite mapear toda la frontera de estabilidad, no solo la región segura.

## 7 — Barrido 2D con `contourf` y frontera de estabilidad

El barrido 2D genera un mapa de calor de la métrica de estabilidad en el espacio de dos parámetros. El resultado más útil es la curva de nivel \( \max\mathrm{Re}(\lambda) = 0 \), que define la frontera exacta de estabilidad.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


def build_pi_closedloop(Kp, Ti, G_plant):
    """Construye el sistema en lazo cerrado con PI.
    
    G_plant: instancia de signal.lti (planta)
    Retorna: (max_Re_lambda, PM_deg) o (nan, nan) si hay error
    """
    try:
        # PI: C(s) = Kp*(1 + 1/(Ti*s)) = Kp*(Ti*s+1)/(Ti*s)
        C_num = np.array([Kp*Ti, Kp])
        C_den = np.array([Ti, 0])
        # Lazo abierto L = C*G (convolución de polinomios)
        L_num = np.polymul(C_num, G_plant.num)
        L_den = np.polymul(C_den, G_plant.den)
        # Lazo cerrado: T = L/(1+L) -> den_cl = den_L + num_L
        T_den = np.polyadd(L_den, L_num)
        T_num = L_num
        # Polos del lazo cerrado
        poles_cl = np.roots(T_den)
        max_re = np.max(np.real(poles_cl))
        # Margen de fase
        L_sys = signal.lti(L_num, L_den)
        w_arr = np.logspace(0, 5, 2000)
        _, mag_b, phase_b = signal.bode(L_sys, w=w_arr)
        wc_idx = np.argmin(np.abs(mag_b))
        PM = 180 + phase_b[wc_idx]
        return max_re, PM
    except Exception:
        return np.nan, np.nan


# Parámetros del barrido 2D
Kp_arr = np.linspace(0.5, 30, 40)
Ti_arr = np.linspace(1e-3, 50e-3, 40)

# Planta de primer orden: G(s) = 1/(0.005s + 1)
G_plant = signal.lti([1], [5e-3, 1])

# Matrices de resultados
max_re_map = np.zeros((len(Ti_arr), len(Kp_arr)))
PM_map = np.zeros((len(Ti_arr), len(Kp_arr)))

for i, Ti in enumerate(Ti_arr):
    for j, Kp in enumerate(Kp_arr):
        max_re_map[i, j], PM_map[i, j] = build_pi_closedloop(Kp, Ti, G_plant)

KP, TI = np.meshgrid(Kp_arr, Ti_arr * 1000)   # Ti en ms para el gráfico

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Mapa de max Re(lambda)
ax = axes[0]
cf = ax.contourf(KP, TI, max_re_map, levels=50, cmap='RdYlGn_r')
plt.colorbar(cf, ax=ax, label='max Re(λ)')
cs = ax.contour(KP, TI, max_re_map, levels=[0], colors='white', linewidths=2)
ax.clabel(cs, fmt='Re=0 (frontera)', fontsize=9)
ax.set_xlabel('Kp'); ax.set_ylabel('Ti (ms)')
ax.set_title('Mapa de estabilidad: max Re(λ)')
ax.grid(True, alpha=0.2)

# Mapa de margen de fase
ax = axes[1]
PM_clip = np.clip(PM_map, -10, 90)
cf2 = ax.contourf(KP, TI, PM_clip, levels=50, cmap='RdYlGn')
plt.colorbar(cf2, ax=ax, label='Margen de fase (°)')
cs2 = ax.contour(KP, TI, PM_map, levels=[45], colors='white', linewidths=2)
ax.clabel(cs2, fmt='PM=45°', fontsize=9)
ax.set_xlabel('Kp'); ax.set_ylabel('Ti (ms)')
ax.set_title('Mapa de margen de fase PM (°)')
ax.grid(True, alpha=0.2)

plt.tight_layout()
```

## 8 — Optimización con `scipy.optimize.differential_evolution`

La evolución diferencial (DE) es un algoritmo de optimización global estocástico que no requiere gradientes y evita mínimos locales. Es adecuado para funciones de coste no convexas (como el PM o la norma \( H_\infty \)):

```python
from scipy.optimize import differential_evolution
import numpy as np
from scipy import signal


def objetivo_pm(params, G_plant, target_pm=60.0, w_bw=1000.0):
    """Función de coste: penaliza desviación del PM objetivo y bajo BW.
    
    params: [log10(Kp), log10(Ti)] — se optimiza en escala log
    Retorna: escalar de coste (minimizar)
    """
    Kp = 10**params[0]
    Ti = 10**params[1]

    try:
        C_num = np.array([Kp*Ti, Kp])
        C_den = np.array([Ti, 0])
        L_num = np.polymul(C_num, G_plant.num)
        L_den = np.polymul(C_den, G_plant.den)
        T_den = np.polyadd(L_den, L_num)
        poles_cl = np.roots(T_den)

        # Penalización dura si el sistema es inestable
        if np.any(np.real(poles_cl) > 0):
            return 1e6

        L_sys = signal.lti(L_num, L_den)
        w_arr = np.logspace(0, 5, 1000)
        _, mag_b, phase_b = signal.bode(L_sys, w=w_arr)
        wc_idx = np.argmin(np.abs(mag_b))
        PM = 180 + phase_b[wc_idx]
        wc = w_arr[wc_idx]

        # Coste: desviación de PM objetivo + penalización si BW es bajo
        cost_pm = (PM - target_pm)**2
        cost_bw = max(0, w_bw - wc)**2 * 0.01
        return cost_pm + cost_bw
    except Exception:
        return 1e6


G_plant_opt = signal.lti([1], [5e-3, 1])   # planta de primer orden

# Bounds en escala log10: Kp en [0.1, 100], Ti en [0.0005, 0.1]
bounds_log = [(-1, 2), (-3.3, -1)]

result = differential_evolution(
    objetivo_pm,
    bounds=bounds_log,
    args=(G_plant_opt, 60.0, 1000.0),
    seed=42,
    maxiter=300,
    tol=1e-5,
    popsize=15,
    workers=1   # workers=-1 para paralelizar (requiere pickle-safe)
)

Kp_opt = 10**result.x[0]
Ti_opt = 10**result.x[1]
print(f"Kp óptimo: {Kp_opt:.3f},  Ti óptimo: {Ti_opt*1000:.2f} ms")
print(f"Coste final: {result.fun:.4f},  Converge: {result.success}")

# Verificar PM del resultado
_, pm_final, _ = build_pi_closedloop(Kp_opt, Ti_opt, G_plant_opt)
print(f"PM verificado: {pm_final[1]:.1f}°  (objetivo: 60°)")
```

**Parámetros clave de `differential_evolution`:**
- `bounds`: límites [min, max] de cada parámetro. Usar escala logarítmica para parámetros con rango amplio.
- `popsize`: tamaño de la población = `popsize × len(bounds)`. Más grande → más global pero más lento.
- `seed`: fija la aleatoriedad para reproducibilidad.
- `workers=-1`: paraleliza en todos los núcleos (la función de coste debe ser serializable con pickle).

## 9 — Registro en HDF5 con `h5py`

HDF5 es el formato estándar para almacenar grandes matrices de resultados de barridos. Soporta compresión, metadatos, y lectura parcial sin cargar todo el archivo:

```python
import h5py
import numpy as np
from datetime import datetime


def guardar_barrido_hdf5(filepath, Kp_arr, Ti_arr, max_re_map, PM_map,
                          metadata=None):
    """Guarda los resultados de un barrido 2D en formato HDF5.
    
    filepath   : ruta del archivo .h5
    Kp_arr     : array 1D de valores de Kp
    Ti_arr     : array 1D de valores de Ti
    max_re_map : matriz 2D (len(Ti), len(Kp)) de max Re(lambda)
    PM_map     : matriz 2D de margen de fase [°]
    metadata   : dict con información del barrido (planta, fecha, etc.)
    """
    with h5py.File(filepath, 'w') as f:
        # Ejes del barrido
        f.create_dataset('Kp', data=Kp_arr, compression='gzip')
        f.create_dataset('Ti', data=Ti_arr, compression='gzip')
        # Resultados
        f.create_dataset('max_Re_lambda', data=max_re_map, compression='gzip')
        f.create_dataset('PM_deg', data=PM_map, compression='gzip')
        # Metadatos como atributos del grupo raíz
        f.attrs['fecha'] = datetime.now().isoformat()
        f.attrs['N_Kp'] = len(Kp_arr)
        f.attrs['N_Ti'] = len(Ti_arr)
        if metadata:
            for key, val in metadata.items():
                f.attrs[key] = str(val)
        print(f"Guardado: {filepath}  ({max_re_map.nbytes/1024:.1f} kB de datos)")


def cargar_barrido_hdf5(filepath):
    """Carga los resultados de un barrido desde HDF5."""
    with h5py.File(filepath, 'r') as f:
        Kp = f['Kp'][:]
        Ti = f['Ti'][:]
        max_re = f['max_Re_lambda'][:]
        PM = f['PM_deg'][:]
        meta = dict(f.attrs)
    return Kp, Ti, max_re, PM, meta


# Ejemplo de uso
meta = {'planta': 'G=1/(5ms*s+1)', 'objetivo': 'PM=60deg', 'algoritmo': 'DE'}
guardar_barrido_hdf5('barrido_pi_2d.h5', Kp_arr, Ti_arr, max_re_map, PM_map, meta)

Kp_r, Ti_r, mre_r, pm_r, meta_r = cargar_barrido_hdf5('barrido_pi_2d.h5')
print(f"Barrido cargado: {meta_r['fecha']}")
print(f"Frontera de estabilidad (max Re=0): {np.sum(np.abs(mre_r) < 0.5)} puntos")
```

## 10 — Barrido automático en HiL desde Python

Python puede controlar simuladores en tiempo real (OPAL-RT, Typhoon HiL) mediante su API Python para ejecutar barridos de parámetros automáticamente:

```python
# Pseudocódigo para barrido automático en Typhoon HiL
# API real: from typhoon.api.hil import hil

def barrido_hil(hil_api, params_list, T_sim=2.0, fs_capture=10000):
    """Barrido paramétrico en un simulador HiL.
    
    hil_api    : objeto de la API del simulador (Typhoon, OPAL-RT, etc.)
    params_list: lista de dicts {param_name: value} para cada punto del barrido
    T_sim      : duración de la simulación por punto [s]
    fs_capture : frecuencia de captura [Hz]
    
    Retorna: lista de dicts con métricas por punto
    """
    resultados = []

    for i, params in enumerate(params_list):
        print(f"Punto {i+1}/{len(params_list)}: {params}")

        # 1. Escribir parámetros en el simulador
        for nombre, valor in params.items():
            hil_api.set_scada_input_value(nombre, valor)

        # 2. Iniciar simulación y esperar
        hil_api.start_simulation()
        import time; time.sleep(T_sim)

        # 3. Capturar formas de onda
        v_dc = hil_api.read_analog_signal('Vdc')      # array numpy
        i_ind = hil_api.read_analog_signal('I_inductor')

        # 4. Calcular métricas
        # Sobreoscilación de la tensión tras el escalón de carga
        N_transient = int(0.5 * fs_capture)   # primeros 500 ms = transitorio
        Mp_vdc = (np.max(v_dc[N_transient:]) - np.mean(v_dc[-100:])) / np.mean(v_dc[-100:]) * 100

        # Criterio de estabilidad: amplitud de oscilación en estado estacionario
        v_ss = v_dc[-int(0.5*fs_capture):]
        amplitude_ss = (np.max(v_ss) - np.min(v_ss)) / 2
        is_stable = amplitude_ss < 0.02 * np.mean(v_dc)   # <2% de oscilación

        resultados.append({
            **params,
            'Mp_vdc_%': Mp_vdc,
            'estable': is_stable,
            'amplitud_ss': amplitude_ss
        })

        hil_api.stop_simulation()

    return resultados


# Ejemplo de lista de parámetros para el barrido HiL
params_hil = [
    {'Kp_corriente': Kp, 'Ti_corriente': Ti}
    for Kp in [5, 10, 15, 20]
    for Ti in [2e-3, 5e-3, 10e-3]
]
print(f"Total de puntos a evaluar en HiL: {len(params_hil)}")

# Guardar resultados en HDF5 para análisis posterior
import json
with h5py.File('barrido_hil.h5', 'w') as f:
    Kp_vals = [p['Kp_corriente'] for p in params_hil]
    Ti_vals = [p['Ti_corriente'] for p in params_hil]
    f.create_dataset('Kp', data=Kp_vals)
    f.create_dataset('Ti', data=Ti_vals)
    # Reservar datasets para las métricas (se rellenarán durante el barrido)
    f.create_dataset('Mp_vdc', shape=(len(params_hil),), dtype=float)
    f.create_dataset('estable', shape=(len(params_hil),), dtype=bool)
    f.attrs['descripcion'] = 'Barrido HiL PI corriente VSC'
print("Estructura HDF5 creada para el barrido HiL")
```

**Flujo típico completo:**
1. Barrido 2D offline (sección 7) para mapear la región de interés → identifica los puntos candidatos.
2. Optimización con DE (sección 8) → encuentra el óptimo analítico.
3. Validación en HiL (sección 10) de los candidatos seleccionados → confirma el comportamiento real.
4. Almacenamiento en HDF5 (sección 9) → los resultados son reproducibles y comparables entre campañas.
