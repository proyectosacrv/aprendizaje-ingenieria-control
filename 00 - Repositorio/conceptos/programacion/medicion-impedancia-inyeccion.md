---
titulo: Medición de impedancia por inyección de perturbación
slug: medicion-impedancia-inyeccion
categoria: programacion
tipo: metodo
nivel: avanzado
proyectos: [01-GFM-Impedance]
objetivos: [medir Z_dq en simulacion/hardware y validar el modelo]
tags: [impedancia, inyeccion, demodulacion, MIMO, validacion, PLECS]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [impedancia-salida-estabilidad, respuesta-frecuencia-ss, modelo-promediado]
referencias:
  - "Roinila et al., Frequency-Response Measurement of Converters, IEEE TPEL"
---

## Definición
Procedimiento para **medir** la impedancia/admitancia dq de un convertidor (en simulación
conmutada, PLECS o hardware) inyectando perturbaciones y analizando la respuesta. Es la
contraparte experimental del cálculo analítico \( Y=C(sI-A)^{-1}B+D \).

## Fundamento teórico
A cada frecuencia \( f_p \) se inyecta una perturbación senoidal de tensión. Como el sistema dq
es **MIMO 2×2**, se necesitan **dos** inyecciones linealmente independientes (eje d y eje q)
para identificar la matriz completa. Con los fasores de tensión \( \mathbf{V} \) y corriente
\( \mathbf{I} \) (columnas = experimentos):
$$ \mathbf{I}=\mathbf{G}\,\mathbf{V}\;\Rightarrow\;\mathbf{G}=\mathbf{I}\,\mathbf{V}^{-1},\qquad
   \mathbf{Y}=-\mathbf{G},\quad \mathbf{Z}=\mathbf{Y}^{-1} $$
Los fasores se extraen por **demodulación** (correlación con sin/cos sobre un número entero de
periodos).

## Cuándo y por qué se usa
Para **validar** el modelo promediado contra la planta conmutada/real, y para caracterizar
convertidores comerciales "caja negra" cuya impedancia no se conoce analíticamente.

## Procedimiento de diseño (genérico)
1. Lleva el sistema al punto de operación.
2. Para cada \( f_p \): inyecta en d (exp.1) y en q (exp.2), pequeña amplitud (pequeña señal).
3. Simula hasta régimen permanente (descarta el transitorio).
4. Demodula \( v,i \) a \( f_p \) (correlación sobre periodos enteros) → fasores.
5. Monta \( \mathbf{G}=\mathbf{I}\,\mathbf{V}^{-1} \), \( Z=(-G)^{-1} \). Repite en frecuencia.
6. Compara con el analítico (debe coincidir en pequeña señal).

## Ejemplo de código
```python
def phasor(t, x, fp):                 # demodulacion sobre periodos enteros
    w = 2*np.pi*fp; T = t[-1]-t[0]
    c = np.trapz(x*np.cos(w*t), t); s = np.trapz(x*np.sin(w*t), t)
    return (2/T)*(c - 1j*s)
# dos inyecciones (d, q) -> columnas de V e I
G = I @ np.linalg.inv(V); Y = -G; Z = np.linalg.inv(Y)
```

## Parámetros y valores típicos
Amplitud pequeña (pequeña señal); ventana de varios periodos tras el asentamiento. Validez solo
mientras no haya saturación (si entra el current limiting, deja de ser lineal).

## Errores comunes
- Una sola inyección en un sistema dq acoplado → no identifica la matriz 2×2.
- Ventana no entera de periodos → fuga espectral en la demodulación.
- Amplitud grande que activa no linealidades → la "impedancia" deja de tener sentido.

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: validar el modelo): la Z medida por inyección coincidió con
  la analítica con **error medio 0.21%**. En `inject.py` / `main_phase4.py`. El mismo código
  procesa datos exportados de PLECS.

## Conceptos relacionados
- [[impedancia-salida-estabilidad]] · [[respuesta-frecuencia-ss]] · [[modelo-promediado]]

## Referencias
- Roinila et al., medición de respuesta en frecuencia de convertidores.
