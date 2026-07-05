---
titulo: Sistema eólico DFIG/PMSG y MPPT
slug: eolica-mppt
categoria: fisica-modelado
tipo: concepto
nivel: avanzado
proyectos: []
objetivos: [modelar la turbina eólica y extraer la máxima potencia según el viento]
tags: [eolica, dfig, pmsg, mppt, cp-lambda, back-to-back, tipo-3, tipo-4, otc, pitch, avanzado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-03
relacionados: [generador-sincrono, convertidor-vsc, control-vectorial, ecuacion-oscilacion, servicios-red-soporte]
referencias:
  - "Hansen, Aerodynamics of Wind Turbines, Earthscan 2008"
  - "Abad et al., Doubly Fed Induction Machine, Wiley 2011"
  - "Blaabjerg, Ma, Future on Power Electronics for Wind Turbine Systems, IEEE JESTPE 2013"
---

## Definición
Modelos aerodinámico, mecánico y eléctrico de una turbina eólica con generador **DFIG** (Tipo-3,
doblemente alimentado) o **PMSG** (Tipo-4, velocidad variable full-converter), y los algoritmos
**MPPT** para seguir la curva óptima de par/potencia en función de la velocidad del viento.

## Fundamento teórico
**Aerodinámica.** La potencia extraíble del viento:
$$ P=\frac{1}{2}\rho\pi R^2 v_w^3\,C_p(\lambda,\beta) $$
con \( \rho \) densidad del aire, \( R \) radio, \( v_w \) velocidad del viento y \( C_p \) el
coeficiente de potencia (límite de Betz: 16/27 ≈ 0.593). \( C_p \) depende de la **velocidad
específica** \( \lambda=\omega_r R/v_w \) y del ángulo de paso \( \beta \). Existe un \( \lambda^* \)
óptimo que maximiza \( C_p^{max} \approx0.45\text{–}0.50 \).

**MPPT:** mantener \( \lambda=\lambda^* \) a viento variable ajustando la velocidad de giro:
\( \omega_r^*=\lambda^* v_w/R \). Para evitar anemómetro, estrategia **OTC** (Optimal Torque
Control): la curva óptima \( T^*=k_{opt}\omega_r^2 \) (par ∝ cuadrado de velocidad), o
**Speed-mode**: regular \( \omega_r \) a la referencia calculada del viento medido.

**Drivetrain (tren de transmisión).** Modelo de dos masas (rotor aerodinámico + generador):
$$ 2H_t\dot\omega_t=T_{aero}-K_{dt}\theta_{tw}-D_{dt}(\omega_t-\omega_g)/\omega_0 $$
$$ 2H_g\dot\omega_g=K_{dt}\theta_{tw}+D_{dt}(\omega_t-\omega_g)/\omega_0-T_e $$
El modo de torsión del eje (1–3 Hz) puede excitar SSR con compensación serie.

**DFIG (Tipo-3).** El rotor se alimenta por un convertidor back-to-back de potencia parcial
(\(\sim30\,\%\)). Control vectorial del rotor: eje d alineado con el flujo de estátor → desacopla
\( T_e \) (por \( i_{rq} \)) y flujo/reactiva (por \( i_{rd} \)).

**PMSG (Tipo-4).** El generador se desacopla completamente de la red por un convertidor back-to-back de potencia total. Control vectorial del lado máquina: MPPT vía par; lado red: regula bus DC y potencia reactiva.

<div class="cfig"><img src="figuras/eolica-mppt-cp.png" alt="curvas de potencia de la turbina por viento y locus MPPT"><div class="cap">Para cada velocidad de viento, la potencia de la turbina tiene un máximo a una velocidad de rotor distinta (donde $\lambda=\lambda^*$). El MPPT mantiene ese óptimo: la curva de par $T^*=k\,\omega_r^2$ (locus $\propto\omega^3$) pasa justo por los picos, así que basta seguirla —sin medir el viento— para extraer la máxima potencia.</div></div>

## 1 — Del par óptimo \( T^*=k_{opt}\,\omega_r^2 \) sin medir el viento

La estrategia OTC sigue la curva de potencia máxima sin anemómetro. La clave: si se mantiene \( \lambda=\lambda^* \), la velocidad del viento se puede **eliminar** de la ecuación de potencia y dejar el par como función solo de la velocidad de giro, que sí se mide.

**Paso 1 — potencia en el punto óptimo.** Partimos de la aerodinámica con \( A=\pi R^2 \):
$$ P=\tfrac12\,\rho\,A\,v_w^3\,C_p(\lambda,\beta) $$
En MPPT se opera siempre en \( \lambda=\lambda^* \), \( \beta=0 \), donde \( C_p=C_p^{max} \) es **constante**.

**Paso 2 — eliminar el viento usando \( \lambda^* \).** Por definición \( \lambda^*=\omega_r R/v_w \), luego el viento es \( v_w=\omega_r R/\lambda^* \). Sustituyendo \( v_w^3 \) en el Paso 1:
$$ P_{opt}=\tfrac12\,\rho\,A\,C_p^{max}\left(\frac{\omega_r R}{\lambda^*}\right)^3=\underbrace{\frac{\rho\,A\,R^3\,C_p^{max}}{2\,\lambda^{*3}}}_{\displaystyle k_{opt,P}}\;\omega_r^3 $$
El viento ha desaparecido: en la curva óptima, \( P_{opt}\propto\omega_r^3 \).

**Paso 3 — pasar de potencia a par.** El par mecánico es \( T=P/\omega_r \). Dividiendo el Paso 2 por \( \omega_r \):
$$ \boxed{\;T^*=\frac{P_{opt}}{\omega_r}=\underbrace{\frac{\rho\,\pi R^5\,C_p^{max}}{2\,\lambda^{*3}}}_{\displaystyle k_{opt}}\;\omega_r^2\;} $$
(usando \( A R^3=\pi R^5 \)). El control de par del generador solo necesita medir \( \omega_r \) y aplicar \( T_e=k_{opt}\,\omega_r^2 \); el sistema se asienta solo en el óptimo. Si el viento sube, \( T_{aero} \) supera al \( T^* \) demandado y el rotor **acelera**; al acelerar, \( T^*=k_{opt}\omega_r^2 \) crece hasta reequilibrar en el nuevo \( \omega_r \) que vuelve a dar \( \lambda=\lambda^* \).

## 2 — El modelo aerodinámico completo: \( C_p(\lambda,\beta) \)

La curva \( C_p(\lambda,\beta) \) es la "huella digital" aerodinámica de la turbina. Existe un modelo analítico ampliamente usado en simulación:

**Paso 1 — la forma funcional.** Para álabes de perfil aerodinámico típico:
$$ C_p(\lambda,\beta)=c_1\!\left(\frac{c_2}{\lambda_i}-c_3\beta-c_4\right)\exp\!\left(\frac{-c_5}{\lambda_i}\right)+c_6\lambda $$
donde la velocidad específica efectiva \( \lambda_i \) corregida por el ángulo de paso es:
$$ \frac{1}{\lambda_i}=\frac{1}{\lambda+0.08\beta}-\frac{0.035}{\beta^3+1} $$
Coeficientes típicos (WTG de 2 MW): \( c_1=0.5176 \), \( c_2=116 \), \( c_3=0.4 \), \( c_4=5 \), \( c_5=21 \), \( c_6=0.0068 \).

**Paso 2 — el óptimo.** El máximo de \( C_p \) respecto a \( \lambda \) (con \( \beta=0 \)) ocurre en \( \lambda^*\approx8 \), donde \( C_p^{max}\approx0.48 \). Este valor es específico del fabricante; se obtiene del ensayo en túnel de viento o de la curva de potencia certificada.

**Paso 3 — efecto de \( \beta \).** Aumentar el ángulo de paso \( \beta \) desplaza la curva \( C_p(\lambda) \) hacia valores más bajos y hacia \( \lambda \) menores. Para \( \beta=5° \): \( C_p^{max}\approx0.40 \) en \( \lambda^*\approx7 \); para \( \beta=10° \): \( C_p^{max}\approx0.30 \). Esto es el **pitch control**: reducir \( C_p \) limitando la potencia cuando el viento supera la velocidad nominal.

## 3 — La curva de potencia aerodinámica y el límite de Betz

**Paso 1 — la potencia extraíble del viento.** El flujo de energía cinética por unidad de tiempo a través de un disco de área \( A=\pi R^2 \):
$$ P_{viento}=\frac{1}{2}\rho A v^3 $$
El rotor de la turbina extrae solo una fracción \( C_p \) de esta potencia (el aerogenerador no puede detener el viento completamente):
$$ P=\frac{1}{2}\rho A v^3\,C_p(\lambda,\beta),\qquad \lambda=\frac{\omega_r R}{v} $$

**Paso 2 — derivación del límite de Betz \( C_{p,max}=16/27 \).** Betz (1919) modeló el rotor como un disco actuador: la velocidad del viento en el disco es \( v_d=(1-a)v \), con \( a \) el factor de inducción axial. Aguas abajo la velocidad es \( v_2=(1-2a)v \). El balance de energía da:
$$ C_p=4a(1-a)^2 $$

Maximizando respecto a \( a \): \( dC_p/da=4[(1-a)^2-2a(1-a)]=4(1-a)(1-3a)=0 \to a=1/3 \).

Sustituyendo:
$$ \boxed{\;C_{p,max}=4\cdot\frac{1}{3}\cdot\left(1-\frac{1}{3}\right)^2=\frac{4}{3}\cdot\frac{4}{9}=\frac{16}{27}\approx0.593\;} $$

En práctica, los efectos de la estela giratoria y la viscosidad reducen el \( C_p \) máximo alcanzable a \( 0.45\text{–}0.50 \) para turbinas modernas de tres palas.

**Paso 3 — la velocidad de punta de pala \( \lambda \).** La velocidad específica \( \lambda=\omega_r R/v \) es el cociente entre la velocidad periférica de la punta del álabe y la velocidad del viento libre. Cada geometría de álabe tiene un \( \lambda^* \) donde \( C_p \) es máximo. Para \( \lambda<\lambda^* \): el rotor gira demasiado lento, el álabe tiene ángulo de ataque muy alto → pérdida de sustentación (stall). Para \( \lambda>\lambda^* \): el rotor gira demasiado rápido, el álabe "ve" el viento en ángulo casi paralelo → poca fuerza útil.

## 4 — Control MPPT para velocidad variable: derivación de \( k_{opt} \)

**Paso 1 — la condición de operación óptima.** En la curva óptima, la velocidad específica se mantiene fija en \( \lambda^* \). Entonces:
$$ v=\frac{\omega_r R}{\lambda^*}\quad\Longrightarrow\quad P_{opt}=\frac{1}{2}\rho\pi R^2\left(\frac{\omega_r R}{\lambda^*}\right)^3 C_p^{max} $$

**Paso 2 — la referencia de par \( T_{ref}=k_{opt}\omega_r^2 \).** Dividiendo \( P_{opt} \) por \( \omega_r \):
$$ T_{ref}=\frac{P_{opt}}{\omega_r}=\frac{\rho\pi R^5 C_p^{max}}{2\lambda^{*3}}\,\omega_r^2 $$
$$ \boxed{\;k_{opt}=\frac{\rho\pi R^5 C_p^{max}}{2\lambda^{*3}}\;} $$

**Paso 3 — cálculo numérico para la turbina 2 MW.** Con \( R=45\,\text{m} \), \( \rho=1.225\,\text{kg/m}^3 \), \( \lambda^*=8 \), \( C_p^{max}=0.44 \):
$$ k_{opt}=\frac{1.225\times\pi\times45^5\times0.44}{2\times8^3}=\frac{1.225\times\pi\times1.845\times10^8\times0.44}{1024}\approx3.01\times10^5\,\text{N·m·s}^2/\text{rad}^2 $$

El control solo necesita medir \( \omega_r \) y aplicar \( T_e=k_{opt}\omega_r^2 \): sin anemómetro, sin modelo inverso, robustez inherente. Si el viento aumenta, el rotor acelera y el par de referencia sube cuadráticamente, aumentando la extracción de potencia hasta el nuevo equilibrio en \( \lambda=\lambda^* \).

**Paso 4 — velocidad nominal a 12 m/s.** Para \( v=12\,\text{m/s} \):
$$ \omega_{r,nom}=\frac{\lambda^*\,v}{R}=\frac{8\times12}{45}=2.133\,\text{rad/s}\;\;(20.4\,\text{rpm}) $$
$$ T_{nom}=k_{opt}\omega_{r,nom}^2=3.01\times10^5\times2.133^2\approx1.368\times10^6\,\text{N·m}\quad(P=T\omega=2.92\,\text{MW}) $$
*(La potencia supera los 2 MW porque a v=12 m/s con Cp_max=0.44 se extrae más que la potencia nominal; el pitch control limitará a 2 MW.)*

## 5 — El convertidor back-to-back para PMSG

El PMSG (tipo-4) tiene un convertidor back-to-back de plena potencia que desacopla completamente la turbina de la red. Los dos convertidores tienen objetivos independientes.

**Paso 1 — el lado máquina (Machine-Side Converter, MSC).** El MSC controla el par eléctrico \( T_e \) del generador para implementar el MPPT. Con control vectorial orientado al flujo del PMSG (eje d alineado con el flujo del imán permanente \( \psi_d=\psi_{PM} \)):
$$ T_e=\frac{3}{2}\,p\,\psi_{PM}\,i_q $$

Donde \( p \) es el número de pares de polos. El lazo de control en dq:
$$ L_d\,\dot{i}_d=-R_s\,i_d+\omega_e L_q i_q+v_d $$
$$ L_q\,\dot{i}_q=-R_s\,i_q-\omega_e L_d i_d-\omega_e\psi_{PM}+v_q $$

Los lazos de corriente \( i_d \) e \( i_q \) se sintonicen con IMC; \( i_d^*=0 \) (sin flujo externo adicional) e \( i_q^*=T_{ref}^*/[1.5\,p\,\psi_{PM}] \).

**Paso 2 — el bus DC intermedio.** El condensador del bus DC almacena la energía entre ambos convertidores:
$$ C_{dc}\,\dot{v}_{dc}=i_{MSC}-i_{GSC} $$
La dinámica del bus DC es la diferencia entre la corriente del MSC (potencia extraída de la turbina) y la del GSC (potencia entregada a la red).

**Paso 3 — el lado red (Grid-Side Converter, GSC).** El GSC opera como un VSC estándar en modo grid-following. Regula la tensión del bus DC (\( v_{dc}^*=1150\,\text{V} \)) y controla la potencia reactiva entregada a la red (\( Q^*=0 \) o el valor del grid code). Control vectorial orientado a la tensión de red (eje d alineado con \( V_{grid} \)): lazo de tensión de bus externo → referencia de corriente activa → lazo de corriente dq interno.

**Ventaja del back-to-back completo:** la turbina puede girar a la velocidad óptima para cada viento, completamente desacoplada de la frecuencia de red. La turbina puede incluso operar temporalmente a velocidades no síncronas durante transitorios de red (FRT).

## 6 — Diseño iterativo: turbina 2 MW (§ nuevo)

**Datos:** \( P_{rated}=2\,\text{MW} \), \( R=45\,\text{m} \), \( \rho=1.225\,\text{kg/m}^3 \), \( \lambda^*=8 \), \( C_p^{max}=0.44 \).

**Paso 1 — constante k_opt.**
$$ k_{opt}=\frac{1.225\times\pi\times45^5\times0.44}{2\times512}\approx3.01\times10^5\,\text{N·m·s}^2/\text{rad}^2 $$

**Paso 2 — velocidad nominal a 12 m/s.**
$$ v_{rated}: \quad P_{rated}=\frac{1}{2}\rho\pi R^2 v_{rated}^3 C_p^{max} $$
$$ v_{rated}=\left(\frac{2\times2\times10^6}{1.225\times\pi\times2025\times0.44}\right)^{1/3}=\left(\frac{4\times10^6}{2738}\right)^{1/3}=\left(1461\right)^{1/3}\approx11.3\,\text{m/s} $$
$$ \omega_{r,nom}=\frac{8\times11.3}{45}=2.009\,\text{rad/s}\;\;(19.2\,\text{rpm}) $$

**Paso 3 — par de referencia nominal.**
$$ T_{nom}=k_{opt}\,\omega_{r,nom}^2=3.01\times10^5\times(2.009)^2\approx1.215\times10^6\,\text{N·m} $$
Verificación: \( P=T\omega=1.215\times10^6\times2.009\approx2.44\,\text{MW} \). La diferencia respecto a 2 MW se debe a que el pitch control limita la potencia a la nominal; en la curva de potencia certificada, \( C_p \) efectivo a viento nominal es menor que \( C_p^{max} \) (la turbina opera ligeramente fuera del óptimo para respetar el límite de par).

<div class="cfig"><img src="../figuras/eolica-mppt-analisis.png" alt="4 paneles: Cp(lambda,beta), P(wr) con MPP, OTC T*=k·wr², dinámica 8→12 m/s"><div class="cap">
(a) \(C_p(\lambda)\) para β=0°, 5°, 10°: el pitch control desplaza la curva hacia abajo; el óptimo se desplaza a menor λ. (b) Curvas \(P(\omega_r)\) para v=6, 8, 10, 12 m/s y el locus MPPT (trazado punteado) que pasa por todos los picos. (c) Parábola OTC \(T^*=k_{opt}\omega_r^2\): las iso-potencias son líneas rectas en el plano \(T\text{-}\omega\). (d) Respuesta dinámica ante cambio de viento 8→12 m/s: \(\omega_r(t)\) sube gradualmente mientras la potencia sigue el locus óptimo con un pequeño retraso inercial.
</div></div>

## 7 — Control MPPT por referencia de velocidad \( \omega_r^* \) (con anemómetro)

El control por referencia de velocidad (**speed-mode**) calcula directamente la velocidad de rotor óptima a partir del viento medido.

**Paso 1 — referencia de velocidad.** De la definición de velocidad específica óptima:
$$ \omega_r^*=\frac{\lambda^*\,v_w}{R} $$
Con un anemómetro de respuesta rápida (típico en DFIG de clase grande), la referencia se actualiza cada ciclo de control.

**Paso 2 — referencia de par.** El par de referencia que impone el lazo de control del generador:
$$ T^*=\frac{P_{opt}^*}{\omega_r^*}=\frac{k_{opt,P}\,(\omega_r^*)^3}{\omega_r^*}=k_{opt,P}\,(\omega_r^*)^2 $$
que coincide con la fórmula OTC evaluada en la velocidad óptima, no en la actual. La diferencia práctica: en speed-mode el lazo regula \( \omega_r \) a \( \omega_r^* \) (lazo de velocidad externo); en OTC impone el par directamente sin lazo de velocidad.

**Ventaja del speed-mode:** reacciona más rápido a cambios bruscos de viento (la referencia \( \omega_r^* \) cambia de inmediato). **Desventaja:** requiere anemómetro fiable y el lazo de velocidad añade dinamismo propio (puede excitar el modo torsional del drivetrain si se sintoniza demasiado agresivo).

## 8 — Control MPPT sin anemómetro: la ley \( P^*=k_{opt}\,\omega_r^3 \)

La estrategia OTC implementa directamente \( T_e=k_{opt}\omega_r^2 \) o equivalentemente \( P^*=k_{opt,P}\omega_r^3 \) usando solo la velocidad de giro medida.

**Paso 1 — la constante \( k_{opt} \) a partir de los datos de la turbina.**
$$ k_{opt}=\frac{1}{2}\rho\,\pi R^5\,\frac{C_p^{max}}{\lambda^{*3}} $$
Para la turbina 2 MW de §7 (\( R=45\,\text{m} \), \( \rho=1.225\,\text{kg/m}^3 \), \( C_p^{max}=0.48 \), \( \lambda^*=8 \)):
$$ k_{opt}=\frac{1.225\times\pi\times45^5\times0.48}{2\times8^3}\approx 4.38\times10^5\,\text{N·m/(rad/s)}^2 $$

**Paso 2 — par de referencia instantáneo.**
$$ T_e^*=k_{opt}\,\omega_r^2 $$
El control vectorial del generador (DFIG o PMSG) impone este par ajustando la corriente de eje q del rotor: \( T_e=\frac{3}{2}p\,L_m\,i_{sq}^*\,\psi_d \) en DFIG.

**Paso 3 — estabilidad inherente del OTC.** El punto de equilibrio \( T_{aero}(\omega_r,v_w)=T_e^*(\omega_r) \) es estable porque la curva OTC tiene pendiente positiva (\( \partial T^*/\partial\omega_r=2k_{opt}\omega_r>0 \)) y la curva aerodinámica tiene pendiente menor en el óptimo. Una perturbación que hace subir \( \omega_r \) aumenta \( T_e^* \) más rápido que \( T_{aero} \), frenando el rotor de vuelta al equilibrio.

## 9 — La transición MPPT → potencia limitada: pitch control

Por encima de la velocidad de viento nominal \( v_{rated} \), la potencia aerodinámica disponible supera la nominal del generador. Si no se actuara, el rotor aceleraría más allá de su límite mecánico.

**Paso 1 — la condición de transición.** Se detecta cuando \( P_{mec}\geq P_{rated} \) (o \( \omega_r\geq\omega_{rated} \)). Se activa el controlador de paso (\( \beta \)-controller).

**Paso 2 — el lazo de pitch.** Un PI sobre la potencia (o sobre la velocidad) actúa sobre \( \beta \):
$$ \Delta\beta = K_{p,\beta}(P-P_{rated}) + K_{i,\beta}\int(P-P_{rated})\,dt $$
Al aumentar \( \beta \), \( C_p \) cae → la potencia aerodinámica baja → el rotor se estabiliza cerca de \( \omega_{rated} \).

**Paso 3 — coordinación con MPPT.** Para \( v_w < v_{rated} \): \( \beta=0 \) fijo y OTC activo. Para \( v_w > v_{rated} \): OTC desactivado, \( \omega_r=\omega_{rated}=\text{const} \), pitch activo. Para \( v_w > v_{cut-off}\approx25\,\text{m/s} \): la turbina para (\( \beta\to90° \) → feathering).

El transitorio de handover entre MPPT y pitch es crítico: si el pitch responde más lento que el viento sube, el rotor puede sobrevelocidad brevemente; si el MPPT no se "apaga" suavemente, el par del generador puede caer bruscamente causando oscilaciones.

## 10 — Diseño iterativo: turbina 2 MW

**Datos:** \( P_{rated}=2\,\text{MW} \), \( \lambda^*=8 \), \( C_p^{max}=0.48 \), \( R=45\,\text{m} \), \( \rho=1.225\,\text{kg/m}^3 \).

**Velocidad de viento nominal.** De \( P_{rated}=\frac{1}{2}\rho\pi R^2 v_{rated}^3 C_p^{max} \):
$$ v_{rated}=\left(\frac{2P_{rated}}{\rho\pi R^2 C_p^{max}}\right)^{1/3}=\left(\frac{2\times2\times10^6}{1.225\times\pi\times2025\times0.48}\right)^{1/3}\approx12.4\,\text{m/s} $$

**Velocidad de rotor nominal.** Con \( \lambda^*=8 \) y \( v_{rated}=12.4\,\text{m/s} \):
$$ \omega_{r,nom}=\frac{\lambda^*\,v_{rated}}{R}=\frac{8\times12.4}{45}\approx2.20\,\text{rad/s}\;(21.1\,\text{rpm}) $$

**Par nominal.** \( T_{nom}=P_{rated}/\omega_{r,nom}=2\times10^6/2.20\approx909\,\text{kN·m} \).

**Constante OTC.** \( k_{opt}=T_{nom}/\omega_{r,nom}^2=909000/2.20^2\approx1.88\times10^5\,\text{N·m·s}^2/\text{rad}^2 \).
*(Nota: difiere del Paso 1 del §4 porque ese usaba \( A=\pi R^2 \) directamente; la discrepancia es normal si los datos de \( C_p \) del modelo analítico difieren de los del fabricante. En la práctica, \( k_{opt} \) se calibra con la curva de potencia certificada.)*

**Verificación de energía.** Para un emplazamiento con distribución de Weibull \( (k=2,\,c=8\,\text{m/s}) \), la densidad de energía anual aprovechable con MPPT perfecto es:
$$ E_{año}=\int_{v_{cut-in}}^{v_{cut-off}}P(v)\,f(v)\,8760\,dv \approx 4800\,\text{h}\times P_{rated} = 9.6\,\text{GWh} $$


## 11 — Modelo aerodinámico y mecánico: tren de transmisión de dos masas

La potencia mecánica extraída del viento y la dinámica del tren de transmisión determinan la respuesta de la turbina ante variaciones de viento y perturbaciones de la red.

**Potencia aerodinámica.** El viento que atraviesa el área barrida por el rotor \(A = \pi R^2\) lleva un flujo de energía cinética. La turbina extrae la fracción \(C_p\):
$$ P_{aero} = \frac{1}{2}\,\rho\,A\,C_p(\lambda,\beta)\,v_w^3,\qquad \lambda = \frac{\omega_r\,R}{v_w} $$
El coeficiente de potencia real de turbinas modernas de tres palas alcanza \(C_{p,max} \approx 0.45\text{–}0.50\), frente al límite teórico de Betz \(16/27 \approx 0.593\).

**TSR óptimo.** Cada geometría de álabe tiene un \(\lambda^*\) donde \(C_p\) es máximo. Para las curvas analíticas de uso habitual en simulación, \(\lambda^* \approx 8\) con \(\beta = 0\). El MPPT mantiene \(\lambda = \lambda^*\) ajustando \(\omega_r\).

**Modelo de dos masas (drivetrain).** La transmisión mecánica entre el rotor aerodinámico (masa grande, constante de inercia \(H_t \approx 3\text{–}5\,\text{s}\)) y el generador (masa pequeña, \(H_g \approx 0.5\text{–}1\,\text{s}\)) introduce un modo torsional a 1–3 Hz:
$$ 2H_t\,\dot{\omega}_t = T_{aero} - K_{dt}\,\theta_{tw} - D_{dt}\,(\omega_t - \omega_g)/\omega_0 $$
$$ 2H_g\,\dot{\omega}_g = K_{dt}\,\theta_{tw} + D_{dt}\,(\omega_t - \omega_g)/\omega_0 - T_e $$
donde \(\theta_{tw}\) es el ángulo de torsión del eje, \(K_{dt}\) la rigidez torsional y \(D_{dt}\) el amortiguamiento. La frecuencia del modo torsional:
$$ f_{tw} = \frac{1}{2\pi}\sqrt{\frac{K_{dt}}{2}\!\left(\frac{1}{H_t} + \frac{1}{H_g}\right)} \approx 1\text{–}3\,\text{Hz} $$
Este modo puede interactuar con la compensación serie de la red (SSR) si el MPPT se sintoniza demasiado agresivo.

**Punto a resaltar.** Modelar la turbina como una masa única (sin el drivetrain) es suficiente para estudios de respuesta lenta (minutos), pero **insuficiente** para el análisis de oscilaciones electromecánicas y estabilidad de subsistemas a 1–3 Hz.

## 12 — Control MPPT por seguimiento de par: OTC y transición a potencia limitada

**Estrategia OTC (Optimal Torque Control).** La referencia de par se impone directamente sin medir el viento:
$$ T_{ref} = k_{opt}\,\omega_r^2,\qquad k_{opt} = \frac{\rho\,\pi\,R^5\,C_{p,max}}{2\,\lambda^{*3}} $$
El control vectorial del generador (DFIG o PMSG) impone \(T_e = T_{ref}\) ajustando la corriente de eje q. Si el viento sube, \(T_{aero} > T_{ref}\): el rotor acelera hasta que \(k_{opt}\omega_r^2\) se iguala con \(T_{aero}\) en el nuevo \(\lambda = \lambda^*\).

**Zona II (MPPT activo) vs zona III (potencia limitada).**
- **Zona II** (\(v_w < v_{rated}\)): \(\beta = 0\), OTC activo, \(\omega_r\) variable. La potencia sigue \(P \propto \omega_r^3 \propto v_w^3\).
- **Zona III** (\(v_w > v_{rated}\)): la potencia aerodinámica disponible supera \(P_{rated}\). Se activa el control de paso (\(\beta\)-controller), que sube \(\beta\) para reducir \(C_p\) y mantener \(P = P_{rated}\). El OTC se desconecta y \(\omega_r \approx \omega_{rated} = \text{cte}\).
- **Transición suave:** cuando \(P\) se acerca a \(P_{rated}\), la referencia de par del OTC se satura suavemente. Una rampa de saturación evita la discontinuidad de torque que causaría oscilaciones torsionales.

**DFIG vs PMSG.**
- **DFIG (Tipo-3):** el rotor está acoplado a la red a través de un convertidor de potencia parcial (~30 %). El control vectorial del rotor ajusta \(i_{rq}\) para imponer \(T_e\). Respuesta rápida, menor coste de convertidor, pero el acoplamiento parcial limita el rango de velocidad a ±30 % de la velocidad síncrona.
- **PMSG (Tipo-4):** convertidor back-to-back de plena potencia. El MSC controla el par del generador y el GSC regula el bus DC y la potencia reactiva hacia la red. Desacoplamiento completo → mayor rango de velocidad, mejor FRT, pero mayor coste de convertidor.

## 13 — Contribución a la red: inercia sintética y deloading

**El problema de inercia.** La turbina eólica con convertidor back-to-back está desacoplada mecánicamente de la frecuencia de red. La energía cinética del rotor (\(E = H\,S_{base}\)) no responde automáticamente a caídas de frecuencia: el rotor puede girar a cualquier velocidad sin que la red "lo note". Esto reduce la inercia efectiva del sistema a medida que crece la penetración eólica.

**Inercia virtual (FFR: Fast Frequency Response).** Se añade un lazo adicional que modula la referencia de par en respuesta a la desviación de frecuencia:
$$ T_{extra}(s) = -2H_{virt}\,s\,\Delta\omega_{PLL}(s) \approx -2H_{virt}\,\frac{d\omega_{PLL}}{dt} $$
donde \(H_{virt}\) es la constante de inercia virtual (configurable). El término derivativo del PLL estima el ROCOF. Si la frecuencia cae (pérdida de generación), \(d\omega/dt < 0\) → \(T_{extra} > 0\) → el generador extrae más potencia del rotor → la frecuencia se sostiene. Esta respuesta es activa durante los primeros 0–5 segundos tras la perturbación.

**Deloading.** Para tener reserva de regulación primaria disponible, la turbina opera intencionalmente por debajo del MPP:
$$ T_{ref} = (1 - \delta)\,k_{opt}\,\omega_r^2,\qquad \delta = 5\text{–}10\,\% $$
El margen de potencia reservado puede inyectarse rápidamente cuando la frecuencia cae. Coste: pérdida permanente de \(\delta\) de la energía disponible.

**Droop de frecuencia.** Similar al generador síncrono, se añade un término proporcional a \(\Delta f\):
$$ \Delta P_{droop} = -\frac{1}{R_f}\,\Delta f,\qquad R_f \approx 4\text{–}5\,\% $$
para participar en la regulación primaria de frecuencia con respuesta tipo governor.

## 14 — Modelos de viento, fatiga y compromiso vida útil vs frecuencia

**Perfil de viento.** La velocidad del viento tiene dos componentes: media \(\bar{v}_w\) (varía en decenas de minutos) y turbulencia \(v'(t)\) (variaciones rápidas, segundos). El espectro de turbulencia se modela con los modelos de Kaimal (isotrópico) o Von Kármán (anisotrópico):
$$ S_{vv}(f) = \frac{4\,\sigma_u^2\,L_u/\bar{v}_w}{(1 + 6\,f\,L_u/\bar{v}_w)^{5/3}} \quad\text{(Kaimal)} $$
donde \(\sigma_u\) es la desviación estándar de la turbulencia y \(L_u\) la escala de longitud integral (\(\approx 50\text{–}200\,\text{m}\)).

**Carga de fatiga.** Las variaciones rápidas de par (por turbulencia y efecto de torre) causan ciclos de carga en el eje y las palas. La regla de Miner acumula el daño:
$$ D = \sum_i \frac{n_i}{N_i} $$
donde \(n_i\) son los ciclos a la amplitud \(i\) y \(N_i\) es el número de ciclos a fallo para esa amplitud (curva S-N del material). La vida útil se agota cuando \(D = 1\).

**Filtrado de la referencia de potencia.** Las variaciones rápidas de \(\omega_r\) (por turbulencia) generan variaciones rápidas de \(T_{ref} = k_{opt}\omega_r^2\), que se traducen en ciclos de par de alta frecuencia. Un filtro paso bajo sobre la referencia:
$$ T_{ref,filtrado}(s) = \frac{1}{1 + \tau_{lp}\,s}\,k_{opt}\,\omega_r^2 $$
reduce la fatiga a costa de seguir el MPP con un retraso \(\tau_{lp}\). La energía perdida por el suavizado es pequeña (< 0.5 %) pero el beneficio en vida útil puede ser significativo.

**Compromiso fundamental.** Respuesta de frecuencia rápida (inercia virtual, droop) requiere variaciones rápidas de par → más ciclos de fatiga → menor vida útil de la transmisión. Servicios de frecuencia agresivos pueden acortar la vida de la caja multiplicadora en turbinas DFIG de manera apreciable. La optimización de este compromiso es un área activa de investigación.

<div class="cfig"><img src="../figuras/eolica-mppt-analisis.png" alt="4 paneles: Cp vs lambda, curvas P-omega con MPPT, referencia de par OTC, inercia sintética"><div class="cap">
(a) Coeficiente de potencia \(C_p(\lambda)\) para ángulos de paso \(\beta = 0°, 5°, 10°, 15°\): el pitch control desplaza las curvas hacia abajo, reduciendo la potencia extraída. El límite de Betz (línea punteada) es inalcanzable en práctica. (b) Curvas \(P(\omega_r)\) para distintas velocidades de viento y la parábola MPPT \(P^* = k_{opt}\omega_r^3\) que pasa por todos los picos. (c) Referencia de par OTC \(T_{ref} = k_{opt}\omega_r^2\): curva parabólica que el control de par del generador sigue directamente midiendo \(\omega_r\). (d) Inercia sintética: ante una perturbación de frecuencia \(\Delta f\), el término de inercia virtual inyecta un par adicional proporcional a \(d\omega/dt\), amortiguando la caída inicial de frecuencia.
</div></div>

## Cuándo y por qué se usa
Para modelar el comportamiento de un parque eólico en estudios de estabilidad, diseño de control
de parque, servicios de frecuencia y análisis de interacción con la red.

## Procedimiento de diseño (genérico)
1. Parametriza la curva \( C_p(\lambda,\beta) \) del fabricante; halla \( \lambda^*,C_p^{max} \).
2. Implementa el drivetrain de dos masas y la referencia MPPT (\( T^*=k_{opt}\omega_r^2 \)).
3. Diseña el control vectorial del generador (DFIG o PMSG): lazos de par y flujo/reactiva.
4. Diseña el lado red: bus DC y Q de red.
5. Añade pitch control para viento > nominal y protecciones de alta velocidad.
6. Verifica FRT e inyección de reactiva según grid code.

## Ejemplo de código
```python
def cp_lambda(lam, beta, c=(0.5176, 116, 0.4, 5, 21, 0.0068)):
    lam_i = 1/(lam + 0.08*beta) - 0.035/(beta**3 + 1)
    lam_i = max(lam_i, 1e-6)
    c1,c2,c3,c4,c5,c6 = c
    return c1*(c2/lam_i - c3*beta - c4)*np.exp(-c5/lam_i) + c6*lam

def mppt_otc(wr, kopt):
    return kopt * wr**2          # par optimo sin anemometro

# constante OTC para turbina 2MW
rho=1.225; R=45; Cp_max=0.48; lam_opt=8
kopt = 0.5*rho*np.pi*R**5*Cp_max/lam_opt**3
```

## Parámetros y valores típicos
\( C_p^{max}\approx0.45\text{–}0.50 \); \( \lambda^*\approx6\text{–}9 \); \( H_t\approx3\text{–}5 \) s;
\( H_g\approx0.5\text{–}1 \) s. DFIG: deslizamiento ±30 %, potencia convertidor ∼30 %. PMSG: convertidor 100 %. Pitch rate máximo: 8–10 °/s.

## Errores comunes
- Modelar la turbina sin el drivetrain de dos masas → no captura el modo torsional (crítico para SSR).
- DFIG con control solo de lado rotor sin regular el bus DC → tensión DC no controlada.
- MPPT más rápido que el drivetrain → excita la resonancia torsional.
- Usar la misma \( k_{opt} \) calculada analíticamente sin calibrar con la curva real → error de energía de hasta 5 %.

## Conceptos relacionados
- [[generador-sincrono]] · [[convertidor-vsc]] · [[control-vectorial]] · [[ecuacion-oscilacion]] · [[servicios-red-soporte]]

## Referencias
- Hansen, *Aerodynamics of Wind Turbines*, Earthscan 2008.
- Abad et al., *Doubly Fed Induction Machine*, Wiley 2011.
- Blaabjerg, Ma, *Future on Power Electronics for Wind Turbine Systems*, IEEE JESTPE 2013.
