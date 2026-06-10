---
titulo: Ecuación de oscilación (swing equation)
slug: ecuacion-oscilacion
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: []
objetivos: [describir la dinámica ángulo-frecuencia de una fuente síncrona]
tags: [swing, inercia, angulo, frecuencia, par-sincronizante, intermedio, modelado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-09
relacionados: [vsm-inercia, droop-control, grid-forming-vs-following, potencia-ac-fasores, red-thevenin-scr]
referencias:
  - "Kundur, Power System Stability and Control, McGraw-Hill 1994"
  - "Machowski, Bialek, Bumby, Power System Dynamics, Wiley 2008"
---

## Definición
Ecuación que relaciona el **desbalance de potencia** de una máquina (o convertidor) síncrono con la
aceleración de su **ángulo y frecuencia**. Es el modelo electromecánico básico que gobierna la
estabilidad transitoria y la respuesta de frecuencia, y la base de la [[vsm-inercia|inercia
virtual]] y del [[droop-control|droop]].

## Fundamento teórico
En por unidad, con **constante de inercia** \( H \) (energía cinética almacenada / potencia base,
en s):
$$ \frac{2H}{\omega_0}\frac{d^2\delta}{dt^2}=P_m-P_e-D\,\frac{\Delta\omega}{\omega_0} $$
o en forma de estado con \( \Delta\omega=\dot\delta \):
$$ 2H\,\frac{d\Delta\omega}{dt}=P_m-P_e-D\,\Delta\omega,\qquad \frac{d\delta}{dt}=\omega_0\,\Delta\omega $$
- \( P_m \): potencia mecánica/de entrada; \( P_e \): potencia eléctrica entregada; \( D \):
  amortiguamiento.
- Para una fuente tras una reactancia \( X \) hacia una red \( V_g\angle 0 \):
  \( P_e=\dfrac{E V_g}{X}\sin\delta \).

**Linealizando** en \( \delta_0 \) aparece el modo electromecánico:
$$ 2H\,\Delta\ddot\delta + D\,\Delta\dot\delta + \omega_0 K_s\,\Delta\delta=0,\quad
   K_s=\frac{\partial P_e}{\partial\delta}=\frac{E V_g}{X}\cos\delta_0 $$
$$ \omega_{n}=\sqrt{\frac{\omega_0 K_s}{2H}},\qquad \zeta=\frac{D}{2}\sqrt{\frac{\omega_0}{2H K_s}} $$
\( K_s \) es el **par/potencia sincronizante**: si \( K_s<0 \) (p.ej. \( \delta_0>90^\circ \)) se
pierde el sincronismo. Menos inercia \( H \) → oscilaciones más rápidas; red débil (\( X \) grande,
bajo [[red-thevenin-scr|SCR]]) → \( K_s \) pequeño → modo lento y poco amortiguado.

## Cuándo y por qué se usa
Para analizar estabilidad de frecuencia/ángulo, dimensionar inercia y droop, y entender por qué los
convertidores grid-forming (VSM) emulan esta ecuación. Conecta el lazo de potencia con la dinámica
de red.

## Procedimiento de diseño (genérico)
1. Plantea \( P_e(\delta) \) con la reactancia equivalente a la red.
2. Halla el punto de equilibrio \( \delta_0 \) (\( P_m=P_e \)).
3. Linealiza → \( K_s \), \( \omega_n \), \( \zeta \) del modo electromecánico.
4. Ajusta \( H \) (inercia) y \( D \) (amortiguamiento) para el \( \omega_n,\zeta \) deseados.
5. Verifica margen de ángulo (\( \delta_0 \) lejos de 90°) y respuesta ante escalón de \( P_m \).

## Ejemplo de aplicación real
**Problema:** VSM de 1 MVA con inercia emulada \( H=4\,\text{s} \), amortiguamiento \( D=0.1 \), conectado a red de \( X=0.2\,\text{p.u.} \) (SCR≈5) en el punto de operación \( P_0=0.8\,\text{p.u.} \). Calcular la frecuencia y amortiguamiento del modo electromecánico.

Tensión interna \( E=1.05\,\text{p.u.} \), tensión de red \( V_g=1.0\,\text{p.u.} \). Punto de equilibrio: \( \delta_0=\arcsin(P_0 X/(E V_g))=\arcsin(0.8\times0.2/1.05)\approx8.8° \). Par sincronizante: \( K_s=(E V_g/X)\cos\delta_0=(1.05/0.2)\cos8.8°\approx5.19\,\text{p.u.} \). Frecuencia del modo: \( \omega_n=\sqrt{\omega_0 K_s/(2H)}=\sqrt{314\times5.19/(8)}\approx14.3\,\text{rad/s}\approx2.3\,\text{Hz} \). Amortiguamiento: \( \zeta=D\omega_0/(4H\omega_n)=0.1\times314/(16\times14.3)\approx0.14 \). El modo oscila a 2.3 Hz con pobre amortiguamiento — típico de microrredes insulares. Para subir \( \zeta \) a 0.5: aumentar \( D \) a ~0.35 (droop de frecuencia más agresivo) o reducir \( H \) (pero baja la inercia).

## Ejemplo de código
```python
import numpy as np
def swing(t, x, Pm, E, Vg, X, H, D, w0):
    delta, dw = x
    Pe = E*Vg/X*np.sin(delta)
    return [w0*dw, (Pm - Pe - D*dw)/(2*H)]
```

## Parámetros y valores típicos
Generadores: \( H\approx 2\text{–}9 \) s. VSM: \( H \) emulada 1–6 s. Modo electromecánico
0.1–2 Hz. \( \delta_0 \) de diseño < 30–45°.

## Errores comunes
- Operar con \( \delta_0 \) cercano a 90° (poco par sincronizante, riesgo de pérdida de sincronismo).
- Despreciar \( D \): sin amortiguamiento el modo oscila indefinidamente.
- Usar el modelo lineal para transitorios grandes (la no linealidad \( \sin\delta \) domina).

## Conceptos relacionados
- [[vsm-inercia]] · [[droop-control]] · [[grid-forming-vs-following]] · [[red-thevenin-scr]] · [[potencia-ac-fasores]]

## Referencias
- Kundur, *Power System Stability and Control*, 1994.
- Machowski, Bialek, Bumby, *Power System Dynamics*, 2008.
