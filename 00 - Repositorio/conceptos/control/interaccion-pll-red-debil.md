---
titulo: Interacción PLL–red débil (inestabilidad del grid-following)
slug: interaccion-pll-red-debil
categoria: control
tipo: fenomeno
nivel: avanzado
proyectos: [02-GFL-Impedance]
objetivos: [entender y evitar la inestabilidad del GFL en red debil]
tags: [pll, red-debil, SCR, grid-following, oscilaciones, estabilidad]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-02
relacionados: [pll-srf, impedancia-salida-estabilidad, grid-forming-vs-following, red-thevenin-scr]
referencias:
  - "Dong et al., Analysis of Phase-Locked Loop Low-Frequency Stability in DG, IEEE TIE 2015"
  - "Sun, Impedance-based stability criterion for grid-connected inverters, IEEE TPEL 2011"
  - "Harnefors et al., Input-Admittance Calculation and Shaping, IEEE TPEL 2007"
---

## Definición
Inestabilidad característica del inversor grid-following en **red débil** (SCR bajo): la PLL y
la impedancia de red forman un lazo de realimentación positiva que produce oscilaciones de baja
frecuencia.

## Fundamento teórico
La PLL mide la tensión en el PCC para estimar el ángulo. En red débil (alta \( L_g \)), la
**corriente inyectada perturba esa tensión**: al inyectar, cae/gira la tensión del PCC, la PLL
malinterpreta el ángulo y corrige la corriente, que vuelve a perturbar la tensión. Si la PLL es
rápida, esta realimentación se cierra con fase desfavorable → inestable. En términos de
impedancia, la PLL hace \( \mathrm{Re}\{Z\}<0 \) (ver [[impedancia-salida-estabilidad|resistencia negativa]]) y al
cruzarse con la red inductiva se viola el Nyquist (ver [[impedancia-salida-estabilidad]]).

Es el **espejo** del grid-forming: el GFL se inestabiliza en red DÉBIL; el GFM (con control
agresivo) en red FUERTE.

<div class="cfig"><img src="figuras/interaccion-pll-red-debil-mapa.png" alt="SCR critico en funcion del ancho de banda de la PLL"><div class="cap">Mapa de estabilidad del grid-following: cuanto más rápida es la PLL, mayor es el SCR crítico por debajo del cual el sistema oscila, es decir, más amplia la región de red débil inestable. La palanca principal de diseño es reducir el ancho de banda de la PLL.</div></div>

## 1 — Por qué \( \Delta i_d \) perturba \( V_q \) en red débil: la realimentación positiva

**Paso 1 — modelo Thévenin de la red en dq.** La red vista desde el PCC es una fuente \( \mathbf{V}_g \) detrás de \( Z_{red}=R_g+jX_g \). La tensión en el PCC en αβ es:

$$ \mathbf{V}_{PCC} = \mathbf{V}_g - (R_g+jX_g)\,\mathbf{I} $$

**Paso 2 — linealización en el punto de operación.** El control orientado a \( \mathbf{V}_{PCC} \) mantiene \( V_d = V \), \( V_q = 0 \) en equilibrio. Una perturbación pequeña \( \Delta\mathbf{I}=\Delta i_d + j\Delta i_q \) produce una variación en el PCC. Separando partes real (eje d) e imaginaria (eje q) y tomando \( \Delta i_q = 0 \) para aislar el efecto de \( \Delta i_d \):

$$ \Delta V_d = -R_g\,\Delta i_d, \qquad \Delta V_q = -X_g\,\Delta i_d $$

**Paso 3 — por qué importa el signo de \( \Delta V_q \).** La PLL cierra un lazo PI sobre \( V_q \) para forzarla a cero. Una perturbación \( \Delta V_q < 0 \) (producida por \( \Delta i_d > 0 \) con \( X_g > 0 \)) hace que la PLL acelere el ángulo estimado \( \hat\theta \) para "recuperar" \( V_q = 0 \). El nuevo ángulo modifica \( i_d \) en sentido que amplifica \( \Delta i_d \):

$$ \boxed{\Delta V_q \approx -X_g\,\Delta i_d}, \qquad \frac{\partial \hat\omega_{PLL}}{\partial V_q} > 0 $$

**Paso 4 — la ganancia del lazo parásito.** La cadena completa es:

$$ \Delta i_d \xrightarrow{\times(-X_g)} \Delta V_q \xrightarrow{H_{PLL}(s)} \Delta\hat\theta \xrightarrow{\text{lazo corriente}} \Delta i_d $$

La ganancia de lazo en la frecuencia crítica es \( \approx K_{PPLL}\,X_g \). Cuando \( X_g \) crece (red débil, SCR bajo) y \( K_{PPLL} \) es grande (PLL rápida), el producto supera la unidad con fase desfavorable y el lazo se inestabiliza. La condición límite es:

$$ K_{PPLL}\,X_g\big|_{\text{fase}=-180°} = 1 \quad\Rightarrow\quad \text{oscilación sostenida} $$

Esto explica el **mapa de estabilidad**: a \( X_g \) fija, aumentar la PLL lleva antes al límite; a PLL fija, una red más débil (\( X_g \) mayor) cruza el límite con menos margen.

## 2 — El lazo de realimentación adicional que crea la PLL

La PLL no es simplemente un filtro de medida: crea un **lazo de control adicional** que no existe
en la planta nominal y que puede desestabilizar el sistema.

**Paso 1 — el lazo explícito.** El GFL inyecta corriente con ángulo \( \theta_{PLL} \):

$$ \mathbf{i}(t) = I\,e^{j\theta_{PLL}(t)} $$

La tensión en el PCC depende de la corriente inyectada:

$$ \mathbf{V}_{PCC}(t) = \mathbf{V}_g - Z_{red}\,\mathbf{i}(t) $$

La PLL estima el ángulo de \( \mathbf{V}_{PCC} \):

$$ \theta_{PLL}(t) = H_{PLL}(s)\star \angle\mathbf{V}_{PCC}(t) $$

El lazo completo: \( \theta_{PLL}\to\mathbf{i}\to\mathbf{V}_{PCC}\to\theta_{PLL} \). Este es el
**lazo parasitario** que no existe en red infinita (\( Z_{red}=0 \)).

**Paso 2 — cuándo el lazo parasitario es estabilizador o desestabilizador.** En red fuerte
(\( Z_{red}\approx0 \)), \( \mathbf{V}_{PCC}\approx\mathbf{V}_g \) sin importar \( \mathbf{i} \):
el lazo parasitario tiene ganancia cero → el sistema es estable. En red débil
(\( Z_{red} \) grande), la ganancia del lazo parásito es grande → puede desestabilizar.

**Paso 3 — la ganancia del lazo adicional.** Se linealiza alrededor del punto de operación
\( (I_0, V_{PCC,0}, \theta_0) \):

$$ \Delta V_{PCC,q} = -X_g\,\Delta i_d = -X_g\,I_0\,\Delta\theta_{PLL} $$

La ganancia de lazo del circuito parasitario:

$$ L_{par}(s) = \underbrace{X_g\,I_0}_{\text{red débil}} \cdot \underbrace{H_{PLL}(s)}_{\text{dinámica PLL}} $$

El módulo de \( L_{par} \) es proporcional a \( X_g \propto 1/\text{SCR} \). Al bajar el SCR,
la ganancia sube → eventualmente \( |L_{par}(j\omega_{osc})|=1 \) con \( \angle L_{par}=-180° \)
→ oscilación.

**Paso 4 — la frecuencia de oscilación.** La oscilación ocurre aproximadamente en la frecuencia
donde la PLL tiene 90° de retardo, que es cercana al ancho de banda de la PLL. Por eso las
oscilaciones observadas en red débil son de **baja frecuencia** (10–50 Hz), no en la frecuencia
de la portadora ni de la resonancia del filtro.

## 3 — La FDT del lazo de interacción: linealización

La herramienta de análisis formal es la **función de transferencia del lazo de interacción**.

**Paso 1 — perturbación \( \Delta\theta_{PLL} \).** Se introduce una perturbación \( \Delta\theta_{PLL} \)
en el ángulo de la PLL y se calcula cómo afecta a \( V_{PCC,q} \). La corriente perturbada:

$$ \Delta\mathbf{i} = \frac{\partial\mathbf{i}}{\partial\theta_{PLL}}\,\Delta\theta_{PLL}
   = jI_0\,e^{j\theta_0}\,\Delta\theta_{PLL} $$

En el marco DQ del PCC: la componente q de esta corriente perturbada es:

$$ \Delta i_q \approx I_0\,\Delta\theta_{PLL} \quad\text{(para }\theta_0\approx0\text{)} $$

**Paso 2 — propagación a \( V_{PCC,q} \).** La red con impedancia \( Z_{red}=R_g+jX_g \):

$$ \Delta V_{PCC,q} = Z_{red,qq}\,\Delta i_q = X_g\,I_0\,\Delta\theta_{PLL} $$

donde \( Z_{red,qq} \) es el elemento (q,q) de la matriz de impedancias de la red en el marco DQ
(para red inductiva, \( Z_{red,qq}\approx X_g \)).

**Paso 3 — la PLL cierra el lazo.** La PLL procesa \( V_{PCC,q} \) con su FDT \( H_{PLL}(s) \):

$$ \Delta\theta_{PLL} = H_{PLL}(s)\cdot\Delta V_{PCC,q} $$

Sustituyendo:

$$ \Delta\theta_{PLL} = H_{PLL}(s)\cdot X_g\cdot I_0\cdot\Delta\theta_{PLL} $$

**Paso 4 — la FDT del lazo de interacción.** El lazo se cierra con ganancia de lazo:

$$ \boxed{L_{int}(s) = Z_{red}(s)\cdot\left(\frac{\partial i}{\partial\theta}\right)\cdot H_{PLL}(s)
   = X_g\,I_0\,H_{PLL}(s)} $$

La condición de inestabilidad (Nyquist simplificado): \( |L_{int}(j\omega)|=1 \) con
\( \angle L_{int}(j\omega)=-180° \). La PLL de tipo 2 (con integrador) tiene 180° de retardo en
\( \omega\to0 \) → siempre hay un cruce crítico a baja frecuencia cuando \( X_g \) es suficientemente grande.

## 4 — SCR crítico como función del ancho de banda de la PLL

El análisis de \( L_{int} \) permite derivar el SCR crítico en función del diseño de la PLL.

**Paso 1 — la PLL de segundo orden.** La PLL con PI estándar (\( K_p, K_i \)):

$$ H_{PLL}(s) = \frac{K_p\,s + K_i}{s^2 + K_p\,s + K_i} $$

La frecuencia natural \( \omega_{n,pll}=\sqrt{K_i} \) y el amortiguamiento \( \zeta_{pll}=K_p/(2\omega_{n,pll}) \).
El ancho de banda de la PLL es aproximadamente \( \omega_{pll}\approx\omega_{n,pll} \) (para
\( \zeta_{pll}=1/\sqrt{2} \), el ancho de banda −3 dB es \( \approx\omega_{n,pll} \)).

**Paso 2 — el cruce de \( L_{int} \) a −180°.** Para la PLL de 2.° orden con \( \zeta=1/\sqrt{2} \),
el cruce de −180° ocurre aproximadamente en \( \omega_{osc}\approx\omega_{pll}/\sqrt{2} \). En ese
punto, \( |H_{PLL}(j\omega_{osc})|\approx1/\omega_{pll} \) (simplificado). La condición de margen
cero:

$$ |L_{int}(j\omega_{osc})| = X_g\,I_0\cdot\frac{1}{\omega_{pll}} = 1 $$

Despejando \( X_g \):

$$ X_{g,crit} = \frac{\omega_{pll}}{I_0} \quad\Rightarrow\quad \text{SCR}_{crit} = \frac{V_{pcc}^2}{X_{g,crit}\,S_{base}} \propto \frac{1}{X_{g,crit}} \propto \frac{I_0}{\omega_{pll}} $$

**Paso 3 — la relación cuadrática.** Refinando el análisis con la PLL de 2.° orden completa,
el SCR crítico escala aproximadamente como:

$$ \text{SCR}_{crit} \propto \left(\frac{\omega_{pll}}{\omega_0}\right)^2 $$

donde \( \omega_0=2\pi\times1\,\text{rad/s} \) es la referencia. Esto explica la curva cuadrática
del mapa de estabilidad: **doblar la frecuencia de la PLL cuadruplica el SCR mínimo necesario para
mantener la estabilidad**.

**Paso 4 — valores de referencia.**

| \( f_{PLL} \) [Hz] | \( \text{SCR}_{crit} \) | Comentario |
|---------------------|--------------------------|------------|
| 15 | 0.09 | Muy robusta, red casi infinita |
| 30 | 0.38 | Robusta: funciona hasta SCR ≈ 0.4 |
| 50 | 1.06 | Límite: solo para SCR > 1 |
| 100 | 4.2 | Peligrosa: requiere SCR > 4.2 |
| 150 | 9.5 | Muy agresiva: casi inutilizable en campo |
| 170 | 12.2 | Inestable en redes medias |

Los valores de SCR reales dependen del diseño exacto del PI de la PLL, la corriente nominal y
la topología del convertidor. Los de la tabla son indicativos con \( I_0=1\,\text{pu} \),
\( \zeta_{pll}=1/\sqrt{2} \).

## 5 — La resistencia negativa de la PLL: Re{Z_qq}<0

La perspectiva de impedancias da una interpretación física elegante del fenómeno.

**Paso 1 — impedancia de salida del GFL.** El GFL, visto desde el PCC, puede representarse
como una admitancia \( Y_{inv}(s) \). En el marco DQ, la matriz de impedancias de salida
\( Z_{inv}(j\omega) \) tiene cuatro elementos:

$$ \mathbf{Z}_{inv}(j\omega) = \begin{pmatrix} Z_{dd} & Z_{dq} \\ Z_{qd} & Z_{qq} \end{pmatrix} $$

El elemento crítico es \( Z_{qq} \): la impedancia en el eje q (reactiva). La PLL actúa
principalmente en el eje q (intenta mantener \( V_q=0 \)).

**Paso 2 — la PLL introduce Re{Z_qq}<0.** Cuando la PLL funciona a baja frecuencia
(\( \omega<\omega_{pll} \)), el lazo de la PLL "compensa" la variación de \( V_q \) variando
\( \theta_{PLL} \) → variando \( i_d \) → que a su vez perturba más \( V_q \). Esta realimentación
positiva aparece como una **resistencia negativa** en el eje q:

$$ \text{Re}\{Z_{qq}(j\omega)\} < 0 \quad\text{para }\omega < \omega_{pll} $$

La magnitud de esta resistencia negativa es proporcional a \( X_g \): en red débil es mayor.

**Paso 3 — la condición exacta de no pasividad.** El criterio de pasividad exige:

$$ \text{Re}\{Z_{inv}(j\omega)\} \ge 0 \quad\forall\omega $$

Si \( \text{Re}\{Z_{qq}\}<0 \) para \( \omega<\omega_{pll} \) y la red es inductiva
(\( \text{Im}\{Z_{red}\}>0 \)), el criterio de Nyquist para el lazo \( Z_{red}Y_{inv} \) puede
violarse. La condición exacta (Middlebrook generalizado):

$$ \left|\frac{Z_{red}}{Z_{inv}}\right|_{\omega_{osc}} = 1, \quad \angle\frac{Z_{red}}{Z_{inv}} = 180° $$

**Paso 4 — modelo de Re{Z_qq}.** Con un modelo simplificado de la PLL de 1.° orden
(\( H_{PLL}(s)\approx\omega_{pll}/(s+\omega_{pll}) \)):

$$ \text{Re}\{Z_{qq}(j\omega)\} = R_0\left(1 - \frac{2\omega_{pll}^2}{\omega_{pll}^2+\omega^2}\right) $$

- Para \( \omega\ll\omega_{pll} \): \( \text{Re}\{Z_{qq}\}\approx R_0(1-2)=-R_0<0 \).
- Para \( \omega=\omega_{pll} \): \( \text{Re}\{Z_{qq}\}=0 \) (cruce).
- Para \( \omega\gg\omega_{pll} \): \( \text{Re}\{Z_{qq}\}\approx R_0>0 \) (comportamiento pasivo).

La **banda de resistencia negativa** es \( [0, \omega_{pll}] \): toda la banda de la PLL.
Cuanto más ancha la PLL, mayor la banda de no pasividad → mayor riesgo.

$$ \boxed{\text{Re}\{Z_{qq}(j\omega)\} < 0 \quad\Leftrightarrow\quad \omega < \omega_{pll}} $$

## 6 — Soluciones y diseño iterativo

Hay tres estrategias principales, no excluyentes:

**Solución 1 — reducir \( \omega_{pll} \).** La palanca más directa y efectiva. Al bajar
\( \omega_{pll} \), el SCR crítico baja cuadráticamente. El coste es la **velocidad de
sincronización** post-falta: una PLL lenta tarda más en sincronizarse tras un transitorio o
una falta. Para \( f_{pll}=30\,\text{Hz} \), el tiempo de establecimiento es \( \approx5/(2\pi f_{pll})=26\,\text{ms} \); para \( f_{pll}=100\,\text{Hz} \) es \( \approx8\,\text{ms} \).

**Solución 2 — red virtual (impedance shaping).** Se modifica la referencia de corriente del
GFL para que la impedancia de salida se comporte como si hubiera una resistencia virtual en la red:

$$ i_q^* \leftarrow i_q^* - R_{virt}\cdot\frac{\Delta V_{pcc}}{V_{pcc}} $$

Esto añade amortiguamiento al lazo parásito sin cambiar la velocidad de la PLL. Es el análogo
al amortiguamiento activo del LCL: mejora la estabilidad sin sacrificar el ancho de banda de la
PLL. El coste es una pequeña variación en la corriente reactiva.

**Solución 3 — pasar a GFM.** Sin PLL, el problema desaparece. El grid-forming no tiene el
lazo parasitario PLL–red. El GFM sí puede tener inestabilidad en red fuerte (por la impedancia
de salida baja del GFM que interactúa con la red), pero el SCR crítico es diferente y en general
más favorable para redes débiles.

**Tabla de compromiso.**

| Estrategia | SCR mínimo necesario | \( t_{sync} \) [ms] | Complejidad |
|------------|---------------------|---------------------|-------------|
| \( f_{pll}=30 \) Hz | 0.4 | 26 | Baja |
| \( f_{pll}=60 \) Hz | 1.5 | 13 | Baja |
| \( f_{pll}=100 \) Hz | 4.2 | 8 | Baja |
| \( f_{pll}=100 \) Hz + red virtual | 2.0 | 8 | Media |
| GFM (droop) | 0.5 | N/A (sin PLL) | Alta |

Para una instalación con SCR variable (p.ej. parque PV que puede operar desde SCR=1.5 hasta
SCR=8 según la configuración de red), la mejor elección es \( f_{pll}=40\,\text{Hz} \) +
red virtual, que da SCR_crit ≈ 1.0 con un tiempo de sincronización aceptable de 20 ms.

<div class="cfig"><img src="figuras/interaccion-pll-red-debil-analisis.png" alt="analisis interaccion PLL red debil: lazo interaccion, SCR critico vs fpll, resistencia negativa, simulacion"><div class="cap">(a) Bode del lazo de interacción L_int para SCR=2,5,10 con fpll=100 Hz: el SCR bajo sube la ganancia del lazo y facilita la inestabilidad. (b) SCR_crit ∝ fpll²: diseños de referencia a 30 Hz (SCR_crit=0.38, robusto) y 100 Hz (SCR_crit=4.2, arriesgado). (c) Re{Z_qq}: banda negativa se extiende hasta fpll; PLL rápida amplía la banda de resistencia negativa. (d) Simulación con SCR=3: V_pcc con fpll=100 Hz oscila y diverge, con fpll=30 Hz se asienta.</div></div>

## Cuándo y por qué se usa (cómo se evita)
Aparece en parques PV/eólicos GFL conectados por líneas largas (red débil). Se previene
limitando el ancho de banda de la PLL, con impedance shaping, o migrando a grid-forming.

## Procedimiento de diseño (genérico)
1. Estima el SCR del punto de conexión (ver [[red-thevenin-scr]]).
2. Calcula la impedancia del GFL y verifica el Nyquist de \( Z_{red}Y_{inv} \) en el SCR mínimo.
3. Si hay riesgo: **reduce el ancho de banda de la PLL** (es la palanca principal), añade
   amortiguamiento/impedance shaping, o usa grid-forming.
4. Verifica el SCR crítico vs el ancho de banda de la PLL.

## Ejemplo de código
```python
# barrer SCR y ancho de banda de la PLL -> mapa de estabilidad
for fpll in [40, 60, 100, 150]:
    scr_crit = biseccion(lambda scr: maxre_acoplado(scr, fpll))  # inestable por debajo
```

## Parámetros y valores típicos
PLL lenta (≈30 Hz): robusta hasta SCR≈0.4. PLL rápida (≈100 Hz): inestable por debajo de
SCR≈4.2. PLL muy rápida (≈170 Hz): inestable hasta SCR≈12 (casi cualquier red).

## Errores comunes
- Acelerar la PLL para "mejorar" el seguimiento sin comprobar la red débil.
- Diseñar con red fuerte y desplegar en red débil sin reevaluar.
- Ignorar el SCR mínimo durante períodos de baja generación (red efectivamente más débil).
- No incluir el efecto de la PLL en el modelo de impedancia del GFL.

## Uso en proyectos
- **02 - GFL-Impedance** (objetivo: entender la inestabilidad): SCR crítico validado por dos
  vías (acoplado 3.48 vs Nyquist 3.55). La curva SCR_crítico(f_pll) muestra que la PLL rápida
  amplía la región débil inestable. Comparación directa con el GFM en `main_compare.py`.

## Conceptos relacionados
- [[pll-srf]] · [[impedancia-salida-estabilidad|resistencia negativa]] · [[grid-forming-vs-following]] · [[red-thevenin-scr]] · [[no-pasividad-resistencia-negativa]]

## Referencias
- Dong et al., *Analysis of PLL Low-Frequency Stability in DG*, IEEE TIE 2015.
- Sun, *Impedance-based stability criterion*, IEEE TPEL 2011.
- Harnefors et al., *Input-Admittance Calculation and Shaping*, IEEE TPEL 2007.
