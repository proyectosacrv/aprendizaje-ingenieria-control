---
titulo: Control de tensión del bus DC
slug: control-tension-bus-dc
categoria: control
tipo: tecnica
nivel: intermedio
proyectos: []
objetivos: [mantener constante la tensión del bus DC regulando el intercambio de potencia]
tags: [bus-dc, lazo-externo, balance-energia, rectificador-activo, back-to-back, intermedio]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-09
relacionados: [control-cascada, dinamica-bus-dc, convertidor-vsc, controlador-pid, estabilidad-bus-dc-cpl]
referencias:
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
  - "Blaabjerg et al., Overview of Control and Grid Synchronization, IEEE TIE 2006"
---

## Definición
Lazo **externo** que regula la tensión del condensador del bus DC a su referencia, generando la
**referencia de corriente activa** \( i_d^* \) (o de potencia) para el lazo interno de corriente.
Es el lazo que cierra el balance de energía en rectificadores activos y convertidores back-to-back.

## Fundamento teórico
El bus DC es un integrador de potencia (ver [[dinamica-bus-dc]]). En términos de energía
\( E=\tfrac12 C v_{dc}^2 \):
$$ \frac{dE}{dt}=\tfrac12 C\frac{d(v_{dc}^2)}{dt}=P_{in}-P_{out} $$
La planta \( v_{dc}\!\leftarrow\!P \) es **no lineal** (aparece \( v_{dc}^2 \)). Dos enfoques:
- **Linealizar** en torno a \( V_{dc0} \): \( C V_{dc0}\,\dot{\tilde v}_{dc}=\tilde P \) → planta
  integradora \( 1/(C V_{dc0}\,s) \), se cierra con un PI.
- Controlar **\( v_{dc}^2 \)** (la energía) como variable: la planta se vuelve **lineal exacta**
  \( \tfrac{C}{2}\,\dot{(v_{dc}^2)}=P \).

Con tensión de red alineada al eje d (\( e_q=0 \)), \( P\approx \tfrac32 e_d i_d \), así que el PI
de tensión produce \( i_d^* \). El **feedforward** de la potencia de carga \( P_{out} \) acelera el
rechazo. La **separación de bandas** es crítica: el lazo de tensión debe ser bastante más lento que
el de corriente (factor ~5–10) y, en monofásico, más lento que el rizado de \( 2\omega \).

## Cuándo y por qué se usa
En el lado red de cualquier rectificador activo / convertidor back-to-back (el del usuario), en
STATCOM con almacenamiento, y en general cuando el bus DC alimenta una carga y hay que mantener su
tensión pese a perturbaciones de potencia.

## Procedimiento de diseño (genérico)
1. Modela el bus (\( C \), \( V_{dc0} \)) y linealiza, o usa \( v_{dc}^2 \) como variable.
2. Diseña el lazo interno de corriente primero ([[desacoplo-dq]], [[control-cascada]]).
3. Sintoniza el PI de tensión con \( \omega_{v}\approx(1/5\text{–}1/10)\,\omega_{c,i} \).
4. En monofásico/desequilibrio, filtra o haz \( \omega_v < 2\omega \) (evitar realimentar el rizado
   de 100 Hz como referencia de corriente).
5. Añade feedforward de \( P_{out} \) y **anti-windup** ([[anti-windup]]) al límite de \( i_d^* \).

## Ejemplo de aplicación real
**Problema:** Convertidor back-to-back lado red, \( C=10\,\text{mF} \), \( V_{dc0}=1.2\,\text{kV} \), carga de 500 kW. El lazo de corriente ya diseñado croza a \( f_{ci}=1\,\text{kHz} \). Diseñar el lazo de tensión DC.

Planta (usando \( v_{dc}^2 \) como variable): \( P\to\tfrac{C}{2}\dot{(v_{dc}^2)} \), ganancia \( 2/(Cs) \). Ancho de banda objetivo: \( f_{cv}=f_{ci}/5=200\,\text{Hz} \), \( \omega_{cv}=1257\,\text{rad/s} \). PI: \( K_{pv}=C\,\omega_{cv}/2=0.01\times1257/2=6.3\,\text{(W/V}^2\text{)/...} \); aplicando la fórmula en la base de \( v_{dc}^2 \) y \( P \). Con feedforward de carga: ante un escalón de carga del 10 % (50 kW), la caída de \( V_{dc} \) se reduce de 22 V a 6 V (factor 3.7 de mejora). Si \( \omega_{cv} \) se sube a 500 Hz: el rizado de \( 2\times50=100\,\text{Hz} \) del bus se realimenta y distorsiona la corriente de red — este es el límite superior para \( f_{cv} \).

## Ejemplo de código
```python
def dc_voltage_loop(vdc_ref, vdc, P_load, ed, pi_v, C):
    # control sobre energia (planta lineal): error en vdc^2
    e = vdc_ref**2 - vdc**2
    P_ref = pi_v(e) + P_load                 # feedforward de carga
    id_ref = (2/3)*P_ref/max(ed, 1e-3)       # referencia de corriente activa
    return id_ref
```

## Parámetros y valores típicos
Ancho de banda del lazo de tensión: 10–50 Hz (muy por debajo del de corriente). Rizado de
\( v_{dc} \) admisible 1–2 %. \( V_{dc} > 2\sqrt2\,V_{LL}/\sqrt3 \) para no saturar la modulación.

## Errores comunes
- Lazo de tensión demasiado rápido → realimenta el rizado de \( 2\omega \) y distorsiona la corriente.
- Tratar la planta como lineal lejos de \( V_{dc0} \) sin usar \( v_{dc}^2 \).
- Olvidar anti-windup en el límite de \( i_d^* \) (saturación durante arranques/huecos).
- Ignorar que una carga CPL añade impedancia negativa ([[estabilidad-bus-dc-cpl]]).

## Conceptos relacionados
- [[dinamica-bus-dc]] · [[control-cascada]] · [[convertidor-vsc]] · [[desacoplo-dq]] · [[estabilidad-bus-dc-cpl]]

## Referencias
- Yazdani, Iravani, 2010.
- Blaabjerg et al., *Overview of Control and Grid Synchronization*, IEEE TIE 2006.
