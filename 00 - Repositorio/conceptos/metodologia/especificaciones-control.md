---
titulo: Especificaciones de control (traducir requisitos a métricas)
slug: especificaciones-control
categoria: metodologia
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [fijar objetivos medibles antes de disenar]
tags: [especificaciones, ancho-de-banda, margen, requisitos, diseno]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [ciclo-diseno-control, metricas-desempeno, margenes-estabilidad, metodos-sintesis-control]
referencias:
  - "Aström, Murray, Feedback Systems, Princeton 2008 (cap. 11)"
---

## Definición
Primer paso del diseño: convertir requisitos cualitativos ("rápido", "estable", "robusto") en
**números objetivo** que guían la síntesis y sirven de criterio de aceptación.

## Fundamento teórico
Especificaciones típicas y su forma medible:
- **Velocidad / ancho de banda** \( \omega_c \) (frecuencia de cruce de ganancia). Regla:
  \( t_{s}\approx 4/(\zeta\omega_n) \), \( \omega_c \) marca la rapidez del lazo.
- **Amortiguamiento** \( \zeta \) (o sobreimpulso \( M_p\approx e^{-\pi\zeta/\sqrt{1-\zeta^2}} \)).
- **Robustez**: margen de fase \( \ge 40\text{–}60° \), margen de ganancia \( \ge 6 \) dB,
  pico de sensibilidad \( M_s \le 2 \) (≈6 dB).
- **Error en régimen**: tipo de sistema / ganancia DC para anular error a escalón/rampa.
- **Rechazo de perturbación** y atenuación de ruido (forma de S y T, ver [[funciones-sensibilidad]]).

En convertidores hay además restricciones físicas: \( \omega_c < \) (1/5–1/10) de \( f_{sw} \),
y separación de escalas entre lazos en cascada.

<div class="cfig"><img src="figuras/especificaciones-control-mp-zeta.png" alt="relacion entre sobreimpulso y amortiguamiento"><div class="cap">Ejemplo de traducción de un requisito a una métrica: el sobreimpulso de un sistema de 2º orden $M_p=e^{-\pi\zeta/\sqrt{1-\zeta^2}}$ depende solo del amortiguamiento. Fijar $M_p\le10\%$ se convierte en una especificación medible sobre el diseño: $\zeta\ge0.59$. Así cada requisito cualitativo pasa a número objetivo y criterio de aceptación.</div></div>

## 1 — Ejemplo cuantitativo: traducción de requisitos a números objetivo en un GFL
**Requisito 1 — rapidez:** el lazo de corriente debe seguir una rampa de 0 a 1 p.u. en menos de 2 ms. Ello impone \( t_s<2\,\text{ms} \) ↔ \( \omega_{ci}>4/t_s=4/0.002=2000 \) rad/s ↔ \( f_{ci}>318\,\text{Hz} \). Se elige \( f_{ci}=500\,\text{Hz} \) (con \( f_{sw}=5\,\text{kHz} \), factor 10 cumplido \( \checkmark \)).

**Requisito 2 — robustez:** margen de fase mínimo 45° para tolerancia al retardo de cómputo de \( T_s/2=100\,\mu\text{s} \). El retardo puro añade fase \( -\omega\,T_d \): a \( \omega_{ci}=2\pi\times500 \), la pérdida de fase es \( 2\pi\times500\times100\times10^{-6}\times180/\pi=18° \). Partiendo de 72° (cancelación de polo puro), se queda en 54° — cumple el límite de 45° \( \checkmark \).

**Requisito 3 — error en régimen.** Para anular error a escalón de corriente se necesita al menos un integrador en el lazo (acción integral del PI \( \checkmark \)).

**Traducción final:**

| Requisito | Métrica | Valor objetivo |
|---|---|---|
| Rapidez | \( f_{ci} \) | 500 Hz |
| Robustez | margen de fase | ≥ 45° |
| Precisión | error en escalón | 0 (integrador) |
| Compatibilidad PWM | \( f_{ci}/f_{sw} \) | ≤ 1/10 |

## Cuándo y por qué se usa
Antes de elegir cualquier método. Sin especificaciones medibles no hay forma de saber si el
diseño "está bien" ni de validarlo objetivamente.

## Procedimiento (genérico)
1. Lista los requisitos del sistema (rapidez, precisión, robustez, límites físicos).
2. Tradúcelos a métricas: \( \omega_c, \zeta/M_p, \) márgenes, \( M_s \), error, anchos de
   banda relativos de lazos en cascada.
3. Comprueba compatibilidad (p.ej. ancho de banda vs \( f_{sw} \), vs resonancia del filtro).
4. Documenta cada métrica como **criterio de aceptación** para la fase de evaluación/validación.

## Parámetros y valores típicos (convertidores)
Lazo de corriente: \( f_c \) ≈ \( f_{sw}/10 \). Lazo de tensión: ≈ \( f_{ci}/(3\text{–}5) \).
Margen de fase 45–60°, \( M_s \) < 2. Droop/PLL: el lazo más lento (Hz–decenas de Hz).

## Errores comunes
- "Ajustar hasta que vaya" sin objetivos → no es reproducible ni validable.
- Pedir ancho de banda incompatible con \( f_{sw} \) o con la resonancia del filtro.

## Uso en proyectos
- **01/02**: lazo de corriente ~1 kHz, tensión ~350 Hz, droop/PLL ~Hz; margen y \( \zeta \)
  objetivo guiaron la sintonía (modo de potencia GFM a \( \zeta=0.40 \)).

## Conceptos relacionados
- [[ciclo-diseno-control]] · [[metricas-desempeno]] · [[margenes-estabilidad]]

## Referencias
- Aström, Murray, *Feedback Systems*, cap. 11.

## 3 — Especificaciones en tiempo: fórmulas exactas

Para un sistema de segundo orden con función de transferencia \( G(s) = \omega_n^2/(s^2 + 2\zeta\omega_n s + \omega_n^2) \), las especificaciones en el dominio temporal son:

**Tiempo de subida** (10%→90%):

$$ t_r \approx \frac{1 + 1.1\zeta + 1.4\zeta^2}{\omega_n} $$

Válido para \( 0.3 \leq \zeta \leq 0.8 \). Para \( \zeta = 0.7 \): \( t_r \approx 1.93/\omega_n \).

**Sobreimpulso máximo:**

$$ M_p = e^{-\pi\zeta/\sqrt{1-\zeta^2}} \times 100\,\% $$

La curva \( M_p(\zeta) \) es monotónicamente decreciente: \( \zeta=0.5 \rightarrow M_p=16\,\% \); \( \zeta=0.707 \rightarrow M_p=4.3\,\% \); \( \zeta=1 \rightarrow M_p=0 \). El requisito más habitual en convertidores es \( M_p < 10\,\% \Rightarrow \zeta \geq 0.59 \).

**Tiempo de establecimiento** al ±2%:

$$ t_s \approx \frac{4}{\zeta\omega_n} $$

La relación \( t_s \approx 4\tau \) con \( \tau = 1/(\zeta\omega_n) \) la constante de decaimiento de la envolvente exponencial. Para \( t_s < 100\,\text{ms} \) con \( \zeta=0.6 \): \( \omega_n > 4/(0.6 \times 0.1) = 67\,\text{rad/s} \Rightarrow f_n > 10.6\,\text{Hz} \).

$$ \boxed{t_r \cdot \omega_n \approx 1.9\;(\zeta=0.7);\quad M_p(\zeta=0.59)=10\,\%;\quad t_s = \frac{4}{\zeta\omega_n}} $$

## 4 — Especificaciones en frecuencia: PM, GM y Ms

Las especificaciones en frecuencia describen la robustez del lazo en términos del diagrama de Bode de la función de lazo abierto \( L(j\omega) = C(j\omega)G(j\omega) \):

**Margen de fase** PM: ángulo de \( L(j\omega_c) \) respecto a −180° en la frecuencia de cruce de ganancia \( \omega_c \):

$$ \text{PM} = 180° + \angle L(j\omega_c) \geq 45° $$

PM > 45° garantiza tolerancia a un retardo puro de \( T_d < \text{PM}/\omega_c \cdot (\pi/180°) \). Para PM=45° y \( \omega_c = 2\pi \times 500\,\text{Hz} \): tolerancia de \( T_d < 250\,\mu\text{s} \).

**Margen de ganancia** GM: inverso de \( |L(j\omega_\phi)| \) en la frecuencia de cruce de fase \( \omega_\phi \):

$$ \text{GM} = -20\log_{10}|L(j\omega_\phi)| \geq 6\,\text{dB} $$

**Pico de sensibilidad** \( M_s = \|S\|_\infty \) donde \( S = 1/(1+L) \): distancia mínima del Nyquist al punto −1. La relación práctica:

$$ M_s < 2 \;\Leftrightarrow\; \text{PM} > 29°\;\text{ y }\;\text{GM} > 6\,\text{dB (aprox.)} $$

**Frecuencia de cruce mínima:** la rapidez del lazo impone \( \omega_c > 2\pi \cdot \text{BW}_{min} \), donde \( \text{BW}_{min} \) se deriva del \( t_s \) requerido. Límite superior: \( \omega_c < 2\pi \cdot f_{sw}/10 \) para evitar interacción con la conmutación.

## 5 — Especificaciones de calidad de potencia

Para convertidores conectados a red, las especificaciones incluyen los límites normativos:

**THD de corriente (IEEE 519-2022):**

$$ \text{THD}_I = \frac{\sqrt{\sum_{h=2}^{\infty} I_h^2}}{I_1} \times 100\,\% < 5\,\% \quad (I_{sc}/I_L < 20) $$

Armónico individual de orden h < 11: límite 4% de \( I_1 \).

**Factor de potencia** FP > 0.95 (desplazamiento + distorsión): garantiza que la corriente reactiva fundamental y los armónicos no generan pérdidas excesivas en la red.

**Desequilibrio de tensión** VUF < 2% (EN 50160):

$$ \text{VUF} = \frac{V_{neg}}{V_{pos}} \times 100\,\% < 2\,\% $$

donde \( V_{neg} \) y \( V_{pos} \) son las componentes de secuencia negativa y positiva de las tensiones de fase.

**Flicker** \( P_{st} < 1 \) (IEC 61000-3-3): las variaciones rápidas de potencia (modulaciones a 0.5–25 Hz) no deben causar parpadeo perceptible. En data centers con cargas GPU pulsantes, este límite puede ser el más restrictivo.

## 6 — Priorización y ejemplo completo para inversor GFL de 100 kW

**Jerarquía de especificaciones:** seguridad física (corriente pico < 1.5 p.u. en falta) > robustez (PM ≥ 45°, GM ≥ 6 dB) > rendimiento dinámico (\( t_s \), \( M_p \)) > calidad de potencia (THD, FP).

**Ejemplo — inversor GFL de 100 kW, 400 V, \( f_{sw} = 10\,\text{kHz} \):**

| Requisito | Especificación | Métrica | Valor objetivo |
|---|---|---|---|
| Corriente pico en falta | Seguridad del IGBT | Pico \( < 1.5\,\text{p.u.} \) | 150 A (1 p.u. = 100 A) |
| Robustez lazo de corriente | Tolerancia al retardo | PM ≥ 45° | PM ≥ 45° en \( f_c = 800\,\text{Hz} \) |
| Rapidez de corriente | Seguimiento de referencia | \( t_s < 2\,\text{ms} \) | \( f_c \geq 500\,\text{Hz} \) |
| Sobreimpulso de corriente | Calidad transitoria | \( M_p < 10\,\% \) | \( \zeta \geq 0.59 \) |
| Armónicos | IEEE 519-2022 | THD_I < 5% | Filtro LCL con 60 dB en \( f_{sw} \) |
| Factor de potencia | Norma de red | FP > 0.95 | Control Q = 0 (o referencia Q) |
| Compatibilidad PWM | Evitar interacción | \( f_c < f_{sw}/10 \) | \( f_c < 1000\,\text{Hz} \) |

Estas especificaciones se derivan de los requisitos físicos, normativos y de diseño. Cada una tiene un criterio de aceptación medible que guía la síntesis y la validación.

<div class="cfig"><img src="../figuras/especificaciones-control-analisis.png" alt="respuesta escalón con specs, Bode con PM/GM, THD con límites normativos y tabla de specs"><div class="cap">Especificaciones en tiempo (Ms, ts marcados en la respuesta escalón), en frecuencia (PM y GM en el Bode), de calidad de potencia (THD con límite IEEE 519) y tabla completa para un GFL de 100 kW. Cada especificación tiene su criterio numérico y su prueba de validación.</div></div>

## 7 — Separacion de escalas en lazos en cascada

En un convertidor con control en cascada (corriente → tension → potencia), la separacion de escalas entre lazos garantiza que el lazo externo ve al lazo interno como instantaneo:

$$ f_{c,\text{inner}} \geq k \cdot f_{c,\text{outer}}, \quad k = 3\text{–}10 $$

**Especificaciones tipicas en cascada para un GFM de 50 kW:**

| Lazo | \( f_c \) tipica | Razon de separacion | Limitante |
|---|---|---|---|
| Corriente (innermost) | 500–1000 Hz | — | \( f_{sw}/10 \) |
| Tension | 150–300 Hz | 3–5× sobre corriente | Dinamica condensador |
| Droop/potencia | 3–10 Hz | 30–100× sobre tension | Estabilidad de red |
| PLL (GFL) | 10–30 Hz | 50× sobre corriente | No interac. con modo de potencia |

Con \( k < 2 \), los lazos interactuan y el analisis de estabilidad requiere el modelo completo del sistema en cascada — no basta analizar cada lazo por separado.

**Verificacion de compatibilidad de especificaciones:**

Antes de sintonizar, verificar que el conjunto de especificaciones no es contradictorio:

1. **Ancho de banda vs resonancia LCL:** \( f_c \) debe estar fuera de la zona \( f_{res}/3 < f_c < 3\,f_{res} \). Si \( f_{res} = 1.2\,\text{kHz} \) y se quiere \( f_c = 1\,\text{kHz} \): la razon es 0.83 — zona peligrosa. Solucion: anadir amortiguamiento activo.

2. **Sobreimpulso vs margen de fase:** para \( M_p < 10\,\% \) se necesita \( \zeta > 0.59 \), lo que equivale a PM > 59°. Si la especificacion de PM era solo 45°, hay conflicto — prevalece la mas restrictiva: PM > 59°.

3. **Tiempo de establecimiento vs ancho de banda:**
$$ f_c \geq \frac{4}{t_s \cdot \zeta \cdot 2\pi / 3} $$
Para \( t_s = 2\,\text{ms} \), \( \zeta = 0.6 \): \( f_c \geq 530\,\text{Hz} \). Si \( f_{sw} = 5\,\text{kHz} \): limite de ancho de banda = 500 Hz. Incompatible — hay que aumentar \( f_{sw} \) o relajar \( t_s \).

```python
import numpy as np

def verificar_specs(fc_Hz, fsw_Hz, fres_Hz, Mp_pct, ts_s, zeta, Td_s):
    """Verifica compatibilidad de un conjunto de especificaciones de control."""
    res = {}
    # 1. fc vs fsw
    res['fc_vs_fsw'] = {'ok': fc_Hz <= fsw_Hz/10,
                         'msg': f"fc/fsw = {fc_Hz/fsw_Hz:.2f} (lim 0.1)"}
    # 2. fc vs fres LCL
    ratio = fc_Hz / fres_Hz
    res['fc_vs_fres'] = {'ok': ratio < 1/3 or ratio > 3,
                          'msg': f"fc/fres = {ratio:.2f} (evitar 1/3..3)"}
    # 3. Mp vs zeta
    Mp_calc = np.exp(-np.pi*zeta/np.sqrt(1-zeta**2))*100
    res['Mp'] = {'ok': Mp_calc <= Mp_pct,
                  'msg': f"Mp(zeta={zeta:.2f})={Mp_calc:.1f}% (lim {Mp_pct}%)"}
    # 4. ts vs fc
    fc_min = 4/(zeta*ts_s*2*np.pi/3)/(2*np.pi)
    res['ts_fc'] = {'ok': fc_Hz >= fc_min,
                     'msg': f"fc_min_para_ts={fc_min:.0f}Hz (actual {fc_Hz}Hz)"}
    return res

specs = verificar_specs(500, 10000, 1200, 10, 2e-3, 0.6, 100e-6)
for k, v in specs.items():
    print(f"{'OK' if v['ok'] else 'FALLO':5} {k}: {v['msg']}")
```

## 8 — Especificaciones de robustez parametrica

Ademas de las especificaciones nominales, el diseno debe ser robusto a la variacion de parametros de la planta. Las especificaciones de robustez mas comunes son:

**Robustez a variacion de inductancia:**

$$ \text{PM}(L_1 + \Delta L_1) \geq 45° \quad \forall\, |\Delta L_1| \leq 30\,\% $$

En un lazo de corriente PI con cancelacion de polo (\( \omega_z = R/L_1 \)), una variacion de \( L_1 \) en +30% desplaza el cero del PI y deja un polo real no cancelado a \( \omega = R/1.3L_1 \). El efecto sobre el PM es pequeno (< 5°) si \( \omega_z \ll \omega_c \), pero puede ser significativo si estan cerca.

**Robustez al retardo de computo:**

$$ \text{PM} - T_d \cdot \omega_c \cdot \frac{180°}{\pi} \geq 45° $$

Para asegurar PM > 45° con retardo \( T_d = 150\,\mu\text{s} \) y \( f_c = 500\,\text{Hz} \): PM nominal necesario \( > 45° + 150\times10^{-6} \times 2\pi\times500 \times 57.3° = 45° + 27° = 72° \). Esta es la razon por la que muchos disenos apuntan a PM = 70-80° en lugar del limite de 45°.

**Robustez al SCR de la red:**

$$ \text{PM}(\text{SCR}=\text{SCR}_{min}) \geq 45° $$

Con SCR bajo (red debil), la impedancia de la red aumenta y la carga vista por el convertidor cambia. El margen de fase del lazo de corriente puede caer varios grados al reducir el SCR de 10 a 3. Verificar con el modelo completo convertidor + red.

## 9 — Errores comunes al especificar

**Error 1 — especificar el ancho de banda sin considerar el retardo:**

Se especifica \( f_c = 1\,\text{kHz} \) con PM = 45°, ignorando que el retardo de computo \( T_d = 150\,\mu\text{s} \) consume 54° de margen de fase a esa frecuencia. El diseno que cumple PM = 45° en el modelo ideal solo tiene -9° de margen real — completamente inestable.

**Error 2 — no especificar la banda de frecuencias para las especificaciones de amplitud:**

"THD < 5%" no especifica en que rango de frecuencias. La norma IEEE 519-2022 define explicitamente los armónicos a considerar (2° a 50° para 50/60 Hz), el punto de medicion (PCC) y el periodo de observacion (10 min, 99° percentil). Una medicion con ventana de 1 ciclo puede dar un THD muy diferente al de la ventana normativa de 10 ciclos.

**Error 3 — confundir especificaciones de lazo abierto con lazo cerrado:**

El PM y GM son metricas del lazo abierto. El \( M_p \) y \( t_s \) son metricas del lazo cerrado. Para un sistema de segundo orden, la relacion es aproximada (\( \text{PM} \approx 100\zeta \) para \( \zeta < 0.7 \)); para sistemas de orden superior con ceros no minima fase, la relacion puede ser completamente diferente.
