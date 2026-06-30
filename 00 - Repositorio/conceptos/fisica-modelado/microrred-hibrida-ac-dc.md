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
fecha_actualizacion: 2026-06-30
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

<div class="cfig"><img src="figuras/microrred-hibrida-ac-dc-arquitectura.png" alt="arquitectura de microrred hibrida AC/DC con convertidor de interconexion"><div class="cap">Dos subredes —una AC (bus de frecuencia/tensión, con red y cargas rotativas) y una DC (bus de tensión, con PV, baterías y cargas electrónicas)— unidas por un convertidor de interconexión (ILC) bidireccional. El ILC iguala los droops normalizados de cada subred y transfiere potencia desde la menos cargada hacia la más cargada, repartiendo el estrés sin comunicaciones.</div></div>

## 1 — Balance de potencia a través del ILC y su efecto sobre el bus DC
El ILC no almacena energía (salvo su pequeño condensador): cuanta potencia toma de una subred, la entrega a la otra menos sus pérdidas. Ese balance es lo que liga la dinámica de las dos subredes y, en particular, lo que el bus DC "ve".

**Paso 1 — balance en el ILC.** Sea \( P_{ac} \) la potencia que el ILC toma del lado AC y \( P_{dc} \) la que entrega al lado DC. Con rendimiento \( \eta \) del convertidor (sentido AC→DC):

$$ P_{dc}=\eta\,P_{ac}\qquad(\eta\to1\text{ idealmente}) $$

El ILC es bidireccional: si \( P_{ac}<0 \) la potencia fluye DC→AC. En adelante tomamos \( \eta\approx1 \), de modo que \( P_{dc}\approx P_{ILC} \) es la variable de transferencia.

**Paso 2 — balance de potencia en el nodo del bus DC.** Al bus DC entran la generación local de la subred DC (\( P_{gen,dc} \): PV, batería) y la del ILC; salen las cargas DC (\( P_{load,dc} \)) y lo que acumula el condensador. Por conservación de energía (ver [[dinamica-bus-dc]]):

$$ \frac{dE}{dt}=\underbrace{P_{gen,dc}+P_{ILC}}_{\text{entra}}-\underbrace{P_{load,dc}}_{\text{sale}},\qquad E=\tfrac12 C_{dc}V_{dc}^2 $$

**Paso 3 — condición de bus DC en régimen permanente.** En estado estacionario \( dE/dt=0 \) y \( V_{dc} \) se mantiene, lo que fija la potencia que el ILC debe aportar:

$$ \boxed{\;P_{ILC}=P_{load,dc}-P_{gen,dc}\;} $$

Si la subred DC consume más de lo que genera (déficit), el ILC importa desde el AC; si genera de sobra, exporta. El desbalance instantáneo, mientras el ILC reacciona, lo absorbe el condensador como una excursión de \( V_{dc} \): esa es la señal que la ley de droop normalizado del *Fundamento teórico* usa para pedir más o menos \( P_{ILC} \). De ahí que un déficit en DC se refleje en una caída de \( V_{dc} \) que el ILC compensa transfiriendo potencia desde la subred AC, repartiendo el estrés entre ambas (ver [[carga-pulsante-datacenter-ia]] para el caso del pulso de IA).

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
