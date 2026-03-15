"""
Reads families_[label].txt and exotic_[label].txt, and produces
exotic_[label]_summed.txt where each block's N-entry list is replaced
by a new list whose i-th entry is the sum of the Laurent polynomials
at the positions specified by line i of families_[label].txt.

Laurent polynomials are represented as dicts: exponent (int) -> coefficient (int).
"""

import re
from collections import defaultdict

# ---------------------------------------------------------------------------
# Laurent polynomial arithmetic
# ---------------------------------------------------------------------------

def poly_zero():
    return defaultdict(int)

def poly_parse(s):
    """Parse a Laurent polynomial string into a dict {exponent: coeff}.

    Handles terms like: 2x^3, x^{-2}, x, 2x, -x, 3, +x^{-1}
    Positive exponents appear as x^N (no braces); negative as x^{-N} (with braces).
    """
    s = s.strip()
    if s == '0':
        return poly_zero()

    result = poly_zero()

    # Match terms: optional sign, optional int coeff, optional x with optional exponent.
    # Exponent forms: ^N (no braces, positive) or ^{±N} (with braces).
    tok_pat = re.compile(
        r'([+-]?)'                                 # sign
        r'(\d*)'                                   # coefficient digits (empty -> 1)
        r'(?:(x)'                                  # literal 'x'
          r'(?:\^(?:\{([+-]?\d+)\}|(\d+)))?'      # optional exponent: ^{±N} or ^N
        r')?'
    )

    for m in tok_pat.finditer(s):
        sign_s, coeff_s, has_x, exp_braced, exp_plain = m.groups()
        if not m.group(0):
            continue

        if has_x:
            coeff = int(sign_s + coeff_s) if coeff_s else (1 if sign_s != '-' else -1)
            if exp_braced is not None:
                exp = int(exp_braced)
            elif exp_plain is not None:
                exp = int(exp_plain)
            else:
                exp = 1
        else:
            if not coeff_s:
                continue
            coeff = int(sign_s + coeff_s) if coeff_s else 0
            exp = 0

        result[exp] += coeff

    return result

def poly_add(p, q):
    r = defaultdict(int, p)
    for exp, coeff in q.items():
        r[exp] += coeff
    return r

def poly_to_str(p):
    """Convert a Laurent polynomial dict back to a canonical string.
    Positive exponents: x^N (no braces). Negative: x^{-N} (with braces).
    """
    terms = {e: c for e, c in p.items() if c != 0}
    if not terms:
        return '0'

    exponents = sorted(terms.keys(), reverse=True)
    parts = []
    for exp in exponents:
        coeff = terms[exp]
        if exp == 0:
            parts.append(str(coeff))
        elif exp == 1:
            parts.append('x' if coeff == 1 else ('-x' if coeff == -1 else f'{coeff}x'))
        else:
            # positive exponents: x^N, negative: x^{-N}
            exp_str = f'x^{exp}' if exp > 0 else f'x^{{{exp}}}'
            parts.append(exp_str if coeff == 1 else (f'-{exp_str}' if coeff == -1 else f'{coeff}{exp_str}'))

    return '+'.join(parts).replace('+-', '-')


# ---------------------------------------------------------------------------
# File parsing
# ---------------------------------------------------------------------------

def parse_families(filepath):
    """Return list of lists of 1-based indices."""
    families = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line:
                families.append([int(x) for x in line.split(',')])
    return families

def parse_exotic(filepath):
    """
    Return list of blocks. Each block is:
      {'header': str, 'entries': [str, ...]}
    where entries are the N Laurent polynomial strings.
    """
    blocks = []
    current_header = None
    current_entries = []
    in_block = False

    with open(filepath) as f:
        for line in f:
            line = line.rstrip('\n')
            stripped = line.strip()

            if stripped.startswith('#'):
                # Save previous block
                if current_header is not None:
                    blocks.append({'header': current_header, 'entries': current_entries})
                current_header = stripped
                current_entries = []
                in_block = True
            elif in_block and stripped == '':
                # blank line after header or between entries — skip
                continue
            elif in_block:
                current_entries.append(stripped)

    if current_header is not None and current_entries:
        blocks.append({'header': current_header, 'entries': current_entries})

    return blocks


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------

labels = ['b2', 'g2', 'b3', 'b4', 'd4', 'f4', 'd5']

for label in labels:
    fam_file    = f'families/families_{label}.txt'
    exotic_file = f'exotic/exotic_{label}_solved.txt'
    out_file    = f'exotic/exotic_{label}_summed.txt'

    families = parse_families(fam_file)
    blocks   = parse_exotic(exotic_file)

    N = max(max(fam) for fam in families)  # should equal len of each entry list
    F = len(families)

    out_lines = []
    for block in blocks:
        header  = block['header']
        entries = block['entries']
        assert len(entries) == N, f"Expected {N} entries, got {len(entries)} in {header}"

        # Parse all N polynomials
        polys = [poly_parse(e) for e in entries]

        # Compute F summed polynomials
        new_entries = []
        for fam in families:
            total = poly_zero()
            for idx in fam:
                total = poly_add(total, polys[idx - 1])  # 1-based
            new_entries.append(poly_to_str(total))

        out_lines.append(header)
        out_lines.append('')
        out_lines.extend(new_entries)
        out_lines.append('')

    with open(out_file, 'w') as f:
        f.write('\n'.join(out_lines) + '\n')

    print(f"[{label}] summed.")


