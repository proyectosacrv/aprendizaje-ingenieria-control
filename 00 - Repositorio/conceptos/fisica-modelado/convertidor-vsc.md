---
titulo: "Convertidor fuente de tensión (VSC): topología, PWM y modelo promediado"
slug: convertidor-vsc
categoria: fisica-modelado
tipo: concepto
nivel: basico
proyectos: [01-GFM-Impedance]
objetivos: [entender la topología del convertidor controlado por tensión, cómo sintetiza tensión por PWM y cómo se modela en promediado para diseño y control]
tags: [vsc, inversor, dos-niveles, pwm, ciclo-de-trabajo, modelo-promediado, averaging, conmutado, modulacion, modelado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-16
relacionados: [topologias-multinivel, semiconductores-potencia, filtro-lcl, marco-dq, sistema-trifasico, medicion-impedancia-inyeccion]
referencias:
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
  - "Mohan, Undeland, Robbins, Power Electronics, Wiley"
  - "Erickson, Maksimovic, Fundamentals of Power Electronics, Springer (averaging)"
---

## Definición
El convertidor fuente de tensión (VSC, voltage-sourced converter) es la familia de convertidores que parten de un bus DC de tensión (un condensador) y sintetizan tensiones AC controladas conmutando interruptores entre niveles fijos. Esta ficha cubre las tres cosas que son inseparables para entenderlo y usarlo: su topología (el puente), cómo impone la tensión que pide el control (modulación PWM) y cómo se modela para diseño y análisis (modelo promediado frente a conmutado). Aquí se desarrolla la variante base de dos niveles; las variantes multinivel están en [[topologias-multinivel]] y los interruptores en [[semiconductores-potencia]].

## Topología
Cada una de las tres ramas (a, b, c) conecta su salida a +Vdc o a 0 según cuál de sus dos interruptores conduce (los dos de una rama nunca a la vez → tiempo muerto). La tensión de fase media depende del ciclo de trabajo dx entre 0 y 1:

- vx_N = dx·Vdc
- vxn = vx_N − (1/3)·suma_k(vk_N)

El índice de modulación m = Vfase_pico / (Vdc/2) llega a 1 en SPWM lineal y a 2/raiz(3) ≈ 1.15 con inyección de tercer armónico / SVPWM. Del lado DC, balance de potencia: vdc·idc = suma_x(vx·ix).

<div class="cfig"><img src="figuras/convertidor-vsc-rama.png" alt="una rama del VSC de dos niveles"><div class="cap">Una de las tres ramas idénticas (a, b, c): dos interruptores (S1, S2, nunca a la vez) conmutan la salida entre +Vdc y 0. Las tres ramas juntas forman el VSC trifásico de 2 niveles.</div></div>

## Modulación PWM (cómo impone la tensión)
PWM es la técnica con la que el convertidor genera la tensión media que pide el control conmutando entre niveles fijos. El ciclo de trabajo d (entre 0 y 1) es la fracción del periodo de conmutación en que el interruptor está cerrado; la tensión media en un periodo es:

v_media = d·Vdc

Comparando una señal moduladora m(t) (la referencia que da el control, por ejemplo una senoide) con una portadora triangular a frecuencia fsw se generan los pulsos: cuando m > portadora, el interruptor conduce. Así el valor medio sigue a la moduladora. La conmutación introduce armónicos alrededor de fsw y sus múltiplos, que el filtro de salida atenúa. Esto es lo que justifica el modelo promediado: para frecuencias muy por debajo de fsw, el convertidor se comporta como si aplicara v_media = d·Vdc de forma continua.

<div class="cfig"><img src="figuras/modulacion-pwm-ondas.png" alt="moduladora, portadora y salida conmutada"><div class="cap">Arriba: la moduladora (referencia) se compara con la portadora triangular. Abajo: la tensión conmutada resultante; su media (discontinua) reproduce la moduladora. El filtro elimina los armónicos en torno a fsw.</div></div>

## Modelo promediado vs conmutado (cómo se modela)
El modelo promediado sustituye la tensión conmutada del puente por su valor medio en cada periodo de conmutación (la moduladora × Vdc/2 por fase). El modelo conmutado simula los interruptores y el PWM reales, con su rizado de alta frecuencia.

Fundamento: si fsw es mucho mayor que el ancho de banda de control y que la dinámica del filtro, el promedio del puente reproduce la dinámica útil; el filtro atenúa el rizado de conmutación. El error entre conmutado y promediado es pequeño y de alta frecuencia. Formalmente es state-space averaging: se promedia dx/dt = f(x,u) sobre el periodo de conmutación.

<div class="cfig"><img src="figuras/modelo-promediado-ondas.png" alt="conmutado vs promediado"><div class="cap">El modelo conmutado (gris) lleva el rizado de fsw; el promediado (azul) retiene solo la dinámica útil. Si fsw separa escalas, ambos coinciden salvo ese rizado de alta frecuencia.</div></div>

Para diseñar y analizar (control, impedancia, estabilidad) se usa el promediado: es continuo, linealizable y rápido de simular. El conmutado se reserva para validar y para estudiar fenómenos de conmutación (rizado, pérdidas, EMI).

## Cuándo y por qué se usa
El VSC aparece siempre que se necesita intercambiar potencia AC↔DC de forma controlada y bidireccional: conexión a red de renovables, STATCOM, accionamientos de motor, HVDC y back-to-back (en cascada/multinivel). La modulación PWM es el modo estándar de imponer la tensión con bajas pérdidas en prácticamente todos los convertidores (también DC-DC y rectificadores activos). Su salida exige un [[filtro-lcl|filtro]] para atenuar la conmutación.

## Procedimiento (genérico)
1. Dimensiona Vdc: debe superar 2·raiz(2)·VLL/raiz(3) / m_max para no saturar la modulación.
2. Elige frecuencia de conmutación fsw y tipo de modulación; deja ancho de banda de control < fsw/10.
3. Modela en promediado (ciclos de trabajo) y pasa a dq para el control.
4. Diseña el filtro de salida y los lazos de corriente/tensión.
5. Valida en un modelo conmutado (PLECS o PWM en código): compara formas de onda e impedancia; si difieren solo en el rizado, el promediado es válido.

## Ejemplo de aplicación real
VSC de 1 MVA en red de 690 V (LL, RMS) a factor de potencia unidad. Tensión de fase pico Vac = 690·raiz(2)/raiz(3) ≈ 563 V. Para m_max = 0.95: Vdc_min = 2·563/0.95 ≈ 1185 V; elección práctica Vdc = 1.2 kV (m ≈ 0.94, zona lineal). Corriente AC nominal Iac = S/(raiz(3)·VLL) = 1e6/(raiz(3)·690) ≈ 836 A; con fp = 1, toda activa (id* ≈ 836 A, iq* = 0). Si Vdc baja de 1.185 kV la modulación satura y se pierde el control lineal de la tensión AC.

(Verificación de modulación en otro caso: VSC con Vdc = 700 V en red de 400 V → Vf_pico ≈ 327 V, ma = 327/350 ≈ 0.934 < 1, zona lineal; margen de ≈ 7 % hasta Vdc/2 = 350 V antes de saturar.)

## Ejemplo de código
```python
import numpy as np

def vsc_avg(d_abc, vdc):                       # modelo promediado, fase-neutro
    vN = d_abc*vdc                             # tensiones rama-N (d en [0,1])
    return vN - vN.mean()                      # quita modo comun -> fase-neutro

def pwm(t, m, fsw):                            # generacion conmutada
    tri = 2*np.abs(2*((t*fsw) % 1) - 1) - 1    # portadora triangular [-1,1]
    return np.where(m > tri, 1.0, 0.0)         # estado del interruptor

# conmutado vs promediado de una rama:
# v_sw  = np.where(m > tri, Vdc/2, -Vdc/2)
# v_avg = (Vdc/2)*m   -> tras el filtro LC, vc_sw ~= vc_avg + rizado pequeno
```

## Parámetros y valores típicos
- fsw: 2–20 kHz (red). Índice de modulación de diseño m ≈ 0.8–0.95 (lineal ≤ 1; por encima, sobremodulación). Tiempo muerto 1–3 µs. Rizado de bus DC < 1–2 %.
- Validez del promediado si fsw/f_control ≳ 10. En el proyecto: fsw = 10 kHz, rizado de vC ≈ 2.5 %, diferencia conmutado-promediado ≈ 0.67 %.

## Errores comunes
- Elegir Vdc demasiado bajo → saturación de modulación y distorsión.
- Sobremodular (índice > 1) sin querer → distorsión y pérdida de control lineal; pedir ancho de banda de control demasiado cerca de fsw.
- Despreciar el tiempo muerto (introduce armónicos y caída de tensión).
- Usar el modelo promediado más allá de fsw/2 o cuando fsw no separa escalas → oculta inestabilidades de conmutación.
- Comparar conmutado y promediado sin filtrar el rizado y concluir que "no coinciden".

## Uso en proyectos
- 01 - GFM-Impedance (justificar el modelo): switched.py demostró que el promediado captura la dinámica útil (diferencia 0.67 %). Todo el análisis se hizo con el promediado.

## Conceptos relacionados
- [[topologias-multinivel]] · [[semiconductores-potencia]] · [[filtro-lcl]] · [[marco-dq]] · [[sistema-trifasico]] · [[medicion-impedancia-inyeccion]]

## Referencias
- Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010.
- Mohan, Undeland, Robbins, Power Electronics, Wiley.
- Erickson, Maksimovic, Fundamentals of Power Electronics, Springer.
