---
titulo: Desacoplo dq y feedforward de red
slug: desacoplo-dq
categoria: control
tipo: tecnica
nivel: intermedio
proyectos: []
objetivos: [convertir el lazo de corriente dq acoplado en dos lazos SISO independientes]
tags: [desacoplo, feedforward, acoplamiento-cruzado, dq, lazo-corriente, intermedio, control]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-09
relacionados: [marco-dq, control-cascada, control-vectorial, controlador-pid, filtro-lcl]
referencias:
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
  - "Kazmierkowski, Krishnan, Blaabjerg, Control in Power Electronics, Academic Press 2002"
---

## Definición
Técnica que **cancela el acoplamiento cruzado** \( \pm\omega L \) entre los ejes d y q del lazo de
corriente de un convertidor, y compensa por **prealimentación (feedforward)** la tensión de red,
dejando dos plantas SISO de primer orden controlables con sendos PI.

## Fundamento teórico
La dinámica del filtro en dq incluye los términos de Coriolis del marco giratorio (ver [[marco-dq]]):
$$ L\frac{di_d}{dt}=v_d-e_d+\omega L\,i_q-R i_d,\qquad
   L\frac{di_q}{dt}=v_q-e_q-\omega L\,i_d-R i_q $$
con \( v_{dq} \) tensión del convertidor y \( e_{dq} \) tensión de red. Eligiendo la ley de control
$$ v_d=v_d'-\omega L\,i_q+e_d,\qquad v_q=v_q'+\omega L\,i_d+e_q $$
los términos cruzados y la perturbación de red **se cancelan**, y queda
$$ L\frac{di_d}{dt}=v_d'-R i_d \ \Rightarrow\ \frac{i_d}{v_d'}=\frac{1}{Ls+R} $$
es decir, dos plantas de primer orden idénticas y **desacopladas**, donde \( v_{dq}' \) lo fija el
PI. El feedforward de \( e_{dq} \) mejora el rechazo de perturbación de red y la respuesta ante
huecos; el desacoplo de \( \omega L \) elimina el sobreimpulso cruzado en transitorios de par.

## Cuándo y por qué se usa
En todo control vectorial de corriente de convertidores y máquinas, sobre todo cuando \( \omega L \)
es grande (alta frecuencia o inductancia), donde el acoplamiento degrada notablemente la respuesta.
Es la base del lazo interno de la [[control-cascada]].

## Procedimiento de diseño (genérico)
1. Modela el filtro en dq e identifica los términos \( \pm\omega L \) y \( e_{dq} \).
2. Implementa el desacoplo (resta/suma \( \omega L\,i \)) y el feedforward de \( e_{dq} \) medida.
3. Diseña los PI sobre la planta SISO \( 1/(Ls+R) \) (p.ej. *internal model control*:
   \( K_p=L\,\alpha_c \), \( K_i=R\,\alpha_c \), con \( \alpha_c \) el ancho de banda deseado).
4. Verifica robustez al **error de estimación** de \( L \) y \( \omega \) (el desacoplo nunca es
   perfecto) y al retardo de cómputo/PWM.

## Ejemplo de aplicación real
**Problema:** VSC trifásico con \( L=2\,\text{mH} \), \( R=0.05\,\Omega \), \( \omega=314\,\text{rad/s} \). Cuantificar el acoplamiento sin desacoplo y verificar que tras añadir el feedforward desaparece.

Sin desacoplo: una referencia \( i_d^*=1000\,\text{A} \), \( i_q^*=0 \) produce, durante el transitorio, un error cruzado en \( i_q \) de amplitud \( \approx\omega L\Delta i_d/K_p=314\times0.002\times1000/12.6\approx50\,\text{A} \). Con desacoplo: se añade \( v_d\leftarrow v_d-\omega L i_q \) y \( v_q\leftarrow v_q+\omega L i_d \). El término cruzado se cancela algebraicamente y \( i_q \) permanece en 0 durante el escalón de \( i_d^*\) — verificable en simulación midiendo el máximo de \( |i_q| \) con/sin desacoplo. Con \( L \) con error del 10 %: el residuo de acoplamiento es \( 0.1\times\omega L\Delta i_d/K_p\approx5\,\text{A} \), despreciable en la mayoría de aplicaciones.

## Ejemplo de código
```python
def current_ctrl(id_ref, iq_ref, id_, iq_, ed, eq, w, L, pi_d, pi_q):
    vd = pi_d(id_ref - id_) - w*L*iq_ + ed      # desacoplo + feedforward
    vq = pi_q(iq_ref - iq_) + w*L*id_ + eq
    return vd, vq
```

## Parámetros y valores típicos
Ancho de banda del lazo de corriente \( \alpha_c \approx (1/10\text{–}1/5)\,\omega_{sw} \).
El desacoplo importa cuando \( \omega L \gtrsim R \) (casi siempre en convertidores de red).

## Errores comunes
- Usar \( L \) o \( \omega \) erróneos → desacoplo imperfecto y acoplamiento residual.
- Feedforward de \( e_{dq} \) ruidoso (medida sucia) → inyecta ruido en la modulación; filtrar.
- Olvidar el retardo digital, que reintroduce acoplamiento efectivo a alta frecuencia.

## Conceptos relacionados
- [[marco-dq]] · [[control-cascada]] · [[control-vectorial]] · [[controlador-pid]] · [[filtro-lcl]]

## Referencias
- Yazdani, Iravani, 2010.
- Kazmierkowski, Krishnan, Blaabjerg, *Control in Power Electronics*, 2002.
