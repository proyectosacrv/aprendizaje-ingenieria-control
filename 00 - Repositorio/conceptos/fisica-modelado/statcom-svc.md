---
titulo: STATCOM y SVC (compensación de reactiva)
slug: statcom-svc
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: []
objetivos: [soportar tensión de red inyectando/absorbiendo reactiva, comparar fuente de corriente vs susceptancia]
tags: [statcom, svc, facts, reactiva, soporte-tension, tcr, tsc, vsc, modelado]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-06-10
relacionados: [convertidor-vsc, servicios-red-soporte, transferencia-potencia-linea, potencia-instantanea-dq, fault-ride-through, droop-control]
referencias:
  - "Hingorani, Gyugyi, Understanding FACTS, IEEE Press 2000"
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
---

## Definición
Dispositivos **FACTS** en derivación (shunt) que inyectan o absorben **potencia reactiva** para sostener
la tensión de un nudo. El **SVC** lo hace variando una **susceptancia** (tiristores: TCR + TSC); el
**STATCOM** es un [[convertidor-vsc|VSC]] que actúa como **fuente de corriente reactiva** controlada.

## Fundamento teórico
La tensión de un nudo depende de la reactiva inyectada \( \Delta V\approx X_{th}\,\Delta Q/V \): inyectar
\( Q>0 \) **sube** la tensión, absorber \( Q<0 \) la baja. La diferencia clave entre ambos está en cómo
escala su capacidad con la tensión:

- **SVC** = susceptancia controlable \( B \). La reactiva es \( Q=B\,V^2 \): cuando más la necesitas
  (hueco de tensión) **menos das**, porque \( Q\propto V^2 \). Genera armónicos (TCR) → necesita filtros.
- **STATCOM** = fuente de corriente. \( Q=V\,I_q \) con \( I_q \) acotada por el convertidor: mantiene
  **corriente nominal aun con \( V \) baja**, así que su soporte cae solo \( \propto V \) (mucho mejor en
  defecto). Respuesta en ms y huella menor.

| | SVC | STATCOM |
|---|---|---|
| Elemento | susceptancia (TCR/TSC) | VSC (fuente de corriente) |
| \( Q \) a tensión baja | \( \propto V^2 \) (se hunde) | \( \propto V \) (se mantiene) |
| Velocidad | ~1–2 ciclos | sub-ciclo |
| Armónicos | sí (filtros) | bajos (PWM + LCL) |

El control del STATCOM es un lazo de corriente en [[potencia-instantanea-dq|dq]] con \( i_d^\*\approx0 \)
(solo lo justo para pérdidas y bus DC) e \( i_q^\* \) saliendo de un lazo de tensión AC, a menudo con
**[[droop-control|droop]] Q-V** para repartir entre varios equipos.

<div class="cfig"><img src="figuras/statcom-svc-qv.png" alt="reactiva disponible frente a tension para SVC y STATCOM"><div class="cap">Reactiva disponible frente a la tensión: el SVC es una susceptancia, así que su $Q\propto V^2$ se hunde justo cuando más falta (en el hueco); el STATCOM es una fuente de corriente, mantiene $I_q$ y su soporte cae solo $\propto V$. Por eso el STATCOM es muy superior para sostener tensión durante un defecto.</div></div>

## Cuándo y por qué se usa
Soporte de tensión en puntos débiles, cumplimiento de **[[fault-ride-through|FRT]]** (inyección de reactiva
durante huecos exigida por código), reducción de flícker, y compensación dinámica en parques renovables.
El STATCOM se prefiere cuando se necesita soporte **durante** el defecto (tensión baja) o respuesta muy rápida.

## Procedimiento de diseño (genérico)
1. Calcula la reactiva necesaria por el \( \Delta V \) objetivo y la \( X_{th} \) del nudo ([[transferencia-potencia-linea]]).
2. Elige tecnología: STATCOM si hace falta soporte a tensión baja / respuesta rápida; SVC si prima coste/MVAr.
3. Dimensiona corriente (STATCOM) o rango de \( B \) (SVC) con margen para el peor hueco.
4. Diseña el lazo: corriente dq interno + tensión AC externo, con droop Q-V y límites de corriente.
5. Verifica comportamiento en FRT (prioridad de \( i_q \) sobre \( i_d \)) y estabilidad con la red.

## Ejemplo de aplicación real
**Problema:** nudo de 33 kV con \( X_{th}=3\,\Omega \) cae a 0.85 pu en un hueco. Comparar un SVC y un
STATCOM de **20 MVAr nominales** soportando la tensión.

A tensión nominal ambos dan 20 MVAr. Durante el hueco (\( V=0.85 \) pu):
- **SVC:** \( Q=Q_{nom}(V/V_{nom})^2=20\times0.85^2\approx14.5\,\text{MVAr} \) → pierde 27 % justo cuando
  más falta.
- **STATCOM:** mantiene \( I_q \) nominal → \( Q=Q_{nom}(V/V_{nom})=20\times0.85\approx17\,\text{MVAr} \).
El STATCOM aporta \( \sim\!2.5\,\text{MVAr} \) más en el defecto. Subida de tensión aportada por el STATCOM:
\( \Delta V\approx X_{th}Q/V \) en pu base 33 kV → con 17 MVAr,
\( \Delta V\approx (3\times17\times10^6/(0.85\times33\text{k})^2)\approx0.065\,\text{pu} \): recupera de 0.85 a ~0.92 pu.

## Ejemplo de código
```python
def statcom_iq_ref(v_meas, v_ref, droop, iq_max):
    # lazo Q-V con droop; satura a corriente reactiva maxima del VSC
    iq = (v_ref - v_meas) / droop          # +iq inyecta reactiva (sube V)
    return max(-iq_max, min(iq, iq_max))
```

## Parámetros y valores típicos
Rango: ±10 a ±300 MVAr. Droop Q-V: 1–5 %. Tiempo de respuesta STATCOM: < 5 ms; SVC: 20–40 ms.
\( V_{dc} \) STATCOM y filtro como cualquier VSC de red.

## Errores comunes
- Dimensionar el STATCOM por MVAr a tensión nominal y olvidar que en FRT lo que limita es la **corriente**.
- Usar SVC donde se exige soporte a tensión muy baja (su Q se hunde con \( V^2 \)).
- Olvidar la prioridad \( i_q>i_d \) durante el hueco → no cumple el código FRT.
- Droop Q-V demasiado pequeño entre varios equipos → reparto inestable / hunting.

## Conceptos relacionados
- [[convertidor-vsc]] · [[servicios-red-soporte]] · [[fault-ride-through]] · [[transferencia-potencia-linea]] · [[droop-control]]

## Referencias
- Hingorani, Gyugyi, *Understanding FACTS*, 2000.
- Yazdani, Iravani, 2010.
