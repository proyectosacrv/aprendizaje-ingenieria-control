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
fecha_actualizacion: 2026-06-11
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
