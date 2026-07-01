---
titulo: Control por droop (P-f, Q-V)
slug: droop-control
categoria: control
tipo: tecnica
nivel: intermedio
proyectos: [01-GFM-Impedance]
objetivos: [sincronizar sin PLL, repartir potencia entre fuentes]
tags: [grid-forming, droop, frecuencia, reparto-carga, dq]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-30
relacionados: [grid-forming-vs-following, vsm-inercia, impedancia-virtual, transferencia-potencia-linea, analisis-modal]
referencias:
  - "Chandorkar, Divan, Adapa, Control of Parallel Connected Inverters, IEEE TIA 1993"
---

## Definición
Estrategia de **grid-forming** que fija la **frecuencia** según la potencia activa y la **tensión**
según la reactiva, emulando el estatismo de un generador síncrono. Permite sincronizar y repartir
carga **sin comunicación ni PLL**.

## De dónde se sale — el flujo de potencia en la línea
Entre la tensión del inversor \( E\angle\delta \) y la red \( V\angle 0 \) a través de una línea
**inductiva** \( X \), la potencia que se transfiere es (ver [[transferencia-potencia-linea]]):
$$ P=\frac{EV}{X}\sin\delta,\qquad Q=\frac{V\,(E\cos\delta-V)}{X} $$
Para ángulos pequeños (\( \sin\delta\approx\delta,\ \cos\delta\approx1 \)):
$$ P\approx\frac{EV}{X}\,\delta,\qquad Q\approx\frac{V}{X}\,(E-V) $$
Es decir: **P depende del ángulo** \( \delta \) y **Q depende de la diferencia de tensión** \( E-V \).
Como el ángulo es la integral de la frecuencia (\( \dot\delta=\omega-\omega_0 \)), controlar la
frecuencia controla \( P \), y controlar la amplitud controla \( Q \). Eso **justifica** el
emparejamiento P–f / Q–V.

## Fundamento teórico — las leyes de droop
Se invierte la relación anterior: en vez de medir, se **impone** la frecuencia y la tensión con una
pendiente (estatismo) frente a la potencia:
$$ \omega=\omega_0+m_p\,(P_{set}-P),\qquad V^{*}=V_0+n_q\,(Q_{set}-Q),\qquad \dot\delta=\omega-\omega_0 $$

<div class="cfig"><img src="figuras/droop-control-curvas.png" alt="curvas de droop P-f y Q-V"><div class="cap">Curvas de estatismo: la frecuencia cae con la potencia activa (pendiente −mp) y la tensión cae con la reactiva (pendiente −nq). La pendiente fija el reparto de carga entre unidades.</div></div>

La potencia medida se filtra (paso-bajo \( \omega_f \)) para quitar el rizado:
\( \dot{P}_m=\omega_f(P-P_m) \). El **lazo de potencia activa** tiene un integrador (el ángulo
\( \delta \)) y el polo del filtro \( \omega_f \): su ganancia en pequeña señal es
\( m_p\,\partial P/\partial\delta \) con \( \partial P/\partial\delta=\tfrac{EV}{X}\cos\delta \).

> **A resaltar:** si \( m_p\,\partial P/\partial\delta \) es alta, el cruce del lazo cae donde el
> filtro \( \omega_f \) ya aporta −90° → **poco margen de fase** y un modo de potencia mal amortiguado.
> Se baja con [[impedancia-virtual]] (sube \( X \), reduce \( \partial P/\partial\delta \)) o se pasa a
> [[vsm-inercia]].

## 1 — De la caída de frecuencia admisible a la pendiente \( m_p \)
**Paso 1 — qué fija el diseñador.** El estatismo se especifica como un porcentaje: "la frecuencia cae un \( \text{droop}\% \) entre vacío y plena potencia". Es decir, al pasar de \( P=0 \) a \( P=S_n \) la frecuencia debe caer una cantidad
$$ \Delta\omega_{max}=(\text{droop}\%)\,\omega_0 $$
Por ejemplo, \( 0.5\,\% \) sobre \( \omega_0=2\pi\cdot50 \) son \( \Delta\omega_{max}=0.005\cdot314.16=1.571\,\text{rad/s} \), o sea \( 0.25\,\text{Hz} \) de caída a plena carga.

**Paso 2 — igualar a la ley de droop.** La ley \( \omega=\omega_0+m_p\,(P_{set}-P) \) dice que la desviación de frecuencia respecto a \( \omega_0 \) (con \( P_{set}=0 \)) es \( \Delta\omega=-m_p\,P \). En módulo, al cargar de \( 0 \) a \( S_n \):
$$ |\Delta\omega_{max}|=m_p\,S_n $$

**Paso 3 — despejar la pendiente.** Igualando las dos expresiones de \( \Delta\omega_{max} \):
$$ m_p\,S_n=(\text{droop}\%)\,\omega_0\;\Longrightarrow\;\boxed{\;m_p=\frac{(\text{droop}\%)\,\omega_0}{S_n}\;} $$
La misma cuenta con \( V_0 \) en lugar de \( \omega_0 \) da \( n_q=(\text{droop}\%)\,V_0/S_n \) para el droop Q–V. La pendiente tiene unidades \( (\text{rad/s})/\text{W} \): es lo que convierte un error de potencia en una desviación de frecuencia.

## 2 — Por qué el filtro de potencia limita el ancho de banda del lazo P–f
**Paso 1 — la planta del lazo de potencia.** En pequeña señal, una perturbación de ángulo \( \tilde\delta \) mueve la potencia con la pendiente del flujo de carga, \( \partial P/\partial\delta=\tfrac{EV}{X}\cos\delta_0=:K_s \) (par sincronizante). El ángulo es la integral de la frecuencia, \( \dot{\tilde\delta}=\tilde\omega=-m_p\,\tilde P_m \), y la potencia medida pasa por el paso-bajo \( \dot{\tilde P}_m=\omega_f(\tilde P-\tilde P_m) \). Encadenando, la ganancia de lazo abierto es
$$ L(s)=\underbrace{m_p}_{\text{droop}}\cdot\underbrace{\frac{K_s}{s}}_{\delta\to P}\cdot\underbrace{\frac{\omega_f}{s+\omega_f}}_{\text{filtro}} $$

**Paso 2 — los dos polos.** \( L(s) \) tiene un **integrador** (el \( 1/s \) del ángulo) y el **polo del filtro** en \( -\omega_f \). El integrador ya aporta \( -90° \) de fase a toda frecuencia; el filtro añade otros \( -90° \) más a partir de \( \omega_f \). Cerca del cruce, la fase tiende a \( -180° \): el margen de fase sale de lo que falte para los \( -180° \) en la frecuencia de cruce \( \omega_c \) (donde \( |L(j\omega_c)|=1 \)).

**Paso 3 — la trampa de subir la ganancia.** Subir \( m_p \) o \( K_s \) (red más fuerte, \( X \) menor) empuja \( \omega_c \) hacia y por encima de \( \omega_f \), justo donde el filtro ya está restando fase:
$$ \angle L(j\omega_c)=-90°-\arctan\!\frac{\omega_c}{\omega_f}\;\xrightarrow{\;\omega_c\gg\omega_f\;}\;-180° $$
Por eso un \( \omega_f \) **alto** (acerca el polo al cruce) o un \( m_p K_s \) alto dejan el **modo de potencia mal amortiguado**. Las dos palancas para recuperar margen son: bajar \( \omega_f \), o reducir \( K_s \) subiendo \( X \) con [[impedancia-virtual]] (lo que aplana \( P(\delta) \)). Si aun así falta, se pasa a [[vsm-inercia]], que añade inercia y un amortiguamiento \( D \) explícito.

## Cuándo y por qué se usa
Base de la mayoría de microrredes y grid-forming. El reparto de carga es automático: dos unidades con
la misma pendiente se reparten la potencia a partes iguales, sin comunicación.

## Procedimiento de diseño (genérico)
1. **\( m_p \)** desde la caída de frecuencia admisible a plena potencia (típico 0.5–2 %):
   \( m_p=\dfrac{\Delta\omega_{max}}{S_n}=\dfrac{(\text{droop}\%)\,\omega_0}{S_n} \).
2. **\( n_q \)** desde la caída de tensión admisible (típico 2–5 %): \( n_q=\dfrac{(\text{droop}\%)\,V_0}{S_n} \).
3. **Filtro de potencia \( \omega_f \)** bajo (5–20 Hz): promedia el rizado y mantiene lento el lazo
   de potencia. Un \( \omega_f \) alto acerca el polo al cruce y reduce el margen.
4. Verifica el **amortiguamiento del modo de potencia** con autovalores ([[analisis-modal]]). Si es
   bajo, usa [[impedancia-virtual]] o pasa a [[vsm-inercia]].

## Ejemplo de código
```python
mp = droop_p*w0/Sn           # (rad/s)/W
nq = droop_q*V0/Sn           # V/var
w  = w0 + mp*(Pset - Pm)     # droop P-f
Vref = V0 + nq*(Qset - Qm)   # droop Q-V
ddelta = w - w0; dPm = wf*(P - Pm); dQm = wf*(Q - Qm)
```

## Parámetros y valores típicos
\( m_p \) (droop P-f) 0.5–2 %, \( n_q \) (droop Q-V) 2–5 %, \( f_{pow} \) 5–20 Hz. En el proyecto:
0.5 % / 2 % / 15 Hz.

## Errores comunes
- \( \omega_f \) demasiado alto → modo de potencia mal amortiguado o inestable.
- Asumir desacoplo P-f / Q-V con **línea resistiva** (X/R bajo): ahí P y Q se acoplan y hay que rotar
  las consignas o usar impedancia virtual.

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: sincronizar sin PLL): droop P-f/Q-V como capa externa. El modo de
  potencia resultó a 3.3 Hz; su amortiguamiento se trató con impedancia virtual.

## Conceptos relacionados
- [[grid-forming-vs-following]] · [[vsm-inercia]] · [[impedancia-virtual]] · [[transferencia-potencia-linea]] · [[analisis-modal]]

## Referencias
- Chandorkar et al., IEEE TIA 1993.
