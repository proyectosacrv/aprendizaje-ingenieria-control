---
titulo: Respuesta en frecuencia de un sistema en espacio de estados
slug: respuesta-frecuencia-ss
categoria: programacion
tipo: metodo
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [calcular Y(s)/Z(s) y Bode desde A,B,C,D]
tags: [espacio-estados, bode, transferencia, frecuencia, numpy]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [linealizacion-numerica, impedancia-salida-estabilidad, medicion-impedancia-inyeccion]
referencias:
  - "Skogestad, Postlethwaite, Multivariable Feedback Control, Wiley 2005"
---

## Definición
Cálculo de la matriz de transferencia \( \mathbf{G}(s)=\mathbf{C}(s\mathbf{I}-\mathbf{A})^{-1}\mathbf{B}+\mathbf{D} \)
evaluada en \( s=j\omega \), a partir del modelo en espacio de estados. Base para Bode,
impedancia y análisis de estabilidad.

## Fundamento teórico
Para cada frecuencia se resuelve un sistema lineal en vez de invertir explícitamente
\( (j\omega\mathbf{I}-\mathbf{A}) \) (más estable numéricamente con `np.linalg.solve`). En MIMO,
\( \mathbf{G}(j\omega) \) es una matriz; la admitancia de salida del convertidor es \( Y=-G \) y
la impedancia \( Z=Y^{-1} \).

## Cuándo y por qué se usa
Para obtener la impedancia analítica del inversor (Fase 2), trazar Bode de lazos, o construir el
*minor loop gain* del criterio de estabilidad por impedancia.

## Procedimiento de diseño (genérico)
1. Parte de \( A,B,C,D \) (de la linealización).
2. Define la malla de frecuencias (logarítmica).
3. Para cada \( \omega \): \( G=C\,(j\omega I-A)^{-1}B+D \) vía `solve`.
4. Deriva lo que necesites: \( Y=-G \), \( Z=Y^{-1} \), magnitud/fase para Bode.

## Ejemplo de código
```python
import numpy as np
def freqresp(A, B, C, D, freqs):
    n = A.shape[0]; I = np.eye(n)
    G = np.zeros((len(freqs), C.shape[0], B.shape[1]), dtype=complex)
    for k, f in enumerate(freqs):
        s = 2j*np.pi*f
        G[k] = C @ np.linalg.solve(s*I - A, B) + D
    return G
```

## Parámetros y valores típicos
Malla logarítmica (p.ej. 0.1 Hz–5 kHz, 300–2000 puntos). Usar `solve`, no `inv`.

## Errores comunes
- Invertir \( (sI-A) \) explícitamente → menos preciso/eficiente que `solve`.
- Malla de frecuencias demasiado gruesa → pierde resonancias agudas.

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: impedancia y estabilidad): `impedance.py` calcula \( Y \) y
  \( Z \) así; `main_phase3.py` lo usa para el Nyquist generalizado.

## Conceptos relacionados
- [[linealizacion-numerica]] · [[impedancia-salida-estabilidad]] · [[medicion-impedancia-inyeccion]]

## Referencias
- Skogestad, Postlethwaite, *Multivariable Feedback Control*, 2005.
