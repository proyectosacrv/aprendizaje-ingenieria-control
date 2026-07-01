---
titulo: Matching control (control por emparejamiento)
slug: matching-control
categoria: control
tipo: tecnica
nivel: avanzado
proyectos: []
objetivos: [emparejar la dinámica del bus DC con la frecuencia de red para sincronización natural]
tags: [matching, grid-forming, bus-dc, sincronizacion, energia, avanzado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-01
relacionados: [grid-forming-vs-following, vsm-inercia, power-synchronization-control, dinamica-bus-dc, ecuacion-oscilacion]
referencias:
  - "Arghir, Jouini, Dörfler, Grid-Forming Control for Power Converters based on Matching, Automatica 2018"
  - "Dörfler et al., Taming Instabilities in Power Grid Networks, Physica D 2016"
---

## Definición
Estrategia grid-forming que **empareja** la dinámica del condensador del bus DC con la ecuación de
sincronización de un generador síncrono: la tensión del bus \( v_{dc} \) actúa como variable de
frecuencia, de modo que la sincronización se produce de forma **física y natural** sin bucles de
control artificiales.

## Fundamento teórico
En un generador síncrono la variable de sincronización es la velocidad \( \omega \). En un
convertidor, el equivalente natural es la tensión del bus DC \( v_{dc} \) (su cuadrado es la
energía almacenada \( E=\tfrac12 Cv_{dc}^2 \), igual que la cinética \( E=\tfrac12 J\omega^2 \)).
La idea del matching es **asignar el ángulo** del convertidor directamente proporcional al bus DC:
$$ \dot\theta = k_{match}\,v_{dc} $$
y diseñar el control de modulación para que el balance de energía del condensador sea
$$ C\,v_{dc}\dot v_{dc} = P_s - P_e $$
idéntico a la swing equation con \( \omega\equiv k_{match}v_{dc} \). El resultado es:
- La tensión del bus **oscila** con la potencia, como la frecuencia de un generador.
- La sincronización con la red emerge de la dinámica física del almacenamiento DC.
- No se necesita PLL ni lazo de frecuencia artificial.
- **Ventaja**: la inercia es la del condensador real (no virtual), la estabilidad es intrínseca.
- **Limitación**: el bus DC oscila con la carga (no regulado a tensión constante), lo que requiere
  dimensionar \( C \) para el rizado de frecuencia admisible y es incompatible con topologías que
  exigen bus DC estricto.

La conexión formal con el VSM: tomando \( J_{v}=C/k_{match}^2 \) se recupera la inercia virtual
equivalente del condensador. El matching es el camino más corto desde la física del convertidor
hasta la dinámica del generador.

<div class="cfig"><img src="figuras/matching-control-swing.png" alt="tension del bus DC oscilando como un swing tras un escalon de potencia"><div class="cap">Al asignar $\dot\theta=k\,v_{dc}$, la tensión del bus DC hace de frecuencia: ante un escalón de potencia oscila y se asienta igual que el ángulo de un generador síncrono (ecuación de swing), con la inercia del condensador real. La sincronización emerge de la física del almacenamiento, sin PLL ni lazo de frecuencia.</div></div>

## Cuándo y por qué se usa
Convertidores con fuente de energía en el bus DC (BESS, supercondensadores) donde el rizado de
tensión DC es aceptable, y donde se quiere la máxima simplicidad de control con inercia genuina.
Es un marco teórico que también justifica y conecta VSM, PSC y droop.

## Procedimiento de diseño (genérico)
1. Elige \( k_{match} \) de modo que el rango de \( v_{dc} \) corresponda al rango de frecuencia
   admisible: \( \Delta\omega=k_{match}\Delta v_{dc} \).
2. Dimensiona \( C \) para la inercia efectiva deseada \( J_v=C/k_{match}^2 \).
3. Diseña el control de modulación para imponer \( \dot\theta=k_{match}v_{dc} \) y eliminar el
   término de acoplo d-q.
4. Añade regulación de Q/tensión AC de forma independiente (desacoplada).
5. Verifica rizado de \( v_{dc} \) bajo perturbaciones de potencia.

## Ejemplo de código
```python
def matching_angle(vdc, theta, k_match, dt):
    theta += k_match * vdc * dt     # angulo directo del bus DC
    return theta % (2*3.14159)
```

## Parámetros y valores típicos
\( k_{match} \) tal que \( \Delta v_{dc}\approx1\text{–}5\,\% \) de \( V_{dc0} \) corresponda a
\( \Delta\omega/\omega_0\approx0.5\text{–}2\,\% \). Inercia equivalente según la constante \( H \)
deseada.

## Errores comunes
- Ignorar que el bus DC no está regulado: incompatible con cargas que necesitan tensión DC estable.
- Confundir con PSC: el PSC regula \( P \) directamente; el matching deja que la física haga la
  sincronización sin lazo explícito de potencia.
- Dimensionar \( C \) solo por rizado de tensión y olvidar la inercia resultante.

## Conceptos relacionados
- [[grid-forming-vs-following]] · [[vsm-inercia]] · [[power-synchronization-control]] · [[dinamica-bus-dc]] · [[ecuacion-oscilacion]]

## Referencias
- Arghir, Jouini, Dörfler, *Grid-Forming Control for Power Converters based on Matching*, Automatica 2018.
- Dörfler et al., *Taming Instabilities in Power Grid Networks*, Physica D 2016.
