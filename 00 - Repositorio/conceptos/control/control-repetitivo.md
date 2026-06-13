---
titulo: Control repetitivo
slug: control-repetitivo
categoria: control
tipo: tecnica
nivel: avanzado
proyectos: []
objetivos: [anular errores periódicos rechazando todos los armónicos de una frecuencia]
tags: [repetitivo, periodico, armonicos, modelo-interno, plug-in, thd, avanzado]
fecha_creacion: 2026-06-09
fecha_actualizacion: 2026-06-09
relacionados: [controlador-resonante, controlador-pid, discretizacion-controladores, error-regimen-permanente, fft-analisis-espectral]
referencias:
  - "Hara et al., Repetitive Control System: A New Type Servo System for Periodic Exogenous Signals, IEEE TAC 1988"
  - "Zhou, Wang, Digital Repetitive Controlled PWM Inverter, IEEE TIE 2003"
---

## Definición
Controlador basado en el **principio del modelo interno** para señales **periódicas**: incorpora un
generador de periodo \( T \) (un retardo realimentado) que da ganancia infinita a la fundamental y
**todos sus armónicos** a la vez, anulando el error periódico en régimen permanente.

## Fundamento teórico
El modelo interno de una señal periódica de periodo \( T \) es el generador
$$ G_{rc}(s)=\frac{e^{-sT}}{1-e^{-sT}} $$
cuyos polos están en \( s=j\,k\,\frac{2\pi}{T} \) (la fundamental \( \omega_0=2\pi/T \) y **todos**
los armónicos \( k\omega_0 \)) → ganancia infinita en cada uno. Equivale a infinitos
[[controlador-resonante|resonantes]] en paralelo con un solo retardo. En **discreto** con \( N=T/T_s \)
muestras por periodo:
$$ C_{rc}(z)=\frac{z^{-N}}{1-Q(z)\,z^{-N}}\,k_r\,z^{m}\,F(z) $$
- \( Q(z) \): filtro (ganancia \( <1 \) o pasa-bajos) que **sacrifica precisión por robustez** (sin
  él, errores de modelo a alta frecuencia desestabilizan).
- \( z^{m} \): **avance** que compensa el retardo de la planta.
- \( F(z) \): filtro de fase/estabilización; \( k_r \): ganancia de aprendizaje.

Se implementa casi siempre como **plug-in**: se añade en paralelo a un controlador realimentado
existente (PI/PR), que estabiliza y da respuesta rápida, mientras el repetitivo limpia los armónicos
periódicos ciclo a ciclo. Coste: la convergencia tarda **varios periodos** y reacciona lento a
perturbaciones no periódicas.

<div class="cfig"><img src="figuras/control-repetitivo-peine.png" alt="respuesta en magnitud del modelo interno periodico con picos en los armonicos"><div class="cap">Magnitud del modelo interno $e^{-sT}/(1-e^{-sT})$: un peine de resonancias con ganancia alta en la fundamental y en TODOS sus armónicos a la vez, con un solo retardo realimentado. Equivale a infinitos resonantes en paralelo, lo que anula el error periódico ciclo a ciclo.</div></div>

## Cuándo y por qué se usa
Cuando la perturbación/​referencia es periódica y rica en armónicos: inversores de tensión (UPS/CVCF)
con carga no lineal, filtros activos, rectificadores con rizado periódico. Da muy bajo THD con poco
coste de cómputo frente a apilar muchos resonantes.

## Procedimiento de diseño (genérico)
1. Estabiliza primero el lazo con un controlador realimentado (PI/PR).
2. Añade el repetitivo en plug-in: fija \( N=T/T_s \) (entero; ojo si \( f_0 \) varía).
3. Diseña \( Q(z) \) (pasa-bajos) para robustez a alta frecuencia.
4. Ajusta el avance \( z^{m} \) (compensa retardo de planta) y la ganancia \( k_r \).
5. Verifica estabilidad (criterio de pequeña ganancia sobre \( Q-k_r z^{m}F\hat G \)) y THD resultante.

## Ejemplo de código
```python
class Repetitive:                        # plug-in discreto
    def __init__(self, N, kr, Q=0.95): self.buf=[0.0]*N; self.kr=kr; self.Q=Q
    def step(self, err):
        u = self.Q*self.buf[0] + self.kr*err     # memoria de 1 periodo
        self.buf = self.buf[1:] + [u]
        return self.buf[0]
```

## Parámetros y valores típicos
\( Q\approx0.95\text{–}0.99 \) o pasa-bajos con corte < \( f_s/4 \). \( k_r \) 0.5–2. Convergencia
en 3–10 periodos. THD < 1–3 % alcanzable.

## Errores comunes
- \( N \) no entero o frecuencia de red variable → el repetitivo se desintoniza (usar \( N \)
  fraccional/adaptativo).
- Sin filtro \( Q \) → inestabilidad por errores de modelo a alta frecuencia.
- Usarlo solo (sin lazo estabilizante) o esperar respuesta rápida a transitorios no periódicos.

## Conceptos relacionados
- [[controlador-resonante]] · [[controlador-pid]] · [[discretizacion-controladores]] · [[error-regimen-permanente]] · [[fft-analisis-espectral]]

## Referencias
- Hara et al., *Repetitive Control System*, IEEE TAC 1988.
- Zhou, Wang, *Digital Repetitive Controlled PWM Inverter*, IEEE TIE 2003.
