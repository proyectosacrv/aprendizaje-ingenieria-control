---
titulo: Controlador PID
slug: controlador-pid
categoria: control
tipo: tecnica
nivel: basico
proyectos: []
objetivos: [entender que aporta cada termino proporcional, integral y derivativo]
tags: [PID, PI, proporcional, integral, derivativo, basico]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-12
relacionados: [realimentacion, sintonia-pi-pid, sistema-primer-orden, control-cascada]
referencias:
  - "Aström, Hägglund, Advanced PID Control, ISA 2006"
---

## Definición
Controlador que actúa sobre el error con tres términos: **P**roporcional, **I**ntegral y
**D**erivativo. Es el controlador más usado en la industria por su sencillez y eficacia.

## Fundamento teórico
$$ u(t) = K_p\,e(t) + K_i\!\int_0^t e\,d\tau + K_d\,\frac{de}{dt}
   \;\;\Longleftrightarrow\;\; C(s)=K_p+\frac{K_i}{s}+K_d\,s $$
Qué aporta cada término:
- **Proporcional** \( K_p \): reacciona al error actual; más \( K_p \) → más rápido, pero deja
  **error en régimen** y puede oscilar.
- **Integral** \( K_i \): acumula el error pasado; **elimina el error en régimen**, pero añade
  retraso de fase (puede reducir estabilidad y dar *windup*).
- **Derivativo** \( K_d \): anticipa según la tendencia del error; **amortigua** y mejora
  estabilidad, pero amplifica el **ruido** (se suele filtrar).
En convertidores se usa casi siempre **PI** (sin D, por el ruido de conmutación).

<div class="cfig"><img src="figuras/controlador-pid-estructura.png" alt="estructura paralela del PID"><div class="cap">Estructura PID: tres ramas en paralelo sobre el error — proporcional (Kp), integral (Ki/s) y derivativa (Kd·s) — que se suman para formar la acción de control u.</div></div>

## Cuándo y por qué se usa
En lazos de corriente, tensión, velocidad: cuando se quiere seguimiento sin error en régimen con
una estructura simple. Es la base de los lazos en cascada.

## Procedimiento (genérico)
1. Empieza con P para fijar la rapidez.
2. Añade I para anular el error en régimen (cuida el *windup*: usa anti-windup).
3. Añade D (filtrado) solo si necesitas más amortiguamiento y el ruido lo permite.
4. Sintoniza por ancho de banda o cancelación de polo (ver [[sintonia-pi-pid]]).

## Ejemplo de aplicación real
**Problema:** VSC con \( L=2\,\text{mH} \), \( r=50\,\text{m}\Omega \), \( f_{sw}=10\,\text{kHz} \). Diseñar el PI de corriente para \( f_c=1\,\text{kHz} \) con margen de fase real ≥ 45°, considerando el retardo de cómputo \( T_d=150\,\mu\text{s} \).

Paso 1 — cancelación de polo: cero del PI en \( \omega_z=r/L=25\,\text{rad/s} \). Paso 2 — ganancia: \( K_p=L\omega_c=0.002\times6283\approx12.6 \), \( K_i=K_p\,r/L\approx315\,\text{s}^{-1} \). Paso 3 — verificar margen con retardo: desfase del retardo a \( \omega_c \) es \( \omega_c T_d\times(180/\pi)\approx54° \), reduciendo el margen de 90° a 36° (no cumple 45°). Corrección: reducir \( \omega_c \) a 750 Hz (\( K_p\approx9.4 \)), desfase del retardo \( \approx40° \), margen resultante \( \approx50° \). El PI sin considerar el retardo cumpliría en teoría pero no en implementación real.

## Ejemplo de código
```python
# PI discreto con anti-windup (saturacion de la salida)
integ += Ki*e*dt
u = Kp*e + integ
if u > umax: u = umax; integ -= Ki*e*dt    # no acumular si satura
```

## Parámetros y valores típicos
Lazos de convertidor: PI con cero en el polo de la planta. Margen de fase objetivo 45–60°.

## Errores comunes
- Olvidar el **anti-windup**: el integrador se carga al saturar y la respuesta se degrada.
- Usar D con señal ruidosa sin filtrar.

## Conceptos relacionados
- [[realimentacion]] · [[sintonia-pi-pid]] · [[control-cascada]]

## Referencias
- Aström, Hägglund, *Advanced PID Control*, 2006.
