---
titulo: Filtro LCL
slug: filtro-lcl
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [atenuar armonicos de conmutacion, modelar la planta de potencia]
tags: [filtro, resonancia, rizado, dimensionado, convertidor, LCL, dq]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-10
relacionados: [resonancia-lcl, amortiguamiento-activo-lcl, modulacion-pwm, marco-dq, modelo-promediado]
referencias:
  - "Reznik et al., LCL Filter Design and Performance Analysis for Grid-Interconnected Systems, IEEE TIA 2014"
  - "Mohan, Undeland, Robbins, Power Electronics, Wiley 2003 (cap. rizado e inductancias)"
---

## Definición
Filtro de tercer orden \( L_1\!-\!C_f\!-\!L_2 \) intercalado entre el puente del inversor y la red.
Atenúa los armónicos de conmutación con **mejor relación tamaño/atenuación** que un filtro L simple:
por encima de su resonancia cae a **−60 dB/dec** (tres elementos reactivos) en lugar de −20 dB/dec.
El precio de ese orden tres es una **resonancia** poco amortiguada que hay que gestionar.

## Topología y diagrama
La rama serie \( L_1 \) (lado inversor) → nudo \( v_C \) → \( L_2 \) (lado red); el condensador
\( C_f \) cuelga del nudo a tierra (opcionalmente con \( R_d \) de amortiguamiento pasivo).

<div class="cfig"><img src="figuras/filtro-lcl-circuito.png" alt="Circuito del filtro LCL: VSC, L1-R1, nudo vC con Cf a tierra, L2-R2, red"><div class="cap">Topología LCL por fase: rama serie L₁–Cf–L₂ entre el puente y el PCC; Cf deriva el rizado de conmutación a tierra.</div></div>

## Ecuaciones de partida (de dónde se sale)
Aplicando **Kirchhoff** a las tres ramas del diagrama (tensiones en las bobinas, corriente en el
condensador), salen las tres ecuaciones de estado del filtro:

$$ L_1\frac{d i_1}{dt}=v_i-v_C-R_1 i_1 \qquad\text{(KVL rama }L_1\text{)} $$
$$ C_f\frac{d v_C}{dt}=i_1-i_2 \qquad\text{(KCL nudo }v_C\text{)} $$
$$ L_2\frac{d i_2}{dt}=v_C-v_{pcc}-R_2 i_2 \qquad\text{(KVL rama }L_2\text{)} $$

Estas tres ecuaciones (\( i_1,\,v_C,\,i_2 \) como estados) son **el modelo del LCL**. En el marco
\( dq \) (girando a \( \omega \)) cada derivada añade el acoplamiento cruzado \( \omega\mathbf{J} \)
(ver [[marco-dq]]), con \( \mathbf{J}=\left[\begin{smallmatrix}0&-1\\1&0\end{smallmatrix}\right] \):

$$ L_1\dot{\mathbf{i}}_1=\mathbf{v}_i-\mathbf{v}_C-R_1\mathbf{i}_1+\omega L_1\mathbf{J}\mathbf{i}_1,\quad
   C_f\dot{\mathbf{v}}_C=\mathbf{i}_1-\mathbf{i}_2+\omega C_f\mathbf{J}\mathbf{v}_C,\quad
   L_2\dot{\mathbf{i}}_2=\mathbf{v}_C-\mathbf{v}_{pcc}-R_2\mathbf{i}_2+\omega L_2\mathbf{J}\mathbf{i}_2 $$

## Desarrollo 1 — frecuencia de resonancia
Tomando Laplace de las ecuaciones (con \( R\approx0 \) y red rígida \( v_{pcc}=0 \)) y eliminando
\( v_C \) e \( i_2 \), se llega a la corriente de lado red:

$$ \frac{i_2(s)}{v_i(s)}=\frac{1}{s\,L_1 L_2 C_f\,(s^2+\omega_{res}^2)} $$

El denominador se anula en \( s=\pm j\omega_{res} \): hay un **par de polos sin parte real**
(\( \zeta\approx0 \)). De ahí la frecuencia de resonancia, que es \( L_1 \) y \( L_2 \) en paralelo
con \( C_f \):

$$ \boxed{\;f_{res}=\frac{1}{2\pi}\sqrt{\dfrac{L_1+L_2}{L_1 L_2 C_f}}\;} $$

<div class="cfig"><img src="figuras/filtro-lcl-bode.png" alt="Respuesta en frecuencia del LCL con y sin amortiguamiento"><div class="cap">Magnitud de i₂/vᵢ: el pico en la resonancia (rojo, ζ≈0) se acota al amortiguar (azul). Por debajo el filtro deja pasar la fundamental; por encima cae a −60 dB/dec.</div></div>

> **A resaltar:** sin amortiguar, cualquier lazo o impedancia de red que excite \( f_{res} \) provoca
> oscilación sostenida. Desarrollo completo del fenómeno (anti-resonancia, factor Q, red débil) en
> [[resonancia-lcl]]; mitigación en [[amortiguamiento-activo-lcl]].

## Desarrollo 2 — rizado de corriente y dimensionado de \( L_1 \)
La bobina del lado inversor se dimensiona por el **rizado de conmutación** que deja pasar. La base es
\( v_L=L\,di/dt \): mientras el puente aplica una tensión \( \pm V_{dc}/2 \) sobre \( L_1 \) durante una
fracción del periodo \( T_{sw}=1/f_{sw} \), la corriente sube/baja con pendiente \( v_L/L_1 \). El
rizado pico-pico crece con \( T_{sw} \) (menos conmutaciones) y baja con \( L_1 \). El caso peor con
PWM senoidal de dos niveles da la regla de diseño habitual:

$$ \Delta i_{1,pp}\approx\frac{V_{dc}}{8\,f_{sw}\,L_1}\;\;\Longrightarrow\;\;
   \boxed{\;L_1=\frac{V_{dc}}{8\,f_{sw}\,\Delta i_{1,pp}}\;} $$

con \( \Delta i_{1,pp} \) típico del **10–20 %** de la corriente nominal de pico \( I_n \). Más
inductancia = menos rizado pero más caída y volumen.

## Desarrollo 3 — dimensionado de \( C_f \) (reactiva)
El condensador absorbe reactiva a 50 Hz: corriente \( I_{C}=\omega_0 C_f V \), luego
\( Q_{C}=V\,I_{C}=\omega_0 C_f V^2 \). Se limita a un **≤5 %** de la potencia base para no cargar el
inversor con reactiva inútil:

$$ Q_C=\omega_0 C_f V^2\le 0.05\,S_n\;\;\Longrightarrow\;\;
   \boxed{\;C_f\le 0.05\,\frac{S_n}{\omega_0 V^2}\;} $$

## Desarrollo 4 — dimensionado de \( L_2 \) (atenuación a \( f_{sw} \))
Muy por encima de \( f_{res} \), la impedancia del condensador \( 1/(\omega C_f) \) es mucho menor que
\( \omega L_2 \), así que casi todo el rizado se deriva por \( C_f \). El divisor de corriente da la
atenuación de lado inversor a lado red:

$$ \left|\frac{i_2}{i_1}\right|(\omega_{sw})\approx
   \frac{1}{|1-\omega_{sw}^2 L_2 C_f|}\approx\frac{1}{\omega_{sw}^2 L_2 C_f} $$

Para una atenuación objetivo \( k=i_2/i_1 \) a \( f_{sw} \) se despeja:

$$ \boxed{\;L_2\approx\frac{1}{k\,C_f\,\omega_{sw}^2}\;} $$

Relación práctica \( L_2/L_1\in[0.2,\,1] \). Conviene definir \( r=L_2/L_1 \) y comprobar después que
\( f_{res} \) cae en banda.

## Cuándo y por qué se usa
Estándar en inversores conectados a red (PV, eólica, baterías) por la normativa de inyección de
armónicos. Se prefiere al filtro L cuando se busca menos inductancia total / menor caída para la misma
atenuación. **A resaltar:** la inductancia de red \( L_g \) se suma a \( L_2 \) y baja \( f_{res} \) →
en red débil hay que verificar el caso peor.

## Procedimiento de diseño (genérico)
1. **\( L_1 \)** por rizado: \( L_1=\dfrac{V_{dc}}{8 f_{sw}\,\Delta i_{1,pp}} \) (\( \Delta i \)=10–20 % \( I_n \)).
2. **\( C_f \)** por reactiva: \( C_f\le 0.05\,S_n/(\omega_0 V^2) \).
3. **\( L_2 \)** por atenuación a \( f_{sw} \): \( L_2\approx 1/(k\,C_f\,\omega_{sw}^2) \), con \( r=L_2/L_1\in[0.2,1] \).
4. **Coloca \( f_{res} \)** en banda: \( 10 f_0 < f_{res} < f_{sw}/2 \).
5. **Añade amortiguamiento**: pasivo \( R_d\approx 1/(3\omega_{res}C_f) \) en serie con \( C_f \), o
   **activo** por software → [[amortiguamiento-activo-lcl]].
6. **Verifica en red débil**: recalcula \( f_{res} \) con \( L_2+L_{g,\max} \) (mínimo SCR).

## Ejemplo de código
```python
import numpy as np

# Datos: 10 kVA, 400 V (Vll), 50 Hz, Vdc=700 V, fsw=10 kHz, rizado 15% de In
Sn, Vll, f0, Vdc, fsw, rip = 10e3, 400, 50, 700, 10e3, 0.15
w0, wsw = 2*np.pi*f0, 2*np.pi*fsw
V = Vll*np.sqrt(2/3)                 # pico de fase
In = (Sn/(np.sqrt(3)*Vll))*np.sqrt(2)  # pico de fase nominal

L1 = Vdc/(8*fsw*rip*In)              # por rizado
Cf = 0.05*Sn/(w0*V**2)               # por reactiva (<=5%)
L2 = 1/(0.10*Cf*wsw**2)              # atenuacion objetivo k=0.10 a fsw
f_res = 1/(2*np.pi)*np.sqrt((L1+L2)/(L1*L2*Cf))
Rd = 1/(3*(2*np.pi*f_res)*Cf)        # amortiguamiento pasivo
print(f"L1={L1*1e3:.2f} mH  Cf={Cf*1e6:.1f} uF  L2={L2*1e3:.2f} mH  f_res={f_res:.0f} Hz")
```

## Parámetros y valores típicos
- Banda de resonancia: \( 10 f_0 < f_{res} < f_{sw}/2 \).
- \( \Delta i_{1,pp} \): 10–20 % de \( I_n \). \( C_f \): ≤5 % de \( S_n \) en reactiva. \( r=L_2/L_1 \): 0.2–1.
- Proyecto (10 kVA / 400 V / 50 Hz, \( f_{sw}=10\,\text{kHz} \)): \( L_1=2\,\text{mH} \),
  \( C_f=20\,\mu\text{F} \), \( L_2=1\,\text{mH} \) → \( f_{res}\approx1.38\,\text{kHz} \) (LCL aislado).
  En el modelo \( dq \) completo, con la inductancia de red, el modo resonante baja a
  \( \approx1.1\,\text{kHz} \) (\( \zeta\approx0.13 \) ya amortiguado).

## Errores comunes
- Dejar \( f_{res} \) demasiado cerca del ancho de banda de control → resonancia excitada.
- Olvidar el amortiguamiento → polos resonantes con \( \zeta\approx0 \) (modo resonante \( dq \) del
  proyecto: ≈1.1 kHz, \( \zeta\approx0.13 \) ya amortiguado).
- Sobredimensionar \( C_f \) → demasiada reactiva absorbida; sobredimensionar \( L_2 \) → caída y coste.
- No revisar \( f_{res} \) con la inductancia de red en el caso débil.

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: modelar la planta): el LCL aporta 6 de los 15 estados del modelo.
  Su modo resonante (≈1.1 kHz en el modelo dq) obligó a añadir amortiguamiento activo para poder subir
  el lazo de tensión.

## Conceptos relacionados
- [[resonancia-lcl]] · [[amortiguamiento-activo-lcl]] · [[modulacion-pwm]] · [[marco-dq]] · [[modelo-promediado]]

## Referencias
- Reznik et al., *LCL Filter Design...*, IEEE TIA 2014.
- Mohan, Undeland, Robbins, *Power Electronics*, Wiley 2003.
