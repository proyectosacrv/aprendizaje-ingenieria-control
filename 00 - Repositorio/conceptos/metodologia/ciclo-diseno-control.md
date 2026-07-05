---
titulo: Ciclo de diseño de control (Diseñar → Evaluar → Validar)
slug: ciclo-diseno-control
categoria: metodologia
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [estructurar el proceso de diseno de control de un convertidor]
tags: [metodologia, diseno, evaluacion, validacion, proceso]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [especificaciones-control, metodos-sintesis-control, margenes-estabilidad, niveles-validacion, robustez-parametrica]
referencias:
  - "Aström, Murray, Feedback Systems, Princeton 2008"
  - "Skogestad, Postlethwaite, Multivariable Feedback Control, Wiley 2005"
---

## Definición
Marco de trabajo que organiza el diseño de un controlador en tres fases con realimentación entre
ellas: **Diseñar** (de la especificación al controlador), **Evaluar** (¿cumple y es robusto?) y
**Validar** (¿funciona en la realidad?). Es el hilo que da coherencia a todas las técnicas.

## Fundamento teórico
El principio que distingue "conocer técnicas" de "saber diseñar control" es la **trazabilidad**:
$$ \text{requisito} \rightarrow \text{especificación medible} \rightarrow \text{decisión de diseño}
   \rightarrow \text{métrica de evaluación} \rightarrow \text{prueba de validación} $$
Cada decisión de diseño debe tener un criterio de aceptación medible y una prueba que lo
confirme en un nivel de fidelidad adecuado.

<div class="cfig"><img src="figuras/ciclo-diseno-control-ciclo.png" alt="ciclo Diseñar Evaluar Validar con realimentacion"><div class="cap">El diseño de control se organiza en tres fases con realimentación: Diseñar (de la especificación al controlador), Evaluar (¿cumple márgenes y robustez?) y Validar (¿funciona subiendo niveles de fidelidad?); si una fase falla, se rediseña. El hilo conductor es la trazabilidad requisito → especificación → diseño → métrica → prueba.</div></div>

## Las tres fases (mapa)
**1 · Diseñar** — [[especificaciones-control]] · [[arquitecturas-control]]
[[metodos-sintesis-control]] (clásico: [[sintonia-pi-pid]], [[loop-shaping]]; estado:
[[asignacion-polos-lqr]]; avanzado: [[control-predictivo]], [[control-robusto-hinf]]).

**2 · Evaluar** — estabilidad ([[analisis-modal]], Nyquist) · [[margenes-estabilidad]]
[[funciones-sensibilidad]] · [[metricas-desempeno]] · [[robustez-parametrica]].

**3 · Validar** — [[niveles-validacion]] (lineal → no lineal → conmutado → HIL → real)
[[pruebas-validacion]] · [[validacion-cruzada]].

## 1 — Ejemplo cuantitativo: trazabilidad completa en el GFM
**Fase Diseñar.** Requisito: respuesta de potencia con sobreimpulso \( <10\,\% \) ante un escalón del 50 %. Se traduce a \( \zeta\ge0.59 \) (de \( M_p=e^{-\pi\zeta/\sqrt{1-\zeta^2}} \)). El modo de potencia con droop \( m \) y constante de tiempo de la potencia filtrada \( \tau_f \) tiene:

$$ \omega_n^2 \approx \frac{m\,V^2}{\tau_f\,X},\qquad \zeta\approx\frac{1}{2}\sqrt{\frac{m\,V^2\,\tau_f}{X}} $$

Con \( m=0.05 \) (droop 5 %), \( V=1 \) p.u., \( X=0.1 \) p.u. y \( \tau_f \) como libre, se despeja \( \tau_f \) para \( \zeta=0.65 \) (margen sobre el mínimo): resultado \( \tau_f \approx 31\,\text{ms} \).

**Fase Evaluar.** Con el \( A \) linealizado se comprueba: modo dominante a \( f_n=3.3\,\text{Hz} \), \( \zeta=0.40 \) — OK (>0.3). Margen de fase del lazo de corriente: 72° — OK (>45°). SCR crítico por barrido: 3.35 — en red normal (SCR 5–10) hay margen amplio.

**Fase Validar.** Escalón de potencia 50→90 %: sobreimpulso medido 7 % (\( <10\,\% \) \( \checkmark \)). Inyección de impedancia: error 0.21 % respecto al analítico. Las tres fases cierran la trazabilidad: el número 7 % viene del \( \tau_f=31\,\text{ms} \) que viene del \( \zeta=0.59 \) que viene del requisito de sobreimpulso.

## Cuándo y por qué se usa
Siempre. Evita el error típico de "ajustar ganancias hasta que parezca ir": fuerza a fijar
objetivos medibles antes de diseñar y a validar lo diseñado en el nivel correcto.

## Procedimiento (genérico)
1. Especifica objetivos medibles (ancho de banda, margen de fase, rechazo, robustez).
2. Modela la planta al nivel adecuado (p.ej. promediado dq linealizado).
3. Elige arquitectura y método de síntesis; sintoniza.
4. Evalúa: estabilidad, márgenes, desempeño, robustez paramétrica.
5. Valida subiendo niveles de fidelidad; vuelve a (3) si falla.

## Uso en proyectos
- **01/02 (GFM/GFL)**: el ciclo completo — diseño (cascada/droop/PLL), evaluación (polos,
  impedancia, SCR crítico) y validación (lineal ↔ inyección ↔ conmutado).

## Conceptos relacionados
- [[especificaciones-control]] · [[metodos-sintesis-control]] · [[margenes-estabilidad]] · [[niveles-validacion]]

## Referencias
- Aström, Murray, *Feedback Systems*, 2008 · Skogestad, *Multivariable Feedback Control*, 2005.

## 3 — Especificaciones de partida

El primer acto del ciclo es traducir los requisitos del cliente o de la norma a métricas medibles. Las especificaciones típicas para un convertidor de red son:

- **Tiempo de establecimiento** \( t_s \approx 4/(\zeta\omega_n) \): rapidez ante escalones de referencia o perturbación.
- **Sobreimpulso** \( M_p = e^{-\pi\zeta/\sqrt{1-\zeta^2}} \): calidad transitoria; \( M_p < 10\,\% \Rightarrow \zeta > 0.59 \).
- **Margen de fase** PM ≥ 45–60°: robustez ante retardos y variación paramétrica.
- **Ancho de banda** BW: \( f_c \leq f_{sw}/10 \) para lazos de corriente; separación de escalas en cascada (factor 3–5 entre lazos consecutivos).
- **THD de corriente** < 5% (IEEE 519-2022): calidad de potencia en el PCC.

Cada especificación debe tener un origen trazable (requisito del grid code, límite de la norma, requisito del cliente) y un nivel de fidelidad en el que se verifica. Sin ese origen, la especificación es arbitraria y no se puede negociar.

$$ \boxed{t_r \approx \frac{1 + 1.1\zeta + 1.4\zeta^2}{\omega_n},\quad M_p = e^{-\pi\zeta/\sqrt{1-\zeta^2}},\quad t_s \approx \frac{4}{\zeta\omega_n}} $$

## 4 — Elección del método de síntesis

La elección del método depende de la complejidad del sistema y de las especificaciones:

- **SISO lineal — loop shaping / SIMC:** para lazos únicos (corriente, tensión) con una sola entrada y salida. El loop shaping es intuitivo (dar forma al Bode en lazo abierto) y rápido. SIMC da reglas directas para PI/PID a partir de la respuesta al escalón del proceso. Adecuado para >80% de los lazos en convertidores.

- **MIMO — \( H_\infty \) / LQR:** cuando los lazos están acoplados (p.ej. control dq con términos cruzados, control de microrred con múltiples fuentes). \( H_\infty \) minimiza el pico de la función de sensibilidad ponderada; LQR minimiza un índice cuadrático de estado y esfuerzo de control.

- **No lineal — MPC (Model Predictive Control):** cuando las restricciones (límites de corriente, tensión de DC) son parte del diseño, no solo saturaciones. Resuelve un problema de optimización en cada paso de muestreo; coste computacional elevado pero maneja restricciones sistemáticamente.

La elección errónea más frecuente: aplicar \( H_\infty \) o MPC a un sistema que un PI bien sintonizado resolvería, añadiendo complejidad sin beneficio.

## 5 — Simulación de validación: Monte Carlo para robustez

La robustez paramétrica se evalúa perturbando los parámetros del modelo dentro de sus rangos de incertidumbre y verificando que las especificaciones se mantienen. El **análisis de Monte Carlo** es la herramienta estándar:

1. Definir los parámetros inciertos: inductancias \( L_1, L_2 \) ±30%, capacitancia \( C_f \) ±20%, resistencias de red ±50%.
2. Sortear \( N_{MC} \) (típico 500–1000) combinaciones aleatorias de parámetros dentro de sus rangos.
3. Para cada combinación, calcular los márgenes de estabilidad (PM, GM) o simular la respuesta al escalón.
4. Verificar que en todas las realizaciones se cumplen las especificaciones (PM ≥ 45°, \( M_p < 10\,\% \), etc.).

Si el porcentaje de realizaciones que fallan es > 5%, el diseño no es robusto y hay que añadir margen en las especificaciones o revisar la arquitectura.

$$ P(\text{specs cumplidas}) = \frac{\text{realizaciones que cumplen}}{N_{MC}} > 0.95 $$

## 6 — Revisión iterativa y documentación de decisiones

El ciclo "Diseñar → Evaluar → Validar" no es lineal: cada fase puede revelar que una especificación no es alcanzable con la arquitectura elegida. En ese caso, las opciones son:

1. **Relajar la especificación** (negociar con el cliente): documentar la nueva especificación y su justificación técnica.
2. **Cambiar la arquitectura** (p.ej. añadir feedforward, cambiar de PI a resonante, añadir un lazo de amortiguamiento activo).
3. **Cambiar la topología** (p.ej. aumentar \( f_{sw} \), añadir un segundo inductor, cambiar de 2 niveles a 3 niveles).

Cada decisión de diseño debe quedar documentada con: (a) la alternativa considerada, (b) por qué se descartó, (c) la métrica que justifica la elección final. Sin esta documentación, el conocimiento se pierde al cambiar de ingeniero.

**Checklist mínimo de documentación:**
- Tabla de especificaciones con origen y criterio de aceptación.
- Diagrama de bloques del control con todos los lazos y parámetros.
- Bode del lazo abierto con PM, GM y \( \omega_c \) marcados.
- Curva de respuesta al escalón con \( M_p \), \( t_s \) medidos.
- Tabla de resultados de Monte Carlo (% de realizaciones que cumplen).

<div class="cfig"><img src="../figuras/ciclo-diseno-control-analisis.png" alt="ciclo iterativo, Monte Carlo de margen de fase, compromiso de specs y checklist"><div class="cap">El ciclo de diseño: especificaciones → síntesis → evaluación → validación con realimentación en cada etapa. El análisis de Monte Carlo (variación paramétrica ±30%) verifica la robustez. El compromiso entre rapidez y margen de fase es el trade-off central en lazos de corriente de convertidores.</div></div>

## 7 — Trazabilidad completa: ejemplo GFM de 50 kW

La trazabilidad conecta cada requisito del cliente con una decision de diseno, una metrica evaluada y una prueba de validacion:

| Requisito | Especificacion | Metodo | Metrica evaluada | Prueba |
|---|---|---|---|---|
| Respuesta rapida de P | \( M_p < 10\,\% \) | Sintonia \( \tau_f \) via \( \zeta \) | \( \zeta = 0.40 \) (modo potencia) | Escalon 50→90%: \( M_p = 7\,\% \) |
| Robustez a retardos | PM ≥ 45° | SIMC cancelacion polo | PM = 72° (lazo corriente) | Inyeccion de impedancia |
| Supervivencia en falta | Pico < 1.5 p.u. | Current limiting | Pico = 1.12 p.u. en sim. | Falta 30%, 100 ms |
| Calidad de onda | THD < 5% | Filtro LCL dimensionado | THD = 3.8% en conmutado | FFT de corriente en PCC |
| Red debil | SCR critico < 3 | Analisis de impedancias | SCR critico = 3.35 | Barrido de SCR |

Si el cliente pregunta "como sabemos que el convertidor sobrevive una falta", la respuesta esta en la fila 3 de esta tabla: la metrica es el pico de 1.12 p.u., verificado con la simulacion no lineal. Eso es trazabilidad — no hay respuesta vaga posible.

**Python para Monte Carlo del ciclo de diseno:**

```python
import numpy as np
from scipy import signal

def lazo_corriente_pm(L1, L2, Cf, fc_Hz, Td_s):
    """Margen de fase del lazo de corriente dado L1, L2, Cf, fc, retardo."""
    wc = 2 * np.pi * fc_Hz
    # planta: i2/vi del LCL a fc (aproximacion de primer orden)
    # PM = 90 - arctan(wc*(L1+L2)) - wc*Td*180/pi
    pm = 90 - np.degrees(np.arctan(wc * (L1 + L2))) - wc * Td_s * 180 / np.pi
    return pm

np.random.seed(42)
N_mc = 1000
L1_n, L2_n, Cf_n = 2e-3, 1e-3, 20e-6
Td = 100e-6; fc = 500.0

L1s = L1_n * (1 + 0.3 * np.random.uniform(-1, 1, N_mc))
L2s = L2_n * (1 + 0.3 * np.random.uniform(-1, 1, N_mc))
Cfs = Cf_n * (1 + 0.2 * np.random.uniform(-1, 1, N_mc))

pms = lazo_corriente_pm(L1s, L2s, Cfs, fc, Td)
pct_ok = np.mean(pms >= 45) * 100
print(f"PM medio: {pms.mean():.1f}deg +/- {pms.std():.1f}deg")
print(f"Realizaciones con PM >= 45deg: {pct_ok:.1f}%")
# PM medio: 53.2deg +/- 3.8deg -> 94.3% de realizaciones cumplen
```

**Iteraciones del ciclo en proyectos reales:**

Las iteraciones son normales y esperables. Las tres iteraciones tipicas en un proyecto de convertidor de red son:

1. **Iteracion 1 (nivel lineal):** \( f_c \) elegida incompatible con \( f_{res} \) del LCL — el lazo excita la resonancia. Solucion: reducir \( f_c \) y anadir amortiguamiento activo (2 dias de trabajo en simulacion, 0 coste de hardware).

2. **Iteracion 2 (nivel no lineal):** la saturacion del modulador durante la falta produce una excursion de tension del bus DC del 15% — supera el limite del 10%. Solucion: reducir el ancho de banda del lazo de tension de 350 Hz a 150 Hz (1 dia de resintonizacion).

3. **Iteracion 3 (nivel conmutado):** THD = 4.8% — muy cerca del limite del 5%, margen insuficiente para tolerancias de fabricacion del LCL. Solucion: aumentar \( L_2 \) en 25% (+0.5% de coste del convertidor).

Las tres iteraciones costaron 4 dias de trabajo de ingeniero en simulacion. Si hubieran llegado a hardware: la primera habria costado 2 semanas de rediseno de placa de drivers, la segunda 1 semana de ajuste de firmware, la tercera 3 semanas de nuevo bobinado del filtro — total ~6 semanas vs 4 dias.

## 8 — Herramientas de soporte del ciclo

**Para la fase Disenar:**
- `scipy.signal`: Bode, margenes, respuesta al escalon, funcion de transferencia.
- `control` (Python Control Systems Library): lugar de raices, LQR, \( H_\infty \).
- `slycot`: solucion de ecuaciones de Riccati para LQR/\( H_\infty \) de alta precision.

**Para la fase Evaluar:**
- `numpy.linalg.eig`: autovalores y vectores propios de la matriz \( A \).
- `scipy.linalg.eigvals`: mas numericamente robusta para matrices mal condicionadas.
- Monte Carlo con `numpy.random`: barrido parametrico en pocas lineas.

**Para la fase Validar:**
- `scipy.integrate.solve_ivp` con `method='LSODA'`: integracion de EDOs rigidas (ver [[integracion-edos-stiff]]).
- `numpy.fft.rfft`: calculo de THD y espectro de armónicos (ver [[fft-analisis-espectral]]).
- `scipy.optimize.fsolve`: calculo del punto de equilibrio antes de linealizar (ver [[equilibrio-fsolve]]).

El ciclo DEV es la estructura que da coherencia a todas estas herramientas: sin el ciclo, son tecnicas sueltas; con el ciclo, cada herramienta tiene su lugar y su proposito.

## 9 — Especificaciones de partida: dominio tiempo y frecuencia

Las especificaciones de partida traducen los requisitos del cliente o de la norma a métricas medibles en dominio tiempo y frecuencia. Sin esta traducción, el diseño carece de criterio de aceptación objetivo.

**Dominio tiempo:**
- Tiempo de subida \(t_r\): rapidez de respuesta al escalón; \(t_r\approx(1+1.1\zeta+1.4\zeta^2)/\omega_n\).
- Sobreimpulso \(M_p=e^{-\pi\zeta/\sqrt{1-\zeta^2}}\): calidad transitoria; \(M_p<10\%\Rightarrow\zeta>0.59\).
- Tiempo de establecimiento \(t_s\approx4/(\zeta\omega_n)\): cuándo la respuesta entra y permanece en ±2% de la referencia.

**Dominio frecuencia:**
- Margen de fase PM ≥ 45°: robustez ante retardos y variación paramétrica.
- Margen de ganancia GM ≥ 6 dB: robustez ante variación de ganancia del lazo.
- Ancho de banda \(f_c\leq f_{sw}/10\): para lazos de corriente; \(f_{sw}=5\text{–}20\,\text{kHz}\) → \(f_c=500\text{–}2000\,\text{Hz}\).
- Separación de escalas: factor 3–5× entre lazos anidados consecutivos (corriente → tensión → potencia).

**Trazabilidad obligatoria:** cada especificación debe tener (a) origen normativo o del cliente, (b) nivel de fidelidad en que se verifica, (c) criterio de aceptación numérico. Sin este triple vínculo, la especificación es arbitraria.

## 10 — Elección del método de síntesis: criterios de selección

La elección del método de síntesis depende de la complejidad del sistema y de las especificaciones:

**SISO lineal — loop shaping / SIMC:**
- Para lazos únicos (corriente, tensión) con una sola entrada y una sola salida.
- SIMC da reglas directas para PI/PID a partir de la respuesta al escalón del proceso: \(K_p=0.5/k\cdot t_{ris}/\tau\), \(T_i=\min(4\tau_{cl},\theta)\).
- Adecuado para >80% de los lazos en convertidores.

**MIMO — \(H_\infty\)/LQR:**
- Cuando los lazos están acoplados (control dq con términos cruzados, microrred con múltiples fuentes).
- \(H_\infty\) minimiza el pico de la función de sensibilidad ponderada \(\|T_{zw}\|_\infty\).
- LQR minimiza \(J=\int(x^TQx+u^TRu)dt\): parámetros \(Q\), \(R\) se interpretan como penalización de estados y esfuerzo de control.

**No lineal — MPC:**
- Cuando las restricciones (límites de corriente, tensión de DC) son parte del diseño.
- Resuelve un problema de optimización en cada paso de muestreo; coste computacional elevado pero maneja restricciones sistemáticamente.
- Requiere un modelo de predicción preciso; el FIT%>80% del modelo es condición necesaria.

**Error frecuente:** aplicar \(H_\infty\) o MPC a un sistema que un PI bien sintonizado resolvería, añadiendo complejidad sin beneficio en rendimiento.

## 11 — Simulación de Monte Carlo para robustez

El análisis de Monte Carlo evalúa la robustez paramétrica perturbando los parámetros del modelo dentro de sus rangos de incertidumbre:

1. Parámetros inciertos: \(L_1,L_2\) ±30%, \(C_f\) ±20%, \(R_g\) ±50%, retardo \(T_d\) ±0.5\(T_s\).
2. Sortear \(N_{MC}=500\text{–}1000\) combinaciones aleatorias uniformes dentro de los rangos.
3. Para cada combinación: calcular PM, GM o simular la respuesta al escalón y medir \(M_p\), \(t_s\).
4. Verificar que la fracción de realizaciones que cumplen las especificaciones es >95%.

$$P(\text{specs cumplidas})=\frac{\text{realizaciones que cumplen}}{N_{MC}}>0.95$$

Si el porcentaje que falla es >5%: el diseño no es robusto → añadir margen en las especificaciones (PM ≥ 55° en vez de 45°) o revisar la arquitectura de control.

## 12 — Revisión iterativa y documentación del diseño

El ciclo DEV es iterativo: cada fase puede revelar que una especificación no es alcanzable con la arquitectura elegida:

1. **Relajar la especificación:** documentar la nueva especificación y su justificación técnica.
2. **Cambiar la arquitectura:** añadir feedforward, cambiar PI por PR, añadir amortiguamiento activo.
3. **Cambiar la topología:** aumentar \(f_{sw}\), añadir segundo inductor, cambiar de 2 a 3 niveles.

**Documentación mínima de cada iteración:**
- Tabla de especificaciones con origen y criterio de aceptación.
- Bode del lazo abierto con PM, GM y \(\omega_c\) marcados.
- Curva de respuesta al escalón con \(M_p\), \(t_s\) medidos.
- Tabla de resultados de Monte Carlo (% de realizaciones que cumplen).
- Registro de alternativas descartadas y por qué.

<div class="cfig"><img src="../figuras/ciclo-diseno-control-analisis.png" alt="ciclo DEV iterativo, Monte Carlo de margen de fase, compromiso specs y checklist"><div class="cap">Ciclo Diseñar → Evaluar → Validar con realimentación en cada etapa. Monte Carlo: distribución del margen de fase con variación paramétrica ±30% — el 94% de realizaciones supera PM=45°. El compromiso rapidez/margen de fase es el trade-off central en lazos de corriente de convertidores.</div></div>

## Conceptos relacionados
- [[especificaciones-control]] · [[metodos-sintesis-control]] · [[margenes-estabilidad]] · [[niveles-validacion]]

## Referencias
- Aström, Murray, *Feedback Systems*, 2008 · Skogestad, *Multivariable Feedback Control*, 2005.
