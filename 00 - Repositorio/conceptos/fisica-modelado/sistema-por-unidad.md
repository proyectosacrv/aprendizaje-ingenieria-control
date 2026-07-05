---
titulo: Sistema por unidad (p.u.)
slug: sistema-por-unidad
categoria: fisica-modelado
tipo: concepto
nivel: basico
proyectos: []
objetivos: [normalizar magnitudes eléctricas para comparar y escalar sistemas, diseñar el LCL en pu, eliminar transformadores del circuito]
tags: [por-unidad, pu, normalizacion, base, cambio-de-base, transformador, filtro-lcl, basico, modelado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-03
relacionados: [red-thevenin-scr, potencia-ac-fasores, sistema-trifasico, filtro-lcl, transferencia-potencia-linea]
referencias:
  - "Kundur, Power System Stability and Control, McGraw-Hill 1994"
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
  - "Glover, Sarma, Overbye, Power Systems Analysis and Design, Cengage 2012"
---

## Definición
Sistema de normalización en el que cada magnitud se expresa como fracción de un **valor base**:
\( x_{pu}=x/x_{base} \). Convierte voltios, amperios y ohmios en números adimensionales en torno
a 1.

## Fundamento teórico
Se eligen **dos** bases independientes (típicamente \( S_{base} \) y \( V_{base} \)); el resto se
derivan:
$$ I_{base}=\frac{S_{base}}{\sqrt{3}\,V_{base}},\qquad
   Z_{base}=\frac{V_{base}^2}{S_{base}},\qquad
   \omega_{base}=2\pi f,\ \ L_{base}=\frac{Z_{base}}{\omega_{base}},\ \ C_{base}=\frac{1}{\omega_{base}Z_{base}} $$
Ventajas: los parámetros quedan en rangos conocidos (impedancias de transformador 0.05–0.15 p.u.),
las relaciones de transformación desaparecen y el modelo es **escalable** a cualquier potencia.
Para cambiar de base: \( Z_{pu}^{nuevo}=Z_{pu}^{viejo}\frac{S_{base}^{nuevo}}{S_{base}^{viejo}}
\left(\frac{V_{base}^{viejo}}{V_{base}^{nuevo}}\right)^2 \).

<div class="cfig"><img src="figuras/sistema-por-unidad-impedancias.png" alt="impedancias del sistema en por unidad sumandose"><div class="cap">En por unidad, las impedancias de equipos muy distintos (transformador, filtro, red) quedan todas en el rango ~0.05–0.15 y se suman directamente una vez referidas a la misma base. Aquí $Z_{tot}=0.25$ pu; sin pu, cada componente estaría en ohmios de su base propia y sumarlos sería un error.</div></div>

## 1 — De dónde salen las bases derivadas
**Paso 1 — elegir las dos bases independientes.** El sistema p.u. fija libremente **dos** magnitudes; el resto se obliga a ser coherente con las leyes físicas. Se eligen \( S_{base} \) (potencia trifásica nominal) y \( V_{base} \) (tensión de línea nominal RMS). Todas las demás bases salen de imponer que las **mismas fórmulas** del sistema real valgan también entre las bases.

**Paso 2 — base de corriente.** La potencia aparente trifásica cumple \( S=\sqrt3\,V_{LL}I_L \) (ver [[sistema-trifasico]]). Imponiendo esa relación entre bases, \( S_{base}=\sqrt3\,V_{base}I_{base} \), y despejando:

$$ \boxed{\;I_{base}=\frac{S_{base}}{\sqrt3\,V_{base}}\;} $$

**Paso 3 — base de impedancia.** La ley de Ohm por fase es \( V_{fase}=Z\,I \). Con \( V_{fase,base}=V_{base}/\sqrt3 \) e \( I_{base} \) del paso 2:

$$ Z_{base}=\frac{V_{fase,base}}{I_{base}}=\frac{V_{base}/\sqrt3}{S_{base}/(\sqrt3\,V_{base})}=\frac{V_{base}/\sqrt3\cdot\sqrt3\,V_{base}}{S_{base}}=\frac{V_{base}^2}{S_{base}} $$

Los dos \( \sqrt3 \) se cancelan y queda la forma trifásica limpia:

$$ \boxed{\;Z_{base}=\frac{V_{base}^2}{S_{base}}\;} $$

**Paso 4 — bases de inductancia y capacitancia.** Como \( X_L=\omega L \) y \( X_C=1/(\omega C) \) (ver [[impedancia-reactancia]]), las reactancias base son también \( Z_{base} \), de donde a la frecuencia base \( \omega_{base}=2\pi f \):

$$ \boxed{\;L_{base}=\frac{Z_{base}}{\omega_{base}},\qquad C_{base}=\frac{1}{\omega_{base}Z_{base}}\;} $$

Cada base se deriva imponiendo una ley física (Ohm, potencia, reactancia) entre los valores base, de modo que **toda ecuación del sistema real conserva su forma en p.u.**

## 2 — Las cuatro bases en sistemas trifásicos

### Las dos bases libres y las cuatro derivadas

En un sistema trifásico hay exactamente **seis magnitudes eléctricas fundamentales** (tensión, corriente, potencia, impedancia, inductancia, capacitancia) y dos grados de libertad (las dos bases libres). Las cuatro bases derivadas se obtienen de forma inequívoca.

**Ejemplo numérico detallado: \( S_{base}=1 \) MVA, \( V_{base}=690 \) V (línea RMS), \( f=50 \) Hz.**

$$ I_{base}=\frac{1\times10^6}{\sqrt3\cdot690}=836.7\,\text{A} $$

$$ Z_{base}=\frac{690^2}{1\times10^6}=\frac{476100}{10^6}=0.4761\,\Omega $$

$$ \omega_{base}=2\pi\cdot50=314.16\,\text{rad/s} $$

$$ L_{base}=\frac{0.4761}{314.16}=1.516\,\text{mH} $$

$$ C_{base}=\frac{1}{314.16\cdot0.4761}=6.685\,\text{mF} $$

Estos valores son el sistema de referencia: una inductancia de 1.516 mH es exactamente 1 pu en esta base, una corriente de 836.7 A es 1 pu, etc.

### Por qué la base de corriente usa √3

La confusión más frecuente es usar \( I_{base}=S_{base}/V_{base} \) (sin \( \sqrt3 \)), que daría la corriente de **fase** si la tensión fuera la de fase. Como \( V_{base} \) es la tensión de **línea** (la que se mide entre dos bornes), hay que aplicar la relación trifásica exacta \( S_{3\phi}=\sqrt3\,V_{LL}I_L \).

### Relación entre tensión de fase y de línea en pu

En pu, la tensión de fase nominal es siempre \( V_{fase,pu}=1/\sqrt3 \) cuando \( V_{base} \) es la de línea... o siempre 1 si \( V_{base} \) es la de fase. La convención más extendida en sistemas de potencia usa \( V_{base}=V_{linea} \), de modo que la tensión de fase en pu es \( 1/\sqrt3 \). En control de convertidores se usa a veces \( V_{base}=V_{fase,pico} \) para evitar el \( \sqrt3 \) al calcular corrientes. Es imprescindible especificar la convención al inicio.

### Resumen de las cuatro bases (Sbase=1 MVA, Vbase=690 V)

| Base | Fórmula | Valor numérico |
|---|---|---|
| \( S_{base} \) | (libre) | 1 MVA |
| \( V_{base} \) | (libre) | 690 V (línea RMS) |
| \( I_{base} \) | \( S/(√3V) \) | 836.7 A |
| \( Z_{base} \) | \( V^2/S \) | 0.4761 Ω |
| \( L_{base} \) | \( Z/\omega_0 \) | 1.516 mH |
| \( C_{base} \) | \( 1/(Z\omega_0) \) | 6.685 mF |

## 3 — Conversión de bases: de los datos del fabricante al sistema

### La fórmula de cambio de base

**Paso 1 — el valor físico es invariante.** Una impedancia en ohmios \( Z_\Omega \) es la misma magnitud física, se exprese en la base que se exprese. En cada base, \( Z_{pu}=Z_\Omega/Z_{base} \), luego \( Z_\Omega=Z_{pu}^{viejo}Z_{base}^{viejo}=Z_{pu}^{nuevo}Z_{base}^{nuevo} \).

**Paso 2 — despejar el nuevo p.u.** Aislando \( Z_{pu}^{nuevo} \):

$$ Z_{pu}^{nuevo}=Z_{pu}^{viejo}\,\frac{Z_{base}^{viejo}}{Z_{base}^{nuevo}}=Z_{pu}^{viejo}\,\frac{V_{base,viejo}^2/S_{base}^{viejo}}{V_{base,nuevo}^2/S_{base}^{nuevo}} $$

**Paso 3 — reordenar.** Reagrupando los cocientes de \( S \) y de \( V \):

$$ \boxed{\;Z_{pu}^{nuevo}=Z_{pu}^{viejo}\,\frac{S_{base}^{nuevo}}{S_{base}^{viejo}}\left(\frac{V_{base}^{viejo}}{V_{base}^{nuevo}}\right)^2\;} $$

La \( S \) entra directa (más potencia base → menos ohmios por p.u.) y la \( V \) al cuadrado.

### Aplicación: trafo 33 kV/690 V, Sn=1 MVA, Xcc=6%

El fabricante da \( X_{cc}=0.06 \) pu en la **base propia del trafo**: \( S_{fab}=1 \) MVA, \( V_{fab,alta}=33 \) kV, \( V_{fab,baja}=690 \) V.

**Caso 1: convertir a base del sistema (Ssys=10 MVA, Vsys_alta=33 kV).**

$$ X_{cc,sys}=0.06\cdot\frac{10\,\text{MVA}}{1\,\text{MVA}}\cdot\left(\frac{33\,\text{kV}}{33\,\text{kV}}\right)^2=0.06\cdot10\cdot1=0.60\,\text{pu} $$

**Caso 2: misma conversión pero desde el lado de baja (Vsys_baja=690 V, Ssys=10 MVA).**

$$ X_{cc,sys}=0.06\cdot\frac{10}{1}\cdot\left(\frac{690}{690}\right)^2=0.60\,\text{pu} $$

El resultado es idéntico: **la relación de transformación del trafo se cancela automáticamente** en el sistema pu cuando las bases de tensión en cada nivel son coherentes con la relación de transformación nominal del trafo (\( n=33/0.69=47.8 \)). Esto es una de las ventajas centrales del sistema pu: no importa en qué lado se trabaje.

### Verificación numérica

La impedancia en ohmios del trafo (referida al lado de alta):

$$ Z_\Omega=X_{cc,pu}\cdot Z_{base,trafo}=0.06\cdot\frac{33000^2}{1\times10^6}=0.06\cdot1089=65.3\,\Omega $$

Referida a la base del sistema (Ssys=10 MVA, Vsys=33 kV):

$$ Z_{base,sys}=\frac{33000^2}{10\times10^6}=108.9\,\Omega $$

$$ X_{cc,sys}=\frac{65.3}{108.9}=0.60\,\text{pu}\quad\checkmark $$

## 4 — El diagrama en pu: eliminar los transformadores ideales

### Por qué desaparecen los transformadores ideales

En el circuito en SI (ohmios, amperios, voltios), un transformador ideal con relación \( n:1 \) obliga a referir todas las impedancias a un único lado mediante factores \( n^2 \). En el circuito en pu, si se eligen las bases de tensión de tal forma que \( V_{base,alta}/V_{base,baja}=n \) (la relación nominal del trafo), entonces:

- Una impedancia \( Z_\Omega \) en el lado de alta tiene \( Z_{pu}=Z_\Omega/Z_{base,alta} \).
- La misma impedancia referida al lado de baja (en SI): \( Z_\Omega/n^2 \).
- En pu desde el lado de baja: \( (Z_\Omega/n^2)/Z_{base,baja}=(Z_\Omega/n^2)\cdot S_{base}/V_{base,baja}^2 \).
- Con \( V_{base,baja}=V_{base,alta}/n \): \( (Z_\Omega/n^2)\cdot S_{base}/(V_{base,alta}/n)^2=Z_\Omega\cdot S_{base}/V_{base,alta}^2=Z_{pu} \).

El resultado en pu es el mismo desde cualquier lado: **el transformador ideal no aparece en el circuito en pu**, solo su impedancia de cortocircuito.

### El circuito equivalente en pu del sistema completo

Para un sistema con red → transformador → filtro LCL → convertidor:

$$ \underbrace{Z_{red,pu}}_{\text{red}}+\underbrace{X_{cc,trafo,pu}}_{\text{trafo (solo Xcc)}}+\underbrace{L_{1,pu}+\frac{1}{j\omega C_{f,pu}}\parallel L_{2,pu}}_{\text{filtro LCL}} $$

Todo en la misma base → se suman directamente, sin factores \( n^2 \) intermedios.

### La SCR en pu y la red Thévenin

La **Short Circuit Ratio** (SCR) es la relación entre la potencia de cortocircuito de la red y la potencia nominal del convertidor. En pu:

$$ \text{SCR}=\frac{S_{cc,red}}{S_{base}}=\frac{V_{base}^2/Z_{red,\Omega}}{S_{base}}=\frac{1}{Z_{red,pu}} $$

Es decir, **la impedancia de red en pu es exactamente** \( Z_{red,pu}=1/\text{SCR} \). Para SCR=10: \( Z_{red,pu}=0.1 \) pu; para SCR=2: \( Z_{red,pu}=0.5 \) pu. El circuito pu hace evidente por inspección cuándo la red es débil.

## 5 — El filtro LCL en pu: criterios de diseño normalizados

### De SI a pu para el filtro LCL

Con \( S_{base}=1 \) MVA, \( V_{base}=690 \) V, \( f_0=50 \) Hz → \( L_{base}=1.516 \) mH, \( C_{base}=6.685 \) mF.

Para un filtro LCL típico de un convertidor de 1 MVA/690 V (\( L_1=2 \) mH, \( L_2=0.5 \) mH, \( C_f=20\,\mu\text{F} \)):

$$ L_{1,pu}=\frac{2\,\text{mH}}{1.516\,\text{mH}}=1.319\,\text{pu} $$

$$ L_{2,pu}=\frac{0.5\,\text{mH}}{1.516\,\text{mH}}=0.330\,\text{pu} $$

$$ C_{f,pu}=\frac{20\,\mu\text{F}}{6.685\,\text{mF}}=2.99\times10^{-3}\,\text{pu} $$

El criterio estándar dice que \( L_{total,pu}<0.1 \) pu (caída de tensión en la inductancia total menor del 10% a plena carga). Aquí \( L_{1,pu}=1.32 \) pu: **¡demasiado alto!**

### Resolución: la base correcta es la potencia del convertidor, no la del sistema

El error está en elegir \( S_{base}=1 \) MVA siendo la potencia del convertidor exactamente 1 MVA. Los criterios de diseño del LCL (\( L<0.1 \) pu, \( C<0.05 \) pu) están en la base del convertidor, con la tensión de línea del convertidor. Para el filtro anterior:

- La caída de tensión real en \( L_1 \) a plena carga (\( I_{nom}=836.7 \) A): \( \Delta V=\omega_0 L_1 I_{nom}=314\cdot2\times10^{-3}\cdot836.7=527 \) V. La tensión de fase es \( 690/\sqrt3=398 \) V. Porcentaje: \( 527/398=132\% \). Efectivamente: 1.32 pu coincide con 132% de la tensión de fase.

El problema es físico: un filtro con \( L_1=2 \) mH y \( I_{nom}=836 \) A tiene una caída de tensión a 50 Hz mayor que la tensión nominal — ese filtro no puede funcionar en un convertidor de 1 MVA sin saturar.

**Diseño correcto:** para \( L_1\approx0.1 \) pu con \( S_{base}=1 \) MVA y \( V_{base}=690 \) V → \( L_1=0.1\cdot L_{base}=0.1\cdot1.516=0.152 \) mH. Un filtro LCL de 1 MVA/690 V tiene inductancias del orden de **0.1–0.5 mH**, no 2 mH.

### El LCL del proyecto 01 en pu: L1=0.5 mH, L2=0.2 mH, Cf=20 μF

Con \( S_{base}=1 \) MVA, \( V_{base}=690 \) V:

$$ L_{1,pu}=\frac{0.5}{1.516}=0.330\,\text{pu},\quad L_{2,pu}=\frac{0.2}{1.516}=0.132\,\text{pu},\quad C_{f,pu}=\frac{20\times10^{-6}}{6.685\times10^{-3}}=2.99\times10^{-3}\,\text{pu} $$

\( L_{total,pu}=0.462 \) pu — todavía alto para el criterio de 0.1 pu, pero factible para un convertidor de 1 MVA con filtro sobredimensionado por requisitos de rizado.

### La frecuencia de resonancia en pu

La frecuencia de resonancia del LCL en Hz:

$$ f_{res}=\frac{1}{2\pi}\sqrt{\frac{L_1+L_2}{L_1L_2C_f}} $$

En pu (normalizada a \( f_0=50 \) Hz), para \( L_{1,pu}=0.33 \), \( L_{2,pu}=0.13 \), \( C_{f,pu}=3\times10^{-3} \):

$$ f_{res,pu}=\frac{1}{2\pi}\sqrt{\frac{0.33+0.13}{0.33\cdot0.13\cdot3\times10^{-3}}}=\frac{1}{2\pi}\sqrt{3590}\approx9.5 \quad(\text{en }f_0\text{ pu}) $$

Es decir, la resonancia está a \( 9.5\cdot50=475 \) Hz. En unidades de la frecuencia base, el criterio es \( 10<f_{res,pu}<(f_{sw}/f_0)/2 \) — típicamente entre 10× y 25× la fundamental.

## 6 — Diseño iterativo: el LCL del proyecto 01 completamente en pu

### Especificación y base

Convertidor GFM de 1 MVA, \( V_{nom}=690 \) V, \( f_0=50 \) Hz, \( f_{sw}=10 \) kHz.
Base elegida: \( S_{base}=1 \) MVA, \( V_{base}=690 \) V.
Bases derivadas: \( I_{base}=836.7 \) A, \( Z_{base}=0.476 \) Ω, \( L_{base}=1.516 \) mH, \( C_{base}=6.685 \) mF.

### Paso 1: elegir L1 por criterio de rizado

El rizado de corriente en \( L_1 \) con modulación SPWM de dos niveles:

$$ \Delta i_{L1,pico}=\frac{V_{DC}/2}{L_1\cdot f_{sw}}\cdot D(1-D)\bigg|_{D=0.5}\approx\frac{V_{DC}}{8L_1 f_{sw}} $$

Con \( V_{DC}=1000 \) V y criterio \( \Delta i<10\%\cdot I_{nom,pico} \):

$$ L_1>\frac{V_{DC}}{8\cdot f_{sw}\cdot0.1\cdot I_{nom,pico}}=\frac{1000}{8\cdot10^4\cdot0.1\cdot836.7\cdot\sqrt2}=0.13\,\text{mH} $$

Elegimos \( L_1=0.3 \) mH (margen de 2.3×). En pu: \( L_{1,pu}=0.3/1.516=0.198 \) pu.

### Paso 2: elegir Cf por criterio de potencia reactiva

La corriente en \( C_f \) a 50 Hz absorbe potencia reactiva: \( Q_{Cf}=\omega_0 C_f V_{fase}^2 \). Criterio: \( Q_{Cf}<5\%\cdot S_{base} \):

$$ C_f<\frac{0.05\cdot S_{base}}{\omega_0\cdot V_{fase}^2}=\frac{0.05\times10^6}{314\cdot(690/\sqrt3)^2}=\frac{50000}{314\cdot158760}=1.002\,\mu\text{F} $$

Pero con \( C_{base}=6.685 \) mF, el límite en pu es \( C_f<0.05\cdot C_{base}=0.334 \) mF... es decir el criterio del 5% de reactiva corresponde a \( C_f<1 \) μF. Para una mejor atenuación elegimos \( C_f=20\,\mu\text{F} \) con consciencia de que absorbe \( Q=\omega_0\cdot20\times10^{-6}\cdot(398)^2=1.0 \) kVAR = 0.1% de \( S_{base} \): está bien dentro del criterio (la fórmula es \( Q_{Cf}=\omega_0 C_f V^2/3 \) por fase).

En pu: \( C_{f,pu}=20\times10^{-6}/6.685\times10^{-3}=2.99\times10^{-3} \) pu (muy pequeño).

### Paso 3: elegir L2 por atenuación en fsw

La atenuación del LCL a \( f_{sw}=10 \) kHz debe ser \( >30 \) dB adicionales respecto a un filtro L simple. La atenuación del LCL por encima de \( f_{res} \):

$$ G_{LCL}(f_{sw})\approx\frac{1}{L_1 C_f L_2(2\pi f_{sw})^4}\quad\text{(para }f\gg f_{res}\text{)} $$

Criterio: \( i_{grid}(f_{sw})<0.3\%\cdot I_{nom,pico} \), es decir atenuación \( >55 \) dB. Con \( L_1=0.3 \) mH, \( C_f=20\,\mu\text{F} \):

$$ L_2>\frac{1}{L_1 C_f(2\pi f_{sw})^4\cdot(I_{grid,max}/V_{sw})}=0.05\,\text{mH} $$

Elegimos \( L_2=0.15 \) mH. En pu: \( L_{2,pu}=0.15/1.516=0.099 \) pu.

### Verificación final en pu

| Parámetro | Valor SI | Valor pu | Criterio pu | ¿OK? |
|---|---|---|---|---|
| \( L_1 \) | 0.3 mH | 0.198 pu | \( <0.15 \) pu | Límite |
| \( L_2 \) | 0.15 mH | 0.099 pu | \( <0.10 \) pu | OK |
| \( C_f \) | 20 μF | 0.00299 pu | \( <0.05 \) pu | OK |
| \( L_{total} \) | 0.45 mH | 0.297 pu | \( <0.10 \) pu | Alto |
| \( f_{res} \) | 2.4 kHz | 48 × \( f_0 \) | 10–100 × \( f_0 \) | OK |

El \( L_{total} \) alto indica que el convertidor necesitará feedforward de tensión de red para compensar la caída en \( L_{total} \) a plena carga. Alternativamente, usar \( S_{base}=10 \) MVA para el diseño de sistemas de mayor potencia reduce todos los valores pu en un factor 10.

### Relación con la norma IEEE 519 y la base del sistema de transmisión

En transmisión se usa habitualmente \( S_{base}=100 \) MVA. Para comparar el LCL de un convertidor de 1 MVA en esa base:

$$ L_{1,pu,100MVA}=0.198\cdot\frac{1\,\text{MVA}}{100\,\text{MVA}}=0.00198\,\text{pu} $$

El filtro LCL es prácticamente invisible desde la base del sistema de transmisión, lo que explica por qué las normas de red (IEEE 519, IEC 61000) trabajan en la base del sistema: los convertidores individuales, aunque tengan filtros grandes en su propia base, tienen impedancias despreciables en la base del sistema.

<div class="cfig"><img src="figuras/sistema-por-unidad-analisis.png" alt="diagrama pu, conversión de bases, Z_red_pu vs frecuencia, LCL en dos bases"><div class="cap">(a) Diagrama en pu del sistema completo: red (Z_red=1/SCR), trafo (Xcc=0.06 pu), LCL — todo sumable directamente. (b) La impedancia del trafo en tres bases distintas: el valor en ohmios es invariante, el pu varía con la base elegida. (c) Impedancia de red en pu vs frecuencia para SCR=2, 5, 10: a 50 Hz, Z_red=1/SCR pu. (d) Función de transferencia del LCL en pu con dos bases (500 kVA y 1 MVA): la forma es idéntica, los valores de L y C cambian proporcionalmente.</div></div>

## Cuándo y por qué se usa
En modelado de convertidores y redes: facilita comparar equipos de distinta potencia, fija
condiciones de diseño (corriente nominal = 1 p.u.) y mejora el **condicionamiento numérico** de
los modelos de estado. En diseño de LCL: los criterios de \( L<0.1 \) pu y \( C<0.05 \) pu son
directamente verificables en pu sin depender de la potencia absoluta.

## Procedimiento (genérico)
1. Elige \( S_{base} \) (potencia nominal del convertidor o del sistema) y \( V_{base} \) (tensión nominal de línea).
2. Deriva \( I_{base},Z_{base},L_{base},C_{base} \) con las fórmulas de las cuatro bases.
3. Divide cada parámetro físico por su base correspondiente.
4. Verifica los criterios de diseño en pu (\( L_{total}<0.1 \), \( C_f<0.05 \), \( f_{res}\in[10,100]\cdot f_0 \)).
5. Reporta resultados en p.u.; reconvierte a SI solo al final si hace falta.

## Ejemplo de código
```python
import numpy as np

# Bases
Sb, Vb, f = 1e6, 690.0, 50.0
omega0 = 2*np.pi*f
Ib = Sb/(3**0.5*Vb)           # 836.7 A
Zb = Vb**2/Sb                  # 0.4761 Ohm
Lb = Zb/omega0                 # 1.516 mH
Cb = 1/(omega0*Zb)             # 6.685 mF

# Filtro LCL en pu
L1, L2, Cf = 0.3e-3, 0.15e-3, 20e-6
L1_pu = L1/Lb; L2_pu = L2/Lb; Cf_pu = Cf/Cb

# Frecuencia de resonancia en pu
fres = (1/(2*np.pi))*np.sqrt((L1+L2)/(L1*L2*Cf))
fres_pu = fres/f                # en multiplos de f0

# Cambio de base del trafo (Xcc=6% en base 1 MVA, a base 10 MVA)
Xcc_fab = 0.06; Sfab = 1e6; Ssys = 10e6
Xcc_sys = Xcc_fab * (Ssys/Sfab)   # 0.60 pu (Vbase igual a ambos lados)

# SCR en pu
SCR = 5
Zred_pu = 1/SCR                    # 0.20 pu
```

## Parámetros y valores típicos
| Magnitud | Valor pu típico | Comentario |
|---|---|---|
| \( X_{cc} \) de transformador | 0.05–0.15 | En base propia del trafo |
| \( L_1 \) de filtro LCL | 0.05–0.15 | En base del convertidor |
| \( L_2 \) de filtro LCL | 0.02–0.08 | En base del convertidor |
| \( C_f \) de filtro LCL | 0.02–0.05 | En base del convertidor |
| \( Z_{red} \) para SCR=10 | 0.10 | Red fuerte |
| \( Z_{red} \) para SCR=2 | 0.50 | Red débil |
| \( f_{res} \) del LCL | 10–100 × \( f_0 \) | Criterio de diseño |

## Errores comunes
- Mezclar bases monofásicas y trifásicas (factor \( \sqrt3 \) / 3 en corriente).
- No reescalar al combinar equipos con bases distintas (trafo + convertidor + red en bases diferentes).
- Confundir base de pico y base RMS en las tensiones.
- Aplicar los criterios del LCL (\( L<0.1 \) pu) en la base del sistema de transmisión en lugar de la base del convertidor.
- Olvidar que \( Z_{red,pu}=1/\text{SCR} \) solo cuando \( S_{base}=S_{n,convertidor} \).

## Ejemplo de aplicación real
**Problema:** Convertidor de 500 kVA/690 V conectado a transformador de 1 MVA/690 V con \( Z_{cc}=10\,\%\) en base propia. Expresar la impedancia del transformador en la base del convertidor.

Bases del convertidor: \( S_{b,c}=500\,\text{kVA} \), \( V_{b,c}=690\,\text{V} \). Cambio de base: \( Z_{pu}^{(c)}=Z_{pu}^{(t)}\times(S_{b,c}/S_{b,t})\times(V_{b,t}/V_{b,c})^2=0.10\times(500/1000)\times1=0.05\,\text{p.u.} \). En la base del convertidor, el transformador equivale a solo el 5 % de impedancia. Si el reactor de filtro es 0.12 p.u. y la red equivalente 0.08 p.u. en la misma base, la impedancia total vista desde el convertidor es \( Z_{total}=0.12+0.05+0.08=0.25\,\text{p.u.} \) y la SCR es \( 1/0.08=12.5 \) (solo la red).

## Conceptos relacionados
- [[red-thevenin-scr]] · [[potencia-ac-fasores]] · [[sistema-trifasico]] · [[filtro-lcl]] · [[transferencia-potencia-linea]]

## Referencias
- Kundur, *Power System Stability and Control*, 1994.
- Yazdani, Iravani, *Voltage-Sourced Converters in Power Systems*, Wiley 2010.
- Glover, Sarma, Overbye, *Power Systems Analysis and Design*, Cengage 2012.
