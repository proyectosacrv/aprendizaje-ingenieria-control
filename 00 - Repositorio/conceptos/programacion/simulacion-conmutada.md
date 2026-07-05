---
titulo: Simulación conmutada vs promediada
slug: simulacion-conmutada
categoria: programacion
tipo: metodo
nivel: intermedio
proyectos: []
objetivos: [validar el modelo promediado frente a la conmutación real del convertidor]
tags: [conmutada, promediado, switching, paso-fijo, validacion, intermedio, programacion]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-01
relacionados: [convertidor-vsc, integracion-edos-stiff, fft-analisis-espectral]
referencias:
  - "Mohan, Undeland, Robbins, Power Electronics, Wiley"
  - "Maksimovic et al., Modeling and Simulation of Power Electronic Converters, Proc. IEEE 2001"
---

## Definición
Comparación de dos niveles de modelo: la **simulación conmutada** (reproduce el encendido/apagado
real de los interruptores) y la **promediada** (sustituye la conmutación por los ciclos de trabajo
continuos). El método consiste en simular ambas y verificar que coinciden en la banda de interés.

## Fundamento teórico
- **Conmutada:** las funciones de conmutación \( s_x(t)\in\{0,1\}_ \) imponen la tensión de rama;
  la dinámica es lineal a tramos con **eventos** en cada cruce de la portadora PWM. Captura
  armónicos de conmutación, tiempos muertos y rizado, pero es **rígida** y cara (paso pequeño).
- **Promediada:** \( \langle v_x\rangle=d_x V_{dc} \); válida hasta \( \approx f_{sw}/2 \) (teorema
  de muestreo del promediado). Rápida, ideal para diseño de control y linealización
  ([[linealizacion-numerica]]).

La equivalencia se cuantifica comparando la **componente fundamental y la dinámica de baja
frecuencia**; las diferencias por encima de \( f_{sw}/2 \) son esperables (el promediado no las
modela). Un **paso de integración** demasiado grande en la conmutada "pierde" instantes de
conmutación y falsea el rizado: regla práctica \( \Delta t \lesssim \dfrac{1}{20\,f_{sw}} \), o
usar detección de eventos.

<div class="cfig"><img src="figuras/simulacion-conmutada-rizado.png" alt="corriente conmutada con rizado frente a la promediada suave"><div class="cap">El modelo promediado sustituye la conmutación por el ciclo de trabajo y da la trayectoria suave de baja frecuencia; el conmutado reproduce el encendido/apagado real y añade el rizado triangular a $f_{sw}$. Ambos coinciden en la dinámica de baja frecuencia (la que importa para el control); las diferencias por encima de $f_{sw}/2$ son esperables y normales.</div></div>

## 1 — Paso máximo de integración en la simulación conmutada
**Paso 1 — la conmutación como evento.** En cada periodo de portadora PWM \( T_{sw}=1/f_{sw} \) hay uno o dos instantes de cruce (flancos de subida/bajada del comparador). Si el integrador avanza con un paso \( h > T_{sw}/2 \), puede saltarse el instante exacto del flanco, produciendo un **aliasing de la conmutación**: el rizado calculado no es el real y las pérdidas de conmutación son incorrectas.

**Paso 2 — criterio de Nyquist aplicado al integrador.** Para resolver el contenido frecuencial del PWM hasta \( f_{sw} \), el paso debe ser al menos la mitad del periodo de la componente más rápida relevante. Siendo conservador con un factor 10 de sobremuestreo:

$$ \boxed{h_{\max} < \frac{1}{10\,f_{sw}}} $$

Para \( f_{sw}=5\,\text{kHz} \): \( h_{\max}<1/(10\times5000)=20\,\mu\text{s} \). En la práctica se usa \( h=1\,\mu\text{s} \) para no perder los flancos (1/5000 del periodo de la componente fundamental, 1/5 del periodo de \( f_{sw} \)).

**Paso 3 — comparación con el modelo promediado.** El promediado trabaja con el ciclo de trabajo \( d(t) \) continuo; no tiene flancos que resolver. Su step máximo lo impone la dinámica del control (\( h_{prom}\approx1/(10\,f_{control}) \)). Para \( f_{control}=1\,\text{kHz} \): \( h_{prom}\lesssim100\,\mu\text{s} \), es decir **100 veces mayor** que el de la conmutada. Esto explica por qué el promediado es mucho más rápido de simular.

$$ \boxed{\frac{h_{conmutada}}{h_{promediada}}\approx\frac{f_{control}}{10\,f_{sw}}=\frac{1}{100}\quad(\text{para }f_{sw}/f_{control}=10)} $$

## 2 — Error por paso excesivo: aliasing de la conmutación
**Paso 1 — modelo de la señal de conmutación.** La función de conmutación \( s(t)\in\{0,1\} \) a \( f_{sw} \) tiene componentes espectrales a \( n\cdot f_{sw}\pm k\cdot f_1 \) para \( n,k \) enteros. Si el paso \( h \) no resuelve el cruce de la portadora, las componentes en \( f_{sw} \) se pliegan (aliasing) sobre frecuencias bajas, apareciendo como perturbaciones espurias en la corriente de control.

**Paso 2 — cuantificación.** Un error de \( \Delta t_{flanco}\approx h \) en la posición del flanco equivale a un error de ciclo de trabajo de \( \Delta d\approx h\cdot f_{sw} \). La tensión de error resultante es \( \Delta v=V_{dc}\,\Delta d=V_{dc}\,h\,f_{sw} \). Para que este error sea \( <0.1\,\% \) de \( V_{dc} \): \( h < 0.001/f_{sw}=1/(1000\,f_{sw}) \) — en la práctica la detección de eventos (solver con zero-crossing) es más eficiente que reducir \( h \) hasta ese nivel.

## Cuándo y por qué se usa
Para **validar** que el modelo de control diseñado sobre el promediado funciona con conmutación
real, antes de pasar a HIL/hardware; para cuantificar rizado y armónicos (con
[[fft-analisis-espectral]]); y para detectar efectos no capturados por el promediado (tiempo muerto,
saturación de modulación).

## Procedimiento de diseño (genérico)
1. Implementa el modelo promediado (ciclos de trabajo) y el conmutado (portadora + comparador).
2. Fija el paso: conmutada con \( \Delta t \le 1/(20 f_{sw}) \) o solver con eventos; promediada con
   paso mayor (puede ser **stiff** → ver [[integracion-edos-stiff]]).
3. Aplica el **mismo** control y la misma perturbación a ambos.
4. Compara: fundamental, transitorios de baja frecuencia (deben coincidir) y espectro (FFT).
5. Si divergen en baja frecuencia, revisa el promediado (tiempo muerto, no linealidades, saturación).

## Ejemplo de aplicación real
**Problema:** VSC con filtro LCL, \( f_{sw}=5\,\text{kHz} \). Comparar la corriente de red del modelo promediado (\( \Delta t=50\,\mu\text{s} \)) contra la conmutada (\( \Delta t=1\,\mu\text{s} \)) ante un escalón de referencia de corriente.

En baja frecuencia (<500 Hz): la corriente de ambos modelos sigue idéntica trayectoria — la diferencia en amplitud de fundamental es <0.3 %. En alta frecuencia: el modelo conmutado muestra rizado triangular de ~1.8 A de pico a pico a 5 kHz (corriente del inductor) más armónicos a \( f_{sw}\pm50 \). El promediado no los tiene. Divergencia esperable y normal. Si la fundamental difiere >2 % en régimen permanente, hay un efecto no modelado (tiempo muerto, caída de tensión en IGBTs) que el promediado ignora. En ese caso: cuantificar la distorsión con [[fft-analisis-espectral]] y decidir si añadirla al promediado como feedforward de compensación.

## Ejemplo de código
```python
def pwm_switch(d, carrier):              # 1 rama: comparador PWM
    return 1.0 if d > carrier else 0.0   # s_x in {0,1}
# conmutada: dt <= 1/(20*fsw); promediada: v_x = d*Vdc (paso mayor)
```

## Parámetros y valores típicos
Conmutada: \( \Delta t \) = 0.1–1 µs (o eventos). Promediada: \( \Delta t \) = 1–50 µs. La
diferencia de baja frecuencia entre ambas debe ser < 1–2 %.

## Errores comunes
- Paso fijo grande en la conmutada → rizado y pérdidas mal calculados (aliasing de la conmutación).
- Esperar que el promediado reproduzca armónicos de conmutación (no puede, por definición).
- Comparar con controles o condiciones iniciales distintas entre ambos modelos.

## Conceptos relacionados
- [[convertidor-vsc|modelo promediado]] · [[integracion-edos-stiff]] · [[fft-analisis-espectral]]

## Referencias
- Mohan, Undeland, Robbins, *Power Electronics*.
- Maksimovic et al., *Modeling and Simulation of Power Electronic Converters*, Proc. IEEE 2001.

## 3 — Simulación nivel conmutación: dinámica rígida y solver adecuado

La simulación conmutada modela los interruptores como elementos binarios \( s_x(t) \in \{0,1\} \): cuando el comparador PWM cruza la portadora triangular, el estado del interruptor cambia instantáneamente y la topología del circuito se modifica.

Esto genera un sistema **rígido** (stiff): la constante de tiempo de la corriente a través del inductor durante la conducción (\( \tau = L/R \sim \text{ms} \)) coexiste con los transitorios de conmutación (\( \sim \text{ns–}\mu\text{s} \)) y con el rizado triangular a \( f_{sw} \). Para un integrador explícito (RK45, Euler forward), el paso máximo es:

$$ h_{max} < \frac{2}{|\lambda_{max}|} \approx \frac{1}{10\,f_{sw}} $$

Para \( f_{sw} = 5\,\text{kHz} \): \( h_{max} < 20\,\mu\text{s} \). En la práctica se usa \( h = 1\,\mu\text{s} \) (factor 20 de margen). La integración de 1 segundo de operación requiere \( 10^6 \) pasos, frente a los \( 10^4 \) del modelo promediado: ratio 100×.

Un solver con **detección de eventos** (zero-crossing del comparador) es más eficiente: avanza con pasos grandes entre conmutaciones y reduce el paso solo en la vecindad del flanco. PLECS y Simulink/Simscape implementan esto automáticamente.

## 4 — Evento de conmutación: detección precisa del cruce del comparador

El instante de conmutación \( t^* \) ocurre cuando la señal de modulación \( m(t) \) cruza la portadora \( c(t) \): \( m(t^*) = c(t^*) \).

**Detección por bisección:** partiendo de un intervalo \( [t_a, t_b] \) donde se sabe que hay un cruce (\( f(t_a) \cdot f(t_b) < 0 \) con \( f(t) = m(t) - c(t) \)), el método de bisección reduce el intervalo a la mitad en cada iteración:

$$ t_{mid} = \frac{t_a + t_b}{2};\quad \text{si } f(t_a)\cdot f(t_{mid}) < 0 \Rightarrow t_b = t_{mid}, \text{ si no } t_a = t_{mid} $$

Tras \( n \) iteraciones, el error en el instante de conmutación es \( |t^* - t_{mid}| < (t_b - t_a)/2^n \). Para pasar de un intervalo de 1 µs a precisión de 1 ps: \( n = \log_2(10^6) \approx 20 \) iteraciones. Esta precisión sub-nanosegundo es innecesaria para control pero importante para cálculo de pérdidas de conmutación.

**Error de ciclo de trabajo por paso de integración fijo:** un error \( \Delta t \) en el instante del flanco equivale a un error de ciclo de trabajo \( \Delta d = \Delta t \cdot f_{sw} \) y a una tensión de error \( \Delta V = V_{dc} \cdot \Delta d \). Para \( \Delta t = h = 1\,\mu\text{s} \), \( f_{sw} = 5\,\text{kHz} \): \( \Delta d = 0.005 \Rightarrow \Delta V = 0.5\,\%\, V_{dc} \). Aceptable para control; inaceptable para medición de THD con < 0.1% de error.

$$ \boxed{\Delta d = h \cdot f_{sw};\quad \Delta V = V_{dc} \cdot h \cdot f_{sw};\quad \text{para }h = 1\,\mu\text{s},\;f_{sw}=5\,\text{kHz}: \Delta V = 0.5\,\%\,V_{dc}} $$

## 5 — Herramientas y paso de tiempo: PLECS, Simulink, Python

**PLECS (Plexim):** simulador especializado en electrónica de potencia. Usa detección de eventos para los conmutadores; el modelo de componentes incluye pérdidas de conmutación (mapa de \( E_{on}, E_{off} \) vs \( I, V \)). Estándar de facto en la industria de convertidores.

**Simulink/Simscape:** Simscape Electrical incluye componentes de electrónica de potencia con event detection. El bloque Specialized Power Systems (antiguo SimPowerSystems) usa paso variable con detección de conmutación. Integración con Simulink facilita el diseño de control y la generación de código.

**Python (scipy.integrate):** implementación manual con `solve_ivp` usando `events` para detectar los cruces. Más flexible para modelos propios pero más lento que los simuladores especializados:

```python
from scipy.integrate import solve_ivp

def comparator_event(t, x, m_func, carrier_func):
    return m_func(t) - carrier_func(t)
comparator_event.terminal = False
comparator_event.direction = 0  # cruces en ambas direcciones

sol = solve_ivp(rhs, (0, T_sim), x0, method='LSODA',
                events=comparator_event, max_step=1e-5)
```

**Regla práctica:** \( T_{sim} \leq T_{sw}/100 \) para resolver el rizado correctamente sin detección de eventos; con detección de eventos, el paso medio puede ser 10× mayor manteniendo la misma precisión.

## 6 — Compromiso precisión vs velocidad: cuándo usar cada modelo

La elección entre modelo conmutado y promediado es una decisión de ingeniería, no de perfección:

| Objetivo | Modelo recomendado | Paso típico |
|---|---|---|
| Diseño del controlador | Promediado linealizado | 50–100 µs |
| Validación de transitorios grandes | Promediado no lineal | 10–50 µs |
| Verificar THD, rizado, armónicos | Conmutado | 0.1–1 µs |
| Pérdidas de conmutación | Conmutado con mapa de pérdidas | 0.1–1 µs |
| HIL (tiempo real) | Conmutado en FPGA | 0.5–2 µs |

El modelo promediado es **100× más rápido** que el conmutado (ratio de pasos de tiempo). Para un estudio de Monte Carlo con 500 realizaciones de 10 s cada una, el promediado tarda minutos; el conmutado tardaría días. Por eso el diseño siempre se hace en el promediado y el conmutado solo se usa para **validación final** y para obtener el espectro de armónicos con [[fft-analisis-espectral]].

$$ \boxed{\frac{t_{CPU,\text{conmutado}}}{t_{CPU,\text{promediado}}} \approx \frac{h_{promediado}}{h_{conmutado}} \approx \frac{f_{sw}/10}{f_{sw}/100} = 10 \times \frac{f_{sw}}{f_{control}}} $$

<div class="cfig"><img src="../figuras/simulacion-conmutada-analisis.png" alt="señal conmutada vs promediada, error vs Tsim, coste computacional y comparativa simuladores"><div class="cap">Comparativa conmutado vs promediado: el conmutado reproduce el rizado a fsw; el promediado da la trayectoria suave. El error en la fundamental aumenta con el paso h (aliasing de la conmutación). El coste computacional del conmutado es ~100× mayor, justificado solo para validación final y cálculo de THD.</div></div>

## 7 — Implementacion Python: conmutado con eventos

```python
import numpy as np
from scipy.integrate import solve_ivp

def portadora_triangular(t, fsw):
    """Portadora triangular PWM: 0..1 en cada periodo Tsw."""
    Tsw = 1.0 / fsw
    phase = (t % Tsw) / Tsw
    return 2 * phase if phase < 0.5 else 2 * (1 - phase)

def rhs_conmutado(t, x, d_ref, L, R, Vdc, fsw):
    """Buck: x=[iL]. carrier = portadora triangular."""
    iL = x[0]
    s = 1.0 if d_ref > portadora_triangular(t, fsw) else 0.0
    diL = (s * Vdc - R * iL) / L
    return [diL]

def event_comparator(t, x, d_ref, L, R, Vdc, fsw):
    """Evento: cruce del comparador -> cambio de estado."""
    return d_ref - portadora_triangular(t, fsw)
event_comparator.terminal = False; event_comparator.direction = 0

# Parametros
L, R, Vdc, fsw = 2e-3, 0.1, 400.0, 5000.0
d_ref = 0.6
t_end = 0.01

sol = solve_ivp(
    lambda t, x: rhs_conmutado(t, x, d_ref, L, R, Vdc, fsw),
    (0, t_end), [0.0],
    method='LSODA', max_step=1.0/fsw/20,
    events=lambda t, x: event_comparator(t, x, d_ref, L, R, Vdc, fsw),
    rtol=1e-6, atol=1e-8
)
t_sw = sol.t; iL_sw = sol.y[0]

# Rizado teorico
delta_iL_teo = Vdc * d_ref * (1 - d_ref) / (L * fsw)
# Rizado simulado (ultimos 3 periodos)
mask = t_sw >= t_end - 3/fsw
delta_iL_sim = iL_sw[mask].max() - iL_sw[mask].min()
print(f"Rizado teorico: {delta_iL_teo:.2f} A, simulado: {delta_iL_sim:.2f} A, "
      f"error: {abs(delta_iL_sim-delta_iL_teo)/delta_iL_teo*100:.1f}%")
```

La amplitud del rizado de corriente teorica para un buck es:

$$ \Delta i_L = \frac{V_{dc} \cdot d \cdot (1-d)}{L \cdot f_{sw}} $$

Para los parametros del ejemplo: \( \Delta i_L = 400 \times 0.6 \times 0.4 / (2\times10^{-3} \times 5000) = 9.6\,\text{A} \). La simulacion conmutada con deteccion de eventos deberia dar < 2% de error respecto a este valor.

## 8 — Limites del modelo promediado: cuando diverge del conmutado

El modelo promediado es valido mientras:
1. \( f_{control} \ll f_{sw}/2 \): el ancho de banda del control es mucho menor que la mitad de la frecuencia de conmutacion.
2. La profundidad de modulacion \( d \in (0.05, 0.95) \): cerca de los limites, el modulador satura y el modelo promediado no captura el clipping.
3. Los tiempos muertos son pequenos frente al periodo de conmutacion: \( t_{dead} < 0.05 \cdot T_{sw} \).

Cuando estas condiciones no se cumplen, la divergencia entre el conmutado y el promediado puede ser significativa incluso en baja frecuencia:

**Efecto del tiempo muerto:** el tiempo muerto \( t_{dead} \) introduce una tension de error media de:

$$ \overline{\Delta v}_{dead} = \frac{2\,t_{dead}}{T_{sw}} \cdot V_{dc} \cdot \text{sign}(i_L) $$

Para \( t_{dead} = 2\,\mu\text{s} \), \( T_{sw} = 200\,\mu\text{s} \), \( V_{dc} = 400\,\text{V} \): \( \overline{\Delta v} = 8\,\text{V} \) — un error de ciclo de trabajo del 2% que el promediado ignora. Esto explica las diferencias en la tension de salida de regimen entre el modelo promediado y el conmutado que se observan en la practica.
