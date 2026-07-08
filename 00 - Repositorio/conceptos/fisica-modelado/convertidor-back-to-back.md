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
fecha_actualizacion: 2026-06-30
relacionados: [convertidor-vsc, dinamica-bus-dc, control-tension-bus-dc, eolica-mppt, modelo-bateria-bess]
referencias:
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
  - "Teodorescu, Liserre, Rodríguez, Grid Converters for PV and Wind Power Systems, Wiley 2011"
---

## 1 — Definición y topología

Dos [[convertidor-vsc|VSC]] conectados por un **bus DC común** (condensador compartido). Cada convertidor
mira a un sistema AC distinto; el bus DC los **desacopla** y permite flujo de potencia **bidireccional**
entre ambos lados. Es la topología base del aerogenerador full-converter (Tipo 4), el convertidor de
rotor del DFIG (Tipo 3), los accionamientos regenerativos y el HVDC-VSC.

```
   Red AC 1              Filtro L1         Bus DC          Filtro L2              Red AC 2
   (vg1, ω1)  ─────── R1+jX1 ──── ┌────────────────┐ ──── R2+jX2 ──────── (vg2, ω2)
                                    │                │
                               VSC1 │      C_dc      │ VSC2
                          (MSC/GSC) │  ─── V_dc ─── │ (GSC/LSC)
                                    │    +   -       │
                                    └────────────────┘
                                         ▲
                                    Condensador de bus
                                    E = ½ C V²_dc
```

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

**Balance de potencia del bus:**

$$ C_{dc}\,V_{dc}\,\frac{dV_{dc}}{dt} = P_{MSC} - P_{GSC} - P_{losses} $$

En equilibrio \( P_{MSC} \approx P_{GSC} \) y \( V_{dc} \) es constante. La **energía almacenada** en el
condensador \( E = \tfrac{1}{2}C_{dc}V_{dc}^2 \) actúa de pulmón: dimensionarla correctamente fija cuánto
cae \(V_{dc}\) ante un transitorio de potencia. Ver [[dinamica-bus-dc]] para el análisis de estabilidad
del bus con CPL.

**Aplicaciones principales:**
- Aerogenerador full-converter PMSG (Tipo 4): todo el flujo de potencia pasa por el back-to-back.
- DFIG (Tipo 3): solo la potencia de deslizamiento (\(\approx 30\,\%\) de \(P_{nom}\)) pasa por el convertidor.
- HVDC-VSC: interconexión asíncrona de dos redes AC a distintas frecuencias o fases.
- BESS ([[modelo-bateria-bess]]): batería + convertidor DC-DC + GSC.
- Accionamientos regenerativos: motor + convertidor de motor + convertidor de red.

---

## 2 — Modelo en dq: derivación paso a paso

Esta sección desarrolla el modelo matemático completo del GSC desde las ecuaciones de Kirchhoff en
coordenadas de fase (abc) hasta el modelo en dq listo para diseñar los lazos de control.

### Paso 1 — Circuito en abc

Para el GSC, el circuito equivalente en cada fase es una inductancia \(L\) con resistencia de pérdidas
\(R\) entre la tensión de salida del VSC \(v_{conv}\) y la tensión de red \(v_g\):

$$ v_{conv,a} = L\frac{di_a}{dt} + Ri_a + v_{g,a} $$

En forma matricial para las tres fases:

$$ L\frac{d}{dt}\begin{pmatrix}i_a\\i_b\\i_c\end{pmatrix} = \begin{pmatrix}v_{conv,a}\\v_{conv,b}\\v_{conv,c}\end{pmatrix} - \begin{pmatrix}v_{g,a}\\v_{g,b}\\v_{g,c}\end{pmatrix} - R\begin{pmatrix}i_a\\i_b\\i_c\end{pmatrix} $$

Esta ecuación es en frecuencia de red (50 Hz): las variables son sinusoidales en estado estacionario,
lo que hace difícil diseñar un controlador con error nulo usando un PI ordinario.

### Paso 2 — Transformación de Clarke (abc → αβ)

La transformada de Clarke proyecta las tres fases sobre dos ejes ortogonales fijos en el espacio
(marco αβ estacionario). Para sistema equilibrado (sin componente de secuencia cero):

$$ \begin{pmatrix}i_\alpha\\i_\beta\end{pmatrix} = \frac{2}{3}\begin{pmatrix}1 & -\frac{1}{2} & -\frac{1}{2}\\ 0 & \frac{\sqrt{3}}{2} & -\frac{\sqrt{3}}{2}\end{pmatrix}\begin{pmatrix}i_a\\i_b\\i_c\end{pmatrix} $$

Las ecuaciones en αβ conservan la misma estructura que en abc:

$$ L\frac{d}{dt}\begin{pmatrix}i_\alpha\\i_\beta\end{pmatrix} = \begin{pmatrix}v_{conv,\alpha}\\v_{conv,\beta}\end{pmatrix} - \begin{pmatrix}v_{g,\alpha}\\v_{g,\beta}\end{pmatrix} - R\begin{pmatrix}i_\alpha\\i_\beta\end{pmatrix} $$

Las variables en αβ siguen siendo sinusoidales (rotan a \(\omega_0\) en el plano αβ), así que el PI
todavía tendría error en estado estacionario. Se necesita el siguiente paso.

### Paso 3 — Transformación de Park (αβ → dq)

El marco dq gira solidario con el vector de tensión de red a velocidad \(\omega_0 = 2\pi f_0\). La
transformación de Park es una rotación de ángulo \(\theta = \omega_0 t\):

$$ \begin{pmatrix}i_d\\i_q\end{pmatrix} = \begin{pmatrix}\cos\theta & \sin\theta\\ -\sin\theta & \cos\theta\end{pmatrix}\begin{pmatrix}i_\alpha\\i_\beta\end{pmatrix} $$

Al derivar la corriente en dq aparece un término adicional por la rotación del marco de referencia
(regla de la cadena sobre la transformación dependiente del tiempo). Ese término produce el **acoplamiento
cruzado** entre los ejes d y q:

$$ L\dot{i}_d = v_{d,conv} - v_{d,g} - Ri_d + \omega_0 L i_q $$

$$ L\dot{i}_q = v_{q,conv} - v_{q,g} - Ri_q - \omega_0 L i_d $$

En forma matricial compacta:

$$ L\frac{d}{dt}\begin{pmatrix}i_d\\i_q\end{pmatrix} = \begin{pmatrix}v_{d,conv}\\v_{q,conv}\end{pmatrix} - \begin{pmatrix}v_{d,g}\\v_{q,g}\end{pmatrix} - \begin{pmatrix}R & -\omega_0 L\\ \omega_0 L & R\end{pmatrix}\begin{pmatrix}i_d\\i_q\end{pmatrix} $$

**Resultado clave:** en el marco dq, las variables son **continuas** en estado estacionario. Un PI
ordinario puede regular \(i_d\) e \(i_q\) con error nulo, siempre que se elimine el acoplamiento cruzado.

### Paso 4 — Orientación del marco dq

Se orienta el eje d alineado con el vector de tensión de red \(\vec{v}_g\). Con esta elección:

- \(v_{d,g} = |\vec{v}_g|\) (módulo de la tensión de red)
- \(v_{q,g} = 0\) (por definición de la orientación)

Las potencias activa y reactiva en dq se simplifican:

$$ P = \frac{3}{2}(v_{d,g}i_d + v_{q,g}i_q) = \frac{3}{2}v_{d,g}i_d $$

$$ Q = \frac{3}{2}(v_{q,g}i_d - v_{d,g}i_q) = -\frac{3}{2}v_{d,g}i_q $$

**Conclusión fundamental:** \(i_d\) controla \(P\) (y por tanto \(V_{dc}\)) e \(i_q\) controla \(Q\).
Las dos potencias quedan **desacopladas naturalmente** por la orientación del marco dq. Esta es la razón
por la que el control orientado por tensión de red (VOC, *Voltage Oriented Control*) es el estándar en
convertidores de red.

### Paso 5 — Desacoplamiento feedforward: derivación completa

Las ecuaciones dq del paso 3 contienen los términos de acoplamiento cruzado \(+\omega_0 L i_q\) (en el eje d) y \(-\omega_0 L i_d\) (en el eje q). Estos términos hacen que el sistema sea **MIMO acoplado**: si \(i_d\) varía, perturba inmediatamente \(i_q\), y viceversa.

**Objetivo:** diseñar la tensión de salida del convertidor \(v_{d,conv}^*\) y \(v_{q,conv}^*\) de modo que, vista desde el PI, la planta sea dos sistemas SISO independientes.

**Paso 5a — Elección de la ley de control:**

Se define la tensión de salida del convertidor como:

$$ v_{d,conv}^* = \underbrace{v_{d,PI}}_{\text{salida del PI}} + \underbrace{v_{d,g}}_{\text{FF tensión red}} + \underbrace{\omega_0 L\, i_q}_{\text{FF desacoplo}} $$

$$ v_{q,conv}^* = \underbrace{v_{q,PI}}_{\text{salida del PI}} + \underbrace{v_{q,g}}_{\text{FF tensión red}} - \underbrace{\omega_0 L\, i_d}_{\text{FF desacoplo}} $$

Nótese que el desacoplo **añade** \(+\omega_0 L i_q\) en el eje d (para cancelar el \(-\omega_0 L i_q\) que aparece en la ecuación) y **resta** \(\omega_0 L i_d\) en el eje q (para cancelar el \(+\omega_0 L i_d\)).

**Paso 5b — Sustitución en las ecuaciones dq:**

Sustituyendo \(v_{d,conv}^*\) en la ecuación del eje d:

$$ L\dot{i}_d = \underbrace{(v_{d,PI} + v_{d,g} + \omega_0 L i_q)}_{v_{d,conv}^*} - v_{d,g} - Ri_d + \omega_0 L i_q $$

Los términos \(v_{d,g}\) se cancelan entre sí, y los términos \(\omega_0 L i_q\) también:

$$ L\dot{i}_d = v_{d,PI} - Ri_d \implies \frac{I_d(s)}{V_{d,PI}(s)} = \frac{1}{Ls+R} $$

Ídem para el eje q:

$$ L\dot{i}_q = \underbrace{(v_{q,PI} + v_{q,g} - \omega_0 L i_d)}_{v_{q,conv}^*} - v_{q,g} - Ri_q - \omega_0 L i_d $$

$$ L\dot{i}_q = v_{q,PI} - Ri_q \implies \frac{I_q(s)}{V_{q,PI}(s)} = \frac{1}{Ls+R} $$

**Resultado:** tras el desacoplo, ambos ejes se rigen por la misma planta de primer orden:

$$ \boxed{G_i(s) = \frac{1}{Ls + R}} $$

El sistema MIMO acoplado se reduce a **dos lazos SISO independientes e idénticos**. Cada PI solo ve su propio eje; el acoplamiento cruzado ha sido absorbido por el feedforward.

**Condición de validez:** el desacoplo es exacto si las corrientes \(i_d\) e \(i_q\) medidas son exactas (sin ruido ni retardo). En la práctica, el retardo de muestreo introduce un error pequeño en el desacoplo que se tolera si \(\omega_{ci} \ll \omega_s\) (ancho de banda del lazo de corriente mucho menor que la frecuencia de muestreo).

**Diagrama de bloques — lazo de corriente dq desacoplado y lazo DC:**

<div class="cfig"><img src="../figuras/btb-diagramas-bloques.png" alt="Diagramas de bloques del back-to-back: lazo de corriente dq con desacoplo feedforward y lazo de tensión DC con feedforward de potencia"><div class="cap">Izquierda: lazos de corriente d y q tras el desacoplo feedforward — cada eje ve la planta escalar \(1/(Ls+R)\) sin acoplamiento cruzado. Los términos naranja son el feedforward de desacoplo (\(\pm\omega_0 L i_{q,d}\)) y los verdes el feedforward de tensión de red (\(v_{d,g}\)). Derecha: lazo de tensión DC con el PI sobre \(V_{dc}^2\), feedforward de potencia \(P_{MSC}/V_{dc,0}\) y bloque anti-windup.</div></div>

---

## 3 — Función de transferencia del lazo de corriente y diseño del PI

### FdT de lazo abierto

Con el desacoplo aplicado, la planta es \(G_i(s) = 1/(Ls+R)\) en cada eje. El controlador PI es:

$$ C_{PI}(s) = K_p \frac{T_i s + 1}{T_i s} $$

La FdT de lazo abierto del lazo de corriente:

$$ L_i(s) = C_{PI}(s) \cdot G_i(s) = K_p\frac{T_i s + 1}{T_i s} \cdot \frac{1}{Ls+R} $$

### Cancelación del polo de la planta

Eligiendo \(T_i = L/R\), el cero del PI cancela exactamente el polo de la planta:

$$ L_i(s) = K_p \frac{T_i s + 1}{T_i s} \cdot \frac{1/R}{(L/R)s+1} = \frac{K_p}{T_i R} \cdot \frac{1}{s} = \frac{K_p}{L} \cdot \frac{1}{s} $$

La FdT de lazo cerrado resultante es de **primer orden**:

$$ T_i(s) = \frac{L_i}{1+L_i} = \frac{K_p/L}{s + K_p/L} = \frac{\omega_{ci}}{s + \omega_{ci}} $$

con frecuencia de cruce \(\omega_{ci} = K_p/L\).

### Sintonía por método IMC

El método de control interno por modelo (IMC) da directamente los parámetros del PI a partir de la
frecuencia de cruce deseada \(\omega_{ci}\):

$$ \boxed{K_p = \omega_{ci} L, \qquad T_i = \frac{L}{R}, \qquad K_i = \frac{K_p}{T_i} = \omega_{ci} R} $$

### Criterio de selección de \(\omega_{ci}\)

La frecuencia de cruce del lazo de corriente debe satisfacer dos restricciones:

**Restricción superior** — no excitar la frecuencia de conmutación ni el rizado de la portadora PWM:
$$ \omega_{ci} < \frac{\omega_{sw}}{10} $$

**Restricción inferior** — separación de escalas con el lazo DC (el lazo de corriente debe ser mucho
más rápido que el DC para que el lazo DC pueda asumir que la corriente sigue la referencia
instantáneamente):
$$ \omega_{ci} > 10 \cdot \omega_{dc} $$

**Ejemplo:** \(f_{sw} = 3\,\text{kHz}\), \(\omega_{sw} = 18850\,\text{rad/s}\) → \(\omega_{ci} < 1885\,\text{rad/s}\) → elegir
\(\omega_{ci} = 1885\,\text{rad/s}\) (300 Hz).

**Margen de fase del lazo de corriente:** con cancelación exacta del polo, la FdT de lazo abierto es
un integrador puro \(K/s\) → \(PM = 90°\). En la práctica, el retardo del modulador PWM y del muestreo
digital reducen el PM real; suele estar entre 60° y 75°.

---

## 4 — Control del bus DC: de la física a la FdT

### 4.1 — Modelo linealizado

La dinámica del bus DC en función de la tensión es no lineal:

$$ C_{dc} V_{dc} \dot{V}_{dc} = P_{in} - P_{out} $$

El cambio de variable \(w = V_{dc}^2\) lineariza la ecuación. Derivando:
\(\dot{w} = 2V_{dc}\dot{V}_{dc}\), y sustituyendo:

$$ \frac{1}{2}C_{dc}\dot{w} = P_{in} - P_{out} \quad \Rightarrow \quad \dot{w} = \frac{2}{C_{dc}}(P_{in} - P_{out}) $$

La planta del lazo de \(w = V_{dc}^2\) es un **integrador puro** respecto a la potencia:

$$ G_{dc}(s) = \frac{\tilde{w}(s)}{\tilde{P}_{in}(s)} = \frac{2}{C_{dc}\,s} $$

Esta linealización es exacta (no una aproximación): la no linealidad de \(V_{dc}^2\) se elimina
completamente con el cambio de variable. Por tanto el controlador PI diseñado sobre \(w\) es lineal
y sus márgenes de estabilidad son exactos.

### 4.2 — Lazo cerrado con PI

El controlador PI opera sobre el error de \(w = V_{dc}^2\):

$$ C_{dc}^{ctrl}(s) = K_{p,dc}\frac{T_{i,dc}s + 1}{T_{i,dc}s} $$

FdT de lazo abierto del lazo DC:

$$ L_{dc}(s) = K_{p,dc}\frac{T_{i,dc}s+1}{T_{i,dc}s} \cdot \frac{2}{C_{dc}s} = \frac{2K_{p,dc}}{C_{dc}T_{i,dc}} \cdot \frac{T_{i,dc}s+1}{s^2} $$

La planta es un integrador; el PI añade otro integrador → **doble integrador** en lazo abierto. El
cero del PI \(s = -1/T_{i,dc}\) es el único elemento estabilizante. El margen de fase depende de la
posición de ese cero relativo a la frecuencia de cruce \(\omega_{dc}\).

**Sintonía para \(\zeta = 0.707\) (criterio de módulo óptimo):**

$$ \boxed{K_{p,dc} = \frac{C_{dc}\,\omega_{dc}}{2}, \qquad T_{i,dc} = \frac{4}{\omega_{dc}}, \qquad \omega_{dc} = \frac{\omega_{ci}}{10}} $$

Con esta sintonía el PM del lazo DC es:

$$ PM_{dc} = \arctan(\omega_{dc} T_{i,dc}) = \arctan(4) \approx 76° $$

### 4.3 — Feedforward de potencia

Sin feedforward, cada cambio de potencia del MSC es una perturbación que el lazo DC debe rechazar.
Como el lazo DC es lento (\(\omega_{dc} \approx \omega_{ci}/10\)), el condensador absorbe el transitorio
durante un tiempo del orden de \(1/\omega_{dc}\) antes de que el GSC ajuste su corriente.

El feedforward añade directamente la potencia del lado máquina como referencia anticipada:

$$ i_{d,GSC}^* = \underbrace{C_{dc}^{ctrl}(e_w)}_{\text{PI}} + \underbrace{\frac{P_{MSC}}{1.5\,v_{d,g}}}_{\text{feedforward}} $$

Con feedforward, la corriente del GSC sube casi instantáneamente cuando sube la potencia del MSC. El
condensador solo absorbe el transitorio del retardo del lazo de corriente interno (\(\sim 1/\omega_{ci}\)),
que es mucho menor. El condensador puede dimensionarse 5–10 veces más pequeño.

### 4.4 — Diagrama de bloques del lazo DC completo

```
  V*²_dc  +  ┌────────┐  i*_d,dc   ┌──────────────┐  P_GSC   ┌─────────┐
─────────►──┤  PI_dc  ├────────────►│ Lazo corr.   ├──────────►│  2/C·s  ├──► w = V²_dc
         -  └────────┘             │  ≈ 1 (rápido) │          └─────────┘        │
         ▲                         └──────────────┘                               │
         └──────────────────────────────────────────────────────────────────────────┘

                        ▲
                   P_MSC/(1.5·v_d,g)  ←── feedforward (suma en i*_d,dc)
```

El bloque "Lazo corr. ≈ 1" es la aproximación de separación de escalas: a la frecuencia del lazo DC,
el lazo de corriente tiene una ganancia de 1 y retardo despreciable.

### 4.5 — Características que debe tener el lazo DC

- **Separación de escalas:** \(\omega_{dc} = \omega_{ci}/10\) para que el lazo de corriente sea
  "instantáneo" desde el punto de vista del DC.
- **Margen de fase:** \(PM_{dc} \geq 45°\) para robustez ante variación de \(C_{dc}\) y ante la CPL.
- **Feedforward de \(P_{MSC}\):** imprescindible para no sobredimensionar \(C_{dc}\) y para obtener
  una respuesta dinámica aceptable.
- **Anti-windup en el integrador:** cuando \(i_d^*\) satura (límite de corriente del GSC), el
  integrador del PI debe congelarse para evitar que acumule error y genere sobretensión al salir de
  la saturación.
- **Chopper de freno:** durante LVRT, el GSC no puede evacuar potencia; el chopper disipa el exceso
  en una resistencia conectada directamente al bus DC, manteniendo \(V_{dc} \leq 1.1\,V_{dc,0}\).

---

## 5 — Aplicación en eólica PMSG: desarrollo teórico completo

### 5.1 — El generador PMSG como fuente de potencia

El PMSG se modela en el marco dq del rotor (eje d alineado con el flujo del imán permanente). Las
ecuaciones del circuito equivalente en dq son:

$$ L_d\dot{i}_{d,gen} = v_{d,gen} - R_s i_{d,gen} + \omega_r L_q i_{q,gen} $$

$$ L_q\dot{i}_{q,gen} = v_{q,gen} - R_s i_{q,gen} - \omega_r(L_d i_{d,gen} + \psi_m) $$

donde \(R_s\) es la resistencia de estátor, \(L_d\), \(L_q\) son las inductancias de eje directo y
en cuadratura, \(\psi_m\) es el flujo de los imanes y \(\omega_r = p\,\Omega_{mec}\) es la
velocidad eléctrica del rotor (\(p\) = pares de polos).

El par electromagnético:

$$ T_{em} = \frac{3}{2}p\left[\psi_m i_{q,gen} + (L_d - L_q)i_{d,gen}i_{q,gen}\right] $$

Para máquinas no salientes (\(L_d = L_q\), típico de PMSG de imanes en superficie):

$$ T_{em} = \frac{3}{2}p\,\psi_m i_{q,gen} $$

**Control del MSC (lado máquina):**

La frecuencia del marco dq del MSC es la velocidad eléctrica del rotor \(\omega_r = p\Omega_{mec}\),
que varía con el viento. El MSC controla:

- **Eje q:** \(i_{q,gen}^* = T_{ref}/(1.5\,p\,\psi_m)\), donde \(T_{ref} = K_{opt}\Omega_r^2\) es la
  referencia de par MPPT ([[eolica-mppt]]). El control de par controla indirectamente la velocidad y
  el punto de máxima potencia.
- **Eje d:** \(i_{d,gen}^* = 0\) (máximo par por amperio, sin componente de flujo de armadura).

La potencia eléctrica generada es:
$$ P_{elec} = \frac{3}{2}(v_{d,gen}i_{d,gen} + v_{q,gen}i_{q,gen}) $$

Esta potencia fluye hacia el bus DC a través del MSC. El GSC la evacúa hacia la red manteniendo
\(V_{dc}\) constante.

### 5.2 — Potencia generada y transmitida al bus DC

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
(ver sección 5.3).

### 5.3 — Pérdidas totales y eficiencia: desarrollo completo

Las pérdidas en cada VSC se descomponen en cuatro componentes por semiconductor:

**Pérdidas de conducción del IGBT:**

$$ P_{cond,IGBT} = V_{ce0} \cdot \bar{I} + R_{ce} \cdot \overline{I^2} $$

donde \(V_{ce0}\) es la tensión umbral (~1 V para IGBT Si, ~0.5 V para SiC), \(R_{ce}\) la resistencia
de conducción y \(\bar{I}\), \(\overline{I^2}\) son la media y la media cuadrática de la corriente de
colector. Para corriente sinusoidal de amplitud \(\hat{I}\) con índice de modulación \(m\):

$$ \bar{I} = \frac{\hat{I}}{\pi}\left(1+\frac{m}{4}\right), \qquad \overline{I^2} = \frac{\hat{I}^2}{8}\left(1+\frac{2m}{3}\right) $$

**Pérdidas de conmutación del IGBT:**

$$ P_{sw,IGBT} = \frac{f_s}{\pi}(E_{on} + E_{off})\frac{\hat{I}}{I_{test}}\frac{V_{dc}}{V_{test}} $$

donde \(E_{on}\), \(E_{off}\) son las energías de conmutación del datasheet a tensión \(V_{test}\) y
corriente \(I_{test}\). La energía de recuperación inversa del diodo antiparalelo añade \(E_{rr}\):

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

## 6 — Proceso de diseño completo: de los componentes al control

### 6.1 — Especificaciones de partida

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

### 6.2 — Diseño del nivel eléctrico (componentes)

**Iteración 1 — Tensión del bus DC:**

La tensión del bus DC debe ser suficiente para modular la tensión de red con margen de saturación:

$$ V_{dc} \geq \frac{2\sqrt{2}\,V_{ac,max}}{m_{max}\sqrt{3}}, \quad m_{max} \approx 0.9 $$

Por ejemplo: \(V_{ac} = 690\,\text{V}\) (línea) → \(V_{ac,fase,pico} = 690\sqrt{2}/\sqrt{3} = 563\,\text{V}\):
$$ V_{dc} \geq \frac{2\times563}{0.9} = 1251\,\text{V} $$

Elegir \(V_{dc} = 1150\,\text{V}\) (con \(m_{max}=0.98\) en casos de emergencia).

**Iteración 2 — Inductancia del filtro \(L\):**

Criterio de rizado de corriente \(\Delta i_L \leq 20\,\%\,\hat{I}_{nom}\) (rizado pico-pico en la
frecuencia de conmutación):

$$ L \geq \frac{V_{dc}}{4\,f_s\,\Delta i_{L,max}} $$

Con \(V_{dc}=1150\,\text{V}\), \(f_s=3000\,\text{Hz}\), \(\Delta i_{L,max} = 0.20\times2366 = 473\,\text{A}\):

$$ L \geq \frac{1150}{4\times3000\times473} = 0.203\,\text{mH} $$

Elegir \(L = 0.25\,\text{mH}\). Verificar caída de tensión en pu:
\(X_L = 2\pi\times50\times0.25\times10^{-3} = 0.079\,\Omega\);
\(Z_{base} = V_{ac,fase}^2/P_{nom} = 398^2/2\times10^6 = 0.079\,\Omega\) → \(x_L \approx 1\,\text{pu}\)
(demasiado alto; reducir \(f_s\) o aceptar filtro LCL, ver [[filtro-lcl]]).

**Iteración 3 — Condensador del bus DC:**

*Criterio energético* (transitorio más severo: escalón de \(P_{nom}\) en \(\Delta t \approx 1/\omega_{ci}\)):

$$ C_{dc} \geq \frac{2\,P_{nom}\,\Delta t}{V_{dc}^2 - (V_{dc}-\Delta V_{dc,max})^2} \approx \frac{2\,P_{nom}\,\Delta t}{2\,V_{dc}\,\Delta V_{dc,max}} $$

Con \(P_{nom}=2\,\text{MW}\), \(\Delta t = 1/1885 = 0.53\,\text{ms}\), \(V_{dc}=1150\,\text{V}\),
\(\Delta V_{dc,max} = 57.5\,\text{V}\) (5 %):

$$ C_{dc} \geq \frac{2\times2\times10^6\times0.53\times10^{-3}}{2\times1150\times57.5} = \frac{2120}{132250} = 16\,\text{mF} $$

*Criterio de rizado de conmutación* (mucho más pequeño, no domina):

$$ C_{dc,sw} \geq \frac{\Delta i_{L,max}}{8\,f_s\,\Delta V_{dc,sw}} = \frac{473}{8\times3000\times11.5} = 1.7\,\text{mF} $$

El criterio energético domina → elegir \(C_{dc} = 20\,\text{mF}\).

*Verificación térmica de los semiconductores:*

$$ T_j = T_{ambiente} + P_{loss}\times R_{th,j-c} + P_{loss}\times R_{th,c-h} $$

Si \(T_j > T_{j,max}\): reducir \(f_s\) o aumentar el disipador e iterar desde Iteración 1.

### 6.3 — Diseño del control (lazos)

**Paso 1 — Lazo de corriente (IMC):**

$$ \omega_{ci} = \frac{\omega_{sw}}{10} = \frac{2\pi\times3000}{10} = 1885\,\text{rad/s} $$

$$ K_p = \omega_{ci}L = 1885\times0.25\times10^{-3} = 0.471\,\text{V/A} $$

$$ T_i = L/R = 0.25\times10^{-3}/0.05 = 5\,\text{ms}, \qquad K_i = K_p/T_i = 94.2\,\text{V/(A\,s)} $$

Verificar: PM del lazo de corriente = 90° (integrador puro tras cancelación del polo) → OK.

**Paso 2 — Lazo de tensión DC:**

$$ \omega_{dc} = \omega_{ci}/10 = 188.5\,\text{rad/s} $$

$$ K_{p,dc} = \frac{C_{dc}\,\omega_{dc}}{2} = \frac{0.020\times188.5}{2} = 1.885\,\text{A/V}^2 $$

$$ T_{i,dc} = \frac{4}{\omega_{dc}} = \frac{4}{188.5} = 21.2\,\text{ms} $$

Verificar margen de fase del lazo DC. La FdT de lazo abierto:

$$ L_{dc}(s) = \frac{2K_{p,dc}}{C_{dc}T_{i,dc}} \cdot \frac{T_{i,dc}s+1}{s^2} $$

En \(s = j\omega_{dc}\): el término \(T_{i,dc}s+1\) contribuye \(\arctan(\omega_{dc}T_{i,dc}) = \arctan(4) = 76°\)
de fase avanzante. La fase de lazo abierto en \(\omega_{dc}\):

$$ \angle L_{dc}(j\omega_{dc}) = -180° + 76° = -104° \quad \Rightarrow \quad PM_{dc} = 76° \checkmark $$

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

### 6.4 — Tabla resumen del diseño

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
| \(T_{i,dc}\) | \(4/\omega_{dc}\) | 21.2 ms |
| \(PM_{dc}\) | \(\arctan(\omega_{dc}T_{i,dc})\) | ~76° |
| \(\eta_{B2B}\) | \(\eta_{MSC}\times\eta_{GSC}\) | ~95.4% |

---

## 7 — Errores comunes y puntos clave

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

<div class="cfig"><img src="../figuras/convertidor-back-to-back-analisis.png" alt="Modelo y control del convertidor back-to-back"><div class="cap">Esquema de flujo de potencia del back-to-back, respuesta de Vdc ante escalón, curvas de eficiencia por convertidor y sistema completo, y comportamiento durante FRT.</div></div>

## Conceptos relacionados
- [[filtro-lcl]] · [[convertidor-vsc]] · [[dinamica-bus-dc]] · [[control-tension-bus-dc]]
- [[eolica-mppt]] · [[aerogenerador-pmsg-dfig]] · [[hvdc-vsc-topologia]]
- [[desacoplo-dq]] · [[marco-dq]] · [[control-feedforward]]

## Referencias
- Yazdani, Iravani, *Voltage-Sourced Converters in Power Systems*, Wiley 2010.
- Teodorescu, Liserre, Rodríguez, *Grid Converters for PV and Wind Power Systems*, Wiley 2011.
- Holmes, Lipo, *Pulse Width Modulation for Power Converters*, IEEE Press 2003.
