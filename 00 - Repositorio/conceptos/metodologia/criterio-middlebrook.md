---
titulo: Criterio de Middlebrook (estabilidad de cascadas por impedancia)
slug: criterio-middlebrook
categoria: metodologia
tipo: metodo
nivel: avanzado
proyectos: [03-DataCenter-IA]
objetivos: [evaluar la estabilidad de una cascada fuente-carga por sus impedancias]
tags: [middlebrook, impedancia, cascada, bus-dc, estabilidad]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [dinamica-bus-dc, impedancia-salida-estabilidad]
referencias:
  - "Middlebrook, Input Filter Considerations in Design of Switching Regulators, IEEE 1976"
---

## Definición
Criterio para decidir la estabilidad de una **cascada fuente → carga** (p.ej. filtro/fuente que
alimenta un convertidor) a partir del cociente de sus impedancias, sin reconstruir el sistema
completo. Es el análogo DC del criterio de estabilidad por impedancia en AC.

## Fundamento teórico
Sea \( Z_{fuente}(s) \) la impedancia de salida de la fuente y \( Z_{carga}(s) \) la impedancia
de entrada de la carga. Si ambas son estables por separado, la cascada es estable según el
Nyquist del **cociente**:
$$ T_m(s) = \frac{Z_{fuente}(s)}{Z_{carga}(s)} $$
El **criterio de Middlebrook** (condición suficiente y conservadora) exige:
$$ |Z_{fuente}(j\omega)| \ll |Z_{carga}(j\omega)| \quad \forall \omega $$
es decir, que la impedancia de salida de la fuente sea mucho menor que la de entrada de la carga.
Con una [[dinamica-bus-dc|CPL]], \( Z_{carga}=-V^2/P \) (resistencia negativa,
\( |Z|=V^2/P \)): al subir \( P \), \( |Z_{carga}| \) baja y, cuando cae por debajo del pico de
resonancia de \( |Z_{fuente}| \), el sistema se inestabiliza. Existen criterios menos
conservadores (GMPM, banda prohibida, ESAC) que relajan el de Middlebrook.

<div class="cfig"><img src="figuras/criterio-middlebrook-impedancias.png" alt="impedancia de fuente con pico de resonancia frente a impedancia de carga CPL"><div class="cap">La fuente (filtro LC) tiene un pico de impedancia en su resonancia; la carga CPL presenta $|Z_{carga}|=V^2/P$, una línea horizontal que baja al subir la potencia. Mientras $|Z_{carga}|$ quede por encima del pico hay margen; cuando la potencia la hace cortar el pico, se viola el criterio y el bus se inestabiliza. Da la potencia límite de forma modular.</div></div>

## 1 — De dónde sale el cociente \( Z_o/Z_i \) (minor loop gain)
**Paso 1 — partir la cascada.** En el punto de interconexión, la fuente entrega una tensión \( v \) y la carga absorbe una corriente \( i \). Modelando cada lado por su Thévenin/Norton de pequeña señal: la fuente es \( v=v_{src}-Z_o\,i \) (su tensión ideal \( v_{src} \) menos la caída en su impedancia de salida \( Z_o=Z_{fuente} \)); la carga es \( i=v/Z_i \) (con \( Z_i=Z_{carga} \) su impedancia de entrada).

**Paso 2 — cerrar el lazo.** Sustituyendo \( i=v/Z_i \) en la ecuación de la fuente:
$$ v=v_{src}-Z_o\frac{v}{Z_i}\;\Rightarrow\; v\left(1+\frac{Z_o}{Z_i}\right)=v_{src}\;\Rightarrow\; \boxed{\;\frac{v}{v_{src}}=\frac{1}{1+\dfrac{Z_o}{Z_i}}\;} $$
La transferencia real de la cascada es la que tendría la fuente **sola** (\( v=v_{src} \)) multiplicada por el factor \( \dfrac{1}{1+T_m} \), con
$$ T_m(s)=\frac{Z_o(s)}{Z_i(s)}=\frac{Z_{fuente}}{Z_{carga}} $$

**Paso 3 — leerlo como un lazo.** \( \dfrac{1}{1+T_m} \) tiene exactamente la forma de una sensibilidad: \( T_m \) es la **ganancia de lazo menor** (minor loop gain) de la interconexión. Si fuente y carga son estables por separado, la cascada es estable \( \Leftrightarrow 1+T_m \) no tiene ceros en el semiplano derecho \( \Leftrightarrow \) el Nyquist de \( T_m \) no rodea \( -1 \). Toda la estabilidad de la cascada se reduce al Nyquist de **un cociente de impedancias**.

**Paso 4 — la condición de Middlebrook.** Si \( |T_m|=|Z_{fuente}|/|Z_{carga}|\ll1 \) a toda frecuencia, el punto \( -1 \) queda lejísimos: imposible rodearlo. De ahí la condición **suficiente** (y conservadora):
$$ \boxed{\;|Z_{fuente}(j\omega)|\ll|Z_{carga}(j\omega)|\quad\forall\omega\;} $$
Es suficiente pero no necesaria: la cascada puede ser estable aun violándola localmente, mientras el Nyquist de \( T_m \) no rodee \( -1 \) (eso explotan GMPM, banda prohibida, ESAC).

## 2 — La potencia límite con una carga CPL: cálculo
**Paso 1 — impedancia de la CPL.** Una carga de potencia constante absorbe \( P=v\,i \) ⇒ \( i=P/v \). Su impedancia incremental de pequeña señal es
$$ Z_{carga}=\frac{\partial v}{\partial i}=\left(\frac{\partial i}{\partial v}\right)^{-1}=\left(-\frac{P}{v^2}\right)^{-1}=-\frac{V^2}{P} $$
resistencia **negativa**; en módulo, \( |Z_{carga}|=V^2/P \). Sube la potencia ⇒ baja \( |Z_{carga}| \).

**Paso 2 — la fuente y su pico.** La fuente es un filtro LC, cuya impedancia de salida tiene un **pico** en su resonancia. Llámese \( Z_{pico}=\max_\omega|Z_{fuente}| \). El criterio se viola cuando la línea horizontal \( |Z_{carga}|=V^2/P \) cae por debajo de ese pico:
$$ \frac{V^2}{P}<Z_{pico} $$

**Paso 3 — despejar la potencia límite.** El borde es \( V^2/P=Z_{pico} \):
$$ \boxed{\;P_{lim}=\frac{V^2}{Z_{pico}}\;} $$

**Paso 4 — número del proyecto 03.** Con \( V=800 \) V y un pico medido \( Z_{pico}\approx4.8\,\Omega \):
$$ P_{lim}=\frac{800^2}{4.8}=\frac{640000}{4.8}\approx1.33\times10^5\,\text{W}\approx134\ \text{kW} $$
que coincide con la \( P_{crit}\approx128 \) kW obtenida por autovalores del sistema completo (la pequeña diferencia es el conservadurismo del criterio). El método da la potencia límite de forma **modular**, sin montar el modelo entero.

## Cuándo y por qué se usa
En sistemas DC en cascada (microrredes DC, data centers, alimentación distribuida) y en filtros
de entrada de convertidores. Permite diseñar de forma modular: caracterizar fuente y carga por
separado.

## Procedimiento (genérico)
1. Obtén \( Z_{fuente}(j\omega) \) (impedancia de salida del filtro/fuente).
2. Obtén \( Z_{carga}(j\omega) \) (de la CPL: \( -V^2/P \)).
3. Compara magnitudes: si \( |Z_{fuente}| \) supera \( |Z_{carga}| \) en alguna banda → riesgo.
4. Para el límite exacto, aplica Nyquist a \( T_m=Z_{fuente}/Z_{carga} \).
5. Si no cumple: baja \( |Z_{fuente}| \) (más \( C \), amortiguamiento) o sube \( |Z_{carga}| \).

## Ejemplo de código
```python
# pico de |Z_fuente| vs |Z_carga| = V^2/P  -> potencia limite
P_lim = V**2 / np.max(np.abs(Z_fuente))
```

## Parámetros y valores típicos
Margen recomendado: \( |Z_{fuente}| \) varias veces menor que \( |Z_{carga}| \) en la resonancia.
Criterio conservador (deja margen de diseño).

## Errores comunes
- Aplicar Middlebrook (muy conservador) y sobredimensionar; para el límite real usar Nyquist del cociente.
- Olvidar que \( |Z_{carga}| \) de la CPL baja al subir la potencia.

## Uso en proyectos
- **03 - DataCenter-IA**: pico de \( |Z_{fuente}|\approx 4.8 \) Ω → potencia límite \( V^2/4.8 \approx 134 \)
  kW, coincide con la \( P_{crit} \) por autovalores (128 kW). Validación cruzada de la Fase 2.

## Conceptos relacionados
- [[dinamica-bus-dc|estabilidad del bus DC con CPL]] · [[impedancia-salida-estabilidad]]

## Referencias
- Middlebrook, *Input Filter Considerations...*, IEEE 1976.
