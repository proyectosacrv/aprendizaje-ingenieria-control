"""Generador del informe HTML (nivel tesis) del proyecto 01 - GFM-Impedance.

Lee los ficheros .py REALES del proyecto, los escapa para HTML y los embebe en el
documento junto a la explicacion detallada y a los resultados de consola capturados
de la ejecucion real de cada script. Reejecutar este generador regenera informe.html.

    python gen_informe.py
"""
import os, html, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
import sys; sys.path.insert(0, os.path.join(HERE, "..", "00 - Repositorio"))
from conceptos_link import link_concepts


def embed(fname, caption=None):
    """Devuelve un bloque de codigo HTML con el contenido REAL del fichero."""
    path = os.path.join(HERE, fname)
    code = open(path, encoding="utf-8").read()
    nlines = code.count("\n") + 1
    esc = html.escape(code)
    cap = f'<div class="cap">{caption}</div>' if caption else ""
    return (f'<div class="codefile"><div class="h"><span>📄 {fname}</span>'
            f'<span>{nlines} líneas · código real del proyecto</span></div>'
            f'<pre>{esc}</pre></div>{cap}')


def console(text):
    """Bloque de salida de consola real."""
    return f'<div class="console">{html.escape(text)}</div>'


# ====================================================================== #
#  RESULTADOS DE CONSOLA REALES (capturados de la ejecucion de cada script)
# ====================================================================== #
R_PHASE1 = """============================================================
FASE 1 - Inversor grid-forming
============================================================
Equilibrio: ier=1  residual=9.69e-11
  P_eq =   5000.0 W   (consigna 5000 W)
  Q_eq =   -554.2 var (consigna 0 var)
  delta = 5.11 deg
  |vc|  = 326.7 V (pico fase, nominal 326.6)

Autovalores (parte real, parte imag, f[Hz], zeta):
         -8.32        +0.00j   f=     0.0 Hz   zeta=+1.000
         -8.93       -20.49j   f=     3.3 Hz   zeta=+0.400
         -8.93       +20.49j   f=     3.3 Hz   zeta=+0.400
        -49.93        +0.00j   f=     0.0 Hz   zeta=+1.000
        -50.08        +0.00j   f=     0.0 Hz   zeta=+1.000
        -54.45       -25.85j   f=     4.1 Hz   zeta=+0.903
        -54.45       +25.85j   f=     4.1 Hz   zeta=+0.903
        -87.52        +0.00j   f=     0.0 Hz   zeta=+1.000
       -100.32        +0.00j   f=     0.0 Hz   zeta=+1.000
       -934.51     +6940.80j   f=  1104.7 Hz   zeta=+0.133
       -934.51     -6940.80j   f=  1104.7 Hz   zeta=+0.133
      -1168.37     +6844.76j   f=  1089.4 Hz   zeta=+0.168
      -1168.37     -6844.76j   f=  1089.4 Hz   zeta=+0.168
      -7188.21      +486.77j   f=    77.5 Hz   zeta=+0.998
      -7188.21      -486.77j   f=    77.5 Hz   zeta=+0.998

Sistema ESTABLE (max Re = -8.32)
Figura guardada en results/polos_fase1.png"""

R_PHASE2 = """Impedancia de salida dq (Z_inv = Y_inv^-1):
   f[Hz]    |Zdd|   /_Zdd    |Zqq|   /_Zqq
     0.1    3.994    87.8    3.827   -85.6
     1.0    1.248    72.6    0.511    52.5
     3.3    2.472    63.1    2.242    61.9
    10.0    4.685    59.1    4.616    59.3
    50.0   16.735    47.1   16.733    47.2
    99.2   25.341    19.4   25.342    19.5
  1001.8    2.423   -17.5    2.423   -17.5
  1096.5    2.024    10.9    2.024    10.9

Figura: results/impedancia_fase2.png"""

R_PHASE3 = """(A) SCR critico (modelo acoplado) = 3.347
(B) SCR critico (Nyquist impedancia) = 3.390
    diferencia = 0.043

Figura: results/nyquist_fase3.png
Interpretacion: al crecer SCR (red mas fuerte) el locus envuelve -1 -> inestable."""

R_PHASE4 = """Midiendo impedancia por inyeccion (puede tardar ~1 min)...
Figura: results/fase4_validacion.png
Error medio |Zdd|: 0.21%  (max 0.83%)

Linealidad: |Zdd| medida a 20 Hz vs amplitud de perturbacion:
   amp[V]  |Zdd|med   error% vs analitica
      1.0     7.788         0.08%
      5.0     7.788         0.08%
     20.0     7.788         0.08%
     80.0     7.788         0.07%
Error ~constante e ~0 -> regimen lineal. La no linealidad por SATURACION de
corriente es un fenomeno de gran senal: ver Fase 5 (current limiting bajo falta)."""

R_SWITCHED = """fsw=10 kHz, filtro L1=2.0mH Cf=20uF
amplitud fundamental vc  = 317.8 V (pico)
rizado de conmutacion (pp) = 7.94 V  (2.50 % de la fundamental)
RMS(conmutado-promediado)/RMS(fundamental) = 0.67 %
-> la dinamica util (fundamental) es identica; el promediado es valido."""

R_PHASE5 = """Figura: results/fase5_inercia.png
Figura: results/fase5_falta.png
  falta sin limite  : pico |i_L1| =   97.1 A  (4.76 pu)
  falta con limite  : pico |i_L1| =   30.7 A  (1.51 pu)
  In nominal = 20.4 A, Imax = 30.6 A"""

R_DIAG = """  baseline               -> max Re =     -8.32  [ESTABLE  ]  (res 9.7e-11)
  sin droop Q (nq=0)     -> max Re =     -7.86  [ESTABLE  ]  (res 9.5e-11)
  droop P /2             -> max Re =     -8.32  [ESTABLE  ]  (res 9.7e-11)
  filtro pot 5 Hz        -> max Re =     -6.53  [ESTABLE  ]  (res 3.3e-11)
  filtro pot 30 Hz       -> max Re =     -8.04  [ESTABLE  ]  (res 4.8e-11)
  lazo V x3              -> max Re =      1.21  [INESTABLE]  (res 4.0e-11)"""


# ====================================================================== #
#  CABECERA, CSS Y NAVEGACION
# ====================================================================== #
HEAD = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GFM · Tesis técnica — modelado, control y estabilidad por impedancia</title>
<style>
  :root{
    --bg:#0f1419; --panel:#161d26; --panel2:#1c2530; --ink:#e6edf3; --muted:#9aa7b4;
    --acc:#4ea3ff; --acc2:#ffb454; --ok:#5ad19a; --bad:#ff6b6b; --line:#2a3542;
    --f1:#4ea3ff; --f2:#a78bfa; --f3:#5ad19a; --f4:#ffb454; --f5:#ff7eb6;
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
  nav a.sub{padding-left:24px;font-size:12px}
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
  p{margin:11px 0} blockquote{margin:14px 0;padding:2px 18px;border-left:3px solid var(--muted);color:var(--muted)}
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
  .step{border-left:3px solid var(--line);padding:4px 0 18px 20px;margin-left:8px;position:relative}
  .step::before{content:"";position:absolute;left:-8px;top:6px;width:13px;height:13px;border-radius:50%;background:var(--acc)}
  .step.bad::before{background:var(--bad)} .step.ok::before{background:var(--ok)} .step.warn::before{background:var(--acc2)}
  .step h4{margin:0 0 4px;font-size:15.5px}
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
  <a href="#estados">6 · Designación de los 15 estados</a>
  <a href="#parametros">7 · Parámetros (params.py)</a>
  <a href="#modelomat">8 · Modelo matemático (model.py)</a>
  <a href="#equilibrio">9 · Equilibrio y linealización</a>
  <h2>III · Desarrollo (fases)</h2>
  <a href="#f1"><span class="badge" style="background:var(--f1)">1</span>Modelo y estabilidad</a>
  <a href="#f2"><span class="badge" style="background:var(--f2)">2</span>Impedancia Z(s)</a>
  <a href="#f3"><span class="badge" style="background:var(--f3)">3</span>Estabilidad en red</a>
  <a href="#f4"><span class="badge" style="background:var(--f4)">4</span>Validación</a>
  <a href="#f5"><span class="badge" style="background:var(--f5)">5</span>Gran señal</a>
  <h2>IV · Diagnóstico</h2>
  <a href="#iter">10 · Proceso de iteración</a>
  <a href="#discusion">11 · Discusión global</a>
  <a href="#lecciones">12 · Lecciones aprendidas</a>
  <a href="#concl">13 · Conclusiones y aportaciones</a>
  <a href="#biblio">Bibliografía</a>
  <h2>Apéndices</h2>
  <a href="#apA">A · Parámetros completos</a>
  <a href="#apB">B · Tabla de estados</a>
  <a href="#apC">C · Código fuente</a>
  <a href="#apD">D · Resultados de consola</a>
  <a href="#apE">E · Reproducir</a>
  <a href="#apF">F · Glosario</a>
  <h2>Enlaces</h2>
  <a href="../index.html">🏠 Inicio (proyectos y repositorio)</a>
  <a href="../00%20-%20Repositorio/index.html">📚 Repositorio</a>
  <a href="../02%20-%20GFL-Impedance/informe.html">📁 02 · GFL</a>
  <a href="../03%20-%20Energia-DataCenter-IA/informe.html">📁 03 · DataCenter</a>
</nav>
<main>
"""

FECHA = datetime.date.today().strftime("%d/%m/%Y")

HERO = r"""<header class="hero">
  <h1>Inversor grid-forming: modelado, control y estabilidad por impedancia</h1>
  <p class="sub">Informe técnico exhaustivo — formulación física, modelo de pequeña señal de 15
  estados, diseño del control, análisis de estabilidad por impedancia y validación, con el código
  de simulación real y sus resultados.</p>
  <p class="meta">Proyecto 01 · Repositorio de aprendizaje de ingeniería de control · Generado el """ + FECHA + r""" a partir del código fuente del proyecto.</p>
  <div class="tagrow">
    <span class="tag">Python 3.13</span><span class="tag">NumPy · SciPy · python-control</span>
    <span class="tag">marco dq</span><span class="tag">droop / VSM</span>
    <span class="tag">impedancia dq 2×2</span><span class="tag">Nyquist generalizado</span>
    <span class="tag">impedancia virtual</span><span class="tag">current limiting</span>
    <span class="tag">linealización numérica</span>
  </div>
</header>
"""

# Lista de fragmentos del cuerpo. Cada elemento es HTML (raw string) o el resultado
# de embed()/console(). Se concatenan al final.
S = []

# ---------------------------------------------------------------- RESUMEN
S.append(r"""
<section id="resumen">
  <h2 class="sec">Resumen ejecutivo</h2>
  <p class="lead">Qué se hace, cómo, con qué código, y qué resultados reales se obtienen.</p>

  <p>Este documento reconstruye, con detalle de tesis, el diseño y análisis completo de un
  <b>inversor formador de red</b> (grid-forming, GFM) de 10&nbsp;kVA conectado a través de un filtro
  LCL. A diferencia de un resumen de resultados, aquí se explica <b>cada decisión</b>: por qué se elige
  un modelo no lineal linealizado numéricamente, cómo se designa cada uno de los 15 estados, de dónde
  sale cada ecuación, qué hace literalmente cada línea relevante del código, y qué número exacto
  produce cada simulación. Todo el código mostrado es el <b>código real</b> del proyecto, leído de los
  ficheros <code class="inl">.py</code>, y todos los resultados numéricos son la <b>salida de consola
  real</b> capturada al ejecutarlos.</p>

  <div class="kpi">
    <div class="b"><div class="n">15</div><div class="l">estados del modelo dq</div></div>
    <div class="b"><div class="n">−8.32</div><div class="l">máx. parte real (estable)</div></div>
    <div class="b"><div class="n">ζ = 0.40</div><div class="l">modo de potencia 3.3 Hz</div></div>
    <div class="b"><div class="n">0.21 %</div><div class="l">error validación impedancia</div></div>
    <div class="b"><div class="n">1.3 %</div><div class="l">SCR crítico (2 métodos)</div></div>
    <div class="b"><div class="n">0.67 %</div><div class="l">promediado vs conmutado</div></div>
    <div class="b"><div class="n">1.51 pu</div><div class="l">falta con current limiting</div></div>
  </div>

  <p>El hilo conductor metodológico es la <b>doble validación</b>: cada resultado importante se obtiene
  por dos vías independientes que deben coincidir. El SCR crítico se calcula por autovalores del modelo
  acoplado <i>y</i> por Nyquist de impedancia (coinciden al 1.3&nbsp;%); la impedancia se obtiene
  analíticamente <i>y</i> por inyección sobre el modelo no lineal (0.21&nbsp;%); el modelo promediado se
  contrasta con el conmutado (0.67&nbsp;%). Esa concordancia es la prueba de que el método es fiable.</p>

  <p>El segundo hilo es el <b>proceso de iteración</b> (capítulo 10): el primer diseño salió inestable
  (\( \max\mathrm{Re}=+37 \)) y el documento reconstruye el diagnóstico paso a paso hasta el diseño
  final estable y amortiguado, con el código de diagnóstico y sus salidas reales.</p>

  <h3>Resumen</h3>
  <p>Se presenta el modelado en pequeña señal, el diseño del control y el análisis de estabilidad por
  impedancia de un inversor formador de red (grid-forming) trifásico de 10&nbsp;kVA con filtro LCL,
  conectado a una red modelada como equivalente Thévenin parametrizado por su relación de cortocircuito
  (SCR). El modelo no lineal en el marco \( dq \), de quince variables de estado, se obtiene escribiendo
  las ecuaciones físicas y linealizándolo numéricamente en torno a su punto de equilibrio mediante un
  Jacobiano por diferencias finitas centradas. A partir del modelo lineal se calculan los modos propios,
  se sintetiza la matriz de impedancia de salida \( \mathbf{Z}_{dq}(s) \) y se evalúa la estabilidad de
  la interacción convertidor-red con el criterio de Nyquist generalizado. La metodología se sustenta en
  la <b>validación por dos vías independientes</b> de cada resultado relevante. Se documenta además el
  proceso de diagnóstico que llevó de un diseño inicial inestable a uno estable y bien amortiguado, y se
  estudian los fenómenos de gran señal (inercia virtual y limitación de corriente) que el análisis lineal
  no captura.</p>
  <p><b>Palabras clave:</b> inversor grid-forming; estabilidad por impedancia; marco dq; criterio de
  Nyquist generalizado; impedancia virtual; máquina síncrona virtual; redes débiles; SCR.</p>

  <h3>Abstract</h3>
  <p>This work presents the small-signal modelling, control design and impedance-based stability analysis
  of a 10&nbsp;kVA three-phase grid-forming inverter with an LCL filter, connected to a grid represented
  as a Thévenin equivalent parameterised by its short-circuit ratio (SCR). A fifteen-state nonlinear
  model in the \( dq \) frame is built from the physical equations and linearised numerically around its
  equilibrium point by means of a central finite-difference Jacobian. From the linear model, the modal
  eigenvalues are computed, the output impedance matrix \( \mathbf{Z}_{dq}(s) \) is synthesised, and the
  stability of the converter-grid interaction is assessed with the generalised Nyquist criterion. The
  methodology relies on the <b>cross-validation of every key result through two independent routes</b>.
  The diagnostic process that led from an initial unstable design to a stable, well-damped one is
  documented, and the large-signal phenomena (virtual inertia and current limiting) not captured by the
  linear analysis are studied.</p>
  <p><b>Keywords:</b> grid-forming inverter; impedance-based stability; dq frame; generalised Nyquist
  criterion; virtual impedance; virtual synchronous machine; weak grids; SCR.</p>
</section>

<section id="nomenclatura">
  <h2 class="sec">Nomenclatura</h2>
  <p class="lead">Símbolos, subíndices y acrónimos empleados en la memoria.</p>
  <div class="grid2">
    <div>
      <h3>Magnitudes eléctricas</h3>
      <table>
        <tr><th>Símbolo</th><th>Significado</th><th>Unidad</th></tr>
        <tr><td>\( \mathbf{i}_{L1} \)</td><td>corriente del inductor lado inversor (d,q)</td><td>A</td></tr>
        <tr><td>\( \mathbf{v}_C \)</td><td>tensión del condensador de filtro (d,q)</td><td>V</td></tr>
        <tr><td>\( \mathbf{i}_{L2}=\mathbf{i}_g \)</td><td>corriente lado red / inyectada (d,q)</td><td>A</td></tr>
        <tr><td>\( \mathbf{v}_i \)</td><td>tensión de salida del puente</td><td>V</td></tr>
        <tr><td>\( \mathbf{v}_{pcc} \)</td><td>tensión en el punto de conexión común</td><td>V</td></tr>
        <tr><td>\( P,\,Q \)</td><td>potencia activa, reactiva</td><td>W, var</td></tr>
        <tr><td>\( \delta \)</td><td>ángulo marco control − marco red</td><td>rad</td></tr>
        <tr><td>\( \omega,\,\omega_0 \)</td><td>frecuencia del inversor, nominal</td><td>rad/s</td></tr>
      </table>
      <h3>Parámetros</h3>
      <table>
        <tr><th>Símbolo</th><th>Significado</th></tr>
        <tr><td>\( L_1,R_1,C_f,L_2,R_2 \)</td><td>elementos del filtro LCL</td></tr>
        <tr><td>\( R_g,L_g \)</td><td>resistencia e inductancia de red</td></tr>
        <tr><td>\( m_p,\,n_q \)</td><td>pendientes de droop P-f, Q-V</td></tr>
        <tr><td>\( R_v,X_v,R_{vt} \)</td><td>impedancia virtual (R, X, R transit.)</td></tr>
        <tr><td>\( K_\text{ad} \)</td><td>ganancia de amortiguamiento activo</td></tr>
        <tr><td>\( H,\,J,\,D \)</td><td>constante de inercia, inercia, damping VSM</td></tr>
      </table>
    </div>
    <div>
      <h3>Operadores y modelo</h3>
      <table>
        <tr><th>Símbolo</th><th>Significado</th></tr>
        <tr><td>\( \mathbf{x},\mathbf{u},\mathbf{y} \)</td><td>estado, entrada, salida</td></tr>
        <tr><td>\( \mathbf{f}(\cdot) \)</td><td>campo vectorial no lineal</td></tr>
        <tr><td>\( A,B,C,D \)</td><td>matrices del modelo lineal</td></tr>
        <tr><td>\( \mathbf{J} \)</td><td>\( [[0,-1],[1,0]] \), rotación 90°</td></tr>
        <tr><td>\( \mathbf{R}(\theta) \)</td><td>matriz de rotación de ángulo \( \theta \)</td></tr>
        <tr><td>\( \mathbf{Y}_\text{inv},\mathbf{Z}_\text{inv} \)</td><td>admitancia / impedancia de salida (2×2)</td></tr>
        <tr><td>\( \mathbf{L}(s) \)</td><td>minor loop gain \( Z_\text{red}Y_\text{inv} \)</td></tr>
        <tr><td>\( \lambda,\,\zeta \)</td><td>autovalor, amortiguamiento</td></tr>
      </table>
      <h3>Acrónimos</h3>
      <table>
        <tr><th>Sigla</th><th>Significado</th></tr>
        <tr><td>GFM / GFL</td><td>grid-forming / grid-following</td></tr>
        <tr><td>VSC</td><td>voltage source converter</td></tr>
        <tr><td>LCL</td><td>filtro inductor-condensador-inductor</td></tr>
        <tr><td>PLL</td><td>phase-locked loop</td></tr>
        <tr><td>VSM</td><td>virtual synchronous machine</td></tr>
        <tr><td>SCR</td><td>short-circuit ratio</td></tr>
        <tr><td>PWM</td><td>pulse-width modulation</td></tr>
        <tr><td>RoCoF</td><td>rate of change of frequency</td></tr>
      </table>
    </div>
  </div>
  <p class="small">Convenio: negrita para vectores/matrices; magnitudes dq referidas a amplitud de
  <b>pico de fase</b> (\( V_0=V_{ll}\sqrt{2/3} \)); potencia trifásica \( P=\tfrac32(v_di_d+v_qi_q) \).</p>
</section>

<section id="indice">
  <h2 class="sec">Índice, objetivos y alcance</h2>
  <h3>Objetivos</h3>
  <ol class="tight">
    <li><b>Modelar</b> el inversor GFM en el marco dq con todas sus capas de control (cascada,
    impedancia virtual, amortiguamiento activo, droop) y obtener su modelo de pequeña señal.</li>
    <li><b>Diseñar</b> el control para que sea estable y bien amortiguado, documentando el proceso de
    diagnóstico de la inestabilidad inicial.</li>
    <li><b>Caracterizar</b> la impedancia de salida \( Z_{dq}(s) \) y usarla para evaluar la estabilidad
    de la interacción con redes de distinta fortaleza (SCR).</li>
    <li><b>Validar</b> el modelo: la linealización (por inyección de perturbación) y el promediado
    (frente al modelo conmutado PWM).</li>
    <li><b>Estudiar</b> el régimen de gran señal: inercia virtual (VSM) y limitación de corriente bajo
    falta.</li>
  </ol>
  <h3>Estructura del documento</h3>
  <div class="flow">
    <div class="n"><b>I. Preliminares</b><br>problema, teoría, método</div><div class="ar">→</div>
    <div class="n"><b>II. Modelado</b><br>físico → estados → ecuaciones → código</div><div class="ar">→</div>
    <div class="n"><b>III. Fases 1–5</b><br>desarrollo con código y resultados</div><div class="ar">→</div>
    <div class="n"><b>IV. Diagnóstico</b><br>iteración, lecciones, cierre</div>
  </div>
  <div class="note"><b>Convenio del documento:</b> los bloques <span class="file">📄 fichero.py</span>
  contienen el código fuente real; los bloques verdes con borde a la izquierda son la salida de
  consola real de ejecutar ese código. Las fórmulas se muestran en notación matemática (MathJax).</div>
</section>
""")

# ---------------------------------------------------------------- PARTE I
S.append(r"""<div class="part">Parte I · Preliminares</div>

<section id="problema">
  <h2 class="sec">1 · Planteamiento del problema</h2>
  <p class="lead">Por qué un grid-forming, por qué su impedancia, y qué hay que demostrar.</p>

  <h3>1.1 Contexto: la red cambia de naturaleza</h3>
  <p>La red eléctrica tradicional se sostiene sobre <b>máquinas síncronas</b>: grandes masas rotantes
  cuya inercia física amortigua las perturbaciones y cuya tensión y frecuencia sirven de referencia a
  todo lo demás. La sustitución masiva de generación síncrona por <b>convertidores de electrónica de
  potencia</b> elimina esa inercia y esa referencia: la mayoría de los convertidores instalados son
  <b>grid-following</b> y dependen de que otro forme la red. Cuando la proporción de convertidores
  crece lo suficiente, deja de haber quién forme la tensión, y el sistema se vuelve inestable. El
  inversor <b>grid-forming</b> resuelve esto comportándose como una fuente de tensión —como una máquina
  síncrona— capaz de sostener la red por sí mismo. Es la tecnología clave para redes con alta
  penetración renovable y para microrredes.</p>

  <div class="grid2">
    <div class="card"><h3>Grid-following (GFL)</h3>
      <p>Mide el ángulo de red con una PLL e <b>inyecta corriente</b>: fuente de corriente controlada.
      Necesita una red preexistente y <b>pierde estabilidad en red débil</b> (SCR bajo), donde su propia
      corriente mueve mucho la tensión y la PLL se confunde.</p></div>
    <div class="card"><h3>Grid-forming (GFM)</h3>
      <p><b>Impone tensión</b> con su propia frecuencia interna (droop o VSM): fuente de tensión detrás
      de una impedancia. No necesita PLL para sincronizar y es robusto en red débil. Su reto se
      desplaza a la limitación de corriente bajo falta.</p></div>
  </div>

  <h3>1.2 Por qué el enfoque de impedancia</h3>
  <p>Estudiar la estabilidad re-simulando todo el sistema cada vez que cambia la red es caro y poco
  revelador. El enfoque de impedancia descompone el problema: el inversor se reduce a su admitancia de
  salida \( Y_\text{inv}(s) \) (matriz 2×2 en dq, obtenida una vez), y la red a su impedancia
  \( Z_\text{red}(s) \) (un parámetro: el SCR). La estabilidad del conjunto la decide el <b>minor loop
  gain</b> \( L(s)=Z_\text{red}(s)\,Y_\text{inv}(s) \) por el criterio de Nyquist generalizado. La
  ventaja es doble: barrer la fortaleza de red es cambiar un parámetro (no re-modelar), y el resultado
  es interpretable —se ve en qué frecuencia y por qué se cruza el límite.</p>

  <div class="note"><b>Objetivo concreto:</b> diseñar el control (Fase&nbsp;1), caracterizar la
  impedancia (Fase&nbsp;2), hallar el SCR crítico validando el criterio de impedancia contra el modelo
  acoplado (Fase&nbsp;3), validar la linealización y el promediado (Fase&nbsp;4) y estudiar inercia y
  faltas (Fase&nbsp;5).</div>

  <div class="repolinks"><b>📚 En el repositorio:</b>
    <a href="../00%20-%20Repositorio/index.html#grid-forming-vs-following">Grid-forming vs grid-following</a> ·
    <a href="../00%20-%20Repositorio/index.html#red-thevenin-scr">Red Thévenin, SCR y X/R</a> ·
    <a href="../00%20-%20Repositorio/index.html#convertidor-vsc">Convertidor VSC</a></div>
</section>

<section id="marco">
  <h2 class="sec">2 · Estado del arte y marco teórico</h2>
  <p class="lead">Antecedentes en la literatura y los fundamentos matemáticos que sostienen el análisis.</p>

  <h3>2.1 Estado del arte</h3>
  <p>El control de convertidores conectados a red se organiza tradicionalmente en dos familias. Los
  <b>grid-following</b>, que siguen la tensión de red con una PLL e inyectan corriente, son la
  arquitectura dominante del parque renovable instalado; su limitación en redes débiles está bien
  documentada y se asocia a la interacción de la PLL con la impedancia de red [5],[6]. Frente a ellos,
  los <b>grid-forming</b> imponen tensión y frecuencia, emulando el comportamiento de una máquina
  síncrona, y son considerados habilitadores de redes con muy alta penetración de electrónica de
  potencia [7],[8].</p>
  <p>Dentro del grid-forming, las estrategias de sincronización primaria más extendidas son el
  <b>control por estatismo</b> (droop) [1] y la <b>máquina síncrona virtual</b> (VSM/VSG) [2], que
  añade inercia mediante la ecuación de oscilación. Un problema recurrente del grid-forming sobre filtro
  LCL es la baja amortiguación del modo de sincronización cuando la reactancia de acoplamiento es
  pequeña; la solución canónica es la <b>impedancia virtual</b> [3], que emula reactancia por software
  sin elemento físico.</p>
  <p>Para analizar la estabilidad de la interacción convertidor-red sin reconstruir el sistema completo,
  el <b>enfoque de impedancia</b> [4] modela cada lado como una impedancia (o admitancia) y aplica el
  <b>criterio de Nyquist generalizado</b> al producto \( \mathbf{Z}_\text{red}\mathbf{Y}_\text{inv} \).
  Su raíz está en el criterio de Middlebrook para convertidores DC-DC [9], extendido al dominio
  \( dq \) trifásico. Este trabajo se inscribe en esa línea y la aplica de extremo a extremo —del modelo
  físico a la validación por inyección— con verificación cruzada de cada resultado.</p>
  <div class="note"><b>Aportación frente al estado del arte (alcance docente):</b> el valor de esta
  memoria no es un método nuevo, sino la <b>integración reproducible</b> de todo el flujo (modelado →
  impedancia → Nyquist generalizado → validación por inyección → gran señal) sobre un mismo caso, con el
  código abierto, los resultados verificados por dos vías, y el proceso de diagnóstico de la
  inestabilidad documentado paso a paso.</div>

  <h3>2.2 El marco \( dq \) y la derivación del acoplamiento cruzado</h3>
  <p>Las magnitudes trifásicas se transforman al marco \( dq \) (Park), que gira a la frecuencia de red.
  En régimen permanente las senoides se convierten en <b>constantes</b>, lo que permite control PI con
  error nulo en continua y linealización en torno a un punto estacionario. El precio es un acoplamiento
  cruzado d↔q que conviene <b>derivar</b> explícitamente. Sea una magnitud vectorial
  \( \mathbf{x}_{abc} \) que en el marco estacionario \( \alpha\beta \) es \( \mathbf{x}_s \); en el
  marco giratorio \( \mathbf{x}_{dq}=\mathbf{R}(-\theta)\mathbf{x}_s \) con
  \( \theta=\int\omega\,dt \). Derivando un elemento inductivo \( \mathbf{v}=L\,d\mathbf{i}_s/dt \) y
  sustituyendo \( \mathbf{i}_s=\mathbf{R}(\theta)\mathbf{i}_{dq} \):</p>
  <div class="eq">\[ \mathbf{v}_s=L\frac{d}{dt}\!\big(\mathbf{R}(\theta)\mathbf{i}_{dq}\big)
     =L\,\mathbf{R}(\theta)\Big(\frac{d\mathbf{i}_{dq}}{dt}+\omega\mathbf{J}\,\mathbf{i}_{dq}\Big),
     \qquad \mathbf{J}=\begin{bmatrix}0&-1\\1&0\end{bmatrix} \]</div>
  <p>de donde, proyectando al marco \( dq \),
  \( L\,d\mathbf{i}_{dq}/dt=\mathbf{v}_{dq}-\omega L\,\mathbf{J}\,\mathbf{i}_{dq} \). El término
  \( \omega L\mathbf{J} \) es precisamente el acoplamiento cruzado \( \pm\omega L \) que aparece en las
  ecuaciones de la planta (cap. 8) y que el control cancela mediante desacoplo. La misma derivación con
  un condensador da el término \( \omega C\mathbf{J} \).</p>

  <h3>2.3 Estabilidad por autovalores (análisis modal)</h3>
  <p>Linealizado el sistema a \( \Delta\dot{\mathbf{x}}=A\,\Delta\mathbf{x} \), su solución es
  combinación de modos \( e^{\lambda_i t} \). El sistema es asintóticamente estable si y solo si
  \( \mathrm{Re}(\lambda_i)<0\ \forall i \). De cada autovalor \( \lambda=\sigma\pm j\omega_d \) se lee
  la frecuencia \( f=\omega_d/2\pi \) y el amortiguamiento
  \( \zeta=-\sigma/|\lambda| \). Los <b>factores de participación</b>
  \( p_{ki}=\dfrac{|\phi_{ki}||\psi_{ik}|}{\sum_j|\phi_{ji}||\psi_{ij}|} \) (con \( \phi,\psi \) los
  autovectores derecho e izquierdo) indican qué estado \( k \) domina el modo \( i \), herramienta clave
  para diagnosticar qué lazo causa una inestabilidad (cap. 10).</p>

  <h3>2.4 Impedancia de salida y criterio de Nyquist generalizado</h3>
  <p>Del modelo lineal, la respuesta del puerto es
  \( \mathbf{G}(s)=\mathbf{C}(s\mathbf{I}-A)^{-1}\mathbf{B}+\mathbf{D} \). Con el convenio de corriente
  saliente, la admitancia de salida es \( \mathbf{Y}_\text{inv}=-\mathbf{G} \) y la impedancia
  \( \mathbf{Z}_\text{inv}=\mathbf{Y}_\text{inv}^{-1} \), matrices 2×2 por el acoplamiento d-q.
  Conectado el inversor (fuente Norton \( \mathbf{Y}_\text{inv} \)) a la red (\( \mathbf{Z}_\text{red} \)),
  la corriente de interacción contiene el factor \( (\mathbf{I}+\mathbf{Z}_\text{red}\mathbf{Y}_\text{inv})^{-1} \).
  La estabilidad del lazo, asumiendo subsistemas individualmente estables, equivale a que
  \( \mathbf{L}(s)=\mathbf{Z}_\text{red}\mathbf{Y}_\text{inv} \) cumpla el <b>criterio de Nyquist
  generalizado</b>: el locus de los <b>autovalores</b> de \( \mathbf{L}(j\omega) \) no debe rodear el
  punto \( -1 \). De forma equivalente y más cómoda de barrer numéricamente,
  \( \det(\mathbf{I}+\mathbf{L}(j\omega))\neq 0\ \forall\omega \): el mínimo de
  \( |\det(\mathbf{I}+\mathbf{L})| \) pasando por cero marca la frontera de estabilidad (cap. Fase 3).</p>

  <h3>2.5 Pequeña señal frente a gran señal</h3>
  <p>Impedancia y autovalores describen el comportamiento en <b>pequeña señal</b> (perturbaciones
  infinitesimales en torno al equilibrio, régimen lineal). En cuanto una no linealidad fuerte se
  activa —típicamente la <b>saturación de corriente</b>— el concepto de impedancia lineal pierde validez
  y es necesaria la <b>simulación temporal no lineal</b> (gran señal). Esta memoria cubre ambos
  regímenes: pequeña señal en las Fases 1–4, gran señal en la Fase 5.</p>

  <div class="repolinks"><b>📚 En el repositorio:</b>
    <a href="../00%20-%20Repositorio/index.html#marco-dq">Marco dq</a> ·
    <a href="../00%20-%20Repositorio/index.html#analisis-modal">Análisis modal</a> ·
    <a href="../00%20-%20Repositorio/index.html#impedancia-salida-estabilidad">Estabilidad por impedancia</a> ·
    <a href="../00%20-%20Repositorio/index.html#nyquist-generalizado">Nyquist generalizado</a></div>
</section>

<section id="sw">
  <h2 class="sec">3 · Software, herramientas y método</h2>
  <p class="lead">Todo en Python; el análisis principal se hace a mano para que sea transparente.</p>
  <table>
    <tr><th>Herramienta</th><th>Rol en el proyecto</th></tr>
    <tr><td><b>Python 3.13</b></td><td>Lenguaje base de todo el análisis</td></tr>
    <tr><td><b>NumPy</b></td><td>Álgebra lineal, autovalores (<code class="inl">linalg.eigvals</code>), resolución de \( (sI-A)^{-1}B \)</td></tr>
    <tr><td><b>SciPy</b></td><td><code class="inl">optimize.fsolve</code> (equilibrio), <code class="inl">integrate.solve_ivp</code> (simulación temporal stiff, LSODA)</td></tr>
    <tr><td><b>Matplotlib</b></td><td>Todas las figuras (mapa de polos, Bode, Nyquist, transitorios)</td></tr>
    <tr><td><b>python-control</b></td><td>Disponible; el análisis se hace a mano para máxima transparencia</td></tr>
    <tr><td><b>PLECS</b> <span class="pill warn">pendiente</span></td><td>Validación sobre el modelo conmutado (IGBTs, PWM)</td></tr>
  </table>

  <h3>3.1 La decisión central: linealización numérica</h3>
  <p>Hay dos formas de obtener el modelo de pequeña señal \( (A,B,C,D) \): derivarlo a mano (exacto pero
  frágil ante cada cambio de control) o escribir solo las ecuaciones físicas no lineales
  \( f(\mathbf{x},\mathbf{u}) \) y dejar que el ordenador derive por <b>diferencias finitas</b>. Se
  elige lo segundo. El coste —resolver el equilibrio numéricamente antes de linealizar— se paga una vez;
  a cambio, añadir el VSM, la saturación o la impedancia virtual no obliga a rehacer ningún álgebra. Es
  el enfoque profesional cuando el sistema es complejo, y la columna vertebral de todo el proyecto.</p>

  <div class="repolinks"><b>📚 En el repositorio:</b>
    <a href="../00%20-%20Repositorio/index.html#linealizacion-numerica">Linealización numérica</a> ·
    <a href="../00%20-%20Repositorio/index.html#equilibrio-fsolve">Equilibrio (fsolve)</a> ·
    <a href="../00%20-%20Repositorio/index.html#integracion-edos-stiff">Integración de EDOs stiff</a></div>
</section>
""")

# ---------------------------------------------------------------- PARTE II
S.append(r"""<div class="part">Parte II · Modelado</div>

<section id="fisica">
  <h2 class="sec">4 · El sistema físico</h2>
  <p class="lead">Etapa de potencia (filtro LCL), conexión a red y control en cascada.</p>
  <div class="card">
  <svg viewBox="0 0 920 300" style="width:100%;height:auto;font-family:monospace;font-size:12px">
    <defs><marker id="ah" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="#9aa7b4"/></marker></defs>
    <rect x="20" y="60" width="70" height="60" rx="6" fill="#1c2530" stroke="#4ea3ff"/>
    <text x="55" y="85" fill="#e6edf3" text-anchor="middle">Vdc</text>
    <text x="55" y="102" fill="#9aa7b4" text-anchor="middle">750 V</text>
    <rect x="120" y="55" width="90" height="70" rx="6" fill="#1c2530" stroke="#4ea3ff"/>
    <text x="165" y="83" fill="#e6edf3" text-anchor="middle">Puente</text>
    <text x="165" y="100" fill="#9aa7b4" text-anchor="middle">2 niveles</text>
    <line x1="90" y1="90" x2="120" y2="90" stroke="#9aa7b4" marker-end="url(#ah)"/>
    <line x1="210" y1="90" x2="270" y2="90" stroke="#9aa7b4"/>
    <rect x="270" y="80" width="55" height="20" fill="none" stroke="#5ad19a"/>
    <text x="297" y="74" fill="#5ad19a" text-anchor="middle">L1 2mH</text>
    <line x1="325" y1="90" x2="400" y2="90" stroke="#9aa7b4"/>
    <circle cx="400" cy="90" r="4" fill="#ffb454"/>
    <text x="400" y="58" fill="#ffb454" text-anchor="middle">v_C</text>
    <line x1="400" y1="90" x2="400" y2="150" stroke="#9aa7b4"/>
    <rect x="385" y="150" width="30" height="14" fill="none" stroke="#a78bfa"/>
    <text x="445" y="162" fill="#a78bfa" text-anchor="middle">Cf 20µF</text>
    <line x1="400" y1="164" x2="400" y2="195" stroke="#9aa7b4"/>
    <line x1="385" y1="195" x2="415" y2="195" stroke="#9aa7b4"/>
    <line x1="400" y1="90" x2="470" y2="90" stroke="#9aa7b4"/>
    <rect x="470" y="80" width="55" height="20" fill="none" stroke="#5ad19a"/>
    <text x="497" y="74" fill="#5ad19a" text-anchor="middle">L2 1mH</text>
    <line x1="525" y1="90" x2="600" y2="90" stroke="#9aa7b4"/>
    <circle cx="600" cy="90" r="4" fill="#ff7eb6"/>
    <text x="600" y="58" fill="#ff7eb6" text-anchor="middle">PCC</text>
    <line x1="600" y1="90" x2="660" y2="90" stroke="#9aa7b4"/>
    <rect x="660" y="80" width="60" height="20" fill="none" stroke="#ff6b6b"/>
    <text x="690" y="74" fill="#ff6b6b" text-anchor="middle">Z_red</text>
    <line x1="720" y1="90" x2="780" y2="90" stroke="#9aa7b4"/>
    <circle cx="820" cy="90" r="28" fill="#1c2530" stroke="#ff6b6b"/>
    <text x="820" y="86" fill="#e6edf3" text-anchor="middle">red</text>
    <text x="820" y="102" fill="#9aa7b4" text-anchor="middle">SCR,X/R</text>
    <line x1="780" y1="90" x2="792" y2="90" stroke="#9aa7b4"/>
    <rect x="120" y="210" width="405" height="70" rx="8" fill="#10202e" stroke="#2a3542"/>
    <text x="135" y="232" fill="#cdd9e5">CONTROL (marco dq, ω del propio inversor)</text>
    <text x="135" y="252" fill="#9aa7b4">droop/VSM → v_C* → PI tensión → i_L1* → PI corriente → PWM</text>
    <text x="135" y="270" fill="#9aa7b4">+ impedancia virtual + amortiguamiento activo LCL + current limiting</text>
    <line x1="165" y1="210" x2="165" y2="125" stroke="#4ea3ff" stroke-dasharray="4" marker-end="url(#ah)"/>
  </svg>
  </div>

  <h3>4.1 El filtro LCL y su resonancia</h3>
  <p>El inversor conmuta a 10&nbsp;kHz; el filtro LCL atenúa los armónicos de conmutación con pendiente
  de −60&nbsp;dB/dec (frente a −20 de un filtro L), más atenuación con menos inductancia. Su pega es una
  resonancia aguda con amortiguamiento casi nulo:</p>
  <div class="eq">\[ f_\text{res}=\frac{1}{2\pi}\sqrt{\frac{L_1+L_2}{L_1 L_2 C_f}}
     =\frac{1}{2\pi}\sqrt{\frac{3\times10^{-3}}{(2\times10^{-3})(1\times10^{-3})(20\times10^{-6})}}
     \approx 1.1\ \text{kHz} \]</div>
  <p>La simulación lo confirma con precisión: los autovalores de la resonancia LCL aparecen a
  1104.7&nbsp;Hz y 1089.4&nbsp;Hz (Fase&nbsp;1). Sin tratarla, esa resonancia desestabiliza cualquier
  lazo rápido; se doma con <b>amortiguamiento activo</b> (§4.4).</p>

  <h3>4.2 Grid-forming vs grid-following</h3>
  <p>El GFM impone tensión con su frecuencia interna (sin PLL) y es robusto en red débil; el GFL inyecta
  corriente siguiendo una PLL y falla en red débil. La firma de impedancia (Fase&nbsp;2) lo confirma:
  inductiva en banda media (fase +47°…+59°), como una máquina síncrona.</p>

  <h3>4.3 Impedancia virtual: la pieza que estabiliza el lazo de potencia</h3>
  <p>Con reactancia de acoplamiento pequeña, la ganancia de sincronización
  \( \partial P/\partial\delta\approx 1.5\,V^2/X \) es enorme y el lazo de potencia es difícil de
  estabilizar (es lo que ocurrió en el primer diseño, cap. 10). La impedancia virtual emula impedancia
  restándola de la referencia de tensión, sin componente físico:</p>
  <div class="eq">\[ \mathbf{v}_C^*=V_\text{ref}-(R_v\,\mathbf{i}_{L2}+X_v\,\mathbf{J}\,\mathbf{i}_{L2}) \]</div>
  <ul class="tight">
    <li>La parte <b>inductiva</b> \( X_v \) baja \( \partial P/\partial\delta \) sin caída resistiva:
    estabiliza sin distorsionar el equilibrio (la caída cae en el eje q, mantenido en cero).</li>
    <li>La parte <b>resistiva</b> \( R_v \) amortigua pero su caída cae en el eje d y pelea con el droop
    Q-V (dispara \( Q_\text{eq} \)); por eso se usa poca \( R_v \) estática.</li>
  </ul>

  <h3>4.4 Amortiguamiento activo y resistencia virtual transitoria</h3>
  <p>El <b>amortiguamiento activo</b> realimenta la corriente del condensador
  (\( \mathbf{i}_{L1}-\mathbf{i}_{L2} \)) con ganancia \( K_\text{ad} \), emulando una resistencia que
  amortigua la resonancia LCL sin pérdidas. La <b>resistencia virtual transitoria</b> aplica \( R_{vt} \)
  solo a la componente transitoria de la corriente (vía un paso-alto): amortigua el modo de potencia sin
  afectar al equilibrio (en DC su efecto es cero).</p>

  <h3>4.5 Control en cascada</h3>
  <div class="flow">
    <div class="n">Potencia / droop<br><b>~3 Hz</b></div><div class="ar">→</div>
    <div class="n">Tensión<br><b>~350 Hz</b></div><div class="ar">→</div>
    <div class="n">Corriente<br><b>~1 kHz</b></div>
  </div>
  <p>Tres lazos anidados, cada interno ~3–5× más rápido que el externo. El ángulo lo genera el droop,
  sin PLL. El desacoplo dq cancela el acoplamiento cruzado para controlar cada eje por separado.</p>

  <div class="repolinks"><b>📚 En el repositorio:</b>
    <a href="../00%20-%20Repositorio/index.html#filtro-lcl">Filtro LCL</a> ·
    <a href="../00%20-%20Repositorio/index.html#impedancia-virtual">Impedancia virtual</a> ·
    <a href="../00%20-%20Repositorio/index.html#amortiguamiento-activo-lcl">Amortiguamiento activo</a> ·
    <a href="../00%20-%20Repositorio/index.html#control-cascada">Control en cascada</a></div>
</section>

<section id="marcos">
  <h2 class="sec">5 · Marcos de referencia (la clave del grid-forming)</h2>
  <p class="lead">Dos marcos giratorios y el ángulo que los acopla.</p>
  <p>Un GFM genera su propia frecuencia, así que conviven dos marcos dq giratorios:</p>
  <ul class="tight">
    <li><b>Marco \( s \) (sistema/red):</b> gira a \( \omega_0 \) constante. Es la referencia común;
    aquí se define el puerto con la red y se expresa la impedancia de salida.</li>
    <li><b>Marco \( c \) (control):</b> gira a \( \omega \), la frecuencia que fija el droop. El inversor
    vive en este marco.</li>
    <li>\( \delta=\theta_c-\theta_s \) es el ángulo entre ambos, con \( \dot\delta=\omega-\omega_0 \).</li>
  </ul>
  <p>La pequeña señal de \( \delta \) es <b>lo que acopla</b> la dinámica de potencia con la eléctrica.
  Una tensión de red fija en \( s \) se ve <b>rotada</b> por \( \delta \) desde \( c \); este término de
  rotación es el corazón del modelo y la fuente de los acoplamientos sutiles:</p>
  <div class="eq">\[ \mathbf{v}_{pcc}^{c}=\mathbf{R}(-\delta)\,\mathbf{v}_{pcc}^{s},\qquad
    \mathbf{R}(\theta)=\begin{bmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{bmatrix} \]</div>
  <p>En el código (cap. 8) esto son exactamente las líneas que rotan <code class="inl">vpcc_s</code> a
  <code class="inl">vpcc_c</code> con \( \cos\delta,\sin\delta \), y la salida que rota
  <code class="inl">iL2</code> de vuelta al marco \( s \).</p>
</section>

<section id="estados">
  <h2 class="sec">6 · Designación de los 15 estados</h2>
  <p class="lead">Cuáles son, de dónde sale cada uno y por qué es estado.</p>
  <p>Un <b>estado</b> es una variable cuya derivada aparece en el modelo: algo que "tiene memoria"
  (almacena energía o integra). Cada elemento que almacena energía (inductor, condensador) aporta un
  estado por eje; cada integrador del control aporta otro; el ángulo y las potencias filtradas son
  estados de la sincronización. Así se llega a 15:</p>
  <table>
    <tr><th>#</th><th>Estado</th><th>Por qué es estado</th><th>Ecuación de su derivada</th></tr>
    <tr><td>0,1</td><td><code>iL1d, iL1q</code></td><td>corriente en \( L_1 \): la inductancia integra tensión</td><td>\( L_1\dot{\mathbf{i}}_{L1}=\mathbf{v}_i-\mathbf{v}_C-R_1\mathbf{i}_{L1}+\omega L_1\mathbf{J}\mathbf{i}_{L1} \)</td></tr>
    <tr><td>2,3</td><td><code>vcd, vcq</code></td><td>tensión en \( C_f \): el condensador integra corriente</td><td>\( C_f\dot{\mathbf{v}}_C=\mathbf{i}_{L1}-\mathbf{i}_{L2}+\omega C_f\mathbf{J}\mathbf{v}_C \)</td></tr>
    <tr><td>4,5</td><td><code>iL2d, iL2q</code></td><td>corriente en \( L_2 \) (= corriente a red \( i_g \))</td><td>\( L_2\dot{\mathbf{i}}_{L2}=\mathbf{v}_C-\mathbf{v}_{pcc}-R_2\mathbf{i}_{L2}+\omega L_2\mathbf{J}\mathbf{i}_{L2} \)</td></tr>
    <tr><td>6</td><td><code>delta</code></td><td>ángulo control−red: integra la diferencia de frecuencia</td><td>\( \dot\delta=\omega-\omega_0 \)</td></tr>
    <tr><td>7,8</td><td><code>Pm, Qm</code></td><td>potencia filtrada: el filtro paso-bajo tiene memoria</td><td>\( \dot P_m=\omega_f(P-P_m) \)</td></tr>
    <tr><td>9,10</td><td><code>xvd, xvq</code></td><td>integradores del PI de tensión</td><td>\( \dot{\mathbf{x}}_v=\mathbf{e}_v \)</td></tr>
    <tr><td>11,12</td><td><code>xid, xiq</code></td><td>integradores del PI de corriente</td><td>\( \dot{\mathbf{x}}_i=\mathbf{e}_i \)</td></tr>
    <tr><td>13,14</td><td><code>iL2d_lp, iL2q_lp</code></td><td>filtro paso-bajo de la R virtual transitoria</td><td>\( \dot{\mathbf{x}}=\omega_{ht}(\mathbf{i}_{L2}-\mathbf{x}) \)</td></tr>
  </table>
  <p>Estos nombres son literalmente la lista <code class="inl">STATE_NAMES</code> del código
  (<span class="file">model.py</span>), y el orden es el del vector de estado. El término
  \( \mathbf{J}=\left[\begin{smallmatrix}0&-1\\1&0\end{smallmatrix}\right] \) es el acoplamiento cruzado
  d↔q que surge al derivar en un marco giratorio.</p>
  <div class="note"><b>Nota de honestidad técnica:</b> el docstring de <span class="file">model.py</span>
  dice "Estados (13)" por un comentario antiguo, pero la lista real <code class="inl">STATE_NAMES</code>
  tiene <b>15</b> entradas (se añadieron los dos estados del filtro de la R virtual transitoria) y
  <code class="inl">NX = len(STATE_NAMES) = 15</code>. La verdad la fija el código, no el comentario: la
  Fase&nbsp;1 devuelve 15 autovalores, confirmándolo.</div>
  <figure style="margin:18px auto;max-width:660px;text-align:center"><img src="results/matriz_A.png" alt="estructura de la matriz de estado A">
    <figcaption>Estructura de la matriz de estado \( A \) (15×15): se ven los bloques acoplados —el LCL (6 estados),
    el droop/VSM, los integradores PI de tensión y corriente, y el filtro de la \( R \) virtual— y el
    acoplamiento cruzado d↔q (sub-bloques 2×2 antidiagonales). Generada con <span class="file">figuras_modelo.py</span>.</figcaption></figure>
</section>

<section id="parametros">
  <h2 class="sec">7 · Parámetros del sistema <span class="file">params.py</span></h2>
  <p class="lead">Una sola fuente de verdad; las ganancias se derivan de los anchos de banda.</p>
  <p>Todos los parámetros viven en una <code class="inl">@dataclass</code>. Lo nominal y el filtro son
  datos; las ganancias de control se <b>calculan</b> en <code class="inl">__post_init__</code> a partir
  de los anchos de banda objetivo, de modo que cambiar \( f_{ci} \) o \( f_{cv} \) re-sintoniza los PI
  automáticamente. La sintonía es por <b>cancelación de polo de planta</b> (IMC): para el lazo de
  corriente, \( K_{p,i}=L_1\omega_{ci} \) y \( K_{i,i}=R_1\omega_{ci} \), de modo que el cero del PI
  cancela el polo \( R_1/L_1 \) del inductor y el lazo cerrado queda como un primer orden de ancho de
  banda \( \omega_{ci} \). Análogamente \( K_{p,v}=C_f\omega_{cv} \) para el lazo de tensión.</p>
""" + embed("params.py",
  "El convenio de amplitud (pico de fase, V0 = Vll·√(2/3) = 326.6 V) fija el factor 1.5 de la potencia "
  "trifásica. mp y nq son las pendientes de droop; Jvsm y Dvsm derivan de la constante de inercia H.") + r"""
</section>
""")

S.append(r"""
<section id="modelomat">
  <h2 class="sec">8 · Modelo matemático no lineal <span class="file">model.py</span></h2>
  <p class="lead">El campo vectorial \( f(\mathbf{x},\mathbf{u}) \): física y control en 15 ecuaciones.</p>
  <p>El método <code class="inl">f(x,u)</code> evalúa \( \dot{\mathbf{x}} \) para un estado y una
  entrada. Se lee de arriba abajo siguiendo la cascada: primero la <b>capa externa</b> (droop P-ω fija
  la frecuencia \( \omega \); potencia medida y filtrada), luego el <b>droop Q-V</b> con la impedancia
  virtual y la R transitoria que arman la referencia de tensión, después los <b>PI de tensión y de
  corriente</b> con sus desacoplos, el <b>amortiguamiento activo</b>, la <b>rotación</b> de la tensión
  de red por \( \delta \), y por último la <b>planta LCL</b>. Cada bloque corresponde a un grupo de
  estados de la tabla del cap.&nbsp;6.</p>
  <h4>Las tres ecuaciones de la planta LCL (en dq, marco \( c \))</h4>
  <div class="eq">
    \[ L_1\dot{\mathbf{i}}_{L1}=\mathbf{v}_i-\mathbf{v}_C-R_1\mathbf{i}_{L1}+\omega L_1\mathbf{J}\,\mathbf{i}_{L1} \]
    \[ C_f\dot{\mathbf{v}}_C=\mathbf{i}_{L1}-\mathbf{i}_{L2}+\omega C_f\mathbf{J}\,\mathbf{v}_C \]
    \[ L_2\dot{\mathbf{i}}_{L2}=\mathbf{v}_C-\mathbf{v}_{pcc}-R_2\mathbf{i}_{L2}+\omega L_2\mathbf{J}\,\mathbf{i}_{L2} \]
  </div>
  <h4>La potencia y el droop</h4>
  <div class="eq">
    \[ P=\tfrac{3}{2}(v_{cd}i_{L2d}+v_{cq}i_{L2q}),\quad Q=\tfrac{3}{2}(v_{cq}i_{L2d}-v_{cd}i_{L2q}) \]
    \[ \omega=\omega_0+m_p(P_\text{set}-P_m),\quad V_\text{ref}=V_0+n_q(Q_\text{set}-Q_m) \]
  </div>
""" + embed("model.py",
  "Estados, output (rota i_L2 al marco s por δ), equilibrium (fsolve con guess físico) y "
  "linearize (Jacobiano por diferencias centradas escaladas). Los flags de opts permiten apagar lazos "
  "para el diagnóstico del cap. 10.") + r"""
  <div class="note"><b>Detalle del código que importa:</b> la rotación
  <code class="inl">vpcc_cd = cd*vpcc_sd + sd*vpcc_sq</code> implementa
  \( \mathbf{R}(-\delta) \); la salida <code class="inl">output()</code> aplica \( \mathbf{R}(+\delta) \)
  para devolver la corriente al marco \( s \). La red Thévenin en serie aparece como
  <code class="inl">L2t = L2 + Lg</code>, <code class="inl">R2t = R2 + Rg</code>: con
  \( L_g=R_g=0 \) el puerto es rígido (Fases 1–2); con valores no nulos, red débil (Fase 3).</div>
</section>

<section id="equilibrio">
  <h2 class="sec">9 · Equilibrio y linealización</h2>
  <p class="lead">Cómo se halla \( \mathbf{x}_e \) y cómo se obtiene \( (A,B,C,D) \).</p>
  <h3>9.1 El punto de equilibrio</h3>
  <p>Antes de linealizar hay que resolver \( f(\mathbf{x}_e,\mathbf{u}_e)=0 \). El método
  <code class="inl">equilibrium()</code> construye una <b>estimación física</b> a partir de la consigna
  (corrientes que dan \( P_\text{set} \), tensión nominal, ángulo pequeño) y la refina con
  <code class="inl">fsolve</code> (tolerancia \( 10^{-12} \)). Un buen guess es clave: con uno arbitrario
  el solver puede no converger o caer en una solución no física. La Fase&nbsp;1 confirma residual
  \( \approx 9.7\times10^{-11} \) y \( P_\text{eq}=5000 \) W exactos.</p>
  <h3>9.2 La linealización por diferencias centradas</h3>
  <p>Cada columna de \( A \) es \( \partial f/\partial x_j \), aproximada perturbando el estado \( j \)
  arriba y abajo y dividiendo por \( 2\Delta x_j \). Las diferencias <b>centradas</b> dan error
  \( O(\Delta x^2) \) (no \( O(\Delta x) \)); el paso se <b>escala</b> con la magnitud del estado
  (<code class="inl">eps*max(1,|x|)</code>) porque corrientes de decenas de A y ángulos de fracciones de
  rad no admiten el mismo paso absoluto. La misma idea da \( B \) (perturbando \( u \)), \( C \) y
  \( D \) (perturbando la salida).</p>
  <h3>9.3 Validación previa obligatoria</h3>
  <p>Antes de creerse nada: (1) residual del equilibrio \( \approx 10^{-10} \); (2) signo de
  \( \partial P/\partial\delta>0 \) (físico: más ángulo → más potencia en línea inductiva); (3) la
  resonancia LCL aparece a ~1.1&nbsp;kHz. Las tres cuadran, luego el modelo es fiable.</p>

  <h3>9.4 Derivación de la sensibilidad potencia-ángulo</h3>
  <p>La ganancia del lazo de sincronización —y, por tanto, la raíz de la inestabilidad del primer
  diseño (cap. 10)— es \( \partial P/\partial\delta \). Para una fuente de tensión \( V \) detrás de una
  reactancia \( X \) conectada a una red \( E \), la potencia activa transmitida es la conocida ecuación
  de transferencia:</p>
  <div class="eq">\[ P=\frac{V\,E}{X}\sin\delta \quad\Longrightarrow\quad
     \frac{\partial P}{\partial\delta}=\frac{V\,E}{X}\cos\delta \;\xrightarrow[\delta\to0]{}\; \frac{V\,E}{X} \]</div>
  <p>Con \( V\approx E\approx V_0 \) y considerando la potencia trifásica (factor \( \tfrac32 \) en
  amplitud de pico), la sensibilidad en torno al punto de operación es del orden de
  \( \partial P/\partial\delta\sim 1.5\,V_0^2/X \). El término clave es \( 1/X \): si la reactancia de
  acoplamiento \( X \) es <b>pequeña</b>, la ganancia es <b>enorme</b>, el lazo de potencia cruza con
  poco margen de fase y el sistema tiende a la inestabilidad. La medición numérica sobre el modelo da
  \( \partial P/\partial\delta=+127 \) kW/rad (positivo y físico). Esta fórmula explica
  cuantitativamente por qué la <b>impedancia virtual inductiva</b> —que aumenta \( X \) por software— es
  la cura: reduce \( \partial P/\partial\delta \) y devuelve margen de fase al lazo, sin distorsionar el
  equilibrio (su caída cae en el eje q).</p>

  <div class="repolinks"><b>📚 En el repositorio:</b>
    <a href="../00%20-%20Repositorio/index.html#equilibrio-fsolve">Equilibrio (fsolve)</a> ·
    <a href="../00%20-%20Repositorio/index.html#linealizacion-numerica">Linealización numérica</a> ·
    <a href="../00%20-%20Repositorio/index.html#analisis-modal">Análisis modal</a> ·
    <a href="../00%20-%20Repositorio/index.html#ecuacion-oscilacion">Ecuación de oscilación</a></div>
</section>
""")

# ---------------------------------------------------------------- PARTE III
S.append(r"""<div class="part">Parte III · Desarrollo — las cinco fases</div>

<section id="f1">
  <div class="phase-h"><div class="phase-n" style="background:var(--f1)">1</div>
    <h2 class="sec" style="border:0;margin:0">Fase 1 · Modelo y estabilidad</h2></div>
  <p class="lead">Equilibrio, linealización, autovalores y mapa de polos.</p>
  <h3>1.1 Objetivo y método</h3>
  <p>Demostrar que el diseño es estable e identificar sus modos. El script construye el modelo, resuelve
  el equilibrio, linealiza, calcula los autovalores ordenados de menos a más estable, y dibuja el mapa
  de polos. Para cada autovalor imprime frecuencia \( f=|\mathrm{Im}|/2\pi \) y amortiguamiento
  \( \zeta=-\mathrm{Re}/|\lambda| \).</p>
""" + embed("main_phase1.py") + r"""
  <h3>1.2 Resultados reales</h3>
""" + console(R_PHASE1) + r"""
  <div class="grid2">
    <figure><img src="results/polos_fase1.png" alt="mapa de polos">
      <figcaption>Mapa de polos en lazo cerrado: los 15 autovalores, todos en el semiplano izquierdo.</figcaption></figure>
    <div>
      <h3>1.3 Lectura de los modos</h3>
      <p>El espectro se separa en familias, confirmando la separación temporal de la cascada:</p>
      <ul class="tight">
        <li><b>Resonancia LCL</b> a 1104.7 y 1089.4 Hz (\( \zeta\approx 0.13\text{–}0.17 \)): el filtro,
        amortiguado por \( K_\text{ad} \).</li>
        <li><b>Lazo de corriente</b> a 77.5 Hz (\( \zeta=0.998 \), casi crítico).</li>
        <li>Modos reales rápidos a −50, −87, −100 (lazo de tensión e integradores).</li>
        <li><b>Modo de potencia</b> a <b>3.3 Hz con \( \zeta=0.40 \)</b>: el más lento y el crítico, el
        equivalente al modo electromecánico de una máquina síncrona.</li>
      </ul>
      <p>Equilibrio: \( P=5000 \) W exactos, \( Q=-554 \) var (físico: lo consume la impedancia virtual y
      el filtro), \( \delta=5.11° \), \( |v_C|=326.7 \) V ≈ nominal. <span class="pill ok">ESTABLE</span>
      \( \max\mathrm{Re}=-8.32 \).</p>
    </div>
  </div>
  <div class="repolinks"><b>📚 En el repositorio:</b>
    <a href="../00%20-%20Repositorio/index.html#droop-control">Droop</a> ·
    <a href="../00%20-%20Repositorio/index.html#analisis-modal">Análisis modal</a> ·
    <a href="../00%20-%20Repositorio/index.html#ecuacion-oscilacion">Ecuación de oscilación</a></div>
</section>

<section id="f2">
  <div class="phase-h"><div class="phase-n" style="background:var(--f2)">2</div>
    <h2 class="sec" style="border:0;margin:0">Fase 2 · Impedancia de salida Z(s)</h2></div>
  <p class="lead">La huella dinámica del inversor vista desde la red.</p>
  <h3>2.1 Cómo se calcula</h3>
  <p>Del modelo linealizado, la respuesta en frecuencia es
  \( G(s)=C(sI-A)^{-1}B+D=\partial \mathbf{i}_g/\partial \mathbf{v}_{pcc} \). Por el convenio de signos
  (corriente saliente hacia la red), la admitancia de salida es \( Y=-G \) y la impedancia
  \( Z=Y^{-1} \), una matriz 2×2 en dq. El módulo <span class="file">impedance.py</span> lo implementa;
  nótese el uso de <code class="inl">np.linalg.solve(sI-A, B)</code> en vez de invertir \( (sI-A) \)
  explícitamente (más estable y rápido).</p>
""" + embed("impedance.py") + r"""
  <p>El driver de la fase barre 0.1&nbsp;Hz–5&nbsp;kHz y dibuja las cuatro componentes
  \( Z_{dd},Z_{dq},Z_{qd},Z_{qq} \) en Bode, marcando el modo de potencia y la resonancia LCL:</p>
""" + embed("main_phase2.py") + r"""
  <h3>2.2 Resultados reales</h3>
""" + console(R_PHASE2) + r"""
  <div class="grid2">
    <figure><img src="results/impedancia_fase2.png" alt="impedancia dq">
      <figcaption>Bode de las 4 componentes de Z_dq.</figcaption></figure>
    <div>
      <p>La impedancia es <b>inductiva en banda media</b>: la fase de \( Z_{dd} \) y \( Z_{qq} \) está
      entre +47° (50 Hz) y +59° (10 Hz), la firma de una fuente de tensión detrás de impedancia
      (grid-forming). El módulo crece con la frecuencia en esa banda (\( |Z|=16.7 \) Ω a 50 Hz), como
      una inductancia. Cerca de la resonancia LCL (~1.1 kHz) la fase cambia de signo. El pico del modo
      de potencia (3.3 Hz) <b>no</b> es agudo, gracias a \( \zeta=0.40 \): un pico agudo aquí avisaría
      de riesgo de oscilación con la red.</p>
      <h3>2.3 Por qué matriz 2×2</h3>
      <p>Los términos fuera de la diagonal (\( Z_{dq},Z_{qd} \)) miden el acoplamiento d↔q; no son
      despreciables en un GFM. Ignorarlos daría una predicción de estabilidad errónea: por eso la
      Fase&nbsp;3 usa Nyquist <b>generalizado</b> (autovalores de una matriz), no SISO.</p>
    </div>
  </div>
  <div class="repolinks"><b>📚 En el repositorio:</b>
    <a href="../00%20-%20Repositorio/index.html#respuesta-frecuencia-ss">Respuesta en frecuencia (SS)</a> ·
    <a href="../00%20-%20Repositorio/index.html#impedancia-salida-estabilidad">Estabilidad por impedancia</a></div>
</section>

<section id="f3">
  <div class="phase-h"><div class="phase-n" style="background:var(--f3)">3</div>
    <h2 class="sec" style="border:0;margin:0">Fase 3 · Estabilidad en red débil</h2></div>
  <p class="lead">Nyquist generalizado, validado contra el modelo acoplado.</p>
  <h3>3.1 La red Thévenin <span class="file">grid.py</span></h3>
  <p>La red se parametriza por SCR y X/R. De \( \mathrm{SCR}=V_{ll}^2/(|Z_g|S_n) \) se obtiene
  \( |Z_g| \), y de X/R se reparten \( R_g \) y \( L_g \). Su impedancia en dq es la de un inductor con
  acoplamiento cruzado \( \omega_0 L_g \):</p>
""" + embed("grid.py") + r"""
  <h3>3.2 Las dos vías y el código</h3>
  <p>El driver usa un control <b>agresivo</b> (droop alto, sin amortiguamiento transitorio) que sí
  pierde estabilidad, para ilustrar el criterio. Calcula el SCR crítico por <b>(A)</b> bisección sobre
  el \( \max\mathrm{Re} \) del modelo acoplado, y por <b>(B)</b> el mínimo de
  \( |\det(I+Z_\text{red}Y_\text{inv})| \) (Nyquist de impedancia). Ambos deben coincidir.</p>
""" + embed("main_phase3.py") + r"""
  <h3>3.3 Resultados reales</h3>
""" + console(R_PHASE3) + r"""
  <div class="grid2">
    <figure><img src="results/nyquist_fase3.png" alt="nyquist generalizado">
      <figcaption>Nyquist generalizado: al crecer el SCR el locus envuelve −1.</figcaption></figure>
    <div>
      <table>
        <tr><th>Método</th><th>SCR crítico</th></tr>
        <tr><td>(A) Autovalores del modelo acoplado</td><td><b>3.347</b></td></tr>
        <tr><td>(B) Nyquist de Z_red·Y_inv</td><td><b>3.390</b></td></tr>
        <tr><td colspan="2">Diferencia 0.043 → <span class="pill ok">1.3 %</span></td></tr>
      </table>
      <div class="def"><b>Hallazgo:</b> el GFM bien amortiguado es estable en <b>todo</b> el rango de
      SCR. El caso crítico solo aparece con control <b>agresivo</b>, y es en red <b>fuerte</b>
      (SCR&gt;3.3), lo <b>opuesto</b> al grid-following. La red débil no molesta a un GFM porque no
      depende de PLL; lo que lo desestabiliza es una red fuerte con \( \partial P/\partial\delta \) alto.</div>
    </div>
  </div>
  <div class="repolinks"><b>📚 En el repositorio:</b>
    <a href="../00%20-%20Repositorio/index.html#nyquist-generalizado">Nyquist generalizado</a> ·
    <a href="../00%20-%20Repositorio/index.html#red-thevenin-scr">Red Thévenin / SCR</a> ·
    <a href="../00%20-%20Repositorio/index.html#grid-forming-vs-following">GFM vs GFL</a></div>
</section>

<section id="f4">
  <div class="phase-h"><div class="phase-n" style="background:var(--f4)">4</div>
    <h2 class="sec" style="border:0;margin:0">Fase 4 · Validación</h2></div>
  <p class="lead">Medir la impedancia como en PLECS/hardware, y justificar el promediado.</p>
  <h3>4.1 Medición por inyección <span class="file">inject.py</span></h3>
  <p>Esta es la técnica que se programa en un banco real: inyectar una perturbación senoidal de tensión
  a frecuencia \( f_p \), primero en d y luego en q (dos experimentos, por ser MIMO 2×2), simular hasta
  régimen permanente, y extraer los fasores por <b>demodulación</b> (correlación con sin/cos sobre
  periodos enteros). Con las dos columnas se monta \( I=G\,V \) y se despeja \( G=I\,V^{-1} \),
  \( Y=-G \), \( Z=Y^{-1} \). La "planta" aquí es el modelo no lineal (<span class="file">simulate.py</span>),
  así que comparar con el \( Z \) analítico valida la linealización.</p>
""" + embed("inject.py") + r"""
  <h3>4.2 El driver de validación</h3>
""" + embed("main_phase4.py") + r"""
  <h3>4.3 Resultados reales</h3>
""" + console(R_PHASE4) + r"""
  <h3>4.4 Justificación del promediado <span class="file">switched.py</span></h3>
  <p>Todo el proyecto usa el modelo promediado (tensión de puente continua). Para justificarlo, se
  compara la tensión real <b>conmutada</b> (PWM a 10 kHz, portadora triangular) con la <b>promediada</b>
  integrando ambas sobre el mismo filtro L-C:</p>
""" + embed("switched.py") + r"""
""" + console(R_SWITCHED) + r"""
  <div class="grid2">
    <figure><img src="results/fase4_validacion.png" alt="validacion impedancia">
      <figcaption>4a — Impedancia medida (inyección) vs analítica: error medio 0.21 %.</figcaption></figure>
    <figure><img src="results/fase4b_averaging.png" alt="promediado vs conmutado">
      <figcaption>4b — Tensión conmutada (PWM) vs promediada: diferencia RMS 0.67 %.</figcaption></figure>
  </div>
  <div class="warn-box"><b>Régimen de validez:</b> el barrido de amplitud (1→80 V) da error plano
  (~0.07 %): la impedancia medida no depende de la amplitud → régimen lineal confirmado. Cuando entra
  la saturación de corriente, el concepto de impedancia lineal deja de aplicar → gran señal (Fase 5).</div>
  <div class="repolinks"><b>📚 En el repositorio:</b>
    <a href="../00%20-%20Repositorio/index.html#medicion-impedancia-inyeccion">Medición por inyección</a> ·
    <a href="../00%20-%20Repositorio/index.html#modelo-promediado">Modelo promediado vs conmutado</a> ·
    <a href="../00%20-%20Repositorio/index.html#fft-analisis-espectral">FFT / espectral</a></div>
</section>

<section id="f5">
  <div class="phase-h"><div class="phase-n" style="background:var(--f5)">5</div>
    <h2 class="sec" style="border:0;margin:0">Fase 5 · Gran señal: VSM y current limiting</h2></div>
  <p class="lead">Lo que la impedancia lineal no captura: inercia y saturación.</p>
  <h3>5.1 El simulador temporal <span class="file">simulate.py</span></h3>
  <p>Reutiliza la planta y los lazos del modelo, pero (1) la capa externa puede ser droop o <b>VSM</b>
  (ecuación de swing, con \( \omega \) como estado 15), y (2) añade <b>current limiting</b>: si la
  magnitud de la referencia de corriente supera \( I_\text{max} \), se escala y se congelan los
  integradores de tensión (anti-windup). Integra con LSODA (stiff). Es un modelo de <b>16 estados</b>
  (los 15 + \( \omega \)).</p>
""" + embed("simulate.py") + r"""
  <h3>5.2 El driver: escalón de potencia y falta</h3>
""" + embed("main_phase5.py") + r"""
  <h3>5.3 Resultados reales</h3>
""" + console(R_PHASE5) + r"""
  <div class="grid2">
    <figure><img src="results/fase5_inercia.png" alt="droop vs vsm">
      <figcaption>Escalón 5→9 kW: el droop responde de golpe; el VSM (H=4s) suaviza el RoCoF.</figcaption></figure>
    <figure><img src="results/fase5_falta.png" alt="current limiting">
      <figcaption>Falta (hueco 30%): sin límite 4.76 pu; con límite 1.51 pu.</figcaption></figure>
  </div>
  <div class="grid2">
    <div class="card"><h3>Droop vs VSM</h3>
      <p>El VSM usa \( J\dot\omega=(P_\text{set}-P)/\omega_0-D(\omega-\omega_0) \): convierte la
      frecuencia en un estado con inercia, limitando el RoCoF como una máquina real. El droop la fija
      algebraicamente (sin inercia).</p></div>
    <div class="card"><h3>Current limiting</h3>
      <p>Sin límite, la falta lleva la corriente a <b>4.76 pu</b> (97.1 A, destruiría los
      semiconductores). Saturando a \( I_\text{max}=1.5 \) pu (30.6 A) con anti-windup, queda en
      <b>1.51 pu</b>. \( I_n=20.4 \) A.</p></div>
  </div>
  <div class="repolinks"><b>📚 En el repositorio:</b>
    <a href="../00%20-%20Repositorio/index.html#vsm-inercia">VSM / inercia</a> ·
    <a href="../00%20-%20Repositorio/index.html#current-limiting">Current limiting</a> ·
    <a href="../00%20-%20Repositorio/index.html#anti-windup">Anti-windup</a> ·
    <a href="../00%20-%20Repositorio/index.html#integracion-edos-stiff">EDOs stiff</a></div>
</section>
""")

# ---------------------------------------------------------------- PARTE IV
S.append(r"""<div class="part">Parte IV · Diagnóstico, lecciones y cierre</div>

<section id="iter">
  <h2 class="sec">10 · El proceso de iteración (lo que más enseña)</h2>
  <p class="lead">El primer diseño salió inestable. Así se diagnosticó y corrigió.</p>
  <div class="note"><b>Principio guía:</b> si reducir mucho una ganancia (×20) <b>no</b> estabiliza, el
  problema no es de ajuste: es <b>estructural</b> (signo, acoplamiento, realimentación positiva). Cada
  vez que un barrido mostraba insensibilidad a la ganancia, se dejaba de afinar números y se buscaba un
  error estructural.</div>

  <h3>10.1 La herramienta de diagnóstico <span class="file">diag_sweep.py</span></h3>
  <p>Un barrido que evalúa el \( \max\mathrm{Re} \) bajo distintas variaciones de parámetros y flags,
  para distinguir "ajuste" de "estructura". Es el código con el que se localizó la causa raíz:</p>
""" + embed("diag_sweep.py") + r"""
  <h3>10.2 Resultados reales del barrido</h3>
""" + console(R_DIAG) + r"""
  <p>Lectura clave: variar el droop P a la mitad o el droop Q a cero <b>apenas</b> mueve el
  \( \max\mathrm{Re} \) (de −8.32 a −7.86): el modo no es sensible a esas ganancias → su (in)estabilidad
  es estructural. En cambio, subir el lazo de tensión ×3 (<code class="inl">f_cv=180</code>) lleva el
  sistema a <b>+1.21 (INESTABLE)</b>: confirma que forzar el lazo intermedio desestabiliza, coherente
  con el diagnóstico histórico.</p>

  <h3>10.3 Cronología real del debugging</h3>
  <div style="margin-top:16px">
    <div class="step bad"><h4>① Diseño inicial — INESTABLE</h4>
      \( \max\mathrm{Re}=+37 \), modo a 6 Hz con \( \zeta=-0.71 \). Participación: \( P_m,Q_m \) → lazo
      de potencia.</div>
    <div class="step warn"><h4>② Los barridos no estabilizan</h4>
      Variar droop y filtro casi no mueve el modo; subir el lazo de tensión lo empeora. → estructural.</div>
    <div class="step ok"><h4>③ Aislamiento → causa #1</h4>
      Con droops=0 pero <b>feedforward de carga activo</b> (flag <code class="inl">ff_load</code>),
      \( \max\mathrm{Re}=+14 \): el feedforward es inestable por sí solo. Se elimina → +1.26.</div>
    <div class="step warn"><h4>④ Modo Q residual (0.4 Hz)</h4>
      Insensible al droop Q (×5 apenas cambia) → otra vez estructural.</div>
    <div class="step"><h4>⑤ Diagnóstico físico</h4>
      \( \partial P/\partial\delta=+127 \) kW/rad (correcto en signo), pero el sistema real es inestable
      → la inestabilidad está en la <b>fase dinámica</b>, no en la ganancia DC. La reactancia de
      acoplamiento es minúscula → \( \partial P/\partial\delta\approx 1.5V^2/X \) enorme.</div>
    <div class="step bad"><h4>⑥ Bode del lazo de potencia</h4>
      Margen de fase <b>−86°</b>. Cura canónica: impedancia virtual.</div>
    <div class="step ok"><h4>⑦ Inductancia virtual → causa #2</h4>
      \( X_v\approx 0.16 \) pu baja \( \partial P/\partial\delta \) y estabiliza sin distorsionar el
      equilibrio. La resistiva pelearía con el droop Q (dispara \( Q_\text{eq} \)).</div>
    <div class="step ok"><h4>⑧ Amortiguamiento: ζ 0.17 → 0.40</h4>
      La resistencia virtual transitoria (paso-alto, cero en DC) sube \( \zeta \) sin tocar el
      equilibrio.</div>
    <div class="step ok"><h4>⑨ Resultado final — ESTABLE</h4>
      \( \max\mathrm{Re}=-8.32 \), modo de potencia \( \zeta=0.40 \), equilibrio físico correcto.</div>
  </div>
  <div class="repolinks"><b>📚 En el repositorio:</b>
    <a href="../00%20-%20Repositorio/index.html#impedancia-virtual">Impedancia virtual</a> ·
    <a href="../00%20-%20Repositorio/index.html#margenes-estabilidad">Márgenes de estabilidad</a> ·
    <a href="../00%20-%20Repositorio/index.html#robustez-parametrica">Robustez paramétrica</a></div>
</section>

<section id="discusion">
  <h2 class="sec">11 · Discusión global</h2>
  <p class="lead">Síntesis crítica de los resultados, contraste con lo esperado y limitaciones del estudio.</p>

  <h3>11.1 Coherencia interna de los resultados</h3>
  <p>Las cinco fases no son compartimentos estancos: sus resultados se refuerzan mutuamente, lo que da
  solidez al conjunto. El modo de potencia identificado en la Fase&nbsp;1 (3.3&nbsp;Hz, \( \zeta=0.40 \))
  es el mismo que la Fase&nbsp;2 muestra como un pico suave en la impedancia, el que la Fase&nbsp;3
  gobierna la frontera de estabilidad con la red, y el que la Fase&nbsp;5 excita el escalón de potencia.
  La resonancia LCL (~1.1&nbsp;kHz) aparece consistentemente como autovalor (Fase&nbsp;1), como cambio
  de signo de fase en \( \mathbf{Z}_{dq} \) (Fase&nbsp;2) y como pico de \( |Z_\text{fuente}| \) implícito
  en el amortiguamiento activo. Esta trazabilidad de un mismo fenómeno físico a través de herramientas
  distintas es, en sí misma, una verificación.</p>

  <h3>11.2 Contraste con lo esperado y con la literatura</h3>
  <ul class="tight">
    <li>La <b>firma inductiva</b> de la impedancia (fase +47°…+59°) coincide con lo esperado de una
    fuente de tensión detrás de impedancia, es decir, el comportamiento tipo máquina síncrona que la
    literatura atribuye al grid-forming [7],[8].</li>
    <li>El hallazgo de que el GFM bien amortiguado es <b>más vulnerable en red fuerte</b> que en débil
    —opuesto al grid-following— es consistente con el mecanismo \( \partial P/\partial\delta\propto V^2/X \):
    a menor \( X \) (red fuerte), mayor ganancia del lazo de sincronización y menor margen de fase. Esto
    sitúa al GFM y al GFL como complementarios, como recoge el proyecto 02.</li>
    <li>El acuerdo entre el SCR crítico por autovalores (3.347) y por Nyquist de impedancia (3.390),
    del 1.3&nbsp;%, confirma que el método de impedancia [4] reproduce la "verdad" del modelo acoplado.</li>
  </ul>

  <h3>11.3 Limitaciones del estudio</h3>
  <ul class="tight">
    <li><b>Modelo promediado.</b> Se trabaja con tensión de puente promediada; el rizado de conmutación
    se justifica despreciable (0.67&nbsp;%, Fase&nbsp;4b) pero no se modelan armónicos de conmutación,
    tiempos muertos ni no idealidades de los IGBT. La validación en PLECS (conmutado) queda pendiente.</li>
    <li><b>Condiciones equilibradas.</b> Todo el análisis asume red trifásica equilibrada; las faltas
    asimétricas (componentes inversa y homopolar) y su efecto sobre el current limiting no se abordan.</li>
    <li><b>Linealización local.</b> La impedancia y los modos son válidos en torno a un punto de
    operación (5&nbsp;kW); un barrido completo del plano P-Q quedaría fuera del alcance.</li>
    <li><b>Parámetros nominales.</b> No se realiza un análisis de incertidumbre/Montecarlo sobre la
    dispersión de \( L,C,R \); la robustez se explora de forma puntual en los barridos de diagnóstico.</li>
  </ul>
  <div class="note">Estas limitaciones no invalidan las conclusiones en su régimen de validez (pequeña
  señal, equilibrado, punto nominal); delimitan dónde el modelo deja de aplicar y orientan las líneas
  futuras (cap. 13).</div>
</section>

<section id="lecciones">
  <h2 class="sec">12 · Lecciones aprendidas</h2>
  <div class="grid2">
    <div class="card"><h3>Diagnóstico</h3>
      <ul class="tight">
        <li><b>Ganancia vs estructura:</b> si bajar una ganancia ×20 no estabiliza, el fallo es
        estructural.</li>
        <li><b>Aísla lazos</b> (flags droop=0, ff=0) para localizar la fuente antes de tocar nada.</li>
        <li><b>Mide sensibilidades físicas</b> (\( \partial P/\partial\delta \)) para separar error de
        modelo de inestabilidad real.</li>
      </ul></div>
    <div class="card"><h3>Control de GFM</h3>
      <ul class="tight">
        <li>Un feedforward "que mejora el rechazo" puede desestabilizar — verifícalo en lazo cerrado.</li>
        <li>Impedancia virtual <b>inductiva ≠ resistiva</b>: una baja la ganancia del lazo, la otra
        interfiere con el droop Q.</li>
        <li><b>Ganancia DC correcta ≠ estable:</b> decide la fase a la frecuencia de cruce (Bode).</li>
        <li>El droop tiene amortiguamiento limitado; el VSM da control directo (D explícito).</li>
      </ul></div>
  </div>
  <div class="card"><h3>Método</h3>
    <ul class="tight">
      <li>La linealización numérica escala a no linealidades sin re-hacer álgebra.</li>
      <li>El análisis lineal vale <b>hasta</b> que una protección/saturación entra en juego.</li>
      <li><b>Valida por dos vías:</b> la concordancia (acoplado↔impedancia, analítico↔inyección) es lo
      que da confianza al método barato.</li>
    </ul></div>
</section>

<section id="concl">
  <h2 class="sec">13 · Conclusiones, aportaciones y líneas futuras</h2>
  <p class="lead">Cierre formal: qué se concluye, qué se aporta y qué queda abierto.</p>

  <h3>13.1 Conclusiones generales</h3>
  <p>Se ha completado el ciclo íntegro de ingeniería de un inversor grid-forming, desde la formulación
  física hasta la validación, con las siguientes conclusiones:</p>
  <ol class="tight">
    <li>El modelo no lineal de 15 estados en \( dq \), linealizado numéricamente, reproduce el
    equilibrio físico (\( P=5000 \) W, residual \( \sim10^{-10} \)) y un espectro de modos coherente con
    la física esperada (resonancia LCL a ~1.1&nbsp;kHz, modo de potencia a 3.3&nbsp;Hz).</li>
    <li>El diseño final es <b>estable y bien amortiguado</b> (\( \max\mathrm{Re}=-8.32 \),
    \( \zeta=0.40 \) en el modo crítico), gracias a la combinación de impedancia virtual inductiva y
    resistencia virtual transitoria.</li>
    <li>La <b>impedancia de salida</b> tiene firma inductiva (fuente de tensión tras impedancia) y
    permite, vía Nyquist generalizado, predecir el SCR crítico con un error del 1.3&nbsp;% frente al
    modelo acoplado.</li>
    <li>El modelo lineal y el promediado quedan <b>validados</b>: 0.21&nbsp;% por inyección de
    perturbación, 0.67&nbsp;% frente al modelo conmutado.</li>
    <li>El análisis de gran señal cuantifica el papel de la inercia virtual (RoCoF) y de la limitación de
    corriente (de 4.76 a 1.51&nbsp;pu bajo falta), fenómenos fuera del alcance del análisis lineal.</li>
  </ol>

  <h3>13.2 Aportaciones</h3>
  <ol class="tight">
    <li><b>Integración reproducible de extremo a extremo</b> del flujo modelado→impedancia→estabilidad→
    validación→gran señal sobre un único caso, con código abierto y resultados regenerables.</li>
    <li><b>Verificación cruzada sistemática</b> de cada resultado por dos vías independientes
    (autovalores↔Nyquist de impedancia; analítico↔inyección; promediado↔conmutado).</li>
    <li><b>Documentación del proceso de diagnóstico</b> de la inestabilidad inicial, con la herramienta de
    barrido y el principio "ganancia vs estructura", de alto valor didáctico y transferible.</li>
    <li><b>Material docente</b> trazable al repositorio de conceptos, que convierte el proyecto en un
    recurso de aprendizaje reutilizable.</li>
  </ol>

  <h3>13.3 Limitaciones</h3>
  <p>Resumidas en el cap.&nbsp;11.3: modelo promediado (sin conmutación real), condiciones equilibradas
  (sin faltas asimétricas), linealización en un punto de operación, y parámetros nominales (sin análisis
  de incertidumbre). Acotan el régimen de validez sin invalidar las conclusiones dentro de él.</p>

  <h3>13.4 Líneas futuras</h3>
  <ul class="tight">
    <li><b>Validación en PLECS</b>: montar el modelo conmutado (IGBT, PWM) y repetir las Fases 2–4 sobre
    la planta realista, cerrando el lazo Python↔PLECS.</li>
    <li><b>Faltas asimétricas</b>: extender el current limiting con componentes simétricas y estudiar la
    recuperación a modo formador tras el despeje.</li>
    <li><b>Robustez</b>: análisis de sensibilidad/Montecarlo sobre la dispersión de parámetros del filtro
    y del control.</li>
    <li><b>Otras arquitecturas</b>: control predictivo de conjunto finito (FCS-MPC) y convertidor
    multinivel modular (MMC).</li>
  </ul>
</section>
""")

S.append(r"""
<section id="biblio">
  <h2 class="sec">Bibliografía</h2>
  <p class="lead">Referencias de fundamento (selección representativa del estado del arte).</p>
  <table>
    <tr><td>[1]</td><td>M. C. Chandorkar, D. M. Divan, R. Adapa, "Control of parallel connected inverters
      in standalone AC supply systems," <i>IEEE Trans. Ind. Appl.</i>, vol. 29, no. 1, 1993.</td></tr>
    <tr><td>[2]</td><td>Q.-C. Zhong, G. Weiss, "Synchronverters: Inverters that mimic synchronous
      generators," <i>IEEE Trans. Ind. Electron.</i>, vol. 58, no. 4, 2011.</td></tr>
    <tr><td>[3]</td><td>J. He, Y. W. Li, "Analysis, design, and implementation of virtual impedance for
      power electronics interfaced distributed generation," <i>IEEE Trans. Ind. Appl.</i>, vol. 47,
      no. 6, 2011.</td></tr>
    <tr><td>[4]</td><td>J. Sun, "Impedance-based stability criterion for grid-connected inverters,"
      <i>IEEE Trans. Power Electron.</i>, vol. 26, no. 11, 2011.</td></tr>
    <tr><td>[5]</td><td>X. Wang, F. Blaabjerg, "Harmonic stability in power electronic-based power
      systems: concept, modeling, and analysis," <i>IEEE Trans. Smart Grid</i>, vol. 10, no. 3, 2019.</td></tr>
    <tr><td>[6]</td><td>B. Wen et al., "Analysis of D-Q small-signal impedance of grid-tied inverters,"
      <i>IEEE Trans. Power Electron.</i>, vol. 31, no. 1, 2016.</td></tr>
    <tr><td>[7]</td><td>R. H. Lasseter, Z. Chen, D. Pattabiraman, "Grid-forming inverters: a critical
      asset for the power grid," <i>IEEE J. Emerg. Sel. Topics Power Electron.</i>, vol. 8, no. 2, 2020.</td></tr>
    <tr><td>[8]</td><td>D. B. Rathnayake et al., "Grid forming inverter modeling, control, and
      applications," <i>IEEE Access</i>, vol. 9, 2021.</td></tr>
    <tr><td>[9]</td><td>R. D. Middlebrook, "Input filter considerations in design and application of
      switching regulators," <i>IEEE IAS Annual Meeting</i>, 1976.</td></tr>
    <tr><td>[10]</td><td>P. Kundur, <i>Power System Stability and Control</i>. McGraw-Hill, 1994
      (análisis modal, factores de participación, ecuación de oscilación).</td></tr>
  </table>
  <p class="small">Referencias de fundamento conceptual; los desarrollos numéricos y el código son
  propios de este proyecto. Cada concepto está además desarrollado en el
  <a href="../00%20-%20Repositorio/index.html">repositorio de conocimiento</a>.</p>
</section>
""")

# ---------------------------------------------------------------- APENDICES
S.append(r"""<div class="part">Apéndices</div>

<section id="apA">
  <h2 class="sec">Apéndice A · Parámetros completos</h2>
  <div class="grid2">
    <div>
      <h3>A.1 Nominales y base</h3>
      <table>
        <tr><th>Parámetro</th><th>Valor</th></tr>
        <tr><td>\( S_n \)</td><td>10 kVA</td></tr>
        <tr><td>\( V_{ll} \) / \( f_0 \)</td><td>400 V / 50 Hz</td></tr>
        <tr><td>\( V_0 \) (pico fase)</td><td>326.6 V</td></tr>
        <tr><td>\( \omega_0 \)</td><td>314.16 rad/s</td></tr>
        <tr><td>\( V_{dc} \)</td><td>750 V</td></tr>
      </table>
      <h3>A.2 Filtro LCL</h3>
      <table>
        <tr><th>Parámetro</th><th>Valor</th></tr>
        <tr><td>\( L_1 \) / \( R_1 \)</td><td>2 mH / 0.10 Ω</td></tr>
        <tr><td>\( C_f \)</td><td>20 µF</td></tr>
        <tr><td>\( L_2 \) / \( R_2 \)</td><td>1 mH / 0.05 Ω</td></tr>
        <tr><td>\( f_\text{res} \)</td><td>~1.1 kHz</td></tr>
      </table>
    </div>
    <div>
      <h3>A.3 Control</h3>
      <table>
        <tr><th>Parámetro</th><th>Valor</th></tr>
        <tr><td>BW corriente \( f_{ci} \)</td><td>1000 Hz</td></tr>
        <tr><td>BW tensión \( f_{cv} \)</td><td>350 Hz</td></tr>
        <tr><td>Amort. activo \( K_\text{ad} \)</td><td>6 Ω</td></tr>
        <tr><td>Droop P / Q</td><td>0.5 % / 2 %</td></tr>
        <tr><td>Filtro potencia \( f_\text{pow} \)</td><td>15 Hz</td></tr>
        <tr><td>Inercia VSM \( H \)</td><td>4 s</td></tr>
      </table>
      <h3>A.4 Impedancia virtual y operación</h3>
      <table>
        <tr><th>Parámetro</th><th>Valor</th></tr>
        <tr><td>\( R_v \) / \( L_v \)</td><td>0.2 Ω / 8 mH (Xv≈0.16 pu)</td></tr>
        <tr><td>\( R_{vt} \) / \( f_{ht} \)</td><td>2 Ω / 4 Hz</td></tr>
        <tr><td>\( P_\text{set} \) / \( Q_\text{set} \)</td><td>5 kW / 0 var</td></tr>
        <tr><td>\( Q_\text{eq} \) / \( \delta_\text{eq} \)</td><td>−554 var / 5.11°</td></tr>
      </table>
    </div>
  </div>
  <p class="small">Valores y ganancias derivadas: ver el código real en el cap. 7
  (<span class="file">params.py</span>).</p>
</section>

<section id="apB">
  <h2 class="sec">Apéndice B · Vector de estado (15 estados)</h2>
  <table>
    <tr><th>#</th><th>Estado</th><th>Significado</th><th>Grupo</th><th>Unidad</th></tr>
    <tr><td>0</td><td><code>iL1d</code></td><td>corriente inductor inversor, eje d</td><td>planta LCL</td><td>A</td></tr>
    <tr><td>1</td><td><code>iL1q</code></td><td>corriente inductor inversor, eje q</td><td>planta LCL</td><td>A</td></tr>
    <tr><td>2</td><td><code>vcd</code></td><td>tensión condensador, eje d</td><td>planta LCL</td><td>V</td></tr>
    <tr><td>3</td><td><code>vcq</code></td><td>tensión condensador, eje q</td><td>planta LCL</td><td>V</td></tr>
    <tr><td>4</td><td><code>iL2d</code></td><td>corriente a red (i_g), eje d</td><td>planta LCL</td><td>A</td></tr>
    <tr><td>5</td><td><code>iL2q</code></td><td>corriente a red (i_g), eje q</td><td>planta LCL</td><td>A</td></tr>
    <tr><td>6</td><td><code>delta</code></td><td>ángulo control − red</td><td>sincronización</td><td>rad</td></tr>
    <tr><td>7</td><td><code>Pm</code></td><td>potencia activa filtrada</td><td>sincronización</td><td>W</td></tr>
    <tr><td>8</td><td><code>Qm</code></td><td>potencia reactiva filtrada</td><td>sincronización</td><td>var</td></tr>
    <tr><td>9</td><td><code>xvd</code></td><td>integrador PI tensión, eje d</td><td>control</td><td>A·s</td></tr>
    <tr><td>10</td><td><code>xvq</code></td><td>integrador PI tensión, eje q</td><td>control</td><td>A·s</td></tr>
    <tr><td>11</td><td><code>xid</code></td><td>integrador PI corriente, eje d</td><td>control</td><td>V·s</td></tr>
    <tr><td>12</td><td><code>xiq</code></td><td>integrador PI corriente, eje q</td><td>control</td><td>V·s</td></tr>
    <tr><td>13</td><td><code>iL2d_lp</code></td><td>iL2d filtrada (R virtual transit.)</td><td>control</td><td>A</td></tr>
    <tr><td>14</td><td><code>iL2q_lp</code></td><td>iL2q filtrada (R virtual transit.)</td><td>control</td><td>A</td></tr>
  </table>
  <p>En simulación temporal (Fase 5) se añade el estado 15, \( \omega \) (frecuencia del VSM): 16 en total.</p>
</section>

<section id="apC">
  <h2 class="sec">Apéndice C · Código fuente del proyecto</h2>
  <p class="lead">Todos los ficheros de simulación, con su contenido real.</p>
  <p>Los ficheros principales están embebidos en sus capítulos (params §7, model §8, impedance §F2,
  grid §F3, inject/switched §F4, simulate §F5, diag_sweep §10, drivers en cada fase). Aquí se incluyen
  los dos auxiliares restantes para completitud.</p>
""" + embed("diagramas.py", "Genera los diagramas (esquema eléctrico, modelo, control) de la carpeta results/.")
   + embed("plecs_cosim.py", "Plantilla de co-simulación XML-RPC con PLECS para la validación sobre el modelo conmutado.")
   + r"""
  <div class="note">Resumen de ficheros: <span class="file">params.py</span>
  <span class="file">model.py</span> <span class="file">impedance.py</span>
  <span class="file">grid.py</span> <span class="file">simulate.py</span>
  <span class="file">inject.py</span> <span class="file">switched.py</span>
  <span class="file">diag_sweep.py</span> <span class="file">main_phase1…5.py</span>
  <span class="file">diagramas.py</span> <span class="file">plecs_cosim.py</span>. Este mismo informe lo
  genera <span class="file">gen_informe.py</span>, que lee estos ficheros y los embebe.</div>
</section>

<section id="apD">
  <h2 class="sec">Apéndice D · Resultados de consola (ejecución real)</h2>
  <p class="lead">Salida íntegra de cada script, capturada al ejecutarlo.</p>
  <h4>Fase 1 — <span class="file">main_phase1.py</span></h4>""" + console(R_PHASE1) + r"""
  <h4>Fase 2 — <span class="file">main_phase2.py</span></h4>""" + console(R_PHASE2) + r"""
  <h4>Fase 3 — <span class="file">main_phase3.py</span></h4>""" + console(R_PHASE3) + r"""
  <h4>Fase 4 — <span class="file">main_phase4.py</span></h4>""" + console(R_PHASE4) + r"""
  <h4>Fase 4b — <span class="file">switched.py</span></h4>""" + console(R_SWITCHED) + r"""
  <h4>Fase 5 — <span class="file">main_phase5.py</span></h4>""" + console(R_PHASE5) + r"""
  <h4>Diagnóstico — <span class="file">diag_sweep.py</span></h4>""" + console(R_DIAG) + r"""
</section>

<section id="apE">
  <h2 class="sec">Apéndice E · Cómo reproducir</h2>
  <figure style="margin:18px auto;max-width:860px;text-align:center"><img src="results/flujo_codigo.png" alt="flujo de datos del codigo">
    <figcaption>Flujo de datos del código: <span class="file">params.py</span> → modelo no lineal \( f(x,u) \) →
    equilibrio (fsolve) → linealización numérica \( (A,B,C,D) \) → los cuatro análisis (polos, impedancia,
    Nyquist, simulación) de las fases.</figcaption></figure>
  <pre>python main_phase1.py    # equilibrio, polos          -> results/polos_fase1.png
python main_phase2.py    # impedancia dq Z(jw)        -> results/impedancia_fase2.png
python main_phase3.py    # estabilidad red debil      -> results/nyquist_fase3.png
python main_phase4.py    # validacion por inyeccion   -> results/fase4_validacion.png
python switched.py       # promediado vs conmutado    -> results/fase4b_averaging.png
python main_phase5.py    # droop vs VSM, limiting     -> results/fase5_*.png
python diag_sweep.py     # barrido de diagnostico
python figuras_modelo.py # estructura de A + flujo      -> results/matriz_A.png, flujo_codigo.png
python gen_informe.py    # regenera este informe.html</pre>
  <p class="small">Requiere Python 3.13 con NumPy, SciPy y Matplotlib. Todas las figuras se escriben en
  <code class="inl">results/</code>.</p>
</section>

<section id="apF">
  <h2 class="sec">Apéndice F · Glosario</h2>
  <table>
    <tr><td><b>GFM / GFL</b></td><td>Grid-forming (impone tensión) / grid-following (inyecta corriente).</td></tr>
    <tr><td><b>SCR / X·R</b></td><td>Short-circuit ratio (fortaleza de red) / relación reactancia-resistencia.</td></tr>
    <tr><td><b>marco dq</b></td><td>Referencia giratoria donde las magnitudes AC son constantes en régimen.</td></tr>
    <tr><td><b>droop / VSM</b></td><td>Control P-f, Q-V / máquina síncrona virtual (inercia por swing).</td></tr>
    <tr><td><b>impedancia virtual</b></td><td>Impedancia emulada restándola de la referencia de tensión.</td></tr>
    <tr><td><b>amortiguamiento activo</b></td><td>Amortigua la resonancia LCL por realimentación, sin R física.</td></tr>
    <tr><td><b>minor loop gain</b></td><td>\( L=Z_\text{red}Y_\text{inv} \); su Nyquist decide la estabilidad.</td></tr>
    <tr><td><b>anti-windup</b></td><td>Congelar el integrador al saturar la salida.</td></tr>
    <tr><td><b>RoCoF</b></td><td>Velocidad de cambio de frecuencia.</td></tr>
  </table>
  <p class="small" style="margin-top:24px">Definiciones extensas en el
  <a href="../00%20-%20Repositorio/index.html">repositorio de conocimiento</a>.</p>
</section>
""")

# ====================================================================== #
#  ENSAMBLADO
# ====================================================================== #
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
out_path = os.path.join(HERE, "informe.html")
with open(out_path, "w", encoding="utf-8") as fh:
    fh.write(html_out)
print(f"informe.html generado: {html_out.count(chr(10))+1} lineas, {len(html_out)} bytes")

