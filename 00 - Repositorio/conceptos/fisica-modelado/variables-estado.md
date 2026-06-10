---
titulo: Cómo definir las variables de estado
slug: variables-estado
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: [01-GFM-Impedance, 02-GFL-Impedance, 03-DataCenter-IA]
objetivos: [elegir el conjunto minimo de variables que describen el sistema]
tags: [estado, orden, energia, independencia, modelado]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [modelado-sistemas, representacion-espacio-estados, filtro-lcl, linealizacion-teoria]
referencias:
  - "Franklin, Powell, Feedback Control of Dynamic Systems"
---

## Definición
Las **variables de estado** son el conjunto **mínimo** de variables que, junto con las entradas
futuras, determinan por completo la evolución del sistema. Son la "memoria" del sistema en cada
instante.

## Fundamento teórico
Idea central: el estado guarda la **energía almacenada**. El número de variables de estado
(el **orden** del sistema) es igual al número de elementos **independientes** que almacenan
energía:
- Inductor → su **corriente** \( i_L \) (energía \( \tfrac{1}{2}L i_L^2 \)).
- Condensador → su **tensión** \( v_C \) (energía \( \tfrac{1}{2}C v_C^2 \)).
- Masa/inercia → su **velocidad** \( \omega \) (energía \( \tfrac{1}{2}J\omega^2 \)).
- Integradores del control (PI, filtros) → su salida es estado.

La elección **no es única** (cualquier transformación invertible \( \mathbf{z}=T\mathbf{x} \) da
otro conjunto válido), pero conviene que sean:
- **Físicas / medibles** (facilitan observador y validación).
- **Independientes**: si un lazo solo de condensadores o un corte solo de inductores crea una
  dependencia, esos almacenadores **no** son independientes y el orden baja.

## Cuándo y por qué se usa
Es el paso que fija la estructura del modelo de estado. Elegir bien evita estados redundantes
(matriz \( A \) singular) o modelos de orden equivocado.

## Procedimiento (genérico)
1. Lista todos los elementos almacenadores de energía.
2. Comprueba **independencia** (lazos de C, cortes de L → reducen el orden).
3. Asigna a cada almacenador independiente su variable de energía (i en L, v en C, ω en J).
4. Añade los estados del **control** (integradores de PI, filtros, PLL).
5. Verifica que con esas variables puedes escribir \( \dot{\mathbf{x}}=\mathbf{f}(\mathbf{x},\mathbf{u}) \).

## Ejemplo de código
```python
# filtro LCL por fase -> 3 estados; en dq -> 6 (cada uno d y q)
estados = ["iL1", "vC", "iL2"]          # corriente L1, tension Cf, corriente L2
```

## Parámetros y valores típicos
GFM (proyecto 01): 15 estados = 6 del LCL (dq) + δ + Pm, Qm + 4 integradores PI + 2 del HPF.
GFL (proyecto 02): 10 = 6 del LCL + δ + ε(PLL) + 2 integradores de corriente.

## Errores comunes
- Tomar como estados independientes condensadores en paralelo o inductores en serie (no lo son).
- Olvidar los estados del controlador (integradores, filtros, PLL).

## Uso en proyectos
- **01/02**: las variables de estado se eligieron como las corrientes de inductor y tensiones de
  condensador del LCL más los estados del control (droop/PLL e integradores).

## Conceptos relacionados
- [[modelado-sistemas]] · [[representacion-espacio-estados]] · [[filtro-lcl]]

## Referencias
- Franklin, Powell, *Feedback Control of Dynamic Systems*.
