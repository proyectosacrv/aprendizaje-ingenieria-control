---
titulo: Transformador
slug: transformador
categoria: fisica-modelado
tipo: concepto
nivel: basico
proyectos: []
objetivos: [adaptar niveles de tensión y entender la impedancia de cortocircuito]
tags: [transformador, relacion-espiras, impedancia-cortocircuito, basico]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-06-30
relacionados: [sistema-por-unidad, red-thevenin-scr, sistema-trifasico, generador-sincrono, impedancia-reactancia]
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
El transformador real añade resistencia y reactancia de dispersión (la **impedancia de
cortocircuito** \( Z_{cc}=R_{cc}+jX_{cc} \)) y una rama de magnetización. \( X_{cc} \) (típicamente
4–12 % en pu) determina la caída de tensión con carga y **contribuye a la impedancia de red** (afecta
al SCR visto por un convertidor).

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

La tensión multiplica por \( a \) y la corriente divide por \( a \) (multiplica por \( a \) en el denominador), así que la impedancia sale por \( a\cdot a=a^2 \). Por eso una impedancia del secundario "pesa" \( a^2 \) veces más vista desde un primario de mayor tensión. En [[sistema-por-unidad|p.u.]] este factor **desaparece**: como cada lado se normaliza por su propio \( Z_{base}\propto V_{base}^2 \), el \( a^2 \) se cancela y la impedancia es la misma en p.u. desde cualquier lado — la gran ventaja del p.u. en redes con varios niveles de tensión. La \( X_{cc} \) referida así se suma a la de la línea para la [[red-thevenin-scr|impedancia Thévenin]] y el SCR.

## Cuándo y por qué se usa
Para adaptar tensiones (conexión de un convertidor de BT a una red de MT), aislar, y modelar la
impedancia entre el convertidor y la red. En por unidad, su \( X_{cc} \) se suma a la de la línea para
formar la impedancia Thévenin.

## Procedimiento de diseño (genérico)
1. Fija la relación \( a = N_1/N_2 \) por los niveles de tensión deseados.
2. Refiere las impedancias a un lado con \( a^2 \) (o trabaja directamente en pu, donde desaparece).
3. Incluye \( X_{cc} \) en la impedancia de red para el cálculo de cortocircuito y SCR.

## Ejemplo de código
```python
a = 400/20e3                 # relacion BT/MT
Z2 = 1.0 + 1j*5.0            # impedancia en el secundario (MT)
Z2_ref = a**2 * Z2           # referida al primario (BT)
```

## Parámetros y valores típicos
\( X_{cc} \): 4–8 % en distribución, hasta 12–15 % en grandes potencias. La rama de magnetización suele
despreciarse en estudios de red. En pu, la impedancia es la misma vista desde cualquier lado.

## Errores comunes
- No referir las impedancias al cambiar de lado (olvidar el factor \( a^2 \)).
- Despreciar \( X_{cc} \) al calcular cortocircuitos o el SCR.
- Ignorar el desfase de las conexiones Y/Δ (30°) en análisis trifásicos.

## Conceptos relacionados
- [[sistema-por-unidad]] · [[red-thevenin-scr]] · [[sistema-trifasico]] · [[generador-sincrono]] · [[impedancia-reactancia]]

## Referencias
- Chapman, *Máquinas Eléctricas*.
- Fitzgerald, *Electric Machinery*.
