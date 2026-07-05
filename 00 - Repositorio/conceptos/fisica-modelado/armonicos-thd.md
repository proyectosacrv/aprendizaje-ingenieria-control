---
titulo: Armónicos y THD en sistemas de potencia
slug: armonicos-thd
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance]
objetivos: [cuantificar la distorsión armónica, identificar su origen en convertidores PWM, aplicar límites normativos y diseñar mitigación]
tags: [armonicos, thd, fourier, ieee-519, lcl, filtro-activo, controlador-resonante, pwm, calidad-potencia, intermedio]
fecha_creacion: 2026-07-03
fecha_actualizacion: 2026-07-03
relacionados: [armonicos-thd-convertidores, filtro-lcl, controlador-resonante, series-fourier, convertidor-vsc]
referencias:
  - "IEEE Std 519-2022, Harmonic Control in Electric Power Systems"
  - "IEC 61000-3-2:2018, Limits for harmonic current emissions"
  - "Liserre et al., Design and control of an LCL-filter based three-phase active rectifier, IEEE TIA 2005"
---

## Definición
Los armónicos son componentes de frecuencia que son múltiplos enteros de la fundamental (\( 50\,\text{Hz} \)) presentes en señales de tensión o corriente de un sistema de potencia. Aparecen porque los convertidores de potencia son dispositivos no lineales. La **Distorsión Armónica Total** (THD) cuantifica su peso relativo respecto a la fundamental.

## Fundamento teórico
Para una señal periódica de corriente, la serie de Fourier es:
$$ i(t) = I_1\sqrt{2}\sin(\omega t+\phi_1) + \sum_{n=2}^{\infty}I_n\sqrt{2}\sin(n\omega t+\phi_n) $$
con \( I_n \) el valor RMS del armónico de orden \( n \). La THD de corriente:
$$ \text{THD}_I = \frac{\sqrt{\sum_{n=2}^{\infty}I_n^2}}{I_1}\times100\% $$

El filtro LCL atenúa los armónicos de alta frecuencia con −60 dB/dec por encima de la frecuencia de resonancia \( f_{res}=1/(2\pi\sqrt{L_{eq}C_f}) \).

<div class="cfig"><img src="../figuras/armonicos-thd-analisis.png" alt="4 paneles: espectro corriente inversor LCL, Bode LCL, THD vs L2, filtro activo APF"><div class="cap">
(a) Espectro de la corriente de red \(i_{L2}\) antes y después del LCL: las bandas de conmutación alrededor de \(f_{sw}\) se atenúan drásticamente; los armónicos de bajo orden (5°, 7°) persisten. (b) Bode del filtro LCL \(i_{L2}/i_{L1}\): la atenuación en \(f_{sw}=10\,\text{kHz}\) supera −60 dB. (c) THD en el PCC vs inductancia del filtro \(L_2\): aumentar \(L_2\) mejora el THD a costa de mayor reactancia. (d) Espectro antes y después de la compensación con APF: los armónicos 5° y 7° prácticamente desaparecen.
</div></div>

## 1 — Los armónicos en sistemas de potencia: serie de Fourier y THD

**Paso 1 — la serie de Fourier de una señal periódica.** Cualquier señal periódica de periodo \( T=1/f_1 \) puede descomponerse en su componente fundamental más sus armónicos:
$$ v(t) = V_1\sin(\omega t+\phi_1) + V_2\sin(2\omega t+\phi_2) + V_3\sin(3\omega t+\phi_3) + \ldots = \sum_{n=1}^{\infty}V_n\sin(n\omega t+\phi_n) $$

Los coeficientes de Fourier se calculan por la integral:
$$ V_n = \frac{\sqrt{a_n^2+b_n^2}}{\sqrt{2}},\quad a_n=\frac{2}{T}\int_0^T v(t)\cos(n\omega t)\,dt,\quad b_n=\frac{2}{T}\int_0^T v(t)\sin(n\omega t)\,dt $$

**Paso 2 — el RMS total y su distribución entre armónicos.** Por ortogonalidad de los senos:
$$ I_{rms}^2 = I_1^2 + I_2^2 + \ldots = \sum_{n=1}^{\infty}I_n^2 $$

**Paso 3 — la THD como medida de distorsión.** Normalizando la energía armónica sobre la fundamental:
$$ \boxed{\;\text{THD}_I = \frac{\sqrt{\sum_{n=2}^{\infty}I_n^2}}{I_1}\times100\%\;} $$

En sistemas trifásicos equilibrados sin neutro, los armónicos de orden triple (3°, 9°, 15°…) son de **secuencia homopolar** y no circulan por la línea (se cancelan en el transformador triángulo). Los dominantes son el 5° (secuencia negativa), 7° (positiva), 11° (negativa), 13° (positiva).

**Nota sobre THD vs TDD.** IEEE 519 usa la **TDD** (Total Demand Distortion): normaliza la corriente armónica sobre la corriente de demanda máxima \( I_L \), no sobre la fundamental del instante. Esto es más justo en sistemas que operan parcialmente cargados.

## 2 — El origen de los armónicos en convertidores PWM

**Paso 1 — el modulador SPWM y sus bandas laterales.** La modulación senoidal de ancho de pulso (SPWM) genera una tensión de salida con la fundamental deseada más bandas laterales centradas en múltiplos de \( f_{sw} \):
$$ V_{an}(t) = \frac{m_a V_{dc}}{2}\sin(\omega_1 t) + \sum_{m=1}^{\infty}\sum_{n=-\infty}^{\infty}V_{mn}\sin((m\,\omega_{sw}+n\,\omega_1)t) $$

donde \( m_a=\hat{V}_{ref}/\hat{V}_{tri} \) es el índice de modulación y \( m_f=f_{sw}/f_1 \) es el índice de modulación de frecuencia. Los grupos de armónicos más relevantes:
- Alrededor de \( m_f \): \( m_f\pm2,\;m_f\pm4,\ldots \)
- Alrededor de \( 2m_f \): \( 2m_f\pm1,\;2m_f\pm3,\ldots \)
- Alrededor de \( 3m_f \): \( 3m_f\pm2,\ldots \)

**Paso 2 — el filtro LCL como atenuador.** El filtro LCL (con inductancias \( L_1 \) en el lado inversor y \( L_2 \) en el lado red, y condensador \( C_f \)) atenúa la corriente de red a alta frecuencia con −60 dB/dec por encima de su frecuencia de resonancia:
$$ f_{res} = \frac{1}{2\pi}\sqrt{\frac{L_1+L_2}{L_1\,L_2\,C_f}} $$

La función de transferencia \( i_{L2}(s)/v_{inv}(s) \) cae como \( 1/\omega^3 \) para \( f\gg f_{res} \). Con \( L_1=2\,\text{mH} \), \( L_2=0.5\,\text{mH} \), \( C_f=10\,\mu\text{F} \): \( f_{res}\approx2.25\,\text{kHz} \). A \( f_{sw}=10\,\text{kHz} \) (4.44× \( f_{res} \)):
$$ \text{Aten}=20\log_{10}\!\left(\frac{f_{sw}}{f_{res}}\right)^3\times(-20\,\text{dB/dec})\approx-60\,\text{dB} $$

*(Factor exacto calculado con la función de transferencia completa del LCL.)*

**Paso 3 — los armónicos de baja frecuencia y el tiempo muerto.** Los armónicos de bajo orden (5°, 7°, 11°, 13°) no vienen del SPWM ideal sino de las **no idealidades**:
- El **tiempo muerto** \( t_d \) (pausa entre la apertura de un transistor y el cierre del complementario) introduce un error de tensión casi cuadrado en fase con la corriente. Su amplitud:
  $$ \Delta V_{td} = \frac{t_d}{T_{sw}}\,V_{dc} $$
  Un tiempo muerto de \( t_d=2\,\mu\text{s} \) a \( f_{sw}=10\,\text{kHz} \) con \( V_{dc}=700\,\text{V} \): \( \Delta V_{td}=14\,\text{V} \) → THD de la tensión de salida de \( \approx14/311=4.5\% \) solo por tiempo muerto.
- La **caída de tensión en los semiconductores** (IGBT: 1–3 V) introduce una distorsión de alto orden.
- La **distorsión de la tensión de red** se refleja directamente en la corriente.

## 3 — Los límites normativos: IEEE 519 e IEC 61000-3-2

**IEEE 519-2022** es el estándar más usado en sistemas de potencia industriales. Limita tanto la distorsión de tensión en el PCC (Point of Common Coupling) como la distorsión de corriente por la carga.

**Paso 1 — límites de tensión.** En el PCC para sistemas de distribución (BT y MT):

| Tensión del bus | THD_V máximo | Armónico individual |
|---|---|---|
| BT (< 1 kV) | 8 % | 5 % |
| MT (1–69 kV) | 5 % | 3 % |
| AT (69–161 kV) | 2.5 % | 1.5 % |
| EAT (> 161 kV) | 1.5 % | 1 % |

**Paso 2 — límites de corriente (TDD).** Dependen de la relación de cortocircuito \( SCR = I_{sc}/I_L \):

| SCR = I_sc/I_L | THD_I límite | Orden 5° | Orden 7° | Orden 11° | Orden 13° |
|---|---|---|---|---|---|
| < 20 | 5 % | 4 % | 4 % | 2 % | 2 % |
| 20–50 | 8 % | 7 % | 7 % | 3.5 % | 3.5 % |
| 50–100 | 12 % | 10 % | 10 % | 4.5 % | 4.5 % |
| 100–1000 | 15 % | 12 % | 12 % | 5.5 % | 5.5 % |
| > 1000 | 20 % | 15 % | 15 % | 7 % | 7 % |

**Paso 3 — la IEC 61000-3-2 para equipos de bajo voltaje.** Clasifica los equipos en cuatro clases:
- **Clase A:** equipos trifásicos equilibrados (motores, inversores de potencia media).
- **Clase B:** herramientas portátiles.
- **Clase C:** equipos de iluminación (THD especialmente restrictivo por el 3°).
- **Clase D:** equipos con forma de onda especificada (< 600 W, PCs, fuentes de alimentación).

## 4 — La medición del THD: DFT, sincronización y leakage

**Paso 1 — la DFT de la corriente de línea.** La DFT de \( N \) muestras tomadas a \( f_s \) Hz da la amplitud de cada armónico:
$$ I_n = \frac{2}{N}\left|\sum_{k=0}^{N-1}i(k\,T_s)\,e^{-j2\pi nk/N}\right| $$

La resolución en frecuencia es \( \Delta f = f_s/N \). Para resolver el armónico 5° (250 Hz) de la fundamental con resolución de 50 Hz: \( N=f_s/50 \). Con \( f_s=10\,\text{kHz} \): \( N=200 \) muestras por ciclo.

**Paso 2 — la sincronización con el PLL.** La ventana de observación debe ser exactamente \( M \) ciclos completos de 50 Hz. Si la frecuencia de red es \( f_{grid}=50\pm\epsilon \), una ventana de duración fija \( T_{obs}=M/50 \) no incluye exactamente \( M \) ciclos → leakage espectral: la energía del armónico "se derrama" a las frecuencias adyacentes, subestimando la amplitud real. La solución:

1. Sincronizar \( T_{obs} \) con el PLL: arrancar y parar la adquisición en cruces por cero consecutivos separados exactamente \( M \) periodos medidos por el PLL.
2. Alternativa: usar ventana de Kaiser-Bessel con apodización para reducir el leakage (a costa de peor resolución frecuencial).

**Paso 3 — el efecto del leakage en la estimación del THD.** Sin sincronización correcta, el leakage introduce un suelo espectral que puede elevar artificialmente la estimación de THD en 1–3 puntos porcentuales. Para el cumplimiento normativo, la medición debe hacerse con la ventana sincronizada al PLL.

**Paso 4 — el IEC 61000-4-7 como metodología estándar.** El estándar define cómo medir: ventana de 200 ms (10 ciclos a 50 Hz), sin ventana Hanning (ventana rectangular con sincronización perfecta), promediado temporal de múltiples ventanas.

## 5 — La mitigación: filtro LCL, APF y controlador resonante

**Paso 1 — el filtro LCL (mitigación pasiva).** El filtro LCL atenúa pasivamente las bandas de conmutación de alta frecuencia. El diseño básico parte de especificar la atenuación necesaria a \( f_{sw} \):
$$ \left|\frac{I_{L2}}{I_{L1}}\right|_{f=f_{sw}} = \frac{1}{|1-(f_{sw}/f_{res})^2|} \cdot \frac{1}{(f_{sw}/f_{res})^2} $$
Para la atenuación requerida, se elige \( f_{res} \) suficientemente por debajo de \( f_{sw} \) (regla práctica: \( f_{res} < f_{sw}/5 \)) y se fija el reparto de inductancia \( r=L_2/L_1 \).

**Paso 2 — el filtro activo de potencia (APF).** El APF inyecta corrientes de compensación que se oponen a los armónicos medidos:
$$ i_{APF}(t) = -\sum_{n=5,7,11,13,\ldots}I_n\sqrt{2}\sin(n\omega t+\phi_n) $$

Mide en tiempo real la corriente de carga, extrae los armónicos por transformada de Park o con un banco de filtros resonantes, y los inyecta a través de un VSC conectado en paralelo. La velocidad de respuesta del APF debe ser suficiente para seguir el armónico 25° (1250 Hz), lo que requiere un ancho de banda del lazo de corriente > 5–10 kHz.

**Paso 3 — el controlador resonante (RC).** Para eliminar armónicos específicos en el lazo de corriente del VSC, se añaden resonantes a las frecuencias armónicas:
$$ C_{PR}(s) = K_p + \frac{2K_r\,\omega_c\,s}{s^2+2\omega_c\,s+\omega_h^2} $$
con \( \omega_h=2\pi\,n\,f_1 \) (la frecuencia del armónico a compensar) y \( \omega_c \) el ancho de banda del resonante (típicamente \( 2\pi\times5 \) rad/s). Un banco de resonantes para el 5°, 7°, 11° y 13° puede reducir el THD de 5–7 % a < 2 % sin hardware adicional.

## 6 — Diseño iterativo: inversor 01-GFM con LCL, fsw=10 kHz, verificación IEEE 519

**Parámetros del inversor:** \( f_{sw}=10\,\text{kHz} \), \( V_{dc}=800\,\text{V} \), \( P=100\,\text{kW} \), \( V_{red}=400\,\text{V(L-L)} \), \( I_{nom}=144\,\text{A} \). Filtro LCL: \( L_1=2\,\text{mH} \), \( L_2=0.5\,\text{mH} \), \( C_f=10\,\mu\text{F} \). Subestación: \( S_{cc}=20\,\text{MVA} \), \( SCR=20\,\text{MVA}/(100\,\text{kVA})=200 \) (¡verificar el SCR correcto en el PCC real).

**Paso 1 — frecuencia de resonancia del LCL.**
$$ f_{res} = \frac{1}{2\pi}\sqrt{\frac{L_1+L_2}{L_1\,L_2\,C_f}} = \frac{1}{2\pi}\sqrt{\frac{2.5\times10^{-3}}{10^{-3}}} = \frac{1}{2\pi}\sqrt{\frac{2.5\times10^{-3}}{5\times10^{-10}}}\approx2252\,\text{Hz} $$

*(Más preciso: \( \sqrt{(L_1+L_2)/(L_1 L_2 C_f)}=\sqrt{2.5\times10^{-3}/(10^{-6}\times0.5\times10^{-6}\times10^{-5})} \) — usar la fórmula correcta con \( L_{eq}=L_1 L_2/(L_1+L_2)=0.4\,\text{mH} \)):*
$$ f_{res}=\frac{1}{2\pi\sqrt{0.4\times10^{-3}\times10\times10^{-6}}}=\frac{1}{2\pi\times2\times10^{-4}}\approx795\,\text{Hz} $$

**Paso 2 — atenuación a f_sw.**

La relación \( f_{sw}/f_{res}=10000/795=12.6 \). La atenuación del LCL a esta frecuencia:
$$ \text{Aten}_{LCL}(f_{sw})=\frac{1}{(f_{sw}/f_{res})^2-1}\approx\frac{1}{(12.6)^2}=\frac{1}{158.8}\approx-44\,\text{dB} $$

*(La fórmula exacta del LCL da -60 dB considerando la pendiente cúbica; -44 dB es la cota conservadora.)*

**Paso 3 — THD de corriente en el PCC estimado.** Con los armónicos de conmutación dominantes alrededor de \( f_{sw} \) reducidos en -44 dB (factor 158), su contribución al THD es despreciable. Los armónicos de bajo orden debidos al tiempo muerto (\( t_d=2\,\mu\text{s} \)) son los dominantes:
$$ \text{THD}_{I,5}=\frac{\Delta V_{td}}{V_1}\cdot\frac{6}{\pi}\cdot\frac{1}{5}\approx\frac{14}{311}\cdot\frac{6}{\pi}\cdot0.2\approx1.7\,\% $$

THD total estimado por tiempo muerto (5° + 7° + 11° + 13°): ≈ 2.8 %.

**Paso 4 — verificación vs IEEE 519 para SCR=200 (tabla 50–100).**

Límite de TDD para \( 50 < SCR < 100 \): THD_I < 12 %, orden 5° < 10 %, orden 7° < 10 %. El inversor con LCL cumple con margen. Si se opera a baja carga (<20 % de la nominal), la TDD puede subir porque \( I_L \) baja pero \( I_n \) permanece (tiempo muerto es independiente de la carga) → necesario activar la compensación de tiempo muerto en el controlador para garantizar el cumplimiento en toda la gama de operación.

## 7 — Descomposición en serie de Fourier

**Representación general.** Cualquier señal periódica de período \( T = 1/f_0 \) se expresa como:
$$ x(t) = \sum_{n=1}^{\infty}\!\left(a_n\cos n\omega_0 t + b_n\sin n\omega_0 t\right) $$

**Coeficientes de Fourier.** Se calculan proyectando la señal sobre cada armónico por ortogonalidad:
$$ a_n = \frac{2}{T}\int_0^T x(t)\cos(n\omega_0 t)\,dt, \qquad b_n = \frac{2}{T}\int_0^T x(t)\sin(n\omega_0 t)\,dt $$

La amplitud del armónico de orden \( n \) es:
$$ C_n = \sqrt{a_n^2 + b_n^2} $$

**Espectro de un inversor PWM.** Para modulación SPWM con índice \( m_f = f_{sw}/f_0 \), el espectro teórico contiene:
- La fundamental a \( f_0 \) con amplitud \( m_a V_{dc}/2 \).
- Bandas laterales (sidebands) centradas en \( m \cdot f_{sw} \) con separación \( 2f_0 \): \( m_f\pm2,\; m_f\pm4,\;\ldots \) para \( m=1 \); \( 2m_f\pm1,\; 2m_f\pm3,\;\ldots \) para \( m=2 \).
- Los armónicos de bajo orden (5°, 7°, 11°…) aparecen por no idealidades (tiempo muerto, caídas en semiconductores), no por el SPWM ideal.

## 8 — THD y normativa IEC/IEEE

**Definición de THD de corriente:**
$$ \text{THD}_I = \frac{\sqrt{\sum_{n=2}^{N}I_n^2}}{I_1}\times100\% $$

**Definición de THD de tensión:**
$$ \text{THD}_V = \frac{\sqrt{\sum_{n=2}^{N}V_n^2}}{V_1}\times100\% $$

**IEEE 519-2022: límites de TDD según SCR.** La TDD (Total Demand Distortion) normaliza sobre la corriente de demanda máxima \( I_L \):

| SCR = \( I_{sc}/I_L \) | Límite TDD |
|---|---|
| < 20 (red débil) | 5 % |
| 20–50 | 8 % |
| 50–100 | 12 % |
| 100–1000 | 15 % |
| > 1000 | 20 % |

**IEC 61000-3-2: equipos hasta 16 A por fase.** Clasifica los equipos en clases A–D con límites absolutos en amperios por armónico. Clase A (equipos industriales trifásicos equilibrados): 3° ≤ 2.30 A, 5° ≤ 1.14 A, 7° ≤ 0.77 A.

**Armónicos pares.** En general son pequeños porque la simetría de semiperíodo (\( x(t) = -x(t+T/2) \)) implica que todos los coeficientes de Fourier pares son nulos. Su presencia indica asimetría en el circuito (p.ej., disparo desigual de los semiconductores).

## 9 — Filtros y mitigación

**Filtro pasivo LC en derivación.** Resuena a la frecuencia del armónico dominante \( f_h = h \cdot f_0 \):
$$ L_h C_h = \frac{1}{(2\pi f_h)^2} $$
Ofrece baja impedancia a \( f_h \), desviando el armónico de la red. Económico pero fijo en frecuencia y puede interaccionar con la red (amplificación por resonancia paralela).

**Filtro activo de potencia (APF).** El APF mide la corriente de carga, extrae los armónicos (transformada de Park instantánea o banco de resonantes), y los inyecta en fase opuesta a través de un VSC en paralelo:
$$ i_{APF}(t) = -\sum_{n=5,7,11,\ldots}I_n\sqrt{2}\sin(n\omega_0 t + \phi_n) $$
Requiere ancho de banda del lazo de corriente superior a 5–10 kHz para compensar hasta el armónico 25°.

**Filtro híbrido.** Combina un filtro pasivo sintonizado al armónico dominante con un APF de menor potencia que compensa el resto. Mejor relación coste-eficiencia que un APF puro para grandes instalaciones.

**STATCOM con control de armónicos.** En parques eólicos y fotovoltaicos, el STATCOM puede incluir un lazo de compensación de armónicos mediante resonantes en dq, eliminando los órdenes 5°, 7°, 11° y 13° sin hardware adicional.

## 10 — Impacto en el sistema

**Pérdidas adicionales en transformadores.** Los armónicos elevan las pérdidas en el cobre por efecto skin y en el hierro por corrientes de Foucault. El factor K (norma IEEE C57.110) cuantifica el aumento de pérdidas:
$$ K = \sum_{n=1}^{N} \left(\frac{I_n}{I_1}\right)^2 n^2 $$
Un transformador estándar con \( K=1 \) debe ser sobredimensionado (o reemplazado por un transformador K-rated) si la carga no lineal impone \( K > 1.5 \).

**Interferencias en protecciones.** Los relés de sobrecorriente electromecánicos responden al valor RMS total incluyendo armónicos, pudiendo dispararse ante THD elevada incluso si la fundamental está dentro del límite. Los relés digitales modernos permiten configurar el umbral sobre la fundamental o el RMS total.

**Resonancia paralela.** La instalación de condensadores de corrección de factor de potencia puede crear una resonancia paralela con la inductancia de la red a una frecuencia próxima a un armónico de orden impar. Si el armónico generado coincide con la resonancia, la amplitud puede multiplicarse por el factor Q del circuito.

**Medida práctica.** El analizador de calidad de potencia debe usar una ventana de análisis de al menos 10 ciclos (200 ms a 50 Hz), sincronizada con el PLL, para evitar leakage espectral. La metodología estándar es la IEC 61000-4-7.

<div class="cfig"><img src="../figuras/armonicos-thd-analisis.png" alt="4 paneles: corriente distorsionada, espectro armonicos, THD acumulado, limites IEEE 519"><div class="cap">
(a) Corriente distorsionada con armónicos 3°, 5° y 7° superpuestos a la fundamental de 100 A: la distorsión es visible en la forma de onda. (b) Espectro de amplitudes: la fundamental domina con 100 A; los armónicos de orden impar decrecen con el orden; el THD calculado se muestra en el título. (c) THD acumulado al aumentar el orden máximo considerado: la mayor contribución viene de los primeros armónicos impares. (d) Límites de THD_I según IEEE 519-2022 en función del SCR: redes fuertes (SCR alto) admiten mayor THD porque tienen menor impedancia para absorber la distorsión.
</div></div>

## Cuándo y por qué se usa
El análisis de THD es obligatorio para la conexión de inversores de generación renovable, cargadores de VE, y sistemas industriales de gran potencia. Determina si el equipo cumple con los requisitos del operador de red (TSO/DSO) y las normativas de calidad de potencia.

## Procedimiento de diseño (genérico)
1. Calcular las bandas armónicas generadas por el SPWM a \( f_{sw} \).
2. Dimensionar el LCL para que \( f_{res}<f_{sw}/5 \) y la atenuación a \( f_{sw} \) sea suficiente.
3. Estimar el THD por tiempo muerto e implementar la compensación en el controlador.
4. Verificar contra IEEE 519 / IEC 61000-3-2 en el PCC con el SCR real.
5. Si no cumple, añadir resonantes (RC) para los órdenes problemáticos.

## Ejemplo de código
```python
import numpy as np

def thd(V_harmonics, V1):
    """THD [%] dado array de amplitudes V2, V3, ... y fundamental V1."""
    return 100 * np.sqrt(np.sum(np.array(V_harmonics)**2)) / V1

# Corriente de inversor con LCL: armónicos medidos
I1 = 100.0  # A (fundamental)
I_harm = [3.5, 1.8, 0.9, 0.6]  # A: orden 5, 7, 11, 13
print(f"THD = {thd(I_harm, I1):.2f} %")  # ~4.1 %

# Bode del filtro LCL
L1, L2, Cf = 2e-3, 0.5e-3, 10e-6
Leq = L1*L2/(L1+L2)
fres = 1/(2*np.pi*np.sqrt(Leq*Cf))
f = np.logspace(1, 5, 500)
w = 2*np.pi*f
# G_LCL(jw) = 1/(1 - w^2*Leq*Cf)
G_LCL = np.abs(1 / (1 - w**2 * Leq * Cf))
```

## Parámetros y valores típicos
\( f_{res} \) del LCL: \( 0.2\text{–}0.4\times f_{sw} \). Tiempo muerto típico: 1–4 µs. THD_V en red de distribución: < 5 % (IEEE 519). Ancho de banda del APF: debe alcanzar al menos el armónico 25° (1250 Hz en 50 Hz). Resonante PR: \( \omega_c=2\pi\times5\,\text{rad/s} \).

## Errores comunes
- Calcular \( f_{res} \) del LCL sin incluir la inductancia de la red → \( f_{res} \) sobreestimada, menor atenuación real.
- No sincronizar la ventana de medición con el PLL → leakage espectral → sobreestimación del THD.
- Ignorar los armónicos de bajo orden (tiempo muerto) confiando solo en el LCL → el LCL no los atenúa (están muy por debajo de \( f_{res} \)).
- Usar el límite de SCR equivocado (confundir el SCR del transformador con el del PCC real).

## Conceptos relacionados
- [[filtro-lcl]] · [[controlador-resonante]] · [[armonicos-thd-convertidores]] · [[series-fourier]] · [[convertidor-vsc]]

## Referencias
- IEEE Std 519-2022, *Harmonic Control in Electric Power Systems*.
- IEC 61000-3-2:2018, *Limits for harmonic current emissions*.
- Liserre et al., *Design and control of an LCL-filter based three-phase active rectifier*, IEEE TIA 2005.
