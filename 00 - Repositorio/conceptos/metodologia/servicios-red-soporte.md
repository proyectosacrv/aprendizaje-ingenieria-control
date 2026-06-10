---
titulo: Servicios de red y soporte de la red (grid services)
slug: servicios-red-soporte
categoria: metodologia
tipo: concepto
nivel: intermedio
proyectos: []
objetivos: [conocer los servicios auxiliares que un convertidor puede prestar a la red]
tags: [servicios-red, inercia, ffr, p-f, q-v, ancillary, grid-code, intermedio]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-09
relacionados: [vsm-inercia, droop-control, fault-ride-through, ecuacion-oscilacion, grid-forming-vs-following]
referencias:
  - "ENTSO-E, Network Codes (RfG, HVDC)"
  - "Milano et al., Foundations and Challenges of Low-Inertia Systems, PSCC 2018"
---

## Definición
Conjunto de **servicios auxiliares** (ancillary services) que un convertidor presta para mantener
la calidad y estabilidad de la red: respuesta de frecuencia, soporte de tensión/reactiva, inercia
sintética y soporte en falta. Cada vez más exigidos por los grid codes a renovables.

## Fundamento teórico
- **Respuesta inercial (sintética):** entregar potencia proporcional a la derivada de frecuencia,
  emulando inercia (ver [[vsm-inercia]], [[ecuacion-oscilacion]]):
  $$ \Delta P_{iner}=-2H_{v}\frac{d f}{dt} $$
- **Respuesta rápida de frecuencia (FFR) y regulación primaria (droop P-f):**
  $$ \Delta P = -\frac{1}{R}\,\Delta f $$
  con estatismo \( R \) (típ. 2–5 %), banda muerta y saturación; reserva activa o almacenamiento.
- **Soporte de tensión (droop Q-V):** \( \Delta Q=-\dfrac{1}{R_v}\Delta V \); regula reactiva para
  sostener tensión, dentro del diagrama P-Q del convertidor.
- **Modos de factor de potencia / Q(P) / Q(V):** según consigna o normativa.
- **Soporte en falta:** inyección de reactiva durante huecos ([[fault-ride-through]]).
- **Calidad:** compensación de armónicos/desequilibrio (filtro activo).

Distinción clave: grid-following **sigue** la red y modula corriente para estos servicios;
grid-forming **forma** tensión/frecuencia y aporta inercia y soporte de forma intrínseca (ver
[[grid-forming-vs-following]]). En **redes de baja inercia** estos servicios pasan de opcionales a
imprescindibles.

## Cuándo y por qué se usa
En el diseño del nivel superior de control de cualquier convertidor de red moderno: define qué
referencias de P y Q recibe el control de corriente y cómo responde a \( f \) y \( V \). Es donde
se traducen los requisitos del grid code a lazos concretos.

## Procedimiento de diseño (genérico)
1. Lista los servicios exigidos por el grid code y el mercado (inercia, FFR, droop, Q-V, FRT).
2. Asigna reservas (margen de P, capacidad de Q, almacenamiento) en el diagrama P-Q.
3. Implementa cada lazo: droop con banda muerta y saturación, inercia con filtro de \( df/dt \).
4. Coordina prioridades y límites (corriente, térmico) y la jerarquía ([[control-jerarquico-microrred]]).
5. Verifica respuesta temporal frente a eventos normativos.

## Ejemplo de código
```python
def primary_response(f, V, f0=50.0, R=0.04, Rv=0.05, Pmax=1.0, Qmax=0.6):
    dP = -(1/R)*(f - f0)/f0              # droop P-f (p.u.)
    dQ = -(1/Rv)*(V - 1.0)              # droop Q-V (p.u.)
    return max(min(dP, Pmax), -Pmax), max(min(dQ, Qmax), -Qmax)
```

## Parámetros y valores típicos
Estatismo P-f \( R \) 2–5 %; banda muerta ±10–20 mHz; \( H_v \) 2–6 s; respuesta FFR < 1–2 s;
soporte de reactiva hasta 0.3–0.5 p.u. de Q.

## Errores comunes
- Pedir inercia sintética sin **reserva** de energía (no hay potencia que entregar).
- Droop sin banda muerta → actuación continua por ruido de frecuencia.
- Ignorar el acoplamiento P-f / Q-V en redes con relación X/R baja (distribución).

## Conceptos relacionados
- [[vsm-inercia]] · [[droop-control]] · [[fault-ride-through]] · [[ecuacion-oscilacion]] · [[grid-forming-vs-following]]

## Referencias
- ENTSO-E, *Network Codes (RfG, HVDC)*.
- Milano et al., *Foundations and Challenges of Low-Inertia Systems*, PSCC 2018.
