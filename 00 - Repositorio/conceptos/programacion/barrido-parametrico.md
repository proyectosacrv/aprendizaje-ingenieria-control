---
titulo: Barrido paramétrico y sensibilidad numérica
slug: barrido-parametrico
categoria: programacion
tipo: tecnica
nivel: intermedio
proyectos: []
objetivos: [evaluar cómo cambian polos y márgenes al variar parámetros del sistema]
tags: [barrido, sweep, sensibilidad, autovalores, robustez, intermedio, programacion]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-30
relacionados: [robustez-parametrica, respuesta-frecuencia-ss, analisis-modal, margenes-estabilidad, red-thevenin-scr]
referencias:
  - "Skogestad, Postlethwaite, Multivariable Feedback Control, Wiley 2005"
  - "Saltelli et al., Global Sensitivity Analysis, Wiley 2008"
---

## Definición
Procedimiento numérico que **recalcula indicadores de estabilidad/desempeño** (autovalores,
márgenes, pico de sensibilidad \( M_s \)) mientras se **varía uno o varios parámetros** del modelo,
para localizar el caso crítico y cuantificar la robustez. Es la implementación práctica de la
[[robustez-parametrica]].

## Fundamento teórico
Dado el modelo \( A(\theta) \) (o \( L(s;\theta) \)) función de un parámetro \( \theta \) (SCR de
red, \( L \), \( C \), ganancia, retardo):
- **Barrido 1-D:** se recorre \( \theta\in[\theta_{min},\theta_{max}] \) y se calculan
  \( \lambda_i(\theta)=\mathrm{eig}\,A(\theta) \) → **root-loci numérico** (trayectoria de polos).
- **Barrido 2-D:** dos parámetros → **mapa de calor** de \( \max\mathrm{Re}\,\lambda \) o de
  \( M_s \); la curva \( \max\mathrm{Re}\,\lambda=0 \) es la **frontera de estabilidad**.
- **Sensibilidad local:** \( \partial\lambda_i/\partial\theta \) (vía autovectores derecho/izquierdo
  \( w_i,v_i \)): \( \dfrac{\partial\lambda_i}{\partial\theta}=\dfrac{w_i^\top (\partial A/\partial\theta)\,v_i}{w_i^\top v_i} \),
  que indica qué parámetro mueve más cada modo (enlaza con el [[analisis-modal|análisis modal]]).

Para muchos parámetros a la vez, el barrido en rejilla escala mal (maldición de la dimensión) → se
usa muestreo (Latin Hypercube, Monte Carlo) o análisis de sensibilidad global (Sobol).

<div class="cfig"><img src="figuras/barrido-parametrico-mapa.png" alt="mapa de calor 2D de max Re lambda frente a SCR y ancho de banda de PLL"><div class="cap">Barrido 2-D: para cada combinación de SCR y ancho de banda de la PLL se recalcula $\max\mathrm{Re}(\lambda)$ del modelo. El mapa de calor revela la región inestable (rojo) y la línea negra $\max\mathrm{Re}(\lambda)=0$ es la frontera de estabilidad. Una PLL más rápida desplaza la frontera hacia SCR mayores, reduciendo el margen en red débil.</div></div>

## 1 — Cómo se barre un parámetro y se traza el polo dominante
**Paso 1 — parametrizar la matriz de estado.** Se escribe el modelo de pequeña señal como \( \dot x=A(\theta)\,x \), donde \( \theta \) es el parámetro físico que se quiere variar (aquí el SCR de red). La dependencia entra por la inductancia de red: con \( L_g=1/(\mathrm{SCR}\cdot\omega_0) \), cada valor de \( \theta=\mathrm{SCR} \) produce una matriz \( A(\theta) \) distinta porque \( L_g \) aparece en las filas del inductor de red.

**Paso 2 — definir la rejilla.** Se elige el rango \( [\theta_{min},\theta_{max}] \) y un número de puntos. Si el rango abarca varios órdenes (SCR de 1 a 20), se usa espaciado logarítmico para no malgastar puntos en el extremo alto:

$$ \theta_k = \theta_{min}\left(\frac{\theta_{max}}{\theta_{min}}\right)^{k/(N-1)},\qquad k=0,\dots,N-1 $$

**Paso 3 — autovalores en cada punto.** Para cada \( \theta_k \) se resuelve el problema de autovalores \( \det\!\big(A(\theta_k)-\lambda I\big)=0 \), obteniendo el espectro \( \{\lambda_i(\theta_k)\} \). Los polos del sistema lineal son exactamente esos autovalores.

**Paso 4 — extraer el indicador escalar.** De cada espectro se condensa un único número: la **abscisa espectral**, la parte real más a la derecha, que decide la estabilidad:

$$ \alpha(\theta_k)=\max_i \operatorname{Re}\lambda_i(\theta_k) $$

El sistema es estable en \( \theta_k \) si y solo si \( \alpha(\theta_k)<0 \). El autovalor que alcanza ese máximo es el **modo dominante** (el más lento en amortiguarse, o el que primero se desestabiliza).

**Paso 5 — localizar la frontera.** Se busca el cruce \( \alpha(\theta)=0 \). Numéricamente es el primer \( k \) en que \( \alpha \) cambia de signo; el \( \theta \) crítico se afina por interpolación lineal entre \( \theta_{k-1} \) y \( \theta_k \):

$$ \boxed{\;\theta_{crit}\approx\theta_{k-1}-\alpha(\theta_{k-1})\,\frac{\theta_k-\theta_{k-1}}{\alpha(\theta_k)-\alpha(\theta_{k-1})}\;} $$

**Paso 6 — interpretar.** Trazar \( \operatorname{Re}\lambda \) (o todo \( \lambda \) en el plano complejo) frente a \( \theta \) da el **root-locus numérico**: la trayectoria del modo dominante. El punto donde cruza el eje imaginario es el límite de estabilidad, y la distancia entre el \( \theta \) nominal y \( \theta_{crit} \) es el **margen de robustez** (en el ejemplo de abajo, SCR nominal frente a \( \mathrm{SCR}_{crit}\approx2.3 \)).

## 2 — Sensibilidad modal: qué parámetro mueve más cada polo
**Paso 1 — derivar la ecuación del autovalor.** Para un autovalor simple \( \lambda_i \) con autovector derecho \( v_i \) (cumple \( A v_i=\lambda_i v_i \)) e izquierdo \( w_i \) (cumple \( w_i^\top A=\lambda_i w_i^\top \)). Se deriva \( A v_i=\lambda_i v_i \) respecto de \( \theta \):

$$ \frac{\partial A}{\partial\theta}v_i + A\frac{\partial v_i}{\partial\theta}=\frac{\partial\lambda_i}{\partial\theta}v_i+\lambda_i\frac{\partial v_i}{\partial\theta} $$

**Paso 2 — proyectar sobre el autovector izquierdo.** Se multiplica por la izquierda por \( w_i^\top \). El término \( w_i^\top A\,\partial_\theta v_i=\lambda_i w_i^\top\partial_\theta v_i \) (porque \( w_i^\top A=\lambda_i w_i^\top \)) se cancela exactamente con \( \lambda_i w_i^\top\partial_\theta v_i \) del otro lado. Queda solo el término del autovector derecho desaparecido:

$$ w_i^\top\frac{\partial A}{\partial\theta}v_i=\frac{\partial\lambda_i}{\partial\theta}\,w_i^\top v_i $$

**Paso 3 — despejar la sensibilidad.** Dividiendo entre el producto \( w_i^\top v_i\neq0 \):

$$ \boxed{\;\frac{\partial\lambda_i}{\partial\theta}=\frac{w_i^\top\,(\partial A/\partial\theta)\,v_i}{w_i^\top v_i}\;} $$

**Paso 4 — leer el resultado.** Es un número complejo: su parte real dice cuánto se desplaza el amortiguamiento del modo \( i \) por unidad de \( \theta \), y su parte imaginaria cuánto cambia su frecuencia. Comparando \( |\partial\lambda_i/\partial\theta| \) entre todos los parámetros se identifica **cuál mueve más** el modo crítico, es decir, dónde actuar para estabilizar. Esta fórmula es de primer orden (válida cerca del punto de evaluación) y enlaza con el [[analisis-modal|análisis modal]]; el barrido completo del apartado 1 es su versión exacta y no lineal.

## Cuándo y por qué se usa
Para hallar el **margen de robustez** ante variación de red/planta (p.ej. estabilidad vs
[[red-thevenin-scr|SCR]]), identificar el parámetro crítico, validar el diseño en el peor caso y
generar las figuras de robustez del informe.

## Procedimiento de diseño (genérico)
1. Parametriza el modelo: \( A(\theta) \) o \( L(s;\theta) \).
2. Define el rango y la rejilla (o el muestreo) de \( \theta \).
3. Para cada valor: calcula autovalores / \( M_s \) / márgenes ([[respuesta-frecuencia-ss]]).
4. Localiza la frontera de estabilidad y el caso peor.
5. Reporta margen (distancia al límite) y, si procede, sensibilidad modal del parámetro dominante.

## Ejemplo de aplicación real
**Problema:** Lazo de corriente de GFL: ¿para qué SCR mínimo el sistema se vuelve inestable con el control diseñado? Barrer SCR de 1 a 20 y trazar la trayectoria del modo más crítico.

Se parametriza \( A(\text{SCR}) \): la inductancia de red varía como \( L_g=1/(\text{SCR}\times\omega_0) \). Para cada valor del barrido (50 puntos log-espaciados de SCR=1 a 20) se calculan los autovalores de \( A \). El modo de la PLL mueve su parte real: a SCR=20 tiene \( \text{Re}(\lambda)\approx-25 \) (estable); a SCR=2.3 cruza a \( \text{Re}(\lambda)=0 \) (frontera de estabilidad). El SCR crítico \( \approx2.3 \) da el margen de robustez: el sistema aguanta una red 2.3 veces más débil que la nominal. Frente al requisito del código de red (SCR>2.0), el margen es del 15 %: ajustado. Reducir el ancho de banda de la PLL desplaza el límite a SCR<1.5.

## Ejemplo de código
```python
import numpy as np
scr = np.linspace(1.0, 10.0, 50)
worst = [np.max(np.real(np.linalg.eigvals(A_of(s)))) for s in scr]
scr_lim = scr[np.argmax(np.array(worst) > 0)]    # primer SCR inestable
```

## Parámetros y valores típicos
Rejilla 1-D: 50–500 puntos (logarítmica si el rango es amplio). Objetivo: estable en todo el rango
esperado con \( M_s<2 \) y margen al límite > 20–30 %.

## Errores comunes
- Rejilla gruesa que **salta** una franja de inestabilidad estrecha.
- Reordenamiento de autovalores entre puntos (el "tracking" de modos requiere emparejar por
  continuidad/autovectores).
- Barrer un solo parámetro cuando el peor caso aparece por **combinación** de varios.

## Conceptos relacionados
- [[robustez-parametrica]] · [[respuesta-frecuencia-ss]] · [[analisis-modal]] · [[margenes-estabilidad]] · [[red-thevenin-scr]]

## Referencias
- Skogestad, Postlethwaite, *Multivariable Feedback Control*, 2005.
- Saltelli et al., *Global Sensitivity Analysis*, 2008.
