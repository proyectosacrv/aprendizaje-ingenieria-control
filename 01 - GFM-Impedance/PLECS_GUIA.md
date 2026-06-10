# Fase 4 en PLECS — modelo conmutado y validación de impedancia (guía completa)

El análisis en Python usa el **modelo promediado** (la tensión del puente es continua). El
modelo **conmutado** de PLECS incluye los IGBTs, el PWM y el rizado de conmutación. Validar
uno contra otro es el flujo estándar del ingeniero de control de convertidores:

```
Python (promediado, diseño y analisis)  <── valida ──>  PLECS (conmutado, "realidad")
```

La impedancia `Z_dq(s)` que calculamos analíticamente (Fase 2, `main_phase2.py`) y medimos
por inyección sobre el modelo no lineal (Fase 4a, `main_phase4.py`) debe coincidir con la
medida sobre el modelo conmutado de PLECS. Si coincide, el modelo promediado queda validado
sobre la planta realista.

> **Archivos de apoyo (ya listos en esta carpeta):**
> - `plecs_control_gfm.c` — el control grid-forming completo, listo para pegar en un bloque
>   C-Script (réplica exacta de `model.py`, discretizada).
> - `plecs_cosim.py` — driver de co-simulación: mide la impedancia en PLECS y la compara
>   automáticamente con la analítica; guarda el CSV y el error.

---

## 0. Resumen del montaje

```
   Vdc=750V ──[Puente 2 niveles, 3 ramas IGBT]── L1,R1 ──┬── L2,R2 ──[PCC]── Lg,Rg ──[red 3~]
                         ▲                                 Cf (Y)
                         │ m_abc (PWM, fsw=10 kHz)         │
                   [bloque PWM] ◄── [C-Script: control GFM] ◄── medidas (vC, iL1, iL2 abc)
```

---

## 1. Esquemático conmutado: etapa de potencia

Usa los mismos valores que [params.py](params.py):

| Bloque PLECS | Valor | Notas |
|---|---|---|
| **DC Voltage Source** | `Vdc = 750 V` | margen para PWM lineal con 400 V LL |
| **IGBT Half Bridge** ×3 | — | un medio puente por fase (a, b, c) |
| **Inductor** `L1` + **Resistor** `R1` | 2 mH, 0.1 Ω | una por fase, lado inversor |
| **Capacitor** `Cf` | 20 µF | conexión en **estrella** (3 condensadores a neutro) |
| **Inductor** `L2` + **Resistor** `R2` | 1 mH, 0.05 Ω | una por fase, lado red |
| **Inductor** `Lg` + **Resistor** `Rg` | desde SCR/X-R | red Thévenin (ver §6); `0` = red rígida |
| **Voltage Source (AC)** 3~ | 230 Vrms fase, 50 Hz | fuente de red ideal detrás de `Lg,Rg` |
| **Voltage/Current Meters** | `v_C`, `i_L1`, `i_L2`, `v_pcc` | para el control y para la impedancia |

Construcción recomendada:
1. Monta una sola fase completa (DC→medio puente→L1→nodo Cf→L2→PCC→Lg→red) y comprueba que
   conduce.
2. Replica a 3 fases. Cf en estrella con neutro flotante o aterrizado según tu convenio.
3. Añade los medidores y agrúpalos en buses de 3 (`Mux`) para llevarlos al control.

---

## 2. Control: bloque C-Script (lo más importante)

Inserta un bloque **C-Script** y configúralo así:

- **Number of inputs:** 1 puerto de ancho **9**, en este orden exacto:
  `[ vCa, vCb, vCc , iL1a, iL1b, iL1c , iL2a, iL2b, iL2c ]` (usa un `Mux`).
- **Number of outputs:** 1 puerto de ancho **3** → `[ ma, mb, mc ]` (modulantes en [-1,1]).
- **Number of states → Discrete:** **9**.
- **Sample time:** `Ts` (p.ej. `1e-4` = 10 kHz). **Debe coincidir** con `TS` del código.

Pega el contenido de [plecs_control_gfm.c](plecs_control_gfm.c) en las pestañas del bloque:
`Code declarations`, `Start function code`, `Output function code`, `Update function code`
(cada sección está marcada en el archivo). El control replica exactamente la cascada de
`model.py`:

1. **Park** de las medidas abc → dq con el ángulo `theta` del propio control
   (grid-forming: el ángulo lo genera el droop, **NO** una PLL).
2. Potencia `P,Q`, filtro de potencia (`WF`), **droop P-f** → `w`, integración `theta`.
3. **Droop Q-V** → `Vref`; **impedancia virtual** `Rv, Lv` y `Rvt` (paso-alto transitorio).
4. **Lazo de tensión** PI (`KP_V, KI_V`) con desacoplo `±wCf`.
5. **Lazo de corriente** PI (`KP_I, KI_I`) con desacoplo `±wL1` y **damping activo** `KAD`.
6. **Current limiting** (satura la magnitud de `iL1*`, con anti-windup) — pon `IMAX = 30.6`
   (1.5 pu) para activarlo; por defecto está desactivado (`1e9`).
7. **Park inverso** → modulantes abc, normalizadas por `Vdc/2`.

Las 3 salidas van al bloque **PWM** (portadora triangular `fsw = 10 kHz`), cuyas señales de
disparo gobiernan los medios puentes.

> **Verificación de signos (importante):** si al arrancar la potencia o la tensión divergen,
> revisa (a) el sentido de las corrientes medidas (`i_L1`, `i_L2` saliendo del inversor),
> (b) el signo del ángulo en Park/Park-inverso, (c) que `Vdc` sea suficiente.

---

## 3. Punto de operación: reproducir la Fase 1 antes de medir

1. Empieza con **red rígida** (`Lg=Rg=0`) y `Vdc` ideal.
2. Simula y comprueba el régimen permanente contra `main_phase1.py`:
   `P ≈ 5 kW`, `Q ≈ −0.55 kvar`, `|v_C| ≈ 326.6 V (pico)`, `δ ≈ 5°`.
3. Si cuadra, el control está bien montado. **Solo entonces** pasa a medir impedancia.

---

## 4. Medir la impedancia en el modelo conmutado

**Vía (a) — Herramienta de PLECS** (`Analysis tools > Impedance`, si tu licencia la incluye):
define el puerto en el PCC y PLECS hace el barrido automáticamente (inyección + extracción).
Es lo más directo; exporta el `Z_dq(jw)` y compáralo con `main_phase2.py`.

**Vía (b) — Inyección + co-simulación** (recomendada, reutiliza nuestro código):
1. Añade una **fuente de tensión de perturbación** en serie en el PCC, parametrizada por
   `f_pert`, `amp_pert`, `axis_d` (inyecta en d si `axis_d=1`, en q si `0`).
2. Expón en la estructura de salida las series **en este orden**:
   `vpcc_d, vpcc_q, ig_d, ig_q` (y `i_L1` si vas a hacer faltas). Usa un bloque `Outport` o
   `To File`. Las dq pueden salir del propio control (ya hace Park) o de un Park auxiliar.
3. Activa el **servidor XML-RPC** en PLECS (Preferences > XML-RPC Interface > Enable, 1080).
4. Ejecuta `python plecs_cosim.py`: inyecta en d y en q a cada frecuencia, demodula
   (correlación, `inject._phasor`), identifica `G=I·V⁻¹`, `Z=(-G)⁻¹`, **compara con la
   analítica** y guarda `datos/impedancia_plecs_vs_analitica.csv` con el error.

Diferencias esperadas al comparar PLECS vs analítica:
- En **banda media** deben solaparse (valida el promediado: error de pocos %).
- Cerca de `fsw/2` aparecen efectos de muestreo/conmutación que el promediado no captura.

---

## 5. Co-simulación Python ↔ PLECS (orquestación)

PLECS ejecuta el modelo conmutado; Python fija parámetros, lanza simulaciones y procesa.
El modelo debe exponer en `Model initialization commands` las variables que Python escribe:
`f_pert, amp_pert, axis_d` (impedancia) y `Lg, Rg` (barrido de SCR).

```
Python: set parametros  ->  PLECS: simula (conmutado)  ->  Python: extrae Z / metricas, compara
```

`plecs_cosim.py` incluye:
- `measure_Z(server, freqs)` — barrido de impedancia (Fase 4 sobre la planta conmutada).
- `compare_with_analytic(...)` — error vs `main_phase2.py`, guarda CSV.
- `sweep_scr(server, scr_list)` — reproduce el barrido de SCR de la **Fase 3** sobre el
  modelo conmutado (p.ej. pico de `i_L1` bajo falta) para confirmar el SCR crítico.

---

## 6. Red Thévenin desde SCR y X/R (igual que en Python)

```
|Zg| = Vll² / (SCR · Sn)     Rg = |Zg| / √(1+(X/R)²)     Lg = Rg·(X/R) / ω0
```
Idéntico a `grid.py`. `plecs_cosim.py` ya calcula `Lg, Rg` a partir del SCR en `sweep_scr`.

---

## 7. Checklist de validación (cierre de la Fase 4)

- [ ] El régimen permanente del conmutado coincide con la Fase 1 (P, Q, |vC|, δ).
- [ ] El rizado de conmutación en `v_C` es ~2.5 % (coincide con `switched.py`).
- [ ] `Z_dq` (PLECS) ≈ `Z_dq` (analítica) en banda media → **promediado validado**.
- [ ] El SCR crítico del barrido conmutado ≈ 3.35 (coincide con la Fase 3).
- [ ] Bajo falta con current limiting, el pico de `i_L1` ≈ 1.5 pu (coincide con la Fase 5).

---

## 8. Problemas frecuentes

| Síntoma | Causa probable | Solución |
|---|---|---|
| Diverge al arrancar | signo de corriente/ángulo, `Vdc` bajo | revisar §2; `Vdc=750` |
| Resonancia LCL no amortiguada | `KAD` mal conectado | realimentar `i_L1−i_L2` con `KAD` |
| `Q_eq` se dispara | `Rv` estática alta | usar `Rv` baja + `Rvt` transitoria |
| XML-RPC no conecta | servidor desactivado/puerto | habilitar interfaz, puerto 1080 |
| `Z` medida ruidosa | ventana no entera de periodos | aumentar tiempo de asentamiento |
| dq de salida desfasadas | Park con ángulo distinto al control | usar el mismo `theta` del C-Script |
```
Python (modelo promediado, diseño) <──valida──> PLECS (conmutado, realidad)
```
