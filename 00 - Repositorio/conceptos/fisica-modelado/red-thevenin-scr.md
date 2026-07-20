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

## 3 — Equivalente de Thévenin de la red eléctrica

La red vista desde el PCC se modela como \( V_{th} \) en serie con \( Z_{th}=R_{th}+jX_{th} \).
\( Z_{th} \) es la impedancia de Thévenin, inversamente proporcional a la potencia de cortocircuito
\( S_{cc} \):

$$ X_{th} = \frac{V^2}{S_{cc}} \qquad \text{(aproximando } R_{th}\ll X_{th} \text{ en redes de transmisión)} $$

**Variación con la topología.** En contingencia N-1 (pérdida de una línea), \( Z_{th} \) puede
duplicarse y el SCR caer a la mitad. Esto convierte una red "media" (SCR = 4) en "débil" (SCR = 2)
de forma instantánea.

**ESCR (Effective SCR).** Cuando hay condensadores de compensación conectados en el PCC, parte de
la potencia reactiva la aportan los propios condensadores. El ESCR corrige el SCR restando la
potencia capacitiva instalada \( Q_C \):

$$ \mathrm{ESCR} = \frac{S_{cc} - Q_C}{S_{n,conv}} $$

El ESCR es el indicador real de la fortaleza de la red desde el punto de vista del convertidor: si
\( Q_C \) es grande, la red parece más débil aunque su potencia de cortocircuito no haya cambiado,
porque el condensador ya aportaba la reactiva que antes venía de la red.

**Impedancia de Thévenin en alta frecuencia.** Para el análisis de estabilidad de armónicos, la
red no se modela solo con \( Z_{th}=R_{th}+jX_{th} \) a 50 Hz sino con su variación en frecuencia.
La impedancia de red crece con la frecuencia (\( X_{th}(\omega)=\omega L_{th} \)) y puede presentar
resonancias paralelas con bancos de condensadores conectados en la red. Estas resonancias son la
principal causa de amplificación de armónicos en redes industriales.

## 4 — SCR y sus implicaciones para el convertidor

El SCR cuantifica cuántas veces es la red más "fuerte" que el convertidor:

$$ \mathrm{SCR} = \frac{S_{cc}}{P_{conv}} $$

**Clasificación práctica:**

| SCR | Régimen | Comportamiento del convertidor |
|---|---|---|
| > 10 | Red muy fuerte | El convertidor no perturba la tensión del PCC. Control GFL estándar sin problemas. |
| 5–10 | Red fuerte | Interacción leve. PLL estable con BW normal. |
| 2–5 | Red media | Interacción significativa. Reducir BW del PLL. Vigilar resonancias. |
| 1.5–2 | Red débil | PLL al límite de estabilidad. Usar PSC o reducir BW agresivamente. |
| < 1.5 | Red muy débil | Control GFL estándar inestable. Requiere GFM o estrategias avanzadas. |

**Por qué el PLL es el límite crítico.** El PLL del convertidor GFL mide la tensión del PCC para
sincronizarse. En red débil, la inyección de corriente del propio convertidor perturba la tensión
que el PLL mide: se crea una realimentación positiva entre la estimación del ángulo del PLL y la
corriente inyectada. Cuando el BW del PLL supera un umbral (que depende del SCR), esta
realimentación positiva domina y el sistema se vuelve inestable.

**Margen de estabilidad del PLL.** La condición aproximada para estabilidad del PLL de primer orden
con ganancia \( K_{PLL} \) (rad/s/rad):

$$ K_{PLL} < \frac{\omega_0}{X_{th}\,I_{nom}} $$

Nótese que \( X_{th}=V^2/(S_{cc})=V^2/(\mathrm{SCR}\cdot P_{conv}) \): a mayor SCR, mayor margen
de estabilidad para el PLL.

**ESCR en parques eólicos offshore.** Los parques eólicos offshore con muchos aerogeneradores VSC
conectados a un bus AC colectivo presentan una carga capacitiva elevada (cables de 33 kV internos).
Esto reduce el ESCR del punto de entrega al convertidor HVDC offshore, que puede operar con ESCR
efectivo muy bajo — la razón por la que estos terminales usan control GFM (mode grid-forming) en
lugar de GFL.

## 5 — Impacto del SCR en el control GFL

El control GFL (grid-following) asume que la tensión del PCC es una referencia estable a la que
sincronizarse. Esta suposición se degrada a medida que el SCR disminuye.

**Mecanismo de inestabilidad del PLL en red débil.** El PLL estima el ángulo de la tensión del PCC.
Pero en red débil, la corriente inyectada por el convertidor modifica esa tensión. Si el convertidor
inyecta corriente en cuadratura (reactiva), la tensión del PCC cambia en fase — exactamente la
señal que el PLL usa para estimar el ángulo. Se crea un bucle cerrado parásito:

$$\Delta\theta_{PLL} \rightarrow \Delta i_q \rightarrow \Delta V_{PCC} \rightarrow \Delta\theta_{PLL}$$

La ganancia de este bucle es proporcional a \( X_{th}/V \) y crece cuando el SCR baja.

**Impedancia negativa del inversor GFL.** Para frecuencias por debajo del BW del PLL, el inversor
GFL presenta impedancia negativa en la banda \( [0, f_{PLL}] \):

$$ \mathrm{Re}[Z_{inv}(j\omega)] < 0 \quad \text{para } \omega < \omega_{PLL} $$

Esta impedancia negativa puede interactuar con la resonancia LC de la red o del filtro LCL,
produciendo oscilaciones sostenidas — el fenómeno de SSO (Sub-Synchronous Oscillations) observado
en parques eólicos conectados a redes débiles.

**Mitigaciones para SCR bajo:**

1. **Reducir el BW del PLL:** la zona de impedancia negativa se contrae. Contrapartida: respuesta
   más lenta ante perturbaciones de frecuencia.
2. **PSC (Power Synchronization Control):** sustituye el PLL por sincronización por potencia
   activa — el convertidor se sincroniza comparando su potencia con la referencia, sin medir el
   ángulo directamente.
3. **Impedancia virtual:** añadir una resistencia virtual en el lazo de control que amortigüe la
   resonancia. Equivalente a subir el amortiguamiento de la red sin pérdidas físicas.
4. **VSM (Virtual Synchronous Machine):** control que imita la inercia y el amortiguamiento de un
   generador síncrono — inherentemente estable en red débil porque su sincronización no pasa
   por un PLL.
5. **GFM pleno (grid-forming):** el convertidor forma su propia tensión y no depende de una red
   de referencia. La solución más robusta para SCR → 0.

## 6 — Medición del SCR en campo

El SCR no es un parámetro fijo: varía con la hora del día, la estación y los mantenimientos
programados de la red. Tres métodos para cuantificarlo:

**Método 1 — Inyección de perturbación.** Se inyectan pequeñas variaciones de potencia \( \Delta P \)
o \( \Delta Q \) mediante el propio convertidor y se mide la variación de tensión resultante
\( \Delta V \):

$$ |Z_{th}| \approx \frac{|\Delta V|}{|\Delta I|} \quad\Rightarrow\quad \mathrm{SCR} = \frac{V^2}{|Z_{th}|\,P_{nom}} $$

Es el método más práctico en campo porque no requiere acceso a la red: el convertidor actúa como
su propio medidor de impedancia.

**Método 2 — Cortocircuito trifásico programado.** En estudios de planificación (nunca en
operación), se calcula la potencia de cortocircuito a partir del flujo de cargas con la red en
cortocircuito en el PCC:

$$ S_{cc} = \frac{V_{PCC}^2}{|Z_{th}|} \quad\Leftarrow\quad |Z_{th}|=\frac{V_{PCC}}{I_{cc,trifásico}} $$

**Método 3 — Medición continua por variación natural.** Se aprovechan las variaciones naturales de
potencia (flicker de carga, rampa de generación) para estimar \( Z_{th} \) mediante correlación:

$$ Z_{th}(\omega) = \frac{\Delta V(\omega)}{\Delta I(\omega)} $$

Este método no perturba el sistema pero requiere señal suficiente y separación entre la perturbación
del convertidor y el ruido de fondo de la red.

**Variación temporal del SCR.** El SCR del mismo punto puede variar en un factor 2–3 entre:

- Horas punta (mucha generación distribuida en servicio → red más mallada → SCR alto)
- Noches de fin de semana (líneas en mantenimiento → red reducida → SCR bajo)
- Contingencias N-1 (pérdida de una línea o un transformador → SCR puede caer a la mitad)

Por eso los estudios de estabilidad deben verificar el convertidor tanto en el SCR máximo (para
dimensionar los filtros y la tensión DC) como en el SCR mínimo (para la estabilidad del PLL y
el control de reactiva).

**Norma IEC 61400-21.** Define el procedimiento de medición de la potencia de cortocircuito
disponible en el punto de conexión de un parque eólico. Requiere al menos 10 mediciones en
condiciones de viento distintas para obtener una estimación estadísticamente representativa.

<div class="cfig"><img src="figuras/red-thevenin-scr-analisis.png" alt="Red Thévenin, SCR e implicaciones para el control del convertidor"><div class="cap">Equivalente Thévenin del PCC con parámetros derivados del SCR y X/R; reactancia de Thévenin en función del SCR; margen de estabilidad del PLL frente al SCR; y variación del SCR ante contingencias N-1 y N-2 en la red de transmisión.</div></div>

## Conceptos relacionados
- [[impedancia-salida-estabilidad]] · [[grid-forming-vs-following]]

## Referencias
- Kundur, 1994; IEEE Std 1204.
