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
fecha_actualizacion: 2026-06-30
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

## 1 — De dónde sale la regla bilineal y por qué preserva la estabilidad
**Paso 1 — el mapeo exacto.** El paso de continuo a discreto exacto es \( z=e^{sT_s} \): un polo en \( s \) se traslada a \( z=e^{sT_s} \). El problema es que \( e^{sT_s} \) es trascendente y no da una función racional en \( z \) (no se implementa como ecuación en diferencias). Hay que aproximarlo.

**Paso 2 — invertir y aproximar el logaritmo.** Despejando, \( s=\dfrac{1}{T_s}\ln z \). Se usa la serie del logaritmo en la variable \( \tfrac{z-1}{z+1} \):

$$ \ln z = 2\left(\frac{z-1}{z+1}+\frac13\left(\frac{z-1}{z+1}\right)^3+\cdots\right) $$

Truncando en el primer término (aproximación de Padé de orden 1, equivalente a la regla del trapecio para integrar):

$$ \boxed{\;s=\frac{2}{T_s}\,\frac{z-1}{z+1}\;} $$

que es la sustitución de **Tustin / bilineal**. Es racional en \( z \), luego cualquier \( C(s) \) racional se convierte en \( C(z) \) racional implementable.

**Paso 3 — despejar el mapeo inverso.** Resolviendo para \( z \):

$$ z=\frac{1+sT_s/2}{1-sT_s/2} $$

**Paso 4 — probar que conserva la estabilidad.** Un polo continuo es estable si está en el semiplano izquierdo, \( \operatorname{Re}s<0 \); un polo discreto es estable si \( |z|<1 \). Hay que ver que la transformación lleva uno al otro. Escribiendo \( s=\sigma+j\omega \):

$$ |z|^2=\frac{|1+sT_s/2|^2}{|1-sT_s/2|^2}=\frac{(1+\sigma T_s/2)^2+(\omega T_s/2)^2}{(1-\sigma T_s/2)^2+(\omega T_s/2)^2} $$

Numerador y denominador comparten el término \( (\omega T_s/2)^2 \); la diferencia está en \( (1+\sigma T_s/2)^2 \) frente a \( (1-\sigma T_s/2)^2 \). Su diferencia es \( 4\cdot(\sigma T_s/2)=2\sigma T_s \). Por tanto:

$$ |z|^2-1=\frac{2\sigma T_s}{(1-\sigma T_s/2)^2+(\omega T_s/2)^2} $$

El denominador es siempre positivo, así que el signo de \( |z|^2-1 \) es el de \( \sigma=\operatorname{Re}s \):

$$ \boxed{\;\operatorname{Re}s<0\;\Longleftrightarrow\;|z|<1\;} $$

El semiplano izquierdo completo se mapea **biyectivamente** al interior del círculo unidad, y el eje \( j\omega \) al borde \( |z|=1 \). Por eso Tustin nunca convierte un controlador estable en uno inestable (al contrario de Euler adelantado, cuyo mapeo \( z=1+sT_s \) puede sacar polos fuera del círculo).

## 2 — Discretizar un PI paso a paso con Tustin
**Paso 1 — el PI en continuo.** Partimos de \( C(s)=K_p+\dfrac{K_i}{s} \) (forma paralela, con \( K_i=K_p/T_i \)). Tiene un polo en el origen (acción integral) y un cero en \( s=-K_i/K_p=-1/T_i \).

**Paso 2 — sustituir Tustin.** Se reemplaza \( s\to\dfrac{2}{T_s}\dfrac{z-1}{z+1} \):

$$ C(z)=K_p+K_i\,\frac{T_s}{2}\,\frac{z+1}{z-1} $$

(el término integral \( K_i/s \) se invierte: \( 1/s\to\tfrac{T_s}{2}\tfrac{z+1}{z-1} \)).

**Paso 3 — combinar sobre denominador común.** Poniendo todo sobre \( z-1 \):

$$ C(z)=\frac{K_p(z-1)+K_i\tfrac{T_s}{2}(z+1)}{z-1}
=\frac{\big(K_p+K_i\tfrac{T_s}{2}\big)z-\big(K_p-K_i\tfrac{T_s}{2}\big)}{z-1} $$

Definiendo los coeficientes \( b_0=K_p+K_i\tfrac{T_s}{2} \), \( b_1=-(K_p-K_i\tfrac{T_s}{2}) \):

$$ C(z)=\frac{b_0+b_1 z^{-1}}{1-z^{-1}} $$

**Paso 4 — pasar a ecuación en diferencias.** Con \( U(z)=C(z)E(z) \), multiplicando en cruz \( (1-z^{-1})U(z)=(b_0+b_1z^{-1})E(z) \), y recordando que \( z^{-1} \) es un retardo de una muestra:

$$ \boxed{\;u[n]=u[n-1]+b_0\,e[n]+b_1\,e[n-1]\;} $$

Es la forma implementable: la salida actual se actualiza con la anterior más una combinación del error actual y el previo. El \( u[n-1] \) realiza el integrador (el polo en \( z=1 \)).

**Paso 5 — comprobar el cero.** El cero de \( C(z) \) está en \( z=-b_1/b_0=\dfrac{K_p-K_i T_s/2}{K_p+K_i T_s/2} \). Con \( K_p=12{,}6 \), \( T_i=40\,\text{ms} \) (\( K_i=315 \)) y \( T_s=100\,\mu\text{s} \) da \( z\approx0{,}9975 \): muy cerca de \( z=1 \), coherente con un cero lento a \( 25\,\text{rad/s} \). El mapeo bilineal del cero coincide hasta la cuarta cifra con \( e^{-T_s/T_i} \), confirmando que el efecto integral se conserva.

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

---

## 3 — Métodos de discretización

**Euler hacia adelante (FE):** \( s \to (z-1)/T_s \). Mapa: \( z = 1 + sT_s \). El semiplano izquierdo continuo se mapea a un círculo de radio \( 1/2 \) centrado en \( z = 1/2 \): para polos continuos rápidos (\( |s|T_s > 2 \)), el mapa cae fuera del círculo unitario. **Puede inestabilizar polos continuos estables** si \( T_s \) es grande respecto al polo.

**Euler hacia atrás (BE):** \( s \to (z-1)/(zT_s) \). Mapa: \( z = 1/(1-sT_s) \). El semiplano izquierdo se mapea al interior de un círculo de radio \( 1/2 \) centrado en \( z = 1/2 \): **siempre estable** (polo continuo estable → polo discreto estable). Sin embargo, distorsiona la dinámica transitoria: los polos se desplazan hacia el origen, lo que acelera artificialmente la respuesta.

**Bilineal (Tustin):** \( s \to 2(z-1)/(T_s(z+1)) \). El eje \( j\omega \) continuo se mapea biyectivamente al círculo unitario \( |z|=1 \): **preserva la respuesta en frecuencia** hasta \( \omega_s/2 \). Es el método estándar para PI, PR y filtros en control de convertidores.

**Prewarping de Tustin:** si se quiere coincidencia exacta a una frecuencia crítica \( \omega_c \) (p.ej. la frecuencia de resonancia del filtro LCL):

$$ s \to \frac{\omega_c}{\tan(\omega_c T_s/2)} \cdot \frac{z-1}{z+1} $$

Esto fuerza \( G_{discreto}(e^{j\omega_c T_s}) = G_{continuo}(j\omega_c) \) exactamente, a costa de mayor distorsión en otras frecuencias.

<div class="cfig"><img src="figuras/discretizacion-controladores-analisis.png" alt="Métodos de discretización: plano z, warping, retardo y escalón discreto"><div class="cap">Panel superior izquierdo: mapeo de polos al plano z para los tres métodos (FE, BE, Tustin). Superior derecho: warping de frecuencia de Tustin — la frecuencia continua se comprime hacia π/Ts. Inferior izquierdo: pérdida de margen de fase por retardo de cómputo (1, 2 y 3 muestras). Inferior derecho: respuesta al escalón de segundo orden en continuo vs discreto para distintos Ts.</div></div>

## 4 — Mapeo de polos y ceros

**Polo continuo → polo discreto.** El mapeo exacto es \( z = e^{sT_s} \). Para un polo real en \( s = -a \):

$$ z = e^{-aT_s} \in (0, 1) \quad\text{(estable si } a > 0 \text{)} $$

Para \( T_s < 1/(10a) \) (el polo es "lento" respecto al periodo de muestreo), todos los métodos son precisos. Para \( T_s > 1/(5a) \), Tustin y BE son preferibles a FE.

**Cero discreto de Tustin.** Al discretizar \( C(s) \) con un cero en \( s = -b \) mediante Tustin, el cero se mapea a:

$$ z_{cero} = -\frac{1 - T_s b/2}{1 + T_s b/2} $$

Si \( b > 0 \) (cero en semiplano izquierdo continuo), el cero discreto puede caer en \( z < -1 \): fuera del círculo unitario, creando un sistema discreto de **no-fase mínima**. Esto ocurre cuando \( b \) es grande (cero rápido) y \( T_s \) no es suficientemente pequeño.

**ZOH.** El retenedor de orden cero modela exactamente el comportamiento del D/A: mantiene el valor de la muestra constante durante \( T_s \). Preserva el polo continuo con el mapa exacto \( z = e^{sT_s} \), pero introduce ceros adicionales que no corresponden a ningún cero del sistema continuo (ceros de ZOH): pueden ser de no-fase mínima.

## 5 — Efecto del retardo y antialiasing

**Retardo de cómputo.** El procesador tarda un tiempo \( T_d \) (típicamente \( 1 \) a \( 1.5 \) muestras) en calcular la salida del control a partir de las medidas. Este retardo se modela como \( z^{-k} \) (con \( k \) muestras enteras) y produce una pérdida de fase:

$$ \Delta\phi = -k\omega T_s \quad\text{(radianes)} = -k \cdot 360° \cdot \frac{f}{f_s} $$

A la frecuencia de cruce \( f_c = 1\,\text{kHz} \) con \( f_s = 10\,\text{kHz} \) y \( k=1 \): \( \Delta\phi = -36° \). Con \( k=2 \): \( -72° \). Por eso el ancho de banda del controlador debe ser \( < f_s/10 \) para que el retardo no consuma todo el margen de fase disponible.

**Filtro antialiasing.** Antes del ADC debe haber un filtro pasa-bajas analógico con frecuencia de corte \( f_{cutoff} \approx f_s/4 \) para atenuar las señales por encima de la frecuencia de Nyquist (\( f_s/2 \)). Sin este filtro, componentes de alta frecuencia se pliegan (alias) sobre el espectro útil y aparecen como señales de baja frecuencia falsas.

**Alias.** Una señal a frecuencia \( f \) muestreada a \( f_s \) aparece como señal a \( f_{alias} = |f - n f_s| \), donde \( n \) es el entero más cercano. Si \( f = 9.5\,\text{kHz} \) y \( f_s = 10\,\text{kHz} \): alias a \( 500\,\text{Hz} \), justo en la banda de control.

**Regla práctica.** Mantener la frecuencia de muestreo \( f_s \geq 20 f_{bw} \) (20 veces el ancho de banda del controlador). Esto garantiza \( < 18° \) de pérdida de fase por retardo de cómputo de 1 muestra.

## 6 — Implementación en punto fijo vs flotante

**Punto flotante (float32/float64).** Implementación directa: los coeficientes \( b_0, b_1, a_1 \) se usan tal cual sin escalado. Overflow solo con exponentes extremos (\( > 10^{38} \) en float32). Es el estándar en DSPs modernos y microcontroladores de 32 bits (Cortex-M4/M7 con FPU).

**Punto fijo (Q15, Q31).** Los coeficientes deben escalarse para caber en el rango del registro. En Q15 (15 bits fraccionarios): rango \( [-1, 1) \), resolución \( 2^{-15} \approx 3\times10^{-5} \). Si el coeficiente supera este rango, hay que reducir la escala del numerador y ajustar la escala de la salida.

**Acumuladores.** Al multiplicar dos valores Q15 se obtiene un resultado Q30; al acumular N multiplicaciones, el resultado puede crecer hasta Q30+\( \log_2 N \) bits. Usar acumuladores de doble precisión (32 o 64 bits) para la suma antes de redondear al formato de salida.

**Código ejemplo — PI con Tustin en Python:**

```python
def pi_tustin(Kp, Ki, Ts):
    """Devuelve coeficientes b0, b1, a1 para u[n] = a1*u[n-1] + b0*e[n] + b1*e[n-1]"""
    b0 = Kp + Ki * Ts / 2
    b1 = -(Kp - Ki * Ts / 2)
    a1 = 1.0  # polo en z=1 (integrador)
    return b0, b1, a1

# Implementación en el loop de control:
# u[n] = u[n-1] + b0*e[n] + b1*e[n-1]
b0, b1, _ = pi_tustin(Kp=12.6, Ki=315, Ts=1e-4)
```

El factor \( b_0 = K_p + K_i T_s/2 \approx K_p \) para \( K_i T_s/2 \ll K_p \): la ganancia proporcional domina el coeficiente de entrada. El factor \( b_1 \approx -K_p \): la acción integral es la diferencia entre la muestra actual y la anterior, dividida por \( T_s \).
