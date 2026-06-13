---
titulo: Transformada de Clarke (αβ)
slug: transformada-clarke
categoria: fisica-modelado
tipo: tecnica
nivel: basico
proyectos: []
objetivos: [reducir tres magnitudes trifásicas a dos ejes estacionarios ortogonales]
tags: [clarke, alfa-beta, trifasico, transformada, basico, modelado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-12
relacionados: [marco-dq, control-vectorial, sistema-trifasico, potencia-instantanea-dq, componentes-simetricas]
referencias:
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
  - "Akagi, Watanabe, Aredes, Instantaneous Power Theory, Wiley 2007"
---

## Definición
Transformación lineal que lleva las tres magnitudes \( (a,b,c) \) a dos ejes ortogonales
**estacionarios** \( (\alpha,\beta) \) (más una componente homopolar \( 0 \)). Es el paso previo
a la rotación de [[marco-dq|Park]].

## Fundamento teórico
Con convención de **amplitud invariante** (factor 2/3):
$$ \begin{bmatrix}x_\alpha\\x_\beta\\x_0\end{bmatrix}=
   \frac{2}{3}\begin{bmatrix}1&-\tfrac12&-\tfrac12\\[2pt]0&\tfrac{\sqrt3}{2}&-\tfrac{\sqrt3}{2}\\[2pt]
   \tfrac12&\tfrac12&\tfrac12\end{bmatrix}
   \begin{bmatrix}x_a\\x_b\\x_c\end{bmatrix} $$
\( \alpha \) se alinea con la fase \( a \). En un sistema **equilibrado** \( x_0=0 \) y un fasor
giratorio en abc se vuelve un vector que gira en el plano \( \alpha\beta \) a frecuencia \( \omega \).
Con convención de **potencia invariante** el factor es \( \sqrt{2/3} \) (la matriz es ortonormal y
conserva la potencia). El homopolar captura el desequilibrio de modo común.

<div class="cfig"><img src="figuras/transformada-clarke-ejes.png" alt="ejes abc y alfa-beta de Clarke"><div class="cap">Clarke proyecta las tres fases (ejes a, b, c a 120°) sobre dos ejes ortogonales fijos: α (alineado con a) y β. Cualquier terna se reduce al vector espacial x = xα + j·xβ.</div></div>

## Cuándo y por qué se usa
Base del **control vectorial** y de la teoría de potencia instantánea. Permite trabajar con un
solo número complejo \( x_\alpha+jx_\beta \), simplifica el modelado y es donde operan PLLs y
resonantes (control PR en αβ sin necesidad de rotar a dq).

## Procedimiento (genérico)
1. Mide \( x_a,x_b,x_c \).
2. Aplica la matriz de Clarke (elige convención y mantenla en todo el proyecto).
3. Opera en αβ (control PR, PLL) o rota a dq con Park usando \( \theta \).
4. Antitransforma αβ→abc para las modulantes del PWM.

## Ejemplo de aplicación real
**Problema:** Corrientes trifásicas levemente desequilibradas: \( [i_a,i_b,i_c]=[1.0,\,-0.55,\,-0.45]\,\text{p.u.} \) Aplicar Clarke y detectar el desequilibrio en el plano αβ.

Componente α (amplitud invariante): \( i_\alpha=\tfrac{2}{3}[1.0-(-0.55)/2-(-0.45)/2]=\tfrac{2}{3}[1.0+0.275+0.225]=1.0\,\text{p.u.} \). Componente β: \( i_\beta=\tfrac{1}{\sqrt3}[i_b-i_c]=\tfrac{1}{\sqrt3}[-0.55+0.45]=-0.058\,\text{p.u.} \). En equilibrio perfecto \( i_\beta \) tendría magnitud igual a \( i_\alpha \) y desfase 90°; aquí \( |i_\beta|\approx0.058\ll i_\alpha=1.0 \): el desequilibrio es leve (~5.8 %). En el plano αβ la trayectoria describe una elipse en lugar de un círculo — cuanto más excéntrica, mayor el desequilibrio. Un detector [[dsogi-pll|DSOGI]] puede separar directamente las secuencias positiva y negativa desde αβ.

## Ejemplo de código
```python
import numpy as np
def clarke(a, b, c):                    # amplitud invariante
    al = (2/3)*(a - 0.5*b - 0.5*c)
    be = (2/3)*(np.sqrt(3)/2)*(b - c)
    return al, be
```

## Parámetros y valores típicos
Si las tres fases suman cero (sin neutro), \( x_0=0 \) y basta con \( \alpha,\beta \). Convención
de amplitud: el pico de fase se conserva (\( x_\alpha \) = pico de la fase a).

## Errores comunes
- Mezclar convención de amplitud y de potencia (factores \( \sqrt{2/3} \) vs 2/3).
- Descartar el homopolar cuando hay neutro o desequilibrio relevante.
- Confundir Clarke (eje fijo) con Park (eje giratorio).

## Conceptos relacionados
- [[marco-dq]] · [[control-vectorial]] · [[potencia-instantanea-dq]] · [[componentes-simetricas]]

## Referencias
- Yazdani, Iravani, 2010.
- Akagi, Watanabe, Aredes, *Instantaneous Power Theory*, 2007.
