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
fecha_actualizacion: 2026-06-10
relacionados: [dinamica-bus-dc, carga-potencia-constante-cpl, control-tension-bus-dc, fotovoltaica-mppt, modelo-promediado]
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
- [[dinamica-bus-dc]] · [[carga-potencia-constante-cpl]] · [[control-tension-bus-dc]] · [[fotovoltaica-mppt]] · [[modelo-promediado]]

## Referencias
- Erickson & Maksimovic, *Fundamentals of Power Electronics*.
