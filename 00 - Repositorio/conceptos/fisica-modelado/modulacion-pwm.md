---
titulo: Modulación por ancho de pulso (PWM)
slug: modulacion-pwm
categoria: fisica-modelado
tipo: concepto
nivel: basico
proyectos: []
objetivos: [entender como un convertidor sintetiza una tension media conmutando]
tags: [PWM, ciclo-de-trabajo, conmutacion, modulacion, basico]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [modelo-promediado, topologias-multinivel, control-vectorial]
referencias:
  - "Mohan, Undeland, Robbins, Power Electronics, Wiley"
---

## Definición
Técnica para que un convertidor genere una **tensión media** deseada **conmutando** sus
interruptores entre niveles fijos (p.ej. \( +V_{dc} \) y \( 0 \)). Variando la fracción de tiempo
que está en cada nivel se controla el valor medio.

## Fundamento teórico
El **ciclo de trabajo** \( d \) (entre 0 y 1) es la fracción del periodo de conmutación en que el
interruptor está cerrado. La tensión **media** en un periodo es:
$$ \bar{v} = d\,V_{dc} $$
Comparando una señal **moduladora** \( m(t) \) (la referencia, p.ej. una senoide) con una
**portadora** triangular a frecuencia \( f_{sw} \) se generan los pulsos: cuando \( m>\text{portadora} \),
el interruptor conduce. Así, el valor medio sigue a la moduladora. La conmutación introduce
**armónicos** alrededor de \( f_{sw} \) y sus múltiplos, que el filtro atenúa. Esto justifica el
[[modelo-promediado]]: para frecuencias muy por debajo de \( f_{sw} \), el convertidor se comporta
como si aplicara \( \bar{v}=d\,V_{dc} \) de forma continua.

## Cuándo y por qué se usa
En prácticamente todos los convertidores (inversores, DC-DC, rectificadores activos): es el modo
de imponer la tensión que pide el control con bajas pérdidas.

## Procedimiento (genérico)
1. El control calcula la tensión de referencia (moduladora).
2. Se normaliza por \( V_{dc} \) para obtener el ciclo de trabajo / índice de modulación.
3. Se compara con la portadora (\( f_{sw} \)) para generar los pulsos de disparo.
4. El filtro de salida atenúa los armónicos de conmutación.

## Ejemplo de aplicación real
**Problema:** VSC trifásico con \( V_{dc}=700\,\text{V} \) inyectando en red de 400 V (LL, RMS). Verificar que el modulador opera en zona lineal a plena potencia y calcular el margen de reserva.

Tensión de fase pico de red: \( \hat V_f=400\sqrt{2}/\sqrt{3}\approx327\,\text{V} \). Índice de modulación: \( m_a=\hat V_f/(V_{dc}/2)=327/350\approx0.934<1 \): zona lineal (\(\checkmark\)). Reserva para inyectar reactiva: con \( Q_{max} \) el vector de referencia crece a \( |\hat V_{ref}|=\sqrt{327^2+V_q^2} \). Margen disponible: la referencia puede crecer hasta \( V_{dc}/2=350\,\text{V} \), es decir, un \( 7\,\% \) más antes de salir de la zona lineal. Para mantener margen del 10 % ante variaciones de red: \( V_{dc,min}=2\times327/0.90\approx727\,\text{V} \).

## Ejemplo de código
```python
import numpy as np
def pwm(t, m, fsw):
    tri = 2*np.abs(2*((t*fsw) % 1) - 1) - 1     # portadora triangular [-1,1]
    return np.where(m > tri, 1.0, 0.0)          # estado del interruptor
```

## Parámetros y valores típicos
\( f_{sw} \) de unos kHz a decenas de kHz. Índice de modulación lineal \( \le 1 \) (por encima,
sobremodulación). Regla: ancho de banda de control \( < f_{sw}/10 \).

## Errores comunes
- Sobremodular (índice > 1) sin querer → distorsión y pérdida de control lineal.
- Pedir un ancho de banda de control demasiado cerca de \( f_{sw} \).

## Conceptos relacionados
- [[modelo-promediado]] · [[topologias-multinivel]] · [[control-vectorial]]

## Referencias
- Mohan, Undeland, Robbins, *Power Electronics*, Wiley.
