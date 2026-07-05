---
titulo: Current limiting (limitación de corriente en grid-forming)
slug: current-limiting
categoria: control
tipo: tecnica
nivel: avanzado
proyectos: [01-GFM-Impedance]
objetivos: [proteger los semiconductores ante faltas]
tags: [falta, saturacion, anti-windup, proteccion, gran-señal, prioridad-reactiva, impedancia-virtual, grid-forming]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-03
relacionados: [control-cascada, impedancia-virtual, vsm-inercia, anti-windup, fault-ride-through]
referencias:
  - "Paquette, Divan, Virtual Impedance Current Limiting for Inverters in Microgrids, IEEE TIA 2015"
  - "He, Li, Virtual Impedance Current Limiting Scheme for GFM Inverters, IEEE TPEL 2021"
  - "Milano, Dörfler et al., Foundations and Challenges of Low-Inertia Systems, PSCC 2018"
---

## Definición
Mecanismo que acota la corriente del inversor ante perturbaciones grandes (faltas). Crítico en
grid-forming porque, al ser **fuente de tensión**, ante un hueco de red inyectaría una corriente
enorme que destruiría los semiconductores. El limitador debe actuar sin romper el carácter
formador ni perder la sincronización con la red.

## Fundamento teórico
La forma más directa: **saturar la magnitud** de la referencia de corriente del lazo interno a
\( I_{max} \), con **anti-windup** para no cargar los integradores del lazo de tensión:

$$ \lVert \mathbf{i}_{L1}^{*}\rVert \le I_{max} \;\Rightarrow\;
   \mathbf{i}_{L1}^{*}\leftarrow I_{max}\,\frac{\mathbf{i}_{L1}^{*}}{\lVert\mathbf{i}_{L1}^{*}\rVert} $$

Es un fenómeno de **gran señal**: rompe la linealidad, por lo que el análisis de impedancia/
estabilidad lineal deja de aplicar y se estudia por simulación temporal.

<div class="cfig"><img src="figuras/current-limiting-falta.png" alt="corriente en falta con y sin limite"><div class="cap">Ante un hueco de red, un grid-forming sin límite inyecta una corriente de falta enorme (≈4.76 pu) que destruiría los semiconductores; la saturación de la magnitud de la referencia la acota a $I_{max}$≈1.5 pu. Es un fenómeno de gran señal: rompe la linealidad y se estudia por simulación temporal.</div></div>

## 1 — El clamping del módulo \( \sqrt{i_d^2+i_q^2} \): por qué por magnitud y no por eje
**Paso 1 — la corriente trifásica como un fasor en dq.** Un sistema trifásico equilibrado de corriente se representa en el marco \( dq \) por dos componentes \( (i_d,i_q) \). Estas no son dos corrientes independientes: son las proyecciones de un único vector cuyo **módulo** es la amplitud de pico de la corriente de fase y cuyo argumento es su fase:

$$ I=\lVert\mathbf{i}\rVert=\sqrt{i_d^2+i_q^2},\qquad \varphi=\arctan\frac{i_q}{i_d} $$

Lo que daña los semiconductores es la **amplitud de pico por fase**, es decir, exactamente este módulo. La restricción física es por tanto \( \sqrt{i_d^{*2}+i_q^{*2}}\le I_{max} \), una circunferencia de radio \( I_{max} \) en el plano \( (d,q) \).

**Paso 2 — proyectar de vuelta sobre el círculo.** Cuando la referencia que pide el lazo de tensión cae fuera del círculo (\( \lVert\mathbf{i}^*\rVert>I_{max} \)), hay que devolverla al borde conservando su dirección (su fase). El punto del círculo más cercano en dirección es el del mismo ángulo: se escala el vector por el factor

$$ s=\frac{I_{max}}{\lVert\mathbf{i}^*\rVert}=\frac{I_{max}}{\sqrt{i_d^{*2}+i_q^{*2}}}\le1 $$

$$ \boxed{\;\mathbf{i}^*\leftarrow s\,\mathbf{i}^*=I_{max}\,\frac{\mathbf{i}^*}{\lVert\mathbf{i}^*\rVert}\;} $$

**Paso 3 — comprobar que preserva la fase.** Tras escalar, \( i_d^*\!\leftarrow\!s\,i_d^* \), \( i_q^*\!\leftarrow\!s\,i_q^* \). El nuevo argumento es \( \arctan\dfrac{s\,i_q^*}{s\,i_d^*}=\arctan\dfrac{i_q^*}{i_d^*}=\varphi \): **idéntico**. El nuevo módulo es \( s\,\lVert\mathbf{i}^*\rVert=I_{max} \). La corriente queda en \( I_{max} \) con la misma fase: misma relación P/Q, solo más pequeña.

**Paso 4 — por qué NO saturar cada eje por separado.** Si se hiciera \( i_d^*\!\leftarrow\!\text{sat}(i_d^*,I_{max}) \) e \( i_q^*\!\leftarrow\!\text{sat}(i_q^*,I_{max}) \) de forma independiente, el límite efectivo sería un **cuadrado** \( [-I_{max},I_{max}]^2 \), no un círculo. Dos problemas: (a) en la esquina la magnitud llega a \( \sqrt2\,I_{max} \), un 41% por encima del límite real; (b) saturar un eje y no el otro **cambia el ángulo** \( \varphi \) (cada eje se recorta en distinta proporción), distorsionando la fase de la corriente —y con ella el reparto P/Q justo en plena falta—. Por eso se satura la magnitud y se reescalan ambos ejes con el mismo \( s \).

**Paso 5 — anti-windup acoplado.** Mientras \( s<1 \), la referencia entregada es menor que la que pide el PI de tensión; su integrador seguiría acumulando error (windup). Por eso, durante la saturación se congelan/recortan los integradores del lazo externo (ver código), de modo que al despejar la falta no haya un sobreimpulso por el término integral cargado.

## 2 — El current limiting circular: el círculo de corriente máxima en el plano id–iq

El espacio de operación del convertidor, desde el punto de vista de la corriente, es el disco de radio \( I_{max} \) en el plano \( (i_d, i_q) \). Cada punto del disco corresponde a una combinación de potencia activa e inductiva reactiva:

$$ P = \frac{3}{2}v_d\,i_d + \frac{3}{2}v_q\,i_q,\qquad Q=-\frac{3}{2}v_d\,i_q+\frac{3}{2}v_q\,i_d $$

(con la orientación estándar \( v_q=0 \), \( P=\frac{3}{2}v_d\,i_d \), \( Q=-\frac{3}{2}v_d\,i_q \)).

La restricción de corriente máxima define una **circunferencia** en ese plano. Cualquier referencia que caiga fuera se proyecta radialmente sobre ella. El operador de proyección es:

$$ \Pi_{I_{max}}(\mathbf{i}^*)=\begin{cases}\mathbf{i}^* & \text{si }\lVert\mathbf{i}^*\rVert\le I_{max}\\ I_{max}\,\dfrac{\mathbf{i}^*}{\lVert\mathbf{i}^*\rVert} & \text{si }\lVert\mathbf{i}^*\rVert>I_{max}\end{cases} $$

Este operador es continuo (no hay salto) y la dirección del vector se conserva: la relación P/Q de la referencia original se mantiene, solo se escala la magnitud.

**El límite como restricción de potencia aparente.** En el punto del círculo, la potencia aparente inyectada es \( S=\frac{3}{2}V_{pcc}\,I_{max} \) (cte.). Dentro del círculo se puede elegir libremente el reparto entre P y Q; en el borde, P y Q están acoplados por \( P^2+Q^2=(SI_{max})^2 \). Aumentar Q durante una falta (para soportar la tensión) reduce la P disponible.

## 3 — La prioridad reactiva durante faltas: iq tiene prioridad sobre id

Durante un hueco de tensión, los códigos de red de muchos países exigen **inyección reactiva prioritaria** (reactive power priority): el convertidor debe sostener la tensión antes que exportar potencia activa. Esto se implementa mediante una estrategia de asignación que da prioridad al eje q (o al eje d en función de la convención de signos adoptada):

**Algoritmo de prioridad reactiva:**

$$ i_q^* = \text{sat}\!\left(i_{q,ref}, I_{max}\right) $$
$$ i_d^* = \text{sat}\!\left(i_{d,ref}, \sqrt{I_{max}^2 - i_q^{*2}}\right) $$

**Paso 1 — determinar el hueco.** A partir de la tensión medida en el PCC: \( \Delta V = 1 - |\mathbf{v}_{pcc}|/V_{n} \). Un hueco de \( \Delta V > 0{,}1\,\text{pu} \) activa el modo de soporte reactivo.

**Paso 2 — calcular iq de soporte.** Los códigos de red (ej. E.ON, ENTSO-E) piden \( \Delta i_q = k\cdot\Delta V \) con \( k\approx 2\,\text{pu/pu} \): por cada 10% de hueco, 20% de corriente reactiva adicional.

**Paso 3 — acotar iq y calcular id residual.** Se satura primero \( i_q^* = \min(i_{q,ref}+\Delta i_q, I_{max}) \) y luego \( i_d^* = \sqrt{\max(0, I_{max}^2 - i_q^{*2})} \). Si el soporte reactivo consume toda la capacidad (\( |i_q^*|=I_{max} \)), la potencia activa cae a cero durante la falta.

**Por qué iq da soporte de tensión.** En una red inductiva, la tensión en el PCC es \( V_{pcc}\approx V_{grid}-X_{red}\,i_q \) (aproximación de la potencia reactiva sobre la impedancia de red): inyectar \( i_q \) (reactiva capacitiva) eleva la tensión local. El convertidor actúa como un STATCOM dinámico durante la falta.

**El plano id-iq durante un hueco.** Antes de la falta: el punto de operación está dentro del círculo, con el ángulo entre id e iq fijado por el despacho P/Q. Durante la falta: la referencia de iq sube (soporte de tensión) y la de id baja hasta que la corriente total toca el borde del círculo. El punto de operación se desplaza sobre el arco hacia el eje q. Al recuperarse la tensión, vuelve al punto nominal.

## 4 — El current limiting en grid-forming: el virtual impedance current limiter

En un convertidor grid-following (GFL) la corriente se controla directamente: el limitador actúa sobre la referencia de corriente del lazo interno, que no puede superar \( I_{max} \). La dinámica es limpia. En un grid-forming (GFM) el convertidor es una **fuente de tensión** (VSC controlado en tensión): no hay lazo de corriente externo que limite la corriente de forma natural. Ante una falta, la diferencia de tensión entre el GFM y la red divide entre la impedancia de salida del conjunto, pudiendo dar corrientes de 5–10 pu.

**La solución: el limitador por impedancia virtual (virtual impedance current limiter).** La idea es aumentar la impedancia de salida del convertidor cuando la corriente supera \( I_{max} \), lo que limita la corriente sin saturar referencias:

$$ \mathbf{v}_{ref} \leftarrow \mathbf{v}_{ref} - Z_{virt}(|\mathbf{i}|)\cdot\mathbf{i} $$

donde \( Z_{virt}(|\mathbf{i}|) \) es una impedancia virtual que se activa o sube cuando \( |\mathbf{i}|>I_{max} \):

$$ Z_{virt}(|\mathbf{i}|) = \begin{cases} 0 & |\mathbf{i}|\le I_{max} \\ R_v + jX_v & |\mathbf{i}|>I_{max} \end{cases} $$

**Derivación del efecto limitador.** Si la red tiene impedancia \( Z_{grid} \) y la tensión de falta es \( V_f \), la corriente sin limitador es:

$$ |\mathbf{i}_{falta}|=\frac{|V_{ref}-V_f|}{|Z_{grid}|} $$

Con el limitador activado, la tensión efetiva de salida del GFM baja a \( \mathbf{v}_{ref} - Z_{virt}\mathbf{i} \), de modo que la corriente satisface:

$$ \mathbf{i}=\frac{\mathbf{v}_{ref} - Z_{virt}\mathbf{i} - V_f}{Z_{grid}} \;\Rightarrow\; \mathbf{i}=\frac{\mathbf{v}_{ref}-V_f}{Z_{grid}+Z_{virt}} $$

Al aumentar \( Z_{virt} \), el denominador crece y la corriente cae. Eligiendo \( X_v = Z_{grid}(I_{max,factor}-1) \) donde \( I_{max,factor}=|\mathbf{i}_{falta}|/I_{max} \) se puede acotar la corriente exactamente a \( I_{max} \).

**Ventaja sobre el saturador de referencia.** El limitador por impedancia virtual no satura un lazo de control: actúa sobre la señal de tensión de referencia del PWM. Esto preserva la dinámica del bucle de control de tensión y del algoritmo de sincronización (VSM/droop), permitiendo que el GFM mantenga su carácter formador durante la falta.

**Transición suave.** En la práctica, \( Z_{virt} \) aumenta suavemente (no en escalón) en función de \( |\mathbf{i}| \):

$$ X_{virt}(|\mathbf{i}|) = k_{virt}\cdot\max(0, |\mathbf{i}|-I_{max}) $$

Esto da una transición gradual que evita discontinuidades en la señal de referencia y reduce el impacto en la sincronización.

## 5 — El anti-windup asociado al current limiter

Cuando el current limiter actúa (el sistema está en saturación, \( |\mathbf{i}^*|=I_{max} \)), los integradores de los PI del lazo de corriente (y del lazo de tensión) continúan acumulando el error si no se toman medidas. Este fenómeno se llama **windup** y provoca un sobreimpulso grande cuando la falta se despeja y el sistema sale de saturación.

**El problema con detalle.** Sea el PI del lazo de corriente eje d: \( u_d = K_p e_d + K_i\int e_d\,dt \). Mientras el limitador actúa, la corriente real es \( I_{max} < i_{d,ref} \): el error \( e_d = i_{d,ref} - i_d > 0 \) es positivo y el integrador sube sin parar. Cuando la falta se despeja y la corriente puede crecer, el integrador ya está cargado con un valor grande que provoca un transitorio de sobreimpulso antes de que la acción integral se "descargue".

**Anti-windup para el limitador circular.** La estrategia de back-calculation es la más adecuada aquí porque la saturación es circular (no rectangular). El anti-windup se implementa con la señal de diferencia entre la referencia limitada y la no limitada:

$$ \dot{x}_{i,d} = e_d + \frac{1}{T_{aw}}\underbrace{(i_{d,lim}^* - i_{d,ref}^*)}_{\text{diferencia saturación}} $$

donde \( T_{aw} \) es la constante de tiempo del anti-windup (típico \( T_{aw}=\sqrt{T_i/K_p} \) para respuesta óptima).

**Congelación del integrador.** Una alternativa más simple es congelar el integrador del lazo de tensión (no el de corriente) mientras \( |\mathbf{i}^*|>I_{max} \):

$$ \dot{x}_{i,v} = \begin{cases} e_v & |\mathbf{i}^*|\le I_{max}\\ 0 & |\mathbf{i}^*|>I_{max} \end{cases} $$

Esto evita que el lazo de tensión acumule error durante la saturación. El lazo de corriente sigue actuando (sus integradores no se congelan), lo que mantiene la corriente exactamente en \( I_{max} \) durante la falta.

**Coordinación PI de tensión–saturador–PI de corriente.** La cadena completa es:
1. PI de tensión calcula \( \mathbf{i}^* \) → se aplica el limitador circular → \( \mathbf{i}^*_{lim} \).
2. Si \( |\mathbf{i}^*|>I_{max} \): activar anti-windup del PI de tensión (congelar o back-calc).
3. PI de corriente recibe \( \mathbf{i}^*_{lim} \) como referencia → sus integradores están activos siempre.
4. Al despejar la falta: el PI de tensión retoma el control desde un estado consistente (sin windup).

<div class="cfig"><img src="figuras/current-limiting-analisis.png" alt="cuatro paneles: circulo dq, prioridad reactiva, impedancia virtual, comparativa GFL vs GFM"><div class="cap">(a) El círculo de corriente máxima en el plano id–iq: la referencia fuera del círculo se proyecta radialmente. (b) Prioridad reactiva: iq aumenta con el hueco y desplaza id hasta el borde del círculo. (c) Limitador por impedancia virtual: Xvirt(|i|) y la corriente resultante vs sin limitador. (d) GFL vs GFM ante cortocircuito: con y sin current limiting.</div></div>

## 6 — Diseño iterativo: current limiting para el GFM del proyecto 01 (imax=1.1 pu)

**Parámetros del proyecto 01 — GFM-Impedance.** Inversor trifásico de 10 kVA, tensión de red 400 V (fase-fase, 50 Hz). Corriente nominal pico \( I_n = 10000/(1{,}5\times400/\sqrt{3}) = 20{,}4\,\text{A} \).

**Elección de Imax.** El estándar IEC 62271 y los IGBT de potencia típicos admiten 2× la corriente nominal durante 10 ms (sobrecorriente de falta). Para ser conservadores y proteger también la inductancia de filtro (que puede saturarse): \( I_{max}=1{,}1\,I_n=1{,}1\times20{,}4=22{,}4\,\text{A} \). (En el proyecto original se usó 1,5 pu; aquí se dimensiona el caso conservador de 1,1 pu.)

**Diseño del limitador circular.** Con \( I_{max}=1{,}1\,I_n \):
- Prioridad reactiva: \( k=2\,\text{pu/pu} \) (normativa ENTSO-E). Un hueco del 10% → \( \Delta i_q=0{,}2\,I_n \).
- Con \( \Delta i_q=0{,}2\,I_n \): \( i_d^{max}=\sqrt{(1{,}1\,I_n)^2-(0{,}2\,I_n)^2}=\sqrt{1{,}21-0{,}04}\,I_n=1{,}082\,I_n \). La potencia activa cae solo un 1,6 %.
- Un hueco del 50%: \( \Delta i_q=1{,}0\,I_n \) → \( i_d^{max}=\sqrt{1{,}21-1{,}0}\,I_n=0{,}458\,I_n \). La potencia activa cae al 41,6% de la nominal.

**Diseño del anti-windup.** Usando back-calculation con \( T_{aw}=\sqrt{T_{i,v}/K_{p,v}} \):
- Lazo de tensión: \( \alpha_v = 2\pi\cdot30 \), \( K_{p,v}=0{,}03\,C_{dc}\,\omega_{dc} \), \( T_{i,v}=10/\alpha_v \approx 53\,\text{ms} \).
- \( T_{aw}=\sqrt{0{,}053/K_{p,v}} \approx 5\,\text{ms} \) (5 veces más rápido que el integrador → buena recuperación).

**Verificación por simulación.** Ante un cortocircuito trifásico al 30% durante 100 ms:
- Sin limitador: corriente pico ≈ 4,76 pu → destruye el IGBT (límite absoluto: 2 pu por 10 ms).
- Con limitador circular (1,1 pu): corriente pico = 1,1 pu → dentro del margen.
- Recuperación post-falta: sin anti-windup → sobreimpulso del 35%; con anti-windup → sobreimpulso < 5%.

## Cuándo y por qué se usa
Siempre en convertidores reales. El reto abierto en grid-forming: limitar **sin** perder el
carácter formador ni la sincronización (un límite duro puede hacer que el inversor "siga" la
falta como GFL y pierda estabilidad de ángulo).

## Procedimiento de diseño (genérico)
1. Fija \( I_{max} \) (típico 1.1–1.5 pu de la corriente nominal de pico).
2. Implementa la saturación de la **magnitud** del fasor de referencia (no por eje).
3. Define la estrategia de prioridad: circular (misma dirección) o reactiva (eje q primero).
4. Añade **anti-windup**: congelación o back-calculation en los integradores del lazo externo.
5. Para GFM: evalúa el limitador por impedancia virtual como alternativa que preserva la dinámica formadora.
6. Verifica en simulación temporal la corriente máxima y la recuperación post-falta.

## Ejemplo de código
```python
mag = np.hypot(iL1ref_d, iL1ref_q)
if mag > Imax:
    s = Imax/mag
    iL1ref_d *= s; iL1ref_q *= s
    dxv_d = dxv_q = 0.0          # anti-windup: congela integradores de tension

# Prioridad reactiva (alternativa)
iq_star = np.clip(iq_ref + k_frt*delta_V*In, -Imax, Imax)
id_max  = np.sqrt(max(0.0, Imax**2 - iq_star**2))
id_star = np.clip(id_ref, -id_max, id_max)

# Virtual impedance current limiter (GFM)
i_mag = np.hypot(id, iq)
X_virt = k_virt * max(0.0, i_mag - Imax)
vd_ref -= -X_virt * iq   # terminos de impedancia virtual inductiva
vq_ref -= X_virt * id
```

## Parámetros y valores típicos
\( I_{max} \) = 1.1–1.5 pu. \( k_{FRT} \) = 2 pu/pu (ENTSO-E). \( T_{aw}\approx\sqrt{T_i/K_p} \).
En el proyecto 01, 1.5 pu (≈30.6 A frente a \( I_n=20.4 \) A).

## Errores comunes
- Saturar por eje en vez de por magnitud → distorsiona la fase de la corriente.
- Olvidar el anti-windup → al salir de la falta hay un transitorio grande (windup).
- Analizar la falta con impedancia lineal → no aplica; usar simulación de gran señal.
- En GFM: usar saturador de referencia de corriente sin considerar la pérdida del carácter formador.

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: protección): ante un hueco al 30%, sin límite la corriente
  llegaba a **4.76 pu**; con el límite quedó en **1.51 pu**. En `simulate.py` / `main_phase5.py`.

## 4 — Limitación de corriente en modo dq

**El límite en el plano dq.** La restricción de corriente máxima sobre el módulo del vector \( (i_d, i_q) \) define una circunferencia en el plano dq:

$$ \sqrt{i_d^2 + i_q^2} \leq I_{max} $$

Todo punto de operación dentro del círculo es seguro; cualquier punto fuera se proyecta radialmente al borde conservando el ángulo (la relación P/Q).

**Prioridad reactiva durante faltas.** Los códigos de red (ENTSO-E, RfG) exigen que durante un hueco de tensión el convertidor sostenga la tensión inyectando corriente reactiva con prioridad sobre la activa. El algoritmo asigna primero \( i_q \) (eje de reactiva) y el \( i_d \) residual ocupa el resto del margen del círculo:

$$ i_q^* = \text{sat}(i_{q,ref} + \Delta i_q,\; I_{max}), \qquad i_d^* = \text{sat}\!\left(i_{d,ref},\; \sqrt{I_{max}^2 - i_q^{*2}}\right) $$

**LVRT (Low Voltage Ride-Through).** Durante el hueco se inyecta corriente reactiva proporcional al hueco de tensión:

$$ \Delta I_q = k_{LVRT}\cdot\Delta V, \qquad \Delta V = 1 - \frac{|V_{pcc}|}{V_n} $$

**Reglamentación europea (RfG).** El Reglamento de la Red de Generación (Commission Regulation EU 2016/631) exige que durante el hueco:

$$ \frac{\Delta I_q}{\Delta V} \geq 2\,\text{pu/pu} $$

Es decir, por cada 10 % de caída de tensión, el convertidor debe inyectar al menos 20 % de corriente reactiva adicional respecto a la nominal. Esto activa el soporte de tensión dinámico equivalente a un STATCOM durante la falta.

## 5 — Anti-windup y saturación en el PI

**El problema del windup.** Sin anti-windup, cuando el limitador activa la saturación (\( |\mathbf{i}^*| = I_{max} \)) el error de los PI del lazo de tensión y del lazo de corriente sigue siendo positivo. El integrador acumula sin límite (windup). Al despejar la falta, la salida del PI arranca con un valor muy alto → sobreimpulso de corriente antes de que el integrador se descargue.

**Back-calculation.** El método más robusto: el término de anti-windup resta a la entrada del integrador la diferencia entre la señal sin saturar y la saturada, escalada por \( K_{AW} = 1/T_t \):

$$ \dot{x}_i = e + K_{AW}(u_{sat} - u_{unsat}) $$

Cuando no hay saturación, \( u_{sat} = u_{unsat} \) y el integrador funciona normalmente. Cuando hay saturación, el término correctivo frena la acumulación.

**Clamping condicional.** Alternativa más simple: congela el integrador cuando la salida está saturada **y** el error tiene el mismo signo que la saturación (es decir, el integrador empeoraría la situación):

$$ \dot{x}_i = \begin{cases} e & \text{si } |u| < u_{max} \text{ o } \text{signo}(e) \neq \text{signo}(u) \\ 0 & \text{en otro caso} \end{cases} $$

**Constante de tiempo del anti-windup.** Ziegler-Nichols recomienda:

$$ T_t \approx \sqrt{T_i\,T_d} $$

Para un PI puro (\( T_d=0 \)), una elección práctica es \( T_t = T_i / 5 \) a \( T_i / 10 \): el anti-windup actúa 5–10 veces más rápido que la dinámica integral del PI.

## 6 — Current limiting en microrredes y VSG

**El VSG ante una falta.** Un VSG (Virtual Synchronous Generator) controla el convertidor como una fuente de tensión con inercia y amortiguamiento virtuales. Cuando se activa el limitador de corriente, el VSG sigue generando referencias de tensión a partir de la dinámica del oscilador virtual, pero la corriente entregada queda limitada a \( I_{max} \). El par electromagnético virtual que "siente" el VSG difiere del par real → puede perder la sincronía (equivalente a una pérdida de paso en una máquina real).

**Solución: modo híbrido GFM↔GFL.** Durante la falta, cuando \( |\mathbf{i}| > I_{max} \), el convertidor conmuta a modo GFL (fuente de corriente controlada) inyectando exactamente \( I_{max} \) con prioridad reactiva. Al recuperarse la tensión, retorna al modo GFM:

$$ \Delta t_{transición} < 5\,\text{ms} $$

La transición suave se implementa interpolando la referencia de tensión del GFM y la referencia de corriente del GFL durante el intervalo de conmutación.

**Impacto en la estabilidad de la microrred.** El limitador introduce una no-linealidad (saturación) en el lazo de control. Esta no-linealidad puede:
- Excitar modos de oscilación inter-área que en el régimen lineal estaban amortiguados.
- Reducir el margen de estabilidad efectivo del lazo de tensión durante la saturación.
- Crear ciclos límite si el anti-windup no está correctamente ajustado.

La herramienta de análisis adecuada para estudiar estos efectos es la **función de descripción** (Describing Function), que extiende el análisis de Nyquist a sistemas con no-linealidades estáticas.

<div class="cfig"><img src="../figuras/current-limiting-analisis.png" alt="cuatro paneles: plano dq con circulo, LVRT reactive boost, anti-windup back-calc, corriente durante hueco"><div class="cap">(a) Plano dq: círculo de corriente máxima y prioridad reactiva. (b) LVRT: corriente reactiva inyectada vs tensión. (c) Anti-windup back-calculation: comparativa con y sin AW. (d) Corriente durante hueco: Id disponible e Iq inyectada.</div></div>

## Conceptos relacionados
- [[control-cascada]] · [[impedancia-virtual]] · [[vsm-inercia]] · [[anti-windup]] · [[fault-ride-through]]

## Referencias
- Paquette, Divan, IEEE TIA 2015.
- He, Li, IEEE TPEL 2021.
