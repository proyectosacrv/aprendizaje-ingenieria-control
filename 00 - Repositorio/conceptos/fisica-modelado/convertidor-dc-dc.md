---
titulo: Convertidor DC-DC (buck / boost)
slug: convertidor-dc-dc
categoria: fisica-modelado
tipo: concepto
nivel: basico
proyectos: [03-DataCenter-IA]
objetivos: [entender la célula básica de conversión DC y el origen de la carga CPL]
tags: [dc-dc, buck, boost, duty, conmutado, basico]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-06-30
relacionados: [dinamica-bus-dc, control-tension-bus-dc, fotovoltaica-mppt, convertidor-vsc]
referencias:
  - "Erickson & Maksimovic, Fundamentals of Power Electronics"
---

## Definición
Convierte un nivel de tensión continua en otro, controlando el **ciclo de trabajo** \( D \) (fracción
del periodo en que el interruptor conduce). El **buck** reduce la tensión, el **boost** la eleva.

## Fundamento teórico
En régimen permanente, el balance volt-segundo en el inductor (su tensión media es cero) da las
relaciones de conversión en conducción continua (CCM):
$$ \text{Buck:}\quad V_o = D\,V_{in}, \qquad \text{Boost:}\quad V_o = \frac{V_{in}}{1-D} $$
La corriente de entrada/salida cumple el balance de potencia \( V_{in}I_{in}=V_o I_o \) (ideal). El
inductor y el condensador filtran el rizado; si la corriente del inductor llega a cero aparece la
**conducción discontinua** (DCM), con otras relaciones. El control regula \( V_o \) ajustando \( D \)
con un lazo (a menudo en cascada: tensión externa, corriente interna).

<div class="cfig"><img src="figuras/convertidor-dc-dc-ratio.png" alt="relacion de conversion buck y boost"><div class="cap">Relación de conversión en CCM: el buck reduce la tensión (Vo/Vin=D) y el boost la eleva (1/(1−D)). El control ajusta D para regular Vo.</div></div>

## 1 — Ganancia del buck \( V_o=D\,V_{in} \) por balance voltios-segundo
**Paso 1 — el principio.** En régimen permanente la corriente media del inductor no cambia de un ciclo al siguiente, luego su tensión media en un periodo es cero: \( \langle v_L\rangle=\frac1T\int_0^T v_L\,dt=0 \). Equivale a decir que el área voltios-segundo en el subintervalo de conducción cancela exactamente la del subintervalo de bloqueo.

**Paso 2 — las dos fases del buck.** El inductor une el nudo de conmutación con la salida \( V_o \).
- Interruptor cerrado (fracción \( D\,T \)): el nudo está a \( V_{in} \), así que \( v_L=V_{in}-V_o \).
- Interruptor abierto (fracción \( (1-D)\,T \)): el diodo conduce y el nudo está a \( 0 \), así que \( v_L=-V_o \).

**Paso 3 — igualar el área a cero.**

$$ (V_{in}-V_o)\,D\,T+(-V_o)\,(1-D)\,T=0 $$

Dividiendo por \( T \) y desarrollando:

$$ D\,V_{in}-D\,V_o-V_o+D\,V_o=0\;\Longrightarrow\;D\,V_{in}-V_o=0 $$

(los términos \( \pm D V_o \) se cancelan). Despejando:

$$ \boxed{\;V_o=D\,V_{in}\;} $$

Como \( 0\le D\le1 \), el buck siempre **reduce** la tensión. Con \( V_{in}=400 \) y \( D=0.5 \) da \( V_o=200\,\text{V} \).

## 2 — Ganancia del boost \( V_o=V_{in}/(1-D) \) por balance voltios-segundo
**Paso 1 — las dos fases del boost.** Ahora el inductor está entre la entrada \( V_{in} \) y el nudo de conmutación.
- Interruptor cerrado (\( D\,T \)): el inductor se conecta a tierra, \( v_L=V_{in} \) (se carga).
- Interruptor abierto (\( (1-D)\,T \)): el inductor descarga hacia la salida a través del diodo, \( v_L=V_{in}-V_o \).

**Paso 2 — balance voltios-segundo.**

$$ V_{in}\,D\,T+(V_{in}-V_o)\,(1-D)\,T=0 $$

Dividiendo por \( T \) y agrupando los términos en \( V_{in} \):

$$ V_{in}\big[D+(1-D)\big]-V_o\,(1-D)=0\;\Longrightarrow\;V_{in}-V_o\,(1-D)=0 $$

(\( D+(1-D)=1 \)). Despejando:

$$ \boxed{\;V_o=\frac{V_{in}}{1-D}\;} $$

Como \( 1-D<1 \), el boost siempre **eleva** la tensión, y diverge cuando \( D\to1 \) (de ahí evitar \( D \) cerca de los extremos). Con \( V_{in}=400 \) y \( D=0.5 \): \( V_o=800\,\text{V} \). La corriente queda fijada aparte por el balance de potencia ideal \( V_{in}I_{in}=V_o I_o \).

## Cuándo y por qué se usa
Es la base de las fuentes conmutadas, del MPPT fotovoltaico, y de los **POL** (point-of-load) que
alimentan los servidores. Es clave entender que un DC-DC **regulado** que mantiene su potencia de
salida constante se comporta, visto desde su entrada, como una **carga de potencia constante (CPL)**
con resistencia incremental negativa.

## Procedimiento de diseño (genérico)
1. Elige topología según \( V_o/V_{in} \) (buck si \( <1 \), boost si \( >1 \)).
2. Fija \( f_{sw} \) y dimensiona \( L \) (por el rizado de corriente) y \( C \) (por el rizado de
   tensión).
3. Diseña el lazo de regulación de \( V_o \) (cascada tensión/corriente).

## Ejemplo de código
```python
Vin, D = 400.0, 0.5
Vo_buck  = D*Vin                 # 200 V
Vo_boost = Vin/(1-D)             # 800 V
```

## Parámetros y valores típicos
\( D \) entre 0.1 y 0.9 (extremos comprometen el control). \( f_{sw} \) de decenas de kHz a MHz según
potencia. Rizado de corriente del inductor objetivo ≈ 20–40 % de la nominal.

## Errores comunes
- Confundir las relaciones de buck y boost (o ignorar pérdidas que las modifican).
- Operar muy cerca de \( D=0 \) o \( D=1 \) (mal condicionado).
- No reconocer que el lazo de regulación crea el comportamiento CPL (desamortigua el bus que lo alimenta).

## Uso en proyectos
- **03 - DataCenter-IA:** los servidores (POL DC-DC regulados) se modelan como CPL en el bus DC; su
  resistencia negativa es la causa de la inestabilidad estudiada.

## Conceptos relacionados
- [[dinamica-bus-dc]] · [[control-tension-bus-dc]] · [[fotovoltaica-mppt]] · [[convertidor-vsc|modelo promediado]]

## Referencias
- Erickson & Maksimovic, *Fundamentals of Power Electronics*.
