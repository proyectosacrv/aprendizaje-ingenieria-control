---
titulo: Validación cruzada (coincidencia entre niveles/métodos)
slug: validacion-cruzada
categoria: metodologia
tipo: metodo
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [confirmar un resultado por dos vias independientes]
tags: [validacion, cruzada, consistencia, modelo, confianza]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [niveles-validacion, pruebas-validacion, impedancia-salida-estabilidad, medicion-impedancia-inyeccion]
referencias:
  - "buena praxis de modelado y verificación (V&V)"
---

## Definición
Confirmar un mismo resultado por **dos caminos independientes** (dos modelos, dos métodos, o dos
niveles de fidelidad). Si coinciden, la confianza en ambos sube; si no, hay un error que localizar.

## Fundamento teórico
La validación cruzada es la forma práctica de "verificación y validación" (V&V):
- **Entre métodos**: el mismo resultado por dos teorías distintas (p.ej. SCR crítico por
  autovalores del modelo acoplado **y** por Nyquist de impedancia).
- **Entre niveles**: lineal ↔ medición por inyección; promediado ↔ conmutado; simulación ↔ HIL.
- Un desacuerdo acota el error: si dos métodos discrepan, el fallo está en uno de los dos (o en la
  hipótesis común), y se investiga.

<div class="cfig"><img src="figuras/validacion-cruzada-scr.png" alt="SCR critico por dos metodos independientes en GFM y GFL"><div class="cap">El SCR crítico calculado por dos vías independientes —autovalores del modelo acoplado y Nyquist del cociente de impedancias— coincide en ambos proyectos con menos del 2 % de diferencia. Ese acuerdo convierte "el modelo dice que es estable" en confianza real; un desacuerdo, en cambio, acotaría dónde está el error.</div></div>

## 1 — RMSE y VAF: qué miden y cómo se calculan
**Paso 1 — RMSE (Root Mean Square Error).** Dados \( N \) puntos de la salida medida \( y_k \) y la predicción del modelo \( \hat{y}_k \):

$$ \text{RMSE} = \sqrt{\frac{1}{N}\sum_{k=1}^N \bigl(y_k - \hat{y}_k\bigr)^2} $$

El RMSE tiene las mismas **unidades** que la señal (amperios, voltios, p.u.) y cuantifica el error cuadrático medio: un RMSE de 0.05 A sobre una corriente de 10 A significa un error típico del 0.5 %. Se penalizan los errores grandes (cuadrado) más que los pequeños.

**Paso 2 — VAF (Variance Accounted For).** El VAF normaliza el error por la varianza de la señal medida:

$$ \text{VAF} = 100\cdot\left(1-\frac{\mathrm{var}(y-\hat{y})}{\mathrm{var}(y)}\right)\,[\%] $$

Un VAF del 100 % significa que el modelo reproduce perfectamente la varianza de la señal (la varianza del error es cero). Un VAF del 0 % significa que el modelo no explica nada más que la media. Para un modelo que tiene un error de offset constante, \( \mathrm{var}(y-\hat{y})=0 \) y VAF=100 %, aunque el RMSE sea distinto de cero: el VAF mide **forma dinámica**, no exactitud absoluta de nivel.

**Paso 3 — ejemplo numérico.** Para un modelo que reproduce exactamente la dinámica con un offset del 5 %: \( \hat{y}_k = 1.05\,y_k \), la varianza del error \( \mathrm{var}(y-\hat{y})=0.05^2\,\mathrm{var}(y) \), y:

$$ \text{VAF} = 100\cdot(1-0.0025) = 99.75\,\% $$

mientras que el RMSE sería \( 0.05\,\sqrt{\mathrm{var}(y)} \). Por eso ambas métricas se usan juntas: RMSE detecta el bias; VAF detecta si la dinámica está bien captada.

$$ \boxed{\text{RMSE} \to \text{error de nivel};\quad \text{VAF}\to\text{error de forma dinámica}} $$

## Cuándo y por qué se usa
Siempre que sea posible. Es lo que convierte "el modelo dice que es estable" en "estoy seguro de
que es estable". Especialmente valioso antes de hardware.

## Procedimiento (genérico)
1. Elige dos vías independientes para la misma magnitud.
2. Calcula por ambas y compara (error relativo).
3. Si coinciden (p.ej. <5%), valida; documenta el acuerdo.
4. Si no, localiza la discrepancia (hipótesis, signo, implementación) y corrige.

## Ejemplo de código
```python
scr_acoplado = biseccion(maxre_modelo_acoplado)   # via A: autovalores
scr_impedancia = nyquist_critico(Zred, Yinv)      # via B: criterio de impedancia
err = abs(scr_acoplado - scr_impedancia)/scr_acoplado
assert err < 0.05, "las dos vias no coinciden -> revisar"
```

## Parámetros y valores típicos
Acuerdo aceptable < 5% entre métodos lineales; entre niveles distintos, esperar discrepancias en
las bandas donde el nivel superior añade física (conmutación cerca de \( f_{sw}/2 \)).

## Errores comunes
- Dos vías que en realidad comparten la misma hipótesis (no son independientes) → falso acuerdo.
- Atribuir toda la discrepancia al nivel superior sin revisar el inferior.

## Uso en proyectos
- **01 (GFM)**: SCR crítico 3.35 (acoplado) vs 3.39 (impedancia) → 1.3%.
- **02 (GFL)**: 3.48 (acoplado) vs 3.55 (impedancia) → 2%. Y la impedancia medida por inyección
  coincidió con la analítica (0.21%).

## Conceptos relacionados
- [[niveles-validacion]] · [[pruebas-validacion]] · [[impedancia-salida-estabilidad]] · [[medicion-impedancia-inyeccion]]

## Referencias
- Buena praxis de V&V en modelado.

## 3 — Validación cruzada k-fold

La validación cruzada k-fold divide el conjunto de datos en \( k \) grupos (folds) iguales. En cada iteración, \( k-1 \) grupos se usan para entrenamiento y 1 para validación; el proceso se repite \( k \) veces rotando el fold de validación. El error final se promedía sobre las \( k \) iteraciones:

$$ \text{CV}_k = \frac{1}{k}\sum_{i=1}^{k} \mathcal{L}(y_i, \hat{y}_i) $$

**Leave-one-out (LOO):** caso particular con \( k=N \) (N = número de muestras). Máxima iteraciones, sin sesgo de partición pero con coste computacional \( O(N) \) veces mayor que un entrenamiento. Adecuado para datasets pequeños (\( N<100 \)) como los que aparecen en identificación de modelos de convertidores.

**Métrica FIT%:** mide qué fracción de la varianza de la señal queda explicada por el modelo:

$$ \text{FIT\%} = \left(1 - \frac{\|y - \hat{y}\|}{\|y - \bar{y}\|}\right)\times 100 $$

donde \( \bar{y} \) es la media de la señal medida. Un FIT%>80% se considera condición mínima para usar el modelo en diseño de controladores; FIT%>90% es habitual en lazos de corriente de convertidores bien identificados.

**NRMSE (Normalized RMSE):**

$$ \text{NRMSE} = \frac{\|y - \hat{y}\|}{\|y - \bar{y}\|} = 1 - \frac{\text{FIT\%}}{100} $$

El NRMSE=0 es ajuste perfecto; NRMSE=1 equivale a predecir siempre la media (modelo nulo). La ventaja del NRMSE frente al RMSE es que es adimensional y comparable entre señales de distintas magnitudes.

<div class="cfig"><img src="../figuras/validacion-cruzada-analisis.png" alt="k-fold, curva de aprendizaje y FIT% vs orden del modelo"><div class="cap">Validación cruzada k-fold (k=5): cada fold rota el subconjunto de validación. La curva de aprendizaje muestra cómo el error de validación tiene un mínimo antes de aumentar (overfitting). El FIT% vs orden del modelo permite elegir el orden mínimo que supera el umbral del 80%.</div></div>

## 4 — Overfitting y underfitting

El **overfitting** (sobreajuste) ocurre cuando el modelo tiene demasiados parámetros libres respecto al número de datos: aprende el ruido del conjunto de entrenamiento en lugar de la dinámica subyacente. Síntoma: \( R^2 \approx 1 \) en entrenamiento, error elevado en validación.

El **underfitting** (subajuste) ocurre cuando el modelo es demasiado simple (orden bajo, pocos parámetros) para capturar la dinámica real. Síntoma: error elevado tanto en entrenamiento como en validación.

La **curva de aprendizaje** representa el error de entrenamiento y de validación en función del número de muestras disponibles:
- El error de entrenamiento sube ligeramente con más datos (el modelo ya no puede ajustar todas las muestras).
- El error de validación baja monotónicamente con más datos hasta un mínimo, luego estabiliza.
- Si los dos errores convergen a un valor bajo: buena generalización. Si convergen a un valor alto: underfitting (aumentar complejidad del modelo). Si divergen (entrenamiento bajo, validación alto): overfitting.

**Regularización** para reducir overfitting: penalizar los coeficientes grandes en la función de coste:
- \( \ell_2 \) (ridge): \( \mathcal{L} + \lambda\sum_j\theta_j^2 \); shrinkage suave de todos los parámetros.
- \( \ell_1 \) (lasso): \( \mathcal{L} + \lambda\sum_j|\theta_j| \); selección esparcida (pone algunos \( \theta_j \) exactamente a cero).
- En modelos de sistemas lineales: equivale a añadir un prior bayesiano sobre los coeficientes del modelo de estado.

## 5 — Validación cruzada para modelos de control

En identificación de sistemas para diseño de controladores, la validación cruzada tiene características específicas:

- **Generalización a condiciones no vistas:** el modelo linealizado (p.ej. función de transferencia del lazo de corriente) se identifica con datos a una potencia y se valida con datos a otra potencia o con perturbaciones distintas. Condición mínima: FIT%>80% en el conjunto de validación con excitaciones no usadas en la identificación.

- **Selección del orden del modelo:** comparar FIT% de validación para modelos de orden 1, 2, 3,… eligiendo el orden mínimo que supere el umbral. Un modelo de orden 2 con FIT%=89% es preferible a uno de orden 6 con FIT%=91%: más robusto y más fácil de analizar.

- **Validez del punto de operación:** un modelo lineal solo es válido cerca del punto donde se linealizó. Si se aplica a una condición muy distinta (otra tensión, otra potencia), el FIT% caerá por debajo del umbral — señal de que se necesita linealización o identificación local.

- **Aplicación en convertidores:** modelo del lazo de corriente identificado a 50% de carga, validado a 20% y 80%. Si FIT%>80% en ambas condiciones de validación, el controlador único es válido en todo el rango operativo sin gain-scheduling.

$$ \boxed{\text{FIT\%}>80\%\text{ en validación}\;\Rightarrow\;\text{el modelo es apto para diseño}} $$

## 6 — Herramientas Python

**`sklearn.model_selection.cross_val_score`:** k-fold automático para estimadores de sklearn. Devuelve el array de \( k \) puntuaciones; la media y la desviación estándar caracterizan el rendimiento esperado y su variabilidad.

**`sklearn.model_selection.LeaveOneOut`:** LOO para datasets pequeños; genera iteradores sobre índices de entrenamiento y validación.

**Modelos dinámicos:** para sistemas lineales descritos por funciones de transferencia o espacio de estados, `sklearn` no aplica directamente. Se implementa manualmente con ventanas deslizantes o usando `statsmodels.tsa` para modelos ARMA/ARX.

**Visualización:** `sklearn.model_selection.learning_curve` calcula la curva de aprendizaje para un estimador dado; `matplotlib` la visualiza con bandas de incertidumbre.

```python
from sklearn.model_selection import cross_val_score, LeaveOneOut
import numpy as np

# k-fold para modelo sklearn
scores = cross_val_score(modelo, X, y, cv=5, scoring='r2')
print(f"R² medio: {scores.mean():.3f} ± {scores.std():.3f}")

# FIT% manual para modelo dinámico
def fit_percent(y, y_hat):
    return (1 - np.linalg.norm(y - y_hat) / np.linalg.norm(y - y.mean())) * 100

# Ejemplo: validar modelo ARX de orden n
for n in range(1, 9):
    # ... identificar modelo con datos de entrenamiento ...
    # fit_val = fit_percent(y_val, y_hat_val)
    pass
```

**Implementación manual para datos dinámicos en ventanas deslizantes:**

Para modelos de sistemas dinámicos, la validación cruzada estándar de sklearn no aplica directamente. Se implementa con bloques temporales consecutivos:

```python
import numpy as np

def fit_percent(y, y_hat):
    """FIT% segun definicion del MATLAB System Identification Toolbox."""
    num = np.linalg.norm(y - y_hat)
    den = np.linalg.norm(y - np.mean(y))
    return max(0.0, (1 - num / den) * 100)

def kfold_temporal(y, u, k=5, model_fn=None):
    """k-fold temporal: los bloques son intervalos de tiempo consecutivos."""
    N = len(y)
    fold_size = N // k
    fits = []
    for i in range(k):
        val_s = i * fold_size
        val_e = (i + 1) * fold_size if i < k-1 else N
        tr_idx = list(range(0, val_s)) + list(range(val_e, N))
        val_idx = list(range(val_s, val_e))
        mdl = model_fn(u[tr_idx], y[tr_idx])
        y_hat = mdl.simulate(u[val_idx])
        fits.append(fit_percent(y[val_idx], y_hat))
    return np.array(fits)
```

**Relacion entre FIT% y los margenes de estabilidad:**

Un modelo con FIT% = 85% en el rango de frecuencias de interes predice los margenes de estabilidad con un error de aproximadamente ±5°. Si el margen de fase nominal es 54° y el criterio de aceptacion es PM > 45°, hay un margen de 9° frente al posible error del modelo — suficiente si FIT% > 80% pero ajustado. Con FIT% < 70% el margen de error del modelo es comparable al margen de estabilidad y no se puede confiar en el diseno.

**Errores comunes con la validacion cruzada:**

- **Solapamiento en series temporales:** si se mezclan datos de entrenamiento y validacion sin respetar el orden temporal, el modelo aprende a "copiar" valores del futuro y el FIT% es artificialmente alto. Siempre usar bloques temporales consecutivos.
- **Normalizar con la media del fold:** el NRMSE debe normalizarse con la media de todos los datos o solo de entrenamiento, no con la media del fold de validacion — de lo contrario la metrica es inconsistente entre folds.
- **Validar fuera del rango de identificacion:** si el modelo se identifica con PRBS de 0-500 Hz pero el control opera a 1 kHz, el FIT% en 500-1000 Hz puede ser bajo aunque el modelo sea valido para su uso previsto.

**Valores tipicos en proyectos de convertidores:**

| Lazo | FIT% tipico | Criterio | Comentario |
|---|---|---|---|
| Corriente id (GFL) | 88-95% | >80% | Dinamica lineal, bien identificable |
| Tension Vdc (GFM) | 82-90% | >80% | Mas no-lineal por la saturacion |
| Potencia P (droop) | 75-85% | >70% | Dinamica lenta, mas ruido relativo |
| Impedancia Z(f) | Error<5% | <5% | Comparacion analitica vs inyeccion |

## 7 — k-fold vs LOO: cuándo usar cada uno

**k-fold** (k=5 o k=10): divide los datos en \(k\) bloques iguales y rota el bloque de validación. Equilibra sesgo y varianza: con k=5 cada modelo se entrena con el 80% de los datos; la variabilidad entre folds caracteriza la robustez del resultado. Adecuado cuando \(N>50\) muestras.

**Leave-one-out (LOO):** caso particular con \(k=N\). Mínimo sesgo (cada modelo usa \(N-1\) muestras), pero máxima varianza entre iteraciones y coste computacional \(O(N)\) veces mayor. Indicado cuando los datos son escasos (\(N<30\)) como en la identificación de modelos de convertidores a partir de ensayos de laboratorio con pocas condiciones de operación.

**Regla de selección:**
- \(N>100\): k-fold con k=5 es suficiente y mucho más rápido.
- \(N<30\): LOO; el coste computable es asumible y minimiza el sesgo.
- Series temporales: siempre usar bloques consecutivos (no aleatorizados) para evitar fuga de información futura al pasado.

## 8 — Overfitting y underfitting: diagnóstico y remedio

El **overfitting** ocurre cuando el modelo tiene más parámetros libres que los que los datos pueden determinar: aprende el ruido del conjunto de entrenamiento en lugar de la dinámica subyacente. Síntoma: \(R^2\approx1\) o FIT%≈100% en entrenamiento, pero error elevado en validación.

El **underfitting** ocurre cuando el orden del modelo es insuficiente para capturar la dinámica real. Síntoma: error elevado tanto en entrenamiento como en validación; la curva de aprendizaje converge a un valor alto.

**Diagnóstico por curva de aprendizaje:** trazar el error de entrenamiento y de validación en función del número de muestras \(N\):
- Si ambos convergen a un valor bajo: modelo bien ajustado.
- Si el error de entrenamiento es bajo pero el de validación alto y ambos divergen: overfitting → añadir regularización o reducir el orden del modelo.
- Si ambos convergen a un valor alto: underfitting → aumentar el orden del modelo o añadir características.

**Regularización L1/L2 para reducir overfitting:**
- \(\ell_2\) (ridge): \(\mathcal{L}+\lambda\sum_j\theta_j^2\) — contrae todos los parámetros hacia cero; estabiliza la solución sin anularlos.
- \(\ell_1\) (lasso): \(\mathcal{L}+\lambda\sum_j|\theta_j|\) — selección esparcida; pone algunos \(\theta_j\) exactamente a cero → selección automática de características.

En modelos ARX o de funciones de transferencia: la regularización es equivalente a añadir un prior bayesiano sobre los coeficientes. El parámetro \(\lambda\) se optimiza con validación cruzada.

## 9 — Selección del orden del modelo: criterio del codo

Para seleccionar el orden mínimo suficiente de un modelo lineal (número de polos/ceros o de estados):

1. Identificar modelos de orden 1, 2, 3, ..., \(n_{max}\) con el mismo conjunto de entrenamiento.
2. Calcular FIT% en el conjunto de validación para cada orden.
3. Trazar FIT%(orden) y buscar el "codo": el punto a partir del cual aumentar el orden da una mejora marginal (<2% de FIT%) — ese es el orden mínimo suficiente.
4. Si el orden del codo es el mismo en varias condiciones de operación (50%, 80% de carga, distintas temperaturas), el modelo lineal de ese orden es válido en todo el rango.

**Criterios formales de selección de orden:**
- **AIC** (Akaike): \(\text{AIC}=2k-2\ln\hat{L}\); penaliza la complejidad con \(2k\) parámetros libres.
- **BIC** (Bayesian): \(\text{BIC}=k\ln N - 2\ln\hat{L}\); penalización más fuerte, favorece modelos más simples.
- En la práctica para convertidores: el criterio FIT%>80% con el orden mínimo suele ser suficiente y más intuitivo que AIC/BIC.

## 10 — Aplicación a convertidores: modelo de lazo identificado a una potencia, validado a otra

El flujo de trabajo estándar para identificar el lazo de corriente de un convertidor GFL:

1. **Excitación:** inyectar PRBS (Pseudo-Random Binary Sequence) de amplitud 5% en la referencia de corriente \(i_d^*\) mientras el convertidor opera al 50% de potencia nominal. Registrar \(u(t)=\Delta i_d^*\) e \(y(t)=\Delta i_d\).
2. **Identificación:** ajustar modelo ARX de orden \(n\) usando los primeros 60% de los datos (entrenamiento). Seleccionar el orden mínimo con FIT%>80% en el 40% restante (validación cruzada temporal).
3. **Validación cruzada de potencia:** aplicar el modelo identificado a datos registrados al 20% y al 80% de carga. Condición de aceptación: FIT%>80% en ambas condiciones — el controlador único es válido en todo el rango sin gain-scheduling.
4. **Validación cruzada de método:** comparar la función de transferencia identificada con la analítica (derivada del modelo promediado). Condición: error en \(|G|\) < 5% y error de fase < 5° en la banda de control (DC a \(f_c\)).

$$\boxed{\text{FIT\%}>80\%\ \text{en validación de potencia}\ \Rightarrow\ \text{un solo controlador para todo el rango}}$$

<div class="cfig"><img src="../figuras/validacion-cruzada-analisis.png" alt="k-fold temporal, curva de aprendizaje, FIT% vs orden y comparativa dos métodos"><div class="cap">Validación cruzada aplicada a convertidores: k-fold temporal con bloques consecutivos (izquierda), curva de aprendizaje mostrando el punto de overfitting (centro-izq.), FIT% vs orden del modelo con el "codo" en orden 2 (centro-dcha.), y comparativa analítica vs identificación experimental del lazo de corriente (derecha).</div></div>

## Conceptos relacionados
- [[niveles-validacion]] · [[pruebas-validacion]] · [[impedancia-salida-estabilidad]] · [[medicion-impedancia-inyeccion]]

## Referencias
- Buena praxis de V&V en modelado.
- Ljung, *System Identification: Theory for the User*, Prentice-Hall 1999.
