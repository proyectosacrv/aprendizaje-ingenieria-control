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
fecha_actualizacion: 2026-06-09
relacionados: [discretizacion-controladores, margenes-estabilidad, desacoplo-dq, estabilidad-armonica, controlador-pid]
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
no-pasividad ([[estabilidad-armonica]]). Compensaciones:
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
- [[discretizacion-controladores]] · [[margenes-estabilidad]] · [[desacoplo-dq]] · [[estabilidad-armonica]] · [[controlador-pid]]

## Referencias
- Buso, Mattavelli, *Digital Control in Power Electronics*, 2006.
- Åström, Hägglund, *Advanced PID Control*, 2006.
