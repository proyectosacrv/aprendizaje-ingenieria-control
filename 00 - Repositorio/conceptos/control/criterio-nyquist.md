---
titulo: Criterio de estabilidad de Nyquist
slug: criterio-nyquist
categoria: control
tipo: metodo
nivel: basico
proyectos: []
objetivos: [determinar la estabilidad en lazo cerrado a partir de la ganancia de lazo]
tags: [nyquist, estabilidad, lazo-cerrado, rodeos, basico, control]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-12
relacionados: [margenes-estabilidad, diagrama-bode, estabilidad-bibo, polos-ceros, impedancia-salida-estabilidad]
referencias:
  - "Ogata, Ingeniería de Control Moderna, Pearson"
  - "Aström, Murray, Feedback Systems, Princeton 2008"
---

## Definición
Criterio gráfico que decide la **estabilidad en lazo cerrado** observando cómo la traza de la
ganancia de lazo \( L(j\omega) \) rodea al **punto crítico \( -1 \)**, sin calcular las raíces
del polinomio característico.

## Fundamento teórico
Se apoya en el **principio del argumento**. Para el lazo \( 1+L(s)=0 \), recorriendo el contorno
de Nyquist (todo el eje \( j\omega \) cerrado por la derecha), el número de rodeos en sentido
horario \( N \) de \( L(j\omega) \) alrededor de \( -1 \) cumple:
$$ Z = N + P $$
- \( Z \): ceros de \( 1+L \) en el semiplano derecho = **polos inestables del lazo cerrado**.
- \( P \): polos inestables de \( L \) (lazo abierto).
- Estable \( \iff Z=0 \): se necesitan \( N=-P \) rodeos **antihorarios** de \( -1 \).

Si \( L \) es estable en lazo abierto (\( P=0 \)), basta con que **no se rodee** \( -1 \). La
distancia mínima de la traza a \( -1 \) define el [[margenes-estabilidad|margen de módulo]].

<div class="cfig"><img src="figuras/criterio-nyquist-plot.png" alt="diagrama de Nyquist y el punto -1"><div class="cap">Diagrama de Nyquist de la ganancia de lazo L(jω): aquí la traza no rodea el punto crítico −1, así que (con L estable en lazo abierto) el lazo cerrado es estable. El cruce con el eje real negativo da el margen de ganancia.</div></div>

## Cuándo y por qué se usa
Cuando hay retardos, polos en lazo abierto inestables o sistemas donde Routh no aplica bien. Es
la base del **criterio de estabilidad por impedancia** (el cociente \( Z_o/Z_g \) se trata como
una ganancia de lazo y se le aplica Nyquist).

## Procedimiento (genérico)
1. Obtén \( L(j\omega) \) y cuenta \( P \) (polos de \( L \) en SPD).
2. Traza el diagrama polar de \( L(j\omega) \) para \( \omega:-\infty\to\infty \).
3. Cuenta los rodeos netos \( N \) alrededor de \( -1 \).
4. Aplica \( Z=N+P \); estable si \( Z=0 \).

## Ejemplo de aplicación real
**Problema:** Lazo de corriente con planta \( G_i(s)=1/(Ls) \), \( L=2\,\text{mH} \), PI y retardo de cómputo \( T_d=150\,\mu\text{s} \). Verificar estabilidad por Nyquist y cuantificar el margen.

La ganancia de lazo es \( L(j\omega) \) con contribuciones: integrador \( -90° \), PI (cero muy por debajo de \( \omega_c \), aporte \( \approx0° \)) y retardo \( -\omega_c T_d\times(180/\pi) \). A \( \omega_c=6283\,\text{rad/s} \): desfase del retardo \( \approx-54° \), fase total \( \approx-144° \), margen de fase \( 36° \). Como \( P=0 \) (lazo abierto estable), basta verificar que la traza no rodea \( -1 \). La distancia mínima da \( M_s=1/\sin(36°)\approx1.7<2 \): cumple la especificación. Para subir el margen a 45° bajar \( \omega_c \) a \( \approx750\,\text{Hz} \) (reduce el desfase del retardo a \( -40° \)).

## Ejemplo de código
```python
import control as ct, numpy as np
L = ct.tf([10], [1, 3, 3, 1])
ct.nyquist_plot(L)                 # ¿rodea -1?
print(ct.margin(L))                # (GM, PM, wcg, wcp): lectura cuantitativa
```

## Parámetros y valores típicos
Objetivo práctico: dejar \( -1 \) holgadamente fuera de la traza (margen de módulo \( 1/M_s \)
con \( M_s<2 \)). El cruce con el eje real negativo da el margen de ganancia.

## Errores comunes
- Olvidar contar \( P \): con polos inestables en lazo abierto, "no rodear −1" NO implica estable.
- Ignorar el rizo cerca de \( -1 \) por integradores/retardos (semicírculos en el infinito).
- Confundir el criterio simplificado (válido si \( P=0 \)) con el general.

## Conceptos relacionados
- [[margenes-estabilidad]] · [[diagrama-bode]] · [[estabilidad-bibo]] · [[impedancia-salida-estabilidad]]

## Referencias
- Ogata, *Ingeniería de Control Moderna*.
- Aström, Murray, *Feedback Systems*, 2008.
