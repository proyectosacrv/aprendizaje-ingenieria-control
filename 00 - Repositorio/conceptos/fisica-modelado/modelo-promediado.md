---
titulo: Modelo promediado vs conmutado
slug: modelo-promediado
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance]
objetivos: [justificar el modelo de diseño y validar contra el conmutado]
tags: [averaging, PWM, conmutado, simulacion, rizado]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [filtro-lcl, medicion-impedancia-inyeccion, marco-dq]
referencias:
  - "Erickson, Maksimovic, Fundamentals of Power Electronics, Springer (averaging)"
---

## Definición
El **modelo promediado** sustituye la tensión conmutada del puente por su valor medio en cada
periodo de conmutación (la modulante × \( V_{dc}/2 \)). El **modelo conmutado** simula los IGBTs
y el PWM reales, con su rizado de alta frecuencia.

## Fundamento teórico
Si la frecuencia de conmutación \( f_{sw} \) es mucho mayor que el ancho de banda de control y
que la dinámica del filtro, el promedio del puente reproduce la dinámica **útil**; el filtro LCL
atenúa el rizado de conmutación. El error entre conmutado y promediado es pequeño y de alta
frecuencia. Formalmente es *state-space averaging*: se promedia \( \dot x = f(x,u) \) sobre el
periodo de conmutación.

## Cuándo y por qué se usa
Para **diseñar y analizar** (control, impedancia, estabilidad) se usa el promediado: es continuo,
linealizable y rápido de simular. El conmutado se reserva para **validar** y para estudiar
fenómenos de conmutación (rizado, pérdidas, EMI).

## Procedimiento de diseño (genérico)
1. Diseña y analiza con el modelo promediado.
2. Verifica que \( f_{sw} \gg \) (10×) el mayor ancho de banda de control.
3. Valida en un modelo conmutado (PLECS o PWM en código): compara formas de onda e impedancia.
4. Si difieren salvo el rizado, el promediado es válido.

## Ejemplo de código
```python
# conmutado: v_puente = +-Vdc/2 segun PWM; promediado: v_puente = (Vdc/2)*modulante
v_sw  = np.where(m > carrier(t), Vdc/2, -Vdc/2)
v_avg = (Vdc/2)*m
# tras el filtro LC, vc_sw ~= vc_avg + rizado pequeno
```

## Parámetros y valores típicos
Validez si \( f_{sw}/f_{control}\gtrsim 10 \). En el proyecto: \( f_{sw}=10\,\text{kHz} \),
rizado de \( v_C \) ≈ 2.5%, diferencia conmutado-promediado ≈ 0.67%.

## Errores comunes
- Usar promediado cuando \( f_{sw} \) no separa escalas → el promediado oculta inestabilidades de
  conmutación.
- Comparar conmutado y promediado sin filtrar el rizado y concluir que "no coinciden".

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: justificar el modelo): `switched.py` demostró que el
  promediado captura la dinámica útil (dif. 0.67%). Todo el análisis se hizo con el promediado.

## Conceptos relacionados
- [[filtro-lcl]] · [[medicion-impedancia-inyeccion]] · [[marco-dq]]

## Referencias
- Erickson, Maksimovic, *Fundamentals of Power Electronics*.
