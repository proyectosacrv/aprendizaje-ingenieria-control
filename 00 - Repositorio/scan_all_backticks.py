"""Lista TODOS los backticks inline fuera de bloques de código (excluyendo frontmatter).
Muestra archivo:linea  `contenido` para revisión manual."""
import pathlib, re

CONCEPTS = pathlib.Path("conceptos")
issues = []

# Contenido que es claramente código legítimo -> ignorar
RE_CODE = re.compile(
    r'\.'           # ct.margin, np.array, etc.
    r'|\w+\s*\('    # llamada a función
    r'|True|False|None'
    r'|dtype|shape|axis|atol|rtol|xtol|tol'
    r'|max_step|t_eval|dense_output|full_output'
    r'|method=|bilinear|zoh|euler|backward|forward|tustin|prewarp'
    r'|>>|<<|//|%'
)

KNOWN_CODE = {
    'fsolve','solve_ivp','odeint','lsim','bode','nyquist','feedback','tf','ss',
    'place','margin','gram','ctrb','obsv','hanning','rfft','rfftfreq','c2d',
    'linspace','logspace','zeros','ones','eye','array','eigvals','eig',
    'matrix_rank','norm','polyfit','roots','minimize','brentq','bisect',
    'build.py','check_style.py','scan_backtick_math.py',
    'scipy','numpy','control','sympy','matplotlib',
    'step','impulse','root_locus','sample_system',
    'rtol','atol','idx_id','idx_vd','x0','xe','ier','msg','res',
}

for f in sorted(CONCEPTS.rglob("*.md")):
    text = f.read_text(encoding="utf-8")
    lines = text.splitlines()
    in_code_block = False
    in_front = False
    front_done = False
    front_count = 0

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # Frontmatter
        if i == 1 and stripped == '---':
            in_front = True; continue
        if in_front:
            if stripped == '---':
                front_count += 1
                if front_count >= 1:
                    in_front = False; front_done = True
            continue
        # Bloques de código
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        for m in re.finditer(r'`([^`]+)`', line):
            content = m.group(1).strip()
            if not content or len(content) > 60:
                continue
            if RE_CODE.search(content):
                continue
            if content.lower() in {c.lower() for c in KNOWN_CODE}:
                continue
            issues.append((f.name, i, content))

by_file = {}
for fname, lno, cont in issues:
    by_file.setdefault(fname, []).append((lno, cont))

for fname in sorted(by_file):
    print(f"\n=== {fname} ===")
    for lno, cont in by_file[fname]:
        print(f"  :{lno}  `{cont}`")

print(f"\nTotal: {sum(len(v) for v in by_file.values())} en {len(by_file)} archivos")
