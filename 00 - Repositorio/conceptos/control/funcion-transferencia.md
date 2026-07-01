---
titulo: Función de transferencia
slug: funcion-transferencia
categoria: control
tipo: concepto
nivel: basico
proyectos: []
objetivos: [describir la relacion entrada-salida de un sistema lineal]
tags: [funcion-transferencia, dominio-s, ganancia, basico, control]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [transformada-laplace, polos-ceros, respuesta-frecuencia-ss, diagrama-bode, realimentacion]
referencias:
  - "Ogata, Ingeniería de Control Moderna, Pearson"
---

## Definición
Cociente, en el dominio de Laplace, entre la salida y la entrada de un sistema lineal con
condiciones iniciales nulas. Resume toda la dinámica entrada-salida en una sola expresión
\( G(s) \).

## Fundamento teórico
$$ G(s) = \frac{Y(s)}{U(s)} = \frac{b_m s^m + \dots + b_0}{a_n s^n + \dots + a_0} $$
- El **denominador** igualado a cero da la **ecuación característica**: sus raíces son los
  **polos** (gobiernan la dinámica y la estabilidad).
- El **numerador** da los **ceros**.
- \( G(0) \) es la **ganancia en continua** (régimen permanente ante un escalón).
- Evaluando en \( s=j\omega \) se obtiene la **respuesta en frecuencia** \( G(j\omega) \) (Bode).

El orden \( n \) del denominador es el número de estados/almacenadores de energía.

<div class="cfig"><img src="figuras/funcion-transferencia-polos-step.png" alt="polos de G(s) y la respuesta al escalon que implican"><div class="cap">Los polos de G(s) (raíces del denominador) determinan la forma de la respuesta: este par complejo subamortiguado produce el escalón con sobreimpulso de la derecha.</div></div>

## 1 — De la EDO lineal a G(s) por transformada de Laplace

**Paso 1 — ecuación diferencial de partida.** Considera un sistema descrito por la EDO lineal de orden \( n \) con coeficientes constantes (condiciones iniciales nulas):

$$ a_n y^{(n)}(t) + a_{n-1}y^{(n-1)}(t) + \dots + a_1\dot{y}(t) + a_0 y(t) = b_m u^{(m)}(t) + \dots + b_0 u(t) $$

**Paso 2 — aplicar la transformada de Laplace.** Con CI nulas, \( \mathcal{L}\{y^{(k)}(t)\}=s^k Y(s) \). La EDO se convierte en una ecuación algebraica:

$$ \left(a_n s^n + a_{n-1}s^{n-1} + \dots + a_0\right) Y(s) = \left(b_m s^m + \dots + b_0\right) U(s) $$

**Paso 3 — despejar Y(s)/U(s).** Agrupando los polinomios y despejando:

$$ \boxed{G(s) = \frac{Y(s)}{U(s)} = \frac{b_m s^m + \dots + b_0}{a_n s^n + \dots + a_0}} $$

La EDO de grado \( n \) queda comprimida en un cociente de polinomios: el denominador retiene la dinámica propia del sistema (polos) y el numerador, cómo la entrada accede al sistema (ceros).

## 2 — Ejemplo: G(s) = ωn²/(s² + 2ζωn s + ωn²)

**Paso 1 — EDO del oscilador de segundo orden.** Un oscilador amortiguado (masa-resorte-amortiguador, o circuito RLC) tiene la EDO:

$$ \ddot{y}(t) + 2\zeta\omega_n\,\dot{y}(t) + \omega_n^2\,y(t) = \omega_n^2\,u(t) $$

donde \( \omega_n \) es la frecuencia natural y \( \zeta \) el amortiguamiento. El factor \( \omega_n^2 \) en el lado derecho garantiza ganancia unitaria en continua.

**Paso 2 — Laplace con CI nulas.** Aplicando \( \mathcal{L}\{\cdot\} \) término a término:

$$ s^2 Y(s) + 2\zeta\omega_n\,s\,Y(s) + \omega_n^2 Y(s) = \omega_n^2 U(s) $$

**Paso 3 — factorizar y despejar.** Sacando \( Y(s) \) como factor común en la izquierda:

$$ Y(s)\left(s^2 + 2\zeta\omega_n s + \omega_n^2\right) = \omega_n^2 U(s) $$

$$ \boxed{G(s) = \frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}} $$

**Verificación de ganancia DC.** En \( s=0 \): \( G(0)=\omega_n^2/\omega_n^2=1 \). Correcto: ante una entrada escalón, la salida llega a 1 (sin error en régimen permanente).

## Cuándo y por qué se usa
Es la representación básica del control clásico: permite combinar bloques (serie, paralelo,
realimentación), analizar estabilidad por los polos y diseñar en frecuencia.

## Procedimiento (genérico)
1. Plantea la ecuación diferencial o el modelo de estado.
2. Aplica [[transformada-laplace]] y despeja \( Y(s)/U(s) \).
3. Identifica polos (denominador) y ceros (numerador) y la ganancia DC.
4. Usa \( G(s) \) para análisis (estabilidad, Bode) o interconexión de bloques.

## Ejemplo de aplicación real
**Problema:** VSC con \( L=2\,\text{mH} \), \( r=50\,\text{m}\Omega \). Obtener la FT de tensión de convertidor a corriente y dimensionar el PI para cruzar a \( f_c=1\,\text{kHz} \).

La planta es \( G_i(s)=1/(Ls+r) \), polo en \( s=-r/L=-25\,\text{rad/s} \). El PI con cero en \( z=-r/L \) cancela ese polo; la FT de lazo queda \( K_p/(Ls) \) (integrador puro). Para \( \omega_c=2\pi\times1000\,\text{rad/s} \): \( K_p=L\,\omega_c\approx12.6 \), \( K_i=K_p\,r/L\approx315\,\text{s}^{-1} \). El lazo cerrado resultante es \( G_{cl}(s)=1/(1+s/\omega_c) \): primer orden con \( \tau_{cl}=0.16\,\text{ms} \). La FT hace visible el polo que el PI debe cancelar y permite dimensionar \( K_p \) directamente desde \( \omega_c \).

## Ejemplo de código
```python
import control as ct
G = ct.tf([1], [1, 2, 1])          # 1 / (s^2 + 2s + 1)
polos = ct.poles(G)                 # raices del denominador
```

## Parámetros y valores típicos
Primer orden: \( G(s)=K/(\tau s+1) \). Segundo orden:
\( G(s)=\omega_n^2/(s^2+2\zeta\omega_n s+\omega_n^2) \).

## Errores comunes
- Cancelar un polo con un cero sin notar que oculta dinámica interna (modos no observables).
- Aplicarla a sistemas no lineales sin linealizar.

## Conceptos relacionados
- [[transformada-laplace]] · [[polos-ceros]] · [[respuesta-frecuencia-ss]] · [[diagrama-bode]]

## Referencias
- Ogata, *Ingeniería de Control Moderna*.
