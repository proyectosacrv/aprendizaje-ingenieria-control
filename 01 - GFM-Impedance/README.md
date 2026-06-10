# Grid-forming + estabilidad por impedancia

Proyecto de aprendizaje: modelar un inversor **grid-forming** (droop/VSM) con filtro LCL,
analizar su **impedancia de salida dq**, evaluar estabilidad en **red débil** y simular
su comportamiento dinámico (inercia, faltas). Python = cerebro analítico; PLECS = futura
validación conmutada (Fase 4).

> **Lee primero [DIDACTICA.md](DIDACTICA.md)** — explica el modelado, la física, las
> estrategias de control y, sobre todo, **el proceso de iteración** (cómo se diagnosticó y
> corrigió la inestabilidad inicial). Es el corazón didáctico del proyecto.

## Estado: todas las fases completas (Fase 4 en Python; PLECS documentado)

| Fase | Contenido | Script | Resultado |
|---|---|---|---|
| 1 | Modelo dq (15 estados), equilibrio, linealización, polos | `main_phase1.py` | Estable, modo potencia 3.3 Hz ζ=0.40 |
| 2 | Impedancia de salida `Z_dq(s)` | `main_phase2.py` | Inductiva en banda media (firma GFM) |
| 3 | Red Thévenin + Nyquist generalizado | `main_phase3.py` | SCR crítico 3.35 (acoplado) vs 3.39 (impedancia) |
| 4a | Medición de Z por inyección de perturbación | `main_phase4.py` | Medida vs analítica: error medio 0.21% |
| 4b | Principio de promediado (PWM conmutado vs promediado) | `switched.py` | Diferencia conmutado-promediado 0.67% |
| 4c | Guía PLECS + co-simulación XML-RPC | `PLECS_GUIA.md`, `plecs_cosim.py` | Plantilla lista |
| 5 | Droop vs VSM + current limiting | `main_phase5.py` | Falta: 4.76 pu → 1.51 pu con límite |

## Estructura
- `params.py` — parámetros físicos y de control (notación de ingeniería).
- `model.py` — modelo no lineal dq, equilibrio (`fsolve`), linealización numérica.
- `impedance.py` — admitancia/impedancia de salida `Y(s)`, `Z(s)` en dq.
- `grid.py` — red Thévenin en dq parametrizada por SCR y X/R.
- `simulate.py` — simulación temporal no lineal (droop/VSM, current limiting, faltas).
- `inject.py` — medición de impedancia por inyección de perturbación (Fase 4a).
- `switched.py` — demostración del principio de promediado (PWM, Fase 4b).
- `plecs_cosim.py` — plantilla de co-simulación XML-RPC con PLECS (Fase 4c).
- `main_phase1/2/3/4/5.py` — análisis de cada fase.
- `diag_sweep.py` — barrido de diagnóstico de estabilidad.
- `PLECS_GUIA.md` — guía del modelo conmutado y validación en PLECS.
- `results/` — figuras generadas.

Ejecutar: `python main_phase1.py` (y 2, 3, 4, 5; más `switched.py`).

## Diseño final (estable)
P=5 kW, Q=0, red rígida nominal:
- Equilibrio: P=5000 W, Q=−554 var (~0.06 pu), |vc|≈nominal, δ=5.1°.
- `max Re = −8.3`. Modo de potencia a 3.3 Hz con **ζ=0.40**.
- Resonancia LCL ~1.1 kHz amortiguada por damping activo.

Piezas de control: lazos en cascada (corriente 1 kHz / tensión 350 Hz / droop 3 Hz) +
amortiguamiento activo LCL + impedancia virtual (Xv≈0.16 pu) + resistencia virtual
transitoria (amortiguamiento sin distorsionar el equilibrio).

## Lecciones de diseño (resumen — detalle en DIDACTICA.md)
1. **Feedforward de carga → inestable** por sí solo (+14). Eliminado.
2. **Amortiguamiento activo LCL** imprescindible (resonancia nace con ζ≈0).
3. **Impedancia virtual inductiva** estabiliza el lazo de potencia sin distorsionar `Q_eq`;
   la resistiva amortigua pero pelea con el droop Q-V (→ usar transitoria).
4. **Ganancia DC correcta ≠ estable**: la estabilidad la decide la fase (Bode, no solo polos).
5. El criterio de **impedancia** se validó cruzadamente contra el modelo acoplado (1.3 %).
