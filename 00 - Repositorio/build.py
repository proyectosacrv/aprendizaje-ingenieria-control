"""Generador del Repositorio de Conocimiento.

Escanea conceptos/**/*.md (fichas con frontmatter YAML), las convierte a HTML y genera
un unico index.html OFFLINE con buscador, filtros, seguimiento de progreso, backlinks
y rutas de aprendizaje. Las ecuaciones se renderizan con MathJax local (assets/).

Uso:  python build.py
"""
import re, json, pathlib, datetime
import yaml
import markdown

ROOT = pathlib.Path(__file__).parent
CONCEPTS = ROOT / "conceptos"
OUT = ROOT / "index.html"

CAT_LABEL = {"fisica-modelado": "Física y modelado",
             "control": "Teoría de control",
             "programacion": "Programación e implementación",
             "metodologia": "Metodología de control"}
CAT_COLOR = {"fisica-modelado": "#4ea3ff", "control": "#a78bfa", "programacion": "#5ad19a",
             "metodologia": "#ffb454"}

PROJECT_LINK = {"01-GFM-Impedance": "../01%20-%20GFM-Impedance/informe.html",
                "02-GFL-Impedance": "../02%20-%20GFL-Impedance/informe.html",
                "03-DataCenter-IA": "../03%20-%20Energia-DataCenter-IA/informe.html"}


def split_frontmatter(text):
    """Devuelve (meta_dict, cuerpo_markdown)."""
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        return yaml.safe_load(fm) or {}, body.strip()
    return {}, text


_DEV_HEAD_RE = re.compile(r"^\s*(?:Desarrollo\s+\d+|\d+)\s*[—–-]\s*")
_H2_RE = re.compile(r"<h2>(.*?)</h2>", re.S)
_TAG_RE = re.compile(r"<[^>]+>")


def _anchor(text):
    """Slug ASCII para el id de un heading (para las anclas del indice)."""
    t = _TAG_RE.sub("", text).lower()
    repl = (("á","a"),("é","e"),("í","i"),("ó","o"),("ú","u"),("ñ","n"),("ü","u"))
    for a, b in repl:
        t = t.replace(a, b)
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t or "sec"


def add_toc(html):
    """Numera con id cada <h2> visible y antepone un indice plegable con enlaces
    a cada seccion. Solo se añade si la ficha tiene 4 o mas secciones H2, para
    que las fichas cortas no lo lleven."""
    headings = _H2_RE.findall(html)
    if len(headings) < 4:
        # aun asi, poner ids por si se enlaza desde fuera
        return _H2_RE.sub(lambda m: f'<h2 id="{_anchor(m.group(1))}">{m.group(1)}</h2>', html)

    used = {}
    def add_id(m):
        txt = m.group(1)
        aid = _anchor(txt)
        if aid in used:
            used[aid] += 1; aid = f"{aid}-{used[aid]}"
        else:
            used[aid] = 0
        return f'<h2 id="{aid}">{txt}</h2>'
    html = _H2_RE.sub(add_id, html)

    # reconstruir la lista de (id, texto) en orden
    items = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', html, re.S)
    lis = "".join(
        f'<li><a class="toc-lnk" href="#{aid}">{_TAG_RE.sub("", txt)}</a></li>'
        for aid, txt in items
    )
    toc = (f'<details class="toc" open><summary>Índice</summary>'
           f'<ol class="toc-list">{lis}</ol></details>')
    # insertar antes del primer <h2>
    return html.replace("<h2 ", toc + "<h2 ", 1)


def wrap_dev_sections(html):
    """Envuelve cada seccion de desarrollo numerada ("## N -" / "## Desarrollo N -")
    en un <details> plegado por defecto, para que la ficha se vea corta y el lector
    despliegue solo el desarrollo que le interesa. El resto de secciones (Definicion,
    Cuando se usa, etc.) no se tocan."""
    parts = re.split(r"(<h2[^>]*>.*?</h2>)", html, flags=re.S)
    out = [parts[0]]
    i = 1
    while i < len(parts):
        h2tag = parts[i]
        content = parts[i + 1] if i + 1 < len(parts) else ""
        mh = re.match(r"<h2([^>]*)>(.*?)</h2>", h2tag, re.S)
        attrs, heading_text = mh.group(1), mh.group(2)
        if _DEV_HEAD_RE.match(heading_text):
            out.append(f'<details class="dev"{attrs}><summary>{heading_text}</summary>'
                        f'<div class="dev-body">{content}</div></details>')
        else:
            out.append(h2tag)
            out.append(content)
        i += 2
    return "".join(out)


def render_body(md_text):
    """Markdown -> HTML protegiendo las ecuaciones de MathJax y los [[wikilinks]]."""
    # 1) proteger matematicas para que markdown no toque $...$ ni \(...\) ni _subindices_
    store = []
    def protect(m):
        store.append(m.group(0)); return f"@@M{len(store)-1}@@"
    t = re.sub(r"\$\$.*?\$\$", protect, md_text, flags=re.S)
    t = re.sub(r"\\\(.*?\\\)", protect, t, flags=re.S)
    t = re.sub(r"\$[^\$\n]+?\$", protect, t)
    # 2) wikilinks [[slug]] o [[slug|texto]]
    def wl(m):
        slug = m.group(1).strip(); txt = (m.group(2) or slug).strip()
        return f'<a class="wl" data-slug="{slug}">{txt}</a>'
    t = re.sub(r"\[\[([^\]\|]+)(?:\|([^\]]+))?\]\]", wl, t)
    # 3) markdown -> html
    html = markdown.markdown(t, extensions=["extra", "sane_lists"])
    # 4) restaurar matematicas
    for i, s in enumerate(store):
        html = html.replace(f"@@M{i}@@", s)
    # 5) numerar headings con id y anteponer el indice
    html = add_toc(html)
    # 6) plegar las secciones de desarrollo numeradas
    html = wrap_dev_sections(html)
    return html


def plain_text(md_text):
    """Texto plano para la busqueda (sin marcas)."""
    t = re.sub(r"[#*`>\[\]\$_]", " ", md_text)
    return re.sub(r"\s+", " ", t).lower()


def collect():
    items = []
    for f in sorted(CONCEPTS.rglob("*.md")):
        meta, body = split_frontmatter(f.read_text(encoding="utf-8"))
        if not meta.get("slug"):
            continue
        items.append({
            "slug": meta["slug"],
            "titulo": meta.get("titulo", meta["slug"]),
            "categoria": meta.get("categoria", "control"),
            "tipo": meta.get("tipo", "concepto"),
            "nivel": meta.get("nivel", "intermedio"),
            "proyectos": meta.get("proyectos", []) or [],
            "objetivos": meta.get("objetivos", []) or [],
            "tags": meta.get("tags", []) or [],
            "relacionados": meta.get("relacionados", []) or [],
            "referencias": meta.get("referencias", []) or [],
            "fecha_creacion": str(meta.get("fecha_creacion", "")),
            "fecha_actualizacion": str(meta.get("fecha_actualizacion", "")),
            "html": render_body(body),
            "buscar": plain_text(meta.get("titulo", "") + " " + body
                                 + " " + " ".join(meta.get("tags", []) or [])),
        })
    return items


def facets(items, key):
    vals = set()
    for it in items:
        v = it[key]
        vals.update(v) if isinstance(v, list) else vals.add(v)
    return sorted(x for x in vals if x)


# ---------------- HTML / CSS / JS ----------------
CSS = """
:root{--bg:#0f1419;--panel:#161d26;--panel2:#1c2530;--ink:#e6edf3;--muted:#9aa7b4;
--acc:#4ea3ff;--line:#2a3542;--fisica:#4ea3ff;--control:#a78bfa;--programacion:#5ad19a;--metodologia:#ffb454}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:14.5px/1.6 -apple-system,Segoe UI,Roboto,Arial,sans-serif}
a{color:var(--acc);text-decoration:none}a:hover{text-decoration:underline}
header{padding:16px 26px;border-bottom:1px solid var(--line);background:var(--panel);position:sticky;top:0;z-index:10}
header h1{margin:0;font-size:19px}header .sub{color:var(--muted);font-size:12.5px;margin-top:3px}
.bar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-top:12px}
.bar input,.bar select{background:var(--panel2);border:1px solid var(--line);color:var(--ink);
  padding:7px 10px;border-radius:8px;font-size:13px}
.bar input#q{flex:1;min-width:220px}
.bar .clear{cursor:pointer;color:var(--muted);border:1px solid var(--line);padding:7px 12px;border-radius:8px}
.wrap{display:flex;min-height:calc(100vh - 120px);position:relative}
.list{width:420px;flex:0 0 420px;border-right:1px solid var(--line);overflow-y:auto;max-height:calc(100vh - 120px);
  transition:flex-basis .2s ease,width .2s ease}
body.list-collapsed #list{flex-basis:0;width:0;min-width:0;border-right:0;overflow:hidden}
.listtoggle{position:absolute;top:0;bottom:0;left:420px;z-index:9;width:15px;
  display:flex;align-items:center;justify-content:center;
  border:0;border-right:1px solid var(--line);background:var(--panel);color:var(--muted);
  cursor:pointer;font-size:10px;transition:left .2s ease,background .15s,color .15s}
.listtoggle:hover{background:var(--panel2);color:var(--acc)}
body.list-collapsed .listtoggle{left:0}
#list.hide ~ .listtoggle{display:none}
.count{padding:10px 18px;color:var(--muted);font-size:12px;border-bottom:1px solid var(--line)}
.card{padding:13px 18px;border-bottom:1px solid var(--line);cursor:pointer}
.card:hover{background:var(--panel)}.card.active{background:#1d3148;border-left:3px solid var(--acc)}
.card h3{margin:0 0 5px;font-size:15px}
.card .meta{display:flex;gap:6px;flex-wrap:wrap;font-size:11px;color:var(--muted)}
.chip{padding:1px 8px;border-radius:20px;border:1px solid var(--line);background:var(--panel2)}
.chip.cat{color:#0b0e12;font-weight:700;border:0}
.detail{flex:1;overflow-y:auto;max-height:calc(100vh - 120px);padding:26px 40px}
.detail.empty{display:grid;place-items:center;color:var(--muted)}
.detail h1{font-size:26px;margin:0 0 6px}
.detail h2{font-size:18px;margin:24px 0 8px;padding-bottom:5px;border-bottom:1px solid var(--line);color:#cdd9e5}
.detail h3{font-size:15px;margin:16px 0 6px;color:#cdd9e5}
.detail pre{background:#0b0f14;border:1px solid var(--line);border-radius:9px;padding:13px 15px;overflow-x:auto;
  font:12.5px/1.5 SF Mono,Menlo,Consolas,monospace;color:#cfe3f5}
.detail code{background:var(--panel2);padding:1.5px 6px;border-radius:5px;font:12.5px monospace;color:#ffd9a0}
.detail pre code{background:none;padding:0;color:inherit}
.detail table{border-collapse:collapse;width:100%;margin:10px 0;font-size:13px}
.detail th,.detail td{border:1px solid var(--line);padding:7px 10px;text-align:left}
.detail th{background:var(--panel2)}
.detail blockquote{border-left:3px solid var(--acc);margin:12px 0;padding:6px 15px;background:#13202e;color:#cfe1f0}
.detail details.dev{border:1px solid var(--line);border-radius:9px;margin:24px 0 8px;background:var(--panel)}
.detail details.dev>summary{cursor:pointer;list-style:none;padding:11px 15px;font-size:18px;color:#cdd9e5}
.detail details.dev>summary::-webkit-details-marker{display:none}
.detail details.dev>summary::before{content:"▸";display:inline-block;color:var(--acc);width:14px;transition:transform .15s}
.detail details.dev[open]>summary::before{transform:rotate(90deg)}
.detail details.dev>summary:hover{color:var(--ink)}
.detail details.dev>.dev-body{padding:2px 16px 16px;border-top:1px solid var(--line)}
.detail details.dev>.dev-body>:first-child{margin-top:14px}
.metahead{display:flex;gap:7px;flex-wrap:wrap;margin:10px 0 6px}
.metahead .chip{font-size:12px}
.wl{border-bottom:1px dotted var(--acc)}
/* ── Indice de la ficha ──────────────────────────────────────────── */
.detail details.toc{border:1px solid var(--line);border-radius:9px;margin:6px 0 20px;background:var(--panel2)}
.detail details.toc>summary{cursor:pointer;list-style:none;padding:9px 14px;font-size:13px;font-weight:700;color:var(--muted)}
.detail details.toc>summary::-webkit-details-marker{display:none}
.detail details.toc>summary::before{content:"▸";display:inline-block;color:var(--acc);width:14px;transition:transform .15s}
.detail details.toc[open]>summary::before{transform:rotate(90deg)}
.detail .toc-list{margin:0;padding:2px 14px 12px 34px;columns:2;column-gap:26px;font-size:12.5px}
.detail .toc-list li{margin:3px 0;break-inside:avoid}
.detail .toc-lnk{color:#bcd3ea}
.detail .toc-lnk:hover{color:var(--acc)}
@media(max-width:760px){.detail .toc-list{columns:1}}
.cfig{background:#fff;border:1px solid var(--line);border-radius:9px;padding:12px;margin:16px 0;text-align:center}
.cfig img{max-width:100%;height:auto;border-radius:4px}
.cfig .cap{color:#555;font-size:12px;margin-top:8px;line-height:1.45}
.viewtoggle{display:flex;border:1px solid var(--line);border-radius:8px;overflow:hidden}
.viewtoggle button{background:var(--panel2);color:var(--muted);border:0;padding:7px 12px;cursor:pointer;font-size:13px}
.viewtoggle button.on{background:#23456b;color:#fff}
.list.hide{display:none}
#graphwrap{flex:1;display:none;border-right:1px solid var(--line);background:#0b0f14}
#graphwrap.show{display:block}
#graph{width:100%;height:calc(100vh - 124px)}
.glegend{position:absolute;margin:10px;display:flex;gap:12px;font-size:12px;color:var(--muted);z-index:5}
.glegend i{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:4px;vertical-align:middle}
/* ── Estado ──────────────────────────────────────────────────────── */
.st-badge{display:inline-block;padding:1px 7px;border-radius:10px;font-size:10px;font-weight:700;color:#0b0e12;margin-left:3px;vertical-align:middle}
.st-bar{display:flex;gap:6px;align-items:center;margin:6px 0 14px;flex-wrap:wrap}
.st-label{color:var(--muted);font-size:12px;margin-right:2px}
.st-btn{background:var(--panel2);border:1px solid var(--line);color:var(--muted);padding:4px 11px;border-radius:6px;cursor:pointer;font-size:12px;transition:border-color .15s}
.st-btn:hover{border-color:var(--acc);color:var(--ink)}
/* ── Mini barra de progreso global ───────────────────────────────── */
.mini-prog{display:inline-block;width:56px;height:5px;background:var(--panel2);border-radius:3px;vertical-align:middle;margin-left:4px;overflow:hidden}
.mini-prog span{display:block;height:100%;background:var(--programacion);border-radius:3px;transition:width .3s}
/* ── Backlinks ───────────────────────────────────────────────────── */
.backlinks{margin-top:22px;padding:10px 14px;background:var(--panel2);border-left:3px solid var(--acc);border-radius:0 8px 8px 0;font-size:13px}
.bl-lbl{font-weight:700;color:var(--muted);margin-right:6px}
/* ── Rutas de aprendizaje ────────────────────────────────────────── */
#rutaswrap{flex:1;overflow-y:auto;max-height:calc(100vh - 120px);padding:22px 32px;display:none;background:var(--bg)}
#rutaswrap.show{display:block}
.ruta-card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin-bottom:16px;max-width:840px}
.ruta-hdr{display:flex;gap:14px;align-items:flex-start;margin-bottom:10px}
.ruta-ico{font-size:28px;flex-shrink:0}
.ruta-nom{font-size:16px;font-weight:700;margin-bottom:3px}
.ruta-dsc{font-size:12px;color:var(--muted)}
.ruta-st{margin-left:auto;font-size:12px;color:var(--muted);white-space:nowrap;text-align:right;line-height:1.8}
.ruta-pbwrap{height:6px;background:var(--panel2);border-radius:3px;margin:0 0 12px;position:relative;overflow:hidden}
.ruta-pb{position:absolute;left:0;top:0;height:100%;border-radius:3px;transition:width .4s}
.ruta-pb-v{background:var(--acc);opacity:.35}
.ruta-pb-d{background:var(--programacion)}
.ruta-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:2px}
.ruta-item{display:flex;align-items:center;gap:7px;padding:6px 8px;border-radius:6px;cursor:pointer;font-size:13px;user-select:none}
.ruta-item:hover{background:var(--panel2)}
.ruta-n{color:var(--muted);font-size:11px;min-width:22px;text-align:right;flex-shrink:0}
.ruta-step-ico{width:16px;text-align:center;flex-shrink:0;font-size:13px}
.ruta-nm{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
/* ── Inicio / volver / accesibilidad ─────────────────────────────── */
.home{display:inline-block;color:var(--muted);border:1px solid var(--line);
  padding:5px 11px;border-radius:8px;font-size:12.5px;margin-bottom:8px}
.home:hover{border-color:var(--acc);color:var(--ink);text-decoration:none}
.backbtn{display:none}
.fbtn{display:none;background:var(--panel2);border:1px solid var(--line);color:var(--ink);
  padding:7px 12px;border-radius:8px;font-size:13px;cursor:pointer}
.filters{display:contents}
.backbtn:focus-visible,.fbtn:focus-visible,.st-btn:focus-visible,.card:focus-visible,
.bar input:focus-visible,.bar select:focus-visible,.viewtoggle button:focus-visible,
.home:focus-visible{outline:2px solid var(--acc);outline-offset:2px}
/* ── Responsive / movil ──────────────────────────────────────────── */
@media(max-width:760px){
  header{position:static;padding:12px 16px}
  header h1{font-size:16px}
  .bar{gap:7px}
  .bar input#q{min-width:120px;flex:1 1 55%}
  .bar select,.bar .clear{font-size:12px;padding:8px 9px}
  .fbtn{display:inline-block}
  .filters{display:none;flex-wrap:wrap;gap:7px;width:100%;margin-top:2px}
  body.filters-open .filters{display:flex}
  .filters select,.filters .clear{flex:1 1 45%}
  .viewtoggle{flex:1 1 100%}
  .viewtoggle button{flex:1;padding:9px 12px}
  .wrap{display:block;min-height:0}
  .list{width:100%;flex:none;max-height:none;border-right:0}
  .detail{max-height:none;padding:16px 15px}
  .detail h1{font-size:21px}
  .detail pre{font-size:12px}
  #graph{height:72vh}
  /* conmutar lista <-> teoria a pantalla completa */
  body:not(.detail-open) #detail{display:none}
  body.detail-open .list,body.detail-open #graphwrap,body.detail-open #rutaswrap{display:none}
  body.detail-open header .bar{display:none}
  .backbtn{display:flex;align-items:center;gap:8px;position:sticky;top:0;z-index:6;
    width:calc(100% + 30px);margin:-16px -15px 12px;padding:13px 16px;
    background:var(--panel);border:0;border-bottom:1px solid var(--line);
    color:var(--acc);font-size:15px;cursor:pointer}
}
"""

JS = """
const D = window.DATA, CATL = window.CATL, RUTAS = window.RUTAS||[];
const $=s=>document.querySelector(s);
let sel=null, view='list';

// ─── Estado (progress tracking) ──────────────────────────────────────────
const ST_KEY='repoKB_v1';
const ST_LABELS={visto:'Visto', dominado:'Dominado', repasar:'Repasar'};
const ST_COLOR={visto:'var(--acc)', dominado:'var(--programacion)', repasar:'var(--metodologia)'};

function stMap(){ return JSON.parse(localStorage.getItem(ST_KEY)||'{}'); }
function getStatus(slug){ return stMap()[slug]||null; }
function setStatus(slug,val){
  const m=stMap();
  if(val) m[slug]=val; else delete m[slug];
  localStorage.setItem(ST_KEY,JSON.stringify(m));
  render();
  if(sel===slug) renderStBar(slug);
  if(view==='rutas') renderRutas();
}
function toggleStatus(slug,val){ setStatus(slug, getStatus(slug)===val?null:val); }

function renderStBar(slug){
  const bar=$('#st-bar'); if(!bar) return;
  const s=getStatus(slug);
  bar.innerHTML='<span class="st-label">Estado:</span>'+
    ['visto','dominado','repasar'].map(v=>`<button class="st-btn"${
      s===v?` style="background:${ST_COLOR[v]};color:#0b0e12;border-color:${ST_COLOR[v]}"`:''
    } onclick="toggleStatus('${slug}','${v}')">${ST_LABELS[v]}</button>`
    ).join('')+
    (s?`<button class="st-btn" onclick="setStatus('${slug}',null)">✕</button>`:'');
}

function stBadge(slug){
  const s=getStatus(slug); if(!s) return '';
  return `<span class="st-badge" style="background:${ST_COLOR[s]}">${ST_LABELS[s]}</span>`;
}

// ─── Filtros y lista ──────────────────────────────────────────────────────
function uniqOptions(id,key){
  const s=new Set(); D.forEach(d=>{const v=d[key]; Array.isArray(v)?v.forEach(x=>s.add(x)):s.add(v);});
  const el=$(id); [...s].filter(Boolean).sort().forEach(v=>{
    const o=document.createElement('option'); o.value=v; o.textContent=(CATL[v]||v); el.appendChild(o);});
}

function searchScore(d, q){
  // Devuelve -1 si no hay match; score mayor = más relevante
  if(!q) return 0;
  const titulo = d.titulo.toLowerCase();
  const slug = d.slug.toLowerCase();
  const tags = (d.tags||[]).join(' ').toLowerCase();
  const objetivos = (d.objetivos||[]).join(' ').toLowerCase();
  const html = (d.html||'').toLowerCase();
  if(titulo === q) return 100;
  if(titulo.startsWith(q)) return 90;
  if(titulo.includes(q)) return 80;
  if(slug.includes(q)) return 70;
  if(tags.includes(q)) return 60;
  if(objetivos.includes(q)) return 50;
  if(html.includes(q)) return 10;
  return -1;
}

function matches(d){
  const q=$('#q').value.trim().toLowerCase();
  if(q && searchScore(d, q) < 0) return false;
  for(const [id,key] of [['#fcat','categoria'],['#ftipo','tipo'],['#fniv','nivel']]){
    const v=$(id).value; if(v && d[key]!==v) return false;
  }
  for(const [id,key] of [['#fpro','proyectos'],['#fobj','objetivos'],['#ftag','tags']]){
    const v=$(id).value; if(v && !(d[key]||[]).includes(v)) return false;
  }
  const fs=$('#fstat').value;
  if(fs){ const s=getStatus(d.slug); if(fs==='ninguno'?!!s:(s!==fs)) return false; }
  return true;
}

function render(){
  const sort=$('#sort').value;
  const q=$('#q').value.trim().toLowerCase();
  let r=D.filter(matches);
  if(q){
    r.sort((a,b)=> searchScore(b,q) - searchScore(a,q));
  } else {
    r.sort((a,b)=> sort==='titulo'? a.titulo.localeCompare(b.titulo)
      : (b.fecha_actualizacion||'').localeCompare(a.fecha_actualizacion||''));
  }
  const tot=D.length,
        ndom=D.filter(d=>getStatus(d.slug)==='dominado').length,
        nvis=D.filter(d=>getStatus(d.slug)==='visto').length;
  const pct=Math.round(ndom/tot*100);
  $('#count').innerHTML=`${r.length} concepto(s) &nbsp;·&nbsp; `+
    `<span style="color:var(--programacion)">${ndom} dom.</span> `+
    `<span style="color:var(--acc)">${nvis} vis.</span> `+
    `<span style="color:var(--muted)">${tot-ndom-nvis} sin</span>`+
    `<span class="mini-prog"><span style="width:${pct}%"></span></span>`;
  const L=$('#list'); L.querySelectorAll('.card').forEach(e=>e.remove());
  r.forEach(d=>{
    const c=document.createElement('div'); c.className='card'+(sel===d.slug?' active':'');
    c.onclick=()=>show(d.slug);
    c.innerHTML=`<h3>${d.titulo}${stBadge(d.slug)}</h3><div class="meta">
      <span class="chip cat" style="background:${catColor(d.categoria)}">${CATL[d.categoria]||d.categoria}</span>
      <span class="chip">${d.tipo}</span><span class="chip">${d.nivel}</span>
      ${(d.proyectos||[]).map(p=>`<span class="chip">${p}</span>`).join('')}</div>`;
    L.appendChild(c);
  });
}
function catColor(c){return getComputedStyle(document.documentElement).getPropertyValue('--'+c.split('-')[0])||'#888';}

// ─── Detail view ─────────────────────────────────────────────────────────
function show(slug){
  if(view!=='list') setView('list');
  sel=slug; const d=D.find(x=>x.slug===slug); const det=$('#detail');
  det.className='detail';
  const bl=D.filter(x=>(x.relacionados||[]).includes(slug)&&x.slug!==slug);
  const blHTML=bl.length?`<div class="backlinks"><span class="bl-lbl">← Referenciado por:</span>`+
    bl.map(x=>`<a class="wl" data-slug="${x.slug}">${x.titulo}</a>`).join(' · ')+`</div>`:'';
  det.innerHTML=`<button class="backbtn" onclick="history.back()" aria-label="Volver a la lista de conceptos">← Volver a la lista</button><h1>${d.titulo}</h1><div class="metahead">
    <span class="chip cat" style="background:${catColor(d.categoria)}">${CATL[d.categoria]||d.categoria}</span>
    <span class="chip">${d.tipo}</span><span class="chip">${d.nivel}</span>
    ${(d.proyectos||[]).map(p=> PROJL[p]
       ? `<a class="chip" href="${PROJL[p]}" title="abrir informe del proyecto">📁 ${p} ↗</a>`
       : `<span class="chip">📁 ${p}</span>`).join('')}
    ${(d.objetivos||[]).map(o=>`<span class="chip">🎯 ${o}</span>`).join('')}
    <span class="chip">🗓 ${d.fecha_actualizacion}</span></div>
    <div class="st-bar" id="st-bar"></div>
    ${d.html}${blHTML}`;
  renderStBar(slug);
  det.querySelectorAll('.wl').forEach(a=>a.onclick=()=>{const s=a.dataset.slug; if(D.find(x=>x.slug===s)) show(s);});
  det.querySelectorAll('.toc-lnk').forEach(a=>a.onclick=e=>{
    e.preventDefault();
    const tgt=det.querySelector(a.getAttribute('href'));
    if(!tgt) return;
    if(tgt.tagName==='DETAILS') tgt.open=true;               // desplegar seccion de desarrollo
    const d2=tgt.closest('details'); if(d2) d2.open=true;    // o el details que la contiene
    tgt.scrollIntoView({behavior:'smooth',block:'start'});
  });
  if(window.MathJax&&MathJax.typesetPromise) MathJax.typesetPromise([det]);
  if(location.hash!=='#'+slug) history.pushState(null,'','#'+slug);
  document.body.classList.add('detail-open');
  det.scrollTop=0; window.scrollTo(0,0); render();
}

// ─── Rutas de aprendizaje ─────────────────────────────────────────────────
function renderRutas(){
  const el=$('#rutaswrap'); if(!el) return;
  el.innerHTML=RUTAS.map(r=>{
    const slugs=r.conceptos||[], tot=slugs.length;
    const ndom=slugs.filter(s=>getStatus(s)==='dominado').length;
    const nvis=slugs.filter(s=>getStatus(s)==='visto').length;
    const prep=slugs.filter(s=>getStatus(s)==='repasar').length;
    const pdom=tot?Math.round(ndom/tot*100):0, pall=tot?Math.round((ndom+nvis)/tot*100):0;
    const items=slugs.map((slug,i)=>{
      const dd=D.find(x=>x.slug===slug), nm=dd?dd.titulo:slug, s=getStatus(slug);
      const ico={visto:'👁',dominado:'✓',repasar:'↩'}[s]||'○';
      const col=ST_COLOR[s]||'var(--muted)';
      return `<div class="ruta-item" onclick="show('${slug}')">
        <span class="ruta-n">${i+1}</span>
        <span class="ruta-step-ico" style="color:${col}">${ico}</span>
        <span class="ruta-nm">${nm}</span>
        ${s?`<span class="st-badge" style="background:${col}">${ST_LABELS[s]}</span>`:''}
      </div>`;
    }).join('');
    return `<div class="ruta-card">
      <div class="ruta-hdr">
        <span class="ruta-ico">${r.icono||'📚'}</span>
        <div><div class="ruta-nom">${r.nombre}</div><div class="ruta-dsc">${r.descripcion}</div></div>
        <div class="ruta-st">
          <span style="color:var(--programacion)">${ndom} dom.</span>
          <span style="color:var(--acc)">${nvis} vis.</span>
          ${prep?`<span style="color:var(--metodologia)">${prep} rep.</span>`:''}
          <br><span style="color:var(--muted)">${tot-ndom-nvis-prep} sin · ${tot} total</span>
        </div>
      </div>
      <div class="ruta-pbwrap">
        <div class="ruta-pb ruta-pb-v" style="width:${pall}%"></div>
        <div class="ruta-pb ruta-pb-d" style="width:${pdom}%"></div>
      </div>
      <div class="ruta-list">${items}</div>
    </div>`;
  }).join('');
}

// ─── Vistas ───────────────────────────────────────────────────────────────
let net=null;
const GCOLOR={'fisica-modelado':'#4ea3ff','control':'#a78bfa','programacion':'#5ad19a','metodologia':'#ffb454'};

function setView(v){
  view=v;
  document.body.classList.remove('detail-open');
  $('#vlist').classList.toggle('on',v==='list');
  $('#vgraph').classList.toggle('on',v==='graph');
  $('#vrutas').classList.toggle('on',v==='rutas');
  $('#list').classList.toggle('hide',v!=='list');
  $('#detail').style.display=v==='list'?'':'none';
  $('#graphwrap').classList.toggle('show',v==='graph');
  $('#rutaswrap').classList.toggle('show',v==='rutas');
  if(v==='graph') buildGraph();
  if(v==='rutas') renderRutas();
}

function buildGraph(){
  if(typeof vis==='undefined'){setTimeout(buildGraph,200);return;}
  const vd=D.filter(matches), ok=new Set(vd.map(d=>d.slug));
  const nodes=vd.map(d=>({id:d.slug,label:d.titulo,group:d.categoria,value:1+(d.relacionados||[]).length}));
  const edges=[], ek=new Set();
  vd.forEach(d=>(d.relacionados||[]).forEach(r=>{
    if(!ok.has(r))return; const k=[d.slug,r].sort().join('|');
    if(!ek.has(k)){ek.add(k); edges.push({from:d.slug,to:r});}
  }));
  const opts={
    groups:{'fisica-modelado':{color:GCOLOR['fisica-modelado']},'control':{color:GCOLOR['control']},
            'programacion':{color:GCOLOR['programacion']},'metodologia':{color:GCOLOR['metodologia']}},
    nodes:{shape:'dot',scaling:{min:8,max:26},font:{color:'#e6edf3',size:13}},
    edges:{color:{color:'#3a4756',highlight:'#4ea3ff'},smooth:false,width:1},
    physics:{barnesHut:{gravitationalConstant:-4000,springLength:130,springConstant:0.04},stabilization:{iterations:250}},
    interaction:{hover:true,tooltipDelay:120}
  };
  if(net) net.destroy();
  net=new vis.Network($('#graph'),{nodes:new vis.DataSet(nodes),edges:new vis.DataSet(edges)},opts);
  net.on('click',p=>{if(p.nodes.length){sel=p.nodes[0]; show(sel);}});
}

function onFilter(){render(); if(view==='graph') buildGraph(); if(view==='rutas') renderRutas();}
function clearAll(){['#q','#fcat','#ftipo','#fniv','#fpro','#fobj','#ftag','#fstat'].forEach(s=>$(s).value=''); onFilter();}
function applyHash(){const s=decodeURIComponent(location.hash.slice(1));
  if(s&&D.find(x=>x.slug===s)) show(s); else document.body.classList.remove('detail-open');}

window.addEventListener('DOMContentLoaded',()=>{
  uniqOptions('#fcat','categoria'); uniqOptions('#ftipo','tipo'); uniqOptions('#fniv','nivel');
  uniqOptions('#fpro','proyectos'); uniqOptions('#fobj','objetivos'); uniqOptions('#ftag','tags');
  ['#q','#fcat','#ftipo','#fniv','#fpro','#fobj','#ftag','#fstat','#sort'].forEach(s=>$(s).addEventListener('input',onFilter));
  $('#vlist').onclick=()=>setView('list');
  $('#vgraph').onclick=()=>setView('graph');
  $('#vrutas').onclick=()=>setView('rutas');
  const setListCollapsed=v=>{document.body.classList.toggle('list-collapsed',v);
    $('#listtoggle').textContent=v?'▶':'◀';
    try{localStorage.setItem('listCollapsed',v?'1':'0')}catch(e){}};
  $('#listtoggle').onclick=()=>setListCollapsed(!document.body.classList.contains('list-collapsed'));
  setListCollapsed(localStorage.getItem('listCollapsed')==='1');
  render(); applyHash();
});
window.addEventListener('hashchange', applyHash);
"""

TEMPLATE = """<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Repositorio de Conocimiento</title>
<style>{css}</style>
<script>window.MathJax={{tex:{{inlineMath:[['\\\\(','\\\\)']],displayMath:[['$$','$$']]}},svg:{{fontCache:'global'}}}};</script>
<script src="assets/mathjax-tex-svg.js" async></script>
<script defer src="assets/vis-network.min.js"></script>
</head><body>
<header>
  <a class="home" href="../index.html">🏠 Inicio · proyectos y repositorio</a>
  <h1>Repositorio de Conocimiento — Ingeniería de convertidores</h1>
  <div class="sub">{n} conceptos · generado {fecha} · física · control · programación</div>
  <div class="bar">
    <input id="q" placeholder="🔎 buscar concepto, técnica, parámetro...">
    <button class="fbtn" onclick="document.body.classList.toggle('filters-open')" aria-label="Mostrar u ocultar filtros">⚙ Filtros</button>
    <div class="filters">
      <select id="fcat"><option value="">Categoría</option></select>
      <select id="ftipo"><option value="">Tipo</option></select>
      <select id="fpro"><option value="">Proyecto</option></select>
      <select id="fobj"><option value="">Objetivo</option></select>
      <select id="fniv"><option value="">Nivel</option></select>
      <select id="ftag"><option value="">Tag</option></select>
      <select id="fstat"><option value="">Estado</option><option value="ninguno">Sin estado</option><option value="visto">Visto</option><option value="dominado">Dominado</option><option value="repasar">Repasar</option></select>
      <select id="sort"><option value="fecha">Orden: fecha</option><option value="titulo">Orden: nombre</option></select>
      <span class="clear" onclick="clearAll()">limpiar</span>
    </div>
    <span class="viewtoggle"><button id="vlist" class="on">📋 Lista</button><button id="vgraph">🕸 Grafo</button><button id="vrutas">📚 Rutas</button></span>
  </div>
</header>
<div class="wrap">
  <div class="list" id="list"><div class="count" id="count"></div></div>
  <button id="listtoggle" class="listtoggle" title="Ocultar o mostrar la lista" aria-label="Ocultar o mostrar la lista">◀</button>
  <div id="graphwrap">
    <div class="glegend"><span><i style="background:#4ea3ff"></i>Física</span>
      <span><i style="background:#a78bfa"></i>Control</span>
      <span><i style="background:#5ad19a"></i>Programación</span>
      <span><i style="background:#ffb454"></i>Metodología</span></div>
    <div id="graph"></div>
  </div>
  <div id="rutaswrap"></div>
  <div class="detail empty" id="detail">Selecciona un concepto</div>
</div>
<script>window.DATA={data};window.CATL={catl};window.PROJL={projl};window.RUTAS={rutas};</script>
<script>{js}</script>
</body></html>"""


def main():
    rutas_path = ROOT / "rutas.yaml"
    rutas = yaml.safe_load(rutas_path.read_text(encoding="utf-8")) if rutas_path.exists() else []

    items = collect()
    catl = dict(CAT_LABEL)
    html = TEMPLATE.format(
        css=CSS, js=JS,
        data=json.dumps(items, ensure_ascii=False),
        catl=json.dumps(catl, ensure_ascii=False),
        projl=json.dumps(PROJECT_LINK, ensure_ascii=False),
        rutas=json.dumps(rutas, ensure_ascii=False),
        n=len(items), fecha=datetime.date.today().isoformat())
    OUT.write_text(html, encoding="utf-8")
    print(f"OK · {len(items)} conceptos -> {OUT.name}")
    for c in facets(items, "categoria"):
        n = sum(1 for it in items if it["categoria"] == c)
        print(f"   {CAT_LABEL.get(c,c):28s} {n}")


if __name__ == "__main__":
    main()
