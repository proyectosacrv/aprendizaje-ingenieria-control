---
titulo: Convertidor back-to-back (dos VSC, bus DC común)
slug: convertidor-back-to-back
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: []
objetivos: [desacoplar dos sistemas AC con flujo de potencia bidireccional, modelar el bus DC compartido]
tags: [back-to-back, vsc, bus-dc, hvdc, eolica, full-converter, bidireccional, modelado]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-07-14
relacionados: [convertidor-vsc, dinamica-bus-dc, control-tension-bus-dc, eolica-mppt, modelo-bateria-bess, optimo-simetrico]
referencias:
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
  - "Teodorescu, Liserre, Rodríguez, Grid Converters for PV and Wind Power Systems, Wiley 2011"
---

## 1 — Definición y topología

Dos [[convertidor-vsc|VSC]] conectados por un **bus DC común** (condensador compartido). Cada convertidor
mira a un sistema AC distinto **a través de un filtro inductivo**; el bus DC los **desacopla** y permite
flujo de potencia **bidireccional** entre ambos lados. Es la topología base del aerogenerador
full-converter (Tipo 4), el convertidor de rotor del DFIG (Tipo 3), los accionamientos regenerativos y
el HVDC-VSC.

<div class="cfig"><img src="figuras/btb-topologia.png" alt="Topología del convertidor back-to-back: Red AC 1 - Filtro L1 - VSC1 - bus DC con condensador - VSC2 - Filtro L2 - Red AC 2"><div class="cap">Dos VSC unidos por un bus DC común (condensador \(C_{dc}\)). Cada convertidor mira a un sistema AC independiente a través de su filtro \(L\); el bus DC los desacopla y permite flujo de potencia bidireccional. La energía del condensador \(E=\tfrac{1}{2}C_{dc}V_{dc}^2\) actúa de pulmón entre ambos lados.</div></div>

Los dos VSC solo se "ven" a través del bus DC: el acoplamiento es puramente **energético**. La frecuencia,
la fase y la amplitud de la red AC 1 son completamente independientes de las de la red AC 2. Esta
independencia es la razón de ser de la topología: permite conectar un generador de velocidad variable
(frecuencia variable) a una red de frecuencia fija, o dos redes AC asíncronas entre sí (HVDC).

**Reparto de tareas habitual:**

| Convertidor | Nombre típico | Tarea principal |
|---|---|---|
| VSC1 (lado máquina o fuente) | MSC (*machine-side converter*) | Controla par / velocidad / MPPT |
| VSC2 (lado red) | GSC (*grid-side converter*) | Regula \(V_{dc}\) y \(Q\) hacia la red |

El GSC regula \(V_{dc}\) porque es el único grado de libertad que puede cerrar el balance de potencia del
bus DC: si el MSC inyecta más potencia de la que el GSC evacúa, \(V_{dc}\) sube, y viceversa.

**Aplicaciones principales:**
- Aerogenerador full-converter PMSG (Tipo 4): todo el flujo de potencia pasa por el back-to-back.
- DFIG (Tipo 3): solo la potencia de deslizamiento (\(\approx 30\,\%\) de \(P_{nom}\)) pasa por el convertidor.
- HVDC-VSC: interconexión asíncrona de dos redes AC a distintas frecuencias o fases.
- BESS ([[modelo-bateria-bess]]): batería + convertidor DC-DC + GSC.
- Accionamientos regenerativos: motor + convertidor de motor + convertidor de red.

El convertidor tiene dos lazos anidados: un **lazo de corriente** interno y rápido (apartado 2) y un
**lazo de tensión del bus DC** externo y lento (apartado 3). Cada apartado desarrolla primero el
**modelo** de su planta y luego el **control**.

---

## 2 — Lazo de corriente (interno): modelo y control

El lazo de corriente es el interno y rápido. Primero se **modela** la planta del lado AC (el filtro en
el marco dq) y luego se **controla** (VOC, desacoplo y PI de corriente).

### 2.1 — Modelo: el filtro y el circuito físico del lado AC

Entre cada VSC y su sistema AC hay un **filtro inductivo**. Su función es alisar la corriente: el VSC
impone una tensión **troceada** por el PWM (conmuta entre niveles discretos a \(f_{sw}\)), y la
inductancia del filtro integra esos escalones para entregar una corriente suave a la red. Esa
**inductancia \(L\)** (con su resistencia parásita \(R\)) es, además, la **planta** que verá el lazo de
corriente. Aquí se modela como filtro \(L\) simple; el filtro LCL de tercer orden (mejor atenuación pero
con resonancia) se trata en [[filtro-lcl]].

Para el GSC, el circuito equivalente en cada fase es la inductancia \(L\) con resistencia \(R\) entre la
tensión de salida del VSC \(v_{conv}\) y la tensión de red \(v_g\):

$$ v_{conv,a} = L\frac{di_a}{dt} + Ri_a + v_{g,a} $$

En forma matricial para las tres fases:

$$ L\frac{d}{dt}\begin{pmatrix}i_a\\i_b\\i_c\end{pmatrix} = \begin{pmatrix}v_{conv,a}\\v_{conv,b}\\v_{conv,c}\end{pmatrix} - \begin{pmatrix}v_{g,a}\\v_{g,b}\\v_{g,c}\end{pmatrix} - R\begin{pmatrix}i_a\\i_b\\i_c\end{pmatrix} $$

Esta ecuación está en frecuencia de red (50 Hz): las variables son sinusoidales en estado estacionario,
lo que hace difícil diseñar un controlador con error nulo usando un PI ordinario. Por eso se pasa a dq.

### 2.2 — Modelo: transformación de Clarke (abc → αβ)

La transformada de Clarke proyecta las tres fases sobre dos ejes ortogonales fijos en el espacio
(marco αβ estacionario). Para sistema equilibrado (sin componente de secuencia cero):

$$ \begin{pmatrix}i_\alpha\\i_\beta\end{pmatrix} = \frac{2}{3}\begin{pmatrix}1 & -\frac{1}{2} & -\frac{1}{2}\\ 0 & \frac{\sqrt{3}}{2} & -\frac{\sqrt{3}}{2}\end{pmatrix}\begin{pmatrix}i_a\\i_b\\i_c\end{pmatrix} $$

**De dónde salen las entradas.** Los tres devanados apuntan a \(0°,\,120°,\,240°\). El eje α se alinea con
la fase \(a\) y el eje β va \(90°\) adelantado. Cada componente es la **proyección** de las tres fases sobre
el eje:

- Fila α = \([\cos 0°,\,\cos 120°,\,\cos 240°] = [1,\,-\tfrac12,\,-\tfrac12]\).
- Fila β = \([\sin 0°,\,\sin 120°,\,\sin 240°] = [0,\,\tfrac{\sqrt3}{2},\,-\tfrac{\sqrt3}{2}]\).

El factor \(\tfrac{2}{3}\) es la convención **invariante en amplitud**: hace que una senoide de pico
\(\hat I\) en abc dé un vector de módulo \(\hat I\) en αβ (al sumar tres proyecciones desfasadas se acumula
un factor \(3/2\), que este \(2/3\) compensa).

Las ecuaciones en αβ conservan la misma estructura que en abc:

$$ L\frac{d}{dt}\begin{pmatrix}i_\alpha\\i_\beta\end{pmatrix} = \begin{pmatrix}v_{conv,\alpha}\\v_{conv,\beta}\end{pmatrix} - \begin{pmatrix}v_{g,\alpha}\\v_{g,\beta}\end{pmatrix} - R\begin{pmatrix}i_\alpha\\i_\beta\end{pmatrix} $$

Las variables en αβ siguen siendo sinusoidales (rotan a \(\omega_0\) en el plano αβ), así que el PI
todavía tendría error en estado estacionario. Se necesita el siguiente paso.

### 2.3 — Modelo: transformación de Park (αβ → dq)

El marco dq gira solidario con el vector de tensión de red a velocidad \(\omega_0 = 2\pi f_0\). La
transformación de Park es una rotación de ángulo \(\theta = \omega_0 t\):

$$ \begin{pmatrix}i_d\\i_q\end{pmatrix} = \begin{pmatrix}\cos\theta & \sin\theta\\ -\sin\theta & \cos\theta\end{pmatrix}\begin{pmatrix}i_\alpha\\i_\beta\end{pmatrix} $$

**Derivación del acoplamiento (fasor complejo).** Es más limpio agrupar cada par de ejes en un número
complejo: \(\underline{i}_{\alpha\beta} = i_\alpha + j\,i_\beta\) y \(\underline{i}_{dq} = i_d + j\,i_q\).
La rotación de Park equivale a multiplicar por \(e^{-j\theta}\), luego:

$$ \underline{i}_{dq} = \underline{i}_{\alpha\beta}\,e^{-j\theta} \quad\Longleftrightarrow\quad \underline{i}_{\alpha\beta} = \underline{i}_{dq}\,e^{j\theta} $$

**Paso 1 — Ecuación en αβ en forma compleja:**

$$ L\frac{d\underline{i}_{\alpha\beta}}{dt} = \underline{v}_{conv,\alpha\beta} - \underline{v}_{g,\alpha\beta} - R\,\underline{i}_{\alpha\beta} $$

**Paso 2 — Sustituir \(\underline{i}_{\alpha\beta} = \underline{i}_{dq}e^{j\theta}\) y derivar el producto**
(regla del producto, con \(\dot\theta = \omega_0\)):

$$ \frac{d}{dt}\big(\underline{i}_{dq}e^{j\theta}\big) = \frac{d\underline{i}_{dq}}{dt}e^{j\theta} + \underline{i}_{dq}\,j\omega_0\,e^{j\theta} = e^{j\theta}\Big(\frac{d\underline{i}_{dq}}{dt} + j\omega_0\,\underline{i}_{dq}\Big) $$

El término \(j\omega_0\underline{i}_{dq}\) es el **que introduce la rotación del marco**: es el origen del acoplamiento.

**Paso 3 — Sustituir y dividir por \(e^{j\theta}\)** (aparece en los dos lados y se cancela):

$$ L\Big(\frac{d\underline{i}_{dq}}{dt} + j\omega_0\,\underline{i}_{dq}\Big) = \underline{v}_{conv,dq} - \underline{v}_{g,dq} - R\,\underline{i}_{dq} $$

$$ \Longrightarrow\quad L\frac{d\underline{i}_{dq}}{dt} = \underline{v}_{conv,dq} - \underline{v}_{g,dq} - R\,\underline{i}_{dq} - \underbrace{j\omega_0 L\,\underline{i}_{dq}}_{\text{acoplamiento}} $$

**Paso 4 — Separar en parte real (eje d) e imaginaria (eje q).** Con \(\underline{i}_{dq}=i_d+ji_q\):

$$ -j\omega_0 L\,\underline{i}_{dq} = -j\omega_0 L(i_d + j i_q) = \underbrace{\omega_0 L\,i_q}_{\text{real}} - \underbrace{j\,\omega_0 L\,i_d}_{\text{imag}} $$

(porque \(-j\cdot j = +1\)). La parte real da la ecuación del eje d y la imaginaria la del eje q:

$$ L\dot{i}_d = v_{d,conv} - v_{d,g} - Ri_d + \omega_0 L i_q $$

$$ L\dot{i}_q = v_{q,conv} - v_{q,g} - Ri_q - \omega_0 L i_d $$

Los signos opuestos (\(+\omega_0 L i_q\) en d, \(-\omega_0 L i_d\) en q) vienen directamente del \(-j\cdot j=+1\)
y del \(-j\cdot 1=-j\) del Paso 4.

En forma matricial compacta:

$$ L\frac{d}{dt}\begin{pmatrix}i_d\\i_q\end{pmatrix} = \begin{pmatrix}v_{d,conv}\\v_{q,conv}\end{pmatrix} - \begin{pmatrix}v_{d,g}\\v_{q,g}\end{pmatrix} - \begin{pmatrix}R & -\omega_0 L\\ \omega_0 L & R\end{pmatrix}\begin{pmatrix}i_d\\i_q\end{pmatrix} $$

**Resultado clave:** en el marco dq, las variables son **continuas** en estado estacionario, así que un
PI ordinario podrá regularlas con error nulo. El precio es el acoplamiento cruzado \(\pm\omega_0 L\,i\),
que hace que la planta sea **MIMO** (si \(i_d\) varía, perturba \(i_q\) y viceversa).

### 2.4 — Modelo: orientación del marco dq y la planta del lado AC

Se orienta el eje d alineado con el vector de tensión de red \(\vec{v}_g\). Con esta elección:

- \(v_{d,g} = |\vec{v}_g|\) (módulo de la tensión de red)
- \(v_{q,g} = 0\) (por definición de la orientación)

**De dónde salen \(P\) y \(Q\).** La potencia compleja trifásica es \(S = P + jQ = \tfrac{3}{2}\,\underline{v}_{dq}\,\underline{i}_{dq}^{\,*}\),
donde \(\underline{i}_{dq}^{\,*}\) es el conjugado. Desarrollando con \(\underline{v}_{dq}=v_{d,g}+jv_{q,g}\)
e \(\underline{i}_{dq}=i_d+ji_q\):

$$ S = \frac{3}{2}(v_{d,g}+jv_{q,g})(i_d - j i_q) = \frac{3}{2}\big[(v_{d,g}i_d + v_{q,g}i_q) + j(v_{q,g}i_d - v_{d,g}i_q)\big] $$

La parte real es \(P\) y la imaginaria \(Q\). El **\(3/2\)** viene de la Clarke invariante en amplitud (la
potencia de tres fases con la convención de pico). Con la orientación elegida (\(v_{q,g}=0\)):

$$ P = \frac{3}{2}(v_{d,g}i_d + v_{q,g}i_q) = \frac{3}{2}v_{d,g}i_d $$

$$ Q = \frac{3}{2}(v_{q,g}i_d - v_{d,g}i_q) = -\frac{3}{2}v_{d,g}i_q $$

Es decir, con esta orientación \(i_d\) fija la potencia **activa** \(P\) (y por tanto \(V_{dc}\)) e \(i_q\)
la **reactiva** \(Q\): ambas quedan separadas por la propia geometría del marco. (El signo \(-\) en \(Q\) es
solo convenio de orientación; con \(i_q<0\) el convertidor inyecta reactiva.)

<div class="cfig"><img src="figuras/btb-dq-transformacion.png" alt="Diagrama vectorial de los marcos abc, alfa-beta y dq girando con la tensión de red, y la orientación VOC con v_g sobre el eje d y la descomposición de la corriente en i_d e i_q"><div class="cap">Izquierda: los ejes fijos αβ y el marco dq que gira con \(\vec v_g\) a \(\theta=\omega_0 t\); por eso las componentes dq son continuas en régimen. Derecha: la orientación VOC alinea \(\vec v_g\) con el eje d (\(v_{q,g}=0\)), de modo que \(i_d\) fija la potencia activa \(P\) e \(i_q\) la reactiva \(Q\).</div></div>

Con todo lo anterior, la **planta del lado AC** que verá el control es el sistema MIMO de segundo orden:

$$ L\frac{d}{dt}\begin{pmatrix}i_d\\i_q\end{pmatrix} = \underbrace{\begin{pmatrix}v_{d,conv}\\v_{q,conv}\end{pmatrix}}_{\text{entrada (convertidor)}} - \underbrace{\begin{pmatrix}v_{d,g}\\v_{q,g}\end{pmatrix}}_{\text{perturbación (red)}} - \begin{pmatrix}R & -\omega_0 L\\ \omega_0 L & R\end{pmatrix}\begin{pmatrix}i_d\\i_q\end{pmatrix} $$

La diagonal es la rama RL (un \(1/(Ls+R)\) por eje si estuviera aislado); la antidiagonal \(\pm\omega_0 L\)
es el acoplamiento cruzado. Cancelar ese acoplamiento es ya tarea del control (siguientes subapartados).

### 2.5 — Control: estrategia VOC (Voltage Oriented Control)

Del modelo (2.4): con el eje d alineado con \(\vec v_g\), \(i_d\) manda sobre \(P\) e \(i_q\) sobre \(Q\).
El control aprovecha esa separación:

- **\(i_d^*\)** lo fija el lazo externo (el de \(V_{dc}\) en el GSC, o el de par/MPPT en el MSC).
- **\(i_q^*\)** lo fija la consigna de reactiva \(Q^*\) (o de tensión en el PCC).

Queda por resolver el acoplamiento cruzado \(\pm\omega_0 L\,i\) de la planta, que impediría tratar cada
eje por separado.

### 2.6 — Control: desacoplamiento feedforward

Las ecuaciones dq de la planta contienen \(+\omega_0 L i_q\) (eje d) y \(-\omega_0 L i_d\) (eje q). Para
que, vista desde el PI, la planta sean dos SISO independientes, se define la tensión de salida del
convertidor como suma de tres términos:

$$ v_{d,conv}^* = \underbrace{v_{d,PI}}_{\text{salida del PI}} + \underbrace{v_{d,g}}_{\text{FF tensión red}} - \underbrace{\omega_0 L\, i_q}_{\text{FF desacoplo}} $$

$$ v_{q,conv}^* = \underbrace{v_{q,PI}}_{\text{salida del PI}} + \underbrace{v_{q,g}}_{\text{FF tensión red}} + \underbrace{\omega_0 L\, i_d}_{\text{FF desacoplo}} $$

El signo del feedforward de desacoplo es **opuesto** al del término de acoplamiento físico: el eje d tiene
\(+\omega_0 L i_q\) → el feedforward mete \(-\omega_0 L i_q\); el eje q tiene \(-\omega_0 L i_d\) → el
feedforward mete \(+\omega_0 L i_d\). Así se cancelan exactamente.

**Sustitución en las ecuaciones dq.** Metiendo \(v_{d,conv}^* = v_{d,PI} + v_{d,g} - \omega_0 L i_q\) en la
ecuación del eje d:

$$ L\dot{i}_d = \underbrace{(v_{d,PI} + v_{d,g} - \omega_0 L i_q)}_{v_{d,conv}^*} - v_{d,g} - Ri_d + \omega_0 L i_q $$

- \(v_{d,g}\) del convertidor cancela el \(-v_{d,g}\) de la red: \(\checkmark\)
- \(-\omega_0 L i_q\) del feedforward cancela el \(+\omega_0 L i_q\) físico: \(\checkmark\)

$$ L\dot{i}_d = v_{d,PI} - Ri_d \implies \frac{I_d(s)}{V_{d,PI}(s)} = \frac{1}{Ls+R} $$

Ídem para el eje q, con \(v_{q,conv}^* = v_{q,PI} + v_{q,g} + \omega_0 L i_d\):

$$ L\dot{i}_q = v_{q,PI} - Ri_q \implies \frac{I_q(s)}{V_{q,PI}(s)} = \frac{1}{Ls+R} $$

<div class="cfig"><img src="figuras/btb-tensiones-explicacion.png" alt="Composición de la tensión de salida del convertidor en el eje d"><div class="cap">La tensión de salida del convertidor \(v_{d,conv}^*\) es la suma de tres contribuciones: la salida del PI \(v_{d,PI}\) (corrección del error de corriente), el feedforward de tensión de red \(v_{d,g}\) (cancela la perturbación de la red en la planta) y el feedforward de desacoplo \(-\omega_0 L i_q\) (cancela el acoplamiento cruzado físico del marco dq).</div></div>

**¿Qué señal hay justo antes de la planta y cómo se llama?** La entrada de la planta \(1/(Ls+R)\) **no** es
\(v_{d,conv}\), sino la **tensión neta sobre la rama RL del filtro**: la diferencia entre la tensión que
impone el convertidor y la de la red,

$$ v_{L,d} = v_{d,conv} - v_{d,g} $$

Es la tensión que "empuja" la corriente a través de la inductancia (por eso a veces se llama **tensión
sobre la inductancia**, \(v_L\)). La ecuación física del filtro es \(L\dot{i}_d + R\,i_d = v_{d,conv} -
v_{d,g}\), y por eso la planta corriente/tensión es exactamente \(I_d(s)/\big(V_{d,conv}(s)-V_{d,g}(s)\big)
= 1/(Ls+R)\). En el diagrama, el nudo de resta \(-v_{d,g}\) delante de la planta representa esa caída neta.

**¿Por qué se suma \(v_g\) en el feedforward y luego se resta antes de la planta?** Son dos cosas distintas
en dos sitios distintos: una es **física** y la otra es **control**.

- El nudo de **resta** (\(-v_{d,g}\)) **no es una acción del control**: es el circuito real. La red se
  opone con su propia tensión y, por Kirchhoff, lo que ve la inductancia es \(v_{d,conv}-v_{d,g}\). Esa
  \(v_{d,g}\) entra sí o sí como **perturbación**.
- El **feedforward** (\(+v_{d,g}\)) es la compensación: como sabemos que el circuito nos va a restar
  \(v_{d,g}\), la **añadimos por adelantado** a la referencia del convertidor para que se cancele.

$$ v_{d,conv} - v_{d,g} = (v_{d,PI} + v_{d,g} - \omega_0 L i_q) - v_{d,g} = v_{d,PI} - \omega_0 L i_q $$

La \(v_{d,g}\) **desaparece**: el PI ya no pelea contra la tensión de red, solo ve la planta RL limpia. Sin
este feedforward, cada cambio de \(v_{d,g}\) (huecos, variaciones de red) sería un error que el PI tendría
que corregir *a posteriori*, más lento. El término \(-\omega_0 L i_q\) hace lo mismo para el acoplamiento
cruzado d↔q.

**Resultado:** tras el desacoplo, ambos ejes se rigen por la misma planta de primer orden:

$$ \boxed{G_i(s) = \frac{1}{Ls + R}} $$

El sistema MIMO acoplado se reduce a **dos lazos SISO idénticos**. Cada PI solo ve su propio eje.

<div class="cfig"><img src="figuras/btb-diagramas-bloques.png" alt="Lazo de corriente en dq con desacoplo feedforward: referencia, error, PI, feedforward de tensión de red y de desacoplo, VSC+PWM y planta 1/(Ls+R)"><div class="cap">Lazo de corriente representado una sola vez en dq: tras el desacoplo, los ejes d y q son idénticos y ven la planta escalar \(1/(Ls+R)\). En verde el feedforward de tensión de red \(+v_{dq,g}\) y en naranja el de desacoplo \(\mp\omega_0 L\,i_{qd}\) (procedente del otro eje). El signo del desacoplo es \(-\omega_0 L i_q\) en el eje d y \(+\omega_0 L i_d\) en el eje q.</div></div>

**Condición de validez:** el desacoplo es exacto si \(i_d\) e \(i_q\) medidas son exactas (sin ruido ni
retardo). En la práctica, el retardo de muestreo introduce un error pequeño que se tolera si
\(\omega_{ci} \ll \omega_s\) (ancho de banda del lazo de corriente mucho menor que la frecuencia de
muestreo).

### 2.7 — Control: lazo de corriente y diseño del PI

Con el desacoplo, la planta es \(G_i(s) = 1/(Ls+R)\) en cada eje. El controlador PI es:

$$ C_{PI}(s) = K_p \frac{T_i s + 1}{T_i s} $$

**FdT de lazo abierto:**

$$ L_i(s) = C_{PI}(s) \cdot G_i(s) = K_p\frac{T_i s + 1}{T_i s} \cdot \frac{1}{Ls+R} $$

**Cancelación del polo de la planta.** Primero se pone la planta en forma de constante de tiempo dividiendo
numerador y denominador por \(R\): \(\dfrac{1}{Ls+R} = \dfrac{1/R}{(L/R)s+1}\), con polo en \(s=-R/L\).
Eligiendo el cero del PI igual a ese polo, \(T_i = L/R\), el factor \((T_i s+1)\) del PI cancela el
\(((L/R)s+1)\) de la planta:

$$ L_i(s) = K_p \frac{T_i s + 1}{T_i s} \cdot \frac{1/R}{(L/R)s+1} = \frac{K_p}{T_i R} \cdot \frac{1}{s} $$

y como \(T_i R = (L/R)R = L\), queda un **integrador puro**:

$$ L_i(s) = \frac{K_p}{L}\cdot\frac{1}{s} $$

**Lazo cerrado.** Con \(L_i = (K_p/L)/s\), la FdT de lazo cerrado (realimentación unitaria) se obtiene
multiplicando numerador y denominador por \(s\):

$$ T_i(s) = \frac{L_i}{1+L_i} = \frac{(K_p/L)/s}{1 + (K_p/L)/s} = \frac{K_p/L}{s + K_p/L} = \frac{\omega_{ci}}{s + \omega_{ci}} $$

un **primer orden** con frecuencia de cruce (= ancho de banda) \(\omega_{ci} = K_p/L\).

**Sintonía por método IMC.** La idea del control interno por modelo es **imponer** que el lazo cerrado sea
ese primer orden \(\omega_{ci}/(s+\omega_{ci})\) y despejar el PI. De \(\omega_{ci}=K_p/L\) sale \(K_p\), y
la cancelación fija \(T_i\):

$$ \boxed{K_p = \omega_{ci} L, \qquad T_i = \frac{L}{R}, \qquad K_i = \frac{K_p}{T_i} = \omega_{ci} R} $$

<div class="cfig"><img src="figuras/btb-lazo-corriente-bode.png" alt="Bode del lazo de corriente: la planta 1/(Ls+R) con polo en R/L, el PI con cero en R/L más integrador, y el lazo abierto resultante que es un integrador puro con cruce en omega_ci y fase plana en -90 grados"><div class="cap">Cancelación de polo en el lazo de corriente. El cero del PI (\(1/T_i=R/L\)) cae justo sobre el polo de la planta (\(R/L\)) y lo cancela: el lazo abierto queda como el integrador puro \(L_i=\omega_{ci}/s\) (azul oscuro), que cruza 0 dB en \(\omega_{ci}\) con la fase plana en \(-90°\) → \(PM=90°\).</div></div>

**Selección de \(\omega_{ci}\).** Dos restricciones:

**Superior** — no excitar la conmutación ni el rizado de la portadora PWM:
$$ \omega_{ci} < \frac{\omega_{sw}}{10} $$

**Inferior** — separación de escalas con el lazo DC (el de corriente debe ser mucho más rápido para que el
DC pueda asumir que la corriente sigue la referencia al instante):
$$ \omega_{ci} > 10 \cdot \omega_{dc} $$

**Ejemplo:** \(f_{sw} = 3\,\text{kHz}\), \(\omega_{sw} = 18850\,\text{rad/s}\) → \(\omega_{ci} < 1885\,\text{rad/s}\)
→ elegir \(\omega_{ci} = 1885\,\text{rad/s}\) (300 Hz).

**Margen de fase.** Con cancelación exacta del polo, la FdT de lazo abierto es un integrador puro \(K/s\)
→ \(PM = 90°\). En la práctica, el retardo del modulador PWM y del muestreo lo reducen a 60°–75°.

---

## 3 — Lazo de tensión del bus DC (externo): modelo y control

El lazo externo del GSC regula la tensión del bus DC generando la referencia \(i_d^*\) del lazo de
corriente. Primero se **modela** la dinámica del bus y luego se **controla**.

### 3.1 — Modelo: dinámica del bus DC

Nomenclatura (constante en todo el apartado): \(P_{MSC}\) es la potencia que **entra** al bus desde el
lado máquina y \(P_{GSC}\) la que **sale** hacia la red por el GSC.

**Paso 1 — Balance de energía en el condensador.** La energía almacenada es \(E = \tfrac{1}{2}C_{dc}V_{dc}^2\)
y su derivada es la potencia neta que carga el condensador:

$$ \frac{dE}{dt} = P_{MSC} - P_{GSC} - P_{losses} $$

Desarrollando la derivada \(\dfrac{dE}{dt} = \dfrac{d}{dt}\!\left(\tfrac{1}{2}C_{dc}V_{dc}^2\right) = C_{dc}V_{dc}\dfrac{dV_{dc}}{dt}\)
(despreciando \(P_{losses}\)):

$$ C_{dc}\,V_{dc}\,\frac{dV_{dc}}{dt} = P_{MSC} - P_{GSC} $$

En equilibrio \(P_{MSC} \approx P_{GSC}\) y \(V_{dc}\) es constante; la energía del condensador actúa de
pulmón (ver [[dinamica-bus-dc]] para la estabilidad con CPL).

**Paso 2 — Linealización exacta con \(w = V_{dc}^2\).** La ecuación es **no lineal** (producto \(V_{dc}\dot V_{dc}\)).
Con el cambio de variable \(w = V_{dc}^2\), su derivada es \(\dot{w} = 2V_{dc}\dot{V}_{dc}\), de donde
\(V_{dc}\dot V_{dc} = \tfrac{1}{2}\dot w\). Sustituyendo:

$$ C_{dc}\cdot\frac{1}{2}\dot{w} = P_{MSC} - P_{GSC} \quad\Longrightarrow\quad \dot{w} = \frac{2}{C_{dc}}\big(P_{MSC} - P_{GSC}\big) $$

**Paso 3 — La planta es un integrador.** Pasando a Laplace (variables incrementales, \(s\,\tilde w = \dot w\)):

$$ s\,\tilde{w}(s) = \frac{2}{C_{dc}}\big(\tilde{P}_{MSC}(s) - \tilde{P}_{GSC}(s)\big)
   \quad\Longrightarrow\quad
   \boxed{\;\tilde{w}(s) = \frac{2}{C_{dc}\,s}\big(\tilde{P}_{MSC}(s) - \tilde{P}_{GSC}(s)\big),\qquad G_{dc}(s) = \frac{2}{C_{dc}\,s}\;} $$

La linealización no es una aproximación: la no linealidad de \(V_{dc}^2\) se elimina por completo con el
cambio de variable, así que el PI que se diseñe sobre \(w\) será lineal y sus márgenes, exactos.

**Paso 4 — Manipulada vs perturbación.** La planta tiene **dos** entradas de potencia por el mismo
integrador \(2/(C_{dc}s)\), una con \(+\) (carga) y otra con \(-\) (descarga). El lazo usa solo una como
**mando**: en el GSC que regula el bus, la **variable manipulada** es \(P_{GSC}\) (el PI comanda
\(i_d\to P_{GSC}\)) y la **perturbación** es \(P_{MSC}\), que fija el viento. Por eso, al escribir la FdT
de lazo se toma \(P_{GSC}\) como entrada — \(\tilde w/\tilde P_{GSC} = -2/(C_{dc}s)\), el signo \(-\) solo
fija el sentido del lazo — y \(P_{MSC}\) entra aparte como perturbación (que el feedforward de 3.3
cancela). Es el mismo patrón que \(v_g\) en el lazo de corriente.

### 3.2 — Control: lazo de tensión con PI

**Paso 1 — Estructura del PI.** El PI opera sobre el error \(e_w = w^* - w\) con \(w^* = V_{dc}^{*2}\):

$$ C_{dc}^{ctrl}(s) = K_{p,dc}\frac{T_{i,dc}s + 1}{T_{i,dc}s} $$

**Paso 2 — FdT de lazo abierto.** El lazo abierto es el controlador por la planta \(G_{dc}=2/(C_{dc}s)\):

$$ L_{dc}(s) = C_{dc}^{ctrl}(s)\,G_{dc}(s) = K_{p,dc}\frac{T_{i,dc}s+1}{T_{i,dc}s} \cdot \frac{2}{C_{dc}s} = \frac{2K_{p,dc}}{C_{dc}T_{i,dc}} \cdot \frac{T_{i,dc}s+1}{s^2} $$

La planta es un integrador y el PI añade otro → **doble integrador** (\(1/s^2\)) en lazo abierto. Sin el
cero, la fase sería \(-180°\) a todas las frecuencias (margen nulo, inestable). El cero del PI
\(s = -1/T_{i,dc}\) aporta la fase avanzante que estabiliza; su posición relativa a \(\omega_{dc}\) fija el
margen. Este es el caso típico del **[[optimo-simetrico|óptimo simétrico]]**.

**Paso 3 — Módulo y fase de \(L_{dc}(j\omega)\) (de dónde sale cada término).** Se sustituye \(s=j\omega\) en
\(L_{dc}(s) = \dfrac{2K_{p,dc}}{C_{dc}T_{i,dc}}\cdot\dfrac{T_{i,dc}s+1}{s^2}\).

*Módulo.* El módulo de un producto/cociente es el producto/cociente de los módulos, así que se trata cada
factor por separado:

- La constante \(\dfrac{2K_{p,dc}}{C_{dc}T_{i,dc}}\) es real positiva → su módulo es ella misma.
- El numerador \(1+j\,T_{i,dc}\omega\) es un complejo de parte real \(1\) y parte imaginaria \(T_{i,dc}\omega\);
  su módulo es \(\sqrt{\text{Re}^2+\text{Im}^2}=\sqrt{1+(T_{i,dc}\omega)^2}\) → **de ahí la raíz**.
- El denominador \(s^2=(j\omega)^2=j^2\omega^2=-\omega^2\); su módulo es \(\omega^2\) → **de ahí el \(/\omega^2\)**.

$$ |L_{dc}(j\omega)| = \frac{2K_{p,dc}}{C_{dc}T_{i,dc}}\cdot\frac{\sqrt{1+(T_{i,dc}\omega)^2}}{\omega^2} $$

*Fase.* La fase de un producto/cociente es la suma/resta de las fases:

- La constante positiva aporta \(0°\).
- El numerador \(1+j\,T_{i,dc}\omega\) tiene fase \(\arctan\dfrac{\text{Im}}{\text{Re}}=\arctan(T_{i,dc}\omega)\)
  → **de ahí el arcotangente**.
- El denominador \(s^2=(j\omega)^2\): \(j\omega\) tiene fase \(+90°\), al cuadrado \(+180°\); como está en el
  denominador, **resta** \(180°\) → **de ahí el \(-180°\)**.

$$ \angle L_{dc}(j\omega) = 0 + \arctan(T_{i,dc}\omega) - 180° = -180° + \arctan(T_{i,dc}\omega) $$

*Aproximación por encima del cero del PI.* Conviene explicar qué es "el cero del PI". El PI
\(C_{dc}(s)=K_{p,dc}\dfrac{T_{i,dc}s+1}{T_{i,dc}s}\) tiene un **cero** (una frecuencia donde su numerador se
anula) en \(T_{i,dc}s+1=0 \Rightarrow s=-1/T_{i,dc}\); su frecuencia es \(\omega_z = 1/T_{i,dc}\). Decir
"para frecuencias por encima del cero" es decir \(\omega > \omega_z = 1/T_{i,dc}\), y eso es exactamente la
condición \(T_{i,dc}\,\omega > 1\) (con \(\gg 1\) si es **bastante** por encima). El porqué físico: por
debajo de \(\omega_z\) domina el término **integral** del PI (el \(1/(T_{i,dc}s)\), que añade \(-20\) dB/dec
y \(-90°\)); por encima de \(\omega_z\), el término \(T_{i,dc}s\) del numerador supera al \(1\) y domina la
parte **proporcional** (respuesta plana). El cero es, pues, la frecuencia de transición entre "integral" y
"proporcional".

En esa banda (\(T_{i,dc}\omega \gg 1\)), dentro de la raíz el \(1\) es despreciable frente a
\((T_{i,dc}\omega)^2\), así que \(\sqrt{1+(T_{i,dc}\omega)^2}\approx T_{i,dc}\omega\). Sustituyendo, el
\(T_{i,dc}\) se cancela:

$$ |L_{dc}(j\omega)| \approx \frac{2K_{p,dc}}{C_{dc}T_{i,dc}}\cdot\frac{T_{i,dc}\omega}{\omega^2} = \frac{2K_{p,dc}}{C_{dc}\,\omega} $$

Esta forma simplificada es válida en toda la banda por encima del cero del PI (\(\omega > 1/T_{i,dc}\)).

**Paso 4 — Separación de escalas: dónde se coloca el cruce \(\omega_{dc}\).** El diseño del lazo DC ha
supuesto que el lazo de corriente interno responde "al instante" (\(G_{cl}\approx 1\)). Para que eso sea
cierto, el lazo DC debe ser **mucho más lento** que el de corriente; la regla habitual es un factor 10:

$$ \boxed{\omega_{dc} = \frac{\omega_{ci}}{10}} $$

Aquí \(\omega_{ci}\) **no es libre**: ya se fijó al diseñar el lazo de corriente (apartado 2.7), acotada por
arriba por la conmutación (\(\omega_{ci} < \omega_{sw}/10\), para no excitar el rizado del PWM) y por abajo
por esta misma separación (\(\omega_{ci} > 10\,\omega_{dc}\)). En el ejemplo \(\omega_{ci}=1885\) rad/s
(\(=\omega_{sw}/10\)), luego \(\omega_{dc}=188.5\) rad/s. Además, el polo del lazo
de corriente cerrado \(G_{cl}=\omega_{ci}/(s+\omega_{ci})\) queda en \(\omega_{ci}=10\,\omega_{dc}\), es decir
**un factor 10 por encima** del cruce. Como todo polo de primer orden \(1/(1+s/\omega_{ci})\) aporta una
fase \(-\arctan(\omega/\omega_{ci})\), su retardo en el cruce es solo
\(\arctan(\omega_{dc}/\omega_{ci})=\arctan(0.1)\approx 5.7°\) (pequeño, pero no nulo).

**Paso 5 — Ganancia \(K_{p,dc}\) desde la condición de cruce.** Imponiendo \(|L_{dc}(j\omega_{dc})| = 1\) con
la forma simplificada del Paso 3:

$$ \frac{2K_{p,dc}}{C_{dc}\,\omega_{dc}} = 1 \quad\Longrightarrow\quad \boxed{K_{p,dc} = \frac{C_{dc}\,\omega_{dc}}{2}} $$

**Paso 6 — Tiempo integral \(T_{i,dc}\): el óptimo simétrico y su "factor".** El margen de fase (Paso 3) es
\(PM_{dc} = 180° + \angle L_{dc}(j\omega_{dc}) = \arctan(T_{i,dc}\,\omega_{dc})\), menos el retardo del lazo
de corriente. Depende **solo** del producto \(T_{i,dc}\,\omega_{dc}\), que tiene un significado geométrico:
como el cero del PI está en \(\omega_z=1/T_{i,dc}\),

$$ T_{i,dc}\,\omega_{dc} = \frac{\omega_{dc}}{1/T_{i,dc}} = \frac{\omega_{dc}}{\omega_z} $$

es **cuántas veces el cruce está por encima del cero del PI** (o, al revés, cuántos factores está el cero
por debajo del cruce). Por eso "situar el cero un factor \(a\) por debajo del cruce" **es** fijar
\(T_{i,dc}\,\omega_{dc}=a\); y entonces la fase avanzante que aporta el cero en el cruce —que **es** el
margen de fase, porque el doble integrador solo daría \(-180°\) (margen cero)— vale \(\arctan(a)\).

¿Qué \(a\) elegir? El **[[optimo-simetrico|óptimo simétrico]]** coloca el cero del PI y el polo rápido del
lazo (aquí el del lazo de corriente, en \(\omega_{ci}\)) **simétricos** respecto al cruce en escala
logarítmica: el cruce es su **media geométrica**. Del Paso 4, ese polo está un factor 10 por **encima** del
cruce (\(\omega_{ci}=10\,\omega_{dc}\)); la simetría obliga a poner el cero un factor 10 por **debajo**
(\(\omega_z=\omega_{dc}/10\)), es decir \(a=10\). Nótese que \(a\) coincide con la razón de separación de
escalas, \(a=\omega_{ci}/\omega_{dc}=10\):

$$ T_{i,dc}\,\omega_{dc}=a=10 \quad\Longrightarrow\quad \boxed{T_{i,dc} = \frac{10}{\omega_{dc}}} $$

**De dónde sale la resta de arcotangentes.** Hasta aquí la fase del Paso 3 (\(\angle L_{dc}=-180°+\arctan(T_{i,dc}\omega)\))
solo contaba el doble integrador y el cero del PI. Pero el lazo real lleva **además** el polo del lazo de
corriente \(G_{cl}=\dfrac{\omega_{ci}}{s+\omega_{ci}}\) (Paso 4). Ese polo, igual que cualquier factor
\(1/(1+s/\omega_{ci})\), aporta fase \(-\arctan(\omega/\omega_{ci})\) (negativa porque está en el
**denominador**, al revés que el cero del PI). La fase completa del lazo es entonces la **suma** de las tres
contribuciones:

$$ \angle L_{dc}(j\omega) = \underbrace{-180°}_{\text{doble integrador }1/s^2} + \underbrace{\arctan(T_{i,dc}\,\omega)}_{\text{cero PI (avanza)}} - \underbrace{\arctan(\omega/\omega_{ci})}_{\text{polo lazo corr. (retrasa)}} $$

El margen de fase es lo que le sobra a la fase sobre \(-180°\) en el cruce, \(PM_{dc}=180°+\angle L_{dc}(j\omega_{dc})\).
El \(-180°\) se cancela y quedan las **dos** arcotangentes; evaluando en \(\omega_{dc}\) con
\(T_{i,dc}\,\omega_{dc}=a\) (recién obtenido) y \(\omega_{dc}/\omega_{ci}=1/a\) (Paso 4):

$$ PM_{dc} = \underbrace{\arctan(T_{i,dc}\,\omega_{dc})}_{=\,\arctan a\ \text{(cero PI)}} - \underbrace{\arctan(\omega_{dc}/\omega_{ci})}_{=\,\arctan(1/a)\ \text{(polo corr.)}} = \arctan 10 - \arctan 0.1 \approx 84.3° - 5.7° \approx 79° $$

Es decir: el \(+\arctan(a)\) es la fase que **avanza el cero del PI** en el cruce (la que da el margen), y el
\(-\arctan(1/a)\) es la fase que **retrasa el polo del lazo de corriente** (pequeña porque ese polo está un
factor \(a=10\) por encima). El resultado es un lazo **muy amortiguado y robusto** (lo que interesa frente a
la CPL). El nombre "óptimo simétrico" viene precisamente de esa colocación simétrica del cero y el polo
alrededor del cruce.

<div class="cfig"><img src="figuras/btb-lazo-tension-bode.png" alt="Bode del lazo de tensión DC: doble integrador de pendiente -40 dB/dec que pasa a -20 dB/dec en el cero del PI, cruce en omega_dc entre el cero y el polo del lazo de corriente colocados simetricamente, con margen de fase de 79 grados"><div class="cap">Lazo de tensión DC. La planta \(2/(C_{dc}s)\) más el integral del PI dan un doble integrador (\(1/s^2\), \(-40\) dB/dec y \(-180°\)); el cero del PI en \(\omega_{dc}/10\) sube la pendiente a \(-20\) dB/dec y **levanta la fase**. El cero (\(\omega_{dc}/10\)) y el polo del lazo de corriente (\(\omega_{ci}=10\,\omega_{dc}\)) quedan **simétricos** respecto al cruce \(\omega_{dc}\) (media geométrica), dando el margen \(PM_{dc}=\arctan 10-\arctan 0.1\approx 79°\).</div></div>

### 3.3 — Control: feedforward de potencia y diagrama de bloques

**Paso 1 — El problema: por qué el lazo por sí solo es "lento" ante \(P_{MSC}\).**

*¿Qué significa "rápido" o "lento"?* La velocidad de un lazo la fija su **ancho de banda**, que es su
frecuencia de cruce (aquí \(\omega_{dc}\)). Un lazo **rápido** (ancho de banda alto) corrige lo que cambia
hasta frecuencias altas y su tiempo de respuesta es corto, del orden de \(1/\omega_{dc}\); uno **lento**
(ancho de banda bajo) solo sigue lo que varía despacio, y cualquier perturbación **más rápida** que
\(\omega_{dc}\) le "pasa por delante" antes de reaccionar. El lazo DC es lento **a propósito**:
\(\omega_{dc}=\omega_{ci}/10\) (separación de escalas, 3.2 Paso 4), así que su tiempo de respuesta
\(\sim 1/\omega_{dc}\) es unas 10 veces el del lazo de corriente.

*Cómo se cierra el lazo (deducción de la respuesta a la perturbación).* De la planta del bus (3.1), la
tensión sale de integrar la **potencia neta**:

$$ \tilde w = G_{dc}\,(\tilde P_{MSC} - \tilde P_{GSC}), \qquad G_{dc}(s)=\frac{2}{C_{dc}s} $$

Aquí \(P_{MSC}\) es la **perturbación** (la fija el viento) y \(P_{GSC}\) la **manipulada** (la fija el
control). El lazo mide \(w\) y ajusta \(P_{GSC}\) para llevarlo a \(w^*\). Llamando \(L_{dc}(s)\) a la
**ganancia de lazo** —todo lo que recorre la señal en una vuelta: PI, lazo de corriente, conversión
\(i_d\to P_{GSC}\) y planta \(G_{dc}\), la misma \(L_{dc}\) de 3.2— el efecto de esa realimentación sobre
\(w\) es, por definición, \(-L_{dc}\,\tilde w\). Con \(w^*\) constante (\(\tilde w^*=0\)):

$$ \tilde w = G_{dc}\,\tilde P_{MSC} - L_{dc}\,\tilde w \;\;\Longrightarrow\;\; \tilde w\,(1+L_{dc}) = G_{dc}\,\tilde P_{MSC} $$

$$ \boxed{\ \frac{\tilde w}{\tilde P_{MSC}} = \frac{G_{dc}}{1+L_{dc}} = S(s)\,G_{dc}\ }, \qquad S(s)=\frac{1}{1+L_{dc}(s)} $$

*Qué es la sensibilidad \(S\).* \(S(s)=1/(1+L_{dc})\) es la **función de sensibilidad** ([[funciones-sensibilidad]]),
que mide **cuánta perturbación se cuela** a la salida a cada frecuencia:

- Donde el lazo tiene **mucha ganancia** (\(|L_{dc}|\gg1\), a **bajas** frecuencias, por debajo de
  \(\omega_{dc}\)): \(S\approx 1/L_{dc}\to 0\) → la perturbación se **rechaza** bien.
- Donde el lazo tiene **poca ganancia** (\(|L_{dc}|\ll1\), a **altas** frecuencias, por encima de
  \(\omega_{dc}\)): \(S\approx 1\) → la perturbación **pasa entera**.

Por eso el lazo solo rechaza \(P_{MSC}\) por debajo de \(\omega_{dc}\). Un **escalón** de \(P_{MSC}\)
contiene componentes de todas las frecuencias, incluidas las de por encima de \(\omega_{dc}\): esas se
cuelan y hacen que \(V_{dc}\) se desvíe transitoriamente hasta que el (lento) PI alcanza a corregir, en un
tiempo \(\sim 1/\omega_{dc}\).

**Paso 2 — Cuánta cae \(V_{dc}\): el argumento energético.**

*¿Qué es y por qué se usa?* En vez de resolver la respuesta temporal exacta de \(\tilde w/\tilde P_{MSC}\)
(que se puede, pero es farragosa), se estima el **pico de caída** con un balance de energía: es rápido,
físico, da la dependencia correcta con los parámetros y conecta directamente con el dimensionado del
condensador. El condensador es un **almacén de energía**, y durante el rato en que el control aún no ha
reaccionado toda la potencia sobrante entra o sale de él.

*Paso a paso:*

1. **Tiempo de reacción.** El lazo tarda \(\Delta t \approx 1/\omega_{dc}\) en responder (un lazo tarda del
   orden de un periodo de su ancho de banda). Durante ese rato \(P_{GSC}\) todavía no se ha ajustado, así
   que el desbalance completo \(\Delta P = P_{MSC}-P_{GSC}\approx \Delta P_{MSC}\) va íntegro al condensador.
2. **Energía que absorbe el condensador.** Potencia por tiempo:

   $$ \Delta E = \Delta P\,\Delta t $$

3. **Esa energía cambia la del condensador.** Con \(E=\tfrac12 C_{dc}V_{dc}^2\), un cambio de tensión
   \(\Delta V_{dc}\) supone

   $$ \Delta E = \tfrac12 C_{dc}\big[V_{dc}^2-(V_{dc}-\Delta V_{dc})^2\big] = \tfrac12 C_{dc}\big(2V_{dc}\Delta V_{dc}-\Delta V_{dc}^2\big) \approx C_{dc}V_{dc}\,\Delta V_{dc} $$

   (el \(\Delta V_{dc}^2\) es despreciable frente a \(2V_{dc}\Delta V_{dc}\) porque \(\Delta V_{dc}\ll V_{dc}\)).
4. **Igualar y despejar** la caída, usando \(\Delta t=1/\omega_{dc}\):

   $$ \Delta P\,\Delta t = C_{dc}V_{dc}\,\Delta V_{dc} \;\;\Longrightarrow\;\; \boxed{\ \Delta V_{dc} \approx \frac{\Delta P}{\omega_{dc}\,C_{dc}\,V_{dc}}\ } $$

*Qué implica.* La caída es **inversamente proporcional** a \(\omega_{dc}\) (lazo más lento → más caída) y a
\(C_{dc}\) (condensador más grande → menos caída). Con un lazo lento, mantener \(\Delta V_{dc}\) dentro de
límites obliga a un \(C_{dc}\) grande. La salida es acelerar la **reacción efectiva** ante \(P_{MSC}\) sin
tocar el lazo lento: eso es justo lo que hace el feedforward de los pasos siguientes (reduce el \(\Delta t\)
efectivo de \(1/\omega_{dc}\) a \(\sim 1/\omega_{ci}\), un factor 10, y con ello la caída y el \(C_{dc}\)).

**Paso 3 — ¿Por qué *se puede* hacer feedforward de la potencia?** Un feedforward de una perturbación
requiere tres condiciones, y \(P_{MSC}\) las cumple:

1. **Es medible/conocida** en tiempo real: el MSC mide sus tensiones y corrientes, así que
   \(P_{MSC} = \tfrac{3}{2}(v_{d,gen}i_{d,gen}+v_{q,gen}i_{q,gen})\) está disponible (ambos convertidores
   comparten controlador y bus).
2. **Hay un actuador directo y rápido** que la contrarresta: la potencia del GSC es un grado de libertad
   controlable, \(P_{GSC} = 1.5\,v_{d,g}\,i_d\), e \(i_d\) lo entrega el lazo de corriente interno (rápido).
3. **La relación es algebraica e invertible** (estática, sin dinámica que invertir): para dar una potencia
   \(P\) se necesita una corriente \(P/(1.5\,v_{d,g})\). Por eso el feedforward es realizable (propio) y
   exacto en régimen.

**Paso 4 — Ganancia del feedforward.** De la orientación VOC (2.4), la potencia activa del GSC es
\(P_{GSC} = \tfrac{3}{2}v_{d,g}i_d = 1.5\,v_{d,g}\,i_d\). Para que el GSC evacúe justo la potencia entrante
(\(P_{GSC} = P_{MSC}\)) al instante, la corriente de feedforward debe ser:

$$ i_{d,FF}^* = \frac{P_{MSC}}{1.5\,v_{d,g}} $$

**Paso 5 — Ley de control completa.** La referencia de corriente activa del GSC suma el PI (corrección
lenta: errores de estimación, pérdidas) y el feedforward (grueso de la potencia, al instante):

$$ \boxed{\,i_d^* = \underbrace{C_{dc}^{ctrl}(e_w)}_{\text{PI, }e_w=w^*-w} + \underbrace{\frac{P_{MSC}}{1.5\,v_{d,g}}}_{\text{feedforward}}\,} $$

**Paso 6 — Rechazo de la perturbación con feedforward (desarrollo).** Se incluye la dinámica del lazo de
corriente cerrado \(G_{cl}(s) = \dfrac{\omega_{ci}}{s+\omega_{ci}}\) y un filtro de feedforward \(F_{FF}(s)\).
La potencia del GSC realmente entregada es:

$$ P_{GSC} = 1.5\,v_{d,g}\,i_d = 1.5\,v_{d,g}\,G_{cl}\Big(i_{d,PI}^* + F_{FF}\frac{P_{MSC}}{1.5\,v_{d,g}}\Big)
   = 1.5\,v_{d,g}\,G_{cl}\,i_{d,PI}^* + G_{cl}F_{FF}\,P_{MSC} $$

La potencia **neta** que ve el condensador en el nudo de balance:

$$ P_{net} = P_{MSC} - P_{GSC} = \underbrace{P_{MSC}\big(1 - G_{cl}F_{FF}\big)}_{\text{perturbación efectiva}} - 1.5\,v_{d,g}\,G_{cl}\,i_{d,PI}^* $$

El factor **\((1 - G_{cl}F_{FF})\)** es lo que aporta el feedforward. Tres casos:

- **Sin feedforward** (\(F_{FF}=0\)): factor \(=1\), la perturbación entra entera → solo la rechaza el PI (lento).
- **Feedforward ideal** (\(F_{FF}=1\), \(G_{cl}=1\)): factor \(=1-1=0\) → **cancelación perfecta**.
- **Feedforward real** (\(F_{FF}=1\), \(G_{cl}=\tfrac{\omega_{ci}}{s+\omega_{ci}}\)):

$$ 1 - G_{cl} = 1 - \frac{\omega_{ci}}{s+\omega_{ci}} = \frac{s}{s+\omega_{ci}} $$

un **filtro paso-alto**: solo se cuela lo que cambia más rápido que \(\omega_{ci}\), y ese resto multiplica
al integrador \(2/(C_{dc}s)\) cancelando su polo en el origen. La perturbación deja de integrarse.

**Paso 7 — Efecto: la caída se reduce y \(C_{dc}\) se achica.** Con feedforward, el desbalance que ve el
condensador dura \(\sim 1/\omega_{ci}\) (retardo del lazo de corriente) en vez de \(\sim 1/\omega_{dc}\).
Por el mismo argumento energético del Paso 2:

$$ \Delta V_{dc} \approx \frac{\Delta P}{\omega_{ci}\,C_{dc}\,V_{dc}}, \qquad \frac{\omega_{ci}}{\omega_{dc}} = 10 $$

→ la caída es \(\sim 10\times\) menor; para la misma \(\Delta V_{dc}\) admisible, \(C_{dc}\) puede ser
**5–10 veces más pequeño**.

**Paso 8 — Filtro del feedforward.** \(P_{MSC}\) se estima de medidas ruidosas; se filtra con

$$ F_{FF}(s) = \frac{1}{T_{FF}s+1}, \qquad T_{FF} = \frac{1}{\omega_{ci}} $$

Elimina el ruido de medida sin ralentizar el feedforward respecto al lazo de corriente (mismo ancho de banda).

**Paso 9 — Desarrollo del diagrama de bloques.** El lazo se construye a partir de las ecuaciones anteriores:

1. Referencia \(w^* = V_{dc}^{*2}\) y error \(e_w = w^* - w\).
2. PI \(C_{dc}^{ctrl}(s)\) → corriente de corrección \(i_{d,PI}^*\).
3. Rama de feedforward: \(P_{MSC}\) → filtro \(F_{FF}\) → \(\div(1.5\,v_{d,g})\) → \(i_{d,FF}^*\).
4. Suma de referencias: \(i_d^* = i_{d,PI}^* + i_{d,FF}^*\).
5. Lazo de corriente cerrado \(G_{cl}(s)=\omega_{ci}/(s+\omega_{ci}) \approx 1\) (separación de escalas) → \(i_d\).
6. Conversión a potencia: \(\times\,1.5\,v_{d,g}\) → \(P_{GSC}\).
7. Nudo de balance: \(P_{MSC} - P_{GSC}\) = potencia neta.
8. Planta \(2/(C_{dc}s)\) → \(w\); raíz cuadrada → \(V_{dc}\), que se realimenta al error.

La clave del feedforward está en el nudo de balance: \(P_{MSC}\) llega por **dos caminos** — directo
(\(+\)) y por la rama de feedforward → \(i_d\) → \(\times 1.5\,v_{d,g}\) → \(P_{GSC}\) (\(-\)). Si el
feedforward es exacto y el lazo de corriente ideal, ambos se cancelan y la perturbación **nunca llega al
integrador**.

<div class="cfig"><img src="figuras/btb-lazo-dc.png" alt="Diagrama de bloques del lazo de tensión DC: PI sobre V_dc cuadrado, feedforward de potencia del MSC, lazo de corriente como ganancia unidad y planta integradora 2/(C_dc s)"><div class="cap">El PI actúa sobre el error de \(V_{dc}^2\) y genera la referencia de corriente activa del GSC. El feedforward de potencia \(P_{MSC}/(1.5\,v_{d,g})\) adelanta la corriente antes de que el condensador se descargue. El lazo de corriente interno se ve como ganancia unidad (separación de escalas \(\omega_{dc}=\omega_{ci}/10\)) y la planta es el integrador \(2/(C_{dc}s)\).</div></div>

**Características que debe cumplir el lazo DC:**

- **Separación de escalas:** \(\omega_{dc} = \omega_{ci}/10\) para que el lazo de corriente sea
  "instantáneo" desde el punto de vista del DC.
- **Margen de fase:** \(PM_{dc} \geq 45°\) para robustez ante variación de \(C_{dc}\) y ante la CPL.
- **Feedforward de \(P_{MSC}\):** imprescindible para no sobredimensionar \(C_{dc}\).
- **Anti-windup en el integrador:** cuando \(i_d^*\) satura (límite de corriente del GSC), el integrador
  del PI debe congelarse para no acumular error y generar sobretensión al salir de saturación.
- **Chopper de freno:** durante LVRT el GSC no puede evacuar potencia; el chopper disipa el exceso en una
  resistencia conectada al bus DC, manteniendo \(V_{dc} \leq 1.1\,V_{dc,0}\).

---

## 4 — Aplicación en eólica PMSG: desarrollo teórico completo

### 4.1 — El generador PMSG como fuente de potencia

El PMSG se modela en el marco dq del rotor (eje d alineado con el flujo del imán permanente). Las
ecuaciones del circuito equivalente en dq son:

$$ L_d\dot{i}_{d,gen} = v_{d,gen} - R_s i_{d,gen} + \omega_r L_q i_{q,gen} $$

$$ L_q\dot{i}_{q,gen} = v_{q,gen} - R_s i_{q,gen} - \omega_r(L_d i_{d,gen} + \psi_m) $$

donde \(R_s\) es la resistencia de estátor, \(L_d\), \(L_q\) son las inductancias de eje directo y
en cuadratura, \(\psi_m\) es el flujo de los imanes y \(\omega_r = p\,\Omega_{mec}\) es la
velocidad eléctrica del rotor (\(p\) = pares de polos).

**De dónde salen estas ecuaciones.** Son las mismas ecuaciones de un circuito RL en marco giratorio de
§2.3, pero con dos diferencias: (1) el flujo concatenado incluye el de los imanes, \(\psi_d = L_d i_d + \psi_m\)
y \(\psi_q = L_q i_q\); (2) el término de rotación \(\omega_r\times\)flujo genera la **fuerza
contraelectromotriz** \(-\omega_r\psi_m\) en el eje q (el \(-\omega_r\psi_m\) del segundo renglón) además del
acoplamiento cruzado \(\pm\omega_r L_{q,d} i\). El signo de \(\omega_r\) es opuesto al del lado red porque
aquí la máquina **genera** (la fem impulsa la corriente).

**Par electromagnético.** El par es \(T_{em} = \tfrac{3}{2}p\,(\psi_d i_q - \psi_q i_d)\) (producto vectorial
flujo × corriente). Sustituyendo los enlaces de flujo \(\psi_d = L_d i_d + \psi_m\), \(\psi_q = L_q i_q\):

$$ T_{em} = \frac{3}{2}p\big[(L_d i_{d,gen} + \psi_m)i_{q,gen} - L_q i_{q,gen}\,i_{d,gen}\big]
   = \frac{3}{2}p\left[\psi_m i_{q,gen} + (L_d - L_q)i_{d,gen}i_{q,gen}\right] $$

Para máquinas no salientes (\(L_d = L_q\), típico de PMSG de imanes en superficie) el segundo término
(par de reluctancia) desaparece:

$$ T_{em} = \frac{3}{2}p\,\psi_m i_{q,gen} $$

El par es **proporcional a \(i_{q,gen}\)**: por eso el MSC controla el par actuando solo sobre \(i_q\).

**Control del MSC (lado máquina):**

La frecuencia del marco dq del MSC es la velocidad eléctrica del rotor \(\omega_r = p\Omega_{mec}\),
que varía con el viento. El MSC controla:

- **Eje q:** despejando \(i_{q,gen}\) de \(T_{em} = \tfrac{3}{2}p\,\psi_m i_{q,gen}\) se obtiene la
  referencia \(i_{q,gen}^* = T_{ref}/(1.5\,p\,\psi_m)\), donde \(T_{ref} = K_{opt}\Omega_r^2\) es la
  referencia de par MPPT ([[eolica-mppt]]). El control de par controla indirectamente la velocidad y
  el punto de máxima potencia.
- **Eje d:** \(i_{d,gen}^* = 0\) (máximo par por amperio, sin componente de flujo de armadura).

La potencia eléctrica generada es:
$$ P_{elec} = \frac{3}{2}(v_{d,gen}i_{d,gen} + v_{q,gen}i_{q,gen}) $$

Esta potencia fluye hacia el bus DC a través del MSC. El GSC la evacúa hacia la red manteniendo
\(V_{dc}\) constante.

### 4.2 — Potencia generada y transmitida al bus DC

La potencia mecánica en el rotor depende de la velocidad del viento \(v_w\) y el coeficiente de potencia
\(C_p(\lambda, \beta)\):

$$ P_{mec} = \frac{1}{2}\rho A C_p(\lambda,\beta)v_w^3 $$

donde \(\rho\) es la densidad del aire, \(A = \pi R^2\) el área barrida y \(\lambda = R\Omega_r/v_w\)
la velocidad específica. El MPPT opera en el punto \(\lambda_{opt}\) donde \(C_p\) es máximo.

La potencia eléctrica en el estátor del PMSG:

$$ P_{elec} = P_{mec} - P_{Cu,gen} - P_{Fe,gen} $$

donde \(P_{Cu,gen} = 3R_s I_{gen}^2\) son las pérdidas en el cobre del estátor y \(P_{Fe,gen}\) las
pérdidas en el hierro del núcleo magnético. Para un PMSG de gran potencia,
\(\eta_{gen} \approx 95\text{–}97\,\%\).

La potencia que llega al bus DC desde el MSC:

$$ P_{DC,in} = P_{elec} - P_{sw,MSC} - P_{cond,MSC} $$

donde \(P_{sw,MSC}\) y \(P_{cond,MSC}\) son las pérdidas de conmutación y conducción del propio MSC
(ver sección 4.3).

### 4.3 — Pérdidas totales y eficiencia: desarrollo completo

Las pérdidas en cada VSC se descomponen en cuatro componentes por semiconductor:

**Pérdidas de conducción del IGBT.** Se parte de la característica de salida del IGBT, que se aproxima por
una recta \(v_{ce}(i) = V_{ce0} + R_{ce}\,i\) (tensión umbral + resistencia). La potencia disipada
instantánea es \(v_{ce}\,i = V_{ce0}\,i + R_{ce}\,i^2\); promediando sobre el periodo fundamental:

$$ P_{cond,IGBT} = V_{ce0} \cdot \bar{I} + R_{ce} \cdot \overline{I^2} $$

donde \(V_{ce0}\) es la tensión umbral (~1 V para IGBT Si, ~0.5 V para SiC), \(R_{ce}\) la resistencia
de conducción y \(\bar{I}\), \(\overline{I^2}\) son la media y la media cuadrática de la corriente **que
realmente circula por el IGBT**. El IGBT no conduce todo el ciclo: solo cuando su duty (que depende del
índice de modulación \(m\)) lo activa. Al pesar la corriente sinusoidal \(\hat I\sin\theta\) por ese duty
salen los factores con \(m\):

$$ \bar{I} = \frac{\hat{I}}{\pi}\left(1+\frac{m}{4}\right)\ \Big[\tfrac{\hat I}{\pi}\text{: media de }|\text{sin}|\Big],
   \qquad \overline{I^2} = \frac{\hat{I}^2}{8}\left(1+\frac{2m}{3}\right)\ \Big[\tfrac{\hat I^2}{4}\text{ RMS}^2\!\cdot\!\tfrac12\Big] $$

**Pérdidas de conmutación del IGBT.** El datasheet da la energía por conmutación \((E_{on}+E_{off})\) medida
a \(V_{test}\), \(I_{test}\). Esa energía escala **linealmente** con la corriente conmutada y con la tensión
del bus, y se producen \(f_s\) conmutaciones por segundo; promediando la corriente sinusoidal sobre el
periodo (de ahí el \(1/\pi\), media de \(|\sin|\)):

$$ P_{sw,IGBT} = \frac{f_s}{\pi}(E_{on} + E_{off})\frac{\hat{I}}{I_{test}}\frac{V_{dc}}{V_{test}} $$

donde el factor \(\hat I/I_{test}\) reescala por corriente y \(V_{dc}/V_{test}\) por tensión. La energía de
recuperación inversa del diodo antiparalelo añade \(E_{rr}\):

$$ P_{sw,diodo} = \frac{f_s}{\pi} E_{rr} \frac{\hat{I}}{I_{test}}\frac{V_{dc}}{V_{test}} $$

**Pérdidas totales por VSC** (6 IGBTs + 6 diodos antiparalelos):

$$ P_{loss,VSC} = 6\left(P_{cond,IGBT} + P_{sw,IGBT} + P_{cond,diodo} + P_{sw,diodo}\right) $$

**Eficiencia del convertidor y del sistema completo:**

$$ \eta_{VSC} = 1 - \frac{P_{loss,VSC}}{P_{nominal}} $$

$$ \eta_{B2B} = \eta_{MSC} \cdot \eta_{GSC} = (1-\epsilon_{MSC})(1-\epsilon_{GSC}) $$

**Ejemplo numérico completo:**

Aerogenerador PMSG de 2 MW, \(V_{dc} = 1100\,\text{V}\), \(f_s = 3\,\text{kHz}\), IGBT con
\(V_{ce0}=1.0\,\text{V}\), \(R_{ce}=1\,\text{m}\Omega\), \(E_{on}+E_{off}=50\,\text{mJ}\) a
600 V / 1000 A. Tensión de red \(V_{ac} = 690\,\text{V}\) (tensión de fase pico
\(\hat{V}_{ac} = 690\sqrt{2}/\sqrt{3} = 563\,\text{V}\)).

Corriente nominal (pico por fase, con índice de modulación \(m=0.9\)):

$$ \hat{I} = \frac{2P_{nom}}{3\,\hat{V}_{ac}} = \frac{2\times2\times10^6}{3\times563} = 2366\,\text{A} $$

Con \(m=0.9\):

$$ \bar{I} = \frac{2366}{\pi}\left(1+\frac{0.9}{4}\right) = 753\times1.225 = 922\,\text{A} $$

$$ \overline{I^2} = \frac{2366^2}{8}\left(1+\frac{2\times0.9}{3}\right) = 699698\times1.6 = 1.12\times10^6\,\text{A}^2 $$

Pérdidas de conducción por IGBT:

$$ P_{cond} = 1.0\times922 + 0.001\times1.12\times10^6 = 922 + 1120 = 2042\,\text{W} $$

Pérdidas de conmutación por IGBT (escalar a \(V_{dc}=1100\,\text{V}\)):

$$ P_{sw} = \frac{3000}{\pi}\times0.05\times\frac{2366}{1000}\times\frac{1100}{600} = 955\times0.05\times2.366\times1.833 = 207\,\text{W} \cdot 4.34 = 4328\,\text{W} $$

Total por IGBT: \(\approx 6370\,\text{W}\). Asumiendo pérdidas del diodo \(\approx 40\,\%\) del IGBT:

$$ P_{loss,GSC} \approx 6\times6370\times1.4 \approx 53.5\,\text{kW} $$

Eficiencia del GSC a plena carga:
$$ \eta_{GSC} = 1 - \frac{53500}{2000000} = 97.3\,\% $$

El MSC opera a frecuencia de conmutación típicamente menor (para reducir pérdidas en el generador y
porque la frecuencia del generador es baja a velocidad parcial) → \(\eta_{MSC} \approx 98.0\,\%\):

$$ \eta_{B2B} = 0.973\times0.980 = 95.4\,\% $$

---

## 5 — Proceso de diseño completo: de los componentes al control

### 5.1 — Especificaciones de partida

Antes de diseñar nada, definir las especificaciones de sistema:

| Especificación | Símbolo | Comentario |
|---|---|---|
| Potencia nominal | \(P_{nom}\) | Define la corriente y los semiconductores |
| Tensión AC lado red | \(V_{ac}\) | Tensión de línea RMS |
| Tensión AC lado máquina | \(V_{gen}\) | Puede variar con la velocidad del rotor |
| Tensión bus DC | \(V_{dc}\) | Derivada de \(V_{ac}\) y \(m_{max}\) |
| Frecuencia de conmutación | \(f_s\) | Compromiso pérdidas ↔ calidad de onda |
| Caída admisible de \(V_{dc}\) | \(\Delta V_{dc,max}\) | Define \(C_{dc}\) |
| Ancho de banda lazo de corriente | \(\omega_{ci}\) | Define \(K_p\), \(T_i\) |
| Margen de fase mínimo | \(PM_{min}\) | Robustez, típ. 45° |

### 5.2 — Diseño del nivel eléctrico (componentes)

**Iteración 1 — Tensión del bus DC:**

La tensión del bus DC debe ser suficiente para **sintetizar** el pico de la tensión de red con margen de
saturación. En un VSC de dos niveles con SPWM, el pico de tensión de fase que puede generar es
\(\hat v_{fase} = m\,V_{dc}/2\), luego \(V_{dc} \ge 2\hat v_{fase}/m_{max}\). Como el pico de fase es
\(\hat v_{fase} = \sqrt{2}\,V_{ac,fase} = \sqrt{2}\,V_{ac}/\sqrt{3}\) (de línea a fase):

$$ V_{dc} \geq \frac{2\hat v_{fase}}{m_{max}} = \frac{2\sqrt{2}\,V_{ac,max}}{m_{max}\sqrt{3}}, \quad m_{max} \approx 0.9 $$

Por ejemplo: \(V_{ac} = 690\,\text{V}\) (línea) → \(V_{ac,fase,pico} = 690\sqrt{2}/\sqrt{3} = 563\,\text{V}\):
$$ V_{dc} \geq \frac{2\times563}{0.9} = 1251\,\text{V} $$

Elegir \(V_{dc} = 1150\,\text{V}\) (con \(m_{max}=0.98\) en casos de emergencia).

**Iteración 2 — Inductancia del filtro \(L\):**

Criterio de rizado de corriente \(\Delta i_L \leq 20\,\%\,\hat{I}_{nom}\) (rizado pico-pico en la
frecuencia de conmutación). De dónde sale: en una inductancia \(v_L = L\,di/dt\), así que el rizado durante
el tiempo que se aplica una tensión \(V_{dc}\) es \(\Delta i_L = V_{dc}\,\Delta t/L\). En SPWM de dos niveles
el peor caso ocurre a mitad de modulación, donde el intervalo efectivo es \(\Delta t = 1/(4 f_s)\) (de ahí
el **4**):

$$ \Delta i_L = \frac{V_{dc}}{4\,f_s\,L} \quad\Longrightarrow\quad L \geq \frac{V_{dc}}{4\,f_s\,\Delta i_{L,max}} $$

Con \(V_{dc}=1150\,\text{V}\), \(f_s=3000\,\text{Hz}\), \(\Delta i_{L,max} = 0.20\times2366 = 473\,\text{A}\):

$$ L \geq \frac{1150}{4\times3000\times473} = 0.203\,\text{mH} $$

Elegir \(L = 0.25\,\text{mH}\). Verificar caída de tensión en pu:
\(X_L = 2\pi\times50\times0.25\times10^{-3} = 0.079\,\Omega\);
\(Z_{base} = V_{ac,fase}^2/P_{nom} = 398^2/2\times10^6 = 0.079\,\Omega\) → \(x_L \approx 1\,\text{pu}\)
(demasiado alto; reducir \(f_s\) o aceptar filtro LCL, ver [[filtro-lcl]]).

**Iteración 3 — Condensador del bus DC:**

*Criterio energético* (transitorio más severo: escalón de \(P_{nom}\) en \(\Delta t \approx 1/\omega_{ci}\)).
De dónde sale: la energía \(P_{nom}\Delta t\) que el condensador debe aportar/absorber es la diferencia de
su energía almacenada entre \(V_{dc}\) y la tensión caída \(V_{dc}-\Delta V_{dc,max}\):

$$ P_{nom}\,\Delta t = \tfrac{1}{2}C_{dc}\big[V_{dc}^2 - (V_{dc}-\Delta V_{dc,max})^2\big]
   \quad\Longrightarrow\quad C_{dc} \geq \frac{2\,P_{nom}\,\Delta t}{V_{dc}^2 - (V_{dc}-\Delta V_{dc,max})^2} $$

Desarrollando el cuadrado \(V_{dc}^2-(V_{dc}-\Delta V)^2 = 2V_{dc}\Delta V - \Delta V^2 \approx 2V_{dc}\Delta V\)
(el \(\Delta V^2\) es despreciable frente a \(2V_{dc}\Delta V\) porque \(\Delta V \ll V_{dc}\)):

$$ C_{dc} \approx \frac{2\,P_{nom}\,\Delta t}{2\,V_{dc}\,\Delta V_{dc,max}} = \frac{P_{nom}\,\Delta t}{V_{dc}\,\Delta V_{dc,max}} $$

Con \(P_{nom}=2\,\text{MW}\), \(\Delta t = 1/1885 = 0.53\,\text{ms}\), \(V_{dc}=1150\,\text{V}\),
\(\Delta V_{dc,max} = 57.5\,\text{V}\) (5 %):

$$ C_{dc} \geq \frac{2\times2\times10^6\times0.53\times10^{-3}}{2\times1150\times57.5} = \frac{2120}{132250} = 16\,\text{mF} $$

*Criterio de rizado de conmutación* (mucho más pequeño, no domina):

$$ C_{dc,sw} \geq \frac{\Delta i_{L,max}}{8\,f_s\,\Delta V_{dc,sw}} = \frac{473}{8\times3000\times11.5} = 1.7\,\text{mF} $$

El criterio energético domina → elegir \(C_{dc} = 20\,\text{mF}\).

*Verificación térmica de los semiconductores:*

$$ T_j = T_{ambiente} + P_{loss}\times R_{th,j-c} + P_{loss}\times R_{th,c-h} $$

Si \(T_j > T_{j,max}\): reducir \(f_s\) o aumentar el disipador e iterar desde Iteración 1.

### 5.3 — Diseño del control (lazos)

**Paso 1 — Lazo de corriente (IMC):**

$$ \omega_{ci} = \frac{\omega_{sw}}{10} = \frac{2\pi\times3000}{10} = 1885\,\text{rad/s} $$

$$ K_p = \omega_{ci}L = 1885\times0.25\times10^{-3} = 0.471\,\text{V/A} $$

$$ T_i = L/R = 0.25\times10^{-3}/0.05 = 5\,\text{ms}, \qquad K_i = K_p/T_i = 94.2\,\text{V/(A\,s)} $$

Verificar: PM del lazo de corriente = 90° (integrador puro tras cancelación del polo) → OK.

**Paso 2 — Lazo de tensión DC:**

$$ \omega_{dc} = \omega_{ci}/10 = 188.5\,\text{rad/s} $$

$$ K_{p,dc} = \frac{C_{dc}\,\omega_{dc}}{2} = \frac{0.020\times188.5}{2} = 1.885\,\text{A/V}^2 $$

$$ T_{i,dc} = \frac{a}{\omega_{dc}} = \frac{10}{188.5} = 53.1\,\text{ms} \qquad (a=\omega_{ci}/\omega_{dc}=10) $$

Verificar margen de fase del lazo DC. La FdT de lazo abierto (con el polo del lazo de corriente):

$$ L_{dc}(s) = \frac{2K_{p,dc}}{C_{dc}T_{i,dc}} \cdot \frac{T_{i,dc}s+1}{s^2}\cdot\frac{\omega_{ci}}{s+\omega_{ci}} $$

En \(s = j\omega_{dc}\): el cero \(T_{i,dc}s+1\) aporta \(\arctan(\omega_{dc}T_{i,dc}) = \arctan(10) = 84.3°\)
de fase avanzante, y el polo del lazo de corriente resta \(\arctan(\omega_{dc}/\omega_{ci})=\arctan(0.1)=5.7°\):

$$ \angle L_{dc}(j\omega_{dc}) = -180° + 84.3° - 5.7° = -101.4° \quad \Rightarrow \quad PM_{dc} = 78.6° \approx 79° \checkmark $$

**Paso 3 — Verificación con CPL:**

La carga de potencia constante (MSC controlando potencia) añade una conductancia negativa equivalente
\(G_{CPL} = -P_{2,max}/V_{dc,0}^2\) que tiende a inestabilizar el bus DC. La condición de estabilidad
requiere que la ganancia proporcional del lazo DC supere a esta conductancia negativa:

$$ K_{p,dc} > \frac{P_{2,max}}{2V_{dc,0}^2} = \frac{2\times10^6}{2\times1150^2} = 0.756\,\text{A/V}^2 $$

Como \(K_{p,dc} = 1.885 > 0.756\) → **estable con CPL** \(\checkmark\)

**Paso 4 — Sintonía del feedforward:**

El feedforward de potencia \(i_{d,FF}^* = P_{MSC}/(1.5\,v_{d,g})\) mejora la respuesta transitoria.
\(P_{MSC}\) se estima a partir de las medidas del MSC (\(v_{q,gen}i_{q,gen}\)) filtrando el ruido
con un paso-bajo:

$$ F_{FF}(s) = \frac{1}{T_{FF}s+1}, \qquad T_{FF} = \frac{1}{\omega_{ci}} = 0.53\,\text{ms} $$

El filtro no ralentiza la acción del feedforward respecto al lazo de corriente (ambos tienen el mismo
ancho de banda), pero elimina el ruido de medida del MSC.

**Paso 5 — Verificación final (simulación):**

1. Simular escalón de \(P_{MSC}\) de 0 a \(P_{nom}\) en 100 ms.
2. Verificar \(\Delta V_{dc} \leq \Delta V_{dc,max}\) con y sin feedforward.
3. Simular hueco de tensión (LVRT) al 20 % durante 140 ms.
4. Verificar que el chopper de freno limita \(V_{dc} \leq 1.1\,V_{dc,0}\).
5. Si alguna verificación falla → ajustar \(C_{dc}\) o \(\omega_{dc}\) e iterar desde Paso 2.

### 5.4 — Tabla resumen del diseño

| Parámetro | Fórmula | Valor ejemplo |
|---|---|---|
| \(V_{dc}\) | \(\geq 2\hat{V}_{ac}/m_{max}\) | 1150 V |
| \(L_{filtro}\) | \(V_{dc}/(4f_s\Delta i_{L,max})\) | 0.25 mH |
| \(C_{dc}\) | \(P_{nom}\Delta t/(V_{dc}\Delta V_{dc,max})\) | 20 mF |
| \(\omega_{ci}\) | \(\omega_{sw}/10\) | 1885 rad/s |
| \(K_{p,i}\) | \(\omega_{ci}L\) | 0.471 V/A |
| \(T_{i,i}\) | \(L/R\) | 5 ms |
| \(\omega_{dc}\) | \(\omega_{ci}/10\) | 188.5 rad/s |
| \(K_{p,dc}\) | \(C_{dc}\omega_{dc}/2\) | 1.885 A/V² |
| \(T_{i,dc}\) | \(a/\omega_{dc}\), \(a=\omega_{ci}/\omega_{dc}=10\) | 53.1 ms |
| \(PM_{dc}\) | \(\arctan a-\arctan(1/a)\) | ~79° |
| \(\eta_{B2B}\) | \(\eta_{MSC}\times\eta_{GSC}\) | ~95.4% |

---

## 6 — Errores comunes y puntos clave

**Error 1 — Ambos convertidores intentan fijar \(V_{dc}\):** conflicto de control; solo uno regula
\(V_{dc}\). El otro controla potencia o par.

**Error 2 — Condensador subdimensionado:** sin feedforward de potencia hay que dimensionar \(C_{dc}\)
para absorber toda la energía transitoria, lo que puede llevar a valores de \(C_{dc} > 100\,\text{mF}\)
en aplicaciones de MW. Con feedforward, \(C_{dc}\) puede reducirse en un factor 5–10.

**Error 3 — Olvidar el desacoplo dq:** sin los términos feedforward \(\pm\omega_0 L i_{q,d}\), los lazos
d y q se perturban mutuamente. En red débil (alta impedancia) este acoplamiento puede desestabilizar el
control.

**Error 4 — Saturación del integrador sin anti-windup:** durante LVRT, \(i_d^*\) puede saturar durante
varios ciclos. Sin anti-windup, el integrador acumula un error enorme que genera sobretensión al
recuperar la red.

**Error 5 — Ausencia de chopper de freno:** ante hueco de red el GSC no puede evacuar potencia; sin
chopper, \(V_{dc}\) se dispara hasta el límite de los condensadores o hasta el disparo por
sobretensión.

**Error 6 — Ignorar la CPL del MSC:** el MSC controlando potencia constante actúa como CPL, con
conductancia negativa. Si \(K_{p,dc}\) es pequeño (lazo DC demasiado lento), la CPL puede inestabilizar
el bus DC.

---

<div class="cfig"><img src="figuras/convertidor-back-to-back-analisis.png" alt="Modelo y control del convertidor back-to-back"><div class="cap">Esquema de flujo de potencia del back-to-back, respuesta de Vdc ante escalón, curvas de eficiencia por convertidor y sistema completo, y comportamiento durante FRT.</div></div>

## Conceptos relacionados
- [[filtro-lcl]] · [[convertidor-vsc]] · [[dinamica-bus-dc]] · [[control-tension-bus-dc]]
- [[eolica-mppt]] · [[aerogenerador-pmsg-dfig]] · [[hvdc-vsc-topologia]]
- [[desacoplo-dq]] · [[marco-dq]] · [[control-feedforward]]

## Referencias
- Yazdani, Iravani, *Voltage-Sourced Converters in Power Systems*, Wiley 2010.
- Teodorescu, Liserre, Rodríguez, *Grid Converters for PV and Wind Power Systems*, Wiley 2011.
- Holmes, Lipo, *Pulse Width Modulation for Power Converters*, IEEE Press 2003.
