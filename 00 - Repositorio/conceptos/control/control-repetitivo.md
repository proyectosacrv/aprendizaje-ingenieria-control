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
fecha_actualizacion: 2026-06-30
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

## 1 — Por qué \( 1/(1-e^{-sT}) \) rechaza la fundamental y todos sus armónicos
**Paso 1 — el principio del modelo interno.** Para anular en régimen permanente el error frente a una señal, el lazo debe contener un **generador interno** de esa señal: un bloque cuyos polos coincidan con los modos de la perturbación. En términos de control, ganancia infinita a esas frecuencias hace que el error a ellas tienda a cero (cualquier error las excitaría sin límite, lo que el lazo no permite en equilibrio). Para una constante, ese generador es el integrador \( 1/s \); para una senoide \( \omega_0 \), el resonante \( s/(s^2+\omega_0^2) \). ¿Y para una señal **periódica** cualquiera de periodo \( T \)?

**Paso 2 — el generador de periodo \( T \).** Una señal periódica de periodo \( T \) cumple \( x(t)=x(t-T) \). El bloque que "memoriza un periodo y lo realimenta" es un retardo \( e^{-sT} \) en lazo positivo:

$$ y(t)=u(t)+y(t-T)\quad\Longrightarrow\quad Y(s)=U(s)+e^{-sT}Y(s)\quad\Longrightarrow\quad \frac{Y(s)}{U(s)}=\frac{1}{1-e^{-sT}} $$

(la variante \( e^{-sT}/(1-e^{-sT}) \) solo desplaza la salida un periodo; los polos son los mismos).

**Paso 3 — localizar los polos.** Los polos están donde el denominador se anula:

$$ 1-e^{-sT}=0 \;\Rightarrow\; e^{-sT}=1 \;\Rightarrow\; -sT=j\,2\pi k,\quad k\in\mathbb{Z} $$

$$ \boxed{\;s=j\,k\,\frac{2\pi}{T}=j\,k\,\omega_0,\quad k=0,\pm1,\pm2,\dots\;} $$

Hay un polo en \( k=0 \) (la componente DC), uno en la fundamental \( \omega_0=2\pi/T \) y uno en **cada** armónico \( k\omega_0 \), todos sobre el eje imaginario.

**Paso 4 — ganancia infinita en cada armónico.** En \( s=jk\omega_0 \) el denominador \( 1-e^{-jk\omega_0 T}=1-e^{-j2\pi k}=1-1=0 \), de modo que \( |G_{rc}(jk\omega_0)|\to\infty \). El Bode es un **peine** de resonancias: un solo retardo realimentado coloca ganancia infinita en infinitas frecuencias equiespaciadas. Por eso un único bloque equivale a infinitos [[controlador-resonante|resonantes]] en paralelo (uno por armónico) pero con coste de cómputo de una sola memoria de \( N=T/T_s \) muestras.

**Paso 5 — por qué eso anula el error periódico.** Una perturbación periódica de periodo \( T \) tiene su espectro **exactamente** en \( \{k\omega_0\} \) (serie de Fourier). El modelo interno tiene ganancia infinita justo en esas frecuencias, así que el error en régimen permanente en cada armónico se anula. La contrapartida: como la corrección se construye memorizando el ciclo anterior, la convergencia tarda **varios periodos** y el bloque no ayuda frente a perturbaciones no periódicas (cuyo espectro no cae en el peine). El filtro \( Q(z)<1 \) baja la ganancia en alta frecuencia para robustez, a costa de no anular del todo los armónicos altos.

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
