---
titulo: Control vectorial (orientación de campo / red)
slug: control-vectorial
categoria: control
tipo: tecnica
nivel: avanzado
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [controlar corriente trifasica desacoplando par/flujo o P/Q en dq]
tags: [control-vectorial, FOC, dq, orientacion-de-campo, desacoplo]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [marco-dq, control-cascada, potencia-instantanea-dq, pll-srf]
referencias:
  - "Kazmierkowski, Krishnan, Blaabjerg, Control in Power Electronics, Academic Press 2002"
  - "Vas, Sensorless Vector and Direct Torque Control, Oxford 1998"
---

## Definición
Estrategia que controla las magnitudes trifásicas como **vectores espaciales** en un marco dq
**orientado** con una variable física (el flujo del rotor en máquinas, la tensión de red en
convertidores). Al orientar el marco, las dos componentes \( d \) y \( q \) controlan magnitudes
desacopladas.

## Fundamento teórico
Un sistema trifásico equilibrado se representa por un **vector espacial** que, llevado a dq con
el ángulo de orientación \( \theta \) (ver [[marco-dq]]), queda constante en régimen permanente.
Con la orientación adecuada:
- **Máquinas (FOC, Field-Oriented Control)**: marco alineado con el flujo de rotor. Entonces
  \( i_d \) controla el **flujo** y \( i_q \) controla el **par**:
  \( T \propto \psi\, i_q \). Se controla la máquina como una de continua.
- **Convertidor conectado a red**: marco alineado con la tensión de red (\( v_q=0 \), vía
  [[pll-srf]]). Entonces \( i_d \leftrightarrow P \) e \( i_q \leftrightarrow Q \)
  (ver [[potencia-instantanea-dq]]).

En ambos casos se cierran **lazos de corriente PI sobre \( i_d, i_q \)** con **desacoplo** de los
términos cruzados \( \pm\omega L\,i \) que introduce el marco giratorio. Es la base de los lazos
internos de casi todos los convertidores y accionamientos.

<div class="cfig"><img src="figuras/control-vectorial-orientacion.png" alt="diagrama de orientacion dq con la tension en el eje d"><div class="cap">Al orientar el marco dq con la tensión de red ($v_q=0$, vía PLL), la corriente se descompone en $i_d$ —que gobierna la potencia activa P— e $i_q$ —que gobierna la reactiva Q—, controlables de forma independiente con dos PI. En máquinas el marco se alinea con el flujo y entonces $i_d$ es flujo e $i_q$ es par.</div></div>

## 1 — Orientación del marco dq: por qué \( v_d=V \), \( v_q=0 \) desacopla P de Q

**Paso 1 — vector espacial de tensión de red en αβ.** La red trifásica equilibrada produce una tensión \( \mathbf{v}_{red}(t) \) que, transformada con Clarke, es un fasor giratorio de módulo \( V \) y ángulo \( \theta(t)=\omega t \). En αβ:

$$ \mathbf{v}_{\alpha\beta} = V\,e^{j\theta} $$

**Paso 2 — elección del ángulo de orientación.** Se lleva ese fasor al marco dq girante con el mismo \( \theta \) extraído por la PLL (ver [[pll-srf]]). La transformada de Park alinea el eje d con \( \mathbf{v}_{red} \):

$$ \begin{pmatrix}v_d\\v_q\end{pmatrix} = \begin{pmatrix}\cos\theta & \sin\theta\\-\sin\theta & \cos\theta\end{pmatrix}\begin{pmatrix}v_\alpha\\v_\beta\end{pmatrix} = \begin{pmatrix}V\\0\end{pmatrix} $$

El vector de tensión cae exactamente sobre el eje d, de modo que \( v_d = V \) y \( v_q = 0 \) en régimen permanente.

**Paso 3 — potencia instantánea en dq.** Con la convención de potencia instantánea trifásica (ver [[potencia-instantanea-dq]]) y el factor \( \tfrac{3}{2} \) de la transformada de Park normalizada:

$$ P = \tfrac{3}{2}(v_d\,i_d + v_q\,i_q),\qquad Q = \tfrac{3}{2}(v_q\,i_d - v_d\,i_q) $$

**Paso 4 — sustitución de la orientación.** Sustituyendo \( v_d=V \), \( v_q=0 \):

$$ \boxed{P = \tfrac{3}{2}\,V\,i_d}, \qquad \boxed{Q = -\tfrac{3}{2}\,V\,i_q} $$

**Conclusión.** La potencia activa depende únicamente de \( i_d \) y la reactiva únicamente de \( i_q \). Cerrar un lazo PI sobre \( i_d \) controla P sin perturbar Q, y viceversa: el control vectorial orientado a la tensión de red produce **desacoplo P–Q natural** a partir de la geometría de la transformada, no de cancelaciones complicadas.

## Cuándo y por qué se usa
En accionamientos de máquinas AC (PMSM, inducción) y en convertidores conectados a red. Permite
control independiente y de alto desempeño de par/flujo o de P/Q.

## Procedimiento (genérico)
1. Determina el ángulo de orientación \( \theta \) (estimador de flujo en FOC; PLL en red).
2. Mide corrientes y transfórmalas a dq con \( \theta \) (Clarke + Park).
3. Cierra lazos PI sobre \( i_d, i_q \) con **desacoplo** \( \pm\omega L \) y feedforward.
4. Antitransforma la tensión de referencia (dq→abc) y genera el PWM.
5. Sintoniza los PI por ancho de banda (ver [[control-cascada]], [[sintonia-pi-pid]]).

## Ejemplo de código
```python
# lazo de corriente vectorial (dq) con desacoplo
e_d, e_q = id_ref - id, iq_ref - iq
vd = Kp*e_d + Ki*xd - w*L*iq     # desacoplo cruzado
vq = Kp*e_q + Ki*xq + w*L*id
```

## Parámetros y valores típicos
Ancho de banda del lazo de corriente ≈ \( f_{sw}/10 \). En FOC, \( i_d=0 \) (PMSM de imanes
superficiales) para par máximo por amperio; debilitamiento de campo con \( i_d<0 \) a alta velocidad.

## Errores comunes
- Orientación incorrecta (error en \( \theta \)) → acoplamiento par/flujo o P/Q.
- Olvidar el desacoplo \( \pm\omega L \) → lazos d y q acoplados, peor desempeño.

## Uso en proyectos
- **01/02**: los lazos de corriente dq con desacoplo son control vectorial aplicado a un
  convertidor de red (orientación a la tensión por la PLL en el GFL). El FOC de máquina es
  candidato a proyecto propio.

## Conceptos relacionados
- [[marco-dq]] · [[control-cascada]] · [[potencia-instantanea-dq]] · [[pll-srf]]

## Referencias
- Kazmierkowski et al., *Control in Power Electronics*, 2002.
