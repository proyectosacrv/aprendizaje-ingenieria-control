---
titulo: Red Thévenin, SCR y X/R
slug: red-thevenin-scr
categoria: fisica-modelado
tipo: parametro
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [modelar la fortaleza de la red en el punto de conexion]
tags: [SCR, X/R, thevenin, red-debil, impedancia-red]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [impedancia-salida-estabilidad, grid-forming-vs-following]
referencias:
  - "IEEE Std 1204; Kundur, Power System Stability and Control, 1994"
---

## Definición
Modelo de la red vista desde el punto de conexión (PCC) como una fuente ideal detrás de una
impedancia serie \( Z_{red}=R_g+jX_g \). La **fortaleza** se cuantifica con el **SCR**
(short-circuit ratio) y la naturaleza con la relación **X/R**.

## Fundamento teórico
$$ \mathrm{SCR}=\frac{S_{cc}}{S_n}=\frac{V_{ll}^2}{|Z_{red}|\,S_n},\qquad
   \frac{X}{R}=\frac{X_g}{R_g} $$
Dado SCR y X/R: \( |Z_{red}|=\dfrac{V_{ll}^2}{\mathrm{SCR}\,S_n} \),
\( R_g=\dfrac{|Z_{red}|}{\sqrt{1+(X/R)^2}} \), \( X_g=R_g\,(X/R) \), \( L_g=X_g/\omega_0 \).
En dq, el inductor de red aporta acoplamiento cruzado \( \omega_0 L_g \).

## Cuándo y por qué se usa
Para evaluar la estabilidad del inversor según la fortaleza de la red (Fase 3). Red **fuerte**:
SCR alto, \( Z_{red} \) baja. Red **débil**: SCR bajo, \( Z_{red} \) alta.

## Procedimiento de diseño (genérico)
1. Define el rango de SCR de interés (p.ej. 1–20) y el X/R (2–10 en transmisión).
2. Convierte (SCR, X/R) → \( R_g, L_g \) con las fórmulas de arriba.
3. Úsalo como impedancia de red en el criterio de impedancia o como inductor serie en el modelo
   acoplado (en serie con \( L_2 \)).

## Ejemplo de código
```python
def grid_params(scr, xr, Vll, Sn, w0):
    Z = Vll**2/(scr*Sn)
    Rg = Z/np.sqrt(1+xr**2); Lg = Rg*xr/w0
    return Rg, Lg
```

## Parámetros y valores típicos
SCR: fuerte >10, normal 3–10, débil <3. X/R: 1 (distribución) a 10+ (transmisión).

## Errores comunes
- Confundir SCR con la potencia de cortocircuito absoluta.
- Olvidar el término cruzado \( \omega_0 L_g \) al pasar la red a dq.

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: fortaleza de red): se barrió el SCR para hallar el crítico.
  La red en serie con \( L_2 \) permitió validar el criterio de impedancia. En `grid.py`.

## Conceptos relacionados
- [[impedancia-salida-estabilidad]] · [[grid-forming-vs-following]]

## Referencias
- Kundur, 1994; IEEE Std 1204.
