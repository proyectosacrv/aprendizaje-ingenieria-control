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
