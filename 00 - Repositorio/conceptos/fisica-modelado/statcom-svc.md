---
titulo: STATCOM y SVC (compensación de reactiva)
slug: statcom-svc
categoria: fisica-modelado
tipo: concepto
nivel: intermedio
proyectos: []
objetivos: [soportar tensión de red inyectando/absorbiendo reactiva, comparar fuente de corriente vs susceptancia]
tags: [statcom, svc, facts, reactiva, soporte-tension, tcr, tsc, vsc, modelado]
fecha_creacion: 2026-06-10
fecha_actualizacion: 2026-07-02
relacionados: [convertidor-vsc, servicios-red-soporte, transferencia-potencia-linea, potencia-instantanea-dq, fault-ride-through, droop-control]
referencias:
  - "Hingorani, Gyugyi, Understanding FACTS, IEEE Press 2000"
  - "Yazdani, Iravani, Voltage-Sourced Converters in Power Systems, Wiley 2010"
---

## Definición
Dispositivos **FACTS** en derivación (shunt) que inyectan o absorben **potencia reactiva** para sostener
la tensión de un nudo. El **SVC** lo hace variando una **susceptancia** (tiristores: TCR + TSC); el
**STATCOM** es un [[convertidor-vsc|VSC]] que actúa como **fuente de corriente reactiva** controlada.

## Fundamento teórico
La tensión de un nudo depende de la reactiva inyectada \( \Delta V\approx X_{th}\,\Delta Q/V \): inyectar
\( Q>0 \) **sube** la tensión, absorber \( Q<0 \) la baja. La diferencia clave entre ambos está en cómo
escala su capacidad con la tensión:

- **SVC** = susceptancia controlable \( B \). La reactiva es \( Q=B\,V^2 \): cuando más la necesitas
  (hueco de tensión) **menos das**, porque \( Q\propto V^2 \). Genera armónicos (TCR) → necesita filtros.
- **STATCOM** = fuente de corriente. \( Q=V\,I_q \) con \( I_q \) acotada por el convertidor: mantiene
  **corriente nominal aun con \( V \) baja**, así que su soporte cae solo \( \propto V \) (mucho mejor en
  defecto). Respuesta en ms y huella menor.

| | SVC | STATCOM |
|---|---|---|
| Elemento | susceptancia (TCR/TSC) | VSC (fuente de corriente) |
| \( Q \) a tensión baja | \( \propto V^2 \) (se hunde) | \( \propto V \) (se mantiene) |
| Velocidad | ~1–2 ciclos (20–40 ms) | sub-ciclo (<5 ms) |
| Armónicos | sí (filtros pasivos) | bajos (PWM + LCL) |

El control del STATCOM es un lazo de corriente en [[potencia-instantanea-dq|dq]] con \( i_d^\*\approx0 \)
(solo lo justo para pérdidas y bus DC) e \( i_q^\* \) saliendo de un lazo de tensión AC, a menudo con
**[[droop-control|droop]] Q-V** para repartir entre varios equipos.

<div class="cfig"><img src="figuras/statcom-svc-qv.png" alt="reactiva disponible frente a tension para SVC y STATCOM"><div class="cap">Reactiva disponible frente a la tensión: el SVC es una susceptancia, así que su $Q\propto V^2$ se hunde justo cuando más falta (en el hueco); el STATCOM es una fuente de corriente, mantiene $I_q$ y su soporte cae solo $\propto V$. Por eso el STATCOM es muy superior para sostener tensión durante un defecto.</div></div>

## 1 — La reactiva del STATCOM \( Q=\dfrac{V(E-V)}{X} \) y por qué fija la tensión

**Paso 1 — el circuito.** El STATCOM es un [[convertidor-vsc|VSC]] que impone su tensión \( E\angle\delta \) tras la reactancia de acoplamiento \( X \) (filtro + trafo) hacia el nudo de red \( V\angle 0 \). La corriente es \( \bar I=(\bar E-\bar V)/(jX) \).

**Paso 2 — intercambio puramente reactivo.** Para no intercambiar potencia activa con la red (el STATCOM no tiene fuente DC, solo un condensador), el control mantiene \( E \) **en fase** con \( V \): \( \delta\approx 0 \). Con \( \bar E=E\angle 0 \) y \( \bar V=V\angle 0 \), ambos reales, la corriente es puramente imaginaria:

$$ \bar I=\frac{E-V}{jX}=-j\,\frac{E-V}{X} $$

**Paso 3 — potencia compleja en el nudo de red.** \( S=\bar V\,\bar I^\* \):

$$ S=V\cdot\left(-j\,\frac{E-V}{X}\right)^{\!\*}=V\cdot\left(+j\,\frac{E-V}{X}\right)=j\,\frac{V(E-V)}{X} $$

Es imaginaria pura: \( P=0 \) (consistente con \( \delta=0 \)) y toda la potencia es reactiva:

$$ \boxed{\;Q=\frac{V(E-V)}{X}\;} $$

**Paso 4 — el modo de operación.** El signo lo fija la diferencia de módulos:
- \( E>V \): \( Q>0 \), el STATCOM **inyecta** reactiva (modo capacitivo) y **sube** la tensión del nudo.
- \( E<V \): \( Q<0 \), **absorbe** reactiva (inductivo) y la baja.

El control solo tiene que ajustar la amplitud \( E \) de la moduladora respecto a \( V \) para fijar \( Q \). Ejemplo: \( V=1.0 \), \( E=1.05 \), \( X=0.2 \) p.u. → \( Q=1.0(1.05-1.0)/0.2=0.25 \) p.u. inyectada. Esto explica por qué su soporte cae solo \( \propto V \): la corriente \( I_q=(E-V)/X \) se acota al límite del convertidor, y \( Q=V I_q \) baja linealmente con \( V \), mientras que el SVC (susceptancia \( B \)) da \( Q=BV^2 \), que se hunde con el cuadrado en el hueco.

## 2 — El SVC: banco de condensadores fijos más reactor controlado por tiristor

El SVC combina dos elementos en paralelo conectados al nudo de red:

**TCR (Thyristor Controlled Reactor).** Un reactor de inductancia \( L \) en serie con un par de tiristores. El ángulo de disparo \( \alpha \) controla el porcentaje del semiciclo en que conduce el tiristor, variando la corriente eficaz por el reactor y por tanto la susceptancia inductiva efectiva:

$$ B_{TCR}(\alpha) = \frac{1}{\omega_0 L}\,\frac{2(\pi-\alpha)+\sin 2\alpha}{\pi}, \qquad \alpha\in[90°,180°] $$

Con \( \alpha=90° \) el TCR conduce el ciclo completo (máxima inductancia efectiva); con \( \alpha=180° \) no conduce.

**TSC (Thyristor Switched Capacitor).** Bancos de condensadores conmutados enteros (sin control continuo) mediante tiristores. Proporcionan escalones discretos de reactiva capacitiva.

**La característica V-I del SVC.** La combinación TCR+TSC produce una susceptancia resultante \( B_{SVC}=B_{TSC}-B_{TCR}(\alpha) \) variable. La reactiva entregada al nudo es:

$$ Q_{SVC} = B_{SVC}\,V^2 $$

Esta dependencia cuadrática con la tensión es la debilidad fundamental del SVC: durante un hueco de 15 % (\( V=0{,}85\,\text{pu} \)), la reactiva disponible cae a \( 0{,}85^2=72\,\% \) de su valor nominal. Además el TCR genera armónicos de orden \( 6k\pm1 \) que requieren filtros pasivos sintonizados.

## 3 — El STATCOM como VSC: diferencia con el SVC

El STATCOM reemplaza todo el SVC por un VSC con su condensador de bus DC. Las diferencias esenciales son:

**Fuente de corriente vs susceptancia.** El STATCOM impone \( I_q \) directamente mediante el lazo de corriente; la tensión del nudo y la corriente son independientes en el sentido de que el convertidor puede mantener \( I_q=I_{max} \) incluso si \( V \) cae a 0,5 pu. El SVC no puede: su corriente es \( I=B\,V \) y cae proporcional a \( V \).

**Operación en cualquier punto del plano P-Q.** Con \( i_d^\*\ne 0 \), el STATCOM puede intercambiar potencia activa si dispone de almacenamiento (baterías, supercondensadores) en el bus DC. El SVC es estrictamente reactivo.

**Sin armónicos de baja frecuencia.** La modulación PWM solo genera armónicos alrededor de \( f_{sw} \) y sus múltiplos, fáciles de filtrar con un pequeño LCL. El TCR del SVC produce 5º, 7º, 11º, 13º… que requieren filtros pasivos pesados.

**Respuesta dinámica.** El STATCOM puede cambiar \( I_q \) en menos de un ciclo (tiempo de respuesta \( <5\,\text{ms} \)) porque el lazo de corriente tiene ancho de banda de cientos de Hz. El SVC necesita calcular el siguiente ángulo de disparo, lo que introduce un retardo mínimo de medio ciclo (10 ms a 50 Hz).

## 4 — El control del STATCOM: lazo de tensión AC → \( i_q^\* \)

El control sigue la misma estructura en cascada que cualquier VSC, pero con el objetivo en el eje \( q \):

**Lazo externo: tensión AC en el PCC → referencia \( i_q^\* \).**

$$ i_q^\*(s) = \underbrace{\left(K_p + \frac{K_i}{s}\right)}_{\text{PI}} (V_{pcc}^\* - V_{pcc}) + i_{q,droop} $$

El término de droop Q-V distribuye la reactiva entre varios STATCOM en paralelo: \( i_{q,droop} = (V_{pcc}^\* - V_{pcc})/m_{droop} \). Un droop del 2–5 % asegura un reparto estable sin hunting.

**Lazo interno: corriente dq → tensión moduladora.** Idéntico al VSC inversor con desacoplo \( \omega_0 L \). El eje \( d \) se controla con \( i_d^\*\approx0 \) (solo las pérdidas del convertidor y el control del bus DC interno).

**Prioridad de corriente en FRT.** Durante un hueco de tensión, el código de red exige prioridad de inyección de reactiva sobre la activa. La lógica de saturación aplica:

$$ |i_q^\*| \leq I_{max}, \qquad |i_d^\*| \leq \sqrt{I_{max}^2 - i_q^{*2}} $$

<div class="cfig"><img src="figuras/statcom-svc-analisis.png" alt="topologia, caracteristica V-I, respuesta y control del STATCOM"><div class="cap">Cuatro paneles: (a) topología comparada SVC (TCR+TSC) vs STATCOM (VSC+Cdc); (b) característica V-I mostrando el soporte cuadrático del SVC contra el lineal del STATCOM; (c) respuesta Vpcc(t) ante un hueco de 100 ms, el STATCOM recupera la tensión en menos de un ciclo; (d) diagrama de control en cascada del STATCOM (Vpcc → iq* → vq*).</div></div>

## 5 — La respuesta dinámica: STATCOM en un ciclo, SVC en 3–5 ciclos

La diferencia de velocidad de respuesta tiene consecuencias directas en el cumplimiento del código FRT:

**SVC — retardo de disparo.** El ángulo de disparo \( \alpha \) del TCR solo puede cambiarse en cada cruce por cero de la tensión (cada 3,33 ms a 50 Hz en el TCR trifásico). Para un cambio grande de \( B \) se necesitan 1–3 ciclos completos para alcanzar el nuevo régimen, más el retardo de la medición y el regulador. El tiempo de respuesta efectivo es **20–40 ms**.

**STATCOM — control en tiempo continuo.** El lazo de corriente dq opera a la frecuencia de muestreo (típicamente \( f_{sw}/2 \) o superior). Un cambio en \( i_q^\* \) se ejecuta en el siguiente período de conmutación (\( 100\,\mu\text{s} \) para \( f_{sw}=10\,\text{kHz} \)), y la corriente alcanza su nuevo valor en \( 1\text{–}3\,\text{ms} \) (un tiempo de lazo de corriente). El tiempo de respuesta efectivo es **1–5 ms**.

**Consecuencia en FRT.** Un código típico exige \( Q_{inyectada} \geq 2\,(1-V)\,I_n \) dentro de los primeros **20 ms** del hueco. El STATCOM lo cumple con holgura; el SVC llega al límite o lo incumple dependiendo del pre-carga del banco.

**Banco fijo de condensadores.** No responde en absoluto: \( Q=B_{fijo}\,V^2 \). Útil para corrección de FP estática pero inútil para soporte dinámico.

## 6 — Diseño iterativo: STATCOM 50 MVAr para soporte de tensión en nudo débil

**Datos del nudo:**
- Tensión nominal: \( V_n = 33\,\text{kV} \)
- Reactancia de Thévenin: \( X_{th} = 3\,\Omega \) (equivalente a \( 0{,}28\,\text{pu} \) en base 33 kV, 100 MVA)
- Hueco máximo a cubrir: \( \Delta V = 0{,}10\,\text{pu} \) (de 1.0 a 0.90 pu)
- Tiempo de respuesta exigido: \( <20\,\text{ms} \) (código FRT)

**Paso 1 — reactiva necesaria para recuperar la tensión.**

$$ \Delta Q = \frac{\Delta V \cdot V_{pcc}}{X_{th}} = \frac{0{,}10 \times 0{,}90}{0{,}28} \approx 0{,}32\,\text{pu} \rightarrow 32\,\text{MVAr} $$

Se elige **50 MVAr** con margen del 56 % para cubrir variaciones de \( X_{th} \) y contingencias adicionales.

**Paso 2 — corriente nominal del STATCOM.**

$$ I_n = \frac{Q_n}{\sqrt{3}\,V_n} = \frac{50\times10^6}{\sqrt{3}\times33\,000} = 875\,\text{A} $$

**Paso 3 — tensión del bus DC.** Para modular linealmente con margen:

$$ V_{dc} = \frac{2\sqrt{2}\,V_{n,fase}}{m_a} = \frac{2\sqrt{2}\times19\,050}{0{,}9} \approx 60\,\text{kV} $$

En la práctica se usa un trafo elevador y el STATCOM trabaja a tensiones intermedias (3–6 kV) con transformador de acoplamiento hasta 33 kV.

**Paso 4 — lazo de corriente.** Con \( L_{coupling}=1\,\text{mH} \), \( \alpha_c=2\pi\times500\,\text{rad/s} \):

$$ K_{p,i} = \alpha_c\,L = 3\,140 \times 10^{-3} = 3{,}14\,\text{V/A} $$

**Paso 5 — lazo de tensión con droop.**
Droop \( m_d=0{,}03 \) (3 %): el STATCOM empieza a inyectar cuando \( V<1\,\text{pu} \) y llega a \( I_n \) cuando \( V=0{,}97\,\text{pu} \).

$$ K_{p,v} = \frac{I_n}{\Delta V_{droop}} = \frac{875}{0{,}03\times33\,000/\sqrt{3}} = 1{,}63\,\text{A/V} $$

**Verificación dinámica:**
- El lazo de corriente tiene tiempo de respuesta \( \approx 3/\alpha_c = 0{,}95\,\text{ms} \).
- El lazo de tensión tiene tiempo de respuesta \( \approx 15\,\text{ms} \) (BW \( \approx 20\,\text{Hz} \)).
- Total: \( \approx 16\,\text{ms} \) → cumple el criterio de 20 ms.

**Comparativa SVC vs STATCOM a tensión de hueco (\( V=0{,}85\,\text{pu} \)):**

| Parámetro | SVC 50 MVAr | STATCOM 50 MVAr |
|---|---|---|
| \( Q \) disponible | \( 50\times0{,}85^2=36{,}1\,\text{MVAr} \) | \( 50\times0{,}85=42{,}5\,\text{MVAr} \) |
| Tiempo respuesta | 20–40 ms | <5 ms |
| Cumple FRT | Límite | Holgado |

## Cuándo y por qué se usa
Soporte de tensión en puntos débiles, cumplimiento de **[[fault-ride-through|FRT]]** (inyección de reactiva
durante huecos exigida por código), reducción de flícker, y compensación dinámica en parques renovables.
El STATCOM se prefiere cuando se necesita soporte **durante** el defecto (tensión baja) o respuesta muy rápida.

## Ejemplo de código
```python
def statcom_iq_ref(v_meas, v_ref, droop, iq_max):
    # lazo Q-V con droop; satura a corriente reactiva maxima del VSC
    iq = (v_ref - v_meas) / droop          # +iq inyecta reactiva (sube V)
    return max(-iq_max, min(iq, iq_max))
```

## Errores comunes
- Dimensionar el STATCOM por MVAr a tensión nominal y olvidar que en FRT lo que limita es la **corriente**.
- Usar SVC donde se exige soporte a tensión muy baja (su Q se hunde con \( V^2 \)).
- Olvidar la prioridad \( i_q>i_d \) durante el hueco → no cumple el código FRT.
- Droop Q-V demasiado pequeño entre varios equipos → reparto inestable / hunting.
- Condensador de bus DC subdimensionado: con poco \( C_{dc} \), la tensión del bus oscila con la reactiva inyectada y desestabiliza el lazo.

## Conceptos relacionados
- [[convertidor-vsc]] · [[servicios-red-soporte]] · [[fault-ride-through]] · [[transferencia-potencia-linea]] · [[droop-control]] · [[filtro-lcl]] · [[potencia-instantanea-dq]]

## Referencias
- Hingorani, Gyugyi, *Understanding FACTS*, 2000.
- Yazdani, Iravani, *Voltage-Sourced Converters in Power Systems*, 2010.
