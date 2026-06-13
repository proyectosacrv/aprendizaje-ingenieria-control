---
titulo: Criterio de Middlebrook (estabilidad de cascadas por impedancia)
slug: criterio-middlebrook
categoria: metodologia
tipo: metodo
nivel: avanzado
proyectos: [03-DataCenter-IA]
objetivos: [evaluar la estabilidad de una cascada fuente-carga por sus impedancias]
tags: [middlebrook, impedancia, cascada, bus-dc, estabilidad]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [estabilidad-bus-dc-cpl, carga-potencia-constante-cpl, impedancia-salida-estabilidad, no-pasividad-resistencia-negativa]
referencias:
  - "Middlebrook, Input Filter Considerations in Design of Switching Regulators, IEEE 1976"
---

## Definición
Criterio para decidir la estabilidad de una **cascada fuente → carga** (p.ej. filtro/fuente que
alimenta un convertidor) a partir del cociente de sus impedancias, sin reconstruir el sistema
completo. Es el análogo DC del criterio de estabilidad por impedancia en AC.

## Fundamento teórico
Sea \( Z_{fuente}(s) \) la impedancia de salida de la fuente y \( Z_{carga}(s) \) la impedancia
de entrada de la carga. Si ambas son estables por separado, la cascada es estable según el
Nyquist del **cociente**:
$$ T_m(s) = \frac{Z_{fuente}(s)}{Z_{carga}(s)} $$
El **criterio de Middlebrook** (condición suficiente y conservadora) exige:
$$ |Z_{fuente}(j\omega)| \ll |Z_{carga}(j\omega)| \quad \forall \omega $$
es decir, que la impedancia de salida de la fuente sea mucho menor que la de entrada de la carga.
Con una [[carga-potencia-constante-cpl|CPL]], \( Z_{carga}=-V^2/P \) (resistencia negativa,
\( |Z|=V^2/P \)): al subir \( P \), \( |Z_{carga}| \) baja y, cuando cae por debajo del pico de
resonancia de \( |Z_{fuente}| \), el sistema se inestabiliza. Existen criterios menos
conservadores (GMPM, banda prohibida, ESAC) que relajan el de Middlebrook.

<div class="cfig"><img src="figuras/criterio-middlebrook-impedancias.png" alt="impedancia de fuente con pico de resonancia frente a impedancia de carga CPL"><div class="cap">La fuente (filtro LC) tiene un pico de impedancia en su resonancia; la carga CPL presenta $|Z_{carga}|=V^2/P$, una línea horizontal que baja al subir la potencia. Mientras $|Z_{carga}|$ quede por encima del pico hay margen; cuando la potencia la hace cortar el pico, se viola el criterio y el bus se inestabiliza. Da la potencia límite de forma modular.</div></div>

## Cuándo y por qué se usa
En sistemas DC en cascada (microrredes DC, data centers, alimentación distribuida) y en filtros
de entrada de convertidores. Permite diseñar de forma modular: caracterizar fuente y carga por
separado.

## Procedimiento (genérico)
1. Obtén \( Z_{fuente}(j\omega) \) (impedancia de salida del filtro/fuente).
2. Obtén \( Z_{carga}(j\omega) \) (de la CPL: \( -V^2/P \)).
3. Compara magnitudes: si \( |Z_{fuente}| \) supera \( |Z_{carga}| \) en alguna banda → riesgo.
4. Para el límite exacto, aplica Nyquist a \( T_m=Z_{fuente}/Z_{carga} \).
5. Si no cumple: baja \( |Z_{fuente}| \) (más \( C \), amortiguamiento) o sube \( |Z_{carga}| \).

## Ejemplo de código
```python
# pico de |Z_fuente| vs |Z_carga| = V^2/P  -> potencia limite
P_lim = V**2 / np.max(np.abs(Z_fuente))
```

## Parámetros y valores típicos
Margen recomendado: \( |Z_{fuente}| \) varias veces menor que \( |Z_{carga}| \) en la resonancia.
Criterio conservador (deja margen de diseño).

## Errores comunes
- Aplicar Middlebrook (muy conservador) y sobredimensionar; para el límite real usar Nyquist del cociente.
- Olvidar que \( |Z_{carga}| \) de la CPL baja al subir la potencia.

## Uso en proyectos
- **03 - DataCenter-IA**: pico de \( |Z_{fuente}|\approx 4.8 \) Ω → potencia límite \( V^2/4.8 \approx 134 \)
  kW, coincide con la \( P_{crit} \) por autovalores (128 kW). Validación cruzada de la Fase 2.

## Conceptos relacionados
- [[estabilidad-bus-dc-cpl]] · [[carga-potencia-constante-cpl]] · [[impedancia-salida-estabilidad]]

## Referencias
- Middlebrook, *Input Filter Considerations...*, IEEE 1976.
