---
titulo: Control en cascada (lazos de corriente y tensión)
slug: control-cascada
categoria: control
tipo: tecnica
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance]
objetivos: [regular la tension del condensador con lazos anidados]
tags: [cascada, PI, desacoplo, dq, ancho-de-banda]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [filtro-lcl, amortiguamiento-activo-lcl, marco-dq, droop-control]
referencias:
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
---

## Definición
Arquitectura de control con lazos anidados: un lazo **interno de corriente** (rápido) dentro
de un lazo **externo de tensión** (más lento), cada uno un PI en el marco dq con desacoplo
cruzado.

## Fundamento teórico
Lazo de corriente sobre \( i_{L1} \) (planta \( 1/(sL_1+R_1) \)) y lazo de tensión sobre
\( v_C \). El **desacoplo** cancela los términos cruzados \( \pm\omega L \), \( \pm\omega C \)
del marco giratorio:
$$ v_i = K_{p,i}e_i + K_{i,i}\!\int e_i \;\mp\; \omega L_1 i_{L1q,d} + v_C $$
$$ i_{L1}^{*} = K_{p,v}e_v + K_{i,v}\!\int e_v \;\mp\; \omega C_f v_{Cq,d} $$
**Regla de oro**: cada lazo interno ~5–10× más rápido que el externo (separación de escalas).

## Cuándo y por qué se usa
Estándar en convertidores con control de tensión (grid-forming, UPS). El lazo de corriente da
protección y rechazo rápido; el de tensión fija el punto de operación.

## Procedimiento de diseño (genérico)
1. **Lazo de corriente** (ancho de banda \( f_{ci}\sim f_{sw}/10 \)): PI por cancelación del
   polo de planta → \( K_{p,i}=L_1\omega_{ci},\; K_{i,i}=R_1\omega_{ci} \).
2. **Lazo de tensión** (\( f_{cv}\sim f_{ci}/3 \) a /5): \( K_{p,v}=C_f\omega_{cv} \), \( K_{i,v} \)
   por el cero deseado.
3. Añade **desacoplo** \( \pm\omega L,\ \pm\omega C \) y feedforward de \( v_C \).
4. Si la resonancia LCL limita \( f_{cv} \), añade [[amortiguamiento-activo-lcl]] primero.

## Ejemplo de código
```python
# lazo tension -> referencia de corriente (con desacoplo)
iL1ref_d = Kp_v*ev_d + Ki_v*xvd - w*Cf*vcq
# lazo corriente -> tension de puente (con desacoplo + feedforward vc)
vid = Kp_i*ei_d + Ki_i*xid - w*L1*iL1q + vcd
```

## Parámetros y valores típicos
\( f_{ci} \) ≈ 0.5–1.5 kHz, \( f_{cv} \) ≈ 100–400 Hz. En el proyecto: 1 kHz / 350 Hz.

## Errores comunes
- **Feedforward de corriente de carga mal usado**: en el proyecto desestabilizaba (lazo
  positivo). Verifica los feedforward en lazo cerrado.
- Subir el lazo de tensión sin amortiguar la resonancia LCL → la excita.
- Olvidar el signo del desacoplo cruzado.

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: regular v_C): cascada corriente(1 kHz)/tensión(350 Hz)
  con desacoplo. El feedforward de carga inicial se eliminó por desestabilizar.

## Conceptos relacionados
- [[filtro-lcl]] · [[amortiguamiento-activo-lcl]] · [[marco-dq]] · [[droop-control]]

## Referencias
- Yazdani, Iravani, *Voltage-Sourced Converters in Power Systems*, 2010.
