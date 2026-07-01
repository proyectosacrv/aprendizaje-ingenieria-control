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
fecha_actualizacion: 2026-07-01
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

<div class="cfig"><img src="figuras/servicios-red-soporte-pf.png" alt="caracteristica droop P-f con banda muerta y saturacion"><div class="cap">Característica de la respuesta primaria de frecuencia: el convertidor ajusta su potencia activa proporcionalmente a la desviación de frecuencia, $\Delta P=-\Delta f/R$, con una banda muerta central (evita actuar por ruido) y saturación en los extremos (limitada por la reserva de energía disponible). Análogamente, el droop Q–V sostiene la tensión con reactiva.</div></div>

## 1 — Droop de frecuencia \( \Delta P = -\Delta f / R \): derivación y valores típicos
**Paso 1 — la característica droop.** El estatismo \( R \) (droop) relaciona la desviación de frecuencia con el cambio de potencia del generador/convertidor. Se define como la variación relativa de frecuencia que produce una variación del 100 % de la potencia nominal:

$$ R = \frac{\Delta f/f_0}{\Delta P/P_n} \quad\Rightarrow\quad \Delta P = -\frac{1}{R}\,\frac{\Delta f}{f_0}\,P_n $$

En notación en por unidad, con \( \Delta f \) en Hz y \( f_0=50 \) Hz, y \( \Delta P \) en p.u.:

$$ \boxed{\Delta P\,[\text{p.u.}] = -\frac{1}{R}\,\Delta f\,[\text{p.u.}]} $$

**Paso 2 — verificación numérica.** Con \( R=4\,\% \) y una caída de frecuencia de \( \Delta f=-0.5 \) Hz (que en p.u. es \( -0.5/50=-0.01 \)):

$$ \Delta P = -\frac{1}{0.04}\times(-0.01) = +0.25\,\text{p.u.} = 25\,\% \text{ de } P_n $$

El convertidor aumenta su potencia un 25 % ante una caída de 0.5 Hz: respuesta proporcional al déficit de generación.

**Paso 3 — elección de \( R \).** El estatismo \( R \) es el compromiso entre la **variación de frecuencia** permitida en régimen permanente y la **reserva activa** disponible:
- \( R \) pequeño (2 %): respuesta agresiva, poca desviación, pero requiere mucha reserva.
- \( R \) grande (8 %): respuesta moderada, mayor desviación de frecuencia permitida.
- Valor habitual: \( R=4\text{–}5\,\% \) (convención de los grupos térmicos sincronizados, adoptada por el código de red ENTSO-E para renovables).

La banda muerta (\( \pm10\text{–}20\,\text{mHz} \)) evita que el ruido de medida de frecuencia excite continuamente el lazo de droop. La saturación (\( \Delta P_{\max}=P_{\text{reserva}} \)) refleja que el convertidor no puede dar más potencia que la que tiene disponible.

## 2 — Respuesta inercial sintética: \( \Delta P = -2H\,df/dt \)
**Paso 1 — analogía con la inercia del rotor.** En una máquina síncrona, la energía cinética almacenada es \( E=\frac{1}{2}J\omega^2 \). La constante de inercia \( H=E/S_n \) (en segundos) cuantifica cuánta energía en vatios-segundo por VA nominal hay en el volante. Ante un desequilibrio \( \Delta P \), la ecuación de oscilación es:

$$ 2H\,\frac{d(\Delta f/f_0)}{dt} = \Delta P_{mec} - \Delta P_{elec} \;\Rightarrow\; \Delta P_{iner} = -2H\,\frac{d(\Delta f)}{dt}\frac{1}{f_0} $$

**Paso 2 — emulación virtual.** Un convertidor mide \( df/dt \) (con filtro para evitar ruido) y genera una referencia de potencia adicional:

$$ \boxed{\Delta P_{iner} = -2H_v\,\frac{df}{dt} \cdot \frac{1}{f_0}} $$

donde \( H_v \) es la constante de inercia virtual (típ. 2–6 s). Esta acción es más rápida que el droop (actúa en la transición, no en régimen permanente) y reduce la tasa de cambio de frecuencia (ROCOF), lo que da tiempo a la regulación primaria para actuar.

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
