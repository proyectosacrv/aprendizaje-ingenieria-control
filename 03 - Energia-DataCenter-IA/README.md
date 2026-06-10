# 03 · Energía para data centers de IA (microrred híbrida AC+DC)

Modelado y control del sistema de energía de un data center de IA: un **BESS grid-forming** (AC)
alimenta vía un **AFE** un **bus DC** con la **carga pulsante de IA** (servidores como cargas de
potencia constante, CPL). Estabilidad del bus DC y soporte ante los picos de carga.

> Informe visual: **[informe.html](informe.html)** (ecuaciones, diagramas y enlaces al repositorio).

## Resultados
| Fase | Script | Resultado |
|---|---|---|
| 1 · Inestabilidad CPL | `main_phase1.py` | P_crítica = V²RC/L ≈ 128 kW (autovalores) |
| 2 · Middlebrook | `main_phase2.py` | Límite por impedancia ≈ 134 kW (validación cruzada) |
| 3 · Pico de carga IA | `main_phase3.py` | RoCoF −1.78→−0.34 Hz/s con H=1→6 s; hundimiento DC vs C_dc |
| 4 · Dimensionado | `main_phase4.py` | C_dc por estabilidad CPL (DC); H por RoCoF (AC) |

## Idea central
Los servidores son cargas de **potencia constante**: su resistencia incremental negativa
−V²/P desamortigua el bus DC y lo inestabiliza por encima de P_crítica (es el análogo DC de la
inestabilidad por impedancia del grid-following). El pico de carga de IA exige dimensionar **dos
cosas independientes**: el **condensador de bus** (lado DC, estabilidad) y la **inercia del BESS**
(lado AC, RoCoF).

## Estructura
- `params.py` · `model_dc.py` — bus DC con CPL (2 estados), equilibrio, linealización.
- `simulate.py` — sistema híbrido AC+DC (4 estados) para el pico de carga.
- `main_phase1/2/3/4.py` — análisis. `diagramas.py` — esquema y diagramas.
- `results/` — figuras.

Ejecutar: `python main_phase1.py` (y 2, 3, 4; `diagramas.py`).
