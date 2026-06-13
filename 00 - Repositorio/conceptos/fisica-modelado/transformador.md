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
fecha_actualizacion: 2026-06-12
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
