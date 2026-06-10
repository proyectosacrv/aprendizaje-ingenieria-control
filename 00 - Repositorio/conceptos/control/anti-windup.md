---
titulo: Anti-windup del integrador
slug: anti-windup
categoria: control
tipo: tecnica
nivel: basico
proyectos: []
objetivos: [evitar la sobrecarga del término integral cuando el actuador satura]
tags: [anti-windup, saturacion, integrador, back-calculation, basico, control]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-09
relacionados: [controlador-pid, current-limiting, sintonia-pi-pid, error-regimen-permanente]
referencias:
  - "Aström, Hägglund, PID Controllers, ISA 1995"
  - "Aström, Murray, Feedback Systems, Princeton 2008"
---

## Definición
Conjunto de técnicas que **detienen o corrigen la integración** mientras el actuador está
saturado, para que el término integral no acumule un valor enorme ("wind-up") que retrasaría
gravemente la recuperación.

## Fundamento teórico
Al saturar, el lazo queda **abierto**: el error persiste y el integrador sigue cargando aunque la
salida ya no cambie. La recuperación exige "descargar" esa integral, causando gran sobreimpulso.
Esquema de **back-calculation**: se realimenta la diferencia entre la señal calculada \( u \) y la
saturada \( u_{sat} \) al integrador con ganancia \( 1/T_t \):
$$ \dot I = K_i e + \frac{1}{T_t}\,(u_{sat}-u) $$
Con \( u=K_p e + I \). Cuando no hay saturación, \( u_{sat}=u \) y el término extra desaparece.
Alternativas: **clamping** (congelar \( I \) si satura y el error empuja más a la saturación) o
forma **velocidad** (incremental), que es intrínsecamente anti-windup.

## Cuándo y por qué se usa
En todo lazo PI con límites físicos: corriente, tensión de modulación, par. Imprescindible junto
al [[current-limiting]] de convertidores, donde la referencia se recorta con frecuencia.

## Procedimiento (genérico)
1. Modela el saturador real (límites de \( u \)).
2. Elige el esquema (back-calculation suele ser el más robusto).
3. Sintoniza \( T_t \): regla habitual \( T_t\approx\sqrt{T_i T_d} \) o \( T_t\in[T_i/2,\,T_i] \).
4. Verifica recuperación sin sobreimpulso tras una saturación prolongada.

## Ejemplo de aplicación real
**Problema:** PI de corriente con límite de modulación \( |u|_{max}=1\,\text{p.u.} \). Se aplica una referencia de 2 p.u. durante 80 ms (saturación inevitable). Comparar recuperación con y sin back-calculation (\( T_t=T_i/2 \)).

Sin anti-windup: durante la saturación el integrador acumula hasta \( I\approx K_i\times2\,\text{p.u.}\times0.08\,\text{s}\approx50\,\text{p.u.} \) (con \( K_i=315 \)). Al liberar la saturación, el integrador debe descargarse desde 50 a ~1 p.u. generando un sobreimpulso de corriente de muchas veces la nominal. Con back-calculation: el término \( (u_{sat}-u)/T_t \) mantiene \( I\approx1\,\text{p.u.} \) durante la saturación. Al liberar, el sobreimpulso queda por debajo del 5 %. Ajuste: \( T_t\approx T_i/3\ldots T_i/2 \). Demasiado pequeño → ruidoso; demasiado grande → anti-windup ineficaz.

## Ejemplo de código
```python
def pi_aw(e, I, Kp, Ki, Tt, umin, umax, dt):
    u = Kp*e + I
    usat = min(max(u, umin), umax)
    I += (Ki*e + (usat-u)/Tt)*dt        # back-calculation
    return usat, I
```

## Parámetros y valores típicos
\( T_t \) del orden del tiempo integral \( T_i \) (un poco menor). Demasiado pequeño → ruidoso;
demasiado grande → anti-windup ineficaz.

## Errores comunes
- Saturar la salida pero seguir integrando el error completo (windup clásico).
- Poner \( T_t \) sin relación con \( T_i \).
- Olvidar que en cascada el lazo externo también necesita anti-windup si su salida (referencia
  del interno) se limita.

## Conceptos relacionados
- [[controlador-pid]] · [[current-limiting]] · [[sintonia-pi-pid]] · [[error-regimen-permanente]]

## Referencias
- Aström, Hägglund, *PID Controllers*, 1995.
- Aström, Murray, *Feedback Systems*, 2008.
