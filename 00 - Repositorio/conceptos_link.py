"""Auto-enlazador de conceptos para los informes.

Envuelve la PRIMERA aparicion (en todo el informe) de cada concepto del
repositorio con un enlace inline a su ficha en index.html#<slug>. Salta
titulos, codigo, anclas ya existentes y MathJax para no romper el HTML.

Uso en gen_informe.py:
    import sys, os
    sys.path.insert(0, os.path.join(HERE, "..", "00 - Repositorio"))
    from conceptos_link import link_concepts
    ...
    html_out = HEAD + NAV + HERO + link_concepts("".join(S)) + FOOT

Para anadir conceptos: amplia CONCEPTS con {slug: [terminos...]}. Un slug que
no exista como ficha real (conceptos/**/<slug>.md) se ignora, asi nunca se
generan enlaces muertos.
"""
import os, re, glob

_REPO = os.path.dirname(os.path.abspath(__file__))
HREF = "../00%20-%20Repositorio/index.html#"

# Slugs reales = nombre de cada ficha en conceptos/. Filtra terminos invalidos.
VALID = {os.path.splitext(os.path.basename(p))[0]
         for p in glob.glob(os.path.join(_REPO, "conceptos", "**", "*.md"), recursive=True)}

# slug -> terminos en prosa (variantes). Evita palabras genericas ("control",
# "red", "modelo") y prefiere multipalabra o acronimos distintivos.
CONCEPTS = {
    # --- fisica / modelado ---
    "marco-dq":              ["marco dq", "transformada de Park", "transformada de Clarke"],
    "filtro-lcl":            ["filtro LCL", "resonancia del filtro LCL", "resonancia LCL", "amortiguamiento activo"],
    "red-thevenin-scr":      ["equivalente Thévenin", "red Thévenin", "Thévenin", "red débil"],
    "convertidor-vsc":       ["convertidor VSC", "VSC", "modulación PWM", "PWM", "modelo promediado"],
    "sistema-trifasico":     ["sistema trifásico"],
    "potencia-instantanea-dq": ["potencia instantánea"],
    "potencia-ac-fasores":   ["fasores"],
    "representacion-espacio-estados": ["espacio de estados"],
    "variables-estado":      ["variables de estado"],
    "sistema-por-unidad":    ["por unidad", "p.u."],
    "generador-sincrono":    ["generador síncrono"],
    "microrred-hibrida-ac-dc": ["microrred híbrida"],
    "modelo-bateria-bess":   ["BESS"],
    "fotovoltaica-mppt":     ["fotovoltaica"],
    "eolica-mppt":           ["eólica"],
    "carga-pulsante-datacenter-ia": ["carga pulsante"],
    "topologias-multinivel": ["multinivel"],
    # --- control ---
    "antiresonancia":        ["antiresonancia", "antirresonancia"],
    "frecuencias-segundo-orden": ["frecuencia amortiguada", "frecuencia de pico", "frecuencia natural"],
    "factor-calidad-q":          ["factor de calidad", "factor Q"],
    "series-taylor":             ["serie de Taylor", "series de Taylor", "polinomio de Taylor"],
    "amortiguamiento-pasivo-vs-activo": ["amortiguamiento pasivo", "amortiguamiento activo"],
    "impedancia-virtual":    ["impedancia virtual"],
    "current-limiting":      ["limitación de corriente", "current limiting"],
    "control-cascada":       ["control en cascada", "lazos anidados"],
    "desacoplo-dq":          ["desacoplo dq", "desacoplo"],
    "pll-srf":               ["PLL", "DSOGI"],
    "interaccion-pll-red-debil": ["interacción PLL"],
    "analisis-modal":        ["análisis modal", "autovalores", "factores de participación"],
    "impedancia-salida-estabilidad": ["estabilidad por impedancia", "impedancia de salida", "resistencia negativa", "no pasividad", "impedancia dq"],
    "vsm-inercia":           ["máquina síncrona virtual", "inercia virtual", "VSM"],
    "droop-dc":              ["droop DC"],
    "droop-control":         ["droop"],
    "grid-forming-vs-following": ["grid-forming", "grid-following", "GFM", "GFL"],
    "anti-windup":           ["anti-windup"],
    "criterio-nyquist":      ["criterio de Nyquist"],
    "dinamica-bus-dc":       ["estabilidad del bus DC", "bus DC", "carga de potencia constante", "CPL"],
    "controlador-pid":       ["controlador PID", "controlador PI", "control PI"],
    "controlador-resonante": ["controlador resonante"],
    "transformada-laplace":  ["transformada de Laplace"],
    "funcion-transferencia": ["función de transferencia"],
    "polos-ceros":           ["polos y ceros"],
    "diagrama-bode":         ["diagrama de Bode"],
    "lugar-raices":          ["lugar de las raíces", "lugar de raíces"],
    "realimentacion":        ["realimentación"],
    "observador-estados":    ["observador de estados"],
    "fenomenos-oscilatorios-red": ["estabilidad armónica", "oscilaciones subsíncronas", "fenómenos oscilatorios"],
    "fault-ride-through":    ["fault ride-through", "FRT"],
    "power-synchronization-control": ["power synchronization control", "PSC"],
    "virtual-oscillator-control": ["virtual oscillator control", "VOC"],
    "matching-control":      ["matching control"],
    "deteccion-islanding":   ["islanding"],
    "compensacion-retardo":  ["compensación de retardo", "retardo de cómputo"],
    "control-repetitivo":    ["control repetitivo"],
    "filtro-notch":          ["filtro notch"],
    "compensador-adelanto-atraso": ["adelanto-atraso", "lead-lag"],
    "control-vectorial":     ["control vectorial"],
    "error-regimen-permanente": ["error en régimen permanente"],
    "diagrama-bloques":      ["diagrama de bloques"],
    "routh-hurwitz":         ["Routh-Hurwitz"],
    "estabilidad-bibo":      ["BIBO"],
    # --- metodologia ---
    "nyquist-generalizado":  ["criterio de Nyquist generalizado", "Nyquist generalizado"],
    "criterio-middlebrook":  ["Middlebrook"],
    "margenes-estabilidad":  ["márgenes de estabilidad", "margen de fase", "margen de ganancia"],
    "robustez-parametrica":  ["robustez paramétrica"],
    "valores-singulares-mimo": ["valores singulares", "MIMO"],
    "funciones-sensibilidad": ["función de sensibilidad"],
    "loop-shaping":          ["loop shaping", "loop-shaping"],
    "asignacion-polos-lqr":  ["asignación de polos", "LQR"],
    "control-robusto-hinf":  ["control robusto", "H∞"],
    "control-predictivo":    ["control predictivo", "MPC"],
    "sintonia-pi-pid":       ["sintonía PID", "sintonía PI"],
    "clasificacion-estabilidad": ["clasificación de estabilidad"],
    "servicios-red-soporte": ["servicios de red"],
    "control-jerarquico-microrred": ["control jerárquico"],
    "calidad-potencia":      ["calidad de potencia", "THD"],
    "especificaciones-control": ["especificaciones de control"],
    "metricas-desempeno":    ["métricas de desempeño"],
    # --- programacion ---
    "medicion-impedancia-inyeccion": ["medición por inyección", "inyección de perturbación"],
    "respuesta-frecuencia-ss": ["respuesta en frecuencia"],
    "linealizacion-numerica": ["linealización numérica", "Jacobiano", "diferencias finitas"],
    "integracion-edos-stiff": ["EDOs stiff", "rigidez numérica"],
    "equilibrio-fsolve":     ["fsolve", "punto de equilibrio"],
    "fft-analisis-espectral": ["FFT"],
    "discretizacion-controladores": ["discretización"],
    "hil-phil":              ["PHIL", "HIL"],
}

# Regiones que NO se deben tocar (se copian verbatim).
_PROTECTED = re.compile(
    r"(?s)("
    r"<pre\b[^>]*>.*?</pre>"      r"|"
    r"<code\b[^>]*>.*?</code>"    r"|"
    r"<a\b[^>]*>.*?</a>"          r"|"
    r"<h[1-6]\b[^>]*>.*?</h[1-6]>" r"|"
    r"<script\b[^>]*>.*?</script>" r"|"
    r"<style\b[^>]*>.*?</style>"   r"|"
    r"\\\(.*?\\\)"               r"|"   # MathJax inline  \( ... \)
    r"\\\[.*?\\\]"               r"|"   # MathJax display \[ ... \]
    r"\$\$.*?\$\$"               r"|"   # MathJax $$ ... $$
    r"<[^>]+>"                          # cualquier etiqueta suelta
    r")"
)


def _build_terms():
    pairs = []
    for slug, terms in CONCEPTS.items():
        if slug not in VALID:
            continue
        for t in terms:
            pairs.append((t, slug))
    pairs.sort(key=lambda p: len(p[0]), reverse=True)   # frase larga antes que corta
    out = []
    for t, slug in pairs:
        pat = re.compile(r"(?<![\w-])" + re.escape(t) + r"(?![\w-])", re.IGNORECASE)
        out.append((pat, slug))
    return out


_TERMS = _build_terms()


def _linkify(text, used, store):
    for pat, slug in _TERMS:
        if slug in used:
            continue
        def repl(m, _slug=slug):
            used.add(_slug)
            idx = len(store)
            store.append('<a class="cref" href="%s%s">%s</a>' % (HREF, _slug, m.group(0)))
            return "\x00%d\x00" % idx
        text = pat.sub(repl, text, count=1)
    return text


def link_concepts(body):
    """Enlaza la 1a aparicion de cada concepto en `body` (cuerpo del informe)."""
    used, store = set(), []
    out, pos = [], 0
    for m in _PROTECTED.finditer(body):
        out.append(_linkify(body[pos:m.start()], used, store))
        out.append(m.group(0))
        pos = m.end()
    out.append(_linkify(body[pos:], used, store))
    res = "".join(out)
    return re.sub(r"\x00(\d+)\x00", lambda m: store[int(m.group(1))], res)
