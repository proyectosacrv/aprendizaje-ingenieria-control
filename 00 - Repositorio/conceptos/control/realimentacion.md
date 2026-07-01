---
titulo: Realimentación (lazo abierto y cerrado)
slug: realimentacion
categoria: control
tipo: concepto
nivel: basico
proyectos: []
objetivos: [entender por que se realimenta y que aporta el lazo cerrado]
tags: [realimentacion, lazo-cerrado, feedback, error, basico]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-30
relacionados: [funcion-transferencia, controlador-pid, funciones-sensibilidad, margenes-estabilidad]
referencias:
  - "Aström, Murray, Feedback Systems, Princeton 2008"
---

## Definición
**Realimentar** es medir la salida, compararla con la referencia y actuar sobre la diferencia
(el **error**). El **lazo cerrado** usa esa medida; el **lazo abierto** actúa sin medir. La
realimentación es la idea central del control automático.

## Fundamento teórico
Con planta \( G(s) \) y controlador \( C(s) \) en lazo cerrado con realimentación unitaria, la
transferencia referencia → salida es:
$$ T(s) = \frac{C(s)G(s)}{1 + C(s)G(s)} $$
y el error responde según la **sensibilidad** \( S(s)=1/(1+CG) \). Lo que aporta el lazo cerrado:
- **Reduce el error** ante perturbaciones y errores de modelo (si la ganancia de lazo \( CG \) es
  grande, \( S \) es pequeña).
- **Modifica la dinámica** (mueve los polos) y puede estabilizar una planta inestable.
- **Riesgo**: una ganancia mal puesta puede **inestabilizar** (de ahí los márgenes).

El lazo abierto es simple pero no corrige perturbaciones ni errores de modelo.

<div class="cfig"><img src="figuras/realimentacion-lazo.png" alt="lazo de control realimentado"><div class="cap">Lazo cerrado: el error e=r−y entra al controlador C(s), que actúa sobre la planta G(s); la salida se mide y realimenta (signo −). Es lo que permite corregir perturbaciones y errores de modelo.</div></div>

## 1 — Cómo sale \( T=L/(1+L) \) del diagrama
**Paso 1 — escribir las relaciones del lazo.** En el lazo cerrado con realimentación unitaria hay tres ecuaciones de bloques (ver [[diagrama-bloques]]): el error es la resta, la salida es la cadena directa actuando sobre el error, y abreviamos la **ganancia de lazo** \( L(s)\equiv C(s)G(s) \):

$$ E=R-Y,\qquad Y=C\,G\,E = L\,E $$

**Paso 2 — eliminar el error.** Sustituyendo \( E=R-Y \) en \( Y=L\,E \):

$$ Y = L\,(R-Y) = L\,R - L\,Y $$

**Paso 3 — agrupar \( Y \).** Pasando \( L\,Y \) a la izquierda y sacando factor común:

$$ Y + L\,Y = L\,R \;\Longrightarrow\; Y(1+L)=L\,R $$

de donde la transferencia referencia → salida (la **función de transferencia complementaria**):

$$ \boxed{\;T(s)=\frac{Y}{R}=\frac{L}{1+L}=\frac{CG}{1+CG}\;} $$

El denominador \( 1+L=0 \) es la **ecuación característica**: sus raíces son los polos del lazo cerrado. De ahí que realimentar **mueva los polos** (y pueda estabilizar o inestabilizar según \( L \)).

## 2 — La sensibilidad \( S \) y la identidad \( S+T=1 \)
**Paso 1 — transferencia referencia → error.** Partiendo de \( E=R-Y \) y \( Y=T\,R \) del apartado anterior:

$$ E = R - T\,R = (1-T)\,R $$

**Paso 2 — sustituir \( T \) y combinar fracciones.** Con \( T=\dfrac{L}{1+L} \), poniendo \( 1=\dfrac{1+L}{1+L} \):

$$ 1-T = \frac{1+L}{1+L}-\frac{L}{1+L} = \frac{1+L-L}{1+L}=\frac{1}{1+L} $$

Se define esa transferencia como **sensibilidad** \( S \):

$$ \boxed{\;S(s)=\frac{E}{R}=\frac{1}{1+L},\qquad S+T=1\;} $$

**Paso 3 — interpretar.** El error en el lazo es \( E=S\,R \). Si la ganancia de lazo es **grande** en una frecuencia (\( |L|\gg 1 \)), entonces \( S\approx 1/L\to 0 \): el error se reduce en ese rango — por eso el integrador del PI, que hace \( |L|\to\infty \) en continua, **anula el error en régimen** ante escalón (ver [[error-regimen-permanente]]). La identidad \( S+T=1 \) impone el compromiso fundamental: no se puede hacer \( S \) pequeña (rechazo) y \( T\approx 1 \) (seguimiento) más allá de lo que suman a 1 en cada frecuencia.

## Cuándo y por qué se usa
Siempre que se quiera precisión y robustez ante incertidumbre: regular tensión, corriente,
velocidad. La práctica totalidad del control de convertidores es en lazo cerrado.

## Procedimiento (genérico)
1. Mide la salida y forma el error \( e = \text{ref} - \text{salida} \).
2. El controlador \( C(s) \) actúa sobre \( e \).
3. Diseña \( C \) para que \( T \) cumpla las especificaciones y el lazo sea estable (márgenes).
4. Verifica robustez (sensibilidad, márgenes).

## Ejemplo de aplicación real
**Problema:** Bus DC con carga CPL (resistencia diferencial negativa \( -R_{neg}=-200\,\Omega \)): el polo del modelo linealizado está en \( s=1/(C\cdot R_{neg})>0 \) (inestable). Diseñar la realimentación mínima para estabilizarlo.

Planta: \( G(s)=1/(Cs-1/R_{neg}) \) con \( C=10\,\text{mF} \). Con realimentación proporcional \( K \), el polo del lazo cerrado es \( p_{cl}=(1/R_{neg}-K)/C \). Para estabilizar: \( K>1/R_{neg}=0.005 \). Con \( K=0.01 \): \( p_{cl}=(−0.005−0.01)/0.01=−1.5\,\text{s}^{-1} \). Sistema estable. En la práctica se implementa como una **resistencia virtual activa**: el control inyecta potencia adicional proporcional a \( \Delta V_{dc} \), emulando una resistencia de amortiguamiento que no disipa calor.

## Ejemplo de código
```python
import control as ct
L = C * G                          # ganancia de lazo abierto
T = ct.feedback(L, 1)              # lazo cerrado con realimentacion unitaria
```

## Parámetros y valores típicos
Ganancia de lazo alta en baja frecuencia (buen seguimiento), baja en alta (robustez/ruido).

## Errores comunes
- Subir la ganancia para reducir el error sin mirar la estabilidad (margen de fase).
- Confiar en lazo abierto cuando hay perturbaciones o incertidumbre.

## Conceptos relacionados
- [[funcion-transferencia]] · [[controlador-pid]] · [[funciones-sensibilidad]] · [[margenes-estabilidad]]

## Referencias
- Aström, Murray, *Feedback Systems*, 2008.
