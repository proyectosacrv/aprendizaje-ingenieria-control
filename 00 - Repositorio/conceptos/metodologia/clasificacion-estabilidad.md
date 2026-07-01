---
titulo: Clasificación de la estabilidad del sistema de potencia
slug: clasificacion-estabilidad
categoria: metodologia
tipo: concepto
nivel: intermedio
proyectos: []
objetivos: [ubicar cada fenómeno de estabilidad en un marco común y elegir la herramienta]
tags: [estabilidad, clasificacion, converter-driven, frecuencia, tension, angulo, intermedio]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-01
relacionados: [fenomenos-oscilatorios-red, ecuacion-oscilacion, interaccion-pll-red-debil, grid-forming-vs-following]
referencias:
  - "Hatziargyriou et al., Definition and Classification of Power System Stability Revisited & Extended, IEEE TPWRS 2021"
  - "Kundur, Power System Stability and Control, McGraw-Hill 1994"
---

## Definición
Marco taxonómico (IEEE/CIGRE 2021) que organiza **todos** los fenómenos de estabilidad de un
sistema eléctrico según la variable física afectada, la magnitud de la perturbación y la escala de
tiempo. Permite ubicar cada concepto del repositorio y elegir el modelo/criterio adecuado.

## Fundamento teórico
Categorías principales:
- **Estabilidad de ángulo del rotor:** capacidad de las máquinas síncronas de mantener sincronismo.
  Subdivisiones: *pequeña señal* (oscilaciones, [[ecuacion-oscilacion|modo electromecánico]]) y
  *transitoria* (gran perturbación, criterio de áreas iguales).
- **Estabilidad de frecuencia:** equilibrio generación-carga tras un desbalance grande; depende de
  inercia y reservas (FFR, droop). Escala: segundos a minutos.
- **Estabilidad de tensión:** capacidad de mantener tensiones aceptables; *pequeña* y *gran*
  perturbación; ligada a límites de reactiva y colapso de tensión.
- **Estabilidad de resonancia:** intercambio de energía oscilatorio — *eléctrica* (serie, SSR) y
  *electromecánica* (torsional); ver [[fenomenos-oscilatorios-red|oscilaciones subsíncronas]].
- **Estabilidad impulsada por convertidor (converter-driven):** la categoría **nueva** de 2021,
  por la dinámica rápida de la electrónica de potencia. Dos bandas:
  - *Interacción lenta* (< ~10 Hz): PLL en red débil, lazo de potencia/sincronización
    ([[interaccion-pll-red-debil]], GFM vs GFL).
  - *Interacción rápida* (decenas de Hz–kHz): resonancia/[[fenomenos-oscilatorios-red|estabilidad armónica]].

Eje transversal: **pequeña señal** (linealización, autovalores/impedancia) vs **gran perturbación**
(simulación no lineal en el tiempo).

<div class="cfig"><img src="figuras/clasificacion-estabilidad-bandas.png" alt="bandas de frecuencia de los fenomenos de estabilidad"><div class="cap">La frecuencia de la oscilación ubica el fenómeno: modos electromecánicos de ángulo/frecuencia (0.1–2 Hz), interacción converter-driven lenta (PLL en red débil, 1–10 Hz), resonancia SSR/SSCI (5–100 Hz) e interacción rápida / armónica (100 Hz–3 kHz). Cada banda dicta el modelo (electromecánico, fasorial, conmutado), la herramienta y la mitigación.</div></div>

## 1 — Ejemplo cuantitativo: diagnóstico de una oscilación por su frecuencia
**Caso A — oscilación a 3.3 Hz.** En el proyecto GFM, el análisis modal da un modo dominante a \( f=3.3\,\text{Hz} \) con \( \zeta=0.40 \). Por la taxonomía: \( f<10\,\text{Hz} \), origen en el lazo de potencia/droop (converter-driven lento). Herramienta adecuada: modelo lineal dq + autovalores. No es un modo electromecánico (no hay máquina síncrona) ni resonancia armónica (demasiado lenta).

**Caso B — oscilación a 250 Hz.** Si en el modelo conmutado aparece una resonancia a 250 Hz, la taxonomía indica: converter-driven rápido (10 Hz–kHz), posiblemente resonancia del filtro LCL (\( f_{res}=1/(2\pi\sqrt{L_2 C_f})\approx250\,\text{Hz} \) con \( L_2=1.5\,\text{mH} \), \( C_f=270\,\mu\text{F} \)). Herramienta: impedancia dq, criterio Nyquist generalizado. Mitigación: amortiguamiento activo o resistor de damping en el filtro.

**Caso C — colapso de tensión en 2 s.** Oscilación lenta que colapsa en segundos → estabilidad de tensión (no converter-driven). Herramienta: flujo de carga dinámico, margen de reactiva. Modelo adecuado: fasorial lento, no dq de alta frecuencia.

La frecuencia de la oscilación es el primer clasificador; la variable afectada (ángulo, tensión, corriente) y el origen físico (inercia, PLL, filtro) son el segundo nivel de clasificación.

## Cuándo y por qué se usa
Como mapa para diagnosticar: ante una oscilación o colapso, su frecuencia y causa la sitúan en una
categoría, lo que dicta el modelo (electromecánico, fasorial, conmutado), la herramienta (modal,
impedancia, dominio del tiempo) y la mitigación.

## Procedimiento de diseño (genérico)
1. Caracteriza el evento: variable afectada (ángulo/frecuencia/tensión), frecuencia de oscilación,
   tamaño de la perturbación.
2. Ubícalo en la categoría correspondiente.
3. Elige el modelo y el criterio (modal/impedancia/temporal) acorde a la escala.
4. Aplica la mitigación propia de esa categoría.

## Ejemplo de código
```text
f_osc < 1 Hz  ........ ángulo (modo electromecánico) / frecuencia
1–10 Hz ............. converter-driven lento (PLL, red débil)
10 Hz–kHz ........... converter-driven rápido (resonancia/armónica)
```

## Parámetros y valores típicos
Modo electromecánico 0.1–2 Hz; interárea 0.1–0.8 Hz; converter-driven lento 1–10 Hz; armónico
100 Hz–3 kHz; SSR/SSCI 5–100 Hz.

## Errores comunes
- Aplicar modelos electromecánicos (fasor a 50 Hz) a fenómenos converter-driven rápidos.
- Tratar como "estabilidad de tensión" una oscilación que es resonancia de impedancia.
- Olvidar que en sistemas dominados por convertidores la inercia ya no garantiza estabilidad.

## Conceptos relacionados
- [[fenomenos-oscilatorios-red|estabilidad armónica]] · [[ecuacion-oscilacion]] · [[interaccion-pll-red-debil]] · [[grid-forming-vs-following]]

## Referencias
- Hatziargyriou et al., *Definition and Classification of Power System Stability Revisited & Extended*, IEEE TPWRS 2021.
- Kundur, *Power System Stability and Control*, 1994.
