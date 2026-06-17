---
titulo: Transformadas de Clarke y Park (marco αβ y dq)
slug: marco-dq
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [reducir las tres magnitudes trifásicas a dos ejes, llevar las senoides a continua y desacoplar el control]
tags: [clarke, park, alfa-beta, dq, transformada, acoplamiento, homopolar, trifasico, modelado]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-16
relacionados: [desacoplo-dq, potencia-instantanea-dq, componentes-simetricas, control-cascada, control-vectorial, filtro-lcl, pll-srf]
referencias:
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
  - "Akagi, Watanabe, Aredes, Instantaneous Power Theory, Wiley 2007"
---

## Definición
Cadena de dos transformaciones que reducen las tres magnitudes trifásicas (abc) primero a dos ejes ortogonales estacionarios (alfa-beta, transformada de Clarke) y luego a un marco giratorio sincronizado con la red (dq, transformada de Park). El resultado clave: en régimen permanente las senoides de 50 Hz se convierten en constantes, lo que permite usar PI con error nulo en continua y analizar el sistema trifásico como uno de continua. Esta ficha cubre las dos transformadas porque Clarke es simplemente el primer paso de Park; se separan solo cuando el control vive en alfa-beta (controladores resonantes, algunas PLL).

## La idea en una figura
Montarse en un marco que gira a la misma velocidad que las senoides las convierte en valores DC:

<div class="cfig"><img src="figuras/marco-dq-park.png" alt="senoides trifasicas que en dq se vuelven constantes"><div class="cap">Las tres senoides del marco abc (izquierda) se vuelven dos constantes en el marco dq (derecha): con el eje d alineado con la tensión, vd es la amplitud y vq≈0.</div></div>

## Paso 1 — Clarke (abc → αβ)
Transformación lineal que proyecta las tres fases a dos ejes ortogonales fijos (más una componente homopolar 0). Con convención de amplitud invariante (factor 2/3):

- x_alpha = (2/3)·(xa − xb/2 − xc/2)
- x_beta  = (2/3)·(raiz(3)/2)·(xb − xc)
- x_0     = (1/3)·(xa + xb + xc)

El eje alpha se alinea con la fase a. En un sistema equilibrado x_0 = 0 y un fasor giratorio en abc se vuelve un vector que gira en el plano alfa-beta a frecuencia omega. Con convención de potencia invariante el factor es raiz(2/3) (matriz ortonormal que conserva la potencia). El homopolar captura el desequilibrio de modo común. Trabajar en alfa-beta permite usar un solo número complejo x_alpha + j·x_beta, y es donde operan los controladores resonantes (PR en alfa-beta sin necesidad de rotar a dq) y algunas PLL.

<div class="cfig"><img src="figuras/transformada-clarke-ejes.png" alt="ejes abc y alfa-beta de Clarke"><div class="cap">Clarke proyecta las tres fases (ejes a, b, c a 120°) sobre dos ejes ortogonales fijos: α (alineado con a) y β. Cualquier terna se reduce al vector espacial x = xα + j·xβ.</div></div>

## Paso 2 — Park (αβ → dq)
Rota los ejes fijos alfa-beta al marco que gira con el ángulo theta = ∫omega·dt:

- xd = cos(theta)·x_alpha + sin(theta)·x_beta
- xq = −sin(theta)·x_alpha + cos(theta)·x_beta

Con el eje d alineado con la tensión, en permanente vd es la amplitud y vq ≈ 0.

### El acoplamiento cruzado (por qué aparece el término omega·J)
Visto como vector complejo, x_alfabeta = x_dq·e^(j·theta). Al derivar un inductor v = L·di/dt y sustituir, la regla del producto sobre e^(j·theta) (con dtheta/dt = omega y d/dt de e^(j·theta) = j·omega·e^(j·theta)) añade un término extra:

v_dq = L·d(i_dq)/dt + j·omega·L·i_dq

En forma matricial real, j equivale a J = [[0, −1],[1, 0]] (rotar 90°), así que cada elemento reactivo arrastra un término omega·J que cruza d↔q: omega·L en bobinas, omega·C en condensadores. El control lo elimina por desacoplo (ver [[desacoplo-dq]]).

> A resaltar: ese término no existe en trifásico; nace solo de girar el marco (la "fuerza de Coriolis" del marco dq). Es el responsable de los sub-bloques 2×2 antidiagonales que se ven en la matriz de estado de los modelos dq.

## Cuándo y por qué se usa
En todo control de convertidores trifásicos y máquinas. El premio: referencias constantes → PI sin error en permanente más linealización en torno a un punto fijo. En grid-forming el ángulo theta lo genera el propio control (droop/VSM); en grid-following lo da la PLL (ver [[pll-srf]]). Se trabaja en alfa-beta (sin el paso de Park) cuando se usan controladores resonantes o teoría de potencia instantánea.

## Procedimiento de diseño (genérico)
1. Define el ángulo theta del marco (de la PLL en GFL, del droop/VSM en GFM).
2. Aplica Clarke y Park a tensiones y corrientes medidas (elige convención —amplitud o potencia invariante— y mantenla en todo el proyecto).
3. Diseña el control en dq (referencias constantes, PI sin error), con desacoplo de los términos omega·J. Si usas resonantes, quédate en alfa-beta.
4. Antitransforma (dq→alfa-beta→abc) para generar las modulantes del PWM.
5. Cuida el alineamiento (eje d con la tensión) y la convención.

## Ejemplo de código
```python
import numpy as np

def clarke(a, b, c):                          # amplitud invariante
    al = (2/3)*(a - 0.5*b - 0.5*c)
    be = (2/3)*(np.sqrt(3)/2)*(b - c)
    return al, be

def park(alpha, beta, th):
    c, s = np.cos(th), np.sin(th)
    return c*alpha + s*beta, -s*alpha + c*beta   # (d, q)
```

## Ejemplos de aplicación real
Detección de desequilibrio con Clarke. Corrientes [ia, ib, ic] = [1.0, −0.55, −0.45] p.u. Componente alpha (amplitud invariante): i_alpha = (2/3)· [1.0 + 0.275 + 0.225] = 1.0 p.u. Componente beta: i_beta = (1/raiz(3))· (ib − ic) = (1/raiz(3))· (−0.10) = −0.058 p.u. En equilibrio perfecto |i_beta| igualaría a i_alpha con desfase 90°; aquí |i_beta| ≈ 0.058 << 1.0, desequilibrio leve (~5.8 %). En el plano alfa-beta la trayectoria describe una elipse en vez de un círculo; cuanto más excéntrica, mayor el desequilibrio. Un DSOGI (ver [[pll-srf]]) separa directamente las secuencias positiva y negativa desde alfa-beta.

## Parámetros y valores típicos
- Si las tres fases suman cero (sin neutro), x_0 = 0 y basta con alfa-beta. Convención de amplitud: el pico de fase se conserva (x_alpha = pico de la fase a).
- Convención de amplitud usada en el proyecto: V0 = Vll·raiz(2/3). Esta elección fija el factor 3/2 de la potencia trifásica P = (3/2)·(vd·id + vq·iq).

## Errores comunes
- Mezclar convención de amplitud (factor 2/3) y de potencia (raiz(2/3)) → factores 3/2 mal en la potencia.
- Descartar el homopolar cuando hay neutro o desequilibrio relevante.
- Confundir Clarke (eje fijo) con Park (eje giratorio).
- Olvidar los términos cruzados omega·J al modelar → modelo dq incorrecto.
- No alinear bien el eje d con la tensión → medidas y arranque defectuosos.

## Uso en proyectos
- 01 - GFM-Impedance (modelado): todo el modelo (15 estados) vive en dq. Además se usan dos marcos (red y control) ligados por el ángulo delta.
- 02 - GFL-Impedance: el marco dq se alinea con la red mediante la PLL.

## Conceptos relacionados
- [[desacoplo-dq]] · [[potencia-instantanea-dq]] · [[componentes-simetricas]] · [[control-cascada]] · [[control-vectorial]] · [[filtro-lcl]] · [[pll-srf]]

## Referencias
- Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010.
- Akagi, Watanabe, Aredes, Instantaneous Power Theory, Wiley 2007.
