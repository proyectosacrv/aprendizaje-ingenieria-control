---
titulo: Error en régimen permanente y tipo de sistema
slug: error-regimen-permanente
categoria: control
tipo: concepto
nivel: basico
proyectos: []
objetivos: [predecir el error estacionario según el número de integradores del lazo]
tags: [error-permanente, tipo-sistema, Kp, Kv, Ka, basico, control]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-30
relacionados: [realimentacion, metricas-desempeno, controlador-pid, funcion-transferencia, anti-windup]
referencias:
  - "Ogata, Ingeniería de Control Moderna, Pearson"
  - "Franklin, Powell, Feedback Control of Dynamic Systems, Pearson"
---

## Definición
Error que persiste entre referencia y salida cuando el transitorio se ha extinguido. Depende del
**tipo de sistema** (número de integradores \( 1/s \) en la ganancia de lazo) y de la clase de
entrada.

## Fundamento teórico
Por el teorema del valor final, para realimentación unitaria con lazo \( L(s) \):
$$ e_{ss}=\lim_{s\to0} \frac{s\,R(s)}{1+L(s)} $$
Se definen las **constantes de error estático**:
$$ K_p=\lim_{s\to0}L(s),\quad K_v=\lim_{s\to0}sL(s),\quad K_a=\lim_{s\to0}s^2L(s) $$

| Tipo (nº integradores) | Escalón \(1/s\) | Rampa \(1/s^2\) | Parábola \(1/s^3\) |
|---|---|---|---|
| 0 | \(1/(1+K_p)\) | \(\infty\) | \(\infty\) |
| 1 | 0 | \(1/K_v\) | \(\infty\) |
| 2 | 0 | 0 | \(1/K_a\) |

Cada integrador añade un tipo → anula el error ante una entrada de un orden más alto, **a costa**
de margen de fase (90° menos por integrador).

<div class="cfig"><img src="figuras/error-regimen-permanente-step.png" alt="error en regimen tipo 0 vs tipo 1"><div class="cap">Ante un escalón, el sistema tipo 0 (solo P) deja un error en régimen e_ss; el tipo 1 (con integrador) lo anula, a costa de más sobreimpulso / menos margen de fase.</div></div>

## 1 — Error ante escalón: por qué el integrador lo anula
**Paso 1 — punto de partida.** El error en el dominio de Laplace es \( E(s)=S(s)\,R(s)=\dfrac{R(s)}{1+L(s)} \) (sensibilidad, ver [[realimentacion]]). El **teorema del valor final** da su valor estacionario \( e_{ss}=\lim_{t\to\infty}e(t)=\lim_{s\to 0}sE(s) \):

$$ e_{ss}=\lim_{s\to0}\frac{s\,R(s)}{1+L(s)} $$

**Paso 2 — entrada escalón.** Para un escalón \( r(t)=1 \), \( R(s)=1/s \). El \( s \) del teorema cancela el \( 1/s \) del escalón:

$$ e_{ss}=\lim_{s\to0}\frac{s\,(1/s)}{1+L(s)}=\frac{1}{1+\lim_{s\to0}L(s)}=\frac{1}{1+K_p} $$

donde \( K_p=\lim_{s\to0}L(s) \) es la constante de error de posición.

**Paso 3 — tipo 0 vs tipo 1.** Si el lazo **no** tiene integrador (tipo 0), \( L(0)=K_p \) es un número finito y \( e_{ss}=\dfrac{1}{1+K_p}\neq 0 \): queda error. Si el lazo tiene un integrador \( 1/s \) (tipo 1, p.ej. un PI), al evaluar \( s\to 0 \):

$$ K_p=\lim_{s\to0}\frac{K(\cdots)}{s(\cdots)}\to\infty \;\Longrightarrow\; e_{ss}=\frac{1}{1+\infty}=0 $$

El integrador hace \( |L|\to\infty \) en continua, llevando el error de escalón **exactamente a cero**. Esa es la razón física de poner acción integral.

## 2 — Error ante rampa: por qué hace falta un tipo más
**Paso 1 — entrada rampa.** Para una rampa \( r(t)=t \), \( R(s)=1/s^2 \). El teorema del valor final deja un \( s \) en el denominador:

$$ e_{ss}=\lim_{s\to0}\frac{s\,(1/s^2)}{1+L(s)}=\lim_{s\to0}\frac{1}{s\,(1+L(s))}=\lim_{s\to0}\frac{1}{s+sL(s)} $$

Como \( s\to0 \), el sumando \( s \) se va y queda \( e_{ss}=\dfrac{1}{\lim_{s\to0}sL(s)}=\dfrac{1}{K_v} \), con \( K_v=\lim_{s\to0}sL(s) \) la constante de velocidad.

**Paso 2 — evaluar según el tipo.** Con un lazo tipo 1, \( L(s)=\dfrac{K}{s(s+a)} \): \( sL(s)=\dfrac{K}{s+a} \), luego \( K_v=\dfrac{K}{a} \) es **finito** y el error de rampa es:

$$ \boxed{\;e_{ss,\text{rampa}}=\frac{1}{K_v}=\frac{a}{K}\neq 0\;} $$

Un solo integrador sigue el escalón sin error pero deja **error constante** ante la rampa. Para anularlo haría falta tipo 2 (dos integradores), que haría \( sL\to\infty \) y \( K_v\to\infty \) — al precio de 90° más de pérdida de fase. Esto justifica la tabla: cada integrador "sube de nivel" la entrada que puede seguir con error nulo.

## Cuándo y por qué se usa
Para decidir si hace falta acción **integral**: seguir una referencia constante sin error exige
tipo ≥1; seguir una rampa sin error, tipo ≥2. Es el motivo de usar PI en lazos de corriente/tensión.

## Procedimiento (genérico)
1. Identifica integradores en \( L(s) \) → tipo del sistema.
2. Calcula \( K_p,K_v,K_a \) según la entrada relevante.
3. Si el error no cumple, añade integración (sube el tipo) y re-sintoniza.
4. Verifica que el margen de fase sigue siendo aceptable.

## Ejemplo de aplicación real
**Problema:** Lazo de corriente tipo I (PI) ante dos entradas: referencia escalón de 10 A y perturbación escalón de 1 V de tensión de red. Calcular el error en régimen para cada caso.

Para la **referencia escalón**: el PI tiene un integrador → tipo 1, \( K_p=\infty \) → \( e_{ss}=1/(1+K_p)=0 \). El PI integra hasta que el error desaparece. Para la **perturbación escalón** que entra después del controlador (tensión de red, componente \( d \)): el integrador del PI sigue estando en el camino de retroalimentación y también la anula → \( e_{ss}=0 \). Verificación: simular un escalón de perturbación de 5 V: la corriente se desviará transitoriamente pero regresará a los 10 A de referencia. Si se usa solo control P (sin integrador, tipo 0), el error ante la perturbación escalón sería \( 5/(R\cdot K_p) \neq 0 \).

## Ejemplo de código
```python
import sympy as sp
s = sp.symbols('s'); L = 20/(s*(s+5))      # tipo 1
Kv = sp.limit(s*L, s, 0)                    # error de rampa = 1/Kv
```

## Parámetros y valores típicos
Lazos de convertidor con PI → tipo 1 (error nulo a referencia constante en dq). Tipo 2 es raro
por la pérdida de fase.

## Errores comunes
- Subir el tipo sin vigilar el margen de fase → oscilación o inestabilidad.
- Olvidar que la integración pura sufre **windup** ante saturación → ver [[anti-windup]].
- Aplicar las fórmulas a lazos no unitarios sin reducir primero el diagrama.

## Conceptos relacionados
- [[realimentacion]] · [[controlador-pid]] · [[metricas-desempeno]] · [[anti-windup]]

## Referencias
- Ogata, *Ingeniería de Control Moderna*.
- Franklin, Powell, *Feedback Control of Dynamic Systems*.
