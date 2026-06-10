---
titulo: Microrred híbrida AC/DC e interlink converter
slug: microrred-hibrida-ac-dc
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: []
objetivos: [entender la arquitectura de una microrred con subredes AC y DC acopladas]
tags: [microrred-hibrida, ac-dc, interlink, ilc, bus-dc, datacenter, intermedio]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-09
relacionados: [convertidor-vsc, dinamica-bus-dc, droop-dc, control-jerarquico-microrred, carga-pulsante-datacenter-ia]
referencias:
  - "Loh et al., Autonomous Operation of Hybrid Microgrid With AC and DC Subgrids, IEEE TPEL 2013"
  - "Nejabatkhah, Li, Overview of Power Management Strategies of Hybrid AC/DC Microgrid, IEEE TPEL 2015"
---

## Definición
Microrred con **dos subredes** —una AC y una DC— unidas por uno o varios **convertidores de
interconexión** (interlink converter, ILC). Combina las ventajas de cada dominio: la DC integra de
forma natural PV, baterías y cargas electrónicas (data centers); la AC conecta a la red y a cargas
rotativas.

## Fundamento teórico
- **Subred DC:** bus de tensión \( V_{dc} \) con fuentes/cargas y reparto por [[droop-dc]]. Su
  estado de carga se refleja en \( V_{dc} \) (ver [[dinamica-bus-dc]]).
- **Subred AC:** bus de frecuencia \( \omega \)/tensión \( V \) con droop AC ([[droop-control]]).
- **Interlink converter (ILC):** un [[convertidor-vsc|VSC]] bidireccional que **transfiere potencia**
  entre ambas y normaliza los indicadores de carga de cada subred. La estrategia autónoma habitual
  iguala los **droop normalizados**:
  $$ P_{ILC}\ \propto\ \frac{\omega-\omega^*}{\Delta\omega_{max}}-\frac{V_{dc}-V_{dc}^*}{\Delta V_{dc,max}} $$
  de modo que cuando una subred está más cargada (su variable de droop más desviada), el ILC le
  envía potencia desde la otra, **repartiendo el estrés** sin comunicaciones.

Modos: **conectado a red** (la red AC fija \( \omega,V \); el ILC regula \( V_{dc} \)) e **isla**
(droop en ambas subredes + balanceo por el ILC). Para data centers IA, la subred DC absorbe la
[[carga-pulsante-datacenter-ia|carga pulsante]] y el dimensionado del bus ([[dinamica-bus-dc]]) y la
estabilidad CPL son críticos.

## Cuándo y por qué se usa
En instalaciones con fuerte componente DC (PV, baterías, cargas electrónicas) y necesidad de
conexión AC: data centers, edificios, buques, microrredes rurales. Reduce etapas de conversión y
mejora eficiencia frente a una arquitectura puramente AC.

## Procedimiento de diseño (genérico)
1. Define topología: nº de buses, ubicación de fuentes/cargas, nº de ILC.
2. Diseña el primario de cada subred (droop AC y [[droop-dc|DC]]).
3. Diseña la estrategia del ILC (igualar droops normalizados) y sus límites de potencia.
4. Coordina con el [[control-jerarquico-microrred|control jerárquico]] (secundario/terciario).
5. Verifica estabilidad del bus DC con cargas CPL/pulsantes y transiciones de modo.

## Ejemplo de código
```python
def ilc_power(w, Vdc, w0, Vdc0, dW_max, dVdc_max, Kp):
    soc_ac = (w - w0)/dW_max            # carga normalizada AC
    soc_dc = (Vdc - Vdc0)/dVdc_max      # carga normalizada DC
    return Kp*(soc_ac - soc_dc)         # potencia a transferir por el ILC
```

## Parámetros y valores típicos
Desviaciones normalizadas de droop ±1 a plena carga. Bus DC 350–800 V (BT). ILC dimensionado al
máximo intercambio esperado entre subredes.

## Errores comunes
- ILC sin normalizar los droops → reparto AC/DC desequilibrado.
- Despreciar la dinámica CPL del bus DC con cargas de data center.
- No definir prioridades de carga ni la transición isla↔red del ILC.

## Conceptos relacionados
- [[convertidor-vsc]] · [[dinamica-bus-dc]] · [[droop-dc]] · [[control-jerarquico-microrred]] · [[carga-pulsante-datacenter-ia]]

## Referencias
- Loh et al., *Autonomous Operation of Hybrid Microgrid With AC and DC Subgrids*, IEEE TPEL 2013.
- Nejabatkhah, Li, *Overview of Power Management Strategies of Hybrid AC/DC Microgrid*, IEEE TPEL 2015.
