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
| 2 | `02_etapa_potencia.sce` | VSC conmutado + filtro L; valida el **rizado** de corriente y el **THD** frente a la fórmula. | ✅ hecho |
| 3 | `03_lazos.sce` | Lazos de control: **corriente** (IMC, escalón) y **tensión del bus DC** (con feedforward, escalón de potencia). | ✅ hecho |
| 4 | `04_diseno.sce` | Diseño iterativo de componentes (**Vdc, L, Cdc**) desde las especificaciones + verificación CPL. | ✅ hecho |
| — | `informe.html` | Informe del proyecto (especificaciones, diseño, resultados, conclusiones). | ✅ hecho |

> El **informe** se ve en el navegador (también en la tablet): abre `informe.html`, o desde la web del
> repositorio en la chip de proyecto de la ficha *convertidor-back-to-back*.
> Ampliaciones futuras: back-to-back completo con MSC+MPPT y ensayos LVRT/arranque.

## Parámetros del caso (del ejemplo de la ficha)
- Potencia nominal: 2 MW · Red: 690 V (línea) · Bus DC: 1150 V
- Frecuencia de red: 50 Hz · Conmutación: 3 kHz · Índice de modulación: 0.9
- Filtro: L = 0.25 mH · Bus: C = 20 mF
