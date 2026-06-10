# Aprendizaje de ingeniería de control de convertidores

Repositorio de conocimiento + memorias técnicas (nivel TFM/tesis) de tres proyectos de
electrónica de potencia y control de convertidores conectados a red.

**🌐 Sitio web:** https://proyectosacrv.github.io/aprendizaje-ingenieria-control/

La portada enlaza el repositorio de conocimiento y los tres informes. Se ve en cualquier
dispositivo (los informes son responsive) sin necesidad de tener el PC encendido.

## Contenido

- **`00 - Repositorio/`** — repositorio de conocimiento: conceptos de física, control y
  programación, filtrable y con vista de grafo (`index.html`).
- **`01 - GFM-Impedance/`** — inversor grid-forming: modelado, control y estabilidad por
  impedancia (15 estados, Nyquist generalizado, impedancia virtual, VSM, current limiting).
- **`02 - GFL-Impedance/`** — inversor grid-following: impedancia e inestabilidad en red débil
  (PLL, resistencia negativa, dualidad GFM↔GFL).
- **`03 - Energia-DataCenter-IA/`** — microrred híbrida AC+DC para data centers de IA
  (bus DC, carga de potencia constante, criterio de Middlebrook, inercia/RoCoF).

Cada proyecto incluye: código Python (modelo, análisis, simulación), `informe.html` (memoria
técnica), figuras en `results/`, datos numéricos en `datos/`, y un `gen_informe.py` que genera
el informe a partir del código real y los resultados. Detalle en [GUIA-ARCHIVOS.md](GUIA-ARCHIVOS.md).

## Reproducir

Requiere Python 3.13 con NumPy, SciPy y Matplotlib.

```bash
cd "01 - GFM-Impedance"
python main_phase1.py      # ... hasta main_phase5.py: regenera figuras
python exportar_datos.py   # vuelca resultados a datos/*.csv
python gen_informe.py      # regenera informe.html
```
