---
titulo: Sintonía de PI/PID (cancelación de polo, óptimo de módulo)
slug: sintonia-pi-pid
categoria: metodologia
tipo: metodo
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [obtener las ganancias de un PI a partir del ancho de banda]
tags: [PI, PID, sintonia, cancelacion-polo, modulo-optimo]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [metodos-sintesis-control, control-cascada, especificaciones-control, loop-shaping]
referencias:
  - "Aström, Hägglund, Advanced PID Control, ISA 2006"
---

## Definición
Métodos sistemáticos para fijar las ganancias de un controlador PI/PID a partir del modelo de la
planta y del ancho de banda deseado, en lugar de prueba y error.

## Fundamento teórico
Para una planta de primer orden \( G(s)=\dfrac{K}{1+\tau s} \) (típico del lazo de corriente,
\( \tau=L/R \)) con PI \( C(s)=K_p+\dfrac{K_i}{s} \):
- **Cancelación de polo**: coloca el cero del PI sobre el polo de la planta
  (\( K_i/K_p = 1/\tau = R/L \)), dejando un lazo de primer orden con ancho de banda
  \( \omega_c \): \( K_p = L\,\omega_c \), \( K_i = R\,\omega_c \).
- **Óptimo de módulo** (plantas con retardo/2º orden): hace \( |T(j\omega)|\approx 1 \) en la
  banda; bueno para lazos internos.
- **Óptimo simétrico**: para plantas con integrador (lazos de tensión/posición), maximiza el
  margen de fase a la frecuencia de cruce.

## Cuándo y por qué se usa
Es el método base en convertidores: rápido, intuitivo y con relación directa al ancho de banda.
Se combina con la arquitectura en [[control-cascada]].

## Procedimiento (genérico)
1. Modela la planta del lazo (orden, polos, ganancia).
2. Fija \( \omega_c \) desde [[especificaciones-control]].
3. Cancelación de polo: \( K_p=L\omega_c \), \( K_i=R\omega_c \) (lazo de corriente).
4. Verifica margen de fase y respuesta; si hay retardo, reduce \( \omega_c \) o usa óptimo de módulo.

## Ejemplo de código
```python
# PI de lazo de corriente por cancelacion de polo (planta L,R)
wc = 2*np.pi*f_c          # ancho de banda objetivo
Kp = L*wc;  Ki = R*wc     # cero del PI en R/L (cancela el polo de planta)
```

## Parámetros y valores típicos
\( f_c \) del lazo de corriente ≈ \( f_{sw}/10 \). Margen de fase resultante ≈ 60–90° (1er orden).

## Errores comunes
- Cancelar un polo mal identificado o variable → cancelación imperfecta.
- Ignorar el retardo de cómputo/PWM: reduce el margen real a alto \( \omega_c \).

## Uso en proyectos
- **01/02**: lazos de corriente sintonizados así (\( K_p=L_1\omega_{ci} \), \( K_i=R_1\omega_{ci} \)),
  \( f_{ci} \) ≈ 1 kHz / 800 Hz.

## Conceptos relacionados
- [[metodos-sintesis-control]] · [[control-cascada]] · [[loop-shaping]] · [[especificaciones-control]]

## Referencias
- Aström, Hägglund, *Advanced PID Control*, 2006.
