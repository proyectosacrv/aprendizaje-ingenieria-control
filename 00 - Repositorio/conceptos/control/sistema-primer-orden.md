---
titulo: Sistema de primer orden
slug: sistema-primer-orden
categoria: control
tipo: concepto
nivel: basico
proyectos: []
objetivos: [entender la respuesta de un sistema de un solo polo]
tags: [primer-orden, constante-de-tiempo, polo, respuesta-escalon, basico]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-11
relacionados: [polos-ceros, respuesta-segundo-orden, funcion-transferencia, sintonia-pi-pid]
referencias:
  - "Ogata, Ingeniería de Control Moderna, Pearson"
---

## Definición
Sistema con un único polo (un solo almacenador de energía dominante). Su respuesta no oscila:
sube o baja exponencialmente hacia su valor final. Es el ladrillo más simple del control.

## Fundamento teórico
$$ G(s) = \frac{K}{\tau s + 1} $$
- \( K \): ganancia en continua (valor final ante un escalón unitario).
- \( \tau \): **constante de tiempo** (s). El polo está en \( s=-1/\tau \).
Respuesta a un escalón de amplitud \( A \):
$$ y(t) = A\,K\left(1 - e^{-t/\tau}\right) $$
Alcanza el 63% del valor final en \( t=\tau \) y prácticamente el 100% en \( t\approx 4\tau \)
(tiempo de establecimiento). Cuanto menor \( \tau \) (polo más a la izquierda), más rápido.
Ejemplo físico: un inductor con resistencia tiene \( \tau=L/R \); un condensador, \( \tau=RC \).

<div class="cfig"><img src="figuras/sistema-primer-orden-escalon.png" alt="respuesta al escalon de primer orden"><div class="cap">Respuesta al escalón de primer orden: alcanza el 63% del valor final en t=τ y prácticamente el 100% en 4τ. El polo en −1/τ fija la rapidez.</div></div>

## Cuándo y por qué se usa
Muchos lazos internos (corriente sobre un inductor) son de primer orden. Entenderlo permite
sintonizar por cancelación de polo y estimar tiempos de respuesta.

## Procedimiento (genérico)
1. Identifica el polo dominante y la ganancia DC.
2. Lee \( \tau \) (rapidez) y \( K \) (valor final).
3. Estima el tiempo de establecimiento \( \approx 4\tau \).
4. Para acelerar, diseña un control que mueva el polo a la izquierda.

## Ejemplo de aplicación real
**Problema:** Lazo de corriente diseñado para \( \tau_{cl}=0.2\,\text{ms} \). Verificar midiendo la respuesta escalón en simulación.

Se aplica un escalón de referencia de 1 A. La corriente debe llegar al 63.2 % (0.632 A) en \( \tau_{cl}=0.2\,\text{ms} \). En simulación se mide \( t_{63\%}=0.21\,\text{ms} \): error del 5 %, aceptable. La ganancia DC se verifica como \( K=i(\infty)/i_{ref}=1.0 \): error en régimen nulo (el PI integra). El tiempo de asentamiento al 2 % es \( t_s\approx4\tau_{cl}=0.8\,\text{ms} \). Para acelerar: aumentar \( K_p \) (reduce \( \tau_{cl}=L/K_p \)); para reducir sensibilidad al ruido: reducirlo. El modelo de primer orden permite planificar estos compromisos analíticamente antes de simular.

## Ejemplo de código
```python
import control as ct
G = ct.tf([2], [0.1, 1])           # K=2, tau=0.1 s
t, y = ct.step_response(G)         # sube hacia 2 con tau=0.1
```

## Parámetros y valores típicos
\( t \) al 63% = \( \tau \); al 95% ≈ \( 3\tau \); al 98% ≈ \( 4\tau \).

## Errores comunes
- Confundir constante de tiempo con tiempo de establecimiento (este es ~4 veces mayor).
- Tratar como primer orden un sistema con dinámica oculta (segundo orden mal amortiguado).

## Conceptos relacionados
- [[polos-ceros]] · [[respuesta-segundo-orden]] · [[sintonia-pi-pid]]

## Referencias
- Ogata, *Ingeniería de Control Moderna*.
