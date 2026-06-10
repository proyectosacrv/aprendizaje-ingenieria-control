---
titulo: Calidad de potencia y normativa (IEEE 519, IEC 61000)
slug: calidad-potencia
categoria: metodologia
tipo: concepto
nivel: intermedio
proyectos: []
objetivos: [cuantificar y cumplir los límites de distorsión armónica, desequilibrio y flicker]
tags: [calidad-potencia, thd, armonicos, flicker, ieee519, iec61000, desequilibrio, intermedio]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-09
relacionados: [fft-analisis-espectral, modulacion-pwm, filtro-lcl, estabilidad-armonica, deteccion-islanding]
referencias:
  - "IEEE Std 519-2022, Harmonic Control in Electric Power Systems"
  - "IEC 61000-3-2/3-12, Limits for Harmonic Current Emissions"
  - "IEC 61000-4-30, Power Quality Measurement Methods"
---

## Definición
Conjunto de métricas y límites normativos que caracterizan la **calidad de la tensión/corriente**
entregada a la red: armónicos, interarmónicos, desequilibrio, flicker (parpadeo), dips/swells y
transitorios. Define lo que el convertidor no debe inyectar en el punto de conexión común (PCC).

## Fundamento teórico
**Distorsión armónica total (THD):**
$$ \text{THD}_I = \frac{\sqrt{\sum_{h=2}^{\infty}I_h^2}}{I_1}\times100\,\% $$
En **IEEE 519-2022** los límites de corriente se fijan en el PCC en función de la relación
\( I_{sc}/I_L \) (relación de cortocircuito / carga): a mayor SCR más corriente armónica admisible.
Armónicos de tensión total < 5 %, individuales < 3 %.

**IEC 61000-3-2/3-12:** límites de emisión armónica de equipos individuales (hasta 16 A y hasta
75 A respectivamente) para 2–40 armónicos en valores absolutos (A) por fase.

**Desequilibrio de tensión** (NEMA / IEC 61000-2-2): factor de desequilibrio
\( V_{unb}=V_{neg}/V_{pos}\times100\,\% < 2\text{–}3\,\% \).

**Flicker (IEC 61000-3-3 / 61000-3-11):** \( P_{st} \) (flicker de corta duración, 10 min) y
\( P_{lt} \) (larga duración, 2 h) miden la sensación de parpadeo; causado por cargas pulsantes de
gran amplitud a 0.5–25 Hz. Límites: \( P_{st}<1 \), \( P_{lt}<0.65 \).

**Medición normativa (IEC 61000-4-30 clase A):** ventanas sincronizadas de 10/12 ciclos (200/166,7 ms);
agrupación en 3 s, 10 min, 2 h para estadísticas.

**Origen en convertidores:** la [[modulacion-pwm|conmutación PWM]] genera armónicos en torno a
\( f_{sw} \) y bandas laterales; el [[filtro-lcl]] los atenúa; la resonancia del LCL y la
[[estabilidad-armonica]] pueden amplificarlos. Las cargas pulsantes de data center (GPU en rafaga)
generan flicker e interarmónicos.

## Cuándo y por qué se usa
Como criterio de aceptación en el diseño del filtro y del control, en auditorías de conexión a red
y en el análisis de impacto de cargas de data center / renovables. Conecta los estudios de
simulación con los requisitos legales.

## Procedimiento de diseño (genérico)
1. Identifica la norma aplicable (IEEE 519 para red industrial US; IEC 61000 para Europa/equipos).
2. Mide o simula la corriente en el PCC con [[fft-analisis-espectral|FFT]] (ventana IEC 61000-4-30).
3. Compara con los límites por armónico y THD.
4. Si incumple: aumenta la atenuación del [[filtro-lcl]], añade filtro activo o [[control-repetitivo]],
   o reduce la carga armónica en el PCC.
5. Para flicker: evalúa la carga pulsante y mitiga con almacenamiento/bus DC correctamente
   dimensionado ([[dinamica-bus-dc]]).

## Ejemplo de código
```python
import numpy as np
def thd(spectrum_rms, fundamental_idx=1):
    harm = np.concatenate([spectrum_rms[:fundamental_idx], spectrum_rms[fundamental_idx+1:]])
    return np.sqrt(np.sum(harm**2)) / spectrum_rms[fundamental_idx] * 100  # %
```

## Parámetros y valores típicos
THD de corriente < 5 % (IEEE 519 en conexión típica); armónico individual 3–5 % (orden dependiente);
desequilibrio < 2 %; \( P_{st}<1 \). Armónicos dominantes de VSC 2-niveles: \( f_{sw}\pm 2f_1 \),
\( 2f_{sw}\pm f_1 \).

## Errores comunes
- Medir THD con ventana no sincronizada → fuga espectral que infla el THD artificialmente.
- Cumplir límites de armónicos individuales pero ignorar el THD total.
- Confundir límites de emisión de equipo (IEC 61000-3-2) con límites del PCC (IEEE 519).
- Ignorar el flicker en cargas pulsantes de data center (GPU workloads).

## Conceptos relacionados
- [[fft-analisis-espectral]] · [[modulacion-pwm]] · [[filtro-lcl]] · [[estabilidad-armonica]] · [[deteccion-islanding]]

## Referencias
- IEEE Std 519-2022, *Harmonic Control in Electric Power Systems*.
- IEC 61000-3-2, *Limits for Harmonic Current Emissions*.
- IEC 61000-4-30, *Power Quality Measurement Methods*.
