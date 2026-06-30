---
titulo: Sistema fotovoltaico y MPPT
slug: fotovoltaica-mppt
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: []
objetivos: [modelar la célula PV y extraer la máxima potencia con MPPT]
tags: [pv, fotovoltaica, mppt, p-and-o, inc-cond, curva-iv, intermedio, modelado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-30
relacionados: [modelo-bateria-bess, convertidor-vsc, dinamica-bus-dc, control-tension-bus-dc, sistema-por-unidad]
referencias:
  - "Sera et al., PV Panel Model Based on Datasheet Values, IEEE ISIE 2007"
  - "Esram, Chapman, Comparison of Photovoltaic Array MPPT Techniques, IEEE TEC 2007"
---

## Definición
Modelo eléctrico de la célula/módulo fotovoltaico (curva I-V no lineal) y algoritmos de
**Maximum Power Point Tracking (MPPT)** que ajustan el punto de operación para extraer la máxima
potencia disponible ante variaciones de irradiancia y temperatura.

## Fundamento teórico
**Modelo de diodo único:**
$$ I = I_{ph} - I_0\left(\exp\!\frac{V+IR_s}{nV_T}-1\right) - \frac{V+IR_s}{R_{sh}} $$
con \( V_T=kT/q \) (tensión térmica, \( \approx26 \) mV a 25 °C), \( n \) factor de idealidad,
\( I_{ph} \) fotocorriente (proporcional a irradiancia G), \( I_0 \) corriente de saturación inversa
(fuertemente dependiente de T). La curva I-V tiene:
- **Isc** (cortocircuito, \( V=0 \)): corriente máxima ≈ \( I_{ph} \).
- **Voc** (circuito abierto, \( I=0 \)): tensión máxima.
- **MPP** (máxima potencia): punto de tangente \( dP/dV=0 \); típicamente 70–80 % de \( V_{oc} \).

<div class="cfig"><img src="figuras/fotovoltaica-mppt-iv.png" alt="curva I-V y P-V de un modulo PV"><div class="cap">La curva I-V del PV (azul) es no lineal; la potencia P=V·I (rojo) tiene un máximo único, el MPP (~76 % de Voc), que el MPPT persigue ante cambios de irradiancia y temperatura.</div></div>

La irradiancia eleva \( I_{ph}\sim G \); la temperatura sube \( V_{oc} \) cae (\( -2.3 \) mV/°C
por célula).

**MPPT — algoritmos:**
- **Perturba y observa (P&O):** incrementa/decrementa la tensión de referencia y compara \( P \) con
  el ciclo anterior. Simple; oscila alrededor del MPP en régimen permanente (amplitud \( \propto \Delta V_{step} \)).
- **Conductancia incremental (INC):** condición exacta del MPP: \( dI/dV=-I/V \) (la conductancia
  incremental iguala la conductancia instantánea). Sin oscilación en permanente; más costoso.
- **MPPT por tensión constante (Voc fracción):** \( V_{MPP}\approx0.76 V_{oc} \). Muy simple, no
  requiere medida de corriente; impreciso ante sombreado.
- **MPP global con sombreado parcial:** la curva P-V tiene **múltiples máximos locales** (bypass
  diodes); P&O/INC quedan atrapados. Se requieren técnicas globales (barrido periódico, PSO).

**Integración al convertidor:** el MPPT genera la referencia de tensión DC \( V^*_{dc} \) (o de
corriente). Un boost DC/DC intermedio adapta la tensión del string al bus DC; el VSC controla el bus
DC hacia la red ([[control-tension-bus-dc]]).

## 1 — La condición \( dP/dV=0 \) del MPP y por qué INC usa \( dI/dV=-I/V \)
El MPP es, por definición, el punto donde la potencia entregada es máxima. Como la potencia es \( P=V\,I \) con \( I=I(V) \) dado por la curva no lineal, "máximo" significa derivada nula. De ahí sale la condición exacta que usa el algoritmo de conductancia incremental.

**Paso 1 — escribir la potencia y derivar (regla del producto).** Con \( P(V)=V\cdot I(V) \):

$$ \frac{dP}{dV}=\frac{d(V\,I)}{dV}=I+V\,\frac{dI}{dV} $$

(el primer término es la derivada de \( V \) por \( I \); el segundo, \( V \) por la derivada de \( I \)).

**Paso 2 — imponer máximo.** En el MPP la potencia no crece ni decrece: \( dP/dV=0 \). Igualando a cero el Paso 1:

$$ I+V\,\frac{dI}{dV}=0 $$

**Paso 3 — despejar la condición de conductancia incremental.** Pasando \( I \) al otro lado y dividiendo por \( V \):

$$ \boxed{\;\frac{dI}{dV}=-\frac{I}{V}\;} $$

Lectura: la **conductancia incremental** \( dI/dV \) (pendiente local de la curva I-V) iguala en magnitud a la **conductancia instantánea** \( I/V \), con signo opuesto. El signo de \( dP/dV=I+V\,dI/dV \) dice de qué lado del MPP estamos:

$$ \frac{dI}{dV}>-\frac{I}{V}\Rightarrow\text{a la izquierda del MPP (subir }V),\qquad \frac{dI}{dV}<-\frac{I}{V}\Rightarrow\text{a la derecha (bajar }V) $$

Eso es exactamente lo que decide el algoritmo INC, y por ser una condición **exacta** no oscila en permanente (a diferencia de P&O, que necesita perturbar para "ver" la pendiente).

## 2 — Por qué P&O converge: el signo de \( \Delta P/\Delta V \)
P&O no calcula derivadas: las **estima** perturbando \( V \) y mirando cómo cambió \( P \). El truco es que el signo de \( dP/dV \) cambia justo en el MPP, y eso basta para decidir hacia dónde moverse.

**Paso 1 — la pendiente cambia de signo en el MPP.** De la curva P-V (un único máximo en condiciones uniformes):

$$ \frac{dP}{dV}>0 \text{ a la izquierda del MPP},\qquad \frac{dP}{dV}<0 \text{ a la derecha} $$

**Paso 2 — aproximar la pendiente por incrementos.** Entre dos pasos de control con perturbación \( \Delta V=V_k-V_{k-1} \) y respuesta \( \Delta P=P_k-P_{k-1} \):

$$ \frac{dP}{dV}\approx\frac{\Delta P}{\Delta V} $$

**Paso 3 — regla de decisión.** Para subir por la curva hacia el máximo hay que moverse en el sentido en que \( P \) aumenta. Combinando los signos de \( \Delta P \) y \( \Delta V \):

$$ \boxed{\;V_{k+1}=V_k+\Delta V_{step}\cdot\operatorname{sign}(\Delta P)\cdot\operatorname{sign}(\Delta V)\;} $$

Si la última perturbación subió la potencia (\( \Delta P>0 \)), se repite el mismo sentido de \( \Delta V \); si la bajó (\( \Delta P<0 \)), se invierte. Por eso, en permanente, P&O **oscila** en torno al MPP con amplitud \( \propto\Delta V_{step} \): nunca se queda quieto porque necesita perturbar para medir. Es justo la regla del bloque de código de la ficha (las cuatro ramas son las cuatro combinaciones de signos). Con sombreado parcial la curva tiene varios máximos y esta regla local queda atrapada en uno: ahí hace falta búsqueda global.

## Cuándo y por qué se usa
En toda instalación PV conectada a red o a microrred. El MPPT es la capa de control más exterior
(más lenta, decenas de ms) sobre el lazo de tensión/corriente del DC/DC.

## Procedimiento de diseño (genérico)
1. Parametriza el modelo de diodo único con los datos de la hoja (Isc, Voc, Impp, Vmpp a STC).
2. Elige el algoritmo MPPT (P&O para simplicidad; INC para menos rizado; global si hay sombreado).
3. Sintoniza el paso \( \Delta V \) (P&O): pequeño → poco rizado, respuesta lenta; grande → rápido, mucho rizado.
4. Conecta el MPPT al lazo de tensión del DC/DC; separa bandas (MPPT \( \ll \) lazo de tensión).
5. Verifica comportamiento con irradiancia variable y sombreado parcial.

## Ejemplo de código
```python
def mppt_po(V_ref, P_now, P_prev, V_prev, dV=0.5):
    if P_now >= P_prev:
        return V_ref + dV if V_ref >= V_prev else V_ref - dV
    else:
        return V_ref - dV if V_ref >= V_prev else V_ref + dV
```

## Parámetros y valores típicos
Paso P&O \( \Delta V \) 0.5–2 V; periodo MPPT 10–100 ms. \( V_{MPP}/V_{oc}\approx0.76 \);
\( I_{MPP}/I_{sc}\approx0.92 \). Eficiencia MPPT > 99 % en condiciones uniformes.

## Errores comunes
- Paso \( \Delta V \) grande en P&O → rizado permanente significativo en potencia.
- Usar P&O simple con sombreado parcial → queda en máximo local (pérdidas de hasta 30–50 %).
- MPPT más rápido que el lazo de tensión del convertidor → interacción y oscilación.

## Conceptos relacionados
- [[convertidor-vsc]] · [[dinamica-bus-dc]] · [[control-tension-bus-dc]] · [[modelo-bateria-bess]] · [[sistema-por-unidad]]

## Referencias
- Sera et al., *PV Panel Model Based on Datasheet Values*, IEEE ISIE 2007.
- Esram, Chapman, *Comparison of PV Array MPPT Techniques*, IEEE TEC 2007.
