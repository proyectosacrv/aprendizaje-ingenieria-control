# Guía de archivos — dónde está todo y cómo analizarlo

Validado el 2026-06-10: los **29 scripts** de los tres proyectos se ejecutan sin error y
regeneran sus figuras y datos.

## Estructura por proyecto

Cada carpeta `NN - Nombre` contiene:

| Archivo / carpeta | Qué es |
|---|---|
| `*.py` | código fuente (modelo, análisis, simulación) |
| `informe.html` | memoria técnica (nivel TFM/tesis) — abrir en navegador |
| `gen_informe.py` | **genera** `informe.html` (editar aquí, no el HTML) |
| `exportar_datos.py` | vuelca los resultados numéricos a `datos/*.csv` |
| `results/*.png` | figuras (mapas de polos, Bode, Nyquist, transitorios, diagramas) |
| `datos/*.csv` | **datos numéricos para analizar** (Excel / pandas) |
| `README.md` | resumen del proyecto |

## Cómo reproducir y analizar

```bash
cd "01 - GFM-Impedance"        # (o 02, 03)
python main_phase1.py          # ... hasta main_phase5.py: regenera figuras en results/
python exportar_datos.py       # vuelca CSV a datos/
python gen_informe.py          # regenera informe.html
```

Para analizar en Python:
```python
import pandas as pd
ev = pd.read_csv("01 - GFM-Impedance/datos/autovalores.csv")   # modos del sistema
Z  = pd.read_csv("01 - GFM-Impedance/datos/impedancia_dq.csv") # impedancia vs frecuencia
```

## Datos exportados (`datos/`)

**01 · GFM-Impedance**
- `equilibrio.csv` — punto de operación (15 estados + P, Q, residual)
- `autovalores.csv` — 15 modos: parte real, imaginaria, frecuencia, amortiguamiento
- `impedancia_dq.csv` — |Z| y fase de Zdd, Zqq, Zdq, Zqd vs frecuencia (600 puntos)
- `scr_sweep.csv` — max Re vs SCR (control agresivo)

**02 · GFL-Impedance**
- `equilibrio.csv` — punto de operación (10 estados)
- `autovalores.csv` — 10 modos
- `impedancia_reZ.csv` — Re(Zdd), Re(Zqq) para f_pll = 30 y 100 Hz (resistencia negativa)
- `scr_vs_pll.csv` — SCR crítico vs ancho de banda de la PLL (40–170 Hz)

**03 · Energia-DataCenter-IA**
- `estabilidad_cpl.csv` — max Re vs P_cpl para Cdc = 2/5/10 mF
- `impedancia_fuente.csv` — |Z_fuente| vs frecuencia (criterio de Middlebrook)
- `pico_frecuencia.csv` — frecuencia AC vs tiempo ante el pico, para H = 1/3/6 s
- `pico_tension_dc.csv` — tensión del bus DC vs tiempo, para Cdc = 4/8/16 mF

## Resultados clave (verificados por ejecución)

| Proyecto | Resultado | Valor |
|---|---|---|
| GFM | estable, modo de potencia | max Re = −8.32; 3.3 Hz, ζ = 0.40 |
| GFM | SCR crítico (acoplado / Nyquist) | 3.347 / 3.390 (1.3 %) |
| GFM | validación impedancia / promediado | 0.21 % / 0.67 % |
| GFM | falta con/sin current limiting | 4.76 → 1.51 pu |
| GFL | modo de la PLL | 21.3 Hz, ζ = 0.71 |
| GFL | SCR crítico (acoplado / Nyquist) | 3.478 / 3.551 (~2 %) |
| GFL | SCR crítico vs PLL | 40 Hz → 1.0 ; 170 Hz → 8.0 |
| DataCenter | P crítica CPL (teórica / autovalores / Middlebrook) | 128 / 129 / 134 kW |
| DataCenter | RoCoF con H = 1 / 3 / 6 s | −1.78 / −0.68 / −0.34 Hz/s |

## Acceso desde el móvil / remoto

Los informes son **responsive**: en móvil la barra lateral se pliega arriba y el contenido
ocupa todo el ancho. Dos formas de verlos (ambas sirven la portada + repositorio + 3 informes):

- **Misma WiFi** → `lanzar-servidor.bat` (raíz). Muestra una IP `http://192.168.x.x:8080`;
  ábrela en el móvil conectado a la misma red.
- **Desde cualquier sitio (datos móviles, otra red)** → `lanzar-remoto.bat` (raíz). Crea un
  enlace público temporal `https://XXXX.trycloudflare.com` (túnel de Cloudflare; descarga
  `cloudflared.exe` la primera vez, sin cuenta). Mantén la ventana abierta mientras lo uses.
- **Permanente y público** (opcional) → publicar la carpeta en **GitHub Pages**: URL fija
  accesible siempre, sin tener el PC encendido (requiere cuenta de GitHub; el contenido es
  público).

## PLECS (validación del modelo conmutado — proyecto 01)

- `01 - GFM-Impedance/PLECS_GUIA.md` — guía completa de construcción del esquemático conmutado
  y de la medición de impedancia.
- `01 - GFM-Impedance/plecs_control_gfm.c` — control grid-forming listo para pegar en un
  bloque C-Script (réplica de `model.py`, discretizada).
- `01 - GFM-Impedance/plecs_cosim.py` — co-simulación XML-RPC: mide la impedancia en PLECS,
  la compara con la analítica y guarda el error en `datos/`.
