---
titulo: Criterio de Middlebrook (estabilidad de cascadas por impedancia)
slug: criterio-middlebrook
categoria: metodologia
tipo: metodo
nivel: avanzado
proyectos: [03-DataCenter-IA]
objetivos: [evaluar la estabilidad de una cascada fuente-carga por sus impedancias]
tags: [middlebrook, impedancia, cascada, bus-dc, estabilidad, CPL, ESAC, minor-loop-gain]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-02
relacionados: [dinamica-bus-dc, impedancia-salida-estabilidad, criterio-nyquist, nyquist-generalizado]
referencias:
  - "Middlebrook, Input Filter Considerations in Design of Switching Regulators, IEEE 1976"
  - "Wildrick et al., A Method of Defining the Load Impedance Specification for a Stable Distributed Power System, IEEE TPEL 1995"
  - "Feng et al., Impedance Specification and Impedance Improvement for a Two-Stage Power Electronic System, PESC 1999"
---

## Definición
Criterio para decidir la estabilidad de una **cascada fuente → carga** (p.ej. filtro/fuente que
alimenta un convertidor) a partir del cociente de sus impedancias, sin reconstruir el sistema
completo. Es el análogo DC del criterio de estabilidad por impedancia en AC.

## Fundamento teórico
Sea \( Z_{fuente}(s) \) la impedancia de salida de la fuente y \( Z_{carga}(s) \) la impedancia
de entrada de la carga. Si ambas son estables por separado, la cascada es estable según el
Nyquist del **cociente**:
$$ T_m(s) = \frac{Z_{fuente}(s)}{Z_{carga}(s)} $$
El **criterio de Middlebrook** (condición suficiente y conservadora) exige:
$$ |Z_{fuente}(j\omega)| \ll |Z_{carga}(j\omega)| \quad \forall \omega $$
es decir, que la impedancia de salida de la fuente sea mucho menor que la de entrada de la carga.
Con una [[dinamica-bus-dc|CPL]], \( Z_{carga}=-V^2/P \) (resistencia negativa,
\( |Z|=V^2/P \)): al subir \( P \), \( |Z_{carga}| \) baja y, cuando cae por debajo del pico de
resonancia de \( |Z_{fuente}| \), el sistema se inestabiliza. Existen criterios menos
conservadores (GMPM, banda prohibida, ESAC) que relajan el de Middlebrook.

<div class="cfig"><img src="figuras/criterio-middlebrook-impedancias.png" alt="impedancia de fuente con pico de resonancia frente a impedancia de carga CPL"><div class="cap">La fuente (filtro LC) tiene un pico de impedancia en su resonancia; la carga CPL presenta $|Z_{carga}|=V^2/P$, una línea horizontal que baja al subir la potencia. Mientras $|Z_{carga}|$ quede por encima del pico hay margen; cuando la potencia la hace cortar el pico, se viola el criterio y el bus se inestabiliza. Da la potencia límite de forma modular.</div></div>

## 1 — De dónde sale el cociente \( Z_o/Z_i \) (minor loop gain)
**Paso 1 — partir la cascada.** En el punto de interconexión, la fuente entrega una tensión \( v \) y la carga absorbe una corriente \( i \). Modelando cada lado por su Thévenin/Norton de pequeña señal: la fuente es \( v=v_{src}-Z_o\,i \) (su tensión ideal \( v_{src} \) menos la caída en su impedancia de salida \( Z_o=Z_{fuente} \)); la carga es \( i=v/Z_i \) (con \( Z_i=Z_{carga} \) su impedancia de entrada).

**Paso 2 — cerrar el lazo.** Sustituyendo \( i=v/Z_i \) en la ecuación de la fuente:
$$ v=v_{src}-Z_o\frac{v}{Z_i}\;\Rightarrow\; v\left(1+\frac{Z_o}{Z_i}\right)=v_{src}\;\Rightarrow\; \boxed{\;\frac{v}{v_{src}}=\frac{1}{1+\dfrac{Z_o}{Z_i}}\;} $$
La transferencia real de la cascada es la que tendría la fuente **sola** (\( v=v_{src} \)) multiplicada por el factor \( \dfrac{1}{1+T_m} \), con
$$ T_m(s)=\frac{Z_o(s)}{Z_i(s)}=\frac{Z_{fuente}}{Z_{carga}} $$

**Paso 3 — leerlo como un lazo.** \( \dfrac{1}{1+T_m} \) tiene exactamente la forma de una sensibilidad: \( T_m \) es la **ganancia de lazo menor** (minor loop gain) de la interconexión. Si fuente y carga son estables por separado, la cascada es estable \( \Leftrightarrow 1+T_m \) no tiene ceros en el semiplano derecho \( \Leftrightarrow \) el Nyquist de \( T_m \) no rodea \( -1 \). Toda la estabilidad de la cascada se reduce al Nyquist de **un cociente de impedancias**.

**Paso 4 — la condición de Middlebrook.** Si \( |T_m|=|Z_{fuente}|/|Z_{carga}|\ll1 \) a toda frecuencia, el punto \( -1 \) queda lejísimos: imposible rodearlo. De ahí la condición **suficiente** (y conservadora):
$$ \boxed{\;|Z_{fuente}(j\omega)|\ll|Z_{carga}(j\omega)|\quad\forall\omega\;} $$
Es suficiente pero no necesaria: la cascada puede ser estable aun violándola localmente, mientras el Nyquist de \( T_m \) no rodee \( -1 \) (eso explotan GMPM, banda prohibida, ESAC).

## 2 — El criterio de Middlebrook: derivación desde el divisor de impedancias

**El modelo fuente-carga en pequeña señal.**
La cascada se modela como un divisor de impedancias: la tensión en el bus es
$$ V_{bus}=V_{src}\cdot\frac{Z_{carga}}{Z_{fuente}+Z_{carga}} $$
Esta expresión es exacta (sin aproximación) para fuente y carga linealizadas. La inestabilidad ocurre cuando \( Z_{fuente}+Z_{carga}=0 \), es decir, \( Z_{fuente}=-Z_{carga} \): la fuente y la carga tienen impedancias iguales y opuestas → resonancia sin amortiguamiento → inestabilidad.

**Reescritura en forma de lazo cerrado.** Factorizando:
$$ V_{bus}=V_{src}\cdot\frac{1}{1+Z_{fuente}/Z_{carga}}=V_{src}\cdot\frac{1}{1+T_m} $$
El denominador \( 1+T_m \) tiene la forma de la función característica de un lazo realimentado con ganancia de lazo \( T_m=Z_{fuente}/Z_{carga} \).

**El minor loop gain \( T_m \).**
\( T_m(s)=Z_{fuente}(s)/Z_{carga}(s) \) es la **ganancia de lazo menor** de la interconexión. No es un lazo físico de control, sino la "ganancia de lazo equivalente" que emerge de la interacción entre la impedancia de la fuente y la admitancia de la carga. Sus polos y ceros determinan los modos de la cascada.

**El criterio de Middlebrook como condición suficiente.**
Si \( |T_m(j\omega)|<1 \) para todo \( \omega \) → el Nyquist de \( T_m \) no puede rodear \( -1 \) (está siempre dentro del círculo unidad) → cascada estable. La condición Middlebrook \( |Z_{fuente}|<|Z_{carga}| \) es precisamente \( |T_m|<1 \). Es suficiente pero conservadora: el sistema puede ser estable con \( |T_m|>1 \) en alguna banda, siempre que la curva de Nyquist no rodee \( -1 \).

## 3 — El criterio generalizado: ESAC y pasividad

El criterio de Middlebrook (\( |T_m|<1 \) en toda la banda) es muy conservador: puede rechazar diseños perfectamente estables en los que \( T_m \) supera la unidad pero su Nyquist no encierra \( -1 \). Se han desarrollado varios criterios menos conservadores:

**El ESAC (Energy Source Analysis Consortium).**
Define una región en el plano de Nyquist de \( T_m(j\omega) \): cualquier curva de Nyquist que permanezca dentro de esta región garantiza estabilidad. La región ESAC es más grande que el círculo unidad (por eso es menos conservadora): es un óvalo que se extiende hacia \( -\infty \) en el eje negativo real, excluyendo solo el punto \( -1 \) y sus vecinos próximos. Diseños que violan Middlebrook (\( |T_m|>1 \)) pero cuya curva de Nyquist permanece dentro del ESAC son estables.

**El criterio de pasividad (inmitancia).**
Si la impedancia de la fuente satisface \( \text{Re}[Z_{fuente}(j\omega)]>0 \) para todo \( \omega \) (fuente pasiva en el sentido de la parte real positiva), y la carga satisface \( \text{Re}[Z_{carga}(j\omega)]>0 \), la cascada es estable sin más condición. Una CPL tiene \( Z_{carga}=-V^2/P<0 \): no es pasiva, por eso puede inestabilizar. Un convertidor boost con lazo de tensión también puede presentar impedancia negativa en la banda del lazo.

**El criterio de Nyquist exacto.**
El más general: calcular directamente el Nyquist de \( T_m(j\omega)=Z_{fuente}(j\omega)/Z_{carga}(j\omega) \) y contar los rodeos de \( -1 \). Si ambas (fuente y carga) son estables por separado (\( P_{ol}=0 \)), la cascada es estable si y solo si el Nyquist de \( T_m \) no rodea \( -1 \). Este criterio es exacto (ni conservador ni optimista), pero requiere calcular \( Z_{fuente} \) y \( Z_{carga} \) completas en frecuencia.

**La jerarquía de criterios (de más a menos conservador):**
1. Middlebrook: \( |T_m|<1\ \forall\omega \) → muy conservador, fácil de verificar.
2. ESAC: curva de Nyquist dentro de la región ESAC → menos conservador.
3. Pasividad: \( \text{Re}[Z_{fuente}]>0 \) y \( \text{Re}[Z_{carga}]>0 \) → más general.
4. Nyquist exacto de \( T_m \) → exacto, pero requiere la impedancia completa.

## 4 — Aplicación al bus DC con CPL

**Modelo de la cascada en el datacenter.** El bus DC de 700 V está alimentado por un rectificador activo con filtro LC (\( L_f=0.5 \) mH, \( R_f=0.1 \) Ω, \( C_f \) grande) y la carga es un convertidor DC-DC que opera como CPL (potencia constante \( P \)).

**Impedancia de la fuente (filtro LC+rectificador).**
Simplificando el modelo: la impedancia de salida de la fuente en régimen pequeña señal es la del filtro LC con resistencia de fuente:
$$ Z_{fuente}(s)=R_f+sL_f $$
(se ignora \( C_f \) porque el condensador de salida es grande y lo hace casi nulo en la banda de interés; la impedancia sube linealmente con la frecuencia para \( \omega>R_f/L_f \)).

**Impedancia de la carga (CPL).**
La CPL con potencia \( P \) tiene impedancia de entrada:
$$ Z_{carga}=-\frac{V^2}{P}\quad (resistencia\ negativa) $$
En módulo: \( |Z_{carga}|=V^2/P=700^2/P \). Al subir \( P \), \( |Z_{carga}| \) baja.

**Verificación del criterio de Middlebrook.** ¿Se cumple \( |Z_{fuente}|<|Z_{carga}|\ \forall\omega \)?
- En DC (\( \omega=0 \)): \( |Z_{fuente}|=R_f=0.1\ \Omega \), \( |Z_{carga}|=700^2/100000=4.9\ \Omega \). \( 0.1<4.9 \). \( \checkmark \)
- El cruce (\( |Z_{fuente}|=|Z_{carga}| \)): \( |Z_{fuente}|=\sqrt{R_f^2+\omega^2 L_f^2}=4.9 \) cuando
  $$ \omega=\frac{\sqrt{4.9^2-R_f^2}}{L_f}=\frac{\sqrt{24.01-0.01}}{5\times10^{-4}}\approx\frac{4.899}{5\times10^{-4}}\approx9800\ \text{rad/s}\approx1560\ \text{Hz} $$
- Para \( \omega>9800 \) rad/s: \( |Z_{fuente}|>|Z_{carga}| \) → Middlebrook no garantiza estabilidad.

**Interpretación.** El criterio dice que por encima de 1560 Hz la condición de Middlebrook se viola. Sin embargo, en la práctica la CPL real no mantiene \( P=\text{cte} \) a esas frecuencias: el lazo de control del convertidor de carga tiene un ancho de banda finito (típicamente \( \le1 \) kHz), así que para frecuencias mayores la impedancia de carga se vuelve pasiva. El análisis de Middlebrook con CPL ideal es conservador: sobreestima el riesgo de inestabilidad a alta frecuencia.

**La potencia crítica por Middlebrook.** La condición \( |Z_{fuente}(\omega\to0)|<|Z_{carga}| \) da:
$$ R_f < \frac{V^2}{P}\;\Rightarrow\; P_{crit}^{Middlebrook}=\frac{V^2}{R_f}=\frac{700^2}{0.1}=4.9\ \text{MW} $$
Mucho más alta que la potencia real del sistema (100 kW): Middlebrook en DC no da el límite real. El límite real viene del pico de impedancia del filtro, que incluye la resonancia LC.

## 5 — El criterio para el lazo de potencia convertidor-red

**En sistemas de convertidores conectados a red**, el análisis de estabilidad por impedancia en AC usa exactamente el mismo marco de Middlebrook, pero en el dominio dq (ver [[nyquist-generalizado]]).

**Las impedancias relevantes:**
- \( Z_{fuente} = Z_{red}(s) \): impedancia de la red (Thévenin desde el PCC), que incluye la inductancia y resistencia de línea. Para una red con SCR definido: \( Z_{red}=V_{PCC}^2/(SCR\cdot S_n)\cdot(X/R\ \text{ratio}) \).
- \( Z_{carga} = 1/Y_{inv}(s) \): impedancia de entrada del inversor (vista desde el PCC). Es la inversa de la admitancia de entrada del convertidor.

**El minor loop gain en AC:**
$$ T_m(s)=Z_{red}(s)\cdot Y_{inv}(s) $$
En sistemas trifásicos dq, \( Z_{red} \) y \( Y_{inv} \) son matrices \( 2\times2 \), y \( T_m \) es también \( 2\times2 \): el criterio generalizado es el de Nyquist MIMO (ver [[nyquist-generalizado]]).

**El criterio de Middlebrook en AC:** \( |Z_{red}(j\omega)|<|Z_{inv}(j\omega)|\ \forall\omega \). Equivalente a \( |T_m|<1 \). Es más fácil de verificar que el Nyquist MIMO exacto, pero más conservador. En la práctica:
- Si la red es débil (SCR bajo → \( |Z_{red}| \) grande) y el inversor tiene impedancia de salida baja (convertidor GFL con mucha ganancia de lazo), puede violarse Middlebrook incluso con diseño estable.
- Si el inversor es GFM con impedancia virtual elevada (\( X_{virt}\gg Z_{red} \)), Middlebrook se satisface fácilmente.

**Comparación GFL vs GFM desde Middlebrook:**

| Tipo | \( |Z_{inv}| \) típico | Sensibilidad a red débil |
|---|---|---|
| GFL (lazo de corriente) | Baja (fuente de corriente ideal) | Alta: \( |Z_{red}|<|Z_{inv}|\approx\infty \) difícil |
| GFM (droop + impedancia virtual) | Alta (fuente de tensión + \( X_{virt} \)) | Baja: \( |Z_{red}|\ll|Z_{inv}| \) fácil |

## 6 — Diseño iterativo: verificación Middlebrook para el bus DC del datacenter

**Especificaciones del sistema:** bus DC 700 V, potencia de carga \( P_{carga}=100 \) kW (CPL), filtro de salida del rectificador \( L_f=0.5 \) mH, \( R_f=0.1 \) Ω, condensador de bus \( C_{bus}=10 \) mF.

**Impedancia de la fuente con condensador de bus:**
$$ Z_{fuente}(s)=\frac{(R_f+sL_f)\cdot(1/(sC_{bus}))}{R_f+sL_f+1/(sC_{bus})}=\frac{R_f+sL_f}{1+sC_{bus}(R_f+sL_f)} $$
Aproximación: resonancia LC en \( f_{res}=1/(2\pi\sqrt{L_f C_{bus}})=1/(2\pi\sqrt{5\times10^{-4}\cdot10^{-2}})\approx71 \) Hz. El pico de \( |Z_{fuente}| \) en la resonancia es \( \approx\sqrt{L_f/C_{bus}}/R_f\cdot R_f=\sqrt{L_f/C_{bus}}=\sqrt{0.05}=0.224 \) Ω (amortiguado por \( R_f \)).

**Impedancia de la carga (CPL para tres niveles de potencia):**
$$ |Z_{carga}|=\frac{V^2}{P}=\begin{cases}700^2/50000=9.8\ \Omega & P=50\ \text{kW}\\ 700^2/100000=4.9\ \Omega & P=100\ \text{kW}\\ 700^2/150000=3.27\ \Omega & P=150\ \text{kW}\end{cases} $$

**Verificación de Middlebrook:** el pico de \( |Z_{fuente}|\approx0.224 \) Ω es menor que \( |Z_{carga}|=4.9 \) Ω para \( P=100 \) kW. Middlebrook se satisface en toda la banda de 0 a ∞ para los tres niveles de potencia considerados.
$$ \max_\omega|Z_{fuente}|=0.224\ \Omega < 3.27\ \Omega=|Z_{carga}|(P=150\ \text{kW})\quad\checkmark $$

**La potencia crítica de Middlebrook:** \( P_{crit}^{Middlebrook}=V^2/\max|Z_{fuente}|=700^2/0.224\approx2.19 \) MW. El sistema no alcanza ese límite en operación real. Middlebrook es muy conservador con condensador de bus grande.

**Contraste con el análisis de Nyquist exacto:** el Nyquist de \( T_m=Z_{fuente}/Z_{carga} \) puede calcularse numéricamente. Para \( P=150 \) kW, el pico de \( |T_m|=0.224/3.27\approx0.068 \ll1 \): el punto de Nyquist más cercano a \( -1 \) es \( -0.068 \) → margen enorme. El análisis de Nyquist confirma lo que Middlebrook predice: el sistema con \( C_{bus}=10 \) mF está muy lejos de la inestabilidad incluso a 150 kW. El condensador de bus es el elemento estabilizador clave.

<div class="cfig"><img src="figuras/criterio-middlebrook-analisis.png" alt="Criterio de Middlebrook: impedancias, región de Nyquist, bus DC y comparativa"><div class="cap">(a) $|Z_{fuente}|$ y $|Z_{carga}|$ en el mismo Bode: la zona donde $|Z_{fuente}|>|Z_{carga}|$ es de riesgo. (b) La curva de Nyquist de $T_m=Z_{fuente}/Z_{carga}$ para los tres niveles de potencia: ninguna rodea $-1$. (c) Las tres curvas de $|Z_{carga}|$ para P=50, 100, 150 kW junto con $|Z_{fuente}|$: el condensador de bus mantiene el pico de fuente muy por debajo de la carga. (d) Comparativa Middlebrook vs Nyquist: el margen real (Nyquist) es mucho mayor que el mínimo que Middlebrook pide — Middlebrook es conservador en este caso.</div></div>

## Cuándo y por qué se usa
En sistemas DC en cascada (microrredes DC, data centers, alimentación distribuida) y en filtros
de entrada de convertidores. Permite diseñar de forma modular: caracterizar fuente y carga por
separado.

## Procedimiento (genérico)
1. Obtén \( Z_{fuente}(j\omega) \) (impedancia de salida del filtro/fuente).
2. Obtén \( Z_{carga}(j\omega) \) (de la CPL: \( -V^2/P \)).
3. Compara magnitudes: si \( |Z_{fuente}| \) supera \( |Z_{carga}| \) en alguna banda → riesgo.
4. Para el límite exacto, aplica Nyquist a \( T_m=Z_{fuente}/Z_{carga} \).
5. Si no cumple: baja \( |Z_{fuente}| \) (más \( C \), amortiguamiento) o sube \( |Z_{carga}| \).

## Ejemplo de código
```python
import numpy as np
from scipy import signal

V, P = 700.0, 100e3          # bus DC, potencia CPL
Lf, Rf, Cbus = 0.5e-3, 0.1, 10e-3

f = np.logspace(0, 4, 2000); s = 1j*2*np.pi*f

# Impedancia de fuente (filtro LC)
Zf_num = [Lf, Rf]; Zf_den = [Cbus*Lf, Cbus*Rf, 1]
# Zfuente(s) = (sLf+Rf)/(s^2*Cbus*Lf + s*Cbus*Rf + 1)
Zfuente = (s*Lf + Rf) / (s**2 * Cbus*Lf + s*Cbus*Rf + 1)

# Impedancia de carga (CPL, valor absoluto)
Zcarga_abs = V**2 / P

# Criterio de Middlebrook
middlebrook_ok = np.all(np.abs(Zfuente) < Zcarga_abs)
print(f"Middlebrook: {'OK' if middlebrook_ok else 'NO OK'}")
print(f"Pico |Zfuente| = {np.max(np.abs(Zfuente)):.3f} Ohm vs |Zcarga| = {Zcarga_abs:.2f} Ohm")

# Minor loop gain Tm = Zfuente/Zcarga
Tm = Zfuente / (-V**2/P)   # Zcarga = -V^2/P (negativo, CPL)
print(f"max|Tm| = {np.max(np.abs(Tm)):.4f}")
```

## Parámetros y valores típicos
Margen recomendado: \( |Z_{fuente}| \) varias veces menor que \( |Z_{carga}| \) en el pico de resonancia.
Criterio conservador (deja margen de diseño). Para verificación exacta: Nyquist de \( T_m \).

## Errores comunes
- Aplicar Middlebrook (muy conservador) y sobredimensionar; para el límite real usar Nyquist del cociente.
- Olvidar que \( |Z_{carga}| \) de la CPL baja al subir la potencia.
- Ignorar el ancho de banda finito del lazo de control de la carga (la CPL ideal es un modelo conservador).
- Confundir la condición suficiente de Middlebrook con el límite exacto de estabilidad.

## Uso en proyectos
- **03 - DataCenter-IA**: pico de \( |Z_{fuente}|\approx0.224 \) Ω con \( C_{bus}=10 \) mF → potencia límite
  de Middlebrook \( \approx2.19 \) MW, muy por encima de los 150 kW de operación.

## Conceptos relacionados
- [[dinamica-bus-dc|estabilidad del bus DC con CPL]] · [[impedancia-salida-estabilidad]] · [[nyquist-generalizado]]

## Referencias
- Middlebrook, *Input Filter Considerations...*, IEEE 1976.
- Wildrick et al., *A Method of Defining the Load Impedance Specification*, IEEE TPEL 1995.
