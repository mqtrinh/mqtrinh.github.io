import re


def parse_lp(s):
    """Parse a Laurent polynomial string into a dict {exp: coeff}."""
    s = s.strip()
    s = re.sub(r'\^{([^}]*)}', r'^\1', s)   # x^{-1} -> x^-1
    s = re.sub(r'(?<=[0-9x])-', '+-', s)    # insert + before internal -
    terms = [t for t in s.split('+') if t.strip()]
    poly = {}
    for term in terms:
        term = term.strip()
        if not term:
            continue
        if term.startswith('-'):
            sign = -1
            term = term[1:]
        else:
            sign = 1
        if 'x' not in term:
            coeff = int(term) if term else 1
            exp = 0
        else:
            parts = term.split('x', 1)
            c_part, e_part = parts
            coeff = int(c_part) if c_part != '' else 1
            exp = 1 if e_part == '' else int(e_part[1:])
        poly[exp] = poly.get(exp, 0) + sign * coeff
    return {k: v for k, v in poly.items() if v != 0}

def check_unimodal(coeffs):
    """Return True if seq is unimodal (weakly increases then weakly decreases)."""
    if len(coeffs) <= 1:
        return False
    abs_coeffs = [abs(c) for c in coeffs]
    for i in range(1, len(coeffs) // 2 + 1):
        if abs_coeffs[i] < abs_coeffs[i-1]:
            return True
    return False

def check_signs(coeffs):
    if all(c <= 0 for c in coeffs):
        return True, False
    if any(c > 0 for c in coeffs) and any(c < 0 for c in coeffs):
        return False, True
    return False, False

def read_vectors(filepath):
    with open(filepath) as f:
        raw = f.read()
    blocks = re.split(r'(#[0-9]+ [^\n]*)\n', raw)
    headers, vectors_raw = [], []
    i = 1
    while i < len(blocks):
        headers.append(blocks[i].strip())
        content = blocks[i+1].strip().split('\n')
        vectors_raw.append([l.strip() for l in content if l.strip()])
        i += 2
    return headers, vectors_raw

def formatter(i, list, lines, x, y, family_to_special):
    if list:
        for i in list:
            special_i = family_to_special[i + 1]
            lines.append("  family " + "{:<12}".format(x[special_i - 1]) + " = " + "{:<20}".format(y[special_i - 1]))
    else:
        lines.append("  none")

with open(f'test/mode.txt') as f:
    mode = f.read().strip()

with open(f'test/labels_{mode}.txt') as f:
    labels = re.split('\n+', f.read().strip())

for label in labels:
    with open(f'families/families_{label}.txt') as f:
        families = re.split('\n', f.read().strip())
    with open(f'x/x_{label}.txt') as f:
        x = [s[1:] for s in re.split('\n', f.read().strip())]
    with open(f'y/y_{label}.txt') as f:
        y = re.split('\n', f.read().strip())
    
    input_file  = f'test/{mode}/{label}_{mode}_summed.txt'
    output_file = f'test/{mode}/{label}_{mode}_tested.txt'

    family_to_special = [None] # family_to_special takes 1-indexing to 1-indexing
    for i in range(len(families)):
        family_str = re.split(',', families[i].strip())
        for j in range(len(family_str)):
            if family_str[j][0] == "*": # each family contains exactly one special element
                family_to_special.append(int(family_str[j][1:]))

    headers, vectors_raw = read_vectors(input_file)

    nonunimodal_headers, mixed_headers, negative_headers = [], [], []
    nonunimodal_fam, mixed_fam, negative_fam = set(), set(), set()

    for header, v in zip(headers, vectors_raw):
        nonunimodal_temp, mixed_temp, negative_temp = [], [], []

        for i in range(len(v)):
            s = v[i].strip()
            if s != "0":
                poly = parse_lp(s)
                coeffs = list(poly.values())
                if check_unimodal(coeffs):
                    nonunimodal_fam.add(i)
                    nonunimodal_temp.append(i)
                fneg, fmixed = check_signs(coeffs)
                if fmixed:
                    mixed_fam.add(i)
                    mixed_temp.append(i)
                if fneg: 
                    negative_fam.add(i)
                    negative_temp.append(i)
            
        if nonunimodal_temp: nonunimodal_headers.append((header, nonunimodal_temp))
        if mixed_temp: mixed_headers.append((header, mixed_temp))
        if negative_temp: negative_headers.append((header, negative_temp))

    lines = []
    lines.append(f"\n{len(nonunimodal_headers)} entries where some sequence of nonzero coeffs is not unimodal in abs value.")
    if nonunimodal_headers:
        for header, nonunimodal_temp in nonunimodal_headers:
            lines.append(f"\n  {header}")
            for i in nonunimodal_temp:
                lines.append(f"    {x[i]}: {vectors_raw[headers.index(header)][i]}")
    lines.append(f"\n{len(mixed_headers)} entries where some polynomial has both positive and negative coeffs.")
    if mixed_headers:
        for header, mixed_temp in mixed_headers:
            lines.append(f"\n  {header}")
            for i in mixed_temp:
                lines.append(f"    {x[i]}: {vectors_raw[headers.index(header)][i]}")
    lines.append(f"\n{len(negative_headers)} entries where some polynomial has strictly negative coeffs.")
    if negative_headers:
        for header, negative_temp in negative_headers:
            lines.append(f"\n  {header}")
            for i in negative_temp:
                lines.append(f"    {x[i]}: {vectors_raw[headers.index(header)][i]}")

    lines_top = []

    lines_top.append(f"total num of chars: {len(x)}")
    lines_top.append(f"total num of families: {len(families)}")
    
    lines_top.append("families where some sequence of nonzero coeffs is not unimodal in abs value:")
    formatter(i, nonunimodal_fam, lines_top, x, y, family_to_special)
    lines_top.append("families where some polynomial has both positive and negative coeffs:")
    formatter(i, mixed_fam, lines_top, x, y, family_to_special)
    lines_top.append("families where some polynomial has strictly negative coeffs:")
    formatter(i, negative_fam, lines_top, x, y, family_to_special)

    output = '\n'.join(lines_top) + '\n' + '\n'.join(lines) + '\n'

    with open(output_file, 'w') as f:
        f.write(output)

    print(f'[{label}]')
    print('  ' + '\n  '.join(lines_top))