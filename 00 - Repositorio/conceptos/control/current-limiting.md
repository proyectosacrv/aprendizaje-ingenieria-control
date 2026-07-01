---
titulo: Current limiting (limitación de corriente en grid-forming)
slug: current-limiting
categoria: control
tipo: tecnica
nivel: avanzado
proyectos: [01-GFM-Impedance]
objetivos: [proteger los semiconductores ante faltas]
tags: [falta, saturacion, anti-windup, proteccion, gran-señal]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [control-cascada, impedancia-virtual, vsm-inercia]
referencias:
  - "Paquette, Divan, Virtual Impedance Current Limiting for Inverters in Microgrids, IEEE TIA 2015"
---

## Definición
Mecanismo que acota la corriente del inversor ante perturbaciones grandes (faltas). Crítico en
grid-forming porque, al ser **fuente de tensión**, ante un hueco de red inyectaría una corriente
enorme que destruiría los semiconductores.

## Fundamento teórico
La forma más directa: **saturar la magnitud** de la referencia de corriente del lazo interno a
\( I_{max} \), con **anti-windup** para no cargar los integradores del lazo de tensión:

$$ \lVert \mathbf{i}_{L1}^{*}\rVert \le I_{max} \;\Rightarrow\;
   \mathbf{i}_{L1}^{*}\leftarrow I_{max}\,\frac{\mathbf{i}_{L1}^{*}}{\lVert\mathbf{i}_{L1}^{*}\rVert} $$

Es un fenómeno de **gran señal**: rompe la linealidad, por lo que el análisis de impedancia/
estabilidad lineal deja de aplicar y se estudia por simulación temporal.

<div class="cfig"><img src="figuras/current-limiting-falta.png" alt="corriente en falta con y sin limite"><div class="cap">Ante un hueco de red, un grid-forming sin límite inyecta una corriente de falta enorme (≈4.76 pu) que destruiría los semiconductores; la saturación de la magnitud de la referencia la acota a $I_{max}$≈1.5 pu. Es un fenómeno de gran señal: rompe la linealidad y se estudia por simulación temporal.</div></div>

## 1 — El clamping del módulo \( \sqrt{i_d^2+i_q^2} \): por qué por magnitud y no por eje
**Paso 1 — la corriente trifásica como un fasor en dq.** Un sistema trifásico equilibrado de corriente se representa en el marco \( dq \) por dos componentes \( (i_d,i_q) \). Estas no son dos corrientes independientes: son las proyecciones de un único vector cuyo **módulo** es la amplitud de pico de la corriente de fase y cuyo argumento es su fase:

$$ I=\lVert\mathbf{i}\rVert=\sqrt{i_d^2+i_q^2},\qquad \varphi=\arctan\frac{i_q}{i_d} $$

Lo que daña los semiconductores es la **amplitud de pico por fase**, es decir, exactamente este módulo. La restricción física es por tanto \( \sqrt{i_d^{*2}+i_q^{*2}}\le I_{max} \), una circunferencia de radio \( I_{max} \) en el plano \( (d,q) \).

**Paso 2 — proyectar de vuelta sobre el círculo.** Cuando la referencia que pide el lazo de tensión cae fuera del círculo (\( \lVert\mathbf{i}^*\rVert>I_{max} \)), hay que devolverla al borde conservando su dirección (su fase). El punto del círculo más cercano en dirección es el del mismo ángulo: se escala el vector por el factor

$$ s=\frac{I_{max}}{\lVert\mathbf{i}^*\rVert}=\frac{I_{max}}{\sqrt{i_d^{*2}+i_q^{*2}}}\le1 $$

$$ \boxed{\;\mathbf{i}^*\leftarrow s\,\mathbf{i}^*=I_{max}\,\frac{\mathbf{i}^*}{\lVert\mathbf{i}^*\rVert}\;} $$

**Paso 3 — comprobar que preserva la fase.** Tras escalar, \( i_d^*\!\leftarrow\!s\,i_d^* \), \( i_q^*\!\leftarrow\!s\,i_q^* \). El nuevo argumento es \( \arctan\dfrac{s\,i_q^*}{s\,i_d^*}=\arctan\dfrac{i_q^*}{i_d^*}=\varphi \): **idéntico**. El nuevo módulo es \( s\,\lVert\mathbf{i}^*\rVert=I_{max} \). La corriente queda en \( I_{max} \) con la misma fase: misma relación P/Q, solo más pequeña.

**Paso 4 — por qué NO saturar cada eje por separado.** Si se hiciera \( i_d^*\!\leftarrow\!\text{sat}(i_d^*,I_{max}) \) e \( i_q^*\!\leftarrow\!\text{sat}(i_q^*,I_{max}) \) de forma independiente, el límite efectivo sería un **cuadrado** \( [-I_{max},I_{max}]^2 \), no un círculo. Dos problemas: (a) en la esquina la magnitud llega a \( \sqrt2\,I_{max} \), un 41 % por encima del límite real; (b) saturar un eje y no el otro **cambia el ángulo** \( \varphi \) (cada eje se recorta en distinta proporción), distorsionando la fase de la corriente —y con ella el reparto P/Q justo en plena falta—. Por eso se satura la magnitud y se reescalan ambos ejes con el mismo \( s \).

**Paso 5 — anti-windup acoplado.** Mientras \( s<1 \), la referencia entregada es menor que la que pide el PI de tensión; su integrador seguiría acumulando error (windup). Por eso, durante la saturación se congelan/recortan los integradores del lazo externo (ver código), de modo que al despejar la falta no haya un sobreimpulso por el término integral cargado.

## Cuándo y por qué se usa
Siempre en convertidores reales. El reto abierto en grid-forming: limitar **sin** perder el
carácter formador ni la sincronización (un límite duro puede hacer que el inversor "siga" la
falta como GFL y pierda estabilidad de ángulo).

## Procedimiento de diseño (genérico)
1. Fija \( I_{max} \) (típico 1.1–1.5 pu de la corriente nominal de pico).
2. Implementa la saturación de la **magnitud** del fasor de referencia (no por eje, para no
   distorsionar la fase).
3. Añade **anti-windup**: congela/recorta los integradores del lazo externo mientras satura.
4. Considera variantes que preservan el comportamiento formador: **impedancia virtual
   adaptativa** (sube \( Z_v \) en falta) o limitación con prioridad de eje d/q.

## Ejemplo de código
```python
mag = np.hypot(iL1ref_d, iL1ref_q)
if mag > Imax:
    s = Imax/mag
    iL1ref_d *= s; iL1ref_q *= s
    dxv_d = dxv_q = 0.0          # anti-windup: congela integradores de tension
```

## Parámetros y valores típicos
\( I_{max} \) = 1.1–1.5 pu. En el proyecto, 1.5 pu (≈30.6 A frente a \( I_n=20.4 \) A).

## Errores comunes
- Saturar por eje en vez de por magnitud → distorsiona la fase de la corriente.
- Olvidar el anti-windup → al salir de la falta hay un transitorio grande (windup).
- Analizar la falta con impedancia lineal → no aplica; usar simulación de gran señal.

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: protección): ante un hueco al 30%, sin límite la corriente
  llegaba a **4.76 pu**; con el límite quedó en **1.51 pu**. En `simulate.py` / `main_phase5.py`.

## Conceptos relacionados
- [[control-cascada]] · [[impedancia-virtual]] · [[vsm-inercia]]

## Referencias
- Paquette, Divan, IEEE TIA 2015.
