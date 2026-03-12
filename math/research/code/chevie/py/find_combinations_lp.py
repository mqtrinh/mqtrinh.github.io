import re, numpy as np
from collections import defaultdict
from scipy.optimize import linprog
from itertools import product as iproduct

# ── 1. Parse Laurent polynomials ──────────────────────────────────────────────

def parse_laurent(s):
    """Parse a Laurent polynomial string into a dict {exponent: coefficient}."""
    s = s.strip()
    if s == '0':
        return {}
    poly = defaultdict(int)
    pos = 0; n = len(s); pending_sign = '+'
    while pos < n:
        c = s[pos]
        if c == ' ': pos += 1; continue
        if c in '+-': pending_sign = c; pos += 1; continue
        coef_str = ''
        while pos < n and s[pos].isdigit(): coef_str += s[pos]; pos += 1
        has_x = pos < n and s[pos] == 'x'
        exp = None
        if has_x:
            pos += 1
            if pos < n and s[pos] == '^':
                pos += 1
                if pos < n and s[pos] == '{':
                    pos += 1; exp_str = ''
                    while s[pos] != '}': exp_str += s[pos]; pos += 1
                    pos += 1
                else:
                    # bare exponent: x^2
                    exp_str = ''
                    if pos < n and s[pos] == '-': exp_str += '-'; pos += 1
                    while pos < n and s[pos].isdigit(): exp_str += s[pos]; pos += 1
                exp = int(exp_str)
            else:
                exp = 1  # bare 'x'
        sign = -1 if pending_sign == '-' else 1; pending_sign = '+'
        if has_x:
            poly[exp] += sign * (int(coef_str) if coef_str else 1)
        elif coef_str:
            poly[0] += sign * int(coef_str)
    return {k: v for k, v in poly.items() if v != 0}

# ── 2. Parse the input file ───────────────────────────────────────────────────

def parse_blocks(filepath):
    """
    Parse a file of vectors separated by '#<number> <label>' headers.
    Returns a list of (header, vec) where vec is a list of Laurent poly dicts.
    """
    with open(filepath) as f:
        content = f.read()
    raw = re.split(r'(?=^#[0-9]+ )', content, flags=re.MULTILINE)
    blocks = []
    for block in raw:
        block = block.strip()
        if not block:
            continue
        lines = block.split('\n')
        header = lines[0].strip()
        entries = [l.strip() for l in lines[1:] if l.strip()]
        vec = [parse_laurent(e) for e in entries]
        blocks.append((header, vec))
    return blocks

# ── 3. Convert vectors to flat numpy arrays ───────────────────────────────────

def build_arrays(blocks):
    """
    Represent each vector as a flat numpy array.
    Axes: (entry position) x (Laurent exponent), flattened.
    """
    all_exps = set()
    for _, vec in blocks:
        for poly in vec:
            all_exps.update(poly.keys())
    all_exps = sorted(all_exps)
    dim = len(blocks[0][1])
    coords = [(pos, exp) for pos in range(dim) for exp in all_exps]
    coord_idx = {c: i for i, c in enumerate(coords)}

    def to_array(vec):
        arr = np.zeros(len(coords))
        for pos, poly in enumerate(vec):
            for exp, coef in poly.items():
                arr[coord_idx[(pos, exp)]] = coef
        return arr

    return [to_array(vec) for _, vec in blocks]

# ── 4. Main: find positive integer linear combinations ────────────────────────

def find_combinations(filepath):
    """
    For each vector v[i] in the file, check whether it can be expressed as a
    positive integer linear combination of the vectors v[1], ..., v[i-1] that
    precede it.

    Strategy:
      1. Solve the LP relaxation (continuous c_j >= 0).
         If infeasible, no integer solution exists either.
      2. If feasible, identify the support (nonzero LP variables) and do a
         small exhaustive integer search over those indices to find an exact
         integer solution.
      3. Fall back to rounding the LP solution and checking exactly.
    """
    blocks = parse_blocks(filepath)
    arrays = build_arrays(blocks)
    print(f"Loaded {len(blocks)} vectors.\n")

    results = []

    for i in range(1, len(blocks)):
        header = blocks[i][0]
        b = arrays[i]

        if np.allclose(b, 0):
            continue

        # Matrix of earlier vectors as columns
        A = np.column_stack([arrays[j] for j in range(i)])  # shape (K, i)

        # LP: find c >= 0 such that A @ c = b  (feasibility only)
        c_obj = np.zeros(i)
        result = linprog(c_obj, A_eq=A, b_eq=b, bounds=[(0, None)] * i, method='highs')

        if result.status != 0:
            continue  # LP infeasible → no integer solution

        c_lp = result.x
        support = [j for j in range(i) if c_lp[j] > 1e-6]

        if not support:
            continue

        # Upper bound on integer coefficients
        max_b = max((abs(v) for v in b if abs(v) > 1e-9), default=1)
        max_c = min(int(max_b) + 2, 20)

        found = None

        # Exhaustive integer search over the LP support (usually 1-3 vectors)
        if len(support) <= 4:
            for cs in iproduct(*[range(1, max_c + 1)] * len(support)):
                combo_vec = sum(cs[k] * arrays[support[k]] for k in range(len(support)))
                if np.allclose(combo_vec, b):
                    found = [(cs[k], support[k]) for k in range(len(support))]
                    break

        # Fallback: try rounding the LP solution directly
        if found is None:
            c_rounded = np.maximum(np.round(c_lp).astype(int), 0)
            if np.allclose(A @ c_rounded.astype(float), b):
                found = [(c_rounded[j], j) for j in range(i) if c_rounded[j] > 0]

        if found:
            results.append((i + 1, header, found))

    # ── Report ────────────────────────────────────────────────────────────────
    print("=" * 60)
    if not results:
        print("No vector is a positive integer linear combination of earlier vectors.")
    else:
        for idx, header, combo in results:
            terms = [f"{c}·v[{j+1}]  ({blocks[j][0]})" for c, j in combo]
            print(f"v[{idx}]  {header}")
            print("  = " + "\n  + ".join(terms))
            print()


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python find_combinations_lp.py <input_file.txt>")
        sys.exit(1)
    find_combinations(sys.argv[1])
