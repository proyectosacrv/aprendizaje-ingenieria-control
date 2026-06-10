---
titulo: Estabilidad (concepto)
slug: estabilidad-bibo
categoria: control
tipo: concepto
nivel: basico
proyectos: []
objetivos: [definir que significa que un sistema sea estable]
tags: [estabilidad, BIBO, polos, equilibrio, basico]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [polos-ceros, margenes-estabilidad, analisis-modal, linealizacion-teoria]
referencias:
  - "Khalil, Nonlinear Systems, Prentice Hall 2002"
---

## Definición
Un sistema es **estable** si su respuesta no crece sin límite. La idea básica: ante una entrada
acotada, la salida permanece acotada (**estabilidad BIBO**); y ante una perturbación, el sistema
vuelve (o no se aleja) de su punto de equilibrio.

## Fundamento teórico
Para un sistema **lineal** (o linealizado), la condición es sencilla y exacta:
$$ \text{estable} \iff \text{todos los polos tienen parte real negativa} $$
(autovalores de \( A \) en el semiplano izquierdo). Tipos de estabilidad:
- **Asintóticamente estable**: vuelve al equilibrio (polos con \( \mathrm{Re}<0 \)).
- **Marginal**: ni crece ni decae (polos sobre el eje imaginario; p.ej. un integrador).
- **Inestable**: al menos un polo con \( \mathrm{Re}>0 \).
En sistemas **no lineales**, la estabilidad es **local** (depende del punto de operación) y se
estudia por linealización (ver [[linealizacion-teoria]]) o por métodos de Lyapunov. No basta con
ser estable: interesa el **margen** (cuánto se puede variar antes de inestabilizar).

## Cuándo y por qué se usa
Es el primer requisito de cualquier diseño de control: un sistema inestable es inutilizable o
peligroso. Toda evaluación empieza por comprobar estabilidad.

## Procedimiento (genérico)
1. Obtén el modelo lineal (o lineliza en el punto de operación).
2. Calcula los polos / autovalores.
3. Estable si todos tienen parte real negativa.
4. Si es no lineal, recuerda que la conclusión es local; valida con simulación de gran señal.

## Ejemplo de aplicación real
**Problema:** Dos buses DC con modelos linealizados: \( G_1(s)=10/(s^2+2s+5) \) (carga resistiva) y \( G_2(s)=10/(s^2-2s+5) \) (carga CPL no compensada). Determinar cuál es BIBO estable.

Para \( G_1 \): polos en \( s=-1\pm j2 \), parte real \( -1<0 \) → **BIBO estable**. Ante un escalón acotado la respuesta oscila y se asienta. Para \( G_2 \): polos en \( s=+1\pm j2 \), parte real \( +1>0 \) → **no BIBO estable**. Ante el mismo escalón, la respuesta crece como \( e^t\cos(2t) \) hasta que alguna limitación física (saturación, protección) interviene. El diagnóstico toma segundos con `np.linalg.eigvals(A)`: cualquier valor propio con parte real positiva indica inestabilidad y obliga a revisar el control (resistencia virtual, lazo de tensión).

## Ejemplo de código
```python
import numpy as np
estable = np.all(np.linalg.eigvals(A).real < 0)
```

## Parámetros y valores típicos
Se busca margen: no basta \( \mathrm{Re}<0 \), interesa que sea bastante negativo y con
amortiguamiento suficiente (ver [[margenes-estabilidad]]).

## Errores comunes
- Confundir estabilidad con buen desempeño (un sistema estable puede ser lentísimo u oscilatorio).
- Extender la estabilidad local de un linealizado a gran señal (saturaciones, faltas).

## Conceptos relacionados
- [[polos-ceros]] · [[margenes-estabilidad]] · [[analisis-modal]] · [[linealizacion-teoria]]

## Referencias
- Khalil, *Nonlinear Systems*, 2002.
