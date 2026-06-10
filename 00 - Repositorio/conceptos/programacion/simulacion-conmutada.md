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
fecha_actualizacion: 2026-06-09
relacionados: [modelo-promediado, modulacion-pwm, convertidor-vsc, integracion-edos-stiff, fft-analisis-espectral]
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
- [[modelo-promediado]] · [[modulacion-pwm]] · [[convertidor-vsc]] · [[integracion-edos-stiff]] · [[fft-analisis-espectral]]

## Referencias
- Mohan, Undeland, Robbins, *Power Electronics*.
- Maksimovic et al., *Modeling and Simulation of Power Electronic Converters*, Proc. IEEE 2001.
