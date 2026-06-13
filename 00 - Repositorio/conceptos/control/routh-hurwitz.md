---
titulo: Criterio de Routh-Hurwitz
slug: routh-hurwitz
categoria: control
tipo: metodo
nivel: basico
proyectos: []
objetivos: [comprobar estabilidad sin calcular las raíces del polinomio característico]
tags: [routh, hurwitz, estabilidad, ecuacion-caracteristica, basico, control]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-09
relacionados: [estabilidad-bibo, polos-ceros, funcion-transferencia, criterio-nyquist]
referencias:
  - "Ogata, Ingeniería de Control Moderna, Pearson"
  - "Dorf, Bishop, Modern Control Systems, Pearson"
---

## Definición
Test **algebraico** que dice cuántas raíces de un polinomio tienen parte real positiva (polos
inestables) sin resolverlo, a partir de los signos de la primera columna de la **tabla de Routh**.

## Fundamento teórico
Dado el polinomio característico
$$ a_n s^n + a_{n-1}s^{n-1} + \dots + a_1 s + a_0 = 0 $$
condición **necesaria**: todos los \( a_i \) presentes y del mismo signo. Condición **suficiente**:
se construye la tabla
$$ b_1=\frac{a_{n-1}a_{n-2}-a_n a_{n-3}}{a_{n-1}}, \quad
   b_2=\frac{a_{n-1}a_{n-4}-a_n a_{n-5}}{a_{n-1}}, \ \dots $$
El **nº de cambios de signo en la primera columna = nº de polos en el SPD**. Sistema estable
\( \iff \) toda la primera columna es positiva (sin cambios de signo).

Casos especiales: un cero en la primera columna se sustituye por \( \varepsilon\to0^+ \); una
fila entera nula indica raíces simétricas (polinomio auxiliar) → al menos marginalmente inestable.

<div class="cfig"><img src="figuras/routh-hurwitz-locus.png" alt="raices del polinomio al variar Kp"><div class="cap">Raíces de $s^3+3s^2+2s+K_p$ al variar $K_p$ (color). El par complejo cruza el eje imaginario en $s=\pm j\sqrt{2}$ exactamente en $K_p=6$: por debajo el sistema es estable, por encima inestable. Routh entrega ese límite ($0<K_p<6$) sin resolver el polinomio.</div></div>

## Cuándo y por qué se usa
Para hallar **rangos de un parámetro** (p.ej. la ganancia \( K \)) que mantienen la estabilidad,
en sistemas de orden bajo-medio y sin retardos. Complementa a [[criterio-nyquist]] (que sí maneja
retardos).

## Procedimiento (genérico)
1. Escribe la ecuación característica \( 1+L(s)=0 \) como polinomio.
2. Chequeo rápido: ¿faltan términos o cambian de signo? → inestable.
3. Construye la tabla de Routh.
4. Cuenta cambios de signo en la 1ª columna; con un parámetro libre, despeja la condición.

## Ejemplo de aplicación real
**Problema:** Lazo de tensión de tercer orden con polinomio característico \( s^3+3s^2+2s+K_p \). Determinar el rango de \( K_p \) que garantiza estabilidad.

Tabla de Routh: fila \( s^3 \): \( [1,\,2] \); fila \( s^2 \): \( [3,\,K_p] \); fila \( s^1 \): \( [(6-K_p)/3,\,0] \); fila \( s^0 \): \( [K_p,\,0] \). Para primera columna positiva: \( K_p>0 \) y \( (6-K_p)/3>0\Rightarrow K_p<6 \). Rango de estabilidad: \( 0<K_p<6 \). En \( K_p=6 \): el elemento de \( s^1 \) se anula — sistema al límite con par de polos imaginarios puros en \( \pm j\sqrt{2} \) (oscilaciones sostenidas). Esto da directamente el **margen de ganancia**: la ganancia de lazo puede multiplicarse por \( 6/K_p^{nom} \) antes de inestabilizar.

## Ejemplo de código
```python
import sympy as sp
s, K = sp.symbols('s K')
p = sp.Poly(s**3 + 3*s**2 + 3*s + (1+K), s)
print(sp.stability.routh(p) if hasattr(sp,'stability') else p.all_coeffs())
# para K: estable si todos los términos de la 1ª columna > 0
```

## Parámetros y valores típicos
Útil hasta orden ~4-5 a mano. Para órdenes altos o MIMO, usar autovalores numéricos
(`np.linalg.eigvals`).

## Errores comunes
- Olvidar el chequeo necesario (signos/términos) antes de montar la tabla.
- No tratar los casos especiales (cero en columna, fila nula).
- Usarlo con retardos puros \( e^{-sT} \) (no es polinómico) → usar Nyquist.

## Conceptos relacionados
- [[estabilidad-bibo]] · [[polos-ceros]] · [[criterio-nyquist]] · [[funcion-transferencia]]

## Referencias
- Ogata, *Ingeniería de Control Moderna*.
- Dorf, Bishop, *Modern Control Systems*.
