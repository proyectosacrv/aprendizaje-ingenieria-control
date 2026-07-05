---
titulo: Medición de impedancia por inyección de perturbación
slug: medicion-impedancia-inyeccion
categoria: programacion
tipo: metodo
nivel: avanzado
proyectos: [01-GFM-Impedance]
objetivos: [medir Z_dq en simulacion/hardware y validar el modelo]
tags: [impedancia, inyeccion, demodulacion, MIMO, validacion, PLECS]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [impedancia-salida-estabilidad, respuesta-frecuencia-ss, convertidor-vsc]
referencias:
  - "Roinila et al., Frequency-Response Measurement of Converters, IEEE TPEL"
---

## Definición
Procedimiento para **medir** la impedancia/admitancia dq de un convertidor (en simulación
conmutada, PLECS o hardware) inyectando perturbaciones y analizando la respuesta. Es la
contraparte experimental del cálculo analítico \( Y=C(sI-A)^{-1}B+D \).

## Fundamento teórico
A cada frecuencia \( f_p \) se inyecta una perturbación senoidal de tensión. Como el sistema dq
es **MIMO 2×2**, se necesitan **dos** inyecciones linealmente independientes (eje d y eje q)
para identificar la matriz completa. Con los fasores de tensión \( \mathbf{V} \) y corriente
\( \mathbf{I} \) (columnas = experimentos):
$$ \mathbf{I}=\mathbf{G}\,\mathbf{V}\;\Rightarrow\;\mathbf{G}=\mathbf{I}\,\mathbf{V}^{-1},\qquad
   \mathbf{Y}=-\mathbf{G},\quad \mathbf{Z}=\mathbf{Y}^{-1} $$
Los fasores se extraen por **demodulación** (correlación con sin/cos sobre un número entero de
periodos).

<div class="cfig"><img src="figuras/medicion-impedancia-inyeccion-bode.png" alt="impedancia medida por inyeccion frente a la analitica"><div class="cap">La impedancia medida inyectando perturbaciones y demodulando los fasores (en simulación conmutada, PLECS o hardware) se superpone a la calculada analíticamente con $Y=C(sI-A)^{-1}B+D$. El acuerdo (error medio ~0.2 %) valida el modelo promediado en pequeña señal; deja de valer si la amplitud activa el current limiting.</div></div>

## 1 — De la perturbación inyectada al fasor: proceso completo a una frecuencia
**Paso 1 — inyección de un tono.** A la frecuencia \( f_p \) se superpone una perturbación senoidal de tensión de amplitud \( A \) sobre el punto de equilibrio:

$$ v_{pert}(t) = A\sin(2\pi f_p t) $$

La amplitud \( A \) debe ser **pequeña señal**: suficiente para que la relación señal/ruido (SNR) en la medición de la respuesta sea adecuada, pero sin activar saturaciones ni el current limiting. En la práctica \( A \approx 0.01\text{–}0.05\,\text{p.u.} \) del nominal.

**Paso 2 — medición y demodulación.** Se miden \( v(t) \) e \( i(t) \) durante \( N_{ciclos} \) periodos completos de \( f_p \). Los fasores se extraen por correlación (DFT a una única frecuencia):

$$ \hat{V}(f_p) = \frac{2}{T}\int_0^T v(t)\,e^{-j2\pi f_p t}\,dt \approx \frac{2}{N}\sum_{k=1}^N v[k]\,e^{-j2\pi f_p k/N} $$

Usar un número **entero** de periodos evita fuga espectral: si la ventana no es exactamente \( N_{ciclos}/f_p \), el fasor tiene error por el espectro de las frecuencias vecinas.

**Paso 3 — relación señal/ruido vs amplitud.** El SNR de la medición a \( f_p \) es:

$$ \text{SNR} \approx \frac{A \cdot |Z(f_p)|}{v_{ruido,rms}} $$

Un SNR \( >20\,\text{dB} \) (factor 10 en amplitud) garantiza errores de fasor \( <1\,\% \). Si la impedancia \( |Z| \) es pequeña (frecuencias altas, donde el inductor domina) se necesita \( A \) mayor; si es grande (cerca de resonancias), con \( A \) pequeña basta. El compromiso: \( A \) grande mejora el SNR pero puede excitar no linealidades.

**Paso 4 — construcción de la matriz \( \mathbf{Z} \).** Con las dos inyecciones (eje d y eje q) se forman las matrices \( 2\times2 \) de fasores y se invierte:

$$ \mathbf{Z}(f_p) = -\mathbf{V}\,\mathbf{I}^{-1} $$

$$ \boxed{Z_{dd},Z_{dq},Z_{qd},Z_{qq} \text{ en un punto de frecuencia con 2 experimentos MIMO}} $$

## Cuándo y por qué se usa
Para **validar** el modelo promediado contra la planta conmutada/real, y para caracterizar
convertidores comerciales "caja negra" cuya impedancia no se conoce analíticamente.

## Procedimiento de diseño (genérico)
1. Lleva el sistema al punto de operación.
2. Para cada \( f_p \): inyecta en d (exp.1) y en q (exp.2), pequeña amplitud (pequeña señal).
3. Simula hasta régimen permanente (descarta el transitorio).
4. Demodula \( v,i \) a \( f_p \) (correlación sobre periodos enteros) → fasores.
5. Monta \( \mathbf{G}=\mathbf{I}\,\mathbf{V}^{-1} \), \( Z=(-G)^{-1} \). Repite en frecuencia.
6. Compara con el analítico (debe coincidir en pequeña señal).

## Ejemplo de código
```python
def phasor(t, x, fp):                 # demodulacion sobre periodos enteros
    w = 2*np.pi*fp; T = t[-1]-t[0]
    c = np.trapz(x*np.cos(w*t), t); s = np.trapz(x*np.sin(w*t), t)
    return (2/T)*(c - 1j*s)
# dos inyecciones (d, q) -> columnas de V e I
G = I @ np.linalg.inv(V); Y = -G; Z = np.linalg.inv(Y)
```

## Parámetros y valores típicos
Amplitud pequeña (pequeña señal); ventana de varios periodos tras el asentamiento. Validez solo
mientras no haya saturación (si entra el current limiting, deja de ser lineal).

## Errores comunes
- Una sola inyección en un sistema dq acoplado → no identifica la matriz 2×2.
- Ventana no entera de periodos → fuga espectral en la demodulación.
- Amplitud grande que activa no linealidades → la "impedancia" deja de tener sentido.

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: validar el modelo): la Z medida por inyección coincidió con
  la analítica con **error medio 0.21%**. En `inject.py` / `main_phase4.py`. El mismo código
  procesa datos exportados de PLECS.

## Conceptos relacionados
- [[impedancia-salida-estabilidad]] · [[respuesta-frecuencia-ss]] · [[convertidor-vsc|modelo promediado]]

## Referencias
- Roinila et al., medición de respuesta en frecuencia de convertidores.

---

## 3 — Método de inyección de señal

**Inyección de la perturbación.** Se superpone una señal senoidal de tensión en el punto de medida:

$$ v_p(t) = A\sin(\omega t), \quad \omega = 2\pi f_p $$

La amplitud \( A \) es un compromiso entre relación señal/ruido (requiere \( A \) grande) y linealidad del sistema (requiere \( A \) pequeña). En convertidores de potencia, \( A \approx 1\text{–}5\,\% \) del valor nominal garantiza ambas condiciones.

**Medición de tensión y corriente.** Se registran simultáneamente \( v(t) \) e \( i(t) \) en el punto de inyección. La impedancia se calcula como:

$$ Z(j\omega) = \frac{V(j\omega)}{I(j\omega)} $$

donde \( V(j\omega) \) e \( I(j\omega) \) son los fasores a frecuencia \( f_p \) obtenidos por DFT.

**Amplitud de perturbación.** La elección práctica de \( A \) depende del nivel de ruido \( v_{ruido,rms} \) y de la impedancia esperada:

$$ \text{SNR} \approx \frac{A \cdot |Z(f_p)|}{v_{ruido,rms}} > 20\,\text{dB} $$

<div class="cfig"><img src="../figuras/medicion-impedancia-inyeccion-analisis.png" alt="Medición de impedancia por inyección de señal"><div class="cap">Panel superior izquierdo: señal inyectada y respuesta en corriente. Superior derecho: espectro DFT mostrando el tono inyectado. Inferior izquierdo: comparación impedancia teórica vs medida en barrido de frecuencia. Inferior derecho: coherencia del barrido — válido solo donde γ²>0.9.</div></div>

## 4 — DFT y sincronización

**Ventana coherente.** La DFT asume señales periódicas. Si la ventana de análisis no contiene exactamente \( N_{ciclos} \) períodos completos de la señal inyectada, aparece **fuga espectral**: energía de la frecuencia de inyección se dispersa hacia frecuencias vecinas, contaminando la estimación del fasor.

**Condición de coherencia:**

$$ T_{ventana} = \frac{N_{ciclos}}{f_p} \quad (N_{ciclos} \in \mathbb{Z}^+) $$

Si no se puede garantizar coherencia (p.ej. el muestreo no es síncrono con la inyección), se aplica una **ventana de Hanning** que atenúa la fuga a costa de reducir la resolución espectral.

**Rango de frecuencias analizables:**
- Mínimo: \( f_{min} = f_p \) (una resolución de la DFT)
- Máximo: \( f_{max} \approx f_{sw}/2 \) (Nyquist del muestreo de control)
- Límite práctico: evitar frecuencias múltiplos de \( f_0=50\,\text{Hz} \) donde el ruido de red es mayor

**Supresión de interarmónicos.** El muestreo coherente con la señal inyectada asegura que los armónicos del convertidor (múltiplos de \( f_{sw} \)) caen en bins separados de la DFT, sin solaparse con \( f_p \).

## 5 — Analizador de impedancias en lazo cerrado

**Inyección en el lazo de control.** Al inyectar la perturbación después del regulador (entre el control y el modulador), se mide la impedancia de lazo cerrado \( Z_{cl}(j\omega) \). Esta es la magnitud relevante para el criterio de estabilidad de Middlebrook.

**Inyección en la red.** Al inyectar en la red (entre el convertidor y el transformador), se mide \( Z_{grid}(j\omega) \), útil para detectar variaciones del SCR sin interrumpir la operación.

**Separación fuente/carga.** Para separar la impedancia de la fuente \( Z_s \) de la de la carga \( Z_l \), se realizan dos inyecciones en puntos distintos o una perturbación diferencial; la combinación lineal de las respuestas da cada impedancia por separado.

**Criterio de validez de la medición:** el SNR debe superar 20 dB en la frecuencia de análisis. Por debajo de este umbral el fasor estimado tiene error angular \( > 5.7° \), que puede confundirse con una variación real de impedancia.

## 6 — Herramientas Python y aplicación práctica

**Estimación espectral con ruido.** Para señales ruidosas, `scipy.signal.welch` calcula la densidad espectral de potencia (PSD) promediando sobre ventanas solapadas de Welch, reduciendo la varianza de la estimación de \( |Z|^2 \) a costa de resolución temporal.

**Coherencia.** El índice de coherencia entre tensión y corriente indica la fiabilidad de la estimación de impedancia:

$$ \gamma^2(f) = \frac{|S_{vi}(f)|^2}{S_{vv}(f)\,S_{ii}(f)} \in [0,1] $$

Un valor \( \gamma^2 > 0.9 \) indica que al menos el 90% de la varianza de la corriente a esa frecuencia se explica por la tensión inyectada: la medición es válida. Valores menores indican ruido excesivo, no-linealidades, o que la señal inyectada es demasiado débil.

**Aplicación en bus DC de data center.** Para caracterizar la estabilidad de un bus DC con cargas de potencia constante (CPL) se mide \( Z_{bus}(j\omega) \) a distintas cargas:
1. Inyectar una perturbación de tensión \( \Delta v_{dc} \) a la frecuencia de interés.
2. Medir la corriente de respuesta \( \Delta i_{dc} \).
3. Calcular \( Z_{bus}(j\omega) = \Delta V_{dc}(j\omega)/\Delta I_{dc}(j\omega) \).
4. Verificar el **criterio de Middlebrook**: el sistema es estable si \( |Z_{source}(j\omega)| < |Z_{load}(j\omega)| \) para toda \( \omega \). Si la CPL hace que \( Z_{load} \) tenga parte real negativa y su módulo sea menor que \( Z_{source} \), hay riesgo de oscilación.
