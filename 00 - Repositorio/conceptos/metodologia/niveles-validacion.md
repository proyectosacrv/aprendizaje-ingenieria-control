---
titulo: Niveles de validación (fidelidad creciente)
slug: niveles-validacion
categoria: metodologia
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [validar el control subiendo niveles de realismo hasta el hardware]
tags: [validacion, fidelidad, conmutado, HIL, hardware, PLECS]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [validacion-cruzada, pruebas-validacion, convertidor-vsc, medicion-impedancia-inyeccion]
referencias:
  - "Lauss et al., Characteristics and Design of Power-HIL Simulations, IEEE TIE 2016"
---

## Definición
Escalera de modelos de **realismo creciente** por la que pasa un control antes de llegar al
hardware. Cada nivel añade efectos que el anterior ignoraba; subir solo cuando el nivel previo
está validado.

## Fundamento teórico
1. **Modelo lineal** (análisis): polos, impedancia, márgenes. Donde se **diseña**. Rápido pero
   solo pequeña señal alrededor de un punto.
2. **Modelo no lineal / promediado** (simulación temporal): gran señal, saturaciones, faltas,
   escalones grandes. Captura no linealidades pero no la conmutación. Ver [[convertidor-vsc|modelo promediado]].
3. **Modelo conmutado** (PLECS/Spice): IGBTs, PWM, rizado, retardo de cómputo, muestreo,
   cuantización. La "verdad" de simulación.
4. **HIL** (Hardware-in-the-Loop): el control **real** (DSP/FPGA) contra la planta simulada en
   tiempo real. Valida el código, los tiempos y la implementación digital sin arriesgar potencia.
5. **Prototipo / hardware**: la realidad (parásitos, EMI, térmica, tolerancias).

Cada salto añade riesgo de descubrir algo nuevo; el coste y el tiempo también crecen.

<div class="cfig"><img src="figuras/niveles-validacion-escalera.png" alt="escalera de niveles de validacion de fidelidad creciente"><div class="cap">Escalera de validación de realismo creciente: del modelo lineal (donde se diseña) al no lineal (gran señal, faltas), al conmutado (PWM, retardo, rizado), al HIL (control real contra planta en tiempo real) y al hardware. Cada salto añade física, coste y riesgo de descubrir algo nuevo; se sube solo cuando el nivel previo está validado.</div></div>

## 1 — Ejemplo cuantitativo: qué aparece en cada salto de nivel en el GFM
**Nivel 1 → Nivel 2 (lineal → no lineal/promediado).** En el lineal, el modo de potencia aparece a \( f_n=3.3\,\text{Hz} \) con \( \zeta=0.40 \). En el no lineal, ante un escalón de carga del 50 %, la corriente pico es 1.12 p.u. (inside del current limiting de 1.5 p.u. \( \checkmark \)) y el sobreimpulso de tensión es 7 %. Nuevo hallazgo: el feedforward de carga, estable en el lineal, provoca un pico transitorio del 12 % en el no lineal (no linealidad de la saturación del modulador) → se elimina.

**Nivel 2 → Nivel 3 (promediado → conmutado).** El promediado predice THD de corriente 0 % (no modela conmutación). El conmutado a \( f_{sw}=10\,\text{kHz} \) mide THD = 3.2 % (rizado en los armónicos \( f_{sw}\pm 2f_1 \)). El filtro LCL dimensionado cumple el límite de 5 % \( \checkmark \). Nuevo hallazgo: el retardo de cómputo de \( 1\,T_s=100\,\mu\text{s} \) reduce el margen de fase de corriente de 72° a 54° — aún cumple 45° \( \checkmark \) pero ajusta el margen.

**Nivel 3 → Nivel 4 (conmutado → HIL).** El firmware en DSP introduce una latencia adicional de \( 0.5\,T_s \) por el muestreo del ADC — el margen baja a 48°, límite. El HIL detecta esto sin riesgo; en hardware habría sido un rediseño costoso.

La escalera es económicamente eficiente: cada nivel nuevo detecta un problema diferente y el coste de arreglarlo crece con el nivel.

## Cuándo y por qué se usa
Para no llevar a hardware un diseño que falla por algo que un nivel intermedio habría detectado
barato. Estructura el "de la teoría a la realidad".

## Procedimiento (genérico)
1. Diseña y evalúa en el nivel lineal.
2. Sube a no lineal: prueba gran señal (faltas, current limiting).
3. Sube a conmutado: comprueba que el promediado seguía siendo válido (rizado, retardos).
4. HIL: porta el control al hardware de control contra planta en tiempo real.
5. Hardware: pruebas finales con todas las protecciones.
Vuelve atrás si un nivel revela un problema.

## Parámetros y valores típicos
Validez del promediado: \( f_{sw}/f_{control}\gtrsim 10 \). HIL: paso de tiempo del simulador
~µs. El retardo de cómputo (1–1.5 periodos de muestreo) suele aparecer en conmutado/HIL.

## Errores comunes
- Saltarse niveles ("del lineal al hardware"): caro y peligroso.
- No re-evaluar márgenes al añadir el retardo de cómputo (aparece en conmutado/HIL).

## Uso en proyectos
- **01/02**: niveles 1 (lineal: polos, impedancia) y 2 (no lineal: faltas, gran señal). El nivel
  3 (conmutado/PLECS) se valida con [[medicion-impedancia-inyeccion]]; HIL y hardware, pendientes.

## Conceptos relacionados
- [[validacion-cruzada]] · [[pruebas-validacion]] · [[convertidor-vsc|modelo promediado]] · [[medicion-impedancia-inyeccion]]

## Referencias
- Lauss et al., *Power-HIL Simulations*, IEEE TIE 2016.

## 3 — SiL: Software in the Loop

En **SiL** el algoritmo de control se ejecuta en un PC (o servidor de CI) simulando el hardware real: misma lógica de control, misma aritmética de punto flotante o fijo, pero sin DSP físico. La planta se simula en el mismo PC, típicamente en Python/Simulink, sin restricción de tiempo real.

Ventajas de SiL frente al modelo lineal:
- Detecta errores del algoritmo (lógica de saturación, secuencias de arranque, máquinas de estado) que el modelo de señal pequeña ignora.
- Permite pruebas de regresión automatizadas en CI/CD: cada cambio de código genera una suite de simulaciones.
- Más rápido que tiempo real: puede simular 10 s de operación en segundos.

**Herramientas:** Simulink con Code Generation (el mismo código C del DSP se compila para PC), Python con modelos propios, DSPACE ControlDesk (solo software), o simplemente el mismo `solve_ivp` del proyecto con la función de control importada del firmware.

**Criterio de salida del nivel SiL:** todos los casos de prueba (escalón, perturbación, falta, LVRT) superan sus criterios de aceptación en la simulación en tiempo libre.

## 4 — HiL: Hardware in the Loop

En **HiL** el DSP real (equipo bajo prueba, EUT) se conecta a una planta simulada en tiempo real en FPGA o PC de alto rendimiento. El lazo de señal es:

$$ \text{Planta}_{sim} \xrightarrow{\text{ADC}} \text{DSP}_{real} \xrightarrow{\text{PWM}} \text{Planta}_{sim} $$

El bucle HiL introduce un retardo total de interfaz \( T_d = T_{ADC} + T_{comp} + T_{DAC} \), típicamente 1–3 muestras. Este retardo reduce el margen de fase del lazo de corriente:

$$ \Delta\phi = T_d \cdot \omega_c \cdot \frac{180°}{\pi} $$

Para \( T_d = 100\,\mu\text{s} \) y \( \omega_c = 2\pi \times 1000 \) rad/s: \( \Delta\phi \approx 36° \). Si el margen nominal era 72°, el HiL lo reduce a 36° — por debajo del límite de 45°. El HiL detecta este problema sin riesgo para el equipo de potencia.

**Cobertura del HiL:** protecciones de sobrecorriente/sobretensión, LVRT (bajo tensión de red), islanding, arranque y parada, cambio de modo GFL→GFM. Estos casos son peligrosos en hardware real pero seguros en HiL.

**Plataformas:** dSPACE SCALEXIO, OPAL-RT eMEGAsim, Typhoon HIL 402, National Instruments PXI. Todas usan FPGA para resolver la conmutación (\( \Delta t \sim 1\,\mu\text{s} \)) y CPU para la red (\( \Delta t \sim 10\text{–}50\,\mu\text{s} \)).

## 5 — PHiL: Power Hardware in the Loop

En **PHiL** se cierra un lazo físico de potencia real: el inversor bajo prueba ve una red emulada a potencia real, suministrada por un amplificador lineal de potencia.

La **interfaz de estabilidad** es el punto crítico: la impedancia del amplificador \( Z_{amp} \) puede interactuar con la impedancia de la planta simulada \( Z_{sim} \) e inestabilizar el lazo. El criterio del ITM (Ideal Transformer Model) exige:

$$ \left|\frac{Z_{amp}(j\omega)}{Z_{sim}(j\omega)}\right| < 1 \quad \forall\omega \text{ en la banda de interés} $$

Si no se cumple, se añade compensación de fase (filtro lead) en la interfaz o se aumenta \( Z_{sim} \) (red más débil en la simulación).

**Aplicaciones de PHiL:** LVRT a potencia real, compatibilidad electromagnética con la red, pruebas de tipo para certificación IEC. El equipo bajo prueba experimenta tensiones y corrientes reales, con toda la dinámica de la red emulada.

**Coste:** €100k–€1M; justificado para proyectos de potencia >1 MW o para certificación de equipos según IEC 62690 o IEEE Std 1459.

## 6 — Comparativa y elección del nivel

La pirámide V agrupa los niveles por coste (creciente hacia arriba) y cobertura (decreciente hacia arriba):

| Nivel | Coste relativo | Cobertura | Duración típica |
|---|---|---|---|
| SiL | 1× | 95% de la lógica | Semanas (CI) |
| HiL | 5× | 85% (firmware + protecciones) | 1–2 semanas |
| PHiL | 50× | 70% (potencia real, EMC) | Días |
| Prototipo | 200× | 60% | Semanas |
| Campo | 1000× | 40% (condiciones reales) | Meses |

**Regla económica:** un error detectado en SiL cuesta ~10× menos de corregir que el mismo error detectado en prototipo y ~100× menos que en campo. La secuencia recomendada es completar y aprobar cada nivel antes de avanzar al siguiente.

**Criterio de salida de cada nivel:** todos los casos de prueba definidos superan sus criterios de aceptación sin fallo. Los casos no cubiertos por el nivel actual quedan explícitamente pendientes para el nivel siguiente.

**Metodología de transición entre niveles:**

La transición de SiL a HiL no es automática: exige una revisión de los supuestos de modelado. Al pasar de SiL a HiL, los efectos que aparecen por primera vez son:
1. La cuantización del ADC (12-16 bits) introduce un ruido de cuantización de \( \Delta q = V_{ref}/2^N \). Para \( N=12 \) bits y \( V_{ref}=3.3\,\text{V} \): \( \Delta q \approx 0.8\,\text{mV} \) — inapreciable para señales de potencia.
2. El jitter del reloj del DSP (tipicamente < 1 ns) genera un error de posición de muestra que equivale a una variación del ciclo de trabajo de \( \Delta d = \Delta t_{jitter} \cdot f_{sw} \approx 10^{-9} \times 5000 = 5 \times 10^{-6} \) — completamente despreciable.
3. El tiempo de ejecución del ISR (Interrupt Service Routine): si la rutina de control tarda más de \( T_s \) en ejecutarse, el DSP pierde un ciclo. El HiL detecta esto como un overrun del controlador, que en hardware real se manifestaría como una inestabilidad intermitente difícil de reproducir.

**Integración continua (CI) con SiL:**

En proyectos de software embebido para convertidores, el SiL puede integrarse en pipelines de CI/CD (GitHub Actions, Jenkins):
```yaml
# .github/workflows/sil_test.yml
on: [push, pull_request]
jobs:
  sil:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: pip install scipy numpy matplotlib
      - run: python tests/run_sil.py --cases=all --criterion=FIT80
```

Cada push ejecuta automáticamente la suite de pruebas SiL. Si algún caso falla el criterio de aceptación, el PR se bloquea antes de hacer merge. Esto reduce a cero el número de errores que llegan al nivel HiL por descuido.

**Ejemplo cuantitativo de la escalera: GFL de 50 kW**

**Nivel 1 (lineal):** el modelo de espacio de estados linealizado (\( 8 \times 8 \), estados: \( i_d, i_q, i_{2d}, i_{2q}, v_{Cd}, v_{Cq}, \theta_{PLL}, \omega_{PLL} \)) da: polo dominante del PLL a 15 Hz con \( \zeta = 0.62 \), margen de fase del lazo de corriente = 68°, SCR crítico = 3.48 por autovalores.

**Nivel 2 (no lineal / promediado):** escalón de potencia de 20→100% en 50 ms. El current limiting se activa durante 8 ms con pico = 1.32 p.u. — dentro del límite de 1.5 p.u. La inyección de reactiva durante la saturación produce una desviación de ángulo del PLL de 3.2°, recuperada en 45 ms. Nuevo hallazgo: la rampa de referencia programada no respeta el límite de \( dP/dt = 20\,\%/s \) del grid code — se corrige añadiendo un ramp limiter en la referencia de potencia.

**Nivel 3 (conmutado):** THD de corriente en el PCC = 3.8% — cumple el límite de 5% (IEEE 519). El rizado de corriente del inductor \( L_1 \) es 1.6 A p-p a 10 kHz, dentro del margen de diseño. El retardo de cómputo real del DSP reduce el margen de fase de 68° a 51° — aún cumple el límite de 45°.

**Nivel 4 (HiL):** el firmware introduce una latencia adicional de 0.5 \( T_s \) por el pipeline del ADC: margen de fase cae a 43° — por debajo del límite. Solución: compensación de retardo Smith Predictor de 1 \( T_s \) → margen recuperado a 58°. Este problema no habría sido detectable sin HiL.

**Documentación de discrepancias entre niveles:**

Cada discrepancia entre niveles debe quedar documentada en una tabla de trazabilidad:

| Discrepancia | Nivel detectado | Causa | Solución |
|---|---|---|---|
| Feedforward de carga produce pico 12% | Nivel 2 vs 1 | Saturacion del modulador | Eliminado feedforward |
| Ramp rate incumple grid code | Nivel 2 | No modelado en nivel 1 | Añadido ramp limiter |
| Margen de fase 51° (vs 68° lineal) | Nivel 3 | Retardo de computo | Verificado, cumple 45° |
| Margen de fase 43° (vs 51° conmutado) | Nivel 4 (HiL) | Latencia ADC pipeline | Smith Predictor 1Ts |

## 7 — SiL en detalle: arquitectura y criterio de salida

**Arquitectura SiL:** el mismo código C/C++ del DSP se compila para PC (cross-compilation o nativo). La planta se simula en Python/Simulink en tiempo libre — sin restricciones de tiempo real. El lazo de control ejecuta exactamente la misma aritmética (punto fijo o flotante) que el DSP real.

**Lo que SiL detecta que el modelo lineal no detecta:**
- Errores de lógica en la máquina de estados (transiciones de modo GFL→GFM, secuencias de arranque).
- Saturaciones y anti-windup: la saturación del integrador puede producir comportamientos distintos del análisis de pequeña señal.
- Condiciones de carrera en el firmware (interrupciones mal priorizadas).
- Errores de escala o unidades en la conversión de magnitudes físicas a p.u.

**Criterio de salida del nivel SiL:** todos los casos de prueba (escalón de referencia, perturbación de carga, falta trifásica y monofásica, LVRT, cambio de modo) superan sus criterios de aceptación en la simulación en tiempo libre. Los casos no cubiertos quedan explícitamente listados como pendientes para HiL.

**Integración continua:** el SiL se integra en pipelines CI/CD (GitHub Actions, Jenkins). Cada commit ejecuta la suite completa; si algún caso falla el criterio, el PR queda bloqueado.

## 8 — HiL en detalle: retardo de lazo y cobertura de protecciones

**Retardo total de interfaz HiL:** el bucle DSP real ↔ planta simulada en FPGA introduce un retardo total \(T_d=T_{ADC}+T_{comp}+T_{DAC}\), típicamente 1–3 muestras:
$$\Delta\phi = T_d\cdot\omega_c\cdot\frac{180°}{\pi}$$

Para \(T_d=100\,\mu\text{s}\) y \(\omega_c=2\pi\times500\,\text{rad/s}\): \(\Delta\phi\approx18°\). Si el margen nominal era 54°, el HiL lo reduce a 36° — detectado sin riesgo para el equipo de potencia.

**Lo que HiL detecta que SiL no detecta:**
- Latencia real del pipeline del ADC (puede ser 0.5–1.5 \(T_s\) adicionales).
- Tiempo de ejecución del ISR: overrun si la rutina de control excede \(T_s\).
- Jitter del reloj del DSP y su efecto en el ciclo de trabajo del PWM.
- Cuantización del ADC (12–16 bits): ruido de cuantización en señales pequeñas.

**Cobertura de protecciones en HiL:** todas las protecciones de hardware (sobrecorriente, sobretensión, temperatura, LVRT, islanding) se prueban sin riesgo para la potencia real. En hardware, probar una protección de sobrecorriente podría dañar el equipo; en HiL es un caso de prueba estándar.

**Plataformas HiL:** dSPACE SCALEXIO, OPAL-RT eMEGAsim, Typhoon HIL 402, NI PXI. Todas usan FPGA para la conmutación (\(\Delta t\sim1\,\mu\text{s}\)) y CPU para la red (\(\Delta t\sim10\text{–}50\,\mu\text{s}\)).

## 9 — PHiL: amplificador real, interfaz de estabilidad y coste

**Arquitectura PHiL:** el inversor bajo prueba (equipo de potencia real) ve una red emulada a plena potencia suministrada por un amplificador lineal de potencia. El lazo físico cierra tensión o corriente real con la planta simulada en tiempo real en FPGA.

**Interfaz de estabilidad — criterio ITM:** la impedancia del amplificador \(Z_{amp}\) puede interactuar con la impedancia de la planta simulada \(Z_{sim}\). El criterio del Ideal Transformer Model (ITM) exige:
$$\left|\frac{Z_{amp}(j\omega)}{Z_{sim}(j\omega)}\right| < 1 \quad\forall\omega\text{ en la banda de interés}$$
Si no se cumple: añadir compensación de fase en la interfaz o aumentar \(Z_{sim}\) artificialmente.

**Lo que PHiL detecta que HiL no detecta:** comportamiento EMC (compatibilidad electromagnética) real del equipo, disipación térmica, comportamiento de los componentes de potencia (IGBT, diodos) a corriente y tensión reales, y la interacción con la red real a través del amplificador.

**Coste y justificación:** €100k–€1M; justificado para potencia >1 MW o para certificación de tipo (IEC 62690, IEEE 1547-2018). Para proyectos de I+D de convertidores ≤100 kW, el HiL cubre el 85% de los casos a 1/10 del coste.

## 10 — Comparativa coste/cobertura/detección de errores

| Nivel | Coste relativo | Cobertura lógica | Duración | Errores típicos detectados |
|---|---|---|---|---|
| Lineal | 1× | 60% | Horas | Diseño de lazo, márgenes |
| No lineal / promediado | 2× | 75% | Días | Gran señal, saturaciones |
| Conmutado | 3× | 85% | Días | Rizado, retardo de cómputo, THD |
| SiL | 4× | 95% | Semanas (CI) | Lógica, estados, escala |
| HiL | 10× | 85% | 1–2 semanas | Latencia ADC, overrun, protecciones |
| PHiL | 100× | 70% | Días | EMC, térmica, interacción red real |
| Prototipo | 300× | 60% | Semanas | Todo lo anterior + tolerancias fab. |

**Regla económica:** un error detectado en SiL cuesta ~10× menos de corregir que el mismo error detectado en prototipo, y ~100× menos que en campo. La secuencia óptima es completar y aprobar cada nivel antes de avanzar al siguiente.

<div class="cfig"><img src="../figuras/niveles-validacion-analisis.png" alt="pirámide de validación, coste vs cobertura, retardo HiL y detección de errores"><div class="cap">Pirámide de validación: SiL (bajo coste, alta cobertura) hasta campo (alto coste, baja cobertura). El retardo de interfaz HiL reduce el margen de fase del lazo. Los errores detectados en SiL/HiL cuestan órdenes de magnitud menos que los detectados en campo.</div></div>

## Conceptos relacionados
- [[validacion-cruzada]] · [[pruebas-validacion]] · [[convertidor-vsc|modelo promediado]] · [[medicion-impedancia-inyeccion]]

## Referencias
- Lauss et al., *Power-HIL Simulations*, IEEE TIE 2016.
