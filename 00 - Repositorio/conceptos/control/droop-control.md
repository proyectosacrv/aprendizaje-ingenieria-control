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
fecha_actualizacion: 2026-06-08
relacionados: [grid-forming-vs-following, vsm-inercia, impedancia-virtual, analisis-modal]
referencias:
  - "Chandorkar, Divan, Adapa, Control of Parallel Connected Inverters, IEEE TIA 1993"
---

## Definición
Estrategia de grid-forming que fija la **frecuencia** según la potencia activa y la **tensión**
según la reactiva, emulando el estatismo de un generador síncrono. Permite sincronizar y
repartir carga **sin comunicación ni PLL**.

## Fundamento teórico
$$ \omega = \omega_0 + m_p\,(P_{set}-P), \qquad V^{*} = V_0 + n_q\,(Q_{set}-Q) $$
$$ \dot\delta = \omega - \omega_0 $$
La potencia se mide y filtra (paso-bajo \( \omega_f \)) para quitar el rizado:
\( \dot{P}_m=\omega_f(P-P_m) \). El lazo de potencia activa tiene un **integrador** (el ángulo
\( \delta \)) y el polo del filtro \( \omega_f \): si la ganancia \( m_p\,\partial P/\partial\delta \)
es alta, el cruce cae donde el filtro ya da −90° → poco margen de fase.

## Cuándo y por qué se usa
Base de la mayoría de microrredes y grid-forming. Para una línea inductiva, P↔ángulo y
Q↔tensión están desacoplados, lo que justifica el emparejamiento P-f / Q-V.

## Procedimiento de diseño (genérico)
1. **\( m_p \)** desde la caída de frecuencia admisible a plena potencia (típico 0.5–2%):
   \( m_p = \dfrac{\Delta\omega_{max}}{S_n} = \dfrac{(\text{droop}\%)\,\omega_0}{S_n} \).
2. **\( n_q \)** desde la caída de tensión admisible (típico 2–5%): \( n_q=\dfrac{(\text{droop}\%)\,V_0}{S_n} \).
3. **Filtro de potencia \( \omega_f \)**: bajo (5–20 Hz) para promediar el rizado y mantener el
   lazo de potencia lento; un \( \omega_f \) alto acerca el polo al cruce y reduce el margen.
4. Verifica el **amortiguamiento del modo de potencia** con autovalores. Si es bajo, usa
   [[impedancia-virtual]] (reduce \( \partial P/\partial\delta \)) o pasa a [[vsm-inercia]].

## Ejemplo de código
```python
mp = droop_p*w0/Sn           # (rad/s)/W
nq = droop_q*V0/Sn           # V/var
w  = w0 + mp*(Pset - Pm)     # droop P-f
Vref = V0 + nq*(Qset - Qm)   # droop Q-V
ddelta = w - w0; dPm = wf*(P - Pm); dQm = wf*(Q - Qm)
```

## Parámetros y valores típicos
\( m_p \) (droop P-f) 0.5–2 %, \( n_q \) (droop Q-V) 2–5 %, \( f_{pow} \) 5–20 Hz. En el proyecto: 0.5 % / 2 % / 15 Hz.

## Errores comunes
- \( \omega_f \) demasiado alto → modo de potencia mal amortiguado o inestable.
- Asumir desacoplo P-f / Q-V con línea resistiva (X/R bajo): ahí P y Q se acoplan.

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: sincronizar sin PLL): droop P-f/Q-V como capa externa.
  El modo de potencia resultó a 3.3 Hz; su amortiguamiento se trató con impedancia virtual.

## Conceptos relacionados
- [[grid-forming-vs-following]] · [[vsm-inercia]] · [[impedancia-virtual]] · [[analisis-modal]]

## Referencias
- Chandorkar et al., IEEE TIA 1993.
