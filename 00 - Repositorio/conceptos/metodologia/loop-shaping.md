---
titulo: Loop-shaping (diseño en frecuencia)
slug: loop-shaping
categoria: metodologia
tipo: metodo
nivel: avanzado
proyectos: [01-GFM-Impedance]
objetivos: [disenar el controlador dando forma a la ganancia de lazo]
tags: [bode, ganancia-de-lazo, frecuencia, margen, diseno]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-30
relacionados: [metodos-sintesis-control, margenes-estabilidad, funciones-sensibilidad, sintonia-pi-pid]
referencias:
  - "Skogestad, Postlethwaite, Multivariable Feedback Control, Wiley 2005 (cap. 2-3)"
---

## Definición
Método de diseño que da forma a la **ganancia de lazo abierto** \( L(s)=C(s)G(s) \) en el dominio
de la frecuencia para cumplir las especificaciones, en vez de razonar sobre los polos cerrados.

## Fundamento teórico
Objetivos de forma de \( L(j\omega) \):
- **Baja frecuencia**: ganancia alta → buen seguimiento y rechazo (S pequeña).
- **Cruce \( \omega_c \)**: fija el ancho de banda; pendiente ≈ −20 dB/dec en el cruce para buen
  margen de fase.
- **Alta frecuencia**: ganancia baja → atenúa ruido y dinámica no modelada (T pequeña).
Compromiso fundamental (Bode): no se puede tener S y T pequeñas a la vez en la misma banda
(\( S+T=1 \)); ver [[funciones-sensibilidad]]. El margen de fase y \( M_s \) se leen directo de \( L \).

<div class="cfig"><img src="figuras/loop-shaping-ganancia.png" alt="forma deseada de la ganancia de lazo en frecuencia"><div class="cap">Forma objetivo de la ganancia de lazo $|L|$: alta a baja frecuencia (buen seguimiento y rechazo, $S$ pequeña), baja a alta frecuencia (atenúa ruido y dinámica no modelada, $T$ pequeña) y con pendiente $-20$ dB/dec en el cruce $f_c$ para un buen margen de fase. El diseño consiste en moldear esta curva con el controlador.</div></div>

## 1 — La forma deseada de \( L \) y de dónde sale la regla de la pendiente
**Paso 1 — qué pide cada banda.** El desempeño y la robustez se traducen en cotas sobre \( |L| \):
- **Baja frecuencia** (\( \omega\ll\omega_c \)): rechazo y seguimiento exigen \( |S|=\frac1{|1+L|}\le\varepsilon \), o sea \( |L|\ge 1/\varepsilon\gg1 \). Ganancia alta. Un integrador \( 1/s \) la hace \( \to\infty \) en DC (error de posición nulo).
- **Alta frecuencia** (\( \omega\gg\omega_c \)): atenuar ruido y dinámica no modelada exige \( |T|\approx|L|\le\delta\ll1 \). Ganancia baja, con caída rápida.
- **Cruce** \( \omega_c \): \( |L(j\omega_c)|=1 \); ahí se fija el ancho de banda.

**Paso 2 — por qué \( -20 \) dB/dec en el cruce.** Para un \( L \) de fase mínima, la fase está atada a la pendiente de la magnitud (relación de Bode magnitud-fase): una pendiente local de \( -n\cdot20 \) dB/dec corresponde aproximadamente a una fase de \( -n\cdot90^\circ \). En el cruce:
$$ \text{pendiente }-20\text{ dB/dec}\Rightarrow\angle L\approx-90^\circ\Rightarrow \mathrm{PM}\approx90^\circ $$
$$ \text{pendiente }-40\text{ dB/dec}\Rightarrow\angle L\approx-180^\circ\Rightarrow \mathrm{PM}\approx0^\circ\ (\text{al borde}) $$
Por eso se busca cruzar 0 dB con pendiente \( -20 \) dB/dec: es la única que garantiza margen de fase holgado. La forma ideal es entonces "\( \approx-20 \) dB/dec sostenida alrededor del cruce, cayendo más rápido lejos".

## 2 — Moldear \( L \) con un PI + adelanto: cálculo concreto
**Paso 1 — planta y objetivo.** Sea \( G(s)=\dfrac{k}{s+a} \) con \( k=10 \), \( a=2 \) (un primer orden, ganancia DC \( k/a=5 \)). Objetivo: cruce en \( \omega_c=20 \) rad/s con \( \mathrm{PM}=60^\circ \) y error de DC nulo.

**Paso 2 — añadir el integrador (PI).** Un PI \( C(s)=k_p\dfrac{s+z}{s} \) aporta el polo en el origen (error DC nulo) y un cero \( z \) que recupera fase. Pónganse el cero una década por debajo del cruce, \( z=\omega_c/10=2 \) (de paso cancela el polo de la planta en \( a=2 \)), dejando
$$ L(s)=C(s)G(s)=k_p\,\frac{s+2}{s}\cdot\frac{10}{s+2}=\frac{10\,k_p}{s} $$
un integrador puro: pendiente \( -20 \) dB/dec en todo el rango.

**Paso 3 — fijar la ganancia por el cruce.** \( |L(j\omega_c)|=\dfrac{10\,k_p}{\omega_c}=1 \) en \( \omega_c=20 \):
$$ k_p=\frac{\omega_c}{10}=\frac{20}{10}=2 $$

**Paso 4 — comprobar el margen de fase.** Con \( L=10k_p/s \), la fase es \( -90^\circ \) a toda frecuencia, luego
$$ \mathrm{PM}=180^\circ-90^\circ=90^\circ $$
Sale más margen del pedido (90° > 60°): el cruce a \( -20 \) dB/dec da PM máximo. Si se quisiera exactamente 60° y un cruce más alto sin tanto margen sobrante, se añadiría una red de adelanto \( \dfrac{1+s/\omega_z}{1+s/\omega_p} \) centrada en \( \omega_c \) para subir el cruce manteniendo \( -20 \) dB/dec; el adelanto aporta su pico de fase \( \phi_{max}=\arcsin\frac{\omega_p-\omega_z}{\omega_p+\omega_z} \) justo en el cruce. **Lectura:** moldear \( L \) es elegir dónde poner ceros y polos del controlador para mantener \( -20 \) dB/dec en el cruce con la ganancia que sitúa \( \omega_c \) donde se quiere.

## Cuándo y por qué se usa
Cuando se quiere control explícito del compromiso desempeño/robustez/ruido, o la planta tiene
resonancias/retardos que conviene modelar en frecuencia. Es el lenguaje natural del análisis de
impedancia.

## Procedimiento (genérico)
1. Traza \( G(j\omega) \) (Bode de la planta).
2. Diseña \( C(s) \) para situar el cruce en \( \omega_c \) con pendiente −20 dB/dec y margen de
   fase objetivo (añade ceros/polos, adelanto-retardo).
3. Comprueba S y T (sensibilidad/complementaria) y \( M_s \).
4. Itera hasta el compromiso deseado.

## Ejemplo de código
```python
import numpy as np
L = C(1j*w) * G(1j*w)                  # ganancia de lazo
wc = w[np.argmin(np.abs(np.abs(L)-1))] # cruce de ganancia
PM = 180 + np.degrees(np.angle(L[np.argmin(np.abs(np.abs(L)-1))]))  # margen de fase
```

## Parámetros y valores típicos
Margen de fase 45–60°, pendiente −20 dB/dec en el cruce, \( M_s<2 \).

## Errores comunes
- Cruce con pendiente −40 dB/dec → margen de fase pobre.
- Forzar S pequeña en banda donde T debe serlo (viola el compromiso de Bode).

## Uso en proyectos
- **01 (GFM)**: el diagnóstico del lazo de potencia se hizo en frecuencia (margen de fase −86°
  reveló la causa de la inestabilidad), lenguaje de loop-shaping.

## Conceptos relacionados
- [[metodos-sintesis-control]] · [[margenes-estabilidad]] · [[funciones-sensibilidad]]

## Referencias
- Skogestad, Postlethwaite, *Multivariable Feedback Control*, 2005.
