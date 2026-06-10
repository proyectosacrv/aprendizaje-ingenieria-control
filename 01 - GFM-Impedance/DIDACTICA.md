# Guía didáctica — Modelado, control y estabilidad de un inversor grid-forming

Este documento explica **cómo** se construyó el proyecto, **por qué** cada decisión, y
sobre todo **el proceso de iteración** que llevó de un diseño inestable a uno robusto.
Está pensado para leerse junto al código. No es la teoría de un libro: es el razonamiento
de ingeniería aplicado, con los tropiezos incluidos (que es donde más se aprende).

Índice:
- [A. Cómo se construye el modelo](#a-cómo-se-construye-el-modelo)
- [B. El sistema físico](#b-el-sistema-físico)
- [C. Estrategias de control](#c-estrategias-de-control)
- [D. El proceso de iteración (lo importante)](#d-el-proceso-de-iteración)
- [E. Impedancia y estabilidad en red](#e-impedancia-y-estabilidad-en-red)
- [F. Cómo correr todo](#f-cómo-correr-todo)

---

## A. Cómo se construye el modelo

### A.1 Por qué un modelo no lineal + linealización numérica

Hay dos formas de obtener el modelo de pequeña señal (`A,B,C,D`):

1. **Derivar A,B,C,D a mano** (state-space averaging analítico). Exacto pero propenso a
   errores algebraicos, y cada cambio de control obliga a rehacer el álgebra.
2. **Modelo no lineal `f(x,u)` + linealización numérica** (Jacobiano por diferencias
   finitas). Escribes solo las ecuaciones físicas; el ordenador deriva. Escala a
   cualquier no linealidad (VSM, saturación, impedancia virtual) sin reescribir álgebra.

Elegimos la 2 (ver [model.py](model.py)). Es el enfoque profesional cuando el sistema es
complejo. El precio: necesitas resolver el **punto de equilibrio** numéricamente antes de
linealizar.

```
f(x,u) ──fsolve──> x_eq  ──Jacobiano numérico──> A,B,C,D
```

### A.2 Los dos marcos de referencia (la clave conceptual del grid-forming)

Un grid-forming **genera** su propia frecuencia y ángulo; no los toma de una PLL. Por eso
necesitamos distinguir dos marcos giratorios dq:

- **Marco `s` (sistema/red):** gira a `w0` constante. Es la referencia común. Aquí se
  define el puerto con la red y se expresa la impedancia.
- **Marco `c` (control):** gira a `w`, la frecuencia que **fija el droop**. El inversor
  vive en este marco.
- `delta = theta_c - theta_s` es el ángulo entre ambos, y `ddelta/dt = w - w0`.

La pequeña señal de `delta` es **lo que acopla** la dinámica de potencia con la eléctrica.
Una tensión de red fija en `s` se ve **rotada** por `delta` desde `c`:
`v_pcc_c = R(-delta) · v_pcc_s`. Este término de rotación es el corazón del modelo y
fuente de la mayoría de los acoplamientos sutiles.

### A.3 De dónde sale cada ecuación (los 15 estados)

| Estados | Física | Ecuación |
|---|---|---|
| `iL1d,iL1q` | inductor lado inversor | `L1 di/dt = v_inv - v_C - R1·i + jωL1·i` |
| `vcd,vcq` | condensador de filtro | `Cf dv/dt = iL1 - iL2 + jωCf·v` |
| `iL2d,iL2q` | inductor lado red | `L2 di/dt = v_C - v_pcc - R2·i + jωL2·i` |
| `delta` | ángulo de control | `ddelta/dt = w - w0` |
| `Pm,Qm` | potencia filtrada | `dPm/dt = wf·(P - Pm)` |
| `xvd,xvq` | integradores PI tensión | `dx/dt = error_v` |
| `xid,xiq` | integradores PI corriente | `dx/dt = error_i` |
| `iL2d_lp,iL2q_lp` | filtro de la R virtual transitoria | `dx/dt = wht·(iL2 - x)` |

El término `jω·(·)` representa el acoplamiento cruzado d↔q que aparece al derivar en un
marco giratorio (`d/dt(R(θ)x)`). Es el origen de los términos de desacoplo del control.

### A.4 Validación del modelo (siempre)

Antes de confiar en un modelo, comprobar:
- **Equilibrio coherente:** residual ≈ 1e-10, y `P_eq = Pset`, `|vc| ≈ nominal`.
- **Signo de sensibilidades físicas:** medimos `∂P/∂δ = +127 kW/rad` (positivo, correcto:
  más ángulo → más potencia inyectada en línea inductiva).
- **Autovalores plausibles:** la resonancia LCL aparece donde la teoría dice
  (`f = 1/2π·√((L1+L2)/(L1·L2·Cf)) ≈ 1.1 kHz`).

Si estas tres cosas cuadran, el modelo es fiable.

---

## B. El sistema físico

### B.1 El filtro LCL

El inversor conmuta a alta frecuencia; el filtro LCL (`L1-Cf-L2`) atenúa los armónicos de
conmutación. Su pega: una **resonancia** aguda (~1.1 kHz aquí) con amortiguamiento
natural casi nulo (ζ≈0). Sin tratar, esa resonancia hace inestable cualquier lazo rápido.
Solución: **amortiguamiento activo** (ver C.2).

### B.2 Grid-forming vs grid-following (la distinción fundamental)

- **Grid-following (GFL):** mide el ángulo de red con una PLL y **inyecta corriente**. Se
  comporta como fuente de corriente. Pierde estabilidad en **red débil** (SCR bajo).
- **Grid-forming (GFM):** **impone tensión** con su propia frecuencia (droop/VSM). Se
  comporta como fuente de tensión detrás de una impedancia. Es robusto en red débil y, si
  el control es agresivo, puede tener problemas en red **fuerte** (lo veremos en E).

Este proyecto es GFM. La firma de impedancia lo confirma: **inductiva** en banda media
(fase +47°…+59°), como una máquina síncrona (ver [main_phase2.py](main_phase2.py)).

### B.3 Impedancia virtual (la pieza que faltaba)

Un GFM con reactancia de acoplamiento pequeña tiene ganancia `∂P/∂δ = 1.5·V²/X` enorme →
el lazo de potencia se vuelve difícil de estabilizar. La **impedancia virtual**
`Zv = Rv + jXv` emula impedancia adicional **restándola de la referencia de tensión**:

```
v_C_ref = V_ref - (Rv·iL2 + jXv·iL2)
```

Ventajas frente a poner inductancia física:
- No añade un polo lento de planta (es algebraica sobre la referencia).
- La parte **inductiva** (`Xv`) baja `∂P/∂δ` sin caída resistiva → estabiliza el lazo de
  potencia **sin** distorsionar el equilibrio (la caída inductiva cae en el eje q, que el
  control mantiene en 0).
- La parte **resistiva** (`Rv`) amortigua, pero su caída cae en el eje d y **pelea con el
  droop Q-V** → dispara `Q_eq`. Por eso usamos poca `Rv` estática y la complementamos con
  **resistencia virtual transitoria** (D.5).

---

## C. Estrategias de control

### C.1 Lazos en cascada (la arquitectura)

```
 droop P/Q ─> v_C_ref ─> [PI tensión] ─> iL1_ref ─> [PI corriente] ─> v_inv
              (lento)       (medio)                    (rápido)
```

Regla de oro: cada lazo interno debe ser **más rápido** que el externo. Aquí: corriente
~1 kHz, tensión ~350 Hz, potencia/droop ~3 Hz. El **desacoplo** (`±jωL`, `±jωCf`) cancela
el acoplamiento d↔q para que cada eje se controle por separado.

### C.2 Amortiguamiento activo del LCL

Realimentamos la corriente del condensador (`iL1 - iL2`) a la tensión de puente con
ganancia `Kad`. Equivale a una **resistencia virtual en serie** que amortigua la
resonancia LCL sin pérdidas reales. Imprescindible para poder subir el lazo de tensión.

### C.3 Droop vs VSM (dos formas de fijar la frecuencia)

- **Droop P-f:** `w = w0 + mp·(Pset - P)`. Frecuencia **algebraica**: responde
  instantáneamente. Sin inercia.
- **VSM (Virtual Synchronous Machine):** ecuación de swing
  `J·dω/dt = (Pset - P)/w0 - D·(ω - w0)`. Frecuencia es un **estado** con **inercia** `J`
  y amortiguamiento `D`. Emula una máquina síncrona real.

En [main_phase5.py](main_phase5.py) (figura `fase5_inercia.png`) se ve la diferencia ante
un escalón de carga: el droop deja saltar la frecuencia de golpe; el VSM la mueve
**suavemente** (RoCoF limitado por `J`). El VSM da control directo del amortiguamiento del
modo de potencia, que en droop puro es difícil de mejorar (ver D.4).

### C.4 Current limiting bajo falta

Un GFM es fuente de tensión: ante un hueco de red inyecta corriente enorme (medimos
**4.76 pu** sin protección — destruiría los semiconductores). El **current limiting**
satura la magnitud de `iL1_ref` a `Imax` y congela los integradores (anti-windup). Con él,
la corriente de falta queda en **1.51 pu** (figura `fase5_falta.png`). Es uno de los retos
abiertos reales del grid-forming: limitar corriente **sin** perder el carácter formador.

---

## D. El proceso de iteración

Esta es la parte más valiosa. El primer diseño salió **inestable**. Lo importante no es el
diseño final, sino **cómo se diagnostica y se corrige** una inestabilidad. Toda la
cronología real está abajo.

### D.1 La caja de herramientas de diagnóstico

| Herramienta | Para qué | Dónde |
|---|---|---|
| **Mapa de polos** | ¿estable? ¿qué modos hay y a qué frecuencia? | `main_phase1.py` |
| **Factores de participación** | ¿qué estados forman el modo inestable? | autovectores de A |
| **Barridos de parámetros** | ¿es sensible a la ganancia (ajuste) o no (estructura)? | `diag_sweep.py` |
| **Aislamiento de lazos** | apagar un lazo (droop=0, ff=0) para ver quién causa qué | flags en `model.py` |
| **Medición de sensibilidades** | medir `∂P/∂δ` directamente para verificar signos | numérico |
| **Bode / margen de fase** | margen del lazo abierto, frecuencia de cruce | `control.margin` |

### D.2 El principio guía: ganancia vs estructura

> Si reducir mucho una ganancia (×20) **no** estabiliza, el problema **no es ajuste**: es
> estructural (signo, acoplamiento, realimentación positiva).

Este principio dirigió todo el debugging. Cada vez que un barrido mostraba insensibilidad
a la ganancia, dejábamos de "afinar números" y buscábamos un error estructural.

### D.3 Cronología real del debugging (resumida)

1. **Primer diseño → INESTABLE** (+37, modo a 6 Hz, ζ=−0.71). Participación: dominado por
   `Pm, Qm` → lazo de potencia.
2. **Barridos de droop y filtro:** nada estabiliza, y subir el lazo de tensión **empeora**.
   → No es ajuste. Es estructural.
3. **Aislamiento:** con droops=0 pero **feedforward de carga activo**, max Re=+14. ¡El
   feedforward de carga es inestable **por sí solo**! → Eliminado. Cae a +1.26.
4. **Sigue marginalmente inestable** (+1.26, modo Q a 0.4 Hz). Insensible al droop Q
   (×5 → apenas cambia). → Otra vez estructural.
5. **Medimos `∂P/∂δ` = +127 kW/rad** (positivo, correcto). El modelo reducido 2×2 predice
   estabilidad, pero el sistema real no. → La inestabilidad está en la **fase dinámica**,
   no en la ganancia DC.
6. **Bode del lazo de potencia abierto:** margen de fase **−86°**. Confirmado: el lazo de
   potencia cruza con fase insuficiente.
7. **Diagnóstico físico:** la reactancia de acoplamiento es minúscula → `∂P/∂δ` enorme →
   margen negativo. La cura canónica es **impedancia virtual**.
8. **Inductancia virtual alta (Xv≈0.16 pu):** estabiliza bajando `∂P/∂δ`, **sin** disparar
   `Q_eq` (la `Rv` resistiva sí lo disparaba: lección sobre por qué resistiva ≠ inductiva).
9. **Amortiguamiento:** el modo de potencia quedaba con ζ=0.17. La **resistencia virtual
   transitoria** (high-pass, cero en DC) sube ζ a **0.40** sin tocar el equilibrio.

Resultado: estable, `max Re=−8.3`, modo de potencia a 3.3 Hz con ζ=0.40, equilibrio
físico correcto (`P=5 kW`, `Q=−554 var`, `|vc|≈nominal`).

### D.4 Lecciones transferibles

- **El feedforward "que mejora el rechazo" puede desestabilizar.** Verifícalo siempre en
  lazo cerrado, no asumas que ayuda.
- **Resistiva ≠ inductiva.** La impedancia virtual inductiva baja la ganancia del lazo de
  potencia; la resistiva amortigua pero interfiere con el droop Q-V en DC.
- **Ganancia DC correcta ≠ estable.** Un signo DC bueno (`∂P/∂δ>0`) no garantiza nada; la
  estabilidad la decide la **fase a la frecuencia de cruce** (por eso el Bode).
- **El droop tiene amortiguamiento limitado** del modo de potencia. Si necesitas más,
  el VSM (con `D` explícito) o trucos transitorios son el camino.

### D.5 La resistencia virtual transitoria (ejemplo de diseño elegante)

Problema: queremos el amortiguamiento de `Rv` sin su efecto en DC (que dispara `Q_eq`).
Solución: aplicar `Rv` solo a la **componente transitoria** de la corriente, vía un
filtro paso-alto (`iL2 - iL2_filtrada`). En DC, transitorio=0 → no afecta el equilibrio;
en transitorios, amortigua. Detalle fino descubierto en el barrido: el corte del HPF debe
estar **por debajo** del modo a amortiguar (si no, lo atenúa).

---

## E. Impedancia y estabilidad en red

### E.1 Por qué el enfoque de impedancia

Para estudiar la interacción inversor-red sin reconstruir todo el sistema cada vez, se
modela cada lado como una impedancia:
- Inversor: **admitancia de salida** `Y_inv(s)` (2×2 en dq), de su modelo linealizado.
- Red: **impedancia** `Z_grid(s) = Rg + jωLg`, parametrizada por **SCR** y **X/R**.

La estabilidad del conjunto se decide por el **minor loop gain** `L(s) = Z_grid·Y_inv`,
aplicando el **criterio de Nyquist generalizado** (los autovalores de `L(jω)` no deben
rodear −1). Es la herramienta estándar para integración masiva de inversores y
oscilaciones subsíncronas.

### E.2 Validación cruzada (la prueba de que el método es correcto)

Hicimos lo mismo por dos caminos independientes y comparamos:
- **(A)** Autovalores del **modelo acoplado** inversor+red (la "verdad").
- **(B)** Criterio de **impedancia** (Nyquist de `Z_grid·Y_inv`).

Resultado (control agresivo, X/R=5): **SCR crítico = 3.35 (A) vs 3.39 (B)**, diferencia
1.3 %. Ambos coinciden → el método de impedancia es fiable. Ver
[main_phase3.py](main_phase3.py) y `nyquist_fase3.png`.

### E.3 El resultado físico interesante

El GFM bien amortiguado es **estable en todo el rango de SCR** (red débil → fuerte). Solo
forzando un control **agresivo** (droop alto, sin amortiguamiento) aparece un SCR crítico,
y es en red **fuerte** (SCR>3.3), no débil. Esto es lo **opuesto** al grid-following, y es
una de las razones por las que el grid-forming es clave para redes con alta penetración
renovable.

### E.4 Medir la impedancia por inyección (Fase 4 — el método de PLECS/hardware)

El `Z_dq(s)` analítico (Fase 2) viene de la linealización. ¿Cómo se mide en una planta real
(o en PLECS, o en un banco)? Por **inyección de perturbación** ([inject.py](inject.py)):

1. En el punto de operación, inyectar una pequeña tensión senoidal a frecuencia `f_p`.
2. Como es un sistema **MIMO 2×2** (ejes d,q acoplados), hacen falta **dos** inyecciones
   independientes (una en d, otra en q) para identificar la matriz completa.
3. Demodular (correlación con sin/cos sobre periodos enteros) para extraer los fasores de
   `v_pcc` e `i_g` a `f_p`.
4. Montar `I = G·V` con las dos columnas → `G = I·V⁻¹`, `Y = -G`, `Z = Y⁻¹`.

Aplicado sobre el modelo no lineal (la "planta"), el `Z` medido coincide con el analítico:
**error medio 0.21 %** ([main_phase4.py](main_phase4.py)). Esto valida la linealización y,
sobre todo, enseña el procedimiento **idéntico** al que se programa en PLECS o en hardware.

**Régimen de validez:** la impedancia lineal solo describe **pequeña señal**. Mientras no se
active una no linealidad fuerte, el `Z` medido es independiente de la amplitud de la
perturbación (lo comprobamos en `main_phase4.py` barriendo la amplitud: el error se mantiene
plano). Cuando entra en juego una saturación —típicamente el **current limiting**— el
concepto de impedancia lineal deja de aplicar: la respuesta se distorsiona y ya no es
proporcional a la perturbación. Ese régimen es de **gran señal** y se estudia por simulación
temporal (Fase 5, current limiting bajo falta), no por impedancia. Lección: el análisis de
impedancia/estabilidad lineal vale hasta que una protección o saturación entra en juego.

### E.5 Por qué vale el modelo promediado (Fase 4b)

Todo el proyecto usa el modelo **promediado** (tensión de puente continua). ¿Es legítimo?
[switched.py](switched.py) lo comprueba: compara la tensión real **conmutada** (PWM a 10
kHz) con la **promediada**. El rizado de conmutación en `v_C` es ~2.5 %, y la diferencia
RMS entre conmutado y promediado es **0.67 %**. El filtro LCL atenúa el rizado; la dinámica
de baja frecuencia (la que controla el grid-forming) es idéntica. Por eso se diseña con el
promediado y se valida con el conmutado.

---

## F. Cómo correr todo

```bash
python main_phase1.py    # equilibrio, polos, mapa de polos        -> results/polos_fase1.png
python main_phase2.py    # impedancia de salida dq Z(jw)           -> results/impedancia_fase2.png
python main_phase3.py    # estabilidad red debil, Nyquist          -> results/nyquist_fase3.png
python main_phase4.py    # validacion Z por inyeccion              -> results/fase4_validacion.png
python switched.py       # principio de promediado (PWM)           -> results/fase4b_averaging.png
python main_phase5.py    # droop vs VSM, current limiting          -> results/fase5_*.png
python diag_sweep.py     # barrido de diagnostico de estabilidad
```

Archivos núcleo: [params.py](params.py) (parámetros), [model.py](model.py) (modelo +
equilibrio + linealización), [impedance.py](impedance.py) (Y/Z dq), [grid.py](grid.py)
(red Thévenin), [simulate.py](simulate.py) (simulación temporal no lineal),
[inject.py](inject.py) (medición de impedancia).

### Validación en PLECS (modelo conmutado)
La Fase 4 en Python valida la linealización (inyección) y el promediado (PWM). El cierre
final del flujo es montar el modelo **conmutado** en PLECS y repetir la medición de
impedancia y el barrido de SCR sobre la planta realista. La guía completa (esquemático,
control, inyección, co-simulación XML-RPC) está en [PLECS_GUIA.md](PLECS_GUIA.md) y
[plecs_cosim.py](plecs_cosim.py).
```
Python (modelo promediado, diseño) <──valida──> PLECS (conmutado, realidad)
```
