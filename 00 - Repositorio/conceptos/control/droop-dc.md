---
titulo: Droop DC y reparto de carga en bus continuo
slug: droop-dc
categoria: control
tipo: tecnica
nivel: intermedio
proyectos: []
objetivos: [repartir corriente entre fuentes de un bus DC sin comunicaciones]
tags: [droop-dc, reparto-carga, bus-dc, resistencia-virtual, microrred-dc, intermedio]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-09
relacionados: [droop-control, control-tension-bus-dc, dinamica-bus-dc, control-jerarquico-microrred, microrred-hibrida-ac-dc]
referencias:
  - "Guerrero et al., Hierarchical Control of Droop-Controlled AC and DC Microgrids, IEEE TIE 2011"
  - "Lu et al., State-of-Charge Balancing Using Adaptive Droop for DC Microgrids, IEEE TPEL 2014"
---

## Definición
Estrategia de control primario que reparte la corriente/potencia entre varias fuentes conectadas a
un **bus DC común** introduciendo una **caída de tensión proporcional a la corriente** (resistencia
virtual), sin necesidad de comunicaciones entre convertidores.

## Fundamento teórico
Cada convertidor sigue la ley:
$$ V_{dc}=V_{dc}^*-R_d\,I_o $$
con \( R_d \) la **resistencia de droop (virtual)**. Como todas las unidades comparten el mismo
\( V_{dc} \) del bus, el reparto de corriente queda fijado por
$$ \frac{I_{o,1}}{I_{o,2}}=\frac{R_{d,2}}{R_{d,1}} $$
es decir, **inversamente proporcional** a la resistencia de droop. Análogo DC del [[droop-control|
droop AC]] (allí \( \omega\!-\!P \); aquí \( V_{dc}\!-\!I \)).

**Compromiso fundamental:** un \( R_d \) grande mejora el reparto y la estabilidad pero empeora la
**regulación de tensión** (mayor caída con la carga). La desviación de tensión la corrige el nivel
**secundario** (ver [[control-jerarquico-microrred]]) sumando \( \delta V \) a \( V_{dc}^* \).

**Error por resistencia de línea:** las resistencias de cable \( R_{line,i} \) se suman a \( R_d \) y
distorsionan el reparto; \( R_d\gg R_{line} \) lo mitiga, o se compensa en el secundario. Variantes:
droop **adaptativo** (función del SoC para equilibrar baterías) y droop no lineal.

## Cuándo y por qué se usa
En microrredes DC y en el subsistema DC de la [[microrred-hibrida-ac-dc|microrred híbrida]] (data
center): reparto robusto entre fuentes/baterías/convertidores de interconexión sin depender de
comunicaciones, como capa primaria del control jerárquico.

## Procedimiento de diseño (genérico)
1. Fija la desviación de tensión admisible \( \Delta V_{dc} \) a plena carga → \( R_d=\Delta V_{dc}/I_{max} \).
2. Comprueba que \( R_d\gg R_{line} \) para que el reparto no dependa del cableado.
3. Cierra el lazo de tensión del convertidor sobre la referencia con droop ([[control-tension-bus-dc]]).
4. Añade restauración secundaria de \( V_{dc} \) y, si hay baterías, droop adaptativo por SoC.
5. Verifica estabilidad con carga CPL ([[dinamica-bus-dc]]) y reparto en todo el rango.

## Ejemplo de código
```python
def dc_droop(Vdc_ref, Io, Rd, dV_sec=0.0):
    return Vdc_ref - Rd*Io + dV_sec      # referencia de tension con droop + secundario
# reparto: Io1/Io2 = Rd2/Rd1
```

## Parámetros y valores típicos
Desviación de tensión por droop 1–5 % de \( V_{dc} \). \( R_d \) tal que \( R_d\gg R_{line} \).
Banda del secundario ~1/10 de la del lazo de tensión.

## Errores comunes
- \( R_d \) pequeño → reparto dominado por las resistencias de línea (desequilibrado).
- \( R_d \) grande sin secundario → caída de tensión excesiva con carga.
- Ignorar la impedancia negativa de cargas CPL al evaluar la estabilidad del bus.

## Conceptos relacionados
- [[droop-control]] · [[control-tension-bus-dc]] · [[dinamica-bus-dc]] · [[control-jerarquico-microrred]] · [[microrred-hibrida-ac-dc]]

## Referencias
- Guerrero et al., *Hierarchical Control of Droop-Controlled AC and DC Microgrids*, IEEE TIE 2011.
- Lu et al., *State-of-Charge Balancing Using Adaptive Droop for DC Microgrids*, IEEE TPEL 2014.
