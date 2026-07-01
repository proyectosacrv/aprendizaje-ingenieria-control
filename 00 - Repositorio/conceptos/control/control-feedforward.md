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
fecha_actualizacion: 2026-06-30
relacionados: [realimentacion, desacoplo-dq, control-cascada, controlador-pid, funciones-sensibilidad, control-tension-bus-dc]
referencias:
  - "Åström, Murray, Feedback Systems, Princeton 2008"
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
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

**Paso 4 — dos conclusiones.** (a) El feedforward **inyecta por \( G \) justo lo contrario** de lo que la perturbación mete por \( G_d \): \( G\,G_{ff}=-G_d \), así que en la salida los dos caminos se restan y \( d \) desaparece. (b) El denominador \( 1+GC \) (la ecuación característica, ver [[realimentacion]]) **no cambia**: el feedforward es lazo abierto, no afecta a la estabilidad ni a los polos, solo al término de \( d \). Por eso el feedback sigue limpiando cualquier residuo por error de modelo en \( G_{ff} \).

## Cuándo y por qué se usa
Cuando la perturbación es **medible** y el feedback solo es demasiado lento para rechazarla a tiempo:
tensión de red en el lazo de corriente, acoplamiento \( \pm\omega L \) entre ejes dq, potencia del otro
lado en un [[convertidor-back-to-back|back-to-back]] (ff hacia el lazo de \( V_{dc} \)), par de carga en un
accionamiento. También en 2-DOF para seguimiento rápido sin sobrepaso.

## Procedimiento de diseño (genérico)
1. Identifica la perturbación/referencia **medible** y su camino \( G_d \) hasta la salida.
2. Calcula \( u_{ff}=-G^{-1}G_d\,d \); si \( G^{-1} \) no es causal, aproxima (ganancia, adelanto, filtro).
3. Filtra la señal de ff para no inyectar ruido de medida (paso-bajo suave).
4. Súmalo a la acción del feedback; **mantén el integrador** del feedback para el residuo de modelo.
5. Verifica que ante error de modelo el sistema sigue estable (lo garantiza el feedback) y mide la mejora.

## Ejemplo de aplicación real
**Problema:** lazo de corriente de un VSC con \( L=2\,\text{mH} \) sufre un hueco de red de 0.3 pu en 1 ms.
El PI tiene ancho de banda 500 Hz. ¿Cuánto ayuda el feedforward de tensión de red?

Sin ff, el escalón de \( v_{red} \) es una perturbación que el PI corrige con su constante de tiempo
\( \tau\approx1/(2\pi\,500)\approx0.32\,\text{ms} \): durante \( \sim\!1\,\text{ms} \) la corriente se desvía
porque \( v_{red} \) cambia más rápido de lo que el integrador compensa, con pico de error
\( \Delta i\approx\Delta v\,\Delta t/L=(0.3\times325)\times10^{-3}/2\times10^{-3}\approx49\,\text{A} \).
Con ff, \( v_{red} \) medida entra directa en \( v_{conv}^\* \): el PI solo ve el **residuo** del retardo de
medida (un ciclo de muestreo, ~decenas de µs), y el pico de corriente cae más de un orden de magnitud. La
estabilidad del lazo es idéntica en ambos casos.

## Ejemplo de código
```python
def current_loop(i_ref, i_meas, v_grid, w, L, pi):
    # feedback PI + feedforward de red + desacoplo dq (+-wL)
    v_fb = pi.update(i_ref - i_meas)         # realimentacion
    v_ff = v_grid + w*L*cross(i_meas)        # ff red + acoplamiento cruzado
    return v_fb + v_ff
```

## Parámetros y valores típicos
Filtro de la señal de ff: 1–5× el ancho de banda del lazo. Ganancia de ff de red: 1.0 (cancelación
directa). El desacoplo \( \pm\omega L \) usa la \( L \) nominal; un 10–20 % de error es tolerable (lo limpia
el feedback).

## Errores comunes
- Esperar que el ff **estabilice** un lazo mal sintonizado: no toca \( 1+GC \), solo el seguimiento/rechazo.
- Diferenciar señales ruidosas en el ff sin filtrar → inyecta ruido en la acción de control.
- Invertir una planta con ceros de fase no mínima (\( G^{-1} \) inestable): usar aproximación, no inversión exacta.
- Quitar el integrador del feedback "porque ya hay ff": el residuo de modelo deja error en permanente.

## Conceptos relacionados
- [[realimentacion]] · [[desacoplo-dq]] · [[control-cascada]] · [[controlador-pid]] · [[control-tension-bus-dc]]

## Referencias
- Åström, Murray, *Feedback Systems*, 2008.
- Yazdani, Iravani, 2010.
