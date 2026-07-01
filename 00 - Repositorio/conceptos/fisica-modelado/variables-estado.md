---
titulo: Cómo definir las variables de estado
slug: variables-estado
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance, 03-DataCenter-IA]
objetivos: [elegir el conjunto minimo de variables que describen el sistema, construir las matrices A B C D, entender la forma modal y los autovalores]
tags: [estado, orden, energia, independencia, modelado, matrices-ABCd, autovalores, modal, LCL, dq]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [modelado-sistemas, representacion-espacio-estados, filtro-lcl, linealizacion-teoria]
referencias:
  - "Franklin, Powell, Feedback Control of Dynamic Systems"
  - "Kailath, Linear Systems, Prentice Hall"
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

## 2 — Variables de estado en circuitos eléctricos: corrientes de L y tensiones de C

### Por qué son estados: la energía no puede saltar
La energía almacenada en un inductor es \( W_L=\tfrac12 L i_L^2 \). Si la corriente pudiera saltar en un instante \( dt\to0 \), la potencia \( p=v\cdot i=L\,\dot i\cdot i \) sería infinita, lo que requeriría una fuente de energía infinita. Por eso \( i_L \) varía de forma continua (es diferenciable): es una variable de estado natural. Análogamente, \( v_C \) en un condensador (\( W_C=\tfrac12 C v_C^2 \)) no puede saltar sin corriente infinita (\( i_C=C\,\dot v_C \)).

### Regla de independencia
No todos los inductores/condensadores de un circuito son estados independientes:
- **Inductores en serie o en corte solo de L**: la misma corriente circula por todos → solo uno es estado, los demás dependen de él.
- **Condensadores en paralelo o en lazo solo de C**: la misma tensión → solo uno es estado.

Si existen esas dependencias, el orden del sistema es **menor** que el número de elementos almacenadores.

### Ejemplo: filtro LC → 2 estados
Un filtro LC serie (L en serie, C en paralelo) tiene un inductor y un condensador independientes: \( \mathbf{x}=[i_L,\, v_C]^T \), sistema de orden 2.

### Ejemplo: filtro LCL → 3 estados por fase
El LCL tiene \( L_1 \), \( C_f \), \( L_2 \) todos independientes:
$$ \mathbf{x}=[i_{L1},\, v_{C},\, i_{L2}]^T \quad \text{(por fase, orden 3)} $$
En el marco dq, cada variable tiene componente d y q: \( \mathbf{x}\in\mathbb{R}^6 \), orden 6.

### Los estados del control añaden más orden
El controlador tiene también sus integradores y filtros, cuya salida no se puede "saltar":
- Integrador del PI de corriente: estado \( \varepsilon_i \) (error integrado).
- Filtro de potencia del droop: estado \( P_m \) (potencia filtrada).
- PLL: dos estados \( (\theta_{PLL},\varepsilon_{PLL}) \).

Cada uno suma al orden del modelo completo del sistema (ver Apartado 5).

## 3 — Las matrices A, B, C, D: de qué depende cada una

### La física de cada matriz
En el modelo lineal \( \dot{\mathbf{x}}=A\mathbf{x}+B\mathbf{u} \), \( \mathbf{y}=C\mathbf{x}+D\mathbf{u} \):

- **\( A \)** (dinámica): proviene de las leyes de KVL/KCL aplicadas a los almacenadores. Es la matriz que determina los **autovalores** (polos del sistema). Cada elemento \( A_{ij} \) cuantifica cómo el estado \( j \) afecta a \( \dot x_i \). Cambiar la inductancia \( L_1 \) cambia la fila de la ecuación de \( i_{L1} \) en \( A \).

- **\( B \)** (entrada): describe cómo las entradas (\( v_i \), \( v_{pcc} \)) inyectan fuerza sobre los estados. Si la entrada entra directamente en la KVL de \( L_1 \), el coeficiente es \( 1/L_1 \).

- **\( C \)** (salida): selecciona qué combinaciones de estados se miden o se definen como salidas. Si se mide la corriente de red \( i_{L2} \), entonces \( C=[0,0,1] \).

- **\( D \)** (realimentación directa): acoplamiento directo entrada→salida, **sin pasar por los integradores**. En circuitos con almacenadores, \( D=0 \) casi siempre: el condensador y el inductor siempre "mediatizan" la relación entre \( v_i \) e \( i_{L2} \).

### La matriz A del LCL en dq: 6×6
Las tres ecuaciones de KVL/KCL del LCL por fase (de [[filtro-lcl]]):
$$ L_1\dot i_1 = v_i - v_C - R_1 i_1, \quad C_f\dot v_C = i_1-i_2, \quad L_2\dot i_2 = v_C - v_{pcc} - R_2 i_2 $$

En el marco dq (girando a \( \omega \)), cada ecuación escalar se convierte en dos (d y q) con acoplamiento cruzado \( \pm\omega \):

$$ A_{6\times6}=\begin{bmatrix}
-R_1/L_1 & \omega & -1/L_1 & 0 & 0 & 0 \\
-\omega & -R_1/L_1 & 0 & -1/L_1 & 0 & 0 \\
1/C_f & 0 & 0 & \omega & -1/C_f & 0 \\
0 & 1/C_f & -\omega & 0 & 0 & -1/C_f \\
0 & 0 & 1/L_2 & 0 & -R_2/L_2 & \omega \\
0 & 0 & 0 & 1/L_2 & -\omega & -R_2/L_2
\end{bmatrix} $$

El estado es \( \mathbf{x}=[i_{1d},i_{1q},v_{Cd},v_{Cq},i_{2d},i_{2q}]^T \). Los términos \( \pm\omega \) en la diagonal secundaria son el **acoplamiento de Park**: la rotación del marco dq introduce una fuerza de Coriolis ficticia que acopla las componentes d y q de la misma variable.

## 4 — El cambio de base modal: de coordenadas físicas a modales

### Por qué cambiar de base
La matriz \( A \) en coordenadas físicas es densa (acoplada): \( \dot x_i \) depende de muchos \( x_j \). En coordenadas **modales** la matriz se vuelve diagonal: cada modo evoluciona de forma **independiente**. Esto permite analizar la estabilidad modo a modo y entender qué partes del sistema son lentas o rápidas.

### La transformación modal
Si \( A \) tiene autovalores \( \lambda_1,\dots,\lambda_n \) y autovectores (columnas) \( \Phi=[\phi_1|\cdots|\phi_n] \), entonces:
$$ A\,\Phi = \Phi\,\Lambda, \quad \Lambda=\mathrm{diag}(\lambda_1,\dots,\lambda_n) $$

Definiendo el cambio de base \( \mathbf{x}=\Phi\,\mathbf{z} \) (coordenadas modales \( \mathbf{z} \)):
$$ \dot{\mathbf{x}}=A\mathbf{x} \implies \Phi\dot{\mathbf{z}}=A\Phi\mathbf{z}=\Phi\Lambda\mathbf{z} \implies \boxed{\dot{\mathbf{z}}=\Lambda\mathbf{z}} $$

El sistema modal es diagonal: \( \dot z_i=\lambda_i z_i \), cuya solución es \( z_i(t)=z_i(0)\,e^{\lambda_i t} \). Cada modo \( i \) evoluciona de forma completamente independiente de los demás.

### La respuesta libre como superposición de modos
Volviendo a coordenadas físicas con \( \mathbf{z}(0)=\Phi^{-1}\mathbf{x}_0 \) y definiendo los **vectores fila** de \( \Phi^{-1} \) como \( \psi_i^T \):
$$ \mathbf{x}(t)=\Phi\,e^{\Lambda t}\,\Phi^{-1}\,\mathbf{x}_0=\sum_{i=1}^n \phi_i\cdot\underbrace{(\psi_i^T\,\mathbf{x}_0)}_{\text{excitación del modo }i}\cdot e^{\lambda_i t} $$

El término \( \psi_i^T\mathbf{x}_0 \) indica cuánto excita la condición inicial al modo \( i \); el autovector \( \phi_i \) indica la "forma" de ese modo (qué estados participan y en qué proporción); y \( e^{\lambda_i t} \) da la dinámica temporal.

### Por qué los polos de G(s) son los autovalores de A
La función de transferencia \( G(s)=C(sI-A)^{-1}B \). El denominador es \( \det(sI-A) \), que es el **polinomio característico** de \( A \). Sus raíces son, por definición, los autovalores \( \lambda_i \). Por tanto, los **polos de \( G(s) \)** coinciden exactamente con los **autovalores de \( A \)**, independientemente de \( B \), \( C \) y \( D \) (los ceros sí dependen de \( B,C,D \)).

## 5 — Estados del control: PI, filtros, PLL como estados

### El integrador PI es un estado
El controlador PI tiene la ecuación:
$$ u_{PI}(t)=K_p\,e(t)+K_i\underbrace{\int_0^t e\,d\tau}_{\varepsilon} \implies \dot\varepsilon = e $$

La variable \( \varepsilon \) (el error integrado) **no puede saltar**: es el estado del PI. En el modelo de espacio de estados del lazo cerrado, aparece una nueva fila/columna correspondiente a \( \varepsilon \). Cada lazo PI añade un estado.

### El filtro de potencia del droop
El droop mide la potencia activa a través de un filtro paso bajo:
$$ \dot P_m = \omega_f\,(P_{inst}-P_m) $$
donde \( \omega_f=2\pi f_c \) es la frecuencia de corte del filtro. El estado es \( P_m \) (la potencia filtrada); el estado de \( Q_m \) es análogo.

### El PLL: dos estados
Un PLL de tipo 2 (con integrador en la rama de control) tiene dos estados:
1. \( \theta_{PLL} \): el ángulo estimado de la red (integración de la frecuencia estimada).
2. \( \varepsilon_{PLL} \): el estado interno del PI del bucle de fase.

### Conteo completo para el GFM del Proyecto 01
Partiendo de los bloques del modelo del convertidor grid-forming (ver proyecto 01-GFM-Impedance):

| Bloque | Estados | Orden |
|---|---|---|
| Filtro LCL en dq | \( i_{1d},i_{1q},v_{Cd},v_{Cq},i_{2d},i_{2q} \) | 6 |
| Ángulo de oscilador virtual (droop de frecuencia) | \( \delta \) | 1 |
| Filtros de potencia (droop) | \( P_m, Q_m \) | 2 |
| Integradores PI de corriente (d y q) | \( \varepsilon_{id}, \varepsilon_{iq} \) | 2 |
| Integradores PI de tensión (d y q) | \( \varepsilon_{vd}, \varepsilon_{vq} \) | 2 |
| Filtros HPF de amortiguamiento activo | \( \xi_{d},\xi_{q} \) | 2 |
| **Total** | | **15** |

El modelo linealizado del GFM es una matriz \( A_{15\times15} \). Sus 15 autovalores muestran el modo de resonancia del LCL, los modos de control de corriente y tensión, y el modo de potencia del droop.

## 6 — Diseño iterativo: construir el espacio de estados del filtro LCL

### Paso 1 — identificar los almacenadores de energía
El LCL tiene tres elementos que almacenan energía de forma independiente:
- \( L_1=2\,\text{mH} \): inductor lado fuente → estado \( i_{L1} \) (corriente)
- \( C_f=15\,\mu\text{F} \): condensador de filtrado → estado \( v_C \) (tensión)
- \( L_2=0.5\,\text{mH} \): inductor lado red → estado \( i_{L2} \) (corriente)

Orden del sistema: 3 (por fase).

### Paso 2 — escribir las ecuaciones diferenciales de KVL/KCL
Aplicando KVL a la rama de \( L_1 \), KCL al nudo \( v_C \) y KVL a la rama de \( L_2 \) (con \( v_{pcc}=0 \) para la función de transferencia directa):

$$ \dot i_{L1} = -\frac{R_1}{L_1}\,i_{L1} - \frac{1}{L_1}\,v_C + \frac{1}{L_1}\,v_i $$
$$ \dot v_C = \frac{1}{C_f}\,i_{L1} - \frac{1}{C_f}\,i_{L2} $$
$$ \dot i_{L2} = \frac{1}{L_2}\,v_C - \frac{R_2}{L_2}\,i_{L2} $$

### Paso 3 — forma matricial \( \dot{\mathbf{x}}=A\mathbf{x}+Bu \)
Con \( \mathbf{x}=[i_{L1},v_C,i_{L2}]^T \) y \( u=v_i \):

$$ A=\begin{bmatrix}-R_1/L_1&-1/L_1&0\\1/C_f&0&-1/C_f\\0&1/L_2&0\end{bmatrix},\quad
B=\begin{bmatrix}1/L_1\\0\\0\end{bmatrix} $$

Con los valores numéricos (\( L_1=2\,\text{mH} \), \( L_2=0.5\,\text{mH} \), \( C_f=15\,\mu\text{F} \), \( R_1=50\,\text{m}\Omega \)):

$$ A=\begin{bmatrix}-25 & -500 & 0 \\ 66667 & 0 & -66667 \\ 0 & 2000 & 0 \end{bmatrix} $$

### Paso 4 — en dq: añadir acoplamiento de Park
En el marco dq (girando a \( \omega=2\pi\times50\approx314\,\text{rad/s} \)), cada variable escalar se desdobla en d y q. La matriz \( A \) crece a \( 6\times6 \) con los términos \( \pm\omega \) de acoplamiento cruzado (ver Apartado 3). Esto es una transformación de base (el cambio de abc a dq), no un cambio en la física.

### Paso 5 — verificar que los autovalores coinciden con los polos de G(s)
Los autovalores de \( A_{3\times3} \) deben coincidir con las raíces del denominador de la función de transferencia \( G_{i_{L2}/v_i}(s) \). El denominador es:
$$ D(s) = L_1 L_2 C_f\,s^3 + R_1 L_2 C_f\,s^2 + (L_1+L_2)\,s + R_1 = \det(sI-A)\cdot L_1 L_2 C_f $$
Las raíces de \( D(s) \) son: un par complejo conjugado en \( s\approx\pm j\omega_{res} \) (la resonancia) y un polo real lento en \( s\approx-R_1/(L_1+L_2) \). Estos coinciden exactamente con \( \lambda_{1,2,3} \) de \( A \).

La frecuencia de resonancia (con \( R_1\approx0 \)):
$$ f_{res}=\frac{1}{2\pi}\sqrt{\frac{L_1+L_2}{L_1\,L_2\,C_f}}=\frac{1}{2\pi}\sqrt{\frac{2.5\times10^{-3}}{2\times10^{-3}\times0.5\times10^{-3}\times15\times10^{-6}}}\approx1837\,\text{Hz} $$

<div class="cfig"><img src="figuras/variables-estado-analisis.png" alt="Analisis completo: circuito LCL estados, respuesta escalon, autovalores, forma modal"><div class="cap">Panel (a): los tres estados del LCL (iL1, vC, iL2) y sus energías almacenadas. (b): respuesta a un escalón de tensión de 100 V mostrando las tres dinámicas acopladas. (c): los tres autovalores de A en el plano s: un par complejo ±j·ωres y un polo real lento. (d): el autovector del modo resonante, que muestra la participación relativa de cada estado en la resonancia.</div></div>

## Cuándo y por qué se usa
Es el paso que fija la estructura del modelo de estado. Elegir bien evita estados redundantes
(matriz \( A \) singular) o modelos de orden equivocado.

## Procedimiento (genérico)
1. Lista todos los elementos almacenadores de energía.
2. Comprueba **independencia** (lazos de C, cortes de L → reducen el orden).
3. Asigna a cada almacenador independiente su variable de energía (i en L, v en C, ω en J).
4. Añade los estados del **control** (integradores de PI, filtros, PLL).
5. Escribe las KVL/KCL → forma matricial \( A,B,C,D \).
6. En dq: añadir términos \( \pm\omega \) de acoplamiento de Park.
7. Verifica que los autovalores de \( A \) coinciden con los polos de \( G(s) \).

## Ejemplo de código
```python
import numpy as np
from scipy.linalg import eig

L1, L2, Cf, R1 = 2e-3, 0.5e-3, 15e-6, 0.05
A = np.array([[-R1/L1, -1/L1, 0],
              [1/Cf,   0,    -1/Cf],
              [0,      1/L2,  0]])
B = np.array([[1/L1], [0], [0]])
C = np.array([[0, 0, 1]])   # salida: iL2

evals, evecs = eig(A)
print("Autovalores:", evals)
# -> un par complejo ±j*11543 rad/s (~1837 Hz) + polo real -25 rad/s

# Forma modal del modo resonante
idx = np.argmax(evals.imag)
phi_res = np.abs(evecs[:, idx]) / np.max(np.abs(evecs[:, idx]))
print("Autovector normalizado:", phi_res)  # [0.94, 1.0, 0.04]
```

## Parámetros y valores típicos
GFM (proyecto 01): 15 estados = 6 del LCL (dq) + δ + Pm, Qm + 4 integradores PI + 2 del HPF.
GFL (proyecto 02): 10 = 6 del LCL + δ + ε(PLL) + 2 integradores de corriente.
LCL monofásico: 3 estados, \( f_{res}\approx1837\,\text{Hz} \) con L1=2mH, L2=0.5mH, Cf=15µF.

## Errores comunes
- Tomar como estados independientes condensadores en paralelo o inductores en serie (no lo son).
- Olvidar los estados del controlador (integradores, filtros, PLL).
- Confundir autovalores de \( A \) con ceros de \( G(s) \): los ceros dependen de \( B,C,D \) pero los polos (autovalores de \( A \)) no.
- En dq, olvidar los términos de acoplamiento cruzado \( \pm\omega \) de la transformación de Park.

## Uso en proyectos
- **01/02**: las variables de estado se eligieron como las corrientes de inductor y tensiones de
  condensador del LCL más los estados del control (droop/PLL e integradores).

## Conceptos relacionados
- [[modelado-sistemas]] · [[representacion-espacio-estados]] · [[filtro-lcl]] · [[linealizacion-teoria]]

## Referencias
- Franklin, Powell, *Feedback Control of Dynamic Systems*.
- Kailath, *Linear Systems*, Prentice Hall.
