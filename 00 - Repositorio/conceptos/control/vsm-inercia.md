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
fecha_actualizacion: 2026-06-30
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

<div class="cfig"><img src="figuras/vsm-inercia-rocof.png" alt="frecuencia tras escalon de carga: droop vs VSM"><div class="cap">Tras un escalón de carga, el droop puro salta a su nuevo valor de frecuencia de forma instantánea (sin inercia); el VSM la mueve con pendiente acotada (RoCoF $\propto 1/J$): la inercia virtual frena la caída inicial. Ambos asientan en el mismo punto (mismo droop estacionario).</div></div>

## 1 — De la ecuación de swing al RoCoF y la inercia sintética
**Paso 1 — balance de pares en el eje virtual.** El VSM emula la 2ª ley de Newton rotacional de un generador: la inercia \( J \) por la aceleración angular iguala al par neto (par mecánico de entrada menos par eléctrico menos amortiguamiento):
$$ J\,\dot\omega=T_{set}-T_e-D\,(\omega-\omega_0) $$

**Paso 2 — de par a potencia.** Cerca de \( \omega_0 \), par y potencia se relacionan por \( T=P/\omega\approx P/\omega_0 \). Sustituyendo \( T_{set}=P_{set}/\omega_0 \) y \( T_e=P/\omega_0 \):
$$ \boxed{\;J\,\dot\omega=\frac{P_{set}-P}{\omega_0}-D\,(\omega-\omega_0),\qquad \dot\delta=\omega-\omega_0\;} $$
Es la swing equation. A diferencia del droop —donde \( \omega \) es algebraica e instantánea— aquí \( \omega \) es un **estado** integrado: no puede saltar.

**Paso 3 — el RoCoF en el primer instante.** Justo tras un escalón de carga, \( \omega \) aún no se ha movido (\( \omega=\omega_0 \)), así que el término de \( D \) es nulo y la tasa de cambio de frecuencia es
$$ \left.\dot\omega\right|_{t=0^+}=\frac{P_{set}-P}{\omega_0\,J} $$
El RoCoF inicial es **inversamente proporcional a \( J \)**: más inercia virtual → caída de frecuencia más lenta. Esa es la "inercia sintética" — el inversor frena el RoCoF como lo haría la masa rotante de una máquina, pero \( J \) es un parámetro de software.

**Paso 4 — dimensionar \( J \) por la constante de inercia \( H \).** \( H \) es la energía cinética almacenada a \( \omega_0 \) normalizada por la potencia nominal, \( H=\tfrac12 J\omega_0^2/S_n \) (segundos). Despejando:
$$ J=\frac{2H\,S_n}{\omega_0^2} $$
Con \( H=4\,\text{s} \) se emula una máquina de tamaño medio.

## 2 — Por qué en régimen permanente el VSM es un droop \( 1/(\omega_0 D) \)
**Paso 1 — anular la derivada.** En régimen permanente la frecuencia ya no cambia, \( \dot\omega=0 \). La swing se reduce a un balance algebraico:
$$ 0=\frac{P_{set}-P}{\omega_0}-D\,(\omega-\omega_0) $$

**Paso 2 — despejar la frecuencia.** Aislando \( \omega \):
$$ \omega=\omega_0+\frac{1}{\omega_0 D}\,(P_{set}-P) $$

**Paso 3 — comparar con el droop.** Esto es idéntico a la ley de droop \( \omega=\omega_0+m_p(P_{set}-P) \) con pendiente equivalente
$$ \boxed{\;m_{p,eq}=\frac{1}{\omega_0 D}\;\Longleftrightarrow\;D=\frac{1}{\omega_0\,m_p}\;} $$
Conclusión: \( J \) gobierna **solo el transitorio** (RoCoF, inercia) y \( D \) fija el **estatismo estacionario** — el reparto de carga es el mismo que un droop con \( m_p=1/(\omega_0 D) \). Por eso \( D \) se elige para igualar el droop deseado y \( J \) para el soporte inercial, de forma independiente. El par \( (J,D) \) también fija el amortiguamiento del modo de potencia: \( \omega_n=\sqrt{K_s/(J\omega_0)} \) y \( \zeta=\tfrac{D}{2}\sqrt{\omega_0/(J K_s)} \) con \( K_s=\partial P/\partial\delta \), ajustables por [[analisis-modal]].

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
