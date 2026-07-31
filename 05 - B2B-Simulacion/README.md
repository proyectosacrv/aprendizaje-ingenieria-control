# Proyecto: Simulación y control del convertidor back-to-back

Modelado, control y **simulación en Scilab** de un convertidor back-to-back
(aerogenerador full-converter PMSG → bus DC → red), siguiendo la metodología de
la ficha [convertidor-back-to-back]: especificaciones → diseño iterativo de
componentes → diseño de lazos → ensayos y validación.

## Cómo ejecutar
Cada módulo es un script de Scilab autocontenido. En la consola de Scilab:

```scilab
exec('01_modulacion.sce', -1)
```

(el `-1` ejecuta sin parar pidiendo confirmación).

> Nota: el código está comentado **línea a línea** para poder entenderlo y
> revisarlo. Los números clave se cruzan además en Python para validarlos.

## Plan de módulos (roadmap)

| # | Módulo | Qué hace | Estado |
|---|--------|----------|--------|
| 1 | `01_modulacion.sce` | Modulador PWM de 2 niveles: portadora, referencias y **pulsos**. Compara **SPWM**, **3.er armónico** y **SVPWM** (min-max). | ✅ hecho |
| 2 | `02_etapa_potencia.sce` | VSC conmutado + filtro L de un lado; valida el **rizado** de corriente y el **THD** frente a lo previsto. | pendiente |
| 3 | `03_planta_lazos.sce` | Modelo **dq promediado** de la planta y diseño/validación de los **lazos** (corriente + tensión DC). | pendiente |
| 4 | `04_b2b_completo.sce` | Back-to-back completo: **MSC (PMSG+MPPT)** + bus DC + **GSC (red)**, promediado. | pendiente |
| 5 | `05_ensayos.sce` | Ensayos: escalón de potencia, hueco de red (LVRT), arranque, seguimiento MPPT, con y sin feedforward. | pendiente |
| 6 | `06_diseno_iterativo.sce` | Itera el dimensionado de componentes (**Vdc, L, C**) a partir de las especificaciones y comprueba que cumplen. | pendiente |
| — | `informe.html` | Informe del proyecto (especificaciones, diseño, ensayos, conclusiones). | pendiente |

## Parámetros del caso (del ejemplo de la ficha)
- Potencia nominal: 2 MW · Red: 690 V (línea) · Bus DC: 1150 V
- Frecuencia de red: 50 Hz · Conmutación: 3 kHz · Índice de modulación: 0.9
- Filtro: L = 0.25 mH · Bus: C = 20 mF
