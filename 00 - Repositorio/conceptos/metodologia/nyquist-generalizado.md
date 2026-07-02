---
titulo: Criterio de Nyquist generalizado (MIMO, GNC)
slug: nyquist-generalizado
categoria: metodologia
tipo: metodo
nivel: avanzado
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [decidir estabilidad de sistemas multivariable y del cociente de impedancias]
tags: [nyquist-generalizado, gnc, mimo, eigenloci, impedancia, minor-loop-gain, avanzado, GNSI, SCR, GFM]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-02
relacionados: [criterio-nyquist, impedancia-salida-estabilidad, valores-singulares-mimo, criterio-middlebrook, impedancia-virtual]
referencias:
  - "Skogestad, Postlethwaite, Multivariable Feedback Control, Wiley 2005"
  - "Sun, Impedance-Based Stability Criterion for Grid-Connected Inverters, IEEE TPEL 2011"
  - "Belkhayat, Stability Criteria for AC Power Systems with Regulated Loads, PhD Purdue 1997"
  - "Wen et al., Analysis of D-Q Small-Signal Impedance of Grid-Tied Inverters, IEEE TPEL 2016"
---

## Definición
Extensión del [[criterio-nyquist|criterio de Nyquist]] a sistemas **multivariable**: la estabilidad
en lazo cerrado se decide por los rodeos de \( -1 \) de los **loci característicos** (autovalores)
de la matriz de ganancia de lazo \( \mathbf{L}(j\omega) \). Es la base formal del **criterio de
estabilidad por impedancia** en convertidores (cociente de impedancias \( 2\times2 \) en dq).

## Fundamento teórico
Para una planta MIMO con lazo \( \mathbf{L}(s)=\mathbf{C}(s)\mathbf{G}(s) \), el polinomio
característico del lazo cerrado es \( \det(\mathbf{I}+\mathbf{L}(s)) \). Aplicando el principio del
argumento a este determinante:
$$ Z = N\big(\det(\mathbf{I}+\mathbf{L}),\,-1\big) + P_{ol} $$
Equivalentemente (Teorema de Nyquist generalizado), se trazan los **eigenloci**
\( \lambda_i(j\omega)=\mathrm{eig}\,\mathbf{L}(j\omega) \), \( i=1\dots m \), y la suma de sus rodeos
netos de \( -1 \) debe ser \( -P_{ol} \) (polos inestables de lazo abierto) para que \( Z=0 \).

**Aplicación a impedancia (source-load).** Partiendo de un divisor fuente–carga estable por
separado, la tensión en el punto de conexión es
$$ \mathbf{V}=\mathbf{V}_s\big(\mathbf{I}+\mathbf{Z}_s\mathbf{Y}_l\big)^{-1} $$
con **minor loop gain** \( \mathbf{L}=\mathbf{Z}_s\mathbf{Y}_l=\mathbf{Z}_s\mathbf{Z}_l^{-1} \). El
conjunto es estable \( \iff \mathbf{L}(j\omega) \) cumple Nyquist generalizado. En AC trifásico,
\( \mathbf{Z} \) son matrices \( 2\times2 \) en dq → **dos** eigenloci. El caso SISO (DC, o
desacoplado) recupera el [[criterio-middlebrook|criterio de Middlebrook]] (\( Z_s/Z_l \) dentro del
círculo unidad como condición suficiente).

**Criterios suficientes (menos conservadores que la norma).** Calcular eigenloci es costoso y poco
robusto; alternativas:
- Norma: si \( \bar\sigma(\mathbf{Z}_s\mathbf{Y}_l)<1\ \forall\omega \) → estable (muy conservador).
- **G-norm / pasividad**: índices de pasividad de la impedancia (ver [[impedancia-salida-estabilidad|resistencia negativa]]).
- Valores singulares estructurados (μ) para incertidumbre (ver [[valores-singulares-mimo]]).

<div class="cfig"><img src="figuras/nyquist-generalizado-eigenloci.png" alt="eigenloci del minor loop gain frente al punto -1"><div class="cap">En un sistema MIMO la estabilidad la deciden los autovalores (eigenloci) de la matriz de ganancia de lazo $L=Z_sY_l$, no una sola función escalar. La suma de sus rodeos netos del punto $-1$ debe ser $-P_{ol}$; aquí ninguno rodea $-1$, así que el conjunto fuente-carga es estable. Es la base formal del criterio por impedancia en dq.</div></div>

## 1 — De \( \det(\mathbf{I}+\mathbf{L}) \) a los eigenloci: por qué son equivalentes
**Paso 1 — polinomio característico.** El lazo cerrado de un sistema MIMO con ganancia de lazo \( \mathbf{L}(s)\in\mathbb{C}^{m\times m} \) tiene la función característica \( \phi(s)=\det(\mathbf{I}+\mathbf{L}(s)) \). El principio del argumento (Cauchy) aplicado al contorno de Nyquist \( \Gamma \) da el número de ceros menos polos de \( \phi \) en el semiplano derecho:

$$ N = Z - P_{ol} = \frac{1}{2\pi j}\oint_\Gamma \frac{\phi'(s)}{\phi(s)}\,ds $$

Para lazo cerrado estable se requiere \( Z=0 \), es decir \( N=-P_{ol} \) (los rodeos netos de la imagen de \( \phi \) alrededor del origen deben cancelar exactamente los polos de lazo abierto inestables).

**Paso 2 — factorización por autovalores.** Usando la identidad \( \det(\mathbf{I}+\mathbf{L})=\prod_{i=1}^m(1+\lambda_i(\mathbf{L})) \):

$$ \phi(j\omega)=\det(\mathbf{I}+\mathbf{L}(j\omega))=\prod_{i=1}^m\bigl(1+\lambda_i(j\omega)\bigr) $$

Por tanto los rodeos de \( \phi \) alrededor del origen son equivalentes a la suma de los rodeos de cada factor \( (1+\lambda_i) \) alrededor del origen, que a su vez son los rodeos de los **eigenloci** \( \lambda_i(j\omega) \) alrededor de \( -1 \).

**Paso 3 — comparación con SISO.** En SISO (\( m=1 \)) hay un único eigenloci \( \lambda_1=L(j\omega) \) y la condición reduce exactamente al criterio de Nyquist clásico: \( N(j\omega)=1+L(j\omega) \), rodeos de \( -1 \) de \( L \). El GNC es su extensión natural al caso matricial sin ninguna hipótesis adicional.

$$ \boxed{N_{\text{neto rodeos}}\;\text{de } -1 \text{ por todos los eigenloci} = -P_{ol}} $$

## 2 — De SISO a MIMO: por qué los autovalores y no la traza

**El paso de SISO a MIMO.** En SISO, la ganancia de lazo es un escalar \( L(j\omega) \) y el criterio de Nyquist trata con una única curva en el plano complejo. En MIMO, la ganancia de lazo es una matriz \( \mathbf{L}(j\omega)\in\mathbb{C}^{N\times N} \): la pregunta es qué escalar o qué conjunto de escalares representan correctamente la información de estabilidad.

**Por qué no basta la traza.** Una primera idea intuitiva es usar la traza de \( \mathbf{L} \), que es la suma de los elementos diagonales (y también la suma de los autovalores): \( \text{tr}(\mathbf{L})=\sum_i\lambda_i \). Sin embargo, la traza puede ser pequeña incluso cuando la matriz tiene un autovalor grande que rodea \( -1 \):
- Ejemplo: \( \mathbf{L}=\begin{bmatrix}a&b\\-b&a\end{bmatrix} \) tiene \( \text{tr}(\mathbf{L})=2a \) y autovalores \( a\pm jb \). Si \( a\approx-1 \) y \( b \) es pequeño, un autovalor estará cerca de \( -1 \), aunque la traza valga \( 2a\approx-2 \), que no parece peligrosa.
- Más en general: la traza no detecta cancelaciones entre autovalores de signos opuestos.

**Por qué sí los autovalores.** Los autovalores \( \lambda_i \) de \( \mathbf{L}(j\omega) \) son las "ganancias de lazo generalizadas" en cada dirección modal. El criterio \( \det(\mathbf{I}+\mathbf{L})=\prod(1+\lambda_i) \) muestra que la inestabilidad ocurre cuando algún \( \lambda_i\to-1 \), independientemente de los demás. Cada autovalor actúa como una ganancia de lazo SISO independiente en su dirección propia.

**El caso más simple: \( \mathbf{L} \) diagonal.** Si \( \mathbf{L}=\text{diag}(L_1,L_2,\ldots,L_N) \), los autovalores son directamente los elementos diagonales: los N lazos son independientes. El GNC se reduce a N criterios de Nyquist SISO aplicados por separado, exactamente como el criterio de Middlebrook en el caso desacoplado. El acoplamiento d-q del sistema trifásico introduce elementos fuera de la diagonal que hacen que los autovalores difieran de los elementos diagonales.

**El criterio de la norma como condición suficiente.** Si \( \|\mathbf{L}\|_2<1 \) (la norma de valores singulares máximos), entonces \( |\lambda_i|<1\ \forall i \), y ningún eigenloci puede rodear \( -1 \). Esta condición es suficiente pero muy conservadora; es el análogo MIMO del criterio de Middlebrook SISO.

## 3 — El índice de estabilidad de Nyquist generalizado (GNSI)

**Definición del GNSI.** Para cada frecuencia \( \omega \), la distancia mínima de los autovalores de \( \mathbf{L}(j\omega) \) al punto \( -1+j0 \) es:
$$ d_{\min}(\omega) = \min_i\left|\lambda_i\big(\mathbf{L}(j\omega)\big) + 1\right| $$
El Índice de Estabilidad de Nyquist Generalizado (GNSI) es el mínimo de esa distancia sobre todas las frecuencias:
$$ \mathrm{GNSI} = \min_\omega\,d_{\min}(\omega) = \min_\omega\min_i\left|\lambda_i\big(\mathbf{L}(j\omega)\big)+1\right| $$

**Condición de estabilidad.** Si fuente y carga son estables individualmente (\( P_{ol}=0 \)), la cascada es estable si y solo si el Nyquist de todos los eigenloci evita \( -1 \), lo que implica GNSI > 0. Para un diseño bien amortiguado se busca GNSI > 0.3–0.5.

**El margen de módulo generalizado.** El GNSI es el análogo MIMO del margen de módulo SISO \( 1/M_s \). En SISO: \( d_{\min}=1/M_s \). En MIMO: \( \mathrm{GNSI}=\min|\lambda_i+1| \). Si \( \mathrm{GNSI}=1/M_s^{\text{gen}} \), entonces:
$$ M_s^{\text{gen}} = \frac{1}{\mathrm{GNSI}} $$
Un objetivo razonable es \( M_s^{\text{gen}}<2 \), equivalente a GNSI > 0.5.

**Interpretación geométrica.** El GNSI mide el "espacio de seguridad" alrededor del punto \( -1 \) en el plano de Nyquist: todos los eigenloci deben mantenerse fuera del disco de radio GNSI centrado en \( -1 \). Si GNSI disminuye, algún eigenloci se acerca a \( -1 \), señalando pérdida de estabilidad. Cuando GNSI → 0, el sistema está al borde de la inestabilidad.

## 4 — Conexión con el criterio de impedancia para convertidores de red

**El minor loop gain en dq.** Para un convertidor trifásico conectado a red, el análisis de estabilidad por impedancia trabaja en el marco de referencia dq (ver [[marco-dq]]). La interacción entre la red y el convertidor se modela como:
$$ \mathbf{V}_{PCC} = \mathbf{V}_s(\mathbf{I}+\underbrace{\mathbf{Z}_{red}\mathbf{Y}_{inv}}_{\mathbf{L}}(j\omega))^{-1} $$
La matriz \( \mathbf{L}(j\omega)=\mathbf{Z}_{red}(j\omega)\mathbf{Y}_{inv}(j\omega) \) es el minor loop gain \( 2\times2 \) en dq.

**Los componentes de \( \mathbf{L} \):**
- \( \mathbf{Z}_{red}(j\omega) \): impedancia de la red en dq. Para una red inductiva resistiva \( (R_g, L_g) \): \( \mathbf{Z}_{red}=\begin{bmatrix}R_g+sL_g & -\omega_0 L_g\\ \omega_0 L_g & R_g+sL_g\end{bmatrix} \) (con acoplamiento cruzado por Park).
- \( \mathbf{Y}_{inv}(j\omega) \): admitancia de entrada del inversor (inversa de su impedancia de salida en dq). Para un GFL con PI de corriente: tiene forma de filtro de paso bajo con polo en \( \omega_{ci} \).

**El criterio de Nyquist generalizado aplicado.** Los autovalores \( \lambda_{1,2}(j\omega)=\text{eigvals}(\mathbf{L}(j\omega)) \) son dos curvas en el plano complejo. El sistema es estable si ninguna de las dos rodea \( -1 \).

**El SCR crítico.** Al bajar el SCR (red más débil), \( \mathbf{Z}_{red} \) crece y \( \mathbf{L}=\mathbf{Z}_{red}\mathbf{Y}_{inv} \) también. En algún SCR crítico, uno de los eigenloci roza \( -1 \): el sistema está al límite de la inestabilidad. Para el proyecto 01 (GFM con LCL), el análisis modal y el GNC dan \( \mathrm{SCR}_{crit}\approx3.35\text{–}3.39 \), confirmado por ambos métodos.

**Por qué el GNC da el límite exacto y Middlebrook no.** El criterio de Middlebrook MIMO equivale a \( \|\mathbf{L}\|_2<1 \): condición suficiente que puede rechazan diseños estables. El GNC es exacto: el sistema es inestable si y solo si algún eigenloci rodea \( -1 \).

## 5 — El Nyquist generalizado en el plano de Nyquist: visualización

**La representación gráfica.** Para un sistema \( 2\times2 \), en cada frecuencia \( \omega \) se calculan los dos autovalores complejos \( \lambda_1(j\omega) \) y \( \lambda_2(j\omega) \). Al barrer \( \omega \) de \( -\infty \) a \( +\infty \) (o de 0 a \( \infty \) si la simetría lo permite), cada autovalor traza una curva en el plano complejo: los **eigenloci**.

**Lo que se busca en el plot.** El sistema es estable si ninguna de las dos curvas encierra el punto \( -1+j0 \). Esto es exactamente el criterio de Nyquist SISO para cada eigenloci por separado, pero con la salvedad de que el número total de rodeos de ambas curvas combinadas debe ser \( -P_{ol} \).

**Diferencia con SISO.** En SISO hay una única curva de Nyquist; la estabilidad se lee visualmente (¿rodea \( -1 \)?). En MIMO hay dos (o N) curvas; todas deben no rodear \( -1 \) (si \( P_{ol}=0 \)). La complejidad gráfica sube, pero la regla es la misma para cada curva.

**La distancia al punto \( -1 \).** En el plot de Nyquist generalizado, se dibuja un círculo de radio GNSI centrado en \( -1 \): todas las curvas de eigenloci deben quedar fuera de ese círculo. Cuanto más alejadas, mayor el margen de estabilidad.

**Efecto del SCR.** Al bajar SCR (subir \( \mathbf{Z}_{red} \)):
- Los eigenloci se "agrandan": se alejan del origen y se acercan a \( -1 \).
- El GNSI disminuye.
- En \( \mathrm{SCR}=\mathrm{SCR}_{crit} \), una curva toca \( -1 \): GNSI = 0.

## 6 — Diseño iterativo: Nyquist generalizado para el GFM con impedancia virtual

**Sistema y parámetros:**
- Filtro LCL: \( L_1=2 \) mH, \( L_2=0.5 \) mH, \( C_f=15\,\mu\mathrm{F} \), \( R_1=R_2=50\,\mathrm{m\Omega} \).
- Potencia nominal: \( S_n=1 \) MVA, tensión \( V_{ll}=690 \) V, frecuencia \( f_0=50 \) Hz.
- Red con SCR variable: \( Z_{base}=V_{ll}^2/S_n=0.476\,\Omega \). Para SCR \( x \): \( R_g+jX_g=V_{ll}^2/(x\cdot S_n) \) con \( X/R=10 \) (es decir, \( X_g=10R_g \), \( L_g=X_g/\omega_0 \)).
- Impedancia virtual del GFM: \( X_{virt} \) en serie con la impedancia de salida del convertidor, que sube \( |Z_{inv}| \) en la banda de interés.

**Cálculo de \( \mathbf{L}=\mathbf{Z}_{red}\mathbf{Y}_{inv} \) en dq:**

La red tiene:
$$ \mathbf{Z}_{red}(j\omega)=\begin{bmatrix}R_g+j\omega L_g & -\omega_0 L_g\\ \omega_0 L_g & R_g+j\omega L_g\end{bmatrix} $$

La admitancia de entrada del GFM \( \mathbf{Y}_{inv}=\mathbf{Z}_{inv}^{-1} \) incluye el LCL, los lazos de control de corriente y tensión, y la impedancia virtual \( jX_{virt} \) en la representación de red dq.

**Sin impedancia virtual (\( X_{virt}=0 \)):**
Para SCR = 5: los eigenloci de \( \mathbf{L} \) se calculan numéricamente. El GNSI estimado por el análisis de los proyectos:
$$ \mathrm{GNSI}(\mathrm{SCR}=5,X_{virt}=0)\approx0.45 $$
El sistema es estable (GNSI > 0) pero con margen moderado.

Para SCR = 3 (cerca del crítico):
$$ \mathrm{GNSI}(\mathrm{SCR}=3,X_{virt}=0)\approx0.08\text{–}0.12 $$
Muy cercano al límite; pequeñas variaciones paramétricas pueden inestabilizarlo.

**Con impedancia virtual \( X_{virt}=0.05 \) pu \( =0.05\times0.476=23.8\,\mathrm{m\Omega} \):**
La impedancia virtual actúa como una inductancia en serie con la salida del GFM, subiendo \( |\mathbf{Z}_{inv}| \) y bajando \( |\mathbf{Y}_{inv}| \) → los eigenloci de \( \mathbf{L}=\mathbf{Z}_{red}\mathbf{Y}_{inv} \) se encogen → se alejan de \( -1 \):
$$ \mathrm{GNSI}(\mathrm{SCR}=5,X_{virt}=0.05\,\text{pu})\approx0.65 $$
$$ \mathrm{GNSI}(\mathrm{SCR}=3,X_{virt}=0.05\,\text{pu})\approx0.30 $$

**El SCR crítico con impedancia virtual.** Con \( X_{virt}=0.05 \) pu, el SCR donde GNSI → 0 baja de \( \approx3.35 \) (sin \( X_{virt} \)) a \( \approx2.1 \): la red puede ser más débil antes de que el sistema pierda estabilidad.

**Paradoja aparente.** "El SCR crítico baja" podría parecer que la situación empeora, pero es al contrario: el SCR crítico es el límite inferior que el sistema puede tolerar. Si el SCR crítico baja de 3.35 a 2.1, el sistema puede funcionar en redes más débiles (SCR entre 2.1 y 3.35) sin inestabilizarse. La impedancia virtual amplía el rango de operación estable.

**Resumen del análisis:**

| Configuración | \( \mathrm{SCR}_{crit} \) | GNSI @ SCR=5 | GNSI @ SCR=3 |
|---|---|---|---|
| Sin \( X_{virt} \) | ≈ 3.37 | ≈ 0.45 | ≈ 0.10 |
| \( X_{virt}=0.05 \) pu | ≈ 2.10 | ≈ 0.65 | ≈ 0.30 |

<div class="cfig"><img src="figuras/nyquist-generalizado-analisis.png" alt="Nyquist generalizado: eigenloci, GNSI vs SCR, efecto de impedancia virtual"><div class="cap">(a) Los dos eigenloci $\lambda_{1,2}(j\omega)$ de $L=Z_{red}Y_{inv}$ en el plano complejo para SCR=5 sin $X_{virt}$: ambas curvas evitan $-1$ (sistema estable). (b) Para SCR=3 (cerca del crítico): los eigenloci más cercanos a $-1$; el círculo de radio GNSI$\approx$0.10 muestra el pequeño margen. (c) El GNSI vs SCR barriendo de 2 a 15: el SCR crítico donde GNSI$\to$0 es $\approx$3.37. (d) El efecto de $X_{virt}$: con $X_{virt}=0.05$ pu el GNSI sube y el SCR crítico baja a $\approx$2.1 — la impedancia virtual amplía el margen de operación en red débil.</div></div>

## Cuándo y por qué se usa
Estabilidad de convertidor conectado a red (GFL/GFM), interacción entre subsistemas (fuente–carga,
convertidor–convertidor) y microrredes, donde el modelo natural es MIMO y el acoplamiento d-q no es
despreciable. Es el criterio que sustenta el análisis por impedancia de los proyectos 01 y 02.

## Procedimiento de diseño (genérico)
1. Verifica estabilidad **individual** de fuente y carga (sin interconectar).
2. Forma el minor loop gain \( \mathbf{L}=\mathbf{Z}_s\mathbf{Y}_l \) en la frecuencia (dq, 2×2).
3. Calcula los eigenloci \( \lambda_i(j\omega) \) y cuenta rodeos de \( -1 \).
4. Calcula el GNSI = mínima distancia de los eigenloci a \( -1 \).
5. Si GNSI < 0.3, reforzar el diseño (subir impedancia de salida, añadir \( X_{virt} \), etc.).

## Ejemplo de código
```python
import numpy as np

def eigenloci(Zs, Yl, freqs):
    """Zs, Yl: (Nf, 2, 2) en dq; retorna loci (Nf, 2) y GNSI."""
    loci = np.zeros((len(freqs), 2), dtype=complex)
    for k in range(len(freqs)):
        loci[k] = np.linalg.eigvals(Zs[k] @ Yl[k])
    gnsi = np.min(np.abs(loci + 1))
    return loci, gnsi

# Ejemplo: red inductiva en dq
Sn, Vll, f0 = 1e6, 690.0, 50.0
w0 = 2*np.pi*f0
Zbase = Vll**2 / Sn         # 0.476 Ohm
f = np.logspace(-1, 3, 2000)
w = 2*np.pi*f

for SCR in [15, 5, 3, 2]:
    Zred_mag = Zbase / SCR
    XR_ratio = 10
    Rg = Zred_mag / np.sqrt(1 + XR_ratio**2)
    Lg = XR_ratio * Rg / w0

    Zs = np.zeros((len(f), 2, 2), dtype=complex)
    for k, wk in enumerate(w):
        Zs[k] = np.array([[Rg + 1j*wk*Lg, -w0*Lg],
                           [w0*Lg,          Rg + 1j*wk*Lg]])

    # Yl simplificada: filtro paso bajo (reemplazar con Y_inv real)
    wci = 2*np.pi*750
    yl_scalar = wci / (1j*w + wci)
    Yl = np.zeros((len(f), 2, 2), dtype=complex)
    for k in range(len(f)):
        Yl[k] = np.diag([yl_scalar[k], yl_scalar[k]])

    loci, gnsi = eigenloci(Zs, Yl, f)
    print(f"SCR={SCR:2d}: GNSI = {gnsi:.4f}")
```

## Parámetros y valores típicos
GNSI > 0.3–0.5 para margen de estabilidad razonable. Malla de frecuencia fina
alrededor de las resonancias de \( \mathbf{Z}_{red} \) y \( \mathbf{Z}_{inv} \).
\( \mathrm{SCR}_{crit} \) para GFM con LCL: típicamente entre 2 y 4 dependiendo del diseño.

## Errores comunes
- Aplicar el criterio sin comprobar la estabilidad individual de fuente y carga.
- Usar \( |Z_s/Z_l|<1 \) (SISO) en un sistema con fuerte acoplamiento d-q → conclusión errónea.
- Olvidar \( P_{ol} \) (rodeos requeridos ≠ 0 cuando hay polos inestables de lazo abierto).
- Confundir el determinante \( \det(\mathbf{I}+\mathbf{L}) \) con uno solo de los eigenloci.
- Interpretar "SCR crítico más bajo" como peor: significa que el sistema admite redes más débiles.

## Conceptos relacionados
- [[criterio-nyquist]] · [[impedancia-salida-estabilidad]] · [[criterio-middlebrook]] · [[valores-singulares-mimo]] · [[impedancia-virtual]]

## Referencias
- Skogestad, Postlethwaite, *Multivariable Feedback Control*, 2005.
- Sun, *Impedance-Based Stability Criterion for Grid-Connected Inverters*, IEEE TPEL 2011.
- Belkhayat, *Stability Criteria for AC Power Systems with Regulated Loads*, PhD 1997.
- Wen et al., *Analysis of D-Q Small-Signal Impedance of Grid-Tied Inverters*, IEEE TPEL 2016.
