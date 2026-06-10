# 02 · Grid-following + impedancia

Inversor **grid-following** (PLL + control de corriente) sobre el mismo filtro LCL del proyecto
01, su impedancia de salida y la **inestabilidad en red débil** — el espejo del grid-forming.

> Lee el informe visual: **[informe.html](informe.html)** (memoria del proyecto, con ecuaciones
> y enlaces a las fichas del repositorio).

## Resultados
| Tema | Script | Resultado |
|---|---|---|
| Estabilidad (red rígida) | `main_phase1.py` | Estable; modo PLL a 21 Hz (ζ=0.71) |
| Impedancia de salida | `main_phase2.py` | Re(Z_qq) < 0 = resistencia negativa de la PLL |
| Estabilidad red débil | `main_phase3.py` | SCR crítico 3.48 (acoplado) vs 3.55 (Nyquist) |
| GFM vs GFL | `main_compare.py` | Espejo: GFL inestable en red débil, GFM en red fuerte |

## Idea central
El GFL es **estable en red fuerte e inestable en red débil** si la PLL es rápida. El **ancho de
banda de la PLL** fija el SCR crítico: 40 Hz → SCR_crít ≈ 1 (robusto); 170 Hz → ≈ 8 (frágil).
Es lo contrario del GFM (inestable en red fuerte) — y se explica con la misma herramienta de
impedancia + Nyquist generalizado del proyecto 01.

## Estructura
- `params.py` · `model.py` — modelo GFL (LCL + PLL + lazo de corriente), equilibrio, linealización.
- `impedance.py` · `grid.py` — utilidades (compartidas con el proyecto 01).
- `main_phase1/2/3.py` · `main_compare.py` — análisis.
- `results/` — figuras.

Ejecutar: `python main_phase1.py` (y 2, 3, y `main_compare.py`).
