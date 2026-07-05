---
titulo: Topologías de inversores multinivel (NPC, MMC, CHB)
slug: topologias-multinivel
categoria: fisica-modelado
tipo: concepto
nivel: avanzado
proyectos: []
objetivos: [elegir la topologia de convertidor segun tension, potencia y calidad]
tags: [multinivel, NPC, T-type, flying-capacitor, MMC, CHB, HVDC, STATCOM]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-03
relacionados: [convertidor-vsc, marco-dq, control-vectorial, semiconductores-potencia]
referencias:
  - "Rodriguez, Lai, Peng, Multilevel Inverters: Survey of Topologies, IEEE TIE 2002"
  - "Akagi, Classification and Terminology of MMC, IEEE TPEL 2011"
  - "Lesnicar & Marquardt, An Innovative Modular Multilevel Converter Topology, IEEE ISIE 2003"
---

## Definición
Convertidores que sintetizan la tensión de salida en **más de dos niveles**. Frente al puente de
2 niveles, reparten la tensión entre más dispositivos y producen una onda más escalonada: menor
contenido armónico, menor \( dv/dt \) y mayor tensión/potencia manejable.

## Fundamento teórico
Con \( n \) niveles, la tensión de salida toma \( n \) valores discretos; el rizado y la \( THD \)
caen y la tensión de bloqueo por dispositivo es \( \approx V_{dc}/(n-1) \). Familias principales:
- **NPC** (Neutral-Point-Clamped, diode-clamped): 3 niveles con diodos de anclaje al neutro del
  bus DC. Reto: **balanceo del punto neutro**.
- **T-type**: variante de 3 niveles con conmutador bidireccional al neutro; buen compromiso en
  baja-media tensión.
- **Flying Capacitor (FC)**: niveles mediante condensadores flotantes; reto: **balanceo de los
  condensadores**, redundancia de estados de conmutación.
- **Cascaded H-Bridge (CHB)**: puentes H en serie con fuentes DC aisladas; modular, ideal con
  fuentes separadas (PV, baterías).
- **MMC** (Modular Multilevel Converter): brazos de submódulos en serie; estándar en **HVDC** y
  alta potencia. Retos: control de **energía de submódulos** y **corriente circulante**.

Modulación: PD/POD-PWM multinivel, **SVM** multinivel, o selección de estados (MMC). La
**redundancia** de estados de conmutación se aprovecha para balancear condensadores.

<div class="cfig"><img src="figuras/topologias-multinivel-ondas.png" alt="ondas de tension de 2, 3 y 7 niveles frente a la referencia"><div class="cap">Síntesis de la tensión de salida: con más niveles la onda escalonada se acerca a la senoidal de referencia, reduciendo el contenido armónico y el $dv/dt$. Además la tensión de bloqueo por dispositivo baja a $V_{dc}/(n-1)$, lo que permite alcanzar tensiones/potencias mayores (NPC/T-type en BT-MT, MMC en HVDC).</div></div>

## 1 — Por qué \( n \) niveles reduce el \( dv/dt \) y los armónicos
**Paso 1 — tensión de bloqueo por dispositivo.** El bus DC total \( V_{dc} \) se reparte en serie entre los \( n-1 \) escalones que separan los \( n \) niveles de salida. Cada dispositivo bloquea solo un escalón:

$$ \boxed{\;V_{bloqueo}=\frac{V_{dc}}{n-1}\;} $$

Para \( n=2 \) cada interruptor aguanta \( V_{dc} \); para \( n=3 \), solo \( V_{dc}/2 \). Eso permite usar dispositivos de menor tensión (más rápidos y baratos, ver [[semiconductores-potencia]]) o alcanzar mayor \( V_{dc} \) con la misma tecnología.

**Paso 2 — el salto de tensión en cada conmutación.** La salida pasa de un nivel al adyacente, no de un extremo al otro. El salto es la separación entre niveles consecutivos:

$$ \Delta v = \frac{V_{dc}}{n-1} $$

El \( dv/dt \) lo fija ese salto dividido por el tiempo de conmutación \( t_{sw} \):

$$ \frac{dv}{dt}\approx\frac{\Delta v}{t_{sw}}=\frac{V_{dc}}{(n-1)\,t_{sw}} $$

**Paso 3 — comparar 3 niveles con 2 niveles.** Manteniendo \( V_{dc} \) y \( t_{sw} \), el cociente es:

$$ \frac{(dv/dt)_{3\text{niv}}}{(dv/dt)_{2\text{niv}}}=\frac{V_{dc}/2}{V_{dc}/1}=\frac12 $$

El \( dv/dt \) cae a la **mitad** al pasar de 2 a 3 niveles: menor estrés en el aislamiento del motor, menos EMI. En general escala como \( 1/(n-1) \).

**Paso 4 — los armónicos.** La onda escalonada de \( n \) niveles se aproxima mejor a la senoidal: cada paso de \( V_{dc}/(n-1) \) es más pequeño, por lo que la amplitud del rizado de conmutación —y con él la \( THD \) de tensión— escala también como \( \sim 1/(n-1) \). Con la misma \( f_{sw} \), una onda de 7 niveles tiene una \( THD \) muy inferior a la de 2 niveles antes de filtrar. Por eso el multinivel permite filtros de salida más pequeños o frecuencias de conmutación más bajas (menos pérdidas) para la misma calidad.

## 2 — El NPC (neutral-point clamped) de 3 niveles
El NPC de 3 niveles fue propuesto por Nabae, Takahashi y Akagi en 1981 y es la topología multinivel más usada en aplicaciones industriales (accionamientos, generación renovable).

**La topología.** Una fase del NPC usa 4 IGBTs en serie (\( T_1,T_2,T_3,T_4 \)) más 2 diodos de anclaje (\( D_1, D_2 \)) conectados al punto neutro del bus DC \( O \):
- Bus positivo \( P \) (tensión \( +V_{dc}/2 \) respecto a \( O \)).
- Bus negativo \( N \) (tensión \( -V_{dc}/2 \) respecto a \( O \)).
- Punto de anclaje \( O \) (tensión 0).

**Cómo genera los tres niveles.**
- \( +V_{dc}/2 \): enciende \( T_1 \) y \( T_2 \); la salida se conecta a \( P \).
- \( 0 \): enciende \( T_2 \) y \( T_3 \); la salida se conecta a \( O \) a través de los diodos de anclaje.
- \( -V_{dc}/2 \): enciende \( T_3 \) y \( T_4 \); la salida se conecta a \( N \).

Cada dispositivo bloquea \( V_{dc}/2 \), por lo que se pueden usar IGBTs de 1700 V para un bus de 2.8 kV en vez de IGBTs de 3.3 kV.

**La calidad del voltaje.** Con 3 niveles y la misma \( f_{sw} \), el salto de tensión en cada conmutación es \( V_{dc}/2 \) en vez de \( V_{dc} \) como en el convertidor de 2 niveles. El contenido armónico de la tensión de salida —y por tanto la corriente de rizado— cae un factor ~4 (proporcional al cuadrado del salto de tensión en la inductancia del filtro):

$$ \frac{\Delta i_{NPC}}{\Delta i_{2L}}=\frac{(V_{dc}/2)^2}{V_{dc}^2}\cdot\frac{T_{sw}/8}{T_{sw}/4}=\frac{1}{4} $$

Esto permite reducir la inductancia del filtro a ~1/4 con el mismo rizado de corriente, o mantener la inductancia y reducir el rizado 4 veces. En la práctica: NPC a 5 kHz + filtro LCL comparable a 2 niveles a 20 kHz.

**El reto del balanceo del punto neutro.** Los condensadores superior e inferior del bus DC deben mantenerse a \( V_{dc}/2 \) cada uno. La corriente que fluye hacia/desde \( O \) es impulsiva y puede desbalancear los condensadores. Se necesita modulación con gestión de neutro (p.ej. SVPWM con inyección de 3ª armónica) o un lazo de control adicional de balanceo. En el T-type (variante moderna), el conmutador bidireccional al neutro simplifica el balanceo y reduce las pérdidas en el nivel cero.

## 3 — El convertidor modular multinivel (MMC)
El MMC, desarrollado por Lesnicar y Marquardt en 2003, es la topología estándar para HVDC y FACTS de alta potencia. Su característica esencial es que el número de niveles de salida puede ser arbitrariamente grande apilando submódulos en serie.

**La estructura.** Una fase del MMC tiene dos brazos: el **brazo superior** (entre el bus positivo y la salida de fase) y el **brazo inferior** (entre la salida de fase y el bus negativo). Cada brazo contiene \( N \) submódulos (SM) en serie más una inductancia de brazo \( L_{arm} \). La tensión de salida de fase se sintetiza por la diferencia entre las tensiones de los brazos:

$$ v_{out}=\frac{v_{u}-v_{l}}{2} $$

donde \( v_u \) y \( v_l \) son las tensiones totales del brazo superior e inferior.

**El submódulo.** El SM más común es el **half-bridge**: dos interruptores (\( S_1, S_2 \)) con un condensador flotante \( C_{SM} \). En estado activo (\( S_1 \) ON, \( S_2 \) OFF) la tensión del condensador se inserta en el brazo; en estado bypass (\( S_2 \) ON, \( S_1 \) OFF) se cortocircuita. Con \( N \) SMs por brazo, la tensión del brazo puede variar en pasos de \( V_{SM}=V_{dc}/N \) entre 0 y \( V_{dc} \).

**Ventajas para HVDC.** Con \( N=200\text{–}400 \) SMs por brazo y \( V_{SM}=2\,\text{kV} \), se logran \( V_{dc}=\pm400\,\text{kV} \) con dispositivos de 3.3–6.5 kV. La onda de salida tiene 400+ niveles: la \( THD \) de la tensión es <0.5 % sin filtro de salida. Los \( dv/dt \) son mínimos.

**Los retos de control del MMC.**
1. **Balanceo de la energía de submódulos:** los condensadores de los \( 2N \) SMs deben mantenerse todos a \( V_{SM}=V_{dc}/N \). Se usa selección de SM basada en capacitor voltage sorting: en cada periodo de modulación se elige qué SMs insertar según su tensión y el sentido de la corriente de brazo.
2. **La corriente circulante \( i_{circ} \):** fluye por los brazos superior e inferior de la misma fase sin salir al exterior. Contiene una componente a 2ω que intercambia energía entre los brazos. Se controla con un controlador de corriente circulante (CCSC) que inyecta una tensión diferencial entre brazos.

La ecuación de la corriente de brazo:

$$ L_{arm}\frac{di_{arm,u}}{dt}=\frac{V_{dc}}{2}-v_{arm,u}-\frac{v_{out}}{2}-R_{arm}\,i_{arm,u} $$

y la corriente de salida \( i_{out}=i_{arm,u}-i_{arm,l} \); la corriente circulante \( i_{circ}=(i_{arm,u}+i_{arm,l})/2 \).

## 4 — El H-bridge en cascada (CHB): submódulos con fuentes aisladas
El convertidor CHB apila puentes H completos en serie, cada uno con su fuente DC independiente. Esta independencia eléctrica entre módulos es su mayor diferencia respecto al NPC y el MMC.

**La topología.** Cada módulo es un puente H (4 IGBTs, 1 condensador DC). En una fase, \( m \) módulos en serie generan \( 2m+1 \) niveles de tensión (cada módulo puede producir \( +V_{DC} \), \( 0 \) o \( -V_{DC} \)). Con \( m=6 \): 13 niveles, \( THD<2\% \) sin filtro.

**Las fuentes DC aisladas.** En el CHB, los módulos necesitan fuentes aisladas (transformadores independientes, rectificadores separados, o fuentes fotovoltaicas/baterías). Esto es un coste extra pero también una ventaja:
- En aplicaciones con baterías (BESS modular): cada módulo tiene su batería propia → balance natural.
- En STATCOM con transformador: un transformador multi-devanado con 6–18 secundarios proporciona las fuentes aisladas.

**Gestión del SOC en CHB con baterías.** Si cada módulo tiene una batería de estado de carga (SOC) diferente, las tensiones DC de los módulos difieren. El control debe:
1. Balancear el SOC entre módulos de la misma fase (regulando la potencia activa de cada módulo a través de la modulación de fase).
2. Balancear el SOC entre fases (intercambiando potencia entre fases a través del punto neutro del sistema).

La estrategia más común es **indirect current control con SOC balancing**: el controlador de tensión general determina la referencia de corriente; un segundo lazo ajusta los índices de modulación individuales para equilibrar los SOC.

## 5 — Comparativa: 2 niveles vs 3 niveles vs MMC
La elección de la topología impacta todos los aspectos del sistema: tamaño de filtros, pérdidas, complejidad del control y coste de semiconductores.

| Parámetro | 2 niveles | NPC 3 niveles | MMC (N=200) |
|---|---|---|---|
| Niveles de tensión | 2 | 3 | 201+ |
| Tensión de bloqueo/disp. | \( V_{dc} \) | \( V_{dc}/2 \) | \( V_{dc}/N \) |
| THD tensión (\( f_{sw}=5\,\text{kHz} \)) | ~40–60 % | ~10–15 % | <0.5 % |
| Pérdidas totales | ~1–2 % | ~0.8–1.5 % | ~0.8–1.2 % |
| Filtro de salida | obligatorio (grande) | moderado | no necesario |
| Complejidad de control | baja | media (balanceo neutro) | alta (SM sorting, CCSC) |
| Coste relativo | 1× | 1.5× | 3–5× |
| Rango de aplicación | <3.3 kV, <10 MVA | <33 kV, <50 MVA | hasta ±800 kV, GW |

**Tendencia de pérdidas.** Los 3 sistemas tienen eficiencias similares en el punto nominal porque la reducción de pérdidas de conmutación al tener más niveles se compensa parcialmente por más dispositivos. La ventaja real del MMC en pérdidas viene de la menor frecuencia de conmutación por dispositivo (puede funcionar a 150 Hz por SM) y del uso de dispositivos optimizados para su baja tensión de bloqueo.

<div class="cfig"><img src="figuras/topologias-multinivel-analisis.png" alt="comparativa 2L NPC: formas de onda, THD, pérdidas y balanceo de neutro"><div class="cap">Panel (a): tensión de salida del NPC 3 niveles vs 2 niveles con la referencia senoidal — el nivel intermedio en 0 reduce el salto de conmutación a la mitad. Panel (b): THD de tensión vs número de niveles a igual $f_{sw}$=5 kHz — cae como $1/(n{-}1)^{1.8}$. Panel (c): comparativa de pérdidas de conmutación y conducción entre 2L y NPC para 1 MVA a 5 kHz. Panel (d): desequilibrio del punto neutro sin y con control de inyección de 3ª armónica.</div></div>

## 6 — Diseño iterativo: elegir la topología para un STATCOM de 10 MVAr, 33 kV
**Datos del problema.** STATCOM trifásico, \( Q_n=10\,\text{MVAr} \), \( V_{LL}=33\,\text{kV} \), conexión a través de transformador 33/1 kV (o directo con multinivel). Se pide evaluar las opciones.

**Paso 1 — tensión de bus DC necesaria.**
Para un convertidor de 2 niveles conectado a 33 kV directamente (sin transformador), cada interruptor debería bloquear \( V_{dc}\approx\sqrt2\times33\,\text{kV}=46.7\,\text{kV} \): no existe dispositivo comercial. Se necesita transformador o multinivel.

**Opción A: 2 niveles + transformador 33/1 kV.** Bus DC ≈ 1.6 kV. Semiconductores IGBT 1700 V. Transformador de gran potencia: coste y peso elevados. \( f_{sw}=5\,\text{kHz} \) → filtro LC necesario. Solución estándar a costes moderados.

**Opción B: NPC 3 niveles + transformador 33/2.8 kV.** Bus DC ≈ 5.6 kV → IGBT 3.3 kV. THD 4× menor que 2 niveles → filtro más pequeño. Un transformador menos voluminoso (menor relación de transformación). Más complejo (balanceo de neutro) pero maduro industrialmente. Ideal para 10 MVAr.

**Opción C: CHB con transformador multi-devanado.** Transformador 33 kV → 18 secundarios de 1 kV (6 módulos × 3 fases). 13 niveles → THD <2 % sin filtro. Sin baterías, el coste del transformador es el factor dominante. Viable y muy limpio armónicamente; elegido frecuentemente en STATCOM de media-alta tensión.

**Opción D: MMC (sin transformador).** Con \( N=50 \) SMs por brazo y \( V_{SM}=\sqrt2\times33\,\text{kV}\times\sqrt{2/3}/50=540\,\text{V} \) → IGBT 1200 V. 51 niveles por fase → THD <1 % sin filtro. Sin transformador → menor coste y pérdidas. Mayor complejidad de control (SM sorting, CCSC). Solución moderna óptima para ≥10 MVAr.

**Conclusión.** Para 10 MVAr / 33 kV:
- Mínimo coste y complejidad: Opción A (2L + trafo).
- Mejor calidad con complejidad moderada: Opción B (NPC + trafo).
- Sin filtro, sin transformador: Opción D (MMC), con mayor coste de desarrollo.
- Con baterías integradas: Opción C (CHB).

## Cuándo y por qué se usa
Cuando la tensión supera la capacidad de un dispositivo de 2 niveles, o se exige baja \( THD \) /
bajo \( dv/dt \) (motores, red). Selección por tensión/potencia:

| Topología | Rango típico |
|---|---|
| NPC / T-type (3 niveles) | baja-media tensión, industrial |
| Flying capacitor | media tensión, alta frecuencia efectiva |
| CHB | con fuentes DC aisladas (PV, baterías) |
| MMC | alta tensión / HVDC / gran potencia |

## Procedimiento de elección (genérico)
1. Fija tensión y potencia → descarta familias por tensión de bloqueo.
2. Requisitos de \( THD \), \( dv/dt \), eficiencia → nº de niveles.
3. Disponibilidad de fuentes DC aisladas → CHB vs NPC/FC/MMC.
4. Evalúa el coste de control (balanceo de condensadores, corriente circulante en MMC).

## Ejemplo de código
```python
import numpy as np

# Comparativa THD vs niveles (estimacion simplificada)
n_levels = np.array([2, 3, 5, 7, 11, 17])
thd_v = 100 / (n_levels - 1)**2  # % aproximado, misma fsw

# tension de bloqueo por dispositivo
Vdc = 3000.0  # bus DC [V]
V_block = Vdc / (n_levels - 1)

# Numero de transistores por fase (NPC)
n_transistors = 2 * (n_levels - 1)

for n, thd, vb, nt in zip(n_levels, thd_v, V_block, n_transistors):
    print(f"n={n:3d}  THD≈{thd:5.1f}%  V_block={vb:.0f}V  IGBTs/fase={nt}")
```

## Parámetros y valores típicos
3 niveles (NPC/T-type) en convertidores industriales; decenas-cientos de submódulos en MMC para
HVDC. Tensión de bloqueo repartida \( V_{dc}/(n-1) \). \( L_{arm}/L_{base} \approx 0.1\,\text{pu} \) en MMC.

## Errores comunes
- Ignorar el balanceo de condensadores (NPC neutro, FC, MMC): puede divergir.
- Subestimar el coste de control y medida al subir niveles.
- Aplicar el modelo de 2 niveles (ganancia del modulador \( V_{dc}/V_{tri} \)) al NPC sin ajustar por 2.
- Olvidar la corriente circulante en el MMC: puede disparar la protección de sobrecorriente.

## 7 — NPC de 3 niveles: estados de conmutación y balance del punto neutro

En la topología NPC de 3 niveles cada fase tiene 4 interruptores \((S_1, S_2, S_3, S_4)\) y 2 diodos de pinzado al neutro. Los estados válidos:

| Estado | \(S_1\) | \(S_2\) | \(S_3\) | \(S_4\) | \(v_{an}\) |
|---|---|---|---|---|---|
| P | ON | ON | OFF | OFF | \(+V_{dc}/2\) |
| 0 | OFF | ON | ON | OFF | \(0\) |
| N | OFF | OFF | ON | ON | \(-V_{dc}/2\) |

El condensador superior \(C_1\) se carga cuando \(S_1,S_2\) conducen corriente positiva y se descarga cuando \(S_3,S_4\) conducen. El desequilibrio entre \(V_{C1}\) y \(V_{C2}\) genera una tensión de modo común que distorsiona la salida. Se corrige añadiendo un offset de neutro proporcional a la diferencia \(V_{C1}-V_{C2}\).

**THD de línea a línea:** el NPC triplica los pulsos efectivos del modulador → THD tensión \(\approx50\%\) menor que el de 2 niveles al mismo \(V_{dc}\) y \(f_s\).

<div class="cfig"><img src="../figuras/topologias-multinivel-analisis.png" alt="Análisis de topologías multinivel: formas de onda, THD, espectro CHB y curva STATCOM"><div class="cap">(a) Formas de onda de tensión de fase: 2, 3 y 5 niveles. (b) THD de tensión vs número de niveles N. (c) Espectro de la tensión CHB de 5 niveles con PS-PWM. (d) Curva característica I-V de un STATCOM multinivel.</div></div>

## 8 — CHB (Cascaded H-Bridge): modulación PS-PWM y fuentes aisladas

Con \(N\) celdas H-bridge en serie, la tensión de fase toma \(2N+1\) valores. La modulación Phase-Shifted PWM (PS-PWM) desplaza las portadoras de cada celda en \(360°/N\):

$$\varphi_k = (k-1)\cdot\frac{360°}{N}, \quad k=1,\ldots,N$$

Esto produce una cancelación de armónicos que sitúa la primera distorsión significativa en la banda alrededor de \(2N\,f_s\), reduciendo el filtro necesario.

**Fuentes DC aisladas:** cada celda requiere su propia fuente. Las opciones son:
- Transformador multi-devanado (CHBT): un único transformador de media frecuencia con \(N\) secundarios aislados.
- Baterías individuales (BESS modular): cada celda conecta directamente a un pack de baterías; permite balanceo de SOC celda a celda.

**Aplicaciones típicas:** accionamientos de media tensión (3,3–11 kV), STATCOM de alta potencia, cargadores de BESS.

## 9 — THD y filtrado: ventaja de aumentar el número de niveles

La amplitud del armónico dominante de la tensión de salida cae aproximadamente como:

$$\text{THD}_V \propto \frac{1}{N^2-1}$$

Para 2 niveles \(\text{THD}_V\approx100\%\) (referido al fundamental), para 3 niveles \(\approx30\%\), para 5 niveles \(\approx12\%\), para 7 niveles \(\approx7\%\).

Esto reduce la inductancia del filtro necesaria para alcanzar el mismo THD de corriente:

$$L_{f,N} \approx L_{f,2\text{-niv}}\cdot\left(\frac{2}{N^2-1}\right)^{1/2}$$

**Compromiso:** más niveles → menor filtro pero más componentes, mayor complejidad de control y mayor coste de gate drivers.

## 10 — Aplicaciones de alta potencia: STATCOM, accionamientos y BESS

**STATCOM multinivel:** un MMC o CHB de 5–7 niveles inyecta corriente reactiva con THD < 3% sin filtro externo. Para \(S_{STATCOM}=100\,\text{MVAr}\) a 33 kV, el NPC de 3 niveles es la referencia industrial (ABB SVC Plus, Siemens SVC PLUS).

**Accionamientos de media tensión:** el CHB de 7 niveles (6 celdas) con IGBT 1700 V alimenta motores de 3,3–11 kV con rendimiento > 98,5 % y THD de corriente motor < 1%.

**BESS modular:** topología CHB con baterías por celda. El control de balance de SOC redistribuye la potencia entre celdas igualando voltajes de batería. Permite conectar celdas de diferente envejecimiento sin paralelo directo.

**MMC en HVDC:** el MMC de N = 200–400 submódulos por brazo opera a \(f_s = 100\,\text{Hz}\) efectivos por submódulo; \(f_s\) equivalente vista por el filtro es \(N \cdot f_s = 20\,\text{kHz}\), con pérdidas totales < 1% por terminal.

## Uso en proyectos
- Candidato a proyecto propio (MMC). Ficha de panorama por ahora; los proyectos 01/02 usan 2
  niveles (modelo promediado).

## 11 — Modulación PS-PWM en CHB: cancelación de armónicos y frecuencia efectiva

Con \(N\) celdas H-bridge y portadoras desfasadas \(\varphi_k=(k-1)\cdot360°/N\), los armónicos de conmutación del \(k\)-ésimo módulo están en torno a \(2f_{sw}\), desfasados entre sí. La suma vectorial de los \(N\) módulos produce cancelación de todos los armónicos de orden inferior a \(2N\cdot f_{sw}\). El primer grupo armónico no cancelado está en la frecuencia efectiva:

$$f_{ef}=2N\,f_{sw}$$

Para 5 celdas con \(f_{sw}=1\,\text{kHz}\): \(f_{ef}=10\,\text{kHz}\), igual que si cada módulo conmutara a 10 kHz. Resultado: las pérdidas de conmutación son las de 1 kHz por módulo mientras la calidad de la tensión es la de 10 kHz. Esta es la ventaja fundamental del CHB con PS-PWM: **las pérdidas escalan como \(f_{sw}/N\) mientras la calidad escala como \(N\cdot f_{sw}\)**.

**Condición de cancelación.** La cancelación es perfecta si las fuentes DC de todos los módulos son iguales \(V_{DC,k}=V_{DC}\). Si difieren (p.ej. por distinto SOC de baterías), aparecen armónicos residuales en \(f_{ef}/N,\,2f_{ef}/N,\ldots\) La estrategia de balanceo de SOC debe mantener las tensiones de los módulos dentro del ±5 % para que el THD residual sea inferior al 1 %.

## 12 — Balance de condensadores en NPC: inyección de 3ª armónica

El desequilibrio del punto neutro en el NPC se produce porque los estados de nivel "0" pueden extraer corriente del condensador superior o del inferior según la polaridad de la corriente de carga. El efecto es un voltaje diferencial \(\Delta V=V_{C1}-V_{C2}\) que varía a la frecuencia de la fundamental y sus armónicos.

**Estrategia de corrección.** El modulador SVPWM multinivel dispone de estados redundantes para el nivel "0": el estado \(P\!-\!0\!-\!N\) puede aplicarse con la celda superior o con la inferior. Eligiendo cuál usar en función del signo de \(\Delta V\) y de la polaridad de la corriente, se inyecta una corriente neta de corrección sin modificar la tensión de salida. La dinámica del balanceo:

$$C\frac{d(\Delta V)}{dt}=i_{neutro}(\text{control})$$

donde \(i_{neutro}\) se puede controlar mediante el ratio de los tiempos de los estados redundantes. La inyección de 3ª armónica en la referencia de modulación también redistribuye los tiempos de los estados "0" de forma que reduce el \(\Delta V\) sin un lazo de control explícito.

**Límite:** con factores de potencia muy bajos o cargas muy desequilibradas, el balanceo pasivo por inyección de armónica no es suficiente y se necesita un lazo de control de neutro explícito. En la variante T-type (con conmutador bidireccional al neutro), la corriente de neutro fluye por un camino diferente que reduce la sensibilidad al desequilibrio.

## 13 — El Flying Capacitor (FC): estados redundantes y balanceo automático

El convertidor de condensadores flotantes (Flying Capacitor, FC) de \(n\) niveles usa \(n-2\) condensadores flotantes por fase, cargados a múltiplos de \(V_{dc}/(n-1)\). La clave es que cada nivel de tensión intermedio se puede generar con múltiples combinaciones de interruptores (estados redundantes), y el sentido de la corriente en cada combinación determina si los condensadores flotantes se cargan o descargan.

Para 4 niveles: \(V_{C1}=V_{dc}/3\), \(V_{C2}=2V_{dc}/3\). El estado que produce \(V_{dc}/3\) puede usar la celda superior o la inferior; eligiendo según el SOC de cada condensador se consigue el balanceo automático sin sensor de tensión dedicado (solo con los estados naturales del modulador).

**Ventaja sobre NPC:** cada fase del FC es autónoma (no comparte el neutro con otras fases), lo que elimina el acoplamiento de la regulación de neutro entre fases. **Desventaja:** se necesitan \((n-1)(n-2)/2\) condensadores flotantes por fase, frente a \(n-2\) diodos de clamping en el NPC. Con muchos niveles, el volumen de condensadores crece cuadráticamente.

## 14 — Tabla comparativa extendida: NPC / T-type / FC / CHB / MMC

| Parámetro | NPC 3 niv. | T-type 3 niv. | FC 4 niv. | CHB 5 niv. | MMC (N=100) |
|---|---|---|---|---|---|
| Semiconductores/fase | 4 IGBT + 2 D | 4 IGBT | 6 IGBT | 8 IGBT | 200 IGBT |
| Condensadores extras | 2 bus | 2 bus | 2 flotantes | 0 (fuentes ext.) | 100 SMs |
| Fuentes DC independientes | No | No | No | Sí (×4) | No |
| Balanceo | Control PWM | Bidireccional | Estados redund. | Modulación PS | SM sorting |
| THD a \(5\,\text{kHz}\) | ~10 % | ~10 % | ~5 % | <5 % | <0.5 % |
| Pérdidas conducción | Media | Baja (T-type) | Media | Media | Baja (baja \(V_{block}\)) |
| Pérdidas conmutación | Media | Media-alta (serie) | Media | Baja (\(f_{sw}\) bajo) | Muy baja (\(f_{sw}\ll\)) |
| Nivel de tensión típico | 1–10 kV | 0.4–3 kV | 3–20 kV | 3–36 kV | 100 kV–1 MV |
| Potencia típica | 1–50 MVA | <5 MVA | 1–20 MVA | 1–100 MVA | 100 MVA–GW |

## 15 — Control de corriente circulante en el MMC

La corriente circulante del MMC es la corriente que fluye por el lazo formado por los dos brazos de una fase sin salir al exterior. Tiene una componente de corriente continua (necesaria para mantener la energía de los condensadores) y una componente a doble frecuencia de red (\(2\omega_0\)) que aparece naturalmente por la modulación.

**La componente a \(2\omega_0\) es indeseada.** Aumenta el valor eficaz de la corriente de brazo (mayores pérdidas de conducción) y complica el control de energía de los submódulos. El controlador de corriente circulante (CCSC, Circulating Current Suppression Controller) la cancela aplicando un voltaje diferencial entre brazos:

$$v_{diff,ref} = K_{CCSC}(i_{circ}^{ref} - i_{circ}^{med})$$

Donde \(i_{circ}=(i_{arm,u}+i_{arm,l})/2\) y la referencia es solo la componente DC (\(I_{DC}/2\)). El CCSC actúa en el marco de referencia a \(2\omega_0\) (marco dq girando a doble velocidad), usando controladores PI o resonantes sintonizados a \(2\omega_0\).

**Impacto en el diseño.** Sin CCSC, la ondulación de energía de los condensadores es mucho mayor → necesitan mayor capacidad (más submódulos o mayor \(C_{SM}\)). Con CCSC efectivo, la energía de los condensadores oscila solo a \(\omega_0\) (componente de 50 Hz residual), reduciendo el requisito de capacidad en un factor ×2–3.

## 16 — Pérdidas en convertidores multinivel: desglose por mecanismo

Las pérdidas totales en un convertidor multinivel son la suma de pérdidas de conmutación y conducción. Para el NPC 3 niveles vs el de 2 niveles (mismo \(V_{dc}\), misma potencia):

**Pérdidas de conducción.** Con más dispositivos en la cadena de conducción, las pérdidas de conducción por dispositivo se reducen (menor tensión de bloqueo → IGBT con menor \(V_{CE,sat}\)), pero hay más dispositivos en paralelo. Resultado: pérdidas de conducción comparables o ligeramente menores en el NPC.

**Pérdidas de conmutación.** En el NPC 3 niveles, el voltaje de bloqueo por dispositivo es \(V_{dc}/2\), pero la **energía de conmutación** de un IGBT escala como \(V_{bloqueo}^{1.5}\text{–}2\). Reducir el voltaje a la mitad puede reducir la energía de conmutación por evento a 1/3–1/4, permitiendo frecuencias de conmutación más altas con las mismas pérdidas totales.

**Pérdidas en los diodos de clamping.** Los dos diodos de clamping del NPC conducen corriente durante el estado "0" del ciclo. Sus pérdidas de conducción se suman a las de los IGBTs. En el T-type (donde el switch bidireccional reemplaza los dos diodos más dos IGBTs adicionales), las pérdidas en el nivel cero son menores porque el switch bidireccional tiene menor caída de conducción.

**Regla:** la eficiencia del NPC 3 niveles es típicamente 0.2–0.5 % mayor que la del de 2 niveles a la misma \(f_{sw}\), o permite subir \(f_{sw}\) en un factor ×2–4 con la misma eficiencia.

## 17 — Diseño del condensador de submódulo del MMC

El condensador de submódulo \(C_{SM}\) debe almacenar suficiente energía para soportar la ondulación de tensión durante el ciclo de modulación. El criterio de diseño es que la variación de tensión no supere el ±10 % del valor nominal:

$$C_{SM} \geq \frac{S_{arm}}{N\,\omega_0\,\varepsilon_v\,V_{SM}^2}$$

donde \(S_{arm}\) es la potencia aparente por brazo, \(\varepsilon_v=0.1\) es la variación máxima permitida (10 %), \(N\) es el número de SMs por brazo y \(V_{SM}=V_{dc}/N\) la tensión nominal por SM.

**Ejemplo para un HVDC de 1 GW, ±500 kV, N=400 SMs por brazo, \(V_{SM}=2{,}5\,\text{kV}\).**

$$S_{arm}=\frac{P/3}{2}=\frac{1\,\text{GW}/3}{2}=167\,\text{MVA}$$

$$C_{SM} \geq \frac{167\times10^6}{400\times2\pi\times50\times0.1\times(2500)^2}=\frac{167\times10^6}{400\times314\times0.1\times6.25\times10^6}=\frac{167\times10^6}{78.5\times10^6}\approx2.1\,\text{mF}$$

Con \(C_{SM}=2.5\,\text{mF}\) por SM (valor comercial), la energía almacenada por brazo es \(E_{arm}=\frac12 N C_{SM} V_{SM}^2=\frac12\times400\times2.5\times10^{-3}\times6.25\times10^6=3{,}125\,\text{MJ}\) — comparable a la energía de un volante de inercia pequeño. Este es uno de los aspectos que hace al MMC útil como reserva de energía inertial.

## 18 — Seguridad de fallo en MMC: operación con submódulos defectuosos

El MMC tiene tolerancia de fallo inherente: si un SM falla, puede cortocircuitarse (bypass) y el convertidor sigue operando con \(N-1\) SMs activos por brazo, con una reducción de la tensión de salida máxima de \(1/N\):

$$V_{out,max,fault} = V_{dc}\cdot\frac{N-1}{N} = V_{dc}\left(1-\frac{1}{N}\right)$$

Para \(N=400\): la pérdida de un SM reduce \(V_{out,max}\) en solo 0.25 %. En la práctica, se diseña con un 5–10 % de SMs de reserva para tolerar múltiples fallos simultáneos sin reducir la potencia nominal.

**Gestión del fallo.** Al detectar un SM defectuoso (sobretensión del condensador o fallo de gate drive), el controlador:
1. Activa el bypass (interruptor de cortocircuito mecánico o semiconductor).
2. Redistribuye la modulación entre los SMs restantes, manteniendo la tensión de brazo total.
3. Registra el evento para mantenimiento programado.

## 19 — Modulación del MMC: Nearest Level Modulation (NLM) vs PWM

Con cientos de submódulos, el MMC puede modular de forma diferente al PWM clásico:

**Nearest Level Modulation (NLM).** En cada periodo de control, la referencia de tensión de brazo \(v_{arm}^*\) se redondea al nivel más cercano \(n_{insert}=\text{round}(v_{arm}^*\cdot N/V_{dc})\). Solo conmutan uno o dos SMs por cambio de nivel. Con N=400, la transición entre niveles produce un \(dv/dt\) de \(V_{SM}/t_{sw}\approx2500/(5\,\mu\text{s})=0.5\,\text{kV/\mu s}\) — mucho menor que en un convertidor de 2 niveles.

**SM sorting.** En cada paso de NLM, el controlador selecciona qué SMs insertar/retirar usando capacitor voltage sorting: ordenar los SMs por tensión de condensador y elegir los de menor/mayor tensión según si la corriente de brazo los carga o descarga. Esto garantiza el balanceo de tensión sin lazo de control explícito adicional.

## 20 — Normas y estándares aplicables a convertidores multinivel

- **IEEE 519-2014:** límites de THD de corriente en el PCC (THD_I <5% para cargas >20 MVA a alta tensión). El MMC y el CHB de 5+ niveles cumplen este requisito sin filtro adicional.
- **IEC 61800-3:** requisitos de EMC para accionamientos de velocidad variable; límites de clase C3/C4 para accionamientos de MT.
- **EN 50160:** calidad de la tensión en redes públicas (THD_V <5% a MT); la conexión de convertidores no debe agravar el THD en el PCC.
- **IEEE 1547-2018:** interconexión con distribución; incluye ride-through de tensión/frecuencia, soporte de Q y límites de armónicos.
- **Cigré B4-57:** guía de diseño y operación de sistemas HVDC con MMC (VSC-HVDC).

## Errores comunes
- Ignorar el balanceo de condensadores (NPC neutro, FC, MMC): puede divergir.
- Subestimar el coste de control y medida al subir niveles.
- Aplicar el modelo de 2 niveles (ganancia del modulador \( V_{dc}/V_{tri} \)) al NPC sin ajustar por 2.
- Olvidar la corriente circulante en el MMC: puede disparar la protección de sobrecorriente.

## Conceptos relacionados
- [[convertidor-vsc|modelo promediado]] · [[marco-dq]] · [[control-vectorial]] · [[semiconductores-potencia]]

## 21 — Tendencias: SiC y GaN en convertidores multinivel

Los semiconductores de banda ancha (Wide Bandgap, WBG) — SiC MOSFET y GaN HEMT — están cambiando el diseño de los convertidores multinivel:

**SiC MOSFETs en NPC 3 niveles.** Con tensiones de bloqueo de 1200–3300 V y \(R_{on}\) muy bajo, los SiC MOSFETs permiten frecuencias de conmutación de 50–200 kHz en el NPC 3 niveles de potencia media (1–10 kW). La mayor \(f_{sw}\) reduce el tamaño del filtro LCL en un factor \((f_{sw,SiC}/f_{sw,Si})^2\), típicamente ×4–16. Las pérdidas totales caen al 0.3–0.5 % (vs 0.8–1.5 % con Si IGBT), mejorando la densidad de potencia.

**GaN en T-type de baja tensión.** GaN HEMTs de 650 V permiten frecuencias de conmutación de 1 MHz en convertidores de baja potencia (<10 kW). En el T-type, el switch bidireccional al neutro (el que mayor frecuencia necesita) se implementa con GaN, mientras los switches de los extremos usan Si de 1200 V (solo conmutan a la fundamental). Resultado: ventajas de eficiencia del GaN donde más importa, con coste reducido.

**MMC con SiC.** Con SiC en los SMs, \(f_{sw}\) puede subir de 150 Hz a 500–1000 Hz por SM, reduciendo la ondulación de tensión del condensador y permitiendo condensadores más pequeños. El principal beneficio: menor volumen de la instalación y menores costes de mantenimiento.

## 22 — Ejemplo de código: simulación del NPC 3 niveles con balanceo

```python
import numpy as np

def npc_modulate(ref, Vdc, Vc1, Vc2, i_load):
    """Modulador NPC 3 niveles con balanceo de neutro.
    ref: referencia normalizada en [-1, 1]
    Devuelve: nivel de tensión (Vdc/2, 0, -Vdc/2) y ajuste de balanceo."""
    dV = Vc1 - Vc2  # desequilibrio del punto neutro
    # Inyección de offset de neutro proporcional al desequilibrio
    offset = -0.05 * dV * np.sign(i_load)
    ref_adj = np.clip(ref + offset, -1, 1)
    if ref_adj > 0.5:
        return Vdc/2, 1   # estado P
    elif ref_adj > -0.5:
        return 0, 0       # estado O (neutro)
    else:
        return -Vdc/2, -1 # estado N

# Ejemplo de uso
Vdc = 800; Vc1 = 402; Vc2 = 398; f0 = 50; Ts = 1e-4
t = np.arange(0, 0.04, Ts)
ref = 0.9 * np.sin(2*np.pi*f0*t)
i_load = 100 * np.sin(2*np.pi*f0*t - np.pi/6)  # carga inductiva
v_out = np.array([npc_modulate(r, Vdc, Vc1, Vc2, il)[0]
                  for r, il in zip(ref, i_load)])
```

## Referencias
- Rodriguez et al., *Multilevel Inverters: Survey of Topologies*, IEEE TIE 2002.
- Akagi, *Classification and Terminology of MMC*, IEEE TPEL 2011.
- Lesnicar & Marquardt, *An Innovative Modular Multilevel Converter Topology*, IEEE ISIE 2003.
