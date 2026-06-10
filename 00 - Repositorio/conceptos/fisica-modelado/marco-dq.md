---
titulo: Marco de referencia dq (Park/Clarke)
slug: marco-dq
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [modelar el sistema trifasico como continuo y desacoplar el control]
tags: [park, clarke, dq, transformada, trifasico]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [potencia-instantanea-dq, control-cascada, filtro-lcl]
referencias:
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
---

## Definición
Transformación que lleva las magnitudes trifásicas (abc) a un marco giratorio de dos ejes
(d, q) sincronizado con la frecuencia de red. En régimen permanente, las senoides de 50 Hz se
convierten en **constantes** → permite usar PI y analizar el sistema como uno de continua.

## Fundamento teórico
Clarke (abc→αβ) y Park (αβ→dq) con ángulo \( \theta=\int\omega\,dt \):
$$ \begin{bmatrix}x_d\\x_q\end{bmatrix}=
   \begin{bmatrix}\cos\theta&\sin\theta\\-\sin\theta&\cos\theta\end{bmatrix}
   \begin{bmatrix}x_\alpha\\x_\beta\end{bmatrix} $$
Al derivar en el marco giratorio aparece el **acoplamiento cruzado** \( \pm\omega \) entre d y q
(la "fuerza de Coriolis" del marco): por eso los modelos dq llevan términos \( \pm\omega L i \),
\( \pm\omega C v \).

## Cuándo y por qué se usa
En todo control de convertidores trifásicos y máquinas. En grid-forming, el ángulo \( \theta \)
lo genera el propio control (droop/VSM), no una PLL.

## Procedimiento de diseño (genérico)
1. Define el ángulo \( \theta \) del marco (de la PLL en GFL, del droop/VSM en GFM).
2. Aplica Clarke y Park a tensiones y corrientes medidas.
3. Diseña el control en dq (referencias constantes, PI sin error en permanente).
4. Antitransforma (dq→abc) para generar las modulantes del PWM.
5. Cuida la convención (amplitud vs potencia invariante) y el alineamiento (eje d con tensión).

## Ejemplo de código
```python
def park(alpha, beta, th):
    c, s = np.cos(th), np.sin(th)
    return c*alpha + s*beta, -s*alpha + c*beta   # (d, q)
```

## Parámetros y valores típicos
Convención de amplitud (pico de fase) usada en el proyecto: \( V_0=V_{ll}\sqrt{2/3} \).

## Errores comunes
- Mezclar convenciones (amplitud vs potencia invariante) → factores 3/2 mal en la potencia.
- Olvidar los términos cruzados \( \pm\omega \) al modelar.

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: modelado): todo el modelo (15 estados) vive en dq. Además
  se usan **dos** marcos (red y control) ligados por el ángulo \( \delta \).

## Conceptos relacionados
- [[potencia-instantanea-dq]] · [[control-cascada]] · [[filtro-lcl]]

## Referencias
- Yazdani, Iravani, 2010.
