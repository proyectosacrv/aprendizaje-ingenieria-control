---
titulo: Pruebas de validación (escalón, perturbación, inyección, falta)
slug: pruebas-validacion
categoria: metodologia
tipo: metodo
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [definir que ensayos confirman cada especificacion]
tags: [ensayos, escalon, perturbacion, inyeccion, falta, validacion]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [niveles-validacion, validacion-cruzada, medicion-impedancia-inyeccion, especificaciones-control]
referencias:
  - "Teodorescu et al., Grid Converters for PV and Wind Power Systems, Wiley 2011"
---

## Definición
Catálogo de ensayos que confirman, cada uno, una especificación concreta. La regla: **a cada
especificación, su prueba**.

## Fundamento teórico (ensayos típicos)
- **Escalón de referencia**: mide \( M_p, t_s, e_{ss} \) → desempeño de seguimiento.
- **Escalón de perturbación / carga**: mide el rechazo (caída y recuperación) → robustez del lazo.
- **Barrido / inyección de pequeña señal**: mide la respuesta en frecuencia o la **impedancia**
  (ver [[medicion-impedancia-inyeccion]]) → valida el modelo lineal y la robustez en frecuencia.
- **Falta / hueco de tensión**: gran señal → activa el [[current-limiting]] y prueba la
  supervivencia y la sincronización.
- **Arranque / black-start, cambio de modo**: prueba transitorios de puesta en marcha.
- **Variación paramétrica** (cambiar SCR, potencia): liga con [[robustez-parametrica]].

<div class="cfig"><img src="figuras/pruebas-validacion-ensayos.png" alt="cuatro ensayos tipicos de validacion de control"><div class="cap">A cada especificación, su ensayo: el escalón de referencia mide el seguimiento ($M_p,t_s$); el escalón de carga mide el rechazo de perturbación; la inyección de pequeña señal mide la respuesta en frecuencia / impedancia; y el hueco de tensión prueba la supervivencia en falta y el current limiting. Cada uno con su criterio de aceptación numérico.</div></div>

## 1 — Ejemplo cuantitativo: tabla de ensayos con criterio de aceptación
**Contexto:** GFM de 50 kVA, \( V_n=400\,\text{V} \), \( f_{sw}=10\,\text{kHz} \), SCR nominal = 8.

| Ensayo | Especificación | Resultado medido | Veredicto |
|---|---|---|---|
| Escalón de potencia 50→90 % | \( M_p<10\,\%;\; t_s<100\,\text{ms} \) | \( M_p=7\,\%;\; t_s=68\,\text{ms} \) | \( \checkmark \) |
| Escalón de carga (microgrid isla) | Caída de tensión \( <5\,\% \) durante \( <80\,\text{ms} \) | Caída 3.8 %, recuperación 72 ms | \( \checkmark \) |
| Inyección de impedancia (10–500 Hz) | Error modelo/medición \( <5\,\% \) | Error medio 0.21 % | \( \checkmark \) |
| Hueco de tensión al 30 % (100 ms) | Corriente pico \( <1.5\,\text{p.u.} \) | Pico 1.12 p.u. | \( \checkmark \) |
| Barrido SCR 1–12 | SCR crítico \( <1.5 \) (inestable en red fuerte confirmado) | SCR crítico 3.35 | \( \checkmark \) |

**Clave:** cada fila de la tabla liga directamente un requisito del grid code o del diseño a un número medible. Sin ese criterio previo, el ensayo solo produce una curva sin conclusión.

## Cuándo y por qué se usa
En la fase de validación, en cada nivel de fidelidad. Cada ensayo debe tener un **criterio de
aceptación** derivado de las [[especificaciones-control]].

## Procedimiento (genérico)
1. Por cada especificación, elige el ensayo que la mide.
2. Define el criterio de aceptación numérico (p.ej. \( M_p<10\% \), pico de falta < 1.5 pu).
3. Ejecuta el ensayo en el nivel de fidelidad correspondiente.
4. Registra resultado vs criterio; documenta. Si falla, vuelve a diseño.

## Ejemplo de código
```python
# escalon de potencia + falta (simulacion temporal del modelo no lineal)
pset = lambda t: 5e3 if t < 0.2 else 9e3            # escalon de referencia
efunc = lambda t: (0.3*V0,0) if 0.3<=t<0.42 else (V0,0)  # hueco de tension (falta)
```

## Parámetros y valores típicos
Escalón 50→90% de potencia, hueco al 30% durante ~100 ms, inyección de pequeña señal (amplitud
pequeña), barrido de SCR.

## Errores comunes
- Ensayos sin criterio de aceptación previo → "parece que va bien" subjetivo.
- Probar inyección de impedancia con amplitud que activa saturación (deja de ser pequeña señal).

## Uso en proyectos
- **01 (GFM)**: escalón de potencia (droop vs VSM), falta con current limiting (4.76→1.51 pu),
  inyección de impedancia (error 0.21%).
- **02 (GFL)**: barrido de SCR y de ancho de banda de la PLL.

## Conceptos relacionados
- [[niveles-validacion]] · [[validacion-cruzada]] · [[medicion-impedancia-inyeccion]] · [[current-limiting]]

## Referencias
- Teodorescu et al., *Grid Converters for PV and Wind Power Systems*, 2011.

## 3 — Prueba de escalón: lazo de corriente y de tensión

La prueba de escalón es la más básica y la más informativa: aplica un cambio escalón en la referencia (o en la perturbación) y mide la respuesta temporal.

**Lazo de corriente:** escalón de referencia \( i_d^* \) de 0 a 1 p.u. (o del 50% al 90% para evitar saturación). Se miden:
- Tiempo de subida \( t_r \): de 10% a 90% del valor final.
- Sobreimpulso \( M_p = (i_{max} - i_{ss})/i_{ss} \times 100\,\% \).
- Tiempo de establecimiento \( t_s \): tiempo para que el error caiga por debajo de ±2%.
- Error en régimen \( e_{ss} \): debe ser cero si hay integrador en el lazo.

**Criterio de aceptación típico para lazo de corriente** (GFL 100 kW):
- \( t_r < 1\,\text{ms} \) (para \( f_c = 500\,\text{Hz} \), \( \omega_n \approx 3000\,\text{rad/s} \))
- \( M_p < 10\,\% \) (\( \zeta > 0.59 \))
- \( e_{ss} = 0 \) (acción integral \( \checkmark \))

**Lazo de tensión** (microgrid isla o GFM): escalón de carga del 50% al 100% de la potencia nominal. Se mide la caída de tensión transitoria y el tiempo de recuperación. Criterio: caída < 5%, recuperación < 100 ms.

$$ \boxed{M_p = \frac{y_{max} - y_{ss}}{y_{ss}} \times 100\,\%;\quad t_s: |e(t)| < 0.02\,y_{ss}\;\forall t > t_s} $$

## 4 — Prueba de perturbación de red: LVRT, salto de frecuencia y arranque

Las pruebas de perturbación de red verifican la supervivencia del convertidor ante condiciones de red anormales definidas en los grid codes (IEC 61727, IEEE 1547-2018, RD 661/2007):

**LVRT (Low Voltage Ride Through):** hueco de tensión de red al 0–80% de \( V_n \) durante 100–600 ms. El convertidor debe:
1. Permanecer conectado (no disparar la protección de subtensión).
2. Limitar la corriente pico a < 1.5 p.u. (current limiting activo).
3. Inyectar corriente reactiva proporcional a la profundidad del hueco: \( \Delta i_q = k \cdot \Delta V/V_n \) con \( k \geq 2 \).
4. Recuperar la inyección de potencia activa en < 200 ms tras la recuperación de la tensión.

**Salto de frecuencia (frequency step):** cambio de ±2 Hz en 200 ms. El PLL (GFL) o la inercia virtual (GFM) deben seguir la frecuencia sin perder sincronismo. Criterio: error de frecuencia en régimen < 0.1 Hz.

**Arranque / rampa de potencia:** subida de \( P^* \) de 0 a \( P_{nom} \) en 1 s. Verifica que el current limiting no se activa innecesariamente y que la tensión de bus DC no supera el límite.

**Criterio de aceptación:** todos los parámetros del grid code superados sin disparo de protecciones, con registros completos de \( v_{abc}, i_{abc}, P, Q, f \).

## 5 — Prueba de armónicos: FFT e THD

La prueba de armónicos verifica el cumplimiento de los límites de calidad de potencia (IEEE 519-2022, IEC 61000):

**Procedimiento:**
1. Registrar la corriente de red \( i_{PCC}(t) \) a la frecuencia de muestreo \( f_s \geq 20\,\text{kHz} \) durante al menos 10 ciclos de red (200 ms a 50 Hz) para asegurar resolución suficiente (\( \Delta f = 1/T = 5\,\text{Hz} \)).
2. Aplicar ventana de Hann (o muestreo coherente) para evitar fuga espectral.
3. Calcular el espectro de amplitudes \( I_h \) para \( h = 1, 3, 5, \ldots, 50 \).
4. Calcular THD_I y comparar con el límite (5% para \( I_{sc}/I_L < 20 \)).
5. Verificar además cada armónico individual: \( I_5 < 4\,\% \), \( I_7 < 4\,\% \), etc.

**Efecto del control activo:** un controlador resonante o repetitivo aplicado reduce los armónicos de baja frecuencia (5°, 7°, 11°, 13°) pero el filtro LCL es el responsable de la atenuación de los armónicos de conmutación. Ambos mecanismos deben cumplir simultáneamente.

$$ \text{THD}_I = \frac{\sqrt{\sum_{h=2}^{50} I_h^2}}{I_1} \times 100\,\% < 5\,\% \quad (\text{IEEE 519, } I_{sc}/I_L < 20) $$

## 6 — Documentación: informe de pruebas

Cada prueba de validación debe generar un informe con estructura fija que ligue el resultado medido al criterio de aceptación:

**Estructura del informe de prueba:**
1. **Identificación:** nombre del equipo, fecha, nivel de fidelidad (SiL/HiL/prototipo), versión del firmware.
2. **Condición de prueba:** potencia, tensión, SCR de red, temperatura.
3. **Procedimiento:** descripción del estímulo (forma de onda, amplitud, duración).
4. **Resultado medido:** valores numéricos de \( M_p \), \( t_s \), THD, PM, etc.
5. **Comparativa spec vs medida:** tabla con criterio de aceptación, resultado y veredicto (PASS/FAIL).
6. **Capturas:** oscilogramas o curvas de simulación con escala temporal y unidades.
7. **Análisis de discrepancias:** si hay FAIL, descripción del problema y acción correctiva.

**Hoja de pruebas (test sheet):** documento de una página que resume todos los ensayos de una sesión de validación con sus veredictos. Permite rastrear qué versión del diseño aprobó qué pruebas y cuándo.

<div class="cfig"><img src="../figuras/pruebas-validacion-analisis.png" alt="escalón de corriente, LVRT, THD y timeline del plan de pruebas"><div class="cap">Cuatro pruebas clave de validación: (1) escalón de corriente con Ms y ts marcados, (2) LVRT con hueco al 30% y recuperación en 100 ms, (3) espectro FFT de la corriente con límites IEEE 519, (4) timeline del plan de pruebas desde SiL hasta campo con criterios de salida de cada nivel.</div></div>

## 7 — Automatizacion de pruebas en Python

Las pruebas de validacion se pueden automatizar completamente en Python, generando resultados reproducibles y comparables entre versiones del diseno:

```python
import numpy as np
from scipy.integrate import solve_ivp
from scipy import signal

def prueba_escalon_corriente(rhs, x0, params, t_end=0.005, i_ref=1.0):
    """
    Ejecuta la prueba de escalon del lazo de corriente y verifica specs.
    Retorna dict con Mp, ts, ess y veredicto PASS/FAIL.
    """
    t_eval = np.linspace(0, t_end, 2000)
    sol = solve_ivp(rhs, (0, t_end), x0, args=(params, i_ref),
                    method='LSODA', t_eval=t_eval, rtol=1e-7)

    # extraer corriente id (primer estado del lazo de corriente)
    id_t = sol.y[0]
    t = sol.t

    # calcular metricas
    ss_val = id_t[-1]  # valor de regimen permanente
    Mp_pct = (id_t.max() - ss_val) / ss_val * 100
    ess = abs(ss_val - i_ref) / i_ref * 100

    # ts: ultimo instante donde |id - ss| > 2%
    within_band = np.abs(id_t - ss_val) / ss_val < 0.02
    ts_idx = np.where(~within_band)[0]
    ts_s = t[ts_idx[-1]] if len(ts_idx) > 0 else 0

    resultado = {
        'Mp_pct': Mp_pct, 'ts_ms': ts_s * 1000, 'ess_pct': ess,
        'pass_Mp': Mp_pct < 10,
        'pass_ts': ts_s < 2e-3,
        'pass_ess': ess < 0.1,
    }
    resultado['pass_all'] = all([resultado['pass_Mp'], resultado['pass_ts'],
                                   resultado['pass_ess']])
    return resultado


def prueba_thd(i_pcc, fs, N_cycles=10, f1=50):
    """
    Calcula THD de la corriente en PCC con ventana de N ciclos (IEC 61000-4-7).
    """
    N = int(N_cycles * fs / f1)  # muestras en N ciclos
    if len(i_pcc) < N:
        raise ValueError(f"Senyal demasiado corta: {len(i_pcc)} < {N}")
    # usar los ultimos N muestras (regimen permanente)
    x = i_pcc[-N:]
    # muestreo coherente: sin ventana
    X = np.fft.rfft(x)
    f_bins = np.fft.rfftfreq(N, 1/fs)
    # amplitudes corregidas
    amps = 2 * np.abs(X) / N
    # fundamental: bin mas cercano a f1
    idx_f1 = np.argmin(np.abs(f_bins - f1))
    I1 = amps[idx_f1]
    # armonicos 2 a 50
    Ih_sq = 0
    for h in range(2, 51):
        fh = h * f1
        idx_h = np.argmin(np.abs(f_bins - fh))
        Ih_sq += amps[idx_h]**2
    THD_pct = np.sqrt(Ih_sq) / I1 * 100
    return {'THD_pct': THD_pct, 'I1': I1, 'pass': THD_pct < 5.0}


# Ejemplo de uso en suite de pruebas automatizada
if __name__ == "__main__":
    # ... definir rhs, x0, params, i_pcc_data ...
    # r1 = prueba_escalon_corriente(rhs, x0, params)
    # r2 = prueba_thd(i_pcc_data, fs=10000)
    # print(f"Escalon: {'PASS' if r1['pass_all'] else 'FAIL'} | "
    #       f"Mp={r1['Mp_pct']:.1f}%, ts={r1['ts_ms']:.1f}ms")
    # print(f"THD: {'PASS' if r2['pass'] else 'FAIL'} | THD={r2['THD_pct']:.2f}%")
    pass
```

## 8 — Pruebas de robustez parametrica

Las pruebas de robustez parametrica verifican que el diseno cumple las especificaciones en todo el rango de operacion, no solo en el punto nominal:

**Prueba de barrido de SCR:** variar el SCR de la red desde el maximo (SCR = 20, red fuerte) hasta el minimo operativo (SCR = 1.5 para GFM, SCR = 3 para GFL) y verificar que:
1. El sistema permanece estable (autovalores con parte real negativa).
2. El margen de fase del lazo de corriente sigue siendo > 45°.
3. El THD en el PCC sigue siendo < 5% (la impedancia de red amplifica los armonicos de corriente en red debil).

**Prueba de barrido de potencia:** variar la potencia de 10% a 110% de la nominal. Los cambios de potencia afectan el punto de operacion y por tanto el modelo linealizado. La prueba verifica que el controlador disenado para el punto nominal sigue siendo estable y con buenas prestaciones en todo el rango.

**Prueba de temperatura:** la resistencia del devanado del inductor \( L_1 \) varia con la temperatura: +0.4%/°C para cobre. A 100°C de elevacion de temperatura: \( R_1 \) aumenta un 40%. Esto modifica el punto de operacion (mas perdidas) y la planta del lazo de corriente. Verificar que la sintonizacion sigue siendo valida.

| Prueba de robustez | Rango | Criterio | Metodo |
|---|---|---|---|
| Barrido SCR | 1.5–20 | PM > 45°, estable | Autovalores del modelo lineal |
| Barrido potencia | 10–110% | Mp < 10%, ts < 2ms | Simulacion no lineal |
| Variacion L ±30% | -30%..+30% | PM > 45° | Monte Carlo N=1000 |
| Variacion temperatura | 25–125°C | Estable, THD < 5% | Barrido 1D parametrico |

## 9 — Gestion del plan de pruebas

El plan de pruebas es un documento vivo que evoluciona durante el proyecto. La estructura recomendada incluye:

1. **Version del firmware/modelo:** cada suite de pruebas debe estar ligada a una version especifica del codigo de control (hash de git o numero de version). Esto permite repetir exactamente las pruebas de validacion si surge una duda retrospectiva.

2. **Condiciones de referencia:** temperatura, tension de bus DC, frecuencia de red, SCR de la red — todos los parametros que afectan al resultado deben estar especificados y registrados.

3. **Trazabilidad de requisitos:** cada prueba debe estar ligada al requisito del grid code o del cliente que verifica. Un requisito sin prueba asociada es un requisito no verificado.

4. **Criterio de salida del nivel:** una suite de pruebas no esta completa hasta que todos los casos pasan con sus criterios de aceptacion. Si hay un caso que falla pero se decide aceptarlo (con una exencion documentada), la exencion debe incluir el riesgo tecnico y el plan de mitigacion.
