---
titulo: Diagrama de Bode
slug: diagrama-bode
categoria: control
tipo: concepto
nivel: intermedio
proyectos: []
objetivos: [leer la respuesta en frecuencia, derivar asíntotas, identificar resonancias y ceros RHP, construir el Bode de funciones complejas, diseñar por loop-shaping]
tags: [bode, frecuencia, magnitud, fase, decibelios, resonancia, cero-rhp, fase-no-minima, retardo, loop-shaping, lcl, basico, intermedio]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-07-01
relacionados: [funcion-transferencia, margenes-estabilidad, loop-shaping, respuesta-frecuencia-ss, filtro-lcl, antiresonancia, compensador-adelanto-atraso, transformada-laplace]
referencias:
  - "Ogata, Ingeniería de Control Moderna, Pearson"
  - "Franklin, Powell, Emami-Naeini, Feedback Control of Dynamic Systems, Pearson"
  - "Skogestad & Postlethwaite, Multivariable Feedback Design, Wiley"
  - "Erickson & Maksimovic, Fundamentals of Power Electronics, Springer"
---

## Definición
Par de gráficas que muestran cómo responde un sistema lineal a senoides de distinta frecuencia:
la **magnitud** (en dB) y la **fase** (en grados) de \( G(j\omega) \) frente a la frecuencia (en
escala logarítmica). Es la herramienta visual del diseño en frecuencia porque multiplicar funciones
de transferencia equivale a sumar sus curvas de Bode — y las asíntotas de cada factor elemental se
construyen de cabeza sin calcular el módulo exacto.

## Fundamento teórico

Se evalúa la función de transferencia en \( s=j\omega \):

$$ |G(j\omega)|_{dB}=20\log_{10}|G(j\omega)|, \qquad \angle G(j\omega)=\arg G(j\omega) $$

La descomposición en factores elementales (ganancias, integradores, polos y ceros simples, pares
de polos complejos) hace que cada factor contribuya aditivamente a la curva total. Las reglas de
asíntota son exactas en los extremos y tienen errores de apenas 3 dB en la frecuencia de esquina.

**Factores elementales y su contribución:**

| Factor | Magnitud | Fase |
|---|---|---|
| Ganancia \( K \) | \( 20\log_{10}K \) dB (constante) | \( 0° \) o \( 180° \) si \( K<0 \) |
| Integrador \( 1/(j\omega) \) | \( -20 \) dB/dec, pasa por 0 dB en \( \omega=1 \) | \( -90° \) constante |
| Polo simple \( 1/(1+j\omega/\omega_p) \) | \( 0 \) dB → \( -20 \) dB/dec en \( \omega_p \) | \( 0° \to -90° \) |
| Cero simple \( 1+j\omega/\omega_z \) | \( 0 \) dB → \( +20 \) dB/dec en \( \omega_z \) | \( 0° \to +90° \) |
| Par complejo \( \omega_n^2/(s^2+2\zeta\omega_n s+\omega_n^2) \) | \( 0 \) dB → \( -40 \) dB/dec en \( \omega_n \) | \( 0° \to -180° \) |

La **frecuencia de cruce de ganancia** \( \omega_c \) (donde \( |G|=0 \) dB) fija el ancho de
banda; en ella se lee el **margen de fase** \( \text{PM}=180°+\angle G(j\omega_c) \). La
frecuencia donde la fase cruza \( -180° \) da el **margen de ganancia**
\( \text{GM}=-|G(j\omega_{180°})|_{dB} \).

<div class="cfig"><img src="figuras/diagrama-bode-ejemplo.png" alt="diagrama de Bode de ejemplo"><div class="cap">Bode de \(G(s)=100/[(s+1)(s+10)]\): cada polo añade \(-20\) dB/dec y hasta \(-90°\). Las líneas verticales marcan las frecuencias de esquina 1 rad/s y 10 rad/s.</div></div>

## 1 — De dónde salen las asíntotas de un polo simple (−20 dB/dec, −90°)

**Paso 1 — evaluar el polo en \( j\omega \).** Toma un polo simple \( G(s)=\dfrac{1}{1+s/\omega_p} \). En \( s=j\omega \):

$$ G(j\omega)=\frac{1}{1+j\,\omega/\omega_p} $$

**Paso 2 — módulo y fase.** El módulo de un cociente es el cociente de módulos; la fase, la diferencia de fases. El numerador \( 1 \) tiene módulo \( 1 \) y fase \( 0 \); el denominador \( 1+j\,\omega/\omega_p \) tiene módulo \( \sqrt{1+(\omega/\omega_p)^2} \) y fase \( \arctan(\omega/\omega_p) \):

$$ |G(j\omega)|=\frac{1}{\sqrt{1+(\omega/\omega_p)^2}},\qquad \angle G(j\omega)=-\arctan\!\frac{\omega}{\omega_p} $$

**Paso 3 — pasar a decibelios.** Por definición \( |G|_{dB}=20\log_{10}|G| \). Como \( \log\) de un cociente resta y \( \log\sqrt{x}=\tfrac12\log x \):

$$ |G(j\omega)|_{dB}=-20\log_{10}\sqrt{1+(\omega/\omega_p)^2}=-10\log_{10}\!\Big(1+(\omega/\omega_p)^2\Big) $$

**Paso 4 — asíntota de baja frecuencia.** Si \( \omega\ll\omega_p \), \( (\omega/\omega_p)^2\ll1 \), el argumento del log tiende a \( 1 \) y \( |G|_{dB}\to0 \). La asíntota es **plana a 0 dB**. La fase tiende a \( -\arctan 0=0^\circ \).

**Paso 5 — asíntota de alta frecuencia (la pendiente).** Si \( \omega\gg\omega_p \), \( 1+(\omega/\omega_p)^2\approx(\omega/\omega_p)^2 \), luego:

$$ |G(j\omega)|_{dB}\approx-20\log_{10}\frac{\omega}{\omega_p} $$

Cada vez que \( \omega \) se multiplica por 10 (una década), \( \log_{10}(\omega/\omega_p) \) crece en 1 y la magnitud cae \( 20 \) dB: **pendiente \( -20 \) dB/dec**. La fase tiende a \( -\arctan(\infty)=-90^\circ \). Verificado: en \( \omega=10\,\omega_p \) la fórmula exacta da \( -20.04 \) dB.

$$ \boxed{\;\text{polo simple: } 0\text{ dB} \to -20\text{ dB/dec},\quad \text{fase } 0^\circ\to-90^\circ\;} $$

**Paso 6 — la frecuencia de esquina.** En \( \omega=\omega_p \): \( 1+1=2 \), \( |G|_{dB}=-10\log_{10}2\approx-3.01 \) dB (el conocido "punto de \( -3 \) dB") y \( \angle G=-\arctan1=-45^\circ \) (verificado). Un **cero** simple \( 1+s/\omega_z \) es idéntico con signo opuesto: \( +20 \) dB/dec y \( +90^\circ \). Un **integrador** \( 1/s \) es el caso límite \( \omega_p\to0 \): pendiente \( -20 \) dB/dec y fase \( -90^\circ \) constantes en todo el rango.

## 2 — El par de polos complejos conjugados: Bode exacto y asíntotas

### El sistema de segundo orden canónico

La forma estándar de un sistema de segundo orden con ganancia estática unitaria es:

$$ G(s)=\frac{\omega_n^2}{s^2+2\zeta\omega_n s+\omega_n^2} $$

donde \( \omega_n \) es la **frecuencia natural** (rad/s) y \( \zeta \) es el **factor de amortiguamiento** (adimensional). En \( s=j\omega \):

$$ G(j\omega)=\frac{\omega_n^2}{\omega_n^2-\omega^2+j\,2\zeta\omega_n\omega} $$

### Cálculo explícito del módulo

El denominador es \( (\omega_n^2-\omega^2)+j\,(2\zeta\omega_n\omega) \). Su módulo al cuadrado es la suma de cuadrados de parte real e imaginaria:

$$ |G(j\omega)|^2=\frac{\omega_n^4}{(\omega_n^2-\omega^2)^2+(2\zeta\omega_n\omega)^2} $$

Dividiendo numerador y denominador por \( \omega_n^4 \) y definiendo \( u=\omega/\omega_n \):

$$ |G(j\omega)|^2=\frac{1}{(1-u^2)^2+(2\zeta u)^2} $$

En decibelios:

$$ \boxed{|G(j\omega)|_{dB}=-10\log_{10}\!\Big[(1-u^2)^2+(2\zeta u)^2\Big],\quad u=\frac{\omega}{\omega_n}} $$

### Cálculo explícito de la fase

La fase es el argumento del cociente; como el numerador \( \omega_n^2 \) es real positivo, el argumento viene sólo del denominador con signo cambiado:

$$ \angle G(j\omega)=-\arctan\!\frac{2\zeta\omega_n\omega}{\omega_n^2-\omega^2}=-\arctan\!\frac{2\zeta u}{1-u^2} $$

**Tramo \( u<1 \):** el denominador \( 1-u^2>0 \), por lo que el arctan está en el primer cuadrante y la fase es negativa pero con módulo pequeño (va de \( 0° \) a \( -90° \)).

**En \( u=1 \) (\( \omega=\omega_n \)):** el denominador del arctan se anula y el argumento tiende a \( +\infty \): \( \arctan(+\infty)=90° \), de modo que \( \angle G=-90° \) exactamente para cualquier \( \zeta \).

**Tramo \( u>1 \):** el denominador \( 1-u^2<0 \), el arctan se mueve al segundo cuadrante; la fase cae de \( -90° \) a \( -180° \). En \( u\to\infty \) la fase llega a \( -180° \).

### Las asíntotas

**Baja frecuencia (\( \omega\ll\omega_n \), \( u\to0 \)):**

$$ (1-u^2)^2+(2\zeta u)^2\to 1 \implies |G|_{dB}\to 0 \text{ dB}$$

La asíntota es plana a 0 dB; la fase tiende a \( 0° \).

**Alta frecuencia (\( \omega\gg\omega_n \), \( u\to\infty \)):**

$$ (1-u^2)^2\approx u^4,\quad (2\zeta u)^2\ll u^4 \implies |G|_{dB}\approx-20\log_{10}(u^2)=-40\log_{10}u $$

Cada década en \( \omega \) añade \( 40 \) dB de caída: **pendiente \( -40 \) dB/dec**. La fase se asienta en \( -180° \).

### El pico de resonancia: derivación de \( \omega_r \) y \( |G|_{\max} \)

Para encontrar la frecuencia del pico diferenciamos \( |G(j\omega)|^2 \) respecto a \( \omega \) e igualamos a cero. Es equivalente (y más limpio) maximizar \( |G|^2 \), es decir minimizar el denominador \( D(u)=(1-u^2)^2+(2\zeta u)^2 \):

$$ \frac{dD}{du}=2(1-u^2)\cdot(-2u)+2(2\zeta)^2 u=0 $$

Dividiendo por \( 2u \) (el caso \( u=0 \) es un mínimo local, no el máximo que buscamos):

$$ -2(1-u^2)+4\zeta^2=0 \implies 2u^2=2-4\zeta^2 \implies u^2=1-2\zeta^2 $$

Esto solo tiene solución real positiva cuando \( 1-2\zeta^2>0 \), es decir, cuando:

$$ \zeta<\frac{1}{\sqrt{2}}\approx 0.707 $$

La frecuencia de resonancia (donde ocurre el pico) es:

$$ \boxed{\omega_r=\omega_n\sqrt{1-2\zeta^2}} $$

Sustituyendo \( u_r^2=1-2\zeta^2 \) en \( D(u_r) \):

$$D(u_r)=(1-(1-2\zeta^2))^2+(2\zeta)^2(1-2\zeta^2)=(2\zeta^2)^2+4\zeta^2(1-2\zeta^2)$$
$$=4\zeta^4+4\zeta^2-8\zeta^4=4\zeta^2(1-\zeta^2)$$

Por tanto el valor pico es:

$$ \boxed{|G(j\omega_r)|_{\max}=\frac{1}{\sqrt{4\zeta^2(1-\zeta^2)}}=\frac{1}{2\zeta\sqrt{1-\zeta^2}}} $$

En decibelios: \( |G|_{\max,dB}=-20\log_{10}(2\zeta\sqrt{1-\zeta^2}) \).

### Tabla numérica del pico

| \( \zeta \) | \( \omega_r/\omega_n \) | \( \|G\|_{\max} \) | Pico [dB] | Notas |
|---|---|---|---|---|
| 0.10 | 0.990 | 5.03 | **+14.0 dB** | Resonancia muy afilada |
| 0.30 | 0.906 | 1.75 | **+4.9 dB** | Pico notable |
| 0.50 | 0.707 | 1.15 | **+1.2 dB** | Pico leve, ≈ −3 dB en \( \omega_n \) |
| 0.70 | 0.141 | 1.02 | **+0.2 dB** | Casi crítico; sin pico apreciable |
| 1.00 | — | — | — | Sobreamortiguado: sin pico |

Para \( \zeta\ge 1/\sqrt{2}\approx0.707 \) no existe \( \omega_r \) real positivo y la respuesta en frecuencia decrece monótonamente desde 0 dB.

<div class="cfig"><img src="figuras/diagrama-bode-analisis.png" alt="Bode avanzado: segundo orden, cero RHP, LCL, retardo"><div class="cap">Panel (a): magnitud y fase del segundo orden canónico para cuatro valores de amortiguamiento; los círculos marcan la frecuencia \(\omega_r\) donde ocurre el pico. Panel (b): cero RHP vs LHP — mismo módulo, fase opuesta; el área sombreada es la pérdida de margen de fase que impone el RHP. Panel (c): Bode de \(i_2/v_i\) del filtro LCL con las asíntotas \(-20\) dB/dec (baja frecuencia) y \(-60\) dB/dec (alta frecuencia) y las frecuencias de antirresonancia \(f_{ar}\) y resonancia \(f_{res}\). Panel (d): efecto del retardo digital \(\tau=1.5\,T_s\) sobre el margen de fase en el cruce a 1 kHz.</div></div>

## 3 — Cero en el semiplano derecho (fase no mínima)

### Qué es un cero RHP

Un **cero en el semiplano derecho** (Right-Half Plane, RHP) es un cero de la función de
transferencia \( G(s) \) situado en \( s=+z \) con \( z>0 \). El ejemplo más común en electrónica
de potencia es el convertidor buck en modo de control por corriente de pico:

$$ G(s)=\frac{1-s/z}{1+s/p}, \qquad z>0,\; p>0 $$

El numerador \( 1-s/z \) tiene su cero en \( s=+z \) (semiplano derecho).

### Módulo idéntico, fase opuesta

Compara \( G_{\text{LHP}}(s)=(1+s/z)/(1+s/p) \) (cero LHP) con \( G_{\text{RHP}}(s)=(1-s/z)/(1+s/p) \) (cero RHP). En \( s=j\omega \):

$$G_{\text{LHP}}(j\omega)=\frac{1+j\omega/z}{1+j\omega/p},\qquad G_{\text{RHP}}(j\omega)=\frac{1-j\omega/z}{1+j\omega/p}$$

Los módulos del numerador son \( |1\pm j\omega/z|=\sqrt{1+(\omega/z)^2} \): **idénticos** para ambos casos. El denominador es igual en los dos. Conclusión:

$$ |G_{\text{LHP}}(j\omega)|=|G_{\text{RHP}}(j\omega)|=\frac{\sqrt{1+(\omega/z)^2}}{\sqrt{1+(\omega/p)^2}} $$

Las curvas de magnitud en el Bode son exactamente iguales. La diferencia está en la fase:

$$\angle G_{\text{LHP}}(j\omega)=+\arctan\!\frac{\omega}{z}-\arctan\!\frac{\omega}{p}$$

$$\angle G_{\text{RHP}}(j\omega)=-\arctan\!\frac{\omega}{z}-\arctan\!\frac{\omega}{p}$$

El cero LHP **aporta fase positiva** (adelanto); el cero RHP **aporta fase negativa** (atraso).
En alta frecuencia (\( \omega\to\infty \)):

- \( G_{\text{LHP}} \): fase total \( +90°-90°=0° \)
- \( G_{\text{RHP}} \): fase total \( -90°-90°=-180° \)

El cero RHP convierte un sistema de "fase mínima" en uno de **fase no mínima**: para una dada
magnitud, la fase es la mínima posible con el cero LHP, y cualquier cero RHP añade retraso
adicional e inevitable.

### Por qué limita el ancho de banda

El margen de fase en la frecuencia de cruce \( \omega_c \) se calcula como:

$$\text{PM}=180°+\angle L(j\omega_c)$$

Si \( L(s)=G_{\text{planta}}(s)\cdot C(s) \) y la planta tiene un cero RHP en \( z \), la fase de ese cero en \( \omega_c \) es \( -\arctan(\omega_c/z) \). Para que PM\( \geq 45° \) hace falta:

$$\angle L(j\omega_c)\geq -135° \implies \arctan\!\frac{\omega_c}{z}\leq 45° \implies \omega_c\leq z$$

Para mantener \( \text{PM}\geq45° \) con margen cómodo se suele tomar \( \omega_c\leq z/3 \) o incluso \( z/5 \). El cero RHP impone un **techo absoluto sobre el ancho de banda** aunque el controlador sea perfecto.

### Ejemplo numérico

Con \( z=100 \) rad/s (\( f_z\approx15.9 \) Hz), \( p=1000 \) rad/s:

La fase del cero RHP en \( \omega_c=30 \) rad/s es \( -\arctan(30/100)=-16.7° \). Si la planta base ya consume \( -90° \) (un polo en 0) y el polo de la planta en \( p=1000 \) añade \( -\arctan(30/1000)\approx-1.7° \):

$$\angle L=-90°-1.7°-16.7°=-108.4° \implies \text{PM}=71.6°\quad\checkmark$$

Si subiésemos a \( \omega_c=100 \) rad/s (\( =z \)):

$$\angle L=-90°-5.7°-45°=-140.7° \implies \text{PM}=39.3°\quad\text{(insuficiente)}$$

La frecuencia de cruce máxima para PM\( \geq45° \) es la \( \omega_c \) donde \( \angle L=-135° \):

$$90°+\arctan\!\frac{\omega_c}{1000}+\arctan\!\frac{\omega_c}{100}=135°$$

Resolviendo numéricamente: \( \omega_c\approx83 \) rad/s (\( f_c\approx13.2 \) Hz). El cero RHP a 15.9 Hz limita el lazo a ~13 Hz.

## 4 — Construir el Bode de una función compleja: suma de asíntotas

### La función de ejemplo

$$G(s)=\frac{K\,(s+z_1)}{s\,(s+p_1)\,(s^2+2\zeta\omega_n s+\omega_n^2)}$$

con \( K=5\cdot10^7 \), \( z_1=200 \) rad/s, \( p_1=3000 \) rad/s, \( \zeta=0.3 \), \( \omega_n=5000 \) rad/s.

### Paso 1 — factorizar en forma normalizada

Se extrae la ganancia a frecuencia DC de cada factor para que todos valgan 1 en \( \omega=0 \). Para el par de polos complejos el factor normalizado es \( \omega_n^2/(s^2+2\zeta\omega_n s+\omega_n^2) \), que vale 1 en CC. El integrador \( 1/s \) no tiene valor en CC, pero su escala se ajusta en el siguiente paso:

$$G(s)=\frac{K\,z_1}{\omega_n^2\,p_1}\cdot\frac{(1+s/z_1)}{s\,(1+s/p_1)\,(s^2/\omega_n^2+2\zeta s/\omega_n+1)}\cdot\frac{\omega_n^2}{1}$$

Ganancia estática de los factores normalizados (excluyendo el integrador): \( K_0=K\,z_1/(p_1) \).

### Paso 2 — calcular dónde empieza la curva

Con un integrador \( 1/s \) la curva en baja frecuencia no es constante sino una recta de \( -20 \) dB/dec que pasa por \( 0 \) dB cuando \( \omega=K_0 \) (si \( K_0 \) está en la escala adecuada). Con los valores del ejemplo: \( K_0=5\cdot10^7\cdot200/3000=3.33\cdot10^6 \). La recta \( K_0/\omega \) en dB vale 0 dB en \( \omega=K_0=3.33\cdot10^6 \) rad/s y 120 dB en \( \omega=1 \) rad/s.

### Paso 3 — lista de frecuencias de esquina ordenadas

| Frecuencia | Factor | Tipo | Efecto en magnitud | Efecto en fase |
|---|---|---|---|---|
| \( \omega=0 \) | \( 1/s \) | Integrador | Parte de \(-20\) dB/dec | \(-90°\) constante |
| \( \omega_z=200 \) rad/s | \( 1+s/z_1 \) | Cero simple | \(+20\) dB/dec (pendiente 0) | \(+90°\) total |
| \( \omega_p=3000 \) rad/s | \( 1/(1+s/p_1) \) | Polo simple | \(-20\) dB/dec | \(-90°\) total |
| \( \omega_n=5000 \) rad/s | Par compl. | Polo doble | \(-40\) dB/dec adicional | \(-180°\) total |

### Paso 4 — sumar asíntotas de magnitud

- Para \( \omega\ll 200 \): solo el integrador activo, pendiente \( -20 \) dB/dec.
- Para \( 200<\omega<3000 \): integrador + cero se cancelan, pendiente \( 0 \) dB/dec (plana).
- Para \( 3000<\omega<5000 \): integrador + cero + polo → pendiente \( -20 \) dB/dec de nuevo.
- Para \( \omega\gg 5000 \): integrador + cero + polo + par compl. → pendiente \( -60 \) dB/dec.

### Paso 5 — sumar asíntotas de fase

- Para \( \omega\ll 200 \): \( -90° \) (integrador solo).
- En \( \omega\approx 200 \): el cero empieza a añadir fase → la fase sube hacia \( -90°+90°=0° \).
- En \( \omega\approx 3000 \): el polo la baja → vuelve hacia \( -90° \).
- En \( \omega\approx 5000 \): el par complejo la arrastra hasta \( -90°-180°=-270° \).
- En alta frecuencia: \( -270° \) asintótico.

### Paso 6 — verificación en tres frecuencias

| \( \omega \) [rad/s] | Asíntota [dB] | Exacto [dB] | Error |
|---|---|---|---|
| 100 | 120 dB − 20·log(100/1)=80 dB (aprox) | 78.5 dB | 1.5 dB |
| 1000 | ~60 dB (plana, zona cero+integrador) | 61.1 dB | 1.1 dB |
| 10000 | ~20 dB − 60·log(10000/5000)=2 dB | 4.3 dB | 2.3 dB |

Los errores son siempre pequeños salvo en la vecindad inmediata de las frecuencias de esquina (máximo ~3 dB en cada una).

## 5 — El Bode del LCL: interpretación paso a paso

### Parámetros de referencia

Tomamos el LCL de la ficha [[filtro-lcl]]: \( L_1=2 \) mH, \( L_2=0.5 \) mH, \( C_f=15\,\mu\text{F} \), con una resistencia de amortiguamiento pasivo \( R_d=0.5\,\Omega \) en serie con \( C_f \).

### La función de transferencia \( i_2/v_i \)

Con \( v_{pcc}=0 \) y \( R_d \) en serie con el condensador, la FDT es (ver [[filtro-lcl]] §1):

$$\frac{I_2(s)}{V_i(s)}=\frac{1+s\,R_d C_f}{s\,L_1 L_2 C_f\,s^2 + s\,R_d C_f(L_1+L_2)\,s + (L_1+L_2)}$$

Más explícito como cociente de polinomios en \( s \):

$$\frac{I_2}{V_i}=\frac{R_d C_f\,s+1}{L_1 L_2 C_f\,s^3+R_d C_f(L_1+L_2)\,s^2+(L_1+L_2)\,s}$$

### Frecuencias características

La **antirresonancia** (cero del numerador, cuando \( R_d=0 \) la FDT \( i_1/v_i \) tiene un cero aquí):

$$\omega_{ar}=\frac{1}{\sqrt{L_2 C_f}}=\frac{1}{\sqrt{0.5\cdot10^{-3}\cdot15\cdot10^{-6}}}\approx 11\,547\,\text{rad/s}\implies f_{ar}\approx1838\,\text{Hz}$$

La **resonancia** (raíces del denominador cúbico, sin \( R_d \)):

$$\omega_{res}=\sqrt{\frac{L_1+L_2}{L_1 L_2 C_f}}=\sqrt{\frac{2.5\cdot10^{-3}}{2\cdot10^{-3}\cdot0.5\cdot10^{-3}\cdot15\cdot10^{-6}}}\approx 12\,910\,\text{rad/s}\implies f_{res}\approx2054\,\text{Hz}$$

> Con los parámetros exactos usados en la figura (\( L_2=0.5 \) mH, \( C_f=15\,\mu\text{F} \)): \( f_{ar}\approx1838 \) Hz y \( f_{res}\approx2054 \) Hz. La figura del panel (c) muestra valores ligeramente distintos porque usa \( R_d=0.5\,\Omega \), que desplaza levemente las frecuencias.

### Construcción del Bode por asíntotas

**Zona 1 — \( f\ll f_{ar} \) (baja frecuencia):** los dos inductores están en serie (la impedancia del condensador es muy alta) y la corriente es \( i_2\approx v_i/[s(L_1+L_2)] \). Esto es un **integrador** con inductancia \( L_1+L_2=2.5 \) mH: pendiente \( -20 \) dB/dec. A \( f=1 \) Hz la magnitud es \( 1/(2\pi\cdot1\cdot2.5\cdot10^{-3})\approx63.7\;\text{A/V} = 36 \) dB.

**Zona 2 — alrededor de \( f_{ar} \):** el condensador resuena con \( L_2 \) (antirresonancia). Sin \( R_d \) la impedancia de esa malla se anula y la corriente \( i_2\to 0 \): el Bode cae a \( -\infty \). Con \( R_d=0.5\,\Omega \) el mínimo es finito pero muy profundo.

**Zona 3 — alrededor de \( f_{res} \):** el denominador cúbico tiene raíces complejas que producen un pico de resonancia. Sin amortiguamiento sube a \( +\infty \); con \( R_d \) el pico tiene amplitud finita. Aquí la fase cruza de \( -90° \) (pendiente de -40 dB/dec) hacia abajo y llega a \( -270° \) al pasar la resonancia.

**Zona 4 — \( f\gg f_{res} \):** todos los factores activos: dos inductores + condensador → pendiente \( -60 \) dB/dec. La atenuación de este filtro de tercer orden hace que a \( f_{sw}=10 \) kHz (5× por encima de \( f_{res} \)) la atenuación relativa sea \( -60\log(5)\approx -42 \) dB adicionales.

### Por qué la fase tiene saltos de ±180°

- En \( f_{ar} \) la magnitud pasa por un mínimo muy profundo (cero teórico sin \( R_d \)). La fase de un cero RLC salta de \( -90° \) a \( +90° \) (sube 180°), porque el cero del numerador al cruzar el eje jω invierte el signo.
- En \( f_{res} \) la magnitud tiene un máximo (polo); la fase salta 180° hacia abajo, de \( -90° \) a \( -270° \).
- Con \( R_d \), estos saltos son suavizados pero el sentido se preserva: la fase sube en \( f_{ar} \) y baja en \( f_{res} \).

## 6 — Sensibilidad al retardo en el Bode: cómo cambia el margen con \( T_s \)

### El retardo digital en el dominio de la frecuencia

Un retardo puro de tiempo \( \tau \) tiene función de transferencia \( e^{-s\tau} \). En \( s=j\omega \):

$$e^{-j\omega\tau}=\cos(\omega\tau)-j\sin(\omega\tau)$$

Su módulo es \( |e^{-j\omega\tau}|=1 \) para todo \( \omega \): el retardo **no cambia la magnitud**. Pero su fase es:

$$\angle e^{-j\omega\tau}=-\omega\tau\quad\text{[rad]}=-\omega\tau\cdot\frac{180°}{\pi}\quad\text{[grados]}$$

La fase crece linealmente con la frecuencia en escala lineal (en escala logarítmica la pérdida de fase se acelera sin límite).

### Retardo efectivo en un convertidor digital

En un sistema digital con periodo de muestreo \( T_s \), el retardo total no es exactamente \( T_s \). Hay tres contribuciones:

1. **Retardo de muestreo**: el modulador actualiza la referencia al inicio del periodo, pero la sensal muestreada tiene, en media, un retraso de \( T_s/2 \).
2. **Retardo de cálculo**: el algoritmo del DSP tarda hasta un periodo completo en ejecutarse.
3. **ZOH (Zero-Order Hold)**: el DAC mantiene la salida constante durante \( T_s \), lo que equivale a otro \( T_s/2 \).

El retardo total efectivo es \( \tau\approx 1.5\,T_s \) (resultado estándar para DSP con cálculo en un periodo).

### Cuantificación de la pérdida de margen

Con un lazo de corriente diseñado para cruzar a \( \omega_c=2\pi\cdot1000 \) rad/s, la fase adicional
que añade el retardo en ese punto es:

$$\Delta\phi=-\omega_c\tau=-\omega_c\cdot1.5\,T_s\;\text{[rad]}$$

En grados:

$$\Delta\phi_{°}=-\omega_c\cdot1.5\,T_s\cdot\frac{180°}{\pi}$$

| \( T_s \) | \( \tau=1.5\,T_s \) | \( \Delta\phi \) a 1 kHz | PM efectivo si PM\(_0\)=45° |
|---|---|---|---|
| 50 µs (20 kHz) | 75 µs | \(-2\pi\cdot1000\cdot75\cdot10^{-6}\cdot180/\pi\approx -27°\) | **18°** (marginal) |
| 100 µs (10 kHz) | 150 µs | \(-2\pi\cdot1000\cdot150\cdot10^{-6}\cdot180/\pi\approx -54°\) | **−9° (inestable)** |
| 200 µs (5 kHz) | 300 µs | \(\approx -108°\) | **−63° (muy inestable)** |

Con \( T_s=100 \) µs y un lazo diseñado ignorando el retardo, el sistema **oscila** al conectarlo.

### La regla de diseño con retardo

El margen de fase efectivo es \( \text{PM}_\text{ef}=\text{PM}_0-\omega_c\cdot1.5\,T_s\cdot(180°/\pi) \). Para garantizar \( \text{PM}_\text{ef}\geq\phi_\text{min} \), el controlador debe diseñarse con margen objetivo:

$$\boxed{\text{PM}_{0,\text{objetivo}}=\phi_\text{min}+\omega_c\cdot1.5\,T_s\cdot\frac{180°}{\pi}}$$

O bien reducir \( \omega_c \) hasta que la pérdida de fase sea tolerable. Como regla práctica, para \( T_s=100 \) µs y PM mínimo de 45°, el cruce no debe superar:

$$f_c\leq\frac{45°/27°}{2\pi\cdot1.5\cdot100\cdot10^{-6}}\approx500\;\text{Hz}$$

### Cómo el compensador de adelanto recupera el margen

Un compensador de adelanto de fase (lead compensator) de la forma:

$$C_\text{lead}(s)=\frac{1+s/\omega_z}{1+s/\omega_p},\quad \omega_z<\omega_p$$

aporta un pico de fase en la frecuencia geométrica media \( \omega_m=\sqrt{\omega_z\,\omega_p} \), con valor:

$$\phi_\text{max}=\arcsin\!\frac{\omega_p-\omega_z}{\omega_p+\omega_z}=\arcsin\!\frac{1-\sqrt{\alpha}}{1+\sqrt{\alpha}},\quad \alpha=\frac{\omega_z}{\omega_p}<1$$

Eligiendo \( \omega_m=\omega_c \) y \( \phi_\text{max} \) igual a la pérdida por retardo, el lead compensa exactamente el deterioro del margen. La penalización es un aumento de ganancia en alta frecuencia (mayor amplificación de ruido en \( \omega_p \)).

## 7 — Diseño por loop-shaping: especificación → curva de Bode → controlador

### Las especificaciones del lazo

El diseño en frecuencia parte de requisitos cuantificables:

- **Ancho de banda**: \( f_c=1 \) kHz (\( \omega_c=2\pi\cdot1000 \) rad/s) → velocidad de respuesta.
- **Margen de fase**: PM \( \geq 45° \) → amortiguamiento del lazo cerrado, \( \zeta_\text{cl}\geq0.35 \).
- **Margen de ganancia**: GM \( \geq 6 \) dB → robustez frente a variaciones de parámetros.
- **Pendiente en el cruce**: \( -20 \) dB/dec → garantiza PM suficiente incluso sin calcularlo.
- **Rechazo de perturbaciones**: \( |L(j\omega)|\gg1 \) para \( \omega\ll\omega_c \) → error de régimen pequeño.

### Paso 1 — trazar la curva objetivo \( L_\text{obj}(j\omega) \)

La curva de lazo abierto objetivo \( L_\text{obj} \) debe:

1. Cruzar 0 dB en \( \omega_c=2\pi\cdot1000 \) rad/s.
2. Tener pendiente \( -20 \) dB/dec en \( \omega_c \) (una década alrededor del cruce).
3. Tener fase \( > -135° \) en \( \omega_c \) (para PM \( \geq 45° \)).
4. Caer rápido para \( \omega\gg\omega_c \) (rechazar ruido de alta frecuencia).

Una función que cumple los tres primeros criterios con la planta más simple (\( G=1/(sL_1) \)) es:

$$L_\text{obj}(s)=\frac{\omega_{ci}}{s},\quad \omega_{ci}=\omega_c$$

Magnitud: \( |L_\text{obj}(j\omega_c)|=\omega_{ci}/\omega_c=1 \) → 0 dB \( \checkmark \). Fase: \( \angle(1/(j\omega))=-90° \) → PM = \( 180°-90°=90° \) \( \checkmark \). Pendiente: \( -20 \) dB/dec constante \( \checkmark \).

### Paso 2 — dividir por la planta para obtener el controlador

Con planta \( G(s)=1/(sL_1) \) (un inductor, válida para \( f<f_{res} \)):

$$C(s)=\frac{L_\text{obj}(s)}{G(s)}=\frac{\omega_{ci}/s}{1/(sL_1)}=\omega_{ci}\,L_1$$

El controlador resultante es una ganancia proporcional pura:

$$\boxed{C(s)=K_p=\omega_{ci}\,L_1=2\pi\cdot1000\cdot2\cdot10^{-3}=12.57\;\text{A/V}}$$

Verificación: \( |L(j\omega_c)|=K_p\cdot|G(j\omega_c)|=12.57\cdot1/(2\pi\cdot1000\cdot2\cdot10^{-3})=1 \) → 0 dB \( \checkmark \).

### Paso 3 — añadir integrador para error nulo en CC

La ganancia proporcional pura tiene error de régimen permanente distinto de cero frente a una referencia constante. Se añade un polo en el origen (acción integral):

$$C(s)=K_p\cdot\frac{1+s/\omega_i}{s/\omega_i}=K_p\cdot\frac{\omega_i+s}{s}$$

con \( \omega_i\ll\omega_c \) (normalmente \( \omega_i=\omega_c/10 \)) para que el integrador apenas afecte a la fase en \( \omega_c \). La pérdida de fase en \( \omega_c \) que añade la parte integral es \( \arctan(\omega_c/\omega_i)^{-1}\approx5.7° \) para \( \omega_i=\omega_c/10 \).

### Paso 4 — verificar realizabilidad y añadir filtro de alta frecuencia

El controlador \( C(s)=(K_p/\omega_i)(s+\omega_i)/s \) tiene grado de denominador = grado de numerador (bipropio), lo que es realizable. Para atenuar el ruido de alta frecuencia y evitar excitar la resonancia del LCL, se añade un polo de corte:

$$C(s)=K_p\cdot\frac{1+s/\omega_i}{s/\omega_i}\cdot\frac{1}{1+s/\omega_f},\quad \omega_f\approx\frac{\omega_{res}}{3}$$

El polo en \( \omega_f \) añade \( -20 \) dB/dec para \( \omega>\omega_f \), reduciendo la ganancia en la resonancia.

### Resumen del procedimiento loop-shaping

<div class="cfig"><img src="../figuras/loop-shaping-flujo.png" alt="Flujo del procedimiento de loop-shaping: de las especificaciones a la curva objetivo, al controlador, su simplificación, filtro HF y verificación final"><div class="cap">Se parte de las especificaciones (ancho de banda, márgenes), se construye la \(L_{obj}(j\omega)\) que las cumple y se despeja el controlador dividiendo por la planta. Después se simplifica \(C(s)\), se añade filtrado de alta frecuencia si hace falta y se verifica que \(L(s)=C(s)G(s)\) exacto mantiene los márgenes.</div></div>

## Cuándo y por qué se usa

Para diseñar por loop-shaping, leer márgenes de estabilidad y entender el filtrado (qué
frecuencias pasan o se atenúan). Es el lenguaje del análisis de impedancia. La escala logarítmica
hace que multiplicar bloques equivalga a sumar curvas, lo que permite construir el Bode de
sistemas complejos de cabeza en segundos.

## Errores comunes

- Confundir frecuencia en rad/s con Hz al leer la gráfica (factor \( 2\pi \)).
- Cruce con pendiente \( -40 \) dB/dec → margen de fase pobre (cerca de inestable, PM \( <20° \)).
- Ignorar el retardo digital: diseñar con PM=45° sin contabilizar \( 1.5\,T_s \) lleva a oscilaciones.
- Confundir la antirresonancia (caída profunda en \( f_{ar} \)) con la resonancia (pico en \( f_{res} \)).
- No distinguir cero RHP de cero LHP: mismo módulo, fase opuesta → el RHP consume margen irrecuperablemente.

## Conceptos relacionados

- [[funcion-transferencia]] · [[margenes-estabilidad]] · [[loop-shaping]] · [[respuesta-frecuencia-ss]]
- [[filtro-lcl]] · [[antiresonancia]] · [[compensador-adelanto-atraso]] · [[transformada-laplace]]

## Referencias

- Ogata, *Ingeniería de Control Moderna*, Pearson.
- Franklin, Powell, Emami-Naeini, *Feedback Control of Dynamic Systems*, Pearson.
- Skogestad & Postlethwaite, *Multivariable Feedback Design*, Wiley.
- Erickson & Maksimovic, *Fundamentals of Power Electronics*, Springer (Cap. 9, cero RHP).
