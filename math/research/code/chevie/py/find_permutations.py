"""
find_permutations.py

For each label in a given list, reads:
  - chevie/chevie_charinfo_[label].txt
  - x/x_[label].txt

and prints the permutation (1-indexed) that maps the ith entry of CharInfo
to the a_i-th entry of X, as a space-separated sequence.

Normalisation rules:
  - CharInfo entries: strip LaTeX 'phi_' prefix; normalise braces/cdot
  - X entries: strip leading 'X' or 'Xphi' prefix; normalise braces
  - Both: map cdot -> . and strip whitespace
"""

import re

def normalise(s):
    s = s.strip()
    # Strip icc prefix: 'Xphi{' -> '{', 'X' -> ''
    if s.startswith('Xphi{'):
        s = s[4:]           # remove 'Xphi', leaving '{a,b}'
    elif s.startswith('X'):
        s = s[1:]           # remove 'X'
    # Strip charinfo LaTeX prefix: '\phi_{' -> '{', or '\phi_' -> ''
    s = re.sub(r'\\phi_\{', '{', s)
    s = re.sub(r'\\phi_', '', s)
    # Normalise braces: {a,b} -> a,b  (so Xphi{1,0} and \phi_{1,0} both -> 1,0)
    s = re.sub(r'^\{(.+)\}$', r'\1', s)
    # \cdot -> .
    s = s.replace(r'\cdot', '.')
    # remove spaces before + or - (e.g. '111. +' -> '111.+')
    s = re.sub(r'\s+([+-])$', r'\1', s)
    # for D-type entries: drop dot immediately before +/- (e.g. '111.+' -> '111+')
    s = re.sub(r'\.([+-])$', r'\1', s)
    # normalise whitespace
    s = s.strip()
    return s

with open(f'labels.txt') as f:
    labels = re.split('\n+', f.read().strip())

lines = []

for label in labels:
    charinfo_path = f'chevie/chevie_charinfo_{label}.txt'
    x_path      = f'x/x_{label}.txt'

    with open(charinfo_path) as f:
        charinfo = [l.strip() for l in f.read().strip().split('\n')]
    with open(x_path) as f:
        x      = [l.strip() for l in f.read().strip().split('\n')]

    charinfo_norm = [normalise(s) for s in charinfo]
    x_norm      = [normalise(s) for s in x]

    # Build index map: normalised label -> 1-based position in icc
    x_index = {}
    for i, s in enumerate(x_norm):
        x_index[s] = i + 1

    perm = []
    errors = []
    for i, s in enumerate(charinfo_norm):
        if s in x_index:
            perm.append(x_index[s])
        else:
            perm.append(None)
            errors.append(f"  charinfo[{i+1}] = {charinfo[i]!r} -> norm={s!r} NOT FOUND in icc")

    if errors:
        print(f"\n[{label.upper()}] ERRORS:")
        for e in errors:
            print(e)
    else:
        lines.append(f'[{label}]\n' + ' '.join(str(a) for a in perm) + '\n')

output = '\n'.join(lines)

with open('permutations.txt', 'w') as f:
    f.write(output)
print(output)


