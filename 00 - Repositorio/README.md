# 00 · Repositorio de Conocimiento

Base de conocimiento **transversal y dinámica** de ingeniería de convertidores. Reúne, de
forma reutilizable entre proyectos, la teoría física, las técnicas de control y los métodos de
programación/implementación en los que se basan los desarrollos.

## Cómo se usa (interfaz)
1. Ejecuta el generador:
   ```bash
   python build.py
   ```
2. Abre **`index.html`** en el navegador. Es 100% offline (MathJax incluido en `assets/`).
3. Busca y **filtra** por: texto libre, categoría, tipo, **proyecto**, **objetivo**, nivel, tag;
   ordena por fecha o nombre. Clic en un concepto → ficha completa con ecuaciones y código.
   Los enlaces `[[concepto]]` navegan entre fichas.

## Estructura
```
00 - Repositorio/
  conceptos/
    fisica-modelado/    fichas .md de física y modelado
    control/            fichas .md de teoría de control
    programacion/       fichas .md de programación e implementación
  assets/mathjax-tex-svg.js   render de ecuaciones offline
  plantilla-concepto.md       plantilla para fichas nuevas
  build.py                    genera index.html
  index.html                  interfaz (generada)
```

## Cómo añadir un concepto
1. Copia `plantilla-concepto.md` a `conceptos/<disciplina>/<slug>.md`.
2. Rellena el **frontmatter** (metadatos de filtrado) y las secciones.
3. `python build.py` y recarga `index.html`.

### Frontmatter (metadatos)
`titulo · slug · categoria` (fisica-modelado | control | programacion) `· tipo` (concepto |
tecnica | parametro | metodo | herramienta | fenomeno) `· nivel · proyectos · objetivos ·
tags · fecha_creacion · fecha_actualizacion · relacionados · referencias`.

### Secciones de cada ficha (máximo detalle)
Definición · Fundamento teórico (ecuaciones) · Cuándo y por qué · **Procedimiento de diseño
genérico** · Ejemplo de código reducido · Parámetros típicos · Errores comunes · Uso en
proyectos · Conceptos relacionados · Referencias.

## Flujo de trabajo (aprendizaje)
1. Se desarrolla un proyecto (carpeta `NN - Nombre`).
2. Se redactan/actualizan en el repo las fichas de **todos** los conceptos usados o relacionados.
3. El proyecto incluye un **informe HTML** (memoria visual con todo el detalle).
4. Al preguntar por un concepto: primero se revisa el repo → si existe, se dirige a la ficha;
   si no, se explica y se **añade** la ficha.

## Notas
- Las ecuaciones usan `$$...$$` (display) y `\( ... \)` (inline), renderizadas por MathJax local.
- Enlaces entre conceptos con `[[slug]]` o `[[slug|texto visible]]`.
