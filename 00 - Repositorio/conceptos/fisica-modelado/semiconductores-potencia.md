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
relacionados: [convertidor-vsc, simulacion-conmutada, topologias-multinivel]
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

## Impacto de la topología sobre el modelo de planta y el control

La elección del semiconductor y la topología de conmutación modifica directamente los parámetros de
diseño del control:

### Si (IGBT, 2 niveles) vs SiC MOSFET vs NPC/T-type 3 niveles

| Parámetro | IGBT 2-niv | SiC MOSFET 2-niv | NPC/T-type 3-niv |
|---|---|---|---|
| \(f_{sw}\) típica | 2–16 kHz | 20–100 kHz | 10–30 kHz efectiva |
| \(f_{res,LCL}\) admisible | 1–5 kHz | 5–30 kHz | 3–12 kHz |
| Filtro LCL | mayor inductancia | menor inductancia | intermedio |
| Ganancia modulador \(K_m\) | \(V_{dc}/V_{tri}\) (2 niv) | idem | \(V_{dc}/(2V_{tri})\) (3 niv) |
| Dead time / distorsión | 1–3 µs, notable | 100–300 ns, mínimo | 1–2 µs por semiciclo |

El **cambio de topología exige re-sintonizar el control**:
- Con SiC a 50 kHz, el LCL puede ser 5–10× más pequeño → la resonancia sube → el amortiguamiento
  activo ([[filtro-lcl|amortiguamiento activo]]) debe extenderse a esa banda.
- Con NPC (3 niveles): la ganancia del modulador se reduce a la mitad (\(V_{dc}/2\) por nivel) →
  la ganancia de lazo del control de corriente baja a la mitad → hay que reajustar el PI.
- La corriente de rizado cae en proporción al número de niveles, lo que relaja el dimensionado del
  condensador del filtro.

### Modelo de pérdidas para comparar topologías
```
P_total = P_cond + P_sw = D·Vce_sat·I + (Eon+Eoff)·fsw   [IGBT]
P_total = I²·Rds_on   + (Qg·Vgs)·fsw                      [SiC MOSFET, aprox]
```
A \(f_{sw}\) baja (<5 kHz): IGBT gana (menor \(P_{sw}\)); a alta frecuencia (>20 kHz): SiC gana porque
\(E_{on}+E_{off}\) es ×5–10 menor. El cruce suele estar en 10–20 kHz.

## Procedimiento de diseño (genérico)
1. Elige el tipo según tensión/corriente/\( f_{sw} \) (IGBT para el VSC de red típico).
2. Estima pérdidas de conducción + conmutación para dimensionar el disipador.
3. Fija el tiempo muerto (decenas–cientos de ns para SiC; 1–3 µs para IGBT).
4. Revisa el impacto sobre el diseño del LCL y la ganancia del modulador (ver tabla).
5. Si cambias de 2 a 3 niveles: ajusta \(K_m\) y re-sintoniza los PI de corriente.

## Ejemplo de código
```python
# Estimacion gruesa de perdidas de un IGBT
Vce_sat, I, Eon, Eoff, fsw = 1.8, 20.0, 3e-3, 2e-3, 10e3
P_cond = Vce_sat*I                          # conduccion (aprox, factor de uso ~0.5)
P_sw   = (Eon+Eoff)*fsw                     # conmutacion

# SiC MOSFET: mismo bus DC, fsw=50kHz, perdidas mucho menores
Rds_on, I_sic, Eon_sic, Eoff_sic, fsw_sic = 7e-3, 20.0, 0.3e-3, 0.2e-3, 50e3
P_cond_sic = Rds_on * I_sic**2
P_sw_sic   = (Eon_sic + Eoff_sic) * fsw_sic   # ≈25W vs ≈50W del IGBT a 10kHz

# Ganancia de modulador 3 niveles (NPC)
Km_2niv = Vdc / Vtri           # 2 niveles
Km_3niv = Vdc / (2 * Vtri)    # 3 niveles: mitad de ganancia -> resintonizar PI
```

## Parámetros y valores típicos
\( f_{sw} \) en VSC de red: 2–20 kHz (IGBT), 20–100 kHz (SiC). \( V_{ce(sat)} \) de IGBT ≈ 1.5–2.5 V.
Tiempo muerto: 1–3 µs para módulos IGBT; 100–300 ns para SiC.

## Errores comunes
- Omitir el tiempo muerto en el modelo \( \to \) cortocircuito de rama (en hardware, destrucción).
- Despreciar las pérdidas de conmutación al subir \( f_{sw} \).
- Suponer interruptores ideales y olvidar la distorsión por dead time.

## Uso en proyectos
- **01 - GFM-Impedance** (validación PLECS): el modelo conmutado usa medios puentes IGBT con PWM a
  10 kHz; se compara con el promediado (diferencia ≈ 0.67 %).

## Conceptos relacionados
- [[convertidor-vsc]] · [[simulacion-conmutada]] · [[topologias-multinivel]]

## Referencias
- Mohan, Undeland & Robbins, *Power Electronics*.
