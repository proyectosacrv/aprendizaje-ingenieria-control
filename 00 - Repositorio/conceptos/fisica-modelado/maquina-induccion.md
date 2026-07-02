---
titulo: Máquina de inducción (asíncrona)
slug: maquina-induccion
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: []
objetivos: [base de la eólica DFIG y de los accionamientos AC]
tags: [maquina-induccion, asincrona, deslizamiento, dfig, basico]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-07-02
relacionados: [generador-sincrono, eolica-mppt, control-vectorial, marco-dq, sistema-trifasico]
referencias:
  - "Fitzgerald, Electric Machinery, McGraw-Hill"
  - "Krause, Analysis of Electric Machinery"
---

## Definición
Máquina de corriente alterna cuyo rotor **no** gira sincronizado con el campo del estátor, sino con un
pequeño retraso (**deslizamiento**). No necesita excitación externa en el rotor: las corrientes del
rotor se **inducen** (de ahí "inducción"). Es la máquina más usada como motor y, en eólica, como
generador (jaula o DFIG).

## Fundamento teórico
El estátor crea un campo giratorio a la **velocidad de sincronismo**:
$$ n_s = \frac{120 f}{p} \ \text{[rpm]} \qquad (\,p = \text{nº de polos}\,) $$
El rotor gira a \( n \), y el **deslizamiento** es
$$ s = \frac{n_s - n}{n_s} $$
- \( 0 < s < 1 \): funcionamiento como **motor** (el rotor va más lento que el campo).
- \( s < 0 \) (rotor más rápido que el campo): funcionamiento como **generador**.
El circuito equivalente por fase tiene \( R_1, X_1 \) (estátor), \( X_m \) (magnetización) y
\( R_2/s, X_2 \) (rotor referido): el término \( R_2/s \) concentra la dependencia con la carga. El
par es máximo a un cierto deslizamiento y cae a cero en sincronismo.

<div class="cfig"><img src="figuras/maquina-induccion-par.png" alt="curva par-velocidad de la maquina de induccion"><div class="cap">Curva par–velocidad: por debajo del sincronismo ($n<n_s$, $0<s<1$) la máquina funciona como motor; por encima ($n>n_s$, $s<0$) como generador. El par se anula exactamente en sincronismo porque sin deslizamiento no se inducen corrientes en el rotor. La DFIG opera ±30 % alrededor del sincronismo con un convertidor de potencia parcial.</div></div>

## 1 — El deslizamiento y por qué el par se anula en sincronismo
**Paso 1 — qué es el deslizamiento.** El campo del estátor gira a \( n_s \); el rotor gira a \( n \). El deslizamiento mide la velocidad **relativa** del rotor respecto al campo, normalizada a \( n_s \):

$$ \boxed{\;s=\frac{n_s-n}{n_s}\;}\qquad\Longrightarrow\qquad n=n_s(1-s) $$

En reposo \( n=0\Rightarrow s=1 \); en sincronismo \( n=n_s\Rightarrow s=0 \). Para \( n=1455 \) rpm con \( n_s=1500 \) rpm: \( s=(1500-1455)/1500=0.03 \) (3 %, motor).

**Paso 2 — la frecuencia que ve el rotor.** Las barras del rotor cortan el campo a la velocidad relativa \( n_s-n=s\,n_s \). La FEM inducida en el rotor es proporcional a esa velocidad relativa, luego a la frecuencia de deslizamiento \( f_r=s\,f \):

$$ E_{rotor}\propto s\,n_s\;\Longrightarrow\; I_{rotor}\propto E_{rotor}\propto s $$

**Paso 3 — el par.** El par electromagnético sale de la potencia que cruza el entrehierro disipada en la resistencia rotórica referida \( R_2/s \). Con la corriente rotórica \( I_2 \), esa potencia es \( P_{ag}=3\,I_2^2\,R_2/s \), y el par es \( P_{ag} \) entre la velocidad de sincronismo en rad/s, \( \omega_s \):

$$ T=\frac{P_{ag}}{\omega_s}=\frac{3\,I_2^2\,(R_2/s)}{\omega_s} $$

Con el circuito equivalente (estátor \( R_1,X_1 \); rotor \( R_2/s,X_2 \)) la corriente rotórica es \( I_2=\dfrac{V_1}{\sqrt{(R_1+R_2/s)^2+(X_1+X_2)^2}} \). Sustituyendo:

$$ \boxed{\;T=\frac{3\,V_1^2\,(R_2/s)}{\omega_s\big[(R_1+R_2/s)^2+(X_1+X_2)^2\big]}\;} $$

**Paso 4 — el límite en sincronismo.** Cuando \( n\to n_s \), \( s\to 0 \) y \( R_2/s\to\infty \): en la fórmula del par, el numerador crece como \( 1/s \) pero el denominador crece como \( (R_2/s)^2\sim 1/s^2 \), que domina, así que \( T\to 0 \). Físicamente: sin deslizamiento las barras no cortan el campo, no se induce corriente (\( I_2\to0 \)) y no hay par. **Esta es la diferencia esencial con la [[generador-sincrono|máquina síncrona]]:** la de inducción *necesita* deslizar para producir par. Derivando \( T \) respecto a \( s \) se obtiene el par máximo en \( s_{max}=R_2/\sqrt{R_1^2+(X_1+X_2)^2} \). Para \( s<0 \) (rotor más rápido que el campo) el par cambia de signo: la máquina **genera** (caso DFIG/eólica).

## 2 — El modelo en espacio de estados dq de la máquina de inducción

**Los cuatro estados.** En el marco dq girado con el campo del estátor (\( \omega_s \)), los estados son las corrientes de estátor y los flujos de rotor:

$$ \mathbf{x}=\begin{bmatrix}i_{sd}\\i_{sq}\\\psi_{rd}\\\psi_{rq}\end{bmatrix} $$

**Las ecuaciones diferenciales.** Definiendo \( \sigma = 1 - L_m^2/(L_s L_r) \) (factor de dispersión), \( L_{v\sigma s}=\sigma L_s \) y \( \tau_r=L_r/R_r \) (constante de tiempo del rotor):

$$  L_{v\sigma s}\frac{di_{sd}}{dt} = v_{sd} - R_s i_{sd} + \omega_s L_{v\sigma s} i_{sq} + \frac{L_m}{L_r}\left(\frac{\psi_{rd}}{\tau_r} - \omega_r \psi_{rq}\right) $$

$$  L_{v\sigma s}\frac{di_{sq}}{dt} = v_{sq} - R_s i_{sq} - \omega_s L_{v\sigma s} i_{sd} + \frac{L_m}{L_r}\left(\frac{\psi_{rq}}{\tau_r} + \omega_r \psi_{rd}\right) $$

$$  \frac{d\psi_{rd}}{dt} = -\frac{\psi_{rd}}{\tau_r} + (\omega_s-\omega_r)\psi_{rq} + \frac{L_m}{\tau_r}i_{sd} $$

$$  \frac{d\psi_{rq}}{dt} = -\frac{\psi_{rq}}{\tau_r} - (\omega_s-\omega_r)\psi_{rd} + \frac{L_m}{\tau_r}i_{sq} $$

**El par electromagnético** (en pu, con P pares de polos):
$$  T_e = \frac{3}{2}\,P\,\frac{L_m}{L_r}\left(\psi_{rd}\,i_{sq} - \psi_{rq}\,i_{sd}\right) $$

**Complejidad del modelo.** Las cuatro ecuaciones están acopladas: los flujos del rotor aparecen en las ecuaciones de corriente del estátor y viceversa. El modelo completo es no lineal (productos \( \omega_r\psi_{rd} \), etc.) lo que motivó el desarrollo del FOC para linealizar mediante cambio de variables.

## 3 — El modelo simplificado en FOC (Field Oriented Control)

**Orientación de flujo del rotor.** En FOC se elige el marco dq de modo que \( \psi_{rq}=0 \) en todo instante. Entonces:

$$  \frac{d\psi_{rd}}{dt} = -\frac{\psi_{rd}}{\tau_r} + \frac{L_m}{\tau_r}i_{sd} \qquad\Rightarrow\qquad \boxed{\tau_r\dot\psi_{rd}+\psi_{rd}=L_m\,i_{sd}} $$

El flujo del rotor responde como un primer orden de tiempo \( \tau_r \) forzado por \( i_{sd} \).

**El par en FOC.** Con \( \psi_{rq}=0 \):

$$  \boxed{T_e = \frac{3}{2}\,P\,\frac{L_m}{L_r}\,\psi_{rd}\,i_{sq}} $$

El par es proporcional al producto \( \psi_{rd}\cdot i_{sq} \): si el flujo está establecido (\( \psi_{rd}=\text{cte} \)), el par es lineal en \( i_{sq} \). Esto desacopla el control:

- **Lazo de flujo** (lento, constante de tiempo \( \tau_r \)): \( i_{sd}^* \) controla \( \psi_{rd} \).
- **Lazo de par** (rápido, \( \tau_c=1/\alpha_c\ll\tau_r \)): \( i_{sq}^* \) controla \( T_e \).

La **separación temporal** entre los dos lazos es el requisito fundamental del FOC. Si \( \alpha_c\gg1/\tau_r \), el par responde a \( i_{sq}^* \) sin perturbar el flujo.

## 4 — El deslizamiento y la frecuencia del rotor en FOC

**El ángulo del flujo del rotor.** En FOC, el marco dq gira a la velocidad del flujo del rotor \( \omega_s \), no a la velocidad de la red. Esta velocidad no se mide directamente: se estima a partir del deslizamiento:

$$  \omega_s = \omega_r + \omega_{slip}, \qquad \omega_{slip} = \frac{L_m\,i_{sq}}{\tau_r\,\psi_{rd}} $$

El ángulo de Park se obtiene integrando \( \omega_s \):

$$  \theta_s(t)=\int_0^t \omega_s(\tau)\,d\tau = \int_0^t \left[\omega_r(\tau)+\frac{L_m\,i_{sq}(\tau)}{\tau_r\,\psi_{rd}(\tau)}\right]d\tau $$

**La desalineación por error en \( R_r \).** La constante de tiempo del rotor es \( \tau_r=L_r/R_r \), y \( R_r \) varía con la temperatura (puede subir un 20–30 % de frío a caliente). Si se usa \( \tau_r^{est}\ne\tau_r^{real} \):

$$  \omega_{slip}^{est}=\frac{L_m\,i_{sq}}{\tau_r^{est}\,\psi_{rd}}\ne\omega_{slip}^{real} $$

El error acumulado en \( \theta_s \) desalinea el marco dq respecto al flujo real del rotor: \( \psi_{rq}\ne0 \) y el desacoplamiento del FOC se rompe. El par estimado difiere del real, degradando el control de velocidad.

**Corrección en línea.** Los variadores modernos identifican \( R_r \) en caliente mediante inyección de señal o estimación de estado (Kalman), actualizando \( \tau_r^{est} \) continuamente.

<div class="cfig"><img src="figuras/maquina-induccion-analisis.png" alt="FOC y dinámica de la máquina de inducción"><div class="cap">Panel (a): la curva par–velocidad de arranque directo (zona de par máximo limitado) frente al FOC que mantiene el par máximo hasta la velocidad base, y luego flux weakening. Panel (b): el modelo desacoplado del FOC con los dos lazos (flujo lento y par rápido). Panel (c): respuesta dinámica ante un escalón de Te*, mostrando que isq responde rápido (αc) mientras isd y ψrd permanecen constantes. Panel (d): el error de ángulo acumulado cuando Rr cambia un ±20%, que desalinea el marco FOC progresivamente.</div></div>

## 5 — Curvas características: par-velocidad y su control

**Arranque directo.** Sin control, la curva \( T(n) \) está dada por la fórmula del circuito equivalente. Tiene un máximo en \( s_{max}=R_2/\sqrt{R_1^2+(X_1+X_2)^2} \), típicamente \( s_{max}\approx0.1\text{–}0.3 \). En el arranque (\( s=1 \)), la corriente es 5–7 veces la nominal y el par es solo 1.5–2 veces el nominal.

**Con FOC: par constante hasta la velocidad base.** Manteniendo \( \psi_{rd}=\psi_{rd,nom} \) (flujo nominal) e \( i_{sd}=i_{sd,nom} \), el par máximo disponible es:

$$  T_{max}^{FOC}=\frac{3}{2}P\frac{L_m}{L_r}\,\psi_{rd,nom}\,I_{s,max} $$

Este par se puede mantener desde \( n=0 \) hasta la **velocidad base** \( n_{base}=n_s \) porque el convertidor puede suministrar la tensión necesaria con \( f \) variable.

**Flux weakening (por encima de la velocidad base).** Para \( n>n_s \), la tensión del convertidor ya está saturada. Para subir la frecuencia hay que bajar el flujo (\( \psi_{rd}\propto V/f \)) y el par disponible decrece:

$$  T_{max}(n)=T_{max}^{FOC}\cdot\frac{n_{base}}{n},\qquad n>n_{base} $$

La **potencia** \( P=T\cdot\omega_r \) permanece constante en esta región: el flux weakening es la zona de **potencia constante**. Esta región es equivalente al régimen de debilitamiento de campo de una máquina DC.

## 6 — Diseño iterativo: FOC para motor de inducción 500 kW

**Parámetros del motor** (en pu, base \( S_n=500\,\text{kW} \), \( f=50\,\text{Hz} \)):

| Parámetro | Valor | Significado |
|-----------|-------|-------------|
| \( R_s \) | 0.01 pu | Resistencia de estátor |
| \( R_r \) | 0.008 pu | Resistencia de rotor (en frío) |
| \( L_m \) | 3.0 pu | Inductancia de magnetización |
| \( \sigma \) | 0.05 | Factor de dispersión total |
| \( \tau_r \) | \( L_r/R_r \approx 3.08/0.008=385\,\text{ms} \)| Constante de tiempo del rotor |
| P | 2 pares de polos | \( n_s=1500 \) rpm |

**Paso 1 — ancho de banda del lazo de corriente.** Se elige \( \alpha_c=2\pi\cdot100\,\text{Hz}=628\,\text{rad/s} \) (lazo de par rápido). Comprobación de separación: \( \alpha_c\cdot\tau_r=628\times0.385\approx242\gg1 \) ✓.

**Paso 2 — lazo de flujo.** El lazo de flujo debe ser más lento que \( 1/\tau_r \) para no excitar el transitorio del rotor. Se elige \( \alpha_\psi\approx1/\tau_r/10\approx2.6\,\text{rad/s} \). El regulador de flujo es un PI:

$$  i_{sd}^*(s)=\left(K_{p\psi}+\frac{K_{i\psi}}{s}\right)\left(\psi_{rd}^*-\psi_{rd}\right) $$

con \( K_{p\psi}=\alpha_\psi\cdot\tau_r/L_m \), \( K_{i\psi}=\alpha_\psi/L_m \).

**Paso 3 — lazo de par/velocidad.** El lazo de par usa \( i_{sq}^* = T_e^*/(k_T\psi_{rd}) \) con \( k_T=\tfrac32 P L_m/L_r \). El lazo de velocidad (por encima del lazo de par) tiene ancho de banda \( \alpha_v\approx\alpha_c/10=62\,\text{rad/s} \): es el más lento de los tres lazos.

**Paso 4 — verificación de la separación temporal.**

$$ \alpha_c \gg \alpha_v \gg \alpha_\psi \gg 1/\tau_r $$
$$ 628 \gg 62 \gg 2.6 \gg 2.6 \quad\text{(escalonado x10 entre lazos)}\quad\checkmark $$

La jerarquía de 10:1 entre lazos consecutivos garantiza que cada lazo "ve" los lazos internos como instantáneos y los externos como estáticos.

## Cuándo y por qué se usa
En accionamientos de velocidad variable (con control vectorial) y en generación eólica: la **DFIG**
(doblemente alimentada) alimenta el rotor por un convertidor para operar a velocidad variable en torno
al sincronismo con un convertidor de potencia reducida.

## Procedimiento de diseño (genérico)
1. Determina \( n_s \) a partir de \( f \) y \( p \).
2. Plantea el circuito equivalente y la curva par-velocidad.
3. Para control de velocidad/par, usa **control vectorial** (orientación de campo) en el marco dq.
4. Diseña los tres lazos (corriente, flujo, velocidad) con separación temporal 10:1.
5. Compensa la variación de \( R_r \) con temperatura mediante estimación en línea.

## Ejemplo de código
```python
f, p, n = 50.0, 4, 1455.0
ns = 120*f/p                 # 1500 rpm
s  = (ns - n)/ns             # deslizamiento ~ 0.03 (motor)

# FOC: referencia de corriente de par
Lm, Lr, P_poles = 3.0, 3.05, 2   # en pu
k_T = 1.5 * P_poles * Lm / Lr    # ganancia par
isq_ref = Te_ref / (k_T * psi_rd) # referencia isq

# deslizamiento estimado
omega_slip = (Lm * isq) / (tau_r * psi_rd)
omega_s = omega_r + omega_slip
```

## Parámetros y valores típicos
Deslizamiento nominal: 1–5 % (motor). En generación, \( s \) negativo de magnitud similar. La DFIG
maneja \( \pm 30\% \) de velocidad con un convertidor de ~30 % de la potencia nominal.
\( \tau_r \): 50–500 ms (máquinas pequeñas a grandes). Varía un 20–30 % con la temperatura.

## Errores comunes
- Confundirla con la síncrona (la asíncrona necesita deslizamiento para producir par).
- Equivocar el signo del deslizamiento en modo generador.
- Olvidar que el par cae a cero exactamente en sincronismo.
- Usar \( \tau_r \) a temperatura ambiente en el FOC de una máquina caliente → desalineación del marco dq.

## Conceptos relacionados
- [[generador-sincrono]] · [[eolica-mppt]] · [[control-vectorial]] · [[marco-dq]] · [[sistema-trifasico]]

## Referencias
- Fitzgerald, *Electric Machinery*.
- Krause, *Analysis of Electric Machinery*.
