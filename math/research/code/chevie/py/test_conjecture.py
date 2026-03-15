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


labels = ['b2', 'g2', 'b3', 'b4', 'd4', 'f4', 'd5']

for label in labels:
    input_file  = f'exotic/exotic_{label}_summed.txt'
    output_file = f'exotic/exotic_{label}_tested.txt'

    headers, vectors_raw = read_vectors(input_file)

    nonunimodal_headers = []
    nonunimodal_indices = set()

    mixed_headers = []
    mixed_indices = set()

    neg_headers = []
    neg_indices = set()

    for header, v in zip(headers, vectors_raw):
        nonunimodal_temp = []
        neg_temp = []
        mixed_temp = [] 
        for i in range(len(v)):
            s = v[i].strip()
            if s != "0":
                poly = parse_lp(s)
                coeffs = list(poly.values())
                fnonunimodal = check_unimodal(coeffs)
                if fnonunimodal:
                    nonunimodal_indices.add(i+1)
                    nonunimodal_temp.append(i)
                fneg, fmixed = check_signs(coeffs)
                if fmixed:
                    mixed_indices.add(i+1)
                    mixed_temp.append(i)
                if fneg: 
                    neg_indices.add(i+1)
                    neg_temp.append(i)
            
        if nonunimodal_temp: nonunimodal_headers.append((header, nonunimodal_temp))
        if mixed_temp: mixed_headers.append((header, mixed_temp))
        if neg_temp: neg_headers.append((header, neg_temp))

    lines = []
    lines.append(f"\n{len(nonunimodal_headers)} entries where some sequence of nonzero coeffs is not unimodal in abs value.")
    if nonunimodal_headers:
        for header, nonunimodal_temp in nonunimodal_headers:
            lines.append(f"\n  {header}")
            for i in nonunimodal_temp:
                lines.append(f"    line {i+1}: {vectors_raw[headers.index(header)][i]}")
    lines.append(f"\n{len(mixed_headers)} entries where some polynomial has both positive and negative coeffs.")
    if mixed_headers:
        for header, mixed_temp in mixed_headers:
            lines.append(f"\n  {header}")
            for i in mixed_temp:
                lines.append(f"    line {i+1}: {vectors_raw[headers.index(header)][i]}")
    lines.append(f"\n{len(neg_headers)} entries where some polynomial has strictly negative coeffs.")
    if neg_headers:
        for header, neg_temp in neg_headers:
            lines.append(f"\n  {header}")
            for i in neg_temp:
                lines.append(f"    line {i+1}: {vectors_raw[headers.index(header)][i]}")

    nonunimodal_str = "Families where some sequence of nonzero coeffs is not unimodal in abs value: "
    if nonunimodal_indices:
        nonunimodal_list_str = ', '.join(str(i) for i in sorted(nonunimodal_indices))
        nonunimodal_str += f"#{nonunimodal_list_str}"
    else:
        nonunimodal_str += "none"
    
    mixed_str = "Families where some polynomial has both positive and negative coeffs: "
    if mixed_indices:
        mixed_list_str = ', '.join(str(i) for i in sorted(mixed_indices))
        mixed_str += f"#{mixed_list_str}"
    else:        
        mixed_str += "none"
    
    neg_str = "Families where some polynomial has strictly negative coeffs: "
    if neg_indices:
        neg_list_str = ', '.join(str(i) for i in sorted(neg_indices))
        neg_str += f"#{neg_list_str}"
    else:
        neg_str += "none"
    
    output = nonunimodal_str + '\n' + mixed_str + '\n' + neg_str + '\n' + '\n'.join(lines) + '\n'

    with open(output_file, 'w') as f:
        f.write(output)

    print(f'[{label}]')
    print('  ' + nonunimodal_str)
    print('  ' + mixed_str)
    print('  ' + neg_str)