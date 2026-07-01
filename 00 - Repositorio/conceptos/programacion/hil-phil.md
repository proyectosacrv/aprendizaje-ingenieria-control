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
