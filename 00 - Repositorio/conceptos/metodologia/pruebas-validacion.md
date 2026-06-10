---
titulo: Pruebas de validación (escalón, perturbación, inyección, falta)
slug: pruebas-validacion
categoria: metodologia
tipo: metodo
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [definir que ensayos confirman cada especificacion]
tags: [ensayos, escalon, perturbacion, inyeccion, falta, validacion]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [niveles-validacion, validacion-cruzada, medicion-impedancia-inyeccion, especificaciones-control]
referencias:
  - "Teodorescu et al., Grid Converters for PV and Wind Power Systems, Wiley 2011"
---

## Definición
Catálogo de ensayos que confirman, cada uno, una especificación concreta. La regla: **a cada
especificación, su prueba**.

## Fundamento teórico (ensayos típicos)
- **Escalón de referencia**: mide \( M_p, t_s, e_{ss} \) → desempeño de seguimiento.
- **Escalón de perturbación / carga**: mide el rechazo (caída y recuperación) → robustez del lazo.
- **Barrido / inyección de pequeña señal**: mide la respuesta en frecuencia o la **impedancia**
  (ver [[medicion-impedancia-inyeccion]]) → valida el modelo lineal y la robustez en frecuencia.
- **Falta / hueco de tensión**: gran señal → activa el [[current-limiting]] y prueba la
  supervivencia y la sincronización.
- **Arranque / black-start, cambio de modo**: prueba transitorios de puesta en marcha.
- **Variación paramétrica** (cambiar SCR, potencia): liga con [[robustez-parametrica]].

## Cuándo y por qué se usa
En la fase de validación, en cada nivel de fidelidad. Cada ensayo debe tener un **criterio de
aceptación** derivado de las [[especificaciones-control]].

## Procedimiento (genérico)
1. Por cada especificación, elige el ensayo que la mide.
2. Define el criterio de aceptación numérico (p.ej. \( M_p<10\% \), pico de falta < 1.5 pu).
3. Ejecuta el ensayo en el nivel de fidelidad correspondiente.
4. Registra resultado vs criterio; documenta. Si falla, vuelve a diseño.

## Ejemplo de código
```python
# escalon de potencia + falta (simulacion temporal del modelo no lineal)
pset = lambda t: 5e3 if t < 0.2 else 9e3            # escalon de referencia
efunc = lambda t: (0.3*V0,0) if 0.3<=t<0.42 else (V0,0)  # hueco de tension (falta)
```

## Parámetros y valores típicos
Escalón 50→90% de potencia, hueco al 30% durante ~100 ms, inyección de pequeña señal (amplitud
pequeña), barrido de SCR.

## Errores comunes
- Ensayos sin criterio de aceptación previo → "parece que va bien" subjetivo.
- Probar inyección de impedancia con amplitud que activa saturación (deja de ser pequeña señal).

## Uso en proyectos
- **01 (GFM)**: escalón de potencia (droop vs VSM), falta con current limiting (4.76→1.51 pu),
  inyección de impedancia (error 0.21%).
- **02 (GFL)**: barrido de SCR y de ancho de banda de la PLL.

## Conceptos relacionados
- [[niveles-validacion]] · [[validacion-cruzada]] · [[medicion-impedancia-inyeccion]] · [[current-limiting]]

## Referencias
- Teodorescu et al., *Grid Converters for PV and Wind Power Systems*, 2011.
