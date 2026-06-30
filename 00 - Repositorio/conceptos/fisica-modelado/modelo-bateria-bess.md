---
titulo: Modelo de batería y sistema BESS
slug: modelo-bateria-bess
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: []
objetivos: [modelar la dinámica eléctrica de una batería y dimensionar un BESS]
tags: [bateria, bess, soc, thevenin, degradacion, almacenamiento, intermedio, modelado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-30
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

**Degradación (simplificada):** el estado de salud SoH disminuye con los ciclos y el tiempo; la
resistencia interna \( R_0 \) aumenta y \( Q_{nom} \) cae. Para control de servicios de red
(droop por SoC): un droop adaptativo \( R_d=f(SoC) \) equilibra el uso entre baterías.

**Arquitectura BESS:**
- Bus DC → convertidor bidireccional DC/DC (*boost/buck*) → batería (desacopla tensión de batería
  variable del bus DC).
- Bus DC → VSC ([[convertidor-vsc]]) → red AC.
- La gestión de SoC y límites de potencia/corriente es responsabilidad del BMS (Battery Management
  System), que limita las referencias del control.

<div class="cfig"><img src="figuras/modelo-bateria-bess-pulso.png" alt="respuesta de tension de la bateria a un pulso de corriente"><div class="cap">Respuesta del modelo Thevenin 1-RC a un pulso de descarga: al aplicar corriente, la tensión cae instantáneamente por la resistencia óhmica $R_0$ y luego sigue bajando con la constante $\tau_{RC}$ por la difusión; al cesar el pulso ocurre lo inverso. Un modelo solo resistivo (sin RC) no captura esa cola, relevante para dimensionar el convertidor.</div></div>

## 1 — El modelo Thévenin \( V_t=OCV-I\,R_{int} \) desde la malla equivalente
La celda se modela como una fuente interna (la tensión química \( OCV \)) en serie con una impedancia que representa todas las pérdidas. La tensión en bornes que ve el convertidor es lo que queda tras la caída en esa impedancia.

**Paso 1 — circuito equivalente.** En descarga, la celda es una fuente \( OCV(SoC) \) en serie con la resistencia óhmica \( R_0 \) y el par \( R_1\,C_1 \) de difusión. La corriente \( I \) (positiva en descarga) circula por la malla; la tensión de salida \( V_t \) es la de la fuente menos las caídas en serie.

**Paso 2 — Kirchhoff de tensiones en la malla.** Recorriendo la malla desde la fuente a los bornes, se restan la caída óhmica \( I\,R_0 \) y la tensión del condensador de difusión \( V_{RC} \):

$$ V_t=OCV(SoC)-I\,R_0-V_{RC} $$

**Paso 3 — el término de difusión es de primer orden.** El par \( R_1\,C_1 \) responde a un escalón de corriente con constante \( \tau_{RC}=R_1 C_1 \). Su ecuación de estado (corriente del condensador \( C_1\dot V_{RC}=I-V_{RC}/R_1 \), multiplicada por \( R_1 \)):

$$ \tau_{RC}\,\dot V_{RC}=I\,R_1-V_{RC} $$

En **régimen permanente** (\( \dot V_{RC}=0 \)) queda \( V_{RC}=I R_1 \), y agrupando ambas resistencias \( R_{int}=R_0+R_1 \) se recupera la forma compacta de la definición:

$$ \boxed{\;V_t=OCV(SoC)-I\,R_{int}\;} $$

La cola transitoria entre el salto óhmico inmediato (\( I R_0 \)) y este valor final (\( I R_{int} \)) es la que dibuja la figura del pulso: un modelo puramente resistivo se saltaría esa cola de constante \( \tau_{RC} \), relevante para dimensionar el convertidor.

## 2 — El SoC por integración de corriente (coulomb counting)
**Paso 1 — definición del estado de carga.** El SoC es la fracción de carga disponible respecto a la capacidad nominal \( Q_{nom} \) (en culombios, o Ah). Si \( q(t) \) es la carga remanente:

$$ SoC(t)=\frac{q(t)}{Q_{nom}} $$

**Paso 2 — la corriente es el flujo de carga.** Por definición de corriente, \( I=-dq/dt \) en descarga (la carga remanente disminuye al entregar corriente). Con la eficiencia coulómbica \( \eta_c \) que contabiliza las pérdidas de carga:

$$ \frac{dq}{dt}=-\eta_c\,I $$

**Paso 3 — derivar el SoC.** Dividiendo por \( Q_{nom} \) constante:

$$ \boxed{\;\dot{SoC}=-\frac{\eta_c\,I}{Q_{nom}}\;} $$

**Paso 4 — integrar para obtener el SoC.** Resolviendo la EDO desde un valor inicial conocido:

$$ SoC(t)=SoC(0)-\frac{\eta_c}{Q_{nom}}\int_0^t I(\tau)\,d\tau $$

De ahí el nombre *coulomb counting*: se integra (se "cuenta") la carga que entra y sale. Su debilidad es que es un **integrador puro**: cualquier sesgo en la medida de \( I \) (offset del sensor) se acumula y hace **derivar** la estimación con el tiempo, lo que obliga a recalibrar (p.ej. en SoC conocidos, como plena carga) o a corregir con un filtro de Kalman que usa también \( V_t \) del modelo Thévenin del apartado anterior.

## Cuándo y por qué se usa
Para modelar el bus DC de un BESS, diseñar los lazos de carga/descarga, los servicios de
frecuencia/inercia ([[servicios-red-soporte]]) y el [[droop-dc|droop DC]] con equilibrio de SoC
entre baterías en paralelo.

## Procedimiento de diseño (genérico)
1. Parametriza el modelo Thevenin (\( R_0,R_1,\tau_{RC} \)) con datos de la hoja de datos o
   identificación (HPPC test).
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
```

## Parámetros y valores típicos
Li-ion: \( R_0\approx0.5\text{–}5 \) mΩ/celda; C-rate 0.5–2C continuo, 3–5C pulso; ciclos 2000–6000
(LFP > NMC); tensión celda 2.5–4.2 V. BESS de red: 0.5–4 h de descarga.

## Errores comunes
- Usar un modelo puramente resistivo (sin RC) → no captura la dinámica de difusión (rizado de tensión
  en pulsos, relevante para dimensionar el convertidor).
- Ignorar el límite de C-rate en el control (puede degradar la batería o disparar el BMS).
- Asumir \( OCV \) lineal con SoC (la curva es muy no lineal en los extremos).

## Conceptos relacionados
- [[dinamica-bus-dc]] · [[droop-dc]] · [[control-tension-bus-dc]] · [[servicios-red-soporte]] · [[sistema-por-unidad]]

## Referencias
- Tremblay, Dessaint, *Experimental Validation of a Battery Dynamic Model*, IEEE TVT 2009.
- Plett, *Battery Management Systems*, Artech House 2015.
