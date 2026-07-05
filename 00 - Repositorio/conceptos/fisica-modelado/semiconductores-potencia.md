---
titulo: Semiconductores de potencia (IGBT, MOSFET, SiC, gate driver)
slug: semiconductores-potencia
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance]
objetivos: [entender qué conmuta realmente en el VSC, cuantificar las pérdidas y elegir el semiconductor]
tags: [igbt, mosfet, sic, diodo, conmutacion, perdidas, gate-driver, basico]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-07-04
relacionados: [convertidor-vsc, simulacion-conmutada, topologias-multinivel]
referencias:
  - "Mohan, Undeland & Robbins, Power Electronics"
  - "Erickson & Maksimovic, Fundamentals of Power Electronics"
  - "Millan et al., A Survey of Wide Bandgap Power Semiconductor Devices, IEEE TPEL 2014"
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
| Si MOSFET | sí (tensión) | <900 V | alta (>100 kHz) |
| IGBT | sí (tensión) | 600 V–6.5 kV | media (2–20 kHz) |
| SiC MOSFET | sí (tensión) | 650 V–3.3 kV | alta (20–200 kHz) |

<div class="cfig"><img src="figuras/semiconductores-potencia-conmutacion.png" alt="perdida de conmutacion V I solapadas"><div class="cap">Pérdida de conmutación: durante cada transición la tensión sube mientras la corriente aún no ha caído (y viceversa); ese solapamiento V·I es energía disipada, proporcional a fsw.</div></div>

## 1 — Pérdida de conmutación \( P_{sw}=\tfrac12 V I (t_{on}+t_{off}) f_{sw} \)
**Paso 1 — energía de una transición.** Durante una conmutación, la tensión \( V \) y la corriente \( I \) del dispositivo se solapan: mientras la tensión sube, la corriente aún no ha caído (y viceversa). La potencia instantánea disipada es \( p(t)=v(t)\,i(t) \), y la energía de esa transición es su integral:

$$ E=\int_{0}^{t_{sw}} v(t)\,i(t)\,dt $$

**Paso 2 — aproximación lineal del solapamiento.** En el encendido (duración \( t_{on} \)) se modela la corriente subiendo en rampa de \( 0 \) a \( I \) mientras la tensión cae de \( V \) a \( 0 \). El producto \( v\,i \) es un triángulo de altura máxima \( V I \) y base \( t_{on} \). El área de un triángulo es \( \tfrac12\,\text{base}\times\text{altura} \):

$$ E_{on}=\tfrac12\,V\,I\,t_{on} $$

Igual razonamiento en el apagado:

$$ E_{off}=\tfrac12\,V\,I\,t_{off} $$

**Paso 3 — sumar y multiplicar por la frecuencia.** Cada periodo de conmutación tiene un encendido y un apagado, luego la energía perdida por ciclo es \( E_{on}+E_{off}=\tfrac12 V I (t_{on}+t_{off}) \). Se repite \( f_{sw} \) veces por segundo, así que la potencia media de conmutación es:

$$ \boxed{\;P_{sw}=\big(E_{on}+E_{off}\big)\,f_{sw}=\tfrac12\,V\,I\,(t_{on}+t_{off})\,f_{sw}\;} $$

Es la versión analítica de la \( P_{sw}\approx(E_{on}+E_{off})f_{sw} \) del Fundamento (las hojas de datos dan \( E_{on},E_{off} \) medidas, que ya incluyen colas de corriente y recuperación inversa del diodo). **Clave física:** \( P_{sw}\propto f_{sw} \) — por eso subir la frecuencia para reducir el filtro tiene un coste térmico lineal, y por eso el SiC (con \( t_{on}+t_{off} \) ×5–10 menores) gana a alta frecuencia.

Ejemplo: \( V=600\,\text{V} \), \( I=20\,\text{A} \), \( t_{on}=1\,\mu s \), \( t_{off}=2\,\mu s \), \( f_{sw}=10\,\text{kHz} \) → \( P_{sw}=\tfrac12\cdot600\cdot20\cdot3{\times}10^{-6}\cdot10^4=180\,\text{W} \).

## 2 — Los tipos de interruptores: MOSFET, IGBT, SiC MOSFET
Los semiconductores de potencia se distinguen por la tecnología del material y la arquitectura del dispositivo. Cada tecnología nació para cubrir un hueco en el espacio tensión–corriente–frecuencia.

**El MOSFET de silicio** es un transistor de efecto de campo: la compuerta controla un canal resistivo entre drenador y surtidor. Su pérdida de conducción es puramente resistiva \( P_{cond}=I^2\,R_{ds(on)} \), por lo que aumenta con el cuadrado de la corriente. \( R_{ds(on)} \) crece fuertemente con la tensión de bloqueo (\( \propto V_{br}^{2.5} \)), así que por encima de 600–900 V el MOSFET de Si se vuelve ineficiente en conducción. Su ventaja principal es la velocidad de conmutación: tiempos de cruce de 50–200 ns permiten frecuencias de 100–500 kHz.

**El IGBT** combina la compuerta del MOSFET con la estructura bipolar de un BJT: la conducción inyecta portadores minoritarios que saturan el material y reducen la caída a \( V_{ce(sat)}\approx1.5\text{–}2.5\,\text{V} \) independientemente de la tensión de bloqueo. Esto lo hace superior al MOSFET de Si por encima de 600 V. El precio es la **cola de corriente** al apagar: los portadores minoritarios inyectados tardan en recombinarse, frenando \( t_{off} \) a 0.5–5 µs y limitando \( f_{sw} \) a 2–20 kHz en aplicaciones de media-alta potencia.

**El SiC MOSFET** (carburo de silicio) usa un material de banda prohibida ancha (3.26 eV vs 1.12 eV del Si): soporta campos eléctricos 10× mayores, lo que permite diseñar dispositivos de 650 V–3.3 kV con \( R_{ds(on)} \) muy inferior al Si MOSFET equivalente y sin cola de corriente. El resultado es \( E_{on}+E_{off} \) entre 5× y 10× menor que el IGBT a la misma tensión, y frecuencias de 20–200 kHz con eficiencias superiores al 99 % en muchas aplicaciones.

| Parámetro | Si MOSFET | Si IGBT | SiC MOSFET |
|---|---|---|---|
| \( V_{br} \) típica | <900 V | 600 V–6.5 kV | 650 V–3.3 kV |
| \( f_{sw} \) práctica | >100 kHz | 2–20 kHz | 20–200 kHz |
| \( P_{cond} \) | \( I^2 R_{ds} \) | \( V_{ce}\cdot I_{avg} \) | \( I^2 R_{ds} \) (bajo) |
| \( E_{sw} \) relativa | 1× | 5–10× | ≈1× (a igual tensión) |
| Temperatura máxima | 150 °C | 150–175 °C | 200–250 °C |
| Coste | bajo | bajo | alto (×3–5) |

El punto de cruce entre IGBT y SiC depende del punto de operación: a baja \( f_{sw} \) (<5 kHz) la pérdida dominante es la de conducción y el IGBT puede ganar; a alta \( f_{sw} \) (>20 kHz) el SiC es claramente superior por su \( E_{sw} \) reducida.

<div class="cfig"><img src="figuras/semiconductores-potencia-analisis.png" alt="comparativa IGBT vs SiC y gate driver"><div class="cap">Panel (a): energía de conmutación vs tensión para Si MOSFET, IGBT y SiC — el SiC mantiene E_sw bajo incluso a alta tensión. Panel (b): pérdidas totales vs fsw — cruce IGBT/SiC en 10–20 kHz. Panel (c): circuito de gate driver con Rg y el efecto sobre dV/dt. Panel (d): comparativa de pérdidas en el punto nominal del convertidor 1 MVA / 690 V.</div></div>

## 3 — Las pérdidas de conmutación: \( P_{sw}=(E_{on}+E_{off})\,f_{sw} \)
Las pérdidas de conmutación dependen de tres factores: la energía de cada evento, la frecuencia con que se repite y las condiciones del circuito (tensión de bus, corriente de carga, temperatura de unión).

**Energía de conmutación en la hoja de datos.** El fabricante mide \( E_{on} \) y \( E_{off} \) en un circuito de doble pulso a tensión y corriente definidas (p.ej. \( V_{DC}=400\,\text{V} \), \( I=100\,\text{A} \), \( T_j=125\,°C \)). Se escalan a las condiciones reales aproximadamente como:

$$ E_{sw}(V,I) \approx E_{sw,ref}\cdot\frac{V}{V_{ref}}\cdot\frac{I}{I_{ref}} $$

La dependencia en temperatura es también importante: a \( T_j \) más alta, \( E_{sw} \) del IGBT sube un 20–40 % (la cola de corriente se alarga con la temperatura). El SiC es menos sensible.

**La potencia de conmutación total** en un puente de fase con modulación SPWM, considerando que solo una transición ocurre por portadora en cada brazo, es aproximadamente:

$$ P_{sw,total}=2\,(E_{on}+E_{off})\,f_{sw}\cdot\frac{V_{DC}}{V_{ref}}\cdot\frac{\hat I}{I_{ref}} $$

donde \( \hat I \) es la amplitud de la corriente de fase y el factor 2 cuenta encendido y apagado. Esta expresión muestra que \( P_{sw} \) es proporcional a \( f_{sw} \): duplicar la frecuencia para reducir el filtro LCL a la mitad duplica las pérdidas de conmutación.

**Eficiencia y disipador.** Para el convertidor de referencia (1 MVA, 690 V, IGBT, \( f_{sw}=10\,\text{kHz} \)):

$$ P_{sw,IGBT}\approx2\times(3+2)\times10^{-3}\times10\times10^3=100\,\text{W/módulo} $$

Con 6 módulos (3 fases × 2 interruptores): \( P_{sw,total}\approx600\,\text{W} \). Las pérdidas de conducción (§4) añaden otro tanto. El disipador se dimensiona para mantener \( T_j<T_{j,max} \) con la resistencia térmica \( R_{thJC}+R_{thCS}+R_{thSA} \).

## 4 — Las pérdidas de conducción: resistencia vs caída de tensión
Las pérdidas de conducción son las que ocurren mientras el dispositivo está en ON y la corriente fluye a través de él. Su forma analítica difiere entre el MOSFET y el IGBT.

**MOSFET (y SiC MOSFET) — pérdida resistiva.**

$$ P_{cond,MOS}=R_{ds(on)}\,I_{rms}^2 $$

La resistencia \( R_{ds(on)} \) es constante (a temperatura fija), por lo que la pérdida crece con el cuadrado de la corriente RMS. Esta es la contribución del drenador; el diodo en antiparalelo añade una pérdida adicional durante la conducción de corriente de roue. El \( R_{ds(on)} \) aumenta con la temperatura (coeficiente positivo) y con la tensión de bloqueo.

**IGBT — pérdida bilineal.**

$$ P_{cond,IGBT}=V_{ce(sat)}\,I_{avg}+r_{CE}\,I_{rms}^2 $$

donde \( V_{ce(sat)} \) es la caída de saturación (≈1.5–2.5 V) e \( I_{avg} \) es la corriente media de colector. El término \( r_{CE}\,I_{rms}^2 \) (resistencia dinámica) es usualmente secundario. Para un factor de potencia ≈1 y modulación SPWM:

$$ I_{avg,IGBT}\approx\frac{\hat I}{\pi},\quad I_{rms,IGBT}\approx\frac{\hat I}{2} $$

Ejemplo: \( \hat I=100\,\text{A} \), \( V_{ce(sat)}=1.8\,\text{V} \), \( r_{CE}=5\,\text{m}\Omega \):

$$ P_{cond}=1.8\times\frac{100}{\pi}+0.005\times\left(\frac{100}{2}\right)^2=57.3+12.5=69.8\,\text{W} $$

**Comparativa en el punto de diseño.** Para el mismo inversor (690 V, 100 A de pico de fase):
- IGBT: \( P_{cond}\approx70\,\text{W/interruptor} \), \( P_{sw}\approx50\,\text{W/interruptor} \), total ≈120 W.
- SiC MOSFET: \( R_{ds(on)}=10\,\text{m}\Omega \), \( P_{cond}=0.010\times(100/\sqrt2)^2=50\,\text{W} \), \( P_{sw}\approx10\,\text{W} \), total ≈60 W.

El SiC logra pérdidas totales ~50 % menores a \( f_{sw}=10\,\text{kHz} \). A \( f_{sw}=50\,\text{kHz} \) el IGBT no es viable (\( P_{sw} \) ×5) mientras el SiC solo sube 40 W: la ventaja crece.

## 5 — El gate driver: \( R_g \) controla la velocidad y las pérdidas
El gate driver es el circuito que traduce la señal de control digital (0/5 V) en la señal de compuerta del interruptor (típicamente −15/+15 V para IGBT, −4/+15 V para SiC). Su componente más influyente en el comportamiento dinámico es la **resistencia de compuerta** \( R_g \).

**Circuito equivalente de la compuerta.** La compuerta del MOSFET/IGBT es esencialmente un condensador \( C_{iss}=C_{gs}+C_{gd} \) (para el MOSFET) que debe cargarse y descargarse. El tiempo de conmutación es proporcional a la constante de tiempo \( \tau_g=R_g\,C_{iss} \):

$$ t_{on}\approx R_g\,C_{iss}\,\ln\!\left(\frac{V_{GE,on}-V_{th}}{V_{GE,pl}-V_{th}}\right) $$

donde \( V_{GE,pl} \) es la tensión de meseta Miller (plateau). Una \( R_g \) mayor alarga la transición.

**El trade-off central.** \( R_g \) grande:
- ↑ \( t_{on}+t_{off} \) → ↑ \( E_{sw} \) → ↑ \( P_{sw} \) (pérdidas).
- ↓ \( dv/dt \) y \( di/dt \) → menos EMI, menos estrés en el aislamiento, menos ruido en los drivers de otras ramas.

\( R_g \) pequeña:
- ↓ \( E_{sw} \) → menos pérdidas.
- ↑ \( dv/dt \) → potencialmente \( dV/dt > 10\,\text{kV/\mu s} \) en SiC → problemas de EMI y fallo de aislamiento.
- Riesgo de **disparo parásito**: la corriente de desplazamiento a través de \( C_{gd} \) puede superar el umbral \( V_{th} \) del interruptor complementario y encenderlo → cortocircuito de rama.

La tabla muestra valores típicos:

| Tecnología | \( R_g \) on/off típica | \( dV/dt \) resultante | Riesgo |
|---|---|---|---|
| IGBT 1200 V | 10–22 Ω / 5–10 Ω | 2–5 kV/µs | disparo parásito bajo |
| SiC 1200 V | 2–10 Ω / 1–5 Ω | 5–50 kV/µs | alto, requiere \( R_g \) negativa |

**Resistencia de compuerta negativa al apagar.** Para el SiC, se usan dos resistencias: \( R_{g,on} \) y \( R_{g,off} \), con la de apagado menor o incluso conectada a una tensión negativa (−4 V) para acelerar el apagado y forzar que \( V_{GS} \) quede bien por debajo de \( V_{th} \) durante el pico de \( dv/dt \).

**El gate driver también protege:** desaturación (detecta que \( V_{ce} \) sube por encima de un umbral durante conducción → cortocircuito), bajo voltaje de compuerta (UVLO) y algunos incluyen medida de temperatura.

## 6 — Diseño iterativo: elegir el semiconductor para un VSC 1 MVA, 690 V, \( f_{sw}=10\,\text{kHz} \)
**Datos del problema.** Convertidor trifásico GFM, \( S_n=1\,\text{MVA} \), \( V_{LL}=690\,\text{V} \), \( f_{sw}=10\,\text{kHz} \). Bus DC nominal \( V_{DC}=1100\,\text{V} \) (para modular sin sobremodulación). Corriente de fase pico: \( \hat I=S_n\sqrt{2}/(\sqrt{3}V_{LL})=1\times10^6\times\sqrt2/(\sqrt3\times690)=1183\,\text{A} \). Un módulo de potencia puede manejar hasta 600–800 A; se usarán módulos en paralelo o módulos de 1200 A.

**Paso 1 — tensión de bloqueo.** Los dispositivos deben bloquear \( V_{DC}=1100\,\text{V} \). Se necesita un margen de seguridad ×1.5–2: \( V_{br}\geq1700\,\text{V} \). Candidatos: IGBT 1700 V o SiC MOSFET 1700 V.

**Paso 2 — estimación de pérdidas de conmutación (IGBT 1700 V).** Datos típicos de hoja: \( E_{on}+E_{off}=25\,\text{mJ} \) a \( V_{DC}=900\,\text{V} \), \( I=600\,\text{A} \). Escalando a 1100 V y 600 A:

$$ E_{sw}=25\times10^{-3}\times\frac{1100}{900}\times1=30.6\,\text{mJ/evento} $$

$$ P_{sw,total}=6\times30.6\times10^{-3}\times10^4=18.4\,\text{kW} \quad(1.84\%\text{ de }1\,\text{MVA}) $$

**Paso 3 — estimación de pérdidas de conmutación (SiC MOSFET 1700 V).** Datos típicos: \( E_{on}+E_{off}=5\,\text{mJ} \) a condiciones similares.

$$ P_{sw,SiC}=6\times5\times10^{-3}\times\frac{1100}{900}\times10^4=3.7\,\text{kW}\quad(0.37\%) $$

**Paso 4 — pérdidas de conducción (IGBT 1700 V, \( V_{ce(sat)}=2.0\,\text{V} \)).** \( I_{avg,IGBT}\approx\hat I/\pi=1183/\pi\approx377\,\text{A} \) (por interruptor). \( P_{cond}=6\times2.0\times377=4.5\,\text{kW}\,(0.45\%) \).

**Paso 5 — pérdidas de conducción (SiC MOSFET 1700 V, \( R_{ds(on)}=3\,\text{m}\Omega \)).** \( I_{rms}=\hat I/2=591\,\text{A} \). \( P_{cond}=6\times3\times10^{-3}\times591^2=6.3\,\text{kW}\,(0.63\%) \).

**Paso 6 — comparativa total.**

| Tecnología | \( P_{sw} \) | \( P_{cond} \) | \( P_{total} \) | \( \eta \) |
|---|---|---|---|---|
| IGBT 1700 V | 18.4 kW | 4.5 kW | 22.9 kW | 97.7 % |
| SiC MOSFET 1700 V | 3.7 kW | 6.3 kW | 10.0 kW | 99.0 % |

A \( f_{sw}=10\,\text{kHz} \) el SiC ya supera al IGBT. Si se baja a \( f_{sw}=4\,\text{kHz} \), el IGBT mejoraría a ≈10 kW total, igualando al SiC; pero el filtro LCL requeriría más inductancia. Para este proyecto (\( f_{sw}=10\,\text{kHz} \)) el SiC ofrece mejor eficiencia al coste de mayor precio por unidad.

**Paso 7 — impacto sobre el control.** El SiC permite \( f_{sw}=10\,\text{kHz} \) con mayor margen para subir hasta 20–50 kHz si se quisiera. Con IGBT a 10 kHz el filtro LCL se diseña con \( f_{res}\approx1\,\text{kHz} \) (§1 de [[filtro-lcl]]); con SiC a 20 kHz se podría reducir \( L_1 \) a la mitad y la inductancia a 25 % del peso y tamaño originales. El time dead también cae: IGBT requiere 2–3 µs de muerto (distorsión notable), SiC solo 200–300 ns.

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

## Procedimiento de diseño (genérico)
1. Elige el tipo según tensión/corriente/\( f_{sw} \) (IGBT para el VSC de red típico).
2. Estima pérdidas de conducción + conmutación para dimensionar el disipador.
3. Fija el tiempo muerto (decenas–cientos de ns para SiC; 1–3 µs para IGBT).
4. Elige \( R_g \) según el trade-off pérdidas vs EMI; usa resistencias distintas para encendido y apagado en SiC.
5. Revisa el impacto sobre el diseño del LCL y la ganancia del modulador (ver tabla).
6. Si cambias de 2 a 3 niveles: ajusta \(K_m\) y re-sintoniza los PI de corriente.

## Ejemplo de código
```python
# Estimacion de perdidas para un VSC 1 MVA / 690 V
import numpy as np

Vdc = 1100.0       # bus DC [V]
Vpico = 690*np.sqrt(2/3)  # pico de fase [V]
Ipico = 1e6 / (1.5 * Vpico)  # pico de corriente de fase [A]

# IGBT 1700 V
Eon_igbt = 15e-3   # [J] a Vref=900 V, Iref=600 A
Eoff_igbt = 10e-3
Vref, Iref = 900.0, 600.0
Esw_igbt = (Eon_igbt+Eoff_igbt) * (Vdc/Vref) * (Ipico/Iref)
Psw_igbt = 6 * Esw_igbt * 10e3
Vce_sat, Iavg = 2.0, Ipico/np.pi
Pcond_igbt = 6 * Vce_sat * Iavg

# SiC MOSFET 1700 V
Esw_sic = (1e-3+0.5e-3) * (Vdc/Vref) * (Ipico/Iref)
Psw_sic = 6 * Esw_sic * 10e3
Rds_on = 3e-3
Irms = Ipico / 2
Pcond_sic = 6 * Rds_on * Irms**2

print(f"IGBT: Psw={Psw_igbt/1e3:.1f} kW, Pcond={Pcond_igbt/1e3:.1f} kW")
print(f"SiC:  Psw={Psw_sic/1e3:.1f} kW, Pcond={Pcond_sic/1e3:.1f} kW")
```

## Parámetros y valores típicos
\( f_{sw} \) en VSC de red: 2–20 kHz (IGBT), 20–100 kHz (SiC). \( V_{ce(sat)} \) de IGBT ≈ 1.5–2.5 V.
Tiempo muerto: 1–3 µs para módulos IGBT; 100–300 ns para SiC.
\( R_g \) IGBT: 10–22 Ω (on) / 5–10 Ω (off). \( R_g \) SiC: 2–10 Ω (on) / 1–5 Ω (off).

## Errores comunes
- Omitir el tiempo muerto en el modelo \( \to \) cortocircuito de rama (en hardware, destrucción).
- Despreciar las pérdidas de conmutación al subir \( f_{sw} \).
- Suponer interruptores ideales y olvidar la distorsión por dead time.
- Usar \( R_g \) demasiado pequeña en SiC sin tensión negativa de compuerta → disparo parásito.
- Escalar \( E_{sw} \) de la hoja sin corregir por tensión y corriente reales.

## Uso en proyectos
- **01 - GFM-Impedance** (validación PLECS): el modelo conmutado usa medios puentes IGBT con PWM a
  10 kHz; se compara con el promediado (diferencia ≈ 0.67 %).

## 7 — Pérdidas totales y temperatura de unión: el modelo térmico RC

La temperatura de unión \( T_j \) es el parámetro que limita la vida del semiconductor. Un modelo térmico permite estimar \( T_j \) a partir de las pérdidas calculadas en §§3–4.

**Paso 1 — el modelo térmico de una etapa.** En régimen permanente, la potencia disipada fluye del chip a través de la pasta térmica, el substrato de cobre, el disipador y finalmente al aire. Cada interfaz tiene una resistencia térmica:

$$ T_j = P_{loss}\cdot(R_{th,jc} + R_{th,cs} + R_{th,sa}) + T_{amb} $$

donde \( R_{th,jc} \) (unión–carcasa), \( R_{th,cs} \) (carcasa–disipador), \( R_{th,sa} \) (disipador–aire), y \( T_{amb} \) es la temperatura ambiente.

**Paso 2 — red RC de Foster (modelo dinámico).** Para ciclos térmicos rápidos (p.ej. variaciones de carga a decenas de Hz), la temperatura de unión oscila. La red de Foster modela \( Z_{th,jc}(t) \) como suma de exponenciales:

$$ Z_{th,jc}(t)=R_{th,jc}\left[1-\sum_{k=1}^{N}r_k\,e^{-t/\tau_k}\right], \qquad \sum_{k}r_k=1 $$

Los parámetros \( (r_k, \tau_k) \) están en la hoja de datos como tabla de la red de Foster (típicamente 4–5 etapas para un módulo IGBT). El modelo de Cauer es físicamente más correcto pero menos común en hojas de datos.

**Paso 3 — ejemplo numérico.** Para el módulo del §6 (SiC, \( P_{total}=10\,\text{kW}/6=1667\,\text{W/módulo} \)):
- \( R_{th,jc}=0.05\,\text{°C/W} \) (del datasheet)
- \( R_{th,cs}=0.02\,\text{°C/W} \) (pasta de alta conductividad)
- \( R_{th,sa}=0.03\,\text{°C/W} \) (disipador con ventilador)
- \( T_{amb}=40\,\text{°C} \)

$$ T_j = 1667 \times (0.05+0.02+0.03) + 40 = 1667\times0.10 + 40 = 166.7+40 = 207\,\text{°C} $$

Supera \( T_{j,max}=200\,\text{°C} \) de los SiC: se necesita un disipador con menor \( R_{th,sa} \) o refrigeración líquida (\( R_{th,sa}\approx0.005\text{–}0.015\,\text{°C/W} \)).

**Paso 4 — margen de temperatura.** En diseño se reserva un margen de 15–25 °C para cubrir envejecimiento, tolerancias de fabricación y variaciones de \( T_{amb} \): el objetivo real es \( T_j \leq T_{j,max}-20\,\text{°C} \). Para el SiC: \( T_{j,obj}=180\,\text{°C} \) → máxima disipación por módulo: \( P_{mod,max}=(180-40)/0.10=1400\,\text{W} \).

## 8 — IGBT vs SiC MOSFET: comparativa técnica sistemática

La elección entre IGBT de Si y SiC MOSFET es la decisión principal en el diseño de un VSC moderno. Los criterios son múltiples y algunos van en sentidos opuestos.

**Paso 1 — tensión de bloqueo y conducción.** El IGBT utiliza inyección bipolar para reducir la resistencia en conducción; la caída \( V_{ce,sat} \approx 1.5\text{–}2.5\,\text{V} \) es casi independiente de la tensión de bloqueo. El SiC MOSFET aprovecha el campo de ruptura ×10 mayor del SiC para crear un canal MOSFET con \( R_{ds,on} \) bajo incluso a 1200–3300 V:

$$ R_{ds,on,SiC} \propto V_{br}^{2.4} \quad \text{(frente a } V_{br}^{2.5}\text{ en Si)} $$

A 1200 V: \( R_{ds,on,SiC}\approx5\text{–}15\,\text{m}\Omega \) vs \( R_{ds,on,Si}\approx100\text{–}300\,\text{m}\Omega \) — una diferencia de ×10 a ×20.

**Paso 2 — pérdidas de conmutación.** El IGBT sufre la **cola de corriente** al apagar: los portadores minoritarios inyectados tardan en recombinarse, prolongando \( t_{off} \) y aumentando \( E_{off} \). El SiC carece de portadores minoritarios → \( E_{sw} \) entre 5× y 10× menor a la misma tensión:

$$ E_{sw,SiC} \approx \frac{E_{sw,IGBT}}{5\text{–}10} $$

**Paso 3 — temperatura máxima y ciclos térmicos.** Los SiC soportan hasta 200–250 °C (vs 150–175 °C del Si), lo que permite reducir el tamaño del disipador. Sin embargo, los materiales de encapsulado (pasta de Ag sinterizada, substrato de AlN/SiN) deben ser compatibles con esas temperaturas.

**Paso 4 — tabla comparativa sintetizada.**

| Criterio | Si IGBT (1700 V) | SiC MOSFET (1700 V) | Ganador |
|---|---|---|---|
| \( V_{ce,sat} \) / \( R_{ds,on} \) | 2.0 V | 8 mΩ | empate (depende de carga) |
| \( E_{sw} \) (1100 V, 300 A) | 25 mJ | 4 mJ | **SiC** (×6) |
| \( T_{j,max} \) | 175 °C | 225 °C | **SiC** |
| Precio (2025) | 1× | 3–4× | **IGBT** |
| \( f_{sw,max} \) práctica | 20 kHz | 150 kHz | **SiC** |
| Disponibilidad en alta corriente | alta (>1 kA módulo) | media (creciendo) | **IGBT** |
| Ruido EMI | bajo | alto (\( dV/dt \) alto) | **IGBT** |

**Conclusión de diseño.** Para VSC de red (690 V–6 kV, 100 kVA–10 MVA) con \( f_{sw}\leq10\,\text{kHz} \): el IGBT sigue siendo competitivo en coste. Para \( f_{sw}>15\,\text{kHz} \) o cuando la eficiencia es crítica (>99 %), el SiC es claramente superior. La tendencia es que el coste del SiC caiga ×2 cada 5–7 años, desplazando progresivamente al IGBT.

## 9 — Ciclo de vida y fiabilidad: modelo de Coffin-Manson

La fiabilidad del semiconductor define el MTBF (Mean Time Between Failures) del convertidor. El mecanismo de fallo dominante es el **fatiga termomecánica** de las uniones de soldera o de la metalización, causada por los ciclos térmicos durante la operación.

**Paso 1 — ciclos térmicos y amplitud de temperatura.** Cada vez que el semiconductor carga/descarga (ciclo de la demanda, ciclo diario), la unión experimenta un ciclo térmico de amplitud \( \Delta T_j \). La metalización de aluminio y las soldaduras tienen coeficientes de expansión térmica diferentes → aparecen tensiones mecánicas repetidas → fatiga.

**Paso 2 — modelo de Coffin-Manson.** El número de ciclos hasta fallo \( N_f \) sigue la ley de Coffin-Manson adaptada para semiconductores de potencia:

$$ \boxed{N_f = A \cdot \Delta T_j^{-\alpha} \cdot e^{E_a/(k_B T_{j,mean})}} $$

donde:
- \( A \): constante de material (depende del tipo de módulo y proceso)
- \( \alpha \): exponente típicamente 5–7 para soldaduras de Sn, 4–6 para metalización de Al
- \( E_a \): energía de activación ≈ 0.5–1.2 eV
- \( k_B \): constante de Boltzmann
- \( T_{j,mean} \): temperatura media de la unión durante el ciclo

**Paso 3 — ejemplo de estimación de vida.** Convertidor fotovoltaico en campo español: ciclo diario de 8 h de generación, \( \Delta T_j \approx 40\,\text{°C} \), \( T_{j,mean}\approx90\,\text{°C} \). Con parámetros del modelo para IGBT típico (\( A=3.4\times10^{14} \), \( \alpha=6 \), \( E_a=0.68\,\text{eV} \)):

$$ N_f \approx 3.4\times10^{14}\times40^{-6}\times e^{0.68/(8.62\times10^{-5}\times363)} = 3.4\times10^{14}\times\frac{1}{4.1\times10^{9}}\times e^{21.7} $$

$$ N_f \approx 3.4\times10^{14}\times 2.4\times10^{-10}\times 2.7\times10^9 \approx 2.2\times10^5 \text{ ciclos} $$

Con 1 ciclo diario: vida estimada ≈ 600 años → la fatiga del ciclo diario no es el problema. El problema son los **microciclos** asociados al paso de nubes: cientos de ciclos/día de \( \Delta T_j\approx10\text{–}20\,\text{°C} \), que con \( \alpha=6 \) reducen \( N_f \) en \( (40/15)^6\approx500\times \) → vida real del módulo IGBT ≈ 1200 días en ese perfil.

**Paso 4 — diseño para MTBF > 200 000 h.** Para convertidores de larga vida (20 años = 175 000 h de operación) en parques eólicos u offshore:
1. Reducir \( \Delta T_j \) bajando la potencia nominal del módulo un 20–30 % (margen de corriente).
2. Usar pasta de Ag sinterizada en vez de soldadura convencional: \( N_f \) ×5–10 mayor.
3. Substrato cerámico de AlN (baja expansión térmica) en vez de Al₂O₃: menos tensión mecánica.
4. Monitorización on-line de \( T_j \) estimada mediante el parámetro \( V_{CE,0} \) (o \( V_{GS,th} \) para SiC) como indicador de envejecimiento → mantenimiento predictivo.

<div class="cfig"><img src="../figuras/semiconductores-potencia-analisis.png" alt="comparativa pérdidas IGBT vs SiC y temperatura de unión"><div class="cap">Panel (a): pérdidas de conducción vs corriente para SiC MOSFET (cuadrática) e IGBT (lineal). Panel (b): pérdidas de conmutación totales vs frecuencia de conmutación — el cruce IGBT/SiC ocurre entre 5 y 15 kHz según la tensión del bus. Panel (c): temperatura de unión vs potencia disipada para distintas resistencias térmicas totales. Panel (d): SOA del IGBT 1200 V con límite térmico y de pulso.</div></div>

## 10 — Recuperación inversa del diodo: pérdida extra y soluciones

El **diodo en antiparalelo** (freewheeling diode) de cada interruptor introduce pérdidas adicionales por **recuperación inversa** que el modelo simplificado del §1 no incluye completamente.

**Paso 1 — la corriente de recuperación inversa \( I_{rr} \).** Cuando el diodo conduce y se le aplica tensión inversa (el interruptor complementario entra en ON), los portadores almacenados deben extraerse antes de que el diodo bloquee. Esto genera un pico de corriente inversa \( I_{rr} \) de duración \( t_{rr} \):

$$ Q_{rr} = \frac{1}{2}I_{rr}\,t_{rr}, \qquad E_{rr} = \frac{1}{2}Q_{rr}\,V_{DC} $$

Esta energía se disipa en el diodo **y** en el interruptor que está entrando en conducción (la corriente de recuperación pasa por él).

**Paso 2 — clasificación de diodos por velocidad.** Los diodos de Si convencionales tienen \( t_{rr}\approx1\text{–}10\,\mu\text{s} \) — demasiado lento para >5 kHz. Los **diodos ultrarrápidos** (Fast Recovery Epitaxial Diode, FRED) alcanzan \( t_{rr}<100\,\text{ns} \). Los **módulos SiC** usan diodos SiC Schottky que prácticamente no tienen portadores minoritarios → \( Q_{rr}\approx0 \), solo la capacidad de unión contribuye.

**Paso 3 — impacto en el IGBT.** En un módulo IGBT con diodo de Si, la energía total de conmutación medida en la hoja de datos **ya incluye** la contribución de \( E_{rr} \) del diodo comanejado, por eso \( E_{on} \) (el encendido del IGBT) contiene el efecto de la recuperación del diodo opuesto. Al usar un módulo IGBT con diodo SiC en antiparalelo (configuración híbrida), \( E_{on} \) cae significativamente (30–50 %) aunque el transistor sea Si IGBT.

**Paso 4 — cuantificación.** Para el módulo de referencia (IGBT 1700 V, \( I_{rr}=80\,\text{A} \), \( t_{rr}=500\,\text{ns} \), \( V_{DC}=1100\,\text{V} \)):

$$ Q_{rr}=\frac{1}{2}\times80\times500\times10^{-9}=20\,\mu\text{C} $$

$$ E_{rr}=\frac{1}{2}\times20\times10^{-6}\times1100=11\,\text{mJ} $$

A \( f_{sw}=10\,\text{kHz} \): \( P_{rr}=6\times11\times10^{-3}\times10^4=6.6\,\text{kW} \) — una fracción significativa de las pérdidas totales. Con diodo SiC Schottky en antiparalelo, \( E_{rr}\approx0.5\,\text{mJ} \) → \( P_{rr}\approx0.3\,\text{kW} \).

## 11 — Pérdidas por conducción y conmutación: resumen unificado

Las pérdidas en un semiciclo completo del inversor suman las contribuciones del IGBT y del diodo en antiparalelo.

**Conducción:**

$$P_{cond,IGBT} = V_{ce,sat}\,I_c\,D, \qquad P_{cond,diodo} = V_F\,I_F\,(1-D)$$

donde \(D\) es el ciclo de trabajo promedio. A plena carga \(D\approx0.5\) y ambas contribuciones son comparables.

**Conmutación:**

$$P_{sw} = (E_{on}+E_{off})\,f_s$$

Las energías \(E_{on}\) y \(E_{off}\) se leen de las curvas del fabricante a \(V_{dc,test}\) e \(I_{c,test}\) y se escalan como

$$E_{sw}(V,I) = E_{sw,test}\cdot\frac{V}{V_{dc,test}}\cdot\frac{I}{I_{c,test}}$$

**Recuperación del diodo:** añade \(E_{rr}=(1/2)I_{rr}\,t_{rr}\,V_{dc}\) por conmutación; con diodo SiC Schottky \(E_{rr}\approx0\).

**Regla de diseño:** para IGBT de 1700 V a \(f_s=10\,\text{kHz}\), \(P_{sw}\approx P_{cond}\); a \(f_s=20\,\text{kHz}\) domina la conmutación → interesa SiC.

<div class="cfig"><img src="../figuras/semiconductores-potencia-analisis.png" alt="Análisis de pérdidas, temperatura, IGBT vs SiC y fiabilidad de semiconductores de potencia"><div class="cap">(a) Pérdidas conducción+conmutación vs corriente para IGBT y SiC. (b) Pérdidas totales vs frecuencia de conmutación. (c) Red térmica RC de dos capas Foster. (d) Eficiencia total IGBT vs SiC vs frecuencia.</div></div>

## 12 — Temperatura de unión y red térmica

La temperatura de unión \(T_j\) determina la vida útil. El modelo térmico de Foster de dos capas:

$$T_j = P_{loss}\cdot(R_{th,jc,1}(1-e^{-t/\tau_1})+R_{th,jc,2}(1-e^{-t/\tau_2})) + T_c$$

En régimen permanente:

$$T_j = P_{loss}\,R_{th,jc} + T_c, \qquad T_c = P_{loss}\,R_{th,cs} + T_s$$

donde \(R_{th,jc}\approx0.1\)–\(0.3\,\text{K/W}\), \(R_{th,cs}\approx0.05\,\text{K/W}\) (pasta térmica), \(T_s=T_{amb}+P_{loss}\,R_{th,sa}\).

**Limitación de corriente por temperatura:** los fabricantes indican la corriente continua máxima \(I_{C,max}(T_c)\); a \(T_c=80\,°\text{C}\) el IGBT puede conducir solo el 60–70% de la corriente nominal de 25 °C.

**Criterio de diseño:** mantener \(T_j<125\,°\text{C}\) (IGBT Si) o \(<175\,°\text{C}\) (SiC) con margen térmico de 20 K.

## 13 — IGBT vs SiC MOSFET: comparativa técnica

| Parámetro | IGBT Si (1700 V) | SiC MOSFET (1700 V) |
|---|---|---|
| Tensión de saturación/conducción | \(V_{ce,sat}\approx2\,\text{V}\) | \(R_{ds,on}\approx25\,\text{m}\Omega\) |
| Pérdidas conducción @ 100 A | \(\approx200\,\text{W}\) | \(\approx250\,\text{mW}\cdot100^2=250\,\text{W}\) (*) |
| \(E_{on}+E_{off}\) @ 10 kHz | \(\approx150\,\text{mJ}\) | \(\approx25\,\text{mJ}\) |
| \(f_s\) óptima | 2–16 kHz | 20–100 kHz |
| \(T_{j,max}\) | 150–175 °C | 200 °C |
| Coste relativo | 1× | 2–4× |

(*) A corrientes altas \(I>50\,\text{A}\) el IGBT conduce mejor que SiC porque \(V_{ce,sat}\) no crece con \(I^2\).

**Ventaja SiC:** \(f_s\) ×5–10 permite filtros LCL 5–10× más pequeños y disipadores compactos. El sobreprecio se recupera en ahorro de magnéticos y refrigeración.

## 14 — Fiabilidad y ciclo de vida: modelo de Coffin-Manson

Los ciclos térmicos \(\Delta T_j\) producen fatiga en los bonds de aluminio. El número de ciclos hasta fallo:

$$N_f = A\,(\Delta T_j)^{-n}, \quad n\approx5\text{–}6,\; A\approx3\times10^{14}$$

Para una misión típica de 20 años con ciclos diarios \(\Delta T_j=40\,\text{K}\):

$$N_f \approx 3\times10^{14}\cdot40^{-6} \approx 7.3\times10^6 \text{ ciclos}$$

La vida real se acumula usando la regla de Miner: \(\sum_i n_i/N_{f,i} < 1\).

**MTBF:** los módulos de alta calidad alcanzan MTBF > 200 000 h. Diseñar para \(\Delta T_j < 50\,\text{K}\) por ciclo de misión garantiza \(N_f > 10^6\) ciclos.

**Acciones de diseño:** termistores NTC integrados en el módulo; control adaptativo de \(f_s\) según \(T_j\); derating del 20% en corriente respecto al límite absoluto.

## Conceptos relacionados
- [[convertidor-vsc]] · [[simulacion-conmutada]] · [[topologias-multinivel]]

## Referencias
- Mohan, Undeland & Robbins, *Power Electronics*.
- Millan et al., *A Survey of Wide Bandgap Power Semiconductor Devices*, IEEE TPEL 2014.
