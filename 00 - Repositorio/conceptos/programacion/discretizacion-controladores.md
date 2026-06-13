---
titulo: Discretización de controladores (Tustin, ZOH)
slug: discretizacion-controladores
categoria: programacion
tipo: tecnica
nivel: basico
proyectos: []
objetivos: [pasar un controlador continuo a su versión digital implementable]
tags: [discretizacion, tustin, zoh, c2d, retardo, basico, programacion]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-09
relacionados: [controlador-pid, respuesta-frecuencia-ss, sintonia-pi-pid, margenes-estabilidad]
referencias:
  - "Aström, Wittenmark, Computer-Controlled Systems, Prentice Hall 1997"
  - "Franklin, Powell, Digital Control of Dynamic Systems, Addison-Wesley"
---

## Definición
Conversión de un controlador diseñado en el dominio continuo \( C(s) \) a una ecuación en
diferencias \( C(z) \) que se ejecuta cada periodo de muestreo \( T_s \) en el procesador.

## Fundamento teórico
Métodos de mapeo \( s\to z \):
- **Tustin (bilineal):** \( s=\dfrac{2}{T_s}\dfrac{z-1}{z+1} \). Conserva la estabilidad y la
  respuesta en frecuencia (con *warping*); el más usado para PI/PR.
- **ZOH (zero-order hold):** exacto para la planta con retenedor; mapea \( z=e^{sT_s} \).
- **Euler hacia atrás/adelante:** simples, menos precisos; el adelantado puede inestabilizar.

El muestreo añade un **retardo equivalente** de \( \approx T_s/2 \) (ZOH) más el cómputo, que
**resta margen de fase**: \( \Delta\phi\approx-\omega_c(T_s/2+T_{calc}) \). El **prewarping** de
Tustin fuerza coincidencia exacta a una frecuencia crítica \( \omega_0 \).

<div class="cfig"><img src="figuras/discretizacion-controladores-fase.png" alt="fase del PI continuo frente al discretizado por Tustin"><div class="cap">La discretización por Tustin conserva la fase del controlador continuo a baja frecuencia (diferencia $<1°$ en la banda de control), pero el retardo equivalente del muestreo añade fase negativa cerca de $f_s/2$. Por eso el ancho de banda de control debe quedar por debajo de $\sim f_s/10$ para que el margen de fase sobreviva al muestreo y el cómputo.</div></div>

## Cuándo y por qué se usa
En toda implementación digital (DSP/FPGA/micro) de PI, PR, filtros y observadores. Decide el
\( T_s \) y verifica que los márgenes sobreviven al retardo de muestreo.

## Procedimiento (genérico)
1. Diseña \( C(s) \) en continuo con margen de fase holgado.
2. Elige \( T_s \) (\( f_s\gtrsim 10\text{–}20\,f_c \), ligado a \( f_{sw} \)).
3. Discretiza con Tustin (prewarp en la frecuencia clave si importa).
4. Re-verifica márgenes incluyendo retardo de muestreo+cómputo; implementa la ecuación en diferencias.

## Ejemplo de aplicación real
**Problema:** PI de corriente diseñado en continuo: \( C(s)=K_p(1+1/(T_i s)) \) con \( K_p=12.6 \), \( T_i=40\,\text{ms} \), cruce a \( f_c=1\,\text{kHz} \). Discretizar con Tustin a \( T_s=100\,\mu\text{s} \) y verificar que los márgenes se preservan.

Tustin: \( s\leftarrow\tfrac{2}{T_s}\tfrac{z-1}{z+1} \). El cero del PI en continuo está en \( \omega_z=1/T_i=25\,\text{rad/s} \); en discreto, el cero se mapea a \( z_1=e^{-\omega_z T_s}\approx0.9975 \) (muy cerca de \( z=1 \)), manteniendo el efecto integral. A \( f=1\,\text{kHz} \): diferencia de fase entre continuo y discreto <1° — preservación excelente. A \( f=4\,\text{kHz} \) (cercano a \( f_s/2=5\,\text{kHz} \)) el retardo equivalente del ZOH/Tustin introduce ~50° de desfase adicional: por eso el ancho de banda de control debe mantenerse por debajo de \( f_s/10 \). El margen de fase del diseño continuo (36°) baja ~3° con Tustin: cumple.

## Ejemplo de código
```python
import control as ct
Cs = ct.tf([Kp, Ki], [1, 0])           # PI continuo
Cz = ct.sample_system(Cs, Ts, method='bilinear')   # Tustin
num, den = Cz.num[0][0], Cz.den[0][0]  # coeffs para la ecuación en diferencias
```

## Parámetros y valores típicos
\( f_s \) entre 10 y 20 veces el ancho de banda del lazo (a menudo = \( f_{sw} \) o \( 2f_{sw} \)).
Margen de fase a reservar por el muestreo: 5–15°.

## Errores comunes
- Discretizar con \( T_s \) grande y perder margen de fase (oscila el lazo).
- Usar Euler adelantado en lazos rápidos (riesgo de inestabilidad).
- Olvidar el retardo de cómputo al validar márgenes ([[margenes-estabilidad]]).

## Conceptos relacionados
- [[controlador-pid]] · [[sintonia-pi-pid]] · [[respuesta-frecuencia-ss]] · [[margenes-estabilidad]]

## Referencias
- Aström, Wittenmark, *Computer-Controlled Systems*, 1997.
- Franklin, Powell, *Digital Control of Dynamic Systems*.
