---
titulo: Modelado de sistemas físicos
slug: modelado-sistemas
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance, 03-DataCenter-IA]
objetivos: [obtener un modelo matematico util de un sistema fisico]
tags: [modelado, ecuaciones, caja-blanca, identificacion, dominios]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [variables-estado, representacion-espacio-estados, linealizacion-teoria, marco-dq, modelo-promediado]
referencias:
  - "Ljung, System Identification, Prentice Hall 1999"
  - "Khalil, Nonlinear Systems, Prentice Hall 2002"
---

## Definición
Construir una descripción matemática que reproduzca el comportamiento **relevante** de un sistema
físico para un propósito concreto (diseñar control, analizar estabilidad, simular). Un modelo no
es "la realidad", es una aproximación útil con un dominio de validez.

## Fundamento teórico
Enfoques según el conocimiento disponible:
- **Caja blanca** (de conocimiento): se derivan las ecuaciones de las leyes físicas
  (balance + leyes constitutivas). Es lo que usamos en convertidores.
- **Caja negra** (identificación): se ajusta un modelo a datos de entrada/salida sin física.
- **Caja gris**: estructura física con parámetros ajustados a datos.

La caja blanca combina:
- **Leyes de balance** (conservación): Kirchhoff de corrientes/tensiones, Newton, balance de energía.
- **Leyes constitutivas** de cada elemento: inductor \( v=L\,\dfrac{di}{dt} \), condensador
  \( i=C\,\dfrac{dv}{dt} \), resistencia \( v=Ri \), inercia \( T=J\,\dfrac{d\omega}{dt} \).
Combinándolas se obtiene un sistema de EDOs \( \dot{\mathbf{x}}=\mathbf{f}(\mathbf{x},\mathbf{u}) \).
La elección de **nivel de abstracción** (qué se desprecia) es la decisión clave: p.ej. modelo
promediado vs conmutado.

<div class="cfig"><img src="figuras/modelado-sistemas-flujo.png" alt="flujo del modelado caja blanca de sistema fisico a modelo lineal"><div class="cap">Flujo del modelado caja blanca: del sistema físico se extraen las leyes de balance y constitutivas, que dan un sistema de EDOs $\dot x=f(x,u)$; se lleva a espacio de estados, se lineliza si el análisis lo requiere y finalmente se valida contra datos o un modelo de mayor fidelidad. La decisión clave es el nivel de abstracción (qué se desprecia).</div></div>

## Cuándo y por qué se usa
Es el primer paso de todo: sin modelo no hay diseño ni análisis. El nivel del modelo debe
ajustarse al uso (diseño de control → promediado lineal; verificar EMI → conmutado).

## Procedimiento (genérico)
1. Define el **propósito** del modelo y su rango de validez (qué fenómenos debe capturar).
2. Identifica los elementos **almacenadores de energía** (fijan el orden; ver [[variables-estado]]).
3. Aplica leyes de balance + constitutivas → ecuaciones diferenciales.
4. Lleva a forma de estado \( \dot{\mathbf{x}}=\mathbf{f}(\mathbf{x},\mathbf{u}) \) (ver [[representacion-espacio-estados]]).
5. Si hace falta para el análisis lineal, lineliza (ver [[linealizacion-teoria]]).
6. **Valida** el modelo contra datos o un modelo de mayor fidelidad.

## Ejemplo de código
```python
# circuito RLC serie -> dos estados (i del inductor, v del condensador)
def f(x, u):
    i, v = x; Vin = u
    di = (Vin - R*i - v)/L
    dv = i/C
    return [di, dv]
```

## Parámetros y valores típicos
El orden del modelo = nº de almacenadores independientes. Para un filtro LCL por fase: 3
(\( i_{L1}, v_C, i_{L2} \)); en dq, 6.

## Errores comunes
- Modelar con más detalle del necesario para el propósito (lento, frágil).
- No declarar el rango de validez → usar el modelo fuera de donde vale.

## Uso en proyectos
- **01/02**: caja blanca del inversor (LCL + control) en marco dq, nivel promediado, validado
  contra inyección de impedancia y promediado-vs-conmutado.

## Conceptos relacionados
- [[variables-estado]] · [[representacion-espacio-estados]] · [[linealizacion-teoria]] · [[modelo-promediado]]

## Referencias
- Khalil, *Nonlinear Systems*, 2002 · Ljung, *System Identification*, 1999.
