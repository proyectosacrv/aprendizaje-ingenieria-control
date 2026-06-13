---
titulo: Estabilidad por impedancia (Nyquist generalizado)
slug: impedancia-salida-estabilidad
categoria: control
tipo: metodo
nivel: avanzado
proyectos: [01-GFM-Impedance, 02-GFL-Impedance, 03-DataCenter-IA]
objetivos: [evaluar estabilidad inversor-red sin re-simular todo]
tags: [impedancia, nyquist, dq, red-debil, SCR, oscilaciones-subsincronas]
fecha_creacion: 2026-06-08
fecha_actualizacion: 2026-06-08
relacionados: [respuesta-frecuencia-ss, red-thevenin-scr, medicion-impedancia-inyeccion, analisis-modal]
referencias:
  - "Sun, Impedance-Based Stability Criterion for Grid-Connected Inverters, IEEE TPEL 2011"
  - "Wang, Blaabjerg, Harmonic Stability in Power-Electronic-Based Power Systems, IEEE TPEL 2019"
---

## Definición
Criterio que decide la estabilidad de la interacción **inversor–red** comparando sus
impedancias, sin reconstruir el modelo completo cada vez. En dq es un sistema MIMO 2×2, así que
se usa el **Nyquist generalizado** (sobre los autovalores de la matriz de retorno).

## Fundamento teórico
Inversor como admitancia de salida \( Y_{inv}(s) \) (2×2), red como impedancia
\( Z_{red}(s) \). El *minor loop gain* es:
$$ \mathbf{L}(s)=\mathbf{Z}_{red}(s)\,\mathbf{Y}_{inv}(s) $$
Si inversor y red son estables por separado, el conjunto es estable **si y solo si** los
autovalores de \( \mathbf{L}(j\omega) \) **no rodean −1** (Nyquist generalizado). Equivale a
exigir que \( \det(\mathbf{I}+\mathbf{L}(s)) \) no tenga ceros en el semiplano derecho.

<div class="cfig"><img src="figuras/impedancia-salida-estabilidad-cruce.png" alt="cruce de magnitudes de impedancia inversor y red"><div class="cap">Criterio de impedancia visto en magnitud: la estabilidad se juega en la frecuencia donde $|Z_{red}|$ corta a $|Z_{inv}|$. Una red débil (SCR bajo) sube $|Z_{red}|$ y mueve el cruce a frecuencias donde el margen de fase del cociente $Z_{red}/Z_{inv}$ puede ser insuficiente; el criterio exacto es el Nyquist generalizado de sus autovalores.</div></div>

## Cuándo y por qué se usa
Integración masiva de inversores, oscilaciones subsíncronas, redes débiles. Permite barrer la
fortaleza de red (SCR) y hallar el **SCR crítico** de inestabilidad de forma modular.

## Procedimiento de diseño (genérico)
1. Obtén \( Y_{inv}(j\omega) \) del inversor (ver [[respuesta-frecuencia-ss]] o
   [[medicion-impedancia-inyeccion]]).
2. Modela \( Z_{red}(j\omega) \) según SCR y X/R (ver [[red-thevenin-scr]]).
3. Calcula \( \mathbf{L}=Z_{red}Y_{inv} \) y sus autovalores en frecuencia.
4. Aplica Nyquist generalizado: ¿rodean −1? Barre SCR hasta el crítico.
5. **Valida** contra los autovalores del modelo acoplado (deben coincidir).

## Ejemplo de código
```python
# autovalores del minor loop gain en cada frecuencia
for k, f in enumerate(freqs):
    s = 2j*np.pi*f
    G = C @ np.linalg.solve(s*np.eye(n) - A, B) + D
    Yinv = -G
    Zg = np.array([[Rg+s*Lg, -w0*Lg], [w0*Lg, Rg+s*Lg]])
    lam[k] = np.linalg.eigvals(Zg @ Yinv)   # no deben rodear -1
```

## Parámetros y valores típicos
SCR crítico depende del control. Grid-following: inestable en red débil (SCR bajo). Grid-forming
agresivo: inestable en red fuerte (SCR alto).

## Errores comunes
- Confundir el signo: \( Y_{inv}=-\partial i_g/\partial v_{pcc} \) (convención de fuente).
- Aplicar el Nyquist SISO a un sistema dq acoplado → hay que usar el generalizado (autovalores
  de la matriz 2×2).
- Olvidar validar contra el modelo acoplado.

## Uso en proyectos
- **01 - GFM-Impedance** (objetivo: estabilidad en red): SCR crítico por Nyquist = **3.39** y
  por autovalores del modelo acoplado = **3.35** (diferencia 1.3%). En `main_phase3.py`.

## Conceptos relacionados
- [[respuesta-frecuencia-ss]] · [[red-thevenin-scr]] · [[medicion-impedancia-inyeccion]] · [[analisis-modal]]

## Referencias
- Sun, IEEE TPEL 2011 · Wang, Blaabjerg, IEEE TPEL 2019.
