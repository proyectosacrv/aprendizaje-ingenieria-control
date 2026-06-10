---
titulo: Máquina de inducción (asíncrona)
slug: maquina-induccion
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: []
objetivos: [base de la eólica DFIG y de los accionamientos AC]
tags: [maquina-induccion, asincrona, deslizamiento, dfig, basico]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-06-10
relacionados: [generador-sincrono, eolica-mppt, control-vectorial, marco-dq, sistema-trifasico]
referencias:
  - "Fitzgerald, Electric Machinery, McGraw-Hill"
  - "Krause, Analysis of Electric Machinery"
---

## Definición
Máquina de corriente alterna cuyo rotor **no** gira sincronizado con el campo del estátor, sino con un
pequeño retraso (**deslizamiento**). No necesita excitación externa en el rotor: las corrientes del
rotor se **inducen** (de ahí "inducción"). Es la máquina más usada como motor y, en eólica, como
generador (jaula o DFIG).

## Fundamento teórico
El estátor crea un campo giratorio a la **velocidad de sincronismo**:
$$ n_s = \frac{120 f}{p} \ \text{[rpm]} \qquad (\,p = \text{nº de polos}\,) $$
El rotor gira a \( n \), y el **deslizamiento** es
$$ s = \frac{n_s - n}{n_s} $$
- \( 0 < s < 1 \): funcionamiento como **motor** (el rotor va más lento que el campo).
- \( s < 0 \) (rotor más rápido que el campo): funcionamiento como **generador**.
El circuito equivalente por fase tiene \( R_1, X_1 \) (estátor), \( X_m \) (magnetización) y
\( R_2/s, X_2 \) (rotor referido): el término \( R_2/s \) concentra la dependencia con la carga. El
par es máximo a un cierto deslizamiento y cae a cero en sincronismo.

## Cuándo y por qué se usa
En accionamientos de velocidad variable (con control vectorial) y en generación eólica: la **DFIG**
(doblemente alimentada) alimenta el rotor por un convertidor para operar a velocidad variable en torno
al sincronismo con un convertidor de potencia reducida.

## Procedimiento de diseño (genérico)
1. Determina \( n_s \) a partir de \( f \) y \( p \).
2. Plantea el circuito equivalente y la curva par-velocidad.
3. Para control de velocidad/par, usa **control vectorial** (orientación de campo) en el marco dq.

## Ejemplo de código
```python
f, p, n = 50.0, 4, 1455.0
ns = 120*f/p                 # 1500 rpm
s  = (ns - n)/ns             # deslizamiento ~ 0.03 (motor)
```

## Parámetros y valores típicos
Deslizamiento nominal: 1–5 % (motor). En generación, \( s \) negativo de magnitud similar. La DFIG
maneja \( \pm 30\% \) de velocidad con un convertidor de ~30 % de la potencia nominal.

## Errores comunes
- Confundirla con la síncrona (la asíncrona necesita deslizamiento para producir par).
- Equivocar el signo del deslizamiento en modo generador.
- Olvidar que el par cae a cero exactamente en sincronismo.

## Conceptos relacionados
- [[generador-sincrono]] · [[eolica-mppt]] · [[control-vectorial]] · [[marco-dq]] · [[sistema-trifasico]]

## Referencias
- Fitzgerald, *Electric Machinery*.
- Krause, *Analysis of Electric Machinery*.
