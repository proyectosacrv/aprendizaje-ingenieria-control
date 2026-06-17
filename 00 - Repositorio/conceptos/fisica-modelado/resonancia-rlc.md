---
titulo: Resonancia en circuitos RLC
slug: resonancia-rlc
categoria: fisica-modelado
tipo: concepto
nivel: basico
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [entender la resonancia LC, el factor de calidad y por qué hay que amortiguarla]
tags: [resonancia, rlc, factor-calidad, ancho-de-banda, amortiguamiento, filtro, basico]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-06-17
relacionados: [filtro-lcl, impedancia-reactancia, diagrama-bode, respuesta-segundo-orden]
referencias:
  - "Sedra & Smith, Microelectronic Circuits"
  - "Erickson & Maksimovic, Fundamentals of Power Electronics"
---

## Definición
Siempre que en un circuito coexisten una inductancia L (que almacena energía en forma de corriente) y una capacidad C (que la almacena en forma de tensión), existe una frecuencia a la que sus reactancias se cancelan y la energía oscila entre ambas: la frecuencia de resonancia. Cerca de ella, una excitación pequeña produce tensiones o corrientes grandes (un pico de ganancia), tanto más agudo cuanto menor sea la resistencia que disipa la energía.

## Dónde aparece (contexto genérico)
La resonancia RLC no es de ningún componente concreto: surge en cualquier lazo donde un elemento inductivo y uno capacitivo intercambian energía con poca disipación. Da igual que la L sea la bobina de un filtro, la inductancia de un cable o la de dispersión de un transformador, y que la C sea un condensador de filtro, la capacidad de un cable largo o la de un banco. Lo único que fija la resonancia es el par L–C que forman y la resistencia en serie con ellos. Por eso este desarrollo se aplica igual al filtro LCL, a una línea con compensación serie, o a un bus DC con su condensador.

## Desarrollo 1 — frecuencia de resonancia (versión reducida, sin pérdidas)
**Paso 1 — las dos reactancias.** La reactancia de la bobina crece con la frecuencia, XL = omega·L; la del condensador decrece, XC = 1/(omega·C). En un lazo LC la reactancia total es XL − XC.

**Paso 2 — condición de resonancia.** La resonancia es donde las dos reactancias se cancelan (reactancia total nula), es decir donde el circuito deja de comportarse como inductivo o capacitivo y solo queda la resistencia:

omega·L = 1/(omega·C)

**Paso 3 — despejar.** Multiplicando por omega y dividiendo por L:

omega0² = 1/(L·C)   ⟹   omega0 = 1/raiz(L·C)   ⟹   f0 = 1/(2·pi·raiz(L·C))

**Paso 4 — qué pasa en resonancia.** Un RLC serie presenta impedancia mínima (igual a R, porque las reactancias se anulan): a f0 deja pasar la máxima corriente. Un RLC paralelo presenta impedancia máxima: a f0 bloquea. Son la misma resonancia vista desde la conexión serie o paralelo.

## Desarrollo 2 — factor de calidad y amortiguamiento (versión completa, con R)
Sin despreciar la resistencia, conviene cuantificar cómo de agudo es el pico. La impedancia del RLC serie completa es Z(s) = R + s·L + 1/(s·C).

**Factor de calidad Q.** Mide la energía almacenada frente a la disipada por ciclo; equivale a la relación entre la reactancia en resonancia y la resistencia:

Q = omega0·L / R = (1/R)·raiz(L/C)

El término raiz(L/C) es la impedancia característica del tanque: Q es esa impedancia dividida por R. Q alto (R pequeña) significa poca disipación → pico agudo; Q bajo (R grande) → pico suave.

**Amortiguamiento zeta.** Para el par de polos de segundo orden, la relación con Q es:

zeta = 1/(2·Q)

Sin resistencia (R→0) se tiene Q→infinito y zeta→0: el pico es teóricamente infinito y la oscilación, no amortiguada. Con R real el pico es finito.

**Ancho de banda.** El pico no solo sube con Q, también se estrecha: el ancho de banda a −3 dB es

delta_f = f0 / Q

es decir, doblar Q duplica la altura del pico y reduce a la mitad su anchura. Esta es la relación clave para el diseño del amortiguamiento.

**Caso de estudio: efecto de Q en la respuesta.** La gráfica de la izquierda muestra el mínimo de impedancia del RLC serie (más profundo y agudo si R baja); la de la derecha, el pico de resonancia para varios Q: su altura es aproximadamente Q y su anchura f0/Q.

<div class="cfig"><img src="figuras/resonancia-rlc-zf.png" alt="Izquierda: impedancia del RLC serie para Q alto y bajo. Derecha: pico de resonancia para varios Q mostrando altura proporcional a Q y anchura f0/Q"><div class="cap">Izquierda: |Z| del RLC serie cae a un mínimo (=R) en f₀, más agudo cuanto menor es R (mayor Q). Derecha: el pico de resonancia tiene altura ≈ Q y anchura ≈ f₀/Q; a más Q, pico más alto y estrecho (menos amortiguado).</div></div>

## Relación con el filtro LCL
El filtro LCL es un caso de resonancia con dos inductancias: L1 y L2 resuenan contra Cf, y el papel de L en las fórmulas lo hace la inductancia equivalente paralelo Leq = L1·L2/(L1+L2), de modo que fres = 1/(2·pi·raiz(Leq·Cf)). El factor Q y el amortiguamiento se calculan igual. La derivación completa está en [[filtro-lcl]].

## Cuándo y por qué se usa
Aparece en todo filtro LC/LCL de convertidor y en cualquier lazo L–C de la red. Su resonancia, si no se amortigua, hace inestable cualquier lazo de control rápido que la excite. Entender f0 y Q es el paso previo a diseñar el amortiguamiento (pasivo con una resistencia, o activo por realimentación).

## Procedimiento de diseño (genérico)
1. Identifica el par L y C y calcula f0.
2. Calcula Q (o zeta) con la resistencia presente.
3. Si Q es alto (poco amortiguado), añade amortiguamiento: resistencia serie/paralelo (pasivo, con pérdidas) o realimentación (activo, sin pérdidas).
4. Coloca f0 lejos del ancho de banda de control y por debajo de fsw/2.

## Ejemplo de código
```python
import numpy as np
L, C, R = 2e-3, 20e-6, 0.1
f0 = 1/(2*np.pi*np.sqrt(L*C))          # frecuencia de resonancia
Q  = (1/R)*np.sqrt(L/C)                 # factor de calidad
zeta = 1/(2*Q)                          # amortiguamiento
bw  = f0/Q                              # ancho de banda a -3 dB
```

## Parámetros y valores típicos
f0 de un LCL: cientos de Hz a pocos kHz (≈1.1 kHz en el proyecto 01). zeta natural casi nulo; tras amortiguamiento activo se lleva a zeta ≈ 0.1–0.3 (Q ≈ 1.7–5).

## Errores comunes
- Dejar la resonancia sin amortiguar y subir el lazo de corriente → inestabilidad.
- Confundir resonancia serie (mínimo de impedancia) con paralelo (máximo).
- Situar f0 demasiado cerca del ancho de banda del control.
- Olvidar que la inductancia de red se suma a L y baja f0 (caso peor en red débil).

## Uso en proyectos
- 01 / 02 (filtro LCL): la resonancia a ~1.1 kHz aparece como un par de polos poco amortiguados; se trata con amortiguamiento activo (realimentación de la corriente del condensador).

## Conceptos relacionados
- [[filtro-lcl]] · [[impedancia-reactancia]] · [[diagrama-bode]] · [[respuesta-segundo-orden]]

## Referencias
- Sedra & Smith, Microelectronic Circuits.
- Erickson & Maksimovic, Fundamentals of Power Electronics.
