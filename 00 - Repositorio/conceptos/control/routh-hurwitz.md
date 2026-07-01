---
titulo: Criterio de Routh-Hurwitz
slug: routh-hurwitz
categoria: control
tipo: metodo
nivel: basico
proyectos: []
objetivos: [comprobar estabilidad sin calcular las raíces del polinomio característico]
tags: [routh, hurwitz, estabilidad, ecuacion-caracteristica, basico, control, lugar-raices]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-01
relacionados: [estabilidad-bibo, polos-ceros, funcion-transferencia, criterio-nyquist, lugar-raices]
referencias:
  - "Ogata, Ingeniería de Control Moderna, Pearson"
  - "Dorf, Bishop, Modern Control Systems, Pearson"
---

## Definición
Test **algebraico** que dice cuántas raíces de un polinomio tienen parte real positiva (polos
inestables) sin resolverlo, a partir de los signos de la primera columna de la **tabla de Routh**.

## Fundamento teórico
Dado el polinomio característico
$$ a_n s^n + a_{n-1}s^{n-1} + \dots + a_1 s + a_0 = 0 $$
condición **necesaria**: todos los \( a_i \) presentes y del mismo signo. Condición **suficiente**:
se construye la tabla
$$ b_1=\frac{a_{n-1}a_{n-2}-a_n a_{n-3}}{a_{n-1}}, \quad
   b_2=\frac{a_{n-1}a_{n-4}-a_n a_{n-5}}{a_{n-1}}, \ \dots $$
El **nº de cambios de signo en la primera columna = nº de polos en el SPD**. Sistema estable
\( \iff \) toda la primera columna es positiva (sin cambios de signo).

Casos especiales: un cero en la primera columna se sustituye por \( \varepsilon\to0^+ \); una
fila entera nula indica raíces simétricas (polinomio auxiliar) → al menos marginalmente inestable.

<div class="cfig"><img src="figuras/routh-hurwitz-locus.png" alt="raices del polinomio al variar Kp"><div class="cap">Raíces de $s^3+3s^2+2s+K_p$ al variar $K_p$ (color). El par complejo cruza el eje imaginario en $s=\pm j\sqrt{2}$ exactamente en $K_p=6$: por debajo el sistema es estable, por encima inestable. Routh entrega ese límite ($0<K_p<6$) sin resolver el polinomio.</div></div>

## 1 — Construcción de la tabla y por qué los signos cuentan polos
**Paso 1 — las dos primeras filas.** Con el polinomio \( a_n s^n+a_{n-1}s^{n-1}+\dots+a_0 \), las dos primeras filas se rellenan **alternando** los coeficientes: la fila \( s^n \) toma los de potencias pares contando desde arriba, la fila \( s^{n-1} \) los de potencias impares.

$$
\begin{array}{c|ccc}
s^n     & a_n     & a_{n-2} & a_{n-4} \\
s^{n-1} & a_{n-1} & a_{n-3} & a_{n-5} \\
\end{array}
$$

**Paso 2 — fila siguiente por el determinante \( 2\times2 \).** Cada elemento nuevo se calcula con las dos filas inmediatamente superiores. La fila \( s^{n-2} \) tiene elementos \( b_i \):

$$ b_1=\frac{a_{n-1}a_{n-2}-a_n a_{n-3}}{a_{n-1}}=-\frac{1}{a_{n-1}}\begin{vmatrix} a_n & a_{n-2}\\ a_{n-1} & a_{n-3}\end{vmatrix},\qquad b_2=\frac{a_{n-1}a_{n-4}-a_n a_{n-5}}{a_{n-1}} $$

El patrón: numerador = (producto de la diagonal del primer pivote) − (producto cruzado con la columna siguiente), todo dividido por el pivote \( a_{n-1} \) de la fila de encima. Se repite con las filas \( s^{n-2} \) y \( s^{n-1} \) para obtener \( s^{n-3} \), y así hasta \( s^0 \).

**Paso 3 — por qué la primera columna detecta el SPD.** Routh-Hurwitz es equivalente a aplicar el principio del argumento a \( D(j\omega) \) recorriendo el eje imaginario: el número de cambios de signo en la primera columna iguala el número de raíces con parte real positiva. Intuición: si todas las raíces tuvieran \( \mathrm{Re}<0 \), la división sucesiva nunca cambia de signo (todos los pivotes positivos); cada raíz que cruza al SPD fuerza un cambio de signo. Por eso:

$$ \boxed{\;\text{nº de cambios de signo en la 1ª columna}=\text{nº de raíces en el SPD}\;} $$

**Paso 4 — ejemplo de 3er orden.** Para \( s^3+3s^2+2s+K_p \) (coef. \( a_3{=}1,a_2{=}3,a_1{=}2,a_0{=}K_p \)):

$$
\begin{array}{c|cc}
s^3 & 1 & 2 \\
s^2 & 3 & K_p \\
s^1 & \dfrac{3\cdot2-1\cdot K_p}{3}=\dfrac{6-K_p}{3} & 0 \\
s^0 & K_p & 0
\end{array}
$$

Primera columna \( \{1,\,3,\,(6-K_p)/3,\,K_p\} \): toda positiva exige \( K_p>0 \) y \( 6-K_p>0 \), es decir \( \boxed{0<K_p<6} \). En \( K_p=6 \) el pivote \( s^1 \) se anula: verificado numéricamente, las raíces son \( -3 \) y \( \pm j\sqrt2 \) (\( \sqrt2\approx1.414 \)), par imaginario puro = oscilación sostenida = margen de ganancia. Coincide con el cruce del [[lugar-raices]] por el eje imaginario.

## 2 — Construcción paso a paso: ejemplo de 4º orden

Se trabaja con \( p(s) = s^4+3s^3+3s^2+2s+K \), polinomio de grado cuatro con un parámetro \( K \).

**Paso 1 — rellenar las dos primeras filas alternando.**
Los coeficientes son \( a_4=1,\,a_3=3,\,a_2=3,\,a_1=2,\,a_0=K \). La regla de alternado da:

$$
\begin{array}{c|ccc}
s^4 & 1 & 3 & K \\
s^3 & 3 & 2 & 0 \\
\end{array}
$$

**Paso 2 — fila \( s^2 \): usar pivote \( a_3=3 \).**

$$
b_1 = \frac{3\cdot3 - 1\cdot2}{3} = \frac{7}{3}, \qquad b_2 = \frac{3\cdot K - 1\cdot 0}{3} = K
$$

$$
\begin{array}{c|ccc}
s^4 & 1 & 3 & K \\
s^3 & 3 & 2 & 0 \\
s^2 & 7/3 & K & 0 \\
\end{array}
$$

**Paso 3 — fila \( s^1 \): usar pivote \( b_1=7/3 \).**

$$
c_1 = \frac{(7/3)\cdot2 - 3\cdot K}{7/3} = \frac{14/3 - 3K}{7/3} = 2 - \frac{9K}{7}
$$

**Paso 4 — fila \( s^0 \):** se arrastra el último término de la fila anterior (que no tiene columna de cruce):

$$
d_0 = K
$$

**Tabla completa:**
$$
\begin{array}{c|ccc}
s^4 & 1       & 3 & K \\
s^3 & 3       & 2 & 0 \\
s^2 & 7/3     & K & 0 \\
s^1 & 2-9K/7  & 0 & 0 \\
s^0 & K       & 0 & 0 \\
\end{array}
$$

**Primera columna:** \( \{1,\; 3,\; 7/3,\; 2-9K/7,\; K\} \). Para que todos sean positivos:
- \( K > 0 \)
- \( 2 - 9K/7 > 0 \;\Rightarrow\; K < 14/9 \approx 1.556 \)

Rango estable: \( \boxed{0 < K < 14/9} \). En \( K=14/9 \): el pivote de \( s^1 \) se anula → par de raíces imaginarias puras (oscilación sostenida). Para \( K>14/9 \): dos cambios de signo en la primera columna → dos raíces en el SPD (inestable).

## 3 — El caso de la fila de ceros y el pivote cero

Aparecen dos casos especiales durante la construcción de la tabla:

**Caso A — pivote cero (un elemento nulo en la primera columna, resto de la fila no nulo).**
Ejemplo: \( s^3 + 2s^2 + s + 2 \):

$$
\begin{array}{c|cc}
s^3 & 1 & 1 \\
s^2 & 2 & 2 \\
s^1 & (2\cdot1 - 1\cdot2)/2 = 0 & 0 \\
s^0 & 2 & \\
\end{array}
$$

El pivote de \( s^1 \) es cero. Si se calcula directamente la fila siguiente se divide por cero. **Solución:** reemplazar el cero por \( \varepsilon \to 0^+ \) y calcular \( s^0 \):

$$
\frac{0\cdot2 - 2\cdot\varepsilon}{\varepsilon} = \frac{-2\varepsilon}{\varepsilon} \to -2 < 0
$$

Hay un cambio de signo: \( \varepsilon > 0 \) y \( -2 < 0 \). La primera columna es \( \{1, 2, \varepsilon, -2\} \) — **un cambio de signo → una raíz en SPD**. Verificación: \( s^3+2s^2+s+2=(s^2+1)(s+2) \) tiene raíces en \( \pm j \) y \( -2 \) → en el eje imaginario (caso límite), lo que confirma que el criterio detecta inestabilidad marginal.

**Caso B — fila entera nula.**
Ejemplo: \( s^3 + s^2 + s + 1 \):

$$
\begin{array}{c|cc}
s^3 & 1 & 1 \\
s^2 & 1 & 1 \\
s^1 & (1\cdot1-1\cdot1)/1 = 0 & 0 \\
s^0 & ? & \\
\end{array}
$$

La fila de \( s^1 \) es completamente nula. Esto significa que hay **pares de raíces simétricas respecto al origen**: pares \( \pm j\omega \) (en el eje imaginario) o pares \( \pm\sigma \) (en el eje real, uno en SPD). **Solución:** usar el **polinomio auxiliar** formado por la fila inmediatamente anterior (\( s^2 \)):

$$
P_{aux}(s) = 1\cdot s^2 + 1 = s^2 + 1 \;\Rightarrow\; \frac{dP_{aux}}{ds} = 2s
$$

Reemplazar la fila nula con los coeficientes de \( dP_{aux}/ds \): \( [2, 0] \). Entonces:

$$
\begin{array}{c|cc}
s^3 & 1 & 1 \\
s^2 & 1 & 1 \\
s^1 & 2 & 0 \quad\leftarrow\text{derivada de }P_{aux}\\
s^0 & 1 & \\
\end{array}
$$

Primera columna \( \{1,1,2,1\} \): sin cambios de signo → no hay raíces en el SPD. Pero las raíces del polinomio auxiliar \( s^2+1=0 \) son \( s=\pm j \): **marginalmente inestable** (raíces en el eje imaginario). El sistema \( s^3+s^2+s+1=(s^2+1)(s+1) \) oscila sin amortiguamiento: ni estable ni inestable en el sentido estricto.

## 4 — Número de raíces en el SPD y rango de \( K \) estable

**Contar raíces inestables mediante los cambios de signo.**
Si la primera columna de la tabla de Routh tiene \( m \) cambios de signo, el polinomio tiene exactamente \( m \) raíces en el semiplano derecho abierto (\( \mathrm{Re}(s)>0 \)). Esta es la información que Routh comparte con el [[criterio-nyquist|criterio de Nyquist]] (\( Z = N + P \)), pero expresada algebraicamente.

**Límite de estabilidad: cuándo un elemento de la primera columna se hace cero.**
Cuando se barre un parámetro \( K \) y un elemento de la primera columna se anula exactamente, hay raíces imaginarias puras: el sistema está en el **margen de estabilidad**. La frecuencia de esas raíces se obtiene del polinomio auxiliar (la fila anterior al cero).

**Procedimiento para encontrar el \( K \) máximo estable (lazo de tercer orden genérico).**
Para \( s^3 + a_2 s^2 + a_1 s + K \):

$$
\begin{array}{c|cc}
s^3 & 1 & a_1 \\
s^2 & a_2 & K \\
s^1 & (a_2 a_1 - K)/a_2 & 0 \\
s^0 & K & 0 \\
\end{array}
$$

Condición de estabilidad: \( K > 0 \) y \( a_2 a_1 - K > 0 \;\Rightarrow\; K < a_1 a_2 \). Luego:

$$ \boxed{K_{max} = a_1\,a_2} $$

**Para el 4º orden (\( s^4+3s^3+3s^2+2s+K \)):** \( K_{max} = 14/9 \approx 1.556 \) (calculado en el apartado anterior).

**Margen de ganancia como cociente.**
Si la ganancia nominal es \( K_0 \), el margen de ganancia en Routh es:

$$ \text{GM} = \frac{K_{max}}{K_0} $$

Este valor corresponde exactamente al margen de ganancia del diagrama de Bode: la ganancia puede multiplicarse por GM antes de que la primera columna cambie de signo.

<div class="cfig"><img src="figuras/routh-hurwitz-analisis.png" alt="tabla de Routh, lugar de raíces y casos especiales"><div class="cap">Análisis completo de Routh-Hurwitz para el polinomio $s^4+3s^3+3s^2+2s+K$. (a) Elementos de la primera columna vs $K$: el valor $c_1=2-9K/7$ cruza cero en $K_{lim}=14/9\approx1.56$ (límite de estabilidad). (b) Lugar de raíces: las raíces cruzan el eje imaginario exactamente en $K_{lim}$, verificando el resultado algebraico. (c) Para $K=2>K_{lim}$: dos raíces en el SPD (cruces rojos); Routh predice 2 cambios de signo. (d) Caso fila nula $s^3+s^2+s+1$: raíces en $\pm j$ (eje imaginario) → marginalmente inestable.</div></div>

## 5 — Routh vs autovalores: cuándo usar cada uno

Ambos métodos responden la misma pregunta — ¿tiene el polinomio raíces en el SPD? — pero con herramientas distintas y con fortalezas complementarias.

**Routh-Hurwitz: método algebraico, analítico.**
- Trabaja directamente con los **coeficientes del polinomio**: no resuelve las raíces.
- Permite dejar un **parámetro simbólico** (p.ej. \( K \)) y obtener su rango de estabilidad en forma cerrada.
- Ideal para sistemas de **orden bajo a medio** (hasta orden ~4–5 a mano) sin retardos.
- No da información de amortiguamiento ni frecuencia — solo si hay raíces en el SPD o no.
- **Limitación**: los retardos \( e^{-sT} \) no son polinómicos; Routh no aplica directamente (requiere aproximación de Padé u otro método).

**Autovalores numéricos: método computacional.**
- Calcula las raíces exactas del polinomio → da **amortiguamiento** \( \zeta_k \) y **frecuencia** \( \omega_{n,k} \) de cada modo.
- Funciona para cualquier orden, incluyendo MIMO (autovalores de la matriz \( A \) del espacio de estados).
- No permite parámetros simbólicos: hay que fijar todos los valores numéricos antes.
- En Python: `numpy.linalg.eigvals(A)` o `numpy.roots(p)`.

**Cuándo elegir Routh.**
Cuando se quiere el **rango de un parámetro** (ganancia, coeficiente del controlador) que garantiza estabilidad, en sistemas de orden ≤4 sin retardos. Es la herramienta natural para derivar el margen de ganancia analíticamente, sin necesidad de trazar el lugar de raíces.

**Ejemplo práctico — droop de potencia (orden 2).**
El lazo de potencia de un convertidor grid-forming con control droop y filtro de medida de orden 1 da un polinomio característico de segundo orden:

$$ s^2 + \left(\frac{1}{\tau_f}\right)s + m_p \frac{3V^2}{2X\tau_f} = 0 $$

Con \( a_1=1/\tau_f \) y \( a_0=m_p\cdot 3V^2/(2X\tau_f) \), ambos positivos para \( m_p>0 \): Routh confirma directamente estabilidad sin calcular las raíces. Si \( m_p<0 \) (droop negativo, lazo positivo): \( a_0<0 \) → condición necesaria incumplida → inestable. Routh lo detecta en una línea.

## Cuándo y por qué se usa
Para hallar **rangos de un parámetro** (p.ej. la ganancia \( K \)) que mantienen la estabilidad,
en sistemas de orden bajo-medio y sin retardos. Complementa a [[criterio-nyquist]] (que sí maneja
retardos).

## Procedimiento (genérico)
1. Escribe la ecuación característica \( 1+L(s)=0 \) como polinomio.
2. Chequeo rápido: ¿faltan términos o cambian de signo? → inestable.
3. Construye la tabla de Routh.
4. Cuenta cambios de signo en la 1ª columna; con un parámetro libre, despeja la condición.

## Ejemplo de aplicación real
**Problema:** Lazo de tensión de tercer orden con polinomio característico \( s^3+3s^2+2s+K_p \). Determinar el rango de \( K_p \) que garantiza estabilidad.

Tabla de Routh: fila \( s^3 \): \( [1,\,2] \); fila \( s^2 \): \( [3,\,K_p] \); fila \( s^1 \): \( [(6-K_p)/3,\,0] \); fila \( s^0 \): \( [K_p,\,0] \). Para primera columna positiva: \( K_p>0 \) y \( (6-K_p)/3>0\Rightarrow K_p<6 \). Rango de estabilidad: \( 0<K_p<6 \). En \( K_p=6 \): el elemento de \( s^1 \) se anula — sistema al límite con par de polos imaginarios puros en \( \pm j\sqrt{2} \) (oscilaciones sostenidas). Esto da directamente el **margen de ganancia**: la ganancia de lazo puede multiplicarse por \( 6/K_p^{nom} \) antes de inestabilizar.

## Ejemplo de código
```python
import sympy as sp
s, K = sp.symbols('s K')
p = sp.Poly(s**3 + 3*s**2 + 3*s + (1+K), s)
print(sp.stability.routh(p) if hasattr(sp,'stability') else p.all_coeffs())
# para K: estable si todos los términos de la 1ª columna > 0

# Verificación numérica para un K dado:
import numpy as np
K_val = 1.0
roots = np.roots([1, 3, 3, 1+K_val])
n_unstable = sum(r.real > 0 for r in roots)
print(f"Raíces en SPD: {n_unstable}")
```

## Parámetros y valores típicos
Útil hasta orden ~4-5 a mano. Para órdenes altos o MIMO, usar autovalores numéricos
(`np.linalg.eigvals`).

## Errores comunes
- Olvidar el chequeo necesario (signos/términos) antes de montar la tabla.
- No tratar los casos especiales (cero en columna, fila nula).
- Usarlo con retardos puros \( e^{-sT} \) (no es polinómico) → usar Nyquist.

## Conceptos relacionados
- [[estabilidad-bibo]] · [[polos-ceros]] · [[criterio-nyquist]] · [[funcion-transferencia]] · [[lugar-raices]]

## Referencias
- Ogata, *Ingeniería de Control Moderna*.
- Dorf, Bishop, *Modern Control Systems*.
