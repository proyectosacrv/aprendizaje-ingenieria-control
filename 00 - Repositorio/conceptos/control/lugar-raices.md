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
fecha_actualizacion: 2026-06-30
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

## Conceptos relacionados
- [[polos-ceros]] · [[realimentacion]] · [[respuesta-segundo-orden]] · [[controlador-pid]]

## Referencias
- Ogata, *Ingeniería de Control Moderna*.
- Franklin, Powell, *Feedback Control of Dynamic Systems*.
