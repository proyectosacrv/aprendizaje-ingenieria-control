"""Genera la portada (index.html) del directorio de aprendizaje: punto de entrada que
enlaza el Repositorio de Conocimiento y cada proyecto (con su informe). Dinamico: escanea
las carpetas 'NN - Nombre' y se actualiza solo al anadir proyectos.

Uso:  python portada.py    (desde 00 - Repositorio)
"""
import re, pathlib, urllib.parse

REPO = pathlib.Path(__file__).parent
BASE = REPO.parent
OUT = BASE / "index.html"


def enc(p):  # ruta relativa con espacios escapados para href
    return urllib.parse.quote(p)


def projects():
    out = []
    for d in sorted(BASE.iterdir()):
        if not d.is_dir() or not re.match(r"\d{2}\s*-\s*", d.name):
            continue
        if d.name.startswith("00"):
            continue
        informe = next((f for f in ["informe.html", "informe_portable.html"]
                        if (d / f).exists()), None)
        out.append((d.name, informe))
    return out


def card(title, sub, href, icon):
    a = f'href="{enc(href)}"' if href else 'style="opacity:.6;cursor:default"'
    return (f'<a class="card" {a}><div class="ic">{icon}</div>'
            f'<div><h3>{title}</h3><p>{sub}</p></div></a>')


def main():
    cards = [card("Repositorio de Conocimiento", "Conceptos de física, control y programación · filtrable",
                  "00 - Repositorio/index.html", "📚"),
             card("Guía: ciclo de diseño de control", "Metodología — diseñar · evaluar · validar",
                  "00 - Repositorio/guia-metodologia.html", "🧭")]
    for name, informe in projects():
        sub = "Informe / memoria del proyecto" if informe else "(sin informe aún)"
        href = f"{name}/{informe}" if informe else None
        cards.append(card(name, sub, href, "📁"))

    html = f"""<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Aprendizaje · Ingeniería de convertidores</title>
<style>
:root{{--bg:#0f1419;--panel:#161d26;--ink:#e6edf3;--muted:#9aa7b4;--acc:#4ea3ff;--line:#2a3542}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 -apple-system,Segoe UI,Roboto,Arial,sans-serif}}
.hero{{padding:54px 40px 26px;max-width:1000px;margin:0 auto}}
.hero h1{{font-size:30px;margin:0 0 6px}}.hero p{{color:var(--muted);margin:0}}
.grid{{max-width:1000px;margin:0 auto;padding:10px 40px 60px;display:grid;
  grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}}
.card{{display:flex;gap:14px;align-items:center;background:var(--panel);border:1px solid var(--line);
  border-radius:14px;padding:18px 20px;color:var(--ink);text-decoration:none;transition:.15s}}
.card:hover{{border-color:var(--acc);transform:translateY(-2px)}}
.card .ic{{font-size:30px}}.card h3{{margin:0 0 3px;font-size:16px}}
.card p{{margin:0;color:var(--muted);font-size:13px}}
</style></head><body>
<div class="hero"><h1>07 · Aprendizaje — Ingeniería de convertidores</h1>
<p>Punto de entrada: el repositorio de conocimiento y los proyectos.</p></div>
<div class="grid">{''.join(cards)}</div>
</body></html>"""
    OUT.write_text(html, encoding="utf-8")
    print(f"portada -> {OUT}  ({len(projects())} proyecto(s) + repositorio)")


if __name__ == "__main__":
    main()
