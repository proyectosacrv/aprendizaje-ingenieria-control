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
fecha_actualizacion: 2026-06-30
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

<div class="cfig"><img src="figuras/droop-dc-reparto.png" alt="curvas V-I de droop DC y reparto de corriente"><div class="cap">Cada convertidor impone una recta $V_{dc}=V_{dc}^*-R_d I_o$. Como todos comparten el mismo $V_{bus}$, el reparto de corriente queda fijado por las pendientes: $I_1/I_2=R_{d2}/R_{d1}$ (aquí 2:1). Más $R_d$ mejora el reparto pero hunde más la tensión con la carga.</div></div>

## 1 — De dos rectas V–I al reparto de corriente
**Paso 1 — la recta de cada fuente.** Cada convertidor \( i \) impone una característica lineal entre la tensión que entrega y la corriente que da:
$$ V_{dc}=V_{dc}^*-R_{d,i}\,I_{o,i} $$
Es una recta de ordenada en el origen \( V_{dc}^* \) (tensión en vacío) y pendiente \( -R_{d,i} \). Cuanto más carga, más cae la tensión.

**Paso 2 — el nudo común fuerza un único \( V_{dc} \).** Todas las unidades cuelgan del mismo bus, así que en régimen permanente comparten **la misma tensión** \( V_{dc} \). Para dos fuentes con igual \( V_{dc}^* \):
$$ V_{dc}=V_{dc}^*-R_{d,1}I_{o,1}=V_{dc}^*-R_{d,2}I_{o,2} $$

**Paso 3 — cancelar e invertir.** Restando \( V_{dc}^* \) de ambos lados queda \( R_{d,1}I_{o,1}=R_{d,2}I_{o,2} \), de donde
$$ \boxed{\;\frac{I_{o,1}}{I_{o,2}}=\frac{R_{d,2}}{R_{d,1}}\;} $$
El reparto es **inversamente proporcional** a la resistencia de droop: la unidad con menor \( R_d \) (recta más plana) carga más. Con \( R_{d,1}=2R_{d,2} \) sale \( I_{o,1}/I_{o,2}=1/2 \): la primera da la mitad de corriente que la segunda. La pendiente de droop hace de "ganancia de reparto" sin que las unidades se comuniquen — solo "ven" la tensión común del bus, igual que el droop AC reparte por la frecuencia común.

## 2 — Cómo la resistencia de cable distorsiona el reparto
**Paso 1 — el cable se suma en serie.** Entre los bornes del convertidor \( i \) y el nudo común hay un cable de resistencia \( R_{line,i} \). La tensión en el **nudo** es la del convertidor menos la caída del cable:
$$ V_{bus}=\underbrace{V_{dc}^*-R_{d,i}I_{o,i}}_{\text{bornes}}-R_{line,i}I_{o,i}=V_{dc}^*-(R_{d,i}+R_{line,i})\,I_{o,i} $$
La resistencia efectiva de droop vista desde el bus es \( R_{d,i}+R_{line,i} \), no \( R_{d,i} \).

**Paso 2 — el reparto real.** Repitiendo el paso 3 del apartado anterior con esa resistencia efectiva:
$$ \frac{I_{o,1}}{I_{o,2}}=\frac{R_{d,2}+R_{line,2}}{R_{d,1}+R_{line,1}} $$
El reparto deseado \( R_{d,2}/R_{d,1} \) solo se recupera si \( R_{line,i}\ll R_{d,i} \). Si \( R_d \) es pequeño y comparable a \( R_{line} \), el cableado (asimétrico entre unidades) decide el reparto y lo desequilibra.

**Paso 3 — las dos salidas.** De aquí el compromiso de la ficha: subir \( R_d \) para que \( R_d\gg R_{line} \) ancla el reparto al diseño, **pero** hunde más la tensión con la carga (\( \Delta V=R_d I_{max} \)). La regulación perdida la repone el **secundario** sumando \( \delta V \) a \( V_{dc}^* \) (ver [[control-jerarquico-microrred]]), que también puede compensar el sesgo de \( R_{line} \) sin tener que subir \( R_d \).

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
