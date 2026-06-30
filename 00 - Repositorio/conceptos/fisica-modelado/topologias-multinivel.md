---
titulo: Topologías de inversores multinivel
slug: topologias-multinivel
categoria: fisica-modelado
tipo: concepto
nivel: avanzado
proyectos: []
objetivos: [elegir la topologia de convertidor segun tension, potencia y calidad]
tags: [multinivel, NPC, T-type, flying-capacitor, MMC, CHB]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-30
relacionados: [convertidor-vsc, marco-dq, control-vectorial, semiconductores-potencia]
referencias:
  - "Rodriguez, Lai, Peng, Multilevel Inverters: Survey of Topologies, IEEE TIE 2002"
  - "Akagi, Classification and Terminology of MMC, IEEE TPEL 2011"
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

**Paso 2 — el salto de tensión en cada conmutación.** La salida pasa de un nivel al adyacente, no de un extremo al otro. El salto es la separación entre niveles consecutivos, igual a la tensión de bloqueo:

$$ \Delta v = \frac{V_{dc}}{n-1} $$

El \( dv/dt \) lo fija ese salto dividido por el tiempo de conmutación \( t_{sw} \) del dispositivo:

$$ \frac{dv}{dt}\approx\frac{\Delta v}{t_{sw}}=\frac{V_{dc}}{(n-1)\,t_{sw}} $$

**Paso 3 — comparar 3 niveles con 2 niveles.** Manteniendo \( V_{dc} \) y \( t_{sw} \), el cociente es:

$$ \frac{(dv/dt)_{3\text{niv}}}{(dv/dt)_{2\text{niv}}}=\frac{V_{dc}/2}{V_{dc}/1}=\frac12 $$

El \( dv/dt \) cae a la **mitad** al pasar de 2 a 3 niveles: menor estrés en el aislamiento del motor, menos EMI. En general escala como \( 1/(n-1) \).

**Paso 4 — los armónicos.** La onda escalonada de \( n \) niveles se aproxima mejor a la senoidal: cada paso de \( V_{dc}/(n-1) \) es más pequeño, por lo que la amplitud del rizado de conmutación —y con él la \( THD \) de tensión— escala también como \( \sim 1/(n-1) \). Con la misma \( f_{sw} \), una onda de 7 niveles tiene una \( THD \) muy inferior a la de 2 niveles antes de filtrar. Por eso el multinivel permite filtros de salida más pequeños o frecuencias de conmutación más bajas (menos pérdidas) para la misma calidad.

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
# tension de bloqueo por dispositivo y niveles
n_niveles = 3
V_bloqueo = Vdc/(n_niveles-1)     # menor tension por interruptor que en 2 niveles
```

## Parámetros y valores típicos
3 niveles (NPC/T-type) en convertidores industriales; decenas-cientos de submódulos en MMC para
HVDC. Tensión de bloqueo repartida \( V_{dc}/(n-1) \).

## Errores comunes
- Ignorar el balanceo de condensadores (NPC neutro, FC, MMC): puede divergir.
- Subestimar el coste de control y medida al subir niveles.

## Uso en proyectos
- Candidato a proyecto propio (MMC). Ficha de panorama por ahora; los proyectos 01/02 usan 2
  niveles (modelo promediado).

## Conceptos relacionados
- [[convertidor-vsc|modelo promediado]] · [[marco-dq]] · [[control-vectorial]]

## Referencias
- Rodriguez et al., *Multilevel Inverters: Survey of Topologies*, IEEE TIE 2002.
