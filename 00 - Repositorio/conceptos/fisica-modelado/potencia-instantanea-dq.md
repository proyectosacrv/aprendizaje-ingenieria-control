---
titulo: Potencia instantánea en dq (P, Q)
slug: potencia-instantanea-dq
categoria: fisica-modelado
tipo: concepto
nivel: basico
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [medir P y Q para el droop y el reparto de carga]
tags: [potencia, activa, reactiva, dq, medida]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-02
relacionados: [marco-dq, droop-control]
referencias:
  - "Akagi et al., Instantaneous Power Theory, Wiley-IEEE 2007"
---

## Definición
Cálculo de las potencias activa (P) y reactiva (Q) a partir de tensiones y corrientes en el
marco dq, sin necesidad de promediar sobre un periodo de red (medida "instantánea").

## Fundamento teórico
Con convención de **amplitud de pico de fase**:
$$ P=\tfrac{3}{2}(v_d i_d + v_q i_q), \qquad Q=\tfrac{3}{2}(v_q i_d - v_d i_q) $$
(Con convención de potencia invariante el factor 3/2 desaparece.) Si el eje d se alinea con la
tensión (\( v_q=0 \)): \( P=\tfrac{3}{2}v_d i_d \), \( Q=-\tfrac{3}{2}v_d i_q \) → P↔\( i_d \),
Q↔\( i_q \).

<div class="cfig"><img src="figuras/potencia-instantanea-dq-fasor.png" alt="diagrama fasorial de potencia en dq"><div class="cap">Con el eje d alineado con la tensión, P es proporcional a la proyección id de la corriente y Q a su proyección iq. El ángulo φ entre V e I fija el reparto activa/reactiva.</div></div>

## 1 — De dónde sale el factor \( \tfrac32 \) en \( P=\tfrac32(v_d i_d+v_q i_q) \)
**Paso 1 — la potencia es invariante al marco.** La potencia trifásica instantánea es la suma de las tres fases, \( p(t)=v_ai_a+v_bi_b+v_ci_c \). Una transformada que **conserve la potencia** cumpliría \( p=v_di_d+v_qi_q+v_0i_0 \) sin más. Pero el convenio del repositorio usa la transformada de Park de **amplitud invariante** (la que hace \( v_d=\hat V \), no \( \sqrt{3/2}\hat V \)), y esa **no** conserva la potencia: introduce un factor de escala que hay que recuperar.

**Paso 2 — la inversa de la Park de amplitud.** Con \( K=2/3 \) (amplitud invariante) y sin homopolar, la transformada directa e inversa de la fase \( a \) son:

$$ \begin{bmatrix}x_d\\x_q\end{bmatrix}=\frac{2}{3}\begin{bmatrix}\cos\theta&\cos(\theta-\tfrac{2\pi}{3})&\cos(\theta+\tfrac{2\pi}{3})\\-\sin\theta&-\sin(\theta-\tfrac{2\pi}{3})&-\sin(\theta+\tfrac{2\pi}{3})\end{bmatrix}\!\begin{bmatrix}x_a\\x_b\\x_c\end{bmatrix},\quad
x_a=x_d\cos\theta-x_q\sin\theta\;(\text{etc.}) $$

**Paso 3 — sustituir las inversas en la suma de las tres fases.** Escribiendo \( v_a=v_d\cos\theta-v_q\sin\theta \), \( i_a=i_d\cos\theta-i_q\sin\theta \), y análogos para b (ángulo \( \theta-\tfrac{2\pi}{3} \)) y c (\( \theta+\tfrac{2\pi}{3} \)), y multiplicando \( v_ki_k \), aparecen productos de cosenos y senos. Al sumar las tres fases usamos las identidades de simetría trifásica:

$$ \sum_{k}\cos^2\theta_k=\frac32,\quad \sum_{k}\sin^2\theta_k=\frac32,\quad \sum_{k}\sin\theta_k\cos\theta_k=0 $$

(donde \( \theta_k=\theta,\theta\mp\tfrac{2\pi}{3} \)). Los términos cruzados \( \cos\theta_k\sin\theta_k \) se cancelan entre fases y solo sobreviven los cuadrados, cada uno aportando \( 3/2 \):

$$ \sum_{k}v_ki_k=\Big(\underbrace{\textstyle\sum\cos^2}_{3/2}\Big)v_di_d+\Big(\underbrace{\textstyle\sum\sin^2}_{3/2}\Big)v_qi_q=\frac32\big(v_di_d+v_qi_q\big) $$

**Paso 4 — resultado.** La suma física de las tres fases es exactamente:

$$ \boxed{\;P=v_ai_a+v_bi_b+v_ci_c=\tfrac32\big(v_di_d+v_qi_q\big)\;} $$

El \( 3/2 \) no es un convenio arbitrario: es \( 3 \) fases \( \times\,\tfrac12 \) del promedio de \( \cos^2 \). Si se usara la Park de **potencia invariante** (\( K=\sqrt{2/3} \)), esos sumatorios darían \( 1 \) en vez de \( 3/2 \) y el factor desaparecería. La parte reactiva sale igual cruzando los ejes: \( Q=\tfrac32(v_qi_d-v_di_q) \). Comprobado numéricamente: para \( \hat V=325 \), \( \hat I=10 \), \( \varphi=30° \), la suma trifásica y \( \tfrac32(v_di_d+v_qi_q) \) coinciden, y su media vale \( 3V_{rms}I_{rms}\cos\varphi \) (ver [[potencia-ac-fasores]]).

## 2 — De \( P=v_d i_d+v_q i_q \) a la teoría de potencia instantánea αβ

**La potencia en αβ.** Con la transformada de Clarke de amplitud invariante
\( (v_\alpha,v_\beta)=(\hat V\cos\omega t,\,\hat V\sin\omega t) \),
la potencia trifásica instantánea en el plano αβ es (Akagi, 1983):

$$ p(t)=v_\alpha i_\alpha+v_\beta i_\beta, \qquad q(t)=v_\beta i_\alpha - v_\alpha i_\beta $$

**El factor 3/2 de dq respecto a αβ.** La transformada de Clarke de amplitud invariante satisface
\( \sum v_k i_k = \tfrac{3}{2}(v_\alpha i_\alpha + v_\beta i_\beta) \).
La de Park (dq) aplica además una rotación de ángulo \( \theta \); como la rotación conserva el producto escalar,
\( v_\alpha i_\alpha+v_\beta i_\beta=v_di_d+v_qi_q \). Por tanto:

$$ \boxed{P_{3\phi}=\tfrac32(v_di_d+v_qi_q)=\tfrac32(v_\alpha i_\alpha+v_\beta i_\beta)} $$

Es decir, el factor 3/2 aparece en los dos dominios por la misma razón: la transformada de amplitud invariante no conserva la potencia.

**Con eje d alineado a la tensión (\( v_q=0 \)).** Entonces \( v_d=V \) (pico de fase), \( v_\alpha=V\cos\theta \), \( v_\beta=V\sin\theta \), y:

$$ P=\tfrac32 V i_d, \qquad Q=-\tfrac32 V i_q $$

La potencia reactiva instantánea de Akagi \( q(t)=v_\beta i_\alpha - v_\alpha i_\beta \) es, en este marco,
\( q=-Vi_q \) (sin el 3/2 al ser una definición en αβ, no en trifásica total).

## 3 — La potencia trifásica: por qué es constante en equilibrio

**La potencia de fase tiene un rizado a 2ω.** Para la fase \( a \) en equilibrio:
\( v_a=V\cos\omega t \), \( i_a=I\cos(\omega t-\varphi) \), luego:

$$ p_a(t)=V I\cos\omega t\cos(\omega t-\varphi)=\tfrac{VI}{2}\bigl[\cos\varphi+\cos(2\omega t-\varphi)\bigr] $$

Tiene una componente continua \( \tfrac{VI}{2}\cos\varphi \) (es la potencia activa por fase) y un **rizado a 2ω** de la misma amplitud.

**La suma de tres rizados a 2ω desfasados 120° se cancela.** Para las fases b y c los ángulos del coseno de 2ω son \( 2\omega t-\varphi-\tfrac{2\cdot2\pi}{3} \) y \( 2\omega t-\varphi+\tfrac{2\cdot2\pi}{3} \). La suma de tres cosenos desfasados 120° entre sí es cero (identidad trigonométrica):

$$ \sum_{k=a,b,c}\cos(2\omega t - \varphi - k\tfrac{2\pi}{3}) = 0 $$

Resultado: \( p_{3\phi}(t)=\tfrac32 VI\cos\varphi = P = \text{constante} \).

**En desequilibrio la componente de secuencia negativa introduce rizado.** Si existe una componente de secuencia negativa \( V^- \) en la tensión, la potencia instantánea total tiene un término oscilatorio a 2ω cuya amplitud depende de \( V^- \):

$$ \Delta P_{2\omega}\approx 2 V^+ V^- I^+ \cos(2\omega t+\phi)/V^{+2} $$

Este rizado es el síntoma del desequilibrio y la razón por la que la medida de P en dq también oscila a 2ω si no se filtra o si no se implementa estrategia de control asimétrica.

<div class="cfig"><img src="figuras/potencia-instantanea-dq-analisis.png" alt="análisis completo de potencia instantánea dq"><div class="cap">Panel (a): las tres potencias de fase oscilan a 2ω (100 Hz) y su suma es constante en equilibrio. Panel (b): la potencia instantánea p(αβ) y la potencia reactiva q(αβ) de Akagi para V=690 V ll, fp=0.95. Panel (c): el desequilibrio del 10% de V⁻ introduce un rizado visible en p₃φ(t) que no existe en el caso equilibrado. Panel (d): la trayectoria de i_d*(t) durante un escalón de P* de 0 a 500 kW (constante de tiempo ~5 ms del lazo de corriente) con Q* constante.</div></div>

## 4 — El control de P y Q en dq: las referencias \( i_d^* \), \( i_q^* \)

**Marco orientado a la tensión.** Con \( v_d=V \), \( v_q\approx 0 \) (el PLL alinea el eje d):

$$ P=\tfrac32 V i_d, \qquad Q=-\tfrac32 V i_q $$

**Las referencias de corriente.** Despejando de las expresiones anteriores:

$$ \boxed{i_d^*=\frac{2P^*}{3V},\qquad i_q^*=-\frac{2Q^*}{3V}} $$

Estas referencias entran directamente al lazo de corriente en dq. El error de seguimiento de P y Q queda reducido al error de seguimiento de \( i_d \) e \( i_q \) por el lazo PI de corriente, que tiene un ancho de banda \( \alpha_c \) mucho mayor que la dinámica de la potencia:

$$  P_{error}=\tfrac32 V(i_d^*-i_d)=\tfrac32 V \cdot e_{i_d}  $$

Así, la calidad del control de potencia depende directamente de la calidad del lazo de corriente.

**El papel de vq≠0.** Si la PLL no está perfectamente alineada (\( v_q\ne0 \)), el desacoplamiento no es exacto y P mezcla contribuciones de \( i_d \) e \( i_q \). Por eso el feedforward de tensión y un lazo de corriente rápido son críticos para el control preciso de P y Q.

## 5 — Potencia instantánea en presencia de desequilibrio: la descomposición

**Representación αβ con secuencia positiva y negativa.** Con una tensión desequilibrada:

$$ v_\alpha = V^+\cos(\omega t) + V^-\cos(-\omega t+\phi^-), \quad v_\beta = V^+\sin(\omega t) + V^-\sin(-\omega t+\phi^-) $$

(secuencia positiva gira en sentido positivo, negativa en sentido negativo.)

**La potencia instantánea con corriente de secuencia positiva** \( i_\alpha=I^+\cos(\omega t-\varphi) \), \( i_\beta=I^+\sin(\omega t-\varphi) \):

$$ p(t)=\underbrace{V^+I^+\cos\varphi}_{P_{dc}}+\underbrace{V^-I^+\cos(2\omega t-\varphi+\phi^-)}_{\tilde P_{2\omega}} $$

El rizado a 2ω tiene amplitud \( V^- I^+ \) y es proporcional a la magnitud de la secuencia negativa.

**Estrategias de control frente a desequilibrio:**

- **Eliminar el rizado de P** a costa de rizado en Q: se añade una componente de corriente de secuencia negativa tal que anule el término \( \tilde P_{2\omega} \). Esto requiere inyectar corriente de secuencia negativa \( I^- = V^- I^+ / V^+ \).

- **Eliminar el rizado de Q** a costa de rizado en P: la estrategia opuesta, útil para mantener Q=cte (por ejemplo para el soporte de tensión).

- **Eliminar ambos rizados** no es posible simultáneamente con un único VSC; requeriría cuatro grados de libertad de corriente (sistema sobredeterminado).

En la práctica (red con menos del 5% de V⁻) se trabaja en el marco dq con filtrado a 2ω o se implementan lazos separados de secuencia positiva/negativa.

## 6 — Diseño iterativo: referencias \( i_d^* \), \( i_q^* \) para un VSC de 1 MVA

**Especificaciones:** \( P^*=500\,\text{kW} \), \( Q^*=200\,\text{kVAr} \), \( V_{ll}=690\,\text{V} \), convención amplitud invariante.

**Paso 1 — tensión de fase pico.** El PLL alinea el eje d con la tensión de fase:
\( v_d = \hat V_{fase} = 690/\sqrt{3}\cdot\sqrt{2} \approx 563\,\text{V} \).

**Paso 2 — referencias de corriente.**
$$ i_d^*=\frac{2P^*}{3v_d}=\frac{2\times500\,000}{3\times563}\approx 591\,\text{A} $$
$$ i_q^*=-\frac{2Q^*}{3v_d}=-\frac{2\times200\,000}{3\times563}\approx -237\,\text{A} $$

El signo negativo de \( i_q^* \) indica inyección de potencia reactiva inductiva (absorción de reactiva → corriente de adelanto).

**Paso 3 — verificación de la corriente máxima.** El VSC de 1 MVA a 690 V tiene una corriente máxima:
\( I_{max}=S_n/(3\hat V_{fase}/2)\cdot 2/3 = 1\,000\,000\cdot 2/(3\times 563)\approx 836\,\text{A} \).

$$ |i^*|=\sqrt{i_d^{*2}+i_q^{*2}}=\sqrt{591^2+237^2}\approx 636\,\text{A} < 836\,\text{A}\quad\checkmark $$

El margen de corriente disponible es \( 836-636=200\,\text{A} \), suficiente para FRT.

**Paso 4 — lazo de corriente.** Con \( \alpha_c=2\pi\cdot 200\,\text{Hz} \) (ancho de banda del PI), la constante de tiempo del lazo es \( \tau_c=1/\alpha_c\approx 0.8\,\text{ms} \). En respuesta a un escalón de \( P^* \), \( i_d(t) \) alcanza el 95% de \( i_d^* \) en \( 3\tau_c\approx 2.4\,\text{ms} \). Esto es mucho más rápido que la dinámica del droop o el filtro de potencia (\( \tau_f\approx 10\,\text{ms} \)), lo que justifica la separación temporal del diseño.

## Cuándo y por qué se usa
Para el droop (que reacciona a P y Q), el reparto de carga y la supervisión. Se suele **filtrar**
(paso-bajo) para eliminar el rizado de conmutación y los transitorios rápidos.

## Procedimiento de diseño (genérico)
1. Elige el punto de medida (condensador, PCC) y el alineamiento del marco.
2. Aplica las fórmulas con la convención coherente con tu transformada dq.
3. Filtra P y Q (corte 5–20 Hz) para el droop.

## Ejemplo de código
```python
P = 1.5*(vd*id + vq*iq)
Q = 1.5*(vq*id - vd*iq)
dPm = wf*(P - Pm); dQm = wf*(Q - Qm)   # filtrado para el droop

# Referencias de corriente (marco orientado: vq=0)
id_ref = (2/3)*P_star / vd
iq_ref = -(2/3)*Q_star / vd
```

## Parámetros y valores típicos
Corte del filtro de potencia 5–20 Hz. Factor 3/2 con amplitud de pico.
Corriente máxima VSC típica: \( I_{max}=S_n\sqrt{2}/(3V_{fase,rms}) \).

## Errores comunes
- Mezclar la convención de la transformada con la de la potencia (factor 3/2).
- Signo de Q según convención (inductivo/capacitivo): verifícalo en el equilibrio.
- Olvidar que en desequilibrio P y Q medidas en dq tienen rizado a 2ω (100 Hz en 50 Hz).

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: alimentar el droop): P,Q medidas en el condensador y
  filtradas a 15 Hz alimentan el droop P-f/Q-V. Son 2 de los 15 estados (\( P_m,Q_m \)).

## Conceptos relacionados
- [[marco-dq]] · [[droop-control]] · [[sistema-trifasico]] · [[potencia-ac-fasores]]

## Referencias
- Akagi et al., *Instantaneous Power Theory*, Wiley-IEEE 2007.
