---
titulo: Virtual Oscillator Control (VOC / dVOC)
slug: virtual-oscillator-control
categoria: control
tipo: tecnica
nivel: avanzado
proyectos: []
objetivos: [sincronizar convertidores en paralelo usando un oscilador no lineal virtual]
tags: [voc, dvoc, oscilador-virtual, sincronizacion, no-lineal, despacho, grid-forming, avanzado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-01
relacionados: [grid-forming-vs-following, vsm-inercia, power-synchronization-control, matching-control, droop-control]
referencias:
  - "Johnson et al., Synthesizing Virtual Oscillators to Control Islanded Inverters, IEEE TPEL 2016"
  - "Colombino et al., Global Phase and Magnitude Synchronization of Coupled Oscillators, IEEE TAC 2019"
---

## Definición
Estrategia grid-forming en la que la tensión de salida del convertidor es la salida de un
**oscilador no lineal emulado** (Van der Pol / oscilador de Liénard). En red islandica, los
convertidores se auto-sincronizan globalmente sin comunicaciones; la versión **dispatchable (dVOC)**
añade la capacidad de rastrear referencias de potencia P/Q arbitrarias.

## Fundamento teórico
**VOC básico (Van der Pol):**
$$ \ddot v + \epsilon(\kappa v^2-1)\dot v + \omega_0^2 v = 0 $$
La señal \( v(t) \) converge a una oscilación de amplitud \( 1/\sqrt\kappa \) y frecuencia
\( \omega_0 \) independientemente de las condiciones iniciales (atractor de ciclo límite). Al
conectar dos convertidores con este oscilador a través de sus impedancias, la **interacción
eléctrica actúa como acoplamiento de fase**; la teoría de sincronización (Kuramoto) garantiza
sincronización global si el acoplamiento supera un umbral.

**dVOC** (linealización alrededor del ciclo límite):
$$ \dot{\boldsymbol{\eta}} = \omega J\boldsymbol{\eta}+\frac{\alpha}{\|\eta\|^2}
   \bigl[\eta\eta^\top-\|\eta\|^2 I+\kappa(I-\eta\eta^\top/\|\eta\|^2)\bigr]\boldsymbol{\eta}
   +\frac{\gamma}{|\mathbf{v}^*|^2}\bigl(\mathbf{i}^*_{inj}-\mathbf{i}_{inj}\bigr) $$
con \( \boldsymbol{\eta}\in\mathbb{R}^2 \) (αβ), \( \mathbf{v}^* \), \( \mathbf{i}^*_{inj} \)
referencias de tensión y corriente derivadas de P*/Q*. La dVOC hereda la sincronización global del
VOC y permite despacho (P*, Q* arbitrarios); demuestra convergencia exponencial.

**Equivalencia con droop:** en régimen permanente linealizado, dVOC reduce al droop estándar (las
mismas relaciones P-ω / Q-V). La diferencia es la **dinámica transitoria**: VOC es globalmente
estable no linealmente, mientras el droop solo es local. En red **fuerte** (conectado a red), la
dinámica del oscilador aún tiene que coordinarse con la impedancia de red (análisis por
[[impedancia-salida-estabilidad|impedancia]]).

<div class="cfig"><img src="figuras/virtual-oscillator-control-ciclo.png" alt="ciclo limite de Van der Pol como atractor global"><div class="cap">El VOC emula un oscilador de Van der Pol: cualquier condición inicial (dentro o fuera) converge al mismo ciclo límite de amplitud y frecuencia fijas. Al acoplar varios convertidores por sus impedancias, la interacción eléctrica los sincroniza globalmente sin comunicaciones (sincronización tipo Kuramoto).</div></div>

## 1 — Linealización del oscilador de Van der Pol: amortiguamiento negativo y ciclo límite

**Paso 1 — ecuación completa.** El VOC emula el oscilador de Van der Pol:

$$ \ddot{v} - \varepsilon(1-\kappa v^2)\dot{v} + \omega_0^2\,v = 0 $$

con \( \varepsilon > 0 \) (coeficiente de no linealidad) y \( \kappa > 0 \) (parámetro de saturación de amplitud).

**Paso 2 — linealización alrededor de \( v = 0 \).** Para amplitudes pequeñas (\( \kappa v^2 \ll 1 \)) el término de amortiguamiento queda:

$$ \varepsilon(1-\kappa v^2)\dot{v}\approx \varepsilon\,\dot{v} $$

La ecuación linealizada es:

$$ \ddot{v} - \varepsilon\,\dot{v} + \omega_0^2\,v = 0 $$

cuyo polinomio característico es \( s^2 - \varepsilon s + \omega_0^2 = 0 \).

**Paso 3 — raíces y comportamiento.** Las raíces son:

$$ s = \frac{\varepsilon}{2} \pm j\sqrt{\omega_0^2 - \frac{\varepsilon^2}{4}} $$

Para \( \varepsilon \ll 2\omega_0 \) (caso típico): parte real \( +\varepsilon/2 > 0 \) → las oscilaciones de amplitud pequeña **crecen exponencialmente** con la frecuencia \( \omega_0 \). El sistema es inestable alrededor del origen (amortiguamiento negativo).

**Paso 4 — saturación no lineal y ciclo límite.** A medida que crece \( |v| \), el factor \( (1-\kappa v^2) \) se vuelve negativo para \( |v| > 1/\sqrt\kappa \): el amortiguamiento pasa a ser positivo y frena el crecimiento. El equilibrio entre los dos regímenes define el ciclo límite de amplitud:

$$ \boxed{A_{lim} = \frac{1}{\sqrt\kappa}} $$

con frecuencia \( \omega_0 \). Cualquier condición inicial converge a esta trayectoria (atractor global del ciclo límite), lo que garantiza que la tensión de salida del convertidor alcanza siempre la amplitud y frecuencia correctas.

**Paso 5 — efecto de la red.** Al conectar el convertidor a la red (o a otros convertidores), la corriente inyectada añade un término de fuerza al oscilador. En régimen permanente sincronizado, ese término compensa exactamente el amortiguamiento negativo, dejando \( \varepsilon_{efectivo} = 0 \): el convertidor oscila en el ciclo límite con la frecuencia y fase de la red, sin PLL.

## Cuándo y por qué se usa
Redes islandinas con múltiples convertidores (microrredes) donde se quiere sincronización robusta y
global sin comunicaciones, y donde las garantías formales de estabilidad no lineal son valiosas.
También como base teórica para entender la sincronización espontánea de convertidores.

## Procedimiento de diseño (genérico)
1. Elige la frecuencia del oscilador \( \omega_0 \) y la amplitud deseada → parámetros \( \kappa,\alpha \).
2. Linealiza (dVOC): mapea P*, Q* a \( \mathbf{i}^*_{inj} \) con la ganancia \( \gamma \).
3. Verifica que el acoplamiento supera el umbral de sincronización (análisis Kuramoto para N unidades).
4. Comprueba estabilidad de pequeña señal cuando se conecta a red (impedancia 2×2).
5. Implementa en discreto con paso \( T_s \); la oscilación de ciclo límite debe estar bien
   resuelta (\( f_s \gg \omega_0/2\pi \)).

## Ejemplo de código
```python
def voc_step(eta, i_inj, i_ref, v_ref, alpha, kappa, w0, gamma, dt):
    import numpy as np
    J = np.array([[0,-1],[1,0]])
    nm2 = eta@eta
    corr = alpha/nm2 * (np.outer(eta,eta) - nm2*np.eye(2)
                        + kappa*(np.eye(2) - np.outer(eta,eta)/nm2)) @ eta
    inj  = (gamma/v_ref**2) * (i_ref - i_inj)
    return eta + (w0*J@eta + corr + inj)*dt
```

## Parámetros y valores típicos
\( \alpha \approx 5\text{–}50 \) (velocidad de convergencia de amplitud), \( \kappa \) fija la
amplitud del ciclo límite, \( \gamma \) equivale al droop. En régimen permanente, los parámetros
deben dar el mismo estatismo que el droop deseado.

## Errores comunes
- Elegir \( \alpha \) muy grande: oscilaciones transitorias rápidas que saturan el convertidor.
- Olvidar que la sincronización global garantizada es para redes **islandinas**; en red conectada
  hay que analizar la interacción con la impedancia de red por separado.
- Discretizar con \( T_s \) demasiado grande y perder el ciclo límite.

## Conceptos relacionados
- [[grid-forming-vs-following]] · [[vsm-inercia]] · [[power-synchronization-control]] · [[matching-control]] · [[droop-control]]

## Referencias
- Johnson et al., *Synthesizing Virtual Oscillators to Control Islanded Inverters*, IEEE TPEL 2016.
- Colombino et al., *Global Phase and Magnitude Synchronization of Coupled Oscillators*, IEEE TAC 2019.
