---
titulo: Modelado de sistemas físicos
slug: modelado-sistemas
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance, 03-DataCenter-IA]
objetivos: [obtener un modelo matematico util de un sistema fisico]
tags: [modelado, ecuaciones, caja-blanca, identificacion, dominios]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-30
relacionados: [variables-estado, representacion-espacio-estados, linealizacion-teoria, marco-dq, convertidor-vsc]
referencias:
  - "Ljung, System Identification, Prentice Hall 1999"
  - "Khalil, Nonlinear Systems, Prentice Hall 2002"
---

## Definición
Construir una descripción matemática que reproduzca el comportamiento **relevante** de un sistema
físico para un propósito concreto (diseñar control, analizar estabilidad, simular). Un modelo no
es "la realidad", es una aproximación útil con un dominio de validez.

## Fundamento teórico
Enfoques según el conocimiento disponible:
- **Caja blanca** (de conocimiento): se derivan las ecuaciones de las leyes físicas
  (balance + leyes constitutivas). Es lo que usamos en convertidores.
- **Caja negra** (identificación): se ajusta un modelo a datos de entrada/salida sin física.
- **Caja gris**: estructura física con parámetros ajustados a datos.

La caja blanca combina:
- **Leyes de balance** (conservación): Kirchhoff de corrientes/tensiones, Newton, balance de energía.
- **Leyes constitutivas** de cada elemento: inductor \( v=L\,\dfrac{di}{dt} \), condensador
  \( i=C\,\dfrac{dv}{dt} \), resistencia \( v=Ri \), inercia \( T=J\,\dfrac{d\omega}{dt} \).
Combinándolas se obtiene un sistema de EDOs \( \dot{\mathbf{x}}=\mathbf{f}(\mathbf{x},\mathbf{u}) \).
La elección de **nivel de abstracción** (qué se desprecia) es la decisión clave: p.ej. modelo
promediado vs conmutado.

<div class="cfig"><img src="figuras/modelado-sistemas-flujo.png" alt="flujo del modelado caja blanca de sistema fisico a modelo lineal"><div class="cap">Flujo del modelado caja blanca: del sistema físico se extraen las leyes de balance y constitutivas, que dan un sistema de EDOs $\dot x=f(x,u)$; se lleva a espacio de estados, se lineliza si el análisis lo requiere y finalmente se valida contra datos o un modelo de mayor fidelidad. La decisión clave es el nivel de abstracción (qué se desprecia).</div></div>

## 1 — El balance genérico: de dónde sale toda EDO de un almacenador
Todas las ecuaciones de estado de la caja blanca tienen la misma raíz: una **ley de balance** sobre una magnitud conservada (carga, flujo, masa, energía, cantidad de movimiento). Vale la pena verlo en forma genérica una vez, porque después la EDO de cualquier inductor, condensador o inercia es un caso particular.

**Paso 1 — enunciar el balance.** Para cualquier magnitud almacenada \( Q \) en un volumen de control, la tasa de acumulación es lo que entra menos lo que sale (más lo que se genera):

$$ \frac{dQ}{dt}=\dot Q_{\text{entra}}-\dot Q_{\text{sale}}+\dot Q_{\text{gen}} $$

Sin generación interna (\( \dot Q_{\text{gen}}=0 \)) queda el balance puro: lo que se acumula es el desbalance de flujos.

**Paso 2 — relacionar \( Q \) con la variable de estado.** Cada almacenador tiene una **ley constitutiva** que liga la magnitud conservada con la variable de energía (el estado):

$$ \text{condensador: } Q=C\,v_C,\qquad \text{inductor: } \lambda=L\,i_L,\qquad \text{inercia: } p=J\,\omega $$

donde \( \lambda \) es el flujo concatenado y \( p \) la cantidad de movimiento angular.

**Paso 3 — derivar con \( C,L,J \) constantes.** Sustituyendo el Paso 2 en el Paso 1 y sacando el parámetro fuera de la derivada:

$$ \frac{d(C\,v_C)}{dt}=C\frac{dv_C}{dt}=i_{\text{entra}}-i_{\text{sale}} \;\Longrightarrow\; \boxed{\;C\frac{dv_C}{dt}=\sum i\;} $$

que es la ley del condensador y, leída como balance de carga, la **Kirchhoff de corrientes** en su nodo. Idéntico procedimiento sobre el flujo da \( L\,di_L/dt=\sum v \) (balance de flujo = Kirchhoff de tensiones de la malla) y sobre la cantidad de movimiento da \( J\,d\omega/dt=\sum T \) (segunda ley de Newton rotacional).

**Paso 4 — apilar todos los almacenadores.** Hay una EDO de primer orden por almacenador independiente; cada flujo (\( \sum i \), \( \sum v \), \( \sum T \)) se expresa con las leyes constitutivas de los elementos disipativos y las variables de estado vecinas. El resultado es el sistema

$$ \dot{\mathbf{x}}=\mathbf{f}(\mathbf{x},\mathbf{u}) $$

Esto explica por qué el **orden = número de almacenadores independientes** (ver [[variables-estado]]): cada balance aporta exactamente una integración. El balance de **energía** \( dE/dt=P_{\text{entra}}-P_{\text{sale}} \) es el mismo principio aplicado a \( E=\sum\frac12 C v^2+\frac12 L i^2+\frac12 J\omega^2 \), y es la forma natural de modelar el bus DC (ver [[dinamica-bus-dc]]).

## Cuándo y por qué se usa
Es el primer paso de todo: sin modelo no hay diseño ni análisis. El nivel del modelo debe
ajustarse al uso (diseño de control → promediado lineal; verificar EMI → conmutado).

## Procedimiento (genérico)
1. Define el **propósito** del modelo y su rango de validez (qué fenómenos debe capturar).
2. Identifica los elementos **almacenadores de energía** (fijan el orden; ver [[variables-estado]]).
3. Aplica leyes de balance + constitutivas → ecuaciones diferenciales.
4. Lleva a forma de estado \( \dot{\mathbf{x}}=\mathbf{f}(\mathbf{x},\mathbf{u}) \) (ver [[representacion-espacio-estados]]).
5. Si hace falta para el análisis lineal, lineliza (ver [[linealizacion-teoria]]).
6. **Valida** el modelo contra datos o un modelo de mayor fidelidad.

## Ejemplo de código
```python
# circuito RLC serie -> dos estados (i del inductor, v del condensador)
def f(x, u):
    i, v = x; Vin = u
    di = (Vin - R*i - v)/L
    dv = i/C
    return [di, dv]
```

## Parámetros y valores típicos
El orden del modelo = nº de almacenadores independientes. Para un filtro LCL por fase: 3
(\( i_{L1}, v_C, i_{L2} \)); en dq, 6.

## Errores comunes
- Modelar con más detalle del necesario para el propósito (lento, frágil).
- No declarar el rango de validez → usar el modelo fuera de donde vale.

## Uso en proyectos
- **01/02**: caja blanca del inversor (LCL + control) en marco dq, nivel promediado, validado
  contra inyección de impedancia y promediado-vs-conmutado.

## 2 — Tipos de modelos

Los modelos se clasifican según la fuente del conocimiento que los genera:

- **Caja blanca (físico):** derivado de primeros principios (leyes de Newton, Kirchhoff, termodinámica). Los parámetros tienen significado físico directo (\( L \), \( C \), \( R \), \( J \)). Es preciso si los parámetros son conocidos con exactitud, pero puede ser costoso de derivar para sistemas complejos.
- **Caja negra (datos):** se ajusta un modelo genérico (ARX, ARMAX, redes neuronales) a datos de entrada-salida medidos. No requiere conocimiento del sistema interno. Es eficiente para sistemas cuya física es compleja, pero queda limitado al rango de datos usados en el ajuste: extrapolación fuera de ese rango no es fiable.
- **Caja gris:** combina estructura física (balances de energía, número de estados) con parámetros identificados experimentalmente. Es el enfoque habitual en convertidores: la estructura dq se conoce de la física, pero las inductancias y resistencias parásitas se miden. Combina robustez del caja blanca con adaptabilidad del caja negra.

La elección del tipo de modelo depende del propósito y de la información disponible. Para diseño de control de convertidores se usa casi siempre caja blanca o caja gris, porque se requiere que el modelo sea válido fuera del punto de operación nominal.

## 3 — Modelado en espacio de estados

La forma canónica para sistemas dinámicos es:

$$ \dot{x} = f(x, u), \qquad y = g(x, u) $$

donde \( x \in \mathbb{R}^n \) es el vector de estado, \( u \in \mathbb{R}^m \) las entradas y \( y \in \mathbb{R}^p \) las salidas. La **elección de variables de estado** es la decisión clave: se debe elegir el conjunto mínimo de variables que describen completamente la energía almacenada en el sistema (y por tanto su historia pasada).

Regla práctica para sistemas eléctricos y electromecánicos:
- **Inductores:** la corriente \( i_L \) es variable de estado (energía magnética \( \frac{1}{2}Li_L^2 \))
- **Condensadores:** la tensión \( v_C \) es variable de estado (energía eléctrica \( \frac{1}{2}Cv_C^2 \))
- **Masas / inercias:** posición y velocidad (energía cinética \( \frac{1}{2}J\omega^2 \))

Para **convertidores** en régimen de conmutación, el modelado directo en variables conmutadas incluye discontinuidades no analíticas. La técnica de **promediado de estado** sustituye las señales conmutadas por su valor medio en un período \( T_s \), obteniendo un modelo diferencial continuo válido para frecuencias \( f \ll f_s \).

## 4 — Modelo promediado de convertidores

El modelo promediado conserva la dinámica de interés (lazos de control a 10–100 Hz) y descarta el rizado de conmutación. Para un buck con ciclo de trabajo \( D \), inductancia \( L \), condensador \( C \) y carga \( R \):

$$ \langle\dot{i}_L\rangle = \frac{D V_{in} - V_o}{L}, \qquad \langle\dot{v}_C\rangle = \frac{i_L - V_o/R}{C} $$

El punto de operación \( (D_0, I_0, V_0) \) se obtiene igualando las derivadas a cero. La linealización alrededor de ese punto (perturbando \( D = D_0 + \hat{d} \), \( i_L = I_0 + \hat{i}_L \), \( v_C = V_0 + \hat{v}_C \)) introduce el término de perturbación de ciclo de trabajo \( V_{in}\hat{d}/L \) en la primera ecuación. El resultado es el modelo en pequeña señal en matrices \( A, B, C, D \) del espacio de estados (ver [[representacion-espacio-estados]]):

$$ \frac{d}{dt}\begin{pmatrix}\hat{i}_L\\\hat{v}_C\end{pmatrix} = \underbrace{\begin{pmatrix}-R_{ESR}/L & -1/L\\ 1/C & -1/(RC)\end{pmatrix}}_{A} \begin{pmatrix}\hat{i}_L\\\hat{v}_C\end{pmatrix} + \underbrace{\begin{pmatrix}V_{in}/L\\ 0\end{pmatrix}}_{B} \hat{d} $$

donde se ha incluido la resistencia de serie del inductor \( R_{ESR} \) como perturbación de primer orden. La función de transferencia control-a-salida \( G_{vd}(s) = \hat{v}_C/\hat{d} \) se obtiene directamente de \( C(sI-A)^{-1}B + D \).

## 5 — Identificación experimental

Cuando el modelo físico no es suficientemente preciso (parámetros inciertos, no linealidades no modeladas), se complementa con identificación experimental:

- **Respuesta al escalón:** se aplica un escalón de entrada y se mide la salida. Para un sistema de segundo orden se estiman \( K \) (ganancia DC), \( \omega_n \) (de la frecuencia de oscilación) y \( \zeta \) (del sobreimpulso o del tiempo de establecimiento).
- **Análisis de respuesta en frecuencia (FRA):** barrido sinusoidal en frecuencia → Bode experimental. Es el método de referencia para identificar la impedancia de convertidores (ver [[medicion-impedancia-inyeccion]]).
- **Mínimos cuadrados recursivos:** actualización online de los parámetros del modelo ante cambios lentos del sistema (temperatura, envejecimiento). El estimador actualiza el vector de parámetros \( \hat{\theta} \) cada muestra con la ganancia de Kalman discreta.
- **Criterio de bondad:** \( R^2 = 1 - \text{SSR}/\text{SST} > 0.95 \) y error de predicción \( < 5\,\% \) del rango dinámico de la señal medida son requisitos mínimos para dar el modelo por válido.

## 6 — Validación del modelo

Un modelo se *ajusta* con un conjunto de datos y se *valida* con otro independiente. Los pasos:

1. **Prueba cruzada (*cross-validation*):** ajustar con el *dataset* A (p. ej., escalones de carga), validar con el *dataset* B (p. ej., escalones de referencia). Si el modelo solo es bueno en A, está sobreajustado.
2. **Comparación de respuesta al escalón:** superposición del modelo frente al sistema real — diferencia pico máxima \( < 10\,\% \) del valor final.
3. **Análisis de residuos:** el error \( e(t) = y_{real}(t) - y_{modelo}(t) \) debe ser ruido blanco (sin autocorrelación significativa), lo que indica que el modelo ha capturado toda la dinámica determinista.
4. **Límites de validez:** el modelo linealizado es fiable en una región pequeña alrededor del punto de operación donde se identificó. Extrapolar a puntos de operación alejados (arranque, cortocircuito) requiere modelos no lineales o gain scheduling (ver [[gain-scheduling]]).

<div class="cfig"><img src="../figuras/modelado-sistemas-analisis.png" alt="Modelado de sistemas: ciclo, promediado, validación y compromiso complejidad-generalización"><div class="cap">Cuatro paneles: ciclo completo de modelado desde el sistema real hasta la validación; señal conmutada de buck frente a su modelo promediado; comparación de la respuesta al escalón del modelo frente a medidas reales; curva de compromiso entre complejidad del modelo y precisión en entrenamiento vs validación (sobreajuste).</div></div>

## Conceptos relacionados
- [[variables-estado]] · [[representacion-espacio-estados]] · [[linealizacion-teoria]] · [[convertidor-vsc|modelo promediado]]

## Referencias
- Khalil, *Nonlinear Systems*, 2002 · Ljung, *System Identification*, 1999.
