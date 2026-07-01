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
fecha_actualizacion: 2026-07-01
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

## 1 — Ejemplo cuantitativo: diseño de las tres capas para una microrred de 200 kVA
**Primario.** Dos convertidores GFM de 100 kVA cada uno en paralelo. Para que a plena carga la desviación de frecuencia sea \( \le1\,\% \) (\( \le0.5\,\text{Hz} \)) con el estatismo \( m \):

$$ \Delta\omega = m\,P_{\max}\;\Rightarrow\; m=\frac{2\pi\times0.5}{100\times10^3}=3.14\times10^{-5}\,\text{rad/s/W} $$

Cada unidad tendrá \( m_1=m_2=3.14\times10^{-5} \) → potencias iguales a plena carga (reparto proporcional). Si los droop son iguales, la carga se reparte 50/50 independientemente de las impedancias de línea (en la banda donde el droop domina).

**Secundario.** Para restaurar \( \omega \) con un PI de restauración: constante de tiempo del secundario \( \tau_s=5\,\text{s} \) (factor 5 más lento que el primario, cuya dinámica dominante es \( \tau_1\approx 1/m/P_n\cdot 2H\approx 1\,\text{s} \)). Ganancia del PI secundario: \( K_s=2\pi\times(1/\tau_s)=1.26 \) rad/s/Hz.

**Terciario.** Despacho económico cada 5 min. Con dos fuentes de coste marginal \( c_1<c_2 \), la unidad 1 produce a \( P_1^*=P_{carga}-P_2^{min} \) hasta su límite; el terciario envía estas referencias al secundario como desplazamientos del punto de operación \( \delta\omega^* \).

**Verificación de separación de escalas:** primario ms–s, secundario s–10 s, terciario minutos: factor \( \ge5 \) entre cada nivel \( \checkmark \).

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
