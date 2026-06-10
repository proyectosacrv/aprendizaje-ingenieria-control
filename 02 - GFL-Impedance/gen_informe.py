"""Generador del informe HTML (nivel tesis) del proyecto 02 - GFL-Impedance.

Lee los .py reales del proyecto, los embebe escapados y los acompana de la explicacion
detallada y de los resultados de consola reales. Reejecutar regenera informe.html.
    python gen_informe.py
"""
import os, html, datetime

HERE = os.path.dirname(os.path.abspath(__file__))


def embed(fname, caption=None):
    path = os.path.join(HERE, fname)
    code = open(path, encoding="utf-8").read()
    nlines = code.count("\n") + 1
    cap = f'<div class="cap">{caption}</div>' if caption else ""
    return (f'<div class="codefile"><div class="h"><span>📄 {fname}</span>'
            f'<span>{nlines} líneas · código real del proyecto</span></div>'
            f'<pre>{html.escape(code)}</pre></div>{cap}')


def console(text):
    return f'<div class="console">{html.escape(text)}</div>'


# ---- RESULTADOS DE CONSOLA REALES ----
R_P1 = """============================================================
FASE 1 - Inversor grid-following (red rigida)
============================================================
Equilibrio: ier=1 residual=1.76e-11
  P_eq=  5000.0 W  Q_eq=  1012.3 var  |vc|=327.7 V  delta=0.54 deg
  v_Cq=5.05e-28 (la PLL lo lleva a 0)

Autovalores:
      -50.01      +0.00j   f=    0.0 Hz   zeta=+1.000
      -50.06      +0.00j   f=    0.0 Hz   zeta=+1.000
     -134.27    +133.83j   f=   21.3 Hz   zeta=+0.708
     -134.27    -133.83j   f=   21.3 Hz   zeta=+0.708
     -946.52   +5996.35j   f=  954.3 Hz   zeta=+0.156
     -946.52   -5996.35j   f=  954.3 Hz   zeta=+0.156
    -1100.34   +6743.39j   f= 1073.2 Hz   zeta=+0.161
    -1100.34   -6743.39j   f= 1073.2 Hz   zeta=+0.161
    -5684.46      +0.00j   f=    0.0 Hz   zeta=+1.000
    -6373.78      +0.00j   f=    0.0 Hz   zeta=+1.000

Sistema ESTABLE (max Re=-50.01)
Nota: el modo a ~21 Hz, zeta 0.71, es el de la PLL (f_pll=30 Hz)."""

R_P2 = """Parte real de la impedancia de salida, eje q  Re(Z_qq) [ohm]:
   f[Hz]   f_pll=30  f_pll=100
       1     -33.51     -33.54
       5     -32.62     -33.48
      10     -30.12     -33.18
      20     -23.48     -31.81
      50      -8.82     -24.06
     100      -0.01     -11.16

Re(Z_qq) < 0 = comportamiento NO PASIVO (resistencia negativa) inducido por la PLL.
Con PLL rapida se mantiene negativa hasta mas alta frecuencia -> mas riesgo en red debil."""

R_P3 = """(A) SCR critico (modelo acoplado) = 3.478  [inestable por debajo]
(B) SCR critico (Nyquist impedancia) = 3.551
    diferencia = 0.073

SCR critico vs f_pll:
  f_pll=  40 Hz -> SCR critico = 1.00
  f_pll=  60 Hz -> SCR critico = 1.49
  f_pll=  80 Hz -> SCR critico = 2.41
  f_pll= 100 Hz -> SCR critico = 3.48
  f_pll= 130 Hz -> SCR critico = 5.29
  f_pll= 170 Hz -> SCR critico = 8.00"""

R_CMP = """SCR critico GFM (inestable por ENCIMA) ~ 3.35
SCR critico GFL (inestable por DEBAJO) ~ 3.48"""


HEAD = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GFL · Tesis técnica — impedancia e inestabilidad en red débil</title>
<style>
  :root{
    --bg:#0f1419; --panel:#161d26; --panel2:#1c2530; --ink:#e6edf3; --muted:#9aa7b4;
    --acc:#4ea3ff; --acc2:#ffb454; --ok:#5ad19a; --bad:#ff6b6b; --line:#2a3542;
    --f1:#4ea3ff; --f2:#a78bfa; --f3:#5ad19a; --f4:#ff7eb6;
  }
  *{box-sizing:border-box}
  html{scroll-behavior:smooth}
  body{margin:0;background:var(--bg);color:var(--ink);
    font:15px/1.75 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}
  a{color:var(--acc);text-decoration:none} a:hover{text-decoration:underline}
  .wrap{display:flex;max-width:1560px;margin:0 auto}
  nav{position:sticky;top:0;align-self:flex-start;height:100vh;width:320px;flex:0 0 320px;
    overflow-y:auto;padding:24px 18px;border-right:1px solid var(--line);background:var(--panel)}
  nav h2{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:18px 0 6px}
  nav a{display:block;color:var(--muted);padding:4px 10px;border-radius:7px;font-size:13px;margin:1px 0}
  nav a:hover{background:var(--panel2);color:var(--ink);text-decoration:none}
  nav a.active{background:#23456b;color:#fff}
  nav .badge{font-size:10px;padding:1px 6px;border-radius:5px;margin-right:6px;color:#0b0e12;font-weight:700}
  main{flex:1;min-width:0;padding:40px 60px 160px;max-width:1080px}
  header.hero{padding:14px 0 26px;border-bottom:1px solid var(--line);margin-bottom:30px}
  header.hero h1{font-size:33px;margin:0 0 8px;line-height:1.18}
  header.hero .sub{color:var(--muted);font-size:17px;margin:4px 0}
  header.hero .meta{color:var(--muted);font-size:13px;margin-top:10px}
  .tagrow{margin-top:14px;display:flex;gap:8px;flex-wrap:wrap}
  .tag{background:var(--panel2);border:1px solid var(--line);color:var(--muted);
    padding:3px 11px;border-radius:20px;font-size:12.5px}
  section{margin:58px 0;scroll-margin-top:20px}
  .part{margin:70px 0 0;padding:10px 0 6px;border-bottom:2px solid var(--acc);color:var(--acc);
    font-size:13px;letter-spacing:.14em;text-transform:uppercase;font-weight:700}
  h2.sec{font-size:26px;margin:6px 0 4px;padding-bottom:8px;border-bottom:2px solid var(--line)}
  h3{font-size:19.5px;margin:32px 0 8px;color:#cdd9e5}
  h4{font-size:16px;margin:20px 0 6px;color:#bcc9d6}
  .lead{color:var(--muted);font-size:15.5px;margin:6px 0 18px;font-style:italic}
  p{margin:11px 0}
  .card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:20px 22px;margin:16px 0}
  .grid2{display:grid;grid-template-columns:1fr 1fr;gap:18px}
  .grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
  @media(max-width:1100px){.grid2,.grid3{grid-template-columns:1fr}}
  pre{background:#0b0f14;border:1px solid var(--line);border-radius:10px;padding:15px 17px;
    overflow-x:auto;font:12.5px/1.5 "SF Mono",Menlo,Consolas,monospace;color:#cfe3f5;margin:0}
  code.inl{background:var(--panel2);padding:1.5px 6px;border-radius:5px;font:12.5px monospace;color:#ffd9a0}
  .codefile{margin:18px 0;border:1px solid var(--line);border-radius:10px;overflow:hidden}
  .codefile>.h{background:#0b1118;padding:7px 14px;font:12px monospace;color:#7fd7ff;
    border-bottom:1px solid var(--line);display:flex;justify-content:space-between;gap:10px}
  .codefile pre{border:0;border-radius:0}
  .cap{font-size:12.5px;color:var(--muted);margin:6px 2px 0;font-style:italic}
  .console{background:#0a0e12;border:1px solid #1f3a2a;border-left:3px solid var(--ok);
    border-radius:0 8px 8px 0;padding:12px 16px;font:12.5px/1.5 "SF Mono",Menlo,Consolas,monospace;
    color:#bfe8d2;overflow-x:auto;white-space:pre;margin:14px 0}
  .file{display:inline-block;background:#13202e;border:1px solid #244;color:#7fd7ff;
    padding:1px 8px;border-radius:6px;font:12px monospace;margin:2px 4px 2px 0}
  table{width:100%;border-collapse:collapse;margin:14px 0;font-size:13.5px}
  th,td{border:1px solid var(--line);padding:8px 11px;text-align:left;vertical-align:top}
  th{background:var(--panel2);color:#cdd9e5;font-weight:600}
  td code{color:#ffd9a0}
  figure{margin:16px 0;background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px;text-align:center}
  figure img{max-width:100%;border-radius:8px;background:#fff}
  figcaption{color:var(--muted);font-size:13px;margin-top:10px}
  .pill{display:inline-block;padding:2px 10px;border-radius:20px;font-size:12px;font-weight:600}
  .pill.ok{background:#10341f;color:var(--ok);border:1px solid #1f5e39}
  .pill.bad{background:#3a1414;color:var(--bad);border:1px solid #5e1f1f}
  .pill.warn{background:#3a2c10;color:var(--acc2);border:1px solid #5e451f}
  .kpi{display:flex;gap:14px;flex-wrap:wrap;margin:14px 0}
  .kpi .b{background:var(--panel2);border:1px solid var(--line);border-radius:10px;padding:12px 16px;min-width:128px}
  .kpi .b .n{font-size:22px;font-weight:700;color:#fff}
  .kpi .b .l{font-size:12px;color:var(--muted)}
  .phase-h{display:flex;align-items:center;gap:12px;margin-bottom:2px}
  .phase-n{width:40px;height:40px;border-radius:10px;display:grid;place-items:center;font-weight:800;color:#0b0e12;font-size:19px}
  .note{background:#13202e;border-left:3px solid var(--acc);padding:10px 15px;border-radius:0 8px 8px 0;margin:14px 0;color:#cfe1f0}
  .warn-box{background:#2a1d10;border-left:3px solid var(--acc2);padding:10px 15px;border-radius:0 8px 8px 0;margin:14px 0;color:#f0e1cf}
  .def{background:#101c1a;border-left:3px solid var(--ok);padding:10px 15px;border-radius:0 8px 8px 0;margin:14px 0;color:#d4ece2}
  .flow{display:flex;align-items:stretch;gap:0;flex-wrap:wrap;margin:18px 0}
  .flow .n{flex:1;min-width:140px;background:var(--panel2);border:1px solid var(--line);border-radius:10px;padding:12px;text-align:center;font-size:13px}
  .flow .ar{display:grid;place-items:center;color:var(--muted);font-size:22px;padding:0 6px}
  ul.tight li{margin:5px 0} ol.tight li{margin:6px 0}
  .eq{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--acc2);
    border-radius:0 10px 10px 0;padding:6px 18px;margin:14px 0;overflow-x:auto}
  mjx-container{color:#e6edf3}
  .twocol{column-count:2;column-gap:26px} @media(max-width:1100px){.twocol{column-count:1}}
  .small{font-size:13px;color:var(--muted)}
  .repolinks{margin:16px 0;padding:11px 15px;background:#13202e;border:1px dashed var(--acc);border-radius:8px;font-size:13px;color:var(--muted)}
  .repolinks a{color:#7fd7ff}.repolinks b{color:#cfe1f0}
  /* --- responsive: movil / pantalla estrecha --- */
  @media(max-width:820px){
    .wrap{flex-direction:column}
    nav{position:static;height:auto;width:100%;flex:none;border-right:0;
      border-bottom:1px solid var(--line);max-height:42vh}
    main{padding:24px 18px 90px;max-width:100%}
    header.hero h1{font-size:24px} h2.sec{font-size:21px}
    .grid2,.grid3{grid-template-columns:1fr}
    pre,.console{font-size:11.5px}
    table{font-size:12px} th,td{padding:6px 7px}
  }
</style>
<script>
  window.MathJax = {tex:{inlineMath:[['\\\\(','\\\\)']], displayMath:[['\\\\[','\\\\]']]},
                    svg:{fontCache:'global'}};
</script>
<script async src="../00%20-%20Repositorio/assets/mathjax-tex-svg.js"></script>
</head>
<body>
<div class="wrap">
"""

NAV = """<nav id="nav">
  <h2>Portada</h2>
  <a href="#resumen">Resumen / Abstract</a>
  <a href="#nomenclatura">Nomenclatura</a>
  <a href="#indice">Índice y alcance</a>
  <h2>I · Preliminares</h2>
  <a href="#problema">1 · Planteamiento del problema</a>
  <a href="#marco">2 · Estado del arte y marco teórico</a>
  <a href="#sw">3 · Software y método</a>
  <h2>II · Modelado</h2>
  <a href="#fisica">4 · Sistema físico</a>
  <a href="#marcos">5 · Marcos de referencia</a>
  <a href="#estados">6 · Designación de los 10 estados</a>
  <a href="#parametros">7 · Parámetros (params.py)</a>
  <a href="#modelomat">8 · Modelo matemático (model.py)</a>
  <a href="#equilibrio">9 · Equilibrio y linealización</a>
  <h2>III · Desarrollo</h2>
  <a href="#f1"><span class="badge" style="background:var(--f1)">1</span>Estabilidad red rígida</a>
  <a href="#f2"><span class="badge" style="background:var(--f2)">2</span>Impedancia: R negativa</a>
  <a href="#f3"><span class="badge" style="background:var(--f3)">3</span>Inestabilidad red débil</a>
  <a href="#comp"><span class="badge" style="background:var(--f4)">★</span>GFM vs GFL</a>
  <h2>IV · Cierre</h2>
  <a href="#discusion">10 · Discusión global</a>
  <a href="#lecciones">11 · Lecciones aprendidas</a>
  <a href="#concl">12 · Conclusiones y aportaciones</a>
  <a href="#biblio">Bibliografía</a>
  <h2>Apéndices</h2>
  <a href="#apA">A · Parámetros</a>
  <a href="#apB">B · Tabla de estados</a>
  <a href="#apC">C · Código fuente</a>
  <a href="#apD">D · Resultados de consola</a>
  <a href="#apE">E · Reproducir</a>
  <a href="#apF">F · Glosario</a>
  <h2>Enlaces</h2>
  <a href="../00%20-%20Repositorio/index.html">📚 Repositorio</a>
  <a href="../01%20-%20GFM-Impedance/informe.html">📁 01 · GFM</a>
  <a href="../03%20-%20Energia-DataCenter-IA/informe.html">📁 03 · DataCenter</a>
</nav>
<main>
"""

FECHA = datetime.date.today().strftime("%d/%m/%Y")

HERO = r"""<header class="hero">
  <h1>Inversor grid-following: impedancia e inestabilidad en red débil</h1>
  <p class="sub">Informe técnico exhaustivo — el espejo del grid-forming. Modelo de pequeña señal de 10
  estados (PLL + lazo de corriente), impedancia de salida, resistencia negativa de la PLL y SCR crítico,
  con el código de simulación real y sus resultados.</p>
  <p class="meta">Proyecto 02 · Repositorio de aprendizaje de ingeniería de control · Generado el """ + FECHA + r""" a partir del código fuente.</p>
  <div class="tagrow">
    <span class="tag">Python 3.13</span><span class="tag">marco dq</span><span class="tag">SRF-PLL</span>
    <span class="tag">impedancia dq 2×2</span><span class="tag">resistencia negativa</span>
    <span class="tag">Nyquist generalizado</span><span class="tag">red débil / SCR</span>
  </div>
</header>
"""

S = []

S.append(r"""
<section id="resumen">
  <h2 class="sec">Resumen ejecutivo</h2>
  <p class="lead">El espejo del proyecto 01: mismo hardware, control opuesto, inestabilidad opuesta.</p>
  <p>Sobre el <b>mismo filtro LCL</b> del proyecto 01 (10&nbsp;kVA), se implementa el control
  <b>grid-following (GFL)</b>: una PLL que sigue la red y un lazo de corriente que inyecta la potencia
  de consigna. El objetivo es entender, con la misma herramienta de impedancia, por qué el GFL <b>se
  desestabiliza en red débil</b> —lo opuesto al grid-forming— y demostrar que el formalismo de
  impedancia es general (explica ambos). Como en el proyecto 01, todo el código mostrado es el código
  real y todos los números son la salida de consola real de ejecutarlo.</p>
  <div class="kpi">
    <div class="b"><div class="n">10</div><div class="l">estados del modelo dq</div></div>
    <div class="b"><div class="n">−50.0</div><div class="l">máx. Re (red rígida)</div></div>
    <div class="b"><div class="n">21.3 Hz</div><div class="l">modo PLL, ζ=0.71</div></div>
    <div class="b"><div class="n">Re(Z<sub>qq</sub>)&lt;0</div><div class="l">resistencia negativa PLL</div></div>
    <div class="b"><div class="n">3.48</div><div class="l">SCR crítico (PLL 100 Hz)</div></div>
    <div class="b"><div class="n">2 %</div><div class="l">acuerdo de las dos vías</div></div>
  </div>
  <div class="def"><b>Idea central:</b> el GFL es estable en red fuerte e inestable en red débil si la
  PLL es rápida. El <b>ancho de banda de la PLL</b> fija el SCR crítico de forma monótona: 40&nbsp;Hz →
  SCR≈1 (robusto); 170&nbsp;Hz → SCR≈8 (frágil). Es lo contrario del GFM (inestable en red fuerte), y se
  explica con la misma impedancia + Nyquist generalizado.</div>

  <h3>Resumen</h3>
  <p>Se presenta el modelado en pequeña señal y el análisis de estabilidad por impedancia de un inversor
  grid-following trifásico de 10&nbsp;kVA con filtro LCL (el mismo hardware del proyecto 01), controlado
  mediante una PLL de marco síncrono y un lazo de corriente. El modelo no lineal en \( dq \), de diez
  variables de estado, se linealiza numéricamente para obtener los modos propios y la matriz de impedancia
  de salida \( \mathbf{Z}_{dq}(s) \). Se identifica la <b>resistencia negativa</b> que la PLL induce en el
  eje q (comportamiento no pasivo) y, mediante el criterio de Nyquist generalizado, se determina la
  relación de cortocircuito (SCR) crítica por debajo de la cual el sistema se inestabiliza en red débil.
  Se demuestra que el ancho de banda de la PLL gobierna monótonamente dicha frontera y se cierra la
  dualidad grid-forming↔grid-following con la misma herramienta de impedancia.</p>
  <p><b>Palabras clave:</b> inversor grid-following; PLL de marco síncrono; resistencia negativa;
  estabilidad por impedancia; Nyquist generalizado; red débil; SCR.</p>

  <h3>Abstract</h3>
  <p>This work presents the small-signal modelling and impedance-based stability analysis of a 10&nbsp;kVA
  three-phase grid-following inverter with an LCL filter (the same hardware as project 01), controlled by
  a synchronous-reference-frame PLL and a current loop. A ten-state nonlinear \( dq \) model is linearised
  numerically to obtain the modal eigenvalues and the output impedance matrix \( \mathbf{Z}_{dq}(s) \).
  The <b>negative resistance</b> induced by the PLL on the q axis (non-passive behaviour) is identified
  and, via the generalised Nyquist criterion, the critical short-circuit ratio (SCR) below which the
  system becomes unstable in weak grids is determined. The PLL bandwidth is shown to monotonically govern
  that boundary, closing the grid-forming↔grid-following duality with the same impedance tool.</p>
  <p><b>Keywords:</b> grid-following inverter; synchronous-reference-frame PLL; negative resistance;
  impedance-based stability; generalised Nyquist; weak grid; SCR.</p>
</section>

<section id="nomenclatura">
  <h2 class="sec">Nomenclatura</h2>
  <div class="grid2">
    <div>
      <h3>Magnitudes y parámetros</h3>
      <table>
        <tr><th>Símbolo</th><th>Significado</th></tr>
        <tr><td>\( \mathbf{i}_{L1},\mathbf{v}_C,\mathbf{i}_{L2} \)</td><td>estados del filtro LCL (d,q)</td></tr>
        <tr><td>\( \delta \)</td><td>ángulo del marco de la PLL − marco red</td></tr>
        <tr><td>\( \varepsilon \)</td><td>integrador del PI de la PLL</td></tr>
        <tr><td>\( \gamma_d,\gamma_q \)</td><td>integradores del PI de corriente</td></tr>
        <tr><td>\( \omega_\text{pll} \)</td><td>frecuencia estimada por la PLL</td></tr>
        <tr><td>\( P^*,Q^* \)</td><td>consignas de potencia activa/reactiva</td></tr>
        <tr><td>\( f_\text{pll},\zeta \)</td><td>ancho de banda y amort. de la PLL</td></tr>
        <tr><td>\( K_p^\text{pll},K_i^\text{pll} \)</td><td>ganancias de la PLL</td></tr>
      </table>
    </div>
    <div>
      <h3>Modelo y acrónimos</h3>
      <table>
        <tr><th>Símbolo / sigla</th><th>Significado</th></tr>
        <tr><td>\( A,B,C,D \)</td><td>matrices del modelo lineal</td></tr>
        <tr><td>\( \mathbf{Y}_\text{inv},\mathbf{Z}_\text{inv} \)</td><td>admitancia / impedancia de salida</td></tr>
        <tr><td>\( \mathbf{L}(s) \)</td><td>\( Z_\text{red}Y_\text{inv} \) (minor loop gain)</td></tr>
        <tr><td>GFL / GFM</td><td>grid-following / grid-forming</td></tr>
        <tr><td>PLL (SRF)</td><td>phase-locked loop de marco síncrono</td></tr>
        <tr><td>SCR / X·R</td><td>short-circuit ratio / razón X/R</td></tr>
        <tr><td>LCL</td><td>filtro inductor-condensador-inductor</td></tr>
      </table>
    </div>
  </div>
</section>

<section id="indice">
  <h2 class="sec">Índice, objetivos y alcance</h2>
  <h3>Objetivos</h3>
  <ol class="tight">
    <li><b>Modelar</b> el GFL en dq (PLL SRF + lazo de corriente) sobre el LCL del proyecto 01.</li>
    <li><b>Caracterizar</b> su impedancia de salida y exponer la <b>resistencia negativa</b> de la PLL.</li>
    <li><b>Hallar</b> el SCR crítico por dos vías (autovalores y Nyquist de impedancia) y mostrar el
    papel del ancho de banda de la PLL.</li>
    <li><b>Comparar</b> con el GFM (proyecto 01) para cerrar la dualidad GFM↔GFL.</li>
  </ol>
  <div class="flow">
    <div class="n"><b>I. Preliminares</b><br>problema, teoría, método</div><div class="ar">→</div>
    <div class="n"><b>II. Modelado</b><br>físico → 10 estados → código</div><div class="ar">→</div>
    <div class="n"><b>III. Fases 1–3 + ★</b><br>código y resultados</div><div class="ar">→</div>
    <div class="n"><b>IV. Cierre</b><br>lecciones, conclusiones</div>
  </div>
  <div class="note"><b>Convenio:</b> bloques <span class="file">📄 fichero.py</span> = código real;
  bloques verdes = salida de consola real. Fórmulas en MathJax.</div>
</section>
""")

S.append(r"""<div class="part">Parte I · Preliminares</div>

<section id="problema">
  <h2 class="sec">1 · Planteamiento del problema</h2>
  <p class="lead">¿Por qué un inversor que "solo sigue a la red" se vuelve inestable en red débil?</p>
  <h3>1.1 El grid-following es la arquitectura dominante</h3>
  <p>Casi todo el parque fotovoltaico y eólico instalado es grid-following: mide el ángulo de red con
  una PLL e inyecta la corriente que entrega la potencia deseada. Es sencillo y eficiente <b>mientras la
  red sea fuerte</b>. El problema aparece cuando la red se debilita (se llena de convertidores y pierde
  máquinas síncronas): el GFL empieza a oscilar. Entender ese límite es el objeto de este proyecto.</p>
  <div class="grid2">
    <div class="card"><h3>El grid-following</h3>
      <p>La PLL alinea el marco dq con la tensión de red (lleva \( v_{Cq}\to 0 \)) y el lazo de corriente
      impone \( i_{L1} \) para entregar \( P^*,Q^* \). Se comporta como fuente de corriente.</p></div>
    <div class="card"><h3>El mecanismo de inestabilidad</h3>
      <p>En red débil (alta \( L_g \)), la corriente inyectada perturba la tensión del PCC que la PLL
      mide. La PLL corrige el ángulo → cambia la corriente → vuelve a perturbar la tensión. Si la PLL es
      rápida, el lazo se cierra con fase desfavorable y oscila.</p></div>
  </div>
  <h3>1.2 El lazo oculto PLL ↔ red</h3>
  <div class="flow">
    <div class="n">PLL mide \( v_{pcc} \)</div><div class="ar">→</div>
    <div class="n">lazo corriente inyecta \( i_g \)</div><div class="ar">→</div>
    <div class="n">\( i_g \) sobre \( Z_\text{red} \) mueve \( v_{pcc} \)</div><div class="ar">↺</div>
  </div>
  <p>Con red fuerte (\( Z_\text{red}\approx 0 \)) el lazo está "abierto" y la PLL trabaja contra una
  referencia firme. Con red débil el lazo se cierra; el análisis de impedancia lo traduce a una
  condición cuantitativa: la resistencia negativa de la PLL (Fase 2).</p>
  <div class="repolinks"><b>📚 En el repositorio:</b>
    <a href="../00%20-%20Repositorio/index.html#grid-forming-vs-following">GFM vs GFL</a> ·
    <a href="../00%20-%20Repositorio/index.html#pll-srf">SRF-PLL</a> ·
    <a href="../00%20-%20Repositorio/index.html#interaccion-pll-red-debil">Interacción PLL–red débil</a></div>
</section>

<section id="marco">
  <h2 class="sec">2 · Estado del arte y marco teórico</h2>
  <p class="lead">Antecedentes y fundamentos de la inestabilidad PLL–red débil.</p>

  <h3>2.1 Estado del arte</h3>
  <p>El inversor grid-following es la arquitectura predominante del parque renovable: sincroniza con la
  red mediante una PLL e inyecta corriente [5]. Su talón de Aquiles es la operación en <b>redes
  débiles</b>: numerosos trabajos han mostrado que la interacción entre la dinámica de la PLL y la
  impedancia de red da lugar a oscilaciones e inestabilidad cuando el SCR es bajo [5],[6]. El enfoque de
  <b>impedancia</b> [4] —caracterizar el convertidor por su admitancia de salida \( \mathbf{Y}_\text{inv} \)
  y aplicar el criterio de Nyquist generalizado al producto con \( \mathbf{Z}_\text{red} \)— se ha
  consolidado como la herramienta estándar para predecir estas inestabilidades, y revela que el lazo de
  la PLL introduce una <b>parte real negativa</b> (comportamiento no pasivo) en la impedancia de salida
  [6]. Este proyecto reproduce ese fenómeno sobre el mismo hardware del grid-forming del proyecto 01,
  cerrando la dualidad entre ambas arquitecturas [7],[8] con un único formalismo.</p>

  <h3>2.2 La PLL de marco síncrono: derivación de segundo orden</h3>
  <p>Una SRF-PLL es un lazo de control que lleva \( v_{Cq}\to 0 \). Para una desviación de ángulo
  pequeña \( \Delta\theta \), la componente q de la tensión es \( v_{Cq}\approx V_0\,\Delta\theta \). El
  PI de la PLL genera la frecuencia \( \omega_\text{pll}=\omega_0+K_p^\text{pll}v_{Cq}+K_i^\text{pll}\!\int v_{Cq} \),
  y \( \dot{\Delta\theta}=\omega_\text{pll}-\omega_0 \). Sustituyendo, la dinámica del error de fase es:</p>
  <div class="eq">\[ \ddot{\Delta\theta}+K_p^\text{pll}V_0\,\dot{\Delta\theta}+K_i^\text{pll}V_0\,\Delta\theta=0
     \;\Rightarrow\; \omega_n=\sqrt{K_i^\text{pll}V_0},\quad \zeta=\frac{K_p^\text{pll}V_0}{2\omega_n} \]</div>
  <p>Igualando a una respuesta de segundo orden objetivo (\( \omega_n=2\pi f_\text{pll} \),
  \( \zeta=0.707 \)) se despejan \( K_i^\text{pll}=\omega_n^2/V_0 \) y
  \( K_p^\text{pll}=2\zeta\omega_n/V_0 \) —exactamente las expresiones de
  <span class="file">params.py</span>—. La normalización por \( V_0 \) hace el ancho de banda
  independiente del nivel de tensión. Este modo de segundo orden es el "modo de la PLL" que aparece en
  el mapa de polos a ~21&nbsp;Hz.</p>

  <h3>2.3 Pasividad y resistencia negativa</h3>
  <p>Una impedancia con \( \mathrm{Re}\{Z(j\omega)\}>0 \) disipa energía (pasiva, amortigua); con
  \( \mathrm{Re}\{Z\}<0 \) la aporta (activa, desamortigua). La PLL, al reaccionar a \( v_{Cq} \) con la
  fase de un PI, crea —vista desde la red— una conductancia negativa en el eje q en su banda de
  actuación. La <b>pasividad</b> (signo de \( \mathrm{Re}\{Z\} \)) es por ello un criterio rápido de
  riesgo: una región de no pasividad es condición necesaria para la inestabilidad, que se materializa al
  resonar esa resistencia negativa con la reactancia inductiva de la red débil.</p>

  <h3>2.4 Impedancia y criterio de Nyquist generalizado</h3>
  <p>Del modelo lineal, \( \mathbf{Y}_\text{inv}=-(\mathbf{C}(s\mathbf{I}-A)^{-1}\mathbf{B}+\mathbf{D}) \).
  La estabilidad de la conexión la decide \( \mathbf{L}(s)=\mathbf{Z}_\text{red}\mathbf{Y}_\text{inv} \)
  (MIMO 2×2): los autovalores de \( \mathbf{L}(j\omega) \) no deben rodear \( -1 \), o equivalentemente
  \( \det(\mathbf{I}+\mathbf{L})\neq 0\ \forall\omega \). El mínimo de
  \( |\det(\mathbf{I}+\mathbf{L})| \) marca la frontera (SCR crítico). Es el mismo criterio del
  proyecto 01, lo que evidencia su generalidad.</p>

  <div class="repolinks"><b>📚 En el repositorio:</b>
    <a href="../00%20-%20Repositorio/index.html#pll-srf">SRF-PLL</a> ·
    <a href="../00%20-%20Repositorio/index.html#no-pasividad-resistencia-negativa">Resistencia negativa</a> ·
    <a href="../00%20-%20Repositorio/index.html#nyquist-generalizado">Nyquist generalizado</a></div>
</section>

<section id="sw">
  <h2 class="sec">3 · Software y método</h2>
  <p class="lead">Mismo flujo del proyecto 01; comparte utilidades de análisis.</p>
  <p>Todo en Python (NumPy, SciPy, Matplotlib). El método es idéntico al del proyecto 01: modelo no
  lineal \( f(\mathbf{x},\mathbf{u}) \) → equilibrio con <code class="inl">fsolve</code> → linealización
  numérica por diferencias centradas → \( Y(s) \) → Nyquist generalizado. Lo único que cambia es la capa
  de control del modelo. De hecho, <span class="file">impedance.py</span> y
  <span class="file">grid.py</span> son los mismos que en el proyecto 01, y
  <span class="file">main_compare.py</span> carga el modelo del GFM con <code class="inl">importlib</code>
  para superponer ambas curvas. Esto demuestra que la herramienta de impedancia es general.</p>
  <div class="repolinks"><b>📚 En el repositorio:</b>
    <a href="../00%20-%20Repositorio/index.html#linealizacion-numerica">Linealización numérica</a> ·
    <a href="../00%20-%20Repositorio/index.html#equilibrio-fsolve">Equilibrio (fsolve)</a></div>
</section>
""")

S.append(r"""<div class="part">Parte II · Modelado</div>

<section id="fisica">
  <h2 class="sec">4 · El sistema físico</h2>
  <p class="lead">Mismo hardware que el GFM; la diferencia está toda en el control.</p>
  <h3>4.1 La planta: filtro LCL idéntico al proyecto 01</h3>
  <p>El inversor, el filtro LCL y la conexión a red son los del proyecto 01 (\( L_1=2 \) mH,
  \( C_f=20 \) µF, \( L_2=1 \) mH, resonancia ~1.1&nbsp;kHz). Mantener la planta fija y cambiar solo el
  control hace de esto un <b>experimento controlado</b>: cualquier diferencia de comportamiento es del
  control, no del hardware.</p>
  <h3>4.2 La capa de control: PLL + lazo de corriente</h3>
  <div class="twocol">
  <p><b>La PLL (SRF).</b> Mide \( v_C \), la proyecta sobre el eje q y ajusta la frecuencia del marco
  para llevar \( v_{Cq}\to 0 \). Es un PI sobre \( v_{Cq} \). Cuando bloquea, el ángulo del marco sigue
  al de la red.</p>
  <p><b>El lazo de corriente.</b> Con la PLL alineando \( v_C \) al eje d, la potencia activa la fija
  \( i_{L1d} \) y la reactiva \( i_{L1q} \). Es un PI rápido (~800&nbsp;Hz) con desacoplo dq y
  feedforward de \( v_C \).</p>
  </div>
  <h3>4.3 La diferencia conceptual clave</h3>
  <table>
    <tr><th></th><th>Grid-forming (01)</th><th>Grid-following (02)</th></tr>
    <tr><td>Quién fija el ángulo</td><td>el droop/VSM (interno)</td><td>la PLL (sigue la red)</td></tr>
    <tr><td>Se comporta como</td><td>fuente de tensión</td><td>fuente de corriente</td></tr>
    <tr><td>Variable controlada</td><td>tensión \( v_C \)</td><td>corriente \( i_{L1} \)</td></tr>
    <tr><td>Falla en</td><td>red fuerte</td><td>red débil</td></tr>
  </table>
  <div class="repolinks"><b>📚 En el repositorio:</b>
    <a href="../00%20-%20Repositorio/index.html#filtro-lcl">Filtro LCL</a> ·
    <a href="../00%20-%20Repositorio/index.html#pll-srf">SRF-PLL</a> ·
    <a href="../00%20-%20Repositorio/index.html#control-cascada">Control en cascada</a></div>
</section>

<section id="marcos">
  <h2 class="sec">5 · Marcos de referencia</h2>
  <p class="lead">Dos marcos, pero el ángulo lo da la PLL (no el droop).</p>
  <p>Como en el GFM hay un marco de red (gira a \( \omega_0 \)) y uno de control. La diferencia: aquí el
  marco de control lo gira la <b>PLL</b>. El ángulo \( \delta=\theta_\text{pll}-\theta_s \) sigue
  acoplando lo eléctrico con la sincronización, pero su dinámica es la de un lazo de seguimiento:</p>
  <div class="eq">\[ \dot\delta=\omega_\text{pll}-\omega_0,\qquad
     \omega_\text{pll}=\omega_0+K_p^\text{pll}\,v_{Cq}+K_i^\text{pll}\,\varepsilon,\qquad
     \dot\varepsilon=v_{Cq} \]</div>
  <p>Aquí nace la resistencia negativa: la PLL, al reaccionar a \( v_{Cq} \), introduce una
  realimentación que en cierta banda se comporta como conductancia negativa vista desde la red.</p>
</section>

<section id="estados">
  <h2 class="sec">6 · Designación de los 10 estados</h2>
  <p class="lead">Cuáles son, de dónde sale cada uno y por qué es estado.</p>
  <table>
    <tr><th>#</th><th>Estado</th><th>Por qué es estado</th><th>Derivada</th></tr>
    <tr><td>0,1</td><td><code>iL1d, iL1q</code></td><td>corriente en \( L_1 \)</td><td>\( L_1\dot{\mathbf{i}}_{L1}=\mathbf{v}_i-\mathbf{v}_C-R_1\mathbf{i}_{L1}+\omega L_1\mathbf{J}\mathbf{i}_{L1} \)</td></tr>
    <tr><td>2,3</td><td><code>vcd, vcq</code></td><td>tensión en \( C_f \)</td><td>\( C_f\dot{\mathbf{v}}_C=\mathbf{i}_{L1}-\mathbf{i}_{L2}+\omega C_f\mathbf{J}\mathbf{v}_C \)</td></tr>
    <tr><td>4,5</td><td><code>iL2d, iL2q</code></td><td>corriente en \( L_2 \) (= \( i_g \))</td><td>\( L_2\dot{\mathbf{i}}_{L2}=\mathbf{v}_C-\mathbf{v}_{pcc}-R_2\mathbf{i}_{L2}+\omega L_2\mathbf{J}\mathbf{i}_{L2} \)</td></tr>
    <tr><td>6</td><td><code>delta</code></td><td>ángulo del marco de la PLL</td><td>\( \dot\delta=\omega_\text{pll}-\omega_0 \)</td></tr>
    <tr><td>7</td><td><code>eps</code></td><td>integrador del PI de la PLL</td><td>\( \dot\varepsilon=v_{Cq} \)</td></tr>
    <tr><td>8,9</td><td><code>gd, gq</code></td><td>integradores del PI de corriente</td><td>\( \dot{\boldsymbol{\gamma}}=\mathbf{i}_{L1}^*-\mathbf{i}_{L1} \)</td></tr>
  </table>
  <p>Frente a los 15 del GFM, el GFL tiene 10: comparten los 6 de la planta LCL, pero el GFL sustituye
  los 9 estados de sincronización del GFM (droop, potencias, impedancia virtual, R transitoria) por solo
  4 (PLL + lazo de corriente). Es la lista real <code class="inl">STATE_NAMES</code> de
  <span class="file">model.py</span>; la Fase&nbsp;1 devuelve 10 autovalores, confirmándolo.</p>
</section>

<section id="parametros">
  <h2 class="sec">7 · Parámetros <span class="file">params.py</span></h2>
  <p class="lead">LCL igual que el 01; control PLL+corriente. Las ganancias se derivan.</p>
  <p>El lazo de corriente se sintoniza por cancelación de polo (\( K_{p,i}=L_1\omega_{ci} \),
  \( K_{i,i}=R_1\omega_{ci} \), con \( f_{ci}=800 \) Hz). La PLL es de segundo orden: dados
  \( f_\text{pll} \) y \( \zeta \), \( K_i^\text{pll}=\omega_n^2/V_0 \) y
  \( K_p^\text{pll}=2\zeta\omega_n/V_0 \); la normalización por \( V_0 \) hace el ancho de banda
  independiente del punto de tensión.</p>
""" + embed("params.py") + r"""
</section>

<section id="modelomat">
  <h2 class="sec">8 · Modelo matemático <span class="file">model.py</span></h2>
  <p class="lead">El campo vectorial \( f(\mathbf{x},\mathbf{u}) \) del GFL en 10 ecuaciones.</p>
  <p>Se lee de arriba abajo: primero la <b>PLL</b> (frecuencia del marco desde \( v_{Cq} \)), luego las
  <b>referencias de corriente</b> desde \( P^*,Q^* \), el <b>lazo de corriente PI</b> con desacoplo y
  feedforward, el <b>amortiguamiento activo</b>, la <b>rotación</b> de la tensión de red por \( \delta \),
  y la <b>planta LCL</b>. Las referencias \( i^*_{L1d}=2P^*/(3v_{Cd}) \),
  \( i^*_{L1q}=-2Q^*/(3v_{Cd}) \) son las que convierten al inversor en fuente de corriente.</p>
""" + embed("model.py",
  "GFLInverter: f(x,u), output (rota i_L2 al marco s), equilibrium (fsolve) y linearize (diferencias "
  "centradas). La PLL fija w; el lazo de corriente impone i_L1.") + r"""
  <div class="note"><b>Detalle clave:</b> <code class="inl">w = w0 + Kp_pll*vcq + Ki_pll*eps</code> es la
  PLL; <code class="inl">vmag = max(vcd, 1.0)</code> evita dividir por cero en las referencias. La planta
  LCL es idéntica a la del GFM (mismo hardware).</div>
</section>

<section id="equilibrio">
  <h2 class="sec">9 · Equilibrio y linealización</h2>
  <p class="lead">Idéntico método al proyecto 01.</p>
  <p>El equilibrio se halla con <code class="inl">fsolve</code> desde un guess físico; la Fase&nbsp;1
  confirma residual \( \approx 1.8\times10^{-11} \), \( P_\text{eq}=5000 \) W y \( v_{Cq}\approx 0 \) (la
  PLL bloqueada, \( \sim 10^{-28} \)). La linealización es por diferencias centradas escaladas, igual que
  en el proyecto 01. <span class="file">impedance.py</span> (compartido) construye
  \( Y=-G \), \( Z=Y^{-1} \).</p>
""" + embed("impedance.py", "Compartido con el proyecto 01 (importa GFLInverter con alias). Y=-G, Z=inv(Y).") + r"""
</section>
""")

S.append(r"""<div class="part">Parte III · Desarrollo</div>

<section id="f1">
  <div class="phase-h"><div class="phase-n" style="background:var(--f1)">1</div>
    <h2 class="sec" style="border:0;margin:0">Fase 1 · Estabilidad en red rígida</h2></div>
  <p class="lead">Punto de partida: con red fuerte el GFL es estable.</p>
""" + embed("main_phase1.py") + r"""
  <h3>1.1 Resultados reales</h3>
""" + console(R_P1) + r"""
  <div class="grid2">
    <figure><img src="results/polos_fase1.png" alt="polos GFL">
      <figcaption>Mapa de polos (red rígida): los 10 autovalores en el semiplano izquierdo.</figcaption></figure>
    <div>
      <p><span class="pill ok">ESTABLE</span> \( \max\mathrm{Re}=-50.0 \). El polo dominante es el
      <b>modo de la PLL</b> a <b>21.3 Hz con \( \zeta=0.708 \)</b> (diseñada a 30 Hz, \( \zeta=0.707 \);
      la diferencia refleja la interacción con la planta). Equilibrio: \( P=5000 \) W,
      \( v_{Cq}\approx 0 \) (la PLL alinea), \( \delta=0.54° \). La resonancia LCL aparece a ~950–1073 Hz.</p>
      <div class="note">El amplio margen \( -50 \) en red rígida es engañoso: se evapora al debilitar la
      red, porque la red débil cierra el lazo PLL↔red que aquí está casi abierto. La Fase&nbsp;3 lo
      cuantifica.</div>
    </div>
  </div>
</section>

<section id="f2">
  <div class="phase-h"><div class="phase-n" style="background:var(--f2)">2</div>
    <h2 class="sec" style="border:0;margin:0">Fase 2 · Impedancia: la resistencia negativa</h2></div>
  <p class="lead">La firma del GFL: parte real negativa en la banda de la PLL.</p>
""" + embed("main_phase2.py") + r"""
  <h3>2.1 Resultados reales</h3>
""" + console(R_P2) + r"""
  <div class="grid2">
    <figure><img src="results/impedancia_fase2.png" alt="impedancia GFL">
      <figcaption>Re(Z) por eje: Re(Z<sub>qq</sub>)&lt;0 (no pasivo). La PLL rápida la extiende.</figcaption></figure>
    <div>
      <p>La parte real de la impedancia es <b>negativa en el eje q</b> en la banda de la PLL: a 1&nbsp;Hz
      vale −33.5&nbsp;Ω. Con PLL rápida (100&nbsp;Hz) se mantiene negativa hasta más alta frecuencia (a
      100&nbsp;Hz: −11.2&nbsp;Ω, frente a −0.01 con 30&nbsp;Hz).</p>
      <div class="def"><b>Por qué en el eje q:</b> la PLL controla precisamente \( v_{Cq} \), así que toda
      su dinámica vive en ese eje. El eje d (que lleva la tensión) queda pasivo:
      \( \mathrm{Re}\{Z_{dd}\}>0 \), \( \mathrm{Re}\{Z_{qq}\}<0 \).</div>
    </div>
  </div>
  <div class="repolinks"><b>📚 En el repositorio:</b>
    <a href="../00%20-%20Repositorio/index.html#no-pasividad-resistencia-negativa">Resistencia negativa</a> ·
    <a href="../00%20-%20Repositorio/index.html#respuesta-frecuencia-ss">Respuesta en frecuencia</a></div>
</section>

<section id="f3">
  <div class="phase-h"><div class="phase-n" style="background:var(--f3)">3</div>
    <h2 class="sec" style="border:0;margin:0">Fase 3 · Inestabilidad en red débil</h2></div>
  <p class="lead">SCR crítico por dos vías y el papel del ancho de banda de la PLL.</p>
  <h3>3.1 La red Thévenin <span class="file">grid.py</span></h3>
""" + embed("grid.py", "Compartido con el proyecto 01. SCR y X/R -> (Rg, Lg); impedancia dq 2x2 con acoplamiento cruzado.") + r"""
  <h3>3.2 El driver</h3>
""" + embed("main_phase3.py") + r"""
  <h3>3.3 Resultados reales</h3>
""" + console(R_P3) + r"""
  <div class="grid2">
    <figure><img src="results/estabilidad_fase3.png" alt="estabilidad GFL">
      <figcaption>Izq.: Nyquist generalizado (envuelve −1 al bajar SCR). Der.: SCR crítico vs ancho de banda de la PLL.</figcaption></figure>
    <div>
      <table>
        <tr><th>Método</th><th>SCR crítico</th></tr>
        <tr><td>(A) Modelo acoplado</td><td><b>3.478</b></td></tr>
        <tr><td>(B) Nyquist de impedancia</td><td><b>3.551</b></td></tr>
        <tr><td colspan="2">Diferencia 0.073 → <span class="pill ok">~2 %</span></td></tr>
      </table>
      <p><b>Inestable por debajo del crítico</b> (red débil), lo opuesto al GFM. El barrido de
      \( f_\text{pll} \) es monótono: 40→1.00, 100→3.48, 170→8.00.</p>
      <div class="warn-box"><b>Compromiso de la PLL:</b> lenta = robusta en red débil pero peor
      seguimiento; rápida = buen seguimiento pero frágil. Este análisis da la frontera cuantitativa.</div>
    </div>
  </div>
  <div class="repolinks"><b>📚 En el repositorio:</b>
    <a href="../00%20-%20Repositorio/index.html#nyquist-generalizado">Nyquist generalizado</a> ·
    <a href="../00%20-%20Repositorio/index.html#red-thevenin-scr">Red Thévenin / SCR</a> ·
    <a href="../00%20-%20Repositorio/index.html#interaccion-pll-red-debil">Interacción PLL–red débil</a></div>
</section>

<section id="comp">
  <div class="phase-h"><div class="phase-n" style="background:var(--f4)">★</div>
    <h2 class="sec" style="border:0;margin:0">GFM vs GFL: estabilidad espejo</h2></div>
  <p class="lead">El resultado que une los dos proyectos.</p>
  <p>El script carga el modelo del GFM (proyecto 01) con <code class="inl">importlib</code> y superpone
  el \( \max\mathrm{Re} \) de ambos frente al SCR:</p>
""" + embed("main_compare.py") + r"""
  <h3>★.1 Resultados reales</h3>
""" + console(R_CMP) + r"""
  <figure><img src="results/comparacion_gfm_gfl.png" alt="GFM vs GFL">
    <figcaption>max Re vs SCR: el GFL se inestabiliza en red débil; el GFM (agresivo) en red fuerte.</figcaption></figure>
  <table>
    <tr><th></th><th>GFL</th><th>GFM</th></tr>
    <tr><td>Impone</td><td>corriente</td><td>tensión</td></tr>
    <tr><td>Red problemática</td><td>débil (Z alta)</td><td>fuerte (Z baja)</td></tr>
    <tr><td>Mecanismo</td><td>PLL ve tensión inestable</td><td>\( \partial P/\partial\delta \) excesiva</td></tr>
    <tr><td>Frontera</td><td>SCR≈3.48 (por debajo)</td><td>SCR≈3.35 (por encima)</td></tr>
  </table>
  <div class="def"><b>Conclusión:</b> una fuente de corriente (GFL) sufre con carga de alta impedancia
  (red débil); una fuente de tensión (GFM) con baja impedancia (red fuerte). Por eso el grid-forming es
  clave en redes con alta penetración renovable (débiles), y por eso ambos conviven en redes reales.</div>
</section>
""")

S.append(r"""<div class="part">Parte IV · Cierre</div>

<section id="discusion">
  <h2 class="sec">10 · Discusión global</h2>
  <p class="lead">Síntesis crítica, contraste con lo esperado y limitaciones.</p>
  <h3>10.1 Coherencia interna</h3>
  <p>Los resultados encajan en una sola narrativa física: el modo de la PLL identificado en la
  Fase&nbsp;1 (21.3&nbsp;Hz) es el que la Fase&nbsp;2 muestra como resistencia negativa en el eje q, el
  que la Fase&nbsp;3 lleva a la inestabilidad al resonar con la red débil, y el que el barrido de
  \( f_\text{pll} \) desplaza monótonamente. El acuerdo del SCR crítico por autovalores (3.478) y por
  Nyquist de impedancia (3.551), del ~2&nbsp;%, valida el método de impedancia [4] frente a la "verdad"
  del modelo acoplado.</p>
  <h3>10.2 Contraste con lo esperado y con la literatura</h3>
  <ul class="tight">
    <li>La <b>resistencia negativa de la PLL en el eje q</b> reproduce el mecanismo descrito en [6]: la
    no pasividad se concentra donde la PLL actúa (\( v_{Cq} \)), no en el eje d.</li>
    <li>La <b>inestabilidad en red débil</b> (SCR bajo) es el comportamiento canónico del grid-following
    [5], opuesto al del grid-forming, que el proyecto 01 muestra inestable en red fuerte.</li>
    <li>La relación <b>monótona</b> PLL rápida → SCR crítico mayor cuantifica el compromiso clásico
    seguimiento↔robustez de la PLL.</li>
  </ul>
  <h3>10.3 Limitaciones</h3>
  <ul class="tight">
    <li>Modelo promediado y condiciones equilibradas (sin conmutación ni faltas asimétricas).</li>
    <li>PLL SRF básica; no se modelan PLL avanzadas (DSOGI, SOGI-FLL) que alteran la resistencia negativa.</li>
    <li>Linealización en un punto de operación nominal; sin análisis de incertidumbre paramétrica.</li>
  </ul>
</section>

<section id="lecciones">
  <h2 class="sec">11 · Lecciones aprendidas</h2>
  <div class="grid2">
    <div class="card"><h3>Sobre el GFL</h3>
      <ul class="tight">
        <li>El GFL con PLL nominal (30 Hz) es robusto incluso en red muy débil; la inestabilidad aparece
        al <b>acelerar la PLL</b>.</li>
        <li>La resistencia negativa vive en el <b>eje q</b> (la PLL controla \( v_{Cq} \)).</li>
        <li>El <b>ancho de banda de la PLL</b> fija el SCR crítico de forma monótona: es la palanca y un
        compromiso seguimiento↔robustez.</li>
      </ul></div>
    <div class="card"><h3>Sobre el método</h3>
      <ul class="tight">
        <li>El método de impedancia (el mismo del 01) predijo el SCR crítico con ~2 % de error: es
        general.</li>
        <li>Reutilizar <span class="file">impedance.py</span> y <span class="file">grid.py</span> entre
        proyectos demuestra que GFM y GFL son el mismo problema con distinta capa de control.</li>
        <li>La pasividad (signo de \( \mathrm{Re}\{Z\} \)) es un diagnóstico rápido de riesgo antes de
        Nyquist.</li>
      </ul></div>
  </div>
</section>

<section id="concl">
  <h2 class="sec">12 · Conclusiones, aportaciones y líneas futuras</h2>
  <p class="lead">Cierre formal del estudio del grid-following.</p>
  <h3>12.1 Conclusiones generales</h3>
  <ol class="tight">
    <li>El modelo GFL de 10 estados es estable en red rígida (\( \max\mathrm{Re}=-50 \)), con el modo de
    la PLL a 21.3&nbsp;Hz (\( \zeta=0.71 \)) coherente con su diseño de segundo orden.</li>
    <li>La impedancia de salida es <b>no pasiva</b>: \( \mathrm{Re}\{Z_{qq}\}<0 \) en la banda de la PLL,
    firma de la realimentación de la PLL sobre el eje q.</li>
    <li>El SCR crítico (\( \approx 3.5 \), inestable por debajo) se predice por dos vías con ~2&nbsp;% de
    error, y crece monótonamente con el ancho de banda de la PLL (de 1 a 8 entre 40 y 170&nbsp;Hz).</li>
    <li>La dualidad GFM↔GFL queda demostrada con un único formalismo de impedancia: el GFL falla en red
    débil, el GFM en red fuerte.</li>
  </ol>
  <h3>12.2 Aportaciones</h3>
  <ol class="tight">
    <li><b>Reutilización del método</b> del proyecto 01 (impedancia + Nyquist) sobre un control opuesto,
    evidenciando su generalidad (mismos <span class="file">impedance.py</span> y
    <span class="file">grid.py</span>).</li>
    <li><b>Cuantificación de la frontera</b> de estabilidad en función de la palanca de diseño (ancho de
    banda de la PLL), con barrido reproducible.</li>
    <li><b>Cierre de la dualidad</b> GFM↔GFL en una sola figura comparativa, de alto valor didáctico.</li>
  </ol>
  <h3>12.3 Limitaciones</h3>
  <p>Resumidas en el cap.&nbsp;10.3: modelo promediado, condiciones equilibradas, PLL SRF básica y punto
  de operación nominal.</p>
  <h3>12.4 Líneas futuras</h3>
  <ul class="tight">
    <li>PLL avanzadas (DSOGI, SOGI-FLL) y su efecto sobre la resistencia negativa.</li>
    <li>Desequilibrio (componentes simétricas) y respuesta a faltas.</li>
    <li>Validación en PLECS del modelo conmutado.</li>
    <li>Estrategias de mitigación: realimentación de tensión, impedancia activa, atenuación de la PLL.</li>
  </ul>
</section>
""")

S.append(r"""
<section id="biblio">
  <h2 class="sec">Bibliografía</h2>
  <table>
    <tr><td>[4]</td><td>J. Sun, "Impedance-based stability criterion for grid-connected inverters,"
      <i>IEEE Trans. Power Electron.</i>, vol. 26, no. 11, 2011.</td></tr>
    <tr><td>[5]</td><td>X. Wang, F. Blaabjerg, "Harmonic stability in power electronic-based power
      systems," <i>IEEE Trans. Smart Grid</i>, vol. 10, no. 3, 2019.</td></tr>
    <tr><td>[6]</td><td>B. Wen et al., "Analysis of D-Q small-signal impedance of grid-tied inverters,"
      <i>IEEE Trans. Power Electron.</i>, vol. 31, no. 1, 2016.</td></tr>
    <tr><td>[7]</td><td>R. H. Lasseter et al., "Grid-forming inverters: a critical asset for the power
      grid," <i>IEEE J. Emerg. Sel. Topics Power Electron.</i>, vol. 8, no. 2, 2020.</td></tr>
    <tr><td>[8]</td><td>D. B. Rathnayake et al., "Grid forming inverter modeling, control, and
      applications," <i>IEEE Access</i>, vol. 9, 2021.</td></tr>
    <tr><td>[11]</td><td>S.-K. Chung, "A phase tracking system for three phase utility interface
      inverters," <i>IEEE Trans. Power Electron.</i>, vol. 15, no. 3, 2000 (diseño de la SRF-PLL).</td></tr>
  </table>
  <p class="small">Referencias de fundamento; el código y los resultados numéricos son propios. Cada
  concepto está desarrollado en el <a href="../00%20-%20Repositorio/index.html">repositorio</a>.</p>
</section>
""")

S.append(r"""<div class="part">Apéndices</div>

<section id="apA">
  <h2 class="sec">Apéndice A · Parámetros</h2>
  <div class="grid2">
    <div>
      <h3>A.1 Nominales y LCL (= proyecto 01)</h3>
      <table>
        <tr><th>Parámetro</th><th>Valor</th></tr>
        <tr><td>\( S_n \) / \( V_{ll} \) / \( f_0 \)</td><td>10 kVA / 400 V / 50 Hz</td></tr>
        <tr><td>\( V_0 \) (pico fase)</td><td>326.6 V</td></tr>
        <tr><td>\( L_1 \) / \( R_1 \)</td><td>2 mH / 0.10 Ω</td></tr>
        <tr><td>\( C_f \)</td><td>20 µF</td></tr>
        <tr><td>\( L_2 \) / \( R_2 \)</td><td>1 mH / 0.05 Ω</td></tr>
      </table>
    </div>
    <div>
      <h3>A.2 Control GFL</h3>
      <table>
        <tr><th>Parámetro</th><th>Valor</th></tr>
        <tr><td>BW lazo corriente \( f_{ci} \)</td><td>800 Hz</td></tr>
        <tr><td>Amort. activo \( K_\text{ad} \)</td><td>6 Ω</td></tr>
        <tr><td>BW PLL nominal \( f_\text{pll} \)</td><td>30 Hz</td></tr>
        <tr><td>Amortiguamiento PLL \( \zeta \)</td><td>0.707</td></tr>
        <tr><td>\( P^* \) / \( Q^* \)</td><td>5 kW / 0 var</td></tr>
        <tr><td>Barrido PLL (Fase 3)</td><td>40 – 170 Hz</td></tr>
      </table>
    </div>
  </div>
</section>

<section id="apB">
  <h2 class="sec">Apéndice B · Vector de estado (10 estados)</h2>
  <table>
    <tr><th>#</th><th>Estado</th><th>Significado</th><th>Grupo</th></tr>
    <tr><td>0</td><td><code>iL1d</code></td><td>corriente inductor inversor, eje d</td><td>planta LCL</td></tr>
    <tr><td>1</td><td><code>iL1q</code></td><td>corriente inductor inversor, eje q</td><td>planta LCL</td></tr>
    <tr><td>2</td><td><code>vcd</code></td><td>tensión condensador, eje d</td><td>planta LCL</td></tr>
    <tr><td>3</td><td><code>vcq</code></td><td>tensión condensador, eje q</td><td>planta LCL</td></tr>
    <tr><td>4</td><td><code>iL2d</code></td><td>corriente a red (i_g), eje d</td><td>planta LCL</td></tr>
    <tr><td>5</td><td><code>iL2q</code></td><td>corriente a red (i_g), eje q</td><td>planta LCL</td></tr>
    <tr><td>6</td><td><code>delta</code></td><td>ángulo del marco de la PLL</td><td>PLL</td></tr>
    <tr><td>7</td><td><code>eps</code></td><td>integrador del PI de la PLL</td><td>PLL</td></tr>
    <tr><td>8</td><td><code>gd</code></td><td>integrador PI corriente, eje d</td><td>lazo corriente</td></tr>
    <tr><td>9</td><td><code>gq</code></td><td>integrador PI corriente, eje q</td><td>lazo corriente</td></tr>
  </table>
</section>

<section id="apC">
  <h2 class="sec">Apéndice C · Código fuente del proyecto</h2>
  <p class="lead">Los ficheros principales están embebidos en sus capítulos; aquí el auxiliar de diagramas.</p>
""" + embed("diagramas.py", "Genera el esquema eléctrico y los diagramas de modelo y control en results/.") + r"""
  <div class="note">Ficheros: <span class="file">params.py</span> <span class="file">model.py</span>
  <span class="file">impedance.py</span> <span class="file">grid.py</span>
  <span class="file">main_phase1/2/3.py</span> <span class="file">main_compare.py</span>
  <span class="file">diagramas.py</span>. Este informe lo genera
  <span class="file">gen_informe.py</span>.</div>
</section>

<section id="apD">
  <h2 class="sec">Apéndice D · Resultados de consola (ejecución real)</h2>
  <h4>Fase 1 — <span class="file">main_phase1.py</span></h4>""" + console(R_P1) + r"""
  <h4>Fase 2 — <span class="file">main_phase2.py</span></h4>""" + console(R_P2) + r"""
  <h4>Fase 3 — <span class="file">main_phase3.py</span></h4>""" + console(R_P3) + r"""
  <h4>Comparación — <span class="file">main_compare.py</span></h4>""" + console(R_CMP) + r"""
</section>

<section id="apE">
  <h2 class="sec">Apéndice E · Cómo reproducir</h2>
  <pre>python main_phase1.py    # equilibrio, polos (red rigida)   -> results/polos_fase1.png
python main_phase2.py    # impedancia, resistencia negativa -> results/impedancia_fase2.png
python main_phase3.py    # SCR critico, barrido de PLL      -> results/estabilidad_fase3.png
python main_compare.py   # GFM vs GFL (carga modelo del 01) -> results/comparacion_gfm_gfl.png
python gen_informe.py    # regenera este informe.html</pre>
  <p class="small">Requiere Python 3.13 con NumPy, SciPy y Matplotlib.</p>
</section>

<section id="apF">
  <h2 class="sec">Apéndice F · Glosario</h2>
  <table>
    <tr><td><b>GFL / GFM</b></td><td>Grid-following (inyecta corriente) / grid-forming (impone tensión).</td></tr>
    <tr><td><b>PLL (SRF)</b></td><td>Estima el ángulo de red llevando \( v_{Cq}\to 0 \).</td></tr>
    <tr><td><b>SCR</b></td><td>Short-circuit ratio: fortaleza de la red. Bajo = débil.</td></tr>
    <tr><td><b>resistencia negativa</b></td><td>\( \mathrm{Re}\{Z\}<0 \): aporta energía (no pasiva).</td></tr>
    <tr><td><b>ancho de banda PLL</b></td><td>\( f_\text{pll} \): palanca que fija el SCR crítico.</td></tr>
    <tr><td><b>minor loop gain</b></td><td>\( L=Z_\text{red}Y_\text{inv} \); su Nyquist decide la estabilidad.</td></tr>
  </table>
  <p class="small" style="margin-top:24px">Definiciones extensas en el
  <a href="../00%20-%20Repositorio/index.html">repositorio de conocimiento</a>.</p>
</section>
""")

FOOT = """</main>
</div>
<script>
  const links=[...document.querySelectorAll('#nav a[href^="#"]')];
  const map={}; links.forEach(a=>{const id=a.getAttribute('href').slice(1); if(id && !map[id]) map[id]=a;});
  const obs=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){
    links.forEach(l=>l.classList.remove('active'));
    if(map[e.target.id]) map[e.target.id].classList.add('active');}}),
    {rootMargin:'-15% 0px -75% 0px'});
  document.querySelectorAll('section[id]').forEach(s=>obs.observe(s));
</script>
</body>
</html>"""

html_out = HEAD + NAV + HERO + "".join(S) + FOOT
with open(os.path.join(HERE, "informe.html"), "w", encoding="utf-8") as fh:
    fh.write(html_out)
print(f"informe.html generado: {html_out.count(chr(10))+1} lineas, {len(html_out)} bytes")
