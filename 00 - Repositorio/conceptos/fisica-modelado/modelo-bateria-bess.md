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
fecha_actualizacion: 2026-06-09
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
