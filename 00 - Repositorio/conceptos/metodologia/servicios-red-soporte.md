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

## 3 — Regulación primaria y reserva de frecuencia

El **gobernador convencional** de una turbina de vapor o hidráulica responde al desvío de frecuencia en 10–30 s, activando o reduciendo mecánicamente la potencia del generador síncrono. Esta velocidad de respuesta fue suficiente cuando la red tenía alta inercia; en redes de baja inercia con alta penetración renovable, el nadir de frecuencia ocurre antes de que el gobernador haya actuado.

Los **inversores renovables** pueden proporcionar FFR (Fast Frequency Response) en menos de 1 s, e inercia sintética prácticamente instantánea (< 100 ms). La diferencia fundamental es que el inversor actúa sobre una señal eléctrica medida, sin partes mecánicas que limiten la velocidad de respuesta.

El droop de frecuencia para inversores se expresa como:

$$ \Delta P = -\frac{1}{R_f} \Delta f $$

donde \( R_f \) es el estatismo en %/Hz (o en pu/pu). Un \( R_f = 4\,\% \) significa que una caída de 2 Hz (4 % de 50 Hz) activa el 100 % de la reserva disponible.

**Dead band:** la respuesta de frecuencia tiene una zona muerta de \( |\Delta f| < 20\,\text{mHz} \) (valor típico en Europa según el código de red ENTSO-E) para evitar que el ruido de medida de la frecuencia excite continuamente el lazo de droop. Por encima de la dead band, la respuesta es lineal hasta la saturación.

## 4 — Soporte de tensión y potencia reactiva

La **inyección de corriente reactiva** durante huecos de tensión es obligatoria en muchos países desde la entrada en vigor del reglamento RfG (Requirements for Generators) de ENTSO-E en 2019. La regla básica establece:

$$ \Delta I_q = k \cdot (1 - V_{meas}) \cdot I_n $$

donde \( k \geq 2 \) (ganancia de soporte de tensión), \( V_{meas} \) es la tensión medida en pu y \( I_n \) la corriente nominal. Esta inyección de reactiva ayuda a sostener la tensión durante el hueco y facilita la recuperación.

La **curva Q(V)** define el soporte estático de tensión en condiciones normales de operación:

$$ Q = k_v(V_{ref} - V_{meas}) $$

con dead band centrada en \( V_{ref} = 1\,\text{pu} \) y saturación en \( Q_{max} \).

El **STATCOM** es el dispositivo dedicado al soporte de reactiva: responde en menos de 10 ms, sin inercia ni almacenamiento de energía, actuando como fuente de corriente reactiva pura. Su ventaja frente al SVC clásico (banco de condensadores conmutado) es la respuesta continua y sin inercia (ver [[statcom-svc]]).

**Límite P-Q del inversor:** la zona de operación en el plano P-Q está limitada por la corriente máxima del convertidor \( I_{max} \) (círculo de radio \( V \cdot I_{max} \)) y por los límites de tensión DC. Durante un hueco, si se prioriza la corriente reactiva, la corriente activa disponible se reduce: \( i_d^{max} = \sqrt{I_{max}^2 - (i_q^*)^2} \).

## 5 — Servicios de balance de energía

Los mercados europeos de servicios de balance se estructuran en tres productos con distintas velocidades de activación:

**FCR (Frequency Containment Reserve):** primera defensa ante desvíos de frecuencia. Se activa automáticamente en segundos, es simétrica (carga y descarga) y la reserva es proporcional a la desviación de frecuencia. Es el equivalente de mercado al droop primario. Precio típico en Europa: 10–50 €/MW/h.

**aFRR (automatic Frequency Restoration Reserve):** restaura la frecuencia a 50 Hz después de que la FCR la ha contenido. Tiempo de activación completa < 30 s. Es equivalente al nivel secundario del control jerárquico. Precio: hasta 100 €/MW/h en periodos de escasez.

**mFRR (manual Frequency Restoration Reserve):** reserva de reemplazo activada manualmente por el TSO (Transmission System Operator) para restaurar la FCR. Tiempo de activación de minutos. Se subasta en el mercado de balance intradiario.

Para los BESS, la FCR y la aFRR son los productos más atractivos porque requieren mucha potencia durante segundos–minutos, y los BESS tienen tiempos de respuesta muy inferiores a los requeridos, dándoles una ventaja competitiva sobre las centrales térmicas.

## 6 — Mercados y regulación

**ENTSO-E** (European Network of Transmission System Operators for Electricity) define los códigos de red europeos que regulan cómo los generadores deben conectarse y qué servicios deben prestar: RfG (*Requirements for Generators*), DCC (*Demand Connection Code*), HVDC (*High Voltage Direct Current Guidelines*). Son vinculantes para todos los estados miembro de la UE.

**REE (Red Eléctrica de España)** opera el sistema de transmisión español e integra los mercados de balance bajo las directrices de ENTSO-E. El **CECRE** (Centro de Control de Energías Renovables) monitoriza y controla en tiempo real la generación eólica y fotovoltaica, pudiendo ordenar reducciones de potencia si la estabilidad del sistema lo requiere.

**Informe de adecuación:** los TSO publican anualmente un informe verificando que hay suficiente capacidad de reserva (FCR, aFRR, mFRR) para todas las condiciones operativas previstas. Es la base para decidir si se necesitan nuevas inversiones en almacenamiento o interconexiones.

**Tendencia:** la participación de recursos distribuidos (BESS residenciales, cargadores de VE, demanda flexible industrial) en los mercados de servicios ancillary está creciendo rápidamente a través de agregadores virtuales (VPP, *Virtual Power Plants*). El reto regulatorio es diseñar mercados que valoren adecuadamente la velocidad de respuesta, no solo la energía.

<div class="cfig"><img src="../figuras/servicios-red-soporte-analisis.png" alt="Servicios de red: respuesta de frecuencia por etapas, curva Q(V), diagrama P-Q del inversor y precios de mercado FCR/aFRR"><div class="cap">Cuatro paneles: desglose de la respuesta de frecuencia en inercia sintética, FFR y FCR; curva Q(V) con dead band para soporte de tensión local; zona de operación P-Q del inversor limitada por corriente máxima; precio horario típico de los servicios FCR y aFRR en el mercado europeo de balance.</div></div>

## Conceptos relacionados
- [[vsm-inercia]] · [[droop-control]] · [[fault-ride-through]] · [[ecuacion-oscilacion]] · [[grid-forming-vs-following]]

## Referencias
- ENTSO-E, *Network Codes (RfG, HVDC)*.
- Milano et al., *Foundations and Challenges of Low-Inertia Systems*, PSCC 2018.
