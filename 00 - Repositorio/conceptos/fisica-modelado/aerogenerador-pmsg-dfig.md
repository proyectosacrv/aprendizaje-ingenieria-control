---
titulo: Aerogenerador PMSG y DFIG
slug: aerogenerador-pmsg-dfig
categoria: fisica-modelado
tipo: concepto
nivel: avanzado
proyectos: []
objetivos: [entender las dos tecnologías dominantes de aerogenerador de velocidad variable y su control]
tags: [pmsg, dfig, aerogenerador, rotor, estator, control-vectorial, back-to-back, crowbar, frt, offshore]
fecha_creacion: 2026-07-08
fecha_actualizacion: 2026-07-08
relacionados: [eolica-mppt, convertidor-back-to-back, control-vectorial, hvdc-vsc-topologia, fault-ride-through]
referencias:
  - "Ackermann, Wind Power in Power Systems, Wiley 2012"
  - "Hansen et al., Control of Variable Speed Wind Turbines, Wind Energy 2004"
  - "Pena et al., Doubly Fed Induction Generator Using Back-to-Back PWM Converters, IEE Proc. 1996"
---

## Definición
Las dos tecnologías dominantes de aerogenerador de velocidad variable son el **PMSG** (generador síncrono de imanes permanentes, Tipo 4) y el **DFIG** (generador de inducción doblemente alimentado, Tipo 3). El PMSG usa un convertidor back-to-back de potencia total que desacopla completamente el generador de la red; el DFIG alimenta el rotor a través de un convertidor de **potencia parcial** (~30 %) que solo gestiona la potencia de deslizamiento. La elección entre ambos tiene implicaciones directas en el coste del convertidor, la complejidad del FRT y la capacidad de proporcionar servicios de red.

## Fundamento teórico

**Modelo dq del PMSG.** En el marco del rotor, con imanes en el eje d:

$$L_d\frac{di_d}{dt} = v_d - R_s i_d + \omega_r L_q i_q$$

$$L_q\frac{di_q}{dt} = v_q - R_s i_q - \omega_r(L_d i_d + \psi_m)$$

El par electromagnético: \( T_{em} = \tfrac{3}{2}p[\psi_m i_q + (L_d-L_q)i_d i_q] \). Para máquinas no salientes (\( L_d \approx L_q \)): \( T_{em} = \tfrac{3}{2}p\psi_m i_q \) — el par es directamente proporcional a \( i_q \).

**Modelo dq del DFIG.** El estátor conectado directamente a la red y el rotor alimentado por convertidor. En el marco del estátor orientado al flujo estátorico (\( \psi_{sq}=0 \)):

$$P_s \approx -\frac{3}{2}\frac{L_m}{L_s}V_s i_{rq}, \quad Q_s \approx \frac{3}{2}V_s\!\left(\frac{V_s}{\omega_s L_s} - \frac{L_m}{L_s}i_{rd}\right)$$

El desacoplamiento natural: \( i_{rq} \) controla \( P_s \) e \( i_{rd} \) controla \( Q_s \).

**Potencia del rotor en DFIG.** La fracción de potencia que fluye por el convertidor:
\( P_r = s \cdot P_s \), donde \( s = (\omega_s - \omega_r)/\omega_s \) es el deslizamiento. Con \( |s| \leq 0.3 \), el convertidor solo procesa el 30 % de la potencia nominal.

<div class="cfig"><img src="figuras/aerogenerador-pmsg-dfig-analisis.png" alt="PMSG y DFIG: modelos, control y FRT"><div class="cap">Curvas de par-velocidad PMSG con MPPT, reparto de potencia estátor/rotor en DFIG según el deslizamiento, respuesta FRT con activación del crowbar y comparativa de características DFIG vs PMSG.</div></div>

## 1 — Evolución de las tipologías de aerogenerador

Los aerogeneradores han evolucionado desde máquinas de velocidad fija hasta máquinas de velocidad variable que permiten el MPPT y reducen las cargas mecánicas estructurales:

**Tipo 1 — velocidad fija.** Generador de inducción de jaula de ardilla conectado directamente a la red. La velocidad queda fijada por la frecuencia de red y el número de polos. No hay control de velocidad ni de par. El Cp no puede mantenerse en su óptimo ante variaciones de viento: cada desviación de \( \lambda^* \) supone pérdida de energía. Además, las ráfagas se transmiten mecánicamente sin amortiguamiento. Retirado del mercado para nuevas instalaciones desde mediados de los 2000.

**Tipo 2 — velocidad variable limitada (\( \pm10\,\% \)).** Generador de inducción de rotor bobinado con resistencia variable en el rotor controlada por electrónica. Al aumentar la resistencia del rotor, la curva par-velocidad se desplaza y se amplía el rango de deslizamiento. Coste reducido (no hay convertidor de frecuencia completo), pero la energía de deslizamiento se disipa en calor y el rango de velocidad es estrecho. Productos históricos: Vestas OptiSlip.

**Tipo 3 — DFIG.** La solución dominante en onshore hasta 2015. El rotor bobinado se conecta a la red a través de dos VSC back-to-back (RSC y GSC). El RSC controla el par/velocidad del generador; el GSC controla la tensión del bus DC y la potencia reactiva hacia la red. El convertidor procesa solo la potencia del rotor \( P_r = sP_s \); con \( |s| \leq 0.30 \), el rating del convertidor es el 30–35 % de la potencia nominal, lo que reduce significativamente el coste. El rango de velocidad es típicamente 0.70–1.30 de la velocidad sincrónica.

La desventaja principal del DFIG es el **acoplamiento directo del estátor con la red**: un hueco de tensión provoca oscilaciones del flujo estátorico que inducen sobretensiones en el rotor capaces de destruir el convertidor. Esto exige protecciones adicionales (crowbar) para cumplir los requisitos FRT.

**Tipo 4 — full-converter (PMSG o PMSG con transmisión directa).** El generador queda **completamente desacoplado de la red** por el convertidor de potencia total. El MSC (Machine Side Converter) controla el par y la velocidad del generador; el GSC (Grid Side Converter) controla la tensión del bus DC y la potencia reactiva inyectada a la red. El rating del convertidor es el 100 % de la potencia nominal, lo que encarece el sistema eléctrico pero elimina la caja de cambios (en configuración de accionamiento directo) y simplifica el FRT. Es el estándar en offshore moderno: SiemensGamesa SG 14-236 DD, Vestas V236-15.0 MW.

**Tendencia.** El mercado offshore se ha consolidado en el Tipo 4 con PMSG de accionamiento directo. El mayor coste del convertidor queda compensado por la eliminación de la caja de cambios (principal fuente de averías en onshore), el mantenimiento reducido (sin anillos rozantes ni escobillas) y la mayor facilidad para implementar GFM (grid-forming) — capacidad clave para la estabilidad de redes con alta penetración renovable.

## 2 — PMSG: modelo en dq y estrategia de control

El **PMSG** (Permanent Magnet Synchronous Generator) tiene los imanes permanentes en el rotor, lo que elimina la excitación externa y las pérdidas de rotor asociadas. El modelo en dq en el marco del rotor (velocidad eléctrica \( \omega_r = p\,\Omega_m \), con \( p \) pares de polos):

$$\boxed{L_d\frac{di_d}{dt} = v_d - R_s i_d + \omega_r L_q i_q}$$

$$\boxed{L_q\frac{di_q}{dt} = v_q - R_s i_q - \omega_r L_d i_d - \omega_r\psi_m}$$

Los términos \( \omega_r L_q i_q \) y \( \omega_r L_d i_d + \omega_r\psi_m \) son los **acoplamientos cruzados**: aparecen porque el marco dq gira con la máquina, y cada eje "ve" una fem inducida por el flujo del otro eje moviéndose junto con él. El control debe compensarlos explícitamente (desacoplamiento feed-forward, ver más abajo) o el lazo de corriente queda con dos entradas que se interfieren entre sí.

**Par electromagnético — derivación desde el balance de potencia (no solo el resultado).** En vez de partir de la coenergía magnética (que exige cuidado extra con el factor \(3/2\) de la transformación de Park, que no conserva la potencia instantánea), es más directo partir de la potencia eléctrica total en el marco dq y separar qué parte se convierte en trabajo mecánico. La potencia eléctrica instantánea entregada por la fuente a la máquina es:

$$ p_{elec}(t) = \frac{3}{2}\big(v_d i_d + v_q i_q\big) $$

Sustituyendo \(v_d\), \(v_q\) por las ecuaciones de tensión de arriba:

$$ p_{elec} = \frac{3}{2}\Big[\big(R_s i_d + L_d\tfrac{di_d}{dt} - \omega_r L_q i_q\big)i_d + \big(R_s i_q + L_q\tfrac{di_q}{dt} + \omega_r L_d i_d + \omega_r\psi_m\big)i_q\Big] $$

Agrupando por tipo de término:

$$ p_{elec} = \underbrace{\frac{3}{2}R_s(i_d^2+i_q^2)}_{\text{pérdidas resistivas}} \ +\ \underbrace{\frac{3}{2}\Big(L_d i_d\tfrac{di_d}{dt}+L_q i_q\tfrac{di_q}{dt}\Big)}_{\text{variación de energía magnética almacenada}} \ +\ \underbrace{\frac{3}{2}\omega_r\big[\psi_m i_q + (L_d-L_q)i_d i_q\big]}_{\text{potencia convertida a mecánica, }p_{mec}} $$

Los dos primeros términos no producen par (uno se disipa en calor, el otro se acumula/libera en los campos magnéticos sin cruzar el entrehierro); el tercero es exactamente la potencia que atraviesa el entrehierro y se convierte en trabajo mecánico. Como \(p_{mec}=T_{em}\,\Omega_m\) y \(\Omega_m=\omega_r/p\):

$$ T_{em}\,\frac{\omega_r}{p} = \frac{3}{2}\omega_r\big[\psi_m i_q + (L_d-L_q)i_d i_q\big] \quad\Longrightarrow\quad \boxed{\ T_{em} = \frac{3}{2}p\big[\psi_m i_q + (L_d-L_q)i_d i_q\big]\ } $$

el factor \(\omega_r\) se cancela en ambos lados — el par no depende de la velocidad, solo de las corrientes, como debe ser en una máquina eléctrica ideal. El primer término \( \psi_m i_q \) es el **par de excitación** (por interacción del flujo de los imanes con \(i_q\)); el segundo \( (L_d-L_q)i_d i_q \) es el **par de reluctancia** (por la diferencia de reluctancia magnética entre ejes, solo existe si \(L_d\neq L_q\)).

**MTPA (Maximum Torque Per Ampere): dónde está el óptimo, y por qué \(i_d=0\) no siempre lo es.** El objetivo de MTPA es, para un módulo de corriente disponible \(|I_s|=\sqrt{i_d^2+i_q^2}\) fijado por el límite térmico del convertidor, encontrar el reparto \((i_d,i_q)\) que maximiza \(T_{em}\).

*Caso no saliente (\(L_d=L_q\), típico de imanes en superficie).* El término de reluctancia se anula idénticamente:

$$ T_{em} = \frac{3}{2}p\,\psi_m\,i_q $$

El par ya no depende de \(i_d\) en absoluto — solo "gasta" módulo de corriente sin aportar par. El óptimo es entonces trivial: **\(i_d=0\)**, todo el módulo disponible se destina a \(i_q\). De aquí:

- La referencia de corriente de cuadratura viene del MPPT: \( i_q^* = T_{ref}/(1.5\,p\,\psi_m) \)
- La referencia de par del MPPT: \( T_{ref} = k_{opt}\,\omega_r^2 \)

*Caso saliente (\(L_d\neq L_q\), típico de PMSG de imanes interiores, IPM).* Ahora el término de reluctancia sí depende de \(i_d\), y **puede sumar par adicional** si tiene el signo correcto. Con \(i_q=\sqrt{I_s^2-i_d^2}\) (módulo fijo) y \(L_q>L_d\) (el caso IPM habitual, porque el hueco de aire equivalente es mayor en el eje d por los imanes), el par crece al hacer \(i_d<0\): el término \((L_d-L_q)i_d i_q\) se vuelve positivo (producto de dos negativos por \(L_d-L_q<0\)), sumándose al par de excitación. El máximo real ya no está en \(i_d=0\) sino desplazado hacia \(i_d<0\) — ver panel (a) de la figura: para el ejemplo con \(L_q/L_d=1.3\), el par máximo alcanzable es más del doble que en \(i_d=0\) con el mismo módulo de corriente.

<div class="cfig"><img src="figuras/pmsg-mtpa.png" alt="grafica del par electromagnetico en funcion de id a modulo de corriente constante, comparando maquina no saliente con maximo en id=0 frente a maquina saliente IPM con maximo en id negativo por el par de reluctancia adicional; y diagrama de bloques del lazo de corriente del MSC mostrando los dos PI de eje d y q con la suma/resta del termino de desacoplo feedforward antes de la referencia de tension"><div class="cap">(a) \(T_{em}(i_d)\) a módulo de corriente \(|I_s|\) constante: en la máquina no saliente (\(L_d=L_q\), azul) el máximo está exactamente en \(i_d=0\); en la máquina saliente IPM (\(L_q>L_d\), roja) el par de reluctancia adicional desplaza el óptimo a \(i_d<0\), con un par máximo notablemente mayor para el mismo módulo de corriente. (b) Lazo de corriente del MSC: cada eje tiene su PI, y antes de la referencia de tensión final se suma/resta el término de desacoplo feedforward correspondiente, calculado en tiempo real a partir de \(\omega_r\), \(i_d\), \(i_q\) medidos.</div></div>

Por eso la ficha, al asumir \(L_d=L_q\) para el ejemplo numérico de 6 MW, usa correctamente \(i_d^*=0\) — pero conviene tener presente que esa simplificación es válida solo para PMSG de imanes en superficie, no en general.

**Por qué hace falta el desacoplo feedforward, y cómo se implementa.** Sin compensar, cada lazo PI de corriente (eje d, eje q) ve la salida del otro eje como una perturbación no modelada: mover \(i_q\) cambia instantáneamente el término \(\omega_r L_q i_q\) que aparece en la ecuación de \(i_d\) (y viceversa), lo que el PI de \(i_d\) percibe como una perturbación externa y corrige con retraso — degradando la respuesta dinámica del lazo, especialmente a alta velocidad (\(\omega_r\) grande amplifica el acoplamiento). La solución estándar es calcular explícitamente esos términos con los valores medidos de \(i_d\), \(i_q\), \(\omega_r\) y sumarlos/restarlos a la salida del PI antes de aplicar la tensión:

$$ v_q^* = \underbrace{K_{p,q}(i_q^*-i_q)+K_{i,q}\!\int(i_q^*-i_q)\,dt}_{\text{salida del PI de eje q}} \ +\ \underbrace{\omega_r(L_d i_d+\psi_m)}_{\text{desacoplo feedforward}} $$

$$ v_d^* = \underbrace{K_{p,d}(i_d^*-i_d)+K_{i,d}\!\int(i_d^*-i_d)\,dt}_{\text{salida del PI de eje d}} \ -\ \underbrace{\omega_r L_q i_q}_{\text{desacoplo feedforward}} $$

Con esta compensación, cada PI ve una planta de primer orden desacoplada y pura (\(L\,di/dt=v_{PI}\)), sin el término cruzado — el diseño del PI se hace exactamente igual que para dos ejes independientes, y el acoplamiento físico real queda cancelado en tiempo real por el término feedforward, como se ve en el panel (b) de la figura.

**Control del MSC (Machine Side Converter).** Lazo interno PI de corriente en dq con compensación de acoplamientos cruzados (arriba). Lazo externo de velocidad (o par directo sin lazo de velocidad en configuraciones de MPPT directo). Ancho de banda típico del lazo de corriente: 500–1500 rad/s; lazo de velocidad: 20–50 rad/s.

**Control del GSC (Grid Side Converter).** Lazo de control de tensión del bus DC (referencia fija, por ejemplo 1150 V para un convertidor de 690 V) y lazo de potencia reactiva. En modo GFL, el GSC usa PLL para sincronizarse con la red. En modo GFM (grid-forming), el GSC usa droop de tensión/frecuencia o PSC (Power Synchronization Control) — posible solo con el Tipo 4, ya que el bus DC proporciona el desacoplamiento necesario.

**Lógica de potencia de la máquina.** La dinámica mecánica del aerogenerador:

$$J\frac{d\omega_r}{dt} = T_{aero} - T_{em} - B\omega_r$$

donde \( J \) es la inercia total, \( B \) el rozamiento viscoso. En MPPT, \( T_{em} = k_{opt}\omega_r^2 \) y el sistema se asienta en el punto de operación donde \( T_{aero}(\omega_r, v_w) = T_{em}(\omega_r) \), que coincide con \( \lambda = \lambda^* \).

## 3 — DFIG: modelo en dq y control orientado al flujo

El **DFIG** (Doubly Fed Induction Generator) tiene el estátor conectado directamente a la red (tensión y frecuencia impuestas) y el rotor conectado al RSC (Rotor Side Converter) a través de anillos rozantes. Las ecuaciones de tensión del estátor y del rotor en el marco de referencia sincrónico (\( \omega_s = 2\pi f_s \)):

**Estátor (marco sincrónico, velocidad \( \omega_s \)):**
$$v_{sd} = R_s i_{sd} + \frac{d\psi_{sd}}{dt} - \omega_s \psi_{sq}$$
$$v_{sq} = R_s i_{sq} + \frac{d\psi_{sq}}{dt} + \omega_s \psi_{sd}$$

**Rotor (marco sincrónico, frecuencia de deslizamiento \( s\omega_s \)):**
$$v_{rd} = R_r i_{rd} + \frac{d\psi_{rd}}{dt} - s\omega_s \psi_{rq}$$
$$v_{rq} = R_r i_{rq} + \frac{d\psi_{rq}}{dt} + s\omega_s \psi_{rd}$$

**Flujos de enlace** (\( L_m \) inductancia magnetizante, \( L_s = L_{ls} + L_m \), \( L_r = L_{lr} + L_m \)):
$$\psi_{sd} = L_s i_{sd} + L_m i_{rd}, \quad \psi_{sq} = L_s i_{sq} + L_m i_{rq}$$
$$\psi_{rd} = L_r i_{rd} + L_m i_{sd}, \quad \psi_{rq} = L_r i_{rq} + L_m i_{sq}$$

**Control vectorial orientado al flujo del estátor.** Se elige el eje d alineado con el vector de flujo del estátor: \( \psi_{sd} = |\psi_s| \), \( \psi_{sq} = 0 \). Bajo esta orientación, y despreciando \( R_s \) (válido para máquinas grandes):

$$V_s \approx \omega_s\psi_{sd} = \omega_s|\psi_s| \quad \Rightarrow \quad |\psi_s| \approx \frac{V_s}{\omega_s} = \text{constante}$$

Expresando las potencias activa y reactiva del estátor en función de las corrientes de rotor:

$$P_s = -\frac{3}{2}\frac{L_m}{L_s}V_s i_{rq}$$

$$Q_s = \frac{3}{2}V_s\!\left(\frac{V_s}{\omega_s L_s} - \frac{L_m}{L_s}i_{rd}\right)$$

**Resultado de control:** \( i_{rq} \) controla directamente \( P_s \) (y por tanto el par y la velocidad) e \( i_{rd} \) controla directamente \( Q_s \). El RSC implementa dos lazos PI internos de corriente de rotor más los lazos externos de par (o velocidad) y potencia reactiva.

**Reparto de potencia.** La potencia del rotor inyectada por el convertidor:
$$P_r = s\,P_s = \frac{\omega_s - \omega_r}{\omega_s}P_s$$

- Para \( \omega_r < \omega_s \) (subsíncrono, \( s > 0 \)): el convertidor inyecta potencia en el rotor (RSC consume de la red a través del GSC)
- Para \( \omega_r > \omega_s \) (supersíncrono, \( s < 0 \)): el convertidor extrae potencia del rotor hacia la red
- La potencia total a la red: \( P_{red} = P_s + P_{GSC} = P_s(1-s) \approx P_s \) (despreciando pérdidas)

Este balance explica por qué el convertidor DFIG solo necesita un rating de ~30–35 % de la potencia nominal: en todo momento, solo gestiona la **potencia de deslizamiento** \( |s|P_s \leq 0.30\,P_s \).

## 4 — FRT (Fault Ride-Through) en DFIG y PMSG

Los requisitos de FRT (Grid Code RfG, ENTSO-E) obligan a los aerogeneradores a permanecer conectados durante huecos de tensión y a aportar corriente reactiva durante el hueco:

$$\Delta I_q \geq 2\,\Delta V \quad \text{(corriente reactiva en pu por caída de tensión en pu)}$$

El aerogenerador debe mantenerse conectado para \( V > 0.20\,\text{pu} \) durante al menos 140 ms, y hasta \( V > 0.85\,\text{pu} \) durante 1.5 s.

**FRT del DFIG — el problema del flujo.** Cuando se produce un hueco de tensión en la red, la tensión del estátor cae de forma abrupta. El flujo estátorico no puede cambiar instantáneamente (es un estado del sistema), por lo que surge un **componente de flujo natural** (DC) que oscila a la frecuencia del estátor \( \omega_s \) y decae con la constante \( \tau_s = L_s/R_s \). Este flujo oscilante induce en el rotor, que gira a \( \omega_r \), tensiones a la frecuencia \( (\omega_s - \omega_r) + \omega_s = (2-s)\omega_s \approx 2\omega_s \). Las tensiones de rotor inducidas pueden superar varias veces la tensión nominal del convertidor del rotor, poniendo en riesgo los IGBTs.

**Crowbar del DFIG.** La protección estándar es el **crowbar**: un conjunto de resistencias que se conectan en cortocircuito al circuito del rotor cuando la corriente supera un umbral. Durante la activación del crowbar:

1. El RSC se bloquea (sus IGBTs se desactivan)
2. La corriente de rotor circula por las resistencias del crowbar, limitando la sobretensión
3. El DFIG se comporta como un generador de inducción de jaula de ardilla: no puede controlar \( P \) ni \( Q \)
4. El GSC permanece activo y puede inyectar corriente reactiva desde el bus DC

Tiempo típico de activación del crowbar: 20–80 ms. Después, el crowbar se desconecta y el RSC retoma el control.

**FRT del PMSG — bus DC como amortiguador.** El PMSG tiene una ventaja fundamental: el bus DC desacopla el generador de la red. El proceso durante un hueco:

1. La tensión de la red cae → la potencia que el GSC puede inyectar disminuye (\( P_{out} \propto V_{red} \))
2. La potencia que el MSC transfiere al bus DC sigue siendo la potencia del generador \( P_{gen} \)
3. El bus DC empieza a subir porque \( P_{in} > P_{out} \)
4. El **chopper de freno** (braking resistor en paralelo con el bus DC) se activa cuando \( V_{dc} > V_{dc,max} \), disipando el exceso de potencia
5. Simultáneamente, el MSC reduce la referencia de par \( T_{ref} \) para desacelerar el generador y reducir \( P_{gen} \)
6. El GSC inyecta la máxima corriente reactiva permitida por su límite de corriente \( I_{max} \)

No hay crowbar ni pérdida de control durante el hueco. La FRT del PMSG es más sencilla y robusta.

**Comparativa cuantitativa de FRT.** Para un hueco al 15 % de la tensión nominal (\( \Delta V = 0.85\,\text{pu} \)):

- Corriente reactiva requerida: \( \Delta I_q = 2 \times 0.85 = 1.70\,\text{pu} \) (limitado a \( I_{max} \approx 1.10\,\text{pu} \) en la práctica)
- Corriente activa durante el hueco: \( I_d = \sqrt{I_{max}^2 - I_q^2} = \sqrt{1.10^2 - 1.10^2} \approx 0 \) — prácticamente toda la capacidad del convertidor se dedica a la reactiva
- Para el DFIG, durante la activación del crowbar: \( I_q \approx 0 \) (GSC limitado al 30 % de \( P_{nom} \))

## 5 — Comparativa DFIG vs PMSG

| Característica | DFIG (Tipo 3) | PMSG (Tipo 4) |
|---|---|---|
| Potencia del convertidor | ~30 % \( P_{nom} \) | 100 % \( P_{nom} \) |
| Coste relativo del convertidor | Menor | Mayor (~2×) |
| Caja de cambios | Normalmente sí (ratio ~1:100) | No (accionamiento directo) |
| FRT | Complejo (crowbar, pérdida temporal de control) | Simple (chopper, control continuo) |
| Desacoplamiento de la red | No (estátor directo) | Completo (bus DC) |
| SCR mínimo de operación | ~2 (PLL del GSC) | 0 en modo GFM |
| Capacidad de potencia reactiva | Limitada a rating del convertidor (30 %) | Hasta \( I_{max} \) (100 %) |
| Grid-forming | No nativo | Posible (PSC, droop, VSM) |
| Anillos rozantes y escobillas | Sí | No |
| Mantenimiento offshore | Complejo | Simplificado |
| Inercia de la nacelle | ~300–350 t (con caja) | ~350–400 t (sin caja, mayor generador) |
| Estándar offshore actual | Minoritario | Dominante (SG 14-236, V236-15) |

**Por qué PMSG gana en offshore.** En offshore, los costes de operación y mantenimiento (O&M) son 3–5× los de onshore. La caja de cambios es el componente con mayor tasa de fallos en aerogeneradores (especialmente en offshore); eliminarla reduce drásticamente los eventos de O&M. Además, la conexión mediante HVDC requiere que el convertidor AC onshore del HVDC pueda operar en modo GFM — el PMSG con full-converter lo facilita, mientras el DFIG con su estátor directo a la red AC del parque crea dependencias de SCR.

## 6 — Dimensionado y parámetros típicos

**Número de polos de un PMSG de accionamiento directo.** La velocidad de giro del rotor de una turbina de 10 MW es típicamente 8–12 rpm. Para generar a 50 Hz:

$$p = \frac{2 \times 60 \times f}{n\,[\text{rpm}]} = \frac{2 \times 60 \times 50}{10} = 600 \text{ polos (300 pares de polos)}$$

Un generador de 600 polos tiene un diámetro de aire muy grande (10–15 m) pero elimina la caja de cambios.

**Ejemplo: PMSG de 6 MW offshore.**

| Parámetro | Símbolo | Valor típico |
|---|---|---|
| Potencia nominal | \( P_{nom} \) | 6 MW |
| Tensión de estátor | \( V_s \) | 690 V (a trafo del convertidor) |
| Velocidad nominal de giro | \( n \) | 12 rpm |
| Pares de polos | \( p \) | 250 |
| Flujo de imanes | \( \psi_m \) | 1.5 Wb |
| Inductancia eje d/q | \( L_d = L_q \) | 2 mH |
| Resistencia de estátor | \( R_s \) | 10 mΩ |
| Inercia total | \( J \) | \( 1.5 \times 10^7 \,\text{kg·m}^2 \) |
| Constante de inercia | \( H \) | 5.5 s |
| Par nominal | \( T_{nom} \) | \( P_{nom}/\Omega_m = 4.77 \,\text{MN·m} \) |
| \( k_{opt} \) (MPPT) | — | \( T_{nom}/\omega_{r,nom}^2 \) |

**Cálculo de \( k_{opt} \).** La velocidad angular eléctrica nominal: \( \omega_{r,nom} = p\,\Omega_m = 250 \times (12\,\text{rpm} \times 2\pi/60) = 314 \,\text{rad/s}\) (coincide con \( \omega_s \) — máquina síncrona a velocidad nominal). El \( k_{opt} \) en el eje del generador (eléctrico):

$$k_{opt} = \frac{T_{nom}}{\omega_{r,nom}^2} = \frac{4.77\times10^6}{314^2} = 48.3\,\text{N·m·s}^2/\text{rad}^2$$

**Ejemplo: DFIG de 2 MW onshore.**

| Parámetro | Símbolo | Valor típico |
|---|---|---|
| Potencia nominal | \( P_{nom} \) | 2 MW |
| Tensión de estátor | \( V_s \) | 690 V |
| Ratio de la caja de cambios | — | 1:100 |
| Velocidad del rotor (alta velocidad) | \( \omega_r \) | 1000–1700 rpm |
| Deslizamiento máximo | \( |s_{max}| \) | 0.30 |
| Rating del convertidor | — | 600 kW (30 % de 2 MW) |
| Inductancia magnetizante | \( L_m \) | 2.5 mH |
| Inductancia propia de rotor | \( L_r \) | 2.58 mH |
| Inductancia propia de estátor | \( L_s \) | 2.58 mH |
| Resistencia de rotor | \( R_r \) | 2.6 mΩ |

**Diseño del crowbar.** La resistencia del crowbar se dimensiona para limitar la corriente de rotor durante el hueco:

$$R_{crow} \geq \frac{V_{r,max}}{I_{r,max}} - R_r$$

Con \( V_{r,max} \approx 2V_{r,nom} \) y \( I_{r,max} \approx 2I_{r,nom} \), una resistencia típica es \( R_{crow} \approx 0.1\,\text{pu} \).
