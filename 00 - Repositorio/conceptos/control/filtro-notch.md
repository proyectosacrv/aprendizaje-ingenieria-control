---
titulo: Filtro notch (rechazo de banda) para resonancias
slug: filtro-notch
categoria: control
tipo: tecnica
nivel: intermedio
proyectos: []
objetivos: [atenuar una resonancia estrecha en el lazo sin perder ancho de banda]
tags: [notch, rechazo-banda, resonancia, lcl, filtro, intermedio, control]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-02
relacionados: [filtro-lcl, diagrama-bode, loop-shaping]
referencias:
  - "Yepes et al., Analysis and design of resonant current controllers, IEEE TIE 2011"
  - "Peña-Alzola et al., LCL-filter design for grid converters, IEEE TPEL 2014"
  - "Briz & Hinkkanen, Design of deadbeat controllers for grid-connected voltage-source converters, IEEE TPEL 2021"
---

## Definición
Filtro selectivo que **atenúa una banda estrecha** centrada en \( \omega_n \) dejando pasar el
resto del espectro casi intacto. En convertidores se usa para cancelar el pico de resonancia del
[[filtro-lcl]] dentro del lazo de control.

## Fundamento teórico
Forma general con cero y polo amortiguados:
$$ N(s)=\frac{s^2+2\zeta_z\,\omega_n s+\omega_n^2}{s^2+2\zeta_p\,\omega_n s+\omega_n^2},
   \qquad \zeta_z<\zeta_p $$
- La profundidad del *notch* la fija \( \zeta_z/\zeta_p \) (cuanto menor el cociente, más profundo).
- El ancho de la muesca lo fija \( \zeta_p \): estrecho (selectivo) → muy sensible a que \( \omega_n \)
  coincida con la resonancia real; ancho → más robusto pero introduce **más retardo de fase** en la
  banda de control.
- Penalización clave: el notch **resta fase** por debajo de \( \omega_n \), reduciendo el margen del
  lazo si \( \omega_n \) está cerca del cruce de ganancia.

Frente al **amortiguamiento activo** ([[filtro-lcl|amortiguamiento activo]]): el notch es más simple (no
necesita sensar la corriente del condensador) pero menos robusto a la deriva de \( \omega_{res} \)
(con \( L \), \( C \) variando con el punto de operación o tolerancias).

<div class="cfig"><img src="figuras/filtro-notch-respuesta.png" alt="respuesta en frecuencia de un filtro notch"><div class="cap">El notch atenúa profundamente una banda estrecha en fn (la resonancia LCL) dejando el resto casi intacto; el precio es algo de fase restada por debajo de fn.</div></div>

## 1 — Por qué el cero anula la frecuencia \( \omega_n \)
**Paso 1 — el notch ideal.** Tomamos el caso límite de máxima profundidad, \( \zeta_z=0 \), que deja el numerador como un par de ceros sobre el eje imaginario:

$$ N(s)=\frac{s^2+\omega_n^2}{s^2+2\zeta_p\,\omega_n s+\omega_n^2} $$

**Paso 2 — evaluar en \( s=j\omega \).** Con \( (j\omega)^2=-\omega^2 \), el numerador es \( -\omega^2+\omega_n^2=\omega_n^2-\omega^2 \). El denominador, separando real e imaginario:

$$ N(j\omega)=\frac{\omega_n^2-\omega^2}{(\omega_n^2-\omega^2)+2\zeta_p\,\omega_n\,(j\omega)} $$

**Paso 3 — el numerador se anula en \( \omega_n \).** Justo en \( \omega=\omega_n \), el numerador \( \omega_n^2-\omega^2=0 \), mientras el denominador conserva su parte imaginaria \( 2\zeta_p\,\omega_n\,j\omega_n\neq 0 \). Por tanto:

$$ \boxed{\;N(j\omega_n)=\frac{0}{2\zeta_p\,\omega_n\,j\omega_n}=0\;} $$

Atenuación **total** en \( \omega_n \): el filtro tiene ceros en \( s=\pm j\omega_n \) (raíces de \( s^2+\omega_n^2 \)) exactamente sobre la frecuencia que se quiere matar. Una senoide de \( \omega_n \) que entre se anula a la salida.

**Paso 4 — fuera de \( \omega_n \) deja pasar.** En continua, \( \omega=0 \): \( N(0)=\dfrac{\omega_n^2}{\omega_n^2}=1 \). En alta frecuencia, \( \omega\to\infty \): el \( -\omega^2 \) domina arriba y abajo, \( N\to\dfrac{-\omega^2}{-\omega^2}=1 \). El notch vale **1 (0 dB) lejos del pico** y solo cava la muesca en torno a \( \omega_n \); de ahí "rechazo de banda" estrecho.

## 2 — Profundidad finita: el papel de \( \zeta_z \)
**Paso 1 — caso general.** En la práctica se usa \( \zeta_z>0 \) (un notch infinito es frágil). Con \( N(s)=\dfrac{s^2+2\zeta_z\omega_n s+\omega_n^2}{s^2+2\zeta_p\omega_n s+\omega_n^2} \), en \( \omega=\omega_n \) los términos \( \omega_n^2-\omega^2 \) se cancelan en numerador y denominador, quedando solo las partes imaginarias:

$$ N(j\omega_n)=\frac{2\zeta_z\,\omega_n\,(j\omega_n)}{2\zeta_p\,\omega_n\,(j\omega_n)} $$

**Paso 2 — cancelar.** El factor \( 2\omega_n\,(j\omega_n)=2j\omega_n^2 \) es común y se cancela:

$$ \boxed{\;\big|N(j\omega_n)\big|=\frac{\zeta_z}{\zeta_p}\;} $$

La profundidad de la muesca es el **cociente \( \zeta_z/\zeta_p \)**: con \( \zeta_z=0 \) es 0 (atenuación infinita, caso ideal); con \( \zeta_z=0.02 \), \( \zeta_p=0.5 \) da \( 0.04 \), es decir \( 20\log_{10}(0.04)\approx-28 \) dB. Esto justifica el criterio de diseño \( \zeta_z\ll\zeta_p \).

## 3 — La FDT del filtro notch: derivación desde ceros complejos

**Paso 1 — el notch como cancelación de resonancia.** Para cancelar la resonancia del LCL a
\( \omega_{res} \), se centra el notch en esa frecuencia. La FDT es:

$$ G_{notch}(s) = \frac{s^2+\omega_0^2}{s^2+2\zeta_p\,\omega_0\,s+\omega_0^2} $$

Los **ceros** del numerador son exactamente \( s=\pm j\omega_0 \): en el eje imaginario puro.
En \( s=j\omega_0 \), el numerador se anula → \( |G_{notch}(j\omega_0)|=0 \): rechazo teórico total.

**Paso 2 — el factor de calidad Q.** Se define \( Q=1/(2\zeta_p) \):
- \( Q \) alto (\( \zeta_p \) pequeño) → muesca estrecha y profunda. Muy sensible a la frecuencia
  exacta: si la resonancia real está a \( f_{res}\pm\epsilon \), el notch puede no alcanzarla.
- \( Q \) bajo (\( \zeta_p \) grande) → muesca ancha y suave. Más robusto a la deriva de
  \( f_{res} \), pero introduce mayor retardo de fase en la banda de control.

**Paso 3 — ancho de banda de rechazo.** Las frecuencias a las que \( |G_{notch}|\ge-3 \) dB
están en:
$$ \Delta\omega_{-3\text{dB}} = \frac{\omega_0}{Q} = 2\zeta_p\,\omega_0 $$

Para \( f_0=3404 \) Hz y \( Q=10 \) (\( \zeta_p=0.05 \)):
\( \Delta f = 3404/10 = 340 \) Hz → rechazo efectivo entre 3234 y 3574 Hz.

**Paso 4 — efecto del notch en la respuesta de fase.** El notch introduce un **mínimo de fase
negativa** justo por debajo de \( \omega_0 \). La fase baja hasta \( -90° \) en
\( \omega\to\omega_0^- \) y vuelve a 0° en \( \omega\to\omega_0^+ \) (pasa rápidamente por el
cero). Esta pérdida de fase por debajo del notch es el coste del método: si el cruce de ganancia
\( \omega_c \) está cerca de \( \omega_0 \), el margen de fase se reduce.

$$ \angle G_{notch}(j\omega) \xrightarrow{\omega\to\omega_0^-} -90°,
   \quad \angle G_{notch}(j\omega) \xrightarrow{\omega\to\omega_0^+} +90° $$

## 4 — El notch asimétrico para la resonancia del LCL

El notch simétrico (ceros y polos centrados en \( \omega_{res} \)) tiene un problema: la FDT del
LCL tiene tanto una **resonancia** (pico) como una **antirresonancia** (valle), y el notch
simétrico afecta a ambas.

**Paso 1 — el notch centrado como caso base.** El notch centrado en la resonancia del LCL:
$$ G_{notch}(s) = \frac{s^2+\omega_{res}^2}{s^2+2\zeta_p\,\omega_{res}\,s+\omega_{res}^2} $$
Esta es la forma estándar y la más usada. Funciona bien cuando el pico de resonancia es el problema
dominante y la antirresonancia no interfiere con el lazo.

**Paso 2 — el notch asimétrico.** Se puede desplazar los polos a \( \omega_{pole}\neq\omega_{res} \):
$$ G_{notch,\text{asim}}(s) = \frac{s^2+\omega_{res}^2}{s^2+2\zeta_p\,\omega_{pole}\,s+\omega_{pole}^2} $$
Los ceros siguen en \( \pm j\omega_{res} \) (anulan exactamente la resonancia), pero los polos
están en \( \omega_{pole} \). Esto permite modelar el rechazo solo en la resonancia sin tocar
la antirresonancia. Para el LCL del proyecto 01, \( \omega_{pole}=\omega_{res} \) (notch centrado)
es la elección habitual; el asimétrico se usa cuando la antirresonancia del LCL está cerca del
cruce de ganancia y no se quiere pertorbar.

**Paso 3 — sintonía práctica.** El procedimiento:
1. Medir \( f_{res} \) con un barrido de frecuencia o calcularla de \( L_1,L_2,C_f \).
2. Centrar el notch: \( f_0 = f_{res} \).
3. Elegir \( Q \): si la variación de \( f_{res} \) con la red es ±5%, necesitas \( Q<10 \) para
   cubrir ese rango (la muesca de −3 dB cubre ±\( f_0/(2Q) \)).
4. Verificar que \( \omega_c\ll\omega_{res} \) para que la pérdida de fase no reduzca el PM.

## 5 — Implementación discreta: transformación bilineal con prewarping

Los filtros continuos deben discretizarse para implementarlos en un DSP con período \( T_s \).

**Paso 1 — por qué la Tustin simple no basta.** La transformación bilineal estándar
\( s=(2/T_s)(z-1)/(z+1) \) introduce **distorsión de frecuencia**: la frecuencia digital \( \Omega \)
se mapea a la continua como \( \omega=(2/T_s)\tan(\Omega T_s/2) \), no de forma lineal. Para un
notch a \( f_0=3404 \) Hz con \( T_s=100\,\mu\text{s} \), la diferencia es:

$$ \omega_{mapped} = \frac{2}{T_s}\tan\!\left(\frac{\omega_0 T_s}{2}\right)
   = \frac{2}{100\mu}\tan\!\left(\frac{2\pi\cdot3404\cdot100\mu}{2}\right) $$

Si no se corrige, el notch digital rechaza una frecuencia diferente a \( f_{res} \) → no atenúa
el pico.

**Paso 2 — prewarping.** La solución es calcular la frecuencia continua "prewarpada" tal que
la Tustin la mapee exactamente a \( \omega_0 \):

$$ \omega_{pw} = \frac{2}{T_s}\tan\!\left(\frac{\omega_0\,T_s}{2}\right) $$

Se diseña el filtro continuo con \( \omega_n=\omega_{pw} \) y luego se aplica Tustin.
El resultado es un filtro IIR de 2.° orden cuya frecuencia de rechazo digital es exactamente
\( f_0 \).

**Paso 3 — forma directa del filtro IIR.** La ecuación en diferencias:

$$ y[k] = b_0\,x[k] + b_1\,x[k-1] + b_2\,x[k-2] - a_1\,y[k-1] - a_2\,y[k-2] $$

Los coeficientes se obtienen de Tustin con prewarping:
- \( \Omega_0 = 2\tan(\omega_0 T_s/2)/T_s \) (frecuencia prewarpada)
- \( K = \Omega_0^2\,T_s^2/4 \)
- \( \gamma = \Omega_0\,\zeta_p\,T_s \)
- Denominador: \( D = 1 + \gamma + K \)
- \( b_0 = (1+K)/D,\quad b_1 = 2(K-1)/D,\quad b_2 = (1+K)/D \)
- \( a_1 = 2(K-1)/D,\quad a_2 = (1-\gamma+K)/D \)

**Paso 4 — ejemplo numérico para el proyecto 01.** \( f_0=3404 \) Hz, \( \zeta_p=0.05 \) (Q=10),
\( T_s=100\,\mu\text{s} \):
- \( \omega_0=2\pi\times3404=21390 \) rad/s
- \( \omega_{pw}=2/T_s\cdot\tan(\omega_0 T_s/2)=20000\cdot\tan(1.069)=23420 \) rad/s
- \( K=23420^2\times(100\mu)^2/4=1.371 \)
- \( \gamma=23420\times0.05\times100\mu=0.1171 \)
- \( D=1+0.1171+1.371=2.488 \)
- \( b_0=b_2=(1+1.371)/2.488=0.953 \), \( b_1=2(1.371-1)/2.488=0.298 \)
- \( a_1=0.298 \), \( a_2=(1-0.1171+1.371)/2.488=0.905 \)

## 6 — Notch para rechazar rizado de 2ω en el control de tensión

Un caso de uso frecuente que no es el LCL: el **bus DC de convertidores monofásicos**.

**Paso 1 — el rizado a 2ω.** Un convertidor monofásico transfiere potencia pulsante a
\( 2\omega_1 \) (100 Hz en red de 50 Hz). El bus DC tiene un rizado de tensión:

$$ v_{dc}(t) = V_{dc0} + \hat{V}_{2\omega}\cos(2\omega_1 t + \phi) $$

La amplitud \( \hat{V}_{2\omega} \) depende de la capacidad del bus: con \( C_{dc}=50\,\text{mF} \)
y \( P=10\,\text{kW} \):
\( \hat{V}_{2\omega} = P/(2\omega_1\,C_{dc}\,V_{dc0}) = 10000/(628\times0.05\times700) \approx 0.45\,\text{V} \).

**Paso 2 — el problema si el lazo de tensión es rápido.** Si el ancho de banda del lazo de tensión
DC supera los 100 Hz (\( \omega_{cv}>2\omega_1 \)), el PI de tensión ve el rizado como un "error"
y lo realimenta: la corriente de referencia tendrá componente a 100 Hz → distorsión en corriente AC.
La norma EN 61000-3-2 limita los armónicos inyectados → el rizado en la corriente es problemático.

**Paso 3 — notch en la realimentación de tensión.** Se inserta el notch a 100 Hz solo en la
rama de realimentación del lazo de tensión:

$$ V_{dc,filt}(s) = G_{notch,100}(s)\cdot V_{dc}(s), \quad f_0=100\,\text{Hz} $$

El PI de tensión recibe \( V_{dc,filt} \) en lugar de \( V_{dc} \) directamente: el rizado
a 100 Hz queda atenuado y no se amplifica en la corriente de referencia.

**Paso 4 — penalización en el margen de fase.** El notch a 100 Hz resta fase en esa banda.
Si el cruce del lazo de tensión está a 80–150 Hz, la pérdida de fase puede ser de 20–40°.
Hay que verificar el Bode del lazo cerrado de tensión con el notch incluido. Si el PM baja de 30°,
bajar el ancho de banda del PI de tensión (reducir \( K_{pv} \)).

$$ \text{Regla de diseño:}\quad \omega_{cv} < 0.5\,\omega_{notch} = \pi\times100 \approx 314\,\text{rad/s}\;(50\,\text{Hz}) $$

Con esta restricción, el margen de fase del lazo de tensión se mantiene por encima de 45°.

## 7 — Diseño iterativo: notch para el LCL del proyecto 01

El LCL del proyecto 01 tiene \( L_1=1.8\,\text{mH} \), \( L_2=0.6\,\text{mH} \), \( C_f=4.4\,\mu\text{F} \),
red aislada (sin \( L_g \)). La frecuencia de resonancia es:

$$ f_{res} = \frac{1}{2\pi}\sqrt{\frac{L_1+L_2}{L_1 L_2 C_f}}
   = \frac{1}{2\pi}\sqrt{\frac{2.4\times10^{-3}}{1.8\times0.6\times10^{-6}\times4.4\times10^{-6}}}
   \approx 3404\,\text{Hz} $$

**Situación base sin Kad:** El amortiguamiento del LCL es \( \zeta\approx0.02 \) (casi sin pérdidas).
El pico de resonancia en el Bode de la planta supera 40 dB. El lazo de corriente con PI simple
(\( f_c=500\,\text{Hz} \)) es inestable: el pico gana más de 0 dB antes de cruzar.

**Paso 1 — notch en 3404 Hz con Q=10.** Se diseña el notch centrado en \( f_{res} \), con
\( \zeta_p=0.05 \) (Q=10). La atenuación en \( f_{res} \) con \( \zeta_z=0.001 \) es:
\( 20\log_{10}(0.001/0.05)=20\log_{10}(0.02)=-34\,\text{dB} \). El pico del LCL de +40 dB queda
reducido a +6 dB: el lazo de corriente es estable.

El margen de fase del lazo de corriente:
- Sin notch: PM ≈ −15° (inestable)
- Con notch Q=10: PM ≈ 52° (estable, válido)

**Paso 2 — alternativa con Kad.** El amortiguamiento activo \( K_{ad}=6\,\Omega \) en la rama del
condensador eleva \( \zeta \) a ≈0.35. El pico de resonancia cae de 40 dB a 10 dB: el lazo de
corriente pasa a tener PM ≈ 48°. Sin notch.

**Paso 3 — comparativa de soluciones.**

| Estrategia | PM lazo corriente | Sensor extra | Robustez a \( f_{res} \) variable |
|------------|-------------------|--------------|-----------------------------------|
| Sin Kad, sin notch | −15° (inestable) | No | N/A |
| Notch Q=10 | 52° | No | Media (±5%) |
| Kad = 6 Ω | 48° | \( i_{Cf} \) | Alta |
| Kad + notch Q=5 | 62° | \( i_{Cf} \) | Alta |

Para el proyecto 01 en red aislada (sin variación de \( L_g \)), el notch Q=10 es suficiente y
no requiere sensor adicional. Con red variable, se prefiere Kad + notch para mayor robustez.

<div class="cfig"><img src="figuras/filtro-notch-analisis.png" alt="analisis filtro notch: Bode Q variable, lazo corriente, rizado Vdc, comparativa Kad vs notch"><div class="cap">(a) Bode del notch para Q=1,5,10,20 a fres=3404 Hz: mayor Q da muesca más estrecha y profunda pero más sensible a la frecuencia exacta. (b) Lazo de corriente LCL: sin notch el pico supera 40 dB, con notch Q=10 queda suprimido y el PM es mayor de 45°. (c) Notch 100 Hz en la realimentación de tensión DC monofásica: atenúa el rizado 2ω antes de entrar al PI. (d) Comparativa: sin Kad ni notch el lazo es inestable; Kad y notch son alternativas viables; combinados dan el mayor PM.</div></div>

## Cuándo y por qué se usa
Para estabilizar el lazo de corriente con filtro LCL sin recurrir a sensores extra de
amortiguamiento activo, o para eliminar un armónico/oscilación concreta. Encaja en el moldeo de
[[loop-shaping]].

## Procedimiento de diseño (genérico)
1. Identifica la frecuencia de resonancia \( \omega_{res}=\sqrt{\frac{L_1+L_2}{L_1 L_2 C}} \) del LCL.
2. Sitúa \( \omega_n=\omega_{res} \); elige \( \zeta_p \) (ancho) y \( \zeta_z\ll\zeta_p \) (profundidad).
3. Comprueba la fase introducida cerca de \( \omega_c \): si daña el margen, aleja el cruce o ensancha.
4. Verifica robustez: barre \( L,C \) (ver [[barrido-parametrico]]) y confirma que el pico queda
   atenuado en todo el rango.
5. Discretiza con Tustin/*prewarp* en \( \omega_n \).

## Ejemplo de código
```python
import control as ct
wn, zz, zp = 2*3.1416*2500, 0.02, 0.5
notch = ct.tf([1, 2*zz*wn, wn**2], [1, 2*zp*wn, wn**2])
```

## Parámetros y valores típicos
\( \zeta_z \approx 0.01\text{–}0.05 \), \( \zeta_p \approx 0.3\text{–}0.7 \). Profundidad de muesca
20–40 dB. \( \omega_n \) en la resonancia LCL (típica 1–5 kHz).

## Errores comunes
- Notch muy estrecho con \( \omega_{res} \) mal estimada → no atenúa nada (queda al lado del pico).
- Colocar \( \omega_n \) cerca de \( \omega_c \) → la pérdida de fase desestabiliza el lazo.
- Ignorar la deriva de la resonancia con el punto de operación/tolerancias.
- No usar prewarping en la discretización → el notch digital cae a una frecuencia diferente.

## Conceptos relacionados
- [[filtro-lcl|amortiguamiento activo]] · [[loop-shaping]] · [[diagrama-bode]] · [[barrido-parametrico]]

## Referencias
- Yepes et al., *Resonant current controllers*, IEEE TIE 2011.
- Peña-Alzola et al., *LCL-filter design for grid converters*, IEEE TPEL 2014.
- Briz & Hinkkanen, *Design of deadbeat controllers*, IEEE TPEL 2021.
