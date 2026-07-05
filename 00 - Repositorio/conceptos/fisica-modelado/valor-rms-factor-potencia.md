---
titulo: Valor eficaz (RMS), valor medio y factor de potencia
slug: valor-rms-factor-potencia
categoria: fisica-modelado
tipo: concepto
nivel: basico
proyectos: []
objetivos: [manejar magnitudes AC y el convenio pico/RMS del marco dq]
tags: [rms, valor-eficaz, factor-potencia, potencia, basico]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-06-30
relacionados: [potencia-ac-fasores, sistema-trifasico, potencia-instantanea-dq, calidad-potencia, series-fourier]
referencias:
  - "Mohan, Undeland & Robbins, Power Electronics"
---

## Definición
El **valor eficaz (RMS)** de una señal es el valor de continua que disiparía la misma potencia en una
resistencia. El **factor de potencia (FP)** mide qué fracción de la potencia aparente se convierte en
potencia activa útil.

## Fundamento teórico
El valor eficaz y el medio de una señal periódica:
$$ X_{rms} = \sqrt{\frac{1}{T}\int_0^T x^2(t)\,dt}, \qquad X_{med} = \frac{1}{T}\int_0^T x(t)\,dt $$
Para una senoide pura, \( X_{rms} = X_{pico}/\sqrt{2} \) y \( X_{med}=0 \). Las potencias en AC
monofásica:
$$ S = V_{rms} I_{rms}, \quad P = V_{rms} I_{rms}\cos\varphi, \quad Q = V_{rms} I_{rms}\sin\varphi $$
$$ \mathrm{FP} = \frac{P}{S} = \cos\varphi \ \text{(senoidal)} $$
En trifásico equilibrado \( P = \sqrt{3}\,V_{LL} I_L \cos\varphi \). **Convenio del proyecto:** se
trabaja con **amplitud de pico de fase**, \( V_0 = V_{LL}\sqrt{2/3} \), y por eso la potencia
trifásica instantánea en dq lleva el factor \( \tfrac32 \): \( P = \tfrac32(v_d i_d + v_q i_q) \).

<div class="cfig"><img src="figuras/valor-rms-factor-potencia-rms.png" alt="valor RMS de una senoide"><div class="cap">El valor eficaz (RMS) de una senoide es su pico dividido por √2: la continua que disiparía la misma potencia en una resistencia. Las magnitudes nominales (400 V, etc.) son RMS.</div></div>

## 1 — Por qué el RMS de una senoide es \( X_{pico}/\sqrt2 \)
**Paso 1 — partir de la definición.** El RMS es la raíz de la media del cuadrado. Para \( x(t)=X_{pico}\sin(\omega t) \) con periodo \( T=2\pi/\omega \):

$$ X_{rms}^2=\frac{1}{T}\int_0^T X_{pico}^2\sin^2(\omega t)\,dt=\frac{X_{pico}^2}{T}\int_0^T\sin^2(\omega t)\,dt $$

**Paso 2 — linealizar el seno al cuadrado.** Con la identidad \( \sin^2\theta=\tfrac12\big(1-\cos2\theta\big) \):

$$ \int_0^T\sin^2(\omega t)\,dt=\int_0^T\frac{1-\cos(2\omega t)}{2}\,dt=\underbrace{\frac{T}{2}}_{\text{término }1/2}-\underbrace{\frac{1}{2}\int_0^T\cos(2\omega t)\,dt}_{=\,0} $$

El segundo integrando es un coseno de frecuencia \( 2\omega \): sobre un periodo completo \( T \) caben exactamente dos ciclos suyos, así que su integral se anula (el área positiva cancela la negativa). Queda solo \( T/2 \).

**Paso 3 — sustituir y simplificar.** Reemplazando la integral por \( T/2 \):

$$ X_{rms}^2=\frac{X_{pico}^2}{T}\cdot\frac{T}{2}=\frac{X_{pico}^2}{2}\quad\Longrightarrow\quad \boxed{\;X_{rms}=\frac{X_{pico}}{\sqrt2}\;} $$

La \( T \) del prefactor cancela la \( T/2 \) de la integral y desaparece el periodo: el resultado vale para **cualquier** frecuencia. Numéricamente, \( X_{pico}=326{,}6 \) V de pico de fase da \( 326{,}6/\sqrt2=230{,}9 \) V RMS — la tensión nominal de fase de una red de 400 V de línea.

## 2 — Por qué \( P=V_{rms}I_{rms}\cos\varphi \)
**Paso 1 — potencia instantánea.** Con \( v(t)=V_{pico}\sin(\omega t) \) e \( i(t)=I_{pico}\sin(\omega t-\varphi) \), la potencia instantánea es el producto:

$$ p(t)=v(t)\,i(t)=V_{pico}I_{pico}\,\sin(\omega t)\sin(\omega t-\varphi) $$

**Paso 2 — producto de senos a suma.** Con \( \sin A\sin B=\tfrac12\big[\cos(A-B)-\cos(A+B)\big] \), siendo \( A=\omega t \), \( B=\omega t-\varphi \):

$$ p(t)=\frac{V_{pico}I_{pico}}{2}\Big[\underbrace{\cos\varphi}_{\text{constante}}-\underbrace{\cos(2\omega t-\varphi)}_{\text{oscila a }2\omega}\Big] $$

**Paso 3 — promediar sobre un periodo.** La potencia activa es el valor medio de \( p(t) \). El término \( \cos(2\omega t-\varphi) \) oscila a \( 2\omega \) y promedia cero (igual que en el apartado 1); solo sobrevive la constante:

$$ P=\frac{V_{pico}I_{pico}}{2}\cos\varphi $$

**Paso 4 — pasar a RMS.** Usando \( V_{pico}=\sqrt2\,V_{rms} \) e \( I_{pico}=\sqrt2\,I_{rms} \), el producto \( V_{pico}I_{pico}=2\,V_{rms}I_{rms} \) y el factor \( 2 \) cancela el \( \tfrac12 \):

$$ \boxed{\;P=V_{rms}I_{rms}\cos\varphi\;} $$

El \( \cos\varphi \) es el factor de potencia: la fracción de la potencia aparente \( S=V_{rms}I_{rms} \) que se convierte en activa. La misma cuenta en dq aparece en [[potencia-instantanea-dq]], donde el factor \( \tfrac32 \) sustituye a este \( \tfrac12 \) por sumar las tres fases con amplitud de pico.

## 3 — El RMS de señales no sinusoidales y la relación con el THD

Las señales en convertidores nunca son sinusoidales puras: contienen armónicos. El RMS total incluye la contribución de todos ellos.

**Paso 1 — descomposición de Parseval.** Una señal periódica \( i(t) \) puede escribirse como suma de Fourier: \( i(t)=\sum_{n=1}^{\infty}I_n\sin(n\omega t+\phi_n) \). Dado que los armónicos son ortogonales entre sí (integral del producto de dos diferentes = 0), el RMS total es la raíz cuadrada de la suma de los cuadrados de los RMS individuales:

$$ I_{rms}^2=\frac{1}{T}\int_0^T i^2\,dt=\sum_{n=1}^{\infty}\frac{I_n^2}{2}=I_{1,rms}^2+I_{3,rms}^2+I_{5,rms}^2+\cdots $$

**Paso 2 — definición del THD.** El THD (Total Harmonic Distortion) de la corriente se define como la relación entre el contenido armónico total (excluyendo la fundamental) y la amplitud de la fundamental:

$$ THD_I=\frac{\sqrt{I_{rms}^2-I_{1,rms}^2}}{I_{1,rms}}=\frac{I_{harm,rms}}{I_{1,rms}} $$

**Paso 3 — relación entre \( I_{rms} \) y \( THD \).** Despejando de la definición:

$$ I_{rms}=I_{1,rms}\sqrt{1+THD_I^2} $$

Para una senoide pura \( THD=0 \) y \( I_{rms}=I_{1,rms} \). Para un rectificador con \( THD_I=30\,\% \): \( I_{rms}=I_{1,rms}\sqrt{1+0.09}=1.044\,I_{1,rms} \) — solo 4.4 % más que la fundamental. Con \( THD_I=100\,\% \): \( I_{rms}=\sqrt2\,I_{1,rms} \) — el rms se multiplica por \( \sqrt2 \). El cable debe dimensionarse para el \( I_{rms} \) total, no solo para la fundamental.

**Paso 4 — valor de pico vs RMS con armónicos.** La relación \( V_{pico}/V_{rms} \) (**factor de cresta**) es \( \sqrt2 \) para senoide pura. Con armónicos puede ser mayor o menor dependiendo de cómo se sumen los picos. Por ejemplo, si los armónicos están en fase con la fundamental en el instante de pico: \( V_{pico}=V_1\sqrt2+V_3\sqrt2+\cdots>\sqrt2\,V_{rms} \). Los equipos deben tolerar el factor de cresta real del convertidor.

## 4 — El factor de potencia con armónicos: FP, DPF y factor de distorsión

El factor de potencia con armónicos es diferente al \( \cos\varphi \) de la fundamental.

**Paso 1 — potencia activa con armónicos.** Solo los armónicos de la misma frecuencia en \( v \) e \( i \) pueden intercambiar potencia activa. Si la tensión es senoidal pura \( v=V_1\sin(\omega t) \), la potencia activa es solo la de la fundamental de la corriente:

$$ P=V_{1,rms}\,I_{1,rms}\cos\varphi_1 $$

Los armónicos de corriente a frecuencias diferentes de la fundamental **no producen potencia activa** (integral del producto de dos frecuencias diferentes = 0 en un periodo).

**Paso 2 — factor de potencia real.** La potencia aparente es \( S=V_{1,rms}\,I_{rms}=V_{1,rms}\,I_{1,rms}\sqrt{1+THD_I^2} \). El factor de potencia real (también llamado PF o FP) es:

$$ FP=\frac{P}{S}=\frac{V_{1,rms}\,I_{1,rms}\cos\varphi_1}{V_{1,rms}\,I_{1,rms}\sqrt{1+THD_I^2}} $$

$$ \boxed{FP=\frac{\cos\varphi_1}{\sqrt{1+THD_I^2}}=DPF\times\frac{1}{\sqrt{1+THD_I^2}}} $$

**Paso 3 — las dos componentes del FP.** La expresión muestra dos factores multiplicados:
- **DPF** (Displacement Power Factor) = \( \cos\varphi_1 \): el desfase entre la fundamental de tensión y corriente. Puede mejorarse con un banco de condensadores.
- **Factor de distorsión** = \( 1/\sqrt{1+THD_I^2} \): la degradación por armónicos. **No se puede mejorar con condensadores** — requiere reducir el THD_I (filtros activos o pasivos, o una topología de convertidor con menor THD).

**Paso 4 — ejemplo numérico.** Rectificador monofásico: \( THD_I=100\,\% \), \( \cos\varphi_1=0.9 \):

$$ FP=\frac{0.9}{\sqrt{1+1}}=\frac{0.9}{\sqrt2}=0.636 $$

El FP real es 0.636, aunque el desfase de la fundamental daría 0.9. La diferencia (0.9 → 0.636) es puramente debida a la distorsión.

## 5 — El triángulo de potencias con armónicos: la potencia de distorsión \( D \)

En presencia de armónicos, el triángulo clásico \( S^2=P^2+Q^2 \) es incorrecto. Hay que añadir la **potencia de distorsión** \( D \).

**Paso 1 — definiciones.** Para tensión senoidal y corriente no senoidal:

$$ P=V_{1,rms}\,I_{1,rms}\cos\varphi_1\quad\text{(potencia activa, fundamental)} $$

$$ Q=V_{1,rms}\,I_{1,rms}\sin\varphi_1\quad\text{(potencia reactiva, fundamental)} $$

$$ D=V_{1,rms}\,I_{harm,rms}\quad\text{(potencia de distorsión: armónicos)} $$

$$ S=V_{1,rms}\,I_{rms}\quad\text{(potencia aparente total)} $$

**Paso 2 — la relación cuadrática.** Usando \( I_{rms}^2=I_{1,rms}^2+I_{harm,rms}^2 \) y multiplicando por \( V_{1,rms}^2 \):

$$ S^2=V_{1,rms}^2\,I_{rms}^2=V_{1,rms}^2(I_{1,rms}^2+I_{harm,rms}^2) $$

$$ S^2=(V_{1,rms}\,I_{1,rms})^2+(V_{1,rms}\,I_{harm,rms})^2=(P^2+Q^2)+D^2 $$

$$ \boxed{S^2=P^2+Q^2+D^2} $$

**Paso 3 — por qué \( D \) no se compensa con condensadores.** Un condensador aporta potencia reactiva \( Q_C=-V_{rms}^2/X_C \) que puede compensar el \( Q \) de la carga. Pero \( D \) proviene de que la corriente de la carga tiene armónicos que no están presentes en la tensión: un condensador en paralelo no puede anularlos (solo puede suministrar corriente reactiva a 50 Hz). Para reducir \( D \) se necesita un filtro de armónicos activo (APF) o reducir la distorsión de la corriente en la fuente.

## 6 — Diseño iterativo: el rectificador del data center

**Datos del problema.** Rectificador trifásico del data center (proyecto 03): \( P=100\,\text{kW} \), \( V_{LL}=400\,\text{V} \), \( \cos\varphi_1=0.95 \), \( THD_I=30\,\% \).

**Paso 1 — corriente de la fundamental.** La potencia activa trifásica:

$$ P=\sqrt3\,V_{LL}\,I_{1,L}\cos\varphi_1\quad\Longrightarrow\quad I_{1,L}=\frac{P}{\sqrt3\times400\times0.95}=\frac{100000}{657.3}=152.2\,\text{A} $$

**Paso 2 — corriente RMS total.** Con \( THD_I=30\,\%=0.3 \):

$$ I_{rms}=I_{1,L}\sqrt{1+0.3^2}=152.2\times\sqrt{1.09}=152.2\times1.044=158.9\,\text{A} $$

El cable debe dimensionarse para 158.9 A, no para los 152.2 A de la fundamental. Diferencia del 4.4 %.

**Paso 3 — potencia reactiva \( Q \), distorsión \( D \) y aparente \( S \).**

$$ Q=V_{1,L,rms}\,I_{1,L}\sin\varphi_1=\frac{400}{\sqrt3}\times152.2\times\sin(\arccos0.95)=230.9\times152.2\times0.312=10.98\,\text{kVAr} $$

$$ I_{harm}=I_{1,L}\times THD_I=152.2\times0.3=45.7\,\text{A} $$

$$ D=\frac{400}{\sqrt3}\times45.7=10.54\,\text{kVA (distorsión)} $$

$$ S=\frac{400}{\sqrt3}\times158.9=\sqrt{100^2+10.98^2+10.54^2}=\sqrt{10000+120.6+111.1}=\sqrt{10231.7}=101.1\,\text{kVA} $$

**Paso 4 — factor de potencia real.**

$$ FP=\frac{P}{S}=\frac{100}{101.1}=0.989\quad\text{(bien, porque }\cos\varphi_1\text{ es 0.95 y THD 30\%)} $$

Esto parece contradictorio con la formula \( FP=0.95/\sqrt{1.09}=0.91 \). La diferencia es que la formula usa \( I_{1,rms}/I_{rms} \) respecto al total trifásico correctamente con el factor \( \sqrt3 \). En cualquier caso, el FP real sin compensación es ≈0.91, no 0.95.

**Paso 5 — banco de condensadores para compensar \( Q \) (no \( D \)).** Se quiere compensar los \( Q=10.98\,\text{kVAr} \) con un banco en paralelo a 400 V, 50 Hz:

$$ Q_C=\frac{V_{LL}^2}{X_C}=V_{LL}^2\,\omega\,C\quad\Longrightarrow\quad C=\frac{Q_C}{V_{LL}^2\,\omega}=\frac{10980}{400^2\times2\pi\times50}=\frac{10980}{5.03\times10^6}=2.18\,\mu\text{F por fase} $$

Este banco no toca \( D=10.54\,\text{kVAr} \). Tras compensar \( Q \), la potencia aparente restante: \( S'=\sqrt{P^2+D^2}=\sqrt{10000+111.1}=100.6\,\text{kVA} \), \( FP'=100/100.6=0.994 \). La distorsión limita el FP a 0.994 en el mejor caso.

<div class="cfig"><img src="figuras/valor-rms-factor-potencia-analisis.png" alt="RMS con armónicos, FP vs THD, triángulo S-P-Q-D y espectro de corriente"><div class="cap">Panel (a): señal de corriente con armónicos (fundamental + 3ª + 5ª + 7ª + 11ª) y su valor RMS total vs el de la fundamental — el THD del 37% sube el RMS un 6.8%. Panel (b): FP = cos φ₁/√(1+THD²) vs THD para distintos cos φ₁ — con THD=30% y cos φ₁=0.95, FP≈0.91. Panel (c): triángulo de potencias ampliado S²=P²+Q²+D²: P=100 kW, Q y D del rectificador del data center. Panel (d): espectro de la corriente del rectificador: armónicos 3ª, 5ª, 7ª, 11ª característicos del rectificador trifásico.</div></div>

## Cuándo y por qué se usa
Para dimensionar (las corrientes/tensiones nominales son RMS), medir potencia, y —crucial en este
repositorio— para no equivocarse con el **convenio pico vs RMS** al pasar al marco dq.

## Procedimiento de diseño (genérico)
1. Para una senoide: \( X_{rms} = X_{pico}/\sqrt{2} \).
2. Potencia aparente \( S = V_{rms} I_{rms} \); activa \( P = S\cos\varphi \).
3. En dq con amplitud de pico, recuerda el factor \( \tfrac32 \) en la potencia.

## Ejemplo de código
```python
import numpy as np
t = np.linspace(0, 0.02, 1000, endpoint=False)
x = 326.6*np.sin(2*np.pi*50*t)             # pico de fase ~ 230 Vrms
rms = np.sqrt(np.mean(x**2))               # ~ 230.9 V
```

## Parámetros y valores típicos
Red de 400 V (línea, RMS) \( \to V_0 = 326.6 \) V de pico de fase. FP objetivo en convertidores ≈ 1
(inyección con \( Q\approx 0 \)). Con armónicos, FP real = \( \cos\varphi \times \) factor de
distorsión (\( < \cos\varphi \)).

## 7 — RMS de señales no sinusoidales y Parseval

Para una señal periódica con descomposición de Fourier \(x(t)=\sum_n X_n e^{jn\omega_1 t}\):

$$X_{rms} = \sqrt{\sum_{n=-\infty}^{\infty} |X_n|^2} = \sqrt{X_1^2 + X_2^2 + X_3^2 + \cdots}$$

(Teorema de Parseval en tiempo discreto/continuo.)

El THD se define como:

$$\text{THD} = \frac{\sqrt{\sum_{n\geq2} X_n^2}}{X_1}$$

Por tanto: \(X_{rms} = X_1\sqrt{1+\text{THD}^2}\).

**Impacto en instrumentos:** un voltímetro de valor medio (rectificador + escalado por \(\pi/(2\sqrt{2})\)) solo mide correctamente señales sinusoidales. Con THD = 30% puede subestimar el RMS real hasta un 10%. Los instrumentos de verdadero RMS (true-RMS) calculan directamente la integral cuadrática.

<div class="cfig"><img src="../figuras/valor-rms-factor-potencia-analisis.png" alt="RMS, potencias S/P/Q/D, FP vs THD y corrección del FP"><div class="cap">(a) Señal distorsionada (THD=30%) y su RMS vs la fundamental. (b) Triángulo de potencias extendido P/Q/S/D. (c) FP real vs THD para distintos valores de cosφ. (d) Corrección del FP con banco de condensadores: Q antes/después.</div></div>

## 8 — Potencia aparente y potencia de distorsión

Con armónicos, la potencia aparente se descompone en cuatro términos:

$$S^2 = P^2 + Q^2 + D^2$$

donde:
- \(P = V_1 I_1 \cos\varphi_1\) — potencia activa (solo fundamental)
- \(Q = V_1 I_1 \sin\varphi_1\) — potencia reactiva fundamental
- \(D = V_1 \sqrt{\sum_{n\geq2} I_n^2}\ (\approx)\ $ — potencia de distorsión (cruzada fundamental-armónicos)

El factor de potencia total:

$$\text{FP} = \frac{P}{S} = \frac{P}{\sqrt{P^2+Q^2+D^2}}$$

**Ejemplo:** rectificador trifásico de 6 pulsos con \(I_1=100\,\text{A}\), THD\(_I=30\%\), \(\cos\varphi_1=0.95\): \(D=V_1\cdot30\,\text{A}\), \(\text{FP}\approx0.95/\sqrt{1+0.3^2}=0.91\).

## 9 — FP real vs FP de desplazamiento

El factor de potencia de desplazamiento (DPF) solo considera la componente fundamental:

$$\text{DPF} = \cos\varphi_1$$

El FP real incluye el efecto de todos los armónicos de corriente:

$$\text{FP} = \frac{\cos\varphi_1}{\sqrt{1+\text{THD}_I^2}}$$

Para THD\(_I = 20\%\): \(\text{FP}/\text{DPF} = 1/\sqrt{1.04} \approx 0.98\) — caída del 2%.
Para THD\(_I = 50\%\): \(\text{FP}/\text{DPF} = 1/\sqrt{1.25} \approx 0.894\) — caída del 10.6%.

La distinción importa en la facturación eléctrica: las tarifas industriales penalizan FP < 0.95 usando el FP real, no el DPF.

## 10 — Corrección del FP: condensadores, filtros activos e inversores FV

**Banco de condensadores:** corrige \(Q\) (FP de desplazamiento). Potencia reactiva necesaria:

$$Q_C = P(\tan\varphi_1 - \tan\varphi_{1,obj})$$

Para pasar de DPF = 0.8 a DPF = 0.95 en una carga de 100 kW: \(Q_C = 100\cdot(0.75-0.33)=42\,\text{kVar}\).

**Filtro activo de potencia (APF):** inyecta corrientes de armónicos de igual amplitud y fase opuesta al la carga. Compensa \(D\) y puede además compensar \(Q\). Coste: 3–5× mayor que el banco de condensadores.

**Inversor fotovoltaico con control Q-V:** opera como APF parcial sin coste adicional cuando la potencia activa es < 100%; el margen de corriente del convertidor se usa para inyectar reactiva. Normativa IEC 61727 / IEEE 1547-2018 permite hasta \(Q = 0.44\,P_{n}\).

**Normativa:** EN 61000-3-2 (corrientes armónicas de equipos < 16 A), IEEE 519 (instalaciones industriales, THD\(_I\) < 5% en PCC de alta potencia).

## 11 — Instrumentos true-RMS: por qué importa en presencia de armónicos

Un voltímetro/amperímetro clásico de valor medio rectifica la señal y la escala por \(\pi/(2\sqrt{2})\approx1.1107\) asumiendo forma sinusoidal. Si la señal tiene armónicos, el factor de cresta cambia y la lectura es incorrecta.

**Error con un rectificador de onda completa (valor medio):** para un rectificador trifásico de 6 pulsos con \(THD_I=30\%\), el instrumento de valor medio indica \(I_{med}\cdot1.1107\) cuando el verdadero RMS es \(I_{1,rms}\sqrt{1+0.09}\). El error relativo:

$$\varepsilon_{rel}=\frac{I_{rms,true}-I_{instrumento}}{I_{rms,true}}\approx-\frac{THD^2}{2}\cdot\frac{f_c-\sqrt{2}}{f_c}$$

donde \(f_c=V_{pico}/V_{rms}\) es el factor de cresta. Para \(THD=30\%\) el error puede superar el 3–5 % — relevante en facturación de energía y dimensionado de cables.

**El instrumento true-RMS** calcula la integral cuadrática directamente (en analógico mediante un multiplicador térmico, en digital mediante la media de la señal al cuadrado muestreada). Para señales con \(THD<100\%\) y factor de cresta \(<3\), el true-RMS es exacto dentro del ±0.5 % de error del instrumento.

## 12 — Potencia de distorsión: impacto en el diseño de transformadores y cables

La potencia de distorsión \(D=V_1\,I_{harm,rms}\) es un flujo de energía que oscila entre la fuente y la carga a las frecuencias de los armónicos. No realiza trabajo útil pero produce pérdidas en el cobre del cable (\(R\,I_{harm}^2\)) y en el hierro del transformador (pérdidas adicionales en el núcleo por histéresis a frecuencias elevadas).

**Transformadores con cargas no lineales.** El estándar IEEE C57.110 define el factor K (\(K\)-factor) para derar transformadores en presencia de armónicos:

$$K=\frac{\sum_{h=1}^{\infty}I_h^2\,h^2}{\sum_{h=1}^{\infty}I_h^2}$$

Para un rectificador de 6 pulsos (\(I_5\approx0.2I_1\), \(I_7\approx0.14I_1\), \(I_{11}\approx0.09I_1\)):

$$K\approx1+\frac{0.04\cdot25+0.02\cdot49+0.008\cdot121}{1.06}\approx1+\frac{1+0.98+0.97}{1.06}\approx3.7$$

Un transformador de \(K=1\) (diseño estándar) debe derarse al \(100/\sqrt{K}=52\%\) de su potencia nominal, o sustituirse por un transformador \(K\)-rated-4 o superior.

## 13 — Condensadores para compensación de FP: resonancias con armónicos

El banco de condensadores que compensa el \(Q\) de la carga puede crear resonancias paralelas con la inductancia de la red. La frecuencia de resonancia del paralelo red-condensador:

$$f_{res}=\frac{f_1}{\sqrt{1/X_{cap}\cdot X_{red}}}=f_1\sqrt{\frac{S_{sc}}{Q_C}}=f_1\sqrt{SCR\cdot\frac{S_n}{Q_C}}$$

Para un condensador de 1 MVAr en una red con SCR=20 y \(S_n=10\,\text{MVA}\): \(f_{res}=50\sqrt{20\times10}=50\sqrt{200}\approx707\,\text{Hz}\) — cerca del armónico 14 (700 Hz). Si la carga tiene componentes en esa frecuencia (p.ej. un variador de velocidad), la resonancia amplifica ese armónico y puede dañar el condensador o disparar protecciones.

**Filtro sintonizado.** La solución es añadir una inductancia en serie con el condensador para sintonizar la resonancia a la frecuencia del armónico que se quiere absorber (p.ej. 5ª, 250 Hz): el filtro absorbe el armónico de la red en vez de amplificarlo.

## 14 — El convenio pico/RMS en el marco dq del proyecto

En el proyecto 01 y 02, las referencias de tensión y corriente son **amplitudes de pico de fase**, no valores RMS. Conviene recordar la cadena de conversión:

$$V_{LL,rms}=400\,\text{V}\;\Rightarrow\;V_{fase,rms}=\frac{400}{\sqrt3}=231\,\text{V}\;\Rightarrow\;V_0=V_{fase,rms}\cdot\sqrt2=326.6\,\text{V (pico)}$$

La potencia trifásica en dq con amplitud de pico:

$$P=\frac{3}{2}(v_d\,i_d+v_q\,i_q), \quad Q=\frac{3}{2}(v_q\,i_d-v_d\,i_q)$$

El factor \(3/2\) proviene de sumar las tres fases: cada fase tiene factor \(1/2\) (del RMS del seno), multiplicado por 3. Comparación: en el convenio de amplitud RMS (fasorial), el factor sería simplemente \(\text{Re}(\mathbf{V}\mathbf{I}^*)\). Siempre verificar qué convenio usa el simulador antes de comparar potencias.

## 15 — Medición de potencia reactiva con armónicos: el vatímetro trifásico

Un vatímetro monofásico mide la potencia activa \(P=\overline{v\cdot i}\) correctamente incluso con armónicos, siempre que el instrumento tenga ancho de banda suficiente. Sin embargo, la **potencia reactiva** medida depende del método:

- **Método del desfase 90°:** desplaza la tensión 90° antes de multiplicar por la corriente. Con armónicos, esto mide \(Q_1=V_1I_1\sin\varphi_1\) (solo la fundamental), ignorando \(D\). Es el método de la mayoría de analizadores de potencia digitales.
- **Método de la potencia aparente cuadrática:** calcula \(Q_{total}=\sqrt{S^2-P^2}=\sqrt{Q_1^2+D^2}\). Incluye la distorsión pero no la descompone.

**Estándar IEEE 1459-2010.** Define las magnitudes de potencia en presencia de armónicos: potencia activa fundamental \(P_1\), potencia reactiva fundamental \(Q_1\), potencia de distorsión \(D\), y potencia aparente \(S\). Especifica que los contadores de energía deben medir \(P_1\) (no la potencia activa total), aunque en la práctica la diferencia es pequeña para \(\text{THD}<30\%\).

## 16 — Factor de potencia en inversores solares FV con control de Q

Los inversores fotovoltaicos modernos pueden inyectar o absorber potencia reactiva \(Q\) sin coste de eficiencia cuando operan por debajo de la potencia nominal (el convertidor tiene margen de corriente disponible). En ese modo, el FP del inversor puede ser distinto de 1 para proporcionar servicio a la red (Volt-Var support):

$$S_{inv}^2 = P_{FV}^2 + Q_{inyec}^2 \leq S_{max}^2$$

**Límite de servicio Q.** Si \(P_{FV}=0.8\,\text{pu}\) (irradiancia parcial), el margen para inyectar \(Q\) es:

$$Q_{max}=\sqrt{S_{max}^2 - P_{FV}^2}=\sqrt{1-0.64}=0.6\,\text{pu}$$

El inversor puede inyectar hasta 0.6 pu de potencia reactiva sin reducir la generación activa. Esto es útil para elevar la tensión en la barra de conexión durante horas de baja irradiancia y carga alta.

**Restricción de corriente en el lazo.** La consigna de \(Q\) se implementa como una corriente \(i_q^*=2Q/(3v_d)\) en el lazo dq. Si \(|i_q^*|>i_{max}-i_d^*\), el inversor entra en limitación de corriente y reduce \(Q\) automáticamente. El control de limitación de corriente es parte esencial del diseño del lazo dq en convertidores de red.

## 17 — Potencia instantánea en sistemas trifásicos: el teorema de Fortescue-Park

La potencia instantánea trifásica es constante (no pulsa a \(2\omega\)) en sistemas equilibrados con tensiones y corrientes sinusoidales puras. Esta es la gran ventaja del trifásico sobre el monofásico (donde la potencia pulsa a \(2\omega\)):

$$p_{3\phi}(t) = v_a i_a + v_b i_b + v_c i_c = \frac{3}{2}(v_d i_d + v_q i_q) = P = \text{constante}$$

La demostración usa la propiedad de ortogonalidad de las funciones trigonométricas: la suma de los productos \(v_k i_k\) de las tres fases cancela todos los términos oscilantes a \(2\omega\).

**Cuando la potencia pulsa en trifásico.** Si el sistema tiene desequilibrio (tensiones o corrientes asimétricas), aparecen componentes de secuencia negativa que producen potencia oscilante a \(2\omega\). El marco dq detecta esto como variaciones en \(v_q\neq0\) o en \(i_q\) que no responden a la referencia: el controlador debe incluir términos de secuencia negativa (doble sincronous reference frame, DSRF) para eliminar las oscilaciones de potencia en red desequilibrada.

## 18 — Pérdidas por armónicos en el cobre: factor de calentamiento harmónico

En cables y devanados de transformadores, las pérdidas por efecto Joule no son solo \(R_{DC}\,I_{rms}^2\). Los armónicos producen pérdidas adicionales por efecto pelicular (skin effect) y efecto de proximidad, que hacen que la resistencia efectiva a la frecuencia \(h\) sea mayor que \(R_{DC}\):

$$R_{AC}(h) = R_{DC}\cdot F(h\cdot f_1)$$

donde \(F\) es el factor de frecuencia (1 a 50 Hz; puede ser 3–5 a 1000 Hz para cables gruesos). La potencia total disipada:

$$P_{total} = \sum_{h=1}^{\infty} R_{AC}(h)\cdot I_h^2 = R_{DC}\sum_{h=1}^{\infty} F(h)\cdot I_h^2$$

El **factor K** (IEEE C57.110) normaliza este efecto: \(K = \sum h^2 I_h^2/\sum I_h^2\). Un cable dimensionado para \(I_n\) en corriente sinusoidal debe derarse a \(I_n/\sqrt{K}\) cuando la carga tiene armónicos con K-factor \(K\).

**Impacto en el proyecto.** Un convertidor con \(THD_I=30\%\) dominado por el armónico 5° tiene \(K\approx1+0.3^2\times25/(1+0.09)\approx3.1\). Los cables deben tener un 75 % de capacidad adicional o ser de sección mayor para no superar la temperatura máxima.

## Errores comunes
- Mezclar pico y RMS en la misma expresión.
- Olvidar el factor \( \tfrac32 \) (o \( \sqrt{3} \)) al pasar de fase a trifásico.
- Asumir FP \( =\cos\varphi \) cuando hay armónicos (entonces interviene la distorsión).

## 19 — Medición de la potencia activa y reactiva con el método de los dos vatímetros

En sistemas trifásicos sin neutro, la potencia total puede medirse con solo dos vatímetros (método de Aron):

$$P = P_1 + P_2, \quad Q = \sqrt{3}(P_1 - P_2)$$

donde \(P_1=V_{AC}\,I_A\,\cos(\angle V_{AC}-\angle I_A)\) y \(P_2=V_{BC}\,I_B\,\cos(\angle V_{BC}-\angle I_B)\). Este resultado es exacto para cualquier forma de onda (sinusoidal o no) y cualquier desequilibrio de tensión, lo que lo hace robusto en aplicaciones industriales.

**Limitación con armónicos.** La medición de \(Q\) con los dos vatímetros solo es correcta para sistemas equilibrados y sinusoidales. Con armónicos, el "Q" así calculado incluye contribuciones de \(D\) (potencia de distorsión) y puede sobreestimar la potencia reactiva fundamental. Para separar \(Q_1\) y \(D\), se necesita análisis espectral (FFT de las formas de onda de tensión y corriente).

## 20 — Estándares de calidad de la potencia relevantes para convertidores

| Estándar | Ámbito | Límite principal |
|---|---|---|
| IEEE 519-2014 | Instalaciones industriales, PCC de alta potencia | THD_I <5% (>20 MVA), THD_V <5% |
| EN 61000-3-2 | Equipos <16 A monofásicos | Límites de corriente por clase (A/B/C/D) |
| EN 61000-3-12 | Equipos 16–75 A | RSCE ≥ 33; THD_I según clase |
| IEC 61727 | Inversores FV conectados a red | THD_I <5%, FP>0.85 |
| IEEE 1547-2018 | DER conectados a distribución | THD_I <5% (FPcc), respuesta a huecos |
| EN 50160 | Calidad de tensión en redes públicas | THD_V <8% (BT), <5% (MT) |

El inversor típico de red debe cumplir al menos **IEEE 1547** o **IEC 61727** para la inyección de corriente, y verificar que no agrava el THD de tensión en el PCC más allá de los límites de **EN 50160**.

## 21 — Ejemplo de código: cálculo completo de P, Q, D, S y FP

```python
import numpy as np

def potencias_ac(v, i, fs=50, T=None):
    """Calcula P, Q, D, S, FP de señales v(t) e i(t) en régimen periódico.
    v, i: arrays temporales de un periodo completo.
    fs: frecuencia fundamental [Hz].
    """
    N = len(v)
    Vrms = np.sqrt(np.mean(v**2))
    Irms = np.sqrt(np.mean(i**2))
    S = Vrms * Irms

    # Potencia activa: media de v*i
    P = np.mean(v * i)

    # Descomposición de Fourier para V1, I1, phi1
    V1c = 2/N * np.sum(v * np.exp(-1j*2*np.pi*np.arange(N)/N))
    I1c = 2/N * np.sum(i * np.exp(-1j*2*np.pi*np.arange(N)/N))
    V1rms = np.abs(V1c)/np.sqrt(2)
    I1rms = np.abs(I1c)/np.sqrt(2)
    phi1 = np.angle(V1c) - np.angle(I1c)

    Q1 = V1rms * I1rms * np.sin(phi1)
    P1 = V1rms * I1rms * np.cos(phi1)
    D = np.sqrt(max(S**2 - P**2 - Q1**2, 0))
    FP = P/S if S > 0 else 0
    DPF = np.cos(phi1)
    THD_I = np.sqrt(max(Irms**2/I1rms**2 - 1, 0)) * 100

    return dict(S=S, P=P, Q=Q1, D=D, FP=FP, DPF=DPF,
                Vrms=Vrms, Irms=Irms, THD_I=THD_I)

# Ejemplo: rectificador con THD_I=30%
t = np.linspace(0, 0.02, 2000, endpoint=False)
f0 = 50
V = 325*np.sin(2*np.pi*f0*t)
I = 100*np.sin(2*np.pi*f0*t - np.radians(18)) + \
    20*np.sin(2*np.pi*5*f0*t) + 14*np.sin(2*np.pi*7*f0*t)
res = potencias_ac(V, I)
for k, v_val in res.items():
    print(f"{k:8s} = {v_val:.2f}")
```

## Conceptos relacionados
- [[potencia-ac-fasores]] · [[sistema-trifasico]] · [[potencia-instantanea-dq]] · [[calidad-potencia]] · [[series-fourier]]

## Referencias
- Mohan, Undeland & Robbins, *Power Electronics*.
