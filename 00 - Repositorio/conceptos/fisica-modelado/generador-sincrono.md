---
titulo: Generador síncrono — modelo dq y dinámica
slug: generador-sincrono
categoria: fisica-modelado
tipo: concepto
nivel: avanzado
proyectos: []
objetivos: [modelar la dinámica electromagnética y mecánica del generador síncrono]
tags: [generador-sincrono, dq-park, swing, amortiguador, AVR, avanzado, modelado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-09
relacionados: [ecuacion-oscilacion, vsm-inercia, marco-dq, representacion-espacio-estados, clasificacion-estabilidad]
referencias:
  - "Kundur, Power System Stability and Control, McGraw-Hill 1994"
  - "Anderson, Fouad, Power System Control and Stability, IEEE Press 2003"
---

## Definición
Modelo matemático del generador síncrono en el marco **dq de Park** (referencial del rotor), que
desacopla las dinámicas de circuito electromagnético y mecánico y es la base de todos los estudios
de estabilidad de sistemas de potencia y de la emulación virtual (VSM).

## Fundamento teórico
**Circuito electromagnético.** En el eje d (flujo del rotor) y q (en cuadratura), con devanados
de campo \( f \) y amortiguadores \( D \) (eje d) y \( Q \) (eje q):
$$ \psi_d = -L_d i_d + L_{md}(i_f+i_D),\quad \psi_q=-L_q i_q+L_{mq}i_Q $$
Las tensiones de estátor (con velocidad del rotor \( \omega_r \)):
$$ v_d = -R_s i_d + \dot\psi_d - \omega_r\psi_q,\quad v_q=-R_s i_q+\dot\psi_q+\omega_r\psi_d $$
Esto es el **modelo de orden completo** (5–6 estados eléctricos). Se simplifican:
- **Modelo de 4º orden** (subransitorio): \( \psi_d,\psi_q,\psi_D,\psi_Q \) como estados; \( E'_d,E'_q \) tensiones transitorias.
- **Modelo clásico** (2 estados: \( \delta,\omega \)): solo la [[ecuacion-oscilacion|swing equation]] con \( E' \) constante; suficiente para estabilidad transitoria.

**Mecánica** ([[ecuacion-oscilacion]]):
$$ 2H\frac{d\omega}{dt}=T_m-T_e-D\Delta\omega,\quad \frac{d\delta}{dt}=\omega_0\Delta\omega $$
Par electromagnético: \( T_e=\psi_d i_q - \psi_q i_d \).

**Regulación**: AVR (Automatic Voltage Regulator) cierra el lazo \( V_{terminal}\to E_f \) (campo);
el governor cierra \( \omega\to T_m \). Su dinámica (tiempo \( \sim100\,\)ms–s) es la base de los
[[servicios-red-soporte|servicios de soporte de frecuencia/tensión]].

**Relevancia para convertidores.** El VSM ([[vsm-inercia]]) emula exactamente este modelo pero
sobre un convertidor; entender el original clarifica qué se emula, sus límites y las aproximaciones.

## Cuándo y por qué se usa
Para estudios de estabilidad de red mixta (generadores + convertidores), para entender la base
física del VSM/PSC/matching, y para modelar el lado AC de sistemas back-to-back con máquina.

## Procedimiento de diseño (genérico)
1. Elige el orden del modelo según el estudio: clásico (ángulo), 4º (transitorio), completo (cortocircuito).
2. Parametriza \( L_d,L_q,L'_d,L'_q,T'_{d0},T'_{q0},H,D \) de la hoja de datos.
3. Implementa en espacio de estados ([[representacion-espacio-estados]]) y linealiza en el punto de operación.
4. Cierra AVR y governor para estudios de régimen dinámico.
5. Conecta al modelo de red (Thevenin o nodos) y verifica estabilidad.

## Ejemplo de código
```python
def sg_swing(delta, dw, Tm, Te, H, D, w0):
    return [w0*dw, (Tm - Te - D*dw)/(2*H)]   # [d(delta)/dt, d(omega)/dt]

def Te_elec(psi_d, psi_q, id_, iq):
    return psi_d*iq - psi_q*id_               # par electromagnetico
```

## Parámetros y valores típicos
\( H=2\text{–}9 \) s; \( X_d=0.8\text{–}2.0 \) p.u.; \( X'_d=0.1\text{–}0.35 \) p.u.;
\( T'_{d0}=3\text{–}10 \) s; \( T''_{d0}=0.02\text{–}0.05 \) s. \( X_d>X_q \) (polo saliente) o
\( X_d=X_q \) (cilíndrico).

## Errores comunes
- Usar el modelo clásico (2 estados) para estudios subtransitorios → no captura la dinámica de los amortiguadores.
- Olvidar que \( X_d\ne X_q \) en máquinas de polo saliente (PMSG, hidro) → error en \( T_e \).
- Parametrizar el VSM con \( H \) del generador real sin considerar la limitación de corriente del convertidor.

## Conceptos relacionados
- [[ecuacion-oscilacion]] · [[vsm-inercia]] · [[marco-dq]] · [[representacion-espacio-estados]] · [[clasificacion-estabilidad]]

## Referencias
- Kundur, *Power System Stability and Control*, 1994.
- Anderson, Fouad, *Power System Control and Stability*, IEEE Press 2003.
