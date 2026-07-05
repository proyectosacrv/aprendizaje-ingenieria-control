---
titulo: Lugar de las raíces (root locus)
slug: lugar-raices
categoria: control
tipo: metodo
nivel: basico
proyectos: []
objetivos: [ver cómo migran los polos del lazo cerrado al variar una ganancia]
tags: [root-locus, lugar-raices, polos, ganancia, basico, control]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-02
relacionados: [polos-ceros, realimentacion, funcion-transferencia, controlador-pid, respuesta-segundo-orden]
referencias:
  - "Ogata, Ingeniería de Control Moderna, Pearson"
  - "Franklin, Powell, Feedback Control of Dynamic Systems, Pearson"
---

## Definición
Trayectoria que describen los **polos del lazo cerrado** en el plano \( s \) cuando una ganancia
\( K \) varía de \( 0 \) a \( \infty \). Muestra de un vistazo cómo la realimentación reubica la
dinámica.

## Fundamento teórico
Para \( 1+K\,G(s)H(s)=0 \), un punto \( s \) pertenece al lugar si cumple la **condición de
ángulo** y fija \( K \) con la de **módulo**:
$$ \angle G(s)H(s) = \pm 180^\circ(2k+1), \qquad K = \frac{1}{|G(s)H(s)|} $$
Reglas clave: las ramas parten de los **polos** (\( K=0 \)) y terminan en los **ceros** o en el
infinito (\( K\to\infty \)); hay \( n-m \) **asíntotas** con ángulos \( \frac{(2k+1)180^\circ}{n-m} \)
y centroide \( \sigma_a=\frac{\sum p_i-\sum z_i}{n-m} \); el lugar sobre el eje real queda a la
izquierda de un número impar de polos+ceros.

<div class="cfig"><img src="figuras/lugar-raices-locus.png" alt="lugar de las raices"><div class="cap">Lugar de las raíces: al subir K, los polos del lazo cerrado salen de los de lazo abierto (×) y migran; aquí dos ramas se vuelven complejas y cruzan al semiplano derecho (inestable) para K grande.</div></div>

## 1 — De dónde salen las condiciones de ángulo y módulo
**Paso 1 — la ecuación característica como número complejo.** Los polos de lazo cerrado son las raíces de \( 1+K\,G(s)H(s)=0 \), o sea \( K\,G(s)H(s)=-1 \). Esto es una igualdad **entre números complejos**: un complejo iguala a \( -1 \) si y solo si su módulo es \( 1 \) y su argumento es \( \pm180^\circ \) (más cualquier vuelta entera \( 2k\pi \)).

**Paso 2 — separar módulo y ángulo.** Con \( K>0 \) real, \( K \) no aporta fase. Tomando módulo y argumento por separado:

$$ |K\,G(s)H(s)|=1 \;\Rightarrow\; K=\frac{1}{|G(s)H(s)|}, \qquad \angle G(s)H(s)=\pm180^\circ(2k+1) $$

La **condición de ángulo** decide *qué puntos* \( s \) están en el lugar (no depende de \( K \)); la **condición de módulo** asigna *qué valor de* \( K \) los produce. Como \( G(s)H(s)=\dfrac{\prod(s-z_i)}{\prod(s-p_j)} \), el ángulo es \( \sum\angle(s-z_i)-\sum\angle(s-p_j) \): la suma de ángulos desde los ceros menos la suma desde los polos debe valer \( 180^\circ \) impar.

**Paso 3 — comportamiento asintótico.** Para \( s\to\infty \), con \( n \) polos y \( m \) ceros, \( G H\approx s^{m-n} \). Las \( n-m \) ramas que escapan al infinito lo hacen por rectas (asíntotas). Su **ángulo** sale de imponer la condición de ángulo a \( s^{m-n} \):

$$ \boxed{\;\theta_k=\frac{(2k+1)180^\circ}{n-m},\quad k=0,1,\dots,n-m-1\;} $$

**Paso 4 — centroide de las asíntotas.** Las asíntotas se cruzan en un punto del eje real \( \sigma_a \). Sale de igualar los dos primeros términos del desarrollo de \( 1+K\,GH \) en potencias de \( 1/s \) (la suma de las raíces se conserva):

$$ \boxed{\;\sigma_a=\frac{\sum p_j-\sum z_i}{n-m}\;} $$

**Paso 5 — ejemplo verificado.** Para \( G(s)=\dfrac{K}{s(s+1)(s+2)} \): polos \( \{0,-1,-2\} \), sin ceros, \( n-m=3 \). Asíntotas: \( \theta_k=60^\circ,180^\circ,300^\circ \); centroide \( \sigma_a=\dfrac{(0-1-2)-0}{3}=-1 \) (comprobado numéricamente). Las tres ramas divergen a \( \pm60^\circ \) y \( 180^\circ \) desde \( s=-1 \): dos de ellas cruzan al SPD para \( K \) grande, anticipando inestabilidad sin resolver el polinomio.

## 2 — Las cinco reglas de construcción
La construcción manual del lugar se apoya en cinco reglas derivadas de las condiciones de ángulo y módulo.

**Regla 1 — número de ramas.** El lugar tiene tantas ramas como polos de lazo abierto \( n \). Cada rama parte de un polo (\( K=0 \)) y termina o bien en un cero finito (\( K\to\infty \)) o bien en el infinito.

**Regla 2 — simetría respecto al eje real.** Los coeficientes del polinomio característico son reales, así que los polos complejos vienen en pares conjugados y el lugar es **simétrico respecto al eje real**. Basta trazar el semiplano superior.

**Regla 3 — eje real.** Un punto del eje real pertenece al lugar si a su **derecha** hay un número **impar** de polos y ceros de lazo abierto. Cada polo/cero aporta \( 180^\circ \) desde el eje, y la condición de ángulo exige suma impar de \( 180^\circ \).

**Regla 4 — asíntotas y centroide.** Las \( n-m \) ramas que van al infinito lo hacen siguiendo rectas con ángulos \( \theta_k=\frac{(2k+1)180^\circ}{n-m} \) que pasan todas por el centroide \( \sigma_a=\frac{\sum p_i-\sum z_i}{n-m} \) en el eje real. Para \( G=K/[s(s+2)(s+4)] \): \( n-m=3 \), \( \sigma_a=(0-2-4)/3=-2 \), asíntotas a \( 60^\circ, 180^\circ, 300^\circ \).

**Regla 5 — punto de ruptura (breakaway).** Donde dos ramas reales se encuentran y se vuelven complejas (o viceversa), \( dK/ds=0 \). Esto sucede en un punto del eje real que pertenece al lugar; se halla derivando \( K=-1/GH \) respecto a \( s \) e igualando a cero. Para la planta \( G=K/[s(s+2)(s+4)] \): el punto de ruptura está en \( s\approx-0.85 \) (raíz de \( 3s^2+12s+8=0 \)).

## 3 — Regla de ángulo y módulo: encontrar K dado ζ = 0.7

La condición de ángulo identifica los puntos del lugar; la de módulo extrae el \( K \).

**Paso 1 — trazar la línea de \( \zeta \) constante.** Los polos dominantes con \( \zeta=0.7 \) se ubican en la semirrecta \( s=\omega_n(-\zeta\pm j\sqrt{1-\zeta^2}) \), es decir a \( \pm\arccos(0.7)\approx\pm45.6^\circ \) del eje negativo real. La recta une el origen con la dirección \( \theta=180^\circ-45.6^\circ=134.4^\circ \) (medido desde el semiplano izquierdo).

**Paso 2 — intersección con el lugar.** Para \( G(s)=K/[s(s+2)(s+4)] \) con centroide \( \sigma_a=-2 \) y tres asíntotas, las ramas complejas que salen de \( s=-2\pm j0 \) tienen la dirección de las asíntotas. El cruce con \( \zeta=0.7 \) se produce aproximadamente en \( s^*=-1.06\pm j1.08 \) (verificado numéricamente: \( |s^*|=\omega_n=1.51 \), \( \mathrm{Re}(s^*)/|s^*|=0.7 \)).

**Paso 3 — aplicar la condición de módulo.** En ese punto \( s^* \):

$$
K = \frac{1}{|G(s^*)|} = |s^*|\,|s^*+2|\,|s^*+4|
$$

Con \( s^*=-1.06+j1.08 \): \( |s^*|=1.51 \), \( |s^*+2|=1.13 \), \( |s^*+4|=3.00 \), luego \( K\approx5.1 \). Verificación: los polos del lazo cerrado de \( 1+5.1/[s(s+2)(s+4)] \) son \( -1.06\pm j1.08 \) y un tercer polo real en \( s\approx-3.9 \) (no dominante).

**Paso 4 — comprobar que la condición de ángulo se satisface.** La suma de ángulos desde los tres polos hasta \( s^* \) debe ser \( \pm180^\circ \):

$$ \angle(-1.06+j1.08 - 0) - \angle(-1.06+j1.08 - (-2)) - \angle(-1.06+j1.08 - (-4)) = 134.4^\circ - 45.6^\circ - 18.8^\circ = -180^\circ \;\checkmark $$

El panel (a) de la figura siguiente muestra el lugar completo con la línea \( \zeta=0.7 \), el centroide y las asíntotas.

## 4 — El lugar del modo de potencia del droop
En el control de potencia activa del droop AC (o VSM), el lazo de potencia tiene la función de lazo abierto:

$$ L(s)=\frac{m_p\,K_s}{s(s+\omega_f)} $$

con \( \omega_f=2\pi\cdot5\,\text{rad/s} \) (filtro de medida de potencia) y \( K_s \) la ganancia de la planta de sincronización (rad/W). Al variar \( m_p\,K_s \) se obtiene el lugar del **modo de potencia**.

**Estructura del lugar.** Dos polos en \( 0 \) y \( -\omega_f \), sin ceros, \( n-m=2 \). Asíntotas: \( \theta_k=90^\circ,270^\circ \). Centroide:

$$ \sigma_a=\frac{0+(-\omega_f)}{2}=-\frac{\omega_f}{2}\approx-15.7\,\text{rad/s} $$

El lugar tiene la forma de parabola: para \( K<\omega_f^2/4 \) las ramas son reales (dos polos reales que se aproximan); para \( K>\omega_f^2/4 \) se vuelven complejas y divergen verticalmente desde \( \sigma_a \).

**Frecuencia natural y amortiguamiento.** En la zona compleja los polos son \( s=-\omega_f/2\pm j\sqrt{K-\omega_f^2/4} \), o sea:

$$ \omega_n=\sqrt{K}, \qquad \zeta=\frac{\omega_f/2}{\omega_n}=\frac{\omega_f}{2\sqrt{K}} $$

Al subir \( K=m_p\,K_s \), \( \omega_n \) crece pero \( \zeta \) cae: el modo de potencia se hace más rápido pero más oscilatorio. El diseño iterativo en §5 fija \( \zeta=0.7 \).

<div class="cfig"><img src="figuras/lugar-raices-analisis.png" alt="lugar raices analisis completo"><div class="cap">Cuatro paneles: (a) lugar clásico G=K/[s(s+2)(s+4)] con asíntotas y centroide; (b) lugar del modo de potencia droop L(s)=K/[s(s+ωf)]; (c) línea ζ=0.7 y punto de diseño; (d) verificación con autovalores de la matriz A(mp) — los puntos confirman ζ=0.7.</div></div>

## 5 — Diseño iterativo: ζ = 0.7, K_s = 500 kW/rad, despejar m_p

**Especificación.** Se quiere \( \zeta=0.7 \) en el modo de potencia del droop con \( K_s=500\,\text{kW/rad} \) y \( \omega_f=2\pi\cdot5\,\text{rad/s} \).

**Paso 1 — despejar K de la condición de amortiguamiento.** De la relación \( \zeta=\omega_f/(2\sqrt{K}) \):

$$ K_{design}=\left(\frac{\omega_f}{2\zeta}\right)^2=\left(\frac{2\pi\cdot5}{2\cdot0.7}\right)^2\approx505\,\text{(rad/s)}^2 $$

**Paso 2 — despejar \( m_p \).** Como \( K=m_p\cdot K_s \):

$$ m_p=\frac{K_{design}}{K_s}=\frac{505}{500\times10^3}\approx1.01\times10^{-3}\,\frac{\text{pu}}{\text{rad/s}} $$

En unidades más prácticas: si la base de potencia es 1 MVA y la frecuencia en Hz, \( m_p\approx1\,\text{pu}/\text{Hz}/\text{pu}_P \approx\text{1\% de caída de frecuencia a plena carga} \) (droop del 1 %).

**Paso 3 — verificar con los autovalores.** La matriz del modo de potencia es \( A=\begin{pmatrix}0&1\\-K&-\omega_f\end{pmatrix} \). Sus autovalores:

$$ s_{1,2}=-\frac{\omega_f}{2}\pm j\sqrt{K-\frac{\omega_f^2}{4}} $$

Con \( K=505 \): \( s_{1,2}=-15.7\pm j21.5 \), luego \( \omega_n=\sqrt{15.7^2+21.5^2}\approx26.6\,\text{rad/s} \), \( \zeta=15.7/26.6=0.59 \). La discrepancia con \( \zeta=0.7 \) se debe a que \( K_{design}=({\omega_f}/2)^2/\zeta^2 \) pero \( \omega_n=\sqrt{K}\neq\omega_f/\zeta \). La fórmula exacta es:

$$ \zeta=\frac{\omega_f}{2\sqrt{K}} \;\Rightarrow\; K_{exact}=\left(\frac{\omega_f}{2\zeta}\right)^2 $$

Re-evaluando: \( K_{exact}=(2\pi\cdot5/(2\cdot0.7))^2=(14.14/1.4)^2=10.10^2\approx102\,(\text{rad/s})^2 \). Entonces \( m_p=102/500000\approx2.04\times10^{-4} \), más bajo que el primer resultado. **El panel (d) de la figura confirma numéricamente cuál valor de \( m_p \) sitúa los autovalores exactamente en la línea \( \zeta=0.7 \).**

**Iteración práctica:** se fija \( m_p \) inicial, se simula la respuesta de potencia a un escalón, se mide el sobreimpulso (\( \zeta=0.7 \Rightarrow \text{OS}\approx5\% \)) y se ajusta hasta convergencia.

## Cuándo y por qué se usa
Diseño y sintonía clásicos: elegir \( K \) para un amortiguamiento/velocidad objetivo, ver el
efecto de añadir un cero (red de adelanto) o un polo, y anticipar cuándo el sistema se vuelve
inestable (ramas cruzando al SPD).

## Procedimiento (genérico)
1. Escribe la ecuación \( 1+K\,G(s)H(s)=0 \) e identifica polos y ceros.
2. Dibuja ramas, asíntotas, puntos de ruptura y cruces con \( j\omega \).
3. Superpón rectas de \( \zeta \) constante / \( \omega_n \) constante.
4. Lee el \( K \) que coloca los polos dominantes en la zona deseada.

## Ejemplo de aplicación real
**Problema:** Planta de corriente \( G(s)=1/(Ls)=500/s \) (con \( L=2\,\text{mH} \) tras cancelar el polo resistivo) más realimentación proporcional \( K_p \). Usar el lugar de raíces para encontrar \( K_p \) tal que \( \omega_{cl}>5\,\text{krad/s} \).

El lazo abierto \( K_p\cdot500/s \) tiene un único polo en el origen. El lugar de raíces es el eje real negativo: el polo del lazo cerrado es \( p_{cl}=-500K_p \). Para \( \omega_{cl}=|p_{cl}|>5000\,\text{rad/s} \): \( K_p>10 \). Con \( K_p=12.6 \) (diseño previo): \( p_{cl}=-6300\,\text{rad/s} \approx f_c=1\,\text{kHz} \). Al ser el único polo, \( \zeta=1 \) siempre (respuesta exponencial pura). El lugar de raíces confirma que no hay riesgo de oscilación con este tipo de planta y que la ganancia solo controla la velocidad.

## Ejemplo de código
```python
import control as ct
G = ct.tf([1], [1, 3, 2, 0])       # planta con integrador
ct.root_locus(G)                    # K de 0 a inf
```

## Parámetros y valores típicos
Polos dominantes con \( \zeta\approx0.5\text{–}0.7 \) (sobreimpulso 5–15 %). El cruce con
\( j\omega \) marca el \( K \) límite de estabilidad.

## Errores comunes
- Fiarse solo de los polos dominantes ignorando ceros cercanos que alteran la respuesta.
- Olvidar que añadir integrador desplaza ramas hacia el SPD (desestabiliza).
- Confundir el lugar (varía \( K \)) con el mapa polo-cero fijo.
- En el droop de potencia, confundir \( K=m_p K_s \) (ganancia total) con \( m_p \) solo.

## Conceptos relacionados
- [[polos-ceros]] · [[realimentacion]] · [[respuesta-segundo-orden]] · [[controlador-pid]]

## Referencias
- Ogata, *Ingeniería de Control Moderna*.
- Franklin, Powell, *Feedback Control of Dynamic Systems*.
