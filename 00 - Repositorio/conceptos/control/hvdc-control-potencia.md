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

## 7 — Control del terminal offshore (modo GFM)

El terminal offshore de un parque eólico HVDC es el caso más representativo de convertidor
grid-forming en aplicación industrial. Su función es crear la red AC del parque de cero:
sin él, los aerogeneradores no tienen tensión de referencia para sincronizarse.

**Diferencia fundamental con el terminal onshore.** El terminal onshore está conectado a la red de
transmisión pública: tiene una tensión de referencia externa y puede operar como GFL con PLL. El
terminal offshore opera en isla completa — no hay otra fuente de tensión en la red del parque.
Debe fijar \( f \) y \( |V| \) sin ninguna referencia externa.

**Control V/f del terminal offshore.** El convertidor offshore actúa como un oscilador de tensión:

$$v_{AC}^*(t) = V_{nom}\sin(2\pi f_{nom}\,t + \phi_0)$$

La frecuencia \( f_{nom} = 50\,\text{Hz} \) y la amplitud \( V_{nom} \) son constantes fijadas por
el operador. No hay PLL ni lazo de sincronización — el convertidor genera su propio ángulo de referencia.

**Lazo de corriente como protección.** A diferencia del GFM con droop, el terminal offshore no tiene
un lazo de potencia: simplemente mantiene la tensión deseada. El lazo de corriente interno actúa
como limitador ante sobrecargas: si la corriente supera \( I_{max} \), se satura la referencia de
tensión de modulación sin cambiar la frecuencia ni la fase de salida (corriente virtual
limitación). Esto permite que los aerogeneradores arranquen secuencialmente sin colapso de la red.

**Arranque del parque (energización secuencial).** El procedimiento estándar:

1. El convertidor offshore genera la tensión \( V_{nom} \) a 50 Hz vacío (sin carga).
2. Se cierra el interruptor del cable de exportación a 33 kV del primer aerogenerador.
3. La corriente de magnetización del transformador y la capacidad del cable aparece como carga
   del offshore — el lazo de corriente la limita si es necesario.
4. El aerogenerador sincroniza su PLL con la nueva red y arranca su control vectorial.
5. Se repite para cada aerogenerador del parque.

**Regulación de tensión ante variación de carga.** Cuando los aerogeneradores inyectan potencia,
la tensión en el PCC offshore tendería a subir. El convertidor offshore contrarresta esto regulando
la tensión de forma droop o con un lazo PI de amplitud:

$$|V_{PCC}^*| = V_{nom} - k_q\,Q_{inversor}$$

donde \( k_q \) es el coeficiente de droop de reactiva. Alternativamente, se usa un lazo PI que
mide \( |V_{PCC}| \) y ajusta la referencia de corriente reactiva \( i_q^* \).

## 8 — Coordinación entre el terminal offshore y los aerogeneradores

El terminal offshore y los aerogeneradores (WTGs) interactúan a través de la red AC del parque
(33 kV o 66 kV). La coordinación es necesaria para maximizar la energía extraída y proteger el
sistema ante perturbaciones.

**MPPT colectivo vs. individual.** Cada aerogenerador tiene su propio MPPT que maximiza su
extracción de potencia ajustando la velocidad del rotor. El terminal offshore no interviene en
el MPPT individual — simplemente absorbe la potencia total que los WTGs inyectan y la transmite
por el cable DC. La regulación de frecuencia de la red del parque no es para compartir carga
(todos los WTGs van a su MPPT), sino para fijar la referencia de tiempo de los IGBT.

**Rampa de potencia en arranque.** Cuando el parque arranca desde cero o tras un evento, la
potencia total debe subir de forma controlada para no saturar el bus DC ni provocar sobretensión
en el cable:

$$\frac{dP_{parque}}{dt} \leq \dot{P}_{max} \approx 0.1\text{–}0.2\,\text{pu/s}$$

La rampa se implementa en el nivel superior del despacho — no en el lazo de corriente de cada WTG.

**Señal de reducción de potencia (curtailment).** Cuando la tensión DC supera un umbral
(\( V_{dc} > 1.05\,\text{pu} \)), el terminal onshore no puede absorber más potencia. El terminal
offshore detecta la sobretensión DC y envía una señal de reducción de potencia a los WTGs:

$$P_{WTG}^* = P_{MPPT}\,\min\left(1,\; \frac{k_{dc}}{V_{dc}-V_{dc,0}}\right)$$

Esta señal puede transmitirse por la red AC del parque modulando ligeramente la frecuencia
(frequency-based power curtailment): si \( f_{parque} \) sube 0.1–0.2 Hz, los WTGs interpretan
que hay exceso de potencia y reducen su inyección.

**Sincronización de la energización del parque.** En parques con múltiples strings, el terminal
offshore debe gestionar el escalón de corriente de magnetización de cada transformador de string.
La corriente de inrush puede alcanzar 6–10 veces la nominal del transformador en el primer semiciclo.
El offshore limita esta corriente saturando su lazo de corriente interno, con la consiguiente
reducción temporal de la tensión del parque — que los WTGs ya conectados deben tolerar sin
desconectarse por su protección de baja tensión.

## 9 — Protección ante falta AC en el lado offshore

Una falta AC en la red del parque (33 kV o en el cable de export) afecta tanto al terminal
offshore como a los aerogeneradores.

**Perspectiva del terminal offshore.** El terminal ve una carga prácticamente a cero (el
cortocircuito cortocircuita la tensión). El lazo de control intenta mantener \( V_{nom} \) pero la
corriente satura al límite \( I_{max} \). Si la falta persiste, la potencia que llega por el cable
DC supera la que el offshore puede inyectar en la red → \( V_{dc} \) sube. La secuencia de
protección:

1. \( t = 0 \): se detecta la falta (sobrecorriente del lazo de corriente offshore)
2. \( t < 10\,\text{ms} \): el offshore activa el chopper de freno DC para absorber el exceso
3. \( t < 100\,\text{ms} \): el terminal onshore recibe señal (fibra) y reduce \( P_{rec} \)
4. \( t = 100\text{–}300\,\text{ms} \): disparo del interruptor de la red AC del parque si la
   falta es permanente; los WTGs entran en modo FRT

**Perspectiva de los aerogeneradores.** Los WTGs ven una depresión de tensión en sus bornes.
El código de red exige FRT (Fault Ride Through) durante la falta y soporte de reactiva tras la
recuperación. Como la "red" a la que están conectados es el propio terminal offshore, el
comportamiento es diferente al de una falta en red pública:

- La tensión se recupera tan pronto como el offshore puede restablecer \( V_{nom} \) (< 100 ms
  para faltas en la red del parque)
- Los WTGs deben tolerar la reducción de tensión sin desconectarse por un tiempo igual al del
  código FRT de la TSO onshore (típicamente 150–625 ms según el nivel de tensión)

**Falta AC en el lado onshore.** El terminal onshore ve la depresión de tensión de la red pública.
Su respuesta debe ser:

1. Activar el modo LVRT (Low Voltage Ride Through): mantener la conexión y soportar con reactiva
2. Si la capacidad de inyección de potencia cae (porque \( V_{AC} \) baja), el exceso de potencia
   del parque sube \( V_{dc} \): el chopper de freno del terminal offshore se activa automáticamente
3. Tras la recuperación de tensión AC, ramp-up de la potencia activa para evitar nuevos picos

## 10 — Comunicación entre terminales: fibra óptica y latencia

La fibra óptica integrada en el cable DC submarino es la columna vertebral de la comunicación
entre terminales HVDC. Esta comunicación es necesaria para la coordinación pero no para el
control básico de estabilidad (que es local).

**Fibra en el cable HVDC.** Los cables submarinos modernos integran 4–12 fibras ópticas en la
estructura del cable, a un coste marginal mínimo sobre el coste total del cable. La posición
habitual es en el centro del cable, protegida por la armadura metálica.

**Latencia de propagación.** La velocidad de la luz en la fibra monomodo es
\( v_{fibra} \approx 2\times10^5\,\text{km/s} \) (índice de refracción ~1.5). Para 500 km:

$$ \tau_{prop} = \frac{500}{2\times10^5} = 2.5\,\text{ms} $$

Más la latencia del equipamiento de interfaz (serialización, encoding, procesado): total ~5 ms.

**Impacto de la latencia en el control.** Los 5 ms de latencia limitan los lazos de control que
dependen de comunicación entre terminales:

- **Droop DC (local, sin comunicación):** actúa en < 1 ms — no afectado.
- **Reducción de potencia por señal del onshore:** actúa en ~10 ms (5 ms latencia + 5 ms respuesta)
  — suficiente para el chopper de freno que actúa en 1–2 ms.
- **Control secundario (restauración de \( V_{dc} \)):** actúa en 100 ms–1 s — la latencia de 5 ms
  es completamente irrelevante.
- **Control terciario (despacho óptimo):** actúa en 1–30 min — latencia irrelevante.

**Protocolo de comunicación.** Los sistemas HVDC comerciales usan protocolos seriales robustos
(IEC 61850 GOOSE para la protección, IEC 61850-90-3 para la comunicación entre terminales HVDC).
La redundancia de la fibra (2 canales independientes en el mismo cable) asegura la disponibilidad
del sistema de comunicación ante fallos de fibra individual.

**Fallo de la comunicación.** El sistema HVDC debe operar de forma segura cuando la fibra falla.
Con droop DC, el control básico de \( V_{dc} \) funciona sin comunicación. La pérdida de la
comunicación solo afecta al control secundario y al FRT coordinado — ambos pueden implementarse
con estrategias locales de degradación: el offshore mantiene su tensión, el onshore sigue en droop,
y la potencia del parque se reduce por curtailment automático si \( V_{dc} \) supera 1.05 pu.

<div class="cfig"><img src="../figuras/hvdc-control-potencia-analisis.png" alt="Control HVDC-VSC: cascada, Vdc, droop MTDC y FRT"><div class="cap">Estructura de control en cascada (outer/inner loop), respuesta de \( V_{dc} \) ante perturbación de potencia, curvas droop DC de tres terminales MTDC, y evolución de \( V_{dc} \) durante una falta AC con chopper de freno.</div></div>
