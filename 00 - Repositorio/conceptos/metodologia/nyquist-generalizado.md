---
titulo: Criterio de Nyquist generalizado (MIMO, GNC)
slug: nyquist-generalizado
categoria: metodologia
tipo: metodo
nivel: avanzado
proyectos: []
objetivos: [decidir estabilidad de sistemas multivariable y del cociente de impedancias]
tags: [nyquist-generalizado, gnc, mimo, eigenloci, impedancia, minor-loop-gain, avanzado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-01
relacionados: [criterio-nyquist, impedancia-salida-estabilidad, valores-singulares-mimo, criterio-middlebrook]
referencias:
  - "Skogestad, Postlethwaite, Multivariable Feedback Control, Wiley 2005"
  - "Sun, Impedance-Based Stability Criterion for Grid-Connected Inverters, IEEE TPEL 2011"
  - "Belkhayat, Stability Criteria for AC Power Systems with Regulated Loads, PhD Purdue 1997"
---

## Definición
Extensión del [[criterio-nyquist|criterio de Nyquist]] a sistemas **multivariable**: la estabilidad
en lazo cerrado se decide por los rodeos de \( -1 \) de los **loci característicos** (autovalores)
de la matriz de ganancia de lazo \( \mathbf{L}(j\omega) \). Es la base formal del **criterio de
estabilidad por impedancia** en convertidores (cociente de impedancias \( 2\times2 \) en dq).

## Fundamento teórico
Para una planta MIMO con lazo \( \mathbf{L}(s)=\mathbf{C}(s)\mathbf{G}(s) \), el polinomio
característico del lazo cerrado es \( \det(\mathbf{I}+\mathbf{L}(s)) \). Aplicando el principio del
argumento a este determinante:
$$ Z = N\big(\det(\mathbf{I}+\mathbf{L}),\,-1\big) + P_{ol} $$
Equivalentemente (Teorema de Nyquist generalizado), se trazan los **eigenloci**
\( \lambda_i(j\omega)=\mathrm{eig}\,\mathbf{L}(j\omega) \), \( i=1\dots m \), y la suma de sus rodeos
netos de \( -1 \) debe ser \( -P_{ol} \) (polos inestables de lazo abierto) para que \( Z=0 \).

**Aplicación a impedancia (source-load).** Partiendo de un divisor fuente–carga estable por
separado, la tensión en el punto de conexión es
$$ \mathbf{V}=\mathbf{V}_s\big(\mathbf{I}+\mathbf{Z}_s\mathbf{Y}_l\big)^{-1} $$
con **minor loop gain** \( \mathbf{L}=\mathbf{Z}_s\mathbf{Y}_l=\mathbf{Z}_s\mathbf{Z}_l^{-1} \). El
conjunto es estable \( \iff \mathbf{L}(j\omega) \) cumple Nyquist generalizado. En AC trifásico,
\( \mathbf{Z} \) son matrices \( 2\times2 \) en dq → **dos** eigenloci. El caso SISO (DC, o
desacoplado) recupera el [[criterio-middlebrook|criterio de Middlebrook]] (\( Z_s/Z_l \) dentro del
círculo unidad como condición suficiente).

**Criterios suficientes (menos conservadores que la norma).** Calcular eigenloci es costoso y poco
robusto; alternativas:
- Norma: si \( \bar\sigma(\mathbf{Z}_s\mathbf{Y}_l)<1\ \forall\omega \) → estable (muy conservador).
- **G-norm / pasividad**: índices de pasividad de la impedancia (ver [[impedancia-salida-estabilidad|resistencia negativa]]).
- Valores singulares estructurados (μ) para incertidumbre (ver [[valores-singulares-mimo]]).

<div class="cfig"><img src="figuras/nyquist-generalizado-eigenloci.png" alt="eigenloci del minor loop gain frente al punto -1"><div class="cap">En un sistema MIMO la estabilidad la deciden los autovalores (eigenloci) de la matriz de ganancia de lazo $L=Z_sY_l$, no una sola función escalar. La suma de sus rodeos netos del punto $-1$ debe ser $-P_{ol}$; aquí ninguno rodea $-1$, así que el conjunto fuente-carga es estable. Es la base formal del criterio por impedancia en dq.</div></div>

## 1 — De \( \det(\mathbf{I}+\mathbf{L}) \) a los eigenloci: por qué son equivalentes
**Paso 1 — polinomio característico.** El lazo cerrado de un sistema MIMO con ganancia de lazo \( \mathbf{L}(s)\in\mathbb{C}^{m\times m} \) tiene la función característica \( \phi(s)=\det(\mathbf{I}+\mathbf{L}(s)) \). El principio del argumento (Cauchy) aplicado al contorno de Nyquist \( \Gamma \) da el número de ceros menos polos de \( \phi \) en el semiplano derecho:

$$ N = Z - P_{ol} = \frac{1}{2\pi j}\oint_\Gamma \frac{\phi'(s)}{\phi(s)}\,ds $$

Para lazo cerrado estable se requiere \( Z=0 \), es decir \( N=-P_{ol} \) (los rodeos netos de la imagen de \( \phi \) alrededor del origen deben cancelar exactamente los polos de lazo abierto inestables).

**Paso 2 — factorización por autovalores.** Usando la identidad \( \det(\mathbf{I}+\mathbf{L})=\prod_{i=1}^m(1+\lambda_i(\mathbf{L})) \):

$$ \phi(j\omega)=\det(\mathbf{I}+\mathbf{L}(j\omega))=\prod_{i=1}^m\bigl(1+\lambda_i(j\omega)\bigr) $$

Por tanto los rodeos de \( \phi \) alrededor del origen son equivalentes a la suma de los rodeos de cada factor \( (1+\lambda_i) \) alrededor del origen, que a su vez son los rodeos de los **eigenloci** \( \lambda_i(j\omega) \) alrededor de \( -1 \).

**Paso 3 — comparación con SISO.** En SISO (\( m=1 \)) hay un único eigenloci \( \lambda_1=L(j\omega) \) y la condición reduce exactamente al criterio de Nyquist clásico: \( N(j\omega)=1+L(j\omega) \), rodeos de \( -1 \) de \( L \). El GNC es su extensión natural al caso matricial sin ninguna hipótesis adicional.

$$ \boxed{N_{\text{neto rodeos}}\;\text{de } -1 \text{ por todos los eigenloci} = -P_{ol}} $$

## 2 — Aplicación al minor loop gain \( \mathbf{L}=\mathbf{Z}_s\mathbf{Y}_l \) en dq
**Paso 1 — por qué aparece este \( \mathbf{L} \).** La tensión en el PCC entre fuente (admitancia \( \mathbf{Y}_s \)) y carga (admitancia \( \mathbf{Y}_l \)) en el dominio dq satisface:

$$ \mathbf{V}_{PCC} = \mathbf{V}_s\,(\mathbf{Y}_s+\mathbf{Y}_l)^{-1}\mathbf{Y}_l = \mathbf{V}_s\,(\mathbf{I}+\underbrace{\mathbf{Z}_l\mathbf{Y}_s^{-1}}_{\mathbf{L}^{-1}})^{-1} $$

Reescribiendo en la forma estándar de lazo cerrado con \( \mathbf{L}=\mathbf{Z}_s\mathbf{Y}_l \):

$$ \mathbf{V}_{PCC}=\mathbf{V}_s\,(\mathbf{I}+\mathbf{L})^{-1} $$

**Paso 2 — condición de estabilidad.** Si fuente y carga son individualmente estables (\( P_{ol}=0 \)), la condición reduce a \( N=0 \): ningún eigenlocus de \( \mathbf{L}(j\omega) \) debe rodear \( -1 \). En dq, \( \mathbf{L} \) es \( 2\times2 \) → **dos** eigenloci que deben trazar el mapa sin encerrar \( -1 \).

**Paso 3 — recuperación del criterio SISO.** En DC o con acoplamiento d-q nulo, \( \mathbf{L}=\text{diag}(L_d,L_q) \) y cada entrada diagonal es el criterio de Middlebrook/SISO: la estabilidad requiere que ninguna de las dos razones escalares \( Z_{s,d}/Z_{l,d} \) ni \( Z_{s,q}/Z_{l,q} \) rode el punto \( -1 \). El módulo \( |\mathbf{L}|<1 \) (norma de valores singulares) es una **condición suficiente** conservadora para que ningún eigenloci alcance \( -1 \).

## Cuándo y por qué se usa
Estabilidad de convertidor conectado a red (GFL/GFM), interacción entre subsistemas (fuente–carga,
convertidor–convertidor) y microrredes, donde el modelo natural es MIMO y el acoplamiento d-q no es
despreciable. Es el criterio que sustenta el análisis por impedancia de tus proyectos.

## Procedimiento de diseño (genérico)
1. Verifica estabilidad **individual** de fuente y carga (sin interconectar).
2. Forma el minor loop gain \( \mathbf{L}=\mathbf{Z}_s\mathbf{Y}_l \) en la frecuencia (dq, 2×2).
3. Calcula los eigenloci \( \lambda_i(j\omega) \) y cuenta rodeos de \( -1 \).
4. Compara con \( -P_{ol} \); si hay polos inestables de lazo abierto, contabilízalos.
5. Para márgenes, mide la distancia de los eigenloci a \( -1 \) (margen de módulo MIMO).

## Ejemplo de código
```python
import numpy as np
def eigenloci(Zs, Yl, freqs):           # Zs, Yl: (Nf,2,2) en dq
    loci = np.zeros((len(freqs), 2), dtype=complex)
    for k in range(len(freqs)):
        loci[k] = np.linalg.eigvals(Zs[k] @ Yl[k])   # rodeos de -1 -> Nyquist
    return loci
```

## Parámetros y valores típicos
Margen de módulo MIMO (mín. distancia de los eigenloci a \( -1 \)) > 0.3–0.5. Malla de frecuencia
fina alrededor de las resonancias de \( \mathbf{Z}_s,\mathbf{Z}_l \).

## Errores comunes
- Aplicar el criterio sin comprobar la estabilidad individual de fuente y carga.
- Usar \( |Z_s/Z_l|<1 \) (SISO) en un sistema con fuerte acoplamiento d-q → conclusión errónea.
- Olvidar \( P_{ol} \) (rodeos requeridos ≠ 0 cuando hay polos inestables de lazo abierto).
- Confundir el determinante \( \det(\mathbf{I}+\mathbf{L}) \) con uno solo de los eigenloci.

## Conceptos relacionados
- [[criterio-nyquist]] · [[impedancia-salida-estabilidad]] · [[criterio-middlebrook]] · [[valores-singulares-mimo]]

## Referencias
- Skogestad, Postlethwaite, *Multivariable Feedback Control*, 2005.
- Sun, *Impedance-Based Stability Criterion for Grid-Connected Inverters*, IEEE TPEL 2011.
- Belkhayat, *Stability Criteria for AC Power Systems with Regulated Loads*, PhD 1997.
