---
titulo: Transformador
slug: transformador
categoria: fisica-modelado
tipo: concepto
nivel: basico
proyectos: []
objetivos: [adaptar niveles de tensión, entender la impedancia de cortocircuito y su efecto en el LCL]
tags: [transformador, relacion-espiras, impedancia-cortocircuito, circuito-T, delta-y, basico]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-07-02
relacionados: [sistema-por-unidad, red-thevenin-scr, sistema-trifasico, generador-sincrono, impedancia-reactancia, filtro-lcl]
referencias:
  - "Fitzgerald, Electric Machinery, McGraw-Hill"
  - "Chapman, Máquinas Eléctricas"
---

## Definición
Dispositivo de dos (o más) devanados acoplados por un núcleo magnético que transfiere energía entre
ellos cambiando los niveles de tensión y corriente según la **relación de espiras**, sin conexión
eléctrica directa (aislamiento galvánico).

## Fundamento teórico
En el transformador ideal, con \( N_1 \) y \( N_2 \) espiras:
$$ \frac{V_1}{V_2} = \frac{N_1}{N_2} = a, \qquad \frac{I_1}{I_2} = \frac{N_2}{N_1} = \frac{1}{a} $$
de modo que la potencia se conserva (\( V_1 I_1 = V_2 I_2 \)). Una impedancia \( Z_2 \) en el
secundario se ve desde el primario **referida** por el cuadrado de la relación:
$$ Z_2' = a^2 Z_2 $$
El transformador real añade la **impedancia de cortocircuito** \( Z_{cc}=R_{cc}+jX_{cc} \) (modelada
en el circuito equivalente en T) y una rama de magnetización \( Z_m \). Típicamente
\( X_{cc} \) es 4–12 % en p.u. y \( Z_m \approx 50\text{–}100\cdot X_{cc} \), de modo que la
corriente en vacío \( I_0 < 1\,\%I_n \) y la rama \( Z_m \) se desprecia en estudios de red.

<div class="cfig"><img src="figuras/transformador-simbolo.png" alt="simbolo del transformador"><div class="cap">Transformador ideal: dos devanados acoplados por el núcleo; las tensiones siguen la relación de espiras V1/V2=N1/N2=a, y una impedancia del secundario se ve desde el primario multiplicada por a².</div></div>

## 1 — De dónde sale la relación de transformación \( V_1/V_2=N_1/N_2 \)
**Paso 1 — un flujo común enlaza ambos devanados.** El núcleo magnético obliga a que el mismo flujo \( \phi(t) \) atraviese las \( N_1 \) espiras del primario y las \( N_2 \) del secundario (acoplamiento perfecto, sin dispersión).

**Paso 2 — ley de Faraday en cada devanado.** La tensión inducida en cada bobina es el número de espiras por la derivada del flujo común:

$$ v_1=N_1\frac{d\phi}{dt},\qquad v_2=N_2\frac{d\phi}{dt} $$

**Paso 3 — dividir para eliminar el flujo.** El factor \( d\phi/dt \) es idéntico en ambas (mismo flujo), así que al dividir se cancela:

$$ \frac{v_1}{v_2}=\frac{N_1\,d\phi/dt}{N_2\,d\phi/dt}=\frac{N_1}{N_2}=a\quad\Longrightarrow\quad \boxed{\;\frac{V_1}{V_2}=\frac{N_1}{N_2}=a\;} $$

**Paso 4 — la corriente sale de conservar la potencia.** El transformador ideal no disipa ni almacena energía en régimen, luego \( V_1I_1=V_2I_2 \) (la potencia que entra sale). Despejando el cociente de corrientes y usando \( V_1/V_2=a \):

$$ \frac{I_1}{I_2}=\frac{V_2}{V_1}=\frac{1}{a}\quad\Longrightarrow\quad\boxed{\;I_1=\frac{I_2}{a}\;} $$

La tensión sube con \( a \) y la corriente baja con \( 1/a \): se transforma el **nivel**, no la potencia.

## 2 — Por qué una impedancia se refiere por \( a^2 \)
**Paso 1 — definir la impedancia en cada lado.** En el secundario, \( Z_2=V_2/I_2 \). Vista desde el primario sería \( Z_2'=V_1/I_1 \), con las **mismas** \( V_1,I_1 \) reales del primario.

**Paso 2 — sustituir las relaciones del apartado 1.** Con \( V_1=a\,V_2 \) e \( I_1=I_2/a \):

$$ Z_2'=\frac{V_1}{I_1}=\frac{a\,V_2}{I_2/a}=a^2\,\frac{V_2}{I_2}=a^2 Z_2 $$

$$ \boxed{\;Z_2'=a^2 Z_2\;} $$

La tensión multiplica por \( a \) y la corriente divide por \( a \) (multiplica por \( a \) en el denominador), así que la impedancia sale por \( a\cdot a=a^2 \). Por eso una impedancia del secundario "pesa" \( a^2 \) veces más vista desde un primario de mayor tensión. En [[sistema-por-unidad|p.u.]] este factor **desaparece**: como cada lado se normaliza por su propio \( Z_{base}\propto V_{base}^2 \), el \( a^2 \) se cancela y la impedancia es la misma en p.u. desde cualquier lado.

## 2 — Circuito equivalente exacto y aproximación en T

El transformador real se modela con el **circuito en T**, que añade al transformador ideal:
- **Impedancias de dispersión:** \( Z_s = R_s + jX_s \) (primario) y \( Z_r = R_r + jX_r \) (secundario), ambas referidas al mismo lado. Su suma es la impedancia de cortocircuito:
  $$ Z_{cc} = Z_s + Z_r = R_{cc} + jX_{cc} $$
- **Rama de magnetización:** \( Z_m = R_{Fe} \parallel jX_m \), en paralelo con la fuente de tensión ideal. Modela las pérdidas en el hierro y la corriente de excitación.

La **aproximación habitual** en estudios de red traslada \( Z_m \) a los bornes del primario y la desprecia (\( Z_m \gg Z_{cc} \)), quedando solo la impedancia de cortocircuito en serie:

$$\boxed{\;Z_{cc} = R_{cc} + jX_{cc},\quad X_{cc}[\%] = \frac{Z_{cc}[\Omega]\,S_{base}}{V_{base}^2}\times 100\;}$$

El error de despreciar \( Z_m \) es la corriente en vacío \( I_0 = V_1/Z_m \approx 0{,}3\text{–}1\,\%\,I_n \), despreciable en todos los estudios de potencia.

## 3 — Reactancia de cortocircuito \( X_{cc} \) en %: efecto sobre \( I_{cc} \) y sobre el LCL

La **corriente de cortocircuito** que puede entregar el transformador (secundario en cortocircuito) es directamente la inversa de \( X_{cc}\,\% \):

$$\boxed{\;\frac{I_{cc}}{I_n} = \frac{100}{X_{cc}[\%]}\;}\qquad\text{(resistencia despreciada)}$$

Con \( X_{cc}=6\,\% \) el trafo puede entregar \( 16{,}7\,I_n \); con 12 % solo \( 8{,}3\,I_n \). Por eso los transformadores de gran potencia tienen \( X_{cc} \) más alta: limitan la corriente de falta y reducen el estrés de los interruptores.

**Efecto sobre el filtro LCL.** En un convertidor, el reactor de red \( L_2 \) del LCL ve en serie la inductancia equivalente del transformador:

$$L_2^{eff} = L_2 + L_{cc},\qquad L_{cc} = \frac{X_{cc}[\%]}{100}\cdot\frac{Z_{base}}{\omega_0}$$

Como \( L_2^{eff} > L_2 \), la frecuencia de resonancia del LCL **baja**:

$$f_{res} = \frac{1}{2\pi}\sqrt{\frac{L_1+L_2^{eff}}{L_1\,L_2^{eff}\,C_f}} < f_{res,0}$$

Esto es conveniente para filtrar armónicos pero puede acercar \( f_{res} \) a la frecuencia de conmutación si \( X_{cc} \) es muy alta — hay que verificar siempre.

## 4 — El transformador en dq: términos de acoplamiento ±ωL

En el marco \( dq \) que gira a \( \omega \), cualquier inductancia \( L \) introduce términos de acoplamiento cruzado entre los ejes. El transformador, modelado por su inductancia de cortocircuito \( L_{cc} \), se comporta **exactamente igual que cualquier otro inductor**:

$$\begin{pmatrix}\dot{i}_d\\\dot{i}_q\end{pmatrix} = \frac{1}{L_{cc}}\begin{pmatrix}V_{d,1}-V_{d,2}\\ V_{q,1}-V_{q,2}\end{pmatrix} - \omega\begin{pmatrix}-i_q\\i_d\end{pmatrix}$$

Los términos \( +\omega L_{cc}\,i_q \) y \( -\omega L_{cc}\,i_d \) son los acoplamientos dq que el control debe compensar (feedforward de desacoplamiento). El trafo no añade ninguna novedad respecto a \( L_1 \) o \( L_2 \) del filtro: se suma a ellos en el circuito del eje d y del eje q de manera simétrica.

En p.u. con la base del convertidor el término de acoplamiento es simplemente \( \omega_{pu}\,L_{cc,pu} \), que se suma a los del filtro en los lazos de corriente.

## 5 — Trafo Δ-Y: desfase 30° y filtrado de armónicos triplen

La conexión **Δ en el primario y Y en el secundario** (o al revés, Yd o Dy) tiene dos efectos fundamentales:

**Desfase de 30°.** La tensión de fase del secundario adelanta (grupo Yd) o retrasa (Dy) 30° respecto al primario. En la norma europea, el grupo vector **Yd11** es habitual: el secundario adelanta 330° = −30°, equivalente a un desfase de 30° en el convenio de retraso. Esto es crítico en sistemas con dos transformadores en paralelo: deben ser del mismo grupo vector o se produce circulación de corriente.

**Filtrado de armónicos triplen.** La corriente de secuencia homopolar (3°, 9°, 15°, …) circula libremente en el devanado Δ (se cierra en sí mismo) pero **no puede fluir en el lado Y** si no hay neutro conectado a tierra. El efecto en el espectro:

- Armónicos múltiplos de 3 (3°, 9°, 15°, …) quedan **atrapados** en el devanado Δ y no aparecen en el secundario.
- Solo pasan al secundario los armónicos de secuencia positiva (1°, 7°, 13°, …) y negativa (5°, 11°, 17°, …).

Esto reduce el THD en el lado de red y es una razón práctica para preferir la conexión Δ-Y en parques eólicos y fotovoltaicos.

<div class="cfig"><img src="figuras/transformador-analisis.png" alt="analisis del transformador"><div class="cap">Panel (a): la corriente de cortocircuito Icc/In es 100/Xcc%; los modelos exacto y aproximado son prácticamente iguales porque Zm ≫ Zcc. Panel (b): Icc cae en hipérbola con Xcc%; distribución usa 4–8%, gran potencia 8–15%. Panel (c): filtrado Δ-Y elimina 3° y 9° en el secundario. Panel (d): Xcc del trafo se suma a L2, bajando la frecuencia de resonancia del LCL.</div></div>

## 6 — Diseño iterativo: trafo 33 kV/690 V para parque eólico 10 MVA

**Datos:** parque de 10 MVA, tensión de red 33 kV (MT), tensión del bus del inversor 690 V (BT). Resistencia máxima de cortocircuito 5 %, reactancia de cortocircuito 6 %.

**Paso 1 — relación de espiras.**
$$a = \frac{N_1}{N_2} = \frac{33\,000}{690} \approx 47{,}8$$

**Paso 2 — bases.**
$$Z_{base,HV} = \frac{(33\,000)^2}{10\times10^6} = 108{,}9\,\Omega, \qquad Z_{base,LV} = \frac{690^2}{10\times10^6} = 0{,}0476\,\Omega$$

**Paso 3 — impedancia de cortocircuito en Ω (referida a LV).**
$$Z_{cc,\Omega} = (0{,}05 + j\,0{,}06)\times0{,}0476 = (2{,}38 + j\,2{,}86)\,\text{m}\Omega$$

**Paso 4 — inductancia equivalente** (para el LCL, \( S_{base}=500\,\text{kVA} \)).
$$L_{cc} = \frac{X_{cc,\Omega}}{\omega_0} = \frac{0{,}06\times0{,}0476}{2\pi\times50} \approx 9{,}1\,\mu\text{H}$$

En la base del convertidor (500 kVA, 690 V, \( Z_{base}=0{,}952\,\Omega \), \( L_{base}=3{,}03\,\text{mH} \)):
$$L_{cc,pu} = \frac{0{,}0091\,\text{mH}}{3{,}03\,\text{mH}} \approx 0{,}003\,\text{p.u.}$$

**Paso 5 — verificar resonancia del LCL** con \( L_1=0{,}08\,\text{p.u.} \), \( L_2=0{,}03\,\text{p.u.} \):
$$L_2^{eff} = 0{,}030 + 0{,}003 = 0{,}033\,\text{p.u.}$$
$$f_{res} = \frac{1}{2\pi}\sqrt{\frac{L_1+L_2^{eff}}{L_1\,L_2^{eff}\,C_f}}$$

Con \( C_f=0{,}05\,\text{p.u.} \) esto cae bien alejado de la frecuencia de conmutación (típicamente >2 kHz), así que el diseño es aceptable. Si \( X_{cc} \) fuera 12 %, \( L_{cc,pu} \) doblaría a 0,006 p.u. y habría que reverificar el margen de amortiguamiento activo.

## Cuándo y por qué se usa
Para adaptar tensiones (conexión de un convertidor de BT a una red de MT), aislar, y modelar la
impedancia entre el convertidor y la red. En por unidad, su \( X_{cc} \) se suma a la de la línea para
formar la impedancia Thévenin. La conexión Δ-Y filtra triplen y el desfase 30° es relevante en
sistemas en paralelo.

## Procedimiento de diseño (genérico)
1. Fija la relación \( a = N_1/N_2 \) por los niveles de tensión deseados.
2. Refiere las impedancias a un lado con \( a^2 \) (o trabaja directamente en pu, donde desaparece).
3. Calcula \( L_{cc} \) y súmala a \( L_2 \) del filtro LCL para obtener \( L_2^{eff} \).
4. Verifica que \( f_{res,LCL} \) con \( L_2^{eff} \) mantiene margen respecto a la frecuencia de conmutación.
5. Incluye \( X_{cc} \) en la impedancia de red para el cálculo de cortocircuito y SCR.

## Ejemplo de código
```python
# Bases del convertidor
Sb_conv = 500e3; Vb = 690.0; f0 = 50.0; omega0 = 2*3.14159*f0
Zb = Vb**2 / Sb_conv          # 0.952 Ω
Lb = Zb / omega0               # 3.03 mH

# Trafo 1 MVA, Xcc = 6%
Xcc_pct = 6.0
Sb_trafo = 1e6
Zcc_ohm  = (Xcc_pct/100) * Vb**2 / Sb_trafo   # en LV
Lcc_H    = Zcc_ohm / omega0                     # inductancia equivalente
Lcc_pu   = Lcc_H / Lb                           # en base del convertidor

# Efecto en LCL
L1_pu = 0.08; L2_pu = 0.03; Cf_pu = 0.05
L2eff_pu  = L2_pu + Lcc_pu
fres = (1/(2*3.14159)) * (((L1_pu+L2eff_pu)/(L1_pu*L2eff_pu*Cf_pu*Zb**2/omega0**2))**0.5)
```

## Parámetros y valores típicos
\( X_{cc} \): 4–8 % en distribución, hasta 12–15 % en grandes potencias. La rama de magnetización suele
despreciarse en estudios de red. En pu, la impedancia es la misma vista desde cualquier lado. La
conexión Δ-Y (grupo Yd11) introduce desfase de 30° entre primario y secundario.

## Errores comunes
- No referir las impedancias al cambiar de lado (olvidar el factor \( a^2 \)).
- Despreciar \( X_{cc} \) al calcular cortocircuitos o el SCR.
- Ignorar el desfase de las conexiones Y/Δ (30°) en análisis trifásicos.
- Olvidar sumar \( L_{cc} \) a \( L_2 \) al dimensionar el amortiguamiento del LCL.

## Conceptos relacionados
- [[sistema-por-unidad]] · [[red-thevenin-scr]] · [[sistema-trifasico]] · [[generador-sincrono]] · [[impedancia-reactancia]] · [[filtro-lcl]]

## Referencias
- Chapman, *Máquinas Eléctricas*.
- Fitzgerald, *Electric Machinery*.
