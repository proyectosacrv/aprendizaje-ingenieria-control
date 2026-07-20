---
titulo: Modelo de batería y sistema BESS
slug: modelo-bateria-bess
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: []
objetivos: [modelar la dinámica eléctrica de una batería y dimensionar un BESS]
tags: [bateria, bess, soc, thevenin, ocv, lifep04, degradacion, almacenamiento, droop-dc, inercia-virtual, intermedio, modelado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-03
relacionados: [dinamica-bus-dc, droop-dc, control-tension-bus-dc, servicios-red-soporte, sistema-por-unidad]
referencias:
  - "Tremblay, Dessaint, Experimental Validation of a Battery Dynamic Model, IEEE TVT 2009"
  - "Plett, Battery Management Systems Vol.1-2, Artech House 2015"
---

## Definición
Modelo eléctrico equivalente de una celda electroquímica (Li-ion, LFP, etc.) y su integración como
sistema BESS (Battery Energy Storage System) con convertidor DC/DC o DC/AC para inyección a red o
soporte de bus DC.

## Fundamento teórico
**Modelo de Thevenin de 1 RC** (suficiente para control):
$$ V_{bat}=OCV(SoC)-I\,R_0-V_{RC},\qquad \tau_{RC}\dot V_{RC}=I\,R_1-V_{RC} $$
con:
- \( OCV(SoC) \): tensión en circuito abierto, función no lineal del estado de carga.
- \( R_0 \): resistencia interna (pérdidas óhmicas, calentamiento, caída en pulsos).
- \( R_1,C_1=\tau_{RC}/R_1 \): par RC de difusión (constante \( \tau_{RC}\sim10\text{–}100 \) s).

**Estado de carga (SoC):**
$$ \dot{SoC}=-\frac{\eta_c\,I}{Q_{nom}},\quad SoC\in[0,1] $$
con \( \eta_c \) eficiencia coulómbica y \( Q_{nom} \) capacidad nominal (Ah). SoC se estima por
integración de corriente (*coulomb counting*, deriva con tiempo) o por filtro de Kalman sobre \( V_{bat} \).

<div class="cfig"><img src="figuras/modelo-bateria-bess-pulso.png" alt="respuesta de tension de la bateria a un pulso de corriente"><div class="cap">Respuesta del modelo Thevenin 1-RC a un pulso de descarga: al aplicar corriente, la tensión cae instantáneamente por la resistencia óhmica $R_0$ y luego sigue bajando con la constante $\tau_{RC}$ por la difusión; al cesar el pulso ocurre lo inverso. Un modelo solo resistivo (sin RC) no captura esa cola, relevante para dimensionar el convertidor.</div></div>

## 1 — El modelo Thévenin \( V_t=OCV-I\,R_{int} \) desde la malla equivalente

La celda se modela como una fuente interna (la tensión química \( OCV \)) en serie con una impedancia que representa todas las pérdidas. La tensión en bornes que ve el convertidor es lo que queda tras la caída en esa impedancia.

**Paso 1 — circuito equivalente.** En descarga, la celda es una fuente \( OCV(SoC) \) en serie con la resistencia óhmica \( R_0 \) y el par \( R_1\,C_1 \) de difusión. La corriente \( I \) (positiva en descarga) circula por la malla; la tensión de salida \( V_t \) es la de la fuente menos las caídas en serie.

**Paso 2 — Kirchhoff de tensiones en la malla.** Recorriendo la malla desde la fuente a los bornes, se restan la caída óhmica \( I\,R_0 \) y la tensión del condensador de difusión \( V_{RC} \):
$$ V_t=OCV(SoC)-I\,R_0-V_{RC} $$

**Paso 3 — el término de difusión es de primer orden.** El par \( R_1\,C_1 \) responde a un escalón de corriente con constante \( \tau_{RC}=R_1 C_1 \). Su ecuación de estado (corriente del condensador \( C_1\dot V_{RC}=I-V_{RC}/R_1 \), multiplicada por \( R_1 \)):
$$ \tau_{RC}\,\dot V_{RC}=I\,R_1-V_{RC} $$

En **régimen permanente** (\( \dot V_{RC}=0 \)) queda \( V_{RC}=I R_1 \), y agrupando ambas resistencias \( R_{int}=R_0+R_1 \) se recupera la forma compacta:
$$ \boxed{\;V_t=OCV(SoC)-I\,R_{int}\;} $$

La cola transitoria entre el salto óhmico inmediato (\( I R_0 \)) y este valor final (\( I R_{int} \)) es la que dibuja la figura del pulso: un modelo puramente resistivo se saltaría esa cola de constante \( \tau_{RC} \), relevante para dimensionar el convertidor.

## 2 — El modelo de SOC: integración de coulomb y su deriva

**Paso 1 — definición del estado de carga.** El SoC es la fracción de carga disponible respecto a la capacidad nominal \( Q_{nom} \). Si \( q(t) \) es la carga remanente en culombios:
$$ SoC(t)=\frac{q(t)}{Q_{nom}} $$

**Paso 2 — la corriente es el flujo de carga.** Por definición de corriente, \( I=-dq/dt \) en descarga (la carga remanente disminuye al entregar corriente). Con la eficiencia coulómbica \( \eta_c \):
$$ \frac{dq}{dt}=-\eta_c\,I $$

**Paso 3 — derivar el SoC.**
$$ \boxed{\;\dot{SoC}=-\frac{\eta_c\,I}{Q_{nom}}\;} $$

**Paso 4 — la deriva del integrador.** Resolviendo la EDO desde un valor inicial conocido:
$$ SoC(t)=SoC(0)-\frac{\eta_c}{Q_{nom}}\int_0^t I(\tau)\,d\tau $$
De ahí el nombre *coulomb counting*: se integra (se "cuenta") la carga que entra y sale. Su debilidad es que es un **integrador puro**: cualquier sesgo en la medida de \( I \) (offset del sensor ADC) se acumula y hace **derivar** la estimación, obligando a recalibrar periódicamente o a corregir con un filtro de Kalman.

**Corrección por OCV.** En reposo (corriente cero, tras al menos 30 minutos de reposo para que la difusión decaiga), la tensión en bornes iguala a \( OCV(SoC) \). Midiendo \( V_t \) y aplicando la inversa: \( SoC=f^{-1}(V_t) \). Esta "ancora" periódica combate la deriva del coulomb counting.

## 3 — El modelo equivalente de circuito (ECM) con 2 RC

El modelo de un único RC captura la dinámica de difusión dominante, pero para aplicaciones de alta precisión (EKF, dimensionado térmico) se añade un segundo par \( R_2\text{-}C_2 \) que captura la dinámica lenta de la difusión de iones en el electrodo sólido.

**Paso 1 — el circuito 2RC.** La tensión terminal es:
$$ V_t = OCV(SoC) - R_0\,I - V_{RC1} - V_{RC2} $$

donde \( V_{RC1} \) (constante \( \tau_1=R_1 C_1\sim1\text{–}10\,\text{s} \)) captura la dinámica de interfaz de electrodo, y \( V_{RC2} \) (constante \( \tau_2=R_2 C_2\sim100\text{–}1000\,\text{s} \)) captura la difusión sólida.

**Paso 2 — ecuaciones de estado.** Con vector de estado \( \mathbf{x}=[SoC,\,V_{RC1},\,V_{RC2}]^\top \):

$$ \dot{\mathbf{x}} = \underbrace{\begin{bmatrix}-\eta_c/Q_{nom} & 0 & 0 \\ 0 & -1/\tau_1 & 0 \\ 0 & 0 & -1/\tau_2\end{bmatrix}}_{\mathbf{A}}\mathbf{x} + \underbrace{\begin{bmatrix}1/Q_{nom} \\ R_1/\tau_1 \\ R_2/\tau_2\end{bmatrix}}_{\mathbf{B}}I_{\text{sign}} $$

donde \( I_{\text{sign}}=-I \) en descarga (convenio positivo en descarga). La salida:
$$ y = V_t = OCV(x_1) - R_0\,I - x_2 - x_3 = h(\mathbf{x},I) $$

**Paso 3 — identificación de parámetros.** Se realiza el ensayo HPPC (Hybrid Pulse Power Characterization):
1. Pulso de descarga a 1C durante 18 s → la caída instantánea mide \( R_0 \).
2. La recuperación en los primeros 10 s → ajusta \( R_1,\tau_1 \).
3. La cola lenta de recuperación (hasta 60–300 s) → ajusta \( R_2,\tau_2 \).
4. Repetir a varios SoC (10 %, 20 %,…, 90 %) para obtener la dependencia de SoC.

Valores típicos para LFP a 25 °C: \( R_0=2\,\text{m}\Omega \), \( R_1=1.5\,\text{m}\Omega \), \( C_1=3000\,\text{F} \) (\( \tau_1=4.5\,\text{s} \)), \( R_2=0.8\,\text{m}\Omega \), \( C_2=12500\,\text{F} \) (\( \tau_2=10\,\text{s} \)) — por celda de 100 Ah.

## 4 — La estimación del SOC: coulomb counting y filtro de Kalman extendido (EKF)

El coulomb counting integra la corriente pero **deriva** con el tiempo por offsets del sensor. El EKF usa el modelo ECM para corregir la estimación usando la medición de tensión.

**Paso 1 — el EKF: predicción.** En cada paso de tiempo \( T_s \):

*Predicción del estado:*
$$ \hat{\mathbf{x}}_{k|k-1} = \mathbf{A}_d\,\hat{\mathbf{x}}_{k-1|k-1} + \mathbf{B}_d\,I_k $$
*Predicción de la covarianza del error:*
$$ \mathbf{P}_{k|k-1} = \mathbf{A}_d\,\mathbf{P}_{k-1|k-1}\,\mathbf{A}_d^\top + \mathbf{Q}_{noise} $$

donde \( \mathbf{A}_d,\mathbf{B}_d \) son la versión discreta del modelo (Euler o ZOH), y \( \mathbf{Q}_{noise} \) es la covarianza del ruido de proceso (incertidumbre en el modelo).

**Paso 2 — el EKF: actualización con la medición \( V_t \).**

La función de salida \( h \) es no lineal (por la curva OCV). Se linealiza:
$$ \mathbf{H}_k = \frac{\partial h}{\partial \mathbf{x}}\bigg|_{\hat{\mathbf{x}}_{k|k-1}} = \begin{bmatrix}\frac{dOCV}{dSoC}\bigg|_{\hat{SoC}} & -1 & -1\end{bmatrix} $$

*Ganancia de Kalman:*
$$ \mathbf{K}_k = \mathbf{P}_{k|k-1}\,\mathbf{H}_k^\top \left(\mathbf{H}_k\,\mathbf{P}_{k|k-1}\,\mathbf{H}_k^\top + R_{meas}\right)^{-1} $$

*Actualización del estado:*
$$ \hat{\mathbf{x}}_{k|k} = \hat{\mathbf{x}}_{k|k-1} + \mathbf{K}_k\!\left(V_{t,meas} - h(\hat{\mathbf{x}}_{k|k-1},I_k)\right) $$

*Actualización de la covarianza:*
$$ \mathbf{P}_{k|k} = (I-\mathbf{K}_k\,\mathbf{H}_k)\,\mathbf{P}_{k|k-1} $$

**Paso 3 — la clave del EKF: \( dOCV/dSoC \).** En LFP, la curva OCV es casi plana en el 20–80 % de SoC, por lo que \( dOCV/dSoC\approx0.05\,\text{V/pu} \) en esa zona. La ganancia de Kalman en \( SoC \) se hace pequeña: la corrección por tensión tiene poco efecto. El EKF confía más en el modelo de corriente (coulomb counting) en la zona plana, y confía más en la tensión en los extremos de SoC donde la pendiente de OCV es mayor. Esto es matemáticamente correcto: la información de la tensión sobre el SoC es máxima donde la curva tiene mayor pendiente.

## 5 — El envejecimiento del BESS: degradación de capacidad y resistencia

La batería pierde capacidad y aumenta su resistencia interna con el uso. Entender el envejecimiento es esencial para planificar los reemplazos y proteger la garantía.

**Paso 1 — el modelo de degradación por ciclos.** La capacidad remanente tras \( n \) ciclos (a un DOD fijo):
$$ Q_{nom}(n) = Q_0 \cdot \left(1 - k_{deg}\cdot n\right) $$
donde \( k_{deg} \) depende del DOD, temperatura y C-rate. Para LFP a DOD=80 %, 25 °C, C-rate=1C: \( k_{deg}\approx10^{-5} \) por ciclo → vida útil de 3000 ciclos (EOL en \( Q<80\%Q_0 \)).

**Paso 2 — el método Rainflow para contar ciclos.** La corriente de una batería en servicio real es irregular (no ciclos completos). El algoritmo Rainflow (norma ASTM E1049) descompone la señal de SoC en semicyclos y los pondera por su amplitud (DOD). Ciclos a DOD=20 % dañan menos que ciclos a DOD=80 %. La fórmula de Ahrens-Doerffel:
$$ k_{deg}(DOD) = A\cdot e^{B\cdot DOD} $$
con \( A \) y \( B \) calibrados empíricamente para cada química.

**Paso 3 — estrategias de control para maximizar vida útil.**
- **Limitar el SOC de operación:** operar entre [20 %, 90 %] en lugar de [0 %, 100 %] reduce el DOD efectivo → multiplica la vida por 2–3×.
- **Limitar el C-rate de carga (CC/CV):** cargar rápido (>1C) genera calor y acelera la degradación del electrodo. El modo CV (tensión constante hacia el final de la carga) reduce el C-rate.
- **Control de temperatura:** el BMS desclasifica la corriente máxima por encima de 40 °C y por debajo de 0 °C. La ventana óptima es 15–35 °C.
- **Droop adaptativo por SOC:** en paralelo de BESS, el que tiene más SoC descarga más, equilibrando el desgaste entre unidades.

**Paso 4 — EOL y análisis económico.** Cuando \( Q_{nom}<80\%Q_0 \), el BESS ya no cumple la especificación de energía. El coste por ciclo:
$$ \text{LCOE}_{BESS}=\frac{C_{CAPEX}}{N_{ciclos}\cdot E_{descarga\_util\_por\_ciclo}} $$
Para un BESS de 1 MWh a 200 k€/MWh, con 3000 ciclos a DOD=80 %: LCOE ≈ 83 €/MWh.

## 6 — Diseño iterativo: BESS 1 MWh, carga de 0.5 MW durante 1 h

**Especificaciones:** \( E_{bess}=1\,\text{MWh} \), \( P=500\,\text{kW} \), \( R_0=5\,\text{m}\Omega \) (por string), \( R_1=3\,\text{m}\Omega \), \( C_1=10000\,\text{F} \), \( V_{nom}=800\,\text{V} \) (bus DC), \( SoC_0=80\,\% \).

**Paso 1 — corriente de descarga.**
$$ I_{discharge}=\frac{P}{V_{bat}}\approx\frac{500\times10^3}{800}=625\,\text{A} $$

**Paso 2 — caída de tensión en \( R_0 \).**
$$ \Delta V_{R0} = I\cdot R_0 = 625\times5\times10^{-3}=3.125\,\text{V}\;\;(<0.4\%\text{ de }800\,\text{V}) $$

La caída en \( R_1 \) en régimen permanente (tras varios \( \tau_1 \)):
$$ \Delta V_{R1,ss} = I\cdot R_1 = 625\times3\times10^{-3}=1.875\,\text{V} $$

Tensión en bornes en permanente: \( V_t = OCV(80\%) - 3.125 - 1.875 \approx OCV(80\%) - 5\,\text{V} \). Para LFP, \( OCV(80\%)\approx3.33\,\text{V/celda} \); en un pack de 800 V con \( N_s=250 \) celdas en serie:
$$ V_t = 250\times3.33 - 5 = 832.5 - 5 = 827.5\,\text{V} $$

**Paso 3 — energía disipada en \( R_0 \).**
$$ P_{disipada} = I^2\cdot R_0 = 625^2\times5\times10^{-3}=1953\,\text{W}=1.95\,\text{kW} $$
En 1 hora: \( E_{disipada}=1.95\,\text{kWh}\;\;(0.39\%\text{ de la energía descargada}) \).

**Paso 4 — SOC final tras 1 h de descarga a 500 kW.**
$$ \Delta SoC = \frac{P\cdot t}{E_{bess}}=\frac{500\,\text{kW}\times1\,\text{h}}{1000\,\text{kWh}}=0.5\;\;(50\%\text{ de SOC}) $$
$$ SoC_{final} = SoC_0 - \Delta SoC = 80\% - 50\% = 30\% $$
Dentro del rango útil [20 %, 90 %]. El BESS puede continuar hasta \( SoC=20\% \) antes de reducir potencia, dando 10 % de margen adicional (\( 0.10\times1000\,\text{kWh}=100\,\text{kWh} \) extra a potencia reducida).

<div class="cfig"><img src="figuras/modelo-bateria-bess-analisis.png" alt="4 paneles: OCV LiFePO4, respuesta impulso corriente, EKF vs coulomb counting, capacidad vs ciclos"><div class="cap">
(a) Curva OCV(SoC) de LiFePO4: la región central 20–80 % es casi plana (~3.30–3.35 V/celda), dificultando la estimación de SoC por tensión; los extremos tienen mayor pendiente. (b) Respuesta de \(V_t\) a un escalón de corriente de descarga: la caída instantánea por \(R_0\), la subida gradual por \(R_1\text{-}C_1\) (τ₁) y \(R_2\text{-}C_2\) (τ₂), y la recuperación al cesar la corriente. (c) EKF vs coulomb counting en 1 h de ciclo: el coulomb counting deriva ~5 % de SoC; el EKF lo corrige usando la información de tensión. (d) Capacidad residual \(Q_{nom}(n)/Q_0\) vs número de ciclos para DOD=40 %, 60 %, 80 %: el EOL al 80 % de capacidad ocurre antes con DOD mayor.
</div></div>

## 7 — La curva OCV(SOC) para LiFePO4

La curva \( OCV(SoC) \) es la relación entre la tensión en circuito abierto y el estado de carga. Cada química tiene su forma característica.

**Características del LiFePO4 (LFP):**
- Rango de tensión: 2.5 V (SoC=0) → 3.65 V (SoC=100 %).
- La curva tiene una región **muy plana** entre SoC=20 % y SoC=80 % (≈ 3.30–3.35 V), lo que dificulta la estimación de SoC por OCV en esa región.
- En los extremos (SoC < 10 % y SoC > 90 %) la curva es más inclinada → mejor resolución de la estimación.

**Linealización local.** Para pequeños excursiones alrededor de un punto de operación \( SoC_0 \):
$$ OCV(SoC)\approx OCV_0 + k_{oc}\cdot\Delta SoC, \qquad k_{oc}=\frac{dOCV}{dSoC}\bigg|_{SoC_0} $$
En la región plana central, \( k_{oc}\approx0.1\,\text{V/pu} \) (muy pequeño): un error de 50 mV en la medición de OCV produce un error de 0.5 pu (50 %) en la estimación de SoC. Por eso en LFP no basta el coulomb counting corregido por OCV: se usa un filtro de Kalman extendido que combina ambos.

**Efecto de la temperatura.** A \( T < 0°C \): la viscosidad del electrolito aumenta, la difusión se ralentiza (\( \tau_{RC} \) sube a cientos de segundos), y \( R_0 \) puede multiplicarse por 3–5×. A \( T > 45°C \): la degradación se acelera. El BMS limita la potencia fuera de la ventana [5–45 °C].

**Efecto del envejecimiento.** Con los ciclos, \( Q_{nom} \) disminuye (\( Q_{nom}(n)=Q_0\cdot(1-k_{deg}\cdot n) \)) y \( R_0 \) aumenta. El fin de vida se define típicamente en \( Q_{nom}<80\,\%Q_0 \) o \( R_0>2R_{0,new} \).

## 8 — El SoC por integración de corriente (coulomb counting)

*Este apartado desarrolla el Paso 4 del §2 con más detalle sobre la implementación práctica.*

**Implementación discreta.** En un sistema digital con paso \( T_s \):
$$ SoC_{k+1}=SoC_k - \frac{\eta_c\,I_k\,T_s}{Q_{nom}\cdot3600} $$
(el factor 3600 convierte de Ah a As = C). La eficiencia \( \eta_c \) es típicamente 0.99–0.995 para Li-ion.

**Fuentes de error y sus consecuencias:**
- **Offset del sensor de corriente:** \( \epsilon_I \) A → error de SoC que crece como \( \epsilon_I\,t/(Q_{nom}\cdot3600) \). Con \( \epsilon_I=0.5\,\text{A} \), \( Q_{nom}=200\,\text{Ah} \): error de 0.07 % por hora → 1.7 % en 24 h.
- **Ganancia del sensor:** error proporcional a la corriente, acumula más rápido en ciclos a alta potencia.
- **Incertidumbre en \( Q_{nom} \):** si la batería ha envejecido y \( Q_{nom,real}<Q_{nom,nominal} \), el SoC calculado infraestima el real → riesgo de sobredescarga.

## 9 — Control del BESS en microrred

El BESS puede operar en varios modos según el estado de la microrred y el nivel de SoC.

**Modo grid-following (GFL).** El convertidor del BESS inyecta la potencia de referencia \( (P^*, Q^*) \) fijada por el EMS (Energy Management System). El lazo de corriente del VSC sigue la referencia del EMS. Este modo asume que hay otra fuente (generador síncrono o VSC grid-forming) que impone la tensión y frecuencia de la microrred.

**Modo droop DC.** En bus DC compartido, el BESS aplica la característica droop:
$$ V_{dc}=V_{dc,0} - R_d\cdot I_{bess} $$
donde \( R_d \) es la resistencia de droop (Ω equivalentes, determina el reparto de carga entre baterías en paralelo). El droop adaptativo \( R_d=f(SoC) \) hace que las baterías con más SoC descarguen más rápido, equilibrando el desgaste.

**Límites de SoC (gestión BMS):**
- \( SoC < 20\,\% \): reducir potencia de descarga linealmente → cero descarga en \( SoC=10\,\% \).
- \( SoC > 90\,\% \): reducir potencia de carga linealmente → cero carga en \( SoC=95\,\% \).
- \( SoC < 10\,\% \) o corriente de batería \( > I_{max} \): apertura del contactor del BMS (protección hardware).

**Modo grid-forming (GFM) en isla.** El BESS puede actuar como GFM imponiendo \( V \) y \( f \) de la microrred en isla. La energía disponible es limitada por el SoC, de modo que el EMS debe equilibrar generación y carga. La inercia virtual \( H_{virtual}=E_{bess}/(2\cdot P_{rated}) \) equivalente aumenta la inercia eléctrica del sistema.

## 10 — Diseño iterativo: BESS 200 kWh/200 kW para soporte de frecuencia

**Especificaciones:** soporte de frecuencia primaria con \( H_{eq}=4\,\text{s} \) equivalente, tiempo de descarga 1 h, potencia \( P_{rated}=200\,\text{kW} \), química LiFePO4.

**Paso 1 — capacidad de energía.** Con 1 h de descarga a potencia nominal:
$$ E_{bess} = P_{rated}\times 1\,\text{h} = 200\,\text{kW}\times1\,\text{h} = 200\,\text{kWh} $$
Con ventana útil de SoC [20–90 %]: capacidad instalada \( E_{inst}=200/0.70=285\,\text{kWh} \). En celdas de 3.2 V nominal y 200 Ah por bloque: \( N_{celdas}=E_{inst}/(3.2\times200\times10^{-3})\approx445\,\text{celdas} \).

**Paso 2 — C-rate.** \( I_{max}=P_{rated}/V_{bat,nom}=200000/512\approx390\,\text{A} \). C-rate = 390 A / (200 Ah) = 1.95C → dentro del límite de 2C continuo para LFP. La temperatura aumentará ≈ 5–10 °C en descarga sostenida; el BMS debe gestionar el límite térmico.

**Paso 3 — inercia virtual equivalente.** La constante de inercia virtual que aporta el BESS como GFM en un sistema de \( S_{base}=10\,\text{MVA} \):
$$ H_{virtual}=\frac{E_{bess}}{S_{base}}=\frac{200\,\text{kWh}}{10000\,\text{kVA}}=0.02\,\text{h}=72\,\text{s} $$

En pu del sistema: \( H_{pu}=H_{virtual}/S_{base} \), relevante para calcular el \( df/dt \) que puede soportar el BESS en la respuesta inercial.

**Paso 4 — condensador de bus DC equivalente.** El BESS de 200 kWh a 800 V de bus DC se puede modelar como un condensador equivalente para análisis de dinámica de bus DC:
$$ C_{eq}=\frac{2\,E_{bess}}{V_{dc}^2}=\frac{2\times200\times3600\times10^3}{800^2}\approx2250\,\text{F} $$

Este valor de \( C_{eq} \) entra en el modelo de dinámica del bus DC ([[dinamica-bus-dc]]) con la constante de tiempo \( \tau_{bus}=R_{droop}\cdot C_{eq} \).


## 11 — Modelo eléctrico equivalente de Thevenin

El modelo de Thevenin de orden 1 resume la celda en tres parámetros extraíbles del datasheet o de un ensayo HPPC.

**Circuito equivalente.** En descarga, la tensión en bornes es:
$$ V_{batt} = E_{OCV}(SOC) - R_0\,i - R_1\!\left(1-e^{-t/\tau_1}\right)i $$

donde el término exponencial captura la respuesta transitoria de la difusión electroquímica. En régimen permanente (\( t\gg\tau_1 \)) la caída total es \( (R_0+R_1)\,i \).

**\( E_{OCV}(SOC) \): tensión en circuito abierto.** Función no lineal del SOC, típicamente modelada como polinomio de grado 5:
$$ E_{OCV}(SOC) = \sum_{k=0}^{5} a_k\,SOC^k $$
o bien como tabla de lookup interpolada. Para LiFePO4, la curva es casi plana entre 20 % y 80 % de SOC (~3.30–3.35 V/celda), lo que dificulta la estimación de SOC por tensión en esa zona.

**\( R_0 \): resistencia interna serie.** Causa la caída instantánea al aplicar corriente (efecto Joule directo). Valores típicos: 0.5–5 mΩ/celda para Li-ion. Aumenta con el envejecimiento y a bajas temperaturas.

**\( R_1,\,C_1 = \tau_1/R_1 \): rama RC de difusión.** Modela el transporte iónico en el electrodo. La constante \( \tau_1 \sim 10\text{–}100\,\text{s} \) es relevante para dimensionar el control: un PI que ignore esta dinámica verá el equivalente de un polo adicional.

**Modelo de orden 2.** Añadir una segunda rama \( R_2\text{-}C_2 \) (\( \tau_2 \sim 500\text{–}2000\,\text{s} \)) mejora la precisión a dinámica lenta (importante para el EKF y la estimación de SOC en carga sostenida):
$$ V_{batt} = E_{OCV}(SOC) - R_0\,i - V_{RC1} - V_{RC2} $$

## 12 — Estado de carga y degradación

**SOC por integración coulombiana.** La ecuación diferencial del SOC es:
$$ \dot{SOC} = -\frac{\eta_i\,i}{Q_{nom}} $$
donde \( \eta_i \) es la eficiencia coulombiana (típicamente 0.99–0.995 para Li-ion) y \( Q_{nom} \) la capacidad nominal en Ah. El SOC se obtiene integrando desde un valor inicial conocido.

**SOH (State of Health).** Relación entre la capacidad actual y la nominal:
$$ SOH = \frac{Q_{actual}}{Q_{nom,nuevo}} \times 100\% $$
Se considera fin de vida (\textit{EOL}) cuando \( SOH < 80\% \) o la resistencia interna supera el doble del valor inicial.

**Degradación calendárica vs cíclica.** La degradación calendárica ocurre incluso sin ciclos de carga (almacenamiento a SOC alto o temperatura elevada). La cíclica depende del DOD, C-rate y temperatura. La temperatura es el factor dominante en ambos tipos.

**Regla de Arrhenius simplificada.** Cada 10 °C de aumento de temperatura duplica aproximadamente la tasa de degradación:
$$ k_{deg}(T) \approx k_{deg,25°C} \cdot 2^{(T-25)/10} $$

**C-rate.** Se define como \( 1C = Q_{nom} \) (en amperios). Operar a C-rate bajo (0.5C) extiende significativamente la vida útil frente a ciclos a 2C: la energía de activación de la degradación crece con la densidad de corriente.

## 13 — Control del BESS: carga/descarga

El convertidor del BESS trabaja con dos lazos anidados de diferente ancho de banda.

**Lazo de corriente (rápido).** Sigue la referencia \( i_{ref} \) con un controlador PI cuyo ancho de banda es ~1 kHz. Es el lazo interno del VSC; su función de transferencia de lazo cerrado es aproximadamente de primer orden con constante \( \tau_{cl} = L/K_p \).

**Lazo de SOC (lento).** Mantiene el SOC dentro de la ventana útil \( [SOC_{min},\,SOC_{max}] \) ajustando la referencia de potencia enviada al lazo de corriente. Su ancho de banda es de segundos a minutos. La consigna de potencia viene del EMS (Energy Management System) y el lazo de SOC la recorta o limita según el estado de la batería.

**Protecciones implementadas en el BMS:**
- **Sobretemperatura:** desclasificación de corriente máxima por encima de 40 °C.
- **Sobretensión de celda:** corte de carga al superar \( V_{cell,max} \) (3.65 V en LFP).
- **Subtensión:** corte de descarga por debajo de \( V_{cell,min} \) (2.5 V en LFP).
- **Sobrecorriente:** apertura del contactor hardware si \( i > I_{max} \).

**Estrategias de operación.** En la red, el BESS puede operar en modo:
- *Peak shaving*: recorta las puntas de demanda diaria reduciendo el cargo por potencia contratada.
- *Frequency response*: inyecta o absorbe potencia en proporción a la desviación de frecuencia (\( \Delta f \)).
- *Arbitraje energético*: carga en horas de bajo precio (exceso solar/eólico) y descarga en horas de alto precio.

## 14 — Integración en microrred y dimensionado

**Potencia del BESS.** Determinada por el requerimiento de regulación de frecuencia. Si la microrred tiene una carga de \( P_{carga} \) y se especifica un droop \( \Delta f / \Delta P \):
$$ P_{BESS} = \frac{\Delta P_{regulacion}}{\Delta f/f_0} $$

Típicamente el BESS cubre el 5–15 % de la potencia instalada para servicios de frecuencia primaria.

**Energía.** La energía almacenada se dimensiona según el tiempo de autonomía requerido:
$$ E = P_{BESS} \cdot t_{autonomia} $$
Para servicios de red: 15 min a 1 h (regulación de frecuencia), 1 a 4 h (peak shaving), >4 h (desplazamiento de energía).

**Temperatura y BMS.** El sistema de gestión térmica (BMS) impacta directamente en la capacidad disponible: a baja temperatura la resistencia interna sube y la capacidad efectiva cae. El BMS desclasifica la corriente máxima fuera de la ventana [5–45 °C].

**Cálculo de ejemplo.** Microrred industrial de 1 MW con un requerimiento de \( \pm 100\,\text{kW} \) de regulación durante 30 min:
$$ E_{BESS} = 100\,\text{kW} \times 0.5\,\text{h} = 50\,\text{kWh} $$
Con ventana útil de SOC del 70 %: capacidad instalada \( E_{inst} = 50/0.70 \approx 71.4\,\text{kWh} \). La potencia nominal del convertidor DC/AC debe ser al menos 100 kW con margen del 10–20 % para las pérdidas.

<div class="cfig"><img src="figuras/modelo-bateria-bess-analisis.png" alt="4 paneles: OCV LiFePO4, respuesta escalon corriente, SOC ciclo carga-descarga, degradacion vs temperatura"><div class="cap">
(a) Curva OCV(SOC) de Li-ion: polinomio cúbico típico; la tensión crece de ~3.0 V a ~4.0 V entre SOC=0 y SOC=100 %. (b) Respuesta de tensión ante un escalón de corriente de 50 A: caída instantánea por \(R_0\) y cola exponencial por la rama RC con \(\tau_1=10\,\text{s}\). (c) SOC en un ciclo de carga/descarga a corriente cuadrada: la integración coulombiana revela cómo el SOC oscila en torno al 50 % con los límites operativos al 20 % y 80 %. (d) Ciclos de vida útil en función de la temperatura: la regla de Arrhenius duplica la tasa de degradación cada 10 °C, pasando de ~3000 ciclos a 25 °C a menos de 1000 ciclos a 55 °C.
</div></div>

## Cuándo y por qué se usa
Para modelar el bus DC de un BESS, diseñar los lazos de carga/descarga, los servicios de
frecuencia/inercia y el droop DC con equilibrio de SoC entre baterías en paralelo.

## Procedimiento de diseño (genérico)
1. Parametriza el modelo Thevenin (\( R_0,R_1,\tau_{RC} \)) con datos de la hoja de datos o identificación (HPPC test).
2. Obtén la curva \( OCV(SoC) \) del fabricante.
3. Dimensiona capacidad: \( E_{bat}=P_{nom}\cdot t_{descarga} \); corriente máxima por C-rate.
4. Conecta al control de bus DC y define límites de corriente/SoC para el BMS.
5. Implementa estimación de SoC (integración o Kalman) y droop adaptativo si hay varias baterías.

## Ejemplo de código
```python
def battery_step(I, soc, Vrc, R0, R1, tau, Qnom, dt, ocv_fn):
    Vbat = ocv_fn(soc) - I*R0 - Vrc
    dsoc = -I/Qnom                         # coulomb counting (Ah -> fraccion)
    dVrc = (I*R1 - Vrc)/tau
    return Vbat, soc + dsoc*dt, Vrc + dVrc*dt

# OCV(SoC) LiFePO4 parametrizada
import numpy as np
SOC = np.linspace(0, 1, 200)
OCV = (3.20 + 0.30*SOC + 0.08*np.exp(-15*(SOC-0.05))
       - 0.08*np.exp(-15*(0.95-SOC)))
ocv_fn = lambda s: np.interp(s, SOC, OCV)
```

## Parámetros y valores típicos
Li-ion: \( R_0\approx0.5\text{–}5 \) mΩ/celda; C-rate 0.5–2C continuo, 3–5C pulso; ciclos 2000–6000
(LFP > NMC); tensión celda 2.5–4.2 V (NMC) / 2.5–3.65 V (LFP). BESS de red: 0.5–4 h de descarga. \( \tau_{RC} \) 10–100 s.

## Errores comunes
- Usar un modelo puramente resistivo (sin RC) → no captura la dinámica de difusión (rizado de tensión en pulsos, relevante para dimensionar el convertidor).
- Ignorar el límite de C-rate en el control (puede degradar la batería o disparar el BMS).
- Asumir \( OCV \) lineal con SoC (la curva es muy no lineal en los extremos y casi plana en el centro para LFP).
- No recalibrar el coulomb counting periódicamente → la deriva acumulada puede superar el 10 % en semanas.

## Conceptos relacionados
- [[dinamica-bus-dc]] · [[droop-dc]] · [[control-tension-bus-dc]] · [[servicios-red-soporte]] · [[sistema-por-unidad]]

## Referencias
- Tremblay, Dessaint, *Experimental Validation of a Battery Dynamic Model*, IEEE TVT 2009.
- Plett, *Battery Management Systems*, Artech House 2015.
