---
titulo: Convertidor fuente de tensión (VSC, 2 niveles)
slug: convertidor-vsc
categoria: fisica-modelado
tipo: concepto
nivel: basico
proyectos: []
objetivos: [entender la topología base del inversor trifásico controlado]
tags: [vsc, inversor, dos-niveles, igbt, puente, basico, modelado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-12
relacionados: [modulacion-pwm, modelo-promediado, topologias-multinivel, filtro-lcl, sistema-trifasico]
referencias:
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
  - "Mohan, Undeland, Robbins, Power Electronics, Wiley"
---

## Definición
Convertidor con un **bus DC de tensión** (condensador) que sintetiza tensiones AC controladas
mediante **tres ramas** de dos interruptores (IGBT + diodo). Es la topología base de inversores
de red, accionamientos y convertidores back-to-back.

## Fundamento teórico
Cada rama conecta su salida a \( +V_{dc} \) o a \( 0 \) según el interruptor activo (los dos de
una rama nunca conducen a la vez → **tiempo muerto**). La tensión de fase media depende del
ciclo de trabajo \( d_x\in[0,1] \):
$$ v_{x,N}=d_x\,V_{dc},\qquad v_{xn}=v_{x,N}-\tfrac13\textstyle\sum_k v_{k,N} $$
El **índice de modulación** \( m=\hat V_{fase}/(V_{dc}/2) \) llega a 1 en SPWM lineal y a
\( 2/\sqrt3\approx1.15 \) con inyección de 3º armónico / SVPWM. Del lado DC, balance de potencia:
\( v_{dc}i_{dc}=\sum_x v_x i_x \). El [[modelo-promediado]] sustituye la conmutación por las
\( d_x \) continuas para análisis y control.

<div class="cfig"><img src="figuras/convertidor-vsc-rama.png" alt="una rama del VSC de dos niveles"><div class="cap">Una de las tres ramas idénticas (a, b, c): dos interruptores (S1, S2, nunca a la vez) conmutan la salida entre +Vdc y 0. Las tres ramas juntas forman el VSC trifásico de 2 niveles.</div></div>

## Cuándo y por qué se usa
Siempre que se necesite intercambiar potencia AC↔DC de forma controlada y bidireccional:
conexión a red de renovables, STATCOM, motores, HVDC (en cascada/multinivel). Su salida exige un
[[filtro-lcl|filtro]] para atenuar la conmutación.

## Procedimiento (genérico)
1. Dimensiona \( V_{dc} \) (\( >\,2\sqrt2 V_{LL}/\sqrt3 / m_{max} \) para no saturar la modulación).
2. Elige frecuencia de conmutación \( f_{sw} \) y modulación ([[modulacion-pwm]]).
3. Modela en promediado (ciclos de trabajo) y pasa a dq para el control.
4. Diseña filtro de salida y lazos de corriente/tensión.

## Ejemplo de aplicación real
**Problema:** VSC de 1 MVA conectado a red de 690 V (LL, RMS) a factor de potencia unidad. Calcular la tensión de DC mínima para modulación lineal y la corriente AC nominal.

Tensión de fase pico: \( \hat V_{ac}=690\sqrt{2}/\sqrt{3}\approx563\,\text{V} \). Para índice de modulación máximo \( m_{max}=0.95 \): \( V_{dc,min}=2\hat V_{ac}/m_{max}=2\times563/0.95\approx1185\,\text{V} \). Elección práctica: \( V_{dc}=1.2\,\text{kV} \) (\( m\approx0.94 \), zona lineal). Corriente AC nominal: \( I_{ac}=S/(\sqrt{3}\,V_{LL})=10^6/(\sqrt{3}\times690)\approx836\,\text{A} \). Con \( fp=1 \), toda la corriente es activa (\( i_d^*\approx836\,\text{A} \), \( i_q^*=0 \)). Si la tensión de DC baja bajo 1.185 kV la modulación satura y el convertidor pierde control lineal de la tensión AC.

## Ejemplo de código
```python
def vsc_avg(d_abc, vdc):                 # modelo promediado, fase-neutro
    vN = d_abc*vdc                       # tensiones rama-N (d en [0,1])
    return vN - vN.mean()                # quita modo común -> fase-neutro
```

## Parámetros y valores típicos
\( f_{sw} \): 2–20 kHz (red), índice de modulación de diseño \( m\approx0.8\text{–}0.95 \), tiempo
muerto 1–3 µs, rizado de bus DC < 1–2 %.

## Errores comunes
- Elegir \( V_{dc} \) demasiado bajo → saturación de modulación y distorsión.
- Despreciar el tiempo muerto (introduce armónicos y caída de tensión).
- Usar el modelo promediado más allá de \( f_{sw}/2 \) (no captura la conmutación).

## Conceptos relacionados
- [[modulacion-pwm]] · [[modelo-promediado]] · [[topologias-multinivel]] · [[filtro-lcl]]

## Referencias
- Yazdani, Iravani, 2010.
- Mohan, Undeland, Robbins, *Power Electronics*.
