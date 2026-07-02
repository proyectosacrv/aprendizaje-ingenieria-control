---
titulo: Microrred híbrida AC/DC e interlink converter
slug: microrred-hibrida-ac-dc
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: []
objetivos: [entender la arquitectura de una microrred con subredes AC y DC acopladas]
tags: [microrred-hibrida, ac-dc, interlink, ilc, bus-dc, datacenter, intermedio]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-02
relacionados: [convertidor-vsc, dinamica-bus-dc, droop-dc, control-jerarquico-microrred, carga-pulsante-datacenter-ia]
referencias:
  - "Loh et al., Autonomous Operation of Hybrid Microgrid With AC and DC Subgrids, IEEE TPEL 2013"
  - "Nejabatkhah, Li, Overview of Power Management Strategies of Hybrid AC/DC Microgrid, IEEE TPEL 2015"
---

## Definición
Microrred con **dos subredes** —una AC y una DC— unidas por uno o varios **convertidores de
interconexión** (interlink converter, ILC). Combina las ventajas de cada dominio: la DC integra de
forma natural PV, baterías y cargas electrónicas (data centers); la AC conecta a la red y a cargas
rotativas.

## Fundamento teórico
- **Subred DC:** bus de tensión \( V_{dc} \) con fuentes/cargas y reparto por [[droop-dc]]. Su
  estado de carga se refleja en \( V_{dc} \) (ver [[dinamica-bus-dc]]).
- **Subred AC:** bus de frecuencia \( \omega \)/tensión \( V \) con droop AC ([[droop-control]]).
- **Interlink converter (ILC):** un [[convertidor-vsc|VSC]] bidireccional que **transfiere potencia**
  entre ambas y normaliza los indicadores de carga de cada subred. La estrategia autónoma habitual
  iguala los **droop normalizados**:
  $$ P_{ILC}\ \propto\ \frac{\omega-\omega^*}{\Delta\omega_{max}}-\frac{V_{dc}-V_{dc}^*}{\Delta V_{dc,max}} $$
  de modo que cuando una subred está más cargada (su variable de droop más desviada), el ILC le
  envía potencia desde la otra, **repartiendo el estrés** sin comunicaciones.

Modos: **conectado a red** (la red AC fija \( \omega,V \); el ILC regula \( V_{dc} \)) e **isla**
(droop en ambas subredes + balanceo por el ILC). Para data centers IA, la subred DC absorbe la
[[carga-pulsante-datacenter-ia|carga pulsante]] y el dimensionado del bus ([[dinamica-bus-dc]]) y la
estabilidad CPL son críticos.

<div class="cfig"><img src="figuras/microrred-hibrida-ac-dc-arquitectura.png" alt="arquitectura de microrred hibrida AC/DC con convertidor de interconexion"><div class="cap">Dos subredes —una AC (bus de frecuencia/tensión, con red y cargas rotativas) y una DC (bus de tensión, con PV, baterías y cargas electrónicas)— unidas por un convertidor de interconexión (ILC) bidireccional. El ILC iguala los droops normalizados de cada subred y transfiere potencia desde la menos cargada hacia la más cargada, repartiendo el estrés sin comunicaciones.</div></div>

## 1 — Balance de potencia a través del ILC y su efecto sobre el bus DC
El ILC no almacena energía (salvo su pequeño condensador): cuanta potencia toma de una subred, la entrega a la otra menos sus pérdidas. Ese balance es lo que liga la dinámica de las dos subredes y, en particular, lo que el bus DC "ve".

**Paso 1 — balance en el ILC.** Sea \( P_{ac} \) la potencia que el ILC toma del lado AC y \( P_{dc} \) la que entrega al lado DC. Con rendimiento \( \eta \) del convertidor (sentido AC→DC):

$$ P_{dc}=\eta\,P_{ac}\qquad(\eta\to1\text{ idealmente}) $$

El ILC es bidireccional: si \( P_{ac}<0 \) la potencia fluye DC→AC. En adelante tomamos \( \eta\approx1 \), de modo que \( P_{dc}\approx P_{ILC} \) es la variable de transferencia.

**Paso 2 — balance de potencia en el nodo del bus DC.** Al bus DC entran la generación local de la subred DC (\( P_{gen,dc} \): PV, batería) y la del ILC; salen las cargas DC (\( P_{load,dc} \)) y lo que acumula el condensador. Por conservación de energía (ver [[dinamica-bus-dc]]):

$$ \frac{dE}{dt}=\underbrace{P_{gen,dc}+P_{ILC}}_{\text{entra}}-\underbrace{P_{load,dc}}_{\text{sale}},\qquad E=\tfrac12 C_{dc}V_{dc}^2 $$

**Paso 3 — condición de bus DC en régimen permanente.** En estado estacionario \( dE/dt=0 \) y \( V_{dc} \) se mantiene, lo que fija la potencia que el ILC debe aportar:

$$ \boxed{\;P_{ILC}=P_{load,dc}-P_{gen,dc}\;} $$

Si la subred DC consume más de lo que genera (déficit), el ILC importa desde el AC; si genera de sobra, exporta. El desbalance instantáneo, mientras el ILC reacciona, lo absorbe el condensador como una excursión de \( V_{dc} \): esa es la señal que la ley de droop normalizado del *Fundamento teórico* usa para pedir más o menos \( P_{ILC} \). De ahí que un déficit en DC se refleje en una caída de \( V_{dc} \) que el ILC compensa transfiriendo potencia desde la subred AC, repartiendo el estrés entre ambas (ver [[carga-pulsante-datacenter-ia]] para el caso del pulso de IA).

## 2 — Arquitectura de la microrred híbrida: los tres buses y sus interfaces

**Bus AC principal.** Opera a 400 V (residencial/comercial) o 690 V (industrial), 50 Hz. Aloja:
- Cargas AC convencionales (iluminación, motores, HVAC).
- Generadores AC síncronos (grupos electrógenos, eólica directa de SCIG).
- El punto de conexión a la red (**PCC**: point of common coupling).

**Bus DC principal.** Opera a 400–800 V DC. Las tensiones típicas son:
- 400 V DC: compatibilidad con estándares de data center (ETSI EN 300 132-3).
- 700–800 V DC: mayor eficiencia en grandes instalaciones (cables más delgados para la misma potencia).

El bus DC integra PV (directamente con boost), BESS (con convertidor bidireccional DC-DC), y cargas electrónicas (servidores, cargadores EV, motores DC con convertidor).

**La interfaz AC-DC: el convertidor interlínea (ILC).** Es un VSC bidireccional de potencia completa. En modo conectado a red:
- El lado AC opera en modo GFL sincronizando con la red.
- El lado DC regula \( V_{dc} \) (lazo de tensión DC).

En modo isla:
- El lado AC opera en modo GFM imponiendo \( f \) y \( V \) en el bus AC.
- La potencia DC/AC viene determinada por el balance de la microrred.

**La jerarquía de control.** El bus AC es la referencia de frecuencia y tensión para la microrred. El bus DC tiene su propia referencia de tensión (\( V_{dc}^* \)) controlada por el ILC. Si hay múltiples ILC, se coordinan mediante droop de tensión DC: un mayor \( V_{dc} \) indica exceso de generación DC y desencadena exportación al AC.

## 3 — El balance de potencia en la microrred: quién controla qué

**En modo conectado a red.** La red AC fija \( f \) y \( V_{ac} \). El ILC regula \( V_{dc} \) absorbiendo o inyectando la diferencia entre generación DC y carga DC. El BESS y el PV operan con sus propios lazos (MPPT para PV, SOC para BESS). El ILC puede importar o exportar potencia de la red según la disponibilidad solar y el SOC de las baterías.

**En modo isla.** Un GFM debe imponer \( f \) y \( V_{ac} \):
- Si hay un generador AC (grupo electrógeno): el grupo impone la frecuencia y la tensión mediante su AVR y governor.
- Si solo hay convertidores: el ILC (o el BESS a través de un convertidor GFM en el bus DC) opera en modo GFM.

El **BESS en el bus DC** hace droop DC para repartir la carga con el convertidor PV o con otros BESS. La ley de droop DC:

$$ V_{dc}=V_{dc}^*-k_{d}\cdot P_{BESS} $$

Un mayor \( k_d \) reduce la variación de \( V_{dc} \) pero implica mayor desvío de tensión con la carga. En práctica \( k_d \) se elige para que \( V_{dc} \) no caiga más del 5% a plena carga.

**Régimen de emergencia.** Si el BESS llega al SOC mínimo o el PV no genera, el ILC puede importar de la red (si está disponible) o conectar el grupo electrógeno de respaldo. La lógica de transición entre modos es parte del **EMS** (Energy Management System), el nivel terciario.

## 4 — La estabilidad de la microrred: el problema de la CPL en el bus DC

**Las cargas de potencia constante (CPL).** Los convertidores de electrónica de potencia que alimentan servidores u otros equipos desde el bus DC tienen control de tensión de salida: mantienen una potencia constante independientemente de la tensión de entrada. Su impedancia incremental es negativa:

$$  \frac{dP_{CPL}}{dV_{dc}}=0\quad\Rightarrow\quad Z_{inc}=\frac{dV_{dc}}{dI_{CPL}}=-\frac{V_{dc}^2}{P_{CPL}} $$

Esta impedancia negativa reduce el amortiguamiento efectivo del bus DC. Para el bus DC con condensador \( C \), inductancia de cable \( L \) y una CPL de potencia \( P_{CPL} \):

$$  L\frac{dI}{dt}=V_{source}-V_{dc}\,, \qquad C\frac{dV_{dc}}{dt}=I-\frac{P_{CPL}}{V_{dc}} $$

Linealizando: el sistema tiene un polo con parte real \( +P_{CPL}/(C\,V_{dc}^2) \) que aumenta con la potencia de la CPL. Existe una **potencia crítica** \( P_{crit} \) por encima de la cual el sistema es inestable.

**Amortiguamiento activo del ILC.** El ILC puede inyectar una corriente proporcional a \( \dot V_{dc} \) (equivalente a añadir una resistencia virtual en el bus DC) sin pérdidas reales. Esto aumenta el amortiguamiento efectivo y eleva \( P_{crit} \):

$$  i_{ad}=K_{ad}\cdot C\frac{dV_{dc}}{dt} $$

Con \( K_{ad} \) ajustado, el amortiguamiento del bus DC puede aumentarse hasta \( \zeta\approx0.7 \) incluso con CPL de gran potencia.

## 5 — El control jerárquico: primario, secundario y terciario

**Nivel primario (ms).** Opera de forma autónoma y descentralizada, sin comunicaciones. Incluye:
- Droop AC en GFM para reparto de \( P \) (por frecuencia) y \( Q \) (por tensión).
- Droop DC en BESS/PV para reparto de corriente (y potencia) en el bus DC.
- Lazo de tensión DC del ILC.
- Amortiguamiento activo del bus DC.

El primario responde en tiempos del orden de la constante de tiempo del lazo de corriente (ms) y del lazo de tensión (decenas de ms). Su desventaja: el droop causa una desviación permanente de \( f \) y \( V_{dc} \) respecto a los valores nominales.

**Nivel secundario (s).** Restaura \( f \) y \( V \) a sus valores nominales tras los cambios de carga. Requiere comunicación lenta (varios segundos de latencia son aceptables):

$$  \omega^*(t)=\omega_0+k_I\int\left(\omega_0-\bar\omega_{meas}\right)dt $$

donde \( \bar\omega_{meas} \) es la frecuencia medida en el PCC (o promediada entre nodos). En la subred DC, el secundario restaura \( V_{dc} \) ajustando la referencia del droop.

**Nivel terciario (min).** Optimización de la operación de la microrred:
- Minimización del coste de energía (prioridad: PV > BESS > red).
- Maximización del autoconsumo solar.
- Gestión del SOC del BESS para garantizar autonomía en modo isla.
- Coordinación con la red para servicios (respuesta de frecuencia, peak shaving).

El terciario es centralizado (EMS) y opera con horizontes de 15 min a horas. Sus salidas son setpoints para el secundario: \( P_{ILC}^{ref} \), \( SOC^{ref} \), \( P_{PV}^{ref} \).

**La comunicación entre niveles.** El primario no requiere comunicación (descentralizado). El secundario usa comunicación lenta: latencias de 100 ms–1 s son aceptables. El terciario puede usar buses de campo (MODBUS, CANopen) o comunicaciones IP.

## 6 — Diseño iterativo: microrred híbrida 100 kW para datacenter

**Especificaciones del sistema:**
- Bus AC: 400 V, 50 Hz. Bus DC: 700 V.
- Cargas: 75 kW de servidores DC + 25 kW de cargas AC.
- Generación: 60 kWp de PV en DC, 50 kWh/200 kW de BESS en DC.
- Conexión a red AC disponible (PCC con interruptor automático).

**Paso 1 — dimensionado del ILC.** El ILC debe cubrir el peor caso: toda la carga DC sin generación PV (noche) más la exportación máxima del BESS al AC:

$$ P_{ILC,max}=75\,\text{kW}+\text{margen}=100\,\text{kW}\quad\Rightarrow\quad\text{elegimos }150\,\text{kW bidireccional} $$

**Paso 2 — lazo de tensión DC del ILC.** Se elige \( \alpha_{cv}=2\pi\cdot200\,\text{Hz} \) para el lazo de tensión DC:

$$ C_{dc,min}=P_{ILC,max}/(\alpha_{cv}\cdot V_{dc}^2\cdot\Delta_{V_{dc}})=100\,000/(1257\times700^2\times0.05)\approx 3.2\,\text{mF} $$

Se elige \( C_{dc}=5\,\text{mF} \). Con esto el rizado de tensión ante un escalón de 50 kW es \( \Delta V_{dc}\approx(50\,000)/(5\times10^{-3}\times1257\times700)\approx11\,\text{V}\) (1.6 %).

**Paso 3 — verificación de la estabilidad CPL.** La potencia crítica de la CPL sin amortiguamiento activo:

$$  P_{crit}=\frac{C_{dc}\,V_{dc}^2}{2L_{cable}}\bigg|_{L=0.5\,\text{mH}}=\frac{5\times10^{-3}\times700^2}{2\times5\times10^{-4}}=2\,450\,\text{kW}\gg100\,\text{kW}\quad\checkmark $$

El bus DC es estable en lazo abierto. El amortiguamiento activo eleva adicionalmente el margen.

**Paso 4 — droop del BESS en DC.** Para que \( V_{dc} \) no caiga más del 3% a plena potencia del BESS:

$$ k_d=\frac{\Delta V_{dc,max}}{P_{BESS,max}}=\frac{0.03\times700}{100\,000}=2.1\times10^{-4}\,\text{V/W} $$

**Paso 5 — autonomía en modo isla.** Con 50 kWh y una carga mínima de 25 kW (solo servidores críticos en modo isla), la autonomía sin PV es \( t=50\,\text{kWh}/25\,\text{kW}=2\,\text{h} \). Con PV a plena irradiación (\( G=1\,\text{kW/m}^2 \)), el PV cubre las 75 kW de carga DC sin usar el BESS ni la red.

<div class="cfig"><img src="figuras/microrred-hibrida-ac-dc-analisis.png" alt="análisis completo de la microrred híbrida AC/DC"><div class="cap">Panel (a): diagrama de la arquitectura con bus AC (azul), bus DC (naranja) e ILC. Panel (b): flujos de potencia durante un día solar típico: el PV cubre la carga DC en las horas centrales y el excedente carga el BESS; la red cubre el déficit nocturno. Panel (c): tensión del bus DC ante un escalón de +50 kW, con y sin amortiguamiento activo; sin AD las oscilaciones son significativas. Panel (d): frecuencia del bus AC tras la desconexión de red; el droop primario provoca una caída permanente que el secundario restaura en ~2 s.</div></div>

## Cuándo y por qué se usa
En instalaciones con fuerte componente DC (PV, baterías, cargas electrónicas) y necesidad de
conexión AC: data centers, edificios, buques, microrredes rurales. Reduce etapas de conversión y
mejora eficiencia frente a una arquitectura puramente AC.

## Procedimiento de diseño (genérico)
1. Define topología: nº de buses, ubicación de fuentes/cargas, nº de ILC.
2. Diseña el primario de cada subred (droop AC y [[droop-dc|DC]]).
3. Diseña la estrategia del ILC (igualar droops normalizados) y sus límites de potencia.
4. Coordina con el [[control-jerarquico-microrred|control jerárquico]] (secundario/terciario).
5. Verifica estabilidad del bus DC con cargas CPL/pulsantes y transiciones de modo.

## Ejemplo de código
```python
def ilc_power(w, Vdc, w0, Vdc0, dW_max, dVdc_max, Kp):
    soc_ac = (w - w0)/dW_max            # carga normalizada AC
    soc_dc = (Vdc - Vdc0)/dVdc_max      # carga normalizada DC
    return Kp*(soc_ac - soc_dc)         # potencia a transferir por el ILC

def droop_dc_bess(Vdc, Vdc0, kd, P_bess_prev, dt, tau_d=0.02):
    """Droop DC con filtrado de primer orden."""
    P_ref = (Vdc0 - Vdc) / kd          # referencia de potencia por droop
    P_bess = P_bess_prev + dt/tau_d*(P_ref - P_bess_prev)
    return P_bess
```

## Parámetros y valores típicos
Desviaciones normalizadas de droop ±1 a plena carga. Bus DC 350–800 V (BT). ILC dimensionado al
máximo intercambio esperado entre subredes.
Droop DC: \( k_d = 2\text{–}5\% \) de \( V_{dc}^* \) a plena potencia.

## Errores comunes
- ILC sin normalizar los droops → reparto AC/DC desequilibrado.
- Despreciar la dinámica CPL del bus DC con cargas de data center.
- No definir prioridades de carga ni la transición isla↔red del ILC.
- Dimensionar el condensador DC solo para el rizado PWM, ignorando el escalón de carga (debe cubrir ambos).

## Conceptos relacionados
- [[convertidor-vsc]] · [[dinamica-bus-dc]] · [[droop-dc]] · [[control-jerarquico-microrred]] · [[carga-pulsante-datacenter-ia]]

## Referencias
- Loh et al., *Autonomous Operation of Hybrid Microgrid With AC and DC Subgrids*, IEEE TPEL 2013.
- Nejabatkhah, Li, *Overview of Power Management Strategies of Hybrid AC/DC Microgrid*, IEEE TPEL 2015.
