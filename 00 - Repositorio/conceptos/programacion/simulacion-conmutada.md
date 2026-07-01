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
