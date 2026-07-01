---
titulo: Impedancia virtual
slug: impedancia-virtual
categoria: control
tipo: tecnica
nivel: avanzado
proyectos: [01-GFM-Impedance]
objetivos: [estabilizar el lazo de potencia, amortiguar oscilaciones, desacoplar P-Q]
tags: [grid-forming, droop, reactancia, dq, amortiguamiento]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-30
relacionados: [droop-control, control-cascada, grid-forming-vs-following]
referencias:
  - "Rocabert et al., Control of Power Converters in AC Microgrids, IEEE Trans. Power Electron., 2012"
  - "Wang, Blaabjerg, Harmonic Stability in Power-Electronic-Based Power Systems, IEEE TPEL 2019"
---

## Definición
La **impedancia virtual** es una impedancia emulada por software que el inversor añade a su
salida **restándola de la referencia de tensión**, sin componentes físicos. Sirve para dar
forma a la impedancia de salida del convertidor: amortiguar, desacoplar P–Q y limitar
corriente.

## Fundamento teórico
La referencia de tensión del lazo se corrige con la caída sobre una impedancia
\( Z_v = R_v + jX_v \) recorrida por la corriente de salida \( \mathbf{i} \):

$$ \mathbf{v}_{C}^{*} = \mathbf{v}_{ref} - Z_v\,\mathbf{i} $$

En el marco dq (síncrono a \( \omega \)) la caída se expresa con el acoplamiento cruzado:

$$ v^{*}_{Cd} = v_{ref,d} - R_v i_d + \omega L_v i_q, \qquad
   v^{*}_{Cq} = v_{ref,q} - R_v i_q - \omega L_v i_d $$

El efecto clave: la ganancia del lazo de potencia de un grid-forming es
\( \partial P/\partial\delta \approx 1.5\,V^2/X \). Aumentar la reactancia efectiva con
\( X_v \) **reduce esa ganancia** y, por tanto, el riesgo de inestabilidad del lazo de
potencia, sin añadir un polo de planta lento (es algebraica sobre la referencia).

<div class="cfig"><img src="figuras/impedancia-virtual-pd.png" alt="curva P-delta con y sin impedancia virtual"><div class="cap">Curva $P(\delta)=1.5\,V^2/X\,\sin\delta$. Sumar reactancia virtual $X_v$ (azul) aplana la curva: la pendiente en el punto de operación $\partial P/\partial\delta$ —la ganancia del lazo de potencia— se reduce, amortiguando el lazo sin introducir un polo lento de planta.</div></div>

## 1 — Por qué restar \( Z_v\,\mathbf{i} \) de la referencia emula una impedancia
**Paso 1 — el lazo de tensión sigue su referencia.** El lazo interno de tensión es rápido y de alta ganancia, así que en su banda hace \( \mathbf{v}_C\approx\mathbf{v}_C^* \): la tensión del condensador sigue a la referencia que le damos. Esa es la palanca: lo que escribamos en \( \mathbf{v}_C^* \) aparece en bornes.

**Paso 2 — inyectar la caída de una impedancia ficticia.** Definimos la referencia como la consigna deseada menos la caída de una impedancia \( Z_v \) recorrida por la corriente de salida medida \( \mathbf{i} \):
$$ \mathbf{v}_C^*=\mathbf{v}_{ref}-Z_v\,\mathbf{i} $$
Combinando con \( \mathbf{v}_C\approx\mathbf{v}_C^* \):
$$ \mathbf{v}_C\approx\mathbf{v}_{ref}-Z_v\,\mathbf{i} $$

**Paso 3 — leerlo como Thévenin.** Esta ecuación es exactamente la de una fuente ideal \( \mathbf{v}_{ref} \) detrás de una impedancia serie \( Z_v \): la tensión en bornes cae \( Z_v\,\mathbf{i} \) conforme sube la corriente, igual que si hubiera un \( R_v+jX_v \) **físico** en serie. La impedancia de salida de pequeña señal que el equipo presenta hacia la red gana ese término:
$$ Z_o^{eff}(s)=Z_{o,fis}(s)+Z_v(s) $$
pero sin disipar potencia ni añadir hardware: es una caída calculada y reescrita en la referencia. Por eso tampoco mete un polo de planta lento — la operación es **algebraica** sobre \( \mathbf{v}_C^* \), instantánea dentro de la banda del lazo de tensión.

**Paso 4 — en dq el término reactivo se cruza.** Una reactancia es \( Z_v=R_v+j\omega L_v \); en el marco dq el producto \( j\omega L_v\cdot\mathbf{i} \) rota \( 90° \) los ejes, dando los términos cruzados de la ficha:
$$ v_{Cd}^*=v_{ref,d}-R_v i_d+\omega L_v i_q,\qquad v_{Cq}^*=v_{ref,q}-R_v i_q-\omega L_v i_d $$
(el \( +\omega L_v i_q \) en d y el \( -\omega L_v i_d \) en q son el "\( j \)" de la reactancia visto en componentes).

## 2 — Cómo \( X_v \) reduce la ganancia del lazo de potencia
**Paso 1 — la ganancia depende de \( 1/X \).** La pendiente del flujo de carga en el punto de operación es \( \partial P/\partial\delta\approx 1.5\,V^2\cos\delta_0/X \) (factor \( 1.5 \) por la potencia trifásica en valores de pico dq). Esta pendiente es la ganancia del lazo de potencia del grid-forming: cuanto mayor, menos margen de fase (ver [[droop-control]] apartado 2).

**Paso 2 — la virtual entra en serie.** La impedancia virtual suma su reactancia a la de acoplamiento real, \( X_{tot}=X_{fis}+X_v \), porque aparece en serie con la fuente de tensión (apartado anterior). Sustituyendo:
$$ \frac{\partial P}{\partial\delta}\approx\frac{1.5\,V^2\cos\delta_0}{X_{fis}+X_v} $$

**Paso 3 — el efecto.** Subir \( X_v \) **baja** \( \partial P/\partial\delta \) (curva \( P(\delta) \) más plana), reduciendo la ganancia del lazo de potencia y amortiguándolo, sin el polo lento que añadiría subir \( L_2 \) físico. Coste: más caída de tensión y mayor \( \delta_0 \) en operación (hay que generar el mismo \( P \) con menor pendiente, así que el ángulo de trabajo crece). Por eso \( X_v \) típica \( 0.1\text{–}0.3 \) pu: suficiente para amortiguar sin disparar \( \delta_0 \).

## Cuándo y por qué se usa
- Cuando la reactancia de acoplamiento real es pequeña → \( \partial P/\partial\delta \)
  enorme → el lazo de potencia tiene poco margen de fase y oscila o se inestabiliza.
- Para **desacoplar** P (ángulo) de Q (tensión) haciendo la red vista más inductiva.
- Como base del **current limiting** (impedancia virtual adaptativa en faltas).

## Procedimiento de diseño (genérico)
1. **Elige la parte inductiva \( X_v \)** para fijar la impedancia de acoplamiento total
   deseada (típico 0.1–0.3 pu): \( X_{tot} = X_{fisica} + X_v \). Más \( X_v \) → menor
   \( \partial P/\partial\delta \) → lazo de potencia más amortiguado, pero más caída de
   tensión y mayor \( \delta \) en operación.
2. **Verifica el equilibrio**: la parte **resistiva \( R_v \)** estática introduce una caída
   en el eje d que el droop Q–V intenta compensar generando reactiva → puede disparar
   \( Q_{eq} \). Usa \( R_v \) pequeña.
3. **Para amortiguar sin distorsionar el equilibrio**, usa **resistencia virtual transitoria**:
   aplica \( R_v \) solo a la componente de alta frecuencia de la corriente (filtro paso-alto),
   con corte **por debajo** del modo a amortiguar:
   $$ v_{virt} = R_{v,tr}\,\big(i - \text{LPF}_{f_{ht}}(i)\big) $$
4. **Comprueba con autovalores**: barre \( X_v, R_{v,tr} \) y maximiza el amortiguamiento
   \( \zeta \) del modo de potencia manteniendo \( Q_{eq} \) y \( \delta \) razonables.

## Ejemplo de código
```python
# Impedancia virtual estatica + resistencia virtual transitoria (marco dq)
wht = 2*np.pi*f_ht                      # corte del HPF
iL2_hp = iL2 - iL2_lp                   # componente transitoria (estado iL2_lp = LPF)
vvirt_d = Rv*iL2d - w*Lv*iL2q + Rvt*iL2_hp[0]
vvirt_q = Rv*iL2q + w*Lv*iL2d + Rvt*iL2_hp[1]
vcref_d, vcref_q = Vref - vvirt_d, 0.0 - vvirt_q
diL2_lp = wht*(iL2 - iL2_lp)            # dinamica del filtro paso-bajo
```

## Parámetros y valores típicos
- \( X_v \): 0.1–0.3 pu (en el proyecto, \( L_v = 8\,\text{mH} \approx 0.16\,\text{pu} \)).
- \( R_v \) estática: pequeña (≈0.05 pu) para no disparar Q.
- \( R_{v,tr} \): mayor (≈0.1–0.2 pu) porque solo actúa en transitorios; corte \( f_{ht} \)
  por debajo del modo (en el proyecto, 4 Hz para un modo de 3.3 Hz).

## Errores comunes
- **Usar \( R_v \) resistiva grande** para amortiguar → dispara \( Q_{eq} \) (pelea con el
  droop Q–V). Solución: inductiva para ganancia, transitoria para amortiguamiento.
- **Confundir \( L_v \) virtual con subir \( L_2 \) físico**: el físico añade un polo lento de
  planta y mueve la resonancia LCL; la virtual no.
- Poner el corte del HPF por encima del modo → la resistencia transitoria no actúa donde se
  necesita.

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: estabilizar el lazo de potencia): el primer diseño era
  inestable porque \( \partial P/\partial\delta \) era enorme. Añadir \( L_v = 8\,\text{mH} \)
  estabilizó sin distorsionar el equilibrio, y la \( R_{v,tr} \) subió el amortiguamiento del
  modo de potencia de \( \zeta=0.17 \) a \( \zeta=0.40 \). Implementado en `simulate.py` y
  `model.py`.

## Conceptos relacionados
- [[droop-control]] — la impedancia virtual moldea el lazo de potencia del droop.
- [[control-cascada]] — se aplica sobre la referencia del lazo de tensión.
- [[grid-forming-vs-following]] — pieza casi obligatoria en grid-forming.

## Referencias
- Rocabert et al., *Control of Power Converters in AC Microgrids*, IEEE TPEL 2012.
