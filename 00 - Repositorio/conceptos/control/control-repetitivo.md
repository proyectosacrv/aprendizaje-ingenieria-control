---
titulo: Control repetitivo
slug: control-repetitivo
categoria: control
tipo: tecnica
nivel: avanzado
proyectos: []
objetivos: [anular errores periódicos rechazando todos los armónicos de una frecuencia]
tags: [repetitivo, periodico, armonicos, modelo-interno, plug-in, thd, avanzado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-30
relacionados: [controlador-resonante, controlador-pid, discretizacion-controladores, error-regimen-permanente, fft-analisis-espectral]
referencias:
  - "Hara et al., Repetitive Control System: A New Type Servo System for Periodic Exogenous Signals, IEEE TAC 1988"
  - "Zhou, Wang, Digital Repetitive Controlled PWM Inverter, IEEE TIE 2003"
---

## Definición
Controlador basado en el **principio del modelo interno** para señales **periódicas**: incorpora un
generador de periodo \( T \) (un retardo realimentado) que da ganancia infinita a la fundamental y
**todos sus armónicos** a la vez, anulando el error periódico en régimen permanente.

## Fundamento teórico
El modelo interno de una señal periódica de periodo \( T \) es el generador
$$ G_{rc}(s)=\frac{e^{-sT}}{1-e^{-sT}} $$
cuyos polos están en \( s=j\,k\,\frac{2\pi}{T} \) (la fundamental \( \omega_0=2\pi/T \) y **todos**
los armónicos \( k\omega_0 \)) → ganancia infinita en cada uno. Equivale a infinitos
[[controlador-resonante|resonantes]] en paralelo con un solo retardo. En **discreto** con \( N=T/T_s \)
muestras por periodo:
$$ C_{rc}(z)=\frac{z^{-N}}{1-Q(z)\,z^{-N}}\,k_r\,z^{m}\,F(z) $$
- \( Q(z) \): filtro (ganancia \( <1 \) o pasa-bajos) que **sacrifica precisión por robustez** (sin
  él, errores de modelo a alta frecuencia desestabilizan).
- \( z^{m} \): **avance** que compensa el retardo de la planta.
- \( F(z) \): filtro de fase/estabilización; \( k_r \): ganancia de aprendizaje.

Se implementa casi siempre como **plug-in**: se añade en paralelo a un controlador realimentado
existente (PI/PR), que estabiliza y da respuesta rápida, mientras el repetitivo limpia los armónicos
periódicos ciclo a ciclo. Coste: la convergencia tarda **varios periodos** y reacciona lento a
perturbaciones no periódicas.

<div class="cfig"><img src="figuras/control-repetitivo-peine.png" alt="respuesta en magnitud del modelo interno periodico con picos en los armonicos"><div class="cap">Magnitud del modelo interno $e^{-sT}/(1-e^{-sT})$: un peine de resonancias con ganancia alta en la fundamental y en TODOS sus armónicos a la vez, con un solo retardo realimentado. Equivale a infinitos resonantes en paralelo, lo que anula el error periódico ciclo a ciclo.</div></div>

## 1 — Por qué \( 1/(1-e^{-sT}) \) rechaza la fundamental y todos sus armónicos
**Paso 1 — el principio del modelo interno.** Para anular en régimen permanente el error frente a una señal, el lazo debe contener un **generador interno** de esa señal: un bloque cuyos polos coincidan con los modos de la perturbación. En términos de control, ganancia infinita a esas frecuencias hace que el error a ellas tienda a cero (cualquier error las excitaría sin límite, lo que el lazo no permite en equilibrio). Para una constante, ese generador es el integrador \( 1/s \); para una senoide \( \omega_0 \), el resonante \( s/(s^2+\omega_0^2) \). ¿Y para una señal **periódica** cualquiera de periodo \( T \)?

**Paso 2 — el generador de periodo \( T \).** Una señal periódica de periodo \( T \) cumple \( x(t)=x(t-T) \). El bloque que "memoriza un periodo y lo realimenta" es un retardo \( e^{-sT} \) en lazo positivo:

$$ y(t)=u(t)+y(t-T)\quad\Longrightarrow\quad Y(s)=U(s)+e^{-sT}Y(s)\quad\Longrightarrow\quad \frac{Y(s)}{U(s)}=\frac{1}{1-e^{-sT}} $$

(la variante \( e^{-sT}/(1-e^{-sT}) \) solo desplaza la salida un periodo; los polos son los mismos).

**Paso 3 — localizar los polos.** Los polos están donde el denominador se anula:

$$ 1-e^{-sT}=0 \;\Rightarrow\; e^{-sT}=1 \;\Rightarrow\; -sT=j\,2\pi k,\quad k\in\mathbb{Z} $$

$$ \boxed{\;s=j\,k\,\frac{2\pi}{T}=j\,k\,\omega_0,\quad k=0,\pm1,\pm2,\dots\;} $$

Hay un polo en \( k=0 \) (la componente DC), uno en la fundamental \( \omega_0=2\pi/T \) y uno en **cada** armónico \( k\omega_0 \), todos sobre el eje imaginario.

**Paso 4 — ganancia infinita en cada armónico.** En \( s=jk\omega_0 \) el denominador \( 1-e^{-jk\omega_0 T}=1-e^{-j2\pi k}=1-1=0 \), de modo que \( |G_{rc}(jk\omega_0)|\to\infty \). El Bode es un **peine** de resonancias: un solo retardo realimentado coloca ganancia infinita en infinitas frecuencias equiespaciadas. Por eso un único bloque equivale a infinitos [[controlador-resonante|resonantes]] en paralelo (uno por armónico) pero con coste de cómputo de una sola memoria de \( N=T/T_s \) muestras.

**Paso 5 — por qué eso anula el error periódico.** Una perturbación periódica de periodo \( T \) tiene su espectro **exactamente** en \( \{k\omega_0\} \) (serie de Fourier). El modelo interno tiene ganancia infinita justo en esas frecuencias, así que el error en régimen permanente en cada armónico se anula. La contrapartida: como la corrección se construye memorizando el ciclo anterior, la convergencia tarda **varios periodos** y el bloque no ayuda frente a perturbaciones no periódicas (cuyo espectro no cae en el peine). El filtro \( Q(z)<1 \) baja la ganancia en alta frecuencia para robustez, a costa de no anular del todo los armónicos altos.

## 3 — Principio del modelo interno (IMP)

**El principio del modelo interno (Internal Model Principle, IMP).** Francis y Wonham (1975) formalizaron la condición necesaria y suficiente para rechazo/seguimiento asintótico: el lazo de control debe contener un **modelo generador** de la señal a rechazar o seguir. Sin ese modelo en el lazo, el error en régimen permanente ante esa señal es inevitablemente no nulo.

- Para seguir/rechazar una **constante**: el modelo generador es un integrador \( 1/s \) (polo en \( s=0 \)).
- Para seguir/rechazar una **senoide de frecuencia \( \omega_0 \)**: el modelo es un resonante \( \omega_0^2/(s^2+\omega_0^2) \) (polos en \( \pm j\omega_0 \)).
- Para seguir/rechazar una **señal periódica de período \( T \)**: el modelo es \( e^{sT}/(1-e^{sT}) \) — un retardo más uno.

En discreta, con \( N = T/T_s \) muestras por período:

$$ G_{IMP}(z) = \frac{z^N}{1 - z^N} $$

Este bloque tiene polos en todas las raíces de la unidad de orden \( N \), es decir, en \( z = e^{j2\pi k/N} \) para \( k = 0, 1, \ldots, N-1 \): exactamente la fundamental y todos sus armónicos hasta \( f_s/2 \).

**Por qué un solo retardo reemplaza infinitos resonantes.** Un controlador resonante para el armónico \( k \) requiere un par de polos en \( \pm jk\omega_0 \). Para eliminar los armónicos 1°, 3°, 5°, 7°, 9°... se necesitarían 5 resonantes en paralelo (10 polos adicionales). El modelo interno periódico logra lo mismo con \( N \) celdas de memoria (una por muestra del período), sin necesidad de sintonizar cada resonante individualmente.

## 4 — Estructura del controlador repetitivo

**La estructura completa en z.** El controlador repetitivo plug-in en discreto es:

$$ C_{rep}(z) = \frac{z^N}{1 - Q(z)\,z^N} \cdot C_f(z) $$

donde los bloques tienen funciones específicas:

- **\( z^N \):** retardo de un período en el numerador — "aprende" del ciclo anterior.
- **\( Q(z) \):** filtro de estabilización. Debe satisfacer \( |Q(e^{j\omega T_s})| \leq 1 \) para todos \( \omega \). Sin \( Q \), los errores de modelo a alta frecuencia desestabilizan el lazo. La penalización: \( Q < 1 \) sacrifica ganancia en alta frecuencia a cambio de robustez.
- **\( C_f(z) \):** compensador de fase para garantizar margen de estabilidad positivo a la frecuencia de cruce de cada armónico. Típicamente \( C_f(z) = K_r z^m \): una ganancia más un anticipo de fase de \( m \) muestras.

**Condición de estabilidad.** El lazo cerrado con el repetitivo plug-in es estable si y solo si:

$$ \|Q(z) - P_{cl}(z)\,C_f(z)\|_\infty < 1 $$

donde \( P_{cl}(z) \) es la planta con el lazo base (PI) ya cerrado. Esta es la condición de pequeña ganancia aplicada al lazo de "aprendizaje": el residuo \( Q - P_{cl}C_f \) debe tener ganancia menor que 1 en todas las frecuencias.

## 5 — Diseño de \( Q(z) \) y \( C_f(z) \)

**Filtro \( Q(z) \).** El diseño clásico usa un filtro FIR de 3 puntos:

$$ Q(z) = 0{,}25\,z + 0{,}5 + 0{,}25\,z^{-1} $$

Este filtro tiene ganancia unitaria en DC (\( Q(1) = 1 \)), suaviza la respuesta en alta frecuencia (atenúa por encima de \( f_s/4 \)) y es de fase lineal (no introduce retardo de grupo). La penalización: a las frecuencias armónicas altas, \( Q < 1 \) reduce la ganancia del repetitivo y el error en esos armónicos no se anula completamente.

**Compensador \( C_f(z) = K_r z^m \).** El anticipo de \( m \) muestras compensa el retardo de la planta en el lazo abierto:
- Retardo total del lazo (computación + PWM + filtro): \( m_{delay} \) muestras.
- Se elige \( m \approx m_{delay} \) para que la fase total en cada frecuencia armónica sea mayor que 0°.
- Verificar que la condición de pequeña ganancia se cumple gráficamente: trazar \( |Q(e^{j\omega T_s}) - P_{cl}(e^{j\omega T_s})C_f(e^{j\omega T_s})| \) y comprobar que es menor que 1 en todo el rango de frecuencias relevante.

**Ganancia \( K_r \).** Determina la velocidad de convergencia del aprendizaje:
- \( K_r \) grande → converge más rápido (menos períodos para reducir el THD) pero reduce el margen de estabilidad.
- \( K_r < 1 \) es el criterio conservador que garantiza robustez ante incertidumbre de la planta.
- Valor típico: \( K_r = 0{,}5\text{–}1{,}5 \).

## 6 — Control repetitivo para inversores

**Objetivo.** El inversor conectado a red inyecta una corriente con armónicos de orden 3°, 5°, 7°, 9°,... debidos a la no linealidad de la carga o a la conmutación. El controlador PI solo puede rechazar la fundamental (armónico 1°). El repetitivo elimina todos los armónicos de 50 Hz simultáneamente.

**Reducción de THD.** Resultado típico en simulación con carga no lineal (rectificador diodo):
- Solo PI: THD ≈ 8% (con ganancia de cruce a 750 Hz, armónicos 5°, 7° mal atenuados).
- PI + repetitivo: THD < 2% tras 3–5 períodos de convergencia.

**Período y número de muestras.** Con \( f_0 = 50\,\text{Hz} \) y frecuencia de muestreo \( f_s = 10\,\text{kHz} \):

$$ N = \frac{T}{T_s} = \frac{1/50}{1/10000} = 200 \text{ muestras} $$

El buffer de memoria del repetitivo ocupa 200 palabras (floats de 32 bits = 800 bytes): coste computacional muy bajo comparado con el beneficio en THD.

**Combinación PI + repetitivo.** El PI gestiona la dinámica rápida y las perturbaciones no periódicas (transitorios de carga, cambios de referencia). El repetitivo corrige el error periódico residual que el PI no puede anular por falta de ganancia en alta frecuencia. La arquitectura plug-in garantiza que el repetitivo no afecta a la estabilidad del lazo base: si el repetitivo falla (p. ej. por desintonización), el PI sigue funcionando.

**Limitación: frecuencia variable.** Si la frecuencia de red varía (\( f_0 \neq 50\,\text{Hz} \)), \( N = f_s/f_0 \) deja de ser entero y el buffer circular no se sincroniza con el período de red. Solución: \( N \) fraccionario con interpolación, o adaptar \( N \) en tiempo real con la frecuencia estimada por el PLL.

<div class="cfig"><img src="../figuras/control-repetitivo-analisis.png" alt="cuatro paneles: espectro antes-despues, convergencia THD, Bode controlador repetitivo, forma de onda PI vs PI+rep"><div class="cap">(a) Espectro de corriente antes y después del repetitivo: reducción del THD de ~24% a ~2%. (b) Convergencia del THD ciclo a ciclo. (c) Diagrama de Bode del controlador: peine de ganancias en armónicos de 50 Hz. (d) Forma de onda de corriente: solo PI vs PI+repetitivo.</div></div>

## Cuándo y por qué se usa
Cuando la perturbación/​referencia es periódica y rica en armónicos: inversores de tensión (UPS/CVCF)
con carga no lineal, filtros activos, rectificadores con rizado periódico. Da muy bajo THD con poco
coste de cómputo frente a apilar muchos resonantes.

## Procedimiento de diseño (genérico)
1. Estabiliza primero el lazo con un controlador realimentado (PI/PR).
2. Añade el repetitivo en plug-in: fija \( N=T/T_s \) (entero; ojo si \( f_0 \) varía).
3. Diseña \( Q(z) \) (pasa-bajos) para robustez a alta frecuencia.
4. Ajusta el avance \( z^{m} \) (compensa retardo de planta) y la ganancia \( k_r \).
5. Verifica estabilidad (criterio de pequeña ganancia sobre \( Q-k_r z^{m}F\hat G \)) y THD resultante.

## Ejemplo de código
```python
class Repetitive:                        # plug-in discreto
    def __init__(self, N, kr, Q=0.95): self.buf=[0.0]*N; self.kr=kr; self.Q=Q
    def step(self, err):
        u = self.Q*self.buf[0] + self.kr*err     # memoria de 1 periodo
        self.buf = self.buf[1:] + [u]
        return self.buf[0]
```

## Parámetros y valores típicos
\( Q\approx0.95\text{–}0.99 \) o pasa-bajos con corte < \( f_s/4 \). \( k_r \) 0.5–2. Convergencia
en 3–10 periodos. THD < 1–3 % alcanzable.

## Errores comunes
- \( N \) no entero o frecuencia de red variable → el repetitivo se desintoniza (usar \( N \)
  fraccional/adaptativo).
- Sin filtro \( Q \) → inestabilidad por errores de modelo a alta frecuencia.
- Usarlo solo (sin lazo estabilizante) o esperar respuesta rápida a transitorios no periódicos.

## Conceptos relacionados
- [[controlador-resonante]] · [[controlador-pid]] · [[discretizacion-controladores]] · [[error-regimen-permanente]] · [[fft-analisis-espectral]]

## Referencias
- Hara et al., *Repetitive Control System*, IEEE TAC 1988.
- Zhou, Wang, *Digital Repetitive Controlled PWM Inverter*, IEEE TIE 2003.
