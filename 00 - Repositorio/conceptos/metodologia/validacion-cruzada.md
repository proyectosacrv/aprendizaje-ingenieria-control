---
titulo: Validación cruzada (coincidencia entre niveles/métodos)
slug: validacion-cruzada
categoria: metodologia
tipo: metodo
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [confirmar un resultado por dos vias independientes]
tags: [validacion, cruzada, consistencia, modelo, confianza]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [niveles-validacion, pruebas-validacion, impedancia-salida-estabilidad, medicion-impedancia-inyeccion]
referencias:
  - "buena praxis de modelado y verificación (V&V)"
---

## Definición
Confirmar un mismo resultado por **dos caminos independientes** (dos modelos, dos métodos, o dos
niveles de fidelidad). Si coinciden, la confianza en ambos sube; si no, hay un error que localizar.

## Fundamento teórico
La validación cruzada es la forma práctica de "verificación y validación" (V&V):
- **Entre métodos**: el mismo resultado por dos teorías distintas (p.ej. SCR crítico por
  autovalores del modelo acoplado **y** por Nyquist de impedancia).
- **Entre niveles**: lineal ↔ medición por inyección; promediado ↔ conmutado; simulación ↔ HIL.
- Un desacuerdo acota el error: si dos métodos discrepan, el fallo está en uno de los dos (o en la
  hipótesis común), y se investiga.

<div class="cfig"><img src="figuras/validacion-cruzada-scr.png" alt="SCR critico por dos metodos independientes en GFM y GFL"><div class="cap">El SCR crítico calculado por dos vías independientes —autovalores del modelo acoplado y Nyquist del cociente de impedancias— coincide en ambos proyectos con menos del 2 % de diferencia. Ese acuerdo convierte "el modelo dice que es estable" en confianza real; un desacuerdo, en cambio, acotaría dónde está el error.</div></div>

## Cuándo y por qué se usa
Siempre que sea posible. Es lo que convierte "el modelo dice que es estable" en "estoy seguro de
que es estable". Especialmente valioso antes de hardware.

## Procedimiento (genérico)
1. Elige dos vías independientes para la misma magnitud.
2. Calcula por ambas y compara (error relativo).
3. Si coinciden (p.ej. <5%), valida; documenta el acuerdo.
4. Si no, localiza la discrepancia (hipótesis, signo, implementación) y corrige.

## Ejemplo de código
```python
scr_acoplado = biseccion(maxre_modelo_acoplado)   # via A: autovalores
scr_impedancia = nyquist_critico(Zred, Yinv)      # via B: criterio de impedancia
err = abs(scr_acoplado - scr_impedancia)/scr_acoplado
assert err < 0.05, "las dos vias no coinciden -> revisar"
```

## Parámetros y valores típicos
Acuerdo aceptable < 5% entre métodos lineales; entre niveles distintos, esperar discrepancias en
las bandas donde el nivel superior añade física (conmutación cerca de \( f_{sw}/2 \)).

## Errores comunes
- Dos vías que en realidad comparten la misma hipótesis (no son independientes) → falso acuerdo.
- Atribuir toda la discrepancia al nivel superior sin revisar el inferior.

## Uso en proyectos
- **01 (GFM)**: SCR crítico 3.35 (acoplado) vs 3.39 (impedancia) → 1.3%.
- **02 (GFL)**: 3.48 (acoplado) vs 3.55 (impedancia) → 2%. Y la impedancia medida por inyección
  coincidió con la analítica (0.21%).

## Conceptos relacionados
- [[niveles-validacion]] · [[pruebas-validacion]] · [[impedancia-salida-estabilidad]] · [[medicion-impedancia-inyeccion]]

## Referencias
- Buena praxis de V&V en modelado.
