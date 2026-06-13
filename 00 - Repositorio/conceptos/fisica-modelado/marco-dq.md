---
titulo: Marco de referencia dq (Park/Clarke)
slug: marco-dq
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [modelar el sistema trifasico como continuo y desacoplar el control]
tags: [park, clarke, dq, transformada, acoplamiento, trifasico]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-11
relacionados: [transformada-clarke, desacoplo-dq, potencia-instantanea-dq, control-cascada, filtro-lcl]
referencias:
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
---

## Definición
Transformación que lleva las magnitudes trifásicas (abc) a un **marco giratorio** de dos ejes
(d, q) sincronizado con la frecuencia de red. En régimen permanente las senoides de 50 Hz se
convierten en **constantes** → permite usar PI con error nulo en continua y analizar el sistema
como uno de continua.

## La idea en una figura
Montarse en un marco que gira a la misma velocidad que las senoides las convierte en valores DC:

<div class="cfig"><img src="figuras/marco-dq-park.png" alt="senoides trifasicas que en dq se vuelven constantes"><div class="cap">Las tres senoides del marco abc (izquierda) se vuelven dos constantes en el marco dq (derecha): con el eje d alineado con la tensión, vd es la amplitud y vq≈0.</div></div>

## Fundamento teórico — de dónde se sale
Son **dos pasos** encadenados con el ángulo \( \theta=\int\omega\,dt \):

**1) Clarke (abc → αβ):** proyecta las tres fases a dos ejes ortogonales **fijos**:
$$ \begin{bmatrix}x_\alpha\\x_\beta\end{bmatrix}=\frac{2}{3}
   \begin{bmatrix}1&-\tfrac12&-\tfrac12\\[2pt]0&\tfrac{\sqrt3}{2}&-\tfrac{\sqrt3}{2}\end{bmatrix}
   \begin{bmatrix}x_a\\x_b\\x_c\end{bmatrix} $$

**2) Park (αβ → dq):** rota esos ejes al marco que gira con \( \theta \):
$$ \begin{bmatrix}x_d\\x_q\end{bmatrix}=
   \begin{bmatrix}\cos\theta&\sin\theta\\-\sin\theta&\cos\theta\end{bmatrix}
   \begin{bmatrix}x_\alpha\\x_\beta\end{bmatrix} $$

### El acoplamiento cruzado (por qué aparece el término \( \omega\mathbf{J} \))
Visto como vector complejo, \( \vec{x}_{\alpha\beta}=\vec{x}_{dq}\,e^{j\theta} \). Al derivar un
inductor \( v=L\,di/dt \) y sustituir, la **regla del producto** sobre \( e^{j\theta} \) (con
\( \dot\theta=\omega \) y \( \tfrac{d}{dt}e^{j\theta}=j\omega e^{j\theta} \)) añade un término extra:
$$ v_{dq}=L\frac{d\,i_{dq}}{dt}+\,j\omega L\,i_{dq} $$
En forma matricial real, \( j \) equivale a \( \mathbf{J}=\left[\begin{smallmatrix}0&-1\\1&0\end{smallmatrix}\right] \)
(rotar 90°), así que cada elemento reactivo arrastra un término \( \omega\mathbf{J} \) que **cruza
d↔q**: \( \omega L \) en bobinas, \( \omega C \) en condensadores. El control lo elimina por
**desacoplo** (ver [[desacoplo-dq]]).

> **A resaltar:** ese término no existe en trifásico; nace solo de **girar el marco** (la "fuerza de
> Coriolis" del marco dq). Es el responsable de los sub-bloques 2×2 antidiagonales que se ven en la
> matriz de estado de los modelos dq.

## Cuándo y por qué se usa
En todo control de convertidores trifásicos y máquinas. El premio: referencias constantes → PI sin
error en permanente + linealización en torno a un punto fijo. En grid-forming el ángulo \( \theta \)
lo genera el propio control (droop/VSM); en grid-following lo da la PLL ([[pll-srf]]).

## Procedimiento de diseño (genérico)
1. Define el ángulo \( \theta \) del marco (de la PLL en GFL, del droop/VSM en GFM).
2. Aplica Clarke y Park a tensiones y corrientes medidas.
3. Diseña el control en dq (referencias constantes, PI sin error), **con desacoplo** de los términos
   \( \omega\mathbf{J} \).
4. Antitransforma (dq→abc) para generar las modulantes del PWM.
5. Cuida la convención (amplitud vs potencia invariante) y el alineamiento (eje d con la tensión).

## Ejemplo de código
```python
def park(alpha, beta, th):
    c, s = np.cos(th), np.sin(th)
    return c*alpha + s*beta, -s*alpha + c*beta   # (d, q)
```

## Parámetros y valores típicos
Convención de amplitud (pico de fase) usada en el proyecto: \( V_0=V_{ll}\sqrt{2/3} \). Esta elección
fija el factor \( 3/2 \) de la potencia trifásica \( P=\tfrac32(v_d i_d+v_q i_q) \).

## Errores comunes
- Mezclar convenciones (amplitud vs potencia invariante) → factores \( 3/2 \) mal en la potencia.
- Olvidar los términos cruzados \( \omega\mathbf{J} \) al modelar → modelo dq incorrecto.
- No alinear bien el eje d con la tensión → medidas y arranque defectuosos.

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: modelado): todo el modelo (15 estados) vive en dq. Además se usan
  **dos** marcos (red y control) ligados por el ángulo \( \delta \).
- **02 - GFL-Impedance**: el marco dq se alinea con la red mediante la PLL.

## Conceptos relacionados
- [[transformada-clarke]] · [[desacoplo-dq]] · [[potencia-instantanea-dq]] · [[control-cascada]] · [[filtro-lcl]]

## Referencias
- Yazdani, Iravani, 2010.
