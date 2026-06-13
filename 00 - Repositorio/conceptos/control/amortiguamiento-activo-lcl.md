---
titulo: Amortiguamiento activo del filtro LCL
slug: amortiguamiento-activo-lcl
categoria: control
tipo: tecnica
nivel: avanzado
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [amortiguar la resonancia LCL sin perdidas]
tags: [LCL, resonancia, damping, realimentacion, dq]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-10
relacionados: [resonancia-lcl, filtro-lcl, control-cascada]
referencias:
  - "Dannehl et al., Investigation of Active Damping Approaches for LCL Filters, IEEE TIA 2010"
---

## Definición
Técnica que amortigua la resonancia del [[filtro-lcl]] mediante **realimentación de software**
(sin resistencias físicas), emulando una resistencia de amortiguamiento. Evita las pérdidas
del amortiguamiento pasivo.

## Fundamento teórico
La realimentación de la **corriente del condensador** \( i_{Cf}=i_{L1}-i_{L2} \) a la tensión
de puente con ganancia \( K_{ad} \) emula una resistencia en serie con \( L_1 \):

$$ \mathbf{v}_i = \mathbf{v}_{i,PI} - K_{ad}\,(\mathbf{i}_{L1}-\mathbf{i}_{L2}) $$

Esto añade un término disipativo en la dinámica de \( i_{L1} \) que amortigua los polos de
resonancia (lleva su \( \zeta \) de ~0 a un valor útil).

<div class="cfig"><img src="figuras/amortiguamiento-activo-lcl-polos.png" alt="polos de resonancia LCL al barrer Kad"><div class="cap">Barrido de la ganancia $K_{ad}$: el par de polos de resonancia del LCL parte casi sobre el eje imaginario ($\zeta\approx0$) y, al subir $K_{ad}$, se desplaza hacia la izquierda (más amortiguado). Equivale a una resistencia en serie con $L_1$ pero sin pérdidas.</div></div>

## Cuándo y por qué se usa
Siempre que la resonancia LCL caiga dentro o cerca del ancho de banda de control, o cuando se
quiera subir el lazo de tensión sin excitar la resonancia. Es alternativa al amortiguamiento
pasivo (R en serie con \( C_f \)), que disipa potencia.

## Procedimiento de diseño (genérico)
1. Identifica \( f_{res} \) del LCL.
2. Mide/sintetiza la **corriente del condensador** (o estímala como \( i_{L1}-i_{L2} \)).
3. Elige \( K_{ad} \) [Ω] para el \( \zeta \) objetivo de la resonancia (≈0.3–0.7). Barre
   \( K_{ad} \) observando los polos de resonancia.
4. Verifica que no degrada el margen de los lazos de corriente/tensión.

## Ejemplo de código
```python
iC = iL1 - iL2                 # corriente del condensador (dq)
vi_d = vi_pi_d - Kad*iC[0]     # resistencia virtual en serie con L1
vi_q = vi_pi_q - Kad*iC[1]
```

## Parámetros y valores típicos
\( K_{ad} \) del orden de unos pocos ohmios (en el proyecto, 6 Ω). Existen variantes con
realimentación de \( i_{L2} \) o de la derivada de \( v_C \).

## Errores comunes
- Ganancia excesiva → ruido amplificado y posible inestabilidad de alta frecuencia.
- Estimar \( i_{Cf} \) con retardo de muestreo significativo → el damping pierde eficacia.

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: amortiguar la resonancia): \( K_{ad}=6\,\Omega \) permitió
  subir el lazo de tensión a 350 Hz; la resonancia (1.1 kHz) quedó con \( \zeta\approx0.13 \).

## Conceptos relacionados
- [[filtro-lcl]] · [[control-cascada]]

## Referencias
- Dannehl et al., IEEE TIA 2010.
