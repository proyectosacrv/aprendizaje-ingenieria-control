---
titulo: Control jerárquico de microrredes (primario/secundario/terciario)
slug: control-jerarquico-microrred
categoria: metodologia
tipo: metodo
nivel: avanzado
proyectos: []
objetivos: [organizar el control de una microrred en capas por escala de tiempo y objetivo]
tags: [microrred, jerarquico, primario, secundario, terciario, droop, restauracion, avanzado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-09
relacionados: [droop-control, droop-dc, microrred-hibrida-ac-dc, servicios-red-soporte, vsm-inercia]
referencias:
  - "Guerrero et al., Hierarchical Control of Droop-Controlled AC and DC Microgrids, IEEE TIE 2011"
  - "Olivares et al., Trends in Microgrid Control, IEEE TSG 2014"
---

## Definición
Arquitectura de control en **tres niveles** —primario, secundario y terciario— separados por escala
de tiempo y objetivo, que coordina las fuentes de una microrred desde la dinámica rápida del
convertidor hasta la gestión económica y el intercambio con la red.

## Fundamento teórico
- **Primario (ms–s):** local, sin comunicaciones. Lazos de tensión/corriente del convertidor y
  **droop** para reparto de potencia entre unidades en paralelo (ver [[droop-control]],
  [[droop-dc]]):
  $$ \omega=\omega^*-m\,P,\qquad V=V^*-n\,Q\quad(\text{AC});\qquad V_{dc}=V_{dc}^*-R_d\,I\ (\text{DC}) $$
  Da estabilidad y reparto proporcional, pero deja **desviación** en \( \omega/V \).
- **Secundario (s–min):** **restaura** la desviación que deja el droop, devolviendo \( \omega \) y
  \( V \) a su valor nominal y corrigiendo el reparto; puede ser centralizado o **distribuido**
  (consenso). Aporta el término de corrección \( \delta\omega,\delta V \) que se suma a la referencia
  del primario.
- **Terciario (min–h):** **optimiza** el flujo de potencia: despacho económico, intercambio con la
  red principal, gestión de almacenamiento (EMS). Fija las referencias de P/Q de cada unidad.

Principio de **separación temporal**: cada nivel es ~5–10× más lento que el inferior para no
interactuar. Modos de operación: **conectado a red** (terciario manda P/Q) e **isla** (primario +
secundario mantienen la red).

<div class="cfig"><img src="figuras/control-jerarquico-microrred-capas.png" alt="tres capas del control jerarquico de microrred por escala de tiempo"><div class="cap">El control se organiza en tres capas separadas por escala de tiempo: el primario (ms–s, local, droop) da estabilidad y reparto pero deja desviación; el secundario (s–min) la restaura devolviendo ω/V a su nominal; el terciario (min–h) optimiza el despacho. Cada capa es ~5–10× más lenta que la inferior para no interactuar.</div></div>

## Cuándo y por qué se usa
En microrredes (incluida la híbrida AC/DC del data center): coordina varias fuentes/convertidores,
garantiza reparto de carga, calidad de tensión/frecuencia y operación económica, con transición
suave isla↔red. Traduce los [[servicios-red-soporte|servicios de red]] a una estructura operable.

## Procedimiento de diseño (genérico)
1. Diseña el **primario** (lazos internos + droop) para estabilidad y reparto.
2. Añade el **secundario** (PI/consenso) con banda ~1/10 del primario para restaurar \( \omega/V \).
3. Define el **terciario** (optimización/EMS) y las referencias que envía.
4. Especifica comunicaciones y tolerancia a su fallo (distribuido > centralizado en robustez).
5. Verifica transiciones isla↔red y estabilidad de la interacción entre niveles.

## Ejemplo de código
```python
def primary(w_ref, V_ref, P, Q, m, n, dW=0.0, dV=0.0):
    w = w_ref - m*P + dW                 # droop + correccion secundaria (dW, dV)
    V = V_ref - n*Q + dV
    return w, V
# secundario: dW += k_s*(w_nom - w_med)*dt   (restauracion)
```

## Parámetros y valores típicos
Primario ms–s; secundario segundos; terciario minutos. Droop \( m,n \) para 1–5 % de desviación a
plena carga. Bandas separadas factor 5–10 entre niveles.

## Errores comunes
- Bandas de niveles solapadas → interacción y oscilación entre primario y secundario.
- Secundario centralizado sin plan ante fallo de comunicaciones.
- Reparto deficiente en DC por resistencias de línea desiguales (corregir en secundario).
- Transición isla↔red sin sincronización previa → transitorios bruscos.

## Conceptos relacionados
- [[droop-control]] · [[droop-dc]] · [[microrred-hibrida-ac-dc]] · [[servicios-red-soporte]] · [[vsm-inercia]]

## Referencias
- Guerrero et al., *Hierarchical Control of Droop-Controlled AC and DC Microgrids*, IEEE TIE 2011.
- Olivares et al., *Trends in Microgrid Control*, IEEE TSG 2014.
