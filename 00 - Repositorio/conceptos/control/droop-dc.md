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
fecha_actualizacion: 2026-07-02
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

## 3 — Estado estacionario con N fuentes: tensión del bus y ejemplo numérico

Con \( N \) convertidores en paralelo, cada uno con tensión en vacío \( V_{0,i} \) y resistencia de droop \( R_{d,i} \), y una carga resistiva \( R_{load} \) en el bus, el estado estacionario se obtiene igualando la suma de corrientes de las fuentes a la corriente de carga.

**Paso 1 — corriente de cada fuente.** De la ley de droop:

$$
I_{o,i} = \frac{V_{0,i} - V_{bus}}{R_{d,i}}
$$

**Paso 2 — corriente de carga.**

$$
I_{load} = \frac{V_{bus}}{R_{load}}
$$

**Paso 3 — balance de nudo** (\( \sum I_{o,i} = I_{load} \)):

$$
\sum_{i=1}^{N}\frac{V_{0,i}-V_{bus}}{R_{d,i}} = \frac{V_{bus}}{R_{load}}
$$

Despejando \( V_{bus} \):

$$
\boxed{V_{bus} = \frac{\displaystyle\sum_{i=1}^{N}\frac{V_{0,i}}{R_{d,i}}}{\displaystyle\sum_{i=1}^{N}\frac{1}{R_{d,i}}+\frac{1}{R_{load}}}}
$$

**Ejemplo numérico (data center, 2 fuentes).** \( V_{0,1}=V_{0,2}=400\,\text{V} \), \( R_{d,1}=0.5\,\Omega \), \( R_{d,2}=1.0\,\Omega \), \( R_{load}=400/60=6.67\,\Omega \) (60 A de carga total, 400 V nominal).

$$
V_{bus}=\frac{400/0.5+400/1.0}{1/0.5+1/1.0+1/6.67}=\frac{800+400}{2+1+0.15}=\frac{1200}{3.15}\approx381\,\text{V}
$$

Corrientes:

$$
I_1=\frac{400-381}{0.5}=38\,\text{A}, \quad I_2=\frac{400-381}{1.0}=19\,\text{A}
$$

Comprobación: \( I_1+I_2=57\approx60\,\text{A} \) (error por redondeo). Reparto: \( I_1/I_2=2 = R_{d,2}/R_{d,1} \) ✓. La caída de tensión en carga nominal es \( 400-381=19\,\text{V} \), o sea **4.75 %** — dentro del ±5 % usual para bus DC.

**Efecto de añadir más fuentes.** Con \( N \) fuentes iguales (\( V_{0,i}=V_0 \), \( R_{d,i}=R_d \)):

$$
V_{bus} = \frac{V_0\cdot N/R_d}{N/R_d + 1/R_{load}} = V_0\cdot\frac{1}{1+R_d/(N\cdot R_{load})}
$$

Al añadir fuentes (subir \( N \)), la impedancia droop equivalente cae \( (R_d/N) \) y la tensión de bus se aproxima a \( V_0 \). La caída porcentual con \( N \) fuentes es la mitad que con \( N/2 \).

## 4 — Droop DC en microrredes: robustez cuando \( R_d \gg R_{cable} \)

La robustez del droop DC frente a la asimetría del cableado se cuantifica comparando la desviación del reparto respecto al ideal.

**Error de reparto relativo.** Si el reparto ideal es \( I_1^*/I_2^*=R_{d,2}/R_{d,1} \) pero con cables el reparto real es \( I_1/I_2=(R_{d,2}+R_{line,2})/(R_{d,1}+R_{line,1}) \), el error relativo es:

$$
\varepsilon_{reparto}=\frac{I_1/I_2 - I_1^*/I_2^*}{I_1^*/I_2^*}=\frac{R_{line,2}R_{d,1}-R_{line,1}R_{d,2}}{R_{d,1}\,R_{d,2}}
$$

Para \( R_{line,1}=R_{line,2}=R_{line} \): \( \varepsilon=(R_{line}(R_{d,1}-R_{d,2}))/(R_{d,1}R_{d,2}) \). Si \( R_{d,1}=R_{d,2}=R_d \): el error es cero independientemente del cable — el droop simétrico anula el efecto de líneas iguales. La asimetría del reparto solo aparece cuando los cables son diferentes.

**Regla práctica.** Para un error máximo \( \varepsilon_{max}=5\% \) con asimetría de cable de \( \Delta R_{line} \):

$$
R_d \geq \frac{\Delta R_{line}}{\varepsilon_{max}}
$$

Con \( \Delta R_{line}=0.1\,\Omega \) y \( \varepsilon_{max}=5\% \): \( R_d \geq 2\,\Omega \). Este valor puede ser mayor que el calculado por la caída de tensión (\( \Delta V/I_{max} \)) — en ese caso el criterio del cable es el restrictivo.

**Microrred de data center.** En el proyecto de la [[microrred-hibrida-ac-dc|microrred híbrida]], el bus DC a 400 V alimenta servidores (cargas CPL) y baterías. Con cableado de cobre de 10 m y sección 10 mm²: \( R_{line}\approx17\,\text{m}\Omega/\text{m}\times10=170\,\text{m}\Omega \). Para \( \varepsilon<5\% \): \( R_d\geq3.4\,\Omega \). Esto daría una caída de tensión a 60 A de \( 3.4\times60=204\,\text{V} \) — inaceptable. **Solución:** usar sección mayor (25 mm², \( R_{line}\approx68\,\text{m}\Omega \)) para bajar la asimetría, y fijar \( R_d=0.5\,\Omega \) con control secundario que compense el resto.

## 5 — Corrección secundaria: restaurar \( V_{nom} \), jerarquía primario-secundario-terciario

El droop primario sacrifica tensión para lograr el reparto. La **corrección secundaria** la restaura sin romper el reparto.

**Principio.** El secundario mide \( V_{bus} \) (o un estimado por comunicaciones de baja velocidad) y calcula un offset \( \delta V_{sec} \) que suma a todas las referencias primarias simultáneamente:

$$
V_{ref,i} = V_{0,i} + \delta V_{sec}
$$

La corrección no cambia las pendientes de droop, solo desplaza verticalmente todas las rectas V-I. El nuevo punto de operación tiene la misma relación \( I_1/I_2 \) pero con \( V_{bus} \) más alta.

**Control secundario típico.** Un integrador lento (banda ~1/10 del lazo primario) que anula el error de tensión en régimen permanente:

$$
\delta V_{sec}(t) = K_{sec}\int_0^t (V_{nom}-V_{bus}(\tau))\,d\tau
$$

La velocidad del secundario es intencionalmente baja para no interferir con el lazo primario de tensión, que es el que proporciona la respuesta rápida a perturbaciones de carga.

**Jerarquía completa.** El control jerárquico de la microrred DC tiene tres niveles:

1. **Primario (µs–ms):** lazo de tensión local + droop. Responde a escalones de carga, comparte corriente entre fuentes sin comunicaciones. No restaura \( V_{nom} \).

2. **Secundario (segundos):** restaura \( V_{bus}=V_{nom} \) enviando \( \delta V_{sec} \) a todas las unidades por una red de comunicaciones de baja latencia (~100 ms). Puede también compensar el sesgo de \( R_{line} \) ajustando \( V_{0,i} \) de forma individual.

3. **Terciario (minutos–horas):** gestión de energía, SoC de baterías, intercambio con la red AC. Ajusta las referencias de droop (\( V_{0,i} \), \( R_{d,i} \)) para optimizar la operación.

**Por qué el secundario no rompe el reparto.** Si el secundario envía el mismo \( \delta V_{sec} \) a todas las unidades (señal broadcast), el desplazamiento vertical es idéntico para todas las rectas V-I. El punto de cruce con la horizontal \( V_{bus} \) se eleva, pero las corrientes se reparten de la misma forma:

$$
\frac{I_{o,1}}{I_{o,2}}=\frac{V_{0,2}+\delta V_{sec}-V_{bus}'}{R_{d,2}}\cdot\frac{R_{d,1}}{V_{0,1}+\delta V_{sec}-V_{bus}'}=\frac{R_{d,2}}{R_{d,1}} \quad \checkmark
$$

## 6 — Diseño iterativo para data center: conflicto \( R_d \) mínimo/máximo y solución normalizada

En el proyecto de microrred de data center (Proyecto 03), el bus DC a 400 V debe cumplir simultáneamente:

- **Regulación de tensión:** caída ≤ 5 % = 20 V a plena carga (\( I_{max}=100\,\text{A} \)).
- **Robustez al cable:** \( R_d \gg R_{line,max}=200\,\text{m}\Omega \) (peor caso de cableado asimétrico).
- **Estabilidad con CPL:** la impedancia de droop debe superar la impedancia negativa de la CPL: \( R_d > P_{CPL}/V_{bus}^2 \) (criterio de impedancia).

**Conflicto.** De la caída máxima: \( R_d \leq \Delta V/I_{max}=20/100=0.2\,\Omega \). De la robustez al cable: \( R_d \geq 20\times R_{line}=4\,\Omega \). **Contradicción**: no es posible satisfacer ambos con una \( R_d \) fija.

**Solución normalizada.** Usar \( R_d=0.5\,\Omega \) (compromiso: caída del 12.5 % a plena carga, pero robusto con cableado moderado ≤25 mΩ) y delegar la restauración de tensión al **secundario**. El resultado es:

| capa | función | velocidad |
|---|---|---|
| primario (droop) | reparto de corriente | rápida (lazo de V: ~200 Hz) |
| secundario (PI lento) | restaura \( V_{bus}=400\,\text{V} \) | lenta (~1 Hz) |
| terciario | equilibra SoC baterías | muy lenta (~1/hora) |

**Cálculo de \( R_d \) por estabilidad con CPL.** La carga CPL (\( P_{CPL}=30\,\text{kW} \) a 400 V) tiene impedancia negativa \( Z_{CPL}=-V^2/P=-5.3\,\Omega \). Para estabilidad con droop, el criterio simplificado es \( R_d > |Z_{CPL}|\cdot(R_d/(R_d+Z_{filter})) \approx R_d > 0.5\,\Omega \). Ver [[dinamica-bus-dc]] para el análisis completo con la matriz de estado.

<div class="cfig"><img src="figuras/droop-dc-analisis.png" alt="analisis completo droop dc"><div class="cap">Cuatro paneles: (a) curvas V-I de dos fuentes y punto de operación compartido — el reparto es 2:1 según Rd; (b) corrientes y tensión de bus vs carga total; (c) error de reparto al aumentar la resistencia de cable de la fuente 1; (d) corrección secundaria — subir δV restaura Vnom sin alterar el reparto.</div></div>

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

# Tension de bus en regimen estacionario con N fuentes
def Vbus_ss(V0_list, Rd_list, Rload):
    num = sum(V0/Rd for V0, Rd in zip(V0_list, Rd_list))
    den = sum(1/Rd for Rd in Rd_list) + 1/Rload
    return num / den

# Ejemplo: 2 fuentes, 60 A de carga
Vbus = Vbus_ss([400, 400], [0.5, 1.0], 400/60)
print(f"Vbus = {Vbus:.1f} V")  # 381 V
```

## Parámetros y valores típicos
Desviación de tensión por droop 1–5 % de \( V_{dc} \). \( R_d \) tal que \( R_d\gg R_{line} \).
Banda del secundario ~1/10 de la del lazo de tensión.

## Errores comunes
- \( R_d \) pequeño → reparto dominado por las resistencias de línea (desequilibrado).
- \( R_d \) grande sin secundario → caída de tensión excesiva con carga.
- Ignorar la impedancia negativa de cargas CPL al evaluar la estabilidad del bus.
- Usar el mismo \( R_d \) para fuentes con potencias nominales muy distintas (el reparto debe ser proporcional a la capacidad: \( R_{d,i}\propto1/P_{nom,i} \)).

## Conceptos relacionados
- [[droop-control]] · [[control-tension-bus-dc]] · [[dinamica-bus-dc]] · [[control-jerarquico-microrred]] · [[microrred-hibrida-ac-dc]]

## Referencias
- Guerrero et al., *Hierarchical Control of Droop-Controlled AC and DC Microgrids*, IEEE TIE 2011.
- Lu et al., *State-of-Charge Balancing Using Adaptive Droop for DC Microgrids*, IEEE TPEL 2014.
