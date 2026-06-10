"""Detecta ecuaciones en formato codigo fuera de bloques de codigo y MathJax."""
import pathlib, re

CONCEPTS = pathlib.Path("conceptos")
problems = []

for f in sorted(CONCEPTS.rglob("*.md")):
    text = f.read_text(encoding="utf-8")
    lines = text.splitlines()
    in_code = False
    in_math = False

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # tracking bloques ```
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue

        # Eliminar partes entre $$ y \( \) para no analizar matematicas ya correctas
        clean = re.sub(r"\$\$.*?\$\$", "", line, flags=re.S)
        clean = re.sub(r"\\\(.*?\\\)", "", clean)
        clean = re.sub(r"`[^`]+`", "", clean)  # eliminar codigo inline

        # 1. potencia Python x**n (excluir bold **texto**)
        if re.search(r"[A-Za-z0-9]\*\*[0-9]", clean):
            problems.append((f.name, i, "potencia x**n", line.strip()[:100]))

        # 2. multiplicacion Python 1.5*var o var*var sin espacio
        if re.search(r"[0-9]\*[A-Za-z]|[A-Za-z]\*[0-9]", clean):
            problems.append((f.name, i, "mult x*y", line.strip()[:100]))

        # 3. sqrt() fuera de MathJax
        if re.search(r"\bsqrt\s*\(", clean):
            problems.append((f.name, i, "sqrt()", line.strip()[:100]))

        # 4. subindice Python x_y como variable standalone (no en LaTeX)
        # busca patron "palabra_palabra" fuera de LaTeX/wikilink/frontmatter
        if re.search(r"\b[A-Za-z]{2,}_[A-Za-z]{2,}\b", clean) and i > 15:
            # excluir slugs de wikilinks, fechas, tags YAML
            if not re.search(r"\[\[|fecha_|slug:|tags:|relacionados:|objetivos:", line):
                problems.append((f.name, i, "subindice_texto", line.strip()[:100]))

        # 5. griegas escritas como palabras en contexto matematico (fuera de LaTeX)
        greek_words = r"\b(omega|lambda|delta|theta|phi|sigma|alpha|beta|gamma|zeta|tau|mu)\b"
        if re.search(greek_words, clean, re.IGNORECASE):
            # solo si parece contexto matematico (esta entre numeros, =, signos)
            if re.search(r"[=<>+\-*/][^a-z]*" + greek_words, clean, re.IGNORECASE) or \
               re.search(greek_words + r"[^a-z]*[=<>+\-*/]", clean, re.IGNORECASE):
                problems.append((f.name, i, "griega sin LaTeX", line.strip()[:100]))

for fname, lno, ptype, txt in sorted(problems):
    print(f"{fname}:{lno} [{ptype}]  {txt}")
print(f"\nTotal: {len(problems)} problemas")
