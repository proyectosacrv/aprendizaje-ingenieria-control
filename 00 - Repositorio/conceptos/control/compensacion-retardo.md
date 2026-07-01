---
titulo: Compensación de retardo (Smith predictor, retardo digital)
slug: compensacion-retardo
categoria: control
tipo: tecnica
nivel: intermedio
proyectos: []
objetivos: [recuperar margen y desempeño perdidos por el retardo de cómputo y PWM]
tags: [retardo, smith-predictor, computo, pwm, prediccion, fase, intermedio, control]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-30
relacionados: [discretizacion-controladores, margenes-estabilidad, desacoplo-dq, fenomenos-oscilatorios-red, controlador-pid]
referencias:
  - "Buso, Mattavelli, Digital Control in Power Electronics, Morgan & Claypool 2006"
  - "Åström, Hägglund, Advanced PID Control, ISA 2006"
---

## Definición
Conjunto de técnicas para **contrarrestar el efecto desestabilizador del retardo** del control
digital (cómputo + modulación), que resta fase y limita el ancho de banda. Incluye la predicción de
estados y el **predictor de Smith** para retardos dominantes.

## Fundamento teórico
En un convertidor digital el retardo total es típicamente \( T_d\approx1.5\,T_s \) (un periodo de
cómputo + medio de PWM/ZOH). Su efecto en frecuencia es fase pura:
$$ e^{-sT_d}\ \Rightarrow\ \Delta\phi(\omega)=-\omega T_d $$
que **resta margen de fase** proporcional a \( \omega_c \) y empuja la impedancia hacia la
no-pasividad ([[fenomenos-oscilatorios-red|estabilidad armónica]]). Compensaciones:
- **Predicción de estados / corriente:** estimar el valor de la variable \( T_d \) por delante
  (modelo del filtro, observador) y controlar sobre la predicción → cancela el retardo dentro de la
  banda del modelo.
- **Predictor de Smith:** para una planta \( G(s)e^{-sT_d} \), realimenta una predicción **sin
  retardo** usando un modelo \( \hat G \):
  $$ C_{eq}(s)=\frac{C(s)}{1+C(s)\hat G(s)\,(1-e^{-sT_d})} $$
  Así el controlador "ve" \( \hat G(s) \) sin retardo y se sintoniza como si no lo hubiera; el
  retardo queda fuera del lazo característico (si el modelo es exacto).
- **Adelanto de ángulo:** en dq, rotar la referencia/medida \( \omega T_d \) compensa el giro del
  marco durante el retardo (mejora el [[desacoplo-dq|desacoplo]]).

Limitación: todas dependen de la **exactitud del modelo**; un \( \hat G \) o \( T_d \) erróneo
reintroduce error y puede empeorar la robustez.

<div class="cfig"><img src="figuras/compensacion-retardo-fase.png" alt="fase restada por el retardo en funcion de la frecuencia"><div class="cap">El retardo $T_d=1.5\,T_s$ resta fase pura $\Delta\phi=-\omega T_d$, que crece linealmente con la frecuencia. A la frecuencia de cruce $f_c=f_s/10$ ya se pierden ~54° de margen: por eso en lazos rápidos hay que compensarlo (predicción de estados, Smith, adelanto de ángulo).</div></div>

## 1 — De dónde sale \( e^{-sT_d} \) y la pérdida de fase \( -\omega T_d \)
**Paso 1 — el retardo en el tiempo.** El control digital aplica la acción calculada con un retraso \( T_d \): la medida del instante \( t \) no se actúa hasta \( t+T_d \). En el dominio del tiempo, retrasar una señal \( x(t) \) en \( T_d \) es \( x(t-T_d) \).

**Paso 2 — su transformada de Laplace.** Aplicando la definición \( \mathcal{L}\{x(t-T_d)\}=\int_0^\infty x(t-T_d)e^{-st}\,dt \); con el cambio \( \tau=t-T_d \):

$$ \int_{-T_d}^\infty x(\tau)\,e^{-s(\tau+T_d)}\,d\tau = e^{-sT_d}\!\int_0^\infty x(\tau)e^{-s\tau}\,d\tau = e^{-sT_d}\,X(s) $$

$$ \boxed{\;\text{retraso }T_d \;\Longleftrightarrow\; \text{factor } e^{-sT_d}\;} $$

**Paso 3 — composición del retardo total.** El retardo lo forman el cómputo (un periodo \( T_s \): la muestra de un ciclo se aplica al siguiente) más la actualización del PWM/ZOH (que en promedio retrasa medio periodo, \( T_s/2 \)):

$$ T_d=T_s+\tfrac12 T_s=\tfrac32 T_s\approx1.5\,T_s $$

**Paso 4 — efecto en frecuencia: fase pura.** Evaluando en \( s=j\omega \): \( e^{-j\omega T_d} \) tiene módulo \( |e^{-j\omega T_d}|=1 \) (no atenúa) y argumento

$$ \angle e^{-j\omega T_d}=-\omega T_d \quad\Longrightarrow\quad \Delta\phi(\omega)=-\omega T_d $$

Es **fase pura negativa que crece linealmente** con \( \omega \): a baja frecuencia apenas se nota, pero en el cruce \( \omega_c \) resta \( \omega_c T_d \) directamente del margen de fase.

**Paso 5 — números.** Con \( T_d=1.5\,T_s \) y un cruce ambicioso \( f_c=f_s/10 \):

$$ \Delta\phi=-\omega_c T_d=-2\pi f_c\cdot1.5T_s=-2\pi\frac{f_s}{10}\cdot\frac{1.5}{f_s}=-2\pi\cdot0.15=-54^\circ $$

Se pierden 54° de margen solo por el retardo — inadmisible sin compensar. Esto motiva la predicción.

## 2 — Predictor de Smith: cómo saca el retardo del lazo característico
**Paso 1 — la planta con retardo.** La planta real es \( G(s)\,e^{-sT_d} \). Cerrar el lazo con un controlador \( C(s) \) da la característica \( 1+C(s)G(s)e^{-sT_d}=0 \): el \( e^{-sT_d} \) está **dentro**, y es lo que come el margen.

**Paso 2 — la idea: predecir la salida sin retardo.** Con un modelo \( \hat G(s) \) de la planta (sin retardo), se construye en paralelo una estimación de cuánto valdría la salida si no hubiera retardo. La señal que se realimenta al controlador es la salida medida **corregida** con la diferencia entre el modelo sin retardo \( \hat G \) y el modelo con retardo \( \hat G\,e^{-sT_d} \).

**Paso 3 — el controlador equivalente.** Esa estructura es algebraicamente equivalente a sustituir \( C(s) \) por

$$ \boxed{\;C_{eq}(s)=\frac{C(s)}{1+C(s)\,\hat G(s)\,(1-e^{-sT_d})}\;} $$

**Paso 4 — qué ve el lazo si el modelo es exacto.** Si \( \hat G=G \), la función de transferencia de lazo cerrado resulta

$$ T(s)=\frac{C_{eq}\,G\,e^{-sT_d}}{1+C_{eq}\,G\,e^{-sT_d}}=\frac{C\,G}{1+C\,G}\;e^{-sT_d} $$

El denominador característico es \( 1+C(s)G(s) \): **el \( e^{-sT_d} \) ha salido del lazo**. El controlador se sintoniza sobre \( G(s) \) sin retardo (margen completo); el retardo solo aparece como un \( e^{-sT_d} \) multiplicativo a la salida, que desplaza la respuesta en el tiempo pero no afecta a la estabilidad.

**Paso 5 — el precio.** Todo depende de \( \hat G\approx G \) y \( \hat T_d\approx T_d \). Un error de modelo > 10–20 % reintroduce \( (1-e^{-sT_d}) \) mal cancelado en el lazo y puede empeorar la robustez respecto a no compensar; por eso en convertidores se prefiere a menudo la predicción de estados (un paso adelante con el modelo del filtro), más simple y tolerante.

## Cuándo y por qué se usa
En lazos rápidos (corriente) con \( f_c \) cercano a \( f_s/10 \), donde el retardo ya cuesta varios
grados de margen; en convertidores de alta frecuencia de cruce; y para mejorar la pasividad de la
impedancia a alta frecuencia.

## Procedimiento de diseño (genérico)
1. Cuantifica \( T_d \) real (cómputo + actualización PWM) y su \( \Delta\phi \) en \( \omega_c \).
2. Decide técnica: predicción de estados (robusta, sencilla) o Smith (retardos grandes).
3. Implementa el predictor con el modelo \( \hat G \) y verifica robustez a error de \( \hat G,T_d \).
4. Re-evalúa [[margenes-estabilidad|márgenes]] e impedancia con el compensador.
5. Discretiza con cuidado ([[discretizacion-controladores]]).

## Ejemplo de código
```python
# Adelanto de angulo en dq por el retardo de computo+PWM
import numpy as np
def angle_advance(theta, w, Td):
    return theta + w*Td                 # rota referencia para compensar el retardo
```

## Parámetros y valores típicos
\( T_d\approx1.5\,T_s \). Adelanto de ángulo \( \omega T_d \). El predictor de Smith es sensible a
errores de modelo > 10–20 %.

## Errores comunes
- Despreciar \( T_d \) al diseñar (márgenes optimistas que no se cumplen en hardware).
- Predictor de Smith con modelo pobre → peor que sin compensar.
- Sobre-predecir (compensar de más) → adelanto excesivo y ruido amplificado.

## Conceptos relacionados
- [[discretizacion-controladores]] · [[margenes-estabilidad]] · [[desacoplo-dq]] · [[fenomenos-oscilatorios-red|estabilidad armónica]] · [[controlador-pid]]

## Referencias
- Buso, Mattavelli, *Digital Control in Power Electronics*, 2006.
- Åström, Hägglund, *Advanced PID Control*, 2006.
