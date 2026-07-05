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

## 3 — Nivel primario: control local del inversor

El nivel primario actúa en la escala de milisegundos a segundos y opera **sin comunicación**, basándose únicamente en medidas locales de tensión y corriente.

**Droop de frecuencia:** cada inversor ajusta su frecuencia de salida en función de la potencia activa que inyecta:

$$ f = f_0 - m_p(P - P_0) $$

donde \( m_p \) es la ganancia de caída (pendiente del droop, en Hz/W) y \( P_0 \) es la referencia de potencia activa. Cuando la carga aumenta, la frecuencia baja en todos los inversores de forma proporcional a \( m_p \), lo que distribuye la carga entre ellos de forma automática y proporcional.

**Droop de tensión:** análogamente para la potencia reactiva:

$$ V = V_0 - n_q(Q - Q_0) $$

Con droop simétrico (\( m_p \) iguales en todos los inversores), el reparto de potencia activa es proporcional a la potencia nominal, independientemente de las impedancias de línea.

El lazo interno del inversor tiene dos capas: el **lazo de corriente** (el más rápido, con ancho de banda de 1–5 kHz) que controla la corriente del inductor, y el **lazo de tensión** (más lento, 200–500 Hz) que mantiene la tensión en bornes del filtro. Las referencias del droop se suman como correcciones a la referencia del lazo de tensión.

## 4 — Nivel secundario: restauración

El droop deja una desviación permanente en frecuencia y tensión (el *offset* de la característica estática). El nivel secundario corrige esta desviación devolviendo \( f \) y \( V \) a sus valores nominales, **sin cambiar el reparto de carga**.

El controlador secundario centralizado o distribuido (consenso) calcula la corrección \( \delta f, \delta V \) que se envía a cada inversor:

$$ \delta f = K_{p,s}(f^* - f_{meas}) + K_{i,s}\int (f^* - f_{meas})\,dt $$

El nivel secundario **requiere comunicación** entre los inversores (o hacia un controlador central), aunque puede ser lenta (bus de bajo ancho de banda, típ. 1–10 bits/s suficiente). Esta comunicación es el punto débil de robustez del sistema: su fallo deja al sistema con las desviaciones del primario.

**Tiempo de respuesta:** 1–10 s, mucho más lento que el primario (escala de ms), para no interactuar con la dinámica primaria. La regla de separación de bandas exige un factor ≥ 5–10 entre los anchos de banda de niveles adyacentes.

La frecuencia de referencia es \( f^* = 50\,\text{Hz} \) y la tensión \( V^* = 1\,\text{pu} \). El secundario puede también corregir el reparto de carga si las resistencias de línea son desiguales (especialmente crítico en microrredes DC).

## 5 — Nivel terciario: gestión de energía (EMS)

El nivel terciario opera en la escala de minutos a horas y tiene por objetivo la **optimización económica** del despacho, coordinando las fuentes con la demanda y los mercados de energía.

El problema de **despacho económico** se formula como minimización del coste total de generación sujeto a restricciones:

$$ \min_{P_{gen,i}} \sum_i c_i(P_{gen,i}) \quad \text{s.t.} \quad \sum_i P_{gen,i} = P_{load},\; P_{i,min} \leq P_{gen,i} \leq P_{i,max} $$

donde \( c_i(P) \) es la función de coste del generador \( i \) (coste marginal o función cuadrática). La solución óptima iguala los costes marginales de todos los generadores activos (condición KKT).

**Variables gestionadas:** \( P_{gen,i} \) de cada unidad, \( SOC_{BESS} \) para gestionar la carga y descarga del almacenamiento, y \( P_{import/export} \) el intercambio con la red principal.

**Horizonte de optimización:** 15 min a 24 h en modo *day-ahead* (con predicción solar/eólica) o 5 min en modo *real-time* (reajuste con datos recientes). La comunicación se implementa via SCADA o IEC 61850, con latencias de segundos tolerables a esta escala de tiempo.

## 6 — Coordinación entre niveles y sincronización

La **separación temporal** garantiza que los niveles no interfieran entre sí: primario en ms, secundario en s, terciario en min–h. El factor mínimo entre bandas adyacentes es 5–10 para que cada nivel vea al inferior como ya establecido.

**Conflicto potencial:** el terciario puede ordenar un despacho que el primario no puede seguir (saturación de corriente, límites del bus DC). La resolución es que el **secundario actúa como interfaz**: el terciario envía setpoints de potencia \( P^*, Q^* \) al secundario, que los traduce en correcciones de la referencia del primario respetando los límites dinámicos.

**Microrred islada:** en ausencia de red principal, el nivel secundario es crítico para mantener la estabilidad de frecuencia a largo plazo. Sin él, la frecuencia deriva indefinidamente siguiendo la característica droop. El secundario restaura \( f \) al nominal en cada perturbación de carga.

**Transición isla ↔ red:** al reconectar a la red, la microrred debe sincronizarse en fase, frecuencia y tensión antes de cerrar el interruptor. El nivel secundario gestiona esta sincronización ajustando gradualmente la frecuencia de referencia del primario hasta igualar la de la red, minimizando el transitorio de reconexión.

<div class="cfig"><img src="../figuras/control-jerarquico-microrred-analisis.png" alt="Control jerárquico de microrred: primario droop, restauración secundaria y despacho terciario"><div class="cap">Cuatro paneles: pirámide de control jerárquico con las cuatro capas y sus escalas de tiempo; característica droop P-f del control primario; restauración de frecuencia por el nivel secundario ante una perturbación de carga; perfil de generación solar, demanda y SOC del BESS en un ciclo de 24 horas gestionado por el EMS terciario.</div></div>

## Conceptos relacionados
- [[droop-control]] · [[droop-dc]] · [[microrred-hibrida-ac-dc]] · [[servicios-red-soporte]] · [[vsm-inercia]]

## Referencias
- Guerrero et al., *Hierarchical Control of Droop-Controlled AC and DC Microgrids*, IEEE TIE 2011.
- Olivares et al., *Trends in Microgrid Control*, IEEE TSG 2014.
