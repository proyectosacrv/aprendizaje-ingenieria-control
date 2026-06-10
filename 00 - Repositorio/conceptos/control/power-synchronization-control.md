---
titulo: Power Synchronization Control (PSC)
slug: power-synchronization-control
categoria: control
tipo: tecnica
nivel: avanzado
proyectos: []
objetivos: [sincronizar un convertidor a la red por potencia activa, sin PLL]
tags: [psc, sincronizacion, grid-forming, sin-pll, hvdc, red-debil, avanzado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-09
relacionados: [grid-forming-vs-following, vsm-inercia, droop-control, interaccion-pll-red-debil, ecuacion-oscilacion]
referencias:
  - "Zhang et al., Power Synchronization Control of Grid-Connected VSC, IEEE TPWRS 2010"
  - "Harnefors et al., Synchronization Stability of Grid-Connected VSCs, IEEE TPEL 2017"
---

## Definición
Estrategia grid-forming en la que el ángulo de salida del convertidor se genera **integrando el
error de potencia activa** —en vez de usar una PLL que mide la fase de la red— de forma análoga a
la sincronización electromagnética de un generador síncrono.

## Fundamento teórico
La idea central es que la **potencia activa** fluye entre dos fuentes de tensión según su diferencia
de ángulo \( \delta \). Usando esa relación como lazo de control:
$$ \dot\delta = K_{psc}(P^*-P) \implies \delta = \int K_{psc}(P^*-P)\,dt $$
con \( K_{psc} \) ganancia de sincronización. Esto produce la misma dinámica que la
[[ecuacion-oscilacion|swing equation]] sin inercia explícita: en régimen permanente \( P=P^* \) y
el ángulo \( \delta \) queda fijo. La acción integral acumula el ángulo relativo correcto.

Comparando con [[vsm-inercia|VSM]] y [[droop-control|droop P-f]]:

| Aspecto | Droop \(\omega-P\) | VSM | PSC |
|---|---|---|---|
| Variable de lazo | frecuencia | frecuencia (virtual) | ángulo |
| PLL | necesaria | puede evitarse | no, intrínseca |
| Inercia | no | sí (emulada) | no (puede añadirse) |
| Análisis | Bode de lazo P | modelo SS mecánico | sistema de 1er orden en \(\delta\) |

La **estabilidad** de PSC se analiza linearizando la potencia \( P=\frac{EV_g}{X}\sin\delta \) en
el punto de operación: la ganancia del lazo de sincronización es \( K_{psc}\cdot K_s \) (par
sincronizante \( K_s=EV_g\cos\delta_0/X \)). Un polo dominante en
\( s=-K_{psc}K_s \) → la sincronización es de **primer orden** (sin oscilación) mientras no haya
retardos importantes. La **limitación de corriente** se implementa reduciendo \( E \) (tensión
virtual) o cambiando la referencia de \( Q \); esto cambia dinámicamente la reactancia efectiva y
puede inestabilizar en red muy débil si no se coordina.

En red débil (bajo [[red-thevenin-scr|SCR]]), la PLL de un GFL desestabiliza
([[interaccion-pll-red-debil]]), mientras PSC opera estable porque no depende de medir la fase de
la red; fue propuesto originalmente para **HVDC** en red débil.

## Cuándo y por qué se usa
Convertidores HVDC, almacenamiento y renovables en redes muy débiles (SCR < 1.5) donde la PLL
falla. Alternativa más simple que el VSM (sin ecuación de oscilación explícita) cuando no se
necesita emular inercia.

## Procedimiento de diseño (genérico)
1. Determina el punto de operación \( \delta_0 \) y calcula \( K_s=EV_g\cos\delta_0/X_{total} \).
2. Elige \( K_{psc} \) para el tiempo de respuesta de sincronización deseado; verifica que el polo
   \( -K_{psc}K_s \) sea suficientemente negativo.
3. Añade amortiguamiento si hay oscilación (derivada de potencia, similar a \( D\dot\delta \)).
4. Diseña el lazo de tensión/reactiva independiente (controla \( |E| \)).
5. Implementa limitación de corriente coordinada con la magnitud \( E \) y verifica estabilidad en
   todo el rango de SCR.

## Ejemplo de código
```python
def psc_angle(P_ref, P_meas, delta, K_psc, dt):
    delta += K_psc * (P_ref - P_meas) * dt   # integra el error de potencia
    return delta                              # angulo de referencia del convertidor
```

## Parámetros y valores típicos
\( K_{psc} \approx 1\text{–}10 \) rad/s/MW (p.u.). \( \delta_0 < 30\text{–}45° \) para operar lejos
del límite. Tiempo de sincronización: decenas de ms–s.

## Errores comunes
- Operar con \( \delta_0 \) cercano a 90° (margen de par sincronizante mínimo, pérdida de
  sincronismo ante perturbación).
- Acoplar la limitación de corriente sin analizar su efecto sobre \( K_s \) (puede hacer el lazo
  inestable).
- Confundir con droop: el droop varía la frecuencia; el PSC integra directamente el ángulo.

## Conceptos relacionados
- [[grid-forming-vs-following]] · [[vsm-inercia]] · [[droop-control]] · [[interaccion-pll-red-debil]] · [[ecuacion-oscilacion]]

## Referencias
- Zhang et al., *Power Synchronization Control of Grid-Connected VSC*, IEEE TPWRS 2010.
- Harnefors et al., *Synchronization Stability of Grid-Connected VSCs*, IEEE TPEL 2017.
