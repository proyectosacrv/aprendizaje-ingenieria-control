---
titulo: Semiconductores de potencia (IGBT, MOSFET, diodo)
slug: semiconductores-potencia
categoria: fisica-modelado
tipo: concepto
nivel: basico
proyectos: [01-GFM-Impedance]
objetivos: [entender qué conmuta realmente en el VSC y de dónde salen las pérdidas]
tags: [igbt, mosfet, diodo, conmutacion, perdidas, basico]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-06-12
relacionados: [convertidor-vsc, modulacion-pwm, modelo-promediado, simulacion-conmutada, topologias-multinivel]
referencias:
  - "Mohan, Undeland & Robbins, Power Electronics"
  - "Erickson & Maksimovic, Fundamentals of Power Electronics"
---

## Definición
Son los interruptores electrónicos que encienden y apagan el paso de corriente en un convertidor. El
**diodo** conduce en un sentido sin control; el **MOSFET** y el **IGBT** son interruptores
controlables por puerta. La elección depende de la tensión, la corriente y la frecuencia de
conmutación.

## Fundamento teórico
Idealmente conmutan entre **ON** (conduce, caída casi nula) y **OFF** (bloquea). En la realidad:
- **Pérdidas de conducción:** caída no nula. MOSFET \( \approx R_{ds(on)} I^2 \); IGBT
  \( \approx V_{ce(sat)} I \).
- **Pérdidas de conmutación:** energía disipada en cada transición, proporcional a la frecuencia:
$$ P_{sw} \approx (E_{on}+E_{off})\,f_{sw} $$
Cada interruptor lleva un **diodo en antiparalelo** para la corriente inductiva. En una rama
(medio puente) los dos interruptores **nunca** deben conducir a la vez: se inserta un **tiempo
muerto** (dead time) entre el apagado de uno y el encendido del otro.

| Dispositivo | Control | Rango típico | Frecuencia |
|---|---|---|---|
| Diodo | no | — | — |
| MOSFET | sí (tensión) | baja-media tensión | alta (>100 kHz) |
| IGBT | sí (tensión) | media-alta tensión/potencia | media (2–20 kHz) |

<div class="cfig"><img src="figuras/semiconductores-potencia-conmutacion.png" alt="perdida de conmutacion V I solapadas"><div class="cap">Pérdida de conmutación: durante cada transición la tensión sube mientras la corriente aún no ha caído (y viceversa); ese solapamiento V·I es energía disipada, proporcional a fsw.</div></div>

## Cuándo y por qué se usa
Definen el **modelo conmutado** (lo que PLECS simula en detalle) frente al **modelo promediado**
(diseño y análisis). Sus pérdidas fijan el rendimiento y la refrigeración; sus tiempos muertos
introducen distorsión que el modelo promediado no captura.

## Procedimiento de diseño (genérico)
1. Elige el tipo según tensión/corriente/\( f_{sw} \) (IGBT para el VSC de red típico).
2. Estima pérdidas de conducción + conmutación para dimensionar el disipador.
3. Fija el tiempo muerto (decenas–cientos de ns) para evitar cortocircuito de rama.

## Ejemplo de código
```python
# Estimacion gruesa de perdidas de un IGBT
Vce_sat, I, Eon, Eoff, fsw = 1.8, 20.0, 3e-3, 2e-3, 10e3
P_cond = Vce_sat*I                          # conduccion (aprox, factor de uso ~0.5)
P_sw   = (Eon+Eoff)*fsw                      # conmutacion
```

## Parámetros y valores típicos
\( f_{sw} \) en VSC de red: 2–20 kHz (10 kHz en el proyecto). \( V_{ce(sat)} \) de IGBT ≈ 1.5–2.5 V.
Tiempo muerto: 1–3 µs en módulos de potencia.

## Errores comunes
- Omitir el tiempo muerto en el modelo \( \to \) cortocircuito de rama (en hardware, destrucción).
- Despreciar las pérdidas de conmutación al subir \( f_{sw} \).
- Suponer interruptores ideales y olvidar la distorsión por dead time.

## Uso en proyectos
- **01 - GFM-Impedance** (validación PLECS): el modelo conmutado usa medios puentes IGBT con PWM a
  10 kHz; se compara con el promediado (diferencia ≈ 0.67 %).

## Conceptos relacionados
- [[convertidor-vsc]] · [[modulacion-pwm]] · [[modelo-promediado]] · [[simulacion-conmutada]] · [[topologias-multinivel]]

## Referencias
- Mohan, Undeland & Robbins, *Power Electronics*.
