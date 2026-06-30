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
fecha_actualizacion: 2026-06-30
relacionados: [impedancia-salida-estabilidad, grid-forming-vs-following, filtro-lcl, impedancia-reactancia]
referencias:
  - "IEEE Std 1204; Kundur, Power System Stability and Control, 1994"
---

## Definición
Modelo de la red vista desde el punto de conexión (PCC) como una fuente ideal detrás de una
impedancia serie \( Z_{red}=R_g+jX_g \). La **fortaleza** se cuantifica con el **SCR**
(short-circuit ratio) y la naturaleza con la relación **X/R**.

<div class="cfig"><img src="figuras/red-thevenin-scr-circuito.png" alt="equivalente Thevenin de la red"><div class="cap">Equivalente Thévenin visto desde el PCC: una fuente ideal Vg detrás de la impedancia serie Rg + jXg. El SCR mide cuán pequeña es esa impedancia frente a la potencia nominal (red fuerte ↔ Z baja).</div></div>

## Fundamento teórico
$$ \mathrm{SCR}=\frac{S_{cc}}{S_n}=\frac{V_{ll}^2}{|Z_{red}|\,S_n},\qquad
   \frac{X}{R}=\frac{X_g}{R_g} $$
Dado SCR y X/R: \( |Z_{red}|=\dfrac{V_{ll}^2}{\mathrm{SCR}\,S_n} \),
\( R_g=\dfrac{|Z_{red}|}{\sqrt{1+(X/R)^2}} \), \( X_g=R_g\,(X/R) \), \( L_g=X_g/\omega_0 \).
En dq, el inductor de red aporta acoplamiento cruzado \( \omega_0 L_g \).

## 1 — De dónde sale la fórmula del SCR
**Paso 1 — potencia de cortocircuito.** El SCR es el cociente entre la potencia de cortocircuito de la red en el PCC, \( S_{cc} \), y la potencia nominal del equipo, \( S_n \). \( S_{cc} \) es la potencia que entregaría la red si se cortocircuitara el PCC: con la fuente ideal \( V_g \) (tensión de línea \( V_{ll} \)) detrás de \( Z_{red} \), un cortocircuito deja toda la tensión sobre \( Z_{red} \), de modo que la corriente de falta es \( I_{cc}=V_{fase}/|Z_{red}| \). En trifásico, la potencia aparente es \( S=\sqrt3\,V_{ll}I_{linea} \), y con \( V_{fase}=V_{ll}/\sqrt3 \):

$$ S_{cc}=\sqrt3\,V_{ll}\,I_{cc}=\sqrt3\,V_{ll}\cdot\frac{V_{ll}/\sqrt3}{|Z_{red}|}=\frac{V_{ll}^2}{|Z_{red}|} $$

(el \( \sqrt3 \) del numerador se cancela con el del denominador de \( V_{fase} \)).

**Paso 2 — normalizar.** Dividiendo entre \( S_n \):

$$ \boxed{\;\mathrm{SCR}=\frac{S_{cc}}{S_n}=\frac{V_{ll}^2}{|Z_{red}|\,S_n}\;} $$

Es un número adimensional: cuántas veces la potencia de falta de la red supera a la del equipo. Red **fuerte** = \( |Z_{red}| \) pequeña = \( S_{cc} \) grande = SCR alto. La red apenas se inmuta ante lo que haga el convertidor.

## 2 — Descomponer (SCR, X/R) en \( R_g \) y \( L_g \)
**Paso 1 — del SCR al módulo.** Despejando \( |Z_{red}| \) de la fórmula del SCR:

$$ |Z_{red}|=\frac{V_{ll}^2}{\mathrm{SCR}\,S_n} $$

**Paso 2 — separar módulo y ángulo.** \( Z_{red}=R_g+jX_g \) tiene módulo \( |Z_{red}|=\sqrt{R_g^2+X_g^2} \). Sacando factor común \( R_g \) y usando \( X/R\equiv X_g/R_g \):

$$ |Z_{red}|=\sqrt{R_g^2+X_g^2}=R_g\sqrt{1+\left(\frac{X_g}{R_g}\right)^2}=R_g\sqrt{1+(X/R)^2} $$

de donde se despeja la parte resistiva, y de ella la reactiva e inductiva:

$$ \boxed{\;R_g=\frac{|Z_{red}|}{\sqrt{1+(X/R)^2}},\qquad X_g=R_g\,(X/R),\qquad L_g=\frac{X_g}{\omega_0}\;} $$

Así, dos números físicamente intuitivos (fortaleza vía SCR, naturaleza vía X/R) se convierten en los dos parámetros \( R_g,L_g \) que entran en el modelo. **Comprobación:** con cualquier \( X/R \), \( \sqrt{R_g^2+X_g^2} \) reconstruye el mismo \( |Z_{red}| \) — el \( X/R \) reparte ese módulo entre resistencia y reactancia sin cambiarlo. El \( L_g \) resultante se suma en serie con \( L_2 \) del filtro (ver [[filtro-lcl]] apartado 8) y aporta el acoplamiento cruzado \( \omega_0 L_g \) en dq.

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
