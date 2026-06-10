---
titulo: Hardware-in-the-loop (HIL y PHIL)
slug: hil-phil
categoria: programacion
tipo: metodo
nivel: intermedio
proyectos: []
objetivos: [validar control y hardware contra un modelo de planta en tiempo real]
tags: [hil, phil, tiempo-real, validacion, simulacion, fpga, intermedio, programacion]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-09
relacionados: [niveles-validacion, simulacion-conmutada, discretizacion-controladores, pruebas-validacion, medicion-impedancia-inyeccion]
referencias:
  - "Bélanger, Venne, Paquin, The What, Where and Why of Real-Time Simulation, IEEE PES 2010"
  - "Lauss et al., Characteristics and Design of Power Hardware-in-the-Loop Simulations, IEEE TIE 2016"
---

## Definición
Técnica de validación en la que un **modelo de planta** se ejecuta en un simulador de **tiempo real**
y se conecta al sistema bajo prueba. En **HIL** se prueba el **controlador real** (señales de bajo
nivel); en **PHIL** (power HIL) se conecta **hardware de potencia real** mediante un amplificador,
intercambiando potencia con la planta simulada.

## Fundamento teórico
- **Tiempo real:** el solver debe completar cada paso \( \Delta t \) **antes** del siguiente tick
  (sin *overruns*). Modelos de convertidor exigen \( \Delta t \) de µs → se usan FPGA para la
  conmutación y CPU para la red.
- **HIL (control):** el simulador emula la planta (sensores → controlador → PWM de vuelta). Valida
  firmware, protecciones, lógica de fallo y secuencias sin riesgo ni hardware de potencia.
- **PHIL (potencia):** se cierra un lazo **físico** de potencia. El acoplamiento entre la planta
  simulada y el equipo real introduce un lazo con retardo del amplificador y del paso de cálculo →
  problemas de **estabilidad y exactitud**. El método de interfaz (Interface Algorithm) más común,
  *Ideal Transformer Model* (ITM), es estable si
  $$ \left|\frac{Z_{HW}}{Z_{sim}}\right|<1\ \text{(en la región crítica)} $$
  es decir, depende del cociente de impedancias real/simulada (mismo espíritu que el
  [[medicion-impedancia-inyeccion|criterio de impedancia]]); se estabiliza con filtros/compensación
  en la interfaz.

Encaja en la pirámide de [[niveles-validacion]]: modelo offline → HIL de control → PHIL → campo.

## Cuándo y por qué se usa
Para validar el control diseñado (sobre [[simulacion-conmutada|modelo conmutado]]) en condiciones
realistas y peligrosas (faltas, huecos, pérdida de red) antes de hardware; certificación de grid
codes; y prueba de equipos de potencia reales contra redes/cargas difíciles de montar físicamente.

## Procedimiento de diseño (genérico)
1. Discretiza el modelo de planta para tiempo real ([[discretizacion-controladores]]); reparte
   CPU/FPGA según constantes de tiempo.
2. Verifica ausencia de *overruns* y la fidelidad frente al modelo offline.
3. HIL: conecta el controlador real; prueba protecciones, fallos y grid codes.
4. PHIL (si aplica): elige Interface Algorithm, comprueba estabilidad (cociente de impedancias),
   añade compensación/filtros.
5. Documenta cobertura y discrepancias ([[pruebas-validacion]]).

## Ejemplo de código
```python
# Lazo de tiempo real (pseudocodigo): respetar el deadline dt
while running:
    t0 = now()
    y = plant_model.step(u, dt)          # planta en tiempo real
    u = controller.step(y)               # HIL: controlador real
    assert now() - t0 < dt               # sin overrun
    wait_until(t0 + dt)
```

## Parámetros y valores típicos
Paso de tiempo: 0.5–2 µs (FPGA, conmutación), 10–50 µs (CPU, red). Latencia de amplificador PHIL
decenas de µs. Objetivo: 0 overruns y error vs offline < pocos %.

## Errores comunes
- *Overruns* no detectados → resultados sin sentido (el "tiempo real" deja de serlo).
- PHIL sin analizar estabilidad de la interfaz (cociente de impedancias) → oscilación o daño.
- Validar solo en nominal y no los casos límite (faltas, pérdida de red) que justifican el HIL.

## Conceptos relacionados
- [[niveles-validacion]] · [[simulacion-conmutada]] · [[discretizacion-controladores]] · [[pruebas-validacion]] · [[medicion-impedancia-inyeccion]]

## Referencias
- Bélanger, Venne, Paquin, *The What, Where and Why of Real-Time Simulation*, IEEE PES 2010.
- Lauss et al., *Characteristics and Design of Power Hardware-in-the-Loop Simulations*, IEEE TIE 2016.
