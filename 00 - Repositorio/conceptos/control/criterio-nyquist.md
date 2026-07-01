---
titulo: Criterio de estabilidad de Nyquist
slug: criterio-nyquist
categoria: control
tipo: metodo
nivel: basico
proyectos: []
objetivos: [determinar la estabilidad en lazo cerrado a partir de la ganancia de lazo]
tags: [nyquist, estabilidad, lazo-cerrado, rodeos, basico, control, principio-argumento, integrador]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-07-01
relacionados: [margenes-estabilidad, diagrama-bode, estabilidad-bibo, polos-ceros, impedancia-salida-estabilidad, routh-hurwitz]
referencias:
  - "Ogata, Ingeniería de Control Moderna, Pearson"
  - "Aström, Murray, Feedback Systems, Princeton 2008"
---

## Definición
Criterio gráfico que decide la **estabilidad en lazo cerrado** observando cómo la traza de la
ganancia de lazo \( L(j\omega) \) rodea al **punto crítico \( -1 \)**, sin calcular las raíces
del polinomio característico.

## Fundamento teórico
Se apoya en el **principio del argumento**. Para el lazo \( 1+L(s)=0 \), recorriendo el contorno
de Nyquist (todo el eje \( j\omega \) cerrado por la derecha), el número de rodeos en sentido
horario \( N \) de \( L(j\omega) \) alrededor de \( -1 \) cumple:
$$ Z = N + P $$
- \( Z \): ceros de \( 1+L \) en el semiplano derecho = **polos inestables del lazo cerrado**.
- \( P \): polos inestables de \( L \) (lazo abierto).
- Estable \( \iff Z=0 \): se necesitan \( N=-P \) rodeos **antihorarios** de \( -1 \).

Si \( L \) es estable en lazo abierto (\( P=0 \)), basta con que **no se rodee** \( -1 \). La
distancia mínima de la traza a \( -1 \) define el [[margenes-estabilidad|margen de módulo]].

<div class="cfig"><img src="figuras/criterio-nyquist-plot.png" alt="diagrama de Nyquist y el punto -1"><div class="cap">Diagrama de Nyquist de la ganancia de lazo L(jω): aquí la traza no rodea el punto crítico −1, así que (con L estable en lazo abierto) el lazo cerrado es estable. El cruce con el eje real negativo da el margen de ganancia.</div></div>

## 1 — De dónde sale \( Z = N + P \) (principio del argumento)
**Paso 1 — el polinomio característico como una función.** El lazo cerrado es estable si \( 1+L(s)=0 \) no tiene raíces en el semiplano derecho (SPD). Escribe la ganancia de lazo como cociente de polinomios \( L(s)=B(s)/A(s) \). Entonces:

$$ F(s)\equiv 1+L(s)=\frac{A(s)+B(s)}{A(s)} $$

Los **polos** de \( F \) son las raíces de \( A(s) \) = polos de lazo abierto. Los **ceros** de \( F \) son las raíces de \( A+B \) = polos de lazo cerrado. Queremos contar cuántos ceros de \( F \) caen en el SPD: ese número es \( Z \).

**Paso 2 — el principio del argumento.** Sea \( F(s) \) meromorfa y \( \Gamma \) un contorno cerrado que no pasa por ningún polo ni cero. El teorema de Cauchy del argumento dice que, al recorrer \( \Gamma \) una vez en sentido horario, la imagen \( F(\Gamma) \) rodea el origen un número neto de veces igual a (ceros − polos) encerrados:

$$ N_0 = Z_{\Gamma} - P_{\Gamma} $$

La idea: cada cero \( z_k \) aporta un factor \( (s-z_k) \), cuyo argumento gira \( +2\pi \) si \( z_k \) queda dentro de \( \Gamma \) (horario), y cada polo aporta \( -2\pi \). Sumando todas las contribuciones queda el conteo neto.

**Paso 3 — el contorno de Nyquist.** Elige \( \Gamma \) = todo el eje \( j\omega \) de \( -\infty \) a \( +\infty \), cerrado por un semicírculo de radio infinito que envuelve **todo el SPD**, recorrido en sentido horario. Así \( Z_\Gamma=Z \) (ceros de \( F \) en SPD = polos inestables de lazo cerrado) y \( P_\Gamma=P \) (polos de \( F \) en SPD = polos inestables de lazo abierto). El principio del argumento da \( N_0=Z-P \).

**Paso 4 — trasladar el conteo del origen a \( -1 \).** En vez de dibujar \( F=1+L \) y contar rodeos del origen, se dibuja directamente \( L(j\omega) \): como \( F=1+L \), un rodeo de \( F \) al origen es exactamente un rodeo de \( L \) al punto \( -1 \) (restar 1 traslada el origen a \( -1 \)). Llamando \( N \) a los rodeos horarios de \( L(j\omega) \) alrededor de \( -1 \), entonces \( N=N_0 \) y:

$$ \boxed{\;Z = N + P\;} $$

**Paso 5 — el caso estable.** Lazo cerrado estable \( \iff Z=0 \iff N=-P \): hacen falta \( P \) rodeos **antihorarios** de \( -1 \). Si además el lazo abierto es estable (\( P=0 \)) la condición se reduce a \( N=0 \): **la traza no debe rodear \( -1 \)**. Por eso un único punto \( -1 \) decide todo: encierra la información de cuántos polos inestables se generan al cerrar el lazo. Conecta con [[estabilidad-bibo]] (un solo polo en SPD basta para inestabilidad).

## 2 — El principio del argumento y el conteo de encirclements

El resultado \( Z=N+P \) surge del principio del argumento, que merece desarrollarse con más detalle para entender por qué "contar rodeos" es equivalente a "contar raíces".

**Idea geométrica del argumento.**
Si \( s \) recorre un contorno \( \Gamma \) una vez en sentido horario, el vector \( (s-z_k) \) — que apunta desde el cero \( z_k \) al punto \( s \) — gira \( +2\pi \) (un rodeo completo, sentido horario) si \( z_k \) está dentro de \( \Gamma \), y no da un rodeo completo si \( z_k \) está fuera. Lo mismo para los polos pero con signo contrario (el vector \( 1/(s-p_k) \) gira en sentido contrario).

**Conteo algebraico del argumento total.**
El cambio total del argumento de \( F(s) \) al recorrer \( \Gamma \) es:
$$ \Delta\arg F = \sum_k \Delta\arg(s-z_k) - \sum_k \Delta\arg(s-p_k) = 2\pi(Z_\Gamma - P_\Gamma) $$
El número de rodeos del origen de \( F(\Gamma) \) es \( N_0 = \Delta\arg F / (2\pi) = Z_\Gamma - P_\Gamma \).

**De \( F(s) \) a \( L(j\omega) \) — el traslado.**
En lugar de trazar \( F(j\omega)=1+L(j\omega) \) y contar rodeos del origen, se traza \( L(j\omega) \) y se cuenta rodeos del punto \( -1+j0 \). Son equivalentes porque \( F = 1+L \) es simplemente \( L \) trasladado 1 unidad a la derecha.

**El diagrama completo de Nyquist.**
El eje imaginario recorre \( \omega:\,-\infty\to+\infty \). Para \( \omega<0 \), la traza es el conjugado complejo de la traza para \( \omega>0 \) (espejo respecto al eje real), porque \( L(-j\omega)=\overline{L(j\omega)} \) para sistemas reales. En la práctica se dibuja solo \( \omega>0 \) y se añade el espejo. El semicírculo de radio infinito queda mapeado a un punto (si el grado del denominador de \( L \) supera al del numerador) o a un círculo.

## 3 — El contorno de Nyquist y el caso del integrador

**Qué hacer cuando \( L(s) \) tiene un polo en el eje imaginario.**
Si \( L(s) \) tiene un polo en \( s=0 \) (integrador) o en \( s=j\omega_0 \) (polo oscilatorio), el contorno de Nyquist no puede pasar por ese punto. Se desvía con un **semicírculo de radio \( \varepsilon\to 0 \)** a la derecha del polo, para no excluirlo (se queda en el contorno) ni incluirlo (no está en el SPD).

**El integrador \( 1/s \) produce un arco de radio \(\infty\).**
Para \( s=\varepsilon e^{j\theta} \) con \( \varepsilon\to 0 \) y \( \theta:-\pi/2\to+\pi/2 \) (semicírculo hacia la derecha):

$$ L(s)\big|_{s=\varepsilon e^{j\theta}} \approx \frac{K}{\varepsilon e^{j\theta}} \to \infty\cdot e^{-j\theta} $$

Al recorrer el semicírculo \( \theta \) de \( -\pi/2 \) a \( +\pi/2 \), el argumento de \( L \) gira de \( +\pi/2 \) a \( -\pi/2 \): la traza de Nyquist barre un arco de radio infinito de \( +j\infty \) a \( -j\infty \) en sentido horario. Este arco cierra la curva de Nyquist y es parte esencial del contorno; ignorarlo lleva a un conteo incorrecto de rodeos.

**Regla práctica para el integrador:**
Cuando \( L(s)=K/(s\cdot Q(s)) \) con \( Q(0)\neq 0 \), el arco del integrador barre \( 180° \) en la dirección contraria al eje imaginario positivo. Si hay dos integradores (\( 1/s^2 \)), el arco barre \( 360° \). Esto equivale a "despegar" la curva de Nyquist del origen y añadir el rodeo correspondiente.

**Ejemplo — lazo de corriente con PI.**
\( L(s) = K_i(1+s/\omega_z)/(s\cdot(1+s/\omega_p)) \). El integrador produce un arco de \( +j\infty \) (ω→0⁺) a \( -j\infty \) (ω→0⁺ desde el espejo). A frecuencias altas la traza se enrolla en el origen. Para verificar estabilidad hay que incluir el arco del integrador en el conteo de rodeos.

## 4 — Nyquist para sistemas inestables en lazo abierto

Este es el caso donde el criterio de Nyquist se vuelve imprescindible: si \( L(s) \) tiene polos en el SPD (\( P>0 \)), la condición simplificada "no rodear −1" **no aplica**.

**Condición general.**
Para lazo cerrado estable, \( Z=N+P=0 \;\Rightarrow\; N=-P \). Se necesitan exactamente \( P \) rodeos **antihorarios** de \( -1 \) en el diagrama de Nyquist de \( L(j\omega) \).

**Ejemplo — \( L(s) = K/(s-1) \).**
La planta tiene un polo en \( s=+1 \) (inestable), así \( P=1 \). Para lazo cerrado estable necesitamos \( N=-1 \): un rodeo antihorario de \( -1 \).

Evaluando en el eje imaginario:
$$ L(j\omega) = \frac{K}{j\omega-1} = \frac{K(-1-j\omega)}{1+\omega^2} $$
- En \( \omega=0 \): \( L(0)=-K \) (real negativo).
- En \( \omega\to\infty \): \( L\to 0 \).
- El arco del polo en \( s=+1 \): por convención se excluye del SPD rodeando con \( \varepsilon \to 0 \) por la **izquierda** (dentro del contorno). Esto añade un arco de radio finito.

Para \( K>1 \): \( L(0)=-K < -1 \) → la traza cruza el eje real a la izquierda de \( -1 \), rodeándolo una vez en sentido antihorario → \( N=-1=-P \) → \( Z=0 \) → **estable**. Para \( K<1 \): \( L(0)=-K>-1 \) → no rodea \( -1 \) → \( N=0 \) → \( Z=P=1 \) → inestable. Esta planta **solo se estabiliza con realimentación** (y con ganancia suficiente).

**Generalización.**
Sistemas con \( P \) polos inestables en lazo abierto (como los que aparecen en el análisis de estabilidad por impedancia cuando la fuente o la carga tiene dinámica inestable) requieren el criterio de Nyquist generalizado. No es posible usar Bode ni Routh en estos casos sin modificaciones.

## 5 — Nyquist vs Bode: cuándo usar cada uno

Ambos métodos visualizan la ganancia de lazo y determinan estabilidad, pero con supuestos y capacidades diferentes.

**Bode: más intuitivo, válido solo para sistemas de fase mínima y lazo abierto estable.**
El diagrama de Bode muestra \( |L(j\omega)| \) y \( \angle L(j\omega) \) por separado en escala logarítmica. El margen de fase y el margen de ganancia se leen directamente de los cruces. Sin embargo:
- Asume \( P=0 \): no funciona si \( L \) tiene polos en el SPD.
- En sistemas de **fase no mínima** (ceros en el SPD o retardos grandes), la correspondencia entre márgenes de Bode y estabilidad se rompe: puede haber sistemas con PM>0 que sean inestables (sistemas condicionalmente estables).
- Con retardos grandes: el diagrama de Bode se extiende pero el criterio de PM solo es válido si no hay rodeos del \( -1 \) a frecuencias más altas.

**Nyquist: más general, funciona siempre.**
- Válido para cualquier \( P \) (lazo abierto con polos en SPD).
- Correcto para fase no mínima, retardos arbitrarios, sistemas condicionalmente estables.
- El conteo de rodeos de \( -1 \) captura toda la información sin restricciones.
- Más difícil de leer en sistemas de orden alto: la curva puede ser complicada.

**Recomendación práctica.**
| Situación | Herramienta |
|---|---|
| Lazo estable, planta conocida, sin retardos grandes | Bode (más rápido) |
| Retardos significativos o \( e^{-sT} \) | Nyquist (o PM desde Bode con retardo incluido) |
| Planta inestable en lazo abierto (\( P>0 \)) | Nyquist (obligatorio) |
| Fase no mínima o sistema condicionalmente estable | Nyquist |
| Estabilidad de impedancias en convertidores | [[criterio-nyquist|Nyquist generalizado]] con \( Z_o/Z_g \) |

**Para convertidores con impedancia no mínima.**
En el criterio de estabilidad por impedancia (ver [[impedancia-salida-estabilidad]]), la ganancia de lazo es \( L_{imp}=Z_{out}/Z_{in} \). Si la impedancia de salida de la fuente tiene ceros en el SPD (lo que ocurre con algunos convertidores grid-forming con control de tensión inestabilizado), el diagrama de Bode da conclusiones erróneas. El criterio de Nyquist aplicado directamente sobre \( L_{imp}(j\omega) \) cuenta correctamente los rodeos y determina el número de polos inestables del sistema interconectado.

<div class="cfig"><img src="figuras/criterio-nyquist-analisis.png" alt="aplicaciones del criterio de Nyquist"><div class="cap">Cuatro situaciones del criterio de Nyquist. (a) $L=5/[(s+1)(s+2)]$: traza que no rodea $-1$; los márgenes GM y PM son directamente legibles. (b) Sistema condicionalmente estable: rodear $-1$ depende de $K$, ilustrando la limitación del criterio de Bode. (c) $L=4/[(s-2)(s+1)]$, $P=1$: el rodeo antihorario de $-1$ garantiza lazo cerrado estable ($N=-1=-P$, $Z=0$). (d) Ilustración del principio del argumento: $F(\Gamma)$ rodea el origen exactamente $Z-P$ veces.</div></div>

## Cuándo y por qué se usa
Cuando hay retardos, polos en lazo abierto inestables o sistemas donde Routh no aplica bien. Es
la base del **criterio de estabilidad por impedancia** (el cociente \( Z_o/Z_g \) se trata como
una ganancia de lazo y se le aplica Nyquist).

## Procedimiento (genérico)
1. Obtén \( L(j\omega) \) y cuenta \( P \) (polos de \( L \) en SPD).
2. Traza el diagrama polar de \( L(j\omega) \) para \( \omega:-\infty\to\infty \).
3. Cuenta los rodeos netos \( N \) alrededor de \( -1 \).
4. Aplica \( Z=N+P \); estable si \( Z=0 \).

## Ejemplo de aplicación real
**Problema:** Lazo de corriente con planta \( G_i(s)=1/(Ls) \), \( L=2\,\text{mH} \), PI y retardo de cómputo \( T_d=150\,\mu\text{s} \). Verificar estabilidad por Nyquist y cuantificar el margen.

La ganancia de lazo es \( L(j\omega) \) con contribuciones: integrador \( -90° \), PI (cero muy por debajo de \( \omega_c \), aporte \( \approx0° \)) y retardo \( -\omega_c T_d\times(180/\pi) \). A \( \omega_c=6283\,\text{rad/s} \): desfase del retardo \( \approx-54° \), fase total \( \approx-144° \), margen de fase \( 36° \). Como \( P=0 \) (lazo abierto estable), basta verificar que la traza no rodea \( -1 \). La distancia mínima da \( M_s=1/\sin(36°)\approx1.7<2 \): cumple la especificación. Para subir el margen a 45° bajar \( \omega_c \) a \( \approx750\,\text{Hz} \) (reduce el desfase del retardo a \( -40° \)).

## Ejemplo de código
```python
import control as ct, numpy as np
L = ct.tf([10], [1, 3, 3, 1])
ct.nyquist_plot(L)                 # ¿rodea -1?
print(ct.margin(L))                # (GM, PM, wcg, wcp): lectura cuantitativa

# Para contar P (polos de L en SPD):
poles_L = ct.poles(L)
P = sum(1 for p in poles_L if p.real > 0)
print(f"P={P} polos inestables en lazo abierto")
```

## Parámetros y valores típicos
Objetivo práctico: dejar \( -1 \) holgadamente fuera de la traza (margen de módulo \( 1/M_s \)
con \( M_s<2 \)). El cruce con el eje real negativo da el margen de ganancia.

## Errores comunes
- Olvidar contar \( P \): con polos inestables en lazo abierto, "no rodear −1" NO implica estable.
- Ignorar el rizo cerca de \( -1 \) por integradores/retardos (semicírculos en el infinito).
- Confundir el criterio simplificado (válido si \( P=0 \)) con el general.
- Usar Bode para concluir estabilidad en sistemas de fase no mínima o condicionalmente estables.

## Conceptos relacionados
- [[margenes-estabilidad]] · [[diagrama-bode]] · [[estabilidad-bibo]] · [[impedancia-salida-estabilidad]] · [[routh-hurwitz]]

## Referencias
- Ogata, *Ingeniería de Control Moderna*.
- Aström, Murray, *Feedback Systems*, 2008.
