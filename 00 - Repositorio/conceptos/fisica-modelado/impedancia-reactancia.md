---
titulo: Impedancia, reactancia y admitancia
slug: impedancia-reactancia
categoria: fisica-modelado
tipo: concepto
nivel: basico
proyectos: [01-GFM-Impedance, 02-GFL-Impedance, 03-DataCenter-IA]
objetivos: [base del análisis fasorial y del enfoque de impedancia]
tags: [impedancia, reactancia, admitancia, fasores, basico]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-06-30
relacionados: [potencia-ac-fasores, resonancia-rlc, impedancia-salida-estabilidad, red-thevenin-scr, filtro-lcl]
referencias:
  - "Sedra & Smith, Microelectronic Circuits"
---

## Definición
La **impedancia** \( Z \) es la "resistencia" generalizada de un elemento al paso de corriente
alterna: la relación (fasorial) entre tensión y corriente. Tiene parte resistiva \( R \) y parte
**reactiva** \( X \) (la que desfasa). La **admitancia** \( Y = 1/Z \) es su inversa.

## Fundamento teórico
En régimen senoidal, con fasores:
$$ Z = \frac{\hat V}{\hat I} = R + jX, \qquad Y = \frac{1}{Z} = G + jB $$
Para los elementos básicos:
$$ Z_R = R, \qquad Z_L = j\omega L, \qquad Z_C = \frac{1}{j\omega C} = -\frac{j}{\omega C} $$
La reactancia inductiva \( X_L=\omega L \) es positiva (la corriente atrasa); la capacitiva
\( X_C=-1/(\omega C) \) es negativa (la corriente adelanta). El módulo \( |Z|=\sqrt{R^2+X^2} \) y el
ángulo \( \angle Z = \arctan(X/R) \). Se combinan como las resistencias: **serie** suma \( Z \),
**paralelo** suma \( Y \). En sistemas trifásicos en el marco dq, la impedancia ya **no es un escalar
sino una matriz 2×2** por el acoplamiento entre ejes.

<div class="cfig"><img src="figuras/impedancia-reactancia-zf.png" alt="impedancia de R, L y C con la frecuencia"><div class="cap">Las reactancias dependen de la frecuencia: R es plana, la inductiva XL=ωL sube y la capacitiva XC=1/ωC baja. Donde se cruzan L y C aparece la resonancia.</div></div>

## 1 — Por qué \( Z_L=j\omega L \) (la reactancia inductiva \( X_L=\omega L \))
**Paso 1 — la ley física del inductor.** La ley de Faraday para un inductor relaciona tensión y derivada de la corriente:

$$ v(t)=L\frac{di(t)}{dt} $$

**Paso 2 — excitar con una corriente senoidal en forma compleja.** Usamos el fasor giratorio \( i(t)=\hat I\,e^{j\omega t} \) (la senoide real es su parte real). Derivar una exponencial solo la multiplica por \( j\omega \):

$$ \frac{di}{dt}=\frac{d}{dt}\big(\hat I\,e^{j\omega t}\big)=j\omega\,\hat I\,e^{j\omega t}=j\omega\,i(t) $$

**Paso 3 — sustituir en la ley.** Reemplazando:

$$ v(t)=L\cdot j\omega\,i(t)=j\omega L\,i(t) $$

**Paso 4 — tomar el cociente impedancia.** La impedancia es \( Z=v/i \), y \( i(t) \) se cancela:

$$ \boxed{\;Z_L=\frac{v}{i}=j\omega L\quad\Longrightarrow\quad X_L=\omega L\;} $$

La derivada temporal se ha convertido en una multiplicación por \( j\omega \): por eso el análisis fasorial sustituye ecuaciones diferenciales por álgebra. El factor \( j \) significa \( +90° \): la tensión adelanta a la corriente (equivalente: la corriente **atrasa**). \( X_L=\omega L \) crece con la frecuencia — la línea ascendente de la figura.

## 2 — Por qué \( Z_C=\dfrac{1}{j\omega C} \) (la reactancia capacitiva \( X_C=-1/\omega C \))
**Paso 1 — la ley física del condensador.** Ahora la corriente es la derivada de la tensión:

$$ i(t)=C\frac{dv(t)}{dt} $$

**Paso 2 — excitar con tensión senoidal compleja.** Con \( v(t)=\hat V\,e^{j\omega t} \), la derivada multiplica por \( j\omega \):

$$ i(t)=C\cdot j\omega\,v(t)=j\omega C\,v(t) $$

**Paso 3 — despejar la impedancia.** \( Z=v/i \), y \( v(t) \) se cancela:

$$ Z_C=\frac{v}{i}=\frac{1}{j\omega C} $$

**Paso 4 — racionalizar.** Multiplicando arriba y abajo por \( -j \) (con \( -j\cdot j=1 \)):

$$ \boxed{\;Z_C=\frac{1}{j\omega C}=\frac{-j}{\omega C}\quad\Longrightarrow\quad X_C=-\frac{1}{\omega C}\;} $$

El signo \( -j \) significa \( -90° \): la corriente **adelanta** a la tensión, justo lo contrario que en el inductor. Y \( X_C \) **decrece** con la frecuencia — la línea descendente de la figura. Donde \( |X_L|=|X_C| \), es decir \( \omega L=1/\omega C \), se cruzan: es la resonancia \( \omega_0=1/\sqrt{LC} \) (ver [[resonancia-rlc]]).

## 3 — La impedancia de la inductancia en el LCL: \( Z_L(s)=sL \) y su reactancia

**Paso 1 — la forma general.** En la variable compleja de Laplace \( s=\sigma+j\omega \), la ley del inductor \( v=L\,di/dt \) se convierte en \( V(s)=sL\cdot I(s) \), y la impedancia es:

$$ Z_L(s)=sL $$

En régimen senoidal \( s=j\omega \), de modo que \( Z_L=j\omega L \) (lo derivado en §1). La reactancia es la parte imaginaria:

$$ X_L=\omega L=2\pi f L $$

**Paso 2 — ejemplo numérico.** Para \( L=2\,\text{mH} \) a \( f=50\,\text{Hz} \):

$$ X_L=2\pi\times50\times0.002=0.628\,\Omega $$

A \( f=1\,\text{kHz} \): \( X_L=2\pi\times1000\times0.002=12.57\,\Omega \). La reactancia crece linealmente con la frecuencia: a la frecuencia de resonancia del LCL (\( f_{res}\approx3\,\text{kHz} \) en el proyecto 01), \( X_{L1}=2\pi\times3000\times0.002=37.7\,\Omega \).

**Paso 3 — en por unidad.** Con base de potencia \( S_{base}=1\,\text{MVA} \) y base de tensión \( V_{base}=400\,\text{V} \):

$$ Z_{base}=\frac{V_{base}^2}{S_{base}}=\frac{400^2}{10^6}=0.16\,\Omega $$

$$ X_{L,pu}=\frac{X_L}{Z_{base}}=\frac{0.628}{0.16}=3.93\,\%\,\text{pu} $$

Es el valor de inductancia en pu usado en diseño de convertidores: la inductancia del filtro suele estar entre 2 % y 10 % pu, lo que corresponde a \( L\in[0.05,\,0.25]\,\text{mH} \) en este base.

## 4 — La impedancia del condensador y la resonancia: \( Z_C=1/(sC) \)

**Paso 1 — impedancia capacitiva.** La ley del condensador \( i=C\,dv/dt \) en Laplace es \( I(s)=sC\,V(s) \), luego:

$$ Z_C(s)=\frac{1}{sC}\qquad\Longrightarrow\qquad Z_C(j\omega)=\frac{1}{j\omega C}=\frac{-j}{\omega C} $$

La reactancia capacitiva \( X_C=-1/(\omega C) \) es **negativa**: la corriente adelanta a la tensión 90°. Cae con la frecuencia, lo opuesto a \( X_L \).

**Paso 2 — la resonancia serie.** En el circuito LC serie, las impedancias se suman:

$$ Z_{serie}=Z_L+Z_C=j\omega L+\frac{1}{j\omega C}=j\left(\omega L-\frac{1}{\omega C}\right) $$

En la frecuencia de resonancia \( \omega_0 \) se anulan:

$$ \omega_0 L=\frac{1}{\omega_0 C}\quad\Longrightarrow\quad \omega_0=\frac{1}{\sqrt{LC}}\quad\Longrightarrow\quad \boxed{f_0=\frac{1}{2\pi\sqrt{LC}}} $$

En resonancia serie: \( Z_{serie}=0 \) (si \( R=0 \)): la corriente es máxima para tensión mínima — es un **cortocircuito en frecuencia**. Con resistencia \( R \), \( Z_{serie}(j\omega_0)=R \) (mínimo real).

**Paso 3 — la resonancia paralelo.** En el paralelo LC, las admitancias se suman:

$$ Y_{par}=\frac{1}{Z_L}+\frac{1}{Z_C}=\frac{1}{j\omega L}+j\omega C=j\left(\omega C-\frac{1}{\omega L}\right) $$

En \( \omega_0=1/\sqrt{LC} \): \( Y_{par}=0 \Rightarrow Z_{par}\to\infty \) — la impedancia de la rama paralela se hace infinita: **circuito abierto en frecuencia** (sin resistencia). Es la antiresonancia: la corriente de entrada cae a cero aunque haya corriente circulante interna entre L y C.

**Paso 4 — aplicación al filtro LCL.** El LCL del proyecto 01 (\( L_1=2\,\text{mH} \), \( C_f=25\,\mu\text{F} \), \( L_2=0.5\,\text{mH} \)) tiene una resonancia a:

$$ f_{res}=\frac{1}{2\pi}\sqrt{\frac{L_1+L_2}{L_1 L_2 C_f}}=\frac{1}{2\pi}\sqrt{\frac{0.0025}{0.002\times0.0005\times25\times10^{-6}}}=\frac{1}{2\pi}\sqrt{10^8}\approx1.6\,\text{kHz} $$

A esa frecuencia, la impedancia de entrada del LCL tiene un **pico** (la corriente de \( L_2 \) puede ser grande) mientras que la impedancia de entrada del condensador \( Z_{Cf} \) tiene un **valle** (antiresonancia desde el convertidor).

## 5 — El diagrama de Bode de la impedancia del LCL: picos y valles

**Paso 1 — la impedancia de entrada del LCL.** Vista desde el convertidor, el LCL es \( L_1 \) en serie con el paralelo de \( C_f \) y \( L_2 \):

$$ Z_{LCL}(s)=sL_1+\frac{sL_2\cdot\frac{1}{sC_f}}{sL_2+\frac{1}{sC_f}}=sL_1+\frac{L_2}{1+s^2 L_2 C_f}/s $$

**Paso 2 — identificar polos y ceros.** El numerador de la fracción tiene un cero en \( s=0 \) (el inductor \( L_2 \) bloquea DC) y el denominador tiene dos polos en \( s=\pm j/\sqrt{L_2 C_f} \). Sumando \( sL_1 \) aparece un polo adicional en \( s=0 \) (la inductancia total a baja frecuencia).

**Paso 3 — comportamiento asintótico.**
- **Bajas frecuencias** (\( f\ll f_{res} \)): \( Z_{LCL}\approx j\omega(L_1+L_2) \) — el LCL actúa como una inductancia total \( L_1+L_2 \) (+20 dB/dec).
- **En la resonancia** \( f=f_{res} \): \( |Z_{LCL}|\to\infty \) (sin amortiguamiento — pico real) o limitado por \( R_1+R_2 \) (damping resistivo).
- **Altas frecuencias** (\( f\gg f_{res} \)): \( Z_{LCL}\approx sL_1 \) — solo ve \( L_1 \) porque \( C_f \) cortocircuita \( L_2 \) (+20 dB/dec, pero con nivel reducido).
- **Antiresonancia**: a la frecuencia donde \( Z_{Cf}=Z_{L2} \), la impedancia de entrada tiene un **mínimo**; el condensador y \( L_2 \) forman un resonador que absorbe corriente sin que salga al exterior.

**Paso 4 — importancia para el control.** La resonancia del LCL está en la planta que ve el controlador de corriente. Sin amortiguamiento activo (§ amortiguamiento-activo en [[filtro-lcl]]), la ganancia de lazo pasa por infinito en \( f_{res} \) — el lazo se vuelve inestable para cualquier ganancia finita. El diseño de control **debe** tener en cuenta esta resonancia.

<div class="cfig"><img src="figuras/impedancia-reactancia-analisis.png" alt="impedancia LCL, reactancias vs frecuencia y comparativa pu vs Ω"><div class="cap">Panel (a): reactancias $X_L = \omega L_1$ y $X_C = 1/\omega C_f$ vs frecuencia — se cruzan en $f_{res}$. Panel (b): impedancia de entrada del LCL mostrando el pico de resonancia en $\approx$1.6 kHz. Panel (c): $X_L$ en pu para distintas potencias base: la misma inductancia física tiene distinto valor en pu según la base elegida. Panel (d): $|Z_{LCL}| \gg |Z_{red}|$ a $f_{sw}$=10 kHz: el LCL filtra eficazmente la corriente de rizado antes de llegar a la red.</div></div>

## 6 — Diseño iterativo: la impedancia del LCL del proyecto 01 a 50 Hz, 1 kHz y \( f_{res} \)

**Datos.** \( L_1=2\,\text{mH} \), \( L_2=0.5\,\text{mH} \), \( C_f=25\,\mu\text{F} \), red \( L_g=1\,\text{mH} \), \( S_{base}=1\,\text{MVA} \), \( V_{base}=400\,\text{V} \) → \( Z_{base}=0.16\,\Omega \).

**Paso 1 — a 50 Hz (fundamental).** El LCL actúa como \( L_1+L_2 \):

$$ Z_{LCL}(j2\pi\cdot50)=j\cdot2\pi\cdot50\cdot(0.002+0.0005)=j\cdot0.785\,\Omega\quad(=4.9\,\%\,\text{pu}) $$

La red tiene \( Z_{red}=j\cdot2\pi\cdot50\cdot0.001=j\cdot0.314\,\Omega \). El LCL es 2.5× mayor que la red a 50 Hz: la diferencia de tensión entre convertidor y red a nominal está repartida entre LCL y red en esa relación. El filtro no carga excesivamente la red a fundamental.

**Paso 2 — a 1 kHz.** Por encima de la resonancia pero por debajo de \( f_{sw} \):

$$ Z_{LCL}(j2\pi\cdot1000)\approx j\cdot2\pi\cdot1000\cdot0.002=j\cdot12.57\,\Omega\,(=78.6\,\%\,\text{pu}) $$

$$ Z_{red}(j2\pi\cdot1000)=j\cdot6.28\,\Omega $$

El LCL ya supera a la red por un factor 2, pero la componente de corriente a 1 kHz aún puede circular. El condensador empieza a derivar corriente.

**Paso 3 — en la resonancia \( f_{res}\approx1.6\,\text{kHz} \).** La impedancia de entrada teórica (sin \( R \)) tiende a infinito. Con \( R_1=0.05\,\Omega \) el pico real es:

$$ |Z_{LCL}(jf_{res})|_{max}=\frac{L_1+L_2}{R_1\,C_f\,f_{res}}\approx\frac{0.0025}{0.05\times25\times10^{-6}\times1600}\approx1250\,\Omega $$

Este pico descomunal (7812 pu) es la razón por la que el amortiguamiento activo es imprescindible.

**Paso 4 — a la frecuencia de conmutación \( f_{sw}=10\,\text{kHz} \).**

$$ Z_{LCL}(j2\pi\cdot10^4)\approx j\cdot2\pi\cdot10^4\cdot0.002=j\cdot125.7\,\Omega $$

$$ Z_{red}(j2\pi\cdot10^4)=j\cdot62.8\,\Omega $$

La condición de aislamiento \( Z_{LCL}\gg Z_{red} \) se cumple (razón ×2). La corriente de rizado a \( f_{sw} \) que llega a la red es \( \approx Z_{red}/(Z_{LCL}+Z_{red})\approx33\,\% \) de la generada por el convertidor antes de pasar por \( C_f \). Con el condensador, la atenuación real es mucho mayor (el \( C_f \) cortocircuita la corriente a alta frecuencia).

## Cuándo y por qué se usa
Es el lenguaje de todo el análisis AC: filtros, red Thévenin (\( Z_{red}=R_g+j\omega L_g \)),
resonancias y, sobre todo, el **enfoque de impedancia** para la estabilidad convertidor-red.

## Procedimiento de diseño (genérico)
1. Sustituye cada elemento por su impedancia \( Z(j\omega) \).
2. Combina por topología: serie \( \to \sum Z \); paralelo \( \to (\sum 1/Z)^{-1} \).
3. Evalúa \( |Z| \) y \( \angle Z \) en la banda de interés (o barre la frecuencia, Bode).

## Ejemplo de código
```python
import numpy as np
w = 2*np.pi*np.logspace(0, 4, 500)
ZL = 1j*w*2e-3; ZC = 1/(1j*w*20e-6)        # inductor y condensador
Zserie = 0.1 + ZL + ZC                      # R + L + C en serie
```

## Parámetros y valores típicos
Reactancias en pu: una inductancia de filtro suele ser 0.02–0.1 pu; la impedancia de red varía con el
SCR (\( |Z_{red}| = V_{ll}^2/(\mathrm{SCR}\cdot S_n) \)).

## 7 — Reactancia de cortocircuito y SCR: fuerza de la red

La reactancia de cortocircuito en el PCC se obtiene de la potencia de cortocircuito \(S_{sc}\):

$$X_{sc} = \frac{V_{ll}^2}{S_{sc}}, \qquad \text{SCR} = \frac{S_{sc}}{P_{conv}}$$

Para un convertidor de \(P_{conv}=10\,\text{MW}\) conectado a un nudo con \(S_{sc}=200\,\text{MVA}\): SCR = 20 (red fuerte). En redes de distribución rural con \(S_{sc}=30\,\text{MVA}\): SCR = 3 (red débil). Para SCR < 2 el convertidor GFL con PLL pierde estabilidad por la impedancia de red.

**Regla práctica:** diseñar el lazo de PLL para \(\omega_{PLL} < \omega_s/\text{SCR}^{0.5}\); en red débil (SCR = 3) limitar \(f_{PLL} < 20\,\text{Hz}\).

<div class="cfig"><img src="../figuras/impedancia-reactancia-analisis.png" alt="Análisis de impedancia: diagrama fasorial, impedancia vs SCR, Nyquist y medición"><div class="cap">(a) Diagrama fasorial R+jX con ángulo de impedancia φ. (b) Módulo de impedancia de red vs SCR para distintas tensiones de punto de conexión. (c) Criterio de Nyquist fuente/carga para estabilidad por impedancia. (d) Módulo de impedancia medida vs frecuencia con método de inyección sinusoidal.</div></div>

## 8 — Impedancia de Thevenin del convertidor

Vista desde la red, el convertidor controlado por realimentación presenta una impedancia de salida \(Z_{conv}(j\omega)\) que depende del lazo de control:

$$Z_{conv}(j\omega) = \frac{v_{PCC}(j\omega)}{i_{conv}(j\omega)}\bigg|_{v_{ref}=0}$$

Para un GFL con lazo de corriente PI y PLL:

$$Z_{conv}(j\omega) \approx \frac{L_1 s + R_1 + C_{PI}(s)}{1 + C_{PI}(s) G_{delay}(s)}$$

En la frecuencia de la portadora de PLL (\(\omega \approx \omega_{PLL}\)), la parte real de \(Z_{conv}\) puede volverse **negativa**: el convertidor actúa como una fuente de energía que amplifica las oscilaciones en esa banda. Esto es la raíz de la inestabilidad GFL en red débil.

## 9 — Criterio de estabilidad por impedancia

Con la notación fuente/carga, el sistema es estable si el lazo \(L(j\omega) = Z_s(j\omega)/Z_l(j\omega)\) satisface el criterio de Nyquist (no rodea \(-1+j0\)):

- **Middlebrook (conservador):** \(|Z_s| < |Z_l|\) para todo \(\omega\) — rechaza incertidumbre total.
- **ESAC (relajado):** permite \(|Z_s| > |Z_l|\) siempre que la fase de \(Z_s/Z_l\) no produzca encirculamiento; admite margen de fase de lazo abierto > 30°.

Gráficamente: trazar \(|Z_s|\) y \(|Z_l|\) en Bode y verificar que no se crucen, o trazar el Nyquist de \(Z_s/Z_l\) y comprobar que no rodee \(-1\).

**Para GFM:** \(Z_{conv}\) es inductivo-resistivo en toda la banda → siempre cumple Middlebrook frente a cargas resistivas/inductivas típicas.

## 10 — Medición práctica de impedancia

La técnica de inyección sinusoidal mide \(Z(j\omega)\) en el punto de operación:

1. Inyectar una perturbación de corriente \(\hat{i}\) a frecuencia \(f_k\) (amplitud 1–5% de la fundamental).
2. Medir \(\hat{v}\) en el mismo punto.
3. Calcular \(Z(f_k) = \hat{v}/\hat{i}\) mediante FFT o correlación.

**Criterio de calidad:** coherencia \(\gamma^2 > 0.9\) garantiza que la señal domina sobre el ruido.

**Comparación modelo/medida:** si \(|Z_{medida}| < |Z_{modelo}|\) en la zona de cruce → el modelo subestima la impedancia y el sistema puede ser menos estable de lo calculado.

**Herramientas:** analizadores de respuesta en frecuencia (FRA), inyectores de perturbación FPGA, o software MATLAB/Python con correlación cruzada.

## 11 — La impedancia de red en el marco dq: matriz 2×2

En el marco dq síncrono, el modelo de la red \(R_g + j\omega L_g\) no es un escalar sino una matriz:

$$\mathbf{Z}_{red}(s) = \begin{pmatrix} R_g + sL_g & -\omega L_g \\ \omega L_g & R_g + sL_g \end{pmatrix}$$

Los términos fuera de la diagonal (\(\pm\omega L_g\)) son el acoplamiento cruzado entre ejes d y q. En el análisis de impedancia para estabilidad, la condición de Middlebrook debe aplicarse sobre los valores singulares de \(\mathbf{Z}_{red}\) y \(\mathbf{Z}_{inv}\), no sobre sus módulos escalares.

**Consecuencia práctica.** Si el inversor inyecta solo corriente en el eje d (\(i_q=0\)), la reactancia de red en el eje q que "ve" el lazo de PLL no es cero: hay una tensión inducida \(\omega L_g i_d\) en el eje q que perturba el PLL. Esto es el origen de la interacción PLL-red débil: en red fuerte \(\omega L_g\) es pequeño; en red débil puede ser mayor que la tensión de referencia del PLL, produciendo pérdida de sincronismo.

## 12 — Impedancia de salida del inversor GFM (VSM/PSC)

A diferencia del GFL, el inversor GFM no sincroniza con la red mediante un PLL sino que genera su propio ángulo de tensión. Su impedancia de salida vista desde la red tiene parte real **positiva** en toda la banda de frecuencias:

$$\text{Re}[Z_{GFM}(j\omega)] > 0 \quad \forall \omega$$

Esta propiedad — que el GFM sea pasivo en toda la banda — es la razón por la que el GFM es estable en red débil mientras el GFL puede ser inestable. Físicamente: el GFM actúa como una fuente de tensión con impedancia interna (la inductancia del filtro + la impedancia virtual del control), que siempre absorbe energía de perturbaciones externas en lugar de amplificarlas.

**Cuantificación.** Para un VSM con droop de frecuencia \(D_p\) y constante de inercia virtual \(J\):

$$Z_{GFM}(j\omega) \approx R_{virt} + j\omega L_{virt} + \frac{(j\omega)^2 J \omega_0}{D_p}$$

A bajas frecuencias la impedancia es dominada por el término inercial; a frecuencias intermedias por la resistencia/inductancia virtual. El resultado es que \(\text{Re}(Z_{GFM})>0\) en toda la banda de control, lo que garantiza pasividad y robustez.

## 13 — Medición de impedancia: verificación del criterio en laboratorio

El criterio de estabilidad por impedancia puede verificarse experimentalmente midiendo \(Z_{inv}(j\omega)\) y \(Z_{red}(j\omega)\) con la técnica de inyección sinusoidal:

1. **Con el inversor en operación**, inyectar una perturbación de corriente \(\hat{i}\) a frecuencia \(f_k\) (2–5 % de la fundamental) mediante un convertidor auxiliar.
2. **Medir** \(\hat{v}_{PCC}\) en el mismo punto con un analizador de espectros o FFT.
3. **Calcular** \(Z_{inv}(f_k) = \hat{v}/\hat{i}\) y repetir para todo el barrido en frecuencia.

**Indicador de calidad:** la función de coherencia \(\gamma^2(f) = |S_{vi}|^2/(S_{vv}S_{ii}) > 0.95\) garantiza que la señal domina sobre el ruido y los no lineales.

**Verificación del criterio:** si en alguna frecuencia \(|Z_{inv}| < |Z_{red}|\) y la fase de \(Z_{inv}/Z_{red}\) se acerca a \(\pm180°\), el sistema está cerca del límite de inestabilidad. El procedimiento permite detectar problemas antes de que ocurran en campo.

## 14 — Aplicación: lazo de diseño impedancia → estabilidad → control

El flujo de diseño basado en impedancia para un inversor GFL conectado a red débil:

1. **Calcular \(Z_{red}\)** desde el SCR y la longitud de cable: \(Z_{red}=R_g+j\omega L_g\).
2. **Sintonizar el PLL** con \(\omega_{PLL} < \omega_s/\sqrt{SCR}\) para que la frecuencia de cruce del PLL caiga en la zona donde \(\text{Re}(Z_{inv})>0\).
3. **Calcular \(Z_{inv}\)** con el lazo de corriente y el PLL sintonizados.
4. **Verificar Middlebrook:** \(|Z_{inv}|<|Z_{red}|\) en toda la banda, o ESAC con margen de fase del ratio \(Z_{inv}/Z_{red}\) superior a 30°.
5. **Si no se cumple:** reducir \(\omega_{PLL}\), añadir impedancia virtual inductiva al GFL (que hace \(Z_{inv}\) más inductivo), o cambiar a GFM.

**Diseño iterativo.** En el proyecto 02 (GFL en red débil), el SCR efectivo cae a 1.5 cuando se añaden líneas largas. Con el PLL sintonizado a \(f_{PLL}=10\,\text{Hz}\), la zona de impedancia negativa del inversor queda por debajo de 10 Hz — fuera del rango donde \(Z_{red}\) tiene resonancias relevantes, y el criterio se cumple.

## 15 — Impedancia de la red en sistemas con múltiples convertidores

Cuando varios convertidores se conectan al mismo bus, la impedancia efectiva vista por cada uno depende de la topología de red y del estado de los demás:

$$Z_{eff,k}(j\omega) = Z_{linea,k} + \frac{1}{\sum_{j\neq k} 1/Z_{tot,j}(j\omega)}$$

Donde \(Z_{tot,j}=Z_{linea,j}+Z_{inv,j}\) es la impedancia total del convertidor \(j\) vista desde el PCC. Si todos los convertidores son GFL con impedancias de salida similares y hay \(N\) conectados en paralelo, la impedancia equivalente vista por cualquiera es \(\approx Z_{inv}/(N-1)\): **más convertidores en paralelo hacen más débil la red efectiva** para cada uno individualmente.

Esto explica por qué parques eólicos con muchos aerogeneradores GFL pueden tener problemas de estabilidad aunque el SCR de la barra de colectora sea alto: la impedancia negativa de cada GFL se multiplica, pudiendo crear inestabilidades cuando el número de unidades supera cierto umbral.

## 16 — Por unidad de la impedancia: conversión entre bases

En análisis de sistemas, todas las impedancias se expresan en pu para poder comparar componentes de distintos niveles de tensión/potencia. La base de impedancia en un bus de tensión \(V_{base}\) y potencia \(S_{base}\):

$$Z_{base} = \frac{V_{base}^2}{S_{base}}$$

**Cambio de base.** Si un componente tiene impedancia \(Z_{pu,old}\) en la base \((S_{base,old}, V_{base,old})\) y se quiere expresar en la nueva base \((S_{base,new}, V_{base,new})\):

$$Z_{pu,new} = Z_{pu,old}\cdot\frac{S_{base,new}}{S_{base,old}}\cdot\left(\frac{V_{base,old}}{V_{base,new}}\right)^2$$

**Ejemplo.** El transformador de conexión tiene \(X_{trafo}=10\%\) en base \(S_T=25\,\text{MVA}\), \(V_T=33\,\text{kV}\). El parque tiene base \(S_{base}=10\,\text{MVA}\), \(V_{base}=33\,\text{kV}\):

$$X_{trafo,pu,parque} = 0.10\cdot\frac{10}{25}\cdot\left(\frac{33}{33}\right)^2 = 0.04\,\text{pu}$$

El SCR del parque visto a través del transformador: \(X_{sc}=X_{trafo}=0.04\,\text{pu}\), \(S_{sc}=S_{base}/X_{sc}=10/0.04=250\,\text{MVA}\), \(\text{SCR}=250/10=25\) — red muy fuerte.

## 17 — Visualización del lugar de impedancias: el diagrama de Nichols

El diagrama de Nichols (fase vs ganancia en dB) es equivalente al Bode pero permite leer directamente los márgenes de fase y ganancia sin separar dos gráficos. Para el criterio de estabilidad por impedancia:

Trazar la curva \(Z_s(j\omega)/Z_l(j\omega)\) en el diagrama de Nichols. La condición de Nyquist requiere que la curva no encircle el punto \((-180°, 0\,\text{dB})\). Los márgenes de estabilidad se leen directamente:
- **GM** = distancia vertical al punto de 0 dB cuando la fase cruza \(-180°\).
- **PM** = distancia horizontal a \(-180°\) cuando la magnitud cruza 0 dB.

Esta representación es útil porque un único gráfico muestra simultáneamente ganancia y fase, facilitando el análisis visual de la estabilidad cuando hay múltiples resonancias que producen cruces múltiples de 0 dB o de \(-180°\).

## 18 — La admitancia de la red y el concepto de "bus infinito"

Un **bus infinito** es una idealización donde la impedancia de la red es cero: la tensión es perfectamente sinusoidal e inmutable independientemente de la corriente inyectada. En ese caso, el inversor trabaja "contra" una fuente de tensión ideal y la estabilidad solo depende de la impedancia interna del convertidor y su control.

En la práctica, todo bus tiene una impedancia finita que aumenta a medida que el SCR baja. El "bus infinito" corresponde al límite \(\text{SCR}\to\infty\) o equivalentemente \(Z_{red}\to0\). Para un convertidor GFL, este es el caso más favorable (la perturbación de tensión por la corriente inyectada es mínima). Para un GFM operando como referencia de tensión, el bus infinito externo no es problema mientras la impedancia interna del GFM sea mayor que la de la red.

**Cuándo la hipótesis de bus infinito falla.** En sistemas de isla o en redes de distribución con DER de alta penetración, el bus de conexión ya no es infinito: \(Z_{red}\) tiene magnitud comparable a \(Z_{inv}\) y la interacción impacta la estabilidad. Es cuando el análisis de impedancia sustituye al análisis de "lazo cerrado sobre bus infinito".

## 19 — Medición de SCR en campo: método de perturbación activa

El SCR de un punto de conexión puede medirse sin interrupción de la operación inyectando una perturbación de corriente calibrada mediante el propio inversor:

1. Inyectar una perturbación armónica pequeña \(\hat{i}(f_k)\approx1\%\,I_n\) a frecuencia \(f_k\).
2. Medir la variación de tensión en el PCC: \(\hat{v}_{PCC}(f_k)\).
3. Calcular \(Z_{red}(f_k)=\hat{v}_{PCC}/\hat{i}\).
4. A baja frecuencia (f_k→0): \(|Z_{red}(0)|=V_{LL}^2/(S_{sc})\), de donde \(S_{sc}=V_{LL}^2/|Z_{red}(0)|\) y \(\text{SCR}=S_{sc}/P_n\).

**Incertidumbre.** La medición tiene un error típico del ±15–20 % debido al ruido de medición, las armónicas de fondo y la variabilidad de la red. Para una estimación de SCR<2, la incertidumbre es suficiente para confirmar que la red es débil; no es suficiente para diseñar con precisión. En ese caso, se recomienda un barrido en frecuencia completo para obtener el modelo \(Z_{red}(j\omega)\) versus el escalar SCR.

## Errores comunes
- Olvidar el signo negativo de la reactancia capacitiva.
- Confundir \( |Z| \) con \( \mathrm{Re}(Z) \) (la parte real es la que disipa/aporta energía).
- Tratar la impedancia dq como un escalar cuando es una matriz 2×2.

## 20 — La impedancia en el análisis de armónicos de red

Los armónicos de corriente inyectados por convertidores interactúan con la impedancia de red para producir armónicos de tensión en el PCC. La relación (en el dominio de la frecuencia):

$$V_{harm}(j\omega_h) = Z_{red}(j\omega_h)\cdot I_{harm}(j\omega_h)$$

Si la impedancia de red tiene una resonancia en la frecuencia \(\omega_h\) (por la interacción de inductancias de línea y condensadores de banco), el armónico de corriente se amplifica en tensión por el factor Q de esa resonancia. Esto puede producir distorsión de tensión en el PCC mucho mayor que la que cabría esperar de la impedancia de red en baja frecuencia.

**Mitigación.** El análisis de armónicos de red (con el software de flujo de armónicos) calcula \(Z_{red}(j\omega_h)\) para todas las frecuencias de interés y verifica que el producto \(|Z_{red}|\cdot|I_{harm}|\) no supere los límites de tensión del EN 50160. Si hay resonancias, se sintoniza el banco de condensadores para que la resonancia caiga fuera de las frecuencias armónicas características del convertidor (5ª, 7ª, 11ª, 13ª para rectificadores de 6 y 12 pulsos).

## 21 — Resumen: las relaciones fundamentales de impedancia en convertidores

Las relaciones de impedancia que aparecen en el diseño y análisis de convertidores de red:

| Relación | Fórmula | Uso |
|---|---|---|
| Impedancia de filtro LCL | \(Z_{LCL}(s)=sL_1+\frac{L_2}{1+s^2L_2C_f}\cdot\frac{1}{s}\) | Diseño de filtro, resonancia |
| Impedancia de red (Thévenin) | \(Z_{red}=R_g+j\omega L_g\) | SCR, análisis de estabilidad |
| Impedancia de salida del inversor | \(Z_{inv}=v_{PCC}/i_{conv}|_{v_{ref}=0}\) | Análisis por impedancia |
| Criterio de Middlebrook | \(|Z_{inv}|<|Z_{load}|\) | Estabilidad fuente-carga |
| SCR efectivo | \(\text{SCR}=V_{LL}^2/(|Z_{red}|\cdot P_n)\) | Robustez del control |
| Reactancia por unidad | \(X_{pu}=X_{Ω}/Z_{base}\) | Escalado y comparación |

## 22 — Ejemplo de código: barrido de impedancia del LCL y verificación de Middlebrook

```python
import numpy as np

def lcl_zin(w, L1, L2, Cf, R1=0, R2=0):
    """Impedancia de entrada del LCL (vista desde el convertidor)."""
    s = 1j*w
    Zcf = 1/(s*Cf) + R2
    ZL2 = s*L2 + R2
    Zpar = (ZL2 * (1/(s*Cf))) / (ZL2 + 1/(s*Cf))
    return s*L1 + R1 + Zpar

def Zred(w, Lg, Rg=0):
    return 1j*w*Lg + Rg

L1=2e-3; L2=0.5e-3; Cf=10e-6; Lg=1e-3
f = np.logspace(1, 5, 2000)
w = 2*np.pi*f

Zlcl = np.abs(lcl_zin(w, L1, L2, Cf, R1=0.05, R2=0.05))
Zg   = np.abs(Zred(w, Lg))

# Criterio de Middlebrook: Z_source < Z_load (si LCL es fuente y red es carga)
idx_cross = np.where(np.diff(np.sign(Zlcl - Zg)))[0]
if len(idx_cross):
    print(f"Cruce Middlebrook en f={f[idx_cross[0]]:.0f} Hz")
    print("Zona de riesgo por encima de esa frecuencia." if Zlcl[idx_cross[0]+1] > Zg[idx_cross[0]+1]
          else "Middlebrook OK en todo el rango.")
else:
    print("Sin cruce: Middlebrook cumplido en toda la banda.")
```

## Conceptos relacionados
- [[potencia-ac-fasores]] · [[resonancia-rlc]] · [[impedancia-salida-estabilidad]] · [[red-thevenin-scr]] · [[filtro-lcl]]

## Referencias
- Sedra & Smith, *Microelectronic Circuits*.
