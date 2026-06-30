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
fecha_actualizacion: 2026-06-30
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

## Cuándo y por qué se usa
En accionamientos de velocidad variable (con control vectorial) y en generación eólica: la **DFIG**
(doblemente alimentada) alimenta el rotor por un convertidor para operar a velocidad variable en torno
al sincronismo con un convertidor de potencia reducida.

## Procedimiento de diseño (genérico)
1. Determina \( n_s \) a partir de \( f \) y \( p \).
2. Plantea el circuito equivalente y la curva par-velocidad.
3. Para control de velocidad/par, usa **control vectorial** (orientación de campo) en el marco dq.

## Ejemplo de código
```python
f, p, n = 50.0, 4, 1455.0
ns = 120*f/p                 # 1500 rpm
s  = (ns - n)/ns             # deslizamiento ~ 0.03 (motor)
```

## Parámetros y valores típicos
Deslizamiento nominal: 1–5 % (motor). En generación, \( s \) negativo de magnitud similar. La DFIG
maneja \( \pm 30\% \) de velocidad con un convertidor de ~30 % de la potencia nominal.

## Errores comunes
- Confundirla con la síncrona (la asíncrona necesita deslizamiento para producir par).
- Equivocar el signo del deslizamiento en modo generador.
- Olvidar que el par cae a cero exactamente en sincronismo.

## Conceptos relacionados
- [[generador-sincrono]] · [[eolica-mppt]] · [[control-vectorial]] · [[marco-dq]] · [[sistema-trifasico]]

## Referencias
- Fitzgerald, *Electric Machinery*.
- Krause, *Analysis of Electric Machinery*.
