"""Generador del informe HTML (nivel tesis) del proyecto 03 - Energia-DataCenter-IA.

Lee los .py reales, los embebe escapados y los acompana de la explicacion detallada y de los
resultados de consola reales. Reejecutar regenera informe.html.
    python gen_informe.py
"""
import os, html, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
import sys; sys.path.insert(0, os.path.join(HERE, "..", "00 - Repositorio"))
from conceptos_link import link_concepts


def embed(fname, caption=None):
    code = open(os.path.join(HERE, fname), encoding="utf-8").read()
    nlines = code.count("\n") + 1
    cap = f'<div class="cap">{caption}</div>' if caption else ""
    return (f'<div class="codefile"><div class="h"><span>📄 {fname}</span>'
            f'<span>{nlines} líneas · código real del proyecto</span></div>'
            f'<pre>{html.escape(code)}</pre></div>{cap}')


def console(text):
    return f'<div class="console">{html.escape(text)}</div>'


R_P1 = """============================================================
FASE 1 - Sub-bus DC con carga CPL
============================================================
P_critica teorica  P = V^2 R C / L = 128 kW
P_critica numerica (maxRe=0)     = 129 kW
  -> por encima, el bus DC oscila (CPL desamortigua el filtro L-C)"""

R_P2 = """============================================================
FASE 2 - Estabilidad del bus DC por impedancia
============================================================
Pico de |Z_fuente| = 4.767 ohm (resonancia L-C)
|Z_cpl| = V^2/P. Inestable cuando |Z_cpl| < pico  ->  P > V^2/pico = 134 kW
Coincide con la P_critica de Fase 1 (128 kW)."""

R_P3 = """============================================================
FASE 3 - Pico de carga de IA (100 -> 230 kW)
============================================================
  H=1 s: nadir=49.920 Hz, RoCoF=-1.78 Hz/s
  H=3 s: nadir=49.920 Hz, RoCoF=-0.68 Hz/s
  H=6 s: nadir=49.922 Hz, RoCoF=-0.34 Hz/s"""

R_P4 = """============================================================
FASE 4 - Dimensionado ante pico de carga de IA
============================================================
Ejemplo: pico de 250 kW, salto dP=150 kW, RoCoF_max=1 Hz/s
  C_dc minimo (DC)  = 3.9 mF
  H minima (AC)     = 3.75 s
Regla: el lado DC fija C_dc por estabilidad CPL; el lado AC fija H por RoCoF."""


HEAD = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DataCenter IA · Tesis técnica — bus DC, CPL e inercia</title>
<style>
  :root{
    --bg:#0f1419; --panel:#161d26; --panel2:#1c2530; --ink:#e6edf3; --muted:#9aa7b4;
    --acc:#4ea3ff; --acc2:#ffb454; --ok:#5ad19a; --bad:#ff6b6b; --line:#2a3542;
    --f1:#4ea3ff; --f2:#a78bfa; --f3:#5ad19a; --f4:#ffb454;
  }
  *{box-sizing:border-box}
  html{scroll-behavior:smooth}
  body{margin:0;background:var(--bg);color:var(--ink);
    font:15px/1.75 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}
  a{color:var(--acc);text-decoration:none} a:hover{text-decoration:underline}
  .cref{color:var(--acc);border-bottom:1px dotted rgba(78,163,255,.55)} .cref:hover{border-bottom-style:solid;text-decoration:none}
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
  header.hero h1{font-size:31px;margin:0 0 8px;line-height:1.18}
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
  .flow .n{flex:1;min-width:130px;background:var(--panel2);border:1px solid var(--line);border-radius:10px;padding:12px;text-align:center;font-size:13px}
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
  <a href="#estados">5 · Designación de estados</a>
  <a href="#parametros">6 · Parámetros (params.py)</a>
  <a href="#modelomat">7 · Modelo DC (model_dc.py)</a>
  <a href="#modelohib">8 · Modelo híbrido (simulate.py)</a>
  <h2>III · Desarrollo (fases)</h2>
  <a href="#f1"><span class="badge" style="background:var(--f1)">1</span>Inestabilidad CPL</a>
  <a href="#f2"><span class="badge" style="background:var(--f2)">2</span>Middlebrook</a>
  <a href="#f3"><span class="badge" style="background:var(--f3)">3</span>Pico de carga IA</a>
  <a href="#f4"><span class="badge" style="background:var(--f4)">4</span>Dimensionado</a>
  <h2>IV · Cierre</h2>
  <a href="#discusion">9 · Discusión global</a>
  <a href="#lecciones">10 · Lecciones aprendidas</a>
  <a href="#concl">11 · Conclusiones y aportaciones</a>
  <a href="#biblio">Bibliografía</a>
  <h2>Apéndices</h2>
  <a href="#apA">A · Parámetros</a>
  <a href="#apB">B · Tabla de estados</a>
  <a href="#apC">C · Código fuente</a>
  <a href="#apD">D · Resultados de consola</a>
  <a href="#apE">E · Reproducir</a>
  <a href="#apF">F · Glosario</a>
  <h2>Enlaces</h2>
  <a href="../index.html">🏠 Inicio (proyectos y repositorio)</a>
  <a href="../00%20-%20Repositorio/index.html">📚 Repositorio</a>
  <a href="../01%20-%20GFM-Impedance/informe.html">📁 01 · GFM</a>
  <a href="../02%20-%20GFL-Impedance/informe.html">📁 02 · GFL</a>
</nav>
<main>
"""

FECHA = datetime.date.today().strftime("%d/%m/%Y")

HERO = r"""<header class="hero">
  <h1>Energía para data centers de IA: bus DC, CPL e inercia</h1>
  <p class="sub">Informe técnico exhaustivo — microrred híbrida AC+DC. Estabilidad del bus DC ante carga
  de potencia constante, soporte de frecuencia ante el pico de carga, y dimensionado, con el código de
  simulación real y sus resultados.</p>
  <p class="meta">Proyecto 03 · Repositorio de aprendizaje de ingeniería de control · Generado el """ + FECHA + r""" a partir del código fuente.</p>
  <div class="tagrow">
    <span class="tag">Python 3.13</span><span class="tag">bus DC</span><span class="tag">CPL</span>
    <span class="tag">criterio de Middlebrook</span><span class="tag">VSM / inercia</span>
    <span class="tag">RoCoF</span><span class="tag">carga pulsante IA</span>
  </div>
</header>
"""

S = []

S.append(r"""
<section id="resumen">
  <h2 class="sec">Resumen ejecutivo</h2>
  <p class="lead">Dos dominios acoplados: estabilidad del bus DC (CPL) y soporte de frecuencia (AC).</p>
  <p>La energía de un data center de IA es un caso de control exigente y actual. La carga —miles de
  GPUs— es <b>pulsante</b> y, vista desde el bus de continua, se comporta como <b>carga de potencia
  constante</b> (CPL): su resistencia incremental es negativa, lo que desamortigua el bus DC y puede
  inestabilizarlo. Este proyecto modela la microrred híbrida AC+DC, halla la potencia crítica por dos
  vías independientes, simula el pico de carga en ambos dominios y deriva las reglas de dimensionado.
  Como en los proyectos 01–02, todo el código mostrado es real y todos los números son la salida de
  consola real de ejecutarlo.</p>
  <div class="kpi">
    <div class="b"><div class="n">128 kW</div><div class="l">potencia CPL crítica</div></div>
    <div class="b"><div class="n">128 / 134</div><div class="l">autovalores / Middlebrook</div></div>
    <div class="b"><div class="n">−1.78 → −0.34</div><div class="l">RoCoF [Hz/s] con H=1→6 s</div></div>
    <div class="b"><div class="n">2 / 4</div><div class="l">estados (DC / híbrido)</div></div>
    <div class="b"><div class="n">AC + DC</div><div class="l">microrred híbrida</div></div>
  </div>
  <div class="def"><b>Idea central:</b> los servidores son cargas de potencia constante; su resistencia
  incremental negativa \( -V_{dc}^2/P \) desamortigua el bus DC y lo inestabiliza por encima de
  \( P_\text{crit} \) (el análogo DC de la inestabilidad por impedancia del grid-following). El pico de
  carga de IA exige dimensionar <b>dos cosas independientes</b>: el condensador de bus (DC, estabilidad)
  y la inercia del BESS (AC, RoCoF).</div>

  <h3>Resumen</h3>
  <p>Se presenta el modelado y análisis de estabilidad del sistema de energía de un data center de IA,
  concebido como microrred híbrida AC+DC: un sistema de almacenamiento en baterías (BESS) grid-forming
  alimenta, vía un rectificador activo (AFE), un bus de continua que abastece a los servidores. Estos,
  regulados por sus convertidores de punto de carga, se comportan como carga de potencia constante (CPL)
  cuya resistencia incremental negativa puede inestabilizar el bus. Se deriva analíticamente la potencia
  crítica \( P_\text{crit}=V_{dc}^2R_fC_{dc}/L_f \) y se valida por dos vías (autovalores y criterio de
  Middlebrook). Se simula el sistema híbrido ante el pico de carga de un trabajo de IA, cuantificando el
  RoCoF en el lado AC en función de la inercia y el hundimiento de tensión en el lado DC en función del
  condensador, y se derivan las reglas de dimensionado de ambos elementos, que resultan desacopladas.</p>
  <p><b>Palabras clave:</b> data center de IA; bus DC; carga de potencia constante; criterio de
  Middlebrook; estabilidad por impedancia; máquina síncrona virtual; RoCoF; dimensionado.</p>

  <h3>Abstract</h3>
  <p>This work presents the modelling and stability analysis of the power system of an AI data centre,
  conceived as a hybrid AC+DC microgrid: a grid-forming battery energy storage system (BESS) feeds,
  through an active front-end (AFE), a DC bus that supplies the servers. The servers, regulated by their
  point-of-load converters, behave as a constant power load (CPL) whose negative incremental resistance
  may destabilise the bus. The critical power \( P_\text{crit}=V_{dc}^2R_fC_{dc}/L_f \) is derived
  analytically and validated through two routes (eigenvalues and the Middlebrook criterion). The hybrid
  system is simulated under an AI-job load step, quantifying the AC-side RoCoF as a function of inertia
  and the DC-side voltage sag as a function of the bus capacitor, and the sizing rules for both elements
  —which turn out to be decoupled— are derived.</p>
  <p><b>Keywords:</b> AI data centre; DC bus; constant power load; Middlebrook criterion; impedance-based
  stability; virtual synchronous machine; RoCoF; sizing.</p>
</section>

<section id="nomenclatura">
  <h2 class="sec">Nomenclatura</h2>
  <div class="grid2">
    <div>
      <h3>Magnitudes y parámetros</h3>
      <table>
        <tr><th>Símbolo</th><th>Significado</th></tr>
        <tr><td>\( i_L \)</td><td>corriente del cable de distribución DC</td></tr>
        <tr><td>\( V_{dc} \)</td><td>tensión del bus DC (rack)</td></tr>
        <tr><td>\( V_\text{bus} \)</td><td>tensión del bus DC principal (regulada)</td></tr>
        <tr><td>\( \omega,\,P_m \)</td><td>frecuencia del BESS, potencia AFE filtrada</td></tr>
        <tr><td>\( L_f,R_f,C_{dc} \)</td><td>cable y condensador de bus</td></tr>
        <tr><td>\( P_\text{cpl} \)</td><td>potencia de la carga CPL</td></tr>
        <tr><td>\( P_\text{crit} \)</td><td>potencia CPL crítica de estabilidad</td></tr>
        <tr><td>\( H,J,D \)</td><td>inercia (constante, momento, damping) del VSM</td></tr>
      </table>
    </div>
    <div>
      <h3>Conceptos y acrónimos</h3>
      <table>
        <tr><th>Símbolo / sigla</th><th>Significado</th></tr>
        <tr><td>\( Z_\text{cpl}=-V_{dc}^2/P \)</td><td>impedancia incremental de la CPL</td></tr>
        <tr><td>\( Z_\text{fuente} \)</td><td>impedancia de salida del filtro L-C</td></tr>
        <tr><td>RoCoF</td><td>velocidad de cambio de frecuencia</td></tr>
        <tr><td>CPL</td><td>constant power load (carga potencia constante)</td></tr>
        <tr><td>BESS</td><td>battery energy storage system</td></tr>
        <tr><td>AFE</td><td>active front-end (rectificador activo)</td></tr>
        <tr><td>VSM</td><td>virtual synchronous machine</td></tr>
        <tr><td>SCR</td><td>short-circuit ratio</td></tr>
      </table>
    </div>
  </div>
</section>

<section id="indice">
  <h2 class="sec">Índice, objetivos y alcance</h2>
  <h3>Objetivos</h3>
  <ol class="tight">
    <li><b>Modelar</b> el bus DC con CPL (2 estados) y el sistema híbrido AC+DC (4 estados).</li>
    <li><b>Hallar</b> la potencia CPL crítica por autovalores y validarla por el criterio de
    Middlebrook (impedancia).</li>
    <li><b>Simular</b> el pico de carga de IA y ver el efecto de la inercia (RoCoF) y del condensador
    (hundimiento DC).</li>
    <li><b>Derivar</b> las reglas de dimensionado de \( C_{dc} \) y \( H \).</li>
  </ol>
  <div class="flow">
    <div class="n"><b>I. Preliminares</b><br>problema, teoría, método</div><div class="ar">→</div>
    <div class="n"><b>II. Modelado</b><br>físico → estados → código</div><div class="ar">→</div>
    <div class="n"><b>III. Fases 1–4</b><br>código y resultados</div><div class="ar">→</div>
    <div class="n"><b>IV. Cierre</b><br>lecciones, conclusiones</div>
  </div>
  <div class="note"><b>Convenio:</b> bloques <span class="file">📄 fichero.py</span> = código real;
  bloques verdes = salida de consola real. Fórmulas en MathJax.</div>
</section>
""")

S.append(r"""<div class="part">Parte I · Preliminares</div>

<section id="problema">
  <h2 class="sec">1 · Planteamiento del problema</h2>
  <p class="lead">Por qué la energía de un data center de IA es un caso de control exigente.</p>
  <h3>1.1 La IA dispara una demanda eléctrica de naturaleza nueva</h3>
  <p>El entrenamiento de modelos de IA concentra decenas o cientos de megavatios en un emplazamiento,
  con un perfil de consumo muy distinto al de un data center clásico: los <i>jobs</i> sincronizan miles
  de aceleradores que arrancan y paran casi a la vez, produciendo <b>escalones de potencia</b> de gran
  amplitud en milisegundos. Esto somete al sistema a dos retos en dominios distintos: la <b>estabilidad
  del bus de continua</b> que alimenta los servidores, y el <b>soporte de frecuencia</b> en el lado de
  alterna que entrega esa potencia.</p>
  <div class="grid2">
    <div class="card"><h3>Carga pulsante</h3>
      <p>Miles de GPUs entran/salen de un job a la vez: la demanda salta como un escalón en
      milisegundos, con RoCoF severo en el lado AC si no hay inercia que lo frene.</p></div>
    <div class="card"><h3>Cargas de potencia constante (CPL)</h3>
      <p>Cada servidor regula su tensión interna, así que en el bus DC consume potencia constante: su
      corriente es \( i=P/V_{dc} \) y su resistencia incremental \( -V_{dc}^2/P \) es negativa.</p></div>
  </div>
  <h3>1.2 La arquitectura: microrred híbrida AC+DC</h3>
  <div class="flow">
    <div class="n"><b>BESS</b><br>grid-forming (AC)</div><div class="ar">→</div>
    <div class="n"><b>AFE</b><br>AC → DC</div><div class="ar">→</div>
    <div class="n"><b>Bus DC</b><br>cable + \( C_{dc} \)</div><div class="ar">→</div>
    <div class="n"><b>CPL</b><br>servidores IA</div>
  </div>
  <p>El BESS forma la red AC interna (impone tensión y frecuencia, aporta inercia vía VSM). El AFE
  rectifica al bus DC. El bus distribuye a los racks por un cable (\( L_f,R_f \)) y un condensador
  (\( C_{dc} \)). Los servidores son la CPL.</p>
  <div class="repolinks"><b>📚 En el repositorio:</b>
    <a href="../00%20-%20Repositorio/index.html#carga-pulsante-datacenter-ia">Carga pulsante de IA</a> ·
    <a href="../00%20-%20Repositorio/index.html#carga-potencia-constante-cpl">CPL</a> ·
    <a href="../00%20-%20Repositorio/index.html#estabilidad-bus-dc-cpl">Estabilidad de bus DC con CPL</a></div>
</section>

<section id="marco">
  <h2 class="sec">2 · Estado del arte y marco teórico</h2>
  <p class="lead">Antecedentes y fundamentos de la estabilidad del bus DC con CPL.</p>

  <h3>2.1 Estado del arte</h3>
  <p>La inestabilidad de buses de continua que alimentan cargas de potencia constante (CPL) es un
  problema clásico, formalizado por Middlebrook para filtros de entrada de reguladores conmutados [9] y
  ampliamente estudiado en distribución DC y microrredes [12],[13]: la carga regulada presenta una
  resistencia incremental negativa que desamortigua el filtro L-C. En paralelo, el soporte de frecuencia
  mediante inercia virtual (VSM) en sistemas con almacenamiento es una técnica consolidada [2],[10]. La
  novedad del caso es el <b>data center de IA</b>, cuya carga pulsante y de gran amplitud somete a la vez
  al bus DC (estabilidad CPL) y al lado AC (RoCoF). Este trabajo aborda ambos dominios de forma unificada
  y conecta la inestabilidad CPL con el mismo formalismo de impedancia de los proyectos 01–02.</p>

  <h3>2.2 La CPL y la resistencia negativa</h3>
  <p>Si la tensión del bus baja un poco, la CPL —que mantiene \( P=Vi \) constante— <b>aumenta</b> la
  corriente (\( i=P/V \)). Una resistencia haría lo contrario. Ese comportamiento invertido es, en
  pequeña señal, una resistencia incremental negativa \( \partial V/\partial i=-V_{dc}^2/P \), que resta
  amortiguamiento al circuito LC del bus y lo inestabiliza por encima de cierta potencia.</p>

  <h3>2.3 Derivación de la potencia crítica por Routh-Hurwitz</h3>
  <p>El modelo DC de dos estados (\( i_L,V_{dc} \)) linealizado en torno al equilibrio
  (\( V_{dc}\approx V_\text{bus} \), \( i_L=P/V_\text{bus} \)) tiene matriz de estado:</p>
  <div class="eq">\[ A=\begin{bmatrix} -\dfrac{R_t}{L_f} & -\dfrac{1}{L_f} \\
     \dfrac{1}{C_{dc}} & \dfrac{1}{C_{dc}}\dfrac{P}{V_{dc}^2} \end{bmatrix},\qquad R_t=R_f+R_d \]</div>
  <p>donde el término \( +\dfrac{P}{V_{dc}^2} \) en \( A_{22} \) es la conductancia negativa de la CPL
  (al linealizar \( -P/V_{dc} \)). La ecuación característica es \( s^2-\mathrm{tr}(A)\,s+\det(A)=0 \),
  con</p>
  <div class="eq">\[ \mathrm{tr}(A)=-\frac{R_t}{L_f}+\frac{1}{C_{dc}}\frac{P}{V_{dc}^2},\qquad
     \det(A)=\frac{1}{L_fC_{dc}}\Big(1-\frac{R_t P}{V_{dc}^2}\Big) \]</div>
  <p>El criterio de Routh-Hurwitz para segundo orden exige \( -\mathrm{tr}(A)>0 \) y \( \det(A)>0 \). La
  segunda da \( P<V_{dc}^2/R_t \) (cota muy holgada, no vinculante). La primera es la condición
  <b>binding</b>:</p>
  <div class="eq">\[ -\mathrm{tr}(A)>0 \;\Longleftrightarrow\; \frac{R_t}{L_f}>\frac{1}{C_{dc}}\frac{P}{V_{dc}^2}
     \;\Longleftrightarrow\; \boxed{\,P<P_\text{crit}=\frac{V_{dc}^2\,R_t\,C_{dc}}{L_f}\,} \]</div>
  <p>Esta es la fórmula que codifica la <code class="inl">@property Pcrit</code> de
  <span class="file">params.py</span> y que la Fase&nbsp;1 confirma numéricamente (128 kW teórico,
  129 kW por autovalores). Físicamente: el amortiguamiento del filtro (\( R_t/L_f \)) debe superar el
  desamortiguamiento de la CPL (\( P/(C_{dc}V_{dc}^2) \)); más \( C_{dc} \) o más \( R_t \) suben el
  límite, más \( L_f \) lo baja.</p>

  <h3>2.4 El criterio de Middlebrook (verificación por impedancia)</h3>
  <p>Para un par fuente↔carga, la estabilidad se garantiza si
  \( |Z_\text{fuente}(j\omega)|<|Z_\text{carga}(j\omega)| \) en todo \( \omega \). Con la CPL,
  \( |Z_\text{carga}|=V_{dc}^2/P \) baja al subir la potencia; la inestabilidad aparece cuando cae por
  debajo del pico de resonancia de \( Z_\text{fuente} \), dando \( P_\text{lim}=V_{dc}^2/\max|Z_\text{fuente}| \).
  Es el mismo enfoque de impedancia de los proyectos 01–02, aplicado al bus DC, y confirma la
  \( P_\text{crit} \) de Routh-Hurwitz con margen conservador.</p>

  <h3>2.5 Inercia y RoCoF (lado AC)</h3>
  <p>La ecuación de oscilación del BESS, \( 2HS\,\dfrac{d(\Delta f/f_0)}{dt}=\Delta P \), da ante un
  escalón \( \Delta P \) una pendiente inicial de frecuencia:</p>
  <div class="eq">\[ \mathrm{RoCoF}=\frac{df}{dt}\bigg|_{0^+}=\frac{\Delta P\,f_0}{2\,H\,S} \]</div>
  <p>inversamente proporcional a la inercia \( H \): duplicar \( H \) mitad el RoCoF. Un RoCoF excesivo
  dispara las protecciones de \( df/dt \), de ahí su importancia en el dimensionado.</p>

  <div class="repolinks"><b>📚 En el repositorio:</b>
    <a href="../00%20-%20Repositorio/index.html#carga-potencia-constante-cpl">CPL / resistencia negativa</a> ·
    <a href="../00%20-%20Repositorio/index.html#routh-hurwitz">Routh-Hurwitz</a> ·
    <a href="../00%20-%20Repositorio/index.html#criterio-middlebrook">Middlebrook</a> ·
    <a href="../00%20-%20Repositorio/index.html#vsm-inercia">VSM / inercia</a></div>
</section>

<section id="sw">
  <h2 class="sec">3 · Software y método</h2>
  <p class="lead">Linealizar para la estabilidad; simular para el transitorio.</p>
  <p>Todo en Python (NumPy, SciPy, Matplotlib). Para la <b>estabilidad</b> (¿hasta qué potencia aguanta
  el bus?) se linealiza y se miran autovalores e impedancias (pequeña señal). Para el <b>transitorio</b>
  (¿cómo responde al pico?) se integra el modelo no lineal completo (gran señal). El hilo metodológico
  es la <b>doble validación</b>, como en los proyectos 01–02: la potencia crítica se obtiene por
  autovalores y por Middlebrook, y se comparan (~5 %). El método de impedancia conecta este problema DC
  con los problemas AC anteriores: en los tres, una resistencia negativa desestabiliza por interacción
  de impedancias.</p>
  <div class="repolinks"><b>📚 En el repositorio:</b>
    <a href="../00%20-%20Repositorio/index.html#linealizacion-numerica">Linealización numérica</a> ·
    <a href="../00%20-%20Repositorio/index.html#integracion-edos-stiff">EDOs stiff</a></div>
</section>
""")

S.append(r"""<div class="part">Parte II · Modelado</div>

<section id="fisica">
  <h2 class="sec">4 · El sistema físico</h2>
  <p class="lead">Dos dominios acoplados por el AFE: el bus DC (estabilidad) y el lado AC (frecuencia).</p>
  <h3>4.1 El lado DC: el bus y la CPL</h3>
  <p>Desde el AFE hasta el rack hay un cable (\( L_f=50\,\mu\text{H} \), \( R_f=5\,\text{m}\Omega \)) y
  un condensador de bus \( C_{dc} \). La carga es la CPL (\( P_\text{cpl}=150 \) kW nominal). El bus
  principal \( V_\text{bus}=800 \) V lo regula el AFE (rígido). El elemento crítico es la CPL, que aporta
  amortiguamiento negativo.</p>
  <h3>4.2 El lado AC: BESS grid-forming con inercia</h3>
  <p>El BESS (\( S_\text{ac}=1 \) MVA) forma la red AC con una capa VSM (\( H=3 \) s nominal). Ante un
  cambio de potencia, su frecuencia evoluciona según la ecuación de swing; esa inercia limita el RoCoF.</p>
  <h3>4.3 El acoplamiento entre dominios</h3>
  <p>El AFE es el puente: toma del lado AC la potencia \( P_\text{afe}=V_\text{bus}\,i_L \) que el bus DC
  demanda, y la traslada al BESS como carga. Así, un escalón en el lado DC se convierte en un escalón de
  potencia que el BESS ve en AC, y su frecuencia responde. Eso hace el problema <b>híbrido</b>: la
  perturbación nace en DC pero se siente en AC.</p>
  <div class="repolinks"><b>📚 En el repositorio:</b>
    <a href="../00%20-%20Repositorio/index.html#carga-potencia-constante-cpl">CPL</a> ·
    <a href="../00%20-%20Repositorio/index.html#dinamica-bus-dc">Dinámica del bus DC</a> ·
    <a href="../00%20-%20Repositorio/index.html#vsm-inercia">VSM / inercia</a></div>
</section>

<section id="estados">
  <h2 class="sec">5 · Designación de los estados</h2>
  <p class="lead">Dos modelos: el DC (2 estados) para la estabilidad, el híbrido (4) para el pico.</p>
  <h3>5.1 Modelo DC — 2 estados</h3>
  <table>
    <tr><th>#</th><th>Estado</th><th>Por qué es estado</th><th>Derivada</th></tr>
    <tr><td>0</td><td><code>iL</code></td><td>corriente en el cable \( L_f \)</td><td>\( L_f\dot i_L=V_\text{bus}-V_{dc}-(R_f+R_d)i_L \)</td></tr>
    <tr><td>1</td><td><code>Vdc</code></td><td>tensión en \( C_{dc} \)</td><td>\( C_{dc}\dot V_{dc}=i_L-\dfrac{P_\text{cpl}}{V_{dc}}+i_\text{pert} \)</td></tr>
  </table>
  <h3>5.2 Modelo híbrido — 4 estados</h3>
  <table>
    <tr><th>#</th><th>Estado</th><th>Significado</th><th>Dominio</th></tr>
    <tr><td>0</td><td><code>iL</code></td><td>corriente del cable DC</td><td>DC</td></tr>
    <tr><td>1</td><td><code>Vdc</code></td><td>tensión del bus DC</td><td>DC</td></tr>
    <tr><td>2</td><td><code>omega</code></td><td>frecuencia del BESS (swing)</td><td>AC</td></tr>
    <tr><td>3</td><td><code>Pm</code></td><td>potencia del AFE filtrada</td><td>AC</td></tr>
  </table>
  <div class="note">El acoplamiento es \( P_\text{afe}=V_\text{bus}\,i_L \): la corriente del bus DC
  (estado 0) entra en la ecuación de swing del BESS (estados 2–3) como carga. Por eso una perturbación
  de carga en DC se siente como caída de frecuencia en AC.</div>
</section>

<section id="parametros">
  <h2 class="sec">6 · Parámetros <span class="file">params.py</span></h2>
  <p class="lead">Una sola fuente de verdad; incluye la fórmula de la potencia crítica.</p>
  <p>Nótese la <code class="inl">@property Pcrit</code>: codifica la potencia crítica analítica
  \( P_\text{crit}=V_\text{bus}^2(R_f+R_d)C_{dc}/L_f \), que la Fase&nbsp;1 confirma numéricamente. Los
  parámetros del VSM (\( J_\text{vsm}, D_\text{vsm} \)) se derivan de la constante de inercia \( H \) y
  del droop, igual que en el proyecto 01.</p>
""" + embed("params.py") + r"""
</section>

<section id="modelomat">
  <h2 class="sec">7 · Modelo del bus DC <span class="file">model_dc.py</span></h2>
  <p class="lead">2 estados, no lineal por el término de la CPL.</p>
  <p>El balance del bus es no lineal por \( P_\text{cpl}/V_{dc} \). Al linealizar ese término alrededor
  del equilibrio aparece la resistencia negativa \( -P/V_{dc}^2 \), origen de la inestabilidad. La
  entrada \( i_\text{pert} \) permite medir la impedancia de salida (Fase&nbsp;2). La estructura
  (equilibrio + linealización por diferencias centradas) es la misma de los proyectos 01–02.</p>
""" + embed("model_dc.py",
  "DCBus: f(x,u) con la CPL no lineal, equilibrium (guess: iL=Pcpl/Vbus, Vdc=Vbus) y linearize.") + r"""
</section>

<section id="modelohib">
  <h2 class="sec">8 · Modelo híbrido AC+DC <span class="file">simulate.py</span></h2>
  <p class="lead">4 estados; integra el pico de carga en ambos dominios.</p>
  <p>Añade al modelo DC la dinámica AC del BESS: el AFE toma \( P_\text{afe}=V_\text{bus}i_L \), que se
  filtra (\( P_m \)) y entra en la ecuación de swing del VSM. Se integra con LSODA (stiff). El parámetro
  \( H \) se puede variar en cada corrida para estudiar su efecto sobre el RoCoF.</p>
""" + embed("simulate.py",
  "rhs de 4 estados (iL, Vdc, omega, Pm); run() integra con LSODA y permite barrer H.") + r"""
  <div class="eq">\[ J\,\dot\omega=\frac{P_\text{ac0}-P_m}{\omega_0}-D(\omega-\omega_0),\qquad
     \dot P_m=\omega_{pac}(P_\text{afe}-P_m),\qquad P_\text{afe}=V_\text{bus}\,i_L \]</div>
</section>
""")

S.append(r"""<div class="part">Parte III · Desarrollo — las cuatro fases</div>

<section id="f1">
  <div class="phase-h"><div class="phase-n" style="background:var(--f1)">1</div>
    <h2 class="sec" style="border:0;margin:0">Fase 1 · Inestabilidad por CPL</h2></div>
  <p class="lead">La resistencia negativa de la carga desamortigua el bus DC.</p>
""" + embed("main_phase1.py") + r"""
  <h3>1.1 Resultados reales</h3>
""" + console(R_P1) + r"""
  <div class="grid2">
    <figure><img src="results/fase1_cpl.png" alt="inestabilidad CPL">
      <figcaption>max Re vs potencia CPL: cruza a inestable en P_crit; más C_dc lo eleva.</figcaption></figure>
    <div>
      <p>La condición de Routh-Hurwitz sobre el modelo DC da una potencia crítica de forma cerrada:</p>
      <div class="eq">\[ P_\text{crit}=\frac{V_{dc}^2\,R_f\,C_{dc}}{L_f} \]</div>
      <p><span class="pill bad">INESTABLE</span> por encima de \( P_\text{crit} \). Teórica <b>128 kW</b>,
      numérica (autovalores) <b>129 kW</b> (&lt;1 % de acuerdo). Más \( C_{dc} \) o más amortiguamiento
      \( R_d \) suben \( P_\text{crit} \).</p>
      <div class="def"><b>El análogo DC:</b> igual que la PLL del GFL (proyecto 02) creaba una resistencia
      negativa que resonaba con la inductancia de la red, aquí la CPL crea una resistencia negativa que
      resuena con el circuito LC del bus. Mismo principio, otro dominio.</div>
    </div>
  </div>
  <div class="repolinks"><b>📚 En el repositorio:</b>
    <a href="../00%20-%20Repositorio/index.html#estabilidad-bus-dc-cpl">Estabilidad de bus DC con CPL</a> ·
    <a href="../00%20-%20Repositorio/index.html#routh-hurwitz">Routh-Hurwitz</a></div>
</section>

<section id="f2">
  <div class="phase-h"><div class="phase-n" style="background:var(--f2)">2</div>
    <h2 class="sec" style="border:0;margin:0">Fase 2 · Estabilidad por impedancia (Middlebrook)</h2></div>
  <p class="lead">El mismo límite, visto como cociente de impedancias.</p>
""" + embed("main_phase2.py") + r"""
  <h3>2.1 Resultados reales</h3>
""" + console(R_P2) + r"""
  <div class="grid2">
    <figure><img src="results/fase2_middlebrook.png" alt="middlebrook">
      <figcaption>|Z_fuente| vs |Z_cpl|: estable mientras |Z_cpl|=V²/P supere el pico de la fuente.</figcaption></figure>
    <div>
      <p>El pico de \( |Z_\text{fuente}| \) (la resonancia LC) es <b>4.767 Ω</b>. La carga es estable
      mientras \( |Z_\text{cpl}|=V_{dc}^2/P \) lo supere; el límite es \( P=V_{dc}^2/\max|Z_\text{fuente}|
      \approx \) <b>134 kW</b>, que coincide con la \( P_\text{crit} \) por autovalores (128 kW) con
      ~5 %. <span class="pill ok">validación cruzada</span></p>
      <div class="note">Middlebrook dice además <b>por qué</b> y <b>dónde</b>: la inestabilidad ocurre en
      el pico de resonancia de la fuente. Para subir el margen hay que bajar ese pico (más amortiguamiento
      o \( C_{dc} \)), no solo añadir potencia. El ~5 % viene de que Middlebrook es conservador
      (suficiente, no exacto).</div>
    </div>
  </div>
  <div class="repolinks"><b>📚 En el repositorio:</b>
    <a href="../00%20-%20Repositorio/index.html#criterio-middlebrook">Middlebrook</a> ·
    <a href="../00%20-%20Repositorio/index.html#impedancia-salida-estabilidad">Estabilidad por impedancia</a></div>
</section>

<section id="f3">
  <div class="phase-h"><div class="phase-n" style="background:var(--f3)">3</div>
    <h2 class="sec" style="border:0;margin:0">Fase 3 · Pico de carga de IA (híbrido)</h2></div>
  <p class="lead">Un job arranca: 100 → 230 kW en milisegundos.</p>
""" + embed("main_phase3.py") + r"""
  <h3>3.1 Resultados reales</h3>
""" + console(R_P3) + r"""
  <div class="grid2">
    <figure><img src="results/fase3_pico_carga.png" alt="pico de carga">
      <figcaption>Arriba: frecuencia AC (más inercia → menor RoCoF). Abajo: tensión DC (más C_dc → menor hundimiento).</figcaption></figure>
    <div>
      <p>El escalón se propaga a los dos dominios. En AC, el RoCoF lo limita la inercia:</p>
      <div class="eq">\[ \mathrm{RoCoF}\approx\frac{\Delta P\,f_0}{2\,H\,S} \]</div>
      <table>
        <tr><th>\( H \)</th><th>RoCoF</th></tr>
        <tr><td>1 s</td><td>−1.78 Hz/s</td></tr>
        <tr><td>3 s</td><td>−0.68 Hz/s</td></tr>
        <tr><td>6 s</td><td>−0.34 Hz/s</td></tr>
      </table>
      <p>Relación inversa: duplicar la inercia mitad el RoCoF. En DC, durante los ms que tarda el
      AFE/BESS en subir la corriente, la energía la pone \( C_{dc} \) y su tensión cae; más \( C_{dc} \),
      menor hundimiento. Las dos palancas son <b>independientes</b>.</p>
    </div>
  </div>
  <div class="repolinks"><b>📚 En el repositorio:</b>
    <a href="../00%20-%20Repositorio/index.html#carga-pulsante-datacenter-ia">Carga pulsante de IA</a> ·
    <a href="../00%20-%20Repositorio/index.html#vsm-inercia">VSM / inercia</a> ·
    <a href="../00%20-%20Repositorio/index.html#integracion-edos-stiff">EDOs stiff</a></div>
</section>

<section id="f4">
  <div class="phase-h"><div class="phase-n" style="background:var(--f4)">4</div>
    <h2 class="sec" style="border:0;margin:0">Fase 4 · Dimensionado</h2></div>
  <p class="lead">Dos requisitos independientes, uno por dominio.</p>
""" + embed("main_phase4.py") + r"""
  <h3>4.1 Resultados reales</h3>
""" + console(R_P4) + r"""
  <figure><img src="results/fase4_dimensionado.png" alt="dimensionado">
    <figcaption>Izq.: condensador mínimo de bus DC vs pico (estabilidad CPL). Der.: inercia mínima vs salto de carga (RoCoF).</figcaption></figure>
  <div class="grid2">
    <div class="card"><h3>Lado DC — condensador</h3>
      <div class="eq">\[ C_{dc}\ge\frac{P_\text{pico}\,L_f}{V_{dc}^2\,R_f} \]</div>
      <p>Ejemplo (250 kW): \( C_{dc}\ge 3.9 \) mF.</p></div>
    <div class="card"><h3>Lado AC — inercia</h3>
      <div class="eq">\[ H\ge\frac{\Delta P\,f_0}{2\,S\,\mathrm{RoCoF}_\text{max}} \]</div>
      <p>Ejemplo (ΔP=150 kW, 1 Hz/s): \( H\ge 3.75 \) s.</p></div>
  </div>
  <div class="def"><b>Hallazgo de diseño:</b> \( C_{dc} \) (DC, estabilidad CPL) y \( H \) (AC, RoCoF) se
  dimensionan por criterios <b>independientes</b>, en dominios distintos. Subir \( C_{dc} \) no ayuda al
  RoCoF, y subir \( H \) no ayuda a la estabilidad CPL. Hay que cumplir ambos por separado.</div>
  <div class="repolinks"><b>📚 En el repositorio:</b>
    <a href="../00%20-%20Repositorio/index.html#robustez-parametrica">Robustez paramétrica</a> ·
    <a href="../00%20-%20Repositorio/index.html#dinamica-bus-dc">Dinámica del bus DC</a></div>
</section>
""")

S.append(r"""<div class="part">Parte IV · Cierre</div>

<section id="discusion">
  <h2 class="sec">9 · Discusión global</h2>
  <p class="lead">Síntesis crítica, contraste con lo esperado y limitaciones.</p>
  <h3>9.1 Coherencia interna</h3>
  <p>El resultado central —la potencia crítica— se obtiene tres veces de forma consistente: por la
  fórmula de Routh-Hurwitz (cap. 2.3, 128&nbsp;kW), por autovalores del modelo linealizado (Fase&nbsp;1,
  129&nbsp;kW) y por el criterio de Middlebrook (Fase&nbsp;2, 134&nbsp;kW). La resonancia L-C que fija el
  pico de \( |Z_\text{fuente}| \) (4.767&nbsp;Ω) es la misma que aparece en el modo del bus. Esta triple
  coincidencia da gran solidez al límite de estabilidad.</p>
  <h3>9.2 Contraste con lo esperado y con la literatura</h3>
  <ul class="tight">
    <li>La inestabilidad CPL reproduce el fenómeno clásico [9],[12]: una resistencia negativa que
    desamortigua un filtro L-C. Es el <b>análogo DC</b> de la resistencia negativa de la PLL del
    grid-following (proyecto 02), lo que unifica los tres proyectos bajo una misma idea.</li>
    <li>El RoCoF medido (−1.78 a −0.34&nbsp;Hz/s para H de 1 a 6&nbsp;s) sigue la ley
    \( \Delta P f_0/(2HS) \) con buena fidelidad, validando el modelo de swing.</li>
    <li>El <b>desacoplo</b> de los dos requisitos de dimensionado (\( C_{dc} \) por CPL, \( H \) por
    RoCoF) es un resultado de diseño relevante: pertenecen a dominios físicos distintos.</li>
  </ul>
  <h3>9.3 Limitaciones</h3>
  <ul class="tight">
    <li>Bus principal idealizado como rígido (el AFE se supone ideal y de respuesta instantánea).</li>
    <li>CPL ideal (potencia exactamente constante); no se modela el ancho de banda finito de los POL.</li>
    <li>Escalón de carga idealizado; un perfil real de IA tiene estadística de picos más compleja.</li>
    <li>Un solo BESS/AFE; sin reparto de carga ni estabilidad de varios convertidores en paralelo.</li>
  </ul>
</section>

<section id="lecciones">
  <h2 class="sec">10 · Lecciones aprendidas</h2>
  <div class="grid2">
    <div class="card"><h3>Sobre la física</h3>
      <ul class="tight">
        <li>El bus DC con CPL es el <b>análogo DC</b> de la inestabilidad por impedancia del
        grid-following: la misma idea de resistencia negativa.</li>
        <li>\( P_\text{crit}=V^2RC/L \) confirmada por dos vías (autovalores y Middlebrook), ~5 %.</li>
        <li>La carga pulsante es el <b>caso de diseño dominante</b>: dimensionar por la media subestima
        ambos requisitos.</li>
      </ul></div>
    <div class="card"><h3>Sobre el diseño</h3>
      <ul class="tight">
        <li>Dos requisitos <b>desacoplados</b>: condensador de bus (DC) e inercia del BESS (AC).</li>
        <li>Para subir el margen CPL hay que <b>bajar el pico de \( |Z_\text{fuente}| \)</b>, no solo
        añadir potencia.</li>
        <li>El mismo formalismo de impedancia explica AC (01–02) y DC (este): es unificador.</li>
      </ul></div>
  </div>
</section>

<section id="concl">
  <h2 class="sec">11 · Conclusiones, aportaciones y líneas futuras</h2>
  <p class="lead">Cierre formal del estudio de la microrred del data center de IA.</p>
  <h3>11.1 Conclusiones generales</h3>
  <ol class="tight">
    <li>El bus DC con CPL se inestabiliza por encima de \( P_\text{crit}=V_{dc}^2R_fC_{dc}/L_f \), valor
    derivado analíticamente (Routh-Hurwitz) y confirmado por autovalores y por Middlebrook (128–134&nbsp;kW,
    ~5&nbsp;%).</li>
    <li>La inestabilidad CPL es el <b>análogo DC</b> de la resistencia negativa de la PLL (proyecto 02):
    el mismo principio de impedancia que en AC.</li>
    <li>Ante el pico de carga de IA, la inercia del BESS gobierna el RoCoF del lado AC
    (\( \propto 1/H \)) y el condensador de bus el hundimiento del lado DC.</li>
    <li>Los dos requisitos de dimensionado (\( C_{dc} \) por estabilidad CPL, \( H \) por RoCoF) son
    <b>desacoplados</b>: pertenecen a dominios físicos distintos y deben cumplirse por separado.</li>
  </ol>
  <h3>11.2 Aportaciones</h3>
  <ol class="tight">
    <li><b>Tratamiento unificado AC+DC</b> de un caso de actualidad (data center de IA), con la
    perturbación naciendo en DC y sintiéndose en AC vía el AFE.</li>
    <li><b>Derivación cerrada</b> de la potencia crítica y su triple verificación.</li>
    <li><b>Reglas de dimensionado</b> explícitas y desacopladas para \( C_{dc} \) y \( H \).</li>
    <li><b>Conexión conceptual</b> de la inestabilidad CPL (DC) con las inestabilidades por impedancia
    AC de los proyectos 01–02, cerrando el repositorio en torno a una idea común.</li>
  </ol>
  <h3>11.3 Limitaciones</h3>
  <p>Resumidas en el cap.&nbsp;9.3: bus principal/AFE idealizados, CPL ideal, escalón de carga simple y
  un solo convertidor.</p>
  <h3>11.4 Líneas futuras</h3>
  <ul class="tight">
    <li>Amortiguamiento activo del bus DC (resistencia virtual DC) para subir \( P_\text{crit} \) sin
    pérdidas.</li>
    <li>Reparto de carga entre varios BESS/AFE y estabilidad del conjunto en paralelo.</li>
    <li>Perfiles reales de carga de IA (estadística de picos) y dimensionado probabilístico.</li>
    <li>Servicios a la red externa (FFR, inercia sintética) y modelo del AFE con ancho de banda finito.</li>
  </ul>
</section>
""")

S.append(r"""
<section id="biblio">
  <h2 class="sec">Bibliografía</h2>
  <table>
    <tr><td>[2]</td><td>Q.-C. Zhong, G. Weiss, "Synchronverters: Inverters that mimic synchronous
      generators," <i>IEEE Trans. Ind. Electron.</i>, vol. 58, no. 4, 2011.</td></tr>
    <tr><td>[9]</td><td>R. D. Middlebrook, "Input filter considerations in design and application of
      switching regulators," <i>IEEE IAS Annual Meeting</i>, 1976.</td></tr>
    <tr><td>[10]</td><td>P. Kundur, <i>Power System Stability and Control</i>. McGraw-Hill, 1994
      (ecuación de oscilación, RoCoF, inercia).</td></tr>
    <tr><td>[12]</td><td>A. Emadi et al., "Constant power loads and negative impedance instability in
      automotive systems," <i>IEEE Trans. Veh. Technol.</i>, vol. 55, no. 4, 2006.</td></tr>
    <tr><td>[13]</td><td>A. P. N. Tahim et al., "Modeling and stability analysis of islanded DC
      microgrids under droop control," <i>IEEE Trans. Power Electron.</i>, vol. 30, no. 8, 2015.</td></tr>
    <tr><td>[14]</td><td>R. H. Lasseter et al., "Grid-forming inverters: a critical asset for the power
      grid," <i>IEEE J. Emerg. Sel. Topics Power Electron.</i>, vol. 8, no. 2, 2020.</td></tr>
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
      <h3>A.1 Bus DC</h3>
      <table>
        <tr><th>Parámetro</th><th>Valor</th></tr>
        <tr><td>\( V_\text{bus} \)</td><td>800 V</td></tr>
        <tr><td>\( L_f \) / \( R_f \)</td><td>50 µH / 5 mΩ</td></tr>
        <tr><td>\( C_{dc} \) (nominal)</td><td>2 mF</td></tr>
        <tr><td>\( P_\text{cpl} \)</td><td>150 kW</td></tr>
        <tr><td>\( P_\text{crit} \)</td><td>128 kW</td></tr>
      </table>
    </div>
    <div>
      <h3>A.2 Lado AC (BESS)</h3>
      <table>
        <tr><th>Parámetro</th><th>Valor</th></tr>
        <tr><td>\( S_\text{ac} \)</td><td>1 MVA</td></tr>
        <tr><td>\( f_\text{ac} \)</td><td>50 Hz</td></tr>
        <tr><td>\( H \) (nominal)</td><td>3 s</td></tr>
        <tr><td>droop AC</td><td>2 %</td></tr>
        <tr><td>filtro potencia \( f_\text{pac} \)</td><td>10 Hz</td></tr>
      </table>
    </div>
  </div>
</section>

<section id="apB">
  <h2 class="sec">Apéndice B · Vectores de estado</h2>
  <h3>B.1 Modelo DC (2) — <span class="file">model_dc.py</span></h3>
  <table>
    <tr><th>#</th><th>Estado</th><th>Significado</th></tr>
    <tr><td>0</td><td><code>iL</code></td><td>corriente del cable de distribución DC</td></tr>
    <tr><td>1</td><td><code>Vdc</code></td><td>tensión del bus DC (rack)</td></tr>
  </table>
  <h3>B.2 Modelo híbrido (4) — <span class="file">simulate.py</span></h3>
  <table>
    <tr><th>#</th><th>Estado</th><th>Significado</th><th>Dominio</th></tr>
    <tr><td>0</td><td><code>iL</code></td><td>corriente del cable DC</td><td>DC</td></tr>
    <tr><td>1</td><td><code>Vdc</code></td><td>tensión del bus DC</td><td>DC</td></tr>
    <tr><td>2</td><td><code>omega</code></td><td>frecuencia del BESS</td><td>AC</td></tr>
    <tr><td>3</td><td><code>Pm</code></td><td>potencia del AFE filtrada</td><td>AC</td></tr>
  </table>
</section>

<section id="apC">
  <h2 class="sec">Apéndice C · Código fuente del proyecto</h2>
  <p class="lead">Los ficheros principales están embebidos en sus capítulos; aquí el de diagramas.</p>
""" + embed("diagramas.py", "Genera el esquema eléctrico y los diagramas de modelo y control en results/.") + r"""
  <div class="note">Ficheros: <span class="file">params.py</span> <span class="file">model_dc.py</span>
  <span class="file">simulate.py</span> <span class="file">main_phase1…4.py</span>
  <span class="file">diagramas.py</span>. Este informe lo genera
  <span class="file">gen_informe.py</span>.</div>
</section>

<section id="apD">
  <h2 class="sec">Apéndice D · Resultados de consola (ejecución real)</h2>
  <h4>Fase 1 — <span class="file">main_phase1.py</span></h4>""" + console(R_P1) + r"""
  <h4>Fase 2 — <span class="file">main_phase2.py</span></h4>""" + console(R_P2) + r"""
  <h4>Fase 3 — <span class="file">main_phase3.py</span></h4>""" + console(R_P3) + r"""
  <h4>Fase 4 — <span class="file">main_phase4.py</span></h4>""" + console(R_P4) + r"""
</section>

<section id="apE">
  <h2 class="sec">Apéndice E · Cómo reproducir</h2>
  <pre>python main_phase1.py    # inestabilidad CPL, P_crit       -> results/fase1_cpl.png
python main_phase2.py    # Middlebrook (impedancia)        -> results/fase2_middlebrook.png
python main_phase3.py    # pico de carga IA (hibrido)      -> results/fase3_pico_carga.png
python main_phase4.py    # dimensionado C_dc y H           -> results/fase4_dimensionado.png
python diagramas.py      # esquema y diagramas
python gen_informe.py    # regenera este informe.html</pre>
  <p class="small">Requiere Python 3.13 con NumPy, SciPy y Matplotlib.</p>
</section>

<section id="apF">
  <h2 class="sec">Apéndice F · Glosario</h2>
  <table>
    <tr><td><b>CPL</b></td><td>Constant power load: potencia constante; resistencia incremental negativa \( -V^2/P \).</td></tr>
    <tr><td><b>BESS / AFE</b></td><td>Batería + inversor grid-forming / rectificador activo AC-DC.</td></tr>
    <tr><td><b>bus DC</b></td><td>Barra de continua que distribuye a los racks; estabilizada por \( C_{dc} \).</td></tr>
    <tr><td><b>Middlebrook</b></td><td>Criterio fuente↔carga: \( |Z_\text{fuente}|<|Z_\text{carga}| \).</td></tr>
    <tr><td><b>RoCoF</b></td><td>Velocidad de cambio de frecuencia tras un escalón.</td></tr>
    <tr><td><b>VSM / \( H \)</b></td><td>Máquina síncrona virtual; \( H \) = constante de inercia (s).</td></tr>
    <tr><td><b>\( P_\text{crit} \)</b></td><td>Potencia CPL máxima estable: \( V_{dc}^2R_fC_{dc}/L_f \).</td></tr>
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

html_out = HEAD + NAV + HERO + link_concepts("".join(S)) + FOOT
with open(os.path.join(HERE, "informe.html"), "w", encoding="utf-8") as fh:
    fh.write(html_out)
print(f"informe.html generado: {html_out.count(chr(10))+1} lineas, {len(html_out)} bytes")
