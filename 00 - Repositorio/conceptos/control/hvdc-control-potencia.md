---
titulo: Control de potencia del HVDC-VSC
slug: hvdc-control-potencia
categoria: control
tipo: concepto
nivel: avanzado
proyectos: []
objetivos: [diseñar la jerarquía de control de un VSC-HVDC, entender el droop DC en MTDC y el FRT]
tags: [hvdc, control-potencia, control-tension-dc, outer-loop, inner-loop, droop-dc, mtdc]
fecha_creacion: 2026-07-05
fecha_actualizacion: 2026-07-05
relacionados: [convertidor-back-to-back, topologias-multinivel, filtro-lcl, fenomenos-oscilatorios-red]
referencias:
  - "Cigré TB 604, Guide for the Development of Models for HVDC Converters"
  - "Lesnicar & Marquardt, An Innovative Modular Multilevel Converter Topology"
---

## 1 — Estructura de control del VSC-HVDC

El control del VSC-HVDC tiene la misma arquitectura en cascada que cualquier convertidor de fuente
de tensión, organizada en tres capas con anchos de banda claramente separados:

- **Lazo interno (inner loop):** control de corriente en el marco dq síncrono. Igual que en el
  [[control-vectorial|GFL clásico]]; ancho de banda ~1 kHz. Genera la referencia de tensión de
  modulación para cada fase del MMC.
- **Lazo externo (outer loop):** controla las magnitudes físicas de interés — \( P \), \( Q \),
  \( V_{dc} \) o \( V_{ac} \) — según el modo de operación del terminal; ancho de banda ~50 Hz.
  Genera las referencias de corriente \( i_d^* \) e \( i_q^* \) para el lazo interno.
- **Capa superior:** despacho de potencia, droop DC para MTDC, limitación de rampa de potencia,
  coordinación entre terminales. Tiempos de respuesta de cientos de ms a segundos.

La separación de escalas temporal entre capas garantiza que cada lazo puede diseñarse de forma
independiente, como en cualquier control en cascada ([[arquitecturas-control]]).

**Asignación de modos por terminal.** El reparto típico en un enlace punto a punto es:

- Terminal **rectificador** (onshore o generación): controla \( V_{dc} \) — fija la tensión del
  enlace DC y absorbe o inyecta la diferencia entre potencia generada y consumida.
- Terminal **inversor** (red receptora): controla \( P \) — inyecta la potencia deseada según el
  despacho. El lazo de \( V_{dc} \) no actúa.

En un parque eólico offshore, el esquema es distinto: el terminal **offshore** controla \( V_{ac} \)
de la red interna del parque (modo GFM, grid-forming), y el terminal **onshore** controla \( V_{dc} \).
El terminal offshore no tiene PLL — forma la tensión de referencia sin necesidad de sincronización
externa, lo que lo convierte en un formador de red para los aerogeneradores.

## 2 — Lazo de control de tensión DC

El bus DC del enlace HVDC tiene una dinámica integradora. La energía almacenada en los condensadores
del cable y del MMC es proporcional a \( V_{dc}^2 \):

$$W_{dc} = \frac{1}{2}C_{eq}V_{dc}^2$$

**Paso 1 — balance de potencia.** La derivada de la energía iguala la diferencia entre potencia
rectificada y potencia invertida (más pérdidas):

$$\frac{dW_{dc}}{dt} = P_{rec} - P_{inv} - P_{loss}$$

**Paso 2 — linealización en \( V_{dc}^2 \).** Definiendo \( w = V_{dc}^2 \):

$$\frac{dw}{dt} = \frac{2}{C_{eq}}(P_{rec} - P_{inv} - P_{loss})$$

La planta es un integrador puro en \( w \). Esto es análogo al bus DC del [[convertidor-back-to-back]],
con la diferencia de que aquí \( C_{eq} \) incluye la capacidad distribuida del cable (decenas de µF).

**Paso 3 — diseño del lazo PI.** El controlador PI actúa sobre el error \( w^* - w = V_{dc}^{*2} - V_{dc}^2 \):

$$P_{ref} = K_p(V_{dc}^{*2} - V_{dc}^2) + K_i\int(V_{dc}^{*2} - V_{dc}^2)\,dt$$

La referencia de corriente se obtiene dividiendo por \( 1.5\,V_d \) (potencia en dq):
\( i_d^* = P_{ref}/(1.5\,V_d) \).

**Paso 4 — ancho de banda.** Con planta integradora \( G(s) = 2/(C_{eq}\,s) \) y PI \( C(s) = K_p + K_i/s \),
la función de lazo es de segundo orden. Para un amortiguamiento de 0.7 y \( \omega_n = 2\pi\times 10\,\text{Hz} \):

$$K_p = \frac{C_{eq}\,\omega_n^2}{2\,K_i/K_p}, \qquad K_i = \frac{K_p\,\omega_n}{\sqrt{2}}$$

## 3 — Control de potencia activa y reactiva

**Control de P directo.** El terminal inversor recibe una referencia \( P^* \) del despacho externo.
La corriente de referencia en el eje d es:

$$i_d^* = \frac{P^*}{1.5\,V_d}$$

donde \( V_d \) es la componente directa de la tensión en el PCC (punto de conexión común), que en
orientación de campo de tensión (\( V_q \approx 0 \)) es igual a la amplitud de la tensión de red.

**Control de Q.** La potencia reactiva en dq (con \( V_q \approx 0 \)):

$$Q \approx -\frac{3}{2}V_d i_q$$

La referencia de corriente reactiva:

$$i_q^* = -\frac{Q^*}{1.5\,V_d}$$

El signo negativo es convencional (generador de reactiva positiva → corriente \( i_q \) negativa con
orientación de campo de tensión estándar). El eje q es independiente del eje d gracias al
[[desacoplo-dq|desacoplamiento cruzado]].

**Modo \( V_{ac} \)-control.** Un lazo PI externo regula la amplitud de tensión \( |V_{PCC}| \):

$$i_q^* = K_{p,V}(V_{ac}^* - |V_{PCC}|) + K_{i,V}\int(V_{ac}^* - |V_{PCC}|)\,dt$$

Este modo es esencial en redes débiles (SCR < 3) donde la tensión del PCC es sensible al flujo de
reactiva ([[interaccion-pll-red-debil]]), y en el terminal offshore de parques eólicos donde el VSC
forma la red local.

## 4 — Droop de tensión DC para MTDC

En un sistema MTDC con \( N \) terminales, si un solo terminal controla \( V_{dc} \), su fallo colapsa
toda la red DC en milisegundos. La solución es el **droop de tensión DC** (Vdc-droop):

$$P_i = P_{0,i} + k_{d,i}(V_{dc} - V_{dc,0})$$

donde \( P_{0,i} \) es el punto de operación nominal del terminal \( i \), \( k_{d,i} \) su ganancia
de droop (en MW/kV o en pu/pu) y \( V_{dc,0} \) la tensión nominal del bus DC.

**Interpretación.** Cuando la tensión DC sube (exceso de potencia en la red DC), todos los terminales
con droop reducen su inyección (o aumentan su absorción) proporcionalmente a su \( k_{d,i} \). El
equilibrio se alcanza en una tensión ligeramente diferente de \( V_{dc,0} \):

$$\Delta V_{dc} = \frac{\Delta P_{total}}{\sum_i k_{d,i}}$$

Este es el mismo principio que el droop de frecuencia en redes AC ([[ecuacion-oscilacion|droop de
frecuencia en generadores síncronos]]), trasladado al bus DC.

**Ventajas del droop frente al control maestro-esclavo:**

- Sin comunicación entre terminales — acción local e instantánea (< 1 ms)
- Redundancia: si un terminal falla, los demás absorben el desequilibrio automáticamente
- Ajuste de prioridades: mayor \( k_{d,i} \) → mayor participación en el control de \( V_{dc} \)
- Compatible con el despacho económico: se puede ajustar \( P_{0,i} \) desde el nivel superior

**Ajuste de \( k_d \).** Un droop más alto da mejor regulación de \( V_{dc} \) pero más variación
de \( P \) ante perturbaciones. El compromiso estándar:

$$k_d = \frac{\Delta P_{max}}{\Delta V_{dc,max}} \approx \frac{0.1\,P_{nom}}{0.05\,V_{dc,nom}}$$

## 5 — Limitación de corriente y FRT en HVDC

Durante una falta AC en el terminal inversor, la potencia que ese terminal puede evacuar cae
bruscamente. Si el terminal rectificador sigue inyectando potencia al bus DC, \( V_{dc} \) sube:

$$C_{eq}\frac{dV_{dc}}{dt} = \frac{P_{rec} - P_{inv}}{V_{dc}}$$

La sobretensión DC puede disparar las protecciones del MMC (típicamente \( V_{dc} > 1.2\,\text{pu} \)).

**Chopper de freno (braking resistor).** Resistencia conectada al bus DC a través de un IGBT.
Cuando \( V_{dc} > V_{dc,lim} \), el chopper se activa y absorbe el exceso de potencia:

$$P_{chopper} = \frac{V_{dc}^2}{R_{br}} \cdot d_{chopper}$$

donde \( d_{chopper} \) es el ciclo de trabajo del IGBT del chopper (0–1). Es la solución más rápida
y eficaz para proteger el bus DC durante faltas AC.

**Reducción de \( P_{rec} \).** Si existe un enlace de fibra óptica entre terminales (latencia ~5 ms),
el terminal rectificador puede reducir su potencia al recibir la señal de falta. Limitado por la
latencia y la complejidad del sistema de comunicación.

**FB-SM — bloqueo de falta DC.** Los submódulos de puente completo pueden polarizarse inversamente
para bloquear una falta DC, actuando como disyuntor distribuido. Elimina la necesidad del DCCB
(DC circuit breaker) pero añade pérdidas y coste.

## 6 — Modos de operación y transición entre modos

El VSC-HVDC debe poder transitar entre modos de forma suave (bumpless transfer). La tabla resume
los modos típicos:

| Terminal | Modo normal | Falta AC local | Falta AC remota |
|---|---|---|---|
| Rectificador (onshore) | \( V_{dc} \)-control | Reducción P, LVRT | LVRT + Q-support |
| Inversor offshore (parque) | \( V_{ac} \)-control (GFM) | Mantiene \( V_{ac} \) parque | Reducción P + chopper |
| Inversor onshore (carga) | P-control | LVRT + Q-support | P-control normal |

**Transición bumpless.** Cuando se cambia de modo (p. ej. de P-control a \( V_{dc} \)-control tras
la pérdida del terminal rectificador), el integrador del nuevo lazo debe precargarse con el valor
actual de la variable de control. De lo contrario, el salto de la referencia del integrador produce
un transitorio de corriente que puede disparar la limitación:

$$\text{Antes del cambio de modo:} \quad \int_{\,nuevo}(t_0^-) = i_{d,actual}(t_0^-)$$

Esta precarga (preloading o bumpless transfer) es imprescindible en convertidores reales y se
implementa en la lógica de conmutación del controlador de estado superior.

<div class="cfig"><img src="../figuras/hvdc-control-potencia-analisis.png" alt="Control HVDC-VSC: cascada, Vdc, droop MTDC y FRT"><div class="cap">Estructura de control en cascada (outer/inner loop), respuesta de \( V_{dc} \) ante perturbación de potencia, curvas droop DC de tres terminales MTDC, y evolución de \( V_{dc} \) durante una falta AC con chopper de freno.</div></div>
