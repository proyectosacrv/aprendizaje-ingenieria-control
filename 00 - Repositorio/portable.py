"""Genera versiones OFFLINE de un solo archivo (repo + informes) para estudiar SIN CONEXIÓN.

Incrusta todo lo externo —MathJax, vis-network y las imágenes PNG como data URIs base64— en un
único .html autocontenido por documento. Basta copiar el archivo al móvil/tablet y abrirlo en
cualquier navegador (modo avión).

  python portable.py
    -> 00 - Repositorio/index_offline.html                 (repositorio: fichas)
    -> NN - <proyecto>/informe_offline.html                (cada informe)
"""
import os, re, base64

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MATHJAX = os.path.join(HERE, "assets", "mathjax-tex-svg.js")
VIS = os.path.join(HERE, "assets", "vis-network.min.js")
PROJECTS = ["01 - GFM-Impedance", "02 - GFL-Impedance", "03 - Energia-DataCenter-IA"]


def _read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def _inline_js(path):
    return "<script>\n" + _read(path).replace("</script>", "<\\/script>") + "\n</script>"


def _png_datauri(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")


def _externals_left(html):
    return re.findall(r'(?:src|href)="((?:assets/|results/|figuras/|\.\./)[^"]*)"', html)


def build_repo():
    html = _read(os.path.join(HERE, "index.html"))
    html = re.sub(r'<script src="assets/mathjax-tex-svg\.js"[^>]*></script>',
                  lambda m: _inline_js(MATHJAX), html, count=1)
    html = re.sub(r'<script defer src="assets/vis-network\.min\.js"></script>',
                  lambda m: _inline_js(VIS), html, count=1)
    fig_dir = os.path.join(HERE, "figuras")
    n = 0
    if os.path.isdir(fig_dir):
        for name in sorted(os.listdir(fig_dir)):
            if name.endswith(".png"):
                html = html.replace("figuras/" + name, _png_datauri(os.path.join(fig_dir, name)))
                n += 1
    out = os.path.join(HERE, "index_offline.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"index_offline.html: {os.path.getsize(out)/1e6:.1f} MB, {n} figuras")


def build_informe(proj):
    pdir = os.path.join(ROOT, proj)
    src = os.path.join(pdir, "informe.html")
    if not os.path.exists(src):
        print(f"  (sin informe.html en {proj})"); return
    html = _read(src)
    # MathJax (cualquier src que acabe en mathjax-tex-svg.js)
    html = re.sub(r'<script[^>]*src="[^"]*mathjax-tex-svg\.js"[^>]*></script>',
                  lambda m: _inline_js(MATHJAX), html, count=1)
    # imágenes results/ SOLO en src="..." (no en el texto de los bloques de código)
    rdir = os.path.join(pdir, "results")
    n = 0
    if os.path.isdir(rdir):
        for name in sorted(os.listdir(rdir)):
            if name.endswith(".png"):
                tag = 'src="results/' + name + '"'
                if tag in html:
                    html = html.replace(tag, 'src="' + _png_datauri(os.path.join(rdir, name)) + '"')
                    n += 1
    out = os.path.join(pdir, "informe_offline.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    left = [x for x in _externals_left(html) if not x.startswith("../00")]  # cruces al repo: se dejan
    print(f"  {proj}/informe_offline.html: {os.path.getsize(out)/1e6:.1f} MB, {n} imágenes"
          + (f"  [externos sin incrustar: {len(left)}]" if left else ""))


def main():
    build_repo()
    print("informes:")
    for p in PROJECTS:
        build_informe(p)


if __name__ == "__main__":
    main()
