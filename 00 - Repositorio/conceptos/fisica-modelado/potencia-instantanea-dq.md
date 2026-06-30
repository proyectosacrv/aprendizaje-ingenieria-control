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
fecha_actualizacion: 2026-06-30
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

## Cuándo y por qué se usa
Para el droop (que reacciona a P y Q), el reparto de carga y la supervisión. Se suele **filtrar**
(paso-bajo) para eliminar el rizado de conmutación y los transitorios rápidos.

## Procedimiento de diseño (genérico)
1. Elige el punto de medida (condensador, PCC) y el alineamiento del marco.
2. Aplica las fórmulas con la convención coherente con tu transformada dq.
3. Filtra P y Q (corte 5–20 Hz) para el droop.

## Ejemplo de aplicación real
**Problema:** VSC con \( V_d=325\,\text{V} \), \( V_q=0 \) (marco orientado a la tensión). Calcular las referencias de corriente para inyectar \( P^*=500\,\text{kW} \) y absorber \( Q^*=100\,\text{kVAr} \) (inductivo).

Con el marco orientado: \( P=\tfrac{3}{2}V_d i_d \) y \( Q=-\tfrac{3}{2}V_d i_q \). Despejando: \( i_d^*=2P^*/(3V_d)=2\times500000/(3\times325)\approx1026\,\text{A} \); \( i_q^*=-2Q^*/(3V_d)=-2\times100000/(3\times325)\approx-205\,\text{A} \) (negativo porque absorción inductiva exige corriente reactiva en fase −q). Estas son las referencias que el lazo de corriente en dq debe seguir. Verificación: \( P_{real}=\tfrac{3}{2}\times325\times1026\approx500\,\text{kW} \) ✓.

## Ejemplo de código
```python
P = 1.5*(vd*id + vq*iq)
Q = 1.5*(vq*id - vd*iq)
dPm = wf*(P - Pm); dQm = wf*(Q - Qm)   # filtrado para el droop
```

## Parámetros y valores típicos
Corte del filtro de potencia 5–20 Hz. Factor 3/2 con amplitud de pico.

## Errores comunes
- Mezclar la convención de la transformada con la de la potencia (factor 3/2).
- Signo de Q según convención (inductivo/capacitivo): verifícalo en el equilibrio.

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: alimentar el droop): P,Q medidas en el condensador y
  filtradas a 15 Hz alimentan el droop P-f/Q-V. Son 2 de los 15 estados (\( P_m,Q_m \)).

## Conceptos relacionados
- [[marco-dq]] · [[droop-control]]

## Referencias
- Akagi et al., *Instantaneous Power Theory*, 2007.
