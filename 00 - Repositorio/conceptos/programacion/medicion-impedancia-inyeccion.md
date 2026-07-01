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
