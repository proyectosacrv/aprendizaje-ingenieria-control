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
fecha_actualizacion: 2026-06-09
relacionados: [criterio-nyquist, impedancia-salida-estabilidad, valores-singulares-mimo, criterio-middlebrook, impedancia-dq-vs-secuencia]
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
- **G-norm / pasividad**: índices de pasividad de la impedancia (ver [[no-pasividad-resistencia-negativa]]).
- Valores singulares estructurados (μ) para incertidumbre (ver [[valores-singulares-mimo]]).

<div class="cfig"><img src="figuras/nyquist-generalizado-eigenloci.png" alt="eigenloci del minor loop gain frente al punto -1"><div class="cap">En un sistema MIMO la estabilidad la deciden los autovalores (eigenloci) de la matriz de ganancia de lazo $L=Z_sY_l$, no una sola función escalar. La suma de sus rodeos netos del punto $-1$ debe ser $-P_{ol}$; aquí ninguno rodea $-1$, así que el conjunto fuente-carga es estable. Es la base formal del criterio por impedancia en dq.</div></div>

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
- [[criterio-nyquist]] · [[impedancia-salida-estabilidad]] · [[criterio-middlebrook]] · [[valores-singulares-mimo]] · [[impedancia-dq-vs-secuencia]]

## Referencias
- Skogestad, Postlethwaite, *Multivariable Feedback Control*, 2005.
- Sun, *Impedance-Based Stability Criterion for Grid-Connected Inverters*, IEEE TPEL 2011.
- Belkhayat, *Stability Criteria for AC Power Systems with Regulated Loads*, PhD 1997.
