---
titulo: VSM — máquina síncrona virtual (inercia)
slug: vsm-inercia
categoria: control
tipo: tecnica
nivel: avanzado
proyectos: [01-GFM-Impedance, 03-DataCenter-IA]
objetivos: [aportar inercia y amortiguamiento ajustable]
tags: [grid-forming, VSM, inercia, swing, RoCoF]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [droop-control, grid-forming-vs-following, analisis-modal]
referencias:
  - "Zhong, Weiss, Synchronverters: Inverters That Mimic Synchronous Generators, IEEE TIE 2011"
---

## Definición
Estrategia grid-forming que reproduce la **ecuación de swing** de un generador síncrono, dando
al inversor **inercia** virtual \( J \) y **amortiguamiento** \( D \) ajustables por software.

## Fundamento teórico
$$ J\,\dot\omega = \frac{P_{set}-P}{\omega_0} - D\,(\omega-\omega_0), \qquad \dot\delta=\omega-\omega_0 $$
A diferencia del droop (donde \( \omega \) es algebraica e instantánea), aquí \( \omega \) es un
**estado** con inercia: la frecuencia no salta, su tasa de cambio (RoCoF) está limitada por
\( J \). En régimen permanente el VSM reproduce un droop con pendiente \( 1/(\omega_0 D) \).

## Cuándo y por qué se usa
Para aportar **soporte inercial** a la red (frenar el RoCoF ante perturbaciones) y para tener
control directo del amortiguamiento del modo de potencia, que en droop puro es limitado.

## Procedimiento de diseño (genérico)
1. **Inercia** desde la constante \( H \) deseada (s): \( J = 2H S_n/\omega_0^2 \).
   \( H \) típica 2–10 s (como una máquina real).
2. **Amortiguamiento \( D \)** para igualar el droop estacionario deseado:
   \( D = 1/(\omega_0\,m_p) \), o para fijar el \( \zeta \) del modo de potencia.
3. Verifica el par de polos del modo de potencia: \( \omega_n=\sqrt{1/(J\cdot\partial P/\partial\delta/\omega_0)} \).
4. Ajusta \( J,D \) por análisis modal hasta el \( \zeta \) objetivo.

## Ejemplo de código
```python
Jvsm = 2*H*Sn/w0**2
Dvsm = 1/(w0*mp)
domega = ((Pset - Pm)/w0 - Dvsm*(omega - w0)) / Jvsm   # ecuacion de swing
ddelta = omega - w0
```

## Parámetros y valores típicos
\( H \) = 2–10 s (proyecto: 4 s). \( D \) ligado al droop equivalente.

## Errores comunes
- \( J \) grande sin \( D \) suficiente → modo de potencia poco amortiguado y lento.
- Olvidar que en gran señal hace falta limitar corriente igual que en droop (ver
  [[current-limiting]]).

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: inercia): comparado con droop ante un escalón de potencia;
  el VSM (H=4 s) suaviza la frecuencia (RoCoF limitado) frente a la respuesta instantánea del
  droop. En `simulate.py`.

## Conceptos relacionados
- [[droop-control]] · [[grid-forming-vs-following]] · [[analisis-modal]]

## Referencias
- Zhong, Weiss, *Synchronverters*, IEEE TIE 2011.
