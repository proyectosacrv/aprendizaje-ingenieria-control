---
titulo: Transferencia de potencia en una línea (P-δ, Q-V)
slug: transferencia-potencia-linea
categoria: fisica-modelado
tipo: concepto
nivel: basico
proyectos: [01-GFM-Impedance]
objetivos: [fundamento del droop y de la rigidez sincronizante del grid-forming, estabilidad transitoria, perfil de tensión]
tags: [flujo-potencia, angulo, p-delta, q-v, estabilidad-estatica, estabilidad-transitoria, ferranti, area-igual, basico]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-07-03
relacionados: [droop-control, generador-sincrono, ecuacion-oscilacion, impedancia-virtual, grid-forming-vs-following, red-thevenin-scr]
referencias:
  - "Kundur, Power System Stability and Control, McGraw-Hill"
  - "Bergen, Vittal, Power Systems Analysis, Prentice Hall 2000"
  - "Anderson, Fouad, Power System Control and Stability, IEEE Press 2003"
---

## Definición
Describe cuánta potencia activa y reactiva fluye entre dos nudos conectados por una impedancia, en
función de la **diferencia de ángulo** y de las **tensiones**. Es el fundamento del reparto de carga
por droop y de la sincronización de máquinas y grid-forming.

## Fundamento teórico
Para dos tensiones \( V\angle\delta \) y \( E\angle 0 \) unidas por una reactancia \( X \) (línea
predominantemente inductiva), la potencia transmitida es:
$$ P = \frac{V E}{X}\sin\delta, \qquad Q = \frac{V(V - E\cos\delta)}{X} $$
Dos lecturas clave:
- La **activa** depende sobre todo del **ángulo** \( \delta \); la **reactiva** de la **diferencia de
  módulos** \( V-E \). De ahí el droop \( P\text{–}f \) (ajustar \( \delta \) vía frecuencia) y
  \( Q\text{–}V \) (ajustar \( |V| \)).
- Para \( \delta \) pequeño, \( P \approx \dfrac{VE}{X}\,\delta \), y la **rigidez sincronizante** es
$$ \frac{\partial P}{\partial \delta}\bigg|_{\delta\to 0} \approx \frac{VE}{X} $$
Si \( X \) es **pequeña** (red fuerte o poca reactancia de acoplamiento), \( \partial P/\partial\delta \)
es **enorme**: el lazo de potencia se vuelve muy sensible y difícil de estabilizar. Esta es,
exactamente, la razón por la que el grid-forming añade **impedancia virtual** (aumentar \( X \)).

<div class="cfig"><img src="figuras/transferencia-potencia-linea-pdelta.png" alt="curva P-delta"><div class="cap">La potencia transmitida crece con sen δ (máxima a 90°). Cerca de δ=0 es casi lineal: la pendiente ∂P/∂δ=VE/X es la rigidez sincronizante; con X pequeña se dispara y el lazo de potencia se vuelve difícil de estabilizar.</div></div>

## 1 — De dónde sale \( P=\dfrac{VE}{X}\sin\delta \)
**Paso 1 — la corriente por la reactancia.** Entre el nudo emisor \( \bar V=V\angle\delta \) y el receptor \( \bar E=E\angle0 \) hay solo una reactancia \( jX \) (línea inductiva pura, \( R=0 \)). Por la ley de Ohm fasorial:

$$ \bar I=\frac{\bar V-\bar E}{jX}=\frac{V\angle\delta-E\angle0}{jX} $$

**Paso 2 — potencia compleja que sale del nudo \( V \).** Usando \( \bar S=\bar V\,\bar I^{*} \) (conjugado, ver [[potencia-ac-fasores]]). Conjugar \( \bar I \) cambia el signo de su parte imaginaria; como \( (jX)^{*}=-jX \):

$$ \bar S=\bar V\,\bar I^{*}=V\angle\delta\cdot\left(\frac{V\angle\delta-E\angle0}{jX}\right)^{*}=V\angle\delta\cdot\frac{V\angle{-\delta}-E\angle0}{-jX} $$

**Paso 3 — multiplicar el numerador.** Distribuyendo \( V\angle\delta \):

$$ \bar S=\frac{V^2\angle0-VE\angle\delta}{-jX}=\frac{V^2-VE(\cos\delta+j\sin\delta)}{-jX} $$

**Paso 4 — racionalizar el \( -jX \).** Multiplicar arriba y abajo por \( j \) (porque \( \tfrac{1}{-j}=j \)):

$$ \bar S=\frac{j\big[V^2-VE\cos\delta-jVE\sin\delta\big]}{X}=\frac{VE\sin\delta}{X}+j\,\frac{V^2-VE\cos\delta}{X} $$

(el término \( -j\cdot j=+1 \) pasa a la parte real, y el resto queda imaginario).

**Paso 5 — separar P y Q.** Con \( \bar S=P+jQ \):

$$ \boxed{\;P=\frac{VE}{X}\sin\delta,\qquad Q=\frac{V(V-E\cos\delta)}{X}\;} $$

El \( \sin\delta \) sale del término cruzado \( VE\angle\delta \) al proyectarlo sobre el eje imaginario tras racionalizar — por eso **la activa la gobierna el ángulo**. La reactiva contiene \( V-E\cos\delta\approx V-E \) para \( \delta \) pequeño, así que **la gobierna la diferencia de módulos**.

## 2 — La rigidez sincronizante \( \partial P/\partial\delta \)
**Paso 1 — derivar \( P(\delta) \).** De \( P=\tfrac{VE}{X}\sin\delta \), tratando \( V,E,X \) como constantes:

$$ \frac{\partial P}{\partial\delta}=\frac{VE}{X}\cos\delta $$

**Paso 2 — evaluar en el punto de operación.** En torno a \( \delta\to0 \) (operación normal, pocos grados), \( \cos\delta\to1 \):

$$ \boxed{\;\frac{\partial P}{\partial\delta}\bigg|_{\delta\to0}=\frac{VE}{X}\;} $$

Es la pendiente de la curva P-δ en el origen: la "constante de muelle" que devuelve la máquina al sincronismo. Con \( X \) **pequeña** (red fuerte) la pendiente se dispara y el lazo de potencia se vuelve agresivo; por eso el grid-forming añade [[impedancia-virtual]] para aumentar \( X \) y bajar esta rigidez. En el proyecto 01 dio \( \approx 127 \) kW/rad.

## 3 — Las curvas P(δ) y Q(δ): derivación completa para línea con resistencia

### Modelo general: fuente E∠δ, receptor V∠0, línea Z=R+jX

El caso real de una línea de distribución (X/R pequeño) o de un cable submarino (R significativo) requiere incluir la resistencia. La corriente:

$$ \bar I=\frac{E\angle\delta-V\angle0}{R+jX}=\frac{E\cos\delta-V+jE\sin\delta}{R+jX} $$

La potencia compleja entregada al receptor \( S=V\bar I^* \):

$$ \bar S=V\cdot\frac{E\cos\delta-V-jE\sin\delta}{R-jX} $$

Multiplicando numerador y denominador por \( (R+jX) \):

$$ \bar S=\frac{V\big[(E\cos\delta-V)(R+jX)+jE\sin\delta(R+jX)\big]}{R^2+X^2} $$

Expandiendo la parte real e imaginaria con \( Z^2=R^2+X^2 \):

$$ \boxed{P=\frac{EV}{Z^2}(R\cos\delta+X\sin\delta)-\frac{V^2R}{Z^2}} $$

$$ \boxed{Q=\frac{EV}{Z^2}(X\cos\delta-R\sin\delta)-\frac{V^2X}{Z^2}} $$

### Para línea inductiva pura (R=0): recuperación del caso anterior

Con \( R=0 \), \( Z=X \):

$$ P=\frac{EV}{X^2}(X\sin\delta)=\frac{EV}{X}\sin\delta\quad\checkmark $$

$$ Q=\frac{EV}{X^2}(X\cos\delta)-\frac{V^2}{X}=\frac{EV\cos\delta-V^2}{X}=\frac{V(E\cos\delta-V)}{X} $$

que con el signo de convenio \( Q=V(V-E\cos\delta)/X \) coincide cuando se define la reactiva con sentido de entrega al emisor.

### Potencia máxima y ángulo crítico

Para línea con resistencia, \( P(\delta) \) tiene su máximo cuando \( dP/d\delta=0 \):

$$ \frac{dP}{d\delta}=\frac{EV}{Z^2}(-R\sin\delta+X\cos\delta)=0\;\Rightarrow\;\tan\delta_{Pmax}=\frac{X}{R} $$

El ángulo crítico es \( \delta_{crit}=\arctan(X/R) \): para una línea puramente inductiva, \( \delta_{crit}=90° \); para una resistiva pura, \( \delta_{crit}=0° \) (no hay transferencia de activa con ángulo).

### El ángulo de carga y la estabilidad de estado estacionario

Para una potencia requerida \( P_0 \) en una línea inductiva:

$$ \sin\delta_0=\frac{P_0 X}{EV} $$

Hay dos soluciones: \( \delta_0 \) y \( \pi-\delta_0 \). La condición de **estabilidad estática** es \( \partial P/\partial\delta>0 \):

$$ \frac{\partial P}{\partial\delta}=\frac{EV}{X}\cos\delta>0\;\Rightarrow\;\delta<90°\;\text{(estable)} $$

El **margen de estabilidad estática** mide cuánta potencia adicional se puede transmitir antes de cruzar los 90°:

$$ \Delta P=P_{max}-P_0=\frac{EV}{X}(1-\sin\delta_0) $$

**Ejemplo numérico:** \( P_0=0.7 \) pu, \( E=V=1 \) pu, \( X=0.1 \) pu.

$$ \sin\delta_0=\frac{0.7\cdot0.1}{1}=0.07\;\Rightarrow\;\delta_0=4.0°\quad(\text{muy bajo}) $$

Espera — para \( P_{max}=EV/X=10 \) pu y \( P_0=0.7 \) pu: \( \sin\delta_0=0.7/10=0.07 \), \( \delta_0=4.0° \). El margen es \( 10-0.7=9.3 \) pu.

Con \( X=1 \) pu (reactancia de acoplamiento más débil): \( \sin\delta_0=0.7/1=0.7 \), \( \delta_0=44.4° \), margen \( =1-0.7=0.3 \) pu (30%). Este segundo escenario ilustra mejor el diseño típico de un enlace de transmisión donde se opera entre 30° y 50°.

## 4 — El criterio de área igual para estabilidad transitoria

### La física de la aceleración y desaceleración

Durante un cortocircuito próximo al generador, la potencia eléctrica \( P_e \) cae bruscamente (la impedancia de falta hace que la tensión en el punto de conexión caiga). Sin embargo la potencia mecánica \( P_m \) no puede cambiar instantáneamente (inercia del árbol). El exceso \( P_m-P_e>0 \) acelera el rotor: \( M\ddot\delta=P_m-P_e \) (ecuación de oscilación, ver [[ecuacion-oscilacion]]).

El ángulo \( \delta \) crece mientras dura la falta. Cuando se despeja (apertura del relé en \( \delta_{cl} \)), la potencia eléctrica vuelve a la curva normal — pero ahora es mayor que \( P_m \): el generador desacelera. Si el ángulo no ha superado el punto en que \( P_e=P_m \) del lado inestable (\( \delta_{us}=\pi-\delta_s \)), existe margen de desaceleración suficiente y el sistema recupera el sincronismo.

### Las dos áreas y el criterio

**Área de aceleración** \( A_1 \): energía cinética ganada durante la falta, desde \( \delta_s \) (punto de operación previo) hasta \( \delta_{cl} \) (ángulo de despeje):

$$ A_1=\int_{\delta_s}^{\delta_{cl}}(P_m-P_e^{falta})\,d\delta $$

Durante la falta, si la tensión en PCC cae a 0 (cortocircuito sólido próximo), \( P_e^{falta}=0 \) y \( A_1=P_m(\delta_{cl}-\delta_s) \).

**Área de deceleración máxima disponible** \( A_2^{max} \): energía cinética que puede absorberse entre \( \delta_{cl} \) y \( \delta_{us} \):

$$ A_2^{max}=\int_{\delta_{cl}}^{\delta_{us}}(P_e^{post}-P_m)\,d\delta $$

**Criterio de área igual:** el sistema es estable si y solo si:

$$ \boxed{A_1\leq A_2^{max}} $$

Si \( A_1>A_2^{max} \): la energía cinética acumulada no puede disiparse antes de cruzar \( \delta_{us} \) → pérdida de sincronismo.

### El tiempo crítico de despeje

Para cada ángulo de despeje \( \delta_{cl} \), se puede calcular \( A_1 \) y \( A_2^{max} \). El **ángulo crítico de despeje** \( \delta_{cl,crit} \) es el máximo que permite \( A_1=A_2^{max} \). El relé de protección debe abrir antes de que \( \delta \) alcance \( \delta_{cl,crit} \), lo que impone el **tiempo crítico de despeje** \( t_{cl,crit} \) (típicamente 80–150 ms para máquinas de mediana inercia).

En los VSC con control de potencia, la inercia virtual puede ajustarse. Con más inercia virtual (\( M \) grande), la aceleración \( \ddot\delta=\Delta P/M \) es menor, \( \delta_{cl} \) más pequeño para el mismo tiempo de falta → mayor margen de estabilidad transitoria.

## 5 — El perfil de tensión y el efecto Ferranti

### La línea larga: distribución continua de parámetros

Para una línea de longitud \( l>100 \) km, la tensión varía a lo largo de la línea. El modelo de parámetros distribuidos (telegrafista) da la solución exacta. Con impedancia serie \( z=R'+jX' \) por unidad de longitud y admitancia shunt \( y=jB' \):

$$ \gamma=\sqrt{zy} \quad\text{(constante de propagación)} $$

La tensión en un punto a distancia \( x \) del extremo receptor:

$$ V(x)=V_R\cosh(\gamma x)+Z_c I_R\sinh(\gamma x) $$

donde \( Z_c=\sqrt{z/y} \) es la impedancia característica.

### El efecto Ferranti: tensión en vacío sube del receptor al emisor

En vacío (\( I_R=0 \)), la corriente capacitiva fluye hacia la fuente y la caída inductiva tiene signo opuesto al caso cargado. La tensión en el extremo emisor con el receptor abierto:

$$ V_E=V_R\cosh(\gamma l) $$

Para una línea puramente reactiva (\( R'=0 \)), \( \gamma=j\beta \) con \( \beta=\omega\sqrt{L'C'} \), y \( \cosh(j\beta l)=\cos(\beta l) \). Como \( \cos(\beta l)<1 \), **el emisor ve menos tensión que el receptor en vacío**: es decir, la tensión sube a lo largo de la línea desde el emisor hasta el receptor. El efecto Ferranti: el receptor en vacío puede tener tensión hasta un 10–15% superior a la del emisor en líneas de 300–400 km.

### Compensación reactiva: STATCOM y compensador serie

El **STATCOM** (compensador shunt) absorbe potencia reactiva inductiva en el extremo receptor cuando hay exceso de tensión (vacío) y la genera cuando hay carga. El **compensador serie** (condensador en serie) reduce la reactancia efectiva \( X_{ef}=X_l-X_c \), aumentando \( P_{max} \) y el margen de estabilidad.

**Ejemplo: línea 200 km, R'=0.1 Ω/km, X'=0.35 Ω/km, B'=2.7·10⁻⁶ S/km.**
- \( Z_{total}=20+j70\,\Omega \), \( Z_c\approx350\,\Omega \).
- Sin carga: el extremo receptor está al 105% de la tensión del emisor (Ferranti).
- Con carga nominal (0.8 pu, fp=0.9): caída de tensión ≈8%, receptor al 92%.
- Con STATCOM en el receptor absorbiendo/generando Q: tensión mantenida en ±2%.

## 6 — Diseño iterativo: línea 20 km para parque eólico 100 MW

### Datos del sistema

Parque eólico: \( P=100 \) MW, factor de potencia nominal \( \cos\phi=0.95 \) → \( Q_{max}=32.9 \) MVAR.
Línea de 33 kV, 20 km: \( R=0.1\cdot20=2\,\Omega \), \( X=0.35\cdot20=7\,\Omega \).
Trafo en el parque: 33/0.69 kV, \( S_n=100 \) MVA (agrupado).

### Paso 1: calcular la base y la línea en pu

Base elegida: \( S_{base}=100 \) MVA, \( V_{base}=33 \) kV.

$$ Z_{base}=\frac{V_{base}^2}{S_{base}}=\frac{33000^2}{100\times10^6}=10.89\,\Omega $$

$$ R_{pu}=\frac{2}{10.89}=0.184\,\text{pu},\qquad X_{pu}=\frac{7}{10.89}=0.643\,\text{pu} $$

$$ Z_{pu}=\sqrt{0.184^2+0.643^2}=0.669\,\text{pu},\qquad X/R=3.5 $$

### Paso 2: ángulo de operación y margen

Con \( P=1 \) pu, \( E=V=1 \) pu, usando la fórmula completa con resistencia:

$$ P=\frac{EV}{Z^2}(R\cos\delta+X\sin\delta)-\frac{V^2R}{Z^2}=1 $$

$$ \frac{R\cos\delta+X\sin\delta}{Z^2}=\frac{1+V^2R/Z^2}{EV}\approx1+\frac{0.184}{0.669^2}=1.411 $$

La solución numérica da \( \delta\approx40° \). Para la aproximación inductiva pura:

$$ \delta_{aprox}=\arcsin\!\left(\frac{P\cdot X}{EV}\right)=\arcsin(0.643)=40°\quad\text{(coincide)} $$

**Margen de estabilidad estática** (línea inductiva equivalente):

$$ \Delta P=P_{max}-P=\frac{1}{X_{pu}}-1=\frac{1}{0.643}-1=0.555\,\text{pu}\;(55.5\%) $$

Un margen del 55% es cómodo para un enlace de 20 km. La norma suele pedir > 20% de margen.

### Paso 3: verificar con Q adicional

Si el parque exporta también \( Q=0.5 \) pu de reactiva inductiva (para controlar la tensión del PCC):

La corriente de línea aumenta: \( I=\sqrt{P^2+Q^2}/V=\sqrt{1+0.25}=1.118 \) pu. La caída de tensión en la reactancia: \( \Delta V_X=X\cdot I\cdot\sin\phi=0.643\cdot1.118\cdot0.447=0.321 \) pu. Tensión en el generador necesaria: \( E=\sqrt{(V+\Delta V_R)^2+\Delta V_X^2}\approx1.35 \) pu — el generador necesita sobre-excitarse un 35%. Si el límite de tensión del generador es 1.1 pu, habrá que reducir la Q exportada o añadir un compensador STATCOM en el PCC.

<div class="cfig"><img src="figuras/transferencia-potencia-linea-analisis.png" alt="P-delta, criterio área igual, perfil de tensión, diagrama P-Q"><div class="cap">(a) Curvas P(δ) y Q(δ) con región estable (δ<90°) e inestable marcadas; Pmax y punto de operación a δ=30°. (b) Criterio de área igual: A1 (aceleración durante falta) ≤ A2 (desaceleración disponible) determina la estabilidad transitoria. (c) Perfil de tensión en línea de 100 km: efecto Ferranti en vacío (tensión sube) y caída de tensión con carga; banda ±5% marcada. (d) Capacidad P-Q del parque 100 MVA: región operativa limitada por corriente máxima, Qmax y Qmin de regulación de tensión.</div></div>

## Cuándo y por qué se usa
En el reparto de carga (droop), en la estabilidad de ángulo de máquinas síncronas y en el diseño del
lazo de sincronización del grid-forming. La derivación \( \partial P/\partial\delta \) del proyecto 01
sale de aquí. La estabilidad transitoria y el criterio de área igual son la base del estudio de
faltas y de la coordinación de protecciones.

## Procedimiento de diseño (genérico)
1. Identifica \( V \), \( E \), \( X \) (y \( R \) si la línea no es predominantemente inductiva) y el ángulo de operación \( \delta_0 \).
2. Calcula \( P(\delta) \) y la rigidez \( \partial P/\partial\delta \) en el punto; verifica margen > 20%.
3. Si la rigidez es excesiva (\( X \) pequeña), añade reactancia (física o virtual) para recuperar margen.
4. Para estabilidad transitoria: calcula \( A_1 \) y verifica \( A_1\leq A_2^{max} \) con el tiempo de despeje del relé.
5. Para línea larga: analiza el perfil de tensión y dimensiona la compensación shunt/serie.

## Ejemplo de código
```python
import numpy as np
# Curva P-delta (linea inductiva pura)
V, E, X = 1.0, 1.0, 0.643          # pu (linea 20 km, base 100 MVA)
delta = np.linspace(0, np.pi/2, 200)
P = V*E/X * np.sin(delta)          # potencia en pu
dPdd = V*E/X * np.cos(delta)       # rigidez sincronizante [pu/rad]

# Angulo de operacion para P=1 pu
P0 = 1.0
delta0 = np.arcsin(P0*X/(V*E))     # 40 grados
margen = (V*E/X - P0)              # 0.555 pu = 55.5%

# Criterio area igual (cortocircuito, P_e_falta=0)
Pm = 0.5; delta_s = np.arcsin(Pm); delta_us = np.pi - delta_s
delta_cl = np.radians(60)          # angulo de despeje
A1 = Pm*(delta_cl - delta_s)
A2 = np.trapz(np.sin(np.linspace(delta_cl, delta_us, 500)) - Pm,
              np.linspace(delta_cl, delta_us, 500))
estable = A1 <= A2
```

## Parámetros y valores típicos
| Magnitud | Valor típico | Condición |
|---|---|---|
| Ángulo de operación | 20°–50° | Líneas de transmisión con margen |
| Potencia máxima | \( P_{max}=EV/X \) | Línea inductiva, \( \delta=90° \) |
| Rigidez sincronizante (GFM 1 MVA) | ≈127 kW/rad | \( X_{virtual}=0.2 \) pu |
| Efecto Ferranti en 200 km | +5–10% tensión | En vacío |
| Tiempo crítico de despeje | 80–150 ms | Máquina síncrona mediana |
| Margen de estabilidad mínimo | >20% de \( P_{max} \) | Criterio N-1 |

## Errores comunes
- Aplicar las fórmulas P-δ / Q-V a una línea **resistiva**: el acoplamiento se invierte (entonces P
  depende de \( V \) y Q de \( \delta \)).
- Olvidar que \( X \) pequeña \( \Rightarrow \) lazo de potencia agresivo e inestable.
- Confundir el ángulo de potencia \( \delta \) con la fase instantánea de la tensión.
- Ignorar la resistencia en redes de distribución (X/R < 2): las fórmulas simplificadas dan errores grandes.
- Aplicar el criterio de área igual solo a la curva de prefalta, sin reconstruir la curva post-falta (que puede ser diferente si se abre una línea).

## Uso en proyectos
- **01 - GFM-Impedance:** la rigidez \( \partial P/\partial\delta \approx 127 \) kW/rad explica la
  inestabilidad del primer diseño; la inductancia virtual la reduce y estabiliza el lazo de potencia.

## Conceptos relacionados
- [[droop-control]] · [[generador-sincrono]] · [[ecuacion-oscilacion]] · [[impedancia-virtual]] · [[grid-forming-vs-following]] · [[red-thevenin-scr]]

## Referencias
- Kundur, *Power System Stability and Control*, McGraw-Hill.
- Bergen, Vittal, *Power Systems Analysis*, Prentice Hall 2000.
- Anderson, Fouad, *Power System Control and Stability*, IEEE Press 2003.
