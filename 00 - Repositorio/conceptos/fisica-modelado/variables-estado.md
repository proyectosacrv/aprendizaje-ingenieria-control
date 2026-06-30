---
titulo: Cómo definir las variables de estado
slug: variables-estado
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance, 03-DataCenter-IA]
objetivos: [elegir el conjunto minimo de variables que describen el sistema]
tags: [estado, orden, energia, independencia, modelado]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-30
relacionados: [modelado-sistemas, representacion-espacio-estados, filtro-lcl, linealizacion-teoria]
referencias:
  - "Franklin, Powell, Feedback Control of Dynamic Systems"
---

## Definición
Las **variables de estado** son el conjunto **mínimo** de variables que, junto con las entradas
futuras, determinan por completo la evolución del sistema. Son la "memoria" del sistema en cada
instante.

## Fundamento teórico
Idea central: el estado guarda la **energía almacenada**. El número de variables de estado
(el **orden** del sistema) es igual al número de elementos **independientes** que almacenan
energía:
- Inductor → su **corriente** \( i_L \) (energía \( \tfrac{1}{2}L i_L^2 \)).
- Condensador → su **tensión** \( v_C \) (energía \( \tfrac{1}{2}C v_C^2 \)).
- Masa/inercia → su **velocidad** \( \omega \) (energía \( \tfrac{1}{2}J\omega^2 \)).
- Integradores del control (PI, filtros) → su salida es estado.

La elección **no es única** (cualquier transformación invertible \( \mathbf{z}=T\mathbf{x} \) da
otro conjunto válido), pero conviene que sean:
- **Físicas / medibles** (facilitan observador y validación).
- **Independientes**: si un lazo solo de condensadores o un corte solo de inductores crea una
  dependencia, esos almacenadores **no** son independientes y el orden baja.

<div class="cfig"><img src="figuras/variables-estado-circuito.png" alt="estados de un circuito LC"><div class="cap">Los estados son las variables de energía de los elementos independientes: la corriente del inductor iL y la tensión del condensador vC. Dos almacenadores independientes → sistema de orden 2.</div></div>

## 1 — Por qué una EDO de orden \( n \) se convierte en \( n \) EDOs de primer orden
La razón profunda de que el orden del sistema sea el número de almacenadores de energía es puramente algebraica: **toda** ecuación diferencial de orden \( n \) se reescribe como un sistema de \( n \) ecuaciones de **primer** orden eligiendo como estados la salida y sus \( n-1 \) derivadas. El modelo de estado no es más que esa reescritura, hecha de forma sistemática.

**Paso 1 — la EDO de partida.** Sea un sistema lineal de orden \( n \) con salida \( y(t) \) y entrada \( u(t) \):

$$ y^{(n)}+a_{n-1}\,y^{(n-1)}+\dots+a_1\,\dot y+a_0\,y = b_0\,u $$

donde \( y^{(k)} \) es la derivada \( k \)-ésima. Hay **una** ecuación, pero involucra hasta la derivada \( n \)-ésima: para integrarla numéricamente necesitamos conocer en \( t_0 \) el valor de \( y \) y de sus \( n-1 \) primeras derivadas. Esas \( n \) cantidades son exactamente la "memoria" del sistema.

**Paso 2 — bautizar las derivadas como estados.** Definimos un vector de \( n \) estados, cada uno una derivada sucesiva:

$$ x_1 = y,\quad x_2 = \dot y,\quad x_3 = \ddot y,\;\dots,\; x_n = y^{(n-1)} $$

**Paso 3 — derivar cada definición.** Al derivar \( x_1 \) aparece \( x_2 \); al derivar \( x_2 \) aparece \( x_3 \); y así en cadena. Cada derivada de un estado **es** el siguiente estado, salvo la última:

$$ \dot x_1 = \dot y = x_2,\qquad \dot x_2 = \ddot y = x_3,\qquad \dots,\qquad \dot x_{n-1}=y^{(n-1)}=x_n $$

**Paso 4 — la última ecuación es la EDO original.** Para \( \dot x_n = y^{(n)} \) no hay un "estado siguiente": usamos la EDO del Paso 1 para despejar \( y^{(n)} \), sustituyendo cada derivada por su estado (\( y^{(n-1)}=x_n,\dots,\dot y=x_2,\,y=x_1 \)):

$$ \dot x_n = y^{(n)} = -a_0\,x_1 - a_1\,x_2 - \dots - a_{n-1}\,x_n + b_0\,u $$

**Paso 5 — apilar en forma matricial.** Los Pasos 3 y 4 son \( n \) ecuaciones de **primer orden**. En forma \( \dot{\mathbf{x}}=A\mathbf{x}+B u \):

$$ \boxed{\;\frac{d}{dt}\!\begin{bmatrix}x_1\\\vdots\\x_{n-1}\\x_n\end{bmatrix}=
\begin{bmatrix}0&1&\cdots&0\\\vdots&&\ddots&\vdots\\0&0&\cdots&1\\-a_0&-a_1&\cdots&-a_{n-1}\end{bmatrix}\!
\begin{bmatrix}x_1\\\vdots\\x_{n-1}\\x_n\end{bmatrix}+
\begin{bmatrix}0\\\vdots\\0\\b_0\end{bmatrix}u\;} $$

Los unos de la superdiagonal son las \( n-1 \) cadenas \( \dot x_k=x_{k+1} \) (puro renombre); la última fila es la única "física", la EDO original. Esta es precisamente la **forma canónica controlable** que se construye en [[representacion-espacio-estados]]. Conclusión: elegir como estados las variables de energía (corriente de L, tensión de C, velocidad de J) no es un truco, sino la versión física de tomar "la salida y sus derivadas": cada almacenador independiente aporta una integración, es decir, un orden, es decir, un estado.

## Cuándo y por qué se usa
Es el paso que fija la estructura del modelo de estado. Elegir bien evita estados redundantes
(matriz \( A \) singular) o modelos de orden equivocado.

## Procedimiento (genérico)
1. Lista todos los elementos almacenadores de energía.
2. Comprueba **independencia** (lazos de C, cortes de L → reducen el orden).
3. Asigna a cada almacenador independiente su variable de energía (i en L, v en C, ω en J).
4. Añade los estados del **control** (integradores de PI, filtros, PLL).
5. Verifica que con esas variables puedes escribir \( \dot{\mathbf{x}}=\mathbf{f}(\mathbf{x},\mathbf{u}) \).

## Ejemplo de código
```python
# filtro LCL por fase -> 3 estados; en dq -> 6 (cada uno d y q)
estados = ["iL1", "vC", "iL2"]          # corriente L1, tension Cf, corriente L2
```

## Parámetros y valores típicos
GFM (proyecto 01): 15 estados = 6 del LCL (dq) + δ + Pm, Qm + 4 integradores PI + 2 del HPF.
GFL (proyecto 02): 10 = 6 del LCL + δ + ε(PLL) + 2 integradores de corriente.

## Errores comunes
- Tomar como estados independientes condensadores en paralelo o inductores en serie (no lo son).
- Olvidar los estados del controlador (integradores, filtros, PLL).

## Uso en proyectos
- **01/02**: las variables de estado se eligieron como las corrientes de inductor y tensiones de
  condensador del LCL más los estados del control (droop/PLL e integradores).

## Conceptos relacionados
- [[modelado-sistemas]] · [[representacion-espacio-estados]] · [[filtro-lcl]]

## Referencias
- Franklin, Powell, *Feedback Control of Dynamic Systems*.
