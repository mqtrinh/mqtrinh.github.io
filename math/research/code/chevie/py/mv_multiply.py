"""
mv_multiply.py

Usage:
    python3 mv_multiply.py <vector_file> <matrix_file> <output_file>

Given a file of column vectors of Laurent polynomials in the format of
exotic_b2_dedup.txt, and a matrix in CSV format, computes M*v for each
column vector v and writes the results to the output file in the same format.
"""

import re

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
    labels, vectors_raw = [], []
    i = 1
    while i < len(blocks):
        labels.append(blocks[i].strip())
        content = blocks[i+1].strip().split('\n')
        vectors_raw.append([l.strip() for l in content if l.strip()])
        i += 2
    return labels, vectors_raw

def apply_matrix(M, labels, vectors_raw):
    output_blocks = []
    for label, v_strs in zip(labels, vectors_raw):
        v = [parse_lp(s) for s in v_strs]
        result = []
        for row in M:
            entry = {}
            for j, c in enumerate(row):
                if c != 0:
                    entry = lp_add(entry, lp_scale(c, v[j]))
            result.append(lp_to_str(entry))
        output_blocks.append(label + '\n\n' + '\n'.join(result))
    return '\n\n'.join(output_blocks) + '\n'

if __name__ == '__main__':
    import sys
    vec_file = sys.argv[1]
    mat_file = sys.argv[2]
    out_file = sys.argv[3]

    with open(mat_file) as f:
        M = [[int(x) for x in line.split(',')] for line in f.read().strip().split('\n')]

    labels, vectors_raw = read_vectors(vec_file)
    output = apply_matrix(M, labels, vectors_raw)

    with open(out_file, 'w') as f:
        f.write(output)
    print(f"Written to {out_file}")
