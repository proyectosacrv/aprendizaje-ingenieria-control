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
