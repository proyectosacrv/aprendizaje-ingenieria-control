---
titulo: Amortiguamiento pasivo vs activo (por control software)
slug: amortiguamiento-pasivo-vs-activo
categoria: control
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [comparar el amortiguamiento físico (resistencias) con el amortiguamiento por control software y elegir cuál usar]
tags: [amortiguamiento, pasivo, activo, damping, resistencia-virtual, perdidas, lcl, bus-dc, intermedio]
fecha_creacion: 2026-06-17
fecha_actualizacion: 2026-06-30
relacionados: [filtro-lcl, resonancia-rlc, antiresonancia, dinamica-bus-dc, control-cascada, compensacion-retardo]
referencias:
  - "Dannehl et al., Investigation of Active Damping Approaches for LCL Filters, IEEE TIA 2010"
  - "Wang, Blaabjerg, Harmonic Stability in Power-Electronic-Based Power Systems, IEEE TPEL 2014"
---

## Definición
Amortiguar una resonancia es añadirle disipación (o emularla) para que su pico deje de ser peligroso. En sistemas eléctricos hay dos familias para hacerlo:
- **Amortiguamiento pasivo:** colocar componentes físicos disipativos (resistencias) que convierten en calor la energía que oscila en la resonancia.
- **Amortiguamiento activo (por control software):** medir una variable del sistema y realimentarla con una ganancia adecuada para que el convertidor **emule** una resistencia, amortiguando sin disipar energía real.

Las dos llevan el par de polos de resonancia desde el eje imaginario (\( \zeta\approx 0 \)) hacia la izquierda del plano \( s \) (\( \zeta \) útil); la diferencia está en el coste, las pérdidas y la flexibilidad.

## Dónde aparece (contexto genérico)
Cualquier sistema eléctrico con una resonancia LC poco amortiguada es candidato: el filtro \( LCL \) de un convertidor de red, el filtro \( LC \) de salida de un inversor en isla, el bus DC con su condensador y la inductancia de cable, o una línea con compensación serie. El criterio de elección es el mismo en todos: ¿compensa disipar (pasivo, simple) o emular sin pérdidas (activo, eficiente pero exige sensor y cómputo)?

## Amortiguamiento pasivo
Se intercala una resistencia en la rama reactiva. La variante más común en un \( LCL \) es una \( R_d \) en serie con el condensador \( C_f \). El amortiguamiento que aporta al par resonante es
$$ \zeta = \tfrac{1}{2}\,R_d\,\sqrt{\dfrac{C_f\,(L_1+L_2)}{L_1\,L_2}} $$
y la resistencia óptima (compromiso entre acotar el pico y no estropear la atenuación a \( f_{sw} \)) es
$$ R_d \approx \frac{1}{3\,\omega_{res}\,C_f} $$
El precio es la potencia disipada, que crece con el amortiguamiento buscado y con la corriente de rizado que atraviesa \( R_d \):
$$ P_{R_d} = R_d\,I_{C_f,\,rms}^2 $$
Variantes para reducir esas pérdidas: \( R_d \) en paralelo con \( L_2 \), o una rama \( R\!-\!C \) de amortiguamiento (split-capacitor) que solo disipa cerca de \( f_{res} \) y deja pasar la fundamental sin pérdidas.

## Amortiguamiento activo (por control software)
En vez de una resistencia física, se realimenta una variable medida con una ganancia que hace que el convertidor se comporte como si hubiera una resistencia. En el \( LCL \) lo habitual es realimentar la **corriente del condensador** \( i_{C_f}=i_1-i_2 \) a la tensión de referencia con ganancia \( K_{ad} \):
$$ v_i = v_{i,PI} - K_{ad}\,(i_1 - i_2) $$
Sustituyendo en la dinámica de \( i_1 \), el término \( -K_{ad}\,i_1 \) actúa como una resistencia en serie con \( L_1 \): emula una \( R_d \) **sin** caída óhmica real, por lo que no disipa potencia. La ganancia \( K_{ad} \) (en ohmios) se elige para el \( \zeta \) objetivo barriendo el lugar de polos (desarrollo completo en [[filtro-lcl]]). Su límite es el **retardo de cómputo + PWM** (\( \approx 1.5\,T_s \)): si la resonancia está cerca de \( f_s/2 \), el retardo desfasa la realimentación y el damping pierde eficacia o se vuelve negativo (ver [[compensacion-retardo]]).

## 1 — De dónde sale \( \zeta(R_d) \): la resistencia que mueve los polos resonantes
**Paso 1 — el par resonante sin amortiguar.** El lazo serie \( L_1\!-\!C_f\!-\!L_2 \) presenta una resonancia. Visto desde la corriente que oscila entre las dos ramas inductivas, la inductancia efectiva es el paralelo \( L_1\|L_2=L_1L_2/(L_1+L_2) \) resonando con \( C_f \). La pulsación natural es

$$ \omega_{res}=\frac{1}{\sqrt{(L_1\|L_2)\,C_f}}=\sqrt{\frac{L_1+L_2}{L_1\,L_2\,C_f}} $$

Sin disipación, el par de polos está sobre el eje imaginario en \( \pm j\omega_{res} \): \( \zeta\approx0 \), pico infinito.

**Paso 2 — insertar \( R_d \) en serie con \( C_f \).** La impedancia de la rama del condensador pasa de \( 1/(sC_f) \) a \( R_d+1/(sC_f) \). El polinomio característico del lazo resonante (la malla \( L_1\|L_2 \), \( C_f \), \( R_d \)) toma la forma canónica de segundo orden:

$$ s^2+\frac{R_d}{L_1\|L_2}\,s+\omega_{res}^2 = s^2+2\zeta\omega_{res}\,s+\omega_{res}^2 $$

donde el término en \( s \) lo aporta exclusivamente \( R_d \) (sin él, ese coeficiente es nulo y \( \zeta=0 \)).

**Paso 3 — identificar \( \zeta \).** Igualando el coeficiente del término lineal:

$$ 2\zeta\omega_{res}=\frac{R_d}{L_1\|L_2}=R_d\,\frac{L_1+L_2}{L_1L_2} \quad\Longrightarrow\quad \zeta=\frac{R_d}{2\omega_{res}}\cdot\frac{L_1+L_2}{L_1L_2} $$

**Paso 4 — sustituir \( \omega_{res} \) y cerrar.** Metiendo \( \omega_{res}=\sqrt{(L_1+L_2)/(L_1L_2C_f)} \):

$$ \zeta=\frac{R_d}{2}\cdot\frac{L_1+L_2}{L_1L_2}\cdot\sqrt{\frac{L_1L_2C_f}{L_1+L_2}}=\frac{R_d}{2}\sqrt{\frac{C_f(L_1+L_2)}{L_1L_2}} $$

$$ \boxed{\;\zeta=\tfrac12\,R_d\sqrt{\frac{C_f(L_1+L_2)}{L_1L_2}}=\tfrac12\,R_d\,C_f\,\omega_{res}\;} $$

El amortiguamiento es **lineal en \( R_d \)**: cada ohmio empuja los polos resonantes a la izquierda de \( \zeta\approx0 \) hacia \( \zeta \) útil. Con la regla óptima \( R_d=1/(3\omega_{res}C_f) \) se obtiene un valor concreto: \( \zeta=\tfrac12\cdot\tfrac{1}{3\omega_{res}C_f}\cdot C_f\omega_{res}=\tfrac{1}{6}\approx0.167 \), un compromiso entre acotar el pico y no añadir demasiada pérdida ni estropear la atenuación a \( f_{sw} \).

## 2 — Amortiguamiento activo: \( K_{ad} \) emula una \( R_d \) virtual
**Paso 1 — la ley de realimentación.** Se realimenta la corriente del condensador \( i_{C_f}=i_1-i_2 \) restándola de la tensión de referencia con ganancia \( K_{ad} \) (en ohmios):

$$ v_i=v_{i,PI}-K_{ad}\,(i_1-i_2) $$

**Paso 2 — la dinámica de la rama \( L_1 \).** La tensión aplicada al inductor del lado convertidor es \( v_i-v_{C_f} \), de modo que

$$ L_1\frac{di_1}{dt}=v_i-v_{C_f}=v_{i,PI}-K_{ad}(i_1-i_2)-v_{C_f} $$

**Paso 3 — el término \( -K_{ad}\,i_1 \) es una resistencia.** Reordenando y agrupando el término proporcional a \( i_1 \):

$$ L_1\frac{di_1}{dt}+K_{ad}\,i_1 = v_{i,PI}-v_{C_f}+K_{ad}\,i_2 $$

El lado izquierdo es idéntico al de un inductor \( L_1 \) **en serie con una resistencia \( K_{ad} \)**: la realimentación coloca una resistencia virtual \( R_{vir}=K_{ad} \) en la rama de \( L_1 \), exactamente donde haría falta una física para amortiguar. La diferencia: \( K_{ad} \) no produce caída óhmica real (\( i_1^2K_{ad} \) no se disipa en calor, es una manipulación de la referencia), por eso **no hay pérdidas**.

**Paso 4 — equivalencia de damping y su límite.** Sustituyendo \( R_{vir}=K_{ad} \) en el papel que jugaba \( R_d \), el par resonante adquiere un \( \zeta \) análogo al del caso pasivo; \( K_{ad} \) se barre en el lugar de polos para el \( \zeta \) objetivo (desarrollo en [[filtro-lcl]]). El límite es el **retardo de cómputo + PWM** \( \approx1.5\,T_s \): introduce un \( e^{-s\,1.5T_s} \) en la realimentación que, cerca de \( f_s/2 \), desfasa \( K_{ad} \) hasta convertir la resistencia virtual en negativa (anti-damping). Por eso el activo exige que \( f_{res} \) esté holgadamente por debajo de \( f_s/2 \) o un predictor que compense el retardo (ver [[compensacion-retardo]]).

## Comparativa
<div class="cfig"><img src="figuras/amortiguamiento-pasivo-vs-activo.png" alt="Izquierda: Bode de i2/vi sin amortiguar, con amortiguamiento pasivo y activo. Derecha: pérdidas frente al amortiguamiento objetivo"><div class="cap">Izquierda: ambos métodos doman el pico de resonancia de forma parecida, pero el pasivo (\(R_d\) serie \(C_f\)) pierde algo de atenuación a alta frecuencia. Derecha: las pérdidas del pasivo crecen con el amortiguamiento buscado (\(P=R_d I_{Cf}^2\)), mientras el activo no disipa (solo coste de cómputo).</div></div>

| Aspecto | Pasivo (resistencia física) | Activo (control software) |
|---|---|---|
| Pérdidas | Disipa \( R_d\,I_{C_f}^2 \) (calor) | Prácticamente nulas |
| Eficiencia / térmica | Baja la eficiencia; necesita disipar calor | No afecta a la eficiencia |
| Coste hardware | Resistencia + disipador | Ninguno extra (usa el control) |
| Sensores | No necesita medida extra | Necesita medir/estimar \( i_{C_f} \) (o \( v_C \)) |
| Complejidad | Muy simple, siempre estable | Requiere diseño y sintonía del lazo |
| Atenuación a \( f_{sw} \) | La degrada algo (la \( R_d \) añade un cero) | La conserva |
| Robustez | Muy robusto (no depende de modelo ni muestreo) | Sensible a retardo de cómputo y a errores de medida |
| Ajuste | Fijo (hay que cambiar el componente) | Reprogramable (cambiar \( K_{ad} \) por software) |

## Ventajas y desventajas
**Pasivo — ventajas:** simplicidad máxima, robustez incondicional, sin dependencia del muestreo ni del modelo, fácil de garantizar. **Desventajas:** pérdidas y calor, peor eficiencia, peor atenuación a \( f_{sw} \), valor fijo (no adaptable), volumen y coste del componente y su refrigeración.

**Activo — ventajas:** sin pérdidas, no afecta a la eficiencia, sin hardware extra, reprogramable y adaptable (incluso con gain scheduling según el punto de operación), conserva la atenuación del filtro. **Desventajas:** necesita sensor/estimador de la corriente del condensador, exige diseño cuidadoso, y su eficacia la limita el retardo digital (problema si \( f_{res} \) está cerca de \( f_s/2 \)); un fallo del control deja la resonancia sin amortiguar.

## Cuándo usar cada uno
- **Pasivo:** baja potencia, donde las pérdidas son asumibles y prima la simplicidad/robustez; o como red de seguridad mínima.
- **Activo:** potencia media-alta, donde las pérdidas del pasivo serían inaceptables y ya hay capacidad de cómputo y medida. Es el estándar en convertidores de red modernos.
- **Mixto:** a veces se combina un amortiguamiento pasivo ligero (garantiza estabilidad pase lo que pase) con amortiguamiento activo (hace el grueso sin pérdidas).

## Ejemplo de código
```python
import numpy as np
# pasivo: Rd optimo y perdidas
w_res = np.sqrt((L1+L2)/(L1*L2*Cf))
Rd = 1/(3*w_res*Cf)
P_Rd = Rd*Icf_rms**2                 # potencia disipada (W)
# activo: resistencia virtual por realimentacion de i_Cf
iC = iL1 - iL2
vi = vi_pi - Kad*iC                  # emula Rd sin perdidas (Kad en ohmios)
```

## Errores comunes
- Sobredimensionar \( R_d \) en el pasivo: amortigua mucho pero dispara las pérdidas y estropea la atenuación a \( f_{sw} \).
- Confiar el amortiguamiento activo a una medida con retardo de muestreo grande: pierde eficacia cerca de \( f_s/2 \).
- Suponer que las resistencias parásitas (sin \( R_d \) ni \( K_{ad} \)) ya amortiguan lo suficiente: su \( \zeta \) es demasiado bajo (ver [[filtro-lcl]]).

## Uso en proyectos
- **01 / 02 (filtro LCL):** se usó amortiguamiento **activo** (\( K_{ad}=6\,\Omega \) realimentando \( i_{C_f} \)) para evitar las pérdidas que tendría una \( R_d \) física a esa potencia; la resonancia de ≈1.1 kHz quedó con \( \zeta\approx0.13 \).

## Conceptos relacionados
- [[filtro-lcl]] · [[resonancia-rlc]] · [[antiresonancia]] · [[dinamica-bus-dc]] · [[control-cascada]] · [[compensacion-retardo]]

## Referencias
- Dannehl et al., *Investigation of Active Damping Approaches for LCL Filters*, IEEE TIA 2010.
- Wang, Blaabjerg, *Harmonic Stability in Power-Electronic-Based Power Systems*, IEEE TPEL 2014.
