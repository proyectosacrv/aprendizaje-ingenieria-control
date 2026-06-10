"""Anade a informe.html enlaces a las fichas del repositorio (00 - Repositorio) y
regenera informe_portable.html con las imagenes en base64.

Idempotente: re-ejecutar no duplica los bloques. Mapea cada seccion del informe con los
conceptos del repo relevantes.
"""
import re, base64, pathlib, yaml

HERE = pathlib.Path(__file__).parent
REPO = HERE.parent / "00 - Repositorio"
INFORME = HERE / "informe.html"
PORTABLE = HERE / "informe_portable.html"
REPO_HREF = "../00%20-%20Repositorio/index.html#"

# que conceptos del repo enlaza cada seccion del informe (por id de <section>)
MAP = {
    "fisica":  ["filtro-lcl", "marco-dq", "control-cascada"],
    "metodo":  ["linealizacion-numerica", "equilibrio-fsolve", "marco-dq"],
    "f1":      ["droop-control", "filtro-lcl", "linealizacion-numerica", "analisis-modal"],
    "f2":      ["respuesta-frecuencia-ss", "impedancia-salida-estabilidad"],
    "f3":      ["impedancia-salida-estabilidad", "red-thevenin-scr", "grid-forming-vs-following"],
    "f4":      ["medicion-impedancia-inyeccion", "modelo-promediado"],
    "f5":      ["vsm-inercia", "droop-control", "current-limiting"],
    "iter":    ["impedancia-virtual", "amortiguamiento-activo-lcl", "analisis-modal"],
}

CSS_RULE = (".repolinks{margin:16px 0;padding:11px 15px;background:#13202e;"
            "border:1px dashed var(--acc);border-radius:8px;font-size:13px;color:var(--muted)}"
            ".repolinks a{color:#7fd7ff}.repolinks b{color:#cfe1f0}")


def titles():
    t = {}
    for f in REPO.rglob("conceptos/**/*.md"):
        meta, _ = (lambda s: (yaml.safe_load(s.split('---', 2)[1]), None))(f.read_text(encoding="utf-8"))
        t[meta["slug"]] = meta.get("titulo", meta["slug"])
    return t


def block(slugs, t):
    links = " · ".join(f'<a href="{REPO_HREF}{s}">{t.get(s, s)}</a>' for s in slugs)
    return f'<div class="repolinks"><b>📚 En el repositorio:</b> {links}</div>'


def main():
    html = INFORME.read_text(encoding="utf-8")
    t = titles()
    # 1) CSS (una vez)
    if ".repolinks{" not in html:
        html = html.replace("</style>", CSS_RULE + "\n</style>", 1)
    # 2) limpiar bloques previos (idempotencia)
    html = re.sub(r'<div class="repolinks">.*?</div>', "", html, flags=re.S)
    # 3) insertar antes del </section> de cada seccion mapeada
    n = 0
    for sid, slugs in MAP.items():
        m = re.search(rf'(<section id="{sid}">.*?)(</section>)', html, flags=re.S)
        if m:
            html = html[:m.end(1)] + "\n" + block(slugs, t) + "\n" + m.group(2) + html[m.end(2):]
            n += 1
    INFORME.write_text(html, encoding="utf-8")
    print(f"informe.html: {n} secciones enlazadas")
    # 4) regenerar portable con imagenes base64
    def b64(mm):
        rel = mm.group(1)
        data = base64.b64encode((HERE / rel).read_bytes()).decode()
        return f'src="data:image/png;base64,{data}"'
    port, k = re.subn(r'src="(results/[^"]+\.png)"', b64, html)
    PORTABLE.write_text(port, encoding="utf-8")
    print(f"informe_portable.html: {k} imagenes incrustadas ({len(port)//1024} KB)")


if __name__ == "__main__":
    main()
