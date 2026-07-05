---
titulo: Hardware-in-the-loop (HIL y PHIL)
slug: hil-phil
categoria: programacion
tipo: metodo
nivel: intermedio
proyectos: []
objetivos: [validar control y hardware contra un modelo de planta en tiempo real]
tags: [hil, phil, tiempo-real, validacion, simulacion, fpga, intermedio, programacion]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-01
relacionados: [niveles-validacion, simulacion-conmutada, discretizacion-controladores, pruebas-validacion, medicion-impedancia-inyeccion]
referencias:
  - "Bélanger, Venne, Paquin, The What, Where and Why of Real-Time Simulation, IEEE PES 2010"
  - "Lauss et al., Characteristics and Design of Power Hardware-in-the-Loop Simulations, IEEE TIE 2016"
---

## Definición
Técnica de validación en la que un **modelo de planta** se ejecuta en un simulador de **tiempo real**
y se conecta al sistema bajo prueba. En **HIL** se prueba el **controlador real** (señales de bajo
nivel); en **PHIL** (power HIL) se conecta **hardware de potencia real** mediante un amplificador,
intercambiando potencia con la planta simulada.

## Fundamento teórico
- **Tiempo real:** el solver debe completar cada paso \( \Delta t \) **antes** del siguiente tick
  (sin *overruns*). Modelos de convertidor exigen \( \Delta t \) de µs → se usan FPGA para la
  conmutación y CPU para la red.
- **HIL (control):** el simulador emula la planta (sensores → controlador → PWM de vuelta). Valida
  firmware, protecciones, lógica de fallo y secuencias sin riesgo ni hardware de potencia.
- **PHIL (potencia):** se cierra un lazo **físico** de potencia. El acoplamiento entre la planta
  simulada y el equipo real introduce un lazo con retardo del amplificador y del paso de cálculo →
  problemas de **estabilidad y exactitud**. El método de interfaz (Interface Algorithm) más común,
  *Ideal Transformer Model* (ITM), es estable si
  $$ \left|\frac{Z_{HW}}{Z_{sim}}\right|<1\ \text{(en la región crítica)} $$
  es decir, depende del cociente de impedancias real/simulada (mismo espíritu que el
  [[medicion-impedancia-inyeccion|criterio de impedancia]]); se estabiliza con filtros/compensación
  en la interfaz.

Encaja en la pirámide de [[niveles-validacion]]: modelo offline → HIL de control → PHIL → campo.

<div class="cfig"><img src="figuras/hil-phil-lazo.png" alt="lazo de HIL y PHIL contra simulador en tiempo real"><div class="cap">El modelo de planta corre en un simulador de tiempo real que debe completar cada paso antes del siguiente tick (sin overruns). En HIL se cierra el lazo de señal con el controlador real (sensores→control→PWM) para validar firmware y protecciones; en PHIL se cierra además un lazo de potencia real con un amplificador, cuya estabilidad depende del cociente de impedancias real/simulada.</div></div>

## 1 — El lazo HIL: señales y retardos de interfaz
**Paso 1 — ciclo de un paso HIL.** En cada paso de tiempo \( \Delta t \) el simulador en tiempo real ejecuta la secuencia:

1. **ADC:** las salidas analógicas de la planta simulada (tensiones, corrientes) se convierten a digital con retardo \( T_{ADC}\approx1\text{–}5\,\mu\text{s} \).
2. **Cómputo del controlador:** el DSP/FPGA real procesa la medida y calcula la acción de control. Tiempo de cómputo \( T_{comp}\approx5\text{–}50\,\mu\text{s} \).
3. **DAC:** la señal de control (PWM o referencia) se convierte a analógico con retardo \( T_{DAC}\approx1\text{–}5\,\mu\text{s} \).
4. **Modelo:** el simulador avanza la planta un paso \( \Delta t \).

El **retardo total de interfaz** es \( T_d=T_{ADC}+T_{comp}+T_{DAC} \).

**Paso 2 — efecto del retardo en el lazo de control.** Un retardo puro \( e^{-T_d s} \) en el lazo de corriente reduce el margen de fase en:

$$ \Delta\phi = T_d\cdot\omega_c\cdot\frac{180°}{\pi} $$

Para \( \omega_c=2\pi\times1000 \) rad/s y \( T_d=100\,\mu\text{s} \): \( \Delta\phi=2\pi\times1000\times10^{-4}\times57.3°=36° \). Si el margen nominal era 72°, queda en 36° — por debajo del límite de 45°. El HIL detecta esto sin riesgo.

$$ \boxed{T_d\cdot\omega_c<\frac{\pi}{4}\;\Rightarrow\; T_d < \frac{1}{4f_c}} $$

Para \( f_c=1\,\text{kHz} \): \( T_d < 250\,\mu\text{s} \). Valores típicos de HIL (50–150 µs) cumplen con margen.

## 2 — Estabilidad del PHIL: condición sobre el retardo y la impedancia de interfaz
**Paso 1 — el bucle de potencia PHIL.** En PHIL se cierra un lazo físico de potencia entre el amplificador real y la planta simulada. El amplificador impone la tensión \( V_{HW} \) y mide la corriente \( I_{HW} \). La planta simulada recibe \( I_{HW} \) y devuelve la tensión de referencia \( V_{ref} \) al amplificador. El retardo total del lazo introduce una fase que puede inestabilizar el acoplamiento.

**Paso 2 — criterio de estabilidad del ITM (Ideal Transformer Model).** Para el algoritmo ITM, el lazo PHIL es estable si la impedancia del hardware real \( Z_{HW} \) es menor que la de la planta simulada \( Z_{sim} \) en la banda crítica:

$$ \left|\frac{Z_{HW}(j\omega)}{Z_{sim}(j\omega)}\right| < 1\quad\forall\omega \text{ en la banda de interés} $$

El retardo \( T_d \) añade fase \( e^{-j\omega T_d} \) y transforma la condición en una restricción de estabilidad más estricta a altas frecuencias. La compensación estándar es añadir un filtro en la interfaz que anticipe fase (lead) para compensar el retardo.

$$ \boxed{|Z_{HW}/Z_{sim}|<1 \;\wedge\; T_d<T_{crit}\;\Rightarrow\;\text{PHIL estable}} $$

## Cuándo y por qué se usa
Para validar el control diseñado (sobre [[simulacion-conmutada|modelo conmutado]]) en condiciones
realistas y peligrosas (faltas, huecos, pérdida de red) antes de hardware; certificación de grid
codes; y prueba de equipos de potencia reales contra redes/cargas difíciles de montar físicamente.

## Procedimiento de diseño (genérico)
1. Discretiza el modelo de planta para tiempo real ([[discretizacion-controladores]]); reparte
   CPU/FPGA según constantes de tiempo.
2. Verifica ausencia de *overruns* y la fidelidad frente al modelo offline.
3. HIL: conecta el controlador real; prueba protecciones, fallos y grid codes.
4. PHIL (si aplica): elige Interface Algorithm, comprueba estabilidad (cociente de impedancias),
   añade compensación/filtros.
5. Documenta cobertura y discrepancias ([[pruebas-validacion]]).

## Ejemplo de código
```python
# Lazo de tiempo real (pseudocodigo): respetar el deadline dt
while running:
    t0 = now()
    y = plant_model.step(u, dt)          # planta en tiempo real
    u = controller.step(y)               # HIL: controlador real
    assert now() - t0 < dt               # sin overrun
    wait_until(t0 + dt)
```

## Parámetros y valores típicos
Paso de tiempo: 0.5–2 µs (FPGA, conmutación), 10–50 µs (CPU, red). Latencia de amplificador PHIL
decenas de µs. Objetivo: 0 overruns y error vs offline < pocos %.

## Errores comunes
- *Overruns* no detectados → resultados sin sentido (el "tiempo real" deja de serlo).
- PHIL sin analizar estabilidad de la interfaz (cociente de impedancias) → oscilación o daño.
- Validar solo en nominal y no los casos límite (faltas, pérdida de red) que justifican el HIL.

## Conceptos relacionados
- [[niveles-validacion]] · [[simulacion-conmutada]] · [[discretizacion-controladores]] · [[pruebas-validacion]] · [[medicion-impedancia-inyeccion]]

## Referencias
- Bélanger, Venne, Paquin, *The What, Where and Why of Real-Time Simulation*, IEEE PES 2010.
- Lauss et al., *Characteristics and Design of Power Hardware-in-the-Loop Simulations*, IEEE TIE 2016.

## 3 — Arquitectura HiL: distribución CPU/FPGA y retardos de bucle

La arquitectura típica de un banco HiL separa la simulación en dos dominios:

**FPGA (tiempo real estricto, \( \Delta t \sim 0.5\text{–}2\,\mu\text{s} \)):** resuelve la conmutación de los interruptores, los modelos de inductores y condensadores durante los estados ON/OFF. Usa aritmética de punto fijo y modelos VHDL compilados. Sin FPGA, el bucle completo tardaría más de 10 µs y se perdería la dinámica de conmutación.

**CPU (tiempo real, \( \Delta t \sim 10\text{–}50\,\mu\text{s} \)):** resuelve la dinámica de red (líneas, transformadores, cargas), la lógica de protecciones y la interfaz con el usuario. Usa punto flotante de doble precisión.

**Interfaz FPGA↔CPU:** comunicación por DMA o bus paralelo con retardo \( < 1\,\mu\text{s} \). El retardo total del bucle HIL es:

$$ T_d = T_{ADC} + T_{comp,DSP} + T_{DAC} \approx 50\text{–}150\,\mu\text{s} $$

Este retardo reduce el margen de fase del lazo de corriente. Para \( T_d = 100\,\mu\text{s} \) y \( f_c = 1\,\text{kHz} \): pérdida de fase \( \Delta\phi = 100\times10^{-6} \times 2\pi\times10^3 \times 57.3° = 36° \). El diseño debe tener PM > 45° + 36° = 81° para sobrevivir al HiL — lo que a menudo lleva a reducir \( f_c \) o a añadir compensación de retardo.

**Verificación de overruns:** el simulador en tiempo real monitorea que cada paso se complete en el tiempo disponible. Un overrun (paso que tarda más de \( \Delta t \)) invalida el resultado. La métrica de calidad es el porcentaje de pasos sin overrun: debe ser 100% en operación nominal.

## 4 — PHiL e interfaz de potencia: compensación del retardo del amplificador

En PHiL, el amplificador lineal de potencia introduce un retardo propio \( T_{amp} \approx 100\text{–}500\,\mu\text{s} \) (función de su ancho de banda, típicamente 2–10 kHz). Este retardo, combinado con el retardo del simulador, forma el retardo total del lazo de potencia:

$$ T_{d,total} = T_{sim} + T_{amp} + T_{ADC} $$

**Compensación del retardo del amplificador:** se añade un filtro de adelanto de fase (lead) en la señal de referencia del amplificador para cancelar parcialmente el retardo:

$$ C_{comp}(s) = \frac{1 + s\,T_{amp}}{1 + s\,\alpha\,T_{amp}},\quad \alpha < 1 $$

Este filtro da ganancia de fase \( \Delta\phi_{max} = \arcsin\left(\frac{1-\alpha}{1+\alpha}\right) \) centrada en \( \omega_{max} = 1/(T_{amp}\sqrt{\alpha}) \).

**Impedancia de interfaz estabilizante:** además del retardo, la impedancia propia del amplificador \( Z_{amp}(j\omega) \) debe cumplir el criterio ITM:

$$ |Z_{amp}(j\omega)| < |Z_{sim}(j\omega)| \quad \Rightarrow \quad Z_{sim} \text{ debe ser mayor (red más débil en la simulación)} $$

Si la planta simulada es una red muy fuerte (SCR alto, \( Z_{sim} \) pequeña), el amplificador con \( Z_{amp} \) finita no cumple el criterio. La solución es añadir una inductancia virtual en serie en el modelo de red simulado.

## 5 — Casos de prueba: cobertura por estándar

El HiL permite ejecutar de forma segura y reproducible los casos de prueba más peligrosos:

**LVRT (Low Voltage Ride Through):** hueco de tensión al 0–30% de \( V_n \) durante 150–600 ms (según IEC 61727, IEEE 1547). El convertidor debe permanecer conectado e inyectar corriente reactiva. En hardware real, este ensayo requiere un generador de huecos de €50k+; en HiL es una condición de simulación.

**Islanding (detección de isla):** pérdida de la red con una carga local resonante en el PCC. El convertidor debe detectar el islanding en < 2 s (IEEE 1547) y desconectarse (anti-islanding) o pasar a modo isla (GFM). La Non-Detection Zone (NDZ) se barre sistemáticamente en HiL.

**Protecciones de sobrecorriente/sobretensión:** falta trifásica, bifásica y monofásica a distintas distancias eléctricas del convertidor. El current limiting debe activarse en < 100 µs y mantener la corriente < 1.5 p.u.

**Criterios de aceptación por estándar:**
- IEC 61727: LVRT hasta 0% de \( V_n \) durante 150 ms.
- IEEE 1547-2018: ramp rate < 10% de \( P_n \)/min, frequency ride-through ±3 Hz.
- VDE-AR-N 4110: Q(U) droop, inyección de reactiva en falta.

## 6 — Certificación: reducción de coste y tiempo vs ensayo de tipo

La certificación de convertidores de red (IEC 62690, IEC 61727, IEEE 1547) requiere ensayos de tipo en laboratorio acreditado. El HiL reduce el tiempo y coste de estos ensayos de varias formas:

**Reducción de tiempo:** los casos de prueba se ejecutan automáticamente (scripts); una suite de 50 casos tarda 4 horas en HiL vs 2 semanas en laboratorio de alta potencia.

**Reducción de coste:** un banco HiL cuesta €50k–€200k; un laboratorio de ensayos de tipo cobra €10k–€50k por campaña. Si el diseño tiene 3–5 iteraciones antes de aprobar, el HiL amortiza en 2–3 años.

**Límites del HiL:** los ensayos de EMC (emisiones conducidas y radiadas), la calefacción térmica real y el envejecimiento de componentes no se pueden simular en HiL — requieren el equipo real. Por eso el HiL precede pero no sustituye completamente al ensayo de tipo.

$$ \boxed{\text{Ahorro}_{HiL} \approx N_{iteraciones} \times \left(\text{Coste}_{lab} - \text{Coste}_{HiL}/N_{años}\right)} $$

<div class="cfig"><img src="../figuras/hil-phil-analisis.png" alt="arquitectura HiL, LVRT en HiL vs real, efecto retardo en estabilidad y cobertura de pruebas"><div class="cap">Arquitectura HiL con distribución CPU/FPGA y retardos de bucle. LVRT en HiL: comparativa con ensayo real mostrando la coincidencia de formas de onda. El retardo de 100 µs reduce el margen de fase en 36°. Cobertura de pruebas HiL vs campo: el HiL cubre 85% de los casos a 5% del coste.</div></div>

## 7 — Implementacion Python: bucle HiL en tiempo libre (pseudocodigo)

En Python no es posible hacer tiempo real estricto (el GIL y el sistema operativo no lo garantizan), pero se puede implementar un bucle de co-simulacion SiL que emula el comportamiento del HiL para pruebas de verificacion de firmware:

```python
import numpy as np
from scipy.integrate import solve_ivp

class PlantaSimulada:
    """Modelo de planta para co-simulacion tipo HiL."""
    def __init__(self, L=2e-3, R=0.1, Vdc=400, dt=50e-6):
        self.L = L; self.R = R; self.Vdc = Vdc; self.dt = dt
        self.x = np.array([0.0, 0.0])  # [id, iq]

    def step(self, u_d, u_q):
        """Avanza la planta un paso dt dado el vector de tension de control."""
        def rhs(t, x):
            id_, iq_ = x
            did = (u_d - self.R * id_ + 50 * 2*np.pi * self.L * iq_) / self.L
            diq = (u_q - self.R * iq_ - 50 * 2*np.pi * self.L * id_) / self.L
            return [did, diq]
        sol = solve_ivp(rhs, (0, self.dt), self.x, method='LSODA',
                        rtol=1e-6, atol=1e-8)
        self.x = sol.y[:, -1]
        return self.x.copy()


class ControladorPI:
    """Controlador PI dq para el lazo de corriente (firmware simplificado)."""
    def __init__(self, Kp=4.0, Ki=200.0, dt=50e-6, umax=600.0):
        self.Kp = Kp; self.Ki = Ki; self.dt = dt; self.umax = umax
        self.xi_d = 0.0; self.xi_q = 0.0

    def update(self, id_ref, iq_ref, id_meas, iq_meas):
        """Un paso del controlador PI con anti-windup clamping."""
        ed = id_ref - id_meas; eq = iq_ref - iq_meas
        u_d = self.Kp * ed + self.xi_d
        u_q = self.Kp * eq + self.xi_q
        u_d_sat = np.clip(u_d, -self.umax, self.umax)
        u_q_sat = np.clip(u_q, -self.umax, self.umax)
        # clamping anti-windup
        if u_d == u_d_sat:
            self.xi_d += self.Ki * ed * self.dt
        if u_q == u_q_sat:
            self.xi_q += self.Ki * eq * self.dt
        return u_d_sat, u_q_sat


def run_hil_loop(t_end=0.1, id_ref=1.0, iq_ref=0.0, Td_steps=1):
    """
    Co-simulacion tipo HiL: planta avanza dt, controlador recibe con Td de retardo.
    Td_steps: numero de pasos de retardo del bucle HIL.
    """
    dt = 50e-6
    N = int(t_end / dt)
    planta = PlantaSimulada(dt=dt)
    ctrl = ControladorPI(dt=dt)

    # buffer de retardo para emular Td
    u_buffer = [(0.0, 0.0)] * (Td_steps + 1)

    t_hist, id_hist, iq_hist = [], [], []
    for k in range(N):
        t = k * dt
        # la planta recibe la accion de control con retardo Td
        u_d, u_q = u_buffer[0]
        id_m, iq_m = planta.step(u_d, u_q)

        # el controlador calcula la nueva accion
        u_d_new, u_q_new = ctrl.update(id_ref, iq_ref, id_m, iq_m)

        # actualizar buffer de retardo
        u_buffer.pop(0)
        u_buffer.append((u_d_new, u_q_new))

        t_hist.append(t); id_hist.append(id_m); iq_hist.append(iq_m)

    return np.array(t_hist), np.array(id_hist), np.array(iq_hist)

# Comparar con y sin retardo HIL
t0, id0, _ = run_hil_loop(Td_steps=0)  # sin retardo (SiL)
t1, id1, _ = run_hil_loop(Td_steps=2)  # con 2 pasos de retardo (HiL tipico)
# Analizar: el retardo reduce el PM y puede causar oscilaciones si PM < 0
```

## 8 — Verificacion de overruns en tiempo real

En un sistema HiL real, el simulador en tiempo real debe completar cada paso \( \Delta t \) antes del siguiente tick del reloj hardware. La verificacion de overruns es critica:

```c
/* Pseudocodigo C en DSP/RTOS */
void ISR_Timer_100us(void) {
    uint32_t t_start = get_time_us();

    /* 1. Leer ADC */
    float id_meas = adc_read(CH_ID);
    float iq_meas = adc_read(CH_IQ);

    /* 2. Ejecutar controlador */
    float ud = pi_update(&ctrl_d, id_ref, id_meas);
    float uq = pi_update(&ctrl_q, iq_ref, iq_meas);

    /* 3. Escribir PWM */
    pwm_set_duty(ud, uq);

    /* 4. Verificar overrun */
    uint32_t t_elapsed = get_time_us() - t_start;
    if (t_elapsed > TS_US) {
        overrun_count++;
        /* alarma o log */
    }
}
```

El porcentaje de overruns debe ser 0% durante toda la suite de pruebas. Incluso un 0.01% de overruns (1 de cada 10000 ciclos) puede causar inestabilidad intermitente difícil de reproducir.

**Margen de tiempo recomendado:** el tiempo de ejecucion del ISR debe ser < 70-80% del periodo de muestreo, dejando un 20-30% de margen para variaciones de latencia del sistema operativo o del bus de datos.

## 9 — Relacion entre HIL, PHiL y la piramide de validacion

El HIL y el PHiL no son alternativas sino niveles complementarios de la escalera de validacion:

- **HIL** verifica que el algoritmo de control funciona correctamente en el hardware de control (DSP/FPGA) — validacion del firmware.
- **PHiL** verifica que el convertidor real (hardware de potencia) opera correctamente con la red emulada — validacion del hardware de potencia.
- **Ensayo de tipo** verifica que el sistema completo cumple los estandares en condiciones reales (EMC, temperatura, humedad) — certificacion.

Ninguno de los tres sustituye a los otros. La combinacion de los tres cubre el 95% de los requisitos de certificacion a un coste total inferior al ensayo de tipo completo sin preparacion previa.
