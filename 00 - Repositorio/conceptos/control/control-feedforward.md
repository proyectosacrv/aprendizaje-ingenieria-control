---
titulo: Control feedforward (prealimentación)
slug: control-feedforward
categoria: control
tipo: tecnica
nivel: intermedio
proyectos: []
objetivos: [cancelar perturbaciones medibles antes de que afecten la salida, acelerar el seguimiento]
tags: [feedforward, prealimentacion, perturbacion, desacoplo, 2dof, anticipativo, control]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-07-01
relacionados: [realimentacion, desacoplo-dq, control-cascada, controlador-pid, funciones-sensibilidad, control-tension-bus-dc]
referencias:
  - "Åström, Murray, Feedback Systems, Princeton 2008"
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
  - "Buso, Mattavelli, Digital Control in Power Electronics, Morgan & Claypool 2006"
---

## Definición
Acción de control calculada a partir de una señal **medida o conocida** (referencia o perturbación), que
se suma a la salida del controlador por **realimentación**. Actúa **anticipándose**: corrige antes de que
el error aparezca, en lugar de reaccionar a él.

## Fundamento teórico
La realimentación corrige *después* de ver el error; el feedforward corrige *antes*, pero depende de la
calidad del modelo. Se usa de dos formas:

- **Feedforward de perturbación.** Si la perturbación medible \( d \) afecta a la salida a través de
  \( G_d \) y la planta es \( G \), la cancelación ideal es \( u_{ff}=-G^{-1}G_d\,d \). En la práctica se
  usa una aproximación causal (a menudo una simple ganancia o adelanto).
- **Feedforward de referencia (2-DOF).** \( u_{ff}=G^{-1}r \) (o un modelo de referencia) para que la
  salida siga \( r \) sin esperar a que el feedback integre el error; separa **seguimiento** de **rechazo**.

La clave: el feedforward **no cambia la estabilidad** (es lazo abierto, no entra en la ecuación
característica \( 1+GC \)), solo mejora la respuesta. Todo error de modelo queda como residuo que limpia el
feedback. En convertidores los casos canónicos son:
$$ \underbrace{v_{conv}^\*=\,PI(i^\*-i)}_{\text{feedback}}+\underbrace{v_{red}}_{\text{ff de tensión de red}}\;\underbrace{\mp\,\omega L\,i}_{\text{ff de desacoplo dq}} $$
El **feedforward de tensión de red** evita que el hueco/transitorio de red sea una perturbación para el
lazo de corriente, y el **\( \pm\omega L\,i \)** es el [[desacoplo-dq|desacoplo dq]] (un feedforward del
acoplamiento cruzado).

<div class="cfig"><img src="figuras/control-feedforward-hueco.png" alt="desviacion de corriente ante un hueco de red con y sin feedforward"><div class="cap">Ante un hueco de red, el lazo con solo feedback deja un pico de error de corriente que el PI tarda en limpiar; con feedforward de la tensión de red medida, la perturbación se cancela casi por completo (solo queda el residuo de una muestra de retardo). La estabilidad del lazo es idéntica: el ff no entra en $1+GC$.</div></div>

## 1 — Por qué \( u_{ff}=-G^{-1}G_d\,d \) cancela la perturbación
**Paso 1 — escribir la salida.** La perturbación medible \( d \) llega a la salida por su camino \( G_d \); la acción de control \( u \) por la planta \( G \). Superponiendo ambos caminos:

$$ y = G\,u + G_d\,d $$

La acción total suma feedback y feedforward: \( u = C\,e + u_{ff} \), con \( e=r-y \) y \( u_{ff}=G_{ff}\,d \).

**Paso 2 — sustituir y agrupar.** Metiendo \( u \) en la salida y usando \( e=r-y \):

$$ y = G\big(C(r-y)+G_{ff}\,d\big)+G_d\,d = GC\,r - GC\,y + G\,G_{ff}\,d + G_d\,d $$

Pasando \( GC\,y \) al lado izquierdo, \( y+GC\,y=y(1+GC) \), y despejando:

$$ y = \frac{GC}{1+GC}\,r \;+\; \frac{G\,G_{ff}+G_d}{1+GC}\,d $$

**Paso 3 — anular el término de perturbación.** El efecto de \( d \) sobre \( y \) es el segundo sumando. Para cancelarlo basta hacer **cero su numerador**, sin tocar el denominador \( 1+GC \):

$$ G\,G_{ff}+G_d = 0 \;\Longrightarrow\; \boxed{\;G_{ff}=u_{ff}/d=-G^{-1}G_d\;} $$

**Paso 4 — dos conclusiones.** (a) El feedforward **inyecta por \( G \) justo lo contrario** de lo que la perturbación mete por \( G_d \): \( G\,G_{ff}=-G_d \), así que en la salida los dos caminos se restan y \( d \) desaparece. (b) El denominador \( 1+GC \) (la ecuación característica) **no cambia**: el feedforward es lazo abierto, no afecta a la estabilidad ni a los polos, solo al término de \( d \). Por eso el feedback sigue limpiando cualquier residuo por error de modelo en \( G_{ff} \).

## 2 — Feedforward vs retroalimentación: complementarios

Retroalimentación y feedforward son técnicas complementarias, no alternativas. Sus fortalezas son opuestas:

**Retroalimentación (feedback).**
- Reactiva: actúa una vez que el error \( e = r - y \) ya existe.
- Robusta a incertidumbre: no necesita modelo exacto de la planta ni de la perturbación.
- Limpia errores residuales de cualquier fuente (ruido, variación paramétrica, perturbaciones no medibles).
- El integrador garantiza error nulo en régimen permanente (para señales de tipo compatible).

**Feedforward.**
- Proactivo: actúa antes de que \( e \) aparezca, con la perturbación o referencia como señal de disparo.
- Requiere modelo exacto: si \( G^{-1}G_d \) está mal, el FF inyecta una señal errónea que el FB debe corregir.
- No cierra ningún lazo: no afecta a la estabilidad en absoluto.
- Velocidad de actuación limitada solo por el retardo de medida (una muestra \( T_s \)), no por la dinámica del lazo.

**Por qué el FF solo no es suficiente.** Sin FB, el error residual de modelo se acumula indefinidamente:

$$ y = G\,G_{ff}\,d + G_d\,d = (G\,G_{ff} + G_d)\,d $$

Si \( G_{ff} \neq -G^{-1}G_d \) (inevitablemente, porque el modelo nunca es exacto), el término residual \( (G\,G_{ff}+G_d)\,d \neq 0 \) produce un error permanente proporcional al error del modelo. El integrador del FB lo elimina.

**La combinación óptima.** FF cancela la perturbación conocida con rapidez (un ciclo de retardo); FB corrige el residuo con robustez. El diseño óptimo asigna a cada uno su rol:

$$ v_{conv} = \underbrace{PI(i_d^* - i_d)}_{\text{FB: robustez, residuo}} + \underbrace{e_d}_{\text{FF: rapidez, cancelación}} $$

## 3 — Condición de cancelación: derivación completa

**Planta y perturbación del lazo de corriente.** La planta es \( G_p(s) = 1/(Ls+R) \) (filtro inductivo). La tensión de red \( e_d \) entra restando a la tensión del convertidor \( v_{conv} \):

$$ (Ls+R)\,i_d = v_{conv} - e_d \quad\Longrightarrow\quad i_d = \frac{1}{Ls+R}\,v_{conv} - \frac{1}{Ls+R}\,e_d $$

Comparando con \( y = G\,u + G_d\,d \): \( G = 1/(Ls+R) \) y \( G_d = -1/(Ls+R) \).

**FF perfecto.** Aplicando la condición de cancelación:

$$ G_{ff} = -G^{-1}G_d = -(Ls+R)\cdot\frac{-1}{Ls+R} = 1 $$

$$ \boxed{u_{ff} = G_{ff}\cdot e_d = e_d} $$

El feedforward perfecto para el lazo de corriente es **añadir directamente la tensión de red** \( e_d \) a la salida del PI: no hay inversión de planta inestable, no hay derivadas, es una ganancia unitaria pura.

**Interpretación física.** La tensión de red \( e_d \) tira de la corriente en la misma dirección que \( -v_{conv} \). Al añadir \( e_d \) a \( v_{conv} \), el convertidor compensa exactamente la perturbación: la corriente "no se entera" del cambio de red.

**Si la inversión de \( G_p \) tiene ceros RHP o retardo.** En general, \( G_{ff} = -G^{-1}G_d \) puede ser inestable si \( G_p \) tiene ceros en el semiplano derecho o retardos en el numerador. En esos casos se aproxima \( G_{ff} \) con un filtro causal estable (p.ej., \( G_{ff} \approx -G_d/G_{dc} \) con \( G_{dc} \) la ganancia en DC de \( G_p \)). Para la planta RL esto no aplica: \( G_p^{-1} = Ls+R \) es estable (aunque contiene derivada, que se aproxima con un filtro paso-bajo).

## 4 — Feedforward de referencia: mejorar la respuesta al set-point

El feedforward de referencia (estructura **2-DOF**, dos grados de libertad) mejora el seguimiento sin alterar el rechazo de perturbaciones.

**Idea.** En un lazo con solo FB, cuando cambia \( i_d^* \), el PI tarda \( \sim 1/\alpha_c \) en hacer que \( i_d \) siga la nueva referencia. Si se añade:

$$ u_{ff,ref} = G_p^{-1}(s)\cdot i_d^* = (Ls+R)\cdot i_d^* $$

la corriente seguiría idealmente la referencia de forma inmediata. El problema es que \( G_p^{-1} \) contiene la derivada \( L\,\dot i_d^* \): para una referencia escalón, genera un impulso.

**Implementación práctica.** Se filtra con un polo a alta frecuencia:

$$ u_{ff,ref}(s) = \frac{Ls+R}{\varepsilon s+1}\cdot i_d^* $$

Con \( \varepsilon = T_s \) (un ciclo de muestreo), el filtro es prácticamente transparente en banda y evita el impulso. En tiempo discreto:

$$ u_{ff,ref}[k] = L\,\frac{i_d^*[k]-i_d^*[k-1]}{T_s} + R\,i_d^*[k] $$

**Para el lazo de tensión.** Cuando cambia \( V_{dc}^* \), el PI de tensión tardaría varios ciclos en generar la corriente extra necesaria. Con FF de referencia, el cambio de \( V_{dc}^* \) genera directamente un escalón en \( i_d^* \) proporcional a \( C_{dc}\,\dot V_{dc}^* \):

$$ i_{d,ff}^* = C_{dc}\,\frac{V_{dc}^*[k]-V_{dc}^*[k-1]}{T_s} $$

El PI de tensión solo tiene que corregir el residuo por error de modelo en \( C_{dc} \).

## 5 — FF en el droop GFM: el término EV/X

En un convertidor grid-forming con droop activo, la referencia de potencia activa \( P_{set} \) pasa por el filtro del droop antes de llegar al ángulo de referencia \( \theta_{ref} \):

$$ \dot\theta = \omega_0 + m_p\,(P_{set} - P_{elec}) $$

Con un filtro de paso bajo de frecuencia de corte \( \omega_f \) en la medida de potencia, el cambio de \( P_{set} \) tarda \( \tau_f = 1/\omega_f \) en propagarse al ángulo.

**FF de \( P_{set} \).** Añadir \( P_{set} \) directamente a la referencia de ángulo, sin pasar por el filtro:

$$ \dot\theta = \omega_0 + m_p\,P_{set}^{ff} + m_p\,(P_{set} - P_{elec})_{filtrado} $$

El cambio de \( P_{set} \) mueve \( \theta_{ref} \) de inmediato (un ciclo de retardo) en lugar de esperar \( \tau_f \). La potencia inyectada sigue siendo la misma, pero el transitorio de ángulo es más corto.

**Trade-off.** La respuesta al escalón de \( P_{set} \) es más rápida, pero si \( P_{set} \) tiene ruido de alta frecuencia (p.ej., comandos de despacho con cuantificación), ese ruido entra directamente en \( \theta_{ref} \) y puede producir oscilaciones en la tensión terminal. Se añade un filtro de paso bajo suave (\( \omega_{ff} \approx 2–5\,\omega_f \)) al término de FF para limitar el ruido sin perder la velocidad de respuesta.

## 6 — Diseño iterativo: lazo de corriente con FF de red

Parámetros: \( L=2\ \text{mH} \), \( R=50\ \text{m}\Omega \), \( \alpha_c=2\pi\cdot750\ \text{Hz} \), \( T_s=100\ \mu\text{s} \), escalón de perturbación \( \Delta e_d=100\ \text{V} \).

**Iteración 0 — solo PI (sin FF).**
El PI tiene \( K_p=\alpha_c L=9{,}42\ \text{V/A} \), \( K_i=\alpha_c R=0{,}236\ \text{V/(A·s)} \).
Ante el escalón de \( e_d \), el pico de error de corriente es:
\( \Delta i_{max} \approx \Delta e_d / (\alpha_c L) = 100 / 9{,}42 \approx 10{,}6\ \text{A} \).
Tiempo de rechazo aproximado: \( t_r \approx 1/\alpha_c = 0{,}21\ \text{ms} \).
Área del error: \( \int e\,dt \approx \Delta e_d/(alpha_c^2 L) \approx 1{,}4\ \text{mA·s} \).

**Iteración 1 — añadir FF de \( e_d \).**
Se mide \( v_C \approx e_d \) (tensión en el condensador del filtro, que en red fuerte ≈ tensión de red).
Se añade \( u_{ff} = v_C[k-1] \) (un ciclo de retardo por implementación).
El pico de corriente cae a \( \Delta i_{max} \approx \Delta e_d\,T_s/L = 100\times10^{-4}/2\times10^{-3} = 0{,}5\ \text{A} \): mejora de **20×**.
Tiempo de rechazo: \( T_s = 100\ \mu\text{s} \) (un ciclo) en lugar de 0.21 ms.

**Iteración 2 — verificar que el FF no introduce inestabilidad.**
El FF de \( e_d \) es una señal de lazo abierto: no entra en \( 1+GC \). La estabilidad del lazo depende solo del PI y la planta. Verificación: el polinomio característico del lazo con FF es idéntico al del lazo sin FF. ✓

**Iteración 3 — verificar efecto del ruido de \( v_C \).**
Si \( v_C \) tiene armónicos de red (50 Hz y sus múltiplos), estos entran directamente en la acción de control a través del FF. Para un armónico de 50 Hz con amplitud 5 V:
\( \Delta i_{armónico} \approx 5\ \text{V} / (\alpha_c L) = 5/9{,}42 \approx 0{,}53\ \text{A} \): tolerable (< 0.1% de la corriente nominal en un sistema de 1000 A).
Si el ruido es mayor (p.ej., armónico del quinto de 20 V a 250 Hz), se filtra el FF con un polo a \( 2\alpha_c \):
\( u_{ff,filt}(s) = \frac{2\alpha_c}{s+2\alpha_c}\cdot e_d \)
En digital: \( u_{ff}[k] = (1-a)\,e_d[k-1] + a\,u_{ff}[k-1] \) con \( a = e^{-2\alpha_c T_s} \approx 0.01 \) para \( \alpha_c = 2\pi\cdot750 \).

<div class="cfig"><img src="figuras/control-feedforward-analisis.png" alt="analisis feedforward lazo corriente"><div class="cap">(a) Ante escalón de $e_d$=100 V: solo FB (rojo) tarda ~0.2 ms en rechazar; FB+FF (azul) lo cancela en un ciclo. (b) Escalón de $i_d^*$=500 A: FF de referencia reduce el tiempo de subida y el sobreimpulso. (c) Sensibilidad al error en L: ±20% de error en L produce un residuo pequeño que el FB limpia. La zona verde indica que el FF es robusto dentro del rango de variación realista. (d) Diagrama de bloques completo: PI (FB), FF de perturbación ($e_d\approx v_C$), FF de referencia $(Ls+R)i_d^*$.</div></div>

| Iteración | Técnica | Pico \(\Delta i_d\) [A] | \(t_{rechazo}\) | Observación |
|---|---|---|---|---|
| 0 | Solo PI | ~10.6 | ~0.21 ms | Lento frente a transitorio rápido |
| 1 | PI + FF \(e_d\) | ~0.5 | ~0.1 ms (1 ciclo) | Mejora 20×, estabilidad idéntica |
| 2 | Verificar estabilidad | — | — | ✓ FF no modifica 1+GC |
| 3 | FF filtrado a 2αc | ~0.5 | ~0.1 ms | Robusto al ruido de armónicos |

## Cuándo y por qué se usa
Cuando la perturbación es **medible** y el feedback solo es demasiado lento para rechazarla a tiempo:
tensión de red en el lazo de corriente, acoplamiento \( \pm\omega L \) entre ejes dq, potencia del otro
lado en un [[convertidor-back-to-back|back-to-back]] (ff hacia el lazo de \( V_{dc} \)), par de carga en un
accionamiento. También en 2-DOF para seguimiento rápido sin sobrepaso.

## Procedimiento de diseño (genérico)
1. Identifica la perturbación/referencia **medible** y su camino \( G_d \) hasta la salida.
2. Calcula \( u_{ff}=-G^{-1}G_d\,d \); si \( G^{-1} \) no es causal, aproxima (ganancia, adelanto, filtro).
3. Filtra la señal de ff para no inyectar ruido de medida (paso-bajo a 2–5× el ancho de banda del lazo).
4. Súmalo a la acción del feedback; **mantén el integrador** del feedback para el residuo de modelo.
5. Verifica que ante error de modelo el sistema sigue estable (lo garantiza el feedback) y mide la mejora.

## Ejemplo de código
```python
def current_loop(i_ref, i_meas, v_grid, w, L, R, pi, Ts):
    """Lazo de corriente con FF de red y desacoplo dq."""
    # Feedback PI
    v_fb = pi.update(i_ref - i_meas)
    # FF de perturbacion: tensión de red medida (1 ciclo de retardo)
    v_ff_pert = v_grid    # v_grid es v_grid[k-1] (muestra anterior)
    # FF de referencia: modelo directo de la planta
    v_ff_ref = L*(i_ref - pi.i_ref_prev)/Ts + R*i_ref
    pi.i_ref_prev = i_ref
    return v_fb + v_ff_pert + v_ff_ref
```

## Parámetros y valores típicos
- Filtro del FF: polo a 2–5× \( \alpha_c \).
- Ganancia de FF de red: 1.0 (cancelación directa, unitaria).
- FF de referencia: \( (Ls+R) \) o versión filtrada con polo a \( 1/T_s \).
- Desacoplo dq \( \pm\omega L \): usa la \( L \) nominal; un 10–20 % de error es tolerable.

## Errores comunes
- Esperar que el FF **estabilice** un lazo mal sintonizado: no toca \( 1+GC \), solo el seguimiento/rechazo.
- Diferenciar señales ruidosas en el FF sin filtrar → inyecta ruido en la acción de control.
- Invertir una planta con ceros de fase no mínima (\( G^{-1} \) inestable): usar aproximación, no inversión exacta.
- Quitar el integrador del feedback "porque ya hay ff": el residuo de modelo deja error en régimen permanente.
- No retardar la señal de FF un ciclo (\( T_s \)): en implementación digital, la medida de \( e_d \) del ciclo actual no está disponible hasta el ciclo siguiente.

## Conceptos relacionados
- [[realimentacion]] · [[desacoplo-dq]] · [[control-cascada]] · [[controlador-pid]] · [[control-tension-bus-dc]]

## Referencias
- Åström, Murray, *Feedback Systems*, 2008.
- Yazdani, Iravani, *Voltage-Sourced Converters in Power Systems*, 2010.
- Buso, Mattavelli, *Digital Control in Power Electronics*, 2006.
