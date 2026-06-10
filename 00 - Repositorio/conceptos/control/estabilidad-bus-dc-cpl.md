---
titulo: Estabilidad de bus DC con cargas CPL
slug: estabilidad-bus-dc-cpl
categoria: control
tipo: fenomeno
nivel: avanzado
proyectos: [03-DataCenter-IA]
objetivos: [predecir y evitar la inestabilidad de un bus DC con cargas de potencia constante]
tags: [bus-dc, CPL, estabilidad, microrred-dc, amortiguamiento, datacenter]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [carga-potencia-constante-cpl, criterio-middlebrook, no-pasividad-resistencia-negativa, robustez-parametrica]
referencias:
  - "Riccobono, Santi, Comprehensive Review of Stability Criteria for DC Power Systems, IEEE TIA 2014"
---

## Definición
Estudio de cuándo un bus DC alimentado a través de un filtro L-C y cargado con una
[[carga-potencia-constante-cpl|CPL]] permanece estable. La resistencia incremental negativa de la
CPL puede desamortiguar el filtro y provocar oscilaciones del bus.

## Fundamento teórico
Para un filtro \( L_f, R_f \) que alimenta un condensador \( C_{dc} \) con una CPL de potencia
\( P \), el modelo linealizado tiene matriz
$$ A=\begin{bmatrix} -R_f/L_f & -1/L_f \\ 1/C_{dc} & \tfrac{P}{V^2 C_{dc}} \end{bmatrix} $$
El término \( P/(V^2 C_{dc}) \) (de la CPL) es **positivo** en la diagonal: reduce el
amortiguamiento. La traza se hace positiva (inestable) cuando
$$ P > P_{crit} = \frac{V^2 R_f C_{dc}}{L_f} $$
Es decir: más potencia, menos resistencia o menos condensador → inestable. Soluciones:
- **Amortiguamiento pasivo**: aumentar \( R \) (disipa) o rama R-C de damping.
- **Más capacidad de bus** \( C_{dc} \) (sube \( P_{crit} \)).
- **Amortiguamiento activo**: el convertidor fuente emula resistencia sin pérdidas.
- **Impedance shaping** y verificación por [[criterio-middlebrook]].

## Cuándo y por qué se usa
En toda microrred DC con cargas reguladas: data centers, vehículos eléctricos, naval, aeronáutica.
Es el análogo DC de la inestabilidad por impedancia que en AC vimos en el grid-following.

## Procedimiento (genérico)
1. Modela el bus (L-C) y la CPL (resistencia incremental \( -V^2/P \)).
2. Calcula \( P_{crit}=V^2 R C/L \) y compáralo con el rango de carga.
3. Verifica por autovalores y por impedancia ([[criterio-middlebrook]]).
4. Si \( P_{op} \) se acerca a \( P_{crit} \): aumenta \( C_{dc} \) o añade amortiguamiento.

## Ejemplo de código
```python
A = np.array([[-Rf/Lf, -1/Lf],
              [ 1/Cdc,  P/(V**2*Cdc)]])     # el termino CPL resta amortiguamiento
estable = np.all(np.linalg.eigvals(A).real < 0)
P_crit = V**2 * Rf * Cdc / Lf
```

## Parámetros y valores típicos
Margen recomendado: operar con \( P_{op} \) bastante por debajo de \( P_{crit} \) (factor 2 o
más), porque \( P_{crit} \) depende de parámetros inciertos (resistencia de cable, etc.).

## Errores comunes
- Confiar solo en el amortiguamiento resistivo natural del cable (pequeño) → \( P_{crit} \) baja.
- No dejar margen: \( P_{crit} \) varía con la temperatura/longitud de cable.

## Uso en proyectos
- **03 - DataCenter-IA**: \( P_{crit}\approx 128 \) kW para el filtro de distribución; validado por
  autovalores y por Middlebrook (134 kW). El condensador del rack \( C_{dc} \) se dimensiona por
  el pico de carga.

## Conceptos relacionados
- [[carga-potencia-constante-cpl]] · [[criterio-middlebrook]] · [[no-pasividad-resistencia-negativa]] · [[robustez-parametrica]]

## Referencias
- Riccobono, Santi, *Review of Stability Criteria for DC Power Systems*, IEEE TIA 2014.
