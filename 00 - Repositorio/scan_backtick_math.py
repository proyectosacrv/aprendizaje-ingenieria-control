"""
Detecta contenido en backticks inline que parece variable/formula matematica
(no codigo real: sin punto, sin parentesis de llamada, sin rutas/nombres de funcion conocidos).
"""
import pathlib, re, sys

CONCEPTS = pathlib.Path("conceptos")

# Nombres de funcion/herramienta/libreria que SON codigo legítimo en backticks
CODE_NAMES = {
    'fsolve','solve_ivp','odeint','ode','lsim','step','impulse','bode','nyquist',
    'root_locus','feedback','tf','ss','place','pole','zero','margin','gram','ctrb',
    'obsv','hanning','hamming','rfft','rfftfreq','sample_system','c2d','linspace',
    'logspace','arange','zeros','ones','eye','array','linalg','eigvals','eig',
    'matrix_rank','norm','allclose','argmax','argmin','where','abs','max','min',
    'sqrt','exp','log','cos','sin','pi','deg2rad','rad2deg','conj','real','imag',
    'angle','unwrap','interp','polyfit','polyval','roots','poly','lstsq',
    'fmin','minimize','fminbound','brentq','bisect','newton',
    'build','build.py','check_style','scan_backtick',
    'scipy','numpy','control','sympy','matplotlib','pandas',
    'IGBT','PWM','SPWM','SVPWM','ZOH','FFT','DFT','BIBO','CPL','SCR','VSC','PLL',
    'GFM','GFL','LVRT','FRT','MPPT','DFIG','PMSG','BESS','STATCOM','HVDC',
    'full_output','xtol','ier','msg','method','bilinear','prewarp',
    'droop_p','droop_q',  # ya estaban corregidos, pero por si acaso
}

# Patrones que indican codigo (tienen . :: / \ -> o son llamadas de funcion)
RE_CODE = re.compile(
    r'\.'         # metodos: ct.margin, np.array
    r'|::'        # rutas tipo Python
    r'|/[a-z]'   # rutas
    r'|\\[a-z]'  # rutas Windows
    r'|\w+\s*\('  # llamada a funcion
    r'|True|False|None|if |for |def |class |import |return '
    r'|dtype|shape|axis'
)

# Patron de variable/formula matematica pura
RE_MATH_VAR = re.compile(
    r'^[A-Za-z][A-Za-z0-9_\-]*$'  # identificador simple
    r'|^[A-Za-z]+\s*[=<>+\-*/^]\s*.*$'  # asignacion/ecuacion
    r'|^[0-9]+[\.,][0-9]+\s*[A-Za-z%]'  # numero con unidad
)

issues = []

for f in sorted(CONCEPTS.rglob("*.md")):
    text = f.read_text(encoding="utf-8")
    lines = text.splitlines()
    in_code_block = False

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        # Saltar frontmatter
        if i <= 16 and (stripped.startswith("---") or ":" in stripped):
            continue

        # Encontrar todos los backticks inline
        for m in re.finditer(r'`([^`]+)`', line):
            content = m.group(1).strip()
            if not content:
                continue
            # Skip si parece codigo real
            if RE_CODE.search(content):
                continue
            if content.lower() in {c.lower() for c in CODE_NAMES}:
                continue
            # Skip si es muy corto y no parece variable matematica
            if len(content) == 1 and content not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
                continue

            # Heuristica: ¿parece variable/formula matematica?
            is_math = False

            # Contiene subindice tipico o nombre de parametro de control
            math_patterns = [
                r'[A-Za-z]_[A-Za-z0-9]',  # subindice: x_d, V_dc
                r'[A-Za-z]+[0-9]$',         # K2, T1
                r'^[A-Z][a-z]$',            # Ki, Kp, Kv pero NO en, de, la
                r'^[A-Z]{1,2}$',            # L, C, R, P, Q, S pero NO OK
                r'^[a-z]{1,2}$',            # re, im, etc - skip
                r'omega|alpha|beta|gamma|delta|zeta|tau|lambda|sigma|phi|theta|mu|eta|xi|nu|rho|psi',
                r'[*]{2}[0-9]',             # x**2
                r'[0-9]\*[0-9a-zA-Z]',      # 2*pi
                r'sqrt\(',                   # sqrt(
                r'\bpu\b|p\.u\.',           # por unidad
            ]
            for pat in math_patterns:
                if re.search(pat, content, re.IGNORECASE):
                    is_math = True
                    break

            if is_math:
                issues.append((f.name, i, content, line.strip()[:120]))

# Agrupar por archivo
by_file = {}
for fname, lno, content, ctx in issues:
    by_file.setdefault(fname, []).append((lno, content, ctx))

for fname in sorted(by_file):
    for lno, content, ctx in by_file[fname]:
        print(f"{fname}:{lno}  `{content}`")
        print(f"   >> {ctx[:100]}")
    print()

print(f"Total: {sum(len(v) for v in by_file.values())} casos en {len(by_file)} archivos")
