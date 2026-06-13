---
titulo: Carga pulsante de data centers de IA
slug: carga-pulsante-datacenter-ia
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: [03-DataCenter-IA]
objetivos: [modelar la demanda electrica caracteristica de la computacion de IA]
tags: [datacenter, IA, carga-pulsante, RoCoF, microrred, GPU]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [carga-potencia-constante-cpl, vsm-inercia, estabilidad-bus-dc-cpl]
referencias:
  - "Informes de operadores de red sobre integracion de cargas de data center (2024-2025)"
---

## Definición
La carga eléctrica de un data center de IA tiene un perfil distintivo: **escalones de potencia
grandes, rápidos y sincronizados**. Miles de GPUs entran o salen de un mismo *job* de
entrenamiento casi a la vez, lo que produce saltos de potencia de MW en milisegundos.

## Fundamento teórico
Dos rasgos clave para el sistema de energía:
- **Pulsos sincronizados**: el paralelismo de un entrenamiento hace que las GPUs cambien de estado
  coordinadamente → la demanda agregada salta como un escalón, no de forma suave.
- **Comportamiento de potencia constante**: cada servidor, vía su POL, es una
  [[carga-potencia-constante-cpl|CPL]] en el bus DC.
El escalón de potencia \( \Delta P \) impacta:
- En **frecuencia** (lado AC): impone un RoCoF inicial \( \dfrac{df}{dt}\approx \dfrac{\Delta P\,f_0}{2HS} \),
  que el soporte inercial del BESS ([[vsm-inercia]]) debe limitar.
- En **tensión de bus DC**: hundimiento transitorio que el condensador de bus amortigua, y riesgo
  de inestabilidad si la potencia supera la crítica del filtro ([[estabilidad-bus-dc-cpl]]).

<div class="cfig"><img src="figuras/carga-pulsante-datacenter-ia-impacto.png" alt="escalon de potencia de un data center de IA y su impacto en frecuencia"><div class="cap">La carga de IA salta como un escalón sincronizado (miles de GPUs entran a un job a la vez). Ese $\Delta P$ impone un RoCoF inicial $\approx\Delta P f_0/(2HS)$ y una caída de frecuencia que el soporte inercial del BESS debe limitar; en el bus DC produce un hundimiento que amortigua el condensador. Es el caso de diseño más exigente.</div></div>

## Cuándo y por qué se usa
Para dimensionar la generación/almacenamiento y el control de la microrred del data center: la
carga pulsante es el caso de diseño más exigente (peor que una carga suave de igual potencia media).

## Procedimiento (genérico)
1. Caracteriza el perfil: potencia media, amplitud del pulso \( \Delta P \), tiempo de subida.
2. Modela el pulso como escalón (peor caso) en P (CPL).
3. Evalúa el impacto en frecuencia (RoCoF, nadir) y en el bus DC (hundimiento, estabilidad).
4. Dimensiona inercia/almacenamiento (AC) y condensador de bus (DC) para los límites admisibles.

## Ejemplo de código
```python
# pico de carga IA como escalon de potencia
P_cpl = lambda t: 100e3 if t < 0.1 else 230e3      # arranque de un job de entrenamiento
```

## Parámetros y valores típicos
Pods de IA de 100 kW–varios MW; saltos \( \Delta P \) de decenas a cientos de kW en ms; RoCoF
admisible de red típico ≈ 0.5–1 Hz/s.

## Errores comunes
- Dimensionar por potencia media e ignorar los pulsos (subdimensiona inercia y bus).
- Tratar la carga como suave: el escalón sincronizado es mucho más exigente.

## Uso en proyectos
- **03 - DataCenter-IA**: un escalón de 100→230 kW se usa como caso de diseño; el soporte inercial
  del BESS limita el RoCoF y el condensador de bus el hundimiento de \( V_{dc} \).

## Conceptos relacionados
- [[carga-potencia-constante-cpl]] · [[vsm-inercia]] · [[estabilidad-bus-dc-cpl]]

## Referencias
- Informes de operadores de red sobre integración de data centers (2024-2025).
