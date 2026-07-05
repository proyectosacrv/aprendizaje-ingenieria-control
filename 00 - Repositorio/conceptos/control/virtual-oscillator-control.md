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

## 3 — Modelo Van der Pol completo: ciclo límite y amplitud estable

La ecuación de Van der Pol que emula el VOC:

$$\ddot{v} - \mu(1-v^2)\dot{v} + \omega_0^2\,v = 0$$

tiene dos regímenes claros:
- **Para \(|v| < 1\):** el factor \((1-v^2) > 0\) → amortiguamiento negativo → las oscilaciones crecen.
- **Para \(|v| > 1\):** el factor \((1-v^2) < 0\) → amortiguamiento positivo → las oscilaciones se frenan.

El ciclo límite estable se establece en \(A_{ss} = 2\) (para la forma normalizada con \(\kappa=1/4\)):

$$A_{ss} = \frac{2}{\sqrt{\kappa}}$$

Para \(\kappa = 1/4\): \(A_{ss} = 2\) (amplitud de la tensión de salida del VOC). La frecuencia del ciclo límite es \(\omega_0\) con una corrección de segundo orden \(O(\mu^2)\) despreciable para \(\mu \ll 2\omega_0\).

**Energía del ciclo límite:** la potencia media disipada en el ciclo límite es nula (el oscilador es conservativo en el ciclo), lo que implica que el convertidor no necesita energía interna para mantener la oscilación — la energía viene de la red o de la carga.

## 4 — Sincronización de Kuramoto: VOC como caso particular

El modelo de Kuramoto describe la sincronización de \(N\) osciladores acoplados:

$$\dot{\theta}_i = \omega_i + \frac{K}{N}\sum_{j=1}^N \sin(\theta_j - \theta_i)$$

donde \(\omega_i\) son las frecuencias naturales de cada oscilador y \(K\) es la ganancia de acoplamiento. El teorema de Kuramoto establece que, si \(K > K_c = 2/(\pi g(0))\) (donde \(g\) es la distribución de frecuencias naturales), todos los osciladores se sincronizan a una frecuencia común.

**VOC como Kuramoto:** cuando dos convertidores VOC están conectados eléctricamente, la corriente entre ellos actúa como la señal de acoplamiento \(\sin(\theta_j-\theta_i)\). El dVOC (dispatchable VOC) introduce explícitamente el control de P/Q:

$$\dot{\theta}_i = \omega_0 + \frac{1}{v_{ref}^2}\text{Im}\{(P_i^* + jQ_i^*)e^{-j\theta_i}/\overline{v}_i\}$$

La condición de sincronización global: la ganancia de acoplamiento \(\gamma\) debe superar el umbral de Kuramoto, lo que en convertidores se traduce en que el acoplamiento eléctrico (impedancia de interconexión) sea suficientemente bajo.

## 5 — VOC vs Droop vs VSG: comparativa de propiedades

| Propiedad | VOC | Droop | VSG/VSM |
|---|---|---|---|
| Inercia explícita | No (ciclo límite) | No | Sí (\(J\) virtual) |
| Sincronización global | Sí (garantía formal) | No (local) | No |
| Gran señal estable | Sí (ciclo límite = atractor global) | Solo con saturación | Con saturación |
| Armónicos en tensión | Bajos (filtro LC integrado) | Depende del lazo interno | Depende del lazo interno |
| Respuesta a transitorios de P | Instantánea (no filtrada) | Filtrada por LPF | Filtrada por inercia |
| Complejidad de implementación | Media (integración ODE) | Baja (PI+droop) | Media-alta (modelo swing) |

El VOC no tiene inercia explícita: ante un escalón de carga, la frecuencia cambia instantáneamente. Esto puede ser una ventaja (respuesta rápida) o desventaja (ROCOF alto) según el contexto. Para aplicaciones donde se requiere inercia, se usa VSG; para microrredes islandinas con muchos generadores, VOC ofrece las mejores garantías de sincronización.

## 6 — Implementación discreta: Runge-Kutta orden 4 y lazo interno de corriente

La implementación discreta del VOC integra las ecuaciones diferenciales con Runge-Kutta orden 4 (RK4):

$$v_{k+1} = v_k + \frac{T_s}{6}(k_1 + 2k_2 + 2k_3 + k_4)$$

donde \(k_1 = f(v_k, \dot{v}_k)\), \(k_2 = f(v_k+k_1T_s/2, ...)\), etc.

**Condición de paso de tiempo:** para resolver el ciclo límite con precisión, \(T_s \leq T_0/100\) donde \(T_0 = 2\pi/\omega_0 = 20\,\text{ms}\) a 50 Hz. Por tanto \(T_s \leq 200\,\mu\text{s}\) — compatible con convertidores a \(f_s \geq 5\,\text{kHz}\).

**Lazo interno de corriente:** el VOC proporciona la referencia de tensión \(v^*\), pero el convertidor en la práctica requiere un lazo interno de corriente para:
- Limitar la corriente durante transitorios (protección ante cortocircuito)
- Rejetar perturbaciones de impedancia interna de la etapa de potencia
- Filtrar las oscilaciones del ciclo límite que de otro modo generarían contenido armónico a \(f_0\)

El lazo interno de corriente (PR o PI en dq) opera 10× más rápido que la dinámica del oscilador, preservando la separación de escalas. La tensión de referencia del VOC actualiza el setpoint del lazo interno a cada período de modulación.

## 7 — Sincronización con la red: análisis de impedancia y límites del VOC

La garantía de sincronización global del VOC es estrictamente válida en redes **islandinas**. Al conectar a una red rígida, el comportamiento cambia:

- **Red muy fuerte (SCR → ∞):** la tensión del PCC está fijada por la red; el VOC se comporta como un generador de corriente cuya frecuencia es arrastrada por la red — sincronización trivial.
- **Red débil (SCR < 3):** la impedancia de red interactúa con la impedancia de salida del VOC. Si el ciclo límite produce una componente de impedancia de salida con \(\text{Re}\{Z_{VOC}\}<0\) en alguna banda, pueden aparecer oscilaciones subsíncronas (ver [[fenomenos-oscilatorios-red]]).
- **Verificación:** calcular \(Z_{VOC}(j\omega)\) linearizando alrededor del ciclo límite y aplicar el criterio de pasividad \(\text{Re}\{Z_{VOC}\}>0\) para toda \(\omega\).

**Protección de corriente:** el VOC no limita la corriente de forma natural — el ciclo límite puede crecer si la perturbación de corriente es grande. Se requiere un lazo de corriente interno (PI en dq o PR) con limitador de amplitud, operando 10× más rápido que la dinámica del oscilador para preservar la separación de escalas.

## 8 — VOC vs droop vs VSG: tabla comparativa ampliada

| Propiedad | VOC | Droop | VSG/VSM |
|---|---|---|---|
| Inercia explícita | No (ciclo límite) | No | Sí (\(J\) virtual) |
| Sincronización global | Sí (formal, islandina) | No (local) | No |
| Estabilidad gran señal | Sí (ciclo límite = atractor global) | Solo con saturación | Con saturación |
| PLL necesario | No | No | No |
| Respuesta ROCOF | Alta (sin filtro de inercia) | Alta | Baja (filtrada por \(J\)) |
| Arranque robusto | Sí (converge desde cualquier CI) | Requiere inicialización | Requiere inicialización |
| Complejidad impl. | Media (integración ODE RK4) | Baja (PI + droop) | Media-alta (modelo swing) |
| Parámetro de diseño | \(\mu\), \(\kappa\), \(\gamma\) | \(m_p\), \(m_q\), \(\omega_{LPF}\) | \(J\), \(D\), \(m_p\) |

El VOC no tiene inercia explícita: ante un escalón de carga, la frecuencia cambia rápidamente (ROCOF alto). Para aplicaciones que requieren inercia sintética (soporte de frecuencia de red), el VSG es más adecuado. Para microrredes islandinas con múltiples fuentes donde la sincronización robusta es prioritaria, el VOC ofrece las mejores garantías formales.

## 9 — Implementación discreta: RK4 y paso de tiempo

La implementación en DSP integra la ODE del oscilador con Runge-Kutta orden 4 (RK4):
$$v_{k+1}=v_k+\frac{T_s}{6}(k_1+2k_2+2k_3+k_4)$$

**Condición de paso de tiempo:** para resolver el ciclo límite con precisión, \(T_s \leq T_0/100\) donde \(T_0=2\pi/\omega_0=20\,\text{ms}\) a 50 Hz. Por tanto \(T_s \leq 200\,\mu\text{s}\) — compatible con conversores a \(f_s \geq 5\,\text{kHz}\).

**Escalado con potencia nominal:** los parámetros \(\mu\) (velocidad de convergencia de amplitud) y \(K_v\) (ganancia de acoplamiento de corriente) se escalan inversamente con la potencia nominal para que la dinámica sea la misma en cualquier tamaño de convertidor. La amplitud del ciclo límite determina la tensión nominal de salida: \(A_{ss}=2/\sqrt{\kappa}=V_{ref}\).

<div class="cfig"><img src="../figuras/virtual-oscillator-control-analisis.png" alt="ciclo límite Van der Pol, arranque, sincronización de dos VOC y tabla comparativa"><div class="cap">(a) Ciclo límite de Van der Pol en el plano de fase: cualquier condición inicial converge al mismo atractor. (b) Tensión durante el arranque: convergencia al ciclo límite en ~50 ms. (c) Sincronización de dos VOC acoplados: a los 50 ms ambas tensiones son coherentes. (d) Tabla comparativa VOC/Droop/VSG.</div></div>

## Errores comunes
- Elegir \( \alpha \) muy grande: oscilaciones transitorias rápidas que saturan el convertidor.
- Olvidar que la sincronización global garantizada es para redes **islandinas**; en red conectada
  hay que analizar la interacción con la impedancia de red por separado.
- Discretizar con \( T_s \) demasiado grande y perder el ciclo límite.
- No añadir lazo de corriente interno: el VOC no limita corriente de forma natural ante cortocircuito.

## Conceptos relacionados
- [[grid-forming-vs-following]] · [[vsm-inercia]] · [[power-synchronization-control]] · [[matching-control]] · [[droop-control]]

## Referencias
- Johnson et al., *Synthesizing Virtual Oscillators to Control Islanded Inverters*, IEEE TPEL 2016.
- Colombino et al., *Global Phase and Magnitude Synchronization of Coupled Oscillators*, IEEE TAC 2019.
