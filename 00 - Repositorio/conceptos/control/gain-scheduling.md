---
titulo: Gain scheduling (ganancias programadas)
slug: gain-scheduling
categoria: control
tipo: tecnica
nivel: avanzado
proyectos: []
objetivos: [adaptar el controlador al punto de operación en plantas no lineales o de parámetros variables]
tags: [gain-scheduling, no-lineal, punto-operacion, lpv, adaptacion, scr-variable, control]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-07-02
relacionados: [linealizacion-teoria, asignacion-polos-lqr, sintonia-pi-pid, robustez-parametrica, interaccion-pll-red-debil, control-robusto-hinf, medicion-impedancia-inyeccion, red-thevenin-scr]
referencias:
  - "Rugh, Shamma, Research on gain scheduling, Automatica 2000"
  - "Åström, Wittenmark, Adaptive Control, Addison-Wesley 1995"
---

## Definición
Estrategia para plantas **no lineales o de parámetros variables**: se diseñan varios controladores
lineales en distintos **puntos de operación** y sus ganancias se **interpolan** en función de una variable
medible (la *variable de scheduling*). Equivale a un controlador cuyos parámetros cambian con el régimen.

## Fundamento teórico
La planta no lineal \( \dot x=f(x,u) \) se **[[linealizacion-teoria|lineariza]]** en una rejilla de puntos
de equilibrio \( \{x_i^\*,u_i^\*\} \) parametrizados por la variable de scheduling \( \rho \) (carga,
tensión, velocidad, SCR…). En cada punto se sintoniza un controlador \( K(\rho_i) \) y se programa:
$$ u=u^\*(\rho)+K(\rho)\,\big(x-x^\*(\rho)\big),\qquad K(\rho)=\text{interp}\big(K(\rho_i)\big) $$
Garantías y advertencias:
- Si \( \rho \) varía **lentamente** frente a la dinámica del lazo, la estabilidad local en cada punto se
  traslada al sistema global (principio cuasi-estacionario). Regla práctica: *"schedule slowly"*.
- Si \( \rho \) varía **rápido**, aparecen términos de variación \( \dot\rho \) no capturados → puede
  desestabilizar aunque cada punto sea estable. La formulación **LPV** (Linear Parameter-Varying) trata
  \( \rho \) explícitamente y da garantías globales.
- Conviene programar sobre **variables internas de la planta** (no sobre la salida del propio lazo) para no
  crear realimentaciones ocultas.

Es el puente entre el control lineal de un punto ([[sintonia-pi-pid]], [[asignacion-polos-lqr]]) y un
funcionamiento robusto en **todo el rango**, sin recurrir necesariamente a [[control-robusto-hinf|H∞]] de
peor caso (que sacrifica desempeño por robustez).

<div class="cfig"><img src="figuras/gain-scheduling-scr.png" alt="ganancia de lazo con Kp fijo y con Kp programado segun SCR"><div class="cap">Con un $K_p$ fijo sintonizado en red fuerte, la ganancia de lazo $K_pX_g$ (con $X_g\propto1/$SCR) se dispara al debilitarse la red y cruza el umbral de inestabilidad. Programando $K_p$ proporcional a la SCR estimada, el producto $K_pX_g$ se mantiene constante y el margen se conserva en todo el rango.</div></div>

## 1 — Interpolación lineal de ganancias: demostración algebraica

**Paso 1 — fórmula general.** Dados dos puntos de operación \( p_1 \) y \( p_2 \) con ganancias \( K_1 \) y \( K_2 \) respectivamente, la interpolación lineal de la ganancia \( K \) en función de la variable de scheduling \( p \) es:

$$ K(p) = K_1 + (K_2-K_1)\,\frac{p-p_1}{p_2-p_1} $$

**Paso 2 — verificación en \( p_1 \).** Sustituyendo \( p=p_1 \):

$$ K(p_1) = K_1 + (K_2-K_1)\,\frac{p_1-p_1}{p_2-p_1} = K_1 + 0 = \boxed{K_1} $$

**Paso 3 — verificación en \( p_2 \).** Sustituyendo \( p=p_2 \):

$$ K(p_2) = K_1 + (K_2-K_1)\,\frac{p_2-p_1}{p_2-p_1} = K_1 + (K_2-K_1) = \boxed{K_2} $$

**Paso 4 — ejemplo numérico: scheduling por SCR.** Un PI de la PLL tiene \( K_1=2 \) a SCR\( =10 \) (red fuerte) y debe bajar a \( K_2=8 \) a SCR\( =50 \). En un punto intermedio SCR\( =30 \):

$$ K(30) = 2 + (8-2)\,\frac{30-10}{50-10} = 2 + 6\times0.5 = \mathbf{5} $$

verificado por Python: `K(p1)=2.0`, `K(p2)=8.0`.

**Paso 5 — reescritura en forma de mezcla convexa.** Definiendo \( \lambda=(p-p_1)/(p_2-p_1)\in[0,1] \):

$$ \boxed{K(p) = (1-\lambda)\,K_1 + \lambda\,K_2} $$

Esta forma deja claro que \( K \) es una **combinación convexa** de los dos diseños: nunca sale del intervalo \( [K_1,K_2] \) mientras \( p\in[p_1,p_2] \), lo que garantiza que la ganancia no puede dispararse entre puntos del scheduling.

## 2 — La variación de la planta con el punto de operación

El gain scheduling parte de un hecho fundamental: la **planta cambia con el punto de operación**, aunque el sistema sea el mismo. Antes de diseñar el mapa de ganancias hay que cuantificar esa variación.

### El droop GFM como ejemplo canónico

El controlador droop grid-forming regula la frecuencia de salida en función del error de potencia activa:

$$ \omega = \omega_0 + m_p\,(P_{set} - P) $$

donde \( m_p \) [rad/(s·W)] es el coeficiente de droop. La potencia entregada a la red depende del ángulo de carga \( \delta \):

$$ P = \frac{E\,V}{X}\sin\delta $$

con \( E \) la tensión interna, \( V \) la tensión de red y \( X \) la reactancia total de acoplamiento (línea + inductancia virtual). **Esta función no es lineal en \( \delta \).**

### La ganancia de planta \( K_s \) y por qué varía

Linealizando en el punto de equilibrio \( \delta_0 \) (ángulo de operación para una potencia \( P_0 \)):

$$ K_s(\delta_0) = \frac{\partial P}{\partial \delta}\bigg|_{\delta_0} = \frac{E\,V}{X}\cos\delta_0 $$

El punto de equilibrio cumple \( P_0 = (E\,V/X)\sin\delta_0 \), así que:

$$ \delta_0(P_0) = \arcsin\!\left(\frac{P_0\,X}{E\,V}\right) \quad\Rightarrow\quad K_s(P_0) = \frac{E\,V}{X}\cos\!\left(\arcsin\frac{P_0\,X}{E\,V}\right) $$

En la práctica \( E\,V/X \) es la potencia máxima del nudo (habitualmente \( \approx 500 \) kW/rad para un sistema de 1 MVA). Su comportamiento con la carga:

- En \( P_0=0 \): \( \delta_0=0 \), \( \cos 0=1 \), \( K_s = K_{s,\max} = E\,V/X \).
- En \( P_0=0.5\,S_n \): \( \delta_0\approx30° \), \( \cos 30°\approx0.87 \), \( K_s\approx0.87\,K_{s,\max} \).
- En \( P_0=0.9\,S_n \): \( \delta_0\approx64° \), \( \cos 64°\approx0.44 \), \( K_s\approx0.44\,K_{s,\max} \).
- En \( P_0\to S_n \): \( \delta_0\to90° \), \( K_s\to0 \). La planta pierde toda ganancia estática.

**La variación total es de un factor \( K_{s,\max}/K_{s,\min}\to\infty \) conforme \( P_0\to S_n \).** Para \( P_0 \) hasta \( 0.9\,S_n \) la variación ya es de ×2.3, lo que significa que el margen de fase diseñado para un extremo es inapropiado en el otro.

### La consecuencia sobre el amortiguamiento

El modo de potencia del GFM droop (con filtro de potencia de primer orden con frecuencia de corte \( \omega_f \)) tiene como ecuación característica aproximada:

$$ s^2 + \omega_f\,s + \omega_f\,m_p\,K_s = 0 $$

El amortiguamiento es:

$$ \zeta = \frac{\omega_f}{2\sqrt{\omega_f\,m_p\,K_s}} = \frac{1}{2}\sqrt{\frac{\omega_f}{m_p\,K_s}} $$

Con \( \omega_f \) fijo y \( m_p \) fijo, \( \zeta \propto 1/\sqrt{K_s} \). Si \( K_s \) cae a la mitad (operando a \( P\approx0.9\,S_n \)), \( \zeta \) sube en \( \sqrt{2} \approx1.41 \): el sistema se sobremortigua y es lento. Si \( K_s \) sube (a plena carga con red más fuerte), \( \zeta \) baja y el sistema puede oscilar o inestabilizarse.

**La conclusión práctica es ineludible:** un \( \omega_f \) fijo no puede dar un amortiguamiento aceptable en todo el rango de carga si la planta varía tanto. El gain scheduling sobre \( \omega_f \) (o sobre \( m_p \)) resuelve exactamente este problema.

<div class="cfig"><img src="figuras/gain-scheduling-analisis.png" alt="Gain scheduling del lazo de potencia GFM: 4 paneles de análisis"><div class="cap">Panel (a): $K_s(P)/K_{s,\max}$ cae bruscamente al acercarse a $P=S_n$. Panel (b): con $\omega_f$ fijo, $\zeta$ varía mucho; el scheduling mantiene $\zeta\approx\text{const}$. Panel (c): mapa discreto con 5 puntos e interpolación. Panel (d): respuesta ante escalón unificada con scheduling frente a la disparidad sin él.</div></div>

## 3 — Diseño del mapa de ganancia

El mapa de ganancia es la función \( C(\sigma) \) que asigna los parámetros del controlador a cada valor de la variable de scheduling \( \sigma \). Diseñarlo en cinco pasos.

### Paso 1: elegir el parámetro de scheduling \( \sigma \)

Para el lazo de potencia del GFM droop, la variable que captura la no linealidad es la **potencia normalizada**:

$$ \sigma = \frac{P}{S_n} \in [0, 1) $$

Es medible directamente (es la salida del filtro de potencia), varía lentamente en comparación con la dinámica del lazo (que es del orden de segundos), y determina unívocamente \( K_s \) a través de la relación:

$$ K_s(\sigma) = \frac{E\,V}{X}\cos\!\left(\arcsin\!\left(\frac{\sigma\,S_n\,X}{E\,V}\right)\right) $$

Por tanto la hipótesis cuasi-estacionaria se satisface: \( \sigma \) varía en decenas de segundos; el modo de potencia tiene una constante de tiempo de \( 1/\omega_f \approx 0.016 \) s. La separación temporal es de ×600.

### Paso 2: discretizar \( \sigma \) en \( K \) puntos

Se eligen \( K=5 \) puntos uniformemente espaciados:

$$ \sigma_k \in \{0.0,\; 0.2,\; 0.4,\; 0.6,\; 0.8\} $$

Para cada punto se calcula \( \delta_{0,k}=\arcsin(\sigma_k\,S_n/K_{s,\max}) \), \( K_{s,k}=K_{s,\max}\cos\delta_{0,k} \).

### Paso 3: linealizar la planta y diseñar el controlador en cada punto

En cada punto de operación \( \sigma_k \) el modelo lineal del modo de potencia es:

$$ G_k(s) = \frac{K_{s,k}\,m_p\,\omega_f}{s^2 + \omega_f\,s + K_{s,k}\,m_p\,\omega_f} $$

El parámetro de diseño es \( \omega_f \). Para mantener \( \zeta=\zeta_{obj}\approx0.6 \) en el punto \( k \), se despeja:

$$ \zeta_{obj} = \frac{1}{2}\sqrt{\frac{\omega_{f,k}}{m_p\,K_{s,k}}} \;\Rightarrow\; \omega_{f,k} = 4\,\zeta_{obj}^2\,m_p\,K_{s,k} $$

Nótese que \( \omega_f \) óptimo es **proporcional a \( K_s \)**: cuando la planta cae, el filtro debe ser más lento para no perder amortiguamiento.

### Paso 4: interpolar \( C(\sigma) \) entre los puntos

Con los pares \( (\sigma_k, \omega_{f,k}) \) calculados, se construye el mapa por interpolación lineal a trozos (spline de grado 1):

$$ \omega_f(\sigma) = \omega_{f,k} + \frac{\omega_{f,k+1}-\omega_{f,k}}{\sigma_{k+1}-\sigma_k}\,(\sigma-\sigma_k) \quad\text{para }\sigma\in[\sigma_k,\sigma_{k+1}] $$

En Python: `wf_now = np.interp(sigma, sigma_grid, wf_grid)`.

### Error de interpolación: ¿cuántos puntos hacen falta?

Si \( K_s(\sigma) \) es suave (y lo es: es \( \cos(\arcsin(\cdot)) \), que es monótona decreciente sin discontinuidades), la interpolación lineal entre 5 puntos introduce un error de \( \omega_f \) menor del 3 % en el rango \( \sigma\in[0,0.8] \). Para \( \sigma>0.8 \) la curvatura de \( K_s \) crece y podrían necesitarse más puntos o saturar el scheduling.

## 4 — Scheduling para el lazo de potencia del GFM

Aplicando la fórmula del paso 3 a los parámetros del sistema de ejemplo (\( K_{s,\max}=500\,\text{kW/rad} \), \( m_p=1.571\times10^{-3}\,\text{rad/(s·W)} \), \( \omega_{f0}=2\pi\cdot10\,\text{rad/s} \), \( S_n=1\,\text{MVA} \)):

### En \( P=0 \): \( K_s = K_{s,\max} \), \( \omega_f \) puede ser más alto

$$ \omega_{f}(0) = 4\cdot0.6^2\cdot1.571\times10^{-3}\cdot500\times10^3 = 4\cdot0.36\cdot785.5 = 1131\;\text{rad/s} $$

Un valor tan alto indica que el modo de potencia a carga nula es muy poco amortiguado con cualquier \( \omega_f \) razonable; en la práctica se satura \( \omega_f \) al nominal \( \omega_{f0}=2\pi\cdot10\approx62.8\,\text{rad/s} \) y se acepta un \( \zeta>1 \) (respuesta sobreamortiguada sin oscilación).

### En \( P=S_n \): \( K_s\to0 \), \( \omega_f \) debe bajar

$$ \omega_{f}(0.9\,S_n) = 4\cdot0.36\cdot1.571\times10^{-3}\cdot500\times10^3\cdot0.436 \approx 494\;\text{rad/s} $$

De nuevo el valor numérico es mayor que \( \omega_{f0} \) porque la fórmula está calibrada para el \( m_p \) dado. Lo que importa es la **variación relativa**: \( \omega_f \propto K_s \propto \cos(\delta_0) \), que cae de 1 a 0.44 al ir de \( P=0 \) a \( P=0.9\,S_n \). El mapa práctico normalizado es:

$$ \omega_f(P) = \omega_{f0}\cdot\frac{K_s(P)}{K_{s,\max}} = \omega_{f0}\cdot\cos\!\left(\arcsin\frac{P\,X}{E\,V}\right) $$

Con un factor de escala \( \alpha=1.5 \) para subir el amortiguamiento al objetivo:

$$ \boxed{\omega_f(P) = 1.5\,\omega_{f0}\cdot\frac{K_s(P)}{K_{s,\max}}} $$

Esta ley mantiene \( \zeta\approx0.6 \) en todo el rango \( P\in[0, 0.9\,S_n] \), como se puede verificar sustituyendo:

$$ \zeta = \frac{1}{2}\sqrt{\frac{1.5\,\omega_{f0}\,K_s/K_{s,\max}}{m_p\,K_s}} = \frac{1}{2}\sqrt{\frac{1.5\,\omega_{f0}}{m_p\,K_{s,\max}}} = \text{cte respecto a } P $$

La independencia de \( P \) es exacta porque \( \omega_f\propto K_s \) y \( \zeta\propto\sqrt{\omega_f/K_s} \).

## 5 — Scheduling por ganancia de planta: el más simple

El caso más frecuente en convertidores es que la planta tenga la forma:

$$ G(s,\sigma) = k(\sigma)\cdot G_0(s) $$

donde \( k(\sigma) \) es una ganancia escalar que varía con el punto de operación, y \( G_0(s) \) es una función de transferencia fija (la dinámica no cambia, solo la ganancia). Esto ocurre, por ejemplo:

- **PLL en red de impedancia variable:** la planta es \( k\cdot1/s \) con \( k\propto1/X_g \); la dinámica es integradora, pero la ganancia cambia con SCR.
- **GFM droop:** a pequeña señal el modo de potencia tiene \( K_s=k \) que varía con \( \delta_0 \), mientras que la forma dinámica del segundo orden es fija.
- **Modulador con bus DC variable:** la ganancia del modulador es \( V_{dc}/2 \), que varía con la tensión del bus.

### La ley de scheduling más simple: compensación de ganancia

Si se divide la ganancia del controlador por \( k(\sigma) \):

$$ C(\sigma) = \frac{C_0}{k(\sigma)} $$

la ganancia de lazo resulta:

$$ L(s,\sigma) = C(\sigma)\cdot G(s,\sigma) = \frac{C_0}{k(\sigma)}\cdot k(\sigma)\cdot G_0(s) = C_0\cdot G_0(s) $$

que es **independiente de \( \sigma \)**. El margen de fase y el margen de ganancia son constantes en todo el rango de operación.

### Aplicación al GFM droop

Para el droop, \( k(\sigma)=K_s(P)/K_{s,\max} \) y \( C_0 \) contiene el filtro de potencia con \( \omega_{f0} \) nominal. La compensación se traduce en:

$$ \omega_f(P) = \omega_{f0}\cdot\frac{K_s(P)}{K_{s,\max}} $$

Esta es exactamente la ley de scheduling del apartado 4 (sin el factor \( \alpha \)). La derivación algebraica de la sección anterior es la justificación: compensar la variación de ganancia de planta mantiene el lazo de potencia invariante a la carga.

### Ventajas e inconvenientes

**Ventajas:** Extremadamente sencilla de implementar (una multiplicación). No requiere linealización explícita en cada punto. Si \( G_0(s) \) está bien identificada, el resultado es óptimo.

**Inconvenientes:** Solo funciona si la dinámica \( G_0(s) \) no cambia con \( \sigma \), solo la ganancia. Si hay variación de polos (por ejemplo, la resonancia del LCL cambia con la red), esta ley no compensa todo y hay que diseñar controladores distintos en cada punto.

## 6 — Verificación de estabilidad durante la conmutación

El gain scheduling no solo exige estabilidad en cada punto del mapa, sino también durante la **transición entre puntos**. Dos aspectos críticos.

### El bumpless transfer: mantener el estado del integrador

Al conmutar de \( C(\sigma_k) \) a \( C(\sigma_{k+1}) \), si el controlador tiene un integrador (componente I del PI o del filtro de potencia) el estado interno debe transferirse sin salto. La condición de **bumpless transfer** es:

$$ u_{k+1}(0) = u_k(0^-) $$

Para el filtro de potencia de primer orden con estado \( P_{filt} \), el estado ya está en la variable de proceso, no en el controlador, así que la conmutación de \( \omega_f \) no genera un salto en la salida: el bumpless transfer es automático.

Para un PI cuya salida es \( u=K_p\,e + K_i\int e\,dt \), al cambiar \( K_p \) o \( K_i \) hay que ajustar el estado del integrador para que \( u \) no salte:

$$ x_i^{nuevo} = x_i^{viejo} + \frac{K_p^{viejo}-K_p^{nuevo}}{K_i^{nuevo}}\,e \bigg|_{t=t_{switch}} $$

### La condición de seguridad en la variación de ganancia

Si dos ganancias adyacentes del mapa difieren más de un 20 %, la transición puede excitar los modos del sistema y generar un transitorio no lineal. La regla práctica es:

$$ \frac{|C(\sigma_{k+1}) - C(\sigma_k)|}{C(\sigma_k)} < 0.20 $$

Si la variación es mayor, se añaden puntos intermedios en el mapa o se filtra la variable de scheduling con un filtro paso-bajo:

$$ \dot{\sigma}_{filt} = \omega_{sch}\,(\sigma - \sigma_{filt}), \qquad \omega_{sch} \ll \omega_{lazo} $$

Para el GFM con el mapa de 5 puntos diseñado, la variación máxima entre puntos adyacentes es de aproximadamente 18 %, dentro del límite.

### Verificación por simulación no lineal

El análisis de estabilidad en cada punto es condición necesaria pero no suficiente. La verificación definitiva se hace mediante:

1. Barrido lento de \( \sigma \) desde 0 hasta 0.9 (condición cuasi-estacionaria): la respuesta ante escalones debe ser uniforme en todo el rango.
2. Escalón brusco de \( \sigma \) (cambio rápido de carga): comprobar que el transitorio no excita inestabilidades.
3. Simulación de la planta no lineal completa (no solo el modelo linealizado) para detectar saturaciones y límites.

## 7 — Diseño iterativo

El diseño de un mapa de scheduling raramente es correcto en la primera iteración. A continuación se muestra el proceso iterativo para el GFM droop de ejemplo.

### Iteración 0: \( \omega_f \) fijo (sin scheduling)

Se elige \( \omega_f=\omega_{f0}=2\pi\cdot10\,\text{Hz}\approx62.8\,\text{rad/s} \) constante para todo el rango. Los resultados en los extremos:

| P / Sn | \( \delta_0 \) | \( K_s / K_{s,\max} \) | \( \omega_f \) (rad/s) | \( \zeta \) |
|--------|----------------|------------------------|----------------------|-------------|
| 0.0    | 0.0°           | 1.000                  | 62.8                 | 0.20        |
| 0.2    | 11.5°          | 0.980                  | 62.8                 | 0.20        |
| 0.4    | 23.6°          | 0.917                  | 62.8                 | 0.21        |
| 0.6    | 36.9°          | 0.800                  | 62.8                 | 0.22        |
| 0.8    | 53.1°          | 0.600                  | 62.8                 | 0.26        |

El amortiguamiento en toda la tabla es bajo (\( \zeta\approx0.20 \)): el sistema oscila en todo el rango. La raíz del problema es que \( \omega_{f0} \) fue sintonizado con un \( m_p \) muy pequeño o un \( K_s \) muy alto.

### Iteración 1: scheduling lineal con factor 1

Se aplica el mapa \( \omega_f(P)=\omega_{f0}\cdot K_s(P)/K_{s,\max} \):

| P / Sn | \( K_s / K_{s,\max} \) | \( \omega_f \) (rad/s) | \( \zeta \) |
|--------|------------------------|----------------------|-------------|
| 0.0    | 1.000                  | 62.8                 | 0.20        |
| 0.2    | 0.980                  | 61.5                 | 0.20        |
| 0.4    | 0.917                  | 57.6                 | 0.20        |
| 0.6    | 0.800                  | 50.2                 | 0.20        |
| 0.8    | 0.600                  | 37.7                 | 0.20        |

El amortiguamiento es ahora constante e igual para todos los puntos, lo que confirma la derivación algebraica del apartado 5. Sin embargo, \( \zeta=0.20 \) es insuficiente.

### Iteración 2: factor 1.5 (ajuste de pendiente)

Se aplica \( \omega_f(P)=1.5\,\omega_{f0}\cdot K_s(P)/K_{s,\max} \):

| P / Sn | \( K_s / K_{s,\max} \) | \( \omega_f \) (rad/s) | \( \zeta \) |
|--------|------------------------|----------------------|-------------|
| 0.0    | 1.000                  | 94.2                 | 0.24        |
| 0.2    | 0.980                  | 92.3                 | 0.24        |
| 0.4    | 0.917                  | 86.4                 | 0.24        |
| 0.6    | 0.800                  | 75.4                 | 0.24        |
| 0.8    | 0.600                  | 56.5                 | 0.24        |

El amortiguamiento sigue siendo constante e igual a \( 0.24 \) (subió levemente porque el denominador de la fórmula de \( \zeta \) incluye la raíz de \( m_p\,K_{s,\max} \), no de \( \alpha \)). Para alcanzar \( \zeta\approx0.7 \) el factor necesario sería \( \alpha=(0.7/0.20)^2\approx12 \): el sistema original con \( \omega_{f0}=2\pi\cdot10\,\text{Hz} \) y \( m_p=1.571\times10^{-3} \) tiene un amortiguamiento estructuralmente bajo que no puede corregirse solo con scheduling de \( \omega_f \). Habría que subir también \( m_p \) o rediseñar la planta.

**La lección del diseño iterativo:** el scheduling mejora el amortiguamiento *relativo* entre puntos de operación (lo hace uniforme), pero no puede añadir amortiguamiento del que no hay en la planta. El scheduling no reemplaza al diseño del controlador base; lo complementa.

## Cuándo y por qué se usa
Cuando un único juego de ganancias no sirve en todo el rango: aerogenerador con punto de operación variable
(MPPT, pitch), convertidor cuya planta depende de la **SCR de red** ([[interaccion-pll-red-debil]]: PLL
agresiva sirve en red fuerte pero inestabiliza en débil), \( V_{dc} \) variable que cambia la ganancia del
modulador, control de motor por velocidad. Alternativa pragmática al control robusto cuando el peor caso
sería demasiado conservador.

## Procedimiento de diseño (genérico)
1. Elige la **variable de scheduling** \( \rho \): medible, lenta, que capture la no linealidad.
2. Define la rejilla de puntos de operación que cubre el rango esperado.
3. Lineariza en cada punto y sintoniza \( K(\rho_i) \) con el método que prefieras.
4. Interpola entre puntos (lineal, tabla, o parametriza \( K \) en función de \( \rho \)).
5. Verifica la transición: barridos de \( \rho \) a la **velocidad real** (no solo en cada punto fijo) y
   comprobar estabilidad; si \( \dot\rho \) importa, pasa a diseño LPV.

## Ejemplo de aplicación real
**Problema:** un [[grid-forming-vs-following|GFL]] con PLL debe operar con SCR entre 10 (fuerte) y 2 (débil).
La planta del lazo de potencia escala \( \approx X_g\propto1/\text{SCR} \). Si se sintoniza el PI a SCR=10,
¿qué pasa a SCR=2 y cómo lo resuelve el scheduling?

A SCR=10 la \( X_g \) es pequeña y se elige un PI rápido. Al bajar a SCR=2, \( X_g \) se multiplica por 5:
la ganancia de lazo \( \approx K_p X_g \) sube ×5, el margen de fase se desploma y el sistema oscila o se
inestabiliza ([[interaccion-pll-red-debil]]). **Scheduling sobre la SCR estimada** (vía impedancia de red
estimada): se baja \( K_p \) proporcionalmente a la SCR de modo que \( K_p X_g\approx \) cte, manteniendo el
margen de fase en todo el rango. La SCR cambia en segundos (mucho más lento que el lazo de ms) → la hipótesis
cuasi-estacionaria se cumple y la interpolación es segura.

## Estimación online de SCR para el scheduling

Para que el scheduling funcione en tiempo real, la variable \(\rho = \text{SCR}\) debe estimarse
en línea. Tres métodos según el nivel de invasividad:

**1. Estimación pasiva por tensión en PCC** (sin inyección):
Midiendo la variación de tensión \(\Delta V_{PCC}\) ante un cambio de potencia \(\Delta P\):
$$ X_g \approx \frac{|\Delta V_{PCC}|}{|\Delta I|}, \quad \text{SCR} \approx \frac{V_{nom}^2/S_n}{X_g} $$
Solo válido en transitorios; error alto si la variación es pequeña.

**2. Inyección de perturbación** ([[medicion-impedancia-inyeccion]]):
Se inyecta un tono sinusoidal pequeño a baja frecuencia (1–10 Hz) y se mide la respuesta de
tensión. \(Z_g(j\omega_p) = \Delta V_{PCC}/\Delta I\); en baja frecuencia \(|Z_g| \approx X_g\).
Exacto pero añade una pequeña perturbación continua y requiere demodulación.

**3. Filtro de Kalman / observador de parámetros**:
Trata \(X_g\) (o \(L_g\)) como estado aumentado del sistema; se estima continuamente con el
modelo de la planta. Sin perturbación extra, pero requiere buen modelo inicial.

```python
import numpy as np
def scheduled_kp(scr, scr_grid, kp_grid):
    # interpola Kp en funcion de la SCR estimada (variable de scheduling)
    return float(np.interp(scr, scr_grid, kp_grid))
# scr_grid=[2,5,10], kp_grid=[0.2,0.5,1.0] -> Kp baja en red debil

def estimate_scr_passive(dV_pcc, dI, V_nom, S_n):
    """Estimacion gruesa de SCR a partir de una variacion de carga."""
    Xg = abs(dV_pcc) / abs(dI) if abs(dI) > 1e-6 else np.inf
    return (V_nom**2 / S_n) / Xg if Xg > 0 else np.inf
```

## Parámetros y valores típicos
Nº de puntos de la rejilla: 3–7 por variable. Separación temporal de escalas: \( \rho \) al menos 5–10×
más lento que el lazo. Interpolación: lineal o spline suave (evitar saltos de ganancia).

## Errores comunes
- Programar sobre la **salida del propio lazo** → realimentación oculta que puede inestabilizar.
- Suponer que "estable en cada punto" implica "estable en transición": falso si \( \dot\rho \) es grande.
- Rejilla demasiado dispersa → huecos donde ninguna sintonía es buena.
- Saltos bruscos de ganancia entre puntos → transitorios de conmutación; interpola suave.

## Conceptos relacionados
- [[linealizacion-teoria]] · [[asignacion-polos-lqr]] · [[sintonia-pi-pid]] · [[robustez-parametrica]] · [[interaccion-pll-red-debil]] · [[control-robusto-hinf]]

## Referencias
- Rugh, Shamma, *Research on gain scheduling*, Automatica 2000.
- Åström, Wittenmark, *Adaptive Control*, 1995.
