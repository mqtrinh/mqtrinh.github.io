import re, sys

mode = sys.argv[1]

def parse_lp(s):
    s = s.strip()
    s = re.sub(r'\^{([^}]*)}', r'^\1', s)
    s = re.sub(r'(?<=[0-9x])-', '+-', s)
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
            parts = term.split('x')
            c_part = parts[0]
            e_part = parts[1]
            coeff = int(c_part) if c_part != '' else 1
            exp = 1 if e_part == '' else int(e_part[1:])
        poly[exp] = poly.get(exp, 0) + sign * coeff
    return {k: v for k, v in poly.items() if v != 0}

def lp_add(a, b):
    result = dict(a)
    for k, v in b.items():
        result[k] = result.get(k, 0) + v
    return {k: v for k, v in result.items() if v != 0}

def lp_scale(c, a):
    return {k: c*v for k, v in a.items() if c*v != 0}

def lp_to_str(poly):
    if not poly:
        return '0'
    exps = sorted(poly.keys(), reverse=True)
    terms = []
    for e in exps:
        c = poly[e]
        if e == 0:
            terms.append(str(c))
        elif e == 1:
            terms.append(f'{c}x' if abs(c) != 1 else ('-x' if c == -1 else 'x'))
        elif e == -1:
            terms.append(f'{c}x^{{-1}}' if abs(c) != 1 else ('-x^{-1}' if c == -1 else 'x^{-1}'))
        elif e > 0:
            terms.append(f'{c}x^{e}' if abs(c) != 1 else ('x^' + str(e) if c == 1 else '-x^' + str(e)))
        else:
            terms.append(f'{c}x^{{{e}}}' if abs(c) != 1 else ('x^{' + str(e) + '}' if c == 1 else '-x^{' + str(e) + '}'))
    result = terms[0]
    for t in terms[1:]:
        if t.startswith('-'):
            result += t
        else:
            result += '+' + t
    return result

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

def apply_matrix(M, headers, vectors_raw):
    output_blocks = []
    for header, v_strs in zip(headers, vectors_raw):
        v = [parse_lp(s) for s in v_strs]
        result = []
        for row in M:
            entry = {}
            for j, c in enumerate(row):
                if c != 0:
                    entry = lp_add(entry, lp_scale(c, v[j]))
            result.append(lp_to_str(entry))
        output_blocks.append(header + '\n\n' + '\n'.join(result))
    return '\n\n'.join(output_blocks) + '\n'

with open(f'test/labels_{mode}.txt') as f:
    labels = re.split('\n+', f.read().strip())

for label in labels:
    # if mode == 'all': vec_file = f'test/{mode}/{label}_{mode}_trimmed.txt'
    # if mode == 'min': vec_file = f'test/{mode}/{label}_{mode}_sorted.txt'
    vec_file = f'test/{mode}/{label}_{mode}.txt'
    
    mat_file = f'icc/icc_{label}_inverted.txt'
    out_file = f'test/{mode}/{label}_{mode}_solved.txt'

    with open(mat_file) as f:
        M = [[int(x) for x in line.split(',')] for line in f.read().strip().split('\n')]

    headers, vectors_raw = read_vectors(vec_file)
    output = apply_matrix(M, headers, vectors_raw)

    with open(out_file, 'w') as f:
        f.write(output)
    print(f"[{label}] solved.")
