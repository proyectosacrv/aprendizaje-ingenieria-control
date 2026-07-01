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
fecha_actualizacion: 2026-07-01
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

<div class="cfig"><img src="figuras/respuesta-frecuencia-ss-bode.png" alt="Bode de magnitud y fase calculado desde el espacio de estados"><div class="cap">Bode obtenido directamente del modelo en espacio de estados: para cada frecuencia se resuelve $G(j\omega)=C(j\omega I-A)^{-1}B+D$ con <code>np.linalg.solve</code> (más estable que invertir). De aquí salen la impedancia analítica $Y=-G$, $Z=Y^{-1}$ y el minor loop gain del criterio por impedancia. La malla logarítmica debe ser fina para no perder resonancias agudas.</div></div>

## 1 — De las matrices \( A,B,C,D \) a \( G(j\omega) \): derivación y ejemplo numérico
**Paso 1 — origen de la fórmula.** En espacio de estados, con entrada \( u(t) \) y salida \( y(t)=C\,x+D\,u \), tomando la transformada de Laplace con condiciones iniciales nulas:

$$ s\,X(s) = A\,X(s) + B\,U(s) \;\Rightarrow\; (sI-A)\,X(s) = B\,U(s) \;\Rightarrow\; X(s)=(sI-A)^{-1}B\,U(s) $$

Sustituyendo en la salida:

$$ Y(s) = \bigl[C(sI-A)^{-1}B + D\bigr]\,U(s) = \mathbf{G}(s)\,U(s) $$

Evaluar en \( s=j\omega \) da la respuesta en frecuencia: \( \mathbf{G}(j\omega)=C(j\omega I-A)^{-1}B+D \).

**Paso 2 — ejemplo numérico \( 2\times2 \).** Sistema RL acoplado en dq: \( \dot{i}_d=-(R/L)\,i_d+\omega_0\,i_q+v_d/L \), \( \dot{i}_q=-(R/L)\,i_q-\omega_0\,i_d+v_q/L \). Con \( R/L=50 \), \( \omega_0=314 \):

$$ A=\begin{bmatrix}-50 & 314 \\ -314 & -50\end{bmatrix},\quad B=\frac{1}{L}I_{2\times2},\quad C=I_{2\times2},\quad D=0 $$

A \( f=50\,\text{Hz} \) (\( \omega=314 \) rad/s):

$$ j\omega I - A = \begin{bmatrix}j314+50 & -314 \\ 314 & j314+50\end{bmatrix} $$

$$ \det = (50+j314)^2 + 314^2 = 2500 - 98596 + j\cdot2\times50\times314 + 314^2 = 314^2(j^2-1)+j31400+2500+314^2 $$

Al invertir y multiplicar por \( B,C \) se obtiene la admitancia \( Y(j\omega) \) que muestra el acoplamiento d-q: la excitación en el eje d produce respuesta tanto en d como en q (términos fuera de la diagonal de la matriz \( 2\times2 \)).

**Paso 3 — por qué usar `solve` en vez de `inv`.** Calcular \( (j\omega I-A)^{-1}B \) como \( [(j\omega I-A)^{-1}]\cdot B \) requiere invertir la matriz; numéricamente equivale a resolver \( n \) sistemas lineales. `np.linalg.solve(sI-A, B)` lo hace directamente con factorización LU, con mejor estabilidad numérica (condicionamiento similar, pero evita la amplificación de errores al multiplicar la inversa completa).

$$ \boxed{\mathbf{G}(j\omega)=C\,(j\omega I-A)^{-1}B+D\;\equiv\;\text{FDT evaluada en }s=j\omega} $$

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
