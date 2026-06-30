---
titulo: Sistema por unidad (p.u.)
slug: sistema-por-unidad
categoria: fisica-modelado
tipo: concepto
nivel: basico
proyectos: []
objetivos: [normalizar magnitudes eléctricas para comparar y escalar sistemas]
tags: [por-unidad, pu, normalizacion, base, basico, modelado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-30
relacionados: [red-thevenin-scr, potencia-ac-fasores, sistema-trifasico, filtro-lcl]
referencias:
  - "Kundur, Power System Stability and Control, McGraw-Hill 1994"
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
---

## Definición
Sistema de normalización en el que cada magnitud se expresa como fracción de un **valor base**:
\( x_{pu}=x/x_{base} \). Convierte voltios, amperios y ohmios en números adimensionales en torno
a 1.

## Fundamento teórico
Se eligen **dos** bases independientes (típicamente \( S_{base} \) y \( V_{base} \)); el resto se
derivan:
$$ I_{base}=\frac{S_{base}}{\sqrt{3}\,V_{base}},\qquad
   Z_{base}=\frac{V_{base}^2}{S_{base}},\qquad
   \omega_{base}=2\pi f,\ \ L_{base}=\frac{Z_{base}}{\omega_{base}},\ \ C_{base}=\frac{1}{\omega_{base}Z_{base}} $$
Ventajas: los parámetros quedan en rangos conocidos (impedancias de transformador 0.05–0.15 p.u.),
las relaciones de transformación desaparecen y el modelo es **escalable** a cualquier potencia.
Para cambiar de base: \( Z_{pu}^{nuevo}=Z_{pu}^{viejo}\frac{S_{base}^{nuevo}}{S_{base}^{viejo}}
\left(\frac{V_{base}^{viejo}}{V_{base}^{nuevo}}\right)^2 \).

<div class="cfig"><img src="figuras/sistema-por-unidad-impedancias.png" alt="impedancias del sistema en por unidad sumandose"><div class="cap">En por unidad, las impedancias de equipos muy distintos (transformador, filtro, red) quedan todas en el rango ~0.05–0.15 y se suman directamente una vez referidas a la misma base. Aquí $Z_{tot}=0.25$ pu; sin pu, cada componente estaría en ohmios de su base propia y sumarlos sería un error.</div></div>

## 1 — De dónde salen las bases derivadas
**Paso 1 — elegir las dos bases independientes.** El sistema p.u. fija libremente **dos** magnitudes; el resto se obliga a ser coherente con las leyes físicas. Se eligen \( S_{base} \) (potencia trifásica nominal) y \( V_{base} \) (tensión de línea nominal RMS). Todas las demás bases salen de imponer que las **mismas fórmulas** del sistema real valgan también entre las bases.

**Paso 2 — base de corriente.** La potencia aparente trifásica cumple \( S=\sqrt3\,V_{LL}I_L \) (ver [[sistema-trifasico]]). Imponiendo esa relación entre bases, \( S_{base}=\sqrt3\,V_{base}I_{base} \), y despejando:

$$ \boxed{\;I_{base}=\frac{S_{base}}{\sqrt3\,V_{base}}\;} $$

**Paso 3 — base de impedancia.** La ley de Ohm por fase es \( V_{fase}=Z\,I \). Con \( V_{fase,base}=V_{base}/\sqrt3 \) e \( I_{base} \) del paso 2:

$$ Z_{base}=\frac{V_{fase,base}}{I_{base}}=\frac{V_{base}/\sqrt3}{S_{base}/(\sqrt3\,V_{base})}=\frac{V_{base}/\sqrt3\cdot\sqrt3\,V_{base}}{S_{base}}=\frac{V_{base}^2}{S_{base}} $$

Los dos \( \sqrt3 \) se cancelan y queda la forma trifásica limpia:

$$ \boxed{\;Z_{base}=\frac{V_{base}^2}{S_{base}}\;} $$

**Paso 4 — bases de inductancia y capacitancia.** Como \( X_L=\omega L \) y \( X_C=1/(\omega C) \) (ver [[impedancia-reactancia]]), las reactancias base son también \( Z_{base} \), de donde a la frecuencia base \( \omega_{base}=2\pi f \):

$$ \boxed{\;L_{base}=\frac{Z_{base}}{\omega_{base}},\qquad C_{base}=\frac{1}{\omega_{base}Z_{base}}\;} $$

Cada base se deriva imponiendo una ley física (Ohm, potencia, reactancia) entre los valores base, de modo que **toda ecuación del sistema real conserva su forma en p.u.** Un cálculo con \( S_{base}=1 \) MVA, \( V_{base}=690 \) V da \( I_{base}\approx837 \) A y \( Z_{base}\approx0{,}476\,\Omega \).

## 2 — De dónde sale la fórmula de cambio de base
**Paso 1 — el valor físico es invariante.** Una impedancia en ohmios \( Z_\Omega \) es la misma magnitude física, se exprese en la base que se exprese. En cada base, \( Z_{pu}=Z_\Omega/Z_{base} \), luego \( Z_\Omega=Z_{pu}^{viejo}Z_{base}^{viejo}=Z_{pu}^{nuevo}Z_{base}^{nuevo} \).

**Paso 2 — despejar el nuevo p.u.** Aislando \( Z_{pu}^{nuevo} \):

$$ Z_{pu}^{nuevo}=Z_{pu}^{viejo}\,\frac{Z_{base}^{viejo}}{Z_{base}^{nuevo}}=Z_{pu}^{viejo}\,\frac{V_{base,viejo}^2/S_{base}^{viejo}}{V_{base,nuevo}^2/S_{base}^{nuevo}} $$

**Paso 3 — reordenar.** Reagrupando los cocientes de \( S \) y de \( V \):

$$ \boxed{\;Z_{pu}^{nuevo}=Z_{pu}^{viejo}\,\frac{S_{base}^{nuevo}}{S_{base}^{viejo}}\left(\frac{V_{base}^{viejo}}{V_{base}^{nuevo}}\right)^2\;} $$

La \( S \) entra directa (más potencia base → menos ohmios por p.u.) y la \( V \) al cuadrado por la \( V^2 \) de \( Z_{base} \). Es la cuenta del ejemplo: un transformador de \( 0{,}10 \) p.u. en su base de 1 MVA pasa a \( 0{,}05 \) p.u. en la base de 500 kVA del convertidor (mismo \( V_{base} \)).

## Cuándo y por qué se usa
En modelado de convertidores y redes: facilita comparar equipos de distinta potencia, fija
condiciones de diseño (corriente nominal = 1 p.u.) y mejora el **condicionamiento numérico** de
los modelos de estado.

## Procedimiento (genérico)
1. Elige \( S_{base} \) (potencia nominal del convertidor) y \( V_{base} \) (tensión nominal).
2. Deriva \( I_{base},Z_{base},L_{base},C_{base} \).
3. Divide cada parámetro físico por su base.
4. Reporta resultados en p.u.; reconvierte a SI solo al final si hace falta.

## Ejemplo de aplicación real
**Problema:** Convertidor de 500 kVA/690 V conectado a transformador de 1 MVA/690 V con \( Z_{cc}=10\,\%\) en base propia. Expresar la impedancia del transformador en la base del convertidor.

Bases del convertidor: \( S_{b,c}=500\,\text{kVA} \), \( V_{b,c}=690\,\text{V} \). Cambio de base: \( Z_{pu}^{(c)}=Z_{pu}^{(t)}\times(S_{b,c}/S_{b,t})\times(V_{b,t}/V_{b,c})^2=0.10\times(500/1000)\times1=0.05\,\text{p.u.} \). En la base del convertidor, el transformador equivale a solo el 5 % de impedancia. Si el reactor de filtro es 0.12 p.u. y la red equivalente 0.08 p.u. en la misma base, la impedancia total vista desde el convertidor es \( Z_{total}=0.12+0.05+0.08=0.25\,\text{p.u.} \) y la SCR es \( 1/0.05=20 \) (solo el transformador). Sin p.u., cada componente estaría en ohmios de su base propia y sumarlos directamente sería un error.

## Ejemplo de código
```python
Sb, Vb, f = 1e6, 690.0, 50.0          # 1 MVA, 690 V, 50 Hz
Ib = Sb/(3**0.5*Vb); Zb = Vb**2/Sb
Lb = Zb/(2*3.14159*f); Cb = 1/(2*3.14159*f*Zb)
L_pu = 0.15e-3 / Lb                    # ej.: 0.15 mH a p.u.
```

## Parámetros y valores típicos
Impedancia de cortocircuito de transformador 0.05–0.15 p.u.; filtro de convertidor \( L\approx
0.05\text{–}0.15 \) p.u., \( C\approx 0.05\text{–}0.1 \) p.u.

## Errores comunes
- Mezclar bases monofásicas y trifásicas (factor \( \sqrt3 \) / 3).
- No reescalar al combinar equipos con bases distintas.
- Confundir base de pico y base RMS en las tensiones.

## Conceptos relacionados
- [[red-thevenin-scr]] · [[potencia-ac-fasores]] · [[sistema-trifasico]] · [[filtro-lcl]]

## Referencias
- Kundur, *Power System Stability and Control*, 1994.
- Yazdani, Iravani, 2010.
